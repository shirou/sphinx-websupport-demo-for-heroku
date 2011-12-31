.. highlightlang:: c


.. _api-intro:

********
はじめに
********

Python のアプリケーションプログラマ用インタフェース (Application Programmer's
Interface, API) は、 Python インタプリタに対する様々なレベルでのアクセス手段を
C や C++ のプログラマに提供しています。
この API は通常 C++ からも全く同じように利用できるのですが、簡潔な呼び名に
するために Python/C API と名づけられています。根本的に異なる二つの目的から、
Python/C API が用いられます。第一は、特定用途の *拡張モジュール (extention
module)* 、すなわち Python インタプリタを拡張する C で書かれたモジュール
を記述する、という目的です。第二は、より大規模なアプリケーション内で Python
を構成要素 (component) として利用するという目的です; このテクニックは、
一般的にはアプリケーションへの Python の埋め込み (:dfn:`embedding`) と呼びます。
拡張モジュールの作成は比較的わかりやすいプロセスで、 "手引書 (cookbook)"
的なアプローチでうまく実現できます。作業をある程度まで自動化してくれる
ツールもいくつかあります。一方、他のアプリケーションへの Python の
埋め込みは、Python ができてから早い時期から行われてきましたが、
拡張モジュールの作成に比べるとやや難解です。

多くの API 関数は、Python の埋め込みであるか拡張であるかに関わらず
役立ちます; とはいえ、 Python を埋め込んでいるほとんどのアプリケーション
は、同時に自作の拡張モジュールも提供する必要が生じることになる
でしょうから、Python を実際にアプリケーションに埋め込んでみる前に
拡張モジュールの書き方に詳しくなっておくのはよい考えだと思います。


.. _api-includes:

インクルードファイル
====================

Python/C API を使うために必要な、関数、型およびマクロの全ての定義
をインクルードするには、以下の行::

   #include "Python.h"

をソースコードに記述します。
この行を記述すると、標準ヘッダ: ``<stdio.h>``, ``<string.h>``, ``<errno.h>``,
``<limits.h>``, ``<assert.h>``,  ``<stdlib.h>``  を (利用できれば) インクルードします。

.. note::

   システムによっては、Python の定義しているプリプロセッサ定義が標準ヘッダに
   影響をおよぼす可能性があるので、 :file:`Python.h` は他の標準ヘッダファイルよりも
   前にインクルードしてください。

Python.h で定義されている、ユーザから見える名前全て (Python.h がインクルード
している標準ヘッダの名前は除きます) には、接頭文字列 ``Py`` または ``_Py``
が付きます。 ``_Py`` で始まる名前は Python 実装で内部使用するための名前で、
拡張モジュールの作者は使ってはなりません。構造体のメンバには予約済みの
接頭文字列はありません。

**重要:** API のユーザは、 ``Py`` や ``_Py`` で始まる名前を定義するような
コードを絶対に書いてはなりません。後からコードを読む人を混乱させたり、
将来の Python のバージョンで同じ名前が定義されて、ユーザの書いたコードの
可搬性を危うくする可能性があります。

ヘッダファイル群は通常 Python と共にインストールされます。 Unixでは
:file:`{prefix}/include/pythonversion/` および :file:`{exec_prefix}/include/pythonversion/` に
置かれます。 :envvar:`prefix` と :envvar:`exec_prefix` は Python をビルドする際の
:program:`configure` スクリプトに与えたパラメタに対応し、 *version* は
``sys.version[:3]`` に対応します。 Windows では、ヘッダは :file:`{prefix}/include`
に置かれます。 :envvar:`prefix` はインストーラに指定したインストールディレクトリです。

ヘッダをインクルードするには、各ヘッダの入ったディレクトリ (別々の
ディレクトリの場合は両方) を、コンパイラがインクルードファイルを
検索するためのパスに入れます。親ディレクトリをサーチパスに入れて、
``#include <pythonX.Y/Python.h>`` のようにしては *なりません* ;
:envvar:`prefix` 内のプラットフォームに依存しないヘッダは、
:envvar:`exec_prefix` からプラットフォーム依存のヘッダをインクルード
しているので、このような操作を行うと複数のプラットフォームでのビルドが
できなくなります。

