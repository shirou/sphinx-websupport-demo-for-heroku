==================
拡張と埋め込み FAQ
==================

.. contents::

.. highlight:: c


C で独自の関数を作ることはできますか？
--------------------------------------

はい。関数、変数、例外、そして新しいタイプまで含んだビルトインモジュールを
C で作れます。これはドキュメント :ref:`extending-index` で説明されています。

ほとんどの中級から上級の Python 本もこの話題を扱っています。


C++ で独自の関数を作ることはできますか？
----------------------------------------

はい。C++ 内にある C 互換機能を使ってできます。\ ``extern "C" { ... }`` で
Python のインクルードファイルを囲み、\ ``extern "C"`` を
Python インタプリタから呼ぶ各関数の前に置いてください。
グローバルや静的な C++ オブジェクトの構造体を持つものは良くないでしょう。


.. _c-wrapper-software:

C を書くのは大変です。他の方法はありませんか？
----------------------------------------------

独自の C 拡張を書くための別のやり方は、目的によっていくつかあります。

.. XXX make sure these all work; mention Cython

速度が必要なら、\ `Psyco <http://psyco.sourceforge.net/>`_ は
Python バイトコードから x86 アセンブリコードを生成します。
Psyco でコードの最も時間制約が厳しい関数群をコンパイルすれば、
x-86 互換のプロセッサ上で動かす限り、わずかな手間で著しい改善ができます。

`Pyrex <http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/>`_ は、
わずかに変形した Python を受け取り、対応する C コードを生成します。
Cython や Pyrex を使えば Python の C API を習得することなく拡張を書けます。

今のところ Python 拡張が存在しないような C や C++ ライブラリへの
インタフェースが必要なら、\ `SWIG <http://www.swig.org>`_ のようなツールで、
そのライブラリのデータ型のラッピングを図れます。
`SIP <http://www.riverbankcomputing.co.uk/software/sip/>`_\ 、
`CXX <http://cxx.sourceforge.net/>`_\ 、
`Boost <http://www.boost.org/libs/python/doc/index.html>`_\ 、
`Weave <http://www.scipy.org/Weave>`_
でも C++ ライブラリをラッピングできます。


C から任意の Python 文を実行するにはどうしますか？
--------------------------------------------------

これを行う最高水準の関数は :c:func:`PyRun_SimpleString` で、
一つの文字列引数を取り、モジュール ``__main__`` のコンテキストでそれを実行し、
成功なら 0、例外 (``SyntaxError`` を含む) が発生したら -1 を返します。
更に制御したければ、\ :c:func:`PyRun_String`  を使ってください。
ソースは ``Python/pythonrun.c`` の ':c:func:`PyRun_SimpleString` を
参照してください。


C から任意の Python 式を評価するにはどうしますか？
--------------------------------------------------

先の質問の :c:func:`PyRun_String` を、スタートシンボル
:c:data:`Py_eval_input` を渡して呼び出してください。これは式を解析し、
評価してその値を返します。


Python オブジェクトから C の値を展開するにはどうしますか？
----------------------------------------------------------

オブジェクトの型に依ります。タプルなら、\ :c:func:`PyTuple_Size` が長さを返し、
:c:func:`PyTuple_GetItem` が指定されたインデックスの要素を返します。
リストにも同様の関数 :c:func:`PyList_Size` と :c:func:`PyList_GetItem` があります。

文字列なら、\ :c:func:`PyString_Size` が長さを、
:c:func:`PyString_AsString` がその値への
ポインタを返します。なお、Python の文字列には null バイトが含まれている
可能性があるので、C の :c:func:`strlen` は使うべきではありません。

オブジェクトの型を確かめるには、まず *NULL*  ではないことを確かめてから、
:c:func:`PyString_Check`\ 、\ :c:func:`PyTuple_Check`\ 、\ :c:func:`PyList_Check` などを
使ってください。

Python オブジェクトへの高レベルな API には、
いわゆる 'abstract' インタフェースが提供するものもあります。
機能の詳細は ``Include/abstract.h`` を読んでください。これで、
:c:func:`PySequence_Length` や :c:func:`PySequence_GetItem` などの
呼び出しであらゆるタイプの Python シーケンスのインタフェースができますし、
その他多くの役立つプロトコルもできます。


Py_BuildValue() で任意長のタプルを作るにはどうしますか？
--------------------------------------------------------

できません。代わりに ``t = PyTuple_New(n)`` を使い、
``PyTuple_SetItem(t, i, o)`` でオブジェクトを埋めてください --
なお、これは ``o`` のリファレンスカウントを"食う"ので、
:c:func:`Py_INCREF` しなければなりません。リストにも同様の
関数 ``PyList_New(n)`` と ``PyList_SetItem(l, i, o)`` があります。
なお、タプルは Python コードに渡される前に *必ず* すべての値が
設定されていなければなリません -- ``PyTuple_New(n)`` は各要素を
初期化して NULL にしますが、これは Python の適切な値ではありません。


