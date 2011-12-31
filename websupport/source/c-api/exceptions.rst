.. highlightlang:: c


.. _exceptionhandling:

********
例外処理
********

この章で説明する関数を使うと、 Python の例外の処理や送出ができるようになります。 Python の例外処理の基本をいくらか理解することが大切です。
例外は Unix :c:data:`errno` 変数にやや似た機能を果たします: 発生した
中で最も新しいエラーの (スレッド毎の) グローバルなインジケータがあります。実行に成功した場合にはほとんどの関数がこれをクリアしませんが、失敗したときには
エラーの原因を示すために設定します。ほとんどの関数はエラーインジケータも返し、通常は関数がポインタを返すことになっている場合は *NULL* であり、
関数が整数を返す場合は ``-1`` です。(例外: :c:func:`PyArg_\*` 関数は
実行に成功したときに ``1`` を返し、失敗したときに ``0`` を返します).

ある関数が呼び出した関数がいくつか失敗したために、その関数が失敗しなければならないとき、一般的にエラーインジケータを設定しません。呼び出した関数が
すでに設定しています。エラーを処理して例外をクリアするか、あるいは (オブジェクト参照またはメモリ割り当てのような)それが持つどんなリソースも
取り除いた後に戻るかのどちらか一方を行う責任があります。エラーを処理する準備をしていなければ、普通に続けるべきでは *ありません* 。エラーのために
戻る場合は、エラーが設定されていると呼び出し元に知らせることが大切です。エラーが処理されていない場合または丁寧に伝えられている場合には、 Python/C
APIのさらなる呼び出しは意図した通りには動かない可能性があり、不可解な形で失敗するかもしれません。

.. index::
   single: exc_type (in module sys)
   single: exc_value (in module sys)
   single: exc_traceback (in module sys)

エラーインジケータは  Python変数 ``sys.exc_type``, ``sys.exc_value`` および
``sys.exc_traceback`` に対応する三つのPythonオブジェクトからからなります。
いろいろな方法でエラーインジケータとやりとりするためにAPI関数が存在します。各スレッドに別々のエラーインジケータがあります。

.. XXX Order of these should be more thoughtful.
   Either alphabetical or some kind of structure.


.. c:function:: void PyErr_PrintEx(int set_sys_last_vars)

   ``sys.stderr`` へ標準トレースバックをプリントし、エラーインジケータをクリアします。エラーインジケータが設定されているときにだけ、この関数を
   呼び出してください。(それ以外の場合、致命的なエラーを引き起こすでしょう!)

   *set_sys_last_vars* が非ゼロであれば、 :data:`sys.last_type`, :data:`sys.last_value`,
   :data:`sys.last_traceback` 変数が、表示される例外のタイプ、値、トレースバックそれぞれに
   反映されます。


.. c:function:: void PyErr_Print()

   ``PyErr_PrintEx(1)`` のエイリアス.


.. c:function:: PyObject* PyErr_Occurred()

   エラーインジケータが設定されているかテストします。設定されている場合は、例外の *型* (:c:func:`PyErr_Set\*` 関数の一つあるいは
   :c:func:`PyErr_Restore` への最も新しい呼び出しに対する第一引数)を返します。
   設定されていない場合は *NULL* を返します。あなたは戻り値への参照を持っていませんので、それに :c:func:`Py_DECREF` する必要はありません。

   .. note::

      戻り値を特定の例外と比較しないでください。その代わり、下に示す :c:func:`PyErr_ExceptionMatches` を
      使ってください。(比較は簡単に失敗するでしょう。なぜなら、例外はクラスではなくインスタンスかもしれないし、あるいは、クラス例外の場合は期待される例外の
      サブクラスかもしれないからです。)


.. c:function:: int PyErr_ExceptionMatches(PyObject *exc)

   ``PyErr_GivenExceptionMatches(PyErr_Occurred(), exc)`` と同じ。
   例外が実際に設定されたときにだけ、これを呼び出だすべきです。例外が発生していないならば、メモリアクセス違反が起きるでしょう。


.. c:function:: int PyErr_GivenExceptionMatches(PyObject *given, PyObject *exc)

   *given* 例外が *exc* の例外と一致するなら真を返します。これは *exc* が\
   クラスオブジェクトである場合も真を返します。これは *given* がサブクラスの\
   インスタンスであるときも真を返します。 *exc* がタプルならば、タプル内\
   (と再帰的にサブタプル内)のすべての例外が一致するか調べられます。


