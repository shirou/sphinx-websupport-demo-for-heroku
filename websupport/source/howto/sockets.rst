********************************
  ソケットプログラミング HOWTO
********************************

:Author: Gordon McMillan


.. topic:: 概要

   ソケットはそこかしこで使われているが、最大級に誤解されている技術でもある。
   この文書はソケットの全体像を俯瞰しており、チュートリアルとしてはあまり役に立たない。
   実際に動くモノを完成させるには、他にもやらなければいけないことがあるからだ。
   この文書はソケットの微妙なところ (たくさんある) まではカバーしていないが、
   恥ずかしくない使い方ができるようになる程度の情報は得られるはずだ。


ソケット
========

..
   Sockets are used nearly everywhere, but are one of the most severely
   misunderstood technologies around. This is a 10,000 foot overview of sockets.
   It's not really a tutorial - you'll still have work to do in getting things
   working. It doesn't cover the fine points (and there are a lot of them), but I
   hope it will give you enough background to begin using them decently.

ソケットはそこかしこで使われているが、最大級に誤解されている技術でもある。
この文書はソケットの全体像を俯瞰しており、チュートリアルとしてはあまり役に立たない。
実際に動くモノを完成させるには、他にもやらなければいけないことがあるからだ。
この文書はソケットの微妙なところ (たくさんある) まではカバーしていないが、
恥ずかしくない使い方ができるようになる程度の情報は得られるはずだ。

..
   I'm only going to talk about INET sockets, but they account for at least 99% of
   the sockets in use. And I'll only talk about STREAM sockets - unless you really
   know what you're doing (in which case this HOWTO isn't for you!), you'll get
   better behavior and performance from a STREAM socket than anything else. I will
   try to clear up the mystery of what a socket is, as well as some hints on how to
   work with blocking and non-blocking sockets. But I'll start by talking about
   blocking sockets. You'll need to know how they work before dealing with
   non-blocking sockets.

INET ソケットのことしか語らないつもりだが、利用率でいうとソケットの 99% 以上はこれだ。
さらに中でも STREAM ソケットに話題を絞ろうと思う - 自分が何をしているのか分かっているのでない限り
(分かってるならこの HOWTO なんて要らないだろ!)、
STREAM ソケットが一番分かりやすく、一番性能が出るのだ。
そうやって謎に包まれたソケットの正体を明らかにしてゆくと共に、
ブロッキングおよびノンブロッキングなソケットの扱いに関するいくつかのヒントを提示しよう。
だが、まずはブロッキングソケットから始めることにする。
ノンブロッキングを扱うより先に、ブロッキングの仕組みを知っておかなくてはならないのだ。

..
   Part of the trouble with understanding these things is that "socket" can mean a
   number of subtly different things, depending on context. So first, let's make a
   distinction between a "client" socket - an endpoint of a conversation, and a
   "server" socket, which is more like a switchboard operator. The client
   application (your browser, for example) uses "client" sockets exclusively; the
   web server it's talking to uses both "server" sockets and "client" sockets.

話を理解しにくくしている要因として、
「ソケット」という言葉が文脈によって微妙に違うものを指すことが挙げられる。
そこでまず、「クライアント」ソケット - 対話の両端 - と
「サーバ」ソケット - 電話交換手みたいなもの - の区別を付けておこう。
クライアント側アプリケーション (たとえばブラウザ) は「クライアント」ソケットだけを使うが、
話し相手のウェブサーバは「サーバ」ソケットと「クライアント」ソケットの両方を使う。


歴史
----

各種 :abbr:`IPC (Inter Process Communication` (プロセス間通信) の中でも、
ソケットは群を抜いて人気がある。
どのプラットフォームにも、ソケットより速い IPC はあるだろう。
だが、プラットフォームをまたぐ通信はソケットの独擅場だ。

..
   They were invented in Berkeley as part of the BSD flavor of Unix. They spread
   like wildfire with the Internet. With good reason --- the combination of sockets
   with INET makes talking to arbitrary machines around the world unbelievably easy
   (at least compared to other schemes).

ソケットは BSD Unix の一部としてバークレイで発明され、
インターネットの普及と共に野火のごとく広まった。
それももっともなことで、ソケットと INET のコンビによって世界中どんなマシンとも、
信じられないほど簡単 (少なくとも他のスキームと比べて) に通信できるようになったのだ。


ソケットの作成
==============

..
   Roughly speaking, when you clicked on the link that brought you to this page,
   your browser did something like the following::

