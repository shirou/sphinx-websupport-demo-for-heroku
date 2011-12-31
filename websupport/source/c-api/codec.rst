.. _codec-registry:

.. Codec registry and support functions

codec レジストリとサポート関数
====================================

.. c:function:: int PyCodec_Register(PyObject *search_function)

   新しい codec 検索関数を登録します。

   副作用として、この関数は :mod:`encodings` パッケージが常に検索関数の先頭に来るように、
   まだロードされていない場合はロードします。

.. c:function:: int PyCodec_KnownEncoding(const char *encoding)

   *encoding* のための登録された codec が存在するかどうかに応じて ``1`` か ``0`` を返します。

.. c:function:: PyObject* PyCodec_Encode(PyObject *object, const char *encoding, const char *errors)

   汎用の codec ベースの encode API.

   *encoding* に応じて見つかったエンコーダ関数に対して *object* を渡します。
   エラーハンドリングメソッドは *errors* で指定します。
   *errors* は *NULL* でもよく、その場合はその codec のデフォルトのメソッドが利用されます。
   エンコーダが見つからなかった場合は :exc:`LookupError` を発生させます。

.. c:function:: PyObject* PyCodec_Decode(PyObject *object, const char *encoding, const char *errors)

   汎用の codec ベースの dencode API.

   *encoding* に応じて見つかったデコーダ関数に対して *object* を渡します。
   エラーハンドリングメソッドは *errors* で指定します。
   *errors* は *NULL* でもよく、その場合はその codec のデフォルトのメソッドが利用されます。
   デコーダが見つからなかった場合は :exc:`LookupError` を発生させます。


.. Codec lookup API

コーデック検索API
------------------

以下の関数では、文字列 *encoding* は全て小文字に変換することで、効率的に、大文字小文字を
無視した検索をします。
コーデックが見つからない場合、 :exc:`KeyError` を設定して *NULL* を返します。

.. c:function:: PyObject* PyCodec_Encoder(const char *encoding)

   *encoding* のエンコーダ関数を返します。

.. c:function:: PyObject* PyCodec_Decoder(const char *encoding)

   *encoding* のデコーダ関数を返します。

.. c:function:: PyObject* PyCodec_IncrementalEncoder(const char *encoding, const char *errors)

   *encoding* の :class:`IncrementalEncoder` オブジェクトを返します。

.. c:function:: PyObject* PyCodec_IncrementalDecoder(const char *encoding, const char *errors)

   *encoding* の :class:`IncrementalDecoder` オブジェクトを返します。

.. c:function:: PyObject* PyCodec_StreamReader(const char *encoding, PyObject *stream, const char *errors)

   *encoding* の :class:`StreamReader` ファクトリ関数を返します。

.. c:function:: PyObject* PyCodec_StreamWriter(const char *encoding, PyObject *stream, const char *errors)

   *encoding* の :class:`StreamWriter` ファクトリ関数を返します。


.. Registry API for Unicode encoding error handlers

Unicode エラーハンドラ用レジストリ API
------------------------------------------------

.. c:function:: int PyCodec_RegisterError(const char *name, PyObject *error)

   エラーハンドルのためのコールバック関数 *error* を *name* で登録します。
   このコールバック関数は、コーデックがエンコードできない文字/デコードできないバイトに
   遭遇した時に、そのエンコード/デコード関数の呼び出しで *name* が指定されていたら
   呼び出されます。

   コールバックは1つの引数として、 :exc:`UnicodeEncodeError`, :exc:`UnicodeDecodeError`,
   :exc:`UnicodeTranslateError` のどれかのインスタンスを受け取ります。
   このインスタンスは問題のある文字列やバイト列に関する情報と、その元の文字列中の
   オフセットを持っています。(その情報を取得するための関数については
   :ref:`unicodeexceptions` を参照してください。)
   コールバックは渡された例外を発生させるか、2要素のタプルに問題のシーケンスの代替と、
   encode/decode を再開する元の文字列中のオフセットとなる整数を格納して返します。

   成功したら ``0`` を、エラー時は ``-1`` を返します。

.. c:function:: PyObject* PyCodec_LookupError(const char *name)

   *name* で登録されたエラーハンドリングコールバック関数を検索します。
   特別な場合として、 *NULL* が渡された場合、 "strict" のエラーハンドリングコールバック
   関数を返します。

.. c:function:: PyObject* PyCodec_StrictErrors(PyObject *exc)

   *exc* を例外として発生させます。

.. c:function:: PyObject* PyCodec_IgnoreErrors(PyObject *exc)

   unicode エラーを無視し、問題の入力をスキップします。

.. c:function:: PyObject* PyCodec_ReplaceErrors(PyObject *exc)

   unicode エラーを ``?`` か ``U+FFFD`` で置き換えます。

.. c:function:: PyObject* PyCodec_XMLCharRefReplaceErrors(PyObject *exc)

   unicode encode エラーを XML文字参照で置き換えます。

.. c:function:: PyObject* PyCodec_BackslashReplaceErrors(PyObject *exc)

   unicode encode エラーをバックスラッシュエスケープ (``\x``, ``\u``, ``\U``)
   で置き換えます。

