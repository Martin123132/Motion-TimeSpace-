#!/usr/bin/env python3
"""Attempt a parent tensor for the ruler-only BAO projection route."""

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

PROJECTION_RUN = RUNS_ROOT / "20260531-235959-anisotropic-BAO-projection-owner-attempt"
PROJECTION_RESULTS = PROJECTION_RUN / "results"
RULER_CONTRACT_RUN = RUNS_ROOT / "20260531-235959-ruler-only-projection-theorem-contract"
RULER_CONTRACT_RESULTS = RULER_CONTRACT_RUN / "results"
FAILURE_RUN = RUNS_ROOT / "20260531-235959-cell-clock-failure-mode-audit"
FAILURE_RESULTS = FAILURE_RUN / "results"

PROJECTION_FACTORS = PROJECTION_RESULTS / "radial_transverse_projection_factors.csv"
CLAIM_CEILING = "ruler_parent_tensor_attempt_no_bridge_promotion"
STATUS = "ruler_parent_tensor_decomposition_found_source_law_missing"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rms(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values) / len(values))


def sign_label(value: float) -> str:
    if value > 0:
        return "positive"
    if value < 0:
        return "negative"
    return "zero"


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("160-") or name.endswith("ruler_projection_parent_tensor_attempt.py"):
        return "current parent-tensor attempt"
    if name.startswith("159-") or "ruler-only-projection-theorem-contract" in str(path):
        return "ruler-only no-smuggling contract"
    if name.startswith("154-") or "anisotropic-BAO-projection" in str(path):
        return "radial/transverse BAO target source"
    if name.startswith("158-") or "cell-clock-failure-mode" in str(path):
        return "global clock demotion and ruler-only motivation"
    if name.startswith("10-"):
        return "observer/coframe contract"
    if name.startswith("53-") or name.startswith("54-"):
        return "coherent domain and local-silence contract"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "10-observer-map-symplectic-contract.md",
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "154-anisotropic-BAO-projection-owner-attempt.md",
        WORK_DIR / "158-cell-clock-BAO-row-and-SN-Hz-failure-mode-audit.md",
        WORK_DIR / "159-ruler-only-projection-theorem-contract.md",
        PROJECTION_RUN / "status.json",
        PROJECTION_FACTORS,
        RULER_CONTRACT_RUN / "status.json",
        RULER_CONTRACT_RESULTS / "theorem_object_contract.csv",
        RULER_CONTRACT_RESULTS / "formula_contract.csv",
        RULER_CONTRACT_RESULTS / "gate_results.csv",
        FAILURE_RUN / "status.json",
        FAILURE_RESULTS / "ruler_only_projection_scores.csv",
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def projection_decomposition_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv_rows(PROJECTION_FACTORS):
        z = float(row["z"])
        pi_perp = float(row["Pi_perp_required"])
        pi_parallel = float(row["Pi_parallel_required"])
        trace_scalar = (2.0 * pi_perp + pi_parallel) / 3.0
        quadrupole_scalar = pi_parallel - pi_perp
        volume_trace = 2.0 * pi_perp + pi_parallel
        trace_free_residual = pi_parallel + 2.0 * pi_perp
        isotropic_residual = pi_parallel - pi_perp
        trace_free_pred_parallel = -2.0 * pi_perp
        isotropic_pred_parallel = pi_perp
        rows.append(
            {
                "z": z,
                "Pi_perp_required": pi_perp,
                "Pi_parallel_required": pi_parallel,
                "T_trace": trace_scalar,
                "S_quadrupole": quadrupole_scalar,
                "volume_trace_2perp_plus_parallel": volume_trace,
                "isotropic_residual_parallel_minus_perp": isotropic_residual,
                "tracefree_residual_parallel_plus_2perp": trace_free_residual,
                "isotropic_predicted_parallel": isotropic_pred_parallel,
                "tracefree_predicted_parallel": trace_free_pred_parallel,
                "radial_transverse_sign": row.get("radial_transverse_sign", ""),
                "T_sign": sign_label(trace_scalar),
                "S_sign": sign_label(quadrupole_scalar),
                "interpretation": "trace_plus_quadrupole_target",
            }
        )
    return rows


