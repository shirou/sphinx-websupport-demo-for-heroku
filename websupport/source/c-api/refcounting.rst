.. highlightlang:: c


.. _countingrefs:

************
参照カウント
************

この節のマクロはPythonオブジェクトの参照カウントを管理するために使われます。


.. c:function:: void Py_INCREF(PyObject *o)

   オブジェクト *o* に対する参照カウントを一つ増やします。オブジェクトが *NULL* であってはいけません。それが *NULL* ではないと確信が持てないならば、
   :c:func:`Py_XINCREF` を使ってください。


.. c:function:: void Py_XINCREF(PyObject *o)

   オブジェクト *o* に対する参照カウントを一つ増やします。オブジェクトが *NULL* であってもよく、その場合マクロは何の影響も与えません。


.. c:function:: void Py_DECREF(PyObject *o)

   オブジェクト *o* に対する参照カウントを一つ減らします。オブジェクトが *NULL* であってはいけません。それが *NULL* ではないと確信が持てないならば、
   :c:func:`Py_XDECREF` を使ってください。参照カウントがゼロになったら、
   オブジェクトの型のメモリ解放関数(*NULL* であってはならない)が呼ばれます。

   .. warning::

      (例えば :meth:`__del__` メソッドをもつクラスインスタンスがメモリ解放されたときに)メモリ解放関数は任意のPythonコードを呼び出すことが
      できます。このようなコードでは例外は伝播しませんが、実行されたコードはすべてのPythonグローバル変数に自由にアクセスできます。
      これが意味するのは、 :c:func:`Py_DECREF` が呼び出されるより前では、グローバル変数から到達可能などんなオブジェクトも一貫した状態に
      あるべきであるということです。例えば、リストからオブジェクトを削除するコードは削除するオブジェクト
      への参照を一時変数にコピーし、リストデータ構造を更新し、それから一時変数に対して :c:func:`Py_DECREF` を呼び出すべきです。


.. c:function:: void Py_XDECREF(PyObject *o)

   オブジェクト *o* への参照カウントを一つ減らします。オブジェクトは *NULL* でもかまいませんが、その場合マクロは何の影響も与えません。それ以外の
   場合、結果は :c:func:`Py_DECREF` と同じです。また、注意すべきことも同じです。


.. c:function:: void Py_CLEAR(PyObject *o)

   *o* の参照カウントを減らします．オブジェクトは *NULL* でもよく，その場合このマクロは何も行いません．オブジェクトが *NULL* でなければ，引数を
   *NULL* にした :c:func:`Py_DECREF` と同じ効果をもたらします．このマクロは一時変数を使って，参照カウントをデクリメントする前に引数を
   *NULL* にセットしてくれるので， :c:func:`Py_DECREF` に使うときの警告を気にしなくてすみます．

   ガベージコレクション中に追跡される可能性のある変数の参照デクリメントを行うには，このマクロを使うのがよいでしょう．

   .. versionadded:: 2.4

以下の関数: ``Py_IncRef(PyObject *o)``, ``Py_DecRef(PyObject *o)``,
は，実行時の動的な Python 埋め込みで使われる関数です．これらの関数はそれぞれ :c:func:`Py_XINCREF` および
:c:func:`Py_XDECREF` をエクスポートしただけです．

以下の関数やマクロ:  :c:func:`_Py_Dealloc`, :c:func:`_Py_ForgetReference`,
:c:func:`_Py_NewReference` は，インタプリタのコアの内部においてのみ使用するためのものです。
また、グローバル変数 :c:data:`_Py_RefTotal` も同様です。

