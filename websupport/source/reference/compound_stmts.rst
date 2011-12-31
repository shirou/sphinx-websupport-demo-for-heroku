.. _compound:

***************************
複合文 (compound statement)
***************************

.. index:: pair: compound; statement

複合文には、他の文 (のグループ) が入ります; 複合文は、中に入っている他の文の実行の制御に何らかのやり方で影響を及ぼします。
一般的には、複合文は複数行にまたがって書かれますが、全部の文を一行に連ねた単純な書き方もあります。

:keyword:`if` 、 :keyword:`while` 、および :keyword:`for` 文は、
伝統的な制御フロー構成を実現します。 :keyword:`try` は例外処理および/または一連の文に対するクリーンアップコードを指定します。
関数とクラス定義もまた、構文法的には複合文です。

複合文は、一つまたはそれ以上の '節 (clause)' からなります。一つの節は、ヘッダと 'スイート (suite)' からなります。
特定の複合文を構成する節のヘッダ部分は、全て同じインデントレベルになります。各々の節ヘッダ行は一意に識別されるキーワード
から始まり、コロンで終わります。スイートは、ヘッダのコロンの後ろにセミコロンで区切られた一つまたはそれ以上の単純文を並べるか、
ヘッダ行後のインデントされた文の集まりです。後者の形式のスイートに限り、ネストされた複合文を入れることができます;
以下の文は、 :keyword:`else` 節がどの :keyword:`if` 節に属するかがはっきりしないという理由から不正になります:

.. index::
   single: clause
   single: suite

::

   if test1: if test2: print x

また、このコンテキスト中では、セミコロンはコロンよりも強い結合を表すことにも注意してください。従って、以下の例では、 :keyword:`print`
は全て実行されるか、されないかのどちらかです::

   if x < y < z: print x; print y; print z

まとめると、以下のようになります:

.. productionlist::
   compound_stmt: `if_stmt`
                : | `while_stmt`
                : | `for_stmt`
                : | `try_stmt`
                : | `with_stmt`
                : | `funcdef`
                : | `classdef`
                : | `decorated`
   suite: `stmt_list` NEWLINE | NEWLINE INDENT `statement`+ DEDENT
   statement: `stmt_list` NEWLINE | `compound_stmt`
   stmt_list: `simple_stmt` (";" `simple_stmt`)* [";"]

.. index::
   single: NEWLINE token
   single: DEDENT token
   pair: dangling; else

文は常に ``NEWLINE`` か、その後に ``DEDENT`` が続いたもので終了することに注意してください。
また、オプションの継続節は常にあるキーワードから始まり、このキーワードから複合文を開始することはできないため、曖昧さは存在しないことにも注意してください
(Python では、 'ぶら下がり(dangling) :keyword:`else`' 問題を、ネストされた :keyword:`if`
文はインデントさせること解決しています)。

以下の節における文法規則の記述方式は、明確さのために、各節を別々の行に書くようにしています。


.. _if:
.. _elif:
.. _else:

:keyword:`if` 文
================

.. index::
   statement: if
   keyword: elif
   keyword: else

:keyword:`if` 文は、条件分岐を実行するために使われます:

.. productionlist::
   if_stmt: "if" `expression` ":" `suite`
          : ( "elif" `expression` ":" `suite` )*
          : ["else" ":" `suite`]

:keyword:`if` 文は、式を一つ一つ評価してゆき、真になるまで続けて、真になった節のスイートだけを選択します (真: true と偽: false
の定義については、 :ref:`booleans` 節を参照してください); 次に、選択したスイートを実行します
(そして、 :keyword:`if` 文の他の部分は、実行や評価をされません)。
全ての式が偽になった場合、 :keyword:`else` 節があれば、そのスイートが実行されます。


.. _while:

:keyword:`while` 文
===================

.. index::
   statement: while
   pair: loop; statement
   keyword: else

:keyword:`while` 文は、式の値が真である間、実行を繰り返すために使われます:

.. productionlist::
   while_stmt: "while" `expression` ":" `suite`
             : ["else" ":" `suite`]

