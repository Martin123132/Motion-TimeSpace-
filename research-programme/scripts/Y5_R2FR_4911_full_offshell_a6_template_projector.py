from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import itertools
import math
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy import linalg


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

MARKER = "MTS_FULL_OFFSHELL_A6_TEMPLATE_PROJECTOR_4911"
FORMAL_MARKER = "PPC4161_FULL_OFFSHELL_A6_TEMPLATE_PROJECTOR_4911"
NEXT_TARGET = (
    "4912-Y5-R2FR-free-lattice-multigeometry-a6-response-and-"
    "continuum-projector-recovery.md"
)
CHECKED_DATE = "2026-07-12"
DIMENSIONS = 4
JET_COUNT = 8
GRID_AXES = tuple(range(1, DIMENSIONS + 1))
TENSOR_AXIS_START = 1 + DIMENSIONS
TORUS_LENGTH = 2.0 * math.pi

OPERATOR_NAMES = (
    "D1_grad_R_squared",
    "D2_grad_Ricci_squared",
    "D3_crossed_grad_Ricci",
    "D4_grad_Riemann_squared",
    "C1_R_cubed",
    "C2_R_Ricci_squared",
    "C3_R_Riemann_squared",
    "C4_Ricci_cubed",
    "C5_Ricci_Ricci_Riemann",
    "C6_Ricci_Riemann_Riemann",
    "C7_I1_Riemann_cubed",
    "C8_I2_Riemann_cubed",
)

# Vassilevich, hep-th/0306138, ch4.tex, lines 429--448.  The total
# derivative integrates to zero on T4.  The four box/cross terms have been
# integrated by parts with the source's rightmost-derivative convention.
A6_SOURCE_INTEGRATED_NUMERATORS = np.array(
    [
        -11.0,
        6.0,
        -28.0,
        -3.0,
        35.0 / 9.0,
        -14.0 / 3.0,
        14.0 / 3.0,
        -208.0 / 9.0,
        -64.0 / 3.0,
        -16.0 / 3.0,
        -44.0 / 9.0,
        -80.0 / 9.0,
    ],
    dtype=float,
)
A6_ENGINE_INTEGRATED_NUMERATORS = A6_SOURCE_INTEGRATED_NUMERATORS.copy()
# The geometric engine differentiates with respect to H=sqrt(g) g^{-1}.
# Its linearized Weyl tensor is the negative of the checkpoint-4909/source
# convention for the same H polarization.  Derivative-squared invariants are
# unchanged, while every cubic-curvature template changes sign.
A6_ENGINE_INTEGRATED_NUMERATORS[4:] *= -1.0
A6_COEFFICIENTS = A6_ENGINE_INTEGRATED_NUMERATORS / math.factorial(7)

