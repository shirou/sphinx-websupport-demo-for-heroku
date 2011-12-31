.. highlightlang:: c

.. _stringobjects:

文字列/バイトオブジェクト
-------------------------

以下の関数では、文字列が渡されるはずのパラメタに非文字列が渡された場合に :exc:`TypeError` を送出します。

.. note::

   これらの関数群は Python 3.x では PyBytes_* へリネームされます。
   移植を容易にするために、特に注釈されていない限り、 3.x で利用できる PyBytes 関数群は
   同等の PyString_* 関数へのエイリアスにされています。

.. index:: object: string


.. c:type:: PyStringObject

   この :c:type:`PyObject` のサブタイプは Python の文字列オブジェクトを表現します。


.. c:var:: PyTypeObject PyString_Type

   .. index:: single: StringType (in module types)

   この :c:type:`PyTypeObject` のインスタンスは Python の文字列型を表現します; このオブジェクトは Python レイヤにおける
   ``str`` や ``types.StringType`` と同じです。 .


.. c:function:: int PyString_Check(PyObject *o)

   *o* が文字列型か文字列型のサブタイプであるときに真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyString_CheckExact(PyObject *o)

   *o* が文字列型で、かつ文字列型のサブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyString_FromString(const char *v)

   *v* を値に持つ文字列オブジェクトを返します。失敗すると *NULL* を返します。パラメタ *v* は *NULL* であってはなりません;
   *NULL* かどうかはチェックしません。


.. c:function:: PyObject* PyString_FromStringAndSize(const char *v, Py_ssize_t len)

   値が *v* で長さが *len* の新たな文字列オブジェクトを返します。失敗すると *NULL* を返します。 *v* が *NULL*
   の場合、文字列の中身は未初期化の状態になります。

   .. versionchanged:: 2.5
      この関数は以前は *len* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyString_FromFormat(const char *format, ...)

   C 関数 :c:func:`printf` 形式の *format* 文字列と可変個の引数をとり、書式化済みの文字列長を計算した上で、書式化を行った結果を
   値とする Python 文字列にして返します。可変個の引数部は C のデータ型でなくてはならず、かつ *format* 文字列内の書式指定文字 (format
   character) に一致する型でなくてはなりません。利用できる書式化文字は以下の通りです:

   +--------------+---------------+----------------------------------------------+
   | 書式指定文字 | 型            | コメント                                     |
   +==============+===============+==============================================+
   | :attr:`%%`   | *n/a*         | 文字 % のリテラル。                          |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%c`   | int           | C の整数型で表現される単一の文字。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%d`   | int           | C の ``printf("%d")`` と全く同じ。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%u`   | unsigned int  | C の ``printf("%u")`` と全く同じ。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%ld`  | long          | C の ``printf("%ld")`` と全く同じ。          |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%lu`  | unsigned long | C の ``printf("%lu")`` と全く同じ。          |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%lld` | long long     | C の ``printf("%lld")`` と全く同じ。         |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%llu` | unsigned      | C の ``printf("%llu")`` と全く同じ。         |
   |              | long long     |                                              |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%zd`  | Py_ssize_t    | C の ``printf("%zd")`` と全く同じ。          |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%zu`  | size_t        | C の ``printf("%zu")`` と全く同じ。          |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%i`   | int           | C の ``printf("%i")`` と全く同じ。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%x`   | int           | C の ``printf("%x")`` と全く同じ。           |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%s`   | char\*        | null で終端された C の文字列。               |
   +--------------+---------------+----------------------------------------------+
   | :attr:`%p`   | void\*        | C ポインタの 16                              |
   |              |               | 進表記。 ``printf("%p")``                    |
   |              |               | とほとんど同じだが、プラットフォームにおける |
   |              |               | ``printf`` の定義に関わりなく先頭にリテラル  |
   |              |               | ``0x`` が付きます。                          |
   +--------------+---------------+----------------------------------------------+

   識別できない書式指定文字があった場合、残りの書式文字列はそのまま出力文字列にコピーされ、残りの引数は無視されます。

   .. note::

      `"%lld"` と `"%llu"` 書式指定文字は :const:`HAVE_LONG_LONG`
      が定義されている時だけ利用できます。

   .. versionchanged:: 2.7
      `"%lld"` と `"%llu"` のサポートが追加されました。


.. c:function:: PyObject* PyString_FromFormatV(const char *format, va_list vargs)

   :c:func:`PyString_FromFormat` と同じです。ただし、こちらの関数は二つしか引数をとりません。


