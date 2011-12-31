.. highlightlang:: c

.. _unicodeobjects:

Unicode オブジェクトと codec
----------------------------

.. sectionauthor:: Marc-Andre Lemburg <mal@lemburg.com>

Unicode オブジェクト
^^^^^^^^^^^^^^^^^^^^

Unicode 型
""""""""""

以下は Python の Unicode 実装に用いられている基本 Unicode オブジェクト型です:


.. c:type:: Py_UNICODE

   この型は Unicode 序数 (Unicode ordinal) を保持するための基礎単位として、 Python が内部的に使います。
   Python のデフォルトのビルドでは、 :c:type:`Py_UNICODE` として 16-bit 型を利用し、 Unicode の値を内部では UCS-2 で保持します。
   UCS4 版の Python をビルドすることもできます。(最近の多くの Linux ディストリビューションでは UCS4 版の Python がついてきます)
   UCS4 版ビルドでは :c:type:`Py_UNICODE` に 32-bit 型を利用し、内部では Unicode データを UCS4 で保持します。
   :c:type:`wchar_t` が利用できて、 Python の Unicode に関するビルドオプションと
   一致するときは、 :c:type:`Py_UNICODE` は :c:type:`wchar_t` を typedef でエイリアス
   され、ネイティブプラットフォームに対する互換性を高めます。それ以外のすべてのプラットフォームでは、 :c:type:`Py_UNICODE` は
   :c:type:`unsigned short` (UCS2) か :c:type:`unsigned long` (UCS4) の
   typedef によるエイリアスになります。

UCS2 と UCS4 の Python ビルドの間にはバイナリ互換性がないことに注意してください。拡張やインタフェースを書くときには、このことを覚えておいてください。


.. c:type:: PyUnicodeObject

   この :c:type:`PyObject` のサブタイプは Unicode オブジェクトを表します。


.. c:var:: PyTypeObject PyUnicode_Type

   この :c:type:`PyTypeObject` のインスタンスは Python の Unicode 型を表します。
   Python レイヤにおける ``unicode`` や ``types.UnicodeType`` と同じオブジェクトです。

以下の API は実際には C マクロで、Unicode オブジェクト内部の読み出し専用データに対するチェックやアクセスを高速に行います:


.. c:function:: int PyUnicode_Check(PyObject *o)

   *o* が Unicode 文字列型か Unicode 文字列型のサブタイプであるときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyUnicode_CheckExact(PyObject *o)

   *o* が Unicode 文字列型で、かつ Unicode 文字列型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. c:function:: Py_ssize_t PyUnicode_GET_SIZE(PyObject *o)

   オブジェクトのサイズを返します。 *o* は :c:type:`PyUnicodeObject` でなければなりません (チェックはしません)。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_ssize_t PyUnicode_GET_DATA_SIZE(PyObject *o)

   オブジェクトの内部バッファのサイズをバイト数で返します。 *o* は :c:type:`PyUnicodeObject` でなければなりません
   (チェックはしません)。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_UNICODE* PyUnicode_AS_UNICODE(PyObject *o)

   オブジェクト内部の :c:type:`Py_UNICODE` バッファへのポインタを返します。  *o* は :c:type:`PyUnicodeObject`
   でなければなりません (チェックはしません)。


.. c:function:: const char* PyUnicode_AS_DATA(PyObject *o)

   オブジェクト内部バッファへのポインタを返します。  *o* は :c:type:`PyUnicodeObject` でなければなりません
   (チェックはしません)。

.. c:function:: int PyUnicode_ClearFreeList()

   free list をクリアします。
   開放できなかった要素数を返します。

   .. versionadded:: 2.6


Unicode 文字プロパティ
""""""""""""""""""""""""

Unicode は数多くの異なる文字プロパティ (character property) を提供しています。よく使われる文字プロパティは、以下のマクロ
で利用できます。これらのマクロは Python の設定に応じて、各々 C の関数に対応付けられています。


.. c:function:: int Py_UNICODE_ISSPACE(Py_UNICODE ch)

   *ch* が空白文字かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISLOWER(Py_UNICODE ch)

   *ch* が小文字かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISUPPER(Py_UNICODE ch)

   *ch* が大文字かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISTITLE(Py_UNICODE ch)

   *ch* がタイトルケース文字 (titlecase character) かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISLINEBREAK(Py_UNICODE ch)

   *ch* が改行文字かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISDECIMAL(Py_UNICODE ch)

   *ch* が 10 進の数字文字かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISDIGIT(Py_UNICODE ch)

   *ch* が 2 進の数字文字かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISNUMERIC(Py_UNICODE ch)

   *ch* が数字文字かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISALPHA(Py_UNICODE ch)

   *ch* がアルファベット文字かどうかに応じて 1 または 0 を返します。


.. c:function:: int Py_UNICODE_ISALNUM(Py_UNICODE ch)

   *ch* が英数文字かどうかに応じて 1 または 0 を返します。

以下の API は、高速に直接文字変換を行うために使われます:


.. c:function:: Py_UNICODE Py_UNICODE_TOLOWER(Py_UNICODE ch)

   *ch* を小文字に変換したものを返します。


.. c:function:: Py_UNICODE Py_UNICODE_TOUPPER(Py_UNICODE ch)

   *ch* を大文字に変換したものを返します。


.. c:function:: Py_UNICODE Py_UNICODE_TOTITLE(Py_UNICODE ch)

   *ch* をタイトルケース文字に変換したものを返します。


.. c:function:: int Py_UNICODE_TODECIMAL(Py_UNICODE ch)

   *ch* を 10 進の正の整数に変換したものを返します。不可能ならば ``-1`` を返します。このマクロは例外を送出しません。


.. c:function:: int Py_UNICODE_TODIGIT(Py_UNICODE ch)

   *ch* を一桁の 2 進整数に変換したものを返します。不可能ならば ``-1`` を返します。このマクロは例外を送出しません。


.. c:function:: double Py_UNICODE_TONUMERIC(Py_UNICODE ch)

   *ch* を :c:type:`double` に変換したものを返します。不可能ならば ``-1.0`` を返します。このマクロは例外を送出しません。


Plain Py_UNICODE
""""""""""""""""