API はすべて C 言語を使って定義していますが、ヘッダファイルはエントリ
ポイントを ``extern "C"`` で適切に宣言しているので、 C++ ユーザは、
なんの問題もなく C++から API を利用できることに気づくはずです。


.. _api-objects:

オブジェクト、型および参照カウント
==================================

.. index:: object: type

Python/C API 関数は、 :c:type:`PyObject\*` 型の一つ以上の引数と戻り値を持ちます。
この型は、任意の Python オブジェクトを表現する不透明 (opaque) なデータ型へのポインタです。
Python 言語は、全ての Python オブジェクト型をほとんどの状況 (例えば代入、スコープ規則
(scope rule)、引数渡し) で同様に扱います。ほとんど全ての Python オブジェクトはヒープ
(heap) 上に置かれます: このため、 :c:type:`PyObject` 型のオブジェクトは、
自動記憶 (automatic) としても静的記憶 (static) としても宣言できません。
:c:type:`PyObject\*` 型のポインタ変数のみ宣言できます。唯一の例外は、型オブジェクト
です; 型オブジェクトはメモリ解放 (deallocate) してはならないので、
通常は静的記憶の :c:type:`PyTypeObject` オブジェクトにします。

全ての Python オブジェクトには (Python 整数型ですら) 型 (:dfn:`type`)  と参照カウント
(:dfn:`reference count`) があります。
あるオブジェクトの型は、そのオブジェクトがどの種類のオブジェクトか
(例えば整数、リスト、ユーザ定義関数、など; その他多数については :ref:`types` で説明しています)
を決定します。よく知られている型については、各々マクロが存在して、
あるオブジェクトがその型かどうか調べられます; 例えば、 ``PyList_Check(a)`` は、
*a* で示されたオブジェクトが Python リスト型のとき (かつそのときに限り) 真値を返します。

.. _api-refcounts:

参照カウント
------------

今日の計算機は有限の (しばしば非常に限られた) メモリサイズしか持たないので、参照カウントは重要な概念です; 参照カウントは、
あるオブジェクトに対して参照を行っている場所が何箇所あるかを数える値です。参照を行っている場所とは、別のオブジェクトであったり、グローバルな
(あるいは静的な) C 変数であったり、何らかの C 関数内にあるローカルな変数だったりします。
あるオブジェクトの参照カウントがゼロになると、そのオブジェクトは解放されます。そのオブジェクトに他のオブジェクトへの
参照が入っていれば、他のオブジェクトの参照カウントはデクリメントされます。デクリメントの結果、他のオブジェクトの参照カウント
がゼロになると、今度はそのオブジェクトが解放される、といった具合に以後続きます。(言うまでもなく、互いを参照しあうオブジェクトについて問題があります;
現状では、解決策は "何もしない" です。)

.. index::
   single: Py_INCREF()
   single: Py_DECREF()

参照カウントは、常に明示的なやり方で操作されます。通常の方法では、 :c:func:`Py_INCREF`  でオブジェクトの参照を 1 インクリメントし、
:c:func:`Py_DECREF` で 1 デクリメントします。 :c:func:`Py_DECREF` マクロは、incref よりもかなり
複雑です。というのは、 :c:func:`Py_DECREF` マクロは参照カウントがゼロになったかどうかを調べて、なった場合にはオブジェクトのデアロケータ
(deallocator) を呼び出さなければならないからです。デアロケータとは、オブジェクトの型を定義している構造体内にある関数へのポインタです。
型固有のデアロケータは、その型が複合オブジェクト (compound object) 型である場合には、オブジェクト内の他のオブジェクトに対する参照
カウントをデクリメントするよう気を配るとともに、その他の必要なファイナライズ (finalize) 処理を実行します。
参照カウントがオーバフローすることはありません; というのも、仮想メモリ空間には、(``sizeof(Py_ssize_t) >= sizeof(char*)`` と
仮定した場合) 少なくとも参照カウントの記憶に使われるビット数と同じだけのメモリ上の位置があるからです。従って、参照カウントの
インクリメントは単純な操作になります。