:keyword:`while` 文は式を繰り返し真偽評価し、真であれば最初のスイートを実行します。式が偽であれば (最初から偽になっていることも
ありえます)、 :keyword:`else` 節がある場合にはそれを実行し、ループを終了します。

.. index::
   statement: break
   statement: continue

最初のスイート内で :keyword:`break` 文が実行されると、 :keyword:`else` 節のスイートを実行することなくループを終了します。
:keyword:`continue` 文が最初のスイート内で実行されると、スイート内にある残りの文の実行をスキップして、式の真偽評価に戻ります。


.. _for:

:keyword:`for` 文
=================

.. index::
   statement: for
   pair: loop; statement
   keyword: in
   keyword: else
   pair: target; list
   object: sequence

:keyword:`for` 文は、シーケンス (文字列、タプルまたはリスト) や、その他の反復可能なオブジェクト (iterable object)
内の要素に渡って反復処理を行うために使われます:

.. productionlist::
   for_stmt: "for" `target_list` "in" `expression_list` ":" `suite`
           : ["else" ":" `suite`]

式リストは一度だけ評価されます; 結果はイテレーション可能オブジェクトにならねばなりません。 ``expression_list`` の結果に対してイテレータ
を生成し、その後、シーケンスの各要素についてインデクスの小さい順に一度だけスイートを実行します。
このときシーケンス内の要素が通常の代入規則を使ってターゲットリストに代入され、その後スイートが実行されます。全ての要素を使い切ると
(シーケンスが空の場合にはすぐに)、 :keyword:`else` 節があればそれが実行され、ループを終了します。

.. index::
   statement: break
   statement: continue

最初のスイート内で :keyword:`break` 文が実行されると、 :keyword:`else` 節のスイートを実行することなくループを終了します。
:keyword:`continue` 文が最初のスイート内で実行されると、スイート内にある残りの文の実行をスキップして、式の真偽評価に戻ります。

スイートの中では、ターゲットリスト内の変数に代入を行えます;  この代入によって、次に代入される要素に影響を及ぼすことはありません。

.. index::
   builtin: range
   pair: Pascal; language

ループが終了してもターゲットリストは削除されませんが、シーケンスが空の場合には、ループでの代入は全く行われません。ヒント: 組み込み関数
:func:`range` は、 Pascal 言語における ``for i := a to b do`` の効果をエミュレートするのに適した数列を返します;
すなわち、 ``range(3)`` はリスト ``[0, 1, 2]`` を返します。

.. note::

   .. index::
      single: loop; over mutable sequence
      single: mutable sequence; loop over

   ループ中のシーケンスの変更には微妙な問題があります (これは変更可能なシーケンス、すなわちリストで起こります)。
   どの要素が次に使われるかを追跡するために、内部的なカウンタが使われており、このカウンタは反復処理を行うごとに加算されます。
   このカウンタがシーケンスの長さに達すると、ループは終了します。このことは、スイート中でシーケンスから現在の (または以前の) 要素を
   除去すると、(次の要素のインデクスは、すでに取り扱った要素のインデクスになるために) 次の要素が飛ばされることを意味します。
   同様に、スイート中でシーケンス中の現在の要素以前に要素を挿入すると、ループ中で現在の要素が再度扱われることになります。
   こうした仕様は、厄介なバグになります。シーケンス全体に相当するスライスを使って一時的なコピーを作ると、これを避けることができます。 ::

       for x in a[:]:
           if x < 0: a.remove(x)


.. _try:
.. _except:
.. _finally:

:keyword:`try` 文
=================

.. index::
   statement: try
   keyword: except
   keyword: finally

:keyword:`try` 文は、ひとまとめの文に対して、例外処理および/またはクリーンアップコードを指定します:

.. productionlist::
   try_stmt: try1_stmt | try2_stmt
   try1_stmt: "try" ":" `suite`
            : ("except" [`expression` [("as" | ",") `target`]] ":" `suite`)+
            : ["else" ":" `suite`]
            : ["finally" ":" `suite`]
   try2_stmt: "try" ":" `suite`
            : "finally" ":" `suite`

