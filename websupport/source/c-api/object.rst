.. highlightlang:: c

.. _object:

オブジェクトプロトコル (object protocol)
========================================


.. c:function:: int PyObject_Print(PyObject *o, FILE *fp, int flags)

   オブジェクト *o* をファイル *fp* に出力します。失敗すると ``-1`` を返します。 *flags*
   引数は何らかの出力オプションを有効にする際に使います。現在サポートされている唯一のオプションは :const:`Py_PRINT_RAW` です;
   このオプションを指定すると、 :func:`repr` の代わりに :func:`str` を使ってオブジェクトを書き込みます。


.. c:function:: int PyObject_HasAttr(PyObject *o, PyObject *attr_name)

   *o* が属性 *attr_name* を持つときに ``1`` を、それ以外のときに ``0`` を返します。
   この関数は Python の式
   ``hasattr(o, attr_name)`` と同じです。この関数は常に成功します。

.. c:function:: int PyObject_HasAttrString(PyObject *o, const char *attr_name)

   *o* が属性 *attr_name* を持つときに ``1`` を、それ以外のときに ``0`` を返します。この関数は Python の式
   ``hasattr(o, attr_name)`` と同じです。この関数は常に成功します。


.. c:function:: PyObject* PyObject_GetAttr(PyObject *o, PyObject *attr_name)

   オブジェクト *o* から、名前 *attr_name* の属性を取得します。
   成功すると属性値を返し失敗すると *NULL* を返します。この関数は
   Python の式 ``o.attr_name`` と同じです。


.. c:function:: PyObject* PyObject_GetAttrString(PyObject *o, const char *attr_name)

   オブジェクト *o* から、名前 *attr_name* の属性を取得します。成功すると属性値を返し失敗すると *NULL* を返します。この関数は
   Python の式 ``o.attr_name`` と同じです。


.. c:function:: PyObject* PyObject_GenericGetAttr(PyObject *o, PyObject *name)

   汎用の属性取得関数で、 type オブジェクトの ``tp_getattro`` スロットに
   置かれることを意図されています。
   この関数は、オブジェクトのMRO中のクラスの辞書にあるディスクリプタと、オブジェクトの
   :attr:`__dict__` (があれば)に格納されている属性を検索します。
   :ref:`descriptors` で説明されているように、データディスクリプタはインスタンス属性より
   優先され、非データディスクリプタは後回しにされます。
   見つからなかった場合は :exc:`AttributeError` を発生させます。


.. c:function:: int PyObject_SetAttr(PyObject *o, PyObject *attr_name, PyObject *v)

   オブジェクト *o* の *attr_name* という名の属性に、値 *v* を設定します。失敗すると ``-1`` を返します。この関数は Python
   の式 ``o.attr_name = v`` と同じです。


.. c:function:: int PyObject_SetAttrString(PyObject *o, const char *attr_name, PyObject *v)

   オブジェクト *o* の *attr_name* という名の属性に、値 *v* を設定します。失敗すると ``-1`` を返します。この関数は Python
   の式 ``o.attr_name = v`` と同じです。


.. c:function:: int PyObject_GenericSetAttr(PyObject *o, PyObject *name, PyObject *value)

   汎用の属性設定関数で、typeオブジェクトの ``tp_setattro`` スロットに
   置かれることを意図しています。
   オブジェクトのMROにあるクラス列の辞書からデータディスクリプタを探し、
   見つかればインスタンス辞書への格納よりもデータディスクリプタを優先します。
   見つからなければ、オブジェクトの :attr:`__dict__` (があれば) に属性を設定します。
   失敗した場合、 :exc:`AttributeError` を発生させて ``-1`` を返します。


.. c:function:: int PyObject_DelAttr(PyObject *o, PyObject *attr_name)

   オブジェクト *o* の *attr_name* という名の属性を削除します。失敗すると ``-1`` を返します。この関数は Python の文 ``del
   o.attr_name`` と同じです。