オブジェクトへのポインタが入っているローカルな変数全てについて、オブジェクトの参照カウントを必ずインクリメントしなければならない
わけではありません。理論上は、オブジェクトの参照カウントは、オブジェクトを指し示す変数が生成されたときに 1 増やされ、その変数がスコープから出て行った際に
1 減らされます。しかしこの場合、二つの操作は互いに相殺するので、結果的に参照カウントは変化しません。参照カウントを使う真の意義とは、手持ちの何らかの
変数がオブジェクトを指している間はオブジェクトがデアロケートされないようにすることにあります。オブジェクトに対して、
一つでも別の参照が行われていて、その参照が手持ちの変数と同じ間維持されるのなら、参照カウントを一時的に増やす必要は
ありません。参照カウント操作の必要性が浮き彫りになる重要な局面とは、Python から呼び出された拡張モジュール内の C 関数に
オブジェクトを引数として渡すときです; 呼び出しメカニズムは、呼び出しの間全ての引数に対する参照を保証します。

しかしながら、よく陥る過ちとして、あるオブジェクトをリストから得たときに、参照カウントをインクリメントせずにしばらく放っておく
というのがあります。他の操作がオブジェクトをリストから除去してしまい、参照カウントがデクリメントされてデアロケートされてしまうことが考えられます。
本当に危険なのは、まったく無害そうにみえる操作が、上記の動作を引き起こす何らかの Python コードを呼び出しかねないということです;
:c:func:`Py_DECREF` からユーザへ制御を戻せるようなコードパスが存在するため、ほとんど全ての操作が潜在的に危険をはらむことになります。

安全に参照カウントを操作するアプローチは、汎用の操作 (関数名が  ``PyObject_``, ``PyNumber_``, ``PySequence_``,
および  ``PyMapping_`` で始まる関数) の利用です。これらの操作は常に戻り値となるオブジェクトの参照カウントをインクリメントします。
ユーザには戻り値が不要になったら :c:func:`Py_DECREF` を呼ぶ責任が残されています; とはいえ、すぐにその習慣は身に付くでしょう。


.. _api-refcountdetails:

参照カウントの詳細
^^^^^^^^^^^^^^^^^^

Python/C API の各関数における参照カウントの振る舞いは、説明するには、 *参照の所有権 (ownership of references)*
という言葉でうまく説明できます。所有権は参照に対するもので、オブジェクトに対するものではありません (オブジェクトは
誰にも所有されず、常に共有されています)。ある参照の "所有" は、その参照が必要なくなった時点で :c:func:`Py_DECREF`
を呼び出す役割を担うことを意味します。所有権は委譲でき、あるコードが委譲によって所有権を得ると、今度はそのコードが参照が必要なくなった際に最終的に
:c:func:`Py_DECREF` や :c:func:`Py_XDECREF` を呼び出して decref する役割を担います --- あるいは、その役割を
(通常はコードを呼び出した元に) 受け渡します。ある関数が、関数の呼び出し側に対して参照の所有権を渡すと、呼び出し側は *新たな* 参照 (new
reference) を得る、と言います。所有権が渡されない場合、呼び出し側は参照を *借りる* (borrow)
といいます。借りた参照に対しては、何もする必要はありません。

逆に、ある関数呼び出しで、あるオブジェクトへの参照を呼び出される関数に渡す際には、二つの可能性: 関数がオブジェクトへの参照を *盗み取る* (steal)
場合と、そうでない場合があります。

*参照を盗む* とは、関数に参照を渡したときに、参照の所有者がその関数になったと仮定し、関数の呼び出し元には所有権がなくなるということです。

.. index::
   single: PyList_SetItem()
   single: PyTuple_SetItem()

参照を盗み取る関数はほとんどありません; 例外としてよく知られているのは、 :c:func:`PyList_SetItem` と
:c:func:`PyTuple_SetItem` で、これらはシーケンスに入れる要素に対する参照を盗み取ります (しかし、要素の
入る先のタプルやリストの参照は盗み取りません!)。これらの関数は、リストやタプルの中に新たに作成されたオブジェクトを入れていく際の
常套的な書き方をしやすくするために、参照を盗み取るように設計されています; 例えば、 ``(1, 2, "three")`` というタプルを生成するコードは
以下のようになります (とりあえず例外処理のことは忘れておきます; もっとよい書き方を後で示します)::

   PyObject *t;

   t = PyTuple_New(3);
   PyTuple_SetItem(t, 0, PyInt_FromLong(1L));
   PyTuple_SetItem(t, 1, PyInt_FromLong(2L));
   PyTuple_SetItem(t, 2, PyString_FromString("three"));

