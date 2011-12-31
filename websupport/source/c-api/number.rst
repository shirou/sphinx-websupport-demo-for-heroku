.. highlightlang:: c

.. _number:

数値型プロトコル (number protocol)
==================================


.. c:function:: int PyNumber_Check(PyObject *o)

   オブジェクト *o* が数値型プロトコルを提供している場合に ``1`` を返し、そうでないときには偽を返します。この関数呼び出しは常に成功します。


.. c:function:: PyObject* PyNumber_Add(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* を加算した結果を返し、失敗すると *NULL* を返します。 Python の式 ``o1 + o2`` と同じです。


.. c:function:: PyObject* PyNumber_Subtract(PyObject *o1, PyObject *o2)

   成功すると *o1* から *o2* を減算した結果を返し、失敗すると *NULL* を返します。 Python の式 ``o1 - o2`` と同じです。


.. c:function:: PyObject* PyNumber_Multiply(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* を乗算した結果を返し、失敗すると *NULL* を返します。 Python の式 ``o1 * o2`` と同じです。


.. c:function:: PyObject* PyNumber_Divide(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した結果を返し, 失敗すると *NULL* を返します。  Python の式 ``o1 / o2`` と同じです。


.. c:function:: PyObject* PyNumber_FloorDivide(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した切捨て値を返し、失敗すると *NULL* を返します。  "旧仕様の" 整数間での除算と同じです。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyNumber_TrueDivide(PyObject *o1, PyObject *o2)

   成功すると、数学的な *o1* の *o2* による除算値に対する妥当な近似 (reasonable approximation) を返し、失敗すると
   *NULL* を返します。全ての実数を 2 を基数として表現するのは不可能なため、二進の浮動小数点数は "近似値"
   しか表現できません。このため、戻り値も近似になります。この関数に二つの整数を渡した際、浮動小数点の値を返すことがあります。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyNumber_Remainder(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した剰余を返し、失敗すると *NULL* を返します。 Python の式 ``o1 % o2`` と同じです。


.. c:function:: PyObject* PyNumber_Divmod(PyObject *o1, PyObject *o2)

   .. index:: builtin: divmod

   組み込み関数 :func:`divmod` を参照してください。失敗すると *NULL* を返します。 Python の式 ``divmod(o1,
   o2)`` と同じです。


.. c:function:: PyObject* PyNumber_Power(PyObject *o1, PyObject *o2, PyObject *o3)

   .. index:: builtin: pow

   組み込み関数 :func:`pow` を参照してください。失敗すると *NULL* を返します。
   Python の式 ``pow(o1, o2, o3)`` と同じです。
   *o3* はオプションです。 *o3* を無視させたいなら、 :c:data:`Py_None` を入れてください (*o3*
   に *NULL* を渡すと、不正なメモリアクセスを引き起こすことがあります)。


.. c:function:: PyObject* PyNumber_Negative(PyObject *o)

   成功すると *o* の符号反転を返し、失敗すると *NULL* を返します。 Python の式 ``-o`` と同じです。


.. c:function:: PyObject* PyNumber_Positive(PyObject *o)

   成功すると *o* を返し、失敗すると *NULL* を返します。 Python の式 ``+o`` と同じです。


.. c:function:: PyObject* PyNumber_Absolute(PyObject *o)

   .. index:: builtin: abs

   成功すると *o* の絶対値を返し、失敗すると *NULL* を返します。 Python の式 ``abs(o)`` と同じです。


.. c:function:: PyObject* PyNumber_Invert(PyObject *o)

   成功すると *o* のビット単位反転 (bitwise negation) を返し、失敗すると *NULL* を返します。Python の式 ``~o``
   と同じです。


.. c:function:: PyObject* PyNumber_Lshift(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* だけ左シフトした結果を返し、失敗すると *NULL* を返します。 Python の式 ``o1 << o2``
   と同じです。


.. c:function:: PyObject* PyNumber_Rshift(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* だけ右シフトした結果を返し、失敗すると *NULL* を返します。 Python の式 ``o1 >> o2``
   と同じです。


.. c:function:: PyObject* PyNumber_And(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位論理積 (bitwise and)" を返し、失敗すると *NULL* を返します。 Python の式
   ``o1 & o2`` と同じです。


.. c:function:: PyObject* PyNumber_Xor(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の  "ビット単位排他的論理和 (bitwise exclusive or)" を返し、失敗すると *NULL*
   を返します。 Python の式 ``o1 ^ o2`` と同じです。


.. c:function:: PyObject* PyNumber_Or(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位論理和 (bitwise or)" を返し失敗すると *NULL* を返します。 Python の式
   ``o1 | o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlaceAdd(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* を加算した結果を返し、失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 += o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlaceSubtract(PyObject *o1, PyObject *o2)

   成功すると *o1* から *o2* を減算した結果を返し、失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 -= o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlaceMultiply(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* を乗算した結果を返し、失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 *= o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlaceDivide(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した結果を返し, 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 /= o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlaceFloorDivide(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した切捨て値を返し、失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 //= o2`` と同じです。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyNumber_InPlaceTrueDivide(PyObject *o1, PyObject *o2)

   成功すると、数学的な *o1* の *o2* による除算値に対する妥当な近似 (reasonable approximation) を返し、失敗すると
   *NULL* を返します。全ての実数を 2 を基数として表現するのは不可能なため、二進の浮動小数点数は "近似値"
   しか表現できません。このため、戻り値も近似になります。この関数に二つの整数を渡した際、浮動小数点の値を返すことがあります。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyNumber_InPlaceRemainder(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* で除算した剰余を返し、 , 失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 %= o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlacePower(PyObject *o1, PyObject *o2, PyObject *o3)

   .. index:: builtin: pow

   組み込み関数 :func:`pow` を参照してください。失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。この関数は *o3* が :c:data:`Py_None` の場合は Python 文 
   ``o1 **= o2`` と同じで、それ以外の場合は ``pow(o1, o2, o3)`` の in-place 版です。 *o3* を無視させたいなら、
   :c:data:`Py_None` を入れてください (*o3* に *NULL* を渡すと、不正なメモリアクセスを引き起こすことがあります)。


.. c:function:: PyObject* PyNumber_InPlaceLshift(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* だけ左シフトした結果を返し、失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 <<= o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlaceRshift(PyObject *o1, PyObject *o2)

   成功すると *o1* を *o2* だけ右シフトした結果を返し、失敗すると *NULL* を返します。 *o1* が *in-place*
   演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 >>= o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlaceAnd(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位論理積 (bitwise and)" を返し、失敗すると *NULL* を返します。  *o1* が
   *in-place* 演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 &= o2`` と同じです。


.. c:function:: PyObject* PyNumber_InPlaceXor(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位排他的論理和  (bitwise exclusive or)" を返し、失敗すると *NULL*
   を返します。  *o1* が *in-place* 演算をサポートする場合、in-place 演算を行います。 Python の文 ``o1 ^= o2``
   と同じです。


.. c:function:: PyObject* PyNumber_InPlaceOr(PyObject *o1, PyObject *o2)

   成功すると *o1* と *o2* の "ビット単位論理和 (bitwise or)" を返し失敗すると *NULL* を返します。
   *o1* が *in-place* 演算をサポートする場合、in-place 演算を行います。
   Python の文 ``o1 |= o2`` と同じです。


.. c:function:: int PyNumber_Coerce(PyObject **p1, PyObject **p2)

   .. index:: builtin: coerce

   この関数は :c:type:`PyObject\*` 型の二つの変数のアドレスを引数にとります。 ``*p1`` と ``*p2``
   が指すオブジェクトが同じ型の場合、それぞれの参照カウントをインクリメントして ``0`` (成功) を返します。
   オブジェクトを変換して共通の数値型にできる場合、 ``*p1`` と ``*p2`` を変換後の値に置き換えて (参照カウントを '新しく' して)
   、 ``0`` を返します。変換が不可能な場合や、その他何らかのエラーが生じた場合、 ``-1`` (失敗) を返し、参照カウントをインクリメントしません。
   ``PyNumber_Coerce(&o1, &o2)`` の呼び出しは Python 文 ``o1, o2 = coerce(o1, o2)`` と同じです。


.. c:function:: int PyNumber_CoerceEx(PyObject **p1, PyObject **p2)

   This function is similar to :c:func:`PyNumber_Coerce`, except that it returns
   ``1`` when the conversion is not possible and when no error is raised.
   Reference counts are still not increased in this case.
   この関数は :c:func:`PyNumber_Coerce` と似ていますが、
   変換が失敗た場合にはエラーを発生させず、 ``-1`` を返します。
   この場合、参照カウントはインクリメントされません。


.. c:function:: PyObject* PyNumber_Int(PyObject *o)

   .. index:: builtin: int

   成功すると *o* を整数に変換したものを返し、失敗すると *NULL* を返します。
   引数の値が整数の範囲外の場合、長整数を代わりに返します。 Python
   の式 ``int(o)`` と同じです。


.. c:function:: PyObject* PyNumber_Long(PyObject *o)

   .. index:: builtin: long

   成功すると *o* を長整数に変換したものを返し、失敗すると *NULL* を返します。
   Python の式 ``long(o)`` と同じです。


.. c:function:: PyObject* PyNumber_Float(PyObject *o)

   .. index:: builtin: float

   成功すると *o* を浮動小数点数に変換したものを返し、失敗すると *NULL* を返します。
   Python の式 ``float(o)`` と同じです。


.. c:function:: PyObject* PyNumber_Index(PyObject *o)

   *o* をPythonのintもしくはlong型に変換し、成功したらその値を返します。
   失敗したら *NULL* が返され、 :exc:`TypeError` 例外が送出されます。

   .. versionadded:: 2.5


.. c:function:: PyObject* PyNumber_ToBase(PyObject *n, int base)

   整数 *n* を、 *base* 進数の文字列に変換し、適切であれば ``'0b'``, ``'0o'``,
   ``'0x'`` の基数マーカーをつけます。
   *base* が 2, 8, 10, 16 のいずれでも無い場合、フォーマットは x を基数として
   ``'x#num'`` となります。
   もし *n* が整数オブジェクトでない場合、まず :c:func:`PyNumber_Index` を使って
   変換されます。

   .. versionadded:: 2.6


.. c:function:: Py_ssize_t PyNumber_AsSsize_t(PyObject *o, PyObject *exc)

   *o* を整数として解釈可能だった場合、Py_ssize_t型の値に変換して返します。
   もし *o* がPythonのintもしくはlongに変換できたのに、Py_ssize_tへの変換が
   :exc:`OverflowError` になる場合は、 *exc* 引数で渡された型
   (普通は :exc:`IndexError` か :exc:`OverflowError`) の例外を送出します。
   もし、 *exc* が *NULL* なら、例外はクリアされて、値が負の場合は *PY_SSIZE_T_MIN* へ、
   正の場合は *PY_SSIZE_T_MAX* へと制限されます。

   .. versionadded:: 2.5


.. c:function:: int PyIndex_Check(PyObject *o)

   *o* がインデックス整数であるときにTrueを返します。 (tp_as_number構造体のnb_indexスロットが埋まっている場合)

   .. versionadded:: 2.5
