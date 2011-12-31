.. highlightlang:: c

.. _bufferobjects:

buffer オブジェクトと memoryview オブジェクト
----------------------------------------------

.. sectionauthor:: Greg Stein <gstein@lyra.org>
.. sectionauthor:: Benjamin Peterson


.. index::
   object: buffer
   single: buffer interface

C で実装された Python オブジェクトは、"バッファインタフェース (buffer interface)" と呼ばれる一連の
関数を公開していることがあります。これらの関数は、あるオブジェクトのデータを生 (raw) のバイト列形式で公開するために使います。
このオブジェクトの使い手は、バッファインタフェースを使うことで、オブジェクトをあらかじめコピーしておく必要なしに、オブジェクトの
データに直接アクセスできます。

バッファインタフェースをサポートするオブジェクトの例として、文字列型とアレイ (array) 型の二つがあります。文字列オブジェクトは、
その内容をバッファインタフェースのバイト単位形式で公開しています。アレイもその内容を公開していますが、注意する必要が
あるのはアレイの要素は複数バイトの値になりうる、ということです。

バッファインタフェースの使い手の一例として、ファイルオブジェクトの :meth:`write` メソッドがあります。バッファインタフェースを
介してバイト列を公開しているオブジェクトは全て、ファイルへの書き出しができます。オブジェクトのバッファインタフェースを操作し、
対象となるオブジェクトからデータを返させる  :c:func:`PyArg_ParseTuple` には数多くのデータ書式化コードがあります。

バージョン 1.6 から、Python は Python レベルのバッファオブジェクトと、
C 言語レベルのバッファ API を提供しており、任意のビルトイン型やユーザー定義型は
その文字列表現を公開することができます。
しかし、両方共、幾つかの欠点のために廃止予定扱いされていて、
Python 3.0 では公式に削除され、新しい C 言語レベルのバッファ API と
新しい Python レベルの :class:`memoryview` という名前のオブジェクトに
置き換えられています。

新しいバッファ API は Python 2.6 に逆移植されており、 :class:`memoryviews`
オブジェクトは Python 2.7 に逆移植されています。
古いバージョンとの互換性が必要なければ、古いAPIの代わりにこれらを使うことをおすすめします。


新スタイル Py_buffer 構造体
===========================


.. c:type:: Py_buffer

   .. c:member:: void *buf

      オブジェクトのメモリの開始位置へのポインタ

   .. c:member:: Py_ssize_t len
      :noindex:

      メモリのトータルサイズ [byte]

   .. c:member:: int readonly

      バッファが読み込み専用かどうかを示す

   .. c:member:: const char *format
      :noindex:

      バッファを通してアクセスできる要素の形式を指定する、 :mod:`struct`
      モジュールスタイル文法の、 *NULL* 終端文字列。
      このポインタの値が *NULL* なら、 ``"B"`` (符号無しバイト) として扱われます。

   .. c:member:: int ndim

      メモリが多次元配列を表している時の次元数。 0 の場合、 :c:data:`strides`
      と :c:data:`suboffsets` は *NULL* でなければなりません。

   .. c:member:: Py_ssize_t *shape

      メモリが多次元配列を表しているとき、その形を示す長さ :c:data:`ndim` の
      :c:type:`Py_ssize_t` の配列。
      ``((*shape)[0] * ... * (*shape)[ndims-1])*itemsize`` は :c:data:`len`
      と等しくなければならないことに気をつけてください。

   .. c:member:: Py_ssize_t *strides

      各次元で次の要素を得るためにスキップするバイト数を示す、長さ :c:data:`ndim`
      の :c:type:`Py_ssize_t` の配列。

   .. c:member:: Py_ssize_t *suboffsets

      長さ :c:data:`ndim` の :c:type:`Py_ssize_t` の配列。
      suboffset の各数値が 0 以上であるとき、その次元に格納されているのはポインタで、
      suboffset の値はそのポインタの参照を解決するときに何バイトのオフセットを足すかを
      示しています。
      suboffset に負の数が格納されているときは、参照解決が不要であること
      (連続したメモリブロック内に直接配置されていること)を意味しています。

      次の例は、 strides も suboffsets も非NULL の時に、N次元配列からN次元インデックスで
      示される要素のポインタを返す関数です。 ::

          void *get_item_pointer(int ndim, void *buf, Py_ssize_t *strides,
              Py_ssize_t *suboffsets, Py_ssize_t *indices) {
              char *pointer = (char*)buf;
              int i;
              for (i = 0; i < ndim; i++) {
                  pointer += strides[i] * indices[i];
                  if (suboffsets[i] >=0 ) {
                      pointer = *((char**)pointer) + suboffsets[i];
                  }
              }
              return (void*)pointer;
           }


   .. c:member:: Py_ssize_t itemsize

      これは共有メモリ上の各要素のbyte単位のサイズを格納する変数です。
      これは :c:func:`PyBuffer_SizeFromFormat` を使って計算できる値なので
      技術的には不要なのですが、バッファを提供する側はフォーマット文字列を
      解析しなくてもこの情報を知っているでしょうし、バッファを受け取る側に
      とっては正しく解釈するのに必要な情報です。なので、要素サイズを格納する
      ほうが便利ですし高速です。

   .. c:member:: void *internal

      バッファを提供する側のオブジェクトが内部的に利用するための変数です。
      例えば、提供側はこの変数に整数型をキャストして、 shape, strides, suboffsets
      といった配列をバッファを開放するときに同時に開放するべきかどうかを
      管理するフラグに使うことができるでしょう。
      バッファを受け取る側は、この値を変更してはなりません。


