.. todo

   ``?`` がある行以外での「〜型」の型を削除

.. highlightlang:: c

.. _arg-parsing:

引数の解釈と値の構築
====================

これらの関数は独自の拡張モジュール用の関数やメソッドを作成する際に便利です。
詳しい情報や用例は :ref:`extending-index` にあります。

最初に説明する 3 つの関数、 :c:func:`PyArg_ParseTuple`,
:c:func:`PyArg_ParseTupleAndKeywords`,および :c:func:`PyArg_Parse` はいずれも
*書式化文字列 (format string)* を使います。
書式化文字列は、関数が受け取るはずの引数に関する情報を伝えるのに用いられます。
いずれの関数における書式化文字列も、同じ書式を使っています。

書式化文字列は、ゼロ個またはそれ以上の "書式化単位 (format unit)" から成り立ちます。
1つの書式化単位は1つの Python オブジェクトを表します;
通常は単一の文字か、書式化単位からなる文字列を括弧で囲ったものになります。例外として、括弧で囲われていない
書式化単位文字列が単一のアドレス引数に対応する場合がいくつかあります。
以下の説明では、引用符のついた形式は書式化単位です;
(丸)括弧で囲った部分は書式化単位に対応する Python のオブジェクト型です; [角] 括弧は値をアドレス渡しする際に使う C の変数型です。

``s`` (文字列型または Unicode 型) [const char \*]
   Python の文字列または Unicode オブジェクトを、キャラクタ文字列を指す C のポインタに変換します。
   変換先の文字列自体の記憶領域を提供する必要はありません; キャラクタ型ポインタ変数のアドレスを渡すと、すでに存在している
   文字列へのポインタをその変数に記録します。C 文字列は NUL で終端されています。Python の文字列型は、NUL バイトが途中に埋め込まれて
   いてはなりません; もし埋め込まれていれば :exc:`TypeError` 例外を送出します。Unicode オブジェクトはデフォルトエンコーディングを使って
   C 文字列に変換されます。変換に失敗すると :exc:`UnicodeError` を送出します。

``s#`` (文字列型、Unicode 型または任意の読み出しバッファ互換型) [const char \*, int (または :c:type:`Py_ssize_t`, 下記参照)]
   これは ``s`` の変化形で、値を二つの変数に記録します。一つ目の変数はキャラクタ文字列へのポインタで、二つ目はその長さです。
   この書式化単位の場合には、Python 文字列に null バイトが埋め込まれていてもかまいません。 Unicode オブジェクトの場合、デフォルト
   エンコーディングでの変換が可能ならば、変換したオブジェクトから文字列へのポインタを返します。その他の読み出しバッファ互換オブジェクトは
   生の内部データ表現への参照を返します。

   Python 2.5 から、長さの引数の型を、 :file:`Python.h` を include する前に
   :c:macro:`PY_SSIZE_T_CLEAN` マクロ を定義することで制御できるようになりました。
   もしこのマクロが定義されていた場合、長さは int ではなく :c:type:`Py_ssize_t`
   になります。

``s*`` (文字列型、Unicode 型、または任意のバッファー互換オブジェクト) [Py_buffer]
   ``s#`` と似ていますが、呼び出し元から渡された Py_buffer 構造体に書き込みます。
   バッファーはロックされるので、呼び出し元はそのバッファーを ``Py_BEGIN_ALLOW_THREADS``
   したブロック内でさえも利用することができます。その代わり、呼び出し元には、
   データを処理した後にその構造体に対して ``PyBuffer_Release`` する責任があります。

   .. versionadded:: 2.6

``z`` (文字列型、Unicode 型 または ``None``) [const char \*]
   ``s`` に似ていますが、Python オブジェクトは ``None`` でもよく、
   その場合には C のポインタは *NULL* にセットされます。

``z#`` (文字列型、 ``None`` 、または任意の読み出しバッファ互換型) [const char \*, int]
   ``s#`` の ``s`` を ``z`` にしたような意味です。

``z*`` (文字列型、Unicode型、 ``None`` または任意のバッファー互換型) [Py_buffer]
   ``s*`` の ``s`` を ``z`` にしたような意味です。

   .. versionadded:: 2.6

