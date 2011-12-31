.. highlightlang:: c


.. _building:

****************************************************
distutils による C および C++ 拡張モジュールのビルド
****************************************************

.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>


Python 1.4 になってから、動的にリンクされるような拡張モジュールをビルドするためのメイクファイルを作成するような、特殊なメイクファイルをUnix
向けに提供するようになりました。Python 2.0 からはこの機構 (いわゆる Makefile.pre.in および Setup ファイルの関係ファイル)
はサポートされなくなりました。インタプリタ自体のカスタマイズはほとんど使われず、 distutils で拡張モジュールをビルドできるようになったからです。

distutils を使った拡張モジュールのビルドには、ビルドを行う計算機上に distutils をインストールしていることが必要です。 Python 2.x
には distutils が入っており、 Python 1.5 用には個別のパッケージがあります。distutils はバイナリパッケージの作成も
サポートしているので、ユーザが拡張モジュールをインストールする際に、必ずしもコンパイラが必要というわけではありません。

distutils ベースのパッケージには、駆動スクリプト (driver script) となる :file:`setup.py` が入っています。
:file:`setup.py` は普通の Python プログラムファイルで、ほとんどの場合以下のような見かけになっています::

   from distutils.core import setup, Extension

   module1 = Extension('demo',
                       sources = ['demo.c'])

   setup (name = 'PackageName',
          version = '1.0',
          description = 'This is a demo package',
          ext_modules = [module1])


この :file:`setup.py` とファイル :file:`demo.c` があるとき、以下のコマンド ::

   python setup.py build

を実行すると、 :file:`demo.c` をコンパイルして、 ``demo`` という名前の拡張モジュールを :file:`build`
ディレクトリ内に生成します。システムによってはモジュールファイルは :file:`build/lib.system`
サブディレクトリに生成され、 :file:`demo.so` や :file:`demo.pyd` といった名前になることがあります。

:file:`setup.py` 内では、コマンドの実行はすべて ``setup`` 関数を呼び出して行います。この関数は可変個のキーワード引数をとります。
例ではその一部を使っているにすぎません。もっと具体的にいうと、例の中ではパッケージをビルドするためのメタ情報と、パッケージの内容を指定しています。
通常、パッケージには Python ソースモジュールやドキュメント、サブパッケージ等といった別のファイルも入ります。 distutils
の機能に関する詳細は、 :ref:`distutils-index` に書かれている distutils
のドキュメントを参照してください;  この節では、拡張モジュールのビルドについてのみ説明します。

駆動スクリプトをよりよく構成するために、決め打ちの引数を :func:`setup` に入れておくことがよくあります。上の例では、 :func:`setup`
の ``ext_modules`` は拡張モジュールのリストで、リストの各々の要素は :class:`Extension`
クラスのインスタンスになっています。上の例では、 ``demo`` という名の拡張モジュールを定義していて、単一のソースファイル :file:`demo.c`
をコンパイルしてビルドするよう定義しています。

多くの場合、拡張モジュールのビルドはもっと複雑になります。というのは、プリプロセッサ定義やライブラリの追加指定が必要に
なることがあるからです。例えば以下のファイルがその実例です。 ::

   from distutils.core import setup, Extension

   module1 = Extension('demo',
                       define_macros = [('MAJOR_VERSION', '1'),
                                        ('MINOR_VERSION', '0')],
                       include_dirs = ['/usr/local/include'],
                       libraries = ['tcl83'],
                       library_dirs = ['/usr/local/lib'],
                       sources = ['demo.c'])

   setup (name = 'PackageName',
          version = '1.0',
          description = 'This is a demo package',
          author = 'Martin v. Loewis',
          author_email = 'martin@v.loewis.de',
          url = 'http://docs.python.org/extending/building',
          long_description = '''
   This is really just a demo package.
   ''',
          ext_modules = [module1])


この例では、 :func:`setup` は追加のメタ情報と共に呼び出されます。配布パッケージを構築する際には、メタ情報の追加が推奨されています。
拡張モジュール自体については、プリプロセッサ定義、インクルードファイルのディレクトリ、ライブラリのディレクトリ、ライブラリといった指定があります。
distutils はこの情報をコンパイラに応じて異なるやり方で引渡します。例えば、Unix では、上の設定は以下のようなコンパイルコマンドに
なるかもしれません::

   gcc -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 -DMINOR_VERSION=0 -I/usr/local/include -I/usr/local/include/python2.2 -c demo.c -o build/temp.linux-i686-2.2/demo.o

   gcc -shared build/temp.linux-i686-2.2/demo.o -L/usr/local/lib -ltcl83 -o build/lib.linux-i686-2.2/demo.so

これらのコマンドラインは実演目的で書かれたものです; distutils のユーザは distutils が正しくコマンドを実行すると信用してください。


.. _distributing:

拡張モジュールの配布
====================

拡張モジュールをうまくビルドできたら、三通りの使い方があります。

エンドユーザは普通モジュールをインストールしようと考えます; これには ::

   python setup.py install

を実行します。

モジュールメンテナはソースパッケージを作成します; これには ::

   python setup.py sdist

を実行します。

場合によっては、ソース配布物に追加のファイルを含める必要があります; これには :file:`MANIFEST.in` ファイルを使います; 詳しくは
distutils のドキュメントを参照してください。

ソースコード配布物をうまく構築できたら、メンテナはバイナリ配布物も作成できます。プラットフォームに応じて、以下のコマンドのいずれかを使います。 ::

   python setup.py bdist_wininst
   python setup.py bdist_rpm
   python setup.py bdist_dumb

