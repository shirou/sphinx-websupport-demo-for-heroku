******************************
  関数型プログラミング HOWTO
******************************

:Author: A. M. Kuchling
:Release: 0.31

この文書では、関数型スタイルでプログラムを実装するのにピッタリな Python
の機能を見てまわることにしましょう。まず関数型プログラミングという概念を
紹介したあと、 :term:`iterator` や :term:`generator` のような言語機能、
および :mod:`itertools` や :mod:`functools` といった関連するライブラリ
モジュールを見ることにします。


はじめに
========

この章は関数型プログラミングの基本概念を説明します; Python
の言語機能についてだけ知りたい人は、次の章まで飛ばしてください。

プログラミング言語とは問題を分解するものですが、
各言語がサポートする分解方法にはいくつかの種類があります:

* ほとんどのプログラミング言語は **手続き型** です: プログラムは、
  入力に対して行うべきことをコンピュータに教える指示リストとなります。
  C, Pascal, さらには Unix シェルまでもが手続き型言語に入ります。

* **宣言型** 言語で書くのは、解くべき問題を説明する仕様書であって、それを
  効率的に計算処理する方法を見付けるのは言語実装の役目です。SQL はおそらく
  一番よく知られた宣言型言語です; SQL のクエリは取得したいデータセットを
  説明しているだけで、テーブルを走査するかインデックスを使うか、
  どのサブクローズから実行するか等々を決めるのは SQL エンジンなのです。

* **オブジェクト指向** プログラムはオブジェクトの集まりを操作します。
  オブジェクトには内部状態があり、その状態を調べたり色々と変更したりするための
  メソッドがあります。Smalltalk や Java はオブジェクト指向言語です。
  C++ と Python はオブジェクト指向プログラミングをサポートしていますが、
  関連する機能を使わなくても構わないようになっています。

* **関数型** プログラミングは問題をいくつかの関数にわけて考えます。
  理想的に言うと、関数は入力を受けて出力を吐くだけで、同じ入力に対して
  異なる出力をするような内部状態を一切持ちません。有名な関数型言語には
  ML 一家 (Standard ML, OCaml 等々) と Haskell があります。

設計者が特定のアプローチを強調することにした言語もありますが、
そうすると大抵は、別のアプローチを使うプログラムを書きにくくなります。
複数のアプローチに対応した言語もあり、Lisp, C++, Python はそうした
マルチパラダイム言語です; この中のどれを使っても、基本的に手続き型な、または
基本的にオブジェクト指向な、とか、基本的に関数型なプログラムやライブラリを
書くことができます。大きなプログラムでは、各部で別々のアプローチを使って書く
ことがあるかもしれません; GUI はオブジェクト指向で、でも処理ロジックは
手続き型や関数型で、といったようにです。

関数型プログラムでは、入力は一連の関数を通って流れていきます。それぞれの関数は
入力に何らかの作業をして出力します。関数型スタイルにおいては、内部状態を
変えてしまったり、返り値に現れない変更をしたりといった副作用のある関数は
やめるように言われています。副作用のまったくない関数は **純粋関数型** である
とされます。副作用をなくすということは、プログラムの実行中に順次変化していく
データ構造を持たない、つまり各関数の出力はその入力にしか影響を受けてはいけない
ということです。

この純粋性を守る面で非常に厳しい言語もあり、そうした言語には ``a=3`` や
``c = a + b`` といった代入文さえありません。しかし副作用を完全になくすのは
難しいもので、たとえば画面表示やディスクファイルへの書き込みも副作用なのです。
Python で言うと、たとえば ``print`` 文や ``time.sleep(1)`` はどちらも
意味ある値を返しません; ただ画面にテキストを送ったり動作を 1 秒止めたり
といった副作用のためだけに呼ばれるのです。

関数型スタイルで書いた Python プログラムはふつう、I/O や代入を完全になくす
といった極端なところまでは行かずに、関数型っぽく見えるインタフェースを
提供しつつも内部では非関数型の機能を使います。たとえば、関数内で
ローカル変数の代入は使いますが、グローバル変数は変更せず、他の副作用も
ないように実装するのです。

関数型プログラミングはオブジェクト指向プログラミングの反対と考えることも
できます。オブジェクト指向において、オブジェクトは内部状態とそれを変更する
メソッドコールの入ったカプセルであり、プログラムはその状態を適正に変化
させていく手順です。一方で、関数型プログラミングは可能なかぎり状態の変更を
避け、関数どうしの間を流れるデータだけを扱おうとします。Python ではこの
二つのアプローチを結び合わせることができます。アプリケーション内の
オブジェクト (メール、トランザクション、等々) を表現したインスタンスを、
関数が受け渡しするようにするのです。

関数型デザインは、わけのわからない制約に見えるかもしれません。
どうしてオブジェクトも副作用もないほうが良いのでしょうか。
実は、関数型スタイルには理論と実践に基づく次の利点があるのです:

* 形式的証明可能性
* モジュラー性
* 結合性
* デバグやテストの簡単さ


形式的証明可能性
----------------

理論面の利点としては、プログラムが正しいことの数学的証明を
他より簡単に構築できるという点があります。

研究者たちは長いあいだ、プログラムが正しいことを数学的に証明する方法の
発見に血道をあげてきました。これは、色々な入力でテストして出力が正しかった
からまあ正しいだろう、と結論するのとも違いますし、ソースコードを読んで
「間違いはなさそうだ」と言うのとも別の話です; 目指すのは、出現しうる入力
すべてに対してプログラムが正しい結果を出すことの厳密な証明なのです。

プログラムを証明するために使われているのは **不変式** を書き出していく
というテクニックで、不変式とは入力データやプログラム変数のうち常に真である
性質のことです。コードの一行一行で、 **実行前** の不変式 X と Y が真なら
**実行後に** ちょっと違う不変式 X' と Y' が真になることを示していき、
これをプログラムの終わりまで続けるわけです。すると最終的な不変式は
プログラムの出力に合った条件になっているはずです。

関数型プログラミングが代入を嫌うのは、この不変式テクニックでは代入を
扱いにくいからです; 代入は、それまで真だった不変式を壊しておいて、
自分は次の行に伝えてゆける不変式を生み出さないことがあるのです。

残念ながら、プログラムの証明はだいたい実際的でもありませんし、Python
ソフトウェアにも関係ありません。本当に簡単なプログラムでも、証明には
数ページにわたる論文が必要なのです; ある程度の複雑なプログラムではもう
尋常でない長さになってしまうので、日常で使っているプログラム (Python
インタプリタ、XML パーサ、ウェブブラウザ) はほとんど、あるいはすべて、
正しさを証明するのは不可能でしょう。仮に証明を書き出したり生成したりしても、
その証明を検証するための疑いが残ります; 証明に間違いがあるかもしれず、
その場合は証明したと自分で勝手に思い込んでいただけになるのです。


