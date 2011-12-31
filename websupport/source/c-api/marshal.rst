.. highlightlang:: c

.. _marshalling-utils:

データ整列化 (data marshalling) のサポート
==========================================

以下のルーチン群は、 :mod:`marshal` モジュールと同じ形式を使った整列化オブジェクトを C コードから使えるようにします。
整列化形式でデータを書き出す関数に加えて、データを読み戻す関数もあります。整列化されたデータを記録するファイルはバイナリモードで
開かれていなければなりません。

数値は最小桁が先にくるように記録されます。

このモジュールでは、3つのバージョンのデータ形式をサポートしています。
バージョン 0 は従来のもので、(Python 2.4 で新たに追加された) バージョン
1  は intern 化された文字列をファイル内で共有し、逆マーシャル化の時にも共有されるようにします。
(Python 2.5 で新たに追加された) バージョン2は、浮動小数点数に対してバイナリフォーマットを利用します。
*PY_MARSHAL_VERSION* は現在のバージョン (バージョン 2) を示します。


.. c:function:: void PyMarshal_WriteLongToFile(long value, FILE *file, int version)

   :c:type:`long` 型の整数値 *value* を *file* へ整列化します。この関数は *value* の下桁 32 ビットを書き込むだけです;
   ネイティブの :c:type:`long` 型サイズには関知しません。

   .. versionchanged:: 2.4
      ファイル形式を示す *version* が追加されました.


.. c:function:: void PyMarshal_WriteObjectToFile(PyObject *value, FILE *file, int version)

   Python オブジェクト *value* を *file* へ整列化します。

   .. versionchanged:: 2.4
      ファイル形式を示す *version* が追加されました.


.. c:function:: PyObject* PyMarshal_WriteObjectToString(PyObject *value, int version)

   *value* の整列化表現が入った文字列オブジェクトを返します。

   .. versionchanged:: 2.4
      ファイル形式を示す *version* が追加されました.

以下の関数を使うと、整列化された値を読み戻せます。

.. XXX What about error detection?  It appears that reading past the end
.. of the file will always result in a negative numeric value (where
.. that's relevant), but it's not clear that negative values won't be
.. handled properly when there's no error.  What's the right way to tell?
.. Should only non-negative values be written using these routines?

.. c:function:: long PyMarshal_ReadLongFromFile(FILE *file)

   読み出し用に開かれた :c:type:`FILE\*` 内のデータストリームから、 C の :c:type:`long` 型データを読み出して返します。
   この関数は、ネイティブの :c:type:`long` のサイズに関係なく、 32 ビットの値だけを読み出せます。


.. c:function:: int PyMarshal_ReadShortFromFile(FILE *file)

   読み出し用に開かれた :c:type:`FILE\*` 内のデータストリームから、 C の :c:type:`short` 型データを読み出して返します。
   この関数は、ネイティブの :c:type:`short` のサイズに関係なく、 16 ビットの値だけを読み出せます。


.. c:function:: PyObject* PyMarshal_ReadObjectFromFile(FILE *file)

   読み出し用に開かれた :c:type:`FILE\*` 内のデータストリームから、 Python オブジェクトを読み出して返します。
   エラーが生じた場合、適切な例外 (:exc:`EOFError` または :exc:`TypeError`) を送出して *NULL* を返します。


.. c:function:: PyObject* PyMarshal_ReadLastObjectFromFile(FILE *file)

   読み出し用に開かれた :c:type:`FILE\*` 内のデータストリームから、 Python オブジェクトを読み出して返します。
   :c:func:`PyMarshal_ReadObjectFromFile` と違い、この関数はファイル中に後続のオブジェクトが存在しないと仮定し、ファイルから
   メモリ上にファイルデータを一気にメモリにロードして、逆整列化機構がファイルから一バイトづつ読み出す代わりにメモリ上のデータを操作
   できるようにします。対象のファイルから他に何も読み出さないと分かっている場合にのみ、この関数を使ってください。エラーが生じた場合、適切な例外
   (:exc:`EOFError` または :exc:`TypeError`) を送出して *NULL* を返します。


.. c:function:: PyObject* PyMarshal_ReadObjectFromString(char *string, Py_ssize_t len)

   *string* が指している *len* バイトの文字列バッファに納められたデータストリームから Python オブジェクトを読み出して返します。
   エラーが生じた場合、適切な例外 (:exc:`EOFError` または :exc:`TypeError`) を送出して *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *len* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。
