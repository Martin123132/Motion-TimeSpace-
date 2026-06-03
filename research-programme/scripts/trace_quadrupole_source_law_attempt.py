#!/usr/bin/env python3
"""Test source-law candidates for the trace/quadrupole BAO ruler tensor."""

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

TENSOR_RUN = RUNS_ROOT / "20260531-235959-ruler-projection-parent-tensor-attempt"
TENSOR_RESULTS = TENSOR_RUN / "results"
DECOMPOSITION_CSV = TENSOR_RESULTS / "projection_target_decomposition.csv"

B_MEM = 2.0 / 27.0
U3_QUARTER = 0.25
U3_FIT = 0.2429466120286312
TRACE_FIXED_COEFF = B_MEM / 4.0
QUAD_FIXED_COEFF = B_MEM / 6.0
CLAIM_CEILING = "trace_quadrupole_source_law_attempt_no_bridge_promotion"
STATUS = "trace_law_strong_quadrupole_law_rough_parent_derivation_missing"


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


def max_abs(values: list[float]) -> float:
    return max(abs(value) for value in values)


def sign(value: float, tolerance: float = 1.0e-12) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def fit_single_scale(target: list[float], shape: list[float]) -> float:
    denominator = sum(value * value for value in shape)
    if denominator == 0.0:
        return 0.0
    return sum(actual * basis for actual, basis in zip(target, shape, strict=True)) / denominator


def activation_f(load_n: float, u3: float) -> float:
    if load_n <= 0.0:
        return 0.0
    return 1.0 - math.exp(-((load_n / u3) ** 3))


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("161-") or name.endswith("trace_quadrupole_source_law_attempt.py"):
        return "current trace/quadrupole source-law attempt"
    if name.startswith("160-") or "ruler-projection-parent-tensor-attempt" in str(path):
        return "parent tensor decomposition source"
    if name.startswith("159-"):
        return "ruler-only no-smuggling contract"
    if name.startswith("156-"):
        return "cell-balanced clock/source-law precedent"
    if name.startswith("53-") or name.startswith("54-"):
        return "coherent-domain/local-silence source"
    if name.startswith("51-"):
        return "FLRW memory-current source"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "51-FLRW-memory-current-contract.md",
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "156-clock-projection-functional-theorem-or-demotion.md",
        WORK_DIR / "159-ruler-only-projection-theorem-contract.md",
        WORK_DIR / "160-ruler-projection-parent-tensor-attempt.md",
        TENSOR_RUN / "status.json",
        DECOMPOSITION_CSV,
        TENSOR_RESULTS / "single_scalar_restriction_tests.csv",
        TENSOR_RESULTS / "source_law_targets.csv",
        TENSOR_RESULTS / "gate_results.csv",
        TENSOR_RESULTS / "decision.csv",
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


def target_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv_rows(DECOMPOSITION_CSV):
        z = float(row["z"])
        load_n = math.log1p(z)
        rows.append(
            {
                "z": z,
                "N_load_ln_1_plus_z": load_n,
                "Pi_perp_required": float(row["Pi_perp_required"]),
                "Pi_parallel_required": float(row["Pi_parallel_required"]),
                "T_trace_required": float(row["T_trace"]),
                "S_quadrupole_required": float(row["S_quadrupole"]),
            }
        )
    return rows


def trace_shape(name: str, load_n: float) -> float:
    endpoint_balance = 1.0 - 2.0 * math.exp(-load_n)
    if name == "endpoint_balance_no_activation":
        return endpoint_balance
    if name == "endpoint_balance_F_quarter":
        return activation_f(load_n, U3_QUARTER) * endpoint_balance
    if name == "endpoint_balance_F_fit":
        return activation_f(load_n, U3_FIT) * endpoint_balance
    if name == "linear_ln2_crossing":
        return load_n - math.log(2.0)
    raise ValueError(f"unknown trace shape {name}")


def quadrupole_shape(name: str, load_n: float) -> float:
    pair_saturation = 1.0 - math.exp(-2.0 * load_n)
    if name == "pair_saturation_two_endpoint":
        return pair_saturation
    if name == "pair_saturation_two_endpoint_F_quarter":
        return activation_f(load_n, U3_QUARTER) * pair_saturation
    if name == "pair_saturation_two_endpoint_F_fit":
        return activation_f(load_n, U3_FIT) * pair_saturation
    if name == "determinant_activation_only":
        return activation_f(load_n, U3_QUARTER)
    if name == "one_endpoint_saturation":
        return 1.0 - math.exp(-load_n)
    if name == "three_endpoint_saturation":
        return 1.0 - math.exp(-3.0 * load_n)
    raise ValueError(f"unknown quadrupole shape {name}")


