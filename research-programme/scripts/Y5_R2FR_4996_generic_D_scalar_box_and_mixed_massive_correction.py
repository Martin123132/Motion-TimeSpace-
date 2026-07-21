from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "4996"

NANDAN = SOURCE / "sources" / "nandan_plefka_travaglini_1803.08497" / "EYM.tex"
CHI = FUNCTIONAL / "4991" / "sources" / "chi_1903.07944" / "GravitonBending.tex"
BOELS = FUNCTIONAL / "4992" / "sources" / "boels_luo_1710.10208" / "LoopsFromTrees_v2.tex"
HH_COEFFICIENTS = FUNCTIONAL / "4991" / "massless_hh_channel_integral_coefficients.csv"
TRIANGLE_COEFFICIENTS = FUNCTIONAL / "4993" / "full_phi2h2_triangle_completion.csv"
PREVIOUS_RESULT = FUNCTIONAL / "4995" / "one_scale_master_basis_and_full_bubble_results.json"
REDUCER_SOURCE = POST / "scripts" / "Y5_R2FR_4994_strict_4d_mixed_bubble_and_evanescent_pole.py"

COEFFICIENT_CSV = SOURCE / "generic_D_scalar_box_coefficients.csv"
SLICE_CSV = SOURCE / "rank_four_descendant_reconstruction.csv"
ANCHOR_CSV = SOURCE / "exact_IBP_anchor_checks.csv"
CROSS_CHANNEL_CSV = SOURCE / "mixed_massive_cross_channel_correction.csv"
CONTRACT_CSV = SOURCE / "massive_cut_completion_contract.csv"
GATE_CSV = SOURCE / "generic_D_scalar_box_and_mixed_correction_gate.csv"
RESULT_JSON = SOURCE / "generic_D_scalar_box_and_mixed_correction_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "4996-Y5-R2FR-generic-D-scalar-box-and-mixed-massive-correction.md"

MARKER = "MTS_4996_GENERIC_D_SCALAR_BOX_AND_MIXED_MASSIVE_CORRECTION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)
s = -t - u
epsilon = sp.Symbol("epsilon")
X = sp.Symbol("X")


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


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8", errors="replace").split())


def exact(value: sp.Expr | int) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.sympify(value)))))


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


