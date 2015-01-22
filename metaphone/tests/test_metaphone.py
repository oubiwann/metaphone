# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from metaphone.metaphone import doublemetaphone


class MetaphoneTestCase(unittest.TestCase):
    """
    """
    def test_single_result(self):
        result = doublemetaphone(u"aubrey")
        self.assertEquals(result, ('APR', ''))

    def test_double_result(self):
        result = doublemetaphone(u"richard")
        self.assertEquals(result, ('RXRT', 'RKRT'))

    def test_general_word_list(self):
        result = doublemetaphone('Jose')
        self.assertEquals(result, ('JS', 'HS'))
        result = doublemetaphone('cambrillo')
        self.assertEquals(result, ('KMPRL', 'KMPR'))
        result = doublemetaphone('otto')
        self.assertEquals(result, ('AT', ''))
        result = doublemetaphone('aubrey')
        self.assertEquals(result, ('APR', ''))
        result = doublemetaphone('maurice')
        self.assertEquals(result, ('MRS', ''))
        result = doublemetaphone('auto')
        self.assertEquals(result, ('AT', ''))
        result = doublemetaphone('maisey')
        self.assertEquals(result, ('MS', ''))
        result = doublemetaphone('catherine')
        self.assertEquals(result, ('K0RN', 'KTRN'))
        result = doublemetaphone('geoff')
        self.assertEquals(result, ('JF', 'KF'))
        result = doublemetaphone('Chile')
        self.assertEquals(result, ('XL', ''))
        result = doublemetaphone('katherine')
        self.assertEquals(result, ('K0RN', 'KTRN'))
        result = doublemetaphone('steven')
        self.assertEquals(result, ('STFN', ''))
        result = doublemetaphone('zhang')
        self.assertEquals(result, ('JNK', ''))
        result = doublemetaphone('bob')
        self.assertEquals(result, ('PP', ''))
        result = doublemetaphone('ray')
        self.assertEquals(result, ('R', ''))
        result = doublemetaphone('Tux')
        self.assertEquals(result, ('TKS', ''))
        result = doublemetaphone('bryan')
        self.assertEquals(result, ('PRN', ''))
        result = doublemetaphone('bryce')
        self.assertEquals(result, ('PRS', ''))
        result = doublemetaphone('Rapelje')
        self.assertEquals(result, ('RPL', ''))
        result = doublemetaphone('richard')
        self.assertEquals(result, ('RXRT', 'RKRT'))
        result = doublemetaphone('solilijs')
        self.assertEquals(result, ('SLLS', ''))
        result = doublemetaphone('Dallas')
        self.assertEquals(result, ('TLS', ''))
        result = doublemetaphone('Schwein')
        self.assertEquals(result, ('XN', 'XFN'))
        result = doublemetaphone('dave')
        self.assertEquals(result, ('TF', ''))
        result = doublemetaphone('eric')
        self.assertEquals(result, ('ARK', ''))
        result = doublemetaphone('Parachute')
        self.assertEquals(result, ('PRKT', ''))
        result = doublemetaphone('brian')
        self.assertEquals(result, ('PRN', ''))
        result = doublemetaphone('randy')
        self.assertEquals(result, ('RNT', ''))
        result = doublemetaphone('Through')
        self.assertEquals(result, ('0R', 'TR'))
        result = doublemetaphone('Nowhere')
        self.assertEquals(result, ('NR', ''))
        result = doublemetaphone('heidi')
        self.assertEquals(result, ('HT', ''))
        result = doublemetaphone('Arnow')
        self.assertEquals(result, ('ARN', 'ARNF'))
        result = doublemetaphone('Thumbail')
        self.assertEquals(result, ('0MPL', 'TMPL'))

    def test_homophones(self):
        self.assertEqual(
            doublemetaphone(u"tolled"),
            doublemetaphone(u"told"))
        self.assertEqual(
            doublemetaphone(u"katherine"),
            doublemetaphone(u"catherine"))
        self.assertEqual(
            doublemetaphone(u"brian"),
            doublemetaphone(u"bryan"))

    def test_similar_names(self):
        result = doublemetaphone("Bartoš")
        self.assertEquals(result, ('PRTS', ''))
        result = doublemetaphone(u"Bartosz")
        self.assertEquals(result, ('PRTS', 'PRTX'))
        result = doublemetaphone(u"Bartosch")
        self.assertEquals(result, ('PRTX', ''))
        result = doublemetaphone(u"Bartos")
        self.assertEquals(result, ('PRTS', ''))

        result = set(doublemetaphone(u"Jablonski")).intersection(
            doublemetaphone(u"Yablonsky"))
        self.assertEquals(list(result), ['APLNSK'])
        result = set(doublemetaphone(u"Smith")).intersection(
            doublemetaphone(u"Schmidt"))
        self.assertEquals(list(result), ['XMT'])

    def test_non_english_unicode(self):
        result = doublemetaphone("andestādītu")
        self.assertEquals(result, ('ANTSTTT', ''))

    def test_c_cedilla(self):
        result = doublemetaphone("français")
        self.assertEquals(result, ('FRNS', 'FRNSS'))
        result = doublemetaphone("garçon")
        self.assertEquals(result, ('KRSN', ''))
        result = doublemetaphone("leçon")
        self.assertEquals(result, ('LSN', ''))

    def test_various_german(self):
        result = doublemetaphone("ach")
        self.assertEquals(result, ("AX", "AK"))
        result = doublemetaphone("bacher")
        self.assertEquals(result, ("PKR", ""))
        result = doublemetaphone("macher")
        self.assertEquals(result, ("MKR", ""))

    def test_various_italian(self):
        result = doublemetaphone("bacci")
        self.assertEquals(result, ("PX", ""))
        result = doublemetaphone("bertucci")
        self.assertEquals(result, ("PRTX", ""))
        result = doublemetaphone("bellocchio")
        self.assertEquals(result, ("PLX", ""))
        result = doublemetaphone("bacchus")
        self.assertEquals(result, ("PKS", ""))
        result = doublemetaphone("focaccia")
        self.assertEquals(result, ("FKX", ""))
        result = doublemetaphone("chianti")
        self.assertEquals(result, ("KNT", ""))
        result = doublemetaphone("tagliaro")
        self.assertEquals(result, ("TKLR", "TLR"))
        result = doublemetaphone("biaggi")
        self.assertEquals(result, ("PJ", "PK"))

    def test_various_spanish(self):
        result = doublemetaphone("bajador")
        self.assertEquals(result, ("PJTR", "PHTR"))
        result = doublemetaphone("cabrillo")
        self.assertEquals(result, ("KPRL", "KPR"))
        result = doublemetaphone("gallegos")
        self.assertEquals(result, ("KLKS", "KKS"))
        result = doublemetaphone("San Jacinto")
        self.assertEquals(result, ("SNHSNT", ""))

    def test_various_french(self):
        result = doublemetaphone("rogier")
        self.assertEquals(result, ("RJ", "RKR"))
        result = doublemetaphone("breaux")
        self.assertEquals(result, ("PR", ""))

    def test_various_slavic(self):
        result = doublemetaphone("Wewski")
        self.assertEquals(result, ("ASK", "FFSK"))

    def test_various_chinese(self):
        result = doublemetaphone("zhao")
        self.assertEquals(result, ("J", ""))

    def test_dutch_origin(self):
        result = doublemetaphone("school")
        self.assertEquals(result, ("SKL", ""))
        result = doublemetaphone("schooner")
        self.assertEquals(result, ("SKNR", ""))
        result = doublemetaphone("schermerhorn")
        self.assertEquals(result, ("XRMRRN", "SKRMRRN"))
        result = doublemetaphone("schenker")
        self.assertEquals(result, ("XNKR", "SKNKR"))

    def test_ch_words(self):
        result = doublemetaphone("Charac")
        self.assertEquals(result, ("KRK", ""))
        result = doublemetaphone("Charis")
        self.assertEquals(result, ("KRS", ""))
        result = doublemetaphone("chord")
        self.assertEquals(result, ("KRT", ""))
        result = doublemetaphone("Chym")
        self.assertEquals(result, ("KM", ""))
        result = doublemetaphone("Chia")
        self.assertEquals(result, ("K", ""))
        result = doublemetaphone("chem")
        self.assertEquals(result, ("KM", ""))
        result = doublemetaphone("chore")
        self.assertEquals(result, ("XR", ""))
        result = doublemetaphone("orchestra")
        self.assertEquals(result, ("ARKSTR", ""))
        result = doublemetaphone("architect")
        self.assertEquals(result, ("ARKTKT", ""))
        result = doublemetaphone("orchid")
        self.assertEquals(result, ("ARKT", ""))

    def test_cc_words(self):
        result = doublemetaphone("accident")
        self.assertEquals(result, ("AKSTNT", ""))
        result = doublemetaphone("accede")
        self.assertEquals(result, ("AKST", ""))
        result = doublemetaphone("succeed")
        self.assertEquals(result, ("SKST", ""))

    def test_mc_words(self):
        result = doublemetaphone("mac caffrey")
        self.assertEquals(result, ("MKFR", ""))
        result = doublemetaphone("mac gregor")
        self.assertEquals(result, ("MKRKR", ""))
        result = doublemetaphone("mc crae")
        self.assertEquals(result, ("MKR", ""))
        result = doublemetaphone("mcclain")
        self.assertEquals(result, ("MKLN", ""))

    def test_gh_words(self):
        result = doublemetaphone("laugh")
        self.assertEquals(result, ("LF", ""))
        result = doublemetaphone("cough")
        self.assertEquals(result, ("KF", ""))
        result = doublemetaphone("rough")
        self.assertEquals(result, ("RF", ""))

    def test_g3_words(self):
        result = doublemetaphone("gya")
        self.assertEquals(result, ("K", "J"))
        result = doublemetaphone("ges")
        self.assertEquals(result, ("KS", "JS"))
        result = doublemetaphone("gep")
        self.assertEquals(result, ("KP", "JP"))
        result = doublemetaphone("geb")
        self.assertEquals(result, ("KP", "JP"))
        result = doublemetaphone("gel")
        self.assertEquals(result, ("KL", "JL"))
        result = doublemetaphone("gey")
        self.assertEquals(result, ("K", "J"))
        result = doublemetaphone("gib")
        self.assertEquals(result, ("KP", "JP"))
        result = doublemetaphone("gil")
        self.assertEquals(result, ("KL", "JL"))
        result = doublemetaphone("gin")
        self.assertEquals(result, ("KN", "JN"))
        result = doublemetaphone("gie")
        self.assertEquals(result, ("K", "J"))
        result = doublemetaphone("gei")
        self.assertEquals(result, ("K", "J"))
        result = doublemetaphone("ger")
        self.assertEquals(result, ("KR", "JR"))
        result = doublemetaphone("danger")
        self.assertEquals(result, ("TNJR", "TNKR"))
        result = doublemetaphone("manager")
        self.assertEquals(result, ("MNKR", "MNJR"))
        result = doublemetaphone("dowager")
        self.assertEquals(result, ("TKR", "TJR"))

    def test_pb_words(self):
        result = doublemetaphone("Campbell")
        self.assertEquals(result, ("KMPL", ""))
        result = doublemetaphone("raspberry")
        self.assertEquals(result, ("RSPR", ""))

    def test_th_words(self):
        result = doublemetaphone("Thomas")
        self.assertEquals(result, ("TMS", ""))
        result = doublemetaphone("Thames")
        self.assertEquals(result, ("TMS", ""))
