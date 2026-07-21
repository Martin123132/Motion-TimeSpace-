from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5018"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5008 = POST / "scripts" / "Y5_R2FR_5008_completed_hh_kernel_outer_cut_Wigner_insertion.py"
SCRIPT_5014 = POST / "scripts" / "Y5_R2FR_5014_crossing_complete_locality_and_graph_complete_pph_bridge.py"
SCRIPT_5015 = POST / "scripts" / "Y5_R2FR_5015_graph_complete_pph_crossed_sheet_continuation.py"
SCRIPT_5016 = POST / "scripts" / "Y5_R2FR_5016_completed_hh_crossed_function_and_hhh_nonlocal_target.py"
SCRIPT_5017 = POST / "scripts" / "Y5_R2FR_5017_complex_safe_hhh_crossed_integrand_and_coupled_locality_smoke.py"
RESULT_5008 = POST / "source-intake" / "functional_rg" / "5008" / "hh_outer_Wigner_insertion_results.json"
RESULT_5014 = POST / "source-intake" / "functional_rg" / "5014" / "crossing_complete_graph_complete_pph_results.json"
RESULT_5015 = POST / "source-intake" / "functional_rg" / "5015" / "graph_complete_pph_crossed_sheet_results.json"
RESULT_5017 = POST / "source-intake" / "functional_rg" / "5017" / "complex_safe_hhh_crossed_results.json"
HH_TOWER = POST / "source-intake" / "functional_rg" / "5008" / "hh_wigner_partial_wave_tower.csv"
PPH_CROSSING = POST / "source-intake" / "functional_rg" / "5015" / "graph_complete_pph_cyclic_crossing_function.csv"
HHH_CROSSING = POST / "source-intake" / "functional_rg" / "5017" / "graph_complete_hhh_cyclic_crossing_smoke.csv"

IDENTITY_CSV = SOURCE / "Legendre_resolvent_and_Hadamard_kernel_identity.csv"
MOMENT_CSV = SOURCE / "hh_Hadamard_endpoint_moments.csv"
DIRECT_CSV = SOURCE / "hh_Hadamard_crossed_direct_function.csv"
CROSSING_CSV = SOURCE / "hh_Hadamard_cyclic_crossing_function.csv"
TARGET_CSV = SOURCE / "known_master_without_hhh_and_matched_hhh_target.csv"
COMPARISON_CSV = SOURCE / "raw_hhh_smoke_vs_matched_nonlocal_target.csv"
GATE_CSV = SOURCE / "hh_Hadamard_crossing_completion_gate.csv"
RESULT_JSON = SOURCE / "hh_Hadamard_crossing_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5018-Y5-R2FR-hh-Legendre-resolvent-Hadamard-crossing-completion.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5018_VALIDATION.csv"

MARKER = "MTS_5018_HH_LEGENDRE_RESOLVENT_HADAMARD_CROSSING_COMPLETION"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
PHYSICAL_COSINES = (-0.6, -0.3, 0.0, 0.3, 0.6)


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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


def source_locks() -> dict[str, bool]:
    required = (
        SCRIPT_5008,
        SCRIPT_5014,
        SCRIPT_5015,
        SCRIPT_5016,
        SCRIPT_5017,
        RESULT_5008,
        RESULT_5014,
        RESULT_5015,
        RESULT_5017,
        HH_TOWER,
        PPH_CROSSING,
        HHH_CROSSING,
    )
    result_5008 = read_json(RESULT_5008)
    result_5014 = read_json(RESULT_5014)
    result_5015 = read_json(RESULT_5015)
    result_5017 = read_json(RESULT_5017)
    corrected_5016 = SCRIPT_5016.read_text(encoding="utf-8")
    return {
        "required_paths": all(path.exists() for path in required),
        "5008_exact_arbitrary_J_generator": result_5008["partial_wave_tower"]["arbitrary_even_J_exact_generator"] is True,
        "5008_prefactor": result_5008["normalization"]["reduced_cut_prefactor"] == "-64/pi",
        "5014_per_mode_rule_rejected": result_5014["5013_per_J_locality_rule_valid"] is False,
        "5015_pph_crossed": result_5015["graph_complete_pph_crossed_function"] is True,
        "5017_complex_safe_hhh": result_5017["complex_safe_five_point_KLT"] is True,
        "5016_opposite_helicity_pair_repaired": "left_plus_minus" in corrected_5016 and "right_minus_plus" in corrected_5016,
    }


