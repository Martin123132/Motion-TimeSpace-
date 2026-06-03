from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "post-scale-lock-CMB-bridge-readiness-gate"
STATUS = "post_scale_lock_CMB_bridge_ready_for_matched_mock_or_official_preflight_no_CMB_claim"
CLAIM_CEILING = "CMB_bridge_readiness_only_no_official_likelihood_or_parent_promotion"
B_MEM_FIXED = 2.0 / 27.0

RUN_190 = ROOT / "runs" / "20260601-000007-CMB-matched-mock-likelihood-or-derivation-pivot" / "results"
RUN_193 = ROOT / "runs" / "20260601-000010-calibration-bridge-H0-owner-or-demotion" / "results"
RUN_195 = ROOT / "runs" / "20260601-000012-late-CMB-domain-rule-and-local-silence-gate" / "results"
RUN_261 = ROOT / "runs" / "20260601-000079-Hstar-H0-scale-lock-and-local-silence-attempt" / "results"
RUN_262 = ROOT / "runs" / "20260601-000080-boundary-Noether-scale-lock-attempt" / "results"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "189-CMB-profiled-shape-residual-and-likelihood-readiness.md", "profiled CMB shape residual readiness"),
        (ROOT / "190-CMB-matched-mock-likelihood-or-derivation-pivot.md", "matched mock likelihood proxy"),
        (ROOT / "193-calibration-bridge-H0-owner-or-demotion.md", "half-memory H0 bridge"),
        (ROOT / "195-late-CMB-domain-rule-and-local-silence-gate.md", "endpoint memory rule"),
        (ROOT / "261-Hstar-H0-scale-lock-and-local-silence-attempt.md", "Hstar scale-lock closure"),
        (ROOT / "262-boundary-Noether-scale-lock-attempt.md", "boundary/Noether closure lock"),
        (RUN_190 / "decision_snapshot.csv", "190 CMB mock likelihood decision rows"),
        (RUN_193 / "calibration_bridge_candidates.csv", "193 half-memory bridge candidates"),
        (RUN_193 / "inferred_B_from_H0_ratio.csv", "193 inferred B from H0 ratio"),
        (RUN_195 / "observable_domain_classification.csv", "195 endpoint observable classification"),
        (RUN_261 / "scale_lock_gate_results.csv", "261 Hstar gate results"),
        (RUN_262 / "scale_lock_branch_policy.csv", "262 scale-lock branch policy"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def bridge_numeric_rows() -> list[dict[str, Any]]:
    candidates = read_csv(RUN_193 / "calibration_bridge_candidates.csv")
    inferred = read_csv(RUN_193 / "inferred_B_from_H0_ratio.csv")
    rows: list[dict[str, Any]] = []
    for row in candidates:
        if row.get("candidate") in {
            "identity_single_H0",
            "linear_half_memory",
            "exponential_half_memory",
            "inverse_half_memory",
            "linear_full_memory",
            "exponential_full_memory",
        }:
            error = float(row["predicted_CMB_H0"]) - float(row["actual_CMB_H0"])
            rows.append(
                {
                    "object": row["candidate"],
                    "formula": row["formula"],
                    "value": row["predicted_CMB_H0"],
                    "reference": row["actual_CMB_H0"],
                    "error": error,
                    "readout": "best_half_memory_candidate" if row["candidate"] == "exponential_half_memory" else "comparison_candidate",
                }
            )
    for row in inferred:
        rows.append(
            {
                "object": row["estimator"],
                "formula": row["formula"],
                "value": row["B_inferred"],
                "reference": row["B_locked"],
                "error": row["delta_B"],
                "readout": "inferred_B_near_locked_value_not_derivation",
            }
        )
    return rows


def imported_mock_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(RUN_190 / "decision_snapshot.csv"):
        rows.append(
            {
                "arena": row["arena"],
                "data_vector": row["data_vector"],
                "MTS_chi2_proxy": row["MTS_chi2_proxy"],
                "MTS_delta_AIC_vs_LCDM": row["MTS_delta_AIC_vs_LCDM"],
                "MTS_delta_BIC_vs_LCDM": row["MTS_delta_BIC_vs_LCDM"],
                "verdict": row["verdict"],
                "claim_ceiling": "mock_likelihood_proxy_only",
            }
        )
    return rows


def endpoint_domain_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(RUN_195 / "observable_domain_classification.csv"):
        observable = row["observable"]
        if "CMB" in observable or "BAO" in observable or "local" in observable or "SN" in observable:
            rows.append(
                {
                    "observable": observable,
                    "endpoints": row["endpoints"],
                    "Delta_C": row["Delta_C"],
                    "post_scale_lock_status": endpoint_status(observable),
                }
            )
    return rows


def endpoint_status(observable: str) -> str:
    if "CMB" in observable:
        return "best_endpoint_bridge_candidate_but_parent_clock_map_and_official_likelihood_missing"
    if "BAO" in observable:
        return "mixed_ruler_hazard_needs_rd_bridge_no_CMB_claim"
    if "local" in observable:
        return "safe_only_with_parent_local_silence_or_domain_zero_mode"
    if "SN" in observable:
        return "late_common_mode_candidate_no_parent_promotion"
    return "classified_only"


def post_scale_lock_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy": "B_mem_amplitude",
            "status": "fixed_closure_theorem_target",
            "rule": "B_mem=2/27 remains imposed, not parent-derived",
            "claim_effect": "CMB bridge may use locked value only as closure",
        },
        {
            "policy": "Hstar_scale_lock",
            "status": "closure_locked",
            "rule": "Hstar=H0 is not derived after boundary/Noether attempt",
            "claim_effect": "no CMB or amplitude promotion from scale-lock",
        },
        {
            "policy": "half_memory_H0_bridge",
            "status": "numeric_theorem_target",
            "rule": "H_CMB=H_late exp(-B_mem/2) remains candidate endpoint map",
            "claim_effect": "must derive clock-map factor and endpoint domain rule before promotion",
        },
        {
            "policy": "same_density_CMB_branch",
            "status": "mock_likelihood_promising",
            "rule": "same-density profiled branch deserves stricter matched mock or official likelihood preflight",
            "claim_effect": "proxy only; no official CMB claim",
        },
        {
            "policy": "locked_Omega_m_CMB_branch",
            "status": "pressure_branch",
            "rule": "locked-Omega_m branch failed previous mock proxy",
            "claim_effect": "derive compensation or demote before CMB claim",
        },
    ]


