.. highlightlang:: none

.. _using-on-general:

コマンドラインと環境
=====================

CPython インタプリタはコマンドラインと環境を読み取って様々な設定を行ないます。

.. impl-detail::

   他の実装のコマンドラインスキームは CPython とは異なります。
   さらなる情報は :ref:`implementations` を参照してください。


.. _using-on-cmdline:

コマンドライン
---------------

Python を起動するとき、以下のうち任意のオプションを指定できます。 ::

    python [-BdEiOQsStuUvVWxX3?] [-c command | -m module-name | script | - ] [args]

もちろん、もっとも一般的な利用方法は、シンプルにスクリプトを実行するものです。 ::

    python myscript.py


.. _using-on-interface-options:

インターフェイスオプション
~~~~~~~~~~~~~~~~~~~~~~~~~~~

インタプリタのインターフェイスは UNIX シェルに似ていますが、
より多くのの実行方法を提供しています。

* tty デバイスに接続された標準入力とともに起動された場合、 EOF (end-of-file
  文字。 UNIX では *Ctrl-D* で、Windows では *Ctrl-Z, Enter* で入力可能)
  を受け取るまで、コマンドを受け取り、それを実行します。
* ファイル名引数を指定されるか、ファイルを標準入力に渡された場合は、
  そのファイルから読み込んだスクリプトを実行します。
* ディレクトリ名を引数に受け取ったときは、そのディレクトリから適切な
  名前のスクリプトファイルを読み込んで実行します。
* ``-c コマンド`` オプションを利用して起動された場合、 *コマンド* として渡された
  Python の文を実行します。 *コマンド* の部分には改行で区切られた複数行を指定する
  こともできます。行の先頭の空白文字は Python 文の重要要素です！
* ``-m モジュール名`` として Python モジュールパスにあるモジュールを指定された場合、
  そのモジュールをスクリプトとして実行します。

非インタラクティブモードでは、入力の全体が実行前にパースされます。

インタプリタによって消費されるオプションリストが終了したあと、継続する全ての
引数は :data:`sys.argv` に渡ります。 -- ただし、添字 0 の先頭要素(``sys.argv[0]``)
はプログラムのソース自体を示す文字列です。

.. cmdoption:: -c <command>

   *command* 内の Python コードを実行します。
   *command* は改行によって区切られた1行以上の文です。
   通常のモジュールのコードと同じく、行頭の空白文字は意味を持ちます。

   このオプションが指定された場合、 :data:`sys.argv` の先頭要素は ``"-c"`` になり、
   カレントディレクトリが :data:`sys.path` の先頭に追加されます。
   (そのディレクトリにあるモジュールをトップレベルモジュールとして import
   することが可能になります。)


.. cmdoption:: -m <module-name>

   :data:`sys.path` から指定されたモジュール名のモジュールを探し、その内容を
   :mod:`__main__` モジュールとして実行します。

   引数は *module* 名なので、拡張子 (``.py``) を含めてはいけません。
   ``module-name`` は有効な Python のモジュール名であるべきですが、実装がそれを
   強制しているとは限りません。 (例えば、ハイフンを名前に含める事を許可するかも
   しれません。)

   パッケージ名を指定することもできます。通常のモジュールの代わりにパッケージ名を
   指定された場合、インタープリタは ``<pkg>.__main__`` をメインモジュールとして
   実行します。
   この動作はインタープリタのスクリプト引数としてディレクトリやzipファイルを
   指定された時の動作と意図的に似せています。

   .. note::

      このオプションはビルトインモジュールや C で書かれた拡張モジュールには
      利用できません。 Python モジュールファイルを持っていないからです。
      しかし、コンパイル済みのモジュールは、たとえ元のソースファイルがなくても
      利用可能です。

   このオプションが指定された場合、 :data:`sys.argv` の先頭要素はモジュールファイルの
   フルパスになります。
   :option:`-c` オプションのように、カレントディレクトリが :data:`sys.path`
   の先頭に追加されます。

   .. Many standard library modules contain code that is invoked on their execution
      as a script.  An example is the :mod:`timeit` module::

   多くの標準ライブラリモジュールが、スクリプトとして実行された時のコードを持っています。
   例えば、 :mod:`timeit` モジュールは次のように実行可能です。 ::

       python -mtimeit -s 'setup here' 'benchmarked code here'
       python -mtimeit -h # for details

   .. seealso::
      :func:`runpy.run_module`
         Python コードから直接利用できる同等の機能

      :pep:`338` -- Executing modules as scripts

   .. versionadded:: 2.4

   .. versionchanged:: 2.5
      パッケージ内のモジュールを指定できるようになりました。

   .. versionchanged:: 2.7
      パッケージ名を指定したときに ``__main__`` サブモジュールを実行するようにしました。
      そのモジュールを検索している間の sys.argv[0] は ``"-m"`` に設定されるようになりました。
      (以前は間違って ``"-c"`` が設定されていました)


