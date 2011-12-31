.. highlightlang:: c

.. _type-structs:

型オブジェクト
==============

新スタイルの型を定義する構造体: :c:type:`PyTypeObject` 構造体は、おそらく Python
オブジェクトシステムの中で最も重要な構造体の1つでしょう。型オブジェクトは
:c:func:`PyObject_\*` 系や :c:func:`PyType_\*` 系の関数で扱えますが、ほとんどの
Python アプリケーションにとって、さして面白みのある機能を提供しません。
型オブジェクトはオブジェクトがどのように振舞うかを決める基盤ですから、
インタプリタ自体や新たな型を定義する拡張モジュールでは非常に重要な存在です。

型オブジェクトは標準の型 (standard type) に比べるとかなり大きな構造体です。
各型オブジェクトは多くの値を保持しており、そのほとんどは C 関数へのポインタで、
それぞれの関数はその型の機能の小さい部分を実装しています。
この節では、型オブジェクトの各フィールドについて詳細を説明します。
各フィールドは、構造体内で出現する順番に説明されています。

Typedefs: unaryfunc, binaryfunc, ternaryfunc, inquiry, coercion, intargfunc,
intintargfunc, intobjargproc, intintobjargproc, objobjargproc, destructor,
freefunc, printfunc, getattrfunc, getattrofunc, setattrfunc, setattrofunc,
cmpfunc, reprfunc, hashfunc

:c:type:`PyTypeObject` の構造体定義は :file:`Include/object.h`
で見つけられるはずです。参照の手間を省くために、ここでは定義を繰り返します:

.. literalinclude:: ../includes/typestruct.h


型オブジェクト構造体は :c:type:`PyVarObject` 構造体を拡張したものです。
:attr:`ob_size` フィールドは、(通常 class 文が呼び出す :func:`type_new`
で生成される) 動的な型に使います。 :c:data:`PyType_Type` (メタタイプ)
は :attr:`tp_itemsize` を初期化するので注意してください。すなわち、
インスタンス (つまり型オブジェクト) には :attr:`ob_size`
フィールドがなければ *なりません* 。


.. c:member:: PyObject* PyObject._ob_next
             PyObject* PyObject._ob_prev

   これらのフィールドはマクロ  ``Py_TRACE_REFS`` が定義されている場合のみ
   存在します。 ``PyObject_HEAD_INIT`` マクロを使うと、フィールドを *NULL*
   に初期化します。静的にメモリ確保されているオブジェクトでは、これらの
   フィールドは常に *NULL* のままです。動的にメモリ確保されるオブジェクトの
   場合、これら二つのフィールドは、ヒープ上の *全ての* 存続中のオブジェクト
   からなる二重リンクリストでオブジェクトをリンクする際に使われます。
   このことは様々なデバッグ目的に利用できます; 現状では、環境変数
   :envvar:`PYTHONDUMPREFS` が設定されているときに、プログラムの実行終了時点で
   存続しているオブジェクトを出力するのが唯一の用例です。

   サブタイプはこのフィールドを継承しません。


.. c:member:: Py_ssize_t PyObject.ob_refcnt

   型オブジェクトの参照カウントで、 ``PyObject_HEAD_INIT`` はこの値を ``1``
   に初期化します。静的にメモリ確保された型オブジェクトでは、型のインスタンス
   (:attr:`ob_type` が該当する型を指しているオブジェクト) は参照をカウントする
   対象には *なりません* 。
   動的にメモリ確保される型オブジェクトの場合、インスタンスは参照カウントの
   対象に *なります* 。

   サブタイプはこのフィールドを継承しません。

   .. versionchanged:: 2.5
      このフィールドは以前は :c:type:`int` でした。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:member:: PyTypeObject* PyObject.ob_type

   型自体の型、別の言い方をするとメタタイプです。 ``PyObject_HEAD_INIT`` マクロで初期化され、通常は ``&PyType_Type``
   になります。しかし、(少なくとも) Windows で利用できる動的ロード可能な拡張モジュールでは、コンパイラは
   有効な初期化ではないと文句をつけます。そこで、ならわしとして、 ``PyObject_HEAD_INIT`` には *NULL* を渡して初期化しておき、
   他の操作を行う前にモジュールの初期化関数で明示的にこのフィールドを初期化することになっています。この操作は以下のように行います::

      Foo_Type.ob_type = &PyType_Type;

   上の操作は、該当する型のいかなるインスタンス生成よりも前にしておかねばなりません。 :c:func:`PyType_Ready` は
   :attr:`ob_type` が *NULL* かどうか調べ、 *NULL* の場合には初期化します: Python 2.2
   では、 ``&PyType_Type`` にセットします; in Python 2.2.1 およびそれ以降では基底クラスの :attr:`ob_type`
   フィールドに初期化します。 :attr:`ob_type` が非ゼロの場合、 :c:func:`PyType_Ready` はこのフィールドを変更しません。

   Python 2.2 では、サブタイプはこのフィールドを継承しません。 2.2.1 と 2.3 以降では、サブタイプはこのフィールドを継承します。


.. c:member:: Py_ssize_t PyVarObject.ob_size

   静的にメモリ確保されている型オブジェクトの場合、このフィールドはゼロに初期化されます。動的にメモリ確保されている型オブジェクトの
   場合、このフィールドは内部使用される特殊な意味を持ちます。

   サブタイプはこのフィールドを継承しません。


.. c:member:: char* PyTypeObject.tp_name

   型の名前が入っている NUL 終端された文字列へのポインタです。モジュールのグローバル変数としてアクセスできる型の場合、
   この文字列は完全なモジュール名、ドット、そして型の名前と続く文字列になります; 組み込み型の場合、ただの型の名前です。
   モジュールがあるパッケージのサブモジュールの場合、完全なパッケージ名が完全なモジュール名の一部になっています。例えば、パッケージ :mod:`P`
   内のサブモジュール :mod:`Q` に入っているモジュール :mod:`M` 内で定義されている :class:`T` は、 :attr:`tp_name` を
   ``"P.Q.M.T"`` に初期化します。

   動的にメモリ確保される型オブジェクトの場合、このフィールドは単に型の名前になり、モジュール名は型の辞書内でキー ``'__module__'``
   に対する値として明示的に保存されます。

   静的にメモリ確保される型オブジェクトの場合、 :attr:`tp_name` フィールドにはドットが入っているはずです。最後のドットよりも前にある
   部分文字列全体は :attr:`__module__` 属性として、またドットよりも後ろにある部分は :attr:`__name__`
   属性としてアクセスできます。

   ドットが入っていない場合、 :attr:`tp_name` フィールドの内容全てが :attr:`__name__` 属性になり、
   :attr:`__module__` 属性は (前述のように型の辞書内で明示的にセットしないかぎり) 未定義になります。このため、こうした型オブジェクトは
   pickle 化できないことになります。

   サブタイプはこのフィールドを継承しません。


.. c:member:: Py_ssize_t PyTypeObject.tp_basicsize
             Py_ssize_t PyTypeObject.tp_itemsize

   これらのフィールドは、型インスタンスのバイトサイズを計算できるようにします。

   型には二つの種類があります: 固定長インスタンスの型は、 :attr:`tp_itemsize` フィールドがゼロで、可変長インスタンスの方は
   :attr:`tp_itemsize` フィールドが非ゼロの値になります。固定長インスタンスの型の場合、全てのインスタンスは等しく
   :attr:`tp_basicsize` で与えられたサイズになります。

   可変長インスタンスの型の場合、インスタンスには :attr:`ob_size`  フィールドがなくてはならず、インスタンスのサイズは N をオブジェクトの
   "長さ" として、 :attr:`tp_basicsize` と N かける :attr:`tp_itemsize` の加算になります。N
   の値は通常、インスタンスの :attr:`ob_size`  フィールドに記憶されます。ただし例外がいくつかあります: 例えば、長整数では負の値を
   :attr:`ob_size` に使って、インスタンスの表す値が負であることを示し、 N 自体は ``abs(ob_size)``
   になります。また、 :attr:`ob_size` フィールドがあるからといって、必ずしもインスタンスが可変長であることを意味しません (例えば、
   リスト型の構造体は固定長のインスタンスになるにもかかわらず、インスタンスにはちゃんと意味を持った :attr:`ob_size` フィールドがあります)。

   基本サイズには、 :c:macro:`PyObject_HEAD` マクロまたは  :c:macro:`PyObject_VAR_HEAD` マクロ
   (インスタンス構造体を宣言するのに使ったどちらかのマクロ) で宣言されているフィールドが入っています。さらに、 :attr:`_ob_prev` および
   :attr:`_ob_next` フィールドがある場合、これらのフィールドもサイズに加算されます。

   従って、 :attr:`tp_basicsize` の正しい初期化パラメタを得るには、インスタンスデータのレイアウトを宣言するのに使う構造体に対して
   ``sizeof`` 演算子を使うしかありません。基本サイズには、GC ヘッダサイズは入っていません (これは Python 2.2
   からの新しい仕様です; 2.1 や 2.0 では、GC ヘッダサイズは :attr:`tp_basicsize` に入っていました)。

   これらのフィールドはサブタイプに別々に継承されます。
   基底タイプが 0 でない :attr:`tp_itemsize` を持っていた場合、基底タイプの実装に依存しますが、
   一般的にはサブタイプで別の 0 で無い値を :attr:`tp_itemsize` に設定するのは安全ではありません。

   バイト整列 (alignment) に関する注釈: 変数の各要素を配置する際に特定のバイト整列が必要となる場合、 :attr:`tp_basicsize`
   の値に気をつけなければなりません。一例: 例えばある型が ``double`` の配列を実装しているとします。 :attr:`tp_itemsize` は
   ``sizeof(double)`` です。(``double`` のバイト整列条件に従って) :attr:`tp_basicsize`
   が ``sizeof(double)`` の個数分のサイズになるようにするのはプログラマの責任です。