def score_trace_candidates(targets: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    target = [float(row["T_trace_required"]) for row in targets]
    candidates = [
        {
            "candidate": "T_endpoint_balance_F_quarter_fixed_B_over_4",
            "shape_name": "endpoint_balance_F_quarter",
            "coefficient": TRACE_FIXED_COEFF,
            "coefficient_status": "fixed_B_mem_over_4",
            "zero_memory_status": "pass",
            "interpretation": "determinant-gated two-endpoint trace balance; strongest source-law clue",
        },
        {
            "candidate": "T_endpoint_balance_F_quarter_fitted_amplitude",
            "shape_name": "endpoint_balance_F_quarter",
            "coefficient": None,
            "coefficient_status": "diagnostic_fit_only",
            "zero_memory_status": "pass",
            "interpretation": "tests closeness of preferred trace amplitude to B_mem/4",
        },
        {
            "candidate": "T_endpoint_balance_no_activation_fixed_B_over_4",
            "shape_name": "endpoint_balance_no_activation",
            "coefficient": TRACE_FIXED_COEFF,
            "coefficient_status": "fixed_B_mem_over_4",
            "zero_memory_status": "fail_N0_nonzero",
            "interpretation": "row match is good, but zero-memory identity fails without F_D",
        },
        {
            "candidate": "T_endpoint_balance_F_fit_fixed_B_over_4",
            "shape_name": "endpoint_balance_F_fit",
            "coefficient": TRACE_FIXED_COEFF,
            "coefficient_status": "fixed_B_mem_over_4_borrowed_u3_fit",
            "zero_memory_status": "pass",
            "interpretation": "same trace law with fitted u3 activation; should not be preferred if quarter works",
        },
        {
            "candidate": "T_linear_ln2_crossing_fitted_amplitude",
            "shape_name": "linear_ln2_crossing",
            "coefficient": None,
            "coefficient_status": "diagnostic_fit_only",
            "zero_memory_status": "fail_N0_nonzero",
            "interpretation": "tests whether only a crossing location is being fit; fails zero-memory and is rougher",
        },
    ]
    score_rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []
    for candidate in candidates:
        shape = [trace_shape(str(candidate["shape_name"]), float(row["N_load_ln_1_plus_z"])) for row in targets]
        fitted_coeff = fit_single_scale(target, shape)
        coefficient = fitted_coeff if candidate["coefficient"] is None else float(candidate["coefficient"])
        predictions = [coefficient * value for value in shape]
        residuals = [actual - predicted for actual, predicted in zip(target, predictions, strict=True)]
        sign_matches = sum(1 for actual, predicted in zip(target, predictions, strict=True) if sign(actual) == sign(predicted))
        fixed_delta = (fitted_coeff - TRACE_FIXED_COEFF) / TRACE_FIXED_COEFF
        if sign_matches == len(target) and rms(residuals) < 3.0e-4 and candidate["zero_memory_status"] == "pass":
            status = "strong_theorem_target_not_parent_derived"
        elif candidate["zero_memory_status"] != "pass":
            status = "row_match_but_zero_memory_fail"
        elif sign_matches == len(target):
            status = "rough_theorem_target_not_parent_derived"
        else:
            status = "fail_shape"
        score_rows.append(
            {
                "sector": "trace",
                "candidate": candidate["candidate"],
                "formula": trace_formula(str(candidate["shape_name"]), coefficient),
                "coefficient": coefficient,
                "fitted_coefficient": fitted_coeff,
                "fixed_reference": TRACE_FIXED_COEFF,
                "fractional_delta_from_reference": fixed_delta,
                "rms_residual": rms(residuals),
                "max_abs_residual": max_abs(residuals),
                "sign_matches": f"{sign_matches}/{len(target)}",
                "zero_memory_status": candidate["zero_memory_status"],
                "coefficient_status": candidate["coefficient_status"],
                "status": status,
                "interpretation": candidate["interpretation"],
            }
        )
        for source, prediction, residual in zip(targets, predictions, residuals, strict=True):
            prediction_rows.append(
                {
                    "sector": "trace",
                    "candidate": candidate["candidate"],
                    "z": source["z"],
                    "N_load_ln_1_plus_z": source["N_load_ln_1_plus_z"],
                    "target": source["T_trace_required"],
                    "prediction": prediction,
                    "residual": residual,
                    "coefficient": coefficient,
                }
            )
    return score_rows, prediction_rows


def score_quadrupole_candidates(targets: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    target = [float(row["S_quadrupole_required"]) for row in targets]
    candidates = [
        {
            "candidate": "S_pair_saturation_fixed_B_over_6",
            "shape_name": "pair_saturation_two_endpoint",
            "coefficient": QUAD_FIXED_COEFF,
            "coefficient_status": "fixed_B_mem_over_6",
            "zero_memory_status": "pass",
            "interpretation": "two-endpoint radial/screen saturation; rough but structural",
        },
        {
            "candidate": "S_pair_saturation_fitted_amplitude",
            "shape_name": "pair_saturation_two_endpoint",
            "coefficient": None,
            "coefficient_status": "diagnostic_fit_only",
            "zero_memory_status": "pass",
            "interpretation": "tests how far the quadrupole amplitude wants to move from B_mem/6",
        },
        {
            "candidate": "S_pair_saturation_F_quarter_fixed_B_over_6",
            "shape_name": "pair_saturation_two_endpoint_F_quarter",
            "coefficient": QUAD_FIXED_COEFF,
            "coefficient_status": "fixed_B_mem_over_6",
            "zero_memory_status": "pass",
            "interpretation": "adds determinant activation to the quadrupole; similar row score",
        },
        {
            "candidate": "S_determinant_activation_only_fixed_B_over_6",
            "shape_name": "determinant_activation_only",
            "coefficient": QUAD_FIXED_COEFF,
            "coefficient_status": "fixed_B_mem_over_6",
            "zero_memory_status": "pass",
            "interpretation": "tests whether saturated memory alone can be the quadrupole source",
        },
        {
            "candidate": "S_one_endpoint_saturation_fitted_amplitude",
            "shape_name": "one_endpoint_saturation",
            "coefficient": None,
            "coefficient_status": "diagnostic_fit_only",
            "zero_memory_status": "pass",
            "interpretation": "one-endpoint alternative; less structural for a two-point ruler",
        },
        {
            "candidate": "S_three_endpoint_saturation_fixed_B_over_6",
            "shape_name": "three_endpoint_saturation",
            "coefficient": QUAD_FIXED_COEFF,
            "coefficient_status": "fixed_B_mem_over_6",
            "zero_memory_status": "pass",
            "interpretation": "three-spatial-direction saturation check; overshoots low-z",
        },
    ]
    score_rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []
    for candidate in candidates:
        shape = [quadrupole_shape(str(candidate["shape_name"]), float(row["N_load_ln_1_plus_z"])) for row in targets]
        fitted_coeff = fit_single_scale(target, shape)
        coefficient = fitted_coeff if candidate["coefficient"] is None else float(candidate["coefficient"])
        predictions = [coefficient * value for value in shape]
        residuals = [actual - predicted for actual, predicted in zip(target, predictions, strict=True)]
        sign_matches = sum(1 for actual, predicted in zip(target, predictions, strict=True) if sign(actual) == sign(predicted))
        fixed_delta = (fitted_coeff - QUAD_FIXED_COEFF) / QUAD_FIXED_COEFF
        if sign_matches == len(target) and rms(residuals) < 7.0e-4 and candidate["zero_memory_status"] == "pass":
            status = "viable_theorem_target_amplitude_not_locked"
        elif sign_matches == len(target) and candidate["zero_memory_status"] == "pass":
            status = "rough_theorem_target_not_parent_derived"
        else:
            status = "fail_shape"
        score_rows.append(
            {
                "sector": "quadrupole",
                "candidate": candidate["candidate"],
                "formula": quadrupole_formula(str(candidate["shape_name"]), coefficient),
                "coefficient": coefficient,
                "fitted_coefficient": fitted_coeff,
                "fixed_reference": QUAD_FIXED_COEFF,
                "fractional_delta_from_reference": fixed_delta,
                "rms_residual": rms(residuals),
                "max_abs_residual": max_abs(residuals),
                "sign_matches": f"{sign_matches}/{len(target)}",
                "zero_memory_status": candidate["zero_memory_status"],
                "coefficient_status": candidate["coefficient_status"],
                "status": status,
                "interpretation": candidate["interpretation"],
            }
        )
        for source, prediction, residual in zip(targets, predictions, residuals, strict=True):
            prediction_rows.append(
                {
                    "sector": "quadrupole",
                    "candidate": candidate["candidate"],
                    "z": source["z"],
                    "N_load_ln_1_plus_z": source["N_load_ln_1_plus_z"],
                    "target": source["S_quadrupole_required"],
                    "prediction": prediction,
                    "residual": residual,
                    "coefficient": coefficient,
                }
            )
    return score_rows, prediction_rows


def trace_formula(shape_name: str, coefficient: float) -> str:
    coeff = f"{coefficient:.16g}"
    if shape_name == "endpoint_balance_no_activation":
        return f"T_D={coeff}*(1-2 exp(-N))"
    if shape_name == "endpoint_balance_F_quarter":
        return f"T_D={coeff}*F_D(N,u3=1/4)*(1-2 exp(-N))"
    if shape_name == "endpoint_balance_F_fit":
        return f"T_D={coeff}*F_D(N,u3_fit)*(1-2 exp(-N))"
    if shape_name == "linear_ln2_crossing":
        return f"T_D={coeff}*(N-ln2)"
    raise ValueError(f"unknown trace shape {shape_name}")


def quadrupole_formula(shape_name: str, coefficient: float) -> str:
    coeff = f"{coefficient:.16g}"
    if shape_name == "pair_saturation_two_endpoint":
        return f"S_D={coeff}*(1-exp(-2N))"
    if shape_name == "pair_saturation_two_endpoint_F_quarter":
        return f"S_D={coeff}*F_D(N,u3=1/4)*(1-exp(-2N))"
    if shape_name == "pair_saturation_two_endpoint_F_fit":
        return f"S_D={coeff}*F_D(N,u3_fit)*(1-exp(-2N))"
    if shape_name == "determinant_activation_only":
        return f"S_D={coeff}*F_D(N,u3=1/4)"
    if shape_name == "one_endpoint_saturation":
        return f"S_D={coeff}*(1-exp(-N))"
    if shape_name == "three_endpoint_saturation":
        return f"S_D={coeff}*(1-exp(-3N))"
    raise ValueError(f"unknown quadrupole shape {shape_name}")


def combined_projection_scorecard(
    targets: list[dict[str, Any]],
    trace_scores: list[dict[str, Any]],
    quadrupole_scores: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    score_by_candidate = {row["candidate"]: row for row in trace_scores + quadrupole_scores}
    combos = [
        {
            "candidate": "fixed_endpoint_trace_plus_fixed_pair_quadrupole",
            "trace_candidate": "T_endpoint_balance_F_quarter_fixed_B_over_4",
            "quadrupole_candidate": "S_pair_saturation_fixed_B_over_6",
            "status_hint": "best_fixed_theorem_target_not_parent_derived",
        },
        {
            "candidate": "fixed_endpoint_trace_plus_fitted_pair_quadrupole",
            "trace_candidate": "T_endpoint_balance_F_quarter_fixed_B_over_4",
            "quadrupole_candidate": "S_pair_saturation_fitted_amplitude",
            "status_hint": "diagnostic_amplitude_fit_not_theorem",
        },
        {
            "candidate": "fitted_endpoint_trace_plus_fitted_pair_quadrupole",
            "trace_candidate": "T_endpoint_balance_F_quarter_fitted_amplitude",
            "quadrupole_candidate": "S_pair_saturation_fitted_amplitude",
            "status_hint": "diagnostic_fit_only",
        },
    ]
    score_rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []
    for combo in combos:
        trace_coeff = float(score_by_candidate[str(combo["trace_candidate"])]["coefficient"])
        quad_coeff = float(score_by_candidate[str(combo["quadrupole_candidate"])]["coefficient"])
        if str(combo["trace_candidate"]).startswith("T_endpoint_balance_F_quarter"):
            trace_shape_name = "endpoint_balance_F_quarter"
        else:
            raise ValueError("unexpected trace candidate")
        if str(combo["quadrupole_candidate"]).startswith("S_pair_saturation"):
            quad_shape_name = "pair_saturation_two_endpoint"
        else:
            raise ValueError("unexpected quadrupole candidate")
        perp_residuals: list[float] = []
        parallel_residuals: list[float] = []
        all_residuals: list[float] = []
        sign_matches = 0
        total_signs = 0
        for source in targets:
            load_n = float(source["N_load_ln_1_plus_z"])
            trace = trace_coeff * trace_shape(trace_shape_name, load_n)
            quad = quad_coeff * quadrupole_shape(quad_shape_name, load_n)
            pi_perp = trace - quad / 3.0
            pi_parallel = trace + 2.0 * quad / 3.0
            perp_residual = float(source["Pi_perp_required"]) - pi_perp
            parallel_residual = float(source["Pi_parallel_required"]) - pi_parallel
            perp_residuals.append(perp_residual)
            parallel_residuals.append(parallel_residual)
            all_residuals.extend([perp_residual, parallel_residual])
            for actual, predicted in [(float(source["Pi_perp_required"]), pi_perp), (float(source["Pi_parallel_required"]), pi_parallel)]:
                total_signs += 1
                if sign(actual) == sign(predicted):
                    sign_matches += 1
            prediction_rows.append(
                {
                    "candidate": combo["candidate"],
                    "z": source["z"],
                    "N_load_ln_1_plus_z": load_n,
                    "Pi_perp_required": source["Pi_perp_required"],
                    "Pi_perp_predicted": pi_perp,
                    "Pi_perp_residual": perp_residual,
                    "Pi_parallel_required": source["Pi_parallel_required"],
                    "Pi_parallel_predicted": pi_parallel,
                    "Pi_parallel_residual": parallel_residual,
                    "T_trace_predicted": trace,
                    "S_quadrupole_predicted": quad,
                }
            )
        if combo["status_hint"] == "best_fixed_theorem_target_not_parent_derived" and rms(all_residuals) < 8.0e-4:
            status = "fixed_law_competitive_theorem_target_not_parent_derived"
        else:
            status = str(combo["status_hint"])
        score_rows.append(
            {
                "candidate": combo["candidate"],
                "trace_candidate": combo["trace_candidate"],
                "quadrupole_candidate": combo["quadrupole_candidate"],
                "rms_Pi_perp_residual": rms(perp_residuals),
                "rms_Pi_parallel_residual": rms(parallel_residuals),
                "rms_all_projection_residual": rms(all_residuals),
                "max_abs_projection_residual": max_abs(all_residuals),
                "sign_matches": f"{sign_matches}/{total_signs}",
                "status": status,
                "interpretation": "reconstructs Pi_perp=T-S/3 and Pi_parallel=T+2S/3 from source-law candidates",
            }
        )
    return score_rows, prediction_rows


def equation_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "coherent load",
            "symbol": "N",
            "candidate_equation": "N=ln(1+z) as FLRW coherent expansion load, not a fitted redshift remap",
            "status": "borrowed_from_background_branch",
            "required_derivation": "derive the two-point ruler load from the parent observer/coframe map",
        },
        {
            "object": "memory activation",
            "symbol": "F_D",
            "candidate_equation": "F_D=1-exp[-(N/u3)^3], with u3=1/4 for the structural branch",
            "status": "conditional_prior_theorem_target",
            "required_derivation": "derive determinant activation and u3=1/4 from parent cell/current rule",
        },
        {
            "object": "trace source",
            "symbol": "T_D",
            "candidate_equation": "T_D=(B_mem/4) F_D (1-2 exp(-N))",
            "status": "strong_row_match_theorem_target",
            "required_derivation": "derive endpoint-balance factor and four-cell amplitude before BAO fitting",
        },
        {
            "object": "quadrupole source",
            "symbol": "S_D",
            "candidate_equation": "S_D=(B_mem/6)(1-exp(-2N))",
            "status": "rough_row_match_theorem_target",
            "required_derivation": "derive two-endpoint radial/screen saturation and six-orientation amplitude",
        },
        {
            "object": "ruler tensor",
            "symbol": "R^A_B",
            "candidate_equation": "R^A_B=delta^A_B+T_D h^A_B+S_D(n^A n_B-h^A_B/3)",
            "status": "algebraic_parent_tensor_with_candidate_sources",
            "required_derivation": "derive why this operator acts on pair separations rather than one-point luminosity distance",
        },
        {
            "object": "SN/H(z) null response",
            "symbol": "delta D_L_SN=0, delta H_CC=0 at leading order",
            "candidate_equation": "projection is a two-point ruler transport, not delta g_mu_nu",
            "status": "still_missing",
            "required_derivation": "prove pair-vs-one-point split from action/operator structure",
        },
    ]


def gate_rows(
    trace_scores: list[dict[str, Any]],
    quadrupole_scores: list[dict[str, Any]],
    combined_scores: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    trace_fixed = next(row for row in trace_scores if row["candidate"] == "T_endpoint_balance_F_quarter_fixed_B_over_4")
    trace_no_activation = next(row for row in trace_scores if row["candidate"] == "T_endpoint_balance_no_activation_fixed_B_over_4")
    quad_fixed = next(row for row in quadrupole_scores if row["candidate"] == "S_pair_saturation_fixed_B_over_6")
    quad_fit = next(row for row in quadrupole_scores if row["candidate"] == "S_pair_saturation_fitted_amplitude")
    combined_fixed = next(row for row in combined_scores if row["candidate"] == "fixed_endpoint_trace_plus_fixed_pair_quadrupole")
    return [
        {
            "gate": "source_paths",
            "status": "pass",
            "evidence": "all required source paths exist",
        },
        {
            "gate": "trace_source_law",
            "status": "strong_theorem_target_not_derived",
            "evidence": f"fixed trace rms={trace_fixed['rms_residual']}; max={trace_fixed['max_abs_residual']}; signs={trace_fixed['sign_matches']}",
        },
        {
            "gate": "trace_zero_memory",
            "status": "pass_with_F_D",
            "evidence": f"ungated endpoint balance status={trace_no_activation['status']}; F_D-gated law restores N=0 identity",
        },
        {
            "gate": "quadrupole_source_law",
            "status": "rough_theorem_target_amplitude_open",
            "evidence": f"fixed quadrupole rms={quad_fixed['rms_residual']}; fitted amplitude delta={quad_fit['fractional_delta_from_reference']}",
        },
        {
            "gate": "combined_projection",
            "status": "competitive_theorem_target_not_exact",
            "evidence": f"fixed combined rms_all={combined_fixed['rms_all_projection_residual']}; max={combined_fixed['max_abs_projection_residual']}; signs={combined_fixed['sign_matches']}",
        },
        {
            "gate": "pre_data_lock",
            "status": "fail_open",
            "evidence": "the formulas were identified after the 154/160 BAO decomposition and must be rederived independently",
        },
        {
            "gate": "SN_Hz_immunity",
            "status": "fail_open",
            "evidence": "pair-ruler versus one-point null theorem remains missing",
        },
        {
            "gate": "parent_action_derivation",
            "status": "fail_open",
            "evidence": "no action variation or conservation identity derives the endpoint-balance and pair-saturation factors",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(
    trace_scores: list[dict[str, Any]],
    quadrupole_scores: list[dict[str, Any]],
    combined_scores: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    trace_fixed = next(row for row in trace_scores if row["candidate"] == "T_endpoint_balance_F_quarter_fixed_B_over_4")
    quad_fixed = next(row for row in quadrupole_scores if row["candidate"] == "S_pair_saturation_fixed_B_over_6")
    combined_fixed = next(row for row in combined_scores if row["candidate"] == "fixed_endpoint_trace_plus_fixed_pair_quadrupole")
    return [
        {
            "item": "status",
            "verdict": STATUS,
            "evidence": "trace source law is strong; quadrupole law is plausible but rough; parent derivation and SN/H(z) immunity missing",
        },
        {
            "item": "trace_candidate",
            "verdict": "T_D=(B_mem/4) F_D(N,u3=1/4)(1-2e^{-N})",
            "evidence": f"rms={trace_fixed['rms_residual']}; max={trace_fixed['max_abs_residual']}; fitted coefficient within {trace_fixed['fractional_delta_from_reference']} of B_mem/4",
        },
        {
            "item": "quadrupole_candidate",
            "verdict": "S_D=(B_mem/6)(1-e^{-2N})",
            "evidence": f"rms={quad_fixed['rms_residual']}; max={quad_fixed['max_abs_residual']}; fitted coefficient delta={quad_fixed['fractional_delta_from_reference']}",
        },
        {
            "item": "combined_projection_candidate",
            "verdict": "fixed trace plus fixed quadrupole reconstructs percent-level BAO tensor roughly",
            "evidence": f"rms_all={combined_fixed['rms_all_projection_residual']}; max={combined_fixed['max_abs_projection_residual']}; signs={combined_fixed['sign_matches']}",
        },
        {
            "item": "not_yet_derived",
            "verdict": "endpoint balance, pair saturation, and one-point immunity are theorem targets",
            "evidence": "current formulas are disciplined candidate source laws, not action-derived identities",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no bridge promotion, no CMB claim, no local-GR claim",
        },
        {
            "item": "next_target",
            "verdict": "162-pair-ruler-operator-null-response-contract.md",
            "evidence": "derive why the operator acts on BAO pair separations while SN/H(z) remain null, or demote to closure",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-trace-quadrupole-source-law-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    targets = target_rows()
    trace_scores, trace_predictions = score_trace_candidates(targets)
    quadrupole_scores, quadrupole_predictions = score_quadrupole_candidates(targets)
    combined_scores, combined_predictions = combined_projection_scorecard(targets, trace_scores, quadrupole_scores)
    equations = equation_contract_rows()
    gates = gate_rows(trace_scores, quadrupole_scores, combined_scores)
    decisions = decision_rows(trace_scores, quadrupole_scores, combined_scores)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "source_law_scorecard.csv",
        trace_scores + quadrupole_scores,
        [
            "sector",
            "candidate",
            "formula",
            "coefficient",
            "fitted_coefficient",
            "fixed_reference",
            "fractional_delta_from_reference",
            "rms_residual",
            "max_abs_residual",
            "sign_matches",
            "zero_memory_status",
            "coefficient_status",
            "status",
            "interpretation",
        ],
    )
    write_csv(
        results_dir / "source_law_predictions.csv",
        trace_predictions + quadrupole_predictions,
        ["sector", "candidate", "z", "N_load_ln_1_plus_z", "target", "prediction", "residual", "coefficient"],
    )
    write_csv(
        results_dir / "combined_projection_scorecard.csv",
        combined_scores,
        [
            "candidate",
            "trace_candidate",
            "quadrupole_candidate",
            "rms_Pi_perp_residual",
            "rms_Pi_parallel_residual",
            "rms_all_projection_residual",
            "max_abs_projection_residual",
            "sign_matches",
            "status",
            "interpretation",
        ],
    )
    write_csv(
        results_dir / "combined_projection_predictions.csv",
        combined_predictions,
        [
            "candidate",
            "z",
            "N_load_ln_1_plus_z",
            "Pi_perp_required",
            "Pi_perp_predicted",
            "Pi_perp_residual",
            "Pi_parallel_required",
            "Pi_parallel_predicted",
            "Pi_parallel_residual",
            "T_trace_predicted",
            "S_quadrupole_predicted",
        ],
    )
    write_csv(
        results_dir / "equation_contract.csv",
        equations,
        ["object", "symbol", "candidate_equation", "status", "required_derivation"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    trace_fixed = next(row for row in trace_scores if row["candidate"] == "T_endpoint_balance_F_quarter_fixed_B_over_4")
    quad_fixed = next(row for row in quadrupole_scores if row["candidate"] == "S_pair_saturation_fixed_B_over_6")
    combined_fixed = next(row for row in combined_scores if row["candidate"] == "fixed_endpoint_trace_plus_fixed_pair_quadrupole")
    status = {
        "status": STATUS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "trace_candidate": "T_D=(B_mem/4) F_D(N,u3=1/4)(1-2e^{-N})",
        "quadrupole_candidate": "S_D=(B_mem/6)(1-e^{-2N})",
        "B_mem": B_MEM,
        "u3_quarter": U3_QUARTER,
        "trace_fixed_rms": float(trace_fixed["rms_residual"]),
        "trace_fixed_max_abs": float(trace_fixed["max_abs_residual"]),
        "quadrupole_fixed_rms": float(quad_fixed["rms_residual"]),
        "quadrupole_fixed_max_abs": float(quad_fixed["max_abs_residual"]),
        "combined_fixed_rms_all": float(combined_fixed["rms_all_projection_residual"]),
        "combined_fixed_max_abs": float(combined_fixed["max_abs_projection_residual"]),
        "generated": [
            "source_register.csv",
            "source_law_scorecard.csv",
            "source_law_predictions.csv",
            "combined_projection_scorecard.csv",
            "combined_projection_predictions.csv",
            "equation_contract.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "162-pair-ruler-operator-null-response-contract.md",
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
