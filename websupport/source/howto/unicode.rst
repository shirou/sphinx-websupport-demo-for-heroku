*****************
  Unicode HOWTO
*****************

:Release: 1.03

この HOWTO 文書は Python 2.x の Unicode サポートについて論じ、
さらに Unicode を使おうというときによくでくわす多くの問題について説明します。
(この HOWTO はまだ Python 3.x をカバーしていません)

..
  Introduction to Unicode
  =======================

Unicode 入門
============

..
  History of Character Codes
  --------------------------

文字コードの歴史
----------------

..
  In 1968, the American Standard Code for Information Interchange, better known by
  its acronym ASCII, was standardized.  ASCII defined numeric codes for various
  characters, with the numeric values running from 0 to
  127.  For example, the lowercase letter 'a' is assigned 97 as its code
  value.

1968年に American Standard Code for Information Interchange が標準化されました。
頭文字の ASCII でよく知られています。
ASCII は0から127までの、異なる文字の数値コードを定義していて、
例えば、小文字の 'a' にはコード値 97 が割り当てられています。

..
  ASCII was an American-developed standard, so it only defined unaccented
  characters.  There was an 'e', but no 'é' or 'Í'.  This meant that languages
  which required accented characters couldn't be faithfully represented in ASCII.
  (Actually the missing accents matter for English, too, which contains words such
  as 'naïve' and 'café', and some publications have house styles which require
  spellings such as 'coöperate'.)

ASCII はアメリカの開発標準だったのでアクセント無しの文字のみを定義していて、
'e' はありましたが、 'é' や 'Í' はありませんでした。
つまり、アクセント付きの文字を必要とする言語は ASCII できちんと表現するとができません。
(実際には英語でもアクセント無いために起きる問題がありました、
'naïve' や 'café' のようなアクセントを含む単語や、
いくつかの出版社は 'coöperate' のような独自のスタイルのつづりを必要とするなど)

