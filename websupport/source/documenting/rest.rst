.. highlightlang:: rest

reStructuredText の基礎
=======================

この節は reStructuredText (reST) のコンセプトと文法の要約です。
ドキュメント作者の生産性のために十分な情報を提供することに注目しています。
reST はシンプルで、出しゃばらないマークアップ言語として設計されたので、
この文章はあまり長くありません。

.. seealso::

    The authoritative `reStructuredText User
    Documentation <http://docutils.sourceforge.net/rst.html>`_.


段落 (Paragraphs)
-----------------

段落は reST においてもっとも基本的なブロックです。
一行以上の空行で区切られただけのテキストの固まりが段落になります。
Python と同じく、 reST ではインデントは重要な意味を持つので、同じ段落に属す
行は全て同じインデントレベルで左揃えする必要があります。


インラインマークアップ (Inline markup)
--------------------------------------

reST 標準のインラインマークアップは非常にシンプルです。

* アスタリスク一つ: ``*text*`` を強調 (斜体) に、
* アスタリスク二つ: ``**text**`` を強い強調 (太字) に、
* バッククォート: ````text```` をサンプルコードに、

使ってください。

もしアスタリスクやバッククォートが通常のテキストの中で出てきて、インラインマーク
アップ用の区切り文字と混合する場合は、バックスラッシュ(訳注: 日本語フォントでは、
一般的に円記号になります)でエスケープする必要があります。

インラインマークアップの幾つかの制限に気をつけてください:

* ネストできません。
* マークアップされる内容の先頭や終端に空白文字があってはなりません:
  ``* text*`` は間違いです。
* マークアップの外側は、non-word 文字で囲まれていなければなりません。
  必要な場合はバックスラッシュでエスケープしたスペースを使ってください: ``thisis\ *one*\ word``

これらの制限は将来のバージョンの docutils で解除されるかもしれません。

reST は独自の "interpreted text roles" に対応していて、囲まれたテキストを専用の
方法で解釈することができます。別の節で解説しますが、Sphinx はこれを、
意味に基づくマークアップと識別子のクロスリファレンスのために利用しています。
"interpreted text roles" の一般的な文法は ``:rolename:`内容``` になります。


リストとクォート (Lists and Quotes)
-----------------------------------

.. List markup is natural: just place an asterisk at the start of a paragraph and
.. indent properly.  The same goes for numbered lists; they can also be
.. autonumbered using a ``#`` sign::

リストの表現は自然です: 段落の最初にアスタリスクをおいて、適切にインデント
するだけです。番号付きリストも同じで、 ``#`` 記号を使えば自動的にナンバリング
されます::

   * これは番号なしリストです。
   * リストの要素は二つあり、二つ目は
     二行使用しています。

   #. これば番号付きリストです。
   #. こちらも要素が二つあります。

..    * This is a bulleted list.
..    * It has two items, the second
..      item uses two lines.
..
..    #. This is a numbered list.
..    #. It has two items too.

.. Nested lists are possible, but be aware that they must be separated from the
.. parent list items by blank lines::

リストはネストさせることもできます。親になるリスト要素との間に空行が必要な
ことに気をつけてください::

   * これは
   * リストで

     * ネストされたリストと
     * 子要素があります。

   * そしてここは親のリストの続きです。

..    * this is
..    * a list
..
..      * with a nested list
..      * and some subitems
..
..    * and here the parent list continues

.. Definition lists are created as follows::

定義リストは次のようにして作ります::

   単語 (行の終わりまで)
      単語の定義。インデントされている必要がある。

      複数の段落を持つことも可能。

   次の単語
      定義。

..    term (up to a line of text)
..       Definition of the term, which must be indented
..
..       and can even consist of multiple paragraphs
..
..    next term
..       Description.

.. Paragraphs are quoted by just indenting them more than the surrounding
.. paragraphs.

定義の部分は周りの段落よりも深くインデントします。


.. Source Code
.. -----------

ソースコード (Source Code)
--------------------------

.. Literal code blocks are introduced by ending a paragraph with the special marker
.. ``::``.  The literal block must be indented, to be able to include blank lines::

