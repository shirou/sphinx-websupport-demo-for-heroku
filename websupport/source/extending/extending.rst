.. highlightlang:: c

.. _extending-intro:

*****************************
C や C++ による Python の拡張
*****************************

C プログラムの書き方を知っているなら、Python に新たな組み込みモジュールを追加するのはきわめて簡単です。この新たなモジュール、拡張モジュール
(:dfn:`extention module`) を使うと、Python が直接行えない二つのこと: 新しい組み込みオブジェクトの実装、そして全ての C
ライブラリ関数とシステムコールに対する呼び出し、ができるようになります。

拡張モジュールをサポートするため、Python API (Application Programmer's Interface) では一連の関数、マクロ
および変数を提供していて、Python ランタイムシステムのほとんどの側面へのアクセス手段を提供しています。 Python API は、ヘッダ
``"Python.h"`` をインクルードして C ソースに取り込みます。

拡張モジュールのコンパイル方法は、モジュールの用途やシステムの設定方法に依存します; 詳細は後の章で説明します。

もし C ライブラリ関数やシステムコールを呼び出すような使い方を考えているなら、
C のコードをいちいち書く前に :mod:`ctypes` モジュールの使用を検討してください。
:mod:`ctypes` モジュールを使うと C のコードを扱う Python のコードが書けるようになるだけでなく、
拡張モジュールを書きコンパイルして CPython に縛られてしまうよりも Python の実装間での互換性を高めることができます。


.. _extending-simpleexample:

簡単な例
========

``spam`` (Monty Python ファンの好物ですね) という名の拡張モジュールを作成することにして、C ライブラリ関数
:c:func:`system` に対する Python インタフェースを作成したいとします。  [#]_ この関数は null
で終端されたキャラクタ文字列を引数にとり、整数を返します。この関数を以下のようにして Python から呼び出せるようにしたいとします::

   >>> import spam
   >>> status = spam.system("ls -l")

まずは :file:`spammodule.c` を作成するところから始めます。 (伝統として、 ``spam`` という名前のモジュールを作成する場合、
モジュールの実装が入った C ファイルを :file:`spammodule.c` と呼ぶことになっています;  ``spammify`` のように長すぎる
モジュール名の場合には、単に :file:`spammify.c` にもできます。)

このファイルの最初の行は以下のようにします::

   #include <Python.h>

これで、Python API を取り込みます (必要なら、モジュールの用途に関する説明や、著作権表示を追加します)。 

.. note::

   Python は、システムによっては標準ヘッダの定義に影響するようなプリプロセッサ定義を行っているので、 :file:`Python.h` を
   いずれの標準ヘッダよりも前にインクルード *せねばなりません* 。

:file:`Python.h` で定義されているユーザから可視のシンボルは、全て接頭辞 ``Py`` または ``PY`` が付いています。ただし、
標準ヘッダファイル内の定義は除きます。簡単のためと、Python 内で広範に使うことになるという理由から、 ``"Python.h"``
はいくつかの標準ヘッダファイル: ``<stdio.h>`` 、 ``<string.h>`` 、 ``<errno.h>`` 、および ``<stdlib.h>``
をインクルードしています。後者のヘッダファイルがシステム上になければ、 ``"Python.h"`` が関数
:c:func:`malloc` 、 :c:func:`free` および  :c:func:`realloc` を直接定義します。

次にファイルに追加する内容は、Python 式 ``spam.system(string)`` を評価する際に呼び出されることになる C 関数です
(この関数を最終的にどのように呼び出すかは、後ですぐわかります)::

   static PyObject *
   spam_system(PyObject *self, PyObject *args)
   {
       const char *command;
       int sts;

       if (!PyArg_ParseTuple(args, "s", &command))
           return NULL;
       sts = system(command);
       return Py_BuildValue("i", sts);
   }

ここでは、Python の引数リスト (例えば、単一の式 ``"ls -l"``)  から C 関数に渡す引数にそのまま変換しています。 C
関数は常に二つの引数を持ち、便宜的に *self* および *args* と呼ばれます。

*self* 引数には、モジュールレベルの関数であればモジュールが、メソッドには
オブジェクトインスタンスが渡されます。

*args* 引数は、引数の入った Python タプルオブジェクトへのポインタになります。タプル内の各要素は、呼び出しの際の引数リストに
おける各引数に対応します。引数は Python オブジェクトです ---  C 関数で引数を使って何かを行うには、オブジェクトから C の値に
変換せねばなりません。Python API の関数 :c:func:`PyArg_ParseTuple` は引数の型をチェックし、C の値に変換します。
:c:func:`PyArg_ParseTuple` はテンプレート文字列を使って、引数オブジェクトの型と、変換された値を入れる C 変数の型を判別します。
これについては後で詳しく説明します。

:c:func:`PyArg_ParseTuple` は、全ての引数が正しい型を持っていて、アドレス渡しされた各変数に各引数要素を保存したときに真 (非ゼロ)
を返します。この関数は不正な引数リストを渡すと偽 (ゼロ) を返します。後者の場合、関数は適切な例外を送出するので、呼び出し側は (例にもあるように)
すぐに *NULL* を返すようにしてください。


.. _extending-errors:

幕間小話: エラーと例外
======================

Python インタプリタ全体を通して、一つの重要な取り決めがあります: それは、関数が処理に失敗した場合、例外状態をセットして、エラーを示す値 (通常は
*NULL* ポインタ) を返さねばならない、ということです。例外はインタプリタ内の静的なグローバル変数に保存されます; この値が *NULL*
の場合、例外は何も起きていないことになります。第二のグローバル変数には、例外の "付属値 (associated value)"
(:keyword:`raise` 文の第二引数) が入ります。第三の値には、エラーの発生源が Python コード内だった場合にスタックトレースバック
(stack traceback) が入ります。これらの三つの変数は、それぞれ Python の変数 ``sys.exc_type`` 、
``sys.exc_value`` および ``sys.exc_traceback`` と等価な C の変数です (Python ライブラリリファレンスの
:mod:`sys` モジュールに関する節を参照してください。)
エラーがどのように受け渡されるかを理解するには、これらの変数についてよく知っておくことが重要です。

Python API では、様々な型の例外をセットするための関数をいくつか定義しています。

もっともよく用いられるのは :c:func:`PyErr_SetString` です。引数は例外オブジェクトと C 文字列です。例外オブジェクトは
通常、 :c:data:`PyExc_ZeroDivisionError` のような定義済みのオブジェクトです。 C 文字列はエラーの原因を示し、Python
文字列オブジェクトに変換されて例外の "付属値" に保存されます。

もう一つ有用な関数として :c:func:`PyErr_SetFromErrno` があります。この関数は引数に例外だけをとり、付属値はグローバル変数
:c:data:`errno` から構築します。もっとも汎用的な関数は :c:func:`PyErr_SetObject` で、
二つのオブジェクト、例外と付属値を引数にとります。これら関数に渡すオブジェクトには :c:func:`Py_INCREF` を使う必要はありません。

例外がセットされているかどうかは、 :c:func:`PyErr_Occurred`  を使って非破壊的に調べられます。この関数は現在の例外オブジェクトを
返します。例外が発生していない場合には *NULL* を返します。通常は、関数の戻り値からエラーが発生したかを判別できるはずなので、
:c:func:`PyErr_Occurred` を呼び出す必要はありません。

関数 *g* を呼び出す *f* が、前者の関数の呼び出しに失敗したことを検出すると、 *f* 自体はエラー値 (大抵は *NULL* や ``-1``)
を返さねばなりません。しかし、 :c:func:`PyErr_\*` 関数群のいずれかを呼び出す必要は *ありません* --- なぜなら、 *g*
がすでに呼び出しているからです。次いで *f* を呼び出したコードもエラーを示す値を *自らを呼び出したコード* に返すことになりますが、
同様に :c:func:`PyErr_\*` は *呼び出しません* 。以下同様に続きます --- エラーの最も詳しい原因は、最初にエラーを検出した
関数がすでに報告しているからです。エラーが Python インタプリタのメインループに到達すると、現在実行中の Python コードは一時停止し、
Python プログラマが指定した例外ハンドラを探し出そうとします。

(モジュールが :c:func:`PyErr_\*` 関数をもう一度呼び出して、より詳細なエラーメッセージを提供するような状況があります。このような状況では
そうすべきです。とはいえ、一般的な規則としては、 :c:func:`PyErr_\*`  を何度も呼び出す必要はなく、ともすればエラーの原因に関する情報を
失う結果になりがちです: これにより、ほとんどの操作が様々な理由から失敗するかもしれません)

ある関数呼び出しでの処理の失敗によってセットされた例外を無視するには、 :c:func:`PyErr_Clear` を呼び出して例外状態を明示的に消去
しなくてはなりません。エラーをインタプリタには渡したくなく、自前で (何か他の作業を行ったり、何も起こらなかったかのように見せかけるような)
エラー処理を完全に行う場合にのみ、 :c:func:`PyErr_Clear` を呼び出すようにすべきです。

:c:func:`malloc` の呼び出し失敗は、常に例外にしなくてはなりません --- :c:func:`malloc` (または
:c:func:`realloc`) を直接呼び出しているコードは、 :c:func:`PyErr_NoMemory`
を呼び出して、失敗を示す値を返さねばなりません。オブジェクトを生成する全ての関数 (例えば :c:func:`PyInt_FromLong`) は
:c:func:`PyErr_NoMemory` の呼び出しを済ませてしまうので、この規則が関係するのは直接 :c:func:`malloc` を呼び出す
コードだけです。

また、 :c:func:`PyArg_ParseTuple` という重要な例外を除いて、整数の状態コードを返す関数はたいてい、Unix のシステムコール
と同じく、処理が成功した際にはゼロまたは正の値を返し、失敗した場合には ``-1`` を返します。

最後に、エラー標示値を返す際に、(エラーが発生するまでに既に生成してしまったオブジェクトに対して :c:func:`Py_XDECREF` や
:c:func:`Py_DECREF` を呼び出して) ごみ処理を注意深く行ってください!

どの例外を返すかの選択は、ユーザに完全にゆだねられます。 :c:data:`PyExc_ZeroDivisionError` のように、全ての組み込みの
Python  例外には対応する宣言済みの C オブジェクトがあり、直接利用できます。もちろん、例外の選択は賢く行わねばなりません ---
ファイルが開けなかったことを表すのに :c:data:`PyExc_TypeError`  を使ったりはしないでください
(この場合はおそらく :c:data:`PyExc_IOError`  の方にすべきでしょう)。
引数リストに問題がある場合には、 :c:func:`PyArg_ParseTuple`  はたいてい :c:data:`PyExc_TypeError`
を送出します。引数の値が特定の範囲を超えていたり、その他の満たすべき条件を満たさなかった場合には、 :c:data:`PyExc_ValueError`
が適切です。

モジュール固有の新たな例外も定義できます。定義するには、通常はファイルの先頭部分に静的なオブジェクト変数の宣言を行います::

   static PyObject *SpamError;

そして、モジュールの初期化関数 (:c:func:`initspam`) の中で、例外オブジェクトを使って初期化します (ここでは
エラーチェックを省略しています)::

   PyMODINIT_FUNC
   initspam(void)
   {
       PyObject *m;

       m = Py_InitModule("spam", SpamMethods);
       if (m == NULL)
           return;

       SpamError = PyErr_NewException("spam.error", NULL, NULL);
       Py_INCREF(SpamError);
       PyModule_AddObject(m, "error", SpamError);
   }

Python レベルでの例外オブジェクトの名前は :exc:`spam.error` になることに注意してください。
:c:func:`PyErr_NewException`  関数は、 :ref:`bltin-exceptions` で述べられている
:exc:`Exception` クラスを基底クラスに持つ例外クラスも作成できます  (*NULL* の代わりに他のクラスを渡した場合は別です)。

:c:data:`SpamError` 変数は、新たに生成された例外クラスへの参照を維持することにも注意してください; これは意図的な仕様です!
外部のコードが例外オブジェクトをモジュールから除去できるため、モジュールから新たに作成した例外クラスが見えなくなり、 :c:data:`SpamError`
がぶら下がりポインタ (dangling pointer) になってしまわないようにするために、クラスに対する参照を所有しておかねばなりません。
もし :c:data:`SpamError` がぶら下がりポインタになってしまうと、 C コードが例外を送出しようとしたときにコアダンプや意図しない副作用を
引き起こすことがあります。

この例にある、関数の戻り値型に ``PyMODINIT_FUNC`` を使う方法については後で議論します。

:c:func:`PyErr_SetString` を次のように呼び出すと、拡張モジュールで例外 :exc:`spam.error` を送出することができます::
 
   static PyObject *
   spam_system(PyObject *self, PyObject *args)
   {
       const char *command;
       int sts;
 
       if (!PyArg_ParseTuple(args, "s", &command))
           return NULL;
       sts = system(command);
       if (sts < 0) {
           PyErr_SetString(SpamError, "System command failed");
           return NULL;
       }
       return PyLong_FromLong(sts);
   }

.. _backtoexample:

例に戻る
========

先ほどの関数の例に戻ると、今度は以下の実行文を理解できるはずです::

   if (!PyArg_ParseTuple(args, "s", &command))
       return NULL;

この実行文は、 :c:func:`PyArg_ParseTuple` がセットする例外によって、引数リストに何らかのエラーが生じたときに *NULL*
(オブジェクトへのポインタを返すタイプの関数におけるエラー標示値)  を返します。エラーでなければ、引数として与えた文字列値はローカルな変数
:c:data:`command` にコピーされています。この操作はポインタ代入であり、ポインタが指している文字列に対して変更が行われるとは想定されていません
(従って、標準 C では、変数 :c:data:`command` は ``const char* command`` として適切に定義せねばなりません)。

次の文では、 :c:func:`PyArg_ParseTuple` で得た文字列を渡して Unix 関数 :c:func:`system` を呼び出しています::

   sts = system(command);

:func:`spam.system` は :c:data:`sts` を Python オブジェクト
として返さねばなりません。これには、 :c:func:`PyArg_ParseTuple` の逆ともいうべき関数 :c:func:`Py_BuildValue`
を使います: :c:func:`Py_BuildValue` は書式化文字列と任意の数の C の値を引数にとり、新たな Python オブジェクトを返します。
:c:func:`Py_BuildValue` に関する詳しい情報は後で示します。 ::

   return Py_BuildValue("i", sts);

上の場合では、 :c:func:`Py_BuildValue` は整数オブジェクトを返します。(そう、整数ですら、 Python においてはヒープ上の
オブジェクトなのです! )

何ら有用な値を返さない関数 (:c:type:`void` を返す関数) に対応する Python の関数は ``None`` を返さねばなりません。関数に
``None`` を返させるには、以下のような慣用句を使います (この慣用句は :c:macro:`Py_RETURN_NONE` マクロに実装されています)::

   Py_INCREF(Py_None);
   return Py_None;

:c:data:`Py_None` は特殊な Pyhton オブジェクトである ``None`` に対応する C
での名前です。これまで見てきたようにほとんどのコンテキストで "エラー" を意味する *NULL* ポインタとは違い、 ``None`` は純粋な Python
のオブジェクトです。


.. _methodtable:

モジュールのメソッドテーブルと初期化関数
========================================

さて、前に約束したように、 :c:func:`spam_system` を Python プログラム
からどうやって呼び出すかをこれから示します。まずは、関数名とアドレスを "メソッドテーブル (method table)" に列挙する必要があります::

   static PyMethodDef SpamMethods[] = {
       ...
       {"system",  spam_system, METH_VARARGS,
        "Execute a shell command."},
       ...
       {NULL, NULL, 0, NULL}        /* Sentinel */
   };

リスト要素の三つ目のエントリ (``METH_VARARGS``) に注意してください。このエントリは、C 関数が使う呼び出し規約をインタプリタに教えるための
フラグです。通常この値は ``METH_VARARGS`` か ``METH_VARARGS | METH_KEYWORDS`` のはずです; ``0``
は旧式の :c:func:`PyArg_ParseTuple` の変化形が使われることを意味します。

``METH_VARARGS`` だけを使う場合、C 関数は、Python レベルでの引数が :c:func:`PyArg_ParseTuple`
が受理できるタプルの形式で渡されるものと想定しなければなりません; この関数についての詳細は下で説明します。

関数にキーワード引数が渡されることになっているのなら、第三フィールドに :const:`METH_KEYWORDS` ビットをセットできます。この場合、C
関数は第三引数に ``PyObject *`` を受理するようにせねばなりません。このオブジェクトは、キーワード引数の辞書に
なります。こうした関数で引数を解釈するには、 :c:func:`PyArg_ParseTupleAndKeywords` を使ってください。

メソッドテーブルは、モジュールの初期化関数内でインタプリタに渡さねばなりません。
初期化関数はモジュールの名前を *name* としたときに
:c:func:`initname` という名前でなければならず、
モジュールファイル内で定義されているもののうち、唯一の非 `static`
要素でなければなりません::

   PyMODINIT_FUNC
   initspam(void)
   {
       (void) Py_InitModule("spam", SpamMethods);
   }

PyMODINIT_FUNC は関数の戻り値を ``void`` になるように宣言し、プラットフォーム毎に必要とされる、特有のリンク宣言 (linkage
declaration) を定義すること、さらに C++ の場合には関数を ``extern "C"`` に宣言することに注意してください。

Python プログラムがモジュール :mod:`spam` を初めて import するとき、 :c:func:`initspam` が呼び出されます。
(Python の埋め込みに関するコメントは下記を参照してください。) :c:func:`initspam` は :c:func:`Py_InitModule`
を呼び出して "モジュールオブジェクト" を生成し (オブジェクトは ``"spam"`` をキーとして辞書 ``sys.modules``
に挿入されます)、第二引数として与えたメソッドテーブル (:c:type:`PyMethodDef` 構造体の配列) の情報に
基づいて、組み込み関数オブジェクトを新たなモジュールに挿入していきます。 :c:func:`Py_InitModule` は、自らが生成した
(この段階ではまだ未使用の)  モジュールオブジェクトへのポインタを返します。
:c:func:`Py_InitModule`
は、幾つかのエラーでは致命的エラーで abort し、それ以外のモジュールが満足に初期化できなかった場合は
*NULL* を返します。

Python を埋め込む場合には、 :c:data:`_PyImport_Inittab` テーブルのエントリ内に :c:func:`initspam`
がない限り、 :c:func:`initspam` は自動的には呼び出されません。この問題を解決する最も簡単な方法は、 :c:func:`Py_Initialize`
や :c:func:`PyMac_Initialize` を呼び出した後に :c:func:`initspam` を直接呼び出し、
静的にリンクしておいたモジュールを静的に初期化してしまうというものです::

   int
   main(int argc, char *argv[])
   {
       /* Python インタプリタに argv[0] を渡す */
       Py_SetProgramName(argv[0]);

       /* Python インタプリタを初期化する。必ず必要。 */
       Py_Initialize();

       /* 静的モジュールを追加する */
       initspam();

Python ソース配布物中の :file:`Demo/embed/demo.c` ファイル内に例があります。

.. note::

   単一のプロセス内 (または :c:func:`fork` 後の :c:func:`exec` が介入していない状態) における複数のインタプリタにおいて、
   ``sys.module`` からエントリを除去したり新たなコンパイル済みモジュールを import
   したりすると、拡張モジュールによっては問題を生じることがあります。拡張モジュールの作者は、内部データ構造を初期化する際にはよくよく
   用心すべきです。また、 :func:`reload` 関数を拡張モジュールに対して利用でき、この場合はモジュール初期化関数
   (:c:func:`initspam`) は呼び出されますが、モジュールが動的にロード可能なオブジェクトファイル (Unixでは
   :file:`.so` 、Windows では :file:`.dll`) から読み出された場合にはモジュールファイルを再読み込みしないので注意してください。

より実質的なモジュール例は、Python ソース配布物に :file:`Modules/xxmodule.c` という名前で入っています。
このファイルはテンプレートとしても利用できますし、単に例としても読めます。


.. _compilation:

コンパイルとリンク
==================

新しい拡張モジュールを使えるようになるまで、まだ二つの作業:  コンパイルと、Python システムへのリンク、が残っています。動的読み込み (dynamic
loading) を使っているのなら、作業の詳細は自分のシステムが使っている動的読み込みの形式によって変わるかもしれません;
詳しくは、拡張モジュールのビルドに関する章  (:ref:`building` 章) や、Windows におけるビルドに関係する追加情報の章
(:ref:`building-on-windows` 章) を参照してください。

動的読み込みを使えなかったり、モジュールを常時 Python インタプリタの一部にしておきたい場合には、インタプリタのビルド設定を変更して再ビルド
しなければならなくなるでしょう。Unixでは、幸運なことにこの作業はとても単純です: 単に自作のモジュールファイル (例えば
:file:`spammodule.c` ) を展開したソース配布物の :file:`Modules/`  ディレクトリに置き、
:file:`Modules/Setup.local` に自分のファイルを説明する以下の一行::

   spam spammodule.o

を追加して、トップレベルのディレクトリで :program:`make` を実行して、インタプリタを再ビルドするだけです。 :file:`Modules/`
サブディレクトリでも :program:`make` を実行できますが、前もって ':program:`make` Makefile' を実行して
:file:`Makefile` を再ビルドしておかなければならりません。(この作業は :file:`Setup` ファイルを変更するたびに必要です。)

モジュールが別のライブラリとリンクされている必要がある場合、ライブラリも設定ファイルに列挙できます。例えば以下のようにします::

   spam spammodule.o -lX11


.. _callingpython:

C から Python 関数を呼び出す
============================

これまでは、Python からの C 関数の呼び出しに重点を置いて述べてきました。ところでこの逆:  C からの Python 関数の呼び出し
もまた有用です。とりわけ、いわゆる "コールバック" 関数をサポートするようなライブラリを作成する際にはこの機能が便利です。ある C
インタフェースがコールバックを利用している場合、同等の機能を提供する Python コードでは、しばしば Python プログラマに
コールバック機構を提供する必要があります; このとき実装では、 C で書かれたコールバック関数から Python で書かれたコールパック関数
を呼び出すようにする必要があるでしょう。もちろん、他の用途も考えられます。

幸運なことに、Python インタプリタは簡単に再帰呼び出しでき、 Python 関数を呼び出すための標準インタフェースもあります。 (Python
パーザを特定の入力文字を使って呼び出す方法について詳説するつもりはありません --- この方法に興味があるなら、 Python ソースコードの
:file:`Modules/main.c` にある、コマンドラインオプション :option:`-c` の実装を見てください)

Python 関数の呼び出しは簡単です。まず、C のコードに対してコールバックを登録しようとする Python プログラムは、何らかの方法で Python
の関数オブジェクトを渡さねばなりません。このために、コールバック登録関数 (またはその他のインタフェース) を提供
せねばなりません。このコールバック登録関数が呼び出された際に、引き渡された Python 関数オブジェクトへのポインタをグローバル変数に ---
あるいは、どこか適切な場所に --- 保存します (関数オブジェクトを :c:func:`Py_INCREF` するようよく注意して
ください!)。例えば、以下のような関数がモジュールの一部になっていることでしょう::

   static PyObject *my_callback = NULL;

   static PyObject *
   my_set_callback(PyObject *dummy, PyObject *args)
   {
       PyObject *result = NULL;
       PyObject *temp;

       if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
           if (!PyCallable_Check(temp)) {
               PyErr_SetString(PyExc_TypeError, "parameter must be callable");
               return NULL;
           }
           Py_XINCREF(temp);         /* 新たなコールバックへの参照を追加 */
           Py_XDECREF(my_callback);  /* 以前のコールバックを捨てる */
           my_callback = temp;       /* 新たなコールバックを記憶 */
           /* "None" を返す際の定型句 */
           Py_INCREF(Py_None);
           result = Py_None;
       }
       return result;
   }

この関数は :const:`METH_VARARGS` フラグを使ってインタプリタに登録せねばなりません; :const:`METH_VARARGS`
フラグについては、 :ref:`methodtable` で説明しています。
:c:func:`PyArg_ParseTuple` 関数とその引数については、 :ref:`parsetuple` に記述しています。

:c:func:`Py_XINCREF` および :c:func:`Py_XDECREF` は、オブジェクトに対する参照カウントをインクリメント/デクリメントする
ためのマクロで、 *NULL* ポインタが渡されても安全に操作できる形式です (とはいえ、上の流れでは *temp* が *NULL* になることはありません)。
これらのマクロと参照カウントについては、 :ref:`refcounts` で説明しています。

.. index:: single: PyObject_CallObject()

その後、コールバック関数を呼び出す時が来たら、C 関数 :c:func:`PyObject_CallObject` を呼び出します。この関数には二つの引数:
Python 関数と Python 関数の引数リストがあり、いずれも任意の Python オブジェクトを表すポインタ型です。
引数リストは常にタプルオブジェクトでなければならず、その長さは引数の数になります。Python 関数を引数なしで呼び出すのなら、
NULL か空のタプルを渡します;
単一の引数で関数を呼び出すのなら、単要素 (singleton) のタプルを渡します。 :c:func:`Py_BuildValue`
の書式化文字列中に、ゼロ個または一個以上の書式化コードが入った丸括弧がある場合、この関数はタプルを返します。以下に例を示します::

   int arg;
   PyObject *arglist;
   PyObject *result;
   ...
   arg = 123;
   ...
   /* ここでコールバックを呼ぶ */
   arglist = Py_BuildValue("(i)", arg);
   result = PyObject_CallObject(my_callback, arglist);
   Py_DECREF(arglist);

:c:func:`PyObject_CallObject` は Python オブジェクトへのポインタを返します; これは Python
関数からの戻り値になります。 :c:func:`PyObject_CallObject` は、引数に対して "参照カウント中立 (reference-count-
neutral)" です。上の例ではタプルを生成して引数リストとして提供しており、このタプルは呼び出し直後に :c:func:`Py_DECREF`
しています。

:c:func:`PyObject_CallObject` は戻り値として "新しい" オブジェクト: 新規に作成されたオブジェクトか、既存のオブジェクトの
参照カウントをインクリメントしたものを返します。
従って、このオブジェクトをグローバル変数に保存したいのでないかぎり、たとえこの戻り値に興味がなくても
(むしろ、そうであればなおさら!) 何がしかの方法で戻り値オブジェクトを :c:func:`Py_DECREF`  しなければなりません。

とはいえ、戻り値を :c:func:`Py_DECREF` する前には、値が *NULL* でないかチェックしておくことが重要です。もし
*NULL* なら、呼び出した Python 関数は例外を送出して終了させられています。 :c:func:`PyObject_CallObject`
を呼び出しているコード自体もまた Python から呼び出されているのであれば、今度は C コードが自分を呼び出している Python
コードにエラー標示値を返さねばなりません。それにより、インタプリタはスタックトレースを出力したり、例外を処理するための Python
コードを呼び出したりできます。例外の送出が不可能だったり、したくないのなら、 :c:func:`PyErr_Clear`
を呼んで例外を消去しておかねばなりません。例えば以下のようにします::

   if (result == NULL)
       return NULL; /* エラーを返す */
   ...use result...
   Py_DECREF(result);

Python コールバック関数をどんなインタフェースにしたいかによっては、引数リストを :c:func:`PyObject_CallObject` に与えなければ
ならない場合もあります。あるケースでは、コールバック関数を指定したのと同じインタフェースを介して、引数リストも渡されているかもしれません。
また別のケースでは、新しいタプルを構築して引数リストを渡さねばならないかもしれません。この場合最も簡単なのは :c:func:`Py_BuildValue`
を呼ぶやり方です。例えば、整数のイベントコードを渡したければ、以下のようなコードを使うことになるでしょう::

   PyObject *arglist;
   ...
   arglist = Py_BuildValue("(l)", eventcode);
   result = PyObject_CallObject(my_callback, arglist);
   Py_DECREF(arglist);
   if (result == NULL)
       return NULL; /* エラーを返す */
   /* 場合によってはここで結果を使うかもね */
   Py_DECREF(result);

``Py_DECREF(arglist)`` が呼び出しの直後、エラーチェックよりも前に置かれていることに注意してください! また、厳密に言えば、このコードは
完全ではありません: :c:func:`Py_BuildValue` はメモリ不足におちいるかもしれず、チェックしておくべきです。

通常の引数とキーワード引数をサポートする :c:func:`PyObject_Call` を使って、
キーワード引数を伴う関数呼び出しをすることができます。
上の例と同じように、 :c:func:`Py_BuildValue` を作って辞書を作ります。 ::

   PyObject *dict;
   ...
   dict = Py_BuildValue("{s:i}", "name", val);
   result = PyObject_Call(my_callback, NULL, dict);
   Py_DECREF(dict);
   if (result == NULL)
       return NULL; /* エラーを返す */
   /* 場合によってはここで結果を使うかもね */
   Py_DECREF(result);


.. _parsetuple:

拡張モジュール関数でのパラメタ展開
==================================

.. index:: single: PyArg_ParseTuple()

:c:func:`PyArg_ParseTuple` は、以下のように宣言されています::

   int PyArg_ParseTuple(PyObject *arg, char *format, ...);

引数 *arg* は C 関数から Python に渡される引数リストが入ったタプルオブジェクトでなければなりません。
*format* 引数は書式化文字列で、
Python/C API リファレンスマニュアルの :ref:`arg-parsing` で解説されている書法に従わねばなりません。
残りの引数は、それぞれの変数のアドレスで、書式化文字列から決まる型になっていなければなりません。

:c:func:`PyArg_ParseTuple` は Python 側から与えられた引数が
必要な型になっているか調べるのに対し、 :c:func:`PyArg_ParseTuple`  は呼び出しの際に渡された C 変数のアドレスが有効な値を持つか調べ
られないことに注意してください: ここで間違いを犯すと、コードがクラッシュするかもしれませんし、少なくともでたらめなビットを
メモリに上書きしてしまいます。慎重に!

呼び出し側に提供されるオブジェクトへの参照はすべて *借用* 参照 (borrowed reference) になります; これらのオブジェクトの参照
カウントをデクリメントしてはなりません!

以下にいくつかの呼び出し例を示します::

   int ok;
   int i, j;
   long k, l;
   const char *s;
   int size;

   ok = PyArg_ParseTuple(args, ""); /* 引数なし */
       /* Python での呼び出し: f() */

::

   ok = PyArg_ParseTuple(args, "s", &s); /* 文字列 */
       /* Python での呼び出し例: f('whoops!') */

::

   ok = PyArg_ParseTuple(args, "lls", &k, &l, &s);
       /* 二つの long と文字列 */
       /* Python での呼び出し例: f(1, 2, 'three') */

::

   ok = PyArg_ParseTuple(args, "(ii)s#", &i, &j, &s, &size);
       /* 二つの int と文字列、文字列のサイズも返す */
       /* Python での呼び出し例: f((1, 2), 'three') */

::

   {
       const char *file;
       const char *mode = "r";
       int bufsize = 0;
       ok = PyArg_ParseTuple(args, "s|si", &file, &mode, &bufsize);
       /* 文字列、オプションとして文字列がもう一つと整数が一つ */
       /* Python での呼び出し例:
          f('spam')
          f('spam', 'w')
          f('spam', 'wb', 100000) */
   }

::

   {
       int left, top, right, bottom, h, v;
       ok = PyArg_ParseTuple(args, "((ii)(ii))(ii)",
                &left, &top, &right, &bottom, &h, &v);
       /* 矩形と点を表現するデータ */
       /* Python での呼び出し例:
          f(((0, 0), (400, 300)), (10, 10)) */
   }

::

   {
       Py_complex c;
       ok = PyArg_ParseTuple(args, "D:myfunction", &c);
       /* 複素数。エラー発生時用に関数名も指定 */
       /* Python での呼び出し例: myfunction(1+2j) */
   }


.. _parsetupleandkeywords:

拡張モジュール関数のキーワードパラメタ
======================================

.. index:: single: PyArg_ParseTupleAndKeywords()

:c:func:`PyArg_ParseTupleAndKeywords`  は、以下のように宣言されています::

   int PyArg_ParseTupleAndKeywords(PyObject *arg, PyObject *kwdict,
                                   char *format, char *kwlist[], ...);

*arg* と *format* パラメタは :c:func:`PyArg_ParseTuple`  のものと同じです。 *kwdict*
パラメタはキーワード引数の入った辞書で、 Python ランタイムシステムから第三パラメタとして受け取ります。 *kwlist*
パラメタは各パラメタを識別するための文字列からなる、 *NULL* 終端されたリストです; 各パラメタ名は *format* 中の
型情報に対して左から右の順に照合されます。

成功すると :c:func:`PyArg_ParseTupleAndKeywords` は真を返し、それ以外の場合には適切な例外を送出して偽を返します。

.. note::

   キーワード引数を使っている場合、タプルは入れ子にして使えません! *kwlist* 内に存在しないキーワードパラメタが渡された場合、
   :exc:`TypeError` の送出を引き起こします。

.. index:: single: Philbrick, Geoff

以下にキーワードを使ったモジュール例を示します。これは Geoff Philbrick (philbrick@hks.com) によるプログラム例を
もとにしています。 ::

   #include "Python.h"

   static PyObject *
   keywdarg_parrot(PyObject *self, PyObject *args, PyObject *keywds)
   {
       int voltage;
       char *state = "a stiff";
       char *action = "voom";
       char *type = "Norwegian Blue";

       static char *kwlist[] = {"voltage", "state", "action", "type", NULL};

       if (!PyArg_ParseTupleAndKeywords(args, keywds, "i|sss", kwlist,
                                        &voltage, &state, &action, &type))
           return NULL;

       printf("-- This parrot wouldn't %s if you put %i Volts through it.\n",
              action, voltage);
       printf("-- Lovely plumage, the %s -- It's %s!\n", type, state);

       Py_INCREF(Py_None);

       return Py_None;
   }

   static PyMethodDef keywdarg_methods[] = {
       / * PyCFunction の値は PyObject* パラメタを二つだけしか引数に
        * 取らないが、 keywordarg_parrot() は三つとるので、キャストが
        * 必要。
        */
       {"parrot", (PyCFunction)keywdarg_parrot, METH_VARARGS | METH_KEYWORDS,
        "Print a lovely skit to standard output."},
       {NULL, NULL, 0, NULL}   /* センティネル値 */
   };

::

   void
   initkeywdarg(void)
   {
     /* モジュールを作成して関数を追加する */
     Py_InitModule("keywdarg", keywdarg_methods);
   }


.. _buildvalue:

任意の値を構築する
==================

:c:func:`Py_BuildValue` は :c:func:`PyArg_ParseTuple` の
対極に位置するものです。この関数は以下のように定義されています::

   PyObject *Py_BuildValue(char *format, ...);

:c:func:`Py_BuildValue` は、 :c:func:`PyArg_ParseTuple`
の認識する一連の書式化単位に似た書式化単位を認識します。ただし (関数への出力ではなく、入力に使われる) 引数はポインタではなく、
ただの値でなければなりません。 Python から呼び出された C 関数が返す値として適切な、新たな Python  オブジェクトを返します。

:c:func:`PyArg_ParseTuple` とは一つ違う点があります:  :c:func:`PyArg_ParseTuple`
は第一引数をタプルにする必要があります (Python の引数リストは内部的には常にタプルとして表現されるからです)
が、 :c:func:`Py_BuildValue` はタプルを生成するとは限りません。 :c:func:`Py_BuildValue`
は書式化文字列中に書式化単位が二つかそれ以上入っている場合にのみタプルを構築します。書式化文字列が空なら、 ``None`` を返します。きっかり一つの
書式化単位なら、その書式化単位が記述している何らかのオブジェクトになります。サイズが 0 や 1 のタプル返させたいのなら、書式化文字列を丸括弧で囲います。

以下に例を示します (左に呼び出し例を、右に構築される Python 値を示します)::

   Py_BuildValue("")                        None
   Py_BuildValue("i", 123)                  123
   Py_BuildValue("iii", 123, 456, 789)      (123, 456, 789)
   Py_BuildValue("s", "hello")              'hello'
   Py_BuildValue("ss", "hello", "world")    ('hello', 'world')
   Py_BuildValue("s#", "hello", 4)          'hell'
   Py_BuildValue("()")                      ()
   Py_BuildValue("(i)", 123)                (123,)
   Py_BuildValue("(ii)", 123, 456)          (123, 456)
   Py_BuildValue("(i,i)", 123, 456)         (123, 456)
   Py_BuildValue("[i,i]", 123, 456)         [123, 456]
   Py_BuildValue("{s:i,s:i}",
                 "abc", 123, "def", 456)    {'abc': 123, 'def': 456}
   Py_BuildValue("((ii)(ii)) (ii)",
                 1, 2, 3, 4, 5, 6)          (((1, 2), (3, 4)), (5, 6))


.. _refcounts:

参照カウント法
==============

C や C++のような言語では、プログラマはヒープ上のメモリを動的に確保したり解放したりする責任があります。こうした作業は C
では関数 :c:func:`malloc` や :c:func:`free` で行います。C++では本質的に同じ意味で演算子 ``new`` や
``delete`` が使われます。そこで、以下の議論は C の場合に限定して行います。

:c:func:`malloc` が確保する全てのメモリブロックは、最終的には :c:func:`free` を厳密に一度だけ呼び出して利用可能メモリのプールに
戻さねばなりません。そこで、適切な時に :c:func:`free` を呼び出すことが重要になります。あるメモリブロックに対して、 :c:func:`free`
を呼ばなかったにもかかわらずそのアドレスを忘却してしまうと、ブロックが占有しているメモリはプログラムが終了するまで再利用できなくなります。
これはメモリリーク(:dfn:`memory leak`) と呼ばれています。逆に、プログラムがあるメモリブロックに対して :c:func:`free` を
呼んでおきながら、そのブロックを使い続けようとすると、別の :c:func:`malloc` 呼び出しによって行われるブロックの再利用
と衝突を起こします。これは解放済みメモリの使用 (:dfn:`using freed memory`)
と呼ばれます。これは初期化されていないデータに対する参照と同様のよくない結果 --- コアダンプ、誤った参照、不可解なクラッシュ --- を引き起こします。

よくあるメモリリークの原因はコード中の普通でない処理経路です。例えば、ある関数があるメモリブロックを確保し、何らかの計算を行って、
再度ブロックを解放するとします。さて、関数の要求仕様を変更して、計算に対するテストを追加すると、エラー条件を検出し、関数の途中で
処理を戻すようになるかもしれません。この途中での終了が起きるとき、確保されたメモリブロックは解放し忘れ
やすいのです。コードが後で追加された場合には特にそうです。このようなメモリリークが一旦紛れ込んでしまうと、長い間検出されないままになることがよくあります:
エラーによる関数の終了は、全ての関数呼び出しのに対してほんのわずかな割合しか起きず、その一方でほとんどの近代的な計算機は相当量の仮想記憶を持っているため、
メモリリークが明らかになるのは、長い間動作していたプロセスがリークを起こす関数を何度も使った場合に限られるからです。
従って、この種のエラーを最小限にとどめるようなコーディング規約や戦略を設けて、不慮のメモリリークを避けることが重要なのです。

Python は :c:func:`malloc` や :c:func:`free` を非常によく利用するため、メモリリークの防止に加え、解放されたメモリの使用を
防止する戦略が必要です。このために選ばれたのが参照カウント法 (:dfn:`reference counting`) と呼ばれる手法です。
参照カウント法の原理は簡単です: 全てのオブジェクトにはカウンタがあり、オブジェクトに対する参照がどこかに保存されたら
カウンタをインクリメントし、オブジェクトに対する参照が削除されたらデクリメントします。カウンタがゼロになったら、オブジェクトへの
最後の参照が削除されたことになり、オブジェクトは解放されます。

もう一つの戦略は自動ガベージコレクション  (:dfn:`automatic garbage collection`) と呼ばれています。
(参照カウント法はガベージコレクション戦略の一つとして挙げられることもあるので、二つを区別するために筆者は "自動 (automatic)"
を使っています。) 自動ガベージコレクションの大きな利点は、ユーザが :c:func:`free`  を明示的によばなくてよいことにあります。
(速度やメモリの有効利用性も利点として主張されています --- が、これは確たる事実ではありません。) C
における自動ガベージコレクションの欠点は、真に可搬性のあるガベージコレクタが存在しないということです。それに対し、参照カウント法は可搬性のある実装ができます
(:c:func:`malloc`  や :c:func:`free` を利用できるのが前提です --- C 標準はこれを保証しています)。
いつの日か、十分可搬性のあるガベージコレクタが C で使えるようになるかもしれませんが、それまでは参照カウント法でやっていく以外にはないのです。

Python では、伝統的な参照カウント法の実装を行っている一方で、参照の循環を検出するために働く循環参照検出機構 (cycle detector)
も提供しています。循環参照検出機構のおかげで、直接、間接にかかわらず循環参照の生成を気にせずにアプリケーションを構築できます;
というのも、参照カウント法だけを使ったガベージコレクション実装にとって循環参照は弱点だからです。循環参照は、(間接参照の場合も含めて)
相互への参照が入ったオブジェクトから形成されるため、循環内のオブジェクトは各々非ゼロの参照カウント
を持ちます。典型的な参照カウント法の実装では、たとえ循環参照を形成するオブジェクトに対して他に全く参照がないとしても、
循環参照内のどのオブジェクトに属するメモリも再利用できません。

循環参照検出機構は、ごみとなった循環参照を検出し、Python で実装された後始末関数 (finalizer、 :meth:`__del__` メソッド)
が定義されていないかぎり、それらのメモリを再利用できます。
後始末関数がある場合、検出機構は検出した循環参照を :mod:`gc` モジュールに
(具体的にはこのモジュールの ``garbage`` 変数内)
に公開します。 :mod:`gc` モジュールではまた、検出機構 (:func:`collect` 関数) を実行する方法や設定用の
インタフェース、実行時に検出機構を無効化する機能も公開しています。循環参照検出機構はオプションの機構とみなされています;
デフォルトで入ってはいますが、Unix プラットフォーム (Mac OS X も含みます) ではビルド時に :program:`configure` スクリプトの
:option:`--without-cycle-gc` オプションを使って、他のプラットフォームでは :file:`pyconfig.h`
ヘッダの ``WITH_CYCLE_GC`` 定義をはずして無効にできます。こうして循環参照検出機構を無効化すると、 :mod:`gc` モジュールは
利用できなくなります。


.. _refcountsinpython:

Python における参照カウント法
-----------------------------

Python には、参照カウントのインクリメントやデクリメントを処理する二つのマクロ、 ``Py_INCREF(x)`` と ``Py_DECREF(x)``
があります。 :c:func:`Py_DECREF` は、参照カウントがゼロに到達した際に、オブジェクトのメモリ解放も行います。
柔軟性を持たせるために、 :c:func:`free` を直接呼び出しません ---  その代わりにオブジェクトの型オブジェクト (:dfn:`type
object`) を介します。このために (他の目的もありますが)、全てのオブジェクトには自身の型オブジェクトに対するポインタが入っています。

さて、まだ重大な疑問が残っています: いつ ``Py_INCREF(x)`` や ``Py_DECREF(x)`` を使えばよいのでしょうか?
まず、いくつかの用語説明から始めさせてください。まず、オブジェクトは "占有 (own)" されることはありません;
しかし、あるオブジェクトに対する参照の所有 :dfn:`own a reference`  はできます。オブジェクトの参照カウントは、そのオブジェクトが
参照の所有を受けている回数と定義されています。参照の所有者は、参照が必要なくなった際に :c:func:`Py_DECREF`
を呼び出す役割を担います。参照の所有権は委譲 (transfer) できます。所有参照 (owned reference) の放棄には、渡す、保存する、
:c:func:`Py_DECREF` を呼び出す、という三つの方法があります。所有参照を処理し忘れると、メモリリークを引き起こします。

オブジェクトに対する参照は、借用 (:dfn:`borrow`) も可能です。  [#]_ 参照の借用者は、 :c:func:`Py_DECREF`
を呼んではなりません。借用者は、参照の所有者から借用した期間を超えて参照を保持し続けてはなりません。所有者が参照を放棄した後で借用参照を使うと、
解放済みメモリを使用してしまう危険があるので、絶対に避けねばなりません。  [#]_

参照の借用が参照の所有よりも優れている点は、コードがとりうるあらゆる処理経路で参照を廃棄しておくよう注意しなくて済むことです ---
別の言い方をすれば、借用参照の場合には、処理の途中で関数を終了してもメモリリークの危険を冒すことがない、ということです。
逆に、所有よりも不利な点は、ごくまともに見えるコードが、実際には参照の借用元で放棄されてしまった後に
その参照を使うかもしれないような微妙な状況があるということです。

:c:func:`Py_INCREF` を呼び出すと、借用参照を所有参照  に変更できます。この操作は参照の借用元の状態には影響しません ---
:c:func:`Py_INCREF` は新たな所有参照を生成し、参照の所有者が担うべき全ての責任を課します (つまり、新たな参照の所有者は、以前の
所有者と同様、参照の放棄を適切に行わねばなりません)。


.. _ownershiprules:

所有権にまつわる規則
--------------------

オブジェクトへの参照を関数の内外に渡す場合には、オブジェクトの所有権が参照と共に渡されるか否かが常に関数インタフェース仕様の一部となります。

オブジェクトへの参照を返すほとんどの関数は、参照とともに所有権も渡します。特に、 :c:func:`PyInt_FromLong` や
:c:func:`Py_BuildValue` のように、新しいオブジェクトを生成する関数は全て所有権を相手に渡します。オブジェクトが実際には新たな
オブジェクトでなくても、そのオブジェクトに対する新たな参照の所有権を得ます。例えば、 :c:func:`PyInt_FromLong`
はよく使う値をキャッシュしており、キャッシュされた値への参照を返すことがあります。

:c:func:`PyObject_GetAttrString` のように、あるオブジェクトから別のオブジェクトを抽出するような関数もまた、参照とともに所有権を
委譲します。こちらの方はやや理解しにくいかもしれません。というのはよく使われるルーチンのいくつかが例外となっているからです:
:c:func:`PyTuple_GetItem` 、 :c:func:`PyList_GetItem` 、 :c:func:`PyDict_GetItem` 、および
:c:func:`PyDict_GetItemString` は全て、タプル、リスト、または辞書から借用参照を返します。

:c:func:`PyImport_AddModule` は、実際にはオブジェクトを生成して返すことがあるにもかかわらず、借用参照を返します:
これが可能なのは、生成されたオブジェクトに対する所有参照は ``sys.modules`` に保持されるからです。

オブジェクトへの参照を別の関数に渡す場合、一般的には、関数側は呼び出し手から参照を借用します --- 参照を保存する必要があるなら、
関数側は :c:func:`Py_INCREF` を呼び出して独立した所有者になります。とはいえ、この規則には二つの重要な例外:
:c:func:`PyTuple_SetItem` と :c:func:`PyList_SetItem` があります。これらの関数は、渡された引数要素に対して所有権を
乗っ取り (take over) ます --- たとえ失敗してもです! (:c:func:`PyDict_SetItem` とその仲間は所有権を乗っ取りません
--- これらはいわば "普通の" 関数です。)

Python から C 関数が呼び出される際には、C 関数は呼び出し側から引数への参照を借用します。C 関数の呼び出し側はオブジェクトへの参照を
所有しているので、借用参照の生存期間が保証されるのは関数が処理を返すまでです。このようにして借用参照を保存したり他に渡したりしたい
場合にのみ、 :c:func:`Py_INCREF` を使って所有参照にする必要があります。

Python から呼び出された C 関数が返す参照は所有参照でなければなりません --- 所有権は関数から呼び出し側へと委譲されます。


.. _thinice:

薄氷
----

数少ない状況において、一見無害に見える借用参照の利用が問題をひきおこすことがあります。この問題はすべて、インタプリタが非明示的に呼び出され、
インタプリタが参照の所有者に参照を放棄させてしまう状況と関係しています。

知っておくべきケースのうち最初の、そして最も重要なものは、リスト要素に対する参照を借りている際に起きる、
関係ないオブジェクトに対する :c:func:`Py_DECREF` の使用です。例えば::

   void
   bug(PyObject *list)
   {
       PyObject *item = PyList_GetItem(list, 0);

       PyList_SetItem(list, 1, PyInt_FromLong(0L));
       PyObject_Print(item, stdout, 0); /* BUG! */
   }

上の関数はまず、 ``list[0]`` への参照を借用し、次に ``list[1]``  を値 ``0`` で置き換え、最後にさきほど借用した参照を出力
しています。何も問題ないように見えますね? でもそうではないのです!

:c:func:`PyList_SetItem` の処理の流れを追跡してみましょう。リストは全ての要素に対して参照を所有しているので、要素 1 を
置き換えると、以前の要素 1 を放棄します。ここで、以前の要素 1  がユーザ定義クラスのインスタンスであり、さらにこのクラスが :meth:`__del__`
メソッドを定義していると仮定しましょう。このクラスインスタンスの参照カウントが 1 だった場合、リストが参照を放棄すると、インスタンスの
:meth:`__del__` メソッドが呼び出されます。

クラスは Python で書かれているので、 :meth:`__del__` は任意の Python コードを実行できます。この :meth:`__del__`
が :c:func:`bug` における ``item`` に何か不正なことをしているのでしょうか? その通り! :c:func:`buf` に渡したリストが
:meth:`__del__` メソッドから操作できるとすると、 ``del list[0]`` の効果を持つような文を実行できてしまいます。もしこの操作で
``list[0]`` に対する最後の参照が放棄されてしまうと、 ``list[0]`` に関連付けられていたメモリは解放され、結果的に ``item``
は無効な値になってしまいます。

問題の原因が分かれば、解決は簡単です。一時的に参照回数を増やせばよいのです。正しく動作するバージョンは以下のようになります::

   void
   no_bug(PyObject *list)
   {
       PyObject *item = PyList_GetItem(list, 0);

       Py_INCREF(item);
       PyList_SetItem(list, 1, PyInt_FromLong(0L));
       PyObject_Print(item, stdout, 0);
       Py_DECREF(item);
   }

これは実際にあった話です。以前のバージョンの Python には、このバグの一種が潜んでいて、 :meth:`__del__` メソッドが
どうしてうまく動かないのかを調べるために C デバッガで相当時間を費やした人がいました...

二つ目は、借用参照がスレッドに関係しているケースです。通常は、 Python インタプリタにおける複数のスレッドは、
グローバルインタプリタロックがオブジェクト空間全体を保護しているため、互いに邪魔し合うことはありません。とはいえ、ロックは
:c:macro:`Py_BEGIN_ALLOW_THREADS` マクロで一時的に解除したり、 :c:macro:`Py_END_ALLOW_THREADS`
で再獲得したりできます。これらのマクロはブロックの起こる I/O 呼び出しの周囲によく置かれ、 I/O
が完了するまでの間に他のスレッドがプロセッサを利用できるようにします。明らかに、以下の関数は上の例と似た問題をはらんでいます::

   void
   bug(PyObject *list)
   {
       PyObject *item = PyList_GetItem(list, 0);
       Py_BEGIN_ALLOW_THREADS
       ...ブロックが起こる何らかの I/O 呼び出し...
       Py_END_ALLOW_THREADS
       PyObject_Print(item, stdout, 0); /* BUG! */
   }


.. _nullpointers:

NULL ポインタ
-------------

一般論として、オブジェクトへの参照を引数にとる関数はユーザが *NULL* ポインタを渡すとは予想しておらず、渡そうとするとコアダンプになる
(か、あとでコアダンプを引き起こす) ことでしょう。一方、オブジェクトへの参照を返すような関数は一般に、例外の発生を示す場合にのみ *NULL*
を返します。引数に対して *NULL* テストを行わない理由は、こうした関数群はしばしば受け取った関数を他の関数へと引き渡すからです --- 各々の関数が
*NULL* テストを行えば、冗長なテストが大量に行われ、コードはより低速に動くことになります。

従って、 *NULL* のテストはオブジェクトの "発生源"、すなわち値が *NULL* になるかもしれないポインタを受け取ったときだけに
しましょう。 :c:func:`malloc` や、例外を送出する可能性のある関数がその例です。

マクロ :c:func:`Py_INCREF` および :c:func:`Py_DECREF` は *NULL* ポインタのチェックを行いません ---
しかし、これらのマクロの変化形である :c:func:`Py_XINCREF` および :c:func:`Py_XDECREF` はチェックを行います。

特定のオブジェクト型について調べるマクロ (``Pytype_Check()``)  は *NULL* ポインタのチェックを行いません --- 繰り返しますが、
様々な異なる型を想定してオブジェクトの型を調べる際には、こうしたマクロを続けて呼び出す必要があるので、個別に *NULL* ポインタの
チェックをすると冗長なテストになってしまうのです。型を調べるマクロには、 *NULL* チェックを行う変化形はありません。

Python から C 関数を呼び出す機構は、 C 関数に渡される引数リスト (例でいうところの ``args``) が決して *NULL* にならないよう
保証しています --- 実際には、常にタプル型になるよう保証しています。  [#]_

*NULL* ポインタを Python ユーザレベルに "逃がし" てしまうと、深刻なエラーを引き起こします。

.. Frank Stajano:
   A pedagogically buggy example, along the lines of the previous listing, would
   be helpful here -- showing in more concrete terms what sort of actions could
   cause the problem. I can't very well imagine it from the description.

.. _cplusplus:

C++での拡張モジュール作成
=========================

C++でも拡張モジュールは作成できます。ただしいくつか制限があります。メインプログラム (Python インタプリタ) は C コンパイラでコンパイルされ
リンクされているので、グローバル変数や静的オブジェクトをコンストラクタで作成できません。メインプログラムが C++ コンパイラでリンクされて
いるならこれは問題ではありません。 Python インタプリタから呼び出される関数 (特にモジュール初期化関数) は、 ``extern "C"``
を使って宣言しなければなりません。また、Python ヘッダファイルを ``extern "C" {...}`` に入れる必要はありません---
シンボル ``__cplusplus`` (最近の C++ コンパイラは全てこのシンボルを定義しています) が定義されているときに ``extern "C"
{...}`` が行われるように、ヘッダファイル内にすでに書かれているからです。


.. _using-capsules:

拡張モジュールに C API を提供する
=================================

.. sectionauthor:: Konrad Hinsen <hinsen@cnrs-orleans.fr>


多くの拡張モジュールは単に Python から使える新たな関数や型を提供するだけですが、時に拡張モジュール内のコードが他の拡張
モジュールでも便利なことがあります。例えば、あるモジュールでは順序概念のないリストのように動作する "コレクション (collection)"
クラスを実装しているかもしれません。ちょうどリストを生成したり操作したりできる C API を備えた標準の Python
リスト型のように、この新たなコレクション型も他の拡張モジュールから直接操作できるようにするには一連の C 関数を持っていなければなりません。

一見するとこれは簡単なこと: 単に関数を (もちろん ``static`` などとは宣言せずに) 書いて、適切なヘッダファイルを提供し、C API
を書けばよいだけ、に思えます。そして実際のところ、全ての拡張モジュールが Python インタプリタに常に静的にリンクされている場合にはうまく動作します。
ところがモジュールが共有ライブラリの場合には、一つのモジュールで定義されているシンボルが他のモジュールから不可視なことがあります。
可視性の詳細はオペレーティングシステムによります; あるシステムは Python インタプリタと全ての拡張モジュール用に単一のグローバルな
名前空間を用意しています (例えば Windows)。別のシステムはモジュールのリンク時に取り込まれるシンボルを明示的に指定する必要があります  (AIX
がその一例です)、また別のシステム (ほとんどの Unix) では、違った戦略を選択肢として提供しています。
そして、たとえシンボルがグローバル変数として可視であっても、呼び出したい関数の入ったモジュールがまだロードされていないことだってあります!

従って、可搬性の点からシンボルの可視性には何ら仮定をしてはならないことになります。つまり拡張モジュール中の全てのシンボルは ``static``
と宣言せねばなりません。例外はモジュールの初期化関数で、これは (:ref:`methodtable` で述べたように) 他の拡張モジュールとの間で
名前が衝突するのを避けるためです。また、他の拡張モジュールからアクセスを *受けるべきではない*  シンボルは別のやり方で公開せねばなりません。

Python はある拡張モジュールの C レベルの情報 (ポインタ) を別のモジュールに渡すための
特殊な機構: Capsule (カプセル)を提供しています。
Capsule はポインタ (:c:type:`void\*`) を記憶する Python のデータ型です。 Capsule は C API
を介してのみ生成したりアクセスしたりできますが、他の Python オブジェクトと同じように受け渡しできます。
とりわけ、Capsule は拡張モジュールの名前空間内にある名前に代入できます。
他の拡張モジュールはこのモジュールを import でき、次に名前を取得し、最後にCapsule
へのポインタを取得します。

拡張モジュールの C API を公開するために、様々な方法で Capsule が使われます。
各関数を1つのオブジェクトに入れたり、全ての C API のポインタ配列を Capsule に入れることができます。
そして、ポインタに対する保存や取得といった様々な作業は、コードを提供している
モジュールとクライアントモジュールとの間では異なる方法で分散できます。

どの方法を選ぶにしても、 Capsule の name を正しく設定することは重要です。
:c:func:`PyCapsule_New` は name 引数 (:c:type:`const char \*`) を取ります。
*NULL* を name に渡すことも許可されていますが、 name を設定することを強く推奨します。
正しく名前を付けられた Capsule はある程度の実行時型安全性を持ちます。
名前を付けられていない Capsule を他の Capsule と区別する現実的な方法はありません。

特に、 C API を公開するための Capsule には次のルールに従った名前を付けるべきです::

    modulename.attributename

:c:func:`PyCapsule_Import` という便利関数は、 Capsule の名前がこのルールに一致しているときにのみ、
簡単に Capsule 経由で公開されている C API をロードすることができます。
この挙動により、 C API のユーザーが、確実に正しい C API を格納している Capsule を
ロードできたことを確かめることができます。

以下の例では、名前を公開するモジュールの作者にほとんどの負荷が掛かりますが、よく使われるライブラリを作る際に適切なアプローチを実演します。
このアプローチでは、全ての C API ポインタ (例中では一つだけですが!) を、 Capsule の値となる :c:type:`void`
ポインタの配列に保存します。拡張モジュールに対応するヘッダファイルは、モジュールの import  と C API
ポインタを取得するよう手配するマクロを提供します; クライアントモジュールは、C API にアクセスする前にこのマクロを呼ぶだけです。

名前を公開する側のモジュールは、 :ref:`extending-simpleexample` 節の :mod:`spam`
モジュールを修正したものです。関数 :func:`spam.system` は C ライブラリ関数 :c:func:`system` を直接呼び出さず、
:c:func:`PySpam_System` を呼び出します。この関数はもちろん、実際には (全てのコマンドに "spam" を付けるといったような)
より込み入った処理を行います。この関数 :c:func:`PySpam_System` はまた、他の拡張モジュールにも公開されます。

関数 :c:func:`PySpam_System` は、他の全ての関数と同様に ``static`` で宣言された通常の C 関数です。 ::

   static int
   PySpam_System(const char *command)
   {
       return system(command);
   }

:c:func:`spam_system` には取るに足らない変更が施されています::

   static PyObject *
   spam_system(PyObject *self, PyObject *args)
   {
       const char *command;
       int sts;

       if (!PyArg_ParseTuple(args, "s", &command))
           return NULL;
       sts = PySpam_System(command);
       return Py_BuildValue("i", sts);
   }

モジュールの先頭にある以下の行 ::

   #include "Python.h"

の直後に、以下の二行::

   #define SPAM_MODULE
   #include "spammodule.h"

を必ず追加してください。

``#define`` は、ファイル :file:`spammodule.h` をインクルードして
いるのが名前を公開する側のモジュールであって、クライアントモジュールではないことをヘッダファイルに教えるために使われます。最後に、モジュールの初期化関数は
C API のポインタ配列を初期化するよう手配しなければなりません::

   PyMODINIT_FUNC
   initspam(void)
   {
       PyObject *m;
       static void *PySpam_API[PySpam_API_pointers];
       PyObject *c_api_object;

       m = Py_InitModule("spam", SpamMethods);
       if (m == NULL)
           return;

       /* C API ポインタ配列を初期化する */
       PySpam_API[PySpam_System_NUM] = (void *)PySpam_System;

       /* API ポインタ配列のアドレスが入った Capsule を生成する */
       c_api_object = PyCapsule_New((void *)PySpam_API, "spam._C_API", NULL);

       if (c_api_object != NULL)
           PyModule_AddObject(m, "_C_API", c_api_object);
   }

``PySpam_API`` が ``static`` と宣言されていることに注意してください;
そうしなければ、 :func:`initspam` が終了したときにポインタアレイは消滅してしまいます!

からくりの大部分はヘッダファイル :file:`spammodule.h` 内にあり、以下のようになっています::

   #ifndef Py_SPAMMODULE_H
   #define Py_SPAMMODULE_H
   #ifdef __cplusplus
   extern "C" {
   #endif

   /* spammodule のヘッダファイル */

   /* C API 関数 */
   #define PySpam_System_NUM 0
   #define PySpam_System_RETURN int
   #define PySpam_System_PROTO (const char *command)

   /* C API ポインタの総数 */
   #define PySpam_API_pointers 1


   #ifdef SPAM_MODULE
   /* この部分は spammodule.c をコンパイルする際に使われる */

   static PySpam_System_RETURN PySpam_System PySpam_System_PROTO;

   #else
   /* この部分は spammodule の API を使うモジュール側で使われる */

   static void **PySpam_API;

   #define PySpam_System \
    (*(PySpam_System_RETURN (*)PySpam_System_PROTO) PySpam_API[PySpam_System_NUM])

   /* エラーによる例外の場合には -1 を、成功すると 0 を返す
    * エラーがあれば PyCapsule_Import が例外を設定する。
    */
   static int
   import_spam(void)
   {
       PySpam_API = (void **)PyCapsule_Import("spam._C_API", 0);
       return (PySpam_API != NULL) ? 0 : -1;
   }

   #endif

   #ifdef __cplusplus
   }
   #endif

   #endif /* !defined(Py_SPAMMODULE_H) */

:c:func:`PySpam_System` へのアクセス手段を得るためにクライアントモジュール側がしなければならないことは、初期化関数内
での :c:func:`import_spam` 関数 (またはマクロ) の呼び出しです::

   PyMODINIT_FUNC
   initclient(void)
   {
       PyObject *m;

       m = Py_InitModule("client", ClientMethods);
       if (m == NULL)
           return;
       if (import_spam() < 0)
           return;
       /* さらなる初期化処理はここに置ける */
   }

このアプローチの主要な欠点は、 :file:`spammodule.h` がやや難解になるということです。とはいえ、各関数の基本的な構成は公開される
ものと同じなので、書き方を一度だけ学べばすみます。

最後に、Capsule は、自身に保存されているポインタをメモリ確保したり解放したりする際に特に便利な、もう一つの機能を提供しているという
ことに触れておかねばなりません。詳細は Python/C API リファレンスマニュアルの
:ref:`capsules`, および Capsule の実装部分 (Python
ソースコード配布物中のファイル  :file:`Include/pycapsule.h` および :file:`Objects/pycapsule.c`
に述べられています。

.. rubric:: 注記

.. [#] この関数へのインタフェースはすでに標準モジュール :mod:`os` にあります --- この関数を選んだのは、単純で直接的な例を示したいからです。

.. [#] 参照を "借用する" というメタファは厳密には正しくありません: なぜなら、参照の所有者は依然として参照のコピーを持っているからです。

.. [#] 参照カウントが 1 以上かどうか調べる方法は **うまくいきません** --- 参照カウント自体も解放されたメモリ上に
   あるため、その領域が他のオブジェクトに使われている可能性があります!

.. [#] "旧式の" 呼び出し規約を使っている場合には、この保証は適用されません --- 既存のコードにはいまだに旧式の呼び出し規約が多々あります

