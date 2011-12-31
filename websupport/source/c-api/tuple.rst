.. highlightlang:: c

.. _tupleobjects:

タプルオブジェクト (tuple object)
---------------------------------

.. index:: object: tuple


.. c:type:: PyTupleObject

   この :c:type:`PyObject` のサブタイプは Python のタプルオブジェクトを表現します。


.. c:var:: PyTypeObject PyTuple_Type

   .. index:: single: TupleType (in module types)

   この :c:type:`PyTypeObject` のインスタンスは Python のタプル型を表現します; Python レイヤにおける ``tuple``
   や ``types.TupleType``  と同じオブジェクトです。


.. c:function:: int PyTuple_Check(PyObject *p)

   *p* がタプルオブジェクトか、タプル型のサブタイプのインスタンスである場合に真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyTuple_CheckExact(PyObject *p)

   *p* がタプルオブジェクトで、かつタプル型のサブタイプのインスタンスでない場合に真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyTuple_New(Py_ssize_t len)

   サイズが *len* の新たなタプルオブジェクトを返します。失敗すると *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *len* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyTuple_Pack(Py_ssize_t n, ...)

   サイズが *n* の新たなタプルオブジェクトを返します。失敗すると *NULL* を返します。タプルの値は後続の *n* 個の Python オブジェクトを指す C
   引数になります。 ``PyTuple_Pack(2, a, b)`` は ``Py_BuildValue("(OO)", a, b)`` と同じです。

   .. versionadded:: 2.4

   .. versionchanged:: 2.5
      この関数は以前は *n* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_ssize_t PyTuple_Size(PyObject *p)

   タプルオブジェクトへのポインタを引数にとり、そのタプルのサイズを返します。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_ssize_t PyTuple_GET_SIZE(PyObject *p)

   タプル *p* のサイズを返しますが、 *p* は非 *NULL* でなくてはならず、タプルオブジェクトを指していなければなりません;
   この関数はエラーチェックを行いません。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyTuple_GetItem(PyObject *p, Py_ssize_t pos)

   *p* の指すタプルオブジェクト内の、位置 *pos* にあるオブジェクトを返します。 *pos* が範囲を超えている場合、 *NULL* を返して
   :exc:`IndexError` 例外をセットします。

   .. versionchanged:: 2.5
      この関数は以前は *pos* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyTuple_GET_ITEM(PyObject *p, Py_ssize_t pos)

   :c:func:`PyTuple_GetItem` に似ていますが、引数に対するエラーチェックを行いません。

   .. versionchanged:: 2.5
      この関数は以前は *pos* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyTuple_GetSlice(PyObject *p, Py_ssize_t low, Py_ssize_t high)

   *p* の指すタプルオブジェクト内の、位置 *low* から *high* までのスライスを取り出して、タプルオブジェクトとして返します。

   .. versionchanged:: 2.5
      この関数は以前は *low*, *high* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyTuple_SetItem(PyObject *p, Py_ssize_t pos, PyObject *o)

   *p* の指すタプルオブジェクト内の位置 *pos* に、オブジェクト *o* への参照を挿入します。成功した場合には ``0`` を返します。

   .. note::

      この関数は *o* への参照を "盗み取り" ます。

   .. versionchanged:: 2.5
      この関数は以前は *pos* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: void PyTuple_SET_ITEM(PyObject *p, Py_ssize_t pos, PyObject *o)

   :c:func:`PyTuple_SetItem` に似ていますが、エラーチェックを行わず、新たなタプルに値を入れるとき *以外には使ってはなりません* 。

   .. note::

      この関数は *o* への参照を "盗み取り" ます。

   .. versionchanged:: 2.5
      この関数は以前は *pos* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int _PyTuple_Resize(PyObject **p, Py_ssize_t newsize)

   タプルをリサイズする際に使えます。 *newsize* はタプルの新たな長さです。タプルは変更不能なオブジェクト *ということになっている*
   ので、この関数はこのオブジェクトに対してただ一つしか参照がない時以外には使ってはなりません。タプルがコード中の他の部分ですでに参照
   されている場合には、この関数を *使ってはなりません* 。タプルは常に指定サイズの末尾まで伸縮します。成功した場合には ``0`` を返します。
   クライアントコードは、 ``*p`` の値が呼び出し前と同じになると期待してはなりません。 ``*p`` が置き換えられた場合、オリジナルの ``*p``
   は破壊されます。失敗すると ``-1`` を返し、 ``*p`` を *NULL* に設定して、  :exc:`MemoryError` または
   :exc:`SystemError` を送出します。

   .. versionchanged:: 2.2
      使われていなかった三つ目のパラメタ、 *last_is_sticky* を削除しました.

   .. versionchanged:: 2.5
      この関数は以前は *newsize* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyTuple_ClearFreeList()

   free list をクリアします。
   開放したアイテム数を返します。

   .. versionadded:: 2.6
