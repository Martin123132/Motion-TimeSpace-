from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "empirical-preflight-readout-after-281"
STATUS = "empirical_preflights_run_local_proxy_passed_cosmo_schema_blocked_by_BAO_manifest"
CLAIM_CEILING = "dryrun_and_proxy_preflight_only_no_empirical_support_claim"

LOCAL_RUN = ROOT / "runs" / "20260601-000100-local-bound-preflight-and-baseline-comparison"
COSMO_SCHEMA_RUN = ROOT / "runs" / "20260601-093239-cosmo-SN-BAO-closure-dryrun"
FIXED_KAPPA_RUN = ROOT / "runs" / "20260601-000101-fixed-vs-kappa-free-SN-BAO-dryrun-runner"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "281-empirical-closure-test-design-after-local-ledger.md", "test design checkpoint"),
        (ROOT / "runs" / "20260601-000099-empirical-closure-test-design-after-local-ledger" / "results" / "test_manifest.csv", "test manifest"),
        (LOCAL_RUN / "status.json", "T1 local proxy preflight status"),
        (LOCAL_RUN / "results" / "claim_gate_results.csv", "T1 local proxy gate results"),
        (COSMO_SCHEMA_RUN / "status.json", "T2 SN+BAO schema dry-run status"),
        (COSMO_SCHEMA_RUN / "results" / "data_schema_report.csv", "T2 data schema report"),
        (FIXED_KAPPA_RUN / "status.json", "T3 fixed-vs-kappa dry-run status"),
        (FIXED_KAPPA_RUN / "results" / "preflight_gates.csv", "T3 preflight gates"),
        (ROOT / "scripts" / "empirical_preflight_readout_after_281.py", "this readout script"),
    ]
    return [
        {"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"}
        for path, role in sources
    ]