.. c:function:: Py_ssize_t PyString_Size(PyObject *string)

   文字列オブジェクト *string* 内の文字列値の長さを返します。

   .. versionchanged:: 2.5
      この関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: Py_ssize_t PyString_GET_SIZE(PyObject *string)

   :c:func:`PyString_Size` をマクロで実装したもので、エラーチェックを行いません。

   .. versionchanged:: 2.5
      この関数は以前は :c:type:`int` を返していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: char* PyString_AsString(PyObject *string)

   *string* の中身を NUL 文字終端された表現で返します。ポインタは *string* オブジェクトの内部バッファを指し、
   バッファのコピーを指すわけではありません。 ``PyString_FromStringAndSize(NULL, size)`` を使って
   生成した文字列でない限り、バッファ内のデータはいかなる変更もしてはなりません。この文字列をデアロケートしてはなりません。 *string* が Unicode
   オブジェクトの場合、この関数は *string* のデフォルトエンコーディング版を計算し、デフォルトエンコーディング版に対して操作を行います。
   *string* が文字列オブジェクトですらない場合、 :c:func:`PyString_AsString` は *NULL* を返して
   :exc:`TypeError` を送出します。


.. c:function:: char* PyString_AS_STRING(PyObject *string)

   :c:func:`PyString_AsString` をマクロで実装したもので、エラーチェックを行いません。文字列オブジェクトだけをサポートします;
   Unicode オブジェクトを渡してはなりません。


.. c:function:: int PyString_AsStringAndSize(PyObject *obj, char **buffer, Py_ssize_t *length)

   *obj* の中身を NUL 文字終端された表現にして、出力用の変数 *buffer* と *length* を使って返します。

   この関数は文字列オブジェクトと Unicode オブジェクトのどちらも入力として受理します。 Unicode オブジェクトの場合、オブジェクトを
   デフォルトエンコーディングでエンコードしたバージョン (default encoded version) を返します。 *length* が *NULL* の
   場合、値を返させるバッファには NUL 文字を入れてはなりません; NUL 文字が入っている場合、関数は ``-1`` を返し、
   :exc:`TypeError` を送出します。

   *buffer* は *obj* の内部文字列バッファを参照し、バッファのコピーを参照するわけではありません。
   ``PyString_FromStringAndSize(NULL, size)`` を使って生成した文字列でない限り、バッファ内のデータはいかなる変更も
   してはなりません。この文字列をデアロケートしてはなりません。

   *string* が Unicode オブジェクトの場合、この関数は *string* のデフォルトエンコーディング版を計算し、
   デフォルトエンコーディング版に対して操作を行います。 *string* が文字列オブジェクトですらない場合、
   :c:func:`PyString_AsStringAndSize` は ``-1`` を返して :exc:`TypeError` を送出します。

   .. versionchanged:: 2.5
      この関数は以前は *length* の型に :c:type:`int *` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: void PyString_Concat(PyObject **string, PyObject *newpart)

   新しい文字列オブジェクトを *\*string* に作成し、 *newpart* の内容を *string* に追加します; 呼び出し側は新たな参照を所有
   することになります。 *string* の以前の値に対する参照は盗み取られます。新たな文字列を生成できなければ、 *string* に対する古い参照は無視され、
   *\*string* の値は *NULL* に設定されます; その際、適切な例外情報が設定されます。


.. c:function:: void PyString_ConcatAndDel(PyObject **string, PyObject *newpart)

   新しい文字列オブジェクトを *\*string* に作成し、 *newpart* の内容を *string* に追加します。こちらのバージョンの関数は
   *newpart* への参照をデクリメントします。


.. c:function:: int _PyString_Resize(PyObject **string, Py_ssize_t newsize)

   "変更不能" である文字列オブジェクトをサイズ変更する手段です。新たな文字列オブジェクトを作成するときにのみ使用してください;
   文字列がすでにコードの他の部分で使われているかもしれない場合には、この関数を使ってはなりません。入力する文字列オブジェクトの参照カウントが 1
   でない場合、この関数を呼び出すとエラーになります。左側値には、既存の文字列オブジェクトのアドレスを渡し (このアドレスには
   書き込み操作が起きるかもしれません)、新たなサイズを指定します。成功した場合、 *\*string* はサイズ変更された文字列オブジェクトを
   保持し、 ``0`` が返されます; *\*string* の値は、入力したときの値と異なっているかもしれません。文字列の再アロケーションに失敗した場合、
   *\*string* に入っていた元の文字列オブジェクトを解放し、 *\*string* を *NULL* にセットし、メモリ例外をセットし、 ``-1``
   を返します。

   .. versionchanged:: 2.5
      この関数は以前は *newsize* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyString_Format(PyObject *format, PyObject *args)

   新たな文字列オブジェクトを  *format* と *args* から生成します。 ``format % args`` と似た働きです。引数 *args*
   はタプルでなければなりません。


