.. highlightlang:: c

.. _method-objects:

メソッドオブジェクト (method object)
------------------------------------

.. index:: object: method

C API にはメソッドオブジェクトを扱うのに便利な関数があります。


.. c:var:: PyTypeObject PyMethod_Type

   .. index:: single: MethodType (in module types)

   この :c:type:`PyTypeObject` のインスタンスは Python のメソッド型を表現します。
   このオブジェクトは、 ``types.MethodType``  として Python プログラムに公開されています。


.. c:function:: int PyMethod_Check(PyObject *o)

   *o* がメソッドオブジェクト (:c:data:`PyMethod_Type` 型である) 場合に真を返します。パラメータは *NULL* にできません。


.. c:function:: PyObject* PyMethod_New(PyObject *func, PyObject *self, PyObject *class)

   任意の呼び出し可能オブジェクト *func* を使った新たなメソッドオブジェクトを返します; 関数 *func* は、メソッドが呼び出された
   時に呼び出されるオブジェクトです。このメソッドをインスタンスに束縛 (bind) したい場合、 *self* をインスタンス自体にして、 *class*
   を *self* のクラスにしなければなりません。それ以外の場合は *self* を *NULL* に、 *class* を
   非束縛メソッドを提供しているクラスにしなければなりません。


.. c:function:: PyObject* PyMethod_Class(PyObject *meth)

   メソッドオブジェクト *meth* を生成したクラスオブジェクトを返します; インスタンスがメソッドオブジェクトを生成した場合、戻り値は
   インスタンスのクラスになります。


.. c:function:: PyObject* PyMethod_GET_CLASS(PyObject *meth)

   :c:func:`PyMethod_Class` をマクロで実装したバージョンで、エラーチェックを行いません。


.. c:function:: PyObject* PyMethod_Function(PyObject *meth)

   メソッド *meth* に関連付けられている関数オブジェクトを返します。


.. c:function:: PyObject* PyMethod_GET_FUNCTION(PyObject *meth)

   :c:func:`PyMethod_Function` のマクロ版で、エラーチェックを行いません。


.. c:function:: PyObject* PyMethod_Self(PyObject *meth)

   *meth* が束縛メソッドの場合には、メソッドに関連付けられているインスタンスを返します。それ以外の場合には *NULL* を返します。


.. c:function:: PyObject* PyMethod_GET_SELF(PyObject *meth)

   :c:func:`PyMethod_Self` のマクロ版で、エラーチェックを行いません。


.. c:function:: int PyMethod_ClearFreeList()

   free list をクリアします。
   解放された要素数を返します。

   .. versionadded:: 2.6
