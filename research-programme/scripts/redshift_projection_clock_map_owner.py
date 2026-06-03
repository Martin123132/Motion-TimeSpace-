#!/usr/bin/env python3
"""Audit whether the BAO redshift projection can be owned by an MTS clock map."""

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
SCALAR_REMAP = PROJECTION_RESULTS / "scalar_redshift_remap_consistency.csv"
RADIAL_TRANSVERSE_FACTORS = PROJECTION_RESULTS / "radial_transverse_projection_factors.csv"
PROJECTION_STATUS = PROJECTION_RUN / "status.json"

HZ_RUN = RUNS_ROOT / "20260531-221500-fresh-CC-Hz-source-locked-holdout"
HZ_DECISION = HZ_RUN / "results" / "decision.csv"
HZ_GATES = HZ_RUN / "results" / "gate_results.csv"

B_MEM = 2.0 / 27.0
U3_FIT = 0.2429466120286312
U3_QUARTER = 0.25
CLAIM_CEILING = "redshift_clock_map_owner_not_promoted_no_BAO_CMB_support_claim"


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


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("10-"):
        return "local observer coframe and configuration-cell contract"
    if name.startswith("51-"):
        return "FLRW memory-current and activation contract"
    if name.startswith("53-"):
        return "coherent projection and local-silence gate"
    if name.startswith("54-"):
        return "coherent domain and u3 origin attempt"
    if name.startswith("145-") or "fresh-CC-Hz" in str(path):
        return "cosmic chronometer consistency pressure"
    if name.startswith("154-") or "anisotropic-BAO" in str(path):
        return "previous BAO projection target"
    if name.endswith(".py"):
        return "machine auditor"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "10-observer-map-symplectic-contract.md",
        WORK_DIR / "51-FLRW-memory-current-contract.md",
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md",
        WORK_DIR / "154-anisotropic-BAO-projection-owner-attempt.md",
        PROJECTION_STATUS,
        SCALAR_REMAP,
        RADIAL_TRANSVERSE_FACTORS,
        HZ_DECISION,
        HZ_GATES,
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


def sign(value: float, tolerance: float = 1.0e-12) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def activation_f(load_n: float, u3: float) -> float:
    if load_n <= 0.0:
        return 0.0
    x = load_n / u3
    return 1.0 - math.exp(-(x**3))


def activation_tail(load_n: float, u3: float) -> float:
    if load_n <= 0.0:
        return 1.0
    return math.exp(-((load_n / u3) ** 3))


def activation_current(load_n: float, u3: float) -> float:
    if load_n <= 0.0:
        return 0.0
    x = load_n / u3
    return (3.0 * load_n * load_n / (u3**3)) * math.exp(-(x**3))


def activation_curvature(load_n: float, u3: float) -> float:
    if load_n <= 0.0:
        return 0.0
    x = load_n / u3
    return ((6.0 * load_n / (u3**3)) - (9.0 * load_n**4 / (u3**6))) * math.exp(-(x**3))


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(vector)
    augmented = [row[:] + [rhs] for row, rhs in zip(matrix, vector, strict=True)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1.0e-18:
            raise ValueError("singular normal-equation matrix")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row_index in range(size):
            if row_index == column:
                continue
            factor = augmented[row_index][column]
            augmented[row_index] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row_index], augmented[column], strict=True)
            ]
    return [row[-1] for row in augmented]


def least_squares(design: list[list[float]], target: list[float]) -> list[float]:
    column_count = len(design[0])
    normal = [[0.0 for _ in range(column_count)] for _ in range(column_count)]
    rhs = [0.0 for _ in range(column_count)]
    for row, value in zip(design, target, strict=True):
        for i in range(column_count):
            rhs[i] += row[i] * value
            for j in range(column_count):
                normal[i][j] += row[i] * row[j]
    return solve_linear_system(normal, rhs)


def fit_single_shape(target: list[float], shape: list[float]) -> tuple[float, list[float]]:
    denominator = dot(shape, shape)
    coefficient = 0.0 if denominator == 0.0 else dot(target, shape) / denominator
    return coefficient, [coefficient * value for value in shape]


def fit_multi_shape(target: list[float], design: list[list[float]]) -> tuple[list[float], list[float]]:
    coefficients = least_squares(design, target)
    predictions = [sum(c * value for c, value in zip(coefficients, row, strict=True)) for row in design]
    return coefficients, predictions


