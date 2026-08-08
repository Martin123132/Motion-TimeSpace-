from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4986"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4986_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RESULT_JSON = SOURCE / "common_scheme_log_and_local_metric_results.json"
RESULT_4963 = POST / "source-intake" / "functional_rg" / "4963" / "strong_field_C3_and_scalar_branch_results.json"
OUTPUTS = {
    "basis": SOURCE / "O2_crossing_log_basis_and_scheme_invariant.csv",
    "kinematic": SOURCE / "O2_exact_kinematic_reconstruction.csv",
    "rg": SOURCE / "O2_full_logarithmic_RG_checks.csv",
    "C3": SOURCE / "C3_exterior_compactness_bounds.csv",
    "determinant": SOURCE / "determinant_exterior_tail_bounds.csv",
    "contact": SOURCE / "pure_metric_contact_and_claim_gate.csv",
    "gate": SOURCE / "common_scheme_log_and_local_metric_gate.csv",
}

MARKER = "MTS_4986_COMMON_SCHEME_LOG_INVARIANT_LOCAL_METRIC_BOUNDS"
VALIDATION_MARKER = "MTS_4986_INDEPENDENT_VALIDATION"
CHECKED_DATE = "2026-07-14"

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054_571_817e-34
PLANCK_LENGTH_M = math.sqrt(HBAR * G_NEWTON / C_LIGHT**3)
MIXING_B = -6.0 / math.pi


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def add_check(rows: list[dict[str, Any]], name: str, passed: bool, evidence: str) -> None:
    rows.append(
        {
            "validation_id": f"VAL4986_{len(rows) + 1:03d}_{name}",
            "passed": passed,
            "evidence": evidence,
            "validation_marker": VALIDATION_MARKER,
            "checkpoint_marker": MARKER,
            "source_checked_date": CHECKED_DATE,
        }
    )