あなたがリンクをクリックしてこのページに来たとき、
ブラウザは大雑把に言って次のようなことをしたのである::

   #INET の STREAM ソケットを作る
   s = socket.socket(
       socket.AF_INET, socket.SOCK_STREAM)
   #ここでウェブサーバに 80 番 (http の標準) ポートで接続
   s.connect(("www.mcmillan-inc.com", 80))


この ``connect`` が完了すると、ソケット ``s`` を使ってこのページ文章への要求を送ることができるようになる。
その同じソケットが返答を読み、そして破壊される。そう、破壊される。
クライアントソケットは通常、一回 (か少数の) やり取りで使い捨てになるのだ。

ウェブサーバで起こる事柄はもう少し複雑だ。まず「サーバソケット」を作る::

   #INET の STREAM ソケットを作る
   serversocket = socket.socket(
       socket.AF_INET, socket.SOCK_STREAM)
   #そのソケットを公開ホストのウェルノウンポートにつなぐ
   serversocket.bind((socket.gethostname(), 80))
   #サーバソケットになる
   serversocket.listen(5)

..
   A couple things to notice: we used ``socket.gethostname()`` so that the socket
   would be visible to the outside world. If we had used ``s.bind(('', 80))`` or
   ``s.bind(('localhost', 80))`` or ``s.bind(('127.0.0.1', 80))`` we would still
   have a "server" socket, but one that was only visible within the same machine.

ここで注意すべき点がいくつかある:
今回はソケットが外界に見えるよう、 ``socket.gethostname()`` を使った。
``s.bind(('', 80))`` や ``s.bind(('localhost', 80))`` でも「サーバ」ソケットにはなるが、
それだと同じマシン内にしか見えないものになってしまう。

..
   A second thing to note: low number ports are usually reserved for "well known"
   services (HTTP, SNMP etc). If you're playing around, use a nice high number (4
   digits).

ふたつめ: 小さな番号のポートは大抵、「ウェルノウン (有名)」なサービス (HTTP, SNMP 等々) のために取ってある。
お遊びで使うのなら適当に大きな数 (4桁) を使おう。

..
   Finally, the argument to ``listen`` tells the socket library that we want it to
   queue up as many as 5 connect requests (the normal max) before refusing outside
   connections. If the rest of the code is written properly, that should be plenty.

最後に: ``listen`` の引数はソケットライブラリに、
接続要求を 5 個 (通常の最大値) まで順番待ちさせるように命じている。
これ以降の外部接続は拒否するのだが、
コードが適切に書かれていれば、それで十分すぎるほどだ。

..
   OK, now we have a "server" socket, listening on port 80. Now we enter the
   mainloop of the web server::

よし、「サーバーソケット」ができて、80 番ポートで耳を澄ましているところまで来た。
では、ウェブサーバのメインループに入ろう::

   while 1:
       #外からの接続を受け入れる
       (clientsocket, address) = serversocket.accept()
       #ここで clientsocket に何かをする。
       #今回はスレッド化サーバということにしよう
       ct = client_thread(clientsocket)
       ct.run()

..
   There's actually 3 general ways in which this loop could work - dispatching a
   thread to handle ``clientsocket``, create a new process to handle
   ``clientsocket``, or restructure this app to use non-blocking sockets, and
   mulitplex between our "server" socket and any active ``clientsocket``\ s using
   ``select``. More about that later. The important thing to understand now is
   this: this is *all* a "server" socket does. It doesn't send any data. It doesn't
   receive any data. It just produces "client" sockets. Each ``clientsocket`` is
   created in response to some *other* "client" socket doing a ``connect()`` to the
   host and port we're bound to. As soon as we've created that ``clientsocket``, we
   go back to listening for more connections. The two "clients" are free to chat it
   up - they are using some dynamically allocated port which will be recycled when
   the conversation ends.

このループには実際のところ、3 通りの一般的な動作方法がある -
``clientsocket`` を扱うようにスレッドを割り当てたり、
``clientsocket`` を扱う新しいプロセスを作ったり、
あるいはノンブロッキングソケットを使うようにアプリを作り直して ``select`` で
「サーバ」ソケットとアクティブな ``clientsocket`` の間を多重化したりするのだ。
最後のについてはまた後にしよう。ここで理解しておくべき要点はこれだ:
以上が「サーバ」ソケットの仕事の *すべて* である。
データは一切送信しないし、受信しない。「クライアント」ソケットを生み出すだけ。
我々のバインドされているホストとポートに ``connect()`` してくる *他の*
「クライアント」ソケットに応える形で ``clientsocket`` を作り、
作るや否や、さらなる接続を聞きに戻っていくのだ。
このふたつの「クライアント」は、あとは勝手に喋っていればいい -
使うポートは動的に割り当てられ、会話が終わればリサイクルに廻される。


