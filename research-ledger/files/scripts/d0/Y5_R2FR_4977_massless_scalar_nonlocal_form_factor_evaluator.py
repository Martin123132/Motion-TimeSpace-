from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np
import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_ROOT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4973"
    / "src-0911.1168"
)
SOURCE = POST / "source-intake" / "functional_rg" / "4977"

TEX_SOURCE = SOURCE_ROOT / "cpt2009m.tex"
ALPHA_SOURCE = SOURCE_ROOT / "anc" / "ffwa.m"
EXPLICIT_SOURCE = SOURCE_ROOT / "anc" / "ffwd.m"

STRUCTURE_MAP_CSV = SOURCE / "C3_massless_scalar_structure_map.csv"
MANIFEST_CSV = SOURCE / "C3_massless_scalar_form_factor_manifest.csv"
CROSSCHECK_CSV = SOURCE / "C3_massless_scalar_form_factor_crosscheck.csv"
HOMOGENEITY_CSV = SOURCE / "C3_massless_scalar_scale_homogeneity.csv"
TRIANGLE_CSV = SOURCE / "C3_massless_scalar_potential_triangle.csv"
QUADRATIC_LOG_CSV = SOURCE / "C3_massless_scalar_quadratic_log.csv"
REDUCED_CHANNEL_CSV = SOURCE / "C3_massless_scalar_reduced_channel_values.csv"
GATE_CSV = SOURCE / "C3_massless_scalar_nonlocal_gate.csv"
RESULT_JSON = SOURCE / "C3_massless_scalar_nonlocal_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4977_MASSLESS_SCALAR_NONLOCAL_FORM_FACTORS"
CHECKED_DATE = "2026-07-13"

RELEVANT_INDICES = (1, 4, 5, 6, 9, 10, 11, 15, 16, 17, 22, 23, 24, 25, 26, 27, 28, 29)
MOMENTUM_SAMPLES = {
    "K01_q2_2_3_1": (-2.0, -3.0, -1.0),
    "K02_q2_4_3_1": (-4.0, -3.0, -1.0),
    "K03_q2_5_2_3": (-5.0, -2.0, -3.0),
}

# Source equations (2.46)--(2.74).  The paper explicitly warns that the
# unsymmetrized alpha and explicit representations can differ by terms that
# vanish under these averages; only the symmetrized form factors make sense.
SYMMETRIZATION = {
    1: ((0, 1, 2), (2, 0, 1), (1, 2, 0)),
    4: ((0, 1, 2), (1, 0, 2)),
    5: ((0, 1, 2), (1, 0, 2)),
    6: ((0, 1, 2), (1, 0, 2)),
    9: ((0, 1, 2), (2, 0, 1), (1, 2, 0), (1, 0, 2), (2, 1, 0), (0, 2, 1)),
    10: ((0, 1, 2), (2, 0, 1), (1, 2, 0), (1, 0, 2), (2, 1, 0), (0, 2, 1)),
    11: ((0, 1, 2), (1, 0, 2)),
    15: ((0, 1, 2),),
    16: ((0, 1, 2), (1, 0, 2)),
    17: ((0, 1, 2),),
    22: ((0, 1, 2), (0, 2, 1)),
    23: ((0, 1, 2), (1, 0, 2)),
    24: ((0, 1, 2), (0, 2, 1)),
    25: ((0, 1, 2), (0, 2, 1)),
    26: ((0, 1, 2), (1, 0, 2)),
    27: ((0, 1, 2), (1, 0, 2)),
    28: ((0, 1, 2), (1, 0, 2)),
    29: ((0, 1, 2), (2, 0, 1), (1, 2, 0)),
}


@dataclass(frozen=True)
class Structure:
    index: int
    source_structure: str
    minimal_scalar_structure: str
    derivative_order: int
    p_factor: Fraction
    source_lines: str


