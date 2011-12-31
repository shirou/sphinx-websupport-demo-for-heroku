.. highlightlang:: c

.. _classobjects:

クラスとインスタンスオブジェクト
--------------------------------

.. index:: object: class

ここで説明されているクラスオブジェクトは旧スタイルクラスのもので、
Python 3 では削除されることに注意してください。
新スタイルクラス(type)を拡張モジュールで作成する場合は、 type オブジェクトを
扱うべきです。 (:ref:`typeobjects` を参照)

.. c:type:: PyClassObject

   ビルトインクラスを表すためのオブジェクトの構造体


.. c:var:: PyObject* PyClass_Type

   .. index:: single: ClassType (in module types)

   クラスオブジェクトのための type オブジェクト。
   Python レイヤーの、 ``types.ClassType`` と同じオブジェクト。


.. c:function:: int PyClass_Check(PyObject *o)

   *o* が、標準のクラスオブジェクトから派生した type のインスタンスだった場合を含めて、
   クラスオブジェクトだった場合に真を返します。
   それ以外の場合は偽を返します。


.. c:function:: int PyClass_IsSubclass(PyObject *klass, PyObject *base)

   *klass* が *base* のサブクラスだった場合に真を返します。
   それ以外の場合は偽を返します。

.. index:: object: instance

インスタンスオブジェクト固有の関数はきわめてわずかです。


.. c:var:: PyTypeObject PyInstance_Type

   クラスインスタンスの型オブジェクトです。


.. c:function:: int PyInstance_Check(PyObject *obj)

   *obj* がインスタンスの場合に真を返します。


.. c:function:: PyObject* PyInstance_New(PyObject *class, PyObject *arg, PyObject *kw)

   特定クラスの新たなインスタンスを生成します。パラメタ *arg*  および *kw* はそれぞれオブジェクトのコンストラクタに渡す
   実引数およびキーワードパラメタとして使われます。


.. c:function:: PyObject* PyInstance_NewRaw(PyObject *class, PyObject *dict)

   特定クラスの新たなインスタンスを、コンストラクタを呼ばずに生成します。 *class* は新たに作成するオブジェクトのクラスです。 *dict* パラメタは
   オブジェクトの :attr:`__dict__` に使われます; *dict* が *NULL* なら、インスタンス用に新たな辞書が作成されます。

