.. highlightlang:: rest


Sphinx のビルドシステム (The Sphinx build system)
==================================================

XXX: intro...

.. _doc-build-config:


ビルド設定ファイル (The build configuration file)
--------------------------------------------------

ドキュメントのルートはソース配布の中の ``Doc`` サブディレクトリで、 ``conf.py``
という名前のファイルがそこにあります。このファイルは "ビルド設定ファイル"
と呼ばれていて、ビルド中に利用される幾つかの変数が入っています。

その変数は:

version : string
   ``|version||`` という reST 置換で利用される文字列。ドキュメントが言及している
   Python のバージョンであるべきです。これはメジャー部 (major part) とマイナー部
   (minor part) のみで構成されていて、例えばバージョン 2.5.1 でも ``2.5`` になります。

release : string
   ``|release|`` という reST 置換で利用される文字列。これは ``2.5.2b3`` のように、
   alpha/beta/release canadiate タグを含めたバージョン全体であるべきです。

``release`` と ``version`` のどちらも ``'auto'`` にすることができて、その場合
Python ソース配布物全体があれば ``Include/patchlevel.h`` ファイルから、無ければ
Sphinx を実行しているインタプリタから実行時に決定されます。

today_fmt : string
   ``|today|`` reST 置換で利用される、 ``strftime`` のフォーマット。

today : string
   ドキュメントにそのまま出力される、日付の文字列。非ゼロ (nonzero) の場合、
   ``strftime(today_fmt)`` の代わりにこちらが利用される。

unused_files : list of strings
   ビルド時に無視される reST ファイル名のリスト。一時的に無効にされたモジュールの
   ドキュメントや、まだ一般利用の準備が整っていないドキュメントに使います。

last_updated_format : string
   空白でない場合、 ``time.strftime()`` に渡されて、各出力ファイルの "last update
   on:" の後ろに書かれます。

use_smartypants : bool
   true の場合、 SmartyPants を使ってクォートやダッシュを印刷用文字への実態参照
   (typographically correct entities) へ変換します。

add_function_parentheses : bool
   true の場合、 ``:func:``, ``:meth:``, ``:cfunc:`` のクロスリファレンスに
   ``()`` を付け加えます。