リテラルコードブロックは、特別なマーカー ``::`` で終わる段落の次に始まります。
リテラルブロックはインデントしなければなりません。 ::

   これは通常の段落です。次の段落はコードサンプルです::

      ここには、インデントの除去以外の
      処理が行われません。

      複数行にまたがることもできます。

   ここでまた通常の段落になります。

..    This is a normal text paragraph. The next paragraph is a code sample::
..
..       It is not processed in any way, except
..       that the indentation is removed.
..
..       It can span multiple lines.
..
..    This is a normal text paragraph again.

.. The handling of the ``::`` marker is smart:

``::`` マーカーの処理はスマートです:

.. * If it occurs as a paragraph of its own, that paragraph is completely left
..   out of the document.
.. * If it is preceded by whitespace, the marker is removed.
.. * If it is preceded by non-whitespace, the marker is replaced by a single
..   colon.

* 単体で段落になっていた場合は、その段落はドキュメントから完全に除去されます。
* マーカーの前に空白があれば、マーカーは削除されます。
* マーカーの前が空白でなければ、マーカーはコロン一つに置き換えられます。

.. That way, the second sentence in the above example's first paragraph would be
.. rendered as "The next paragraph is a code sample:".

なので、上の例での最初の段落の二つ目の文は、 "次の段落はコードサンプルです:" と
出力されます。


.. Hyperlinks
.. ----------

ハイパーリンク (Hyperlinks)
----------------------------

.. External links
.. ^^^^^^^^^^^^^^

外部リンク (External links)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Use ```Link text <http://target>`_`` for inline web links.  If the link text
.. should be the web address, you don't need special markup at all, the parser
.. finds links and mail addresses in ordinary text.

インラインでのWebリンクには、 ```リンク文字列 <http://target>`_`` を使ってください。
リンク文字列をアドレスにする場合は、マークアップしなくても、パーサーがリンクや
メールアドレスを見つけて処理します。

.. Internal links
.. ^^^^^^^^^^^^^^

内部リンク (Internal links)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Internal linking is done via a special reST role, see the section on specific
.. markup, :ref:`doc-ref-role`.

内部リンクには、reSTの特別な role を利用します。特別なマークアップのセクションを
見てください。 :ref:`doc-ref-role`


.. Sections
.. --------

セクション
^^^^^^^^^^

.. XXX: punctuation は記号で良いのか？
.. Section headers are created by underlining (and optionally overlining) the
.. section title with a punctuation character, at least as long as the text::

セクションヘッダは、記号を使って、セクションタイトルにそれ以上の長さのアンダーライン
(とオプションでオーバーライン) を引いて作ります。::

   ==============
   ここにタイトル
   ==============

..    =================
..    This is a heading
..    =================

.. Normally, there are no heading levels assigned to certain characters as the
.. structure is determined from the succession of headings.  However, for the
.. Python documentation, we use this convention:

通常、特定の文字に特定の見出しレベルが割り当てられておらず、ヘッダ構造から
自動的にレベルが決まります。しかし、 Python ドキュメントにおいては、以下の
ルールを使います:

* ``#`` (オーバーライン付き) を編(part) に
* ``*`` (オーバーライン付き) を章(chapter) に
* ``=`` を節(section) に
* ``-`` を項(subsection) に
* ``^`` を小区分(subsubsection) に
* ``"`` を段落(paragraph) に

.. * ``#`` with overline, for parts
.. * ``*`` with overline, for chapters
.. * ``=``, for sections
.. * ``-``, for subsections
.. * ``^``, for subsubsections
.. * ``"``, for paragraphs

.. Explicit Markup
.. ---------------

明示的なマークアップ (Explicit Markup)
--------------------------------------

.. "Explicit markup" is used in reST for most constructs that need special
.. handling, such as footnotes, specially-highlighted paragraphs, comments, and
.. generic directives.

reST において、 "明示的なマークアップ (explicit markup)" は、脚注、特別な
ハイライト付きの文、コメント、一般的な指定のために利用されます。

.. An explicit markup block begins with a line starting with ``..`` followed by
.. whitespace and is terminated by the next paragraph at the same level of
.. indentation.  (There needs to be a blank line between explicit markup and normal
.. paragraphs.  This may all sound a bit complicated, but it is intuitive enough
.. when you write it.)

