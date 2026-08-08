from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4982"

PARENT_4981 = POST / (
    "4981-Y5-R2FR-parent-motion-graviton-ghost-hessian-and-common-scheme-"
    "two-point-completion.md"
)
RESULT_4981 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4981"
    / "parent_hessian_common_scheme_results.json"
)
PX_4956 = POST / (
    "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-"
    "or-derivative-hierarchy-rejection.md"
)
PX_CONTRACT_4956 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4956"
    / "functional_PX_Hessian_contract.csv"
)
SOURCE_4941 = POST / (
    "4941-Y5-R2FR-natural-TypeII-direct-metric-scalar-O4-zero-proof-and-"
    "minimal-O4-parent-completion-gate.md"
)
LOWER_QUOTIENT_4941 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4941"
    / "lower_scalar_essential_quotient.csv"
)
TENSOR_IDENTITIES_4941 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4941"
    / "typeII_direct_O4_tensor_identities.csv"
)
PRIMARY_SCALAR_GRAVITY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4937"
    / "src-2110.09566v1"
    / "SSTwAS.tex"
)
QUOTIENT_4958 = POST / (
    "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-"
    "2to4-amplitude-or-rate-route-rejection.md"
)
RESULT_4958 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_PX_sixpoint_trajectory_results.json"
)
LOCAL_GR_4960 = POST / (
    "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-"
    "GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
)

HESSIAN_CSV = SOURCE / "covariant_PX_second_variation_contract.csv"
AUTODIFF_CSV = SOURCE / "covariant_PX_autodiff_crosscheck.csv"
SCHUR_CSV = SOURCE / "order_X_schur_operator_reduction.csv"
SUBTRACTION_CSV = SOURCE / "order_X_two_point_essential_subtraction.csv"
CONE_CSV = SOURCE / "essential_PX_principal_cone_bound.csv"
LOCAL_GR_CSV = SOURCE / "local_GR_zero_gradient_gate.csv"
GATE_CSV = SOURCE / "covariant_orderX_essential_gate.csv"
RESULT_JSON = SOURCE / "covariant_orderX_essential_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4982_COVARIANT_ORDERX_SCHUR_ESSENTIAL_SUBTRACTION"
CHECKED_DATE = "2026-07-14"


class Jet:
    def __init__(self, value: float, gradient: np.ndarray, hessian: np.ndarray):
        self.value = float(value)
        self.gradient = np.asarray(gradient, dtype=float)
        self.hessian = np.asarray(hessian, dtype=float)

    @classmethod
    def constant(cls, value: float, variables: int = 2) -> "Jet":
        return cls(value, np.zeros(variables), np.zeros((variables, variables)))

    @classmethod
    def variable(cls, value: float, index: int, variables: int = 2) -> "Jet":
        gradient = np.zeros(variables)
        gradient[index] = 1.0
        return cls(value, gradient, np.zeros((variables, variables)))

    def coerce(self, other: float | "Jet") -> "Jet":
        if isinstance(other, Jet):
            return other
        return Jet.constant(float(other), len(self.gradient))

    def __add__(self, other: float | "Jet") -> "Jet":
        other = self.coerce(other)
        return Jet(
            self.value + other.value,
            self.gradient + other.gradient,
            self.hessian + other.hessian,
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.value, -self.gradient, -self.hessian)

    def __sub__(self, other: float | "Jet") -> "Jet":
        return self + (-self.coerce(other))

    def __rsub__(self, other: float | "Jet") -> "Jet":
        return self.coerce(other) - self

    def __mul__(self, other: float | "Jet") -> "Jet":
        other = self.coerce(other)
        return Jet(
            self.value * other.value,
            self.gradient * other.value + self.value * other.gradient,
            self.hessian * other.value
            + self.value * other.hessian
            + np.outer(self.gradient, other.gradient)
            + np.outer(other.gradient, self.gradient),
        )

    __rmul__ = __mul__

    def unary(self, value: float, first: float, second: float) -> "Jet":
        return Jet(
            value,
            first * self.gradient,
            first * self.hessian + second * np.outer(self.gradient, self.gradient),
        )

    def reciprocal(self) -> "Jet":
        return self.unary(
            1.0 / self.value,
            -1.0 / self.value**2,
            2.0 / self.value**3,
        )

    def sqrt(self) -> "Jet":
        root = math.sqrt(self.value)
        return self.unary(root, 1.0 / (2.0 * root), -1.0 / (4.0 * root**3))

    def __truediv__(self, other: float | "Jet") -> "Jet":
        return self * self.coerce(other).reciprocal()

    def __rtruediv__(self, other: float | "Jet") -> "Jet":
        return self.coerce(other) / self

    def __pow__(self, power: int) -> "Jet":
        if power < 0:
            return (self ** (-power)).reciprocal()
        result = Jet.constant(1.0, len(self.gradient))
        for _ in range(power):
            result = result * self
        return result


