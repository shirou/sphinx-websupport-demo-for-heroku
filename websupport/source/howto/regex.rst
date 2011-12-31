..
  ****************************
    Regular Expression HOWTO 
  ****************************

.. _regex-howto:

******************
  正規表現 HOWTO 
******************

:Author: A.M. Kuchling

.. TODO:
   Document lookbehind assertions
   Better way of displaying a RE, a string, and what it matches
   Mention optional argument to match.groups()
   Unicode (at least a reference)



..
  .. topic:: Abstract
  
     This document is an introductory tutorial to using regular expressions in Python
     with the :mod:`re` module.  It provides a gentler introduction than the
     corresponding section in the Library Reference.

.. topic:: 概要

   このドキュメントは :mod:`re` モジュールを使って Python で正規表現を扱うための
   導入のチュートリアルです。
   ライブラリレファレンスの正規表現の節よりもやさしい入門ドキュメントを用意しています。

..
  Introduction
  ============

入門
====

..
  The :mod:`re` module was added in Python 1.5, and provides Perl-style regular
  expression patterns.  Earlier versions of Python came with the :mod:`regex`
  module, which provided Emacs-style patterns.  The :mod:`regex` module was
  removed completely in Python 2.5.

:mod:`re` モジュールは Python 1.5 で追加され、Perl スタイルの正規表現パターンを提供します。
それ以前の Python では :mod:`regex` モジュールが Emacs スタイルのパターンを提供していました。
:mod:`regex` モジュールは Python 2.5 で完全に削除されました。

..
  Regular expressions (called REs, or regexes, or regex patterns) are essentially
  a tiny, highly specialized programming language embedded inside Python and made
  available through the :mod:`re` module. Using this little language, you specify
  the rules for the set of possible strings that you want to match; this set might
  contain English sentences, or e-mail addresses, or TeX commands, or anything you
  like.  You can then ask questions such as "Does this string match the pattern?",
  or "Is there a match for the pattern anywhere in this string?".  You can also
  use REs to modify a string or to split it apart in various ways.

正規表現 regular expressions (REs や regexes または regex patterns と呼ばれます) は
本質的に小さく、Python 内部に埋め込まれた高度に特化したプログラミング言語で
:mod:`re` モジュールから利用可能です。
この小さな言語を利用することで、マッチさせたい文字列に適合するような文字列の集合を
指定することができます;
この集合は英文や e-mail アドレスや TeX コマンドなど、どんなものでも構いません。
「この文字列は指定したパターンにマッチしますか?」
「このパターンはこの文字列のどの部分にマッチするのですか?」といったことを
問い合わせることができます。
正規表現を使って文字列を変更したりいろいろな方法で別々の部分に分割したりすることもできます。

..
  Regular expression patterns are compiled into a series of bytecodes which are
  then executed by a matching engine written in C.  For advanced use, it may be
  necessary to pay careful attention to how the engine will execute a given RE,
  and write the RE in a certain way in order to produce bytecode that runs faster.
  Optimization isn't covered in this document, because it requires that you have a
  good understanding of the matching engine's internals.

正規表現パターンは一連のバイトコードとしてコンパイルされ、
C で書かれたマッチングエンジンによって実行されます。
より進んだ利用法では、エンジンがどう与えられた正規表現を実行するかに注意することが
必要になり、高速に実行できるバイトコードを生成するように正規表現を書くことになります。
このドキュメントでは最適化までは扱いません、それにはマッチングエンジンの内部に対する十分な理解が必要だからです。

..
  The regular expression language is relatively small and restricted, so not all
  possible string processing tasks can be done using regular expressions.  There
  are also tasks that *can* be done with regular expressions, but the expressions
  turn out to be very complicated.  In these cases, you may be better off writing
  Python code to do the processing; while Python code will be slower than an
  elaborate regular expression, it will also probably be more understandable.

正規表現言語は相対的に小さく、制限されています、
そのため正規表現を使ってあらゆる文字列処理作業を行なえるわけではありません。
正規表現を使って行うことのできる作業もあります、
ただ表現はとても複雑なものになります。
それらの場合では、Python コードを書いた方がいいでしょう;
Python コードは念入りに作られた正規表現より遅くなりますが、
おそらくより読み易いでしょう。

..
  Simple Patterns
  ===============

単純なパターン
==============

..
  We'll start by learning about the simplest possible regular expressions.  Since
  regular expressions are used to operate on strings, we'll begin with the most
  common task: matching characters.

まずはできるだけ簡単な正規表現を学ぶことから始めてみましょう。
正規表現は文字列の操作に使われるので、ますは最も一般的な作業である文字のマッチングをしてみます。

..
  For a detailed explanation of the computer science underlying regular
  expressions (deterministic and non-deterministic finite automata), you can refer
  to almost any textbook on writing compilers.

正規表現の基礎を成す計算機科学 (決定、非決定有限オートマトン) の詳細な説明については,
コンパイラ作成に関するテキストブックをどれでもいいので参照して下さい。

..
  Matching Characters
  -------------------

文字のマッチング
----------------

..
  Most letters and characters will simply match themselves.  For example, the
  regular expression ``test`` will match the string ``test`` exactly.  (You can
  enable a case-insensitive mode that would let this RE match ``Test`` or ``TEST``
  as well; more about this later.)

多くの活字や文字は単純にそれ自身とマッチします。例えば、 ``test`` という正規表現は文字列 ``test`` に厳密にマッチします。
(大文字小文字を区別しないモードでその正規表現が ``Test`` や ``TEST`` にも同様にマッチすることもできます; 詳しくは後述します。)

..
  There are exceptions to this rule; some characters are special
  :dfn:`metacharacters`, and don't match themselves.  Instead, they signal that
  some out-of-the-ordinary thing should be matched, or they affect other portions
  of the RE by repeating them or changing their meaning.  Much of this document is
  devoted to discussing various metacharacters and what they do.

この規則には例外が存在します; いくつかの文字は特別な :dfn:`特殊文字 (metacharacters)` で、それら自身にマッチしません。
代わりに通常のマッチするものとは違うという合図を出したり、正規表現の一部に対して繰り返したり、意味を変えたりして影響を与えます。
このドキュメントの中の多くは様々な特殊文字とそれが何をするかについて論じることになります。

..
  Here's a complete list of the metacharacters; their meanings will be discussed
  in the rest of this HOWTO. ::

ここに特殊文字の完全な一覧があります; これらの意味はこの HOWTO の残りの部分で説明します::

   . ^ $ * + ? { } [ ] \ | ( )

..
  The first metacharacters we'll look at are ``[`` and ``]``. They're used for
  specifying a character class, which is a set of characters that you wish to
  match.  Characters can be listed individually, or a range of characters can be
  indicated by giving two characters and separating them by a ``'-'``.  For
  example, ``[abc]`` will match any of the characters ``a``, ``b``, or ``c``; this
  is the same as ``[a-c]``, which uses a range to express the same set of
  characters.  If you wanted to match only lowercase letters, your RE would be
  ``[a-z]``.

最初に扱う特殊文字は ``[`` と ``]`` です。
これらは文字クラスを指定します、文字クラスはマッチしたい文字の集合です。
文字は個別にリストにしても構いませんし、二つの文字を ``'-'`` でつなげて文字を範囲で与えてもかまいません。
たとえば ``[abc]`` は ``a``, ``b``, または ``c`` のどの文字列にもマッチします;
これは ``[a-c]`` で同じ文字集合を範囲で表現しても全く同じです。
小文字のアルファベットのみにマッチしたい場合、 ``[a-z]`` の正規表現をつかうことになるでしょう。

..
  Metacharacters are not active inside classes.  For example, ``[akm$]`` will
  match any of the characters ``'a'``, ``'k'``, ``'m'``, or ``'$'``; ``'$'`` is
  usually a metacharacter, but inside a character class it's stripped of its
  special nature.

特殊文字は文字クラスの内部では有効になりません。
例えば、 ``[akm$]`` は ``'a'``, ``'k'``, ``'m'`` または ``'$'`` にマッチします;
``'$'`` は通常は特殊文字ですが、文字クラス内部では特殊な性質は取り除かれます。

..
  You can match the characters not listed within the class by :dfn:`complementing`
  the set.  This is indicated by including a ``'^'`` as the first character of the
  class; ``'^'`` outside a character class will simply match the ``'^'``
  character.  For example, ``[^5]`` will match any character except ``'5'``.

文字クラス内のリストにない文字に対しても :dfn:`補集合` を使ってマッチすることができます。
補集合はクラスの最初の文字として ``'^'`` を含めることで表すことができます;
文字クラスの外側の ``'^'`` は単に ``'^'`` 文字にマッチします。
例えば、 ``[^5]`` は ``'5'`` を除く任意の文字にマッチします。

