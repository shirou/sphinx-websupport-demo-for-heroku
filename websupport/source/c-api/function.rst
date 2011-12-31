.. highlightlang:: c

.. _function-objects:

関数オブジェクト (Function Objects)
-----------------------------------

.. index:: object: function

Pythonの関数にはいくつかの種類があります。


.. c:type:: PyFunctionObject

   関数に使われるCの構造体


.. c:var:: PyTypeObject PyFunction_Type

   .. index:: single: MethodType (in module types)

   :c:type:`PyTypeObject` 型のインスタンスで、 Python の関数型を表します。これは Python プログラムに
   ``types.FunctionType`` として公開されます。


.. c:function:: int PyFunction_Check(PyObject *o)

   *o* が関数オブジェクト (:c:data:`PyFunction_Type` を持っている) なら true を返します。引数は *NULL*
   であってはいけません。


.. c:function:: PyObject* PyFunction_New(PyObject *code, PyObject *globals)

   コードオブジェクト *code* に関連付けられた新しい関数オブジェクトを返します。 *globals*
   はこの関数からアクセスできるグローバル変数の辞書でなければなりません。

   関数のドキュメント文字列、名前および *__module__* はコードオブジェクトから取得されます。引数のデフォルト値やクロージャは *NULL*
   にセットされます。


.. c:function:: PyObject* PyFunction_GetCode(PyObject *op)

   関数オブジェクト *op* に関連付けられたコードオブジェクトを返します。


.. c:function:: PyObject* PyFunction_GetGlobals(PyObject *op)

   関数オブジェクト *op* に関連付けられたglobals辞書を返します。


.. c:function:: PyObject* PyFunction_GetModule(PyObject *op)

   関数オブジェクト *op* の *__module__* 属性を返します。　これは普通はモジュール名の文字列が入っていますが、Python コードから
   他のオブジェクトをセットされることもあります。


.. c:function:: PyObject* PyFunction_GetDefaults(PyObject *op)

   関数オブジェクト *op* の引数のデフォルト値を返します。引数のタプルか *NULL* になります。


.. c:function:: int PyFunction_SetDefaults(PyObject *op, PyObject *defaults)

   関数オブジェクト *op* の引数のデフォルト値を設定します。 *defaults* は *Py_None* かタプルでなければいけません。

   失敗した時は、 :exc:`SystemError` を発生し、 ``-1`` を返します。


.. c:function:: PyObject* PyFunction_GetClosure(PyObject *op)

   関数オブジェクト *op* に設定されたクロージャを返します。 *NULL* か cell オブジェクトのタプルです。


.. c:function:: int PyFunction_SetClosure(PyObject *op, PyObject *closure)

   関数オブジェクト *op* にクロージャを設定します。 *closure* は、 *Py_None* もしくは cell
   オブジェクトのタプルでなければなりません。

   失敗した時は、 :exc:`SystemError` を送出し、 ``-1`` を返します。

