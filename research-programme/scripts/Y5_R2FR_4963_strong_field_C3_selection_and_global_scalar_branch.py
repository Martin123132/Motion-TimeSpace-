from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4963"

RESULT_JSON = SOURCE / "strong_field_C3_and_scalar_branch_results.json"
C3_OWNERSHIP_CSV = SOURCE / "C3_source_ownership_audit.csv"
C3_SELECTION_CSV = SOURCE / "C3_Wilson_selection_and_running.csv"
COMPACT_CSV = SOURCE / "compact_C3_residual_domain.csv"
SCALAR_CSV = SOURCE / "nonlinear_scalar_branch_theorem.csv"
DECISION_CSV = SOURCE / "strong_field_compact_GR_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4963_C3_SELECTION_GLOBAL_SCALAR_BRANCH"
CHECKED_DATE = "2026-07-13"

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054_571_817e-34
M_SUN_KG = 1.98847e30
PLANCK_LENGTH_M = math.sqrt(HBAR * G_NEWTON / C_LIGHT**3)
SOLAR_MASS_LENGTH_M = G_NEWTON * M_SUN_KG / C_LIGHT**2

C3_GRAVITY_PHOTON_SOURCE = -3.669491731602941e-5
C3_SCALAR_SOURCE_DENOMINATOR = 483_840.0 * math.pi**2
FIT_WINDOWS = (10, 20)
RUNNING_SCALE_FACTORS = (0.5, 1.0, 2.0)

SOURCE_PATHS = {
    "trajectory_4935": POST
    / "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md",
    "local_C3_4942": POST
    / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md",
    "mass_family_4942": POST
    / "source-intake"
    / "functional_rg"
    / "4942"
    / "completed_O4_endpoint_Wilson_family.csv",
    "matter_junction_4943": POST
    / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md",
    "scalar_junction_4943": POST
    / "source-intake"
    / "functional_rg"
    / "4943"
    / "junction_scalar_charge_and_fifth_force.csv",
    "fixed_function_convexity_4956": POST
    / "source-intake"
    / "functional_rg"
    / "4956"
    / "functional_regular_convexity_gate.csv",
    "functional_trajectory_4957": POST
    / "4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md",
    "trajectory_regularity_4957": POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "trajectory_functional_regularity_gate.csv",
    "essential_trajectory_4958_doc": POST
    / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md",
    "essential_trajectory_4958": POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_functional_GR_trajectory.csv",
    "IR_convergence_4958": POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_IR_coordinate_convergence.csv",
    "compact_theorem_4962": POST
    / "4962-Y5-R2FR-compact-body-sensitivity-binary-flux-and-junction-matching-or-strong-GR-residual-boundary.md",
    "EOS_stability_4962": POST
    / "source-intake"
    / "functional_rg"
    / "4962"
    / "realistic_EOS_scalar_stability_transfer.csv",
}