C からオブジェクトのメソッドを呼び出すにはどうしますか？
--------------------------------------------------------

:c:func:`PyObject_CallMethod` 関数でオブジェクトの任意のメソッドを呼び出せます。
パラメタは、オブジェクト、呼び出すメソッドの名前、
:c:func:`Py_BuildValue` で
使われるようなフォーマット文字列、そして引数です::

   PyObject *
   PyObject_CallMethod(PyObject *object, char *method_name,
                       char *arg_format, ...);

これはメソッドを持ついかなるオブジェクトにも有効で、組み込みかユーザ定義かは
関係ありません。返り値に対して :c:func:`Py_DECREF` する必要が
あることもあります。

例えば、あるファイルオブジェクトの "seek" メソッドを
10, 0 を引数として呼ぶとき (ファイルオブジェクトのポインタを "f" とします)::

   res = PyObject_CallMethod(f, "seek", "(ii)", 10, 0);
   if (res == NULL) {
           ... an exception occurred ...
   }
   else {
           Py_DECREF(res);
   }

なお、\ :c:func:`PyObject_CallObject` の引数リストには *常に* タプルが必要です。
関数を引数なしで呼び出すには、フォーマットに "()" を渡し、
関数を一つの引数で呼び出すには、関数を括弧でくくって例えば
"(i)" としてください。


PyErr_Print() (その他 stdout/stderr に印字するもの) からの出力を受け取るにはどうしますか？
----------------------------------------------------------------------------------------------

Python コード内で、\ ``write()`` メソッドをサポートするオブジェクトを
定義してください。そのオブジェクトを :data:`sys.stdout` と :data:`sys.stderr`
に代入してください。print_error を呼び出すか、単に標準のトレースバック機構を
作動させてください。そうすれば、出力は ``write()`` が送る任意の所に行きます。

最も簡単な方法は、標準ライブラリの StringIO クラスを使うことです。

サンプルコードと出力の受け取り例:

   >>> class StdoutCatcher:
   ...     def __init__(self):
   ...         self.data = ''
   ...     def write(self, stuff):
   ...         self.data = self.data + stuff
   ...
   >>> import sys
   >>> sys.stdout = StdoutCatcher()
   >>> print 'foo'
   >>> print 'hello world!'
   >>> sys.stderr.write(sys.stdout.data)
   foo
   hello world!


C から Python で書かれたモジュールにアクセスするにはどうしますか？
------------------------------------------------------------------

以下のようにモジュールオブジェクトへのポインタを得られます::

   module = PyImport_ImportModule("<modulename>");

そのモジュールがまだインポートされていない (つまり、まだ
:data:`sys.modules` に現れていない) なら、これはモジュールを初期化します。
そうでなければ、単純に ``sys.modules["<modulename>"]``  の値を返します。
なお、これはモジュールをいかなる名前空間にも代入しません。
これはモジュールが初期化されて ':data:`sys.modules` に保管されていることを
保証するだけです。

これで、モジュールの属性 (つまり、モジュールで定義された任意の名前) に
以下のようにアクセスできるようになります::

   attr = PyObject_GetAttrString(module, "<attrname>");

:c:func:`PyObject_SetAttrString` を呼んでモジュールの変数に
代入することもできます。


Python から C++ へインタフェースするにはどうしますか？
------------------------------------------------------

やりたいことに応じて、いろいろな方法があります。手動でやるなら、
:ref:`"拡張と埋め込み" ドキュメント <extending-index>` を
読むことから始めてください。なお、Python ランタイムシステムにとっては、
C と C++ はあまり変わりません。だから、C 構造体 (ポインタ )型に基づいて
新しい Python の型を構築する方針は C++ オブジェクトに対しても有効です。

C++ ライブラリに関しては、\ :ref:`c-wrapper-software` を参照してください。


セットアップファイルでモジュールを追加しようとしたらメイクに失敗しました。なぜですか？
--------------------------------------------------------------------------------------

セットアップは改行で終わらなければならなくて、改行がないと、
ビルド工程は失敗します。(これを直すには、ある種の醜いシェルスクリプトハックが
必要ですが、このバグは小さいものですから努力に見合う価値はないでしょう。)


拡張をデバッグするにはどうしますか？
------------------------------------

動的にロードされた拡張に GDB を使うとき、拡張がロードされるまで
ブレークポイントを設定してはいけません。

``.gdbinit`` ファイルに(または対話的に)、このコマンドを加えてください::

   br _PyImport_LoadDynamicModule

そして、GDB を起動するときに::

   $ gdb /local/bin/python
   gdb) run myscript.py
   gdb) continue # repeat until your extension is loaded
   gdb) finish   # so that your extension is loaded
   gdb) br myfunction.c:50
   gdb) continue