モジュラー性
------------

より実用的には、関数型プログラミングをすると問題を細かく切り分けることになる
という利点があります。結果としてプログラムはモジュラー化されます。
複雑な変形を施す大きな関数を書くより、一つのことに絞ってそれだけをする
小さな関数のほうが書きやすいものです。それに、小さいほうが
読むのもエラーをチェックするのも簡単です。


デバグやテストの簡単さ
----------------------

テストやデバグも関数型プログラムなら簡単です。

関数が一般的に小さくて明確に意味付けされているので、デバグ方法は単純です。
プログラムが正しく動かないときには、関数ひとつひとつがデータの正しさを
チェックするポイントになるので、それぞれの時点における入力と出力を
見ていけば、バグの原因となる関数を素早く切り出すことができるのです。

ひとつひとつの関数がユニットテストの対象になり得るわけですから、
テストも簡単です。関数はシステムの状態に依存しませんので、テストの実行前に
そうした状態を再現する必要はありません; 単に適切な入力を合成して、
出力が期待どおりかどうかチェックするだけで良いのです。


結合性
------

関数型スタイルのプログラムを作っていると、色々な入力や出力のために
色々な関数を書くことになります。仕方なく特定のアプリケーションに特化した関数を
書くこともあるでしょうけれど、広範なプログラムに使える関数もあることでしょう。
たとえば、ディレクトリ名を受け取ってその中の XML ファイル一覧を返す関数や、
ファイル名を受け取って内容を返す関数などは、多様な場面に適用できそうです。

時たつうちに自分の特製ライブラリやユーティリティが充実してくると、
新しいプログラムも、既存の関数を調整して少し今回に特化した関数を書くだけで
組み立てられるようになります。


イテレータ
==========

まずは関数型スタイルのプログラムを書く際の基礎となる重要な
Python 機能から見ていきましょう: イテレータです。

イテレータは連続データを表現するオブジェクトです; このオブジェクトは
一度に一つの要素ずつデータを返します。Python のイテレータは ``next()``
という、引数を取らず次の要素を返すメソッドを必ずサポートしています。
データストリームに要素が残っていない場合、 ``next()`` は必ず
``StopIteration`` 例外を出します。ただ、イテレータの長さは有限である
必要はありません; 無限のストリームを出すイテレータを書くというのも
まったく理に適ったことです。

ビルトインの :func:`iter` 関数は任意のオブジェクトを受けて、
その中身や要素を返すイテレータを返そうとします。引数のオブジェクトが
イテレータを作れないときは :exc:`TypeError` を投げます。Python の
ビルトインなデータ型にもいくつかイテレータ化のできるものがあり、
中でもよく使われるのはリストと辞書です。イテレータを作れる
オブジェクトは **イテラブル** オブジェクトと呼ばれます。

手を動かしてイテレータ化の実験をしてみましょう:

    >>> L = [1,2,3]
    >>> it = iter(L)
    >>> print it
    <...iterator object at ...>
    >>> it.next()
    1
    >>> it.next()
    2
    >>> it.next()
    3
    >>> it.next()
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    StopIteration
    >>>

Python は色々な文脈でイテラブルなオブジェクトを期待しますが、
最も重要なのは ``for`` 文です。 ``for X in Y`` という文の Y は、
イテレータか、あるいは ``iter()`` でイテレータを作れるオブジェクト
である必要があります。次の二つは同じ意味になります::

    for i in iter(obj):
        print i

    for i in obj:
        print i

イテレータは :func:`list` や :func:`tuple` といったコンストラクタ関数
を使ってリストやタプルに具現化することができます:

    >>> L = [1,2,3]
    >>> iterator = iter(L)
    >>> t = tuple(iterator)
    >>> t
    (1, 2, 3)

シーケンスのアンパックもイテレータに対応しています: イテレータが N 個の要素を
返すということが事前にわかっていれば、N-タプルにアンパックすることができます:

    >>> L = [1,2,3]
    >>> iterator = iter(L)
    >>> a,b,c = iterator
    >>> a,b,c
    (1, 2, 3)

ビルトイン関数の :func:`max` や :func:`min` なども、イテレータ一つだけを引数に
取って最大・最小の要素を返すことができます。 ``in`` や ``not in`` 演算子も
イテレータに対応しています: ``X in イテレータ`` は、そのイテレータから返る
ストリームに X があれば真です。ですからイテレータが無限長だと、当然ながら問題
に直面します; ``max()``, ``min()``, ``not in`` はいつまでも戻って来ませんし、
要素 X がストリームに出てこなければ ``in`` オペレータも戻りません。

イテレータは次に進むことしかできませんのでご注意ください;
前の要素を手に入れたり、イテレータをリセットしたり、コピーを作ったり
する方法はありません。イテレータがオブジェクトとしてそうした追加機能を
持つことはできますが、プロトコルでは ``next()`` メソッドのことしか
指定されていません。ですから関数はイテレータの出力を使い尽くして
しまうかもしれませんし、同じストリームに何か別のことをする
必要があるなら新しいイテレータを作らなくてはいけません。


イテレータ対応のデータ型
------------------------

リストやタプルがイテレータに対応している方法については既に見ましたが、
実のところ Python のシーケンス型はどれでも、たとえば文字列なども、
自動でイテレータ生成に対応しています。

辞書に対して :func:`iter` すると、
辞書のキーでループを回すイテレータが返されます:

.. not a doctest since dict ordering varies across Pythons

::

    >>> m = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    ...      'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    >>> for key in m:
    ...     print key, m[key]
    Mar 3
    Feb 2
    Aug 8
    Sep 9
    Apr 4
    Jun 6
    Jul 7
    Jan 1
    May 5
    Nov 11
    Dec 12
    Oct 10

順番は基本的にランダムであることに注目してください。
これは辞書内オブジェクトのハッシュの順番になっているからです。

辞書は :func:`iter` を適用するとキーでループを回しますが、辞書には他の
イテレータを返すメソッドもあります。明示的にキー、値、あるいはキーと値のペアで
イテレートしたければ、 ``iterkeys()``, ``itervalues()``, ``iteritems()``
というメソッドでイテレータを作ることができます。

逆に :func:`dict` コンストラクタは、有限な ``(キー, 値)`` タプルのストリーム
を返すイテレータを受け入れることができます:

    >>> L = [('Italy', 'Rome'), ('France', 'Paris'), ('US', 'Washington DC')]
    >>> dict(iter(L))
    {'Italy': 'Rome', 'US': 'Washington DC', 'France': 'Paris'}

