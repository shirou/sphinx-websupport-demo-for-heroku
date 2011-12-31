.. highlightlang:: c

.. _longobjects:

長整数型オブジェクト (long integer object)
------------------------------------------

.. index:: object: long integer


.. c:type:: PyLongObject

   この :c:type:`PyObject` のサブタイプは長整数型を表現します。


.. c:var:: PyTypeObject PyLong_Type

   .. index:: single: LongType (in modules types)

   この :c:type:`PyTypeObject` のインスタンスは Python 長整数型を表現します。これは
   ``long`` や ``types.LongType`` と同じオブジェクトです。


.. c:function:: int PyLong_Check(PyObject *p)

   引数が :c:type:`PyLongObject` か :c:type:`PyLongObject` のサブタイプのときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyLong_CheckExact(PyObject *p)

   引数が :c:type:`PyLongObject` 型で、かつ :c:type:`PyLongObject` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyLong_FromLong(long v)

   *v* から新たな :c:type:`PyLongObject` オブジェクトを生成して返します。失敗のときには *NULL* を返します。


.. c:function:: PyObject* PyLong_FromUnsignedLong(unsigned long v)

   C の :c:type:`unsigned long` 型から新たな :c:type:`PyLongObject` オブジェクトを生成して返します。
   失敗のときには *NULL* を返します。


.. c:function:: PyObject* PyLong_FromSsize_t(Py_ssize_t v)

   C の :c:type:`Py_ssize_t` 型から新たな :c:type:`PyLongObject` オブジェクトを生成して返します。
   失敗のときには *NULL* を返します。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyLong_FromSize_t(size_t v)

   C の :c:type:`size_t` 型から新たな :c:type:`PyLongObject` オブジェクトを生成して返します。
   失敗のときには *NULL* を返します。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyLong_FromSsize_t(Py_ssize_t v)

   *v* から新しい :c:type:`PyLongObject` オブジェクトを返します。
   失敗したら *NULL* を返します。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyLong_FromSize_t(size_t v)

   *v* から新しい :c:type:`PyLongObject` オブジェクトを返します。
   失敗したら *NULL* を返します。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyLong_FromLongLong(PY_LONG_LONG v)

   C の :c:type:`long long` 型から新たな :c:type:`PyLongObject` オブジェクトを生成して返します。失敗のときには
   *NULL* を返します。


.. c:function:: PyObject* PyLong_FromUnsignedLongLong(unsigned PY_LONG_LONG v)

   C の :c:type:`unsigned long long` 型から新たな :c:type:`PyLongObject`
   オブジェクトを生成して返します。失敗のときには *NULL* を返します。


.. c:function:: PyObject* PyLong_FromDouble(double v)

   *v* の整数部から新たな :c:type:`PyLongObject` オブジェクトを生成して返します。失敗のときには *NULL* を返します。


.. c:function:: PyObject* PyLong_FromString(char *str, char **pend, int base)

   *str* の文字列値に基づいて、新たな :c:type:`PyLongObject` を返します。このとき *base* を基数として文字列を解釈します。
   *pend* が *NULL* でなければ、 *\*pend* は *str* 中で数が表現されている部分以後の先頭の文字のアドレスを指しています。
   *base* が ``0`` ならば、 *str* の先頭の文字列に基づいて基数を決定します: もし *str* が ``'0x'`` または ``'0X'``
   で始まっていれば、基数に 16 を使います; *str* が ``'0'`` で始まっていれば、基数に 8 を使います; その他の場合には基数に 10 を
   使います。 *base* が ``0`` でなければ、 *base* は ``2`` 以上 ``36`` 以下の数でなければなりません。先頭に空白がある場合は
   無視されます。数字が全くない場合、 :exc:`ValueError` が送出されます。


.. c:function:: PyObject* PyLong_FromUnicode(Py_UNICODE *u, Py_ssize_t length, int base)

   Unicode の数字配列を Python の長整数型に変換します。最初のパラメタ *u* は、 Unicode 文字列の最初の文字を指し、 *length*
   には文字数を指定し、 *base* には変換時の基数を指定します。基数は範囲 [2, 36] になければなりません; 範囲外の基数を指定すると、
   :exc:`ValueError` を送出します。

   .. versionadded:: 1.6

   .. versionchanged:: 2.5
      この関数は以前は *length* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyLong_FromVoidPtr(void *p)

   Python 整数型または長整数型をポインタ *p* から生成します。ポインタに入れる値は :c:func:`PyLong_AsVoidPtr` を使って
   得られるような値です。

   .. versionadded:: 1.5.2

   .. versionchanged:: 2.5
      整数値がLONG_MAXより大きい場合は、正の長整数を返します.


.. c:function:: long PyLong_AsLong(PyObject *pylong)

   .. index::
      single: LONG_MAX
      single: OverflowError (built-in exception)

   *pylong* の指す長整数値を、 C の :c:type:`long` 型表現で返します。 *pylong* が :const:`LONG_MAX` よりも
   大きい場合、 :exc:`OverflowError` を送出し、 ``-1`` を返します。


