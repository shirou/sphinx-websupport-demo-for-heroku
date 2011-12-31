..
  **************************************
    HOWTO Use Python in the web (英語)
  **************************************

************************************
  Python を Web 上で使うには HOWTO
************************************

:Author: Marek Kubica

..
  .. topic:: Abstract
  
     This document shows how Python fits into the web.  It presents some ways on
     how to integrate Python with the web server and general practices useful for
     developing web sites.

.. topic:: 概要

   このドキュメントは Python を web 向けに組み込む方法を示します。
   Python を web サーバとともに利用するためのいくつかの方法や
   web サイトを開発する際の一般的なプラクティスを示します。

..
  Programming for the Web has become a hot topic since the raise of the "Web 2.0",
  which focuses on user-generated content on web sites.  It has always been
  possible to use Python for creating web sites, but it was a rather tedious task.
  Therefore, many so-called "frameworks" and helper tools were created to help
  developers creating sites faster and these sites being more robust.  This HOWTO
  describes some of the methods used to combine Python with a web server to create
  dynamic content.  It is not meant as a general introduction as this topic is far
  too broad to be covered in one single document.  However, a short overview of
  the most popular libraries is provided.

web サイトのコンテンツをユーザが作るということに焦点を当てた "Web 2.0" の提起以来
Web プログラミングは人気の話題となっています。
web サイトを作るのに Python を利用することは可能でしたが、それは退屈な作業でした。
そのため、開発者がサイトを速く、頑強に作るのを助けるために多くの「フレームワーク」と補助ツールが作成されました。
この HOWTO では動的なコンテンツを作成するために Python と web サーバを結合させるいくつかの方法について述べます。
この話題に対する一般的な入門はこのドキュメントだけで扱いきれないほど広いわけではありませんが、
ここでは最も人気のあるライブラリの簡単な概要のみを扱います。

..
  .. seealso::
   
     While this HOWTO tries to give an overview over Python in the Web, it cannot
     always be as up to date as desired.  Web development in Python is moving
     forward rapidly, so the wiki page on `Web Programming
     <http://wiki.python.org/moin/WebProgramming>`_ might be more in sync with
     recent development.

.. seealso::

   この HOWTO は Python を web 上で使う方法の概要を扱おうとしていますが、
   HOWTO が常に望みどおりに最新の状況を伝えているとは限りません。
   Python での web 開発は急速に発展しています、そのため
   Wiki ページ `Web Programming <http://wiki.python.org/moin/WebProgramming>`_
   に多くの最新の開発に関する内容があるでしょう。
   
..
  The low-level view
  ==================
   
低レベルから見て
================
   
   .. .. image:: http.png
   
..
  When a user enters a web site, his browser makes a connection to the site's
  webserver (this is called the *request*).  The server looks up the file in the
  file system and sends it back to the user's browser, which displays it (this is
  the *response*).  This is roughly how the unterlying protocol, HTTP works.
   
ユーザが web サイトを訪れた時、ブラウザはサイトの web サーバとコネクションを形成します
(これは *リクエスト* と呼ばれます)。
サーバはファイルシステム上からファイルを探し出し、ユーザのブラウザにそれを送り返し、
ブラウザが表示します (これが *レスポンス* です)。
これが基礎となるプロトロル、 HTTP のおおまかな動作です。

..
  Now, dynamic web sites are not files in the file system, but rather programs
  which are run by the web server when a request comes in.  They can do all sorts
  of useful things, like display the postings of a bulletin board, show your
  mails, configurate software or just display the current time.  These programs
  can be written in about any programming language the server supports, so it is
  easy to use Python for creating dynamic web sites.
   
さて、動的な web サイトはファイルシステム上のファイルではなく、
リクエストが来たときに web サーバが実行するプログラムです。
それらは掲示板の投稿を表示したり、メールを表示したり、
ソフトウェアの設定や現在時刻の表示などの様々な便利なことができます。
これらのプログラムはサーバがサポートするあらゆる言語で書くことができます、
そのため動的な web サイトを作成するのに Python を利用することは簡単です。

..
  As most of HTTP servers are written in C or C++, they cannot execute Python code
  in a simple way -- a bridge is needed between the server and the program.  These
  bridges or rather interfaces define how programs interact with the server.  In
  the past there have been numerous attempts to create the best possible
  interface, but there are only a few worth mentioning.

ほとんどの HTTP サーバは C や C++ で書かれていて、
これらは Python コードを単純な方法で実行できません
-- サーバとプログラムの間にブリッジが必要です。
これらのブリッジやインターフェースはプログラムがサーバとどうやりとりするかを定めます。
これまでに最良のインターフェースを決めるために膨大な数の試みがなされてきましたが、
言及すべきものはわずかです。
   
..
  Not every web server supports every interface.  Many web servers do support only
  old, now-obsolete interfaces.  But they can often be extended using some
  third-party modules to support new interfaces.

全ての web サーバが全てのインターフェースをサポートしているわけではありません。
多くの web サーバは古い、現在では撤廃されたインターフェースのみをサポートしています。
しかし、多くの場合にはサードパーティーモジュールを利用して
新しいインターフェースをサポートするように拡張できます。
   
Common Gateway Interface
------------------------
   
..
  This interface is the oldest one, supported by nearly every web server out of
  the box.  Programs using CGI to communicate with their web server need to be
  started by the server for every request.  So, every request starts a new Python
  interpreter -- which takes some time to start up -- thus making the whole
  interface only usable for low load situations.
   
このインターフェースは最も古く、ほとんどの web サーバでサポートされ、すぐに使うことができます。
CGI を利用して web サーバと通信するプログラムはリクエスト毎に起動される必要があります。
そのため毎回のリクエストは新しい Python インタプリタを起動します
-- このため起動にいくらか時間がかかります --
そのためこのインターフェースは負荷が少ない状況にのみ向いています。

..
  The upside of CGI is that it is simple -- writing a program which uses CGI is a
  matter of about three lines of code.  But this simplicity comes at a price: it
  does very few things to help the developer.
   
CGI の利点は単純だということです
-- CGI を利用するプログラムを書くのは3行のコードを書くだけです。
しかし、この単純さは後で高くつきます;
開発者を少ししか助けてくれません。

..
  Writing CGI programs, while still possible, is not recommended anymore.  With
  WSGI (more on that later) it is possible to write programs that emulate CGI, so
  they can be run as CGI if no better option is available.

CGI プログラムを書くことは可能ではありますが、もはや推奨されません。
WSGI (詳しくは後で述べます) では CGI をエミュレートするプログラムを書くことができます、
そのため、よりよい選択肢が選べない場合には CGI としてプログラムを実行できます。

..
  .. seealso::
   
     The Python standard library includes some modules that are helpful for
     creating plain CGI programs:
  
     * :mod:`cgi` -- Handling of user input in CGI scripts
     * :mod:`cgitb` -- Displays nice tracebacks when errors happen in of CGI
       applications, instead of presenting a "500 Internal Server Error" message
   
     The Python wiki features a page on `CGI scripts
     <http://wiki.python.org/moin/CgiScripts>`_ with some additional information
     about CGI in Python.
 
.. seealso::

   Python の標準ライブラリには簡素な CGI プログラムを作成するのを助けるいくつかのモジュールが含まれています:

   * :mod:`cgi` -- CGI スクリプトでのユーザ入力を扱います
   * :mod:`cgitb` -- CGI アプリケーションの中でエラーが発生した場合に、
     "500 Internal Server Error" メッセージの代わりに親切なトレースバックを表示します

   Python wiki では `CGI scripts <http://wiki.python.org/moin/CgiScripts>`_ ページに
   Python での CGI に関した追加情報を取り上げています。
   
..
  Simple script for testing CGI
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
CGI をテストするための単純なスクリプト
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..
  To test whether your web server works with CGI, you can use this short and
  simple CGI program::

CGI が web サーバで動くかどうかを調べるのに、この短かく単純な CGI プログラムが利用できます::
   
    #!/usr/bin/env python
    # -*- coding: UTF-8 -*-

    # enable debugging
    import cgitb; cgitb.enable()

    print "Content-Type: text/plain;charset=utf-8"
    print

    print "Hello World!"
   
