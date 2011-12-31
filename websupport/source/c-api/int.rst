.. highlightlang:: c

.. _intobjects:

(通常)整数型オブジェクト (plain integer object)
-----------------------------------------------

.. index:: object: integer


.. c:type:: PyIntObject

   この :c:type:`PyObject` のサブタイプは Python の整数型オブジェクトを表現します。


.. c:var:: PyTypeObject PyInt_Type

   .. index:: single: IntType (in modules types)

   この :c:type:`PyTypeObject` のインスタンスは Python の (長整数でない)整数型を表現します。これは
   ``int`` や ``types.IntType`` と同じオブジェクトです。


.. c:function:: int PyInt_Check(PyObject *o)

   *o* が :c:data:`PyInt_Type` 型か :c:data:`PyInt_Type` 型のサブタイプであるときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyInt_CheckExact(PyObject *o)

   *o* が :c:data:`PyInt_Type` 型で、かつ :c:data:`PyInt_Type` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyInt_FromString(char *str, char **pend, int base)

   *str* の文字列値に基づいて、新たな :c:type:`PyIntObject` または :c:type:`PyLongObject` を返します。このとき
   *base* を基数として文字列を解釈します。 *pend* が *NULL* でなければ、 ``*pend`` は *str* 中で
   数が表現されている部分以後の先頭の文字のアドレスを指しています。 *base* が ``0`` ならば、 *str* の先頭の文字列に基づいて基数を決定します:
   もし *str* が ``'0x'`` または ``'0X'`` で始まっていれば、基数に 16 を使います; *str* が ``'0'``
   で始まっていれば、基数に 8 を使います; その他の場合には基数に 10 を使います。 *base* が ``0`` でなければ、 *base* は ``2``
   以上 ``36`` 以下の数でなければなりません。先頭に空白がある場合は無視されます。数字が全くない場合、 :exc:`ValueError` が送出
   されます。使用しているマシンの :c:type:`long int` 型で表現し切れないくらい大きな数が文字列に入っており、オーバフロー警告が抑制されていれば、
   :c:type:`PyLongObject` を返します。オーバフロー警告が抑制されていなければ、 *NULL* を返します。


.. c:function:: PyObject* PyInt_FromLong(long ival)

   *ival* の値を使って新たな整数オブジェクトを生成します。

   現在の実装では、 ``-5`` から ``256`` までの全ての整数に対する整数オブジェクトの配列を保持するようにしており、
   この範囲の数を生成すると、実際には既存のオブジェクトに対する参照が返るようになっています。従って、 ``1`` の
   値を変えることすら可能です。変えてしまった場合の Python の挙動は未定義です :-)


.. c:function:: PyObject* PyInt_FromSsize_t(Py_ssize_t ival)

   *ival* の値を使って新たな整数オブジェクトを生成します。
   値が ``LONG_MAX`` を超えている場合、長整数オブジェクトを返します。

   .. versionadded:: 2.5


.. c:function:: PyObject* PyInt_FromSize_t(size_t ival)

   *ival* の値を使って新たな整数オブジェクトを生成します。
   値が ``LONG_MAX`` を超えている場合、長整数オブジェクトを返します。

   .. versionadded:: 2.5


.. c:function:: long PyInt_AsLong(PyObject *io)

   オブジェクトがまだ :c:type:`PyIntObject` でなければまず型キャストを試み、次にその値を返します。
   エラーが発生した場合、 ``-1`` が返されます。その時呼び出し側は、 ``PyErr_Occurred()`` を使って、エラーが発生したのか、
   単に値が-1だったのかを判断するべきです。


.. c:function:: long PyInt_AS_LONG(PyObject *io)

   オブジェクト *io* の値を返します。エラーチェックを行いません。


.. c:function:: unsigned long PyInt_AsUnsignedLongMask(PyObject *io)

   オブジェクトがまだ :c:type:`PyIntObject` または :c:type:`PyLongObject` で
   なければまず型キャストを試み、次にその値を :c:type:`unsigned long` 型で返します。この関数はオーバフローをチェックしません。

   .. versionadded:: 2.3


.. c:function:: unsigned PY_LONG_LONG PyInt_AsUnsignedLongLongMask(PyObject *io)

   オブジェクトがまだ :c:type:`PyIntObject` または :c:type:`PyLongObject` で
   なければまず型キャストを試み、次にその値を :c:type:`unsigned long long` 型で返します。オーバフローをチェックしません。

   .. versionadded:: 2.3


.. c:function:: Py_ssize_t PyInt_AsSsize_t(PyObject *io)

   オブジェクトがまだ :c:type:`PyIntObject` でなければまず型キャストを試み、次にその値を :c:type:`Py_ssize_t` 型で返します。

   .. versionadded:: 2.5


.. c:function:: long PyInt_GetMax()

   .. index:: single: LONG_MAX

   システムの知識に基づく、扱える最大の整数値 (システムのヘッダファイルに定義されている :const:`LONG_MAX`) を返します。

.. c:function:: int PyInt_ClearFreeList()

   整数の free list をクリアします。
   開放できなかった要素の数を返します。

   .. versionadded:: 2.6