IPC
---

..
   If you need fast IPC between two processes on one machine, you should look into
   whatever form of shared memory the platform offers. A simple protocol based
   around shared memory and locks or semaphores is by far the fastest technique.

同一マシンのプロセス間で高速な IPC が必要なのであれば、
そのプラットフォームが提供している何らかの共有メモリに目を向けるべきだ。
共有メモリとロックやセマフォに基づいた簡素なプロトコルが断然一番速い。

..
   If you do decide to use sockets, bind the "server" socket to ``'localhost'``. On
   most platforms, this will take a shortcut around a couple of layers of network
   code and be quite a bit faster.

ソケットを使うことにしたのであれば、「サーバ」ソケットは
``'localhost'`` にバインドすることだ。こうすると、ほとんどのプラットフォームでは
ネットワーク関連コードを何層かスキップすることになり、かなり速くなる。


ソケットの利用
==============

..
   The first thing to note, is that the web browser's "client" socket and the web
   server's "client" socket are identical beasts. That is, this is a "peer to peer"
   conversation. Or to put it another way, *as the designer, you will have to
   decide what the rules of etiquette are for a conversation*. Normally, the
   ``connect``\ ing socket starts the conversation, by sending in a request, or
   perhaps a signon. But that's a design decision - it's not a rule of sockets.

はじめに憶えておくべきなのは、ウェブブラウザの「クライアント」ソケットと
ウェブサーバの「クライアント」ソケットがまったく同じ種族だということだ。
つまり、これは「ピア・トゥ・ピア」(1 対 1) の会話である。別の言い方をすると、
*設計者として自分で会話のエチケット規則を決めなくてはいけない* ということでもある。
通常は、 ``connect`` してくるソケットが要求あるいは宣言をして会話を始める。
だが、それはそう設計しただけのことだ - ソケットの規則ではない。

..
   Now there are two sets of verbs to use for communication. You can use ``send``
   and ``recv``, or you can transform your client socket into a file-like beast and
   use ``read`` and ``write``. The latter is the way Java presents their sockets.
   I'm not going to talk about it here, except to warn you that you need to use
   ``flush`` on sockets. These are buffered "files", and a common mistake is to
   ``write`` something, and then ``read`` for a reply. Without a ``flush`` in
   there, you may wait forever for the reply, because the request may still be in
   your output buffer.

さて、コミュニケーションに使う動詞は二組ある。 ``send`` と ``recv`` を使うこともできるし、
クライアントソケットをファイルっぽい種族に変形して ``read`` と ``write`` を使っても良い。
後者は Java のソケットの表現方法だ。ここで詳しく語るつもりはないが、
その場合はソケットも ``flush`` しなければいけない、とだけ言っておく。
これはバッファリングした「ファイル」なので、何かを
``write`` してすぐに返答を ``read`` するというのはよくある間違いだ。
間に ``flush`` を入れないと、要求がまだ出力バッファにあって永遠に返事が来ない、という可能性がある。

..
   Now we come the major stumbling block of sockets - ``send`` and ``recv`` operate
   on the network buffers. They do not necessarily handle all the bytes you hand
   them (or expect from them), because their major focus is handling the network
   buffers. In general, they return when the associated network buffers have been
   filled (``send``) or emptied (``recv``). They then tell you how many bytes they
   handled. It is *your* responsibility to call them again until your message has
   been completely dealt with.

さあ、ソケットの主要な難関に進もう -
``send`` と ``recv`` はネットワークバッファに働きかけるものだ。だから、
手渡したもの (や返してもらいたいもの) を 1 バイトも残さず実際に処理してくれているとは限らない。
一般的に言って、 ``send`` はバッファが埋まったとき、
``recv`` はバッファが空になったときに実際の処理をして、そのバイト数を返す。
メッセージが完全に処理されるまでコールを繰り返すのは *自分の* 責任なのだ。

..
   When a ``recv`` returns 0 bytes, it means the other side has closed (or is in
   the process of closing) the connection.  You will not receive any more data on
   this connection. Ever.  You may be able to send data successfully; I'll talk
   about that some on the next page.

``recv`` が 0 バイトを返したときは、向こう側が接続を閉じてしまった (または閉じようとしている途中) という意味だ。
もうこの接続でデータを受け取ることはない。永遠にだ。
ただ、データ送信は成功するかもしれない; これについては次のページで語ることにしよう。

..
   A protocol like HTTP uses a socket for only one transfer. The client sends a
   request, the reads a reply.  That's it. The socket is discarded. This means that
   a client can detect the end of the reply by receiving 0 bytes.

