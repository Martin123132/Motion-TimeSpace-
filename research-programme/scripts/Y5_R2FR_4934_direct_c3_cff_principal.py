from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from itertools import combinations
from pathlib import Path

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4934"
LINEAR_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_portal_linear_c3_zero.py"
C3_FLOW = POST / "source-intake" / "functional_rg" / "4933" / "Flow_mendeley_input_extracted.wl"
PHOTON_FLOW = POST / "source-intake" / "functional_rg" / "4933" / "RHS_general_regulator_extracted.wl"
OUTPUT = SOURCE_DIR / "direct_c3_cff_principal_results.json"
MARKER = "MTS_4934_DIRECT_C3_CFF_PRINCIPAL"
EXPECTED_HASHES = {
    C3_FLOW: "7a6ce0ad809f1c8932511d4652542599ea30499805d8b71a5b758443a0e797d1",
    PHOTON_FLOW: "28be0c586f31fa83a0a0b888f686b5564f6af0c4f74f5888d229aa9b58a8903c",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def load_linear_module():
    specification = importlib.util.spec_from_file_location("mts_4934_linear_direct", LINEAR_SCRIPT)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the 4934 Weyl helper")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def symmetric_basis(dimension: int) -> list[sp.Matrix]:
    basis: list[sp.Matrix] = []
    for diagonal_index in range(dimension):
        element = sp.zeros(dimension)
        element[diagonal_index, diagonal_index] = 1
        basis.append(element)
    for first_index, second_index in combinations(range(dimension), 2):
        element = sp.zeros(dimension)
        element[first_index, second_index] = 1 / sp.sqrt(2)
        element[second_index, first_index] = 1 / sp.sqrt(2)
        basis.append(element)
    return basis


def dewitt_matrix(basis: list[sp.Matrix]) -> sp.Matrix:
    count = len(basis)
    return sp.Matrix(
        count,
        count,
        lambda row_index, column_index: sp.trace(basis[row_index] * basis[column_index])
        - sp.trace(basis[row_index]) * sp.trace(basis[column_index]) / 2,
    )


def linearized_weyl(
    metric_mode: sp.Matrix, momentum: tuple[sp.Symbol, ...]
) -> sp.MutableDenseNDimArray:
    dimension = 4
    linear_riemann = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for index_a in range(dimension):
        for index_b in range(dimension):
            for index_c in range(dimension):
                for index_d in range(dimension):
                    linear_riemann[index_a, index_b, index_c, index_d] = sp.Rational(1, 2) * (
                        momentum[index_c] * momentum[index_b] * metric_mode[index_a, index_d]
                        + momentum[index_d] * momentum[index_a] * metric_mode[index_b, index_c]
                        - momentum[index_d] * momentum[index_b] * metric_mode[index_a, index_c]
                        - momentum[index_c] * momentum[index_a] * metric_mode[index_b, index_d]
                    )
    linear_ricci = sp.MutableDenseNDimArray.zeros(dimension, dimension)
    for index_b in range(dimension):
        for index_d in range(dimension):
            linear_ricci[index_b, index_d] = sum(
                linear_riemann[index_a, index_b, index_a, index_d]
                for index_a in range(dimension)
            )
    linear_scalar = sum(
        linear_riemann[index_a, index_b, index_a, index_b]
        for index_a in range(dimension)
        for index_b in range(dimension)
    )
    linear_weyl = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for index_a in range(dimension):
        for index_b in range(dimension):
            for index_c in range(dimension):
                for index_d in range(dimension):
                    linear_weyl[index_a, index_b, index_c, index_d] = sp.expand(
                        linear_riemann[index_a, index_b, index_c, index_d]
                        - sp.Rational(1, 2)
                        * (
                            int(index_a == index_c) * linear_ricci[index_d, index_b]
                            - int(index_a == index_d) * linear_ricci[index_c, index_b]
                            - int(index_b == index_c) * linear_ricci[index_d, index_a]
                            + int(index_b == index_d) * linear_ricci[index_c, index_a]
                        )
                        + sp.Rational(1, 6)
                        * linear_scalar
                        * (
                            int(index_a == index_c and index_b == index_d)
                            - int(index_a == index_d and index_b == index_c)
                        )
                    )
    return linear_weyl


def c3_hessian(
    background_weyl: sp.MutableDenseNDimArray,
    linear_weyls: list[sp.MutableDenseNDimArray],
) -> sp.Matrix:
    dimension = 4
    mode_count = len(linear_weyls)
    return sp.Matrix(
        mode_count,
        mode_count,
        lambda row_index, column_index: sp.expand(
            6
            * sum(
                background_weyl[index_r, index_s, index_m, index_n]
                * linear_weyls[row_index][index_m, index_n, index_a, index_b]
                * linear_weyls[column_index][index_a, index_b, index_r, index_s]
                for index_r in range(dimension)
                for index_s in range(dimension)
                for index_m in range(dimension)
                for index_n in range(dimension)
                for index_a in range(dimension)
                for index_b in range(dimension)
            )
        ),
    )


def sample_field_strength(dimension: int) -> sp.MutableDenseNDimArray:
    field_strength = sp.MutableDenseNDimArray.zeros(dimension, dimension)
    entries = (
        (0, 1, 1),
        (0, 2, 2),
        (0, 3, -1),
        (1, 2, 3),
        (1, 3, 1),
        (2, 3, 2),
    )
    for first_index, second_index, value in entries:
        field_strength[first_index, second_index] = value
        field_strength[second_index, first_index] = -value
    return field_strength


def cff_invariant(
    background_weyl: sp.MutableDenseNDimArray,
    field_strength: sp.MutableDenseNDimArray,
) -> sp.Expr:
    dimension = 4
    return sp.simplify(
        sum(
            background_weyl[index_a, index_b, index_c, index_d]
            * field_strength[index_a, index_b]
            * field_strength[index_c, index_d]
            for index_a in range(dimension)
            for index_b in range(dimension)
            for index_c in range(dimension)
            for index_d in range(dimension)
        )
    )


def maxwell_metric_hessian(
    basis: list[sp.Matrix], field_strength: sp.MutableDenseNDimArray
) -> sp.Matrix:
    dimension = 4
    identity = sp.eye(dimension)
    hessian = sp.zeros(len(basis))
    for row_index, first_mode in enumerate(basis):
        for column_index, second_mode in enumerate(basis):
            first_volume = sp.trace(first_mode) / 2
            second_volume = sp.trace(second_mode) / 2
            mixed_volume = (
                sp.trace(first_mode) * sp.trace(second_mode) / 4
                - sp.trace(first_mode * second_mode) / 2
            )
            first_inverse = -first_mode
            second_inverse = -second_mode
            mixed_inverse = first_mode * second_mode + second_mode * first_mode
            value = 0
            for index_a in range(dimension):
                for index_b in range(dimension):
                    for index_c in range(dimension):
                        for index_d in range(dimension):
                            mixed_metric = (
                                mixed_volume * identity[index_a, index_c] * identity[index_b, index_d]
                                + first_volume
                                * (
                                    second_inverse[index_a, index_c] * identity[index_b, index_d]
                                    + identity[index_a, index_c] * second_inverse[index_b, index_d]
                                )
                                + second_volume
                                * (
                                    first_inverse[index_a, index_c] * identity[index_b, index_d]
                                    + identity[index_a, index_c] * first_inverse[index_b, index_d]
                                )
                                + mixed_inverse[index_a, index_c] * identity[index_b, index_d]
                                + identity[index_a, index_c] * mixed_inverse[index_b, index_d]
                                + first_inverse[index_a, index_c] * second_inverse[index_b, index_d]
                                + second_inverse[index_a, index_c] * first_inverse[index_b, index_d]
                            )
                            value += (
                                sp.Rational(1, 4)
                                * field_strength[index_a, index_b]
                                * field_strength[index_c, index_d]
                                * mixed_metric
                            )
            hessian[row_index, column_index] = sp.simplify(value)
    return hessian


def photon_field_variation(
    momentum: tuple[sp.Symbol, ...], photon_index: int
) -> sp.MutableDenseNDimArray:
    dimension = 4
    return sp.MutableDenseNDimArray(
        [
            momentum[index_a] * int(index_b == photon_index)
            - momentum[index_b] * int(index_a == photon_index)
            for index_a in range(dimension)
            for index_b in range(dimension)
        ],
        (dimension, dimension),
    )


def maxwell_mixed_hessian(
    basis: list[sp.Matrix],
    field_strength: sp.MutableDenseNDimArray,
    momentum: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    dimension = 4
    identity = sp.eye(dimension)
    mixed = sp.zeros(len(basis), dimension)
    for metric_index, metric_mode in enumerate(basis):
        for photon_index in range(dimension):
            photon_field = photon_field_variation(momentum, photon_index)
            field_contraction = sum(
                field_strength[index_a, index_b] * photon_field[index_a, index_b]
                for index_a in range(dimension)
                for index_b in range(dimension)
            )
            value = sp.trace(metric_mode) * field_contraction / 4
            value -= sp.Rational(1, 2) * sum(
                field_strength[index_a, index_b]
                * photon_field[index_c, index_d]
                * (
                    metric_mode[index_a, index_c] * identity[index_b, index_d]
                    + identity[index_a, index_c] * metric_mode[index_b, index_d]
                )
                for index_a in range(dimension)
                for index_b in range(dimension)
                for index_c in range(dimension)
                for index_d in range(dimension)
            )
            mixed[metric_index, photon_index] = sp.expand(value)
    return mixed


def cff_mixed_hessian(
    linear_weyls: list[sp.MutableDenseNDimArray],
    field_strength: sp.MutableDenseNDimArray,
    momentum: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    dimension = 4
    mixed = sp.zeros(len(linear_weyls), dimension)
    for metric_index, metric_weyl in enumerate(linear_weyls):
        for photon_index in range(dimension):
            photon_field = photon_field_variation(momentum, photon_index)
            mixed[metric_index, photon_index] = sp.expand(
                -2
                * sum(
                    metric_weyl[index_a, index_b, index_c, index_d]
                    * field_strength[index_a, index_b]
                    * photon_field[index_c, index_d]
                    for index_a in range(dimension)
                    for index_b in range(dimension)
                    for index_c in range(dimension)
                    for index_d in range(dimension)
                )
            )
    return mixed


def first_christoffel(
    metric_mode: sp.Matrix, wave_vector: tuple[sp.Expr, ...]
) -> sp.MutableDenseNDimArray:
    dimension = 4
    christoffel = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension)
    for upper_index in range(dimension):
        for first_lower in range(dimension):
            for second_lower in range(dimension):
                christoffel[upper_index, first_lower, second_lower] = sp.I * sp.Rational(1, 2) * (
                    wave_vector[first_lower] * metric_mode[upper_index, second_lower]
                    + wave_vector[second_lower] * metric_mode[upper_index, first_lower]
                    - wave_vector[upper_index] * metric_mode[first_lower, second_lower]
                )
    return christoffel


def first_riemann(
    christoffel: sp.MutableDenseNDimArray, wave_vector: tuple[sp.Expr, ...]
) -> sp.MutableDenseNDimArray:
    dimension = 4
    riemann = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for upper_index in range(dimension):
        for second_index in range(dimension):
            for third_index in range(dimension):
                for fourth_index in range(dimension):
                    riemann[upper_index, second_index, third_index, fourth_index] = sp.expand(
                        sp.I
                        * wave_vector[third_index]
                        * christoffel[upper_index, fourth_index, second_index]
                        - sp.I
                        * wave_vector[fourth_index]
                        * christoffel[upper_index, third_index, second_index]
                    )
    return riemann


def mixed_riemann(
    first_connection: sp.MutableDenseNDimArray,
    second_connection: sp.MutableDenseNDimArray,
) -> sp.MutableDenseNDimArray:
    dimension = 4
    riemann = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for upper_index in range(dimension):
        for second_index in range(dimension):
            for third_index in range(dimension):
                for fourth_index in range(dimension):
                    riemann[upper_index, second_index, third_index, fourth_index] = sp.expand(
                        sum(
                            first_connection[upper_index, third_index, contracted_index]
                            * second_connection[contracted_index, fourth_index, second_index]
                            + second_connection[upper_index, third_index, contracted_index]
                            * first_connection[contracted_index, fourth_index, second_index]
                            - first_connection[upper_index, fourth_index, contracted_index]
                            * second_connection[contracted_index, third_index, second_index]
                            - second_connection[upper_index, fourth_index, contracted_index]
                            * first_connection[contracted_index, third_index, second_index]
                            for contracted_index in range(dimension)
                        )
                    )
    return riemann


def ricci_from_riemann(
    riemann: sp.MutableDenseNDimArray,
) -> sp.MutableDenseNDimArray:
    dimension = 4
    return sp.MutableDenseNDimArray(
        [
            sum(
                riemann[contracted_index, second_index, contracted_index, fourth_index]
                for contracted_index in range(dimension)
            )
            for second_index in range(dimension)
            for fourth_index in range(dimension)
        ],
        (dimension, dimension),
    )


def lower_riemann(
    riemann: sp.MutableDenseNDimArray,
) -> sp.MutableDenseNDimArray:
    dimension = 4
    return sp.MutableDenseNDimArray(
        [
            riemann[first_index, second_index, third_index, fourth_index]
            for first_index in range(dimension)
            for second_index in range(dimension)
            for third_index in range(dimension)
            for fourth_index in range(dimension)
        ],
        (dimension, dimension, dimension, dimension),
    )


def first_weyl_from_riemann(
    lower_curvature: sp.MutableDenseNDimArray,
    ricci: sp.MutableDenseNDimArray,
    scalar: sp.Expr,
) -> sp.MutableDenseNDimArray:
    dimension = 4
    weyl = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for index_a in range(dimension):
        for index_b in range(dimension):
            for index_c in range(dimension):
                for index_d in range(dimension):
                    weyl[index_a, index_b, index_c, index_d] = sp.expand(
                        lower_curvature[index_a, index_b, index_c, index_d]
                        - sp.Rational(1, 2)
                        * (
                            int(index_a == index_c) * ricci[index_d, index_b]
                            - int(index_a == index_d) * ricci[index_c, index_b]
                            - int(index_b == index_c) * ricci[index_d, index_a]
                            + int(index_b == index_d) * ricci[index_c, index_a]
                        )
                        + scalar
                        * sp.Rational(1, 6)
                        * (
                            int(index_a == index_c and index_b == index_d)
                            - int(index_a == index_d and index_b == index_c)
                        )
                    )
    return weyl


def cff_metric_hessian_entry(
    first_mode: sp.Matrix,
    second_mode: sp.Matrix,
    field_strength: sp.MutableDenseNDimArray,
    momentum: tuple[sp.Symbol, ...],
) -> sp.Expr:
    dimension = 4
    first_wave = tuple(-component for component in momentum)
    second_wave = momentum
    first_connection = first_christoffel(first_mode, first_wave)
    second_connection = first_christoffel(second_mode, second_wave)
    first_curvature = first_riemann(first_connection, first_wave)
    second_curvature = first_riemann(second_connection, second_wave)
    mixed_curvature = mixed_riemann(first_connection, second_connection)
    first_ricci = ricci_from_riemann(first_curvature)
    second_ricci = ricci_from_riemann(second_curvature)
    mixed_ricci = ricci_from_riemann(mixed_curvature)
    first_scalar = sum(first_ricci[index_a, index_a] for index_a in range(dimension))
    second_scalar = sum(second_ricci[index_a, index_a] for index_a in range(dimension))
    mixed_scalar = sp.expand(
        sum(mixed_ricci[index_a, index_a] for index_a in range(dimension))
        - sum(
            first_mode[index_a, index_b] * second_ricci[index_a, index_b]
            + second_mode[index_a, index_b] * first_ricci[index_a, index_b]
            for index_a in range(dimension)
            for index_b in range(dimension)
        )
    )
    first_lower = lower_riemann(first_curvature)
    second_lower = lower_riemann(second_curvature)
    mixed_lower = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for index_a in range(dimension):
        for index_b in range(dimension):
            for index_c in range(dimension):
                for index_d in range(dimension):
                    mixed_lower[index_a, index_b, index_c, index_d] = sp.expand(
                        mixed_curvature[index_a, index_b, index_c, index_d]
                        + sum(
                            first_mode[index_a, contracted_index]
                            * second_curvature[contracted_index, index_b, index_c, index_d]
                            + second_mode[index_a, contracted_index]
                            * first_curvature[contracted_index, index_b, index_c, index_d]
                            for contracted_index in range(dimension)
                        )
                    )
    first_weyl = first_weyl_from_riemann(first_lower, first_ricci, first_scalar)
    second_weyl = first_weyl_from_riemann(second_lower, second_ricci, second_scalar)
    mixed_weyl = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for index_a in range(dimension):
        for index_b in range(dimension):
            for index_c in range(dimension):
                for index_d in range(dimension):
                    metric_ricci_mixed = (
                        int(index_a == index_c) * mixed_ricci[index_d, index_b]
                        - int(index_a == index_d) * mixed_ricci[index_c, index_b]
                        - int(index_b == index_c) * mixed_ricci[index_d, index_a]
                        + int(index_b == index_d) * mixed_ricci[index_c, index_a]
                    )
                    metric_ricci_mixed += (
                        first_mode[index_a, index_c] * second_ricci[index_d, index_b]
                        - first_mode[index_a, index_d] * second_ricci[index_c, index_b]
                        - first_mode[index_b, index_c] * second_ricci[index_d, index_a]
                        + first_mode[index_b, index_d] * second_ricci[index_c, index_a]
                        + second_mode[index_a, index_c] * first_ricci[index_d, index_b]
                        - second_mode[index_a, index_d] * first_ricci[index_c, index_b]
                        - second_mode[index_b, index_c] * first_ricci[index_d, index_a]
                        + second_mode[index_b, index_d] * first_ricci[index_c, index_a]
                    )
                    scalar_metric_mixed = mixed_scalar * (
                        int(index_a == index_c and index_b == index_d)
                        - int(index_a == index_d and index_b == index_c)
                    )
                    scalar_metric_mixed += first_scalar * (
                        second_mode[index_a, index_c] * int(index_b == index_d)
                        + int(index_a == index_c) * second_mode[index_b, index_d]
                        - second_mode[index_a, index_d] * int(index_b == index_c)
                        - int(index_a == index_d) * second_mode[index_b, index_c]
                    )
                    scalar_metric_mixed += second_scalar * (
                        first_mode[index_a, index_c] * int(index_b == index_d)
                        + int(index_a == index_c) * first_mode[index_b, index_d]
                        - first_mode[index_a, index_d] * int(index_b == index_c)
                        - int(index_a == index_d) * first_mode[index_b, index_c]
                    )
                    mixed_weyl[index_a, index_b, index_c, index_d] = sp.expand(
                        mixed_lower[index_a, index_b, index_c, index_d]
                        - metric_ricci_mixed / 2
                        + scalar_metric_mixed / 6
                    )
    raised_mixed = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for index_a in range(dimension):
        for index_b in range(dimension):
            for index_c in range(dimension):
                for index_d in range(dimension):
                    value = mixed_weyl[index_a, index_b, index_c, index_d]
                    for raised_position in range(4):
                        for contracted_index in range(dimension):
                            first_indices = [index_a, index_b, index_c, index_d]
                            second_indices = [index_a, index_b, index_c, index_d]
                            first_indices[raised_position] = contracted_index
                            second_indices[raised_position] = contracted_index
                            value -= first_mode[
                                (index_a, index_b, index_c, index_d)[raised_position],
                                contracted_index,
                            ] * second_weyl[tuple(first_indices)]
                            value -= second_mode[
                                (index_a, index_b, index_c, index_d)[raised_position],
                                contracted_index,
                            ] * first_weyl[tuple(second_indices)]
                    raised_mixed[index_a, index_b, index_c, index_d] = sp.expand(value)
    first_volume = sp.trace(first_mode) / 2
    second_volume = sp.trace(second_mode) / 2
    return sp.expand(
        sum(
            (
                raised_mixed[index_a, index_b, index_c, index_d]
                + first_volume * second_weyl[index_a, index_b, index_c, index_d]
                + second_volume * first_weyl[index_a, index_b, index_c, index_d]
            )
            * field_strength[index_a, index_b]
            * field_strength[index_c, index_d]
            for index_a in range(dimension)
            for index_b in range(dimension)
            for index_c in range(dimension)
            for index_d in range(dimension)
        )
    )


def cff_metric_hessian(
    basis: list[sp.Matrix],
    field_strength: sp.MutableDenseNDimArray,
    momentum: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    hessian = sp.zeros(len(basis))
    for row_index, first_mode in enumerate(basis):
        for column_index in range(row_index, len(basis)):
            value = cff_metric_hessian_entry(
                first_mode, basis[column_index], field_strength, momentum
            )
            hessian[row_index, column_index] = value
            hessian[column_index, row_index] = value
    return hessian


def metric_rg_kernel_jacobians(
    basis: list[sp.Matrix],
    field_strength: sp.MutableDenseNDimArray,
    momentum: tuple[sp.Symbol, ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    dimension = 4
    identity = sp.eye(dimension)
    field_squared = sp.Rational(1, 4) * sum(
        field_strength[index_a, index_b] ** 2
        for index_a in range(dimension)
        for index_b in range(dimension)
    )
    metric_trace = sp.zeros(len(basis))
    metric_tl = sp.zeros(len(basis))
    for input_index, metric_mode in enumerate(basis):
        inverse_variation = -metric_mode
        field_squared_variation = sp.Rational(1, 4) * sum(
            field_strength[index_a, index_b]
            * field_strength[index_c, index_d]
            * (
                inverse_variation[index_a, index_c] * identity[index_b, index_d]
                + identity[index_a, index_c] * inverse_variation[index_b, index_d]
            )
            for index_a in range(dimension)
            for index_b in range(dimension)
            for index_c in range(dimension)
            for index_d in range(dimension)
        )
        quadratic_variation = sp.Matrix(
            dimension,
            dimension,
            lambda row_index, column_index: sum(
                field_strength[row_index, index_a]
                * inverse_variation[index_a, index_b]
                * field_strength[index_b, column_index]
                for index_a in range(dimension)
                for index_b in range(dimension)
            ),
        )
        trace_output = field_squared_variation * identity + field_squared * metric_mode
        tl_output = quadratic_variation + trace_output
        for output_index, output_mode in enumerate(basis):
            metric_trace[output_index, input_index] = sp.trace(output_mode * trace_output)
            metric_tl[output_index, input_index] = sp.trace(output_mode * tl_output)

    photon_trace = sp.zeros(len(basis), dimension)
    photon_tl = sp.zeros(len(basis), dimension)
    for photon_index in range(dimension):
        photon_field = photon_field_variation(momentum, photon_index)
        field_squared_variation = sp.Rational(1, 2) * sum(
            field_strength[index_a, index_b] * photon_field[index_a, index_b]
            for index_a in range(dimension)
            for index_b in range(dimension)
        )
        quadratic_variation = sp.Matrix(
            dimension,
            dimension,
            lambda row_index, column_index: sum(
                photon_field[row_index, contracted_index]
                * field_strength[contracted_index, column_index]
                + field_strength[row_index, contracted_index]
                * photon_field[contracted_index, column_index]
                for contracted_index in range(dimension)
            ),
        )
        trace_output = field_squared_variation * identity
        tl_output = quadratic_variation + trace_output
        for output_index, output_mode in enumerate(basis):
            photon_trace[output_index, photon_index] = sp.trace(output_mode * trace_output)
            photon_tl[output_index, photon_index] = sp.trace(output_mode * tl_output)
    return metric_trace, metric_tl, photon_trace, photon_tl


def photon_rg_metric_jacobian(
    basis: list[sp.Matrix],
    field_strength: sp.MutableDenseNDimArray,
    momentum: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    dimension = 4
    jacobian = sp.zeros(dimension, len(basis))
    for metric_index, metric_mode in enumerate(basis):
        metric_trace = sp.trace(metric_mode)
        for output_index in range(dimension):
            value = 0
            for index_lambda in range(dimension):
                for index_alpha in range(dimension):
                    connection_first = sp.Rational(1, 2) * (
                        momentum[index_alpha] * metric_mode[index_lambda, output_index]
                        + momentum[output_index] * metric_mode[index_lambda, index_alpha]
                        - momentum[index_lambda] * metric_mode[index_alpha, output_index]
                    )
                    value -= connection_first * field_strength[index_lambda, index_alpha]
                contracted_connection = (
                    sum(
                        momentum[index_alpha] * metric_mode[index_lambda, index_alpha]
                        for index_alpha in range(dimension)
                    )
                    - momentum[index_lambda] * metric_trace / 2
                )
                value -= contracted_connection * field_strength[output_index, index_lambda]
            jacobian[output_index, metric_index] = sp.expand(value)
    return jacobian


def sphere_average(
    expression: sp.Expr, momentum: tuple[sp.Symbol, ...], degree: int
) -> sp.Expr:
    dimension = len(momentum)
    polynomial = sp.Poly(sp.expand(expression), momentum)
    denominator = sp.prod(dimension + 2 * offset for offset in range(degree // 2))
    average = 0
    for powers, coefficient in polynomial.terms():
        if sum(powers) != degree or any(power % 2 for power in powers):
            continue
        numerator = 1
        for power in powers:
            for odd_number in range(1, power, 2):
                numerator *= odd_number
        average += coefficient * sp.Rational(numerator, denominator)
    return sp.simplify(average)


def block_matrix(
    gravity_gravity: sp.Matrix,
    gravity_photon: sp.Matrix,
    photon_gravity: sp.Matrix,
    photon_photon: sp.Matrix,
) -> sp.Matrix:
    return gravity_gravity.row_join(gravity_photon).col_join(
        photon_gravity.row_join(photon_photon)
    )


def direct_coefficient_formula() -> tuple[sp.Expr, dict[str, sp.Symbol]]:
    spectral_value = sp.Symbol("x", real=True)
    newton, cff = sp.symbols("g g_CFF", positive=True)
    beta_newton = sp.Symbol("beta_g", real=True)
    gamma_g, gamma_s, gamma_a, gamma_df, gamma_ftl = sp.symbols(
        "gamma_g gamma_s gamma_a gamma_df gamma_ftl", real=True
    )
    propagator_gap = 1 - newton / (2 * sp.pi)
    gravity_propagator = 32 * sp.pi * newton / propagator_gap
    inverse_eh = 1 / (32 * sp.pi * newton)
    eta = (beta_newton - 2 * newton) / newton
    regulator_shape = 1 - spectral_value
    gravity_numerator = (
        4 + 4 * gamma_g + gamma_s * spectral_value - 2 * eta
    ) * regulator_shape + 4 * spectral_value
    photon_numerator = 2 * (
        (1 + gamma_a - gamma_df * spectral_value) * regulator_shape
        + spectral_value
    )
    diagonal_kernel = (
        sp.Rational(7, 32) * spectral_value**2
        - sp.Rational(7, 8) * cff * spectral_value**3
    )
    mixed_kernel = (
        sp.Rational(7, 32) * spectral_value**3
        - sp.Rational(7, 8) * cff * spectral_value**4
        + sp.Rational(7, 8) * cff**2 * spectral_value**5
    )
    standard_integrand = (
        gravity_propagator**3
        * inverse_eh
        * gravity_numerator
        * diagonal_kernel
        - gravity_propagator**2
        * (
            gravity_propagator * inverse_eh * gravity_numerator
            + photon_numerator / 2
        )
        * mixed_kernel
    )
    n2_integrand = (
        -sp.Rational(7, 16)
        * gravity_propagator**2
        * inverse_eh
        * regulator_shape
        * gamma_ftl
        * spectral_value**2
    )
    n1_integrand = (
        gravity_propagator**2
        * regulator_shape
        * (gamma_df * inverse_eh + 2 * gamma_ftl)
        * (
            sp.Rational(7, 32) * spectral_value**3
            - sp.Rational(7, 16) * cff * spectral_value**4
        )
    )
    integrated = sp.integrate(
        spectral_value * (standard_integrand + n2_integrand + n1_integrand),
        (spectral_value, 0, 1),
    )
    coefficient = sp.factor(integrated / (2 * 16 * sp.pi**2))
    symbols = {
        "g": newton,
        "g_CFF": cff,
        "beta_g": beta_newton,
        "gamma_g": gamma_g,
        "gamma_s": gamma_s,
        "gamma_a": gamma_a,
        "gamma_df": gamma_df,
        "gamma_ftl": gamma_ftl,
    }
    return coefficient, symbols


def source_cubic_calibration() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    spectral_value, newton, rho = sp.symbols("x g rho", positive=True)
    propagator_gap = 1 - 2 * newton * rho
    gravity_propagator = 32 * sp.pi * newton / propagator_gap
    inverse_eh = 1 / (32 * sp.pi * newton)
    source_numerator = 8 - 4 * spectral_value
    raw = sp.factor(
        -sp.Rational(1, 2)
        * gravity_propagator**4
        * inverse_eh
        * (-sp.Rational(27, 64))
        * sp.integrate(spectral_value**7 * source_numerator, (spectral_value, 0, 1))
        / (16 * sp.pi**2)
    )
    source = 120 * sp.pi * newton**3 / propagator_gap**4
    return raw, source, sp.simplify(source / raw)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes = {path: digest(path) for path in EXPECTED_HASHES}
    failed_hashes = [
        path.as_posix()
        for path, expected_hash in EXPECTED_HASHES.items()
        if source_hashes[path] != expected_hash
    ]
    if failed_hashes:
        raise RuntimeError(f"source hash mismatch: {failed_hashes}")

    dimension = 4
    momentum = sp.symbols("p0:4")
    background_weyl, _ = linear_module.build_generic_weyl()
    substitutions = {
        sp.Symbol("plus_first"): 1,
        sp.Symbol("plus_second"): 2,
        sp.Symbol("minus_first"): 4,
        sp.Symbol("minus_second"): -1,
    }
    background_weyl = background_weyl.applyfunc(lambda value: sp.simplify(value.subs(substitutions)))
    metric_basis = symmetric_basis(dimension)
    dewitt = dewitt_matrix(metric_basis)
    linear_weyls = [linearized_weyl(mode, momentum) for mode in metric_basis]
    c3_matrix = c3_hessian(background_weyl, linear_weyls)
    field_strength = sample_field_strength(dimension)
    invariant_cff = cff_invariant(background_weyl, field_strength)
    maxwell_metric = maxwell_metric_hessian(metric_basis, field_strength)
    maxwell_mixed = maxwell_mixed_hessian(metric_basis, field_strength, momentum)
    cff_metric = cff_metric_hessian(metric_basis, field_strength, momentum)
    cff_mixed = cff_mixed_hessian(linear_weyls, field_strength, momentum)
    metric_trace, metric_tl, photon_trace, photon_tl = metric_rg_kernel_jacobians(
        metric_basis, field_strength, momentum
    )
    photon_metric = photon_rg_metric_jacobian(metric_basis, field_strength, momentum)

    diagonal_polynomial = sp.expand(sp.trace(dewitt * c3_matrix * dewitt * maxwell_metric))
    mixed_polynomial = sp.expand(
        sp.trace(dewitt * c3_matrix * dewitt * maxwell_mixed * maxwell_mixed.T)
    )
    cubic_polynomial = sp.expand(
        sp.trace(dewitt * c3_matrix * dewitt * c3_matrix * dewitt * c3_matrix)
    )
    cff_diagonal_polynomial = sp.expand(
        sp.trace(dewitt * c3_matrix * dewitt * cff_metric)
    )
    cff_mixed_cross_polynomial = sp.expand(
        sp.trace(
            dewitt
            * c3_matrix
            * dewitt
            * (maxwell_mixed * cff_mixed.T + cff_mixed * maxwell_mixed.T)
        )
    )
    cff_mixed_square_polynomial = sp.expand(
        sp.trace(dewitt * c3_matrix * dewitt * cff_mixed * cff_mixed.T)
    )
    diagonal_average = sphere_average(diagonal_polynomial, momentum, 4)
    mixed_average = sphere_average(mixed_polynomial, momentum, 6)
    cubic_average = sphere_average(cubic_polynomial, momentum, 12)
    cff_diagonal_average = sphere_average(cff_diagonal_polynomial, momentum, 6)
    cff_mixed_cross_average = sphere_average(cff_mixed_cross_polynomial, momentum, 8)
    cff_mixed_square_average = sphere_average(cff_mixed_square_polynomial, momentum, 10)
    _, cubic_invariant = linear_module.curvature_invariants(background_weyl)

    trace_symbol, tl_symbol, df_symbol = sp.symbols("gamma_ftrace gamma_ftl gamma_df")
    as_symbol, inverse_eh_symbol, regulator_symbol = sp.symbols(
        "Gg inverse_EH regulator_shape"
    )
    metric_jacobian = trace_symbol * metric_trace + tl_symbol * metric_tl
    photon_jacobian = trace_symbol * photon_trace + tl_symbol * photon_tl
    gravity_metric_jacobian = df_symbol * photon_metric
    gravity_zero = sp.zeros(len(metric_basis))
    photon_zero = sp.zeros(dimension)
    c3_block = block_matrix(c3_matrix, sp.zeros(len(metric_basis), dimension), sp.zeros(dimension, len(metric_basis)), photon_zero)
    mixed_block = block_matrix(
        gravity_zero,
        sp.I * maxwell_mixed,
        -sp.I * maxwell_mixed.T,
        photon_zero,
    )
    cff_mixed_block = block_matrix(
        gravity_zero,
        sp.I * cff_mixed,
        -sp.I * cff_mixed.T,
        photon_zero,
    )
    propagator = block_matrix(
        as_symbol * dewitt,
        sp.zeros(len(metric_basis), dimension),
        sp.zeros(dimension, len(metric_basis)),
        sp.eye(dimension),
    )
    n1_block = block_matrix(
        gravity_zero,
        2 * regulator_symbol * sp.I * photon_jacobian,
        2
        * regulator_symbol
        * inverse_eh_symbol
        * sp.I
        * gravity_metric_jacobian
        * dewitt,
        photon_zero,
    )
    n1_expression = sp.expand(
        sp.Rational(1, 2)
        * sp.trace(
            (
                propagator * c3_block * propagator * mixed_block * propagator
                + propagator * mixed_block * propagator * c3_block * propagator
            )
            * n1_block
        )
    )
    n1_average = sphere_average(n1_expression, momentum, 6)
    n1_cff_expression = sp.expand(
        sp.Rational(1, 2)
        * sp.trace(
            (
                propagator * c3_block * propagator * cff_mixed_block * propagator
                + propagator * cff_mixed_block * propagator * c3_block * propagator
            )
            * n1_block
        )
    )
    n1_cff_average = sphere_average(n1_cff_expression, momentum, 8)
    n2_averages: dict[str, sp.Expr] = {}
    for name, jacobian in (("trace", metric_trace), ("tl", metric_tl)):
        n2_matrix = 2 * regulator_symbol * inverse_eh_symbol * jacobian * dewitt
        n2_expression = -sp.Rational(1, 2) * sp.trace(
            as_symbol * dewitt * c3_matrix * as_symbol * dewitt * n2_matrix
        )
        n2_averages[name] = sphere_average(sp.expand(n2_expression), momentum, 4)

    ratios = {
        "diagonal_Maxwell": sp.simplify(diagonal_average / invariant_cff),
        "mixed_Maxwell": sp.simplify(mixed_average / invariant_cff),
        "c3_cubic": sp.simplify(cubic_average / cubic_invariant),
        "CFF_diagonal": sp.simplify(cff_diagonal_average / invariant_cff),
        "CFF_mixed_cross": sp.simplify(cff_mixed_cross_average / invariant_cff),
        "CFF_mixed_square": sp.simplify(cff_mixed_square_average / invariant_cff),
        "n2_trace": sp.simplify(n2_averages["trace"] / invariant_cff),
        "n2_tl": sp.simplify(n2_averages["tl"] / invariant_cff),
        "n1": sp.simplify(n1_average / invariant_cff),
        "n1_CFF": sp.simplify(n1_cff_average / invariant_cff),
    }
    coefficient_formula, coefficient_symbols = direct_coefficient_formula()
    raw_cubic, source_cubic, polarization_calibration = source_cubic_calibration()
    combined_values = {
        coefficient_symbols["g"]: 0.13056045261536448,
        coefficient_symbols["g_CFF"]: 0.003729942575813481,
        coefficient_symbols["beta_g"]: 0.0,
        coefficient_symbols["gamma_g"]: -1.6778714945723168,
        coefficient_symbols["gamma_s"]: -0.006235559035968446,
        coefficient_symbols["gamma_a"]: 0.04101920752494062,
        coefficient_symbols["gamma_df"]: -0.005379640817968146,
        coefficient_symbols["gamma_ftl"]: 0.1359035335847571,
    }
    numeric_direct_coefficient = float(coefficient_formula.subs(combined_values))
    h_value = 4.273038337287102e-6
    numeric_direct_projection = numeric_direct_coefficient * h_value
    checks = {
        "dewitt_involution": dewitt * dewitt == sp.eye(len(metric_basis)),
        "Maxwell_diagonal_ratio": ratios["diagonal_Maxwell"] == sp.Rational(7, 32),
        "Maxwell_mixed_ratio": ratios["mixed_Maxwell"] == sp.Rational(7, 32),
        "CFF_diagonal_ratio": ratios["CFF_diagonal"] == -sp.Rational(7, 8),
        "CFF_mixed_cross_ratio": ratios["CFF_mixed_cross"] == -sp.Rational(7, 8),
        "CFF_mixed_square_ratio": ratios["CFF_mixed_square"] == sp.Rational(7, 8),
        "C3_source_calibration": polarization_calibration == sp.Rational(1, 2),
        "trace_RG_kernel_zero": ratios["n2_trace"] == 0,
        "numeric_projection_finite": math.isfinite(numeric_direct_projection),
    }
    if not all(checks.values()):
        raise RuntimeError(f"direct C3 to CFF derivation failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): source_hashes[path]
            for path in EXPECTED_HASHES
        },
        "sample_invariants": {
            "CFF": str(invariant_cff),
            "C3": str(cubic_invariant),
        },
        "angular_ratios": {name: str(value) for name, value in ratios.items()},
        "source_cubic_calibration": {
            "raw_c3_cubic_angular_ratio": str(ratios["c3_cubic"]),
            "raw_h_cubed_RHS_coefficient": str(raw_cubic),
            "source_h_cubed_RHS_coefficient": str(source_cubic),
            "source_trace_polarization_calibration": str(polarization_calibration),
        },
        "direct_coefficient": {
            "formula": str(coefficient_formula),
            "definition": "Delta RHS_CFF|direct C3 = h_C3 * direct_coefficient",
            "coefficient_at_4933_partial_point": numeric_direct_coefficient,
            "projection_at_4933_partial_point": numeric_direct_projection,
            "includes": [
                "Maxwell metric and mixed Hessians",
                "CFF metric and mixed Hessians through g_CFF squared",
                "gamma_F2_TL metric RG-kernel block",
                "gamma_DF and gamma_F2_TL mixed RG-kernel blocks",
                "source Litim radial moments",
                "source 1/2 graviton polarization calibration",
            ],
        },
        "checks": checks,
        "claim_boundary": {
            "standard_hessian_blocks_derived": True,
            "rg_kernel_F_dependent_blocks_derived": True,
            "CFF_portal_hessian_correction_derived": True,
            "full_direct_C3_to_CFF_coefficient_derived": True,
            "full_combined_fixed_point_claimed": False,
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_DIAGONAL_RATIO={ratios['diagonal_Maxwell']}", flush=True)
    print(f"{MARKER}_MIXED_RATIO={ratios['mixed_Maxwell']}", flush=True)
    print(f"{MARKER}_CUBIC_RATIO={ratios['c3_cubic']}", flush=True)
    print(f"{MARKER}_CFF_DIAGONAL_RATIO={ratios['CFF_diagonal']}", flush=True)
    print(f"{MARKER}_CFF_MIXED_CROSS_RATIO={ratios['CFF_mixed_cross']}", flush=True)
    print(f"{MARKER}_CFF_MIXED_SQUARE_RATIO={ratios['CFF_mixed_square']}", flush=True)
    print(f"{MARKER}_N2_TL_RATIO={ratios['n2_tl']}", flush=True)
    print(f"{MARKER}_N1_RATIO={ratios['n1']}", flush=True)
    print(f"{MARKER}_N1_CFF_RATIO={ratios['n1_CFF']}", flush=True)
    print(f"{MARKER}_DIRECT_COEFFICIENT={numeric_direct_coefficient:.16g}", flush=True)
    print(f"{MARKER}_DIRECT_PROJECTION={numeric_direct_projection:.16g}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


linear_module = load_linear_module()


if __name__ == "__main__":
    raise SystemExit(main())