def rms(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values) / len(values))


def max_abs(values: list[float]) -> float:
    return max(abs(value) for value in values)


def metric_row(
    candidate: str,
    target: list[float],
    predictions: list[float],
    coefficient_summary: str,
    parent_status: str,
    interpretation: str,
) -> dict[str, Any]:
    residuals = [actual - predicted for actual, predicted in zip(target, predictions, strict=True)]
    target_signs = [sign(value) for value in target]
    predicted_signs = [sign(value) for value in predictions]
    sign_matches = sum(1 for expected, actual in zip(target_signs, predicted_signs, strict=True) if expected == actual)
    has_predicted_crossing = min(predictions) < 0.0 < max(predictions)
    if sign_matches < len(target):
        status = "fail_sign_structure"
    elif rms(residuals) > 0.0015:
        status = "rough_fit_only"
    elif parent_status == "parent_owned":
        status = "pass"
    else:
        status = "fit_shape_but_unowned"
    return {
        "candidate": candidate,
        "coefficient_summary": coefficient_summary,
        "rms_theta_residual": rms(residuals),
        "max_abs_theta_residual": max_abs(residuals),
        "sign_matches": f"{sign_matches}/{len(target)}",
        "predicted_sign_crossing": "yes" if has_predicted_crossing else "no",
        "parent_status": parent_status,
        "status": status,
        "interpretation": interpretation,
    }


def target_rows(remap_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in remap_rows:
        z = float(row["z"])
        zeta = float(row["zeta_from_DM"])
        theta_required = -zeta / (1.0 + z)
        load_n = math.log1p(z)
        rows.append(
            {
                "z": z,
                "N_load_ln_1_plus_z": load_n,
                "zeta_required": zeta,
                "Theta_clock_required": theta_required,
                "abs_Theta_clock_required": abs(theta_required),
                "Theta_over_B_mem": theta_required / B_MEM,
                "zeta_over_B_mem": zeta / B_MEM,
                "target_sign": "positive" if theta_required > 0.0 else "negative",
                "Pi_parallel_required": float(row["Pi_parallel_required"]),
                "zeta_prime_needed_from_DH": float(row["zeta_prime_needed_from_DH"]),
                "zeta_prime_finite_difference_from_DM": float(row["zeta_prime_finite_difference_from_DM"]),
                "zeta_prime_mismatch": float(row["zeta_prime_mismatch"]),
            }
        )
    return rows


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "theta_0 = T c dt",
            "status": "available_contract",
            "meaning": "the observer coframe contains a clock/lapse factor",
            "blocker": "local contract was written for PPN, not yet for cosmological redshift calibration",
        },
        {
            "step": 2,
            "equation": "1+z_obs = (1+z_FLRW) exp(Theta_clock)",
            "status": "candidate_observer_map",
            "meaning": "a relative clock map can relabel measured photon redshift",
            "blocker": "a homogeneous universal lapse is gauge unless matter-clock coupling is specified",
        },
        {
            "step": 3,
            "equation": "zeta = z_true - z_obs = -(1+z_obs) Theta_clock + O(Theta_clock^2)",
            "status": "derived_linear_relation",
            "meaning": "the BAO scalar remap fixes the required clock-lapse target",
            "blocker": "sign convention must be checked in any parent action",
        },
        {
            "step": 4,
            "equation": "Theta_required(z) = -zeta(z)/(1+z)",
            "status": "machine_target",
            "meaning": "the previous BAO projection target becomes a direct clock-map target",
            "blocker": "target is not yet a theory prediction",
        },
        {
            "step": 5,
            "equation": "Theta_clock = B_mem C_clock[Q_coh,D]",
            "status": "theorem_target",
            "meaning": "zero-memory identity and local silence would follow if C_clock is parent-derived",
            "blocker": "C_clock is missing",
        },
        {
            "step": 6,
            "equation": "Q_coh^i_j = (1/u3) integral P_coh[Theta]^i_j d tau",
            "status": "available_conditional_route",
            "meaning": "coherent volume expansion supplies the existing memory activation channel",
            "blocker": "this channel is nonnegative/saturating on BAO redshifts and does not by itself give the signed target",
        },
    ]