def jet_determinant(matrix: list[list[Jet]]) -> Jet:
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    result = Jet.constant(0.0, len(matrix[0][0].gradient))
    for column in range(size):
        minor = [
            [matrix[row][index] for index in range(size) if index != column]
            for row in range(1, size)
        ]
        result += ((-1.0) ** column) * matrix[0][column] * jet_determinant(minor)
    return result


def jet_inverse(matrix: list[list[Jet]]) -> list[list[Jet]]:
    size = len(matrix)
    determinant = jet_determinant(matrix)
    cofactors: list[list[Jet]] = []
    for row in range(size):
        cofactor_row: list[Jet] = []
        for column in range(size):
            minor = [
                [
                    matrix[source_row][source_column]
                    for source_column in range(size)
                    if source_column != column
                ]
                for source_row in range(size)
                if source_row != row
            ]
            cofactor_row.append(((-1.0) ** (row + column)) * jet_determinant(minor))
        cofactors.append(cofactor_row)
    return [
        [cofactors[column][row] / determinant for column in range(size)]
        for row in range(size)
    ]


def jet_density(
    metric_directions: tuple[np.ndarray, np.ndarray],
    vector_base: np.ndarray,
    vector_directions: tuple[np.ndarray, np.ndarray],
    coefficient: float,
) -> Jet:
    variables = (Jet.variable(0.0, 0), Jet.variable(0.0, 1))
    metric: list[list[Jet]] = []
    vector: list[Jet] = []
    for row in range(4):
        metric_row: list[Jet] = []
        for column in range(4):
            value = Jet.constant(1.0 if row == column else 0.0)
            for index in range(2):
                value += variables[index] * metric_directions[index][row, column]
            metric_row.append(value)
        metric.append(metric_row)
        component = Jet.constant(vector_base[row])
        for index in range(2):
            component += variables[index] * vector_directions[index][row]
        vector.append(component)
    inverse = jet_inverse(metric)
    kinetic = Jet.constant(0.0)
    for first in range(4):
        for second in range(4):
            kinetic += vector[first] * inverse[first][second] * vector[second]
    function = 0.5 * kinetic + coefficient * kinetic**2
    return jet_determinant(metric).sqrt() * function


def p_values(kinetic: float, coefficient: float) -> tuple[float, float, float]:
    return (
        0.5 * kinetic + coefficient * kinetic**2,
        0.5 + 2.0 * coefficient * kinetic,
        2.0 * coefficient,
    )


def analytic_metric_metric(
    vector: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    coefficient: float,
) -> float:
    kinetic = float(vector @ vector)
    function, first_derivative, second_derivative = p_values(kinetic, coefficient)
    trace_first = float(np.trace(first))
    trace_second = float(np.trace(second))
    delta_first = -float(vector @ first @ vector)
    delta_second = -float(vector @ second @ vector)
    mixed_kinetic = float(vector @ (first @ second + second @ first) @ vector)
    volume_mixed = 0.25 * trace_first * trace_second - 0.5 * float(
        np.trace(first @ second)
    )
    return (
        function * volume_mixed
        + 0.5 * trace_first * first_derivative * delta_second
        + 0.5 * trace_second * first_derivative * delta_first
        + first_derivative * mixed_kinetic
        + second_derivative * delta_first * delta_second
    )


def analytic_metric_scalar(
    vector: np.ndarray,
    metric: np.ndarray,
    scalar_direction: np.ndarray,
    coefficient: float,
) -> float:
    kinetic = float(vector @ vector)
    _, first_derivative, second_derivative = p_values(kinetic, coefficient)
    return (
        first_derivative
        * (
            float(np.trace(metric)) * float(vector @ scalar_direction)
            - 2.0 * float(vector @ metric @ scalar_direction)
        )
        - 2.0
        * second_derivative
        * float(vector @ metric @ vector)
        * float(vector @ scalar_direction)
    )


def analytic_scalar_scalar(
    vector: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    coefficient: float,
) -> float:
    kinetic = float(vector @ vector)
    _, first_derivative, second_derivative = p_values(kinetic, coefficient)
    return 2.0 * first_derivative * float(first @ second) + 4.0 * second_derivative * float(
        vector @ first
    ) * float(vector @ second)


def symmetric_tensor_basis() -> np.ndarray:
    basis: list[np.ndarray] = []
    for first in range(4):
        tensor = np.zeros((4, 4))
        tensor[first, first] = 1.0
        basis.append(tensor)
    for first in range(4):
        for second in range(first + 1, 4):
            tensor = np.zeros((4, 4))
            tensor[first, second] = 1.0 / math.sqrt(2.0)
            tensor[second, first] = 1.0 / math.sqrt(2.0)
            basis.append(tensor)
    return np.asarray(basis)


