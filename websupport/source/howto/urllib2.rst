************************************************************
  urllib2 を使ってインターネット上のリソースを取得するには
************************************************************
..
  ******************************************************
    HOWTO Fetch Internet Resources Using urllib2 (英語)
  ******************************************************

:Author: `Michael Foord <http://www.voidspace.org.uk/python/index.shtml>`_

..
  .. note::
  
      There is an French translation of an earlier revision of this
      HOWTO, available at `urllib2 - Le Manuel manquant
      <http://www.voidspace.org.uk/python/articles/urllib2_francais.shtml>`_.

.. note::

    この HOWTO の前段階の版のフランス語訳が
    `urllib2 - Le Manuel manquant
    <http://www.voidspace.org.uk/python/articles/urllib2_francais.shtml>`_
    で入手できます。

..
  Introduction
  ============

はじめに
========

..
  .. sidebar:: Related Articles
  
      You may also find useful the following article on fetching web resources
      with Python :
  
      * `Basic Authentication <http://www.voidspace.org.uk/python/articles/authentication.shtml>`_
  
          A tutorial on *Basic Authentication*, with examples in Python.

.. sidebar:: 関連する記事

    同じように Python でインターネットリソースを取得するのに以下の記事が役に立ちます:

    * `Basic Authentication <http://www.voidspace.org.uk/python/articles/authentication.shtml>`_

        *Basic 認証* についてのチュートリアルで Python の例がついています。

..
  **urllib2** is a `Python <http://www.python.org>`_ module for fetching URLs
  (Uniform Resource Locators). It offers a very simple interface, in the form of
  the *urlopen* function. This is capable of fetching URLs using a variety of
  different protocols. It also offers a slightly more complex interface for
  handling common situations - like basic authentication, cookies, proxies and so
  on. These are provided by objects called handlers and openers.

**urllib2** は URLs (Uniform Resource Locators) を取得するための
`Python <http://www.python.org>`_ モジュールです。
このモジュールはとても簡単なインターフェースを *urlopen* 関数の形式で
提供しています。
また、このモジュールは一般的な状況で利用するために
いくらか複雑なインターフェースも提供しています
- basic 認証やクッキー、プロキシ等。
これらは handler や opener と呼ばれる
オブジェクトとして提供されます。

..
  urllib2 supports fetching URLs for many "URL schemes" (identified by the string
  before the ":" in URL - for example "ftp" is the URL scheme of
  "ftp://python.org/") using their associated network protocols (e.g. FTP, HTTP).
  This tutorial focuses on the most common case, HTTP.

urllib2 は多くの "URL スキーム" (URL の ":" の前の文字列で識別されるもの
- 例えば "ftp://python.org/" では "ftp") の URL を、関連する
ネットワークプロトコル(例えば FTP, HTTP) を利用することで、取得できます。

..
  For straightforward situations *urlopen* is very easy to use. But as soon as you
  encounter errors or non-trivial cases when opening HTTP URLs, you will need some
  understanding of the HyperText Transfer Protocol. The most comprehensive and
  authoritative reference to HTTP is :rfc:`2616`. This is a technical document and
  not intended to be easy to read. This HOWTO aims to illustrate using *urllib2*,
  with enough detail about HTTP to help you through. It is not intended to replace
  the :mod:`urllib2` docs, but is supplementary to them.

単純な状況では *urlopen* はとても簡単に使うことができます。
しかし HTTP の URL を開くときにエラーが起きたり、特殊なケースに遭遇すると、
HyperText Transfer Protocol に関するいくつかのことを理解する必要があります。
HTTP に関して最も包括的で信頼できる文献は :rfc:`2616` です。
この文書は技術文書なので簡単には読めません。
この HOWTO の目的は *urllib2* の利用法を例示することです、
HTTP についてはその助けになるのに十分に詳しく載せています。
このドキュメントは :mod:`urllib2` のドキュメントの代わりにはなりませんが、
補完する役割を持っています。

..
  Fetching URLs
  =============

URL を取得する
==============

..
  The simplest way to use urllib2 is as follows::

urllib2 を利用する最も簡単な方法は以下です::

    import urllib2
    response = urllib2.urlopen('http://python.org/')
    html = response.read()

..
  Many uses of urllib2 will be that simple (note that instead of an 'http:' URL we
  could have used an URL starting with 'ftp:', 'file:', etc.).  However, it's the
  purpose of this tutorial to explain the more complicated cases, concentrating on
  HTTP.

