.. highlightlang:: c

.. _iterator-objects:

イテレータオブジェクト (iterator object)
----------------------------------------

Python では二種類のイテレータオブジェクトを提供しています。一つ目はシーケンスイテレータで、 :meth:`__getitem__` メソッドを
サポートする任意のシーケンスを取り扱います。二つ目は呼び出し可能オブジェクトとセンチネル値 (sentinel value) を扱い、
シーケンス内の要素ごとに呼び出し可能オブジェクトを呼び出して、センチネル値が返されたときに反復処理を終了します。


.. c:var:: PyTypeObject PySeqIter_Type

   :c:func:`PySeqIter_New` や、組み込みシーケンス型に対して 1 引数形式の組み込み関数 :func:`iter` を呼び出したときに
   返される、イテレータオブジェクトの型オブジェクトです。

   .. versionadded:: 2.2


.. c:function:: int PySeqIter_Check(op)

   :c:data:`PySeqIter_Type` の型が *op* のときに真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PySeqIter_New(PyObject *seq)

   一般的なシーケンスオブジェクト *seq* を扱うイテレータを返します。反復処理は、シーケンスが添字指定操作の際に :exc:`IndexError` を
   返したときに終了します。

   .. versionadded:: 2.2


.. c:var:: PyTypeObject PyCallIter_Type

   :c:func:`PyCallIter_New` や、組み込み関数 :func:`iter` の 2 引数形式が返すイテレータオブジェクトの型オブジェクトです。
   :func:`iter` built-in function.

   .. versionadded:: 2.2


.. c:function:: int PyCallIter_Check(op)

   :c:data:`PyCallIter_Type` の型が *op* のときに真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyCallIter_New(PyObject *callable, PyObject *sentinel)

   新たなイテレータを返します。最初のパラメタ *callable* は引数なしで呼び出せる Python の呼び出し可能オブジェクトならなんでもかまいません;
   *callable* は、呼び出されるたびに次の反復処理対象オブジェクトを返さなければなりません。生成されたイテレータは、 *callable* が
   *sentinel* に等しい値を返すと反復処理を終了します。

   .. versionadded:: 2.2

