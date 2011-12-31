..
  *****************************************
    Curses Programming with Python (英語)
  *****************************************

.. _curses-howto:

***********************************
  Python で Curses プログラミング
***********************************

:Author: A.M. Kuchling, Eric S. Raymond
:Release: 2.03

..
  .. topic:: Abstract
  
     This document describes how to write text-mode programs with Python 2.x, using
     the :mod:`curses` extension module to control the display.

.. topic:: 概要

   このドキュメントでは Python 2.x でテキストモードプログラムを
   表示をコントロールする :mod:`curses` 拡張モジュールを利用して
   書く方法について記述します。

..
  What is curses?
  ===============

curses ってなに?
================

..
  The curses library supplies a terminal-independent screen-painting and
  keyboard-handling facility for text-based terminals; such terminals include
  VT100s, the Linux console, and the simulated terminal provided by X11 programs
  such as xterm and rxvt.  Display terminals support various control codes to
  perform common operations such as moving the cursor, scrolling the screen, and
  erasing areas.  Different terminals use widely differing codes, and often have
  their own minor quirks.

curses ライブラリは、テキストベースの端末、VT100s や Linux コンソールや
xterm や rxvt などの X11 プログラムから提供される端末エミュレータなどの
端末に依存せずに、スクリーンに描画やキーボード処理する機能を供給します。
表示端末は様々な制御コードをサポートしていて、
カーソル移動、画面のスクロール、領域の消去などの一般的な操作を実行できます。
端末によって大きく異なるコードを使うことがあるので、しばしば独自の癖があります。

..
  In a world of X displays, one might ask "why bother"?  It's true that
  character-cell display terminals are an obsolete technology, but there are
  niches in which being able to do fancy things with them are still valuable.  One
  is on small-footprint or embedded Unixes that don't carry an X server.  Another
  is for tools like OS installers and kernel configurators that may have to run
  before X is available.

X ディスプレイの世界では、「どうしてこんな面倒なことを?」と疑問に思うかもしれません。
確かに文字表示端末は時代遅れな技術ではありますが、ニッチな領域が存在していて、
意匠を凝らすことができるため、未だ価値あるものとなっています。
その領域は例えば X サーバを持たない、小さな机上用コンピュータや組み込みの Unix です。
他のものとしては OS インストーラーやカーネル設定ツールなどで、
これらは X が利用できるようになる前に動作する必要があります。

..
  The curses library hides all the details of different terminals, and provides
  the programmer with an abstraction of a display, containing multiple
  non-overlapping windows.  The contents of a window can be changed in various
  ways-- adding text, erasing it, changing its appearance--and the curses library
  will automagically figure out what control codes need to be sent to the terminal
  to produce the right output.

curses ライブラリは異なる端末の詳細を全て隠蔽し、
プログラマに対して、重なり合わない複数のウィンドウを持つ抽象化されたディスプレイを提供します。
ウィンドウの内容は様々な方法で変更されます
-- テキストの追加、消去、外観の変更 -- そして curses ライブラリは
送るべき制御コードを自動的に理解し、正しい出力を生成してくれます。

..
  The curses library was originally written for BSD Unix; the later System V
  versions of Unix from AT&T added many enhancements and new functions. BSD curses
  is no longer maintained, having been replaced by ncurses, which is an
  open-source implementation of the AT&T interface.  If you're using an
  open-source Unix such as Linux or FreeBSD, your system almost certainly uses
  ncurses.  Since most current commercial Unix versions are based on System V
  code, all the functions described here will probably be available.  The older
  versions of curses carried by some proprietary Unixes may not support
  everything, though.

curses ライブラリは元々 BSD UNIX 向けに書かれました;
後の AT&T から出た Unix System V バージョンで多くの機能と新機能が追加されました。
BSD curses はいまやメンテナンスされておらず、
これは AT&T インターフェースのオープンソース実装である ncurses にとって置き換えられました。
Linux や FreeBSD のようなオープンソース Unix を利用している場合は、
おそらくシステムは ncurses を利用しています。
現在のほとんどの商用 Unix は System V のコードを基にしているため、
ここれ述べる全ての関数が利用できるはずです。
しかし、古いバージョンの curses を持ついくつかのプロプライエタリ Unix は
全てには対応していないでしょう。

..
  No one has made a Windows port of the curses module.  On a Windows platform, try
  the Console module written by Fredrik Lundh.  The Console module provides
  cursor-addressable text output, plus full support for mouse and keyboard input,
  and is available from http://effbot.org/zone/console-index.htm.

curses モジュールの Windows 移植は作られていません。
Windows プラットフォーム上では、Fredrik Lundh が書いた Console モジュールを試してみてください。
Console モジュールはカーソル位置を指定してテキスト出力することができ、
マウス、キーボード入力の両方を完全にサポートしていて、
http://effbot.org/zone/console-index.htm から入手できます。


..
  The Python curses module
  ------------------------

Python の curses module
-----------------------