HTTP のようなプロトコルでは、ひとつのソケットを1回の転送にしか使わない。
クライアントは要求を送り、返答を受ける。以上だ。これでソケットは破棄される。
だからこの場合、クライアントは受信 0 バイトの時点で返答の末尾を検出することができる。

..
   But if you plan to reuse your socket for further transfers, you need to realize
   that *there is no "EOT" (End of Transfer) on a socket.* I repeat: if a socket
   ``send`` or ``recv`` returns after handling 0 bytes, the connection has been
   broken.  If the connection has *not* been broken, you may wait on a ``recv``
   forever, because the socket will *not* tell you that there's nothing more to
   read (for now).  Now if you think about that a bit, you'll come to realize a
   fundamental truth of sockets: *messages must either be fixed length* (yuck), *or
   be delimited* (shrug), *or indicate how long they are* (much better), *or end by
   shutting down the connection*. The choice is entirely yours, (but some ways are
   righter than others).

だが、以降の転送にもそのソケットを使い回すつもりなら、
ソケットに "EOT" (End of Transfer) など *存在しない* ことを認識する必要がある。
もう一度言おう: ソケットの ``send`` や ``recv`` が 0 バイト処理で返ってきたなら、その接続は終わっている。
終わって *いない* なら、いつまで ``recv`` を待てばいいかは分からない。
ソケットは「もう読むものが (今のところ) ないぜ」などと *言わない* のだから。
このことを少し考えれば、ソケットの真実を悟ることになるだろう:
*メッセージは必ず固定長か* (うげぇ) *区切り文字を使うか* (やれやれ)
*長さ標識を付けておくか* (かなりマシ)
*接続を閉じて終わらせるかのいずれかでなければいけない* のだ。
選ぶ権利と責任はまったくもって自分にある (が、正しさの程度に違いはある)。

..
   Assuming you don't want to end the connection, the simplest solution is a fixed
   length message::

毎回接続を終わらせるのはイヤだとして、
最も単純な解決策は固定長メッセージだろう::

   class mysocket:
       '''demonstration class only
         - coded for clarity, not efficiency
       '''

       def __init__(self, sock=None):
            if sock is None:
                self.sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.sock = sock

       def connect(self, host, port):
            self.sock.connect((host, port))

       def mysend(self, msg):
            totalsent = 0
            while totalsent < MSGLEN:
                sent = self.sock.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent

       def myreceive(self):
            msg = ''
            while len(msg) < MSGLEN:
                chunk = self.sock.recv(MSGLEN-len(msg))
                if chunk == '':
                    raise RuntimeError("socket connection broken")
                msg = msg + chunk
            return msg

..
   The sending code here is usable for almost any messaging scheme - in Python you
   send strings, and you can use ``len()`` to determine its length (even if it has
   embedded ``\0`` characters). It's mostly the receiving code that gets more
   complex. (And in C, it's not much worse, except you can't use ``strlen`` if the
   message has embedded ``\0``\ s.)

この送信コードは、ほぼあらゆるメッセージ通信スキームで使える -
文字列を送るとき、Python なら長さを ``len()`` で見極めることができる
(中に ``\0`` が埋め込まれていても大丈夫)。
難しくしているのは、おもに受信コードである。
(なお、C でも事態はあまり悪くならないが、メッセージに ``\0`` が埋め込まれていると
``strlen`` が使えないのは面倒だ。)

..
   The easiest enhancement is to make the first character of the message an
   indicator of message type, and have the type determine the length. Now you have
   two ``recv``\ s - the first to get (at least) that first character so you can
   look up the length, and the second in a loop to get the rest. If you decide to
   go the delimited route, you'll be receiving in some arbitrary chunk size, (4096
   or 8192 is frequently a good match for network buffer sizes), and scanning what
   you've received for a delimiter.

最も簡単な改良法は、メッセージの最初の一文字をタイプ標識にして、
そのタイプで長さを決定するというものだ。この場合ふたつの ``recv`` があることになる -
一番目でその一文字 (だけじゃなくても可) を取って長さを調べ、
二番目でループして残りを取るのだ。
あるいはもし区切り方式の道を行くのであれば、任意のサイズ
(4096 か 8192 がネットワークバッファには最適なことが多い) で
受信して区切り文字を走査していくことになる。

..
   One complication to be aware of: if your conversational protocol allows multiple
   messages to be sent back to back (without some kind of reply), and you pass
   ``recv`` an arbitrary chunk size, you may end up reading the start of a
   following message. You'll need to put that aside and hold onto it, until it's
   needed.