.. c:member:: destructor PyTypeObject.tp_dealloc

   インスタンスのデストラクタ関数へのポインタです。この関数は (単量子 ``None``
   や ``Ellipsis`` の場合のように) インスタンスが決してメモリ解放されない型で
   ない限り必ず定義しなければなりません。

   デストラクタ関数は、 :c:func:`Py_DECREF` や :c:func:`Py_XDECREF` マクロで、
   操作後の参照カウントがゼロになった際に呼び出されます。呼び出された時点では、
   インスタンスはまだ存在しますが、インスタンスに対する参照は全くない状態です。
   デストラクタ関数はインスタンスが保持している全ての参照を解放し、
   インスタンスが確保している全てのメモリバッファを (バッファの確保時に使った
   関数に対応するメモリ解放関数を使って) 解放し、最後に (かならず最後に行う
   操作として) その型の :attr:`tp_free` 関数を呼び出します。
   ある型がサブタイプを作成できない (:const:`Py_TPFLAGS_BASETYPE`
   フラグがセットされていない) 場合、 :attr:`tp_free` の代わりにオブジェクトの
   メモリ解放関数 (deallocator) を直接呼び出してもかまいません。オブジェクトの
   メモリ解放関数は、インスタンスのメモリ確保を行う際に使った関数と同じ
   ファミリでなければなりません;
   インスタンスを :c:func:`PyObject_New` や :c:func:`PyObject_VarNew` でメモリ
   確保した場合には、通常 :c:func:`PyObject_Del` を使い、
   :c:func:`PyObject_GC_New` や :c:func:`PyObject_GC_NewVar` で確保した場合には
   :c:func:`PyObject_GC_Del` を使います。

   サブタイプはこのフィールドを継承します。


.. c:member:: printfunc PyTypeObject.tp_print

   オプションのフィールドで、インスタンスの出力 (print) を行う関数を
   指すポインタです。

   出力関数は、インスタンスが *実体のある (real)* ファイルに出力される場合に
   のみ呼び出されます; (:class:`StringIO` インスタンスのような) 擬似ファイルに
   出力される場合には、インスタンスの :attr:`tp_repr` や :attr:`tp_str` が指す
   関数が呼び出され、文字列への変換を行います。
   また、 :attr:`tp_print` が *NULL* の場合にもこれらの関数が呼び出されます。
   :attr:`tp_repr` や :attr:`tp_str` と異なる出力を生成するような
   :attr:`tp_print` は、決して型に実装してはなりません。

   出力関数は :c:func:`PyObject_Print` と同じシグネチャ:
   ``int tp_print(PyObject *self, FILE *file, int flags)`` で呼び出されます。
   *self* 引数は出力するインスタンスを指します。
   *file* 引数は出力先となる標準入出力 (stdio) ファイルです。
   *flags* 引数はフラグビットを組み合わせた値です。
   現在定義されているフラグビットは :const:`Py_PRINT_RAW` のみです。
   :const:`Py_PRINT_RAW` フラグビットがセットされていれば、 インスタンスは
   :attr:`tp_str` と同じ書式で出力されます。 :const:`Py_PRINT_RAW`
   フラグビットがクリアならば、インスタンスは :attr:`tp_repr`
   と同じ書式で出力されます。この関数は、操作中にエラーが生じた場合、
   ``-1`` を返して例外状態をセットしなければなりません。

   :attr:`tp_print` フィールドは撤廃されるかもしれません。いずれにせよ、
   :attr:`tp_print` は定義せず、代わりに :attr:`tp_repr` や :attr:`tp_str`
   に頼って出力を行うようにしてください。

   サブタイプはこのフィールドを継承します。


.. c:member:: getattrfunc PyTypeObject.tp_getattr

   オプションのフィールドです。ポインタで、 get-attribute-string を行う関数を指します。

   このフィールドは撤廃されています。このフィールドを定義する場合、 :attr:`tp_getattro` 関数と同じように動作し、属性名は Python 文字列
   オブジェクトではなく C 文字列で指定するような関数を指すようにしなければなりません。シグネチャは
   :c:func:`PyObject_GetAttrString` と同じです。

   このフィールドは :attr:`tp_getattro` と共にサブタイプに継承されます: すなわち、サブタイプの :attr:`tp_getattr` および
   :attr:`tp_getattro` が共に *NULL* の場合、サブタイプは基底タイプから :attr:`tp_getattr` と
   :attr:`tp_getattro` を一緒に継承します。


.. c:member:: setattrfunc PyTypeObject.tp_setattr

   オプションのフィールドです。ポインタで、 set-attribute-string を行う関数を指します。

   このフィールドは撤廃されています。このフィールドを定義する場合、 :attr:`tp_setattro` 関数と同じように動作し、属性名は Python 文字列
   オブジェクトではなく C 文字列で指定するような関数を指すようにしなければなりません。シグネチャは
   :c:func:`PyObject_SetAttrString` と同じです。

   このフィールドは :attr:`tp_setattro` と共にサブタイプに継承されます: すなわち、サブタイプの :attr:`tp_setattr` および
   :attr:`tp_setattro` が共に *NULL* の場合、サブタイプは基底タイプから :attr:`tp_setattr` と
   :attr:`tp_setattro` を一緒に継承します。


.. c:member:: cmpfunc PyTypeObject.tp_compare

   オプションのフィールドです。ポインタで、三値比較 (three-way comparison) を行う関数を指します。

   シグネチャは :c:func:`PyObject_Compare` と同じです。この関数は *self* が *other* よりも大きければ ``1``,
   *self* と *other* の値が等しければ ``0``, *self* が *other* より小さければ ``-1`` を返します。
   この関数は、比較操作中にエラーが生じた場合、例外状態をセットして ``-1`` を返さねばなりません。

   このフィールドは :attr:`tp_richcompare` および :attr:`tp_hash` と共にサブタイプに継承されます:
   すなわち、サブタイプの :attr:`tp_compare`, :attr:`tp_richcompare` および :attr:`tp_hash` が共に
   *NULL* の場合、サブタイプは基底タイプから :attr:`tp_compare`, :attr:`tp_richcompare`,
   :attr:`tp_hash` の三つを一緒に継承します。


.. c:member:: reprfunc PyTypeObject.tp_repr

   .. index:: builtin: repr

   オプションのフィールドです。ポインタで、組み込み関数 :func:`repr` を実装している関数を指します。

   シグネチャは :c:func:`PyObject_Repr` と同じです。この関数は文字列オブジェクトか Unicode オブジェクトを返さねば
   なりません。理想的には、この関数が返す文字列は、適切な環境で :func:`eval` に渡した場合、同じ値を持つオブジェクトになるような
   文字列でなければなりません。不可能な場合には、オブジェクトの型と値から導出した内容の入った ``'<'``  から始まって ``'>'``
   で終わる文字列を返さねばなりません。

   このフィールドが設定されていない場合、 ``<%s object at %p>``  の形式をとる文字列が返されます。 ``%s`` は型の名前に、 ``%p``
   はオブジェクトのメモリアドレスに置き換えられます。

   サブタイプはこのフィールドを継承します。

.. c:member:: PyNumberMethods* tp_as_number

   数値プロトコルを実装した追加の構造体を指すポインタです。
   これらのフィールドについては :ref:`number-structs` で説明されています。

   :attr:`tp_as_number` フィールドは継承されませんが、そこの含まれるフィールドが
   個別に継承されます。


.. c:member:: PySequenceMethods* tp_as_sequence

   シーケンスプロトコルを実装した追加の構造体を指すポインタです。
   これらのフィールドについては :ref:`sequence-structs` で説明されています。

   :attr:`tp_as_sequence` フィールドは継承されませんが、そこの含まれるフィールドが
   個別に継承されます。


.. c:member:: PyMappingMethods* tp_as_mapping

   マッピングプロトコルを実装した追加の構造体を指すポインタです。
   これらのフィールドについては :ref:`mapping-structs` で説明されています。

   :attr:`tp_as_mapping` フィールドは継承されませんが、そこの含まれるフィールドが
   個別に継承されます。