..
  For a while people just wrote programs that didn't display accents.  I remember
  looking at Apple ][ BASIC programs, published in French-language publications in
  the mid-1980s, that had lines like these::

しばらくの間は単にアクセントが表示されないプログラムを書きました。
1980年半ばのフランス語で出版された Apple ][ の BASIC プログラムを見た記憶を辿ると、
そこにはこんな行が含まれていました::

	PRINT "FICHER EST COMPLETE."
	PRINT "CARACTERE NON ACCEPTE."

..
  Those messages should contain accents, and they just look wrong to someone who
  can read French.

これらのメッセージはアクセントを含むべきで、
フランス語を読める人から見ると単に間違いとみなされます。

..
  In the 1980s, almost all personal computers were 8-bit, meaning that bytes could
  hold values ranging from 0 to 255.  ASCII codes only went up to 127, so some
  machines assigned values between 128 and 255 to accented characters.  Different
  machines had different codes, however, which led to problems exchanging files.
  Eventually various commonly used sets of values for the 128-255 range emerged.
  Some were true standards, defined by the International Standards Organization,
  and some were **de facto** conventions that were invented by one company or
  another and managed to catch on.

1980年代には、多くのパーソナルコンピューターは 8-bit で、
つまり 8-bit で 0-255 までの値を確保することができました。
ASCII コードは 127 までだったので、いくつかのマシンは 128 から 255 の値を
アクセント付きの文字に割り当てました。
マシン毎に異なる文字コードがあり、そのためにファイル交換の問題が起きることとなりました。
結局、128-255 の間の値は多くのよく使われる集合が現われることになりました。
そのうちいくつかは International Standards Organzation の定める本当の標準になり、
またいくつかは一社で開発され、別の会社へと流行することで **事実上の** 慣習となりました。

..
  255 characters aren't very many.  For example, you can't fit both the accented
  characters used in Western Europe and the Cyrillic alphabet used for Russian
  into the 128-255 range because there are more than 127 such characters.

255文字というのは十分多い数ではありません。
例えば、西ヨーロッパで使われるアクセント付き文字とロシアで使われるキリルアルファベットの両方は
127文字以上あるので、128-255の間におさめることはできません。

..
  You could write files using different codes (all your Russian files in a coding
  system called KOI8, all your French files in a different coding system called
  Latin1), but what if you wanted to write a French document that quotes some
  Russian text?  In the 1980s people began to want to solve this problem, and the
  Unicode standardization effort began.

異なる文字コードを使ってファイルを作成することは可能です
(持っているロシア語のファイル全てを KOI8 と呼ばれるコーディングシステムで、
持っているフランス語のファイル全てを別の Latin1 と呼ばれるコーディングシステムにすることで)、
しかし、ロシア語の文章を引用するフランス語の文章を書きたい場合にはどうでしょう?
1989年代にこの問題を解決したいという要望が上って、Unicode 標準化の努力が始まりました。

..
  Unicode started out using 16-bit characters instead of 8-bit characters.  16
  bits means you have 2^16 = 65,536 distinct values available, making it possible
  to represent many different characters from many different alphabets; an initial
  goal was to have Unicode contain the alphabets for every single human language.
  It turns out that even 16 bits isn't enough to meet that goal, and the modern
  Unicode specification uses a wider range of codes, 0-1,114,111 (0x10ffff in
  base-16).

Unicode は 8-bit の文字の代わりに 16-bit の文字を使うことにとりかかりました。
16bit 使うということは 2^16 = 65,536 の異なる値が利用可能だということを意味します、
これによって多くの異なるアルファベット上の多くの異なる文字を表現することができます;
最初の目標は Unicode が人間が使う個々の言語のアルファベットを含むことでした。
あとになってこの目標を達成するには 16bit でさえも不十分であることがわかりました、
そして最新の Unicode 規格は 0-1,114,111 (16進表記で 0x10ffff) までの
より広い文字コードの幅を使っています。

..
  There's a related ISO standard, ISO 10646.  Unicode and ISO 10646 were
  originally separate efforts, but the specifications were merged with the 1.1
  revision of Unicode.

関連する ISO 標準も ISO 10646 があります。Unicode と ISO 10646 は元々独立した成果でしたが、
Unicode の 1.1 リビジョンで仕様を併合しました。

..
  (This discussion of Unicode's history is highly simplified.  I don't think the
  average Python programmer needs to worry about the historical details; consult
  the Unicode consortium site listed in the References for more information.)

(この Unicode の歴史についての解説は非常に単純化しています。
平均的な Python プログラマは歴史的な詳細を気にする必要は無いと考えています;
より詳しい情報は参考文献に載せた Unicode コンソーシアムのサイトを参考にして下さい。)

..
  Definitions
  -----------

定義
----

..
  A **character** is the smallest possible component of a text.  'A', 'B', 'C',
  etc., are all different characters.  So are 'È' and 'Í'.  Characters are
  abstractions, and vary depending on the language or context you're talking
  about.  For example, the symbol for ohms (Ω) is usually drawn much like the
  capital letter omega (Ω) in the Greek alphabet (they may even be the same in
  some fonts), but these are two different characters that have different
  meanings.

**文字** は文章の構成要素の中の最小のものです。'A', 'B', 'C' などは全て異なる文字です。
'È' や 'Í' も同様に異なる文字です。
文字は抽象的な概念で、言語や文脈に依存してさまざまに変化します。
例えば、オーム(Ω) はふつう大文字ギリシャ文字のオメガ (Ω) で書かれますが
(これらはいくつかのフォントで全く同じ書体かもしれません)
しかし、これらは異なる意味を持つ異なる文字とみなされます。

..
  The Unicode standard describes how characters are represented by **code
  points**.  A code point is an integer value, usually denoted in base 16.  In the
  standard, a code point is written using the notation U+12ca to mean the
  character with value 0x12ca (4810 decimal).  The Unicode standard contains a lot
  of tables listing characters and their corresponding code points::

Unicode 標準は文字が **コードポイント (code points)** でどう表現するかを記述しています。
コードポイントは整数値で、ふつう16進表記で書かれます。
標準的にはコードポイントは U+12ca のような表記を使って書かれます、
U+12ca は 0x12ca (10進表記で 4810) を意味しています。
Unicode 標準は文字とコードポイントを対応させる多くのテーブルを含んでいます::

	0061    'a'; LATIN SMALL LETTER A
	0062    'b'; LATIN SMALL LETTER B
	0063    'c'; LATIN SMALL LETTER C
        ...
	007B	'{'; LEFT CURLY BRACKET

..
  Strictly, these definitions imply that it's meaningless to say 'this is
  character U+12ca'.  U+12ca is a code point, which represents some particular
  character; in this case, it represents the character 'ETHIOPIC SYLLABLE WI'.  In
  informal contexts, this distinction between code points and characters will
  sometimes be forgotten.

厳密にいうとこれらの定義は「この文字は U+12ca です」ということを意味していません。
U+12ca はコードポイントで、特定の文字を示しています; この場合では、'ETHIOPIC SYLLABLE WI' を示しています。
細かく気にしない文脈の中ではコードポイントと文字の区別は忘れられることがよくあります。

..
  A character is represented on a screen or on paper by a set of graphical
  elements that's called a **glyph**.  The glyph for an uppercase A, for example,
  is two diagonal strokes and a horizontal stroke, though the exact details will
  depend on the font being used.  Most Python code doesn't need to worry about
  glyphs; figuring out the correct glyph to display is generally the job of a GUI
  toolkit or a terminal's font renderer.

文字は画面や紙面上では **グリフ (glyph)** と呼ばれるグラフィック要素の組で表示されます。
大文字の A のグリフは例えば、厳密な形は使っているフォントによって異なりますが、斜めの線と水平の線です。
たいていの Python コードではグリフの心配をする必要はありません; 
一般的には表示する正しいグリフを見付けることは GUI toolkit や端末のフォントレンダラーの仕事です。

..
  Encodings
  ---------

エンコーディング
----------------

..
  To summarize the previous section: a Unicode string is a sequence of code
  points, which are numbers from 0 to 0x10ffff.  This sequence needs to be
  represented as a set of bytes (meaning, values from 0-255) in memory.  The rules
  for translating a Unicode string into a sequence of bytes are called an
  **encoding**.

前の節をまとめると: Unicode 文字列は 0 から 0x10ffff までの数値であるコードポイントのシーケンスで、
シーケンスはメモリ上でバイト (0 から 255 までの値) の組として表現される必要があります。
バイト列を Unicode 文字列に変換する規則を **エンコーディング (encoding)** と呼びます。

..
  The first encoding you might think of is an array of 32-bit integers.  In this
  representation, the string "Python" would look like this::

最初に考えるであろうエンコーディングは 32-bit 整数の配列でしょう。
この表示では、"Python" という文字列はこうみえます::

       P           y           t           h           o           n
    0x50 00 00 00 79 00 00 00 74 00 00 00 68 00 00 00 6f 00 00 00 6e 00 00 00
       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23

..
  This representation is straightforward but using it presents a number of
  problems.

この表示は直接的でわかりやすい方法ですが、この表示を使うにはいくつかの問題があります。

..
  1. It's not portable; different processors order the bytes differently.

  2. It's very wasteful of space.  In most texts, the majority of the code points
     are less than 127, or less than 255, so a lot of space is occupied by zero
     bytes.  The above string takes 24 bytes compared to the 6 bytes needed for an
     ASCII representation.  Increased RAM usage doesn't matter too much (desktop
     computers have megabytes of RAM, and strings aren't usually that large), but
     expanding our usage of disk and network bandwidth by a factor of 4 is
     intolerable.

  3. It's not compatible with existing C functions such as ``strlen()``, so a new
     family of wide string functions would need to be used.

  4. Many Internet standards are defined in terms of textual data, and can't
     handle content with embedded zero bytes.

1. 可搬性がない; プロセッサが異なるとバイトの順序づけも変わってしまいます。

2. 空間を無駄に使ってしまいます。
   多くの文書では、コードポイントの多くは 127 か 255 より小さいため多くの空間が
   ゼロバイトに占有されます。
   上の文字列はASCII表示では6バイトを必要だったのに対して24バイトを必要としています。
   RAM の使用料の増加はたいした問題ではありませんが
   (デスクトップコンピュータは RAM をメガバイト単位で持っていますし、
   文字列はそこまで大きい容量にはなりません)、
   しかし、ディスクとネットワークの帯域が4倍増えることはとても我慢できるものではありません。

3. ``strlen()`` のような現存する C 関数と互換性がありません、
   そのためワイド文字列関数一式が新たに必要となります。

4. 多くのインターネット標準がテキストデータとして定義されていて、
   それらはゼロバイトの埋め込まれた内容を扱うことができません。

一般的にこのエンコーディングは使わず、変わりにより効率的で便利な他のエンコーディングが選ばれています。
UTF-8 はたぶん最も一般的にサポートされているエンコーディングです。
このエンコーディングについては後で説明します。

..
  Encodings don't have to handle every possible Unicode character, and most
  encodings don't.  For example, Python's default encoding is the 'ascii'
  encoding.  The rules for converting a Unicode string into the ASCII encoding are
  simple; for each code point:

エンコーディングは全ての Unicode 文字を扱う必要はありませんし、多くのエンコーディングはそれをしません。
例えば Python のデフォルトエンコーディングの 'ascii' エンコーディング。
Unicode 文字列を ASCII エンコーディングに変換する規則は単純です; それぞれのコードポイントに対して:

..
  1. If the code point is < 128, each byte is the same as the value of the code
     point.

  2. If the code point is 128 or greater, the Unicode string can't be represented
     in this encoding.  (Python raises a :exc:`UnicodeEncodeError` exception in this
     case.)

1. コードポイントは128より小さい場合、コードポイントと同じ値

2. コードポイントが128以上の場合、Unicode 文字列はエンコーディングで表示することができません。
   (この場合 Python は :exc:`UnicodeEncodeError` 例外を送出します。)

..
  Latin-1, also known as ISO-8859-1, is a similar encoding.  Unicode code points
  0-255 are identical to the Latin-1 values, so converting to this encoding simply
  requires converting code points to byte values; if a code point larger than 255
  is encountered, the string can't be encoded into Latin-1.

Latin-1, ISO-8859-1 として知られるエンコーディングも同様のエンコーディングです。
Unicode コードポイントの 0-255 は Latin-1 の値と等価なので、このエンコーディングの変換するには、
単純にコードポイントをバイト値に変換する必要があります;
もしコードポイントが255より大きい場合に遭遇した場合、文字列は Latin-1 にエンコードできません。

..
  Encodings don't have to be simple one-to-one mappings like Latin-1.  Consider
  IBM's EBCDIC, which was used on IBM mainframes.  Letter values weren't in one
  block: 'a' through 'i' had values from 129 to 137, but 'j' through 'r' were 145
  through 153.  If you wanted to use EBCDIC as an encoding, you'd probably use
  some sort of lookup table to perform the conversion, but this is largely an
  internal detail.

エンコーディングは Latin-1 のように単純な一対一対応を持っていません。
IBM メインフレームで使われていた IBM の EBCDIC で考えてみます。
文字は一つのブロックに収められていませんでした: 'a' から 'i' は 129 から 137 まででしたが、
'j' から 'r' までは 145 から 153 までした。
EBICIC を使いたいと思ったら、おそらく変換を実行するルックアップテーブルの類を使う必要があるでしょう、
これは内部の詳細のことになりますが。

..
  UTF-8 is one of the most commonly used encodings.  UTF stands for "Unicode
  Transformation Format", and the '8' means that 8-bit numbers are used in the
  encoding.  (There's also a UTF-16 encoding, but it's less frequently used than
  UTF-8.)  UTF-8 uses the following rules:

UTF-8 は最もよく使われるエンコーディングの一つです.
UTF は "Unicode Transformation Format" からとられていて、
8 はエンコーディングに 8-bit の数字を使うことを意味しています。
(同じく UTF-16 エンコーディングもあります、しかしこちらは UTF-8 ほど頻繁に使われていません。)
UTF-8 は以下の規則を利用します:

..
  1. If the code point is <128, it's represented by the corresponding byte value.
  2. If the code point is between 128 and 0x7ff, it's turned into two byte values
     between 128 and 255.
  3. Code points >0x7ff are turned into three- or four-byte sequences, where each
     byte of the sequence is between 128 and 255.

1. コードポイントが128より小さい場合、対応するバイト値で表現。
2. コードポイントは128から0x7ff の間の場合、128から255までの2バイト値に変換。
3. 0x7ff より大きいコードポイントは3か4バイト列に変換し、バイト列のそれぞれのバイトは128から255の間をとる。

..
  UTF-8 has several convenient properties:

UTF-8 はいくつかの便利な性質を持っています。

..
  1. It can handle any Unicode code point.
  2. A Unicode string is turned into a string of bytes containing no embedded zero
     bytes.  This avoids byte-ordering issues, and means UTF-8 strings can be
     processed by C functions such as ``strcpy()`` and sent through protocols that
     can't handle zero bytes.
  3. A string of ASCII text is also valid UTF-8 text.
  4. UTF-8 is fairly compact; the majority of code points are turned into two
     bytes, and values less than 128 occupy only a single byte.
  5. If bytes are corrupted or lost, it's possible to determine the start of the
     next UTF-8-encoded code point and resynchronize.  It's also unlikely that
     random 8-bit data will look like valid UTF-8.

1. 任意の Unicode コードポイントを扱うことができる。
2. Unicode 文字列をゼロバイトで埋めないバイト文字列に変換する。
   これによってバイト順の問題を解決し、UTF-8 文字列を ``strcpy()`` のような C 関数で処理することができ、
   そしてゼロバイトを扱うことができないプロトコル経由で送信することができます。
3. ASCII テキストの文字列は UTF-8 テキストとしても有効です。
4. UTF-8 はかなりコンパクトです; コードポイントの多くは2バイトに変換され、
   値が128より小さければ、1バイトしか占有しません。
5. バイトが欠落したり、失われた場合、次の UTF-8 でエンコードされたコードポイントの開始を決定し、
   再同期することができる可能性があります。
   同様の理由でランダムな 8-bit データは正当な UTF-8 とみなされにくくなっています。

..
  References
  ----------

参考文献
--------

..
  The Unicode Consortium site at <http://www.unicode.org> has character charts, a
  glossary, and PDF versions of the Unicode specification.  Be prepared for some
  difficult reading.  <http://www.unicode.org/history/> is a chronology of the
  origin and development of Unicode.

Unicode コンソーシアムのサイト <http://www.unicode.org> には文字の図表や用語辞典、そして Unicode 仕様の PDF があります。
読むのは簡単ではないので覚悟して下さい。

<http://www.unicode.org/history/> は Unicode の起源と発展の年表です。

..
  To help understand the standard, Jukka Korpela has written an introductory guide
  to reading the Unicode character tables, available at
  <http://www.cs.tut.fi/~jkorpela/unicode/guide.html>.

標準についての理解を助けるために Jukka Korpela が Unicode の文字表を読むための導入ガイドを書いています、
<http://www.cs.tut.fi/~jkorpela/unicode/guide.html> から入手可能です。

..
  Another good introductory article was written by Joel Spolsky
  <http://www.joelonsoftware.com/articles/Unicode.html>.
  If this introduction didn't make things clear to you, you should try reading this
  alternate article before continuing.

もう一つのよい入門記事 <http://www.joelonsoftware.com/articles/Unicode.html> を
Joel Spolsky が書いています。
もしこの HOWTO の入門が明解に感じなかった場合には、続きを読む前にこの記事を読んでみるべきです。

.. Jason Orendorff XXX http://www.jorendorff.com/articles/unicode/ is broken

..
  Wikipedia entries are often helpful; see the entries for "character encoding"
  <http://en.wikipedia.org/wiki/Character_encoding> and UTF-8
  <http://en.wikipedia.org/wiki/UTF-8>, for example.

Wikipedia の記事はしばしば役に立ちます; 試しに "character encoding"
<http://en.wikipedia.org/wiki/Character_encoding> の記事と
UTF-8 <http://en.wikipedia.org/wiki/UTF-8> の記事を読んでみて下さい。


Python 2.x の Unicode サポート
===============================

..
  Now that you've learned the rudiments of Unicode, we can look at Python's
  Unicode features.

ここまでで Unicode の基礎を学びました、ここから Python の Unicode 機能に触れます。

..
  The Unicode Type
  ----------------

Unicode 型
----------

..
  Unicode strings are expressed as instances of the :class:`unicode` type, one of
  Python's repertoire of built-in types.  It derives from an abstract type called
  :class:`basestring`, which is also an ancestor of the :class:`str` type; you can
  therefore check if a value is a string type with ``isinstance(value,
  basestring)``.  Under the hood, Python represents Unicode strings as either 16-
  or 32-bit integers, depending on how the Python interpreter was compiled.

Unicode 文字列は Python の組み込み型の一つ :class:`unicode` 型のインスタンスとして表現されます。
:class:`basestring` と呼ばれる抽象クラスから派生しています、 :class:`str` 型の親戚でもあります;
そのため ``isinstance(value, basestring)`` で文字列型かどうか調べることができます。
Python 内部では Unicode 文字列は16-bit, 32-bit 整数のどちらかで表現され、
どちらが使われるかは Python インタプリタがどうコンパイルされたかに依存します。

..
  The :func:`unicode` constructor has the signature ``unicode(string[, encoding,
  errors])``.  All of its arguments should be 8-bit strings.  The first argument
  is converted to Unicode using the specified encoding; if you leave off the
  ``encoding`` argument, the ASCII encoding is used for the conversion, so
  characters greater than 127 will be treated as errors::

:func:`unicode` コンストラクタは ``unicode(string[, encoding, errors])`` という用法を持っています。
この引数は全て 8-bit 文字列でなければいけません。
最初の引数は指定したエンコーディングを使って Unicode に変換されます;
``encoding`` 引数を渡さない場合、変換には ASCII エンコーディングが使われます、
そのため 127 より大きい文字はエラーとして扱われます::

    >>> unicode('abcdef')
    u'abcdef'
    >>> s = unicode('abcdef')
    >>> type(s)
    <type 'unicode'>
    >>> unicode('abcdef' + chr(255))
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xff in position 6:
                        ordinal not in range(128)

..
  The ``errors`` argument specifies the response when the input string can't be
  converted according to the encoding's rules.  Legal values for this argument are
  'strict' (raise a ``UnicodeDecodeError`` exception), 'replace' (add U+FFFD,
  'REPLACEMENT CHARACTER'), or 'ignore' (just leave the character out of the
  Unicode result).  The following examples show the differences::

``errors`` 引数は入力文字列がエンコーディング規則に従って変換できないときの対応を指定します。
この引数に有効な値は 'strict' (``UnicodeDecodeError`` を送出する)、
'replace' (U+FFFD, 'REPLACEMENT CHARACTER' を追加する)、
または 'ignore' (結果の Unicode 文字列から文字を除くだけ) です。
以下の例で違いを示します::

    >>> unicode('\x80abc', errors='strict')
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    UnicodeDecodeError: 'ascii' codec can't decode byte 0x80 in position 0:
                        ordinal not in range(128)
    >>> unicode('\x80abc', errors='replace')
    u'\ufffdabc'
    >>> unicode('\x80abc', errors='ignore')
    u'abc'

..
  Encodings are specified as strings containing the encoding's name.  Python 2.4
  comes with roughly 100 different encodings; see the Python Library Reference at
  :ref:`standard-encodings` for a list.  Some encodings
  have multiple names; for example, 'latin-1', 'iso_8859_1' and '8859' are all
  synonyms for the same encoding.

エンコーディングはエンコーディング名を含む文字列によって指定されます。
Python 2.7 ではエンコーディングはおよそ100に及びます; 
一覧は Python ライブラリレファレンスの :ref:`standard-encodings` を参照して下さい。
いくつかのエンコーディングは複数の名前を持っています; 例えば 'latin-1', 'iso_8859_1',
そして '8859' これらは全て同じエンコーディングの別称です。

..
  One-character Unicode strings can also be created with the :func:`unichr`
  built-in function, which takes integers and returns a Unicode string of length 1
  that contains the corresponding code point.  The reverse operation is the
  built-in :func:`ord` function that takes a one-character Unicode string and
  returns the code point value::

Unicode 文字列の一つの文字は :func:`unichr` 組み込み関数で作成することができます、
この関数は整数を引数にとり、対応するコードポイントを含む長さ1の Unicode 文字列を返します。
逆の操作は :func:`ord` 組み込み関数です、この関数は一文字の Unicode 文字列を引数にとり、
コードポイント値を返します::

    >>> unichr(40960)
    u'\ua000'
    >>> ord(u'\ua000')
    40960

..
  Instances of the :class:`unicode` type have many of the same methods as the
  8-bit string type for operations such as searching and formatting::

:class:`unicode` 型のインスタンスは多くの 8-bit 文字列型と同じ検索や書式指定のためのメソッドを持っています::

    >>> s = u'Was ever feather so lightly blown to and fro as this multitude?'
    >>> s.count('e')
    5
    >>> s.find('feather')
    9
    >>> s.find('bird')
    -1
    >>> s.replace('feather', 'sand')
    u'Was ever sand so lightly blown to and fro as this multitude?'
    >>> s.upper()
    u'WAS EVER FEATHER SO LIGHTLY BLOWN TO AND FRO AS THIS MULTITUDE?'

..
  Note that the arguments to these methods can be Unicode strings or 8-bit
  strings.  8-bit strings will be converted to Unicode before carrying out the
  operation; Python's default ASCII encoding will be used, so characters greater
  than 127 will cause an exception::

これらのメソッドの引数は Unicode 文字列または 8-bit 文字列が使えることに注意して下さい。
8-bit 文字列は操作に使われる前に Unicode に変換されます;
Python デフォルトの ASCII エンコーディングが利用されるため、127より大きい文字列は例外を引き起します::

    >>> s.find('Was\x9f')
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    UnicodeDecodeError: 'ascii' codec can't decode byte 0x9f in position 3: ordinal not in range(128)
    >>> s.find(u'Was\x9f')
    -1

..
  Much Python code that operates on strings will therefore work with Unicode
  strings without requiring any changes to the code.  (Input and output code needs
  more updating for Unicode; more on this later.)

文字列操作を行なう多くの Python コードはコードの変更無しに Unicode 文字列を扱うことができるでしょう。
(入出力に関しては Unicode のための更新が必要になります; 詳しくは後で述べます。)

..
  Another important method is ``.encode([encoding], [errors='strict'])``, which
  returns an 8-bit string version of the Unicode string, encoded in the requested
  encoding.  The ``errors`` parameter is the same as the parameter of the
  ``unicode()`` constructor, with one additional possibility; as well as 'strict',
  'ignore', and 'replace', you can also pass 'xmlcharrefreplace' which uses XML's
  character references.  The following example shows the different results::

別の重要なメソッドは ``.encode([encoding], [errors='strict'])`` があります、
このメソッドは Unicode 文字列を要求したエンコーディングでエンコードされた 8-bit 文字列を返します。
``errors`` パラメータは ``unicode()`` コンストラクタのパラメータと同様ですが、
もう一つ可能性が追加されています; 同様のものとして 'strict', 'ignore', そして 'replace' があり、
さらに XML 文字参照を使う 'xmlcharrefreplace' を渡すことができます::

    >>> u = unichr(40960) + u'abcd' + unichr(1972)
    >>> u.encode('utf-8')
    '\xea\x80\x80abcd\xde\xb4'
    >>> u.encode('ascii')
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    UnicodeEncodeError: 'ascii' codec can't encode character '\ua000' in position 0: ordinal not in range(128)
    >>> u.encode('ascii', 'ignore')
    'abcd'
    >>> u.encode('ascii', 'replace')
    '?abcd?'
    >>> u.encode('ascii', 'xmlcharrefreplace')
    '&#40960;abcd&#1972;'

..
  Python's 8-bit strings have a ``.decode([encoding], [errors])`` method that
  interprets the string using the given encoding::

Python の 8-bit 文字列は ``.decode([encoding], [errors])`` メソッドを持っています、
これは与えたエンコーディングを使って文字列を解釈します::

    >>> u = unichr(40960) + u'abcd' + unichr(1972)   # Assemble a string
    >>> utf8_version = u.encode('utf-8')             # Encode as UTF-8
    >>> type(utf8_version), utf8_version
    (<type 'str'>, '\xea\x80\x80abcd\xde\xb4')
    >>> u2 = utf8_version.decode('utf-8')            # Decode using UTF-8
    >>> u == u2                                      # The two strings match
    True

..
  The low-level routines for registering and accessing the available encodings are
  found in the :mod:`codecs` module.  However, the encoding and decoding functions
  returned by this module are usually more low-level than is comfortable, so I'm
  not going to describe the :mod:`codecs` module here.  If you need to implement a
  completely new encoding, you'll need to learn about the :mod:`codecs` module
  interfaces, but implementing encodings is a specialized task that also won't be
  covered here.  Consult the Python documentation to learn more about this module.

:mod:`codecs` モジュールに利用可能なエンコーディングを登録したり、アクセスする低レベルルーチンがあります。
しかし、このモジュールが返すエンコーディングとデコーディング関数はふつう低レベルすぎて快適とはいえません、
そのためここで :mod:`codecs` モジュールについて述べないことにします。
もし、全く新しいエンコーディングを実装する必要があれば、
:mod:`codecs` モジュールのインターフェースについて学ぶ必要があります、
しかし、エンコーディングの実装は特殊な作業なので、ここでは扱いません。
このモジュールについて学ぶには Python ドキュメントを参照して下さい。

..
  The most commonly used part of the :mod:`codecs` module is the
  :func:`codecs.open` function which will be discussed in the section on input and
  output.


:mod:`codecs` モジュールの中で最も使われるのは :func:`codecs.open` 関数です、
この関数は入出力の節で議題に挙げます。

..
  Unicode Literals in Python Source Code
  --------------------------------------

Python ソースコード内の Unicode リテラル
----------------------------------------

..
  In Python source code, Unicode literals are written as strings prefixed with the
  'u' or 'U' character: ``u'abcdefghijk'``.  Specific code points can be written
  using the ``\u`` escape sequence, which is followed by four hex digits giving
  the code point.  The ``\U`` escape sequence is similar, but expects 8 hex
  digits, not 4.

Python のソースコード内では Unicode リテラルは 'u' または 'U' の文字を最初に付けた文字列として書かれます:
``u'abcdefghijk'`` 。
特定のコードポイントはエスケープシーケンス ``\u`` を使い、続けてコードポイントを4桁の16進数を書きます。
エスケープシーケンス ``\U`` も同様です、ただし4桁ではなく8桁の16進数を使います。

..
  Unicode literals can also use the same escape sequences as 8-bit strings,
  including ``\x``, but ``\x`` only takes two hex digits so it can't express an
  arbitrary code point.  Octal escapes can go up to U+01ff, which is octal 777.

Unicode リテラルは 8-bit 文字列と同じエスケープシーケンスを使うことができます、
使えるエスケープシーケンスには ``\x`` も含みます、ただし ``\x`` は2桁の16進数しかとることができないので
任意のコードポイントを表現することはできません。
8進エスケープは8進数の777を示す U+01ff まで使うことができます。

::

    >>> s = u"a\xac\u1234\u20ac\U00008000"
               ^^^^ two-digit hex escape
                   ^^^^^^ four-digit Unicode escape
                               ^^^^^^^^^^ eight-digit Unicode escape
    >>> for c in s:  print ord(c),
    ...
    97 172 4660 8364 32768

..
  Using escape sequences for code points greater than 127 is fine in small doses,
  but becomes an annoyance if you're using many accented characters, as you would
  in a program with messages in French or some other accent-using language.  You
  can also assemble strings using the :func:`unichr` built-in function, but this is
  even more tedious.

127 より大きいコードポイントに対してエスケープシーケンスを使うのは、
エスケープシーケンスがあまり多くないうちは有効ですが、
フランス語等のアクセントを使う言語でメッセージのような多くのアクセント文字を使う場合には邪魔になります。
文字を :func:`unichr` 組み込み関数を使って組み上げることもできますが、それはさらに長くなってしまうでしょう。

..
  Ideally, you'd want to be able to write literals in your language's natural
  encoding.  You could then edit Python source code with your favorite editor
  which would display the accented characters naturally, and have the right
  characters used at runtime.

理想的にはあなたの言語の自然なエンコーディングでリテラルを書くことでしょう。
そうなれば、Python のソースコードをアクセント付きの文字を自然に表示するお気に入りのエディタで編集し、
実行時に正しい文字が得られます。

..
  Python supports writing Unicode literals in any encoding, but you have to
  declare the encoding being used.  This is done by including a special comment as
  either the first or second line of the source file::

Python は Unicode 文字列を任意のエンコーディングで書くことができます、
ただしどのエンコーディングを使うかを宣言しなければいけません。
それはソースファイルの一行目や二行目に特別なコメントを含めることによってできます::

    #!/usr/bin/env python
    # -*- coding: latin-1 -*-

    u = u'abcdé'
    print ord(u[-1])

..
  The syntax is inspired by Emacs's notation for specifying variables local to a
  file.  Emacs supports many different variables, but Python only supports
  'coding'.  The ``-*-`` symbols indicate that the comment is special; within
  them, you must supply the name ``coding`` and the name of your chosen encoding,
  separated by ``':'``.

この構文は Emacs のファイル固有の変数を指定する表記から影響を受けています。
Emacs は様々な変数をサポートしていますが、Python がサポートしているのは 'coding' のみです。
``-*-`` の記法はコメントが特別であることを示します;
この記号に前後はさまれたところに ``coding`` と選択したコーディングを ``':'`` でつないで書く必要があります。

..
  If you don't include such a comment, the default encoding used will be ASCII.
  Versions of Python before 2.4 were Euro-centric and assumed Latin-1 as a default
  encoding for string literals; in Python 2.4, characters greater than 127 still
  work but result in a warning.  For example, the following program has no
  encoding declaration::

このコメントを含まない場合には、デフォルトエンコーディングとして ASCII が利用されます。
Python のバージョンが 2.4 より前の場合には Euro-centric と Latin-1 が文字列リテラルの
デフォルトエンコーディングであると仮定されていました;
Python 2.4 では 127 より大きい文字でも動作しますが、警告を発することになります。
例えば、以下のエンコーディング宣言のないプログラムは::

    #!/usr/bin/env python
    u = u'abcdé'
    print ord(u[-1])

..
  When you run it with Python 2.4, it will output the following warning::

これを Python 2.4 で動作させたときには、以下の警告が出力されます::

    amk:~$ python2.4 p263.py
    sys:1: DeprecationWarning: Non-ASCII character '\xe9'
         in file p263.py on line 2, but no encoding declared;
         see http://www.python.org/peps/pep-0263.html for details

Python 2.5 以降ではより厳格になり、文法エラーになります::

    amk:~$ python2.5 p263.py
    File "/tmp/p263.py", line 2
    SyntaxError: Non-ASCII character '\xc3' in file /tmp/p263.py
      on line 2, but no encoding declared; see
      http://www.python.org/peps/pep-0263.html for details


..
  Unicode Properties
  ------------------

Unicode プロパティ
------------------

..
  The Unicode specification includes a database of information about code points.
  For each code point that's defined, the information includes the character's
  name, its category, the numeric value if applicable (Unicode has characters
  representing the Roman numerals and fractions such as one-third and
  four-fifths).  There are also properties related to the code point's use in
  bidirectional text and other display-related properties.

Unicode 仕様はコードポイントについての情報データベースを含んでいます。
定義された各コードポイントに対して、情報は文字の名前、カテゴリ、適用可能ならば数値
(Unicode にはローマ数字や 1/3 や 4/5 のような分数などの文字があります)を含んでいます。
コードポイントを左右どちらから読むのか等表示に関連したプロパティもあります。

..
  The following program displays some information about several characters, and
  prints the numeric value of one particular character::

以下のプログラムはいくつかの文字に対する情報を表示し、特定の文字の数値を印字します::

    import unicodedata

    u = unichr(233) + unichr(0x0bf2) + unichr(3972) + unichr(6000) + unichr(13231)

    for i, c in enumerate(u):
        print i, '%04x' % ord(c), unicodedata.category(c),
        print unicodedata.name(c)

    # Get numeric value of second character
    print unicodedata.numeric(u[1])

..
  When run, this prints::

実行時には、このように印字されます::

    0 00e9 Ll LATIN SMALL LETTER E WITH ACUTE
    1 0bf2 No TAMIL NUMBER ONE THOUSAND
    2 0f84 Mn TIBETAN MARK HALANTA
    3 1770 Lo TAGBANWA LETTER SA
    4 33af So SQUARE RAD OVER S SQUARED
    1000.0


カテゴリコードは文字の性質を簡単に説明するものです。
カテゴリの分類は "Letter", "Number", "Punctuation" または "Symbol" で、
さらにサブカテゴリに分かれます。
上に出ている出力結果を例にとると ``'Ll'`` は 'Letter, lowercase' を意味していて、
``'No'`` は "Number, other" を意味しています、 ``'Mn'`` は "Mark, nonspacing" で
``'So'`` は "Symbol, other" です。
カテゴリコードの一覧は
<http://www.unicode.org/reports/tr44/#General_Category_Values>
を参照して下さい。

..
  References
  ----------

参考文献
--------

..
  The Unicode and 8-bit string types are described in the Python library reference
  at :ref:`typesseq`.

Unicode と 8-bit 文字型については Python ライブラリレファレンスの :ref:`typesseq` に記述があります。

..
  The documentation for the :mod:`unicodedata` module.

:mod:`unicodedata` モジュールについてのドキュメント。

..
  The documentation for the :mod:`codecs` module.

:mod:`codecs` モジュールについてのドキュメント。

..
  Marc-André Lemburg gave a presentation at EuroPython 2002 titled "Python and
  Unicode".  A PDF version of his slides is available at
  <http://downloads.egenix.com/python/Unicode-EPC2002-Talk.pdf>, and is an
  excellent overview of the design of Python's Unicode features.

Marc-André Lemburg は EuroPython 2002 で "Python and Unicode" という題のプレゼンテーションを行ないました。
彼のスライドの PDF バージョンが
<http://downloads.egenix.com/python/Unicode-EPC2002-Talk.pdf> から入手できます。
これは、Python の Unicode 機能のデザインの素晴しい概観になっています。

..
  Reading and Writing Unicode Data
  ================================

Unicode データを読み書きする
============================

..
  Once you've written some code that works with Unicode data, the next problem is
  input/output.  How do you get Unicode strings into your program, and how do you
  convert Unicode into a form suitable for storage or transmission?

一旦 Unicode データに対してコードが動作するように書き終えたら、次の問題は入出力です。
プログラムは Unicode 文字列をどう受けとり、どう Unicode を外部記憶装置や送受信装置に適した形式に変換するのでしょう?

..
  It's possible that you may not need to do anything depending on your input
  sources and output destinations; you should check whether the libraries used in
  your application support Unicode natively.  XML parsers often return Unicode
  data, for example.  Many relational databases also support Unicode-valued
  columns and can return Unicode values from an SQL query.

入力ソースと出力先に依存しないような方法は可能です;
アプリケーションに利用されているライブラリが Unicode をそのままサポートしているかを調べなければいけません。
例えば XML パーサーは大抵 Unicode データを返します。
多くのリレーショナルデータベースも Unicode 値の入ったコラムをサポートしていますし、
SQL の問い合わせで Unicode 値を返すことができます。

..
  Unicode data is usually converted to a particular encoding before it gets
  written to disk or sent over a socket.  It's possible to do all the work
  yourself: open a file, read an 8-bit string from it, and convert the string with
  ``unicode(str, encoding)``.  However, the manual approach is not recommended.

Unicode データは大抵の場合、ディスクに書き込んだりソケットを通して送られる前に
特定のエンコーディングに変換されます。
それらを自分自身で行なうことは可能です:
ファイルを開いて、8-bit 文字列を読み、文字列を ``unicode(str, encoding)`` で変換します。
しかし、この手動での操作は推奨できません。

..
  One problem is the multi-byte nature of encodings; one Unicode character can be
  represented by several bytes.  If you want to read the file in arbitrary-sized
  chunks (say, 1K or 4K), you need to write error-handling code to catch the case
  where only part of the bytes encoding a single Unicode character are read at the
  end of a chunk.  One solution would be to read the entire file into memory and
  then perform the decoding, but that prevents you from working with files that
  are extremely large; if you need to read a 2Gb file, you need 2Gb of RAM.
  (More, really, since for at least a moment you'd need to have both the encoded
  string and its Unicode version in memory.)

問題はエンコーディングがマルチバイトであるという性質からきています;
一つの Unicode 文字は数バイトで表現されます。
ファイルを任意のサイズ (1K または 4K) を単位 (chunk) として読みたい場合、
読み込みの単位 (chunk) の最後にエンコーディングされた一つの Unicode 文字の
バイト列の一部のみだった状況に対するエラー処理コードを書く必要がでます。
一つの解決策としてはメモリ上にファイル全体を読み込んでから、デコードを実行するという方法があります、
しかし巨大なファイルを扱うときに問題が起きます; 2Gb のファイルを読む場合、2Gb の RAM が必要です。
(正確にいうとより多くの RAM が必要です、少なくともある時点ではエンコードする文字列と
Unicode に変換した文字列の両方がメモリ上に必要とされるために)

..
  The solution would be to use the low-level decoding interface to catch the case
  of partial coding sequences.  The work of implementing this has already been
  done for you: the :mod:`codecs` module includes a version of the :func:`open`
  function that returns a file-like object that assumes the file's contents are in
  a specified encoding and accepts Unicode parameters for methods such as
  ``.read()`` and ``.write()``.

解決策は文字コードのシーケンスが途中で切れる問題を捉える
低レベルのデコーディングインターフェースを使うことです。
このインターフェースの実装は既に行なわれています:
:mod:`codecs` モジュールは :func:`open` 関数を含んでいます、
この関数はファイルの内容が指定したエンコーディングであると仮定されるファイルオブジェクトを返し、
``.read()`` and ``.write()`` のようなメソッドに対して Unicode パラメータを受けつけます。

..
  The function's parameters are ``open(filename, mode='rb', encoding=None,
  errors='strict', buffering=1)``.  ``mode`` can be ``'r'``, ``'w'``, or ``'a'``,
  just like the corresponding parameter to the regular built-in ``open()``
  function; add a ``'+'`` to update the file.  ``buffering`` is similarly parallel
  to the standard function's parameter.  ``encoding`` is a string giving the
  encoding to use; if it's left as ``None``, a regular Python file object that
  accepts 8-bit strings is returned.  Otherwise, a wrapper object is returned, and
  data written to or read from the wrapper object will be converted as needed.
  ``errors`` specifies the action for encoding errors and can be one of the usual
  values of 'strict', 'ignore', and 'replace'.

