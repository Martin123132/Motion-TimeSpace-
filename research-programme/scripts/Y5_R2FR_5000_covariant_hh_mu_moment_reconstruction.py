from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from itertools import product
from pathlib import Path

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
RESULT_4999 = FUNCTIONAL / "4999" / "hh_one_scale_IR_laurent_completion_results.json"
GLUON_SYMMETRIC_BASIS = (
    FUNCTIONAL
    / "4992"
    / "sources"
    / "boels_luo_1710.10208"
    / "Results"
    / "GluonsSymms.txt"
)
SOURCE = FUNCTIONAL / "5000"
CACHE_JSON = SOURCE / "symbolic_cut_sample_cache.json"
COEFFICIENT_CSV = SOURCE / "generic_D_hh_cut_polynomial_coefficients.csv"
SAMPLE_CSV = SOURCE / "generic_D_hh_cut_reconstruction_samples.csv"
RESULT_JSON = SOURCE / "covariant_hh_mu_moment_reconstruction_results.json"
CROSSED_CACHE_JSON = SOURCE / "crossed_symbolic_cut_sample_cache.json"
CROSSED_COEFFICIENT_CSV = SOURCE / "crossed_generic_D_hh_cut_polynomial_coefficients.csv"
CROSSED_SAMPLE_CSV = SOURCE / "crossed_generic_D_hh_cut_reconstruction_samples.csv"
CROSSED_RESULT_JSON = SOURCE / "crossed_covariant_hh_mu_moment_reconstruction_results.json"

