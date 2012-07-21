# -*- coding: utf-8 -*-
import unittest

from metaphone import doublemetaphone


class MetaphoneTestCase(unittest.TestCase):
    """
    """
    def test_singleResult(self):
        result = doublemetaphone(u"aubrey")
        self.assertEquals(result, ('APR', ''))

    def test_doubleResult(self):
        result = doublemetaphone(u"richard")
        self.assertEquals(result, ('RXRT', 'RKRT'))

    def test_homophones(self):
        self.assertEqual(
            doublemetaphone(u"tolled"),
            doublemetaphone(u"told"))
        self.assertEqual(
            doublemetaphone(u"katherine"),
            doublemetaphone(u"catherine"))

    def test_similarNames(self):
        result = doublemetaphone("Bartoš")
        self.assertEquals(result, ('PRTS', ''))
        result = doublemetaphone(u"Bartosz")
        self.assertEquals(result, ('PRTS', 'PRTX'))
        result = doublemetaphone(u"Bartosch")
        self.assertEquals(result, ('PRTX', ''))
        result = doublemetaphone(u"Bartos")
        self.assertEquals(result, ('PRTS', ''))

    def test_nonEnglishUnicode(self):
        result = doublemetaphone("andestādītu")
        self.assertEquals(result, ('NTSTTT', ''))

    def test_variousGerman(self):
        result = doublemetaphone("ach")
        self.assertEquals(result, ("AX", "AK"))
        result = doublemetaphone("bacher")
        self.assertEquals(result, ("PKR", ""))
        result = doublemetaphone("macher")
        self.assertEquals(result, ("MKR", ""))

    def test_variousItalian(self):
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

    def test_variousSpanish(self):
        result = doublemetaphone("bajador")
        self.assertEquals(result, ("PJTR", "PHTR"))
        result = doublemetaphone("cabrillo")
        self.assertEquals(result, ("KPRL", "KPR "))
        result = doublemetaphone("gallegos")
        self.assertEquals(result, ("KLKS", "K KS"))

    def test_variousFrench(self):
        result = doublemetaphone("rogier")
        self.assertEquals(result, ("RJ", "RKR"))
        result = doublemetaphone("breaux")
        self.assertEquals(result, ("PR", ""))

    def test_variousSlavic(self):
        result = doublemetaphone("Wewski")
        self.assertEquals(result, ("ASK", "FFSK"))

    def test_variousChinese(self):
        result = doublemetaphone("zhao")
        self.assertEquals(result, ("J", ""))

    def test_DutchOrigin(self):
        result = doublemetaphone("school")
        self.assertEquals(result, ("SKL", ""))
        result = doublemetaphone("schooner")
        self.assertEquals(result, ("SKNR", ""))
        result = doublemetaphone("schermerhorn")
        self.assertEquals(result, ("XRMRRN", "SKRMRRN"))
        result = doublemetaphone("schenker")
        self.assertEquals(result, ("XNKR", "SKNKR"))

    def test_ChWords(self):
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

    def test_CcWords(self):
        result = doublemetaphone("accident")
        self.assertEquals(result, ("AKSTNT", ""))
        result = doublemetaphone("accede")
        self.assertEquals(result, ("AKST", ""))
        result = doublemetaphone("succeed")
        self.assertEquals(result, ("SKST", ""))

    def test_McWords(self):
        result = doublemetaphone("mac caffrey")
        self.assertEquals(result, ("MKFR", ""))
        result = doublemetaphone("mac gregor")
        self.assertEquals(result, ("MKRKR", ""))
        result = doublemetaphone("mc crae")
        self.assertEquals(result, ("MKR", ""))
        result = doublemetaphone("mcclain")
        self.assertEquals(result, ("MKLN", ""))

    def test_GhWords(self):
        result = doublemetaphone("laugh")
        self.assertEquals(result, ("LF", ""))
        result = doublemetaphone("cough")
        self.assertEquals(result, ("KF", ""))
        result = doublemetaphone("rough")
        self.assertEquals(result, ("RF", ""))

    def test_G3Words(self):
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

    def test_PbWords(self):
        result = doublemetaphone("Campbell")
        self.assertEquals(result, ("KMPL", ""))
        result = doublemetaphone("raspberry")
        self.assertEquals(result, ("RSPR", ""))

    def test_ThWords(self):
        result = doublemetaphone("Thomas")
        self.assertEquals(result, ("TMS", ""))
        result = doublemetaphone("Thames")
        self.assertEquals(result, ("TMS", ""))