Linux システムで Python モジュールをコンパイルしたいのですが、見つからないファイルがあります。なぜですか？
----------------------------------------------------------------------------------------------------------

Python の多くのパッケージバージョンには、Python 拡張をコンパイルするのに必要な
様々なファイルを含む :file:`/usr/lib/python2.{x}/config/` ディレクトリが
含まれていません。

Red Hat では、Python RPM をインストールして必要なファイルを得てください。

Debian では、\ ``apt-get install python-dev`` を実行してください。


"SystemError: _PyImport_FixupExtension: module yourmodule not loaded" とはどういう意味ですか？
----------------------------------------------------------------------------------------------

これは、"yourmodule" という名前の拡張モジュールが生成されたけれど、
モジュールの init 関数がその名前で初期化しないという意味です。

全てのモジュールの init 関数には次のような行があるでしょう::

   module = Py_InitModule("yourmodule", yourmodule_functions);

この関数に渡された文字列が拡張モジュールと同じ名前でない場合、
:exc:`SystemError` 例外が発生します。


"不完全 (incomplete) な入力" を "不適切 (invalid) な入力" から区別するにはどうしますか？
----------------------------------------------------------------------------------------

Python インタラクティブインタプリタでは、入力が不完全なとき (例えば、
"if" 文の始まりをタイプした時や、カッコや三重文字列引用符を閉じていない時など)
には継続プロンプトを与えられますが、入力が不適切であるときには
即座に構文エラーメッセージが与えられます。このようなふるまいを
模倣したいことがあります。

Python では構文解析器のふるまいに十分に近い :mod:`codeop` モジュールが
使えます。例えば IDLE がこれを使っています。

これを C で行う最も簡単な方法は、\ :c:func:`PyRun_InteractiveLoop` を
(必要ならば別のスレッドで) 呼び出し、Python インタプリタにあなたの
入力を扱わせることです。独自の入力関数を指定するのに
:c:func:`PyOS_ReadlineFunctionPointer` を設定することもできます。
詳しいヒントは、\ ``Modules/readline.c`` や ``Parser/myreadline.c`` を
参照してください。

しかし、組み込みの Python インタプリタを他のアプリケーションと
同じスレッドで実行することが必要で、\ :c:func:`PyRun_InteractiveLoop` で
ユーザの入力を待っている間止められないこともあります。
このような場合の解決策の一つは、\ :c:func:`PyParser_ParseString` を呼んで
``e.error`` と ``E_EOF`` が等しいこと、つまり入力が不完全であることを
確かめることです。これは、Alex Farber のコードを参考にした、コード片の例です::

   #include <Python.h>
   #include <node.h>
   #include <errcode.h>
   #include <grammar.h>
   #include <parsetok.h>
   #include <compile.h>

   int testcomplete(char *code)
     /* code should end in \n */
     /* return -1 for error, 0 for incomplete, 1 for complete */
   {
     node *n;
     perrdetail e;

     n = PyParser_ParseString(code, &_PyParser_Grammar,
                              Py_file_input, &e);
     if (n == NULL) {
       if (e.error == E_EOF)
         return 0;
       return -1;
     }

     PyNode_Free(n);
     return 1;
   }

