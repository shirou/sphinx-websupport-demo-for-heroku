.. highlightlang:: c
.. _codeobjects:

コードオブジェクト
-------------------

.. sectionauthor:: Jeffrey Yasskin <jyasskin@gmail.com>


.. index::
   object: code

コードオブジェクト(Code objects)は CPython 実装の低レベルな詳細部分です。
各オブジェクトは関数に束縛されていない実行可能コードの塊を表現しています。

.. c:type:: PyCodeObject

   コードオブジェクトを表現するために利用されるC構造体。
   この型のフィールドは何時でも変更され得ます。


.. c:var:: PyTypeObject PyCode_Type

   Python の :class:`code` 型を表現する :c:type:`PyTypeObject` のインスタンス


.. c:function:: int PyCode_Check(PyObject *co)

   *co* が :class:`code` オブジェクトのときに真を返します。

.. c:function:: int PyCode_GetNumFree(PyObject *co)

   *co* 内の自由変数(free variables)の数を返します。

.. c:function:: PyCodeObject *PyCode_New(int argcount, int nlocals, int stacksize, int flags, PyObject *code, PyObject *consts, PyObject *names, PyObject *varnames, PyObject *freevars, PyObject *cellvars, PyObject *filename, PyObject *name, int firstlineno, PyObject *lnotab)

   新しいコードオブジェクトを返します。
   フレームを作成するためにダミーのコードオブジェクトが必要な場合は、代わりに
   :c:func:`PyCode_NewEmpty` を利用してください。
   バイトコードは頻繁に変更されるため、 :c:func:`PyCode_New` を直接呼び出すと、
   Python の詳細バージョンに依存してしまうことがあります。


.. c:function:: int PyCode_NewEmpty(const char *filename, const char *funcname, int firstlineno)

   新しい空のコードオブジェクトを、指定されたファイル名、関数名、開始行番号で作成します。
   返されたコードオブジェクトに対しての :keyword:`exec` や :func:`eval` は許されていません。
