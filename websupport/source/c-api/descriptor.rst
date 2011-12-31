.. highlightlang:: c

.. _descriptor-objects:

デスクリプタオブジェクト (descriptor object)
--------------------------------------------

"デスクリプタ (descriptor)" は、あるオブジェクトのいくつかの属性について記述したオブジェクトです。デスクリプタオブジェクトは
型オブジェクトの辞書内にあります。


.. c:var:: PyTypeObject PyProperty_Type

   組み込みデスクリプタ型の型オブジェクトです。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyDescr_NewGetSet(PyTypeObject *type, struct PyGetSetDef *getset)

   .. versionadded:: 2.2


.. c:function:: PyObject* PyDescr_NewMember(PyTypeObject *type, struct PyMemberDef *meth)

   .. versionadded:: 2.2


.. c:function:: PyObject* PyDescr_NewMethod(PyTypeObject *type, struct PyMethodDef *meth)

   .. versionadded:: 2.2


.. c:function:: PyObject* PyDescr_NewWrapper(PyTypeObject *type, struct wrapperbase *wrapper, void *wrapped)

   .. versionadded:: 2.2


.. c:function:: int PyDescr_IsData(PyObject *descr)

   デスクリプタオブジェクト *descr* がデータ属性のデスクリプタの場合には真を、メソッドデスクリプタの場合には偽を返します。 *descr*
   はデスクリプタオブジェクトでなければなりません; エラーチェックは行いません。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyWrapper_New(PyObject *, PyObject *)

   .. versionadded:: 2.2