.. describe:: -

   標準入力 (:data:`sys.stdin`) からコマンドを読み込みます。
   標準入力がターミナルだった場合、 :option:`-i` オプションを含みます。

   このオプションが指定された場合、 :data:`sys.argv` の最初の要素は
   ``"-"`` で、カレントディレクトリが :data:`sys.path` の先頭に追加されます。


.. describe:: <script>

   *script* 内の Python コードを実行します。
   *script* は、 Python ファイル、 ``__main__.py`` ファイルを含むディレクトリ、
   ``__main__.py`` ファイルを含む zip ファイルのいづれかの、ファイルシステム上の
   (絶対あるいは相対)パスでなければなりません。

   このオプションが指定された場合、 :data:`sys.argv` の先頭要素は、
   コマンドラインで指定されたスクリプト名になります。

   スクリプト名が Python ファイルを直接指定していた場合、そのファイルを
   含むディレクトリが :data:`sys.path` の先頭に追加され、そのファイルは
   :mod:`__main__` モジュールとして実行されます。

   スクリプト名がディレクトリか zip ファイルを指定していた場合、
   スクリプト名が :data:`sys.path` に追加され、その中の ``__main__.py``
   ファイルが :mod:`__main__` モジュールとして実行されます。

   .. versionchanged:: 2.5
      トップレベルに ``__main__.py`` ファイルを持つディレクトリや zip ファイルが
      有効な Python スクリプトとなりました。

インターフェイスオプションが与えられなかった場合、 :option:`-i` が暗黙的に指定され、
``sys.argv[0]`` は空白文字列 (``""``)で、カレントディレクトリが :data:`sys.path`
の先頭に追加されます。

.. seealso::  :ref:`tut-invoking`


一般オプション
~~~~~~~~~~~~~~~

.. cmdoption:: -?
               -h
               --help

   全てのコマンドラインオプションの短い説明を表示します。

   .. versionchanged:: 2.5
      ``--help`` 形式


.. cmdoption:: -V
               --version

   Python のバージョン番号を表示して終了します。出力の例::

       Python 2.5.1

   .. versionchanged:: 2.5
      ``--version`` 形式


その他のオプション
~~~~~~~~~~~~~~~~~~~~~

.. cmdoption:: -B

   Python は import したソースモジュールの ``.pyc`` や ``.pyo`` ファイルの
   作成を試みません。
   :envvar:`PYTHONDONTWRITEBYTECODE` 環境変数も参照してください。

   .. versionadded:: 2.6


.. cmdoption:: -d

   パーサーのデバッグ出力を有効にします。(魔法使い専用です。コンパイルオプションに
   依存します)。
   :envvar:`PYTHONDEBUG` も参照してください。


.. cmdoption:: -E

   全ての :envvar:`PYTHON*` 環境変数を無視します。
   例えば、 :envvar:`PYTHONPATH` と :envvar:`PYTHONHOME` などです。

   .. versionadded:: 2.2


.. cmdoption:: -i

   最初の引数にスクリプトが指定された場合や :option:`-c` オプションが利用された場合、
   :data:`sys.stdin` がターミナルに出力されない場合も含めて、
   スクリプトかコマンドを実行した後にインタラクティブモードに入ります。
   :envvar:`PYTHONSTARTUP` ファイルは読み込みません。

   このオプションはグローバル変数や、スクリプトが例外を発生させるときにその
   スタックトレースを調べるのに便利です。 :envvar:`PYTHONINSPECT` も参照してください。


.. cmdoption:: -O

   基本的な最適化を有効にします。
   コンパイル済み (:term:`bytecode`) ファイルの拡張子を ``.pyc`` から ``.pyo``
   に変更します。 :envvar:`PYTHONOPTIMIZE` も参照してください。


.. cmdoption:: -OO

   :option:`-O` の最適化に加えて、ドキュメンテーション文字列の除去も行ないます。


