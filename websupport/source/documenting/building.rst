ドキュメントをビルドする
==========================

.. Building the documentation

.. You need to have Python 2.4 or higher installed; the toolset used to build the
   docs is written in Python.  It is called *Sphinx*, it is not included in this
   tree, but maintained separately.  Also needed are the docutils, supplying the
   base markup that Sphinx uses, Jinja, a templating engine, and optionally
   Pygments, a code highlighter.

ドキュメントをビルドするために使われるツールセットは Python で書かれて
いるので、 Python 2.4 以上をインストールしておく必要があります。
このツールセットは *Sphinx* と呼ばれていて、 Python ソースコードツリーには
含まれておらず、別に管理されています。
他にも、 Sphinx が利用しているマークアップの基礎を提供している docutils と、
テンプレートエンジンの Jinja, オプションでコードハイライトをしたい場合は
Pygments が必要です。

.. Using make

make を使う方法
----------------

.. Luckily, a Makefile has been prepared so that on Unix, provided you have
   installed Python and Subversion, you can just run ::

Makefile が用意されているので、 Python と Subversion がインストールされている
Unix 環境では、シンプルに次のコマンドを実行するだけです。 ::

   make html

.. to check out the necessary toolset in the `tools/` subdirectory and build the
   HTML output files.  To view the generated HTML, point your favorite browser at
   the top-level index `build/html/index.html` after running "make".

このコマンドは必要なツールセットを `tools/` サブディレクトリ配下に
チェックアウトし、　HTML 形式の出力ファイルをビルドします。
出力された HTML ファイルを見るには、 "make" が完了してから、
お好きなブラウザでトップページになる `build/html/index.html` ファイルを
開いてください。

.. Available make targets are:

利用できる make の target は次のとおりです。

.. * "html", which builds standalone HTML files for offline viewing.

 * "html" は、オフラインで閲覧可能なスタンドアロンの HTML ファイルを
   ビルドします。

.. * "htmlhelp", which builds HTML files and a HTML Help project file usable to
   convert them into a single Compiled HTML (.chm) file -- these are popular
   under Microsoft Windows, but very handy on every platform.

.. To create the CHM file, you need to run the Microsoft HTML Help Workshop
   over the generated project (.hhp) file.

 * "htmlhelp" は、 HTML ファイルに加えて、単一のコンパイル済みHTMLファイル
   (.chm) に変換するためのHTML Help プロジェクトファイルをビルドします。
   これは Microsoft Windows で一般的なフォーマットですが、それ以外の
   プラットフォームでも便利です。

   CHM ファイルを作成するには、生成されたプロジェクトファイル (.hhp) に対して
   Microsoft HTML Help Workshop を実行します。

.. * "latex", which builds LaTeX source files as input to "pdflatex" to produce
   PDF documents.

 * "latex" は、 LaTeX ソースファイルをビルドします。 "pdflatex" を利用して、
   PDF ドキュメントを生成できます。

.. * "text", which builds a plain text file for each source file.

 * "text" は、各ソースファイルに対してプレインテキストファイルを作成します。

.. * "linkcheck", which checks all external references to see whether they are
   broken, redirected or malformed, and outputs this information to stdout
   as well as a plain-text (.txt) file.

 * "linkcheck" は、全ての外部参照リンクをチェックして、リンクが壊れていたり、
   リダイレクトされていたり、利用できなくなっていないかを調べます。
   結果の情報は標準出力とプレインテキスト (.txt) ファイルに出力されます。

.. * "changes", which builds an overview over all versionadded/versionchanged/
   deprecated items in the current version. This is meant as a help for the
   writer of the "What's New" document.

 * "changes" は、現在のバージョンの要素にある全ての versionadded/
   versionchanged/deprecated の概要をビルドします。これは、 "What's New"
   ドキュメントの著者のためのものです。

.. * "coverage", which builds a coverage overview for standard library modules
   and C API.

 * "coverage" は、標準ライブラリモジュールと C API に対するカバレッジ情報を
   ビルドします。

.. * "pydoc-topics", which builds a Python module containing a dictionary with
   plain text documentation for the labels defined in
   `tools/sphinxext/pyspecific.py` -- pydoc needs these to show topic and
   keyword help.

 * "pydoc-topics" は、 `tools/sphinxext/pyspecific.py` で定義されているラベル
   とそれに対するプレインテキスト形式のドキュメントを含む辞書を格納した
   Python モジュールをビルドします。これは、 pydoc が topic や
   キーワードヘルプを表示するときに必要になります。


.. A "make update" updates the Subversion checkouts in `tools/`.

"make update" を実行すると、 `tools/` 以下の Subversion チェックアウトを
更新します。


.. Without make

make を使わない方法
--------------------

.. You'll need to install the Sphinx package, either by checking it out via :

Sphinx パッケージを、 PyPI からインストールするか、次のコマンドでチェックアウト
してください。 ::

   svn co http://svn.python.org/projects/external/Sphinx-0.6.5/sphinx tools/sphinx

.. Then, you need to install Docutils, either by checking it out via :

次に、 docutils を、 http://docutils.sf.net/ からインストールするか、
次のコマンドでチェックアウトしてください。 ::

   svn co http://svn.python.org/projects/external/docutils-0.6/docutils tools/docutils

.. You also need Jinja2, either by checking it out via ::

Jinja2 も必要です。 PyPI からインストールするか、次のコマンドでチェックアウト
してください。 ::

   svn co http://svn.python.org/projects/external/Jinja-2.3.1/jinja2 tools/jinja2

.. You can optionally also install Pygments, either as a checkout via :

任意で、 Pygments をインストールすることもできます。 PyPI の
http://pypi.python.org/pypi/Pygments からインストールするか、次のコマンドで
チェックアウトしてください。 ::

   svn co http://svn.python.org/projects/external/Pygments-1.3.1/pygments tools/pygments


.. Then, make an output directory, e.g. under `build/`, and run :

出力ディレクトリ (例では `build/` とします) を作成し、次のコマンドを
実行します。 ::

   python tools/sphinx-build.py -b<builder> . build/<出力ディレクトリ>

`<builder>` は、 html, text, latex, htmlhelp のどれかです。
(説明は上にある make の target を参照してください)
