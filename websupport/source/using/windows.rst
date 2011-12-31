.. highlightlang:: none

.. _using-on-windows:

**************************
 Windows で Python を使う
**************************

.. sectionauthor:: Robert Lehmann <lehmannro@gmail.com>

このドキュメントは、 Python を Microsoft Windows で使うときに知っておくべき、
Windows 独特の動作についての概要を伝えることを目的としています。


Python のインストール
======================

ほとんどの Unix システムやサービスと異なり、 Windows は Python に依存しておらず、
プリインストールの Python はありません。
しかし、 CPython チームは長年にわたり、コンパイル済みの Windows インストーラ
(MSI パッケージ)を `リリース <http://www.python.org/download/releases/>`_
毎に用意しています。


Python の継続的な開発の中で、過去にサポートされていた幾つかのプラットフォームが
(ユーザーと開発者の不足のために) サポートされなくなっています。
全てのサポートされないプラットフォームについての詳細は :pep:`11` をチェックしてください。

* DOS と Windows 3.x は Python 2.0 から廃止予定になり、Python 2.1 でこれらのシステム
  専用のコードは削除されました。
* 2.5 まで、 Python は Windows 95, 98, ME で動きました (ですが、すでにインストール時に
  廃止予定の警告をだしていました)。 Python 2.6 (とその後の全てのリリース) は、
  これらの OS のサポートが止められ、新しいリリースは Windows NT ファミリーしか
  考慮されていません。
* `Windows CE <http://pythonce.sourceforge.net/>`_ は今でもサポートされています。
* `Cygwin <http://cygwin.com/>`_ インストーラも `Python インタープリタ
  <http://cygwin.com/packages/python>`_ のインストールを提供しています。
  これは "Interpreters" の下に置かれています。(cf. `Cygwin package source
  <ftp://ftp.uni-erlangen.de/pub/pc/gnuwin32/cygwin/mirrors/cygnus/
  release/python>`_, `Maintainer releases
  <http://www.tishler.net/jason/software/python/>`_)


コンパイル済みインストーラが提供されているプラットフォームについての詳細な情報は
`Python for Windows (and DOS) <http://www.python.org/download/windows/>`_
を参照してください。


.. seealso::

   `Python on XP <http://www.richarddooling.com/index.php/2006/03/14/python-on-xp-7-minutes-to-hello-world/>`_
      "7 Minutes to "Hello World!""
      by Richard Dooling, 2006

   `Installing on Windows <http://diveintopython.org/installing_python/windows.html>`_
      in "`Dive into Python: Python from novice to pro
      <http://diveintopython.org/index.html>`_"
      by Mark Pilgrim, 2004,
      ISBN 1-59059-356-1

   `For Windows users <http://swaroopch.com/text/Byte_of_Python:Installing_Python#For_Windows_users>`_
      in "Installing Python"
      in "`A Byte of Python <http://www.byteofpython.info>`_"
      by Swaroop C H, 2003


別のバンドル
===================

標準の CPython の配布物の他に、追加の機能を持っている修正されたパッケージがあります。
以下は人気のあるバージョンとそのキーとなる機能です。

`ActivePython <http://www.activestate.com/Products/activepython/>`_
    マルチプラットフォーム互換のインストーラー、ドキュメント、 PyWin32

`Enthought Python Distribution <http://www.enthought.com/products/epd.php>`_
    (PyWin32 などの) 人気のあるモジュールとそのドキュメント、 Python の
    拡張をビルドするためのツールスイート

これらのパッケージは *古い* バージョンの Python をインストールするかもしれないことに
気をつけてください。



Python を構成する
==================

Python を完全に動かすために、幾つかの環境設定を変更しなければならないかもしれません。


補足: 環境変数の設定
----------------------

Windows は環境変数を変更するためのビルトインのダイアログを持っています。
(以降のガイドは XP のクラシカルビューに適用されます。)
マシンのアイコン(たいていデスクトップにあって "マイ コンピュータ" と呼ばれます)
を右クリックして、そこにある :menuselection:`プロパティ` を選択します。
:guilabel:`詳細設定` タブを開いて、 :guilabel:`環境変数` ボタンをクリックします。

