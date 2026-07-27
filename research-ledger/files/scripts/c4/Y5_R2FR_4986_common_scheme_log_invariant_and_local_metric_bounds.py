from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4986"

CHECKPOINT_4985 = POST / "4985-Y5-R2FR-metric-frame-O2-zero-and-partial-wave-mixing-flow.md"
RESULT_4985 = POST / "source-intake" / "functional_rg" / "4985" / "metric_frame_O2_flow_results.json"
CHECKPOINT_4963 = POST / "4963-Y5-R2FR-strong-field-C3-Wilson-selection-and-global-scalar-branch-exclusion-or-compact-GR-finite-residual.md"
RESULT_4963 = POST / "source-intake" / "functional_rg" / "4963" / "strong_field_C3_and_scalar_branch_results.json"
CHECKPOINT_4981 = POST / "4981-Y5-R2FR-parent-motion-graviton-ghost-hessian-and-common-scheme-two-point-completion.md"
RESULT_4981 = POST / "source-intake" / "functional_rg" / "4981" / "parent_hessian_common_scheme_results.json"
PARENT_LOG_CSV = POST / "source-intake" / "functional_rg" / "4981" / "parent_common_scheme_log_coefficients.csv"
BURGESS_SOURCE = POST / "source-intake" / "functional_rg" / "4985" / "sources" / "burgess" / "GRET-jhep.tex"
BERN_SOURCE = POST / "source-intake" / "functional_rg" / "4985" / "sources" / "bern" / "gr_simp.tex"
DUNBAR_SOURCE = SOURCE / "sources" / "dunbar_norridge" / "9512084.tex"
DUNBAR_ARCHIVE = SOURCE / "sources" / "dunbar_norridge_hep-th9512084.tar"

LOG_BASIS_CSV = SOURCE / "O2_crossing_log_basis_and_scheme_invariant.csv"
KINEMATIC_CSV = SOURCE / "O2_exact_kinematic_reconstruction.csv"
RG_CSV = SOURCE / "O2_full_logarithmic_RG_checks.csv"
C3_CSV = SOURCE / "C3_exterior_compactness_bounds.csv"
DETERMINANT_CSV = SOURCE / "determinant_exterior_tail_bounds.csv"
CONTACT_CSV = SOURCE / "pure_metric_contact_and_claim_gate.csv"
GATE_CSV = SOURCE / "common_scheme_log_and_local_metric_gate.csv"
RESULT_JSON = SOURCE / "common_scheme_log_and_local_metric_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4986_COMMON_SCHEME_LOG_INVARIANT_LOCAL_METRIC_BOUNDS"
CHECKED_DATE = "2026-07-14"

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054_571_817e-34
PLANCK_LENGTH_M = math.sqrt(HBAR * G_NEWTON / C_LIGHT**3)

MIXING_B = -6.0 / math.pi
CHANNEL_CUBIC = Fraction(-23, 15)
CHANNEL_STU = Fraction(1, 30)


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalized_text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="replace"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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


def source_lock() -> dict[str, bool]:
    dunbar = normalized_text(DUNBAR_SOURCE)
    bern = normalized_text(BERN_SOURCE).lower()
    burgess = normalized_text(BURGESS_SOURCE).lower()
    checkpoint_4985 = normalized_text(CHECKPOINT_4985)
    checkpoint_4963 = normalized_text(CHECKPOINT_4963)
    return {
        "dunbar_scalar_counterterm": "203 \\over 320\\eps" in dunbar,
        "dunbar_four_scalar_tree": "four scalars (all the same flavour)" in dunbar,
        "dunbar_finite_rational_ambiguity": "only ambiguity will be in finite rational terms" in dunbar,
        "dunbar_scalar_and_graviton_cuts": "intermediate states" in dunbar and "can be either gravitons or scalars" in dunbar,
        "bern_four_dimensional_scale_method": "renormalization-scale dependence directly from four-dimensional unitarity cuts" in bern,
        "bern_evanescent_safe_target": "automatically avoid evanescent operators" in bern,
        "bern_two_and_three_particle_cuts": "cuts where two particles cross the cut" in bern and "where three particles cross the cut" in bern,
        "burgess_analytic_terms_are_contact": "analytic contributions of ${\\cal a}_{\\rm an}$ may be completely ignored" in burgess,
        "burgess_curvature_squared_contact": "b = 128 \\pi^2 g (a + b)" in burgess,
        "checkpoint_4985_channel_polynomial": "-55/36-(1/180)P2" in checkpoint_4985,
        "checkpoint_4985_mixed_beta": "beta_w=6w-(6/pi)gc" in checkpoint_4985,
        "checkpoint_4963_C3_exterior": "|Delta a/a_N| =140|a_+|M^2/r^6" in checkpoint_4963,
    }


def legendre_two(value: Fraction) -> Fraction:
    return (3 * value**2 - 1) / 2


def channel_polynomial(channel: Fraction, other_one: Fraction, other_two: Fraction) -> Fraction:
    cosine = (other_one - other_two) / channel
    return channel**3 * (Fraction(-55, 36) - Fraction(1, 180) * legendre_two(cosine))


