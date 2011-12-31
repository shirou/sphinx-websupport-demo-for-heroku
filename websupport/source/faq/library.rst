:tocdepth: 2

====================
ライブラリと拡張 FAQ
====================

.. contents::

ライブラリ一般の質問
====================

作業 X を行うためのモジュールやアプリケーションを探すにはどうしますか？
-----------------------------------------------------------------------

:ref:`the Library Reference <library-index>` で関連した
標準ライブラリモジュールがないか探してください。(いずれ、何が標準ライブラリに
あるのかをおぼえて、この段階を飛ばせるようになるでしょう。)

サードパーティのパッケージについては、\ `Python Package Index
<http://pypi.python.org/pypi>`_ を探したり、\ `Google <http://www.google.com>`_
その他の Web サーチエンジンを試してください。"Python" に加えて一つか二つの
キーワードで興味のある話題を検索すれば、たいてい役に立つものが
見つかるでしょう。


math.py (socket.py, regex.py, etc.) のソースファイルはどこにありますか？
------------------------------------------------------------------------

モジュールのソースファイルが見つからなかったら、それは C、C++、その他の
コンパイルされた言語で実装され、ビルトインまたは動的にロードされる
モジュールかもしれません。この場合、ソースファイルが存在しないか、
(Python のパスではなく) C のソースディレクトリのどこかに
mathmodule.c のようにあるかもしれません。

Python のモジュールには、(少なくとも) 3 種類あります:

1) Python で書かれたモジュール (.py)。
2) C で書かれ、動的にロードされるモジュール (.dll, .pyd, .so, .sl, etc)。
3) C で書かれ、インタプリタにリンクされているモジュール。このリストを得るには、こうタイプしてください::

      import sys
      print(sys.builtin_module_names)


Python のスクリプトを Unix で実行可能にするにはどうしますか？
-------------------------------------------------------------

二つの条件があります :スクリプトファイルのモードが実行可能で、最初の行が
``#!`` で始まり Python インタプリタのパスが続いていなければなりません。

前者は、\ ``chmod +x scriptfile``\ 、場合によっては ``chmod 755 scriptfile``
を実行すればできます。

後者は、いくつかの方法でできます。最も単純な方法は、
ファイルの最初の行に、プラットフォーム上の Python がインストールされている
パス名を用いて、こう書くことです::

  #!/usr/local/bin/python

スクリプトが Python インタプリタのありかに依らないようにするために、
"env" プログラムを使えます。ほぼすべての Unix バリアントで、Python
インタプリタがユーザの $PATH ディレクトリにあれば、以下のようにできます::

  #!/usr/bin/env python

CGI スクリプトではこれを *しないでください*\ 。 CGI スクリプトの $PATH 変数は
往々にして小さすぎるので、インタプリタの実際のパス名を使わなくてはならないのです。

たまに、ユーザの環境がいっぱいすぎて /usr/bin/env プログラムが働かなかったり、
env プログラムが全く無かったりします。その場合、
(Alex Rezinsky による)以下の技法を試してください::

   #! /bin/sh
   """:"
   exec python $0 ${1+"$@"}
   """

これには、スクリプトの __doc__ 文字列を定義するというちょっとした欠点があります。しかし、これを付け足せば直せます::

   __doc__ = """...Whatever..."""



Python には curses/termcap パッケージはありますか？
---------------------------------------------------

.. XXX curses *is* built by default, isn't it?

Unix バリアントでは: 標準の Python ソース配布には、
``Modules/`` サブディレクトリに curses モジュールが同梱されていますが、
デフォルトではコンパイルされていません
(なお、Windows ディストリビューションでは使えません --
Windows 用の curses モジュールはありません)

curses モジュールには基礎的な curses の機能だけでなく、色や別の文字セットの
サポート、パッド、マウスのサポートなど、ncurses や SYSV curses 由来の
追加の関数も用意されています。これにより、このモジュールは BSD curses しか
持っていないオペレーティングシステムとの互換性を持たないことになりますが、
そのような現行の OS はなさそうです。

Windows では: `the consolelib module
<http://effbot.org/zone/console-index.htm>`_ を使ってください。


Python には C の onexit() に相当するものはありますか？
------------------------------------------------------

:mod:`atexit` モジュールは C の onexit と同じような
レジスタ関数を提供します。


シグナルハンドラが動かないのですがなぜですか？
----------------------------------------------

最もありがちな問題は、シグナルハンドラが間違った引数リストで
宣言されていることです。これは次のように呼び出されます::

   handler(signum, frame)

