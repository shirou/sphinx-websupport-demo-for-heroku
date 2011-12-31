.. highlightlang:: c


.. _defining-new-types:

******************
新しい型を定義する
******************

.. sectionauthor:: Michael Hudson <mwh@python.net>
.. sectionauthor:: Dave Kuhlman <dkuhlman@rexx.com>
.. sectionauthor:: Jim Fulton <jim@zope.com>


.. % jp translation: 新山祐介
.. % 翻訳上の注意:
.. % ここで使っている特別な用語があります。
.. % これらの用語では「type」はわざと翻訳せず、カタカナ用語にしています。
.. % ``type method'' タイプメソッド
.. % ``object method'' オブジェクトメソッド
.. % ``type object'' タイプオブジェクト
.. % ``(type) slot'' (タイプ)スロット

前の章でふれたように、Python では拡張モジュールを書くプログラマが Python のコードから操作できる、新しい型を定義できるようになっています。
ちょうど Python の中核にある文字列やリストをつくれるようなものです。

これはそんなにむずかしくはありません。拡張型のためのコードにはすべて、一定のパターンが存在しています。しかし始める前に、いくつか細かいことを
理解しておく必要があるでしょう。

.. note::

   Python 2.2 から、新しい型を定義する方法がかなり変わって (良くなって) います。この文書は Python 2.2 およびそれ以降で
   新しい型をどうやって定義するかについて述べています。古いバージョンの Python をサポートする必要がある場合は、 `この文書の古い版
   <http://www.python.org/doc/versions/>`_ を参照してください。


.. _dnt-basics:

基本的なこと
============

Python ランタイムでは、すべての Python オブジェクトは :c:type:`PyObject\*`
型の変数として扱います。 :c:type:`PyObject` はさほど大仰なオブジェクトではなく、単にオブジェクトに対する参照回数と、
そのオブジェクトの「タイプオブジェクト (type object)」へのポインタを格納しているだけです。
重要な役割を果たしているのはこのタイプオブジェクトです。つまりタイプオブジェクトは、例えばあるオブジェクトのある属性が参照される
とか、あるいは別のオブジェクトとの間で乗算を行うといったときに、どの (C の) 関数を呼び出すかを決定しているのです。これらの C 関数は「タイプメソッド
(type method)」と呼ばれ、  ``[].append`` のようなもの  (いわゆる「オブジェクトメソッド (object method)」)
とは区別しています。

なので、新しいオブジェクトの型を定義したいときは、新しいタイプオブジェクトを作成すればよいわけです。

この手のことは例を見たほうが早いでしょうから、ここに最小限の、しかし完全な、新しい型を定義するモジュールをあげておきます:

.. literalinclude:: ../includes/noddy.c

さしあたって覚えておくことは以上ですが、これで前の章からすこしは説明がわかりやすくなっていることと思います。

最初に習うのは、つぎのようなものです::

   typedef struct {
       PyObject_HEAD
   } noddy_NoddyObject;

これが Noddy オブジェクトの内容です --- このケースでは、ほかの Python オブジェクトが持っているものと何ら変わりはありません。
つまり参照カウントと型オブジェクトへのポインタですね。これらは  ``PyObject_HEAD`` マクロによって
展開されるメンバです。マクロを使う理由は、レイアウトを標準化するためと、デバッグ用ビルド時に特別なデバッグ用のメンバを定義できるようにするためです。この
``PyObject_HEAD`` マクロの後にはセミコロンがないことに注意してください。
セミコロンはすでにマクロ内に含まれています。うっかり後にセミコロンをつけてしまわないように気をつけて。
これはお使いの機種では何の問題も起こらないかもしれませんが、機種によっては、おそらく問題になるのです!  (Windows 上では、MS Visual C
がこの手のエラーを出し、コンパイルできないことが知られています)

比較のため、以下に標準的な Python の整数型の定義を見てみましょう::

   typedef struct {
       PyObject_HEAD
       long ob_ival;
   } PyIntObject;

では次にいってみます。かなめの部分、タイプオブジェクトです。 ::

   static PyTypeObject noddy_NoddyType = {
       PyObject_HEAD_INIT(NULL)
       0,                         /*ob_size*/
       "noddy.Noddy",             /*tp_name*/
       sizeof(noddy_NoddyObject), /*tp_basicsize*/
       0,                         /*tp_itemsize*/
       0,                         /*tp_dealloc*/
       0,                         /*tp_print*/
       0,                         /*tp_getattr*/
       0,                         /*tp_setattr*/
       0,                         /*tp_compare*/
       0,                         /*tp_repr*/
       0,                         /*tp_as_number*/
       0,                         /*tp_as_sequence*/
       0,                         /*tp_as_mapping*/
       0,                         /*tp_hash */
       0,                         /*tp_call*/
       0,                         /*tp_str*/
       0,                         /*tp_getattro*/
       0,                         /*tp_setattro*/
       0,                         /*tp_as_buffer*/
       Py_TPFLAGS_DEFAULT,        /*tp_flags*/
       "Noddy objects",           /* tp_doc */
   };

:file:`object.h` の中にある :c:type:`PyTypeObject` の定義を見ると、
実際にはここに挙げた以上の数のメンバがあるとわかるでしょう。これ以外のメンバは C コンパイラによってゼロに初期化されるので、
必要な時を除いてふつうはそれらの値を明示的には指定せずにおきます。

次のものは非常に重要なので、とくに最初の最初に見ておきましょう::

   PyObject_HEAD_INIT(NULL)

これはちょっとぶっきらぼうですね。実際に書きたかったのはこうです::

   PyObject_HEAD_INIT(&PyType_Type)

この場合、タイプオブジェクトの型は「type」という名前になりますが、これは厳密には C の基準に従っておらず、コンパイラによっては文句を言われます。
幸いにも、このメンバは :c:func:`PyType_Ready` が埋めてくれます。

.. % だからどうした。本題と関係ない。

::

   0,                          /* ob_size */

ヘッダ中の :attr:`ob_size` メンバは使われていません。これは歴史的な遺物であり、構造体中にこれが存在しているのは古いバージョンの
Python 用にコンパイルされた拡張モジュールとのバイナリ上の互換性を保つためです。ここにはつねにゼロを指定してください。 ::

   "noddy.Noddy",              /* tp_name */

これは型の名前です。この名前はオブジェクトのデフォルトの表現形式と、いくつかのエラーメッセージ中で使われます。たとえば::

   >>> "" + noddy.new_noddy()
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: cannot add type "noddy.Noddy" to string

注意: この名前はドットで区切られた名前で、モジュール名と、そのモジュール内での型名を両方ふくんでいます。この場合のモジュールは :mod:`noddy`
で、型の名前は :class:`Noddy` ですから、ここでの型名としては :class:`noddy.Noddy` を指定するわけです。 ::

   sizeof(noddy_NoddyObject),  /* tp_basicsize */

これによって Python は :c:func:`PyObject_New` が呼ばれたときにどれくらいの量のメモリを割り当てればよいのか知ることができます。

.. note::

   あなたのタイプを Python でサブクラス化可能にしたい場合、そのタイプが基底タイプと同じ :attr:`tp_basicsize` をもっていると
   多重継承のときに問題が生じることがあります。そのタイプを Python のサブクラスにしたとき、その :attr:`__bases__` リストにはあなたの
   タイプが最初にくるようにしなければなりません。さもないとエラーの発生なしにあなたのタイプの :meth:`__new__`
   メソッドを呼び出すことはできなくなります。この問題を回避するには、つねにあなたのタイプの :attr:`tp_basicsize` を
   その基底タイプよりも大きくしておくことです。ほとんどの場合、あなたのタイプは :class:`object` か、そうでなければ基底タイプにデータ用の
   メンバを追加したものでしょうから、したがって大きさはつねに増加するためこの条件は満たされています。

::

   0,                          /* tp_itemsize */

これはリストや文字列などの可変長オブジェクトのためのものです。今のところ無視しましょう。

このあとのいくつかのメソッドは使わないのでとばして、クラスのフラグ (flags) には :const:`Py_TPFLAGS_DEFAULT` を入れます。
::

   Py_TPFLAGS_DEFAULT,        /*tp_flags*/

すべての型はフラグにこの定数を含めておく必要があります。これは現在のバージョンの Python で定義されているすべてのメンバを許可します。

