
.. _simple:

*************************
単純文 (simple statement)
*************************

.. index:: pair: simple; statement

単純文とは、単一の論理行内に収められる文です。単一の行内には、複数の単純文をセミコロンで区切って入れることができます。単純文の構文は以下の通りです:

.. productionlist::
   simple_stmt: `expression_stmt`
              : | `assert_stmt`
              : | `assignment_stmt`
              : | `augmented_assignment_stmt`
              : | `pass_stmt`
              : | `del_stmt`
              : | `print_stmt`
              : | `return_stmt`
              : | `yield_stmt`
              : | `raise_stmt`
              : | `break_stmt`
              : | `continue_stmt`
              : | `import_stmt`
              : | `global_stmt`
              : | `exec_stmt`


.. _exprstmts:

式文 (expression statement)
===========================

.. index::
   pair: expression; statement
   pair: expression; list

式文は、 (主に対話的な使い方では) 値を計算して出力するために使ったり、(通常は) プロシジャ (procedure: 有意な結果を返さない
関数のことです; Python では、プロシジャは値 ``None`` を返します) を呼び出すために使います。その他の使い方でも式文を使うことができ
ますし、有用なこともあります。式文の構文は以下の通りです:

.. productionlist::
   expression_stmt: `expression_list`

式文は式のリスト (単一の式のこともあります) を値評価します。

.. index::
   builtin: repr
   single: None
   pair: string; conversion
   single: output
   pair: standard; output
   pair: writing; values
   pair: procedure; call

対話モードでは、値が ``None`` でない場合、値を組み込み関数 :func:`repr` で文字列に変換して、
その結果のみからなる一行を標準出力に書き出します ( :ref:`print` 節参照)。 (``None``
になる式文の値は書き出されないので、プロシジャ呼び出しを行っても出力は得られません。)


.. _assignment:

代入文 (assignment statement)
=============================

.. index::
   pair: assignment; statement
   pair: binding; name
   pair: rebinding; name
   object: mutable
   pair: attribute; assignment

代入文は、名前を値に (再) 束縛したり、変更可能なオブジェクトの属性や要素を変更したりするために使われます:

.. productionlist::
   assignment_stmt: (`target_list` "=")+ (`expression_list` | `yield_expression`)
   target_list: `target` ("," `target`)* [","]
   target: `identifier`
         : | "(" `target_list` ")"
         : | "[" `target_list` "]"
         : | `attributeref`
         : | `subscription`
         : | `slicing`

(末尾の三つのシンボルの構文については  :ref:`primaries` 節を参照してください。)

.. index:: pair: expression; list

代入文は式のリスト (これは単一の式でも、カンマで区切られた式リストでもよく、後者はタプルになることを思い出してください)
を評価し、得られた単一の結果オブジェクトをターゲット (target) のリストに対して左から右へと代入してゆきます。

.. index::
   single: target
   pair: target; list

代入はターゲット (リスト) の形式に従って再帰的に行われます。ターゲットが変更可能なオブジェクト (属性参照、添字表記、またはスライス)
の一部である場合、この変更可能なオブジェクトは最終的に代入を実行して、その代入が有効な操作であるか判断しなければなりません。
代入が不可能な場合には例外を発行することもできます。型ごとにみられる規則や、送出される例外は、そのオブジェクト型定義で与えられています (
:ref:`types` 節を参照してください).

.. index:: triple: target; list; assignment

ターゲットリストへのオブジェクトの代入は、以下のようにして再帰的に定義されています。

* ターゲットリストが単一のターゲットからなる場合: オブジェクトはそのターゲットに代入されます。

* ターゲットリストが、カンマで区切られた複数のターゲットからなるリストの場合: オブジェクトはターゲットリスト中のターゲット数と
  同じ数の要素からなるイテレート可能オブジェクトでなければならず、その各要素は左から右へと対応するターゲットに代入されます。

単一のターゲットへの単一のオブジェクトの代入は、以下のようにして再帰的に定義されています。

* ターゲットが識別子 (名前) の場合:

   .. index:: statement: global

   * 名前が現在のコードブロック内の :keyword:`global` 文に書かれていない場合: 名前は現在のローカル名前空間内のオブジェクトに
     束縛されます。

   * それ以外の場合: 名前は現在のグローバル名前空間内のオブジェクトに束縛されます。

   .. index:: single: destructor

   名前がすでに束縛済みの場合、再束縛 (rebind) がおこなわれます。再束縛によって、以前その名前に束縛されていたオブジェクトの参照カウント
   (reference count) がゼロになった場合、オブジェクトは解放 (deallocate) され、デストラクタ  (destructor) が
   (存在すれば) 呼び出されます。

* ターゲットが丸括弧や角括弧で囲われたターゲットリストの場合: オブジェクトは
  ターゲットリスト中のターゲット数と同じ数の要素からなるイテレート可能
  オブジェクトでなければならず、その各要素は左から右へと対応するターゲットに代入されます。

  .. index:: pair: attribute; assignment