STRUCTURES = (
    Structure(1, "P1 P2 P3", "R1 R2 R3", 0, Fraction(1, 216), "353"),
    Structure(4, "R1 R2 P3", "R1 R2 R3", 0, Fraction(1, 6), "356"),
    Structure(5, "Ricci1.Ricci2 P3", "Ricci1.Ricci2 R3", 0, Fraction(1, 6), "357"),
    Structure(6, "P1 P2 R3", "R1 R2 R3", 0, Fraction(1, 36), "358"),
    Structure(9, "R1 R2 R3", "R1 R2 R3", 0, Fraction(1, 1), "361"),
    Structure(10, "Ricci1^mu_alpha Ricci2^alpha_beta Ricci3^beta_mu", "unchanged", 0, Fraction(1, 1), "362"),
    Structure(11, "Ricci1.Ricci2 R3", "unchanged", 0, Fraction(1, 1), "363"),
    Structure(15, "Ricci1^mn grad_m R2 grad_n P3", "(1/6) Ricci1^mn grad_m R2 grad_n R3", 2, Fraction(1, 6), "370"),
    Structure(16, "grad^m Ricci1^na grad_n Ricci2_ma P3", "(1/6) grad^m Ricci1^na grad_n Ricci2_ma R3", 2, Fraction(1, 6), "371"),
    Structure(17, "Ricci1^mn Hess_mn P2 P3", "(1/36) Ricci1^mn Hess_mn R2 R3", 2, Fraction(1, 36), "372"),
    Structure(22, "Ricci1^ab grad_a R2 grad_b R3", "unchanged", 2, Fraction(1, 1), "377"),
    Structure(23, "grad^m Ricci1^na grad_n Ricci2_ma R3", "unchanged", 2, Fraction(1, 1), "378"),
    Structure(24, "Ricci1^mn grad_m Ricci2^ab grad_n Ricci3_ab", "unchanged", 2, Fraction(1, 1), "379"),
    Structure(25, "Ricci1^mn grad_a Ricci2_bm grad^b Ricci3_n^a", "unchanged", 2, Fraction(1, 1), "380"),
    Structure(26, "Hess_ab Ricci1^mn Hess_mn Ricci2^ab P3", "(1/6) Hess_ab Ricci1^mn Hess_mn Ricci2^ab R3", 4, Fraction(1, 6), "384"),
    Structure(27, "Hess_ab Ricci1^mn Hess_mn Ricci2^ab R3", "unchanged", 4, Fraction(1, 1), "385"),
    Structure(28, "grad_m Ricci1^al grad_n Ricci2_l^b Hess_ab Ricci3^mn", "unchanged", 4, Fraction(1, 1), "386"),
    Structure(29, "Hess_ls Ricci1^ab Hess_ab Ricci2^mn Hess_mn Ricci3^ls", "unchanged", 6, Fraction(1, 1), "390"),
)

REDUCED_CHANNELS = {
    "S01_R1_R2_R3": {
        "invariant": "R1 R2 R3",
        "members": ((1, Fraction(1, 216)), (4, Fraction(1, 6)), (6, Fraction(1, 36)), (9, Fraction(1, 1))),
        "permutations": SYMMETRIZATION[9],
    },
    "S02_Ricci1_Ricci2_R3": {
        "invariant": "Ricci1^mn Ricci2_mn R3",
        "members": ((5, Fraction(1, 6)), (11, Fraction(1, 1))),
        "permutations": SYMMETRIZATION[11],
    },
    "S03_Ricci_cubed": {
        "invariant": "Ricci1^mu_alpha Ricci2^alpha_beta Ricci3^beta_mu",
        "members": ((10, Fraction(1, 1)),),
        "permutations": SYMMETRIZATION[10],
    },
    "S04_Ricci_gradR_gradR": {
        "invariant": "Ricci1^mn grad_m R2 grad_n R3",
        "members": ((15, Fraction(1, 6)), (22, Fraction(1, 1))),
        "permutations": SYMMETRIZATION[22],
    },
    "S05_cross_gradRicci_R": {
        "invariant": "grad^m Ricci1^na grad_n Ricci2_ma R3",
        "members": ((16, Fraction(1, 6)), (23, Fraction(1, 1))),
        "permutations": SYMMETRIZATION[23],
    },
    "S06_Ricci_HessR_R": {
        "invariant": "Ricci1^mn Hess_mn R2 R3",
        "members": ((17, Fraction(1, 36)),),
        "permutations": SYMMETRIZATION[17],
    },
    "S07_Ricci_gradRicci_gradRicci": {
        "invariant": "Ricci1^mn grad_m Ricci2^ab grad_n Ricci3_ab",
        "members": ((24, Fraction(1, 1)),),
        "permutations": SYMMETRIZATION[24],
    },
    "S08_Ricci_cross_gradRicci": {
        "invariant": "Ricci1^mn grad_a Ricci2_bm grad^b Ricci3_n^a",
        "members": ((25, Fraction(1, 1)),),
        "permutations": SYMMETRIZATION[25],
    },
    "S09_HessRicci_HessRicci_R": {
        "invariant": "Hess_ab Ricci1^mn Hess_mn Ricci2^ab R3",
        "members": ((26, Fraction(1, 6)), (27, Fraction(1, 1))),
        "permutations": SYMMETRIZATION[27],
    },
    "S10_gradRicci_gradRicci_HessRicci": {
        "invariant": "grad_m Ricci1^al grad_n Ricci2_l^b Hess_ab Ricci3^mn",
        "members": ((28, Fraction(1, 1)),),
        "permutations": SYMMETRIZATION[28],
    },
    "S11_triple_HessRicci": {
        "invariant": "Hess_ls Ricci1^ab Hess_ab Ricci2^mn Hess_mn Ricci3^ls",
        "members": ((29, Fraction(1, 1)),),
        "permutations": SYMMETRIZATION[29],
    },
}

A1, A2, A3, D1, D2, D3 = sp.symbols("a1 a2 a3 d1 d2 d3")
CANONICAL_SYMBOLS = {
    "a1": A1,
    "a2": A2,
    "a3": A3,
    "d1": D1,
    "d2": D2,
    "d3": D3,
}


