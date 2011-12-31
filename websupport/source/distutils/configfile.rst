.. _setup-config:

****************************************************
setup 設定ファイル (setup configuration file) を書く
****************************************************

時に、配布物をビルドする際に必要な全ての設定を *あらかじめ* 書ききれない状況が起きます: 例えば、ビルドを進めるために、ユーザに関する
情報や、ユーザのシステムに関する情報を必要とするかもしれません。こうした情報が単純 --- C ヘッダファイルやライブラリを検索する
ディレクトリのリストのように --- であるかぎり、ユーザに設定ファイル (configuration file) :file:`setup.cfg`
を提供して編集してもらうのが、安上がりで簡単な特定方法になります。設定ファイルはまた、あらゆるコマンドにおけるオプションにデフォルト値
を与えておき、インストール作業者がコマンドライン上や設定ファイルの編集でデフォルト設定を上書きできるようにします。

setup 設定ファイルは setup スクリプト ---理想的にはインストール作業者から見えないもの  [#]_
---と、作者の手を離れて、全てインストール作業者次第となる setup スクリプトのコマンドライン引数との間を橋渡しする中間層として有効です。
実際、 :file:`setup.cfg` (と、ターゲットシステム上にある、その他の Distutils 設定ファイル) は、 setup
スクリプトの内容より後で、かつコマンドラインで上書きする前に処理されます。この仕様の結果、いくつかの利点が生まれます:

.. % (If you have more advanced needs, such as determining which extensions
.. % to build based on what capabilities are present on the target system,
.. % then you need the Distutils ``auto-configuration'' facility.  This
.. % started to appear in Distutils 0.9 but, as of this writing, isn't mature
.. % or stable enough yet for real-world use.)

* インストール作業者は、作者が :file:`setup.py` に設定した項目のいくつかを :file:`setup.cfg` を変更して上書きできます。

* :file:`setu.py` では簡単に設定できないような、標準でないオプションのデフォルト値を設定できます。

* インストール作業者は、 :file:`setup.cfg` に書かれたどんな設定も :file:`setup.py`
  のコマンドラインオプションで上書きできます。

設定ファイルの基本的な構文は簡単なものです::

   [command]
   option=value
   ...

ここで、 *command* は Distutils コマンドのうちの一つ (例えば :command:`build_py`,
:command:`install`) で、 *option*  はそのコマンドでサポートされているオプションのうちの一つです。
各コマンドには任意の数のオプションを設定でき、一つの設定ファイル中には任意の数のコマンドセクションを収められます。空白行は無視されます、 ``'#'``
文字で開始して行末まで続くコメントも同様に無視されます。長いオプション設定値は、継続行をインデントするだけで複数行にわたって記述できます。

あるコマンドがサポートしているオプションのリストは、 :option:`--help` オプションで調べられます。例えば以下のように。 ::

   > python setup.py --help build_ext
   [...]
   Options for 'build_ext' command:
     --build-lib (-b)     directory for compiled extension modules
     --build-temp (-t)    directory for temporary files (build by-products)
     --inplace (-i)       ignore build-lib and put compiled extensions into the
                          source directory alongside your pure Python modules
     --include-dirs (-I)  list of directories to search for header files
     --define (-D)        C preprocessor macros to define
     --undef (-U)         C preprocessor macros to undefine
     --swig-opts          list of SWIG command line options
   [...]

コマンドライン上で :option:`--foo-bar` と綴るオプションは、設定ファイル上では :option:`foo_bar`
と綴るので注意してください。

例えば、拡張モジュールを "インプレース (in-place)" でビルドしたいとします --- すなわち、 :mod:`pkg.ext`
という拡張モジュールを持っていて、コンパイル済みの拡張モジュールファイル (例えば Unix では :file:`ext.so`) を pure Python
モジュール :mod:`pkg.mod1` および :mod:`pkg.mod2` と同じソースディレクトリに置きたいとします。
こんなときには、 :option:`--inplace` を使えば、確実にビルドを行えます。 ::

   python setup.py build_ext --inplace

しかし、この操作では、常に :command:`build_ext` を明示的に指定しなければならず、 :option:`--inplace`
オプションを忘れずに与えなければなりません。こうした設定を "設定しっ放しにする" 簡単な方法は、 :file:`setup.cfg`
に書いておくやり方で、設定ファイルは以下のようになります::

   [build_ext]
   inplace=1

この設定は、明示的に :command:`build_ext` を指定するかどうかに関わらず、モジュール配布物の全てのビルドに影響します。ソース配布物に
:file:`setup.cfg` を含めると、エンドユーザの手で行われるビルドにも影響します --- このオプションの例に関しては
:file:`setup.cfg` を含めるのはおそらくよくないアイデアでしょう。というのは、拡張モジュールをインプレースでビルドすると常に
インストールしたモジュール配布物を壊してしまうからです。とはいえ、ある特定の状況では、モジュールをインストールディレクトリ
の下に正しく構築できるので、機能としては有用だと考えられます。 (ただ、インストールディレクトリ上でのビルドを想定するような
拡張モジュールの配布は、ほとんどの場合よくない考え方です。)

もう一つ、例があります: コマンドによっては、実行時にほとんど変更されないたくさんのオプションがあります; 例えば、 :command:`bdist_rpm`
には、RPM 配布物を作成する際に、"spec"  ファイルを作成するために必要な情報を全て与えなければなりません。この情報には setup
スクリプトから与えるものもあり、 (インストールされるファイルのリストのように) Distutils が自動的に
生成するものもあります。しかし、こうした情報の中には :command:`bdist_rpm` のオプションとして与えるものがあり、
毎回実行するごとにコマンドライン上で指定するのが面倒です。そこで、以下のような内容が Distutils 自体の :file:`setup.cfg`
には入っています::

   [bdist_rpm]
   release = 1
   packager = Greg Ward <gward@python.net>
   doc_files = CHANGES.txt
               README.txt
               USAGE.txt
               doc/
               examples/

:option:`doc_files` オプションは、単に空白で区切られた文字列で、ここでは可読性のために複数行をまたぐようにしています。


.. seealso::

   "Python モジュールのインストール" の :ref:`inst-config-syntax`
      設定ファイルに関する詳細情報は、システム管理者向けのこのマニュアルにあります。


.. rubric:: 注記

.. [#] Distutils が自動設定機能 (auto-configuration) をサポートするまで、おそらくこの理想状態を達成することはないでしょう