関数の引数は ``open(filename, mode='rb', encoding=None, errors='strict', buffering=1)`` です。
``mode`` は ``'r'``, ``'w'``, または ``'a'`` が受け付けられ、
通常の組み込み関数 ``open()`` 関数の引数と同様です;
ファイルを更新するには ``'+'`` を加えます。
``buffering`` は標準の関数の引数と同様です。
``encoding`` は使うエンコーディングを文字列で与えます; もし ``None`` にした場合は
8-bit 文字列を受け付ける通常の Python のファイルオブジェクトが返されます。
それ以外の引数の場合には、ラップされたオブジェクトが返され、
データは必要に応じて変換されたラッパーオブジェクトから読み書きされます。
``errors`` はエンコーディイングエラーに対する動作を指定します、
これは例の如く 'strict', 'ignore' そして 'replace' のうちのどれかをとります。

..
  Reading Unicode from a file is therefore simple::

そのためファイルから Unicode を読むのは単純です::

    import codecs
    f = codecs.open('unicode.rst', encoding='utf-8')
    for line in f:
        print repr(line)

..
  It's also possible to open files in update mode, allowing both reading and
  writing::

読み書きの両方ができる update モードでファイルを開くことも可能です::

    f = codecs.open('test', encoding='utf-8', mode='w+')
    f.write(u'\u4500 blah blah blah\n')
    f.seek(0)
    print repr(f.readline()[:1])
    f.close()
 