.. c:function:: void PyString_InternInPlace(PyObject **string)

   引数 *\*string* をインプレースで隔離 (intern) します。引数は Python 文字列オブジェクトを指すポインタへのアドレスで
   なくてはなりません。 *\*string* と等しい、すでに隔離済みの文字列が存在する場合、そのオブジェクトを *\*string* に設定します
   (かつ、元の文字列オブジェクトの参照カウントをデクリメントし、すでに隔離済みの文字列オブジェクトの参照カウントをインクリメントします)。 (補足:
   参照カウントについては沢山説明して来ましtが、この関数は参照カウント中立 (reference-count-neutral) と考えてください;
   この関数では、関数の呼び出し後にオブジェクトに対して参照の所有権を持てるのは、関数を呼び出す前にすでに所有権を持っていた場合に限ります。)

   .. note::

      この関数は 3.x では利用できず、 PyBytes エイリアスもありません。

.. c:function:: PyObject* PyString_InternFromString(const char *v)

   :c:func:`PyString_FromString` と  :c:func:`PyString_InternInPlace` を組み合わせたもので、
   隔離済みの新たな文字列オブジェクトを返すか、同じ値を持つすでに隔離済みの文字列オブジェクトに対する新たな ("所有権を得た") 参照を返します。

   .. note::

      この関数は 3.x では利用できず、 PyBytes エイリアスもありません。

.. c:function:: PyObject* PyString_Decode(const char *s, Py_ssize_t size, const char *encoding, const char *errors)

   *size* からなるエンコード済みのバッファ *s* を *encoding* の名前で登録されている codec に
   渡してデコードし、オブジェクトを生成します。 *encoding* および *errors* は組み込み関数 :func:`unicode`
   に与える同名のパラメタと同じ意味を持ちます。使用する codec の検索は、 Python の codec レジストリを使って行います。codec
   が例外を送出した場合には *NULL* を返します。

   .. note::

      この関数は 3.x では利用できず、 PyBytes エイリアスもありません。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。


.. c:function:: PyObject* PyString_AsDecodedObject(PyObject *str, const char *encoding, const char *errors)

   文字列オブジェクトを *encoding* の名前で登録されている codec に渡してデコードし、Python オブジェクトを返します。 *encoding*
   および *errors* は文字列型の :meth:`encode` メソッドに与える同名のパラメタと同じ意味を持ちます。使用する codec の検索は、
   Python の codec レジストリを使って行います。codec が例外を送出した場合には *NULL* を返します。

   .. note::

      この関数は 3.x では利用できず、 PyBytes エイリアスもありません。

.. c:function:: PyObject* PyString_Encode(const char *s, Py_ssize_t size, const char *encoding, const char *errors)

   *size* で指定されたサイズの :c:type:`char` バッファを *encoding* の名前で登録されている codec に渡してエンコードし、
   Python オブジェクトを返します。 *encoding* および *errors* は文字列型の :meth:`encode`
   メソッドに与える同名のパラメタと同じ意味を持ちます。使用する codec の検索は、 Python の codec レジストリを使って行います。codec
   が例外を送出した場合には *NULL* を返します。

   .. note::

      この関数は 3.x では利用できず、 PyBytes エイリアスもありません。

   .. versionchanged:: 2.5
      この関数は以前は *size* の型に :c:type:`int` を利用していました。
      この変更により、 64bit システムを正しくサポートするには修正が必要になります。

.. c:function:: PyObject* PyString_AsEncodedObject(PyObject *str, const char *encoding, const char *errors)

   エンコード名 *encoding* で登録された codec を使って文字列オブジェクトをエンコードし、その結果を Python オブジェクト
   として返します。 *encoding* および *errors* は文字列型の :meth:`encode` メソッドに与える同名のパラメタと
   同じ意味を持ちます。使用する codec の検索は、 Python の codec レジストリを使って行います。codec が例外を送出した場合には
   *NULL* を返します。

   .. note::

      この関数は 3.x では利用できず、 PyBytes エイリアスもありません。