.. c:member:: hashfunc PyTypeObject.tp_hash

   .. index:: builtin: hash

   オプションのフィールドです。ポインタで、組み込み関数 :func:`hash`
   を実装している関数を指します。

   シグネチャは :c:func:`PyObject_Hash` と同じです。この関数は C の
   :c:type:`long` 型の値を返さねばなりません。通常時には ``-1``
   を戻り値にしてはなりません; ハッシュ値の計算中にエラーが生じた場合、
   関数は例外をセットして ``-1`` を返さねばなりません。

   このフィールドは明示的に :c:func:`PyObject_HashNotImplemented` に設定することで、
   親 type からのハッシュメソッドの継承をブロックすることができます。
   これは Python レベルでの ``__hash__ = None`` と同等に解釈され、
   ``isinstance(o, collections.Hashable)`` が正しく ``False`` を返すようになります。
   逆もまた可能であることに注意してください - Python レベルで ``__hash__ = None``
   を設定することで ``tp_hash`` スロットは :c:func:`PyObject_HashNotImplemented`
   に設定されます。

   このフィールドが設定されていない場合、二つの可能性があります:
   :attr:`tp_compare` および :attr:`tp_richcompare` フィールドの両方が *NULL*
   の場合、オブジェクトのアドレスに基づいたデフォルトのハッシュ値が返されます;
   それ以外の場合、 :exc:`TypeError`  が送出されます。

   このフィールドは :attr:`tp_compare` および :attr:`tp_richcompare` と共にサブタイプに継承されます:
   すなわち、サブタイプの :attr:`tp_compare`, :attr:`tp_richcompare` および :attr:`tp_hash` が共に
   *NULL* の場合、サブタイプは基底タイプから :attr:`tp_compare`, :attr:`tp_richcompare`,
   :attr:`tp_hash` の三つを一緒に継承します。


.. c:member:: ternaryfunc PyTypeObject.tp_call

   オプションのフィールドです。ポインタで、オブジェクトの呼び出しを実装している
   関数を指します。オブジェクトが呼び出し可能でない場合には *NULL*
   にしなければなりません。シグネチャは :c:func:`PyObject_Call` と同じです。

   サブタイプはこのフィールドを継承します。


.. c:member:: reprfunc PyTypeObject.tp_str

   オプションのフィールドです。ポインタで、組み込みの演算 :func:`str` を実装している関数を指します。(:class:`str`
   が型の一つになったため、 :func:`str` は :class:`str` のコンストラクタを呼び出す
   ことに注意してください。このコンストラクタは実際の処理を行う上で :c:func:`PyObject_Str` を呼び出し、さらに
   :c:func:`PyObject_Str` がこのハンドラを呼び出すことになります。)

   シグネチャは :c:func:`PyObject_Str` と同じです; この関数は文字列オブジェクトか Unicode オブジェクトを返さねばなりません。
   また、この関数はオブジェクトを "分かりやすく (friendly)" 表現した文字列を返さねばなりません。というのは、この文字列は
   :keyword:`print` 文で使われることになる表記だからです。

   このフィールドが設定されていない場合、文字列表現を返すためには :c:func:`PyObject_Repr` が呼び出されます。

   サブタイプはこのフィールドを継承します。


.. c:member:: getattrofunc PyTypeObject.tp_getattro

   オプションのフィールドです。ポインタで、 get-attribute を実装している関数を指します。

   シグネチャは :c:func:`PyObject_GetAttr` と同じです。
   対する通常の属性検索を実装している :c:func:`PyObject_GenericGetAttr`  をこのフィールドに設定しておくと往々にして便利です。

   このフィールドは :attr:`tp_getattr` と共にサブタイプに継承されます: すなわち、サブタイプの :attr:`tp_getattr` および
   :attr:`tp_getattro` が共に *NULL* の場合、サブタイプは基底タイプから :attr:`tp_getattr` と
   :attr:`tp_getattro` を一緒に継承します。


.. c:member:: setattrofunc PyTypeObject.tp_setattro

   オプションのフィールドです。ポインタで、 set-attribute を行う関数を指します。

   シグネチャは :c:func:`PyObject_SetAttr` と同じです。
   対する通常の属性設定を実装している :c:func:`PyObject_GenericSetAttr`  をこのフィールドに設定しておくと往々にして便利です。

   このフィールドは :attr:`tp_setattr` と共にサブタイプに継承されます: すなわち、サブタイプの :attr:`tp_setattr` および
   :attr:`tp_setattro` が共に *NULL* の場合、サブタイプは基底タイプから :attr:`tp_setattr` と
   :attr:`tp_setattro` を一緒に継承します。


.. c:member:: PyBufferProcs* PyTypeObject.tp_as_buffer

   バッファインタフェースを実装しているオブジェクトにのみ関連する、
   一連のフィールド群が入った別の構造体を指すポインタです。
   構造体内の各フィールドは :ref:`buffer-structs` で説明します。

   :attr:`tp_as_buffer` フィールド自体は継承されませんが、
   フィールド内に入っているフィールドは個別に継承されます。


.. c:member:: long PyTypeObject.tp_flags

   このフィールドは様々なフラグからなるビットマスクです。いくつかのフラグは、
   特定の状況において変則的なセマンティクスが適用されることを示します;
   その他のフラグは、型オブジェクト (あるいは :attr:`tp_as_number`,
   :attr:`tp_as_sequence`, :attr:`tp_as_mapping`,および :attr:`tp_as_buffer`
   が参照している拡張機能構造体: extention structure) の特定のフィールドのうち、
   過去から現在までずっと存在しているわけではないものが有効になっていることを示すために使われます;
   フラグビットがクリアであれば、フラグが保護しているフィールドにはアクセスしない代わりに、その値はゼロか *NULL* になっているとみなさなければなりません。

   このフィールドの継承は複雑です。ほとんどのフラグビットは個別に継承されます。つまり、基底タイプであるフラグビットがセット
   されている場合、サブタイプはそのフラグビットを継承します。機能拡張のための構造体に関するフラグビットは、その機能拡張構造体
   が継承されるときに限定して継承されます。すなわち、基底タイプのフラグビットの値は、機能拡張構造体へのポインタと一緒にサブタイプにコピーされます。
   :const:`Py_TPFLAGS_HAVE_GC` フラグビットは、 :attr:`tp_traverse`  および :attr:`tp_clear`
   フィールドと合わせてコピーされます。すなわち、サブタイプの :const:`Py_TPFLAGS_HAVE_GC` フラグビットがクリアで、かつ
   (:const:`Py_TPFLAGS_HAVE_RICHCOMPARE` フラグビットの指定によって)  :attr:`tp_traverse` および
   :attr:`tp_clear`  フィールドがサブタイプ内に存在しており、かつ値が *NULL* の場合に基底タイプから値を継承します。

   以下のビットマスクは現在定義されているものです; フラグは ``|`` 演算子で論理和を取って :attr:`tp_flags` フィールドの値にできます。
   :c:func:`PyType_HasFeature` マクロは型とフラグ値、 *tp* および *f* をとり、 ``tp->tp_flags & f``
   が非ゼロかどうか調べます。


   .. data:: Py_TPFLAGS_HAVE_GETCHARBUFFER

      このビットがセットされていれば、 :attr:`tp_as_buffer` が参照する :c:type:`PyBufferProcs` 構造体には
      :attr:`bf_getcharbuffer` フィールドがあります。


   .. data:: Py_TPFLAGS_HAVE_SEQUENCE_IN

      このビットがセットされていれば、 :attr:`tp_as_sequence` が参照する :c:type:`PySequenceMethods` 構造体には
      :attr:`sq_contains` フィールドがあります。


   .. data:: Py_TPFLAGS_GC

      このビットは旧式のものです。このシンボルが指し示していたビットはもはや
      使われていません。シンボルの現在の定義はゼロになっています。


   .. data:: Py_TPFLAGS_HAVE_INPLACEOPS

      このビットがセットされていれば、 :attr:`tp_as_sequence` が参照する :c:type:`PySequenceMethods`
      構造体、および :attr:`tp_as_number` が参照する :c:type:`PyNumberMethods` 構造体には in-place
      演算に関するフィールドが入っています。具体的に言うと、 :c:type:`PyNumberMethods` 構造体はフィールド
      :attr:`nb_inplace_add`, :attr:`nb_inplace_subtract`,
      :attr:`nb_inplace_multiply`, :attr:`nb_inplace_divide`,
      :attr:`nb_inplace_remainder`, :attr:`nb_inplace_power`,
      :attr:`nb_inplace_lshift`, :attr:`nb_inplace_rshift`, :attr:`nb_inplace_and`,
      :attr:`nb_inplace_xor`,および :attr:`nb_inplace_or` を持つことになります; また、
      :c:type:`PySequenceMethods` 構造体はフィールド :attr:`sq_inplace_concat` および
      :attr:`sq_inplace_repeat` を持つことになります。


   .. data:: Py_TPFLAGS_CHECKTYPES

      このビットがセットされていれば、 :attr:`tp_as_number` が参照する :c:type:`PyNumberMethods`
      構造体内で定義されている二項演算子および三項演算子は任意のオブジェクト型を非演算子にとるようになり、
      必要に応じて引数の型変換を行います。このビットがクリアなら、演算子は全ての引数が現在のオブジェクト型と同じであるよう要求し、
      演算の呼び出し側は演算に先立って型変換を行うものと想定します。対象となる演算子は :attr:`nb_add`, :attr:`nb_subtract`,
      :attr:`nb_multiply`, :attr:`nb_divide`, :attr:`nb_remainder`, :attr:`nb_divmod`,
      :attr:`nb_power`, :attr:`nb_lshift`, :attr:`nb_rshift`, :attr:`nb_and`,
      :attr:`nb_xor`,および :attr:`nb_or` です。


   .. data:: Py_TPFLAGS_HAVE_RICHCOMPARE

      このビットがセットされていれば、型オブジェクトには :attr:`tp_richcompare` フィールド、そして :attr:`tp_traverse`
      および :attr:`tp_clear` フィールドがあります。


   .. data:: Py_TPFLAGS_HAVE_WEAKREFS

      このビットがセットされていれば、構造体には :attr:`tp_weaklistoffset`
      フィールドが定義されています。 :attr:`tp_weaklistoffset` フィールドの
      値がゼロより大きければ、この型のインスタンスは弱参照で参照できます。


   .. data:: Py_TPFLAGS_HAVE_ITER

      このビットがセットされていれば、型オブジェクトには :attr:`tp_iter`  および :attr:`tp_iternext` フィールドがあります。


   .. data:: Py_TPFLAGS_HAVE_CLASS

      このビットがセットされていれば、型オブジェクトは Python 2.2 以降で定義されている新たなフィールド: :attr:`tp_methods`,
      :attr:`tp_members`, :attr:`tp_getset`, :attr:`tp_base`, :attr:`tp_dict`,
      :attr:`tp_descr_get`, :attr:`tp_descr_set`, :attr:`tp_dictoffset`,
      :attr:`tp_init`, :attr:`tp_alloc`, :attr:`tp_new`, :attr:`tp_free`,
      :attr:`tp_is_gc`, :attr:`tp_bases`, :attr:`tp_mro`, :attr:`tp_cache`,
      :attr:`tp_subclasses`,および :attr:`tp_weaklist` があります。


   .. data:: Py_TPFLAGS_HEAPTYPE

      型オブジェクト自体がヒープにメモリ確保される場合にセットされるビットです。型オブジェクト自体がヒープにメモリ確保される場合、インスタンスの
      :attr:`ob_type` フィールドは型オブジェクトへの参照とみなされます。この場合、新たなインスタンスを生成する度に型オブジェクトを INCREF
      し、インスタンスを解放するたびに DECREF します (サブタイプのインスタンスには適当されません;  インスタンスが :attr:`ob_type`
      で参照している型だけが INCREF および DECREF されます)。


   .. data:: Py_TPFLAGS_BASETYPE

      型を別の型の基底タイプとして使える場合にセットされるビットです。このビットがクリアならば、この型のサブタイプは生成できません (Java における
      "final" クラスに似たクラスになります)。


   .. data:: Py_TPFLAGS_READY

      型オブジェクトが :c:func:`PyType_Ready` で完全に初期化されるとセットされるビットです。


   .. data:: Py_TPFLAGS_READYING

      :c:func:`PyType_Ready` による型オブジェクトの初期化処理中にセットされるビットです。


   .. data:: Py_TPFLAGS_HAVE_GC

      オブジェクトがガベージコレクション (GC) をサポートする場合にセットされるビットです。
      このビットがセットされている場合、インスタンスは :c:func:`PyObject_GC_New` を使って生成し、
      :c:func:`PyObject_GC_Del` を使って破壊しなければなりません。
      詳しい情報は :ref:`supporting-cycle-detection` にあります。
      このビットはまた、GC に関連するフィールド :attr:`tp_traverse`
      および :attr:`tp_clear` が型オブジェクト内に存在することを示します; しかし、これらのフィールドは
      :const:`Py_TPFLAGS_HAVE_GC` がクリアでも :const:`Py_TPFLAGS_HAVE_RICHCOMPARE`
      がセットされている場合には存在します。


   .. data:: Py_TPFLAGS_DEFAULT

      型オブジェクトおよび拡張機能構造体の特定のフィールドの存在の有無に関連する全てのビットからなるビットマスクです。現状では、このビットマスクには以下のビット:
      :const:`Py_TPFLAGS_HAVE_GETCHARBUFFER`, :const:`Py_TPFLAGS_HAVE_SEQUENCE_IN`,
      :const:`Py_TPFLAGS_HAVE_INPLACEOPS`, :const:`Py_TPFLAGS_HAVE_RICHCOMPARE`,
      :const:`Py_TPFLAGS_HAVE_WEAKREFS`, :const:`Py_TPFLAGS_HAVE_ITER`,および
      :const:`Py_TPFLAGS_HAVE_CLASS` が入っています。


