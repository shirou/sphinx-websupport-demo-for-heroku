.. highlightlang:: c


.. _concrete:

*****************************************
具象オブジェクト (concrete object) レイヤ
*****************************************

この章ではは、特定の Python オブジェクト型固有の関数について述べています。
これらの関数に間違った型のオブジェクトを渡すのは良い考えではありません;
Python プログラムから何らかのオブジェクトを受け取ったとき、
そのオブジェクトが正しい型になっているか確信をもてないのなら、
まず型チェックを行わなければなりません;
例えば、あるオブジェクトが辞書型か調べるには、 :c:func:`PyDict_Check` を使います。
この章は Python のオブジェクト型における "家計図" に従って構成されています。

.. warning::

   この章で述べている関数は、渡されたオブジェクトの型を注意深くチェックしはするものの、多くの関数は渡されたオブジェクトが有効な *NULL*
   なのか有効なオブジェクトなのかをチェックしません。これらの関数に *NULL* を渡させてしまうと、関数はメモリアクセス
   違反を起こして、インタプリタを即座に終了させてしまうはずです。


.. _fundamental:

基本オブジェクト (fundamental object)
=====================================

この節では、Python の型オブジェクトとシングルトン(singleton)オブジェクト ``None`` について述べます。

.. toctree::

   type.rst
   none.rst


.. _numericobjects:

数値型オブジェクト (numeric object)
===================================

.. index:: object: numeric

.. toctree::

   int.rst
   bool.rst
   long.rst
   float.rst
   complex.rst

.. _sequenceobjects:

シーケンスオブジェクト (sequence object)
========================================

.. index:: object: sequence

シーケンスオブジェクトに対する一般的な操作については前の章ですでに述べました;
この節では、Python 言語にもともと備わっている特定のシーケンスオブジェクトについて扱います。

.. toctree::

   bytearray.rst
   string.rst
   unicode.rst
   buffer.rst
   tuple.rst
   list.rst


.. _mapobjects:

マップ型オブジェクト (mapping object)
=====================================

.. index:: object: mapping

.. toctree::

   dict.rst

.. _otherobjects:

その他のオブジェクト
====================

.. toctree::

   class.rst
   function.rst
   method.rst
   file.rst
   module.rst
   iterator.rst
   descriptor.rst
   slice.rst
   weakref.rst
   capsule.rst
   cobject.rst
   cell.rst
   gen.rst
   datetime.rst
   set.rst
   code.rst

