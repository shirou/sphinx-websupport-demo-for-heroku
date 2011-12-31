.. highlightlang:: c

.. _fileobjects:

ファイルオブジェクト
--------------------

.. index:: object: file

Python の組み込みファイルオブジェクトは、全て標準 C ライブラリの
:c:type:`FILE\*` サポートの上に実装されています。以下の詳細説明は
一実装に関するもので、将来の Python のリリースで変更されるかもしれません。


.. c:type:: PyFileObject

   この :c:type:`PyObject` のサブタイプは Python のファイル型オブジェクトを
   表現します。


.. c:var:: PyTypeObject PyFile_Type

   .. index:: single: FileType (in module types)

   この :c:type:`PyTypeObject` のインスタンスは Python のファイル型を表現します。
   このオブジェクトは ``file`` および ``types.FileType`` として Python
   プログラムで公開されています。


.. c:function:: int PyFile_Check(PyObject *p)

   引数が :c:type:`PyFileObject` か :c:type:`PyFileObject` のサブタイプのときに
   真を返します。

   .. versionchanged:: 2.2
      サブタイプを引数にとれるようになりました.


.. c:function:: int PyFile_CheckExact(PyObject *p)

   引数が :c:type:`PyFileObject` 型で、かつ :c:type:`PyFileObject` 型の
   サブタイプでないときに真を返します。

   .. versionadded:: 2.2


.. c:function:: PyObject* PyFile_FromString(char *filename, char *mode)

   .. index:: single: fopen()

   成功すると、 *filename* に指定した名前のファイルを *mode* に指定した
   ファイルモードで開いて得た新たなファイルオブジェクトを返します。
   *mode* のセマンティクスは標準 C ルーチン :c:func:`fopen` と同じです。
   失敗すると *NULL* を返します。


.. c:function:: PyObject* PyFile_FromFile(FILE *fp, char *name, char *mode, int (*close)(FILE*))

   すでに開かれている標準 C ファイルポインタ *fp* から新たな
   :c:type:`PyFileObject` を生成します。この関数で生成したファイルオブジェクト
   は、閉じる際に *close* に指定した関数を呼び出します。失敗すると
   *NULL* を返します。


.. c:function:: FILE* PyFile_AsFile(PyObject *p)

   *p* に関連付けられたファイルオブジェクトを :c:type:`FILE\*` で返します。

   呼び出し側が :term:`GIL` を開放している間もこの関数が返した :c:type:`FILE\*`
   オブジェクトを使うのであれば、以下に解説されている :c:func:`PyFile_IncUseCount`
   と :c:func:`PyFile_DecUseCount` 関数を適切に呼び出さなければなりません。


.. c:function:: void PyFile_IncUseCount(PyFileObject \*p)

   PyFileObject 内部の、 :c:type:`FILE\*` が使用中であることを示す使用数カウント
   をインクリメントします。
   これは、別のスレッドで使用中の :c:type:`FILE\*` に対して Python が
   fclose() を呼び出すことを防ぎます。
   この関数の呼び出し側は、 :c:type:`FILE\*` を使い終わったときに必ず
   :c:func:`PyFile_DecUseCount` を呼び出さなければなりません。
   そうしなければ、 Python はそのファイルオブジェクトを永遠に閉じません。

   この関数を呼び出すときは、 :term:`GIL` を取得していなければなりません。

   例えば、 :c:func:`PyFile_AsFile` を呼び出した後、GILを開放する前に
   この関数を呼び出します。 ::

      FILE *fp = PyFile_AsFile(p);
      PyFile_IncUseCount(p);
      /* ... */
      Py_BEGIN_ALLOW_THREADS
      do_something(fp);
      Py_END_ALLOW_THREADS
      /* ... */
      PyFile_DecUseCount(p);

   .. versionadded:: 2.6