.. c:function:: void PyErr_NormalizeException(PyObject **exc, PyObject **val, PyObject **tb)

   ある状況では、以下の :c:func:`PyErr_Fetch` が返す値は "正規化されていない" 可能性があります。つまり、 ``*exc`` は
   クラスオブジェクトだが ``*val`` は同じクラスのインスタンスではないという意味です。この関数はそのような場合にそのクラスをインスタンス化
   するために使われます。その値がすでに正規化されている場合は何も起きません。遅延正規化はパフォーマンスを改善するために実装されています。


.. c:function:: void PyErr_Clear()

   エラーインジケータをクリアします。エラーインジケータが設定されていないならば、効果はありません。


.. c:function:: void PyErr_Fetch(PyObject **ptype, PyObject **pvalue, PyObject **ptraceback)

   エラーインジケータをアドレスを渡す三つの変数の中へ取り出します。エラーインジケータが設定されていない場合は、三つすべての変数を *NULL* に
   設定します。エラーインジケータが設定されている場合はクリアされ、あなたは取り出されたそれぞれのオブジェクトへの参照を持つことになります。
   型オブジェクトが *NULL* でないときでさえ、その値とトレースバックオブジェクトは *NULL* かもしれません。

   .. note::

      通常、この関数は例外を扱う必要のあるコードあるいはエラーインジケータを一時的に保存して元に戻す必要のあるコードによってのみ使用されます。


.. c:function:: void PyErr_Restore(PyObject *type, PyObject *value, PyObject *traceback)

   三つのオブジェクトからエラーインジケータを設定します。エラーインジケータがすでに設定されている場合は、最初にクリアされます。オブジェクトが *NULL* ならば、
   エラーインジケータがクリアされます。 *NULL* のtypeと非 *NULL* のvalueあるいは
   tracebackを渡してはいけません。例外の型(type)はクラスであるべきです。無効な例外の型(type)あるいは値(value)を渡してはいけません。
   (これらの規則を破ると後で気付きにくい問題の原因となるでしょう。) この呼び出しはそれぞれのオブジェクトへの参照を取り除きます: あなたは
   呼び出しの前にそれぞれのオブジェクトへの参照を持たなければならないのであり、また呼び出しの後にはもはやこれらの参照を持っていません。
   (これを理解していない場合は、この関数を使ってはいけません。注意しておきます。)

   .. note::

      通常この関数はエラーインジケータを一時的に保存し元に戻す必要のあるコードによってのみに使われます。現在の例外状態を保存するためには
      :c:func:`PyErr_Fetch` を使ってください。


.. c:function:: void PyErr_SetString(PyObject *type, const char *message)

   これはエラーインジケータを設定するための最も一般的な方法です。第一引数は
   例外の型を指定します。通常は標準例外の一つ、例えば :c:data:`PyExc_RuntimeError` です。
   その参照カウントを増加させる必要はありません。第二引数はエラーメッセージで、文字列オブジェクトへ変換されます。


.. c:function:: void PyErr_SetObject(PyObject *type, PyObject *value)

   この関数は :c:func:`PyErr_SetString` に似ていますが、
   例外の"値(value)"として任意のPythonオブジェクトを指定することができます。


.. c:function:: PyObject* PyErr_Format(PyObject *exception, const char *format, ...)

   この関数はエラーインジケータを設定し *NULL* を返します。
   *exception* はPython例外クラスであるべきです。
   *format* と以降の引数はエラーメッセージを作るためのもので,
   :c:func:`PyString_FromFormat` の引数と同じ意味を持っています。


.. c:function:: void PyErr_SetNone(PyObject *type)

   これは ``PyErr_SetObject(type, Py_None)`` を省略したものです。


.. c:function:: int PyErr_BadArgument()

   これは ``PyErr_SetString(PyExc_TypeError, message)`` を省略したもので、
   ここで *message* は組み込み操作が不正な引数で呼び出されたということを表しています。主に内部で使用するためのものです。


.. c:function:: PyObject* PyErr_NoMemory()

   これは ``PyErr_SetNone(PyExc_MemoryError)`` を省略したもので、 *NULL* を返します。したがって、メモリ不足になったとき、
   オブジェクト割り当て関数は ``return PyErr_NoMemory();`` と書くことができます。