.. c:function:: int PyObject_DelAttrString(PyObject *o, const char *attr_name)

   オブジェクト *o* の *attr_name* という名の属性を削除します。失敗すると ``-1`` を返します。この関数は Python の文 ``del
   o.attr_name`` と同じです。


.. c:function:: PyObject* PyObject_RichCompare(PyObject *o1, PyObject *o2, int opid)

   *o1* と *o2* を *opid* に指定した演算によって比較します。 *opid* は :const:`Py_LT`, :const:`Py_LE`,
   :const:`Py_EQ`, :const:`Py_NE`, :const:`Py_GT`, または :const:`Py_GE`,
   のいずれかでなければならず、それぞれ ``<``, ``<=``, ``==``, ``!=``, ``>``, および ``>=`` に対応します。
   この関数は Python の式 ``o1 op o2`` と同じで、 ``op`` が *opid* に対応する演算子です。
   成功すると比較結果の値を返し失敗すると *NULL* を返します。


.. c:function:: int PyObject_RichCompareBool(PyObject *o1, PyObject *o2, int opid)

   *o1* と *o2* を *opid* に指定した演算によって比較します。 *opid* は :const:`Py_LT`, :const:`Py_LE`,
   :const:`Py_EQ`, :const:`Py_NE`, :const:`Py_GT`, または :const:`Py_GE`,
   のいずれかでなければならず、それぞれ ``<``, ``<=``, ``==``, ``!=``, ``>``, および ``>=`` に対応します。
   比較結果が真ならば ``1`` を、偽ならば ``0`` を、エラーが発生すると ``-1`` を返します。この関数は Python の式
   ``o1 op o2`` と同じで、 ``op`` が *opid* に対応する演算子です。

.. note::
   *o1* と *o2* が同一のオブジェクトである場合、 :c:func:`PyObject_RichCompareBool`
   は :const:`Py_EQ` に対して常に ``1`` を返し、 :const:`Py_NE` に対して常に ``0``
   を返します。

.. c:function:: int PyObject_Cmp(PyObject *o1, PyObject *o2, int *result)

   .. index:: builtin: cmp

   *o1* と *o2* の値を比較します。このとき *o1* が比較ルーチンを持っていればそれを使い、なければ *o2* のルーチンを使います。比較結果は
   *result* に返されます。失敗すると ``-1`` を返します。 Python 文 ``result = cmp(o1, o2)`` と同じです。


.. c:function:: int PyObject_Compare(PyObject *o1, PyObject *o2)

   .. index::
      builtin: cmp
      builtin: cmp

   *o1* と *o2* の値を比較します。このとき *o1* が比較ルーチンを持っていればそれを使い、なければ *o2* のルーチンを使います。比較結果は
   *result* に返されます。失敗すると ``-1`` を返します。 Python 文 ``result = cmp(o1, o2)``
   と同じです。成功すると比較結果を返します。エラーが生じた場合の戻り値は未定義です; :c:func:`PyErr_Occurred` を使ってエラー検出を
   行って下さい。Python 式 ``cmp(o1,  o2)`` と同じです。


.. c:function:: PyObject* PyObject_Repr(PyObject *o)

   .. index:: builtin: repr

   *o* の文字列表現を計算します。成功すると文字列表現を返し、失敗すると *NULL* を返します。Python 式 ``repr(o)``
   と同じです。この関数は組み込み関数 :func:`repr` や逆クオート表記の処理で呼び出されます。


.. c:function:: PyObject* PyObject_Str(PyObject *o)

   .. index:: builtin: str

   *o* の文字列表現を計算します。成功すると文字列表現を返し、失敗すると *NULL* を返します。Python 式 ``str(o)``
   と同じです。この関数は組み込み関数 :func:`str` や :keyword:`print` 文の処理で呼び出されます。


.. c:function:: PyObject* PyObject_Bytes(PyObject *o)

   .. index:: builtin: bytes

   *o* オブジェクトの bytes 表現を計算します。
   2.x では、単に :c:func:`PyObject_Str` のエイリアスです。