ここで、 :c:func:`PyInt_FromLong` は新しい参照を返し、すぐに :c:func:`PyTuple_SetItem` に盗まれます。
参照が盗まれた後もそのオブジェクトを利用したい場合は、参照盗む関数を呼び出す前に、 :c:func:`Py_INCREF` を利用してもう一つの参照を取得
してください。

.. % Here, \cfunction{PyInt_FromLong()} returns a new reference which is
.. % immediately stolen by \cfunction{PyTuple_SetItem()}.  When you want to
.. % keep using an object although the reference to it will be stolen,
.. % use \cfunction{Py_INCREF()} to grab another reference before calling the
.. % reference-stealing function.

ちなみに、 :c:func:`PyTuple_SetItem` はタプルに値をセットするための *唯一の* 方法です; タプルは変更不能なデータ型なので、
:c:func:`PySequence_SetItem` や :c:func:`PyObject_SetItem`
を使うと上の操作は拒否されてしまいます。自分でタプルの値を入れていくつもりなら、 :c:func:`PyTuple_SetItem` だけしか使えません。

同じく、リストに値を入れていくコードは :c:func:`PyList_New` と  :c:func:`PyList_SetItem` で書けます。

しかし実際には、タプルやリストを生成して値を入れる際には、上記のような方法はほとんど使いません。
より汎用性のある関数、 :c:func:`Py_BuildValue` があり、ほとんどの主要なオブジェクトをフォーマット文字列 :dfn:`format
string` の指定に基づいて C の値から生成できます。例えば、上の二種類のコードブロックは、以下のように置き換えられます
(エラーチェックにも配慮しています)::

   PyObject *tuple, *list;

   tuple = Py_BuildValue("(iis)", 1, 2, "three");
   list = Py_BuildValue("[iis]", 1, 2, "three");

自作の関数に渡す引数のように、単に参照を借りるだけの要素に対しては、 :c:func:`PyObject_SetItem` とその仲間を
使うのがはるかに一般的です。その場合、参照カウントをインクリメントする必要がなく、参照を引き渡せる ("参照を盗み取らせられる") ので、
参照カウントに関する動作はより健全になります。例えば、以下の関数は与えられた要素をリスト中の全ての要素の値にセットします::

   int
   set_all(PyObject *target, PyObject *item)
   {
       int i, n;

       n = PyObject_Length(target);
       if (n < 0)
           return -1;
       for (i = 0; i < n; i++) {
           PyObject *index = PyInt_FromLong(i);
           if (!index)
               return -1;
           if (PyObject_SetItem(target, index, item) < 0)
               return -1;
           Py_DECREF(index);
       }
       return 0;
   }

.. index:: single: set_all()

関数の戻り値の場合には、状況は少し異なります。ほとんどの関数については、参照を渡してもその参照に対する
所有権が変わることがない一方で、あるオブジェクトに対する参照を返すような多くの関数は、参照に対する所有権を呼び出し側に与えます。理由は簡単です:
多くの場合、関数が返すオブジェクトはその場で (on the fly) 生成されるため、呼び出し側が得る参照は生成された
オブジェクトに対する唯一の参照になるからです。従って、 :c:func:`PyObject_GetItem` や
:c:func:`PySequence_GetItem` のように、オブジェクトに対する参照を返す汎用の関数は、常に新たな参照を返します (呼び出し側
が参照の所有者になります)。

重要なのは、関数が返す参照の所有権を持てるかどうかは、どの関数を呼び出すかだけによる、と理解することです --- 関数呼び出し時の *お飾り*
(関数に引数として渡したオブジェクトの型) は *この問題には関係ありません!* 従って、 :c:func:`PyList_GetItem`
を使ってリスト内の要素を得た場合には、参照の所有者にはなりません --- が、同じ要素を同じリストから
:c:func:`PySequence_GetItem` (図らずもこの関数は全く同じ引数をとります) を使って取り出すと、返されたオブジェクト
に対する参照を得ます。