ファイルも、最後の行まで ``readline()`` メソッドを呼んでいくことで
イテレータ化に対応しています。つまりこうやってファイルの各行を
読んでいくことができるわけです::

    for line in file:
        # 一行ごとに何かをする
        ...

セットはイテラブルを受け取れますし、
そのセットの要素でイテレートすることもできます::

    S = set((2, 3, 5, 7, 11, 13))
    for i in S:
        print i



ジェネレータ式とリスト内包表記
==============================

イテレータの出力に対してよく使う操作トップ 2 は、(1) ひとつずつ全要素に
操作を実行する、および (2) 条件に合う要素でサブセットを作る、です。たとえば
文字列のリストなら、各行のうしろに付いた邪魔なホワイトスペースを削りたい
とか、特定の文字列を含む部分をピックアップしたいなどと思うかもしれません。

リスト内包表記とジェネレータ式 (略して「listcomp」と「genexp」) は、
そうした操作向けの簡潔な表記方法です。これは関数型プログラミング言語
Haskell (http://www.haskell.org) にインスパイアされました。
文字列のストリームからホワイトスペースをすべて削るのは次のコードでできます::

    line_list = ['  line 1\n', 'line 2  \n', ...]

    # ジェネレータ式 -- イテレータを返す
    stripped_iter = (line.strip() for line in line_list)

    # リスト内包表記 -- リストを返す
    stripped_list = [line.strip() for line in line_list]

特定の要素だけを選び出すのは ``if`` 条件式を付けることで可能です::

    stripped_list = [line.strip() for line in line_list
                     if line != ""]

リスト内包表記を使うと Python リストが返って来ます; ``stripped_list`` は
実行結果の行が入ったリストであって、イテレータではありません。ジェネレータ
式はイテレータを返し、これだと必要に応じてだけ値を算出しますので、
すべての値を一度に出す必要がありません。つまりリスト内包表記のほうは、
無限長ストリームや膨大なデータを返すようなイテレータを扱う際には、
あまり役に立たないということです。そういった状況では
ジェネレータ式のほうが好ましいと言えます。

ジェネレータ式は丸括弧 "()" で囲まれ、リスト内包表記は
角括弧 "[]" で囲まれます。ジェネレータ式の形式は次のとおりです::

    ( expression for expr in sequence1
                 if condition1
                 for expr2 in sequence2
                 if condition2
                 for expr3 in sequence3 ...
                 if condition3
                 for exprN in sequenceN
                 if conditionN )

リスト内包表記も、外側の括弧が違うだけ (丸ではなく角括弧) で、あとは同じです。

生成される出力は ``expression`` 部分の値を要素として並べたものになります。
``if`` 節はすべて、なくても大丈夫です; あれば ``condition`` が真のときだけ
``expression`` が評価されて出力に追加されます。

ジェネレータ式は常に括弧の中に書かなければなりませんが、
関数コールの目印になっている括弧でも大丈夫です。
関数にすぐ渡すイテレータを作りたければこう書けるのです::

    obj_total = sum(obj.count for obj in list_all_objects())

``for...in`` 節は複数つなげられますが、どれにも、イテレートするための
シーケンスが含まれています。それらのシーケンスは並行して **ではなく** 、
左から右へ順番にイテレートされるので、長さが同じである必要はありません。
``sequence1`` の各要素ごとに毎回最初から ``sequence2`` をループで回すのです。
その後 ``sequence1`` と ``sequence2`` から出た要素ペアごとに、
``sequence3`` でループします。

別の書き方をすると、リスト内包表記やジェネレータ式は次の
Python コードと同じ意味になります::

    for expr1 in sequence1:
        if not (condition1):
            continue   # この要素は飛ばす
        for expr2 in sequence2:
            if not (condition2):
                continue    # この要素は飛ばす
            ...
            for exprN in sequenceN:
                 if not (conditionN):
                     continue   # この要素は飛ばす

                 # expression の値を出力する。

つまり、複数の ``for...in`` 節があって ``if`` がないときの最
終出力は、長さが各シーケンス長の積に等しくなるということです。
長さ 3 のリスト二つなら、出力リストの長さは 9 要素です:

.. doctest::
    :options: +NORMALIZE_WHITESPACE

    >>> seq1 = 'abc'
    >>> seq2 = (1,2,3)
    >>> [(x,y) for x in seq1 for y in seq2]
    [('a', 1), ('a', 2), ('a', 3),
     ('b', 1), ('b', 2), ('b', 3),
     ('c', 1), ('c', 2), ('c', 3)]

Python の文法に曖昧さを紛れ込ませないように、 ``expression``
でタプルを作るなら括弧で囲わなくてはなりません。下にあるリス
ト内包表記で、最初のは構文エラーですが、二番目は有効です::

    # Syntax error
    [ x,y for x in seq1 for y in seq2]
    # Correct
    [ (x,y) for x in seq1 for y in seq2]


ジェネレータ
============

ジェネレータは、イテレータを書く作業を簡単にする、特殊な関数です。
標準的な関数は値を計算して返しますが、ジェネレータが返すのは、
一連の値を返すイテレータです。

Python や C の標準的な関数コールについては、よくご存じに違いありません。
関数を呼ぶと、ローカル変数を作るプライベートな名前空間ができますね。
その関数が ``return`` 文まで来ると、ローカル変数が破壊されてから、返り値が
呼び出し元に返ります。次に同じ関数をもう一度呼ぶと、新しいプライベート
名前空間に新規のローカル変数が作られるのです。しかし、関数を出るときに
ローカル変数を捨てなければどうなるでしょうか。その出ていったところから
関数を続行できたとしたら、どうでしょう。これこそジェネレータが提供する
機能です; すなわち、ジェネレータは続行できる関数と考えることができます。

ごく単純なジェネレータ関数の例がこちらにあります:

.. testcode::

    def generate_ints(N):
        for i in range(N):
            yield i

``yield`` キーワードを含む関数はすべてジェネレータ関数です;
Python の :term:`bytecode` コンパイラがこれを検出して、特別な方法で
コンパイルしてくれるのです。

ジェネレータ関数は、呼ばれたときに一回だけ値を返すのではなく、イテレータ
プロトコルに対応したオブジェクトを返します。上の例で ``yield`` を実行したとき、
ジェネレータは ``return`` 文のようにして ``i`` の値を出力します。
``yield`` と ``return`` 文の大きな違いは、 ``yield`` に到達した段階で
ジェネレータの実行状態が一時停止になって、ローカル変数が保存される点です。
次回そのジェネレータの ``.next()`` を呼ぶと、そこから関数が実行を再開します。

上記 ``generate_ints()`` ジェネレータの使用例はこちらです:

    >>> gen = generate_ints(3)
    >>> gen
    <generator object generate_ints at ...>
    >>> gen.next()
    0
    >>> gen.next()
    1
    >>> gen.next()
    2
    >>> gen.next()
    Traceback (most recent call last):
      File "stdin", line 1, in ?
      File "stdin", line 2, in generate_ints
    StopIteration

同じく ``for i in generate_ints(5)`` や ``a,b,c = generate_ints(3)``
といった書き方もできます。

ジェネレータ関数内で ``return`` 文は、引数を付けずに、処理の終わりを
知らせるためにだけ使うことができます; ``return`` を実行したあとは、
もうそのジェネレータが値を返すことはできません。
ジェネレータ関数の中では、 ``return 5`` などと値を付けた ``return``
は構文エラーです。ジェネレータの出力が終わったことを示すには、
ほかにも、手動で ``StopIteration`` を投げてもいいですし、
関数の最後まで実行するだけでも同じことになります。

自分でクラスを書いて、ジェネレータで言うところのローカル変数を
インスタンス変数として全部保管しておけば、同じ効果を得ることは可能です。
たとえば整数のリストを返すのは、 ``self.count`` を 0 にして、
``next()`` メソッドが ``self.count`` をインクリメントして返すように
すればできます。しかしながら、ある程度複雑なジェネレータになってくると、
同じことをするクラスを書くのは格段にややこしいことになります。

Python のライブラリに含まれているテストスイート ``test_generators.py`` には、
ほかにも興味深い例が数多く入っています。これは二分木の通りがけ順 (in-order) 探索
を再帰で実装したジェネレータです。 ::

    # A recursive generator that generates Tree leaves in in-order.
    def inorder(t):
        if t:
            for x in inorder(t.left):
                yield x

            yield t.label

            for x in inorder(t.right):
                yield x

ほかにも ``test_generators.py`` には、N-Queens 問題 (N×N コマのチェス盤に、
互いに攻撃できないような配置で N 個のクイーンを置く) やナイト・ツアー (N×N
盤の全コマをナイトが一度ずつ通るような経路を探す) の解を出す例が入っています。


ジェネレータに値を渡す
----------------------

Python 2.4 までのジェネレータは出力することしかできませんでした。
ジェネレータのコードを実行してイテレータを作ってしまったあとで、
その関数を再開するときに新しい情報を渡す手段はなかったのです。
ジェネレータがグローバル変数を見るようにしたり、ミュータブルな
オブジェクトを渡しておいて呼び出し元であとからそれを変更したり、
といったハックは可能でしたが、どれもゴチャゴチャしていますね。

Python 2.5 で、ジェネレータに値を渡す簡単な手段ができました。
:keyword:`yield` が、変数に代入したり演算したりできる値を返す
式になったのです::

    val = (yield i)

上のように、返り値で何かをするときは ``yield`` 式の前後に **必ず**
括弧を付けるようお勧めします。括弧は常に必要なわけではありませんが、
どんなとき付けなくて良いのかを覚えておくより、
いつも付けておくほうが楽ですから。

(PEP 342 がその規則を正確に説明していますが、それによると
``yield``-式は、代入式で右辺のトップレベルにあるとき以外はいつも
括弧を付ける必要があります。つまり ``val = yield i`` とは書けますが、
``val = (yield i) + 12`` のように演算子があるときは
括弧を使わなくてはいけません。)

ジェネレータに値を送るには ``send(値)`` メソッドを呼びます。
するとジェネレータのコードが実行を再開し、 ``yield`` 式が
その値を返すのです。ふつうの ``next()`` メソッドを呼ぶと、
``yield`` は ``None`` を返します。

下にあるのは 1 ずつ増える単純なカウンタですが、内部カウンタ
の値を変更することができるようになっています。

.. testcode::

    def counter (maximum):
        i = 0
        while i < maximum:
            val = (yield i)
            # 値が提供されていればカウンタを変更する
            if val is not None:
                i = val
            else:
                i += 1

そしてカウンタ変更の例がこちらです:

    >>> it = counter(10)
    >>> print it.next()
    0
    >>> print it.next()
    1
    >>> print it.send(8)
    8
    >>> print it.next()
    9
    >>> print it.next()
    Traceback (most recent call last):
      File ``t.py'', line 15, in ?
        print it.next()
    StopIteration

``yield`` が ``None`` を返すことはよくあるのですから、そうなっていないか
どうか必ずチェックしておくべきです。ジェネレータ関数を再開するために使う
メソッドが ``send()`` しかないのだと確定してるのでない限り、式の値を
そのまま使ってはいけません。

ジェネレータには、 ``send()`` のほかにも新しいメソッドが二つあります:

* ``throw(type, value=None, traceback=None)`` はジェネレータ内で例外を
  投げるために使います; その例外はジェネレータの実行が停止したところの
  ``yield`` 式によって投げられます。

* ``close()`` はジェネレータ内で :exc:`GeneratorExit` 例外を投げて、
  イテレートを終了させます。この例外を受け取ったジェネレータのコードは
  :exc:`GeneratorExit` か :exc:`StopIteration` を投げなくてはいけません;
  この例外を捕捉して何かほかのことをしようとするのは規則違反であり、
  :exc:`RuntimeError` を引き起こします。 ``close()`` はジェネレータが GC
  されるときにも呼ばれます。

  :exc:`GeneratorExit` が起こったときにクリーンアップ作業をする必要が
  あるなら、 :exc:`GeneratorExit` を捕捉するのではなく
  ``try: ... finaly:`` するようお勧めします。

これらの変更の合わせ技で、ジェネレータは情報の一方的な生産者から、
生産者かつ消費者という存在に変貌を遂げたのです。

ジェネレータは **コルーチン** という、より一般化された形式のサブルーチン
にもなります。サブルーチンは一カ所 (関数の冒頭) から入って別の一カ所
(``return`` 文) から出るだけですが、コルーチンはいろいろな場所
(``yield`` 文) から入ったり出たり再開したりできるのです。


ビルトイン関数
==============

よくイテレータと一緒に使うビルトイン関数について、もっと詳しく見ていきましょう。

Python のビルトイン関数 :func:`map` と :func:`filter` は少し
時代遅れになっています; 機能がリスト内包表記と重複していて、
イテレータではなくリストそのものを返します。

``map(f, iterA, iterB, ...)`` は
``f(iterA[0], iterB[0]), f(iterA[1], iterB[1]), f(iterA[2], iterB[2]), ...``
のリストを返します。

    >>> def upper(s):
    ...     return s.upper()

    >>> map(upper, ['sentence', 'fragment'])
    ['SENTENCE', 'FRAGMENT']

    >>> [upper(s) for s in ['sentence', 'fragment']]
    ['SENTENCE', 'FRAGMENT']

上にあるように、リスト内包表記でも同じ結果を得ることができます。
:func:`itertools.imap` 関数も同じことをしてくれますが、
無限長イテレータまで扱うことができます; これについてはあとから
:mod:`itertools` モジュールの章で論じましょう。

``filter(predicate, iter)`` は条件に合う要素すべてのリストを
返しますので、同様にリスト内包表記で再現できます。 **predicate**
の部分には、条件が合うと真値を返す関数を入れてください;
:func:`filter` で使うには、その関数が取る引数は一つだけ
でなくてはいけません。

    >>> def is_even(x):
    ...     return (x % 2) == 0

    >>> filter(is_even, range(10))
    [0, 2, 4, 6, 8]

これはリスト内包表記でも書けます:

    >>> [x for x in range(10) if is_even(x)]
    [0, 2, 4, 6, 8]

:func:`filter` も :mod:`itertools` モジュールに同等品があり、その
:func:`itertools.ifilter` はイテレータを返すので、
:func:`itertools.imap` と同様、無限長シーケンスまで扱えます。

``reduce(func, iter, [initial_value])`` はイテラブルの要素に対して次々に
演算を実行していった最終結果を出すもので、それゆえ無限長イテラブルには
適用できませんので、 :mod:`itertools` モジュールに同等品がありません。
``func`` には、要素を二つ取って値を一つ返す関数が入ります。
:func:`reduce` はイテレータが返す最初の二要素 A と B を取って
``func(A, B)`` を出します。それから三番目の要素 C を要求して
``func(func(A, B), C)`` を算出すると、その結果をさらに四番目の要素と
組み合わせて……ということをイテラブルが尽きるまで続けるのです。
もしイテラブルが一つも値を返さなければ :exc:`TypeError` が出ます。
初期値 ``initial_value`` があるときには、
``func(initial_value, A)`` がスタート地点として実行されます。

    >>> import operator
    >>> reduce(operator.concat, ['A', 'BB', 'C'])
    'ABBC'
    >>> reduce(operator.concat, [])
    Traceback (most recent call last):
      ...
    TypeError: reduce() of empty sequence with no initial value
    >>> reduce(operator.mul, [1,2,3], 1)
    6
    >>> reduce(operator.mul, [], 1)
    1

:func:`operator.add` を :func:`reduce` で使うと、イテラブルの全要素を
合計することになります。これは使用頻度が高いので、そのためだけの
:func:`sum` というビルトインがあるほどです:

    >>> reduce(operator.add, [1,2,3,4], 0)
    10
    >>> sum([1,2,3,4])
    10
    >>> sum([])
    0

とはいえ、多くの場合 :func:`reduce` を使うよりは単に
:keyword:`for` ループを書いたほうがわかりやすくなるかもしれません::

    # こう書く代わりに
    product = reduce(operator.mul, [1,2,3], 1)

    # こう書けます
    product = 1
    for i in [1,2,3]:
        product *= i


``enumerate(iter)`` はイテラブルの要素を数え上げて、それぞれの
番号と要素の入った 2-タプルを返します。

    >>> for item in enumerate(['subject', 'verb', 'object']):
    ...     print item
    (0, 'subject')
    (1, 'verb')
    (2, 'object')

:func:`enumerate` はよく、リストに対してループさせて、
条件に合う所に印を付けていくときに使われます::

    f = open('data.txt', 'r')
    for i, line in enumerate(f):
        if line.strip() == '':
            print 'Blank line at line #%i' % i

``sorted(iterable, [cmp=None], [key=None], [reverse=false])`` は
イテラブルの要素をすべて集めたリストを作り、ソートして返します。
引数 ``cmp``, ``key``, ``reverse`` は、リストの ``.sort()``
メソッドにそのまま渡されます。 ::

    >>> import random
    >>> # 0 以上 10000 未満の乱数を 8 個生成
    >>> rand_list = random.sample(range(10000), 8)
    >>> rand_list
    [769, 7953, 9828, 6431, 8442, 9878, 6213, 2207]
    >>> sorted(rand_list)
    [769, 2207, 6213, 6431, 7953, 8442, 9828, 9878]
    >>> sorted(rand_list, reverse=True)
    [9878, 9828, 8442, 7953, 6431, 6213, 2207, 769]

(ソートに関する詳細な論議は Python wiki の Sorting mini-HOWTO
を参照: http://wiki.python.org/moin/HowTo/Sorting [#]_

ビルトインの ``any(iter)`` および ``all(iter)`` はイテラブルの真値を調べます。
:func:`any` は要素のどれかが真値なら True を返し、
:func:`all` は要素がどれも真値なら True を返します:

    >>> any([0,1,0])
    True
    >>> any([0,0,0])
    False
    >>> any([1,1,1])
    True
    >>> all([0,1,0])
    False
    >>> all([0,0,0])
    False
    >>> all([1,1,1])
    True


小さな関数とラムダ式
====================

関数型スタイルのプログラムを書いていると、述語として働いたり、何らかの形で
要素をつなぎ合わせたりするミニサイズの関数を必要とすることがよくあります。

ちょうど良い関数がビルトインやモジュールで存在していれば、
新しい関数を定義する必要はまったくありません::

    stripped_lines = [line.strip() for line in lines]
    existing_files = filter(os.path.exists, file_list)

しかし、欲しい関数がないなら書くしかありません。そうした小さな関数を書く方法の
一つが ``lambda`` 文です。 ``lambda`` は引数として複数のパラメータと
それをつなぐ式を取り、その式の値を返す小さな関数を作ります::

    lowercase = lambda x: x.lower()

    print_assign = lambda name, value: name + '=' + str(value)

    adder = lambda x, y: x+y

もう一つの選択肢は、ふつうに ``def`` 文で関数を定義するだけです::

    def lowercase(x):
        return x.lower()

    def print_assign(name, value):
        return name + '=' + str(value)

    def adder(x,y):
        return x + y

どちらのほうが良いのでしょうか。それは好みの問題です; 著者のスタイルとしては
できるだけ ``lambda`` を使わないようにしています。

そのようにしている理由の一つに、 ``lambda`` は定義できる関数が非常に
限られているという点があります。一つの式として算出できる結果に
しなければいけませんので、 ``if... elif... else`` や ``try... except``
のような分岐を持つことができないのです。 ``lambda`` 文の中で
たくさんのことをやろうとしすぎると、ごちゃごちゃして読みにくい式に
なってしまいます。さて、次のコードは何をしているでしょうか、
素早くお答えください!

::

    total = reduce(lambda a, b: (0, a[1] + b[1]), items)[1]

わかるにはわかるでしょうが、何がどうなっているのか紐解いていくには時間が
かかるはずです。短い ``def`` 文で入れ子にすると、少し見通しが良くなりますが::

    def combine (a, b):
        return 0, a[1] + b[1]

    total = reduce(combine, items)[1]

でも単純に ``for`` ループにすれば良かったのです::

     total = 0
     for a, b in items:
         total += b

あるいは :func:`sum` ビルトインとジェネレータ式でも良いですね::

     total = sum(b for a,b in items)

多くの場合、 :func:`reduce` を使っているところは ``for`` ループに
書き直したほうが見やすいです。

Fredrik Lundh は以前 ``lambda`` 利用のリファクタリング
に関して以下の指針を提案したことがあります:

1) ラムダ関数を書く。
2) そのラムダが一体ぜんたい何をしているのかコメントで説明する。
3) そのコメントをしばらく研究して、本質をとらえた名前を考える。
4) ラムダをその名前で def 文に書き換える。
5) コメントを消す。

