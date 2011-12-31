.. highlightlang:: c

.. _complexobjects:

浮動小数点オブジェクト (complex number object)
----------------------------------------------

.. index:: object: complex number

Python の複素数オブジェクトは、 C API 側から見ると二つの別個の型として実装されています: 一方は Python プログラムに対して公開
されている Python のオブジェクトで、他方は実際の複素数値を表現する C の構造体です。 API では、これら双方を扱う関数を提供しています。


C 構造体としての複素数
^^^^^^^^^^^^^^^^^^^^^^

複素数の C 構造体を引数として受理したり、戻り値として返したりする関数は、ポインタ渡しを行うのではなく *値渡し* を行うので注意してください。これは
API 全体を通して一貫しています。


.. c:type:: Py_complex

   Python 複素数オブジェクトの値の部分に対応する C の構造体です。複素数オブジェクトを扱うほとんどの関数は、この型の構造体を
   場合に応じて入力や出力として使います。構造体は以下のように定義されています::

      typedef struct {
         double real;
         double imag;
      } Py_complex;


.. c:function:: Py_complex _Py_c_sum(Py_complex left, Py_complex right)

   二つの複素数の和を C の :c:type:`Py_complex` 型で返します。


.. c:function:: Py_complex _Py_c_diff(Py_complex left, Py_complex right)

   二つの複素数の差を C の :c:type:`Py_complex` 型で返します。


.. c:function:: Py_complex _Py_c_neg(Py_complex complex)

   複素数 *complex* の符号反転 C の :c:type:`Py_complex` 型で返します。


.. c:function:: Py_complex _Py_c_prod(Py_complex left, Py_complex right)

   二つの複素数の積を C の :c:type:`Py_complex` 型で返します。


.. c:function:: Py_complex _Py_c_quot(Py_complex dividend, Py_complex divisor)

   二つの複素数の商を C の :c:type:`Py_complex` 型で返します。


.. c:function:: Py_complex _Py_c_pow(Py_complex num, Py_complex exp)

   指数 *exp* の *num* 乗を C の :c:type:`Py_complex` 型で返します。


Python オブジェクトとしての複素数型
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. c:type:: PyComplexObject

   この :c:type:`PyObject` のサブタイプは Python の複素数オブジェクトを表現します。


.. c:var:: PyTypeObject PyComplex_Type

   この :c:type:`PyTypeObject` のインスタンスは Python の複素数型を表現します。
   Pythonの ``complex`` や ``types.ComplexType`` と同じオブジェクトです。


.. c:function:: int PyComplex_Check(PyObject *p)

   引数が :c:type:`PyComplexObject` 型か :c:type:`PyComplexObject` 型のサブタイプのときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyComplex_CheckExact(PyObject *p)

   引数が :c:type:`PyComplexObject` 型で、かつ :c:type:`PyComplexObject` 型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyComplex_FromCComplex(Py_complex v)

   C の :c:type:`Py_complex` 型から Python の複素数値を生成します。


.. c:function:: PyObject* PyComplex_FromDoubles(double real, double imag)

   新たな :c:type:`PyComplexObject` オブジェクトを *real* と *imag* から生成します。


.. c:function:: double PyComplex_RealAsDouble(PyObject *op)

   *op* の実数部分を C の :c:type:`double` 型で返します。


.. c:function:: double PyComplex_ImagAsDouble(PyObject *op)

   *op* の虚数部分を C の :c:type:`double` 型で返します。


.. c:function:: Py_complex PyComplex_AsCComplex(PyObject *op)

   複素数値 *op* から :c:type:`Py_complex` 型を生成します。