ここまでのパスをまとめると:

    :menuselection:`マイ コンピュータ
    --> プロパティ
    --> 詳細設定
    --> 環境変数`

このダイアログで、ユーザーとシステムの環境変数を追加したり修正できます。
システム変数を変更するには、マシンへの無制限アクセス(管理者権限)が必要です。

環境に変数を追加するもう一つの方法は、 :command:`set` コマンドを使うことです。 ::

    set PYTHONPATH=%PYTHONPATH%;C:\My_python_lib

この設定を永続化するために、このコマンドラインを :file:`autoexec.bat`
に追加することができます。 :program:`msconfig` はこのファイルを編集するGUIです。

もっと直接的な方法で環境変数を見ることができます。
コマンドプロンプトはパーセント記号で囲まれた文字列を自動的に展開します。 ::

    echo %PATH%

この動作についての詳細は :command:`set /?` を見てください。

.. seealso::

   http://support.microsoft.com/kb/100843
      Windows NT の環境変数

   http://support.microsoft.com/kb/310519
      Windows XP での環境変数の管理方法

   http://www.chem.gla.ac.uk/~louis/software/faq/q1.html
      Setting Environment variables, Louis J. Farrugia


Python 実行ファイルを見つける
-----------------------------

スタートメニューに自動的に作られた Python interpreter のメニューエントリを
使うのと別に、DOSプロンプトから Python を実行したいかもしれません。
そのためには、 :envvar:`%PATH%` 環境変数に Python ディストリビューションの
ディレクトリを、セミコロンで他のエントリと区切って含めるように設定する
必要があります。
変数の設定例は次のようになります (最初の2つのエントリが Windows のデフォルト
だと仮定します)::

    C:\WINDOWS\system32;C:\WINDOWS;C:\Python26

コマンドプロンプトから :command:`python` をタイプすると、 Python インタプリタを
起動します。これで、スクリプトをコマンドラインオプション付きで実行することも
可能です。 :ref:`using-on-cmdline` ドキュメントを参照してください。


モジュールの検索
------------------

Python は通常そのライブラリ(と site-packages フォルダ)をインストールした
ディレクトリに格納する。
なので、 Python を :file:`C:\\Python\\` ディレクトリにインストールしたとすると、
デフォルトのライブラリは :file:`C:\\Python\\Lib\\` に存在し、
サードパーティーのモジュールは :file:`C:\\Python\\Lib\\site-packages\\`
に格納されます。

.. `` エディタのシンタックスハイライトの問題回避用コメント

以下は、 Windows で :data:`sys.path` が構築される方法です。 

* 最初に空のエントリが追加されます。これはカレントディレクトリを指しています。

* その次に、 :envvar:`PYTHONPATH` 環境変数が存在するとき、 :ref:`using-on-envvars` で
  解説されているように追加されます。 Windows ではドライブ識別子 (``C:\`` など)と
  区別するために、この環境変数に含まれるパスの区切り文字はセミコロンでなければ
  ならない事に注意してください。

* 追加で "アプリケーションのパス" を ``HKEY_CURRENT_USER`` か ``HKEY_LOCAL_MACHINE``
  の中の :samp:`\\SOFTWARE\\Python\\PythonCore\\{version}\\PythonPath` の
  サブキーとして登録することができます。
  サブキーはデフォルト値としてセミコロンで区切られたパス文字列を持つことができ、
  書くパスが :data:`sys.path` に追加されます。
  (既存のインストーラーは全て HKLM しか利用しないので、 HKCU は通常空です)

* :envvar:`PYTHONHOME` が設定されている場合、それは "Python Home" として扱われます。
  それ以外の場合、 "Python Home" を推定するために Python の実行ファイルのパスから
  "目標ファイル" (``Lib\os.py``) が探されます。 Python home が見つかった場合、
  そこからいくつかのサブディレクトリ (``Lib``, ``plat-win``, など) が :data:`sys.path`
  に追加されます。見つからなかった場合、 core Python path はレジストリに登録された
  PythonPath から構築されます。