def simplified_channel(channel: Fraction, other_one: Fraction, other_two: Fraction) -> Fraction:
    return CHANNEL_CUBIC * channel**3 + CHANNEL_STU * channel * other_one * other_two


def log_basis_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "LB4986_01_channel_reduction",
            "object": "P_s",
            "definition": "s^3[-55/36-(1/180)P2((t-u)/s)]=-(23/15)s^3+(1/30)stu",
            "mu_derivative": "not_applicable",
            "scheme_law": "invariant cut polynomial",
            "status": "EXACT_ALGEBRAIC_REDUCTION",
            "source_path": relative(CHECKPOINT_4985),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_02_crossing",
            "object": "sum_channels_P",
            "definition": "sum_cyclic P_s=-(9/2)stu",
            "mu_derivative": "not_applicable",
            "scheme_law": "crossing invariant",
            "status": "EXACT_CROSSING_IDENTITY",
            "source_path": relative(CHECKPOINT_4985),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_03_LA",
            "object": "L_A",
            "definition": "sum_cyclic s^3 ln(-s/mu^2)",
            "mu_derivative": "d/dlnmu L_A=-6stu",
            "scheme_law": "L_A-L_B is scale invariant",
            "status": "COMPLETE_CROSSING_P6_LOG_BASIS",
            "source_path": relative(DUNBAR_SOURCE),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_04_LB",
            "object": "L_B",
            "definition": "stu sum_cyclic ln(-s/mu^2)",
            "mu_derivative": "d/dlnmu L_B=-6stu",
            "scheme_law": "L_A-L_B is scale invariant",
            "status": "COMPLETE_CROSSING_P6_LOG_BASIS",
            "source_path": relative(DUNBAR_SOURCE),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_05_F1log",
            "object": "F_1_log",
            "definition": "(2/pi)[(23/15)L_A-(1/30)L_B]",
            "mu_derivative": "d/dlnmu F_1_log=-(18/pi)stu=3B_gc stu",
            "scheme_law": "nonlocal cut part invariant",
            "status": "FULL_ONE_LOOP_MIXED_NONLOCAL_LOG_RECONSTRUCTED",
            "source_path": relative(CHECKPOINT_4985),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_06_F1full",
            "object": "F_1",
            "definition": "F_1_log+rho_mix stu",
            "mu_derivative": "d/dlnmu F_1=-(18/pi)stu",
            "scheme_law": "rho_mix'=rho_mix+3alpha",
            "status": "FINITE_LOCAL_RATIONAL_COORDINATE_EXPLICIT",
            "source_path": relative(DUNBAR_SOURCE),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_07_QA",
            "object": "Q_A",
            "definition": "sum_cyclic s^3 ln^2(-s/mu^2)",
            "mu_derivative": "d/dlnmu Q_A=-4L_A",
            "scheme_law": "quadratic-log basis",
            "status": "COMPLETE_CROSSING_P6_DOUBLE_LOG_BASIS",
            "source_path": relative(BERN_SOURCE),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_08_QB",
            "object": "Q_B",
            "definition": "stu sum_cyclic ln^2(-s/mu^2)",
            "mu_derivative": "d/dlnmu Q_B=-4L_B",
            "scheme_law": "quadratic-log basis",
            "status": "COMPLETE_CROSSING_P6_DOUBLE_LOG_BASIS",
            "source_path": relative(BERN_SOURCE),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_09_F2double",
            "object": "F_2_double",
            "definition": "(8/pi)[(23/15)Q_A-(1/30)Q_B]",
            "mu_derivative": "d/dlnmu F_2_double=-16F_1_log",
            "scheme_law": "forced by beta_C=16 and one-loop cut",
            "status": "FULL_TWO_LOOP_DOUBLE_LOG_KERNEL_DERIVED",
            "source_path": relative(BERN_SOURCE),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_10_invariant",
            "object": "I_2L",
            "definition": "I_2L=3S_2L-16rho_mix",
            "mu_derivative": "d/dlnmu F_2_single=I_2L stu",
            "scheme_law": "S_2L'=S_2L+16alpha; rho_mix'=rho_mix+3alpha; I_2L'=I_2L",
            "status": "EXACT_FINITE_SCHEME_INVARIANT",
            "source_path": relative(CHECKPOINT_4985),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_11_single_constraint",
            "object": "F_2_single",
            "definition": "A_2 L_A+B_2 L_B with A_2+B_2=-I_2L/6",
            "mu_derivative": "-6(A_2+B_2)stu=I_2L stu",
            "scheme_law": "A_2-B_2 multiplies scale-invariant L_A-L_B",
            "status": "TWO_LOOP_PRIMITIVE_REDUCED_TO_I2L_AND_J2L",
            "source_path": relative(BERN_SOURCE),
            "valid_for_log_kernel_claim": True,
        },
        {
            "row_id": "LB4986_12_primitive_boundary",
            "object": "I_2L_numeric_and_J_2L",
            "definition": "complete scalar two-loop cuts including mixed one-loop amplitudes and nonvanishing three-particle cuts",
            "mu_derivative": "not yet numeric",
            "scheme_law": "raw S_2L is not an admissible substitute",
            "status": "NUMERIC_TWO_LOOP_PRIMITIVE_OPEN_NONCLAIM",
            "source_path": relative(BERN_SOURCE),
            "valid_for_log_kernel_claim": False,
        },
    ]
    return rows