.. c:function:: PyObject* PyObject_Unicode(PyObject *o)

   .. index:: builtin: unicode

   *o* の Unicode 文字列表現を計算します。成功すると Unicode 文字列表現を返し失敗すると *NULL* を返します。 Python
   式 ``unicode(o)`` と同じです。この関数は組み込み関数 :func:`unicode` の処理で呼び出されます。


.. c:function:: int PyObject_IsInstance(PyObject *inst, PyObject *cls)

   *inst* が *cls* のインスタンスか、 *cls* のサブクラスのインスタンスの場合に ``-1`` を返し、そうでなければ ``0`` を
   返します。エラーの時には ``-1`` を返し、例外をセットします。 *cls* がクラスオブジェクトではなく型オブジェクトの場合、
   :c:func:`PyObject_IsInstance` は *inst* が *cls* であるときに ``1`` を返します。 *cls*
   をタプルで指定した場合、 *cls* に指定した全てのエントリについてチェックを行います。少なくとも一つのエントリに対するチェックが ``1``
   を返せば結果は ``1`` になり、そうでなければ ``0`` になります。 *inst* がクラスインスタンスでなく、かつ *cls* が
   型オブジェクトでもクラスオブジェクトでもタプルでもない場合、 *inst* には :attr:`__class__` 属性がなくてはなりません ---
   この場合、 :attr:`__class__` 属性の値と、 *cls* の値の間のクラス関係を、関数の戻り値を決定するのに使います。

   .. versionadded:: 2.1

   .. versionchanged:: 2.2
      二つ目の引数にタプルのサポートを追加しました。.

サブクラスの決定はかなり正攻法で行いますが、クラスシステムの拡張を実装する人たちに知っておいて欲しいちょっとした問題点があります。 :class:`A` と
:class:`B` がクラスオブジェクトの場合、 :class:`B` が :class:`A` のサブクラスとなるのは、 :class:`B` が
:class:`A` を直接的あるいは間接的に継承 (inherit) している場合です。両方がクラスオブジェクトでない場合、二つのオブジェクト間の
クラス関係を決めるには、より汎用の機構を使います。 *B* が *A* のサブクラスであるか調べたとき、 *A* が *B*
と等しければ、 :c:func:`PyObject_IsSubclass` は真を返します。 *A* および *B* が異なるオブジェクトなら、 *B* の
:attr:`__bases__` 属性から深さ優先探索 (depth-first search)で *A* を探索します ---
オブジェクトに :attr:`__bases__` があるだけで、この決定法を適用する条件を満たしているとみなされます。


.. c:function:: int PyObject_IsSubclass(PyObject *derived, PyObject *cls)

   クラス *derived* が *cls* と同じクラスか、 *cls* の派生クラスの場合に ``1`` を返し、それ以外の場合には ``0`` を
   返します。エラーが生じると ``-1`` を返します。  *cls* をタプルで指定した場合、 *cls* に指定した全てのエントリについてチェックを行います。
   少なくとも一つのエントリに対するチェックが ``1`` を返せば結果は ``1`` になり、そうでなければ ``0`` になります。 *derived* または
   *cls* のいずれかが実際のクラスオブジェクト (あるいはタプル) でない場合、上で述べた汎用アルゴリズムを使います。

   .. versionadded:: 2.1

   .. versionchanged:: 2.3
      以前の Python のバージョンは、二つ目の引数にタプルをサポートしていませんでした.


.. c:function:: int PyCallable_Check(PyObject *o)

   オブジェクト *o* が呼び出し可能オブジェクトかどうか調べます。オブジェクトが呼び出し可能であるときに ``1`` を返し、そうでないときには ``0``
   を返します。この関数呼び出しは常に成功します。


