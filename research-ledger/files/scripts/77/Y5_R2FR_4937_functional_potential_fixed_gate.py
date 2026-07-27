from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4937"
OUTPUT = SOURCE_DIR / "functional_potential_fixed_gate_results.json"
ROOT_OUTPUT = SOURCE_DIR / "constant_potential_root_spectrum.csv"
MES_OUTPUT = SOURCE_DIR / "minimal_essential_motion_spectrum.csv"
SHOOTING_OUTPUT = SOURCE_DIR / "fixed_function_shooting_scan.csv"
COMPATIBILITY_OUTPUT = SOURCE_DIR / "fixed_function_compatibility_brackets.csv"

TRAJECTORY_4935 = POST / "source-intake" / "functional_rg" / "4935" / "completed_fixed_point_trajectory_results.json"
HESSIAN_4937 = SOURCE_DIR / "gravity_motion_block_hessian_results.json"
WETTERICH_SOURCE = SOURCE_DIR / "src-1911.06100v3" / "Eff_Scalar_Pot_ASQG.tex"
MINIMAL_ESSENTIAL_SOURCE = POST / "source-intake" / "functional_rg" / "4929" / "src2204" / "R2scalarMES.tex"

MARKER = "MTS_4937_FUNCTIONAL_POTENTIAL_FIXED_GATE"
EXPECTED_HASHES = {
    TRAJECTORY_4935: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    HESSIAN_4937: "48303c49eac3f41d0e3ba93e9fb82c8cd7f79fc1cc9717f006dba8cc4ecbed73",
    WETTERICH_SOURCE: "5d742ca63e93e1715adfba01f83c6c6cf2fcbbdb57407cb472eee5133914b9b9",
    MINIMAL_ESSENTIAL_SOURCE: "56a906bdfef4af8c1e7a337263636bd0b2d5c863b5d5c52382385b655da4bdd7",
}