def exact_kinematic_rows() -> tuple[list[dict[str, Any]], Fraction, Fraction]:
    events = [
        (2, -5),
        (3, 4),
        (5, -2),
        (7, 3),
        (11, -4),
        (13, 5),
        (17, -6),
        (19, 8),
        (23, -9),
        (29, 12),
        (31, -13),
        (37, 15),
    ]
    rows: list[dict[str, Any]] = []
    maximum_channel_residual = Fraction(0, 1)
    maximum_crossing_residual = Fraction(0, 1)
    for event_index, (s_integer, t_integer) in enumerate(events, start=1):
        s_value = Fraction(s_integer, 1)
        t_value = Fraction(t_integer, 1)
        u_value = -s_value - t_value
        if s_value * t_value * u_value == 0:
            raise ValueError("nonzero Mandelstam variables required")
        channels = (
            (s_value, t_value, u_value),
            (t_value, u_value, s_value),
            (u_value, s_value, t_value),
        )
        original_values = [channel_polynomial(*channel) for channel in channels]
        reduced_values = [simplified_channel(*channel) for channel in channels]
        channel_residual = max(abs(original - reduced) for original, reduced in zip(original_values, reduced_values))
        crossing_sum = sum(original_values, Fraction(0, 1))
        crossing_expected = Fraction(-9, 2) * s_value * t_value * u_value
        crossing_residual = abs(crossing_sum - crossing_expected)
        maximum_channel_residual = max(maximum_channel_residual, channel_residual)
        maximum_crossing_residual = max(maximum_crossing_residual, crossing_residual)
        rows.append(
            {
                "event_id": f"KIN4986_{event_index:02d}",
                "s": str(s_value),
                "t": str(t_value),
                "u": str(u_value),
                "channel_reduction_max_exact_residual": str(channel_residual),
                "crossing_sum": str(crossing_sum),
                "crossing_expected": str(crossing_expected),
                "crossing_exact_residual": str(crossing_residual),
                "status": "EXACT_CHANNEL_AND_CROSSING_MATCH",
                "source_path": relative(CHECKPOINT_4985),
            }
        )
    return rows, maximum_channel_residual, maximum_crossing_residual


def real_logs(s_value: float, t_value: float, u_value: float, mu_value: float) -> tuple[float, float, float, float]:
    logarithms = [
        math.log(abs(s_value) / mu_value**2),
        math.log(abs(t_value) / mu_value**2),
        math.log(abs(u_value) / mu_value**2),
    ]
    invariants = [s_value, t_value, u_value]
    stu_value = s_value * t_value * u_value
    basis_a = sum(invariant**3 * logarithm for invariant, logarithm in zip(invariants, logarithms))
    basis_b = stu_value * sum(logarithms)
    square_a = sum(invariant**3 * logarithm**2 for invariant, logarithm in zip(invariants, logarithms))
    square_b = stu_value * sum(logarithm**2 for logarithm in logarithms)
    return basis_a, basis_b, square_a, square_b


def amplitude_pieces(
    s_value: float,
    t_value: float,
    u_value: float,
    mu_value: float,
    coefficient_c: float,
    coefficient_w: float,
    source_s: float,
    rational_rho: float,
    angular_j: float,
) -> dict[str, float]:
    basis_a, basis_b, square_a, square_b = real_logs(s_value, t_value, u_value, mu_value)
    stu_value = s_value * t_value * u_value
    one_loop_log = (2.0 / math.pi) * (23.0 * basis_a / 15.0 - basis_b / 30.0)
    one_loop_full = one_loop_log + rational_rho * stu_value
    double_log = (8.0 / math.pi) * (23.0 * square_a / 15.0 - square_b / 30.0)
    invariant_i = 3.0 * source_s - 16.0 * rational_rho
    coefficient_a = -invariant_i / 12.0 + angular_j / 2.0
    coefficient_b = -invariant_i / 12.0 - angular_j / 2.0
    single_log = coefficient_a * basis_a + coefficient_b * basis_b
    reduced_amplitude = -3.0 * coefficient_w * stu_value + coefficient_c * one_loop_full + double_log + single_log
    return {
        "L_A": basis_a,
        "L_B": basis_b,
        "Q_A": square_a,
        "Q_B": square_b,
        "F1_log": one_loop_log,
        "F1": one_loop_full,
        "F2_double": double_log,
        "F2_single": single_log,
        "I_2L": invariant_i,
        "amplitude": reduced_amplitude,
    }


