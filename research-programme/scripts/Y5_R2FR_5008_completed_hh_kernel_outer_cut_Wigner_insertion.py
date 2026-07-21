from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "5008"

RESULT_4988 = FUNCTIONAL / "4988" / "scalar_cut_soft_subtraction_results.json"
RESULT_4990 = FUNCTIONAL / "4990" / "crossed_cut_D1_scheme_bridge_results.json"
RESULT_4991 = FUNCTIONAL / "4991" / "massless_hh_channel_amplitude_seed_results.json"
RESULT_5005 = FUNCTIONAL / "5005" / "finite_outer_kernel_results.json"
RESULT_5007 = FUNCTIONAL / "5007" / "finite_rational_factorization_closure_results.json"
BARATELLA_SOURCE = FUNCTIONAL / "4985" / "sources" / "baratella" / "draft.tex"

SOFT_CSV = SOURCE / "hh_outer_soft_endpoint_subtraction.csv"
TOWER_CSV = SOURCE / "hh_wigner_partial_wave_tower.csv"
NORMALIZATION_CSV = SOURCE / "hh_direct_cut_normalization.csv"
CROSSING_CSV = SOURCE / "hh_crossed_nonlocality_gate.csv"
GATE_CSV = SOURCE / "hh_outer_insertion_gate.csv"
RESULT_JSON = SOURCE / "hh_outer_Wigner_insertion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5008_VALIDATION.csv"
DOCUMENT = POST / "5008-Y5-R2FR-completed-hh-one-loop-kernel-outer-cut-Wigner-insertion.md"

MARKER = "MTS_5008_COMPLETED_HH_KERNEL_OUTER_CUT_WIGNER_INSERTION"
VALIDATION_MARKER = "P8_Y5_BRR545_5008_VALIDATION"
CHECKED_DATE = "2026-07-14"

angle_x = sp.symbols("x", positive=True)
mandelstam_t, mandelstam_u = sp.symbols("t u", nonzero=True)
log_ratio_x, log_ratio_y = sp.symbols("X Y", real=True)
newton_g = sp.symbols("G", positive=True)


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


def exact(expression: sp.Expr | int) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.sympify(expression)))))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
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


def source_locks(required: list[Path]) -> dict[str, bool]:
    result_4988 = read_json(RESULT_4988)
    result_4990 = read_json(RESULT_4990)
    result_4991 = read_json(RESULT_4991)
    result_5005 = read_json(RESULT_5005)
    result_5007 = read_json(RESULT_5007)
    baratella = BARATELLA_SOURCE.read_text(encoding="utf-8", errors="ignore")
    projection_4988 = json.dumps(result_4988, sort_keys=True)
    return {
        "all_required_paths_exist": all(path.is_file() for path in required),
        "4988_scalar_cut_normalization": "-32/pi sum_J" in projection_4988,
        "4990_direct_hh_minimum_J4": result_4990["hh_scope"]["direct_channel_minimum_J"] == 4,
        "4990_crossed_hh_open": result_4990["hh_scope"]["full_crossed_hh_open"] is True,
        "4991_physical_interference": result_4991.get("physical_interference") == "M1_hh,s M0*=kappa^6 F_hh,s/(4stu)",
        "5005_finite_log_kernel_complete": result_5005.get("finite_logarithmic_outer_kernel_complete") is True,
        "5005_hard_basis_complete": set(result_5005.get("hard_log_basis", {})) == {"X", "X*Y", "X^2", "Y", "Y^2", "pi^2"},
        "5007_rational_remainder_zero": result_5007.get("finite_rational_remainder") == "0",
        "5007_one_loop_kernel_complete": result_5007.get("minimal_massless_Einstein_scalar_opposite_helicity_one_loop_kernel_complete") is True,
        "baratella_identical_state_factor": "statistical factor 1/2" in baratella,
        "baratella_two_equal_helicity_contributions": "two equal contributions" in baratella,
    }


def completed_hard_kernel() -> sp.Expr:
    basis = read_json(RESULT_5005)["hard_log_basis"]
    local_symbols = {
        "t": mandelstam_t,
        "u": mandelstam_u,
        "X": log_ratio_x,
        "Y": log_ratio_y,
        "pi": sp.pi,
    }
    coefficients = {
        name: sp.sympify(formula, locals=local_symbols)
        for name, formula in basis.items()
    }
    expression = coefficients["X^2"] * log_ratio_x**2
    expression += coefficients["Y^2"] * log_ratio_y**2
    expression += coefficients["X*Y"] * log_ratio_x * log_ratio_y
    expression += coefficients["X"] * log_ratio_x
    expression += coefficients["Y"] * log_ratio_y
    expression += coefficients["pi^2"] * sp.pi**2
    return sp.factor(expression)


def physical_kernel() -> tuple[sp.Expr, sp.Expr]:
    formal = completed_hard_kernel().subs(
        {mandelstam_t: -angle_x, mandelstam_u: angle_x - 1}
    )
    analytic = formal.subs(
        {log_ratio_x: sp.log(angle_x), log_ratio_y: sp.log(1 - angle_x)}
    )
    return sp.expand(formal), sp.expand(analytic)