.. c:function:: PyObject* PyObject_Call(PyObject *callable_object, PyObject *args, PyObject *kw)

   .. index:: builtin: apply

   呼び出し可能な Python オブジェクト *callable_object* をタプルで指定された引数 *args* および辞書で指定された名前つき引数
   (named argument) *kw* とともに呼び出します。名前つき引数を必要としない場合、 *kw* を *NULL* にしてもかまいません。
   *args* は *NULL* であってはなりません。引数が全く必要ない場合には空のタプルを使ってください。
   成功すると呼び出し結果として得られたオブジェクトを返し、失敗すると *NULL* を返します。 Python の式
   ``apply(callable_object, args, kw)`` あるいは ``callable_object(*args, **kw)``
   と同じです。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyObject_CallObject(PyObject *callable_object, PyObject *args)

   .. index:: builtin: apply

   呼び出し可能な Python オブジェクト *callable_object* をタプルで指定された引数 *args* とともに呼び出します。  引数を
   必要としない場合、 *args* を *NULL* にしてもかまいません。成功すると呼び出し結果として得られたオブジェクトを返し、失敗すると *NULL*
   を返します。 Python の式 ``apply(callable_object, args)``  あるいは
   ``callable_object(*args)`` と同じです。


.. c:function:: PyObject* PyObject_CallFunction(PyObject *callable, char *format, ...)

   .. index:: builtin: apply

   呼び出し可能な Python オブジェクト *callable_object* を可変数個の C 引数とともに呼び出します。C 引数は
   :c:func:`Py_BuildValue` 形式のフォーマット文字列を使って記述します。 *format*
   は *NULL* にしてもよく、与える引数がないことを表します。成功すると呼び出し結果として得られたオブジェクトを返し、失敗すると *NULL* を返します。
   Python の式 ``apply(callable, args)`` あるいは ``callable(*args)`` と同じです。
   もしも、 :c:type:`PyObject \*` args だけを引数に渡す場合は、 :c:func:`PyObject_CallFunctionObjArgs`
   がより速い方法であることを覚えておいてください。


.. c:function:: PyObject* PyObject_CallMethod(PyObject *o, char *method, char *format, ...)

   オブジェクト *o* の *method* という名前のメソッドを、可変数個の C 引数とともに呼び出します。C 引数はタプルを生成するような
   :c:func:`Py_BuildValue` 形式のフォーマット文字列を使って記述します。 *format*
   は *NULL* にしてもよく、与える引数がないことを表します。成功すると呼び出し結果として得られたオブジェクトを返し、失敗すると *NULL* を返します。
   Python の式 ``o.method(args)`` と同じです。もしも、 :c:type:`PyObject \*` args
   だけを引数に渡す場合は、 :c:func:`PyObject_CallMethodObjArgs` がより速い方法であることを覚えておいてください。


.. c:function:: PyObject* PyObject_CallFunctionObjArgs(PyObject *callable, ..., NULL)

   呼び出し可能な Python オブジェクト *callable_object* を可変数個の :c:type:`PyObject\*`
   引数とともに呼び出します。引数列は末尾に *NULL* がついた可変数個のパラメタとして与えます。
   成功すると呼び出し結果として得られたオブジェクトを返し失敗すると *NULL* を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyObject_CallMethodObjArgs(PyObject *o, PyObject *name, ..., NULL)

   オブジェクト *o* のメソッドを呼び出します、メソッド名は Python 文字列オブジェクト *name* で与えます。可変数個の
   :c:type:`PyObject\*` 引数と共に呼び出されます. 引数列は末尾に *NULL* がついた可変数個のパラメタとして与えます。
   成功すると呼び出し結果として得られたオブジェクトを返し失敗すると *NULL* を返します。

   .. versionadded:: 2.2


.. c:function:: long PyObject_Hash(PyObject *o)

   .. index:: builtin: hash

   オブジェクト *o* のハッシュ値を計算して返します。失敗すると ``-1`` を返します。 Python の式 ``hash(o)`` と同じです。


.. c:function:: long PyObject_HashNotImplemented(PyObject *o)

   ``type(o)`` がハッシュ不可能であることを示す :exc:`TypeError` を設定し、
   ``-1`` を返します。
   この関数は ``tp_hash`` スロットに格納されたときには特別な扱いを受け、
   その type がハッシュ不可能であることをインタプリタに明示的に示します。

   .. versionadded:: 2.6


