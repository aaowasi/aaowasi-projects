import unittest,sqlite3,tempfile,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
SQL=re.search(r'export const RESERVE_SQL=`(.*?)`;', (ROOT/'server/evaluation-runtime.mjs').read_text(),re.S).group(1)
class MeteringTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'meter.db'
  with sqlite3.connect(self.path) as db:
   db.executescript((ROOT/'migrations/0001_evaluations.sql').read_text());db.execute("INSERT INTO tenants(id,name) VALUES ('tenant','Organization')")
 def tearDown(self):self.tmp.cleanup()
 def reserve(self,id):
  with sqlite3.connect(self.path,timeout=5) as db:
   db.execute(SQL,('tenant',id,'hash','2026-10-03','tenant','tenant'));return db.execute('SELECT changes()').fetchone()[0]
 def test_concurrent_users_share_atomic_two_run_allowance(self):
  with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(self.reserve,[str(i) for i in range(8)]))
  self.assertEqual(sum(results),2)
 def test_idempotency_does_not_consume_another_credit(self):
  self.assertEqual(self.reserve('same-request'),1);self.assertEqual(self.reserve('same-request'),0);self.assertEqual(self.reserve('next'),1);self.assertEqual(self.reserve('over-limit'),0)
 def test_failed_provider_run_releases_allowance(self):
  self.reserve('failed')
  with sqlite3.connect(self.path) as db:db.execute("UPDATE evaluations SET status='failed' WHERE request_id='failed'")
  self.assertEqual(self.reserve('second'),1);self.assertEqual(self.reserve('third'),1);self.assertEqual(self.reserve('fourth'),0)
 def test_other_tenant_has_separate_allowance(self):
  self.reserve('one');self.reserve('two')
  with sqlite3.connect(self.path) as db:
   db.execute("INSERT INTO tenants(id,name) VALUES ('other','Other')");db.execute(SQL,('other','one','hash','date','other','other'));self.assertEqual(db.execute('SELECT changes()').fetchone()[0],1)
