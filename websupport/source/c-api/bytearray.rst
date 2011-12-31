.. highlightlang:: c

.. _bytearrayobjects:

bytearray オブジェクト
------------------------

.. index:: object: bytearray

.. versionadded:: 2.6


.. c:type:: PyByteArrayObject

   Python の bytearray オブジェクトを示す :c:type:`PyObject` のサブタイプ


.. c:var:: PyTypeObject PyByteArray_Type

   この :c:type:`PyTypeObject` のインスタンスは、 Python bytearray 型を示します。
   Python レイヤでの ``bytearray`` と同じオブジェクトです。

型チェックマクロ
^^^^^^^^^^^^^^^^^

.. c:function:: int PyByteArray_Check(PyObject *o)

   *o* が bytearray かそのサブタイプのインスタンスだった場合に真を返します。


.. c:function:: int PyByteArray_CheckExact(PyObject *o)

   *o* が bytearray オブジェクトで、そのサブタイプのインスタンスでは無いときに、
   真を返します。


ダイレクト API 関数
^^^^^^^^^^^^^^^^^^^^

.. c:function:: PyObject* PyByteArray_FromObject(PyObject *o)

   バッファプロトコルを実装している任意のオブジェクト *o* から、
   新しい bytearray オブジェクトを作成し返します。

   .. XXX expand about the buffer protocol, at least somewhere


.. c:function:: PyObject* PyByteArray_FromStringAndSize(const char *string, Py_ssize_t len)

   *string* とその長さ *len* から新しい bytearray オブジェクトを返します。
   失敗した場合は *NULL* を返します。


.. c:function:: PyObject* PyByteArray_Concat(PyObject *a, PyObject *b)

   bytearray *a* と *b* を連結した結果を新しい bytearray として返します。


.. c:function:: Py_ssize_t PyByteArray_Size(PyObject *bytearray)

   *NULL* ポインタチェックの後に *bytearray* のサイズを返します。


.. c:function:: char* PyByteArray_AsString(PyObject *bytearray)

   *NULL* ポインタチェックの後に *bytearray* の内容を char 配列として返します。


.. c:function:: int PyByteArray_Resize(PyObject *bytearray, Py_ssize_t len)

   *bytearray* の内部バッファを *len* へリサイズします。

マクロ
^^^^^^

以下のマクロは、ポインタのチェックをしないことにより安全性を犠牲にして
スピードを優先しています。

.. c:function:: char* PyByteArray_AS_STRING(PyObject *bytearray)

   :c:func:`PyByteArray_AsString` のマクロバージョン。


.. c:function:: Py_ssize_t PyByteArray_GET_SIZE(PyObject *bytearray)

   :c:func:`PyByteArray_Size` のマクロバージョン。
