.. _package-upload:

**********************************************
パッケージを Package Index にアップロードする
**********************************************

.. versionadded:: 2.5

Python Package Index (PyPI) は、パッケージ情報に加えて、作者が望むのであればパッケージデータを置くこともできます。
distutils の :command:`upload` コマンドは配布物をPyPIにアップロードします。

このコマンドは一つ以上の配布物ファイルをビルドした直後に呼び出されます。例えば、次のコマンド ::

    python setup.py sdist bdist_wininst upload

は、ソース配布物とWindowsのインストーラをPyPIにアップロードします。以前に :file:`setup.py`
を実行してビルドした配布物もアップロード対象になるけれども、アップロードされるのは :command:`upload` コマンドと同時に
指定された配布物だけだということに注意してください。

:command:`upload` コマンドは、 :file:`$HOME/.pypirc` ファイル (詳しくは :ref:`pypirc` セクションを
ご覧下さい) の、ユーザー名、パスワードとリポジトリURLを利用します。
同じコマンド内で :command:`register` コマンドが呼ばれていて、そこでプロンプトから
パスワードを入力した場合、 :command:`upload` は入力されたパスワードを再利用します。
:file:`$HOME/.pypirc` ファイルにプレインテキストでパスワードを保存したくない場合は
この方法を利用できます。

:option:`--repository=*url*` オプションを使って別のPyPIサーバーを指定することができます。 ::

    python setup.py sdist bdist_wininst upload -r http://example.com/pypi

複数のサーバーを定義することについて、より詳しい情報は :ref:`pypirc` を参照してください。

:option:`--sign` オプションで、アップロードする各ファイルにGPG (GNU Privacy Guard) を使うことができます。
:program:`gpg` プログラムが環境変数 :envvar:`PATH` から実行可能である必要があります。
署名にどの鍵を使うかを、 :option:`--identity=*name*` で指定することもできます。

他の :command:`upload` のオプションには、 :option:`--repository=<url>` (*url*
はサーバーのURL), :option:`--repository=<section>` (*section* は :file:`$HOME/.pypirc`
のセクション名), :option:`--show-response`
(アップロードの問題をデバッグするために、PyPI サーバーからの全てのレスポンスを表示する)があります。

.. PyPI package display

PyPI パッケージ表示
====================

``long_description`` フィールドは PyPI において特別な役目を持ちます。
サーバーは登録されたパッケージのホームページを表示するためにこれを利用します。

このフィールドに `reStructuredText <http://docutils.sourceforge.net/rst.html>`_
記法を利用した場合、 PyPI はこれをパースして、パッケージのホームページにHTML
出力を表示します。

``long_description`` フィールドにパッケージ内のファイルの内容を利用することもできます。 ::

    from distutils.core import setup

    with open('README.txt') as file:
        long_description = file.read()

    setup(name='Distutils',
          long_description=long_description)

この例では、 :file:`README.txt` は通常の reStructuredText テキストファイルで、
:file:`setup.py` と同じパッケージのルートディレクトリに置かれています。

壊れた reStructuredText を登録してしまうのを防ぐために、コマンドラインから
:mod:`docutils` パッケージが提供している :program:`rst2html` プログラムを
利用して ``long_description`` をチェックすることができます。 ::

    $ python setup.py --long-description | rst2html.py > output.html

文法に問題がある場合は、 :mod:`docutils` は警告を表示するはずです。