多くの urllib2 の利用法はこのように簡単です ('http:' の代わりに URL を
'ftp:' や 'file:' 等で始めればできます。)。
しかし、このチュートリアルの目的は、得に HTTP に絞って、
より複雑な状況を説明することです。

..
  HTTP is based on requests and responses - the client makes requests and servers
  send responses. urllib2 mirrors this with a ``Request`` object which represents
  the HTTP request you are making. In its simplest form you create a Request
  object that specifies the URL you want to fetch. Calling ``urlopen`` with this
  Request object returns a response object for the URL requested. This response is
  a file-like object, which means you can for example call ``.read()`` on the
  response::

HTTP はリクエスト (request) とレスポンス (response) が基本となっています
- クライアントがリクエストし、サーバーがレスポンスを送ります。
urllib2 はこれを真似て、作成する HTTP リクエストを表現する
``Request`` オブジェクトを備えています。
リクエストオブジェクトを作成する最も簡単な方法は
取得したい URL を指定することです。
``urlopen`` をこのオブジェクトを使って呼び出すと、リクエストした URL の
レスポンスオブジェクトが返されます。
このレスポンスはファイルライクオブジェクトで、これはつまりレスポンスに ``.read()``
と呼び出せることを意味しています::

    import urllib2

    req = urllib2.Request('http://www.voidspace.org.uk')
    response = urllib2.urlopen(req)
    the_page = response.read()

..
  Note that urllib2 makes use of the same Request interface to handle all URL
  schemes.  For example, you can make an FTP request like so::

urllib2 は同じリクエストインターフェースを全ての URL スキームに対して
利用できるようにしています。
例えば、FTP リクエストの場合はこうできます::

    req = urllib2.Request('ftp://example.com/')

..
  In the case of HTTP, there are two extra things that Request objects allow you
  to do: First, you can pass data to be sent to the server.  Second, you can pass
  extra information ("metadata") *about* the data or the about request itself, to
  the server - this information is sent as HTTP "headers".  Let's look at each of
  these in turn.

HTTP の場合には、リクエストオブジェクトに対して二つの特別な操作ができます:
一つ目はサーバーに送るデータを渡すことができる、二つ目はサーバーに送るデータや
リクエスト自身に *ついての* 特別な情報 ("metadata")を渡すことができます
- これらの送られる情報は HTTP 「ヘッダ」です。
今度はこれらに関してひとつひとつ見ていきましょう。


..
  Data
  ----

データ
------