だから、これは二つの引数で宣言されるべきです::

   def handler(signum, frame):
       ...


よくある作業
============

Python のプログラムやコンポーネントをテストするにはどうしますか？
-----------------------------------------------------------------

Python には二つのテストフレームワークがついています。\ :mod:`doctest`
モジュールは 、モジュールの docstring から使用例を見つけてそれらを実行し、
出力を docstring によって与えられた望まれる出力と比較します。

:mod:`unittest` モジュールは、Java や Smalltalk のテストフレームワークを
模した装飾されたテストフレームワークです。

テストには、プログラムを書くのに、簡単にテストできるように良い
モジュール式デザインを使うのが役に立ちます。プログラムは、ほとんど全ての
機能を関数かクラスメソッドにカプセル化させるべきです -- そうすることで
プログラムの起動が速くなる (ローカル変数のアクセスはグローバルなアクセスよりも
速いから) という驚くべき嬉しい効果をもたらすこともあります。
さらに、変化するグローバル変数はテストを行うのを非常に難しくするので、
プログラムはそれに依らないようにしましょう。

プログラムの "global main logic" は、プログラムの main モジュールの最後に、
次のようにシンプルに書くべきです::

   if __name__ == "__main__":
       main_logic()

一旦、関数とクラス動作を扱いやすいように集めてプログラムを構成したら、
その動作を洗練させるようなテストを書きましょう。テストスイートには、
それぞれの一連のテストを自動化したモジュールも関係します。
それは大変そうですが、Python は簡潔で柔軟なので、驚くほど簡単です。
テスト関数を"プロダクションコード"と並行して書くことにより、
バグや設計上の欠陥を早く見つけることができるようになり、
コードをもっとずっと快適に楽しく書けます。

プログラムのメインモジュールとして設計されたのではない "補助モジュール" には、
モジュールの自己テストを含めるといいでしょう::

   if __name__ == "__main__":
       self_test()

複雑な外部インタフェースと作用し合うプログラムでさえ、
外部インタフェースが使えない時でも、Python で実装された
"fake" インタフェースを使ってテストできます。


Python のドキュメント文字列からドキュメントを生成するにはどうしますか？
-----------------------------------------------------------------------

:mod:`pydoc` モジュールで Python ソースコード内のドキュメント文字列から
HTML を生成できます。純粋に docstring から API ドキュメントを生成するには、
他に `epydoc <http://epydoc.sf.net/>`_ という選択肢もあります。
`Sphinx <http://sphinx.pocoo.org>`_ も docstring の内容を含めることができます。


一度に一つの押鍵を取得するにはどうしますか？
--------------------------------------------

Unix バリアントでは: いくつかの方法があります。curses を使えば簡単ですが、
curses はかなり大きいモジュールなので習得するのが難しいです。
ここに curses を使わない解決策を挙げます::

   import termios, fcntl, sys, os
   fd = sys.stdin.fileno()

   oldterm = termios.tcgetattr(fd)
   newattr = termios.tcgetattr(fd)
   newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
   termios.tcsetattr(fd, termios.TCSANOW, newattr)

   oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
   fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

   try:
       while 1:
           try:
               c = sys.stdin.read(1)
               print "Got character", repr(c)
           except IOError: pass
   finally:
       termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
       fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

これを動かすためには、\ :mod:`termios` と :mod:`fcntl` モジュールが必要です。
また、多分他でも動きますが、Linux でしかこれを試していません。
このコードでは、文字は一文字づつ読みこまれ、印字されます。

:func:`termios.tcsetattr` は stdin の反響を止め、標準モードを使えなくします。
:func:`fcntl.fnctl` は、stdin のファイルディスクリプタフラグを取得し、
それらをノンブロッキングモードに変えるのに使われます。stdin が空の時に
読み込むのは :exc:`IOError` になるので、このエラーは補足され、無視されます。


スレッド
========

スレッドを使ったプログラムを書くにはどうしますか？
--------------------------------------------------

:mod:`thread` モジュールではなく、
必ず :mod:`threading` モジュールを使ってください。\ :mod:`threading`
モジュールは、\ :mod:`thread` モジュールで提供される低レベルな
基本要素の、便利な抽象化を構成します。

Aahz は、役立つスレッディングのチュートリアルから成るスライドを揃えています。
http://www.pythoncraft.com/OSCON2001/ を参照してください。


スレッドが一つも実行されていないようです。なぜですか？
------------------------------------------------------

メインスレッドが終了するとともに、全てのスレッドは終了されます。
メインスレッドは速く働きすぎるので、スレッドには何をする時間も与えられません。