.. index::
   single: PyList_GetItem()
   single: PySequence_GetItem()

以下は、整数からなるリストに対して各要素の合計を計算する関数をどのようにして書けるかを示した例です; 一つは :c:func:`PyList_GetItem`
を使っていて、もう一つは :c:func:`PySequence_GetItem` を使っています。 ::

   long
   sum_list(PyObject *list)
   {
       int i, n;
       long total = 0;
       PyObject *item;

       n = PyList_Size(list);
       if (n < 0)
           return -1; /* リストではない */
       for (i = 0; i < n; i++) {
           item = PyList_GetItem(list, i); /* 失敗しないはず */
           if (!PyInt_Check(item)) continue; /* 整数でなければ読み飛ばす */
           total += PyInt_AsLong(item);
       }
       return total;
   }

.. index:: single: sum_list()

::

   long
   sum_sequence(PyObject *sequence)
   {
       int i, n;
       long total = 0;
       PyObject *item;
       n = PySequence_Length(sequence);
       if (n < 0)
           return -1; /* 長さの概念がない */
       for (i = 0; i < n; i++) {
           item = PySequence_GetItem(sequence, i);
           if (item == NULL)
               return -1; /* シーケンスでないか、その他の失敗 */
           if (PyInt_Check(item))
               total += PyInt_AsLong(item);
           Py_DECREF(item); /* GetItem で得た所有権を放棄する */
       }
       return total;
   }

.. index:: single: sum_sequence()


.. _api-types:

型
--

Python/C API において重要な役割を持つデータ型は、 :c:type:`PyObject` 型の他にもいくつかあります; ほとんどは
:c:type:`int`, :c:type:`long`,  :c:type:`double`, および :c:type:`char\*` といった、単なる C
のデータ型です。また、モジュールで公開している関数を列挙する際に用いられる静的なテーブルや、新しいオブジェクト型におけるデータ属性を記述したり、
複素数の値を記述したりするために構造体をいくつか使っています。これらの型については、その型を使う関数とともに説明してゆきます。


.. _api-exceptions:

例外
====

Python プログラマは、特定のエラー処理が必要なときだけしか例外を扱う必要はありません; 処理しなかった例外は、処理の呼び出し側、そのまた
呼び出し側、といった具合に、トップレベルのインタプリタ層まで自動的に伝播します。インタプリタ層は、スタックトレースバックと合わせて例外をユーザに報告します。

.. index:: single: PyErr_Occurred()

ところが、 C プログラマの場合、エラーチェックは常に明示的に行わねばなりません。
Python/C API の全ての関数は、関数のドキュメントで明確に説明がない限り
例外を発行する可能性があります。
一般的な話として、ある関数が何らかのエラーに遭遇すると、関数は例外を設定して、
関数内における参照の所有権を全て放棄し、エラー値(error indicator)を返します。
ドキュメントに書かれてない場合、このエラー値は関数の戻り値の型にによって、
*NULL* か ``-1`` のどちらかになります。
いくつかの関数ではブール型で真/偽を返し、偽はエラーを示します。
きわめて少数の関数では明確なエラー指標を返さなかったり、
あいまいな戻り値を返したりするので、 :c:func:`PyErr_Occurred` で明示的に
エラーテストを行う必要があります。
これらの例外は常に明示的にドキュメント化されます。

.. index::
   single: PyErr_SetString()
   single: PyErr_Clear()

例外時の状態情報 (exception state)は、スレッド単位に用意された記憶領域 (per-thread storage) 内で管理されます
(この記憶領域は、スレッドを使わないアプリケーションではグローバルな記憶領域と同じです)。一つのスレッドは二つの状態のどちらか:
例外が発生したか、まだ発生していないか、をとります。関数 :c:func:`PyErr_Occurred` を使うと、この状態を調べられます:
この関数は例外が発生した際にはその例外型オブジェクトに対する借用参照 (borrowed reference) を返し、そうでないときには *NULL*
を返します。例外状態を設定する関数は数多くあります: :c:func:`PyErr_SetString` はもっともよく知られている
(が、もっとも汎用性のない) 例外を設定するための関数で、 :c:func:`PyErr_Clear` は例外状態情報を消し去る関数です。