.. c:function:: long PyLong_AsLongAndOverflow(PyObject *pylong, int *overflow)

   *pylong* の値を :c:type:`long` で返す。
   *pylong* が :const:`LONG_MAX` より大きかったり :const:`LONG_MIN` より小さい場合、
   *\*overflow* に ``1`` か ``-1`` を設定して ``-1`` を返します。
   それ以外の場合は *\*overflow* に ``0`` を設定します。
   なにか例外が発生した場合は(TypeError や MemoryErrorなど)、 *\*overflow* は
   0 で戻り値が ``-1`` になります。

   .. versionadded:: 2.7


.. c:function:: PY_LONG_LONG PyLong_AsLongLongAndOverflow(PyObject *pylong, int *overflow)

   *pylong* の値を :c:type:`long long` で返す。
   *pylong* が :const:`PY_LLONG_MAX` より大きかったり :const:`PY_LLONG_MIN` より小さい場合、
   *\*overflow* に ``1`` か ``-1`` を設定して ``-1`` を返します。
   それ以外の場合は *\*overflow* に ``0`` を設定します。
   なにか例外が発生した場合は(TypeError や MemoryErrorなど)、 *\*overflow* は
   0 で戻り値が ``-1`` になります。

   .. versionadded:: 2.7


.. c:function:: Py_ssize_t PyLong_AsSsize_t(PyObject *pylong)

   .. index::
      single: PY_SSIZE_T_MAX
      single: OverflowError (built-in exception)

   *pylong* の指す長整数値を、 C の :c:type:`Py_ssize_t` 型表現で返します。
   *pylong* が :const:`PY_SSIZE_T_MAX` よりも大きい場合、
   :exc:`OverflowError` を送出し、 ``-1`` を返します。

   .. versionadded:: 2.6


.. c:function:: unsigned long PyLong_AsUnsignedLong(PyObject *pylong)

   .. index::
      single: ULONG_MAX
      single: OverflowError (built-in exception)

   *pylong* の指す長整数値を、 C の :c:type:`unsigned long` 型表現で返します。 *pylong* が
   :const:`ULONG_MAX` よりも大きい場合、 :exc:`OverflowError` を送出します。


.. c:function:: Py_ssize_t PyLong_AsSsize_t(PyObject *pylong)

   .. index::
      single: PY_SSIZE_T_MAX

   *pylong* の指す長整数値を、 C の :c:type:`Py_ssize_t` 型表現で返します。 *pylong* が
   :const:`PY_SSIZE_T_MAX` より大きい場合、  :exc:`OverflowError` を発生させます。

   .. versionadded:: 2.6


.. c:function:: PY_LONG_LONG PyLong_AsLongLong(PyObject *pylong)

   .. index::
      single: OverflowError (built-in exception)

   *pylong* の指す長整数値を、 C の :c:type:`long long` 型表現で返します。
   *pylong* が :c:type:`long long` で表せない場合、 :exc:`OverflowError` を送出し ``-1`` を返します。

   .. versionadded:: 2.2


.. c:function:: unsigned PY_LONG_LONG PyLong_AsUnsignedLongLong(PyObject *pylong)

   .. index::
      single: OverflowError (built-in exception)

   *pylong* の指す値を、 C の :c:type:`unsigned long long` 型表現で返します。 *pylong* が
   :c:type:`unsigned long long` で表せない場合、 :exc:`OverflowError` を発生させて、
   ``(unsigned long long)-1`` を返します。

   .. versionadded:: 2.2

   .. versionchanged:: 2.7
      負の *pylong* が :exc:`TypeError` ではなく :exc:`OverflowError` を発生させるようになりました。


.. c:function:: unsigned long PyLong_AsUnsignedLongMask(PyObject *io)

   Python 長整数値を、オーバフローチェックを行わずに C の :c:type:`unsigned long` 型表現で返します。

   .. versionadded:: 2.3


.. c:function:: unsigned PY_LONG_LONG PyLong_AsUnsignedLongLongMask(PyObject *io)

   Python 長整数値を、オーバフローチェックを行わずに C の :c:type:`unsigned long long` 型表現で返します。

   .. versionadded:: 2.3


.. c:function:: double PyLong_AsDouble(PyObject *pylong)

   *pylong* の指す値を、 C の :c:type:`double` 型表現で返します。 *pylong* が :c:type:`double`
   を使って近似表現できない場合、 :exc:`OverflowError` 例外を送出して ``-1.0`` を返します。


.. c:function:: void* PyLong_AsVoidPtr(PyObject *pylong)

   Python の整数型か長整数型を指す *pylong* を、 C の :c:type:`void` ポインタに変換します。 *pylong* を変換できなければ、
   :exc:`OverflowError` を送出します。この関数は :c:func:`PyLong_FromVoidPtr` で値を生成するときに使うような
   :c:type:`void` ポインタ型を生成できるだけです。

   .. versionadded:: 1.5.2

   .. versionchanged:: 2.5
      値が0..LONG_MAXの範囲の外だった場合、符号付き整数と符号無し整数の両方とも利用可能です.

