'''
Unit test for module utils.
'''

import unittest
from unittest import TestCase
from utils import DecimalVector2
from decimal import Decimal

class DecimalVector2TestCase(TestCase):
    def test_create(self):
        v1 = DecimalVector2(1, 2)
        self.assertEqual((v1.x, v1.y), (Decimal(1), Decimal(2)))
        v1 = DecimalVector2("1.12", "2.23")
        self.assertEqual((v1.x, v1.y), (Decimal("1.12"), Decimal("2.23")))

    def test_eq(self):
        self.assertEqual(DecimalVector2("1.123", "2.456"), DecimalVector2("1.123", "2.456"))

    def test_add_sub(self):
        self.assertEqual(DecimalVector2(1, 2) + DecimalVector2(2, 3), DecimalVector2(3, 5))
        self.assertEqual(DecimalVector2("3.2", "1.1") - DecimalVector2("1.1", "0.9"), DecimalVector2("2.1", "0.2"))

    def test_mul_div(self):
        self.assertEqual(DecimalVector2(2, 3) * DecimalVector2(4, 5), Decimal(2 * 4 + 3 * 5))
        self.assertEqual(DecimalVector2(2, 3) * DecimalVector2("4.2", "5.1"), 2 * Decimal("4.2") + 3 * Decimal("5.1"))
        self.assertEqual(DecimalVector2(2, 3) * Decimal("1.5"), DecimalVector2(3, "4.5"))
        self.assertEqual(DecimalVector2(1, 2) / 11, DecimalVector2(Decimal(1) / Decimal(11), Decimal(2) / Decimal(11)))

unittest.main()