.. cmdoption:: -Q <arg>

   除算制御。引数は以下のうち1つでなければなりません:

   ``old``
     int/int と long/long の除算は、 int か long を返します。 (*デフォルト*)
   ``new``
     新しい除算方式。 int/int や long/long の除算が float を返します。
   ``warn``
     古い除算方式で、 int/int や long/long 除算に警告を表示します。
   ``warnall``
     古い除算方式で、全ての除算演算子に対して警告を表示します。

   .. seealso::
      :file:`Tools/scripts/fixdiv.py`
         ``warnall`` を使っています.

      :pep:`238` -- Changing the division operator


.. cmdoption:: -s

   sys.path にユーザー site ディレクトリを追加しません。

   .. versionadded:: 2.6

   .. seealso::

      :pep:`370` -- Per user site-packages directory


.. cmdoption:: -S

   :mod:`site` モジュールのインポートを無効にし、そのモジュールで行われている
   場所独自の :data:`sys.path` 操作を無効にします。


.. cmdoption:: -t

   ソースファイルが、タブ幅に依存して意味が変わるような方法でタブ文字とスペースを
   混ぜて含んでいる場合に警告を発生させます。このオプションを2重にする (:option:`-tt`)
   とエラーになります。


.. cmdoption:: -u

   stdin, stdout, stderr のバッファを強制的に無効にします。
   関係するシステムでは、 stdin, stdout, stderr をバイナリモードにします。

   :meth:`file.readlines` や :ref:`bltin-file-objects` (``for line in sys.stdin``)
   はこのオプションに影響されない内部バッファリングをしています。
   これを回避したい場合は、 ``while 1:`` ループの中で :meth:`file.readline` します。

   :envvar:`PYTHONUNBUFFERED` も参照してください。


.. cmdoption:: -v

   モジュールが初期化されるたびに、それがどこ(ファイル名やビルトインモジュール)
   からロードされたのかを示すメッセージを表示します。
   2重に指定された場合(:option:`-vv`)は、モジュールを検索するときにチェックされた
   各ファイルに対してメッセージを表示します。また、終了時のモジュールクリーンアップに
   関する情報も提供します。 :envvar:`PYTHONVERBOSE` も参照してください。


.. cmdoption:: -W arg

   警告制御。 Python の警告機構はデフォルトでは警告メッセージを :data:`sys.stderr`
   に表示します。典型的な警告メッセージは次の形をしています::

       file:line: category: message

   デフォルトでは、各警告は発生したソース業ごとに一度だけ表示されます。
   このオプションは、警告をどれくらいの頻度で表示するかを制御します。

   複数の :option:`-W` オプションを指定することができます。警告が1つ以上の
   オプションとマッチしたときは、最後にマッチしたオプションのアクションが有効になります。
   不正な :option:`-W` オプションは無視されます。(最初の警告が発生したときに、
   不正なオプションに対する警告メッセージが表示されます。)

   Python 2.7 から、 :exc:`DeprecationWarning` とその子クラスはデフォルトで無視されます。
   :option:`-Wd` オプションを指定して有効にすることができます。

   警告は Python プログラムの中から :mod:`warnings` モジュールを利用して
   制御することができます。

   引数の一番シンプルな形は、以下のアクション文字列(かそのユニークな短縮形)
   を単体で利用するものです。

   ``ignore``
      全ての警告を無視する。
   ``default``
      明示的にデフォルトの動作(ソース行ごとに1度警告を表示する)を要求する。
   ``all``
      警告が発生するたびに表示する (これは、ループの中などで同じソース行により
      繰り返し警告が発生された場合に、大量のメッセージを表示します。)
   ``module``
      各モジュールで最初に発生した警告を表示する。
   ``once``
      プログラムで最初に発生した警告だけを表示する。
   ``error``
      警告メッセージを表示する代わりに例外を発生させる。

   引数の完全形は次のようになります::

       action:message:category:module:line

   ここで、 *action* は上で説明されたものですが、残りのフィールドにマッチした
   メッセージにだけ適用されます。空のフィールドは全ての値にマッチします。
   空のフィールドの後ろは除外されます。 *message* フィールドは表示される
   警告メッセージの先頭に、大文字小文字を無視してマッチします。 *category*
   フィールドは警告カテゴリにマッチします。これはクラス名でなければなりません。
   *category* のマッチは、メッセージの実際の警告カテゴリーが指定された警告
   カテゴリーのサブクラスかどうかをチェックします。完全なクラス名を指定しなければ
   なりません。
   *module* フィールドは、(完全正規形(fully-qualified)の) モジュール名に対して
   マッチします。このマッチは大文字小文字を区別します。
   *line* フィールドは行番号にマッチします。 0 は全ての行番号にマッチし、
   省略した時と同じです。

   .. seealso::
      :mod:`warnings` -- the warnings module

      :pep:`230` -- Warning framework

      :envvar:`PYTHONWARNINGS`