Unicode オブジェクトを生成したり、Unicode のシーケンスとしての基本的なプロパティにアクセスしたりするには、以下の API を使ってください:


.. c:function:: PyObject* PyUnicode_FromUnicode(const Py_UNICODE *u, Py_ssize_t size)

   *size* で指定された長さを持つ Py_UNICODE 型バッファ *u*  から Unicode オブジェクトを生成します。 *u* を *NULL*
   にしてもよく、その場合オブジェクトの内容は未定義です。バッファに必要な情報を埋めるのはユーザの責任です。バッファの内容は新たなオブジェクトに
   コピーされます。バッファが *NULL* でない場合、戻り値は共有されたオブジェクトになることがあります。従って、この関数が返す Unicode
   オブジェクトを変更してよいのは *u* が *NULL* のときだけです。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_UNICODE* PyUnicode_AsUnicode(PyObject *unicode)

   Unicode オブジェクトの内部バッファ :c:type:`Py_UNICODE` に対する読み出し専用のポインタを返します。 *unicode* が
   Unicode オブジェクトでなければ *NULL* を返します。


.. c:function:: PyObject* PyUnicode_FromStringAndSize(const char *u, Py_ssize_t size)

   char 型バッファ *u*  から Unicode オブジェクトを生成します。
   *u* の内容は UTF-8 エンコードされているものとします。
   *u* を *NULL* にしてもよく、その場合オブジェクトの内容は未定義で、
   バッファに必要な情報を埋めるのはユーザの責任です。バッファの内容は新たなオブジェクトに
   コピーされます。バッファが *NULL* でない場合、戻り値は共有されたオブジェクトになることがあります。
   従って、この関数が返す Unicode オブジェクトを変更してよいのは *u* が *NULL* のときだけです。

   .. versionadded:: 2.6


.. c:function:: PyObject *PyUnicode_FromString(const char *u)

   UTF-8 エンコードされたNUL文字終端のchar 型バッファ *u* から Unicode オブジェクトを生成します。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyUnicode_FromFormat(const char *format, ...)

   :c:func:`printf` スタイルの *format* 文字列と可変長引数を受け取り、
   結果の unicode 文字の長さを計算し、フォーマットされた文字列を含む unicode オブジェクトを
   返します。可変長引数は C の型を持っていて、 *format* 文字列で指定された書式指定文字に
   完全に従う必要があります。
   以下の書式指定文字が利用できます:

   +-------------------+---------------------+--------------------------------------------+
   | 書式指定文字      | 型                  | 備考                                       |
   +===================+=====================+============================================+
   | :attr:`%%`        | *n/a*               | リテラルの % 文字                          |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%c`        | int                 | C言語のintで表現される1文字                |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%d`        | int                 | ``printf("%d")`` と全く同じ                |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%u`        | unsigned int        | ``printf("%u")`` と全く同じ                |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%ld`       | long                | ``printf("%ld")`` と全く同じ               |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%lu`       | unsigned long       | ``printf("%lu")`` と全く同じ               |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%zd`       | Py_ssize_t          | ``printf("%zd")`` と全く同じ               |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%zu`       | size_t              | ``printf("%zu")`` と全く同じ               |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%i`        | int                 | ``printf("%i")`` と全く同じ                |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%x`        | int                 | ``printf("%x")`` と全く同じ                |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%s`        | char\*              | NUL 文字で終わる文字列                     |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%p`        | void\*              | C ポインタの16進数表現。                   |
   |                   |                     | ``printf("%p")`` とほぼ同じですが、        |
   |                   |                     | プラットフォームの ``printf`` に依存せず   |
   |                   |                     | ``0x`` リテラルで始まることが保証されます  |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%U`        | PyObject\*          | unicode オブジェクト                       |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%V`        | PyObject\*, char \* | unicode オブジェクト(*NULL* でも良い)と、  |
   |                   |                     | 2つめの引数として NUL 終端の C 文字列      |
   |                   |                     | (2つめの引数は1つめの引数が *NULL* だった  |
   |                   |                     | 時にのみ利用されます)                      |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%S`        | PyObject\*          | :func:`PyObject_Unicode` の戻り値          |
   +-------------------+---------------------+--------------------------------------------+
   | :attr:`%R`        | PyObject\*          | :func:`PyObject_Repr` の戻り値             |
   +-------------------+---------------------+--------------------------------------------+

   解釈されない書式指定文字があると、それ以降のフォーマット文字列はそのまま出力の文字列にコピーされ、
   以降の引数は無視されます。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyUnicode_FromFormatV(const char *format, va_list vargs)

   2引数であることを除いて :c:func:`PyUnicode_FromFormat` と同じです。

   .. versionadded:: 2.6