..
  You need to write this code into a file with a ``.py`` or ``.cgi`` extension,
  this depends on your web server configuration.  Depending on your web server
  configuration, this file may also need to be in a ``cgi-bin`` folder, for
  security reasons.
   
このコードは ``.py`` または ``.cgi`` 拡張子をつけたファイルに書く必要があります、
どちらを使うかは web サーバの設定に依存します。
web サーバの設定によっては、ファイルは ``cgi-bin`` フォルダ内にある必要があるかもしれません、
これはセキュリティ上の理由のためです。

..
  You might wonder what the ``cgitb`` line is about.  This line makes it possible
  to display a nice traceback instead of just crashing and displaying an "Internal
  Server Error" in the user's browser.  This is useful for debugging, but it might
  risk exposing some confident data to the user.  Don't use it when the script is
  ready for production use.  Still, you should *always* catch exceptions, and
  display proper error pages -- end-users don't like to see nondescript "Internal
  Server Errors" in their browsers.
   
``cgitb`` 行が何なのか疑問に思うかもしれません。
この行は、クラッシュしてブラウザで "Internal Server Error" と表示する代わりに、
親切なトレースバックを表示できるようにします。
これはデバッグの際に便利ですが、いくつかの重要なデータをユーザにさらけ出すリスクにもなりえます。
スクリプトを完成品として利用する準備ができたら ``cgitb`` は使ってはいけません。
さらに、 *常に* 例外を捕捉し、適切なエラーページを表示するようにしなければいけません
-- エンドユーザは漠然とした "Internal Server Errors" をブラウザで見ることを好みません。
   
..
  Setting up CGI on your own server
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

自身のサーバで CGI を立ち上げる
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
..
  If you don't have your own web server, this does not apply to you.  You can
  check whether if works as-is and if not you need to talk to the administrator of
  your web server anyway. If it is a big hoster, you can try filing a ticket
  asking for Python support.

自身の web サーバを持っていない場合には、この内容は当てはまらないでしょ。
そのままで動作するか調べることは可能です、もし動作しない場合、
とにかく web サーバの管理者と話し合う必要があります。
大きなホストである場合、チケットを埋めて Python サポートを得るということができるでしょう。
   
..
  If you're your own administrator or want to install it for testing purposes on
  your own computers, you have to configure it by yourself.  There is no one and
  single way on how to configure CGI, as there are many web servers with different
  configuration options.  The currently most widely used free web server is
  `Apache HTTPd <http://httpd.apache.org/>`_, Apache for short -- this is the one
  that most people use, it can be easily installed on nearly every system using
  the systems' package management.  But `lighttpd <http://www.lighttpd.net>`_ has
  been gaining attention since some time and is said to have a better performance.
  On many systems this server can also be installed using the package management,
  so manually compiling the web server is never needed.
  
  * On Apache you can take a look into the `Dynamic Content with CGI
    <http://httpd.apache.org/docs/2.2/howto/cgi.html>`_ tutorial, where everything
    is described.  Most of the time it is enough just to set ``+ExecCGI``.  The
    tutorial also describes the most common gotchas that might arise.
  * On lighttpd you need to use the `CGI module
    <http://trac.lighttpd.net/trac/wiki/Docs%3AModCGI>`_ which can be configured
    in a straightforward way.  It boils down to setting ``cgi.assign`` properly.
   
あなた自身が管理者であるか、自身のコンピュータで試すためにインストールしたい場合には
自分自身で設定する必要があります。
異なる設定オプションを持つ web サーバがたくさんあるため、
CGI の設定法はひとつではありません、
現在最も広く使われている web サーバは  `Apache HTTPd <http://httpd.apache.org/>`_ です、
Apache を簡単に説明すると -- 最も多くの人が利用しているもので、
ほとんど全てのシステムでシステムのパッケージ管理ソフトを利用して
簡単にインストールできます。
ただし `lighttpd <http://www.lighttpd.net>`_ も注目を集め始めていて、
さらにパフォーマンスの面でより優れているといわれています。
多くのシステムでこのサーバはパッケージ管理ソフトを利用してインストールできるので、
web サーバを手動でコンパイルする必要は全くありません。

* Apache ではチュートリアル `Dynamic Content with CGI
  <http://httpd.apache.org/docs/2.2/howto/cgi.html>`_ を参照できます、
  これには全てが書かれています。
  多くの場合には ``+ExecCGI`` を設定すれば十分です。
  このチュートリアルはよくでくわす可能性のある落し穴についても書かれています。
* lighttpd では `CGI module
  <http://trac.lighttpd.net/trac/wiki/Docs%3AModCGI>`_ を使う必要があります、
  これは直接的な方法で設定できます。
  結局のところ、 ``cgi.assign`` を適切に設定することになります。

..
  Common problems with CGI scripts
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CGI スクリプトでの一般的な問題
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
..
  Trying to use CGI sometimes leads to small annoyances that one might experience
  while trying to get these scripts to run.  Sometimes it happens that a seemingly
  correct script does not work as expected, which is caused by some small hidden
  reason that's difficult to spot.

CGI を利用しようとすると、しばしば小さないらいらを生むことになります、
その中でおそらく経験するものの一つは実行時するためにこれらのスクリプトの取得を
試みるときに起きます。
これによって一見正しいスクリプトが期待どおりに動かないことはよくあります、
これにはいくつかの小さな隠れた理由があるので、突き止めるのが困難です。

..
  Some of these reasons are:

いくつかの理由:
   