この型の docstring は :attr:`tp_doc` に入れます。 ::

   "Noddy objects",           /* tp_doc */

ここからタイプメソッドに入るわけですが。ここがあなたのオブジェクトが他と違うところです。でも今回のバージョンでは、これらはどれも実装しないでおき、
あとでこの例をより面白いものに改造することにしましょう。

とりあえずやりたいのは、この :class:`Noddy` オブジェクトを新しく作れるようにすることです。オブジェクトの作成を許可するには、
:attr:`tp_new` の実装を提供する必要があります。今回は、 API 関数によって提供されるデフォルトの実装
:c:func:`PyType_GenericNew` を使うだけにしましょう。これを単に :attr:`tp_new` スロットに代入すればよいのですが、
これは互換上の理由からできません。プラットフォームやコンパイラによっては、構造体メンバの初期化に別の場所で定義されている C の関数を代入することは
できないのです。なので、この :attr:`tp_new` の値はモジュール初期化用の関数で代入します。 :c:func:`PyType_Ready`
を呼ぶ直前です::

   noddy_NoddyType.tp_new = PyType_GenericNew;
   if (PyType_Ready(&noddy_NoddyType) < 0)
       return;

これ以外のタイプメソッドはすべて *NULL* です。これらについては後ほどふれます。

このファイル中にある他のものは、どれもおなじみでしょう。 :c:func:`initnoddy` のこれを除いて::

   if (PyType_Ready(&noddy_NoddyType) < 0)
       return;

この関数は、上で *NULL* に指定していた  :attr:`ob_type` などのいくつものメンバを埋めて、 :class:`Noddy`
型を初期化します。 ::

   PyModule_AddObject(m, "Noddy", (PyObject *)&noddy_NoddyType);

これはこの型をモジュール中の辞書に埋め込みます。これで、 :class:`Noddy` クラスを呼べば :class:`Noddy` インスタンスを作れるように
なりました::

   >>> import noddy
   >>> mynoddy = noddy.Noddy()

これだけです! 残るはこれをどうやってビルドするかということです。上のコードを :file:`noddy.c` というファイルに入れて、以下のものを
:file:`setup.py` というファイルに入れましょう。 ::

   from distutils.core import setup, Extension
   setup(name="noddy", version="1.0",
         ext_modules=[Extension("noddy", ["noddy.c"])])

そして、シェルから以下のように入力します。 ::

   $ python setup.py build

これでサブディレクトリの下にファイル :file:`noddy.so` が作成されます。このディレクトリに移動して Python を起動しましょう。
``import noddy`` して Noddy オブジェクトで遊べるようになっているはずです。

そんなにむずかしくありません、よね?

もちろん、現在の Noddy 型はまだおもしろみに欠けています。何もデータを持ってないし、何もしてはくれません。
継承してサブクラスを作ることさえできないのです。


基本のサンプルにデータとメソッドを追加する
------------------------------------------

この基本のサンプルにデータとメソッドを追加してみましょう。ついでに、この型を基底クラスとしても利用できるようにします。ここでは新しいモジュール
:mod:`noddy2` をつくり、以下の機能を追加します:

.. literalinclude:: ../includes/noddy2.c

このバージョンでは、いくつもの変更をおこないます。

以下の include を追加します::

   #include <structmember.h>

すこしあとでふれますが、この include には属性を扱うための宣言が入っています。

:class:`Noddy` オブジェクトの構造体の名前は :class:`Noddy` に縮めることにします。タイプオブジェクト名は
:class:`NoddyType` に縮めます。

これから :class:`Noddy` 型は 3つのデータ属性をもつようになります。 *first* 、 *last* 、および *number*
です。 *first* と  *last* 属性はファーストネームとラストネームを格納した Python 文字列で、  *number* 属性は整数の値です。

これにしたがうと、オブジェクトの構造体は次のようになります::

   typedef struct {
       PyObject_HEAD
       PyObject *first;
       PyObject *last;
       int number;
   } Noddy;

いまや管理すべきデータができたので、オブジェクトの割り当てと解放に際してはより慎重になる必要があります。最低限、オブジェクトの解放メソッドが必要です::

   static void
   Noddy_dealloc(Noddy* self)
   {
       Py_XDECREF(self->first);
       Py_XDECREF(self->last);
       self->ob_type->tp_free((PyObject*)self);
   }

この関数は :attr:`tp_dealloc` メンバに代入されます。 ::

   (destructor)Noddy_dealloc, / *tp_dealloc* /

このメソッドでやっているのは、ふたつの Python 属性の参照カウントを減らすことです。 :attr:`first` メンバと :attr:`last`
メンバが *NULL* かもしれないため、ここでは :c:func:`Py_XDECREF` を使いました。このあとそのオブジェクトのタイプメソッドである
:attr:`tp_free` メンバを呼び出しています。ここではオブジェクトの型が :class:`NoddyType` とは限らないことに
注意してください。なぜなら、このオブジェクトはサブクラス化したインスタンスかもしれないからです。

ファーストネームとラストネームを空文字列に初期化しておきたいので、新しいメソッドを追加することにしましょう::

   static PyObject *
   Noddy_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
   {
       Noddy *self;

       self = (Noddy *)type->tp_alloc(type, 0);
       if (self != NULL) {
           self->first = PyString_FromString("");
           if (self->first == NULL)
             {
               Py_DECREF(self);
               return NULL;
             }

           self->last = PyString_FromString("");
           if (self->last == NULL)
             {
               Py_DECREF(self);
               return NULL;
             }

           self->number = 0;
       }

       return (PyObject *)self;
   }

そしてこれを :attr:`tp_new` メンバとしてインストールします::

   Noddy_new,                 /* tp_new */

この新しいメンバはその型のオブジェクトを (初期化するのではなく) 作成する責任を負っています。Python ではこのメンバは :meth:`__new__`
メソッドとして見えています。 :meth:`__new__` メソッドについての詳しい議論は "Unifying types and classes in
Python" という題名の論文を見てください。 new メソッドを実装する理由のひとつは、インスタンス変数の初期値を保証するためです。この例でやりたいのは
new メソッドが :attr:`first` メンバと  :attr:`last` メンバの値を *NULL* でないようにするということです。
もしこれらの初期値が *NULL* でもよいのであれば、先の例でやったように、new メソッドとして :c:func:`PyType_GenericNew` を
使うこともできたでしょう。 :c:func:`PyType_GenericNew` はすべてのインスタンス変数のメンバを *NULL* にします。

この new メソッドは静的なメソッドで、インスタンスを生成するときにその型と、型が呼び出されたときの引数が渡され、新しいオブジェクトを作成して
返します。new メソッドはつねに、あらかじめ固定引数 (positional argument) と
キーワード引数を取りますが、これらのメソッドはしばしばそれらの引数は無視して初期化メソッドにそのまま渡します。new メソッドはメモリ割り当てのために
:attr:`tp_alloc` メンバを呼び出します。 :attr:`tp_alloc` をこちらで初期化する必要はありません。これは
:c:func:`PyType_Ready` が基底クラス (デフォルトでは :class:`object`) をもとに埋めるものです。
ほとんどの型ではデフォルトのメモリ割り当てを使っています。

.. note::

   もし協力的な :attr:`tp_new` (基底タイプの :attr:`tp_new` または :meth:`__new__` を呼んでいるもの)
   を作りたいのならば、実行時のメソッド解決順序をつかってどのメソッドを呼びだすかを決定しようとしては
   *いけません* 。つねに呼び出す型を静的に決めておき、直接その :attr:`tp_new` を呼び出すか、あるいは
   ``type->tp_base->tp_new`` を経由してください。こうしないと、あなたが作成したタイプの Python サブクラスが他の Python
   で定義されたクラスも継承している場合にうまく動かない場合があります。 (とりわけ、そのようなサブクラスのインスタンスを :exc:`TypeError`
   を出さずに作ることが不可能になります。)

つぎに初期化用の関数を見てみましょう::

   static int
   Noddy_init(Noddy *self, PyObject *args, PyObject *kwds)
   {
       PyObject *first=NULL, *last=NULL, *tmp;

       static char *kwlist[] = {"first", "last", "number", NULL};

       if (! PyArg_ParseTupleAndKeywords(args, kwds, "|OOi", kwlist,
                                         &first, &last,
                                         &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_XDECREF(tmp);
       }

       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_XDECREF(tmp);
       }

       return 0;
   }

