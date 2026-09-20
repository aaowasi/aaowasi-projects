from __future__ import annotations

import argparse
import json
from pathlib import Path

from engine.ai.model_router import select_model
from engine.assurance.reporting import write_report
from engine.collectors.aws_iam import analyze_iam_export
from engine.collectors.cloud_events import normalize_jsonl
from engine.collectors.github_alerts import collect_github_alerts
from engine.core.assessment import run_assessment
from engine.core.diagnostics import run_diagnostics
from engine.core.registry import select_frameworks
from engine.ingestion.router import ingest_many


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(prog="grc-engine", description="Adaptive, evidence-led enterprise assurance engine")
    commands = parser.add_subparsers(dest="command", required=True)

    scope = commands.add_parser("scope", help="select applicable frameworks from a client context")
    scope.add_argument("context")

    ingest = commands.add_parser("ingest", help="classify and safely parse one or more payloads")
    ingest.add_argument("sources", nargs="+")
    ingest.add_argument("--output", default="data/runtime/ingestion.json")

    assess = commands.add_parser("assess", help="run deterministic control tests")
    assess.add_argument("context")
    assess.add_argument("evidence")
    assess.add_argument("--json", default="reports/assurance-report.json")
    assess.add_argument("--markdown", default="reports/assurance-report.md")

    commands.add_parser("diagnostics", help="produce a self-diagnosis and operations action brief")

    model = commands.add_parser("select-model", help="select an optional authorized free/local helper model")
    model.add_argument("task")
    model.add_argument("--classification", default="PUBLIC")

    collect = commands.add_parser("collect", help="run a read-only evidence collector")
    collect.add_argument("collector", choices=["aws-iam", "github-alerts", "cloud-events"])
    collect.add_argument("source", nargs="?", help="source file for aws-iam or cloud-events")
    collect.add_argument("--output", default="data/runtime/collector-output.json")

    args = parser.parse_args()
    if args.command == "scope":
        payload = [decision.to_dict() for decision in select_frameworks(_load(args.context))]
        print(json.dumps(payload, indent=2))
    elif args.command == "ingest":
        payload = ingest_many(args.sources)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(output)
    elif args.command == "assess":
        payload = run_assessment(_load(args.context), _load(args.evidence))
        write_report(payload, Path(args.json))
        write_report(payload, Path(args.markdown))
        print(json.dumps(payload["summary"], indent=2))
        return 1 if payload["summary"]["counts"]["FAIL"] else 0
    elif args.command == "diagnostics":
        print(json.dumps(run_diagnostics(), indent=2))
    elif args.command == "select-model":
        print(json.dumps(select_model(args.task, args.classification), indent=2))
    elif args.command == "collect":
        if args.collector == "github-alerts":
            payload = collect_github_alerts()
        elif not args.source:
            parser.error(f"{args.collector} requires a source file")
        elif args.collector == "aws-iam":
            payload = analyze_iam_export(args.source)
        else:
            payload = normalize_jsonl(args.source)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