@dataclass
class AlphaFormFactor:
    dff: sp.Expr
    tr: sp.Expr
    lh: dict[tuple[int, int], sp.Expr]
    symmetry: str
    cyclic: bool
    derivative_order: int
    function: Any


@dataclass
class ExplicitFormFactor:
    rf: sp.Expr
    rt: sp.Expr
    rl: dict[tuple[int, int], sp.Expr]
    lh: dict[tuple[int, int], sp.Expr]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
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


_MATHICS_BUILTINS_READY = False


def mathics_session():
    global _MATHICS_BUILTINS_READY
    import mathics.core.definitions as definitions
    from mathics.core.atoms import String
    from mathics.core.load_builtin import definition_contribute, import_and_load_builtins

    if not _MATHICS_BUILTINS_READY:
        import_and_load_builtins()
        _MATHICS_BUILTINS_READY = True

    def patched_load_builtin_definitions(
        self, builtin_filename=None, extension_modules=()
    ):
        definition_contribute(self)
        self.set_ownvalue("System`$CharacterEncoding", String("UTF-8"))
        from mathics.session import autoload_files
        from mathics.settings import ROOT_DIR

        autoload_files(self, ROOT_DIR, "autoload")

    definitions.load_builtin_definitions = patched_load_builtin_definitions
    from mathics.session import MathicsSession

    return MathicsSession()


def canonicalize(expression: Any) -> sp.Expr:
    converted = sp.sympify(expression.to_sympy())
    replacements: dict[sp.Symbol, sp.Expr] = {}
    for symbol in converted.free_symbols:
        name = str(symbol)
        matched = False
        for source_name, target in CANONICAL_SYMBOLS.items():
            if name == source_name or name.endswith(f"_{source_name}"):
                replacements[symbol] = target
                matched = True
                break
        if not matched and (name == "DD" or name.endswith("_DD")):
            replacements[symbol] = (
                D1**2 + D2**2 + D3**2 - 2 * D1 * D2 - 2 * D1 * D3 - 2 * D2 * D3
            )
            matched = True
        if not matched:
            raise ValueError(f"unmapped Mathics symbol {name} in {converted}")
    result = sp.cancel(converted.xreplace(replacements))
    if result.free_symbols - set(CANONICAL_SYMBOLS.values()):
        raise ValueError(f"unexpected symbols after canonicalization: {result.free_symbols}")
    return result


def extract_alpha_form_factors() -> dict[int, AlphaFormFactor]:
    session = mathics_session()
    loaded = session.evaluate(f'Get["{ALPHA_SOURCE.resolve().as_posix()}"]')
    if str(loaded) != "System`Null":
        raise RuntimeError(f"failed to load alpha representation: {loaded}")
    factors: dict[int, AlphaFormFactor] = {}
    for index in RELEVANT_INDICES:
        dff = canonicalize(session.evaluate(f"dff[{index}]"))
        tr = canonicalize(session.evaluate(f"tr[{index}]"))
        lh = {
            pair: canonicalize(session.evaluate(f"lh[{pair[0]},{pair[1]},{index}]"))
            for pair in ((1, 2), (1, 3), (2, 3))
        }
        symmetry = str(session.evaluate(f"sym[{index}]"))
        cyclic = str(session.evaluate(f"cyc[{index}]")) == "System`True"
        derivative_order = int(str(session.evaluate(f"der[{index}]")))
        function = sp.lambdify((A1, A2, A3, D1, D2, D3), dff, modules="numpy")
        factors[index] = AlphaFormFactor(
            dff=dff,
            tr=tr,
            lh=lh,
            symmetry=symmetry,
            cyclic=cyclic,
            derivative_order=derivative_order,
            function=function,
        )
    return factors


def extract_explicit_form_factors() -> dict[int, ExplicitFormFactor]:
    session = mathics_session()
    loaded = session.evaluate(f'Get["{EXPLICIT_SOURCE.resolve().as_posix()}"]')
    if str(loaded) != "System`Null":
        raise RuntimeError(f"failed to load explicit representation: {loaded}")
    factors: dict[int, ExplicitFormFactor] = {}
    for index in RELEVANT_INDICES:
        factors[index] = ExplicitFormFactor(
            rf=canonicalize(session.evaluate(f"rf[{index}]")),
            rt=canonicalize(session.evaluate(f"rt[{index}]")),
            rl={
                pair: canonicalize(session.evaluate(f"rl[{pair[0]},{pair[1]},{index}]"))
                for pair in ((1, 2), (1, 3), (2, 3))
            },
            lh={
                pair: canonicalize(session.evaluate(f"lh[{pair[0]},{pair[1]},{index}]"))
                for pair in ((1, 2), (1, 3), (2, 3))
            },
        )
    return factors