* ターゲットが属性参照の場合: 参照されている一次語の式が値評価されます。値は代入可能な属性を伴うオブジェクトでなければなりません; そうでなければ、
  :exc:`TypeError` が送出されます。次に、このオブジェクトに対して、被代入オブジェクトを指定した属性に代入してよいか問い合わせます;
  代入を実行できない場合、例外 (通常は :exc:`AttributeError` ですが、必然ではありません) を送出します。

  .. _attr-target-note:
 
  注意: オブジェクトがクラスインスタンスで、代入演算子の両辺に属性参照が
  あるとき、右辺式の ``a.x`` はインスタンスの属性と (インスタンスの
  属性が存在しなければ) クラス属性のどちらにもアクセスする可能性があります。
  左辺のターゲット ``a.x`` は常にインスタンスの属性として割り当てられ、
  必要ならば生成されます。このとおり、現れる二つの ``a.x`` は同じ値を参照する
  とは限りません: 右辺式はクラス属性を参照し、左辺は新しいインスタンス属性を
  代入のターゲットとして生成するようなとき::
 
     class Cls:
         x = 3             # class variable
     inst = Cls()
     inst.x = inst.x + 1   # writes inst.x as 4 leaving Cls.x as 3
 
  このことは、 :func:`property` で作成されたプロパティのような
  デスクリプタ属性に対しては、必ずしもあてはまるとは限りません、

  .. index::
     pair: subscription; assignment
     object: mutable

* ターゲットが添字表記の場合: 参照されている一次語の式が値評価されます。まず、値は変更可能な (リストのような) シーケンスオブジェクトか、
  (辞書のような) マップオブジェクトでなければなりません。次に、添字表記の表す式が値評価されます。

  .. index::
     object: sequence
     object: list

  一次語が変更可能な (リストのような) シーケンスオブジェクトの場合、まず添字は整数でなければなりません。添字が負数の場合、シーケンスの
  長さが加算されます。添字は最終的に、シーケンスの長さよりも小さな非負の整数でなくてはなりません。次に、添字をインデクスに
  持つ要素に非代入オブジェクトを代入してよいか、シーケンスに問い合わせます。範囲を超えたインデクスに対しては :exc:`IndexError`  が送出されます
  (添字指定されたシーケンスに代入を行っても、リスト要素の新たな追加はできません)。

  .. index::
     object: mapping
     object: dictionary

  一次語が (辞書のような) マップオブジェクトの場合、まず添字はマップのキー型と互換性のある型でなくてはなりません。
  次に、添字を被代入オブジェクトに関連付けるようなキー/データの対を生成するようマップオブジェクトに問い合わせます。
  この操作では、既存のキー/値の対を同じキーと別の値で置き換えてもよく、(同じ値を持つキーが存在しない場合) 新たなキー/値の対を挿入してもかまいません。

  .. index:: pair: slicing; assignment

* ターゲットがスライスの場合: 参照されている一次語の式が値評価されます。まず、値は変更可能な (リストのような) シーケンスオブジェクト
  でなければなりません。被代入オブジェクトは同じ型を持ったシーケンスオブジェクトでなければなりません。次に、スライスの下境界と上境界を示す式があれば
  評価されます; デフォルト値はそれぞれゼロとシーケンスの長さです。上下境界は整数にならなければなりません。いずれかの境界が負数に
  なった場合、シーケンスの長さが加算されます。最終的に、境界はゼロからシーケンスの長さまでの内包になるようにクリップされます。
  最後に、スライスを被代入オブジェクトで置き換えてよいかシーケンスオブジェクトに問い合わせます。オブジェクトで許されている限り、スライスの長さは
  被代入シーケンスの長さと異なっていてよく、この場合にはターゲットシーケンスの長さが変更されます。

.. impl-detail::

   現在の実装では、ターゲットの構文は式の構文と同じであるとみなされており、無効な構文はコード生成フェーズ中に詳細なエラーメッセージを伴って拒否されます。

警告: 代入の定義では、左辺値と右辺値がオーバラップするような代入 (例えば、 ``a, b = b, a`` を行うと、二つの変数を入れ替えます) を
定義しても '安全 (safe)' に代入できますが、代入対象となる変数群 *の間で* オーバラップがある場合は安全ではありません！
例えば、以下のプログラムは ``[0, 2]`` を出力してしまいます::

   x = [0, 1]
   i = 0
   i, x[i] = 1, 2
   print x


.. _augassign:

累算代入文 (augmented assignment statement)
-------------------------------------------

.. index::
   pair: augmented; assignment
   single: statement; assignment, augmented

累算代入文は、二項演算と代入文を組み合わせて一つの文にしたものです:

.. productionlist::
   augmented_assignment_stmt: `augtarget` `augop` (`expression_list` | `yield_expression`)
   augtarget: `identifier` | `attributeref` | `subscription` | `slicing`
   augop: "+=" | "-=" | "*=" | "/=" | "//=" | "%=" | "**="
        : | ">>=" | "<<=" | "&=" | "^=" | "|="

累算代入文は、ターゲット (通常の代入文と違って、アンパックは起こりません) と式リストを評価し、それら二つの被演算子間で特定の累算
代入型の二項演算を行い、結果をもとのターゲットに代入します。ターゲットは一度しか評価されません。

.. % JJJ: この一文はおそらく間違ってここに挿入されています
.. % (最後の 3 つのシンボル定義については、~\ref{primaries} 節を参照
.. % してください。)

``x += 1`` のような累算代入式は、 ``x = x + 1`` のように書き換えてほぼ同様の動作にできますが、厳密に等価にはなりません。累算代入の
方では、 ``x`` は一度しか評価されません。また、実際の処理として、可能ならば *インプレース (in-place)* 演算が実行されます。
これは、代入時に新たなオブジェクトを生成してターゲットに代入するのではなく、以前のオブジェクトの内容を変更するということです。

