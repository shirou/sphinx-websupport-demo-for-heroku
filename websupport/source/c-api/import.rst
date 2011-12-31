.. highlightlang:: c

.. _importing:

モジュールの import
===================


.. c:function:: PyObject* PyImport_ImportModule(const char *name)

   .. index::
      single: __all__ (package variable)
      single: package variable; __all__
      single: modules (in module sys)

   この関数は下で述べる :c:func:`PyImport_ImportModuleEx` を単純化したインタフェースで、 *globals* および
   *locals*  引数を *NULL* のままにし、 *level* を 0 にしたものです。
   *name* 引数にドットが含まれる場合 (あるパッケージのサブモジュールを指定している場合)、
   *fromlist* 引数がリスト ``['*']`` に追加され、戻り値がモジュールを含む
   トップレベルパッケージではなく名前つきモジュール (named module) になるようにします。 (残念ながらこのやり方には、 *name*
   が実際にはサブモジュールでなくサブパッケージを指定している場合、パッケージの  ``__all__``   変数に指定されている
   サブモジュールがロードされてしまうという副作用があります。) import されたモジュールへの新たな参照を返します。失敗した
   場合には例外をセットし、 *NULL* を返します。 Python 2.4 より前のバージョンでは、失敗した場合でもモジュールは生成されていることがあります ---
   ``sys.modules``  を使って調べてください。 Python 2.4 以降では、 import に失敗したモジュールは
   ``sys.modules`` に残りません。

   .. versionchanged:: 2.4
      import に失敗した場合、不完全なモジュールを除去するようになりました。

   .. versionchanged:: 2.6
      常に、絶対 import を使うようになりました。


.. c:function:: PyObject* PyImport_ImportModuleNoBlock(const char *name)

   このバージョンの :c:func:`PyImport_ImportModule` はブロックしません。
   関数を実行するために他のモジュールをインポートするC関数から使われることを意図しています。
   インポート処理は他のスレッドがインポートロックを持っている場合はブロックします。
   この関数はブロックしません。まず sys.modules からモジュールのフェッチを試み、
   失敗したら、ロックが取られていなければ :c:func:`PyImport_ImportModule` を実行します。
   ロックが取られていた場合は :exc:`ImportError` を発生させます。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyImport_ImportModuleEx(char *name, PyObject *globals, PyObject *locals, PyObject *fromlist)

   .. index:: builtin: __import__

   モジュールを import します。モジュールの import については組み込みの Python 関数 :func:`__import__`
   を読むとよく分かります。というのも、標準の :func:`__import__`  はこの関数を直接呼び出しているからです。

   戻り値は import されたモジュールかトップレベルパッケージへの新たな参照になります。失敗した場合には例外をセットし、 *NULL* を返します
   (Python 2.4 よりも前のバージョンでは、モジュールは生成されている場合があります) :func:`__import__`
   と同じく、パッケージに対してサブモジュールを要求した場合の戻り値は通常、空でない *fromlist* を指定しない限りトップレベルパッケージになります。

   .. versionchanged:: 2.4
      import に失敗した場合、不完全なモジュールを除去するようになりました。

   .. versionchanged:: 2.6
      この関数は :c:func:`PyImport_ImportModuleLevel` のエイリアスです。
      level には相対インポートを意味する -1 が渡されます。


.. c:function:: PyObject* PyImport_ImportModuleLevel(char *name, PyObject *globals, PyObject *locals, PyObject *fromlist, int level)

   モジュールをインポートします。このモジュールの動作については、Python ビルトイン関数の
   :func:`__import__` でよく説明されています。 :func:`__import__` は直接この関数を実行します。

   戻り値は、インポートされたモジュールかトップレベルパッケージへの新しい参照か、
   失敗した場合は例外を設定して *NULL* を返します。
   :func:`__import__` と同じように、パッケージのサブモジュールが要求されたときは、
   空でない *fromlist* を渡された時以外は、トップレベルのパッケージを返します。

   .. versionadded:: 2.5


