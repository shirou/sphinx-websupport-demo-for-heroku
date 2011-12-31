.. highlightlang:: c

.. _string-conversion:

文字列の変換と書式化
================================

数値変換と、書式化文字列出力のための関数群


.. c:function:: int PyOS_snprintf(char *str, size_t size,  const char *format, ...)

   書式化文字列 *format* と追加の引数から、 *size* バイトを超えない文字列を
   *str* に出力します。
   Unix man page の :manpage:`snprintf(2)` を参照してください。


.. c:function:: int PyOS_vsnprintf(char *str, size_t size, const char *format, va_list va)

   書式化文字列 *format* と可変長引数リスト *va* から、 *size* バイトを超えない文字列を
   *str* に出力します。
   Unix man page の :manpage:`vsnprintf(2)` を参照してください。

:c:func:`PyOS_snprintf` と :c:func:`PyOS_vsnprintf` は標準Cライブラリの
:c:func:`snprintf` と :c:func:`vsnprintf` 関数をラップします。
これらの関数の目的は、C標準ライブラリが保証していないコーナーケースでの
動作を保証することです。

これらのラッパ関数は、戻るときに *str*[*size*-1] が常に ``'\0'`` であることを保証します。
(str の末尾の ``'\0'`` を含めて) *size* バイト以上を書き込みません。
``str != NULL``, ``size > 0``, ``format != NULL`` を要求します。


もし :c:func:`vsnprintf` のないプラットフォームで、切り捨てを避けるために必要な
バッファサイズが *size* を512バイトより大きく超過していれば、 Python は
*Py_FatalError* で abort します。

The return value (*rv*) for these functions should be interpreted as follows:
これらの関数の戻り値 (*rv*) は次のように解釈されなければなりません:

* ``0 <= rv < size`` のとき、変換出力は成功して、 (最後の *str*[*rv*] にある
  ``'\0'`` を除いて) *rv* 文字が *str* に出力された。

* ``rv >= size`` のとき、変換出力は切り詰められており、成功するためには ``rv + 1``
  バイトが必要だったことを示します。 *str*[*size*-1] は ``'\0'`` です。

* ``rv < 0`` のときは、何か悪いことが起こった時です。この場合でも *str*[*size*-1]
  は ``'\0'`` ですが、 *str* のそれ以外の部分は未定義です。エラーの正確な原因は
  プラットフォーム依存です。

以下の関数は locale 非依存な文字列から数値への変換を行ないます。


.. c:function:: double PyOS_string_to_double(const char *s, char **endptr, PyObject *overflow_exception)

   文字列 ``s`` を :c:type:`double` に変換します。失敗したときは Python の例外を発生させます。
   受け入れられる文字列は、 Python の :func:`float` コンストラクタが受け付ける文字列に準拠しますが、
   ``s`` の先頭と末尾に空白文字があってはならないという部分が異なります。
   この変換は現在のロケールに依存しません。

   ``endptr`` が ``NULL`` の場合、変換は文字列全体に対して行われます。
   文字列が正しい浮動小数点数の表現になっていない場合は ``-1.0`` を返して
   ValueError を発生させます。

   endptr が ``NULL`` で無い場合、文字列を可能な範囲で変換して、 ``*endptr``
   に最初の変換されなかった文字へのポインタを格納します。
   文字列の先頭に正しい浮動小数点数の表現が無かった場合、
   ``*endptr`` を文字列の先頭に設定して、 ValueError を発生させ、
   ``-1.0`` を返します。

   ``s`` が float に格納し切れないほど大きい値を表現していた場合、
   (例えば、 ``"1e500"`` は多くのプラットフォームで表現できません)
   ``overflow_exception`` が ``NULL`` なら ``Py_HUGE_VAL`` に適切な符号を
   付けて返します。他の場合は ``overflow_exception`` は Python
   の例外オブジェクトへのポインタでなければならず、その例外を発生させて
   ``-1.0`` を返します。
   どちらの場合でも、 ``*endptr`` には変換された値の直後の最初の文字への
   ポインタが設定されます。

   それ以外のエラーが変換中に発生した場合(例えば out-of-memory エラー)、
   適切な Python の例外を設定して ``-1.0`` を返します。

   .. versionadded:: 2.7


