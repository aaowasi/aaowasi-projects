import unittest
from scripts.monitor_regulations import observe, check_url, fingerprint

REGISTRY={"version":1,"sources":[{
 "url":"https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10",
 "jurisdiction":"United States","title":"NIST AI RMF","domainSlugs":["ai-governance"]
}]}
A="<html><body><h1>Official content</h1><p>" + "Governance framework content. "*20 + "</p></body></html>"
B=A.replace("Governance framework", "Updated risk and governance")


class RegulatoryWatchTests(unittest.TestCase):
 def test_baseline_change_pending_is_never_silently_approved(self):
  first=observe(REGISTRY,{"entries":[]},lambda u:fingerprint(A.encode()),"2026-10-10T01:00:00Z")
  old=first["entries"][0]
  self.assertEqual(old["reviewState"],"baseline")
  self.assertEqual(old["fetchStatus"],"observed")
  changed=observe(REGISTRY,first,lambda u:fingerprint(B.encode()),"2026-10-11T01:00:00Z")
  new=changed["entries"][0]
  self.assertEqual(new["reviewState"],"change_pending_review")
  self.assertEqual(new["previousFingerprint"],old["fingerprint"])
  self.assertNotEqual(new["fingerprint"],old["fingerprint"])
  unchanged=observe(REGISTRY,changed,lambda u:fingerprint(B.encode()),"2026-10-12T01:00:00Z")
  self.assertEqual(unchanged["entries"][0]["reviewState"],"change_pending_review")
  self.assertEqual(unchanged["entries"][0]["changeDetectedAt"],"2026-10-11T01:00:00Z")
  self.assertEqual(unchanged["entries"][0]["lastSuccessfulAt"],"2026-10-12T01:00:00Z")

 def test_transient_source_failure_does_not_erase_last_known_source(self):
  original=observe(REGISTRY,{"entries":[]},lambda u:fingerprint(A.encode()),"2026-10-10T01:00:00Z")
  def broken(url): raise OSError("simulated offline")
  out=observe(REGISTRY,original,broken,"2026-10-11T01:00:00Z")["entries"][0]
  self.assertEqual(out["reviewState"],"baseline")
  self.assertEqual(out["fetchStatus"],"unavailable")
  self.assertEqual(out["lastSuccessfulAt"],"2026-10-10T01:00:00Z")
  self.assertEqual(out["fingerprint"],original["entries"][0]["fingerprint"])
  self.assertNotIn("simulated offline",out["detail"])

 def test_url_allowlist_and_uniqueness(self):
  for url in ["http://www.nist.gov", "https://internal.local/test", "https://www.nist.gov.evil.org",
              "https://user@www.nist.gov/test","https://www.nist.gov:444/test"]:
   with self.assertRaises(ValueError): check_url(url)
  duplicated={**REGISTRY,"sources":REGISTRY["sources"]*2}
  with self.assertRaises(ValueError): observe(duplicated,{"entries":[]},lambda u:"0"*64)

 def test_non_text_gibberish_is_not_falsely_verified(self):
  with self.assertRaises(ValueError): fingerprint(b"not an HTML document")
  with self.assertRaises(ValueError): fingerprint(b"<p>test</p>"*(1000000))
  self.assertEqual(fingerprint(A.encode()),fingerprint((A+"<script>var t=1;</script>").encode()))


if __name__=="__main__": unittest.main()
