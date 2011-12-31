.. highlightlang:: c

.. _datetimeobjects:

DateTime オブジェクト
---------------------

:mod:`datetime` モジュールでは、様々な日付オブジェクトや時刻オブジェクトを
提供しています。以下に示す関数を使う場合には、あらかじめヘッダファイル
:file:`datetime.h` をソースに include し (:file:`Python.h` はこのファイルを
include しません)、 :c:macro:`PyDateTime_IMPORT` マクロを、通常はモジュール
初期化関数から、起動しておく必要があります。このマクロは以下のマクロで
使われる静的変数 :c:data:`PyDateTimeAPI` に C 構造体へのポインタを入れます。

.. % DateTime Objects

以下は型チェックマクロです:


.. c:function:: int PyDate_Check(PyObject *ob)

   *ob* が :c:data:`PyDateTime_DateType` 型か :c:data:`PyDateTime_DateType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyDate_CheckExact(PyObject *ob)

   *ob* が :c:data:`PyDateTime_DateType` 型のオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_Check(PyObject *ob)

   *ob* が :c:data:`PyDateTime_DateTimeType` 型か :c:data:`PyDateTime_DateTimeType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_CheckExact(PyObject *ob)

   *ob* が :c:data:`PyDateTime_DateTimeType` 型のオブジェクトの場合に真を返します; *ob* は *NULL*
   であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyTime_Check(PyObject *ob)

   *ob* が :c:data:`PyDateTime_TimeType` 型か :c:data:`PyDateTime_TimeType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyTime_CheckExact(PyObject *ob)

   *ob* が :c:data:`PyDateTime_TimeType` 型のオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyDelta_Check(PyObject *ob)

   *ob* が :c:data:`PyDateTime_DeltaType` 型か :c:data:`PyDateTime_DeltaType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyDelta_CheckExact(PyObject *ob)

   *ob* が :c:data:`PyDateTime_DeltaType` 型のオブジェクトの場合に真を返します; *ob* は *NULL*
   であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyTZInfo_Check(PyObject *ob)

   *ob* が :c:data:`PyDateTime_TZInfoType` 型か :c:data:`PyDateTime_TZInfoType`
   型のサブタイプのオブジェクトの場合に真を返します; *ob* は *NULL* であってはなりません。

   .. versionadded:: 2.4


.. c:function:: int PyTZInfo_CheckExact(PyObject *ob)

   *ob* が :c:data:`PyDateTime_TZInfoType` 型のオブジェクトの場合に真を返します; *ob* は *NULL*
   であってはなりません。

   .. versionadded:: 2.4

以下はオブジェクトを作成するためのマクロです:


.. c:function:: PyObject* PyDate_FromDate(int year, int month, int day)

   指定された年、月、日の ``datetime.date`` オブジェクトを返します。

   .. versionadded:: 2.4


.. c:function:: PyObject* PyDateTime_FromDateAndTime(int year, int month, int day, int hour, int minute, int second, int usecond)

   指定された年、月、日、時、分、秒、マイクロ秒の ``datetime.datetime``  オブジェクトを返します。

   .. versionadded:: 2.4


.. c:function:: PyObject* PyTime_FromTime(int hour, int minute, int second, int usecond)

   指定された時、分、秒、マイクロ秒の ``datetime.time``  オブジェクトを返します。

   .. versionadded:: 2.4


.. c:function:: PyObject* PyDelta_FromDSU(int days, int seconds, int useconds)

   指定された日、秒、マイクロ秒の ``datetime.timedelta`` オブジェクトを返します。マイクロ秒と秒が
   ``datetime.timedelta`` オブジェクトで定義されている範囲に入るように正規化を行います。

   .. versionadded:: 2.4

以下のマクロは date オブジェクトからフィールド値を取り出すためのものです。引数は :c:data:`PyDateTime_Date` またはそのサブクラス
(例えば :c:data:`PyDateTime_DateTime`)の  インスタンスでなければなりません。引数を *NULL* にしてはならず、
型チェックは行いません:


.. c:function:: int PyDateTime_GET_YEAR(PyDateTime_Date *o)

   年を正の整数で返します。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_GET_MONTH(PyDateTime_Date *o)

   月を 1 から 12 の間の整数で返します。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_GET_DAY(PyDateTime_Date *o)

   日を 1 から 31 の間の整数で返します。

   .. versionadded:: 2.4

以下のマクロは datetime オブジェクトからフィールド値を取り出すためのものです。引数は :c:data:`PyDateTime_DateTime`
またはそのサブクラスのインスタンスでなければなりません。引数を *NULL* にしてはならず、型チェックは行いません:


.. c:function:: int PyDateTime_DATE_GET_HOUR(PyDateTime_DateTime *o)

   時を 0 から 23 の間の整数で返します。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_DATE_GET_MINUTE(PyDateTime_DateTime *o)

   分を 0 から 59 の間の整数で返します。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_DATE_GET_SECOND(PyDateTime_DateTime *o)

   秒を 0 から 59 の間の整数で返します。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_DATE_GET_MICROSECOND(PyDateTime_DateTime *o)

   マイクロ秒を 0 から 999999 の間の整数で返します。

   .. versionadded:: 2.4

以下のマクロは time オブジェクトからフィールド値を取り出すためのものです。引数は :c:data:`PyDateTime_Time` またはそのサブクラスの
インスタンスでなければなりません。引数を *NULL* にしてはならず、型チェックは行いません:


.. c:function:: int PyDateTime_TIME_GET_HOUR(PyDateTime_Time *o)

   時を 0 から 23 の間の整数で返します。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_TIME_GET_MINUTE(PyDateTime_Time *o)

   分を 0 から 59 の間の整数で返します。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_TIME_GET_SECOND(PyDateTime_Time *o)

   秒を 0 から 59 の間の整数で返します。

   .. versionadded:: 2.4


.. c:function:: int PyDateTime_TIME_GET_MICROSECOND(PyDateTime_Time *o)

   マイクロ秒を 0 から 999999 の間の整数で返します。

   .. versionadded:: 2.4

以下のマクロは DB API を実装する上での便宜用です:


.. c:function:: PyObject* PyDateTime_FromTimestamp(PyObject *args)

   ``dateitme.datetime.fromtimestamp()`` に渡すのに適した引数タプルから新たな ``datetime.datetime``
   オブジェクトを生成して返します。

   .. versionadded:: 2.4


.. c:function:: PyObject* PyDate_FromTimestamp(PyObject *args)

   ``dateitme.date.fromtimestamp()`` に渡すのに適した引数タプルから新たな ``datetime.date``
   オブジェクトを生成して返します。

   .. versionadded:: 2.4