.. cmdoption:: -x

   Unix 以外の形式の ``#!cmd`` を使うために、ソースの最初の行をスキップします。
   これは、DOS専用のハックのみを目的としています。

   .. note:: エラーメッセージ内の行番号は -1 されます。

.. cmdoption:: -3

   Python 3.x との、 :ref:`2to3 <2to3-reference>` によって簡単に解決できない
   互換性の問題について警告します。以下のものが該当します。

   * :meth:`dict.has_key`
   * :func:`apply`
   * :func:`callable`
   * :func:`coerce`
   * :func:`execfile`
   * :func:`reduce`
   * :func:`reload`

   これらを使うと、 :exc:`DeprecationWarning` を発生させます。

   .. versionadded:: 2.6

使うべきでないオプション
~~~~~~~~~~~~~~~~~~~~~~~~~

.. cmdoption:: -J

   Jython_ のために予約されています。

.. _Jython: http://jython.org

.. cmdoption:: -U

   全ての文字列リテラルを、全部 unicode にします。
   このオプションはあなたの世界を破壊してしまうかもしれないので、
   このオプションを使おうとしないでください。
   これは、通常とは違うマジックナンバーを使って ``.pyc`` ファイルを生成します。
   ファイルの先頭に次のように書いて、このオプションの代わりにモジュール単位で
   unicode リテラルを有効にできます。 ::

        from __future__ import unicode_literals

   詳細は :mod:`__future__` を参照してください。


.. cmdoption:: -X

    別の Python の実装が独自の目的で利用するために予約されています。

.. _using-on-envvars:

環境変数
---------

以下の環境変数は Python の動作に影響します。

.. envvar:: PYTHONHOME

   標準 Python ライブラリの場所を変更します。デフォルトでは、ライブラリは
   :file:`{prefix}/lib/python{version}` と :file:`{exec_prefix}/lib/python{version}`
   から探されます。ここで、 :file:`{prefix}` と :file:`{exec_prefix}` は
   インストール依存のディレクトリで、両方共デフォルトでは :file:`/usr/local`
   です。

   :envvar:`PYTHONHOME` が1つのディレクトリに設定されている場合、その値は
   :file:`{prefix}` と :file:`{exec_prefix}` の両方を置き換えます。
   それらに別々の値を指定したい場合は、 :envvar:`PYTHONHOME` を
   :file:`{prefix}:{exec_prefix}` のように指定します。


.. envvar:: PYTHONPATH

   モジュールファイルのデフォルトの検索パスを追加します。
   この環境変数のフォーマットはシェルの :envvar:`PATH` と同じで、
   :data:`os.pathsep` (Unix ならコロン、 Windows ならセミコロン)
   で区切られた1つ以上のディレクトリパスです。
   存在しないディレクトリは警告なしに無視されます。

   通常のディレクトリに加えて、 :envvar:`PYTHONPATH` のエントリはピュアPython
   モジュール(ソース形式でもコンパイルされた形式でも) を含む zip ファイルを
   参照することもできます。
   拡張モジュールは zip ファイルの中から import することはできません。

   デフォルトの検索パスはインストール依存ですが、通常は
   :file:`{prefix}/lib/python{version}` で始まります。 (上の :envvar:`PYTHONHOME`
   を参照してください。)
   これは *常に* :envvar:`PYTHONPATH` に追加されます。

   上の :ref:`using-on-interface-options` で説明されているように、
   追加の検索パスディレクトリが :envvar:`PYTHONPATH` の手前に追加されます。
   検索パスは Python プログラムから :data:`sys.path` 変数として操作することが
   できます。


