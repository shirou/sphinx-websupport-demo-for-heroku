.. highlightlang:: c

.. _abstract-buffer:

古いバッファプロトコル
=======================

このセクションは Python 1.6 で導入された古いバッファプロトコルについて解説します。
このプロトコルは、 Python 2.x 系ではサポートされていますが廃止予定扱いです。
Python 3.0 から、このプロトコルの弱点や欠点を克服した新しいバッファプロトコルが導入され、
Python 2.6 へと逆移植されました。詳細は :ref:`bufferobjects` を参照してください。

.. c:function:: int PyObject_AsCharBuffer(PyObject *obj, const char **buffer, Py_ssize_t *buffer_len)

   文字ベースの入力として使える読み出し専用メモリ上の位置へのポインタを返します。
   *obj* 引数は単一セグメントからなる文字バッファインタフェースをサポートしていなければなりません。
   成功すると ``0`` を返し、 *buffer* をメモリの位置に、  *buffer_len*
   をバッファの長さに設定します。エラーの際には  ``-1`` を返し、 :exc:`TypeError` をセットします。

   .. versionadded:: 1.6

   .. versionchanged:: 2.5
      この関数は以前は *buffer_len* の型に :c:type:`int *` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyObject_AsReadBuffer(PyObject *obj, const void **buffer, Py_ssize_t *buffer_len)

   任意のデータを収めた読み出し専用のメモリ上の位置へのポインタを返します。 *obj* 引数は単一セグメントからなる読み出し可能
   バッファインタフェースをサポートしていなければなりません。成功すると ``0`` を返し、 *buffer* をメモリの位置に、  *buffer_len*
   をバッファの長さに設定します。エラーの際には  ``-1`` を返し、 :exc:`TypeError` をセットします。

   .. versionadded:: 1.6

   .. versionchanged:: 2.5
      この関数は以前は *buffer_len* の型に :c:type:`int *` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyObject_CheckReadBuffer(PyObject *o)

   *o* が単一セグメントからなる読み出し可能バッファインタフェースをサポートしている場合に ``1`` を返します。それ以外の場合には ``0``
   を返します。

   .. versionadded:: 2.2


.. c:function:: int PyObject_AsWriteBuffer(PyObject *obj, void **buffer, Py_ssize_t *buffer_len)

   書き込み可能なメモリ上の位置へのポインタを返します。 *obj*  引数は単一セグメントからなる文字バッファインタフェース
   をサポートしていなければなりません。成功すると ``0`` を返し、 *buffer* をメモリの位置に、 *buffer_len* をバッファの
   長さに設定します。エラーの際には ``-1`` を返し、 :exc:`TypeError` をセットします。

   .. versionadded:: 1.6

   .. versionchanged:: 2.5
      この関数は以前は *buffer_len* の型に :c:type:`int *` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。