..
  Thy Python module is a fairly simple wrapper over the C functions provided by
  curses; if you're already familiar with curses programming in C, it's really
  easy to transfer that knowledge to Python.  The biggest difference is that the
  Python interface makes things simpler, by merging different C functions such as
  :func:`addstr`, :func:`mvaddstr`, :func:`mvwaddstr`, into a single
  :meth:`addstr` method.  You'll see this covered in more detail later.

Python モジュールは curses が提供する C 関数に対するまったく単純なラッパーです;
既に C での curses プログラミングに慣れ親しんでいるなら、
その知識を Python に持ち込むのは実に簡単です。
最大の違いは Python インターフェースが
異なる関数 :func:`addstr`, :func:`mvaddstr`, :func:`mvwaddstr` を一つのメソッド
:meth:`addstr` メソッドに統合して単純化していることです。
このことは後でより詳しく扱います。

..
  This HOWTO is simply an introduction to writing text-mode programs with curses
  and Python. It doesn't attempt to be a complete guide to the curses API; for
  that, see the Python library guide's section on ncurses, and the C manual pages
  for ncurses.  It will, however, give you the basic ideas.

この HOWTO は curses と Python を使って
テキストプログラムを書くための簡単な入門記事です。
curses API に対する完全な解説をすることは意図していません;
その目的のためには Python ライブラリガイドの ncurses 節と
ncurses の C 言語マニュアルページを参照してください。
しかし、この文章が基本的な考えを提供してくれるでしょう。

..
  Starting and ending a curses application
  ========================================

curses アプリケーションの起動と終了
===================================

..
  Before doing anything, curses must be initialized.  This is done by calling the
  :func:`initscr` function, which will determine the terminal type, send any
  required setup codes to the terminal, and create various internal data
  structures.  If successful, :func:`initscr` returns a window object representing
  the entire screen; this is usually called ``stdscr``, after the name of the
  corresponding C variable. ::

何をするにもまず、curses を初期化する必要があります。
初期化は :func:`initscr` 関数を呼びだすことでできます、
この関数は端末のタイプを決定し、必要とされるセットアップコードを端末に送り、
様々な内部データ構造を作成します。
成功すると、 :func:`initscr` は画面全体を表わすウィンドウオブジェクトを返します;
これは、 ``stdscr`` と呼ばれます、この名前は C での対応する変数にちなんでいます。::

   import curses
   stdscr = curses.initscr()

..
  Usually curses applications turn off automatic echoing of keys to the screen, in
  order to be able to read keys and only display them under certain circumstances.
  This requires calling the :func:`noecho` function. ::

通常 curses アプリケーションは画面へのキーエコーを自動的に止めます、
これはキーを読みとり特定状況下でのみで表示するためです。
これには :func:`noecho` 関数を呼び出す必要があります。::

   curses.noecho()

..
  Applications will also commonly need to react to keys instantly, without
  requiring the Enter key to be pressed; this is called cbreak mode, as opposed to
  the usual buffered input mode. ::

通常アプリケーションはまた、Enter キーを押すことなく、キーに対してすぐに反応する必要があります;
これは cbreak モードと呼ばれ、通常の入力がバッファされるモードと逆に動作します。::

   curses.cbreak()

..
  Terminals usually return special keys, such as the cursor keys or navigation
  keys such as Page Up and Home, as a multibyte escape sequence.  While you could
  write your application to expect such sequences and process them accordingly,
  curses can do it for you, returning a special value such as
  :const:`curses.KEY_LEFT`.  To get curses to do the job, you'll have to enable
  keypad mode. ::

端末は通常、カーソルキーや Page Up や Home といった操作キーなどの特別なキーを
マルチバイトエスケープシーケンスとして返します。
それらのシーケンスを想定して対応する処理を行うアプリケーションを書けるように、
curses はそれを :const:`curses.KEY_LEFT` のような特別な値を返して行ってくれます。
curses にその仕事をさせるには、キーパッドモードを有効にする必要があります。::

   stdscr.keypad(1)

..
  Terminating a curses application is much easier than starting one. You'll need
  to call  ::

curses アプリケーションを終了させるのは起動よりも簡単です。
curses に親和的な端末設定を元に戻すために以下を呼び出す必要があります::

   curses.nocbreak(); stdscr.keypad(0); curses.echo()

..
  to reverse the curses-friendly terminal settings. Then call the :func:`endwin`
  function to restore the terminal to its original operating mode. ::

そして、 :func:`endwin` 関数を呼び出し、端末設定を通常の操作モードに復旧します。::

     curses.endwin()

..
  A common problem when debugging a curses application is to get your terminal
  messed up when the application dies without restoring the terminal to its
  previous state.  In Python this commonly happens when your code is buggy and
  raises an uncaught exception.  Keys are no longer be echoed to the screen when
  you type them, for example, which makes using the shell difficult.