これは :attr:`tp_init` メンバに代入されます。 ::

   (initproc)Noddy_init,         /* tp_init */

Python では、 :attr:`tp_init` メンバは :meth:`__init__` メソッドとして見えています。
このメソッドは、オブジェクトが作成されたあとに、それを初期化する目的で使われます。 new
メソッドとはちがって、初期化用のメソッドは必ず呼ばれるとは限りません。初期化用のメソッドは、インスタンスの初期値を提供するのに必要な引数を受けとります。
このメソッドはつねに固定引数とキーワード引数を受けとります。

初期化メソッドは複数回呼び出される可能性があります。あなたのオブジェクトの :meth:`__init__` メソッドは、誰にでも呼び出すことができるからです。
このため、新しい値を代入するさいには特別な注意を払う必要があります。たとえば、 :attr:`first`
メンバには以下のように代入したくなるかもしれません::

   if (first) {
       Py_XDECREF(self->first);
       Py_INCREF(first);
       self->first = first;
   }

しかしこのやり方は危険です。このタイプでは :attr:`first` メンバに入るオブジェクトをなにも限定していないので、どんなオブジェクトでも
とり得てしまうからです。それはこのコードが :attr:`first` メンバに
アクセスしようとする前に、そのデストラクタが呼び出されてしまうかもしれないのです。このような可能性からパラノイア的に身をまもるため、ほとんどの場合
メンバへの代入は,その参照カウントを減らす前におこなってください。こうする必要がないのはどんな場合でしょうか?

* その参照カウントが 1 より大きいと確信できる場合。