* Python Home が見つからず、環境変数 :envvar:`PYTHONPATH` が指定されず、
  レジストリエントリが見つからなかった場合、関連するデフォルトのパスが利用されます。
  (例: ``.\Lib;.\plat-win`` など)

結果としてこうなります:

* :file:`python.exe` かそれ以外の Python ディレクトリにある .exe ファイルを
  実行したとき (インストールされている場合でも PCbuild から直接実行されている場合でも)
  core path が利用され、レジストリ内の core path は無視されます。
  それ以外のレジストリの "application paths" は常に読み込まれます。

* Python が他の .exe ファイル (他のディレクトリに存在する場合や、COM経由で組み込まれる場合など)
  にホストされている場合は、 "Python Home" は推定されず、レジストリにある core path
  が利用されます。
  それ以外のレジストリの "application paths" は常に読み込まれます。

* Python が Python home ディレクトリを見つけられずレジストリも存在しない場合
  (例: freeze された .exe, いくつかのとても奇妙なインストール構成)、
  デフォルトの、ただし相対パスが利用されます。

追加のフォルダを Python の import 機構の検索対象に含めることもできます。
:envvar:`PYTHONPATH` を :ref:`using-on-envvars` で解説されているように利用し、
:data:`sys.path` を変更してください。
Windowsでは、 ドライブ識別子 (:file:`C:\\` など) と区別するために、パスはセミコロンで
区切られています。

.. ``

モジュール検索パスの変更は、レジストリの
:file:`HKLM\\SOFTWARE\\Python\\PythonCore\\{version}\\PythonPath` キーからも
可能です。
このキーのデフォルト値と同じように、セミコロンで区切られたパス文字列を持った
サブキーがあれば、その各パスを探します。複数のサブキーを作成することができ、
path に辞書順で追加されます。
便利なレジストリエディタは :program:`regedit` です。
(:menuselection:`スタート --> ファイル名を指定して実行` から "regedit"
とタイプすることで起動することができます。)


スクリプトを実行する
---------------------

Python スクリプト (``.py`` 拡張子を持ったファイル) はデフォルトで :program:`python.exe`
に起動されます。この実行ファイルは、プログラムがGUIを使う場合でもターミナルを開きます。
ターミナル無しでスクリプトを実行したい場合は、拡張子 ``.pyw`` を使うとそのスクリプトが
デフォルトでは :program:`pythonw.exe` で実行されるようになります。
(2つの実行ファイルは両方とも Python をインストールしたディレクトリの直下にあります。)
:program:`pythonw.exe` は起動時にターミナルを開きません。

You can also make all ``.py`` scripts execute with :program:`pythonw.exe`,
setting this through the usual facilities, for example (might require
administrative rights):
全ての ``.py`` スクリプトを :program:`pythonw.exe` で実行するように
設定することもできます。例えば (管理者権限が必要):

#. コマンドプロンプトを起動する
#. ``.py`` スクリプトに正しいファイルグループを関連付ける::

      assoc .py=Python.File

#. 全ての Python ファイルを新しい実行ファイルにリダイレクトする::

      ftype Python.File=C:\Path\to\pythonw.exe "%1" %*


Additional modules
追加のモジュール
=================

Python は全プラットフォーム互換を目指していますが、 Windows にしかない
ユニークな機能もあります。標準ライブラリと外部のライブラリの両方で、
幾つかのモジュールと、そういった機能を使うためのスニペットがあります。

Windows 専用の標準モジュールは、
:ref:`mswin-specific-services` に書かれています。


PyWin32
-------

The `PyWin32 <http://python.net/crew/mhammond/win32/>`_ module by Mark Hammond
is a collection of modules for advanced Windows-specific support.  This includes
utilities for:
Mark Hammond によって開発された `PyWin32 <http://python.net/crew/mhammond/win32/>`_
モジュールは、進んだ Windows 専用のサポートをするモジュール群です。
このモジュールは以下のユーティリティを含んでいます。