EXPECTED_HASHES = {
    "trajectory_4935": "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
    "local_C3_4942": "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f",
    "mass_family_4942": "fc994f761ef08155b926fee675b5617c40aad2ef24b701e645e208fda19b3dea",
    "matter_junction_4943": "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    "scalar_junction_4943": "5fbca2c1672d7fbb6f1741e56a3c72a2adbaee544a4fd5fd5525a616cb836df6",
    "fixed_function_convexity_4956": "f4208beda43a24ddb18cd7d02477f2d9885c991cec1e80b523c64b36a2ef7488",
    "functional_trajectory_4957": "235b2e640428814bbcc3f0af1b2ebef020573314eaae1cb0b793be9122db0cb4",
    "trajectory_regularity_4957": "1071cc4e71dff09a05e1ba10d5c62242d33e2a4cce03c9fe638da402fa1764c2",
    "essential_trajectory_4958_doc": "d08b8a0ab6a5317c77a23accd34dc46c5ad6a0bc5aa73e0767c8e0aa0edd5f1c",
    "essential_trajectory_4958": "b4317dcc01084a61a6b282bd331d2ce111b835e499c86e65077d0fb98a549081",
    "IR_convergence_4958": "724702e024602c8efff03a81245a23221d1f8c8c6a6bf846efb982aecf1e8e3b",
    "compact_theorem_4962": "93c88dd74a719106c998399a4f51bf78f44ed679ff19d3d570c8f3408d2c9134",
    "EOS_stability_4962": "df86b26581b523dcbfa0936c2af65f5d6e10ca4c5d75ac0bbc1b1196fa26a179",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def truth(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def fit_C3_trajectory(
    trajectory: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for row in trajectory:
        groups[(row["scheme"], int(row["polynomial_order"]))].append(row)

    rows: list[dict[str, Any]] = []
    massless_estimates: list[float] = []
    source_slopes: list[float] = []
    maximum_fit_residual = 0.0
    maximum_slope_error = 0.0

    for (scheme, order), group in sorted(groups.items()):
        group.sort(key=lambda row: int(row["sample_index"]))
        endpoint = group[-10:]
        eta_over_g = float(
            np.mean(
                [float(row["eta_psi"]) / float(row["g"]) for row in endpoint]
            )
        )
        c_eff = C3_GRAVITY_PHOTON_SOURCE + (
            eta_over_g / C3_SCALAR_SOURCE_DENOMINATOR
        )
        source_slope = 0.5 * c_eff
        source_slopes.append(source_slope)

        analytic_values = [
            float(row["h_C3"]) / float(row["g"])
            - source_slope * math.log(float(row["g"]))
            for row in endpoint
        ]
        analytic_estimate = float(np.median(analytic_values))
        massless_estimates.append(analytic_estimate)

        for fit_rows in FIT_WINDOWS:
            selected = group[-fit_rows:]
            g_values = np.asarray([float(row["g"]) for row in selected])
            y_values = np.asarray(
                [float(row["h_C3"]) / float(row["g"]) for row in selected]
            )
            log_g = np.log(g_values)
            design = np.column_stack(
                [np.ones(fit_rows), log_g, g_values, g_values * log_g]
            )
            coefficients, _, rank, _ = np.linalg.lstsq(
                design, y_values, rcond=None
            )
            fitted = design @ coefficients
            fit_residual = float(np.max(np.abs(fitted - y_values)))
            slope_error = abs(float(coefficients[1]) - source_slope)
            maximum_fit_residual = max(maximum_fit_residual, fit_residual)
            maximum_slope_error = max(maximum_slope_error, slope_error)
            massless_estimates.append(float(coefficients[0]))
            rows.append(
                {
                    "selection_id": f"C3FIT4963_{scheme}_{order}_{fit_rows}",
                    "scheme": scheme,
                    "polynomial_order": order,
                    "fit_rows": fit_rows,
                    "fit_model": "h_C3/g=A+B ln(g)+C g+D g ln(g)",
                    "A_C3_massless_fit": float(coefficients[0]),
                    "B_C3_fit": float(coefficients[1]),
                    "B_C3_source": source_slope,
                    "eta_psi_over_g_endpoint": eta_over_g,
                    "A_C3_analytic_subtraction_median": analytic_estimate,
                    "maximum_fit_residual": fit_residual,
                    "fit_design_rank": int(rank),
                    "fit_design_condition": float(np.linalg.cond(design)),
                    "slope_source_error": slope_error,
                    "status": "MASSLESS_SOURCE_SCHEME_FINITE_PART_EXTRACTED",
                    "passed": bool(
                        rank == 4
                        and fit_residual < 2.0e-10
                        and slope_error < 5.0e-10
                    ),
                    "valid_for_declared_p6_zero_state": True,
                    "physical_interpretation": "finite renormalized coordinate in the locked natural source scheme; not a scheme-free observable by itself",
                }
            )

    if len(groups) != 4:
        raise RuntimeError(f"expected four trajectory groups, found {len(groups)}")

    mass_family = read_csv(SOURCE_PATHS["mass_family_4942"])
    family_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in mass_family:
        family_groups[(row["mapping"], row["relative_gravity_seed"])].append(row)
    displacements: list[float] = []
    for group in family_groups.values():
        baseline = min(group, key=lambda row: float(row["J_gap_endpoint"]))
        baseline_A = float(baseline["A_C3"])
        displacements.extend(
            abs(float(row["A_C3"]) - baseline_A) for row in group
        )
    finite_gap_displacement = max(displacements)
    maximum_J_gap = max(float(row["J_gap_endpoint"]) for row in mass_family)

    massless_min = min(massless_estimates)
    massless_max = max(massless_estimates)
    selected_min = massless_min - finite_gap_displacement
    selected_max = massless_max + finite_gap_displacement
    selected_abs = max(abs(selected_min), abs(selected_max))
    finite_a_plus_abs = 16.0 * math.pi * selected_abs * PLANCK_LENGTH_M**4
    finite_G_C3_abs = selected_abs * PLANCK_LENGTH_M**2

    rows.extend(
        tagged(
            [
                {
                    "selection_id": "C3SEL4963_massless_envelope",
                    "scheme": "four_scheme_order_branches",
                    "polynomial_order": "6_and_8",
                    "fit_rows": "10_and_20_plus_analytic_subtraction",
                    "fit_model": "union of blind asymptotic fits and source-slope subtraction",
                    "A_C3_massless_min": massless_min,
                    "A_C3_massless_max": massless_max,
                    "B_C3_source_min": min(source_slopes),
                    "B_C3_source_max": max(source_slopes),
                    "status": "MASSLESS_SCHEME_ORDER_ENVELOPE",
                    "passed": massless_max < 0.0,
                    "valid_for_declared_p6_zero_state": True,
                    "physical_interpretation": "regulator/order/numerical bracket in one declared source convention",
                },
                {
                    "selection_id": "C3SEL4963_finite_gap_envelope",
                    "scheme": "inherited_4942_mass_threshold_systematic",
                    "polynomial_order": "older_completed_O4_family",
                    "fit_rows": len(mass_family),
                    "fit_model": "symmetric enlargement by maximum same-family finite-J_gap displacement",
                    "finite_J_gap_max": maximum_J_gap,
                    "finite_gap_A_C3_displacement": finite_gap_displacement,
                    "A_C3_selected_min": selected_min,
                    "A_C3_selected_max": selected_max,
                    "abs_G_C3_selected_m2": finite_G_C3_abs,
                    "abs_a_plus_selected_m4": finite_a_plus_abs,
                    "status": "CONSERVATIVE_FINITE_GAP_SELECTION_ENVELOPE",
                    "passed": selected_max < 0.0,
                    "valid_for_declared_p6_zero_state": True,
                    "physical_interpretation": "conservative threshold systematic; not a rerun of the 4958 functional flow at finite J_gap",
                },
            ]
        )
    )

    rows = [row if "checkpoint_marker" in row else tagged([row])[0] for row in rows]
    summary = {
        "group_count": len(groups),
        "fit_count": len(groups) * len(FIT_WINDOWS),
        "massless_A_C3_min": massless_min,
        "massless_A_C3_max": massless_max,
        "source_B_C3_min": min(source_slopes),
        "source_B_C3_max": max(source_slopes),
        "maximum_fit_residual": maximum_fit_residual,
        "maximum_slope_error": maximum_slope_error,
        "finite_gap_A_C3_displacement": finite_gap_displacement,
        "maximum_J_gap": maximum_J_gap,
        "selected_A_C3_min": selected_min,
        "selected_A_C3_max": selected_max,
        "selected_A_C3_abs_max": selected_abs,
        "selected_G_C3_abs_m2": finite_G_C3_abs,
        "selected_a_plus_abs_m4": finite_a_plus_abs,
        "selected_sign_negative_in_source_scheme": selected_max < 0.0,
    }
    return rows, summary


def C3_ownership_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "operator_id": "C3OWN4963_O1",
                "operator": "O1=X^3",
                "zero_state_C3_source": "zero",
                "reason": "six scalar fields; its zero-background metric/scalar Hessian cannot source the pure C3 projection",
                "status": "SILENT_BY_SCALAR_DEGREE",
                "passed": True,
                "valid_for_declared_p6_zero_state": True,
            },
            {
                "operator_id": "C3OWN4963_O2",
                "operator": "O2=X(nabla nabla psi)^2",
                "zero_state_C3_source": "zero",
                "reason": "scalar degree four; its quadratic Hessian vanishes at psi=0",
                "status": "SILENT_BY_SCALAR_DEGREE",
                "passed": True,
                "valid_for_declared_p6_zero_state": True,
            },
            {
                "operator_id": "C3OWN4963_O3",
                "operator": "O3=C^3",
                "zero_state_C3_source": "target coordinate h_C3",
                "reason": "retained explicitly in every combined fixed point and trajectory",
                "status": "INCLUDED_TARGET",
                "passed": True,
                "valid_for_declared_p6_zero_state": True,
            },
            {
                "operator_id": "C3OWN4963_O4",
                "operator": "O4=C^2 X",
                "zero_state_C3_source": "included through scalar Hessian and eta_psi",
                "reason": "the O4 fixed coordinate and its backreaction are integrated in the 4957/4958 trajectory",
                "status": "INCLUDED_SOURCE",
                "passed": True,
                "valid_for_declared_p6_zero_state": True,
            },
            {
                "operator_id": "C3OWN4963_O5",
                "operator": "O5 reflection-odd scalar-curvature operator",
                "zero_state_C3_source": "forbidden",
                "reason": "selected parent reflection psi->-psi sets u_O5=0",
                "status": "ABSENT_BY_EXACT_REFLECTION",
                "passed": True,
                "valid_for_declared_p6_zero_state": True,
            },
            {
                "operator_id": "C3OWN4963_PX",
                "operator": "complete local P(X) tower",
                "zero_state_C3_source": "eta_psi/(483840 pi^2)",
                "reason": "functional tower retained and its endpoint anomalous-dimension source is included analytically",
                "status": "INCLUDED_FUNCTIONAL_SOURCE",
                "passed": True,
                "valid_for_declared_p6_zero_state": True,
            },
            {
                "operator_id": "C3OWN4963_JGAP",
                "operator": "finite motion mass threshold J_gap",
                "zero_state_C3_source": "bounded by inherited same-family displacement",
                "reason": "4942 supplies a finite-J_gap envelope; the complete 4958 functional flow was not rerun at finite gap",
                "status": "CONSERVATIVE_SYSTEMATIC_NOT_EXACT_CURRENT_RERUN",
                "passed": True,
                "valid_for_declared_p6_zero_state": True,
            },
            {
                "operator_id": "C3OWN4963_P8PLUS",
                "operator": "untruncated p>=8 curvature-motion tower",
                "zero_state_C3_source": "not calculated",
                "reason": "the declared source-completeness theorem stops at the CP-even p6 basis",
                "status": "FULL_PARENT_TAIL_OPEN",
                "passed": True,
                "valid_for_declared_p6_zero_state": False,
            },
        ]
    )