.. index::
   single: exc_type (in module sys)
   single: exc_value (in module sys)
   single: exc_traceback (in module sys)

完全な例外状態情報は、3 つのオブジェクト: 例外の型、例外の値、そしてトレースバック、からなります  (どのオブジェクトも
*NULL* を取り得ます)。これらの情報は、 Python オブジェクトの   ``sys.exc_type``, ``sys.exc_value``, および
``sys.exc_traceback`` と同じ意味を持ちます; とはいえ、 C と Python の例外状態情報は全く同じではありません: Python
における例外オブジェクトは、Python の :keyword:`try` ...  :keyword:`except`
文で最近処理したオブジェクトを表す一方、 C レベルの例外状態情報が存続するのは、渡された例外情報を
``sys.exc_type`` その他に転送するよう取り計らう Python のバイトコードインタプリタのメインループに到達するまで、
例外が関数の間で受け渡しされている間だけです。

.. index:: single: exc_info() (in module sys)

Python 1.5 からは、Python で書かれたコードから例外状態情報にアクセスする方法として、推奨されていてスレッドセーフな方法は
:func:`sys.exc_info` になっているので注意してください。この関数は Python コードの実行されているスレッドにおける
例外状態情報を返します。また、これらの例外状態情報に対するアクセス手段は、両方とも意味づけ (semantics) が変更され、ある関数が例外を捕捉すると、
その関数を実行しているスレッドの例外状態情報を保存して、呼び出し側の呼び出し側の例外状態情報を維持するようになりました。
この変更によって、無害そうに見える関数が現在扱っている例外を上書きすることで引き起こされる、例外処理コードでよくおきていたバグを抑止しています;
また、トレースバック内のスタックフレームで参照されているオブジェクトがしばしば不必要に寿命を永らえていたのをなくしています。

一般的な原理として、ある関数が別の関数を呼び出して何らかの作業をさせるとき、呼び出し先の関数が例外を送出していないか調べなくては
ならず、もし送出していれば、その例外状態情報は呼び出し側に渡されなければなりません。呼び出し元の関数はオブジェクト参照の所有権をすべて放棄し、
エラー指標を返さなくてはなりませんが、余計に例外を設定する必要は *ありません* --- そんなことをすれば、たった今
送出されたばかりの例外を上書きしてしまい、エラーの原因そのものに関する重要な情報を失うことになります。

.. index:: single: sum_sequence()

例外を検出して渡す例は、上の :c:func:`sum_sequence` で示しています。偶然にも、この例ではエラーを検出した際に何ら参照を放棄する必要が
ありません。以下の関数の例では、エラーに対する後始末について示しています。まず、どうして Python で書くのが好きか思い出してもらうために、等価な
Python コードを示します::

   def incr_item(dict, key):
       try:
           item = dict[key]
       except KeyError:
           item = 0
       dict[key] = item + 1

.. index:: single: incr_item()

以下は対応するコードを C で完璧に書いたものです::

   int
   incr_item(PyObject *dict, PyObject *key)
   {
       /* Py_XDECREF 用に全てのオブジェクトを NULL で初期化 */
       PyObject *item = NULL, *const_one = NULL, *incremented_item = NULL;
       int rv = -1; /* 戻り値の初期値を -1 (失敗) に設定しておく */

       item = PyObject_GetItem(dict, key);
       if (item == NULL) {
           /* KeyError だけを処理: */
           if (!PyErr_ExceptionMatches(PyExc_KeyError))
               goto error;

           /* エラーを無かったことに (clear) してゼロを使う: */
           PyErr_Clear();
           item = PyInt_FromLong(0L);
           if (item == NULL)
               goto error;
       }
       const_one = PyInt_FromLong(1L);
       if (const_one == NULL)
           goto error;

       incremented_item = PyNumber_Add(item, const_one);
       if (incremented_item == NULL)
           goto error;

       if (PyObject_SetItem(dict, key, incremented_item) < 0)
           goto error;
       rv = 0; /* うまくいった場合 */
       /* 後始末コードに続く */

    error:
       /* 成功しても失敗しても使われる後始末コード */

       /* NULL を参照している場合は無視するために Py_XDECREF() を使う */
       Py_XDECREF(item);
       Py_XDECREF(const_one);
       Py_XDECREF(incremented_item);

       return rv; /* エラーなら -1 、成功なら 0 */
   }