著者はこの指針を本当に気に入っていますが、こうしたラムダなし
スタイルが他より優れているかどうかについて、異論は認めます。


itertools モジュール
====================

:mod:`itertools` モジュールには、よく使うイテレータや、イテレータ同士の
連結に使う関数がたくさん含まれています。この章では、そのモジュールの内容を
小さな例で紹介していきたいと思います。

このモジュールの関数を大まかに分けるとこうなります:

* 既存のイテレータに基づいて新しいイテレータを作る関数
* イテレータの要素を引数として扱う関数
* イテレータの出力から一部を取り出す関数
* イテレータの出力をグループ分けする関数

新しいイテレータを作る
----------------------

``itertools.count(n)`` は整数を 1 ずつ増やして無限長ストリームを返します。
開始地点となる数を渡すこともでき、既定は 0 になっています::

    itertools.count() =>
      0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...
    itertools.count(10) =>
      10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ...

``itertools.cycle(iter)`` は与えられたイテラブルの内容をコピーして、
その要素を最初から最後まで無限に繰り返していくイテレータを返します。 ::

    itertools.cycle([1,2,3,4,5]) =>
      1, 2, 3, 4, 5, 1, 2, 3, 4, 5, ...

``itertools.repeat(elem, [n])`` は、差し出された要素を ``n``
回返しますが、 ``n`` がなければ永遠に返し続けます。 ::

    itertools.repeat('abc') =>
      abc, abc, abc, abc, abc, abc, abc, abc, abc, abc, ...
    itertools.repeat('abc', 5) =>
      abc, abc, abc, abc, abc

