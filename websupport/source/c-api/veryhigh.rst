.. highlightlang:: c


.. _veryhigh:

****************
超高レベルレイヤ
****************

この章の関数を使うとファイルまたはバッファにあるPythonソースコードを実行できますが、より詳細なやり取りをインタプリタとすることはできないでしょう。

これらの関数のいくつかは引数として文法の開始記号を受け取ります。
使用できる開始記号は :const:`Py_eval_input` と :const:`Py_file_input` 、
:const:`Py_single_input` です。開始期号の説明はこれらを引数として取る関数の後にあります。

これらの関数のいくつかが :c:type:`FILE\*` 引数をとることにも注意してください。
注意深く扱う必要がある特別な問題の1つは、異なるCライブラリの :c:type:`FILE` 構造体は異なっていて互換性がない可能性があるということです。
実際に(少なくとも)Windowsでは、動的リンクされる拡張が異なるライブラリを
使うことが可能であり、したがって、 :c:type:`FILE\*` 引数がPythonランタイムが
使っているライブラリと同じライブラリによって作成されたことが確かならば、単にこれらの関数へ渡すだけということに注意すべきです。


.. c:function:: int Py_Main(int argc, char **argv)

   標準インタプリタのためのメインプログラム。Pythonを組み込むプログラムのためにこれを利用できるようにしています。
   *argc* と *argv* 引数をCプログラムの :c:func:`main` 関数へ渡されるものとまったく同じに作成すべきです。
   引数リストが変更される可能性があるという点に注意することは重要です。
   (しかし、引数リストが指している文字列の内容は変更されません)。
   戻り値はインタプリタが(例外などではなく)普通に終了した時は ``0`` に、
   例外で終了したときには ``1`` に、引数リストが正しい Python コマンドラインが
   渡されなかったときは ``2`` になります。

   ``Py_InspectFlag`` が設定されていない場合、未処理の :exc:`SystemExit` 例外が発生すると、
   この関数は ``1`` を返すのではなくプロセスを exit することに気をつけてください。

.. c:function:: int PyRun_AnyFile(FILE *fp, const char *filename)

   下記の :c:func:`PyRun_AnyFileExFlags` の *closeit* を ``0`` に、 *flags* を
   *NULL* にして単純化したインタフェースです。


.. c:function:: int PyRun_AnyFileFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   下記の :c:func:`PyRun_AnyFileExFlags` の *closeit* を ``0`` にして単純化したインタフェースです。


.. c:function:: int PyRun_AnyFileEx(FILE *fp, const char *filename, int closeit)

   下記の :c:func:`PyRun_AnyFileExFlags` の *flags* を *NULL* にして単純化したインタフェースです。


.. c:function:: int PyRun_AnyFileExFlags(FILE *fp, const char *filename, int closeit, PyCompilerFlags *flags)

   *fp* が対話的デバイス(コンソールや端末入力あるいはUnix仮想端末)と関連づけられたファイルを参照しているならば、
   :c:func:`PyRun_InteractiveLoop` の値を返します。それ以外の場合は、
   :c:func:`PyRun_SimpleFile` の結果を返します。 *filename* が
   *NULL* ならば、この関数はファイル名として ``"???"`` を使います。


.. c:function:: int PyRun_SimpleString(const char *command)

   下記の :c:func:`PyRun_SimpleStringFlags` の *PyCompilerFlags\** を
   *NULL* にして単純化したインタフェースです。


.. c:function:: int PyRun_SimpleStringFlags(const char *command, PyCompilerFlags *flags)

   :mod:`__main__` モジュールの中で *flags* に従って *command* に含まれる Python ソースコードを
   実行します。 :mod:`__main__` がまだ存在しない場合は作成されます。正常終了の場合は ``0`` を返し、また例外が発生した場合は ``-1`` を
   返します。エラーがあっても、例外情報を得る方法はありません。
   *flags* の意味については、後述します。

   ``Py_InspectFlag`` が設定されていない場合、未処理の :exc:`SystemExit` 例外が発生すると、
   この関数は ``1`` を返すのではなくプロセスを exit することに気をつけてください。


.. c:function:: int PyRun_SimpleFile(FILE *fp, const char *filename)

   下記の :c:func:`PyRun_SimpleStringFileExFlags` の *closeit* を ``0`` に、 *flags* を
   *NULL* にして単純化したインタフェースです。


.. c:function:: int PyRun_SimpleFileFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   下記の :c:func:`PyRun_SimpleStringFileExFlags` の *closeit* を ``0``
   にして単純化したインタフェースです。


.. c:function:: int PyRun_SimpleFileEx(FILE *fp, const char *filename, int closeit)

   下記の :c:func:`PyRun_SimpleStringFileExFlags` の *flags* を *NULL* にして単純化したインタフェースです。


