==============
ロギング HOWTO
==============

:Author: Vinay Sajip <vinay_sajip at red-dove dot com>

.. _logging-basic-tutorial:

.. currentmodule:: logging

基本ロギングチュートリアル
--------------------------

ロギングは、あるソフトウェアが実行されているときに起こったイベントを
追跡するための手段です。ソフトウェアの開発者は、特定のイベントが
発生したことを示すロギングの呼び出しをコードに加えます。
イベントは、メッセージで記述され、これに変数データ (すなわち、イベントが
起こる度に異なるかもしれないデータ) を加えることもできます。
イベントには、開発者がそのイベントに定めた重要性も含まれます。
重要性は、 *レベル (level)* や *重大度 (severity)* とも呼ばれます。

ロギングを使うべきとき
^^^^^^^^^^^^^^^^^^^^^^

logging は、単純なロギングの用法に便利な関数群を提供しています。
この中には、 :func:`debug`, :func:`info`, :func:`warning`, :func:`error` および
:func:`critical` があります。logging を使うべき時を決めるには、
よくあるタスクに使う最適なツールを述べた、以下のテーブルを参照してください。

+-----------------------------------+------------------------------------------+
| 行いたいタスク                    | そのタスクに最適なツール                 |
+===================================+==========================================+
| コマンドラインスクリプトや        | :func:`print`                            |
| プログラムで普通に使う、          |                                          |
| コンソール出力の表示              |                                          |
+-----------------------------------+------------------------------------------+
| プログラムの通常の操作中に        | :func:`logging.info` (または、           |
| 発生したイベントの報告            | 診断のための特に詳細な出力には           |
| (例えば、状態の監視や障害の分析)  | :func:`logging.debug`)                   |
+-----------------------------------+------------------------------------------+
| 特定のランタイムイベントに        | その発行が避けられるもので、             |
| 関わる警告の発行                  | クライアントアプリケーションを           |
|                                   | 修正してその警告を排除するべきなら       |
|                                   | :func:`warnings.warn`                    |
|                                   |                                          |
|                                   | アプリケーションにできることはないが、   |
|                                   | それでもイベントを記録するべきなら       |
|                                   | :func:`logging.warning`                  |
+-----------------------------------+------------------------------------------+
| 特定のランタイムイベントに        | 例外の送出                               |
| 関わるエラーの報告                |                                          |
+-----------------------------------+------------------------------------------+
| 例外の送出をしないエラーの抑制    | 特定のエラーやアプリケーションドメインに |
| (例えば、長期のサーバプロセス中の | 応じて :func:`logging.error`,            |
| エラーハンドラ)                   | :func:`logging.exception` または         |
|                                   | :func:`logging.critical`                 |
+-----------------------------------+------------------------------------------+

ロギング関数は、そのイベントのレベルや重大度から名前を付けられ、
それが追跡に使われます。標準のレベルとその適用範囲は、
以下に (重大度が増す順に) 記述されています

+--------------+---------------------------------------------+
| レベル       | 使われるとき                                |
+==============+=============================================+
| ``DEBUG``    | おもに問題を診断するときにのみ関心が        |
|              | あるような、詳細な情報                      |
+--------------+---------------------------------------------+
| ``INFO``     | 想定された通りのことが起こったことの確認    |
|              |                                             |
+--------------+---------------------------------------------+
| ``WARNING``  | 想定外のことが起こった、または問題が近く    |
|              | 起こりそうである (例えば、'disk space low') |
|              | ことの表示                                  |
+--------------+---------------------------------------------+
| ``ERROR``    | より重大な問題により、ソフトウェアが        |
|              | ある機能を実行できないこと                  |
+--------------+---------------------------------------------+
| ``CRITICAL`` | プログラム自体が実行を続けられないことを    |
|              | 表す、重大なエラー                          |
+--------------+---------------------------------------------+

デフォルトのレベルは ``WARNING`` で、logging パッケージが他に設定されなければ、
このレベル以上のイベントのみ追跡されます。

追跡されるイベントは、異なる方法で処理されます。追跡されたイベントを
処理する最も単純な方法は、それをコンソールに表示することです。
その他のよくある方法は、それをディスクファイルに書き出すことです。


.. _howto-minimal-example:

簡単な例
^^^^^^^^

ごく簡単な例は::

   import logging
   logging.warning('Watch out!') # will print a message to the console
   logging.info('I told you so') # will not print anything

これらの行をスクリプトにタイプして実行すると、次のようにコンソールに
出力されます::

   WARNING:root:Watch out!

デフォルトのレベルは ``WARNING`` なので、 ``INFO`` メッセージは現れません。
表示されたメッセージには、レベルの表示と、ロギングの呼び出しで
提供された、イベントの説明すなわち 'Watch out!' が含まれます。
'root' の部分は今は気にしないでください。あとで説明します。実際の出力は、
必要に応じてかなり柔軟に書式化できます。書式化操作もあとで説明します。


ファイルへのロギング
^^^^^^^^^^^^^^^^^^^^

非常によくある状況として、ロギングイベントのファイルへの記録が
挙げられますから、次はそれを見てみましょう::

   import logging
   logging.basicConfig(filename='example.log',level=logging.DEBUG)
   logging.debug('This message should go to the log file')
   logging.info('So should this')
   logging.warning('And this, too')

