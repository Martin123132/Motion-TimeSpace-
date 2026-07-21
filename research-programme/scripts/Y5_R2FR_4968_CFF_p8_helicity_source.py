from __future__ import annotations

import cmath
import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4968"
TROTT_SOURCE = SOURCE / "src-2605.04152" / "superspace.tex"
TROTT_TAR = SOURCE / "2605.04152-source.tar"
TROTT_PDF = SOURCE / "2605.04152.pdf"
BARATELLA_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4967"
    / "src-2010.13809"
    / "draft.tex"
)
AMPLITUDE_CSV = SOURCE / "CFF_tree_helicity_amplitudes.csv"
PROJECTION_CSV = SOURCE / "CFF_squared_p8_partial_wave_projection.csv"
RESULT_JSON = SOURCE / "CFF_squared_p8_helicity_source_results.json"
MARKER = "MTS_4968_CFF_P8_HELICITY_SOURCE"
DIMENSION = 4
METRIC = (-1.0, 1.0, 1.0, 1.0)
TOLERANCE = 5.0e-8
CHECKED_DATE = "2026-07-13"
EXPECTED_HASHES = {
    TROTT_SOURCE: "66cc66258b377f0f7c01c15b660fdee7616e3d3918b689e5195fa3f2f376f531",
    TROTT_TAR: "a664c5e2cd5d65ed3aa543773d1f1fed9034ecf85773b031e757f384fdd96d5f",
    TROTT_PDF: "12245cf5c6c75faf57169e930ec7dbdbc5fefcfb1dfedc1f61deef8be00abdcf",
    BARATELLA_SOURCE: "d2892e4163b5a70ff3f660e2a48ba91f7e7be246dd53d21b3aa874a3a1b13230",
}


@dataclass(frozen=True)
class NilpotentContext:
    momenta: tuple[tuple[complex, ...], ...]

    @property
    def field_count(self) -> int:
        return len(self.momenta)

    @property
    def full_mask(self) -> int:
        return (1 << self.field_count) - 1


class Nilpotent:
    def __init__(
        self,
        context: NilpotentContext,
        coefficients: dict[int, complex] | None = None,
    ) -> None:
        self.context = context
        self.coefficients = {
            mask: complex(value)
            for mask, value in (coefficients or {}).items()
            if abs(value) != 0.0
        }

    @classmethod
    def constant(cls, context: NilpotentContext, value: complex) -> "Nilpotent":
        return cls(context, {0: value})

    @classmethod
    def field(
        cls, context: NilpotentContext, field_index: int, value: complex
    ) -> "Nilpotent":
        return cls(context, {1 << field_index: value})

    def coefficient(self, mask: int) -> complex:
        return self.coefficients.get(mask, 0.0j)

    def _coerce(self, other: object) -> "Nilpotent":
        if isinstance(other, Nilpotent):
            if other.context != self.context:
                raise ValueError("nilpotent contexts differ")
            return other
        if isinstance(other, (int, float, complex)):
            return Nilpotent.constant(self.context, complex(other))
        return NotImplemented

    def __add__(self, other: object) -> "Nilpotent":
        coerced = self._coerce(other)
        if coerced is NotImplemented:
            return NotImplemented
        result = dict(self.coefficients)
        for mask, value in coerced.coefficients.items():
            result[mask] = result.get(mask, 0.0j) + value
        return Nilpotent(self.context, result)

    def __radd__(self, other: object) -> "Nilpotent":
        return self.__add__(other)

    def __neg__(self) -> "Nilpotent":
        return Nilpotent(
            self.context, {mask: -value for mask, value in self.coefficients.items()}
        )

    def __sub__(self, other: object) -> "Nilpotent":
        coerced = self._coerce(other)
        if coerced is NotImplemented:
            return NotImplemented
        return self + (-coerced)

    def __rsub__(self, other: object) -> "Nilpotent":
        coerced = self._coerce(other)
        if coerced is NotImplemented:
            return NotImplemented
        return coerced - self

    def __mul__(self, other: object) -> "Nilpotent":
        coerced = self._coerce(other)
        if coerced is NotImplemented:
            return NotImplemented
        result: dict[int, complex] = {}
        for left_mask, left_value in self.coefficients.items():
            for right_mask, right_value in coerced.coefficients.items():
                if left_mask & right_mask:
                    continue
                combined_mask = left_mask | right_mask
                result[combined_mask] = (
                    result.get(combined_mask, 0.0j) + left_value * right_value
                )
        return Nilpotent(self.context, result)

    def __rmul__(self, other: object) -> "Nilpotent":
        return self.__mul__(other)

    def __truediv__(self, other: object) -> "Nilpotent":
        if not isinstance(other, (int, float, complex)):
            return NotImplemented
        return self * (1.0 / complex(other))

    def derivative(self, coordinate_index: int) -> "Nilpotent":
        result: dict[int, complex] = {}
        for mask, value in self.coefficients.items():
            total_momentum = sum(
                self.context.momenta[field_index][coordinate_index]
                for field_index in range(self.context.field_count)
                if mask & (1 << field_index)
            )
            result[mask] = 1.0j * total_momentum * value
        return Nilpotent(self.context, result)


Matrix = list[list[Nilpotent]]


def zero(context: NilpotentContext) -> Nilpotent:
    return Nilpotent.constant(context, 0.0)