.. c:function:: int PyRun_SimpleFileExFlags(FILE *fp, const char *filename, int closeit, PyCompilerFlags *flags)

   Similar to :c:func:`PyRun_SimpleStringFlags`, but the Python source
   :c:func:`PyRun_SimpleString` と似ていますが、Pythonソースコードをメモリ内の文字列ではなく *fp* から読み込みます。
   *filename* はそのファイルの名前でなければなりません。 *closeit* が真ならば、PyRun_SimpleFileExFlags は処理を戻す前に
   ファイルを閉じます。


.. c:function:: int PyRun_InteractiveOne(FILE *fp, const char *filename)

   下記の :c:func:`PyRun_InteractiveOneFlags` の *flags* を *NULL* にして単純化したインタフェースです。


.. c:function:: int PyRun_InteractiveOneFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   対話的デバイスに関連付けられたファイルから文を一つ読み込み、 *flags* に従って実行します。
   ``sys.ps1`` と ``sys.ps2`` を使って、ユーザにプロンプトを表示します。
   入力が正常に実行されたときは ``0`` を返します。例外が発生した場合は
   ``-1`` を返します。パースエラーの場合はPythonの一部として配布されている
   :file:`errcode.h` インクルードファイルにあるエラーコードを返します。
   (:file:`Python.h` は :file:`errcode.h` をインクルードしません。したがって、
   必要ならば特別にインクルードしなければならないことに注意してください。)


.. c:function:: int PyRun_InteractiveLoop(FILE *fp, const char *filename)

   下記の :c:func:`PyRun_InteractiveLoopFlags` の *flags* を ``0`` にして単純化したインタフェースです。


.. c:function:: int PyRun_InteractiveLoopFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   対話的デバイスに関連付けられたファイルからEOF に達するまで複数の文を
   読み込み実行します。
   使われます。 ``sys.ps1`` と ``sys.ps2`` を使って、ユーザにプロンプトを表示します。
   EOFに達すると ``0`` を返します。


.. c:function:: struct _node* PyParser_SimpleParseString(const char *str, int start)

   下記の :c:func:`PyRun_SimpleParseStringFlagsFilename` の *filename* を *NULL*
   に、 *flags* を ``0`` にして単純化したインタフェースです。


.. c:function:: struct _node* PyParser_SimpleParseStringFlags( const char *str, int start, int flags)

   下記の :c:func:`PyRun_SimpleParseStringFlagsFilename` の *filename* を *NULL*
   にして単純化したインタフェースです。


.. c:function:: struct _node* PyParser_SimpleParseStringFlagsFilename( const char *str, const char *filename, int start, int flags)

   開始トークン *start* を使って *str* に含まれる Python ソースコードを *flags* 引数に従ってパースします。効率的に評価可能なコードオブジェ
   クトを作成するためにその結果を使うことができます。コード断片を何度も評価しなければならない場合に役に立ちます。


.. c:function:: struct _node* PyParser_SimpleParseFile(FILE *fp, const char *filename, int start)

   下記の :c:func:`PyRun_SimpleParseFileFlags` の *flags* を ``0`` にして単純化したインタフェースです。


.. c:function:: struct _node* PyParser_SimpleParseFileFlags(FILE *fp, const char *filename, int start, int flags)

   :c:func:`PyParser_SimpleParseStringFlagsFilename` に似ていますが、
   Pythonソースコードをメモリ内の文字列ではなく *fp* から読み込みます。 *filename* はそのファイルの名前でなけれななりません。


.. c:function:: PyObject* PyRun_String(const char *str, int start, PyObject *globals, PyObject *locals)

   下記の :c:func:`PyRun_StringFlags` の *flags* を *NULL* にして単純化したインタフェースです。


.. c:function:: PyObject* PyRun_StringFlags(const char *str, int start, PyObject *globals, PyObject *locals, PyCompilerFlags *flags)

   辞書 *globals* と *locals* で指定されるコンテキストにおいて、 *str* に含まれるPythonソースコードをコンパイラフラグ *flags* の
   もとで実行します。パラメータ *start* はソースコードをパースするために使われるべき開始トークンを指定します。

   コードを実行した結果をPythonオブジェクトとして返します。または、例外が発生したならば *NULL* を返します。


.. c:function:: PyObject* PyRun_File(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals)

   下記の :c:func:`PyRun_FileExFlags` の *closeit* を ``0`` にし、 *flags*
   を *NULL* にして単純化したインタフェースです。


.. c:function:: PyObject* PyRun_FileEx(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, int closeit)

   下記の :c:func:`PyRun_FileExFlags` の *flags* を *NULL* にして単純化したインタフェースです。


.. c:function:: PyObject* PyRun_FileFlags(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, PyCompilerFlags *flags)

   下記の :c:func:`PyRun_FileExFlags` の *closeit* を ``0`` にして単純化したインタフェースです。