.. versionchanged:: 2.5
   以前のバージョンの Python では、 :keyword:`try`...\ :keyword:`except`...\ :keyword:`finally`
   が機能しませんでした。 :keyword:`try`...\ :keyword:`except` は :keyword:`try`...\
   :keyword:`finally` 中でネストされなければいけません。.

:keyword:`except` 節は一つまたはそれ以上の例外ハンドラを指定します。 :keyword:`try`
節内で全く例外が起きなければ、どの例外ハンドラも実行されません。 :keyword:`try` スイート内で例外が発生すると、
例外ハンドラの検索が開始されます。この検索では、 :keyword:`except`  節を逐次調べて、発生した例外に合致するまで続けます。式を伴わない
:keyword:`except` 節を使う場合、最後に書かなければなりません; この :keyword:`except` 節は全ての例外に合致します。
式を伴う :keyword:`except` 節に対しては、式が値評価され、返されたオブジェクトが例外と "互換である (compatible)"
場合にその節が合致します。ある例外に対してオブジェクトが互換であるのは、それが例外オブジェクトのクラスかベースクラスの場合、または
例外と互換性のある要素が入ったタプルである場合、または、 (非推奨であるところの) 文字列による例外の場合は、送出された文字列そのものである場合です
(注意点として、オブジェクトのアイデンティティが一致しなければいけません。
つまり、同じ文字列オブジェクトなのであって、単なる同じ値を持つ文字列ではありません)。