``itertools.chain(iterA, iterB, ...)`` はイテラブルを好きな数だけ
受け取って、最初のイテレータから要素をすべて返し、次に二番目から
要素をすべて返し、ということを要素がなくなるまで続けます。 ::

    itertools.chain(['a', 'b', 'c'], (1, 2, 3)) =>
      a, b, c, 1, 2, 3

``itertools.izip(iterA, iterB, ...)`` は各イテラブルから
要素を一つずつ取り、タプルに入れて返します::

    itertools.izip(['a', 'b', 'c'], (1, 2, 3)) =>
      ('a', 1), ('b', 2), ('c', 3)

これはビルトインの :func:`zip` 関数と似ていますが、メモリ内に
リストを構築したり、入力イテレータを使い切ってから返したり
しない点が違います; これがタプルを作って返すのは、要求を受けたとき
だけなのです。(この振る舞いを専門用語で `遅延評価
<http://ja.wikipedia.org/wiki/%E9%81%85%E5%BB%B6%E8%A9%95%E4%BE%A1>`__
と言います。)

このイテレータの用途には、すべて同じ長さのイテラブルを想定しています。
長さが違っていれば、出力されるストリームは一番短いイテラブルと
同じ長さになります。 ::

    itertools.izip(['a', 'b'], (1, 2, 3)) =>
      ('a', 1), ('b', 2)