curses アプリケーションをデバッグするときの一般的な問題は、
アプリケーションが端末を以前の状態に復旧することなく異常終了したときに
端末がめちゃめちゃになることです。
Python ではこの問題はコードにバグがあって、捕捉できない例外が発生したときによく起きます。
タイプしたキーはもはやエコーされません、例えば、シェルを使うのが難しくなります。

..
  In Python you can avoid these complications and make debugging much easier by
  importing the module :mod:`curses.wrapper`.  It supplies a :func:`wrapper`
  function that takes a callable.  It does the initializations described above,
  and also initializes colors if color support is present.  It then runs your
  provided callable and finally deinitializes appropriately.  The callable is
  called inside a try-catch clause which catches exceptions, performs curses
  deinitialization, and then passes the exception upwards.  Thus, your terminal
  won't be left in a funny state on exception.

Python では :mod:`curses.wrapper` をインポートすることで
この複雑な問題を避け、デバッグを容易にすることができます。
それは 呼び出し可能オブジェクトを引数にとることができる
:func:`wrapper` 関数を提供します。
これは上に述べた初期化をし、カラーサポートがあればカラーの初期化をします。
そして、与えられた呼び出し可能オブジェクトを実行し、
最終的に適切に初期化の逆操作 (deinitialization) を行います。
呼び出し可能オブジェクトは例外を捕捉する try-catch 節内部で呼び出され、
curses の初期化操作の逆操作を実行します、
そして例外が上に渡されます。
そうして端末は例外が発生しても端末はおかしな状態にならずにすみます。

..
  Windows and Pads
  ================

ウィンドウとパッド
==================

..
  Windows are the basic abstraction in curses.  A window object represents a
  rectangular area of the screen, and supports various methods to display text,
  erase it, allow the user to input strings, and so forth.

ウィンドウは curses での基本的な抽象概念です。
ウィンドウオブジェクトは画面の長方形の領域を表わし、
テキストの表示、消去、ユーザに文字列入力を許可などの様々なメソッドをサポートしています。

..
  The ``stdscr`` object returned by the :func:`initscr` function is a window
  object that covers the entire screen.  Many programs may need only this single
  window, but you might wish to divide the screen into smaller windows, in order
  to redraw or clear them separately. The :func:`newwin` function creates a new
  window of a given size, returning the new window object. ::

:func:`initscr` 関数によって返される ``stdscr`` オブジェクトはウィンドウオブジェクトで
画面全体を扱います。
多くのプログラムはこのウィンドウだけを必要としますが、
画面を小さなウィンドウに分けて
それらを別々に再描画したり消去したいと思うかもしれません。
:func:`newwin` 関数は新しいウィンドウを与えられたサイズで作成し、
新しいウィンドウオブジェクトを返します。::

   begin_x = 20 ; begin_y = 7
   height = 5 ; width = 40
   win = curses.newwin(height, width, begin_y, begin_x)

..
  A word about the coordinate system used in curses: coordinates are always passed
  in the order *y,x*, and the top-left corner of a window is coordinate (0,0).
  This breaks a common convention for handling coordinates, where the *x*
  coordinate usually comes first.  This is an unfortunate difference from most
  other computer applications, but it's been part of curses since it was first
  written, and it's too late to change things now.

curses で利用されている座標形について、言っておくことがあります: 
座標は常に *y,x* の順で渡し、ウィンドウの左上の座標を (0,0) とします。
これは *x* 座標が最初にくる一般的な慣習には反しています。
これは多くの計算機のアプリケーションにとって不幸な違いですが、
curses が最初に書かれて以来そうだったので、
今から変えるには遅すぎます。

..
  When you call a method to display or erase text, the effect doesn't immediately
  show up on the display.  This is because curses was originally written with slow
  300-baud terminal connections in mind; with these terminals, minimizing the time
  required to redraw the screen is very important.  This lets curses accumulate
  changes to the screen, and display them in the most efficient manner.  For
  example, if your program displays some characters in a window, and then clears
  the window, there's no need to send the original characters because they'd never
  be visible.

メソッドを呼びだして、テキストを表示、消去するとき、
その効果はディスプレイにすぐには現われません。
それは curses が元々 300 ボーの端末接続を念頭にいれていたためですl
それらの端末では画面の再描画時間を減らすことがとても重要です。
このため curses は画面への変更を積み上げ、最も効率良い方法でそれらを表示します。
例えば、プログラムがウィンドウにいくつかの文字を表示し、
それからウィンドウを消去する場合、元々の文字を送信する必要はありません、
それらはもう見られることはないのです。

..
  Accordingly, curses requires that you explicitly tell it to redraw windows,
  using the :func:`refresh` method of window objects.  In practice, this doesn't
  really complicate programming with curses much. Most programs go into a flurry
  of activity, and then pause waiting for a keypress or some other action on the
  part of the user.  All you have to do is to be sure that the screen has been
  redrawn before pausing to wait for user input, by simply calling
  ``stdscr.refresh()`` or the :func:`refresh` method of some other relevant
  window.