def scalar_restriction_tests(decomposition: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pi_perp = [float(row["Pi_perp_required"]) for row in decomposition]
    pi_parallel = [float(row["Pi_parallel_required"]) for row in decomposition]
    traces = [float(row["T_trace"]) for row in decomposition]
    quadrupoles = [float(row["S_quadrupole"]) for row in decomposition]
    isotropic_residuals = [parallel - perp for perp, parallel in zip(pi_perp, pi_parallel)]
    tracefree_residuals = [parallel + 2.0 * perp for perp, parallel in zip(pi_perp, pi_parallel)]
    opposed_signs = sum(1 for perp, parallel in zip(pi_perp, pi_parallel) if perp * parallel < 0)
    same_signs = len(pi_perp) - opposed_signs
    best_ratio = sum(perp * parallel for perp, parallel in zip(pi_perp, pi_parallel)) / sum(
        perp * perp for perp in pi_perp
    )
    best_ratio_residuals = [parallel - best_ratio * perp for perp, parallel in zip(pi_perp, pi_parallel)]
    nonzero_trace_ratio = [
        quadrupole / trace for trace, quadrupole in zip(traces, quadrupoles) if abs(trace) > 1.0e-6
    ]
    return [
        {
            "test": "pure_isotropic_scalar",
            "constraint": "Pi_parallel = Pi_perp",
            "status": "fail",
            "rms_residual": rms(isotropic_residuals),
            "max_abs_residual": max(abs(value) for value in isotropic_residuals),
            "evidence": f"opposed_sign_rows={opposed_signs}; same_sign_rows={same_signs}",
            "interpretation": "one isotropic scalar cannot supply the radial/transverse split",
        },
        {
            "test": "pure_tracefree_quadrupole",
            "constraint": "Pi_parallel = -2 Pi_perp",
            "status": "fail",
            "rms_residual": rms(tracefree_residuals),
            "max_abs_residual": max(abs(value) for value in tracefree_residuals),
            "evidence": "target has nonzero trace and endpoint same-sign rows",
            "interpretation": "a trace-free quadrupole is a useful component but not the full route",
        },
        {
            "test": "best_constant_ratio_single_scalar",
            "constraint": "Pi_parallel = k Pi_perp with one fitted k",
            "status": "fail",
            "rms_residual": rms(best_ratio_residuals),
            "max_abs_residual": max(abs(value) for value in best_ratio_residuals),
            "evidence": f"best_k={best_ratio}",
            "interpretation": "a one-scalar fixed-ratio tensor cannot handle the sign pattern",
        },
        {
            "test": "trace_plus_quadrupole_tensor",
            "constraint": "R = I + T h + S(n n - h/3)",
            "status": "algebraic_pass_source_laws_missing",
            "rms_residual": 0.0,
            "max_abs_residual": 0.0,
            "evidence": f"T_range=[{min(traces)}, {max(traces)}]; S_range=[{min(quadrupoles)}, {max(quadrupoles)}]",
            "interpretation": "one tensor can represent the BAO target, but T and S need a parent source law",
        },
        {
            "test": "single_scalar_plus_derivative_escape_hatch",
            "constraint": "T and S come from one pre-fixed transport scalar and its radial derivative",
            "status": "open_theorem_target",
            "rms_residual": "",
            "max_abs_residual": "",
            "evidence": f"S_over_T_not_constant_range=[{min(nonzero_trace_ratio)}, {max(nonzero_trace_ratio)}]",
            "interpretation": "possible only if the parent action fixes the scalar transport function before BAO scoring",
        },
    ]


def tensor_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "metric_deformation_tensor",
            "formula": "g_mu_nu -> g_mu_nu + delta g_mu_nu",
            "status": "rejected_for_ruler_only",
            "strength": "field-theory object exists in principle",
            "failure": "SN/H(z)/lensing/local clocks must inherit the deformation",
            "next_action": "do not use unless returning to a global model and re-facing SN penalties",
        },
        {
            "candidate": "isotropic_ruler_scalar",
            "formula": "R^A_B = delta^A_B + Xi_D h^A_B",
            "status": "rejected_as_complete_owner",
            "strength": "simple scalar, zero-memory limit easy",
            "failure": "forces Pi_parallel=Pi_perp and misses opposed-sign rows",
            "next_action": "can only appear as the trace part T_D",
        },
        {
            "candidate": "tracefree_screen_radial_quadrupole",
            "formula": "R^A_B = delta^A_B + S_D(n^A n_B - h^A_B/3)",
            "status": "rejected_as_complete_owner",
            "strength": "naturally separates radial and transverse BAO response",
            "failure": "forces 2 Pi_perp + Pi_parallel=0, but target has a sign-changing trace",
            "next_action": "retain as the quadrupole part S_D",
        },
        {
            "candidate": "trace_plus_quadrupole_ruler_transport",
            "formula": "R^A_B = delta^A_B + T_D h^A_B + S_D(n^A n_B - h^A_B/3)",
            "status": "best_algebraic_candidate_source_missing",
            "strength": "one tensor exactly decomposes the target into T_D and S_D",
            "failure": "parent action has not derived T_D(z), S_D(z), or SN immunity",
            "next_action": "derive trace and quadrupole source laws from coframe/domain-boundary transport",
        },
        {
            "candidate": "single_transport_scalar_with_derivative",
            "formula": "Pi_perp=Y_D; Pi_parallel=Y_D + radial derivative term",
            "status": "live_high_risk",
            "strength": "could reduce T_D and S_D to one pre-data scalar law",
            "failure": "if interpreted as global redshift/clock map, 157/158 SN failure returns",
            "next_action": "derive as two-point ruler-pair transport, not universal clock remap",
        },
        {
            "candidate": "survey_selection_or_bias_shift",
            "formula": "R inferred through tracer/window/systematics response",
            "status": "deferred",
            "strength": "BAO-specific effects are observationally plausible",
            "failure": "not a fundamental field-theory bridge unless parent-derived",
            "next_action": "use only as baseline/systematics audit, not MTS spine",
        },
    ]