..
  Unicode character U+FEFF is used as a byte-order mark (BOM), and is often
  written as the first character of a file in order to assist with autodetection
  of the file's byte ordering.  Some encodings, such as UTF-16, expect a BOM to be
  present at the start of a file; when such an encoding is used, the BOM will be
  automatically written as the first character and will be silently dropped when
  the file is read.  There are variants of these encodings, such as 'utf-16-le'
  and 'utf-16-be' for little-endian and big-endian encodings, that specify one
  particular byte ordering and don't skip the BOM.

Unicode 文字 U+FEFF は byte-order-mark (BOM) として利用されます、
そしてファイルのバイト順の自動判定の役立てるためにファイルの最初の文字として書かれます。
いくつかのエンコーディング、たとえば UTF-16 では BOM がファイルの最初に存在することになっています;
そのようなエンコーディングが利用されるときには BOM は最初の文字として自動的に書き込まれ、
ファイルの読み込み時には暗黙の内に除かれます。
これらのエンコーディングには
リトルエンディアン (little-endian) とビッグエンディアン (big-endian) に対して
'utf-16-le' と 'utf-16-be' のようにエンコーディングの変種が存在します、
これらは特定のバイト順を示すもので、BOM をスキップしません。

..
  Unicode filenames
  -----------------