別の解決策は、受け取られた文字列を :c:func:`Py_CompileString` で
コンパイルすることを試みることです。エラー無くコンパイルされたら、
返されたコードオブジェクトを :c:func:`PyEval_EvalCode` を呼んで
実行することを試みてください。そうでなければ、
入力を後のために保存してください。コンパイルが失敗したなら、
それがエラーなのか入力の続きが求められているだけなのか調べてください。
そのためには、例外タプルからメッセージ文字列を展開し、それを文字列
"unexpected EOF while parsing" と比較します。ここに GNU readline library を
使った完全な例があります (readline() を読んでいる間は **SIGINT** を
無視したいかもしれません)::

   #include <stdio.h>
   #include <readline.h>

   #include <Python.h>
   #include <object.h>
   #include <compile.h>
   #include <eval.h>

   int main (int argc, char* argv[])
   {
     int i, j, done = 0;                          /* lengths of line, code */
     char ps1[] = ">>> ";
     char ps2[] = "... ";
     char *prompt = ps1;
     char *msg, *line, *code = NULL;
     PyObject *src, *glb, *loc;
     PyObject *exc, *val, *trb, *obj, *dum;

     Py_Initialize ();
     loc = PyDict_New ();
     glb = PyDict_New ();
     PyDict_SetItemString (glb, "__builtins__", PyEval_GetBuiltins ());

     while (!done)
     {
       line = readline (prompt);

       if (NULL == line)                          /* CTRL-D pressed */
       {
         done = 1;
       }
       else
       {
         i = strlen (line);

         if (i > 0)
           add_history (line);                    /* save non-empty lines */

         if (NULL == code)                        /* nothing in code yet */
           j = 0;
         else
           j = strlen (code);

         code = realloc (code, i + j + 2);
         if (NULL == code)                        /* out of memory */
           exit (1);

         if (0 == j)                              /* code was empty, so */
           code[0] = '\0';                        /* keep strncat happy */

         strncat (code, line, i);                 /* append line to code */
         code[i + j] = '\n';                      /* append '\n' to code */
         code[i + j + 1] = '\0';

         src = Py_CompileString (code, "<stdin>", Py_single_input);

         if (NULL != src)                         /* compiled just fine - */
         {
           if (ps1  == prompt ||                  /* ">>> " or */
               '\n' == code[i + j - 1])           /* "... " and double '\n' */
           {                                               /* so execute it */
             dum = PyEval_EvalCode ((PyCodeObject *)src, glb, loc);
             Py_XDECREF (dum);
             Py_XDECREF (src);
             free (code);
             code = NULL;
             if (PyErr_Occurred ())
               PyErr_Print ();
             prompt = ps1;
           }
         }                                        /* syntax error or E_EOF? */
         else if (PyErr_ExceptionMatches (PyExc_SyntaxError))
         {
           PyErr_Fetch (&exc, &val, &trb);        /* clears exception! */

           if (PyArg_ParseTuple (val, "sO", &msg, &obj) &&
               !strcmp (msg, "unexpected EOF while parsing")) /* E_EOF */
           {
             Py_XDECREF (exc);
             Py_XDECREF (val);
             Py_XDECREF (trb);
             prompt = ps2;
           }
           else                                   /* some other syntax error */
           {
             PyErr_Restore (exc, val, trb);
             PyErr_Print ();
             free (code);
             code = NULL;
             prompt = ps1;
           }
         }
         else                                     /* some non-syntax error */
         {
           PyErr_Print ();
           free (code);
           code = NULL;
           prompt = ps1;
         }

         free (line);
       }
     }

     Py_XDECREF(glb);
     Py_XDECREF(loc);
     Py_Finalize();
     exit(0);
   }


未定義の g++ シンボル __builtin_new や __pure_virtual を見つけるにはどうしますか？
----------------------------------------------------------------------------------

g++ モジュールを動的にロードするには、Python を再コンパイルし、
それを g++ で再リンク (Python Modules Makefile 内の LINKCC を変更) し、
拡張を g++ でリンク (例えば ``g++ -shared -o mymodule.so mymodule.o``)
しなければなりません。


メソッドのいくつかは C で、その他は Python で実装されたオブジェクトクラスを (継承などで) 作ることはできますか？
---------------------------------------------------------------------------------------------------------------

Python 2.2 では、\ :class:`int`\ 、\ :class:`list`\ 、\ :class:`dict` などの
ビルトインクラスから継承できます。

The Boost Python Library (BPL, http://www.boost.org/libs/python/doc/index.html)
を使えば、これを C++ からできます。
(すなわち、BPL を使って C++ で書かれた拡張クラスを継承できます).


モジュール X をインポートした時に "undefined symbol: PyUnicodeUCS2*" と言われるのはなぜですか？
-----------------------------------------------------------------------------------------------

あなたは Unicode 文字に 4 バイト表現を使う Python のバージョンを
使っていますが、インポートされた C 拡張モジュールに Unicode 文字に
(デフォルトの) 2 バイト表現を使う Python でコンパイルされたものがあります。

未定義のシンボルの名前が ``PyUnicodeUCS4`` で始まるのなら、
逆の問題です: Python は 2 バイト Unicode 文字でビルトされていて、
拡張モジュールは 4 バイト Unicode 文字の Python でコンパイルされています。

これはあらかじめビルドされた拡張パッケージを使っているときに起こりやすいです。
とりわけ、RedHat Linux 7.x は 4 バイトユニコードでコンパイルされた
"python2" バイナリを提供しました。これは拡張が ``PyUnicode_*()`` 関数の
どれかを使っているとリンクの失敗を起こすだけです。拡張が Unicode に関連する
:c:func:`Py_BuildValue` (等)へのフォーマット指定や :c:func:`PyArg_ParseTuple`
へのパラメタ指定を何かしら含んでいても問題になります。

Python インタプリタが使っている Unicode 文字のサイズは、
sys.maxunicode の値を調べることで確かめられます:

   >>> import sys
   >>> if sys.maxunicode > 65535:
   ...     print 'UCS4 build'
   ... else:
   ...     print 'UCS2 build'

この問題を解決する唯一の方法は、Unicode 文字に同じサイズを使ってビルドされた
Python バイナリでコンパイルされた拡張モジュールを使うことです。