簡単な解決策は、プログラムの終わりに、スレッドが完了するのに十分な時間の
スリープを加えることです::

   import threading, time

   def thread_task(name, n):
       for i in range(n): print name, i

   for i in range(10):
       T = threading.Thread(target=thread_task, args=(str(i), i))
       T.start()

   time.sleep(10) # <----------------------------!

しかし、実際は (ほとんどのプラットフォームでは) スレッドは並行して
実行されるのではなく、一つづつ実行されるのです！ なぜなら、OS の
スレッドスケジューラは、前のスレッドがブロックされるまで
新しいスレッドを開始しないからです。

簡単に治すには、関数の実行の最初にちょっとスリープを加えることです::

   def thread_task(name, n):
       time.sleep(0.001) # <---------------------!
       for i in range(n): print name, i

   for i in range(10):
       T = threading.Thread(target=thread_task, args=(str(i), i))
       T.start()

   time.sleep(10)

:func:`time.sleep` による遅延をどれくらいとれば十分かを考えるより、
セマフォ構造を使ったほうがいいです。一つのやり方は、
:mod:`Queue` モジュールでキューオブジェクトを作り、それぞれの
スレッドが終了するごとにキューにトークンを加えさせ、メインスレッドに
スレッドがあるのと同じ数のトークンをキューから読み込ませるようにすることです。


たくさんのワーカースレッドに作業を割り振るにはどうしますか？
------------------------------------------------------------

:class:`Queue` モジュールで、
作業のリストを含むキューを作ってください。\ :class:`~Queue.Queue` クラスは
オブジェクトのリストを保持し、 ``.put(obj)`` で要素を加え、\ ``.get()`` で
要素を返すことができます。ロッキングを引き受けるクラスは、
全ての作業がちょうど一回づつ行われることを確実にしなければなりません。

ここにちょっとした例があります::

   import threading, Queue, time

   # The worker thread gets jobs off the queue.  When the queue is empty, it
   # assumes there will be no more work and exits.
   # (Realistically workers will run until terminated.)
   def worker ():
       print 'Running worker'
       time.sleep(0.1)
       while True:
           try:
               arg = q.get(block=False)
           except Queue.Empty:
               print 'Worker', threading.currentThread(),
               print 'queue empty'
               break
           else:
               print 'Worker', threading.currentThread(),
               print 'running with argument', arg
               time.sleep(0.5)

   # Create queue
   q = Queue.Queue()

   # Start a pool of 5 workers
   for i in range(5):
       t = threading.Thread(target=worker, name='worker %i' % (i+1))
       t.start()

   # Begin adding work to the queue
   for i in range(50):
       q.put(i)

   # Give threads time to run
   print 'Main thread sleeping'
   time.sleep(5)

実行時には、以下のように出力されます:

   Running worker
   Running worker
   Running worker
   Running worker
   Running worker
   Main thread sleeping
   Worker <Thread(worker 1, started 130283832797456)> running with argument 0
   Worker <Thread(worker 2, started 130283824404752)> running with argument 1
   Worker <Thread(worker 3, started 130283816012048)> running with argument 2
   Worker <Thread(worker 4, started 130283807619344)> running with argument 3
   Worker <Thread(worker 5, started 130283799226640)> running with argument 4
   Worker <Thread(worker 1, started 130283832797456)> running with argument 5
   ...


詳細はモジュールのドキュメントを参照してください。
``Queue`` クラスで多機能なインタフェースを使えます。


グローバルな値のスレッドセーフな変更の種類は何ですか？
------------------------------------------------------

グローバルインタプリタロック (GIL) が
内部で使われ、Python VM で一度に一つだけのスレッドが実行されることが
保証されています。一般に、Python ではスレッド間の切り替えを
バイトコード命令の間でのみ行います。切り替えの周期は、
:func:`sys.setcheckinterval` で設定できます。したがって、
それぞれのバイトコード命令、そしてそれぞれの命令が届く全ての C 実装コードは、
Python プログラムの観点からは、アトミックです。

このことから、理論上は、正確な勘定のためには PVM バイトコードの実装を
理解することが必要です。実際上は、組み込みデータ型(整数、リスト、辞書、等)の、
変数を共有する"アトミックそうな"演算は、実際にアトミックです。

例えば、以下の演算は全てアトミックです (L、L1、L2 はリスト、
D、D1、D2 は辞書、x、y はオブジェクト、i、j は整数です)::

   L.append(x)
   L1.extend(L2)
   x = L[i]
   x = L.pop()
   L1[i:j] = L2
   L.sort()
   x = y
   x.field = y
   D[x] = y
   D1.update(D2)
   D.keys()

