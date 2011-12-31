.. _extending-index:

#######################################
  Python インタプリタの拡張と埋め込み
#######################################

:Release: |version|
:Date: |today|

このドキュメントでは、Python インタプリタを拡張するために C/C++
でモジュールを書く方法について述べます。
拡張モジュールでは、新たな関数を定義できるだけでなく、
新たなオブジェクト型とそのメソッドも定義できます。
このドキュメントではまた、Python インタプリタを別のアプリケーションに
埋め込み (embedding)、拡張言語として使う方法についても述べます。
また、動的に(実行時に)拡張モジュールをロードする機能をOSがサポートしている場合に、
動的ロード可能な拡張モジュールをコンパイルしてリンクする方法を示します。

このドキュメントでは、読者は Python について基礎的な知識を持ち合わせて
いるものと仮定しています。形式ばらない Python 言語の入門には、
:ref:`tutorial-index` を読んでください。
:ref:`reference-index` を読めば、
Python 言語についてより形式的な定義を得られます。
また、 :ref:`library-index` では、Python に広い適用範囲をもたらしている
既存のオブジェクト型、関数、
および (組み込み、および Python で書かれたものの両方の) モジュール
について解説しています。

Python/C API 全体の詳しい説明は、別のドキュメントである、
:ref:`c-api-index` を参照してください。

.. toctree::
   :maxdepth: 2
   :numbered:

   extending.rst
   newtypes.rst
   building.rst
   windows.rst
   embedding.rst

   jptranslation.rst
