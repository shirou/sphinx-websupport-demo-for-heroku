
.. _using-on-mac:

***************************
Macintosh で Python を使う
***************************

:Author: Bob Savage <bobsavage@mac.com>


Mac OS X が動作している Macintosh 上の Python は原則的には他の Unix プラットフォーム上の Python と非常によく似ていますが、 IDE やパッケージ・マネージャなどの指摘すべき追加要素があります。

.. Python on a Macintosh running Mac OS X is in principle very similar to Python on
.. any other Unix platform, but there are a number of additional features such as
.. the IDE and the Package Manager that are worth pointing out.

Mac 特有のモジュールについては :ref:`mac-specific-services` に書かれています。

.. The Mac-specific modules are documented in :ref:`mac-specific-services`.

Mac OS 9 もしくはそれ以前の Mac 上の Python は Unix や Windows 上の Python とは大きく掛け離れていますが、そのプラットフォームは既にサポートされておらずこのマニュアルで扱う範囲を越えているので、Python 2.4 以降を扱うことにします。
Mac OS 9 用の最新のバージョン 2.3 リリースのインストーラやそのドキュメントについては http://www.cwi.nl/~jack/macpython を参照してください。

.. Python on Mac OS 9 or earlier can be quite different from Python on Unix or
.. Windows, but is beyond the scope of this manual, as that platform is no longer
.. supported, starting with Python 2.4. See http://www.cwi.nl/~jack/macpython for
.. installers for the latest 2.3 release for Mac OS 9 and related documentation.


.. _getting-osx:

MacPython の入手とインストール
==============================