``u`` (Unicode 型) [Py_UNICODE \*]
   Python の Unicode オブジェクトを、NUL で終端された 16 ビットの Unicode (UTF-16) データに変換します。 ``s``
   と同様に、 Unicode データバッファ用に記憶領域を提供する必要はありません; :c:type:`Py_UNICODE`
   型ポインタ変数のアドレスを渡すと、すでに存在している Unicode データへのポインタをその変数に記録します。

``u#`` (Unicode 型) [Py_UNICODE \*, int]
   これは ``u`` の変化形で、値を二つの変数に記録します。一つ目の変数は Unicode データバッファへのポインタで、二つ目はその長さです。非
   Unicode のオブジェクトの場合、読み出しバッファのポインタを :c:type:`Py_UNICODE` 型シーケンスへのポインタと解釈して扱います。

``es`` (文字列型、Unicode 型または任意の読み出しバッファ互換型)[const char \*encoding, char \*\*buffer]
   これは ``s`` の変化形で、Unicode オブジェクトや Unicode に変換可能なオブジェクトをキャラクタ型バッファにエンコードするために
   用いられます。NUL バイトが埋め込まれていない文字列でのみ動作します。

   この書式化単位には二つの引数が必要です。一つ目は入力にのみ用いられ、 NUL で終端されたエンコード名文字列を指す :c:type:`const char\*`
   型でなければなりません。指定したエンコード名を Python が理解できない場合には例外を送出します。第二の引数は :c:type:`char\*\*`
   でなければなりません; この引数が参照しているポインタの値は、引数に指定したテキストの内容が入ったバッファへのポインタになります。
   テキストは最初の引数に指定したエンコード方式でエンコードされます。

   :c:func:`PyArg_ParseTuple` を使うと、必要なサイズのバッファを確保し、そのバッファにエンコード後のデータをコピーして、
   *\*buffer* がこの新たに確保された記憶領域を指すように変更します。呼び出し側には、確保されたバッファを使い終わった後に
   :c:func:`PyMem_Free` で解放する責任があります。

``et`` (文字列型、Unicode 型または文字列バッファ互換型) [const char \*encoding, char \*\*buffer]
   ``es`` と同じです。ただし、8 ビット幅の文字列オブジェクトをエンコードし直さずに渡します。その代わり、実装では文字列オブジェクトが
   パラメタに渡したエンコードを使っているものと仮定します。

``es#`` (文字列型、Unicode 型または文字列バッファ互換型) [const char \*encoding, char \*\*buffer, int \*buffer_length]
   ``s#`` の変化形で、Unicode オブジェクトや Unicode に変換可能なオブジェクトをキャラクタ型バッファにエンコードするために
   用いられます。 ``es`` 書式化単位と違って、この変化形はバイトが埋め込まれていてもかまいません。

   この書式化単位には三つの引数が必要です。一つ目は入力にのみ用いられ、 NUL で終端されたエンコード名文字列を指す :c:type:`const char\*`
   型か *NULL* でなければなりません。 *NULL* の場合にはデフォルトエンコーディングを使います。指定したエンコード名を Python が理解できない
   場合には例外を送出します。第二の引数は :c:type:`char\*\*` でなければなりません; この引数が参照しているポインタの値は、引数に指定した
   テキストの内容が入ったバッファへのポインタになります。テキストは最初の引数に指定したエンコード方式でエンコードされます。
   第三の引数は整数へのポインタでなければなりません; ポインタが参照している整数の値は出力バッファ内のバイト数にセットされます。

   この書式化単位の処理には二つのモードがあります:

   *\*buffer* が *NULL* ポインタを指している場合、関数は必要なサイズのバッファを確保し、そのバッファにエンコード後の
   データをコピーして、 *\*buffer* がこの新たに確保された記憶領域を指すように変更します。呼び出し側には、確保されたバッファを使い終わった後に
   :c:func:`PyMem_Free` で解放する責任があります。

   *\*buffer* が非 *NULL* のポインタ (すでにメモリ確保済みのバッファ) を指している場合、 :c:func:`PyArg_ParseTuple`
   はこのメモリ位置をバッファとして用い、 *\*buffer_length*
   の初期値をバッファサイズとして用います。 :c:func:`PyArg_ParseTuple` は次にエンコード済みのデータをバッファにコピーして、NUL で終端
   します。バッファの大きさが足りなければ :exc:`ValueError`  がセットされます。

   どちらの場合も、 *\*buffer_length* は終端の NUL バイトを含まないエンコード済みデータの長さにセットされます。