明示的なマークアップのブロックは、 ``..`` に空白が続いたものが行頭にあるときに
始まり、次の段落が同じインデントになるところで終わります。 (明示的なマークアップと
通常の段落の間には空行が必要です。すこし複雑に思えるかもしれませんが、ドキュメントを
書くときには十分に直感的です。)

.. Directives
.. ----------

ディレクティブ (Directives)
---------------------------

.. A directive is a generic block of explicit markup.  Besides roles, it is one of
.. the extension mechanisms of reST, and Sphinx makes heavy use of it.

ディレクティブは一般的な、明示的なマークアップを行うブロックです。 role のような
reSTの拡張メカニズムの一つで、 Sphinx はディレクティブを多用しています。

.. Basically, a directive consists of a name, arguments, options and content. (Keep
.. this terminology in mind, it is used in the next chapter describing custom
.. directives.)  Looking at this example, ::

基本的に、ディレクティブは、名前、引数、オプション、内容で構成されます。
(この XXX を覚えておいてください。次の章でカスタムディレクティブを説明するときに
出てきます。) 次の例を見てください ::

   .. function:: foo(x)
                 foo(y, z)
      :bar: no

      ユーザーから入力されたテキスト一行を返す.

..    .. function:: foo(x)
..                  foo(y, z)
..       :bar: no
..
..       Return a line of text input from the user.

.. ``function`` is the directive name.  It is given two arguments here, the
.. remainder of the first line and the second line, as well as one option ``bar``
.. (as you can see, options are given in the lines immediately following the
.. arguments and indicated by the colons).

``function`` はディレクティブの名前です。ここでは引数が二つあり、一つは一行目の
残りの部分で、もう一つは次の行です。オプションも一つ、 ``bar`` があります。
(ごらんの通り、オプションは引数の行のすぐ次の行にあり、コロンで示されます.)

.. The directive content follows after a blank line and is indented relative to the
.. directive start.

一行の空行を挟んでディレクティブの内容が続きます。内容はディレクティブの開始位置と
同じ場所までインデントされます。


.. Footnotes
.. ---------

脚注 (Footnotes)
----------------

.. For footnotes, use ``[#]_`` to mark the footnote location, and add the footnote
.. body at the bottom of the document after a "Footnotes" rubric heading, like so::

脚注を使うときは、 ``[#]_`` を使って脚注を入れる場所を示し、脚注の内容はドキュメントの
最後に、次の例のように、"Footnotes" [#]_ という rubric ヘッダの後に書きます。 ::

   Lorem ipsum [#]_ dolor sit amet ... [#]_

   .. rubric:: Footnotes

   .. [#] 最初の脚注の内容
   .. [#] 二つ目の脚注の内容

..    Lorem ipsum [#]_ dolor sit amet ... [#]_
..
..    .. rubric:: 注記
..
..    .. [#] Text of the first footnote.
..    .. [#] Text of the second footnote.


.. Comments
.. --------

コメント (Comments)
-------------------

.. Every explicit markup block which isn't a valid markup construct (like the
.. footnotes above) is regared as a comment.

（上の脚注のような）有効なマークアップになっていない、全ての明示的な
マークアップブロックは、コメントとして扱われます。

.. Source encoding
.. ---------------

ソースのエンコード (Source encoding)
------------------------------------

.. Since the easiest way to include special characters like em dashes or copyright
.. signs in reST is to directly write them as Unicode characters, one has to
.. specify an encoding:

em dash や copyright sign のような特別な文字を reST に含める最も簡単な方法は
Unicode文字を使って直接記述することなので、そのエンコードを決める必要があります。

.. All Python documentation source files must be in UTF-8 encoding, and the HTML
.. documents written from them will be in that encoding as well.

全ての Python ドキュメントのソースファイルは UTF-8 エンコードでなければなりません。
そしてHTMLドキュメントもUTF-8で出力するのが良いでしょう。

判っていること
--------------

reST ドキュメントをオーサリングするときに良く問題になることがあります:

* **インラインマークアップの区切り:** 上で述べたように、インラインマークアップは
  囲っているテキストと non-word 文字で区切られています。
  スペースを囲むときにはエスケープが必要になります。

.. rubric:: 注記

.. [#] 訳注：Sphinx 1.0 以降では日本語で Footnotes の代わりに "注記" も許容されるようです。