累算代入文で行われる代入は、タプルへの代入や、一文中に複数のターゲットが存在する場合を除き、通常の代入と同じように扱われます。
同様に、累算代入で行われる二項演算は、場合によって *インプレース演算* が行われることを除き、通常の二項演算と同じです。

属性参照のターゲットの場合、 :ref:`クラスとインスタンスの属性についての注意 <attr-target-note>` と同様に通常の代入が適用されます。

.. _assert:

:keyword:`assert` 文
============================

.. index::
   statement: assert
   pair: debugging; assertions

assert 文は、プログラム内にデバッグ用アサーション (debugging assertion) を仕掛けるための便利な方法です:

.. productionlist::
   assert_stmt: "assert" `expression` ["," `expression`]

単純な形式 ``assert expression`` は、 ::

   if __debug__:
      if not expression: raise AssertionError

と等価です。拡張形式 ``assert expression1, expression2`` は、 ::

   if __debug__:
      if not expression1: raise AssertionError(expression2)

と等価です。

.. index::
   single: __debug__
   exception: AssertionError

上記の等価関係は、 ``__debug__`` と :exc:`AssertionError` が、同名の組み込み
変数を参照しているという前提の上に成り立っています。現在の実装では、組み込み変数 ``__debug__`` は通常の状況では ``True``
であり、最適化がリクエストされた場合（コマンドラインオプション -O）は ``False`` です。現状のコード生成器は、コンパイル時に最適化が要求されて
いると assert 文に対するコードを全く出力しません。実行に失敗した式のソースコードをエラーメッセージ内に入れる必要はありません;
コードはスタックトレース内で表示されます。

``__debug__`` への代入は不正な操作です。組み込み変数の値は、インタプリタが開始するときに決定されます。


.. _pass:

:keyword:`pass` 文
==================

.. index::
   statement: pass
   pair: null; operation

.. productionlist::
   pass_stmt: "pass"

:keyword:`pass` はヌル操作 (null operation) です --- :keyword:`pass`
が実行されても、何も起きません。 :keyword:`pass` は、例えば::

   def f(arg): pass    # a function that does nothing (yet)

   class C: pass       # a class with no methods (yet)

のように、構文法的には文が必要だが、コードとしては何も実行したくない場合のプレースホルダとして有用です。


.. _del:

:keyword:`del` 文
=================

.. index::
   statement: del
   pair: deletion; target
   triple: deletion; target; list

.. productionlist::
   del_stmt: "del" `target_list`

オブジェクトの削除 (deletion) は、代入の定義と非常に似た方法で再帰的に定義されています。ここでは完全な詳細を記述するよりも
いくつかのヒントを述べるにとどめます。

ターゲットリストに対する削除は、各々のターゲットを左から右へと順に再帰的に削除します。

.. index::
   statement: global
   pair: unbinding; name

名前に対して削除を行うと、ローカルまたはグローバル名前空間でのその名前の束縛を解除します。どちらの名前空間かは、名前が同じコードブロック内の
:keyword:`global` 文で宣言されているかどうかによります。名前が未束縛 (unbound) であるばあい、 :exc:`NameError`
例外が送出されます。

.. index:: pair: free; variable

ネストしたブロック中で自由変数になっているローカル名前空間上の名前に対する削除は不正な操作になります

.. index:: pair: attribute; deletion

属性参照、添字表記、およびスライスの削除操作は、対象となる一次語オブジェクトに渡されます; スライスの削除は一般的には適切な
型の空のスライスを代入するのと等価です (が、この仕様自体もスライスされるオブジェクトで決定されています)。


.. _print:

:keyword:`print` 文
===================

.. index:: statement: print

.. productionlist::
   print_stmt: "print" ([`expression` ("," `expression`)* [","]]
             : | ">>" `expression` [("," `expression`)+ [","]])

:keyword:`print` は、式を逐次的に評価し、得られたオブジェクトを標準出力に書き出します。オブジェクトが文字列でなければ、まず文字列
変換規則を使って文字列に変換され、次いで (得られた文字列か、オリジナルの文字列が) 書き出されます。出力系の現在の書き出し位置が行頭にある
と考えられる場合を除き、各オブジェクトの出力前にスペースが一つ出力されます。行頭にある場合とは、(1) 標準出力にまだ何も書き出されていない場合、(2)
標準出力に最後に書き出された文字が ``' '`` を除く空白である、または (3) 標準出力に対する最後の書き出し操作が  :keyword:`print`
文によるものではない場合、です。(こうした理由から、場合によっては空文字を標準出力に書き出すと便利なことがあります。)

.. note::

   組み込みのファイルオブジェクトでない、ファイルオブジェクトに似た動作をするオブジェクトでは、組み込みのファイルオブジェクト
   が持つ上記の性質を適切にエミュレートしていないことがあるため、当てにしないほうがよいでしょう。

.. index::
   single: output
   pair: writing; values
   pair: trailing; comma
   pair: newline; suppression

:keyword:`print` 文がカンマで終了していない限り、末尾には文字 ``'\n'`` が書き出されます。この仕様は、文に予約語
:keyword:`print` がある場合のみの動作です。

.. index::
   pair: standard; output
   module: sys
   single: stdout (in module sys)
   exception: RuntimeError

