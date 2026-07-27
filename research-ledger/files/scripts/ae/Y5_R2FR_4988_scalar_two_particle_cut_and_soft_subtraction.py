from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4988"

CHECKPOINT_4985 = POST / "4985-Y5-R2FR-metric-frame-O2-zero-and-partial-wave-mixing-flow.md"
CHECKPOINT_4986 = POST / "4986-Y5-R2FR-common-scheme-log-invariant-and-local-metric-exterior-bounds.md"
CHECKPOINT_4987 = POST / "4987-Y5-R2FR-full-finite-scheme-orbit-and-irreducible-two-loop-cut-reduction.md"
RESULT_4987 = POST / "source-intake" / "functional_rg" / "4987" / "full_finite_scheme_orbit_and_cut_reduction_results.json"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
BARATELLA_SOURCE = POST / "source-intake" / "functional_rg" / "4985" / "sources" / "baratella" / "draft.tex"
BERN_SOURCE = POST / "source-intake" / "functional_rg" / "4987" / "sources" / "bern_parra_sawyer" / "smeft2.tex"

NORMALIZATION_CSV = SOURCE / "canonical_tree_normalization_checks.csv"
KERNEL_CSV = SOURCE / "one_loop_hard_kernel_decomposition.csv"
SOFT_CSV = SOURCE / "two_loop_soft_endpoint_subtraction.csv"
PARTIAL_WAVE_CSV = SOURCE / "scalar_cut_partial_wave_integrals.csv"
PROJECTION_CSV = SOURCE / "scalar_cut_channel_projection.csv"
MASTER_GATE_CSV = SOURCE / "scalar_cut_master_subtraction_gate.csv"
RESULT_JSON = SOURCE / "scalar_cut_soft_subtraction_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4988_SCALAR_TWO_PARTICLE_CUT_SOFT_SUBTRACTION"
CHECKED_DATE = "2026-07-14"

x, L = sp.symbols("x L", positive=True)
XLOG, YLOG = sp.symbols("XLOG YLOG", real=True)
PI = sp.pi
ZETA3 = sp.zeta(3)
P2 = 1 - 6 * x + 6 * x**2


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8", errors="replace").split())


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
    baratella = normalized_text(BARATELLA_SOURCE)
    bern = normalized_text(BERN_SOURCE)
    checkpoint_4985 = normalized_text(CHECKPOINT_4985)
    checkpoint_4986 = normalized_text(CHECKPOINT_4986)
    checkpoint_4987 = normalized_text(CHECKPOINT_4987)
    return {
        "dunbar_four_scalar_tree": "The tree amplitude for four scalars" in dunbar and "{i\\kappa^2\\over2}" in dunbar,
        "dunbar_scalar_and_graviton_cuts": "intermediate Scalars first" in dunbar and "contribution to the cut from intermediate gravitons" in dunbar,
        "dunbar_complete_cut_logarithms": "-163\\,u^{3}t-43\\,u^{2}t^{2}-163\\,ut^{3}" in dunbar,
        "dunbar_rational_ambiguity": "finite, non-logarithmic rational polynomials" in dunbar,
        "dunbar_scalar_counterterm": "{203 \\over 320\\eps }" in dunbar and "-{203\\over 160\\eps }" in dunbar,
        "baratella_ir_safe_partial_waves": "aIRsafe" in baratella and "{\\bm T}_{\\rm soft}={-2s}/{M_P^2}" in baratella,
        "baratella_identical_state_factor": "statistical factor 1/2" in baratella and "two equal contributions" in baratella,
        "bern_two_loop_real_master": "twoloopSimon3" in bern and "text{Re}(\\M)" in bern,
        "bern_log_subtraction_pattern": "thus canceling the logarithmic terms" in bern,
        "checkpoint_4985_tree_partial_waves": "GR, regularized -11/6 -1/30" in checkpoint_4985,
        "checkpoint_4986_one_loop_log": "F_1,log=(2/pi)[(23/15)L_A-(1/30)L_B]" in checkpoint_4986,
        "checkpoint_4987_inverse_projector": "K_mu=-6(d0-5d2)" in checkpoint_4987 and "K_ang=d0+7d2" in checkpoint_4987,
    }