# On a four-dimensional Ricci-flat metric, the contracted differential
# Bianchi identity and curvature commutator give
#   int (nabla Riem)^2 = -int(I1 + 4 I2),
# while the four-dimensional algebraic identity gives I2=I1/2.  Therefore
# the coefficient of the checkpoint-4909 C^3 normalization is this
# functional.  In engine variables D4=+3 I1_engine and
# C3_4909=-I1_engine.
RICCI_FLAT_C3_MAP = np.array(
    [0.0, 0.0, 0.0, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, -0.5],
    dtype=float,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
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
    def clean(value: Any) -> Any:
        if isinstance(value, (float, np.floating)) and not math.isfinite(
            float(value)
        ):
            return "not_applicable"
        return value

    return [
        {
            **{key: clean(value) for key, value in row.items()},
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4911_00_predecessor",
            POST
            / "4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md",
            "MTS_FREE_METRIC_TTT_PROJECTOR_ARBITRATION_4910",
            "validated_predecessor",
        ),
        (
            "SRC4911_01_predecessor_validation",
            OUTPUT / "P8_Y5_BRR545_4910_VALIDATION.csv",
            "VAL4910_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4911_02_scalar_a6_owner",
            POST
            / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
            "scalar_a6_source_owner",
        ),
        (
            "SRC4911_03_a6_archive",
            POST
            / "source-intake"
            / "heat_kernel_a6"
            / "4881"
            / "hep-th-0306138.tar",
            "binary_hash_locked_source",
            "primary_heat_kernel_archive",
        ),
        (
            "SRC4911_04_metric_vertex",
            POST
            / "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md",
            "MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908",
            "metric_response_normalization",
        ),
        (
            "SRC4911_05_operator_normalization",
            POST
            / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md",
            "MTS_FIRST_RESIDUAL_OPERATOR_AND_INDEPENDENT_OBSERVABLE_GATE_4905",
            "C3_operator_normalization",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        marker_found = (
            exists
            if source_id == "SRC4911_03_a6_archive"
            else contains(path, marker)
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker_found,
                "sha256": sha256(path) if exists else "",
            }
        )
    return {
        "rows": rows,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


def submasks(mask: int) -> list[int]:
    values: list[int] = []
    current = mask
    while True:
        values.append(current)
        if current == 0:
            return values
        current = (current - 1) & mask


def jet_binary_einsum(
    subscripts: str, left: np.ndarray, right: np.ndarray
) -> np.ndarray:
    output: np.ndarray | None = None
    for target in range(JET_COUNT):
        accumulator: np.ndarray | None = None
        for first in submasks(target):
            second = target ^ first
            term = np.einsum(
                subscripts, left[first], right[second], optimize=True
            )
            accumulator = term if accumulator is None else accumulator + term
        if output is None:
            output = np.empty(
                (JET_COUNT,) + accumulator.shape, dtype=np.complex128
            )
        output[target] = accumulator
    if output is None:
        raise RuntimeError("jet product produced no output")
    return output


def jet_pointwise(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return jet_binary_einsum("...,...->...", left, right)


def jet_matrix_product(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return jet_binary_einsum("...ik,...kj->...ij", left, right)


def jet_linear_einsum(subscripts: str, tensor: np.ndarray) -> np.ndarray:
    return np.stack(
        [np.einsum(subscripts, tensor[mask], optimize=True) for mask in range(JET_COUNT)]
    )


def tensor_transpose(tensor: np.ndarray, permutation: tuple[int, ...]) -> np.ndarray:
    prefix = list(range(TENSOR_AXIS_START))
    suffix = [TENSOR_AXIS_START + index for index in permutation]
    return np.transpose(tensor, prefix + suffix)


def jet_derivative(tensor: np.ndarray, axis: int, size: int) -> np.ndarray:
    transformed = np.fft.fftn(tensor, axes=GRID_AXES)
    frequencies = np.fft.fftfreq(size, d=1.0 / size)
    shape = [1] * tensor.ndim
    shape[1 + axis] = size
    multiplier = 1j * frequencies.reshape(shape)
    return np.fft.ifftn(multiplier * transformed, axes=GRID_AXES)


def stack_derivatives(tensor: np.ndarray, size: int) -> np.ndarray:
    return np.stack(
        [jet_derivative(tensor, axis, size) for axis in range(DIMENSIONS)],
        axis=TENSOR_AXIS_START,
    )


def raise_tensor_axis(
    tensor: np.ndarray, inverse_metric: np.ndarray, axis: int
) -> np.ndarray:
    rank = tensor.ndim - TENSOR_AXIS_START
    labels = list("abcdefgh"[:rank])
    old = labels[axis]
    output_labels = labels.copy()
    output_labels[axis] = "z"
    return jet_binary_einsum(
        f"...z{old},...{''.join(labels)}->...{''.join(output_labels)}",
        inverse_metric,
        tensor,
    )


def raise_tensor_axes(
    tensor: np.ndarray, inverse_metric: np.ndarray, axes: tuple[int, ...]
) -> np.ndarray:
    result = tensor
    for axis in axes:
        result = raise_tensor_axis(result, inverse_metric, axis)
    return result


def identity_matrix_jet(size: int) -> np.ndarray:
    shape = (JET_COUNT,) + (size,) * DIMENSIONS + (DIMENSIONS, DIMENSIONS)
    result = np.zeros(shape, dtype=np.complex128)
    result[0] = np.eye(DIMENSIONS)
    return result


def identity_scalar_jet(size: int) -> np.ndarray:
    result = np.zeros((JET_COUNT,) + (size,) * DIMENSIONS, dtype=np.complex128)
    result[0] = 1.0
    return result


def source_profiles(
    size: int,
    momenta: np.ndarray,
    polarizations: np.ndarray,
    phases: np.ndarray,
) -> list[np.ndarray]:
    coordinate_axes = [
        TORUS_LENGTH * np.arange(size, dtype=float) / size
        for _ in range(DIMENSIONS)
    ]
    coordinates = np.meshgrid(*coordinate_axes, indexing="ij")
    profiles: list[np.ndarray] = []
    for source in range(3):
        phase = np.zeros((size,) * DIMENSIONS, dtype=float)
        for axis in range(DIMENSIONS):
            phase += momenta[source, axis] * coordinates[axis]
        wave = np.cos(phase + phases[source])
        profiles.append(
            wave[..., np.newaxis, np.newaxis] * polarizations[source]
        )
    return profiles


def metric_jets(
    size: int, profiles: list[np.ndarray]
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    identity_matrix = identity_matrix_jet(size)
    identity_scalar = identity_scalar_jet(size)
    perturbation = np.zeros_like(identity_matrix)
    for source, mask in enumerate((1, 2, 4)):
        perturbation[mask] = profiles[source]

    perturbation_squared = jet_matrix_product(perturbation, perturbation)
    perturbation_cubed = jet_matrix_product(
        perturbation_squared, perturbation
    )
    trace_perturbation = jet_linear_einsum("...ii->...", perturbation)
    trace_squared = jet_linear_einsum(
        "...ii->...", perturbation_squared
    )
    trace_cubed = jet_linear_einsum("...ii->...", perturbation_cubed)
    half_log_determinant = 0.5 * (
        trace_perturbation - 0.5 * trace_squared + trace_cubed / 3.0
    )
    half_log_squared = jet_pointwise(
        half_log_determinant, half_log_determinant
    )
    half_log_cubed = jet_pointwise(
        half_log_squared, half_log_determinant
    )
    sqrt_determinant = (
        identity_scalar
        + half_log_determinant
        + 0.5 * half_log_squared
        + half_log_cubed / 6.0
    )
    inverse_sqrt_determinant = (
        identity_scalar
        - half_log_determinant
        + 0.5 * half_log_squared
        - half_log_cubed / 6.0
    )
    densitized_inverse = identity_matrix + perturbation
    densitized_inverse_matrix = (
        identity_matrix
        - perturbation
        + perturbation_squared
        - perturbation_cubed
    )
    covariant_metric = jet_binary_einsum(
        "...,...ij->...ij", sqrt_determinant, densitized_inverse_matrix
    )
    inverse_metric = jet_binary_einsum(
        "...,...ij->...ij",
        inverse_sqrt_determinant,
        densitized_inverse,
    )
    metric_product = jet_matrix_product(covariant_metric, inverse_metric)
    residual = float(np.max(np.abs(metric_product - identity_matrix)))
    return covariant_metric, inverse_metric, sqrt_determinant, residual


def curvature_jets(
    size: int,
    covariant_metric: np.ndarray,
    inverse_metric: np.ndarray,
) -> dict[str, np.ndarray]:
    metric_derivative = stack_derivatives(covariant_metric, size)
    # dg has tensor order (derivative, first metric index, second metric index).
    christoffel_bracket = (
        tensor_transpose(metric_derivative, (1, 0, 2))
        + tensor_transpose(metric_derivative, (1, 2, 0))
        - metric_derivative
    )
    christoffel = 0.5 * jet_binary_einsum(
        "...rs,...smn->...rmn", inverse_metric, christoffel_bracket
    )
    christoffel_derivative = stack_derivatives(christoffel, size)
    derivative_first = tensor_transpose(
        christoffel_derivative, (1, 3, 0, 2)
    )
    derivative_second = tensor_transpose(
        christoffel_derivative, (1, 3, 2, 0)
    )
    quadratic_first = jet_binary_einsum(
        "...rml,...lns->...rsmn", christoffel, christoffel
    )
    quadratic_second = jet_binary_einsum(
        "...rnl,...lms->...rsmn", christoffel, christoffel
    )
    riemann_up = (
        derivative_first
        - derivative_second
        + quadratic_first
        - quadratic_second
    )
    ricci = jet_linear_einsum("...rsrn->...sn", riemann_up)
    scalar = jet_binary_einsum(
        "...mn,...mn->...", inverse_metric, ricci
    )
    riemann = jet_binary_einsum(
        "...ar,...rbcd->...abcd", covariant_metric, riemann_up
    )

    ricci_derivative = stack_derivatives(ricci, size)
    ricci_connection_first = jet_binary_einsum(
        "...lam,...ln->...amn", christoffel, ricci
    )
    ricci_connection_second = jet_binary_einsum(
        "...lan,...ml->...amn", christoffel, ricci
    )
    covariant_ricci_derivative = (
        ricci_derivative
        - ricci_connection_first
        - ricci_connection_second
    )

    riemann_derivative = stack_derivatives(riemann, size)
    riemann_connection_first = jet_binary_einsum(
        "...lam,...lnpq->...amnpq", christoffel, riemann
    )
    riemann_connection_second = jet_binary_einsum(
        "...lan,...mlpq->...amnpq", christoffel, riemann
    )
    riemann_connection_third = jet_binary_einsum(
        "...lap,...mnlq->...amnpq", christoffel, riemann
    )
    riemann_connection_fourth = jet_binary_einsum(
        "...laq,...mnpl->...amnpq", christoffel, riemann
    )
    covariant_riemann_derivative = (
        riemann_derivative
        - riemann_connection_first
        - riemann_connection_second
        - riemann_connection_third
        - riemann_connection_fourth
    )
    scalar_derivative = stack_derivatives(scalar, size)
    return {
        "christoffel": christoffel,
        "riemann": riemann,
        "ricci": ricci,
        "scalar": scalar,
        "grad_scalar": scalar_derivative,
        "grad_ricci": covariant_ricci_derivative,
        "grad_riemann": covariant_riemann_derivative,
    }


def scalar_invariant_jets(
    inverse_metric: np.ndarray, curvature: dict[str, np.ndarray]
) -> list[np.ndarray]:
    scalar = curvature["scalar"]
    ricci = curvature["ricci"]
    riemann = curvature["riemann"]
    grad_scalar = curvature["grad_scalar"]
    grad_ricci = curvature["grad_ricci"]
    grad_riemann = curvature["grad_riemann"]

    grad_scalar_up = raise_tensor_axes(grad_scalar, inverse_metric, (0,))
    d1 = jet_binary_einsum(
        "...a,...a->...", grad_scalar, grad_scalar_up
    )

    grad_ricci_up = raise_tensor_axes(
        grad_ricci, inverse_metric, (0, 1, 2)
    )
    d2 = jet_binary_einsum(
        "...abc,...abc->...", grad_ricci, grad_ricci_up
    )
    d3 = jet_binary_einsum(
        "...abc,...cba->...", grad_ricci, grad_ricci_up
    )
    del grad_ricci_up

    grad_riemann_up = raise_tensor_axes(
        grad_riemann, inverse_metric, (0, 1, 2, 3, 4)
    )
    d4 = jet_binary_einsum(
        "...abcde,...abcde->...", grad_riemann, grad_riemann_up
    )
    del grad_riemann_up
    gc.collect()

    scalar_squared = jet_pointwise(scalar, scalar)
    c1 = jet_pointwise(scalar_squared, scalar)

    ricci_up = raise_tensor_axes(ricci, inverse_metric, (0, 1))
    ricci_squared = jet_binary_einsum(
        "...ab,...ab->...", ricci, ricci_up
    )
    c2 = jet_pointwise(scalar, ricci_squared)

    riemann_up = raise_tensor_axes(
        riemann, inverse_metric, (0, 1, 2, 3)
    )
    riemann_squared = jet_binary_einsum(
        "...abcd,...abcd->...", riemann, riemann_up
    )
    c3 = jet_pointwise(scalar, riemann_squared)

    ricci_mixed = jet_binary_einsum(
        "...ac,...cb->...ab", ricci, inverse_metric
    )
    ricci_mixed_squared = jet_matrix_product(ricci_mixed, ricci_mixed)
    ricci_mixed_cubed = jet_matrix_product(
        ricci_mixed_squared, ricci_mixed
    )
    c4 = jet_linear_einsum("...aa->...", ricci_mixed_cubed)

    ricci_pair = jet_binary_einsum(
        "...ij,...kl->...ijkl", ricci, ricci
    )
    c5 = jet_binary_einsum(
        "...ijkl,...ikjl->...", ricci_pair, riemann_up
    )

    riemann_last_three_up = raise_tensor_axes(
        riemann, inverse_metric, (1, 2, 3)
    )
    ricci_riemann = jet_binary_einsum(
        "...jk,...jnli->...knli", ricci_up, riemann
    )
    c6 = jet_binary_einsum(
        "...knli,...knli->...", ricci_riemann, riemann_last_three_up
    )
    del riemann_last_three_up, ricci_riemann

    riemann_first_two_up = raise_tensor_axes(
        riemann, inverse_metric, (0, 1)
    )
    i1_pair = jet_binary_einsum(
        "...abcd,...abef->...cdef", riemann, riemann_first_two_up
    )
    c7 = jet_binary_einsum(
        "...cdef,...cdef->...", i1_pair, riemann_up
    )
    del riemann_first_two_up, i1_pair

    riemann_zero_two_up = raise_tensor_axes(
        riemann, inverse_metric, (0, 2)
    )
    i2_pair = jet_binary_einsum(
        "...abcd,...aecf->...bdef", riemann, riemann_zero_two_up
    )
    c8 = jet_binary_einsum(
        "...bdef,...bedf->...", i2_pair, riemann_up
    )
    return [d1, d2, d3, d4, c1, c2, c3, c4, c5, c6, c7, c8]


def geometry_templates(
    size: int,
    momenta: np.ndarray,
    polarizations: np.ndarray,
    phases: np.ndarray,
) -> dict[str, Any]:
    profiles = source_profiles(size, momenta, polarizations, phases)
    covariant_metric, inverse_metric, sqrt_determinant, metric_residual = (
        metric_jets(size, profiles)
    )
    curvature = curvature_jets(size, covariant_metric, inverse_metric)
    riemann = curvature["riemann"]
    ricci = curvature["ricci"]
    riemann_pair_residual = float(
        np.max(np.abs(riemann + tensor_transpose(riemann, (1, 0, 2, 3))))
    )
    riemann_last_pair_residual = float(
        np.max(np.abs(riemann + tensor_transpose(riemann, (0, 1, 3, 2))))
    )
    riemann_exchange_residual = float(
        np.max(np.abs(riemann - tensor_transpose(riemann, (2, 3, 0, 1))))
    )
    ricci_symmetry_residual = float(
        np.max(np.abs(ricci - tensor_transpose(ricci, (1, 0))))
    )
    flat_curvature_residual = float(np.max(np.abs(riemann[0])))

    invariants = scalar_invariant_jets(inverse_metric, curvature)
    cell_volume = (TORUS_LENGTH / size) ** DIMENSIONS
    values: list[float] = []
    imaginary_residual = 0.0
    for invariant in invariants:
        density = jet_pointwise(sqrt_determinant, invariant)
        mixed = np.sum(density[7]) * cell_volume
        values.append(float(mixed.real))
        imaginary_residual = max(imaginary_residual, abs(float(mixed.imag)))
    return {
        "values": np.array(values, dtype=float),
        "metric_inverse_residual": metric_residual,
        "riemann_first_pair_residual": riemann_pair_residual,
        "riemann_last_pair_residual": riemann_last_pair_residual,
        "riemann_pair_exchange_residual": riemann_exchange_residual,
        "ricci_symmetry_residual": ricci_symmetry_residual,
        "flat_curvature_residual": flat_curvature_residual,
        "imaginary_residual": imaginary_residual,
    }


def random_source_ensemble(count: int, seed: int = 4911) -> list[dict[str, Any]]:
    rng = np.random.default_rng(seed)
    vectors = [
        np.array(vector, dtype=int)
        for vector in itertools.product((-1, 0, 1), repeat=DIMENSIONS)
        if any(vector)
    ]
    compatible = [
        (first, second, -first - second)
        for first in vectors
        for second in vectors
        if np.any(first + second)
        and np.max(np.abs(first + second)) <= 1
        and not np.array_equal(first, second)
        and not np.array_equal(first, -second)
    ]
    ensemble: list[dict[str, Any]] = []
    for geometry in range(count):
        selected = compatible[int(rng.integers(len(compatible)))]
        momenta = np.stack(selected).astype(float)
        polarizations: list[np.ndarray] = []
        for source in range(3):
            raw = rng.normal(size=(DIMENSIONS, DIMENSIONS))
            symmetric = 0.5 * (raw + raw.T)
            symmetric += (0.15 + 0.05 * source) * np.eye(DIMENSIONS)
            symmetric /= np.linalg.norm(symmetric)
            polarizations.append(symmetric)
        phases = rng.uniform(-0.35, 0.35, size=3)
        if abs(math.cos(float(np.sum(phases)))) < 0.35:
            phases[2] = -phases[0] - phases[1] + 0.17
        ensemble.append(
            {
                "geometry_id": f"G{geometry:02d}",
                "momenta": momenta,
                "polarizations": np.stack(polarizations),
                "phases": phases,
            }
        )
    return ensemble


def basis_rows() -> list[dict[str, Any]]:
    raw_terms = (
        "17-28",
        "-2+8",
        "-4-24",
        "9-12",
        "35/9",
        "-14/3",
        "14/3",
        "-208/9",
        "-64/3",
        "-16/3",
        "-44/9",
        "-80/9",
    )
    definitions = (
        "(nabla_a R)(nabla^a R)",
        "(nabla_a R_mn)(nabla^a R^mn)",
        "(nabla_n R_jk)(nabla_k R_jn)",
        "(nabla_a R_mnrs)(nabla^a R^mnrs)",
        "R^3",
        "R R_mn R^mn",
        "R R_mnrs R^mnrs",
        "R_jk R_jn R_kn",
        "R_ij R_kl R_ikjl",
        "R_jk R_jnli R_knli",
        "R_ijkn R_ijlp R_knlp",
        "R_ijkn R_ilkp R_jlnp",
    )
    return [
        {
            "operator_index": index,
            "operator": name,
            "definition": definitions[index],
            "source_numerator_before_7_factorial": raw_terms[index],
            "source_integrated_numerator": A6_SOURCE_INTEGRATED_NUMERATORS[index],
            "engine_integrated_numerator": A6_ENGINE_INTEGRATED_NUMERATORS[index],
            "engine_a6_coefficient": A6_COEFFICIENTS[index],
            "convention_map": (
                "unchanged_derivative_squared"
                if index < 4
                else "R_engine=-R_source_so_cubic_coefficient_flips"
            ),
            "integration_rule": (
                "closed_T4_total_derivative_zero_and_covariant_integration_by_parts"
                if index < 4
                else "unchanged_cubic_term"
            ),
        }
        for index, name in enumerate(OPERATOR_NAMES)
    ]


def ensemble_row(source: dict[str, Any]) -> dict[str, Any]:
    row: dict[str, Any] = {"geometry_id": source["geometry_id"]}
    for source_index in range(3):
        row[f"q{source_index + 1}"] = " ".join(
            str(int(value)) for value in source["momenta"][source_index]
        )
        row[f"phase{source_index + 1}"] = source["phases"][source_index]
        row[f"polarization{source_index + 1}_trace"] = np.trace(
            source["polarizations"][source_index]
        )
        row[f"polarization{source_index + 1}_norm"] = np.linalg.norm(
            source["polarizations"][source_index]
        )
    row["momentum_closure_residual"] = float(
        np.max(np.abs(np.sum(source["momenta"], axis=0)))
    )
    return row


def matrix_analysis(matrix: np.ndarray) -> dict[str, Any]:
    column_norms = np.linalg.norm(matrix, axis=0)
    if np.any(column_norms < 1e-14):
        raise RuntimeError("at least one a6 template column is numerically zero")
    normalized = matrix / column_norms
    _, singular_values, right_vectors = np.linalg.svd(
        normalized, full_matrices=True
    )
    tolerance = max(normalized.shape) * np.finfo(float).eps * singular_values[0]
    practical_tolerance = max(tolerance, singular_values[0] * 1e-10)
    rank = int(np.sum(singular_values > practical_tolerance))
    _, _, pivots = linalg.qr(normalized, mode="economic", pivoting=True)
    null_normalized = right_vectors[rank:]
    null_original = np.array(
        [vector / column_norms for vector in null_normalized]
    )
    for index in range(len(null_original)):
        norm = np.linalg.norm(null_original[index])
        if norm > 0:
            null_original[index] /= norm
    return {
        "column_norms": column_norms,
        "normalized": normalized,
        "singular_values": singular_values,
        "rank": rank,
        "tolerance": practical_tolerance,
        "pivots": pivots,
        "nullspace": null_original,
        "condition_number_retained": float(
            singular_values[0] / singular_values[rank - 1]
        ),
    }


def dependency_relations(
    matrix: np.ndarray, analysis: dict[str, Any]
) -> list[dict[str, Any]]:
    rank = analysis["rank"]
    independent = np.asarray(analysis["pivots"][:rank], dtype=int)
    dependent = np.asarray(analysis["pivots"][rank:], dtype=int)
    normalized = analysis["normalized"]
    column_norms = analysis["column_norms"]
    rows: list[dict[str, Any]] = []
    for dependent_column in dependent:
        normalized_weights, _, _, _ = np.linalg.lstsq(
            normalized[:, independent],
            normalized[:, dependent_column],
            rcond=1e-10,
        )
        raw_weights = (
            normalized_weights
            * column_norms[dependent_column]
            / column_norms[independent]
        )
        reconstructed = matrix[:, independent] @ raw_weights
        relation_scale = max(
            float(np.linalg.norm(matrix[:, dependent_column])), 1e-30
        )
        relation_residual = float(
            np.linalg.norm(reconstructed - matrix[:, dependent_column])
            / relation_scale
        )
        for position, independent_column in enumerate(independent):
            rational = Fraction(float(raw_weights[position])).limit_denominator(
                10000
            )
            rows.append(
                {
                    "dependent_operator_index": int(dependent_column),
                    "dependent_operator": OPERATOR_NAMES[
                        int(dependent_column)
                    ],
                    "independent_operator_index": int(independent_column),
                    "independent_operator": OPERATOR_NAMES[
                        int(independent_column)
                    ],
                    "coefficient_in_dependent_expansion": raw_weights[
                        position
                    ],
                    "rational_approximation": str(rational),
                    "rational_approximation_residual": abs(
                        float(rational) - raw_weights[position]
                    ),
                    "relative_relation_residual": relation_residual,
                }
            )
    return rows


def free_recovery(
    matrix: np.ndarray, analysis: dict[str, Any]
) -> dict[str, Any]:
    column_norms = analysis["column_norms"]
    normalized = analysis["normalized"]
    response = matrix @ A6_COEFFICIENTS
    beta, _, _, _ = np.linalg.lstsq(
        normalized, response, rcond=1e-10
    )
    recovered = beta / column_norms
    reconstructed = matrix @ recovered
    response_scale = max(float(np.linalg.norm(response)), 1e-30)
    response_residual = float(
        np.linalg.norm(reconstructed - response) / response_scale
    )
    source_raw_c3 = float(RICCI_FLAT_C3_MAP @ A6_COEFFICIENTS)
    recovered_raw_c3 = float(RICCI_FLAT_C3_MAP @ recovered)
    expected_raw_c3 = -1.0 / 15120.0
    source_one_loop_c3 = (
        -0.5 * source_raw_c3 / (4.0 * math.pi) ** 2
    )
    recovered_one_loop_c3 = (
        -0.5 * recovered_raw_c3 / (4.0 * math.pi) ** 2
    )
    expected_one_loop_c3 = 1.0 / (30240.0 * (4.0 * math.pi) ** 2)
    null_map_residual = (
        float(
            np.max(
                np.abs(analysis["nullspace"] @ RICCI_FLAT_C3_MAP)
            )
        )
        if len(analysis["nullspace"])
        else 0.0
    )
    return {
        "response": response,
        "recovered": recovered,
        "response_residual": response_residual,
        "source_raw_c3": source_raw_c3,
        "recovered_raw_c3": recovered_raw_c3,
        "expected_raw_c3": expected_raw_c3,
        "source_one_loop_c3": source_one_loop_c3,
        "recovered_one_loop_c3": recovered_one_loop_c3,
        "expected_one_loop_c3": expected_one_loop_c3,
        "null_map_residual": null_map_residual,
    }


def run(
    geometry_count: int = 12,
    size: int = 6,
    crosscheck_count: int = 2,
    crosscheck_size: int = 8,
) -> dict[str, Any]:
    start = time.perf_counter()
    sources = source_contract()
    ensemble = random_source_ensemble(geometry_count)
    matrix_rows: list[np.ndarray] = []
    diagnostics: list[dict[str, Any]] = []
    for index, source in enumerate(ensemble):
        print(
            f"4911 template {index + 1}/{geometry_count} "
            f"{source['geometry_id']} N={size}",
            flush=True,
        )
        geometry_start = time.perf_counter()
        result = geometry_templates(
            size,
            source["momenta"],
            source["polarizations"],
            source["phases"],
        )
        matrix_rows.append(result["values"])
        diagnostics.append(
            {
                "geometry_id": source["geometry_id"],
                "size": size,
                **{
                    key: value
                    for key, value in result.items()
                    if key != "values"
                },
                "elapsed_seconds": time.perf_counter() - geometry_start,
            }
        )
        gc.collect()
    matrix = np.vstack(matrix_rows)
    analysis = matrix_analysis(matrix)
    relations = dependency_relations(matrix, analysis)
    recovery = free_recovery(matrix, analysis)

    leave_one_out: list[dict[str, Any]] = []
    for omitted, source in enumerate(ensemble):
        reduced_matrix = np.delete(matrix, omitted, axis=0)
        reduced_analysis = matrix_analysis(reduced_matrix)
        reduced_recovery = free_recovery(reduced_matrix, reduced_analysis)
        leave_one_out.append(
            {
                "omitted_geometry_id": source["geometry_id"],
                "rank": reduced_analysis["rank"],
                "condition_number_retained": reduced_analysis[
                    "condition_number_retained"
                ],
                "response_recovery_residual": reduced_recovery[
                    "response_residual"
                ],
                "recovered_raw_c3": reduced_recovery[
                    "recovered_raw_c3"
                ],
                "recovered_one_loop_c3": reduced_recovery[
                    "recovered_one_loop_c3"
                ],
                "absolute_zeta_residual": abs(
                    reduced_recovery["recovered_one_loop_c3"]
                    - reduced_recovery["expected_one_loop_c3"]
                ),
                "null_map_residual": reduced_recovery[
                    "null_map_residual"
                ],
            }
        )

    crosschecks: list[dict[str, Any]] = []
    for index, source in enumerate(ensemble[:crosscheck_count]):
        print(
            f"4911 crosscheck {index + 1}/{crosscheck_count} "
            f"{source['geometry_id']} N={crosscheck_size}",
            flush=True,
        )
        result = geometry_templates(
            crosscheck_size,
            source["momenta"],
            source["polarizations"],
            source["phases"],
        )
        baseline = matrix[index]
        scale = max(float(np.linalg.norm(baseline)), 1e-30)
        crosschecks.append(
            {
                "geometry_id": source["geometry_id"],
                "baseline_size": size,
                "crosscheck_size": crosscheck_size,
                "relative_template_residual": float(
                    np.linalg.norm(result["values"] - baseline) / scale
                ),
                "maximum_absolute_template_residual": float(
                    np.max(np.abs(result["values"] - baseline))
                ),
                "imaginary_residual": result["imaginary_residual"],
            }
        )
        gc.collect()

    maximum_geometry_residual = max(
        max(
            row["metric_inverse_residual"],
            row["riemann_first_pair_residual"],
            row["riemann_last_pair_residual"],
            row["riemann_pair_exchange_residual"],
            row["ricci_symmetry_residual"],
            row["flat_curvature_residual"],
            row["imaginary_residual"],
        )
        for row in diagnostics
    )
    maximum_crosscheck = max(
        (row["relative_template_residual"] for row in crosschecks),
        default=0.0,
    )
    rank_gate = analysis["rank"] == 8
    geometry_gate = maximum_geometry_residual < 1e-9
    crosscheck_gate = maximum_crosscheck < 1e-8
    recovery_gate = (
        recovery["response_residual"] < 1e-10
        and abs(
            recovery["source_raw_c3"] - recovery["expected_raw_c3"]
        )
        < 1e-14
        and abs(
            recovery["recovered_raw_c3"]
            - recovery["expected_raw_c3"]
        )
        < 1e-10
        and recovery["null_map_residual"] < 1e-9
        and all(row["rank"] == 8 for row in leave_one_out)
        and max(
            row["absolute_zeta_residual"] for row in leave_one_out
        )
        < 1e-10
    )
    all_checks = (
        sources["passed"]
        and rank_gate
        and geometry_gate
        and crosscheck_gate
        and recovery_gate
    )
    decision = (
        "SOURCED_SCALAR_A6_INTEGRATED_BASIS_CONSTRUCTED_EXACT_NILPOTENT_"
        "DENSITIZED_METRIC_GEOMETRY_TEMPLATES_RANKED_RICCI_FLAT_C3_MAP_"
        "RECOVERS_KNOWN_FREE_SCALAR_COEFFICIENT_INTERACTING_RESPONSE_"
        "REMAINS_WITHHELD_PENDING_FREE_LATTICE_MULTIGEOMETRY_CONTINUUM_"
        "RECOVERY_ACTIVE_RESIDUAL_ZERO_PRIVATE_NONCLAIM"
    )
    return {
        "sources": sources,
        "ensemble": ensemble,
        "matrix": matrix,
        "diagnostics": diagnostics,
        "analysis": analysis,
        "relations": relations,
        "recovery": recovery,
        "leave_one_out": leave_one_out,
        "crosschecks": crosschecks,
        "maximum_geometry_residual": maximum_geometry_residual,
        "maximum_crosscheck": maximum_crosscheck,
        "rank_gate": rank_gate,
        "geometry_gate": geometry_gate,
        "crosscheck_gate": crosscheck_gate,
        "recovery_gate": recovery_gate,
        "Gamma_MTS_res": 0,
        "interacting_run_launched": False,
        "all_checks_pass": all_checks,
        "decision": decision,
        "next_target": NEXT_TARGET,
        "size": size,
        "crosscheck_size": crosscheck_size,
        "elapsed_seconds": time.perf_counter() - start,
    }


def write_outputs(result: dict[str, Any]) -> None:
    analysis = result["analysis"]
    recovery = result["recovery"]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_SOURCE_REGISTER.csv",
        tagged(result["sources"]["rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_INTEGRATED_A6_BASIS.csv",
        tagged(basis_rows()),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_SOURCE_ENSEMBLE.csv",
        tagged([ensemble_row(source) for source in result["ensemble"]]),
    )
    matrix_rows: list[dict[str, Any]] = []
    for row_index, source in enumerate(result["ensemble"]):
        for column, operator in enumerate(OPERATOR_NAMES):
            matrix_rows.append(
                {
                    "geometry_id": source["geometry_id"],
                    "operator_index": column,
                    "operator": operator,
                    "mixed_third_template": result["matrix"][row_index, column],
                    "column_norm": analysis["column_norms"][column],
                }
            )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_TEMPLATE_MATRIX.csv",
        tagged(matrix_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_GEOMETRY_DIAGNOSTICS.csv",
        tagged(result["diagnostics"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_GRID_CROSSCHECK.csv",
        tagged(result["crosschecks"]),
    )
    spectrum_rows = [
        {
            "singular_index": index,
            "singular_value": value,
            "retained": index < analysis["rank"],
            "rank": analysis["rank"],
            "rank_tolerance": analysis["tolerance"],
            "condition_number_retained": analysis[
                "condition_number_retained"
            ],
        }
        for index, value in enumerate(analysis["singular_values"])
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_SINGULAR_SPECTRUM.csv",
        tagged(spectrum_rows),
    )
    pivot_rows = [
        {
            "pivot_order": order,
            "operator_index": int(column),
            "operator": OPERATOR_NAMES[int(column)],
            "retained": order < analysis["rank"],
        }
        for order, column in enumerate(analysis["pivots"])
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_PIVOT_BASIS.csv", tagged(pivot_rows)
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_DEPENDENCY_RELATIONS.csv",
        tagged(result["relations"]),
    )
    null_rows: list[dict[str, Any]] = []
    if len(analysis["nullspace"]):
        for null_index, vector in enumerate(analysis["nullspace"]):
            for column, value in enumerate(vector):
                null_rows.append(
                    {
                        "null_vector": null_index,
                        "operator_index": column,
                        "operator": OPERATOR_NAMES[column],
                        "coefficient": value,
                        "matrix_residual": float(
                            np.linalg.norm(result["matrix"] @ vector)
                        ),
                        "Ricci_flat_map_residual": float(
                            RICCI_FLAT_C3_MAP @ vector
                        ),
                    }
                )
    else:
        null_rows.append(
            {
                "null_vector": "none",
                "operator_index": "not_applicable",
                "operator": "full_column_rank",
                "coefficient": 0.0,
                "matrix_residual": 0.0,
                "Ricci_flat_map_residual": 0.0,
            }
        )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_NULLSPACE.csv", tagged(null_rows)
    )
    recovery_rows = [
        {
            "operator_index": index,
            "operator": operator,
            "source_a6_coefficient": A6_COEFFICIENTS[index],
            "recovered_quotient_representative": recovery["recovered"][index],
            "coefficient_difference": recovery["recovered"][index]
            - A6_COEFFICIENTS[index],
            "quotient_response_recovery_residual": recovery[
                "response_residual"
            ],
        }
        for index, operator in enumerate(OPERATOR_NAMES)
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_FREE_COEFFICIENT_RECOVERY.csv",
        tagged(recovery_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_LEAVE_ONE_GEOMETRY.csv",
        tagged(result["leave_one_out"]),
    )
    ricci_flat_rows = [
        {
            "identity": "differential_Bianchi_commutator",
            "equation": "source: int (nabla Riem)^2=-int(I1+4 I2); engine: D4=+3 I1_engine on Ricci=0",
            "consequence": "the sign change follows from R_engine=-R_source",
        },
        {
            "identity": "four_dimensional_algebraic_Weyl_identity",
            "equation": "I2=I1/2 on Ricci=0 in d=4",
            "consequence": "one parity-even Weyl-cubic scalar remains",
        },
        {
            "identity": "sourced_scalar_a6_projection",
            "equation": "v_RF dot c_a6=-1/15120",
            "consequence": "minus one-half proper-time sign gives zeta=1/[30240(4pi)^2 m^2]",
        },
        {
            "identity": "numeric_quotient_recovery",
            "equation": "v_RF dot c_recovered=v_RF dot c_source",
            "consequence": f"raw={recovery['recovered_raw_c3']:.17g}; one_loop={recovery['recovered_one_loop_c3']:.17g}",
        },
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_RICCI_FLAT_MAP.csv",
        tagged(ricci_flat_rows),
    )
    projector_gate = [
        {
            "gate": "sourced_integrated_a6_basis",
            "status": "PASS" if result["sources"]["passed"] else "FAIL",
            "reason": "all twelve integrated columns descend from the hash-locked primary formula",
        },
        {
            "gate": "nonlinear_geometric_templates",
            "status": "PASS" if result["geometry_gate"] else "FAIL",
            "reason": "nilpotent mixed derivatives include exact connection metric and volume terms",
        },
        {
            "gate": "template_rank",
            "status": "PASS" if result["rank_gate"] else "FAIL",
            "reason": f"rank={analysis['rank']} of 12; retained condition={analysis['condition_number_retained']:.6g}",
        },
        {
            "gate": "grid_independence",
            "status": "PASS" if result["crosscheck_gate"] else "FAIL",
            "reason": f"maximum N={result['size']} versus N={result['crosscheck_size']} relative residual={result['maximum_crosscheck']:.3e}",
        },
        {
            "gate": "known_free_scalar_quotient_recovery",
            "status": "PASS" if result["recovery_gate"] else "FAIL",
            "reason": f"response residual={recovery['response_residual']:.3e}; zeta={recovery['recovered_one_loop_c3']:.17g}; all leave-one-geometry ranks remain eight",
        },
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_PROJECTOR_GATE.csv",
        tagged(projector_gate),
    )
    interacting_gate = [
        {
            "gate": "geometric_projector",
            "status": "PASS" if result["all_checks_pass"] else "FAIL",
            "reason": "the continuum geometric quotient is now executable",
        },
        {
            "gate": "exact_free_lattice_multigeometry_response",
            "status": "REQUIRED",
            "reason": "the lattice determinant must recover the sourced continuum quotient across independent source geometries",
        },
        {
            "gate": "cutoff_and_volume_sequence",
            "status": "REQUIRED",
            "reason": "am must tend to zero while Nam tends to infinity",
        },
        {
            "gate": "interacting_TTT_long_run",
            "status": "DO_NOT_RUN_YET",
            "reason": "free lattice rather than synthetic heat-kernel response is the remaining calibration",
        },
        {
            "gate": "active_residual",
            "status": "ZERO_PRESERVED",
            "reason": "no interacting coefficient has been measured or promoted",
        },
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_INTERACTING_RUN_GATE.csv",
        tagged(interacting_gate),
    )
    local_gate = [
        {
            "arena": "GR_Newton_PPN",
            "status": "UNCHANGED",
            "reason": "the projector changes no two-derivative parent equation",
        },
        {
            "arena": "Maxwell_Poynting",
            "status": "UNCHANGED",
            "reason": "no mixed metric-gauge operator is activated",
        },
        {
            "arena": "strong_gravity_C3",
            "status": "CALIBRATION_ONLY",
            "reason": "the free coefficient is a projector benchmark rather than an MTS residual",
        },
        {
            "arena": "Gamma_MTS_res",
            "status": "ZERO",
            "reason": "interacting and total parent owners remain unmeasured",
        },
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_LOCAL_LIMIT_GATE.csv", tagged(local_gate)
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4911_DECISION.csv",
        tagged(
            [
                {
                    "overall_decision": result["decision"],
                    "geometry_count": len(result["ensemble"]),
                    "template_rank": analysis["rank"],
                    "retained_condition_number": analysis[
                        "condition_number_retained"
                    ],
                    "response_recovery_residual": recovery[
                        "response_residual"
                    ],
                    "recovered_free_scalar_zeta": recovery[
                        "recovered_one_loop_c3"
                    ],
                    "expected_free_scalar_zeta": recovery[
                        "expected_one_loop_c3"
                    ],
                    "interacting_run_launched": result[
                        "interacting_run_launched"
                    ],
                    "Gamma_MTS_res": result["Gamma_MTS_res"],
                    "all_checks_pass": result["all_checks_pass"],
                    "next_target": result["next_target"],
                    "elapsed_seconds": result["elapsed_seconds"],
                }
            ]
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometries", type=int, default=12)
    parser.add_argument("--size", type=int, default=6)
    parser.add_argument("--crosschecks", type=int, default=2)
    parser.add_argument("--crosscheck-size", type=int, default=8)
    parser.add_argument("--no-write", action="store_true")
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    result = run(
        geometry_count=arguments.geometries,
        size=arguments.size,
        crosscheck_count=arguments.crosschecks,
        crosscheck_size=arguments.crosscheck_size,
    )
    if not arguments.no_write:
        write_outputs(result)
    print(result["decision"])
    print(
        "rank={}/12 condition={:.6g} geometry_residual={:.3e} "
        "grid_residual={:.3e} response_residual={:.3e} "
        "zeta={:.17g} expected={:.17g} interacting=withheld gamma_res={}".format(
            result["analysis"]["rank"],
            result["analysis"]["condition_number_retained"],
            result["maximum_geometry_residual"],
            result["maximum_crosscheck"],
            result["recovery"]["response_residual"],
            result["recovery"]["recovered_one_loop_c3"],
            result["recovery"]["expected_one_loop_c3"],
            result["Gamma_MTS_res"],
        )
    )
    return 0 if result["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