.. c:function:: PyObject* PyErr_SetFromErrno(PyObject *type)

   .. index:: single: strerror()

   Cライブラリ関数がエラーを返してC変数 :c:data:`errno` を設定したときに、これは例外を発生させるために便利な関数です。第一要素が
   整数 :c:data:`errno` 値で、第二要素が (:c:func:`strerror` から得られる)対応する
   エラーメッセージであるタプルオブジェクトを構成します。それから、 ``PyErr_SetObject(type, object)`` を呼び出します。
   Unixでは、 :c:data:`errno` 値が :const:`EINTR` であるとき、すなわち割り込まれたシステムコールを表しているとき、これは
   :c:func:`PyErr_CheckSignals` を呼び出し、それがエラーインジケータを
   設定した場合は設定されたままにしておきます。関数は常に *NULL* を返します。したがって、システムコールがエラーを返したとき、システムコールの
   ラッパー関数は ``return PyErr_SetFromErrno(type);`` と書くことができます。


.. c:function:: PyObject* PyErr_SetFromErrnoWithFilename(PyObject *type, const char *filename)

   :c:func:`PyErr_SetFromErrno` に似ていて、 *filename* が *NULL* でない場合に、
   それが *type* のコンストラクタに第三引数として渡されるというふるまいが追加
   されています。 :exc:`IOError` と :exc:`OSError` のような例外の場合では、
   これが例外インスタンスの :attr:`filename` 属性を定義するために使われます。


.. c:function:: PyObject* PyErr_SetFromWindowsErr(int ierr)

   これは :exc:`WindowsError` を発生させるために便利な関数です。
   :c:data:`0` の *ierr* とともに呼び出された場合、 :c:func:`GetLastError` が
   返すエラーコードが代りに使われます。 *ierr* あるいは :c:func:`GetLastError` によって与えられるエラーコードのWindows用の説明を
   取り出すために、Win32関数 :c:func:`FormatMessage` を呼び出します。それから、
   第一要素が *ierr* 値で第二要素が(:c:func:`FormatMessage` から得られる)
   対応するエラーメッセージであるタプルオブジェクトを構成します。そして、 ``PyErr_SetObject(PyExc_WindowsError,
   object)`` を呼び出します。この関数は常に *NULL* を返します。利用可能範囲: Windows。


.. c:function:: PyObject* PyErr_SetExcFromWindowsErr(PyObject *type, int ierr)

   :c:func:`PyErr_SetFromWindowsErr` に似ていて、送出する例外の型を指定する引数が追加されています。利用可能範囲:
   Windows。

   .. versionadded:: 2.3


.. c:function:: PyObject* PyErr_SetFromWindowsErrWithFilename(int ierr, const char *filename)

   :c:func:`PyErr_SetFromWindowsErr` に似ていて、 *filename* が *NULL* でない場合には
   :exc:`WindowsError` のコンストラクタへ第三引数として渡されるという振る舞いが追加されています。利用可能範囲: Windows。


.. c:function:: PyObject* PyErr_SetExcFromWindowsErrWithFilename(PyObject *type, int ierr, char *filename)

   :c:func:`PyErr_SetFromWindowsErrWithFilename` に似ていて、発生させる例外の型を指定する引数が追加されています。
   利用可能範囲: Windows。

   .. versionadded:: 2.3


.. c:function:: void PyErr_BadInternalCall()

   ``PyErr_SetString(PyExc_SystemError, message)`` を省略したものです。
   ここで *message* は内部操作(例えば、Python/C API関数)が不正な引数と
   ともに呼び出されたということを示しています。主に内部で使用するためのものです。