これらは、アトミックではありません::

   i = i+1
   L.append(L[-1])
   L[i] = L[j]
   D[x] = D[x] + 1

他のオブジェクトを置き換えるような演算は、そのオブジェクトの参照カウントが
ゼロになったときに :meth:`__del__` メソッドを呼び出すことがあり、
これが影響を及ぼすかもしれません。これは特に、辞書やリストの大規模な更新に
当てはまります。疑わしければ、mutex を使ってください！


グローバルインタプリタロック (Global Interpreter Lock) を取り除くことはできないのですか？
-----------------------------------------------------------------------------------------

.. XXX mention multiprocessing
.. XXX link to dbeazley's talk about GIL?

マルチスレッド Python プログラムは事実上一つの CPU しか使えず、
(ほとんど) 全ての Python コードが グローバルインタプリタロック (GIL) が
保持されている間しか作動しなくなるということで、GIL は、
Python をハイエンドなマルチプロセッササーバマシン上に配備する上で
邪魔であると見なされがちです。

Python 1.5 の時代に、Greg Stein は GIL をきめ細かいロッキングで置き換える
総合パッチ ("free threading" パッチ) セットを実装しました。
残念ながら、(ロックがとても効率的な) Windows でさえ、標準的な
Python コードが、GIL を使ったインタプリタの 2 倍くらい遅くなりました。
Linux では、pthread ロックが効率的でないので、パフォーマンスの損失が更に
酷いです。

その後、GIL を取り除くという案はたまに出てきますが、だれも予期される
減速に対処する方法を見つけられず、スレッドを使わないユーザはこーどが
半分の速度でしか動作しないのでは幸せではありません。Greg の
free threading パッチは、以降の Python バージョンには更新されていません。

これは、Python をマルチ CPU マシンで使いこなせないことを意味しません！
作業を複数の *スレッド* ではなく、複数の *プロセッサ* に分けることを
考えればいいのです。
C 拡張をうまく使うことも役に立ちます。C 拡張を使ってに時間のかかる作業を
行わせれば、その実行のスレッドが C のコードにある間その拡張は
GIL を開放でき、他のスレッドに作業させることができます。

GIL を本当にグローバルにするより、インタプリタ状態ごとのロックにするべきと
いう提案もあります。そして、インタプリタはオブジェクトを共有するべきでは
ないということです。残念ながら、どちらも実現しないでしょう。多くの
オブジェクトの実装は現在、グローバル状態を持っているので、実現はたいへんな
大仕事になりそうです。例えば、小さな整数と短い文字列はキャッシュされます。
このキャッシュはインタプリタ状態に動かされなくてはなりません。他の
オブジェクト型は自身の自由変数リストを持っています。
これらの自由変数リストはインタプリタ状態に動かされなくてはなりません。等々。

それどころか、その作業が終わる時が来るかもわかりません。なぜなら、
サードパーティ拡張にも問題があるからです。サードパーティ拡張が書かれる
ペースは、インタプリタ状態にすべてのグローバル状態を格納するように変換できる
ペースよりも速いことでしょう。

そして最後に、一旦複数のインタプリタを状態を全く共有しないようにしたとして、
それぞれのインタプリタを独立したプロセス上で動かしてなにが
得られるというのでしょうか？


入力と出力
==========

ファイルを削除するにはどうしますか？ (その他、ファイルに関する質問...)
----------------------------------------------------------------------

``os.remove(filename)`` または ``os.unlink(filename)`` を使ってください。
ドキュメントは、\ :mod:`os` モジュールを参照してください。この二つの
関数は同じものです。\ :func:`unlink` は単に、
この関数の Unix システムコールの名称です。

ディレクトリを削除するには、\ :func:`os.rmdir` を使ってください。作成には
:func:`os.mkdir` を使ってください。\ ``os.makedirs(path)`` は ``path`` の
中間のディレクトリの、存在しないものを作成します。\ ``os.removedirs(path)`` は
中間のディレクトリが空である限り、それらを削除します。
ディレクトリツリー全体とその中身全てを削除したいなら、\ :func:`shutil.rmtree` を
使ってください。

ファイルの名前を変更するには、\ ``os.rename(old_path, new_path)`` を
使ってください。

ファイルを切り詰めるには、\ ``f = open(filename, "r+")`` でファイルを開いてから、
``f.truncate(offset)`` を使ってください。offset はデフォルトでは
現在のシーク位置です。\ :func:`os.open` で開かれたファイルのために、
``os.ftruncate(fd, offset)`` もあります。\ ``fd`` はファイルディスクリプタ
(小さな整数) です。

