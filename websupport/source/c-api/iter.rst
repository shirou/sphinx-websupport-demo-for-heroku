.. highlightlang:: c

.. _iterator:

イテレータプロトコル (iterator protocol)
========================================

.. versionadded:: 2.2

イテレータを扱うための固有の関数は二つしかありません。


.. c:function:: int PyIter_Check(PyObject *o)

   *o* がイテレータプロトコルをサポートする場合に真を返します。


.. c:function:: PyObject* PyIter_Next(PyObject *o)

   反復処理 *o* における次の値を返します。オブジェクトがイテレータの場合、この関数は反復処理における次の値を取り出します。
   要素が何も残っていない場合には例外がセットされていない状態で *NULL* を返します。オブジェクトがイテレータでない場合には
   :exc:`TypeError` を送出します。要素を取り出す際にエラーが生じると *NULL* を返し、発生した例外を送出します。

イテレータの返す要素にわたって反復処理を行うループを書くと、 C のコードは以下のようになるはずです::

   PyObject *iterator = PyObject_GetIter(obj);
   PyObject *item;

   if (iterator == NULL) {
       /* エラーの伝播処理をここに書く */
   }

   while (item = PyIter_Next(iterator)) {
       /* 取り出した要素で何らかの処理を行う */
       ...
       /* 終わったら参照を放棄する */
       Py_DECREF(item);
   }

   Py_DECREF(iterator);

   if (PyErr_Occurred()) {
       /* エラーの伝播処理をここに書く */
   }
   else {
       /* 別の処理を続ける */
   }