.. c:function:: int PyErr_WarnEx(PyObject *category, char *message, int stacklevel)

   警告メッセージを出します。 *category* 引数は警告カテゴリ(以下を参照)
   かまたは *NULL* で、 *message* 引数はメッセージ文字列です。 *stacklevel* はフレームの数を示す正の整数です;
   警告はそのスタックフレームの中の実行している行から発行されます。 *stacklevel* が1だと、 :c:func:`PyErr_WarnEx` が、2だと
   その上の関数が、Warningの発行元になります。

   この関数は通常警告メッセージを *sys.stderr* へプリントします。けれども、ユーザが警告をエラーへ変更するように指定することも可能です。
   そのような場合には、これは例外を発生させます。警告機構がもつ問題のためにその関数が例外を発生させるということも可能です。(実装ではその厄介な仕事を
   行うために :mod:`warnings` モジュールをインポートします)。例外が発生させられなければ、戻り値は ``0`` です。あるいは、例外が発生させ
   られると ``-1`` です。(警告メッセージが実際にプリントされるかどうかを決定することはできず、また何がその例外の原因なのかを決定することもできない。
   これは意図的なものです。)例外が発生した場合、呼び出し元は通常の例外処理を行います(例えば、 :c:func:`Py_DECREF` は参照を持っており、エラー値を
   返します)。

   警告カテゴリは :c:data:`Warning` のサブクラスでなければならない。デフォルト警告カテゴリは :c:data:`RuntimeWarning` です。
   標準Python警告カテゴリは ``PyExc_`` にPython例外名が続く名前の
   グローバル変数を用いて変更できます。これらは型 :c:type:`PyObject\*` を持ち、すべてクラスオブジェクトです。それらの名前は
   :c:data:`PyExc_Warning`, :c:data:`PyExc_UserWarning`,
   :c:data:`PyExc_UnicodeWarning`, :c:data:`PyExc_DeprecationWarning`,
   :c:data:`PyExc_SyntaxWarning`, :c:data:`PyExc_RuntimeWarning`,
   :c:data:`PyExc_FutureWarning` です。
   :c:data:`PyExc_Warning` は :c:data:`PyExc_Exception` のサブクラスです。
   その他の警告カテゴリは :c:data:`PyExc_Warning` のサブクラスです。

   警告をコントロールするための情報については、 :mod:`warnings` モジュールのドキュメンテーションとコマンドライン・ドキュメンテーションの
   :option:`-W` オプションを参照してください。警告コントロールのためのC APIはありません。


.. c:function:: int PyErr_Warn(PyObject *category, char *message)

   警告メッセージを出します。 *category* 引数は警告カテゴリ(以下を参照) かまたは *NULL* で、 *message* 引数はメッセージ文字列です。警告は
   、 :c:func:`PyErr_WarnEx` を *stacklevel* に 1 を指定した時と同じく、 :c:func:`PyErr_Warn`
   を呼び出した関数から発行されます。

   非推奨; :c:func:`PyErr_WarnEx` を使って下さい。


.. c:function:: int PyErr_WarnExplicit(PyObject *category, const char *message, const char *filename, int lineno, const char *module, PyObject *registry)

   すべての警告の属性を明示的に制御した警告メッセージを出します。
   これはPython関数 :func:`warnings.warn_explicit` の直接的なラッパで、
   さらに情報を得るにはそちらを参照してください。そこに説明されているデフォルトの
   効果を得るために、 *module* と *registry* 引数は *NULL* に設定することができます。


.. c:function:: int PyErr_WarnPy3k(char *message, int stacklevel)

   Issue a :exc:`DeprecationWarning` with the given *message* and *stacklevel*
   if the :c:data:`Py_Py3kWarningFlag` flag is enabled.
   :c:data:`Py_Py3kWarningFlag` フラグが有効な場合、
   与えられた *message* と *stacklevel* に応じて :exc:`DeprecationWarning` を発生させます。

   .. versionadded:: 2.6


.. c:function:: int PyErr_CheckSignals()

   .. index::
      module: signal
      single: SIGINT
      single: KeyboardInterrupt (built-in exception)

   この関数はPythonのシグナル処理とやりとりすることができます。シグナルがそのプロセスへ送られたかどうかチェックし、そうならば対応する
   シグナルハンドラを呼び出します。 :mod:`signal` モジュールがサポートされている場合は、
   これはPythonで書かれたシグナルハンドラを呼び出せます。すべての場合で、 :const:`SIGINT` のデフォルトの効果は
   :exc:`KeyboardInterrupt` 例外を発生させることです。例外が発生した場合、エラーインジケータが設定され、関数は ``-1`` を返します。
   そうでなければ、関数は ``0`` を返します。エラーインジケータが以前に設定されている場合は、それがクリアされるかどうかわからない。