.. c:function:: PyObject* PyRun_FileExFlags(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, int closeit, PyCompilerFlags *flags)

   :c:func:`PyRun_String` と似ていますが、Pythonソースコードをメモリ内の文字列ではなく *fp* から読み込みます。 *closeit*
   を真にすると、 :c:func:`PyRun_FileExFlags` から処理を戻す前にファイルを閉じます。
   *filename* はそのファイルの名前でなければなりません。


.. c:function:: PyObject* Py_CompileString(const char *str, const char *filename, int start)

   下記の :c:func:`Py_CompileStringFlags` の *flags* を *NULL* にして単純化したインタフェースです。


.. c:function:: PyObject* Py_CompileStringFlags(const char *str, const char *filename, int start, PyCompilerFlags *flags)

   *str* 内のPythonソースコードをパースしてコンパイルし、作られたコードオブジェクトを返します。開始トークンは
   *start* によって与えられます。これはコンパイル可能なコードを制限するために使うことができ、 :const:`Py_eval_input` 、
   :const:`Py_file_input` もしくは :const:`Py_single_input` であるべきです。
   *filename* で指定されるファイル名はコードオブジェクトを構築するために使われ、
   トレースバックあるいは :exc:`SyntaxError` 例外メッセージに出てくる可能性があります。
   コードがパースできなかったりコンパイルできなかったりした場合に、これは *NULL* を返します。


.. c:function:: PyObject* PyEval_EvalCode(PyCodeObject *co, PyObject *globals, PyObject *locals)

   :c:func:`PyEval_EvalCodeEx` に対するシンプルなインタフェースで、
   コードオブジェクトと、グローバル・ローカル変数辞書だけを受け取ります。
   他の引数には *NULL* が渡されます。


.. c:function:: PyObject* PyEval_EvalCodeEx(PyCodeObject *co, PyObject *globals, PyObject *locals, PyObject **args, int argcount, PyObject **kws, int kwcount, PyObject **defs, int defcount, PyObject *closure)

   与えられた特定の環境で、コンパイル済みのコードオブジェクトを評価します。
   環境はグローバルとローカルの辞書、引き数の配列、キーワードとデフォルト値、
   クロージャーのためのセルのタプルで構成されています。


.. c:function:: PyObject* PyEval_EvalFrame(PyFrameObject *f)

   実行フレームを評価します。
   これは PyEval_EvalFrameEx に対するシンプルなインタフェースで、
   後方互換性のためのものです。


.. c:function:: PyObject* PyEval_EvalFrameEx(PyFrameObject *f, int throwflag)

   Python のインタープリタの主要な、直接的な関数です。
   この関数には 2000 行ほどあります。
   実行フレーム *f* に関連付けられたコードオブジェクトを実行します。
   バイトコードを解釈して、必要に応じて呼び出しを実行します。
   追加の *throwflag* 引数はほとんど無視できます。 - もし true なら、
   すぐに例外を発生させます。これはジェネレータオブジェクトの :meth:`throw`
   メソッドで利用されます。


.. c:function:: int PyEval_MergeCompilerFlags(PyCompilerFlags *cf)

   現在の評価フレームのフラグを変更します。
   成功したら true を、失敗したら false を返します。


.. c:var:: int Py_eval_input

   .. index:: single: Py_CompileString()

   単独の式に対するPython文法の開始記号で、 :c:func:`Py_CompileString` と一緒に使います。


.. c:var:: int Py_file_input

   .. index:: single: Py_CompileString()

   ファイルあるいは他のソースから読み込まれた文の並びに対するPython文法の開始記号で、 :c:func:`Py_CompileString` と
   一緒に使います。これは任意の長さのPythonソースコードをコンパイルするときに使う記号です。


.. c:var:: int Py_single_input

   .. index:: single: Py_CompileString()

   単一の文に対するPython文法の開始記号で、 :c:func:`Py_CompileString` と一緒に使います。
   これは対話式のインタプリタループのための記号です。


.. c:type:: struct PyCompilerFlags

   コンパイラフラグを収めておくための構造体です。コードをコンパイルするだけの場合、この構造体が ``int flags`` として渡されます。コードを実
   行する場合には ``PyCompilerFlags *flags`` として渡されます。この場合、 ``from __future__  import`` は
   *flags* の内容を変更できます。

   ``PyCompilerFlags *flags`` が *NULL* の場合、 :attr:`cf_flags` は ``0`` として扱われ、
   ``from __future__ import`` による変更は無視されます。 ::

      struct PyCompilerFlags {
          int cf_flags;
      }


.. c:var:: int CO_FUTURE_DIVISION

   このビットを *flags* にセットすると、除算演算子 ``/`` は :pep:`238` による「真の除算 (true division)」
   として扱われます。

