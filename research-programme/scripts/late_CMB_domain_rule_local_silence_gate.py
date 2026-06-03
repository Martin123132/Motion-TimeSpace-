#!/usr/bin/env python3
"""Checkpoint 195: late/CMB domain rule and local-silence gate."""

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

CHECKPOINT_195_NAME = "late-CMB-domain-rule-and-local-silence-gate"
CHECKPOINT_194_RUN = RUNS_ROOT / "20260601-000011-half-memory-clock-map-derivation-attempt"
CHECKPOINT_193_RUN = RUNS_ROOT / "20260601-000010-calibration-bridge-H0-owner-or-demotion"
CHECKPOINT_192_RUN = RUNS_ROOT / "20260601-000009-theta-H0-compensation-derivation-attempt"

STATUS = "late_CMB_endpoint_rule_partially_derived_local_silence_still_closure"
CLAIM_CEILING = "endpoint_clock_map_internal_only_local_silence_not_parent_derived_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0


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
        (Path(__file__).resolve(), "checkpoint 195 domain-rule/local-silence script"),
        (WORK_DIR / "194-half-memory-clock-map-derivation-attempt.md", "half-memory clock map checkpoint"),
        (CHECKPOINT_194_RUN / "status.json", "checkpoint 194 machine status"),
        (CHECKPOINT_194_RUN / "results" / "conformal_clock_map_algebra.csv", "checkpoint 194 conformal algebra"),
        (CHECKPOINT_194_RUN / "results" / "late_CMB_domain_rule_options.csv", "checkpoint 194 domain options"),
        (CHECKPOINT_194_RUN / "results" / "parent_action_contract.csv", "checkpoint 194 parent contract"),
        (WORK_DIR / "193-calibration-bridge-H0-owner-or-demotion.md", "H0 calibration bridge checkpoint"),
        (CHECKPOINT_193_RUN / "status.json", "checkpoint 193 machine status"),
        (WORK_DIR / "192-theta-H0-compensation-derivation-attempt.md", "FLRW distance-response checkpoint"),
        (CHECKPOINT_192_RUN / "status.json", "checkpoint 192 machine status"),
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


def endpoint_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "object": "matter metric",
            "equation": "tilde_g_munu = exp(C) g_munu",
            "consequence": "local clocks and local rulers scale as exp(C/2)",
            "status": "from_checkpoint_194",
        },
        {
            "step": 2,
            "object": "frequency/redshift endpoint map",
            "equation": "1+tilde_z = exp[(C_obs-C_emit)/2] (1+z_g)",
            "consequence": "absolute C cancels; only endpoint difference Delta C enters",
            "status": "derived_endpoint_rule",
        },
        {
            "step": 3,
            "object": "late-local source and observer",
            "equation": "C_emit ~= C_obs ~= B_mem",
            "consequence": "Delta C ~= 0, so common local calibration is absorbed",
            "status": "partial_domain_rule_for_late_local_ladders",
        },
        {
            "step": 4,
            "object": "CMB early-to-late comparison",
            "equation": "C_emit ~= 0, C_obs ~= B_mem",
            "consequence": "Delta C ~= B_mem, exposing exp(B_mem/2) in redshift/frequency and exp(-B_mem/2) in inferred H0",
            "status": "partial_domain_rule_for_CMB_endpoint_bridge",
        },
        {
            "step": 5,
            "object": "domain discriminator",
            "equation": "observable sensitivity is controlled by Delta C along the calibration endpoints, not by C_obs alone",
            "consequence": "prevents pure branch switching, but requires parent ownership of endpoint assignments",
            "status": "candidate_rule_not_parent_derived",
        },
    ]