def dryrun_status_rows() -> list[dict[str, Any]]:
    local = read_json(LOCAL_RUN / "status.json")
    cosmo = read_json(COSMO_SCHEMA_RUN / "status.json")
    fixed = read_json(FIXED_KAPPA_RUN / "status.json")
    return [
        {
            "test_id": "T1_local_proxy_bound_preflight",
            "run": relpath(LOCAL_RUN),
            "status": local["status"],
            "scores_generated": "proxy_only",
            "promotion_allowed": local["promotion_allowed"],
            "readout": f"worst_q_ratio={local['worst_base_q_proxy_ratio']}; tightest_budget={local['tightest_coefficient_budget']}",
            "next_action": local["next_target"],
        },
        {
            "test_id": "T2_SN_BAO_schema_dryrun",
            "run": relpath(COSMO_SCHEMA_RUN),
            "status": cosmo["readout"],
            "scores_generated": cosmo["scores_written"],
            "promotion_allowed": cosmo["stable_evidence_allowed"],
            "readout": ";".join(cosmo.get("failures", [])) or "schema ready",
            "next_action": cosmo["next_action"],
        },
        {
            "test_id": "T3_fixed_vs_kappa_dryrun",
            "run": relpath(FIXED_KAPPA_RUN),
            "status": fixed["status"],
            "scores_generated": fixed["scores_generated"],
            "promotion_allowed": fixed["promotion_allowed"],
            "readout": f"n_eff={fixed['n_eff_template']}; AIC_tax={fixed['kappa_AIC_tax_delta_chi2']}; BIC_tax={fixed['kappa_BIC_tax_delta_chi2']}",
            "next_action": fixed["next_target"],
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    local = read_json(LOCAL_RUN / "status.json")
    cosmo = read_json(COSMO_SCHEMA_RUN / "status.json")
    fixed = read_json(FIXED_KAPPA_RUN / "status.json")
    return [
        {
            "gate": "local_proxy_preflight_completed",
            "status": "pass" if local["missing_sources"] == 0 and local["compact_base_proxy_failures"] == 0 else "fail",
            "evidence": f"missing_sources={local['missing_sources']}; compact_failures={local['compact_base_proxy_failures']}",
            "claim_effect": "proxy readiness only; no PPN promotion",
        },
        {
            "gate": "local_proxy_headroom_exists",
            "status": "warn",
            "evidence": f"worst_base_q_proxy_ratio={local['worst_base_q_proxy_ratio']}; tightest_budget={local['tightest_coefficient_budget']}",
            "claim_effect": "not official bounds; use to prioritize residual vector",
        },
        {
            "gate": "SN_BAO_schema_ready",
            "status": "fail" if not cosmo["data_ready_for_short_smoke"] else "pass",
            "evidence": ";".join(cosmo.get("failures", [])) or "data_ready",
            "claim_effect": "do not run generic SN+BAO short smoke until BAO manifest is fixed",
        },
        {
            "gate": "fixed_vs_kappa_dryrun_ready",
            "status": "pass" if fixed["missing_sources"] == 0 and not fixed["scores_generated"] else "fail",
            "evidence": f"template rows SN={fixed['SN_rows_template']} BAO={fixed['BAO_DR2_rows_template']}",
            "claim_effect": "short smoke may be attempted through this runner if data/template assumptions are accepted",
        },
        {
            "gate": "empirical_support_claim_allowed",
            "status": "fail",
            "evidence": "no scores generated; one schema branch blocked",
            "claim_effect": "no empirical support claim",
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker": "BAO_distance_data_not_validated",
            "affects": "T2 generic SN+BAO dry-run and no-SH0ES branch",
            "evidence": relpath(COSMO_SCHEMA_RUN / "status.json"),
            "fix": "provide explicit --bao-data and --bao-cov or create local data manifest that maps existing BAO files to runner schema",
            "priority": "highest_before_generic_short_smoke",
        },
        {
            "blocker": "official_local_bound_manifest_absent",
            "affects": "local PPN/local-gravity claim level",
            "evidence": relpath(LOCAL_RUN / "status.json"),
            "fix": "map proxy residual vector to official bound manifest before any PPN statement",
            "priority": "high",
        },
        {
            "blocker": "scores_not_generated",
            "affects": "empirical support claims",
            "evidence": "T1 proxy only; T2 dry-run only; T3 dry-run only",
            "fix": "after schema pass, run short-smoke with residuals, prior-edge table, and baseline comparison",
            "priority": "normal_next",
        },
    ]


def next_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "order": 1,
            "action": "build_or_repair_BAO_data_manifest",
            "reason": "generic SN+BAO runner blocked on BAO_distance_data_not_validated",
            "claim_allowed_after": "schema readiness only",
        },
        {
            "order": 2,
            "action": "run_fixed_vs_kappa_short_smoke_if_runner_inputs_are_accepted",
            "reason": "fixed-vs-kappa dry-run passed and gives explicit AIC/BIC penalty template",
            "claim_allowed_after": "short-smoke closure score only",
        },
        {
            "order": 3,
            "action": "write_local_residual_vector_to_official_bound_manifest",
            "reason": "local proxy preflight is not official PPN evidence",
            "claim_allowed_after": "constraint readiness, not local-GR proof",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The first empirical preflights were executed. "
                "Local proxy preflight completed with no compact proxy failures but remains non-promotional. "
                "Generic SN+BAO schema dry-run is blocked by unvalidated BAO distance data. "
                "Fixed-vs-kappa dry-run passed without scores and is the cleanest path to a short-smoke once its template assumptions are accepted."
            ),
            "next_target": "BAO_data_manifest_repair_or_fixed_vs_kappa_short_smoke",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "dryrun_status_matrix.csv": (
            dryrun_status_rows(),
            ["test_id", "run", "status", "scores_generated", "promotion_allowed", "readout", "next_action"],
        ),
        "gate_results.csv": (gate_rows(), ["gate", "status", "evidence", "claim_effect"]),
        "blockers.csv": (blocker_rows(), ["blocker", "affects", "evidence", "fix", "priority"]),
        "next_actions.csv": (next_action_rows(), ["order", "action", "reason", "claim_allowed_after"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    cosmo = read_json(COSMO_SCHEMA_RUN / "status.json")
    local = read_json(LOCAL_RUN / "status.json")
    fixed = read_json(FIXED_KAPPA_RUN / "status.json")
    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "scores_generated": False,
        "local_proxy_preflight_passed": local["missing_sources"] == 0 and local["compact_base_proxy_failures"] == 0,
        "generic_SN_BAO_schema_ready": bool(cosmo["data_ready_for_short_smoke"]),
        "generic_SN_BAO_failures": cosmo.get("failures", []),
        "fixed_vs_kappa_dryrun_passed": fixed["missing_sources"] == 0 and fixed["scores_generated"] is False,
        "empirical_support_claim_allowed": False,
        "next_target": "BAO_data_manifest_repair_or_fixed_vs_kappa_short_smoke",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Empirical preflight readout after checkpoint 281.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