def endpoint_subtraction_rows(
    hard_formal: sp.Expr, hard_analytic: sp.Expr
) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    endpoint_value_left = sp.simplify(sp.limit(hard_analytic, angle_x, 0, dir="+"))
    endpoint_slope_left = sp.simplify(
        sp.limit((hard_analytic - endpoint_value_left) / angle_x, angle_x, 0, dir="+")
    )
    endpoint_value_right = sp.simplify(sp.limit(hard_analytic, angle_x, 1, dir="-"))
    endpoint_slope_right = sp.simplify(
        sp.limit((hard_analytic - endpoint_value_right) / (angle_x - 1), angle_x, 1, dir="-")
    )
    subtraction_constant, subtraction_shape = sp.symbols("a_soft b_soft")
    subtraction_trial = subtraction_constant + subtraction_shape * angle_x * (1 - angle_x)
    solution = sp.solve(
        (
            subtraction_trial.subs(angle_x, 0) - endpoint_value_left,
            sp.diff(subtraction_trial, angle_x).subs(angle_x, 0) - endpoint_slope_left,
        ),
        (subtraction_constant, subtraction_shape),
        dict=True,
    )[0]
    hard_soft = sp.factor(subtraction_trial.subs(solution))
    hard_regular_analytic = sp.expand(hard_analytic - hard_soft)
    hard_regular_formal = sp.expand(hard_formal - hard_soft)
    reduced_regular = sp.cancel(
        hard_regular_analytic / (angle_x**2 * (1 - angle_x) ** 2)
    )
    regular_left = sp.simplify(sp.limit(reduced_regular, angle_x, 0, dir="+"))
    regular_right = sp.simplify(sp.limit(reduced_regular, angle_x, 1, dir="-"))
    crossing_residual = sp.simplify(
        hard_formal
        - hard_formal.subs(
            {
                angle_x: 1 - angle_x,
                log_ratio_x: log_ratio_y,
                log_ratio_y: log_ratio_x,
            },
            simultaneous=True,
        )
    )
    rows = [
        {
            "endpoint_id": "HHEND5008_01_left_value",
            "quantity": "lim_x_to_0 H(x)",
            "derived_value": exact(endpoint_value_left),
            "target_value": "pi**2/16",
            "exact_residual": exact(endpoint_value_left - sp.pi**2 / 16),
            "status": "EXACT",
        },
        {
            "endpoint_id": "HHEND5008_02_left_slope",
            "quantity": "lim_x_to_0 [H(x)-H(0)]/x",
            "derived_value": exact(endpoint_slope_left),
            "target_value": "-5*pi**2/16",
            "exact_residual": exact(endpoint_slope_left + 5 * sp.pi**2 / 16),
            "status": "EXACT",
        },
        {
            "endpoint_id": "HHEND5008_03_right_value",
            "quantity": "lim_x_to_1 H(x)",
            "derived_value": exact(endpoint_value_right),
            "target_value": "pi**2/16",
            "exact_residual": exact(endpoint_value_right - sp.pi**2 / 16),
            "status": "EXACT",
        },
        {
            "endpoint_id": "HHEND5008_04_right_slope",
            "quantity": "lim_x_to_1 [H(x)-H(1)]/(x-1)",
            "derived_value": exact(endpoint_slope_right),
            "target_value": "5*pi**2/16",
            "exact_residual": exact(endpoint_slope_right - 5 * sp.pi**2 / 16),
            "status": "EXACT",
        },
        {
            "endpoint_id": "HHEND5008_05_minimal_quadratic_subtraction",
            "quantity": "H_soft(x)",
            "derived_value": exact(hard_soft),
            "target_value": "pi**2*(1-5*x*(1-x))/16",
            "exact_residual": exact(hard_soft - sp.pi**2 * (1 - 5 * angle_x * (1 - angle_x)) / 16),
            "status": "UNIQUE_CROSSING_EVEN_QUADRATIC_MATCHING_BOTH_ENDPOINT_JETS",
        },
        {
            "endpoint_id": "HHEND5008_06_regular_left",
            "quantity": "lim_x_to_0 [H-H_soft]/[x^2(1-x)^2]",
            "derived_value": exact(regular_left),
            "target_value": "7*pi**2/16",
            "exact_residual": exact(regular_left - 7 * sp.pi**2 / 16),
            "status": "FINITE_EXACT",
        },
        {
            "endpoint_id": "HHEND5008_07_regular_right",
            "quantity": "lim_x_to_1 [H-H_soft]/[x^2(1-x)^2]",
            "derived_value": exact(regular_right),
            "target_value": "7*pi**2/16",
            "exact_residual": exact(regular_right - 7 * sp.pi**2 / 16),
            "status": "FINITE_EXACT",
        },
        {
            "endpoint_id": "HHEND5008_08_crossing",
            "quantity": "H(x;X,Y)-H(1-x;Y,X)",
            "derived_value": exact(crossing_residual),
            "target_value": "0",
            "exact_residual": exact(crossing_residual),
            "status": "EXACT",
        },
    ]
    return rows, {
        "hard_soft": hard_soft,
        "hard_regular_formal": hard_regular_formal,
        "hard_regular_analytic": hard_regular_analytic,
        "reduced_regular": reduced_regular,
        "regular_left": regular_left,
        "regular_right": regular_right,
        "crossing_residual": crossing_residual,
    }


