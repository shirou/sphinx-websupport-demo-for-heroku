.. _extending-distutils:

***************
Distutilsの拡張
***************

Distutilsは様々な方法で拡張できます。ほとんどの拡張は存在するコマンド
を新しいコマンドで置換する形でおこなわれます。新しいコマンドはたとえば
存在するコマンドを置換して、そのコマンドでパッケージをどう処理するかの
細部を変更することでプラットフォーム特有のパッケージ形式をサポートする
ために書かれているかもしれません

ほとんどのdistutilsの拡張は存在するコマンドを変更したい :file:`setup.py`
スクリプト中で行われます。ほとんどはパッケージにコピーされるファイル拡
張子を :file:`.py` の他に、いくつか追加するものです。

ほとんどのdistutilsのコマンド実装は :mod:`distutils.cmd` の
:class:`distutils.cmd.Command` クラスのサブクラスとして実装されています。
新しいコマンドは :class:`Command` を直接継承し、置換するコマンドでは
置換対象のコマンドのサブクラスにすることで :class:`Command` を間接的に
継承します。
コマンドは :class:`Command` から派生したものである必要があります。

.. % \section{Extending existing commands}
.. % \label{extend-existing}

.. % \section{Writing new commands}
.. % \label{new-commands}
.. % \XXX{Would an uninstall command be a good example here?}


新しいコマンドの統合
====================

新しいコマンド実装を統合するにはいくつかの方法があります。一番難しいものは新機能をdistutils本体に取り込み、それのサポートを提供するPythonの
バージョンが出ることを待つ(そして使う)ことです。これは様々な理由で本当に難しいことです。

もっとも一般的な、そしておそらくほとんどの場合にもっとも妥当な方法は、新しい実装をあなたの :file:`setup.py` スクリプトに取り込み、
:func:`distutils.core.setup` 関数でそれらを使うようにすることです。 ::

   from distutils.command.build_py import build_py as _build_py
   from distutils.core import setup

   class build_py(_build_py):
       """Specialized Python source builder."""

       # implement whatever needs to be different...

   setup(cmdclass={'build_py': build_py},
         ...)

このアプローチは新実装をある特定のパッケージで利用したい時、
そのパッケージに興味をもつ人全員がコマンドの新実装を必要とする時
にもっとも価値があります。

Python 2.4から、インストールされたPythonを変更せずに、既存の
:file:`setup.py` スクリプトをサポートするための3つめの選択肢が利用
できるようになりました。
これは追加のパッケージングシステムのサポートを追加するサードパーティ拡
張を提供することを想定していますが、これらのコマンドはdistutilsが利用
されている何にでも利用可能です。新しい設定オプション :option:`command_packages`
(コマンドラインオプション :option:`--command-packages`) は、
コマンド実装モジュールを検索する追加のパッケージを指定するために利用できます。 distutilsの全てのオプショ
ンと同様に、このオプションもコマンドラインまたは設定ファイルで指定できます。このオプションは設定ファイル中では ``[global]`` セクションか、コマン
ドラインのコマンドより前でだけ設定できます。設定ファイル中で指定する場合、コマンドラインで上書きすることができます。
空文字列を指定するとデフォルト値が使われます。これはパッケージと一緒に提供する設定ファイルでは指定しないでください。

この新オプションによってコマンド実装を探すためのパッケージをいくつでも追加することができます。複数のパッケージ名はコンマで区切って指定します。
指定がなければ、検索は :mod:`distutils.command` パッケージのみで行われます。ただし :file:`setup.py` がオプション
:option:`--command-packages`  :option:`distcmds,buildcmds` で実行されている場合には、パッケージは
:mod:`distutils.command` 、 :mod:`distcmds` 、そして :mod:`buildcmds` を、この順番で検索します。
新コマンドはコマンドと同じ名前のモジュールに、コマンドと同じ名前のクラスで実装されていると想定しています。上のコマドラインオプションの例では、コマンド
:command:`bdist_openpkg` は、 :class:`distcmds.bdist_openpkg.bdist_openpkg` か、
:class:`buildcmds.bdist_openpkg.bdist_openpkg` で実装されるかもしれません。

.. % \section{Adding new distribution types}


配布物の種類を追加する
======================

配布物 (:file:`dist/` ディレクトリの中のファイル) を作成するコマンドは、 :command:`upload`
がその配布物をPyPIにアップロードできるように、 ``(command, filename)`` のペアを
``self.distributions.dist_files`` に追加する必要があります。ペア中の *filename*
はパスに関する情報を持たず、単にファイル名だけを持ちます。 dry-run モードでも、何が作成されたかを示すために、同じペアが必要になります。


