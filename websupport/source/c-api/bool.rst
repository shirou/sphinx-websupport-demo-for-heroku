.. highlightlang:: c

.. _boolobjects:

Bool 型オブジェクト
-------------------

Python の Bool 型は整数のサブクラスとして実装されています。ブール型の値は、 :const:`Py_False` と
:const:`Py_True` の 2 つしかありません。従って、通常の生成／削除関数はブール型にはあてはまりません。
とはいえ、以下のマクロが利用できます。

.. % Boolean Objects


.. c:function:: int PyBool_Check(PyObject *o)

   *o* が :c:data:`PyBool_Type` の場合に真を返します。

   .. versionadded:: 2.3


.. c:var:: PyObject* Py_False

   Python における ``False`` オブジェクトです。このオブジェクトはメソッドを持ちません。参照カウントの点では、他のオブジェクトと同様に扱う必要が
   あります。


.. c:var:: PyObject* Py_True

   Python における ``True`` オブジェクトです。このオブジェクトはメソッドを持ちません。参照カウントの点では、他のオブジェクトと同様に扱う必要が
   あります。


.. c:macro:: Py_RETURN_FALSE

   :const:`Py_False` に適切な参照カウントのインクリメントを行って、関数から返すためのマクロです。

   .. versionadded:: 2.4


.. c:macro:: Py_RETURN_TRUE

   :const:`Py_True` に適切な参照カウントのインクリメントを行って、関数から返すためのマクロです。

   .. versionadded:: 2.4


.. c:function:: int PyBool_FromLong(long v)

   *v* の値に応じて :const:`Py_True` または :const:`Py_False` への新しい参照を返します。

   .. versionadded:: 2.3

