.. highlightlang:: c

.. _cobjects:

Cオブジェクト (CObject)
-----------------------

.. index:: object: CObject

.. warning::

   CObject API は Python 2.7 から非推奨になりました。新しい :ref:`capsules` APIへ移行してください。


.. c:type:: PyCObject

   この :c:type:`PyObject` のサブタイプは不透明型値 (opaque value) を表現します。C 拡張モジュールが Python
   コードから不透明型値を  (:c:type:`void\*` ポインタで) 他の C コードに渡す必要があるときに便利です。正規の import
   機構を使って動的にロードされるモジュール内で定義されている C API にアクセスするために、あるモジュール内で定義されている C
   関数ポインタを別のモジュールでも利用できるようにするためによく使われます。


.. c:function:: int PyCObject_Check(PyObject *p)

   引数が :c:type:`PyCObject` の場合に真を返します。


.. c:function:: PyObject* PyCObject_FromVoidPtr(void* cobj, void (*destr)(void *))

   ``void*`` *cobj* から :c:type:`PyCObject` を生成します。関数 *destr* が *NULL*
   でない場合、オブジェクトを再利用する際に呼び出します。


.. c:function:: PyObject* PyCObject_FromVoidPtrAndDesc(void* cobj, void* desc, void (*destr)(void *, void *))

   ``void*`` *cobj* から :c:type:`PyCObject` を生成します。関数 *destr* が *NULL*
   でない場合、オブジェクトを再利用する際に呼び出します。引数 *desc* を使って、デストラクタ関数に追加のコールバックデータを渡せます。


.. c:function:: void* PyCObject_AsVoidPtr(PyObject* self)

   :c:type:`PyCObject` オブジェクト *self* を生成するのに用いたオブジェクト :c:type:`void \*` を返します。


.. c:function:: void* PyCObject_GetDesc(PyObject* self)

   :c:type:`PyCObject` オブジェクト *self* を生成するのに用いたコールバックデータ :c:type:`void \*` を返します。


.. c:function:: int PyCObject_SetVoidPtr(PyObject* self, void* cobj)

   *self* 内の void ポインタ *cobj* に設定します。 :c:type:`PyCObject` にデストラクタが関連づけられていてはなりません。
   成功すると真値を返し、失敗すると偽値を返します。