``et#`` (文字列型、Unicode 型または文字列バッファ互換型) [const char \*encoding, char \*\*buffer, int \*buffer_length]
   ``es#`` と同じです。ただし、文字列オブジェクトをエンコードし直さずに渡します。その代わり、実装では文字列オブジェクトが
   パラメタに渡したエンコードを使っているものと仮定します。

``b`` (整数型) [unsigned char]
   Python の非負の整数を、 C の :c:type:`unsigned char` 型の小さな符号無し整数に変換します。

``B`` (整数型) [unsigned char]
   Python の整数を、オーバフローチェックを行わずに、 C の  :c:type:`unsigned char` 型の小さな整数に変換します。

   .. versionadded:: 2.3

``h`` (整数型) [short int]
   Python の整数を、 C の :c:type:`short int` 型に変換します。

``H`` (整数型) [unsigned short int]
   Python の整数を、オーバフローチェックを行わずに、 C の  :c:type:`unsigned short int` 型に変換します。

   .. versionadded:: 2.3

``i`` (整数型) [int]
   Python の整数を、 C の :c:type:`int` 型に変換します。

``I`` (整数型) [unsigned int]
   Python の整数を、オーバフローチェックを行わずに、 C の  :c:type:`unsigned int` 型に変換します。

   .. versionadded:: 2.3

``l`` (整数型) [long int]
   Python の整数を、 C の :c:type:`long int` 型に変換します。

``k`` (整数型) [unsigned long]
   Python の整数もしくは長整数を、オーバフローチェックを行わずに、 C の  :c:type:`unsigned long int` 型に変換します。

   .. versionadded:: 2.3

``L`` (整数型) [PY_LONG_LONG]
   Python の整数を、 C の :c:type:`long long` 型に変換します。この書式化単位は、 :c:type:`long long` 型 (または
   Windows の  :c:type:`_int64` 型) がサポートされているプラットフォームでのみ利用できます。

``K`` (整数型) [unsigned PY_LONG_LONG]
   Python の整数もしくは長整数を、オーバフローチェックを行わずに、 C の  :c:type:`unsigned long long` 型に変換します。
   この書式化単位は、 :c:type:`unsigned long long` 型 (または Windows の  :c:type:`unsigned _int64`
   型) がサポートされているプラットフォームでのみ利用できます。

   .. versionadded:: 2.3

``n`` (整数型) [Py_ssize_t]
   Python の整数もしくは長整数をCの :c:type:`Py_ssize_t` 型に変換します。

   .. versionadded:: 2.5

``c`` (長さ 1 の文字列型) [char]
   長さ 1 の文字列として表現されている Python キャラクタを C の :c:type:`char` 型に変換します。

``f`` (浮動小数点型) [float]
   Python の浮動小数点型を、 C の :c:type:`float` 型に変換します。

``d`` (浮動小数点型) [double]
   Python の浮動小数点型を、 C の :c:type:`double` 型に変換します。

``D`` (複素数型) [Py_complex]
   Python の複素数型を、 C の :c:type:`Py_complex` 構造体に変換します。

``O`` (オブジェクト) [PyObject \*]
   Python オブジェクトを (一切変換を行わずに) C の Python オブジェクト型ポインタに保存します。これにより、C
   プログラムは実際のオブジェクトを受け渡しされます。オブジェクトの参照カウントは増加しません。保存されるポインタが *NULL* になることはありません。

``O!`` (オブジェクト) [*typeobject*, PyObject \*]
   Python オブジェクトを C の Python オブジェクト型ポインタに保存します。 ``O`` に似ていますが、二つの C の引数をとります:
   一つ目の引数は Python の型オブジェクトへのアドレスで、二つ目の引数はオブジェクトへのポインタが保存されている (:c:type:`PyObject\*`
   の) C の変数へのアドレスです。Python オブジェクトが指定した型ではない場合、 :exc:`TypeError` を送出します。