..
  * The Python script is not marked executable.  When CGI scripts are not
    executable most of the web servers will let the user download it, instead of
    running it and sending the output to the user.  For CGI scripts to run
    properly the ``+x`` bit needs to be set.  Using ``chmod a+x your_script.py``
    might already solve the problem.
  * The line endings must be of Unix-type.  This is important because the web
    server checks the first line of the script (called shebang) and tries to run
    the program specified there.  It gets easily confused by Windows line endings
    (Carriage Return & Line Feed, also called CRLF), so you have to convert the
    file to Unix line endings (only Line Feed, LF).  This can be done
    automatically by uploading the file via FTP in text mode instead of binary
    mode, but the preferred way is just telling your editor to save the files with
    Unix line endings.  Most proper editors support this.
  * Your web server must be able to read the file, you need to make sure the
    permissions are fine.  Often the server runs as user and group ``www-data``,
    so it might be worth a try to change the file ownership or making the file
    world readable by using ``chmod a+r your_script.py``.
  * The webserver must be able to know that the file you're trying to access is a
    CGI script.  Check the configuration of your web server, maybe there is some
    mistake.
  * The path to the interpreter in the shebang (``#!/usr/bin/env python``) must be
    currect.  This line calls ``/usr/bin/env`` to find Python, but it'll fail if
    there is no ``/usr/bin/env``.  If you know where your Python is installed, you
    can also use that path.  The commands ``whereis python`` and ``type -p
    python`` might also help to find where it is installed.  Once this is known,
    the shebang line can be changed accordingly: ``#!/usr/bin/python``.
  * The file must not contain a BOM (Byte Order Mark). The BOM is meant for
    determining the byte order of UTF-16 encodings, but some editors write this
    also into UTF-8 files.  The BOM interferes with the shebang line, so be sure
    to tell your editor not to write the BOM.
  * :ref:`mod-python` might be making problems.  mod_python is able to handle CGI
    scripts by itself, but it can also be a source for problems.  Be sure you
    disable it.

* Python スクリプトが実行可能であると示されていない。
  CGI スクリプトが実行不可能な場合、多くの web サーバは実行しユーザに出力を送る代わりに、
  ユーザがダウンロードできるようにします。
  CGI スクリプトに対しては適切に実行するために ``+x`` ビットが設定される必要があります。
  ``chmod a+x your_script.py`` を使うことで問題は解決します。
* 行末は Unix 形式である必要があります。これは、web サーバがスクリプト最初の行 (shebang と呼ばれます) を調べ、
  そこで指定されたプログラムの実行を試みるため重要となります。
  これは Windows の行末 (Carriage Return & Line Feed、または CRLF) とよく混同されます、
  そのためファイルを Unix 行末 (Line Feed のみ LF) に変換する必要があります。 
  これは FTP 経由でテキストモードではなくバイナリモードでファイルをアップロードすると自動的に行なわれますが、
  より望ましい方法は単にテキストエディタで Unix 行末で保存することです。
  多くの適切なエディタはこれをサポートしています。
* web サーバはファイルを読めるようにしなければいけないので、
  パーミッションが適切になっているか確認してください。
  しばしば、サーバは ``www-data`` ユーザ、グループとして実行します、
  そのためファイルのオーナーシップを変更するか、 ``chmod a+r your_script.py`` を使い
  ファイルを全世界から読み込み可能にするといったことは試す価値があります。
* web サーバはアクセスを試みているファイルが CGI スクリプトであるということを知っていなければいけません。
  web サーバの設定を確認して下さい、おそらくそこに間違いがあります。
* shebang 内のインタプリタへのパス (``#!/usr/bin/env python``) は正確でないといけません。
  この行は Python を見つけるために ``/usr/bin/env`` を呼び出しますが、
  ``/usr/bin/env`` が無い場合失敗します。
  Python がどこにインストールされているか知っている場合、そのパスを使うこともできます。
  ``whereis python`` と ``type -p python`` なども python がどこにインストールされたかを探すのに役立つでしょう。
  一旦わかってしまえば、shebang 行をそれに応じて変更できます: ``#!/usr/bin/python`` 。
* ファイルは BOM (Byte Order Mark) を含んでいてはいけません。
  BOM は UTF-16 エンコーディングのバイト順を決定するのに利用されます、
  しかしいくつかのエディタは UTF-8 ファイルに対してもそれを書き込むことがあります。
  BOM は shebang 行に影響するので、エディタが BOM を書かないようにしてください。
* :ref:`mod-python` が問題となることがあります。mod_python はそれ自身で CGI スクリプトを扱うことができますが、
  そのことが問題の原因となることがあります。
  利用できないようにして下さい。

.. _mod-python:

mod_python
----------
   
..
  People coming from PHP often find it hard to grasp how to use Python in the web.
  Their first thought is mostly `mod_python <http://www.modpython.org/>`_ because
  they think that this is the equivalent to ``mod_php``.  Actually it is not
  really.  It does embed the interpreter into the Apache process, thus speeding up
  requests by not having to start a Python interpreter every request.  On the
  other hand, it is by far not "Python intermixed with HTML" as PHP often does.
  The Python equivalent of that is a template engine.  mod_python itself is much
  more powerful and gives more access to Apache internals.  It can emulate CGI, it
  can work an a "Python Server Pages" mode similar to JSP which is "HTML
  intermangled with Python" and it has a "Publisher" which destignates one file to
  accept all requests and decide on what to do then.

PHP から来た人達はしばしば、Python を web 上で利用する方法を把握するのに苦労します。
彼らはたいてい最初に `mod_python <http://www.modpython.org/>`_ が
``mod_php`` と等価だと考えて、利用しようとします。
しかし実際にはそうではありません。
mod_python は Apache プロセスにインタプリタを埋め込まないため、毎回のリクエストで起動せず
スピードアップします。
一方で PHP でよくやるような「HTML への Python の埋め込み」とはかけ離れています。
Python でそれと等価なことをするのはテンプレートエンジンです。
mod_python 自身はより強力で Apache 内部に対してより多くのアクセスを提供します。
CGI をエミュレートし、
JSP に似た「HTML への Python 埋め込み」である "Python Server Pages" モードで動作でき、
全てのリクエストを一つのファイルで受け付けて何を実行するを決める "Publisher" を持っています。
   
..
  But mod_python has some problems.  Unlike the PHP interpreter the Python
  interpreter uses caching when executing files, so when changing a file the whole
  web server needs to be re-started to update.  Another problem ist the basic
  concept -- Apache starts some child processes to handle the requests and
  unfortunately every child process needs to load the whole Python interpreter
  even if it does not use it.  This makes the whole web server slower.  Another
  problem is that as mod_python is linked against a specific version of
  ``libpython``, it is not possible to switch from an older version to a newer
  (e.g. 2.4 to 2.5) without recompiling mod_python.  mod_python is also bound to
  the Apache web server, so programs written for mod_python cannot easily run on
  other web servers.
   
しかし、 mod_python はいくつかの問題も抱えています。
PHP インタプリタと違い Python インタプリタはファイル実行時にキャッシュを利用するため、
ファイルの変更時にはアップデートするには web サーバ全体を再起動する必要があります。
もう一つの問題は基本的なコンセプトにあります -- Apache はリクエストを扱うために
いくつかの子プロセスを開始し、不幸にも全ての子プロセスが Python インタプリタ全体を、
利用しない場合であっても、読み込む必要があるのです。
このため web サーバ全体が遅くなります。
別の問題は mod_python は ``libpython`` が特定のバージョンに対してリンクされることです、
mod_python を再コンパイルせずに古いバージョンから新しいバージョンに切り替える
(例えば 2.4 から 2.5) ことはできません。
さらに mod_python は Apache web サーバに制限されるため
mod_python 用に書かれたプログラムは他の web サーバで簡単に動かすことはできません。


..
  These are the reasons why mod_python should be avoided when writing new
  programs.  In some circumstances it might be still a good idea to use mod_python
  for deployment, but WSGI makes it possible to run WSGI programs under mod_python
  as well.
   
これらが新しくプログラムを書く際に mod_python を避けるべき理由です。
いくつかの状況では mod_python を利用するのはよいアイデアでしょうが、
WSGI は mod_python 下でも WSGI プログラムを同様に動かせます。
   
..
  FastCGI and SCGI
  ----------------

FastCGI と SCGI
---------------
   
..
  FastCGI and SCGI try to solve the performance problem of CGI in another way.
  Instead of embedding the interpreter into the web server, they create
  long-running processes which run in the background. There still is some module
  in the web server which makes it possible for the web server to "speak" with the
  background process.  As the background process is independent from the server,
  it can be written in any language of course also in Python.  The language just
  needs to have a library which handles the communication with the web server.

FastCGI と SCGI は CGI のパフォーマンス上の問題を別の方法で解決しようという試みです。
web サーバにインタプリタを組み込む代わりに、それらはバックグラウンドで長時間実行されるプロセスを生成します。
さらに web サーバ上にはいくつかのモジュールがあり、
それらは web サーバとバックグラウンドプロセスが「話す」ことを可能にします。
バックグラウンドプロセスはサーバと独立しているため、
もちろん Python を含んだ、任意の言語で書くことができます。
言語は web サーバとの通信を扱うライブラリを持っている必要があるだけです。
   
..
  The difference between FastCGI and SCGI is very small, as SCGI is essentially
  just a "simpler FastCGI".  But as the web server support for SCGI is limited
  most people use FastCGI instead, which works the same way.  Almost everything
  that applies to SCGI also applies to FastCGI as well, so we'll only write about
  the latter.

FastCGI と SCGI の違いはささいなもので、SCGI は基本的に "simpler FastCGI" です。
しかし、SCGI をサポートする web サーバは限定されているため、
多くの人々は代わりに同様に動作する FastCGI を利用します。
SCGI に適用されるほとんど全てのものは FastCGI にも適用できます、
そのため後者のみを書くことになるでしょう。
   
..
  These days, FastCGI is never used directly.  Just like ``mod_python`` it is only
  used for the deployment of WSGI applications.

最近では FastCGI を直接呼ぶことはありません。
``mod_python`` のように WSGI アプリケーションのみが利用されてます。
   
..
  .. seealso::
   
     * `FastCGI, SCGI, and Apache: Background and Future
       <http://www.vmunix.com/mark/blog/archives/2006/01/02/fastcgi-scgi-and-apache-background-and-future/>`_
       is a discussion on why the concept of FastCGI and SCGI is better that that
       of mod_python.
   
.. seealso::
 
   * `FastCGI, SCGI, and Apache: Background and Future
     <http://www.vmunix.com/mark/blog/archives/2006/01/02/fastcgi-scgi-and-apache-background-and-future/>`_
     には FastCGI と SCGI のコンセプトが mod_python よりどうして優れているかが検討されています。
   
..
  Setting up FastCGI
  ^^^^^^^^^^^^^^^^^^
   
FastCGI のセットアップ
^^^^^^^^^^^^^^^^^^^^^^
   
..
  Depending on the web server you need to have a special module.
  
  * Apache has both `mod_fastcgi <http://www.fastcgi.com/>`_ and `mod_fcgid
    <http://fastcgi.coremail.cn/>`_.  ``mod_fastcgi`` is the original one, but it
    has some licensing issues that's why it is sometimes considered non-free.
    ``mod_fcgid`` is a smaller, compatible alternative. One of these modules needs
    to be loaded by Apache.
  * lighttpd ships its own `FastCGI module
    <http://trac.lighttpd.net/trac/wiki/Docs%3AModFastCGI>`_ as well as an `SCGI
    module <http://trac.lighttpd.net/trac/wiki/Docs%3AModSCGI>`_.
  * nginx also supports `FastCGI
    <http://wiki.codemongers.com/NginxSimplePythonFCGI>`_.
   
web サーバに応じて特別なモジュールが必要となります。

* Apache には `mod_fastcgi <http://www.fastcgi.com/>`_ と 
  `mod_fcgid <http://fastcgi.coremail.cn/>`_ の両方があります。
  ``mod_fastcgi`` が最初に作られましたが、
  非フリーとして扱われるという、いくつかのライセンスの問題があります。
  ``mod_fcgid`` はより小さく、前者と互換性があります。
  このうちのどちらかを Apache から読み込む必要があります。
* lighttpd は自身に `FastCGI module
  <http://trac.lighttpd.net/trac/wiki/Docs%3AModFastCGI>`_ を含んでいて、
  `SCGI module <http://trac.lighttpd.net/trac/wiki/Docs%3AModSCGI>`_ も同様に含んでいます。
* nginx も `FastCGI <http://wiki.codemongers.com/NginxSimplePythonFCGI>`_ をサポートしています。
   
..
  Once you have installed and configured the module, you can test it with the
  following WSGI-application::

一旦モジュールをインストールして設定したら、以下の WSGI アプリケーションを使って
テストできます::
   
    #!/usr/bin/env python
    # -*- coding: UTF-8 -*-

    from cgi import escape
    import sys, os
    from flup.server.fcgi import WSGIServer

    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])

        yield '<h1>FastCGI Environment</h1>'
        yield '<table>'
        for k, v in sorted(environ.items()):
             yield '<tr><th>%s</th><td>%s</td></tr>' % (escape(k), escape(v))
        yield '</table>'

    WSGIServer(app).run()
   
