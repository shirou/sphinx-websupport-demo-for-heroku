.. highlightlang:: c

.. _supporting-cycle-detection:

循環参照ガベージコレクションをサポートする
==========================================

Python が循環参照を含むガベージの検出とコレクションをサポートするには、他のオブジェクトに対する "コンテナ" (他のオブジェクトには
他のコンテナも含みます) となるオブジェクト型によるサポートが必要です。他のオブジェクトに対する参照を記憶しないオブジェクトや、 (数値や文字列のような)
アトム型 (atomic type) への参照だけを記憶するような型では、ガベージコレクションに際して特別これといったサポートを提供する必要はありません。

.. ここで説明しているインタフェースの使い方を示した例は、 Python の拡張と埋め込み (XXX reference: ../ext/ext.html) の
   "循環参照の収集をサポートする (XXX reference: ../ext/example-cycle-support.html)" にあります。

コンテナ型を作るには、型オブジェクトの :attr:`tp_flags` フィールドに :const:`Py_TPFLAGS_HAVE_GC`
フラグがなくてはならず、 :attr:`tp_traverse` ハンドラの実装を提供しなければなりません。
実装する型のインスタンスを変更可能なオブジェクトにするなら、 :attr:`tp_clear` の実装も提供しなければなりません。


.. data:: Py_TPFLAGS_HAVE_GC
   :noindex:

   このフラグをセットした型のオブジェクトは、この節に述べた規則に適合しなければなりません。簡単のため、このフラグをセットした型の
   オブジェクトをコンテナオブジェクトと呼びます。

コンテナ型のコンストラクタは以下の二つの規則に適合しなければなりません:

#. オブジェクトのメモリは :c:func:`PyObject_GC_New` または :c:func:`PyObject_GC_NewVar`
   で確保しなければなりません。

#. 一度他のコンテナへの参照が入るかもしれないフィールドが全て初期化されたら、 :c:func:`PyObject_GC_Track` を呼び出さねば
   なりません。


.. c:function:: TYPE* PyObject_GC_New(TYPE, PyTypeObject *type)

   :c:func:`PyObject_New` に似ていますが、 :const:`Py_TPFLAGS_HAVE_GC`
   のセットされたコンテナオブジェクト用です。


.. c:function:: TYPE* PyObject_GC_NewVar(TYPE, PyTypeObject *type, Py_ssize_t size)

   :c:func:`PyObject_NewVar` に似ていますが、 :const:`Py_TPFLAGS_HAVE_GC`
   のセットされたコンテナオブジェクト用です。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: TYPE* PyObject_GC_Resize(TYPE, PyVarObject *op, Py_ssize_t newsize)

   :c:func:`PyObject_NewVar` が確保したオブジェクトのメモリをリサイズします。
   リサイズされたオブジェクトを返します。失敗すると *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *newsize* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: void PyObject_GC_Track(PyObject *op)

   ガベージコレクタが追跡しているコンテナオブジェクトの集合にオブジェクト *op* を追加します。ガベージコレクタの動作する
   回数は予測不能なので、追加対象にするオブジェクトは追跡されている間ずっと有効なオブジェクトでなければなりません。
   この関数は、通常コンストラクタの最後付近で、 :attr:`tp_traverse` ハンドラ以降の全てのフィールドが有効な値になった時点で呼び出さねば
   なりません。


.. c:function:: void _PyObject_GC_TRACK(PyObject *op)

   :c:func:`PyObject_GC_Track` のマクロ版です。拡張モジュールに使ってはなりません。

同様に、オブジェクトのメモリ解放関数も以下の二つの規則に適合しなければなりません:

#. 他のコンテナを参照しているフィールドを無効化する前に、 :c:func:`PyObject_GC_UnTrack` を呼び出さねばなりません。

#. オブジェクトのメモリは :c:func:`PyObject_GC_Del` で解放しなければなりません。


.. c:function:: void PyObject_GC_Del(void *op)

   :c:func:`PyObject_GC_New` や :c:func:`PyObject_GC_NewVar` を使って確保されたメモリを解放します。


.. c:function:: void PyObject_GC_UnTrack(void *op)

   ガベージコレクタが追跡しているコンテナオブジェクトの集合からオブジェクト *op* を除去します。再度 :c:func:`PyObject_GC_Track`
   を呼び出して、除去したオブジェクトを追跡対象セットに追加できることに注意してください。メモリ解放関数 (deallocator,
   :attr:`tp_dealloc` ハンドラ) は、 :attr:`tp_traverse` ハンドラが使用しているフィールドのいずれかが無効化されるよりも
   以前にオブジェクトに対して呼び出されていなければなりません。


.. c:function:: void _PyObject_GC_UNTRACK(PyObject *op)

   :c:func:`PyObject_GC_UnTrack` のマクロ版です。拡張モジュールに使ってはなりません。

:attr:`tp_traverse` ハンドラは以下の型を持つ関数を引数の一つとしてとります:


.. c:type:: int (*visitproc)(PyObject *object, void *arg)

   :attr:`tp_traverse` ハンドラに渡すビジタ関数 (visitor function)  の型です。この関数は追跡すべきオブジェクトを
   *object* に、 :attr:`tp_traverse` ハンドラの第三引数を *arg* にして呼び出されます。Python
   のコア部分では、ガベージコレクションの実装に複数のビジタ関数を使っています。ユーザが独自にビジタ関数を書く必要があるとは想定されていません。

:attr:`tp_traverse` ハンドラは以下の型でなければなりません:


.. c:type:: int (*traverseproc)(PyObject *self, visitproc visit, void *arg)

   コンテナオブジェクトのためのトラバーサル関数 (traversal function) です。実装では、 *self*
   に直接入っている各オブジェクトに対して *visit*  関数を呼び出さねばなりません。このとき、 *visit* へのパラメタは
   コンテナに入っている各オブジェクトと、このハンドラに渡された *arg* の値です。 *visit* 関数は *NULL* オブジェクトを引数に
   渡して呼び出してはなりません。 *visit* が非ゼロの値を返す場合、エラーが発生し、戻り値をそのまま返すようににしなければなりません。

:attr:`tp_traverse` ハンドラの作成を単純化するため、 :c:func:`Py_VISIT`
マクロが提供されています。このマクロを使うには、 :attr:`tp_traverse` の実装で、引数を *visit* および *arg*
という名前にしておかねばなりません:


.. c:function:: void Py_VISIT(PyObject *o)

   引数 *o* および *arg* を使って *visit* コールバックを呼び出します。 *visit* が非ゼロの値を返した場合、その値をそのまま返します。
   このマクロを使えば、 :attr:`tp_traverse` ハンドラは以下のようになります::

      static int
      my_traverse(Noddy *self, visitproc visit, void *arg)
      {
          Py_VISIT(self->foo);
          Py_VISIT(self->bar);
          return 0;
      }

   .. versionadded:: 2.4

:attr:`tp_clear` ハンドラは :c:type:`inquiry` 型にするか、オブジェクトが変更不能の場合には *NULL*
にしなければなりません。


.. c:type:: int (*inquiry)(PyObject *self)

   循環参照を形成しているとおぼしき参照群を放棄します。変更不可能なオブジェクトは循環参照を直接形成することが決してない
   ので、この関数を定義する必要はありません。このメソッドを呼び出した後でもオブジェクトは有効なままでなければならないので注意してください (参照に対して
   :c:func:`Py_DECREF` を呼ぶだけにしないでください)。ガベージコレクタは、オブジェクトが
   循環参照を形成していることを検出した際にこのメソッドを呼び出します。