``O&`` (オブジェクト) [*converter*, *anything*]
   Python オブジェクトを *converter* 関数を介して C の変数に変換します。二つの引数をとります: 一つ目は関数で、二つ目は (任意の型の)
   C 変数へのアドレスを :c:type:`void \*` 型に変換したものです。 *converter* は以下のようにして呼び出されます::

      status = converter(object, address);

   ここで *object* は変換対象の Python オブジェクトで、 *address* は :c:func:`PyArg_Parse\*` に渡した
   :c:type:`void\*`  型の引数です。戻り値 *status* は変換に成功した際に ``1``,失敗した場合には ``0``
   になります。変換に失敗した場合、 *converter* 関数は *address* の内容を変更せずに例外を送出しなくてはなりません。

``S`` (文字列型) [PyStringObject \*]
   ``O`` に似ていますが、Python オブジェクトは文字列オブジェクトでなければなりません。
   オブジェクトが文字列オブジェクトでない場合には :exc:`TypeError` を送出します。 C 変数は :c:type:`PyObject\*`
   で宣言しておいてもかまいません。

``U`` (Unicode 型) [PyUnicodeObject \*]
   ``O`` に似ていますが、Python オブジェクトは Unicode オブジェクトでなければなりません。オブジェクトが Unicode
   オブジェクトでない場合には :exc:`TypeError` を送出します。 C 変数は :c:type:`PyObject\*` で宣言しておいてもかまいません。

``t#`` (読み出し専用キャラクタバッファ) [char \*, int]
   ``s#`` に似ていますが、読み出し専用バッファインタフェースを実装している任意のオブジェクトを受理します。 :c:type:`char\*`
   変数はバッファの最初のバイトを指すようにセットされ、 :c:type:`int` はバッファの長さにセットされます。
   単一セグメントからなるバッファオブジェクトだけを受理します; それ以外の場合には :exc:`TypeError` を送出します。

``w`` (読み書き可能なキャラクタバッファ) [char \*]
   ``s`` と同様ですが、読み書き可能なバッファインタフェースを実装している任意のオブジェクトを受理します。
   呼び出し側は何らかの別の手段でバッファの長さを決定するか、あるいは ``w#`` を使わねばなりません。
   単一セグメントからなるバッファオブジェクトだけを受理します; それ以外の場合には :exc:`TypeError` を送出します。

``w#`` (読み書き可能なキャラクタバッファ) [char \*, Py_ssize_t]
   ``s#`` に似ていますが、読み書き可能なバッファインタフェースを実装している任意のオブジェクトを受理します。 :c:type:`char\*`
   変数はバッファの最初のバイトを指すようにセットされ、 :c:type:`Py_ssize_t` はバッファの長さにセットされます。
   単一セグメントからなるバッファオブジェクトだけを受理します; それ以外の場合には :exc:`TypeError` を送出します。

``w*`` (読み書きできるバイト列バッファ) [Py_buffer]
   ``s`` に対する ``s*`` と同じ、 ``w`` のバージョンです。

   .. versionadded:: 2.6

``(items)`` (タプル) [*matching-items*]
   オブジェクトは *items* に入っている書式化単位の数だけの長さを持つ Python のシーケンス型でなくてはなりません。各 C 引数は *items* 内の
   個々の書式化単位に対応づけできねばなりません。シーケンスの書式化単位は入れ子構造にできます。

   .. note::

      Python のバージョン 1.5.2 より以前は、この書式化指定文字列はパラメタ列ではなく、個別のパラメタが入ったタプルでなければなりません
      でした。このため、以前は :exc:`TypeError` を引き起こしていたようなコードが現在は例外を出さずに処理されるかもしれません。
      とはいえ、既存のコードにとってこれは問題ないと思われます。

Python 整数型を要求している場所に Python 長整数型を渡すのは可能です; しかしながら、適切な値域チェックはまったく行われません ---
値を受け取るためのフィールドが、値全てを受け取るには小さすぎる場合、上桁のビット群は暗黙のうちに切り詰められます (実際のところ、このセマンティクスは C
のダウンキャスト (downcast) から継承しています --- その恩恵は人それぞれかもしれませんが)。

その他、書式化文字列において意味を持つ文字がいくつかあります。それらの文字は括弧による入れ子内には使えません。以下に文字を示します:

``|``
   Python 引数リスト中で、この文字以降の引数がオプションであることを示します。オプションの引数に対応する C の変数はデフォルトの値で初期化して
   おかねばなりません --- オプションの引数が省略された場合、 :c:func:`PyArg_ParseTuple` は対応する C 変数の内容に
   手を加えません。