def observable_domain_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable": "local clock comparison",
            "endpoints": "same laboratory or same screened local domain",
            "Delta_C": "approximately 0",
            "predicted_effect": "common-mode clock scaling cancels",
            "risk": "fails if local dot_C or gradient leaks",
            "status": "safe_only_if_local_fixed_point_exists",
        },
        {
            "observable": "SN distance ladder anchor",
            "endpoints": "late local calibrator to late local observer",
            "Delta_C": "approximately 0",
            "predicted_effect": "absolute calibration absorbs common exp(C/2)",
            "risk": "evolution of C across host/environment would mimic luminosity evolution",
            "status": "partial_pass_with_environmental_silence_condition",
        },
        {
            "observable": "late H(z)",
            "endpoints": "late cosmic clocks compared inside same saturated frame",
            "Delta_C": "small if saturated over the interval",
            "predicted_effect": "uses late-reference H0 rather than CMB-rescaled H0",
            "risk": "nonzero dot_C term shifts measured H",
            "status": "conditional_on_slow_or_saturated_C",
        },
        {
            "observable": "CMB acoustic angle",
            "endpoints": "early recombination ruler to late observer clock/ruler",
            "Delta_C": "approximately B_mem",
            "predicted_effect": "H0 inference gets exp(-B_mem/2) bridge",
            "risk": "requires perturbation and recombination consistency",
            "status": "best_supported_endpoint_case",
        },
        {
            "observable": "BAO drag ruler",
            "endpoints": "early drag ruler to late galaxy survey ruler",
            "Delta_C": "mixed early-late object",
            "predicted_effect": "not safely classified by local cancellation alone",
            "risk": "could shift rd/DV and disturb late BAO fits",
            "status": "hazard_needs_dedicated_BAO_bridge",
        },
        {
            "observable": "growth",
            "endpoints": "perturbation evolution across unscreened cosmological history",
            "Delta_C": "path-dependent",
            "predicted_effect": "cannot be inferred from endpoint clock algebra only",
            "risk": "needs parent perturbation equations",
            "status": "not_closed",
        },
    ]


def local_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "constant local C",
            "equation": "partial_mu C = 0",
            "effect": "conformal connection shift vanishes locally",
            "residual_if_satisfied": "Delta Gamma^rho_munu = 0",
            "status": "local_GR_safe_at_algebra_level",
        },
        {
            "condition": "negligible local gradient",
            "equation": "Delta Gamma^rho_munu = 1/2(delta^rho_mu partial_nu C + delta^rho_nu partial_mu C - g_munu partial^rho C)",
            "effect": "PPN/fifth-force residual is gradient controlled",
            "residual_if_satisfied": "a_C roughly -grad(C)/2 is suppressed",
            "status": "requires_parent_screening_or_fixed_point",
        },
        {
            "condition": "negligible local drift",
            "equation": "d ln tilde_tau/dt = dot_C/2",
            "effect": "clock-drift residual is time-derivative controlled",
            "residual_if_satisfied": "local dot_C must be far smaller than unscreened cosmological drift",
            "status": "requires_local_silence_not_global_leakage",
        },
        {
            "condition": "environmental fixed point",
            "equation": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) -> 0",
            "effect": "local gradients and drift of C are pinned",
            "residual_if_satisfied": "PPN residual vector can vanish while cosmology keeps endpoint Delta C",
            "status": "needed_but_not_derived",
        },
        {
            "condition": "universal unscreened C",
            "equation": "C(t) with same dot_C in laboratories and cosmology",
            "effect": "late/CMB bridge may fit H0 but local clock silence fails",
            "residual_if_satisfied": "none; route rejected unless screened",
            "status": "rejected_as_parent_route",
        },
    ]


def residual_budget_rows(status_194: dict[str, Any]) -> list[dict[str, Any]]:
    required_dot_c_over_h = float(status_194["required_dot_C_over_H"])
    exp_error = float(status_194["exp_half_memory_error_H0"])
    return [
        {
            "budget": "H0 bridge residual",
            "value": exp_error,
            "unit_or_scale": "km/s/Mpc",
            "interpretation": "remaining mismatch after exp(-B_mem/2)",
            "status": "small_but_not_zero",
        },
        {
            "budget": "unscreened residual dot_C/H",
            "value": required_dot_c_over_h,
            "unit_or_scale": "dimensionless relative to H",
            "interpretation": "would repair the H0 residual if it were a cosmological derivative term",
            "status": "cannot_be_allowed_to_leak_locally_without_screening",
        },
        {
            "budget": "endpoint memory amplitude",
            "value": LOCKED_B_MEM,
            "unit_or_scale": "dimensionless",
            "interpretation": "required endpoint jump Delta C for the bridge",
            "status": "locked_not_parent_derived",
        },
        {
            "budget": "local PPN residual vector",
            "value": "",
            "unit_or_scale": "symbolic",
            "interpretation": "R_loc = {partial_i C, dot_C, delta stress from C perturbations}",
            "status": "must_be_derived_or_bounded_next",
        },
    ]