従って curses に明示的にウィンドウの再描画を明示的に伝えてやる必要があります、
それはウィンドウオブジェクトのメソッド :func:`refresh` を使うことでできます。
実際には、これは curses を使ったプログラムをそれほど複雑にするものではありません。
ほとんどのプログラムはせわしなく動いた後キーを押すなどのユーザからの動作を待ちます。
あなたがするべきことはユーザからの入力を待つ前に単に ``stdscr.refresh()`` や
関連するウィンドウの :func:`refresh` メソッドを呼び出して
画面を再描画するだけです。

..
  A pad is a special case of a window; it can be larger than the actual display
  screen, and only a portion of it displayed at a time. Creating a pad simply
  requires the pad's height and width, while refreshing a pad requires giving the
  coordinates of the on-screen area where a subsection of the pad will be
  displayed.   ::

パッドはウィンドウの特別な場合を指します; それは実際に画面に表示されるものより大きくなることがあり、
画面にはその一部だけが表示されます。
パッドを作るのに必要なものはパッドの高さと幅だけです、
一方でパッドの再描画には、表示される部分を指す画面上の領域の座標を指定する必要があります。::

     pad = curses.newpad(100, 100)
     #  These loops fill the pad with letters; this is
     # explained in the next section
     for y in range(0, 100):
         for x in range(0, 100):
             try: pad.addch(y,x, ord('a') + (x*x+y*y) % 26 )
             except curses.error: pass

     #  Displays a section of the pad in the middle of the screen
     pad.refresh( 0,0, 5,5, 20,75)

..
  The :func:`refresh` call displays a section of the pad in the rectangle
  extending from coordinate (5,5) to coordinate (20,75) on the screen; the upper
  left corner of the displayed section is coordinate (0,0) on the pad.  Beyond
  that difference, pads are exactly like ordinary windows and support the same
  methods.

:func:`refresh` はパッドの一部、画面上の座標 (5,5) から (20,75) に及ぶ長方形領域を表示します;
表示される一部の左上の角は パッドの座標 (0,0) です。
この違いを除けば、パッドは通常のウィンドウと全く同じで、
同じメソッドを持ちます。

..
  If you have multiple windows and pads on screen there is a more efficient way to
  go, which will prevent annoying screen flicker at refresh time.  Use the
  :meth:`noutrefresh` method of each window to update the data structure
  representing the desired state of the screen; then change the physical screen to
  match the desired state in one go with the function :func:`doupdate`.  The
  normal :meth:`refresh` method calls :func:`doupdate` as its last act.

複数のウィンドウとパッドが画面上にある場合、より効率的な方法があり、
再描画時に画面をちらつかせるのを防いでくれます。
各ウィンドウの
:meth:`noutrefresh` メソッドを利用して、
画面の望ましい状態を表わすデータ構造をアップデートし、
:func:`doupdate` 関数で望む状態に合った物理的な画面に変更します。
通常の :meth:`refresh` メソッドは自身の動作時の最後に :func:`doupdate` を呼び出します。

..
  Displaying Text
  ===============

テキストの表示
==============

..
  From a C programmer's point of view, curses may sometimes look like a twisty
  maze of functions, all subtly different.  For example, :func:`addstr` displays a
  string at the current cursor location in the ``stdscr`` window, while
  :func:`mvaddstr` moves to a given y,x coordinate first before displaying the
  string. :func:`waddstr` is just like :func:`addstr`, but allows specifying a
  window to use, instead of using ``stdscr`` by default. :func:`mvwaddstr` follows
  similarly.

C 言語のプログラマの視点からすると、curses はしばしば、
混乱を招きやすい、微妙に似た関数を持っています。
例えば :func:`addstr` は ``stdscr`` ウィンドウの現在のカーソル位置の文字列を表示し、
一方で :func:`mvaddstr` は与えられた y,x 座標にまず移動して、文字列を表示します。
:func:`waddstr` はほとんど :func:`addstr` に似ていますが、
デフォルトの ``stdscr`` を使う代わりに使うウィンドウを指定できます。
:func:`mvwaddstr` も同様です。

..
  Fortunately the Python interface hides all these details; ``stdscr`` is a window
  object like any other, and methods like :func:`addstr` accept multiple argument
  forms.  Usually there are four different forms.

幸運にも、Python インターフェースはこれらの詳細を全て隠蔽してくれます;
``stdscr`` は他のものと同様のウィンドウオブジェクトであり、 :func:`addstr` のようなメソッドは
複数の引数形式を許容してくれます。
通常それらは4つの形式です。

..
  +---------------------------------+-----------------------------------------------+
  | Form                            | Description                                   |
  +=================================+===============================================+
  | *str* or *ch*                   | Display the string *str* or character *ch* at |
  |                                 | the current position                          |
  +---------------------------------+-----------------------------------------------+
  | *str* or *ch*, *attr*           | Display the string *str* or character *ch*,   |
  |                                 | using attribute *attr* at the current         |
  |                                 | position                                      |
  +---------------------------------+-----------------------------------------------+
  | *y*, *x*, *str* or *ch*         | Move to position *y,x* within the window, and |
  |                                 | display *str* or *ch*                         |
  +---------------------------------+-----------------------------------------------+
  | *y*, *x*, *str* or *ch*, *attr* | Move to position *y,x* within the window, and |
  |                                 | display *str* or *ch*, using attribute *attr* |
  +---------------------------------+-----------------------------------------------+