``:``
   この文字があると、書式化単位の記述はそこで終わります; コロン以降の文字列は、エラーメッセージにおける関数名
   (:c:func:`PyArg_ParseTuple` が送出する例外の "付属値 (associated value)") として使われます。

``;``
   この文字があると、書式化単位の記述はそこで終わります; セミコロン以降の文字列は、デフォルトエラーメッセージを *置き換える*
   エラーメッセージとして使われます。 ``:`` と ``;`` は相互に排他の文字です。

呼び出し側に提供される Python オブジェクトの参照は全て *借りた (borrowed)* ものです; オブジェクトの参照カウントを
デクリメントしてはなりません!

以下の関数に渡す補助引数 (additional argument) は、書式化文字列から決定される型へのアドレスでなければなりません; 補助引数に指定した
アドレスは、タプルから入力された値を保存するために使います。上の書式化単位のリストで説明したように、補助引数を入力値として使う場合がいくつかあります;
その場合、対応する書式化単位の指定する形式に従うようにせねばなりません。

変換を正しく行うためには、 *arg* オブジェクトは書式化文字に一致しなければならず、かつ書式化文字列内の書式化単位に全て値が入るようにせねばなりません。
成功すると、 :c:func:`PyArg_Parse\*` 関数は真を返します。それ以外の場合には偽を返し、適切な例外を送出します。
書式化単位のどれかの変換失敗により :c:func:`PyArg_Parse\*` が失敗した場合、
失敗した書式化単位に対応するアドレスとそれ以降のアドレスの内容は変更されません。


.. c:function:: int PyArg_ParseTuple(PyObject *args, const char *format, ...)

   固定引数のみを引数にとる関数のパラメタを解釈して、ローカルな変数に変換します。
   成功すると真を返します;失敗すると偽を返し、適切な例外を送出します。


.. c:function:: int PyArg_VaParse(PyObject *args, const char *format, va_list vargs)

   :c:func:`PyArg_ParseTuple` と同じですが、可変長の引数ではなく *va_list* を引数にとります。


.. c:function:: int PyArg_ParseTupleAndKeywords(PyObject *args, PyObject *kw, const char *format, char *keywords[], ...)

   固定引数およびキーワード引数をとる関数のパラメタを解釈して、ローカルな変数に変換します。
   成功すると真を返します;失敗すると偽を返し、適切な例外を送出します。


.. c:function:: int PyArg_VaParseTupleAndKeywords(PyObject *args, PyObject *kw, const char *format, char *keywords[], va_list vargs)

   :c:func:`PyArg_ParseTupleAndKeywords` と同じですが、可変長の引数ではなく *va_list* を引数にとります。


.. c:function:: int PyArg_Parse(PyObject *args, const char *format, ...)

   "旧スタイル" の関数における引数リストを分析するために使われる関数です --- 旧スタイルの関数は、引数解釈手法に
   :const:`METH_OLDARGS` を使います。新たに書かれるコードでのパラメタ解釈にはこの関数の使用は奨められず、
   標準のインタプリタにおけるほとんどのコードがもはや引数解釈のためにこの関数を使わないように変更済みです。
   この関数を残しているのは、この関数が依然として引数以外のタプルを分析する上で便利だからですが、この目的においては将来も使われつづけるかもしれません。