..
  This is a simple WSGI application, but you need to install `flup
  <http://pypi.python.org/pypi/flup/1.0>`_ first, as flup handles the low level
  FastCGI access.

これは単純な WSGI アプリケーションですが、
まず `flup <http://pypi.python.org/pypi/flup/1.0>`_ をインストールする必要があります、
flup は低レベルの FastCGI アクセスを取り扱います。
   
..
  .. seealso::
   
     There is some documentation on `setting up Django with FastCGI
     <http://www.djangoproject.com/documentation/fastcgi/>`_, most of which can be
     reused for other WSGI-compliant frameworks and libraries.  Only the
     ``manage.py`` part has to be changed, the example used here can be used
     instead. Django does more or less the exact same thing.

.. seealso::
 
   `setting up Django with FastCGI <http://www.djangoproject.com/documentation/fastcgi/>`_
   にドキュメントがあります、この内の多くは WSGI 互換フレームワークやライブラリで再利用できます。
   代わりに ``manage.py`` の部分を変更するだけで、ここで使った例を利用できます。
   Django もほとんど同様のことを行います。
   
mod_wsgi
--------
   
..
  `mod_wsgi <http://www.modwsgi.org/>`_ is an attempt to get rid of the low level
  gateways.  As FastCGI, SCGI, mod_python are mostly used to deploy WSGI
  applications anyway, mod_wsgi was started to directly embed WSGI aplications
  into the Apache web server.  The benefit from this approach is that WSGI
  applications can be deployed much easier as is is specially designed to host
  WSGI applications -- unlike the other low level methods which have glue code to
  host WSGI applications (like flup which was mentioned before).  The downside is
  that mod_wsgi is limited to the Apache web server, other servers would need
  their own implementations of mod_wsgi.
   
`mod_wsgi <http://www.modwsgi.org/>`_ 低レベルなゲートウェイから脱するための試みです。
WSGI アプリケーションをどうにかして利用可能にするには多くの場合
FastCGI、SCGI、mod_python が利用されるますが、
mod_wsgi は WSGI アプリケーションを直接 Apache web サーバに埋め込みます。
この方法をとることによる恩恵は
ホストの WSGI アプリケーションのために特別にデザインされたものと比べて
より簡単な WSGI アプリケーションを利用できることです
-- ホストの WSGI アプリケーションに対するグルーコードを持つ他の低レベルな方法
(先ほど述べた flup のような) と違って。
mod_wsgi の欠点は Apache web サーバに制限されているということです、
他の web サーバは mod_wsgi の独自実装が必要となります。
   
..
  It supports two modes: the embedded mode in which it integrates with the Apache
  process and the daemon mode which is more FastCGI-like.  Contrary to FastCGI,
  mod_wsgi handles the worker-processes by itself which makes administration
  easier.
   
mod_wsgi は2つのモードをサポートします:
埋め込みモード(embeded mode)は Apache プロセスとデーモンプロセスを統合し、
動作としては FastCGI に似ています。
FastCGI と比較すると、mod_wsgi はそれ自身がワーカープロセスを取り扱うので
管理が楽になります。

..
  Step back: WSGI
  ===============

.. _WSGI:

後ろに下って: WSGI
==================
   
..   
  WSGI was already mentioned several times so it has to be something important.
  In fact it really is, so now it's time to explain.

WSGI について何度も言及してきたため、なにか重要そうに感じたでしょう。
実際に重要なので、ここで説明します。
   
..
  The *Web Server Gateway Interface*, :pep:`333` or WSGI for short is currently
  the best possible way to Python web programming.  While it is great for
  programmers writing frameworks, the normal person does not need to get in direct
  contact with it.  But when choosing a framework for web development it is a good
  idea to take one which supports WSGI.

*Web Server Gateway Interface*, :pep:`333` または略して WSGI は現在のところ
Python で web プログラミングをする最良の方法です。
programmers writing framework として卓越している一方で、
一般の人は直接接点を持つ必要はありません。
しかし、web 開発フレームワークとして選択する場合に、
WSGI を選ぶことは素晴しい考えです。

.. XXX programmers writing framework

..
  The big profit from WSGI is the unification.  When your program is compatible
  with WSGI -- that means that your framework has support for WSGI, your program
  can be deployed on every web server interface for which there are WSGI wrappers.
  So you do not need to care about whether the user uses mod_python or FastCGI --
  with WSGI it just works on any gateway interface.  The Python standard library
  contains its own WSGI server :mod:`wsgiref`, which is a small web server that
  can be used for testing.

WSGI を使う上での大きな利益は、統一性です。
WSGI と互換性のあるプログラムであれば
-- これはフレームワークが WSGI をサポートしているということを意味し、
プログラムは WSGI ラッパーを持つ全ての web サーバインターフェースで利用可能になります。
つまりユーザが mod_python か FastCGI どちらを利用しているかを気にせずにすみます。--
WSGI を使うことで任意ゲートウェイインターフェース上で動作するようになります。
Python 標準ライブラリには、テストのために利用できる小さな web サーバである、
独自の WSGI サーバ :mod:`wsgiref` が含まれています。
   
