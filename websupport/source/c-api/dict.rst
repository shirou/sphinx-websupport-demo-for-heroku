.. highlightlang:: c

.. _dictobjects:

辞書オブジェクト (dictionary object)
------------------------------------

.. index:: object: dictionary


.. c:type:: PyDictObject

   この :c:type:`PyObject` のサブタイプは Python の辞書オブジェクトを表現します。


.. c:var:: PyTypeObject PyDict_Type

   .. index::
      single: DictType (in module types)
      single: DictionaryType (in module types)

   この :c:type:`PyTypeObject` のインスタンスは Python の辞書を表現します。このオブジェクトは、Python プログラムには
   ``dict`` および ``types.DictType`` として公開されています。


.. c:function:: int PyDict_Check(PyObject *p)

   引数が :c:type:`PyDictObject` のときに真を返します。


.. c:function:: int PyDict_CheckExact(PyObject *p)

   *p* が辞書型オブジェクトであり、かつ辞書型のサブクラスのインスタンスでない場合に真を返します。

   .. versionadded:: 2.4


.. c:function:: PyObject* PyDict_New()

   *p* が辞書型オブジェクトで、かつ辞書型のサブタイプのインスタンスでない場合に真を返します。


.. c:function:: PyObject* PyDictProxy_New(PyObject *dict)

   あるマップ型オブジェクトに対して、読み出し専用に制限されたプロキシオブジェクト (proxy object) を返します。通常、この関数は動的でないクラス型
   (non-dynamic class type) のクラス辞書を変更させないためにプロキシを作成するために使われます。

   .. versionadded:: 2.2


.. c:function:: void PyDict_Clear(PyObject *p)

   現在辞書に入っている全てのキーと値のペアを除去して空にします。


.. c:function:: int PyDict_Contains(PyObject *p, PyObject *key)

   辞書 *p* に *key* が入っているか判定します。 *p* の要素が *key* に一致した場合は ``1`` を返し、それ以外の場合には ``0``
   を返します。エラーの場合 ``-1`` を返します。この関数は Python の式 ``key in p`` と等価です。

   .. versionadded:: 2.4


.. c:function:: PyObject* PyDict_Copy(PyObject *p)

   *p* と同じキーと値のペアが入った新たな辞書を返します。

   .. versionadded:: 1.6


.. c:function:: int PyDict_SetItem(PyObject *p, PyObject *key, PyObject *val)

   辞書 *p* に、 *key* をキーとして値 *value* を挿入します。
   *key* はハッシュ可能(:term:`hashable`)でなければなりません; ハッシュ可能でない場合、
   :exc:`TypeError` を送出します。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。


.. c:function:: int PyDict_SetItemString(PyObject *p, const char *key, PyObject *val)

   .. index:: single: PyString_FromString()

   辞書 *p* に、 *key* をキーとして値 *value* を挿入します。 *key* は :c:type:`char\*` 型でなければなりません。
   キーオブジェクトは ``PyString_FromString(key)`` で生成されます。成功した場合には ``0`` を、失敗した場合には ``-1``
   を返します。


.. c:function:: int PyDict_DelItem(PyObject *p, PyObject *key)

   辞書 *p* から *key* をキーとするエントリを除去します。 *key* はハッシュ可能でなければなりません;  ハッシュ可能でない場合、
   :exc:`TypeError` を送出します。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。


.. c:function:: int PyDict_DelItemString(PyObject *p, char *key)

   辞書 *p* から文字列 *key* をキーとするエントリを除去します。成功した場合には ``0`` を、失敗した場合には ``-1`` を返します。


.. c:function:: PyObject* PyDict_GetItem(PyObject *p, PyObject *key)

   辞書 *p* 内で *key* をキーとするオブジェクトを返します。キー *key* が存在しない場合には *NULL* を返しますが、例外をセット
   *しません* 。


.. c:function:: PyObject* PyDict_GetItemString(PyObject *p, const char *key)

   :c:func:`PyDict_GetItem` と同じですが、 *key* は :c:type:`PyObject\*` ではなく :c:type:`char\*`
   で指定します。


.. c:function:: PyObject* PyDict_Items(PyObject *p)

   辞書オブジェクトのメソッド :meth:`item` のように、辞書内の全ての要素対が入った :c:type:`PyListObject` を返します。
   (:meth:`items` については Python ライブラリリファレンス (XXX reference: ../lib/lib.html) を
   参照してください。)


.. c:function:: PyObject* PyDict_Keys(PyObject *p)

   辞書オブジェクトのメソッド :meth:`keys` のように、辞書内の全てのキーが入った :c:type:`PyListObject` を返します。
   (:meth:`keys` については Python ライブラリリファレンス (XXX reference: ../lib/lib.html) を
   参照してください。)