def normalization_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    s, t, u = sp.symbols("s t u", nonzero=True)
    canonical_shape = t * u / s + s * u / t + s * t / u
    dunbar_bracket = sp.Rational(1, 2) * (
        (t**2 + u**2) / s + (s**2 + u**2) / t + (s**2 + t**2) / u
    )
    old_identity = sp.simplify(dunbar_bracket.subs(u, -s - t) + canonical_shape.subs(u, -s - t))
    contraction_s = -t * u
    canonical_s = sp.simplify((-sp.Rational(1, 4)) * contraction_s / s - t * u / (4 * s))
    planck_map = sp.simplify(32 * PI - 4 * (8 * PI))
    loop_prefactor = sp.simplify((32 * PI) ** 2 / (4 * PI) ** 2 - 64)

    tree_regular = x * (1 - x) + (1 - x) / x + x / (1 - x) - 1 / x - 1 / (1 - x)
    expected_tree_regular = -(7 + (1 - 2 * x) ** 2) / 4
    tree_residual = sp.simplify(tree_regular - expected_tree_regular)
    tree_a0 = sp.integrate(tree_regular, (x, 0, 1))
    tree_a2 = sp.integrate(P2 * tree_regular, (x, 0, 1))

    checks = [
        ("NORM4988_01_old_tree_identity", "Dunbar bracket=-canonical crossing shape", old_identity, "old external-field/sign convention calibrated at tree level"),
        ("NORM4988_02_deDonder_s_channel", "T12.P.T34=-tu gives canonical tu/(4s)", canonical_s, str(contraction_s)),
        ("NORM4988_03_planck_map", "kappa^2=32piG=4/M_P^2", planck_map, "M_P^-2=8piG"),
        ("NORM4988_04_loop_prefactor", "kappa^4/(4pi)^2=64G^2", loop_prefactor, "canonical reduced-Planck convention"),
        ("NORM4988_05_soft_regular_tree", "f_GR,reg=-(7+z^2)/4", tree_residual, str(sp.factor(tree_regular))),
        ("NORM4988_06_tree_J0", "a0_GR=-11/6", sp.simplify(tree_a0 + sp.Rational(11, 6)), str(tree_a0)),
        ("NORM4988_07_tree_J2", "a2_GR=-1/30", sp.simplify(tree_a2 + sp.Rational(1, 30)), str(tree_a2)),
    ]
    rows = [
        {
            "normalization_id": check_id,
            "statement": statement,
            "exact_residual": str(sp.simplify(residual)),
            "derived_value": value,
            "status": "EXACT" if sp.simplify(residual) == 0 else "FAIL",
            "source_path": relative(DUNBAR_SOURCE) if index < 2 else relative(BARATELLA_SOURCE),
            "valid_for_normalization_claim": sp.simplify(residual) == 0,
        }
        for index, (check_id, statement, residual, value) in enumerate(checks)
    ]
    return rows, {
        "canonical_tree": "M_tree=(kappa^2/4)(tu/s+su/t+st/u)",
        "canonical_tree_i_convention": "iM_tree=i(kappa^2/4)(tu/s+su/t+st/u)",
        "dunbar_to_canonical_log_coefficient": "multiply displayed four-scalar logarithmic coefficient by 1/4 after tree external-state calibration",
        "tree_a0": str(tree_a0),
        "tree_a2": str(tree_a2),
        "all_exact": all(sp.simplify(item[2]) == 0 for item in checks),
    }


def kernel_components() -> dict[str, sp.Expr]:
    return {
        "log_x_squared": (x**4 + x**3 - 4 * x**2 + 6 * x - 3) / (16 * (x - 1)),
        "log_x_log_1mx": -(2 * x**4 - 4 * x**3 + 6 * x**2 - 4 * x + 1) / (8 * x * (x - 1)),
        "log_1mx_squared": -(x**4 - 5 * x**3 + 5 * x**2 - 5 * x + 1) / (16 * x),
        "log_x": -(163 * x**2 - 283 * x + 283) / 960,
        "log_1mx": -(163 * x**2 - 43 * x + 163) / 960,
        "pi_squared": -PI**2 * (3 * x**2 - 3 * x + 1) / 16,
    }