.. c:function:: void PyErr_SetInterrupt()

   .. index::
      single: SIGINT
      single: KeyboardInterrupt (built-in exception)

   この関数は廃止されています。 :const:`SIGINT` シグナルが到達した影響をシミュレートします --- 次に
   :c:func:`PyErr_CheckSignals` が呼ばれるとき、
   :exc:`KeyboardInterrupt` は送出されるでしょう。インタプリタロックを保持することなく呼び出すことができます。


.. c:function:: int PySignal_SetWakeupFd(int fd)

   このユーティリティ関数は、シグナルを受信したときに ``'\0'`` バイトを書き込む
   ファイルディスクリプタを指定します。戻り値は、それまで設定されていたファイル
   ディスクリプタです。
   ``-1`` はこの機能を無効にします。これは初期状態です。
   これは Python の :func:`signal.set_wakeup_fd` と同じものですが、
   エラーチェックを行ないません。
   *fd* は有効なファイルディスクリプタであるべきです。
   この関数の呼び出しはメインスレッドのみから行われるべきです。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyErr_NewException(char *name, PyObject *base, PyObject *dict)

   このユーティリティ関数は新しい例外オブジェクトを作成して返します。 *name* 引数は新しい例外の名前、 ``module.class`` 形式の
   C文字列でなければならない。 *base* と *dict* 引数は通常 *NULL* です。
   これはすべての例外のためのルート、組み込み名 :exc:`Exception`
   (Cでは :c:data:`PyExc_Exception` としてアクセス可能)をルートとして派生したクラスオブジェクトを作成します。

   新しいクラスの :attr:`__module__` 属性は *name* 引数の前半部分(最後のドットまで)に
   設定され、クラス名は後半部分(最後のドットの後)に設定されます。 *base* 引数は代わりのベースクラスを指定するために使えます; 一つのクラスでも、
   クラスのタプルでも構いません。 *dict* 引数はクラス変数とメソッドの辞書を指定するために使えます。


.. c:function:: PyObject* PyErr_NewExceptionWithDoc(char *name, char *doc, PyObject *base, PyObject *dict)

   :c:func:`PyErr_NewException` とほぼ同じですが、新しい例外クラスに簡単に docstring
   を設定できます。
   *doc* が *NULL* で無い場合、それが例外クラスの docstring になります。

   .. versionadded:: 2.7


.. c:function:: void PyErr_WriteUnraisable(PyObject *obj)

   例外が設定されているがインタプリタが実際に例外を発生させることができないときに、
   このユーティリティ関数は警告メッセージを ``sys.stderr`` へプリントします。
   例えば、例外が :meth:`__del__` メソッドで発生したときに使われます。

   発生させられない例外が生じたコンテキストを特定するための一つの引数 *obj* とともに
   関数が呼び出されます。 *obj* のreprが警告メッセージにプリントされるでしょう。


.. Unicode Exception Objects

.. _unicodeexceptions:

Unicode 例外オブジェクト
=========================

以下の関数は C言語から Unicode 例外を作ったり修正したりするために利用します。

.. c:function:: PyObject* PyUnicodeDecodeError_Create(const char *encoding, const char *object, Py_ssize_t length, Py_ssize_t start, Py_ssize_t end, const char *reason)

   *encoding*, *object*, *length*, *start*, *end*, *reason* 属性をもった
   :class:`UnicodeDecodeError` オブジェクトを作成します。

.. c:function:: PyObject* PyUnicodeEncodeError_Create(const char *encoding, const Py_UNICODE *object, Py_ssize_t length, Py_ssize_t start, Py_ssize_t end, const char *reason)

   *encoding*, *object*, *length*, *start*, *end*, *reason* 属性を持った
   :class:`UnicodeEncodeError` オブジェクトを作成します。

.. c:function:: PyObject* PyUnicodeTranslateError_Create(const Py_UNICODE *object, Py_ssize_t length, Py_ssize_t start, Py_ssize_t end, const char *reason)

   *object*, *length*, *start*, *end*, *reason* 属性を持った
   :class:`UnicodeTranslateError` オブジェクトを作成します。

.. c:function:: PyObject* PyUnicodeDecodeError_GetEncoding(PyObject *exc)
               PyObject* PyUnicodeEncodeError_GetEncoding(PyObject *exc)

   与えられた例外オブジェクトの *encoding* 属性を返します。