Mac OS X 10.5 には Apple によって Python 2.5.1 がプリインストールされています。
Python の Web サイト (http://www.python.org) から最新バージョンの Python を取得しインストールすることもできます。新しい Intel の CPU でも古い PPC の CPU でもネイティブに動作する "ユニバーサル・バイナリ" ビルドの最新のものがあります。

.. Mac OS X 10.5 comes with Python 2.5.1 pre-installed by Apple.  If you wish, you
.. are invited to install the most recent version of Python from the Python website
.. (http://www.python.org).  A current "universal binary" build of Python, which
.. runs natively on the Mac's new Intel and legacy PPC CPU's, is available there.

インストールを行うといくつかのものが手に入ります:

.. What you get after installing is a number of things:

* :file:`Applications` フォルダにある :file:`MacPython 2.5` フォルダ.
  公式の Python ディストリビューションに含まれる開発環境 IDLE;
  Finder から Python スクリプトをダブルクリックしたときに起動する PythonLauncher;
  Python スクリプトを単独のアプリケーションに変換する "Build Applet" ツールがここにあります.

.. * A :file:`MacPython 2.5` folder in your :file:`Applications` folder. In here
..   you find IDLE, the development environment that is a standard part of official
..   Python distributions; PythonLauncher, which handles double-clicking Python
..   scripts from the Finder; and the "Build Applet" tool, which allows you to
..   package Python scripts as standalone applications on your system.

* Python 実行ファイルやライブラリを含む :file:`/Library/Frameworks/Python.framework` フレームワーク。
  インストーラはシェルのパスにこの場所を追加します。 MacPython をアンインストールするには、これら 3 つを削除すればよいだけです。
  Python 実行ファイルへのシンボリックリンクは /usr/local/bin/ に置かれています。

.. * A framework :file:`/Library/Frameworks/Python.framework`, which includes the
..   Python executable and libraries. The installer adds this location to your shell
..   path. To uninstall MacPython, you can simply remove these three things. A
..   symlink to the Python executable is placed in /usr/local/bin/.

Apple が提供している Python は :file:`/System/Library/Frameworks/Python.framework` と :file:`/usr/bin/python` にそれぞれインストールされています。
これらは Apple が管理しているものであり Apple やサードパーティのソフトウェアが使用するので、編集したり削除してはいけません。
python.org から新しいバージョンの Python をインストールすることにした場合には、異なるが動作する 2 つの Python 環境があなたのコンピュータにあることに注意し、パスの設定や Python の使い方と実際にしたいこととが食い違っていないことが重要です。

.. The Apple-provided build of Python is installed in
.. :file:`/System/Library/Frameworks/Python.framework` and :file:`/usr/bin/python`,
.. respectively. You should never modify or delete these, as they are
.. Apple-controlled and are used by Apple- or third-party software.  Remember that
.. if you choose to install a newer Python version from python.org, you will have
.. two different but functional Python installations on your computer, so it will
.. be important that your paths and usages are consistent with what you want to do.

IDLE にはヘルプメニューがあり Python のドキュメントにアクセスすることができます。
もし Python が全くの初めての場合にはドキュメントのチュートリアルを最初から読み進めることをおすすめします。

.. IDLE includes a help menu that allows you to access Python documentation. If you
.. are completely new to Python you should start reading the tutorial introduction
.. in that document.

もし他の Unix プラットフォーム上の Python に慣れている場合は Unix シェルからの Python スクリプトの実行についての節を読むことをおすすめします。

.. If you are familiar with Python on other Unix platforms you should read the
.. section on running Python scripts from the Unix shell.


Python スクリプトの実行方法
----------------------------

Mac OS X で Python を始める最良の方法は統合開発環境である IDLE を使うことです、 :ref:`ide` 節を参照し IDE を実行しているときにヘルプメニューを使ってください。

.. Your best way to get started with Python on Mac OS X is through the IDLE
.. integrated development environment, see section :ref:`ide` and use the Help menu
.. when the IDE is running.

もし Python スクリプトをターミナルのコマンドラインや Finder から実行したい場合は最初にエディタでスクリプトを作る必要があります。
Mac OS X には :program:`vim` や :program:`emacs` などの Unix の標準のラインエディタが備わっています。
もしもっと Mac らしいエディタが欲しい場合には、Bare Bones Software (http://www.barebones.com/products/bbedit/index.shtml を参照) の :program:`BBEdit` や :program:`TextWrangler` もしくは :program:`TextMate` (see http://macromates.com/) は良い選択候補です。
他には :program:`Gvim` (http://macvim.org) や :program:`Aquamacs` (http://aquamacs.org/) などがあります。

.. If you want to run Python scripts from the Terminal window command line or from
.. the Finder you first need an editor to create your script. Mac OS X comes with a
.. number of standard Unix command line editors, :program:`vim` and
.. :program:`emacs` among them. If you want a more Mac-like editor,
.. :program:`BBEdit` or :program:`TextWrangler` from Bare Bones Software (see
.. http://www.barebones.com/products/bbedit/index.shtml) are good choices, as is
.. :program:`TextMate` (see http://macromates.com/). Other editors include
.. :program:`Gvim` (http://macvim.org) and :program:`Aquamacs`
.. (http://aquamacs.org/).

ターミナルからスクリプトを実行するには :file:`/usr/local/bin` がシェルのパスに含まれていることを確認してください。

.. To run your script from the Terminal window you must make sure that
.. :file:`/usr/local/bin` is in your shell search path.

Finder からスクリプトを実行するのには 2 つの方法があります:

.. To run your script from the Finder you have two options:

* :program:`PythonLauncher` へドラッグする

.. * Drag it to :program:`PythonLauncher`

* Finder の情報ウィンドウから :program:`PythonLauncher` をそのスクリプト (もしくは .py スクリプト全て) を開くデフォルトのアプリケーションとして選び、スクリプトファイルをダブルクリックしてください。
  :program:`PythonLauncher` の環境設定にはどのようにスクリプトを実行するかを管理する様々な設定があります。
  option キーを押しながらドラッグすることで実行するごとにこれらの設定を変えられますし、環境設定メニューから全ての実行に対して設定変更することもできます。

.. * Select :program:`PythonLauncher` as the default application to open your
..   script (or any .py script) through the finder Info window and double-click it.
..   :program:`PythonLauncher` has various preferences to control how your script is
..   launched. Option-dragging allows you to change these for one invocation, or use
..   its Preferences menu to change things globally.


.. _osx-gui-scripts:

GUI でスクリプトを実行
--------------------------

古いバージョンの Python について、気を付けておくべき Mac OS X の癖があります: Aqua ウィンドウマネージャとやりとりをする (別の言い方をすると GUI を持つ) プログラムは特別な方法で実行する必要があります。
そのようなスクリプトを実行するには :program:`python` ではな :program:`pythonw` を使ってください。

.. With older versions of Python, there is one Mac OS X quirk that you need to be
.. aware of: programs that talk to the Aqua window manager (in other words,
.. anything that has a GUI) need to be run in a special way. Use :program:`pythonw`
.. instead of :program:`python` to start such scripts.

Python 2.5 では、 :program:`python` も :program:`pythonw` も使えます。

.. With Python 2.5, you can use either :program:`python` or :program:`pythonw`.


Configuration
-------------

OS X 上の Python では :envvar:`PYTHONPATH` のような全ての標準の Unix 環境変数が使えますが、Finder からプログラムを起動する場合このような環境変数を設定する方法は非標準であり Finder は起動時に :file:`.profile` や :file:`.cshrc` を読み込みません。
:file:`~/.MacOSX/environment.plist` ファイルを作る必要があります。
詳細については Apple の Technical Document QA1067 を参照してください。

.. Python on OS X honors all standard Unix environment variables such as
.. :envvar:`PYTHONPATH`, but setting these variables for programs started from the
.. Finder is non-standard as the Finder does not read your :file:`.profile` or
.. :file:`.cshrc` at startup. You need to create a file :file:`~
.. /.MacOSX/environment.plist`. See Apple's Technical Document QA1067 for details.

MacPython の Python パッケージのインストールについてのさらなる情報は、 :ref:`mac-package-manager` 節を参照してください。

.. For more information on installation Python packages in MacPython, see section
.. :ref:`mac-package-manager`.


.. _ide:

IDE
=======

MacPython には標準の IDLE 開発環境が付いてきます。
http://hkn.eecs.berkeley.edu/~dyoo/python/idle_intro/index.html
に IDLE を使うための良い入門があります。


.. _mac-package-manager:

追加の Python パッケージのインストール
=======================================

追加の Python パッケージをインストールする方法がいくつかあります:

.. There are several methods to install additional Python packages:

* http://pythonmac.org/packages/ には Python 2.5、2.4、2.3 用のコンパイルされたパッケージがあります。

.. * http://pythonmac.org/packages/ contains selected compiled packages for Python
..   2.5, 2.4, and 2.3.

* パッケージは Python の標準の distutils モードを使ってインストールすることができます (``python setup.py install``)。

.. * Packages can be installed via the standard Python distutils mode (``python
..   setup.py install``).

* 多くのパッケージは :program:`setuptools` 拡張を使ってもインストールできます。

.. * Many packages can also be installed via the :program:`setuptools` extension.


Mac での GUI プログラミング
============================

Python で Mac 上の GUI アプリケーションをビルドする方法がいくつかあります。

.. There are several options for building GUI applications on the Mac with Python.

*PyObjC* は Mac の最新の開発基盤である Apple の Objective-C/Cocoa フレームワークへの Python バインディングです。
PyObjC の情報は http://pyobjc.sourceforge.net にあります。

.. *PyObjC* is a Python binding to Apple's Objective-C/Cocoa framework, which is
.. the foundation of most modern Mac development. Information on PyObjC is
.. available from http://pyobjc.sourceforge.net.

標準の Python の GUI ツールキットは :mod:`Tkinter` で、クロスプラットフォームの Tk ツールキット (http://www.tcl.tk) をベースにしています。
Aqua ネイティブ版の Tk は OS X に入っており、最新バージョンが http://www.activestate.com からダウンロードおよびインストールできます; またソースからビルドすることもできます。

.. The standard Python GUI toolkit is :mod:`Tkinter`, based on the cross-platform
.. Tk toolkit (http://www.tcl.tk). An Aqua-native version of Tk is bundled with OS
.. X by Apple, and the latest version can be downloaded and installed from
.. http://www.activestate.com; it can also be built from source.

*wxPython* は別の人気のあるクロスプラットフォームの GUI ツールキットで Mac OS X 上でネイティブに動作します。
パッケージとドキュメントは http://www.wxpython.org から利用できます。

.. *wxPython* is another popular cross-platform GUI toolkit that runs natively on
.. Mac OS X. Packages and documentation are available from http://www.wxpython.org.

*PyQt* は別の人気のあるクロスプラットフォームの GUI ツールキットで Mac OS X 上でネイティブに動作します。
さらなる情報は http://www.riverbankcomputing.co.uk/software/pyqt/intro にあります。

.. *PyQt* is another popular cross-platform GUI toolkit that runs natively on Mac
.. OS X. More information can be found at
.. http://www.riverbankcomputing.co.uk/software/pyqt/intro.


Mac 上の Python アプリケーションの配布
===========================================

フォルダ MacPython 2.5 にある "Built Applet" ツールはあなたのマシンの小さな Python スクリプトを標準の Mac アプリケーションとして実行できるようなパッケージを作るのに優れています。
しかし、このツールは Python アプリケーションを他のユーザに配布するのには向いていません。

.. The "Build Applet" tool that is placed in the MacPython 2.5 folder is fine for
.. packaging small Python scripts on your own machine to run as a standard Mac
.. application. This tool, however, is not robust enough to distribute Python
.. applications to other users.

Mac 上の単独の Python アプリケーションをデプロイする標準のツールは :program:`py2app` です。
py2app のインストールと使用法に関する情報は http://undefined.org/python/#py2app にあります。

.. The standard tool for deploying standalone Python applications on the Mac is
.. :program:`py2app`. More information on installing and using py2app can be found
.. at http://undefined.org/python/#py2app.


アプリケーションスクリプティング
================================

Python は Apple の Open Scripting Architecture (OSA) を通して他の Mac アプリケーションのスクリプトとしても使えます; http://appscript.sourceforge.net を参照してください。
Appscript は高水準でユーザに優しい Apple event ブリッジで普通の Python スクリプトを使って Mac OS X アプリケーションを操作することができます。
Appscript は Mac の自動操作を行うための Apple 自身による言語 *AppleScript* の代わりとして本格的に使えます。
それに関連するパッケージ *PyOSA* は Python のための OSA 言語コンポーネントで、それを使うことで Python のコードをどんな OSA 対応のアプリケーション (Script Editor、Mail、 iTunes など) からも実行できます。
PyOSA によって Python は完全な AppleScript との通信端末になります。

.. Python can also be used to script other Mac applications via Apple's Open
.. Scripting Architecture (OSA); see http://appscript.sourceforge.net. Appscript is
.. a high-level, user-friendly Apple event bridge that allows you to control
.. scriptable Mac OS X applications using ordinary Python scripts. Appscript makes
.. Python a serious alternative to Apple's own *AppleScript* language for
.. automating your Mac. A related package, *PyOSA*, is an OSA language component
.. for the Python scripting language, allowing Python code to be executed by any
.. OSA-enabled application (Script Editor, Mail, iTunes, etc.). PyOSA makes Python
.. a full peer to AppleScript.


他のリソース
============

MacPython メーリングリストは Mac での Python ユーザや開発者にとって素晴しいサポートリソースです:

.. The MacPython mailing list is an excellent support resource for Python users and
.. developers on the Mac:

http://www.python.org/community/sigs/current/pythonmac-sig/

他の役に立つリソースは MacPython wiki です:

.. Another useful resource is the MacPython wiki:

http://wiki.python.org/moin/MacPython