..
  Perhaps the most important metacharacter is the backslash, ``\``.   As in Python
  string literals, the backslash can be followed by various characters to signal
  various special sequences.  It's also used to escape all the metacharacters so
  you can still match them in patterns; for example, if you need to match a ``[``
  or  ``\``, you can precede them with a backslash to remove their special
  meaning: ``\[`` or ``\\``.

おそらく最も重要な特殊文字はバックスラッシュ ``\`` でしょう。
Python の文字列リテラルのようにバックスラッシュに続けていろいろな文字を入力することでいろいろな特殊シーケンスの合図を送ることができます。
また、バックスラッシュはすべての特殊文字をエスケープするのにも利用されます、
つまり、特殊文字をマッチさせることができます;
例えば、 ``[`` または ``\`` にマッチさせたい場合、それらをバックスラッシュに続けることで特殊な意味を除きます: ``\[`` または ``\\`` 。 

..
  Some of the special sequences beginning with ``'\'`` represent predefined sets
  of characters that are often useful, such as the set of digits, the set of
  letters, or the set of anything that isn't whitespace.  The following predefined
  special sequences are a subset of those available. The equivalent classes are
  for byte string patterns. For a complete list of sequences and expanded class
  definitions for Unicode string patterns, see the last part of
  :ref:`Regular Expression Syntax <re-syntax>`.

いくつかの ``'\'`` で始まる特殊シーケンスはあらかじめ定義された文字集合を表していて、
しばしば便利に使うことができます、例えば、10進数の集合、文字の集合、空白以外の任意の文字の集合。
以下のあらかじめ定義された特殊シーケンスは利用可能なものの一部です。
等価なクラスがバイト文字列パターンに対してもあります。
ユニコード文字列パターンのためのシーケンスおよび拡張クラス定義の
完全なリストについては、 :ref:`正規表現のシンタックス <re-syntax>` の
最後の部分を見てください。


..
  ``\d``
     Matches any decimal digit; this is equivalent to the class ``[0-9]``.
  
  ``\D``
     Matches any non-digit character; this is equivalent to the class ``[^0-9]``.
  
  ``\s``
     Matches any whitespace character; this is equivalent to the class ``[
     \t\n\r\f\v]``.
  
  ``\S``
     Matches any non-whitespace character; this is equivalent to the class ``[^
     \t\n\r\f\v]``.
  
  ``\w``
     Matches any alphanumeric character; this is equivalent to the class
     ``[a-zA-Z0-9_]``.
  
  ``\W``
     Matches any non-alphanumeric character; this is equivalent to the class
     ``[^a-zA-Z0-9_]``.

``\d``
   任意の十進数とマッチします；これは集合 ``[0-9]`` と同じ意味です。

``\D``
   任意の非数字文字とマッチします；これは集合 ``[^0-9]`` と同じ意味です。 

``\s``
   任意の空白文字とマッチします；これは集合 ``[\t\n\r\f\v]`` と同じ意味です。

``\S``
   任意の非空白文字とマッチします；これは集合 ``[^\t\n\r\f\v]`` と同じ意味です。

``\w``
   任意の英数文字および下線とマッチします；これは、集合 ``[a-zA-Z0-9_]`` と同じ意味です。 

``\W``
   任意の非英数文字とマッチします；これは集合 ``[^a-zA-Z0-9_]`` と同じ意味です。

..
  These sequences can be included inside a character class.  For example,
  ``[\s,.]`` is a character class that will match any whitespace character, or
  ``','`` or ``'.'``.

これらのシーケンスは文字クラス内に含めることができます。
例えば、 ``[\s,.]`` は空白文字や ``','`` または ``'.'`` にマッチする文字クラスです。

..
  The final metacharacter in this section is ``.``.  It matches anything except a
  newline character, and there's an alternate mode (``re.DOTALL``) where it will
  match even a newline.  ``'.'`` is often used where you want to match "any
  character".

この節での最後の特殊文字は ``.`` です。
これは改行文字を除く任意の文字にマッチします、
さらに改行文字に対してもマッチさせる代替モード (``re.DOTALL``) があります。
``'.'`` は「任意の文字」にマッチさせたい場合に利用されます。

..
  Repeating Things
  ----------------

繰り返し
--------

..
  Being able to match varying sets of characters is the first thing regular
  expressions can do that isn't already possible with the methods available on
  strings.  However, if that was the only additional capability of regexes, they
  wouldn't be much of an advance. Another capability is that you can specify that
  portions of the RE must be repeated a certain number of times.

さまざまな文字集合をマッチさせることは正規表現で最初にできるようになることで、
これは文字列に対するメソッドですぐにできることではありません。
しかし、正規表現がより力を発揮する場面がこれだけだとすると、正規表現はあまり先進的とはいえません。
正規表現の力をもう一つの能力は、正規表現の一部が何度も繰り返されるようものを指定できることです。

..
  The first metacharacter for repeating things that we'll look at is ``*``.  ``*``
  doesn't match the literal character ``*``; instead, it specifies that the
  previous character can be matched zero or more times, instead of exactly once.

最初にとりあげる繰り返しのための最初の特殊文字は ``*`` です。
``*`` は文字リテラル ``*`` とはマッチしません;
その代わりに前の文字が厳密に1回ではなく、0回以上繰り返されるパターンを指定します。

..
  For example, ``ca*t`` will match ``ct`` (0 ``a`` characters), ``cat`` (1 ``a``),
  ``caaat`` (3 ``a`` characters), and so forth.  The RE engine has various
  internal limitations stemming from the size of C's ``int`` type that will
  prevent it from matching over 2 billion ``a`` characters; you probably don't
  have enough memory to construct a string that large, so you shouldn't run into
  that limit.

例えば、 ``ca*t`` は ``ct`` (``a`` が0文字)、 ``cat`` (``a`` が1文字)、
``caaat`` (``a`` 3文字)、続々。
正規表現エンジンには C の ``int`` 型のサイズのために
20億文字の ``a`` とのマッチングができないなど多くの内部制限があります;
おそらくそれほど大きい文字列を構築するほどの十分なメモリはないので、
その制限に達することはありません。

..
  Repetitions such as ``*`` are :dfn:`greedy`; when repeating a RE, the matching
  engine will try to repeat it as many times as possible. If later portions of the
  pattern don't match, the matching engine will then back up and try again with
  few repetitions.


``*`` のような繰り返しは :dfn:`貪欲 (greedy)` です;
正規表現を繰り返したいとき、マッチングエンジンは可能な限り何度も繰り返そうと試みます。
パターンの後ろの部分にマッチしない場合、マッチングエンジンは戻って少ない繰り返しを再び試みます。

..
  A step-by-step example will make this more obvious.  Let's consider the
  expression ``a[bcd]*b``.  This matches the letter ``'a'``, zero or more letters
  from the class ``[bcd]``, and finally ends with a ``'b'``.  Now imagine matching
  this RE against the string ``abcbd``.

例をステップ、ステップで進めていくとより明確にわかります。
正規表現 ``a[bcd]*b`` を考えましょう。
この表現は文字 ``'a'`` と文字クラス ``[bcd]`` の0回以上の文字と最後の ``'b'`` にマッチします。
この正規表現が文字列 ``abcbd`` に対してマッチする作業を想像してみましょう。

..
  +------+-----------+---------------------------------+
  | Step | Matched   | Explanation                     |
  +======+===========+=================================+
  | 1    | ``a``     | The ``a`` in the RE matches.    |
  +------+-----------+---------------------------------+
  | 2    | ``abcbd`` | The engine matches ``[bcd]*``,  |
  |      |           | going as far as it can, which   |
  |      |           | is to the end of the string.    |
  +------+-----------+---------------------------------+
  | 3    | *Failure* | The engine tries to match       |
  |      |           | ``b``, but the current position |
  |      |           | is at the end of the string, so |
  |      |           | it fails.                       |
  +------+-----------+---------------------------------+
  | 4    | ``abcb``  | Back up, so that  ``[bcd]*``    |
  |      |           | matches one less character.     |
  +------+-----------+---------------------------------+
  | 5    | *Failure* | Try ``b`` again, but the        |
  |      |           | current position is at the last |
  |      |           | character, which is a ``'d'``.  |
  +------+-----------+---------------------------------+
  | 6    | ``abc``   | Back up again, so that          |
  |      |           | ``[bcd]*`` is only matching     |
  |      |           | ``bc``.                         |
  +------+-----------+---------------------------------+
  | 6    | ``abcb``  | Try ``b`` again.  This time     |
  |      |           | the character at the            |
  |      |           | current position is ``'b'``, so |
  |      |           | it succeeds.                    |
  +------+-----------+---------------------------------+

+----------+------------------+----------------------------------+
| ステップ | マッチした文字列 | 説明                             |
+==========+==================+==================================+
| 1        | ``a``            | ``a`` が正規表現にマッチ。       |
+----------+------------------+----------------------------------+
| 2        | ``abcbd``        | 正規表現エンジンが ``[bcd]*`` で |
|          |                  | 文字列の最後まで可能な限り進む。 |
+----------+------------------+----------------------------------+
| 3        | *失敗*           | エンジンが ``b`` とのマッチを    |
|          |                  | 試みるが、現在の位置が           |
|          |                  | 文字列の最後なので、失敗する。   |
+----------+------------------+----------------------------------+
| 4        | ``abcb``         | 戻って ``[bcd]*`` は一文字少なく |
|          |                  | マッチ。                         |
+----------+------------------+----------------------------------+
| 5        | *失敗*           | 再び ``b`` へのマッチを          |
|          |                  | 試みるが、現在の文字は           |
|          |                  | 最後の文字 ``'d'`` 。            |
+----------+------------------+----------------------------------+
| 6        | ``abc``          | 再び戻る, ``[bcd]*`` は ``bc``   |
|          |                  | のみにマッチ。                   |
+----------+------------------+----------------------------------+
| 7        | ``abcb``         | 再び ``b`` を試みる。            |
|          |                  | 今回の現在位置の文字は           |
|          |                  | ``'b'`` なので成功。             |
+----------+------------------+----------------------------------+

..
  The end of the RE has now been reached, and it has matched ``abcb``.  This
  demonstrates how the matching engine goes as far as it can at first, and if no
  match is found it will then progressively back up and retry the rest of the RE
  again and again.  It will back up until it has tried zero matches for
  ``[bcd]*``, and if that subsequently fails, the engine will conclude that the
  string doesn't match the RE at all.

正規表現の終端に達して、 ``abcd`` にマッチしました。
この例はマッチングエンジンが最初に到達できるところまで進みマッチしなかった場合、
逐次戻って再度残りの正規表現とのマッチを次々と試みること様子を示しています。
エンジンは ``[bcd]*`` とマッチしなくなるまで戻ります、
さらに続く正規表現とのマッチに失敗した場合にエンジンは
正規表現と文字列が完全にマッチしないと結論づけることになります。

..
  Another repeating metacharacter is ``+``, which matches one or more times.  Pay
  careful attention to the difference between ``*`` and ``+``; ``*`` matches
  *zero* or more times, so whatever's being repeated may not be present at all,
  while ``+`` requires at least *one* occurrence.  To use a similar example,
  ``ca+t`` will match ``cat`` (1 ``a``), ``caaat`` (3 ``a``'s), but won't match
  ``ct``.

別の繰り返しの特殊文字は ``+`` です、この特殊文字は1回以上の繰り返しにマッチします。
``*`` と ``+`` に違いに対しては十分注意して下さい;
``*`` は *0回* 以上の繰り返しにマッチします、つまり繰り返す部分が全くなくても問題ありません、
一方で ``+`` は少なくとも *1回* は表われる必要があります。
同様の例を使うと
``ca+t`` は ``cat`` (``a`` 1文字), ``caaat`` (``a`` 3文字), とマッチし、
``ct`` とはマッチしません。

..
  There are two more repeating qualifiers.  The question mark character, ``?``,
  matches either once or zero times; you can think of it as marking something as
  being optional.  For example, ``home-?brew`` matches either ``homebrew`` or
  ``home-brew``.

2回以上の繰り返しを制限する修飾子も存在します。
クエスチョンマーク ``?`` は0か1回のどちらかにマッチします;
これはオプションであることを示していると考えることもできます。
例えば、  ``home-?brew`` は ``homebrew`` と ``home-brew`` のどちらにもマッチします。

..
  The most complicated repeated qualifier is ``{m,n}``, where *m* and *n* are
  decimal integers.  This qualifier means there must be at least *m* repetitions,
  and at most *n*.  For example, ``a/{1,3}b`` will match ``a/b``, ``a//b``, and
  ``a///b``.  It won't match ``ab``, which has no slashes, or ``a////b``, which
  has four.

より複雑に繰り返しを制限するのは ``{m,n}`` です、ここで *m* と *n* は10進数の整数です。
この修飾子は最低 *m* 回、最大で *n* 回の繰り返すことを意味しています。
例えば、 ``a/{1,3}b`` は ``a/b`` と ``a//b`` そして ``a///b`` にマッチします。
これはスラッシュの無い ``ab`` や4つのスラッシュを持つ ``a////b`` とはマッチしません。

..
  You can omit either *m* or *n*; in that case, a reasonable value is assumed for
  the missing value.  Omitting *m* is interpreted as a lower limit of 0, while
  omitting *n* results in an upper bound of infinity --- actually, the upper bound
  is the 2-billion limit mentioned earlier, but that might as well be infinity.

*m* か *n* のどちらかは省略することができます;
そうした場合省略された値はもっともらしい値と仮定されます。
*m* の省略は下限 0 と解釈され、 *n* の省略は無限の上限として解釈されます
--- 実際には上限は前に述べたように20億ですが、無限大とみなしてもいいでしょう。

..
  Readers of a reductionist bent may notice that the three other qualifiers can
  all be expressed using this notation.  ``{0,}`` is the same as ``*``, ``{1,}``
  is equivalent to ``+``, and ``{0,1}`` is the same as ``?``.  It's better to use
  ``*``, ``+``, or ``?`` when you can, simply because they're shorter and easier
  to read.

還元主義的素養のある読者は、3つの修飾子がこの表記で表現できることに気づくでしょう。
``{0,}`` は ``*`` と同じで ``{1,}`` は ``+`` と、そして ``{0,1}`` は ``?`` と同じです。
利用できる場合には ``*``, ``+`` または ``?`` を利用した方が賢明です、
そうすることで単純に、短く読み易くすることができます。

..
  Using Regular Expressions
  =========================

正規表現を使う
==============

..
  Now that we've looked at some simple regular expressions, how do we actually use
  them in Python?  The :mod:`re` module provides an interface to the regular
  expression engine, allowing you to compile REs into objects and then perform
  matches with them.

これまででいくつかの単純な正規表現に触れてきました、
実際に Python ではこれらをどう使えばいいのでしょう?
:mod:`re` モジュールは正規表現エンジンに対するインターフェースを提供していて、
それらを使うことで正規表現をオブジェクトにコンパイルし、マッチを実行することができます。

..
  Compiling Regular Expressions
  -----------------------------

正規表現をコンパイルする
------------------------

..
  Regular expressions are compiled into pattern objects, which have
  methods for various operations such as searching for pattern matches or
  performing string substitutions. ::

正規表現はパターンオブジェクトにコンパイルされます、
パターンオブジェクトは多くの操作、
パターンマッチの検索や文字列の置換の実行などのメソッドを持っています::

   >>> import re
   >>> p = re.compile('ab*')
   >>> print p
   <_sre.SRE_Pattern object at 0x...>

..
  :func:`re.compile` also accepts an optional *flags* argument, used to enable
  various special features and syntax variations.  we'll go over the available
  settings later, but for now a single example will do::

:func:`re.compile` はいくつかの *flags* 引数を受け付けることができます、
この引数はさまざまな特別な機能を有効にしたり、構文を変化させたりします。
利用できる設定に何があるかは後に飛ばすことにして、簡単な例をやることにしましょう::

   >>> p = re.compile('ab*', re.IGNORECASE)

..
  The RE is passed to :func:`re.compile` as a string.  REs are handled as strings
  because regular expressions aren't part of the core Python language, and no
  special syntax was created for expressing them.  (There are applications that
  don't need REs at all, so there's no need to bloat the language specification by
  including them.) Instead, the :mod:`re` module is simply a C extension module
  included with Python, just like the :mod:`socket` or :mod:`zlib` modules.

正規表現は文字列として :func:`re.compile` に渡されます。
正規表現は文字列として扱われますが、それは正規表現が Python 言語のコアシステムに含まれないためです、
そのため正規表現を表わす特殊な構文はありません。
(正規表現を全く必要としないアプリケーションも存在します、
そのためそれらを含めて言語仕様を無駄に大きくする必要はありません)
その代わり、 :mod:`re` モジュールは :mod:`socket` や :mod:`zlib` モジュールのような
通常の C 拡張モジュールとして Python に含まれています。

..
  Putting REs in strings keeps the Python language simpler, but has one
  disadvantage which is the topic of the next section.

正規表現を文字列としておくことで Python 言語はより簡素に保たれていますが、
そのため1つの欠点があります、これについては次の節で話題とします。

..
  The Backslash Plague
  --------------------

バックスラッシュ感染症
----------------------

..
  As stated earlier, regular expressions use the backslash character (``'\'``) to
  indicate special forms or to allow special characters to be used without
  invoking their special meaning. This conflicts with Python's usage of the same
  character for the same purpose in string literals.

先に述べたように、正規表現は特別な形式や特殊な文字の特別な意味を意味を除くことを示すために
バックスラッシュ文字 (``'\'``) を利用します。
これは Python が文字列リテラルに対して、同じ文字を同じ目的で使うことと衝突します。

..
  Let's say you want to write a RE that matches the string ``\section``, which
  might be found in a LaTeX file.  To figure out what to write in the program
  code, start with the desired string to be matched.  Next, you must escape any
  backslashes and other metacharacters by preceding them with a backslash,
  resulting in the string ``\\section``.  The resulting string that must be passed
  to :func:`re.compile` must be ``\\section``.  However, to express this as a
  Python string literal, both backslashes must be escaped *again*.

``\section`` という文字列 (これは LaTeX ファイルでみかけます) 
にマッチする正規表現を書きたいとします。
どんなプログラムを書くか考え、マッチして欲しい文字列をはじめに考えます。
次に、バックスラッシュや他の特殊文字をバックスラッシュに続けて書くことでエスケープしなければいけません、
その結果 ``\\section`` のような文字列となります。
こうしてできた :func:`re.compile` に渡す文字列は ``\\section`` でなければいけません。
しかし、これを Python の文字列リテラルとして扱うにはこの二つのバックスラッシュを *再び*
エスケープする必要があります。

..
  +-------------------+------------------------------------------+
  | Characters        | Stage                                    |
  +===================+==========================================+
  | ``\section``      | Text string to be matched                |
  +-------------------+------------------------------------------+
  | ``\\section``     | Escaped backslash for :func:`re.compile` |
  +-------------------+------------------------------------------+
  | ``"\\\\section"`` | Escaped backslashes for a string literal |
  +-------------------+------------------------------------------+

+-------------------+-------------------------------------------------------+
| 文字              | 段階                                                  |
+===================+=======================================================+
| ``\section``      | マッチさせるテキスト                                  |
+-------------------+-------------------------------------------------------+
| ``\\section``     | :func:`re.compile` のためのバックスラッシュエスケープ |
+-------------------+-------------------------------------------------------+
| ``"\\\\section"`` | 文字列リテラルのためのバックスラッシュエスケープ      |
+-------------------+-------------------------------------------------------+

..
  In short, to match a literal backslash, one has to write ``'\\\\'`` as the RE
  string, because the regular expression must be ``\\``, and each backslash must
  be expressed as ``\\`` inside a regular Python string literal.  In REs that
  feature backslashes repeatedly, this leads to lots of repeated backslashes and
  makes the resulting strings difficult to understand.

要点だけをいえば、リテラルとしてのバックスラッシュにマッチさせるために、
正規表現文字列として ``'\\\\'`` 書かなければいけません、
なぜなら正規表現は ``\\`` であり、通常の Python の文字列リテラルとしては
それぞれのバックスラッシュは ``\\`` で表現しなければいけないからです。
正規表現に関してこのバックスラッシュの繰り返しの機能は、
たくさんのバックスラッシュの繰り返しを生むことになり、
その結果として作られる文字列は理解することが難しくなります。

..
  The solution is to use Python's raw string notation for regular expressions;
  backslashes are not handled in any special way in a string literal prefixed with
  ``'r'``, so ``r"\n"`` is a two-character string containing ``'\'`` and ``'n'``,
  while ``"\n"`` is a one-character string containing a newline. Regular
  expressions will often be written in Python code using this raw string notation.

この問題の解決策としては正規表現に対しては Python の raw string 記法を使うことです;
``'r'`` を文字列リテラルの先頭に書くことでバックスラッシュは特別扱いされなくなります、
つまり ``"\n"`` は改行を含む1つの文字からなる文字列であるのに対して、
``r"\n"`` は2つの文字 ``'\'`` と ``'n'`` を含む文字列となります。
多くの場合 Python コードの中の正規表現はこの raw string 記法を使って書かれます。


..
  +-------------------+------------------+
  | Regular String    | Raw string       |
  +===================+==================+
  | ``"ab*"``         | ``r"ab*"``       |
  +-------------------+------------------+
  | ``"\\\\section"`` | ``r"\\section"`` |
  +-------------------+------------------+
  | ``"\\w+\\s+\\1"`` | ``r"\w+\s+\1"``  |
  +-------------------+------------------+

+-------------------+------------------+
| 通常の文字列      | Raw string       |
+===================+==================+
| ``"ab*"``         | ``r"ab*"``       |
+-------------------+------------------+
| ``"\\\\section"`` | ``r"\\section"`` |
+-------------------+------------------+
| ``"\\w+\\s+\\1"`` | ``r"\w+\s+\1"``  |
+-------------------+------------------+

..
  Performing Matches
  ------------------

マッチの実行
------------

..
  Once you have an object representing a compiled regular expression, what do you
  do with it?  Pattern objects have several methods and attributes.
  Only the most significant ones will be covered here; consult the :mod:`re` docs
  for a complete listing.

一旦コンパイルした正規表現を表現するオブジェクトを作成したら、次に何をしますか?
パターンオブジェクトはいくつかのメソッドや属性を持っています。
ここでは、その中でも最も重要なものについて扱います;
完全なリストは :mod:`re` ドキュメントを参照して下さい。

..
  +------------------+-----------------------------------------------+
  | Method/Attribute | Purpose                                       |
  +==================+===============================================+
  | ``match()``      | Determine if the RE matches at the beginning  |
  |                  | of the string.                                |
  +------------------+-----------------------------------------------+
  | ``search()``     | Scan through a string, looking for any        |
  |                  | location where this RE matches.               |
  +------------------+-----------------------------------------------+
  | ``findall()``    | Find all substrings where the RE matches, and |
  |                  | returns them as a list.                       |
  +------------------+-----------------------------------------------+
  | ``finditer()``   | Find all substrings where the RE matches, and |
  |                  | returns them as an :term:`iterator`.          |
  +------------------+-----------------------------------------------+

+------------------+-----------------------------------------------+
| メソッド/属性    | 目的                                          |
+==================+===============================================+
| ``match()``      | 文字列の先頭で正規表現と                      |
|                  | マッチするか判定します                        |
+------------------+-----------------------------------------------+
| ``search()``     | 文字列を操作して、正規表現が                  |
|                  | どこにマッチするか調べます。                  |
+------------------+-----------------------------------------------+
| ``findall()``    | 正規表現にマッチする部分文字列を全て探しだし  |
|                  | リストとして返します。                        |
+------------------+-----------------------------------------------+
| ``finditer()``   | 正規表現にマッチする部分文字列を全て探しだし  |
|                  | :term:`iterator` として返します               |
+------------------+-----------------------------------------------+

..
  :meth:`match` and :meth:`search` return ``None`` if no match can be found.  If
  they're successful, a ``MatchObject`` instance is returned, containing
  information about the match: where it starts and ends, the substring it matched,
  and more.

マッチしない場合 :meth:`match` と :meth:`search` は ``None`` を返します。
もしマッチに成功した場合、 ``MatchObject`` インスタンスを返します、
このインスタンスはマッチの情報を含んでいます: どこで始まりどこで終わったか、
マッチした部分文字列や等々。

..
  You can learn about this by interactively experimenting with the :mod:`re`
  module.  If you have Tkinter available, you may also want to look at
  :file:`Tools/scripts/redemo.py`, a demonstration program included with the
  Python distribution.  It allows you to enter REs and strings, and displays
  whether the RE matches or fails. :file:`redemo.py` can be quite useful when
  trying to debug a complicated RE.  Phil Schwartz's `Kodos
  <http://kodos.sourceforge.net/>`_ is also an interactive tool for developing and
  testing RE patterns.

:mod:`re` モジュールで対話的に実験することで学ぶこともできます。
Tkinter が利用できれば、Python に含まれるデモプログラム
:file:`Tools/scripts/redemo.py` を見るといいかもしれません。
このデモは正規表現と文字列を入力し、正規表現がマッチしたかどうかを表示します。
:file:`redemo.py` は複雑な正規表現のデバッグを試みるときにも便利に使うことができます。
Phil Schwartz の `Kodos <http://kodos.sourceforge.net/>`_ も
正規表現パターンを使った開発とテストのための対話的なツールです。

..
  This HOWTO uses the standard Python interpreter for its examples. First, run the
  Python interpreter, import the :mod:`re` module, and compile a RE::

この HOWTO では例として標準の Python インタプリタを使います。
最初に Python インタプリタを起動して、 :mod:`re` モジュールをインポートし、
正規表現をコンパイルします::

   Python 2.2.2 (#1, Feb 10 2003, 12:57:01)
   >>> import re
   >>> p = re.compile('[a-z]+')
   >>> p
   <_sre.SRE_Pattern object at 0x...>

..
  Now, you can try matching various strings against the RE ``[a-z]+``.  An empty
  string shouldn't match at all, since ``+`` means 'one or more repetitions'.
  :meth:`match` should return ``None`` in this case, which will cause the
  interpreter to print no output.  You can explicitly print the result of
  :meth:`match` to make this clear. ::

さて、いろいろな文字列を使って正規表現 ``[a-z]+`` に対するマッチングを試してみましょう。
空の文字列は全くマッチしません、なぜなら ``+`` は「1回以上の繰り返し」を意味するからです。
この場合では :meth:`match` は ``None`` を返すべきで、インタプタは何も出力しません。
明確にするために :meth:`match` の結果を明示的に出力することもできます::

   >>> p.match("")
   >>> print p.match("")
   None

..
  Now, let's try it on a string that it should match, such as ``tempo``.  In this
  case, :meth:`match` will return a :class:`MatchObject`, so you should store the
  result in a variable for later use. ::

次に、 ``tempo`` のようなマッチすべき文字列を試してみましょう。
この場合 :meth:`match` は :class:`MatchObject` を返します、
後で使うために変数に結果を残す必要があります::

   >>> m = p.match('tempo')
   >>> print m
   <_sre.SRE_Match object at 0x...>

..
  Now you can query the :class:`MatchObject` for information about the matching
  string.   :class:`MatchObject` instances also have several methods and
  attributes; the most important ones are:

これで :class:`MatchObject` にマッチした文字列に対する情報を問い合わせることができます。
:class:`MatchObject` インスタンスもいくつかのメソッドと属性を持っています;
重要なものは:

..
  +------------------+--------------------------------------------+
  | Method/Attribute | Purpose                                    |
  +==================+============================================+
  | ``group()``      | Return the string matched by the RE        |
  +------------------+--------------------------------------------+
  | ``start()``      | Return the starting position of the match  |
  +------------------+--------------------------------------------+
  | ``end()``        | Return the ending position of the match    |
  +------------------+--------------------------------------------+
  | ``span()``       | Return a tuple containing the (start, end) |
  |                  | positions  of the match                    |
  +------------------+--------------------------------------------+

+------------------+--------------------------------------------+
| メソッド/属性    | 目的                                       |
+==================+============================================+
| ``group()``      | 正規表現にマッチした文字列を返す           |
+------------------+--------------------------------------------+
| ``start()``      | マッチの開始位置を返す                     |
+------------------+--------------------------------------------+
| ``end()``        | マッチの終了位置を返す                     |
+------------------+--------------------------------------------+
| ``span()``       | マッチの位置 (start, end) を               |
|                  | 含むタプルを返す                           |
+------------------+--------------------------------------------+

..
  Trying these methods will soon clarify their meaning::

これらのメソッドを試せば、その意味はすぐに理解できます::

   >>> m.group()
   'tempo'
   >>> m.start(), m.end()
   (0, 5)
   >>> m.span()
   (0, 5)

..
  :meth:`group` returns the substring that was matched by the RE.  :meth:`start`
  and :meth:`end` return the starting and ending index of the match. :meth:`span`
  returns both start and end indexes in a single tuple.  Since the :meth:`match`
  method only checks if the RE matches at the start of a string, :meth:`start`
  will always be zero.  However, the :meth:`search` method of patterns
  scans through the string, so  the match may not start at zero in that
  case. ::

:meth:`group` は正規表現にマッチした部分文字列を返します。
:meth:`start` と :meth:`end` はマッチの開始と終了のインデクスを返します。
:meth:`span` は開始と終了のインデクスの両方をを1つのタプルとして返します。
:meth:`match` メソッドは正規表現が文字列の最初にマッチするかどうかを調べるので、
:meth:`start` は常に0です。
ただし、 :meth:`search` メソッドは文字列に対してパターンを操作するので
その場合にはマッチが0から始まるとは限りません。::

   >>> print p.match('::: message')
   None
   >>> m = p.search('::: message') ; print m
   <_sre.SRE_Match object at 0x...>
   >>> m.group()
   'message'
   >>> m.span()
   (4, 11)

..
  In actual programs, the most common style is to store the :class:`MatchObject`
  in a variable, and then check if it was ``None``.  This usually looks like::

実際のプログラムでは :class:`MatchObject` を変数に記憶しておき,
その次に ``None`` なのか調べるのが一般的なスタイルです。
普通このようにします::

   p = re.compile( ... )
   m = p.match( 'string goes here' )
   if m:
       print 'Match found: ', m.group()
   else:
       print 'No match'

..
  Two pattern methods return all of the matches for a pattern.
  :meth:`findall` returns a list of matching strings::

2つのパターンメソッドはパターンにマッチした全てを返します。
:meth:`findall` はマッチした文字列のリストを返します::

   >>> p = re.compile('\d+')
   >>> p.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')
   ['12', '11', '10']

..
  :meth:`findall` has to create the entire list before it can be returned as the
  result.  The :meth:`finditer` method returns a sequence of :class:`MatchObject`
  instances as an :term:`iterator`. [#]_ ::

:meth:`findall` は結果が返される前に結果となるリスト全体を作成します。
:meth:`finditer` メソッドは :class:`MatchObject` インスタンスのシーケンスを
:term:`iterator` として返します。 [#]_ ::

   >>> iterator = p.finditer('12 drummers drumming, 11 ... 10 ...')
   >>> iterator
   <callable-iterator object at 0x401833ac>
   >>> for match in iterator:
   ...     print match.span()
   ...
   (0, 2)
   (22, 24)
   (29, 31)


..
  Module-Level Functions
  ----------------------

モジュールレベルの関数
----------------------

..
  You don't have to create a pattern object and call its methods; the
  :mod:`re` module also provides top-level functions called :func:`match`,
  :func:`search`, :func:`findall`, :func:`sub`, and so forth.  These functions
  take the same arguments as the corresponding pattern method, with
  the RE string added as the first argument, and still return either ``None`` or a
  :class:`MatchObject` instance. ::

パターンオブジェクトを作成し、メソッドを呼び出す必要はありません;
:mod:`re` モジュールはトップレベルの関数 :func:`match`, :func:`search`,
:func:`findall`, :func:`sub` 続々、も提供しています。
これらの関数は対応するパターンメソッドと同じ引数をとり、
正規表現文字列を最初の引数として追加して使います、
そして同じく ``None`` または :class:`MatchObject` インスタンスを返します::

   >>> print re.match(r'From\s+', 'Fromage amk')
   None
   >>> re.match(r'From\s+', 'From amk Thu May 14 19:12:10 1998')
   <_sre.SRE_Match object at 0x...>

..
  Under the hood, these functions simply create a pattern object for you
  and call the appropriate method on it.  They also store the compiled object in a
  cache, so future calls using the same RE are faster.

内部では、これらの関数は単にパターンオブジェクトを生成し、
その適切なメソッドを呼び出しています。
それらは、コンパイル済みのオブジェクトもキャッシュとして記憶するので、
同じ正規表現に対する将来の呼び出しは高速になります。

..
  Should you use these module-level functions, or should you get the
  pattern and call its methods yourself?  That choice depends on how
  frequently the RE will be used, and on your personal coding style.  If the RE is
  being used at only one point in the code, then the module functions are probably
  more convenient.  If a program contains a lot of regular expressions, or re-uses
  the same ones in several locations, then it might be worthwhile to collect all
  the definitions in one place, in a section of code that compiles all the REs
  ahead of time.  To take an example from the standard library, here's an extract
  from :file:`xmllib.py`::

これらのモジュールレベル関数を使うべきでしょうか、それともパターンを取得し、
メソッド自身を呼び出すべきでしょうか?
この選択は利用する正規表現がどのくらい頻繁に利用されるかと個人のコーディングスタイルに依存します。
正規表現がコード内で一度しか使われない場合、モジュール関数の方がより便利でしょう。
プログラムが多くの正規表現を含んだり、同じ正規表現がいくつかの場所で再利用されるときは
定義を一箇所にまとめ、使う前に全ての正規表現をコンパイルしておくことはやる価値があるはずです。
標準ライブラリから例を挙げます、 :file:`xmllib.py` から抜粋で::

   ref = re.compile( ... )
   entityref = re.compile( ... )
   charref = re.compile( ... )
   starttagopen = re.compile( ... )

..
  I generally prefer to work with the compiled object, even for one-time uses, but
  few people will be as much of a purist about this as I am.

私はたいていの場合、一回のみの利用であっても
コンパイル済みオブジェクトを使うことを好みますが、
そこまで厳格な人は少数派でしょう。

..
  Compilation Flags
  -----------------

コンパイルフラグ
----------------

..
  Compilation flags let you modify some aspects of how regular expressions work.
  Flags are available in the :mod:`re` module under two names, a long name such as
  :const:`IGNORECASE` and a short, one-letter form such as :const:`I`.  (If you're
  familiar with Perl's pattern modifiers, the one-letter forms use the same
  letters; the short form of :const:`re.VERBOSE` is :const:`re.X`, for example.)
  Multiple flags can be specified by bitwise OR-ing them; ``re.I | re.M`` sets
  both the :const:`I` and :const:`M` flags, for example.

コンパイルフラグは正規表現の動作をいくつかの側面から変更します。
フラグは :mod:`re` モジュール下で二つの名前で利用することができます、
例えば長い名前は :const:`IGNORECASE` で短い名前は1文字で :const:`I` のようになっています。
(1文字形式は Perl のパターン修飾子と同じ形式を使います;
例えば :const:`re.VERBOSE` の短かい形式は :const:`re.X` です。)
複数のフラグが OR ビット演算で指定することができます;
例えば ``re.I | re.M`` は :const:`I` と :const:`M` フラグの両方を設定します。

.. XXX todo bitwise OR modifier
..
  Here's a table of the available flags, followed by a more detailed explanation
  of each one.

ここに利用可能なフラグの表があります、それぞれについてのより詳細な説明が後に続きます。

..
  +---------------------------------+--------------------------------------------+
  | Flag                            | Meaning                                    |
  +=================================+============================================+
  | :const:`DOTALL`, :const:`S`     | Make ``.`` match any character, including  |
  |                                 | newlines                                   |
  +---------------------------------+--------------------------------------------+
  | :const:`IGNORECASE`, :const:`I` | Do case-insensitive matches                |
  +---------------------------------+--------------------------------------------+
  | :const:`LOCALE`, :const:`L`     | Do a locale-aware match                    |
  +---------------------------------+--------------------------------------------+
  | :const:`MULTILINE`, :const:`M`  | Multi-line matching, affecting ``^`` and   |
  |                                 | ``$``                                      |
  +---------------------------------+--------------------------------------------+
  | :const:`VERBOSE`, :const:`X`    | Enable verbose REs, which can be organized |
  |                                 | more cleanly and understandably.           |
  +---------------------------------+--------------------------------------------+

+---------------------------------+------------------------------------------------+
| フラグ                          | 意味                                           |
+=================================+================================================+
| :const:`DOTALL`, :const:`S`     | ``.`` を改行を含む任意の文字に                 |
|                                 | マッチするようにします                         |
+---------------------------------+------------------------------------------------+
| :const:`IGNORECASE`, :const:`I` | 大文字小文字を区別しないマッチを行います       |
+---------------------------------+------------------------------------------------+
| :const:`LOCALE`, :const:`L`     | ロケールに対応したマッチを行います             |
+---------------------------------+------------------------------------------------+
| :const:`MULTILINE`, :const:`M`  | ``^`` や ``$`` に作用して、                    |
|                                 | 複数行にマッチング                             |
+---------------------------------+------------------------------------------------+
| :const:`VERBOSE`, :const:`X`    | 冗長な正規表現を利用できるようにして、         |
|                                 | よりきれいで理解しやすくまとめることができます |
+---------------------------------+------------------------------------------------+

..
  .. data:: I
            IGNORECASE
     :noindex:
  
     Perform case-insensitive matching; character class and literal strings will
     match letters by ignoring case.  For example, ``[A-Z]`` will match lowercase
     letters, too, and ``Spam`` will match ``Spam``, ``spam``, or ``spAM``. This
     lowercasing doesn't take the current locale into account; it will if you also
     set the :const:`LOCALE` flag.


.. data:: I
          IGNORECASE
   :noindex:

   大文字小文字を区別しないマッチングを実行します;
   文字クラスや文字列リテラルは大文字小文字を無視してマッチします。
   例えば ``[A-Z]`` は小文字にもマッチします、また ``Spam`` は ``Spam``,
   ``spam``, または ``spAM`` にもマッチします。
   この小文字化は現在のロケールは考慮に入れません;
   ロケールの考慮は :const:`LOCALE` も設定することで行います。

..
  .. data:: L
            LOCALE
     :noindex:
  
     Make ``\w``, ``\W``, ``\b``, and ``\B``, dependent on the current locale.
  
     Locales are a feature of the C library intended to help in writing programs that
     take account of language differences.  For example, if you're processing French
     text, you'd want to be able to write ``\w+`` to match words, but ``\w`` only
     matches the character class ``[A-Za-z]``; it won't match ``'é'`` or ``'ç'``.  If
     your system is configured properly and a French locale is selected, certain C
     functions will tell the program that ``'é'`` should also be considered a letter.
     Setting the :const:`LOCALE` flag when compiling a regular expression will cause
     the resulting compiled object to use these C functions for ``\w``; this is
     slower, but also enables ``\w+`` to match French words as you'd expect.


.. data:: L
          LOCALE
   :noindex:

   ``\w``, ``\W``, ``\b``, そして ``\B`` を現在のロケールに依存させます。

   ロケールは C ライブラリの機能の一つで、言語の違いを考慮したプログラム作成を容易にするためのものです。
   例えば、フランス語の文書を処理したい場合、単語のマッチに ``\w+`` を利用したくなります、
   しかし、 ``\w`` は文字クラス ``[A-Za-z]`` のみとマッチします;
   ``'é'`` または ``'ç'`` にはマッチしません。
   システムが適切に設定されていて、ロケールがフランス語に設定されていれば、
   C 関数がプログラムに ``'é'`` をアルファベットとして扱うべきだと伝えます。
   :const:`LOCALE` フラグを正規表現のコンパイル時に設定することで、
   ``\w`` を使う C 関数を利用するコンパイル済みオブジェクトを生み出すことになります;
   これは速度は遅くなりますが、期待通りに ``\w+`` をフランス語の単語にマッチさせることができます。

..
  .. data:: M
            MULTILINE
     :noindex:
  
     (``^`` and ``$`` haven't been explained yet;  they'll be introduced in section
     :ref:`more-metacharacters`.)
  
     Usually ``^`` matches only at the beginning of the string, and ``$`` matches
     only at the end of the string and immediately before the newline (if any) at the
     end of the string. When this flag is specified, ``^`` matches at the beginning
     of the string and at the beginning of each line within the string, immediately
     following each newline.  Similarly, the ``$`` metacharacter matches either at
     the end of the string and at the end of each line (immediately preceding each
     newline).


.. data:: M
          MULTILINE
   :noindex:

   (``^`` と ``$`` についてはまだ説明していません;
   これらは :ref:`more-metacharacters` の節で説明します。)

   通常 ``^`` は文字列の先頭にマッチし、 ``$`` は文字列の末尾と
   文字列の末尾に改行(があれば)その直前にマッチします。
   このフラグが指定されると、 ``^`` は文字列の先頭と文字列の中の改行に続く各行の先頭にマッチします。
   同様に ``$`` 特殊文字は文字列の末尾と各行の末尾(各改行の直前)のどちらにもマッチします。


..
  .. data:: S
            DOTALL
     :noindex:
  
     Makes the ``'.'`` special character match any character at all, including a
     newline; without this flag, ``'.'`` will match anything *except* a newline.

.. data:: S
          DOTALL
   :noindex:

   特別な文字 ``'.'`` を改行を含む全ての任意の文字とマッチするようにします;
   このフラグが無しでは、 ``'.'`` は改行 *以外* の全てにマッチします。


..
  .. data:: X
            VERBOSE
     :noindex:
  
     This flag allows you to write regular expressions that are more readable by
     granting you more flexibility in how you can format them.  When this flag has
     been specified, whitespace within the RE string is ignored, except when the
     whitespace is in a character class or preceded by an unescaped backslash; this
     lets you organize and indent the RE more clearly.  This flag also lets you put
     comments within a RE that will be ignored by the engine; comments are marked by
     a ``'#'`` that's neither in a character class or preceded by an unescaped
     backslash.
  
     For example, here's a RE that uses :const:`re.VERBOSE`; see how much easier it
     is to read? ::
  
        charref = re.compile(r"""
         &[#]		     # Start of a numeric entity reference
         (
             0[0-7]+         # Octal form
           | [0-9]+          # Decimal form
           | x[0-9a-fA-F]+   # Hexadecimal form
         )
         ;                   # Trailing semicolon
        """, re.VERBOSE)
  
     Without the verbose setting, the RE would look like this::
  
        charref = re.compile("&#(0[0-7]+"
                             "|[0-9]+"
                             "|x[0-9a-fA-F]+);")
  
     In the above example, Python's automatic concatenation of string literals has
     been used to break up the RE into smaller pieces, but it's still more difficult
     to understand than the version using :const:`re.VERBOSE`.

.. data:: X
          VERBOSE
   :noindex:

   このフラグはより柔軟な形式で正規表現を読み易く書けるようにします。
   このフラグを指定すると、正規表現の中の空白は無視されます、
   ただし、文字クラス内やエスケープされていないバックスラッシュに続く空白の場合は例外として無視されません;
   これによって正規表現をまとめたり、インデントしてより明確にすることができます。
   このフラグはさらにエンジンが無視するコメントを追加することもできます;
   コメントは ``'#'`` で示します、これは文字クラスやエスケープされていないバックスラッシュに続くものであってはいけません。

   例えば、ここに :const:`re.VERBOSE` を利用した正規表現があります;
   読み易いと思いませんか? ::

      charref = re.compile(r"""
       &[#]		     # Start of a numeric entity reference
       (
           0[0-7]+         # Octal form
         | [0-9]+          # Decimal form
         | x[0-9a-fA-F]+   # Hexadecimal form
       )
       ;                   # Trailing semicolon
      """, re.VERBOSE)

   冗長な表現を利用しない設定の場合、正規表現はこうなります::

      charref = re.compile("&#(0[0-7]+"
                           "|[0-9]+"
                           "|x[0-9a-fA-F]+);")

   上の例では、Python の文字列リテラルの自動結合によって正規表現を小さな部分に分割しています、
   それでも :const:`re.VERBOSE` を使った場合に比べるとまだ難しくなっています。

..
  More Pattern Power
  ==================

パターンの能力をさらに
======================

..
  So far we've only covered a part of the features of regular expressions.  In
  this section, we'll cover some new metacharacters, and how to use groups to
  retrieve portions of the text that was matched.

ここまでで、正規表現の機能のほんの一部を扱ってきました。
この節では、新たにいくつかの特殊文字とグループを使ってマッチしたテキストの一部をどう取得するかについて扱います。

..
  More Metacharacters
  -------------------

.. _more-metacharacters:

さらなる特殊文字
----------------

..
  There are some metacharacters that we haven't covered yet.  Most of them will be
  covered in this section.

これまでで、まだ扱っていない特殊文字がいくつかありました。
そのほとんどをこの節で扱っていきます。

..
  Some of the remaining metacharacters to be discussed are :dfn:`zero-width
  assertions`.  They don't cause the engine to advance through the string;
  instead, they consume no characters at all, and simply succeed or fail.  For
  example, ``\b`` is an assertion that the current position is located at a word
  boundary; the position isn't changed by the ``\b`` at all.  This means that
  zero-width assertions should never be repeated, because if they match once at a
  given location, they can obviously be matched an infinite number of times.

残りの特殊文字の内いくつかは :dfn:`ゼロ幅アサーション zero-width-assertions` に関するものです。
これらは文字列に対してエンジンを進めません; 文字列を全く利用しない代わりに、
単純に成功か失敗かを利用します。
例えば、 ``\b`` は現在位置が単語の境界であることを示します;
``\b`` によってエンジンの読んでいる位置は全く変化しません。
つまり、これはゼロ幅アサーションは繰り返し使うことがありません、
一度ある位置でマッチしたら、明らかに無限回マッチできます。

..
  ``|``
     Alternation, or the "or" operator.   If A and B are regular expressions,
     ``A|B`` will match any string that matches either ``A`` or ``B``. ``|`` has very
     low precedence in order to make it work reasonably when you're alternating
     multi-character strings. ``Crow|Servo`` will match either ``Crow`` or ``Servo``,
     not ``Cro``, a ``'w'`` or an ``'S'``, and ``ervo``.
  
     To match a literal ``'|'``, use ``\|``, or enclose it inside a character class,
     as in ``[|]``.

``|``
   代替 (alternation) または "or" 演算子。
   A と B が正規表現の場合、 ``A|B`` は ``A`` または ``B`` のどちらの文字列にもマッチします。
   ``|`` は複数の文字列をかわるがわる試す場合でもうまく動作するように優先度はとても低くなっています
   ``Crow|Servo`` は ``Crow`` または ``Servo`` のどちらにもマッチします、
   ``Cro``, ``'w'`` または ``'S'``, ``ervo`` とはマッチしません。

   リテラル ``'|'`` にマッチするには、 ``\|`` を利用するか、
   ``[|]`` のように文字クラス内に収めて下さい。

..
  ``^``
     Matches at the beginning of lines.  Unless the :const:`MULTILINE` flag has been
     set, this will only match at the beginning of the string.  In :const:`MULTILINE`
     mode, this also matches immediately after each newline within the string.
  
     For example, if you wish to match the word ``From`` only at the beginning of a
     line, the RE to use is ``^From``. ::
  
        >>> print re.search('^From', 'From Here to Eternity')
        <_sre.SRE_Match object at 0x...>
        >>> print re.search('^From', 'Reciting From Memory')
        None
  
``^``
   行の先頭にマッチします。
   :const:`MULTILINE` フラグが設定されない場合には、文字列の先頭にのみマッチします。
   :const:`MULTILINE` モードでは文字列内の各改行の直後にマッチします。

   例えば、 行の先頭の ``From`` にのみマッチさせたい場合には
   ``^From`` 正規表現を利用します。 ::

      >>> print re.search('^From', 'From Here to Eternity')
      <_sre.SRE_Match object at 0x...>
      >>> print re.search('^From', 'Reciting From Memory')
      None

..
  ``$``
     Matches at the end of a line, which is defined as either the end of the string,
     or any location followed by a newline character.     ::
  
        >>> print re.search('}$', '{block}')
        <_sre.SRE_Match object at 0x...>
        >>> print re.search('}$', '{block} ')
        None
        >>> print re.search('}$', '{block}\n')
        <_sre.SRE_Match object at 0x...>
  
     To match a literal ``'$'``, use ``\$`` or enclose it inside a character class,
     as in  ``[$]``.

``$``
   行の末尾にマッチします、行の末尾は文字列の末尾と改行文字の直前として定義されます。 ::

      >>> print re.search('}$', '{block}')
      <_sre.SRE_Match object at 0x...>
      >>> print re.search('}$', '{block} ')
      None
      >>> print re.search('}$', '{block}\n')
      <_sre.SRE_Match object at 0x...>


   リテラル ``'$'`` にマッチするには、 ``\$`` を利用するか、
   ``[$]`` のように文字クラス内に収めて下さい。

..
  ``\A``
     Matches only at the start of the string.  When not in :const:`MULTILINE` mode,
     ``\A`` and ``^`` are effectively the same.  In :const:`MULTILINE` mode, they're
     different: ``\A`` still matches only at the beginning of the string, but ``^``
     may match at any location inside the string that follows a newline character.

``\A``
   文字列の先頭にのみマッチします。
   :const:`MULTILINE` モードでない場合には ``\A`` と ``^`` は実質的に同じです。
   :const:`MULTILINE` モードでのこれらの違いは:
   ``\A`` は依然として文字列の先頭にのみマッチしますが、
   ``^`` は文字列内に改行文字に続く部分があればそこにマッチすることです。

..
  ``\Z``
     Matches only at the end of the string.

``\Z``
   文字列の末尾にのみマッチします。

..
  ``\b``
     Word boundary.  This is a zero-width assertion that matches only at the
     beginning or end of a word.  A word is defined as a sequence of alphanumeric
     characters, so the end of a word is indicated by whitespace or a
     non-alphanumeric character.
  
     The following example matches ``class`` only when it's a complete word; it won't
     match when it's contained inside another word. ::
  
        >>> p = re.compile(r'\bclass\b')
        >>> print p.search('no class at all')
        <_sre.SRE_Match object at 0x...>
        >>> print p.search('the declassified algorithm')
        None
        >>> print p.search('one subclass is')
        None
  
     There are two subtleties you should remember when using this special sequence.
     First, this is the worst collision between Python's string literals and regular
     expression sequences.  In Python's string literals, ``\b`` is the backspace
     character, ASCII value 8.  If you're not using raw strings, then Python will
     convert the ``\b`` to a backspace, and your RE won't match as you expect it to.
     The following example looks the same as our previous RE, but omits the ``'r'``
     in front of the RE string. ::
  
        >>> p = re.compile('\bclass\b')
        >>> print p.search('no class at all')
        None
        >>> print p.search('\b' + 'class' + '\b')
        <_sre.SRE_Match object at 0x...>
  
     Second, inside a character class, where there's no use for this assertion,
     ``\b`` represents the backspace character, for compatibility with Python's
     string literals.

``\b``
   単語の境界。
   これはゼロ幅アサーションで、単語の始まりか終わりにのみマッチします。
   単語は英数文字のシーケンスとして定義されます、
   つまり単語の終わりは空白か非英数文字として表われます。

   以下の例では ``class`` がそのものの単語のときのみマッチします;
   別の単語内に含まれている場合はマッチしません。 ::

      >>> p = re.compile(r'\bclass\b')
      >>> print p.search('no class at all')
      <re.MatchObject instance at 80c8f28>
      >>> print p.search('the declassified algorithm')
      None
      >>> print p.search('one subclass is')
      None

   この特別なシーケンスを利用するときには二つの微妙な点を心にとめておく必要があります。
   まずひとつめは Python の文字列リテラルと表現の間の最悪の衝突を引き起すことです。
   Python の文字列リテラルでは ``\b`` は ASCII 値8のバックスペース文字です。
   raw string を利用していない場合、Python は ``\b`` をバックスペースに変換し、
   正規表現は期待するものとマッチしなくなります。
   以下の例はさきほどと同じ正規表現のように見えますが、
   正規表現文字列の前の ``'r'`` が省略されています::

      >>> p = re.compile('\bclass\b')
      >>> print p.search('no class at all')
      None
      >>> print p.search('\b' + 'class' + '\b')
      <re.MatchObject instance at 80c3ee0>

   ふたつめはこのアサーションが利用できない文字列クラスの内部では
   Python の文字列リテラルとの互換性のために、
   ``\b`` はバックスペース文字を表わすことになるということです。

..
  ``\B``
     Another zero-width assertion, this is the opposite of ``\b``, only matching when
     the current position is not at a word boundary.

``\B``
   
   別のゼロ幅アサーションで、 ``\b`` と逆で、
   現在の位置が単語の境界でないときにのみマッチします。

..
  Grouping
  --------

グルーピング
------------

..
  Frequently you need to obtain more information than just whether the RE matched
  or not.  Regular expressions are often used to dissect strings by writing a RE
  divided into several subgroups which match different components of interest.
  For example, an RFC-822 header line is divided into a header name and a value,
  separated by a ``':'``, like this::

正規表現にマッチするかどうかだけでなく、より多くの情報を得なければいけない場合は
多々あります。
正規表現はしばしば、正規表現をいくつかのサブグループに分けて
興味ある部分にマッチするようにして、文字列を分割するのに使われます。
例えば、 RFC-822 ヘッダ行は ``':'`` を挟んでこのようにヘッダ名と値に分割されます::

   From: author@example.com
   User-Agent: Thunderbird 1.5.0.9 (X11/20061227)
   MIME-Version: 1.0
   To: editor@example.com

..
  This can be handled by writing a regular expression which matches an entire
  header line, and has one group which matches the header name, and another group
  which matches the header's value.

これはヘッダ全体にマッチし、そしてヘッダ名にマッチするグループと
ヘッダの値にマッチする別のグループを持つように
正規表現を書くことで扱うことができます、

..
  Groups are marked by the ``'('``, ``')'`` metacharacters. ``'('`` and ``')'``
  have much the same meaning as they do in mathematical expressions; they group
  together the expressions contained inside them, and you can repeat the contents
  of a group with a repeating qualifier, such as ``*``, ``+``, ``?``, or
  ``{m,n}``.  For example, ``(ab)*`` will match zero or more repetitions of
  ``ab``. ::

グループは特殊文字 ``'('``, ``')'`` で表わされます。
``'('`` と ``')'`` は数学での意味とほぼ同じ意味を持っています;
その中に含まれた表現はまとめてグループ化され、
グループの中身を ``*``, ``+``, ``?`` や ``{m,n}`` のような繰り返しの修飾子を
使って繰り返すことができます。
例えば、 ``(ab)*`` は ``ab`` の0回以上の繰り返しにマッチします。 ::

   >>> p = re.compile('(ab)*')
   >>> print p.match('ababababab').span()
   (0, 10)

..
  Groups indicated with ``'('``, ``')'`` also capture the starting and ending
  index of the text that they match; this can be retrieved by passing an argument
  to :meth:`group`, :meth:`start`, :meth:`end`, and :meth:`span`.  Groups are
  numbered starting with 0.  Group 0 is always present; it's the whole RE, so
  :class:`MatchObject` methods all have group 0 as their default argument.  Later
  we'll see how to express groups that don't capture the span of text that they
  match. ::

``'('`` と ``')'`` で示されたグループはマッチしたテキストの開始と末尾のインデクスも
capture できます;
インデクスは :meth:`group`, :meth:`start`, :meth:`end`, and :meth:`span` に
引数を与えることで取得できます。
グループは 0 から番号付けされます。
グループ 0 は常に存在し; 正規表現全体です、つまり
:class:`MatchObject` メソッドは常にグループ0 をデフォルト引数として持っています。
マッチしたテキストの範囲を capture しないグループの表し方については後で扱います::

   >>> p = re.compile('(a)b')
   >>> m = p.match('ab')
   >>> m.group()
   'ab'
   >>> m.group(0)
   'ab'

..
  Subgroups are numbered from left to right, from 1 upward.  Groups can be nested;
  to determine the number, just count the opening parenthesis characters, going
  from left to right. ::

サブグループは左から右へ1づつ番号付けされます。
グループはネストしてもかまいません;
番号を決めるには、単に開き括弧を左から右へ数え上げます::

   >>> p = re.compile('(a(b)c)d')
   >>> m = p.match('abcd')
   >>> m.group(0)
   'abcd'
   >>> m.group(1)
   'abc'
   >>> m.group(2)
   'b'

..
  :meth:`group` can be passed multiple group numbers at a time, in which case it
  will return a tuple containing the corresponding values for those groups. ::

:meth:`group` には一回に複数の引数を渡してもかまいません、
その場合にはそれらのグループに対応する値を含むタプルを返します。 ::

   >>> m.group(2,1,2)
   ('b', 'abc', 'b')

..
  The :meth:`groups` method returns a tuple containing the strings for all the
  subgroups, from 1 up to however many there are. ::

:meth:`groups` メソッドは 1 から全てのサブグループの文字列を含むタプルを返します。::

   >>> m.groups()
   ('abc', 'b')

..
  Backreferences in a pattern allow you to specify that the contents of an earlier
  capturing group must also be found at the current location in the string.  For
  example, ``\1`` will succeed if the exact contents of group 1 can be found at
  the current position, and fails otherwise.  Remember that Python's string
  literals also use a backslash followed by numbers to allow including arbitrary
  characters in a string, so be sure to use a raw string when incorporating
  backreferences in a RE.

パターン中で後方参照を利用することで、
前に取り出されたグループが文字列の中の現在位置で見つかるように指定できます。
例えば、 ``\1`` はグループ1の内容が現在位置で見つかった場合成功し、
それ以外の場合に失敗します。
Python の文字列リテラルでもバックスラッシュに続く数字は
任意の文字を文字列に含めるために使われるということを心に留めておいて下さい、
そのため正規表現で後方参照を含む場合には raw string を必ず利用して下さい。

..
  For example, the following RE detects doubled words in a string. ::

例えば、以下の正規表現は二重になった単語を検出します。 ::

   >>> p = re.compile(r'(\b\w+)\s+\1')
   >>> p.search('Paris in the the spring').group()
   'the the'

..
  Backreferences like this aren't often useful for just searching through a string
  --- there are few text formats which repeat data in this way --- but you'll soon
  find out that they're *very* useful when performing string substitutions.

このような後方参照は文字列を検索するだけの用途では多くの場合役に立ちません。
--- このように繰り返されるテキストフォーマットは少数です。---
しかし、文字列の置換をする場合には *とても* 有効であることに気づくでしょう。

..
  Non-capturing and Named Groups
  ------------------------------

取り出さないグループと名前つきグループ
--------------------------------------

..
  Elaborate REs may use many groups, both to capture substrings of interest, and
  to group and structure the RE itself.  In complex REs, it becomes difficult to
  keep track of the group numbers.  There are two features which help with this
  problem.  Both of them use a common syntax for regular expression extensions, so
  we'll look at that first.

念入りに作られた正規表現は多くのグループを利用します、
その利用法には対象となる部分文字列を取り出す、
正規表現自身をグループ化したり構造化する、という二つの方法があります。
複雑な正規表現では、グループ番号を追っていくことは困難になっていきます。
この問題の解決を助ける二つの機能があります。
その両方が正規表現を拡張するための一般的な構文を利用します、
まずはそれらをみてみましょう。

..
  Perl 5 added several additional features to standard regular expressions, and
  the Python :mod:`re` module supports most of them.   It would have been
  difficult to choose new single-keystroke metacharacters or new special sequences
  beginning with ``\`` to represent the new features without making Perl's regular
  expressions confusingly different from standard REs.  If you chose ``&`` as a
  new metacharacter, for example, old expressions would be assuming that ``&`` was
  a regular character and wouldn't have escaped it by writing ``\&`` or ``[&]``.

Perl 5 は標準の正規表現にいくつかの機能が追加されました、
Python の :mod:`re` モジュールもその内のほとんどをサポートしています。
Perl の正規表現が標準の正規表現の違いが混乱を招かないように、
新たな一文字の特殊文字や ``\`` で始まる新しい特殊シーケンスを選ぶことは困難でした。
新しい特殊文字として ``&`` を選ぶとすると古い正規表現では ``&`` を通常の文字とみなされ、
``\&`` や ``[&]`` と書くようにエスケープされません。

..
  The solution chosen by the Perl developers was to use ``(?...)`` as the
  extension syntax.  ``?`` immediately after a parenthesis was a syntax error
  because the ``?`` would have nothing to repeat, so this didn't introduce any
  compatibility problems.  The characters immediately after the ``?``  indicate
  what extension is being used, so ``(?=foo)`` is one thing (a positive lookahead
  assertion) and ``(?:foo)`` is something else (a non-capturing group containing
  the subexpression ``foo``).

解決策として Perl 開発者が選んだものは ``(?...)`` を正規表現構文として利用することでした。
括弧の直後の ``?`` は構文エラーとなります、これは ``?`` で繰り返す対象がないためです、
そのためこれは互換性の問題を持ち込みません。
``?`` の直後の文字はどの拡張が利用されるかを示しています、
つまり、 ``(?=foo)`` は一つの拡張を利用したもの (肯定先読みアサーション) となり、
``(?:foo)`` は別の拡張を利用した表現(``foo`` を含む取り込まないグループ)となります。

..
  Python adds an extension syntax to Perl's extension syntax.  If the first
  character after the question mark is a ``P``, you know that it's an extension
  that's specific to Python.  Currently there are two such extensions:
  ``(?P<name>...)`` defines a named group, and ``(?P=name)`` is a backreference to
  a named group.  If future versions of Perl 5 add similar features using a
  different syntax, the :mod:`re` module will be changed to support the new
  syntax, while preserving the Python-specific syntax for compatibility's sake.

Python は Perl の拡張構文にさらに拡張構文を加えています。
クエスチョンマークの後の最初の文字が ``P`` の場合、それが Python 特有の拡張であることを示しています。
現在では二つの拡張が存在しています:
``(?P<name>...)`` は名前つきグループを定義し、 ``(?P=name)`` は名前つきグループに対する後方参照となります。
Perl 5 の将来のバージョンで同様の機能が別の構文を利用して追加された場合、
:mod:`re` モジュールは互換性のために Python 特有の構文を残しつつ、
新しい構文をサポートするように変更されます。

..
  Now that we've looked at the general extension syntax, we can return to the
  features that simplify working with groups in complex REs. Since groups are
  numbered from left to right and a complex expression may use many groups, it can
  become difficult to keep track of the correct numbering.  Modifying such a
  complex RE is annoying, too: insert a new group near the beginning and you
  change the numbers of everything that follows it.

さて、ここまでで一般的な拡張構文を見てきたので、
複雑な正規表現を単純化するための機能について話を戻しましょう。
グループは左から右に番号づけされ、複雑な正規表現は多くの番号を利用することになるので、
正確な番号づけを追い続けることは難しくなります。
そのような複雑な正規表現を変更することは悩ましい問題となります:
正規表現の先頭に新しいグループを挿入すれば、それ以後の全ての番号を変更することにまります。

..
  Sometimes you'll want to use a group to collect a part of a regular expression,
  but aren't interested in retrieving the group's contents. You can make this fact
  explicit by using a non-capturing group: ``(?:...)``, where you can replace the
  ``...`` with any other regular expression. ::

グループの内容を取得することなく、正規表現の一部を集めるために、
グループを利用したくなることがよくあります。
このことを、取り込まないグループを使うことで明示的に示すことができます:
``(?:...)``, ``...`` は任意の正規表現に置き換えることができます。::

   >>> m = re.match("([abc])+", "abc")
   >>> m.groups()
   ('c',)
   >>> m = re.match("(?:[abc])+", "abc")
   >>> m.groups()
   ()

..
  Except for the fact that you can't retrieve the contents of what the group
  matched, a non-capturing group behaves exactly the same as a capturing group;
  you can put anything inside it, repeat it with a repetition metacharacter such
  as ``*``, and nest it within other groups (capturing or non-capturing).
  ``(?:...)`` is particularly useful when modifying an existing pattern, since you
  can add new groups without changing how all the other groups are numbered.  It
  should be mentioned that there's no performance difference in searching between
  capturing and non-capturing groups; neither form is any faster than the other.

マッチしたグループの内容を取得しないということを除けば、
取り込まないグループは厳密に取り込むグループと同様に振る舞います;
この中に何を入れてもかまいません、 ``*`` のような繰り返しの特殊文字で繰り返したり、
他のグループ (取り込むまたは取り込まない) の入れ子にすることもでいます。
``(?:...)`` は特に、既にあるパターンを変更する際に便利です、
なぜなら他の番号づけ新しいグループを変更することなく新しいグループを追加することができます。
取り込むグループと取り込まないグループで検索のパフォーマンスに差がないことにも触れておくべきことです;
どちらも同じ速度で動作します。

..
  A more significant feature is named groups: instead of referring to them by
  numbers, groups can be referenced by a name.

より重要な機能は名前つきグループです: 番号で参照する代わりに、グループに対して名前で参照できます。

..
  The syntax for a named group is one of the Python-specific extensions:
  ``(?P<name>...)``.  *name* is, obviously, the name of the group.  Named groups
  also behave exactly like capturing groups, and additionally associate a name
  with a group.  The :class:`MatchObject` methods that deal with capturing groups
  all accept either integers that refer to the group by number or strings that
  contain the desired group's name.  Named groups are still given numbers, so you
  can retrieve information about a group in two ways::

名前つきグループの構文は Python 特有の拡張 :``(?P<name>...)`` です。
*name* は、もちろん、グループの名前です。
名前つきグループも厳密に取り込むグループのように振る舞い、
さらにグループを名前と関連づけます。
取り込むグループを扱う :class:`MatchObject` のメソッドは全て、
グループ番号を参照するための整数と欲しいグループの名前を含む文字列を受け付けます。
名前つきグループは番号も与えられているので、
2通りの方法で情報を取得できます::

   >>> p = re.compile(r'(?P<word>\b\w+\b)')
   >>> m = p.search( '(((( Lots of punctuation )))' )
   >>> m.group('word')
   'Lots'
   >>> m.group(1)
   'Lots'

..
  Named groups are handy because they let you use easily-remembered names, instead
  of having to remember numbers.  Here's an example RE from the :mod:`imaplib`
  module::

名前つきグループは、番号を覚える代わりに、簡単に覚えられる名前を利用できるので、簡単に扱うことができます。
これは :mod:`imaplib` モジュールから正規表現の例です::

   InternalDate = re.compile(r'INTERNALDATE "'
           r'(?P<day>[ 123][0-9])-(?P<mon>[A-Z][a-z][a-z])-'
   	r'(?P<year>[0-9][0-9][0-9][0-9])'
           r' (?P<hour>[0-9][0-9]):(?P<min>[0-9][0-9]):(?P<sec>[0-9][0-9])'
           r' (?P<zonen>[-+])(?P<zoneh>[0-9][0-9])(?P<zonem>[0-9][0-9])'
           r'"')

..
  It's obviously much easier to retrieve ``m.group('zonem')``, instead of having
  to remember to retrieve group 9.

取得する番号9を覚えるよりも、 ``m.group('zonem')`` で取得した方が明らかに簡単にすみます。

..
  The syntax for backreferences in an expression such as ``(...)\1`` refers to the
  number of the group.  There's naturally a variant that uses the group name
  instead of the number. This is another Python extension: ``(?P=name)`` indicates
  that the contents of the group called *name* should again be matched at the
  current point.  The regular expression for finding doubled words,
  ``(\b\w+)\s+\1`` can also be written as ``(?P<word>\b\w+)\s+(?P=word)``::

後方参照のための構文 ``(...)\1`` はグループ番号を参照します。
グループ番号の代わりに、グループ名を利用する変種があるのは当然でしょう。
これはもう一つの Python 拡張です: ``(?=name)`` は
*name* と呼ばれるグループの内容を表わし現在位置で再びマッチされます。
二重になった単語を見つける正規表現 ``(\b\w+)\s+\1`` は ``(?P<word>\b\w+)\s+(?P=word)``
のように書くことができます::

   >>> p = re.compile(r'(?P<word>\b\w+)\s+(?P=word)')
   >>> p.search('Paris in the the spring').group()
   'the the'


..
  Lookahead Assertions
  --------------------

先読みアサーション (Lookahead Assertions)
-----------------------------------------

..
  Another zero-width assertion is the lookahead assertion.  Lookahead assertions
  are available in both positive and negative form, and  look like this:

他のゼロ幅アサーションは先読みアサーションです。
先読みアサーションは肯定、否定の両方の形式が利用可能です、これを見てください:

..
  ``(?=...)``
     Positive lookahead assertion.  This succeeds if the contained regular
     expression, represented here by ``...``, successfully matches at the current
     location, and fails otherwise. But, once the contained expression has been
     tried, the matching engine doesn't advance at all; the rest of the pattern is
     tried right where the assertion started.
  
  ``(?!...)``
     Negative lookahead assertion.  This is the opposite of the positive assertion;
     it succeeds if the contained expression *doesn't* match at the current position
     in the string.

``(?=...)``
   肯定先読みアサーション。
   ``...`` で表わす正規表現が現在位置でマッチすれば成功し、それ以外の場合失敗します。
   しかし、表現が試行された場合でもエンジンは先に進みません;
   パターンの残りの部分はアサーションの開始時点から右に試行します。

``(?!...)``
   否定先読みアサーション。
   これは肯定アサーションの逆で、正規表現が文字列の現在位置にマッチ *しなかった* 場合に成功します。

..
  To make this concrete, let's look at a case where a lookahead is useful.
  Consider a simple pattern to match a filename and split it apart into a base
  name and an extension, separated by a ``.``.  For example, in ``news.rc``,
  ``news`` is the base name, and ``rc`` is the filename's extension.

より具体的にするため、先読みが便利な場合をみてみましょう。
ファイル名にマッチし、 ``.`` で分けられた基本部分と拡張子に分離する単純なパターンを考えましょう。
例えば、 ``news.rc`` は ``news`` が基本部分で ``rc`` がファイル名の拡張子です。

..
  The pattern to match this is quite simple:

マッチするパターンはとても単純です:

``.*[.].*$``

..
  Notice that the ``.`` needs to be treated specially because it's a
  metacharacter; I've put it inside a character class.  Also notice the trailing
  ``$``; this is added to ensure that all the rest of the string must be included
  in the extension.  This regular expression matches ``foo.bar`` and
  ``autoexec.bat`` and ``sendmail.cf`` and ``printers.conf``.

``.`` を特別に扱う必要があることに注意して下さい、なぜならこれは特殊文字だからです;
上では文字クラス内に入れました。
また ``$`` が続いていることにも注意して下さい;
これは文字列の残り全てが拡張子に含まれることを保障するために追加されています。
この正規表現は ``foo.bar``, ``autoexec.bat``, ``sendmail.cf``, ``printers.conf`` にマッチします。

..
  Now, consider complicating the problem a bit; what if you want to match
  filenames where the extension is not ``bat``? Some incorrect attempts:

さて、問題を少し複雑にしてみましょう; 
拡張子が ``bat`` でないファイル名にマッチしたい場合はどうでしょう？
間違った試み:

..
  ``.*[.][^b].*$``  The first attempt above tries to exclude ``bat`` by requiring
  that the first character of the extension is not a ``b``.  This is wrong,
  because the pattern also doesn't match ``foo.bar``.

``.*[.][^b].*$``  この最初の ``bat`` を除く試みは、最初の文字が ``b`` でないことを要求します。
これは誤っています、なぜなら ``foo.bar`` にもマッチしないからです。

``.*[.]([^b]..|.[^a].|..[^t])$``

..
  The expression gets messier when you try to patch up the first solution by
  requiring one of the following cases to match: the first character of the
  extension isn't ``b``; the second character isn't ``a``; or the third character
  isn't ``t``.  This accepts ``foo.bar`` and rejects ``autoexec.bat``, but it
  requires a three-letter extension and won't accept a filename with a two-letter
  extension such as ``sendmail.cf``.  We'll complicate the pattern again in an
  effort to fix it.

正規表現が混乱してきました。最初の解決策を取り繕って、
以下の場合に合わせることを要求しています: 拡張子の最初の文字は ``b`` でなく;
二番目の文字は ``a`` でなく; 三番目の文字は ``t`` でない。
これは ``foo.bar`` を受け付けますが、 ``autoexec.bat`` は拒否します。
しかし、三文字の拡張子を要求し、 ``sendmail.cf`` のような二文字の拡張子を受け付けません。
これを修正するのにパターンを再び複雑にすることになります。

``.*[.]([^b].?.?|.[^a]?.?|..?[^t]?)$``

..
  In the third attempt, the second and third letters are all made optional in
  order to allow matching extensions shorter than three characters, such as
  ``sendmail.cf``.

三番目の試みでは、 ``sendmail.cf`` のように三文字より短い拡張子とマッチするために
第二第三の文字を全てオプションにしています。

..
  The pattern's getting really complicated now, which makes it hard to read and
  understand.  Worse, if the problem changes and you want to exclude both ``bat``
  and ``exe`` as extensions, the pattern would get even more complicated and
  confusing.

パターンはさらに複雑さを増し、読みにくく、理解が難しくなりました。
より悪いことに、問題が ``bat`` と ``exe`` 両方を拡張子から除きたい場合に変わった場合、
パターンはより複雑で混乱しやすいものになります。

..
  A negative lookahead cuts through all this confusion:

否定先読みはこの混乱全てを取り除きます:

..
  ``.*[.](?!bat$).*$``  The negative lookahead means: if the expression ``bat``
  doesn't match at this point, try the rest of the pattern; if ``bat$`` does
  match, the whole pattern will fail.  The trailing ``$`` is required to ensure
  that something like ``sample.batch``, where the extension only starts with
  ``bat``, will be allowed.

``.*[.](?!bat$).*$`` 否定先読みは以下を意味します:
この位置で拡張子 ``bat`` にマッチしない場合、残りのパターンが試行されます;
もし ``bat$`` にマッチすればパターン全体が失敗します。
``$`` を続けることで、 ``sample.batch`` にように ``bat`` で始まる拡張子を許容することを保証しています。

..
  Excluding another filename extension is now easy; simply add it as an
  alternative inside the assertion.  The following pattern excludes filenames that
  end in either ``bat`` or ``exe``:

他のファイル名の拡張子を除くことも簡単です; 単純に
アサーション内に拡張子を代替 (or) で加えます。
以下のパターンは ``bat`` や ``exe`` のどちらで終わるファイル名を除外します:

``.*[.](?!bat$|exe$).*$``

..
  Modifying Strings
  =================

文字列を変更する
================

..
  Up to this point, we've simply performed searches against a static string.
  Regular expressions are also commonly used to modify strings in various ways,
  using the following pattern methods:

ここまででは単純に静的な文字列に対する検索を実行してきました。
正規表現は文字列を様々な方法で変更するのにもよく使われます。
変更には以下のパターンメソッドが利用されます:

..
  +------------------+-----------------------------------------------+
  | Method/Attribute | Purpose                                       |
  +==================+===============================================+
  | ``split()``      | Split the string into a list, splitting it    |
  |                  | wherever the RE matches                       |
  +------------------+-----------------------------------------------+
  | ``sub()``        | Find all substrings where the RE matches, and |
  |                  | replace them with a different string          |
  +------------------+-----------------------------------------------+
  | ``subn()``       | Does the same thing as :meth:`sub`,  but      |
  |                  | returns the new string and the number of      |
  |                  | replacements                                  |
  +------------------+-----------------------------------------------+

+------------------+-----------------------------------------------+
| メソッド/属性    | 目的                                          |
+==================+===============================================+
| ``split()``      | 文字列をリストに分割する、                    |
|                  | 正規表現がマッチした全ての場所で分割を行う    |
+------------------+-----------------------------------------------+
| ``sub()``        | 正規表現にマッチした全ての文字列を発見し、    |
|                  | 別の文字列に置き換えます                      |
+------------------+-----------------------------------------------+
| ``subn()``       | :meth:`sub` と同じことをしますが、            |
|                  | 新しい文字列と置き換えの回数を返します        |
+------------------+-----------------------------------------------+

..
  Splitting Strings
  -----------------

文字列の分割
------------

..
  The :meth:`split` method of a pattern splits a string apart
  wherever the RE matches, returning a list of the pieces. It's similar to the
  :meth:`split` method of strings but provides much more generality in the
  delimiters that you can split by; :meth:`split` only supports splitting by
  whitespace or by a fixed string.  As you'd expect, there's a module-level
  :func:`re.split` function, too.

パターンの :meth:`split` メソッドは正規表現にマッチした全ての場所で文字列を分割し、
各部分のリストを返します。
これは文字列の :meth:`split` メソッドに似ていますが、
より一般的なデリミタを提供します;
:meth:`split` は空白や固定文字列による分割のみをサポートしてます。
期待しているとおり、 モジュールレベルの :func:`re.split` 関数もそうです。

..
  .. method:: .split(string [, maxsplit=0])
     :noindex:
  
     Split *string* by the matches of the regular expression.  If capturing
     parentheses are used in the RE, then their contents will also be returned as
     part of the resulting list.  If *maxsplit* is nonzero, at most *maxsplit* splits
     are performed.

.. method:: .split(string [, maxsplit=0])
   :noindex:

   *string* を正規表現のマッチで分割します。
   正規表現内に取り込むための括弧が利用されている場合、
   その内容も結果のリストの一部として返されます。
   *maxsplit* が非ゼロの場合、最大で *maxsplit* の分割が実行されます。

..
  You can limit the number of splits made, by passing a value for *maxsplit*.
  When *maxsplit* is nonzero, at most *maxsplit* splits will be made, and the
  remainder of the string is returned as the final element of the list.  In the
  following example, the delimiter is any sequence of non-alphanumeric characters.
  ::

*maxsplit* に値を渡すことで、分割される回数を制限することができます。
*maxsplit* が非ゼロの場合、最大で *maxsplit* の分割が行なわれ、
文字列の残りがリストの最終要素として返されます。
以下の例では、デリミタは任意の英数文字のシーケンスです。
::

   >>> p = re.compile(r'\W+')
   >>> p.split('This is a test, short and sweet, of split().')
   ['This', 'is', 'a', 'test', 'short', 'and', 'sweet', 'of', 'split', '']
   >>> p.split('This is a test, short and sweet, of split().', 3)
   ['This', 'is', 'a', 'test, short and sweet, of split().']

..
  Sometimes you're not only interested in what the text between delimiters is, but
  also need to know what the delimiter was.  If capturing parentheses are used in
  the RE, then their values are also returned as part of the list.  Compare the
  following calls::

興味の対象がデリミタの間のテキストだけでなく、デリミタが何なのかということを知りたい場合はよくあります。
取りこみ用の括弧を正規表現に使った場合、その値もリストの一部として返されます。
以下の呼び出しを比較してみましょう::

   >>> p = re.compile(r'\W+')
   >>> p2 = re.compile(r'(\W+)')
   >>> p.split('This... is a test.')
   ['This', 'is', 'a', 'test', '']
   >>> p2.split('This... is a test.')
   ['This', '... ', 'is', ' ', 'a', ' ', 'test', '.', '']

..
  The module-level function :func:`re.split` adds the RE to be used as the first
  argument, but is otherwise the same.   ::

モジュールレベル関数 :func:`re.split` は最初の引数に利用する正規表現を追加しますが、
それ以外は同じです。::

   >>> re.split('[\W]+', 'Words, words, words.')
   ['Words', 'words', 'words', '']
   >>> re.split('([\W]+)', 'Words, words, words.')
   ['Words', ', ', 'words', ', ', 'words', '.', '']
   >>> re.split('[\W]+', 'Words, words, words.', 1)
   ['Words', 'words, words.']


..
  Search and Replace
  ------------------

検索と置換
----------

..
  Another common task is to find all the matches for a pattern, and replace them
  with a different string.  The :meth:`sub` method takes a replacement value,
  which can be either a string or a function, and the string to be processed.

もう一つのよくある作用は、パターンにマッチする全てを探し、異なる文字列に置換します。
:meth:`sub` メソッドは置換する値をとります、
文字列と関数の両方をとることができ、文字列を処理します。

..
  .. method:: .sub(replacement, string[, count=0])
     :noindex:
  
     Returns the string obtained by replacing the leftmost non-overlapping
     occurrences of the RE in *string* by the replacement *replacement*.  If the
     pattern isn't found, *string* is returned unchanged.
  
     The optional argument *count* is the maximum number of pattern occurrences to be
     replaced; *count* must be a non-negative integer.  The default value of 0 means
     to replace all occurrences.

.. method:: .sub(replacement, string[, count=0])
   :noindex:

   *string* 内で最も長く、他の部分と重複するところがない正規表現をを *replacement* に置換した文字列を返します。
   パターンが見つからなかった場合 *string* は変更されずに返されます。

   オプション引数 *count* はパターンの出現の最大置換回数です;
   *count* は非負の整数でなければいけません。
   デフォルト値 0 は全ての出現で置換することを意味します。

..
  Here's a simple example of using the :meth:`sub` method.  It replaces colour
  names with the word ``colour``::

ここに :meth:`sub` メソッドを使った単純な例があります。
これは色の名前を ``colour`` に置換します::

   >>> p = re.compile( '(blue|white|red)')
   >>> p.sub( 'colour', 'blue socks and red shoes')
   'colour socks and colour shoes'
   >>> p.sub( 'colour', 'blue socks and red shoes', count=1)
   'colour socks and red shoes'

..
  The :meth:`subn` method does the same work, but returns a 2-tuple containing the
  new string value and the number of replacements  that were performed::

:meth:`subn` メソッドも同じ働きをします、ただ新しい文字列と置換の実行回数を含む 2-タプルを返します::

   >>> p = re.compile( '(blue|white|red)')
   >>> p.subn( 'colour', 'blue socks and red shoes')
   ('colour socks and colour shoes', 2)
   >>> p.subn( 'colour', 'no colours at all')
   ('no colours at all', 0)

..
  Empty matches are replaced only when they're not adjacent to a previous match.
  ::

空文字列とのマッチは直前にマッチした部分と隣接していない場合にのみ置換されます。
::

   >>> p = re.compile('x*')
   >>> p.sub('-', 'abxd')
   '-a-b-d-'

..
  If *replacement* is a string, any backslash escapes in it are processed.  That
  is, ``\n`` is converted to a single newline character, ``\r`` is converted to a
  carriage return, and so forth. Unknown escapes such as ``\j`` are left alone.
  Backreferences, such as ``\6``, are replaced with the substring matched by the
  corresponding group in the RE.  This lets you incorporate portions of the
  original text in the resulting replacement string.

*replacement* が文字列の場合、文字列内のバックスラッシュエスケープは処理されます。
つまり、 ``\n`` は改行文字に ``\r`` はキャリッジリターンに、等となります。
``\j`` のような未知のエスケープシーケンスはそのまま残されます。
``\6`` のような後方参照は正規表現内の対応するグループにマッチする文字列に置換されます。
これを使うことで元のテキストの一部を、置換後の文字列に組み込むことができます。

..
  This example matches the word ``section`` followed by a string enclosed in
  ``{``, ``}``, and changes ``section`` to ``subsection``::

この例は単語 ``section`` に続く ``{`` と ``}`` で閉じられた文字列にマッチし、
``section`` を ``subsection`` に変更します::

   >>> p = re.compile('section{ ( [^}]* ) }', re.VERBOSE)
   >>> p.sub(r'subsection{\1}','section{First} section{second}')
   'subsection{First} subsection{second}'

..
  There's also a syntax for referring to named groups as defined by the
  ``(?P<name>...)`` syntax.  ``\g<name>`` will use the substring matched by the
  group named ``name``, and  ``\g<number>``  uses the corresponding group number.
  ``\g<2>`` is therefore equivalent to ``\2``,  but isn't ambiguous in a
  replacement string such as ``\g<2>0``.  (``\20`` would be interpreted as a
  reference to group 20, not a reference to group 2 followed by the literal
  character ``'0'``.)  The following substitutions are all equivalent, but use all
  three variations of the replacement string. ::

``(?P<name>...)`` 構文で定義された名前つきグループを参照するための構文もあります。
``\g<name>`` は ``name`` で名前づけされたグループにマッチする文字列を利用し、
``\g<number>`` は対応するグループ番号を利用します。
つまり ``\g<2>`` は ``\2`` と等価ですが、 ``\g<2>0`` のような置換文字列に対しては明確に異なります。
(``\20`` はグループ番号20への参照と解釈され、グループ2の後にリテラル文字 ``'0'`` が続くとは解釈されません。)
以下に示す置換は全て等価ですが、これらは文字列置換に全部で3種の変種を利用しています。::

   >>> p = re.compile('section{ (?P<name> [^}]* ) }', re.VERBOSE)
   >>> p.sub(r'subsection{\1}','section{First}')
   'subsection{First}'
   >>> p.sub(r'subsection{\g<1>}','section{First}')
   'subsection{First}'
   >>> p.sub(r'subsection{\g<name>}','section{First}')
   'subsection{First}'

..
  *replacement* can also be a function, which gives you even more control.  If
  *replacement* is a function, the function is called for every non-overlapping
  occurrence of *pattern*.  On each call, the function is  passed a
  :class:`MatchObject` argument for the match and can use this information to
  compute the desired replacement string and return it.

*replacement* は関数であっても構いません、関数を使うことでより一層の制御を行うことができます。
*replacement* が関数の場合、 *pattern* が重複せず現われる度、関数が呼び出されます。
呼び出す度に関数には :class:`MatchObject` 引数が渡されます、
この情報を使って望みの置換文字列を計算し返すことができます。

..
  In the following example, the replacement function translates  decimals into
  hexadecimal::

以下の例では、置換関数は10進数を16進数に変換します::

   >>> def hexrepl( match ):
   ...     "Return the hex string for a decimal number"
   ...     value = int( match.group() )
   ...     return hex(value)
   ...
   >>> p = re.compile(r'\d+')
   >>> p.sub(hexrepl, 'Call 65490 for printing, 49152 for user code.')
   'Call 0xffd2 for printing, 0xc000 for user code.'

..
  When using the module-level :func:`re.sub` function, the pattern is passed as
  the first argument.  The pattern may be provided as an object or as a string; if
  you need to specify regular expression flags, you must either use a
  pattern object as the first parameter, or use embedded modifiers in the
  pattern string, e.g. ``sub("(?i)b+", "x", "bbbb BBBB")`` returns ``'x x'``.

モジュールレベルの :func:`re.sub` 関数を使うときには、パターンが最初の引数として渡されます。
パターンはオブジェクトや文字列をとります; 正規表現フラグを指定する必要がある場合、
パターンオブジェクトを最初の引数として使うか、修飾子を埋め込んだパターン文字列を使うかしなければいけません、
例えば ``sub("(?i)b+", "x", "bbbb BBBB")`` は ``'x x'`` を返します。

..
  Common Problems
  ===============

よくある問題
============

..
  Regular expressions are a powerful tool for some applications, but in some ways
  their behaviour isn't intuitive and at times they don't behave the way you may
  expect them to.  This section will point out some of the most common pitfalls.

正規表現はいくつかの応用に対して強力なツールですが、いくつかの部分で
それらの振る舞いは直感的ではなく、期待通りに振る舞わないことがあります。
この節では最もよくある落とし穴を指摘します。

..
  Use String Methods
  ------------------

文字列メソッドを利用する
------------------------

..
  Sometimes using the :mod:`re` module is a mistake.  If you're matching a fixed
  string, or a single character class, and you're not using any :mod:`re` features
  such as the :const:`IGNORECASE` flag, then the full power of regular expressions
  may not be required. Strings have several methods for performing operations with
  fixed strings and they're usually much faster, because the implementation is a
  single small C loop that's been optimized for the purpose, instead of the large,
  more generalized regular expression engine.

いくつかの場合 :mod:`re` モジュールを利用することは間違いである場合があります。
固定文字列や単一の文字クラスにマッチさせる場合や、
:const:`IGNORECASE` フラグのような :mod:`re` の機能を利用しない場合、
正規表現の全ての能力は必要とされていなでしょう。
文字列は固定文字列に対する操作を実行するメソッドを持っていて、
大きな汎用化された正規表現エンジンではなく、
目的のために最適化された単一の小さな C loop で実装されているため、
大抵の場合高速です.

..
  One example might be replacing a single fixed string with another one; for
  example, you might replace ``word`` with ``deed``.  ``re.sub()`` seems like the
  function to use for this, but consider the :meth:`replace` method.  Note that
  :func:`replace` will also replace ``word`` inside words, turning ``swordfish``
  into ``sdeedfish``, but the  naive RE ``word`` would have done that, too.  (To
  avoid performing the substitution on parts of words, the pattern would have to
  be ``\bword\b``, in order to require that ``word`` have a word boundary on
  either side.  This takes the job beyond  :meth:`replace`'s abilities.)

一つの例としては、単一の固定文字列を別の固定文字列に置き換える作業がそうかもしれません;
例えば ``word`` を ``deed`` で置換したい場合です。
``re.sub()`` はこのために使うことができるように見えますが、
:meth:`replace` メソッドを利用することを考えた方がいいでしょう。
:func:`replace` は単語内の ``word`` も置換します、
``swordfish`` は ``sdeedfish`` に変わることに注意して下さい。
しかし、単純な正規表現 ``word`` も同様に動作します。
(単語の一部に対する置換の実行を避けるには、パターンを ``\bword\b`` として、
``word`` が両側に単語の境界を必要とするようにします。
これは :meth:`replace` の能力を越えた仕事です。)

..
  Another common task is deleting every occurrence of a single character from a
  string or replacing it with another single character.  You might do this with
  something like ``re.sub('\n', ' ', S)``, but :meth:`translate` is capable of
  doing both tasks and will be faster than any regular expression operation can
  be.

別のよくある作業は、文字列の中に出現する文字を全て削除することと、別の文字で置換することです。
この作業を ``re.sub('\n', ' ', S)`` のようにして行うかもしれませんが、
:meth:`translate` は削除と置換の両方の作業をこなし、正規表現操作よりも高速に行うことができます。

..
  In short, before turning to the :mod:`re` module, consider whether your problem
  can be solved with a faster and simpler string method.

要は、 :mod:`re` モジュールに向う前に問題が高速で単純な文字列メソッドで解決できるか考えましょうということです。

..
  match() versus search()
  -----------------------

match() 対 search()
-------------------

..
  The :func:`match` function only checks if the RE matches at the beginning of the
  string while :func:`search` will scan forward through the string for a match.
  It's important to keep this distinction in mind.  Remember,  :func:`match` will
  only report a successful match which will start at 0; if the match wouldn't
  start at zero,  :func:`match` will *not* report it. ::

:func:`match` 関数は文字列の先頭に正規表現がマッチするかどうか調べるだけで、
一方 :func:`search` はマッチするために文字列を進めて走査します。
この違いを認識しておくことは重要なことです。
:func:`match` は開始位置0でマッチしたときのみ報告します; もし開始位置0でマッチしなければ、
:func:`match` はそれを報告 *しません* 。::

   >>> print re.match('super', 'superstition').span()
   (0, 5)
   >>> print re.match('super', 'insuperable')
   None

..
  On the other hand, :func:`search` will scan forward through the string,
  reporting the first match it finds. ::

一方 :func:`search` は文字列を先に進めて走査文字列を進めて走査し、
最初にみつけたマッチを報告します。::

   >>> print re.search('super', 'superstition').span()
   (0, 5)
   >>> print re.search('super', 'insuperable').span()
   (2, 7)

..
  Sometimes you'll be tempted to keep using :func:`re.match`, and just add ``.*``
  to the front of your RE.  Resist this temptation and use :func:`re.search`
  instead.  The regular expression compiler does some analysis of REs in order to
  speed up the process of looking for a match.  One such analysis figures out what
  the first character of a match must be; for example, a pattern starting with
  ``Crow`` must match starting with a ``'C'``.  The analysis lets the engine
  quickly scan through the string looking for the starting character, only trying
  the full match if a ``'C'`` is found.

しばしば、 :func:`re.match` を使い、 ``.*`` を正規表現の最初に付け加える誘惑に
からされることがあるでしょう。
この誘惑に打ち克って、代わりに :func:`re.search` を利用すべきです。
正規表現コンパイラはマッチを探す処理の高速化のためにいくつかの解析を行います。
そのような解析のうちのひとつはマッチの最初の文字が何であるか評価することです;
例えば、 ``Crow`` で始まるパターンは ``C`` から始まらなければいけません。
解析によってエンジンは速やかに開始文字を探して走査します、 ``'C'`` が発見された場合に
はじめて完全なマッチを試みます。

..
  Adding ``.*`` defeats this optimization, requiring scanning to the end of the
  string and then backtracking to find a match for the rest of the RE.  Use
  :func:`re.search` instead.

``.*`` を追加することはこの最適化を無効にします、文字列の終端までの走査が必要となり、
走査後には残りの正規表現とのマッチ部分を見つけるために引き返すことになります。
代わりに :func:`re.search` を利用して下さい。

..
  Greedy versus Non-Greedy
  ------------------------

貪欲 (greedy) 対非貪欲 (non-greedy)
-----------------------------------

..
  When repeating a regular expression, as in ``a*``, the resulting action is to
  consume as much of the pattern as possible.  This fact often bites you when
  you're trying to match a pair of balanced delimiters, such as the angle brackets
  surrounding an HTML tag.  The naive pattern for matching a single HTML tag
  doesn't work because of the greedy nature of ``.*``. ::

正規表現を繰り返す場合、 たとえば ``a*`` のように、
できるだけパターンの多くにマッチするように動作することになります。
この動作は、例えば角括弧で囲まれた HTML タグのような
左右対称のデリミタの対にマッチしようという場合に問題となります。
単一の HTML タグにマッチする素朴な正規表現はうまく動作しません、
なぜならば ``.*`` は貪欲に動作するからです。::

   >>> s = '<html><head><title>Title</title>'
   >>> len(s)
   32
   >>> print re.match('<.*>', s).span()
   (0, 32)
   >>> print re.match('<.*>', s).group()
   <html><head><title>Title</title>

..
  The RE matches the ``'<'`` in ``<html>``, and the ``.*`` consumes the rest of
  the string.  There's still more left in the RE, though, and the ``>`` can't
  match at the end of the string, so the regular expression engine has to
  backtrack character by character until it finds a match for the ``>``.   The
  final match extends from the ``'<'`` in ``<html>`` to the ``'>'`` in
  ``</title>``, which isn't what you want.

正規表現は ``<html>`` 内の ``'<'`` にマッチし、
``.*`` は残りの文字列の全てにマッチします。
しかし、正規表現は以前残っています、 ``>`` は文字列の終端にマッチしないので、
正規表現は一文字ずつ ``>`` とマッチするまで引き返すことになります。
最終的にマッチする領域は ``<html>`` の ``'<'`` から ``</title>`` の ``'>'`` にまで
及ぶことになりますが、これは望んだ結果ではありません。

..
  In this case, the solution is to use the non-greedy qualifiers ``*?``, ``+?``,
  ``??``, or ``{m,n}?``, which match as *little* text as possible.  In the above
  example, the ``'>'`` is tried immediately after the first ``'<'`` matches, and
  when it fails, the engine advances a character at a time, retrying the ``'>'``
  at every step.  This produces just the right result::

この場合、解決法は非貪欲を示す修飾子 ``*?``, ``+?``, ``??`` または ``{m,n}?`` を
利用することです、これらはテキストに可能な限り *少なく* マッチします。
上の例では、 ``'>'`` は最初の ``'<'`` とのマッチ後すぐに ``'>'`` を試みま、
失敗した場合にはエンジンが文字を先に進め、 ``'>'`` が毎ステップ再試行されます。
この動作は正しい結果を生み出します::

   >>> print re.match('<.*?>', s).group()
   <html>

..
  (Note that parsing HTML or XML with regular expressions is painful.
  Quick-and-dirty patterns will handle common cases, but HTML and XML have special
  cases that will break the obvious regular expression; by the time you've written
  a regular expression that handles all of the possible cases, the patterns will
  be *very* complicated.  Use an HTML or XML parser module for such tasks.)

(HTML や XML を正規表現でパースすることは苦痛を伴うものであることは記憶に留めておいて下さい。
素早く、汚いパターンは大抵の場合うまく動作しますが、HTML と XML は 正規表現が破綻する特別な例です;
全ての可能な場合にうまく動作する正規表現を書き上げたときには、
パターンは *非常に* 複雑なものになります。
そのような作業をする場合には HTML や XML パーサを利用しましょう。)

..
  Using re.VERBOSE
  --------------------

re.VERBOSE の利用
---------------------------

..
  By now you've probably noticed that regular expressions are a very compact
  notation, but they're not terribly readable.  REs of moderate complexity can
  become lengthy collections of backslashes, parentheses, and metacharacters,
  making them difficult to read and understand.

ここまでで、正規表現がとても簡潔な表記であることに気づいたでしょう、
また、正規表現は読みやすいものでもないということにも気づいたことでしょう。
そこそこに入り組んだ正規表現ははバックスラッシュ、括弧、特殊文字が長く続いて、
読みにくく、理解しづらいものになります。

..
  For such REs, specifying the ``re.VERBOSE`` flag when compiling the regular
  expression can be helpful, because it allows you to format the regular
  expression more clearly.

そのような正規表現に対しては正規表現をコンパイルする時に
``re.VERBOSE`` フラグを指定することが助けになります、
なぜなら、そうすることによって正規表現を明確にフォーマットすることができるからです。

..
  The ``re.VERBOSE`` flag has several effects.  Whitespace in the regular
  expression that *isn't* inside a character class is ignored.  This means that an
  expression such as ``dog | cat`` is equivalent to the less readable ``dog|cat``,
  but ``[a b]`` will still match the characters ``'a'``, ``'b'``, or a space.  In
  addition, you can also put comments inside a RE; comments extend from a ``#``
  character to the next newline.  When used with triple-quoted strings, this
  enables REs to be formatted more neatly::


``re.VERBOSE`` の効果はいくつかあります。
正規表現内の文字クラス内に *無い* 空白は無視されます。
これは、 ``dog | cat`` のような表現が少々可読性の落ちる ``dog|cat`` と
等価となるということです、
しかし、 ``[a b]`` は依然として ``'a'``, ``'b'``, または空白にマッチします。
加えて、正規表現にコメントを入れることもできるようになります;
``#`` 文字から次の改行までがコメントの範囲です。
三重クォートを利用することで、正規表現をきちんとフォーマットすることができます::

   pat = re.compile(r"""
    \s*                 # Skip leading whitespace
    (?P<header>[^:]+)   # Header name
    \s* :               # Whitespace, and a colon
    (?P<value>.*?)      # The header's value -- *? used to
                        # lose the following trailing whitespace
    \s*$                # Trailing whitespace to end-of-line
   """, re.VERBOSE)

..
  This is far more readable than::

これは下よりはるかに読みやすいです::

   pat = re.compile(r"\s*(?P<header>[^:]+)\s*:(?P<value>.*?)\s*$")


..
  Feedback
  ========

フィードバック
==============

..
  Regular expressions are a complicated topic.  Did this document help you
  understand them?  Were there parts that were unclear, or Problems you
  encountered that weren't covered here?  If so, please send suggestions for
  improvements to the author.

正規表現は複雑な話題です。
このドキュメントは助けになったでしょうか？
わかりにくかったところや、あなたが遭遇した問題が
扱われていない等なかったでしょうか？
もしそんな問題があれば、著者に改善の提案を送って下さい。

..
  The most complete book on regular expressions is almost certainly Jeffrey
  Friedl's Mastering Regular Expressions, published by O'Reilly.  Unfortunately,
  it exclusively concentrates on Perl and Java's flavours of regular expressions,
  and doesn't contain any Python material at all, so it won't be useful as a
  reference for programming in Python.  (The first edition covered Python's
  now-removed :mod:`regex` module, which won't help you much.)  Consider checking
  it out from your library.

O'Reilly から出版されている Jeffrey Friedl の Mastering Regular Expressions は
正規表現に関するほぼ完璧な書籍です [#]_ 。
不幸なことに、この本は Perl と Java の正規表現を集中して扱っていて、
Python の正規表現については全く扱っていません、
そのため Python プログラミングのためのレファレンスとして使うことはできません。
(第一版はいまや削除された Python の :mod:`regex` モジュールについて
扱っていましたが、これはあまり役に立たないでしょう。)
図書館で調べるのを検討してみましょう。

.. rubric:: 注記

..
  .. [#] Introduced in Python 2.2.2.

.. [#] Python 2.2.2 で導入されました。
.. [#] 訳注 日本語訳「詳説 正規表現」が出版されています。
