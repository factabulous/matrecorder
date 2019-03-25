#!/usr/bin/env python3

import mats
import unittest

class MatsTest(unittest.TestCase):

    def test_grade(self):
        m = mats.Mats("material_info.json")
        self.assertEqual(5, m.grade("dataminedwake"))
        self.assertEqual(1, m.grade("iron"))
        self.assertIsNone(m.grade("gold"))

    def test_maximum(self):
        m = mats.Mats("material_info.json")
        self.assertEqual(100, m.maximum("dataminedwake"))
        self.assertEqual(300, m.maximum("sulphur"))
        self.assertEqual(None, m.maximum("gold"))
       

if __name__ == "__main__":
    unittest.main()
   