:mod:`shutil` モジュールにも、\ :func:`~shutil.copyfile`\ 、
:func:`~shutil.copytree`\ 、\ :func:`~shutil.rmtree` 等、ファイルに作用する
関数がいくつか含まれます。


ファイルをコピーするにはどうしますか？
--------------------------------------

:mod:`shutil` モジュールには :func:`~shutil.copyfile` 関数があります。
なお、MacOS 9 ではリソースフォークやファインダー情報をコピーしません。


バイナリデータを読み書きするにはどうしますか？
----------------------------------------------

複雑なバイナリデータ形式の読み書きには、\ :mod:`struct` モジュールを使うのが
一番です。これでバイナリデータ (通常は数) を含む文字列を取って、
Python オブジェクトに変換することができますし、その逆もできます。

例えば、以下のコードはファイルから 2 バイトの整数 2 個と 4 バイトの
整数 1 個をビッグエンディアンフォーマットで読み込みます::

   import struct

   with open(filename, "rb") as f:
      s = f.read(8)
      x, y, z = struct.unpack(">hhl", s)

フォーマット中の '>' はデータを強制的にビッグエンディアンにします。
ファイルから、文字 'h' は一つの"整数"(2 バイト)を読み込み、
文字 'l' は一つの"long 整数"を読み込みます。

より規則的なデータ (整数の、または浮動小数点数の均質なリスト等) には、
:mod:`array` モジュールも使えます。


os.popen() によって作られたパイプで os.read() が使われていないようです。なぜですか？
------------------------------------------------------------------------------------

:func:`os.read` は、開かれたファイルを表す小さな数である
ファイルディスクリプタを取る低レベルな関数です。\ :func:`os.popen` は、
組み込みの :func:`open` 関数が返すのと同じ型である高レベルな
ファイルオブジェクトを生成します。そうして、\ :func:`os.popen` から n バイトを
読み込むには、\ ``p.read(n)`` とする必要があります。

パイプを入力と出力の両方に接続してサブプロセスを動かすにはどうしますか？
------------------------------------------------------------------------

.. XXX update to use subprocess

:mod:`popen2` モジュールを使ってください。例えば::

   import popen2
   fromchild, tochild = popen2.popen2("command")
   tochild.write("input\n")
   tochild.flush()
   output = fromchild.readline()

警告: 一般的に、これをするのは賢くありません。
子があなたからの入力を待ってブロックされている間、プロセスが子からの入力を
待ってブロックされているというようなデッドロックを引き起こしやすいからです。
これは、親が子がそれよりも多くのテキストを出力することを期待することにより、
あるいはデータが書きださされないことで標準入出力バッファがスタックに
あることにより起こります。Python の親はもちろん子に送るデータを出力を
読み込む前に明示的に書きだすことができますが、子が素朴な C プログラムであると、
それが対話的なものであってさえ、書き出しが通常自動的なものであるがゆえ、
明示的に出力を書き出さないように書かれていることがあります。

なお、デッドロックは :func:`popen3` を使って標準出力や標準エラー出力を
読み込むときにも起こりえます。これらのどちらかが内部バッファにとって
大きすぎる (バッファサイズを増やしても役に立ちません) とき、もう片方を先に
``read()`` すると、同じくデッドロックが起こります。

popen2 におけるバグの注釈: プログラムが ``wait()`` や ``waitpid()`` を
呼び出さないかぎり、終了されていない子プロセスは取り除かれることがなく、
いずれ popen2 を呼び出すときに、子プロセス数の制限のために
失敗することがあります。\ :func:`os.waitpid` を :data:`os.WNOHANG` オプションを
つけて呼び出すことで、これを防げます。このような呼び出しをする場所は、
``popen2`` を再び呼びだす前がいいです。