def source_law_target_rows(decomposition: list[dict[str, Any]]) -> list[dict[str, Any]]:
    traces = [float(row["T_trace"]) for row in decomposition]
    quadrupoles = [float(row["S_quadrupole"]) for row in decomposition]
    return [
        {
            "target": "trace_ruler_strain",
            "symbol": "T_D(z)",
            "required_profile": f"sign-changing; range=[{min(traces)}, {max(traces)}]",
            "possible_owner": "cell-balanced scalar memory, late ruler calibration, or scalar transport average",
            "current_status": "not_derived",
            "must_prove": "zero-memory limit, CMB r_d safety, and no one-point SN luminosity coupling",
        },
        {
            "target": "screen_radial_quadrupole",
            "symbol": "S_D(z)",
            "required_profile": f"positive across target rows; range=[{min(quadrupoles)}, {max(quadrupoles)}]",
            "possible_owner": "radial derivative of two-point ruler transport or coherent boundary/coframe gradient",
            "current_status": "not_derived",
            "must_prove": "FLRW statistical isotropy is not broken; anisotropy is observational radial/screen response",
        },
        {
            "target": "BAO_pair_immunity_split",
            "symbol": "delta D_L_SN = 0 while delta ell_BAO != 0",
            "required_profile": "leading-order null response for one-point SN/H(z)",
            "possible_owner": "operator acts on pair separations or late-time ruler calibration only",
            "current_status": "not_derived",
            "must_prove": "not a metric, not a photon-geodesic remap, not a hand exemption",
        },
        {
            "target": "pre_data_shape_lock",
            "symbol": "T_D,S_D = functions[X_D,F_D,boundary/coframe invariants]",
            "required_profile": "fixed before DESI row scoring",
            "possible_owner": "parent action/coherence theorem",
            "current_status": "not_derived",
            "must_prove": "no row-wise DESI repair and no fitted projection polynomial",
        },
    ]