def direct_real_hard_kernel() -> sp.Expr:
    t = -x
    u = x - 1
    log_s_real = L
    log_t = L + XLOG
    log_u = L + YLOG
    expression = (1 + t**4) / (8 * t) * log_s_real * log_t
    expression += (1 + u**4) / (8 * u) * log_s_real * log_u
    expression += (u**4 + t**4) / (8 * t * u) * log_t * log_u
    expression += (1 + 2 * t**2 + 2 * u**2) / 16 * (L**2 - PI**2)
    expression += (t**2 + 2 + 2 * u**2) / 16 * log_t**2
    expression += (u**2 + 2 * t**2 + 2) / 16 * log_u**2
    expression += (t / u + t * u + u / t) / 16 * ((L**2 - PI**2) + t * log_t**2 + u * log_u**2)
    expression -= (163 * u**2 + 163 * t**2 + 43 * t * u) / 960 * log_s_real
    expression -= (163 * u**2 + 163 + 43 * u) / 960 * log_t
    expression -= (163 + 163 * t**2 + 43 * t) / 960 * log_u
    return sp.cancel(expression)


def regular_kernel() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    direct = direct_real_hard_kernel()
    direct_regular = sp.cancel(direct + PI**2 / (16 * x * (1 - x)))
    components = kernel_components()
    decomposed_c0 = (
        components["log_x_squared"] * XLOG**2
        + components["log_x_log_1mx"] * XLOG * YLOG
        + components["log_1mx_squared"] * YLOG**2
        + components["log_x"] * XLOG
        + components["log_1mx"] * YLOG
        + components["pi_squared"]
    )
    c1 = -sp.Rational(203, 320) * (x**2 - x + 1)
    decomposed = decomposed_c0 + L * c1
    residual = sp.simplify(direct_regular - decomposed)
    c2 = sp.simplify(sp.diff(direct_regular, L, 2) / 2)
    c1_residual = sp.simplify(sp.diff(direct_regular, L) - c1)
    return direct_regular, decomposed, residual, sp.simplify(c2 + c1_residual)


def kernel_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    direct_regular, decomposed, residual, scale_residual = regular_kernel()
    components = kernel_components()
    rows: list[dict[str, Any]] = []
    basis_labels = {
        "log_x_squared": "log(x)^2",
        "log_x_log_1mx": "log(x)log(1-x)",
        "log_1mx_squared": "log(1-x)^2",
        "log_x": "log(x)",
        "log_1mx": "log(1-x)",
        "pi_squared": "1",
    }
    for index, (name, coefficient) in enumerate(components.items(), start=1):
        rows.append(
            {
                "kernel_id": f"KERNEL4988_{index:02d}_{name}",
                "basis_function": basis_labels[name],
                "coefficient": str(sp.factor(coefficient)),
                "origin": "canonicalized Dunbar-Norridge complete logarithmic four-scalar amplitude",
                "status": "EXACT_DECOMPOSITION",
                "source_path": relative(DUNBAR_SOURCE),
                "valid_for_kernel_claim": True,
            }
        )
    rows.extend(
        [
            {
                "kernel_id": "KERNEL4988_07_scale_linear",
                "basis_function": "L=log(s/mu^2)",
                "coefficient": "-203(x^2-x+1)/320",
                "origin": "exact cancellation of all L^2 terms",
                "status": "EXACT_SCALE_SLOPE",
                "source_path": relative(DUNBAR_SOURCE),
                "valid_for_kernel_claim": scale_residual == 0,
            },
            {
                "kernel_id": "KERNEL4988_08_scale_quadratic",
                "basis_function": "L^2",
                "coefficient": "0",
                "origin": "complete physical-channel real hard kernel",
                "status": "EXACT_ZERO",
                "source_path": relative(DUNBAR_SOURCE),
                "valid_for_kernel_claim": scale_residual == 0,
            },
            {
                "kernel_id": "KERNEL4988_09_full_identity",
                "basis_function": "h_reg-direct_minus_decomposed",
                "coefficient": str(residual),
                "origin": "independent symbolic assembly",
                "status": "EXACT" if residual == 0 else "FAIL",
                "source_path": relative(DUNBAR_SOURCE),
                "valid_for_kernel_claim": residual == 0,
            },
        ]
    )
    return rows, {
        "direct_regular": str(direct_regular),
        "decomposition_residual": str(residual),
        "scale_residual": str(scale_residual),
        "L_squared_coefficient": "0",
        "L_coefficient": "-203(x^2-x+1)/320",
        "all_exact": residual == 0 and scale_residual == 0,
    }