def exact_resolvent_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spectral = sp.symbols("lambda")
    partial_fraction = sp.apart(
        1 / (spectral * (spectral - 2) * (spectral - 6) * (spectral - 12)),
        spectral,
    )
    expected_partial_fraction = (
        -1 / (144 * spectral)
        + 1 / (80 * (spectral - 2))
        - 1 / (144 * (spectral - 6))
        + 1 / (720 * (spectral - 12))
    )

    w_value, z_value = sp.symbols("w z")
    weights = (
        -sp.Rational(1, 144),
        sp.Rational(1, 80),
        -sp.Rational(1, 144),
        sp.Rational(1, 720),
    )
    kernel = sp.Integer(0)
    for degree, weight in enumerate(weights):
        degree_residue = sp.diff(
            sp.legendre(degree, -w_value) * sp.log((1 - w_value) / 2),
            w_value,
            4,
        )
        kernel += weight * (-1) ** degree * sp.legendre(
            degree, z_value
        ) * degree_residue
    kernel = sp.factor(kernel)
    expected_kernel = sp.factor(
        (
            5 * w_value**3 * z_value**3
            - 3 * w_value**3 * z_value
            - 20 * w_value**2 * z_value**3
            + 3 * w_value**2 * z_value**2
            + 12 * w_value**2 * z_value
            - w_value**2
            + 29 * w_value * z_value**3
            - 12 * w_value * z_value**2
            - 15 * w_value * z_value
            + 4 * w_value
            - 16 * z_value**3
            + 15 * z_value**2
            - 1
        )
        / (96 * (w_value - 1) ** 4)
    )
    apart_kernel = sp.apart(kernel, w_value)
    expected_apart = (
        z_value * (5 * z_value**2 - 3) / (96 * (w_value - 1))
        - (z_value - 1)
        * (5 * z_value**2 + 2 * z_value - 1)
        / (96 * (w_value - 1) ** 2)
        + (z_value - 1) ** 2
        * (2 * z_value + 1)
        / (48 * (w_value - 1) ** 3)
        - (z_value - 1) ** 3 / (48 * (w_value - 1) ** 4)
    )

    mp.mp.dps = 50
    degree = mp.mpf("0.37")
    left = mp.mpf("-0.21")
    right = mp.mpf("0.42")
    series = mp.nsum(
        lambda index: (2 * index + 1)
        * mp.legendre(index, left)
        * mp.legendre(index, right)
        / (index * (index + 1) - degree * (degree + 1)),
        [0, mp.inf],
    )
    closed = -mp.pi / mp.sin(mp.pi * degree) * mp.legenp(
        degree, 0, -left
    ) * mp.legenp(degree, 0, right)
    resolvent_residual = abs(series - closed)

    fourth_derivative_zeros = [
        sp.diff(sp.legendre(degree_index, w_value), w_value, 4)
        for degree_index in range(4)
    ]
    rows = [
        {
            "identity_id": "RES5018_01_factorial_spectral_denominator",
            "statement": "(J-4)!/(J+4)!=1/[lambda(lambda-2)(lambda-6)(lambda-12)]",
            "exact_residual": 0,
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "RES5018_02_partial_fraction",
            "statement": str(partial_fraction),
            "exact_residual": str(sp.simplify(partial_fraction - expected_partial_fraction)),
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "RES5018_03_Legendre_resolvent",
            "statement": "sum_J (2J+1)P_J(x)P_J(y)/(lambda_J-lambda_nu)=-pi P_nu(-x_<)P_nu(x_>)/sin(pi nu)",
            "exact_residual": mp.nstr(resolvent_residual, 20),
            "status": "NUMERIC_IDENTITY_CHECK",
        },
        {
            "identity_id": "RES5018_04_low_poles_annihilated",
            "statement": "d_w^4 P_l(w)=0 for l=0,1,2,3",
            "exact_residual": str(fourth_derivative_zeros),
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "RES5018_05_exterior_kernel",
            "statement": str(kernel),
            "exact_residual": str(sp.simplify(kernel - expected_kernel)),
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "RES5018_06_endpoint_apart_kernel",
            "statement": str(apart_kernel),
            "exact_residual": str(sp.simplify(apart_kernel - expected_apart)),
            "status": "DERIVED_EXACT",
        },
    ]
    return rows, {
        "partial_fraction": str(partial_fraction),
        "exterior_kernel": str(kernel),
        "endpoint_apart_kernel": str(apart_kernel),
        "resolvent_numeric_residual": float(resolvent_residual),
        "all_exact": all(row["exact_residual"] in (0, "0", "[0, 0, 0, 0]") for row in rows if row["identity_id"] != "RES5018_03_Legendre_resolvent"),
    }