とは言え、これをやってしまうと長いイテレータから要素をひとつ無駄に多く
取って捨ててしまうかもしれませんので、やめておいたほうが良いです。
その捨てられた要素を抜かしてしまう危険があるので、
もうそのイテレータはそれ以上使えなくなってしまいます。

``itertools.islice(iter, [start], stop, [step])`` は、イテレータの
スライスをストリームで返します。 ``stop`` 引数だけだと、最初の
``stop`` 個の要素を返します。開始インデックスを渡すと
``stop - start`` 個で、 ``step`` の値も渡せばそれに応じて
要素を抜かします。Python における文字列やリストのスライスとは違って、
マイナスの値は ``start``, ``stop``, ``step`` に使えません。 ::

    itertools.islice(range(10), 8) =>
      0, 1, 2, 3, 4, 5, 6, 7
    itertools.islice(range(10), 2, 8) =>
      2, 3, 4, 5, 6, 7
    itertools.islice(range(10), 2, 8, 2) =>
      2, 4, 6

``itertools.tee(iter, [n])`` はイテレータを複製します; 元のイテレータの
内容を同じように返す、独立した ``n`` 個のイテレータを返すのです。
``n`` の値は、指定しなければ既定が 2 になっています。複製するには元の
イテレータの内容を一部保存しておく必要がありますから、大きな
イテレータから複製したうちの一つが他よりも進んでいってしまうと、
大量のメモリを消費することがあります。 ::

        itertools.tee( itertools.count() ) =>
           iterA, iterB

        where iterA ->
           0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...

        and   iterB ->
           0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...


要素に対して関数を呼ぶ
----------------------

イテラブルの中身に対して他の関数を呼ぶための関数が二つあります。

``itertools.imap(f, iterA, iterB, ...)`` は
``f(iterA[0], iterB[0]), f(iterA[1], iterB[1]), f(iterA[2], iterB[2]), ...``
というストリームを返します::

    itertools.imap(operator.add, [5, 6, 5], [1, 2, 3]) =>
      6, 8, 8

いま使った ``operator`` モジュールには、Python の演算子に対応する関数が入って
います。いくつか例を挙げると、 ``operator.add(a, b)`` (二つの値を加算)、
``operator.ne(a, b)`` (``a!=b`` と同じ)、 ``operator.attrgetter('id')``
(``"id"`` 属性を取得するコーラブルを返す) といった関数です。

``itertools.starmap(func, iter)`` は、イテラブルがタプルを返すものとして、
そのタプルを引数に使って ``func()`` を呼びます::

    itertools.starmap(os.path.join,
                      [('/usr', 'bin', 'java'), ('/bin', 'python'),
                       ('/usr', 'bin', 'perl'),('/usr', 'bin', 'ruby')])
    =>
      /usr/bin/java, /bin/python, /usr/bin/perl, /usr/bin/ruby


要素を選択する
--------------

さらに別のグループとして、述語 (predicate) に基づいて
イテレータの要素からサブセットを選び出す関数があります。