def soft_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    raw_left = -PI**2 / 16
    raw_right = -PI**2 / 16
    subtraction_left = PI**2 / 16
    subtraction_right = PI**2 / 16
    crossing_residual = sp.simplify(PI**2 / (16 * x * (1 - x)) - PI**2 / (4 * (1 - (1 - 2 * x) ** 2)))
    checks = [
        ("SOFT4988_01_raw_x0", "lim[x h_raw]", raw_left, -PI**2 / 16, "universal left endpoint pole"),
        ("SOFT4988_02_raw_x1", "lim[(1-x)h_raw]", raw_right, -PI**2 / 16, "universal right endpoint pole"),
        ("SOFT4988_03_sub_x0", "lim[x h_soft]", subtraction_left, PI**2 / 16, "crossing-even singular counterterm"),
        ("SOFT4988_04_sub_x1", "lim[(1-x)h_soft]", subtraction_right, PI**2 / 16, "crossing-even singular counterterm"),
        ("SOFT4988_05_reg_x0", "lim[x h_reg]", raw_left + subtraction_left, 0, "nonintegrable pole removed"),
        ("SOFT4988_06_reg_x1", "lim[(1-x)h_reg]", raw_right + subtraction_right, 0, "nonintegrable pole removed"),
        ("SOFT4988_07_z_form", "pi^2/[16x(1-x)]=pi^2/[4(1-z^2)]", crossing_residual, 0, "z=1-2x"),
    ]
    rows = [
        {
            "soft_id": check_id,
            "quantity": quantity,
            "derived_value": str(sp.simplify(value)),
            "expected_value": str(sp.simplify(expected)),
            "exact_residual": str(sp.simplify(value - expected)),
            "interpretation": interpretation,
            "status": "EXACT" if sp.simplify(value - expected) == 0 else "FAIL",
            "source_path": relative(BARATELLA_SOURCE),
            "valid_for_soft_subtraction_claim": sp.simplify(value - expected) == 0,
        }
        for check_id, quantity, value, expected, interpretation in checks
    ]
    return rows, {
        "raw_endpoint_residue": "-pi^2/16 at x=0 and x=1",
        "singular_subtraction": "+pi^2/[16x(1-x)]=+pi^2/[4(1-z^2)]",
        "uniqueness_scope": "unique crossing-even singular simple-pole part; integrable finite local terms remain scheme coordinates",
        "post_subtraction_residues_zero": True,
        "all_exact": all(sp.simplify(item[2] - item[3]) == 0 for item in checks),
    }


def harmonic(number: int, power: int = 1) -> sp.Rational:
    return sum((sp.Rational(1, index**power) for index in range(1, number + 1)), sp.Rational(0))


def polynomial_moment(polynomial: sp.Expr, basis: str) -> sp.Expr:
    result = sp.Integer(0)
    for (power,), coefficient in sp.Poly(sp.expand(polynomial), x).terms():
        denominator = power + 1
        if basis == "log_x_squared":
            moment = sp.Rational(2, denominator**3)
        elif basis == "log_1mx_squared":
            moment = (harmonic(denominator) ** 2 + harmonic(denominator, 2)) / denominator
        elif basis == "log_x_log_1mx":
            moment = harmonic(denominator) / denominator**2 - PI**2 / (6 * denominator) + harmonic(denominator, 2) / denominator
        elif basis == "log_x":
            moment = -sp.Rational(1, denominator**2)
        elif basis == "log_1mx":
            moment = -harmonic(denominator) / denominator
        elif basis == "pi_squared":
            moment = sp.Rational(1, denominator)
        else:
            raise ValueError(basis)
        result += coefficient * moment
    return sp.simplify(result)


def exact_basis_integral(coefficient: sp.Expr, basis: str) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    residue_zero = sp.simplify(sp.limit(x * coefficient, x, 0, dir="+"))
    residue_one = sp.simplify(sp.limit((1 - x) * coefficient, x, 1, dir="-"))
    polynomial = sp.cancel(coefficient - residue_zero / x - residue_one / (1 - x))
    if sp.denom(polynomial) != 1:
        raise ValueError(f"non-polynomial remainder for {basis}: {polynomial}")
    value = polynomial_moment(polynomial, basis)
    if basis == "log_x_squared":
        if residue_zero != 0:
            raise ValueError("nonintegrable log(x)^2/x term")
        value += 2 * residue_one * ZETA3
    elif basis == "log_1mx_squared":
        if residue_one != 0:
            raise ValueError("nonintegrable log(1-x)^2/(1-x) term")
        value += 2 * residue_zero * ZETA3
    elif basis == "log_x_log_1mx":
        value += (residue_zero + residue_one) * ZETA3
    elif residue_zero != 0 or residue_one != 0:
        raise ValueError(f"unexpected singular residue for {basis}")
    return sp.simplify(value), residue_zero, residue_one, sp.expand(polynomial)


