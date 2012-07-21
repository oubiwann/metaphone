~~~~~~~~~~~~~~~~
Double Metaphone
~~~~~~~~~~~~~~~~

About
=====

TBD

The Implementation
==================
This is a copy of the Python Double Metaphone algorithm, taken from `Andrew
Collins' work`_, a Python implementation of an algorithm in C originally
created by Lawrence Philips. Since then, improvements have been made by several
contributors.

Users
=====

* `Matthew Somerville`_ uses it on Theatricalia to do people name matching, and
  it appears to work `quite well`_. The database stores the double metaphones
  for first and last names, and then upon searching simply computes the double
  metaphones of what has been entered and looks up anything that matches.

* `Duncan McGreggor`_ uses it on the `φarsk project`_ to provide greater full
  text search capabilities for Indo-European language word lists and
  dictionaries.

.. Links
.. _Andrew Collins' work: http://atomboy.isa-geek.com/plone/Members/acoil/programing/double-metaphone/metaphone.py
.. _Matthew Somerville: https://github.com/dracos/
.. _Duncan McGreggor: https://github.com/oubiwann/
.. _quite well: http://theatricalia.com/search?q=chuck+iwugee
.. _φarsk project: https://github.com/oubiwann/tharsk
