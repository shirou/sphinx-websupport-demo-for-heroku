
.. _top-level:

****************
トップレベル要素
****************

Python インタプリタは、標準入力や、プログラムの引数として与えられたスクリプト、対話的にタイプ入力された命令、モジュールのソースファイルな
ど、様々な入力源から入力を得ることができます。この章では、それぞれの場合に用いられる構文法について説明しています。

.. index:: single: interpreter


.. _programs:

完全な Python プログラム
========================

.. index:: single: program

.. index::
   module: sys
   module: __main__
   module: __builtin__

言語仕様の中では、その言語を処理するインタプリタがどのように起動されるかまで規定する必要はないのですが、完全な Python プログラムについての概
念を持っておくと役に立ちます。完全な Python プログラムは、最小限に初期化された環境: 全ての組み込み変数と標準モジュールが利用可能で、かつ
:mod:`sys` (様々なシステムサービス)、 :mod:`__builtin__` (組み込み関数、例外、および
``None``)、 :mod:`__main__` の 3 つを除く全てのモジュールが初期化されていない状態で動作します。 :mod:`__main__` は、
完全なプログラムを実行する際に、ローカルおよびグローバルな名前空間を提供するために用いられます。

完全な Python プログラムの構文は、下の節で述べるファイル入力のためのものです。

.. index::
   single: interactive mode
   module: __main__

インタプリタは、対話的モード (interactive mode) で起動されることもあります;
この場合、インタプリタは完全なプログラムを読んで実行するのではなく、一度に単一の実行文 (複合文のときもあります) を読み込んで実行します。
初期状態の環境は、完全なプログラムを実行するときの環境と同じです; 各実行文は、 :mod:`__main__` の名前空間内で実行されます。

.. index::
   single: UNIX
   single: command line
   single: standard input

Unixの環境下では、完全なプログラムをインタプリタに渡すには三通りの方法があります: 第一は、 :option:`-c` *string* コマンドラインオ
プションを使う方法、第二はファイルを第一コマンドライン引数として指定する方法、そして最後は標準入力から入力する方法です。ファイルや標準入力が tty (端末)
デバイスの場合、インタプリタは対話モードに入ります; そうでない場合、ファイルを完全なプログラムとして実行します。


.. _file-input:

ファイル入力
============

非対話的なファイルから読み出された入力は、全て同じ形式:

.. productionlist::
   file_input: (NEWLINE | `statement`)*

をとります。この構文法は、以下の状況で用いられます:

* (ファイルや文字列内の) 完全な Python プログラムを構文解析するとき;

* モジュールを構文解析するとき;

* :keyword:`exec` で渡された文字列を構文解析するとき;


.. _interactive:

対話的入力
==========

対話モードでの入力は、以下の文法の下に構文解析されます:

.. productionlist::
   interactive_input: [`stmt_list`] NEWLINE | `compound_stmt` NEWLINE

対話モードでは、(トップレベルの) 複合文の最後に空白行を入れなくてはならないことに注意してください; これは、複合文の終端をパーザが検出するた
めの手がかりとして必要です。


.. _expression-input:

式入力
======

.. index:: single: input

.. index:: builtin: eval

式入力には二つの形式があります。双方とも、先頭の空白を無視します。 :func:`eval` に対する文字列引数は、以下の形式をとらなければなりません:

.. productionlist::
   eval_input: `expression_list` NEWLINE*


.. index:: builtin: input

:func:`input` で読み込まれる入力行は、以下の形式をとらなければなりません:

.. productionlist::
   input_input: `expression_list` NEWLINE

.. index::
   object: file
   single: input; raw
   single: raw input
   builtin: raw_input
   single: readline() (file method)

注意: 文としての解釈を行わない '生の (raw)' 入力行を読み出すためには、組み込み関数 :func:`raw_input` や、ファイルオブジェクトの
:meth:`readline` メソッドを使うことができます。