心に留めておくべき面倒な点がひとつ: 複数メッセージが次々に (何らかの返事を待たずに)
返ってくることのある会話プロトコルなら、そして任意のサイズを
``recv`` に渡しているなら、次のメッセージの冒頭部分まで読んでしまうことがあるかもしれない。
そのときは、必要になるまで脇によけて、大切に保管しておく必要がある。

..
   Prefixing the message with it's length (say, as 5 numeric characters) gets more
   complex, because (believe it or not), you may not get all 5 characters in one
   ``recv``. In playing around, you'll get away with it; but in high network loads,
   your code will very quickly break unless you use two ``recv`` loops - the first
   to determine the length, the second to get the data part of the message. Nasty.
   This is also when you'll discover that ``send`` does not always manage to get
   rid of everything in one pass. And despite having read this, you will eventually
   get bit by it!

メッセージ冒頭に長さを (たとえば 5 桁の数字で) 付けるのは、
それよりもさらに複雑になる。というのも、(信じられないかもしれないが)
一回の ``recv`` で 5 文字を全部受け取ることができるとは限らないからだ。
お遊びでやっている間はごまかせても、高負荷ネットワークのもとでは、
``recv`` ループをふたつ使わないコードは、あっと言う間にダメになってしまう -
一番目は長さを見定める用で、二番目はデータ部分を受け取る用だ。うーむ、いやらしい。
さらにこのとき、 ``send`` も一発で全部を出し切れるとは限らないことに気付くだろう。
なお、今こうやって読んでいても、いつか誰もが痛い目を見るのである!

..
   In the interests of space, building your character, (and preserving my
   competitive position), these enhancements are left as an exercise for the
   reader. Lets move on to cleaning up.

紙面の都合および教育的配慮 (と著者の地位確保)
のため、こうした改良は練習問題として残しておく。さあ片付けてしまおう。


バイナリデータ
--------------

..
   It is perfectly possible to send binary data over a socket. The major problem is
   that not all machines use the same formats for binary data. For example, a
   Motorola chip will represent a 16 bit integer with the value 1 as the two hex
   bytes 00 01. Intel and DEC, however, are byte-reversed - that same 1 is 01 00.
   Socket libraries have calls for converting 16 and 32 bit integers - ``ntohl,
   htonl, ntohs, htons`` where "n" means *network* and "h" means *host*, "s" means
   *short* and "l" means *long*. Where network order is host order, these do
   nothing, but where the machine is byte-reversed, these swap the bytes around
   appropriately.

バイナリデータはまったく問題なくソケットに乗せられる。問題は、
すべてのマシンで同じ形式を使っているわけではないことにある。
たとえば Motorola のチップなら 16 ビット整数の 1 という値をふたつの
16 進バイト列 00 01 で表現するが、Intel や DEC は逆バイトだ -
同じ 1 が 01 00 になるのだ。ソケットライブラリは 16 ビットや
32 ビット整数の変換用コールを持っている - ``ntohl, htonl,
ntohs, htons`` である。"n" は *network*\ 、 "h" は *host* を意味する。
"s" は *short* で "l" は *long* だ。これらのコールは、
「ネットワーク並び = ホスト並び」なら何もしないが、
マシンが逆バイトならそれに合わせてぐるっと交換してくれる。

..
   In these days of 32 bit machines, the ascii representation of binary data is
   frequently smaller than the binary representation. That's because a surprising
   amount of the time, all those longs have the value 0, or maybe 1. The string "0"
   would be two bytes, while binary is four. Of course, this doesn't fit well with
   fixed-length messages. Decisions, decisions.

この 32 ビット時代、バイナリデータは ASCII 表現のほうが小さくなることが多い。
というのも、long なのに値が 0 ばっかりでたまに 1 だとかいうことは驚くほど多いからだ。
文字列なら "0" は 2 バイトなのに、バイナリは 4 バイトも喰う。
もちろんこれは固定長メッセージには合わないが。さあ、どうする、どうする。


切断
====

..
   Strictly speaking, you're supposed to use ``shutdown`` on a socket before you
   ``close`` it.  The ``shutdown`` is an advisory to the socket at the other end.
   Depending on the argument you pass it, it can mean "I'm not going to send
   anymore, but I'll still listen", or "I'm not listening, good riddance!".  Most
   socket libraries, however, are so used to programmers neglecting to use this
   piece of etiquette that normally a ``close`` is the same as ``shutdown();
   close()``.  So in most situations, an explicit ``shutdown`` is not needed.