..
  A really great WSGI feature are the middlewares.  Middlewares are layers around
  your program which can add various functionality to it.  There is a `number of
  middlewares <http://wsgi.org/wsgi/Middleware_and_Utilities>`_ already available.
  For example, instead of writing your own session management (to identify a user
  in subsequent requests, as HTTP does not maintain state, so it does now know
  that the requests belong to the same user) you can just take one middleware,
  plug it in and you can rely an already existing functionality.  The same thing
  is compression -- say you want to compress your HTML using gzip, to save your
  server's bandwidth.  So you only need to plug-in a middleware and you're done.
  Authentication is also a problem easily solved using a middleware.
   
WSGI の本当に卓越している機能はミドルウェアです。
ミドルウェアとはプログラムに様々な機能性を加えるためのレイヤーのことを指します。
`無数のミドルウェア <http://wsgi.org/wsgi/Middleware_and_Utilities>`_ 
が利用可能になっています。
例えばセッション管理(連続したリクエストの中でユーザを同定を行います、HTTP は状態を維持しないので、
リクエストが同じユーザのものであるということがわかります)を書く代わりに、
ミドルウェアを取ってきて繋ぐだけで、既存の機能を当てにできます。
圧縮についても同じです -- HTML を gzip で圧縮してサーバの帯域を節約したい場合。
ミドルウェアを組み込むだけで行うことができます。認証もミドルウェアで簡単に解決できる問題です。

..
  So, generally -- although WSGI may seem complex, the initial phase of learning
  can be very rewarding as WSGI does already have solutions to many problems that
  might arise while writing web sites.
   
一般的には -- WSGI は複雑に思えるかもしれませんが、
WSGI は web サイトを書く際に起きうる多くの問題の解決法を持っているため、
学習の初期段階を実りあるものにしてくれます。
   
..
  WSGI Servers
  ------------
   
WSGI サーバ
-----------

..
  The code that is used to connect to various low level gateways like CGI or
  mod_python is called *WSGI server*.  One of these servers is ``flup`` which was
  already mentioned and supports FastCGI, SCGI as well as `AJP
  <http://en.wikipedia.org/wiki/Apache_JServ_Protocol>`_.  Some of these servers
  are written in Python as ``flup`` is, but there also exist others which are
  written in C and can be used as drop-in replacements.
  
CGI や mod_python などに様々な低レベルゲートウェイに接続するためのコードを
*WSGI サーバ* と呼びます。
これらのサーバの一つに ``flup`` があります、これは前に述べましたが FastCGI、SCGI と
`AJP <http://en.wikipedia.org/wiki/Apache_JServ_Protocol>`_ をサポートしています。
これらのサーバのいくつかは ``flup`` のように Python で書かれていますが、
C で書かれたものもあります、それらは気軽に置き換えることができます。

..
  There are quite a lot of servers already available, so a Python web application
  can be deployed nearly everywhere.  This is one big advantage that Python has
  compared with other web techniques.

いくつものサーバが利用可能ですから、Python の web アプリケーションはほとんどどこでも利用できます。
これは他の web テクニックと比べたときの Python の大きな利点です。

..
  .. seealso::
  
     A good overview of all WSGI-related code can be found in the `WSGI wiki
     <http://wsgi.org/wsgi>`_, which contains an extensive list of `WSGI servers
     <http://wsgi.org/wsgi/Servers>`_, which can be used by *every* application
     supporting WSGI.
  
     You might be interested in some WSGI-supporting modules already contained in
     the standard library, namely:
  
     * :mod:`wsgiref` -- some tiny utilities and servers for WSGI
   
.. seealso::

   `WSGI wiki <http://wsgi.org/wsgi>`_ は全ての WSGI に関連したコードに対して素晴しい概観を与えてくれます、
   ここには WSGI をサポートするアプリケーション *全て* が利用できるサーバの
   広大なリスト `WSGI servers <http://wsgi.org/wsgi/Servers>`_ が含まれています。

   標準ライブラリに含まれる WSGI をサポートするモジュールに興味が湧いたかもしれません:

   * :mod:`wsgiref` -- WSGI のためのいくつかの小さなユーティリティとサーバ
   
..
  Case study: MoinMoin
  --------------------
  
事例研究: MoinMoin
------------------

..
  What does WSGI give the web application developer?  Let's take a look on one
  long existing web application written in Python without using WSGI.
  
WSGI は web アプリケーションプログラマに何をもたらしてくれるのでしょうか?
長く存在しているWSGI を使わない、Python で書かれた web アプリケーションをみてみましょう。

..
  One of the most widely used wiki software is `MoinMoin <http://moinmo.in/>`_.
  It was created in 2000, so it predates WSGI by about three years.  While it now
  includes support for WSGI, older versions needed separate code to run on CGI,
  mod_python, FastCGI and standalone.  Now, this all is possible by using WSGI and
  the already-written gateways.  For running with on FastCGI ``flup`` can be used,
  for running a standalone server :mod:`wsgiref` is the way to go.

最も広く使われている wiki ソフトウェアの一つに `MoinMoin <http://moinmo.in/>`_ があります。
これは2000年に作られたため、WSGI より3年ほど先行していました。
現在では WSGI をサポートしていますが、古いバージョンでは CGI、mod_python、FastCGI、
スタンドアロンで動作するためには別々のコードが必要でした。
いまやこれら全ては WSGI と既存のゲートウェイを使って可能になりました。
FastCGI 上では ``flup`` を使って実行できますし、
スタンドアロンサーバとして実行するには :mod:`wsgiref` を使うことになります。

Model-view-controller
=====================

..
  The term *MVC* is often heard in statements like "framework *foo* supports MVC".
  While MVC is not really something technical but rather organisational, many web
  frameworks use this model to help the developer to bring structure into his
  program.  Bigger web applications can have lots of code so it is a good idea to
  have structure in the program right from the beginnings.  That way, even users
  of other frameworks (or even languages, as MVC is nothing Python-specific) can
  understand the existing code easier, as they are already familiar with the
  structure.
  
*MVC* という用語は 「フレームワーク *foo* は MVC をサポートしています」というような文句でよく聞きます。
MVC は技術的なものというよりかは、構造的なものです、
多くの web フレームワークはこのモデルを使って開発者がプログラムに構造を持ちこむことを助けています。
大きな web アプリケーションはたくさんのコードを持っているので、
最初からプログラムに構造を持たせることはよい考えです。
そうすることで、他のフレームワーク(他の言語でもかまいません、MVC は Python 特有のものではないので)のユーザであっても、
構造に既に馴染んでいるため、
存在しているコードを簡単に理解できるようになります。

..
  MVC stands for three components:
  
  * The *model*.  This is the data that is meant to modify.  In Python frameworks
    this component is often represented by the classes used by the
    object-relational mapper.  So, all declarations go here.
  * The *view*.  This component's job is to display the data of the model to the
    user.  Typically this component is represented by the templates.
  * The *controller*.  This is the layer between the user and the model.  The
    controller reacts on user actions (like opening some specific URL) and tells
    the model to modify the data if neccessary.

MVC は三要素からできています:

* *model* これは変更されるデータのことです。
  たいていの Python のフレームワークでこの要素は object-relational マッパーを
  利用したクラスで表現されます。
  つまり宣言部分はここに集約されます。
* *view* この要素はモデルのデータをユーザに表示する仕事を行います。
  典型的にはこの要素はテンプレートで表現されます。
* *controller* これはユーザとモデルの間のレイヤーです。
  controller はユーザの動作(特定の URL を開く等)に反応して、
  必要に応じてモデルにデータを変更するよう伝えます。
  
..
  While one might think that MVC is a complex design pattern, in fact it is not.
  It is used in Python because it has turned out to be useful for creating clean,
  maintainable web sites.
  
MVC を複雑なデザインパターンだと考える人もいるかもしれませんが、実際はそうではありません。
Python で使われているのは、それがきれいで保守可能な web サイトを作成するのに便利だということがわかっているからです。

..
  .. note::
  
     While not all Python frameworks explicitly support MVC, it is often trivial
     to create a web site which uses the MVC pattern by seperating the data logic
     (the model) from the user interaction logic (the controller) and the
     templates (the view).  That's why it is important not to write unneccessary
     Python code in the templates -- it is against MVC and creates more chaos.