+-------------------------------------+--------------------------------------------+
| 形式                                | 説明                                       |
+=====================================+============================================+
| *str* または *ch*                   | 文字列 *str* または 文字 *ch* を現在位置に |
|                                     | 表示します                                 |
+-------------------------------------+--------------------------------------------+
| *str* または *ch*, *attr*           | 文字列 *str* または 文字 *ch* を           |
|                                     | 属性 *attr* を利用して現在位置に表示します |
+-------------------------------------+--------------------------------------------+
| *y*, *x*, *str* または *ch*         | ウィンドウ内の位置 *y,x* に移動し          |
|                                     | *str* または *ch* を表示します             |
+-------------------------------------+--------------------------------------------+
| *y*, *x*, *str* または *ch*, *attr* | ウィンドウ内の位置 *y,x* に移動し          |
|                                     | 属性 *attr* を利用して                     |
|                                     | *str* または *ch* を表示します             |
+-------------------------------------+--------------------------------------------+

..
  Attributes allow displaying text in highlighted forms, such as in boldface,
  underline, reverse code, or in color.  They'll be explained in more detail in
  the next subsection.

属性によって表示するテキストをハイライトすることができます、
ボールド体、アンダーライン、反転、カラーなど。
より詳しくは次の小節で説明します。

..
  The :func:`addstr` function takes a Python string as the value to be displayed,
  while the :func:`addch` functions take a character, which can be either a Python
  string of length 1 or an integer.  If it's a string, you're limited to
  displaying characters between 0 and 255.  SVr4 curses provides constants for
  extension characters; these constants are integers greater than 255.  For
  example, :const:`ACS_PLMINUS` is a +/- symbol, and :const:`ACS_ULCORNER` is the
  upper left corner of a box (handy for drawing borders).

:func:`addstr` 関数は Python 文字列を引数にとり、表示します。
一方 :func:`addch` 関数は文字を引数にとります、引数は長さ1の文字列か整数のどちらでもかまいません。
文字列の場合には、表示する文字は 0 から 255 の間に制限されます。
SVr4 curses は文字拡張のための定数を提供しています; それらの定数は 255 より大きい整数です。
例えば :const:`ACS_PLMINUS` は +/- 記号で
:const:`ACS_ULCORNER` はボックスの左上角です (境界を描くのに便利です)。

..
  Windows remember where the cursor was left after the last operation, so if you
  leave out the *y,x* coordinates, the string or character will be displayed
  wherever the last operation left off.  You can also move the cursor with the
  ``move(y,x)`` method.  Because some terminals always display a flashing cursor,
  you may want to ensure that the cursor is positioned in some location where it
  won't be distracting; it can be confusing to have the cursor blinking at some
  apparently random location.

ウィンドウは最後の操作の後のカーソル位置を覚えているため、
*y,x* 座標をうっかり忘れてしまっても、文字列や文字は最後の操作位置に表示されます。
``move(y,x)`` メソッドでカーソルを移動させることもできます。
常に点滅するカーソルを表示する端末もあるため、
カーソルが特定の位置にいることを保証して
注意が反れないようにしたいと思うかもしれません;
ランダムに見える位置でカーソルがちらつくとと面を食らってしまいます。

..
  If your application doesn't need a blinking cursor at all, you can call
  ``curs_set(0)`` to make it invisible.  Equivalently, and for compatibility with
  older curses versions, there's a ``leaveok(bool)`` function.  When *bool* is
  true, the curses library will attempt to suppress the flashing cursor, and you
  won't need to worry about leaving it in odd locations.

アプリケーションがちらつくカーソルを全く必要としない場合、
``curs_set(0)`` を呼び出してカーソル見えなくすることができます。
同じことを、古い curses バージョンに対する互換性を保ちつつ行うために
``leaveok(bool)`` 関数があります。
*bool* が true の場合、curses ライブラリは点滅するカーソルを外に出さなくするので、
変な場所に現われるのを心配する必要は無くなります。

..
  Attributes and Color
  --------------------

属性とカラー
------------

..
  Characters can be displayed in different ways.  Status lines in a text-based
  application are commonly shown in reverse video; a text viewer may need to
  highlight certain words.  curses supports this by allowing you to specify an
  attribute for each cell on the screen.

文字は様々な方法で表示することができます。
テキストベースアプリケーションでのステータスラインは通常反転して表示されます;
テキストビュアーは特定の単語をハイライトする必要があるかもしれせん。
curses は属性を画面上の各セルに対して指定することで、それをサポートします。