def official_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "baseline_LCDM_reproduction",
            "current_status": "not_currently_verified_in_263",
            "evidence_needed": "CAMB/CLASS baseline spectra and likelihood reproduce official/reference LCDM before MTS scoring",
            "next_action": "preflight engine and reference data",
        },
        {
            "requirement": "same_data_covariance",
            "current_status": "not_ready",
            "evidence_needed": "official Planck/ACT/SPT TT/TE/EE/lensing likelihood covariance or documented matched proxy",
            "next_action": "choose official-likelihood path or declare proxy-only",
        },
        {
            "requirement": "theta_H0_compensation_owner",
            "current_status": "not_derived",
            "evidence_needed": "parent endpoint clock map derives exp(-B_mem/2) and same-density profile rather than fitting H0",
            "next_action": "derive clock-map owner or keep profiled branch penalized/proxy-only",
        },
        {
            "requirement": "perturbation_parent_owner",
            "current_status": "partial_effective_only",
            "evidence_needed": "parent perturbation equations, sound speed, anisotropic stress, lensing/ISW response",
            "next_action": "Boltzmann-interface contract or effective-parameter sensitivity grid",
        },
        {
            "requirement": "claim_gate",
            "current_status": "no_CMB_claim_allowed",
            "evidence_needed": "official likelihood or audited matched mock plus derivation of calibration bridge",
            "next_action": "write strict test manifest before any long CMB run",
        },
    ]


