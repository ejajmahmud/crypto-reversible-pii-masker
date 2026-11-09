"""Unit tests for crypto-reversible-pii-masker."""
import unittest
from crypto_reversible_pii_masker.masker import PIIMasker


class TestPIIMasker(unittest.TestCase):
    def setUp(self):
        self.masker = PIIMasker()

    def test_mask_and_unmask_cycle(self):
        raw = "User email is test.user@gmail.com and phone is 415-555-2671"
        res = self.masker.mask(raw)
        self.assertNotIn("test.user@gmail.com", res.masked_text)
        self.assertIn("<EMAIL_1>", res.masked_text)

        unmasked = self.masker.unmask(res.masked_text)
        self.assertEqual(unmasked, raw)