多くの場合、本当にやるべきことは、コマンドを通して少しのデータを実行し、
結果を戻させることだけです。データの量がとても多いのでない限り、最も簡単な
方法は、それを一時ファイルに書きこみ、一時ファイルと入力としてコマンドを
実行することです。標準モジュール :mod:`tempfile` は、一意の一時ファイル名を
生成する ``mktemp()`` 関数をエクスポートします::

   import tempfile
   import os

   class Popen3:
       """
       This is a deadlock-safe version of popen that returns
       an object with errorlevel, out (a string) and err (a string).
       (capturestderr may not work under windows.)
       Example: print Popen3('grep spam','\n\nhere spam\n\n').out
       """
       def __init__(self,command,input=None,capturestderr=None):
           outfile=tempfile.mktemp()
           command="( %s ) > %s" % (command,outfile)
           if input:
               infile=tempfile.mktemp()
               open(infile,"w").write(input)
               command=command+" <"+infile
           if capturestderr:
               errfile=tempfile.mktemp()
               command=command+" 2>"+errfile
           self.errorlevel=os.system(command) >> 8
           self.out=open(outfile,"r").read()
           os.remove(outfile)
           if input:
               os.remove(infile)
           if capturestderr:
               self.err=open(errfile,"r").read()
               os.remove(errfile)

なお、多くの対話的プログラム (vi など) は、パイプで標準入出力を置き換える
ことがうまくいきません。このようなときは、パイプの代わりに擬似 tty ("pty") を
使わなければなりません。または、Don Libes の "expect" ライブラリへの Python
インタフェースを使うこともできます。expect へのインタフェースをする
Python 拡張は "expy" と呼ばれ、 http://expectpy.sourceforge.net から
利用できます。expect のように働く pure Python な解決法は、
`pexpect <http://pypi.python.org/pypi/pexpect/>`_ です。



シリアル (RS232) ポートにアクセスするにはどうしますか？
-------------------------------------------------------

Win32、POSIX (Linux、BSD、など)、Jythonでは:

   http://pyserial.sourceforge.net

Unix では、Mitch Chapman による Usenet の投稿を参照してください。

   http://groups.google.com/groups?selm=34A04430.CF9@ohioee.com


sys.stdout (stdin, stderr) を閉じようとしても実際に閉じられないのはなぜですか？
-------------------------------------------------------------------------------

Python のファイルオブジェクトは、
(ここで説明する中では) 低レベルな C ファイルディスクリプタの上にある、
中レベルな抽象のレイヤである C ストリームのそのまた上にある、
高レベルな抽象のレイヤです。

組み込みの ``open`` 関数によって生成されたほとんどの
ファイルオブジェクトでは、\ ``f.close()`` は Python ファイルオブジェクトが
Python の視点からは閉じられているものとする印をつけ、その下にある
C ファイルディスクリプタを閉じるように手配します。これは、\ ``f`` が
ガベージとなったときにも、\ ``f`` のデストラクタで自動的に起こります。

しかし、stdin、stdout、stderr は C で特別な立場が与えられていることから、
Python でも同様に特別に扱われます。\ ``sys.stdout.close()`` を実行すると、
Python レベルのファイルオブジェクトには閉じられているものとする印が
つけられますが、C ファイルディスクリプタは *閉じられません*\ 。

下にある C ファイルディスクリプタのうち、この三つのどれかを閉じるには、
まず本当に閉じる必要があることを確かめるべきです (例えば、拡張モジュールの
I/O を混乱させてしまうかもしれません)。本当に必要ならば、
``os.close`` を使ってください::

    os.close(0)   # close C's stdin stream
    os.close(1)   # close C's stdout stream
    os.close(2)   # close C's stderr stream


ネットワーク/インターネットプログラミング
=========================================

Python の WWW ツールには何がありますか？
----------------------------------------

ライブラリリファレンスマニュアルの :ref:`internet` と :ref:`netdata` と
いう章を参照してください。

.. XXX check if wiki page is still up to date

http://wiki.python.org/moin/WebProgramming で利用可能な
フレームワークの概要が Paul Boddie によって整備されています。

Cameron Laird は、\ http://phaseit.net/claird/comp.lang.python/web_python で
Python のウェブ技術に関する便利なページ群を整備しています。


CGI フォームの発信 (METHOD=POST) を模倣するにはどうしますか？
-------------------------------------------------------------

フォームを POST した結果のウェブページを取得したいです。
簡単に取得するためのコードはあるでしょうか？

あります。これは urllib.request を利用した簡単な例です::

   #!/usr/local/bin/python

   import httplib, sys, time

   ### build the query string
   qs = "First=Josephine&MI=Q&Last=Public"

   ### connect and send the server a path
   httpobj = httplib.HTTP('www.some-server.out-there', 80)
   httpobj.putrequest('POST', '/cgi-bin/some-cgi-script')
   ### now generate the rest of the HTTP headers...
   httpobj.putheader('Accept', '*/*')
   httpobj.putheader('Connection', 'Keep-Alive')
   httpobj.putheader('Content-type', 'application/x-www-form-urlencoded')
   httpobj.putheader('Content-length', '%d' % len(qs))
   httpobj.endheaders()
   httpobj.send(qs)
   ### find out what the server said in response...
   reply, msg, hdrs = httpobj.getreply()
   if reply != 200:
       sys.stdout.write(httpobj.getfile().read())