.. index:: single: incr_item()

.. index::
   single: PyErr_ExceptionMatches()
   single: PyErr_Clear()
   single: Py_XDECREF()

なんとこの例は C で ``goto`` 文を使うお勧めの方法まで示していますね! この例では、特定の例外を処理するために
:c:func:`PyErr_ExceptionMatches`  および :c:func:`PyErr_Clear` をどう使うかを
示しています。また、所有権を持っている参照で、値が *NULL* になるかもしれないものを捨てるために  :c:func:`Py_XDECREF`
をどう使うかも示しています (関数名に ``'X'`` が付いていることに注意してください; :c:func:`Py_DECREF` は *NULL*
参照に出くわすとクラッシュします)。正しく動作させるためには、所有権を持つ参照を保持するための変数を *NULL* で初期化することが重要です; 同様に、
あらかじめ戻り値を定義する際には値を ``-1`` (失敗) で初期化しておいて、最後の関数呼び出しまでうまくいった場合にのみ ``0`` (成功)
に設定します。


.. _api-embedding:

Python の埋め込み
=================

Python インタプリタの埋め込みを行う人 (いわば拡張モジュールの書き手の対極) が気にかけなければならない重要なタスクは、 Python
インタプリタの初期化処理 (initialization)、そしておそらくは終了処理 (finalization) です。インタプリタのほとんどの機能は、
インタプリタの起動後しか使えません。

.. index::
   single: Py_Initialize()
   module: __builtin__
   module: __main__
   module: sys
   module: exceptions
   triple: module; search; path
   single: path (in module sys)

基本的な初期化処理を行う関数は :c:func:`Py_Initialize` です。この関数はロード済みのモジュールからなるテーブルを作成し、
土台となるモジュール :mod:`__builtin__`, :mod:`__main__`, :mod:`sys`, および
:mod:`exceptions` を作成します。また、モジュール検索パス (``sys.path``)    の初期化も行います。

.. index:: single: PySys_SetArgvEx()

:c:func:`Py_Initialize` の中では、 "スクリプトへの引数リスト" (script argument list,
``sys.argv`` のこと) を設定しません。
この変数が後に実行される Python コード中で必要なら、 :c:func:`Py_Initialize` の後で
``PySys_SetArgvEx(argc, argv, updatepath)`` を呼び出して明示的に設定しなければなりません。

ほとんどのシステムでは (特に Unix と Windows は、詳細がわずかに異なりはしますが)、 :c:func:`Py_Initialize` は標準の
Python インタプリタ実行形式の場所に対する推定結果に基づいて、 Python のライブラリが Python インタプリタ実行形式からの相対パスで
見つかるという仮定の下にモジュール検索パスを計算します。とりわけこの検索では、シェルコマンド検索パス (環境変数 :envvar:`PATH`)
上に見つかった :file:`python` という名前の実行ファイルの置かれているディレクトリの親ディレクトリからの相対で、
:file:`lib/python{X.Y}` という名前のディレクトリを探します。

例えば、 Python 実行形式が :file:`/usr/local/bin/python` で見つかった
とすると、 :c:func:`Py_Initialize` はライブラリが :file:`/usr/local/lib/python{X.Y}`
にあるものと仮定します。 (実際には、このパスは "フォールバック (fallback)" のライブラリ位置でもあり、 :file:`python` が
:envvar:`PATH` 上にない場合に使われます。) ユーザは :envvar:`PYTHONHOME` を設定することでこの動作をオーバライド
したり、 :envvar:`PYTHONPATH` を設定して追加のディレクトリを標準モジュール検索パスの前に挿入したりできます。

.. index::
   single: Py_SetProgramName()
   single: Py_GetPath()
   single: Py_GetPrefix()
   single: Py_GetExecPrefix()
   single: Py_GetProgramFullPath()

