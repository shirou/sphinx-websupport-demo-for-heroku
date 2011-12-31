.. highlightlang:: rest

LaTeX マークアップとの違い
===============================

マークアップ言語は変わりましたが、もとの LaTeX ドキュメントにあったコンセプトや
ドキュメント型(markup types) はほとんど残っています -- 環境(environments) は reST
ディレクティブ、インラインコマンドは reST roles などなど。

しかし、それらがどう動作するのか(the way these work)については、マークアップ言語の
違いのため、もしくは Sphinx の改善のために、いくらか異なっています。
このセクションでは、古いフォーマットに慣れた人に新しいフォーマットでどう変わったのか
概要を示すために、違いをリストアップしていきます。

インラインマークアップ
-----------------------

インラインマークアップには以下の変更点があります:

* **クロスリファレンス roles**

  以下の semantic roles は以前はインラインコマンドで、 code としてフォーマット
  する以外には何もしませんでした。
  今は、既知のターゲットに対してクロスリファレンスになります。
  (あと、いくつかの名前は短くなっています):

  | *mod* (previously *refmodule* or *module*)
  | *func* (previously *function*)
  | *data* (new)
  | *const*
  | *class*
  | *meth* (previously *method*)
  | *attr* (previously *member*)
  | *exc* (previously *exception*)
  | *cdata*
  | *cfunc* (previously *cfunction*)
  | *cmacro* (previously *csimplemacro*)
  | *ctype*

  *func* と *meth* の扱いにも違いがあります: 以前は丸括弧を呼び出し可能オブジェクト名の
  後ろに (``\func{str()}`` のように) 書きましたが、ビルドシステムが丸括弧をつけるように
  なりました。　-- ソースファイルに丸括弧を書くと、出力では二重に括弧がついてしまいます。
  ``:func:`str(object)``` も期待通りになりません。
  代わりに ````str(object)```` を使ってください!

* **インラインコマンドはディレクティブとして実装されました**

  LaTeX にはインラインコマンドがありましたが、 reST ではディレクティブになりました:

  | *deprecated*
  | *versionadded*
  | *versionchanged*

  次のようにして使います::

     .. deprecated:: 2.5
        Reason of deprecation.

  同じく、 *versionadded* と *versionchanged* のテキストにはピリオドがつきません。
  *versionchanged*.

  | *note*
  | *warning*

  これらは次のように使います::

     .. note::

        Content of note.

* **その他の変更されたコマンド**

  以前の *samp* コマンドは、 code フォーマットでクォーテーションマークで囲まれていました。
  *samp* role では、 *file* と同じくコードハイライトの機能が新しく追加されました:

     ``:samp:`open({filename}, {mode})``` results in :samp:`open({filename}, {mode})`

* **無くなったコマンド**

  次の LaTeX にあったコマンドは、現在 role では対応していません:

  | *bfcode*
  | *character* (use :samp:`\`\`'c'\`\``)
  | *citetitle* (use ```Title <URL>`_``)
  | *code* (use ````code````)
  | *email* (just write the address in body text)
  | *filenq*
  | *filevar* (use the ``{...}`` highlighting feature of *file*)
  | *programopt*, *longprogramopt* (use *option*)
  | *ulink* (use ```Title <URL>`_``)
  | *url* (just write the URL in body text)
  | *var* (use ``*var*``)
  | *infinity*, *plusminus* (use the Unicode character)
  | *shortversion*, *version* (use the ``|version|`` and ``|release|`` substitutions)
  | *emph*, *strong* (use the reST markup)

* **バックスラッシュによるエスケープ**

  reSTでは、バックスラッシュは通常のテキストや role の中ではエスケープしないといけません。
  しかし、 code リテラルやリテラルブロックではエスケープしてはいけません。
  例えば:  ``:file:`C:\\Temp\\my.tmp``` vs. ````open("C:\Temp\my.tmp")````.

情報単位 (information units)
----------------------------

情報単位(information units) (latexでは *...desc* という環境) は reST ディレクティブで作ります。
説明しておかないといけない情報単位に関する変更点は:

* **新しい名前**
  すべての名前から "desc" が無くなりました。新しい名前は:

  | *cfunction* (以前は *cfuncdesc*)
  | *cmacro* (以前は *csimplemacrodesc*)
  | *exception* (以前は *excdesc*)
  | *function* (以前は *funcdesc*)
  | *attribute* (以前は *memberdesc*)

  *classdesc* と *excclassdesc* 環境は無くなりました。代わりに、 *class* と *exception*
  ディレクティブがコンストラクタの引数あり・なしでクラスのドキュメントをサポートします。

* **複数のオブジェクト**
  *...line* というコマンドと等価なのは::

     .. function:: do_foo(bar)
                   do_bar(baz)

        Description of the functions.

  言い換えると、同じインデントレベルに複数のシグネチャを一行ずつ書くだけです。

* **引数**

  *optional* コマンドはありません。単純に関数のシグネチャを出力で表示されるのと同じ形で書いてください。 ::

     .. function:: open(filename[, mode[, buffering]])

        Description.

  注意: シグネチャの中ではマークアップはサポートされません。

* **Indexing**

  *...descni* 環境は無くなりました。情報単位をインデックスエントリに含めないようにするには、
  *noindex* オプションを次のように利用してください::

     .. function:: foo_*
        :noindex:

        Description.

* **新しい情報単位**

  新しい汎用情報単位があります。一つは "describe" と呼ばれ、他の情報単位の
  対象にならない単位に使うことができます::

     .. describe:: a == b

        The equals operator.

  他には次のような単位があります::

     .. cmdoption:: -O

        Describes a command-line option.

     .. envvar:: PYTHONINSPECT

        Describes an environment variable.

構造 (Structure)
-----------------

LaTeX ドキュメントはいくつかのトップレベルマニュアルに分割されていました。
今は、すべてのファイルは *toctree* ディレクティブで指定される一つのドキュメントツリーの一部です。
(各出力フォーマットでまたファイルを分割することもできます)
すべての *toctree* ディレクティブは他のファイルを現在のファイルのサブドキュメントとして埋め込みます。
(この構造をファイルシステムレイアウトに反映させる必要はありません)
トップレベルのファイルは :file:`contents.rst` です。

しかし、今までのディレクトリ構造の大部分は、次のように名前を変更されながら残っています:

* :file:`api` -> :file:`c-api`
* :file:`dist` -> :file:`distutils`, with the single TeX file split up
* :file:`doc` -> :file:`documenting`
* :file:`ext` -> :file:`extending`
* :file:`inst` -> :file:`installing`
* :file:`lib` -> :file:`library`
* :file:`mac` -> merged into :file:`library`, with :file:`mac/using.tex`
  moved to :file:`using/mac.rst`
* :file:`ref` -> :file:`reference`
* :file:`tut` -> :file:`tutorial`, with the single TeX file split up


.. XXX more (index-generating, production lists, ...)