.. c:member:: char* PyTypeObject.tp_doc

   オプションのフィールドです。ポインタで、この型オブジェクトの docstring を与える NUL 終端された C の文字列を指します。
   この値は型オブジェクトと型のインスタンスにおける :attr:`__doc__` 属性として公開されます。

   サブタイプはこのフィールドを継承 *しません* 。

以下の三つのフィールドは、 :const:`Py_TPFLAGS_HAVE_RICHCOMPARE`  フラグビットがセットされている場合にのみ存在します。


.. c:member:: traverseproc PyTypeObject.tp_traverse

   オプションのフィールドです。ポインタで、ガベージコレクタのためのトラバーサル関数 (traversal function)
   を指します。 :const:`Py_TPFLAGS_HAVE_GC` がセットされている
   場合にのみ使われます。Pythonのガベージコレクションの枠組みに関する詳細は :ref:`supporting-cycle-detection` にあります。

   :attr:`tp_traverse` ポインタは、ガベージコレクタが循環参照を見つけるために使われます。 :attr:`tp_traverse`
   関数の典型的な実装は、インスタンスの各メンバのうち Pythonオブジェクトに対して :c:func:`Py_VISIT` を呼び出します。例えば、次のコードは
   :mod:`thread` 拡張モジュールの :c:func:`local_traverse` 関数になります::

      static int
      local_traverse(localobject *self, visitproc visit, void *arg)
      {
          Py_VISIT(self->args);
          Py_VISIT(self->kw);
          Py_VISIT(self->dict);
          return 0;
      }

   :c:func:`Py_VISIT` が循環参照になる恐れのあるメンバにだけ呼び出されていることに注目してください。 ``self->key``
   メンバもありますが、それは *NULL* か Python文字列なので、循環参照の一部になることはありません。

   一方、メンバが循環参照の一部になり得ないと判っていても、デバッグ目的で巡回したい場合があるかもしれないので、 :mod:`gc` モジュールの
   :c:func:`get_reference` 関数は循環参照になり得ないメンバも返します。

   :c:func:`Py_VISIT` は :c:func:`local_traverse` が *visit* と *arg*
   という決まった名前の引数を持つことを要求します。

   このフィールドは :attr:`tp_clear` および :const:`Py_TPFLAGS_HAVE_GC` フラグビットと一緒に継承されます:
   フラグビット、 :attr:`tp_traverse`,および :attr:`tp_clear` の値がサブタイプで全てゼロになっており、 *かつ*
   サブタイプで :const:`Py_TPFLAGS_HAVE_RICHCOMPARE`  フラグビットがセットされている場合に、基底タイプから値を継承します。


.. c:member:: inquiry PyTypeObject.tp_clear

   オプションのフィールドです。ポインタで、ガベージコレクタにおける消去関数 (clear function) を指します。
   :const:`Py_TPFLAGS_HAVE_GC` がセットされている場合にのみ使われます。

   :attr:`tp_clear` メンバ関数はGCが見つけた循環しているゴミの循環参照を壊すために用いられます。システム内の全ての
   :attr:`tp_clear` 関数によって、全ての循環参照を破壊しなければなりません。 (訳注:
   ある型が :attr:`tp_clear` を実装しなくても全ての循環参照が破壊できるのであれば実装しなくても良い)
   これはとても繊細で、もし少しでも不確かな部分があるのであれば、 :attr:`tp_clear` 関数を提供するべきです。
   例えば、タプルは :attr:`tp_clear` を実装しません。なぜなら、タプルだけで構成された循環参照がみつかることは無いからです。
   したがって、タプル以外の型 :attr:`tp_clear` 関数たちが、タプルを含むどんな循環参照も破壊できる必要があります。
   これは簡単に判ることでははありません。 :attr:`tp_clear` の実装を避ける良い理由はめったにありません。

   :attr:`tp_clear` の実装は、次の実装のように、インスタンスの
   (Pythonオブジェクト)メンバに対する参照を捨てて、メンバに対するポインタ変数を *NULL* にセットするべきです::

      static int
      local_clear(localobject *self)
      {
          Py_CLEAR(self->key);
          Py_CLEAR(self->args);
          Py_CLEAR(self->kw);
          Py_CLEAR(self->dict);
          return 0;
      }

   参照のクリアはデリケートなので、 :c:func:`Py_CLEAR` マクロを使うべきです:
   ポインタを *NULL* にセットするまで、そのオブジェクトの参照カウントをデクリメントしてはいけません。
   参照カウントのデクリメントすると、そのオブジェクトが破棄されるかもしれず、 (そのオブジェクトに関連付けられたファイナライザ、弱参照のコールバックにより)
   任意のPythonコードの実行を含む後片付け処理が実行されるかもしれないからです。もしそういったコードが再び *self* を参照することがあれば、すでに
   持っていたオブジェクトへのポインタは *NULL* になっているので、 *self* は所有していたオブジェクトをもう利用できないことを認識できます。
   :c:func:`Py_CLEAR` マクロはその手続きを安全な順番で実行します。

   :attr:`tp_clear` 関数の目的は参照カウントを破壊することなので、Python文字列や
   Python整数のような、循環参照になりえないオブジェクトをクリアする必要はありません。一方、全部の所有オブジェクトをクリアするようにし、
   :attr:`tp_dealloc` 関数が :attr:`tp_clear` 関数を実行するようにすると実装が楽です。

   Pythonのガベージコレクションの仕組みについての詳細は、 :ref:`supporting-cycle-detection` にあります。

   このフィールドは :attr:`tp_traverse` および :const:`Py_TPFLAGS_HAVE_GC` フラグビットと一緒に継承されます:
   フラグビット、 :attr:`tp_traverse`,および :attr:`tp_clear` の値がサブタイプで全てゼロになっており、 *かつ*
   サブタイプで :const:`Py_TPFLAGS_HAVE_RICHCOMPARE`  フラグビットがセットされている場合に、基底タイプから値を継承します。