厳密には、ソケットを ``close`` する前には ``shutdown`` する
ことになっている。 ``shutdown`` は相手ソケットに対する報告であり、
渡す引数によって「これ以上こっちからは送らないけど、まだ聞いてるぜ」
という意味になったり、「もう聞かない。せいせいした!」だったりする。
しかしほとんどのソケットライブラリは、
このエチケットを怠るプログラマに慣れてしまって、通常 ``close`` だけで
``shutdown(); close()`` と同じことになる。だから大抵はわざわざ
``shutdown`` しなくてもいい。

..
   One way to use ``shutdown`` effectively is in an HTTP-like exchange. The client
   sends a request and then does a ``shutdown(1)``. This tells the server "This
   client is done sending, but can still receive."  The server can detect "EOF" by
   a receive of 0 bytes. It can assume it has the complete request.  The server
   sends a reply. If the ``send`` completes successfully then, indeed, the client
   was still receiving.

``shutdown`` の効果的な使い方のひとつは、HTTP 風のやりとりだ。
クライアントは要求を出してすぐに ``shutdown(1)`` する。これでサーバに、
「クライアントは送信完了ですが、まだ受信可能です」と伝わる。
サーバは 0 バイト受信で "EOF" を検出することができる。
要求を残さず受け取ったことにして良いのだ。対してサーバは返答を送る。
その ``send`` が成功したなら、クライアントは実際にまだ受信していたことになる。

..
   Python takes the automatic shutdown a step further, and says that when a socket
   is garbage collected, it will automatically do a ``close`` if it's needed. But
   relying on this is a very bad habit. If your socket just disappears without
   doing a ``close``, the socket at the other end may hang indefinitely, thinking
   you're just being slow. *Please* ``close`` your sockets when you're done.

Python はこの自動 shutdown をもう一歩進めて、ソケットが GC
されるときに必要なら自動で ``close`` してくれると言っている。
しかしこれに頼るクセをつけてはいけない。もしソケットが ``close`` せずに姿を消せば、
相手ソケットはこちらが遅いだけだと思ってハングしてしまうかもしれない。
*お願いだから* 終わったらちゃんと ``close`` してくれ。


ソケットが死ぬと
----------------

..
   Probably the worst thing about using blocking sockets is what happens when the
   other side comes down hard (without doing a ``close``). Your socket is likely to
   hang. SOCKSTREAM is a reliable protocol, and it will wait a long, long time
   before giving up on a connection. If you're using threads, the entire thread is
   essentially dead. There's not much you can do about it. As long as you aren't
   doing something dumb, like holding a lock while doing a blocking read, the
   thread isn't really consuming much in the way of resources. Do *not* try to kill
   the thread - part of the reason that threads are more efficient than processes
   is that they avoid the overhead associated with the automatic recycling of
   resources. In other words, if you do manage to kill the thread, your whole
   process is likely to be screwed up.

ブロッキングソケットを使っていて一番いやなのは多分、
相手側が意地悪く (``close`` せずに) ダウンするときに起こる事柄だ。
自分側のソケットは高確率でハングするだろう。SOCKSTREAM は信頼性の高いプロトコルなので、
ずっとずっと待ち続けて、なかなか見捨てないのだ。スレッドを使っているのであれば、
そのスレッド全体が根本から死んだ状態になる。こうなると、もう手の施しようがない。
まあ、ブロッキング読み出しの間ロックし続けるといった馬鹿げたことをしていない限り、
リソースの点ではたいして消費にならない。だから *ぜったいに* そのスレッドを
殺そうとしてはいけない - プロセスよりスレッドが効率的である理由のひとつは、
自動リソース回収にまつわるオーバヘッドを避けられるという点にあるのだ。
つまり別の言い方をすると、どうにかしてそのスレッドを殺したなら、
プロセス全体がぐちゃぐちゃになってしまうだろうということだ。


ノンブロッキングソケット
========================

..
   If you've understood the preceeding, you already know most of what you need to
   know about the mechanics of using sockets. You'll still use the same calls, in
   much the same ways. It's just that, if you do it right, your app will be almost
   inside-out.

ここまで理解してきたなら、もうソケットの仕組みについて必要なことはほとんど知っていることになる。
これからも同じコールを、ほぼ同じように使っていくだけ、それだけだ。
これをちゃんとやっていれば、そのアプリはだいたい完璧であろう。

..
   In Python, you use ``socket.setblocking(0)`` to make it non-blocking. In C, it's
   more complex, (for one thing, you'll need to choose between the BSD flavor
   ``O_NONBLOCK`` and the almost indistinguishable Posix flavor ``O_NDELAY``, which
   is completely different from ``TCP_NODELAY``), but it's the exact same idea. You
   do this after creating the socket, but before using it. (Actually, if you're
   nuts, you can switch back and forth.)