``itertools.ifilter(predicate, iter)`` は述語が真を返す要素をすべて返します::

    def is_even(x):
        return (x % 2) == 0

    itertools.ifilter(is_even, itertools.count()) =>
      0, 2, 4, 6, 8, 10, 12, 14, ...

``itertools.ifilterfalse(predicate, iter)`` は反対に、
述語が偽を返す要素をすべて返します::

    itertools.ifilterfalse(is_even, itertools.count()) =>
      1, 3, 5, 7, 9, 11, 13, 15, ...

``itertools.takewhile(predicate, iter)`` は述語が真を返している間だけ要素
を返します。一度でも述語が偽を返すと、イテレータは出力終了の合図をします。

::

    def less_than_10(x):
        return (x < 10)

    itertools.takewhile(less_than_10, itertools.count()) =>
      0, 1, 2, 3, 4, 5, 6, 7, 8, 9

    itertools.takewhile(is_even, itertools.count()) =>
      0

``itertools.dropwhile(predicate, iter)`` は、述語が真を返しているうちは
要素を無視し、偽になってから残りの出力をすべて返します。

::

    itertools.dropwhile(less_than_10, itertools.count()) =>
      10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ...

    itertools.dropwhile(is_even, itertools.count()) =>
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...


要素をグループ分けする
----------------------

最後に議題に上げる関数 ``itertools.groupby(iter, key_func=None)`` は、
これまでで最も複雑です。 ``key_func(elem)`` は、イテラブルから返ってきた要素
それぞれのキー値を計算する関数です。この関数が指定されていなければ、
キーは単に各要素そのものになります。

``groupby()`` は、下敷きになっているイテラブルから、
連続して同じキー値を持つ要素を集めて、キー値とイテレータの 2-タプルを
返していきます。イテレータは、それぞれのキーに対応する要素を出します。

::

    city_list = [('Decatur', 'AL'), ('Huntsville', 'AL'), ('Selma', 'AL'),
                 ('Anchorage', 'AK'), ('Nome', 'AK'),
                 ('Flagstaff', 'AZ'), ('Phoenix', 'AZ'), ('Tucson', 'AZ'),
                 ...
                ]

    def get_state ((city, state)):
        return state

    itertools.groupby(city_list, get_state) =>
      ('AL', iterator-1),
      ('AK', iterator-2),
      ('AZ', iterator-3), ...

    where
    iterator-1 =>
      ('Decatur', 'AL'), ('Huntsville', 'AL'), ('Selma', 'AL')
    iterator-2 =>
      ('Anchorage', 'AK'), ('Nome', 'AK')
    iterator-3 =>
      ('Flagstaff', 'AZ'), ('Phoenix', 'AZ'), ('Tucson', 'AZ')

``groupby()`` は、下敷きにするイテラブルの中身がキー値でソート済みに
なって与えられることを想定しています。さて、こうして出力される
イテレータ自体も下敷きのイテラブルを使うということに注意してください。
ですから iterator-1 に出力し切ってしまうまで、iterator-2
およびそのキー値を要求することはできません。


functools モジュール
====================

Python 2.5 からの :mod:`functools` モジュールには、高階関数がいくつか入って
います。 **高階関数** とは、入力として関数を受け取って新たな関数を返す関数
です。このモジュールで一番便利なツールは :func:`functools.partial` 関数です。

関数型スタイルのプログラムでは時折、既存の関数から一部のパラメータを埋めた
変種を作りたくなることがあります。Python の関数 ``f(a, b, c)`` というものが
あるとしてください; ``f(1, b, c)`` と同じ意味の ``g(b, c)`` という関数を
作りたくなることがあります; つまり ``f()`` のパラメータを一つ埋めるわけです。
これは「関数の部分適用」と呼ばれています。

``partial`` のコンストラクタは
``(関数, 引数1, 引数2, ... キーワード引数1=既定値1, キーワード引数2=既定値2)``
という引数を取ります。できあがったオブジェクトはコーラブルですので、それを
呼べば、引数の埋まった ``function`` を実行したのと同じことになります。

以下にあるのは、小さいけれども現実的な一つの例です::

    import functools

    def log (message, subsystem):
        "Write the contents of 'message' to the specified subsystem."
        print '%s: %s' % (subsystem, message)
        ...

    server_log = functools.partial(log, subsystem='server')
    server_log('Unable to open socket')


operator モジュール
-------------------

:mod:`operator` モジュールは、既に取り上げましたが、Python の演算子に対応する
関数が入っているモジュールです。関数型スタイルのコードにおいて、演算を一つ
実行するだけのくだらない関数を書かずに済むので、よく世話になります。

このモジュールの関数を一部だけ紹介しましょう:

* 数学演算子: ``add()``, ``sub()``, ``mul()``, ``div()``, ``floordiv()``,
  ``abs()``, ...
* 論理演算子: ``not_()``, ``truth()``
* ビット演算子: ``and_()``, ``or_()``, ``invert()``
* 比較: ``eq()``, ``ne()``, ``lt()``, ``le()``, ``gt()``, ``ge()``
* オブジェクト識別: ``is_()``, ``is_not()``

ちゃんとした一覧は operator モジュールの文書でご覧ください。


functional モジュール
---------------------

Collin Winter の
`functional モジュール <http://oakwinter.com/code/functional/>`__
には関数型プログラミング用の上級ツールが多数備わっています。さらには、
いくつかの Python ビルトインを再実装して、既に他言語で関数型プログラミングに
親しんでいる人たちにとってより直感的なようにしてあります。

この章では、 ``functional`` の中で最も重要な関数をいくつか紹介します;
完全版の文書は `プロジェクトのウェブサイト
<http://oakwinter.com/code/functional/documentation/>`__ にあります。

``compose(outer, inner, unpack=False)``

``compose()`` 関数は、関数合成を実装しています。言い換えると、
``inner`` と ``outer`` の両コーラブルを囲んで、 ``inner`` からの返り値を
すぐ ``outer`` に渡すようなラッパを返します。つまり、 ::

    >>> def add(a, b):
    ...     return a + b
    ...
    >>> def double(a):
    ...     return 2 * a
    ...
    >>> compose(double, add)(5, 6)
    22

は下と同じことをしています。 ::

    >>> double(add(5, 6))
    22

``unpack`` キーワードが用意されているのは、Python には完全に `カリー化
<http://en.wikipedia.org/wiki/Currying>`__ されていない関数があるという
現実に対処するためです。既定では ``inner`` 関数も単一オブジェクトを返し
``outer`` 関数も単一の引数を取るものと期待されていますが、 ``unpack``
引数を設定すると、 ``compose`` は ``inner`` からタプルが来るものとして、
``outer`` に渡す前に展開するようになります。ですから単なる ::

    compose(f, g)(5, 6)