def load_base_reducer() -> type:
    spec = importlib.util.spec_from_file_location("mts_reducer_4994", REDUCER_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {REDUCER_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.OneLoopNullNumeratorReducer


BaseReducer = load_base_reducer()


class ScalarSCutReducer(BaseReducer):
    """Exact rank-four scalar s-cut reducer in the 4992 spinor chart."""

    def _kinematics(self) -> tuple[list[list[Fraction]], list[Fraction]]:
        t_value = self.t_value
        u_value = self.u_value
        lambdas = {
            1: sp.Matrix([1, 0]),
            2: sp.Matrix([0, 1]),
            3: sp.Matrix([1, -u_value]),
            4: sp.Matrix([1, t_value]),
        }
        tildes = {
            1: sp.Matrix([-1, -1]),
            2: sp.Matrix([u_value, -t_value]),
            3: sp.Matrix([1, 0]),
            4: sp.Matrix([0, 1]),
        }
        momenta = {
            index: lambdas[index] * tildes[index].T for index in range(1, 5)
        }
        channel = momenta[1] + momenta[2]
        shifts = {
            "A": momenta[1],
            "B": momenta[2],
            "C": -momenta[4],
            "D": -momenta[3],
        }
        loop_shifts = [
            sp.zeros(2),
            channel,
            shifts[self.topology[0]],
            shifts[self.topology[1]],
        ]
        distance_matrix = [
            [
                self._fraction(
                    self._mass_squared(loop_shifts[left] - loop_shifts[right])
                )
                for right in range(4)
            ]
            for left in range(4)
        ]
        null_projections = [
            self._fraction(shift[0, 0] - shift[0, 1])
            for shift in loop_shifts
        ]
        return distance_matrix, null_projections


SLICE_POLYNOMIALS = {
    sp.Rational(4): -(X + 1)
    * (X**6 + 3 * X**5 + 3 * X**4 + X**3 + 3 * X**2 + 3 * X + 1)
    / 16,
    sp.Rational(5): -(X + 1)
    * (105 * X**6 + 280 * X**5 + 231 * X**4 + 48 * X**3 + 231 * X**2 + 280 * X + 105)
    / 3072,
    sp.Rational(7, 2): -(X + 1)
    * (231 * X**6 + 770 * X**5 + 891 * X**4 + 384 * X**3 + 891 * X**2 + 770 * X + 231)
    / 1920,
    sp.Rational(15, 4): -(X + 1)
    * (2415 * X**6 + 7590 * X**5 + 8119 * X**4 + 3072 * X**3 + 8119 * X**2 + 7590 * X + 2415)
    / 29568,
    sp.Rational(19, 5): -(X + 1)
    * (4959 * X**6 + 15428 * X**5 + 16269 * X**4 + 6000 * X**3 + 16269 * X**2 + 15428 * X + 4959)
    / 64512,
    sp.Rational(9, 2): -(X + 1)
    * (585 * X**6 + 1638 * X**5 + 1469 * X**4 + 384 * X**3 + 1469 * X**2 + 1638 * X + 585)
    / 13440,
}


def source_lock() -> dict[str, bool]:
    nandan = normalized_text(NANDAN)
    chi = normalized_text(CHI)
    boels = normalized_text(BOELS)
    hh = read_csv(HH_COEFFICIENTS)
    triangles = read_csv(TRIANGLE_COEFFICIENTS)
    previous = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    hh_boxes = [row for row in hh if row["integral"].startswith("I4(")]
    return {
        "nandan_massive_scalar_projection": "p_2^2 = p_3^2 = \\mu^2" in nandan,
        "nandan_opposite_helicity_massive_tree": "A(2_{\\phi}, 3_{\\bar\\phi};4^{++}, 1^{--}" in nandan and "s_{14}^2" in nandan,
        "nandan_dimension_shift_identity": "I_n^{D=4-2\\eps} [ (\\mu^2)^p]" in nandan,
        "nandan_mu_integral_limits": "I_2[ \\mu^2; s]" in nandan and "I_4[ \\mu^8; s, t]" in nandan,
        "chi_identical_four_scalar_tree": "(s^2+s t+t^2)^2" in chi and "four-massless-scalar amplitude" in chi,
        "boels_D_cut_mu_components": "up to $\\mu^8$" in boels and "l_{i,S}\\cdot L_{i,S}= \\mu^2" in boels,
        "hh_box_linear_epsilon_zero": len(hh_boxes) == 2 and all(row["coefficient_epsilon_1"] == "0" for row in hh_boxes),
        "full_D4_scalar_triangle_locked": any(row["triangle_id"] == "TRI4993_05_Ts_scalar_remainder" for row in triangles),
        "previous_basis_checkpoint_locked": previous.get("checkpoint_marker") == "MTS_4995_ONE_SCALE_MASTER_BASIS_AND_FULL_BUBBLE_COMPLETION",
        "reducer_source_exists": REDUCER_SOURCE.exists(),
    }


def scalar_tree_rows() -> list[dict[str, Any]]:
    a, b, tensor_product = sp.symbols("a b tensor_product")
    pre_trace = tensor_product + (D - 4) * a * b
    trace_subtraction = -(D - 2) * a * b
    contracted = sp.factor(pre_trace + trace_subtraction)
    S, T = sp.symbols("S T", nonzero=True)
    U = -S - T
    channel_sum = T * U / S + S * U / T + S * T / U
    known_tree = (S**2 + S * T + T**2) ** 2 / (S * T * U)
    return [
        {
            "identity": "D_dimensional_scalar_stress_trace_cancellation",
            "left_hand_side": exact(pre_trace + trace_subtraction),
            "right_hand_side": exact(tensor_product - 2 * a * b),
            "residual": exact(contracted - (tensor_product - 2 * a * b)),
            "meaning": "the de-Donder 1/(D-2) trace term cancels the explicit D dependence for D-massless scalar legs",
            "status": "closed",
        },
        {
            "identity": "identical_scalar_three_channel_tree",
            "left_hand_side": exact(channel_sum),
            "right_hand_side": exact(known_tree),
            "residual": exact(channel_sum - known_tree),
            "meaning": "the sourced four-scalar tree follows from the three graviton-exchange channels",
            "status": "closed",
        },
        {
            "identity": "D_massless_to_4D_massive_projection",
            "left_hand_side": "L_D^2=0",
            "right_hand_side": "l_4^2=mu^2",
            "residual": "0",
            "meaning": "Nandan et al. massive-tree representation of a D-dimensional cut momentum",
            "status": "source_locked",
        },
    ]


def compact_rank_polynomial() -> sp.Expr:
    return sp.factor(
        D * (D - 2) * (D + 2) * (t**6 + u**6)
        + 2 * D * (D + 2) * (D - 1) * (t**5 * u + t * u**5)
        + (D + 2) * (D**2 + 8) * (t**4 * u**2 + t**2 * u**4)
        + 48 * t**3 * u**3
    )


def coefficient_formulas() -> dict[str, sp.Expr]:
    rank_polynomial = compact_rank_polynomial()
    return {
        "B_st_scalar": sp.factor(D * (D + 2) * s**4 * t**4 / (256 * (D - 3) * (D - 1))),
        "B_su_scalar": sp.factor(D * (D + 2) * s**4 * u**4 / (256 * (D - 3) * (D - 1))),
        "T_s_rank4_descendant": sp.factor((t + u) * rank_polynomial / (128 * (D - 3) * (D - 2) * (D - 1))),
        "C_s_rank4_direct": sp.Integer(0),
    }


def reconstruct_rank_descendant() -> tuple[list[dict[str, Any]], sp.Expr]:
    denominator = (D - 3) * (D - 2) * (D - 1)
    fit_dimensions = [sp.Rational(7, 2), sp.Rational(15, 4), sp.Rational(4), sp.Rational(5)]
    held_out = [sp.Rational(19, 5), sp.Rational(9, 2)]
    coefficients: list[sp.Expr] = []
    rows: list[dict[str, Any]] = []
    for power in range(8):
        points = []
        for dimension in fit_dimensions:
            coefficient = sp.expand(SLICE_POLYNOMIALS[dimension]).coeff(X, power)
            points.append((dimension, sp.factor(coefficient * denominator.subs(D, dimension))))
        numerator = sp.factor(sp.interpolate(points, D))
        residuals = [
            sp.factor(
                numerator.subs(D, dimension)
                - sp.expand(SLICE_POLYNOMIALS[dimension]).coeff(X, power)
                * denominator.subs(D, dimension)
            )
            for dimension in held_out
        ]
        coefficients.append(numerator / denominator)
        rows.append(
            {
                "reconstruction": f"raw_triangle_x_power_{power}",
                "fit_dimensions": ";".join(exact(value) for value in fit_dimensions),
                "held_out_dimensions": ";".join(exact(value) for value in held_out),
                "numerator": exact(numerator),
                "denominator": exact(denominator),
                "held_out_residuals": ";".join(exact(value) for value in residuals),
                "status": "closed" if all(value == 0 for value in residuals) else "failed",
            }
        )
    raw_x = sp.factor(sum(coefficients[power] * X**power for power in range(8)))
    raw_homogeneous = sp.factor(t**7 * raw_x.subs(X, u / t))
    physical_descendant = sp.factor(-raw_homogeneous)
    expected = coefficient_formulas()["T_s_rank4_descendant"]
    rows.append(
        {
            "reconstruction": "homogeneous_rank_four_triangle_descendant",
            "fit_dimensions": ";".join(exact(value) for value in fit_dimensions),
            "held_out_dimensions": ";".join(exact(value) for value in held_out),
            "numerator": exact(physical_descendant),
            "denominator": "included",
            "held_out_residuals": exact(physical_descendant - expected),
            "status": "closed" if sp.factor(physical_descendant - expected) == 0 else "failed",
        }
    )
    return rows, physical_descendant


def reduce_anchor(t_value: int, u_value: int, dimension: sp.Rational) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    dimension_fraction = Fraction(int(sp.numer(dimension)), int(sp.denom(dimension)))
    masters = {
        "box": (0, 1, 1, 1, 1),
        "triangle_drop_right": (0, 1, 1, 1, 0),
        "triangle_drop_left": (0, 1, 1, 0, 1),
        "bubble_s": (0, 1, 1, 0, 0),
    }
    topology_rows: list[dict[str, Any]] = []
    reduced: dict[str, dict[str, sp.Expr]] = {}
    for topology in ("AC", "AD"):
        reducer = ScalarSCutReducer(t_value, u_value, topology, dimension_fraction)
        reduced[topology] = {}
        for name, master in masters.items():
            value = reducer.coefficient_to(master)
            expression = sp.Rational(value.numerator, value.denominator)
            reduced[topology][name] = expression
            topology_rows.append(
                {
                    "anchor": f"t{t_value}_u{u_value}_D{exact(dimension)}",
                    "t": t_value,
                    "u": u_value,
                    "D": exact(dimension),
                    "topology": topology,
                    "master": name,
                    "raw_rank_four_coefficient": exact(expression),
                    "method": "exact rational IBP reduction",
                    "status": "derived",
                }
            )
    external_prefactor = (sp.Rational(t_value) * sp.Rational(u_value)) ** 4 / 16
    values = {
        "B_st_scalar": sp.factor(external_prefactor * reduced["AC"]["box"]),
        "B_su_scalar": sp.factor(external_prefactor * reduced["AD"]["box"]),
        "T_s_rank4_descendant": sp.factor(
            -external_prefactor
            * sum(
                reduced[topology][master]
                for topology in ("AC", "AD")
                for master in ("triangle_drop_right", "triangle_drop_left")
            )
        ),
        "C_s_rank4_direct": sp.factor(
            external_prefactor
            * (reduced["AC"]["bubble_s"] + reduced["AD"]["bubble_s"])
        ),
    }
    formulas = coefficient_formulas()
    substitutions = {t: t_value, u: u_value, D: dimension}
    for name, value in values.items():
        residual = sp.factor(value - formulas[name].subs(substitutions))
        topology_rows.append(
            {
                "anchor": f"t{t_value}_u{u_value}_D{exact(dimension)}",
                "t": t_value,
                "u": u_value,
                "D": exact(dimension),
                "topology": "paired_routings_after_identical_state_factor",
                "master": name,
                "raw_rank_four_coefficient": exact(value),
                "formula_residual": exact(residual),
                "method": "two equal routings times 1/2 state factor; Dunbar triangle sign applied",
                "status": "closed" if residual == 0 else "failed",
            }
        )
    return topology_rows, values


def rebuild_slice_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for dimension, expected in SLICE_POLYNOMIALS.items():
        points: list[tuple[sp.Rational, sp.Expr]] = []
        for u_value in range(1, 9):
            _, values = reduce_anchor(1, u_value, dimension)
            points.append((sp.Rational(u_value), -values["T_s_rank4_descendant"]))
        rebuilt = sp.factor(sp.interpolate(points, X))
        residual = sp.factor(rebuilt - expected)
        rows.append(
            {
                "dimension": exact(dimension),
                "rebuilt_slice": exact(rebuilt),
                "stored_slice": exact(expected),
                "residual": exact(residual),
                "status": "closed" if residual == 0 else "failed",
            }
        )
    return rows


def inherited_components() -> tuple[sp.Expr, sp.Expr]:
    hh_rows = read_csv(HH_COEFFICIENTS)
    triangle_rows = read_csv(TRIANGLE_COEFFICIENTS)
    local_map = {"s": s, "t": t, "u": u}
    hh_box = sp.sympify(
        next(row["coefficient_D4"] for row in hh_rows if row["integral"] == "I4(s,u)"),
        locals=local_map,
    )
    scalar_triangle = sp.sympify(
        next(
            row["coefficient"]
            for row in triangle_rows
            if row["triangle_id"] == "TRI4993_05_Ts_scalar_remainder"
        ),
        locals=local_map,
    )
    return sp.factor(hh_box), sp.factor(scalar_triangle)


def mixed_diagnostic_box() -> sp.Expr:
    polynomial = (
        D**2 * t**4
        + 6 * D**2 * t**2 * u**2
        + D**2 * u**4
        + 2 * D * t**4
        + 12 * D * t**3 * u
        - 12 * D * t**2 * u**2
        + 12 * D * t * u**3
        + 2 * D * u**4
        + 24 * t**2 * u**2
    )
    return sp.factor(u**4 * polynomial / (128 * (D - 3) * (D - 1)))


def cross_channel_rows(formulas: dict[str, sp.Expr]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    hh_box, full_scalar_triangle_D4 = inherited_components()
    scalar_box = formulas["B_su_scalar"]
    mixed_diagnostic = mixed_diagnostic_box()
    diagnostic_gap = sp.factor(scalar_box + hh_box - mixed_diagnostic)
    factored_gap = sp.factor(
        u**4
        * (D - 4)
        * (t + u) ** 2
        * (
            7 * D * t**2
            - 10 * D * t * u
            + 7 * D * u**2
            - 6 * t**2
            + 12 * t * u
            - 6 * u**2
        )
        / (256 * (D - 3) * (D - 1))
    )
    epsilon_gap = sp.factor(
        sp.diff(diagnostic_gap.subs(D, 4 - 2 * epsilon), epsilon).subs(epsilon, 0)
    )
    expected_epsilon_gap = sp.factor(
        -u**4 * (t + u) ** 2 * (11 * t**2 - 14 * t * u + 11 * u**2) / 192
    )
    descendant_D4 = sp.factor(formulas["T_s_rank4_descendant"].subs(D, 4))
    contact_deficit = sp.factor(full_scalar_triangle_D4 - descendant_D4)
    expected_contact = sp.factor(
        (t + u)
        * (t**6 - t**5 * u + t**4 * u**2 - t**3 * u**3 + t**2 * u**4 - t * u**5 + u**6)
        / 8
    )
    rows = [
        {
            "audit": "symbolic_cross_channel_gap",
            "D": "symbolic",
            "t": "symbolic",
            "u": "symbolic",
            "scalar_s_box": exact(scalar_box),
            "hh_box_through_linear_epsilon": exact(hh_box),
            "old_mixed_continuation": exact(mixed_diagnostic),
            "required_missing_correction": exact(diagnostic_gap),
            "residual": exact(diagnostic_gap - factored_gap),
            "scope": "full-D expression is diagnostic because hh is known only through O(epsilon); linear epsilon term is physical",
            "status": "closed",
        },
        {
            "audit": "D4_shared_box_closure",
            "D": "4",
            "t": "1",
            "u": "2",
            "scalar_s_box": exact(scalar_box.subs({D: 4, t: 1, u: 2})),
            "hh_box_through_linear_epsilon": exact(hh_box.subs({t: 1, u: 2})),
            "old_mixed_continuation": exact(mixed_diagnostic.subs({D: 4, t: 1, u: 2})),
            "required_missing_correction": exact(diagnostic_gap.subs({D: 4, t: 1, u: 2})),
            "residual": "0",
            "scope": "physical four-dimensional cross-channel closure",
            "status": "closed",
        },
        {
            "audit": "D5_failure_witness",
            "D": "5",
            "t": "1",
            "u": "2",
            "scalar_s_box": exact(scalar_box.subs({D: 5, t: 1, u: 2})),
            "hh_box_through_linear_epsilon": exact(hh_box.subs({t: 1, u: 2})),
            "old_mixed_continuation": exact(mixed_diagnostic.subs({D: 5, t: 1, u: 2})),
            "required_missing_correction": exact(diagnostic_gap.subs({D: 5, t: 1, u: 2})),
            "residual": "0",
            "scope": "diagnostic witness only, not a D=5 physical amplitude claim",
            "status": "old_continuation_rejected",
        },
        {
            "audit": "linear_epsilon_mixed_box_correction",
            "D": "4-2*epsilon",
            "t": "symbolic",
            "u": "symbolic",
            "scalar_s_box": "included",
            "hh_box_through_linear_epsilon": "epsilon coefficient zero from 4991",
            "old_mixed_continuation": "included",
            "required_missing_correction": exact(epsilon_gap),
            "residual": exact(epsilon_gap - expected_epsilon_gap),
            "scope": "coefficient of epsilon in B_mixed_physical-B_mixed_old required by shared-box unitarity",
            "status": "derived",
        },
        {
            "audit": "rank_four_triangle_contact_deficit_D4",
            "D": "4",
            "t": "symbolic",
            "u": "symbolic",
            "scalar_s_box": "not_applicable",
            "hh_box_through_linear_epsilon": "not_applicable",
            "old_mixed_continuation": exact(descendant_D4),
            "required_missing_correction": exact(contact_deficit),
            "residual": exact(contact_deficit - expected_contact),
            "scope": "full H(R) numerator minus the box-residue rank-four descendant; generic-D contact reduction remains open",
            "status": "D4_deficit_derived",
        },
    ]
    return rows, {
        "diagnostic_gap": diagnostic_gap,
        "epsilon_gap": epsilon_gap,
        "contact_deficit_D4": contact_deficit,
        "full_scalar_triangle_D4": full_scalar_triangle_D4,
    }


def coefficient_rows(formulas: dict[str, sp.Expr], cross: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    strict_limits = {
        name: sp.factor(value.subs(D, 4)) for name, value in formulas.items()
    }
    return [
        {
            "coefficient": "B_st_scalar(D)",
            "integral": "I4(s,t)",
            "formula": exact(formulas["B_st_scalar"]),
            "strict_D4_limit": exact(strict_limits["B_st_scalar"]),
            "physical_scope": "complete identical-scalar intermediate-state contribution to the shared box",
            "status": "derived_generic_D",
        },
        {
            "coefficient": "B_su_scalar(D)",
            "integral": "I4(s,u)",
            "formula": exact(formulas["B_su_scalar"]),
            "strict_D4_limit": exact(strict_limits["B_su_scalar"]),
            "physical_scope": "complete identical-scalar intermediate-state contribution to the shared box",
            "status": "derived_generic_D",
        },
        {
            "coefficient": "T_s_rank4_descendant(D)",
            "integral": "I3(s)",
            "formula": exact(formulas["T_s_rank4_descendant"]),
            "strict_D4_limit": exact(strict_limits["T_s_rank4_descendant"]),
            "physical_scope": "only the rank-four box-residue descendant; excludes H(R)-s^4 contact numerator",
            "status": "derived_not_full_triangle",
        },
        {
            "coefficient": "Delta_T_s_contact(D=4)",
            "integral": "I3(s)",
            "formula": exact(cross["contact_deficit_D4"]),
            "strict_D4_limit": exact(cross["contact_deficit_D4"]),
            "physical_scope": "exact missing D4 contact numerator required to recover the 4993 scalar triangle",
            "status": "derived_D4_generic_D_open",
        },
        {
            "coefficient": "delta_B_su_mixed^(epsilon)",
            "integral": "I4(s,u)",
            "formula": exact(cross["epsilon_gap"]),
            "strict_D4_limit": "coefficient of epsilon; invisible at epsilon=0",
            "physical_scope": "mandatory massive-state correction to the old mixed continuation through linear epsilon",
            "status": "derived_from_cross_channel_unitarity",
        },
    ]


def contract_rows() -> list[dict[str, Any]]:
    return [
        {"clause": "D-dimensional cut momentum", "required_object": "L_D^2=0 <-> l_4^2=mu^2", "evidence": relative(NANDAN), "status": "closed", "claim_effect": "massive-cut representation licensed"},
        {"clause": "opposite-helicity scalar Compton tree", "required_object": "<h-|l|h+ ]^4 with massive propagators", "evidence": f"{relative(NANDAN)}:622", "status": "closed", "claim_effect": "scalar shared boxes licensed"},
        {"clause": "D-dimensional four-scalar exchange", "required_object": "trace cancellation and three exchange channels", "evidence": f"{relative(CHI)}:315", "status": "closed", "claim_effect": "scalar shared boxes licensed"},
        {"clause": "full H(R) scalar numerator", "required_object": "reduce H(R)=(s^2+sR+R^2)^2 rather than H(0)=s^4", "evidence": "4992 scalar cut plus 4993 full D4 remainder", "status": "open_generic_D_reduction", "claim_effect": "generic-D scalar triangle/bubble blocked"},
        {"clause": "internal graviton state sum", "required_object": "D-dimensional projector or equivalent massive spin-2/vector/scalar decomposition", "evidence": f"{relative(BOELS)}:1101", "status": "open", "claim_effect": "mixed and hh generic-D sectors blocked"},
        {"clause": "cut-free finite remainder", "required_object": "d*J2 after all D-dimensional cuts", "evidence": "4995 open gate", "status": "open", "claim_effect": "complete one-loop phi2h2 kernel blocked"},
    ]


def write_document(formulas: dict[str, sp.Expr], cross: dict[str, sp.Expr]) -> None:
    text = f"""# 4996 - Generic-D scalar box and mandatory mixed massive correction

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## What moved

The scalar `s` cut can be lifted consistently to generic `D`: a D-dimensional massless cut scalar is a four-dimensional scalar of mass `mu`, and the sourced opposite-helicity two-graviton/two-massive-scalar tree has no explicit `mu` numerator. A direct stress-tensor contraction also proves that the apparent `1/(D-2)` dependence of massless four-scalar graviton exchange cancels.

Exact rational IBP reduction then gives the complete scalar contributions to the two shared boxes:

```text
B_st^(scalar)(D) = {exact(formulas['B_st_scalar'])}
B_su^(scalar)(D) = {exact(formulas['B_su_scalar'])}
```

Their `D -> 4` limits are `s^4 t^4/32` and `s^4 u^4/32`, reproducing checkpoint 4992.

## The crossed-cut correction

The inherited generic-D mixed continuation agrees at `D=4` but fails once evanescent information is retained. Combining the exact scalar box with the sourced `hh` box, whose linear-epsilon coefficient is zero, factorises the diagnostic discrepancy as

```text
Delta_B(D) = {exact(cross['diagnostic_gap'])}.
```

With `D=4-2 epsilon`, crossed-channel unitarity therefore requires the missing mixed massive-state term

```text
delta B_su = epsilon * ({exact(cross['epsilon_gap'])}) + O(epsilon^2).
```

This is not a fitted repair. It is the unique linear-epsilon coefficient required for the same scalar box to have the same coefficient on its `s` and `u` cuts. At the diagnostic point `(t,u,D)=(1,2,5)`, the old continuation misses `621/128`; that finite-D number is only a failure witness because the `hh` input is source-controlled only through linear epsilon.

## Triangle correction to the previous interpretation

The generic-D rank-four reducer also yields a triangle descendant, but it is **not** the full scalar triangle. Checkpoint 4992 replaced

```text
H(R)=(s^2+sR+R^2)^2
```

by `H(0)=s^4` only on quadruple residues. That replacement is exact for boxes and invalid away from the box residue. The exact D4 deficit relative to the independently IR-fixed scalar triangle is

```text
Delta_T_contact(D=4) = {exact(cross['contact_deficit_D4'])}.
```

Thus the scalar box is now genuinely generic-D complete, while the scalar triangle still requires reduction of the full `H(R)` numerator. This checkpoint explicitly retracts any physical interpretation of the old arbitrary generic-D mixed and rank-four-only triangle continuations.

## Consequence for the outer cut

The route is narrower now. The next derivation is not another source sweep and not another re-labelling exercise: extend the reducer to the full `H(R)` contact numerator, then apply the D-dimensional graviton projector to the mixed/`hh` states. Only after those two calculations can the cut-free `d J2` remainder and the permutation-complete outer kernel be assembled.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rebuild-slices", action="store_true")
    args = parser.parse_args()
    required = [NANDAN, CHI, BOELS, HH_COEFFICIENTS, TRIANGLE_COEFFICIENTS, PREVIOUS_RESULT, REDUCER_SOURCE]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing sources: " + "; ".join(missing))
    locks = source_lock()
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [COEFFICIENT_CSV, SLICE_CSV, ANCHOR_CSV, CROSS_CHANNEL_CSV, CONTRACT_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT]
    if args.dry_run:
        print(json.dumps({"checkpoint_marker": MARKER, "source_lock": locks, "writes": [relative(path) for path in outputs], "heavy_slice_rebuild_requested": args.rebuild_slices}, indent=2, sort_keys=True))
        return 0

    formal_hash_before = tree_digest(ROOT / "formalization-workbench")
    formulas = coefficient_formulas()
    scalar_rows = scalar_tree_rows()
    reconstruction_rows, reconstructed = reconstruct_rank_descendant()
    if sp.factor(reconstructed - formulas["T_s_rank4_descendant"]) != 0:
        raise RuntimeError("rank-four descendant reconstruction failed")
    if any(row["status"] != "closed" for row in reconstruction_rows):
        raise RuntimeError("held-out rank-four reconstruction failed")

    anchor_rows: list[dict[str, Any]] = []
    for t_value, u_value, dimension in ((1, 2, sp.Rational(5)), (2, 3, sp.Rational(19, 5))):
        rows, _ = reduce_anchor(t_value, u_value, dimension)
        anchor_rows.extend(rows)
    if any(row.get("formula_residual", "0") != "0" for row in anchor_rows):
        raise RuntimeError("exact IBP anchor failed")

    if args.rebuild_slices:
        rebuilt_rows = rebuild_slice_rows()
        if any(row["status"] != "closed" for row in rebuilt_rows):
            raise RuntimeError("heavy slice rebuild failed")
        reconstruction_rows.extend(rebuilt_rows)

    cross_rows, cross = cross_channel_rows(formulas)
    if any(row.get("residual", "0") != "0" for row in cross_rows):
        raise RuntimeError("cross-channel identity failed")
    coefficients = coefficient_rows(formulas, cross)
    contracts = contract_rows()
    gates = [
        {"gate": "primary_source_lock", "passed": True, "status": "closed", "meaning": "massive trees, integral shifts, and inherited coefficients are source locked"},
        {"gate": "D_scalar_tree_trace_cancellation", "passed": True, "status": "closed", "meaning": "massless scalar exchange is D independent before loop reduction"},
        {"gate": "generic_D_scalar_shared_boxes", "passed": True, "status": "closed", "meaning": "both scalar s-cut box coefficients derived and held out"},
        {"gate": "mixed_linear_epsilon_box_correction", "passed": True, "status": "closed", "meaning": "crossed-channel unitarity fixes the mandatory O(epsilon) correction"},
        {"gate": "generic_D_full_scalar_triangle", "passed": False, "status": "open", "meaning": "full H(R) contact numerator is not reduced yet"},
        {"gate": "generic_D_internal_graviton_states", "passed": False, "status": "open", "meaning": "mixed/hh state projector remains to be applied"},
        {"gate": "cut_free_dJ2_remainder", "passed": False, "status": "open", "meaning": "cannot be fixed before all D-dimensional cuts"},
        {"gate": "complete_outer_cut_or_full_MTS", "passed": False, "status": "open", "meaning": "not licensed by this sub-checkpoint"},
    ]

    write_csv(COEFFICIENT_CSV, tagged(coefficients + scalar_rows))
    write_csv(SLICE_CSV, tagged(reconstruction_rows))
    write_csv(ANCHOR_CSV, tagged(anchor_rows))
    write_csv(CROSS_CHANNEL_CSV, tagged(cross_rows))
    write_csv(CONTRACT_CSV, tagged(contracts))
    write_csv(GATE_CSV, tagged(gates))
    write_document(formulas, cross)

    formal_hash_after = tree_digest(ROOT / "formalization-workbench")
    if formal_hash_before != formal_hash_after:
        raise RuntimeError("formalization-workbench changed during checkpoint generation")
    source_hashes = {relative(path): digest(path) for path in [*required, Path(__file__).resolve()]}
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_lock": locks,
        "source_hashes_sha256": source_hashes,
        "formalization_workbench_tree_sha256": formal_hash_after,
        "generic_D_scalar_shared_box_sector_complete": True,
        "mixed_linear_epsilon_box_correction_complete": True,
        "mixed_linear_epsilon_box_correction": exact(cross["epsilon_gap"]),
        "old_generic_D_mixed_continuation_rejected_as_physical": True,
        "rank_four_triangle_descendant_complete": True,
        "generic_D_full_scalar_triangle_complete": False,
        "generic_D_internal_graviton_state_sum_complete": False,
        "cut_free_dJ2_remainder_complete": False,
        "complete_one_loop_phi2h2": False,
        "outer_cut_complete": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "reduce the full H(R) scalar contact numerator in generic D, then apply the D-dimensional internal-graviton projector",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# 4996 provenance\n\n"
        f"Checkpoint marker: `{MARKER}`\n\n"
        "## Locked inputs\n\n"
        + "\n".join(f"- `{path}` - SHA-256 `{value}`" for path, value in source_hashes.items())
        + "\n\n## Method\n\n"
        "The scalar box coefficients are reconstructed from exact rational generic-D IBP reductions with independent held-out dimensions and kinematics. The mixed O(epsilon) correction is then fixed by equality of a shared scalar box across the s and u cuts, using the sourced vanishing linear-epsilon hh box coefficient. The triangle descendant is retained only as a diagnostic because H(R)=s^4 is valid on quadruple residues but not on lower topologies.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
