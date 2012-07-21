# -*- coding: utf-8 -*-
"""
The original Metaphone algorithm was published in 1990 as an improvement over
the Soundex algorithm. Like Soundex, it was limited to English-only use. The
Metaphone algorithm does not produce phonetic representations of an input word
or name; rather, the output is an intentionally approximate phonetic
representation. The approximate encoding is necessary to account for the way
speakers vary their pronunciations and misspell or otherwise vary words and
names they are trying to spell.

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
"""
# This script implements the Double Metaphone algorithm (c) 1998, 1999 by
# Lawrence Philips it was translated to Python from the C source written by
# Kevin Atkinson (http://aspell.net/metaphone/) By Andrew Collins - January 12,
# 2007 who claims no rights to this work
# http://www.atomodo.com/code/double-metaphone/metaphone.py/view
# Updated 2007-02-14 - Found a typo in the 'gh' section (0.1.1)
# Updated 2007-12-17 - Bugs fixed in 'S', 'Z', and 'J' sections (0.1.2;
#                      Chris Leong)
# Updated 2009-03-05 - Various bug fixes against the reference C++
#                      implementation (0.2; Matthew Somerville)
# XXX changes from 2010 haven't been integrated yet -- version 0.3
# Updated 2012-07-11 - Fixed long lines, added more docs, changed function name
#                      (0.4; Duncan McGreggor)
import unicodedata


VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y']
SILENT_STARTERS = ["GN", "KN", "PN", "WR", "PS"]


class Word(object):
    """
    """
    def __init__(self, input):
        self.original = input
        self.decoded = input.decode('utf-8', 'ignore')
        self.normalized = ''.join(
            (c for c in unicodedata.normalize('NFD', self.decoded)
            if unicodedata.category(c) != 'Mn'))
        self.upper = self.normalized.upper()
        self.length = len(self.upper)
        self.prepad = "--"
        self.start_index = len(self.prepad)
        self.last = self.start_index + self.length - 1
        self.postpad = "------"
        # so we can index beyond the begining and end of the input string
        self.buffer = self.prepad + self.upper + self.postpad

    @property
    def is_slavo_germanic(self):
        return (
            self.upper.find('W') > -1
            or self.upper.find('K') > -1
            or self.upper.find('CZ') > -1
            or self.upper.find('WITZ') > -1)

    def get_letters(self, start=0, end=None):
        if not end:
            end = start + 1
        start = self.start_index + start
        end = self.start_index + end
        return self.buffer[start:end]