def next_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "test": "matched_mock_likelihood_refresh",
            "purpose": "rerun same-density branch against matched LCDM/wCDM/CPL controls with frozen post-scale-lock policy",
            "acceptance": "same-density remains near draw and locked-Omega_m is reported symmetrically",
            "claim_limit": "proxy only",
        },
        {
            "rank": 2,
            "test": "official_likelihood_preflight",
            "purpose": "verify local availability of CAMB/CLASS/Cobaya/Planck-lite assets and baseline reproduction",
            "acceptance": "baseline reproduces before MTS score is read",
            "claim_limit": "readiness only unless full likelihood succeeds",
        },
        {
            "rank": 3,
            "test": "half_memory_clock_map_derivation",
            "purpose": "derive or reject H_obs=H_parent exp(-DeltaC/2) with endpoint DeltaC=B_mem",
            "acceptance": "factor 1/2 and endpoint classes derive without fitting H0",
            "claim_limit": "theory gate",
        },
        {
            "rank": 4,
            "test": "BAO_rd_bridge_crosscheck",
            "purpose": "ensure CMB endpoint bridge does not contradict mixed BAO drag-ruler treatment",
            "acceptance": "BAO remains stable under same endpoint rules or is explicitly separated",
            "claim_limit": "bridge consistency only",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "endpoint_rule_exists",
            "result": "partial_pass",
            "evidence": "195 derives DeltaC endpoint algebra",
            "claim_effect": "supports bridge organization, not CMB evidence",
        },
        {
            "gate": "half_memory_numeric_match",
            "result": "pass_as_clue",
            "evidence": "193 exponential half-memory candidate nearly matches profiled H0 split",
            "claim_effect": "theorem target only",
        },
        {
            "gate": "same_density_mock_competitive",
            "result": "pass_proxy",
            "evidence": "190 TT+EE proxy chi2 about 0.00534 against matched control",
            "claim_effect": "justifies stricter CMB testing",
        },
        {
            "gate": "locked_Omega_m_mock_competitive",
            "result": "fail",
            "evidence": "190 TT+EE proxy chi2 about 81.7358",
            "claim_effect": "locked branch stays pressure branch",
        },
        {
            "gate": "official_likelihood_run",
            "result": "not_run",
            "evidence": "no official Planck/ACT/SPT likelihood invoked in this gate",
            "claim_effect": "no CMB support claim",
        },
        {
            "gate": "parent_clock_map_derived",
            "result": "fail",
            "evidence": "scale-lock remains closure; half-memory factor not parent-owned",
            "claim_effect": "no parent promotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "meaning": (
                "After the scale-lock closure lock, the CMB route is still alive only as a disciplined bridge/readiness program. "
                "The endpoint rule and half-memory H0 split are strong theorem targets, and the same-density mock proxy remains promising. "
                "But locked-Omega_m CMB is a pressure branch, no official likelihood has run, and the parent clock/calibration map is still missing."
            ),
            "next_target": "matched_mock_likelihood_refresh_or_official_likelihood_preflight_with_post_scale_lock_claim_gates",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "bridge_numeric_ledger.csv": (
            bridge_numeric_rows(),
            ["object", "formula", "value", "reference", "error", "readout"],
        ),
        "imported_CMB_mock_scorecard.csv": (
            imported_mock_rows(),
            ["arena", "data_vector", "MTS_chi2_proxy", "MTS_delta_AIC_vs_LCDM", "MTS_delta_BIC_vs_LCDM", "verdict", "claim_ceiling"],
        ),
        "endpoint_domain_policy.csv": (
            endpoint_domain_rows(),
            ["observable", "endpoints", "Delta_C", "post_scale_lock_status"],
        ),
        "post_scale_lock_CMB_policy.csv": (
            post_scale_lock_policy_rows(),
            ["policy", "status", "rule", "claim_effect"],
        ),
        "official_likelihood_readiness.csv": (
            official_readiness_rows(),
            ["requirement", "current_status", "evidence_needed", "next_action"],
        ),
        "next_CMB_test_matrix.csv": (
            next_test_rows(),
            ["rank", "test", "purpose", "acceptance", "claim_limit"],
        ),
        "claim_gate_results.csv": (
            claim_gate_rows(),
            ["gate", "result", "evidence", "claim_effect"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "B_mem_fixed": B_MEM_FIXED,
        "official_likelihood_run": False,
        "CMB_claim_allowed": False,
        "same_density_mock_branch": "promising_proxy_only",
        "locked_Omega_m_branch": "pressure_branch",
        "next_target": "matched_mock_likelihood_refresh_or_official_likelihood_preflight_with_post_scale_lock_claim_gates",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post-scale-lock CMB bridge/readiness gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