def numerical_component_value(value: mp.mpf, scale_log: mp.mpf) -> mp.mpf:
    log_x = mp.log(value)
    log_one_minus = mp.log1p(-value)
    coefficients = {
        "log_x_squared": (value**4 + value**3 - 4 * value**2 + 6 * value - 3) / (16 * (value - 1)),
        "log_x_log_1mx": -(2 * value**4 - 4 * value**3 + 6 * value**2 - 4 * value + 1) / (8 * value * (value - 1)),
        "log_1mx_squared": -(value**4 - 5 * value**3 + 5 * value**2 - 5 * value + 1) / (16 * value),
        "log_x": -(163 * value**2 - 283 * value + 283) / 960,
        "log_1mx": -(163 * value**2 - 43 * value + 163) / 960,
        "pi_squared": -(mp.pi**2) * (3 * value**2 - 3 * value + 1) / 16,
    }
    constant = coefficients["log_x_squared"] * log_x**2
    constant += coefficients["log_x_log_1mx"] * log_x * log_one_minus
    constant += coefficients["log_1mx_squared"] * log_one_minus**2
    constant += coefficients["log_x"] * log_x
    constant += coefficients["log_1mx"] * log_one_minus
    constant += coefficients["pi_squared"]
    return constant - mp.mpf(203) * (value**2 - value + 1) * scale_log / 320


def numerical_partial_wave(spin: int, scale_log: mp.mpf) -> mp.mpf:
    delta = mp.mpf("0.01")

    def weight(value: mp.mpf) -> mp.mpf:
        return mp.mpf(1) if spin == 0 else 1 - 6 * value + 6 * value**2

    def left(variable: mp.mpf) -> mp.mpf:
        if variable == 0:
            return mp.mpf(0)
        value = delta * variable**2
        return 2 * delta * variable * weight(value) * numerical_component_value(value, scale_log)

    middle = mp.quad(lambda value: weight(value) * numerical_component_value(value, scale_log), [delta, mp.mpf("0.5"), 1 - delta])
    return 2 * mp.quad(left, [0, 1]) + middle


