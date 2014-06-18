~~~~~~~~~
Metaphone
~~~~~~~~~

.. contents::
   :depth: 2
   :backlinks: top
   :local:

About
=====

Metaphone
---------
As described on the `Wikipedia page`_, the original Metaphone algorithm was
published in 1990 as an improvement over the `Soundex`_ algorithm. Like
Soundex, it was limited to English-only use. The Metaphone algorithm does not
produce phonetic representations of an input word or name; rather, the output
is an intentionally approximate phonetic representation. The approximate
encoding is necessary to account for the way speakers vary their pronunciations
and misspell or otherwise vary words and names they are trying to spell.

Double Metaphone
----------------
The Double Metaphone phonetic encoding algorithm is the second generation of
the Metaphone algorithm. Its implementation was described in the June 2000
issue of C/C++ Users Journal. It makes a number of fundamental design
improvements over the original Metaphone algorithm.

It is called "Double" because it can return both a primary and a secondary code
for a string; this accounts for some ambiguous cases as well as for multiple
variants of surnames with common ancestry. For example, encoding the name
"Smith" yields a primary code of SM0 and a secondary code of XMT, while the
name "Schmidt" yields a primary code of XMT and a secondary code of SMT--both
have XMT in common.

Double Metaphone tries to account for myriad irregularities in English of
Slavic, Germanic, Celtic, Greek, French, Italian, Spanish, Chinese, and other
origin. Thus it uses a much more complex ruleset for coding than its
predecessor; for example, it tests for approximately 100 different contexts of
the use of the letter C alone.

History
-------
This is a copy of the Python Double Metaphone algorithm, taken from `Andrew
Collins' work`_, a Python implementation of an algorithm in C originally
created by Lawrence Philips. Since then, improvements have been made by several
contributors, viewable in the git history.

A ``resources`` directory is included with this project which contains the
following:

* the original C++ file by Lawrence Philips

* Kevin Atkinson's improvements to it

* a C implementation (for use in a Perl extension) by Maurice Aubrey

The contributors of the Python version, originally started by Andrew Collins
include:

* Andrew Collins

* Chris Leong

* Matthew Somerville

* Richard Barran

* Maximillian Dornseif

* Sebastien Metrot

* Duncan McGreggor

Usage
=====

Running the Unit Tests
----------------------
``metaphone`` uses the ``unittest`` package from the standard library, and as
such, its tests are runnable by most test runners. If you have `nose`_ installed,
you can do the following::

  $ git clone https://github.com/oubiwann/metaphone.git
  $ cd metaphone
  $ nosetests -v .

If you have Twisted installed, you can do::

  $ trial ./metaphone

Example Code
------------

The unit tests are full of examples, so be sure to check those out. But here's
a taste::

  $ python
  >>> from metaphone import doublemetaphone
  >>> doublemetaphone("architect")
  ("ARKTKT", "")
  >>> doublemetaphone("bajador")
  ("PJTR", "PHTR")

In the Wild
===========

The following developers/projects make use of this library:

* `Andrew Collins`_ used his original code in various music projects and
  dealing with misspelled text from data provided by various web services. This
  was then integrated with Plone/Zope projects.

* `Matthew Somerville`_ uses it on Theatricalia to do people name matching, and
  it appears to work `quite well`_. The database stores the double metaphones
  for first and last names, and then upon searching simply computes the double
  metaphones of what has been entered and looks up anything that matches.

* `Duncan McGreggor`_ uses it on the `φarsk project`_ to provide greater full
  text search capabilities for Indo-European language word lists and
  dictionaries.

.. Links
.. _Wikipedia page: http://en.wikipedia.org/wiki/Metaphone#Double_Metaphone
.. _Soundex: http://en.wikipedia.org/wiki/Soundex
.. _Andrew Collins' work: http://www.atomodo.com/code/double-metaphone/metaphone.py/view
.. _Andrew Collins: http://www.atomodo.com/
.. _Matthew Somerville: https://github.com/dracos/
.. _Duncan McGreggor: https://github.com/oubiwann/
.. _quite well: http://theatricalia.com/search?q=chuck+iwugee
.. _φarsk project: https://github.com/oubiwann/tharsk
.. _nose: https://nose.readthedocs.org/