そして、ファイルを開いて何が起こったか見てみると、このようなログメッセージが
見つかるでしょう::

   DEBUG:root:This message should go to the log file
   INFO:root:So should this
   WARNING:root:And this, too

この例はまた、追跡のしきい値となるロギングレベルを設定する方法も示しています。
この例では、しきい値を ``DEBUG`` に設定しているので、全てのメッセージが
表示されています。

ロギングレベルをコマンドラインオプションから次のように設定したいなら::

   --log=INFO

``--log`` に渡されたパラメタの値をある変数 *loglevel* に保存すれば::

   getattr(logging, loglevel.upper())

を使い、 *level* 引数を通して :func:`basicConfig` に渡すべき値を得られます。
ユーザの入力値をすべてエラーチェックしたいこともあり、以下のように
なるかもしれません::

   # assuming loglevel is bound to the string value obtained from the
   # command line argument. Convert to upper case to allow the user to
   # specify --log=DEBUG or --log=debug
   numeric_level = getattr(logging, loglevel.upper(), None)
   if not isinstance(numeric_level, int):
       raise ValueError('Invalid log level: %s' % loglevel)
   logging.basicConfig(level=numeric_level, ...)

:func:`basicConfig` は、 :func:`debug` や :func:`info` を
最初に呼び出す *前* に呼び出さなければなりません。
これは、一度限りの単純な設定機能を意図しているので、
実際に作用するのは最初の呼び出しのみで、
続く呼び出しの効果は no-op です。

上記のスクリプトを複数回実行すると、2 回目以降の実行によるメッセージは
*example.log* に加えられます。以前の実行によるメッセージを記憶せず、
実行ごとに新たに始めたいなら、上記の例での呼び出しを次のように変え、
*filemode* 引数を指定することができます::

   logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

出力は先ほどと同じになりますが、ログファイルは追記されるのではなくなり、
以前の実行によるメッセージは失われます。


複数のモジュールからのロギング
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

プログラムが複数のモジュールでできているなら、そのロギングをどのように
構成するかの例はこちらです::

   # myapp.py
   import logging
   import mylib

   def main():
       logging.basicConfig(filename='myapp.log', level=logging.INFO)
       logging.info('Started')
       mylib.do_something()
       logging.info('Finished')

   if __name__ == '__main__':
       main()

::

   # mylib.py
   import logging

   def do_something():
       logging.info('Doing something')

*myapp.py* を実行すると、 *myapp.log* には、おそらく期待したとおりに、
次のように書き込まれるでしょう::

   INFO:root:Started
   INFO:root:Doing something
   INFO:root:Finished

この *mylib.py* でのパターンは、複数のモジュールに一般化できます。なお、
この簡単な使用パターンでは、ログファイルを見ることで、
イベントの説明は見られますが、
アプリケーションの *どこから* メッセージが来たのかを知ることはできません。 
メッセージの位置を追跡したいなら、このチュートリアルレベルを超えた
ドキュメントが必要になります -- :ref:`logging-advanced-tutorial` を
参照してください。


変数データのロギング
^^^^^^^^^^^^^^^^^^^^

変数データのログを取るには、イベント記述メッセージにフォーマット文字列を使い、
引数に変数データを加えてください。例えば::

   import logging
   logging.warning('%s before you %s', 'Look', 'leap!')

により、次のように表示されます::

   WARNING:root:Look before you leap!

ご覧の通り、イベント記述メッセージに変数データを統合するために、
古い、% スタイルの文字列フォーマットを使っています。これは後方互換性の
ためです。logging パッケージは、 :meth:`str.format` や :class:`string.Template`
のような新しいフォーマットオプションよりも先に生まれました。
新しいフォーマットオプションはサポートされて *います* が、
その探求はこのチュートリアルでは対象としません。


表示されるメッセージのフォーマットの変更
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

メッセージを表示するのに使われるフォーマットを変更するには、
使いたいフォーマットを指定する必要があります::

   import logging
   logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
   logging.debug('This message should appear on the console')
   logging.info('So should this')
   logging.warning('And this, too')

すると次のように表示されます::

   DEBUG:This message should appear on the console
   INFO:So should this
   WARNING:And this, too

ご覧の通り、先の例に現れた 'root' が消失しています。フォーマット文字列に
含めることができるものの一覧は、 :ref:`logrecord-attributes` のドキュメント
から参照できますが、単純な用途では、必要なものは *levelname* (重大度)、
*message* (変数データを含むイベント記述)、それともしかしたら、イベントが
いつ起こったかという表示だけです。これは次の節で解説します。


メッセージ内での日付と時刻の表示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

イベントの日付と時刻を表示するには、フォーマット文字列に '%(asctime)s' を
置いてください::

   import logging
   logging.basicConfig(format='%(asctime)s %(message)s')
   logging.warning('is when this event was logged.')

のようにすると、このように表示されます::

   2010-12-12 11:41:42,612 is when this event was logged.

(上で示した) 日付と時刻表示のデフォルトフォーマットは ISO8601 です。
日付と時刻のフォーマットを詳細に制御するには、この例のように、 ``basicConfig``
に *datefmt* 変数を与えてください::

   import logging
   logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
   logging.warning('is when this event was logged.')

すると、このように表示されるでしょう::

   12/12/2010 11:46:36 AM is when this event was logged.