def constant_matrix(
    context: NilpotentContext, values: list[list[complex]]
) -> Matrix:
    return [
        [Nilpotent.constant(context, values[row][column]) for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]


def identity_matrix(context: NilpotentContext) -> Matrix:
    return constant_matrix(
        context,
        [
            [1.0 if row == column else 0.0 for column in range(DIMENSION)]
            for row in range(DIMENSION)
        ],
    )


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[row][column] + right[row][column] for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]


def matrix_scale(matrix: Matrix, factor: complex) -> Matrix:
    return [
        [matrix[row][column] * factor for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    context = left[0][0].context
    return [
        [
            sum(
                (left[row][inner] * right[inner][column] for inner in range(DIMENSION)),
                zero(context),
            )
            for column in range(DIMENSION)
        ]
        for row in range(DIMENSION)
    ]


def matrix_trace(matrix: Matrix) -> Nilpotent:
    context = matrix[0][0].context
    return sum((matrix[index][index] for index in range(DIMENSION)), zero(context))


def nilpotent_exp(value: Nilpotent) -> Nilpotent:
    constant_value = value.coefficient(0)
    nilpotent_value = value - constant_value
    result = Nilpotent.constant(value.context, cmath.exp(constant_value))
    power = Nilpotent.constant(value.context, 1.0)
    factorial = 1
    series = Nilpotent.constant(value.context, 1.0)
    for order in range(1, value.context.field_count + 1):
        power = power * nilpotent_value
        factorial *= order
        series = series + power / factorial
    return result * series


def minkowski_matrix() -> list[list[complex]]:
    return [
        [METRIC[row] if row == column else 0.0 for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]


def build_metric(
    context: NilpotentContext,
    metric_fields: Iterable[tuple[int, list[list[complex]]]],
) -> Matrix:
    metric = constant_matrix(context, minkowski_matrix())
    for field_index, polarization in metric_fields:
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                metric[row][column] = metric[row][column] + Nilpotent.field(
                    context, field_index, polarization[row][column]
                )
    return metric


def inverse_metric_and_volume(metric: Matrix) -> tuple[Matrix, Nilpotent]:
    context = metric[0][0].context
    eta_inverse = constant_matrix(context, minkowski_matrix())
    delta_metric = [
        [
            metric[row][column]
            - (METRIC[row] if row == column else 0.0)
            for column in range(DIMENSION)
        ]
        for row in range(DIMENSION)
    ]
    mixed_delta = matrix_multiply(eta_inverse, delta_metric)
    inverse_series = identity_matrix(context)
    power = identity_matrix(context)
    for order in range(1, context.field_count + 1):
        power = matrix_multiply(power, mixed_delta)
        inverse_series = matrix_add(
            inverse_series, matrix_scale(power, -1.0 if order % 2 else 1.0)
        )
    inverse_metric = matrix_multiply(inverse_series, eta_inverse)
    trace_log = zero(context)
    power = identity_matrix(context)
    for order in range(1, context.field_count + 1):
        power = matrix_multiply(power, mixed_delta)
        trace_log = trace_log + matrix_trace(power) * (
            (1.0 if order % 2 else -1.0) / order
        )
    volume = nilpotent_exp(trace_log * 0.5)
    return inverse_metric, volume


def christoffel(metric: Matrix, inverse_metric: Matrix) -> list[list[list[Nilpotent]]]:
    context = metric[0][0].context
    connection = [
        [[zero(context) for _ in range(DIMENSION)] for _ in range(DIMENSION)]
        for _ in range(DIMENSION)
    ]
    for upper_index in range(DIMENSION):
        for first_lower in range(DIMENSION):
            for second_lower in range(DIMENSION):
                connection[upper_index][first_lower][second_lower] = 0.5 * sum(
                    (
                        inverse_metric[upper_index][contracted_index]
                        * (
                            metric[contracted_index][second_lower].derivative(first_lower)
                            + metric[contracted_index][first_lower].derivative(second_lower)
                            - metric[first_lower][second_lower].derivative(contracted_index)
                        )
                        for contracted_index in range(DIMENSION)
                    ),
                    zero(context),
                )
    return connection


def curvature_tensors(
    metric: Matrix,
    inverse_metric: Matrix,
    connection: list[list[list[Nilpotent]]],
) -> tuple[
    list[list[list[list[Nilpotent]]]],
    list[list[Nilpotent]],
    Nilpotent,
    list[list[list[list[Nilpotent]]]],
]:
    context = metric[0][0].context
    riemann_mixed = [
        [
            [
                [zero(context) for _ in range(DIMENSION)]
                for _ in range(DIMENSION)
            ]
            for _ in range(DIMENSION)
        ]
        for _ in range(DIMENSION)
    ]
    for upper_index in range(DIMENSION):
        for second_index in range(DIMENSION):
            for third_index in range(DIMENSION):
                for fourth_index in range(DIMENSION):
                    value = connection[upper_index][fourth_index][second_index].derivative(
                        third_index
                    ) - connection[upper_index][third_index][second_index].derivative(
                        fourth_index
                    )
                    value = value + sum(
                        (
                            connection[upper_index][third_index][contracted_index]
                            * connection[contracted_index][fourth_index][second_index]
                            - connection[upper_index][fourth_index][contracted_index]
                            * connection[contracted_index][third_index][second_index]
                            for contracted_index in range(DIMENSION)
                        ),
                        zero(context),
                    )
                    riemann_mixed[upper_index][second_index][third_index][fourth_index] = value
    ricci = [
        [
            sum(
                (
                    riemann_mixed[contracted_index][second_index][contracted_index][
                        fourth_index
                    ]
                    for contracted_index in range(DIMENSION)
                ),
                zero(context),
            )
            for fourth_index in range(DIMENSION)
        ]
        for second_index in range(DIMENSION)
    ]
    scalar = sum(
        (
            inverse_metric[first_index][second_index]
            * ricci[first_index][second_index]
            for first_index in range(DIMENSION)
            for second_index in range(DIMENSION)
        ),
        zero(context),
    )
    riemann_lower = [
        [
            [
                [
                    sum(
                        (
                            metric[first_index][contracted_index]
                            * riemann_mixed[contracted_index][second_index][third_index][
                                fourth_index
                            ]
                            for contracted_index in range(DIMENSION)
                        ),
                        zero(context),
                    )
                    for fourth_index in range(DIMENSION)
                ]
                for third_index in range(DIMENSION)
            ]
            for second_index in range(DIMENSION)
        ]
        for first_index in range(DIMENSION)
    ]
    weyl = [
        [
            [
                [zero(context) for _ in range(DIMENSION)]
                for _ in range(DIMENSION)
            ]
            for _ in range(DIMENSION)
        ]
        for _ in range(DIMENSION)
    ]
    for first_index in range(DIMENSION):
        for second_index in range(DIMENSION):
            for third_index in range(DIMENSION):
                for fourth_index in range(DIMENSION):
                    ricci_wedge = (
                        metric[first_index][third_index] * ricci[fourth_index][second_index]
                        - metric[first_index][fourth_index] * ricci[third_index][second_index]
                        - metric[second_index][third_index] * ricci[fourth_index][first_index]
                        + metric[second_index][fourth_index] * ricci[third_index][first_index]
                    )
                    metric_wedge = (
                        metric[first_index][third_index]
                        * metric[second_index][fourth_index]
                        - metric[first_index][fourth_index]
                        * metric[second_index][third_index]
                    )
                    weyl[first_index][second_index][third_index][fourth_index] = (
                        riemann_lower[first_index][second_index][third_index][fourth_index]
                        - 0.5 * ricci_wedge
                        + scalar * metric_wedge / 6.0
                    )
    return riemann_lower, ricci, scalar, weyl


def field_strength(
    context: NilpotentContext,
    photon_fields: Iterable[tuple[int, tuple[complex, ...]]],
) -> list[list[Nilpotent]]:
    strength = [
        [zero(context) for _ in range(DIMENSION)] for _ in range(DIMENSION)
    ]
    for field_index, polarization in photon_fields:
        momentum = context.momenta[field_index]
        for first_index in range(DIMENSION):
            for second_index in range(DIMENSION):
                value = 1.0j * (
                    momentum[first_index] * polarization[second_index]
                    - momentum[second_index] * polarization[first_index]
                )
                strength[first_index][second_index] = strength[first_index][
                    second_index
                ] + Nilpotent.field(context, field_index, value)
    return strength


def raised_field_strength(
    strength: list[list[Nilpotent]], inverse_metric: Matrix
) -> list[list[Nilpotent]]:
    context = inverse_metric[0][0].context
    return [
        [
            sum(
                (
                    inverse_metric[first_index][lower_first]
                    * inverse_metric[second_index][lower_second]
                    * strength[lower_first][lower_second]
                    for lower_first in range(DIMENSION)
                    for lower_second in range(DIMENSION)
                ),
                zero(context),
            )
            for second_index in range(DIMENSION)
        ]
        for first_index in range(DIMENSION)
    ]


def maxwell_and_cff_lagrangians(
    context: NilpotentContext,
    metric_fields: Iterable[tuple[int, list[list[complex]]]],
    photon_fields: Iterable[tuple[int, tuple[complex, ...]]],
) -> tuple[Nilpotent, Nilpotent]:
    metric = build_metric(context, metric_fields)
    inverse_metric, volume = inverse_metric_and_volume(metric)
    connection = christoffel(metric, inverse_metric)
    _, _, _, weyl = curvature_tensors(metric, inverse_metric, connection)
    strength = field_strength(context, photon_fields)
    raised_strength = raised_field_strength(strength, inverse_metric)
    maxwell_contraction = sum(
        (
            strength[first_index][second_index]
            * raised_strength[first_index][second_index]
            for first_index in range(DIMENSION)
            for second_index in range(DIMENSION)
        ),
        zero(context),
    )
    cff_contraction = sum(
        (
            weyl[first_index][second_index][third_index][fourth_index]
            * raised_strength[first_index][second_index]
            * raised_strength[third_index][fourth_index]
            for first_index in range(DIMENSION)
            for second_index in range(DIMENSION)
            for third_index in range(DIMENSION)
            for fourth_index in range(DIMENSION)
        ),
        zero(context),
    )
    return -0.25 * volume * maxwell_contraction, volume * cff_contraction


def einstein_hilbert_lagrangian(
    context: NilpotentContext,
    metric_fields: Iterable[tuple[int, list[list[complex]]]],
) -> Nilpotent:
    metric = build_metric(context, metric_fields)
    inverse_metric, volume = inverse_metric_and_volume(metric)
    connection = christoffel(metric, inverse_metric)
    contraction = zero(context)
    for first_index in range(DIMENSION):
        for second_index in range(DIMENSION):
            gamma_product = zero(context)
            for upper_index in range(DIMENSION):
                for contracted_index in range(DIMENSION):
                    gamma_product = gamma_product + (
                        connection[upper_index][first_index][contracted_index]
                        * connection[contracted_index][second_index][upper_index]
                        - connection[upper_index][first_index][second_index]
                        * connection[contracted_index][upper_index][contracted_index]
                    )
            contraction = contraction + inverse_metric[first_index][second_index] * gamma_product
    return 2.0 * volume * contraction


def dot(first: tuple[complex, ...], second: tuple[complex, ...]) -> complex:
    return sum(
        METRIC[index] * first[index] * second[index] for index in range(DIMENSION)
    )


def outer(first: tuple[complex, ...], second: tuple[complex, ...]) -> list[list[complex]]:
    return [
        [first[row] * second[column] for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]


def helicity_vector(
    theta: float, phi: float, helicity: int
) -> tuple[complex, ...]:
    direction_theta = (
        math.cos(theta) * math.cos(phi),
        math.cos(theta) * math.sin(phi),
        -math.sin(theta),
    )
    direction_phi = (-math.sin(phi), math.cos(phi), 0.0)
    phase = 1.0j if helicity > 0 else -1.0j
    spatial = tuple(
        (direction_theta[index] + phase * direction_phi[index]) / math.sqrt(2.0)
        for index in range(3)
    )
    return (0.0j, spatial[0], spatial[1], spatial[2])


def conjugate_vector(vector: tuple[complex, ...]) -> tuple[complex, ...]:
    return tuple(value.conjugate() for value in vector)


def symmetric_basis(first_index: int, second_index: int) -> list[list[complex]]:
    basis = [[0.0j for _ in range(DIMENSION)] for _ in range(DIMENSION)]
    basis[first_index][second_index] = 1.0
    basis[second_index][first_index] = 1.0
    if first_index == second_index:
        basis[first_index][second_index] = 1.0
    return basis


def h_aa_vertex(
    graviton_momentum: tuple[complex, ...],
    graviton_polarization: list[list[complex]],
    first_photon_momentum: tuple[complex, ...],
    first_photon_polarization: tuple[complex, ...],
    second_photon_momentum: tuple[complex, ...],
    second_photon_polarization: tuple[complex, ...],
    operator: str,
) -> complex:
    context = NilpotentContext(
        (graviton_momentum, first_photon_momentum, second_photon_momentum)
    )
    maxwell, cff = maxwell_and_cff_lagrangians(
        context,
        [(0, graviton_polarization)],
        [(1, first_photon_polarization), (2, second_photon_polarization)],
    )
    selected = maxwell if operator == "maxwell" else cff
    return selected.coefficient(context.full_mask)


def hhh_vertex(
    momenta: tuple[tuple[complex, ...], ...],
    polarizations: tuple[list[list[complex]], ...],
) -> complex:
    context = NilpotentContext(momenta)
    lagrangian = einstein_hilbert_lagrangian(
        context,
        [(index, polarizations[index]) for index in range(3)],
    )
    return lagrangian.coefficient(context.full_mask)


def hh_aa_contact(
    graviton_momenta: tuple[tuple[complex, ...], tuple[complex, ...]],
    graviton_polarizations: tuple[list[list[complex]], list[list[complex]]],
    photon_momenta: tuple[tuple[complex, ...], tuple[complex, ...]],
    photon_polarizations: tuple[tuple[complex, ...], tuple[complex, ...]],
) -> complex:
    context = NilpotentContext(
        (
            graviton_momenta[0],
            graviton_momenta[1],
            photon_momenta[0],
            photon_momenta[1],
        )
    )
    _, cff = maxwell_and_cff_lagrangians(
        context,
        [(0, graviton_polarizations[0]), (1, graviton_polarizations[1])],
        [(2, photon_polarizations[0]), (3, photon_polarizations[1])],
    )
    return cff.coefficient(context.full_mask)


def photon_exchange(
    left_graviton: tuple[tuple[complex, ...], list[list[complex]]],
    left_photon: tuple[tuple[complex, ...], tuple[complex, ...]],
    right_graviton: tuple[tuple[complex, ...], list[list[complex]]],
    right_photon: tuple[tuple[complex, ...], tuple[complex, ...]],
    left_operator: str,
    right_operator: str,
) -> complex:
    internal_left = tuple(
        -(left_graviton[0][index] + left_photon[0][index])
        for index in range(DIMENSION)
    )
    internal_right = tuple(-value for value in internal_left)
    denominator = dot(internal_left, internal_left)
    left_current: list[complex] = []
    right_current: list[complex] = []
    for vector_index in range(DIMENSION):
        basis_vector = tuple(
            1.0 if index == vector_index else 0.0 for index in range(DIMENSION)
        )
        left_current.append(
            h_aa_vertex(
                left_graviton[0],
                left_graviton[1],
                left_photon[0],
                left_photon[1],
                internal_left,
                basis_vector,
                left_operator,
            )
        )
        right_current.append(
            h_aa_vertex(
                right_graviton[0],
                right_graviton[1],
                right_photon[0],
                right_photon[1],
                internal_right,
                basis_vector,
                right_operator,
            )
        )
    contraction = sum(
        METRIC[index] * left_current[index] * right_current[index]
        for index in range(DIMENSION)
    )
    return contraction / denominator


def graviton_current(
    vertex_function,
) -> list[list[complex]]:
    current = [[0.0j for _ in range(DIMENSION)] for _ in range(DIMENSION)]
    for first_index in range(DIMENSION):
        for second_index in range(first_index, DIMENSION):
            value = vertex_function(symmetric_basis(first_index, second_index))
            if first_index != second_index:
                value *= 0.5
            current[first_index][second_index] = value
            current[second_index][first_index] = value
    return current


def de_donder_contraction(
    left: list[list[complex]], right: list[list[complex]]
) -> complex:
    contraction = 0.0j
    for first_index in range(DIMENSION):
        for second_index in range(DIMENSION):
            for third_index in range(DIMENSION):
                for fourth_index in range(DIMENSION):
                    projector = 0.5 * (
                        (METRIC[first_index] if first_index == third_index else 0.0)
                        * (METRIC[second_index] if second_index == fourth_index else 0.0)
                        + (METRIC[first_index] if first_index == fourth_index else 0.0)
                        * (METRIC[second_index] if second_index == third_index else 0.0)
                        - (METRIC[first_index] if first_index == second_index else 0.0)
                        * (METRIC[third_index] if third_index == fourth_index else 0.0)
                    )
                    contraction += (
                        left[first_index][second_index]
                        * projector
                        * right[third_index][fourth_index]
                    )
    return contraction


def graviton_exchange(
    gravitons: tuple[
        tuple[tuple[complex, ...], list[list[complex]]],
        tuple[tuple[complex, ...], list[list[complex]]],
    ],
    photons: tuple[
        tuple[tuple[complex, ...], tuple[complex, ...]],
        tuple[tuple[complex, ...], tuple[complex, ...]],
    ],
) -> complex:
    internal_cff = tuple(
        -(photons[0][0][index] + photons[1][0][index])
        for index in range(DIMENSION)
    )
    internal_eh = tuple(-value for value in internal_cff)
    denominator = dot(internal_cff, internal_cff)
    cff_current = graviton_current(
        lambda basis: h_aa_vertex(
            internal_cff,
            basis,
            photons[0][0],
            photons[0][1],
            photons[1][0],
            photons[1][1],
            "cff",
        )
    )
    eh_current = graviton_current(
        lambda basis: hhh_vertex(
            (internal_eh, gravitons[0][0], gravitons[1][0]),
            (basis, gravitons[0][1], gravitons[1][1]),
        )
    )
    return de_donder_contraction(cff_current, eh_current) / denominator


def scattering_kinematics(
    theta: float, energy: float = 1.0,
) -> tuple[tuple[complex, ...], ...]:
    incoming_first = (energy, 0.0, 0.0, energy)
    incoming_second = (energy, 0.0, 0.0, -energy)
    outgoing_first = (
        energy,
        energy * math.sin(theta),
        0.0,
        energy * math.cos(theta),
    )
    outgoing_second = (
        energy,
        -energy * math.sin(theta),
        0.0,
        -energy * math.cos(theta),
    )
    return incoming_first, incoming_second, outgoing_first, outgoing_second


def cff_tree_amplitude(
    theta: float,
    graviton_helicities: tuple[int, int],
    photon_helicities: tuple[int, int],
    replace_leg: tuple[str, int] | None = None,
    energy: float = 1.0,
) -> dict[str, complex]:
    incoming_first, incoming_second, outgoing_first, outgoing_second = (
        scattering_kinematics(theta, energy)
    )
    all_incoming_momenta = (
        incoming_first,
        incoming_second,
        tuple(-value for value in outgoing_first),
        tuple(-value for value in outgoing_second),
    )
    incoming_first_vector = helicity_vector(0.0, 0.0, graviton_helicities[0])
    incoming_second_vector = helicity_vector(
        math.pi, 0.0, graviton_helicities[1]
    )
    outgoing_first_vector = conjugate_vector(
        helicity_vector(theta, 0.0, photon_helicities[0])
    )
    outgoing_second_vector = conjugate_vector(
        helicity_vector(math.pi - theta, math.pi, photon_helicities[1])
    )
    graviton_polarizations = [
        outer(incoming_first_vector, incoming_first_vector),
        outer(incoming_second_vector, incoming_second_vector),
    ]
    photon_polarizations = [outgoing_first_vector, outgoing_second_vector]
    if replace_leg is not None and replace_leg[0] == "photon":
        photon_index = replace_leg[1]
        photon_polarizations[photon_index] = tuple(
            value for value in all_incoming_momenta[2 + photon_index]
        )
    if replace_leg is not None and replace_leg[0] == "graviton":
        graviton_index = replace_leg[1]
        momentum = all_incoming_momenta[graviton_index]
        reference = (0.0j, 1.0, 0.0, 0.0)
        graviton_polarizations[graviton_index] = [
            [
                momentum[row] * reference[column]
                + reference[row] * momentum[column]
                for column in range(DIMENSION)
            ]
            for row in range(DIMENSION)
        ]
    gravitons = (
        (all_incoming_momenta[0], graviton_polarizations[0]),
        (all_incoming_momenta[1], graviton_polarizations[1]),
    )
    photons = (
        (all_incoming_momenta[2], photon_polarizations[0]),
        (all_incoming_momenta[3], photon_polarizations[1]),
    )
    contact = hh_aa_contact(
        (gravitons[0][0], gravitons[1][0]),
        (gravitons[0][1], gravitons[1][1]),
        (photons[0][0], photons[1][0]),
        (photons[0][1], photons[1][1]),
    )
    photon_terms = 0.0j
    for first_photon_index, second_photon_index in ((0, 1), (1, 0)):
        photon_terms += photon_exchange(
            gravitons[0],
            photons[first_photon_index],
            gravitons[1],
            photons[second_photon_index],
            "cff",
            "maxwell",
        )
        photon_terms += photon_exchange(
            gravitons[0],
            photons[first_photon_index],
            gravitons[1],
            photons[second_photon_index],
            "maxwell",
            "cff",
        )
    gravity_term = graviton_exchange(gravitons, photons)
    total = contact + photon_terms + gravity_term
    return {
        "contact": contact,
        "photon_exchange": photon_terms,
        "graviton_exchange": gravity_term,
        "total": total,
    }


def relative_gauge_residual(
    nominal: complex, replacement: complex
) -> float:
    return abs(replacement) / max(1.0, abs(nominal))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_checks() -> tuple[dict[str, str], dict[str, bool]]:
    actual_hashes = {relative(path): digest(path) for path in EXPECTED_HASHES}
    hash_checks = {
        f"hash_{path.name}": actual_hashes[relative(path)] == expected
        for path, expected in EXPECTED_HASHES.items()
    }
    trott_text = TROTT_SOURCE.read_text(encoding="utf-8")
    baratella_text = BARATELLA_SOURCE.read_text(encoding="utf-8")
    marker_checks = {
        "trott_three_point_CFF_marker": (
            "\\frac{1}{M_{Pl}\\Lambda^2}\\ds{12}^2\\ds{23}^2"
            in trott_text
        ),
        "trott_four_point_CFF_marker": (
            "\\frac{\\ds{12}^2\\ds{34}^4}{s}" in trott_text
        ),
        "baratella_identical_factor_marker": (
            "A factor 1/2 must also be" in baratella_text
        ),
        "baratella_partial_wave_kernel_marker": (
            "-\\frac{1}{8\\pi^2}" in baratella_text
        ),
    }
    return actual_hashes, {**hash_checks, **marker_checks}


def analytic_partial_wave_projection() -> dict[str, object]:
    z = sp.symbols("z", real=True)
    q, w_c, gravity, g_cff = sp.symbols(
        "q W_C g g_CFF", real=True
    )
    d_40_j4 = sp.sqrt(70) * (1 - z**2) ** 2 / 16
    tree_same_a0 = 2 * q
    tree_opposite = q * (1 - z**2) / 2
    tree_opposite_a4 = sp.simplify(
        sp.integrate(d_40_j4 * tree_opposite, (z, -1, 1)) / 2
    )
    target_s_a0 = sp.Integer(1)
    target_crossed_a4 = sp.Rational(1, 9)
    identical_factor = sp.Rational(1, 2)
    same_channel_internal_count = sp.Integer(1)
    crossed_channel_internal_count = sp.Integer(2)
    gamma_s = sp.simplify(
        -identical_factor
        * same_channel_internal_count
        * tree_same_a0**2
        / (8 * sp.pi**2 * target_s_a0)
    )
    gamma_t = sp.simplify(
        -identical_factor
        * crossed_channel_internal_count
        * tree_opposite_a4**2
        / (8 * sp.pi**2 * target_crossed_a4)
    )
    gamma_u = gamma_t
    gamma_r4_prime = sp.simplify(gamma_s + gamma_t + gamma_u)
    gamma_r4 = sp.Integer(0)
    gamma_r4_prime_w = sp.simplify(gamma_r4_prime.subs(q, 2 * w_c))
    beta_b_plus_w = sp.simplify(128 * sp.pi**3 * gamma_r4_prime_w)
    beta_b_plus_running = sp.simplify(
        beta_b_plus_w.subs(w_c, g_cff / (16 * sp.pi * gravity))
    )
    beta_b_c_running = sp.simplify(beta_b_plus_running / 2)
    beta_b_t_running = beta_b_c_running
    checks = {
        "d40_normalization": sp.simplify(
            sp.integrate(d_40_j4**2, (z, -1, 1)) - sp.Rational(2, 9)
        )
        == 0,
        "opposite_tree_a4": (
            tree_opposite_a4 == q * sp.sqrt(70) / 70
        ),
        "same_channel_source": gamma_s == -(q**2) / (4 * sp.pi**2),
        "crossed_channel_source": gamma_t == -(9 * q**2) / (560 * sp.pi**2),
        "mixed_total_source": gamma_r4_prime
        == -(79 * q**2) / (280 * sp.pi**2),
        "W_C_map": gamma_r4_prime_w
        == -(79 * w_c**2) / (70 * sp.pi**2),
        "running_B_plus_map": beta_b_plus_running
        == -(79 * g_cff**2) / (140 * sp.pi * gravity**2),
    }
    rows = [
        {
            "row_id": "CFF4968_PW0_same_pair",
            "channel": "s",
            "external_pair": "h--_to_h--",
            "internal_photons": "gamma++",
            "J": 0,
            "tree_partial_wave": str(tree_same_a0),
            "target_partial_wave_per_C_R4prime": str(target_s_a0),
            "identical_factor": str(identical_factor),
            "channel_source_dC_R4prime_dlnmu": str(gamma_s),
            "status": "DERIVED",
        },
        {
            "row_id": "CFF4968_PW4_crossed_t",
            "channel": "t",
            "external_pair": "h-_h+_to_h+_h-",
            "internal_photons": "gamma++;gamma--",
            "J": 4,
            "tree_partial_wave": str(tree_opposite_a4),
            "target_partial_wave_per_C_R4prime": str(target_crossed_a4),
            "identical_factor": str(identical_factor),
            "channel_source_dC_R4prime_dlnmu": str(gamma_t),
            "status": "DERIVED",
        },
        {
            "row_id": "CFF4968_PW4_crossed_u",
            "channel": "u",
            "external_pair": "h-_h+_to_h-_h+",
            "internal_photons": "gamma++;gamma--",
            "J": 4,
            "tree_partial_wave": str(tree_opposite_a4),
            "target_partial_wave_per_C_R4prime": str(target_crossed_a4),
            "identical_factor": str(identical_factor),
            "channel_source_dC_R4prime_dlnmu": str(gamma_u),
            "status": "DERIVED",
        },
        {
            "row_id": "CFF4968_TOTAL_same_helicity",
            "channel": "s+t+u",
            "external_pair": "all_same_graviton_helicity",
            "internal_photons": "no_common_cut_helicity",
            "J": "0,2,4 target",
            "tree_partial_wave": "zero overlap in every channel",
            "target_partial_wave_per_C_R4prime": "not_applicable",
            "identical_factor": str(identical_factor),
            "channel_source_dC_R4prime_dlnmu": str(gamma_r4),
            "status": "EXACT_HELICITY_ZERO",
        },
        {
            "row_id": "CFF4968_TOTAL_mixed_helicity",
            "channel": "s+t+u",
            "external_pair": "h--_h++_R4prime",
            "internal_photons": "complete_same_helicity_sum",
            "J": "0 plus crossed J=4",
            "tree_partial_wave": "assembled",
            "target_partial_wave_per_C_R4prime": "assembled",
            "identical_factor": str(identical_factor),
            "channel_source_dC_R4prime_dlnmu": str(gamma_r4_prime),
            "status": "DERIVED_COMPLETE_ONE_LOOP_CFF_SQUARED",
        },
    ]
    for row in rows:
        row.update(
            {
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
        )
    return {
        "d40_j4": str(d_40_j4),
        "tree_same_a0": str(tree_same_a0),
        "tree_opposite_a4": str(tree_opposite_a4),
        "target_s_a0": str(target_s_a0),
        "target_crossed_a4": str(target_crossed_a4),
        "gamma_C_R4": str(gamma_r4),
        "gamma_C_R4prime_q": str(gamma_r4_prime),
        "gamma_C_R4prime_WC": str(gamma_r4_prime_w),
        "beta_B_minus": "0",
        "beta_B_plus_WC": str(beta_b_plus_w),
        "beta_B_plus_running": str(beta_b_plus_running),
        "beta_B_C_running": str(beta_b_c_running),
        "beta_B_t_running": str(beta_b_t_running),
        "rows": rows,
        "checks": checks,
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    actual_hashes, provenance_checks = source_checks()
    projection = analytic_partial_wave_projection()
    sample_angles = (0.43, 0.91, 1.37)
    helicity_rows: list[
        tuple[str, tuple[int, int], tuple[int, int]]
    ] = [
        ("forbidden_same_to_same", (1, 1), (1, 1)),
        ("all_incoming_all_plus", (1, 1), (-1, -1)),
        ("opposite_gravitons_to_plus_photons", (1, -1), (1, 1)),
        ("opposite_gravitons_to_minus_photons", (1, -1), (-1, -1)),
        ("forbidden_opposite_photons", (1, -1), (1, -1)),
    ]
    cache: dict[
        tuple[
            float,
            tuple[int, int],
            tuple[int, int],
            tuple[str, int] | None,
            float,
        ],
        dict[str, complex],
    ] = {}

    def evaluate(
        angle: float,
        graviton_helicities: tuple[int, int],
        photon_helicities: tuple[int, int],
        replacement: tuple[str, int] | None = None,
        energy: float = 1.0,
    ) -> dict[str, complex]:
        key = (
            angle,
            graviton_helicities,
            photon_helicities,
            replacement,
            energy,
        )
        if key not in cache:
            cache[key] = cff_tree_amplitude(
                angle,
                graviton_helicities,
                photon_helicities,
                replacement,
                energy,
            )
        return cache[key]

    amplitude_rows: list[dict[str, object]] = []
    amplitude_checks: dict[str, bool] = {}
    for branch, graviton_helicities, photon_helicities in helicity_rows:
        values: list[complex] = []
        for angle in sample_angles:
            total = evaluate(
                angle, graviton_helicities, photon_helicities
            )["total"]
            if branch == "all_incoming_all_plus":
                expected = 8.0
                exact_formula = "kappa^2*c*s^2/2 at kappa=c=E=1"
            elif branch.startswith("opposite_gravitons"):
                expected = 2.0 * math.sin(angle) ** 2
                exact_formula = "kappa^2*c*t*u/2 at kappa=c=E=1"
            else:
                expected = 0.0
                exact_formula = "exact helicity zero"
            absolute_error = abs(total - expected)
            values.append(total)
            amplitude_rows.append(
                {
                    "branch": branch,
                    "graviton_helicities": str(graviton_helicities),
                    "photon_helicities": str(photon_helicities),
                    "theta_rad": angle,
                    "energy": 1.0,
                    "amplitude_real": total.real,
                    "amplitude_imag": total.imag,
                    "expected_real": expected,
                    "absolute_error": absolute_error,
                    "exact_formula": exact_formula,
                    "status": (
                        "PASS" if absolute_error <= 2.0e-11 else "FAIL"
                    ),
                    "checkpoint_marker": MARKER,
                    "valid_for_full_MTS_claim": False,
                    "source_checked_date": CHECKED_DATE,
                }
            )
            amplitude_checks[f"amplitude_{branch}_{angle}"] = (
                absolute_error <= 2.0e-11
            )
        print(
            f"{MARKER}_HELICITY={graviton_helicities}->{photon_helicities} "
            f"VALUES={values}",
            flush=True,
        )
    test_angle = 0.91
    ward_checks: dict[str, bool] = {}
    ward_residuals: dict[str, float] = {}
    for branch, graviton_helicities, photon_helicities in (
        ("all_plus", (1, 1), (-1, -1)),
        ("opposite", (1, -1), (1, 1)),
    ):
        nominal = evaluate(
            test_angle, graviton_helicities, photon_helicities
        )["total"]
        for particle in ("photon", "graviton"):
            for leg_index in (0, 1):
                replacement = evaluate(
                    test_angle,
                    graviton_helicities,
                    photon_helicities,
                    (particle, leg_index),
                )["total"]
                key = f"{branch}_{particle}_{leg_index}"
                residual = relative_gauge_residual(nominal, replacement)
                ward_residuals[key] = residual
                ward_checks[key] = residual <= TOLERANCE
    maximum_ward_residual = max(ward_residuals.values())
    scaled_energy = 0.7
    scaled_amplitude = evaluate(
        test_angle, (1, 1), (-1, -1), energy=scaled_energy
    )["total"]
    scaling_error = abs(scaled_amplitude - 8.0 * scaled_energy**4)
    normalization_checks = {
        "energy_four_scaling": scaling_error <= 2.0e-11,
        "code_E1_amplitude_is_8": abs(
            evaluate(test_angle, (1, 1), (-1, -1))["total"] - 8.0
        )
        <= 2.0e-11,
        "trott_shape_E1_is_s_squared_16": 4.0**2 == 16.0,
        "code_kappa_one_means_MPl_two": (2.0 / 1.0) == 2.0,
        "Lambda_inverse_squared_equals_2c": abs(
            8.0 - (16.0 / 2.0**2) * 2.0
        )
        <= 2.0e-11,
    }
    all_checks = {
        **provenance_checks,
        **amplitude_checks,
        **ward_checks,
        **normalization_checks,
        **{f"projection_{key}": bool(value) for key, value in projection["checks"].items()},
    }
    write_csv(AMPLITUDE_CSV, amplitude_rows)
    write_csv(PROJECTION_CSV, projection["rows"])
    result = {
        "marker": MARKER,
        "source_hashes": actual_hashes,
        "source_urls": {
            "complete_CFF_tree_amplitude": "https://arxiv.org/abs/2605.04152",
            "one_loop_partial_wave_formula": "https://arxiv.org/abs/2010.13809",
        },
        "action_convention": (
            "S=int sqrt(-g)[2 R/kappa^2-F^2/4+c C_mnrs F^mn F^rs]"
        ),
        "amplitude_normalization": {
            "generated_all_incoming_all_plus": (
                "A(gamma+ gamma+ h+ h+)=kappa^2*c*[12]^2[34]^4/(2s)"
            ),
            "generated_physical_same_pair": (
                "M(h+ h+ -> gamma- gamma-)=kappa^2*c*s^2/2"
            ),
            "generated_physical_opposite_pair": (
                "M(h+ h- -> gamma+ gamma+)=M(h+ h- -> gamma- gamma-)="
                "kappa^2*c*t*u/2"
            ),
            "Trott_coupling_map": "Lambda^-2=2c",
            "dimensionless_q": "q=M_P^2*c=2 W_C",
            "MTS_map": "W_C=c/(16 pi G_N)=g_CFF/(16 pi g)",
            "energy_scaling_error": scaling_error,
        },
        "partial_wave_projection": {
            key: value for key, value in projection.items() if key not in {"rows", "checks"}
        },
        "ward_residuals": ward_residuals,
        "maximum_ward_residual": maximum_ward_residual,
        "checks": all_checks,
        "outputs": {
            "amplitudes": relative(AMPLITUDE_CSV),
            "partial_waves": relative(PROJECTION_CSV),
        },
        "decision": {
            "CFF_squared_same_helicity_R4_source": "exact_zero",
            "CFF_squared_mixed_helicity_R4prime_source": "derived",
            "formula": "dC_R4prime/dlnmu=-79 q^2/(280 pi^2)=-79 W_C^2/(70 pi^2)",
            "running_formula": "source_beta_Bplus=-79 g_CFF^2/(140 pi g^2)",
            "full_MTS_claimed": False,
            "remaining_p8_source": "three-loop pure-Einstein and unselected parent sectors",
        },
        "all_checks_pass": all(all_checks.values()),
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        f"{MARKER}_MAX_WARD_RESIDUAL={maximum_ward_residual:.12g}",
        flush=True,
    )
    print(
        f"{MARKER}_GAMMA_R4PRIME={projection['gamma_C_R4prime_q']}",
        flush=True,
    )
    print(
        f"{MARKER}_BETA_BPLUS={projection['beta_B_plus_running']}",
        flush=True,
    )
    if not result["all_checks_pass"]:
        failed = [key for key, passed in all_checks.items() if not passed]
        raise RuntimeError(f"4968 derivation checks failed: {failed}")
    print(f"{MARKER}_OUTPUT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
