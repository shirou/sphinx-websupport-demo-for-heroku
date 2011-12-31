.. highlightlang:: c

.. _common-structs:

共通のオブジェクト構造体 (common object structure)
==================================================

Python では、オブジェクト型を定義する上で数多くの構造体が使われます。この節では三つの構造体とその利用方法について説明します。

全ての Python オブジェクトは、オブジェクトのメモリ内表現の先頭部分にある少数のフィールドを完全に共有しています。このフィールドは
:c:type:`PyObject` および :c:type:`PyVarObject` 型で表現されます。 :c:type:`PyObject` 型や
:c:type:`PyVarObject` 型もまた、他の全ての Python  オブジェクトを定義する上で直接的・間接的に使われているマクロを
使って定義されています。


.. c:type:: PyObject

   全てのオブジェクト型はこの型を拡張したものです。
   この型には、あるオブジェクトに対するオブジェクトとしてのポインタを Python
   から扱う必要がある際に必要な情報が入っています。通常に "リリースされている"
   ビルドでは、この構造体にはオブジェクトの参照カウントと、オブジェクトに
   対応する型オブジェクトだけが入っています。

   ``PyObject_HEAD`` マクロ展開で定義されているフィールドに対応します。


.. c:type:: PyVarObject

   :c:type:`PyObject` を拡張して、 :attr:`ob_size` フィールドを追加したものです。この構造体は、 *長さ (length)*
   の概念を持つオブジェクトだけに対して使います。この型が Python/C API で使われることはほとんどありません。
   ``PyObject_VAR_HEAD`` マクロ展開で定義されているフィールドに対応します。

:c:type:`PyObject` および :c:type:`PyVarObject` の定義には以下のマクロが使われています:


.. c:macro:: PyObject_HEAD

   :c:type:`PyObject` 型のフィールド宣言に展開されるマクロです;  可変でない長さを持つオブジェクトを表現する新たな型を宣言する
   場合に使います。展開によってどのフィールドが宣言されるかは、 :c:macro:`Py_TRACE_REFS` の定義に依存します。
   デフォルトでは、 :c:macro:`Py_TRACE_REFS` は定義されておらず、 :c:macro:`PyObject_HEAD`
   は以下のコードに展開されます::

      Py_ssize_t ob_refcnt;
      PyTypeObject *ob_type;

   :c:macro:`Py_TRACE_REFS` が定義されている場合、以下のように展開されます::

      PyObject *_ob_next, *_ob_prev;
      Py_ssize_t ob_refcnt;
      PyTypeObject *ob_type;


.. c:macro:: PyObject_VAR_HEAD

   マクロです。 :c:type:`PyVarObject` 型のフィールド宣言に展開されるマクロです;
   インスタンスによって可変の長さを持つオブジェクトを表現する新たな型を宣言する場合に使います。マクロは常に以下のように展開されます::

      PyObject_HEAD
      Py_ssize_t ob_size;

   マクロ展開結果の一部に :c:macro:`PyObject_HEAD` が含まれており、 :c:macro:`PyObject_HEAD`
   の展開結果は :c:macro:`Py_TRACE_REFS` の定義に依存します。


.. c:macro:: PyObject_HEAD_INIT(type)

   新しい :c:type:`PyObject` 型のための初期値に展開するマクロです。
   このマクロは次のように展開されます。 ::

      _PyObject_EXTRA_INIT
      1, type,


.. c:macro:: PyVarObject_HEAD_INIT(type, size)

   新しい、 :attr:`ob_size` フィールドを含む :c:type:`PyVarObject`
   型のための初期値に展開するマクロです。
   このマクロは次のように展開されます。 ::

      _PyObject_EXTRA_INIT
      1, type, size,


.. c:type:: PyCFunction

   ほとんどの Python の呼び出し可能オブジェクトを C で実装する際に用いられている関数の型です。この型の関数は二つの
   :c:type:`PyObject\*` 型パラメタをとり、 :c:type:`PyObject\*` 型の値を返します。戻り値を *NULL* にする場合、
   例外をセットしておかなければなりません。 *NULL* でない値を返す場合、戻り値は Python に関数の戻り値として公開される値として解釈されます。
   この型の関数は新たな参照を返さなければなりません。


