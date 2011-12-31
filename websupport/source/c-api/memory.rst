.. highlightlang:: c


.. _memory:

**********
メモリ管理
**********

.. sectionauthor:: Vladimir Marangozov <Vladimir.Marangozov@inrialpes.fr>



.. _memoryoverview:

概要
====

Python におけるメモリ管理には、全ての Python オブジェクトとデータ構造が入ったプライベートヒープ (private heap)
が必須です。プライベートヒープの管理は、内部的には *Python メモリマネージャ (Python memory manager)*
が確実に行います。Python メモリマネージャには、共有 (sharing)、セグメント分割 (segmentation)、事前割り当て
(preallocation)、キャッシュ化 (caching) といった、様々な動的記憶管理の側面を扱うために、個別のコンポーネントがあります。

最低水準層では、素のメモリ操作関数 (raw memory allocator) がオペレーティングシステムのメモリ管理機構とやりとりして、
プライベートヒープ内にPython 関連の全てのデータを記憶するのに十分な空きがあるかどうか確認します。
素のメモリ操作関数の上には、いくつかのオブジェクト固有のメモリ操作関数があります。これらは同じヒープを操作し、
各オブジェクト型固有の事情に合ったメモリ管理ポリシを実装しています。例えば、整数オブジェクトは文字列やタプル、辞書とは違ったやり方で
ヒープ内で管理されます。というのも、整数には値を記憶する上で特別な要件があり、速度/容量のトレードオフが存在するからです。このように、 Python
メモリマネジャは作業のいくつかをオブジェクト固有のメモリ操作関数に委譲しますが、これらの関数がプライベートヒープからはみ出してメモリ管理を行わないように
しています。

重要なのは、たとえユーザがいつもヒープ内のメモリブロックを指すようなオブジェクトポインタを操作しているとしても、Python 用ヒープの管理は
インタプリタ自体が行うもので、ユーザがそれを制御する余地はないと理解することです。Python オブジェクトや内部使用されるバッファを入れるための
ヒープ空間のメモリ確保は、必要に応じて、Python メモリマネージャがこのドキュメント内で列挙しているPython/C API 関数群を介して行います。

.. index::
   single: malloc()
   single: calloc()
   single: realloc()
   single: free()

メモリ管理の崩壊を避けるため、拡張モジュールの作者は決して Python  オブジェクトを C ライブラリが公開している関数:
:c:func:`malloc` 、 :c:func:`calloc` 、 :c:func:`realloc` および :c:func:`free` で操作しようとしては
なりません。こうした関数を使うと、C のメモリ操作関数と Python メモリマネージャとの間で関数呼び出しが交錯します。 C のメモリ操作関数とPython
メモリマネージャは異なるアルゴリズムで実装されていて、異なるヒープを操作するため、呼び出しの交錯は致命的な結果を招きます。とはいえ、個別の目的のためなら、
C ライブラリのメモリ操作関数を使って安全にメモリを確保したり解放したりできます。例えば、以下がそのような例です::

   PyObject *res;
   char *buf = (char *) malloc(BUFSIZ); /* for I/O */

   if (buf == NULL)
       return PyErr_NoMemory();
   ...Do some I/O operation involving buf...
   res = PyString_FromString(buf);
   free(buf); /* malloc'ed */
   return res;

この例では、I/O バッファに対するメモリ要求は C ライブラリのメモリ操作関数を使っています。 Python メモリマネジャは戻り値として
返される文字列オブジェクトを確保する時にだけ必要です。

とはいえ、ほとんどの状況では、メモリの操作は Python ヒープに固定して行うよう勧めます。なぜなら、Python ヒープは Python
メモリマネジャの管理下にあるからです。例えば、インタプリタを C で書かれた新たなオブジェクト型で拡張する際には、ヒープでのメモリ管理が必要です。
Python ヒープを使った方がよいもう一つの理由として、拡張モジュールが必要としているメモリについて Python メモリマネージャに *情報を提供*
してほしいということがあります。たとえ必要なメモリが内部的かつ非常に特化した用途に対して排他的に用いられるものだとしても、全てのメモリ操作要求を
Python メモリマネージャに委譲すれば、インタプリタはより正確なメモリフットプリント (memory footprint)
の全体像を把握できます。その結果、特定の状況では、 Python メモリマネージャがガベージコレクションやメモリのコンパクト化、
その他何らかの予防措置といった、適切な動作をトリガできることがあります。上の例で示したように C ライブラリのメモリ操作関数を使うと、 I/O
バッファ用に確保したメモリは Python メモリマネージャの管理から完全に外れることに注意してください。


.. _memoryinterface:

メモリインタフェース
====================

Python ヒープに対してメモリを確保したり解放したりするために、以下の関数セットが利用できます。これらの関数は ANSI C 標準に
従ってモデル化されていますが、0 バイトの領域を要求した際の動作についても定義しています:


.. c:function:: void* PyMem_Malloc(size_t n)

   *n* バイトをメモリ確保し、確保されたメモリを指す :c:type:`void\*`  型のポインタを返します。確保要求に失敗した場合には *NULL* を
   返します。 0 バイトをリクエストすると、可能ならば独立した非 *NULL* のポインタを返します。このポインタは
   :c:func:`PyMem_Malloc(1)`  を代わりに呼んだときのようなメモリ領域を指しています。
   確保されたメモリ領域はいかなる初期化も行われていません。