Unicode ファイル名
------------------

..
  Most of the operating systems in common use today support filenames that contain
  arbitrary Unicode characters.  Usually this is implemented by converting the
  Unicode string into some encoding that varies depending on the system.  For
  example, Mac OS X uses UTF-8 while Windows uses a configurable encoding; on
  Windows, Python uses the name "mbcs" to refer to whatever the currently
  configured encoding is.  On Unix systems, there will only be a filesystem
  encoding if you've set the ``LANG`` or ``LC_CTYPE`` environment variables; if
  you haven't, the default encoding is ASCII.

多くの OS では現在任意の Unicode 文字を含むファイル名をサポートしています。
通常 Unicode 文字列をシステム依存のエンコーディングに変換することによって実装されています。
例えば、Mac OS X は UTF-8 を利用し、Windows ではエンコーディングが設定で変更することが可能です;
Windows では Python は "mbcs" という名前に現在設定されているエンコーディングを問い合わせて利用します。
Unix システムでは ``LANG`` や ``LC_CTYPE`` 環境変数を設定していれば、
それだけがファイルシステムのエンコーディングとなります;
もしエンコーディングを設定しなければ、デフォルトエンコーディングは ASCII になります。

..
  The :func:`sys.getfilesystemencoding` function returns the encoding to use on
  your current system, in case you want to do the encoding manually, but there's
  not much reason to bother.  When opening a file for reading or writing, you can
  usually just provide the Unicode string as the filename, and it will be
  automatically converted to the right encoding for you::