標準出力は、組み込みモジュール :mod:`sys` 内で ``stdout``  という名前のファイルオブジェクトとして定義されています。
該当するオブジェクトが存在しないか、オブジェクトに :meth:`write` メソッドがない場合、 :exc:`RuntimeError`
例外が送出されます。.

.. index:: single: extended print statement

:keyword:`print` には、上で説明した構文の第二形式で定義されている拡張形式があります。この形式は、"山形 :keyword:`print`
表記 (:keyword:`print` chevron)" と呼ばれます。この形式では、 ``>>`` の直後にくる最初の式の値評価結果は "ファイル類似
(file-like)" なオブジェクト、とりわけ上で述べたように :meth:`write` メソッドを持つオブジェクトで
なければなりません。この拡張形式では、ファイルオブジェクトを指定する式よりも後ろの式が、指定されたファイルオブジェクトに出力されます。最初の式の値評価結果が
``None`` になった場合、 ``sys.stdout``  が出力ファイルとして使われます。


.. _return:

:keyword:`return` 文
====================

.. index::
   statement: return
   pair: function; definition
   pair: class; definition

.. productionlist::
   return_stmt: "return" [`expression_list`]

:keyword:`return` は、関数定義内で構文法的にネストして現れますが、ネストしたクラス定義内には現れません。

式リストがある場合、リストが値評価されます。それ以外の場合は ``None`` で置き換えられます。

:keyword:`return` を使うと、式リスト (または ``None``)  を戻り値として、現在の関数呼び出しから抜け出します。

.. index:: keyword: finally

:keyword:`return` によって、 :keyword:`finally` 節をともなう :keyword:`try`
文の外に処理が引き渡されると、実際に関数から抜ける前に  :keyword:`finally` 節が実行されます。

ジェネレータ関数の場合には、 :keyword:`return` 文の中に :token:`expression_list` を入れることはできません。
ジェネレータ関数の処理コンテキストでは、単体の :keyword:`return`  はジェネレータ処理を終了し :exc:`StopIteration`
を送出させることを示します。


.. _yield:

:keyword:`yield` 文
===================

.. index::
   statement: yield
   single: generator; function
   single: generator; iterator
   single: function; generator
   exception: StopIteration

.. productionlist::
   yield_stmt: `yield_expression`

:keyword:`yield` 文は、ジェネレータ関数 (generator function) を
定義するときだけ使われ、かつジェネレータ関数の本体の中でだけ用いられます。関数定義中で :keyword:`yield`
文を使うだけで、関数定義は通常の関数でなくジェネレータ関数になります。

ジェネレータ関数が呼び出されると、ジェネレータイテレータ (generator iterator)、一般的にはジェネレータ (generator) を
返します。ジェネレータ関数の本体は、ジェネレータの :meth:`next` が例外を発行するまで繰り返し呼び出して実行します。

:keyword:`yield` 文が実行されると、現在のジェネレータの状態は凍結 (freeze) され、 :token:`expression_list`
の値が :meth:`next`  の呼び出し側に返されます。ここでの "凍結" は、ローカルな変数への束縛、命令ポインタ (instruction
pointer)、および内部実行スタック (internal evaluation stack) を含む、全てのローカルな状態が保存されることを意味します:
すなわち、必要な情報を保存しておき、次に :meth:`next` が呼び出された際に、関数が :keyword:`yield` 文をあたかも
もう一つの外部呼出しであるかのように処理できるようにします。

Python バージョン 2.5 では、 :keyword:`yield` 文が  :keyword:`try` ...  :keyword:`finally`
構造における  :keyword:`try` 節で許されるようになりました。ジェネレータが終了（finalized）される
（参照カウントがゼロになるか、ガベージコレクションされる) までに再開されなければ、ジェネレータ-イテレータの :meth:`close` メソッドが呼ばれ、
留保されている :keyword:`finally` 節が実行できるようになります。

.. note::

   Python 2.2 では、 ``generators`` 機能が有効になっている場合にのみ :keyword:`yield` 文を使えました。
   この機能を有効にするための ``__future__`` import 文は次のとおりでした。 ::

      from __future__ import generators


.. seealso::

   :pep:`0255` - 単純なジェネレータ
      Python へのジェネレータと :keyword:`yield` 文の導入提案

   :pep:`0342` - 改善されたジェネレータによるコルーチン (Coroutine)
      その他のジェネレータの改善と共に、 :keyword:`yield` が :keyword:`try` ... :keyword:`finally`
      ブロックの中に存在することを可能にするための提案


.. _raise:

:keyword:`raise` 文
===================

.. index::
   statement: raise
   single: exception
   pair: raising; exception

.. productionlist::
   raise_stmt: "raise" [`expression` ["," `expression` ["," `expression`]]]

式を伴わない場合、 :keyword:`raise` は現在のスコープで最終的に有効になっている例外を再送出します。そのような例外が現在のスコープで
アクティブでない場合、 :exc:`TypeError` 例外が送出されて、これがエラーであることを示します (IDLE で実行した場合は、代わりに
exceptionQueue.Empty 例外を送出します)。

それ以外の場合、 :keyword:`raise` は式を値評価して、三つのオブジェクトを取得します。このとき、 ``None``
を省略された式の値として使います。最初の二つのオブジェクトは、例外の *型 (type)* と例外の *値 (value)* を決定するために用いられます。