def shape_comparison_rows(target: list[dict[str, Any]], u3: float, label: str) -> list[dict[str, Any]]:
    theta = [float(row["Theta_clock_required"]) for row in target]
    load_values = [float(row["N_load_ln_1_plus_z"]) for row in target]
    shapes: list[tuple[str, list[float], str, str]] = [
        (
            f"{label}_Bmem_times_F",
            [B_MEM * activation_f(load_n, u3) for load_n in load_values],
            "closure_owned_shape_only",
            "activation is nearly saturated and cannot naturally make the required sign change",
        ),
        (
            f"{label}_Bmem_times_tail_1_minus_F",
            [B_MEM * activation_tail(load_n, u3) for load_n in load_values],
            "closure_owned_shape_only",
            "unsaturated tail is positive and tiny at high redshift; it cannot own the high-z sign flip",
        ),
        (
            f"{label}_Bmem_times_dF_dN",
            [B_MEM * activation_current(load_n, u3) for load_n in load_values],
            "closure_owned_shape_only",
            "current kernel is single-signed on the target rows",
        ),
        (
            f"{label}_Bmem_times_d2F_dN2",
            [B_MEM * activation_curvature(load_n, u3) for load_n in load_values],
            "closure_owned_shape_only",
            "curvature kernel is not a derived clock observable and still fails the full target shape",
        ),
        (
            f"{label}_Bmem_times_N_over_u3",
            [B_MEM * load_n / u3 for load_n in load_values],
            "closure_owned_shape_only",
            "coherent load grows monotonically and does not supply the target crossing",
        ),
    ]
    rows = []
    for candidate, shape, parent_status, interpretation in shapes:
        coefficient, predictions = fit_single_shape(theta, shape)
        rows.append(
            metric_row(
                candidate=candidate,
                target=theta,
                predictions=predictions,
                coefficient_summary=f"single_scale={coefficient:.12g}",
                parent_status=parent_status,
                interpretation=interpretation,
            )
        )
    return rows


def closure_fit_rows(target: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theta = [float(row["Theta_clock_required"]) for row in target]
    load_values = [float(row["N_load_ln_1_plus_z"]) for row in target]

    affine_design = [[1.0, load_n] for load_n in load_values]
    affine_coefficients, affine_predictions = fit_multi_shape(theta, affine_design)
    affine_crossing = -affine_coefficients[0] / affine_coefficients[1] if affine_coefficients[1] != 0.0 else math.nan

    quadratic_design = [[1.0, load_n, load_n * load_n] for load_n in load_values]
    quadratic_coefficients, quadratic_predictions = fit_multi_shape(theta, quadratic_design)

    return [
        metric_row(
            candidate="affine_in_load_N_closure",
            target=theta,
            predictions=affine_predictions,
            coefficient_summary=(
                f"a={affine_coefficients[0]:.12g}; b={affine_coefficients[1]:.12g}; "
                f"N_cross={affine_crossing:.12g}"
            ),
            parent_status="not_parent_owned",
            interpretation="a smooth signed clock target is easy to fit, but the crossing scale is inserted by regression",
        ),
        metric_row(
            candidate="quadratic_in_load_N_closure",
            target=theta,
            predictions=quadratic_predictions,
            coefficient_summary=(
                f"a={quadratic_coefficients[0]:.12g}; b={quadratic_coefficients[1]:.12g}; "
                f"c={quadratic_coefficients[2]:.12g}"
            ),
            parent_status="not_parent_owned",
            interpretation="extra shape freedom fits better but is exactly the kind of redshift patch that needs a parent theorem",
        ),
    ]


def route_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "universal_homogeneous_lapse",
            "definition": "put Theta_clock into a homogeneous FLRW lapse only",
            "status": "rejected_as_owner_alone",
            "why": "a universal lapse can be time-coordinate gauge unless matter-clock coupling or observer calibration is nontrivial",
            "next_action": "do not claim physical redshift effect from lapse alone",
        },
        {
            "route": "relative_observer_coframe_clock_map",
            "definition": "derive 1+z_obs=(1+z_FLRW) exp(Theta_clock) from matter/clock coupling to theta_0",
            "status": "live_theorem_target",
            "why": "this is the cleanest way to make BAO anisotropic through redshift calibration rather than Q^nu",
            "next_action": "derive C_clock[Q_coh,D] and its sign from parent action",
        },
        {
            "route": "signed_domain_boundary_functional",
            "definition": "Theta_clock=B_mem C_clock[boundary/coherence evolution], with C_clock able to cross zero",
            "status": "live_but_unbuilt",
            "why": "target needs a sign-changing scalar while existing activation kernels are single-signed or saturated",
            "next_action": "construct or reject a boundary/coframe theorem for the sign change",
        },
        {
            "route": "ad_hoc_redshift_relabel",
            "definition": "fit zeta(z) directly against BAO rows",
            "status": "closure_only",
            "why": "it can improve BAO by construction but risks SN/H(z)/CMB and has no field-theory owner",
            "next_action": "use only as a diagnostic benchmark",
        },
        {
            "route": "Qnu_exchange_fallback",
            "definition": "let matter-memory exchange move the BAO bridge",
            "status": "deferred_high_risk",
            "why": "not yet forced, and it threatens local GR/growth unless tightly derived",
            "next_action": "return only if projection/clock theorem fails",
        },
    ]