.. note::

   全ての Python フレームワークが明示的に MVC をサポートしているわけではありませんが、
   MVC パターンを使った、データロジック (model) とインタラクションロジック (controller) 
   とテンプレート (view) を分離した web サイトを作成することはありふれています。
   その理由はテンプレートに不必要な Python コードを書かないことが重要なことだからです
   --  MVC に反すると大混乱を生むことになります。
  
..
  .. seealso::
  
     The english Wikipedia has an article about the `Model-View-Controller pattern
     <http://en.wikipedia.org/wiki/Model-view-controller>`_, which includes a long
     list of web frameworks for different programming languages.
  
.. seealso::

   Wikipedia の英語版には `Model-View-Controller pattern
   <http://en.wikipedia.org/wiki/Model-view-controller>`_ の記事があります、
   この記事には様々な言語での web フレームワークの長大なリストが含まれています。
  
..
  Ingredients for web sites
  =========================
  
web サイトの構成要素
====================
  
..
  Web sites are complex constructs, so tools were created to help the web site
  developer to make his work maintainable.  None of these tools are in any way
  Python specific, they also exist for other programming languages as well.  Of
  course, developers are not forced to use these tools and often there is no
  "best" tool, but it is worth informing yourself before choosing something
  because of the big number of helpers that the developer can use.

web サイトは複雑な構造物です、そのため web サイト開発者の保守作業を助けるために
ツールが作られました。
それらのツールは Python 固有のものではないので、他のプログラミング言語に対しても存在します。
もちろん、開発者はそれらのツールを使うことを強制されることはありませんし、
たいていの場合において「最良」のツールも存在しません、
しかし、開発者が利用できる道具は膨大にあるので、
どれかを選ぶ前に情報を得ておくことは価値のあることです、
  
..
  .. seealso::
  
     People have written far more components that can be combined than these
     presented here.  The Python wiki has a page about these components, called
     `Web Components <http://wiki.python.org/moin/WebComponents>`_.
  
.. seealso::

   ここで述べたものよりも多くの組み合わせ可能な要素が書かれています。
   Python wiki にはこれらの要素についてのページ
   `Web Components <http://wiki.python.org/moin/WebComponents>`_
   があります。
  
..
  Templates
  ---------

テンプレート
------------
  
..
  Mixing of HTML and Python code is possible with some libraries.  While
  convenient at first, it leads to horribly unmaintainable code.  That's why
  templates exist.  Templates are, in the simplest case, just HTML files with
  placeholders.  The HTML is sent to the user's browser after filling out the
  placeholders.
  
HTML と Python コードを混在させることは、いくつかのライブラリを利用することで可能になります。
最初は便利ですが、そうすることでコードが保守不可能となる恐れがあります。
これがテンプレートが存在する理由です。
テンプレートは、最も単純な場合には、単にプレースホルダーを持つ HTML ファイルとなります。
プレースホルダーを埋めた後に HTML はユーザのブラウザに送信されます。

..
  Python already includes such simple templates::
  
Python はこのような単純なテンプレートを含んでいます::

      # a simple template
      template = "<html><body><h1>Hello %s!</h1></body></html>"
      print template % "Reader"

..
  The Python standard library also includes some more advanced templates usable
  through :class:`string.Template`, but in HTML templates it is needed to use
  conditional and looping contructs like Python's *for* and *if*.  So, some
  *template engine* is needed.

Python の標準ライブラリには、 :class:`string.Template` を通して利用できる
より高度なテンプレートも含まれています、
しかし、HTML テンプレートには Python の *for* や *if* のような条件やループなどが使えることが必要です。
そのため、 *テンプレートエンジン* が必要になります。
  
..
  Now, Python has a lot of template engines which can be used with or without a
  `framework`_.  Some of these are using a plain-text programming language which
  is very easy to learn as it is quite limited while others use XML so the
  template output is always guaranteed to be valid XML.  Some `frameworks`_ ship
  their own template engine or recommend one particular.  If one is not yet sure,
  using these is a good idea.
  
いまや、Python には多くのテンプレートエンジンがあり、
`framework`_ とともに、または独立に利用できます。
いくつかのテンプレートエンジンは平文のプログラミング言語を利用します、
この言語はとても限定的なので簡単に学ぶことができます、
一方で他のものには XML を利用し、テンプレートの出力が正当な XML であることが
保証されているものがあります。
いくつかの `framework`_ は独自のテンプレートエンジンを含んでいたり、
特定のエンジンを使うことを推奨しています。
もしどれがいいかわからない場合には、使ってみるといいでしょう。

..
  .. note::
  
     While Python has quite a lot of different template engines it usually does
     not make sense to use a homebrewed template system.  The time needed to
     evaluate all templating systems is not really worth it, better invest the
     time in looking through the most popular ones.  Some frameworks have their
     own template engine or have a recommentation for one.  It's wise to use
     these.
  
     Popular template engines include:
  
     * Mako
     * Genshi
     * Jinja
  
.. note::

   Python はほんとうに様々なテンプレートエンジンを持っていますが、
   たいていの場合に手製のテンプレートシステムを使うことは理にかないません。
   全てのテンプレートシステムを評価するのは不毛ですから、
   最も人気のあるものを探すのに時間を割いた方がよいでしょう。
   いくつかのフレームワークは独自のテンプレートエンジンを持っていたり、
   推奨しているものがあります。
   これらを選ぶのが賢いでしょう。

   人気のあるテンプレートエンジンに含まれるものは:
   
   * Mako
   * Genshi
   * Jinja

..
  .. seealso::
  
     Lots of different template engines divide the attention between themselves
     because it's easy to create them in Python.  The page `Templating
     <http://wiki.python.org/moin/Templating>`_ in the wiki lists a big,
     ever-growing number of these.
  
.. seealso::

   たくさんの様々なテンプレートエンジンが、それぞれに注目を分けあっています、
   これは Python でのエンジン作成が簡単なためです。
   wiki の `Templating <http://wiki.python.org/moin/Templating>`_ 
   には巨大な今も増え続けるエンジンが列挙されています。
  
..
  Data persistence
  ----------------

データの永続性
--------------
  
..
  *Data persistence*, while sounding very complicated is just about storing data.
  This data might be the text of blog entries, the postings of a bulletin board or
  the text of a wiki page.  As always, there are different ways to store
  informations on a web server.
  
*データの永続性 (data persistence)* は複雑に聞こえますが、単にデータを蓄積するだけです。
このデータはブログのエントリであったり、掲示板の投稿であったり、
wiki ページのテキストであったりします。
例のごとく web サーバに情報をたくわえるには様々な方法があります。

..
  Often relational database engines like `MySQL <http://www.mysql.com/>`_ or
  `PostgreSQL <http://www.postgresql.org/>`_ are used due to their good
  performance handling very large databases consisting of up to millions of
  entries.  These are *queried* using a language called `SQL
  <http://en.wikipedia.org/wiki/SQL>`_.  Python programmers in general do not like
  SQL too much, they prefer to work with objects.  It is possible to save Python
  objects into a database using a technology called `ORM
  <http://en.wikipedia.org/wiki/Object-relational_mapping>`_.  ORM translates all
  object-oriented access into SQL code under the hood, the user does not need to
  think about it.  Most `frameworks`_ use ORMs and it works quite well.

しばしば `MySQL <http://www.mysql.com/>`_ や `PostgreSQL <http://www.postgresql.org/>`_ 
のようなリレーショナルデータベースエンジンが利用されます、
それは数百万エントリに及ぶ非常に大きなデータベースを優れたパフォーマンスで扱うことができるためです。
それらは `SQL <http://en.wikipedia.org/wiki/SQL>`_ と呼ばれる言語を利用した *照会 (queried)* です。
一般的な Python プログラマは SQL をあまり好みません、
彼らはオブジェクトで動作する方を好みます。
`ORM <http://en.wikipedia.org/wiki/Object-relational_mapping>`_ と呼ばれる技術を使うことで
データベース内の Python オブジェクトを節約できます。
ORM は内部でオブジェクト指向的アクセスを SQL コードに変換し、
ユーザはそのことを意識せずに済みます。
多くの `framework`_ は ORMs を利用し、とてもうまく動作します.

