.. highlightlang:: c

.. _gen-objects:

ジェネレータオブジェクト
------------------------

ジェネレータ (generator) オブジェクトは、 Python がジェネレータ型イテレータを実装するために使っているオブジェクトです。
ジェネレータオブジェクトは、通常、 :c:func:`PyGen_New` で明示的に生成されることはなく、値を逐次生成するような関数に対してイテレーションを
行うときに生成されます。

.. % Generator Objects


.. c:type:: PyGenObject

   ジェネレータオブジェクトに使われている C 構造体です。


.. c:var:: PyTypeObject PyGen_Type

   ジェネレータオブジェクトに対応する型オブジェクトです。


.. c:function:: int PyGen_Check(ob)

   *ob* がジェネレータオブジェクトの場合に真を返します。 *ob* が *NULL* であってはなりません。


.. c:function:: int PyGen_CheckExact(ob)

   *ob* の型が *PyGen_Type* の場合に真を返します。 *ob* が *NULL* であってはなりません。


.. c:function:: PyObject* PyGen_New(PyFrameObject *frame)

   *frame* オブジェクトに基づいて新たなジェネレータオブジェクトを生成して返します。この関数は *frame* への参照を盗みます。パラメタが
   *NULL* であってはなりません。