.. c:function:: int PyObject_IsTrue(PyObject *o)

   *o* が真を表すとみなせる場合には ``1`` を、そうでないときには ``0`` を返します。   Python の式 ``not not o``
   と同じです。失敗すると ``-1`` を返します。


.. c:function:: int PyObject_Not(PyObject *o)

   *o* が真を表すとみなせる場合には ``0`` を、そうでないときには ``1`` を返します。   Python の式 ``not o`` と同じです。
   失敗すると ``-1`` を返します。


.. c:function:: PyObject* PyObject_Type(PyObject *o)

   .. index:: builtin: type

   *o* が *NULL* でない場合、オブジェクト *o* のオブジェクト型に相当する型オブジェクトを返します。失敗すると :exc:`SystemError`
   を送出して *NULL* を返します。 Python の式 ``type(o)`` と同じです。  この関数は戻り値の参照カウントをインクリメントします。
   参照カウントのインクリメントが必要でない限り、広く使われていて :c:type:`PyTypeObject\*` 型のポインタを返す表記法
   ``o->ob_type`` の代わりに使う理由は全くありません。


.. c:function:: int PyObject_TypeCheck(PyObject *o, PyTypeObject *type)

   オブジェクト *o* が、 *type* か *type* のサブタイプであるときに真を返します。どちらのパラメタも *NULL* であってはなりません。

   .. versionadded:: 2.2


.. c:function:: Py_ssize_t PyObject_Length(PyObject *o)
               Py_ssize_t PyObject_Size(PyObject *o)

   .. index:: builtin: len

   *o* の長さを返します。オブジェクト *o* がシーケンス型プロトコルとマップ型プロトコルの両方を提供している場合、シーケンスとしての長さを
   返します。エラーが生じると ``-1`` を返します。 Python の式 ``len(o)`` と同じです。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` 型を返していました。
      この変更により、 64bit システムを適切にサポートするためにはコードの修正が必要になります。

.. c:function:: PyObject* PyObject_GetItem(PyObject *o, PyObject *key)

   成功するとオブジェクト *key* に対応する *o* の要素を返し、失敗すると *NULL* を返します。  Python の式 ``o[key]``
   と同じです。


.. c:function:: int PyObject_SetItem(PyObject *o, PyObject *key, PyObject *v)

   オブジェクト *key* を値 *v* に対応付けます。失敗すると ``-1`` を返します。 Python の文 ``o[key] = v`` と同じです。


.. c:function:: int PyObject_DelItem(PyObject *o, PyObject *key)

   オブジェクト *o* から *key* に対する対応付けを削除します。失敗すると ``-1`` を返します。 Python の文 ``del o[key]``
   と同じです。


.. c:function:: int PyObject_AsFileDescriptor(PyObject *o)

   Python オブジェクトからファイル記述子を取り出します。オブジェクトが整数か長整数なら、その値を返します。 (長)整数でない場合、オブジェクトに
   :meth:`fileno` メソッドがあれば呼び出します; この場合、 :meth:`fileno` メソッドは
   整数または長整数をファイル記述子の値として返さなければなりません。失敗すると ``-1`` を返します。


.. c:function:: PyObject* PyObject_Dir(PyObject *o)

   この関数は Python の式 ``dir(o)`` と同じで、オブジェクトの変数名に割り当てている文字列からなるリスト (空の場合もあります)
   を返します。エラーの場合には *NULL* を返します。引数を *NULL* にすると、Python における ``dir()``
   と同様に、現在のローカルな名前を返します; この場合、アクティブな実行フレームがなければ *NULL* を返しますが、
   :c:func:`PyErr_Occurred` は偽を返します。


.. c:function:: PyObject* PyObject_GetIter(PyObject *o)

   Python の式 ``iter(o)`` と同じです。引数にとったオブジェクトに対する新たなイテレータか、
   オブジェクトがすでにイテレータの場合にはオブジェクト自身を返します。オブジェクトが反復処理不可能であった場合には :exc:`TypeError` を送出して
   *NULL* を返します。


