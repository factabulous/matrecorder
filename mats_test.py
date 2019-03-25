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

    def test_record(self):
        m = mats.Mats("material_info.json")
        self.assertEqual(0, len(m.recent()))
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        self.assertEqual(1, len(m.recent()))
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        # Should by default return this many events
        self.assertEqual(5, len(m.recent()))
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        self.assertEqual(5, len(m.recent()))
        self.assertEqual(1, len(m.recent(count=1)))

    def test_record_bad_name(self):
        m = mats.Mats("material_info.json")
        self.assertEqual(0, len(m.recent()))
        m.record("gold", "Gold", 3)
        self.assertEqual(0, len(m.recent()))
       

if __name__ == "__main__":
    unittest.main()
   