.. c:type:: PyMethodDef

   拡張型のメソッドを記述する際に用いる構造体です。この構造体には 4 つのフィールドがあります:

   +------------------+-------------+----------------------------------------------+
   | フィールド       | C データ型  | 意味                                         |
   +==================+=============+==============================================+
   | :attr:`ml_name`  | char \*     | メソッド名                                   |
   +------------------+-------------+----------------------------------------------+
   | :attr:`ml_meth`  | PyCFunction | C 実装へのポインタ                           |
   +------------------+-------------+----------------------------------------------+
   | :attr:`ml_flags` | int         | 呼び出しをどのように行うかを示すフラグビット |
   +------------------+-------------+----------------------------------------------+
   | :attr:`ml_doc`   | char \*     | docstring の内容を指すポインタ               |
   +------------------+-------------+----------------------------------------------+

:attr:`ml_meth` は C の関数ポインタです。関数は別の型で定義されていてもかまいませんが、常に  :c:type:`PyObject\*`
を返します。関数が :c:type:`PyFunction` でない場合、メソッドテーブル内でキャストを行うようコンパイラが要求することになるでしょう。
:c:type:`PyCFunction` では最初のパラメタが :c:type:`PyObject\*` 型であると定義していますが、固有の C 型を
*self* オブジェクトに使う実装はよく行われています。

:attr:`ml_flags` フィールドはビットフィールドで、以下のフラグが入ります。個々のフラグは呼び出し規約 (calling convention)
や束縛規約 (binding convention) を表します。呼び出し規約フラグでは、 :const:`METH_VARARGS` および
:const:`METH_KEYWORDS` を組み合わせられます (ただし、 :const:`METH_KEYWORDS` 単体の指定を行っても
``METH_VARARGS | METH_KEYWORDS`` と同じなので注意してください)。呼び出し規約フラグは束縛フラグと組み合わせられます。


.. data:: METH_VARARGS

   :c:type:`PyCFunction` 型のメソッドで典型的に使われる呼び出し規約です。関数は :c:type:`PyObject\*`
   型の引数値を二つ要求します。
   最初の引数はメソッドの *self* オブジェクトです; モジュール関数の場合、これはモジュールオブジェクトです。
   第二のパラメタ (よく *args* と呼ばれます) は、全ての引数を表現するタプルオブジェクトです。
   パラメタは通常、 :c:func:`PyArg_ParseTuple` や :c:func:`PyArg_UnpackTuple` で処理されます。


.. data:: METH_KEYWORDS

   このフラグを持つメソッドは :c:type:`PyCFunctionWithKeywords`
   型でなければなりません。 :c:type:`PyCFunctionWithKeywords` は三つのパラメタ:*self* 、 *args* 、
   およびキーワード引数全てからなる辞書、を要求します。このフラグは通常 :const:`METH_VARARGS` と組み合わされ、パラメタは
   :c:func:`PyArg_ParseTupleAndKeywords` で処理されます。


.. data:: METH_NOARGS

   引数のないメソッドは、 :const:`METH_NOARGS` フラグをつけた場合、必要な引数が指定されているかをチェックしなくなります。こうしたメソッドは
   :c:type:`PyCFunction` 型でなくてはなりません。
   第一のパラメタは ``self`` になり、モジュールかオブジェクトインスタンスへの参照を
   保持することになります。いずれにせよ、第二のパラメタは *NULL* になります。


.. data:: METH_O

   単一のオブジェクト引数だけをとるメソッドは、 :c:func:`PyArg_ParseTuple` を引数 ``"O"`` にして呼び出す代わりに、
   :const:`METH_O` フラグつきで指定できます。メソッドは :c:type:`PyCFunction` 型で、 *self*
   パラメタと単一の引数を表現する :c:type:`PyObject\*` パラメタを伴います。


.. data:: METH_OLDARGS

   この呼び出し規約は撤廃されました。メソッドは :c:type:`PyCFunction` 型でなければなりません。第二引数は、引数がない場合には
   *NULL* 、単一の引数の場合にはその引数オブジェクト、複数個の引数の場合には引数オブジェクトからなるタプルです。この呼び出し規約を使うと、複数個の
   引数の場合と、単一のタプルが唯一引数の場合を区別できなくなってしまいます。

以下の二つの定数は、呼び出し規約を示すものではなく、クラスのメソッドとして使う際の束縛方式を示すものです。
モジュールに対して定義された関数で用いてはなりません。メソッドに対しては、最大で一つしかこのフラグをセットできません。


.. data:: METH_CLASS

   .. index:: builtin: classmethod

   メソッドの最初の引数には、型のインスタンスではなく型オブジェクトが渡されます。このフラグは組み込み関数 :func:`classmethod`
   を使って生成するのと同じ *クラスメソッド (class method)* を生成するために使われます。

   .. versionadded:: 2.3


