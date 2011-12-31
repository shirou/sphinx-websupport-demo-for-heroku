.. _examples:

**
例
**

この章は distutils を使い始めるのに役立つ幾つかの基本的な例を提供します。
distutils を使うための追加の情報は Distutils Cookbook で見つけることができます。

.. seealso::

   `Distutils Cookbook <http://wiki.python.org/moin/Distutils/Cookbook>`_
      distutils をもっと制御するためのレシピ集

.. _pure-mod:

pure Python 配布物 (モジュール形式)
===================================

単に二つのモジュール、特定のパッケージに属しないモジュールを配布するだけなら、setup スクリプト中で :option:`py_modules`
オプションを使って個別に指定できます。

もっとも単純なケースでは、二つのファイル: setup スクリプト自体と、配布したい単一のモジュール、この例では :file:`foo.py` について
考えなければなりません::

   <root>/
           setup.py
           foo.py

(この節の全ての図において、 *<root>* は配布物ルートディレクトリを参照します。) この状況を扱うための最小の setup スクリプトは
以下のようになります::

   from distutils.core import setup
   setup(name='foo',
         version='1.0',
         py_modules=['foo'],
         )

配布物の名前は :option:`name` オプションで個々に指定し、配布されるモジュールの一つと配布物を同じ名前にする必要はないことに注意してください
(とはいえ、この命名方法はよいならわしでしょう)。ただし、配布物名はファイル名を作成するときに使われるので、
文字、数字、アンダースコア、ハイフンだけで構成しなければなりません。

:option:`py_modules` はリストなので、もちろん複数のモジュールを指定できます。例えば、モジュール :mod:`foo` と
:mod:`bar` を配布しようとしているのなら、 setup スクリプトは以下のようになります::

   <root>/
           setup.py
           foo.py
           bar.py

また、セットアップスクリプトは以下のようになります． ::

   from distutils.core import setup
   setup(name='foobar',
         version='1.0',
         py_modules=['foo', 'bar'],
         )

モジュールのソースファイルは他のディレクトリに置けますが、そうしなければならないようなモジュールを沢山持っているのなら、
モジュールを個別に列挙するよりもパッケージを指定した方が簡単でしょう。


.. _pure-pkg:

pure Python 配布物 (パッケージ形式)
===================================

二つ以上のモジュールを配布する場合、とりわけ二つのパッケージに分かれている場合、おそらく個々のモジュールよりもパッケージ全体を
指定する方が簡単です。たとえモジュールがパッケージ内に入っていなくても状況は同じで、その場合はルートパッケージにモジュールが入っていると Distutils
に教えることができ、他のパッケージと同様にうまく処理されます (ただし、 :file:`__init__.py` があってはなりません)。

最後の例で挙げた setup スクリプトは、  ::

   from distutils.core import setup
   setup(name='foobar',
         version='1.0',
         packages=[''],
         )

のようにも書けます (空文字はルートパッケージを意味します)

これら二つのファイルをサブディレクトリ下に移動しておいて、インストール先はルートパッケージのままにしておきたい、例えば::

   <root>/
           setup.py
           src/      foo.py
                     bar.py

のような場合には、パッケージ名にはルートパッケージをそのまま指定しておきますが、ルートパッケージに置くソースファイルがどこにあるかを Distutils
に教えなければなりません:

.. %

::

   from distutils.core import setup
   setup(name='foobar',
         version='1.0',
         package_dir={'': 'src'},
         packages=[''],
         )

もっと典型的なケースでは、複数のモジュールを同じパッケージ  (またはサブパッケージ) に入れて配布しようと思うでしょう。例えば、 :mod:`foo` と
:mod:`bar` モジュールがパッケージ :mod:`foobar` に属する場合、ソースツリーをレイアウトする一案として、以下が考えられます。 ::

   <root>/
           setup.py
           foobar/
                    __init__.py
                    foo.py
                    bar.py

実際、 Distutils ではこれをデフォルトのレイアウトとして想定していて、setup スクリプトを書く際にも最小限の作業しか必要ありません::

   from distutils.core import setup
   setup(name='foobar',
         version='1.0',
         packages=['foobar'],
         )

モジュールを入れるディレクトリをパッケージの名前にしたくない場合、ここでも :option:`package_dir` オプションを使う必要があります。
例えば、パッケージ :mod:`foobar` のモジュールが :file:`src` に入っているとします::

   <root>/
           setup.py
           src/
                    __init__.py
                    foo.py
                    bar.py

適切な setup スクリプトは、 ::

   from distutils.core import setup
   setup(name='foobar',
         version='1.0',
         package_dir={'foobar': 'src'},
         packages=['foobar'],
         )

のようになるでしょう。

.. %

また、メインパッケージ内のモジュールを配布物ルート下に置くことがあるかもしれません::

   <root>/
           setup.py
           __init__.py
           foo.py
           bar.py

この場合、 setup スクリプトは ::

   from distutils.core import setup
   setup(name='foobar',
         version='1.0',
         package_dir={'foobar': ''},
         packages=['foobar'],
         )

のようになるでしょう。 (空文字列も現在のディレクトリを表します。)

.. %

サブパッケージがある場合、 :option:`packages` で明示的に列挙しなければなりませんが、 :option:`package_dir`
はサブパッケージへのパスを自動的に展開します。 (別の言い方をすれば、 Distutils はソースツリーを *走査せず* 、どのディレクトリが Python
パッケージに相当するのかを :file:`__init__.py` files. を探して調べようとします。)
このようにして、デフォルトのレイアウトはサブパッケージ形式に展開されます::

   <root>/
           setup.py
           foobar/
                    __init__.py
                    foo.py
                    bar.py
                    subfoo/
                              __init__.py
                              blah.py

対応する setup スクリプトは以下のようになります。 ::

   from distutils.core import setup
   setup(name='foobar',
         version='1.0',
         packages=['foobar', 'foobar.subfoo'],
         )

(ここでも、 :option:`package_dir` を空文字列にすると現在のディレクトリを表します。)


.. _single-ext:

単体の拡張モジュール
====================

拡張モジュールは、 :option:`ext_modules` オプションを使って指定します。 :option:`package_dir`
は、拡張モジュールのソースファイルをどこで探すかには影響しません; pure Python モジュールのソースのみに影響します。
もっとも単純なケースでは、単一の C ソースファイルで書かれた単一の拡張モジュールは::

   <root>/
           setup.py
           foo.c

になります。

.. %

:mod:`foo` 拡張をルートパッケージ下に所属させたい場合、 setup  スクリプトは ::

   from distutils.core import setup
   from distutils.extension import Extension
   setup(name='foobar',
         version='1.0',
         ext_modules=[Extension('foo', ['foo.c'])],
         )

になります。

.. %

同じソースツリーレイアウトで、この拡張モジュールを :mod:`foopkg` の下に置き、拡張モジュールの名前を変えるには::

   from distutils.core import setup
   from distutils.extension import Extension
   setup(name='foobar',
         version = '1.0',
         ext_modules=[Extension('foopkg.foo', ['foo.c'])],
         )

のようにします。

.. %

.. % \section{Multiple extension modules}
.. % \label{multiple-ext}

.. % \section{Putting it all together}