def logarithmic_moment(power_x: int, power_log_x: int, power_log_one_minus_x: int) -> sp.Expr:
    denominator = sp.Integer(power_x + 1)
    harmonic_one = sp.harmonic(power_x + 1)
    harmonic_two = sp.harmonic(power_x + 1, 2)
    key = (power_log_x, power_log_one_minus_x)
    moments = {
        (0, 0): 1 / denominator,
        (1, 0): -1 / denominator**2,
        (2, 0): 2 / denominator**3,
        (0, 1): -harmonic_one / denominator,
        (0, 2): (harmonic_one**2 + harmonic_two) / denominator,
        (1, 1): harmonic_one / denominator**2 - (sp.pi**2 / 6 - harmonic_two) / denominator,
    }
    if key not in moments:
        raise ValueError(f"unsupported logarithmic moment {key}")
    return moments[key]


def exact_log_integral(expression: sp.Expr) -> sp.Expr:
    total = sp.Integer(0)
    logarithmic_polynomial = sp.Poly(sp.expand(expression), log_ratio_x, log_ratio_y)
    for (power_log_x, power_log_one_minus_x), coefficient in logarithmic_polynomial.terms():
        coefficient = sp.cancel(coefficient)
        if sp.denom(coefficient) != 1:
            raise ValueError(f"non-polynomial angular coefficient: {coefficient}")
        angular_polynomial = sp.Poly(sp.expand(coefficient), angle_x)
        for (power_x,), scalar_coefficient in angular_polynomial.terms():
            total += scalar_coefficient * logarithmic_moment(
                power_x, power_log_x, power_log_one_minus_x
            )
    return sp.factor(total)


def wigner_basis(spin_j: int) -> tuple[sp.Expr, sp.Expr]:
    cosine_z = 1 - 2 * angle_x
    normalization = sp.sqrt(sp.factorial(spin_j - 4) / sp.factorial(spin_j + 4))
    wigner_d = sp.expand(normalization * sp.assoc_legendre(spin_j, 4, cosine_z))
    return normalization, wigner_d


def tree_partial_wave_theorem(spin_j: int, normalization: sp.Expr) -> sp.Expr:
    if spin_j < 4 or spin_j % 2:
        return sp.Integer(0)
    return sp.factor(12 * normalization)