最初のオブジェクトがインスタンスである場合、例外の型はインスタンスのクラスになり、インスタンス自体が例外の値になります。このとき第二のオブジェクトは
``None`` でなければなりません。

最初のオブジェクトがクラスの場合、例外の型になります。第二のオブジェクトは、例外の値を決めるために使われます:
第二のオブジェクトがインスタンスならば、そのインスタンスが例外の値になります。第二のオブジェクトがタプルの場合、
クラスのコンストラクタに対する引数リストとして使われます; ``None`` なら、空の引数リストとして扱われ、それ以外の型
ならコンストラクタに対する単一の引数として扱われます。このようにしてコンストラクタを呼び出して生成したインスタンスが例外の値になります。

.. index:: object: traceback

第三のオブジェクトが存在し、かつ ``None`` でなければ、オブジェクトはトレースバック  オブジェクトでなければなりません (
:ref:`types` 節参照)。また、例外が発生した場所は現在の処理位置に置き換えられます。
第三のオブジェクトが存在し、オブジェクトがトレースバックオブジェクトでも ``None`` でもなければ、 :exc:`TypeError`
例外が送出されます。 :keyword:`raise` の三連式型は、 :keyword:`except`
節から透過的に例外を再送出するのに便利ですが、再送出すべき例外が現在のスコープで発生した最も新しいアクティブな例外である場合には、式なしの
:keyword:`raise` を使うよう推奨します。

例外に関する追加情報は  :ref:`exceptions` 節にあります。また、例外処理に関する情報は  :ref:`try` 節にあります。


.. _break:

:keyword:`break` 文
===================

.. index::
   statement: break
   statement: for
   statement: while
   pair: loop; statement

.. productionlist::
   break_stmt: "break"

:keyword:`break` 文は、構文としては :keyword:`for` ループや :keyword:`while` ループの
内側でのみ出現することができますが、ループ内の関数定義やクラス定義の内側には出現できません。

.. index:: keyword: else

:keyword:`break` 文は、文を囲う最も内側のループを終了させ、ループにオプションの :keyword:`else`
節がある場合にはそれをスキップします。

.. index:: pair: loop control; target

:keyword:`for` ループを :keyword:`break` によって終了すると、ループ制御ターゲットはその時の値を保持します。

.. index:: keyword: finally

:keyword:`break` が :keyword:`finally` 節を伴う :keyword:`try` 文の
外側に処理を渡す際には、ループを実際に抜ける前にその :keyword:`finally`  節が実行されます。


.. _continue:

:keyword:`continue` 文
======================

.. index::
   statement: continue
   statement: for
   statement: while
   pair: loop; statement
   keyword: finally

.. productionlist::
   continue_stmt: "continue"

:keyword:`continue` 文は :keyword:`for` ループや :keyword:`while` ループ内の
ネストで構文法的にのみ現れますが、ループ内の関数定義やクラス定義、
:keyword:`finally` 句の中には現れません。
:keyword:`continue` 文は、文を囲う最も内側のループの次の周期に処理を継続します。

:keyword:`continue` が :keyword:`finally` 句を持った :keyword:`try` 文を抜けるとき、
その :keyword:`finally` 句が次のループサイクルを始める前に実行されます。

.. _import:
.. _from:

:keyword:`import` 文
====================

.. index::
   statement: import
   single: module; importing
   pair: name; binding
   keyword: from

.. productionlist::
   import_stmt: "import" `module` ["as" `name`] ( "," `module` ["as" `name`] )*
              : | "from" `relative_module` "import" `identifier` ["as" `name`]
              : ( "," `identifier` ["as" `name`] )*
              : | "from" `relative_module` "import" "(" `identifier` ["as" `name`]
              : ( "," `identifier` ["as" `name`] )* [","] ")"
              : | "from" `module` "import" "*"
   module: (`identifier` ".")* `identifier`
   relative_module: "."* `module` | "."+
   name: `identifier`

import 文は、(1) モジュールを探し、必要なら初期化 (initialize) する; (:keyword:`import` 文のあるスコープにおける)
ローカルな名前空間で名前を定義する、の二つの段階を踏んで初期化されます。
:keyword:`import` 文には、 :keyword:`from` を使うか使わないかの2種類の形式があります。
第一形式 (:keyword:`from` のない形式) は、上記の段階をリスト中にある各識別子に対して
繰り返し実行していきます。 :keyword:`from` のある形式では、(1) を一度だけ行い、次いで
(2) を繰り返し実行します。

.. index::
    single: package

ステップ(1)がどのように行われるのかを理解するには、まず、 Python が階層的な
モジュール名をどう扱うのかを理解する必要があります。
モジュールを組織化し名前に階層を持たせるために、Python は パッケージ という
概念を持っています。
モジュールが他のモジュールやパッケージを含むことができないのに対して、
パッケージは他のパッケージやモジュールを含むことができます。
ファイルシステムの視点から見ると、パッケージはディレクトリでモジュールはファイルです。
オリジナルの `specification for packages
<http://www.python.org/doc/essays/packages.html>`_ は今でも読むことができますが、
小さい詳細部分はこのドキュメントが書かれた後に変更されています。

.. index::
    single: sys.modules