例外がどの :keyword:`except` 節にも合致しなかった場合、現在のコードを囲うさらに外側、そして呼び出しスタックへと検索を続けます。  [#]_

:keyword:`except` 節のヘッダにある式を値評価するときに例外が発生すると、元々のハンドラ検索はキャンセルされ、新たな例外に対する
例外ハンドラの検索を現在の :keyword:`except` 節の外側のコードや呼び出しスタックに対して行います (:keyword:`try` 文全体が
例外を発行したかのように扱われます)。

合致する except 節が見つかると、その :keyword:`except` 節はその except 節で指定されているターゲットに代入されて、
もし存在する場合、加えて except 節スイートが実行されます。全ての except 節は実行可能なブロックを持っていなければ
なりません。このブロックの末尾に到達すると、通常は :keyword:`try` 文全体の直後に実行を継続します。(このことは、同じ例外に対してネスト
した二つの例外ハンドラが存在し、内側のハンドラ内の :keyword:`try` 節で例外が発生した場合、外側のハンドラは例外を処理しないことを意味
します。)

.. index::
   module: sys
   object: traceback
   single: exc_type (in module sys)
   single: exc_value (in module sys)
   single: exc_traceback (in module sys)

:keyword:`except` 節のスイートが実行される前に、例外に関する詳細が :mod:`sys` モジュール内の三つの変数に代入されます:
``sys.exc_type`` は、例外を示すオブジェクトを受け取ります; ``sys.exc_value`` は例外のパラメタを受け取ります;
``sys.exc_traceback`` は、プログラム上の例外が発生した位置を識別するトレースバックオブジェクト
(:ref:`types` 参照) を受け取ります。これらの詳細はまた、関数 :func:`sys.exc_info` を介して入手することもできます。この関数はタプル
``(exc_type, exc_value, exc_traceback)``  を返します。ただしこの関数に対応する変数の使用は、スレッドを使った
プログラムで安全に使えないため撤廃されています。 Python 1.5 からは、例外を処理した関数から戻るときに、以前の値 (関数呼び出し前の値)
に戻されます。

.. index::
   keyword: else
   statement: return
   statement: break
   statement: continue

オプションの :keyword:`else` 節は、実行の制御が :keyword:`try` 節の末尾に到達した場合に実行されます。 [#]_
:keyword:`else` 節内で起きた例外は、 :keyword:`else` 節に先行する :keyword:`except`
節で処理されることはありません。

.. index:: keyword: finally

:keyword:`finally` が存在する場合、これは 'クリーンアップ' ハンドラを指定しています。 :keyword:`except` や
:keyword:`else` 節を含む :keyword:`try` 節が実行されます。それらの節のいずれかで例外が発生して処理されない場合、
その例外は一時的に保存されます。 :keyword:`finally` 節が実行されます。もし保存された例外が存在する場合、それは
:keyword:`finally` 節の最後で再送出されます。 :keyword:`finally`
節で別の例外が送出されたり、 :keyword:`return` や :keyword:`break` 節が実行された場合、保存されていた
例外は失われます。例外情報は、 :keyword:`finally` 節の実行中にはプログラムで取得することができません。

.. index::
   statement: return
   statement: break
   statement: continue

:keyword:`try`...\ :keyword:`finally` 文の :keyword:`try` スイート内で
:keyword:`return` 、 :keyword:`break` 、または :keyword:`continue` 文が
実行された場合、 :keyword:`finally` 節も '抜け出る途中に (on the way out)' 実行されます。
:keyword:`finally` 節での :keyword:`continue` 文の使用は不正です。
(理由は現在の実装上の問題です -- この制限は将来解消される
かもしれません)。

.. % XXX ここは上段落と全く同じ内容で、冗長です。
.. % \keyword{finally} 節の実行中は、例外情報を取得
.. % することはできません。

例外に関するその他の情報は  :ref:`exceptions` 節にあります。また、 :keyword:`raise`
文の使用による例外の生成に関する情報は、  :ref:`raise` 節にあります。


.. _with:
.. _as:

:keyword:`with` 文
==================

.. index:: statement: with

.. versionadded:: 2.5

:keyword:`with` 文は、ブロックの実行を、コンテキストマネージャによって定義されたメソッドでラップするために使われます（
:ref:`context-managers` セクションを参照してください）。これにより、よくある  :keyword:`try`...\
:keyword:`except`...\ :keyword:`finally` 利用パターンをカプセル化して便利に再利用することができます。

.. productionlist::
   with_stmt: "with" with_item ("," with_item)* ":" `suite`
   with_item: `expression` ["as" `target`]

一つの "要素" を持つ :keyword:`with` 文の実行は以下のように進行します:

#. コンテキスト式 (:token:`with_item` で与えられた式) を評価することで、
   コンテキストマネージャを取得します。

#. コンテキストマネージャの :meth:`__enter__` メソッドが、
   後で使うためにロードされます。

#. コンテキストマネージャの :meth:`__enter__` メソッドが呼ばれます。

#. :keyword:`with` 文に ターゲットが含まれていたら、
   それに :meth:`__enter__` からの戻り値が代入されます。

   .. note::

      :keyword:`with` 文は、 :meth:`__enter__` メソッドがエラーなく終了した場合には :meth:`__exit__`
      が常に呼ばれることを保証します。ですので、もしエラーがターゲットリストへの代入中にエラーが発生した場合には、これは
      そのスイートの中で発生したエラーと同じように扱われます。
      以下のステップ 6 を参照してください。

#. スイートが実行されます。

#. コンテキストマネージャの :meth:`__exit__` メソッドが呼ばれます。もし例外がスイートを終了させる場合、その型、値、そして
   トレースバックが :meth:`__exit__` へ引数として渡されます。そうでなければ、 3 つの :const:`None` 引数が与えられます。

   スイートが例外により終了され、 :meth:`__exit__` メソッドからの
   戻り値が偽（false）ならば、例外が再送出されます。この戻り値が真（true）
   ならば例外は抑制され、実行は :keyword:`with` 文の次の文から続きます。

   もしそのスイートが例外でない何らかの理由で終了した場合、その :meth:`__exit__` からの戻り値は無視されて、実行は
   発生した終了の種類に応じた通常の位置から継続します。

複数の要素があるとき、コンテキストマネージャは複数の :keyword:`with` 文が
ネストされたかのように進行します::

   with A() as a, B() as b:
       suite

は、以下と同等です::

   with A() as a:
       with B() as b:
           suite

.. note::

   Python 2.5 では、 :keyword:`with` 文は ``with_statement`` 機能が有効にされた場合にだけ利用できます。
   Python 2.6 では常に利用できます。

.. versionchanged:: 2.7
   複数のコンテキスト式をサポートしました。

.. seealso::

   :pep:`0343` - The "with" statement
      Python の :keyword:`with` 文の仕様、背景、そして実例


.. _function:
.. _def:

関数定義
========

.. index::
   pair: function; definition
   statement: def

.. index::
   pair: function; definition
   pair: function; name
   pair: name; binding
   object: user-defined function
   object: function

関数定義は、ユーザ定義関数オブジェクトを定義します ( :ref:`types` 節参照):

.. productionlist::
   decorated: decorators (classdef | funcdef)
   decorators: `decorator`+
   decorator: "@" `dotted_name` ["(" [`argument_list` [","]] ")"] NEWLINE
   funcdef: "def" `funcname` "(" [`parameter_list`] ")" ":" `suite`
   dotted_name: `identifier` ("." `identifier`)*
   parameter_list: (`defparameter` ",")*
                 : (  "*" `identifier` [, "**" `identifier`]
                 : | "**" `identifier`
                 : | `defparameter` [","] )
   defparameter: `parameter` ["=" `expression`]
   sublist: `parameter` ("," `parameter`)* [","]
   parameter: `identifier` | "(" `sublist` ")"
   funcname: `identifier`

関数定義は実行可能な文です。関数定義を実行すると、現在のローカルな名前空間内で関数名を関数オブジェクト (関数の実行可能コードをくるむラッパ)
に束縛します。この関数オブジェクトには、関数が呼び出された際に使われるグローバルな名前空間として、現在のグローバルな名前空間への参照が入っています。

関数定義は関数本体を実行しません; 関数本体は関数が呼び出された時にのみ実行されます。 [#]_

.. index::
   statement: @

関数定義は一つ以上のデコレータ (:term:`decorator`) 式でラップできます。
デコレータ式は関数を定義するとき、関数定義の入っているスコープで評価されます。
その結果は、関数オブジェクトを唯一の引数にとる呼び出し可能オブジェクトで
なければなりません。関数オブジェクトの代わりに、返された値が関数名に
束縛されます。複数のデコレータはネストして適用されます。
例えば、以下のようなコード::

   @f1(arg)
   @f2
   def func(): pass

は、 ::

   def func(): pass
   func = f1(arg)(f2(func))

と同じです。

.. index:: triple: default; parameter; value

一つ以上のトップレベルのパラメタに  *parameter* ``=`` *expression* の形式がある場合、関数は "デフォルトのパラメタ値
(default parameter values)" を持つといいます。デフォルト値を伴うパラメタに対しては、関数呼び出しの
際に対応するパラメタが省略されると、パラメタの値はデフォルト値で置き換えられます。あるパラメタがデフォルト値を持つ場合、それ以後の
パラメタは全てデフォルト値を持たなければなりません --- これは文法的には表現されていない構文上の制限です。

**デフォルトパラメタ値は関数定義を実行する際に値評価されます。** これは、デフォルトパラメタの式は関数を定義するときにただ一度だけ評価され、同じ
"計算済みの" 値が全ての呼び出しで使われることを意味します。デフォルトパラメタ値がリストや辞書のような変更可能なオブジェクトである
場合、この使用を理解しておくことは特に重要です: 関数でこのオブジェクトを (例えばリストに要素を追加して) 変更すると、実際のデフォルト
値が変更されてしまいます。一般には、これは意図しない動作です。このような動作を避けるには、デフォルト値に ``None`` を使い、
この値を関数本体の中で明示的にテストします。例えば以下のようにします::

   def whats_on_the_telly(penguin=None):
       if penguin is None:
           penguin = []
       penguin.append("property of the zoo")
       return penguin

.. index::
   statement: *
   statement: **

関数呼び出しの意味付けに関する詳細は、 :ref:`calls` 節で述べられています。関数呼び出しを行うと、パラメタリストに記述された全てのパラメタ
に対して、固定引数、キーワード引数、デフォルト引数のいずれかから値を代入します。"``*identifier``" 形式が存在する場合、
余った固定引数を受け取るタプルに初期化されます。この変数のデフォルト値は空のタプルです。"``**identifier``" 形式が
存在する場合、余ったキーワード引数を受け取るタプルに初期化されます。デフォルト値は空の辞書です。

.. index:: pair: lambda; form

式で直接使うために、無名関数 (名前に束縛されていない関数) を作成することも可能です。無名関数の作成には、 :ref:`lambda` 節で記述されている
ラムダ形式 (lambda form) を使います。ラムダ形式は、単純化された関数定義を行うための略記法にすぎません; ":keyword:`def`"
文で定義された関数は、ラムダ形式で定義された関数と全く同様に引渡したり、他の名前に代入したりできます。実際には、":keyword:`def`"
形式は複数の式を実行できるという点でより強力です。

**プログラマのための注釈:** 関数は一級の (first-class) オブジェクトです。関数定義内で"``def``"
形式を実行すると、戻り値として返したり引き渡したりできるローカルな関数を定義します。ネストされた関数内で自由変数を使うと、 :keyword:`def`
文の入っている関数のローカル変数にアクセスすることができます。詳細は  :ref:`naming`  節を参照してください。


.. _class:

クラス定義
==========

.. index::
   object: class
   statement: class
   pair: class; definition
   pair: class; name
   pair: name; binding
   pair: execution; frame
   single: inheritance
   single: docstring


クラス定義は、クラスオブジェクトを定義します ( :ref:`types` 節参照):

.. productionlist::
   classdef: "class" `classname` [`inheritance`] ":" `suite`
   inheritance: "(" [`expression_list`] ")"
   classname: `identifier`

クラス定義は実行可能な文です。クラス定義では、まず継承リストがあればそれを評価します。
継承リストの各要素の値評価結果はクラスオブジェクトか、
サブクラス可能なクラス型でなければなりません。次にクラスのスイートが新たな実行フレーム内で、
新たなローカル名前空間と元々のグローバル名前空間を使って実行されます
(:ref:`naming` 節を参照してください)。
(通常、スイートには関数定義のみが含まれます) クラスのスイートを実行し終えると、実行フレームは無視されますが、ローカルな
名前空間は保存されます。次に、基底クラスの継承リストを使ってクラスオブジェクトが生成され、ローカルな名前空間を属性値辞書
として保存します。最後に、もとのローカルな名前空間において、クラス名がこのクラスオブジェクトに束縛されます。

**プログラマのための注釈:** クラス定義内で定義された変数はクラス変数です; クラス変数は全てのインスタンス間で共有されます。
インスタンス変数を作成するには、メソッドの中で ``self.name = value`` でセットできます。クラス変数もインスタンス変数も
"``self.name``" 表記でアクセスすることができます。この表記でアクセスする場合、インスタンス変数は同名のクラス変数を隠蔽します。
クラス変数は、インスタンス変数のデフォルト値として使えますが、変更可能な値をそこに使うと予期せぬ結果につながります。
新スタイルクラス(:term:`new-style class`)では、デスクリプタを使ってインスタンス変数の振舞いを変更できます。

クラス定義は、関数定義と同じように、1つ以上のデコレータ(:term:`decorator`)式でラップすることができます。
デコレータ式の評価規則は関数と同じです。結果はクラスオブジェクトでなければならず、
それがクラス名に束縛されます。

.. rubric:: 注記

.. [#] 例外は、例外を打ち消す :keyword:`finally` 節が無い場合にのみ呼び出しスタックへ伝わります。

.. [#] 現在、制御が "末尾に到達する" のは、例外が発生したり、 :keyword:`return`,
   :keyword:`continue`, または :keyword:`break` 文が実行される場合を除きます。

.. [#] 関数の本体の最初の文として現われる文字列リテラルは、その関数の ``__doc__``
   属性に変換され、その関数のドキュメンテーション文字列(:term:`docstring`)
   になります。

.. [#] クラスの本体の最初の文として現われる文字列リテラルは、その名前空間の ``__doc__``
   要素となり、そのクラスのドキュメンテーション文字列(:term:`docstring`)になります。