*datefmt* 引数のフォーマットは、 :func:`time.strftime` で
サポートされているものと同じです。


次のステップ
^^^^^^^^^^^^

基本チュートリアルはこれで終わりです。あなたがロギングを使っていくためには、
これで十分でしょう。logging パッケージが提供するものはもっとありますが、
それを使いこなすためには、もうちょっと時間をかけて、以下のセクションを
読む必要があります。その用意ができたら、好きな飲み物を持って、次に
進みましょう。

ロギングを簡潔に行いたいなら、上記の例を使って、ロギングをあなたのスクリプトに
組み込んでください。そして問題があったり、理解出来ないことがあったら、
comp.lang.python Usenet group
(http://groups.google.com/group/comp.lang.python から利用できます)
に質問を投稿してくだされば、そう遠くないうちに助けが得られるでしょう。

まだいますか？もう少し上級の、踏み込んだチュートリアルを綴った、
幾つかの節を読み続けることができます。その後で、
:ref:`logging-cookbook` もご覧ください。

.. _logging-advanced-tutorial:


上級ロギングチュートリアル
--------------------------

logging ライブラリはモジュール方式のアプローチを取り、いくつかのカテゴリの
部品を提供します。ロガー、ハンドラ、フィルタ、フォーマッタです。

* ロガーは、アプリケーションコードが直接使うインタフェースを公開します。
* ハンドラは、(ロガーによって生成された) ログ記録を適切な送信先に送ります。
* フィルタは、どのログ記録を出力するかを決定する、きめ細かい機能を提供します。
* フォーマッタは、ログ記録が最終的に出力されるレイアウトを指定します。

ロギングは、 :class:`Logger` クラスのインスタンス (以下 :dfn:`ロガー`) に
メソッドを呼び出すことで実行されます。各インスタンスには名前があり、
名前空間階層構造に、ドット (ピリオド) をセパレータとして、
概念的に並べられています。例えば、 'scan' という名前のロガーは、ロガー
'scan.text', 'scan.html' および 'scan.pdf'の親です。ロガー名は、何でも
望むものにでき、ロギングされたメッセージが発生した場所を指し示します。

ロガーに名前をつけるときの良い習慣は、ロギングを使う各モジュールに、
以下のように名付けられた、モジュールレベルロガーを使うことです::

   logger = logging.getLogger(__name__)

これにより、ロガー名はパッケージ/モジュール階層をなぞり、
ロガー名だけで、どこでイベントのログが取られたか、直感的に明らかになります。

ロガーの階層構造の根源は、ルートロガーと呼ばれます。それが、関数 :func:`debug`,
:func:`info`, :func:`warning`, :func:`error` および :func:`critical`
によって使われるロガーとなります。これらの関数は単に、ルートロガーの同名の
メソッドを呼び出します。これらの関数とメソッドは、同じ署名をもっています。
ルートロガーの名前は、ログ出力では 'root' と表示されます。

もちろん、メッセージを異なる送信先に記録することも出来ます。
このパッケージでは、ファイルへ、 HTTP GET/POST 先へ、
SMTP 経由で電子メールへ、汎用のソケットへ、または Windows NT イベントログの
ような OS 毎のログ記録機構への、ログメッセージの書きこみが
サポートされています。送信先は、 :dfn:`handler` クラスによって取り扱われます。
組み込みのハンドラクラスでは満たせないような、特殊な要件があるなら、
独自のログ送信先を生成できます。

デフォルトでは、どのロギングメッセージに対しても、送信先は設定されていません。
チュートリアルの例のように、 :func:`basicConfig` を使って、送信先
(コンソールやファイルなど) を指定できます。関数 :func:`debug`, :func:`info`,
:func:`warning`, :func:`error` および :func:`critical` を呼び出すと、
それらは送信先が設定されていないかを調べます。そして設定されていなければ、
ルートロガーに委譲して実際にメッセージを出力する前に、
コンソール (``sys.stderr``) を送信先に、デフォルトのフォーマットを表示される
メッセージに設定します。

:func:`basicConfig` によって設定される、メッセージの
デフォルトのフォーマットはこうです::

   severity:logger name:message

:func:`basicConfig` の *format* キーワード引数にフォーマット文字列を渡すことで、
これを変更できます。フォーマット文字列を構成するためのすべてのオプションは、
:ref:`formatter-objects` を参照してください。


ロガー
^^^^^^

:class:`Logger` オブジェクトの仕事は大きく三つに分かれます。
一つ目は、アプリケーションが実行中にメッセージを記録できるように、
いくつかのメソッドをアプリケーションから呼べるようにしています。
二つ目に、ロガーオブジェクトはどのメッセージに対して作用するかを、
深刻度 (デフォルトのフィルタ機構) またはフィルタオブジェクトに基づいて決定します。
三つ目に、ロガーオブジェクトは関心を持っているすべてのログハンドラに関連するログメッセージを回送します。

とりわけ広く使われるロガーオブジェクトのメソッドは、二つのカテゴリーに分類できます:
設定とメッセージ送信です。

これらが設定メソッドの中でよく使われます:

* :meth:`Logger.setLevel` はロガーが扱うログメッセージの最も低い深刻度を指定します。
  組み込みの深刻度の中では DEBUG が一番低く、 CRITICAL が一番高くなります。
  たとえば、深刻度が INFO と設定されたロガーは INFO, WARNING, ERROR, CRITICAL
  のメッセージしか扱わず、 DEBUG メッセージは無視します。

* :meth:`Logger.addHandler` と :meth:`Logger.removeHandler` は、
  ハンドラオブジェクトをロガーオブジェクトから追加または削除します。
  ロガーオブジェクトにハンドラオブジェクトを追加または削除します。
  ハンドラについては、 :ref:`handler-basic` で詳しく述べます。

* :meth:`Logger.addFilter` と :meth:`Logger.removeFilter` は
  ロガーオブジェクトにフィルタオブジェクトを追加または削除します。
  フィルタについては、 :ref:`filter` で詳しく述べます。

これらのメソッドを、生成したすべてのロガーに毎回呼び出さなければ
ならないわけではありません。最後の 2 段落を参照してください。

ロガーオブジェクトが設定されれば、以下のメソッドがログメッセージを生成します。

* :meth:`Logger.debug`, :meth:`Logger.info`, :meth:`Logger.warning`,
  :meth:`Logger.error`, :meth:`Logger.critical` はすべて、
  メッセージとメソッド名に対応したレベルでログ記録を作り出します。
  メッセージは実際にはフォーマット文字列であり、通常の文字列代入に使う
  :const:`%s`, :const:`%d`, :const:`%f` などを含むことができます。
  残りの引数はメッセージの代入される位置に対応するオブジェクトのリストです。
  :const:`**kwargs` については、ログ記録メソッドが気にするキーワードは
  :const:`exc_info` だけで、例外の情報をログに記録するかを決定するのに使います。

* :meth:`Logger.exception` は :meth:`Logger.error` と似たログメッセージを作成します。
  違いは :meth:`Logger.exception` がスタックトレースを一緒にダンプすることです。
  例外ハンドラでだけ使うようにしてください。

* :meth:`Logger.log` はログレベルを明示的な引数として受け取ります。
  これは上に挙げた便宜的なログレベル毎のメソッドを使うより少しコード量が多くなりますが、
  独自のログレベルを使うことができます。

:func:`getLogger` は、指定されればその特定の名前の、そうでなければ ``root`` のロガーインスタンスへの参照を返します。
ロガーの名前はピリオド区切りの階層構造を表します。
同じ名前で :func:`getLogger` を複数回呼び出した場合、同一のロガーオブジェクトへの参照が返されます。
階層リストを下ったロガーはリスト上位のロガーの子です。
たとえば、名前が ``foo`` であるロガーがあったとして、
``foo.bar``, ``foo.bar.baz``, ``foo.bam`` といった名前のロガーはすべて ``foo`` の子孫になります。

ロガーには、 *有効レベル (effective level)* の概念があります。
ロガーにレベルが明示的に設定されていなければ、代わりに親のレベルが
その有効レベルとして使われます。親のレベルが設定されなければ、 *その*
親のレベルが確かめられ、以下同様に、明示的に設定されたレベルが見つかるまで
祖先が探されます。ルートロガーは、必ず明示的なレベルが設定されています
(デフォルトでは ``WARNING`` です)。イベントを処理するかを決定するとき、
ロガーの有効レベルを使って、イベントがロガーのハンドラに渡されるかが
決められます。

子ロガーはメッセージを親ロガーのハンドラに伝えます。
このため、アプリケーションが使っているすべてのロガーのためのハンドラを定義して設定する必要はありません。
トップレベルのロガーのためのハンドラだけ設定しておいて必要に応じて子ロガーを作成すれば十分です。
(しかし、ロガーの *propagate* 属性を *False* に設定することで、
伝播を抑制できます。)


.. _handler-basic:

ハンドラ
^^^^^^^^

:class:`Handler` オブジェクトは適切なログメッセージを
(ログメッセージの深刻度に基づいて) ハンドラの指定された出力先に振り分けることに責任を持ちます。
ロガーオブジェクトには :func:`addHandler` メソッドで 0 個以上のハンドラを追加することができます。
例として、あるアプリケーションがすべてのログメッセージをログファイルに、
error 以上のすべてのログメッセージを標準出力に、
critical のメッセージはすべてメールアドレスに、
それぞれ送りたいとします。
この場合、 3 つの個別のハンドラがそれぞれの深刻度と宛先に応じて必要になります。

このライブラリには多くのハンドラが用意されています (:ref:`useful-handlers` を
参照してください) が、このチュートリアルでは :class:`StreamHandler` と
:class:`FileHandler` だけを例に取り上げます。

アプリケーション開発者にとってハンドラを扱う上で気にするべきメソッドは極々限られています。
組み込みのハンドラオブジェクトを使う (つまり自作ハンドラを作らない)
開発者に関係あるハンドラのメソッドは、次の設定用のメソッドだけでしょう:

* :meth:`Handler.setLevel` メソッドは、ロガーオブジェクトの場合と同様に、
  適切な出力先に振り分けられるべき最も低い深刻度を指定します。
  なぜ 2 つも :func:`setLevel` メソッドがあるのでしょうか?
  ロガーで設定されるレベルは、付随するハンドラにどんな深刻度のメッセージを渡すか決めます。
  ハンドラで設定されるレベルは、ハンドラがどのメッセージを送るべきか決めます。

* :func:`setFormatter` でこのハンドラが使用する Formatter オブジェクトを選択します。

* :func:`addFilter` および :func:`removeFilter` はそれぞれハンドラへのフィルタオブジェクトの設定と解除を行います。

アプリケーションのコード中では :class:`Handler` のインスタンスを直接インスタンス化して使ってはなりません。
代わりに、 :class:`Handler` クラスはすべてのハンドラが持つべきインターフェイスを定義し、
子クラスが使える (もしくはオーバライドできる) いくつかのデフォルトの振る舞いを規定します。


フォーマッタ
^^^^^^^^^^^^

フォーマッタオブジェクトは最終的なログメッセージの順序、構造および内容を設定します。
基底クラスである :class:`logging.Handler` とは違って、
アプリケーションのコードはフォーマッタクラスをインスタンス化しても構いません。
特別な振る舞いをさせたいアプリケーションではフォーマッタのサブクラスを使う可能性もあります。
コンストラクタは二つのオプション引数を取ります -- メッセージのフォーマット文字列と日付のフォーマット文字列です。

.. method:: logging.Formatter.__init__(fmt=None, datefmt=None)

メッセージのフォーマット文字列がなければ、デフォルトではメッセージをそのまま使います。
日付のフォーマット文字列がなければ、デフォルトは::

    %Y-%m-%d %H:%M:%S

で、最後にミリ秒が付きます。

メッセージのフォーマット文字列は ``%(<dictionary key>)s`` 形式の文字列代入を用います。
使えるキーについては :ref:`logrecord-attributes` に書いてあります。

次のメッセージフォーマット文字列は、人が読みやすい形式の時刻、メッセージの深刻度、
およびメッセージの内容を、順番に出力します::

    '%(asctime)s - %(levelname)s - %(message)s'

フォーマッタは、ユーザが設定できる関数を使って、生成時刻をタプルに記録します。
デフォルトでは、 :func:`time.localtime` が使われます。特定の
フォーマッタインスタンスに対してこれを変更するには、インスタンスの
``converter`` 属性を :func:`time.localtime` や :func:`time.gmtime` と同じ
署名をもつ関数に設定してください。すべてのフォーマッタインスタンスに対して
これを変更するには、例えば全てのロギング時刻を GMT で表示するには、
フォーマッタクラスの ``converter`` 属性を (GMT 表示の ``time.gmtime`` に)
設定してください。


ロギングの環境設定
^^^^^^^^^^^^^^^^^^

.. currentmodule:: logging.config

プログラマは、ロギングを 3 種類の方法で設定できます:

1. 上述の設定メソッドを呼び出す Python コードを明示的に使って、
   ロガー、ハンドラ、そしてフォーマッタを生成する
2. ロギング設定ファイルを作り、それを :func:`fileConfig` 関数を使って読み込む
3. 設定情報の辞書を作り、それを :func:`dictConfig` 関数に渡す

最後の2つの選択肢については、 :ref:`logging-config-api` で解説しています。
以下の例では、Python コードを使って、とても簡単なロガー、コンソールハンドラ、
そして簡単なフォーマッタを設定しています::

    import logging

    # create logger
    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

このモジュールを実行すると、コマンドラインによって以下の出力がなされます::

    $ python simple_logging_module.py
    2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
    2005-03-19 15:10:26,620 - simple_example - INFO - info message
    2005-03-19 15:10:26,695 - simple_example - WARNING - warn message
    2005-03-19 15:10:26,697 - simple_example - ERROR - error message
    2005-03-19 15:10:26,773 - simple_example - CRITICAL - critical message

以下の Python モジュールは、ロガー、ハンドラ、フォーマッタをほとんど
上述の例と同じように生成していますが、オブジェクト名だけが異なります::

    import logging
    import logging.config

    logging.config.fileConfig('logging.conf')

    # create logger
    logger = logging.getLogger('simpleExample')

    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

これが logging.conf ファイルです::

    [loggers]
    keys=root,simpleExample

    [handlers]
    keys=consoleHandler

    [formatters]
    keys=simpleFormatter

    [logger_root]
    level=DEBUG
    handlers=consoleHandler

    [logger_simpleExample]
    level=DEBUG
    handlers=consoleHandler
    qualname=simpleExample
    propagate=0

    [handler_consoleHandler]
    class=StreamHandler
    level=DEBUG
    formatter=simpleFormatter
    args=(sys.stdout,)

    [formatter_simpleFormatter]
    format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
    datefmt=

出力は、設定ファイルに基づく例とだいたい同じです::

    $ python simple_logging_config.py
    2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
    2005-03-19 15:38:55,979 - simpleExample - INFO - info message
    2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
    2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
    2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message

この通り、設定ファイルの方法は、主に設定とコードが分かれ、
非コーダがロギングプロパティを変えやすくなるという点で、
Python コードの方法より少し優れています。

.. currentmodule:: logging

なお、設定ファイルで参照されるクラス名は、logging モジュールに対して
相対であるか、通常のインポート機構を使って解決される絶対である値で
なければなりません。従って、(logging モジュールに相対な)
:class:`~logging.handlers.WatchedFileHandler` または
(Python インポートパスとして ``mypackage`` が使えるとき、パッケージ
``mypackage`` のモジュール ``mymodule`` で定義されたクラスに)
``mypackage.mymodule.MyHandler`` のどちらかが使えます。

Python 2.7 では、、ロギングを設定するのに新しく、辞書に設定情報を持たせる
手段が導入されました。これは、上で概説した設定ファイルに基づく方法による機能の
上位版を提供し、新しいアプリケーションやデプロイにはこのメソッドが
推奨されます。Python の辞書を使って設定情報を保持し、辞書は他の用途にも
使えるので、設定の選択肢が広がります。例えば、JSON フォーマットの
設定ファイルや、YAML 処理機能が使えれば YAML フォーマットのファイルを使って、
設定辞書を構成できます。また、もちろん、Python コードで辞書を構成し、
ソケットを通して pickle 化された形式を受け取るなど、アプリケーションで
意味があるいかなるやり方でも使えます。

ここに、YAML フォーマットにおける新しい辞書に基づく方法での、
上述の例と同じ設定の例を挙げます::

    version: 1
    formatters:
      simple:
        format: format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
    handlers:
      console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: simple
        stream: ext://sys.stdout
    loggers:
      simpleExample:
        level: DEBUG
        handlers: [console]
        propagate: no
    root:
      level: DEBUG
      handlers: [console]

辞書を使ったロギングについて詳細は、 :ref:`logging-config-api` を
参照してください。

環境設定が与えられないとどうなるか
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ロギング環境設定を与えられないと、ロギングイベントを出力しなければ
ならないのに、イベントを出力するハンドラが見つからないことがあります。
この状況での logging パッケージの振る舞いは、Python のバージョンに依ります。

Python 2.x では、振る舞いは以下の通りです:

* *logging.raiseExceptions* が *False* (製品モード) なら、
  イベントは黙って捨てられます。

* *logging.raiseExceptions* が *True* (開発モード) なら、
  メッセージ 'No handlers could be found for logger X.Y.Z' が一度表示されます。

.. _library-config:

ライブラリのためのロギングの設定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ロギングを使うライブラリを開発するときは、ライブラリがどのようにロギングを
使うのか、例えば使われているロガーの名前などを、
ドキュメントにしておくべきです。ロギングの設定については、いくつか
考えておくべきこともあります。使っているアプリケーションがロギングを
使っていなくて、ライブラリコードがロギングを呼び出すと、
(前の節で解説したように) 重大度 ``WARNING`` 以上のイベントが、
``sys.stderr`` に表示されます。これが最高のデフォルトの振る舞いと見なされます。

何らかの理由で、ロギング設定がなされていないときにメッセージを表示
*させたくない* なら、あなたのライブラリのトップレベルロガーに
何もしないハンドラを取り付けられます。このハンドラは何も処理しないと
いうだけで、全てのライブラリイベントに対してハンドラが見つかるので、
メッセージが表示されることを防げます。ライブラリのユーザがアプリケーションでの
使用のためにロギングを設定したら、それはおそらくハンドラを追加する
設定でしょうが、そしてレベルが適切に設定されたら、ライブラリコード内で
なされたロギングの呼び出しは、通常通りそのハンドラに出力を送るようになります。

何もしないハンドラ :class:`~logging.NullHandler` (Python 2.7 以降) は、
logging パッケージに含まれます。このハンドラのインスタンスを、
(ロギング設定がなされていないときにライブラリのログイベントを ``sys.stderr``
に出力させたく *ないなら*)
ライブラリの名前空間で使われるトップレベルロガーに取り付けられます。
ライブラリ *foo* によるすべてのロギングが、 'foo.x', 'foo.x.y' その他に
該当する名前のロガーによってなされるなら::

    import logging
    logging.getLogger('foo').addHandler(logging.NullHandler())

とすれば望んだ効果が得られるでしょう。組織が複数のライブラリを作り出すなら、
指定されるロガー名は単に 'foo' ではなく、 'orgname.foo' になります。

**注意事項:** *ライブラリのロガーには、* :class:`~logging.NullHandler` *以外の
ハンドラを追加しない* ことを強く推奨します。これは、ハンドラの設定が、
あなたのライブラリを使うアプリケーション開発者に伝播するからです。
アプリケーション開発者は、対象となる聴衆と、そのアプリケーションに
どのハンドラが最も適しているかを知っているからです。ハンドラを
'ボンネットの中で' 加えてしまうと、ユニットテストをして必要に応じた
ログを送達する能力に干渉しかねません。


ロギングレベル
--------------

ログレベルの数値は以下の表のように与えられています。
これらは基本的に自分でレベルを定義したい人のためのもので、
定義するレベルを既存のレベルの間に位置づけるためには具体的な値が必要になります。
もし数値が他のレベルと同じだったら、既存の値は上書きされその名前は失われます。

+--------------+------+
| レベル       | 数値 |
+==============+======+
| ``CRITICAL`` | 50   |
+--------------+------+
| ``ERROR``    | 40   |
+--------------+------+
| ``WARNING``  | 30   |
+--------------+------+
| ``INFO``     | 20   |
+--------------+------+
| ``DEBUG``    | 10   |
+--------------+------+
| ``NOTSET``   | 0    |
+--------------+------+

レベルはロガーに関連付けることもでき、開発者が設定することも、保存されたログ記録設定を読み込む際に設定することもできます。
ロガーに対してログ記録メソッドが呼び出されると、ロガーは自らのレベルとメソッド呼び出しに関連付けられたレベルを比較します。
ロガーのレベルがメソッド呼び出しのレベルよりも高い場合、実際のログメッセージは生成されません。
これはログ出力の冗長性を制御するための基本的なメカニズムです。

ログ記録されるメッセージは :class:`~logging.LogRecord` クラスのインスタンスとしてエンコードされます。
ロガーがあるイベントを実際にログ出力すると決定した場合、
ログメッセージから :class:`~logging.LogRecord` インスタンスが生成されます。

ログ記録されるメッセージは、ハンドラ (:dfn:`handlers`) を通してディスパッチ機構にかけられます。
ハンドラは :class:`Handler` クラスのサブクラスのインスタンスで、
ログ記録された (:class:`LogRecord` 形式の) メッセージが、
そのメッセージの伝達対象となる相手 (エンドユーザ、サポートデスクのスタッフ、
システム管理者、開発者) に行き着くようにする役割を持ちます。
ハンドラには特定の出力先を意図された :class:`LogRecord` インスタンスが渡されます。
各ロガーは 0 個以上のハンドラを (:class:`Logger` の :meth:`addHandler` メソッド) で関連付けることができます。
ロガーに直接関連付けられたハンドラに加えて、\ *ロガーの上位にあるロガーすべてに関連付けられたハンドラ* がメッセージを処理する際に呼び出されます。
(ただしロガーの *propagate* フラグが false 値にセットされている場合を除きます。
その場合は、祖先ハンドラへの伝搬はそこで止まります。)

ロガーと同様に、ハンドラは関連付けられたレベルを持つことができます。
ハンドラのレベルはロガーのレベルと同じ方法で、フィルタとして働きます。
ハンドラがあるイベントを実際に処理すると決定した場合、
:meth:`~Handler.emit` メソッドが使われ、メッセージを出力先に送信します。
ほとんどのユーザ定義の :meth:`~Handler.emit` のサブクラスで、
この :meth:`emit` をオーバライドする必要があるでしょう。

.. _custom-levels:

カスタムレベル
^^^^^^^^^^^^^^

独自のレベルを定義することは可能ですが、必須ではなく、実経験上は既存のレベルが
選ばれます。しかし、カスタムレベルが必要だと確信するなら、レベルの定義には
多大な注意を払うべきで、 *ライブラリの開発の際、カスタムレベルを定義することは
とても悪いアイデア* になり得ます。これは、複数のライブラリの作者がみな独自の
カスタムレベルを定義すると、与えられた数値が異なるライブラリで異なる意味に
なりえるため、開発者がこれを制御または解釈するのが難しくなるからです。

.. _useful-handlers:

便利なハンドラ
--------------

基底の :class:`Handler` クラスに加え、多くの便利なサブクラスが
提供されています:

#. :class:`StreamHandler` インスタンスは、メッセージをストリーム
   (ファイル風オブジェクト) に送ります。

#. :class:`FileHandler` インスタンスは、メッセージをディスクファイルに
   送ります。

#. :class:`~handlers.BaseRotatingHandler` は、ある地点でログファイルを
   循環させるハンドラの基底クラスです。これを直接インスタンス化することは
   意図されていません。代わりに、 :class:`~handlers.RotatingFileHandler` や
   :class:`~handlers.TimedRotatingFileHandler` を使用してください。

#. :class:`~handlers.RotatingFileHandler` インスタンスは、メッセージを
   ディスクファイルに送り、最大ログファイル数とログファイル循環を
   サポートします。

#. :class:`~handlers.TimedRotatingFileHandler` インスタンスは、メッセージを
   ディスクファイルに送り、ログファイルを特定時間のインターバルで循環します。

#. :class:`~handlers.SocketHandler` インスタンスは、メッセージを TCP/IP
   ソケットに送ります。

#. :class:`~handlers.DatagramHandler` インスタンスは、メッセージを UDP
   ソケットに送ります。

#. :class:`~handlers.SMTPHandler` インスタンスは、メッセージを
   指示された email アドレスに送ります。

#. :class:`~handlers.SysLogHandler` インスタンスは、メッセージを、必要ならば
   リモートマシンの、Unix syslog daemon に送ります。

#. :class:`~handlers.NTEventLogHandler` インスタンスは、メッセージを
   Windows NT/2000/XP イベントログに送ります。

#. :class:`~handlers.MemoryHandler` インスタンスは、メッセージを、
   特定の基準が満たされる度に流される、メモリ中のバッファに送ります。

#. :class:`~handlers.HTTPHandler` インスタンスは、メッセージを、 ``GET``
   または ``POST`` セマンティクスを使って、HTTP サーバに送ります。

#. :class:`~handlers.WatchedFileHandler` インスタンスは、ロギングする先の
   ファイルを監視します。ファイルが変更されると、そのファイルは閉じられ、
   ファイル名を使って再び開かれます。このハンドラは Unix 系のシステムにのみ
   便利です。Windows は、使われている基の機構をサポートしていません。

   :class:`NullHandler` インスタンスは、エラーメッセージに対して何もしません。
   これは、ライブラリ開発者がロギングを使いたいが、ライブラリのユーザが
   ロギングを設定してなくても 'No handlers could be found for logger XXX'
   メッセージを表示させたくない場合に使われます。
   詳しい情報は :ref:`library-config` を参照してください。

.. versionadded:: 2.7
   :class:`NullHandler` クラス。

コア logging パッケージで、 :class:`NullHandler`, :class:`StreamHandler`
および :class:`FileHandler` クラスが定義されています。
その他のハンドラは、サブモジュールの :mod:`logging.handlers` で
定義されています。(環境設定機能のためのサブモジュール、 :mod:`logging.config`
もあります。)

ログメッセージは、 :class:`Formatter` クラスのインスタンスを通して
フォーマット化してから表示されます。このインスタンスは、 % 演算子と辞書で
使うのに適切なフォーマット文字列で初期化されます。

複数のメッセージを一括してフォーマット化するには、 :class:`BufferingFormatter` 
が使えます。(一連の文字列のそれぞれに適用される) フォーマット文字列に加え、
ヘッダとトレーラフォーマット文字列も提供されています。

ロガーレベルおよび/またはハンドラレベルに基づくフィルタリングで十分でなければ、
:class:`Filter` のインスタンスを :class:`Logger` と :class:`Handler`
インスタンスの両方に (:meth:`addFilter` を通して) 加えることができます。
メッセージの処理を続ける前に、ロガーもハンドラも、全てのフィルタに許可を
求めます。フィルタのいずれかが偽値を返したら、メッセージの処理は
続けられません。

基本の :meth:`addFilter` 機能では、特定のロガー名でのフィルタリングをできます。
この機能が使われると、指名されたロガーに送られたメッセージとその子だけが
フィルタを通り、その他は落とされます。


.. _logging-exceptions:

ログ記録中に発生する例外
------------------------

logging パッケージは、ログを生成している間に起こる例外を飲み込むように
設計されています。これは、ログ記録イベントを扱っている間に発生するエラー
(ログ記録の設定ミス、ネットワークまたは他の同様のエラー) によって
ログ記録を使用するアプリケーションが早期に終了しないようにするためです。

:class:`SystemExit` と :class:`KeyboardInterrupt` 例外は決して飲み込まれません。
:class:`Handler` サブクラスの :meth:`emit` メソッドの間に起こる他の例外は、
:meth:`handleError` メソッドに渡されます。

:class:`Handler` の :meth:`handleError` のデフォルト実装は、
モジュールレベル変数 :data:`raiseExceptions` が設定されているかどうかチェックします。
設定されているなら、トレースバックが :data:`sys.stderr` に出力されます。
設定されていないなら、例外は飲み込まれます。

**Note:** :data:`raiseExceptions` のデフォルト値は ``True`` です。
これは、開発の間に起こるどんな例外についても通常は通知してほしいからです。
実運用環境では :data:`raiseExceptions` を ``False`` に設定することをお勧めします。

.. currentmodule:: logging

.. _arbitrary-object-messages:

任意のオブジェクトをメッセージに使用する
----------------------------------------

前の節とそこで挙げた例では、イベントを記録するときに渡されたメッセージが
文字列であると仮定していました。しかし、これは唯一の可能性ではありません。
メッセージとして任意のオブジェクトを渡すことができます。
そして、ロギングシステムがそのオブジェクトを文字列表現に変換する必要があるとき、
オブジェクトの :meth:`__str__` メソッドが呼び出されます。
実際、そうしたければ、文字列表現を計算することを完全に避けることができます -
例えば、 :class:`SocketHandler` は、イベントを pickle してネットワーク上で送信することでログ出力します。


最適化
------

message 引数の整形は、必要になるまで延期されます。
しかしながら、ログ記録メソッドに渡す引数を計算するだけでもコストがかかる場合があります。
ロガーが単にイベントを捨てるなら、その計算を避けたいと考えるかもしれません。
どうするかを決定するために :meth:`isEnabledFor` メソッドを呼ぶことができます。
このメソッドは引数にレベルを取って、そのレベルの呼び出しに対して Logger がイベントを生成するなら true を返します。
このようにコードを書くことができます::

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Message with %s, %s', expensive_func1(),
                                            expensive_func2())