:func:`sys.getfilesystemencoding` 関数は現在のシステムで利用するエンコーディングを返し、
エンコーディングを手動で設定したい場合利用します、ただしわざわざそうする積極的な理由はありません。
読み書きのためにファイルを開く時には、ファイル名を Unicode 文字列として渡すだけで
正しいエンコーディングに自動的に変更されます::

    filename = u'filename\u4500abc'
    f = open(filename, 'w')
    f.write('blah\n')
    f.close()

..
  Functions in the :mod:`os` module such as :func:`os.stat` will also accept Unicode
  filenames.

:func:`os.stat` のような :mod:`os` モジュールの関数も Unicode のファイル名を受け付けます。

..
  :func:`os.listdir`, which returns filenames, raises an issue: should it return
  the Unicode version of filenames, or should it return 8-bit strings containing
  the encoded versions?  :func:`os.listdir` will do both, depending on whether you
  provided the directory path as an 8-bit string or a Unicode string.  If you pass
  a Unicode string as the path, filenames will be decoded using the filesystem's
  encoding and a list of Unicode strings will be returned, while passing an 8-bit
  path will return the 8-bit versions of the filenames.  For example, assuming the
  default filesystem encoding is UTF-8, running the following program::

ファイル名を返す :func:`os.listdir` は問題を引き起こします:
この関数はファイル名を返すべきでしょうか、それともエンコードされた内容の 8-bit 文字列を返すべきでしょうか?
:func:`os.listdir` は与えられたデイレクトリへのパスが 8-bit 文字列か Unicode 文字列で与えたかに応じてその両方を返します。
パスを Unicode 文字列で与えた場合、ファイル名はファイルシステムのエンコーディングを利用してデコードされ、
Unicode 文字列のリストが返されます、8-bit パスを与えるとファイル名は 8-bit 文字列で返されます。
例えば、デフォルトのファイルシステムエンコーディングが UTF-8 と仮定される場合、以下のプログラムを実行すると::

  fn = u'filename\u4500abc'
  f = open(fn, 'w')
  f.close()

  import os
  print os.listdir('.')
  print os.listdir(u'.')

