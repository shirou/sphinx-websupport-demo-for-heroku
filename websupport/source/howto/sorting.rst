.. _sortinghowto:

ソート HOW TO
*************

:Author: Andrew Dalke and Raymond Hettinger
:Release: 0.1

..
  Python lists have a built-in :meth:`list.sort` method that modifies the list
  in-place.  There is also a :func:`sorted` built-in function that builds a new
  sorted list from an iterable.

Python のリストにはリストをインプレースに変更する、
組み込みメソッド :meth:`list.sort` があります。
他にもイテラブルからソートしたリストを作成する
組み込み関数 :func:`sorted` があります。

..
  In this document, we explore the various techniques for sorting data using Python.

このドキュメントでは Python を使った様々なソートのテクニックを探索します。

..
  Sorting Basics
  ==============

ソートの基本
============

..
  A simple ascending sort is very easy: just call the :func:`sorted` function. It
  returns a new sorted list::

単純な昇順のソートはとても簡単です: :func:`sorted` 関数を呼ぶだけです。
そうすれば、新たにソートされたリストが返されます::

    >>> sorted([5, 2, 3, 1, 4])
    [1, 2, 3, 4, 5]

..
  You can also use the :meth:`list.sort` method of a list. It modifies the list
  in-place (and returns *None* to avoid confusion). Usually it's less convenient
  than :func:`sorted` - but if you don't need the original list, it's slightly
  more efficient.

リストの :meth:`list.sort` メソッドを呼びだしても同じことができます。
この方法はリストをインプレースに変更します
(そして sorted との混乱を避けるため *None* を返します)。
多くの場合、こちらの方法は :func:`sorted` と比べると不便です
- ただし、元々のリストが不要な場合には、わずかですがより効率的です。

    >>> a = [5, 2, 3, 1, 4]
    >>> a.sort()
    >>> a
    [1, 2, 3, 4, 5]

..
  Another difference is that the :meth:`list.sort` method is only defined for
  lists. In contrast, the :func:`sorted` function accepts any iterable.

違いは他にもあります、 :meth:`list.sort` メソッドはリストにのみ定義されています。
一方 :func:`sorted` 関数は任意のイテラブルを受け付けます。

    >>> sorted({1: 'D', 2: 'B', 3: 'B', 4: 'E', 5: 'A'})
    [1, 2, 3, 4, 5]

..
  Key Functions
  =============

Key 関数
========

..
  Starting with Python 2.4, both :meth:`list.sort` and :func:`sorted` added a
  *key* parameter to specify a function to be called on each list element prior to
  making comparisons.

Python 2.4 から、 :meth:`list.sort` と :func:`sorted` には *key* パラメータが追加されました、
これは比較を行う前にリストの各要素に対して呼び出される関数を指定するパラメータです。

..
  For example, here's a case-insensitive string comparison:

例えば、大文字小文字を区別しない文字列比較の例:

    >>> sorted("This is a test string from Andrew".split(), key=str.lower)
    ['a', 'Andrew', 'from', 'is', 'string', 'test', 'This']

..
  The value of the *key* parameter should be a function that takes a single argument
  and returns a key to use for sorting purposes. This technique is fast because
  the key function is called exactly once for each input record.

*key* パラメータは単一の引数をとり、ソートに利用される key を
返さなければいけません。この制約によりソートを高速に行えます、
キー関数は各入力レコードに対してきっちり一回だけ呼び出されるからです。

..
  A common pattern is to sort complex objects using some of the object's indices
  as keys. For example:

よくある利用パターンはいくつかの要素から成る対象を
インデクスのどれかをキーとしてソートすることです。例えば:

    >>> student_tuples = [
        ('john', 'A', 15),
        ('jane', 'B', 12),
        ('dave', 'B', 10),
    ]
    >>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

..
  The same technique works for objects with named attributes. For example:

同じテクニックは名前づけされた属性 (named attributes) を使うことで
オブジェクトに対しても動作します。
例えば:

    >>> class Student:
            def __init__(self, name, grade, age):
                self.name = name
                self.grade = grade
                self.age = age
            def __repr__(self):
                return repr((self.name, self.grade, self.age))

    >>> student_objects = [
        Student('john', 'A', 15),
        Student('jane', 'B', 12),
        Student('dave', 'B', 10),
    ]
    >>> sorted(student_objects, key=lambda student: student.age)   # sort by age
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

