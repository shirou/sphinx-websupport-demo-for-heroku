.. highlightlang:: c

.. _slice-objects:

スライスオブジェクト (slice object)
-----------------------------------


.. c:var:: PyTypeObject PySlice_Type

   .. index:: single: SliceType (in module types)

   スライスオブジェクトの型オブジェクトです。 ``slice`` や ``types.SliceType`` と同じです。


.. c:function:: int PySlice_Check(PyObject *ob)

   *ob* がスライスオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。


.. c:function:: PyObject* PySlice_New(PyObject *start, PyObject *stop, PyObject *step)

   指定した値から新たなスライスオブジェクトを返します。パラメタ *start*, *stop*, および *step* はスライスオブジェクトに
   おける同名の属性として用いられます。これらの値はいずれも *NULL* にでき、対応する値には ``None`` が使われます。新たな
   オブジェクトをアロケーションできない場合には *NULL* を返します。


.. c:function:: int PySlice_GetIndices(PySliceObject *slice, Py_ssize_t length, Py_ssize_t *start, Py_ssize_t *stop, Py_ssize_t *step)

   スライスオブジェクト *slice* における *start*, *stop*,  および *step* のインデクス値を取得します。このときシーケンスの
   長さを *length* と仮定します。 *length* よりも大きなインデクスになるとエラーとして扱います。

   成功のときには ``0`` を、エラーのときには例外をセットせずに ``-1`` を返します (ただし、指定インデクスのいずれか一つが
   :const:`None` ではなく、かつ整数に変換できなかった場合を除きます。この場合、 ``-1`` を返して例外をセットします)。

   おそらくこの関数を使う気にはならないでしょう。バージョン 2.3 以前の Python でスライスオブジェクトを使いたいのなら、
   :c:func:`PySlice_GetIndicesEx` のソースを適切に名前変更して自分の拡張モジュールのソースコード内に組み込むとよいでしょう。

   .. versionchanged:: 2.5
      この関数は以前は *length* の型に :c:type:`int` を、 *start*, *stop*, *step*
      の型に :c:type:`int *` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PySlice_GetIndicesEx(PySliceObject *slice, Py_ssize_t length, Py_ssize_t *start, Py_ssize_t *stop, Py_ssize_t *step, Py_ssize_t *slicelength)

   :c:func:`PySlice_GetIndices` の置き換えとして使える関数です。

   スライスオブジェクト *slice* における *start*, *stop*,  および *step* のインデクス値を取得します。このときシーケンスの
   長さを *length* と仮定します。スライスの長さを *slicelength* に記憶します。境界をはみだしたインデクスは、通常のスライスを扱うのと
   同じ一貫したやり方でクリップされます。

   成功のときには ``0`` を、エラーのときには例外をセットして ``-1`` を返します。

   .. versionadded:: 2.3

   .. versionchanged:: 2.5
      この関数は以前は *length* の型に :c:type:`int` を、 *start*, *stop*, *step*,
      *slicelength* の型に :c:type:`int *` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。