埋め込みを行うアプリケーションでは、 :c:func:`Py_Initialize` を呼び出す *前に*
``Py_SetProgramName(file)``  を呼び出すことで、上記の検索を操作できます。この埋め込みアプリケーションでの設定は依然として
:envvar:`PYTHONHOME`  でオーバライドでき、標準のモジュール検索パスの前には以前として :envvar:`PYTHONPATH`
が挿入されるので注意してください。アプリケーションでモジュール検索パスを完全に制御したいのなら、独自に :c:func:`Py_GetPath`,
:c:func:`Py_GetPrefix`, :c:func:`Py_GetExecPrefix`,  および
:c:func:`Py_GetProgramFullPath`  の実装を提供しなければなりません (これらは全て
:file:`Modules/getpath.c` で定義されています)。

.. index:: single: Py_IsInitialized()

たまに、 Python を "初期化しない" ようにしたいことがあります。例えば、あるアプリケーションでは実行を最初からやりなおし (start over)
させる (:c:func:`Py_Initialize` をもう一度呼び出させる) ようにしたいかもしれません。あるいは、アプリケーションが Python
を一旦使い終えて、Python が確保したメモリを解放できるようにしたいかもしれません。 :c:func:`Py_Finalize` を使うと、こうした処理を
実現できます。また、関数 :c:func:`Py_IsInitialized`  は、Python が現在初期化済みの状態にある場合に真を返します。
これらの関数についてのさらなる情報は、後の章で説明します。 :c:func:`Py_Finalize` がPythonインタプリタに確保された全てのメモリを
*開放するわけではない* ことに注意してください。例えば、拡張モジュールによって確保されたメモリは、現在のところ開放する事ができません。


.. _api-debugging:

デバッグ版ビルド (Debugging Builds)
===================================

インタプリタと拡張モジュールに対しての追加チェックをするためのいくつかのマクロを有効にしてPythonをビルドすることができます。
これらのチェックは、実行時に大きなオーバーヘッドを生じる傾向があります。なので、デフォルトでは有効にされていません。

Pythonデバッグ版ビルドの全ての種類のリストが、Pythonソース配布(source distribution)の中の
:file:`Misc/SpecialBuilds.txt` にあります。参照カウントのトレース、メモリアロケータのデバッグ、インタプリタのメインループの
低レベルプロファイリングが利用可能です。よく使われるビルドについてのみ、この節の残りの部分で説明します。

インタプリタを :c:macro:`Py_DEBUG` マクロを有効にしてコンパイルすると、一般的に「デバッグビルド」といわれるPythonができます。
Unix では、 :file:`configure` コマンドに :option:`--with-pydebug` を追加することで、
:c:macro:`Py_DEBUG` が有効になります。その場合、暗黙的にPython専用ではない :c:macro:`_DEBUG` も有効になります。
Unix ビルドでは、 :c:macro:`Py_DEBUG` が有効な場合、コンパイラの最適化が無効になります。

あとで説明する参照カウントデバッグの他に、以下の追加チェックも有効になります。

* object allocator に対する追加チェック

* パーサーとコンパイラに対する追加チェック

* 情報損失のために、大きい型から小さい型へのダウンキャストに対するチェック

* 辞書(dict)と集合(set)の実装に対する、いくつもの assertion の追加。加えて、集合オブジェクトに :meth:`test_c_api`
  メソッドが追加されます。

* フレームを作成する時の、引数の健全性チェック。

* 初期化されていない数に対する参照を検出するために、長整数のストレージが特定の妥当でないパターンで初期化されます。

* 低レベルトレースと追加例外チェックがVM runtimeに追加されます。

* メモリアリーナ(memory arena)の実装に対する追加チェック

* threadモジュールに対する追加デバッグ機能.

ここで言及されていない追加チェックもあるでしょう。

:c:macro:`Py_TRACE_REFS` を宣言すると、参照トレースが有効になります。全ての :c:type:`PyObject`
に二つのフィールドを追加することで、使用中のオブジェクトの循環二重連結リストが管理されます。全ての割り当て(allocation)がトレースされます。
終了時に、全ての残っているオブジェクトが表示されます。 (インタラクティブモードでは、インタプリタによる文の実行のたびに表示されます)
:c:macro:`Py_TRACE_REFS` は :c:macro:`Py_DEBUG` によって暗黙的に有効になります。

より詳しい情報については、Pythonのソース配布(source distribution)の中の :file:`Misc/SpecialBuilds.txt`
を参照してください。