def owner_contract_rows(max_theta: float, max_zeta: float, sign_crossing: bool) -> list[dict[str, Any]]:
    return [
        {
            "gate": "redshift_relation",
            "condition": "derive 1+z_obs=(1+z_FLRW) exp(Theta_clock) from observer/matter clock coupling",
            "status": "candidate_relation_written",
            "evidence": "linear map gives zeta=-(1+z)Theta_clock",
        },
        {
            "gate": "amplitude_small_enough",
            "condition": "required clock lapse must be perturbative",
            "status": "pass_target",
            "evidence": f"max |Theta_clock|={max_theta:.12g}; max |zeta|={max_zeta:.12g}",
        },
        {
            "gate": "signed_shape",
            "condition": "parent C_clock must reproduce target sign crossing if the BAO target is correct",
            "status": "required",
            "evidence": f"target sign crossing present={sign_crossing}",
        },
        {
            "gate": "zero_memory_identity",
            "condition": "B_mem -> 0 forces Theta_clock=zeta=0",
            "status": "not_derived",
            "evidence": "can be imposed as Theta=B_mem C_clock, but C_clock is missing",
        },
        {
            "gate": "single_activation_owner",
            "condition": "existing F, tail, dF/dN, d2F/dN2, or N/u3 shape predicts the clock map without extra redshift knobs",
            "status": "fail",
            "evidence": "single locked memory shapes do not own the sign-changing clock target",
        },
        {
            "gate": "local_silence",
            "condition": "Theta_clock vanishes in stationary/virialized bound domains",
            "status": "pass_conditional_not_parent_derived",
            "evidence": "coherent-domain rule gives a plausible silence route but no parent boundary theorem",
        },
        {
            "gate": "SN_Hz_retest",
            "condition": "same clock map must be applied to SN and source-locked H(z), not BAO only",
            "status": "open",
            "evidence": "fresh H(z) branch is a draw before projection; projection has not been retested",
        },
        {
            "gate": "bridge_promotion",
            "condition": "clock map is parent-derived and survives BAO/SN/H(z)/CMB/local checks",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def gate_rows(shape_rows: list[dict[str, Any]], closure_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    single_shape_successes = [row for row in shape_rows if row["status"] in {"pass", "fit_shape_but_unowned"}]
    closure_successes = [row for row in closure_rows if row["sign_matches"].startswith("6/")]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "all cited source artifacts exist",
        },
        {
            "gate": "clock_target_quantified",
            "status": "pass",
            "evidence": "zeta target translated into Theta_clock=-zeta/(1+z)",
        },
        {
            "gate": "locked_memory_shape_owner",
            "status": "fail",
            "evidence": f"single-shape pass-like rows={len(single_shape_successes)}; none are parent-derived clock observables",
        },
        {
            "gate": "smooth_closure_exists",
            "status": "pass_diagnostic_only",
            "evidence": f"closure rows matching all signs={len(closure_successes)}; regression fit is not a theorem",
        },
        {
            "gate": "observer_clock_parent_owner",
            "status": "fail_missing",
            "evidence": "no action/coframe theorem supplies the required signed C_clock",
        },
        {
            "gate": "projection_route_status",
            "status": "retained_conditional",
            "evidence": "clock amplitude is small and smooth enough to be a theorem target, but not claimable",
        },
    ]


def decision_rows(max_theta: float, max_zeta: float) -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "redshift_clock_map_target_quantified_not_parent_derived_projection_retained_conditional",
            "evidence": f"required clock lapse is small: max |Theta_clock|={max_theta:.12g}; max |zeta|={max_zeta:.12g}",
        },
        {
            "item": "main_result",
            "verdict": "single_locked_memory_activation_does_not_own_the_BAO_redshift_map",
            "evidence": "existing F/tail/current/load shapes are single-signed or saturated over BAO rows while target clock map changes sign",
        },
        {
            "item": "surviving_route",
            "verdict": "derive_signed_observer_coframe_or_domain_boundary_clock_functional",
            "evidence": "projection route remains live only if C_clock[Q_coh,D] is derived before data fitting",
        },
        {
            "item": "fallback",
            "verdict": "if_no_clock_functional_then_projection_is_closure_only_and_Qnu_or_full_Boltzmann_returns",
            "evidence": "affine/quadratic redshift fits are diagnostics, not field theory",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no BAO bridge promotion, no CMB support claim, no local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "156-clock-projection-functional-theorem-or-demotion.md",
            "evidence": "construct the signed C_clock theorem or demote the projection route to explicit closure",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-redshift-projection-clock-map-owner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    clock_targets = target_rows(read_csv_rows(SCALAR_REMAP))
    theta_values = [float(row["Theta_clock_required"]) for row in clock_targets]
    zeta_values = [float(row["zeta_required"]) for row in clock_targets]
    max_theta = max_abs(theta_values)
    max_zeta = max_abs(zeta_values)
    sign_crossing = min(theta_values) < 0.0 < max(theta_values)

    derivation_chain = derivation_chain_rows()
    shape_rows = shape_comparison_rows(clock_targets, U3_FIT, "u3_fit") + shape_comparison_rows(
        clock_targets, U3_QUARTER, "u3_quarter"
    )
    closure_rows = closure_fit_rows(clock_targets)
    route_rows = route_matrix_rows()
    contract_rows = owner_contract_rows(max_theta, max_zeta, sign_crossing)
    gates = gate_rows(shape_rows, closure_rows)
    decisions = decision_rows(max_theta, max_zeta)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "clock_redshift_target.csv",
        clock_targets,
        [
            "z",
            "N_load_ln_1_plus_z",
            "zeta_required",
            "Theta_clock_required",
            "abs_Theta_clock_required",
            "Theta_over_B_mem",
            "zeta_over_B_mem",
            "target_sign",
            "Pi_parallel_required",
            "zeta_prime_needed_from_DH",
            "zeta_prime_finite_difference_from_DM",
            "zeta_prime_mismatch",
        ],
    )
    write_csv(results_dir / "clock_map_derivation_chain.csv", derivation_chain, ["step", "equation", "status", "meaning", "blocker"])
    write_csv(
        results_dir / "locked_memory_shape_comparison.csv",
        shape_rows,
        [
            "candidate",
            "coefficient_summary",
            "rms_theta_residual",
            "max_abs_theta_residual",
            "sign_matches",
            "predicted_sign_crossing",
            "parent_status",
            "status",
            "interpretation",
        ],
    )
    write_csv(
        results_dir / "closure_fit_comparison.csv",
        closure_rows,
        [
            "candidate",
            "coefficient_summary",
            "rms_theta_residual",
            "max_abs_theta_residual",
            "sign_matches",
            "predicted_sign_crossing",
            "parent_status",
            "status",
            "interpretation",
        ],
    )
    write_csv(results_dir / "clock_owner_route_matrix.csv", route_rows, ["route", "definition", "status", "why", "next_action"])
    write_csv(results_dir / "owner_contract.csv", contract_rows, ["gate", "condition", "status", "evidence"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "B_mem": B_MEM,
        "u3_fit": U3_FIT,
        "u3_quarter": U3_QUARTER,
        "max_abs_theta_clock_required": max_theta,
        "max_abs_zeta_required": max_zeta,
        "target_clock_sign_crossing": sign_crossing,
        "generated": [
            "source_register.csv",
            "clock_redshift_target.csv",
            "clock_map_derivation_chain.csv",
            "locked_memory_shape_comparison.csv",
            "closure_fit_comparison.csv",
            "clock_owner_route_matrix.csv",
            "owner_contract.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "156-clock-projection-functional-theorem-or-demotion.md",
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