Python の場合、ノンブロッキングにするには ``socket.setblocking(0)`` を使う。
C ならもっと複雑だ (一例を挙げると、BSD 方式の ``O_NONBLOCK`` およびほぼ違いのない
POSIX 方式 ``O_NDELAY`` のどちらを選ぶか決めなくてはならなくて、後者は
``TCP_NODELAY`` とは全然別物だったりする) が、考え方はまったく一緒だ。

..
   The major mechanical difference is that ``send``, ``recv``, ``connect`` and
   ``accept`` can return without having done anything. You have (of course) a
   number of choices. You can check return code and error codes and generally drive
   yourself crazy. If you don't believe me, try it sometime. Your app will grow
   large, buggy and suck CPU. So let's skip the brain-dead solutions and do it
   right.

構造上の大きな違いは、 ``send``, ``recv``, ``connect``, ``accept``
が何もしないで戻ってくるかもしれないという点である。
選択肢は (当然ながら) いくつかある。
返り値とエラーコードをチェックするという方法もある。が、発狂すること請け合いだ。
信じないなら、いつかやってみるといい。
アプリは肥大化し、バグが増え、CPU を喰い尽くすだろう。
だからそんな愚かな解法は飛ばして、正解に進もう。

..
   Use ``select``.

``select`` を使え。

..
   In C, coding ``select`` is fairly complex. In Python, it's a piece of cake, but
   it's close enough to the C version that if you understand ``select`` in Python,
   you'll have little trouble with it in C. ::

C において ``select`` でコードを書くのはかなり面倒だが、Python
なら造作もない。しかし Python で ``select`` を理解しておけば
C でもほとんど問題なく書ける、という程度には似ている::

   readable, writable, in_error = \
                  select.select(
                     potential_readers,
                     potential_writers,
                     potential_errs,
                     timeout)

..
   You pass ``select`` three lists: the first contains all sockets that you might
   want to try reading; the second all the sockets you might want to try writing
   to, and the last (normally left empty) those that you want to check for errors.
   You should note that a socket can go into more than one list. The ``select``
   call is blocking, but you can give it a timeout. This is generally a sensible
   thing to do - give it a nice long timeout (say a minute) unless you have good
   reason to do otherwise.

``select`` に三つのリストを渡しているが、
一番目にはあとで読みたくなるかもしれないソケットすべて、
二番目には書き込みたくなるかもしれないソケットすべて、
最後に (通常は空のままだが) エラーをチェックしたいソケットが入っている。
ひとつのソケットが複数にまたがってリストされても構わないことを憶えておくと良い。
なお、 ``select`` コールはブロックするが、時間制限を与えることができる。
これは、やっておいて損はない - 特に理由がなければ、
かなり長い (たとえば 1 分とかの) 時間制限を付けておくことだ。

戻り値として、三つのリストが手に入る。
それぞれには、実際に読めるソケット、書けるソケット、エラー中のソケットが入っていて、
渡したリストの部分集合 (空集合かもしれない) になっている。

..
   If a socket is in the output readable list, you can be
   as-close-to-certain-as-we-ever-get-in-this-business that a ``recv`` on that
   socket will return *something*. Same idea for the writable list. You'll be able
   to send *something*. Maybe not all you want to, but *something* is better than
   nothing.  (Actually, any reasonably healthy socket will return as writable - it
   just means outbound network buffer space is available.)

出力のうち、readable リストにあるソケットについては、
``recv`` がとりあえず *何か* を返すであろう、ということは史上最高度に確信できる。
writable リストも考え方は同じで、 *何か* は送れる。
送りたいもの全体は無理かもしれないが、 *何も* ないよりはマシだろう。
(実のところ、ふつうに健康なソケットなら writable で返ってくることができる -
それは外向きネットワークバッファに空きがあるというだけの意味しかないのだから)

..
   If you have a "server" socket, put it in the potential_readers list. If it comes
   out in the readable list, your ``accept`` will (almost certainly) work. If you
   have created a new socket to ``connect`` to someone else, put it in the
   potential_writers list. If it shows up in the writable list, you have a decent
   chance that it has connected.

「サーバ」ソケットは potential_readers リストに入れておこう。
それが readable リストに入って出てきたら、 ``accept`` は (ほぼ) 確実に成功するはずだ。
どこかへ ``connect`` するために作った新しいソケットは potential_writers リストに入れる。
それが writable リストに現れたら、接続が成功している可能性は高いと言える。

