.. highlightlang:: c

.. _allocating-objects:

オブジェクトをヒープ上にメモリ確保する
======================================


.. c:function:: PyObject* _PyObject_New(PyTypeObject *type)


.. c:function:: PyVarObject* _PyObject_NewVar(PyTypeObject *type, Py_ssize_t size)

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: void _PyObject_Del(PyObject *op)


.. c:function:: PyObject* PyObject_Init(PyObject *op, PyTypeObject *type)

   新たにメモリ確保されたオブジェクト *op* に対し、型と初期状態での参照 (initial reference) を初期化します。
   初期化されたオブジェクトを返します。 *type* からそのオブジェクトが循環参照ガベージ検出の機能を有する場合、検出機構が監視対象とする
   オブジェクトのセットに追加されます。オブジェクトの他のフィールドには影響を及ぼしません。


.. c:function:: PyVarObject* PyObject_InitVar(PyVarObject *op, PyTypeObject *type, Py_ssize_t size)

   :c:func:`PyObject_Init` の全ての処理を行い、可変サイズオブジェクトの場合には長さ情報も初期化します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: TYPE* PyObject_New(TYPE, PyTypeObject *type)

   C 構造体型 *TYPE* と Python 型オブジェクト *type* を使って新たな Python オブジェクトをメモリ確保します。 Python
   オブジェクトヘッダで定義されていないフィールドは初期化されません; オブジェクトの参照カウントは 1 になります。メモリ確保のサイズは型オブジェクトの
   :attr:`tp_basicsize` で決定します。


.. c:function:: TYPE* PyObject_NewVar(TYPE, PyTypeObject *type, Py_ssize_t size)

   C 構造体型 *TYPE* と Python 型オブジェクト *type* を使って新たな Python オブジェクトをメモリ確保します。 Python
   オブジェクトヘッダで定義されていないフィールドは初期化されません。確保されたメモリは、 *TYPE* 構造体に加え、vartype の
   :attr:`tp_itemsize` フィールドで指定されているサイズ中の *size* フィールドを
   収容できます。この関数は、例えばタプルのように生成時にサイズを決定できるオブジェクトを実装する際に便利です。一連の複数のフィールドに
   対するアロケーション操作を一つにして埋め込むと、アロケーション回数が減り、メモリ管理の処理効率が向上します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: void PyObject_Del(PyObject *op)

   :c:func:`PyObject_New` や :c:func:`PyObject_NewVar` で
   確保されたメモリを解放します。この関数は、通常オブジェクトの型に指定されている :attr:`tp_dealloc` ハンドラ内で呼び出します。
   この関数を呼び出した後では、オブジェクトのメモリ領域はもはや有効な Python オブジェクトを表現してはいないので、オブジェクトのフィールド
   に対してアクセスしてはなりません。


.. c:function:: PyObject* Py_InitModule(char *name, PyMethodDef *methods)

   *name* と関数のテーブルに基づいて新たなモジュールオブジェクトを生成し、生成されたモジュールオブジェクトを返します。

   .. versionchanged:: 2.3
      以前のバージョンの Python では、 *methods* 引数の値として *NULL* をサポートしていませんでした.


.. c:function:: PyObject* Py_InitModule3(char *name, PyMethodDef *methods, char *doc)

   *name* と関数のテーブルに基づいて新たなモジュールオブジェクトを生成し、生成されたモジュールオブジェクトを返します。 *doc* が
   *NULL* でない場合、モジュールの docstring として使われます。

   .. versionchanged:: 2.3
      以前のバージョンの Python では、 *methods* 引数の値として *NULL* をサポートしていませんでした.


.. c:function:: PyObject* Py_InitModule4(char *name, PyMethodDef *methods, char *doc, PyObject *self, int apiver)

   *name* と関数のテーブルに基づいて新たなモジュールオブジェクトを生成し、生成されたモジュールオブジェクトを返します。 *doc* が
   *NULL* でない場合、モジュールの docstring として使われます。 *self* が *NULL* でない場合、モジュール内の各関数
   の第一引数として渡されます (*NULL* の時には第一引数も *NULL* になります)。 (この関数は実験的な機能のために追加されたもので、現在の Python
   のバージョンで使われてはいないはずです。) *apiver* に渡してよい値は、 :const:`PYTHON_API_VERSION`
   で定義されている定数だけです。

   .. note::

      この関数のほとんどの用途は、代わりに :c:func:`Py_InitModule3` を使えるはずです; 本当にこの関数を使いたいときにだけ利用してください

   .. versionchanged:: 2.3
      以前のバージョンの Python では、 *methods* 引数の値として *NULL* をサポートしていませんでした.


.. c:var:: PyObject _Py_NoneStruct

   Python からは ``None`` に見えるオブジェクトです。この値へのアクセスは、このオブジェクトへのポインタを評価する ``Py_None``
   マクロを使わねばなりません。