なお、一般にパーセントエンコードされた POST 演算では、クエリ文字列は必ず
:func:`urllib.parse.urlencode` で引用されなくてはなりません。
例えば name="Guy Steele, Jr." を送信するには::

   >>> import urllib.parse
   >>> urllib.parse.urlencode({'name': 'Guy Steele, Jr.'})
   'name=Guy+Steele%2C+Jr.'
   >>> from urllib import quote
   >>> x = quote("Guy Steele, Jr.")
   >>> x
   'Guy%20Steele,%20Jr.'
   >>> query_string = "name="+x
   >>> query_string
   'name=Guy%20Steele,%20Jr.'


どのモジュールが HTML の生成の役に立ちますか？
----------------------------------------------

.. XXX add modern template languages

さまざまなモジュールが利用できます:

* HTMLgen は全ての HTML 3.2 マークアップタグに対応するオブジェクトの
  クラスライブラリです。Python を書いていて、HTML ページを統合して web や
  CGI フォームを生成したい時などに使えます。

* DocumentTemplate および Zope Page Templates は、それぞれ Zope の
  一部であるシステムです。

* Quixote's PTL は Python の構文を使って文字列やテキストを組み立てます。

その他のリンクは、\ `Web Programming wiki pages
<http://wiki.python.org/moin/WebProgramming>`_ を参照してください。


Python のスクリプトからメールを送るにはどうしますか？
-----------------------------------------------------

標準ライブラリモジュール :mod:`smtplib` を使ってください。

以下に示すのが、これを使ったごく単純な対話型のメール送信器です。
このメソッドは SMTP リスナをサポートするホストならどこででも作動します::

   import sys, smtplib

   fromaddr = raw_input("From: ")
   toaddrs  = raw_input("To: ").split(',')
   print("Enter message, end with ^D:")
   msg = ''
   while True:
       line = sys.stdin.readline()
       if not line:
           break
       msg += line

   # The actual mail send
   server = smtplib.SMTP('localhost')
   server.sendmail(fromaddr, toaddrs, msg)
   server.quit()

Unix のみ、sendmail を使う方法もあります。sendmail プログラムのロケーションは、
システムによって変わります。\ ``/usr/lib/sendmail`` のときもあれば、
``/usr/sbin/sendmail`` のときもあります。sendmail のマニュアルページを
見れば解ります。これはサンプルコードです::

   SENDMAIL = "/usr/sbin/sendmail" # sendmail location
   import os
   p = os.popen("%s -t -i" % SENDMAIL, "w")
   p.write("To: receiver@example.com\n")
   p.write("Subject: test\n")
   p.write("\n") # blank line separating headers from body
   p.write("Some text\n")
   p.write("some more text\n")
   sts = p.close()
   if sts != 0:
       print "Sendmail exit status", sts


ソケットの connect() メソッドでブロッキングされなくするにはどうしますか？
-------------------------------------------------------------------------

主に select モジュールがソケットの非同期の I/O を扱うのに使われます。

TCP 接続がブロッキングされないようにするために、ソケットを
ノンブロッキングモードに設定することが出来ます。そして ``connect()``
したときに、即座に接続できるか、エラー番号を ``.errno`` として含む例外を
受け取るかのどちらかになります。\ ``errno.EINPROGRESS`` は、接続が
進行中であるが、まだ完了していないということを示します。異なる OS では
異なる値が返されるので、あなたのシステムで何が返されるかを
確かめておく必要があります。

``connect_ex()`` メソッドを使えば例外を生成しなくて済みます。これは単に
errno の値を返すでしょう。ポーリングのためには、後でまた ``connect_ex()`` を
呼び出すことができます -- 0 または ``errno.EISCONN`` は接続されたことを
表します -- または、選択するソケットにこれを渡して書き込み可能か
調べることができます。


データベース
============

Python にはデータベースパッケージへのインタフェースはありますか？
-----------------------------------------------------------------

はい。

.. XXX remove bsddb in py3k, fix other module names

:mod:`DBM <dbm.ndbm>` や :mod:`GDBM <dbm.gnu>` のような、ディスクに基づく
ハッシュへのインタフェースも標準の Python に含まれています。
ディスクに基づく軽量なリレーショナルデータベースを提供する
:mod:`sqlite3` モジュールもあります。