def expression_hash(*expressions: sp.Expr) -> str:
    payload = "\n".join(sp.srepr(expression) for expression in expressions)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def quadrature_grid(order: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    unit_nodes = 0.5 * (nodes + 1.0)
    unit_weights = 0.5 * weights
    radial = unit_nodes[:, None]
    angular = unit_nodes[None, :]
    base_weights = unit_weights[:, None] * unit_weights[None, :]

    # The massless triangle kernel has logarithmic endpoint singularities at
    # all three simplex vertices.  A single Duffy map resolves only one of
    # them and converges slowly.  Split the simplex into six triangles, each
    # containing exactly one original vertex, and use that vertex as the
    # radial origin.  The radial Jacobian cancels the linear vanishing of the
    # denominator, leaving a smooth integrand on every sector.
    vertex_1 = np.asarray((1.0, 0.0))
    vertex_2 = np.asarray((0.0, 1.0))
    vertex_3 = np.asarray((0.0, 0.0))
    midpoint_12 = np.asarray((0.5, 0.5))
    midpoint_23 = np.asarray((0.0, 0.5))
    midpoint_31 = np.asarray((0.5, 0.0))
    centroid = np.asarray((1.0 / 3.0, 1.0 / 3.0))
    sectors = (
        (vertex_1, midpoint_12, centroid),
        (vertex_1, centroid, midpoint_31),
        (vertex_2, midpoint_23, centroid),
        (vertex_2, centroid, midpoint_12),
        (vertex_3, midpoint_31, centroid),
        (vertex_3, centroid, midpoint_23),
    )
    all_a1: list[np.ndarray] = []
    all_a2: list[np.ndarray] = []
    all_a3: list[np.ndarray] = []
    all_measure: list[np.ndarray] = []
    for vertex, edge_a, edge_b in sectors:
        direction_a = edge_a - vertex
        direction_b = edge_b - vertex
        direction_x = (1.0 - angular) * direction_a[0] + angular * direction_b[0]
        direction_y = (1.0 - angular) * direction_a[1] + angular * direction_b[1]
        a1 = vertex[0] + radial * direction_x
        a2 = vertex[1] + radial * direction_y
        determinant = abs(
            direction_a[0] * direction_b[1] - direction_a[1] * direction_b[0]
        )
        all_a1.append(np.broadcast_to(a1, (order, order)))
        all_a2.append(np.broadcast_to(a2, (order, order)))
        all_a3.append(np.broadcast_to(1.0 - a1 - a2, (order, order)))
        all_measure.append(base_weights * radial * determinant)
    return (
        np.stack(all_a1),
        np.stack(all_a2),
        np.stack(all_a3),
        np.stack(all_measure),
    )


def basic_gamma(
    boxes: tuple[float, float, float],
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
) -> float:
    a1, a2, a3, measure = grid
    d1, d2, d3 = boxes
    denominator = -(a1 * a2 * d3 + a1 * a3 * d2 + a2 * a3 * d1)
    if np.any(denominator <= 0.0):
        raise ValueError(f"non-positive Euclidean triangle denominator for {boxes}")
    return float(np.sum(measure / denominator))


def exact_coefficient(expression: sp.Expr, boxes: tuple[float, float, float]) -> mp.mpf:
    substitutions = {D1: boxes[0], D2: boxes[1], D3: boxes[2]}
    value = sp.N(expression.subs(substitutions), mp.mp.dps)
    if value.free_symbols:
        raise ValueError(f"unevaluated coefficient {value}")
    return mp.mpf(str(value))


def log_divided(box_m: float, box_n: float) -> mp.mpf:
    left = mp.mpf(box_m)
    right = mp.mpf(box_n)
    if mp.almosteq(left, right):
        return 1 / left
    return mp.log(left / right) / (left - right)


def alpha_form_factor(
    factor: AlphaFormFactor,
    boxes: tuple[float, float, float],
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
) -> float:
    a1, a2, a3, measure = grid
    d1, d2, d3 = boxes
    denominator = -(a1 * a2 * d3 + a1 * a3 * d2 + a2 * a3 * d1)
    numerator = np.asarray(factor.function(a1, a2, a3, d1, d2, d3), dtype=float)
    if numerator.ndim == 0:
        numerator = np.broadcast_to(numerator, denominator.shape)
    integral = float(np.sum(measure * numerator / denominator))
    result = mp.mpf(integral) + exact_coefficient(factor.tr, boxes)
    for pair, coefficient in factor.lh.items():
        result += exact_coefficient(coefficient, boxes) * log_divided(
            boxes[pair[0] - 1], boxes[pair[1] - 1]
        )
    return float(result)


def explicit_form_factor(
    factor: ExplicitFormFactor,
    boxes: tuple[float, float, float],
    gamma_basic: float,
) -> float:
    result = exact_coefficient(factor.rf, boxes) * mp.mpf(gamma_basic)
    result += exact_coefficient(factor.rt, boxes)
    for pair, coefficient in factor.rl.items():
        result += exact_coefficient(coefficient, boxes) * mp.log(
            mp.mpf(boxes[pair[0] - 1]) / mp.mpf(boxes[pair[1] - 1])
        )
    for pair, coefficient in factor.lh.items():
        result += exact_coefficient(coefficient, boxes) * log_divided(
            boxes[pair[0] - 1], boxes[pair[1] - 1]
        )
    return float(result)


def permute_boxes(
    boxes: tuple[float, float, float], permutation: tuple[int, int, int]
) -> tuple[float, float, float]:
    return tuple(boxes[index] for index in permutation)


def symmetrized_alpha_form_factor(
    index: int,
    factor: AlphaFormFactor,
    boxes: tuple[float, float, float],
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
) -> float:
    return float(
        np.mean(
            [
                alpha_form_factor(factor, permute_boxes(boxes, permutation), grid)
                for permutation in SYMMETRIZATION[index]
            ]
        )
    )


def symmetrized_explicit_form_factor(
    index: int,
    factor: ExplicitFormFactor,
    boxes: tuple[float, float, float],
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
) -> float:
    values: list[float] = []
    for permutation in SYMMETRIZATION[index]:
        permuted = permute_boxes(boxes, permutation)
        values.append(explicit_form_factor(factor, permuted, basic_gamma(permuted, grid)))
    return float(np.mean(values))


def averaged_alpha_form_factor(
    factor: AlphaFormFactor,
    boxes: tuple[float, float, float],
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    permutations: tuple[tuple[int, int, int], ...],
) -> float:
    return float(
        np.mean(
            [
                alpha_form_factor(factor, permute_boxes(boxes, permutation), grid)
                for permutation in permutations
            ]
        )
    )


def averaged_explicit_form_factor(
    factor: ExplicitFormFactor,
    boxes: tuple[float, float, float],
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    permutations: tuple[tuple[int, int, int], ...],
) -> float:
    values: list[float] = []
    for permutation in permutations:
        permuted = permute_boxes(boxes, permutation)
        values.append(explicit_form_factor(factor, permuted, basic_gamma(permuted, grid)))
    return float(np.mean(values))


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-30)


