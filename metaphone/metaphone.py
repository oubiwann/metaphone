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
        self.end_index = self.start_index + self.length - 1
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

class DoubleMetaphone(object):
    """
    """
    def __init__(self):
        self.position = 0
        self.primary_phone = ""
        self.secondary_phone = ""
        # next is set to a tuple of the next characters in the primary and
        # secondary codes and how many characters to move forward in the
        # string.  The secondary code letter is given only when it is different
        # than the primary. This is just a trick to make the code easier to
        # write and read. The default action is to add nothing and move to next
        # char.
        self.next = (None, 1)

    def check_word_start(self):
        # skip these silent letters when at start of word
        if self.word.get_letters(0, 2) in SILENT_STARTERS:
            self.position += 1
        # Initial 'X' is pronounced 'Z' e.g. 'Xavier'
        if self.word.get_letters(0) == 'X':
            # 'Z' maps to 'S'
            self.primary_phone = self.secondary_phone = 'S'
            self.position += 1

    def check_vowels(self):
        # XXX do we need this next set? it should already be done...
        self.next = (None, 1)
        # all init vowels now map to 'A'
        if self.position == self.word.start_index:
            self.next = ('A', 1)

    def parse(self, input):
        self.word = Word(input)
        self.position = self.word.start_index
        self.check_word_start()

        # main loop through chars in word.buffer
        while self.position <= self.word.end_index:
            character = self.word.buffer[self.position]
            if character in VOWELS:
                self.check_vowels()

        if self.primary_phone == self.secondary_phone:
            self.secondary_phone = ""
        return (self.primary_phone, self.secondary_phone)


def doublemetaphone(input):
    return DoubleMetaphone().parse(input)


