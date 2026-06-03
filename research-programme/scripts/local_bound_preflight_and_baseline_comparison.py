#!/usr/bin/env python3
"""Checkpoint 226: local-bound dry-run preflight and fair baseline comparison."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_226_NAME = "local-bound-preflight-and-baseline-comparison"
RUN_218 = RUNS_ROOT / "20260601-000035-sidecar-readonly-join-contract-or-local-qloc"
RUN_220 = RUNS_ROOT / "20260601-000037-Jrel-local-trivial-representative-or-closure-bound"
RUN_221 = RUNS_ROOT / "20260601-000038-Noether-source-identity-or-compact-PPN-closure-map"
RUN_225 = RUNS_ROOT / "20260601-000042-local-GR-route-ledger-and-empirical-pivot-gate"

STATUS = "local_bound_preflight_dryrun_ranked_no_PPN_promotion"
CLAIM_CEILING = "dryrun_local_bound_proxy_baseline_no_external_data_or_PPN_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 226 local-bound preflight script"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "effective scalar local fence and q_loc blocker"),
        (WORK_DIR / "218-sidecar-readonly-join-contract-or-local-qloc.md", "compact q proxy checkpoint"),
        (WORK_DIR / "220-Jrel-local-trivial-representative-or-closure-bound.md", "J_rel leakage bound checkpoint"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "PPN closure vector checkpoint"),
        (WORK_DIR / "225-local-GR-route-ledger-and-empirical-pivot-gate.md", "local route consolidation and pivot gate"),
        (RUN_218 / "results" / "local_q_proxy_readout.csv", "q proxy source rows"),
        (RUN_220 / "results" / "Jrel_closure_bound_table.csv", "J_rel leakage budget rows"),
        (RUN_221 / "results" / "compact_PPN_closure_vector.csv", "PPN closure vector rows"),
        (RUN_225 / "results" / "compact_local_bound_stack.csv", "consolidated bound stack"),
        (RUN_225 / "results" / "allowed_local_test_matrix.csv", "allowed test guardrails"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def preflight_input_rows() -> list[dict[str, Any]]:
    rows_225 = read_csv_rows(RUN_225 / "results" / "compact_local_bound_stack.csv")
    rows: list[dict[str, Any]] = []
    for row in rows_225:
        q_ratio = float(row["q_proxy_ratio_to_gate"])
        leakage_fraction = float(row["leakage_budget_fraction_of_gate"])
        response_coeff = row["max_order_unity_response_coefficient_proxy"]
        rows.append(
            {
                "case": row["case"],
                "use_in_gate": row["use_in_gate"],
                "q_total_proxy": float(row["q_total_proxy"]),
                "q_R_like_gate": float(row["q_R_like_gate"]),
                "q_proxy_ratio_to_gate": q_ratio,
                "q_headroom_fraction": 1.0 - q_ratio,
                "max_allowed_abs_Ploc_drel_Jrel_leakage": float(row["max_allowed_abs_Ploc_drel_Jrel_leakage"]),
                "leakage_budget_fraction_of_gate": leakage_fraction,
                "max_order_unity_response_coefficient_proxy": float(response_coeff) if response_coeff else "",
                "risk_readout": row["risk_readout"],
                "preflight_role": "compact_gate_case" if row["use_in_gate"] == "yes" else "stress_diagnostic",
            }
        )
    return rows


def baseline_comparison_rows(input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in input_rows:
        case = row["case"]
        q_gate = float(row["q_R_like_gate"])
        q_base = float(row["q_total_proxy"])
        leakage_budget = float(row["max_allowed_abs_Ploc_drel_Jrel_leakage"])
        rows.extend(
            [
                {
                    "case": case,
                    "baseline": "GR_reference",
                    "residual_model": "0 by local weak-field baseline construction",
                    "residual_value": 0.0,
                    "gate": q_gate,
                    "ratio_to_gate": 0.0,
                    "interpretation": "baseline reference, not a special exemption",
                },
                {
                    "case": case,
                    "baseline": "screened_EFT_cosmo_only",
                    "residual_model": "cosmological tidal/background terms only",
                    "residual_value": 0.0,
                    "gate": q_gate,
                    "ratio_to_gate": 0.0,
                    "interpretation": "checkpoint 179 fence; q_loc sector still separate",
                },
                {
                    "case": case,
                    "baseline": "MTS_base_compact_proxy",
                    "residual_model": "q_total_proxy before unmodelled J_rel leakage",
                    "residual_value": q_base,
                    "gate": q_gate,
                    "ratio_to_gate": q_base / q_gate,
                    "interpretation": "proxy compatibility only, no PPN promotion",
                },
                {
                    "case": case,
                    "baseline": "MTS_at_Jrel_budget",
                    "residual_model": "q_total_proxy + max_allowed_abs_Ploc_drel_Jrel_leakage",
                    "residual_value": q_base + leakage_budget,
                    "gate": q_gate,
                    "ratio_to_gate": (q_base + leakage_budget) / q_gate,
                    "interpretation": "saturates current q-like gate by construction",
                },
            ]
        )
    return rows


def coefficient_budget_rows(input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    coefficient_residuals = [
        ("gamma_minus_1", "c_gamma epsilon_J", "derive weak-field spatial curvature response"),
        ("beta_minus_1", "c_beta epsilon_J", "derive nonlinear temporal potential response"),
        ("Phi_minus_Psi", "c_slip epsilon_J", "derive anisotropic boundary stress/slip map"),
        ("G_eff_over_G_minus_1", "c_G epsilon_J", "derive local source renormalization"),
        ("alpha_clock", "c_clock epsilon_J", "prove no direct clock coupling or bound it"),
        ("epsilon_matter", "c_matter epsilon_J", "prove universal matter coupling or bound it"),
    ]
    rows: list[dict[str, Any]] = []
    for row in input_rows:
        if row["use_in_gate"] != "yes":
            continue
        q_gate = float(row["q_R_like_gate"])
        epsilon_budget = float(row["max_allowed_abs_Ploc_drel_Jrel_leakage"])
        coeff_max = q_gate / epsilon_budget if epsilon_budget > 0 else 0.0
        for residual, model, needed in coefficient_residuals:
            rows.append(
                {
                    "case": row["case"],
                    "residual": residual,
                    "closure_model": model,
                    "epsilon_J_budget": epsilon_budget,
                    "q_like_gate": q_gate,
                    "max_abs_coefficient_before_proxy_gate": coeff_max,
                    "unit_coefficient_ratio_to_gate": epsilon_budget / q_gate,
                    "priority": "highest" if coeff_max < 1.2 else "high" if coeff_max < 2.0 else "medium",
                    "needed_next_derivation": needed,
                    "claim_status": "coefficient_budget_only_no_PPN_claim",
                }
            )
    return rows


def priority_queue_rows(input_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact_rows = [row for row in input_rows if row["use_in_gate"] == "yes"]
    worst_base = max(compact_rows, key=lambda row: float(row["q_proxy_ratio_to_gate"]))
    worst_budget = min(compact_rows, key=lambda row: float(row["max_allowed_abs_Ploc_drel_Jrel_leakage"]))
    tightest_coeff = min(coefficient_rows, key=lambda row: float(row["max_abs_coefficient_before_proxy_gate"]))
    return [
        {
            "rank": 1,
            "target": f"{tightest_coeff['case']} coefficient map",
            "why": "smallest allowed unknown response coefficient before proxy gate",
            "metric": "max_abs_coefficient_before_proxy_gate",
            "value": tightest_coeff["max_abs_coefficient_before_proxy_gate"],
            "next_action": "derive or bound c_gamma/c_beta/c_slip/c_G/c_clock/c_matter for this class",
        },
        {
            "rank": 2,
            "target": f"{worst_base['case']} base q proxy",
            "why": "largest current q_proxy_ratio_to_gate before adding leakage",
            "metric": "q_proxy_ratio_to_gate",
            "value": worst_base["q_proxy_ratio_to_gate"],
            "next_action": "audit whether the compact-shell proxy is too conservative or missing cancellation",
        },
        {
            "rank": 3,
            "target": f"{worst_budget['case']} J_rel leakage budget",
            "why": "smallest absolute remaining source-leakage budget",
            "metric": "max_allowed_abs_Ploc_drel_Jrel_leakage",
            "value": worst_budget["max_allowed_abs_Ploc_drel_Jrel_leakage"],
            "next_action": "prioritize exact local J_rel representative or leakage bound here",
        },
        {
            "rank": 4,
            "target": "official local-bound data manifest",
            "why": "dry-run uses internal q-like proxy only",
            "metric": "external_data_status",
            "value": "not_pulled",
            "next_action": "if proceeding empirical, fetch/cite official bounds before any public statement",
        },
    ]


def fair_baseline_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy": "same_residual_vector",
            "GR_baseline": "q_loc=0, gamma=1, beta=1, Phi=Psi, universal matter coupling in the tested weak-field limit",
            "MTS_treatment": "use q proxy, epsilon_J budget, and explicit closure coefficients",
            "forbidden_shortcut": "only stress MTS while leaving baseline undefined",
        },
        {
            "policy": "same_gate_labels",
            "GR_baseline": "treated as reference residual zero for proxy gate",
            "MTS_treatment": "ratios reported against the same q-like gate",
            "forbidden_shortcut": "swap gates between models or residuals",
        },
        {
            "policy": "coefficient_honesty",
            "GR_baseline": "PPN coefficients fixed by GR field equations",
            "MTS_treatment": "coefficients c_i are unowned until derived",
            "forbidden_shortcut": "assume c_i=0 or c_i=1 as theorem",
        },
        {
            "policy": "external_data_hold",
            "GR_baseline": "do not update historical bounds in this dry-run",
            "MTS_treatment": "do not claim external pass without official-source manifest",
            "forbidden_shortcut": "treat internal proxy as a real observational likelihood",
        },
    ]


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    compact_base_failures = sum(
        row["use_in_gate"] == "yes" and float(row["q_proxy_ratio_to_gate"]) > 1.0
        for row in input_rows
    )
    tight_coeff = min(float(row["max_abs_coefficient_before_proxy_gate"]) for row in coefficient_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal dry-run only",
        },
        {
            "gate": "compact base proxies below q-like gate",
            "status": "pass" if compact_base_failures == 0 else "fail",
            "evidence": f"compact_base_failures={compact_base_failures}",
            "claim_allowed": "magnitude proxy",
        },
        {
            "gate": "fair baseline rows included",
            "status": "pass",
            "evidence": "GR_reference, screened_EFT_cosmo_only, MTS_base, MTS_budget rows generated",
            "claim_allowed": "baseline discipline",
        },
        {
            "gate": "tightest coefficient budget identified",
            "status": "pass",
            "evidence": f"tightest_coeff_proxy={tight_coeff}",
            "claim_allowed": "derivation target",
        },
        {
            "gate": "external local data used",
            "status": "fail",
            "evidence": "dry-run intentionally uses existing internal proxy inputs only",
            "claim_allowed": "no external-data claim",
        },
        {
            "gate": "PPN/local GR promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(priority_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    top = priority_rows[0]
    return [
        {
            "decision": STATUS,
            "meaning": "The dry-run local-bound preflight ranks the pressure points without using external data. The q-like base proxy remains below the internal gate for all compact cases, but unknown PPN response coefficients are tightest for the earth_GPS_shell class. The immediate derivation target is therefore not another global parent placeholder; it is the coefficient map from epsilon_J into gamma, beta, slip, G_eff, clock, and matter residuals, with an official local-bound manifest required before any observational claim.",
            "main_gain": "fair baseline table and residual priority queue are now explicit",
            "main_failure": "coefficient map and official external local-bound manifest are not yet derived/run",
            "top_priority": top["target"],
            "next_target": "227-local-PPN-coefficient-map-or-official-bound-manifest.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_226_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    input_rows = preflight_input_rows()
    baseline_rows = baseline_comparison_rows(input_rows)
    coefficient_rows = coefficient_budget_rows(input_rows)
    priority_rows = priority_queue_rows(input_rows, coefficient_rows)
    policy_rows = fair_baseline_policy_rows()
    gates = claim_gate_rows(source_rows, input_rows, coefficient_rows)
    decision = decision_rows(priority_rows)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "local_bound_preflight_inputs.csv": (
            input_rows,
            [
                "case",
                "use_in_gate",
                "q_total_proxy",
                "q_R_like_gate",
                "q_proxy_ratio_to_gate",
                "q_headroom_fraction",
                "max_allowed_abs_Ploc_drel_Jrel_leakage",
                "leakage_budget_fraction_of_gate",
                "max_order_unity_response_coefficient_proxy",
                "risk_readout",
                "preflight_role",
            ],
        ),
        "fair_baseline_comparison.csv": (
            baseline_rows,
            ["case", "baseline", "residual_model", "residual_value", "gate", "ratio_to_gate", "interpretation"],
        ),
        "coefficient_budget_ranking.csv": (
            coefficient_rows,
            [
                "case",
                "residual",
                "closure_model",
                "epsilon_J_budget",
                "q_like_gate",
                "max_abs_coefficient_before_proxy_gate",
                "unit_coefficient_ratio_to_gate",
                "priority",
                "needed_next_derivation",
                "claim_status",
            ],
        ),
        "residual_priority_queue.csv": (
            priority_rows,
            ["rank", "target", "why", "metric", "value", "next_action"],
        ),
        "fair_baseline_policy.csv": (
            policy_rows,
            ["policy", "GR_baseline", "MTS_treatment", "forbidden_shortcut"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "top_priority",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    compact_base_failures = sum(
        row["use_in_gate"] == "yes" and float(row["q_proxy_ratio_to_gate"]) > 1.0
        for row in input_rows
    )
    tightest_coeff_row = min(coefficient_rows, key=lambda row: float(row["max_abs_coefficient_before_proxy_gate"]))
    worst_base_row = max(
        [row for row in input_rows if row["use_in_gate"] == "yes"],
        key=lambda row: float(row["q_proxy_ratio_to_gate"]),
    )
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "compact_base_proxy_failures": compact_base_failures,
        "worst_base_q_proxy_case": worst_base_row["case"],
        "worst_base_q_proxy_ratio": float(worst_base_row["q_proxy_ratio_to_gate"]),
        "tightest_coefficient_case": tightest_coeff_row["case"],
        "tightest_coefficient_residual": tightest_coeff_row["residual"],
        "tightest_coefficient_budget": float(tightest_coeff_row["max_abs_coefficient_before_proxy_gate"]),
        "external_data_used": False,
        "official_bound_manifest_ready": False,
        "PPN_promoted": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