.. c:function:: PyObject* PyImport_Import(PyObject *name)

   .. index::
      module: rexec
      module: ihooks

   現在の "import フック関数" を呼び出すための高水準のインタフェースです。この関数は現在のグローバル変数辞書内の ``__builtins__``
   から :func:`__import__` 関数を呼び出します。すなわち、現在の環境にインストールされている import フック、例えば
   :mod:`rexec` や :mod:`ihooks` を使って import を行います。

   .. versionchanged:: 2.6
      常に、絶対importを使うようになりました。


.. c:function:: PyObject* PyImport_ReloadModule(PyObject *m)

   .. index:: builtin: reload

   モジュールを再ロード (reload) します。モジュールの再ロードについては組み込みの Python 関数 :func:`reload`
   を読むとよく分かります。というのも、標準の :func:`reload`  はこの関数を直接呼び出しているからです。
   戻り値は再ロードしたモジュールかトップレベルパッケージへの新たな参照になります。失敗した場合には例外をセットし、 *NULL* を返します
   (その場合でも、モジュールは生成されている場合があります)


.. c:function:: PyObject* PyImport_AddModule(const char *name)

   モジュール名に対応するモジュールオブジェクトを返します。 *name* 引数は ``package.module`` の形式でもかまいません。
   まずモジュール辞書に該当するモジュールがあるかどうか調べ、なければ新たなモジュールを生成してモジュール辞書に挿入します。失敗した場合には例外をセットして
   *NULL* を返します。

   .. note::

      この関数はモジュールの import やロードを行いません; モジュールがまだロードされていなければ、空のモジュールオブジェクトを得ることになります。
      :c:func:`PyImport_ImportModule` やその別形式を使ってモジュールを import してください。ドット名表記で
      指定した *name* が存在しない場合、パッケージ構造は作成されません。


.. c:function:: PyObject* PyImport_ExecCodeModule(char *name, PyObject *co)

   .. index:: builtin: compile

   モジュール名 (``package.module`` 形式でもかまいません) および Python のバイトコードファイルや組み込み関数
   :func:`compile`  で得られたコードオブジェクトを元にモジュールをロードします。モジュールオブジェクトへの新たな参照を返します。失敗した
   場合には例外をセットし、 *NULL* を返します。Python 2.4 以前では、失敗した場合でもモジュールは生成されていることがありました。 Python
   2.4 以降では、たとえ :c:func:`PyImport_ExecCodeModule` の処理に入った時に *name* が :attr:`sys.modules`
   に入っていたとしても、 import に失敗したモジュールは :attr:`sys.modules` に残りません。初期化の不完全なモジュールを
   :attr:`sys.modules` に残すのは危険であり、そのようなモジュールを import するコードにとっては、モジュールの状態がわからない
   (モジュール作者の意図から外れた壊れた状態かもしれない) からです。

   モジュールの :attr:`__file__` 属性が、コードオブジェクトの :c:member:`co_filename` に設定されます。

   この関数は、すでに import されているモジュールの場合には再ロードを行います。意図的にモジュールの再ロードを行う方法は
   :c:func:`PyImport_ReloadModule` を参照してください。

   *name* が ``package.module`` 形式のドット名表記であった場合、まだ作成されていないパッケージ構造はその作成されないままになります。

   .. versionchanged:: 2.4
      エラーが発生した場合に *name* を :attr:`sys.modules` から除去するようになりました。


.. c:function:: PyObject* PyImport_ExecCodeModuleEx(char *name, PyObject *co, char *pathname)

   :c:func:`PyImport_ExecCodeModule` に似ていますが、 *pathname* が ``NULL`` で無い場合、
   モジュールオブジェクトの :attr:`__file__` 属性に設定します。


.. c:function:: long PyImport_GetMagicNumber()

   Python バイトコードファイル (いわゆる :file:`.pyc` および :file:`.pyo` ファイル)
   のマジックナンバを返します。マジックナンバはバイトコードファイルの先頭 4 バイトにリトルエンディアン整列で配置されています。


.. c:function:: PyObject* PyImport_GetModuleDict()

   モジュール管理のための辞書 (いわゆる ``sys.modules`` )を返します。この辞書はインタプリタごとに一つだけある変数なので注意してください。