..
  will produce the following output::

以下の出力結果が生成されます::

    amk:~$ python t.py
    ['.svn', 'filename\xe4\x94\x80abc', ...]
    [u'.svn', u'filename\u4500abc', ...]

..
  The first list contains UTF-8-encoded filenames, and the second list contains
  the Unicode versions.

最初のリストは UTF-8 でエンコーディングされたファイル名を含み、第二のリストは Unicode 版を含んでいます。

..
  Tips for Writing Unicode-aware Programs
  ---------------------------------------

Unicode 対応のプログラムを書くための Tips
-----------------------------------------

..
  This section provides some suggestions on writing software that deals with
  Unicode.

この章では Unicode を扱うプログラムを書くためのいくつかの提案を紹介します。

..
  The most important tip is:
  
    Software should only work with Unicode strings internally, converting to a
    particular encoding on output.

最も重要な助言としては:

    ソフトウェア内部の動作には Unicode 文字列のみを利用し、出力時に特定のエンコーディングに変換する。

..
  If you attempt to write processing functions that accept both Unicode and 8-bit
  strings, you will find your program vulnerable to bugs wherever you combine the
  two different kinds of strings.  Python's default encoding is ASCII, so whenever
  a character with an ASCII value > 127 is in the input data, you'll get a
  :exc:`UnicodeDecodeError` because that character can't be handled by the ASCII
  encoding.