.. data:: METH_STATIC

   .. index:: builtin: staticmethod

   メソッドの最初の引数には、型のインスタンスではなく *NULL* が渡されます。このフラグは、 :func:`staticmethod`
   を使って生成するのと同じ *静的メソッド (static method)* を生成するために使われます。

   .. versionadded:: 2.3

もう一つの定数は、あるメソッドを同名の別のメソッド定義と置き換えるかどうかを制御します。


.. data:: METH_COEXIST

   メソッドを既存の定義を置き換える形でロードします。 *METH_COEXIST* を指定しなければ、デフォルトの設定にしたがって、
   定義が重複しないようスキップします。スロットラッパはメソッドテーブルよりも前にロードされるので、例えば *sq_contains* スロットは
   ラップしているメソッド :meth:`__contains__` を生成し、同名の PyCFunction のロードを阻止します。このフラグを定義すると、
   PyCFunction はラッパオブジェクトを置き換える形でロードされ、スロットと連立します。 PyCFunctions の呼び出しはラッパオブジェクトの
   呼び出しよりも最適化されているので、こうした仕様が便利になります。

   .. versionadded:: 2.4


.. c:type:: PyMemberDef

   type の C 構造体のメンバとして格納されている、ある型の属性を表す構造体です。
   この構造体のフィールドは以下のとおりです:


   +------------------+-------------+-------------------------------+
   | フィールド       | C の型      | 意味                          |
   +==================+=============+===============================+
   | :attr:`name`     | char \*     | メンバ名                      |
   +------------------+-------------+-------------------------------+
   | :attr:`type`     | int         | C 構造体の中のメンバの型      |
   +------------------+-------------+-------------------------------+
   | :attr:`offset`   | Py_ssize_t  | そのメンバの type object      |
   |                  |             | 構造体中の場所の offset       |
   |                  |             | バイト数                      |
   +------------------+-------------+-------------------------------+
   | :attr:`flags`    | int         | フィールドが読み込み専用か    |
   |                  |             | 書込み可能なのかを示すビット  |
   |                  |             | フラグ                        |
   +------------------+-------------+-------------------------------+
   | :attr:`doc`      | char \*     | docstring の内容へのポインタ  |
   +------------------+-------------+-------------------------------+

   :attr:`type` はたくさんのCの型を意味する ``T_`` マクロのうちの1つです。
   メンバが Python からアクセスされるとき、そのメンバは対応する Python
   の型に変換されます。

   =============== ==================
   マクロ名          Cの型
   =============== ==================
   T_SHORT         short
   T_INT           int
   T_LONG          long
   T_FLOAT         float
   T_DOUBLE        double
   T_STRING        char \*
   T_OBJECT        PyObject \*
   T_OBJECT_EX     PyObject \*
   T_CHAR          char
   T_BYTE          char
   T_UBYTE         unsigned char
   T_UINT          unsigned int
   T_USHORT        unsigned short
   T_ULONG         unsigned long
   T_BOOL          char
   T_LONGLONG      long long
   T_ULONGLONG     unsigned long long
   T_PYSSIZET      Py_ssize_t
   =============== ==================

   :c:macro:`T_OBJECT` と :c:macro:`T_OBJECT_EX` については、
   :c:macro:`T_OBJECT` がメンバが *NULL* だったときに ``None`` を返すのに対し、
   :c:macro:`T_OBJECT_EX` は :exc:`AttributeError` を発生させる点が異なります。
   :c:macro:`T_OBJECT_EX` は属性に対する :keyword:`del` 文をより正しくあつかうので、
   できれば :c:macro:`T_OBJECT` よりも :c:macro:`T_OBJECT_EX` を使ってください。

   :attr:`flags` には読み書きアクセス可能なら 0 で、読み込み専用なら
   :c:macro:`READONLY` を設定します。
   :attr:`type` に :c:macro:`T_STRING` を使うと、強制的に :c:macro:`READONLY`
   扱いになります。
   :c:macro:`T_OBJECT` and :c:macro:`T_OBJECT_EX` メンバだけが del 可能です。
   (*NULL* が代入されます).

.. c:function:: PyObject* Py_FindMethod(PyMethodDef table[], PyObject *ob, char *name)

   C で実装された拡張型の束縛メソッドオブジェクトを返します。 :c:func:`PyObject_GenericGetAttr` 関数を使わない
   :attr:`tp_getattro` や :attr:`tp_getattr` ハンドラを実装する際に便利です。

