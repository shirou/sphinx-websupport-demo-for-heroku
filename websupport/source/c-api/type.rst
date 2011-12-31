.. highlightlang:: c

.. _typeobjects:

型オブジェクト (type object)
----------------------------

.. index:: object: type


.. c:type:: PyTypeObject

   組み込み型を記述する際に用いられる、オブジェクトを表す C 構造体です。


.. c:var:: PyObject* PyType_Type

   .. index:: single: TypeType (in module types)

   型オブジェクト自身の型オブジェクトです; Python レイヤにおける ``type`` や ``types.TypeType`` と同じオブジェクトです。


.. c:function:: int PyType_Check(PyObject *o)

   オブジェクト *o* が型オブジェクトの場合に真を返します。標準型オブジェクトから派生したサブタイプ (subtype) のインスタンスも
   含みます。その他の場合には偽を返します。


.. c:function:: int PyType_CheckExact(PyObject *o)

   オブジェクト *o* が型オブジェクトの場合に真を返します。標準型のサブタイプの場合は含みません。その他の場合には偽を返します。

   .. versionadded:: 2.2


.. c:function:: unsigned int PyType_ClearCache()

   内部の検索キャッシュをクリアします。
   現在のバージョンタグを返します。

   .. versionadded:: 2.6


.. c:function:: void PyType_Modified(PyTypeObject *type)

   内部の検索キャッシュを、その type とすべてのサブタイプに対して無効にします。
   この関数は type の属性や基底クラス列を変更したあとに手動で呼び出さなければ
   なりません。

   .. versionadded:: 2.6


.. c:function:: int PyType_HasFeature(PyObject *o, int feature)

   型オブジェクト *o* に、型機能 *feature* が設定されている場合に真を返します。型機能は各々単一ビットのフラグで表されます。


.. c:function:: int PyType_IS_GC(PyObject *o)

   型オブジェクトが *o* が循環参照検出をサポートしている場合に真を返します; この関数は型機能フラグ :const:`Py_TPFLAGS_HAVE_GC`
   の設定状態をチェックします。

   .. versionadded:: 2.0


.. c:function:: int PyType_IsSubtype(PyTypeObject *a, PyTypeObject *b)

   *a* が *b* のサブタイプの場合に真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyType_GenericAlloc(PyTypeObject *type, Py_ssize_t nitems)

   .. versionadded:: 2.2

   .. versionchanged:: 2.5
      この関数は以前は *nitems* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyType_GenericNew(PyTypeObject *type, PyObject *args, PyObject *kwds)

   .. versionadded:: 2.2


.. c:function:: int PyType_Ready(PyTypeObject *type)

   型オブジェクトの後始末処理 (finalize) を行います。この関数は全てのオブジェクトで初期化を完了するために呼び出されなくてはなりません。
   この関数は、基底クラス型から継承したスロットを型オブジェクトに追加する役割があります。成功した場合には ``0`` を返し、エラーの場合には ``-1``
   を返して例外情報を設定します。

   .. versionadded:: 2.2