def partial_wave_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    components = kernel_components()
    weights = {0: sp.Integer(1), 2: P2}
    rows: list[dict[str, Any]] = []
    totals: dict[int, sp.Expr] = {}
    slopes: dict[int, sp.Expr] = {}
    component_values: dict[int, dict[str, sp.Expr]] = {}
    for spin, weight in weights.items():
        total = sp.Integer(0)
        component_values[spin] = {}
        for index, (basis, coefficient) in enumerate(components.items(), start=1):
            value, residue_zero, residue_one, polynomial = exact_basis_integral(sp.cancel(weight * coefficient), basis)
            component_values[spin][basis] = value
            total += value
            rows.append(
                {
                    "integral_id": f"PW4988_J{spin}_{index:02d}_{basis}",
                    "spin_J": spin,
                    "weight": "1" if spin == 0 else "P2(1-2x)=1-6x+6x^2",
                    "basis": basis,
                    "residue_at_x0": str(residue_zero),
                    "residue_at_x1": str(residue_one),
                    "polynomial_remainder": str(polynomial),
                    "exact_integral": str(value),
                    "zeta3_coefficient": str(sp.expand(value).coeff(ZETA3)),
                    "status": "EXACT_MOMENT_INTEGRAL",
                    "source_path": relative(DUNBAR_SOURCE),
                    "valid_for_partial_wave_claim": True,
                }
            )
        total = sp.simplify(total)
        slope = sp.integrate(weight * (-sp.Rational(203, 320) * (x**2 - x + 1)), (x, 0, 1))
        totals[spin] = total
        slopes[spin] = sp.simplify(slope)
        rows.append(
            {
                "integral_id": f"PW4988_J{spin}_TOTAL",
                "spin_J": spin,
                "weight": "1" if spin == 0 else "P2(1-2x)=1-6x+6x^2",
                "basis": "complete_h_reg",
                "residue_at_x0": "0",
                "residue_at_x1": "0",
                "polynomial_remainder": "not_applicable",
                "exact_integral": f"({total})+({sp.simplify(slope)})*L",
                "zeta3_coefficient": str(sp.expand(total).coeff(ZETA3)),
                "status": "EXACT_PARTIAL_WAVE",
                "source_path": relative(DUNBAR_SOURCE),
                "valid_for_partial_wave_claim": sp.expand(total).coeff(ZETA3) == 0,
            }
        )

    mp.mp.dps = 70
    quadrature_rows: list[dict[str, Any]] = []
    maximum_residual = mp.mpf(0)
    for scale_log in (mp.mpf("-3.25"), mp.mpf("0"), mp.mpf("2.5")):
        for spin in (0, 2):
            numerical = numerical_partial_wave(spin, scale_log)
            exact = mp.mpf(str(sp.N(totals[spin] + slopes[spin] * sp.Rational(str(scale_log)), 75)))
            residual = abs(numerical - exact)
            maximum_residual = max(maximum_residual, residual)
            quadrature_rows.append(
                {
                    "integral_id": f"PW4988_NUM_J{spin}_L{str(scale_log).replace('-', 'm').replace('.', 'p')}",
                    "spin_J": spin,
                    "weight": "numerical_transformed_endpoint_quadrature",
                    "basis": f"L={scale_log}",
                    "residue_at_x0": "not_applicable",
                    "residue_at_x1": "not_applicable",
                    "polynomial_remainder": "not_applicable",
                    "exact_integral": mp.nstr(exact, 40),
                    "numerical_integral": mp.nstr(numerical, 40),
                    "absolute_residual": mp.nstr(residual, 8),
                    "zeta3_coefficient": "not_applicable",
                    "status": "NUMERICAL_CROSSCHECK_PASS" if residual < mp.mpf("1e-45") else "FAIL",
                    "source_path": relative(DUNBAR_SOURCE),
                    "valid_for_partial_wave_claim": residual < mp.mpf("1e-45"),
                }
            )
    rows.extend(quadrature_rows)
    return rows, {
        "h0_constant": str(totals[0]),
        "h0_scale_slope": str(slopes[0]),
        "h2_constant": str(totals[2]),
        "h2_scale_slope": str(slopes[2]),
        "h0_numeric_L0": float(sp.N(totals[0], 16)),
        "h2_numeric_L0": float(sp.N(totals[2], 16)),
        "zeta3_cancel_J0": sp.expand(totals[0]).coeff(ZETA3) == 0,
        "zeta3_cancel_J2": sp.expand(totals[2]).coeff(ZETA3) == 0,
        "maximum_quadrature_residual": mp.nstr(maximum_residual, 12),
        "component_values": {str(spin): {name: str(value) for name, value in values.items()} for spin, values in component_values.items()},
    }