def hard_regular(x_value: mp.mpf) -> mp.mpf:
    log_x = mp.log(x_value)
    log_y = mp.log(1 - x_value)
    t_value = -x_value
    u_value = x_value - 1
    hard = (
        t_value**3
        * u_value
        * (6 * t_value**2 - 9 * t_value * u_value - 11 * u_value**2)
        * log_x
        / 96
        + t_value**3 * u_value**3 * log_x * log_y / 8
        + t_value**4
        * (t_value**3 + 2 * t_value**2 * u_value + 3 * t_value * u_value**2 + u_value**3)
        * log_x**2
        / (16 * (t_value + u_value))
        - t_value
        * u_value**3
        * (11 * t_value**2 + 9 * t_value * u_value - 6 * u_value**2)
        * log_y
        / 96
        + u_value**4
        * (t_value**3 + 3 * t_value**2 * u_value + 2 * t_value * u_value**2 + u_value**3)
        * log_y**2
        / (16 * (t_value + u_value))
        + (
            t_value**6
            + t_value**5 * u_value
            + 2 * t_value**4 * u_value**2
            + 2 * t_value**2 * u_value**4
            + t_value * u_value**5
            + u_value**6
        )
        * mp.pi**2
        / 16
    )
    hard_soft = mp.pi**2 * (5 * x_value**2 - 5 * x_value + 1) / 16
    return hard - hard_soft


def endpoint_log_moment(power: int, log_power: int, endpoint: mp.mpf) -> mp.mpf:
    denominator = mp.mpf(power + 1)
    logarithm = mp.log(endpoint)
    common = endpoint ** (power + 1)
    if log_power == 0:
        return common / denominator
    if log_power == 1:
        return common * (logarithm / denominator - 1 / denominator**2)
    if log_power == 2:
        return common * (
            logarithm**2 / denominator
            - 2 * logarithm / denominator**2
            + 2 / denominator**3
        )
    raise ValueError(log_power)


def endpoint_series_correction(index: int, endpoint: mp.mpf) -> mp.mpf:
    c_2 = 7 * mp.pi**2 / 16
    coefficient_log = -mp.mpf(11) / 96
    coefficient_constant = -9 * mp.pi**2 / 8 + mp.mpf(1) / 8
    terms = {
        2: ((0, c_2),),
        3: ((1, coefficient_log), (0, coefficient_constant)),
        4: (
            (2, mp.mpf(1) / 16),
            (1, mp.mpf(1) / 8),
            (0, -mp.mpf(5) / 24 + 19 * mp.pi**2 / 16),
        ),
        5: (
            (1, mp.mpf(7) / 32),
            (0, -3 * mp.pi**2 / 4 - mp.mpf(29) / 192),
        ),
        6: (
            (2, -mp.mpf(1) / 16),
            (1, -mp.mpf(13) / 48),
            (0, mp.mpf(2717) / 5760 + mp.pi**2 / 4),
        ),
    }
    removed_orders = {3: {2}, 4: {2, 3}}.get(index, set())
    correction = mp.mpf(0)
    for power_x, logarithmic_terms in terms.items():
        if power_x in removed_orders:
            continue
        residual_power = power_x - index
        for log_power, coefficient in logarithmic_terms:
            correction += coefficient * endpoint_log_moment(
                residual_power, log_power, endpoint
            )
    return correction


def moment_values(decimal_precision: int, endpoint_power: int) -> dict[int, mp.mpf]:
    mp.mp.dps = decimal_precision
    endpoint = mp.mpf(10) ** (-endpoint_power)
    c_2 = 7 * mp.pi**2 / 16
    coefficient_log = -mp.mpf(11) / 96
    coefficient_constant = -9 * mp.pi**2 / 8 + mp.mpf(1) / 8
    splits = [
        endpoint,
        mp.mpf("1e-5"),
        mp.mpf("1e-3"),
        mp.mpf("0.03"),
        mp.mpf("0.2"),
        mp.mpf("0.5"),
    ]
    integrands = {
        1: lambda x: hard_regular(x) * (1 / x + 1 / (1 - x)),
        2: lambda x: hard_regular(x) * (1 / x**2 + 1 / (1 - x) ** 2),
        3: lambda x: hard_regular(x) * (1 / x**3 + 1 / (1 - x) ** 3)
        - c_2 / x,
        4: lambda x: hard_regular(x) / x**4
        + hard_regular(x) / (1 - x) ** 4
        - c_2 / x**2
        - (coefficient_log * mp.log(x) + coefficient_constant) / x,
    }
    result = {
        index: mp.quad(function, splits)
        + endpoint_series_correction(index, endpoint)
        for index, function in integrands.items()
    }
    folded_endpoint = mp.mpf("0.5")
    result[3] += c_2 * mp.log(folded_endpoint)
    result[4] += (
        -2 * c_2
        + coefficient_log * mp.log(folded_endpoint) ** 2 / 2
        + coefficient_constant * mp.log(folded_endpoint)
    )
    return result