SCHEMES = {
    "canonical_signed_block": 1.0,
    "source_diagonal_calibrated": 4.0 / 3.0,
}
MASS_SCAN = (
    -0.99,
    -0.97,
    -0.95,
    -0.90,
    -0.50,
    -0.10,
    -0.01,
    -0.001,
    -0.0001,
    0.0,
    0.0001,
    0.001,
    0.002,
    0.003,
    0.01,
    0.1,
    1.0,
    10.0,
)
PHI_MAX = 3.0
DENOMINATOR_STOP = 1.0e-3
TT_POLE_STOP = 1.0e-5
BLOWUP_STOP = 100.0


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table {path.name}")
    fieldnames = list(rows[0])
    for row in rows[1:]:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    hash_failures = {
        path.as_posix(): {"expected": expected, "actual": digest(path) if path.exists() else "MISSING"}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if hash_failures:
        raise RuntimeError(f"fixed-functional source hash mismatch: {hash_failures}")

    trajectory = json.loads(TRAJECTORY_4935.read_text(encoding="utf-8"))
    hessian = json.loads(HESSIAN_4937.read_text(encoding="utf-8"))
    newton_fixed = float(trajectory["flow_contract"]["fixed_point"][0])
    existing_relevant_directions = 1
    dimensionless_planck = 1.0 / (16.0 * math.pi * newton_fixed)
    loop_factor = 1.0 / (32.0 * math.pi**2)

    def trace_a(potential: float) -> float:
        return 1.0 - potential / (4.0 * dimensionless_planck)

    def tt_trace(potential: float) -> float:
        return 5.0 / (
            24.0
            * math.pi**2
            * (1.0 - potential / dimensionless_planck)
        )

    def boundary_beta(potential: float, mass_squared: float, sigma_weight: float) -> float:
        return (
            -4.0 * potential
            + tt_trace(potential)
            - 1.0 / (8.0 * math.pi**2)
            + loop_factor
            * (1.0 / (1.0 + mass_squared) + sigma_weight / trace_a(potential))
        )

    @lru_cache(maxsize=None)
    def boundary_roots(mass_squared: float, sigma_weight: float) -> tuple[float, ...]:
        if mass_squared <= -1.0:
            return ()
        grid = np.linspace(
            -2.0 * dimensionless_planck,
            0.999 * dimensionless_planck,
            2000,
        )
        values = [boundary_beta(value, mass_squared, sigma_weight) for value in grid]
        roots: list[float] = []
        for left, right, left_value, right_value in zip(
            grid[:-1], grid[1:], values[:-1], values[1:]
        ):
            if not (math.isfinite(left_value) and math.isfinite(right_value)):
                continue
            if left_value == 0.0:
                root = float(left)
            elif left_value * right_value >= 0.0:
                continue
            else:
                root = float(
                    brentq(
                        lambda candidate: boundary_beta(
                            candidate, mass_squared, sigma_weight
                        ),
                        float(left),
                        float(right),
                        xtol=1.0e-14,
                        rtol=1.0e-13,
                    )
                )
            if not roots or abs(root - roots[-1]) > 1.0e-8:
                roots.append(root)
        return tuple(roots)

    def gravity_anomalous_dimension(v_value: float, sigma_weight: float) -> float:
        return (
            5.0
            / (
                24.0
                * math.pi**2
                * dimensionless_planck
                * (1.0 - v_value) ** 2
            )
            + sigma_weight
            / (
                128.0
                * math.pi**2
                * dimensionless_planck
                * (1.0 - v_value / 4.0) ** 2
            )
        )

    root_rows: list[dict[str, Any]] = []
    constant_roots: dict[str, list[dict[str, Any]]] = {}
    for scheme, sigma_weight in SCHEMES.items():
        roots = boundary_roots(0.0, sigma_weight)
        if len(roots) != 2:
            raise RuntimeError(f"expected two constant roots for {scheme}, found {roots}")
        constant_roots[scheme] = []
        for branch_index, potential in enumerate(roots):
            branch = "low" if branch_index == 0 else "high_near_barrier"
            v_value = potential / dimensionless_planck
            anomalous_dimension = gravity_anomalous_dimension(v_value, sigma_weight)
            theta_vacuum = 4.0 - anomalous_dimension
            theta_mass = 2.0 - anomalous_dimension
            theta_quartic = -anomalous_dimension
            theta_fractional_diagonal = 8.0 / 3.0 - anomalous_dimension
            mes_magnitude = 3.0 * newton_fixed / (8.0 * math.pi)
            row = {
                "scheme": scheme,
                "r_sigma": sigma_weight,
                "branch": branch,
                "u0": potential,
                "v0": v_value,
                "TT_pole_margin_1_minus_v": 1.0 - v_value,
                "distance_to_positive_MES_v": abs(v_value - mes_magnitude),
                "A_gravity": anomalous_dimension,
                "theta_vacuum_n0": theta_vacuum,
                "theta_mass_n2": theta_mass,
                "theta_quartic_n4": theta_quartic,
                "theta_fractional_formal_diagonal": theta_fractional_diagonal,
                "regular_even_scalar_relevant_directions_excluding_vacuum": int(theta_mass > 0.0)
                + int(theta_quartic > 0.0),
                "compatible_with_current_MES_v_branch": abs(v_value - mes_magnitude) < 0.05,
                "one_total_relevant_direction_after_Newton_scale": existing_relevant_directions
                + int(theta_mass > 0.0)
                + int(theta_quartic > 0.0)
                == 1,
                "valid_for_full_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
            root_rows.append(row)
            constant_roots[scheme].append(row)

    mes_rows: list[dict[str, Any]] = []
    mes_v_magnitude = 3.0 * newton_fixed / (8.0 * math.pi)
    for sign_label, v_value in (
        ("Wetterich_v_equals_plus_2lambda", mes_v_magnitude),
        ("Wetterich_v_equals_minus_2lambda", -mes_v_magnitude),
    ):
        anomalous_dimension = gravity_anomalous_dimension(
            v_value, SCHEMES["source_diagonal_calibrated"]
        )
        mes_rows.append(
            {
                "mapping": sign_label,
                "g_fixed": newton_fixed,
                "lambda_MES": 3.0 * newton_fixed / (16.0 * math.pi),
                "v_value": v_value,
                "w_value": dimensionless_planck,
                "A_gravity": anomalous_dimension,
                "theta_mass_n2": 2.0 - anomalous_dimension,
                "theta_quartic_n4": -anomalous_dimension,
                "theta_fractional_formal_diagonal": 8.0 / 3.0
                - anomalous_dimension,
                "mass_direction_relevant": 2.0 - anomalous_dimension > 0.0,
                "fractional_is_regular_eigenoperator": False,
                "interpretation": "sign-robust MES comparator; not an absolute-potential root because the essential scheme fixes vacuum energy by a running field redefinition",
                "valid_for_full_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    def fixed_ode_parts(
        field: float,
        potential: float,
        slope: float,
        sigma_weight: float,
    ) -> dict[str, float]:
        a_value = trace_a(potential)
        tt_denominator = 1.0 - potential / dimensionless_planck
        y_value = 32.0 * math.pi**2 * (
            4.0 * potential
            - field * slope
            - tt_trace(potential)
            + 1.0 / (8.0 * math.pi**2)
        )
        mixing_squared = 3.0 * slope**2 / (4.0 * dimensionless_planck)
        denominator = y_value * a_value - sigma_weight
        numerator = a_value - y_value * mixing_squared
        return {
            "a": a_value,
            "tt_denominator": tt_denominator,
            "Y": y_value,
            "mu_squared": mixing_squared,
            "ode_denominator": denominator,
            "ode_numerator": numerator,
            "block_pole_from_reconstructed_b": math.nan,
        }

    def integrate_shot(
        mass_squared: float,
        sigma_weight: float,
        branch_index: int,
        denominator_stop: float = DENOMINATOR_STOP,
        blowup_stop: float = BLOWUP_STOP,
        phi_max: float = PHI_MAX,
    ) -> dict[str, Any]:
        roots = boundary_roots(mass_squared, sigma_weight)
        branch = "low" if branch_index == 0 else "high_near_barrier"
        if len(roots) <= branch_index:
            return {
                "mass_squared": mass_squared,
                "branch": branch,
                "termination": "NO_REGULAR_BOUNDARY_ROOT",
                "reached_phi": 0.0,
                "success": False,
            }
        potential_zero = roots[branch_index]
        boundary_residual = boundary_beta(
            potential_zero, mass_squared, sigma_weight
        )
        if mass_squared == 0.0:
            parts = fixed_ode_parts(0.0, potential_zero, 0.0, sigma_weight)
            return {
                "mass_squared": mass_squared,
                "branch": branch,
                "u0": potential_zero,
                "boundary_residual": boundary_residual,
                "termination": "ANALYTIC_CONSTANT_GLOBAL",
                "reached_phi": math.inf,
                "endpoint_u": potential_zero,
                "endpoint_u_prime": 0.0,
                "endpoint_ode_denominator": parts["ode_denominator"],
                "endpoint_ode_numerator": parts["ode_numerator"],
                "endpoint_TT_margin": abs(parts["tt_denominator"]),
                "success": True,
            }

        def right_hand_side(field: float, state: np.ndarray) -> np.ndarray:
            potential, slope = (float(value) for value in state)
            parts = fixed_ode_parts(field, potential, slope, sigma_weight)
            curvature = (
                parts["ode_numerator"] / parts["ode_denominator"] - 1.0
            )
            if not math.isfinite(curvature):
                raise FloatingPointError("nonfinite fixed-functional curvature")
            return np.array([slope, curvature], dtype=float)

        def denominator_event(field: float, state: np.ndarray) -> float:
            parts = fixed_ode_parts(
                field, float(state[0]), float(state[1]), sigma_weight
            )
            return abs(parts["ode_denominator"]) - denominator_stop

        denominator_event.terminal = True
        denominator_event.direction = -1

        def tt_pole_event(field: float, state: np.ndarray) -> float:
            parts = fixed_ode_parts(
                field, float(state[0]), float(state[1]), sigma_weight
            )
            return abs(parts["tt_denominator"]) - TT_POLE_STOP

        tt_pole_event.terminal = True
        tt_pole_event.direction = -1

        def blowup_event(_field: float, state: np.ndarray) -> float:
            return blowup_stop - max(abs(float(state[0])), abs(float(state[1])))

        blowup_event.terminal = True
        blowup_event.direction = -1

        try:
            solution = solve_ivp(
                right_hand_side,
                (0.0, phi_max),
                np.array([potential_zero, 0.0], dtype=float),
                method="DOP853",
                rtol=3.0e-7,
                atol=np.array([3.0e-9, 3.0e-9]),
                max_step=0.05,
                events=(denominator_event, tt_pole_event, blowup_event),
            )
            event_names = (
                "ODE_DENOMINATOR_APPROACH",
                "TT_POLE_APPROACH",
                "RUNAWAY_FIELD_OR_SLOPE",
            )
            termination = "PHI_MAX_REACHED"
            for name, event_times in zip(event_names, solution.t_events):
                if len(event_times):
                    termination = name
                    break
            if not solution.success and termination == "PHI_MAX_REACHED":
                termination = "INTEGRATOR_FAILURE"
            endpoint_field = float(solution.t[-1])
            endpoint_u = float(solution.y[0, -1])
            endpoint_slope = float(solution.y[1, -1])
            parts = fixed_ode_parts(
                endpoint_field, endpoint_u, endpoint_slope, sigma_weight
            )
            if abs(parts["ode_denominator"]) > 0.0:
                reconstructed_b = (
                    parts["ode_numerator"] / parts["ode_denominator"]
                )
                parts["block_pole_from_reconstructed_b"] = (
                    parts["a"] * reconstructed_b + parts["mu_squared"]
                )
            return {
                "mass_squared": mass_squared,
                "branch": branch,
                "u0": potential_zero,
                "boundary_residual": boundary_residual,
                "termination": termination,
                "reached_phi": endpoint_field,
                "endpoint_u": endpoint_u,
                "endpoint_u_prime": endpoint_slope,
                "endpoint_ode_denominator": parts["ode_denominator"],
                "endpoint_ode_numerator": parts["ode_numerator"],
                "endpoint_block_pole_factor": parts[
                    "block_pole_from_reconstructed_b"
                ],
                "endpoint_TT_margin": abs(parts["tt_denominator"]),
                "steps": int(len(solution.t)),
                "message": str(solution.message),
                "success": bool(solution.success),
            }
        except (FloatingPointError, ValueError, OverflowError) as error:
            return {
                "mass_squared": mass_squared,
                "branch": branch,
                "u0": potential_zero,
                "boundary_residual": boundary_residual,
                "termination": "NUMERIC_EXCEPTION",
                "reached_phi": 0.0,
                "message": str(error),
                "success": False,
            }

    shooting_rows: list[dict[str, Any]] = []
    for scheme, sigma_weight in SCHEMES.items():
        for branch_index in (0, 1):
            for mass_squared in MASS_SCAN:
                row = integrate_shot(mass_squared, sigma_weight, branch_index)
                row = {
                    "scheme": scheme,
                    "r_sigma": sigma_weight,
                    **row,
                    "nonconstant_global_candidate": mass_squared != 0.0
                    and row.get("termination") == "PHI_MAX_REACHED",
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
                shooting_rows.append(row)

    def compatibility_bracket(
        sigma_weight: float,
        left_mass: float,
        right_mass: float,
        label: str,
    ) -> dict[str, Any]:
        left = integrate_shot(
            left_mass,
            sigma_weight,
            0,
            denominator_stop=1.0e-3,
            blowup_stop=50.0,
            phi_max=1.5,
        )
        right = integrate_shot(
            right_mass,
            sigma_weight,
            0,
            denominator_stop=1.0e-3,
            blowup_stop=50.0,
            phi_max=1.5,
        )

        def singular(row: dict[str, Any]) -> bool:
            return row["termination"] == "ODE_DENOMINATOR_APPROACH"

        if singular(left) == singular(right):
            return {
                "candidate": label,
                "left_mass": left_mass,
                "right_mass": right_mass,
                "status": "NO_TERMINATION_TRANSITION_IN_DECLARED_BRACKET",
                "left_termination": left["termination"],
                "right_termination": right["termination"],
            }
        nonsingular_mass = left_mass if not singular(left) else right_mass
        singular_mass = right_mass if singular(right) else left_mass
        nonsingular_row = left if not singular(left) else right
        singular_row = right if singular(right) else left
        for _ in range(14):
            midpoint = (nonsingular_mass + singular_mass) / 2.0
            midpoint_row = integrate_shot(
                midpoint,
                sigma_weight,
                0,
                denominator_stop=1.0e-3,
                blowup_stop=50.0,
                phi_max=1.5,
            )
            if singular(midpoint_row):
                singular_mass = midpoint
                singular_row = midpoint_row
            else:
                nonsingular_mass = midpoint
                nonsingular_row = midpoint_row
        return {
            "candidate": label,
            "nonsingular_side_mass": nonsingular_mass,
            "singular_side_mass": singular_mass,
            "mass_bracket_width": abs(singular_mass - nonsingular_mass),
            "nonsingular_termination": nonsingular_row["termination"],
            "singular_termination": singular_row["termination"],
            "singular_endpoint_phi": singular_row.get("reached_phi"),
            "singular_endpoint_u": singular_row.get("endpoint_u"),
            "singular_endpoint_u_prime": singular_row.get("endpoint_u_prime"),
            "singular_endpoint_denominator": singular_row.get(
                "endpoint_ode_denominator"
            ),
            "singular_endpoint_numerator": singular_row.get(
                "endpoint_ode_numerator"
            ),
            "status": "FINITE_FIELD_TERMINATION_TRANSITION_NOT_GLOBAL_SOLUTION",
        }

    compatibility_rows: list[dict[str, Any]] = []
    for scheme, sigma_weight in SCHEMES.items():
        positive_bracket = (
            (0.0001, 0.001)
            if scheme == "canonical_signed_block"
            else (0.001, 0.004)
        )
        for left_mass, right_mass, label in (
            (*positive_bracket, "positive_mass_transition"),
            (-0.99, -0.90, "near_scalar_threshold_transition"),
        ):
            row = compatibility_bracket(
                sigma_weight, left_mass, right_mass, label
            )
            row.update(
                {
                    "scheme": scheme,
                    "r_sigma": sigma_weight,
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
            compatibility_rows.append(row)

    generic_nonconstant_successes = [
        row
        for row in shooting_rows
        if row["mass_squared"] != 0.0
        and row["termination"] == "PHI_MAX_REACHED"
    ]
    low_rows = [row for row in root_rows if row["branch"] == "low"]
    high_rows = [row for row in root_rows if row["branch"] == "high_near_barrier"]
    canonical_scale_lock_beta = -Fraction(8, 3) + Fraction(4, 3) * 2
    checks = {
        "Hessian_checkpoint_passed": all(hessian["checks"].values()),
        "source_fixed_point_has_one_relevant_direction": trajectory[
            "flow_contract"
        ]["relevant_critical_exponent"]
        > 0.0,
        "w_mapping_positive": dimensionless_planck > 0.0,
        "two_constant_roots_each_scheme": all(
            len(constant_roots[scheme]) == 2 for scheme in SCHEMES
        ),
        "all_low_roots_have_relevant_mass": all(
            row["theta_mass_n2"] > 0.0 for row in low_rows
        ),
        "all_high_roots_have_irrelevant_mass": all(
            row["theta_mass_n2"] < 0.0 for row in high_rows
        ),
        "all_high_roots_near_TT_barrier": all(
            row["TT_pole_margin_1_minus_v"] < 0.04 for row in high_rows
        ),
        "all_high_roots_incompatible_with_MES_v": all(
            not row["compatible_with_current_MES_v_branch"] for row in high_rows
        ),
        "MES_sign_map_keeps_mass_relevant": all(
            row["mass_direction_relevant"] for row in mes_rows
        ),
        "no_generic_nonconstant_scan_reaches_phi_max": not generic_nonconstant_successes,
        "analytic_constant_rows_present": sum(
            row["termination"] == "ANALYTIC_CONSTANT_GLOBAL"
            for row in shooting_rows
        )
        == 4,
        "all_boundary_roots_satisfy_fixed_equation": all(
            abs(float(row.get("boundary_residual", 0.0))) < 1.0e-9
            for row in shooting_rows
            if row["termination"] != "NO_REGULAR_BOUNDARY_ROOT"
        ),
        "fractional_direction_not_counted_as_regular_eigenoperator": all(
            not row["fractional_is_regular_eigenoperator"] for row in mes_rows
        ),
        "no_constant_root_meets_one_total_direction_gate": all(
            not row["one_total_relevant_direction_after_Newton_scale"]
            for row in root_rows
            if row["compatible_with_current_MES_v_branch"]
        ),
        "canonical_motion_Newton_scale_lock_is_RG_invariant": canonical_scale_lock_beta
        == 0,
    }
    if not all(checks.values()):
        raise RuntimeError(f"functional fixed gate checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "flow_definition": {
            "equation": "partial_t u=-4u+varphi u'+5/[24pi^2(1-u/w)]-1/(8pi^2)+(a+r_sigma b)/[32pi^2(a b+mu^2)]",
            "a": "1-u/(4w)",
            "b": "1+u''",
            "mu_squared": "3(u')^2/(4w)",
            "fixed_ODE": "b=(a-Y mu^2)/(Y a-r_sigma), u''=b-1",
            "Y": "32pi^2[4u-varphi u'-5/(24pi^2(1-u/w))+1/(8pi^2)]",
            "flat_O4_boundary": "C^2=0 on the constant flat background, so O4 does not alter this potential equation; its curved C^2 p^2 flow remains an independent unfrozen coordinate",
        },
        "source_scale_map": {
            "g_fixed_4934_4935": newton_fixed,
            "w_equals_1_over_16pi_g": dimensionless_planck,
            "existing_relevant_directions": existing_relevant_directions,
            "scheme_warning": "the physical-gauge absolute potential flow and the minimal-essential source point are compared through g and v, not silently declared one common beta system",
        },
        "constant_root_decision": {
            "roots": constant_roots,
            "low_branch": "MES-adjacent and pole-regular, but its even scalar mass direction is relevant in both regulator normalizations",
            "high_branch": "scalar directions are irrelevant, but v is about 0.964, only about 3.6 percent below the TT pole and incompatible with the small-|v| minimal-essential branch",
            "linear_operator": "delta beta=(-4+A)delta u+varphi delta u'-(1/32pi^2)delta u''; the second derivative lowers polynomial degree and leaves triangular eigenvalues lambda_n=-4+A+n",
            "critical_exponents": "theta_n=4-A-n for regular polynomial eigenoperators",
            "fractional_warning": "n=4/3 gives only a formal diagonal exponent; |varphi|^(4/3) is not a regular eigenoperator because delta u'' produces |varphi|^(-2/3)",
        },
        "minimal_essential_sign_robustness": mes_rows,
        "shooting_gate": {
            "mass_range": [min(MASS_SCAN), max(MASS_SCAN)],
            "mass_samples": list(MASS_SCAN),
            "field_target": PHI_MAX,
            "generic_nonconstant_reaches_target": len(generic_nonconstant_successes),
            "analytic_global_solutions": "the two constant roots in each normalization",
            "compatibility_boundaries": compatibility_rows,
            "interpretation": "generic nonconstant analytic shots terminate at a movable ODE denominator, the TT barrier, or runaway. Fine-tuned termination transitions occur at finite field and are not counted as global fixed functions without a derived smooth continuation and large-field boundary.",
            "scope": "numerical gate in the declared optimized LPA physical block, not a regulator-independent theorem against every enlarged MTS functional",
        },
        "predictivity_decision": {
            "unchanged_parent_one_scale_fixed_function": False,
            "reason": "the MES-connected low branch adds a relevant motion mass direction; the only constant branch with irrelevant scalar directions is near the graviton barrier and not MES-compatible; no scanned nonconstant branch satisfies the global gate",
            "minimum_relevant_directions_on_MES_connected_low_branch": 2,
            "ways_forward": [
                "derive a parent identity locking the motion scale to Newton's scale",
                "accept and calibrate an explicit second essential scale",
                "derive an enlarged nonminimal field-space or derivative sector whose global fixed function changes the spectrum",
            ],
            "selected_next": "parent motion-scale/Newton-scale identity before adding phenomenological profile closures",
        },
        "scale_lock_contract": {
            "dimensionless_invariant": "I_M=gtilde_psi g^(4/3)=g_psi G_N^(4/3)",
            "mass_ratio": "m_gap sqrt(G_N)=c_m I_M^(3/8)",
            "full_flow_condition": "beta_I/I=beta_gtilde_psi/gtilde_psi+(4/3)beta_g/g=0",
            "canonical_Gaussian_value": str(canonical_scale_lock_beta),
            "interpretation": "canonical dimensions preserve I_M, but do not select its value; one-scale predictivity requires the coupled fixed point or a parent identity to fix I_M and c_m rather than treating them as independent data",
        },
        "checks": checks,
        "claim_boundary": {
            "declared_functional_flow_solved_at_constant_roots": True,
            "regular_linear_spectrum_derived": True,
            "MES_sign_robust_mass_relevance_derived": True,
            "global_nonconstant_no_go_theorem": False,
            "one_scale_MTS_fixed_function_derived": False,
            "O4_beta_frozen_to_zero": False,
            "full_MTS_fixed_point_and_trajectory": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(ROOT_OUTPUT, root_rows)
    write_csv(MES_OUTPUT, mes_rows)
    write_csv(SHOOTING_OUTPUT, shooting_rows)
    write_csv(COMPATIBILITY_OUTPUT, compatibility_rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_ROOTS_SHA256={digest(ROOT_OUTPUT)}", flush=True)
    print(f"{MARKER}_MES_SHA256={digest(MES_OUTPUT)}", flush=True)
    print(f"{MARKER}_SHOOTING_SHA256={digest(SHOOTING_OUTPUT)}", flush=True)
    print(f"{MARKER}_COMPATIBILITY_SHA256={digest(COMPATIBILITY_OUTPUT)}", flush=True)
    print(f"{MARKER}_W={dimensionless_planck:.15g}", flush=True)
    print(f"{MARKER}_NONCONSTANT_GLOBAL={len(generic_nonconstant_successes)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