.. c:member:: richcmpfunc PyTypeObject.tp_richcompare

   オプションのフィールドで、拡張比較関数 (rich comparison function)
   を指すポインタです。拡張比較関数のシグネチャは
   ``PyObject *tp_richcompare(PyObject *a, PyObject *b, int op)`` です。

   この関数は、比較結果を返すべきです。(普通は ``Py_True`` か ``Py_False``
   です。) 比較が未定義の場合は、 ``Py_NotImplemented`` を、それ以外のエラーが
   発生した場合には例外状態をセットして ``NULL`` を返さねばなりません。

   .. note::

      限られた種類の比較だけが可能 (例えば、 ``==`` と ``!=`` が可能で ``<``
      などが不可能) な型を実装したい場合、拡張比較関数で直接 :exc:`TypeError`
      を返します。

   このフィールドは :attr:`tp_compare` および :attr:`tp_hash` と共にサブタイプに継承されます: すなわち、サブタイプの
   :attr:`tp_compare`, :attr:`tp_richcompare` および :attr:`tp_hash` が共に
   *NULL* の場合、サブタイプは基底タイプから :attr:`tp_compare`, :attr:`tp_richcompare`,
   :attr:`tp_hash` の三つを一緒に継承します。

   :attr:`tp_richcompare` および :c:func:`PyObject_RichCompare`
   関数の第三引数に使うための定数としては以下が定義されています:

   +----------------+--------+
   | 定数           | 比較   |
   +================+========+
   | :const:`Py_LT` | ``<``  |
   +----------------+--------+
   | :const:`Py_LE` | ``<=`` |
   +----------------+--------+
   | :const:`Py_EQ` | ``==`` |
   +----------------+--------+
   | :const:`Py_NE` | ``!=`` |
   +----------------+--------+
   | :const:`Py_GT` | ``>``  |
   +----------------+--------+
   | :const:`Py_GE` | ``>=`` |
   +----------------+--------+

次のフィールドは、 :const:`Py_TPFLAGS_HAVE_WEAKREFS` フラグビットがセットされている場合にのみ存在します。


.. c:member:: long PyTypeObject.tp_weaklistoffset

   型のインスタンスが弱参照可能な場合、このフィールドはゼロよりも大きな数になり、
   インスタンス構造体における弱参照リストの先頭を示すオフセットが入ります (GC
   ヘッダがある場合には無視します); このオフセット値は :c:func:`PyObject_ClearWeakRefs` および
   :c:func:`PyWeakref_\*` 関数が利用します。インスタンス構造体には、 *NULL* に初期化された :c:type:`PyObject\*` 型の
   フィールドが入っていなければなりません。

   このフィールドを :attr:`tp_weaklist` と混同しないようにしてください; :attr:`tp_weaklist`
   は型オブジェクト自体の弱参照リストの先頭です。

   サブタイプはこのフィールドを継承しますが、以下の規則があるので読んでください。サブタイプはこのオフセット値をオーバライドできます; 従って、
   サブタイプでは弱参照リストの先頭が基底タイプとは異なる場合があります。リストの先頭は常に :attr:`tp_weaklistoffset` で
   分かるはずなので、このことは問題にはならないはずです。

   :keyword:`class` 文で定義された型に :attr:`__slots__` 宣言が全くなく、かつ基底タイプが弱参照可能でない場合、
   その型を弱参照可能にするには弱参照リストの先頭を表すスロットをインスタンスデータレイアウト構造体に追加し、スロットのオフセットを
   :attr:`tp_weaklistoffset` に設定します。

   型の :attr:`__slots__` 宣言中に :attr:`__weakref__` という名前の
   スロットが入っている場合、スロットはその型のインスタンスにおける弱参照リストの先頭を表すスロットになり、スロットのオフセットが型の
   :attr:`tp_weaklistoffset` に入ります。

   型の :attr:`__slots__` 宣言に :attr:`__weakref__` という名のスロット
   が入っていない場合、その型は基底タイプから :attr:`tp_weaklistoffset`  を継承します。

次の二つのフィールドは、 :const:`Py_TPFLAGS_HAVE_ITER` フラグビットがセットされている場合にのみ存在します。


.. c:member:: getiterfunc PyTypeObject.tp_iter

   オプションの変数で、そのオブジェクトのイテレータを返す関数へのポインタです。
   この値が存在することは、通常この型のインスタンスがイテレート可能であることを
   示しています。(しかし、シーケンスはこの関数がなくてもイテレート可能ですし、
   旧スタイルクラスのインスタンスは :meth:`__iter__` メソッドを定義していなくても
   この関数を持っています)

   この関数は :c:func:`PyObject_GetIter` と同じシグネチャを持っています。

   サブタイプはこのフィールドを継承します。


.. c:member:: iternextfunc PyTypeObject.tp_iternext

   オプションのフィールドで、イテレータにおいて次の要素を返す関数への
   ポインタです。
   イテレータの要素がなくなると、この関数は *NULL* を返さなければなりません。
   :exc:`StopIteration` 例外は設定してもしなくても良いです。
   その他のエラーが発生したときも、 *NULL* を返さなければなりません。
   このフィールドがあると、通常この型のインスタンスがイテレータであることを示します
   (ただし、旧スタイルのインスタンスでは、たとえ :meth:`next` メソッドが
   定義されていなくても常にこの関数を持っています)。

   イテレータ型では、 :attr:`tp_iter` 関数も定義していなければならず、 :attr:`tp_iter` は
   (新たなイテレータインスタンスではなく)  イテレータインスタンス自体を返さねばなりません。

   この関数のシグネチャは :c:func:`PyIter_Next` と同じです。

   サブタイプはこのフィールドを継承します。

次の :attr:`tp_weaklist` までのフィールドは、 :const:`Py_TPFLAGS_HAVE_CLASS`
フラグビットがセットされている場合にのみ存在します。


.. c:member:: struct PyMethodDef* PyTypeObject.tp_methods

   オプションのフィールドです。ポインタで、この型の正規 (regular) のメソッドを宣言している :c:type:`PyMethodDef`
   構造体からなる、 *NULL* で終端された静的な配列を指します。

   配列の各要素ごとに、メソッドデスクリプタの入ったエントリが型辞書 (下記の :attr:`tp_dict` 参照) に追加されます。

   サブタイプはこのフィールドを継承しません (メソッドは別個のメカニズムで継承されています)。


.. c:member:: struct PyMemberDef* PyTypeObject.tp_members

   オプションのフィールドです。ポインタで、型の正規 (regular) のデータメンバ (フィールドおよびスロット) を
   宣言している :c:type:`PyMemberDef` 構造体からなる、 *NULL* で終端された静的な配列を指します。

   配列の各要素ごとに、メンバデスクリプタの入ったエントリが型辞書 (下記の :attr:`tp_dict` 参照) に追加されます。

   サブタイプはこのフィールドを継承しません (メンバは別個のメカニズムで継承されています)。


.. c:member:: struct PyGetSetDef* PyTypeObject.tp_getset

   オプションのフィールドです。ポインタで、インスタンスの算出属性 (computed attribute) を
   宣言している :c:type:`PyGetSetDef` 構造体からなる、 *NULL* で終端された静的な配列を指します。

   配列の各要素ごとに、getset デスクリプタの入ったエントリが型辞書 (下記の :attr:`tp_dict` 参照) に追加されます。

   サブタイプはこのフィールドを継承しません (算出属性は別個のメカニズムで継承されています)。

   PyGetSetDef のドキュメント::

      typedef PyObject *(* getter)(PyObject *, void *);
      typedef int (*setter)(PyObject *, PyObject *, void *);

      typedef struct PyGetSetDef {
          char *name;    /* 属性名 */
          getter get;    /* 属性の get を行う C 関数 */
          setter set;    /* 属性の set を行う C 関数 */
          char *doc;     /* オプションの docstring  */
          void *closure; /* オプションの get/set 関数用追加データ */
      } PyGetSetDef;


.. c:member:: PyTypeObject* PyTypeObject.tp_base

   オプションのフィールドです。ポインタで、型に関するプロパティを継承する基底タイプへのポインタです。このフィールドのレベルでは、単継承 (single
   inheritance) だけがサポートされています; 多重継承はメタタイプの呼び出しによる動的な型オブジェクトの生成を必要とします。

   (当たり前ですが) サブタイプはこのフィールドを継承しません。しかし、このフィールドのデフォルト値は  (Python
   プログラマは :class:`object` 型として知っている) ``&PyBaseObject_Type`` になります。 .


.. c:member:: PyObject* PyTypeObject.tp_dict

   型の辞書は :c:func:`PyType_Ready` によってこのフィールドに収められます。

   このフィールドは通常、 :c:func:`PyType_Ready` を呼び出す前に *NULL* に初期化しておかねばなりません; あるいは、型の初期属性の入った
   辞書で初期化しておいてもかまいません。 :c:func:`PyType_Ready` が型をひとたび初期化すると、型の新たな属性をこの辞書に追加できるのは、
   属性が (:meth:`__add__` のような) オーバロード用演算でないときだけです。

   サブタイプはこのフィールドを継承しません (が、この辞書内で定義されている属性は異なるメカニズムで継承されます)。