.. c:function:: PyObject* PyUnicodeDecodeError_GetObject(PyObject *exc)
               PyObject* PyUnicodeEncodeError_GetObject(PyObject *exc)
               PyObject* PyUnicodeTranslateError_GetObject(PyObject *exc)

   与えられた例外オブジェクトの *object* 属性を返します。

.. c:function:: int PyUnicodeDecodeError_GetStart(PyObject *exc, Py_ssize_t *start)
               int PyUnicodeEncodeError_GetStart(PyObject *exc, Py_ssize_t *start)
               int PyUnicodeTranslateError_GetStart(PyObject *exc, Py_ssize_t *start)

   渡された例外オブジェクトから *start* 属性を取得して *\*start* に格納します。
   *start* は *NULL* であってはなりません。
   成功したら ``0`` を、失敗したら ``-1`` を返します。

.. c:function:: int PyUnicodeDecodeError_SetStart(PyObject *exc, Py_ssize_t start)
               int PyUnicodeEncodeError_SetStart(PyObject *exc, Py_ssize_t start)
               int PyUnicodeTranslateError_SetStart(PyObject *exc, Py_ssize_t start)

   渡された例外オブジェクトの *start* 属性を *start* に設定します。
   成功したら ``0`` を、失敗したら ``-1`` を返します。

.. c:function:: int PyUnicodeDecodeError_GetEnd(PyObject *exc, Py_ssize_t *end)
               int PyUnicodeEncodeError_GetEnd(PyObject *exc, Py_ssize_t *end)
               int PyUnicodeTranslateError_GetEnd(PyObject *exc, Py_ssize_t *end)

   渡された例外オブジェクトから *end* 属性を取得して *\*end* に格納します。
   *end* は *NULL* であってはなりません。
   成功したら ``0`` を、失敗したら ``-1`` を返します。

.. c:function:: int PyUnicodeDecodeError_SetEnd(PyObject *exc, Py_ssize_t end)
               int PyUnicodeEncodeError_SetEnd(PyObject *exc, Py_ssize_t end)
               int PyUnicodeTranslateError_SetEnd(PyObject *exc, Py_ssize_t end)

   渡された例外オブジェクトの *end* 属性を *end* に設定します。
   成功したら ``0`` を、失敗したら ``-1`` を返します。

.. c:function:: PyObject* PyUnicodeDecodeError_GetReason(PyObject *exc)
               PyObject* PyUnicodeEncodeError_GetReason(PyObject *exc)
               PyObject* PyUnicodeTranslateError_GetReason(PyObject *exc)

   渡された例外オブジェクトの *reason* 属性を返します。

.. c:function:: int PyUnicodeDecodeError_SetReason(PyObject *exc, const char *reason)
               int PyUnicodeEncodeError_SetReason(PyObject *exc, const char *reason)
               int PyUnicodeTranslateError_SetReason(PyObject *exc, const char *reason)

   渡された例外オブジェクトの *reason* 属性を *reason* に設定します。
   成功したら ``0`` を、失敗したら ``-1`` を返します。



再帰の管理
==========

これら2つの関数は C レベルの再帰呼び出しを安全に実行する方法を、コアモジュールにも拡張モジュールにも提供します。
再帰を使ったコードが必ずしも Python コードを実行するわけではない場合 (Python コードは再帰の深さを自動的に追跡します)、これらの関数が必要となります。

.. c:function:: int Py_EnterRecursiveCall(char *where)

   C レベルの再帰呼び出しをしようとしているところに印を付けます。

   :const:`USE_STACKCHECK` が定義されている場合、 OS のスタックがオーバーフローがしたかどうかを :c:func:`PyOS_CheckStack` を使ってチェックします。
   もしオーバーフローしているなら、 :exc:`MemoryError` をセットしゼロでない値を返します。

   次にこの関数は再帰の上限に達していないかをチェックします。
   上限に達している場合、 :exc:`RuntimeError` をセットしゼロでない値を返します。
   そうでない場合はゼロを返します。

   再帰の深さの上限に達して送出される :exc:`RuntimeError` のメッセージに連結できるよう
   *where* は ``" in instance check"`` のような文字列にしてください。

.. c:function:: void Py_LeaveRecursiveCall()

   :c:func:`Py_EnterRecursiveCall` を終了させます。
   :c:func:`Py_EnterRecursiveCall` の *成功した* 呼び出しに対して必ず 1 回呼び出さなければなりません。