def doublemetaphone(input):
    """
    dm(string) -> (string, string or '') returns the double metaphone codes
    for given string - always a tuple there are no checks done on the input
    string, but it should be a single word or name.
    """
    word = Word(input)
    input = word.buffer
    first = word.start_index
    last = word.last

    # pos is short for position
    pos = word.start_index
    # primary and secondary metaphone codes
    pri = sec = ''
    # skip these silent letters when at start of word
    if word.get_letters(0, 2) in SILENT_STARTERS:
        pos += 1
    # Initial 'X' is pronounced 'Z' e.g. 'Xavier'
    if word.get_letters(0) == 'X':
        # 'Z' maps to 'S'
        pri = sec = 'S'
        pos += 1
    # main loop through chars in input
    while pos <= word.last:
        # ch is short for character
        ch = input[pos]
        # nxt (short for next characters in metaphone code) is set to  a tuple
        # of the next characters in the primary and secondary codes and how
        # many characters to move forward in the string.  the secondary code
        # letter is given only when it is different than the primary.  This is
        # just a trick to make the code easier to write and read.

        # default action is to add nothing and move to next char
        nxt = (None, 1)
        if ch in VOWELS:
            nxt = (None, 1)
            # all init vowels now map to 'A'
            if pos == word.start_index: 
                nxt = ('A', 1)
        elif ch == 'B':
            # "-mb", e.g., "dumb", already skipped over... see 'M' below
            if input[pos + 1] == 'B':
                nxt = ('P', 2)
            else:
                nxt = ('P', 1)
        elif ch == 'C':
            # various germanic
            if (pos > first + 1
                and input[pos - 2] not in VOWELS
                and input[pos - 1:pos + 2] == 'ACH'
                and input[pos + 2] not in ['I']
                and (input[pos + 2] not in ['E']
                     or input[pos - 2:pos + 4] in ['BACHER', 'MACHER'])):
                nxt = ('K', 2)
            # special case 'CAESAR'
            elif pos == first and input[first:first + 6] == 'CAESAR':
                nxt = ('S', 2)
            elif input[pos:pos + 4] == 'CHIA':  # italian 'chianti'
                nxt = ('K', 2)
            elif input[pos:pos + 2] == 'CH':
                # find 'michael'
                if pos > first and input[pos:pos + 4] == 'CHAE':
                    nxt = ('K', 'X', 2)
                elif (pos == first
                      and (input[pos + 1:pos + 6] in ['HARAC', 'HARIS']
                      or input[pos + 1:pos + 4] in ["HOR", "HYM", "HIA",
                                                    "HEM"])
                      and input[first:first + 5] != 'CHORE'):
                    nxt = ('K', 2)
                # germanic, greek, or otherwise 'ch' for 'kh' sound
                elif (
                    input[first:first + 4] in ['VAN ', 'VON ']
                    or input[first:first + 3] == 'SCH'
                    or input[pos - 2:pos + 4] in ["ORCHES", "ARCHIT", "ORCHID"]
                    or input[pos + 2] in ['T', 'S']
                    or (
                        (input[pos - 1] in ["A", "O", "U", "E"]
                         or pos == first)
                        and (input[pos + 2] in [
                            "L", "R", "N", "M", "B", "H", "F", "V", "W"]))):
                    nxt = ('K', 2)
                else:
                    if pos > first:
                        if input[first:first + 2] == 'MC':
                            nxt = ('K', 2)
                        else:
                            nxt = ('X', 'K', 2)
                    else:
                        nxt = ('X', 2)
            # e.g, 'czerny'
            elif (input[pos:pos + 2] == 'CZ'
                  and input[pos - 2:pos + 2] != 'WICZ'):
                nxt = ('S', 'X', 2)
            # e.g., 'focaccia'
            elif input[pos + 1:pos + 4] == 'CIA':
                nxt = ('X', 3)
            # double 'C', but not if e.g. 'McClellan'
            elif (
                input[pos:pos + 2] == 'CC'
                and not (pos == (first + 1) and input[first] == 'M')):
                #'bellocchio' but not 'bacchus'
                if (input[pos + 2] in ["I", "E", "H"]
                    and input[pos + 2:pos + 4] != 'HU'):
                    # 'accident', 'accede' 'succeed'
                    if (
                        (pos == (first + 1) and input[first] == 'A')
                        or input[pos - 1:pos + 4] in ['UCCEE', 'UCCES']):
                        nxt = ('KS', 3)
                    # 'bacci', 'bertucci', other italian
                    else:
                        nxt = ('X', 3)
                else:
                    nxt = ('K', 2)
            elif input[pos:pos + 2] in ["CK", "CG", "CQ"]:
                nxt = ('K', 2)
            elif input[pos:pos + 2] in ["CI", "CE", "CY"]:
                # italian vs. english
                if input[pos:pos + 3] in ["CIO", "CIE", "CIA"]:
                    nxt = ('S', 'X', 2)
                else:
                    nxt = ('S', 2)
            else:
                # name sent in 'mac caffrey', 'mac gregor'
                if input[pos + 1:pos + 3] in [" C", " Q", " G"]:
                    nxt = ('K', 3)
                else:
                    if (input[pos + 1] in ["C", "K", "Q"]
                        and input[pos + 1:pos + 3] not in ["CE", "CI"]):
                        nxt = ('K', 2)
                    else:  # default for 'C'
                        nxt = ('K', 1)
        # will never get here with st.encode('ascii', 'replace') above \xc7 is
        # UTF-8 encoding of Ç
        elif ch == u'\xc7':
            nxt = ('S', 1)
        elif ch == 'D':
            if input[pos:pos + 2] == 'DG':
                if input[pos + 2] in ['I', 'E', 'Y']:  # e.g. 'edge'
                    nxt = ('J', 3)
                else:
                    nxt = ('TK', 2)
            elif input[pos:pos + 2] in ['DT', 'DD']:
                nxt = ('T', 2)
            else:
                nxt = ('T', 1)
        elif ch == 'F':
            if input[pos + 1] == 'F':
                nxt = ('F', 2)
            else:
                nxt = ('F', 1)
        elif ch == 'G':
            if input[pos + 1] == 'H':
                if pos > first and input[pos - 1] not in VOWELS:
                    nxt = ('K', 2)
                elif pos < (first + 3):
                    if pos == first:  # 'ghislane', ghiradelli
                        if input[pos + 2] == 'I':
                            nxt = ('J', 2)
                        else:
                            nxt = ('K', 2)
                # Parker's rule (with some further refinements) - e.g., 'hugh'
                elif ((pos > (first + 1) and input[pos - 2] in ['B', 'H', 'D'])
                      or (pos > (first + 2) and input[pos - 3] in ['B', 'H', 'D'])
                      or (pos > (first + 3) and input[pos - 3] in ['B', 'H'])):
                    nxt = (None, 2)
                else:
                    # e.g., 'laugh', 'McLaughlin', 'cough', 'gough', 'rough',
                    # 'tough'
                    if (pos > (first + 2)
                        and input[pos - 1] == 'U'
                        and input[pos - 3] in ["C", "G", "L", "R", "T"]):
                        nxt = ('F', 2)
                    else:
                        if pos > first and input[pos - 1] != 'I':
                            nxt = ('K', 2)
            elif input[pos + 1] == 'N':
                if pos == ((first + 1)
                           and input[first] in VOWELS
                           and not word.is_slavo_germanic):
                    nxt = ('KN', 'N', 2)
                else:
                    # not e.g. 'cagney'
                    if (input[pos + 2:pos + 4] != 'EY'
                        and input[pos + 1] != 'Y'
                        and not word.is_slavo_germanic):
                        nxt = ('N', 'KN', 2)
                    else:
                        nxt = ('KN', 2)
            # 'tagliaro'
            elif input[pos + 1:pos + 3] == 'LI' and not word.is_slavo_germanic:
                nxt = ('KL', 'L', 2)
            # -ges-,-gep-,-gel-, -gie- at beginning
            elif (pos == first
                  and (input[pos + 1] == 'Y'
                  or input[pos + 1:pos + 3] in ["ES", "EP", "EB", "EL", "EY",
                                             "IB", "IL", "IN", "IE", "EI",
                                             "ER"])):
                nxt = ('K', 'J', 2)
            # -ger-,  -gy-
            elif (
                (input[pos + 1:pos + 3] == 'ER' or input[pos + 1] == 'Y')
                and input[first:first + 6] not in ["DANGER", "RANGER", "MANGER"]
                and input[pos - 1] not in ['E', 'I']
                and input[pos - 1:pos + 2] not in ['RGY', 'OGY']):
                nxt = ('K', 'J', 2)
            # italian e.g, 'biaggi'
            elif (
                input[pos + 1] in ['E', 'I', 'Y']
                or input[pos - 1:pos + 3] in ["AGGI", "OGGI"]):
                # obvious germanic
                if (input[first:first + 4] in ['VON ', 'VAN ']
                    or input[first:first + 3] == 'SCH'
                    or input[pos + 1:pos + 3] == 'ET'):
                    nxt = ('K', 2)
                else:
                    # always soft if french ending
                    if input[pos + 1:pos + 5] == 'IER ':
                        nxt = ('J', 2)
                    else:
                        nxt = ('J', 'K', 2)
            elif input[pos + 1] == 'G':
                nxt = ('K', 2)
            else:
                nxt = ('K', 1)
        elif ch == 'H':
            # only keep if first & before vowel or btw. 2 vowels
            if (
                (pos == first or input[pos - 1] in VOWELS)
                and input[pos + 1] in VOWELS):
                nxt = ('H', 2)
            # (also takes care of 'HH')
            else:
                nxt = (None, 1)
        elif ch == 'J':
            # obvious spanish, 'jose', 'san jacinto'
            if (
                input[pos:pos + 4] == 'JOSE'
                or input[first:first + 4] == 'SAN '):
                if (
                    (pos == first and input[pos + 4] == ' ')
                    or input[first:first + 4] == 'SAN '):
                    nxt = ('H', )
                else:
                    nxt = ('J', 'H')
            # Yankelovich/Jankelowicz
            elif pos == first and input[pos:pos + 4] != 'JOSE':
                nxt = ('J', 'A')
            else:
                # spanish pron. of e.g. 'bajador'
                if (input[pos - 1] in VOWELS
                    and not word.is_slavo_germanic
                    and input[pos + 1] in ['A', 'O']):
                    nxt = ('J', 'H')
                else:
                    if pos == last:
                        nxt = ('J', ' ')
                    else:
                        if (input[pos + 1] not in ["L", "T", "K", "S", "N",
                                                   "M", "B", "Z"]
                            and input[pos - 1] not in ["S", "K", "L"]):
                            nxt = ('J', )
                        else:
                            nxt = (None, )
            if input[pos + 1] == 'J':
                nxt = nxt + (2, )
            else:
                nxt = nxt + (1, )
        elif ch == 'K':
            if input[pos + 1] == 'K':
                nxt = ('K', 2)
            else:
                nxt = ('K', 1)
        elif ch == 'L':
            if input[pos + 1] == 'L':
                # spanish e.g. 'cabrillo', 'gallegos'
                if ((pos == (last - 2)
                     and input[pos - 1:pos + 3] in ["ILLO", "ILLA", "ALLE"])
                    or ((input[last - 1:last + 1] in ["AS", "OS"]
                         or input[last] in ["A", "O"])
                        and input[pos - 1:pos + 3] == 'ALLE')):
                    nxt = ('L', '', 2)
                else:
                    nxt = ('L', 2)
            else:
                nxt = ('L', 1)
        elif ch == 'M':
            if (
                (input[pos + 1:pos + 4] == 'UMB'
                 and (pos + 1 == last or input[pos + 2:pos + 4] == 'ER'))
                or input[pos + 1] == 'M'):
                nxt = ('M', 2)
            else:
                nxt = ('M', 1)
        elif ch == 'N':
            if input[pos + 1] == 'N':
                nxt = ('N', 2)
            else:
                nxt = ('N', 1)
        # UTF-8 encoding of ﾄ
        elif ch == u'\xd1':
            nxt = ('N', 1)
        elif ch == 'P':
            if input[pos + 1] == 'H':
                nxt = ('F', 2)
            # also account for "campbell", "raspberry"
            elif input[pos + 1] in ['P', 'B']:
                nxt = ('P', 2)
            else:
                nxt = ('P', 1)
        elif ch == 'Q':
            if input[pos + 1] == 'Q':
                nxt = ('K', 2)
            else:
                nxt = ('K', 1)
        elif ch == 'R':
            # french e.g. 'rogier', but exclude 'hochmeier'
            if (pos == last
                and not word.is_slavo_germanic
                and input[pos - 2:pos] == 'IE'
                and input[pos - 4:pos - 2] not in ['ME', 'MA']):
                nxt = ('', 'R')
            else:
                nxt = ('R',)
            if input[pos + 1] == 'R':
                nxt = nxt + (2,)
            else:
                nxt = nxt + (1,)
        elif ch == 'S':
            # special cases 'island', 'isle', 'carlisle', 'carlysle'
            if input[pos - 1:pos + 2] in ['ISL', 'YSL']:
                nxt = (None, 1)
            # special case 'sugar-'
            elif pos == first and input[first:first + 5] == 'SUGAR':
                nxt = ('X', 'S', 1)
            elif input[pos:pos + 2] == 'SH':
                # germanic
                if input[pos + 1:pos + 5] in ["HEIM", "HOEK", "HOLM", "HOLZ"]:
                    nxt = ('S', 2)
                else:
                    nxt = ('X', 2)
            # italian & armenian
            elif (input[pos:pos + 3] in ["SIO", "SIA"]
                  or input[pos:pos + 4] == 'SIAN'):
                if not word.is_slavo_germanic:
                    nxt = ('S', 'X', 3)
                else:
                    nxt = ('S', 3)
            # german & anglicisations, e.g. 'smith' match 'schmidt', 'snider'
            # match 'schneider' also, -sz- in slavic language altho in
            # hungarian it is pronounced 's'
            elif (
                (pos == first and input[pos + 1] in ["M", "N", "L", "W"])
                or input[pos + 1] == 'Z'):
                nxt = ('S', 'X')
                if input[pos + 1] == 'Z':
                    nxt = nxt + (2, )
                else:
                    nxt = nxt + (1, )
            elif input[pos:pos + 2] == 'SC':
                # Schlesinger's rule
                if input[pos + 2] == 'H':
                    # dutch origin, e.g. 'school', 'schooner'
                    if input[pos + 3:pos + 5] in ["OO", "ER", "EN", "UY", "ED",
                                                  "EM"]:
                        # 'schermerhorn', 'schenker'
                        if input[pos + 3:pos + 5] in ['ER', 'EN']:
                            nxt = ('X', 'SK', 3)
                        else:
                            nxt = ('SK', 3)
                    else:
                        if (pos == first
                            and input[first + 3] not in VOWELS
                            and input[first + 3] != 'W'):
                            nxt = ('X', 'S', 3)
                        else:
                            nxt = ('X', 3)
                elif input[pos + 2] in ['I', 'E', 'Y']:
                    nxt = ('S', 3)
                else:
                    nxt = ('SK', 3)
            # french e.g. 'resnais', 'artois'
            elif pos == last and input[pos - 2:pos] in ['AI', 'OI']:
                nxt = ('', 'S', 1)
            else:
                nxt = ('S', )
                if input[pos + 1] in ['S', 'Z']:
                    nxt = nxt + (2, )
                else:
                    nxt = nxt + (1, )
        elif ch == 'T':
            if input[pos:pos + 4] == 'TION':
                nxt = ('X', 3)
            elif input[pos:pos + 3] in ['TIA', 'TCH']:
                nxt = ('X', 3)
            elif input[pos:pos + 2] == 'TH' or input[pos:pos + 3] == 'TTH':
                # special case 'thomas', 'thames' or germanic
                if (input[pos + 2:pos + 4] in ['OM', 'AM']
                    or input[first:first + 4] in ['VON ', 'VAN ']
                    or input[first:first + 3] == 'SCH'):
                    nxt = ('T', 2)
                else:
                    nxt = ('0', 'T', 2)
            elif input[pos + 1] in ['T', 'D']:
                nxt = ('T', 2)
            else:
                nxt = ('T', 1)
        elif ch == 'V':
            if input[pos + 1] == 'V':
                nxt = ('F', 2)
            else:
                nxt = ('F', 1)
        elif ch == 'W':
            # can also be in middle of word
            if input[pos:pos + 2] == 'WR':
                nxt = ('R', 2)
            elif (
                pos == first
                and (input[pos + 1] in VOWELS or input[pos:pos + 2] == 'WH')):
                # Wasserman should match Vasserman
                if input[pos + 1] in VOWELS:
                    nxt = ('A', 'F', 1)
                else:
                    nxt = ('A', 1)
            # Arnow should match Arnoff
            elif ((pos == last and input[pos - 1] in VOWELS)
                   or input[pos - 1:pos + 4] in ["EWSKI", "EWSKY", "OWSKI",
                                                 "OWSKY"]
                   or input[first:first + 3] == 'SCH'):
                nxt = ('', 'F', 1)
            # polish e.g. 'filipowicz'
            elif input[pos:pos + 4] in ["WICZ", "WITZ"]:
                nxt = ('TS', 'FX', 4)
            else:  # default is to skip it
                nxt = (None, 1)
        elif ch == 'X':
            # french e.g. breaux
            nxt = (None, )
            if not(pos == last and (input[pos - 3:pos] in ["IAU", "EAU"]
               or input[pos - 2:pos] in ['AU', 'OU'])):
                nxt = ('KS', )
            if input[pos + 1] in ['C', 'X']:
                nxt = nxt + (2, )
            else:
                nxt = nxt + (1, )
        elif ch == 'Z':
            # chinese pinyin e.g. 'zhao'
            if input[pos + 1] == 'H':
                nxt = ('J', )
            elif (
                input[pos + 1:pos + 3] in ["ZO", "ZI", "ZA"]
                or (word.is_slavo_germanic
                    and pos > first
                    and input[pos - 1] != 'T')):
                nxt = ('S', 'TS')
            else:
                nxt = ('S', )
            if input[pos + 1] == 'Z' or input[pos + 1] == 'H':
                nxt = nxt + (2, )
            else:
                nxt = nxt + (1, )
        if len(nxt) == 2:
            if nxt[0]:
                pri += nxt[0]
                sec += nxt[0]
            pos += nxt[1]
        elif len(nxt) == 3:
            if nxt[0]:
                pri += nxt[0]
            if nxt[1]:
                sec += nxt[1]
            pos += nxt[2]
    if pri == sec:
        return (pri, '')
    else:
        return (pri, sec)


# for backwards compatibility
dm = doublemetaphone