.. c:function:: PyObject* PyDict_Values(PyObject *p)

   辞書オブジェクトのメソッド :meth:`values` のように、辞書内の全ての値が入った :c:type:`PyListObject` を返します。
   (:meth:`values` については Python ライブラリリファレンス (XXX reference: ../lib/lib.html) を
   参照してください。)


.. c:function:: Py_ssize_t PyDict_Size(PyObject *p)

   .. index:: builtin: len

   辞書内の要素の数を返します。辞書に対して ``len(p)`` を実行するのと同じです。

   .. versionchanged:: 2.5
      この関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyDict_Next(PyObject *p, Py_ssize_t *ppos, PyObject **pkey, PyObject **pvalue)

   辞書 *p* 内の全てのキー/値のペアにわたる反復処理を行います。
   *ppos* が参照している :c:type:`Py_ssize_t` 型は、この関数で反復処理を開始する際に、
   最初に関数を呼び出すよりも前に ``0`` に初期化しておかなければなりません;
   この関数は辞書内の各ペアを取り上げるごとに真を返し、
   全てのペアを取り上げたことが分かると偽を返します。
   パラメタ *pkey* および *pvalue* には、それぞれ辞書の各々のキーと値を
   指すポインタか、または *NULL* が入ります。
   この関数から返される参照はすべて借りた参照になります。
   反復処理中に *ppos* を変更してはなりません。この値は内部的な辞書構造体の
   オフセットを表現しており、構造体はスパースなので、オフセットの値に一貫性が
   ないためです。

   以下に例を示します::

      PyObject *key, *value;
      Py_ssize_t pos = 0;

      while (PyDict_Next(self->dict, &pos, &key, &value)) {
          /* 取り出した値で何らかの処理を行う... */
          ...
      }

   反復処理中に辞書 *p* を変更してはなりません。 (Python 2.1 からは)
   辞書を反復処理する際に、キーに対応する値を変更しても大丈夫になりましたが、
   キーの集合を変更しないことが前提です。以下に例を示します::

      PyObject *key, *value;
      Py_ssize_t pos = 0;

      while (PyDict_Next(self->dict, &pos, &key, &value)) {
          int i = PyInt_AS_LONG(value) + 1;
          PyObject *o = PyInt_FromLong(i);
          if (o == NULL)
              return -1;
          if (PyDict_SetItem(self->dict, key, o) < 0) {
              Py_DECREF(o);
              return -1;
          }
          Py_DECREF(o);
      }

   .. versionchanged:: 2.5
      この関数は以前は *ppos* の型に :c:type:`int *` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: int PyDict_Merge(PyObject *a, PyObject *b, int override)

   マップ型オブジェクト *b* の全ての要素にわたって、反復的にキー/値のペアを辞書 *a* に追加します。 *b*
   は辞書か、 :c:func:`PyMapping_Keys` または :c:func:`PyObject_GetItem` をサポートする何らかのオブジェクト
   にできます。 *override* が真ならば、 *a* のキーと一致するキーが *b* にある際に、既存のペアを置き換えます。それ以外の場合は、 *b*
   のキーに一致するキーが *a* にないときのみ追加を行います。成功した場合には ``0`` を返し、例外が送出された場合には ``-1`` を返します。

   .. versionadded:: 2.2


.. c:function:: int PyDict_Update(PyObject *a, PyObject *b)

   C で表せば ``PyDict_Merge(a, b, 1)`` と同じ、 Python で表せば ``a.update(b)`` と同じです。成功した場合には
   ``0`` を返し、例外が送出された場合には ``-1`` を返します。

   .. versionadded:: 2.2


.. c:function:: int PyDict_MergeFromSeq2(PyObject *a, PyObject *seq2, int override)

   *seq2* 内のキー/値ペアを使って、辞書 *a* の内容を更新したり統合したりします。 *seq2* は、キー/値のペアとみなせる長さ 2 の
   反復可能オブジェクト(iterable object) を生成する反復可能オブジェクトでなければなりません。重複するキーが存在する場合、 *override*
   が真ならば先に出現したキーを使い、そうでない場合は後に出現したキーを使います。成功した場合には ``0`` を返し、例外が送出された場合には ``-1``
   を返します。

   (戻り値以外は) 等価な Python コードを書くと、以下のようになります::

      def PyDict_MergeFromSeq2(a, seq2, override):
          for key, value in seq2:
              if override or key not in a:
                  a[key] = value

   .. versionadded:: 2.2