..
  A second possibility is using files that are saved on the hard disk (sometimes
  called flatfiles).  This is very easy, but is not too fast.  There is even a
  small database engine called `SQLite <http://www.sqlite.org/>`_ which is bundled
  with Python in the :mod:`sqlite` module and uses only one file.  This database
  can be used to store objects via an ORM and has no other dependencies.  For
  smaller sites SQLite is just enough.  But it is not the only way in which data
  can be saved into the file systems.  Sometimes normal, plain text files are
  enough.
  
第2の可能性はハードディスクに保存されたファイルを利用することです
(しばしば、フラットファイルと呼ばれます)。
これはとても簡単ですが、高速ではありません。
`SQLite <http://www.sqlite.org/>`_ と呼ばれる小さなデータベースエンジンもあります、
これは Python に :mod:`sqlite` モジュールとしてバンドルされていて、ファイル一つだけを利用します。
このデータベースは ORM 経由でオブジェクトを保存するのに利用できて、依存関係がありません。
小さなサイトに対しては SQLite で十分です。
ただ、データをファイルシステムに保存する方法はこれだけではありません。
普通の平文のテキストファイルで十分な場合もあります。

..
  The third and least used possibility are so-called object oriented databases.
  These databases store the *actual objects* instead of the relations that
  OR-mapping creates between rows in a database.  This has the advantage that
  nearly all objects can be saven in a straightforward way, unlike in relational
  databases where some objects are very hard to represent with ORMs.

第3の最も利用されない方法はオブジェクト指向データベースと呼ばれています。
このデータベースは、OR マッピングによって行との間に作成されるリレーションの代わりに、
*実際のオブジェクト* を保存します。
この方法にはほとんど全てのオブジェクトを直接的な方法で保存できるという利点があります、
これはリレーショナルデータベースでいくつかのオブジェクトが ORMs で表現するのが困難であるのと対照的です。
  
..
  `Frameworks`_ often give the users hints on which method to choose, it is
  usually a good idea to stick to these unless there are some special requirements
  which require to use the one method and not the other.
  
`framework`_ はしばしばユーザにどの方法を選べばいいか、ヒントを与えてくれます。
たいていの場合、一つだけの方法を必要とする特別な条件がある場合がない限りは、
それに従うことはいい考えです。

..
  .. seealso::
  
     * `Persistence Tools <http://wiki.python.org/moin/PersistenceTools>`_ lists
       possibilities on how to save data in the file system, some of these modules
       are part of the standard library
     * `Database Programming <http://wiki.python.org/moin/DatabaseProgramming>`_
       helps on choosing a method on how to save the data
     * `SQLAlchemy <http://www.sqlalchemy.org/>`_, the most powerful OR-Mapper for
       Python and `Elixir <http://elixir.ematia.de/>`_ which makes it easier to
       use
     * `SQLObject <http://www.sqlobject.org/>`_, another popular OR-Mapper
     * `ZODB <https://launchpad.net/zodb>`_ and `Durus
       <http://www.mems-exchange.org/software/durus/>`_, two object oriented
       databases

.. seealso::

   * `Persistence Tools <http://wiki.python.org/moin/PersistenceTools>`_ は
     ファイルシステムにデータを保存する方法が列挙されています、
     これらのモジュールの内のいくつかは標準ライブラリの一部です
   * `Database Programming <http://wiki.python.org/moin/DatabaseProgramming>`_
     はデータ保存の方法を選ぶのを助けてくれます
   * `SQLAlchemy <http://www.sqlalchemy.org/>`_ は Python での最も強力な OR マッパーで、
     `Elixir <http://elixir.ematia.de/>`_ は利用しやすいものにしてくれます
   * `SQLObject <http://www.sqlobject.org/>`_ は別の人気のある OR マッパーです
   * `ZODB <https://launchpad.net/zodb>`_ と
     `Durus <http://www.mems-exchange.org/software/durus/>`_ の二つはオブジェクト指向データベースです
  
  
..
  Frameworks
  ==========

.. _framework:
 
フレームワーク
==============

..
  As web sites can easily become quite large, there are so-called frameworks which
  were created to help the developer with making these sites.  Although the most
  well-known framework is Ruby on Rails, Python does also have its own frameworks
  which are partly inspired by Rails or which were existing a long time before
  Rails.

web サイトは簡単に大きくなりうるので、開発者がそれらのサイトを簡単に扱えるよう助けるものは
フレームワークと呼ばれます。
最も知られたフレームワークは Ruby on Rails ですが、Python も独自のフレームワークを持っていて、
それらは Rails からヒントを得たものであったり、Rails より以前から存在していたものであったりします。
  
..
  Two possible approaches to web frameworks exist: the minimalistic approach and
  the all-inclusive approach (somtimes called *full-stack*). Frameworks which are
  all-inclusive give you everything you need to start working, like a template
  engine, some way to save and access data in databases and many features more.
  Most users are best off using these as they are widely used by lots of other
  users and well documented in form of books and tutorials.  Other web frameworks
  go the minimalistic approach trying to be as flexible as possible leaving the
  user the freedom to choose what's best for him.

web フレームワークのアプローチには二つの方法があります: 最小主義アプローチと
全てを含む包括的アプーチ (しばしば *full-stack* と呼ばれます) です。
包括的なフレームワークは作業を始めるのに必要なもの全てが揃っています、
テンプレートエンジン、いくつかのデータベースへの保存、アクセス方法やその他の機能。
それらは他の多くユーザによって広く利用されていて、
本やチュートリアルといった形式で詳細なドキュメントが準備されているので、
多くのユーザはそれらを利用して順調に進めることができます、
他の web フレームワークは最小主義アプローチをとり、
できるだけ自由に変えられるようにして、
ユーザがどれが最良かを選ぶ自由を残せるようにしています。
  
..
  The majority of users is best off with all-inclusive framewors.  They bring
  everything along so a user can just jump in and start to code.  While they do
  have some limitations they can fullfill 80% of what one will ever want to
  perfectly.  They consist of various components which are designed to work
  together as good as possible.
  
ユーザの多数は包括的フレームワークを利用することで順調に進めることができます。
それらのフレームワークは全てを備えているので、ユーザは単に飛び乗ってコートを書くことができます。
それらには制限がある一方で、申し分なくやりたいと思った内容の 80% は埋めてくれます。
それらは多様な要素から成っていて、それぞれの要素ができるだけうまく協調できるようにデザインされています。

..
  The multitude of web frameworks written in Python demonstrates that it is really
  easy to write one.  One of the most well-known web applications written in
  Python is `Zope <http://www.zope.org/>`_ which can be regarded as some kind of
  big framework.  But Zope was not the only framework, there were some others
  which are by now nearly forgotten.  These do not need to be mentioned anymore,
  because most people that used them moved on to newer ones.
  
Python で書かれた web フレームワークが大多数存在することは、
実際にそれらを書くことが容易だということを実証しています。
Python で書かれた web アプリケーションで最も知られているものは 
`Zope <http://www.zope.org/>`_ で、
これは大きなフレームワークの一種とみなすことができます。
しかし、いまではほとんど忘れられていますが、Zope は単なるフレームワークではありません、
利用者の多くが新しいものに移行したため、それらについてこれ以上記述する必要はないでしょう。

..
  Some notable frameworks
  -----------------------

いくつかの著名なフレームワーク
------------------------------
  
..
  There is an incredible number of frameworks, so there is no way to describe them
  all.  It is not even neccessary, as most of these frameworks are nothing special
  and everything that can be done with these can also be done with one of the
  popular ones.
  
膨大な数のフレームワークがあるので、全てについて記述することは不可能ですし、
その必要さえありません、なぜならほとんどのフレームワークは特別なものではありませんし、
それらにできることは人気のあるものでできます。
  
Django
^^^^^^
  