バッファ関連関数
========================


.. c:function:: int PyObject_CheckBuffer(PyObject *obj)

   *obj* がバッファインタフェースをサポートしている場合に 1 を、
   それ以外の場合に 0 を返します。


.. c:function:: int PyObject_GetBuffer(PyObject *obj, Py_buffer *view, int flags)

      *obj* を :c:type:`Py_buffer` *view* へエクスポートします。
      これらの引数は *NULL* であってはなりません。
      *flag* 引数は呼び出し側がどんなバッファを扱おうとしているのか、
      バッファ提供側がどんなバッファを返すことが許されているのかを示す、
      ビットフィールドです。
      バッファインタフェースは複雑なメモリ共有を可能にしていますが、呼び出し元は
      すべての複雑なバッファを扱えるとは限らず、バッファ提供側がシンプルなビューを
      提供できるならそれを利用したいとかもしれません。

      バッファ提供側はすべての方法でメモリを共有できるとは限らず、呼び出し側に
      何かが不可能であることを伝えるためにエラーを発生させる必要があるかもしれません。
      その場合のエラーは、もしその問題を実際に引き起こしているのが別のエラーだったとしても、
      :exc:`BufferError` でなければなりません。
      バッファ提供側は flag の情報を使って :c:data:`Py_buffer` 構造体のどのフィールドへの
      非デフォルト値の設定を省略したり、要求されたシンプルな view を提供できない場合は
      エラーを発生させたりすることができます。

      成功したら 0 が、エラー時には -1 が返されます。

      次のテーブルは、 *flags* 引数が取りうる値です。

      +-----------------------------------+--------------------------------------------------------------+
      | Flag                              | 説明                                                         |
      +===================================+==============================================================+
      | :c:macro:`PyBUF_SIMPLE`           | これはデフォルトの flag の状態です。                         |
      |                                   | 結果のバッファは書き込み可能かもしれませんし、不可能かも     |
      |                                   | しれません。データのフォーマットは unsigned byte とします。  |
      |                                   | これは "スタンドアロン" のフラグ定数です。他の定数と '|'     |
      |                                   | を取る必要はありません。                                     |
      |                                   | 提供側はこのような連続したバイト列のバッファを提供できない   |
      |                                   | 場合に、エラーを発生させるかもしれません。                   |
      |                                   |                                                              |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_WRITABLE`         | 結果のバッファは書込み可能でなければなりません。             |
      |                                   | 書き込み不可能な場合はエラーを発生させます。                 |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_STRIDES`          | この値は :c:macro:`PyBUF_ND` を含みます。                    |
      |                                   | バッファは strides 情報を提供しなければなりません。          |
      |                                   | (言い換えると、 strides は NULL であってはいけません。)      |
      |                                   | このフラグは、呼び出し元が、要素間に隙間のある不連続な       |
      |                                   | 配列を扱えるときに使われます。 strides を扱うことは、        |
      |                                   | 自動的に shape も扱えることを要求されます。                  |
      |                                   | 提供側は stride 形式のバッファを提供できないとき(例えば、    |
      |                                   | suboffset が必要な場合)はエラーを発生させます。              |
      |                                   |                                                              |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_ND`               | バッファは shape 情報を提供しなければなりません。            |
      |                                   | メモリは C スタイルの並び (最後の次元が一番高速) だと仮定    |
      |                                   | されます。提供側はこの種類の連続バッファを提供できない場合は |
      |                                   | エラーを発生させます。このフラグが指定されていな場合は shape |
      |                                   | は *NULL* になります。                                       |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_C_CONTIGUOUS`     | これらのフラグは、返されるバッファの並びを指定します。       |
      | :c:macro:`PyBUF_F_CONTIGUOUS`     | それぞれ、C並び(最後の次元が一番高速)、Fortran並び(最初の    |
      | :c:macro:`PyBUF_ANY_CONTIGUOUS`   | 次元が一番高速), そのどちらでも、を意味します。              |
      |                                   | これらのフラグは :c:macro:`PyBUF_STRIDES` を含んでおり、     |
      |                                   | strides 情報が正しく格納されていることを保証します。         |
      |                                   |                                                              |
      |                                   |                                                              |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_INDIRECT`         | このフラグは、返されるバッファが suboffsets 情報を含んで     |
      |                                   | いることを示します。(suboffsets が必要無いときは NULL でも   |
      |                                   | かまいません。) このフラグは、バッファ利用側が suboffsets    |
      |                                   | を使って参照されている間接配列を扱えるときに利用されます。   |
      |                                   | このフラグは :c:macro:`PyBUF_STRIDES` を含みます。           |
      |                                   |                                                              |
      |                                   |                                                              |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_FORMAT`           | 返されるバッファは正しい format 情報を持っていなければ       |
      |                                   | なりません。このフラグは、バッファ利用側が実際に格納されて   |
      |                                   | いるデータの '種類' をチェックするときに利用します。         |
      |                                   | バッファ提供側は、要求された場合は常にこの情報を提供できる   |
      |                                   | べきです。 format が明示的に要求されていない場合は format は |
      |                                   | *NULL* (``'B'``, unsigned byte を意味する)であるべきです。   |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_STRIDED`          | ``(PyBUF_STRIDES | PyBUF_WRITABLE)`` と同じ                  |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_STRIDED_RO`       | ``(PyBUF_STRIDES)`` と同じ                                   |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_RECORDS`          | ``(PyBUF_STRIDES | PyBUF_FORMAT | PyBUF_WRITABLE)`` と同じ   |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_RECORDS_RO`       | ``(PyBUF_STRIDES | PyBUF_FORMAT)`` と同じ                    |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_FULL`             | ``(PyBUF_INDIRECT | PyBUF_FORMAT | PyBUF_WRITABLE)`` と同じ  |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_FULL_RO`          | ``(PyBUF_INDIRECT | PyBUF_FORMAT)`` と同じ                   |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_CONTIG`           | ``(PyBUF_ND | PyBUF_WRITABLE)`` と同じ                       |
      +-----------------------------------+--------------------------------------------------------------+
      | :c:macro:`PyBUF_CONTIG_RO`        | ``(PyBUF_ND)`` と同じ                                        |
      +-----------------------------------+--------------------------------------------------------------+


.. c:function:: void PyBuffer_Release(Py_buffer *view)

   *view* バッファを開放します。
   バッファが利用されなくなったときに、そのメモリを開放できるようにこの関数を呼び出すべきです。

.. c:function:: Py_ssize_t PyBuffer_SizeFromFormat(const char *)

   :c:data:`~Py_buffer.itemsize` の値を :c:data:`~PyBuffer.format` から計算して返します。


.. c:function:: int PyBuffer_IsContiguous(Py_buffer *view, char fortran)

   *view* で定義されているメモリが、 C スタイル (*fortran* == ``'C'``) のときか、
   Fortran スタイル (*fortran* == ``'F'``) のときか、そのいずれか
   (*fortran* == ``'A'``) であれば 1 を返します。
   それ以外の場合は 0 を返します。


.. c:function:: void PyBuffer_FillContiguousStrides(int ndim, Py_ssize_t *shape, Py_ssize_t *strides, Py_ssize_t itemsize, char fortran)

   *strides* 配列を、 *itemsize* の大きさの要素がバイト単位で連続した、
   *shape* の形をした (*fortran* が ``'C'`` なら C-style, ``'F'``
   なら Fortran-style の) 多次元配列として埋める。


.. c:function:: int PyBuffer_FillInfo(Py_buffer *view, PyObject *obj, void *buf, Py_ssize_t len, int readonly, int infoflags)

   バッファ提供側が与えられた長さの "unsigned bytes" の連続した1つのメモリブロックしか
   提供できないものとして、 *view* バッファ情報構造体を正しく埋める。
   成功したら 0 を、エラー時には (例外を発生させつつ) -1 を返す。


.. MemoryView objects

memoryview オブジェクト
========================

.. versionadded:: 2.7

:class:`memoryview` オブジェクトは、新しい、他のオブジェクトと同じように扱える
Python オブジェクトの形をした C言語レベルのバッファへのインタフェースです。

.. c:function:: PyObject *PyMemoryView_FromObject(PyObject *obj)

   新しいバッファインタフェースを定義しているオブジェクトから memoryview
   オブジェクトを作ります。


.. c:function:: PyObject *PyMemoryView_FromBuffer(Py_buffer *view)

   buffer-info 構造体 *view* をラップする memoryview オブジェクトを作ります。
   作られた memoryview オブジェクトはバッファを所有することになるので、
   *view* を開放してはいけません。このバッファは memoryview オブジェクトが削除されるときに
   解放されます。


.. c:function:: PyObject *PyMemoryView_GetContiguous(PyObject *obj, int buffertype, char order)

   buffer インタフェースを定義しているオブジェクトから ('C' か 'F'ortran の *order* で)
   連続したメモリチャンクへの memoryview オブジェクトを作ります。
   メモリが連続している場合、 memoryview オブジェクトは元のメモリを参照します。
   それ以外の場合、メモリはコピーされて、 memoryview オブジェクトは新しい bytes
   オブジェクトを参照します。


.. c:function:: int PyMemoryView_Check(PyObject *obj)

   *obj* が memoryview オブジェクトの場合に真を返します。
   現在のところ、 :class:`memoryview` のサブクラスの作成は許可されていません。


.. c:function:: Py_buffer *PyMemoryView_GET_BUFFER(PyObject *obj)

   与えられたオブジェクトにラップされた buffer-info 構造体へのポインタを返します。
   オブジェクトは memoryview インスタンスで **なければなりません** 。
   このマクロはオブジェクトの型をチェックしないので、呼び出し側で保証しなければ
   クラッシュする可能性があります。


旧スタイルバッファオブジェクト
=================================

.. index:: single: PyBufferProcs

古いバッファインタフェースに関するより詳しい情報は、 "バッファオブジェクト構造体" 節 ( :ref:`buffer-structs` 節) の、
:c:type:`PyBufferProcs` の説明のところにあります。

"バッファオブジェクト" はヘッダファイル :file:`bufferobject.h`  の中で定義されています (このファイルは
:file:`Python.h` がインクルードしています)。バッファオブジェクトは、 Python プログラミングの
レベルからは文字列オブジェクトと非常によく似ているように見えます: スライス、インデックス指定、結合、その他標準の文字列操作をサポート
しています。しかし、バッファオブジェクトのデータは二つのデータソース: 何らかのメモリブロックか、バッファインタフェースを公開している
別のオブジェクト、のいずれかに由来しています。

バッファオブジェクトは、他のオブジェクトのバッファインタフェースから Python プログラマにデータを公開する方法として便利です。
バッファオブジェクトはゼロコピーなスライス機構 (zero-copy slicing  mechanism) としても使われます。ブロックメモリを参照するという
バッファオブジェクトの機能を使うことで、任意のデータをきわめて簡単に Python プログラマに公開できます。メモリブロックは巨大でもかまいませんし、C
拡張モジュール内の定数配列でもかまいません。また、オペレーティングシステムライブラリ側に渡す前の、操作用の生のブロックメモリでもかまいませんし、
構造化されたデータをネイティブのメモリ配置形式でやりとりするためにも使えます。


.. c:type:: PyBufferObject

   この :c:type:`PyObject` のサブタイプはバッファオブジェクトを表現します。


.. c:var:: PyTypeObject PyBuffer_Type

   .. index:: single: BufferType (in module types)

   Python バッファ型 (buffer type) を表現する :c:type:`PyTypeObject` です; Python レイヤにおける
   ``buffer`` や ``types.BufferType`` と同じオブジェクトです。


.. c:var:: int Py_END_OF_BUFFER

   この定数は、 :c:func:`PyBuffer_FromObject` や :c:func:`PyBuffer_FromReadWriteObject` に
   *size* パラメタとして渡します。このパラメタを渡すと、 :c:type:`PyBufferObject` は指定された *offset*
   からバッファの終わりまでを *base* オブジェクトとして参照します。このパラメタを使うことで、関数の呼び出し側が *base* オブジェクト
   のサイズを調べる必要がなくなります。


.. c:function:: int PyBuffer_Check(PyObject *p)

   引数が :c:data:`PyBuffer_Type` 型のときに真を返します。


.. c:function:: PyObject* PyBuffer_FromObject(PyObject *base, Py_ssize_t offset, Py_ssize_t size)

   新たな読み出し専用バッファオブジェクトを返します。 *base* が読み出し専用バッファに必要なバッファプロトコルをサポートしていない
   場合や、厳密に一つのバッファセグメントを提供していない場合には :exc:`TypeError` を送出し、 *offset* がゼロ以下の場合には
   :exc:`ValueError` を送出します。バッファオブジェクトは *base* オブジェクトに対する参照を保持し、バッファオブジェクトの内容は
   *base* オブジェクトの *offset* から *size* バイトのバッファインタフェースへの参照になります。 *size* が
   :const:`Py_END_OF_BUFFER` の場合、新たに作成するバッファオブジェクトの内容は *base* から公開されているバッファの
   末尾までにわたります。

   .. versionchanged:: 2.5
      この関数は以前は *offset*, *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyBuffer_FromReadWriteObject(PyObject *base, Py_ssize_t offset, Py_ssize_t size)

   新たな書き込み可能バッファオブジェクトを返します。パラメタおよび例外は :c:func:`PyBuffer_FromObject` と同じです。 *base*
   オブジェクトが書き込み可能バッファに必要なバッファプロトコルを公開していない場合、 :exc:`TypeError` を送出します。

   .. versionchanged:: 2.5
      この関数は以前は *offset*, *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyBuffer_FromMemory(void *ptr, Py_ssize_t size)

   メモリ上の指定された場所から指定されたサイズのデータを読み出せる、新たな読み出し専用バッファオブジェクトを返します。
   この関数が返すバッファオブジェクトが存続する間、 *ptr* で与えられたメモリバッファがデアロケートされないようにするのは呼び出し側の責任です。 *size*
   がゼロ以下の場合には :exc:`ValueError` を送出します。 *size* には :const:`Py_END_OF_BUFFER` を指定しては
   *いけません* ; 指定すると、 :exc:`ValueError` を送出します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyBuffer_FromReadWriteMemory(void *ptr, Py_ssize_t size)

   :c:func:`PyBuffer_FromMemory` に似ていますが、書き込み可能なバッファを返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyBuffer_New(Py_ssize_t size)

   *size* バイトのメモリバッファを独自に維持する新たな書き込み可能バッファオブジェクトを返します。 *size*
   がゼロまたは正の値でない場合、 :exc:`ValueError` を送出します。( :c:func:`PyObject_AsWriteBuffer`
   が返すような) メモリバッファは特に整列されていないので注意して下さい。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

