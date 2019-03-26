#!/usr/bin/env python3

import mat_info
import unittest

class MatsTest(unittest.TestCase):

    def test_can_specify_filename(self):
        m = mat_info.Mats("material_info.json")
        self.assertTrue(m)

    def test_grade(self):
        m = mat_info.Mats()
        self.assertEqual(5, m.grade("dataminedwake"))
        self.assertEqual(1, m.grade("iron"))
        self.assertIsNone(m.grade("gold"))

    def test_maximum(self):
        m = mat_info.Mats()
        self.assertEqual(100, m.maximum("dataminedwake"))
        self.assertEqual(300, m.maximum("sulphur"))
        self.assertEqual(None, m.maximum("gold"))

    def test_has_events(self):
        m = mat_info.Mats()
        self.assertFalse(m.has_events())
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        self.assertTrue(m.has_events())
        m.reset()
        self.assertFalse(m.has_events())

    def test_record(self):
        m = mat_info.Mats()
        self.assertEqual(0, len(m.recent()))
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        self.assertEqual(1, len(m.recent()))
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        # Should by default return this many events
        self.assertEqual(1, len(m.recent()))
        m.record("sulphur", "sulphur", 3)
        self.assertEqual(2, len(m.recent()))
        self.assertEqual(1, len(m.recent(count=1)))

    def test_record_bad_name(self):
        m = mat_info.Mats()
        self.assertEqual(0, len(m.recent()))
        m.record("gold", "Gold", 3)
        self.assertEqual(0, len(m.recent()))

    def test_recent_info(self):
        m = mat_info.Mats()
        self.assertEqual(0, len(m.recent()))
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        info = m.recent(count=1)[0]
        self.assertEqual(100, info['maximum'])
        self.assertEqual(3, info['now'])
        self.assertEqual(3, info['percent'])
        self.assertEqual("Datamined Wake Exception", info['local'])
        m.record("dataminedwake", "Datamined Wake Exception", 3)
        info = m.recent(count=1)[0]
        self.assertEqual(6, info['now'])
        self.assertEqual(6, info['percent'])
        self.assertEqual(6, info['count'])

    def test_percent(self):
        m = mat_info.Mats()
        self.assertEqual(0, len(m.recent()))
        m.record("sulphur", "Sulphur", 3)
        info = m.recent(count=1)[0]
        self.assertEqual(1, info['percent'])
        m.record("sulphur", "Sulphur", 3)
        info = m.recent(count=1)[0]
        self.assertEqual(2, info['percent'])

    def test_snapshot(self):
        m = mat_info.Mats()
        m.snapshot( { "event": "Materials", "Raw":[ { "Name":"manganese", "Count":14 }]} )
        m.record("manganese", "Manganese", 3)
        info = m.recent(count=1)[0]
        self.assertEqual(17, info['now'])

    def test_grade_count(self):
        m = mat_info.Mats()
        m.record("sulphur", "Sulphur", 3)
        self.assertEqual( [ ( 1, 3) ], m.grade_counts())
       

if __name__ == "__main__":
    unittest.main()
   