モジュール名(特に記述していない場合は、 "モジュール" とはパッケージと
モジュール両方を指しています)が判ったとき、モジュールかパッケージの検索が始まります。
最初にチェックされる場所は、それまでにインポートされたすべてのモジュールのキャッシュ
である :data:`sys.modules` です。
もしモジュールがそこで見つかれば、それが import のステップ(2)で利用されます。

.. index::
    single: sys.meta_path
    single: finder
    pair: finder; find_module
    single: __path__

キャッシュにモジュールが見つからなかった場合、次は :data:`sys.meta_path` が検索されます。
(:data:`sys.meta_path` の仕様は :pep:`302` に見つけることができます。)
これは :term:`finder` オブジェクトのリストで、そのモジュールを読み込む方法を
知っているかどうかをその :meth:`find_module` メソッドをモジュール名を引数として
呼び出すことで、順番に問い合せていきます。
モジュールがパッケージに含まれていた(モジュール名の中にドットが含まれていた)場合、
:meth:`find_module` の第2引数に親パッケージの :attr:`__path__` 属性が渡されます。
(モジュール名の最後のドットより前のすべてがインポートされます)
finder はモジュールを見つけたとき、(後で解説する) :term:`loader` か :const:`None`
を返します。

.. index::
    single: sys.path_hooks
    single: sys.path_importer_cache
    single: sys.path

:data:`sys.meta_path` に含まれるすべての finder が module を見つけられない場合、
幾つかの暗黙的に定義されている finder に問い合わせられます。
どんな暗黙の meta path finder が定義されているかは Python の実装によって様々です。
すべての実装が定義しなければならない1つの finder は、 :data:`sys.path_hooks`
を扱います。


この暗黙の finder は要求されたモジュールを、2箇所のどちらかで定義されている "paths"
から探します。 ("paths" がファイルシステムパスである必要はありません)
インポートしようとしているモジュールがパッケージに含まれている場合、親パッケージの
:attr:`__path__` が :meth:`find_module` の第2引数として渡され、それが paths
として扱われます。モジュールがパッケージに含まれていない場合、 :data:`sys.path`
が paths として扱われます。

paths が決定されたら、それを巡回してその path を扱える finder を探します。
:data:`sys.path_importer_cache` 辞書は path に対する finder をキャッシュしており、
finder を探すときにチェックされます。
path がキャッシュに登録されていない場合は、 :data:`sys.path_hooks` の各オブジェクトを
1つの引数 path で呼び出します。各オブジェクトは finder を返すか、 :exc:`ImportError`
を発生させます。
finder が返された場合、それを :data:`sys.path_importer_cache` にキャッシュして、
その path に対してその finder を使います。
finder が見つからず、 path が存在している場合、 :const:`None`
が :data:`sys.path_importer_cache` に格納されて、暗黙の、
単一のファイルとしてモジュールが格納されているとしてあつかうファイルベースの finder
をその path に対して利用することを示します。
その path が存在しなかった場合、常に :const:`None` を返す finder がその
path に対するキャッシュとして格納されます。


.. index::
    single: loader
    pair: loader; load_module
    exception: ImportError

全ての finder がそのモジュールを見つけられないときは、 :exc:`ImportError`
が発生します。そうでなければ、どれかの finder が loader を返し、その :meth:`load_module`
メソッドがモジュール名を引数に呼び出されてロードを行ないます。
(ローダーのオリジナルの定義については :pep:`302` を参照してください。)
loader はロードするモジュールに対して幾つかの責任があります。
まず、そのモジュールがすでに :data:`sys.modules` にあれば、
(ローダーが import 機構の外から呼ばれた場合に有り得ます)
そのモジュールを初期化に使い、新しいモジュールを使いません。
:data:`sys.modules` にそのモジュールがなければ、初期化を始める前に :data:`sys.modules`
に追加します。 :data:`sys.modules` に追加したあと、モジュールのロード中に
エラーが発生した場合は、その辞書から削除します。
モジュールが既に :data:`sys.modules` にあった場合は、エラーが発生しても
その辞書に残しておきます。

.. index::
    single: __name__
    single: __file__
    single: __path__
    single: __package__
    single: __loader__

ローダーは幾つかの属性をモジュールに設定しなければなりません。
モジュール名を :data:`__name__` に設定します。
ファイルの "path" を :data:`__file__` に設定しますが、ビルトインモジュール
(:data:`sys.builtin_module_names` にリストされている) の場合には
その属性を設定しません。
インポートしているのがパッケージだった場合は、そのパッケージが含むモジュールや
パッケージを探す場所の path のリストを :data:`__path_` に設定します。
:data:`__package__` はオプションですが、そのモジュールやパッケージを含む
パッケージ名(パッケージに含まれていないモジュールには空文字列)を
設定するべきです。 :data:`__loader__` もオプションですが、そのモジュールを
ロードした loader オブジェクトを設定するべきです。

.. index::
    exception: ImportError

ロード中にエラーが発生した場合、他の例外がすでに伝播していないのであれば、
loader は :exc:`ImportError` を発生させます。
それ以外の場合は、 loader はロードして初期化したモジュールを返します。

段階 (1) が例外を送出することなく完了したなら、段階 (2) を開始します。

:keyword:`import` 文の第一形式は、ローカルな名前空間に置かれたモジュール名をモジュールオブジェクトに束縛し、import すべき
次の識別子があればその処理に移ります。モジュール名の後ろに :keyword:`as` がある場合、 :keyword:`as` の後ろの名前はモジュールの
ローカルな名前として使われます。