..
  An attribute is a integer, each bit representing a different attribute.  You can
  try to display text with multiple attribute bits set, but curses doesn't
  guarantee that all the possible combinations are available, or that they're all
  visually distinct.  That depends on the ability of the terminal being used, so
  it's safest to stick to the most commonly available attributes, listed here.

属性は整数値で、それぞれのビットが異なる属性を表わします。
複数の属性ビットをセットしてテキストの表示を試みることができますが、
curses は全ての組み合わせが利用可能であるかや
視覚的に区別できるかどうかは保証してくれません、
それらは利用している端末の能力に依存しているため、
最も安全なのは、最も一般的に利用可能な属性を設定する方法です、
ここに列挙します

..
  +----------------------+--------------------------------------+
  | Attribute            | Description                          |
  +======================+======================================+
  | :const:`A_BLINK`     | Blinking text                        |
  +----------------------+--------------------------------------+
  | :const:`A_BOLD`      | Extra bright or bold text            |
  +----------------------+--------------------------------------+
  | :const:`A_DIM`       | Half bright text                     |
  +----------------------+--------------------------------------+
  | :const:`A_REVERSE`   | Reverse-video text                   |
  +----------------------+--------------------------------------+
  | :const:`A_STANDOUT`  | The best highlighting mode available |
  +----------------------+--------------------------------------+
  | :const:`A_UNDERLINE` | Underlined text                      |
  +----------------------+--------------------------------------+

+----------------------+--------------------------------------+
| 属性                 | 説明                                 |
+======================+======================================+
| :const:`A_BLINK`     | テキストを点滅                       |
+----------------------+--------------------------------------+
| :const:`A_BOLD`      | 高輝度またはボールドテキスト         |
+----------------------+--------------------------------------+
| :const:`A_DIM`       | 低輝度テキスト                       |
+----------------------+--------------------------------------+
| :const:`A_REVERSE`   | 反転テキスト                         |
+----------------------+--------------------------------------+
| :const:`A_STANDOUT`  | 利用できる最良のハイライトモード     |
+----------------------+--------------------------------------+
| :const:`A_UNDERLINE` | 下線付きテキスト                     |
+----------------------+--------------------------------------+

..
  So, to display a reverse-video status line on the top line of the screen, you
  could code::

つまり、反転するステータスラインを画面の最上部に表示するには、コードをこうします::

     stdscr.addstr(0, 0, "Current mode: Typing mode",
     	      curses.A_REVERSE)
     stdscr.refresh()

..
  The curses library also supports color on those terminals that provide it, The
  most common such terminal is probably the Linux console, followed by color
  xterms.

curses ライブラリはカラー機能を提供している端末でのカラーもサポートしています、
そんな端末の中で最も一般的なものは Linux コンソールで、color xterm もそれに続きます。

..
  To use color, you must call the :func:`start_color` function soon after calling
  :func:`initscr`, to initialize the default color set (the
  :func:`curses.wrapper.wrapper` function does this automatically).  Once that's
  done, the :func:`has_colors` function returns TRUE if the terminal in use can
  actually display color.  (Note: curses uses the American spelling 'color',
  instead of the Canadian/British spelling 'colour'.  If you're used to the
  British spelling, you'll have to resign yourself to misspelling it for the sake
  of these functions.)

カラーを利用するには、 :func:`initscr` を呼び出したすぐ後に
:func:`start_color` 関数を呼びし、デフォルトカラーセット
を初期化しなければいけません
(:func:`curses.wrapper.wrapper` 関数はこれを自動的に行ないます)。
一旦それを行えば、 :func:`has_colors` 関数は、端末が実際にカラーを表示できる場合に
TRUE を返します。
(ノート: curses はカナダ/イギリスつづりに 'colour' ではなくアメリカつづりの 'color' を使います。
イギリスつづりを使っている場合には、これらの関数のミススペルを修正する必要があります。)

..
  The curses library maintains a finite number of color pairs, containing a
  foreground (or text) color and a background color.  You can get the attribute
  value corresponding to a color pair with the :func:`color_pair` function; this
  can be bitwise-OR'ed with other attributes such as :const:`A_REVERSE`, but
  again, such combinations are not guaranteed to work on all terminals.

curses ライブラリは有限の数の、
フォラグラウンド(またはテキスト)カラーとバックグラウンドカラーペアを保持します。
カラーペアに対応する属性値は :func:`color_pair` 関数で取得できます;
これは :const:`A_REVERSE` のような他の属性と OR 論理演算組み合わせることができます、
ただし、繰り返しになりますが、組み合わせは全ての端末で保証されていません。

..
  An example, which displays a line of text using color pair 1::

例として、テキスト行をカラーペア 1 を使って表示します::

   stdscr.addstr( "Pretty text", curses.color_pair(1) )
   stdscr.refresh()

