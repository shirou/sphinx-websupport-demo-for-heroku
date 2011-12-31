.. highlightlang:: none

.. _using-on-unix:

***************************************
 Unix プラットフォームで Python を使う
***************************************

.. sectionauthor:: Shriphani Palakodety


最新バージョンの Python の取得とインストール
==============================================

Linux
--------

ほとんどの Linux ディストリビューションでは Python はプリインストールされており、
それ以外の Linux ディストリビューションでも パッケージとして利用可能です。
しかし、ディストリビューションのパッケージでは、利用したい機能が使えない場合があります。
最新版の Python をソースから簡単にコンパイルすることができます。

Python がプリインストールされておらず、リポジトリにも無い場合、ディストリビューション用の
パッケージを簡単につくることができます。以下のリンクを参照してください。

.. seealso::

   http://www.linux.com/articles/60383
      for Debian users
   http://linuxmafia.com/pub/linux/suse-linux-internals/chapter35.html
      for OpenSuse users
   http://docs.fedoraproject.org/drafts/rpm-guide-en/ch-creating-rpms.html
      for Fedora users
   http://www.slackbook.org/html/package-management-making-packages.html
      for Slackware users


FreeBSD と OpenBSD
----------------------

* FreeBSD ユーザーは、 Python のパッケージを追加するために次のようにしてください。 ::

     pkg_add -r python

* OpenBSD ユーザーはこうです。 ::

     pkg_add ftp://ftp.openbsd.org/pub/OpenBSD/4.2/packages/<アーキテクチャ>/python-<バージョン>.tgz

  たとえば、 i386 ユーザーが Python 2.5.1 を取得するには、次のようにします。 ::

     pkg_add ftp://ftp.openbsd.org/pub/OpenBSD/4.2/packages/i386/python-2.5.1p2.tgz


OpenSolaris
--------------

OpenSolaris に最新版の Python をインストールするには、 blastwave
(http://www.blastwave.org/howto.html) をインストールして、プロンプトから
"pkg_get -i python" とタイプしてください。


Python のビルド
===============

CPython を自分でコンパイルしたい場合、最初にするべきことは
`ソース <http://python.org/download/source/>`_ を取得することです。
最新リリース版のソースか、新しい
`チェックアウト
<http://www.python.org/dev/faq/#how-do-i-get-a-checkout-of-the-repository-read-only-and-read-write>`_
をダウンロードすることができます。

ビルド手順は通常次のステップで構成されます。 ::

   ./configure
   make
   make install

configure のオプションと特定の Unix プラットフォームにおける注意点は
Python のソースツリーのルートにある :file:`README` の中に細かく記載されています。

.. warning::

   ``make install`` は :file:`python` バイナリを上書きまたは覆い隠すかもしれません。
   そのため、 ``make install`` の代わりに :file:`{exec_prefix}/bin/python{version}`
   しかインストールしない ``make altinstall`` が推奨されます。


Python に関係するパスとファイル
================================

これらはローカルインストール時の規約に応じて変化します;
:envvar:`prefix` (``${prefix}``) と :envvar:`exec_prefix` (``${exec_prefix}``) は
インストール状況に依存していて、GNU ソフトウェアによって解釈されます;
この二つは同じかもしれません。

例えば、ほとんどの Linux システムでは、デフォルトでは両方が :file:`/usr` です。

+-----------------------------------------------+------------------------------------------------+
| ファイル/ディレクトリ                         | 意味                                           |
+===============================================+================================================+
| :file:`{exec_prefix}/bin/python`              | インタプリタの推奨される場所                   |
+-----------------------------------------------+------------------------------------------------+
| :file:`{prefix}/lib/python{version}`,         | 標準モジュールを格納するディレクトリの、       |
| :file:`{exec_prefix}/lib/python{version}`     | 推奨される場所                                 |
+-----------------------------------------------+------------------------------------------------+
| :file:`{prefix}/include/python{version}`,     | Python 拡張や Python の埋込みに必要となる      |
| :file:`{exec_prefix}/include/python{version}` | include ファイルを格納するディレクトリの       |
|                                               | 推奨される場所                                 |
+-----------------------------------------------+------------------------------------------------+
| :file:`~/.pythonrc.py`                        | user モジュールによって読み込まれる、          |
|                                               | ごとの初期化ファイル。デフォルトでは、         |
|                                               | ほとんどのアプリケーションは利用しません。     |
+-----------------------------------------------+------------------------------------------------+


その他
=============

Python スクリプトを Unix で簡単に使うために、例えば次のようにして、
そのスクリプトを実行ファイルにし ::

   $ chmod +x script

そして適切な shebang 行をスクリプトの先頭に置きます。
たいていの場合良い方法は ::

   #!/usr/bin/env python

で、 :envvar:`PATH` 全体から Python インタプリタを探します。
しかし、幾つかの Unix は :program:`env` コマンドをもっていないので、
インタプリタのパスを ``/usr/bin/python`` のようにハードコードしなければ
ならないかもしれません。

シェルコマンドを Python スクリプトから使うには、 :mod:`subprocess`
モジュールを参照してください。


エディタ
=========

Vim と Emacs は Python をよくサポートした、素晴らしいエディタです。
これらのエディタで Python のコードを書く方法についての詳しい情報は、
次の場所を参照してください。

* http://www.vim.org/scripts/script.php?script_id=790
* http://sourceforge.net/projects/python-mode

Geany はたくさんの言語をサポートした素晴らしい IDE です。
さらなる情報は、 http://geany.uvena.de/ を読んでください。

Komodo edit も非常に良い IDE です。これもたくさんの言語をサポートしています。
さらなる情報は、
http://www.activestate.com/store/productdetail.aspx?prdGuid=20f4ed15-6684-4118-a78b-d37ff4058c5f
を読んでください。