def gate_result_rows(restrictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    test_status = {row["test"]: row["status"] for row in restrictions}
    return [
        {
            "gate": "source_paths",
            "status": "pass",
            "evidence": "all required source paths exist",
        },
        {
            "gate": "tensor_decomposition",
            "status": "pass_algebraic",
            "evidence": "Pi_perp=T-S/3 and Pi_parallel=T+2S/3 with T=(2Pi_perp+Pi_parallel)/3 and S=Pi_parallel-Pi_perp",
        },
        {
            "gate": "pure_isotropic_scalar",
            "status": test_status["pure_isotropic_scalar"],
            "evidence": "Pi_parallel=Pi_perp fails the DESI target pattern",
        },
        {
            "gate": "pure_tracefree_quadrupole",
            "status": test_status["pure_tracefree_quadrupole"],
            "evidence": "Pi_parallel=-2Pi_perp fails because target has sign-changing trace",
        },
        {
            "gate": "one_parent_tensor",
            "status": "conditional_pass",
            "evidence": "trace-plus-quadrupole tensor is one object, but source laws are missing",
        },
        {
            "gate": "source_law_derivation",
            "status": "fail_open",
            "evidence": "T_D(z), S_D(z), or one scalar-plus-derivative transport law not parent-derived",
        },
        {
            "gate": "SN_Hz_immunity",
            "status": "fail_open",
            "evidence": "two-point BAO response versus one-point SN/H(z) null response remains theorem target",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": STATUS,
            "evidence": "a trace-plus-quadrupole parent tensor can represent the BAO target, but the parent source law is still missing",
        },
        {
            "item": "constructed_object",
            "verdict": "R^A_B = delta^A_B + T_D h^A_B + S_D(n^A n_B - h^A_B/3)",
            "evidence": "Pi_perp=T_D-S_D/3; Pi_parallel=T_D+2S_D/3",
        },
        {
            "item": "required_profiles",
            "verdict": "T_D sign-changing; S_D positive and slowly increasing over target rows",
            "evidence": "computed from 154 radial/transverse projection factors",
        },
        {
            "item": "rejected_complete_owners",
            "verdict": "pure isotropic scalar; pure trace-free quadrupole; metric/geodesic projection",
            "evidence": "scalar and trace-free restrictions fail; metric route violates 159 no-smuggling contract",
        },
        {
            "item": "best_live_route",
            "verdict": "two_point_screen_radial_ruler_transport_with_trace_and_derivative/quadrupole",
            "evidence": "can act on BAO pair separations if source law and SN immunity are derived",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no CMB bridge, no SN immunity theorem, no local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "161-trace-quadrupole-source-law-attempt.md",
            "evidence": "derive T_D and S_D from coherent-domain/coframe transport, or demote ruler route to closure-only",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-ruler-projection-parent-tensor-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    decomposition = projection_decomposition_rows()
    restrictions = scalar_restriction_tests(decomposition)
    candidates = tensor_candidate_rows()
    source_targets = source_law_target_rows(decomposition)
    gates = gate_result_rows(restrictions)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "projection_target_decomposition.csv",
        decomposition,
        [
            "z",
            "Pi_perp_required",
            "Pi_parallel_required",
            "T_trace",
            "S_quadrupole",
            "volume_trace_2perp_plus_parallel",
            "isotropic_residual_parallel_minus_perp",
            "tracefree_residual_parallel_plus_2perp",
            "isotropic_predicted_parallel",
            "tracefree_predicted_parallel",
            "radial_transverse_sign",
            "T_sign",
            "S_sign",
            "interpretation",
        ],
    )
    write_csv(
        results_dir / "single_scalar_restriction_tests.csv",
        restrictions,
        ["test", "constraint", "status", "rms_residual", "max_abs_residual", "evidence", "interpretation"],
    )
    write_csv(
        results_dir / "tensor_candidate_ledger.csv",
        candidates,
        ["candidate", "formula", "status", "strength", "failure", "next_action"],
    )
    write_csv(
        results_dir / "source_law_targets.csv",
        source_targets,
        ["target", "symbol", "required_profile", "possible_owner", "current_status", "must_prove"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    traces = [float(row["T_trace"]) for row in decomposition]
    quadrupoles = [float(row["S_quadrupole"]) for row in decomposition]
    status = {
        "status": STATUS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "T_trace_range": [min(traces), max(traces)],
        "S_quadrupole_range": [min(quadrupoles), max(quadrupoles)],
        "generated": [
            "source_register.csv",
            "projection_target_decomposition.csv",
            "single_scalar_restriction_tests.csv",
            "tensor_candidate_ledger.csv",
            "source_law_targets.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "161-trace-quadrupole-source-law-attempt.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_attempt(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