は次の書き方と同じことです::

    f(g(5, 6))

けれども ::

    compose(f, g, unpack=True)(5, 6)

は次と同じ意味になります::

    f(*g(5, 6))

``compose()`` は二つしか関数を受け付けませんが、
好きなだけ合成できるバージョンを作るのは簡単なことです。それには
``reduce()``, ``compose()``, ``partial()`` を使います (最後のは
``functional`` でも ``functools`` でも提供されています)。 ::

    from functional import compose, partial

    multi_compose = partial(reduce, compose)


``map()``, ``compose()``, ``partial()`` を使って、引数を文字列に
変換するバージョンの ``"".join(...)`` を組み立てることもできます::

    from functional import compose, partial

    join = compose("".join, partial(map, str))


``flip(func)``

``flip()`` は、 ``func`` に指定したコーラブルのラッパを返し、
キーワードなし引数を逆の順番で受け取るようにします。 ::

    >>> def triple(a, b, c):
    ...     return (a, b, c)
    ...
    >>> triple(5, 6, 7)
    (5, 6, 7)
    >>>
    >>> flipped_triple = flip(triple)
    >>> flipped_triple(5, 6, 7)
    (7, 6, 5)

``foldl(func, start, iterable)``

``foldl()`` は引数として二引数関数、初期値 (たいていは「ある種の」ゼロ)、
イテラブルを取ります。その二引数関数を初期値とリスト第一要素に適用し、その結果と
リスト第二要素、さらにその結果と第三要素、というように適用していくのです。

つまり、こういうコールは ::

    foldl(f, 0, [1, 2, 3])

これと同じことになります::

    f(f(f(0, 1), 2), 3)


``foldl()`` は以下の再帰関数とほぼ同じです::

    def foldl(func, start, seq):
        if len(seq) == 0:
            return start

        return foldl(func, func(start, seq[0]), seq[1:])

「同じ」と言えば、さきほどの ``foldl`` コールの例は、ビルトインの
``reduce`` を使ってこのように表現することもできます::

    reduce(f, [1, 2, 3], 0)


``foldl()``, ``operator.concat()``, ``partial()`` を使えば、
スッキリして見やすいバージョンの ``"".join(...)`` を書くことができます::

    from functional import foldl, partial from operator import concat

    join = partial(foldl, concat, "")

更新履歴と謝辞
==============

著者は提案の申し出や修正、様々なこの記事の草稿の助けをしてくれた
以下の人々に感謝します:
Ian Bicking, Nick Coghlan, Nick Efford, Raymond Hettinger, Jim Jewett,
Mike Krell, Leandro Lameiro, Jussi Salmela, Collin Winter, Blake Winton.

Version 0.1: posted June 30 2006.

Version 0.11: posted July 1 2006.  Typo fixes.

Version 0.2: posted July 10 2006.  Merged genexp and listcomp sections into one.
Typo fixes.

Version 0.21: Added more references suggested on the tutor mailing list.

Version 0.30: Adds a section on the ``functional`` module written by Collin
Winter; adds short section on the operator module; a few other edits.


参照資料
========

一般論
------

Harold Abelson と Gerald Jay Sussman, Julie Sussman による
**Structure and Interpretation of Computer Programs** 。
http://mitpress.mit.edu/sicp/ に全文があります。
この計算機科学に関する古典的な教科書では、
2 章と 3 章でデータフローをプログラム内でまとめるための
シーケンスとストリームの利用について議論しています。
この本は例として Scheme を使っていますが、
これらの章内の多くのデザインアプローチは
関数スタイルな Python コードにも適用できます。

http://www.defmacro.org/ramblings/fp.html: 関数プログラミングの一般的な入門で
Java での例を利用していて、長大な歴史の紹介があります。

http://en.wikipedia.org/wiki/Functional_programming: 関数プログラミングに関する
一般的な内容の記事 [#]_ 。

http://en.wikipedia.org/wiki/Coroutine: コルーチンに関する記事 [#]_ 。

http://en.wikipedia.org/wiki/Currying: カリー化の概念に関する記事 [#]_ 。

Python 特有の話
---------------

http://gnosis.cx/TPiP/: David Mertz's の本の最初の章
:title-reference:`Text Processing in Python` では文書処理のための
関数プログラミングについて議論しています、
この議論の節には
"Utilizing Higher-Order Functions in Text Processing"
というタイトルがついています。



Python 文書
-----------

:mod:`itertools` モジュールの文書。

:mod:`operator` モジュールの文書。

:pep:`289`: "Generator Expressions"

:pep:`342`: "Coroutines via Enhanced Generators" describes the new generator
features in Python 2.5.

.. comment

    Topics to place
    -----------------------------

    XXX os.walk()

    XXX Need a large example.

    But will an example add much?  I'll post a first draft and see
    what the comments say.

.. comment

    Original outline:
    Introduction
            Idea of FP
                    Programs built out of functions
                    Functions are strictly input-output, no internal state
            Opposed to OO programming, where objects have state

            Why FP?
                    Formal provability
                            Assignment is difficult to reason about
                            Not very relevant to Python
                    Modularity
                            Small functions that do one thing
                    Debuggability:
                            Easy to test due to lack of state
                            Easy to verify output from intermediate steps
                    Composability
                            You assemble a toolbox of functions that can be mixed

    Tackling a problem
            Need a significant example

    Iterators
    Generators
    The itertools module
    List comprehensions
    Small functions and the lambda statement
    Built-in functions
            map
            filter
            reduce

.. comment

    Handy little function for printing part of an iterator -- used
    while writing this document.

    import itertools
    def print_iter(it):
         slice = itertools.islice(it, 10)
         for elem in slice[:-1]:
             sys.stdout.write(str(elem))
             sys.stdout.write(', ')
        print elem[-1]

.. rubric:: 注記

.. [#] 訳注 Python Wiki の内容の最新の情報は反映されていませんが、
       Python ドキュメント内に和訳があります :ref:`sortinghowto`
.. [#] 訳注 日本語版 Wikipedia に
       `関数型言語
       <http://ja.wikipedia.org/wiki/%E9%96%A2%E6%95%B0%E5%9E%8B%E8%A8%80%E8%AA%9E>`_
       に関する記事があります。
.. [#] 訳注 日本語版 Wikipedia に
       `コルーチン <http://ja.wikipedia.org/wiki/%E3%82%B3%E3%83%AB%E3%83%BC%E3%83%81%E3%83%B3>`_
       に関する記事があります。
.. [#] 訳注 日本語版 Wikipedia に
       `カリー化 <http://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%AA%E3%83%BC%E5%8C%96>`_
       に関する記事があります。