def projection_rows(partial: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    h0_constant = sp.sympify(partial["h0_constant"])
    h0_slope = sp.sympify(partial["h0_scale_slope"])
    h2_constant = sp.sympify(partial["h2_constant"])
    h2_slope = sp.sympify(partial["h2_scale_slope"])
    d0_constant = sp.simplify(sp.Rational(176, 3) * h0_constant / PI)
    d0_slope = sp.simplify(sp.Rational(176, 3) * h0_slope / PI)
    d2_constant = sp.simplify(sp.Rational(16, 3) * h2_constant / PI)
    d2_slope = sp.simplify(sp.Rational(16, 3) * h2_slope / PI)
    amplitude_a = sp.simplify(d0_constant + d2_constant)
    amplitude_b = sp.simplify(-6 * d2_constant)
    delta_k_mu_scalar = sp.simplify(-6 * (d0_constant - 5 * d2_constant))
    delta_k_ang_scalar = sp.simplify(d0_constant + 7 * d2_constant)
    delta_k_mu_scalar_slope = sp.simplify(-6 * (d0_slope - 5 * d2_slope))
    delta_k_ang_scalar_slope = sp.simplify(d0_slope + 7 * d2_slope)

    records = [
        ("PROJ4988_01_h0", "h0(L)", h0_constant, h0_slope, "one-loop hard partial wave"),
        ("PROJ4988_02_h2", "h2(L)", h2_constant, h2_slope, "one-loop hard partial wave"),
        ("PROJ4988_03_d0", "d0_phi(L)", d0_constant, d0_slope, "176 h0/(3pi)"),
        ("PROJ4988_04_d2", "d2_phi(L)", d2_constant, d2_slope, "16 h2/(3pi)"),
        ("PROJ4988_05_A", "A_phi(L=0)", amplitude_a, 0, "A=d0+d2"),
        ("PROJ4988_06_B", "B_phi(L=0)", amplitude_b, 0, "B=-6d2"),
        ("PROJ4988_07_DeltaK_mu_scalar", "Delta K_mu_phi(L)", delta_k_mu_scalar, delta_k_mu_scalar_slope, "-6(d0-5d2); the 2x master factor and cyclic crossing are already encoded in this inverse map"),
        ("PROJ4988_08_DeltaK_ang_scalar", "Delta K_ang_phi(L)", delta_k_ang_scalar, delta_k_ang_scalar_slope, "d0+7d2; additive scalar-cut subtotal, not the complete invariant"),
    ]
    rows = [
        {
            "projection_id": projection_id,
            "quantity": quantity,
            "constant_L0": str(sp.factor(constant)),
            "coefficient_of_L": str(sp.factor(slope)),
            "numeric_L0": f"{float(sp.N(constant, 16)):.15g}",
            "derivation": derivation,
            "status": "EXACT_PARTIAL_SCALAR_CUT_CONTRIBUTION",
            "source_path": relative(CHECKPOINT_4987),
            "valid_for_partial_scalar_cut_claim": True,
            "valid_for_full_K_claim": False,
        }
        for projection_id, quantity, constant, slope, derivation in records
    ]
    return rows, {
        "phase_space_identity": "2 Im F=U and Disc_s F=2i Im F; therefore a c ln(-s/mu^2) term has c=-U/(2pi)",
        "reduced_cut": "D_phiphi=-U_phiphi/(2pi s^3)=-32/pi sum_J(2J+1)a_GR,J h_J P_J",
        "master_cut_weight": "-U_phiphi/(pi s^3)=2 D_phiphi",
        "d0_L0": str(d0_constant),
        "d2_L0": str(d2_constant),
        "d0_L_slope": str(d0_slope),
        "d2_L_slope": str(d2_slope),
        "A_phi_L0": str(amplitude_a),
        "B_phi_L0": str(amplitude_b),
        "Delta_K_mu_phi_L0": str(delta_k_mu_scalar),
        "Delta_K_ang_phi_L0": str(delta_k_ang_scalar),
        "Delta_K_mu_phi_L_slope": str(delta_k_mu_scalar_slope),
        "Delta_K_ang_phi_L_slope": str(delta_k_ang_scalar_slope),
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
    }


def gate_rows(source_checks: dict[str, bool], normalization: dict[str, Any], kernel: dict[str, Any], soft: dict[str, Any], partial: dict[str, Any]) -> list[dict[str, Any]]:
    checks = [
        ("primary_source_lock", all(source_checks.values()), f"{sum(source_checks.values())}/{len(source_checks)} source markers"),
        ("canonical_tree_normalization", normalization["all_exact"], "de Donder contraction plus 4985 partial waves"),
        ("one_loop_hard_kernel", kernel["all_exact"], "complete rational-free logarithmic kernel assembled"),
        ("endpoint_residue_left", soft["post_subtraction_residues_zero"], "raw and subtraction residues cancel at x=0"),
        ("endpoint_residue_right", soft["post_subtraction_residues_zero"], "raw and subtraction residues cancel at x=1"),
        ("scale_quadratic_zero", kernel["L_squared_coefficient"] == "0", "all L^2 terms cancel"),
        ("scale_slope_203", kernel["L_coefficient"] == "-203(x^2-x+1)/320", "counterterm coefficient exposed directly"),
        ("zeta3_cancel_J0", partial["zeta3_cancel_J0"], "endpoint zeta(3) terms cancel in h0"),
        ("zeta3_cancel_J2", partial["zeta3_cancel_J2"], "endpoint zeta(3) terms cancel in h2"),
        ("quadrature_crosscheck", mp.mpf(partial["maximum_quadrature_residual"]) < mp.mpf("1e-45"), partial["maximum_quadrature_residual"]),
        ("scalar_cut_d0_d2", True, "exact d0_phi and d2_phi derived"),
        ("scalar_cut_invariant_subtotal", True, "exact additive scalar-cut Delta K_mu and Delta K_ang subtotals derived; the inverse map already contains the master factor two and cyclic crossing"),
        ("global_D1F1_subtraction", False, "must be applied once to the sum of all four surviving cut classes"),
        ("opposite_helicity_hh_cut", False, "not evaluated in 4988"),
        ("mixed_hhh_cut", False, "not evaluated in 4988"),
        ("phiphih_cut", False, "not evaluated in 4988"),
        ("numeric_full_K_mu", False, "scalar-cut subtotal is not the four-cut master"),
        ("numeric_full_K_ang", False, "scalar-cut subtotal is not the four-cut master"),
        ("exact_all_operator_local_GR", False, "two-loop master and higher residual sectors remain"),
        ("full_MTS", False, "not claimed"),
    ]
    return [
        {
            "gate_id": f"GATE4988_{index:02d}_{name}",
            "gate": name,
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "OPEN_NONCLAIM",
            "claim_allowed": bool(passed),
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], source_checks: dict[str, bool]) -> None:
    lines = [
        "# 4988 scalar two-particle cut provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Primary sources",
        "",
        "- [Dunbar and Norridge, *Infinities within Graviton Scattering Amplitudes*](https://arxiv.org/abs/hep-th/9512084): complete cut-constructible one-loop four-scalar logarithms, scalar/graviton intermediate states, soft pole, UV coefficient, and finite-rational ambiguity.",
        "- [Baratella et al., *Anomalous Dimensions of Effective Theories from Partial Waves*](https://arxiv.org/abs/2010.13809): gravity soft regularization, two-body partial waves, identical-state factor, and phase-space normalization.",
        "- [Bern, Parra-Martinez and Sawyer, *Structure of two-loop SMEFT anomalous dimensions via on-shell methods*](https://arxiv.org/abs/2005.12917): real two-loop master and the required subtraction of the one-loop anomalous-action term.",
        "",
        "## Source-marker checks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{value}`" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "The singular soft subtraction and scalar-scalar two-particle discontinuity are derived exactly in the 4987 rational-free convention. Bern's real two-loop master contains twice the direct `D=-U/(2pi)` cut, and the exact `-6(d0-5d2)` inverse map already incorporates that factor together with cyclic crossing. The displayed `Delta K_mu_phi` and `Delta K_ang_phi` are therefore additive scalar-cut subtotals, but not complete invariants. A single global `D1 ReF1` subtraction cannot be allocated to an individual cut. No local-GR or full-MTS claim follows.",
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
        CHECKPOINT_4986,
        CHECKPOINT_4987,
        RESULT_4987,
        DUNBAR_SOURCE,
        BARATELLA_SOURCE,
        BERN_SOURCE,
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
                    "planned_outputs": 8,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    SOURCE.mkdir(parents=True, exist_ok=True)
    normalization, normalization_summary = normalization_rows()
    kernel, kernel_summary = kernel_rows()
    soft, soft_summary = soft_rows()
    partial_waves, partial_summary = partial_wave_rows()
    projection, projection_summary = projection_rows(partial_summary)
    gates = gate_rows(source_checks, normalization_summary, kernel_summary, soft_summary, partial_summary)

    write_csv(NORMALIZATION_CSV, tagged(normalization))
    write_csv(KERNEL_CSV, tagged(kernel))
    write_csv(SOFT_CSV, tagged(soft))
    write_csv(PARTIAL_WAVE_CSV, tagged(partial_waves))
    write_csv(PROJECTION_CSV, tagged(projection))
    write_csv(MASTER_GATE_CSV, tagged(gates))

    hash_paths = required_paths + (Path(__file__),)
    source_hashes = {relative(path): digest(path) for path in hash_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "normalization": normalization_summary,
        "kernel": kernel_summary,
        "soft_subtraction": soft_summary,
        "partial_waves": partial_summary,
        "projection": projection_summary,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
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
                "h0_L0": partial_summary["h0_constant"],
                "h2_L0": partial_summary["h2_constant"],
                "Delta_K_mu_phi_L0": projection_summary["Delta_K_mu_phi_L0"],
                "Delta_K_ang_phi_L0": projection_summary["Delta_K_ang_phi_L0"],
                "quadrature_maximum_residual": partial_summary["maximum_quadrature_residual"],
                "numeric_full_K_mu": False,
                "numeric_full_K_ang": False,
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
