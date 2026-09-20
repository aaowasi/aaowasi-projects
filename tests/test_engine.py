from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.core.assessment import run_assessment
from engine.collectors.aws_iam import analyze_iam_export
from engine.core.registry import select_frameworks
from engine.ingestion.router import ingest

ROOT = Path(__file__).resolve().parents[1]


class EngineTests(unittest.TestCase):
    def test_aws_iam_collector_detects_wildcard_admin(self):
        payload = analyze_iam_export(ROOT / "data" / "source" / "aws_iam.json")
        self.assertEqual(payload["wildcard_admin_count"], 0)
        self.assertIn("SOC2-CC6.1", payload["control_mappings"])
    def setUp(self) -> None:
        self.context = json.loads((ROOT / "examples/client-context-saas-ai-eu.json").read_text())
        self.evidence = json.loads((ROOT / "examples/evidence/demo-signals.json").read_text())

    def test_framework_selector_is_context_aware(self) -> None:
        selected = {item.framework_id for item in select_frameworks(self.context) if item.selected}
        self.assertIn("EU-AI-ACT", selected)
        self.assertIn("GDPR", selected)
        self.assertIn("ISO-27001-2022", selected)
        self.assertNotIn("HIPAA-SECURITY", selected)

    def test_six_state_summary_is_explicit(self) -> None:
        assessment = run_assessment(self.context, self.evidence)
        counts = assessment["summary"]["counts"]
        self.assertEqual(set(counts), {"PASS", "FAIL", "NOT_CONFIGURED", "ERROR", "NOT_APPLICABLE", "MANUAL_REVIEW"})
        self.assertGreaterEqual(counts["FAIL"], 1)
        self.assertGreaterEqual(counts["MANUAL_REVIEW"], 1)

    def test_missing_evidence_is_not_configured_not_fail(self) -> None:
        evidence = json.loads(json.dumps(self.evidence))
        del evidence["iam"]["admin_mfa_coverage"]
        results = {item["control_id"]: item for item in run_assessment(self.context, evidence)["results"]}
        self.assertEqual(results["IAM-001"]["state"], "NOT_CONFIGURED")

    def test_json_ingestion_hashes_and_parses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_text('{"ok": true}', encoding="utf-8")
            result = ingest(str(path))
            self.assertEqual(result["parser"], "json")
            self.assertTrue(result["content"]["ok"])
            self.assertEqual(len(result["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