.. index::
   pair: name; binding
   exception: ImportError

:keyword:`from` 形式は、モジュール名の束縛を行いません: :keyword:`from` 形式では、段階 (1) で見つかったモジュール内から、
識別子リストの各名前を順に検索し、見つかったオブジェクトを識別子の名前でローカルな名前空間において束縛します。 :keyword:`import`
の第一形式と同じように、":keyword:`as` localname" で別名を与えることができます。指定された名前が見つからない場合、
:exc:`ImportError` が送出されます。識別子のリストを星印 (``'*'``) で置き換えると、モジュールで公開されている名前 (public
name) 全てを :keyword:`import` 文のある場所のローカルな名前空間に束縛します。

.. index:: single: __all__ (optional module attribute)

モジュールで *公開されている名前 (public names)* は、モジュールの名前空間内にある ``__all__`` という名前の変数
を調べて決定します; ``__all__`` が定義されている場合、 ``__all__`` はモジュールで定義されていたり、import されている
ような名前の文字列からなるシーケンスでなければなりません。 ``__all__`` 内にある名前は、全て公開された名前であり、実在するものとみなされます。
``__all__`` が定義されていない場合、モジュールの名前空間に見つかった名前で、アンダースコア文字 (``'_'``) で始まっていない
全ての名前が公開された名前になります。 ``__all__`` には、公開されている API 全てを入れなければなりません。 ``__all__``
には、(モジュール内で import されて使われているライブラリモジュールのように) API を構成しない要素を意に反して
公開してしまうのを避けるという意図があります。

``*`` を使った :keyword:`from` 形式は、モジュールのスコープ内だけに作用します。関数内でワイルドカードの import 文 ---
``import *`` --- を使い、関数が自由変数を伴うネストされたブロックであったり、ブロックを含んでいる場合、コンパイラは
:exc:`SyntaxError` を送出します。

.. index::
    single: relative; import

インポートするモジュールを指定するとき、そのモジュールの絶対名(absolute name)
を指定する必要はありません。
モジュールやパッケージが他のパッケージに含まれている場合、共通のトップパッケージ
からそのパッケージ名を記述することなく相対インポートすることができます。
:keyword:`from` の後に指定されるモジュールやパッケージの先頭に複数個のドットを
付けることで、正確な名前を指定することなしに現在のパッケージ階層からいくつ
上の階層へ行くかを指定することができます。先頭のドットが1つの場合、
import をおこなっているモジュールが存在する現在のパッケージを示します。
3つのドットは2つ上のレベルを示します。
なので、 ``pkg`` パッケージの中のモジュールで ``from . import mod`` を実行すると、
``pkg.mod`` をインポートすることになります。
``pkg.subpkg1`` の中から ``from ..subpkg2 import mod`` を実行すると、
``pkg.subpkg2.mod`` をインポートします。
相対インポートの仕様は :pep:`328` に含まれています。

どのモジュールがロードされるべきかを動的に決めたいアプリケーションのために、
組み込み関数 :func:`importlib.import_module` が提供されています;


.. _future:

future 文 (future statement)
----------------------------

.. index:: pair: future; statement

:dfn:`future 文` は、将来の特定の Python のリリースで利用可能になるような構文や意味付け
を使って、特定のモジュールをコンパイルさせるための、コンパイラに対する指示句 (directive) です。 future
文は、言語仕様に非互換性がもたらされるような、将来の Python  のバージョンに容易に移行できるよう意図されています。 future
文によって、新たな機能が標準化されたリリースが出される前に、その機能をモジュール単位で使えるようにします。

.. productionlist:: *
   future_statement: "from" "__future__" "import" feature ["as" name]
                   : ("," feature ["as" name])*
                   : | "from" "__future__" "import" "(" feature ["as" name]
                   : ("," feature ["as" name])* [","] ")"

future 文は、モジュールの先頭周辺に書かなければなりません。 future 文の前に書いてよい内容は:

* モジュールのドキュメンテーション文字列(あれば)
* コメント
* 空行
* その他の future 文

です。

Python 2.6 が認識する機能は、 ``unicode_literals``, ``print_function``,
``absolute_import``, ``division``, ``generators``,
``nested_scopes``, ``with_statement`` です。 ``generators``, ``with_statement``,
``nested_scopes`` は Python 2.6 以上では常に有効なので冗長です。

future 文は、コンパイル時に特別なやり方で認識され、扱われます: 言語の中核をなす構文構成 (construct) に対する意味付けが変更されて
いる場合、変更部分はしばしば異なるコードを生成することで実現されています。新たな機能によって、(新たな予約語のような)
互換性のない新たな構文が取り入れられることさえあります。この場合、コンパイラはモジュールを別のやりかたで解析する必要が
あるかもしれません。こうしたコード生成に関する決定は、実行時まで先延ばしすることはできません。

これまでの全てのリリースにおいて、コンパイラはどの機能が定義済みかを知っており、future 文に未知の機能が含まれている場合には
コンパイル時エラーを送出します。

future 文の実行時における直接的な意味付けは、import 文と同じです。標準モジュール :mod:`__future__`
があり、これについては後で述べます。 :mod:`__future__` は、future 文が実行される際に通常の方法で import  されます。

future 文の実行時における特別な意味付けは、future 文で有効化される特定の機能によって変わります。

以下の文::

   import __future__ [as name]

