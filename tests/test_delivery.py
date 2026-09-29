import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_delivery import render
class DeliveryEvidenceTests(unittest.TestCase):
 def setUp(self):self.data=json.loads((ROOT/'content/verified-delivery.json').read_text())
 def test_actual_counts_and_elapsed(self):
  html=render(self.data)
  self.assertIn('3 successful workflow checks',html)
  for seconds in [11,12,13]:self.assertIn(f'{seconds} seconds',html)
  self.assertIn('not audit duration',html)
 def test_commit_mismatch_rejected(self):
  self.data['repositories'][0]['runs'][0]['commit']='0'*40
  with self.assertRaises(ValueError):render(self.data)
 def test_negative_interval_rejected(self):
  self.data['repositories'][0]['runs'][0]['updatedAt']='2020-01-01T00:00:00Z'
  with self.assertRaises(ValueError):render(self.data)
 def test_untrusted_url_rejected(self):
  self.data['repositories'][0]['runs'][0]['url']='javascript:alert(1)'
  with self.assertRaises(ValueError):render(self.data)
