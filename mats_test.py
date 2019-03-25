#!/usr/bin/env python3

import mats
import unittest

class MatsTest(unittest.TestCase):

    def test_grade(self):
        m = mats.Mats("material_info.json")
        self.assertEqual(5, m.grade("dataminedwake"))
        self.assertEqual(1, m.grade("iron"))
        self.assertIsNone(m.grade("gold"))

if __name__ == "__main__":
    unittest.main()
   