には、何ら特殊な意味はないので注意してください。

これは future 文ではありません; この文は通常の import 文であり、その他の特殊な意味付けや構文的な制限はありません。

future 文の入ったモジュール :mod:`M` 内で使われている :keyword:`exec` 文、組み込み関数 :func:`compile` や
:func:`execfile` によってコンパイルされるコードは、デフォルトの設定では、 future
文に関係する新たな構文や意味付けを使うようになっています。 Python 2.2 からは、この仕様を :func:`compile` のオプション引数
で制御できるようになりました --- 詳細はこの関数に関するドキュメントを参照してください。

対話的インタプリタのプロンプトでタイプ入力した future 文は、その後のインタプリタセッション中で有効になります。インタプリタを
:option:`-i` オプションで起動して実行すべきスクリプト名を渡し、スクリプト中に future 文を入れておくと、新たな機能は
スクリプトが実行された後に開始する対話セッションで有効になります。

.. seealso::

   :pep:`236` - Back to the __future__
   __future__ 機構の原案


.. _global:

:keyword:`global` 文
====================

.. index::
   statement: global
   triple: global; name; binding

.. productionlist::
   global_stmt: "global" `identifier` ("," `identifier`)*

:keyword:`global` 文は、現在のコードブロック全体で維持される宣言文です。 :keyword:`global`
文は、列挙した識別子をグローバル変数として解釈するよう指定することを意味します。 :keyword:`global`
を使わずにグローバル変数に代入を行うことは不可能ですが、自由変数を使えばその変数をグローバルであると宣言せずにグローバル変数を参照することができます。

:keyword:`global` 文で列挙する名前は、同じコードブロック中で、プログラムテキスト上 :keyword:`global` 文より前に使っては
なりません。

:keyword:`global` 文で列挙する名前は、 :keyword:`for` ループのループ制御ターゲットや、 :keyword:`class`
定義、関数定義、 :keyword:`import` 文内で仮引数として使ってはなりません。

.. impl-detail::

   現在の実装では、後ろ二つの制限については強制していませんが、プログラムでこの緩和された仕様を乱用すべきではありません。
   将来の実装では、この制限を強制したり、暗黙のうちにプログラムの意味付けを変更したりする可能性があります。

.. index::
   statement: exec
   builtin: eval
   builtin: execfile
   builtin: compile

**プログラマのための注意点:** :keyword:`global` はパーザに対する指示句 (directive) です。
この指示句は、 :keyword:`global` 文と同時に読み込まれたコードに対してのみ適用されます。特に、 :keyword:`exec` 文内に入っている
:keyword:`global` 文は、 :keyword:`exec` 文を *含んでいる*
コードブロック内に効果を及ぼすことはなく、 :keyword:`exec` 文内に含まれているコードは、 :keyword:`exec` 文を含むコード内での
:keyword:`global` 文に影響を受けません。同様のことが、関数 :func:`eval` 、 :func:`execfile` 、および
:func:`compile` にも当てはまります。


.. _exec:

:keyword:`exec` 文
==================

.. index:: statement: exec

.. productionlist::
   exec_stmt: "exec" `or_expr` ["in" `expression` ["," `expression`]]

この文は、Python コードの動的な実行をサポートします。最初の式の値評価結果は文字列か、開かれたファイルオブジェクトか、
コードオブジェクトでなければなりません。文字列の場合、一連の Python 実行文として解析し、(構文エラーが生じない限り)
実行します。 [#]_
開かれたファイルであれば、ファイルを EOF まで読んで解析し、実行します。コードオブジェクトなら、単にこれを実行します。全ての
場合で、実行されたコードはファイル入力として有効であることが期待されます (セクション :ref:`file-input` を参照)。
:keyword:`return` と :keyword:`yield` 文は、 :keyword:`exec` 文に
渡されたコードの文脈中においても関数定義の外では使われない点に注意してください。

いずれの場合でも、オプションの部分が省略されると、コードは現在のスコープ内で実行されます。 :keyword:`in` の後ろに一つだけ
式を指定する場合、その式は辞書でなくてはならず、グローバル変数とローカル変数の両方に使われます。
これらはそれぞれグローバル変数とローカル変数として使われます。 *locals* を指定する場合は何らかのマップ型オブジェクトにせねばなりません．

.. versionchanged:: 2.4
   以前は *locals* は辞書でなければなりませんでした.

.. index::
   single: __builtins__
   module: __builtin__

:keyword:`exec` の副作用として実行されるコードで設定された変数名に対応する名前の他に、追加のキーを辞書に追加することがあります。
例えば、現在の実装では、組み込みモジュール :mod:`__builtin__`  の辞書に対する参照を、 ``__builtins__`` (!)
というキーで追加することがあります。

.. index::
   builtin: eval
   builtin: globals
   builtin: locals

**プログラマのためのヒント:** 式の動的な評価は、組み込み関数 :func:`eval` でサポートされています組み込み関数
:func:`globals` および :func:`locals` は、それぞれ現在のグローバル辞書とローカル辞書を返すので、
:keyword:`exec` に渡して使うと便利です。

.. rubric:: 注記

.. [#] パーサーは Unix スタイルの行末の慣習しか許可しないことに注意してください。
       コードをファイルから読み込む場合、Windows や Mac スタイルの改行を変換するために
       必ずユニバーサル改行モード(universal newline mode)を利用してください。
