:tocdepth: 2

.. _windows-faq:

=======================
Windows 上の Python FAQ
=======================

.. contents::

Python プログラムを Windows で動かすにはどうしますか？
------------------------------------------------------

これは単純な問題ではないかもしれません。あなたがすでに
Windows コマンドラインからプログラムを作動させることに慣れているなら、
すぐに全て分かりますが、そうでなければ少し案内が必要です。Windows 95、98、NT、
ME、2000、XP の間にも差があり、混乱のもとになっています。

.. sidebar:: |Python Development on XP|_
   :subtitle: `Python Development on XP`_

   このスクリーンキャストのシリーズは、あなたが Windows XP で Python を
   扱えるようにすることを目標としています。知識は 90 分に凝縮され、
   あなたが正しい Python ディストリビューションを、あなたが選んだ IDE で
   コーディングし、ユニットテストでデバッグをして堅実なコードを
   書いていけるようにします。

.. |Python Development on XP| image:: python-video-icon.png
.. _`Python Development on XP`:
   http://www.showmedo.com/videos/series?name=pythonOzsvaldPyNewbieSeries

あなたがある種の統合開発環境を使っているのでない限り、結局は Windows コマンドを
"DOS ウィンドウ" や "コマンドプロンプトウィンドウ" と様々に呼ばれるものに
*タイプする* ことになります。通常、このようなウィンドウはスタートメニューから
出すことができます。Windows 2000 では選ぶメニューは :menuselection:`Start -->
Programs --> Accessories --> Command Prompt` です。そのようなウィンドウが
開いたことは、通常このような Windows "コマンドプロンプト" が見られることから
わかるでしょう::

   C:\>

この文字は異なっていたり、続きがあったりするので、コンピュータの設定や、
あなたが最近何をしたかに依って、このようになっていることもあるでしょう::

   D:\Steve\Projects\Python>

このようなウィンドウさえ開けば、Python プログラムを動かす手順は順調に進みます。

前提として、Python スクリプトは、Python インタプリタという別のプログラムに
よって加工されなければなりません。インタプリタはスクリプトを読み込み、
バイトコードにコンパイルし、そのバイトコードを実行してプログラムを動かします。
では、インタプリタに Python を扱わせるにはどうするのでしょうか？