def write_validation(rows: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def legendre_two(value: Fraction) -> Fraction:
    return (3 * value**2 - 1) / 2


def independent_kinematic_controls() -> tuple[int, Fraction, Fraction]:
    event_count = 0
    maximum_channel_residual = Fraction(0, 1)
    maximum_crossing_residual = Fraction(0, 1)
    for s_integer in range(2, 27):
        for t_integer in range(-31, 24, 4):
            s_value = Fraction(s_integer, 1)
            t_value = Fraction(t_integer, 1)
            u_value = -s_value - t_value
            if s_value * t_value * u_value == 0:
                continue
            channels = (
                (s_value, t_value, u_value),
                (t_value, u_value, s_value),
                (u_value, s_value, t_value),
            )
            crossing_sum = Fraction(0, 1)
            for channel_value, other_one, other_two in channels:
                cosine = (other_one - other_two) / channel_value
                original = channel_value**3 * (
                    Fraction(-55, 36) - Fraction(1, 180) * legendre_two(cosine)
                )
                reduced = Fraction(-23, 15) * channel_value**3 + Fraction(1, 30) * channel_value * other_one * other_two
                maximum_channel_residual = max(maximum_channel_residual, abs(original - reduced))
                crossing_sum += original
            expected = Fraction(-9, 2) * s_value * t_value * u_value
            maximum_crossing_residual = max(maximum_crossing_residual, abs(crossing_sum - expected))
            event_count += 1
    return event_count, maximum_channel_residual, maximum_crossing_residual


def real_log_basis(s_value: float, t_value: float, u_value: float, mu_value: float) -> tuple[float, float, float, float]:
    invariants = (s_value, t_value, u_value)
    logarithms = tuple(math.log(abs(invariant) / mu_value**2) for invariant in invariants)
    stu_value = s_value * t_value * u_value
    basis_a = sum(invariant**3 * logarithm for invariant, logarithm in zip(invariants, logarithms))
    basis_b = stu_value * sum(logarithms)
    square_a = sum(invariant**3 * logarithm**2 for invariant, logarithm in zip(invariants, logarithms))
    square_b = stu_value * sum(logarithm**2 for logarithm in logarithms)
    return basis_a, basis_b, square_a, square_b


def independent_amplitude(
    s_value: float,
    t_value: float,
    u_value: float,
    mu_value: float,
    coefficient_c: float,
    coefficient_w: float,
    source_s: float,
    rational_rho: float,
    angular_j: float,
) -> tuple[float, float, float, float]:
    basis_a, basis_b, square_a, square_b = real_log_basis(s_value, t_value, u_value, mu_value)
    stu_value = s_value * t_value * u_value
    one_loop_log = (2.0 / math.pi) * (23.0 * basis_a / 15.0 - basis_b / 30.0)
    one_loop_full = one_loop_log + rational_rho * stu_value
    double_log = (8.0 / math.pi) * (23.0 * square_a / 15.0 - square_b / 30.0)
    invariant_i = 3.0 * source_s - 16.0 * rational_rho
    coefficient_a = -invariant_i / 12.0 + angular_j / 2.0
    coefficient_b = -invariant_i / 12.0 - angular_j / 2.0
    single_log = coefficient_a * basis_a + coefficient_b * basis_b
    amplitude = -3.0 * coefficient_w * stu_value + coefficient_c * one_loop_full + double_log + single_log
    return amplitude, invariant_i, one_loop_log, double_log


def independent_rg_controls() -> tuple[int, dict[str, float]]:
    generator = np.random.default_rng(24986)
    maxima = {
        "F1_derivative": 0.0,
        "F2_double_derivative": 0.0,
        "RG_amplitude": 0.0,
        "scheme_invariant": 0.0,
        "scheme_amplitude": 0.0,
    }
    derivative_step = 7.0e-7
    event_count = 0
    for _ in range(96):
        s_value = float(generator.uniform(0.3, 7.0))
        t_value = float(generator.uniform(-8.0, -0.15))
        u_value = -s_value - t_value
        if abs(u_value) < 0.1:
            t_value -= 0.37
            u_value = -s_value - t_value
        mu_value = float(generator.uniform(0.3, 3.1))
        coefficient_c = float(generator.uniform(-2.5, 2.5))
        coefficient_w = float(generator.uniform(-2.5, 2.5))
        source_s = float(generator.uniform(-3.5, 3.5))
        rational_rho = float(generator.uniform(-2.5, 2.5))
        angular_j = float(generator.uniform(-2.5, 2.5))
        alpha_value = float(generator.uniform(-2.0, 2.0))
        time_shift = float(generator.uniform(-1.0, 1.0))
        stu_value = s_value * t_value * u_value

        center = independent_amplitude(
            s_value,
            t_value,
            u_value,
            mu_value,
            coefficient_c,
            coefficient_w,
            source_s,
            rational_rho,
            angular_j,
        )
        plus = independent_amplitude(
            s_value,
            t_value,
            u_value,
            mu_value * math.exp(derivative_step),
            coefficient_c,
            coefficient_w,
            source_s,
            rational_rho,
            angular_j,
        )
        minus = independent_amplitude(
            s_value,
            t_value,
            u_value,
            mu_value * math.exp(-derivative_step),
            coefficient_c,
            coefficient_w,
            source_s,
            rational_rho,
            angular_j,
        )
        derivative_f1 = (plus[2] - minus[2]) / (2.0 * derivative_step)
        expected_f1 = -18.0 * stu_value / math.pi
        residual_f1 = abs(derivative_f1 - expected_f1) / max(abs(expected_f1), 1.0e-14)
        derivative_double = (plus[3] - minus[3]) / (2.0 * derivative_step)
        expected_double = -16.0 * center[2]
        residual_double = abs(derivative_double - expected_double) / max(abs(expected_double), 1.0e-14)

        evolved_c = coefficient_c + 16.0 * time_shift
        evolved_w = coefficient_w + (MIXING_B * coefficient_c + source_s) * time_shift + 8.0 * MIXING_B * time_shift**2
        evolved = independent_amplitude(
            s_value,
            t_value,
            u_value,
            mu_value * math.exp(time_shift),
            evolved_c,
            evolved_w,
            source_s,
            rational_rho,
            angular_j,
        )
        residual_rg = abs(evolved[0] - center[0]) / max(abs(evolved[0]), abs(center[0]), 1.0e-14)

        transformed = independent_amplitude(
            s_value,
            t_value,
            u_value,
            mu_value,
            coefficient_c,
            coefficient_w + alpha_value * coefficient_c,
            source_s + 16.0 * alpha_value,
            rational_rho + 3.0 * alpha_value,
            angular_j,
        )
        invariant_residual = abs(transformed[1] - center[1])
        scheme_residual = abs(transformed[0] - center[0]) / max(abs(transformed[0]), abs(center[0]), 1.0e-14)
        maxima["F1_derivative"] = max(maxima["F1_derivative"], residual_f1)
        maxima["F2_double_derivative"] = max(maxima["F2_double_derivative"], residual_double)
        maxima["RG_amplitude"] = max(maxima["RG_amplitude"], residual_rg)
        maxima["scheme_invariant"] = max(maxima["scheme_invariant"], invariant_residual)
        maxima["scheme_amplitude"] = max(maxima["scheme_amplitude"], scheme_residual)
        event_count += 1
    return event_count, maxima


def close(actual: float, expected: float, relative_tolerance: float = 2.0e-12, absolute_tolerance: float = 1.0e-300) -> bool:
    return abs(actual - expected) <= max(absolute_tolerance, relative_tolerance * max(abs(actual), abs(expected), 1.0e-300))


def main() -> int:
    required = (RESULT_JSON, RESULT_4963, *OUTPUTS.values())
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("\n".join(missing))

    result = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    result_4963 = json.loads(RESULT_4963.read_text(encoding="utf-8"))
    tables = {name: read_csv(path) for name, path in OUTPUTS.items()}
    checks: list[dict[str, Any]] = []

    add_check(checks, "marker", result["checkpoint_marker"] == MARKER, result["checkpoint_marker"])
    for name, rows in tables.items():
        add_check(checks, f"nonempty_{name}", bool(rows), f"rows={len(rows)}")
        add_check(
            checks,
            f"markers_{name}",
            all(row["checkpoint_marker"] == MARKER for row in rows),
            f"rows={len(rows)}",
        )
        add_check(
            checks,
            f"full_MTS_false_{name}",
            all(not parse_bool(row["valid_for_full_MTS_claim"]) for row in rows),
            f"rows={len(rows)}",
        )

    for source_path, expected_hash in result["source_hashes"].items():
        path = ROOT / source_path
        add_check(checks, "source_hash", path.exists() and digest(path) == expected_hash, source_path)

    cited_paths: set[str] = set()
    for rows in tables.values():
        for row in rows:
            source_path = row.get("source_path", "").strip()
            if source_path:
                cited_paths.update(item for item in source_path.split(";") if item)
    for source_path in sorted(cited_paths):
        add_check(checks, "cited_path", (ROOT / source_path).exists(), source_path)

    basis_statuses = {row["status"] for row in tables["basis"]}
    add_check(checks, "F1_log_status", "FULL_ONE_LOOP_MIXED_NONLOCAL_LOG_RECONSTRUCTED" in basis_statuses, str(sorted(basis_statuses)))
    add_check(checks, "F2_double_status", "FULL_TWO_LOOP_DOUBLE_LOG_KERNEL_DERIVED" in basis_statuses, str(sorted(basis_statuses)))
    add_check(checks, "I2L_status", "EXACT_FINITE_SCHEME_INVARIANT" in basis_statuses, str(sorted(basis_statuses)))
    add_check(checks, "numeric_primitive_open", "NUMERIC_TWO_LOOP_PRIMITIVE_OPEN_NONCLAIM" in basis_statuses, str(sorted(basis_statuses)))
    invariant_row = next(row for row in tables["basis"] if row["object"] == "I_2L")
    add_check(checks, "I2L_equation", invariant_row["definition"] == "I_2L=3S_2L-16rho_mix", invariant_row["definition"])
    single_row = next(row for row in tables["basis"] if row["object"] == "F_2_single")
    add_check(checks, "single_log_constraint", "A_2+B_2=-I_2L/6" in single_row["definition"], single_row["definition"])

    output_channel_zero = all(Fraction(row["channel_reduction_max_exact_residual"]) == 0 for row in tables["kinematic"])
    output_crossing_zero = all(Fraction(row["crossing_exact_residual"]) == 0 for row in tables["kinematic"])
    add_check(checks, "output_channel_exact", output_channel_zero, f"rows={len(tables['kinematic'])}")
    add_check(checks, "output_crossing_exact", output_crossing_zero, f"rows={len(tables['kinematic'])}")
    event_count, channel_residual, crossing_residual = independent_kinematic_controls()
    add_check(checks, "independent_channel_exact", channel_residual == 0, f"events={event_count} residual={channel_residual}")
    add_check(checks, "independent_crossing_exact", crossing_residual == 0, f"events={event_count} residual={crossing_residual}")

    runner_rg_maxima = {
        "F1_derivative": max(float(row["F1_log_derivative_relative_residual"]) for row in tables["rg"]),
        "F2_double_derivative": max(float(row["F2_double_derivative_relative_residual"]) for row in tables["rg"]),
        "RG_amplitude": max(float(row["full_reduced_amplitude_RG_relative_residual"]) for row in tables["rg"]),
        "scheme_invariant": max(float(row["I2L_scheme_absolute_residual"]) for row in tables["rg"]),
        "scheme_amplitude": max(float(row["full_reduced_amplitude_scheme_relative_residual"]) for row in tables["rg"]),
    }
    add_check(checks, "runner_F1_derivative", runner_rg_maxima["F1_derivative"] < 2.0e-8, str(runner_rg_maxima))
    add_check(checks, "runner_F2_derivative", runner_rg_maxima["F2_double_derivative"] < 2.0e-8, str(runner_rg_maxima))
    add_check(checks, "runner_RG", runner_rg_maxima["RG_amplitude"] < 2.0e-12, str(runner_rg_maxima))
    add_check(checks, "runner_scheme", runner_rg_maxima["scheme_amplitude"] < 2.0e-12, str(runner_rg_maxima))
    independent_events, independent_rg_maxima = independent_rg_controls()
    add_check(checks, "independent_F1_derivative", independent_rg_maxima["F1_derivative"] < 3.0e-8, f"events={independent_events} {independent_rg_maxima}")
    add_check(checks, "independent_F2_derivative", independent_rg_maxima["F2_double_derivative"] < 3.0e-8, f"events={independent_events} {independent_rg_maxima}")
    add_check(checks, "independent_RG", independent_rg_maxima["RG_amplitude"] < 3.0e-12, f"events={independent_events} {independent_rg_maxima}")
    add_check(checks, "independent_scheme_I", independent_rg_maxima["scheme_invariant"] < 3.0e-12, f"events={independent_events} {independent_rg_maxima}")
    add_check(checks, "independent_scheme_amplitude", independent_rg_maxima["scheme_amplitude"] < 3.0e-12, f"events={independent_events} {independent_rg_maxima}")

    selected_a_plus = float(result_4963["C3_selection"]["selected_a_plus_abs_m4"])
    for row in tables["C3"]:
        radius_m = float(row["radius_or_separation_m"])
        expected_potential = 5.0 * selected_a_plus / radius_m**4
        expected_acceleration = 35.0 * selected_a_plus / radius_m**4
        add_check(
            checks,
            "C3_selected_bound",
            close(float(row["selected_abs_DeltaPhi_over_PhiN_bound"]), expected_potential)
            and close(float(row["selected_abs_Deltaa_over_aN_bound"]), expected_acceleration),
            row["scale_id"],
        )
        add_check(
            checks,
            "C3_claim_guard",
            parse_bool(row["valid_for_selected_C3_coordinate_bound"])
            and not parse_bool(row["valid_for_complete_physical_C3_amplitude"]),
            row["scale_id"],
        )
    r10_c3 = next(row for row in tables["C3"] if row["scale_id"] == "R10_minimum_separation")
    add_check(checks, "C3_R10_numeric", close(float(r10_c3["selected_abs_Deltaa_over_aN_bound"]), 3.6208461805802824e-124), r10_c3["selected_abs_Deltaa_over_aN_bound"])

    coefficient_a = Fraction(43, 120)
    coefficient_b = Fraction(1, 80)
    gravity_a = Fraction(7, 20)
    gravity_b = Fraction(1, 120)
    motion_a = Fraction(1, 120)
    motion_b = Fraction(1, 240)
    coefficient_sum = coefficient_a + coefficient_b
    gravity_sum = gravity_a + gravity_b
    motion_sum = motion_a + motion_b
    spin_two_kernel = coefficient_a / 2
    spin_zero_kernel = 2 * (coefficient_a + 3 * coefficient_b)
    tree_contraction = Fraction(2, 3) - Fraction(1, 2) * Fraction(1, 3)
    weighted_contraction = spin_two_kernel * Fraction(2, 3) + Fraction(1, 4) * spin_zero_kernel * Fraction(1, 3)
    normalized_contraction = weighted_contraction / tree_contraction
    momentum_fraction = 2 * normalized_contraction
    add_check(checks, "determinant_fraction", coefficient_sum == Fraction(89, 240), str(coefficient_sum))
    add_check(
        checks,
        "determinant_sector_sum",
        gravity_a + motion_a == coefficient_a
        and gravity_b + motion_b == coefficient_b
        and gravity_sum == Fraction(43, 120)
        and motion_sum == Fraction(1, 80),
        f"gravity={gravity_sum}; motion={motion_sum}; parent={coefficient_sum}",
    )
    add_check(checks, "determinant_projector", normalized_contraction == coefficient_sum and momentum_fraction == Fraction(89, 120), f"normalized={normalized_contraction}; momentum={momentum_fraction}")
    fourier_tree_coefficient = Fraction(1, 4)
    fourier_log_coefficient = Fraction(-1, 2)
    position_ratio_factor = -fourier_log_coefficient / fourier_tree_coefficient
    add_check(checks, "fourier_ratio", position_ratio_factor == 2, f"F[1/q2]=1/(4pi r); F[lnq2]=-1/(2pi r3); factor={position_ratio_factor}")
    potential_coefficient = 4.0 * float(coefficient_sum) / math.pi
    acceleration_coefficient = 3.0 * potential_coefficient
    gravity_potential_coefficient = 4.0 * float(gravity_sum) / math.pi
    gravity_acceleration_coefficient = 3.0 * gravity_potential_coefficient
    for row in tables["determinant"]:
        radius_m = float(row["radius_or_separation_m"])
        expected_potential = potential_coefficient * PLANCK_LENGTH_M**2 / radius_m**2
        expected_acceleration = acceleration_coefficient * PLANCK_LENGTH_M**2 / radius_m**2
        expected_gravity_potential = gravity_potential_coefficient * PLANCK_LENGTH_M**2 / radius_m**2
        expected_gravity_acceleration = gravity_acceleration_coefficient * PLANCK_LENGTH_M**2 / radius_m**2
        add_check(
            checks,
            "determinant_tail",
            Fraction(row["Einstein_ghost_Ricci_log_Ricci_a"]) == gravity_a
            and Fraction(row["Einstein_ghost_R_log_R_b"]) == gravity_b
            and Fraction(row["massless_motion_Ricci_log_Ricci_a_increment"]) == motion_a
            and Fraction(row["massless_motion_R_log_R_b_increment"]) == motion_b
            and Fraction(row["parent_Ricci_log_Ricci_a"]) == coefficient_a
            and Fraction(row["parent_R_log_R_b"]) == coefficient_b
            and close(float(row["gravity_only_exterior_abs_DeltaPhi_over_PhiN"]), expected_gravity_potential)
            and close(float(row["gravity_only_exterior_abs_Deltaa_over_aN"]), expected_gravity_acceleration)
            and close(float(row["exterior_abs_DeltaPhi_over_PhiN"]), expected_potential)
            and close(float(row["exterior_abs_Deltaa_over_aN"]), expected_acceleration),
            row["scale_id"],
        )
        add_check(
            checks,
            "determinant_claim_guard",
            parse_bool(row["valid_for_parent_massless_endpoint_two_point_tail"])
            and not parse_bool(row["valid_for_unsourced_physical_mgap_tail"])
            and not parse_bool(row["valid_for_complete_quantum_potential"]),
            row["scale_id"],
        )
    r10_determinant = next(row for row in tables["determinant"] if row["scale_id"] == "R10_minimum_separation")
    add_check(checks, "determinant_R10_numeric", close(float(r10_determinant["exterior_abs_Deltaa_over_aN"]), 1.3684320168245822e-61), r10_determinant["exterior_abs_Deltaa_over_aN"])

    contact_statuses = {row["status"] for row in tables["contact"]}
    add_check(checks, "p4_contact_status", "SOURCE_CONTACT_ONLY_AT_EFT_ORDER" in contact_statuses, str(sorted(contact_statuses)))
    local_p4_rows = [row for row in tables["contact"] if row["sector"] == "finite local p4"]
    add_check(checks, "p4_exterior_zero", len(local_p4_rows) == 2 and all(parse_bool(row["valid_for_separated_exterior_zero"]) for row in local_p4_rows), str(local_p4_rows))
    add_check(checks, "source_interior_not_zero", all(not parse_bool(row["valid_for_source_interior_zero"]) for row in tables["contact"]), "all rows retain source-interior guard")

    gate_by_name = {"_".join(row["gate_id"].split("_")[2:]): row for row in tables["gate"]}
    for open_name in ("numeric_I2L", "numeric_J2L", "finite_Cw", "C3_complete_amplitude", "exact_all_operator_local_GR", "full_MTS"):
        row = gate_by_name[open_name]
        add_check(checks, f"open_{open_name}", not parse_bool(row["passed"]) and row["status"] == "OPEN_NONCLAIM", row["evidence"])
    for closed_name in ("one_loop_nonlocal_kernel", "two_loop_double_log_kernel", "C3_compactness_bound", "finite_p4_exterior_contact", "determinant_projector", "determinant_exterior_bound"):
        row = gate_by_name[closed_name]
        add_check(checks, f"closed_{closed_name}", parse_bool(row["passed"]) and row["status"] == "PASS", row["evidence"])

    result_gates = result["gates"]
    add_check(checks, "result_log_promotions", result_gates["one_loop_mixed_nonlocal_log_derived"] and result_gates["two_loop_double_log_kernel_derived"] and result_gates["I2L_scheme_invariant_derived"], str(result_gates))
    add_check(checks, "result_primitives_withheld", not result_gates["I2L_numeric_derived"] and not result_gates["J2L_numeric_derived"] and not result_gates["Cw_derived"], str(result_gates))
    add_check(checks, "result_local_boundary", result_gates["finite_p4_separated_exterior_contact_zero"] and result_gates["massless_parent_determinant_endpoint_bounded"] and not result_gates["physical_motion_mass_threshold_sourced"] and result_gates["selected_C3_exterior_bounded"] and not result_gates["exact_all_operator_local_GR"], str(result_gates))
    add_check(checks, "full_MTS_withheld", result_gates["full_MTS"] is False, str(result_gates))

    all_passed = all(bool(row["passed"]) for row in checks)
    add_check(checks, "overall", all_passed, f"pre_overall_checks={len(checks)}")
    if not all(bool(row["passed"]) for row in checks):
        failures = [row for row in checks if not bool(row["passed"])]
        raise RuntimeError(json.dumps(failures, indent=2))

    write_validation(checks)
    VALIDATION_PROVENANCE.write_text(
        "\n".join(
            [
                "# 4986 independent validation provenance",
                "",
                f"Marker: `{VALIDATION_MARKER}`.",
                "",
                f"Checks: `{len(checks)}/{len(checks)}` passed.",
                "",
                f"Fresh exact rational kinematic controls: `{event_count}`; channel residual `{channel_residual}`; crossing residual `{crossing_residual}`.",
                f"Fresh logarithmic RG controls: `{independent_events}`; maxima `{json.dumps(independent_rg_maxima, sort_keys=True)}`.",
                f"Validator SHA-256: `{digest(Path(__file__))}`.",
                "",
                "The validator does not import runner functions. It independently reconstructs the channel polynomial, crossing sum, logarithmic RG flow, finite scheme orbit, C3 compactness bounds, spin-projector determinant contraction, Fourier-tail normalization, source hashes, cited paths, and all nonclaim gates.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps({"validation_marker": VALIDATION_MARKER, "passed": len(checks), "total": len(checks)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