.. c:member:: descrgetfunc PyTypeObject.tp_descr_get

   オプションのフィールドです。ポインタで、 "デスクリプタ get" 関数を指します。

   関数のシグネチャは次のとおりです。 ::

      PyObject * tp_descr_get(PyObject *self, PyObject *obj, PyObject *type);

   サブタイプはこのフィールドを継承します。


.. c:member:: descrsetfunc PyTypeObject.tp_descr_set

   オプションのフィールドです。ポインタで、 "デスクリプタ set" 関数を指します。

   関数のシグネチャは次のとおりです。 ::

      int tp_descr_set(PyObject *self, PyObject *obj, PyObject *value);

   サブタイプはこのフィールドを継承します。


.. c:member:: long PyTypeObject.tp_dictoffset

   型のインスタンスにインスタンス変数の入った辞書がある場合、このフィールドは非ゼロの値になり、型のインスタンスデータ構造体
   におけるインスタンス変数辞書へのオフセットが入ります; このオフセット値は :c:func:`PyObject_GenericGetAttr` が使います。

   このフィールドを :attr:`tp_dict` と混同しないでください;
   :attr:`tp_dict` は型オブジェクト自体の属性のための辞書です。

   このフィールドの値がゼロより大きければ、値はインスタンス構造体の先頭からの
   オフセットを表します。値がゼロより小さければ、インスタンス構造体の *末尾*
   からのオフセットを表します。負のオフセットを使うコストは比較的高くつくので、
   インスタンス構造体に可変長の部分があるときのみ使うべきです。
   例えば、 :class:`str` や :class:`tuple` のサブタイプにインスタンス辞書を
   追加する場合には、負のオフセットを使います。
   この場合、たとえ辞書が基本のオブジェクトレイアウトに含まれていなくても、
   :attr:`tp_basicsize` フィールドは追加された辞書を考慮にいれなければ
   ならないので注意してください。ポインタサイズが 4 バイトのシステムでは、
   構造体の最後尾に辞書が宣言されていることを示す場合、
   :attr:`tp_dictoffset` を ``-4`` にしなければなりません。

   :attr:`tp_dictoffset` が負の場合、インスタンスにおける実際の辞書の
   オフセットは以下のようにして計算されます::

      dictoffset = tp_basicsize + abs(ob_size)*tp_itemsize + tp_dictoffset
      if dictoffset is not aligned on sizeof(void*):
          round up to sizeof(void*)

   ここで、 :attr:`tp_basicsize`, :attr:`tp_itemsize` および :attr:`tp_dictoffset`
   は型オブジェクトから取り出され、 :attr:`ob_size` はインスタンスから取り出されます。
   長整数は符号を記憶するのに :attr:`ob_size` の符号を使うため、
   :attr:`ob_size` は絶対値を使います。(この計算を自分で行う必要はまったくありません;
   :c:func:`_PyObject_GetDictPtr` がやってくれます。)

   サブタイプはこのフィールドを継承しますが、以下の規則があるので読んでください。
   サブタイプはこのオフセット値をオーバライドできます;
   従って、サブタイプでは辞書のオフセットが基底タイプとは異なる場合があります。
   辞書へのオフセット常に :attr:`tp_dictoffset` で分かるはずなので、
   このことは問題にはならないはずです。

   :keyword:`class` 文で定義された型に :attr:`__slots__` 宣言がなく、
   かつ基底タイプの全てにインスタンス変数辞書がない場合、辞書のスロットを
   インスタンスデータレイアウト構造体に追加し、
   スロットのオフセットを :attr:`tp_dictoffset` に設定します。

   :keyword:`class` 文で定義された型に :attr:`__slots__` 宣言がある場合、
   この型は基底タイプから :attr:`tp_dictoffset` を継承します。

   (:attr:`__dict__` という名前のスロットを :attr:`__slots__` 宣言に
   追加しても、期待どおりの効果は得られず、単に混乱を招くだけになります。
   とはいえ、これは将来 :attr:`__weakref__` のように追加されるはずです。)


.. c:member:: initproc PyTypeObject.tp_init

   オプションのフィールドです。ポインタで、インスタンス初期化関数を指します。

   この関数はクラスにおける  :meth:`__init__` メソッドに対応します。 :meth:`__init__` と同様、 :meth:`__init__`
   を呼び出さずにインスタンスを作成できます。また、 :meth:`__init__` を再度呼び出してインスタンスの再初期化もできます。

   関数のシグネチャは ::

      int tp_init(PyObject *self, PyObject *args, PyObject *kwds)

   です。

   *self* 引数は初期化するインスタンスです; *args* および *kwds* 引数は、
   :meth:`__init__` を呼び出す際の固定引数およびキーワード引数です。

   :attr:`tp_init` 関数のフィールドが *NULL* でない場合、型の呼び出しで普通にインスタンスを生成する際に、型の :attr:`tp_new`
   がインスタンスを返した後に :attr:`tp_init` が呼び出されます。 :attr:`tp_new` が元の型のサブタイプでない別の型を返す場合、
   :attr:`tp_init` は全く呼び出されません; :attr:`tp_new` が元の型のサブタイプのインスタンスを返す場合、サブタイプの
   :attr:`tp_init` が呼び出されます。 (VERSION NOTE: ここに書かれている内容は、Python 2.2.1
   以降での実装に関するものです。Python 2.2 では、 :attr:`tp_init` は *NULL* でない限り :attr:`tp_new` が返す全ての
   オブジェクトに対して常に呼び出されます。) not *NULL*.)

   サブタイプはこのフィールドを継承します。


.. c:member:: allocfunc PyTypeObject.tp_alloc

   オプションのフィールドです。ポインタで、インスタンスのメモリ確保関数を指します。

   関数のシグネチャは ::

      PyObject *tp_alloc(PyTypeObject *self, Py_ssize_t nitems)

   です。

   この関数の目的は、メモリ確保をメモリ初期化から分離することにあります。この関数は、インスタンス用の的確なサイズを持ち、適切にバイト整列
   され、ゼロで初期化され、ただし :attr:`ob_refcnt` を ``1``  にセットされ、 :attr:`ob_type` が型引数 (type
   argument) にセットされているようなメモリブロックを返さねばなりません。型の :attr:`tp_itemsize`
   がゼロでない場合、オブジェクトの :attr:`ob_size` フィールドは *nitems* に初期化され、確保されるメモリブロックの長さは
   ``tp_basicsize + nitems *tp_itemsize`` を ``sizeof(void*)`` の倍数で丸めた値になるはずです;
   それ以外の場合、 *nitems* の値は使われず、メモリブロックの長さは :attr:`tp_basicsize` になるはずです。

   この関数をインスタンス初期化の他のどの処理にも、追加でメモリ確保をする場合でさえ使ってはなりません; そうした処理は :attr:`tp_new`
   で行わねばなりません。

   静的なサブタイプはこのフィールドを継承しますが、動的なサブタイプ (:keyword:`class` 文で生成するサブタイプ) の場合は継承しません;
   後者の場合、このフィールドは常に :c:func:`PyType_GenericAlloc` にセットされ、標準のヒープ上メモリ確保戦略が強制されます。
   静的に定義する型の場合でも、 :c:func:`PyType_GenericAlloc` を推奨します。


.. c:member:: newfunc PyTypeObject.tp_new

   オプションのフィールドです。ポインタで、インスタンス生成関数を指します。

   このフィールドが *NULL* を指している型では、型を呼び出して新たなインスタンスを生成できません; こうした型では、おそらくファクトリ
   関数のように、インスタンスを生成する他の方法があるはずです。

   関数のシグネチャは ::

      PyObject *tp_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds)

   です。

   引数 *subtype* は生成するオブジェクトの型です;  *args* および *kwds* 引数は、型を呼び出すときの
   固定引数およびキーワード引数です。サブタイプは :attr:`tp_new` 関数を呼び出すときに使う型と等価というわけではないので注意してください;
   :attr:`tp_new` 関数を呼び出すときに使う型 (と無関係ではない)  サブタイプのこともあります。

   :attr:`tp_new` 関数は ``subtype->tp_alloc(subtype, nitems)``
   を呼び出してオブジェクトのメモリ領域を確保し、初期化で本当に必要とされる処理だけを行います。省略したり繰り返したりしても問題のない
   初期化処理は :attr:`tp_init` ハンドラ内に配置しなければなりません。経験則からいうと、変更不能な型の場合、初期化は全て
   :attr:`tp_new` で行い、変更可能な型の場合はほとんどの初期化を :attr:`tp_init` に回すべきです。

   サブタイプはこのフィールドを継承します。例外として、 :attr:`tp_base` が *NULL* か ``&PyBaseObject_Type``
   になっている静的な型では継承しません。後者が例外になっているのは、旧式の拡張型が Python 2.2
   でリンクされたときに呼び出し可能オブジェクトにならないようにするための予防措置です。


.. c:member:: destructor PyTypeObject.tp_free

   オプションのフィールドです。ポインタで、インスタンスのメモリ解放関数を指します。

   この関数のシグネチャは少し変更されています; Python 2.2 および 2.2.1 では、シグネチャは :c:type:`destructor` ::

      void tp_free(PyObject *)

   でしたが、 Python 2.3 以降では、シグネチャは :c:type:`freefunc`::

      void tp_free(void *)

   になっています。

   両方のバージョンと互換性のある初期値は ``_PyObject_Del`` です。 ``_PyObject_Del`` の定義は Python 2.3
   で適切に対応できるよう変更されました。

   静的なサブタイプはこのフィールドを継承しますが、動的なサブタイプ (:keyword:`class` 文で生成するサブタイプ) の場合は継承しません;
   後者の場合、このフィールドには :c:func:`PyType_GenericAlloc` と :const:`Py_TPFLAGS_HAVE_GC`
   フラグビットの値に対応させるのにふさわしいメモリ解放関数がセットされます。


