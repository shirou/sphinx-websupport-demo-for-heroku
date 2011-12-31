.. highlightlang:: c

.. _floatobjects:

浮動小数点型オブジェクト (floating point object)
------------------------------------------------

.. index:: object: floating point


.. c:type:: PyFloatObject

   この :c:type:`PyObject` のサブタイプは Python 浮動小数点型オブジェクトを表現します。


.. c:var:: PyTypeObject PyFloat_Type

   .. index:: single: FloatType (in modules types)

   この :c:type:`PyTypeObject` のインスタンスは Python 浮動小数点型を表現します。これは
   ``float`` や ``types.FloatType`` と同じオブジェクトです。


.. c:function:: int PyFloat_Check(PyObject *p)

   引数が :c:type:`PyFloatObject` か :c:type:`PyFloatObject` のサブタイプのときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyFloat_CheckExact(PyObject *p)

   引数が :c:type:`PyFloatObject` 型で、かつ :c:type:`PyFloatObject` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyFloat_FromString(PyObject *str, char **pend)

   *str* の文字列値をもとに :c:type:`PyFloatObject` オブジェクトを生成します。失敗すると *NULL* を返します。引数
   *pend* は無視されます。この引数は後方互換性のためだけに残されています。


.. c:function:: PyObject* PyFloat_FromDouble(double v)

   *v* から :c:type:`PyFloatObject` オブジェクトを生成して返します。失敗すると *NULL* を返します。


.. c:function:: double PyFloat_AsDouble(PyObject *pyfloat)

   *pyfloat* の指す値を、 C の :c:type:`double` 型表現で返します。


.. c:function:: double PyFloat_AS_DOUBLE(PyObject *pyfloat)

   *pyfloat* の指す値を、 C の :c:type:`double` 型表現で返しますが、エラーチェックを行いません。


.. c:function:: PyObject* PyFloat_GetInfo(void)

   float の精度、最小値、最大値に関する情報を含む structseq インスタンスを返します。
   これは、 :file:`float.h` ファイルの薄いラッパーです。

   .. versionadded:: 2.6


.. c:function:: double PyFloat_GetMax()

   float の表現できる最大限解値 *DBL_MAX* を C の :c:type:`double` 型で返します。

   .. versionadded:: 2.6


.. c:function:: double PyFloat_GetMin()

   float の正規化された最小の正の値 *DBL_MIN* を C の :c:type:`double` 型で返します。

   .. versionadded:: 2.6

.. c:function:: int PyFloat_ClearFreeList()

   float の free list をクリアします。
   開放できなかったアイテム数を返します。

   .. versionadded:: 2.6


.. c:function:: void PyFloat_AsString(char *buf, PyFloatObject *v)

   :func:`str` と同じルールで *v* を文字列に変換します。
   *buf* の長さは 100 以上でなければなりません。

   この関数は長さを知らないバッファに書きこむので安全ではありません。

   .. deprecated:: 2.7
      代わりに func:`PyObject_Str` か :func:`PyOS_double_to_string` を利用してください。


.. c:function:: void PyFloat_AsReprString(char *buf, PyFloatObject *v)

   PyFloat_AsString とほとんど同じですが、 :func:`repr` とおなじルールを使います。
   *buf* の長さは 100 以上でなければなりません。

   この関数は長さを知らないバッファに書きこむので安全ではありません。

   .. deprecated:: 2.7
      代わりに :func:`PyObject_Repr` か :func:`PyOS_double_to_string` を利用してください。