.. memo

   エラーメッセージは訳していない.


.. _standardexceptions:

標準例外
========

``PyExc_`` の後ろにPythonの例外名が続く名前をもつグローバル変数として、
すべての標準Python例外が利用可能です。これらは型 :c:type:`PyObject\*` を
持ち、すべてクラスオブジェクトです。完璧を期するために、すべての変数を以下に列挙します:

+---------------------------------------+----------------------------+----------+
| C名                                   | Python名                   | 注記     |
+=======================================+============================+==========+
| :c:data:`PyExc_BaseException`         | :exc:`BaseException`       | (1), (4) |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_Exception`             | :exc:`Exception`           | \(1)     |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_StandardError`         | :exc:`StandardError`       | \(1)     |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_ArithmeticError`       | :exc:`ArithmeticError`     | \(1)     |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_LookupError`           | :exc:`LookupError`         | \(1)     |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_AssertionError`        | :exc:`AssertionError`      |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_AttributeError`        | :exc:`AttributeError`      |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_EOFError`              | :exc:`EOFError`            |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_EnvironmentError`      | :exc:`EnvironmentError`    | \(1)     |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_FloatingPointError`    | :exc:`FloatingPointError`  |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_IOError`               | :exc:`IOError`             |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_ImportError`           | :exc:`ImportError`         |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_IndexError`            | :exc:`IndexError`          |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_KeyError`              | :exc:`KeyError`            |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_KeyboardInterrupt`     | :exc:`KeyboardInterrupt`   |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_MemoryError`           | :exc:`MemoryError`         |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_NameError`             | :exc:`NameError`           |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_NotImplementedError`   | :exc:`NotImplementedError` |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_OSError`               | :exc:`OSError`             |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_OverflowError`         | :exc:`OverflowError`       |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_ReferenceError`        | :exc:`ReferenceError`      | \(2)     |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_RuntimeError`          | :exc:`RuntimeError`        |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_SyntaxError`           | :exc:`SyntaxError`         |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_SystemError`           | :exc:`SystemError`         |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_SystemExit`            | :exc:`SystemExit`          |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_TypeError`             | :exc:`TypeError`           |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_ValueError`            | :exc:`ValueError`          |          |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_WindowsError`          | :exc:`WindowsError`        | \(3)     |
+---------------------------------------+----------------------------+----------+
| :c:data:`PyExc_ZeroDivisionError`     | :exc:`ZeroDivisionError`   |          |
+---------------------------------------+----------------------------+----------+

.. index::
   single: PyExc_BaseException
   single: PyExc_Exception
   single: PyExc_StandardError
   single: PyExc_ArithmeticError
   single: PyExc_LookupError
   single: PyExc_AssertionError
   single: PyExc_AttributeError
   single: PyExc_EOFError
   single: PyExc_EnvironmentError
   single: PyExc_FloatingPointError
   single: PyExc_IOError
   single: PyExc_ImportError
   single: PyExc_IndexError
   single: PyExc_KeyError
   single: PyExc_KeyboardInterrupt
   single: PyExc_MemoryError
   single: PyExc_NameError
   single: PyExc_NotImplementedError
   single: PyExc_OSError
   single: PyExc_OverflowError
   single: PyExc_ReferenceError
   single: PyExc_RuntimeError
   single: PyExc_SyntaxError
   single: PyExc_SystemError
   single: PyExc_SystemExit
   single: PyExc_TypeError
   single: PyExc_ValueError
   single: PyExc_WindowsError
   single: PyExc_ZeroDivisionError

注記:

(1)
   これは別の標準例外のためのベースクラスです。

(2)
   これは :exc:`weakref.ReferenceError` と同じです。

(3)
   Windowsでのみ定義されています。プリプロセッサマクロ ``MS_WINDOWS`` が定義されているかテストすることで、
   これを使うコードを保護してください。

(4)
   .. versionadded:: 2.5


.. String Exceptions

文字列の例外
================

.. versionchanged:: 2.6
   All exceptions to be raised or caught must be derived from :exc:`BaseException`.
   Trying to raise a string exception now raises :exc:`TypeError`.
   発生したりキャッチされる全ての例外は :exc:`BaseException` を継承しなければなりません。
   文字列例外を発生させようとすると :exc:`TypeError` が発生されます。