.. c:member:: inquiry PyTypeObject.tp_is_gc

   オプションのフィールドです。ポインタで、ガベージコレクタから呼び出される関数を指します。

   ガベージコレクタは、オブジェクトがガベージとして収集可能かどうかを知る必要があります。これを知るには、通常はオブジェクトの型の
   :attr:`tp_flags` フィールドを見て、 :const:`Py_TPFLAGS_HAVE_GC`
   フラグビットを調べるだけで十分です。しかし、静的なメモリ確保と動的なメモリ確保が混じっているインスタンスを持つような型や、
   静的にメモリ確保されたインスタンスは収集できません。こうした型では、このフィールドに関数を定義しなければなりません; 関数はインスタンスが収集可能の場合には
   ``1`` を、収集不能の場合には ``0`` を返さねばなりません。シグネチャは ::

      int tp_is_gc(PyObject *self)

   です。

   (上記のような型の例は、型オブジェクト自体です。メタタイプ :c:data:`PyType_Type` は、型のメモリ確保が静的か動的かを
   区別するためにこの関数を定義しています。)

   サブタイプはこのフィールドを継承します。 (VERSION NOTE: Python 2.2 では、このフィールドは継承されませんでした。 2.2.1
   以降のバージョンから継承されるようになりました。)


.. c:member:: PyObject* PyTypeObject.tp_bases

   基底型からなるタプルです。

   :keyword:`class` 文で生成されたクラスの場合このフィールドがセットされます。静的に定義されている型の場合には、このフィールドは *NULL*
   になります。

   このフィールドは継承されません。


.. c:member:: PyObject* PyTypeObject.tp_mro

   基底クラス群を展開した集合が入っているタプルです。集合は該当する型自体からはじまり、 :class:`object` で終わります。メソッド解決順
   (Method Resolution Order) の順に並んでいます。

   このフィールドは継承されません; フィールドの値は :c:func:`PyType_Ready` で毎回計算されます。


.. c:member:: PyObject* PyTypeObject.tp_cache

   使用されていません。継承されません。内部で使用するためだけのものです。


.. c:member:: PyObject* PyTypeObject.tp_subclasses

   サブクラスへの弱参照からなるリストです。継承されません。内部で使用するためだけのものです。


.. c:member:: PyObject* PyTypeObject.tp_weaklist

   この型オブジェクトに対する弱参照からなるリストの先頭です。

残りのフィールドは、機能テスト用のマクロである :const:`COUNT_ALLOCS` が定義されている場合のみ利用でき、内部で使用するためだけのものです。
これらのフィールドについて記述するのは単に完全性のためです。サブタイプはこれらのフィールドを継承しません。


.. c:member:: Py_ssize_t PyTypeObject.tp_allocs

   メモリ確保の回数です。


.. c:member:: Py_ssize_t PyTypeObject.tp_frees

   メモリ解放の回数です。


.. c:member:: Py_ssize_t PyTypeObject.tp_maxalloc

   同時にメモリ確保できる最大オブジェクト数です。


.. c:member:: PyTypeObject* PyTypeObject.tp_next

   :attr:`tp_allocs` フィールドが非ゼロの、(リンクリストの) 次の型オブジェクトを指すポインタです。

また、 Python のガベージコレクションでは、 *tp_dealloc* を呼び出すのはオブジェクトを生成したスレッドだけではなく、任意の Python
スレッドかもしれないという点にも注意して下さい。 (オブジェクトが循環参照の一部の場合、任意のスレッドのガベージコレクション
によって解放されてしまうかもしれません)。Python API 側からみれば、 *tp_dealloc* を呼び出すスレッドはグローバルインタプリタロック
(GIL: Global Interpreter Lock) を獲得するので、これは問題ではありません。
しかしながら、削除されようとしているオブジェクトが何らかの C や C++ ライブラリ由来のオブジェクトを削除する場合、 *tp_dealloc* を
呼び出すスレッドのオブジェクトを削除することで、ライブラリの仮定している何らかの規約に違反しないように気を付ける必要があります。


.. _number-structs:

数値オブジェクト構造体
======================

.. sectionauthor:: Amaury Forgeot d'Arc

.. c:type:: PyNumberMethods

   拡張型で数値型プロトコルを実装するために使われる関数群へのポインタを保持するために使われる構造体です。
   以下のほとんどすべての関数は :ref:`number` で解説されている似た名前の関数から利用されます。

   以下は構造体の定義です。 ::

       typedef struct {
            binaryfunc nb_add;
            binaryfunc nb_subtract;
            binaryfunc nb_multiply;
            binaryfunc nb_divide;
            binaryfunc nb_remainder;
            binaryfunc nb_divmod;
            ternaryfunc nb_power;
            unaryfunc nb_negative;
            unaryfunc nb_positive;
            unaryfunc nb_absolute;
            inquiry nb_nonzero;       /* Used by PyObject_IsTrue */
            unaryfunc nb_invert;
            binaryfunc nb_lshift;
            binaryfunc nb_rshift;
            binaryfunc nb_and;
            binaryfunc nb_xor;
            binaryfunc nb_or;
            coercion nb_coerce;       /* Used by the coerce() function */
            unaryfunc nb_int;
            unaryfunc nb_long;
            unaryfunc nb_float;
            unaryfunc nb_oct;
            unaryfunc nb_hex;

            /* Added in release 2.0 */
            binaryfunc nb_inplace_add;
            binaryfunc nb_inplace_subtract;
            binaryfunc nb_inplace_multiply;
            binaryfunc nb_inplace_divide;
            binaryfunc nb_inplace_remainder;
            ternaryfunc nb_inplace_power;
            binaryfunc nb_inplace_lshift;
            binaryfunc nb_inplace_rshift;
            binaryfunc nb_inplace_and;
            binaryfunc nb_inplace_xor;
            binaryfunc nb_inplace_or;

            /* Added in release 2.2 */
            binaryfunc nb_floor_divide;
            binaryfunc nb_true_divide;
            binaryfunc nb_inplace_floor_divide;
            binaryfunc nb_inplace_true_divide;

            /* Added in release 2.5 */
            unaryfunc nb_index;
       } PyNumberMethods;


2引数および3引数の関数は、 :const:`Py_TPFLAGS_CHECKTYPES` フラグによっては、
異なる種類の引数を受け取るかもしれません。

- :const:`Py_TPFLAGS_CHECKTYPES` がセットされていない場合、関数の引数は
  オブジェクトの型であることが保証されます。呼び出し側は :attr:`nb_coerce`
  メンバで指定されている型強制メソッドを呼び出して引数を変換する責任があります。

  .. c:member:: coercion PyNumberMethods.nb_coerce

     この関数は :c:func:`PyNumber_CoerceEx` から利用され、同じシグネチャを持ちます。
     最初の引数は定義された型のオブジェクトを指すポインタでなければなりません。
     共通の "大きな" 型への変換が可能であれば、この関数はポインタを変換後の
     オブジェクトへの新しい参照へ置き換えて、 ``0`` を返します。
     変換ができないなら、この関数は ``1`` を返します。
     エラーが設定荒れた場合は、 ``-1`` を返します。

- :const:`Py_TPFLAGS_CHECKTYPES` フラグがセットされている場合、2引数および
  3引数関数はすべてのオペランドの型をチェクし、必要な変換を行わなければなりません。
  (少なくとも、オペランドのうち1つは定義している型のものです)
  これは推奨された方式です。 Python 3.0 では型強制は完全に取り除かれています。

与えられたオペランドに対して操作が定義されていな場合は、2引数および3引数関数は
``Py_NotImplemented`` を返さなければなりません。
その他のエラーが発生した場合は、例外を設定して ``NULL`` を返さなければなりません。


.. _mapping-structs:

マップ型オブジェクト構造体
==========================

.. sectionauthor:: Amaury Forgeot d'Arc

.. c:type:: PyMappingMethods

   拡張型でマップ型プロトコルを実装するために使われる関数群へのポインタを保持するために使われる構造体です。
   以下の3つのメンバを持っています。

.. c:member:: lenfunc PyMappingMethods.mp_length

   この関数は :c:func:`PyMapping_Length` や :c:func:`PyObject_Size`
   から利用され、それらと同じシグネチャを持っています。
   オブジェクトが定義された長さを持たない場合は、このスロットは
   *NULL* に設定されることがあります。

.. c:member:: binaryfunc PyMappingMethods.mp_subscript

   この関数は :c:func:`PyObject_GetItem` から利用され、同じシグネチャを持っています。
   このスロットは :c:func:`PyMapping_Check` が ``1`` を返すためには
   必要で、そうでなければ *NULL* の場合があります。

.. c:member:: objobjargproc PyMappingMethods.mp_ass_subscript

   この関数は :c:func:`PyObject_SetItem` から利用され、同じシグネチャを持っています。
   もしこのスロットが *NULL* なら、このオブジェクトはアイテムの代入をサポートしません。


.. _sequence-structs:

シーケンスオブジェクト構造体
=============================

.. sectionauthor:: Amaury Forgeot d'Arc