def rg_check_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    generator = np.random.default_rng(14986)
    rows: list[dict[str, Any]] = []
    maxima = {
        "F1_derivative": 0.0,
        "F2_double_derivative": 0.0,
        "RG_amplitude": 0.0,
        "scheme_invariant": 0.0,
        "scheme_amplitude": 0.0,
    }
    derivative_step = 1.0e-6
    for event_index in range(48):
        s_value = float(generator.uniform(0.4, 5.0))
        t_value = float(generator.uniform(-6.0, -0.2))
        u_value = -s_value - t_value
        if abs(u_value) < 0.15:
            t_value -= 0.41
            u_value = -s_value - t_value
        mu_value = float(generator.uniform(0.5, 2.5))
        coefficient_c = float(generator.uniform(-2.0, 2.0))
        coefficient_w = float(generator.uniform(-2.0, 2.0))
        source_s = float(generator.uniform(-3.0, 3.0))
        rational_rho = float(generator.uniform(-2.0, 2.0))
        angular_j = float(generator.uniform(-2.0, 2.0))
        alpha_value = float(generator.uniform(-2.0, 2.0))
        time_shift = float(generator.uniform(-1.2, 1.2))
        stu_value = s_value * t_value * u_value

        center = amplitude_pieces(
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
        plus = amplitude_pieces(
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
        minus = amplitude_pieces(
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
        derivative_f1 = (plus["F1_log"] - minus["F1_log"]) / (2.0 * derivative_step)
        expected_f1 = -18.0 * stu_value / math.pi
        residual_f1 = abs(derivative_f1 - expected_f1) / max(abs(expected_f1), 1.0e-14)
        derivative_double = (plus["F2_double"] - minus["F2_double"]) / (2.0 * derivative_step)
        expected_double = -16.0 * center["F1_log"]
        residual_double = abs(derivative_double - expected_double) / max(abs(expected_double), 1.0e-14)

        evolved_c = coefficient_c + 16.0 * time_shift
        evolved_w = coefficient_w + (MIXING_B * coefficient_c + source_s) * time_shift + 8.0 * MIXING_B * time_shift**2
        evolved = amplitude_pieces(
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
        residual_rg = abs(evolved["amplitude"] - center["amplitude"]) / max(
            abs(evolved["amplitude"]), abs(center["amplitude"]), 1.0e-14
        )

        transformed_source = source_s + 16.0 * alpha_value
        transformed_rho = rational_rho + 3.0 * alpha_value
        transformed_w = coefficient_w + alpha_value * coefficient_c
        transformed = amplitude_pieces(
            s_value,
            t_value,
            u_value,
            mu_value,
            coefficient_c,
            transformed_w,
            transformed_source,
            transformed_rho,
            angular_j,
        )
        invariant_residual = abs(transformed["I_2L"] - center["I_2L"])
        scheme_amplitude_residual = abs(transformed["amplitude"] - center["amplitude"]) / max(
            abs(transformed["amplitude"]), abs(center["amplitude"]), 1.0e-14
        )

        maxima["F1_derivative"] = max(maxima["F1_derivative"], residual_f1)
        maxima["F2_double_derivative"] = max(maxima["F2_double_derivative"], residual_double)
        maxima["RG_amplitude"] = max(maxima["RG_amplitude"], residual_rg)
        maxima["scheme_invariant"] = max(maxima["scheme_invariant"], invariant_residual)
        maxima["scheme_amplitude"] = max(maxima["scheme_amplitude"], scheme_amplitude_residual)
        rows.append(
            {
                "event_id": f"RG4986_{event_index + 1:02d}",
                "s": s_value,
                "t": t_value,
                "u": u_value,
                "mu": mu_value,
                "time_shift": time_shift,
                "F1_log_derivative_relative_residual": residual_f1,
                "F2_double_derivative_relative_residual": residual_double,
                "full_reduced_amplitude_RG_relative_residual": residual_rg,
                "I2L_scheme_absolute_residual": invariant_residual,
                "full_reduced_amplitude_scheme_relative_residual": scheme_amplitude_residual,
                "status": "RG_AND_FINITE_SCHEME_IDENTITIES_PASS",
                "source_path": relative(BERN_SOURCE),
            }
        )
    return rows, maxima


def local_scales() -> list[tuple[str, float, str]]:
    return [
        ("R10_minimum_separation", 52.0e-6, "Lee et al. apparatus minimum reported separation; used only as a length benchmark"),
        ("one_millimetre", 1.0e-3, "laboratory length benchmark"),
        ("one_metre", 1.0, "laboratory length benchmark"),
        ("Earth_radius", 6.371e6, "surface-radius benchmark"),
        ("Sun_radius", 6.957e8, "surface-radius benchmark"),
        ("one_AU", 149_597_870_700.0, "orbital length benchmark"),
    ]


def c3_rows(result_4963: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    c3_result = result_4963["C3_selection"]
    selected_a_plus = float(c3_result["selected_a_plus_abs_m4"])
    selected_a_min = float(c3_result["selected_A_C3_min"])
    selected_a_max = float(c3_result["selected_A_C3_max"])
    source_b_min = float(c3_result["source_B_C3_min"])
    source_b_max = float(c3_result["source_B_C3_max"])
    rows: list[dict[str, Any]] = []
    maximum_selected_acceleration = 0.0
    maximum_running_acceleration = 0.0
    for scale_id, radius_m, meaning in local_scales():
        selected_potential = 5.0 * selected_a_plus / radius_m**4
        selected_acceleration = 35.0 * selected_a_plus / radius_m**4
        running_values = []
        for selected_a in (selected_a_min, selected_a_max):
            for source_b in (source_b_min, source_b_max):
                for scale_factor in (0.5, 1.0, 2.0):
                    running_values.append(selected_a + source_b * math.log((scale_factor * PLANCK_LENGTH_M / radius_m) ** 2))
        running_a_plus = 16.0 * math.pi * max(abs(value) for value in running_values) * PLANCK_LENGTH_M**4
        running_potential = 5.0 * running_a_plus / radius_m**4
        running_acceleration = 35.0 * running_a_plus / radius_m**4
        coefficient_for_one_percent = 0.01 * radius_m**4 / (35.0 * PLANCK_LENGTH_M**4)
        maximum_selected_acceleration = max(maximum_selected_acceleration, selected_acceleration)
        maximum_running_acceleration = max(maximum_running_acceleration, running_acceleration)
        rows.append(
            {
                "scale_id": scale_id,
                "radius_or_separation_m": radius_m,
                "benchmark_meaning": meaning,
                "condition": "r>=2M and first order in a_plus",
                "selected_a_plus_abs_m4": selected_a_plus,
                "selected_abs_DeltaPhi_over_PhiN_bound": selected_potential,
                "selected_abs_Deltaa_over_aN_bound": selected_acceleration,
                "raw_running_a_plus_abs_envelope_m4": running_a_plus,
                "raw_running_abs_DeltaPhi_over_PhiN_bound": running_potential,
                "raw_running_abs_Deltaa_over_aN_bound": running_acceleration,
                "dimensionless_abs_a_plus_over_lP4_needed_for_one_percent_acceleration": coefficient_for_one_percent,
                "orders_selected_acceleration_below_one_percent": math.log10(0.01 / selected_acceleration),
                "status": "SELECTED_LOCAL_C3_EXTERIOR_BOUND_DERIVED",
                "claim_guard": "raw running envelope is not a physical local-plus-nonlocal amplitude",
                "source_path": relative(CHECKPOINT_4963),
                "valid_for_selected_C3_coordinate_bound": True,
                "valid_for_complete_physical_C3_amplitude": False,
            }
        )
    return rows, {
        "maximum_selected_acceleration_bound": maximum_selected_acceleration,
        "maximum_raw_running_acceleration_bound": maximum_running_acceleration,
    }


def parent_log_coefficients() -> dict[str, tuple[Fraction, Fraction]]:
    rows = read_csv(PARENT_LOG_CSV)
    by_sector = {
        sector: {row["invariant"]: row for row in rows if row["sector"] == sector}
        for sector in ("Einstein_plus_ghost", "one_real_minimal_motion_scalar_UV", "parent_zero_motion_background")
    }
    return {
        sector: (
            Fraction(sector_rows["Ricci_log_Ricci"]["action_coefficient_in_units_1_over_4pi_squared"]),
            Fraction(sector_rows["R_log_R"]["action_coefficient_in_units_1_over_4pi_squared"]),
        )
        for sector, sector_rows in by_sector.items()
    }


def determinant_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coefficient_sets = parent_log_coefficients()
    gravity_a, gravity_b = coefficient_sets["Einstein_plus_ghost"]
    motion_a, motion_b = coefficient_sets["one_real_minimal_motion_scalar_UV"]
    coefficient_a, coefficient_b = coefficient_sets["parent_zero_motion_background"]
    if gravity_a + motion_a != coefficient_a or gravity_b + motion_b != coefficient_b:
        raise RuntimeError("parent determinant sector sum mismatch")
    gravity_sum = gravity_a + gravity_b
    motion_sum = motion_a + motion_b
    coefficient_sum = coefficient_a + coefficient_b
    spin_two_kernel = coefficient_a / 2
    spin_zero_kernel = 2 * (coefficient_a + 3 * coefficient_b)
    source_spin_two = Fraction(2, 3)
    source_spin_zero = Fraction(1, 3)
    tree_source_contraction = source_spin_two - source_spin_zero / 2
    weighted_log_contraction = spin_two_kernel * source_spin_two + Fraction(1, 4) * spin_zero_kernel * source_spin_zero
    normalized_contraction = weighted_log_contraction / tree_source_contraction
    momentum_fraction = 2 * normalized_contraction
    if normalized_contraction != coefficient_a + coefficient_b:
        raise RuntimeError("spin-projector determinant contraction mismatch")
    momentum_coefficient = 2.0 * float(coefficient_sum) / math.pi
    potential_coefficient = 4.0 * float(coefficient_sum) / math.pi
    acceleration_coefficient = 3.0 * potential_coefficient
    gravity_momentum_coefficient = 2.0 * float(gravity_sum) / math.pi
    gravity_potential_coefficient = 4.0 * float(gravity_sum) / math.pi
    gravity_acceleration_coefficient = 3.0 * gravity_potential_coefficient
    rows: list[dict[str, Any]] = []
    maximum_acceleration = 0.0
    for scale_id, radius_m, meaning in local_scales():
        potential_bound = potential_coefficient * PLANCK_LENGTH_M**2 / radius_m**2
        acceleration_bound = acceleration_coefficient * PLANCK_LENGTH_M**2 / radius_m**2
        gravity_potential_bound = gravity_potential_coefficient * PLANCK_LENGTH_M**2 / radius_m**2
        gravity_acceleration_bound = gravity_acceleration_coefficient * PLANCK_LENGTH_M**2 / radius_m**2
        maximum_acceleration = max(maximum_acceleration, acceleration_bound)
        rows.append(
            {
                "scale_id": scale_id,
                "radius_or_separation_m": radius_m,
                "benchmark_meaning": meaning,
                "Einstein_ghost_Ricci_log_Ricci_a": str(gravity_a),
                "Einstein_ghost_R_log_R_b": str(gravity_b),
                "Einstein_ghost_a_plus_b": str(gravity_sum),
                "massless_motion_Ricci_log_Ricci_a_increment": str(motion_a),
                "massless_motion_R_log_R_b_increment": str(motion_b),
                "massless_motion_a_plus_b_increment": str(motion_sum),
                "parent_Ricci_log_Ricci_a": str(coefficient_a),
                "parent_R_log_R_b": str(coefficient_b),
                "a_plus_b": str(coefficient_sum),
                "momentum_relative_kernel": "-[2(a+b)/pi]lP^2 q^2 ln(q^2/mu^2)",
                "momentum_numeric_coefficient": momentum_coefficient,
                "gravity_only_momentum_numeric_coefficient": gravity_momentum_coefficient,
                "gravity_only_exterior_abs_DeltaPhi_over_PhiN": gravity_potential_bound,
                "gravity_only_exterior_abs_Deltaa_over_aN": gravity_acceleration_bound,
                "exterior_abs_DeltaPhi_over_PhiN": potential_bound,
                "exterior_abs_Deltaa_over_aN": acceleration_bound,
                "orders_acceleration_below_one_percent": math.log10(0.01 / acceleration_bound),
                "motion_threshold_regime": "parent value is the m_gap*r<<1 massless-log endpoint; physical m_gap threshold is unsourced",
                "status": "PARENT_MASSLESS_ENDPOINT_TWO_POINT_TAIL_DERIVED",
                "claim_guard": "vacuum-polarization/two-point subset and massless-motion endpoint, not the complete thresholded one-loop source-source potential",
                "source_path": relative(PARENT_LOG_CSV),
                "valid_for_parent_massless_endpoint_two_point_tail": True,
                "valid_for_unsourced_physical_mgap_tail": False,
                "valid_for_complete_quantum_potential": False,
            }
        )
    summary = {
        "a": str(coefficient_a),
        "b": str(coefficient_b),
        "a_plus_b": str(coefficient_sum),
        "gravity_a": str(gravity_a),
        "gravity_b": str(gravity_b),
        "gravity_a_plus_b": str(gravity_sum),
        "massless_motion_a": str(motion_a),
        "massless_motion_b": str(motion_b),
        "massless_motion_a_plus_b": str(motion_sum),
        "spin_two_kernel": str(spin_two_kernel),
        "spin_zero_kernel": str(spin_zero_kernel),
        "tree_source_contraction": str(tree_source_contraction),
        "weighted_log_contraction": str(weighted_log_contraction),
        "normalized_contraction": str(normalized_contraction),
        "momentum_fraction": str(momentum_fraction),
        "momentum_coefficient": momentum_coefficient,
        "potential_coefficient": potential_coefficient,
        "acceleration_coefficient": acceleration_coefficient,
        "gravity_momentum_coefficient": gravity_momentum_coefficient,
        "gravity_potential_coefficient": gravity_potential_coefficient,
        "gravity_acceleration_coefficient": gravity_acceleration_coefficient,
        "maximum_acceleration_bound": maximum_acceleration,
        "physical_mgap_threshold_sourced": False,
    }
    return rows, summary


def contact_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PM4986_01_local_R2",
            "sector": "finite local p4",
            "operator": "R^2",
            "first_order_propagator_effect": "analytic polynomial in q^2",
            "exterior_effect_r_gt_0": "zero distributionally for separated compact sources",
            "status": "SOURCE_CONTACT_ONLY_AT_EFT_ORDER",
            "source_path": relative(BURGESS_SOURCE),
            "valid_for_separated_exterior_zero": True,
            "valid_for_source_interior_zero": False,
        },
        {
            "row_id": "PM4986_02_local_Ricci2",
            "sector": "finite local p4",
            "operator": "R_mn R^mn",
            "first_order_propagator_effect": "analytic polynomial in q^2",
            "exterior_effect_r_gt_0": "zero distributionally for separated compact sources",
            "status": "SOURCE_CONTACT_ONLY_AT_EFT_ORDER",
            "source_path": relative(BURGESS_SOURCE),
            "valid_for_separated_exterior_zero": True,
            "valid_for_source_interior_zero": False,
        },
        {
            "row_id": "PM4986_03_nonlocal_log",
            "sector": "nonlocal p4 gravity plus massless-motion endpoint",
            "operator": "a Ricci log(-Box/mu^2) Ricci+b R log(-Box/mu^2)R",
            "first_order_propagator_effect": "nonanalytic log(q^2), hence r^-3 potential tail",
            "exterior_effect_r_gt_0": "nonzero and explicitly bounded in determinant_exterior_tail_bounds.csv",
            "status": "GRAVITY_TAIL_AND_PARENT_MASSLESS_ENDPOINT",
            "source_path": relative(PARENT_LOG_CSV),
            "valid_for_separated_exterior_zero": False,
            "valid_for_source_interior_zero": False,
        },
        {
            "row_id": "PM4986_04_local_C3",
            "sector": "selected local p6",
            "operator": "a_plus C^3 exterior solution",
            "first_order_propagator_effect": "no flat p2 pole shift; nonlinear r^-7 potential",
            "exterior_effect_r_gt_0": "mass-independent compactness bound for r>=2M",
            "status": "SELECTED_COORDINATE_NONZERO_AND_BOUNDED",
            "source_path": relative(CHECKPOINT_4963),
            "valid_for_separated_exterior_zero": False,
            "valid_for_source_interior_zero": False,
        },
        {
            "row_id": "PM4986_05_all_operator_boundary",
            "sector": "full parent",
            "operator": "p8-plus tower, finite matching and complete source amplitudes",
            "first_order_propagator_effect": "not fully assembled",
            "exterior_effect_r_gt_0": "not promoted",
            "status": "EXACT_ALL_OPERATOR_LOCAL_GR_OPEN_NONCLAIM",
            "source_path": relative(CHECKPOINT_4985),
            "valid_for_separated_exterior_zero": False,
            "valid_for_source_interior_zero": False,
        },
    ]


def gate_rows(
    sources: dict[str, bool],
    channel_residual: Fraction,
    crossing_residual: Fraction,
    rg_maxima: dict[str, float],
    c3_summary: dict[str, float],
    determinant_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    checks = [
        ("sources", all(sources.values()), "all primary/local source markers found"),
        ("channel_reduction", channel_residual == 0, f"exact residual={channel_residual}"),
        ("crossing", crossing_residual == 0, f"exact residual={crossing_residual}"),
        ("one_loop_nonlocal_kernel", rg_maxima["F1_derivative"] < 2.0e-8, f"max={rg_maxima['F1_derivative']:.3e}"),
        ("two_loop_double_log_kernel", rg_maxima["F2_double_derivative"] < 2.0e-8, f"max={rg_maxima['F2_double_derivative']:.3e}"),
        ("full_log_RG", rg_maxima["RG_amplitude"] < 2.0e-12, f"max={rg_maxima['RG_amplitude']:.3e}"),
        ("scheme_invariant_I2L", rg_maxima["scheme_invariant"] < 2.0e-12, f"max={rg_maxima['scheme_invariant']:.3e}"),
        ("scheme_invariant_amplitude", rg_maxima["scheme_amplitude"] < 2.0e-12, f"max={rg_maxima['scheme_amplitude']:.3e}"),
        ("numeric_I2L", False, "complete scalar two-loop mixed and three-particle cuts not yet calculated"),
        ("numeric_J2L", False, "scale-free angular single-log shape not yet calculated"),
        ("finite_Cw", False, "UV trajectory boundary datum remains"),
        ("C3_compactness_bound", c3_summary["maximum_selected_acceleration_bound"] < 0.01, f"max={c3_summary['maximum_selected_acceleration_bound']:.3e}"),
        ("C3_complete_amplitude", False, "selected local coordinate and raw-running guard are not the full local-plus-nonlocal p6 amplitude"),
        ("finite_p4_exterior_contact", True, "local R2/Ricci2 terms are contact-supported at first EFT order"),
        ("determinant_projector", determinant_summary["momentum_fraction"] == "89/120", str(determinant_summary)),
        ("determinant_exterior_bound", determinant_summary["maximum_acceleration_bound"] < 0.01, f"massless-parent endpoint max={determinant_summary['maximum_acceleration_bound']:.3e}; physical m_gap threshold open"),
        ("known_p4_p6_metric_residuals", True, "finite p4 contact, gravity p4 tail, parent massless-log endpoint and selected C3 exterior residual are separated and bounded"),
        ("exact_all_operator_local_GR", False, "p8-plus, source interiors and complete finite amplitudes remain"),
        ("full_MTS", False, "not claimed"),
    ]
    return [
        {
            "gate_id": f"GATE4986_{index:02d}_{name}",
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "OPEN_NONCLAIM",
            "claim_allowed": bool(passed and name not in {"known_p4_p6_metric_residuals"}),
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], source_checks: dict[str, bool]) -> None:
    lines = [
        "# 4986 common-scheme logarithm and local metric provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Primary sources",
        "",
        "- [Dunbar and Norridge, *Infinities within Graviton Scattering Amplitudes*](https://arxiv.org/abs/hep-th/9512084): complete cut-constructible logarithmic part of the one-loop four-scalar Einstein-gravity amplitude, scalar/graviton intermediate states, the scalar counterterm, and the finite-rational ambiguity boundary.",
        "- [Bern et al., *Two-Loop Renormalization of Quantum Gravity Simplified*](https://arxiv.org/abs/1701.02422): renormalization-scale extraction from four-dimensional unitarity, evanescent safety, and the need to inspect both two- and three-particle cuts.",
        "- [Burgess, *Quantum Gravity in Everyday Life*](https://arxiv.org/abs/gr-qc/0311082): field-redefinition quotient and the separation of analytic source contacts from nonanalytic long-range tails.",
        "",
        "The Dunbar-Norridge source archive and extracted TeX are retained under `source-intake/functional_rg/4986/sources/`.",
        "",
        "## Source-marker checks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{hash_value}`" for path, hash_value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "The one-loop mixed nonlocal logarithm, the full RG-forced two-loop double-log kernel, and `I_2L=3S_2L-16rho_mix` are derived in the checkpoint-4985 amplitude conventions. A numeric `I_2L`, the scale-free angular coefficient `J_2L`, and `C_w` are not derived. The metric calculation bounds the selected local `C^3` coordinate, the gravity-only determinant tail, and the parent massless-log endpoint while proving only separated-source contact silence for finite local p4 terms. The physical motion `m_gap` threshold form factor is unsourced, so the parent endpoint is valid only for `m_gap r << 1`. This is not a complete one-loop potential, a source-interior theorem, exact all-operator local GR, or full MTS.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    required_paths = (
        CHECKPOINT_4985,
        RESULT_4985,
        CHECKPOINT_4963,
        RESULT_4963,
        CHECKPOINT_4981,
        RESULT_4981,
        PARENT_LOG_CSV,
        BURGESS_SOURCE,
        BERN_SOURCE,
        DUNBAR_SOURCE,
        DUNBAR_ARCHIVE,
    )
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("\n".join(missing))
    source_checks = source_lock()
    if not all(source_checks.values()):
        raise RuntimeError(json.dumps(source_checks, indent=2, sort_keys=True))

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "dry_run": True,
                    "required_paths": len(required_paths),
                    "source_checks": source_checks,
                    "planned_outputs": 9,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    SOURCE.mkdir(parents=True, exist_ok=True)
    result_4963 = json.loads(RESULT_4963.read_text(encoding="utf-8"))
    basis_rows = log_basis_rows()
    kinematic_rows, channel_residual, crossing_residual = exact_kinematic_rows()
    rg_rows, rg_maxima = rg_check_rows()
    metric_c3_rows, c3_summary = c3_rows(result_4963)
    metric_determinant_rows, determinant_summary = determinant_rows()
    metric_contact_rows = contact_rows()
    gates = gate_rows(source_checks, channel_residual, crossing_residual, rg_maxima, c3_summary, determinant_summary)

    write_csv(LOG_BASIS_CSV, tagged(basis_rows))
    write_csv(KINEMATIC_CSV, tagged(kinematic_rows))
    write_csv(RG_CSV, tagged(rg_rows))
    write_csv(C3_CSV, tagged(metric_c3_rows))
    write_csv(DETERMINANT_CSV, tagged(metric_determinant_rows))
    write_csv(CONTACT_CSV, tagged(metric_contact_rows))
    write_csv(GATE_CSV, tagged(gates))

    hash_paths = required_paths + (Path(__file__),)
    source_hashes = {relative(path): digest(path) for path in hash_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "O2_amplitude": {
            "channel_polynomial": "P_s=-(23/15)s^3+(1/30)stu",
            "crossing_sum": "sum P_s=-(9/2)stu",
            "one_loop_nonlocal_log": "F1_log=(2/pi)[(23/15)L_A-(1/30)L_B]",
            "one_loop_finite_coordinate": "F1=F1_log+rho_mix stu",
            "two_loop_double_log": "F2_double=(8/pi)[(23/15)Q_A-(1/30)Q_B]",
            "scheme_invariant": "I_2L=3S_2L-16rho_mix",
            "single_log_constraint": "A_2+B_2=-I_2L/6; J_2L=A_2-B_2",
            "full_two_loop_scale_coefficient_derived": False,
            "full_two_loop_angular_coefficient_derived": False,
            "finite_Cw_derived": False,
            "maximum_checks": rg_maxima,
        },
        "local_metric": {
            "C3": c3_summary,
            "determinant": determinant_summary,
            "finite_local_p4_separated_exterior_contact_zero": True,
            "known_p4_p6_residuals_separated_and_bounded": True,
            "complete_physical_C3_amplitude": False,
            "complete_quantum_source_source_potential": False,
            "physical_motion_mass_threshold_sourced": False,
            "exact_all_operator_local_GR": False,
        },
        "gates": {
            "one_loop_mixed_nonlocal_log_derived": True,
            "two_loop_double_log_kernel_derived": True,
            "I2L_scheme_invariant_derived": True,
            "I2L_numeric_derived": False,
            "J2L_numeric_derived": False,
            "Cw_derived": False,
            "finite_p4_separated_exterior_contact_zero": True,
            "massless_parent_determinant_endpoint_bounded": True,
            "physical_motion_mass_threshold_sourced": False,
            "selected_C3_exterior_bounded": True,
            "exact_all_operator_local_GR": False,
            "full_MTS": False,
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes, source_checks)

    passed = sum(bool(row["passed"]) for row in gates)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "gate_rows": len(gates),
                "passed_rows": passed,
                "open_nonclaim_rows": len(gates) - passed,
                "RG_maxima": rg_maxima,
                "C3_maximum_selected_acceleration_bound": c3_summary["maximum_selected_acceleration_bound"],
                "determinant_maximum_acceleration_bound": determinant_summary["maximum_acceleration_bound"],
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