..
  Sometimes you want to send data to a URL (often the URL will refer to a CGI
  (Common Gateway Interface) script [#]_ or other web application). With HTTP,
  this is often done using what's known as a **POST** request. This is often what
  your browser does when you submit a HTML form that you filled in on the web. Not
  all POSTs have to come from forms: you can use a POST to transmit arbitrary data
  to your own application. In the common case of HTML forms, the data needs to be
  encoded in a standard way, and then passed to the Request object as the ``data``
  argument. The encoding is done using a function from the ``urllib`` library
  *not* from ``urllib2``. ::

URL にデータを送りたい場合はよくあります
(しばしば、その URL は CGI (Common Gateway Interface) スクリプト [#]_ や
他の web アプリケーションを参照することになります)。
これは HTTP では、 **POST** リクエストとして知られる方法で行なわれます。
これは web 上で HTML フォームを埋めて送信するときにブラウザが
行なっていることです。
全ての POST がフォームから送られるとは限りません:
自身のアプリケーションに対して任意のデータを POST を使って送ることができます。
一般的な HTML フォームの場合、データは標準的な方法でエンコードされている必要があり、
リクエストオブジェクトに ``data`` 引数として渡します。
エンコーディングは ``urllib2`` からではなく、 ``urllib`` ライブラリの関数を
使って行います::

    import urllib
    import urllib2

    url = 'http://www.someserver.com/cgi-bin/register.cgi'
    values = {'name' : 'Michael Foord',
              'location' : 'Northampton',
              'language' : 'Python' }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

..
  Note that other encodings are sometimes required (e.g. for file upload from HTML
  forms - see `HTML Specification, Form Submission
  <http://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13>`_ for more
  details).

他のエンコーディングが必要な場合があることに注意して下さい (例えば、
HTML フォームからファイルをアップロードするための詳細については
`HTML Specification, Form Submission
<http://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13>`_ を見て下さい

..
  If you do not pass the ``data`` argument, urllib2 uses a **GET** request. One
  way in which GET and POST requests differ is that POST requests often have
  "side-effects": they change the state of the system in some way (for example by
  placing an order with the website for a hundredweight of tinned spam to be
  delivered to your door).  Though the HTTP standard makes it clear that POSTs are
  intended to *always* cause side-effects, and GET requests *never* to cause
  side-effects, nothing prevents a GET request from having side-effects, nor a
  POST requests from having no side-effects. Data can also be passed in an HTTP
  GET request by encoding it in the URL itself.

``data`` 引数を渡さない場合、urllib2 は **GET** リクエストを利用します。
GET と POST リクエストの一つの違いは、POST リクエストにしばしば、
「副作用」があることです:
POST リクエストはいくつかの方法によってシステムの状態を変化させます
(例えば100ポンドのスパムの缶詰をドアの前まで配達する注文を web サイトで行う)。
とはいえ HTTP 標準で明確にされている内容では、POST は *常に* 副作用を持ち、
GET リクエストが副作用を持つことを禁止していません、
副作用の無い POST リクエストはありません。
HTTP の GET リクエストでもデータ自身をエンコーディングすることで
データを渡すことができます。

..
  This is done as follows::

以下のようにして行います::

    >>> import urllib2
    >>> import urllib
    >>> data = {}
    >>> data['name'] = 'Somebody Here'
    >>> data['location'] = 'Northampton'
    >>> data['language'] = 'Python'
    >>> url_values = urllib.urlencode(data)
    >>> print url_values
    name=Somebody+Here&language=Python&location=Northampton
    >>> url = 'http://www.example.com/example.cgi'
    >>> full_url = url + '?' + url_values
    >>> data = urllib2.open(full_url)

..
  Notice that the full URL is created by adding a ``?`` to the URL, followed by
  the encoded values.

``?`` を URL に加え、それにエンコードされた値が続くことで、
完全な URL が 作られていることに注意して下さい。

..
  Headers
  -------

ヘッダ
------

..
  We'll discuss here one particular HTTP header, to illustrate how to add headers
  to your HTTP request.

ここでは特定の HTTP ヘッダについて議論します、
HTTP リクエストにヘッダを追加する方法について例示します。

..
  Some websites [#]_ dislike being browsed by programs, or send different versions
  to different browsers [#]_ . By default urllib2 identifies itself as
  ``Python-urllib/x.y`` (where ``x`` and ``y`` are the major and minor version
  numbers of the Python release,
  e.g. ``Python-urllib/2.5``), which may confuse the site, or just plain
  not work. The way a browser identifies itself is through the
  ``User-Agent`` header [#]_. When you create a Request object you can
  pass a dictionary of headers in. The following example makes the same
  request as above, but identifies itself as a version of Internet
  Explorer [#]_. ::

いくつかの web サイト [#]_ はプログラムからブラウズされることを嫌っていたり、
異なるブラウザに対して異なるバージョンのブラウザに送ります [#]_ 。
デフォルトでは urllib2 は自身の情報を ``Python-urllib/x.y`` として扱います
(``x`` と ``y`` は Python のリリースバージョンのメジャーバージョン、
マイナーバージョンです、例えば ``Python-urllib/2.5`` など)、
これによって web サイト側が混乱したり、動作しないかもしれません。
ブラウザは自身の情報を ``User-Agent`` ヘッダ [#]_ を通して扱っています。
リクエストオブジェクトを作るときに、ヘッダに辞書を渡すことができます。
以下の例は上の例と同じですが、自身を Internet Explorer [#]_ の
バージョンの一つとして扱っています。 ::

    import urllib
    import urllib2

    url = 'http://www.someserver.com/cgi-bin/register.cgi'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'name' : 'Michael Foord',
              'location' : 'Northampton',
              'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()

..
  The response also has two useful methods. See the section on `info and geturl`_
  which comes after we have a look at what happens when things go wrong.

レスポンスは二つの便利なメソッドも持っています。
`info と geturl`_ の節を見て下さい、
この節は後で問題が起きた場合に見ておくべき内容です。

..
  Handling Exceptions
  ===================

例外を処理する
==============

..
  *urlopen* raises :exc:`URLError` when it cannot handle a response (though as usual
  with Python APIs, builtin exceptions such as
  :exc:`ValueError`, :exc:`TypeError` etc. may also
  be raised).

*urlopen* はレスポンスを処理できなかった場合、
:exc:`URLError` を送出します
(ふつうの Python API では、組み込み例外の
:exc:`ValueError`, :exc:`TypeError` などが送出されますが)。

..
  :exc:`HTTPError` is the subclass of :exc:`URLError` raised in the specific case of
  HTTP URLs.

:exc:`HTTPError` は :exc:`URLError` のサブクラスで
HTTP URLs の特定の状況で送出されます。

URLError
--------

..
  Often, URLError is raised because there is no network connection (no route to
  the specified server), or the specified server doesn't exist.  In this case, the
  exception raised will have a 'reason' attribute, which is a tuple containing an
  error code and a text error message.

URLError が送出されることはよく起こります、それはネットワーク接続が無い場合や、
指定したサーバが無い場合です。
この場合、例外は 'reason' 属性を持っていて、この属性はエラーコードと
エラーメッセージのテキストを含むタプルです。

.. e.g. ::

例::

    >>> req = urllib2.Request('http://www.pretend_server.org')
    >>> try: urllib2.urlopen(req)
    >>> except URLError, e:
    >>>    print e.reason
    >>>
    (4, 'getaddrinfo failed')


HTTPError
---------

..
  Every HTTP response from the server contains a numeric "status code". Sometimes
  the status code indicates that the server is unable to fulfil the request. The
  default handlers will handle some of these responses for you (for example, if
  the response is a "redirection" that requests the client fetch the document from
  a different URL, urllib2 will handle that for you). For those it can't handle,
  urlopen will raise an :exc:`HTTPError`. Typical errors include '404' (page not
  found), '403' (request forbidden), and '401' (authentication required).

サーバーからの全ての HTTP レスポンスは「ステータスコード」の数値を持っています。
多くの場合ステータスコードはサーバーがリクエストを実現できなかったことを意味します。
デフォルトハンドラーはこれらのレスポンスのいくつかを処理してくれます(例えばレスポンスが
「リダイレクション」、つまりクライアントが別の URL を取得するように要求する場合には
urllib2 はこの処理を行ってくれます。)
処理できないものに対しては urlopen は :exc:`HTTPError` を送出します。
典型的なエラーには '404' (page not found), '403' (request forbidden) と
'401' (authentication required) が含まれます。

..
  See section 10 of RFC 2616 for a reference on all the HTTP error codes.

HTTP のエラーコード全てについては RFC 2616 の10節を参照して下さい。

..
  The :exc:`HTTPError` instance raised will have an integer 'code' attribute, which
  corresponds to the error sent by the server.

送出された :exc:`HTTPError` インスタンスは整数の 'code' 属性を持っていて、
サーバーによって送られた応答に対応しています。

..
  Error Codes
  ~~~~~~~~~~~

エラーコード
~~~~~~~~~~~~

..
  Because the default handlers handle redirects (codes in the 300 range), and
  codes in the 100-299 range indicate success, you will usually only see error
  codes in the 400-599 range.

デフォルトハンドラーはリダイレクト(コードは300番台にあります) を処理し、
100-299番台のコードは成功を意味しているので、たいていの場合は400-599番台の
エラーコードのみを見るだけですみます。

..
  ``BaseHTTPServer.BaseHTTPRequestHandler.responses`` is a useful dictionary of
  response codes in that shows all the response codes used by RFC 2616. The
  dictionary is reproduced here for convenience ::

``BaseHTTPServer.BaseHTTPRequestHandler.responses`` は RFC2616 で利用される
レスポンスコード全てを示す便利な辞書です。
この辞書は便利なのでここに載せておきます::

    # Table mapping response codes to messages; entries have the
    # form {code: (shortmessage, longmessage)}.
    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
              'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
              'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
              'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
              'Document has not changed since given time'),
        305: ('Use Proxy',
              'You must use proxy specified in Location to access this '
              'resource.'),
        307: ('Temporary Redirect',
              'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment Required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this server.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
              'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
              'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
        }

..
  When an error is raised the server responds by returning an HTTP error code
  *and* an error page. You can use the :exc:`HTTPError` instance as a response on the
  page returned. This means that as well as the code attribute, it also has read,
  geturl, and info, methods. ::

エラーが起きた場合、サーバーは HTTP エラーコード *と* エラーページを返して応答します。
返されたページに対する応答として :exc:`HTTPError` インスタンスを使うことができます。
これは code 属性に対しても同様です、これらは read も geturl, info などのメソッドも
持っています。::

    >>> req = urllib2.Request('http://www.python.org/fish.html')
    >>> try:
    >>>     urllib2.urlopen(req)
    >>> except URLError, e:
    >>>     print e.code
    >>>     print e.read()
    >>>
    404
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">
    <?xml-stylesheet href="./css/ht2html.css"
        type="text/css"?>
    <html><head><title>Error 404: File Not Found</title>
    ...... etc...

..
  Wrapping it Up
  --------------

エラーをラップする
------------------

..
  So if you want to be prepared for :exc:`HTTPError` *or* :exc:`URLError` there are two
  basic approaches. I prefer the second approach.

:exc:`HTTPError` *または* :exc:`URLError` が起きたときのために準備しておきたい場合には。
二つの基本的なアプローチがあります。
私は二つ目のアプローチを好みます。

..
  Number 1
  ~~~~~~~~

その1
~~~~~

::


    from urllib2 import Request, urlopen, URLError, HTTPError
    req = Request(someurl)
    try:
        response = urlopen(req)
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    else:
        # everything is fine


..
  .. note::
  
      The ``except HTTPError`` *must* come first, otherwise ``except URLError``
      will *also* catch an :exc:`HTTPError`.

.. note::

    ``except HTTPError`` が *必ず* 最初に来る必要があります、
    そうしないと ``except URLError`` も :exc:`HTTPError` を捕捉してしまいます。

..
  Number 2
  ~~~~~~~~

その2
~~~~~

::

    from urllib2 import Request, urlopen, URLError
    req = Request(someurl)
    try:
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        # everything is fine


..
  info and geturl
  ===============

info と geturl
==============

..
  The response returned by urlopen (or the :exc:`HTTPError` instance) has two useful
  methods :meth:`info` and :meth:`geturl`.

レスポンスは urlopen (または :exc:`HTTPError` インスタンス) によって返され、
:meth:`info` と :meth:`geturl` の二つの便利なメソッドを持っています。

..
  **geturl** - this returns the real URL of the page fetched. This is useful
  because ``urlopen`` (or the opener object used) may have followed a
  redirect. The URL of the page fetched may not be the same as the URL requested.

**geturl** - これは取得したページの実際の URL を返します。
``urlopen`` (または 利用される opener オブジェクト) はリダイレクトに追従するため、
有用です。
取得したページの URL は要求した URL と同じとは限りません。

..
  **info** - this returns a dictionary-like object that describes the page
  fetched, particularly the headers sent by the server. It is currently an
  ``httplib.HTTPMessage`` instance.

**info** - これは取得したページ (特にサーバからヘッダ)を表す
辞書風オブジェクトを返します。
これは現在では ``httplib.HTTPMessage`` インスタンスです。

..
  Typical headers include 'Content-length', 'Content-type', and so on. See the
  `Quick Reference to HTTP Headers <http://www.cs.tut.fi/~jkorpela/http.html>`_
  for a useful listing of HTTP headers with brief explanations of their meaning
  and use.

典型的なヘッダは 'Content-length', 'Content-type' 等を含んでいます。
HTTP ヘッダその意味と利用法について簡単な説明がつきの便利な一覧
`Quick Reference to HTTP Headers <http://www.cs.tut.fi/~jkorpela/http.html>`_ を
参照して下さい、

..
  Openers and Handlers
  ====================

Openers と Handlers
===================

..
  When you fetch a URL you use an opener (an instance of the perhaps
  confusingly-named :class:`urllib2.OpenerDirector`). Normally we have been using
  the default opener - via ``urlopen`` - but you can create custom
  openers. Openers use handlers. All the "heavy lifting" is done by the
  handlers. Each handler knows how to open URLs for a particular URL scheme (http,
  ftp, etc.), or how to handle an aspect of URL opening, for example HTTP
  redirections or HTTP cookies.

URL を取得する場合、opener (混乱を招きやすい名前ですが、 :class:`urllib2.OpenerDirector` の
インスタンス) を利用します。
標準的にはデフォルトの opener を - ``urlopen`` を通して - 利用していますが、
カスタムの opener を作成することもできます。
oppener は handler を利用します。
全ての「一番厄介な仕事」はハンドラによって行なわれます。
各 handler は特定の URL スキーム (http, ftp, 等) での URL の開き方を知っていたり、
URL を開く局面でどう処理するかを知っています、例えば HTTP リダイレクションや
HTTP のクッキーなど。

..
  You will want to create openers if you want to fetch URLs with specific handlers
  installed, for example to get an opener that handles cookies, or to get an
  opener that does not handle redirections.

インストール済みの特定のハンドラで URL を取得したい場合には、
opener を作成したいと思うでしょう、例えばクッキーを処理する opener が得たい場合や、
リダイレクションを処理しない opener を得たい場合。

..
  To create an opener, instantiate an ``OpenerDirector``, and then call
  ``.add_handler(some_handler_instance)`` repeatedly.

opener を作成するには、 ``OpenerDirector`` をインスタンス化して、
続けて、 ``.add_handler(some_handler_instance)`` を呼び出します。

..
  Alternatively, you can use ``build_opener``, which is a convenience function for
  creating opener objects with a single function call.  ``build_opener`` adds
  several handlers by default, but provides a quick way to add more and/or
  override the default handlers.

それに代わる方法として、 ``build_opener`` を利用することもできます、
これは opener オブジェクトを一回の関数呼び出しで作成できる便利な関数です。
``build_opener`` はいくつかのハンドラをデフォルトで追加しますが、
デフォルトのハンドラに対して追加、継承のどちらかまたは両方を行うのに
手っ取り早い方法を提供してくれます。

..
  Other sorts of handlers you might want to can handle proxies, authentication,
  and other common but slightly specialised situations.

追加したくなる可能性がある handler としては、
プロキシ処理、認証など、一般的ですがいくらか特定の状況に限られるものでしょう。

..
  ``install_opener`` can be used to make an ``opener`` object the (global) default
  opener. This means that calls to ``urlopen`` will use the opener you have
  installed.

``install_opener`` も (グローバルな) デフォルト ``opener`` オブジェクトの
作成に利用できます。
つまり、 ``urlopen`` を呼び出すと、インストールした opener が利用されます。

..
  Opener objects have an ``open`` method, which can be called directly to fetch
  urls in the same way as the ``urlopen`` function: there's no need to call
  ``install_opener``, except as a convenience.

opener オブジェクトは ``open`` メソッドを持っていて、
``urlopen`` 関数と同じ様に、url を取得するのに直接呼び出すことができます:
利便性を除けば ``install_opener`` を使う必要はありません。

..
  Basic Authentication
  ====================

Basic 認証
==========

..
  To illustrate creating and installing a handler we will use the
  ``HTTPBasicAuthHandler``. For a more detailed discussion of this subject --
  including an explanation of how Basic Authentication works - see the `Basic
  Authentication Tutorial
  <http://www.voidspace.org.uk/python/articles/authentication.shtml>`_.

ハンドラの作成とインストールを例示するのに、 ``HTTPBasicAuthHandler`` を利用してみます。
この話題についてのより詳しい議論は -- Basic 認証がどうやって動作するのかの説明も含んでいる
`Basic Authentication Tutorial
<http://www.voidspace.org.uk/python/articles/authentication.shtml>`_
を参照して下さい。

..
  When authentication is required, the server sends a header (as well as the 401
  error code) requesting authentication.  This specifies the authentication scheme
  and a 'realm'. The header looks like : ``Www-authenticate: SCHEME
  realm="REALM"``.

認証が必要な場合、サーバは認証を要求するヘッダ (401 のエラーコードとともに) を送ります。
これによって認証スキームと 'realm' が指定されます。
ヘッダはこのようになっています: ``Www-authenticate: SCHEME realm="REALM"`` 。

..
  e.g. ::

例::

    Www-authenticate: Basic realm="cPanel Users"


..
  The client should then retry the request with the appropriate name and password
  for the realm included as a header in the request. This is 'basic
  authentication'. In order to simplify this process we can create an instance of
  ``HTTPBasicAuthHandler`` and an opener to use this handler.

クライアントはリクエストヘッダに含まれる realm に対して適切な名前とパスワードとともに
リクエストを再試行する必要があります。
これが 'basic 認証' です。
一連の流れを簡単化するために、 ``HTTPBasicAuthHandler`` のインスタンスを作成し、
opener が handler を利用するようにします。

..
  The ``HTTPBasicAuthHandler`` uses an object called a password manager to handle
  the mapping of URLs and realms to passwords and usernames. If you know what the
  realm is (from the authentication header sent by the server), then you can use a
  ``HTTPPasswordMgr``. Frequently one doesn't care what the realm is. In that
  case, it is convenient to use ``HTTPPasswordMgrWithDefaultRealm``. This allows
  you to specify a default username and password for a URL. This will be supplied
  in the absence of you providing an alternative combination for a specific
  realm. We indicate this by providing ``None`` as the realm argument to the
  ``add_password`` method.

``HTTPBasicAuthHandler`` はパスワードマネージャーと呼ばれる、
URL と realm をパスワードとユーザ名への対応づけを処理する、オブジェクトを利用します。
realm が何なのか(サーバから返される認証ヘッダから) 知りたい場合には、
``HTTPPasswordMgr`` を利用できます。
多くの場合、realm が何なのかについて気にすることはありません。
そのような場合には ``HTTPPasswordMgrWithDefaultRealm`` を使うと便利です。
これは URL に対してデフォルトのユーザ名とパスワードを指定できます。
これによって特定の realm に対する代替の組み合わせを提供することなしに利用できるように
なります。
このことは ``add_password`` メソッドの realm 引数として ``None`` を与えることで
明示することができます。

..
  The top-level URL is the first URL that requires authentication. URLs "deeper"
  than the URL you pass to .add_password() will also match. ::

トップレベルの URL が認証が必要なはじめに URL です。
この URL よりも「深い」URL を渡しても .add_password() は
同様にマッチします。::

    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of ``None``.
    top_level_url = "http://example.com/foo/"
    password_mgr.add_password(None, top_level_url, username, password)

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)

    # use the opener to fetch a URL
    opener.open(a_url)

    # Install the opener.
    # Now all calls to urllib2.urlopen use our opener.
    urllib2.install_opener(opener)

..
  .. note::
  
      In the above example we only supplied our ``HHTPBasicAuthHandler`` to
      ``build_opener``. By default openers have the handlers for normal situations
      -- ``ProxyHandler``, ``UnknownHandler``, ``HTTPHandler``,
      ``HTTPDefaultErrorHandler``, ``HTTPRedirectHandler``, ``FTPHandler``,
      ``FileHandler``, ``HTTPErrorProcessor``.

.. note::

    上の例では ``build_opener`` に ``HHTPBasicAuthHandler`` のみを与えましたが。
    デフォルトの opener は普通の状況に適用するために
    -- ``ProxyHandler``, ``UnknownHandler``, ``HTTPHandler``,
    ``HTTPDefaultErrorHandler``, ``HTTPRedirectHandler``, ``FTPHandler``,
    ``FileHandler``, ``HTTPErrorProcessor`` を備えています。

..
  ``top_level_url`` is in fact *either* a full URL (including the 'http:' scheme
  component and the hostname and optionally the port number)
  e.g. "http://example.com/" *or* an "authority" (i.e. the hostname,
  optionally including the port number) e.g. "example.com" or "example.com:8080"
  (the latter example includes a port number).  The authority, if present, must
  NOT contain the "userinfo" component - for example "joe@password:example.com" is
  not correct.

``top_level_url`` は実際には "http://example.com/" のような
完全な URL ('http:' スキームとホスト名、オプションとしてポート番号、含む)  *か*
"example.com" や "example.com:8080" (後者はポート番号を含む) のような
"authority" (つまり、ホスト名とオプションとしてポート番号を含む) の
*どちらでも* かまいません。
authority の場合には "userinfo" 要素は含んではいけません
- 例えば "joe@password:example.com" は不適切です。


..
  Proxies
  =======

プロキシ
========

..
  **urllib2** will auto-detect your proxy settings and use those. This is through
  the ``ProxyHandler`` which is part of the normal handler chain. Normally that's
  a good thing, but there are occasions when it may not be helpful [#]_. One way
  to do this is to setup our own ``ProxyHandler``, with no proxies defined. This
  is done using similar steps to setting up a `Basic Authentication`_ handler : ::

**urllib2** は自動でプロキシ設定を認識して使います。
これは通常の handler の組に含まれる ``ProxyHandler`` を通して行なわれます。
たいていの場合はこれでうまくいきますが、役に立たない場合もあります [#]_ 。
この問題に対処する一つの方法はプロキシを定義しない ``ProxyHandler`` を組み立てることです。
この方法は `Basic Authentication`_ handler を設定したときと同じような流れで
行うことができます: ::

    >>> proxy_support = urllib2.ProxyHandler({})
    >>> opener = urllib2.build_opener(proxy_support)
    >>> urllib2.install_opener(opener)

..
  .. note::
  
      Currently ``urllib2`` *does not* support fetching of ``https`` locations
      through a proxy.  However, this can be enabled by extending urllib2 as
      shown in the recipe [#]_.

.. note::

    現在 ``urllib2`` はプロキシ経由で ``https`` ロケーションを取得する機能をサポートしていません。
    しかし、urllib2 をこのレシピ [#]_ で拡張することで可能にすることができます。

..
  Sockets and Layers
  ==================

ソケットとレイヤー
==================

..
  The Python support for fetching resources from the web is layered. urllib2 uses
  the httplib library, which in turn uses the socket library.

Python はレイヤー化された web 上からリソース取得もサポートしています。
urllib2 は httplib ライブラリを利用します、
httplib はさらに socket ライブラリを利用します。

..
  As of Python 2.3 you can specify how long a socket should wait for a response
  before timing out. This can be useful in applications which have to fetch web
  pages. By default the socket module has *no timeout* and can hang. Currently,
  the socket timeout is not exposed at the httplib or urllib2 levels.  However,
  you can set the default timeout globally for all sockets using ::

Python 2.3 ではレスポンスがタイムアウトするまでのソケットの待ち時間を
指定することができます。
これは web ページを取得する場合に便利に使うことができます。
socket モジュールのデフォルトでは *タイムアウトが無く*
ハングしてしまうかもしれません。
現在では socket のタイムアウトは httplib や urllib2 のレベルからは
隠蔽されていています。
しかし、以下を利用することで全てのソケットに対してグローバルに
デフォルトタイムアウトを設定することができます::

    import socket
    import urllib2

    # timeout in seconds
    timeout = 10
    socket.setdefaulttimeout(timeout)

    # this call to urllib2.urlopen now uses the default timeout
    # we have set in the socket module
    req = urllib2.Request('http://www.voidspace.org.uk')
    response = urllib2.urlopen(req)


-------


..
  Footnotes
  =========

脚注
====

..
  This document was reviewed and revised by John Lee.

このドキュメントは John Lee によって査読、改訂されました。

..
  .. [#] For an introduction to the CGI protocol see
         `Writing Web Applications in Python <http://www.pyzine.com/Issue008/Section_Articles/article_CGIOne.html>`_.
  .. [#] Like Google for example. The *proper* way to use google from a program
         is to use `PyGoogle <http://pygoogle.sourceforge.net>`_ of course. See
         `Voidspace Google <http://www.voidspace.org.uk/python/recipebook.shtml#google>`_
         for some examples of using the Google API.
  .. [#] Browser sniffing is a very bad practise for website design - building
         sites using web standards is much more sensible. Unfortunately a lot of
         sites still send different versions to different browsers.
  .. [#] The user agent for MSIE 6 is
         *'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'*
  .. [#] For details of more HTTP request headers, see
         `Quick Reference to HTTP Headers`_.
  .. [#] In my case I have to use a proxy to access the internet at work. If you
         attempt to fetch *localhost* URLs through this proxy it blocks them. IE
         is set to use the proxy, which urllib2 picks up on. In order to test
         scripts with a localhost server, I have to prevent urllib2 from using
         the proxy.
  .. [#] urllib2 opener for SSL proxy (CONNECT method): `ASPN Cookbook Recipe
         <http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/456195>`_.

.. [#] CGI プロトコルの入門については
       `Writing Web Applications in Python <http://www.pyzine.com/Issue008/Section_Articles/article_CGIOne.html>`_
       を参照して下さい。
.. [#] 例を挙げると Google がそうです。プログラムから google を使う
       *正しい* やり方は、もちろん `PyGoogle <http://pygoogle.sourceforge.net>`_ を利用することです。
       Google API を利用した例については
       `Voidspace Google <http://www.voidspace.org.uk/python/recipebook.shtml#google>`_
       を参照して下さい。
.. [#] ブラウザを検知すること (browser sniffing) は web サイトのデザインにおける
       とても悪い習慣です - web 標準を利用する方が賢明でしょう。
       不幸なことに未だに多くの web サイトが異なるブラウザに対して
       異なるバージョンを返しています。
.. [#] MSIE 6 のユーザエージェントは
       *'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'*
       です。
.. [#] HTTP リクエストヘッダの詳細については、
       `Quick Reference to HTTP Headers`_ を参照して下さい。
.. [#] 私の場合は仕事中にインターネットにアクセスするにはプロキシを利用する必要があります。
       *localhost* の URL に対してこのプロキシを経由してアクセスしようとすれば、
       ブロックされます。IE を proxy を利用するように設定すれば、
       urllib2 はその情報を利用します。
       localhost のサーバでスクリプトをテストしようとすると、
       urllib2 がプロキシを利用するのを止めなければいけません。
.. [#] urllib2 opener for SSL proxy (CONNECT method): `ASPN Cookbook Recipe
       <http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/456195>`_.
