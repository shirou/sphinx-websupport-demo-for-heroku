.. highlightlang:: c

.. _listobjects:

List Objects
------------

.. index:: object: list


.. c:type:: PyListObject

   この :c:type:`PyObject` のサブタイプは Python のリストオブジェクトを表現します。


.. c:var:: PyTypeObject PyList_Type

   この :c:type:`PyTypeObject` のインスタンスは Python のタプル型を表現します。
   これは Python レイヤにおける ``list`` と同じオブジェクトです。


.. c:function:: int PyList_Check(PyObject *p)

   引数が :c:type:`PyListObject` である場合に真を返します。


.. c:function:: PyObject* PyList_New(Py_ssize_t len)

   サイズが *len* 新たなリストオブジェクトを返します。失敗すると *NULL* を返します。

   .. note::

      *len* が0より大きいとき、返されるリストオブジェクトの要素には ``NULL`` がセットされています。
      なので、 :c:func:`PyList_SetItem` で本当にオブジェクトをセットする
      までは、Pythonコードにこのオブジェクトを渡したり、 :c:func:`PySequence_SetItem` のような抽象APIを利用してはいけません。

   .. versionchanged:: 2.5
      この関数は以前は *len* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_ssize_t PyList_Size(PyObject *list)

   .. index:: builtin: len

   リストオブジェクト *list* の長さを返します;  リストオブジェクトにおける ``len(list)`` と同じです。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_ssize_t PyList_GET_SIZE(PyObject *list)

   マクロ形式でできた :c:func:`PyList_Size` で、エラーチェックをしません。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyList_GetItem(PyObject *list, Py_ssize_t index)

   *list* の指すリストオブジェクト内の、位置 *index* にあるオブジェクトを返します。
   位置は正である必要があり、リスト終端からのインデックスはサポートされていません。
   *index* が範囲を超えている場合、 *NULL* を返して :exc:`IndexError` 例外をセットします。

   .. versionchanged:: 2.5
      この関数は以前は *index* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyList_GET_ITEM(PyObject *list, Py_ssize_t i)

   マクロ形式でできた :c:func:`PyList_GetItem` で、エラーチェックをしません。

   .. versionchanged:: 2.5
      この関数は以前は *i* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyList_SetItem(PyObject *list, Py_ssize_t index, PyObject *item)

   リストオブジェクト内の位置 *index* に、オブジェクト *item* を挿入します。
   成功した場合には ``0`` を返し、失敗すると ``-1`` を返します。

   .. note::

      この関数は *item* への参照を "盗み取り" ます。また、変更先のインデクスにすでに別の要素が入っている場合、その要素に対する参照を放棄します。

   .. versionchanged:: 2.5
      この関数は以前は *index* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: void PyList_SET_ITEM(PyObject *list, Py_ssize_t i, PyObject *o)

   :c:func:`PyList_SetItem` をマクロによる実装で、エラーチェックを行いません。
   このマクロは、新たなリストのまだ要素を入れたことのない位置に要素を入れるときにのみ使います。

   .. note::

      このマクロは *item* への参照を "盗み取り" ます。また、 :c:func:`PyList_SetItem` と違って、要素の置き換えが生じても
      置き換えられるオブジェクトへの参照を放棄 *しません* ; その結果、 *list* 中の位置 *i* で参照されていたオブジェクト
      がメモリリークを引き起こします。

   .. versionchanged:: 2.5
      この関数は以前は *i* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyList_Insert(PyObject *list, Py_ssize_t index, PyObject *item)

   要素 *item* をインデックス *index* の前に挿入します。成功すると ``0`` を返します。
   失敗すると ``-1`` を返し、例外をセットします。
   ``list.insert(index, item)`` に類似した機能です。

   .. versionchanged:: 2.5
      この関数は以前は *index* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyList_Append(PyObject *list, PyObject *item)

   オブジェクト *item* を *list* の末尾に追加します。成功すると ``0`` を返します; 失敗すると ``-1`` を返し、
   例外をセットします。 ``list.append(item)``  に類似した機能です。


.. c:function:: PyObject* PyList_GetSlice(PyObject *list, Py_ssize_t low, Py_ssize_t high)

   *list* 内の、 *low* から *high* の *間の* オブジェクトからなるリストを返します。
   失敗すると *NULL* を返し、例外をセットします。
   ``list[low:high]`` に類似した機能です。
   ただし、 Python のスライスにある負のインデックスはサポートされていません。

   .. versionchanged:: 2.5
      この関数は以前は *low*, *high* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyList_SetSlice(PyObject *list, Py_ssize_t low, Py_ssize_t high, PyObject *itemlist)

   *list* 内の、 *low* から *high* の間のオブジェクトを、 *itemlist* の内容にします。 ``list[low:high] =
   itemlist`` と類似の機能です。 *itemlist* は *NULL* でもよく、空リストの代入 (指定スライスの削除) になります。
   成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。
   Python のスライスにある負のインデックスはサポートされていません。

   .. versionchanged:: 2.5
      この関数は以前は *low*, *high* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyList_Sort(PyObject *list)

   *list* の内容をインプレースでソートします。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。
   ``list.sort()`` と同じです。


.. c:function:: int PyList_Reverse(PyObject *list)

   *list* の要素をインプレースで反転します。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。
   ``list.reverse()`` と同じです。


.. c:function:: PyObject* PyList_AsTuple(PyObject *list)

   .. index:: builtin: tuple

   *list* の内容が入った新たなタプルオブジェクトを返します; ``tuple(list)`` と同じです。


