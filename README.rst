This is a copy of the Python Double Metaphone algorithm, taken from
http://atomboy.isa-geek.com/plone/Members/acoil/programing/double-metaphone/metaphone.py
and algorithm originally by Lawrence Philips, with some bug fixes to the
core algorithm, and other minor improvements.

I use it on Theatricalia to do people name matching, and it appears to work
quite well, e.g. http://theatricalia.com/search?q=chuck+iwugee

The database stores the double metaphones for first and last names, and then
upon searching simply computes the double metaphones of what has been entered
and looks up anything that matches.