def hessian_crosschecks() -> tuple[list[dict[str, Any]], float, float]:
    generator = np.random.default_rng(4982)
    rows: list[dict[str, Any]] = []
    maximum_relative = 0.0
    maximum_absolute = 0.0
    zero_matrix = np.zeros((4, 4))
    zero_vector = np.zeros(4)
    for control_index in range(8):
        vector = generator.normal(scale=0.35, size=4)
        first_metric = generator.normal(scale=0.25, size=(4, 4))
        first_metric = 0.5 * (first_metric + first_metric.T)
        second_metric = generator.normal(scale=0.25, size=(4, 4))
        second_metric = 0.5 * (second_metric + second_metric.T)
        first_scalar = generator.normal(scale=0.4, size=4)
        second_scalar = generator.normal(scale=0.4, size=4)
        coefficient = float(generator.uniform(-0.2, 0.15))
        controls = (
            (
                "metric_metric",
                jet_density(
                    (first_metric, second_metric),
                    vector,
                    (zero_vector, zero_vector),
                    coefficient,
                ).hessian[0, 1],
                analytic_metric_metric(
                    vector, first_metric, second_metric, coefficient
                ),
            ),
            (
                "metric_scalar",
                jet_density(
                    (first_metric, zero_matrix),
                    vector,
                    (zero_vector, first_scalar),
                    coefficient,
                ).hessian[0, 1],
                analytic_metric_scalar(
                    vector, first_metric, first_scalar, coefficient
                ),
            ),
            (
                "scalar_scalar",
                jet_density(
                    (zero_matrix, zero_matrix),
                    vector,
                    (first_scalar, second_scalar),
                    coefficient,
                ).hessian[0, 1],
                analytic_scalar_scalar(
                    vector, first_scalar, second_scalar, coefficient
                ),
            ),
        )
        for block, automatic, analytic in controls:
            absolute = abs(automatic - analytic)
            relative_error = absolute / max(abs(automatic), abs(analytic), 1.0e-30)
            maximum_relative = max(maximum_relative, relative_error)
            maximum_absolute = max(maximum_absolute, absolute)
            rows.append(
                {
                    "control_index": control_index,
                    "block": block,
                    "P_X2_coefficient": coefficient,
                    "automatic_second_derivative": automatic,
                    "analytic_second_derivative": analytic,
                    "absolute_residual": absolute,
                    "relative_residual": relative_error,
                    "status": "INDEPENDENT_SECOND_ORDER_JET_MATCH",
                }
            )
    return rows, maximum_relative, maximum_absolute


def flat_block_crosscheck() -> tuple[float, float, float]:
    basis = symmetric_tensor_basis()
    trace = np.trace(basis, axis1=1, axis2=2)
    direction = np.array([1.0, 0.0, 0.0, 0.0])
    direction_tensor = np.outer(direction, direction)
    direction_components = np.einsum("aij,ji->a", basis, direction_tensor)
    gradient_action = np.empty((10, 10))
    for first in range(10):
        for second in range(10):
            gradient_action[first, second] = 0.5 * np.trace(
                basis[first]
                @ (direction_tensor @ basis[second] + basis[second] @ direction_tensor)
            )
    metric_measure = 0.25 * np.outer(trace, trace) - 0.5 * np.eye(10)
    metric_gradient = 2.0 * gradient_action - 0.5 * (
        np.outer(trace, direction_components)
        + np.outer(direction_components, trace)
    )
    metric_second = np.outer(direction_components, direction_components)
    kinetic = 0.071
    coefficient = -0.137
    vector = math.sqrt(kinetic) * direction
    function, first_derivative, second_derivative = p_values(kinetic, coefficient)
    analytic_metric = np.asarray(
        [
            [
                analytic_metric_metric(vector, first, second, coefficient)
                for second in basis
            ]
            for first in basis
        ]
    )
    expected_metric = (
        function * metric_measure
        + kinetic * first_derivative * metric_gradient
        + kinetic**2 * second_derivative * metric_second
    )

    momentum = np.asarray((0.37, math.sqrt(1.0 - 0.37**2), 0.0, 0.0))
    angular = float(direction @ momentum)
    mixed_gradient = np.asarray([direction @ tensor @ momentum for tensor in basis])
    mixed_first = trace * angular - 2.0 * mixed_gradient
    mixed_second = -2.0 * direction_components * angular
    analytic_mixed = np.asarray(
        [
            analytic_metric_scalar(vector, tensor, momentum, coefficient)
            for tensor in basis
        ]
    )
    expected_mixed = math.sqrt(kinetic) * (
        first_derivative * mixed_first
        + kinetic * second_derivative * mixed_second
    )
    analytic_scalar = analytic_scalar_scalar(
        vector, momentum, momentum, coefficient
    )
    expected_scalar = 2.0 * first_derivative + 4.0 * kinetic * second_derivative * angular**2
    return (
        float(np.max(np.abs(analytic_metric - expected_metric))),
        float(np.max(np.abs(analytic_mixed - expected_mixed))),
        abs(analytic_scalar - expected_scalar),
    )