..
   One very nasty problem with ``select``: if somewhere in those input lists of
   sockets is one which has died a nasty death, the ``select`` will fail. You then
   need to loop through every single damn socket in all those lists and do a
   ``select([sock],[],[],0)`` until you find the bad one. That timeout of 0 means
   it won't take long, but it's ugly.

``select`` の実にいやらしい問題がひとつ:
突然死したソケットが入力側リストのどこかにあれば、 ``select`` は失敗してしまう。
そうなると、見つけるまですべてのリストでループしてソケットをひとつひとつ
``select([sock],[],[],0)`` していく必要がある。
時間制限を 0 にしてあるので長くはかからないが、これは美しくない。

..
   Actually, ``select`` can be handy even with blocking sockets. It's one way of
   determining whether you will block - the socket returns as readable when there's
   something in the buffers.  However, this still doesn't help with the problem of
   determining whether the other end is done, or just busy with something else.

じつは ``select`` はブロッキングソケットにも便利に使える。
それはブロックするかどうかを見極める方法のひとつである -
バッファに何かがあれば readable として返ってくるのだ。
しかしこれも、相手の用事がもう済んでいるのか、
それとも単に他のことで忙しいだけなのかを見極める役には立たない。

..
   **Portability alert**: On Unix, ``select`` works both with the sockets and
   files. Don't try this on Windows. On Windows, ``select`` works with sockets
   only. Also note that in C, many of the more advanced socket options are done
   differently on Windows. In fact, on Windows I usually use threads (which work
   very, very well) with my sockets. Face it, if you want any kind of performance,
   your code will look very different on Windows than on Unix.

**非互換警報**: Unix ではソケットにもファイルにも ``select`` が使える。
これを Windows でやろうとしてはいけない。Windows で ``select`` はソケットにしか使えない。
また C の場合、高度なソケットオプションの多くは、やり方が Windows では違っている。
実際、Windows なら著者は通常、ソケットにスレッドを使っている (これは実に、実にうまくいく)。
認めたくないが、何らかの性能を求めるなら Windows のコードは
Unix のコードとはかなり異なるものになってしまうだろう。


性能
----

..
   There's no question that the fastest sockets code uses non-blocking sockets and
   select to multiplex them. You can put together something that will saturate a
   LAN connection without putting any strain on the CPU. The trouble is that an app
   written this way can't do much of anything else - it needs to be ready to
   shuffle bytes around at all times.

最速のソケットコードはノンブロッキングソケットを使って
select で多重化するものだということに疑問の余地はない。
CPU に負荷をかけることなく LAN 接続を使いきるアプリは作れる。
問題は、そうやって書かれたものはあまり他のことができなくなるということだ -
いつでもデータをあちらこちらへ廻せるようにしている必要があるのだ。

..
   Assuming that your app is actually supposed to do something more than that,
   threading is the optimal solution, (and using non-blocking sockets will be
   faster than using blocking sockets). Unfortunately, threading support in Unixes
   varies both in API and quality. So the normal Unix solution is to fork a
   subprocess to deal with each connection. The overhead for this is significant
   (and don't do this on Windows - the overhead of process creation is enormous
   there). It also means that unless each subprocess is completely independent,
   you'll need to use another form of IPC, say a pipe, or shared memory and
   semaphores, to communicate between the parent and child processes.

もっと他にやることがあるアプリなのだとすれば、スレッドが最適解だ
(さらにノンブロッキングソケットを使えばブロッキングより速い)。
しかし残念ながら、各種 Unix のスレッド対応は API も品質もバラバラである。
そのため Unix の一般解は、それぞれの接続を取り扱う子プロセスをフォークするというものだ。
このオーバヘッドは甚大 (Windows ではプロセス生成のオーバヘッドが洒落にならないので無理) だ。
それに、子プロセスがお互い完全に独立しているのでない限り、
親子のプロセス間で通信するために他の IPC, たとえばパイプとか、
共有メモリとセマフォだとかを使う必要が出てくる。

..
   Finally, remember that even though blocking sockets are somewhat slower than
   non-blocking, in many cases they are the "right" solution. After all, if your
   app is driven by the data it receives over a socket, there's not much sense in
   complicating the logic just so your app can wait on ``select`` instead of
   ``recv``.

最後に、これを憶えておいてほしい。
ブロッキングソケットはノンブロッキングよりも幾分遅いとはいえ、
多くの場合そちらが「正解」である。
結局のところ、ソケットから受け取るデータに基づいて動くアプリなら、
``recv`` のかわりに ``select`` で待てるようにするためだけにロジックを複雑化する意味はあまりない。