.. c:function:: void PyFile_DecUseCount(PyFileObject \*p)

   PyFileObject 内部の、 :c:type:`FILE\*` が使用中であることを示す unlocked_count
   メンバーをデクリメントして、呼び出し元が :c:type:`FILE\*` を使い終わった
   ことを示します。
   これは、先に行った :c:func:`PyFile_IncUseCount` の呼び出しを取り消すため
   だけに呼び出されるでしょう。

   この関数を呼び出すときは、 :term:`GIL` を取得していなければなりません。
   (上の例を参照してください)

   .. versionadded:: 2.6

.. c:function:: PyObject* PyFile_GetLine(PyObject *p, int n)

   .. index:: single: EOFError (built-in exception)

   ``p.readline([*n*])`` と同じで、この関数はオブジェクト *p*
   の各行を読み出します。 *p* はファイルオブジェクトか、 :meth:`readline`
   メソッドを持つ何らかのオブジェクトでかまいません。
   *n* が ``0`` の場合、行の長さに関係なく正確に 1 行だけ読み出します。
   *n* が ``0`` より大きければ、 *n* バイト以上のデータは読み出しません;
   従って、行の一部だけが返される場合があります。
   どちらの場合でも、読み出し後すぐにファイルの終端に到達した場合には空文字列を
   返します。 *n* が ``0`` より小さければ、長さに関わらず 1 行だけを
   読み出しますが、すぐにファイルの終端に到達した場合には :exc:`EOFError`
   を送出します。


.. c:function:: PyObject* PyFile_Name(PyObject *p)

   *p* に指定したファイルの名前を文字列オブジェクトで返します。


.. c:function:: void PyFile_SetBufSize(PyFileObject *p, int n)

   .. index:: single: setvbuf()

   :c:func:`setvbuf` があるシステムでのみ利用できます。
   この関数を呼び出してよいのはファイルオブジェクトの生成直後のみです。


.. c:function:: int PyFile_SetEncoding(PyFileObject *p, const char *enc)

   Unicode オブジェクトをファイルに出力するときにのエンコーディングを *enc*
   にします。成功すると ``1`` を、失敗すると ``0`` を返します。

   .. versionadded:: 2.3


.. c:function:: int PyFile_SetEncodingAndErrors(PyFileObject *p, const char *enc, *errors)

   Unicode オブジェクトをファイルに出力するときにのエンコーディングを *enc*
   に設定し、そのエラーモードを *err* に設定します。

   .. versionadded:: 2.6


.. c:function:: int PyFile_SoftSpace(PyObject *p, int newflag)

   .. index:: single: softspace (file attribute)

   この関数はインタプリタの内部的な利用のために存在します。
   この関数は *p* の :attr:`softspace` 属性を *newflag* に設定し、
   以前の設定値を返します。この関数を正しく動作させるために、 *p*
   がファイルオブジェクトである必然性はありません; 任意のオブジェクトを
   サポートします (:attr:`softspace` 属性が設定されているかどうかのみが
   問題だと思ってください)。
   この関数は全てのエラーを解消し、属性値が存在しない場合や属性値を
   取得する際にエラーが生じると、 ``0`` を以前の値として返します。
   この関数からはエラーを検出できませんが、そもそもそういう必要はありません。


.. c:function:: int PyFile_WriteObject(PyObject *obj, PyObject *p, int flags)

   .. index:: single: Py_PRINT_RAW

   オブジェクト *obj* をファイルオブジェクト *p* に書き込みます。
   *flag* がサポートするフラグは :const:`Py_PRINT_RAW` だけです;
   このフラグを指定すると、オブジェクトに :func:`repr` ではなく :func:`str`
   を適用した結果をファイルに書き出します。
   成功した場合には ``0`` を返し、失敗すると ``-1`` を返して適切な例外を
   セットします。


.. c:function:: int PyFile_WriteString(const char *s, PyObject *p)

   文字列 *s* をファイルオブジェクト *p* に書き出します。成功した場合には
   ``0`` を返し、失敗すると ``-1`` を返して適切な例外をセットします。