.. c:function:: int PyArg_UnpackTuple(PyObject *args, const char *name, Py_ssize_t min, Py_ssize_t max, ...)

   パラメータ取得を簡単にした形式で、引数の型を指定する書式化文字列を使いません。パラメタの取得にこの手法を使う関数は、関数宣言テーブル、またはメソッド
   宣言テーブル内で :const:`METH_VARARGS` として宣言しなくてはなりません。実引数の入ったタプルは *args* に渡します;
   このタプルは本当のタプルでなくてはなりません。タプルの長さは少なくとも *min* で、 *max* を超えてはなりません; *min* と *max*
   が等しくてもかまいません。補助引数を関数に渡さなくてはならず、各補助引数は :c:type:`PyObject\*`  変数へのポインタでなくてはなりません;
   これらの補助引数には、 *args* の値が入ります; 値の参照は借りた参照です。オプションのパラメタに対応する変数のうち、 *args* に指定していない
   ものには値が入りません; 呼び出し側はそれらの値を初期化しておかねばなりません。この関数は成功すると真を返し、 *args* がタプルでない場合や
   間違った数の要素が入っている場合に偽を返します; 何らかの失敗が起きた場合には例外をセットします。

   この関数の使用例を以下に示します。この例は、弱参照のための :mod:`_weakref` 補助モジュールのソースコードからとったものです::

      static PyObject *
      weakref_ref(PyObject *self, PyObject *args)
      {
          PyObject *object;
          PyObject *callback = NULL;
          PyObject *result = NULL;

          if (PyArg_UnpackTuple(args, "ref", 1, 2, &object, &callback)) {
              result = PyWeakref_NewRef(object, callback);
          }
          return result;
      }

   この例における :c:func:`PyArg_UnpackTuple` 呼び出しは、 :c:func:`PyArg_ParseTuple` を使った以下の呼び出し::

      PyArg_ParseTuple(args, "O|O:ref", &object, &callback)

   と全く等価です。

   .. versionadded:: 2.2

   .. versionchanged:: 2.5
      この関数は *min* と *max* に :c:type:`int` を利用していました。
      この変更により、64 bitシステムを正しくサポートするためには修正が必要になるでしょう。