.. c:type:: PySequenceMethods

   拡張型でシーケンス型プロトコルを実装するために使われる関数群への
   ポインタを保持するために使われる構造体です。

.. c:member:: lenfunc PySequenceMethods.sq_length

   この関数は :c:func:`PySequence_Size` や :c:func:`PyObject_Size`
   から利用され、それらと同じシグネチャを持っています。

.. c:member:: binaryfunc PySequenceMethods.sq_concat

   この関数は :c:func:`PySequence_Concat`
   から利用され、同じシグネチャを持っています。
   また、 ``+`` 演算からも、 :attr:`tp_as_number.nb_add` スロットによる
   数値加算を試したあとに利用されます。

.. c:member:: ssizeargfunc PySequenceMethods.sq_repeat

   この関数は :c:func:`PySequence_Repeat`
   から利用され、同じシグネチャを持っています。
   また、 ``*`` 演算からも、 :attr:`tp_as_number.nb_mul` スロットによる
   数値乗算を試したあとに利用されます。

.. c:member:: ssizeargfunc PySequenceMethods.sq_item

   この関数は :c:func:`PySequence_GetItem`
   から利用され、同じシグネチャを持っています。
   このスロットは :c:func:`PySequence_Check` が ``1`` を返すためには埋めなければならず、
   それ以外の場合は *NULL* の可能性があります。

   負のインデックスは次のように処理されます: :attr:`sq_length` スロットが
   埋められていれば、それを呼び出してシーケンスの長さから正のインデックスを
   計算し、 :attr:`sq_item` に渡します。 :attr:`sq_length` が *NULL*
   の場合は、インデックスはそのままこの関数に渡されます。

.. c:member:: ssizeobjargproc PySequenceMethods.sq_ass_item

   この関数は :c:func:`PySequence_SetItem`
   から利用され、同じシグネチャを持っています。
   このスロットはオブジェクトが要素の代入をサポートしていない場合は
   *NULL* かもしれません。

.. c:member:: objobjproc PySequenceMethods.sq_contains

   この関数は :c:func:`PySequence_Contains`
   から利用され、同じシグネチャを持っています。
   このスロットは *NULL* の場合があり、その時 :c:func:`PySequence_Contains`
   はシンプルにマッチするオブジェクトを見つけるまでシーケンスを巡回します。

.. c:member:: binaryfunc PySequenceMethods.sq_inplace_concat

   この関数は :c:func:`PySequence_InPlaceConcat`
   から利用され、同じシグネチャを持っています。
   この関数は最初のオペランドを修正してそれを返すべきです。

.. c:member:: ssizeargfunc PySequenceMethods.sq_inplace_repeat

   この関数は :c:func:`PySequence_InPlaceRepeat`
   から利用され、同じシグネチャを持っています。
   この関数は最初のオペランドを修正してそれを返すべきです。

.. XXX need to explain precedence between mapping and sequence
.. XXX explains when to implement the sq_inplace_* slots


.. _buffer-structs:

バッファオブジェクト構造体 (buffer object structure)
====================================================

.. sectionauthor:: Greg J. Stein <greg@lyra.org>


バッファインタフェースは、あるオブジェクトの内部データを一連のデータチャンク (chunk) として見せるモデルを外部から利用できるようにします。
各チャンクはポインタ/データ長からなるペアで指定します。チャンクはセグメント(:dfn:`segment`) と呼ばれ、
メモリ内に不連続的に配置されるものと想定されています。

バッファインタフェースを利用できるようにしたくないオブジェクトでは、 :c:type:`PyTypeObject` 構造体の
:attr:`tp_as_buffer` メンバを *NULL* にしなくてはなりません。利用できるようにする場合、 :attr:`tp_as_buffer`
は :c:type:`PyBufferProcs` 構造体を指さねばなりません。

.. note::

   :c:type:`PyTypeObject` 構造体の :attr:`tp_flags` メンバの値を ``0`` でなく
   :const:`Py_TPFLAGS_DEFAULT` にしておくことがとても重要です。この設定は、 :c:type:`PyBufferProcs` 構造体に
   :attr:`bf_getcharbuffer`  スロットが入っていることを Python ランタイムに教えます。 Python の古いバージョンには
   :attr:`bf_getcharbuffer` メンバが存在しないので、古い拡張モジュールを使おうとしている新しいバージョンの Python
   インタプリタは、このメンバがあるかどうかテストしてから使えるようにする必要があるのです。


.. c:type:: PyBufferProcs

   バッファプロトコルの実装を定義している関数群へのポインタを保持するのに使われる構造体です。

   最初のスロットは :attr:`bf_getreadbuffer` で、 :c:type:`getreadbufferproc` 型です。このスロットが
   *NULL* の場合、オブジェクトは内部データの読み出しをサポートしません。そのような仕様には意味がないので、
   実装を行う側はこのスロットに値を埋めるはずですが、呼び出し側では非 *NULL* の値かどうかきちんと調べておくべきです。

   次のスロットは :attr:`bf_getwritebuffer` で、 :c:type:`getwritebufferproc`
   型です。オブジェクトが返すバッファに対して書き込みを許可しない場合はこのスロットを *NULL* にできます。

   第三のスロットは :attr:`bf_getsegcount` で、 :c:type:`getsegcountproc` 型です。このスロットは *NULL*
   であってはならず、オブジェクトにいくつセグメントが入っているかを呼び出し側に教えるために使われます。 :c:type:`PyString_Type` や
   :c:type:`PyBuffer_Type` オブジェクトのような単純なオブジェクトには単一のセグメントしか入っていません。

   .. index:: single: PyType_HasFeature()

   最後のスロットは :attr:`bf_getcharbuffer` で、 :c:type:`getcharbufferproc` です。オブジェクトの
   :c:type:`PyTypeObject` 構造体における :attr:`tp_flags` フィールドに、
   :const:`Py_TPFLAGS_HAVE_GETCHARBUFFER` ビットフラグがセットされている場合にのみ、このスロットが存在することになります。
   このスロットの使用に先立って、呼び出し側は :c:func:`PyType_HasFeature` を使ってスロットが存在するか調べねばなりません。
   フラグが立っていても、 :attr:`bf_getcharbuffer` は *NULL* のときもあり、 *NULL* はオブジェクトの内容を *8 ビット文字列*
   として利用できないことを示します。このスロットに入る関数も、オブジェクトの内容を 8 ビット文字列に
   変換できない場合に例外を送出することがあります。例えば、オブジェクトが浮動小数点数を保持するように設定されたアレイの場合、呼び出し側が
   :attr:`bf_getcharbuffer` を使って 8 ビット文字列としてデータを取り出そうとすると例外を送出するようにできます。
   この、内部バッファを "テキスト" として取り出すという概念は、本質的にはバイナリで、文字ベースの内容を持ったオブジェクト間の区別に使われます。

   .. note::

      現在のポリシでは、文字 (character) はマルチバイト文字でもかまわないと決めているように思われます。従って、サイズ *N* のバッファが *N*
      個のキャラクタからなるとはかぎらないことになります。


.. data:: Py_TPFLAGS_HAVE_GETCHARBUFFER

   型構造体中のフラグビットで、 :attr:`bf_getcharbuffer` スロットが既知の値になっていることを示します。このフラグビットがセット
   されていたとしても、オブジェクトがバッファインタフェースをサポートしていることや、 :attr:`bf_getcharbuffer` スロットが
   *NULL* でないことを示すわけではありません。


.. c:type:: Py_ssize_t (*getreadbufferproc) (PyObject *self, Py_ssize_t segment, void **ptrptr)

   ``*ptrptr`` の中の読み出し可能なバッファセグメントへのポインタを返します。この関数は例外を送出してもよく、送出する場合には ``-1``
   を返さねばなりません。 *segment* に渡す値はゼロまたは正の値で、 :attr:`bf_getsegcount`
   スロット関数が返すセグメント数よりも必ず小さな値でなければなりません。成功すると、セグメントのサイズを返し、 ``*ptrptr`` を
   そのセグメントを指すポインタ値にセットします。


.. c:type:: Py_ssize_t (*getwritebufferproc) (PyObject *self, Py_ssize_t segment, void **ptrptr)

   読み出し可能なバッファセグメントへのポインタを ``*ptrptr`` に返し、セグメントの長さを関数の戻り値として返します。エラーによる例外の場合には
   ``-1`` を ``-1`` を返さねばなりません。オブジェクトが呼び出し専用バッファしかサポートしていない場合には :exc:`TypeError`
   を、 *segment* が存在しないセグメントを指している場合には :exc:`SystemError` を送出しなければなりません。

   .. % Why doesn't it raise ValueError for this one?
   .. % GJS: because you shouldn't be calling it with an invalid
   .. % segment. That indicates a blatant programming error in the C
   .. % code.


.. c:type:: Py_ssize_t (*getsegcountproc) (PyObject *self, Py_ssize_t *lenp)

   バッファを構成するメモリセグメントの数を返します。 *lenp* が *NULL* でない場合、この関数の実装は全てのセグメントのサイズ (バイト単位)
   の合計値を ``*lenp`` を介して報告しなければなりません。この関数呼び出しは失敗させられません。


.. c:type:: Py_ssize_t (*getcharbufferproc) (PyObject *self, Py_ssize_t segment, const char **ptrptr)

   セグメント *segment* のメモリバッファを *ptrptr* に入れ、そのサイズを返します。エラーのときに ``-1`` を返します。