def XXX_doublemetaphone(input):
    """
    dm(string) -> (string, string or '') returns the double metaphone codes
    for given string - always a tuple there are no checks done on the input
    string, but it should be a single word or name.
    """


        elif character == 'B':
            # "-mb", e.g., "dumb", already skipped over... see 'M' below
            if word.buffer[pos + 1] == 'B':
                next = ('P', 2)
            else: next = ('P', 1)
        elif character == 'C':
            # various germanic
            if (pos > word.start_index + 1
                and word.buffer[pos - 2] not in VOWELS
                and word.buffer[pos - 1:pos + 2] == 'ACH'
                and word.buffer[pos + 2] not in ['I']
                and (word.buffer[pos + 2] not in ['E']
                     or word.buffer[pos - 2:pos + 4] in ['BACHER', 'MACHER'])):
                next = ('K', 2)
            # special case 'CAESAR'
            elif pos == word.start_index and word.buffer[word.start_index:word.start_index + 6] == 'CAESAR':
                next = ('S', 2)
            # italian 'chianti'
            elif word.buffer[pos:pos + 4] == 'CHIA':
                next = ('K', 2)
            elif word.buffer[pos:pos + 2] == 'CH':
                # find 'michael'
                if pos > word.start_index and word.buffer[pos:pos + 4] == 'CHAE':
                    next = ('K', 'X', 2)
                elif (pos == word.start_index
                      and (word.buffer[pos + 1:pos + 6] in ['HARAC', 'HARIS']
                      or word.buffer[pos + 1:pos + 4] in ["HOR", "HYM", "HIA",
                                                    "HEM"])
                      and word.buffer[word.start_index:word.start_index + 5] != 'CHORE'):
                    next = ('K', 2)
                # germanic, greek, or otherwise 'ch' for 'kh' sound
                elif (
                    word.buffer[word.start_index:word.start_index + 4] in ['VAN ', 'VON ']
                    or word.buffer[word.start_index:word.start_index + 3] == 'SCH'
                    or word.buffer[pos - 2:pos + 4] in ["ORCHES", "ARCHIT", "ORCHID"]
                    or word.buffer[pos + 2] in ['T', 'S']
                    or (
                        (word.buffer[pos - 1] in ["A", "O", "U", "E"]
                         or pos == word.start_index)
                        and (word.buffer[pos + 2] in [
                            "L", "R", "N", "M", "B", "H", "F", "V", "W"]))):
                    next = ('K', 2)
                else:
                    if pos > word.start_index:
                        if word.buffer[word.start_index:word.start_index + 2] == 'MC':
                            next = ('K', 2)
                        else:
                            next = ('X', 'K', 2)
                    else:
                        next = ('X', 2)
            # e.g, 'czerny'
            elif (word.buffer[pos:pos + 2] == 'CZ'
                  and word.buffer[pos - 2:pos + 2] != 'WICZ'):
                next = ('S', 'X', 2)
            # e.g., 'focaccia'
            elif word.buffer[pos + 1:pos + 4] == 'CIA':
                next = ('X', 3)
            # double 'C', but not if e.g. 'McClellan'
            elif (
                word.buffer[pos:pos + 2] == 'CC'
                and not (pos == (word.start_index + 1) and word.buffer[word.start_index] == 'M')):
                #'bellocchio' but not 'bacchus'
                if (word.buffer[pos + 2] in ["I", "E", "H"]
                    and word.buffer[pos + 2:pos + 4] != 'HU'):
                    # 'accident', 'accede' 'succeed'
                    if (
                        (pos == (word.start_index + 1) and word.buffer[word.start_index] == 'A')
                        or word.buffer[pos - 1:pos + 4] in ['UCCEE', 'UCCES']):
                        next = ('KS', 3)
                    # 'bacci', 'bertucci', other italian
                    else:
                        next = ('X', 3)
                else:
                    next = ('K', 2)
            elif word.buffer[pos:pos + 2] in ["CK", "CG", "CQ"]:
                next = ('K', 2)
            elif word.buffer[pos:pos + 2] in ["CI", "CE", "CY"]:
                # italian vs. english
                if word.buffer[pos:pos + 3] in ["CIO", "CIE", "CIA"]:
                    next = ('S', 'X', 2)
                else:
                    next = ('S', 2)
            else:
                # name sent in 'mac caffrey', 'mac gregor'
                if word.buffer[pos + 1:pos + 3] in [" C", " Q", " G"]:
                    next = ('K', 3)
                else:
                    if (word.buffer[pos + 1] in ["C", "K", "Q"]
                        and word.buffer[pos + 1:pos + 3] not in ["CE", "CI"]):
                        next = ('K', 2)
                    else:  # default for 'C'
                        next = ('K', 1)
        # will never get here with st.encode('ascii', 'replace') above \xc7 is
        # UTF-8 encoding of Ç
        elif character == u'\xc7':
            next = ('S', 1)
        elif character == 'D':
            if word.buffer[pos:pos + 2] == 'DG':
                if word.buffer[pos + 2] in ['I', 'E', 'Y']:  # e.g. 'edge'
                    next = ('J', 3)
                else:
                    next = ('TK', 2)
            elif word.buffer[pos:pos + 2] in ['DT', 'DD']:
                next = ('T', 2)
            else:
                next = ('T', 1)
        elif character == 'F':
            if word.buffer[pos + 1] == 'F':
                next = ('F', 2)
            else:
                next = ('F', 1)
        elif character == 'G':
            if word.buffer[pos + 1] == 'H':
                if pos > word.start_index and word.buffer[pos - 1] not in VOWELS:
                    next = ('K', 2)
                elif pos < (word.start_index + 3):
                    if pos == word.start_index:  # 'ghislane', ghiradelli
                        if word.buffer[pos + 2] == 'I':
                            next = ('J', 2)
                        else:
                            next = ('K', 2)
                # Parker's rule (with some further refinements) - e.g., 'hugh'
                elif ((pos > (word.start_index + 1) and word.buffer[pos - 2] in ['B', 'H', 'D'])
                      or (pos > (word.start_index + 2) and word.buffer[pos - 3] in ['B', 'H', 'D'])
                      or (pos > (word.start_index + 3) and word.buffer[pos - 3] in ['B', 'H'])):
                    next = (None, 2)
                else:
                    # e.g., 'laugh', 'McLaughlin', 'cough', 'gough', 'rough',
                    # 'tough'
                    if (pos > (word.start_index + 2)
                        and word.buffer[pos - 1] == 'U'
                        and word.buffer[pos - 3] in ["C", "G", "L", "R", "T"]):
                        next = ('F', 2)
                    else:
                        if pos > word.start_index and word.buffer[pos - 1] != 'I':
                            next = ('K', 2)
            elif word.buffer[pos + 1] == 'N':
                if pos == ((word.start_index + 1)
                           and word.buffer[word.start_index] in VOWELS
                           and not word.is_slavo_germanic):
                    next = ('KN', 'N', 2)
                else:
                    # not e.g. 'cagney'
                    if (word.buffer[pos + 2:pos + 4] != 'EY'
                        and word.buffer[pos + 1] != 'Y'
                        and not word.is_slavo_germanic):
                        next = ('N', 'KN', 2)
                    else:
                        next = ('KN', 2)
            # 'tagliaro'
            elif word.buffer[pos + 1:pos + 3] == 'LI' and not word.is_slavo_germanic:
                next = ('KL', 'L', 2)
            # -ges-,-gep-,-gel-, -gie- at beginning
            elif (pos == word.start_index
                  and (word.buffer[pos + 1] == 'Y'
                  or word.buffer[pos + 1:pos + 3] in ["ES", "EP", "EB", "EL", "EY",
                                             "IB", "IL", "IN", "IE", "EI",
                                             "ER"])):
                next = ('K', 'J', 2)
            # -ger-,  -gy-
            elif (
                (word.buffer[pos + 1:pos + 3] == 'ER' or word.buffer[pos + 1] == 'Y')
                and word.buffer[word.start_index:word.start_index + 6] not in ["DANGER", "RANGER", "MANGER"]
                and word.buffer[pos - 1] not in ['E', 'I']
                and word.buffer[pos - 1:pos + 2] not in ['RGY', 'OGY']):
                next = ('K', 'J', 2)
            # italian e.g, 'biaggi'
            elif (
                word.buffer[pos + 1] in ['E', 'I', 'Y']
                or word.buffer[pos - 1:pos + 3] in ["AGGI", "OGGI"]):
                # obvious germanic
                if (word.buffer[word.start_index:word.start_index + 4] in ['VON ', 'VAN ']
                    or word.buffer[word.start_index:word.start_index + 3] == 'SCH'
                    or word.buffer[pos + 1:pos + 3] == 'ET'):
                    next = ('K', 2)
                else:
                    # always soft if french ending
                    if word.buffer[pos + 1:pos + 5] == 'IER ':
                        next = ('J', 2)
                    else:
                        next = ('J', 'K', 2)
            elif word.buffer[pos + 1] == 'G':
                next = ('K', 2)
            else:
                next = ('K', 1)
        elif character == 'H':
            # only keep if word.start_index & before vowel or btw. 2 vowels
            if (
                (pos == word.start_index or word.buffer[pos - 1] in VOWELS)
                and word.buffer[pos + 1] in VOWELS):
                next = ('H', 2)
            # (also takes care of 'HH')
            else:
                next = (None, 1)
        elif character == 'J':
            # obvious spanish, 'jose', 'san jacinto'
            if (
                word.buffer[pos:pos + 4] == 'JOSE'
                or word.buffer[word.start_index:word.start_index + 4] == 'SAN '):
                if (
                    (pos == word.start_index and word.buffer[pos + 4] == ' ')
                    or word.buffer[word.start_index:word.start_index + 4] == 'SAN '):
                    next = ('H', )
                else:
                    next = ('J', 'H')
            # Yankelovich/Jankelowicz
            elif pos == word.start_index and word.buffer[pos:pos + 4] != 'JOSE':
                next = ('J', 'A')
            else:
                # spanish pron. of e.g. 'bajador'
                if (word.buffer[pos - 1] in VOWELS
                    and not word.is_slavo_germanic
                    and word.buffer[pos + 1] in ['A', 'O']):
                    next = ('J', 'H')
                else:
                    if pos == word.end_index:
                        next = ('J', ' ')
                    else:
                        if (word.buffer[pos + 1] not in ["L", "T", "K", "S", "N",
                                                   "M", "B", "Z"]
                            and word.buffer[pos - 1] not in ["S", "K", "L"]):
                            next = ('J', )
                        else:
                            next = (None, )
            if word.buffer[pos + 1] == 'J':
                next = next + (2, )
            else:
                next = next + (1, )
        elif character == 'K':
            if word.buffer[pos + 1] == 'K':
                next = ('K', 2)
            else:
                next = ('K', 1)
        elif character == 'L':
            if word.buffer[pos + 1] == 'L':
                # spanish e.g. 'cabrillo', 'gallegos'
                if ((pos == (word.end_index - 2)
                     and word.buffer[pos - 1:pos + 3] in ["ILLO", "ILLA", "ALLE"])
                    or ((word.buffer[word.end_index - 1:word.end_index + 1] in ["AS", "OS"]
                         or word.buffer[word.end_index] in ["A", "O"])
                        and word.buffer[pos - 1:pos + 3] == 'ALLE')):
                    next = ('L', '', 2)
                else:
                    next = ('L', 2)
            else:
                next = ('L', 1)
        elif character == 'M':
            if (
                (word.buffer[pos + 1:pos + 4] == 'UMB'
                 and (pos + 1 == word.end_index or word.buffer[pos + 2:pos + 4] == 'ER'))
                or word.buffer[pos + 1] == 'M'):
                next = ('M', 2)
            else:
                next = ('M', 1)
        elif character == 'N':
            if word.buffer[pos + 1] == 'N':
                next = ('N', 2)
            else:
                next = ('N', 1)
        # UTF-8 encoding of ﾄ
        elif character == u'\xd1':
            next = ('N', 1)
        elif character == 'P':
            if word.buffer[pos + 1] == 'H':
                next = ('F', 2)
            # also account for "campbell", "raspberry"
            elif word.buffer[pos + 1] in ['P', 'B']:
                next = ('P', 2)
            else:
                next = ('P', 1)
        elif character == 'Q':
            if word.buffer[pos + 1] == 'Q':
                next = ('K', 2)
            else:
                next = ('K', 1)
        elif character == 'R':
            # french e.g. 'rogier', but exclude 'hochmeier'
            if (pos == word.end_index
                and not word.is_slavo_germanic
                and word.buffer[pos - 2:pos] == 'IE'
                and word.buffer[pos - 4:pos - 2] not in ['ME', 'MA']):
                next = ('', 'R')
            else:
                next = ('R',)
            if word.buffer[pos + 1] == 'R':
                next = next + (2,)
            else:
                next = next + (1,)
        elif character == 'S':
            # special cases 'island', 'isle', 'carlisle', 'carlysle'
            if word.buffer[pos - 1:pos + 2] in ['ISL', 'YSL']:
                next = (None, 1)
            # special case 'sugar-'
            elif pos == word.start_index and word.buffer[word.start_index:word.start_index + 5] == 'SUGAR':
                next = ('X', 'S', 1)
            elif word.buffer[pos:pos + 2] == 'SH':
                # germanic
                if word.buffer[pos + 1:pos + 5] in ["HEIM", "HOEK", "HOLM", "HOLZ"]:
                    next = ('S', 2)
                else:
                    next = ('X', 2)
            # italian & armenian
            elif (word.buffer[pos:pos + 3] in ["SIO", "SIA"]
                  or word.buffer[pos:pos + 4] == 'SIAN'):
                if not word.is_slavo_germanic:
                    next = ('S', 'X', 3)
                else:
                    next = ('S', 3)
            # german & anglicisations, e.g. 'smith' match 'schmidt', 'snider'
            # match 'schneider' also, -sz- in slavic language altho in
            # hungarian it is pronounced 's'
            elif (
                (pos == word.start_index and word.buffer[pos + 1] in ["M", "N", "L", "W"])
                or word.buffer[pos + 1] == 'Z'):
                next = ('S', 'X')
                if word.buffer[pos + 1] == 'Z':
                    next = next + (2, )
                else:
                    next = next + (1, )
            elif word.buffer[pos:pos + 2] == 'SC':
                # Schlesinger's rule
                if word.buffer[pos + 2] == 'H':
                    # dutch origin, e.g. 'school', 'schooner'
                    if word.buffer[pos + 3:pos + 5] in ["OO", "ER", "EN", "UY", "ED",
                                                  "EM"]:
                        # 'schermerhorn', 'schenker'
                        if word.buffer[pos + 3:pos + 5] in ['ER', 'EN']:
                            next = ('X', 'SK', 3)
                        else:
                            next = ('SK', 3)
                    else:
                        if (pos == word.start_index
                            and word.buffer[word.start_index + 3] not in VOWELS
                            and word.buffer[word.start_index + 3] != 'W'):
                            next = ('X', 'S', 3)
                        else:
                            next = ('X', 3)
                elif word.buffer[pos + 2] in ['I', 'E', 'Y']:
                    next = ('S', 3)
                else:
                    next = ('SK', 3)
            # french e.g. 'resnais', 'artois'
            elif pos == word.end_index and word.buffer[pos - 2:pos] in ['AI', 'OI']:
                next = ('', 'S', 1)
            else:
                next = ('S', )
                if word.buffer[pos + 1] in ['S', 'Z']:
                    next = next + (2, )
                else:
                    next = next + (1, )
        elif character == 'T':
            if word.buffer[pos:pos + 4] == 'TION':
                next = ('X', 3)
            elif word.buffer[pos:pos + 3] in ['TIA', 'TCH']:
                next = ('X', 3)
            elif word.buffer[pos:pos + 2] == 'TH' or word.buffer[pos:pos + 3] == 'TTH':
                # special case 'thomas', 'thames' or germanic
                if (word.buffer[pos + 2:pos + 4] in ['OM', 'AM']
                    or word.buffer[word.start_index:word.start_index + 4] in ['VON ', 'VAN ']
                    or word.buffer[word.start_index:word.start_index + 3] == 'SCH'):
                    next = ('T', 2)
                else:
                    next = ('0', 'T', 2)
            elif word.buffer[pos + 1] in ['T', 'D']:
                next = ('T', 2)
            else:
                next = ('T', 1)
        elif character == 'V':
            if word.buffer[pos + 1] == 'V':
                next = ('F', 2)
            else:
                next = ('F', 1)
        elif character == 'W':
            # can also be in middle of word
            if word.buffer[pos:pos + 2] == 'WR':
                next = ('R', 2)
            elif (
                pos == word.start_index
                and (word.buffer[pos + 1] in VOWELS or word.buffer[pos:pos + 2] == 'WH')):
                # Wasserman should match Vasserman
                if word.buffer[pos + 1] in VOWELS:
                    next = ('A', 'F', 1)
                else:
                    next = ('A', 1)
            # Arnow should match Arnoff
            elif ((pos == word.end_index and word.buffer[pos - 1] in VOWELS)
                   or word.buffer[pos - 1:pos + 4] in ["EWSKI", "EWSKY", "OWSKI",
                                                 "OWSKY"]
                   or word.buffer[word.start_index:word.start_index + 3] == 'SCH'):
                next = ('', 'F', 1)
            # polish e.g. 'filipowicz'
            elif word.buffer[pos:pos + 4] in ["WICZ", "WITZ"]:
                next = ('TS', 'FX', 4)
            else:  # default is to skip it
                next = (None, 1)
        elif character == 'X':
            # french e.g. breaux
            next = (None, )
            if not(pos == word.end_index and (word.buffer[pos - 3:pos] in ["IAU", "EAU"]
               or word.buffer[pos - 2:pos] in ['AU', 'OU'])):
                next = ('KS', )
            if word.buffer[pos + 1] in ['C', 'X']:
                next = next + (2, )
            else:
                next = next + (1, )
        elif character == 'Z':
            # chinese pinyin e.g. 'zhao'
            if word.buffer[pos + 1] == 'H':
                next = ('J', )
            elif (
                word.buffer[pos + 1:pos + 3] in ["ZO", "ZI", "ZA"]
                or (word.is_slavo_germanic
                    and pos > word.start_index
                    and word.buffer[pos - 1] != 'T')):
                next = ('S', 'TS')
            else:
                next = ('S', )
            if word.buffer[pos + 1] == 'Z' or word.buffer[pos + 1] == 'H':
                next = next + (2, )
            else:
                next = next + (1, )
        if len(next) == 2:
            if next[0]:
                pri += next[0]
                sec += next[0]
            pos += next[1]
        elif len(next) == 3:
            if next[0]:
                pri += next[0]
            if next[1]:
                sec += next[1]
            pos += next[2]
    if pri == sec:
        return (pri, '')
    else:
        return (pri, sec)


# for backwards compatibility
dm = doublemetaphone