..
  As I said before, a color pair consists of a foreground and background color.
  :func:`start_color` initializes 8 basic colors when it activates color mode.
  They are: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and
  7:white.  The curses module defines named constants for each of these colors:
  :const:`curses.COLOR_BLACK`, :const:`curses.COLOR_RED`, and so forth.

前に述べたように、カラーペアはフォアグラウンドカラーとバックグラウンドカラーから構成されています。
:func:`start_color` はカラーモードを有効にした場合 8 の基本カラーを初期化します。
基本カラーは: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, 7:white です。
curses モジュールは各名前に対する名前付き定数を定義しています:
:const:`curses.COLOR_BLACK`, :const:`curses.COLOR_RED`, など。

..
  The ``init_pair(n, f, b)`` function changes the definition of color pair *n*, to
  foreground color f and background color b.  Color pair 0 is hard-wired to white
  on black, and cannot be changed.

``init_pair(n, f, b)`` 関数はカラーペア *n* の定義を
フォアグラウンド f バックグラウンド b に
変更します。
カラーペア 0 は黒背景に白で組み込まれていて変更できません。

..
  Let's put all this together. To change color 1 to red text on a white
  background, you would call::

やってみましょう。カラー 1 を白背景に赤に変更してみましょう、こうして呼び出します::

   curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

..
  When you change a color pair, any text already displayed using that color pair
  will change to the new colors.  You can also display new text in this color
  with::

カラーペアを変更するときには、既に表示された任意のテキストが利用するカラーペアを新しい色に変更します。
新しいテキストをこの色で使うこともできます::

   stdscr.addstr(0,0, "RED ALERT!", curses.color_pair(1) )

..
  Very fancy terminals can change the definitions of the actual colors to a given
  RGB value.  This lets you change color 1, which is usually red, to purple or
  blue or any other color you like.  Unfortunately, the Linux console doesn't
  support this, so I'm unable to try it out, and can't provide any examples.  You
  can check if your terminal can do this by calling :func:`can_change_color`,
  which returns TRUE if the capability is there.  If you're lucky enough to have
  such a talented terminal, consult your system's man pages for more information.

凝ったターミナルは実際の色の定義を与えられた RGB 値に変更することができます。
これによってふつうは赤であるカラー1を紫や青など好きな色に変更されます。
不幸にも Linux コンソールはこれをサポートしていません、
そのためこの機能は試すことも例を出すこともできません。
:func:`can_change_color` を呼び出すことで端末が使えるのか調べることができ、
対応していれば、TRUE を返します。
もしそのような telnet 端末を持つ幸運に巡りあえたなら、
より多くの情報の情報を得るためにシステムの man ページを参照することを勧めます。


..
  User Input
  ==========

ユーザ入力
==========

..
  The curses library itself offers only very simple input mechanisms. Python's
  support adds a text-input widget that makes up some of the lack.

curses ライブラリは自身で単純なインプット機構を備えています。
Python はテキスト入力ウィジェットを追加して、いくつかの足りない部分を補っています。

..
  The most common way to get input to a window is to use its :meth:`getch` method.
  :meth:`getch` pauses and waits for the user to hit a key, displaying it if
  :func:`echo` has been called earlier.  You can optionally specify a coordinate
  to which the cursor should be moved before pausing.

ウィンドウに対する入力を得るための最も一般的な方法は
ウィンドウの :meth:`getch` メソッドを利用することです。
:meth:`getch` はユーザが待機してキーを打つのを待ち、
:func:`echo` が先に呼ばれていれば、それを表示します。
オプションとして待機する前にカーソルが移動するべき座標を指定することができます。

..
  It's possible to change this behavior with the method :meth:`nodelay`. After
  ``nodelay(1)``, :meth:`getch` for the window becomes non-blocking and returns
  ``curses.ERR`` (a value of -1) when no input is ready.  There's also a
  :func:`halfdelay` function, which can be used to (in effect) set a timer on each
  :meth:`getch`; if no input becomes available within a specified
  delay (measured in tenths of a second), curses raises an exception.

この挙動は :meth:`nodelay` メソッドで変更することができます。
``nodelay(1)`` の後、 ウィンドウに対する :meth:`getch` はノンブロッキングになり、
入力が準備されていないときには ``curses.ERR`` (-1 の値) を返します。
:func:`halfdelay` 関数もあり、(事実上) 各 :meth:`getch` に対して
タイマーを設定するのに使うことができます;
指定したディレイの間に(10分の1秒単位で測られます)入力が得られなかった場合
curses は例外を送出します。

..
  The :meth:`getch` method returns an integer; if it's between 0 and 255, it
  represents the ASCII code of the key pressed.  Values greater than 255 are
  special keys such as Page Up, Home, or the cursor keys. You can compare the
  value returned to constants such as :const:`curses.KEY_PPAGE`,
  :const:`curses.KEY_HOME`, or :const:`curses.KEY_LEFT`.  Usually the main loop of
  your program will look something like this::