.. c:function:: PyObject* PyImport_GetImporter(PyObject *path)

   :data:`sys.path`/:attr:`pkg.__path__` の要素 *path* の、 importer オブジェクトを返します。
   可能なら、 :data:`sys.path_importer_cache` からフェッチします。
   まだキャッシュされていない場合、そのパスを扱える hook が見つかるまで :data:`sys.path_hooks`
   を巡回します。
   hook が見つからない場合、 ``None`` を返します。この場合、呼び出し元は
   ビルトインの import 機構にフォールバックします。
   結果は :data:`sys.path_importer_cache` にキャッシュされます。
   importer オブジェクトへの新しい参照を返します。

   .. versionadded:: 2.6


.. c:function:: void _PyImport_Init()

   import 機構を初期化します。内部使用だけのための関数です。


.. c:function:: void PyImport_Cleanup()

   モジュールテーブルを空にします。内部使用だけのための関数です。


.. c:function:: void _PyImport_Fini()

   import 機構を終了処理します。内部使用だけのための関数です。


.. c:function:: PyObject* _PyImport_FindExtension(char *, char *)

   内部使用だけのための関数です。


.. c:function:: PyObject* _PyImport_FixupExtension(char *, char *)

   内部使用だけのための関数です。


.. c:function:: int PyImport_ImportFrozenModule(char *name)

   *name* という名前のフリーズ (freeze) されたモジュールをロードします。成功すると ``1`` を、モジュールが見つからなかった場合には
   ``0`` を、初期化が失敗した場合には例外をセットして ``-1`` を返します。ロードに成功したモジュールにアクセスするには
   :c:func:`PyImport_ImportModule` を使ってください。 (Note この関数名はいささか誤称めいています --- この関数はすでに
   import 済みのモジュールをリロードしてしまいます。)


.. c:type:: struct _frozen

   .. index:: single: freeze utility

   :program:`freeze` ユーティリティが生成するようなフリーズ化モジュールデスクリプタの構造体型定義です。 (Python ソース配布物の
   :file:`Tools/freeze/` を参照してください) この構造体の定義は :file:`Include/import.h` にあり、以下のように
   なっています::

      struct _frozen {
          char *name;
          unsigned char *code;
          int size;
      };


.. c:var:: struct _frozen* PyImport_FrozenModules

   このポインタは :c:type:`struct _frozen` のレコードからなり、終端の要素のメンバが *NULL* かゼロになっているような配列
   を指すよう初期化されます。フリーズされたモジュールを import するとき、このテーブルを検索します。サードパーティ製のコードから
   このポインタに仕掛けを講じて、動的に生成されたフリーズ化モジュールの集合を提供するようにできます。


.. c:function:: int PyImport_AppendInittab(const char *name, void (*initfunc)(void))

   既存の組み込みモジュールテーブルに単一のモジュールを追加します。この関数は利便性を目的とした :c:func:`PyImport_ExtendInittab`
   のラッパ関数で、テーブルが拡張できないときには ``-1`` を返します。新たなモジュールは *name* で import でき、最初に import を
   試みた際に呼び出される関数として *initfunc* を使います。 :c:func:`Py_Initialize` よりも前に呼び出さねばなりません。


.. c:type:: struct _inittab

   組み込みモジュールリスト内の一つのエントリを記述している構造体です。リスト内の各構造体には、インタプリタ内に組み込まれているモジュールの
   名前と初期化関数が指定されています。 Python を埋め込むようなプログラムは、この構造体の配列と
   :c:func:`PyImport_ExtendInittab` を組み合わせて、追加の
   組み込みモジュールを提供できます。構造体は :file:`Include/import.h` で以下のように定義されています::

      struct _inittab {
          char *name;
          void (*initfunc)(void);
      };


.. c:function:: int PyImport_ExtendInittab(struct _inittab *newtab)

   組み込みモジュールのテーブルに一群のモジュールを追加します。配列 *newtab* は :attr:`name` フィールドが *NULL* になっている
   センチネル (sentinel) エントリで終端されていなければなりません; センチネル値を与えられなかった場合にはメモリ違反になるかもしれません。成功すると
   ``0`` を、内部テーブルを拡張するのに十分なメモリを確保できなかった場合には ``-1`` を返します。操作が失敗した場合、
   モジュールは一切内部テーブルに追加されません。 :c:func:`Py_Initialize` よりも前に呼び出さねばなりません。