UTF-8 と 8-bit 文字列の両方を処理する関数を書こうとすると、
異なる種類の文字列を結合する際にバグが生じやすいことに気づくでしょう。
Python のデフォルトエンコーディングは ASCII なので、
ASCII の値 127 より大きい文字が入力データにあった場合、
これは ASCII エンコーディングで扱えないために、 :exc:`UnicodeDecodeError` が発生します。

..
  It's easy to miss such problems if you only test your software with data that
  doesn't contain any accents; everything will seem to work, but there's actually
  a bug in your program waiting for the first user who attempts to use characters
  > 127.  A second tip, therefore, is:
  
      Include characters > 127 and, even better, characters > 255 in your test
      data.

この問題を見逃がすのは簡単です、ソフトウェアに対してアクセントを含まないデータのみでテストを行なえばよいのです;
全てはうまく動作しているように見えます、
しかし実際には最初に 127 より大きい文字を試みたユーザにバグが待ち構えていることになります。
第二の助言は:

    テストデータには 127 より大きい文字を含み、
    さらに 255 より大きい文字を含むことが望ましい。

..
  When using data coming from a web browser or some other untrusted source, a
  common technique is to check for illegal characters in a string before using the
  string in a generated command line or storing it in a database.  If you're doing
  this, be careful to check the string once it's in the form that will be used or
  stored; it's possible for encodings to be used to disguise characters.  This is
  especially true if the input data also specifies the encoding; many encodings
  leave the commonly checked-for characters alone, but Python includes some
  encodings such as ``'base64'`` that modify every single character.

Web ブラウザからのデータやその他の信用できないところからのデータを使う場合には、
コマンド行の生成やデータベースへの記録の前に不正な文字に対するチェックを行なうことが
一般的です。
もしコマンド行生成やデータベース記録を行なう場合には、文字列が利用または保存できる形式になっているかを
一度は注意深く確かめる必要があります;
文字を偽装するためにエンコーディングを利用することは可能です。
このことは入力データのエンコーディングが指定されている場合にも可能です;
多くのエンコーディングはチェック用の文字単独をそのままにしておきますが、
Python は ``'base64'`` のような単独の文字を変更するエンコーディングも含んでいます。

..
  For example, let's say you have a content management system that takes a Unicode
  filename, and you want to disallow paths with a '/' character.  You might write
  this code::

例えば、Unicode のファイル名を取るコンテキストマネージメントシステムがあるとします、
そして '/' 文字を含むパスを拒否したいとします。
するとこのコードのように書くでしょう::

    def read_file (filename, encoding):
        if '/' in filename:
            raise ValueError("'/' not allowed in filenames")
        unicode_name = filename.decode(encoding)
        f = open(unicode_name, 'r')
        # ... return contents of file ...

..
  However, if an attacker could specify the ``'base64'`` encoding, they could pass
  ``'L2V0Yy9wYXNzd2Q='``, which is the base-64 encoded form of the string
  ``'/etc/passwd'``, to read a system file.  The above code looks for ``'/'``
  characters in the encoded form and misses the dangerous character in the
  resulting decoded form.

しかし、攻撃者が ``'base64'`` エンコーディングを指定できる場合、
攻撃者はシステムファイルを読むために ``'/etc/passwd'`` の文字列を
base-64 でエンコードした ``'L2V0Yy9wYXNzd2Q='`` を渡すことができます。
上のコードは文字 ``'/'`` をエンコードした形式で探し、
デコードした結果が危険な文字となる場合を見逃してしまいます。

..
  References
  ----------

参考文献
--------

..
  The PDF slides for Marc-André Lemburg's presentation "Writing Unicode-aware
  Applications in Python" are available at
  <http://downloads.egenix.com/python/LSM2005-Developing-Unicode-aware-applications-in-Python.pdf>
  and discuss questions of character encodings as well as how to internationalize
  and localize an application.

Marc-André Lemburg のプレゼンテーション
"Writing Unicode-aware Applications in Python" の PDF スライドが
<http://downloads.egenix.com/python/LSM2005-Developing-Unicode-aware-applications-in-Python.pdf>
から入手可能です、そして文字エンコーディングの問題と同様にアプリケーションの国際化やローカライズについても議論されています。

..
  Revision History and Acknowledgements
  =====================================

更新履歴と謝辞
==============

..
  Thanks to the following people who have noted errors or offered suggestions on
  this article: Nicholas Bastin, Marius Gedminas, Kent Johnson, Ken Krugler,
  Marc-André Lemburg, Martin von Löwis, Chad Whitacre.

この記事中の誤りの指摘や提案を申し出てくれた以下の人々に感謝します:
Nicholas Bastin, Marius Gedminas, Kent Johnson, Ken Krugler,
Marc-André Lemburg, Martin von Löwis, Chad Whitacre.

Version 1.0: posted August 5 2005.

Version 1.01: posted August 7 2005.  Corrects factual and markup errors; adds
several links.

Version 1.02: posted August 16 2005.  Corrects factual errors.

Version 1.03: posted June 20 2010.  Notes that Python 3.x is not covered,
and that the HOWTO only covers 2.x.

.. comment Describe Python 3.x support (new section? new document?)
.. comment Additional topic: building Python w/ UCS2 or UCS4 support
.. comment Describe obscure -U switch somewhere?
.. comment Describe use of codecs.StreamRecoder and StreamReaderWriter

.. comment
   Original outline:

   - [ ] Unicode introduction
       - [ ] ASCII
       - [ ] Terms
	   - [ ] Character
	   - [ ] Code point
	 - [ ] Encodings
	    - [ ] Common encodings: ASCII, Latin-1, UTF-8
       - [ ] Unicode Python type
	   - [ ] Writing unicode literals
	       - [ ] Obscurity: -U switch
	   - [ ] Built-ins
	       - [ ] unichr()
	       - [ ] ord()
	       - [ ] unicode() constructor
	   - [ ] Unicode type
	       - [ ] encode(), decode() methods
       - [ ] Unicodedata module for character properties
       - [ ] I/O
	   - [ ] Reading/writing Unicode data into files
	       - [ ] Byte-order marks
	   - [ ] Unicode filenames
       - [ ] Writing Unicode programs
	   - [ ] Do everything in Unicode
	   - [ ] Declaring source code encodings (PEP 263)
       - [ ] Other issues
	   - [ ] Building Python (UCS2, UCS4)