def domain_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "CMB sees endpoint memory jump",
            "evidence": "redshift/frequency endpoint map depends on C_obs-C_emit",
            "result": "partial_pass",
            "missing_piece": "parent derivation that C_rec~=0 and C_now~=B_mem for CMB calibration",
        },
        {
            "claim": "late local calibrators absorb common C",
            "evidence": "constant conformal factor cancels in same-frame dimensionless ratios",
            "result": "partial_pass",
            "missing_piece": "environmental/local fixed point and no host evolution",
        },
        {
            "claim": "BAO safely follows late branch",
            "evidence": "none from endpoint algebra alone; BAO uses an early drag ruler",
            "result": "fail_open",
            "missing_piece": "dedicated BAO ruler bridge and rd calibration audit",
        },
        {
            "claim": "local GR/PPN recovered",
            "evidence": "constant C gives zero connection shift",
            "result": "partial_pass",
            "missing_piece": "derive partial_mu C -> 0 and dot_C -> 0 locally from parent action",
        },
        {
            "claim": "not branch switching",
            "evidence": "single Delta_C endpoint rule classifies observables",
            "result": "partial_pass",
            "missing_piece": "derive endpoint assignments and screening mechanism",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal gate only",
        },
        {
            "gate": "endpoint Delta_C rule derived algebraically",
            "status": "pass",
            "evidence": "1+tilde_z = exp[(C_obs-C_emit)/2](1+z_g)",
            "claim_allowed": "domain-rule candidate",
        },
        {
            "gate": "late local common-mode cancellation",
            "status": "partial",
            "evidence": "works for constant/saturated C in same calibration frame",
            "claim_allowed": "conditional",
        },
        {
            "gate": "CMB endpoint bridge classified",
            "status": "partial",
            "evidence": "early-to-late Delta_C ~= B_mem gives exp(-B_mem/2) H0 map",
            "claim_allowed": "theorem target",
        },
        {
            "gate": "BAO/r_d safety",
            "status": "fail_open",
            "evidence": "BAO is early-late mixed; endpoint algebra alone is insufficient",
            "claim_allowed": "no",
        },
        {
            "gate": "local PPN silence parent-derived",
            "status": "fail",
            "evidence": "requires parent proof of partial_mu C -> 0 and dot_C -> 0 locally",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(status_194: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The late/CMB split can be organized by a single endpoint Delta_C rule: local late observables are common-mode if Delta_C is near zero, while CMB sees the early-to-late memory jump. But BAO/r_d and local PPN silence are not parent-derived.",
            "exp_half_memory_H0": status_194["exp_half_memory_H0"],
            "exp_half_memory_error_H0": status_194["exp_half_memory_error_H0"],
            "required_dot_C_over_H": status_194["required_dot_C_over_H"],
            "endpoint_rule_derived_algebraically": "true",
            "BAO_safety_closed": "false",
            "local_silence_parent_derived": "false",
            "next_target": "196-BAO-rd-endpoint-bridge-or-demotion.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_195_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    status_194 = load_json(CHECKPOINT_194_RUN / "status.json")
    source_rows = source_register_rows()
    endpoint_rows = endpoint_map_rows()
    observable_rows = observable_domain_rows()
    silence_rows = local_silence_rows()
    residual_rows = residual_budget_rows(status_194)
    scorecard_rows = domain_scorecard_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows(status_194)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "endpoint_memory_map_derivation.csv": (
            endpoint_rows,
            ["step", "object", "equation", "consequence", "status"],
        ),
        "observable_domain_classification.csv": (
            observable_rows,
            ["observable", "endpoints", "Delta_C", "predicted_effect", "risk", "status"],
        ),
        "local_silence_conditions.csv": (
            silence_rows,
            ["condition", "equation", "effect", "residual_if_satisfied", "status"],
        ),
        "residual_budget.csv": (
            residual_rows,
            ["budget", "value", "unit_or_scale", "interpretation", "status"],
        ),
        "domain_rule_scorecard.csv": (
            scorecard_rows,
            ["claim", "evidence", "result", "missing_piece"],
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
                "exp_half_memory_H0",
                "exp_half_memory_error_H0",
                "required_dot_C_over_H",
                "endpoint_rule_derived_algebraically",
                "BAO_safety_closed",
                "local_silence_parent_derived",
                "next_target",
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
        "endpoint_Delta_C_rule_derived_algebraically": True,
        "late_common_mode_cancellation_partial": True,
        "CMB_endpoint_bridge_partial": True,
        "BAO_rd_safety_closed": False,
        "local_silence_parent_derived": False,
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
