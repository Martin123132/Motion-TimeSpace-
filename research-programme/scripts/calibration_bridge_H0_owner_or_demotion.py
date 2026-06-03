#!/usr/bin/env python3
"""Checkpoint 193: calibration bridge H0 owner or demotion gate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_193_NAME = "calibration-bridge-H0-owner-or-demotion"
CHECKPOINT_192_RUN = RUNS_ROOT / "20260601-000009-theta-H0-compensation-derivation-attempt"
CHECKPOINT_191_RUN = RUNS_ROOT / "20260601-000008-CMB-same-density-mock-likelihood-and-theta-derivation-bridge"
CHECKPOINT_190_RUN = RUNS_ROOT / "20260601-000007-CMB-matched-mock-likelihood-or-derivation-pivot"
CHECKPOINT_184_RUN = RUNS_ROOT / "20260601-000001-MTS-CMB-background-injection-dry-run"

STATUS = "calibration_H0_half_memory_bridge_numeric_candidate_parent_owner_missing"
CLAIM_CEILING = "H0_calibration_bridge_internal_candidate_only_no_parent_owner_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0
LATE_REFERENCE_H0 = 68.42175693081872


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 193 calibration bridge script"),
        (WORK_DIR / "192-theta-H0-compensation-derivation-attempt.md", "FLRW H0 compensation derivation checkpoint"),
        (CHECKPOINT_192_RUN / "status.json", "checkpoint 192 machine status"),
        (CHECKPOINT_192_RUN / "results" / "H0_prediction_comparison.csv", "checkpoint 192 H0 prediction comparison"),
        (CHECKPOINT_192_RUN / "results" / "parent_derivation_gap_ledger.csv", "checkpoint 192 parent derivation gaps"),
        (WORK_DIR / "191-CMB-same-density-mock-likelihood-and-theta-derivation-bridge.md", "theta bridge checkpoint"),
        (CHECKPOINT_191_RUN / "status.json", "checkpoint 191 machine status"),
        (CHECKPOINT_191_RUN / "results" / "H0_theta_linear_bridge.csv", "checkpoint 191 H0 bridge"),
        (WORK_DIR / "190-CMB-matched-mock-likelihood-or-derivation-pivot.md", "mock likelihood split checkpoint"),
        (CHECKPOINT_190_RUN / "status.json", "checkpoint 190 machine status"),
        (WORK_DIR / "184-MTS-CMB-background-injection-dry-run.md", "fixed MTS CMB background injection checkpoint"),
        (CHECKPOINT_184_RUN / "results" / "MTS_parameter_locks.csv", "fixed MTS parameter lock table"),
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


def h0_owner_ledger_rows(cmb_h0: float) -> list[dict[str, Any]]:
    checkpoint_192 = load_json(CHECKPOINT_192_RUN / "status.json")
    checkpoint_191 = load_json(CHECKPOINT_191_RUN / "status.json")
    return [
        {
            "H0_object": "late_reference_H0",
            "value": LATE_REFERENCE_H0,
            "source": "h_profiled_reference from locked MTS late-time branch",
            "owner_status": "empirical late-reference calibration, not parent-owned",
            "issue": "conflicts with same-density CMB profile unless a calibration map exists",
        },
        {
            "H0_object": "same_density_CMB_profile_H0",
            "value": cmb_h0,
            "source": "checkpoint 188/192 same-density CMB theta profile",
            "owner_status": "CMB mock-competitive profile, not parent-owned",
            "issue": "requires derivation of why MTS predicts lower H0",
        },
        {
            "H0_object": "FLRW_integral_law_H0",
            "value": checkpoint_192["integral_law_H0"],
            "source": "checkpoint 192 FLRW distance-response law",
            "owner_status": "partially derived FLRW bridge",
            "issue": "depends on locked B_mem and activation closure",
        },
        {
            "H0_object": "linear_theta_bridge_H0",
            "value": checkpoint_191["linear_predicted_profile_H0"],
            "source": "checkpoint 191 local theta derivative bridge",
            "owner_status": "numerical bridge",
            "issue": "does not provide parent clock/calibration owner",
        },
    ]


def bridge_candidate_rows(cmb_h0: float) -> tuple[list[dict[str, Any]], dict[str, float]]:
    ratio_actual = cmb_h0 / LATE_REFERENCE_H0
    inferred_b_exp = -2.0 * math.log(ratio_actual)
    inferred_b_linear = 2.0 * (1.0 - ratio_actual)
    candidates = [
        ("identity_single_H0", 1.0, "H_CMB = H_late", "single global H0 owner; no calibration bridge"),
        ("linear_half_memory", 1.0 - LOCKED_B_MEM / 2.0, "H_CMB = H_late (1 - B_mem/2)", "linearized half-memory clock factor"),
        ("exponential_half_memory", math.exp(-LOCKED_B_MEM / 2.0), "H_CMB = H_late exp(-B_mem/2)", "multiplicative half-memory clock factor"),
        ("inverse_half_memory", 1.0 / (1.0 + LOCKED_B_MEM / 2.0), "H_CMB = H_late/(1+B_mem/2)", "alternative rational half-memory factor"),
        ("linear_full_memory", 1.0 - LOCKED_B_MEM, "H_CMB = H_late (1 - B_mem)", "full-memory linear factor"),
        ("exponential_full_memory", math.exp(-LOCKED_B_MEM), "H_CMB = H_late exp(-B_mem)", "full-memory exponential factor"),
    ]
    rows: list[dict[str, Any]] = []
    for name, factor, formula, interpretation in candidates:
        predicted = LATE_REFERENCE_H0 * factor
        error = predicted - cmb_h0
        if name == "exponential_half_memory" and abs(error) < 0.05:
            status = "best_candidate"
        elif name in {"linear_half_memory", "inverse_half_memory"} and abs(error) < 0.08:
            status = "near_match_sidecar"
        elif name == "identity_single_H0":
            status = "rejected_single_H0"
        else:
            status = "rejected_or_pressure"
        rows.append(
            {
                "candidate": name,
                "formula": formula,
                "factor": factor,
                "predicted_CMB_H0": predicted,
                "actual_CMB_H0": cmb_h0,
                "error_H0": error,
                "abs_error_H0": abs(error),
                "relative_error": error / cmb_h0,
                "status": status,
                "interpretation": interpretation,
            }
        )
    rows.extend(
        [
            {
                "candidate": "inferred_B_from_exponential_ratio",
                "formula": "B_inferred = -2 ln(H_CMB/H_late)",
                "factor": ratio_actual,
                "predicted_CMB_H0": cmb_h0,
                "actual_CMB_H0": cmb_h0,
                "error_H0": inferred_b_exp - LOCKED_B_MEM,
                "abs_error_H0": abs(inferred_b_exp - LOCKED_B_MEM),
                "relative_error": (inferred_b_exp - LOCKED_B_MEM) / LOCKED_B_MEM,
                "status": "locked_B_consistency_check",
                "interpretation": "ratio-inferred B is very close to locked B_mem",
            },
            {
                "candidate": "inferred_B_from_linear_ratio",
                "formula": "B_inferred = 2(1-H_CMB/H_late)",
                "factor": ratio_actual,
                "predicted_CMB_H0": cmb_h0,
                "actual_CMB_H0": cmb_h0,
                "error_H0": inferred_b_linear - LOCKED_B_MEM,
                "abs_error_H0": abs(inferred_b_linear - LOCKED_B_MEM),
                "relative_error": (inferred_b_linear - LOCKED_B_MEM) / LOCKED_B_MEM,
                "status": "locked_B_consistency_check",
                "interpretation": "linearized ratio-inferred B is close but less clean than exponential",
            },
        ]
    )
    summary = {
        "actual_ratio": ratio_actual,
        "inferred_b_exp": inferred_b_exp,
        "inferred_b_linear": inferred_b_linear,
        "best_exponential_h0": LATE_REFERENCE_H0 * math.exp(-LOCKED_B_MEM / 2.0),
        "best_exponential_error": LATE_REFERENCE_H0 * math.exp(-LOCKED_B_MEM / 2.0) - cmb_h0,
        "best_linear_h0": LATE_REFERENCE_H0 * (1.0 - LOCKED_B_MEM / 2.0),
        "best_linear_error": LATE_REFERENCE_H0 * (1.0 - LOCKED_B_MEM / 2.0) - cmb_h0,
    }
    return rows, summary


def inferred_b_ratio_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "estimator": "exponential_half_memory_ratio",
            "formula": "B=-2 ln(H_CMB/H_late)",
            "H0_ratio": summary["actual_ratio"],
            "B_inferred": summary["inferred_b_exp"],
            "B_locked": LOCKED_B_MEM,
            "delta_B": summary["inferred_b_exp"] - LOCKED_B_MEM,
            "relative_delta_B": (summary["inferred_b_exp"] - LOCKED_B_MEM) / LOCKED_B_MEM,
            "status": "best_internal_B_readout",
        },
        {
            "estimator": "linear_half_memory_ratio",
            "formula": "B=2(1-H_CMB/H_late)",
            "H0_ratio": summary["actual_ratio"],
            "B_inferred": summary["inferred_b_linear"],
            "B_locked": LOCKED_B_MEM,
            "delta_B": summary["inferred_b_linear"] - LOCKED_B_MEM,
            "relative_delta_B": (summary["inferred_b_linear"] - LOCKED_B_MEM) / LOCKED_B_MEM,
            "status": "linearized_sidecar_readout",
        },
    ]


def calibration_derivation_attempt_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "attempt": "Assume late-reference H0 and CMB-profile H0 are not the same observable clock normalization.",
            "result": "Required ratio H_CMB/H_late is measured internally.",
            "status": "allowed_hypothesis",
        },
        {
            "step": 2,
            "attempt": "Test whether the ratio is controlled by the locked memory amplitude.",
            "result": f"H_CMB/H_late={summary['actual_ratio']}; exp(-B_mem/2)={math.exp(-LOCKED_B_MEM / 2.0)}",
            "status": "numeric_near_match",
        },
        {
            "step": 3,
            "attempt": "Infer B from the H0 ratio using B=-2 ln(H_CMB/H_late).",
            "result": f"B_inferred={summary['inferred_b_exp']}; B_locked={LOCKED_B_MEM}; delta={summary['inferred_b_exp'] - LOCKED_B_MEM}",
            "status": "strong_internal_consistency",
        },
        {
            "step": 4,
            "attempt": "Promote exp(-B/2) to a parent clock map.",
            "result": "No parent clock action or observer-map variation is available in current checkpoints.",
            "status": "not_derived",
        },
        {
            "step": 5,
            "attempt": "Use the bridge as current owner.",
            "result": "Allowed only as calibration closure/theorem target, not as public evidence.",
            "status": "closure_only",
        },
    ]


def owner_decision_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "owner_option": "single_global_H0",
            "decision": "reject",
            "evidence": f"H_late-H_CMB={LATE_REFERENCE_H0 - load_json(CHECKPOINT_192_RUN / 'status.json')['actual_profile_H0']}",
            "consequence": "cannot use both late-reference and same-density CMB branch without calibration map",
        },
        {
            "owner_option": "half_memory_exponential_clock_bridge",
            "decision": "promote_to_theorem_target_not_owner",
            "evidence": f"error_H0={summary['best_exponential_error']}; B_inferred_delta={summary['inferred_b_exp'] - LOCKED_B_MEM}",
            "consequence": "best current bridge; requires parent derivation",
        },
        {
            "owner_option": "half_memory_linear_clock_bridge",
            "decision": "keep_as_linearized_sidecar",
            "evidence": f"error_H0={summary['best_linear_error']}",
            "consequence": "useful first-order version of exponential candidate",
        },
        {
            "owner_option": "late_reference_primary_demote_CMB",
            "decision": "not_default",
            "evidence": "same-density CMB mock proxy is competitive and has FLRW compensation law",
            "consequence": "would throw away useful CMB branch too early",
        },
        {
            "owner_option": "CMB_same_density_primary_demote_late",
            "decision": "not_default",
            "evidence": "late branch came from previous SN/BAO/H(z) calibration work",
            "consequence": "would abandon late empirical pillar before calibration map is tested",
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "clock map variable",
            "needed_object": "A scalar or functional C whose saturated change is B_mem",
            "acceptance_condition": "parent action yields H_obs = H_parent exp(-C/2) or equivalent",
            "status": "missing",
        },
        {
            "contract": "observer-map variation",
            "needed_object": "variation of matter clocks/rulers under memory normalization",
            "acceptance_condition": "factor 1/2 is derived, not chosen because it fits H0",
            "status": "missing",
        },
        {
            "contract": "late/CMB domain rule",
            "needed_object": "rule deciding why late H0 and CMB-inferred H0 use different memory calibrations",
            "acceptance_condition": "same rule preserves SN/BAO/H(z) and CMB without post-hoc branch switching",
            "status": "missing",
        },
        {
            "contract": "local silence",
            "needed_object": "clock map must not violate local PPN/clock constraints",
            "acceptance_condition": "local q_loc or equivalent fixed point suppresses calibration locally",
            "status": "missing",
        },
        {
            "contract": "fixed amplitude owner",
            "needed_object": "derive B_mem=2/27",
            "acceptance_condition": "calibration bridge inherits B from parent theory rather than empirical lock",
            "status": "missing",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], summary: dict[str, float]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    near_match = abs(summary["best_exponential_error"]) < 0.05
    b_close = abs(summary["inferred_b_exp"] - LOCKED_B_MEM) < 0.001
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal calibration audit only",
        },
        {
            "gate": "half-memory exponential bridge matches H0 split",
            "status": "pass" if near_match else "warning",
            "evidence": f"error_H0={summary['best_exponential_error']}",
            "claim_allowed": "theorem target",
        },
        {
            "gate": "H0 ratio infers locked B_mem",
            "status": "pass" if b_close else "warning",
            "evidence": f"B_inferred={summary['inferred_b_exp']}; B_locked={LOCKED_B_MEM}",
            "claim_allowed": "internal consistency only",
        },
        {
            "gate": "parent clock map derived",
            "status": "fail",
            "evidence": "no action/observer-map variation derives exp(-B/2)",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "single H0 owner allowed",
            "status": "fail",
            "evidence": "late and CMB H0 differ by about 2.5 km/s/Mpc",
            "claim_allowed": "requires calibration bridge or demotion",
        },
        {
            "gate": "official likelihood",
            "status": "not_run",
            "evidence": "no Planck/ACT/SPT likelihood called",
            "claim_allowed": "no CMB claim",
        },
        {
            "gate": "support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The late-reference and CMB-profile H0 values are numerically connected by a half-memory calibration factor, especially exp(-B_mem/2). This is a strong theorem target but not parent-owned yet.",
            "late_reference_H0": LATE_REFERENCE_H0,
            "CMB_profile_H0": load_json(CHECKPOINT_192_RUN / "status.json")["actual_profile_H0"],
            "exp_half_memory_H0": summary["best_exponential_h0"],
            "exp_half_memory_error_H0": summary["best_exponential_error"],
            "B_inferred_from_H0_ratio": summary["inferred_b_exp"],
            "next_target": "194-half-memory-clock-map-derivation-attempt.md",
            "MTS_spectra_run": "false",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_193_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    cmb_h0 = float(load_json(CHECKPOINT_192_RUN / "status.json")["actual_profile_H0"])
    sources = source_register_rows()
    owner_rows = h0_owner_ledger_rows(cmb_h0)
    candidate_rows, summary = bridge_candidate_rows(cmb_h0)
    inferred_b_rows = inferred_b_ratio_rows(summary)
    derivation_rows = calibration_derivation_attempt_rows(summary)
    owner_decisions = owner_decision_rows(summary)
    parent_contract = parent_contract_rows()
    gates = claim_gate_rows(sources, summary)
    decision = decision_rows(summary)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            sources,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "H0_owner_ledger.csv": (
            owner_rows,
            ["H0_object", "value", "source", "owner_status", "issue"],
        ),
        "calibration_bridge_candidates.csv": (
            candidate_rows,
            ["candidate", "formula", "factor", "predicted_CMB_H0", "actual_CMB_H0", "error_H0", "abs_error_H0", "relative_error", "status", "interpretation"],
        ),
        "inferred_B_from_H0_ratio.csv": (
            inferred_b_rows,
            ["estimator", "formula", "H0_ratio", "B_inferred", "B_locked", "delta_B", "relative_delta_B", "status"],
        ),
        "calibration_derivation_attempt.csv": (
            derivation_rows,
            ["step", "attempt", "result", "status"],
        ),
        "candidate_derivation_contract.csv": (
            parent_contract,
            ["contract", "needed_object", "acceptance_condition", "status"],
        ),
        "H0_owner_decision_matrix.csv": (
            owner_decisions,
            ["owner_option", "decision", "evidence", "consequence"],
        ),
        "branch_demotion_decision.csv": (
            owner_decisions,
            ["owner_option", "decision", "evidence", "consequence"],
        ),
        "parent_clock_map_contract.csv": (
            parent_contract,
            ["contract", "needed_object", "acceptance_condition", "status"],
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
                "late_reference_H0",
                "CMB_profile_H0",
                "exp_half_memory_H0",
                "exp_half_memory_error_H0",
                "B_inferred_from_H0_ratio",
                "next_target",
                "MTS_spectra_run",
                "official_likelihood_run",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "late_reference_H0": LATE_REFERENCE_H0,
        "CMB_profile_H0": cmb_h0,
        "actual_H0_ratio": summary["actual_ratio"],
        "exp_half_memory_H0": summary["best_exponential_h0"],
        "exp_half_memory_error_H0": summary["best_exponential_error"],
        "linear_half_memory_H0": summary["best_linear_h0"],
        "linear_half_memory_error_H0": summary["best_linear_error"],
        "B_inferred_from_H0_ratio": summary["inferred_b_exp"],
        "B_locked": LOCKED_B_MEM,
        "parent_clock_map_derived": False,
        "MTS_spectra_run": False,
        "official_likelihood_run": False,
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