.. c:function:: PyObject* Py_BuildValue(const char *format, ...)

   :c:func:`PyArg_Parse\*` ファミリの関数が受け取るのと似た形式の書式化文字列および値列に基づいて、新たな値を生成します。
   生成した値を返します。エラーの場合には *NULL* を返します; *NULL* を返す場合、例外を送出するでしょう。

   :c:func:`Py_BuildValue` は常にタプルを生成するとは限りません。この関数がタプルを生成するのは、書式化文字列に二つ以上の書式化単位
   が入っているときだけです。書式化文字列が空の場合、 ``None``  を返します; 書式化単位が厳密に一つだけ入っている場合、
   書式化単位で指定されている何らかのオブジェクト単体を返します。サイズがゼロや 1 のタプルを返すように強制するには、丸括弧で囲われた書式化文字列を使います。

   書式化単位 ``s`` や ``s#`` の場合のように、オブジェクトを構築する際にデータを供給するためにメモリバッファをパラメタとして渡す
   場合には、指定したデータはコピーされます。 :c:func:`Py_BuildValue` が生成したオブジェクトは、呼び出し側が提供したバッファを決して参照
   しません。別の言い方をすれば、 :c:func:`malloc` を呼び出してメモリを確保し、それを :c:func:`Py_BuildValue`
   に渡した場合、コード内で :c:func:`Py_BuildValue` が返った後で :c:func:`free` を呼び出す責任があるということです。

   以下の説明では、引用符のついた形式は書式化単位です; (丸)括弧で囲った部分は書式化単位が返す Python のオブジェクト型です; [角]
   括弧は関数に渡す値の C 変数型です。

   書式化文字列内では、(``s#`` のような書式化単位を除いて) スペース、タブ、コロンおよびコンマは無視されます。
   これらの文字を使うと、長い書式化文字列をちょっとだけ読みやすくできます。

   ``s`` (文字列型) [char \*]
      null 終端された C 文字列から Python オブジェクトに変換します。 C 文字列ポインタが *NULL* の場合、 ``None`` になります。

   ``s#`` (文字列型) [char \*, int]
      C 文字列とその長さから Python オブジェクトに変換します。 C 文字列ポインタが *NULL* の場合、長さは無視され ``None`` になります。

   ``z`` (文字列型または ``None``) [char \*]
      ``s`` と同じです。

   ``z#`` (文字列型または ``None``) [char \*, int]
      ``s#`` と同じです。

   ``u`` (Unicode 型) [Py_UNICODE \*]
      null 終端された Unicode (UCS-2 または UCS-4) データのバッファから Python オブジェクトに変換します。 Unicode
      バッファポインタが *NULL* の場合、 ``None`` になります。

   ``u#`` (Unicode 型) [Py_UNICODE \*, int]
      null 終端された Unicode (UCS-2 または UCS-4) データのバッファとその長さから Python オブジェクトに変換します。
      Unicode バッファポインタが *NULL* の場合、長さは無視され ``None`` になります。

   ``i`` (整数型) [int]
      通常の C の :c:type:`int` を Python の整数オブジェクトに変換します。

   ``b`` (整数型) [char]
      ``i`` と同じです。通常のC の :c:type:`char` を Python の整数オブジェクトに変換します。

   ``h`` (整数型) [short int]
      通常のC の :c:type:`short int` を Python の整数オブジェクトに変換します。

   ``l`` (整数型) [long int]
      C の :c:type:`long int` を Python の整数オブジェクトに変換します。

   ``B`` (整数型) [unsigned char]
      C の :c:type:`unsigned char` を Python の整数オブジェクトに変換します。

   ``H`` (整数型) [unsigned short int]
      C の :c:type:`unsigned short int` を Python の整数オブジェクトに変換します。

   ``I`` (整数型/長整数型) [unsigned int]
      C の :c:type:`unsigned int` を Python の整数オブジェクト、あるいは、値が ``sys.maxint``
      より大きければ長整数オブジェクトに変換します。

   ``k`` (整数型/長整数型) [unsigned long]
      C の :c:type:`unsigned long` を Python の整数オブジェクト、あるいは、値が ``sys.maxint``
      より大きければ長整数オブジェクトに変換します。

   ``L`` (長整数型) [PY_LONG_LONG]
      C の :c:type:`long long` を Python の長整数オブジェクトに変換します。 :c:type:`long long`
      をサポートしているプラットフォームでのみ利用可能です。

   ``K`` (長整数型) [unsigned PY_LONG_LONG]
      C の :c:type:`unsigned long long` を Python の長整数オブジェクトに変換します。 :c:type:`long long`
      をサポートしているプラットフォームでのみ利用可能です。

   ``n`` (長整数型) [Py_ssize_t]
      C の :c:type:`unsigned long` を Python の整数オブジェクト、あるいは長整数オブジェクトに変換します。

      .. versionadded:: 2.5

   ``c`` (長さ 1 の文字列型) [char]
      文字を表す通常の C の :c:type:`int` を、長さ 1 の Python の文字列オブジェクトに変換します。

   ``d`` (浮動小数点型) [double]
      C の :c:type:`double` を Python の浮動小数点数に変換します。

   ``f`` (浮動小数点型) [float]
      ``d`` と同じです。

   ``D`` (複素数型) [Py_complex \*]
      C の :c:type:`Py_complex` 構造体を Python の複素数に変換します。

   ``O`` (オブジェクト) [PyObject \*]
      Python オブジェクトを手を加えずに渡します (ただし、参照カウントは 1 インクリメントします)。渡したオブジェクトが *NULL* ポインタ
      の場合、この引数を生成するのに使った何らかの呼び出しがエラーになったのが原因であると仮定して、例外をセットします。従ってこのとき
      :c:func:`Py_BuildValue` は *NULL* を返しますが :c:func:`Py_BuildValue` 自体は例外を送出しません。
      例外をまだ送出していなければ :exc:`SystemError` をセットします。

   ``S`` (オブジェクト) [PyObject \*]
      ``O`` と同じです。

   ``N`` (オブジェクト) [PyObject \*]
      ``O`` と同じです。ただし、オブジェクトの参照カウントをインクリメントしません。オブジェクトが引数リスト内のオブジェクト
      コンストラクタ呼び出しによって生成されている場合に便利です。

   ``O&`` (オブジェクト) [*converter*, *anything*]
      *anything* を *converter* 関数を介して Python オブジェクトに変換します。この関数は *anything*
      (:c:type:`void \*` と互換の型でなければなりません) を引数にして呼び出され、"新たな" オブジェクトを返すか、失敗した場合には
      *NULL* を返すようにしなければなりません。

   ``(items)`` (タプル型) [*matching-items*]
      C の値からなる配列を、同じ要素数を持つ Python のタプルに変換します。

   ``[items]`` (リスト型) [*matching-items*]
      C の値からなる配列を、同じ要素数を持つ Python のリストに変換します。

   ``{items}`` (辞書型) [*matching-items*]
      C の値からなる配列を Python の辞書に変換します。一連のペアからなる C の値が、それぞれキーおよび値となって辞書に追加されます。

   書式化文字列に関するエラーが生じると、 :exc:`SystemError` 例外をセットして *NULL* を返します。

.. c:function:: PyObject* Py_VaBuildValue(const char *format, va_list vargs)

   :c:func:`Py_BuildValue` と同じですが、可変長引数の代わりに va_list を受け取ります。

