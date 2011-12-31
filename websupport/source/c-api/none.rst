.. highlightlang:: c

.. _noneobject:

None オブジェクト
-----------------

.. index:: object: None

``None`` に対する :c:type:`PyTypeObject` は、 Python/C API では直接公開されていないので注意してください。
``None`` は単量子 (singleton) なので、オブジェクトのアイデンティティテスト (C では ``==``) を使うだけで十分だからです。
同じ理由から、 :c:func:`PyNone_Check` 関数はありません。


.. c:var:: PyObject* Py_None

   Python における ``None`` オブジェクトで、値がないことを表します。このオブジェクトにはメソッドがありません。リファレンスカウントに
   ついては、このオブジェクトも他のオブジェクトと同様に扱う必要があります。


.. c:macro:: Py_RETURN_NONE

   C 関数から :c:data:`Py_None` を戻す操作を適切に行うためのマクロです。

