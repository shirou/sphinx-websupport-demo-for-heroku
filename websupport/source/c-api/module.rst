.. highlightlang:: c

.. _moduleobjects:

モジュールオブジェクト (module object)
--------------------------------------

.. index:: object: module

モジュールオブジェクト固有の関数は数個しかありません。


.. c:var:: PyTypeObject PyModule_Type

   .. index:: single: ModuleType (in module types)

   この :c:type:`PyTypeObject` のインスタンスは Python のモジュールオブジェクト型を表現します。このオブジェクトは、Python
   プログラムには ``types.ModuleType``  として公開されています。


.. c:function:: int PyModule_Check(PyObject *p)

   *o* がモジュールオブジェクトかモジュールオブジェクトのサブタイプであるときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyModule_CheckExact(PyObject *p)

   *o* がモジュールオブジェクトで、かつモジュールオブジェクトのサブタイプでないときに真を返します。  :c:data:`PyModule_Type`.

   .. versionadded:: 2.2


.. c:function:: PyObject* PyModule_New(const char *name)

   .. index::
      single: __name__ (module attribute)
      single: __doc__ (module attribute)
      single: __file__ (module attribute)

   :attr:`__name__` 属性が *name* に設定された新たなモジュールオブジェクトを返します。モジュールの :attr:`__doc__`
   および :attr:`__name__` 属性だけに値が入っています; :attr:`__file__` 属性に値を入れるのは呼び出し側の責任です。


.. c:function:: PyObject* PyModule_GetDict(PyObject *module)

   .. index:: single: __dict__ (module attribute)

   *module* の名前空間を実現する辞書オブジェクトを返します; このオブジェクトはモジュールオブジェクトの :attr:`__dict__`
   と同じです。この関数が失敗することはありません。  拡張モジュールでは、この関数で得たモジュールの :attr:`__dict__`
   を直接いじるより、他の :c:func:`PyModule_\*` および :c:func:`PyObject_\*` 関数を使うよう勧めます。


.. c:function:: char* PyModule_GetName(PyObject *module)

   .. index::
      single: __name__ (module attribute)
      single: SystemError (built-in exception)

   *module* の :attr:`__name__` の値を返します。モジュールがこの属性を提供していない場合や文字列型でない場合、
   :exc:`SystemError` を送出して *NULL* を返します。


.. c:function:: char* PyModule_GetFilename(PyObject *module)

   .. index::
      single: __file__ (module attribute)
      single: SystemError (built-in exception)

   *module* をロードするために使ったファイルの名前を、 *module* の :attr:`__file__`
   属性から調べて返します。 :attr:`__file__` が定義されていない場合や文字列型でない場合、 :exc:`SystemError` を送出して
   *NULL* を返します。


.. c:function:: int PyModule_AddObject(PyObject *module, const char *name, PyObject *value)

   *module* にオブジェクトを *name* として追加します。この関数はモジュールの初期化関数から利用される便宜関数です。エラーのときには ``-1``
   を、成功したときには ``0`` を返します。

   .. versionadded:: 2.0


.. c:function:: int PyModule_AddIntConstant(PyObject *module, const char *name, long value)

   *module* に整数定数を *name* として追加します。この便宜関数はモジュールの初期化関数から利用されています。エラーのときには ``-1``
   を、成功したときには ``0`` を返します。

   .. versionadded:: 2.0


.. c:function:: int PyModule_AddStringConstant(PyObject *module, const char *name, char *value)

   *module* に文字列定数を *name* として追加します。この便宜関数はモジュールの初期化関数から利用されています。文字列 *value* は
   null 終端されていなければなりません。エラーのときには ``-1`` を、成功したときには ``0`` を返します。

   .. versionadded:: 2.0


.. c:function:: int PyModule_AddIntMacro(PyObject *module, macro)

   *module* に int 定数を追加します。名前と値は *macro* から取得されます。
   例えば、 ``PyModule_AddIntMacro(module, AF_INTE)`` とすると、 *AF_INET*
   という名前の int 型定数を *AF_INET* の値で *module* に追加します。
   エラー時には ``-1`` を、成功時には ``0`` を返します。

   .. versionadded:: 2.6

.. c:function:: int PyModule_AddStringMacro(PyObject *module, macro)

   文字列定数を *module* に追加します。

  .. versionadded:: 2.6