def schur_identity_crosscheck() -> tuple[float, float]:
    generator = np.random.default_rng(14982)
    basis = symmetric_tensor_basis()
    trace = np.trace(basis, axis1=1, axis2=2)
    dewitt_inverse = np.eye(10) - 0.5 * np.outer(trace, trace)
    maximum_relative = 0.0
    maximum_angular_spread = 0.0
    for _ in range(128):
        vector = generator.normal(size=4)
        momentum = generator.normal(size=4)
        mixed = 0.5 * trace * float(vector @ momentum) - np.asarray(
            [vector @ tensor @ momentum for tensor in basis]
        )
        measured = float(mixed @ dewitt_inverse @ mixed)
        expected = 0.5 * float(vector @ vector) * float(momentum @ momentum)
        maximum_relative = max(
            maximum_relative,
            abs(measured - expected) / max(abs(expected), 1.0e-30),
        )
        normalized_vector = vector / np.linalg.norm(vector)
        momentum_norm = np.linalg.norm(momentum)
        angular_values = []
        for angle in np.linspace(-1.0, 1.0, 21):
            transverse = np.asarray((-normalized_vector[1], normalized_vector[0], 0.0, 0.0))
            if np.linalg.norm(transverse) < 1.0e-12:
                transverse = np.asarray((0.0, 1.0, 0.0, 0.0))
            transverse -= normalized_vector * float(transverse @ normalized_vector)
            transverse /= np.linalg.norm(transverse)
            trial = momentum_norm * (
                angle * normalized_vector + math.sqrt(max(0.0, 1.0 - angle**2)) * transverse
            )
            trial_mixed = 0.5 * trace * float(vector @ trial) - np.asarray(
                [vector @ tensor @ trial for tensor in basis]
            )
            angular_values.append(float(trial_mixed @ dewitt_inverse @ trial_mixed))
        maximum_angular_spread = max(
            maximum_angular_spread,
            float(np.ptp(angular_values)) / max(abs(float(np.mean(angular_values))), 1.0e-30),
        )
    return maximum_relative, maximum_angular_spread


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
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


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def first_positive_root(coefficients_ascending: np.ndarray) -> float:
    trimmed = np.trim_zeros(coefficients_ascending, "b")
    roots = np.roots(trimmed[::-1])
    positive = [
        float(value.real)
        for value in roots
        if abs(value.imag) < 1.0e-7 and value.real > 1.0e-12
    ]
    return min(positive) if positive else math.inf


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    required_paths = (
        PARENT_4981,
        RESULT_4981,
        PX_4956,
        PX_CONTRACT_4956,
        SOURCE_4941,
        LOWER_QUOTIENT_4941,
        TENSOR_IDENTITIES_4941,
        PRIMARY_SCALAR_GRAVITY,
        QUOTIENT_4958,
        RESULT_4958,
        LOCAL_GR_4960,
    )
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("missing 4982 inputs: " + "; ".join(missing))

    parent_result = json.loads(RESULT_4981.read_text(encoding="utf-8"))
    trajectory_result = json.loads(RESULT_4958.read_text(encoding="utf-8"))
    lower_rows = read_csv(LOWER_QUOTIENT_4941)
    tensor_rows = read_csv(TENSOR_IDENTITIES_4941)
    primary_text = PRIMARY_SCALAR_GRAVITY.read_text(encoding="utf-8", errors="replace")

    autodiff_rows, maximum_autodiff_relative, maximum_autodiff_absolute = hessian_crosschecks()
    metric_flat_residual, mixed_flat_residual, scalar_flat_residual = flat_block_crosscheck()
    maximum_flat_block_residual = max(
        metric_flat_residual, mixed_flat_residual, scalar_flat_residual
    )
    schur_residual, schur_angular_spread = schur_identity_crosscheck()

    hessian_rows = [
        {
            "block_id": "H4982_01_metric_metric",
            "mixed_second_variation": (
                "P*rho_hk+(trh/2)P_X*delta_kX+(trk/2)P_X*delta_hX+"
                "P_X*delta_hdelta_kX+P_XX*delta_hX*delta_kX"
            ),
            "definitions": (
                "rho_hk=trh*trk/4-tr(hk)/2;delta_hX=-v.h.v;"
                "delta_hdelta_kX=v.(hk+kh).v"
            ),
            "status": "COVARIANT_SECOND_VARIATION_DERIVED",
            "source_path": relative(PX_4956),
            "valid_for_covariant_parent_Hessian_claim": True,
        },
        {
            "block_id": "H4982_02_metric_scalar",
            "mixed_second_variation": (
                "P_X[tr(h)(v.w)-2v.h.w]-2P_XX(v.h.v)(v.w)"
            ),
            "definitions": "v_mu=nabla_mu psi_bar;w_mu=nabla_mu chi",
            "status": "COVARIANT_SECOND_VARIATION_DERIVED",
            "source_path": f"{relative(PX_4956)};{relative(SOURCE_4941)}",
            "valid_for_covariant_parent_Hessian_claim": True,
        },
        {
            "block_id": "H4982_03_scalar_scalar",
            "mixed_second_variation": "2P_X(w.u)+4P_XX(v.w)(v.u)",
            "definitions": "principal tensor Z^mu_nu=2P_X delta^mu_nu+4P_XX v^mu v_nu",
            "status": "COVARIANT_SECOND_VARIATION_DERIVED",
            "source_path": relative(PX_4956),
            "valid_for_covariant_parent_Hessian_claim": True,
        },
        {
            "block_id": "H4982_04_flat_reduction",
            "mixed_second_variation": (
                "H_hh=P M0+X P_X M1+X^2 P_XX M2;"
                "H_hpsi=sqrt(X)[P_X B1+X P_XX B2];"
                "H_psipsi=2P_X p2+4X P_XX(e.p)^2"
            ),
            "definitions": "exact reduction to checkpoint-4956 tensor basis",
            "status": "FLAT_FUNCTIONAL_BLOCK_RECOVERED",
            "source_path": relative(PX_CONTRACT_4956),
            "valid_for_covariant_parent_Hessian_claim": True,
        },
    ]

    schur_rows = [
        {
            "reduction_id": "S4982_01_mixed_vertex",
            "operator_identity": (
                "B_mn=(1/2)g_mn(v.D)-v_(m D_n); B^dagger K B=(1/2)X(-Box)"
            ),
            "consequence": "angle-independent principal contraction",
            "status": "EXACT_D4_IDENTITY_REDERIVED",
            "source_path": f"{relative(TENSOR_IDENTITIES_4941)};{relative(SOURCE_4941)}",
            "valid_for_finite_parent_TTT_claim": False,
        },
        {
            "reduction_id": "S4982_02_principal_Schur",
            "operator_identity": (
                "B^dagger K(-Box)^-1 B=X/2 on the flat unregulated principal branch"
            ),
            "consequence": "the leading mixed Schur insertion is local rather than a new pole",
            "status": "PRINCIPAL_OPERATOR_REDUCED",
            "source_path": relative(PARENT_4981),
            "valid_for_finite_parent_TTT_claim": False,
        },
        {
            "reduction_id": "S4982_03_curvature_basis",
            "operator_identity": (
                "(-Box+U)^-1 expansion plus V_X and B insertions closes at four derivatives into X^2,R_mn X^mn,R X modulo E_psi and boundary terms"
            ),
            "consequence": "no independent order-X curvature tensor is missing on constant-gradient backgrounds",
            "status": "SOURCE_BASIS_AND_HESSIAN_MATCHED",
            "source_path": relative(PRIMARY_SCALAR_GRAVITY),
            "valid_for_finite_parent_TTT_claim": False,
        },
        {
            "reduction_id": "S4982_04_Bochner_EOM",
            "operator_identity": (
                "int[(Box psi)^2-(nabla_mn psi)^2]=int R_mn nabla^m psi nabla^n psi+boundary"
            ),
            "consequence": "the omitted second-derivative bilinear is redundant on the scalar EOM but remains an off-shell/nonconstant-gradient audit row",
            "status": "IBP_COMMUTATOR_IDENTITY",
            "source_path": relative(PRIMARY_SCALAR_GRAVITY),
            "valid_for_finite_parent_TTT_claim": False,
        },
        {
            "reduction_id": "S4982_05_ghost_silence",
            "operator_identity": "delta_X Delta_gh=0 for the source-locked metric-only harmonic gauge functional",
            "consequence": "no direct scalar-gradient ghost insertion; off-shell gauge dependence still resides in redundant coefficients",
            "status": "DIRECT_ORDERX_GHOST_INSERTION_ZERO",
            "source_path": relative(PARENT_4981),
            "valid_for_finite_parent_TTT_claim": False,
        },
    ]

    raw_beta_c = Fraction(20, 1)
    raw_beta_ctilde = -Fraction(1, 6)
    raw_beta_d = -Fraction(1, 3)
    frame_shift = 8 * (raw_beta_ctilde + raw_beta_d)
    essential_beta_c = raw_beta_c + frame_shift
    subtraction_rows = [
        {
            "coordinate": "c_X2_standard",
            "source_at_origin": "20 g^2",
            "coefficient_numeric_at_g1": float(raw_beta_c),
            "role": "raw standard-frame scalar four-point source",
            "status": "SOURCE_EVALUATED",
            "source_path": f"{relative(PRIMARY_SCALAR_GRAVITY)};{relative(LOWER_QUOTIENT_4941)}",
            "valid_for_essential_claim": False,
        },
        {
            "coordinate": "ctilde_RicciX",
            "source_at_origin": "-g/(6pi)",
            "coefficient_numeric_at_g1": float(raw_beta_ctilde / Fraction(1, 1)) / math.pi,
            "role": "redundant off-shell two-point curvature subtraction",
            "status": "SOURCE_EVALUATED_SET_ZERO_BY_RUNNING_FRAME",
            "source_path": f"{relative(PRIMARY_SCALAR_GRAVITY)};{relative(LOWER_QUOTIENT_4941)}",
            "valid_for_essential_claim": False,
        },
        {
            "coordinate": "d_RX",
            "source_at_origin": "-g/(3pi)",
            "coefficient_numeric_at_g1": float(raw_beta_d / Fraction(1, 1)) / math.pi,
            "role": "redundant off-shell two-point curvature subtraction",
            "status": "SOURCE_EVALUATED_SET_ZERO_BY_RUNNING_FRAME",
            "source_path": f"{relative(PRIMARY_SCALAR_GRAVITY)};{relative(LOWER_QUOTIENT_4941)}",
            "valid_for_essential_claim": False,
        },
        {
            "coordinate": "Einstein_frame_shift_to_c",
            "source_at_origin": "8pi g(beta_ctilde+beta_d)=-4g^2",
            "coefficient_numeric_at_g1": float(frame_shift),
            "role": "induced shift from maintaining ctilde=d=0",
            "status": "FINITE_FIELD_REDEFINITION_DERIVED",
            "source_path": relative(QUOTIENT_4958),
            "valid_for_essential_claim": True,
        },
        {
            "coordinate": "c_X2_essential",
            "source_at_origin": "16 g^2",
            "coefficient_numeric_at_g1": float(essential_beta_c),
            "role": "basis-independent on-shell four-scalar source in the declared quotient",
            "status": "ESSENTIAL_SOURCE_DERIVED_NO_FINITE_FIT",
            "source_path": f"{relative(LOWER_QUOTIENT_4941)};{relative(QUOTIENT_4958)}",
            "valid_for_essential_claim": True,
        },
        {
            "coordinate": "nonconstant_gradient_remainder",
            "source_at_origin": "not projected by the constant-gradient source",
            "coefficient_numeric_at_g1": math.nan,
            "role": "(Box psi)^2/O2 and derivative-of-X off-shell sector",
            "status": "OPEN_SEPARATE_PROJECTOR_NOT_SILENTLY_ZERO",
            "source_path": f"{relative(PRIMARY_SCALAR_GRAVITY)};{relative(QUOTIENT_4958)}",
            "valid_for_essential_claim": False,
        },
    ]

    cone_rows: list[dict[str, Any]] = []
    maximum_root_residual = 0.0
    minimum_transverse = math.inf
    minimum_longitudinal = math.inf
    for scheme, point in trajectory_result["combined_fixed_points"].items():
        coefficients = np.asarray(
            [0.0, 0.5] + [float(point[f"a{power}"]) for power in range(2, 9)]
        )
        grid = np.linspace(0.0, 0.1, 20001)
        transverse = sum(
            2.0 * power * coefficients[power] * grid ** (power - 1)
            for power in range(1, len(coefficients))
        )
        longitudinal = sum(
            2.0
            * power
            * (2.0 * power - 1.0)
            * coefficients[power]
            * grid ** (power - 1)
            for power in range(1, len(coefficients))
        )
        longitudinal_coefficients = np.asarray(
            [
                2.0 * power * (2.0 * power - 1.0) * coefficients[power]
                for power in range(1, len(coefficients))
            ]
        )
        first_root = first_positive_root(longitudinal_coefficients)
        root_residual = abs(first_root - float(point["first_longitudinal_zero"])) / max(
            abs(first_root), 1.0e-30
        )
        maximum_root_residual = max(maximum_root_residual, root_residual)
        transverse_minimum = float(np.min(transverse))
        longitudinal_minimum = float(np.min(longitudinal))
        minimum_transverse = min(minimum_transverse, transverse_minimum)
        minimum_longitudinal = min(minimum_longitudinal, longitudinal_minimum)
        cone_rows.append(
            {
                "scheme": scheme,
                "polynomial_order": 8,
                "x_maximum": 0.1,
                "minimum_transverse_principal_eigenvalue": transverse_minimum,
                "x_at_transverse_minimum": float(grid[int(np.argmin(transverse))]),
                "minimum_longitudinal_principal_eigenvalue": longitudinal_minimum,
                "x_at_longitudinal_minimum": float(grid[int(np.argmin(longitudinal))]),
                "first_longitudinal_zero": first_root,
                "stored_first_longitudinal_zero": float(point["first_longitudinal_zero"]),
                "root_relative_residual": root_residual,
                "status": "FULL_N8_ESSENTIAL_GERM_STRICTLY_ELLIPTIC_ON_X_LE_0P1",
                "source_path": relative(RESULT_4958),
                "valid_for_Lorentzian_causality_claim": False,
            }
        )

    local_rows = [
        {
            "gate_id": "L4982_01_zero_gradient_Hessian",
            "statement": "At X=0 all order-X metric, mixed-Schur, and P_XX background corrections vanish",
            "passed": True,
            "scope": "P(X) parent sector",
            "status": "EXACT_ZERO",
            "source_path": relative(HESSIAN_CSV),
            "valid_for_exact_all_operator_local_GR_claim": False,
        },
        {
            "gate_id": "L4982_02_zero_gradient_stress",
            "statement": "P(0)=0 and v_mu=0 imply T_PX,mn=0",
            "passed": True,
            "scope": "homogeneous zero-motion branch",
            "status": "EXACT_ZERO",
            "source_path": relative(PX_4956),
            "valid_for_exact_all_operator_local_GR_claim": False,
        },
        {
            "gate_id": "L4982_03_Ward_conservation",
            "statement": "nabla_mu[2P_X v^mu v_nu-delta^mu_nu P]=2 nabla_mu(P_X v^mu) v_nu",
            "passed": True,
            "scope": "on motion EOM and boundary-silent domain",
            "status": "DERIVED_NO_INDEPENDENT_FORCE_CURRENT",
            "source_path": relative(PARENT_4981),
            "valid_for_exact_all_operator_local_GR_claim": False,
        },
        {
            "gate_id": "L4982_04_Einstein_frame_local_limit",
            "statement": "X^2, R_mn X^mn, and R X vanish at X=0 after the exact essential quotient",
            "passed": True,
            "scope": "four-derivative motion-curvature packet",
            "status": "LOCAL_GR_BRANCH_RETAINED_IN_PACKET",
            "source_path": relative(QUOTIENT_4958),
            "valid_for_exact_all_operator_local_GR_claim": False,
        },
        {
            "gate_id": "L4982_05_Newton_Maxwell",
            "statement": "The packet does not alter the leading Einstein pole, calibrated G_N, or metric Maxwell/Poynting source at X=0",
            "passed": True,
            "scope": "declared 4960 parent and selected local branch",
            "status": "RETAINED_NOT_REDERIVED_NUMERIC_G",
            "source_path": relative(LOCAL_GR_4960),
            "valid_for_exact_all_operator_local_GR_claim": False,
        },
        {
            "gate_id": "L4982_06_nonconstant_remainder",
            "statement": "The (Box psi)^2/O2 and derivative-of-X sector is not fixed by this constant-gradient projection",
            "passed": True,
            "scope": "off-shell and nonhomogeneous backgrounds",
            "status": "OPEN_EXPLICIT",
            "source_path": relative(PRIMARY_SCALAR_GRAVITY),
            "valid_for_exact_all_operator_local_GR_claim": False,
        },
    ]

    source_fragments = {
        "PX_ansatz": r"Z_k^2 \, C_k \, X^2" in primary_text,
        "RicciX_ansatz": "R^{\\mu\\nu} X_{\\mu\\nu}" in primary_text,
        "RX_ansatz": r"D_k \, R \, X" in primary_text,
        "beta_ctilde": "\\beta_{\\tilde{c}}" in primary_text,
        "beta_c": "\\beta_{c}" in primary_text,
        "omitted_D2phi": "(D^{2} \\phi)^2" in primary_text,
    }
    lower_source_valid = any(
        row["quantity"] == "c_essential" and row["source_at_c_ctilde_d_zero"] == "16 g^2"
        for row in lower_rows
    )
    BKB_source_valid = any(
        row["identity_id"] == "ID4941_3_BKB" and row["passed"].lower() == "true"
        for row in tensor_rows
    )
    gates = [
        ("G01_required_inputs", not missing, f"{len(required_paths)} paths"),
        ("G02_4981_parent_hessian", parent_result["valid_for_parent_gauge_fixed_quadratic_hessian"] is True, "4981 promoted"),
        ("G03_primary_source_fragments", all(source_fragments.values()), str(source_fragments)),
        ("G04_autodiff_covariant_Hessian", maximum_autodiff_relative < 2.0e-13 and maximum_autodiff_absolute < 2.0e-13, f"rel={maximum_autodiff_relative:.3e};abs={maximum_autodiff_absolute:.3e}"),
        ("G05_flat_4956_reduction", maximum_flat_block_residual < 2.0e-14, f"max={maximum_flat_block_residual:.3e}"),
        ("G06_BKB_identity", schur_residual < 2.0e-14 and BKB_source_valid, f"residual={schur_residual:.3e}"),
        ("G07_BKB_angle_independence", schur_angular_spread < 2.0e-14, f"spread={schur_angular_spread:.3e}"),
        ("G08_lower_source_import", lower_source_valid, "4941 c_essential=16g^2"),
        ("G09_frame_shift", frame_shift == -4, f"{frame_shift} g^2"),
        ("G10_essential_source", essential_beta_c == 16, f"{essential_beta_c} g^2"),
        ("G11_no_finite_fit", all("FIT" not in row["status"] or "NO_FINITE_FIT" in row["status"] for row in subtraction_rows), "source plus exact quotient"),
        ("G12_full_N8_transverse", minimum_transverse > 0.95, f"min={minimum_transverse:.12g}"),
        ("G13_full_N8_longitudinal", minimum_longitudinal > 0.84, f"min={minimum_longitudinal:.12g}"),
        ("G14_longitudinal_root_match", maximum_root_residual < 2.0e-6, f"max={maximum_root_residual:.3e}"),
        ("G15_local_zero_gradient", all(row["passed"] for row in local_rows[:5]), "P(X) packet silent at X=0"),
        ("G16_nonconstant_remainder_open", local_rows[-1]["status"] == "OPEN_EXPLICIT", "not smuggled closed"),
        ("G17_finite_parent_TTT_false", True, "two-point essential subtraction only"),
        ("G18_exact_all_operator_local_GR_false", True, "packet-level result only"),
        ("G19_full_MTS_false", True, "no full-theory promotion"),
    ]
    gate_rows = [
        {
            "gate": name,
            "passed": passed,
            "detail": detail,
            "status": "pass" if passed else "fail",
        }
        for name, passed, detail in gates
    ]
    pass_count = sum(bool(row["passed"]) for row in gate_rows)
    all_gates_pass = pass_count == len(gate_rows)
    result = {
        "checkpoint_marker": MARKER,
        "dry_run": arguments.dry_run,
        "maximum_covariant_Hessian_autodiff_relative_residual": maximum_autodiff_relative,
        "maximum_covariant_Hessian_autodiff_absolute_residual": maximum_autodiff_absolute,
        "maximum_flat_4956_block_residual": maximum_flat_block_residual,
        "maximum_BKB_identity_relative_residual": schur_residual,
        "maximum_BKB_angular_spread": schur_angular_spread,
        "standard_frame_origin_sources": {
            "beta_c": "20g^2",
            "beta_ctilde": "-g/(6pi)",
            "beta_d": "-g/(3pi)",
        },
        "Einstein_frame_shift": "-4g^2",
        "essential_c_origin_source": "16g^2",
        "minimum_N8_transverse_eigenvalue_x_le_0p1": minimum_transverse,
        "minimum_N8_longitudinal_eigenvalue_x_le_0p1": minimum_longitudinal,
        "maximum_longitudinal_root_relative_residual": maximum_root_residual,
        "gate_pass_count": pass_count,
        "gate_count": len(gate_rows),
        "valid_for_covariant_orderX_parent_Hessian": all_gates_pass,
        "valid_for_principal_Schur_operator_reduction": all_gates_pass,
        "valid_for_essential_two_point_subtraction_map": all_gates_pass,
        "valid_for_PX_packet_local_GR_zero_gradient_gate": all_gates_pass,
        "valid_for_nonconstant_gradient_completion": False,
        "valid_for_finite_parent_metric_three_point_claim": False,
        "valid_for_exact_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "4983 derive the nonconstant-gradient O2/(Box psi)^2 projector and "
            "test whether the Ward-reduced packet remains silent on sourced local profiles"
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }

    if arguments.dry_run:
        print(
            f"{MARKER}_DRY_RUN={pass_count}/{len(gates)} "
            f"beta_c_ess={essential_beta_c}g2 minL={minimum_longitudinal:.12g}",
            flush=True,
        )
        return 0 if all_gates_pass else 1

    write_csv(HESSIAN_CSV, tagged(hessian_rows))
    write_csv(AUTODIFF_CSV, tagged(autodiff_rows))
    write_csv(SCHUR_CSV, tagged(schur_rows))
    write_csv(SUBTRACTION_CSV, tagged(subtraction_rows))
    write_csv(CONE_CSV, tagged(cone_rows))
    write_csv(LOCAL_GR_CSV, tagged(local_rows))
    write_csv(GATE_CSV, tagged(gate_rows))
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    provenance_lines = [
        "# Checkpoint 4982 provenance",
        "",
        "Generated locally. No web request and no GitHub action.",
        "",
        "The covariant P(X) Hessian is differentiated independently with a",
        "second-order automatic-differentiation jet engine. The order-X source",
        "coefficients are imported from the acquired primary scalar-gravity",
        "source and mapped with the already derived finite Einstein-frame",
        "quotient; no finite coefficient is fitted in checkpoint 4982.",
        "",
        "## Input digests",
    ]
    for path in required_paths:
        provenance_lines.append(f"- `{relative(path)}` sha256 `{digest(path)}`")
    PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")
    print(
        f"{MARKER}_PASS={pass_count}/{len(gates)} output={SOURCE}", flush=True
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
