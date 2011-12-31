.. highlightlang:: c

.. _mapping:

マップ型プロトコル (mapping protocol)
=====================================


.. c:function:: int PyMapping_Check(PyObject *o)

   オブジェクトがマップ型プロトコルを提供している場合に ``1`` を返し、そうでないときには ``0`` を返します。この関数呼び出しは常に成功します。


.. c:function:: Py_ssize_t PyMapping_Size(PyObject *o)
                Py_ssize_t PyMapping_Length(PyObject *o)

   .. index:: builtin: len

   成功するとオブジェクト *o* 中のキーの数を返し、失敗すると ``-1`` を返します。マップ型プロトコルを提供していないオブジェクトに対しては、
   Python の式 ``len(o)`` と同じになります。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyMapping_DelItemString(PyObject *o, char *key)

   オブジェクト *o* から *key* に関する対応付けを削除します。失敗すると ``-1`` を返します。 Python の文 ``del o[key]``
   と同じです。


.. c:function:: int PyMapping_DelItem(PyObject *o, PyObject *key)

   オブジェクト *o* から *key* に対する対応付けを削除します。失敗すると ``-1`` を返します。 Python の文 ``del o[key]``
   と同じです。


.. c:function:: int PyMapping_HasKeyString(PyObject *o, char *key)

   成功すると、マップ型オブジェクトがキー *key* を持つ場合に ``1`` を返し、
   そうでないときには ``0`` を返します。
   これは、 ``o[key]`` が成功したときに ``True`` を、例外が発生したときに
   ``False`` を返すのと等価です。
   この関数呼び出しは常に成功します。


.. c:function:: int PyMapping_HasKey(PyObject *o, PyObject *key)

   マップ型オブジェクトがキー *key* を持つ場合に ``1`` を返し、そうでないときには
   ``0`` を返します。
   これは、 ``o[key]`` が成功したときに ``True`` を、例外が発生したときに
   ``False`` を返すのと等価です。
   この関数呼び出しは常に成功します。


.. c:function:: PyObject* PyMapping_Keys(PyObject *o)

   成功するとオブジェクト *o* のキーからなるリストを返します。失敗すると *NULL* を返します。 Python の式 ``o.keys()``
   と同じです。


.. c:function:: PyObject* PyMapping_Values(PyObject *o)

   成功するとオブジェクト *o* のキーに対応する値からなるリストを返します。失敗すると *NULL* を返します。 Python の式
   ``o.values()`` と同じです。


.. c:function:: PyObject* PyMapping_Items(PyObject *o)

   成功するとオブジェクト *o* の要素対、すなわちキーと値のペアが入ったタプルからなるリストを返します。失敗すると *NULL* を返します。 Python
   の式 ``o.items()`` と同じです。


.. c:function:: PyObject* PyMapping_GetItemString(PyObject *o, char *key)

   オブジェクト *key* に対応する *o* の要素を返します。失敗すると *NULL* を返します。 Python の式 ``o[key]`` と同じです。


.. c:function:: int PyMapping_SetItemString(PyObject *o, char *key, PyObject *v)

   オブジェクト *o* で *key* を値 *v* に対応付けます。失敗すると ``-1`` を返します。 Python の文 ``o[key] = v``
   と同じです。