def tower_rows(
    hard_formal: sp.Expr, hard_soft: sp.Expr, hard_regular_formal: sp.Expr, spin_max: int
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cumulative_weighted = sp.Integer(0)
    weighted_numeric_values: list[tuple[int, float]] = []
    orthogonality_residuals: list[sp.Expr] = []
    previous_basis: list[tuple[int, sp.Expr]] = []
    for spin_j in range(4, spin_max + 1, 2):
        normalization, wigner_d = wigner_basis(spin_j)
        tree_integral = sp.factor(
            sp.integrate(sp.expand(wigner_d * angle_x * (1 - angle_x)), (angle_x, 0, 1))
        )
        tree_closed = tree_partial_wave_theorem(spin_j, normalization)
        reduced_wigner = sp.cancel(wigner_d / (angle_x**2 * (1 - angle_x) ** 2))
        hard_raw_partial = exact_log_integral(reduced_wigner * hard_formal)
        hard_soft_partial = exact_log_integral(reduced_wigner * hard_soft)
        hard_regular_partial = exact_log_integral(reduced_wigner * hard_regular_formal)
        split_residual = sp.simplify(hard_raw_partial - hard_soft_partial - hard_regular_partial)
        product_regular = sp.factor(tree_integral * hard_regular_partial)
        weighted_mode = sp.factor((2 * spin_j + 1) * product_regular)
        reduced_cut_mode = sp.factor(-64 * weighted_mode / sp.pi)
        cumulative_weighted = sp.factor(cumulative_weighted + weighted_mode)
        weighted_numeric = float(sp.N(weighted_mode, 18))
        weighted_numeric_values.append((spin_j, weighted_numeric))
        for previous_spin, previous_wigner in previous_basis[-3:]:
            orthogonality_residuals.append(
                sp.simplify(
                    sp.integrate(sp.expand(wigner_d * previous_wigner), (angle_x, 0, 1))
                )
            )
        orthogonality_residuals.append(
            sp.simplify(
                sp.integrate(sp.expand(wigner_d**2), (angle_x, 0, 1))
                - sp.Rational(1, 2 * spin_j + 1)
            )
        )
        previous_basis.append((spin_j, wigner_d))
        rows.append(
            {
                "mode_id": f"HHMODE5008_J{spin_j:03d}",
                "spin_J": spin_j,
                "wigner_basis": f"sqrt(({spin_j}-4)!/({spin_j}+4)!) P_{spin_j}^4(1-2x)",
                "tree_partial_wave_exact": exact(tree_integral),
                "tree_closed_form": exact(tree_closed),
                "tree_theorem_residual": exact(tree_integral - tree_closed),
                "hard_raw_partial_wave_exact": exact(hard_raw_partial),
                "hard_soft_partial_wave_exact": exact(hard_soft_partial),
                "hard_regular_partial_wave_exact": exact(hard_regular_partial),
                "hard_split_residual": exact(split_residual),
                "tree_times_regular_exact": exact(product_regular),
                "tree_times_regular_numeric": f"{float(sp.N(product_regular, 18)):.17g}",
                "weighted_mode_exact": exact(weighted_mode),
                "weighted_mode_numeric": f"{weighted_numeric:.17g}",
                "reduced_cut_mode_exact": exact(reduced_cut_mode),
                "reduced_cut_mode_numeric": f"{float(sp.N(reduced_cut_mode, 18)):.17g}",
                "cumulative_weighted_numeric": f"{float(sp.N(cumulative_weighted, 18)):.17g}",
                "status": "EXACT_SOFT_SUBTRACTED_DIRECT_HH_MODE",
            }
        )
    last_spin, last_mode = weighted_numeric_values[-1]
    previous_spin, previous_mode = weighted_numeric_values[-2]
    observed_power = math.log(abs(previous_mode / last_mode)) / math.log(last_spin / previous_spin)
    empirical_tail = abs(last_mode) * last_spin / (2 * (observed_power - 1))
    return rows, {
        "spin_max": spin_max,
        "mode_count": len(rows),
        "tree_partial_wave_closed_form": "a_J=12 sqrt((J-4)!/(J+4)!) for even J>=4; a_J=0 for odd J",
        "tree_theorem_derivation": "four integrations by parts give integral (1-z^2)^3 P_J'''' =48[1+(-1)^J] because the degree-two bulk term is Legendre-orthogonal for J>=4",
        "orthogonality_exact": all(residual == 0 for residual in orthogonality_residuals),
        "weighted_partial_sum_exact": exact(cumulative_weighted),
        "weighted_partial_sum_numeric": float(sp.N(cumulative_weighted, 18)),
        "reduced_cut_partial_sum_numeric": float(sp.N(-64 * cumulative_weighted / sp.pi, 18)),
        "last_weighted_mode_numeric": last_mode,
        "observed_last_pair_power": observed_power,
        "empirical_tail_estimate_not_bound": empirical_tail,
        "arbitrary_even_J_exact_generator": True,
    }


def normalization_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    interference_prefactor = sp.factor((32 * sp.pi * newton_g) ** 3 / (4 * (4 * sp.pi) ** 2))
    phase_space = 1 / (8 * sp.pi)
    identical_state_factor = sp.Rational(1, 2)
    opposite_helicity_assignments = sp.Integer(2)
    two_loop_cut_placements = sp.Integer(2)
    scalar_state_weight = sp.factor(identical_state_factor * two_loop_cut_placements)
    hh_state_weight = sp.factor(
        identical_state_factor * opposite_helicity_assignments * two_loop_cut_placements
    )
    unitarity_weight = sp.factor(
        interference_prefactor * phase_space * hh_state_weight / newton_g**3
    )
    reduced_cut_prefactor = sp.factor(-unitarity_weight / (2 * sp.pi))
    rows = [
        {
            "normalization_id": "HHNORM5008_01_interference",
            "factor": "[kappa^6/(4stu)]/(4pi)^2 with kappa^2=32piG",
            "derived_value": exact(interference_prefactor),
            "exact_residual": exact(interference_prefactor - 512 * sp.pi * newton_g**3),
            "source_path": relative(RESULT_4991),
            "status": "EXACT",
        },
        {
            "normalization_id": "HHNORM5008_02_phase_space",
            "factor": "massless two-body phase space after azimuthal integration",
            "derived_value": exact(phase_space),
            "exact_residual": "0",
            "source_path": relative(BARATELLA_SOURCE),
            "status": "SOURCE_LOCKED",
        },
        {
            "normalization_id": "HHNORM5008_03_identical_state",
            "factor": "identical two-graviton state factor",
            "derived_value": exact(identical_state_factor),
            "exact_residual": "0",
            "source_path": relative(BARATELLA_SOURCE),
            "status": "SOURCE_LOCKED",
        },
        {
            "normalization_id": "HHNORM5008_04_helicity_assignments",
            "factor": "(+,-) and (-,+) momentum-helicity assignments",
            "derived_value": exact(opposite_helicity_assignments),
            "exact_residual": "0",
            "source_path": relative(BARATELLA_SOURCE),
            "status": "SOURCE_LOCKED",
        },
        {
            "normalization_id": "HHNORM5008_05_loop_placements",
            "factor": "M1 M0* plus M0 M1* in the two-loop cut",
            "derived_value": exact(two_loop_cut_placements),
            "exact_residual": "0",
            "source_path": relative(RESULT_4988),
            "status": "CALIBRATED_TO_4988_SCALAR_CUT",
        },
        {
            "normalization_id": "HHNORM5008_06_relative_state_weight",
            "factor": "hh state weight / scalar state weight",
            "derived_value": exact(hh_state_weight / scalar_state_weight),
            "exact_residual": exact(hh_state_weight / scalar_state_weight - 2),
            "source_path": relative(RESULT_4988),
            "status": "EXACT_RELATIVE_TO_SCALAR_BASELINE",
        },
        {
            "normalization_id": "HHNORM5008_07_unitarity_weight",
            "factor": "U_hh/(G^3 s^3) before partial-wave product",
            "derived_value": exact(unitarity_weight),
            "exact_residual": exact(unitarity_weight - 128),
            "source_path": relative(RESULT_4988),
            "status": "EXACT",
        },
        {
            "normalization_id": "HHNORM5008_08_reduced_cut",
            "factor": "D_hh=-U_hh/(2pi s^3)",
            "derived_value": exact(reduced_cut_prefactor),
            "exact_residual": exact(reduced_cut_prefactor + 64 / sp.pi),
            "source_path": relative(RESULT_4988),
            "status": "EXACT",
        },
    ]
    return rows, {
        "interference_prefactor": exact(interference_prefactor),
        "scalar_state_weight": exact(scalar_state_weight),
        "hh_state_weight": exact(hh_state_weight),
        "hh_to_scalar_ratio": exact(hh_state_weight / scalar_state_weight),
        "unitarity_weight": exact(unitarity_weight),
        "reduced_cut_prefactor": exact(reduced_cut_prefactor),
        "direct_cut_formula": "D_hh,s^reg(z)=-(64/pi) sum_{J even>=4}(2J+1) a_J h_J^reg P_J(z)",
    }


def crossing_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    invariant_s = sp.Integer(1)
    invariant_t = -angle_x
    invariant_u = angle_x - 1
    cosine_s = (invariant_u - invariant_t) / invariant_s
    cosine_t = (invariant_u - invariant_s) / invariant_t
    cosine_u = (invariant_s - invariant_t) / invariant_u
    rows: list[dict[str, Any]] = []
    local_status: dict[int, bool] = {}
    for spin_j in (0, 2, 4, 6):
        crossing_sum = sp.factor(
            invariant_s**3 * sp.legendre(spin_j, cosine_s)
            + invariant_t**3 * sp.legendre(spin_j, cosine_t)
            + invariant_u**3 * sp.legendre(spin_j, cosine_u)
        )
        denominator = sp.factor(sp.denom(sp.cancel(crossing_sum)))
        is_local = denominator == 1
        local_status[spin_j] = is_local
        symmetry_residual = sp.simplify(crossing_sum - crossing_sum.subs(angle_x, 1 - angle_x))
        rows.append(
            {
                "crossing_id": f"HHCROSS5008_J{spin_j}",
                "spin_J": spin_j,
                "crossing_sum": exact(crossing_sum),
                "denominator": exact(denominator),
                "crossing_symmetric_residual": exact(symmetry_residual),
                "is_local_polynomial": is_local,
                "belongs_to_direct_hh_tower": spin_j >= 4,
                "projection_status": (
                    "LOCAL_DIAGNOSTIC_BUT_ABSENT_FROM_DIRECT_HH_TOWER"
                    if spin_j < 4
                    else "NONLOCAL_MUST_CANCEL_ONLY_AFTER_COMBINING_REMAINING_CUTS"
                ),
            }
        )
    return rows, {
        "J0_crossing_sum": rows[0]["crossing_sum"],
        "J2_crossing_sum": rows[1]["crossing_sum"],
        "J4_crossing_sum": rows[2]["crossing_sum"],
        "J6_crossing_sum": rows[3]["crossing_sum"],
        "J0_J2_local": local_status[0] and local_status[2],
        "J4_J6_nonlocal": not local_status[4] and not local_status[6],
        "hh_only_local_UV_projection_well_defined": False,
        "reason": "crossed J>=4 terms contain channel denominators; mode-by-mode polynomial division is not crossing covariant",
    }


def validation_rows(
    outputs: list[Path], locks: dict[str, bool], result: dict[str, Any]
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check: str, passed: bool, evidence: str) -> None:
        checks.append(
            {
                "validation_id": f"VAL5008_{len(checks) + 1:04d}_{check}",
                "check": check,
                "passed": bool(passed),
                "evidence": evidence,
                "validation_marker": VALIDATION_MARKER,
            }
        )

    add("all_source_locks", all(locks.values()), json.dumps(locks, sort_keys=True))
    for output in outputs:
        add(f"output_{output.stem}", output.is_file() and output.stat().st_size > 0, str(output))
    csv_outputs = [SOFT_CSV, TOWER_CSV, NORMALIZATION_CSV, CROSSING_CSV, GATE_CSV]
    for output in csv_outputs:
        rows = read_csv(output)
        add(f"csv_parse_{output.stem}", bool(rows), f"rows={len(rows)}")
        add(
            f"csv_marker_{output.stem}",
            all(row.get("checkpoint_marker") == MARKER for row in rows),
            MARKER,
        )
        add(
            f"csv_nonclaim_{output.stem}",
            all(row.get("valid_for_full_MTS_claim", "").lower() == "false" for row in rows),
            "all rows false",
        )
        add(
            f"csv_no_missing_{output.stem}",
            "MISSING_" not in json.dumps(rows),
            output.name,
        )
    endpoint = {row["endpoint_id"]: row for row in read_csv(SOFT_CSV)}
    add(
        "minimal_soft_subtraction",
        endpoint["HHEND5008_05_minimal_quadratic_subtraction"]["exact_residual"] == "0",
        endpoint["HHEND5008_05_minimal_quadratic_subtraction"]["derived_value"],
    )
    add(
        "regular_endpoint_limits",
        endpoint["HHEND5008_06_regular_left"]["exact_residual"] == "0"
        and endpoint["HHEND5008_07_regular_right"]["exact_residual"] == "0",
        "both 7*pi**2/16",
    )
    tower = {int(row["spin_J"]): row for row in read_csv(TOWER_CSV)}
    expected_products = {
        4: "(1279249 + 3332000*pi**2)/526848000",
        6: "(3989437 + 28106400*pi**2)/71124480000",
        8: "(4675265713 + 57501813600*pi**2)/852000145920000",
        10: "(39809226503 + 736900164000*pi**2)/41596540457472000",
        12: "(499769479399 + 12825154742400*pi**2)/2139250652098560000",
    }
    for spin_j, expected in expected_products.items():
        residual = sp.simplify(
            sp.sympify(tower[spin_j]["tree_times_regular_exact"])
            - sp.sympify(expected)
        )
        add(f"mode_J{spin_j}", residual == 0, exact(residual))
    add(
        "all_tree_theorem_residuals",
        all(row["tree_theorem_residual"] == "0" for row in tower.values()),
        result["partial_wave_tower"]["tree_partial_wave_closed_form"],
    )
    add(
        "all_hard_split_residuals",
        all(row["hard_split_residual"] == "0" for row in tower.values()),
        f"modes={len(tower)}",
    )
    normalization = {row["normalization_id"]: row for row in read_csv(NORMALIZATION_CSV)}
    add(
        "reduced_cut_prefactor",
        normalization["HHNORM5008_08_reduced_cut"]["exact_residual"] == "0",
        normalization["HHNORM5008_08_reduced_cut"]["derived_value"],
    )
    crossing = {int(row["spin_J"]): row for row in read_csv(CROSSING_CSV)}
    add(
        "crossing_locality_pattern",
        crossing[0]["is_local_polynomial"].lower() == "true"
        and crossing[2]["is_local_polynomial"].lower() == "true"
        and crossing[4]["is_local_polynomial"].lower() == "false"
        and crossing[6]["is_local_polynomial"].lower() == "false",
        "J0,J2 local diagnostics; J4,J6 nonlocal",
    )
    add(
        "outer_cut_not_overclaimed",
        result["outer_cut_complete"] is False
        and result["full_crossed_hh_UV_projection_complete"] is False
        and result["valid_for_full_MTS_claim"] is False,
        "all claim gates remain false",
    )
    return checks


def write_document(result: dict[str, Any]) -> None:
    tower = result["partial_wave_tower"]
    DOCUMENT.write_text(
        f"""# 5008 - Completed hh one-loop kernel outer-cut Wigner insertion

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a full-MTS, local-GR, or complete two-loop claim.

## What is now inserted

Checkpoint 5007 proved that the finite rational remainder of the minimal massless Einstein-scalar opposite-helicity one-loop amplitude is zero. The 5005 hard kernel is therefore no longer a representative: it is the completed one-loop kernel for this declared sector. In the physical `s=1`, `t=-x`, `u=x-1` channel, its endpoint data are

```text
H(0)=H(1)=pi^2/16,
H'(0)=-5 pi^2/16,
H'(1)=+5 pi^2/16.
```

The unique crossing-even quadratic matching those four endpoint data is

```text
H_soft(x) = (pi^2/16)[1-5x(1-x)].
```

This is uniqueness only inside the minimal quadratic endpoint-subtraction class. Terms of order `x^2(1-x)^2` are integrable finite reallocations and are not silently declared absent. With `H_reg=H-H_soft`,

```text
lim_(x->0,1) H_reg/[x^2(1-x)^2] = 7 pi^2/16.
```

Thus both double and simple endpoint jets are removed, while crossing is preserved exactly.

## Exact helicity tower

For an external scalar pair and an intermediate `h+ h-` pair, the direct channel uses

```text
d^J_{{0,4}}(1-2x) = sqrt((J-4)!/(J+4)!) P_J^4(1-2x),  J>=4.
```

The tree partial wave is not merely tabulated. Four integrations by parts give

```text
a_J = 12 sqrt((J-4)!/(J+4)!)  for even J>=4,
a_J = 0                         for odd J.
```

The boundary term gives `48[1+(-1)^J]`; the remaining degree-two bulk polynomial is orthogonal to `P_J` for `J>=4`. Every hard coefficient is then evaluated exactly from beta-function derivatives for `1`, `log x`, `log(1-x)`, their squares, and their product. The generator is exact for arbitrary requested even `J`; this checkpoint materializes `J=4,...,{tower['spin_max']}`.

The first five products `a_J h_J^reg` are

```text
J=4  : (1279249 + 3332000 pi^2)/526848000
J=6  : (3989437 + 28106400 pi^2)/71124480000
J=8  : (4675265713 + 57501813600 pi^2)/852000145920000
J=10 : (39809226503 + 736900164000 pi^2)/41596540457472000
J=12 : (499769479399 + 12825154742400 pi^2)/2139250652098560000
```

## Direct-cut normalization

Using `M1_hh M0*=kappa^6 F/(4stu)`, `kappa^2=32piG`, the restored one-loop factor `(4pi)^-2`, two-body phase space, the identical-state factor, both opposite-helicity assignments, and both one-loop placements gives

```text
D_hh,s^reg(z)
 = -(64/pi) sum_(J even>=4) (2J+1) a_J h_J^reg P_J(z).
```

The factor is exactly twice the already normalized scalar-cut factor `-32/pi`, as required by the two opposite-helicity assignments. Through `J={tower['spin_max']}`, the weighted partial sum is `{tower['weighted_partial_sum_numeric']:.16g}` and the reduced-cut coefficient is `{tower['reduced_cut_partial_sum_numeric']:.16g}`. The last-pair falloff and tail estimate in the JSON are convergence diagnostics, not rigorous bounds.

## Why the full UV number is not yet legal

The direct hh channel has no `J=0` or `J=2` support. Crossing does not make it disappear: crossing a mode with `J>=4` produces rational channel denominators. For example, the `J=4` and `J=6` crossing sums are non-polynomial even though the full sums are crossing symmetric. Splitting each into a polynomial quotient and remainder is not crossing covariant.

Therefore an hh-only local UV projection is not well-defined. Those nonlocal pieces must be combined with the mixed `hhh` and `phi-phi-h` three-particle cuts before the local `J=0,2` projector is applied. This is a derived coupling requirement, not another unspecified missing-input ledger.

## Result

- Completed one-loop opposite-helicity kernel inserted into the outer two-particle cut: **yes**.
- Minimal endpoint jets and exact helicity tower: **closed**.
- Direct hh normalization: **closed as `-64/pi`**.
- Crossing-complete hh-only local UV subtotal: **forbidden as a standalone object**.
- Full outer cut: **open only on the coupled three-particle completion and final local projection**.

Next: derive the mixed `hhh` and `phi-phi-h` cut integrands in this normalization, combine all three cut classes before any polynomial projection, and test exact cancellation of the crossed nonlocal denominators.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--j-max", type=int, default=40)
    arguments = parser.parse_args()
    if arguments.j_max < 12 or arguments.j_max % 2:
        raise ValueError("--j-max must be an even integer at least 12")

    started = time.perf_counter()
    required = [
        RESULT_4988,
        RESULT_4990,
        RESULT_4991,
        RESULT_5005,
        RESULT_5007,
        BARATELLA_SOURCE,
    ]
    locks = source_locks(required)
    if not all(locks.values()):
        raise RuntimeError(json.dumps(locks, indent=2, sort_keys=True))
    outputs = [
        SOFT_CSV,
        TOWER_CSV,
        NORMALIZATION_CSV,
        CROSSING_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        DOCUMENT,
        VALIDATION,
    ]
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "dry_run": True,
                    "j_max": arguments.j_max,
                    "source_locks": locks,
                    "would_write": [relative(path) for path in outputs],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    hard_formal, hard_analytic = physical_kernel()
    soft_rows, soft_result = endpoint_subtraction_rows(hard_formal, hard_analytic)
    partial_rows, partial_result = tower_rows(
        hard_formal,
        soft_result["hard_soft"],
        soft_result["hard_regular_formal"],
        arguments.j_max,
    )
    norm_rows, norm_result = normalization_rows()
    crossed_rows, crossed_result = crossing_rows()
    gate_rows = [
        {
            "gate": "source_lock",
            "passed": all(locks.values()),
            "status": "closed",
            "meaning": "all amplitude, normalization, and helicity-scope inputs are source locked",
        },
        {
            "gate": "completed_one_loop_kernel",
            "passed": True,
            "status": "closed",
            "meaning": "5005 logarithmic kernel plus the 5007 factorization theorem leaves no rational remainder",
        },
        {
            "gate": "minimal_endpoint_subtraction",
            "passed": all(sp.sympify(row["exact_residual"]) == 0 for row in soft_rows),
            "status": "closed",
            "meaning": "the minimal crossing-even quadratic removes both endpoint value and slope jets",
        },
        {
            "gate": "exact_direct_hh_Wigner_tower",
            "passed": partial_result["orthogonality_exact"],
            "status": f"closed_through_J{arguments.j_max}_with_exact_arbitrary_J_generator",
            "meaning": "Wigner normalization, tree theorem, and logarithmic moments are exact",
        },
        {
            "gate": "direct_hh_cut_normalization",
            "passed": norm_result["reduced_cut_prefactor"] == "-64/pi",
            "status": "closed",
            "meaning": "the state-counted direct reduced cut is normalized relative to the sourced scalar baseline",
        },
        {
            "gate": "hh_only_local_UV_projection",
            "passed": False,
            "status": "not_a_well_defined_standalone_projection",
            "meaning": "crossed J>=4 modes contain nonlocal channel denominators",
        },
        {
            "gate": "combined_three_particle_cancellation",
            "passed": False,
            "status": "next_derivation",
            "meaning": "mixed hhh and phi-phi-h cuts must be combined with hh before local projection",
        },
        {
            "gate": "full_outer_cut",
            "passed": False,
            "status": "open",
            "meaning": "the direct hh branch is inserted but the coupled three-particle completion remains",
        },
        {
            "gate": "full_MTS_claim",
            "passed": False,
            "status": "blocked",
            "meaning": "this is a private Einstein-scalar amplitude-sector result",
        },
    ]
    write_csv(SOFT_CSV, tagged(soft_rows))
    write_csv(TOWER_CSV, tagged(partial_rows))
    write_csv(NORMALIZATION_CSV, tagged(norm_rows))
    write_csv(CROSSING_CSV, tagged(crossed_rows))
    write_csv(GATE_CSV, tagged(gate_rows))
    formal_after = tree_digest(ROOT / "formalization-workbench")
    if formal_before != formal_after:
        raise RuntimeError("formalization-workbench changed during checkpoint")
    source_hashes = {relative(path): digest(path) for path in [*required, Path(__file__).resolve()]}
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_locks": locks,
        "source_hashes_sha256": source_hashes,
        "formalization_workbench_tree_sha256": formal_after,
        "completed_one_loop_opposite_helicity_kernel_inserted": True,
        "finite_rational_remainder": "0",
        "minimal_endpoint_subtraction": exact(soft_result["hard_soft"]),
        "regular_reduced_endpoint_left": exact(soft_result["regular_left"]),
        "regular_reduced_endpoint_right": exact(soft_result["regular_right"]),
        "partial_wave_tower": partial_result,
        "normalization": norm_result,
        "crossing_projection": crossed_result,
        "full_crossed_hh_UV_projection_complete": False,
        "outer_cut_complete": False,
        "remaining_cut_classes": ["mixed_hhh_three_particle", "phi_phi_h_three_particle"],
        "valid_for_full_MTS_claim": False,
        "next_target": "derive and combine the mixed hhh and phi-phi-h three-particle cuts with the completed hh cut before applying the local UV projector",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_document(result)
    PROVENANCE.write_text(
        f"""# 5008 provenance

Checkpoint marker: `{MARKER}`

## Locked local inputs

{chr(10).join(f'- `{path}` - SHA-256 `{value}`' for path, value in source_hashes.items())}

## Method

- Checkpoint 5005 supplies the complete finite logarithmic hard basis.
- Checkpoint 5007 proves the finite rational remainder vanishes, so no fitted term is added here.
- Checkpoint 4991 supplies the exact helicity-phase cancellation and physical interference `M1_hh M0*=kappa^6 F/(4stu)`.
- Checkpoint 4988 supplies the calibrated two-body phase-space convention and scalar reduced-cut factor `-32/pi`.
- Baratella et al., [arXiv:2010.13809](https://arxiv.org/abs/2010.13809), supplies the Wigner partial-wave convention, identical-state factor, opposite-helicity state sum, and gravitational soft regularization.
- Checkpoint 4990 supplies the corrected scope: direct hh support begins at `J=4`, while crossing can feed low external partial waves.

The endpoint subtraction is solved, not fitted. The exact tower uses associated Legendre polynomials and beta-function derivative moments. Crossing is performed before assessing locality; no non-covariant polynomial quotient is promoted to a UV coefficient.
""",
        encoding="utf-8",
    )
    validation = validation_rows(outputs[:-1], locks, result)
    write_csv(VALIDATION, validation)
    if not all(row["passed"] for row in validation):
        failed = [row for row in validation if not row["passed"]]
        raise RuntimeError(json.dumps(failed, indent=2))
    result["validation_checks"] = len(validation)
    result["validation_all_passed"] = True
    result["elapsed_seconds"] = time.perf_counter() - started
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