.. c:function:: Py_ssize_t PyUnicode_GetSize(PyObject *unicode)

   Unicode オブジェクトの長さを返します。

   .. versionchanged:: 2.5
      これらの関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_FromEncodedObject(PyObject *obj, const char *encoding, const char *errors)

   あるエンコード方式でエンコードされたオブジェクト *obj* を Unicode オブジェクトに型強制して、参照カウントをインクリメントして返します。

   型強制は以下のようにして行われます:

   文字列やその他の char バッファ互換オブジェクトの場合、オブジェクトは *encoding* に従ってデコードされます。このとき *error* で
   定義されたエラー処理を用います。これら二つの引数は *NULL* にでき、その場合デフォルト値が使われます (詳細は次の節を参照してください)

   その他のUnicodeオブジェクトを含むオブジェクトは :exc:`TypeError` 例外を引き起こします。

   この API は、エラーが生じたときには *NULL* を返します。呼び出し側は返されたオブジェクトに対し参照カウンタを 1 つ減らす (decref) する責任があります。


.. c:function:: PyObject* PyUnicode_FromObject(PyObject *obj)

   ``PyUnicode_FromEncodedObject(obj, NULL, "strict")`` を行うショートカットで、インタプリタは Unicode
   への型強制が必要な際に常にこの関数を使います。

プラットフォームで :c:type:`wchar_t` がサポートされていて、かつ wchar.h が提供されている場合、Python は以下の関数を使って
:c:type:`wchar_t` に対して直接アクセスすることができます。このアクセスは、Python 自体の :c:type:`Py_UNICODE`
型がシステムの :c:type:`wchar_t` と同一の場合に最適化されます。

wchar_t サポート
"""""""""""""""""

:c:type:`wchar_t` をサポートするプラットフォームでの wchar_t サポート:

.. c:function:: PyObject* PyUnicode_FromWideChar(const wchar_t *w, Py_ssize_t size)

   *size* の :c:type:`wchar_t` バッファ *w* から Unicode オブジェクトを生成します。
   失敗すると *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: Py_ssize_t PyUnicode_AsWideChar(PyUnicodeObject *unicode, wchar_t *w, Py_ssize_t size)

   Unicode オブジェクトの内容を :c:type:`wchar_t` バッファ *w* にコピーします。最大で *size* 個の
   :c:type:`wchar_t` 文字を (末尾の 0-終端文字を除いて) コピーします。コピーした :c:type:`wchar_t`
   文字の個数を返します。エラーの時には -1 を返します。 :c:type:`wchar_t` 文字列は 0-終端されている場合も、されていない場合も
   あります。関数の呼び出し側の責任で、アプリケーションの必要に応じて :c:type:`wchar_t` 文字列を 0-終端してください。

   .. versionchanged:: 2.5
      この関数は以前は :c:type:`int` を返し、 *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. _builtincodecs:

組み込み codec (built-in codec)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python には、処理速度を高めるために C で書かれた codec が揃えてあります。
これら全ての codec は以下の関数を介して直接利用できます。

以下の API の多くが、 *encoding* と *errors* という二つの引数をとります。これらのパラメータは、組み込みの Unicode
オブジェクトコンストラクタである :func:`unicode` における同名のパラメータと同じ意味を持ちます。

*encoding* を *NULL* にすると、デフォルトエンコーディングである ASCII を使います。ファイルシステムに関する関数の呼び出し
では、ファイル名に対するエンコーディングとして :c:data:`Py_FileSystemDefaultEncoding` を使わねばなりません。
この変数は読み出し専用の変数として扱わねばなりません: この変数は、あるシステムによっては静的な文字列に対するポインタで
あったり、また別のシステムでは、(アプリケーションが setlocale を読んだときなどに) 変わったりもします。

*errors* で指定するエラー処理もまた、 *NULL* を指定できます。 *NULL* を指定すると、codec で定義されているデフォルト処理の使用を
意味します。全ての組み込み codec で、デフォルトのエラー処理は "strict" (:exc:`ValueError` を送出する) になっています。

個々の codec は全て同様のインタフェースを使っています。個別の codec の説明では、説明を簡単にするために以下の汎用のインタフェースとの
違いだけを説明しています。


汎用 codec
""""""""""

以下は汎用 codec の API です:

.. c:function:: PyObject* PyUnicode_Decode(const char *s, Py_ssize_t size, const char *encoding, const char *errors)

   何らかのエンコード方式でエンコードされた、 *size* バイトの文字列 *s* をデコードして Unicode オブジェクトを生成します。
   *encoding* と *errors* は、組み込み関数 unicode() の同名のパラメータと同じ意味を持ちます。使用する codec の検索は、
   Python の codec レジストリを使って行います。codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_Encode(const Py_UNICODE *s, Py_ssize_t size, const char *encoding, const char *errors)

   *size* で指定されたサイズの :c:type:`Py_UNICODE` バッファ *s* をエンコードした
   Python 文字列オブジェクトを返します。
   *encoding* および *errors* は Unicode 型の :meth:`encode` メソッドに与える同名のパラメータと
   同じ意味を持ちます。使用する codec の検索は、 Python の codec レジストリを使って行います。codec が例外を送出した場合には
   *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_AsEncodedString(PyObject *unicode, const char *encoding, const char *errors)

   Unicode オブジェクトをエンコードし、その結果を Python 文字列オブジェクトとして返します。 *encoding* および *errors* は
   Unicode 型の :meth:`encode` メソッドに与える同名のパラメータと同じ意味を持ちます。使用する codec の検索は、 Python の
   codec レジストリを使って行います。codec が例外を送出した場合には *NULL* を返します。


UTF-8 Codecs
""""""""""""

以下は UTF-8 codec の APIです:


.. c:function:: PyObject* PyUnicode_DecodeUTF8(const char *s, Py_ssize_t size, const char *errors)

   UTF-8 でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec が例外を送出した場合には
   *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_DecodeUTF8Stateful(const char *s, Py_ssize_t size, const char *errors, Py_ssize_t *consumed)

   *consumed* が *NULL* の場合、 :c:func:`PyUnicode_DecodeUTF8` と同じように動作します。 *consumed* が
   *NULL* でない場合、 :c:func:`PyUnicode_DecodeUTF8Stateful` は末尾の不完全な UTF-8 バイト列
   をエラーとみなしません。これらのバイト列はデコードされず、デコードされたバイト数を *consumed* に返します。

   .. versionadded:: 2.4

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_EncodeUTF8(const Py_UNICODE *s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :c:type:`Py_UNICODE` 型バッファ *s* を UTF-8 で
   エンコードし、 Python 文字列オブジェクトにして返します。
   codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_AsUTF8String(PyObject *unicode)

   UTF-8 で Unicode オブジェクトをエンコードし、結果を Python 文字列オブジェクトとして返します。エラー処理は "strict" です。
   codec が例外を送出した場合には *NULL* を返します。


UTF-32 Codecs
"""""""""""""

以下は UTF-32 codec API です。


.. c:function:: PyObject* PyUnicode_DecodeUTF32(const char *s, Py_ssize_t size, const char *errors, int *byteorder)

   UTF-32 でエンコードされたバッファ文字列から *size* バイトをデコードし、
   Unicodeオブジェクトとして返します。
   *errors* は (*NULL* でないなら) エラーハンドラを指定します。デフォルトは "strict" です。

   *byteorder* が *NULL* でない時、デコーダは与えられたバイトオーダーでデコードを開始します。 ::

      *byteorder == -1: little endian
      *byteorder == 0:  native order
      *byteorder == 1:  big endian

   ``*byteorder`` が 0 で入力データの最初の 4 バイトがバイトオーダーマーク (BOM) だった場合、
   デコーダーは BOM のバイトオーダーに切り替え、 BOM は結果の unicode 文字列には含まれません。
   ``*byteorder`` が ``-1`` か ``1`` だった場合、すべての BOM は出力へコピーされます。

   デコードが完了した後、入力データの終端に来た時点でのバイトオーダーを *\*byteorder* にセットします。

   narrow build の場合、BMP 外のコードポイントはサロゲートペアとしてデコードされます。

   *byteorder* が *NULL* のとき、 codec は native order モードで開始します。

   codec が例外を発生させたときは *NULL* を返します。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyUnicode_DecodeUTF32Stateful(const char *s, Py_ssize_t size, const char *errors, int *byteorder, Py_ssize_t *consumed)

   *consumed* が *NULL* のとき、 :c:func:`PyUnicode_DecodeUTF32` と同じように振る舞います。
   *consumed* が *NULL* でないとき、 :c:func:`PyUnicode_DecodeUTF32Stateful` は末尾の
   不完全な (4 で割り切れない長さのバイト列などの) UTF-32 バイト列をエラーとして扱いません。
   末尾の不完全なバイト列はデコードされず、デコードされたバイト数が *consumed*
   に格納されます。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyUnicode_EncodeUTF32(const Py_UNICODE *s, Py_ssize_t size, const char *errors, int byteorder)

   *s* の Unicode データを UTF-32 にエンコードし、その値を Python の bytes
   オブジェクトに格納して返します。
   出力は以下のバイトオーダーで従って書かれます。 ::

      byteorder == -1: little endian
      byteorder == 0:  native byte order (BOM マークあり)
      byteorder == 1:  big endian

   byteorder が ``0`` のとき、出力文字列は常に Unicode BOM マーク (U+FEFF) で始まります。
   それ以外の2つのモードでは、先頭に BOM マークは出力されません。

   *Py_UNICODE_WIDE* が定義されていない場合は、サロゲートペアを 1 つのコードポイントとして
   出力します。

   codec が例外を発生させた場合、 *NULL* を返します。

   .. versionadded:: 2.6


.. c:function:: PyObject* PyUnicode_AsUTF32String(PyObject *unicode)

   ネイティブバイトオーダーで UTF-32 エンコーディングされた Python 文字列を
   返します。
   文字列は常に BOM マークで始まります。
   エラーハンドラは "strict" です。
   codec が例外を発生させたときは *NULL* を返します。

   .. versionadded:: 2.6


UTF-16 Codecs
"""""""""""""

以下は UTF-16 codec の APIです:


.. c:function:: PyObject* PyUnicode_DecodeUTF16(const char *s, Py_ssize_t size, const char *errors, int *byteorder)

   UTF-16 でエンコードされたバッファ *s* から *size* バイトだけデコードして、結果を Unicode オブジェクトで返します。 *errors*
   は (*NULL* でない場合) エラー処理方法を定義します。デフォルト値は "strict" です。

   *byteorder* が *NULL* でない場合、デコード機構は以下のように指定されたバイト整列 (byte order) に従ってデコードを開始
   します::

      *byteorder == -1: little endian
      *byteorder == 0:  native order
      *byteorder == 1:  bit endian

   ``*byteorder`` が 0 で、入力データの先頭2バイトがバイトオーダーマーク (BOM)
   だった場合、デコーダは BOM が示すバイトオーダーに切り替え、そのBOMを結果の Unicode
   文字列にコピーしません。
   ``*byteorder`` が ``-1`` か ``1`` だった場合、すべてのBOMは出力へコピーされます。
   (出力では ``\ufeff`` か ``\ufffe`` のどちらかになるでしょう)

   デコードを完了した後、入力データの終端に来た時点でのバイトオーダーを *\*byteorder* にセットします。

   *byteorder* が *NULL* の場合、 codec はネイティブバイト整列のモードで開始します。

   codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_DecodeUTF16Stateful(const char *s, Py_ssize_t size, const char *errors, int *byteorder, Py_ssize_t *consumed)

   *consumed* が *NULL* の場合、 :c:func:`PyUnicode_DecodeUTF16` と同じように動作します。 *consumed* が
   *NULL* でない場合、 :c:func:`PyUnicode_DecodeUTF16Stateful` は末尾の不完全な UTF-16 バイト列
   (奇数長のバイト列や分割されたサロゲートペア) をエラーとみなしません。これらのバイト列はデコードされず、デコードされたバイト数を *consumed*
   に返します。

   .. versionadded:: 2.4

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用し、 *consumed* の型に :c:type:`int *` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_EncodeUTF16(const Py_UNICODE *s, Py_ssize_t size, const char *errors, int byteorder)

   *s* 中の Unicode データを UTF-16 でエンコードした結果が入っている Python 文字列オブジェクトを返します。
   出力は以下のバイトオーダーに従って書き出されます::

      byteorder == -1: little endian
      byteorder == 0:  native byte order (BOM マークあり)
      byteorder == 1:  big endian

   byteorder が ``0`` の場合、出力結果となる文字列は常に Unicode BOM マーク
   (U+FEFF) で始まります。それ以外のモードでは、 BOM マークを頭につけません。

   *Py_UNICODE_WIDE* が定義されている場合、単一の :c:type:`Py_UNICODE` 値はサロゲートペアとして表現されることがあります。
   *Py_UNICODE_WIDE* が定義されていなければ、各 :c:type:`Py_UNICODE` 値は UCS-2 文字として表現されます。

   codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_AsUTF16String(PyObject *unicode)

   ネイティブバイトオーダの UTF-16 でエンコードされた Python 文字列を返します。文字列は常に BOM マークから始まります。エラー処理は
   "strict" です。 codec が例外を送出した場合には *NULL* を返します。


UTF-7 Codecs
""""""""""""
以下は UTF-7 codec の API です。

.. c:function:: PyObject* PyUnicode_DecodeUTF7(const char *s, Py_ssize_t size, const char *errors)

   UTF-7 でエンコードされた *size* バイトの文字列 *s* をデコードして
   Unicode オブジェクトを作成します。
   codec が例外を発生させたときは *NULL* を返します。


.. c:function:: PyObject* PyUnicode_DecodeUTF7Stateful(const char *s, Py_ssize_t size, const char *errors, Py_ssize_t *consumed)

   *consumed* が *NULL* のとき、 :c:func:`PyUnicode_DecodeUTF7` と同じように動作します。
   *consumed* が *NULL* でないとき、末尾の不完全な UTF-7 base-64 部分をエラーとしません。
   不完全な部分のバイト列はデコードせずに、デコードしたバイト数を *consumed* に格納します。


.. c:function:: PyObject* PyUnicode_EncodeUTF7(const Py_UNICODE *s, Py_ssize_t size, int base64SetO, int base64WhiteSpace, const char *errors)

   与えられたサイズの :c:type:`Py_UNICODE` バッファを UTF-7 でエンコードして、
   Python の bytes オブジェクトとして返します。
   codec が例外を発生させたときは *NULL* を返します。

   *base64SetO* がゼロでないとき、 "Set O" 文字
   (他の場合には何も特別な意味を持たない句読点) を base-64 エンコードします。
   *base64WhiteSpace* がゼロでないとき、空白文字を base-64 エンコードします。
   Python の "utf-7" codec では、両方ともゼロに設定されています。


Unicode-Escape Codecs
"""""""""""""""""""""""

以下は "Unicode Escape" codec の API です:


.. c:function:: PyObject* PyUnicode_DecodeUnicodeEscape(const char *s, Py_ssize_t size, const char *errors)

   Unicode-Escape でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec
   が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_EncodeUnicodeEscape(const Py_UNICODE *s, Py_ssize_t size)

   *size* で指定された長さを持つ :c:type:`Py_UNICODE` 型バッファを Unicode-Escape でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_AsUnicodeEscapeString(PyObject *unicode)

   Unicode-Escape で Unicode オブジェクトをエンコードし、結果を  Python 文字列オブジェクトとして返します。エラー処理は
   "strict" です。 codec が例外を送出した場合には *NULL* を返します。


Raw-Unicode-Escape Codecs
"""""""""""""""""""""""""

以下は "Raw Unicode Escape" codec の APIです:


.. c:function:: PyObject* PyUnicode_DecodeRawUnicodeEscape(const char *s, Py_ssize_t size, const char *errors)

   Raw-Unicode-Escape でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec
   が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_EncodeRawUnicodeEscape(const Py_UNICODE *s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :c:type:`Py_UNICODE` 型バッファを Raw-Unicode-Escape でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_AsRawUnicodeEscapeString(PyObject *unicode)

   Raw-Unicode-Escape で Unicode オブジェクトをエンコードし、結果を  Python 文字列オブジェクトとして返します。エラー処理は
   "strict" です。 codec が例外を送出した場合には *NULL* を返します。


Latin-1 Codecs
""""""""""""""

以下は Latin-1 codec の APIです: Latin-1 は、 Unicode 序数の最初の 256 個に対応し、エンコード時にはこの 256
個だけを受理します。


.. c:function:: PyObject* PyUnicode_DecodeLatin1(const char *s, Py_ssize_t size, const char *errors)

   Latin-1 でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec が例外を送出した場合には
   *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_EncodeLatin1(const Py_UNICODE *s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :c:type:`Py_UNICODE` 型バッファを Latin-1 でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_AsLatin1String(PyObject *unicode)

   Latin-1 で Unicode オブジェクトをエンコードし、結果を Python 文字列オブジェクトとして返します。エラー処理は "strict" です。
   codec が例外を送出した場合には *NULL* を返します。

ASCII Codecs
""""""""""""

以下は ASCII codec の APIです。 7 ビットの ASCII データだけを受理します。その他のコードはエラーになります。


.. c:function:: PyObject* PyUnicode_DecodeASCII(const char *s, Py_ssize_t size, const char *errors)

   ASCII でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec が例外を送出した場合には
   *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_EncodeASCII(const Py_UNICODE *s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :c:type:`Py_UNICODE` 型バッファを ASCII でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_AsASCIIString(PyObject *unicode)

   ASCII で Unicode オブジェクトをエンコードし、結果を Python 文字列オブジェクトとして返します。エラー処理は "strict" です。
   codec が例外を送出した場合には *NULL* を返します。


Character Map Codecs
""""""""""""""""""""

この codec は、多くの様々な codec を実装する際に使われるという点で特殊な codec です (実際、 :mod:`encodings`
パッケージに入っている標準 codecs のほとんどは、この codec を使っています)。この codec は、文字のエンコードやデコードにマップ型
(mapping) を使います。

デコード用のマップ型は、文字列型の字列一組みを、 Unicode 型の字列一組、整数 (Unicode 序数として解釈されます) または ``None``
("定義されていない対応付け (undefined mapping)" を意味し、エラーを引き起こします) のいずれかに対応付けなければなりません。

エンコード用のマップ型は、Unicode 型の字列一組みを、 string 型の字列一組、整数 (Latin-1 序数として解釈されます) または
``None`` ("定義されていない対応付け (undefined mapping)" を意味し、エラーを引き起こします) の
いずれかに対応付けなければなりません。

マップ型オブジェクトは、 :meth:`__getitem__` マップ型インタフェースをサポートしなければなりません。

ある文字の検索が LookupError によって失敗すると、その文字はそのままコピーされます。すなわち、その文字の序数値がそれぞれ  Unicode または
Latin-1 として解釈されます。このため、codec を実現するマップ型に入れる必要がある対応付け関係は、ある文字を別の
コード点に対応付けるものだけです。

以下は mapping codec の APIです:

.. c:function:: PyObject* PyUnicode_DecodeCharmap(const char *s, Py_ssize_t size, PyObject *mapping, const char *errors)

   エンコードされた *size* バイトの文字列 *s* から  *mapping* に指定されたオブジェクトを使って Unicode オブジェクトを
   生成します。codec が例外を送出した場合には *NULL* を返します。
   もし、 *mapping* が *NULL* だった場合、latin-1 でデコードされます。それ以外の場合では、 *mapping* は byte に対する辞書マップ
   (訳注: s に含まれる文字の unsigned な値を int 型でキーとして、値として変換対象の Unicode 文字を表す Unicode 文字列になっているような辞書)
   か、ルックアップテーブルとして扱われる Unicode 文字列です。

   文字列 (訳注: mapping が Unicode 文字列として渡された場合) の長さより大きい byte 値や、(訳注: mappingにしたがって変換した結果が)
   U+FFFE "characters" になる Byte値は、"定義されていない対応付け (undefined mapping)" として扱われます。

   .. versionchanged:: 2.4
      mapping引数としてunicodeが使えるようになりました.

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_EncodeCharmap(const Py_UNICODE *s, Py_ssize_t size, PyObject *mapping, const char *errors)

   *size* で指定された長さを持つ :c:type:`Py_UNICODE` 型バッファを *mapping* に指定されたオブジェクトを使ってエンコードし、
   Python 文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_AsCharmapString(PyObject *unicode, PyObject *mapping)

   Unicode オブジェクトを *mapping* に指定されたオブジェクトを使ってエンコードし、結果を Python 文字列オブジェクトとして返します。
   エラー処理は "strict" です。 codec が例外を送出した場合には *NULL* を返します。

以下の codec API は Unicode から Unicode への対応付けを行う特殊なものです。


.. c:function:: PyObject* PyUnicode_TranslateCharmap(const Py_UNICODE *s, Py_ssize_t size, PyObject *table, const char *errors)

   *size* で指定された長さを持つ :c:type:`Py_UNICODE` バッファを、文字変換マップ *table*
   を適用して変換し、変換結果を Unicode オブジェクトで返します。
   codec が例外を発行した場合には *NULL* を返します。

   対応付けを行う *table* は、 Unicode 序数を表す整数を Unicode 序数を表す整数または ``None`` に対応付けます。
   (``None`` の場合にはその文字を削除します)

   対応付けテーブルが提供する必要があるメソッドは :meth:`__getitem__` インタフェースだけです; 従って、辞書や
   シーケンス型を使ってもうまく動作します。対応付けを行っていない (:exc:`LookupError` を起こすような) 文字序数に対しては、
   変換は行わず、そのままコピーします。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. MBCS codecs for Windows

Windows 用の MBCS codec
"""""""""""""""""""""""

以下は MBCS codec の API です。この codec は現在のところ、 Windows 上だけで利用でき、変換の実装には Win32 MBCS
変換機構 (Win32 MBCS converter) を使っています。 MBCS (または DBCS) はエンコード方式の種類 (class)
を表す言葉で、単一のエンコード方式を表すわけでなないので注意してください。利用されるエンコード方式 (target encoding) は、 codec
を動作させているマシン上のユーザ設定で定義されています。


.. c:function:: PyObject* PyUnicode_DecodeMBCS(const char *s, Py_ssize_t size, const char *errors)

   MBCS でエンコードされた *size* バイトの文字列 *s* から Unicode オブジェクトを生成します。codec が例外を送出した場合には
   *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_DecodeMBCSStateful(const char *s, int size, const char *errors, int *consumed)

   *consumed* が *NULL* のとき、 :c:func:`PyUnicode_DecodeMBCS` と同じ動作をします。
   *consumed* が *NULL* でないとき、 :c:func:`PyUnicode_DecodeMBCSStateful` は
   文字列の最後にあるマルチバイト文字の前半バイトをデコードせず、 *consumed* にデコードしたバイト数を格納します。

   .. versionadded:: 2.5


.. c:function:: PyObject* PyUnicode_EncodeMBCS(const Py_UNICODE *s, Py_ssize_t size, const char *errors)

   *size* で指定された長さを持つ :c:type:`Py_UNICODE` 型バッファを MBCS でエンコードし、 Python
   文字列オブジェクトにして返します。 codec が例外を送出した場合には *NULL* を返します。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_AsMBCSString(PyObject *unicode)

   MBCS で Unicode オブジェクトをエンコードし、結果を Python 文字列オブジェクトとして返します。エラー処理は "strict" です。
   codec が例外を送出した場合には *NULL* を返します。


Methods & Slots
"""""""""""""""

.. _unicodemethodsandslots:

メソッドおよびスロット関数 (slot function)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下の API は Unicode オブジェクトおよび文字列を入力に取り (説明では、どちらも文字列と表記しています)、場合に応じて Unicode
オブジェクトか整数を返す機能を持っています。

これらの関数は全て、例外が発生した場合には *NULL* または ``-1`` を返します。


.. c:function:: PyObject* PyUnicode_Concat(PyObject *left, PyObject *right)

   二つの文字列を結合して、新たな Unicode 文字列を生成します。


.. c:function:: PyObject* PyUnicode_Split(PyObject *s, PyObject *sep, Py_ssize_t maxsplit)

   Unicode 文字列のリストを分割して、 Unicode 文字列からなるリストを返します。
   *sep* が *NULL* の場合、全ての空白文字を使って
   分割を行います。それ以外の場合、指定された文字を使って分割を行います。最大で *maxsplit* 個までの分割を行います。 *maxsplit*
   が負ならば分割数に制限を設けません。分割結果のリスト内には分割文字は含みません。

   .. versionchanged:: 2.5
      この関数は以前は *maxsplit* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyUnicode_Splitlines(PyObject *s, int keepend)

   Unicode 文字列を改行文字で区切り、Unicode 文字列からなるリストを返します。CRLF は一個の改行文字とみなします。 *keepend* が 0
   の場合、分割結果のリスト内に改行文字を含めません。


.. c:function:: PyObject* PyUnicode_Translate(PyObject *str, PyObject *table, const char *errors)

   文字列に文字変換マップ *table* を適用して変換し、変換結果を  Unicode オブジェクトで返します。

   対応付けを行う *table* は、 Unicode 序数を表す整数を Unicode 序数を表す整数または ``None`` に対応付けます。
   (``None`` の場合にはその文字を削除します)

   対応付けテーブルが提供する必要があるメソッドは :meth:`__getitem__` インタフェースだけです; 従って、辞書や
   シーケンス型を使ってもうまく動作します。対応付けを行っていない (:exc:`LookupError` を起こすような) 文字序数に対しては、
   変換は行わず、そのままコピーします。

   *errors* は codecs で通常使われるのと同じ意味を持ちます。 *errors* は *NULL* にしてもよく、デフォルトエラー処理の
   使用を意味します。


.. c:function:: PyObject* PyUnicode_Join(PyObject *separator, PyObject *seq)

   指定した *separator* で文字列からなるシーケンスを連結 (join) し、
   連結結果を Unicode 文字列で返します。


.. c:function:: int PyUnicode_Tailmatch(PyObject *str, PyObject *substr, Py_ssize_t start, Py_ssize_t end, int direction)

   *substr* が ``str[start:end]`` の末端 (*direction* == -1 は先頭一致、 *direction* == 1 は末尾一致) で
   とマッチする場合に 1 を返し、それ以外の場合には 0 を返します。エラーが発生した時は ``-1``
   を返します。

   .. versionchanged:: 2.5
      この関数は以前は *start*, *end* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: Py_ssize_t PyUnicode_Find(PyObject *str, PyObject *substr, Py_ssize_t start, Py_ssize_t end, int direction)

   ``str[start:end]`` 中に *substr* が最初に出現する場所を返します。このとき指定された検索方向 *direction*
   (*direction* == 1 は順方向検索、 *direction* == -1 は逆方向検索) で検索します。戻り値は最初にマッチが見つかった場所の
   インデクスです; 戻り値 ``-1`` はマッチが見つからなかったことを表し、 ``-2`` はエラーが発生して例外情報が設定されていることを表します。

   .. versionchanged:: 2.5
      この関数は以前は *start*, *end* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: Py_ssize_t PyUnicode_Count(PyObject *str, PyObject *substr, Py_ssize_t start, Py_ssize_t end)

   ``str[start:end]`` に *substr* が重複することなく出現する回数を返します。エラーが発生した場合には ``-1`` を返します。

   .. versionchanged:: 2.5
      この関数は以前は *start*, *end* と戻り値の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyUnicode_Replace(PyObject *str, PyObject *substr, PyObject *replstr, Py_ssize_t maxcount)

   *str* 中に出現する *substr* を最大で *maxcount* 個 *replstr* に置換し、置換結果を Unicode オブジェクトにして
   返します。 *maxcount* == -1 にすると、全ての *substr* を置換します。

   .. versionchanged:: 2.5
      この関数は以前は *maxcount* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: int PyUnicode_Compare(PyObject *left, PyObject *right)

   二つの文字列を比較して、左引数が右引数より小さい場合、左右引数が等価の場合、左引数が右引数より大きい場合に対して、それぞれ -1, 0, 1 を返します。


.. c:function:: int PyUnicode_RichCompare(PyObject *left,  PyObject *right,  int op)

   二つのunicode文字列を比較して、下のうちの一つを返します:

   * ``NULL`` を、例外が発生したときに返します。
   * :const:`Py_True` もしくは :const:`Py_False` を、正しく比較できた時に返します。
   * :const:`Py_NotImplemented` を、 *left* と *right* のどちらかに対する
     :c:func:`PyUnicode_FromObject` が失敗したときに返します。(原文: in case the type combination is
     unknown)

   .. 訳注: 原文が分かりにくいので翻訳者が解説しました。

   :const:`Py_EQ` と :const:`Py_NE` の比較は、引数からUnicodeへの変換が :exc:`UnicodeDecodeError`
   で失敗した時に、 :exc:`UnicodeWarning` を発生する可能性があることに注意してください。

   *op* に入れられる値は、 :const:`Py_GT`, :const:`Py_GE`, :const:`Py_EQ`, :const:`Py_NE`,
   :const:`Py_LT`, and :const:`Py_LE` のどれかです。


.. c:function:: PyObject* PyUnicode_Format(PyObject *format, PyObject *args)

   新たな文字列オブジェクトを *format* および *args* から生成して返します; このメソッドは ``format % args``
   のようなものです。引数 *args* はタプルでなくてはなりません。


.. c:function:: int PyUnicode_Contains(PyObject *container, PyObject *element)

   *element* が *container* 内にあるか調べ、その結果に応じて真または偽を返します。

   *element* は単要素の Unicode 文字に型強制できなければなりません。
   エラーが生じた場合には ``-1`` を返します。