ほとんどの相対データベースがサポートされています。詳細は
`DatabaseProgramming wiki page
<http://wiki.python.org/moin/DatabaseProgramming>`_ を参照してください。


Python で永続的なオブジェクトを実装するにはどうしますか？
---------------------------------------------------------

:mod:`pickle` ライブラリモジュールで、ごく一般的な方法でこれを
解決できます (開かれたファイル、ソケット、ウィンドウのようなものを
保管することはできませんが)。\ :mod:`shelve` ライブラリモジュールは pickle と
(g)dbm を使い、任意の Python オブジェクトを含む永続的なマッピングを生成します。
パフォーマンスを良くするために、\ :mod:`cPickle` モジュールを使うことも
できます。

もっと不器用な方法は、pickle の妹分である marshal を使うことです。
:mod:`marshal` モジュールは、再帰的でない標準の Python 型を、
ファイルや文字列にとても高速に保存したり、元に戻したりする方法を提供します。
marshal では、インスタンスの保存や共有される参照の適切な処理などの派手な
ことはできませんが、極端に速く動作します。例えば、半メガバイトのデータに
3 分の 1 秒も掛からないでしょう。これは多くの場合、 pickle/shelve で
gdbm を使うというような、複雑な一般の方法に勝ります。


なぜ cPickle はこんなに遅いのですか？
-------------------------------------

.. XXX update this, default protocol is 2/3

pickle モジュールに使われているデフォルトのフォーマットは、読み込み可能な
pickle のための遅いものです。後方互換性は壊されますが、これを使ってください::

    largeString = 'z' * (100 * 1024)
    myPickle = cPickle.dumps(largeString, protocol=1)


bsddb (or anydbm) データベースが開かれたままプログラムがクラッシュすると、だめになってしまいます。なぜですか？
--------------------------------------------------------------------------------------------------------------

bsddb モジュール (やしばしば anydbm モジュール。優先的に bsddb を
使うでしょうから) で書き込みのために開かれたデータベースは、データベースの
``.close()`` メソッドで明示的に閉じられなければなりません。その基礎にある
ライブラリは、ディスク上の形式に変換されて書き込まれるべきデータベースの
中身を、キャッシュします。

新しい bsddb データベースを初期化したけれどプログラムのクラッシュ時までに
何も書き込まれていないとき、長さ 0 のファイルで終わることになり、
次にそのファイルが開かれたときに例外に出くわすでしょう。


Berkeley DB ファイルを開こうとしましたが、bsddb が bsddb.error: (22, 'Invalid argument') を生じます。助けてください！ データを復元するにはどうしたら良いですか？
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

慌てないでください！ あなたのデータはおそらく無事です。
このエラーの一番ありがちな原因は、新しいバージョンの Berkeley DB ライブラリから
古い Berkeley DB ファイルを開こうとすることです。

多くの Linux システムで、今では 3 種類全てのバージョンの Berkeley DB が
利用できます。バージョン 1 から新しいバージョンに移行するには、
db_dump185 でデータベースのプレーンテキスト版をダンプしてください。
バージョン 2 からバージョン 3 に移行するには、db_2dump でデータベースの
プレーンテキスト版を生成してください。そのどちらの場合でも、db_load で
コンピュータにインストールされている最新バージョンの新しい
ネイティブデータベースを生成してください。バージョン 3 の Berkeley DB が
インストールされているなら、db2_load でネイティブのバージョン 2 の
データベースを生成できるでしょう。

Berkeley DB バージョン 1 のハッシュファイルコードにはデータを破壊する
既知のバグがありますから、使うのをやめるべきです。


数学と数
========

Python でランダムな数を生成するにはどうしますか？
-------------------------------------------------

標準モジュールの :mod:`random` がランダムな数の生成器を実装しています。
使い方は単純です::

   import random
   random.random()

これは区間 [0, 1) 内のランダムな浮動小数点数を返します。

このモジュールにはその他多くの特化した生成器もあります。例えば:

* ``randrange(a, b)`` は区間 [a, b) から整数を選びます。
* ``uniform(a, b)`` は区間 [a, b) から浮動小数点数を選びます。
* ``normalvariate(mean, sdev)`` は正規(ガウス)分布をサンプリングします。

シーケンスに直接作用する高水準な関数もあります。例えば:

* ``choice(S)`` は与えられたシーケンスからランダムな要素を選びます。
* ``shuffle(L)`` はリストをインプレースにシャッフルします。
  すなわち、ランダムに並び替えます。

``Random`` クラスのインスタンスを生成して、複数の独立なランダムな数の
生成器をつくることもできます。
