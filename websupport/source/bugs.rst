.. _reporting-bugs:

****************
 問題を報告する
****************

Python は安定性について高い評価を得た、成熟した言語です。
この評価を守るために、開発者たちはあなたが見つけた Python の不備を知りたいと
思っています。

ドキュメントの問題
==================
..
   If you find a bug in this documentation or would like to propose an improvement,
   please send an e-mail to docs@python.org describing the bug and where you found
   it.  If you have a suggestion how to fix it, include that as well.

このドキュメントに問題を発見したり、改善したいと思った場合、その場所と問題を
説明したメールを docs@python.org に送ってください。
もし修正案があれば、それも同じメールに書いてください。

..
   docs@python.org is a mailing list run by volunteers; your request will be
   noticed, even if it takes a while to be processed.

doc@python.org はボランティアによって運営されているメーリングリストです。
あなたの要望は、処理されるまでに暫く掛かってしまうかもしれませんが、
無視されることはないはずです。

..
   Of course, if you want a more persistent record of your issue, you can use the
   issue tracker for documentation bugs as well.

もし問題をしっかり記録しておきたいのであれば、もちろんドキュメントの問題に
ついても 課題管理システム (Issue Tracker) を利用することができます。


.. Using the Python issue tracker

Python の課題管理システムを使う
================================

Python 自体の問題の報告は Python Bug Tracker (http://bugs.python.org/) に
投稿してください。この課題管理システムは、関連情報を入力して開発者に報告するための
Web フォームを提供しています。

問題報告の最初のステップは、その問題がすでの報告済みのものかどうかを判断することです。
報告済みの問題かどうかを判断するメリットとして、開発者の時間を節約する以外にも、
その問題を解決するために既に何が行われているのかを知ることができるというものもあります。
問題は解決済みで次のリリースで解決されるかもしれませんし、さらなる情報を必要としている
(そしてあなたがその上方を提供できる)かもしれません。
そのため、ページの先頭にある検索ボックスを使って、バグデータベースから検索してください。

もし問題がまだ課題管理システムに登録されていない場合、課題管理システムのトップページに
戻ってログインしてください。もし課題管理システムのアカウントをもっていないのであれば、
サイドバーの "Register" リンクを選ぶか、 OpenID を使う場合は OpenID プロバイダの
ロゴをクリックしてください。匿名での問題報告はできません。

ログインできたら、バグを登録できます。サイドバーの "Create New" リンクから
バグ報告フォームを開きます。

バグ報告フォームには幾つかのフィールドがあります。
"Title" フィールドには、問題の概要を *非常に* 簡潔に書いてください。
10語以下くらいが目安です。 "Type" フィールドでは、問題の種類を選択してください。
問題と関係する "Component" と "Versions" も選択してください。

"Comment" フィールドで、問題の詳細を、あなたが期待した結果と実際の結果も含めて
説明してください。拡張モジュール[#]_ が関係しているかどうか、どのハードウェアと
ソフトウェアプラットフォームを使っているか(適切なバージョン情報も含めて)なども
報告に含めてください。
詳細な課題解決ワークフローについては、 http://www.python.org/dev/workflow/
を参照してください。

.. rubric:: 注記

.. [#] 訳注：原文ではextension moduleですが、これはC言語で書かれたモジュールという
       意味ではなくて、広義で非標準ライブラリを指しているかもしれません。

各バグ報告は開発者に割り当てられ、その人がその問題を修正するのに何が必要かを決定します。
そのバグ報告に対して何かアクションがあるたびに、更新情報があなたにメールで届きます。


.. seealso::

   `How to Report Bugs Effectively <http://www.chiark.greenend.org.uk/~sgtatham/bugs.html>`_
      有益なバグ報告について詳しく説明した記事です。
      どんな情報が、なぜ有益なのかを説明しています。

   `Bug Writing Guidelines <http://developer.mozilla.org/en/docs/Bug_writing_guidelines>`_
      良いバグ報告を書くための情報です。
      この情報の一部はMozillaプロジェクト独自のものですが、一般的に良いプラクティスを
      解説しています。