.. c:function:: double PyOS_ascii_strtod(const char *nptr, char **endptr)

   文字列を :c:type:`double` へ変換します。
   この関数は、C locale におけるC標準の :c:func:`strtod` と同じように動作します。
   スレッドセーフのために、この関数は現在の locale を変更せずに実装されています。

   :c:func:`PyOS_ascii_strtod` は通常、設定ファイルを読み込むときや、ロケール独立な
   非ユーザーからの入力を読み込むときに使われるべきです。

   詳細は Unix man page の :manpage:`strtod(2)` を参照してください。

   .. versionadded:: 2.4

   .. deprecated:: 2.7
      代わりに :c:func:`PyOS_string_to_double` を使ってください。


.. c:function:: char* PyOS_ascii_formatd(char *buffer, size_t buf_len, const char *format, double d)

   :c:type:`double` を ``'.'`` を小数点記号に利用して文字列に変換します。
   *format* は数値のフォーマットを指定する :c:func:`printf` スタイルの文字列です。
   利用できる変換文字は ``'e'``, ``'E'``, ``'f'``, ``'F'``, ``'g'``, ``'G'`` です。

   戻り値は、変換された文字列が格納された *buffer* へのポインタか、失敗した場合は NULL です。

   .. versionadded:: 2.4
   .. deprecated:: 2.7
      この関数は Python 2.7 と 3.1 では削除されました。
      代わりに :func:`PyOS_double_to_string` を使ってください。


.. c:function:: char* PyOS_double_to_string(double val, char format_code, int precision, int flags, int *ptype)

   :c:type:`double` *val* を指定された *format_code*, *precision*, *flags* に基づいて文字列に変換します。

   *format_code* は ``'e'``, ``'E'``, ``'f'``, ``'F'``, ``'g'``, ``'G'``, ``'r'``
   のどれかでなければなりません。
   ``'r'`` の場合、 *precision* は 0 でなければならず、無視されます。
   ``'r'`` フォーマットコードは標準の :func:`repr` フォーマットを指定しています。

   *flags* は 0 か、 *Py_DTSF_SIGN*, *Py_DTSF_ADD_DOT_0*, *Py_DTSF_ALT* か
   これらの or を取ったものです。

   * *Py_DTSF_SIGN* は、 *val* が負で無いときも常に符号文字を先頭につけることを意味します。

   * *Py_DTSF_ADD_DOT_0* は文字列が整数のように見えないことを保証します。

   * *Py_DTSF_ALT* は "alternate" フォーマットルールを適用することを意味します。
     詳細は :c:func:`PyOS_snprintf` の ``'#'`` 指定を参照してください。

   *ptype* が NULL で無い場合、 *val* が有限数、無限数、NaNのどれかに合わせて、
   *Py_DTST_FINITE*, *Py_DTST_INFINITE*, *Py_DTST_NAN* のいずれかに設定されます。

   戻り値は変換後の文字列が格納された *buffer* へのポインタか、変換が失敗した場合は *NULL* です。
   呼び出し側は、返された文字列を :c:func:`PyMem_Free` を使って解放する責任があります。

   .. versionadded:: 2.7


.. c:function:: double PyOS_ascii_atof(const char *nptr)

   文字列を、 locale 非依存な方法で :c:type:`double` へ変換します。

   詳細は Unix man page の :manpage:`atof(2)` を参照してください。

   .. versionadded:: 2.4

   .. deprecated:: 3.1
      代わりに :c:func:`PyOS_string_to_double` を使ってください。

.. c:function:: char* PyOS_stricmp(char *s1, char *s2)

   大文字/小文字を区別しない文字列比較。
   大文字/小文字を無視する以外は、 :c:func:`strcmp` と同じ動作をします。

   .. versionadded:: 2.6


.. c:function:: char* PyOS_strnicmp(char *s1, char *s2, Py_ssize_t  size)

   大文字/小文字を区別しない文字列比較。
   大文字/小文字を無視する以外は、 :c:func:`strncmp` と同じ動作をします。

   .. versionadded:: 2.6