.. c:function:: void* PyMem_Realloc(void *p, size_t n)

   *p* が指しているメモリブロックを *n* バイトにサイズ変更します。メモリの内容のうち、新旧のサイズのうち小さい方までの領域は変更されません。 *p* が
   *NULL* ならば、この関数は :c:func:`PyMem_Malloc(n)` と等価になります;  それ以外の場合で、 *n* がゼロに等しければ、
   メモリブロックはサイズ変更されますが、解放されず、非 *NULL* のポインタを返します。 *p* の値を *NULL* にしないのなら、以前呼び出した
   :c:func:`PyMem_Malloc` や  :c:func:`PyMem_Realloc` の返した値でなければなりません。


.. c:function:: void PyMem_Free(void *p)

   *p* が指すメモリブロックを解放します。 *p* は以前呼び出した :c:func:`PyMem_Malloc` や
   :c:func:`PyMem_Realloc` の返した値でなければなりません。それ以外の場合や、すでに :c:func:`PyMem_Free(p)` を
   呼び出した後だった場合、未定義の動作になります。 *p* が *NULL* なら、何も行いません。

以下に挙げる型対象のマクロは利便性のために提供されているものです。 *TYPE* は任意の C の型を表します。


.. c:function:: TYPE* PyMem_New(TYPE, size_t n)

   :c:func:`PyMem_Malloc` と同じですが、 ``(n * sizeof(TYPE))`` バイトのメモリを確保します。
   :c:type:`TYPE\*` に型キャストされたポインタを返します。メモリには何の初期化も行われていません。


.. c:function:: TYPE* PyMem_Resize(void *p, TYPE, size_t n)

   :c:func:`PyMem_Realloc` と同じですが、 ``(n * sizeof(TYPE))``
   バイトにサイズ変更されたメモリを確保します。
   :c:type:`TYPE\*` に型キャストされたポインタを返します。
   関数が終わったとき、 *p* は新しいメモリ領域のポインタか、失敗した場合は
   *NULL* になります。これは C プリプロセッサのマクロで、 p
   は常に上書きされます。エラーを処理するときにメモリを失う事を避けるには、
   p の元の値を保存しておいてください。


.. c:function:: void PyMem_Del(void *p)

   :c:func:`PyMem_Free` と同じです。

上記に加えて、C API 関数を介することなく Python メモリ操作関数を直接呼び出すための以下のマクロセットが提供されています。
ただし、これらのマクロは Python バージョン間でのバイナリ互換性を保てず、それゆえに拡張モジュールでは撤廃されているので注意してください。

:c:func:`PyMem_MALLOC` 、 :c:func:`PyMem_REALLOC` 、 :c:func:`PyMem_FREE` 。

:c:func:`PyMem_NEW` 、 :c:func:`PyMem_RESIZE` 、 :c:func:`PyMem_DEL` 。


.. _memoryexamples:

例
==

最初に述べた関数セットを使って、 :ref:`memoryoverview` 節の例を  Python ヒープに I/O
バッファをメモリ確保するように書き換えたものを以下に示します::

   PyObject *res;
   char *buf = (char *) PyMem_Malloc(BUFSIZ); /* for I/O */

   if (buf == NULL)
       return PyErr_NoMemory();
   /* ...Do some I/O operation involving buf... */
   res = PyString_FromString(buf);
   PyMem_Free(buf); /* allocated with PyMem_Malloc */
   return res;

同じコードを型対象の関数セットで書いたものを以下に示します::

   PyObject *res;
   char *buf = PyMem_New(char, BUFSIZ); /* for I/O */

   if (buf == NULL)
       return PyErr_NoMemory();
   /* ...Do some I/O operation involving buf... */
   res = PyString_FromString(buf);
   PyMem_Del(buf); /* allocated with PyMem_New */
   return res;

上の二つの例では、バッファを常に同じ関数セットに属する関数で操作していることに注意してください。
実際、あるメモリブロックに対する操作は、異なるメモリ操作機構を混用する危険を減らすために、同じメモリ API ファミリを使って行うことが
必要です。以下のコードには二つのエラーがあり、そのうちの一つには異なるヒープを操作する別のメモリ操作関数を混用しているので *致命的 (Fatal)*
とラベルづけをしています。 ::

   char *buf1 = PyMem_New(char, BUFSIZ);
   char *buf2 = (char *) malloc(BUFSIZ);
   char *buf3 = (char *) PyMem_Malloc(BUFSIZ);
   ...
   PyMem_Del(buf3);  /* Wrong -- should be PyMem_Free() */
   free(buf2);       /* Right -- allocated via malloc() */
   free(buf1);       /* Fatal -- should be PyMem_Del()  */

素のメモリブロックを Python ヒープ上で操作する関数に加え、 :c:func:`PyObject_New` 、
:c:func:`PyObject_NewVar` 、および :c:func:`PyObject_Del` を使うと、 Python におけるオブジェクトを
メモリ確保したり解放したりできます。

これらの関数については、次章の C による新しいオブジェクト型の定義や実装に関する記述の中で説明します。

