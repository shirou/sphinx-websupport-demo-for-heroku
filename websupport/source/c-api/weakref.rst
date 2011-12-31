.. highlightlang:: c

.. _weakrefobjects:

弱参照オブジェクト (weak reference object)
------------------------------------------

Python は *弱参照* を第一級オブジェクト (first-class object)
としてサポートします。弱参照を直接実装する二種類の固有のオブジェクト型があります。第一は単純な参照オブジェクトで、第二はオリジナルの
オブジェクトに対して可能な限りプロキシとして振舞うオブジェクトです。


.. c:function:: int PyWeakref_Check(ob)

   *ob* が参照オブジェクトかプロキシオブジェクトの場合に真を返します。

   .. versionadded:: 2.2


.. c:function:: int PyWeakref_CheckRef(ob)

   *ob* が参照オブジェクトの場合に真を返します。

   .. versionadded:: 2.2


.. c:function:: int PyWeakref_CheckProxy(ob)

   *ob* がプロキシオブジェクトの場合に真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyWeakref_NewRef(PyObject *ob, PyObject *callback)

   *ob* に対する弱参照オブジェクトを返します。この関数は常に新たな参照を返しますが、必ずしも新たなオブジェクトを作る保証はありません;
   既存の参照オブジェクトが返されることもあります。第二のパラメタ *callback* は呼び出し可能オブジェクトで、 *ob*
   がガーベジコレクションされた際に通知を受け取ります; *callback* は弱参照オブジェクト自体を単一のパラメタとして受け取ります。 *callback*
   は ``None`` や *NULL* にしてもかまいません。 *ob* が弱参照できないオブジェクトの場合や、 *callback*
   が呼び出し可能オブジェクト、 ``None`` 、 *NULL* のいずれでもない場合は、 *NULL* を返して :exc:`TypeError` を送出します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyWeakref_NewProxy(PyObject *ob, PyObject *callback)

   *ob* に対する弱参照プロキシオブジェクトを返します。この関数は常に新たな参照を返しますが、必ずしも新たなオブジェクトを作る保証はありません;
   既存の参照オブジェクトが返されることもあります。第二のパラメタ *callback* は呼び出し可能オブジェクトで、 *ob*
   がガーベジコレクションされた際に通知を受け取ります; *callback* は弱参照オブジェクト自体を単一のパラメタとして受け取ります。 *callback*
   は ``None`` や *NULL* にしてもかまいません。 *ob* が弱参照できないオブジェクトの場合や、 *callback*
   が呼び出し可能オブジェクト、 ``None`` 、 *NULL* のいずれでもない場合は、 *NULL* を返して :exc:`TypeError` を送出します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyWeakref_GetObject(PyObject *ref)

   弱参照 *ref* が参照しているオブジェクトを返します。被参照オブジェクトが
   すでに存続していない場合、 :const:`Py_None` を返します。

   .. versionadded:: 2.2

   .. warning::

      この関数は参照先オブジェクトの **借り物の参照** を返します。
      そのため、そのオブジェクトを利用している間そのオブジェクトが破棄されない
      ことが判っている場合を除き、常に :c:func:`Py_INCREF` を呼び出すべきです。

.. c:function:: PyObject* PyWeakref_GET_OBJECT(PyObject *ref)

   :c:func:`PyWeakref_GetObject` に似ていますが、マクロで実装されていて、エラーチェックを行いません。

   .. versionadded:: 2.2