..
  Operator Module Functions
  =========================

operator モジュール関数
=======================

..
  The key-function patterns shown above are very common, so Python provides
  convenience functions to make accessor functions easier and faster. The operator
  module has :func:`operator.itemgetter`, :func:`operator.attrgetter`, and
  starting in Python 2.5 a :func:`operator.methodcaller` function.

上述した key 関数のパターンはとても一般的です、
そのため、Python は高速で扱いやすいアクセサ関数を提供しています。
operator モジュールには :func:`operator.itemgetter`, 
:func:`operator.attrgetter`, そして Python 2.5 から利用できるようになった
:func:`operator.methodcaller` 関数があります。

..
  Using those functions, the above examples become simpler and faster:

これらの関数を利用すると、上の例はもっと簡単で高速になります:

    >>> from operator import itemgetter, attrgetter

    >>> sorted(student_tuples, key=itemgetter(2))
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

    >>> sorted(student_objects, key=attrgetter('age'))
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

..
  The operator module functions allow multiple levels of sorting. For example, to
  sort by *grade* then by *age*:

operator モジュールの関数は複数の段階でのソートを可能にします。
例えば、 *grade* でソートしてさらに *age* でソートする場合:

    >>> sorted(student_tuples, key=itemgetter(1,2))
    [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

    >>> sorted(student_objects, key=attrgetter('grade', 'age'))
    [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

..
  Ascending and Descending
  ========================

昇順と降順
==========

..
  Both :meth:`list.sort` and :func:`sorted` accept a *reverse* parameter with a
  boolean value. This is using to flag descending sorts. For example, to get the
  student data in reverse *age* order:

:meth:`list.sort` と :func:`sorted` の両方とも *reverse* パラメータを
真偽値として受け付けます。このパラメータは降順ソートを行うかどうかの
フラグとして利用されます。
例えば、学生のデータを *age* の逆順で得たい場合は:

    >>> sorted(student_tuples, key=itemgetter(2), reverse=True)
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

    >>> sorted(student_objects, key=attrgetter('age'), reverse=True)
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

..
  Sort Stability and Complex Sorts
  ================================

ソートの安定性と複合的なソート
==============================

..
  Starting with Python 2.2, sorts are guaranteed to be `stable
  <http://en.wikipedia.org/wiki/Sorting_algorithm#Stability>`_\. That means that
  when multiple records have the same key, their original order is preserved.

Python 2.2 からソートは、 `stable
<http://en.wikipedia.org/wiki/Sorting_algorithm#Stability>`_
であることが保証されるようになりました。
これはレコードの中に同じキーがある場合、
元々の順序が維持されるということを意味します。

    >>> data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
    >>> sorted(data, key=itemgetter(0))
    [('blue', 1), ('blue', 2), ('red', 1), ('red', 2)]

..
  Notice how the two records for *blue* retain their original order so that
  ``('blue', 1)`` is guaranteed to precede ``('blue', 2)``.

二つの *blue* のレコートが元々の順序を維持して、
``('blue', 1)`` が ``('blue', 2)`` の前にあること注意してください。

..
  This wonderful property lets you build complex sorts in a series of sorting
  steps. For example, to sort the student data by descending *grade* and then
  ascending *age*, do the *age* sort first and then sort again using *grade*:

この素晴しい性質によって複数のソートを段階的に組み合わせることができます。
例えば、学生データを *grade* の降順にソートし、さらに *age* の昇順に
ソートしたい場合には、まず *age* でソートし、
次に *grade* でもう一度ソートします:

    >>> s = sorted(student_objects, key=attrgetter('age'))     # sort on secondary key
    >>> sorted(s, key=attrgetter('grade'), reverse=True)       # now sort on primary key, descending
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

..
  The `Timsort <http://en.wikipedia.org/wiki/Timsort>`_ algorithm used in Python
  does multiple sorts efficiently because it can take advantage of any ordering
  already present in a dataset.

Python では `Timsort <http://en.wikipedia.org/wiki/Timsort>`_ アルゴリズムが
利用されていて、効率良く複数のソートを行うことができます、
これは現在のデータセット中のあらゆる順序をそのまま利用できるからです。

..
  The Old Way Using Decorate-Sort-Undecorate
  ==========================================

デコレート-ソート-アンデコレート を利用した古いやり方
=====================================================

..
  This idiom is called Decorate-Sort-Undecorate after its three steps:
  
  * First, the initial list is decorated with new values that control the sort order.
  
  * Second, the decorated list is sorted.
  
  * Finally, the decorations are removed, creating a list that contains only the
    initial values in the new order.

このイディオムは以下の3つのステップにちなんで 
デコレート-ソート-アンデコレート (Decorate-Sort-Undecorate) と呼ばれています。

* まず、元となるリストをソートしたい順序を制御する新しい値でデコレートします。

* 次に、デコレートしたリストをソートします。

* 最後に、デコレートを取り除き、新しい順序で元々の値のみを持つリストを作ります。

..
  For example, to sort the student data by *grade* using the DSU approach:

例えば、DSU アプローチを利用して学生データを *grade* でソートする場合:

    >>> decorated = [(student.grade, i, student) for i, student in enumerate(student_objects)]
    >>> decorated.sort()
    >>> [student for grade, i, student in decorated]               # undecorate
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

..
  This idiom works because tuples are compared lexicographically; the first items
  are compared; if they are the same then the second items are compared, and so
  on.

このイディオムはタブルが辞書編集的に比較されるため正しく動作します;
最初の要素が比較され、同じ場合には第二の要素が比較され、以下も同様に動きます。

..
  It is not strictly necessary in all cases to include the index *i* in the
  decorated list, but including it gives two benefits:
  
  * The sort is stable -- if two items have the same key, their order will be
    preserved in the sorted list.
  
  * The original items do not have to be comparable because the ordering of the
    decorated tuples will be determined by at most the first two items. So for
    example the original list could contain complex numbers which cannot be sorted
    directly.

デコレートしたリストのインデクス *i* は全ての場合で含まれる必要はありませんが、
そうすることで二つの利点があります:

* ソートが安定になります -- もし二つの要素が同じキーを持つ場合、
  それらの順序がソートされたリストでも維持されます。

* 元々の要素が比較可能な要素を持つとは限りません、
  なぜならデコレートされたタブルの順序は多くの場合、
  最初の二つの要素で決定されるからです。
  例として元のリストは直接比較できない複素数を含むことができます。

..
  Another name for this idiom is
  `Schwartzian transform <http://en.wikipedia.org/wiki/Schwartzian_transform>`_\,
  after Randal L. Schwartz, who popularized it among Perl programmers.

このイディオムの別名に
`Schwartzian transform <http://en.wikipedia.org/wiki/Schwartzian_transform>`_
があります。
これは Perl プログラマの間で有名な Randal L. Schwartz にちなんでいます。

..
  For large lists and lists where the comparison information is expensive to
  calculate, and Python versions before 2.4, DSU is likely to be the fastest way
  to sort the list. For 2.4 and later, key functions provide the same
  functionality.

巨大なリストや比較の情報を得る計算が高くつくリストに対するソートや
Python のバージョンが 2.4 より前の場合には、
DSU はリストをソートするのに最速な方法のようです。
2.4 以降では、key 関数が同じ機能を提供します。

..
  The Old Way Using the *cmp* Parameter
  =====================================

*cmp* パラメータを利用した古い方法
==================================

..
  Many constructs given in this HOWTO assume Python 2.4 or later. Before that,
  there was no :func:`sorted` builtin and :meth:`list.sort` took no keyword
  arguments. Instead, all of the Py2.x versions supported a *cmp* parameter to
  handle user specified comparison functions.

この HOWTO の内容の多くは Python 2.4 以降を仮定しています。
それ以前では 組み込み関数 :func:`sorted` と :meth:`list.sort` は
キーワード引数をとりませんでした。
その代わりに Py2.x バージョンの全ては、ユーザが比較関数を指定するための
*cmp* パラメーターをサポートしました。

..
  In Py3.0, the *cmp* parameter was removed entirely (as part of a larger effort to
  simplify and unify the language, eliminating the conflict between rich
  comparisons and the :meth:`__cmp__` magic method).

Py3.0 では *cmp* パラメータは完全に削除されました
(ぜいたくな比較と :meth:`__cmp__` マジックメソッドの衝突を除き、
言語を単純化しまとるための多大な労力の一環として)

..
  In Py2.x, sort allowed an optional function which can be called for doing the
  comparisons. That function should take two arguments to be compared and then
  return a negative value for less-than, return zero if they are equal, or return
  a positive value for greater-than. For example, we can do:

Py2.x ではソートにオプションとして比較に利用できる関数を与えることができます。
関数は比較される二つの引数をとり、小さい場合には負の値を、等しい場合には
0 を、大きい場合には正の値を返さなければいけません。
例えば、以下のようにできます:

    >>> def numeric_compare(x, y):
            return x - y
    >>> sorted([5, 2, 4, 1, 3], cmp=numeric_compare)
    [1, 2, 3, 4, 5]

..
  Or you can reverse the order of comparison with:

また、比較順を逆にすることもできます:

    >>> def reverse_numeric(x, y):
            return y - x
    >>> sorted([5, 2, 4, 1, 3], cmp=reverse_numeric)
    [5, 4, 3, 2, 1]

..
  When porting code from Python 2.x to 3.x, the situation can arise when you have
  the user supplying a comparison function and you need to convert that to a key
  function. The following wrapper makes that easy to do::

Python 2.x から 3.x にコードを移植する場合、
比較関数を持っている場合には key 関数に比較しなければならないような
状況に陥るかもしれません。
以下のラッパーがそれを簡単にしてくれるでしょう::

    def cmp_to_key(mycmp):
        'Convert a cmp= function into a key= function'
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K

..
  To convert to a key function, just wrap the old comparison function:

key 関数を変換するには、古い比較関数をラップするだけです:

    >>> sorted([5, 2, 4, 1, 3], key=cmp_to_key(reverse_numeric))
    [5, 4, 3, 2, 1]

..
  In Python 2.7, the :func:`functools.cmp_to_key` function was added to the
  functools module.

Python 2.7 には、functools モジュールに :func:`functools.cmp_to_key` 関数が
追加されました。

..
  Odd and Ends
  ============

残りいくつかとまとめ
====================

..
  * For locale aware sorting, use :func:`locale.strxfrm` for a key function or
    :func:`locale.strcoll` for a comparison function.

* ロケールに注意したソートをするには、キー関数 :func:`locale.strxfrm` を
  利用するか、比較関数に :func:`locale.strcoll` を利用します。

..
  * The *reverse* parameter still maintains sort stability (i.e. records with
    equal keys retain the original order). Interestingly, that effect can be
    simulated without the parameter by using the builtin :func:`reversed` function
    twice:

* *reverse* パラメータはソートの安定性を保ちます
  (つまり、レコードのキーが等しい場合元々の順序が維持されます)。
  面白いことにこの影響はパラメータ無しで :func:`reversed` 関数を
  二回使うことで模倣することができます:

    >>> data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
    >>> assert sorted(data, reverse=True) == list(reversed(sorted(reversed(data))))

..
  * The sort routines are guaranteed to use :meth:`__lt__` when making comparisons
    between two objects. So, it is easy to add a standard sort order to a class by
    defining an :meth:`__lt__` method::

* ソートルーチンは二つのオブジェクトを比較するのに
  :meth:`__lt__` を利用することを保証しています。
  そのため :meth:`__lt__` メソッドを定義することで、
  標準のソート順序を追加できます。

    >>> Student.__lt__ = lambda self, other: self.age < other.age
    >>> sorted(student_objects)
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

..
  * Key functions need not depend directly on the objects being sorted. A key
    function can also access external resources. For instance, if the student grades
    are stored in a dictionary, they can be used to sort a separate list of student
    names:

* key 関数はソートするオブジェクトに依存する必要はありません。
  key 関数は外部リソースにアクセスすることもできます。
  例えば学生の成績が辞書に保存されている場合、それを利用して
  別の学生の名前のリストをソートすることができます:

  >>> students = ['dave', 'john', 'jane']
  >>> newgrades = {'john': 'F', 'jane':'A', 'dave': 'C'}
  >>> sorted(students, key=newgrades.__getitem__)
  ['jane', 'dave', 'john']
