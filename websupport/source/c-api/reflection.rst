.. highlightlang:: c

.. _reflection:

リフレクション
=================

.. c:function:: PyObject* PyEval_GetBuiltins()

   現在の実行フレーム内のビルトインの辞書か、もし実行中のフレームがなければ
   スレッド状態のインタプリタのビルトイン辞書を返します。


.. c:function:: PyObject* PyEval_GetLocals()

   現在の実行フレーム内のローカル変数の辞書か、実行中のフレームがなければ
   *NULL* を返します。


.. c:function:: PyObject* PyEval_GetGlobals()

   現在の実行フレームのグローバル変数の辞書か、実行中のフレームがなければ
   *NULL* を返します。


.. c:function:: PyFrameObject* PyEval_GetFrame()

   現在のスレッド状態のフレームを返します。
   現在実行中のフレームがなければ *NULL* を返します。


.. c:function:: int PyFrame_GetLineNumber(PyFrameObject *frame)

   *frame* が現在実行している行番号を返します。


.. c:function:: int PyEval_GetRestricted()

   現在のフレームがありそれが制限モードで実行していた場合、真を返します。
   それ以外の場合は僞を返します。


.. c:function:: const char* PyEval_GetFuncName(PyObject *func)

   *func* が 関数、クラス、インスタンスオブジェクトであればその名前を、
   そうでなければ *func* の型を返します。


.. c:function:: const char* PyEval_GetFuncDesc(PyObject *func)

   *func* の型に依存する、解説文字列(description string)を返します。
   戻り値は、関数とメソッドに対しては "()", " constructor", " instance",
   " object" です。
   :c:func:`PyEval_GetFuncName` と連結された結果、 *func* の解説になります。
   