このようにすると、ロガーの閾値が ``DEBUG`` より上に設定されている場合、
:func:`expensive_func1` と :func:`expensive_func2` の呼び出しは行われません。

これ以外にも、どんなログ情報が集められるかについてより正確なコントロールを必要とする、
特定のアプリケーションでできる最適化があります。
これは、ログ記録の間の不要な処理を避けるためにできることのリストです:

+-------------------------------------------+-------------------------------------------+
| 不要な情報                                | それを避ける方法                          |
+===========================================+===========================================+
| 呼び出しがどこから行われたかに関する情報  | ``logging._srcfile`` を ``None`` にする   |
+-------------------------------------------+-------------------------------------------+
| スレッド情報                              | ``logging.logThreads`` を ``0`` にする    |
+-------------------------------------------+-------------------------------------------+
| プロセス情報                              | ``logging.logProcesses`` を ``0`` にする  |
+-------------------------------------------+-------------------------------------------+

また、コア logging モジュールが基本的なハンドラだけを含んでいることに注意してください。
:mod:`logging.handlers` と :mod:`logging.config` をインポートしなければ、
余分なメモリを消費することはありません。

.. seealso::

   Module :mod:`logging`
      logging モジュールの API リファレンスです。

   Module :mod:`logging.config`
      logging モジュールの環境設定 API です。

   Module :mod:`logging.handlers`
      logging モジュールに含まれる、便利なハンドラです。

   :ref:`ロギングクックブック <logging-cookbook>`

