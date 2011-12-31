:tocdepth: 2

====================================
グラフィックユーザインタフェース FAQ
====================================

.. contents::

Python のプラットフォーム非依存の GUI ツールキットには何がありますか？
======================================================================

目的のプラットフォーム (群) が何かによって、いくつかあります。
この中にはまだ Python 3 に移植されていないものもあります。
少なくとも `Tkinter`_ と `Qt`_ は Python 3 互換であることを確認しています。

.. XXX check links

Tkinter
-------

Python の標準的なビルドには、tkinter という
Tcl/Tk ウィジェットセットのオブジェクト指向インタフェースが含まれています。
これは最も簡単にインストールして使えるでしょう。ソースへのポインタなど、
Tk に関する詳しい情報は、http://www.tcl.tk の Tcl/Tk ホームページを
参照してください。Tcl/Tk は、MacOS、Windows、Unix プラットフォームに
完全にポータブルです。

wxWidgets
---------

wxWidgets (http://www.wxwidgets.org) は、C++ で書かれたフリーでポータブルな
GUI クラスライブラリで、各プラットフォームのネイティブなルックアンドフィールを
提供します。現在、Windows、MacOS X、GTK、X11 はすべて安定した対象です。
言語バインディングは Python、Perl、Ruby などの言語で利用できます。

wxPython (http://www.wxpython.org) が wxWidgets の Python バインディングです。
これはたいてい公式の wxWidgets より少し遅れますが、他の言語バインディングでは
利用できない機能も pure Python 拡張経由でいくつか提供しています。
wxPython ユーザと開発者の活発なコミュニティがあります。

wxWidgets も wxPython も、フリーなオープンソースソフトウェアであり、寛大な
ライセンスでフリーウェアやシェアウェアと同様に商業利用も許可されています。

Qt
---

Qt ツールキットのバインディング
(`PyQt <http://www.riverbankcomputing.co.uk/software/pyqt/>`_)
や KDE へのバインディング
(`PyKDE <http://www.riverbankcomputing.co.uk/software/pykde/intro>`_)
があります。オープンソースソフトウェアを書くには、PyQt に支払いをする
必要はありませんが、
プロプライエタリなアプリケーションを書くためには `Riverbank Computing
<http://www.riverbankcomputing.co.uk/software/pyqt/license>`_ から
PyQt ライセンスを、(Qt 4.4 までは) `Trolltech <http://www.trolltech.com>` _
から Qt ライセンスを購入しなければなりません。
Qt 4.5 以降は LGPL ライセンスが適用されています。

Gtk+
----

`Gtk+ toolkit <http://www.gtk.org>`_ 用の PyGtk バインディングが
James Henstridge によって実装されています。<http://www.pygtk.org> を
参照してください。

FLTK
----

簡潔かつ強力で成熟したクロスプラットフォームウィンドウシステム
`the FLTK toolkit <http://www.fltk.org>`_ の Python バインディングが
`the PyFLTK project <http://pyfltk.sourceforge.net/>`_ から利用できます。


FOX
---

`the FOX toolkit <http://www.fox-toolkit.org/>`_ のラッパ `FXpy
<http://fxpy.sourceforge.net/>`_ が利用できます。FOX は Unix バリアントと
Windows の両方をサポートします。


OpenGL
------

OpenGL のバインディングは、\ `PyOpenGL <http://pyopengl.sourceforge.net>`_
を参照してください。


Python のプラットフォーム固有の GUI ツールキットには何がありますか？
====================================================================

Jack Jansen による `The Mac port <http://python.org/download/mac>`_ には、
ネイティブ Mac ツールボックスコールをサポートする豊富で発展中のモジュール群が
あります。このポートは MacOS X の Carbon ライブラリをサポートしています。

`PyObjc Objective-C bridge <http://pyobjc.sourceforge.net>`_ を
インストールすることによって、Python プログラマは MacOS X の
Cocoa ライブラリを使うことができます。Mac port に付属するドキュメントを
参照してください。

Mark Hammond による :ref:`Pythonwin <windows-faq>` には
Microsoft Foundation Class のインタフェースと Python プログラミング環境が
含まれています。これは MFC クラスを用いて主に Python で書かれています。


Tkinter の質問
==============

Tkinter アプリケーションを凍結するにはどうしますか？
----------------------------------------------------

Freeze はスタンドアロンアプリケーションを生成するツールです。
Tkinter アプリケーションを凍結するとき、それは Tcl と Tk ライブラリを
必要とするので、真のスタンドアロンにはなりません。

一つの解決策は、アプリケーションに Tcl と Tk ライブラリを同梱し、
環境変数 :envvar:`TCL_LIBRARY` と :envvar:`TK_LIBRARY` でランタイムに
指定することです。

真にスタンドアロンなアプリケーションにするためには、ライブラリを成す
Tcl スクリプトもアプリケーションに統合されていなければなりません。
それをサポートするツールの一つは SAM (stand-alone modules) で、
Tix ディストリビューション (http://tix.sourceforge.net/) の一部です。

SAM を有効にするように Tix をビルドして、Python の :file:`Modules/tkappinit.c`
内部の :c:func:`Tclsam_init` 等への適切なコールを実行し、libtclsam と
libtksam にリンクしてください (Tix ライブラリを含んでも良いです)。


I/O を待つ間に扱われる Tk イベントを作れますか？
------------------------------------------------

はい、スレッドさえ必要ありません！  ただし、I/O コードを少し
再構成しなければなりません。Tk には Xt の :c:func:`XtAddInput()` コールと
同等なものがあるので、ファイルディスクリプタ上で I/O が可能なときに
Tk メインループから呼ばれるコールバック関数を登録できます。
このようにすればいいです::

   from Tkinter import tkinter
   tkinter.createfilehandler(file, mask, callback)

file には Python ファイルかソケットオブジェクト(実際には、fileno() メソッドを
持った何か)、または整数のファイルディスクリプタを指定できます。
mask は定数 tkinter.READABLE または tkinter.WRITABLE のどちらかです。
callback は以下のように呼び出されます::

   callback(file, mask)

callback が完了したら、次のように登録を解除しなければなりません::

   tkinter.deletefilehandler(file)

ノート: 読み込みに使える *バイト数* がわからないので、指定されたバイト数を
読み込む Python のファイルオブジェクトの read や readline メソッドを
使うことはできません。ソケットには、\ :meth:`recv` や :meth:`recvfrom` メソッドを
使うといいです。その他のファイルには、\ ``os.read(file.fileno(), maxbytecount)``
を使ってください。


Tkinter で働くキーバインディングが得られません。なぜですか？
------------------------------------------------------------

:meth:`bind` メソッドでイベントに結び付けられたイベントハンドラが、
適切なキーが押されたときにさえハンドルされないという苦情がよく聞かれます。

最も一般的な原因は、バインディングが適用されるウィジェットが
"キーボードフォーカス" を持たないことです。Tk ドキュメントで
フォーカスコマンドを確認してください。通常はウィジェットの中を
クリックすることでキーボードフォーカスを与えられます (ただしラベルには
与えられません。takefocus オプションを参照してください)。


