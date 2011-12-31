.. highlightlang:: c

.. _os:

オペレーティングシステム関連のユーティリティ
============================================


.. c:function:: int Py_FdIsInteractive(FILE *fp, const char *filename)

   *filename* という名前の標準 I/O ファイル *fp* が対話的 (interactive) であると考えられる場合に真 (非ゼロ) を返します。
   これは ``isatty(fileno(fp))`` が真になるファイルの場合です。グローバルなフラグ :c:data:`Py_InteractiveFlag`
   が真の場合には、 *filename* ポインタが *NULL* か、名前が ``'<stdin>'`` または ``'???'``
   のいずれかに等しい場合にも真を返します。


.. c:function:: void PyOS_AfterFork()

   プロセスが fork した後の内部状態を更新するための関数です; fork 後 Python インタプリタを使い続ける場合、新たなプロセス内で
   この関数を呼び出さねばなりません。新たなプロセスに新たな実行可能物をロードする場合、この関数を呼び出す必要はありません。


.. c:function:: int PyOS_CheckStack()

   インタプリタがスタック空間を使い尽くしたときに真を返します。このチェック関数には信頼性がありますが、 :const:`USE_STACKCHECK`
   が定義されている場合 (現状では Microsoft Visual C++ コンパイラでビルドした Windows 版) にしか利用できません .
   :const:`USE_CHECKSTACK` は自動的に定義されます; 自前のコードでこの定義を変更してはなりません。


.. c:function:: PyOS_sighandler_t PyOS_getsig(int i)

   シグナル *i* に対する現在のシグナルハンドラを返します。この関数は :c:func:`sigaction` または :c:func:`signal`
   のいずれかに対する薄いラッパです。 :c:func:`sigaction` や :c:func:`signal` を直接呼び出してはなりません!
   :c:type:`PyOS_sighandler_t` は :c:type:`void (\*)(int)` の typedef  による別名です。


.. c:function:: PyOS_sighandler_t PyOS_setsig(int i, PyOS_sighandler_t h)

   シグナル *i* に対する現在のシグナルハンドラを *h* に設定します; 以前のシグナルハンドラを返します。この関数は
   :c:func:`sigaction` または :c:func:`signal` のいずれかに対する薄いラッパです。 :c:func:`sigaction` や
   :c:func:`signal` を直接呼び出してはなりません!  :c:type:`PyOS_sighandler_t` は :c:type:`void
   (\*)(int)` の typedef  による別名です。


.. _systemfunctions:

システム関数
================

:mod:`sys` モジュールが提供している機能にCのコードからアクセスする関数です。
すべての関数は現在のインタプリタスレッドの :mod:`sys` モジュールの辞書に対して動作します。
この辞書は内部のスレッド状態構造体に格納されています。

.. c:function:: PyObject *PySys_GetObject(char *name)

   :mod:`sys` モジュールの *name* オブジェクトを返すか、存在しなければ
   例外を設定せずに *NULL* を返します。

.. c:function:: FILE *PySys_GetFile(char *name, FILE *def)

   :mod:`sys` モジュールの *name* に関連付けられた :c:type:`FILE*` を返します。
   *name* がなかった場合や :c:type:`FILE*` に関連付けられていなかった場合は *def* を返します。

.. c:function:: int PySys_SetObject(char *name, PyObject *v)

   *v* が *NULL* で無い場合、 :mod:`sys` モジュールの *name* に *v* を設定します。
   *v* が *NULL* なら、 sys モジュールから *name* を削除します。
   成功したら ``0`` を、エラー時は ``-1`` を返します。

.. c:function:: void PySys_ResetWarnOptions()

   :data:`sys.warnoptions` を、空リストにリセットします。

.. c:function:: void PySys_AddWarnOption(char *s)

   :data:`sys.warnoptions` に *s* を追加します。

.. c:function:: void PySys_SetPath(char *path)

   :data:`sys.path` を *path* に含まれるパスの、リストオブジェクトに設定します。
   *path* はプラットフォームの検索パスデリミタ(Unixでは ``:``, Windows では ``;``)
   で区切られたパスのリストでなければなりません。

.. c:function:: void PySys_WriteStdout(const char *format, ...)

   *format* で指定された出力文字列を :data:`sys.stdout` に出力します。
   切り詰めが起こった場合を含め、例外は一切発生しません。(後述)

   *format* は、フォーマット後の出力文字列のトータルの大きさを1000バイト以下に
   抑えるべきです。 -- 1000 バイト以降の出力文字列は切り詰められます。
   特に、制限のない "%s" フォーマットを使うべきではありません。
   "%.<N>s" のようにして N に10進数の値を指定し、<N> + その他のフォーマット後の
   最大サイズが1000を超えないように設定するべきです。
   同じように "%f" にも気を付ける必要があります。非常に大きい数値に対して、
   数百の数字を出力する可能性があります。

   問題が発生したり、 :data:`sys.stdout` が設定されていなかった場合、
   フォーマット後のメッセージは本物の(Cレベルの) *stdout* に出力されます。

.. c:function:: void PySys_WriteStderr(const char *format, ...)

   上と同じですが、 :data:`sys.stderr` か *stderr* に出力します。

.. _processcontrol:

プロセス制御
============


.. c:function:: void Py_FatalError(const char *message)

   .. index:: single: abort()

   致命的エラーメッセージ (fatal error message) を出力してプロセスを強制終了 (kill)
   します。後始末処理は行われません。この関数は、Python  インタプリタを使い続けるのが危険であるような状況が検出されたとき;
   例えば、オブジェクト管理が崩壊していると思われるときにのみ、呼び出されるようにしなければなりません。Unixでは、標準 C ライブラリ関数
   :c:func:`abort` を呼び出して :file:`core` を生成しようと試みます。


.. c:function:: void Py_Exit(int status)

   .. index::
      single: Py_Finalize()
      single: exit()

   現在のプロセスを終了 (exit) します。この関数は :c:func:`Py_Finalize` を呼び出し、次いで標準 C ライブラリ関数
   ``exit(status)`` を呼び出します。


.. c:function:: int Py_AtExit(void (*func) ())

   .. index::
      single: Py_Finalize()
      single: cleanup functions

   :c:func:`Py_Finalize` から呼び出される後始末処理を行う関数 (cleanup function) を登録します。
   後始末関数は引数無しで呼び出され、値を返しません。最大で 32 の後始末処理関数を登録できます。登録に成功すると、 :c:func:`Py_AtExit` は
   ``0`` を返します;  失敗すると ``-1`` を返します。最後に登録した後始末処理関数から先に呼び出されます。各関数は高々一度しか呼び出されません。
   Python の内部的な終了処理は後始末処理関数より以前に完了しているので、 *func* からはいかなる Python API も呼び出してはなりません。