最初に、コマンドウィンドウが "python" という文字列をインタプリタを
開始するための導入として認識していることを確かめる必要があります。
コマンドウィンドウが開いたなら、コマンド ``python`` を入力してリターンキーを
打ってみましょう。するとこのようなものが現れます::

   Python 2.2 (#28, Dec 21 2001, 12:21:22) [MSC 32 bit (Intel)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

インタプリタの"対話モード"が始まりました。これで Python の文や式を対話的に
入力して、待っている間に実行や評価させることができます。これが Python の
最強の機能のひとつです。いくつかの式を選んで入力し、結果を見て確かめて
みましょう::

    >>> print("Hello")
    Hello
    >>> "Hello" * 3
    HelloHelloHello

多くの人が対話モードを便利で高度なプログラム可能計算機として使っています。
対話式 Python セッションを終わらせたいなら、Ctrl キーを押しながら Z を入力し、
"Enter" キーを打って Windows コマンドプロンプトに戻ってください。

また、スタートメニューには :menuselection:`Start --> Programs --> Python 2.2
--> Python (command line)` という項目があり、そこから新しいウィンドウで
``>>>`` というプロンプトが現れます。その場合は、Ctrl-Z の文字を入力すると
ウィンドウは消えます。Windows はウィンドウで "python" コマンドだけを
実行していて、そのウィンドウはインタプリタを終了すると閉じられるのです。

``python`` コマンドで、インタプリタプロンプト ``>>>`` ではなく
次のようなメッセージ::

   'python' is not recognized as an internal or external command,
   operable program or batch file.

.. sidebar:: |Adding Python to DOS Path|_
   :subtitle: `Adding Python to DOS Path`_

   Python はデフォルトでは DOS パスに加えられていません。この
   スクリーンキャストでは、すべてのユーザーがコマンドラインから Python を
   実行できるようにして、 `システムパス` に適切な entry を加えられるように
   します。

.. |Adding Python to DOS Path| image:: python-video-icon.png
.. _`Adding Python to DOS Path`:
   http://showmedo.com/videos/video?name=960000&fromSeriesID=96


や::

   Bad command or filename

が現れたなら、コンピュータが Python インタプリタの場所を認識しているか
確かめなければなりません。そのためには、Windows がプログラムを探す
ディレクトリのリストである PATH という設定を変更しなければなりません。

コマンドウィンドウが始まるごとに Python がインストールされたディレクトリが
PATH 加えられるように設定するといいでしょう。あなたが Python を
インストールしたのが結構最近なら、コマンド::

   dir C:\py*

で、どこにインストールされているかわかるでしょう。通常の場所は
``C:\Python23`` のようになっています。そうでなければ、ディスク全体を
検索することになるでしょう ... :menuselection:`Tools --> Find` を使うか
:guilabel:`Search` ボタンを押して "python.exe" を探してください。
Python が ``C:\Python23`` ディレクトリ (執筆時点でのデフォルト) に
インストールされていたとしたら、次のコマンドを入力すれば上と同じような
インタプリタが開始されることがわかるでしょう (もちろん、終了に
"CTRL-Z" と "Enter" が必要です)::

   c:\Python23\python

一旦ディレクトリを変更したら、コンピュータが行うスタートアップルーチンに
加える必要があります。古いバージョンの Windows では、一番簡単な方法は
``C:\AUTOEXEC.BAT`` ファイルを編集することです。\ ``AUTOEXEC.BAT`` に
以下の行を追加しましょう::

   PATH C:\Python23;%PATH%

Windows NT、2000、(おそらく) XP では、このような文字列::

   ;C:\Python23

を "マイコンピュータ" のプロパティウィンドウの "詳細" タブにある、
PATH 環境変数の現在の設定に加えましょう。なお、十分な権限があれば、
現在のユーザに設定するかシステムに設定するかを選べます。すべてのユーザーが
Python をコンピュータで実行したいのであれば後者を選ぶのがいいです。

この中に自信のない操作があれば、助けを求めてください！　ここでは、
新しい設定が効いたことを絶対確実にするために、システムを再起動しましょう。
Windows NT、XP、2000 では、おそらく再起動の必要はないでしょう。
それ以前のバージョンでも、\ ``AUTOEXEC.BAT`` の代わりに
``C:\WINDOWS\COMMAND\CMDINIT.BAT`` を編集すれば再起動しなくて済みます。

これで新しいコマンドウィンドウが開き、\ ``C:\>`` (等) のプロンプトに
``python`` を入力すれば、Python インタプリタが対話式コマンドを受け付けることを
示す ``>>>`` が現れるでしょう。

それでは、\ ``pytest.py`` というプログラムが ``C:\Steve\Projects\Python``
ディレクトリにあったとしましょう。このプログラムを実行するためのセッションは
このようになるでしょう::

   C:\> cd \Steve\Projects\Python
   C:\Steve\Projects\Python> python pytest.py

インタプリタを開始するためのコマンドにファイル名を加えたので、インタプリタは
開始時にその名前の Python スクリプトを読み込み、コンパイルし、実行し、終了し、
それから再び ``C:\>`` プロンプトが現れます。カレントディレクトリを
変更したくないなら、このように入力しても良いです::

   C:\> python \Steve\Projects\Python\pytest.py

NT、2000、XP では、インストール過程ですでにコマンド ``pytest.py`` (または、
カレントディレクトリになければ ``C:\Steve\Projects\Python\pytest.py``) が
".py" 拡張子を認識してその名前のファイルで Python を実行するように準備して
あるかもしれません。この機能を使うと便利ですが、Windows の *いくつかの*
バージョンでは、この形式がインタプリタを明示的に使うのと正確には同じに
ならないというバグがありますので、ご注意ください。

憶えておくべき重要なポイントは:

1. Python をスタートメニューから開始する、または PATH を正しく設定して
   Windows が Python インタプリタを見つけられるようにします::

      python

   で Python インタプリタから '>>>' プロンプトが与えられます。もちろん、
   CTRL-Z と ENTER でインタプリタが終了します(そして、スタートメニューから
   そのウィンドウを開始したのなら、そのウィンドウは消えます)。

2. それができたら、このコマンドでプログラムを実行してください::

      python {program-file}

3. 使うべきコマンドを知れば、特定の作業ディレクトリを指定して、
   どのスクリプト上でも Python インタプリタを実行する Windows ショートカットを
   構成できます。複雑なことがしたいなら::

      python --help

   を見てください。

4. 対話モード (``>>>`` プロンプトが現れるところ) は、単一の文や式が
   思ったとおりに動くか確かめたり、実験的にコードを開発するときに使うと
   最高です。


Python スクリプトを実行可能にするにはどうしますか？
---------------------------------------------------

Windows 2000 では、標準の Python インストーラはすでに .py 拡張子を
あるファイル型 (Python.File) に関連付け、そのファイル型にインタプリタを実行する
オープンコマンド (``D:\Program Files\Python\python.exe "%1" %*``) を与えます。
コマンドプロンプトから 'foo.py' としてスクリプトを実行可能にするには
これで十分です。スクリプトを拡張子なしで 'foo' とだけタイプして
実行したいのなら、PATHEXT 環境変数に .py を加えてください。

Windows NT では、インストーラによって行われる上記のような段階により、
スクリプトを 'foo.py' で実行できるようになりますが、長年のバグにより、
NT コマンドプロセッサで入力や出力のリダイレクトをすることは、この方法では
できません。これがしばしば重要になります。

Python スクリプトを WinNT で実行できるようにするおまじないは、
ファイルに .cmd 拡張子をつけ、最初の行に以下の文を加えることです::

   @setlocal enableextensions & python -x %~f0 %* & goto :EOF


Python の起動に時間がかかることがあるのはなぜですか？
-----------------------------------------------------

通常 Python は Windows でとても早く起動しますが、ときどき Python が急に
スタートアップに時間がかかるようになったというバグレポートがあります。
更に複雑なことに、Python は同様に設定された他の Windows システムでは
きちんと動くのです。

この問題はそのマシンのウイルス対策ソフトウェアの設定ミスによって
起こされることがあります。ウイルススキャナの中には、ファイルシステムからの
全ての読み込みを監視するように設定した場合に、二桁の
スタートアップオーバーヘッドを引き起すことが知られているものがあります。
あなたのシステムのウイルススキャンソフトウェアの設定を確かめて、
本当に同様に設定されていることを確実にしてください。


Windows 用の Freeze はどこにありますか？
----------------------------------------

"Freeze" は Python プログラムをひとつのスタンドアロンな実行可能なファイルに
まとめて送れるようにするプログラムです。これはコンパイラ *ではありません*\ 。
プログラムの実行が速くなるわけでも、配布が簡単になるわけでもありません、
少なくとも OS や CPU が同じならば。

Windows で freeze を使用できますが、ソースツリーをダウンロードする
必要があります (http://www.python.org/download/source を参照してください)。
freeze プログラムはソースツリーの ``Tools\freeze`` サブディレクトリにあります。

Microsoft VC++ コンパイラが必要で、Python をビルドすることも
必要になるでしょう。要求されるプロジェクトファイルは PCbuild ディレクトリに
あります。


``*.pyd`` ファイルは DLL と同じですか？
---------------------------------------

.. XXX update for py3k (PyInit_foo)

はい、.pyd ファイルは dll と同じようなものですが、少し違いがあります。
``foo.pyd`` という名前の DLL があったとしたら、それには関数 ``initfoo()`` が
含まれていなければなりません。そうすれば Python で "import foo" を書けて、
Python は foo.pyd (や foo.py、foo.pyc) を探して、あれば、\ ``initfoo()`` を
呼び出して初期化しようとします。Windows が DLL の存在を必要とするのと違い、
.exe ファイルを foo.lib にリンクするわけではありません。

なお、foo.pyd を検索するパスは PYTHONPATH であり、Windows が foo.dll を
検索するパスと同じではありません。また、プログラムを dll にリンクしたときは
プログラムの実行に dll が必要ですが、foo.pyd は実行には必要はありません。
もちろん、\ ``import foo`` したいなら foo.pyd は 必要です。DLL では、リンクは
ソースコード内で ``__declspec(dllexport)`` によって宣言されます。.pyd では、
リンクは使える関数のリストで定義されます。


Python を Windows アプリケーションに埋め込むにはどうしたらいいですか？
----------------------------------------------------------------------

Python インタプリタを Windows app に埋め込む方法は、次のように要約できます:

1. Python を .exe ファイルディレクトリに組み込 _まないでください_ 。Windows
   では、Python は (それ自体 DLL である) モジュールをインポートして扱う
   DLL でなくてはなりません (ドキュメント化されていない重大な事実の一つ目
   です)。組み込む代わりに、\ :file:`python{NN}.dll` にリンクしてください。
   通常は ``C:\Windows\System`` にインストールされています。\ *NN* は Python の
   バージョンで、Python 2.3 なら "23" のようになります。

   Python には、静的に、または動的にリンクできます。静的なリンクは、
   :file:`python{NN}.lib` に対してリンクするもので、動的なリンクは
   :file:`python{NN}.dll` に対してリンクするものです。動的なリンクの欠点は、
   :file:`python{NN}.dll` がシステムに存在しないとアプリケーションが起動しない
   ことです。(一般的な注意:
   :file:`python{NN}.lib` は :file:`python{NN}.dll` に対するいわゆる
   "インポートライブラリ" です。これは単にリンカに対するシンボルを定義します。)

   動的なリンクは、リンクの選択を大いに単純化します。
   全ては実行時に行われます。コードは Windows の
   ``LoadLibraryEx()`` ルーチンで :file:`python{NN}.dll` をロード
   しなければなりません。コードはまた、Windows の ``GetProcAddress()``
   ルーチンで得られるポインタで、\ :file:`python{NN}.dll` (すなわち、Python の
   C API)のルーチンとデータへアクセスしていなければなりません。マクロによって、
   このポインタを Python の C API のルーチンを呼び出す任意の C コードに通して
   使えます。

   Borland note: まず :file:`python{NN}.lib` を Coff2Omf.exe で OMF
   フォーマットに変換してください。

   .. XXX what about static linking?

2. SWIG を使えば、app のデータとメソッドを Python で使えるようにする Python
   "拡張モジュール"を簡単に作れます。SWIG は雑用を殆どやってくれるでしょう。
   結果として、.exe ファイル *の中に* リンクする C コードができます(！)。
   DLL を作 _らなくてもよく_ 、リンクも簡潔になります。

3. SWIG は拡張の名前に依る名前の init 関数 (C 関数) を作ります。例えば、
   モジュールの名前が leo なら、init 関数の名前は initleo() になります。
   SWIG shadow クラスを使ったほうがよく、そうすると init 関数の名前は
   initleoc() になります。これは shadow クラスが使うほとんど隠れた helper
   クラスを初期化します。

   ステップ 2 の C コードを .exe ファイルにリンクできるのは、初期化関数の
   呼び出しと Python へのモジュールのインポートが同等だからです！
   (ドキュメント化されていない重大な事実の二つ目です)

4. 要するに、以下のコードを使って Python インタプリタを拡張モジュール込みで
   初期化することができます。

   .. code-block:: c

      #include "python.h"
      ...
      Py_Initialize();  // Initialize Python.
      initmyAppc();  // Initialize (import) the helper class.
      PyRun_SimpleString("import myApp") ;  // Import the shadow class.

5. Python の C API には、pythonNN.dll をビルドするのに使われたコンパイラ
   MSVC 以外のコンパイラを使うと現れる二つの問題があります。

   問題 1: コンパイラによって struct FILE に対する概念が異なるため、FILE *
   引数を取るいわゆる "超高水準" 関数は、多コンパイラ環境で働きません。
   実装の観点から、これらは超 _低_ 水準関数になっています。

   問題 2: SWIG は void 関数へのラッパを生成するときに以下のコードを生成します:

   .. code-block:: c

      Py_INCREF(Py_None);
      _resultobj = Py_None;
      return _resultobj;

   ああ、Py_none は pythonNN.dll 内の _Py_NoneStruct という複雑なデータ構造に
   展開するマクロです。また、このコードは他コンパイラ環境では失敗します。
   このコードを次のように置き換えてください:

   .. code-block:: c

      return Py_BuildValue("");

   これで、SWIG をまだ仕事に使えない (私は SWIG の完全な初心者です) 私でも、
   SWIG の ``%typemap`` コマンドを使って自動的に変更できるようになります。

6. Python シェルスクリプトを使って Windows app 内から Python
   インタプリタウィンドウを掲示するのはいい方法ではありません。そのように
   表示されるウィンドウは app のウィンドウシステムとは関係ありません。むしろ
   "ネイティブな" インタプリタウィンドウを (wxPythonWindow を使ったりして)
   作るべきです。そのウィンドウを Python インタプリタにつなぐのは簡単です。
   Python の i/o は読み書きをサポートする _どんな_ オブジェクトにも
   リダイレクトできるので、read() と write() メソッドを含む (拡張モジュールで
   定義された) Python オブジェクトさえあればいいのです。


Python を CGI に使うにはどうしますか？
--------------------------------------

Microsoft IIS server と Win95 MS Personal Web Server では、
Python を他のどんなスクリプトエンジンとも同じように設定します。

regedt32 を起動し::

    HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W3SVC\Parameters\ScriptMap

に移動し、以下の行を入力してください。(システムによって変わることがあります)::

    .py :REG_SZ: c:\<path to python>\python.exe -u %s %s

この一行によって、スクリプトを ``http://yourserver/scripts/yourscript.py`` の
ように簡単な参照で呼び出せるようになります。ここで "scripts" は
(通常はデフォルトの) "executable" ディレクトリです。\ :option:`-u` フラグは
バッファリングを無効にしたバイナリモードを stdin に使うことを指定するフラグで、
バイナリデータを扱うときに必要です。

さらに、この状況で使われるファイル拡張子には ".py" を使うのを避けることを
勧めます (サポートモジュールに ``*.py`` を、"メインプログラム" スクリプトに
``*.cgi`` や ``*.cgp`` を残しておきたいでしょう)。

Python を CGI 加工に使うために Internet Information Services 5 を
設定するには、以下のリンクを参照してください:

   http://www.e-coli.net/pyiis_server.html (for Win2k Server)
   http://www.e-coli.net/pyiis.html (for Win2k pro)

Apache の設定はもっと単純です。Apache の設定ファイル ``httpd.conf`` で、
ファイルの終わりに以下の行を加えてください::

    ScriptInterpreterSource Registry

そして、Python CGI スクリプトに拡張子 .py をつけて、それらを
cgi-bin ディレクトリに置いてください。


エディタが Python ソースにタブを勝手に挿入しないようにするにはどうしますか？
----------------------------------------------------------------------------

この FAQ ではタブを使うことを勧めません。Python スタイルガイド :pep:`8` では、
配布される Python コードにはスペース 4 つを使うことを推奨しています。
これは Emacs の python-mode のデフォルトでも同じです。

いかなるエディタでも、タブとスペースを混ぜるのは良くないです。
MSVC も全く同じ立場であり、スペースを使うようにする設定が簡単にできます。
:menuselection:`Tools --> Options --> Tabs` を選択し、ファイルタイプの
"デフォルト" の "タブ幅" と "インデント幅" に 4 を設定して、
"スペースを挿入する" のラジオボタンを選択してください。

タブとスペースが混ざっていることで先頭の空白に問題が出ている可能性があるなら、
Python を :option:`-t` スイッチをつけて起動するか、
``Tools/Scripts/tabnanny.py`` を起動してディレクトリツリーをバッチモードで
確認してください。


ブロックすることなく押鍵を検出するにはどうしますか？
----------------------------------------------------

msvcrt モジュールを使ってください。これは標準の Windows 専用拡張モジュール
です。これはキーボードが打たれているかを調べる関数 ``kbhit()`` と、
反響することなく一文字を得る ``getch()`` を定義します。


os.kill() を Windows で模倣するにはどうしますか？
-------------------------------------------------

Python 2.7 および 3.2 以前では、プロセスを終了するために、\ :mod:`ctypes` が
使えます::

   import ctypes

   def kill(pid):
       """kill function for Win32"""
       kernel32 = ctypes.windll.kernel32
       handle = kernel32.OpenProcess(1, 0, pid)
       return (0 != kernel32.TerminateProcess(handle, 0))

2.7 および 3.2 では、上の関数と同様な :func:`os.kill` が実装されていて、
追加の機能として、CTRL+C や CTRL+BREAK をそれらのシグナルを扱うように設計された
コンソールのサブプロセスに送ることができます。


os.path.isdir() が NT で共有されたディレクトリで失敗するのはなぜですか？
------------------------------------------------------------------------

共有されたドライブの最後にいつも "\\" を加えることで、解決が見えます::

   >>> import os
   >>> os.path.isdir( '\\\\rorschach\\public')
   0
   >>> os.path.isdir( '\\\\rorschach\\public\\')
   1

共有店をドライブ文字と同じようなものと考えるとわかりやすいです。例::

   k: is not a directory
   k:\ is a directory
   k:\media is a directory
   k:\media\ is not a directory

"k:" を "\\conky\foo" に置き換えても同じことが言えます::

   \\conky\foo  is not a directory
   \\conky\foo\ is a directory
   \\conky\foo\media is a directory
   \\conky\foo\media\ is not a directory


cgi.py (その他の CGI プログラミング) が NT や win95 で動かないことがあります！
------------------------------------------------------------------------------

最新の python.exe であること、Python の GUI バージョンではなく
python.exe を使っていること、それからサーバが CGI 拡張に::

   "...\python.exe -u ..."

を実行するように設定してあることを確認してください。\ :option:`-u` (unbuffered)
オプションは NT や Win95 でインタプリタが標準入出力で改行を変換することを
防ぎます。これがないとリクエストの post/multipart は誤った長さを持つと
見なされ、バイナリ (例えば GIF) の応答がでっち上げられる(そして壊れた画像、
PDF ファイル、その他のバイナリのダウンロード失敗につながる)でしょう。


os.popen() が NT 上の PythonWin で動かないのはなぜですか？
----------------------------------------------------------

os.popen() が PythonWin の内部から動かないのは、Microsoft の C Runtime Library
(CRT) のバグによるものです。CRT はプロセスに Win32 コンソールが結び付けられて
いると決めてかかります。

その代わりに、Win32 コンソールが結び付けられているかに依らない win32pipe
モジュールの popen() を使うべきです。

例::

   import win32pipe
   f = win32pipe.popen('dir /c c:\\')
   print(f.readlines())
   f.close()


os.popen()/win32pipe.popen() が Win9x で動かないのはなぜですか？
----------------------------------------------------------------

Win9x にはバグがあって、os.popen/win32pipe.popen* が働きません。嬉しいことに、
この問題に対処する方法があります。Microsoft Knowledge Base のこの記事を
調べてください: Q150956。この knowledge base へのリンクはここで見つかります:
http://support.microsoft.com/\ 。


PyRun_SimpleFile() は Windows 上ではクラッシュしますが、Unix 上ではしません。なぜですか？
-----------------------------------------------------------------------------------------

コンパイラのベンダ、バージョン、(もしかすると) オプションに関しても微妙です。
埋め込みシステムの FILE* 構造体が Python インタプリタの想定と異なると、
うまく行きません。

Python 1.5.* DLLs (``python15.dll``) は全て MS VC++ 5.0 にて
マルチスレッディング DLL オプション (``/MD``) をつけてコンパイルされています。

コンパイラやフラグを変更できないなら、\ :c:func:`Py_RunSimpleString` を
使ってみてください。これで任意のファイルを起動するための技は、\ :func:`exec` や
:func:`open` をファイル名を引数として呼ぶことです。

また、Debug と Release 版は継ぎ合わせられません。Debug マルチスレッド DLL を
使いたいなら、そのモジュールは ``_d`` がファイル名に
加えられ *ていなくてはなりません*\ 。


Windows 95/98 上で _tkinter のインポートに失敗します。なぜですか？
------------------------------------------------------------------

たまに、\ _tkinter のインポートが Windows 95 や 98 で失敗し、その時に
以下のようなメッセージを訴えます::

   ImportError: DLL load failed: One of the library files needed
   to run this application cannot be found.

このとき Tcl/Tk がインストールされていないのかもしれませんが、Tcl/Tk が
インストールされていて、Wish アプリケーションが正しく動いているなら、
インストーラが autoexec.bat を適切に編集していないという問題かもしれません。
インストーラは PATH 環境変数に Tcl/Tk 'bin' サブディレクトリを含めるように
変える文を追加しようとしますが、この編集が機能していないことがあります。通常、
このファイルをノートパッドで開くことで、問題が何か解ります。

(David Szafranski による追加のヒント: ここで長いファイル名を使っては
いけません。例えば、\ ``C:\Program Files\Tcl\bin`` の代わりに
``C:\PROGRA~1\Tcl\bin`` を使ってください。)


ダウンロードされたドキュメントを Windows 上で展開するにはどうしますか？
-----------------------------------------------------------------------

たまに、web ブラウザで Windows マシンにドキュメントパッケージを
ダウンロードするとき、その保存されたファイルの拡張子が .EXE になっていることが
あります。これは間違いです。本来の拡張子は .TGZ です。

単純に、ダウンロードしたファイルを名付け直して拡張子を .TGZ にしてください。
そうすれば WinZip で扱えます。(手元の WinZip でできなかったら、
http://www.winzip.com から新しいのをもらいましょう)


cw3215mt.dll がありません(または cw3215.dll がありません)
---------------------------------------------------------

たまに、Tkinter を Windows で使っているとき、 cw3215mt.dll や cw3215.dll が
見つからないというエラーが出ます。

原因: パス (おそらく ``C:\Windows``) にある Tcl/Tk DLL が cygwin でビルドされた
古いものです。標準の Tcl/Tk インストール (Python 1.5.2 に付属しています) による
Tcl/Tk を使わなければなりません。


インストーラからのCTL3D32 version に関する警告
----------------------------------------------

Python インストーラはこのような警告をします::

   This version uses CTL3D32.DLL which is not the correct version.
   This version is used for windows NT applications only.

Tim Peters いわく:

   これは DLL の、そして悪名高きソースの問題です。このメッセージが伝えるものは
   こうです: この DLL のバージョンがオペレーティングシステムに合いません。
   Python のインストールが原因ではありません - それ以前にインストールした
   何かが OS に付属していた DLL を上書きしたのです (おそらく何かの古いソフト
   でしょうが、もうそれは判断できません)。検索エンジン (例えば Altavista) で
   "CTL3D32" を探せば、あらゆる種類のインストールプログラムでの同様の問題を
   訴えるウェブページが何百も何百も現れるでしょう。それらのページにシステムに
   あった正しいバージョンをダウンロードする方法が指摘されていることでしょう
   (Python によって起こされたものではないので、我々には直しようがないのです)。

David A Burton はこれを直すための小さなプログラムを書きました。
http://www.burtonsys.com/downloads.html に行って "ctl3dfix.zip" を
クリックしてください。

