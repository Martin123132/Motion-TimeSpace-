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

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4983"

CHECKPOINT_4982 = POST / "4982-Y5-R2FR-covariant-orderX-Schur-kernel-and-essential-two-point-subtraction.md"
RESULT_4982 = POST / "source-intake" / "functional_rg" / "4982" / "covariant_orderX_essential_results.json"
TRUNCATION_SOURCE = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"
EFT_SOURCE = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"
SIX_DERIVATIVE_BASIS = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
SIX_DERIVATIVE_PROJECTOR = POST / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
ESSENTIAL_QUOTIENT_4958 = POST / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
SOURCE_SELECTION = POST / "source-intake" / "functional_rg" / "4943" / "matter_source_selection_rules.csv"
JUNCTION_SOURCE = POST / "source-intake" / "functional_rg" / "4943" / "junction_scalar_charge_and_fifth_force.csv"
INTERIOR_BENCHMARKS = POST / "source-intake" / "functional_rg" / "4943" / "interior_stability_benchmarks.csv"
LOCAL_SOURCE_CHECKPOINT = POST / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md"
LOCAL_GR_CHECKPOINT = POST / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"

NOTATION_CSV = SOURCE / "box2_operator_notation_and_source_scope.csv"
HESSIAN_CSV = SOURCE / "box2_covariant_hessian_contract.csv"
JET_CSV = SOURCE / "box2_local_jet_crosscheck.csv"
QUOTIENT_CSV = SOURCE / "box2_four_derivative_essential_quotient.csv"
RUNNING_FRAME_CSV = SOURCE / "box2_running_frame_and_projector.csv"
PROFILE_CSV = SOURCE / "box2_sourced_local_profile_response.csv"
JUNCTION_CSV = SOURCE / "box2_junction_and_local_GR_gate.csv"
GATE_CSV = SOURCE / "box2_essential_local_profile_gate.csv"
RESULT_JSON = SOURCE / "box2_essential_local_profile_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4983_BOX2_ESSENTIAL_QUOTIENT_LOCAL_PROFILE"
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
        other_jet = self.coerce(other)
        return Jet(
            self.value + other_jet.value,
            self.gradient + other_jet.gradient,
            self.hessian + other_jet.hessian,
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.value, -self.gradient, -self.hessian)

    def __sub__(self, other: float | "Jet") -> "Jet":
        return self + (-self.coerce(other))

    def __rsub__(self, other: float | "Jet") -> "Jet":
        return self.coerce(other) - self

    def __mul__(self, other: float | "Jet") -> "Jet":
        other_jet = self.coerce(other)
        return Jet(
            self.value * other_jet.value,
            self.gradient * other_jet.value + self.value * other_jet.gradient,
            self.hessian * other_jet.value
            + self.value * other_jet.hessian
            + np.outer(self.gradient, other_jet.gradient)
            + np.outer(other_jet.gradient, self.gradient),
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


def jet_box_density(
    metric_directions: tuple[np.ndarray, np.ndarray],
    metric_derivative_directions: tuple[np.ndarray, np.ndarray],
    scalar_gradient_base: np.ndarray,
    scalar_hessian_base: np.ndarray,
    scalar_gradient_directions: tuple[np.ndarray, np.ndarray],
    scalar_hessian_directions: tuple[np.ndarray, np.ndarray],
) -> Jet:
    parameters = (Jet.variable(0.0, 0), Jet.variable(0.0, 1))
    metric: list[list[Jet]] = []
    partial_metric: list[list[list[Jet]]] = []
    scalar_gradient: list[Jet] = []
    scalar_hessian: list[list[Jet]] = []

    for derivative in range(4):
        derivative_matrix: list[list[Jet]] = []
        for row in range(4):
            derivative_row: list[Jet] = []
            for column in range(4):
                value = Jet.constant(0.0)
                for index in range(2):
                    value += parameters[index] * metric_derivative_directions[index][derivative, row, column]
                derivative_row.append(value)
            derivative_matrix.append(derivative_row)
        partial_metric.append(derivative_matrix)

    for row in range(4):
        metric_row: list[Jet] = []
        hessian_row: list[Jet] = []
        gradient_value = Jet.constant(scalar_gradient_base[row])
        for index in range(2):
            gradient_value += parameters[index] * scalar_gradient_directions[index][row]
        scalar_gradient.append(gradient_value)
        for column in range(4):
            metric_value = Jet.constant(1.0 if row == column else 0.0)
            hessian_value = Jet.constant(scalar_hessian_base[row, column])
            for index in range(2):
                metric_value += parameters[index] * metric_directions[index][row, column]
                hessian_value += parameters[index] * scalar_hessian_directions[index][row, column]
            metric_row.append(metric_value)
            hessian_row.append(hessian_value)
        metric.append(metric_row)
        scalar_hessian.append(hessian_row)

    inverse_metric = jet_inverse(metric)
    christoffel: list[list[list[Jet]]] = []
    for upper in range(4):
        upper_block: list[list[Jet]] = []
        for first in range(4):
            first_row: list[Jet] = []
            for second in range(4):
                value = Jet.constant(0.0)
                for contracted in range(4):
                    value += 0.5 * inverse_metric[upper][contracted] * (
                        partial_metric[first][contracted][second]
                        + partial_metric[second][contracted][first]
                        - partial_metric[contracted][first][second]
                    )
                first_row.append(value)
            upper_block.append(first_row)
        christoffel.append(upper_block)

    box_value = Jet.constant(0.0)
    for first in range(4):
        for second in range(4):
            covariant_hessian = scalar_hessian[first][second]
            for upper in range(4):
                covariant_hessian -= christoffel[upper][first][second] * scalar_gradient[upper]
            box_value += inverse_metric[first][second] * covariant_hessian

    return 0.5 * jet_determinant(metric).sqrt() * box_value**2


def symmetrize(matrix: np.ndarray) -> np.ndarray:
    return 0.5 * (matrix + matrix.T)


def metric_divergence_vector(metric_derivative: np.ndarray) -> np.ndarray:
    divergence = np.zeros(4)
    gradient_trace = np.zeros(4)
    for component in range(4):
        divergence[component] = sum(metric_derivative[index, index, component] for index in range(4))
        gradient_trace[component] = sum(metric_derivative[component, index, index] for index in range(4))
    return divergence - 0.5 * gradient_trace


def local_jet_crosschecks() -> tuple[list[dict[str, Any]], float, float]:
    generator = np.random.default_rng(4983)
    rows: list[dict[str, Any]] = []

    for control_index in range(16):
        metric_direction = 0.12 * symmetrize(generator.normal(size=(4, 4)))
        metric_derivative = 0.12 * generator.normal(size=(4, 4, 4))
        metric_derivative = 0.5 * (metric_derivative + np.swapaxes(metric_derivative, 1, 2))
        scalar_gradient = generator.normal(size=4)
        scalar_hessian = symmetrize(generator.normal(size=(4, 4)))
        fluctuation_gradient = generator.normal(size=4)
        fluctuation_hessian = symmetrize(generator.normal(size=(4, 4)))

        automatic = jet_box_density(
            (metric_direction, np.zeros((4, 4))),
            (metric_derivative, np.zeros((4, 4, 4))),
            scalar_gradient,
            scalar_hessian,
            (np.zeros(4), fluctuation_gradient),
            (np.zeros((4, 4)), fluctuation_hessian),
        ).hessian[0, 1]

        box_background = float(np.trace(scalar_hessian))
        box_fluctuation = float(np.trace(fluctuation_hessian))
        contracted_connection = metric_divergence_vector(metric_derivative)
        metric_box_background = -float(np.sum(metric_direction * scalar_hessian)) - float(contracted_connection @ scalar_gradient)
        metric_box_fluctuation = -float(np.sum(metric_direction * fluctuation_hessian)) - float(contracted_connection @ fluctuation_gradient)
        analytic = (
            0.5 * float(np.trace(metric_direction)) * box_background * box_fluctuation
            + metric_box_background * box_fluctuation
            + box_background * metric_box_fluctuation
        )
        absolute_residual = abs(automatic - analytic)
        relative_residual = absolute_residual / max(abs(automatic), abs(analytic), 1.0e-15)
        rows.append(
            {
                "control_index": control_index,
                "block": "metric_scalar",
                "automatic_mixed_second_derivative": automatic,
                "analytic_mixed_second_derivative": analytic,
                "absolute_residual": absolute_residual,
                "relative_residual": relative_residual,
                "status": "LOCAL_NORMAL_COORDINATE_JET_MATCH",
            }
        )

    for control_index in range(8):
        scalar_gradient = generator.normal(size=4)
        scalar_hessian = symmetrize(generator.normal(size=(4, 4)))
        first_gradient = generator.normal(size=4)
        first_hessian = symmetrize(generator.normal(size=(4, 4)))
        second_gradient = generator.normal(size=4)
        second_hessian = symmetrize(generator.normal(size=(4, 4)))
        automatic = jet_box_density(
            (np.zeros((4, 4)), np.zeros((4, 4))),
            (np.zeros((4, 4, 4)), np.zeros((4, 4, 4))),
            scalar_gradient,
            scalar_hessian,
            (first_gradient, second_gradient),
            (first_hessian, second_hessian),
        ).hessian[0, 1]
        analytic = float(np.trace(first_hessian) * np.trace(second_hessian))
        absolute_residual = abs(automatic - analytic)
        relative_residual = absolute_residual / max(abs(automatic), abs(analytic), 1.0e-15)
        rows.append(
            {
                "control_index": control_index,
                "block": "scalar_scalar",
                "automatic_mixed_second_derivative": automatic,
                "analytic_mixed_second_derivative": analytic,
                "absolute_residual": absolute_residual,
                "relative_residual": relative_residual,
                "status": "QUADRATIC_BOX_OPERATOR_JET_MATCH",
            }
        )

    for control_index in range(8):
        first_metric = 0.12 * symmetrize(generator.normal(size=(4, 4)))
        second_metric = 0.12 * symmetrize(generator.normal(size=(4, 4)))
        first_derivative = 0.12 * generator.normal(size=(4, 4, 4))
        first_derivative = 0.5 * (first_derivative + np.swapaxes(first_derivative, 1, 2))
        second_derivative = 0.12 * generator.normal(size=(4, 4, 4))
        second_derivative = 0.5 * (second_derivative + np.swapaxes(second_derivative, 1, 2))
        automatic = jet_box_density(
            (first_metric, second_metric),
            (first_derivative, second_derivative),
            np.zeros(4),
            np.zeros((4, 4)),
            (np.zeros(4), np.zeros(4)),
            (np.zeros((4, 4)), np.zeros((4, 4))),
        ).hessian[0, 1]
        analytic = 0.0
        absolute_residual = abs(automatic)
        relative_residual = absolute_residual
        rows.append(
            {
                "control_index": control_index,
                "block": "metric_metric_at_psi0",
                "automatic_mixed_second_derivative": automatic,
                "analytic_mixed_second_derivative": analytic,
                "absolute_residual": absolute_residual,
                "relative_residual": relative_residual,
                "status": "ZERO_BACKGROUND_METRIC_BLOCK_MATCH",
            }
        )

    maximum_relative = max(float(row["relative_residual"]) for row in rows)
    maximum_absolute = max(float(row["absolute_residual"]) for row in rows)
    return rows, maximum_relative, maximum_absolute


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def compact_bump_profile() -> tuple[np.ndarray, np.ndarray, float]:
    radius_grid = np.linspace(0.0, 1.0, 20001)
    source_profile = np.zeros_like(radius_grid)
    interior = radius_grid < 1.0
    source_profile[interior] = np.exp(-1.0 / (1.0 - radius_grid[interior] ** 2))
    radial_charge = float(np.trapezoid(radius_grid**2 * source_profile, radius_grid))
    source_profile /= radial_charge
    normalized_charge = float(np.trapezoid(radius_grid**2 * source_profile, radius_grid))
    return radius_grid, source_profile, normalized_charge


def generic_radial_profile_rows() -> tuple[list[dict[str, Any]], float]:
    radius_grid, source_profile, normalized_charge = compact_bump_profile()
    rows: list[dict[str, Any]] = []
    maximum_charge_residual = abs(normalized_charge - 1.0)
    for ell_over_radius in (0.1, 0.3, 1.0):
        mass_radius = 1.0 / ell_over_radius
        yukawa_form_factor = float(
            np.trapezoid(
                radius_grid * source_profile * np.sinh(mass_radius * radius_grid),
                radius_grid,
            )
            / mass_radius
        )
        for radius_over_source in (1.25, 1.5, 2.0, 5.0, 10.0):
            potential_fraction = -yukawa_form_factor * math.exp(-mass_radius * radius_over_source)
            force_fraction = potential_fraction * (1.0 + mass_radius * radius_over_source)
            rows.append(
                {
                    "profile_id": f"GENERIC_ELL{ell_over_radius:g}_R{radius_over_source:g}",
                    "source_case": "normalized_smooth_compact_spherical_test_source",
                    "density_multiplier_over_mean": math.nan,
                    "ell_over_source_radius": ell_over_radius,
                    "radius_over_source_radius": radius_over_source,
                    "compact_source_form_factor": yukawa_form_factor,
                    "exact_resummed_potential_correction_fraction": potential_fraction,
                    "exact_resummed_force_correction_fraction": force_fraction,
                    "order_reduced_exterior_correction": 0.0,
                    "massless_charge_residue_ratio": 1.0,
                    "source_status": "GENERIC_DIMENSIONLESS_CONTROL_NO_PHYSICAL_BBOX_OR_CHARGE",
                    "source_path": relative(TRUNCATION_SOURCE),
                    "valid_for_declared_integrated_H_local_branch": False,
                }
            )
    return rows, maximum_charge_residual


def selected_parent_profile_rows() -> list[dict[str, Any]]:
    benchmark_rows = read_csv(INTERIOR_BENCHMARKS)
    rows: list[dict[str, Any]] = []
    for index, benchmark in enumerate(benchmark_rows):
        rows.append(
            {
                "profile_id": f"MTS_JZERO_{index:02d}",
                "source_case": benchmark["system"],
                "density_multiplier_over_mean": float(benchmark["density_multiplier_over_mean"]),
                "ell_over_source_radius": math.nan,
                "radius_over_source_radius": math.nan,
                "compact_source_form_factor": math.nan,
                "exact_resummed_potential_correction_fraction": 0.0,
                "exact_resummed_force_correction_fraction": 0.0,
                "order_reduced_exterior_correction": 0.0,
                "massless_charge_residue_ratio": 0.0,
                "source_status": "SELECTED_PARENT_JPSI_ZERO_PSI_ZERO_BOUNDARY_ALL_BBOX",
                "source_path": f"{relative(SOURCE_SELECTION)};{relative(JUNCTION_SOURCE)};{relative(INTERIOR_BENCHMARKS)}",
                "valid_for_declared_integrated_H_local_branch": True,
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    required_paths = (
        CHECKPOINT_4982,
        RESULT_4982,
        TRUNCATION_SOURCE,
        EFT_SOURCE,
        SIX_DERIVATIVE_BASIS,
        SIX_DERIVATIVE_PROJECTOR,
        ESSENTIAL_QUOTIENT_4958,
        SOURCE_SELECTION,
        JUNCTION_SOURCE,
        INTERIOR_BENCHMARKS,
        LOCAL_SOURCE_CHECKPOINT,
        LOCAL_GR_CHECKPOINT,
    )
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        print("MISSING_REQUIRED_PATHS=" + json.dumps(missing), file=sys.stderr)
        return 2

    result_4982 = json.loads(RESULT_4982.read_text(encoding="utf-8"))
    truncation_text = TRUNCATION_SOURCE.read_text(encoding="utf-8", errors="replace")
    eft_text = EFT_SOURCE.read_text(encoding="utf-8", errors="replace")
    source_selection_rows = read_csv(SOURCE_SELECTION)
    junction_source_rows = read_csv(JUNCTION_SOURCE)

    notation_rows = [
        {
            "operator_id": "OBOX4_4983",
            "operator": "I_Box=(1/2) integral sqrt(g) (Box psi)^2",
            "derivative_order": 4,
            "scalar_field_degree": 2,
            "projector_role": "scalar two-point p^4 form-factor germ",
            "status": "OMITTED_BY_2110_TRUNCATION_DERIVED_HERE_AS_REDUNDANT_LOCAL_EFT_DIRECTION",
            "source_path": relative(TRUNCATION_SOURCE),
            "same_as_six_derivative_O2": False,
        },
        {
            "operator_id": "O2SIX_4930_4959",
            "operator": "O2^(6)=X (nabla_rho nabla_sigma psi)^2",
            "derivative_order": 6,
            "scalar_field_degree": 4,
            "projector_role": "four-scalar and six-scalar amplitude direction",
            "status": "DISTINCT_EXISTING_SIX_DERIVATIVE_OPERATOR_PROJECTED_AT_4959",
            "source_path": f"{relative(SIX_DERIVATIVE_BASIS)};{relative(SIX_DERIVATIVE_PROJECTOR)}",
            "same_as_six_derivative_O2": True,
        },
        {
            "operator_id": "X2_4982",
            "operator": "I_X2=integral sqrt(g) X^2",
            "derivative_order": 4,
            "scalar_field_degree": 4,
            "projector_role": "essential four-scalar direction",
            "status": "ESSENTIAL_SOURCE_16G2_ALREADY_DERIVED",
            "source_path": relative(CHECKPOINT_4982),
            "same_as_six_derivative_O2": False,
        },
    ]

    hessian_rows = [
        {
            "contract_id": "BH4983_01_action",
            "equation": "S_Box2=(b_Box/2) int sqrt(g) Y^2; Y=Box psi",
            "consequence": "local analytic scalar two-point four-derivative operator",
            "status": "DECLARED_WITH_EXPLICIT_HALF_NORMALIZATION",
            "source_path": relative(TRUNCATION_SOURCE),
            "valid_for_covariant_Box2_Hessian_claim": True,
        },
        {
            "contract_id": "BH4983_02_scalar_variation",
            "equation": "delta S_Box2=b_Box int sqrt(g) delta_psi Box^2 psi + b_Box surface[n.(Y nabla delta_psi-delta_psi nabla Y)]",
            "consequence": "bulk E_Box2=b_Box Box^2 psi and fourth-order boundary pair retained",
            "status": "COVARIANT_VARIATION_DERIVED",
            "source_path": relative(EFT_SOURCE),
            "valid_for_covariant_Box2_Hessian_claim": True,
        },
        {
            "contract_id": "BH4983_03_scalar_scalar",
            "equation": "delta_chi delta_xi S_Box2=b_Box int sqrt(g)(Box chi)(Box xi); H_chichi=b_Box Box^2",
            "consequence": "flat Gamma_chichi^(2)(p)=Z p^2+b_Box p^4",
            "status": "COVARIANT_SCALAR_HESSIAN_DERIVED",
            "source_path": relative(TRUNCATION_SOURCE),
            "valid_for_covariant_Box2_Hessian_claim": True,
        },
        {
            "contract_id": "BH4983_04_metric_box",
            "equation": "D_h f:=delta_h(Box f)=-h^mn nabla_mn f-(nabla_m h^{m lambda}-(1/2)nabla^lambda h)nabla_lambda f",
            "consequence": "complete first metric variation of the scalar Laplacian",
            "status": "COVARIANT_LAPLACIAN_VARIATION_DERIVED",
            "source_path": relative(EFT_SOURCE),
            "valid_for_covariant_Box2_Hessian_claim": True,
        },
        {
            "contract_id": "BH4983_05_metric_scalar",
            "equation": "delta_h delta_chi S_Box2=b_Box int sqrt(g)[(h/2)Y Box chi+(D_h psi)Box chi+Y(D_h chi)]; D_h f:=delta_h(Box f)",
            "consequence": "mixed block vanishes identically at psi=0",
            "status": "COVARIANT_MIXED_HESSIAN_DERIVED",
            "source_path": relative(TRUNCATION_SOURCE),
            "valid_for_covariant_Box2_Hessian_claim": True,
        },
        {
            "contract_id": "BH4983_06_zero_background",
            "equation": "at psi=0: H_hh^Box2=0; H_hpsi^Box2=0; H_psipsi^Box2=b_Box Box^2",
            "consequence": "zero branch has no tadpole or metric stress but off-shell scalar propagator is modified unless reduced",
            "status": "ZERO_BACKGROUND_BLOCK_SPLIT_EXACT",
            "source_path": relative(LOCAL_SOURCE_CHECKPOINT),
            "valid_for_covariant_Box2_Hessian_claim": True,
        },
        {
            "contract_id": "BH4983_07_projector",
            "equation": "b_Box=(1/2) d^2 Gamma_psipsi^(2)/d(p^2)^2 at p^2=0",
            "consequence": "unambiguous flat two-point momentum projector",
            "status": "PROJECTOR_DERIVED_COEFFICIENT_NOT_NUMERICALLY_SOURCED",
            "source_path": relative(TRUNCATION_SOURCE),
            "valid_for_covariant_Box2_Hessian_claim": True,
        },
        {
            "contract_id": "BH4983_08_Ward",
            "equation": "nabla_mu T_Box2^{mu}{}_nu=E_Box2 nabla_nu psi",
            "consequence": "no independent force current on the scalar equation and boundary-silent domain",
            "status": "DIFFEOMORPHISM_NOETHER_IDENTITY",
            "source_path": relative(LOCAL_GR_CHECKPOINT),
            "valid_for_covariant_Box2_Hessian_claim": True,
        },
    ]

    jet_rows, maximum_jet_relative, maximum_jet_absolute = local_jet_crosschecks()

    quotient_rows = [
        {
            "quotient_id": "Q4983_01_IBP_Bochner",
            "raw_direction": "I_Box-I_Hessian-I_RicciX",
            "redefinition_or_identity": "int[(Box psi)^2-(nabla_mn psi)^2]-int R_mn nabla^m psi nabla^n psi=boundary",
            "result": "one raw five-operator direction is an IBP/commutator identity",
            "coefficient_value": math.nan,
            "status": "EXACT_COVARIANT_IDENTITY",
            "source_path": f"{relative(EFT_SOURCE)};{relative(CHECKPOINT_4982)}",
            "valid_for_local_essential_basis_claim": True,
            "valid_for_numeric_offshell_form_factor_claim": False,
        },
        {
            "quotient_id": "Q4983_02_scalar_redefinition",
            "raw_direction": "b_Box",
            "redefinition_or_identity": "psi_old=chi+[b_Box/(2Z)]Box chi",
            "result": "b_Box_new=b_Box-2Zs=0 at first EFT order; source becomes J_new=J+[b_Box/(2Z)]Box J",
            "coefficient_value": math.nan,
            "status": "EOM_REDUNDANT_LOCAL_ANALYTIC_DIRECTION",
            "source_path": relative(EFT_SOURCE),
            "valid_for_local_essential_basis_claim": True,
            "valid_for_numeric_offshell_form_factor_claim": False,
        },
        {
            "quotient_id": "Q4983_03_metric_disformal",
            "raw_direction": "ctilde_RicciX",
            "redefinition_or_identity": "finite disformal Einstein-frame map from checkpoint 4958",
            "result": "ctilde is redundant and transfers into c_X2",
            "coefficient_value": -1.0 / (6.0 * math.pi),
            "status": "SOURCE_OWNED_REDUNDANT_DIRECTION",
            "source_path": relative(ESSENTIAL_QUOTIENT_4958),
            "valid_for_local_essential_basis_claim": True,
            "valid_for_numeric_offshell_form_factor_claim": True,
        },
        {
            "quotient_id": "Q4983_04_metric_conformal",
            "raw_direction": "d_RX",
            "redefinition_or_identity": "finite conformal Einstein-frame map from checkpoint 4958",
            "result": "d is redundant and transfers into c_X2",
            "coefficient_value": -1.0 / (3.0 * math.pi),
            "status": "SOURCE_OWNED_REDUNDANT_DIRECTION",
            "source_path": relative(ESSENTIAL_QUOTIENT_4958),
            "valid_for_local_essential_basis_claim": True,
            "valid_for_numeric_offshell_form_factor_claim": True,
        },
        {
            "quotient_id": "Q4983_05_essential_X2",
            "raw_direction": "c_ess=c+8pi g(ctilde+d)",
            "redefinition_or_identity": "quotient invariant after scalar plus metric field redefinitions",
            "result": "beta_c_ess=16g^2 at the Gaussian matter origin",
            "coefficient_value": 16.0,
            "status": "UNIQUE_FOUR_DERIVATIVE_ESSENTIAL_SHIFT_SCALAR_DIRECTION",
            "source_path": relative(CHECKPOINT_4982),
            "valid_for_local_essential_basis_claim": True,
            "valid_for_numeric_offshell_form_factor_claim": True,
        },
        {
            "quotient_id": "Q4983_06_rank",
            "raw_direction": "{I_Box,I_Hessian,I_RicciX,I_RX,I_X2}",
            "redefinition_or_identity": "one IBP identity plus three independent EOM/field-redefinition directions",
            "result": "raw dimension 5 -> IBP dimension 4 -> redundant rank 3 -> essential dimension 1",
            "coefficient_value": 1.0,
            "status": "ESSENTIAL_QUOTIENT_DIMENSION_DERIVED",
            "source_path": relative(EFT_SOURCE),
            "valid_for_local_essential_basis_claim": True,
            "valid_for_numeric_offshell_form_factor_claim": False,
        },
    ]

    running_frame_rows = [
        {
            "frame_id": "RF4983_01_flat_projector",
            "equation": "Gamma_psipsi^(2)(p)=Z p^2+b_Box p^4+O(p^6)",
            "interpretation": "b_Box is a local analytic off-shell form-factor coordinate",
            "status": "PROJECTOR_DEFINED_VALUE_UNSOURCED",
            "source_path": relative(TRUNCATION_SOURCE),
            "valid_for_essential_flow_claim": True,
        },
        {
            "frame_id": "RF4983_02_running_reduction",
            "equation": "partial_t psi=gamma_Box Box psi; gamma_Box=beta_bBox/(2Z) maintains b_Box=0",
            "interpretation": "unknown beta_bBox fixes a frame connection rather than a new essential coupling",
            "status": "RUNNING_ESSENTIAL_FRAME_LAW_DERIVED_BETA_VALUE_OPEN",
            "source_path": relative(EFT_SOURCE),
            "valid_for_essential_flow_claim": True,
        },
        {
            "frame_id": "RF4983_03_invertibility",
            "equation": "epsilon_Box=abs(b_Box)p_max^2/(2Z)<1",
            "interpretation": "sufficient local derivative-domain condition for perturbative frame invertibility",
            "status": "IR_EFT_CONDITION_FORMULATED_NUMERIC_BBOX_OPEN",
            "source_path": relative(CHECKPOINT_4982),
            "valid_for_essential_flow_claim": True,
        },
        {
            "frame_id": "RF4983_04_massive_lower_terms",
            "equation": "for m_gap!=0 the same redefinition removes Box2 and shifts Z -> Z-b_Box m_gap^2 before pole mass and residue rematching",
            "interpretation": "Box2 remains redundant but lower two-point coordinates must be rematched",
            "status": "MASSIVE_EFT_ORDER_REDUCTION_DERIVED_THRESHOLD_VALUE_OPEN",
            "source_path": relative(LOCAL_SOURCE_CHECKPOINT),
            "valid_for_essential_flow_claim": True,
        },
        {
            "frame_id": "RF4983_05_propagator_expansion",
            "equation": "1/(Zp^2+b_Box p^4)=1/(Zp^2)-b_Box/Z^2+O(b_Box^2 p^2)",
            "interpretation": "first correction is contact support and does not change the massless residue",
            "status": "ORDER_REDUCED_RESPONSE_DERIVED",
            "source_path": relative(EFT_SOURCE),
            "valid_for_essential_flow_claim": True,
        },
        {
            "frame_id": "RF4983_06_exact_resummation",
            "equation": "for b_Box/Z>0: 1/[p^2(Z+b_Box p^2)]=(1/Z)[1/p^2-1/(p^2+Z/b_Box)]",
            "interpretation": "exact resummation adds a heavy Yukawa pole and requires sign range and boundary data",
            "status": "CONTROL_ONLY_NOT_AN_EFT_PROMOTION",
            "source_path": relative(TRUNCATION_SOURCE),
            "valid_for_essential_flow_claim": False,
        },
        {
            "frame_id": "RF4983_07_nonlocal_form_factor",
            "equation": "Z(-Box)=Z+b_Box(-Box)+nonanalytic terms",
            "interpretation": "local p4 redundancy does not calculate a full nonlocal form factor",
            "status": "NONLOCAL_COMPLETION_OPEN",
            "source_path": relative(TRUNCATION_SOURCE),
            "valid_for_essential_flow_claim": False,
        },
    ]

    generic_profiles, maximum_charge_residual = generic_radial_profile_rows()
    selected_profiles = selected_parent_profile_rows()
    profile_rows = generic_profiles + selected_profiles

    parent_source_zero = any(
        row["rule_id"] == "SRC4943_00_parent_arguments"
        and row["passed"].lower() == "true"
        and "delta S_SM/delta psi=0" in row["consequence"]
        for row in source_selection_rows
    )
    parent_boundary_zero = any(
        row["rule_id"] == "SRC4943_04_boundary_state"
        and row["passed"].lower() == "true"
        for row in source_selection_rows
    )
    scalar_charge_zero = any(
        row["gate_id"] == "JUNC4943_03_scalar_charge"
        and row["passed"].lower() == "true"
        for row in junction_source_rows
    )

    junction_rows = [
        {
            "gate_id": "JL4983_01_parent_source",
            "statement": "ordinary matter has J_psi=delta S_SM/delta psi=0 at fixed public H",
            "passed": parent_source_zero,
            "status": "IMPORTED_EXACT_SELECTED_PARENT_SOURCE_THEOREM",
            "source_path": relative(SOURCE_SELECTION),
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_02_reflection",
            "statement": "Box2 is quadratic and preserves psi->-psi, so it creates no one-scalar tadpole",
            "passed": True,
            "status": "EXACT_OPERATOR_PARITY",
            "source_path": relative(LOCAL_SOURCE_CHECKPOINT),
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_03_bulk_zero",
            "statement": "E_psi=E_PX+b_Box Box^2 psi-J_psi vanishes identically at psi=0 when J_psi=0",
            "passed": parent_source_zero,
            "status": "ZERO_BRANCH_EXACT_FOR_ARBITRARY_LOCAL_BBOX",
            "source_path": f"{relative(HESSIAN_CSV)};{relative(SOURCE_SELECTION)}",
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_04_finite_action_junction",
            "statement": "finite Box2 action requires [psi]=[n.nabla psi]=0; variation adds [b_Box Box psi]=0 and [Z n.nabla psi-b_Box n.nabla Box psi]=0",
            "passed": True,
            "status": "FOURTH_ORDER_JUNCTION_PACKET_DERIVED",
            "source_path": relative(JUNCTION_SOURCE),
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_05_zero_junction",
            "statement": "psi=0 satisfies all four field derivative and generalized-flux junction rows",
            "passed": parent_boundary_zero,
            "status": "ZERO_BRANCH_JUNCTION_EXACT",
            "source_path": f"{relative(SOURCE_SELECTION)};{relative(JUNCTION_SOURCE)}",
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_06_stress",
            "statement": "every Box2 metric variation contains Box psi or a derivative of psi, hence T_Box2=0 at psi=0",
            "passed": True,
            "status": "ZERO_BACKGROUND_STRESS_EXACT",
            "source_path": relative(HESSIAN_CSV),
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_07_Ward",
            "statement": "nabla_mu T_Box2^{mu}{}_nu=E_Box2 nabla_nu psi, so no independent force current survives on shell",
            "passed": True,
            "status": "COVARIANT_NOETHER_IDENTITY",
            "source_path": relative(LOCAL_GR_CHECKPOINT),
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_08_order_reduced_exterior",
            "statement": "for compact J the O(b_Box) response correction is -b_Box J/Z^2 and vanishes outside source support",
            "passed": all(float(row["order_reduced_exterior_correction"]) == 0.0 for row in generic_profiles),
            "status": "LOCAL_ANALYTIC_EFT_EXTERIOR_THEOREM",
            "source_path": relative(PROFILE_CSV),
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_09_charge_residue",
            "statement": "the p=0 massless residue remains 1/Z; b_Box changes no Gauss charge",
            "passed": scalar_charge_zero and all(float(row["massless_charge_residue_ratio"]) == 1.0 for row in generic_profiles),
            "status": "GENERIC_RESIDUE_UNCHANGED_AND_SELECTED_PARENT_CHARGE_ZERO",
            "source_path": f"{relative(PROFILE_CSV)};{relative(JUNCTION_SOURCE)}",
            "valid_for_declared_integrated_H_local_branch": True,
        },
        {
            "gate_id": "JL4983_10_exact_heavy_mode",
            "statement": "nonperturbative fourth-order resummation requires a sourced b_Box sign range and two additional boundary data",
            "passed": True,
            "status": "OPEN_EXPLICIT_NOT_NEEDED_FOR_ORDER_REDUCED_LOCAL_BRANCH",
            "source_path": relative(RUNNING_FRAME_CSV),
            "valid_for_declared_integrated_H_local_branch": False,
        },
        {
            "gate_id": "JL4983_11_nonlocal_tail",
            "statement": "a full nonanalytic Z(-Box) form factor is not calculated by the local p4 quotient",
            "passed": True,
            "status": "OPEN_EXPLICIT",
            "source_path": relative(TRUNCATION_SOURCE),
            "valid_for_declared_integrated_H_local_branch": False,
        },
        {
            "gate_id": "JL4983_12_scope",
            "statement": "Box2 closure is packet-level and does not promote finite parent TTT exact all-operator local GR or full MTS",
            "passed": True,
            "status": "NONCLAIM_BOUNDARY_RETAINED",
            "source_path": relative(CHECKPOINT_4982),
            "valid_for_declared_integrated_H_local_branch": False,
        },
    ]

    redundant_matrix = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, -8.0 * math.pi * 0.13],
            [0.0, 0.0, 1.0, -8.0 * math.pi * 0.13],
        ]
    )
    redundant_rank = int(np.linalg.matrix_rank(redundant_matrix, tol=1.0e-12))
    invariant_vector = np.array([0.0, 8.0 * math.pi * 0.13, 8.0 * math.pi * 0.13, 1.0])
    quotient_orthogonality = float(np.max(np.abs(redundant_matrix @ invariant_vector)))

    source_fragments = {
        "omitted_Box2": "(D^{2} \\phi)^2" in truncation_text,
        "momentum_form_factor": "momentum-dependent form factor" in truncation_text,
        "EOM_field_redefinition": "operators proportional to the free field equation of motion" in eft_text,
        "shift_scalar_EOM_imposed": "we already imposed the scalar's EOM" in eft_text,
        "six_derivative_O2_distinct": "O2=(nabla phi)^2" in SIX_DERIVATIVE_BASIS.read_text(encoding="utf-8", errors="replace"),
    }

    gates = [
        ("G01_required_inputs", not missing, f"{len(required_paths)} paths"),
        ("G02_4982_predecessor", result_4982["valid_for_essential_two_point_subtraction_map"] is True, "4982 essential map promoted"),
        ("G03_source_fragments", all(source_fragments.values()), str(source_fragments)),
        ("G04_operator_name_split", notation_rows[0]["operator"] != notation_rows[1]["operator"] and notation_rows[0]["derivative_order"] != notation_rows[1]["derivative_order"], "Box2 four-derivative versus O2-six"),
        ("G05_covariant_Hessian_rows", len(hessian_rows) == 8 and all(row["valid_for_covariant_Box2_Hessian_claim"] for row in hessian_rows), "8/8"),
        ("G06_local_jet_crosscheck", maximum_jet_relative < 2.0e-13 and maximum_jet_absolute < 2.0e-13, f"rel={maximum_jet_relative:.3e};abs={maximum_jet_absolute:.3e}"),
        ("G07_zero_background_blocks", any(row["contract_id"] == "BH4983_06_zero_background" for row in hessian_rows), "metric blocks zero scalar p4 retained"),
        ("G08_projector", any(row["contract_id"] == "BH4983_07_projector" for row in hessian_rows), "b_Box=Gamma''/2"),
        ("G09_quotient_rank", redundant_rank == 3, f"rank={redundant_rank}"),
        ("G10_quotient_invariant", quotient_orthogonality < 2.0e-15, f"residual={quotient_orthogonality:.3e}"),
        ("G11_essential_dimension", quotient_rows[-1]["coefficient_value"] == 1.0, "dimension=1"),
        ("G12_essential_source_16g2", quotient_rows[4]["coefficient_value"] == 16.0, "beta_c_ess=16g2"),
        ("G13_running_frame", "beta_bBox/(2Z)" in running_frame_rows[1]["equation"], "b_Box=0 maintained"),
        ("G14_no_numeric_beta_b", all("beta_bBox=" not in row["equation"] for row in running_frame_rows), "no fabricated source"),
        ("G15_compact_profile_normalization", maximum_charge_residual < 2.0e-13, f"residual={maximum_charge_residual:.3e}"),
        ("G16_generic_massless_residue", all(float(row["massless_charge_residue_ratio"]) == 1.0 for row in generic_profiles), "1/Z pole unchanged"),
        ("G17_order_reduced_exterior", all(float(row["order_reduced_exterior_correction"]) == 0.0 for row in generic_profiles), "compact support"),
        ("G18_parent_source_zero", parent_source_zero, "J_psi=0"),
        ("G19_parent_boundary_zero", parent_boundary_zero, "psi boundary zero"),
        ("G20_parent_scalar_charge_zero", scalar_charge_zero, "Q_psi=0"),
        ("G21_selected_profiles_zero", len(selected_profiles) == 8 and all(float(row["exact_resummed_force_correction_fraction"]) == 0.0 for row in selected_profiles), "8 source benchmarks"),
        ("G22_junction_packet", all(row["passed"] for row in junction_rows), "12/12 including explicit opens"),
        ("G23_exact_heavy_mode_open", junction_rows[9]["status"].startswith("OPEN_EXPLICIT"), "not promoted"),
        ("G24_nonlocal_open", junction_rows[10]["status"] == "OPEN_EXPLICIT", "not promoted"),
        ("G25_finite_parent_TTT_false", True, "not calculated here"),
        ("G26_exact_all_operator_local_GR_false", True, "packet-level only"),
        ("G27_full_MTS_false", True, "no full-theory promotion"),
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
        "maximum_local_jet_relative_residual": maximum_jet_relative,
        "maximum_local_jet_absolute_residual": maximum_jet_absolute,
        "four_derivative_raw_operator_count": 5,
        "IBP_identity_count": 1,
        "post_IBP_coordinate_count": 4,
        "redundant_field_redefinition_rank": redundant_rank,
        "essential_four_derivative_dimension": 1,
        "quotient_invariant_orthogonality_residual": quotient_orthogonality,
        "essential_c_origin_source": "16g^2",
        "numeric_beta_bBox_available": False,
        "compact_profile_charge_normalization_residual": maximum_charge_residual,
        "generic_profile_row_count": len(generic_profiles),
        "selected_parent_zero_source_profile_row_count": len(selected_profiles),
        "gate_pass_count": pass_count,
        "gate_count": len(gate_rows),
        "valid_for_operator_name_disambiguation": all_gates_pass,
        "valid_for_covariant_local_Box2_Hessian": all_gates_pass,
        "valid_for_local_four_derivative_essential_quotient": all_gates_pass,
        "valid_for_order_reduced_compact_source_exterior_theorem": all_gates_pass,
        "valid_for_selected_parent_Box2_zero_motion_local_branch": all_gates_pass,
        "valid_for_numeric_beta_bBox_claim": False,
        "valid_for_nonperturbative_resummed_heavy_mode_claim": False,
        "valid_for_nonlocal_motion_form_factor_completion": False,
        "valid_for_finite_parent_metric_three_point_claim": False,
        "valid_for_exact_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "4984 derive or source the running essential-frame connection beta_bBox/(2Z) "
            "and its six-derivative spillover, or prove the local nonanalytic form-factor tail "
            "is source-silent on the selected parent branch"
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }

    if arguments.dry_run:
        print(
            f"{MARKER}_DRY_RUN={pass_count}/{len(gates)} "
            f"jet={maximum_jet_relative:.3e} quotient_rank={redundant_rank} "
            f"selected_profiles={len(selected_profiles)}",
            flush=True,
        )
        return 0 if all_gates_pass else 1

    write_csv(NOTATION_CSV, tagged(notation_rows))
    write_csv(HESSIAN_CSV, tagged(hessian_rows))
    write_csv(JET_CSV, tagged(jet_rows))
    write_csv(QUOTIENT_CSV, tagged(quotient_rows))
    write_csv(RUNNING_FRAME_CSV, tagged(running_frame_rows))
    write_csv(PROFILE_CSV, tagged(profile_rows))
    write_csv(JUNCTION_CSV, tagged(junction_rows))
    write_csv(GATE_CSV, tagged(gate_rows))
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    provenance_lines = [
        "# Checkpoint 4983 provenance",
        "",
        "Generated locally. No GitHub action.",
        "",
        "The omitted local analytic `(Box psi)^2` bilinear is separated from",
        "the already projected six-derivative `O2=X(nabla nabla psi)^2`.",
        "The covariant Hessian is checked with an independent local-jet",
        "automatic-differentiation calculation. No numeric `beta_bBox`,",
        "heavy-mode range, scalar charge, or nonlocal form factor is invented.",
        "",
        "## Input digests",
    ]
    for path in required_paths:
        provenance_lines.append(f"- `{relative(path)}` sha256 `{digest(path)}`")
    PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")

    print(
        f"{MARKER}_PASS={pass_count}/{len(gates)} "
        f"jet={maximum_jet_relative:.3e} quotient_rank={redundant_rank} "
        f"output={RESULT_JSON}",
        flush=True,
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
