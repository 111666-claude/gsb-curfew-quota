import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from curfew.guard import Guard  # noqa: E402


class CurfewTest(unittest.TestCase):
    def test_inside_curfew(self):
        self.assertTrue(Guard(22, 8, 3600000).in_curfew(23 * 3600000))

    def test_outside_curfew(self):
        self.assertFalse(Guard(22, 8, 3600000).in_curfew(12 * 3600000))

    def test_remaining_starts_at_limit(self):
        self.assertEqual(Guard(22, 8, 3600000).remaining_ms("p1", 1), 3600000)


if __name__ == "__main__":
    unittest.main()
