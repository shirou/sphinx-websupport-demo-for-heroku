初めに
======

.. Python's documentation has long been considered to be good for a free
.. programming language.  There are a number of reasons for this, the most
.. important being the early commitment of Python's creator, Guido van Rossum, to
.. providing documentation on the language and its libraries, and the continuing
.. involvement of the user community in providing assistance for creating and
.. maintaining documentation.

Python のドキュメントは長い間、フリーなプログラミング言語としては良いものであると
考えられてきました。その理由は多々ありますが、最も重要なのは、
Python の作者である Guido van Rossum が、言語やそのライブラリの
ドキュメントの提供と、ドキュメントの作成と維持の手助けする上での
ユーザコミュニティの継続的な参加に早期から関わっていたことです。

.. The involvement of the community takes many forms, from authoring to bug reports
.. to just plain complaining when the documentation could be more complete or
.. easier to use.

コミュニティの参加には、バグ報告の作成から、単にドキュメントをより
完全で利用しやすいものにできる場合に素朴な提案をするといったこと
まで、いくつものやりかたがあります。

.. This document is aimed at authors and potential authors of documentation for
.. Python.  More specifically, it is for people contributing to the standard
.. documentation and developing additional documents using the same tools as the
.. standard documents.  This guide will be less useful for authors using the Python
.. documentation tools for topics other than Python, and less useful still for
.. authors not using the tools at all.

このドキュメントは、Python のドキュメントの作者、あるいは潜在的な
作者向けのものです。もっと具体的にいうと、標準ドキュメントに貢献
したり、標準ドキュメントと同じツールを使って別のドキュメントを
開発する人々向けです。
このガイドは Python 以外のトピックに Python ドキュメント作成
ツールを使う作者にとってはあまり有用ではなく、ツールを全く使用しない
作者にもあまり有用ではないでしょう。

.. If your interest is in contributing to the Python documentation, but you don't
.. have the time or inclination to learn reStructuredText and the markup structures
.. documented here, there's a welcoming place for you among the Python contributors
.. as well.  Any time you feel that you can clarify existing documentation or
.. provide documentation that's missing, the existing documentation team will
.. gladly work with you to integrate your text, dealing with the markup for you.
.. Please don't let the material in this document stand between the documentation
.. and your desire to help out!

仮に、あなたが Python のドキュメントを寄贈したいと思っている一方で、
reStructuredText を学んだり、このドキュメントに書かれているマークアップ構造を
学んだりする時間や気力を持てないとしても、あなたを Python プロジェクト
への協力者として迎え入れる余地はあります。
既存のドキュメントを改善したり、欠けているドキュメントを提供して
もらえるなら、現在のドキュメント製作チームがいつでも喜んでマークアップ
を行い、テキストを組み込みます。手助けしたいという気持ちをお持ちなら、
このドキュメントに書かれていることを障害のように思わないでくださいね！