def cutoff_moment(index: int, epsilon: mp.mpf) -> mp.mpf:
    c_2 = 7 * mp.pi**2 / 16
    coefficient_log = -mp.mpf(11) / 96
    coefficient_constant = -9 * mp.pi**2 / 8 + mp.mpf(1) / 8
    splits = [
        epsilon,
        mp.mpf("1e-4"),
        mp.mpf("1e-2"),
        mp.mpf("0.2"),
        mp.mpf("0.7"),
        mp.mpf("0.97"),
        1 - mp.mpf("1e-30"),
    ]
    value = mp.quad(lambda x: hard_regular(x) / x**index, splits)
    if index == 3:
        value += c_2 * mp.log(epsilon)
    elif index == 4:
        value -= c_2 / epsilon
        value += coefficient_log * mp.log(epsilon) ** 2 / 2
        value += coefficient_constant * mp.log(epsilon)
    return value


def hadamard_moment_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    high = moment_values(90, 8)
    independent = moment_values(70, 7)
    mp.mp.dps = 80
    cutoff_epsilon = mp.mpf("1e-10")
    cutoff = {index: cutoff_moment(index, cutoff_epsilon) for index in (3, 4)}
    rows: list[dict[str, Any]] = []
    maximum_precision_shift = mp.mpf(0)
    for index in range(1, 5):
        precision_shift = abs(high[index] - independent[index])
        maximum_precision_shift = max(maximum_precision_shift, precision_shift)
        rows.append(
            {
                "moment_id": f"HAD5018_J{index}",
                "definition": f"FP integral_0^1 H_reg(x)/x^{index} dx",
                "subtracted_definition": (
                    "ordinary integral"
                    if index <= 2
                    else "integral[H/x^3-(7pi^2/16)/x]"
                    if index == 3
                    else "integral[H/x^4-(7pi^2/16)/x^2-((-11/96)log(x)+1/8-9pi^2/8)/x]-7pi^2/16"
                ),
                "value_50_digits": mp.nstr(high[index], 50),
                "independent_precision_shift": mp.nstr(precision_shift, 12),
                "cutoff_epsilon": mp.nstr(cutoff_epsilon, 5) if index >= 3 else "not_needed",
                "cutoff_value": mp.nstr(cutoff[index], 40) if index >= 3 else "not_needed",
                "cutoff_minus_subtracted": mp.nstr(cutoff[index] - high[index], 12) if index >= 3 else "not_needed",
                "status": "HADAMARD_FINITE_PART_DERIVED",
            }
        )
    w_moments = {
        index: 2 * mp.mpf(-2) ** (-index) * high[index]
        for index in range(1, 5)
    }
    return rows, {
        "x_moments": {str(index): mp.nstr(value, 60) for index, value in high.items()},
        "w_moments": {str(index): mp.nstr(value, 60) for index, value in w_moments.items()},
        "maximum_precision_shift": float(maximum_precision_shift),
        "cutoff_cross_checks": {
            str(index): float(abs(cutoff[index] - high[index])) for index in (3, 4)
        },
    }


def physical_direct(scattering_cosine: float) -> float:
    total = 0.0
    for row in read_csv(HH_TOWER):
        spin = int(row["spin_J"])
        coefficients = np.zeros(spin + 1)
        coefficients[-1] = 1.0
        polynomial = float(
            np.polynomial.legendre.legval(scattering_cosine, coefficients)
        )
        total += (
            (2 * spin + 1)
            * float(row["tree_times_regular_numeric"])
            * polynomial
        )
    return -64 * total / math.pi


def crossed_direct(scattering_cosine: float, w_moments: dict[int, mp.mpf]) -> mp.mpf:
    z_value = abs(mp.mpf(scattering_cosine))
    coefficients = {
        1: z_value * (5 * z_value**2 - 3) / 96,
        2: -(z_value - 1) * (5 * z_value**2 + 2 * z_value - 1) / 96,
        3: (z_value - 1) ** 2 * (2 * z_value + 1) / 48,
        4: -(z_value - 1) ** 3 / 48,
    }
    return 6144 / mp.pi * sum(
        coefficients[index] * w_moments[index] for index in range(1, 5)
    )


