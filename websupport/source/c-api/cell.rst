.. highlightlang:: c

.. _cell-objects:

セルオブジェクト (cell object)
------------------------------

"セル (cell)" オブジェクトは、複数のスコープから参照される変数群を実装するために使われます。セルは各変数について作成され、各々の値を記憶します;
この値を参照する各スタックフレームにおけるローカル変数には、そのスタックフレームの外側で同じ値を参照している
セルに対する参照が入ります。セルで表現された値にアクセスすると、セルオブジェクト自体の代わりにセル内の値が使われます。このセルオブジェクトを使った間接参照
(dereference) は、インタプリタによって生成されたバイトコード内でサポートされている必要があります;
セルオブジェクトにアクセスした際に、自動的に間接参照は起こりません。上記以外の状況では、セルオブジェクトは役に立たないはずです。


.. c:type:: PyCellObject

   セルオブジェクトに使われる C 構造体です。


.. c:var:: PyTypeObject PyCell_Type

   セルオブジェクトに対応する型オブジェクトです。


.. c:function:: int PyCell_Check(ob)

   *ob* がセルオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。


.. c:function:: PyObject* PyCell_New(PyObject *ob)

   値 *ob* の入った新たなセルオブジェクトを生成して返します。引数を *NULL* にしてもかまいません。


.. c:function:: PyObject* PyCell_Get(PyObject *cell)

   *cell* の内容を返します。


.. c:function:: PyObject* PyCell_GET(PyObject *cell)

   *cell* の内容を返しますが、 *cell* が非 *NULL* でかつセルオブジェクトであるかどうかチェックしません。


.. c:function:: int PyCell_Set(PyObject *cell, PyObject *value)

   セルオブジェクト *cell* の内容を *value* に設定します。この関数は現在のセルの全ての内容に対する参照を解放します。 *value* は
   *NULL* でもかまいません。 *cell* は非 *NULL* でなければなりません; もし *cell* がセルオブジェクトでない場合、 ``-1``
   を返します。成功すると ``0`` を返します。


.. c:function:: void PyCell_SET(PyObject *cell, PyObject *value)

   セルオブジェクト *cell* の値を *value* に設定します。参照カウントに対する変更はなく、安全のためのチェックは何も行いません; *cell*
   は非 *NULL* でなければならず、かつセルオブジェクトでなければなりません。