.. envvar:: PYTHONSTARTUP

   もし読込み可能ファイルの名前であれば、インタラクティブモードで最初のプロンプトを
   表示する前にそのファイル内の Python コマンドを実行します。
   このファイルはインタラクティブコマンドが実行されるのと同じ名前空間の中で
   実行されるので、このファイル内で定義されたり import されたオブジェクトは
   インタラクティブセッションから制限無しに利用することができます。
   このファイルで :data:`sys.ps1` と :data:`sys.ps2` を変更してプロンプトを
   変更することもできます。
   


.. envvar:: PYTHONY2K

   この変数に空でない文字列を設定すると、 :mod:`time` モジュールが
   文字列で指定される日付に4桁の年を含むことを要求するようになります。
   そうでなければ、2桁の年は :mod:`time` モジュールのドキュメントに書かれている
   ルールで変換されます。


.. envvar:: PYTHONOPTIMIZE

   この変数に空でない文字列を設定すると、 :option:`-O`
   オプションを指定したのと同じになります。
   整数を指定した場合、 :option:`-O` を複数回指定したのと
   同じになります。


.. envvar:: PYTHONDEBUG

   この変数に空でない文字列を設定すると、 :option:`-d`
   オプションを指定したのと同じになります。
   整数を指定した場合、 :option:`-d` を複数回指定したのと
   同じになります。


.. envvar:: PYTHONINSPECT

   この変数に空でない文字列を設定すると、 :option:`-i`
   オプションを指定したのと同じになります。

   この変数は Python コードから :data:`os.environ` を使って変更して、
   プログラム終了時のインスペクトモードを強制することができます。


.. envvar:: PYTHONUNBUFFERED

   この変数に空でない文字列を設定すると、 :option:`-u`
   オプションを指定したのと同じになります。


.. envvar:: PYTHONVERBOSE

   この変数に空でない文字列を設定すると、 :option:`-v`
   オプションを指定したのと同じになります。
   整数を指定した場合、 :option:`-v` を複数回指定したのと
   同じになります。


.. envvar:: PYTHONCASEOK

   この環境変数が設定されていると、 Python は :keyword:`import`
   文で大文字/小文字を区別しません。
   これは Windows でのみ動作します。


.. envvar:: PYTHONDONTWRITEBYTECODE

   この環境変数が設定されていると、 Python はソースモジュールの
   import 時に ``.pyc``, ``.pyo`` ファイルを生成しません。

   .. versionadded:: 2.6

.. envvar:: PYTHONIOENCODING

   stdin/stdout/stderr のエンコーディングを強制します。
   シンタックスは ``encodingname:errorhandler`` です。
   ``:errorhandler`` の部分はオプションで、 :func:`str.encode`
   の引数と同じ意味です。

   .. versionadded:: 2.6


.. envvar:: PYTHONNOUSERSITE

   この環境変数が設定されている場合、 Python はユーザー site ディレクトリを
   sys.path に追加しません。

   .. versionadded:: 2.6

   .. seealso::

      :pep:`370` -- Per user site-packages directory


.. envvar:: PYTHONUSERBASE

   ユーザー site ディレクトリのベースディレクトリを設定します。

   .. versionadded:: 2.6

   .. seealso::

      :pep:`370` -- Per user site-packages directory


.. envvar:: PYTHONEXECUTABLE

   この環境変数が設定されていると、 ``sys.argv[0]`` に、 C ランタイムから
   取得した値の代わりにこの環境変数の値が設定されます。
   Mac OS X でのみ動作します。

.. envvar:: PYTHONWARNINGS

   これは :option:`-W` オプションと同じです。
   カンマ区切りの文字列が設定されたとき、その動作は :option:`-W`
   を複数回指定されたのと同じになります。


デバッグモード変数
~~~~~~~~~~~~~~~~~~~~

以下の環境変数は、 :option:`--with-pydebug` ビルドオプションを指定して
構成されたデバッグビルド版の Python でのみ効果があります。

.. envvar:: PYTHONTHREADDEBUG

   設定された場合、 Python はスレッドデバッグ情報を表示します。

   .. versionchanged:: 2.6
      以前は、この変数は ``THREADDEBUG`` という名前でした。

.. envvar:: PYTHONDUMPREFS

   設定された場合、 Python はインタプリタのシャットダウン後に残っている
   オブジェクトとリファレンスカウントをダンプします。


.. envvar:: PYTHONMALLOCSTATS

   設定された場合、 Python は、新しいオブジェクトアリーナを作成するときと、
   シャットダウン時に、メモリアロケーション統計情報を表示します。