..
  `Django <http://www.djangoproject.com/>`_ is a framework consisting of several
  tightly coupled elements which were written from scratch and work together very
  well.  It includes an ORM which is quite powerful while being simple to use and
  has a great online administration interface which makes it possible to edit the
  data in the database with a browser.  The template engine is text-based and is
  designed to be usable for page designers who cannot write Python.  It supports
  so-called template inheritance and filters (which work like Unix pipes).  Django
  has many handy features bundled, like creation of RSS feeds or generic views
  which make it possible to write web sites nearly without any Python code.
  
`Django <http://www.djangoproject.com/>`_ はスクラッチから書かれた、
とてもうまく協調する、いくつかの要素が強く結びついてできたフレームワークです。
ORM を含んでいてとても強力である上に、単純に利用でき、
ブラウザからデータベース上のデータを編集できる優秀な管理インターフェースを持っています。
テンプレートエンジンはテキストベースで動作し、
Python を書けないページデザイナーにとっても利用しやすいようにデザインされています。
テンプレート継承やフィルタ (Unix のパイプのように動作します) と呼ばれるものもサポートしています。
Django は
RSS フィードの作成や、ほぼ Python コード無しで web サイトを作ることができるようなジェネリックビューといった、
多くの役に立つ機能をバンドルしています。
  
..
  It has a big, international community which has created many sites using Django.
  There are also quite a lot of add-on projects which extend Django's normal
  functionality.  This is partly due to Django's well written `online
  documentation <http://doc.djangoproject.com/>`_ and the `Django book
  <http://www.djangobook.com/>`_.
  
Django には、Django を利用して多くのサイトを作成してきた
大きく、国際的なコミュニティがあります。
Django の通常の機能を拡張するアドオンプロジェクトもたくさんあります。
この内容の一部は Django の素晴らしい `online documentation <http://doc.djangoproject.com/>`_ と
`Django book <http://www.djangobook.com/>`_ によります。
  
..
  .. note::
  
     Although Django is an MVC-style framework, it calls the components
     differently, which is described in the `Django FAQ
     <http://www.djangoproject.com/documentation/faq/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names>`_.
  
.. note::

   Django は MVC スタイルフレームワークですが、
   Django は構成要素に対して異なる名前で読んでいます、
   このことは `Django FAQ
   <http://www.djangoproject.com/documentation/faq/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names>`_
   に詳しい記述があります。

  
TurboGears
^^^^^^^^^^
  
..
  The other popular web framework in Python is `TurboGears
  <http://www.turbogears.org/>`_.  It takes the approach of using already existing
  components and combining them with glue code to create a seamless experience.
  TurboGears gives the user more flexibility on which components to choose, the
  ORM can be switched between some easy to use but limited and complex but very
  powerful.  Same goes for the template engine.  One strong point about TurboGears
  is that the components that it consists of can be used easily in other projects
  without depending on TurboGears, for example the underlying web server CherryPy.
  
Python の他に人気あるフレームワークは `TurboGears <http://www.turbogears.org/>`_ です。
これは既存の要素と
継ぎ目ををなくすためグルーコードを使って
それらを組み合わせるアプローチをとっています。
TurboGears はユーザが自由に要素を選べるようにしていて、
ORM は制限が多い代わり使いやすいもの、複雑だが強力なもの、に切り替えて使うことができます。
テンプレートエンジンにも同様のことがいえます。
TurboGears の強力な点は、構成要素が他のプロジェクトでも TurboGears への依存無しに
簡単に利用できるということです、例えば TurboGears を支えている web サーバ CherryPy もそうです。

..
  The documentation can be found in the `TurboGears wiki
  <http://docs.turbogears.org/>`_, where links to screencasts can be found.
  TurboGears has also an active user community which can respond to most related
  questions.  There is also a `TurboGears book <http://turbogearsbook.com/>`_
  published, which is a good starting point.

ドキュメントが `TurboGears wiki <http://docs.turbogears.org/>`_ にあり、
スクリーンキャストへのリンクもあります。
TurboGears には関連した質問のほとんどに答えられる、活動的なユーザコミュニティがあります。
入門に向いた `TurboGears book <http://turbogearsbook.com/>`_ も出版されています。

..
  The plan for the next major version of TurboGears, version 2.0 is to switch to a
  more flexible base provided by another very flexible web framework called
  `Pylons <http://pylonshq.com/>`_.

次の TurboGears のメジャーバージョン version 2.0 での計画では、
`Pylons <http://pylonshq.com/>`_ と呼ばれる別の柔軟なフレームワークによって提供される、
より柔軟な基本要素に切り替えることになっています。

..
  Other notable frameworks
  ^^^^^^^^^^^^^^^^^^^^^^^^

他の著名なフレームワーク
^^^^^^^^^^^^^^^^^^^^^^^^
  
..
  These two are of course not the only frameworks that are available, there are
  also some less-popular frameworks worth mentioning.

もちろんこれらの二つだけが利用できるフレームワーク全てではありません、
人気では少し劣りますが、言及するに値するフレームワークがいくつかあります。
  
..
  One of these is the already mentioned Zope, which has been around for quite a
  long time.  With Zope 2.x having been known as rather un-pythonic, the newer
  Zope 3.x tries to change that and therefore gets more acceptance from Python
  programmers.  These efforts already showed results, there is a project which
  connects Zope with WSGI called `Repoze <http://repoze.org/>`_ and another
  project called `Grok <http://grok.zope.org/>`_ which makes it possible for
  "normal" Python programmers use the very mature Zope components.
  
そのうちの一つは既に言及しましたが Zope です、
このフレームワークはずいぶんと長い期間にわたって存在しています。
Zope 2.x はどちらかというと Pythonic でないとされてきましたが、
新しい Zope 3.x ではその変更を試みて、Python プログラマから受け入れられ始めています。
これらの努力は既に結果をみせ始めていて、
`Repoze <http://repoze.org/>`_ と呼ばれる Zope と WSGI を結びつけるプロジェクトや
`Grok <http://grok.zope.org/>`_ と呼ばれる Zope の熟慮された要素を
「普通の」Python プログラマが使えるようにするためのプロジェクトがあります。

..
  Another framework that's already been mentioned is `Pylons`_.  Pylons is much
  like TurboGears with ab even stronger emphasis on flexibility, which is bought
  at the cost of being more difficult to use.  Nearly every component can be
  exchanged, which makes it neccessary to use the documentation of every single
  component, because there are so many Pylons combinations possible that can
  satisfy every requirement.  Pylons builds upon `Paste
  <http://pythonpaste.org/>`_, an extensive set of tools which are handy for WSGI.
  
既に述べた別のフレームワークに `Pylons`_ がありました。
Pylons は TurboGears とよく似ていますが、柔軟性に磨きがかかっていて、
利用するコストが少々高くつきます。
ほとんど全ての要素は交換することができるため、
それぞれの要素について、ドキュメントを利用するこが避けられません、
なぜなら各必要条件を満す Pylons の組み合わせの可能性は本当にたくさんあるのです。
Pylons は WSGI を扱いやすくするための広範囲なツールである、
`Paste <http://pythonpaste.org/>`_ を基にして組まれています。
  
..
  And that's still not everything.  The most up-to-date information can always be
  found in the Python wiki.

これで全てが述べられたわけではありません。
最新の情報の多くは Python wiki で見つけることができます。
  
..
  .. seealso::
  
     The Python wiki contains an extensive list of `web frameworks
     <http://wiki.python.org/moin/WebFrameworks>`_.
  
     Most frameworks also have their own mailing lists and IRC channels, look out
     for these on the projects' websites.  There is also a general "Python in the
     Web" IRC channel on freenode called `#python.web
     <http://wiki.python.org/moin/PoundPythonWeb>`_.

.. seealso::

   Python wiki には広大な `web frameworks <http://wiki.python.org/moin/WebFrameworks>`_ のリストがあります。

   多くのフレームワークは独自のメーリングリストや IRC チャンネルを持っています、
   プロジェクトの web サイトからそれらを探して下さい。
   また、一般的な話題のために "Python in the Web" IRC チャンネルも `#python.web
   <http://wiki.python.org/moin/PoundPythonWeb>`_ と呼ばれる freenode 上にあります。