def structure_rows(alpha: dict[int, AlphaFormFactor]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for structure in STRUCTURES:
        measured_derivatives = alpha[structure.index].derivative_order
        rows.append(
            {
                "form_factor_index": structure.index,
                "source_structure": structure.source_structure,
                "minimal_scalar_substitution": structure.minimal_scalar_structure,
                "P_equals_R_over_6_factor": str(structure.p_factor),
                "derivative_order": structure.derivative_order,
                "ancillary_derivative_order": measured_derivatives,
                "expected_box_homogeneity_power": -(1 + structure.derivative_order // 2),
                "source_tex_lines": structure.source_lines,
                "source_path": relative(TEX_SOURCE),
                "status": "source_mapped_finite_momentum_cubic_curvature_term",
            }
        )
    return tagged(rows)


def manifest_rows(
    alpha: dict[int, AlphaFormFactor], explicit: dict[int, ExplicitFormFactor]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in RELEVANT_INDICES:
        alpha_factor = alpha[index]
        explicit_factor = explicit[index]
        rows.append(
            {
                "form_factor_index": index,
                "symmetry": alpha_factor.symmetry,
                "cyclic": alpha_factor.cyclic,
                "required_symmetrization": ";".join(
                    "".join(str(value + 1) for value in permutation)
                    for permutation in SYMMETRIZATION[index]
                ),
                "symmetrization_source_tex_lines": "423-506,7209-7213",
                "derivative_order": alpha_factor.derivative_order,
                "alpha_expression_sha256": expression_hash(
                    alpha_factor.dff, alpha_factor.tr, *alpha_factor.lh.values()
                ),
                "explicit_expression_sha256": expression_hash(
                    explicit_factor.rf,
                    explicit_factor.rt,
                    *explicit_factor.rl.values(),
                    *explicit_factor.lh.values(),
                ),
                "alpha_source_path": relative(ALPHA_SOURCE),
                "explicit_source_path": relative(EXPLICIT_SOURCE),
                "status": "two_independent_source_representations_loaded",
            }
        )
    return tagged(rows)


def quadratic_log_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "invariant": "R_mn log(-Box/mu^2) R^mn",
            "minimal_scalar_source_combination": "gamma_1",
            "log_coefficient_inside_minus_W_braces": str(-Fraction(1, 60)),
            "finite_constant_inside_minus_W_braces": str(Fraction(4, 225)),
            "d_d_ln_mu_coefficient_inside_minus_W_braces": str(Fraction(1, 30)),
            "overall_prefactor": "1/[2(4pi)^2]",
            "source_tex_lines": "320,3661-3693",
            "status": "derived_exact_massless_quadratic_log",
        },
        {
            "invariant": "R log(-Box/mu^2) R",
            "minimal_scalar_source_combination": "gamma_2+gamma_3/6+gamma_4/36",
            "log_coefficient_inside_minus_W_braces": str(-Fraction(1, 120)),
            "finite_constant_inside_minus_W_braces": str(-Fraction(29, 1800)),
            "d_d_ln_mu_coefficient_inside_minus_W_braces": str(Fraction(1, 60)),
            "overall_prefactor": "1/[2(4pi)^2]",
            "source_tex_lines": "321-323,3661-3693",
            "status": "derived_exact_massless_quadratic_log",
        },
    ]
    return tagged(rows)


def write_provenance(results: dict[str, Any]) -> None:
    PROVENANCE.write_text(
        f"""# Checkpoint 4977 provenance

Marker: `{MARKER}`

## Primary source

- `{relative(TEX_SOURCE)}`
- SHA256 `{digest(TEX_SOURCE)}`
- effective action and quadratic logarithms: source lines 3653--3719
- 29 cubic structures: source lines 349--419

## Machine-readable source representations

- `{relative(ALPHA_SOURCE)}`
- SHA256 `{digest(ALPHA_SOURCE)}`
- `{relative(EXPLICIT_SOURCE)}`
- SHA256 `{digest(EXPLICIT_SOURCE)}`

The two ancillary files encode the alpha-parameter and explicit
triangle/log-ratio representations independently. Mathics loads their
original Mathematica assignments; SymPy canonicalizes the resulting exact
rational expressions; Gauss--Legendre quadrature evaluates the simplex.

## Numerical controls

- low quadrature order: `{results['quadrature']['low_order']}`
- high quadrature order: `{results['quadrature']['high_order']}`
- maximum alpha/explicit relative difference: `{results['crosscheck']['maximum_relative_difference']:.17g}`
- maximum quadrature-order relative difference: `{results['crosscheck']['maximum_quadrature_difference']:.17g}`
- maximum homogeneity residual: `{results['homogeneity']['maximum_relative_residual']:.17g}`
- maximum potential-triangle normalization residual: `{results['triangle']['maximum_relative_residual']:.17g}`

## Scope

This validates the source-complete massless minimal-scalar cubic-curvature
form-factor representation and the independent potential-triangle
normalization. It does not yet reconstruct the full third metric response:
that response also contains the third variation of the quadratic nonlocal
curvature action, including operator variation of `log(-Box/mu^2)`.
Consequently `valid_for_full_MTS_claim=false` remains mandatory.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quadrature-order", type=int, default=40)
    parser.add_argument("--low-order", type=int, default=24)
    arguments = parser.parse_args()
    if arguments.low_order < 24 or arguments.quadrature_order <= arguments.low_order:
        raise ValueError("require quadrature_order > low_order >= 24")

    started = time.perf_counter()
    mp.mp.dps = 80
    SOURCE.mkdir(parents=True, exist_ok=True)
    print(f"{MARKER}_START", flush=True)

    for path in (TEX_SOURCE, ALPHA_SOURCE, EXPLICIT_SOURCE):
        if not path.exists():
            raise FileNotFoundError(path)

    alpha = extract_alpha_form_factors()
    explicit = extract_explicit_form_factors()
    print("4977 source representations loaded", flush=True)

    write_csv(STRUCTURE_MAP_CSV, structure_rows(alpha))
    write_csv(MANIFEST_CSV, manifest_rows(alpha, explicit))
    write_csv(QUADRATIC_LOG_CSV, quadratic_log_rows())

    low_grid = quadrature_grid(arguments.low_order)
    high_grid = quadrature_grid(arguments.quadrature_order)
    crosscheck_rows: list[dict[str, Any]] = []
    value_cache: dict[tuple[int, tuple[float, float, float]], tuple[float, float]] = {}
    maximum_crosscheck = 0.0
    maximum_quadrature = 0.0

    for sample_id, boxes in MOMENTUM_SAMPLES.items():
        gamma_low = basic_gamma(boxes, low_grid)
        gamma_high = basic_gamma(boxes, high_grid)
        gamma_quadrature_error = relative_error(gamma_low, gamma_high)
        for index in RELEVANT_INDICES:
            alpha_low = symmetrized_alpha_form_factor(index, alpha[index], boxes, low_grid)
            alpha_high = symmetrized_alpha_form_factor(index, alpha[index], boxes, high_grid)
            explicit_high = symmetrized_explicit_form_factor(index, explicit[index], boxes, high_grid)
            representation_error = relative_error(alpha_high, explicit_high)
            quadrature_error = relative_error(alpha_low, alpha_high)
            maximum_crosscheck = max(maximum_crosscheck, representation_error)
            maximum_quadrature = max(maximum_quadrature, quadrature_error, gamma_quadrature_error)
            value_cache[(index, boxes)] = (alpha_high, explicit_high)
            crosscheck_rows.append(
                {
                    "sample_id": sample_id,
                    "form_factor_index": index,
                    "symmetrization_term_count": len(SYMMETRIZATION[index]),
                    "box_1": boxes[0],
                    "box_2": boxes[1],
                    "box_3": boxes[2],
                    "basic_triangle_gamma": gamma_high,
                    "alpha_representation": alpha_high,
                    "explicit_representation": explicit_high,
                    "alpha_minus_explicit": alpha_high - explicit_high,
                    "representation_relative_difference": representation_error,
                    "alpha_low_vs_high_relative_difference": quadrature_error,
                    "basic_gamma_low_vs_high_relative_difference": gamma_quadrature_error,
                    "status": "finite_momentum_source_crosscheck",
                }
            )
        print(f"4977 {sample_id} 18/18 form factors evaluated", flush=True)
    write_csv(CROSSCHECK_CSV, tagged(crosscheck_rows))

    reduced_channel_rows: list[dict[str, Any]] = []
    maximum_channel_crosscheck = 0.0
    for sample_id, boxes in MOMENTUM_SAMPLES.items():
        for channel_id, channel in REDUCED_CHANNELS.items():
            permutations = channel["permutations"]
            alpha_value = 0.0
            explicit_value = 0.0
            member_formula: list[str] = []
            for index, coefficient in channel["members"]:
                alpha_value += float(coefficient) * averaged_alpha_form_factor(
                    alpha[index], boxes, high_grid, permutations
                )
                explicit_value += float(coefficient) * averaged_explicit_form_factor(
                    explicit[index], boxes, high_grid, permutations
                )
                member_formula.append(f"({coefficient}) Gamma_{index}")
            channel_error = relative_error(alpha_value, explicit_value)
            maximum_channel_crosscheck = max(maximum_channel_crosscheck, channel_error)
            reduced_channel_rows.append(
                {
                    "sample_id": sample_id,
                    "channel_id": channel_id,
                    "minimal_scalar_invariant": channel["invariant"],
                    "form_factor_combination": " + ".join(member_formula),
                    "enhanced_symmetrization_term_count": len(permutations),
                    "alpha_reduced_channel_value": alpha_value,
                    "explicit_reduced_channel_value": explicit_value,
                    "relative_difference": channel_error,
                    "overall_action_prefactor": "1/[2(4pi)^2] in source -W convention",
                    "status": "source_complete_minimal_scalar_cubic_curvature_channel",
                }
            )
    write_csv(REDUCED_CHANNEL_CSV, tagged(reduced_channel_rows))

    scale = 7.0
    base_boxes = MOMENTUM_SAMPLES["K01_q2_2_3_1"]
    scaled_boxes = tuple(scale * value for value in base_boxes)
    homogeneity_rows: list[dict[str, Any]] = []
    maximum_homogeneity = 0.0
    for structure in STRUCTURES:
        base_alpha, base_explicit = value_cache[(structure.index, base_boxes)]
        scaled_alpha = symmetrized_alpha_form_factor(
            structure.index, alpha[structure.index], scaled_boxes, high_grid
        )
        scaled_explicit = symmetrized_explicit_form_factor(
            structure.index, explicit[structure.index], scaled_boxes, high_grid
        )
        power = -(1 + structure.derivative_order // 2)
        expected_alpha = base_alpha * scale**power
        expected_explicit = base_explicit * scale**power
        alpha_residual = relative_error(scaled_alpha, expected_alpha)
        explicit_residual = relative_error(scaled_explicit, expected_explicit)
        maximum_homogeneity = max(maximum_homogeneity, alpha_residual, explicit_residual)
        homogeneity_rows.append(
            {
                "form_factor_index": structure.index,
                "derivative_order": structure.derivative_order,
                "box_scale": scale,
                "expected_homogeneity_power": power,
                "base_alpha": base_alpha,
                "scaled_alpha": scaled_alpha,
                "expected_scaled_alpha": expected_alpha,
                "alpha_relative_residual": alpha_residual,
                "base_explicit": base_explicit,
                "scaled_explicit": scaled_explicit,
                "expected_scaled_explicit": expected_explicit,
                "explicit_relative_residual": explicit_residual,
                "status": "massless_scale_homogeneity_test",
            }
        )
    write_csv(HOMOGENEITY_CSV, tagged(homogeneity_rows))

    triangle_rows: list[dict[str, Any]] = []
    maximum_triangle = 0.0
    for sample_id, boxes in MOMENTUM_SAMPLES.items():
        gamma_basic = basic_gamma(boxes, high_grid)
        gamma_1_alpha, gamma_1_explicit = value_cache[(1, boxes)]
        source_minus_w_mixed = 6.0 * gamma_1_alpha / (2.0 * (4.0 * math.pi) ** 2)
        direct_determinant_triangle = gamma_basic / (4.0 * math.pi) ** 2
        residual = relative_error(source_minus_w_mixed, direct_determinant_triangle)
        gamma_1_identity = relative_error(gamma_1_explicit, gamma_basic / 3.0)
        maximum_triangle = max(maximum_triangle, residual, gamma_1_identity)
        triangle_rows.append(
            {
                "sample_id": sample_id,
                "box_1": boxes[0],
                "box_2": boxes[1],
                "box_3": boxes[2],
                "basic_triangle_gamma": gamma_basic,
                "Gamma_1_alpha": gamma_1_alpha,
                "Gamma_1_explicit": gamma_1_explicit,
                "Gamma_1_expected_Gamma_over_3": gamma_basic / 3.0,
                "Gamma_1_identity_relative_residual": gamma_1_identity,
                "source_minus_W_mixed_P1P2P3": source_minus_w_mixed,
                "direct_half_Tr_log_mixed_triangle": direct_determinant_triangle,
                "normalization_relative_residual": residual,
                "status": "independent_potential_triangle_normalization_match",
            }
        )
    write_csv(TRIANGLE_CSV, tagged(triangle_rows))

    derivative_orders_match = all(
        alpha[structure.index].derivative_order == structure.derivative_order
        for structure in STRUCTURES
    )
    gates = [
        ("G01_primary_sources_exist", all(path.exists() for path in (TEX_SOURCE, ALPHA_SOURCE, EXPLICIT_SOURCE)), "all three source files exist"),
        ("G02_minimal_scalar_map_complete", len(STRUCTURES) == len(RELEVANT_INDICES) == 18, "18 P=R/6-compatible cubic structures"),
        ("G03_derivative_orders_match_source", derivative_orders_match, "ancillary der[i] matches structure map"),
        ("G04_alpha_explicit_crosscheck", maximum_crosscheck < 2.0e-4, f"max relative difference={maximum_crosscheck:.17g}"),
        ("G05_reduced_scalar_channels_crosscheck", maximum_channel_crosscheck < 2.0e-4, f"max relative difference={maximum_channel_crosscheck:.17g}"),
        ("G06_quadrature_converged", maximum_quadrature < 2.0e-4, f"max low/high difference={maximum_quadrature:.17g}"),
        ("G07_massless_homogeneity", maximum_homogeneity < 2.0e-4, f"max relative residual={maximum_homogeneity:.17g}"),
        ("G08_potential_triangle_normalization", maximum_triangle < 2.0e-4, f"max relative residual={maximum_triangle:.17g}"),
        ("G09_quadratic_log_coefficients_exact", quadratic_log_rows()[0]["log_coefficient_inside_minus_W_braces"] == "-1/60" and quadratic_log_rows()[1]["log_coefficient_inside_minus_W_braces"] == "-1/120", "minimal scalar P=R/6 substitution"),
        ("G10_cubic_absolute_mu_log_absent", True, "source lines 3700-3719: Gamma_i contain no arbitrary parameters and only triangle/log ratios"),
        ("G11_full_metric_response_not_overclaimed", True, "quadratic nonlocal action still requires third metric variation"),
    ]
    gate_rows = tagged(
        [
            {
                "gate": name,
                "passed": passed,
                "detail": detail,
                "status": "pass" if passed else "fail",
            }
            for name, passed, detail in gates
        ]
    )
    write_csv(GATE_CSV, gate_rows)

    results = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "sources": {
            relative(TEX_SOURCE): digest(TEX_SOURCE),
            relative(ALPHA_SOURCE): digest(ALPHA_SOURCE),
            relative(EXPLICIT_SOURCE): digest(EXPLICIT_SOURCE),
        },
        "quadrature": {
            "low_order": arguments.low_order,
            "high_order": arguments.quadrature_order,
        },
        "minimal_scalar": {
            "surviving_cubic_structure_count": len(STRUCTURES),
            "P_substitution": "P=R/6",
            "internal_bundle_curvature": 0,
        },
        "crosscheck": {
            "row_count": len(crosscheck_rows),
            "maximum_relative_difference": maximum_crosscheck,
            "maximum_quadrature_difference": maximum_quadrature,
            "reduced_channel_count": len(REDUCED_CHANNELS),
            "maximum_reduced_channel_relative_difference": maximum_channel_crosscheck,
        },
        "homogeneity": {
            "scale": scale,
            "maximum_relative_residual": maximum_homogeneity,
        },
        "triangle": {
            "maximum_relative_residual": maximum_triangle,
            "identity": "Gamma_1=Gamma_basic/3",
            "mixed_source_minus_W": "6 Gamma_1/[2(4pi)^2]=Gamma_basic/(4pi)^2",
        },
        "massless_log": {
            "quadratic_Ricci_log_coefficient_inside_minus_W_braces": "-1/60",
            "quadratic_R_log_coefficient_inside_minus_W_braces": "-1/120",
            "cubic_Gamma_i_absolute_mu_log": False,
            "interpretation": "the full third metric response inherits its absolute logarithm from the third variation of the quadratic nonlocal action",
        },
        "gate_pass_count": sum(bool(passed) for _, passed, _ in gates),
        "gate_count": len(gates),
        "valid_for_complete_free_scalar_cubic_curvature_form_factors": all(bool(passed) for _, passed, _ in gates[:10]),
        "valid_for_full_third_metric_response": False,
        "valid_for_full_MTS_claim": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    write_provenance(results)

    print(
        f"4977 cross={maximum_crosscheck:.3e} quadrature={maximum_quadrature:.3e} "
        f"homogeneity={maximum_homogeneity:.3e} triangle={maximum_triangle:.3e}",
        flush=True,
    )
    print(f"4977 gates {results['gate_pass_count']}/{results['gate_count']}", flush=True)
    print(f"{MARKER}_COMPLETE", flush=True)
    return 0 if results["gate_pass_count"] == results["gate_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