MARKER = "MTS_5000_COVARIANT_HH_MU_MOMENT_RECONSTRUCTION"
D = sp.Symbol("D")
DIMENSION_DENOMINATOR = D - 2
DIMENSION_NUMERATOR_DEGREE = 3


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def exact(value: sp.Expr | int) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.sympify(value)))))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def dot(metric: sp.Matrix, left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.factor((left.T * metric * right)[0])


def mathematica_list_elements(text: str) -> list[str]:
    stripped = text.strip()
    if not stripped.startswith("{") or not stripped.endswith("}"):
        raise RuntimeError("sourced gluon basis is not a Mathematica list")
    body = stripped[1:-1]
    elements: list[str] = []
    start = 0
    round_depth = 0
    square_depth = 0
    curly_depth = 0
    for index, character in enumerate(body):
        if character == "(":
            round_depth += 1
        elif character == ")":
            round_depth -= 1
        elif character == "[":
            square_depth += 1
        elif character == "]":
            square_depth -= 1
        elif character == "{":
            curly_depth += 1
        elif character == "}":
            curly_depth -= 1
        elif character == "," and round_depth == square_depth == curly_depth == 0:
            elements.append(body[start:index].strip())
            start = index + 1
    elements.append(body[start:].strip())
    return elements


def compile_sourced_yang_mills_seed() -> tuple[object, tuple[tuple[str, str, str], ...]]:
    elements = mathematica_list_elements(GLUON_SYMMETRIC_BASIS.read_text(encoding="utf-8"))
    if len(elements) != 7:
        raise RuntimeError("unexpected sourced symmetric-gluon basis length")
    dot_pattern = re.compile(r"ss\[\s*(p[123]|\\\[Xi\][1-4]R)\s*,\s*(p[123]|\\\[Xi\][1-4]R)\s*\]")
    dot_arguments: list[tuple[str, str, str]] = []

    def replace_dot(match: re.Match[str]) -> str:
        def normalize(token: str) -> str:
            return token if token.startswith("p") else "e" + re.search(r"[1-4]", token).group()

        left = normalize(match.group(1))
        right = normalize(match.group(2))
        name = f"d_{left}_{right}"
        dot_arguments.append((name, left, right))
        return name

    expression = dot_pattern.sub(replace_dot, elements[1]).replace("^", "**")
    expression = re.sub(r"\bs1\b", "S1", expression)
    expression = re.sub(r"\bs2\b", "S2", expression)
    if "ss[" in expression or re.search(r"[^A-Za-z0-9_+\-*/().\s]", expression):
        raise RuntimeError("unparsed token in sourced Yang-Mills seed")
    return compile(expression, str(GLUON_SYMMETRIC_BASIS), "eval"), tuple(sorted(set(dot_arguments)))


YANG_MILLS_SEED_CODE, YANG_MILLS_SEED_DOTS = compile_sourced_yang_mills_seed()


def scaled_yang_mills_tree(
    metric: sp.Matrix,
    momenta: list[sp.Matrix],
    polarizations: list[sp.Matrix],
) -> sp.Expr:
    p1, p2, p3, p4 = momenta
    e1, e2, e3, e4 = polarizations
    invariant_s = dot(metric, p1 + p2, p1 + p2)
    invariant_t = dot(metric, p2 + p3, p2 + p3)
    vectors = {
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4,
        "e1": e1,
        "e2": e2,
        "e3": e3,
        "e4": e4,
    }
    environment: dict[str, sp.Expr] = {"S1": invariant_s, "S2": invariant_t}
    for name, left, right in YANG_MILLS_SEED_DOTS:
        environment[name] = dot(metric, vectors[left], vectors[right])
    sourced_seed = eval(YANG_MILLS_SEED_CODE, {"__builtins__": {}}, environment)
    return sp.factor(sourced_seed / invariant_s)


def scalar_compton_B2(
    metric: sp.Matrix,
    p1: sp.Matrix,
    p2: sp.Matrix,
    p3: sp.Matrix,
    e1: sp.Matrix,
    e2: sp.Matrix,
) -> sp.Expr:
    invariant_s = dot(metric, p1 + p2, p1 + p2)
    invariant_t = dot(metric, p2 + p3, p2 + p3)
    return sp.factor(
        -2 * invariant_t * dot(metric, p3, e1) * dot(metric, p1, e2)
        + 2 * (invariant_s + invariant_t) * dot(metric, p2, e1) * dot(metric, p3, e2)
        + 2 * invariant_s * dot(metric, p3, e1) * dot(metric, p3, e2)
        - (invariant_s * invariant_t + invariant_t**2) * dot(metric, e1, e2)
    )


def bilinear_matrix(dimension: int, function: object) -> sp.Matrix:
    basis = sp.eye(dimension)
    return sp.Matrix(dimension, dimension, lambda row, column: function(basis.col(row), basis.col(column)))


def frobenius(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.trace(left.T * right)


def vector_projector(metric: sp.Matrix, momentum: sp.Matrix, reference: sp.Matrix) -> sp.Matrix:
    return sp.simplify(
        -metric
        + (momentum * reference.T + reference * momentum.T) / dot(metric, momentum, reference)
    )


def external_kinematics(
    dimension: int,
    cosine: sp.Rational,
    sine: sp.Rational,
) -> tuple[sp.Matrix, list[sp.Matrix], sp.Matrix]:
    metric = sp.diag(1, *([-1] * (dimension - 1)))

    def embed(values: list[sp.Expr | int]) -> sp.Matrix:
        return sp.Matrix([*values, *([0] * (dimension - len(values)))])

    p1 = embed([1, 0, 0, 1])
    p2 = embed([1, 0, 0, -1])
    p3 = embed([-1, -sine, 0, -cosine])
    p4 = -(p1 + p2 + p3)
    helicity = embed([0, 1, sp.I, 0])
    return metric, [p1, p2, p3, p4], helicity


def tree_current_matrices(
    dimension: int,
    cosine: sp.Rational,
    sine: sp.Rational,
    spatial_direction: tuple[sp.Expr, ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    metric, momenta, helicity = external_kinematics(dimension, cosine, sine)
    p1, p2, p3, p4 = momenta
    if len(spatial_direction) > dimension - 1:
        raise ValueError("too many spatial components")
    direction = [*spatial_direction, *([0] * (dimension - 1 - len(spatial_direction)))]
    loop_left = sp.Matrix([1, *direction])
    loop_right = p1 + p2 - loop_left
    if sp.factor(dot(metric, loop_left, loop_left)) != 0 or sp.factor(dot(metric, loop_right, loop_right)) != 0:
        raise ValueError("cut direction is not null")

    left_first = bilinear_matrix(
        dimension,
        lambda internal_left, internal_right: scaled_yang_mills_tree(
            metric,
            [p1, p2, -loop_left, -loop_right],
            [helicity, helicity, internal_left, internal_right],
        ),
    )
    left_second = bilinear_matrix(
        dimension,
        lambda internal_right, internal_left: scaled_yang_mills_tree(
            metric,
            [p1, p2, -loop_right, -loop_left],
            [helicity, helicity, internal_right, internal_left],
        ),
    )
    right_first = bilinear_matrix(
        dimension,
        lambda internal_left, internal_right: scalar_compton_B2(
            metric,
            loop_left,
            loop_right,
            p3,
            internal_left,
            internal_right,
        ),
    )
    right_second = bilinear_matrix(
        dimension,
        lambda internal_left, internal_right: scalar_compton_B2(
            metric,
            loop_left,
            loop_right,
            p4,
            internal_left,
            internal_right,
        ),
    )
    return metric, loop_left, loop_right, left_first, left_second, right_first, right_second


def compact_projected_cut(
    left_first: sp.Matrix,
    left_second: sp.Matrix,
    right_first: sp.Matrix,
    right_second: sp.Matrix,
    projector_left: sp.Matrix,
    projector_right: sp.Matrix,
    transverse_dimension: sp.Expr,
) -> sp.Expr:
    projected_first = projector_left * right_first
    projected_second = projector_left * right_second
    trace_current = right_first.T * projector_left * right_second
    left_weight = left_first * projector_right
    right_weight = projector_right * left_second
    joined_weight = left_first * projector_right * left_second
    projected_gram = (
        projected_first * projector_right * projected_second.T
        + projected_second * projector_right * projected_first.T
    ) / 2
    trace_kernel = left_weight.T * projector_left * right_weight.T
    return sp.factor(
        (
            sp.trace(left_weight * projected_first.T)
            * sp.trace(projected_second * right_weight)
            + sp.trace(left_weight * projected_second.T)
            * sp.trace(projected_first * right_weight)
            + frobenius(
                left_weight * projected_first.T,
                projected_second * right_weight,
            )
            + frobenius(
                left_weight * projected_second.T,
                projected_first * right_weight,
            )
        )
        / 4
        - (
            frobenius(trace_current, trace_kernel)
            + frobenius(trace_current.T, trace_kernel)
        )
        / (2 * transverse_dimension)
        - frobenius(joined_weight, projected_gram) / transverse_dimension
        + sp.trace(projector_right * trace_current)
        * frobenius(joined_weight, projector_left)
        / transverse_dimension**2
    )


def covariant_hh_cut_numerator(
    dimension: int,
    cosine: sp.Rational,
    sine: sp.Rational,
    spatial_direction: tuple[sp.Expr, ...],
    reference_projector: bool = True,
) -> sp.Expr:
    (
        metric,
        loop_left,
        loop_right,
        left_first,
        left_second,
        right_first,
        right_second,
    ) = tree_current_matrices(dimension, cosine, sine, spatial_direction)

    if reference_projector:
        projector_left = vector_projector(metric, loop_left, loop_right)
        projector_right = vector_projector(metric, loop_right, loop_left)
    else:
        projector_left = -metric
        projector_right = -metric
    transverse_dimension = sp.Integer(dimension - 2)
    return compact_projected_cut(
        left_first,
        left_second,
        right_first,
        right_second,
        projector_left,
        projector_right,
        transverse_dimension,
    )


def spectator_compressed_hh_cut_numerator(
    dimension: sp.Expr,
    cosine: sp.Rational,
    sine: sp.Rational,
    spatial_direction: tuple[sp.Expr, ...],
) -> sp.Expr:
    if len(spatial_direction) != 4:
        raise ValueError("spectator compression requires the five-dimensional active cut chart")
    (
        active_metric,
        active_loop_left,
        active_loop_right,
        left_active,
        second_active,
        right_first_active,
        right_second_active,
    ) = tree_current_matrices(5, cosine, sine, spatial_direction)
    metric, momenta, helicity = external_kinematics(6, cosine, sine)
    p1, p2, p3, _ = momenta
    loop_left = sp.Matrix([1, *spatial_direction, 0])
    loop_right = p1 + p2 - loop_left
    spectator = sp.eye(6).col(5)
    left_spectator = scaled_yang_mills_tree(
        metric,
        [p1, p2, -loop_left, -loop_right],
        [helicity, helicity, spectator, spectator],
    )
    second_spectator = scaled_yang_mills_tree(
        metric,
        [p1, p2, -loop_right, -loop_left],
        [helicity, helicity, spectator, spectator],
    )
    right_first_spectator = scalar_compton_B2(
        metric,
        loop_left,
        loop_right,
        p3,
        spectator,
        spectator,
    )
    right_second_spectator = scalar_compton_B2(
        metric,
        loop_left,
        loop_right,
        momenta[3],
        spectator,
        spectator,
    )

    active_size = 5
    projector_left = vector_projector(active_metric, active_loop_left, active_loop_right)
    projector_right = vector_projector(active_metric, active_loop_right, active_loop_left)
    spectator_count = sp.sympify(dimension) - active_size
    transverse_dimension = sp.sympify(dimension) - 2

    projected_first = projector_left * right_first_active
    projected_second = projector_left * right_second_active
    trace_active = right_first_active.T * projector_left * right_second_active
    left_weight = left_active * projector_right
    right_weight = projector_right * second_active
    joined_weight = left_active * projector_right * second_active
    projected_gram = (
        projected_first * projector_right * projected_second.T
        + projected_second * projector_right * projected_first.T
    ) / 2
    trace_kernel = left_weight.T * projector_left * right_weight.T

    trace_left_first = (
        sp.trace(left_weight * projected_first.T)
        + spectator_count * left_spectator * right_first_spectator
    )
    trace_left_second = (
        sp.trace(left_weight * projected_second.T)
        + spectator_count * left_spectator * right_second_spectator
    )
    trace_first_right = (
        sp.trace(projected_first * right_weight)
        + spectator_count * right_first_spectator * second_spectator
    )
    trace_second_right = (
        sp.trace(projected_second * right_weight)
        + spectator_count * right_second_spectator * second_spectator
    )
    crossed_first = (
        frobenius(
            left_weight * projected_first.T,
            projected_second * right_weight,
        )
        + spectator_count
        * left_spectator
        * second_spectator
        * right_first_spectator
        * right_second_spectator
    )
    crossed_second = (
        frobenius(
            left_weight * projected_second.T,
            projected_first * right_weight,
        )
        + spectator_count
        * left_spectator
        * second_spectator
        * right_first_spectator
        * right_second_spectator
    )
    first_trace_subtraction = (
        frobenius(trace_active, trace_kernel)
        + frobenius(trace_active.T, trace_kernel)
        + 2
        * spectator_count
        * left_spectator
        * second_spectator
        * right_first_spectator
        * right_second_spectator
    )
    second_trace_subtraction = frobenius(joined_weight, projected_gram) + (
        spectator_count
        * left_spectator
        * second_spectator
        * right_first_spectator
        * right_second_spectator
    )
    projected_trace = (
        sp.trace(projector_right * trace_active)
        + spectator_count * right_first_spectator * right_second_spectator
    )
    joined_trace = (
        frobenius(joined_weight, projector_left)
        + spectator_count * left_spectator * second_spectator
    )
    return sp.factor(
        (
            trace_left_first * trace_second_right
            + trace_left_second * trace_first_right
            + crossed_first
            + crossed_second
        )
        / 4
        - first_trace_subtraction / (2 * transverse_dimension)
        - second_trace_subtraction / transverse_dimension
        + projected_trace * joined_trace / transverse_dimension**2
    )


def stereographic_direction(
    first: sp.Rational,
    second: sp.Rational,
    third: sp.Rational,
) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    norm = first**2 + second**2 + third**2
    denominator = 1 + norm
    return (
        sp.factor(2 * first / denominator),
        sp.factor(2 * second / denominator),
        sp.factor(2 * third / denominator),
        sp.factor((1 - norm) / denominator),
    )


def cut_coordinates(
    cosine: sp.Rational,
    sine: sp.Rational,
    direction: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr],
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    direction_x, _, direction_z, extra = direction
    propagator_left = sp.factor(-2 * (1 - direction_z))
    propagator_right = sp.factor(2 * (-1 + sine * direction_x + cosine * direction_z))
    mu_squared = sp.factor(extra**2)
    return propagator_left, propagator_right, mu_squared


def monomials(maximum_degree: int) -> list[tuple[int, int, int]]:
    return [
        (left_power, right_power, mu_power)
        for mu_power in range(maximum_degree // 2 + 1)
        for left_power in range(maximum_degree - 2 * mu_power + 1)
        for right_power in range(maximum_degree - 2 * mu_power - left_power + 1)
    ]


def sample_basis(
    cosine: sp.Rational,
    sine: sp.Rational,
    maximum_degree: int,
) -> list[tuple[sp.Rational, sp.Rational, sp.Rational]]:
    powers = monomials(maximum_degree)
    candidates = [
        triple
        for triple in product(
            [
                sp.Rational(-3, 2),
                sp.Rational(-1),
                sp.Rational(-1, 2),
                sp.Rational(0),
                sp.Rational(1, 2),
                sp.Rational(1),
                sp.Rational(3, 2),
            ],
            repeat=3,
        )
        if triple != (0, 0, 0)
    ]
    prime = 2_147_483_647
    echelon: dict[int, list[int]] = {}
    selected: list[tuple[sp.Rational, sp.Rational, sp.Rational]] = []

    def finite_field(value: sp.Expr) -> int:
        numerator, denominator = sp.fraction(sp.cancel(value))
        return int(numerator) % prime * pow(int(denominator) % prime, -1, prime) % prime

    for triple in candidates:
        coordinates = cut_coordinates(cosine, sine, stereographic_direction(*triple))
        modular_coordinates = tuple(finite_field(value) for value in coordinates)
        row = [
            pow(modular_coordinates[0], a, prime)
            * pow(modular_coordinates[1], b, prime)
            * pow(modular_coordinates[2], c, prime)
            % prime
            for a, b, c in powers
        ]
        for pivot in sorted(echelon):
            multiplier = row[pivot]
            if multiplier:
                row = [
                    (value - multiplier * basis_value) % prime
                    for value, basis_value in zip(row, echelon[pivot])
                ]
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is None:
            continue
        inverse = pow(row[pivot], -1, prime)
        row = [value * inverse % prime for value in row]
        for old_pivot, old_row in list(echelon.items()):
            multiplier = old_row[pivot]
            if multiplier:
                echelon[old_pivot] = [
                    (value - multiplier * new_value) % prime
                    for value, new_value in zip(old_row, row)
                ]
        echelon[pivot] = row
        selected.append(triple)
        if len(selected) == len(powers):
            return selected
    raise RuntimeError(f"sample rank {len(selected)} != {len(powers)}")


def box_normalization(cosine: sp.Rational, sine: sp.Rational) -> sp.Expr:
    direction_x = sp.factor((1 - cosine) / sine)
    directions = [
        (direction_x, sp.I * direction_x, sp.Integer(1)),
        (direction_x, -sp.I * direction_x, sp.Integer(1)),
    ]
    numerator = sp.factor(
        sum(covariant_hh_cut_numerator(4, cosine, sine, direction) for direction in directions) / 2
    )
    invariant_t = sp.factor(-2 * (1 + cosine))
    invariant_u = sp.factor(-2 * (1 - cosine))
    invariant_s = sp.factor(-invariant_t - invariant_u)
    expected_box = sp.factor(invariant_u**4 * (invariant_t**4 + invariant_u**4) / 32)
    return sp.factor(numerator / (invariant_s**2 * expected_box))


def reconstruct_polynomial(
    dimension: int,
    cosine: sp.Rational,
    sine: sp.Rational,
    maximum_degree: int,
) -> tuple[sp.Expr, list[dict[str, str]], sp.Expr]:
    powers = monomials(maximum_degree)
    samples = sample_basis(cosine, sine, maximum_degree)
    normalization = box_normalization(cosine, sine)
    matrix_rows = []
    values = []
    sample_rows = []
    for index, triple in enumerate(samples, start=1):
        direction = stereographic_direction(*triple)
        reflected = (direction[0], -direction[1], direction[2], direction[3])
        coordinates = cut_coordinates(cosine, sine, direction)
        even_numerator = sp.factor(
            (
                covariant_hh_cut_numerator(dimension, cosine, sine, direction)
                + covariant_hh_cut_numerator(dimension, cosine, sine, reflected)
            )
            / (2 * normalization)
        )
        matrix_rows.append([coordinates[0] ** a * coordinates[1] ** b * coordinates[2] ** c for a, b, c in powers])
        values.append(even_numerator)
        sample_rows.append(
            {
                "sample": str(index),
                "stereographic": str(tuple(map(str, triple))),
                "P_left": str(coordinates[0]),
                "P_right": str(coordinates[1]),
                "mu_squared": str(coordinates[2]),
                "normalized_even_numerator": str(even_numerator),
            }
        )
    coefficients = sp.Matrix(matrix_rows).inv() * sp.Matrix(values)
    P_left, P_right, mu_squared = sp.symbols("P_left P_right mu_squared")
    polynomial = sp.factor(
        sum(
            coefficient * P_left**a * P_right**b * mu_squared**c
            for coefficient, (a, b, c) in zip(coefficients, powers)
        )
    )
    heldout_triple = (sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(-1, 4))
    heldout_direction = stereographic_direction(*heldout_triple)
    heldout_reflected = (
        heldout_direction[0],
        -heldout_direction[1],
        heldout_direction[2],
        heldout_direction[3],
    )
    heldout_coordinates = cut_coordinates(cosine, sine, heldout_direction)
    heldout_value = sp.factor(
        (
            covariant_hh_cut_numerator(dimension, cosine, sine, heldout_direction)
            + covariant_hh_cut_numerator(dimension, cosine, sine, heldout_reflected)
        )
        / (2 * normalization)
    )
    heldout_prediction = polynomial.subs(
        {
            P_left: heldout_coordinates[0],
            P_right: heldout_coordinates[1],
            mu_squared: heldout_coordinates[2],
        }
    )
    return polynomial, sample_rows, sp.factor(heldout_prediction - heldout_value)


def symbolic_even_numerator(
    cosine: sp.Rational,
    sine: sp.Rational,
    triple: tuple[sp.Rational, sp.Rational, sp.Rational],
    normalization: sp.Expr,
) -> tuple[sp.Expr, tuple[sp.Expr, sp.Expr, sp.Expr]]:
    direction = stereographic_direction(*triple)
    reflected = (direction[0], -direction[1], direction[2], direction[3])
    coordinates = cut_coordinates(cosine, sine, direction)
    value = sp.factor(
        (
            spectator_compressed_hh_cut_numerator(D, cosine, sine, direction)
            + spectator_compressed_hh_cut_numerator(D, cosine, sine, reflected)
        )
        / (2 * normalization)
    )
    scaled = sp.factor(DIMENSION_DENOMINATOR * value)
    numerator, denominator = sp.together(scaled).as_numer_denom()
    if D in denominator.free_symbols:
        raise RuntimeError("spectator compression exceeded the expected D-2 denominator")
    if sp.Poly(numerator, D).degree() > DIMENSION_NUMERATOR_DEGREE:
        raise RuntimeError("spectator compression exceeded cubic numerator dependence")
    return value, coordinates


def reconstruct_symbolic_dimension_polynomial(
    cosine: sp.Rational,
    sine: sp.Rational,
    maximum_degree: int,
    cache_path: Path,
) -> tuple[sp.Expr, list[dict[str, object]], list[dict[str, object]], sp.Expr]:
    powers = monomials(maximum_degree)
    samples = sample_basis(cosine, sine, maximum_degree)
    normalization = box_normalization(cosine, sine)
    cache_header = {
        "checkpoint_marker": MARKER,
        "right_double_copy": "B2_p3_times_B2_p4",
        "left_yang_mills_basis": "Boels_Luo_GluonsSymms_element_2_equals_8_st_A_YM",
        "state_sum": "physical_reference_projector",
        "cosine": str(cosine),
        "sine": str(sine),
        "degree": maximum_degree,
        "box_normalization": str(normalization),
        "dimension_denominator": str(DIMENSION_DENOMINATOR),
        "dimension_numerator_degree": DIMENSION_NUMERATOR_DEGREE,
    }
    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
        for key, value in cache_header.items():
            if cache.get(key) != value:
                raise RuntimeError(f"symbolic sample cache mismatch for {key}")
    else:
        cache = {**cache_header, "samples": {}}

    matrix_rows: list[list[sp.Expr]] = []
    scaled_values: list[sp.Expr] = []
    sample_rows: list[dict[str, object]] = []
    for index, triple in enumerate(samples, start=1):
        cache_key = str(tuple(map(str, triple)))
        cached = cache["samples"].get(cache_key)
        if cached is None:
            value, coordinates = symbolic_even_numerator(cosine, sine, triple, normalization)
            cached = {
                "P_left": str(coordinates[0]),
                "P_right": str(coordinates[1]),
                "mu_squared": str(coordinates[2]),
                "normalized_even_numerator": exact(value),
            }
            cache["samples"][cache_key] = cached
            atomic_write_json(cache_path, cache)
            print(f"cached symbolic cut sample {index}/{len(samples)}", file=sys.stderr, flush=True)
        coordinates = tuple(sp.sympify(cached[name]) for name in ("P_left", "P_right", "mu_squared"))
        value = sp.sympify(cached["normalized_even_numerator"], locals={"D": D})
        scaled_value = sp.factor(DIMENSION_DENOMINATOR * value)
        polynomial_in_D = sp.Poly(scaled_value, D)
        matrix_rows.append(
            [coordinates[0] ** a * coordinates[1] ** b * coordinates[2] ** c for a, b, c in powers]
        )
        scaled_values.append(scaled_value)
        sample_rows.append(
            {
                "sample": index,
                "stereographic": cache_key,
                "P_left": exact(coordinates[0]),
                "P_right": exact(coordinates[1]),
                "mu_squared": exact(coordinates[2]),
                "coefficient_D0": exact(polynomial_in_D.coeff_monomial(1)),
                "coefficient_D1": exact(polynomial_in_D.coeff_monomial(D)),
                "coefficient_D2": exact(polynomial_in_D.coeff_monomial(D**2)),
                "coefficient_D3": exact(polynomial_in_D.coeff_monomial(D**3)),
                "normalized_even_numerator": exact(value),
            }
        )

    interpolation_matrix = sp.Matrix(matrix_rows)
    inverse_matrix = interpolation_matrix.inv()
    coefficient_vectors = [
        inverse_matrix
        * sp.Matrix([sp.Poly(value, D).coeff_monomial(D**power) for value in scaled_values])
        for power in range(DIMENSION_NUMERATOR_DEGREE + 1)
    ]
    P_left, P_right, mu_squared = sp.symbols("P_left P_right mu_squared")
    coefficient_rows: list[dict[str, object]] = []
    reconstructed = sp.Integer(0)
    for index, (left_power, right_power, mu_power) in enumerate(powers):
        dimension_coefficients = [sp.factor(vector[index]) for vector in coefficient_vectors]
        coefficient_numerator = sp.factor(
            sum(value * D**power for power, value in enumerate(dimension_coefficients))
        )
        coefficient = sp.factor(coefficient_numerator / DIMENSION_DENOMINATOR)
        reconstructed += coefficient * P_left**left_power * P_right**right_power * mu_squared**mu_power
        coefficient_rows.append(
            {
                "P_left_power": left_power,
                "P_right_power": right_power,
                "mu_squared_power": mu_power,
                "coefficient_D0": exact(dimension_coefficients[0]),
                "coefficient_D1": exact(dimension_coefficients[1]),
                "coefficient_D2": exact(dimension_coefficients[2]),
                "coefficient_D3": exact(dimension_coefficients[3]),
                "coefficient": exact(coefficient),
            }
        )
    reconstructed = sp.factor(reconstructed)

    heldout_triple = (sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(-1, 4))
    heldout_value, heldout_coordinates = symbolic_even_numerator(
        cosine, sine, heldout_triple, normalization
    )
    heldout_prediction = reconstructed.subs(
        {
            P_left: heldout_coordinates[0],
            P_right: heldout_coordinates[1],
            mu_squared: heldout_coordinates[2],
        }
    )
    heldout_residual = sp.factor(heldout_prediction - heldout_value)
    return reconstructed, coefficient_rows, sample_rows, heldout_residual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--symbolic-d", action="store_true")
    parser.add_argument("--crossed", action="store_true")
    parser.add_argument("--cosine")
    parser.add_argument("--sine")
    parser.add_argument("--angle-tag")
    parser.add_argument("--dimension", type=int, default=5)
    parser.add_argument("--degree", type=int, default=8)
    args = parser.parse_args()
    if not RESULT_4999.exists():
        raise FileNotFoundError(RESULT_4999)
    result_4999 = json.loads(RESULT_4999.read_text(encoding="utf-8"))
    if result_4999.get("checkpoint_marker") != "MTS_4999_HH_ONE_SCALE_IR_LAURENT_COMPLETION":
        raise RuntimeError("4999 source lock failed")
    cosine = sp.Rational(args.cosine) if args.cosine else sp.Rational(3, 5)
    sine = sp.Rational(args.sine) if args.sine else sp.Rational(4, 5)
    if args.crossed:
        cosine = -cosine
    if sp.factor(cosine**2 + sine**2 - 1) != 0:
        raise ValueError("cosine and sine must define an exact rational unit direction")
    if args.symbolic_d:
        SOURCE.mkdir(parents=True, exist_ok=True)
        if args.angle_tag:
            prefix = f"{args.angle_tag}_" + ("crossed_" if args.crossed else "")
            cache_path = SOURCE / f"{prefix}symbolic_cut_sample_cache.json"
            coefficient_path = SOURCE / f"{prefix}generic_D_hh_cut_polynomial_coefficients.csv"
            sample_path = SOURCE / f"{prefix}generic_D_hh_cut_reconstruction_samples.csv"
            result_path = SOURCE / f"{prefix}covariant_hh_mu_moment_reconstruction_results.json"
        else:
            cache_path = CROSSED_CACHE_JSON if args.crossed else CACHE_JSON
            coefficient_path = CROSSED_COEFFICIENT_CSV if args.crossed else COEFFICIENT_CSV
            sample_path = CROSSED_SAMPLE_CSV if args.crossed else SAMPLE_CSV
            result_path = CROSSED_RESULT_JSON if args.crossed else RESULT_JSON
        polynomial, coefficient_rows, sample_rows, heldout_residual = reconstruct_symbolic_dimension_polynomial(
            cosine, sine, args.degree, cache_path
        )
        if heldout_residual != 0:
            raise RuntimeError(f"symbolic held-out residual is {heldout_residual}")
        direction = stereographic_direction(sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(-1, 4))
        projector_residual = sp.factor(
            covariant_hh_cut_numerator(5, cosine, sine, direction)
            - covariant_hh_cut_numerator(5, cosine, sine, direction, reference_projector=True)
        )
        compression_residuals = {
            str(dimension): exact(
                spectator_compressed_hh_cut_numerator(dimension, cosine, sine, direction)
                - covariant_hh_cut_numerator(dimension, cosine, sine, direction)
            )
            for dimension in (5, 6, 7)
        }
        if projector_residual != 0 or any(value != "0" for value in compression_residuals.values()):
            raise RuntimeError("projector or spectator-compression validation failed")
        write_csv(coefficient_path, coefficient_rows)
        write_csv(sample_path, sample_rows)
        result = {
            "checkpoint_marker": MARKER,
            "kinematic_orientation": (
                f"custom_{args.angle_tag}_crossed" if args.angle_tag and args.crossed
                else f"custom_{args.angle_tag}" if args.angle_tag
                else "st_crossed" if args.crossed
                else "su_direct"
            ),
            "cosine": exact(cosine),
            "sine": exact(sine),
            "dimension_dependence": "cubic polynomial divided by D-2 after exact spectator trace cancellation",
            "maximum_weighted_loop_degree": args.degree,
            "box_normalization": exact(box_normalization(cosine, sine)),
            "left_yang_mills_basis": "Boels_Luo_GluonsSymms_element_2_equals_8_st_A_YM",
            "right_scalar_gravity_basis": "Boels_Luo_two_scalar_two_graviton_B2_left_times_B2_right",
            "state_sum": "physical_reference_projector",
            "sample_count": len(sample_rows),
            "coefficient_count": len(coefficient_rows),
            "polynomial": exact(polynomial),
            "heldout_residual": exact(heldout_residual),
            "reference_projector_residual": exact(projector_residual),
            "spectator_compression_residuals": compression_residuals,
            "outputs": [relative(path) for path in (cache_path, coefficient_path, sample_path, result_path)],
            "claim_status": "direct_generic_D_cut_integrand_reconstructed_master_reduction_open",
        }
        atomic_write_json(result_path, result)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if args.probe:
        polynomial, rows, heldout_residual = reconstruct_polynomial(
            args.dimension, cosine, sine, args.degree
        )
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "dimension": args.dimension,
                    "degree": args.degree,
                    "box_normalization": str(box_normalization(cosine, sine)),
                    "samples": len(rows),
                    "polynomial": str(polynomial),
                    "heldout_residual": str(heldout_residual),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    print(json.dumps({"checkpoint_marker": MARKER, "status": "probe_only_use_--probe"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