* そのオブジェクトの解放があなたのタイプのコードにコールバックするようなことが決してない場合 [#]_ 。

* ガベージコレクションがサポートされていない場合に :attr:`tp_dealloc` ハンドラで参照カウントを減らすとき [#]_ 。

ここではインスタンス変数を属性として見えるようにしたいのですが、これにはいくつもの方法があります。
もっとも簡単な方法は、メンバの定義を与えることです::

   static PyMemberDef Noddy_members[] = {
       {"first", T_OBJECT_EX, offsetof(Noddy, first), 0,
        "first name"},
       {"last", T_OBJECT_EX, offsetof(Noddy, last), 0,
        "last name"},
       {"number", T_INT, offsetof(Noddy, number), 0,
        "noddy number"},
       {NULL}  /* Sentinel */
   };

そして、この定義を :attr:`tp_members` に入れましょう::

   Noddy_members,             /* tp_members */

各メンバの定義はそれぞれ、メンバの名前、型、オフセット、アクセスフラグおよび docstring です。詳しくは後の "総称的な属性を管理する" 
(:ref:`Generic-Attribute-Management`) の節をご覧ください。

この方法の欠点は、Python 属性に代入できるオブジェクトの型を制限する方法がないことです。ここではファーストネーム first とラストネーム last
に、ともに文字列が入るよう期待していますが、今のやり方ではどんな Python オブジェクトも代入できてしまいます。加えてこの属性は削除 (del)
できてしまい、その場合、 C のポインタには *NULL* が設定されます。たとえもしメンバが *NULL* 以外の値に初期化されるように
してあったとしても、属性が削除されればメンバは *NULL* になってしまいます。

ここでは :meth:`name` と呼ばれるメソッドを定義しましょう。これはファーストネーム first とラストネーム last を連結した文字列を
そのオブジェクトの名前として返します。 ::

   static PyObject *
   Noddy_name(Noddy* self)
   {
       static PyObject *format = NULL;
       PyObject *args, *result;

       if (format == NULL) {
           format = PyString_FromString("%s %s");
           if (format == NULL)
               return NULL;
       }

       if (self->first == NULL) {
           PyErr_SetString(PyExc_AttributeError, "first");
           return NULL;
       }

       if (self->last == NULL) {
           PyErr_SetString(PyExc_AttributeError, "last");
           return NULL;
       }

       args = Py_BuildValue("OO", self->first, self->last);
       if (args == NULL)
           return NULL;

       result = PyString_Format(format, args);
       Py_DECREF(args);

       return result;
   }

このメソッドは C 関数として実装され、 :class:`Noddy` (あるいは   :class:`Noddy` のサブクラス)
のインスタンスを第一引数として受けとります。メソッドはつねにそのインスタンスを最初の引数として受けとらなければなりません。
しばしば固定引数とキーワード引数も受けとりますが、今回はなにも必要ないので、固定引数のタプルもキーワード引数の辞書も取らないことにします。このメソッドは
Python の以下のメソッドと等価です::

   def name(self):
      return "%s %s" % (self.first, self.last)

:attr:`first` メンバと :attr:`last` メンバがそれぞれ *NULL* かどうかチェックしなければならないことに注意してください。
これらは削除される可能性があり、その場合値は *NULL* にセットされます。この属性の削除を禁止して、そこに入れられる値を文字列に限定できれば
なおいいでしょう。次の節ではこれについて扱います。

さて、メソッドを定義したので、ここでメソッド定義用の配列を作成する必要があります::

   static PyMethodDef Noddy_methods[] = {
       {"name", (PyCFunction)Noddy_name, METH_NOARGS,
        "Return the name, combining the first and last name"
       },
       {NULL}  /* Sentinel */
   };

これを :attr:`tp_methods` スロットに入れましょう::

   Noddy_methods,             /* tp_methods */

ここでの :const:`METH_NOARGS` フラグは、そのメソッドが引数を取らないことを宣言するのに使われています。

最後に、この型を基底クラスとして利用可能にしましょう。上のメソッドは注意ぶかく書かれているので、これはそのオブジェクトの型が
作成されたり利用される場合についてどんな仮定も置いていません。なので、ここですべきことは :const:`Py_TPFLAGS_BASETYPE` を
クラス定義のフラグに加えるだけです::

   Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, / *tp_flags* /

:c:func:`initnoddy` の名前を :c:func:`initnoddy2` に変更し、 :c:func:`Py_InitModule3`
に渡されるモジュール名を更新します。

さいごに :file:`setup.py` ファイルを更新して新しいモジュールをビルドします。 ::

   from distutils.core import setup, Extension
   setup(name="noddy", version="1.0",
         ext_modules=[
            Extension("noddy", ["noddy.c"]),
            Extension("noddy2", ["noddy2.c"]),
            ])


データ属性をこまかく制御する
----------------------------

この節では、 :class:`Noddy` クラスの例にあった :attr:`first` と  :attr:`last`
の各属性にたいして、より精密な制御を提供します。以前のバージョンのモジュールでは、インスタンス変数の :attr:`first` と
:attr:`last` には文字列以外のものも代入できてしまい、あまつさえ削除まで可能でした。
ここではこれらの属性が必ず文字列を保持しているようにしましょう。

.. literalinclude:: ../includes/noddy3.c


:attr:`first` 属性と :attr:`last` 属性をよりこまかく制御するためには、カスタムメイドの getter 関数と setter
関数を使います。以下は :attr:`first` 属性から値を取得する関数 (getter) と、この属性に値を格納する関数 (setter) です::

   Noddy_getfirst(Noddy *self, void *closure)
   {
       Py_INCREF(self->first);
       return self->first;
   }

   static int
   Noddy_setfirst(Noddy *self, PyObject *value, void *closure)
   {
     if (value == NULL) {
       PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
       return -1;
     }

     if (! PyString_Check(value)) {
       PyErr_SetString(PyExc_TypeError,
                       "The first attribute value must be a string");
       return -1;
     }

     Py_DECREF(self->first);
     Py_INCREF(value);
     self->first = value;

     return 0;
   }

getter 関数には :class:`Noddy` オブジェクトと「閉包 (closure)」 (これは void型のポインタです)
が渡されます。今回のケースでは閉包は無視します。 (閉包とは定義データが渡される setter や getter の高度な利用をサポートするためのもので、
これを使うとたとえば getter と setter をひとまとめにした関数に、閉包のデータにもとづいて属性を get するか set するか決めさせる、
といったことができます。)

setter 関数には :class:`Noddy` オブジェクトと新しい値、そして閉包が渡されます。新しい値は
*NULL* かもしれず、その場合はこの属性が削除されます。ここでは属性が削除されたり、その値が文字列でないときにはエラーを発生させるようにします。

ここでは :c:type:`PyGetSetDef` 構造体の配列をつくります::

   static PyGetSetDef Noddy_getseters[] = {
       {"first",
        (getter)Noddy_getfirst, (setter)Noddy_setfirst,
        "first name",
        NULL},
       {"last",
        (getter)Noddy_getlast, (setter)Noddy_setlast,
        "last name",
        NULL},
       {NULL}  /* Sentinel */
   };

そしてこれを :attr:`tp_getset` スロットに登録します::

   Noddy_getseters,           /* tp_getset */

これで属性の getter と setter が登録できました。

:c:type:`PyGetSetDef` 構造体の最後の要素が上で説明した閉包です。今回は閉包は使わないので *NULL* を渡しています。

また、メンバ定義からはこれらの属性を除いておきましょう::

   static PyMemberDef Noddy_members[] = {
       {"number", T_INT, offsetof(Noddy, number), 0,
        "noddy number"},
       {NULL}  /* Sentinel */
   };

また、ここでは :attr:`tp_init` ハンドラも渡されるものとして文字列のみを許可するように修正する必要があります  [#]_::

   static int
   Noddy_init(Noddy *self, PyObject *args, PyObject *kwds)
   {
       PyObject *first=NULL, *last=NULL, *tmp;

       static char *kwlist[] = {"first", "last", "number", NULL};

       if (! PyArg_ParseTupleAndKeywords(args, kwds, "|SSi", kwlist,
                                         &first, &last,
                                         &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_DECREF(tmp);
       }

       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_DECREF(tmp);
       }

       return 0;
   }

これらの変更によって、 :attr:`first` メンバと :attr:`last` メンバが決して *NULL*
にならないと保証できました。これでほとんどすべてのケースから *NULL* 値のチェックを除けます。これは :c:func:`Py_XDECREF` 呼び出しを
:c:func:`Py_DECREF` 呼び出しに変えられることを意味します。唯一これを変えられないのはオブジェクト解放メソッド (deallocator)
で、なぜならここではコンストラクタによるメンバ初期化が失敗している可能性があるからです。

さて、先ほどもしたように、このモジュール初期化関数と初期化関数内にあるモジュール名を変更しましょう。そして :file:`setup.py`
ファイルに追加の定義をくわえます。


循環ガベージコレクションをサポートする
--------------------------------------

Python は循環ガベージコレクション機能をもっており、これは不要なオブジェクトを、たとえ参照カウントがゼロでなくても、発見することができます。
これはオブジェクトの参照が循環しているときに起こりえます。たとえば以下の例を考えてください::

   >>> l = []
   >>> l.append(l)
   >>> del l

この例では、自分自身をふくむリストをつくりました。たとえこのリストを del しても、それは自分自身への参照をまだ持ちつづけますから、参照カウントは
ゼロにはなりません。嬉しいことに Python には循環ガベージコレクション機能がありますから、最終的にはこのリストが不要であることを検出し、解放できます。

:class:`Noddy` クラスの 2番目の例では、 :attr:`first` 属性と :attr:`last`
属性にどんなオブジェクトでも格納できるようになっていました。  [#]_ 。つまり、 :class:`Noddy` オブジェクトの参照は循環しうるのです::

   >>> import noddy2
   >>> n = noddy2.Noddy()
   >>> l = [n]
   >>> n.first = l

これは実にばかげた例ですが、すくなくとも :class:`Noddy` クラスに循環ガベージコレクション機能のサポートを加える口実を与えてくれます。
循環ガベージコレクションをサポートするには 2つのタイプスロットを埋め、これらのスロットを許可するようにクラス定義のフラグを設定する必要があります:

.. literalinclude:: ../includes/noddy4.c


traversal メソッドは循環した参照に含まれる可能性のある内部オブジェクトへのアクセスを提供します::

   static int
   Noddy_traverse(Noddy *self, visitproc visit, void *arg)
   {
       int vret;

       if (self->first) {
           vret = visit(self->first, arg);
           if (vret != 0)
               return vret;
       }
       if (self->last) {
           vret = visit(self->last, arg);
           if (vret != 0)
               return vret;
       }

       return 0;
   }

循環した参照に含まれるかもしれない各内部オブジェクトに対して、 traversal メソッドに渡された :c:func:`visit` 関数を呼びます。
:c:func:`visit` 関数は内部オブジェクトと、traversal メソッドに渡された追加の引数 *arg* を引数としてとります。
この関数はこの値が非負の場合に返される整数の値を返します。

Python 2.4 以降では、visit 関数の呼び出しを自動化する :c:func:`Py_VISIT` マクロが用意されています。
:c:func:`Py_VISIT` を使えば、 :c:func:`Noddy_traverse` は次のように簡略化できます::

   static int
   Noddy_traverse(Noddy *self, visitproc visit, void *arg)
   {
       Py_VISIT(self->first);
       Py_VISIT(self->last);
       return 0;
   }

.. note::

   注意: :attr:`tp_traverse` の実装で :c:func:`Py_VISIT` を使うには、その引数に正確に *visit* および *arg*
   という名前をつける必要があります。これは、この退屈な実装に統一性を導入することを促進します。

また、循環した参照に含まれた内部オブジェクトを消去するためのメソッドも提供する必要があります。オブジェクト解放用のメソッドを再実装して、
このメソッドに使いましょう::

   static int
   Noddy_clear(Noddy *self)
   {
       PyObject *tmp;

       tmp = self->first;
       self->first = NULL;
       Py_XDECREF(tmp);

       tmp = self->last;
       self->last = NULL;
       Py_XDECREF(tmp);

       return 0;
   }

   static void
   Noddy_dealloc(Noddy* self)
   {
       Noddy_clear(self);
       self->ob_type->tp_free((PyObject*)self);
   }

:c:func:`Noddy_clear` 中での一時変数の使い方に注目してください。ここでは、一時変数をつかって各メンバの参照カウントを減らす前にそれらに
*NULL* を代入しています。これは次のような理由によります。すでにお話ししたように、もし参照カウントがゼロになると、このオブジェクトが
コールバックされるようになってしまいます。さらに、いまやガベージコレクションをサポートしているため、ガベージコレクション時に実行される
コードについても心配しなくてはなりません。もしガベージコレクションが走っていると、あなたの :attr:`tp_traverse` ハンドラが呼び出される
可能性があります。メンバの参照カウントがゼロになった場合に、その値が *NULL* に設定されていないと :c:func:`Noddy_traverse` が
呼ばれる機会はありません。

Python 2.4 以降では、注意ぶかく参照カウントを減らすためのマクロ :c:func:`Py_CLEAR` が用意されています。
:c:func:`Py_CLEAR` を使えば、 :c:func:`Noddy_clear` は次のように簡略化できます::

   static int
   Noddy_clear(Noddy *self)
   {
       Py_CLEAR(self->first);
       Py_CLEAR(self->last);
       return 0;
   }

最後に、 :const:`Py_TPFLAGS_HAVE_GC` フラグをクラス定義のフラグに加えます::

   Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC, / *tp_flags* /

これで完了です。 :attr:`tp_alloc` スロットまたは :attr:`tp_free` スロットが
書かれていれば、それらを循環ガベージコレクションに使えるよう修正すればよいのです。ほとんどの拡張機能は自動的に提供されるバージョンを使うでしょう。


他の型のサブクラスを作る
-------------------------

既存の型を継承した新しい拡張型を作成することができます。
組み込み型から継承するのは特に簡単です。必要な :class:`PyTypeObject` を簡単に利用できるからです。
それに比べて、 :class:`PyTypeObject` 構造体を拡張モジュール間で共有するのは難しいです。

次の例では、ビルトインの :class:`list` 型を継承した :class:`Shoddy` 型を作成しています。
新しい型は通常のリスト型と完全に互換性がありますが、追加で内部のカウンタを増やす
:meth:`increment` メソッドを持っています。 ::

   >>> import shoddy
   >>> s = shoddy.Shoddy(range(3))
   >>> s.extend(s)
   >>> print len(s)
   6
   >>> print s.increment()
   1
   >>> print s.increment()
   2

.. literalinclude:: ../includes/shoddy.c


見てわかるように、ソースコードは前の節の :class:`Noddy` の時と非常に似ています。
違う部分をそれぞれを見ていきます。 ::

   typedef struct {
       PyListObject list;
       int state;
   } Shoddy;

継承した型のオブジェクトの最初の違いは、親クラスのオブジェクト構造が最初に必要なことです。
基底型が既に :c:func:`PyObject_HEAD` を構造体の先頭に持っています。

Python オブジェクトが :class:`Shoddy` 型のインスタンスだった場合、
その *PyObject\** ポインタは *PyListObject\** にも *Shoddy\** にも安全にキャストできます。

::

   static int
   Shoddy_init(Shoddy *self, PyObject *args, PyObject *kwds)
   {
       if (PyList_Type.tp_init((PyObject *)self, args, kwds) < 0)
          return -1;
       self->state = 0;
       return 0;
   }

この新しい型の :attr:`__init__` メソッドで、基底型の :attr:`__init__`
メソッドを呼び出している様子を見ることができます。

このパターンは、カスタムの :attr:`new` と :attr:`dealloc` メソッドを実装するときには重要です。
継承した型の :attr:`new` メソッドは、 :attr:`tp_alloc` を使ってメモリを割り当てるべきではありません。
それは基底型の :attr:`tp_new` を呼出たときに処理されるからです。

:class:`Shoddy` 型のために :c:func:`PyTypeObject` を埋めるとき、
:c:func:`tp_base` スロットを見つけることができます。
クロスプラットフォームのコンパイラに対応するために、直接そのスロットを :c:func:`PyList_Type`
で埋めてはいけません。代わりに、後でモジュールの :c:func:`init` 関数の中で行うことができます。 ::

   PyMODINIT_FUNC
   initshoddy(void)
   {
       PyObject *m;

       ShoddyType.tp_base = &PyList_Type;
       if (PyType_Ready(&ShoddyType) < 0)
           return;

       m = Py_InitModule3("shoddy", NULL, "Shoddy module");
       if (m == NULL)
           return;

       Py_INCREF(&ShoddyType);
       PyModule_AddObject(m, "Shoddy", (PyObject *) &ShoddyType);
   }

:c:func:`PyType_Read` を呼ぶ前に、型の構造は :attr:`tp_base` スロットは埋められていなければなりません。
継承している新しい型を作るとき、 :attr:`tp_alloc` スロットを :c:func:`PyType_GenericNew`
で埋める必要はありません。 -- 基底型のアロケート関数が継承されます。

その後、 :c:func:`PyType_Read` を呼んで、 :class:`Noddy` の時と同じように
タイプオブジェクトをモジュールに追加します。

.. todo::
   a*

.. _dnt-type-methods:

タイプメソッド
==============

この節ではさまざまな実装可能なタイプメソッドと、それらが何をするものであるかについて、ざっと説明します。

以下は :c:type:`PyTypeObject` の定義です。デバッグビルドでしか使われないいくつかのメンバは省いてあります:

.. literalinclude:: ../includes/typestruct.h


*たくさんの* メソッドがありますね。
でもそんなに心配する必要はありません。定義したい型があるなら、実装するのはこのうちのごくわずかですむことがほとんどです。

すでに予想されているでしょうが、これらの多様なハンドラについて、これからより詳しい情報を提供します。しかしこれらのメンバが構造体中で
定義されている順番は無視します。というのは、これらのメンバの現れる順序は歴史的な遺産によるものだからです。型を初期化するさいに、これらの
メンバを正しい順序で並べるよう、くれぐれも注意してください。ふつういちばん簡単なのは、必要なメンバがすべて含まれている (たとえそれらが ``0``
に初期化されていても) 例をとってきて、自分の型に合わせるよう変更をくわえることです。 ::

   char *tp_name; /* 表示用 */

これは型の名前です。前節で説明したように、これはいろいろな場面で現れ、ほとんどは診断用の目的で使われるものです。
なので、そのような場面で役に立つであろう名前を選んでください。 ::

   int tp_basicsize, tp_itemsize; /* 割り当て用 */

これらのメンバは、この型のオブジェクトが作成されるときにどれだけのメモリを割り当てればよいのかをランタイムに指示します。Python には可変長の構造体
(文字列やリストなどを想像してください) に対する組み込みのサポートがある程度あり、ここで :attr:`tp_itemsize` メンバが使われます。
これらについてはあとでふれます。 ::

   char *tp_doc;

ここには Python スクリプトリファレンス ``obj.__doc__`` が doc string を返すときの文字列 (あるいはそのアドレス)
を入れます。

では次に、ほとんどの拡張型が実装するであろう基本的なタイプメソッドに入っていきます。


最終化 (finalization) と解放
----------------------------

.. index::
   single: object; deallocation
   single: deallocation, object
   single: object; finalization
   single: finalization, of objects

::

   destructor tp_dealloc;

型のインスタンスの参照カウントがゼロになり、 Python インタプリタがそれを潰して再利用したくなると、
この関数が呼ばれます。解放すべきメモリをその型が保持していたり、それ以外にも実行すべき後処理がある場合は、それらをここに入れます。
オブジェクトそれ自体もここで解放される必要があります。この関数の例は、以下のようなものです::

   static void
   newdatatype_dealloc(newdatatypeobject * obj)
   {
       free(obj->obj_UnderlyingDatatypePtr);
       obj->ob_type->tp_free(obj);
   }

.. index::
   single: PyErr_Fetch()
   single: PyErr_Restore()

解放用関数でひとつ重要なのは、処理待ちの例外にいっさい手をつけないことです。なぜなら、解放用の関数は Python
インタプリタがスタックを元の状態に戻すときに呼ばれることが多いからです。そして (通常の関数からの復帰でなく) 例外のために
スタックが巻き戻されるときは、すでに発生している例外から解放用関数を守るものはありません。解放用の関数がおこなう動作が追加の Python のコードを
実行してしまうと、それらは例外が発生していることを検知するかもしれません。これはインタプリタが誤解させるエラーを発生させることにつながります。
これを防ぐ正しい方法は、安全でない操作を実行する前に処理待ちの例外を保存しておき、終わったらそれを元に戻すことです。これは
:c:func:`PyErr_Fetch` および :c:func:`PyErr_Restore` 関数を使うことによって可能になります::

   static void
   my_dealloc(PyObject *obj)
   {
       MyObject *self = (MyObject *) obj;
       PyObject *cbresult;

       if (self->my_callback != NULL) {
           PyObject *err_type, *err_value, *err_traceback;
           int have_error = PyErr_Occurred() ? 1 : 0;

           if (have_error)
               PyErr_Fetch(&err_type, &err_value, &err_traceback);

           cbresult = PyObject_CallObject(self->my_callback, NULL);
           if (cbresult == NULL)
               PyErr_WriteUnraisable();
           else
               Py_DECREF(cbresult);

           if (have_error)
               PyErr_Restore(err_type, err_value, err_traceback);

           Py_DECREF(self->my_callback);
       }
       obj->ob_type->tp_free((PyObject*)self);
   }


オブジェクト表現
-------------------

.. index::
   builtin: repr
   builtin: str

Python では、オブジェクトの文字列表現を生成するのに 3つのやり方があります: :func:`repr` 関数 (あるいはそれと等価な
バッククォートを用いた表現) を使う方法、 :func:`str`  関数を使う方法、そして :keyword:`print` 文を使う方法です。
ほとんどのオブジェクトで :keyword:`print` 文は :func:`str` 関数と同じですが、必要な場合には特殊なケースとして
:c:type:`FILE\*` にも表示できます。 :c:type:`FILE\*` への表示は、効率が問題となっている場合で、一時的な
文字列オブジェクトを作成してファイルに書き込むのでは効率が悪すぎることがプロファイリングからも明らかな場合にのみ使うべきです。

これらのハンドラはどれも必須ではありません。ほとんどの型ではせいぜい :attr:`tp_str` ハンドラと :attr:`tp_repr`
ハンドラを実装するだけですみます。 ::

   reprfunc tp_repr;
   reprfunc tp_str;
   printfunc tp_print;

:attr:`tp_repr` ハンドラは呼び出されたインスタンスの文字列表現を
格納した文字列オブジェクトを返す必要があります。簡単な例は以下のようなものです::

   static PyObject *
   newdatatype_repr(newdatatypeobject * obj)
   {
       return PyString_FromFormat("Repr-ified_newdatatype{{size:\%d}}",
                                  obj->obj_UnderlyingDatatypePtr->size);
   }

:attr:`tp_repr` ハンドラが指定されていなければ、インタプリタはその型の :attr:`tp_name`
とそのオブジェクトの一意な識別値をもちいて文字列表現を作成します。

:attr:`tp_str` ハンドラと :func:`str` の関係は、上の :attr:`tp_repr` ハンドラと :func:`repr`
の関係に相当します。つまり、これは Python のコードがオブジェクトのインスタンスに対して :func:`str`
を呼び出したときに呼ばれます。この関数の実装は :attr:`tp_repr` ハンドラのそれと非常に似ていますが、得られる文字列表現は
人間が読むことを意図されています。 :attr:`tp_str` が指定されていない場合、かわりに :attr:`tp_repr` ハンドラが使われます。

以下は簡単な例です::

   static PyObject *
   newdatatype_str(newdatatypeobject * obj)
   {
       return PyString_FromFormat("Stringified_newdatatype{{size:\%d}}",
                                  obj->obj_UnderlyingDatatypePtr->size);
   }

print ハンドラは Python がその型のインスタンスを「print する」必要のあるときに毎回呼ばれます。たとえば 'node' が TreeNode
型のインスタンスだとすると、print ハンドラは Python が以下を実行したときに呼ばれます::

   print node

flags 引数には :const:`Py_PRINT_RAW` というフラグがあり、これはその文字列をクォートやおそらくはエスケープシーケンスの解釈もなしで
表示することを指示します。

この print 関数は :c:type:`FILE\*` オブジェクトを引数としてとります。たぶん、ここに出力することになるでしょう。

print 関数の例は以下のようになります::

   static int
   newdatatype_print(newdatatypeobject *obj, FILE *fp, int flags)
   {
       if (flags & Py_PRINT_RAW) {
           fprintf(fp, "<{newdatatype object--size: %d}>",
                   obj->obj_UnderlyingDatatypePtr->size);
       }
       else {
           fprintf(fp, "\"<{newdatatype object--size: %d}>\"",
                   obj->obj_UnderlyingDatatypePtr->size);
       }
       return 0;
   }


属性を管理する
--------------

属性をもつどのオブジェクトに対しても、その型は、それらオブジェクトの属性をどのように解決するか制御する関数を提供する
必要があります。必要な関数としては、属性を (それが定義されていれば) 取り出すものと、もうひとつは属性に (それが許可されていれば) 値を
設定するものです。属性を削除するのは特殊なケースで、この場合は新しい値としてハンドラに *NULL* が渡されます。

Python は 2つの属性ハンドラの組をサポートしています。属性をもつ型はどちらか一組を実装するだけでよく、それらの違いは一方の組が属性の名前を
:c:type:`char\*` として受け取るのに対してもう一方の組は属性の名前を :c:type:`PyObject\*` として受け取る、というものです。
それぞれの型はその実装にとって都合がよい方を使えます。 ::

   getattrfunc  tp_getattr;        /* char * バージョン */
   setattrfunc  tp_setattr;
   /* ... */
   getattrofunc tp_getattrofunc;   /* PyObject * バージョン */
   setattrofunc tp_setattrofunc;

オブジェクトの属性へのアクセスがつねに (すぐあとで説明する) 単純な操作だけならば、 :c:type:`PyObject\*` を使って属性を管理する
関数として、総称的 (generic) な実装を使えます。特定の型に特化した属性ハンドラの必要性は Python 2.2 からほとんど完全に
なくなりました。しかし、多くの例はまだ、この新しく使えるようになった総称的なメカニズムを使うよう更新されてはいません。


.. _generic-attribute-management:

総称的な属性を管理する
^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.2

ほとんどの型は *単純な* 属性を使うだけです。では、どのような属性が単純だといえるのでしょうか? それが満たすべき条件はごくわずかです:

#. :c:func:`PyType_Ready` が呼ばれたとき、すでに属性の名前がわかっていること。

#. 属性を参照したり設定したりするときに、特別な記録のための処理が必要でなく、また参照したり設定した値に対してどんな操作も実行する必要がないこと。

これらの条件は、属性の値や、値が計算されるタイミング、または格納されたデータがどの程度妥当なものであるかといったことに
なんら制約を課すものではないことに注意してください。

:c:func:`PyType_Ready` が呼ばれると、これはそのタイプオブジェクトに参照されている
3つのテーブルを使って、そのタイプオブジェクトの辞書中にデスクリプタ(:term:`descriptor`) を作成します。
各デスクリプタは、インスタンスオブジェクトの属性に
対するアクセスを制御します。それぞれのテーブルはなくてもかまいません。もしこれら 3つがすべて *NULL* だと、その型のインスタンスはその基底型から
継承した属性だけを持つことになります。また、 :attr:`tp_getattro` および :attr:`tp_setattro` が *NULL*
のままだった場合も、基底型にこれらの属性の操作がまかせられます。

テーブルはタイプオブジェクト中の 3つのメンバとして宣言されています::

   struct PyMethodDef *tp_methods;
   struct PyMemberDef *tp_members;
   struct PyGetSetDef *tp_getset;

:attr:`tp_methods` が *NULL* でない場合、これは :c:type:`PyMethodDef` 構造体への配列を指している必要があります。
テーブル中の各エントリは、つぎのような構造体のインスタンスです::

   typedef struct PyMethodDef {
       char        *ml_name;       /* メソッド名 */
       PyCFunction  ml_meth;       /* 実装する関数 */
       int          ml_flags;      /* flags */
       char        *ml_doc;        /* docstring */
   } PyMethodDef;

その型が提供する各メソッドについてひとつのエントリを定義する必要があります。基底型から継承してきたメソッドについてはエントリは必要ありません。
これの最後には、配列の終わりを示すための見張り番 (sentinel) として追加のエントリがひとつ必要です。この場合、 :attr:`ml_name`
メンバが sentinel として使われ、その値は *NULL* でなければなりません。

2番目のテーブルは、インスタンス中に格納されるデータと直接対応づけられた属性を定義するのに使います。いくつもの C の原始的な型がサポートされており、
アクセスを読み込み専用にも読み書き可能にもできます。このテーブルで使われる構造体は次のように定義されています:

.. % XXX 次の章もふくめて、構造体の各メンバに対するなんらかの統一した説明が必要。

::

   typedef struct PyMemberDef {
       char *name;
       int   type;
       int   offset;
       int   flags;
       char *doc;
   } PyMemberDef;

このテーブルの各エントリに対してデスクリプタ(:term:`descriptor`)が作成され、
値をインスタンスの構造体から抽出しうる型に対してそれらが追加されます。 :attr:`type`
メンバは :file:`structmember.h` ヘッダで定義された型のコードをひとつ含んでいる必要があります。この値は Python における値と
C における値をどのように変換しあうかを定めるものです。 :attr:`flags` メンバはこの属性がどのようにアクセスされるかを制御する
フラグを格納するのに使われます。

以下のフラグ用定数は :file:`structmember.h` で定義されており、これらはビットごとの OR を取って組み合わせられます。

.. % XXX これらのいくつかを共通の節に移すこと!

+---------------------------+---------------------------------------------------------+
| Constant                  | Meaning                                                 |
+===========================+=========================================================+
| :const:`READONLY`         | 絶対に変更できない。                                    |
+---------------------------+---------------------------------------------------------+
| :const:`RO`               | :const:`READONLY` の短縮形。                            |
+---------------------------+---------------------------------------------------------+
| :const:`READ_RESTRICTED`  | 制限モード (restricted mode) では参照できない。         |
+---------------------------+---------------------------------------------------------+
| :const:`WRITE_RESTRICTED` | 制限モード (restricted mode) では変更できない。         |
+---------------------------+---------------------------------------------------------+
| :const:`RESTRICTED`       | 制限モード (restricted mode) では参照も変更もできない。 |
+---------------------------+---------------------------------------------------------+

.. index::
   single: READONLY
   single: RO
   single: READ_RESTRICTED
   single: WRITE_RESTRICTED
   single: RESTRICTED

:attr:`tp_members` を使ったひとつの面白い利用法は、実行時に使われる
デスクリプタを作成しておき、単にテーブル中にテキストを置いておくことによって、この方法で定義されたすべての属性に doc string を関連付けられるように
することです。アプリケーションはこのイントロスペクション用 API を使って、クラスオブジェクトからデスクリプタを取り出し、その
:attr:`__doc__` 属性を使って doc string を得られます。

:attr:`tp_methods` テーブルと同じように、ここでも :attr:`name` メンバの値を *NULL* にした見張り用エントリが必要です。

.. % XXX デスクリプタについてはどこかでもっと詳しく説明する必要がある。でもそれはここではない。
.. %
.. % デスクリプタオブジェクトは 2つのハンドラ用関数をもっており、これらは
.. % \member{tp_getattro} および \member{tp_setattro} ハンドラに対応しています。
.. % \method{__get__()} ハンドラはデスクリプタとインスタンス、そしてタイプオブジェクトが
.. % 渡される関数で、その属性の値を返すか、あるいは \NULL{} を返して例外を
.. % 発生させるものです。\method{__set__()} ハンドラにはデスクリプタとインスタンス、型、
.. % そして新しい値が渡されます。


特定の型に特化した属性の管理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

話を単純にするため、ここでは :c:type:`char\*` を使ったバージョンのみを示します。name パラメータの型はインターフェイスとして
:c:type:`char\*` を使うか :c:type:`PyObject\*` を使うかの違いしかありません。
この例では、上の総称的な例と同じことを効率的にやりますが、 Python 2.2 で追加された総称的な型のサポートを使わずにやります。これを紹介することは
2つの意味をもっています。ひとつはどうやって、古いバージョンの Python と互換性のあるやり方で、基本的な属性管理を
おこなうか。そしてもうひとつはハンドラの関数がどのようにして呼ばれるのか。これで、たとえその機能を拡張する必要があるとき、何をどうすればいいか
わかるでしょう。

:attr:`tp_getattr` ハンドラはオブジェクトが属性への参照を要求するときに呼ばれます。これは、そのクラスの
:meth:`__getattr__` メソッドが呼ばれるであろう状況と同じ状況下で呼び出されます。

これを処理するありがちな方法は、(1) 一連の関数 (下の例の  :c:func:`newdatatype_getSize` や
:c:func:`newdatatype_setSize`) を実装する、(2) これらの関数を記録したメソッドテーブルを提供する、そして (3)
そのテーブルの参照結果を返す getattr 関数を提供することです。メソッドテーブルはタイプオブジェクトの :attr:`tp_methods` メンバと
同じ構造を持っています。

以下に例を示します::

   static PyMethodDef newdatatype_methods[] = {
       {"getSize", (PyCFunction)newdatatype_getSize, METH_VARARGS,
        "Return the current size."},
       {"setSize", (PyCFunction)newdatatype_setSize, METH_VARARGS,
        "Set the size."},
       {NULL, NULL, 0, NULL}           /* 見張り */
   };

   static PyObject *
   newdatatype_getattr(newdatatypeobject *obj, char *name)
   {
       return Py_FindMethod(newdatatype_methods, (PyObject *)obj, name);
   }

:attr:`tp_setattr` ハンドラは、クラスのインスタンスの :meth:`__setattr__` または :meth:`__delattr__`
メソッドが呼ばれるであろう状況で呼び出されます。ある属性が削除されるとき、3番目のパラメータは *NULL* に
なります。以下の例はたんに例外を発生させるものですが、もし本当にこれと同じことをしたいなら、 :attr:`tp_setattr` ハンドラを
*NULL* に設定すべきです。 ::

   static int
   newdatatype_setattr(newdatatypeobject *obj, char *name, PyObject *v)
   {
       (void)PyErr_Format(PyExc_RuntimeError, "Read-only attribute: \%s", name);
       return -1;
   }


オブジェクトの比較
------------------

::

   cmpfunc tp_compare;

:attr:`tp_compare` ハンドラは、オブジェクトどうしの比較が必要で、
そのオブジェクトに要求された比較をおこなうのに適した特定の拡張比較メソッドが実装されていないときに呼び出されます。(これが定義されているとき、
:c:func:`PyObject_Compare` または :c:func:`PyObject_Cmp` が使われるとこれはつねに呼び出されます、また
Python で :func:`cmp` が使われたときにも呼び出されます。) これは :meth:`__cmp__` メソッドに似ています。この関数はもし
*obj1* が *obj2* より「小さい」場合は ``-1`` を返し、それらが等しければ ``0`` 、そしてもし *obj1* が *obj2* より
「大きい」場合は ``1`` を返す必要があります。 (以前は大小比較の結果として、任意の大きさの負または正の整数を返せましたが、 Python 2.2
以降ではこれはもう許されていません。将来的には、上にあげた以外の返り値は別の意味をもつ可能性があります。)

:attr:`tp_compare` ハンドラは例外を発生させられます。この場合、この関数は負の値を返す必要があります。呼び出した側は
:c:func:`PyErr_Occurred` を使って例外を検査しなければなりません。

以下はサンプル実装です::

   static int
   newdatatype_compare(newdatatypeobject * obj1, newdatatypeobject * obj2)
   {
       long result;

       if (obj1->obj_UnderlyingDatatypePtr->size <
           obj2->obj_UnderlyingDatatypePtr->size) {
           result = -1;
       }
       else if (obj1->obj_UnderlyingDatatypePtr->size >
                obj2->obj_UnderlyingDatatypePtr->size) {
           result = 1;
       }
       else {
           result = 0;
       }
       return result;
   }


抽象的なプロトコルのサポート
----------------------------

Python はいくつもの *抽象的な* “プロトコル”をサポートしています
。これらを使用する特定のインターフェイスについては :ref:`abstract` で解説されています。

これら多数の抽象的なインターフェイスは、Python の実装が開発される初期の段階で定義されていました。とりわけ数値や辞書、そしてシーケンスなどの
プロトコルは最初から Python の一部だったのです。それ以外のプロトコルはその後追加されました。
型の実装にあるいくつかのハンドラルーチンに依存するようなプロトコルのために、古いプロトコルはハンドラの入ったオプションのブロックとして
定義し、型オブジェクトから参照するようになりました。タイプオブジェクトの主部に追加のスロットをもつ新しいプロトコルについては、
フラグ用のビットを立てることでそれらのスロットが存在しており、インタプリタがチェックすべきであることを指示できます。
(このフラグ用のビットは、そのスロットの値が非 *NULL* であることを示しているわけではありません。フラグはスロットの存在を示すのに使えますが、
そのスロットはまだ埋まっていないかもしれないのです。)

.. % 型の実装からいくつかのハンドラ関数に依存しているプロトコルについては、
.. % 古いプロトコルは、そのタイプオブジェクトから参照されている付加的な
.. % ハンドラ部分として定義されています。
.. % (訳註: この文は意味不明。
.. % 原文は ``For protocols which depend on several handler routines from the
.. % type implementation, the older protocols have been defined as
.. % optional blocks of handlers referenced by the type object.'')

::

   PyNumberMethods   tp_as_number;
   PySequenceMethods tp_as_sequence;
   PyMappingMethods  tp_as_mapping;

お使いのオブジェクトを数値やシーケンス、あるいは辞書のようにふるまうようにしたいならば、それぞれに C の :c:type:`PyNumberMethods`
構造体、 :c:type:`PySequenceMethods` 構造体、または :c:type:`PyMappingMethods`  構造体のアドレスを
入れます。これらに適切な値を入れても入れなくてもかまいません。これらを使った例は Python の配布ソースにある :file:`Objects` で
みつけることができるでしょう。 ::

   hashfunc tp_hash;

この関数は、もし使うのならば、これはお使いの型のインスタンスのハッシュ番号を返すようにします。以下はやや的はずれな例ですが ::

   static long
   newdatatype_hash(newdatatypeobject *obj)
   {
       long result;
       result = obj->obj_UnderlyingDatatypePtr->size;
       result = result * 3;
       return result;
   }

::

   ternaryfunc tp_call;

この関数は、その型のインスタンスが「関数として呼び出される」ときに呼ばれます。たとえばもし ``obj1`` にそのインスタンスが入っていて、Python
スクリプトで ``obj1('hello')`` を実行したとすると、 :attr:`tp_call` ハンドラが呼ばれます。

この関数は 3つの引数をとります:

#. *arg1* にはその呼び出しの対象となる、そのデータ型のインスタンスが入ります。たとえば呼び出しが ``obj1('hello')``
   の場合、 *arg1* は ``obj1`` になります。

#. *arg2* は呼び出しの引数を格納しているタプルです。ここから引数を取り出すには :c:func:`PyArg_ParseTuple` を使います。

#. *arg3* はキーワード引数のための辞書です。これが *NULL* 以外で
   キーワード引数をサポートしているなら、 :c:func:`PyArg_ParseTupleAndKeywords`
   をつかって引数を取り出せます。キーワード引数をサポートしていないのにこれが *NULL* 以外の場合は、キーワード引数はサポートしていない旨の
   メッセージとともに :exc:`TypeError` を発生させてください。

以下はこの call 関数をてきとうに使った例です。 ::

   /* call 関数の実装。
    *    obj1 : 呼び出しを受けるインスタンス。
    *    obj2 : 呼び出しのさいの引数を格納するタプル、この場合は 3つの文字列。
    */
   static PyObject *
   newdatatype_call(newdatatypeobject *obj, PyObject *args, PyObject *other)
   {
       PyObject *result;
       char *arg1;
       char *arg2;
       char *arg3;

       if (!PyArg_ParseTuple(args, "sss:call", &arg1, &arg2, &arg3)) {
           return NULL;
       }
       result = PyString_FromFormat(
           "Returning -- value: [\%d] arg1: [\%s] arg2: [\%s] arg3: [\%s]\n",
           obj->obj_UnderlyingDatatypePtr->size,
           arg1, arg2, arg3);
       printf("\%s", PyString_AS_STRING(result));
       return result;
   }

.. % XXX いくつかのメンバを追加する必要。。。

::

   /* バージョン 2.2 以降で追加 */
   /* Iterators */
   getiterfunc tp_iter;
   iternextfunc tp_iternext;

これらの関数はイテレータ用プロトコルをサポートします。オブジェクトが、その (ループ中に順に生成されていくかもしれない) 内容を巡回 (訳注:
イテレータでひとつずつ要素をたどっていくこと) するイテレータをサポートしたい場合は、 ``tp_iter`` ハンドラを実装する必要があります。
``tp_iter`` ハンドラによって返されるオブジェクトは ``tp_iter`` と ``tp_iternext`` の両方を実装する必要があります。
どちらのハンドラも、それが呼ばれたインスタンスをひとつだけ引数としてとり、新しい参照を返します。エラーが起きた場合には例外を設定してから
*NULL* を返す必要があります。

巡回可能な要素を表現するオブジェクトに対しては、 ``tp_iter`` ハンドラがイテレータオブジェクトを返す必要があります。イテレータオブジェクトは
巡回中の状態を保持する責任をもっています。お互いに干渉しない複数のイテレータの存在を許すようなオブジェクト (リストやタプルがそうです) の場合は、
新しいイテレータを作成して返す必要があります。 (巡回の結果生じる副作用のために) 一回だけしか巡回できないオブジェクトの場合は、それ自身への参照を返すような
ハンドラと、 ``tp_iternext`` ハンドラも実装する必要があります。ファイルオブジェクトはそのようなイテレータの例です。

イテレータオブジェクトは両方のハンドラを実装する必要があります。 ``tp_iter`` ハンドラはそのイテレータへの新しい参照を返します
(これは破壊的にしか巡回できないオブジェクトに対する ``tp_iter`` ハンドラと同じです)。 ``tp_iternext``
ハンドラはその次のオブジェクトがある場合、それへの新しい参照を返します。巡回が終端に達したときは例外を出さずに *NULL* を返してもいいですし、
:exc:`StopIteration` を放出してもかまいません。例外を使わないほうがやや速度が上がるかもしれません。
実際のエラーが起こったときには、例外を放出して *NULL* を返す必要があります。


.. _weakref-support:

弱参照(Weak Reference)のサポート
--------------------------------

Pythonの弱参照実装のひとつのゴールは、どのような（数値のような弱参照による利益を得ない）タイプでもオーバーヘッドなしで
弱参照のメカニズムに組み込めるようにすることです。

弱参照可能なオブジェクトの拡張では、弱参照メカニズムのために :c:type:`PyObject\*` フィールドをインスタンス構造体に含む必要があります。
これはオブジェクトのコンストラクタで *NULL* に初期化する必要があります。これは対応するタイプの
:attr:`tp_weaklistoffset` フィールドをフィールドのオフセットに設定しなければいけません。
たとえば、インスタンスタイプは以下の構造体で定義されます::

   typedef struct {
       PyObject_HEAD
       PyClassObject *in_class;       /* The class object */
       PyObject      *in_dict;        /* A dictionary */
       PyObject      *in_weakreflist; /* List of weak references */
   } PyInstanceObject;

インスタンス用に静的に宣言されたタイプオブジェクトはこのように定義されます::

   PyTypeObject PyInstance_Type = {
       PyObject_HEAD_INIT(&PyType_Type)
       0,
       "module.instance",

       /* Lots of stuff omitted for brevity... */

       Py_TPFLAGS_DEFAULT,                         /* tp_flags */
       0,                                          /* tp_doc */
       0,                                          /* tp_traverse */
       0,                                          /* tp_clear */
       0,                                          /* tp_richcompare */
       offsetof(PyInstanceObject, in_weakreflist), /* tp_weaklistoffset */
   };

タイプのコンストラクタは弱参照を *NULL* に初期化する責任があります::

   static PyObject *
   instance_new() {
       /* Other initialization stuff omitted for brevity */

       self->in_weakreflist = NULL;

       return (PyObject *) self;
   }

さらに、デストラクタは弱参照を消すために弱参照のマネージャを呼ぶ必要があります。これはデストラクタのどの処理よりも先に実施される必要がありますが、
弱参照リストが *NULL* でない場合にだけ必要です::

   static void
   instance_dealloc(PyInstanceObject *inst)
   {
       /* Allocate temporaries if needed, but do not begin
          destruction just yet.
        */

       if (inst->in_weakreflist != NULL)
           PyObject_ClearWeakRefs((PyObject *) inst);

       /* Proceed with object destruction normally. */
   }


その他いろいろ
--------------

上にあげたほとんどの関数は、その値として ``0`` を与えれば省略できることを忘れないでください。それぞれの関数で提供しなければならない
型の定義があり、これらは Python の include 用ディレクトリの :file:`object.h` というファイルにおさめられています。これは
Python の配布ソースに含まれています。

新しいデータ型に何らかのメソッドを実装するやりかたを学ぶには、以下の方法がおすすめです: Python の配布されているソースをダウンロードして
展開する。 :file:`Objects` ディレクトリへ行き、C のソースファイルから「 ``tp_`` 欲しい名前」の文字列で検索する (たとえば
``tp_print`` とか ``tp_compare`` のように)。こうすれば実装したい例がみつかるでしょう。

あるオブジェクトが、いま実装している型のインスタンスであるかどうかを確かめたい場合には、 :c:func:`PyObject_TypeCheck`
関数を使ってください。使用例は以下のようなかんじです::

   if (! PyObject_TypeCheck(some_object, &MyType)) {
       PyErr_SetString(PyExc_TypeError, "arg #1 not a mything");
       return NULL;
   }

.. rubric:: 注記

.. [#] これはそのオブジェクトが文字列や実数などの基本タイプであるような時に成り立ちます。

.. [#] We relied ここで出てきたタイプではガベージコレクションをサポートしていないので、この例では :attr:`tp_dealloc`
   ハンドラに依存しています。このハンドラはそのタイプがたとえガベージコレクションをサポートしている場合でも、そのオブジェクトの
   「追跡を解除する」ために呼ばれることがありますが、これは高度な話題でありここでは扱いません。

.. [#] first および last メンバが文字列であるということはわかっているので、いまやそれらの参照カウントを
   減らすときにはそれほど注意する必要はないように思えるかもしれません。しかし文字列型のサブクラスは依然として受けつけられています。
   通常の文字列型ならば、解放時にあなたのオブジェクトがコールバックされることはありませんが、文字列型のサブクラスがそうしないという保証はありません。

.. [#] 3番目のバージョンでさえ、循環を回避できるという保証はされていません。たとえ通常の文字列型なら循環しない場合でも、文字列型の
   サブクラスをとることが許されていれば、そのタイプでは循環が発生しうるからです。