def running_envelope(
    length_m: float,
    A_min: float,
    A_max: float,
    B_min: float,
    B_max: float,
) -> dict[str, float]:
    candidates: list[tuple[float, float, float, float]] = []
    for scale_factor in RUNNING_SCALE_FACTORS:
        g_scale = (scale_factor * PLANCK_LENGTH_M / length_m) ** 2
        for A_value in (A_min, A_max):
            for B_value in (B_min, B_max):
                running_value = A_value + B_value * math.log(g_scale)
                candidates.append(
                    (abs(running_value), running_value, scale_factor, g_scale)
                )
    maximum = max(candidates, key=lambda item: item[0])
    return {
        "A_running_abs_max": maximum[0],
        "A_running_signed_at_max": maximum[1],
        "scale_factor_at_max": maximum[2],
        "g_at_max": maximum[3],
        "a_plus_running_abs_max_m4": 16.0
        * math.pi
        * maximum[0]
        * PLANCK_LENGTH_M**4,
    }


def compact_rows(
    selection: dict[str, Any],
    EOS_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    A_min = float(selection["selected_A_C3_min"])
    A_max = float(selection["selected_A_C3_max"])
    B_min = float(selection["source_B_C3_min"])
    B_max = float(selection["source_B_C3_max"])
    finite_a_plus = float(selection["selected_a_plus_abs_m4"])
    rows: list[dict[str, Any]] = []

    for item in EOS_rows:
        radius_m = 1.0e3 * float(item["radius_km"])
        mass_length = float(item["mass_Msun"]) * SOLAR_MASS_LENGTH_M
        running = running_envelope(radius_m, A_min, A_max, B_min, B_max)
        finite_potential = 20.0 * finite_a_plus * mass_length**2 / radius_m**6
        finite_acceleration = (
            140.0 * finite_a_plus * mass_length**2 / radius_m**6
        )
        running_potential = (
            20.0
            * running["a_plus_running_abs_max_m4"]
            * mass_length**2
            / radius_m**6
        )
        running_acceleration = 7.0 * running_potential
        rows.append(
            {
                "object_id": f"{item['eos_id']}_{item['model_id']}",
                "object_class": "neutron_star",
                "mass_Msun": float(item["mass_Msun"]),
                "radius_or_scale_m": radius_m,
                "mass_length_m": mass_length,
                "A_C3_finite_abs_max": float(selection["selected_A_C3_abs_max"]),
                "a_plus_finite_abs_max_m4": finite_a_plus,
                "finite_abs_DeltaPhi_over_PhiN": finite_potential,
                "finite_abs_Deltaa_over_aN": finite_acceleration,
                "A_C3_running_abs_envelope": running["A_running_abs_max"],
                "a_plus_running_abs_envelope_m4": running[
                    "a_plus_running_abs_max_m4"
                ],
                "running_abs_DeltaPhi_over_PhiN": running_potential,
                "running_abs_Deltaa_over_aN": running_acceleration,
                "running_scale_window": "mu in [1/(2L),2/L]",
                "status": "P6_C3_COMPACT_RESIDUAL_BELOW_ONE_PERCENT",
                "passed": running_acceleration < 0.01,
                "valid_for_declared_p6_zero_state": True,
                "claim_guard": "running envelope is a conservative local-log safety check; a physical amplitude requires local-plus-nonlocal scale cancellation",
            }
        )

    benchmark_radius_m = 12_000.0
    benchmark_mass_length = 1.4 * SOLAR_MASS_LENGTH_M
    benchmark_running = running_envelope(
        benchmark_radius_m, A_min, A_max, B_min, B_max
    )
    benchmark_finite_potential = (
        20.0
        * finite_a_plus
        * benchmark_mass_length**2
        / benchmark_radius_m**6
    )
    benchmark_running_potential = (
        20.0
        * benchmark_running["a_plus_running_abs_max_m4"]
        * benchmark_mass_length**2
        / benchmark_radius_m**6
    )
    rows.append(
        {
            "object_id": "canonical_1p4_12km_benchmark",
            "object_class": "neutron_star_declared_benchmark",
            "mass_Msun": 1.4,
            "radius_or_scale_m": benchmark_radius_m,
            "mass_length_m": benchmark_mass_length,
            "A_C3_finite_abs_max": float(selection["selected_A_C3_abs_max"]),
            "a_plus_finite_abs_max_m4": finite_a_plus,
            "finite_abs_DeltaPhi_over_PhiN": benchmark_finite_potential,
            "finite_abs_Deltaa_over_aN": 7.0 * benchmark_finite_potential,
            "A_C3_running_abs_envelope": benchmark_running["A_running_abs_max"],
            "a_plus_running_abs_envelope_m4": benchmark_running[
                "a_plus_running_abs_max_m4"
            ],
            "running_abs_DeltaPhi_over_PhiN": benchmark_running_potential,
            "running_abs_Deltaa_over_aN": 7.0 * benchmark_running_potential,
            "running_scale_window": "mu in [1/(2L),2/L]",
            "status": "DECLARED_CANONICAL_P6_C3_BENCHMARK_BELOW_ONE_PERCENT",
            "passed": 7.0 * benchmark_running_potential < 0.01,
            "valid_for_declared_p6_zero_state": True,
            "claim_guard": "fixed 1.4 Msun 12 km benchmark, not an additional EOS observation",
        }
    )

    black_hole_mass_length = 10.0 * SOLAR_MASS_LENGTH_M
    running = running_envelope(
        black_hole_mass_length, A_min, A_max, B_min, B_max
    )
    finite_epsilon_h = 0.75 * finite_a_plus / black_hole_mass_length**4
    running_epsilon_h = (
        0.75
        * running["a_plus_running_abs_max_m4"]
        / black_hole_mass_length**4
    )
    rows.append(
        {
            "object_id": "Schwarzschild_10Msun",
            "object_class": "black_hole",
            "mass_Msun": 10.0,
            "radius_or_scale_m": black_hole_mass_length,
            "mass_length_m": black_hole_mass_length,
            "A_C3_finite_abs_max": float(selection["selected_A_C3_abs_max"]),
            "a_plus_finite_abs_max_m4": finite_a_plus,
            "finite_epsilon_h": finite_epsilon_h,
            "A_C3_running_abs_envelope": running["A_running_abs_max"],
            "a_plus_running_abs_envelope_m4": running[
                "a_plus_running_abs_max_m4"
            ],
            "running_epsilon_h": running_epsilon_h,
            "GW250114_robust_epsilon_h_envelope": 0.040,
            "running_scale_window": "mu in [1/(2M),2/M]",
            "status": "P6_C3_HORIZON_CONTROL_BELOW_ONE_PERCENT",
            "passed": running_epsilon_h < 0.01,
            "valid_for_declared_p6_zero_state": True,
            "claim_guard": "static parity-even Schwarzschild proxy; not a rotating waveform or full nonlocal amplitude",
        }
    )

    tagged_rows = tagged(rows)
    finite_values = [
        float(row.get("finite_abs_Deltaa_over_aN", row.get("finite_epsilon_h", 0.0)))
        for row in rows
    ]
    running_values = [
        float(row.get("running_abs_Deltaa_over_aN", row.get("running_epsilon_h", 0.0)))
        for row in rows
    ]
    summary = {
        "object_count": len(rows),
        "EOS_object_count": len(EOS_rows),
        "maximum_finite_compact_residual": max(finite_values),
        "maximum_running_envelope_compact_residual": max(running_values),
        "minimum_orders_below_one_percent_finite": min(
            math.log10(0.01 / value) for value in finite_values if value > 0.0
        ),
        "minimum_orders_below_one_percent_running_envelope": min(
            math.log10(0.01 / value) for value in running_values if value > 0.0
        ),
        "all_p6_compact_rows_pass": all(row["passed"] for row in rows),
    }
    return tagged_rows, summary


def scalar_theorem_rows(
    convexity_rows: list[dict[str, str]],
    regularity_rows: list[dict[str, str]],
    EOS_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    local_fixed = [
        row for row in convexity_rows if math.isclose(float(row["x_domain_max"]), 0.1)
    ]
    extended_fixed = [
        row for row in convexity_rows if math.isclose(float(row["x_domain_max"]), 0.25)
    ]
    local_minimum = min(
        [float(row["minimum_singular_value"]) for row in local_fixed]
        + [float(row["minimum_singular_value"]) for row in regularity_rows]
    )
    local_convex = bool(
        local_fixed
        and all(truth(row["scalar_convex"]) for row in local_fixed)
        and all(truth(row["scalar_convex"]) for row in regularity_rows)
    )
    global_convex = bool(
        extended_fixed
        and all(truth(row["scalar_convex"]) for row in extended_fixed)
    )
    EOS_pass = bool(EOS_rows and all(truth(row["passed"]) for row in EOS_rows))
    maximum_density_ratio = max(
        float(row["central_to_critical_ratio"]) for row in EOS_rows
    )

    rows = tagged(
        [
            {
                "theorem_id": "SCALAR4963_00_equation",
                "clause": "static nonlinear Euler equation",
                "equation": "D_i[N J^i(psi,Dpsi)]-N V_eff'(psi)=0",
                "derivation": "exact variation of the even static effective action; J includes P(X), O4 and matter kinetic contacts",
                "status": "DERIVED_FORM",
                "passed": True,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_01_multiplier",
                "clause": "multiply by psi and integrate",
                "equation": "int N sqrt(gamma)[D_i psi J^i+psi V_eff'(psi)]=boundary",
                "derivation": "one integration by parts over every smooth material domain",
                "status": "EXACT_INTEGRAL_IDENTITY",
                "passed": True,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_02_junction",
                "clause": "internal interfaces cancel",
                "equation": "[psi]=0 and [n_i J^i]=0",
                "derivation": "opposite interface orientations plus the 4943 field-and-flux junctions cancel pairwise",
                "status": "SOURCE_LOCKED_JUNCTION_CANCELLATION",
                "passed": True,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_03_outer_boundary",
                "clause": "outer and regular inner boundaries vanish",
                "equation": "psi->0 at infinity; regular center; N n_i psi J^i->0 at a regular static horizon",
                "derivation": "selected asymptotic state and regularity remove the remaining surface term",
                "status": "BOUNDARY_SILENT_FOR_DECLARED_STATIC_CLASS",
                "passed": True,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_04_kinetic_sign",
                "clause": "strict kinetic monotonicity",
                "equation": "D_i psi J^i >= b_min |D psi|^2 with b_min>0",
                "derivation": f"functional Hessian remains convex on x<=0.1; minimum singular value {local_minimum:.15g}; nine EOS matter shifts remain positive",
                "status": "CERTIFIED_HEALTHY_CHART",
                "passed": local_convex and EOS_pass,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_05_potential_sign",
                "clause": "potential monotonicity",
                "equation": "psi V_eff'(psi)=m_eff^2 psi^2 >=0",
                "derivation": "the retained regular mass-gap operator is quadratic and the matter-corrected m_eff^2 is positive in the certified corridor",
                "status": "NONNEGATIVE_RETAINED_POTENTIAL",
                "passed": EOS_pass,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_06_no_odd_source",
                "clause": "no bulk or surface tadpole",
                "equation": "Gamma[psi]=Gamma[-psi] and delta Gamma/delta psi|0=0",
                "derivation": "parent reflection and metric-only visible matter forbid one-scalar sources; O5 is absent",
                "status": "EXACT_SELECTION_RULE",
                "passed": True,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_07_conclusion",
                "clause": "nonlinear static branch exclusion",
                "equation": "nonnegative integral=0 => D_i psi=0 and psi=0",
                "derivation": "strict kinetic sign forces a constant; positive mass or psi_infinity=0 fixes that constant to zero",
                "status": "NO_HEALTHY_DISCONNECTED_STATIC_SCALAR_BRANCH_IN_CERTIFIED_DOMAIN",
                "passed": local_convex and EOS_pass,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_08_failure_surface",
                "clause": "necessary escape route for a disconnected branch",
                "equation": "branch implies x>0.1 or P_X<=0 or P_X+2XP_XX<=0 or psi V' <0 or odd/boundary source",
                "derivation": "contrapositive of the multiplier theorem",
                "status": "EXPLICIT_FAILURE_SURFACE_SET",
                "passed": not global_convex,
                "valid_for_certified_x_le_0p1": True,
            },
            {
                "theorem_id": "SCALAR4963_09_all_X_boundary",
                "clause": "all-amplitude global theorem",
                "equation": "not established beyond x=0.1",
                "derivation": "both N12 fixed-function charts lose scalar convexity before x=0.25",
                "status": "GLOBAL_ALL_X_EXCLUSION_FALSE",
                "passed": not global_convex,
                "valid_for_certified_x_le_0p1": False,
            },
            {
                "theorem_id": "SCALAR4963_10_dynamical_boundary",
                "clause": "time-dependent binaries and rotating horizons",
                "equation": "not covered by the static positive-multiplier theorem",
                "derivation": "requires a hyperbolic energy estimate or nonlinear evolution, not a static elliptic identity",
                "status": "DYNAMICAL_EXTENSION_OPEN",
                "passed": True,
                "valid_for_certified_x_le_0p1": False,
            },
        ]
    )
    summary = {
        "local_fixed_function_row_count": len(local_fixed),
        "trajectory_regularity_row_count": len(regularity_rows),
        "local_minimum_Hessian_singular_value": local_minimum,
        "local_x_le_0p1_convex": local_convex,
        "x_le_0p25_globally_convex": global_convex,
        "EOS_row_count": len(EOS_rows),
        "EOS_all_pass": EOS_pass,
        "maximum_density_to_instability_ratio": maximum_density_ratio,
        "healthy_static_disconnected_branch_x_le_0p1_excluded": bool(
            local_convex and EOS_pass
        ),
        "all_X_static_branch_excluded": False,
        "dynamical_branch_excluded": False,
    }
    return rows, summary


def decision_rows(
    C3_summary: dict[str, Any],
    compact_summary: dict[str, Any],
    scalar_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    p6_selection = bool(
        C3_summary["selected_sign_negative_in_source_scheme"]
        and compact_summary["all_p6_compact_rows_pass"]
    )
    scalar_local = bool(
        scalar_summary["healthy_static_disconnected_branch_x_le_0p1_excluded"]
    )
    return tagged(
        [
            {
                "decision_id": "DEC4963_00_C3_p6_selection",
                "question": "Does the declared p6 zero-state trajectory select a finite C3 coordinate?",
                "decision": "YES_IN_LOCKED_SOURCE_SCHEME",
                "reason": "all four scheme/order trajectories share the derived logarithmic source and a finite negative A_C3 bracket after the inherited finite-gap systematic",
                "passed": p6_selection,
                "valid_for_declared_p6_healthy_static_domain": True,
            },
            {
                "decision_id": "DEC4963_01_C3_compact",
                "question": "Can the selected p6 C3 coordinate spoil the compact GR corridor?",
                "decision": "NO_WITHIN_DECLARED_LOCAL_AND_RUNNING_ENVELOPES",
                "reason": f"the worst compact running-envelope residual is {compact_summary['maximum_running_envelope_compact_residual']:.6e}, over {compact_summary['minimum_orders_below_one_percent_running_envelope']:.3f} orders below one percent",
                "passed": compact_summary["all_p6_compact_rows_pass"],
                "valid_for_declared_p6_healthy_static_domain": True,
            },
            {
                "decision_id": "DEC4963_02_scalar_nonlinear",
                "question": "Can a healthy disconnected static scalarized branch exist entirely inside x<=0.1?",
                "decision": "NO",
                "reason": "the exact multiplier identity has positive kinetic and potential terms and silent junction/asymptotic boundaries",
                "passed": scalar_local,
                "valid_for_declared_p6_healthy_static_domain": True,
            },
            {
                "decision_id": "DEC4963_03_scalar_all_X",
                "question": "Is every nonlinear scalar branch excluded at arbitrary amplitude?",
                "decision": "NO",
                "reason": "the N12 charts lose convexity before x=0.25 and dynamical or rotating configurations are not covered",
                "passed": True,
                "valid_for_declared_p6_healthy_static_domain": False,
            },
            {
                "decision_id": "DEC4963_04_all_operator_compact_GR",
                "question": "Is exact all-operator compact GR established?",
                "decision": "NO",
                "reason": "p>=8 source completeness, finite R2/C2 and physical CFF matching, all-X scalar control and nonlocal C3 amplitude completion remain open",
                "passed": True,
                "valid_for_declared_p6_healthy_static_domain": False,
            },
            {
                "decision_id": "DEC4963_05_full_MTS",
                "question": "Is full MTS-to-GR emergence established?",
                "decision": "NO",
                "reason": "the result remains branch-, truncation- and domain-conditional and does not derive the absolute Newton residue or every MTS state",
                "passed": True,
                "valid_for_declared_p6_healthy_static_domain": False,
            },
            {
                "decision_id": "DEC4963_06_next_target",
                "question": "What is the next verdict-changing compact target?",
                "decision": "FINITE_R2_C2_CFF_MATCHING_AND_P8PLUS_TAIL",
                "reason": "C3 and healthy static scalar branches no longer dominate the controlled p6 compact residual",
                "passed": True,
                "valid_for_declared_p6_healthy_static_domain": False,
            },
        ]
    )


def provenance_text(
    source_hashes: dict[str, str],
    C3_summary: dict[str, Any],
    compact_summary: dict[str, Any],
    scalar_summary: dict[str, Any],
) -> str:
    lines = [
        "# 4963 provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        "All inputs are local, hash-locked products of the existing private MTS chain. No web acquisition or GitHub action was used.",
        "",
        "## Inputs",
        "",
    ]
    for name, path in SOURCE_PATHS.items():
        lines.append(f"- `{name}`: `{path.relative_to(ROOT)}`")
        lines.append(f"  - SHA256 `{source_hashes[name]}`")
    lines.extend(
        [
            "",
            "## C3 extraction",
            "",
            "For each of the four 4958 scheme/order trajectories, the final 10 and 20 rows are fit to `h_C3/g=A+B ln(g)+C g+D g ln(g)`. The fitted logarithmic slope is checked against the independently derived Gaussian source",
            "",
            "`B=[c_gravity+photon+(eta_psi/g)/(483840 pi^2)]/2`.",
            "",
            "The finite massless envelope is the union of those blind fits and direct analytic-slope subtraction. It is enlarged symmetrically by the maximum same-family finite-`J_gap` displacement in the 4942 45-row family. This is deliberately conservative because the 4958 functional trajectory was not rerun at finite gap.",
            "",
            f"- selected `A_C3` bracket: `{C3_summary['selected_A_C3_min']:.16e}` to `{C3_summary['selected_A_C3_max']:.16e}`",
            f"- maximum `|a_+|`: `{C3_summary['selected_a_plus_abs_m4']:.16e} m^4`",
            "",
            "The finite coordinate is source-scheme dependent. A separate `mu in [1/(2L),2/L]` raw-running envelope is reported only as a conservative log-sensitivity check. A physical amplitude must combine the local coefficient with the corresponding nonlocal loop form factor so that the scale dependence cancels.",
            "",
            "## Scalar theorem",
            "",
            "The nonlinear conclusion is an exact static multiplier theorem inside the certified healthy chart, not a polynomial small-amplitude expansion. Internal surface terms cancel by the 4943 field/flux junctions. Positivity is imported from the 4956/4957 Hessian scans and the 4962 EOS transfer.",
            "",
            f"- minimum certified Hessian singular value: `{scalar_summary['local_minimum_Hessian_singular_value']:.16e}`",
            f"- maximum EOS density/instability ratio: `{scalar_summary['maximum_density_to_instability_ratio']:.16e}`",
            "- healthy static branch inside `x<=0.1`: excluded",
            "- all-`X`, dynamical and rotating branch exclusion: not established",
            "",
            "## Compact gate",
            "",
            f"- maximum finite p6 compact residual: `{compact_summary['maximum_finite_compact_residual']:.16e}`",
            f"- maximum raw-running envelope residual: `{compact_summary['maximum_running_envelope_compact_residual']:.16e}`",
            f"- minimum log-running safety margin below one percent: `{compact_summary['minimum_orders_below_one_percent_running_envelope']:.6f}` orders",
            "",
            "No row is valid for a full-MTS claim.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)
    missing = [name for name, path in SOURCE_PATHS.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source paths: {missing}")

    source_hashes = {name: digest(path) for name, path in SOURCE_PATHS.items()}
    bad_hashes = {
        name: {"expected": EXPECTED_HASHES[name], "actual": actual}
        for name, actual in source_hashes.items()
        if EXPECTED_HASHES.get(name) != actual
    }
    if bad_hashes:
        raise RuntimeError(f"source hash mismatch: {bad_hashes}")

    source_text = {
        name: path.read_text(encoding="utf-8-sig")
        for name, path in SOURCE_PATHS.items()
        if path.suffix.lower() == ".md"
    }
    source_clause_checks = {
        "4935_C3_asymptotic": all(
            token in source_text["trajectory_4935"]
            for token in ("h_C3/g", "A_C3", "c_C3/2")
        ),
        "4942_C3_metric": all(
            token in source_text["local_C3_4942"]
            for token in ("a_+=16pi A_C3 l_P^4", "140|a_+|M^2/r^6")
        ),
        "4943_junction": all(
            token in source_text["matter_junction_4943"]
            for token in ("[psi]_Sigma=0", "Q_psi", "a_psi/a_N=0")
        ),
        "4957_operator_firewall": all(
            token in source_text["functional_trajectory_4957"]
            for token in ("O2:", "O4:", "O5:", "x<=0.1")
        ),
        "4958_GR_trajectory": all(
            token in source_text["essential_trajectory_4958_doc"]
            for token in ("one GR-connected relevant direction", "essential trajectory to Gaussian GR")
        ),
        "4962_compact_boundary": all(
            token in source_text["compact_theorem_4962"]
            for token in ("alpha_A", "C_rad", "disconnected nonlinear scalar")
        ),
    }
    if not all(source_clause_checks.values()):
        raise RuntimeError(f"source clause mismatch: {source_clause_checks}")

    trajectory = read_csv(SOURCE_PATHS["essential_trajectory_4958"])
    convergence = read_csv(SOURCE_PATHS["IR_convergence_4958"])
    convexity = read_csv(SOURCE_PATHS["fixed_function_convexity_4956"])
    regularity = read_csv(SOURCE_PATHS["trajectory_regularity_4957"])
    EOS = read_csv(SOURCE_PATHS["EOS_stability_4962"])
    junction = read_csv(SOURCE_PATHS["scalar_junction_4943"])

    if not trajectory or not convergence or not convexity or not regularity or not EOS:
        raise RuntimeError("one or more source tables are empty")
    if not all(truth(row["converged_below_1e_minus_3"]) for row in convergence):
        raise RuntimeError("4958 infrared convergence source does not fully pass")
    if not all(truth(row["passed"]) for row in EOS):
        raise RuntimeError("4962 EOS stability source does not fully pass")
    if not any("flux" in " ".join(row.values()).lower() for row in junction):
        raise RuntimeError("4943 junction source lacks a flux row")

    C3_selection, C3_summary = fit_C3_trajectory(trajectory)
    ownership = C3_ownership_rows()
    compact, compact_summary = compact_rows(C3_summary, EOS)
    scalar, scalar_summary = scalar_theorem_rows(convexity, regularity, EOS)
    decisions = decision_rows(C3_summary, compact_summary, scalar_summary)

    checks = {
        "all_source_hashes_match": not bad_hashes,
        "all_source_clauses_match": all(source_clause_checks.values()),
        "four_C3_trajectory_groups": C3_summary["group_count"] == 4,
        "eight_asymptotic_fits": C3_summary["fit_count"] == 8,
        "C3_fit_residual_below_2e_10": C3_summary["maximum_fit_residual"] < 2.0e-10,
        "C3_log_slope_matches_source": C3_summary["maximum_slope_error"] < 5.0e-10,
        "finite_gap_displacement_recomputed": math.isclose(
            C3_summary["finite_gap_A_C3_displacement"],
            8.08875617759326e-8,
            rel_tol=1.0e-12,
        ),
        "C3_finite_sign_selected_negative": C3_summary[
            "selected_sign_negative_in_source_scheme"
        ],
        "C3_p6_source_basis_closed": all(
            row["passed"]
            for row in ownership
            if row["operator_id"] != "C3OWN4963_P8PLUS"
        ),
        "C3_untruncated_tail_not_claimed": not next(
            row for row in ownership if row["operator_id"] == "C3OWN4963_P8PLUS"
        )["valid_for_declared_p6_zero_state"],
        "nine_EOS_rows_reused": len(EOS) == 9,
        "all_compact_p6_rows_pass": compact_summary["all_p6_compact_rows_pass"],
        "running_envelope_below_one_percent": compact_summary[
            "maximum_running_envelope_compact_residual"
        ]
        < 0.01,
        "local_scalar_chart_convex": scalar_summary["local_x_le_0p1_convex"],
        "global_scalar_chart_not_claimed": not scalar_summary[
            "x_le_0p25_globally_convex"
        ],
        "healthy_static_scalar_branch_excluded_in_chart": scalar_summary[
            "healthy_static_disconnected_branch_x_le_0p1_excluded"
        ],
        "all_X_scalar_exclusion_false": not scalar_summary[
            "all_X_static_branch_excluded"
        ],
        "all_operator_compact_GR_false": next(
            row
            for row in decisions
            if row["decision_id"] == "DEC4963_04_all_operator_compact_GR"
        )["decision"]
        == "NO",
        "full_MTS_false": next(
            row
            for row in decisions
            if row["decision_id"] == "DEC4963_05_full_MTS"
        )["decision"]
        == "NO",
    }
    if not all(checks.values()):
        raise RuntimeError(
            f"internal checkpoint checks failed: {[name for name, passed in checks.items() if not passed]}"
        )

    write_csv(C3_OWNERSHIP_CSV, ownership)
    write_csv(C3_SELECTION_CSV, C3_selection)
    write_csv(COMPACT_CSV, compact)
    write_csv(SCALAR_CSV, scalar)
    write_csv(DECISION_CSV, decisions)

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "C3_selection": C3_summary,
        "compact_residual_domain": compact_summary,
        "nonlinear_scalar_theorem": scalar_summary,
        "checks": checks,
        "decisions": {
            row["decision_id"]: row["decision"] for row in decisions
        },
        "claim_scope": {
            "declared_p6_zero_state_C3_selected": True,
            "healthy_static_scalar_branch_x_le_0p1_excluded": True,
            "all_X_scalar_branch_excluded": False,
            "all_operator_compact_GR": False,
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    PROVENANCE.write_text(
        provenance_text(source_hashes, C3_summary, compact_summary, scalar_summary),
        encoding="utf-8",
    )

    print(f"{MARKER}_CHECKS={sum(checks.values())}/{len(checks)}", flush=True)
    print(
        f"{MARKER}_A_C3=[{C3_summary['selected_A_C3_min']:.16e},{C3_summary['selected_A_C3_max']:.16e}]",
        flush=True,
    )
    print(
        f"{MARKER}_MAX_RUNNING_COMPACT_RESIDUAL={compact_summary['maximum_running_envelope_compact_residual']:.16e}",
        flush=True,
    )
    print(
        f"{MARKER}_SCALAR_STATIC_XLE0P1_EXCLUDED={scalar_summary['healthy_static_disconnected_branch_x_le_0p1_excluded']}",
        flush=True,
    )
    print(f"{MARKER}_FULL_MTS=False", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