* `Component Object Model <http://www.microsoft.com/com/>`_ (COM)
* Win32 API 呼び出し
* レジストリ
* イベントログ
* `Microsoft Foundation Classes <http://msdn.microsoft.com/en-us/library/fe1cf721%28VS.80%29.aspx>`_ (MFC)
  ユーザーインターフェイス

`PythonWin <http://web.archive.org/web/20060524042422/
http://www.python.org/windows/pythonwin/>`_ は PyWin32 に付属している、
サンプルのMFCアプリケーションです。
これはビルトインのデバッガを含む、組み込み可能なIDEです。

.. seealso::

   `Win32 How Do I...? <http://timgolden.me.uk/python/win32_how_do_i.html>`_
      by Tim Golden

   `Python and COM <http://www.boddie.org.uk/python/COM.html>`_
      by David and Paul Boddie


Py2exe
------

`Py2exe <http://www.py2exe.org/>`_ は :mod:`distutils` 拡張 (:ref:`extending-distutils`
を参照) で、 Python スクリプトを Windows 実行可能プログラム (:file:`{*}.exe` ファイル)
にラップします。
これを使えば、ユーザーに Python のインストールをさせなくても、
アプリケーションを配布することができます。

WConio
------

Python の進んだターミナル制御レイヤである :mod:`curses` は、 Unix ライクシステムでしか
使うことができません。逆に Windows 専用のライブラリ、 Windows Console I/O for Python
があります。

`WConio <http://newcenturycomputers.net/projects/wconio.html>`_ は
Turbo-C の :file:`CONIO.H` のラッパーで、テキストユーザーインタフェースを
作成するために利用することができます。


Windows 上で Python をコンパイルする
=====================================

CPython を自分でコンパイルしたい場合、最初にすることは
`ソース <http://python.org/download/source/>`_ を取得することです。
最新版リリースのソースをダウンロードするか、最新の `チェックアウト
<http://www.python.org/dev/faq/#how-do-i-get-a-checkout-of-the-repository-read-only-and-read-write>`_
を取得することができます。

公式の Python リリースをビルドするのに使われている Microsoft Visual C++ コンパイラのために、
ソースツリーは ソリューション・プロジェクトファイルを含んでいます。
適切なディレクトリにある :file:`readme.txt` を参照してください。

+--------------------+-----------------+--------------------------+
| ディレクトリ       | MSVC バージョン | Visual Studio バージョン |
+====================+=================+==========================+
| :file:`PC/VC6/`    | 6.0             | 97                       |
+--------------------+-----------------+--------------------------+
| :file:`PC/VS7.1/`  | 7.1             | 2003                     |
+--------------------+-----------------+--------------------------+
| :file:`PC/VS8.0/`  | 8.0             | 2005                     |
+--------------------+-----------------+--------------------------+
| :file:`PCbuild/`   | 9.0             | 2008                     |
+--------------------+-----------------+--------------------------+

これらのビルドディレクトリの全てが完全にサポートされているわけではありません。
使用しているバージョンの公式リリースが利用しているコンパイラのバージョンについては、
リリースノートを参照してください。

ビルドプロセスに関する一般的な情報は :file:`PC/readme.txt` をチェックしてください。


拡張モジュールについては、 :ref:`building-on-windows` を参照してください。

.. seealso::

   `Python + Windows + distutils + SWIG + gcc MinGW <http://sebsauvage.net/python/mingw.html>`_
      or "Creating Python extensions in C/C++ with SWIG and compiling them with
      MinGW gcc under Windows" or "Installing Python extension with distutils
      and without Microsoft Visual C++" by Sébastien Sauvage, 2003

   `MingW -- Python extensions <http://oldwiki.mingw.org/index.php/Python%20extensions>`_
      by Trent Apted et al, 2007


その他のリソース
=================

.. seealso::

   `Python Programming On Win32 <http://www.oreilly.com/catalog/pythonwin32/>`_
      "Help for Windows Programmers"
      by Mark Hammond and Andy Robinson, O'Reilly Media, 2000,
      ISBN 1-56592-621-8

   `A Python for Windows Tutorial <http://www.imladris.com/Scripts/PythonForWindows.html>`_
      by Amanda Birmingham, 2004