:meth:`getch` メソッドは整数を返します; もしそれが 0 から 255 までなら、
それは押されたキーの ASCII コードを表わします。
255 より大きな値は Page Up, Home またはカーソルキーのような特別なキーです。
返された値を :const:`curses.KEY_PPAGE`, :const:`curses.KEY_HOME` または
:const:`curses.KEY_LEFT` のような定数と比較することが可能です。
通常プログラムのメインループはこのようになります::

   while 1:
       c = stdscr.getch()
       if c == ord('p'): PrintDocument()
       elif c == ord('q'): break  # Exit the while()
       elif c == curses.KEY_HOME: x = y = 0

..
  The :mod:`curses.ascii` module supplies ASCII class membership functions that
  take either integer or 1-character-string arguments; these may be useful in
  writing more readable tests for your command interpreters.  It also supplies
  conversion functions  that take either integer or 1-character-string arguments
  and return the same type.  For example, :func:`curses.ascii.ctrl` returns the
  control character corresponding to its argument.

:mod:`curses.ascii` モジュールは ASCII クラスのメンバーシップ関数を提供し、
整数と1文字引数のどちらもとることができます;
これらは独自のコマンドインタプリタに対するより読み易いテストを書くのに便利でしょう。
整数と1文字引数のどちらもとることができ、引数と同じ型を返す変換関数も提供します。
例えば :func:`curses.ascii.ctrl` は引数に応じた型で制御文字を返します。

..
  There's also a method to retrieve an entire string, :const:`getstr()`.  It isn't
  used very often, because its functionality is quite limited; the only editing
  keys available are the backspace key and the Enter key, which terminates the
  string.  It can optionally be limited to a fixed number of characters. ::

文字列全体を取得するメソッド :const:`getstr()` もあります。
これは頻繁に使われるものではありません、なぜならこの機能はとても制限的なものだからです;
利用可能な編集キーはバックスペースと Enter キーの文字列を終了させるものだけです。
オプションとして文字列の長さを固定長に限定することもできます。::

   curses.echo()            # Enable echoing of characters

   # Get a 15-character string, with the cursor on the top line
   s = stdscr.getstr(0,0, 15)

..
  The Python :mod:`curses.textpad` module supplies something better. With it, you
  can turn a window into a text box that supports an Emacs-like set of
  keybindings.  Various methods of :class:`Textbox` class support editing with
  input validation and gathering the edit results either with or without trailing
  spaces.   See the library documentation on :mod:`curses.textpad` for the
  details.

Python の :mod:`curses.textpad` モジュールはよりよいものを提供します。
これを使うことで、ウィンドウ をEmacs のようなキーバインドをサポートする
テキストボックスにすることができます。
:class:`Textbox` クラスの様々なメソッドが
入力の検証つきの編集をサポートシ
前後のスペースつき、または無しで編集結果を収集します。
詳しくは :mod:`curses.textpad` のライブラリドキュメントを参照して下さい。

..
  For More Information
  ====================

より多くの情報
==============

..
  This HOWTO didn't cover some advanced topics, such as screen-scraping or
  capturing mouse events from an xterm instance.  But the Python library page for
  the curses modules is now pretty complete.  You should browse it next.

この HOWTO ではいくつかの進んだ話題、スクリーンスクレイピングや
xterm インスタンスからマウスイベントを捉えるなど、については扱っていません。
しかし、Python の curses モジュールのライブラリページはいまやかなり充実しています。
次はこれを見るべきです。

..
  If you're in doubt about the detailed behavior of any of the ncurses entry
  points, consult the manual pages for your curses implementation, whether it's
  ncurses or a proprietary Unix vendor's.  The manual pages will document any
  quirks, and provide complete lists of all the functions, attributes, and
  :const:`ACS_\*` characters available to you.

ncurses のあらゆるエントリポイントの詳細な挙動について疑問があれば、
curses 実装が ncurses か、プロプライエタリな Unix ベンダーのものかによらず
curses 実装のマニュアルページをみることを参照して下さい。
マニュアルページにはあらゆる癖がドキュメントにされていて、全ての関数、属性、
:const:`ACS_\*` 文字の完全なリストが提供されています。

..
  Because the curses API is so large, some functions aren't supported in the
  Python interface, not because they're difficult to implement, but because no one
  has needed them yet.  Feel free to add them and then submit a patch.  Also, we
  don't yet have support for the menus or panels libraries associated with
  ncurses; feel free to add that.

curses API は巨大なので、Python インターフェースではいくつかの関数はサポートされていません、
ですがそれは必要としている人がいまのところいないためです。
気兼ねなく、足りないものを追加してパッチを提出して下さい。
また、ncurese に関連したメニューやパネルライブラリのサポートも行なわれていません;
気兼ねなく追加して下さい。

..
  If you write an interesting little program, feel free to contribute it as
  another demo.  We can always use more of them!

面白い小さなプログラムを書いたら、新たなデモとして気兼ねなく提出して下さい。
私達は常により多くのデモ使うことができます!

The ncurses FAQ: http://invisible-island.net/ncurses/ncurses.faq.html