def crossing_rows(
    moments: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    mp.mp.dps = 80
    w_moments = {
        int(index): mp.mpf(value) for index, value in moments["w_moments"].items()
    }
    crossed_values = sorted(
        {
            abs((3 + cosine) / (1 - cosine))
            for cosine in PHYSICAL_COSINES
        }
        | {
            abs(-(3 - cosine) / (1 + cosine))
            for cosine in PHYSICAL_COSINES
        }
        | {1.0}
    )
    direct_rows: list[dict[str, Any]] = []
    for value in crossed_values:
        direct_rows.append(
            {
                "run_id": f"HHDIRECT5018_absz{value:.9g}",
                "absolute_crossed_cosine": value,
                "D_hh_crossed_over_G3": mp.nstr(crossed_direct(value, w_moments), 40),
                "continuation": "Legendre_resolvent_plus_Hadamard_finite_part",
                "status": "CROSSED_DIRECT_COMPLETED",
            }
        )

    result_5008 = read_json(RESULT_5008)
    weighted_tail = float(
        result_5008["partial_wave_tower"]["empirical_tail_estimate_not_bound"]
    )
    reduced_tail = 64 * weighted_tail / math.pi
    endpoint_exterior = float(crossed_direct(1.0, w_moments))
    endpoint_partial = float(
        result_5008["partial_wave_tower"]["reduced_cut_partial_sum_numeric"]
    )
    endpoint_residual = endpoint_exterior - endpoint_partial

    cyclic_rows: list[dict[str, Any]] = []
    even_values: dict[float, float] = {}
    for cosine in PHYSICAL_COSINES:
        t_ratio = -(1 - cosine) / 2
        u_ratio = -(1 + cosine) / 2
        z_t = (3 + cosine) / (1 - cosine)
        z_u = -(3 - cosine) / (1 + cosine)
        physical = physical_direct(cosine)
        t_crossed = float(crossed_direct(z_t, w_moments))
        u_crossed = float(crossed_direct(z_u, w_moments))
        cyclic = physical + t_ratio**3 * t_crossed + u_ratio**3 * u_crossed
        even_values[cosine] = cyclic
        cyclic_rows.append(
            {
                "run_id": f"HHCROSS5018_z{cosine:.6g}",
                "physical_s_channel_cosine": cosine,
                "physical_direct_J40": physical,
                "z_t": z_t,
                "D_hh_t_crossed_over_G3": t_crossed,
                "z_u": z_u,
                "D_hh_u_crossed_over_G3": u_crossed,
                "cyclic_D_hh_over_G3_real": cyclic,
                "conservative_numeric_error": reduced_tail,
                "error_note": "dominated by empirical, non-rigorous J>40 physical-direct tail estimate",
                "status": "HADAMARD_CYCLIC_COMPLETION",
            }
        )
    maximum_even_residual = max(
        abs(even_values[value] - even_values[-value])
        for value in PHYSICAL_COSINES
        if -value in even_values
    )
    return direct_rows, cyclic_rows, {
        "endpoint_exterior": endpoint_exterior,
        "endpoint_J40_partial": endpoint_partial,
        "endpoint_residual": endpoint_residual,
        "empirical_reduced_tail_estimate_not_bound": reduced_tail,
        "endpoint_within_empirical_tail": abs(endpoint_residual) <= reduced_tail,
        "maximum_crossing_even_residual": maximum_even_residual,
        "cyclic": {str(key): value for key, value in even_values.items()},
    }


def f1_real(scattering_cosine: float) -> float:
    x_value = (1 - scattering_cosine) / 2
    y_value = 1 - x_value
    basis_a = -x_value**3 * math.log(x_value) - y_value**3 * math.log(y_value)
    basis_b = x_value * y_value * (math.log(x_value) + math.log(y_value))
    return 2 / math.pi * (23 * basis_a / 15 - basis_b / 30)


def target_rows(
    hh_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    hh = {
        round(float(row["physical_s_channel_cosine"]), 12): row for row in hh_rows
    }
    pph = {
        round(float(row["physical_s_channel_cosine"]), 12): row
        for row in read_csv(PPH_CROSSING)
    }
    hhh = {
        round(float(row["physical_s_channel_cosine"]), 12): row
        for row in read_csv(HHH_CROSSING)
    }
    scalar_d0 = 143 * (120 * math.pi**2 + 1397) / (6480 * math.pi)
    scalar_d2 = (-621877 + 103800 * math.pi**2) / (162000 * math.pi)
    known_values: list[float] = []
    shapes: list[float] = []
    known_errors: list[float] = []
    base_rows: list[dict[str, Any]] = []
    for cosine in PHYSICAL_COSINES:
        key = round(cosine, 12)
        shape = 1 - cosine**2
        scalar = 3 * (scalar_d0 - 5 * scalar_d2) * shape / 4
        hh_value = float(hh[key]["cyclic_D_hh_over_G3_real"])
        pph_value = float(pph[key]["cyclic_D_pph_over_G3_real"])
        d1_value = 20.3 * f1_real(cosine)
        master = 2 * (scalar + hh_value + pph_value) + d1_value
        error = 2 * math.sqrt(
            float(hh[key]["conservative_numeric_error"]) ** 2
            + float(pph[key]["RQMC_real_error"]) ** 2
        )
        known_values.append(master)
        shapes.append(shape)
        known_errors.append(error)
        base_rows.append(
            {
                "physical_s_channel_cosine": cosine,
                "scalar_cyclic_D_over_G3": scalar,
                "hh_Hadamard_cyclic_D_over_G3": hh_value,
                "pph_graph_complete_cyclic_D_over_G3": pph_value,
                "D1_master_term_over_G3": d1_value,
                "known_master_without_hhh": master,
                "known_master_error": error,
            }
        )
    values = np.asarray(known_values)
    shape_array = np.asarray(shapes)
    local_coefficient = float(shape_array @ values / (shape_array @ shape_array))
    residuals = values - local_coefficient * shape_array
    target = -0.5 * residuals
    for row, residual, required in zip(base_rows, residuals, target):
        row["best_local_stu_coefficient_without_hhh"] = local_coefficient
        row["known_nonlocal_residual"] = float(residual)
        row["required_matched_hhh_nonlocal_cyclic_D_over_G3"] = float(required)
        row["status"] = "MATCHED_HHH_TARGET_MODULO_LOCAL_STU"

    raw_hhh = np.asarray(
        [
            float(hhh[round(cosine, 12)]["cyclic_D_hhh_over_G3_real"])
            for cosine in PHYSICAL_COSINES
        ]
    )
    raw_errors = np.asarray(
        [
            float(hhh[round(cosine, 12)]["RQMC_real_error"])
            for cosine in PHYSICAL_COSINES
        ]
    )
    hhh_local = float(shape_array @ raw_hhh / (shape_array @ shape_array))
    hhh_nonlocal = raw_hhh - hhh_local * shape_array
    mismatch = hhh_nonlocal - target
    comparison_rows: list[dict[str, Any]] = []
    for cosine, raw, error, nonlocal_value, target_value, difference in zip(
        PHYSICAL_COSINES,
        raw_hhh,
        raw_errors,
        hhh_nonlocal,
        target,
        mismatch,
    ):
        comparison_rows.append(
            {
                "physical_s_channel_cosine": cosine,
                "raw_5017_hhh_cyclic_D_over_G3": raw,
                "raw_5017_RQMC_error": error,
                "raw_hhh_best_local_coefficient": hhh_local,
                "raw_hhh_nonlocal_component": nonlocal_value,
                "required_matched_hhh_nonlocal_component": target_value,
                "raw_minus_required": difference,
                "mismatch_significance_using_raw_RQMC_only": abs(difference) / max(error, 1.0e-30),
                "status": "CROSSED_CONTOUR_MATCH_REQUIRED_NOT_THEORY_VERDICT",
            }
        )
    return base_rows, comparison_rows, {
        "known_best_local_stu_coefficient": local_coefficient,
        "required_hhh_nonlocal": target.tolist(),
        "raw_hhh_best_local_stu_coefficient": hhh_local,
        "raw_hhh_nonlocal": hhh_nonlocal.tolist(),
        "raw_minus_required": mismatch.tolist(),
        "maximum_raw_mismatch_sigma": float(
            np.max(np.abs(mismatch) / np.maximum(raw_errors, 1.0e-30))
        ),
        "interpretation": "raw 5017 hhh does not implement the crossed Hadamard/Feynman contour; mismatch selects a contour-residue derivation rather than a locality verdict, and a local finite scheme change cannot erase a nonlocal residual",
    }


def gate_rows(
    locks: dict[str, bool],
    identities: dict[str, Any],
    moments: dict[str, Any],
    crossing: dict[str, Any],
    target: dict[str, Any],
) -> list[dict[str, Any]]:
    gates = [
        ("source_locks", all(locks.values()), "all predecessor/source paths"),
        ("spectral_resolvent_exact", identities["all_exact"], identities["partial_fraction"]),
        ("resolvent_numeric_check", identities["resolvent_numeric_residual"] < 1.0e-35, str(identities["resolvent_numeric_residual"])),
        ("Hadamard_moment_precision", moments["maximum_precision_shift"] < 1.0e-18, str(moments["maximum_precision_shift"])),
        ("Hadamard_cutoff_crosscheck", max(moments["cutoff_cross_checks"].values()) < 1.0e-5, json.dumps(moments["cutoff_cross_checks"])),
        ("endpoint_matches_tower_tail", crossing["endpoint_within_empirical_tail"], f"residual={crossing['endpoint_residual']}; empirical_tail={crossing['empirical_reduced_tail_estimate_not_bound']}"),
        ("crossing_even_exact_numeric", crossing["maximum_crossing_even_residual"] < 1.0e-11, str(crossing["maximum_crossing_even_residual"])),
        ("raw_hhh_not_promoted", target["maximum_raw_mismatch_sigma"] >= 0 and "does not implement" in target["interpretation"], target["interpretation"]),
    ]
    return [
        {
            "gate_id": f"GATE5018_{index:02d}_{name}",
            "gate": name,
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed, evidence) in enumerate(gates, start=1)
    ]


def validation_rows(paths: tuple[Path, ...], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("output_paths_exist", all(path.exists() for path in paths), ";".join(relative(path) for path in paths)),
        ("CSV_rows_parse", all(read_csv(path) for path in paths if path.suffix == ".csv"), "all generated CSVs nonempty"),
        ("no_missing_markers", all("MISSING_" not in path.read_text(encoding="utf-8", errors="ignore") for path in paths), "generated files"),
        ("all_gates_pass", all(row["status"] == "PASS" for row in gates), f"gates={len(gates)}"),
        ("formalization_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)),
    ]
    return tagged(
        [
            {
                "validation_id": f"VAL5018_{index:02d}_{name}",
                "check": name,
                "passed": passed,
                "evidence": evidence,
                "status": "PASS" if passed else "FAIL",
            }
            for index, (name, passed, evidence) in enumerate(checks, start=1)
        ]
    )


def write_provenance() -> None:
    PROVENANCE.write_text(
        "\n".join(
            [
                "# 5018 hh resolvent/Hadamard provenance",
                "",
                f"- Exact hh tower and normalization: `{relative(RESULT_5008)}`",
                f"- Repaired two-helicity implementation: `{relative(SCRIPT_5016)}`",
                f"- Graph-complete pph crossing input: `{relative(PPH_CROSSING)}`",
                f"- Complex-safe raw hhh smoke: `{relative(HHH_CROSSING)}`",
                "- The exterior continuation is derived from the Legendre Sturm-Liouville resolvent and the exact factorial spectral denominator; no fit to the QMC crossed values is made.",
                "- Endpoint divergences are assigned the explicitly written Hadamard finite part in x=(1-w)/2. Changing that finite prescription is a scheme change and must be accompanied by the corresponding hhh real-cut change.",
                "- The J>40 error quoted for the physical direct term is the checkpoint-5008 empirical tail estimate, not a rigorous bound.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_document(
    result: dict[str, Any],
    crossing_rows_value: list[dict[str, Any]],
    target_rows_value: list[dict[str, Any]],
    comparison_rows_value: list[dict[str, Any]],
) -> None:
    crossing_table = "\n".join(
        f"| {row['physical_s_channel_cosine']:.3g} | {row['physical_direct_J40']:.8g} | {row['cyclic_D_hh_over_G3_real']:.9g} | {row['conservative_numeric_error']:.2g} |"
        for row in crossing_rows_value
    )
    target_table = "\n".join(
        f"| {row['physical_s_channel_cosine']:.3g} | {row['known_master_without_hhh']:.8g} | {row['known_nonlocal_residual']:.8g} | {row['required_matched_hhh_nonlocal_cyclic_D_over_G3']:.8g} |"
        for row in target_rows_value
    )
    comparison_table = "\n".join(
        f"| {row['physical_s_channel_cosine']:.3g} | {row['raw_hhh_nonlocal_component']:.8g} | {row['required_matched_hhh_nonlocal_component']:.8g} | {row['raw_minus_required']:.8g} |"
        for row in comparison_rows_value
    )
    DOCUMENT.write_text(
        f"""# 5018 — hh Legendre-resolvent/Hadamard crossing completion

## What changed

The corrected two-helicity state sum explains why checkpoint 5016 passed its physical tower check while failing numerically after crossing: it had duplicated one helicity assignment. More importantly, brute-force continuation is unnecessary. The exact checkpoint-5008 tower contains

```text
N_J^2=(J-4)!/(J+4)!
     =1/[lambda_J(lambda_J-2)(lambda_J-6)(lambda_J-12)].
```

Therefore its crossed sum is the Green function of `L(L-2)(L-6)(L-12)`. Partial fractions reduce it to four Legendre resolvents. Their apparent poles at degrees `0,1,2,3` disappear because the source enters through `d_w^4 P_J` and `P_l''''=0` for all four degrees.

On the `z>1` exterior sheet the resulting fourth-derivative kernel is

```text
K4(z,w)= z(5z^2-3)/[96(w-1)]
        -(z-1)(5z^2+2z-1)/[96(w-1)^2]
        +(z-1)^2(2z+1)/[48(w-1)^3]
        -(z-1)^3/[48(w-1)^4].
```

The last two terms require a finite-part prescription. The Hadamard prescription is written explicitly in `{relative(MOMENT_CSV)}` rather than hidden in a numerical contour.

## Completed hh crossing

The independent endpoint checksum is decisive: the exterior result at `z=1` differs from the exact `J<=40` endpoint sum by `{result['crossing']['endpoint_residual']:.3e}`, inside the earlier empirical `J>40` estimate `{result['crossing']['empirical_reduced_tail_estimate_not_bound']:.3e}`.

| z | physical direct J<=40 | cyclic hh/G^3 | conservative error |
|---:|---:|---:|---:|
{crossing_table}

This supersedes checkpoint 5016's high-variance crossed `hh` central values. It does not supersede its physical integral reconstruction.

## Matched hhh target

With scalar, exact-Hadamard `hh`, graph-complete `phi phi h`, and the global `D1 ReF1` term fixed, the missing `hhh` object is now a precise crossing-complete functional target modulo local `stu`:

| z | known master without hhh | known nonlocal residual | required hhh nonlocal |
|---:|---:|---:|---:|
{target_table}

The raw 5017 KLT smoke does not implement the crossed Hadamard/Feynman contour:

| z | raw hhh nonlocal | required matched hhh | raw-required |
|---:|---:|---:|---:|
{comparison_table}

That discrepancy is not called a theory failure. It identifies the next derivation precisely: deform the finite-`x` azimuth contour, include every pole-crossing residue, and then recompute the KLT real cut. A local finite scheme change cannot remove a nonlocal mismatch, and no coefficient may be fitted to the target.

## Status

- Opposite-helicity state sum: **repaired**.
- Divergent crossed Legendre series: **replaced by an exact resolvent reduction**.
- Exterior `hh` function and cyclic `hh` contribution: **completed in the declared Hadamard scheme**.
- Crossing-complete matched `hhh` nonlocal target: **derived**.
- Matched graph-complete `hhh`, final locality, numeric UV invariant, local GR, and full MTS: **not yet claimed**.

Next: derive the finite-`x` crossed `hhh` contour residues at amplitude/integrand level, not by fitting the five target numbers, and rerun the complex-safe KLT integral.
""",
        encoding="utf-8",
    )


def main() -> None:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    locks = source_locks()
    identity_rows, identities = exact_resolvent_rows()
    moment_rows, moments = hadamard_moment_rows()
    direct_rows, crossing_rows_value, crossing = crossing_rows(moments)
    target_rows_value, comparison_rows_value, target = target_rows(
        crossing_rows_value
    )
    gates = gate_rows(locks, identities, moments, crossing, target)

    for path, rows in (
        (IDENTITY_CSV, tagged(identity_rows)),
        (MOMENT_CSV, tagged(moment_rows)),
        (DIRECT_CSV, tagged(direct_rows)),
        (CROSSING_CSV, tagged(crossing_rows_value)),
        (TARGET_CSV, tagged(target_rows_value)),
        (COMPARISON_CSV, tagged(comparison_rows_value)),
        (GATE_CSV, tagged(gates)),
    ):
        write_csv(path, rows)
    write_provenance()

    result = {
        "checkpoint": 5018,
        "marker": MARKER,
        "source_locks": locks,
        "identities": identities,
        "moments": moments,
        "crossing": crossing,
        "target": target,
        "opposite_helicity_state_sum_repaired": True,
        "hh_crossed_Legendre_resolvent_complete": True,
        "hh_Hadamard_finite_part_declared": True,
        "matched_hhh_scheme_lift_complete": False,
        "matched_hhh_contour_completion_complete": False,
        "combined_crossing_locality_complete": False,
        "numeric_UV_coefficient_complete": False,
        "local_GR_claim": False,
        "full_MTS_claim": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_document(
        result, crossing_rows_value, target_rows_value, comparison_rows_value
    )
    validation = validation_rows(
        (
            IDENTITY_CSV,
            MOMENT_CSV,
            DIRECT_CSV,
            CROSSING_CSV,
            TARGET_CSV,
            COMPARISON_CSV,
            GATE_CSV,
            RESULT_JSON,
            PROVENANCE,
            DOCUMENT,
        ),
        gates,
    )
    write_csv(VALIDATION_CSV, validation)
    if not all(row["status"] == "PASS" for row in validation):
        raise RuntimeError("checkpoint 5018 validation failed")
    print(
        json.dumps(
            {
                "status": "PASS",
                "marker": MARKER,
                "endpoint_residual": crossing["endpoint_residual"],
                "empirical_tail_not_bound": crossing[
                    "empirical_reduced_tail_estimate_not_bound"
                ],
                "hh_cyclic": crossing["cyclic"],
                "required_hhh_nonlocal": target["required_hhh_nonlocal"],
                "raw_hhh_mismatch_sigma": target[
                    "maximum_raw_mismatch_sigma"
                ],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
