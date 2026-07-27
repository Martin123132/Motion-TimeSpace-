from __future__ import annotations

import csv
import hashlib
import itertools
import math
import time
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point as previous


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

MARKER = "MTS_FREE_METRIC_TTT_PROJECTOR_ARBITRATION_4910"
FORMAL_MARKER = "PPC4161_FREE_METRIC_TTT_PROJECTOR_ARBITRATION_4910"
NEXT_TARGET = (
    "4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-"
    "Weyl-cubic-projector.md"
)
CHECKED_DATE = "2026-07-12"
DIMENSIONS = 4
BASE_MOMENTA = np.array(
    [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-1.0, -1.0, 0.0, 0.0],
    ]
)
POLARIZATIONS = [
    previous.transverse_traceless_polarization(momentum, 10 + index)
    for index, momentum in enumerate(BASE_MOMENTA)
]
WEYL_TEMPLATE = previous.Weyl_cubic_template()["base_template"]


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
            "SRC4910_00_predecessor",
            POST
            / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md",
            "MTS_RENORMALIZED_MOTION_SCALAR_GAP_STRESS_THREE_POINT_4909",
            "validated_predecessor",
        ),
        (
            "SRC4910_01_predecessor_validation",
            OUTPUT / "P8_Y5_BRR545_4909_VALIDATION.csv",
            "VAL4909_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4910_02_scalar_a6",
            POST
            / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
            "full_heat_kernel_and_Ricci_flat_projection",
        ),
        (
            "SRC4910_03_operator_basis",
            POST
            / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md",
            "MTS_FIRST_RESIDUAL_OPERATOR_AND_INDEPENDENT_OBSERVABLE_GATE_4905",
            "on_shell_Weyl_cubic_normalization",
        ),
        (
            "SRC4910_04_metric_vertex",
            POST
            / "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md",
            "MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908",
            "triangle_and_seagull_identity",
        ),
        (
            "SRC4910_05_a6_archive",
            POST
            / "source-intake"
            / "heat_kernel_a6"
            / "4881"
            / "hep-th-0306138.tar",
            "binary_hash_locked_source",
            "primary_heat_kernel_archive",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        marker_found = contains(path, marker) if source_id != "SRC4910_05_a6_archive" else exists
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


def lattice_propagator(momentum: np.ndarray, mass: float) -> np.ndarray:
    return 1.0 / (
        mass**2 + np.sum(4.0 * np.sin(momentum / 2.0) ** 2, axis=1)
    )


def one_metric_vertex(
    source_momentum: np.ndarray,
    polarization: np.ndarray,
    incoming_momentum: np.ndarray,
) -> np.ndarray:
    outgoing = incoming_momentum + source_momentum
    forward_in = np.exp(1j * incoming_momentum) - 1.0
    backward_in = 1.0 - np.exp(-1j * incoming_momentum)
    forward_out = np.exp(1j * outgoing) - 1.0
    backward_out = 1.0 - np.exp(-1j * outgoing)
    return 0.5 * (
        np.einsum(
            "bi,ij,bj->b",
            np.conjugate(forward_out),
            polarization,
            forward_in,
            optimize=True,
        )
        + np.einsum(
            "bi,ij,bj->b",
            np.conjugate(backward_out),
            polarization,
            backward_in,
            optimize=True,
        )
    )


def momentum_chunk(start: int, stop: int, size: int) -> np.ndarray:
    flat = np.arange(start, stop, dtype=np.int64)
    digits = np.empty((len(flat), DIMENSIONS), dtype=float)
    working = flat.copy()
    for axis in range(DIMENSIONS - 1, -1, -1):
        digits[:, axis] = working % size
        working //= size
    return 2.0 * math.pi * digits / size


def free_TTT_density(
    size: int,
    momentum_scale: int,
    mass: float,
    chunk_size: int = 100_000,
) -> complex:
    source_momenta = (
        2.0 * math.pi * momentum_scale / size * BASE_MOMENTA
    )
    pair_coefficient = lambda first, second: (
        -0.5
        * mass**2
        * float(np.trace(POLARIZATIONS[first] @ POLARIZATIONS[second]))
    )
    triple_coefficient = 0.5 * mass**2 * float(
        np.trace(POLARIZATIONS[0] @ POLARIZATIONS[1] @ POLARIZATIONS[2])
        + np.trace(POLARIZATIONS[0] @ POLARIZATIONS[2] @ POLARIZATIONS[1])
    )
    volume = size**DIMENSIONS
    total = 0.0j
    for start in range(0, volume, chunk_size):
        momentum = momentum_chunk(start, min(start + chunk_size, volume), size)
        propagator = lattice_propagator(momentum, mass)
        integrand = propagator.astype(complex) * triple_coefficient

        for first, second, third in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
            pair_momentum = source_momenta[second] + source_momenta[third]
            intermediate = momentum + pair_momentum
            integrand -= (
                propagator
                * lattice_propagator(intermediate, mass)
                * one_metric_vertex(
                    source_momenta[first],
                    POLARIZATIONS[first],
                    intermediate,
                )
                * pair_coefficient(second, third)
            )

        after_third = momentum + source_momenta[2]
        after_second = after_third + source_momenta[1]
        integrand += (
            propagator
            * lattice_propagator(after_third, mass)
            * lattice_propagator(after_second, mass)
            * one_metric_vertex(
                source_momenta[2], POLARIZATIONS[2], momentum
            )
            * one_metric_vertex(
                source_momenta[1], POLARIZATIONS[1], after_third
            )
            * one_metric_vertex(
                source_momenta[0], POLARIZATIONS[0], after_second
            )
        )

        after_second = momentum + source_momenta[1]
        after_third = after_second + source_momenta[2]
        integrand += (
            propagator
            * lattice_propagator(after_second, mass)
            * lattice_propagator(after_third, mass)
            * one_metric_vertex(
                source_momenta[1], POLARIZATIONS[1], momentum
            )
            * one_metric_vertex(
                source_momenta[2], POLARIZATIONS[2], after_second
            )
            * one_metric_vertex(
                source_momenta[0], POLARIZATIONS[0], after_third
            )
        )
        total += np.sum(integrand)
    return 0.5 * total / volume


def dense_source_matrix(
    size: int,
    source_momentum: np.ndarray,
    polarization: np.ndarray,
) -> np.ndarray:
    coordinates = np.array(
        list(itertools.product(range(size), repeat=DIMENSIONS)), dtype=int
    )
    volume = len(coordinates)
    lookup = {tuple(coordinate): index for index, coordinate in enumerate(coordinates)}
    forward: list[np.ndarray] = []
    backward: list[np.ndarray] = []
    for axis in range(DIMENSIONS):
        plus = np.zeros((volume, volume), dtype=complex)
        minus = np.zeros((volume, volume), dtype=complex)
        for index, coordinate in enumerate(coordinates):
            coordinate_plus = coordinate.copy()
            coordinate_minus = coordinate.copy()
            coordinate_plus[axis] = (coordinate_plus[axis] + 1) % size
            coordinate_minus[axis] = (coordinate_minus[axis] - 1) % size
            plus[index, lookup[tuple(coordinate_plus)]] = 1.0
            plus[index, index] -= 1.0
            minus[index, index] += 1.0
            minus[index, lookup[tuple(coordinate_minus)]] -= 1.0
        forward.append(plus)
        backward.append(minus)
    phase = np.exp(1j * coordinates @ source_momentum)
    result = np.zeros((volume, volume), dtype=complex)
    for mu in range(DIMENSIONS):
        for nu in range(DIMENSIONS):
            source = np.diag(phase * polarization[mu, nu])
            result += 0.5 * (
                forward[mu].conjugate().T @ source @ forward[nu]
                + backward[mu].conjugate().T @ source @ backward[nu]
            )
    return result


def dense_TTT_density(size: int, momentum_scale: int, mass: float) -> complex:
    coordinates = np.array(
        list(itertools.product(range(size), repeat=DIMENSIONS)), dtype=int
    )
    volume = len(coordinates)
    source_momenta = (
        2.0 * math.pi * momentum_scale / size * BASE_MOMENTA
    )
    source_matrices = [
        dense_source_matrix(size, momentum, polarization)
        for momentum, polarization in zip(source_momenta, POLARIZATIONS)
    ]
    diagonal_momenta = 2.0 * math.pi * coordinates / size
    propagator_eigenvalues = lattice_propagator(diagonal_momenta, mass)
    Fourier = np.exp(
        1j * coordinates @ diagonal_momenta.T
    ) / math.sqrt(volume)
    propagator = Fourier @ np.diag(propagator_eigenvalues) @ Fourier.conjugate().T

    def pair(first: int, second: int) -> np.ndarray:
        coefficient = (
            -0.5
            * mass**2
            * float(np.trace(POLARIZATIONS[first] @ POLARIZATIONS[second]))
        )
        phase = np.exp(
            1j * coordinates @ (source_momenta[first] + source_momenta[second])
        )
        return np.diag(coefficient * phase)

    triple_coefficient = 0.5 * mass**2 * float(
        np.trace(POLARIZATIONS[0] @ POLARIZATIONS[1] @ POLARIZATIONS[2])
        + np.trace(POLARIZATIONS[0] @ POLARIZATIONS[2] @ POLARIZATIONS[1])
    )
    triple = np.diag(np.full(volume, triple_coefficient, dtype=complex))
    value = np.trace(propagator @ triple)
    value -= np.trace(
        propagator @ source_matrices[0] @ propagator @ pair(1, 2)
    )
    value -= np.trace(
        propagator @ source_matrices[1] @ propagator @ pair(0, 2)
    )
    value -= np.trace(
        propagator @ source_matrices[2] @ propagator @ pair(0, 1)
    )
    value += np.trace(
        propagator
        @ source_matrices[0]
        @ propagator
        @ source_matrices[1]
        @ propagator
        @ source_matrices[2]
    )
    value += np.trace(
        propagator
        @ source_matrices[0]
        @ propagator
        @ source_matrices[2]
        @ propagator
        @ source_matrices[1]
    )
    return 0.5 * value / volume


def dense_momentum_validation() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for size in (3, 4):
        dense = dense_TTT_density(size, 1, 1.2)
        momentum = free_TTT_density(size, 1, 1.2, chunk_size=10_000)
        rows.append(
            {
                "size": size,
                "mass": 1.2,
                "momentum_density_real": float(momentum.real),
                "momentum_density_imag": float(momentum.imag),
                "dense_density_real": float(dense.real),
                "dense_density_imag": float(dense.imag),
                "absolute_residual": abs(momentum - dense),
                "passed": abs(momentum - dense) < 1e-13,
            }
        )
    return {
        "rows": rows,
        "passed": all(row["passed"] for row in rows),
    }


def free_TTT_grid() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    start = time.perf_counter()
    for size in (24, 32):
        for momentum_scale in range(7):
            value = free_TTT_density(size, momentum_scale, 1.0)
            rows.append(
                {
                    "size": size,
                    "mass": 1.0,
                    "momentum_scale": momentum_scale,
                    "external_k": 2.0 * math.pi * momentum_scale / size,
                    "external_k_over_mass": 2.0
                    * math.pi
                    * momentum_scale
                    / size,
                    "W123_density_real": float(value.real),
                    "W123_density_imag": float(value.imag),
                }
            )
            print(
                f"free_TTT N={size} s={momentum_scale} "
                f"W/V={value.real:.15g} imag={value.imag:.3g}"
            )
    return {
        "rows": rows,
        "elapsed_seconds": time.perf_counter() - start,
        "maximum_imaginary_residual": max(
            abs(row["W123_density_imag"]) for row in rows
        ),
    }


def naive_fit_rows(grid_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = 1.0 / (30240.0 * (4.0 * math.pi) ** 2)
    rows: list[dict[str, Any]] = []
    for size in (24, 32):
        selected_size = [row for row in grid_rows if row["size"] == size]
        for maximum_scale in (4, 5, 6):
            selected = [
                row
                for row in selected_size
                if row["momentum_scale"] <= maximum_scale
            ]
            x = np.array([row["external_k"] ** 2 for row in selected])
            y = np.array([row["W123_density_real"] for row in selected])
            coefficients = np.polynomial.polynomial.polyfit(x, y, 4)
            naive_zeta = float(coefficients[3] / WEYL_TEMPLATE)
            rows.append(
                {
                    "size": size,
                    "mass": 1.0,
                    "maximum_scale": maximum_scale,
                    "maximum_k_over_mass": max(row["external_k_over_mass"] for row in selected),
                    "fit_degree": 4,
                    "q0_coefficient": float(coefficients[0]),
                    "q2_coefficient": float(coefficients[1]),
                    "q4_coefficient": float(coefficients[2]),
                    "q6_coefficient": float(coefficients[3]),
                    "q8_coefficient": float(coefficients[4]),
                    "Weyl_template": WEYL_TEMPLATE,
                    "naive_zeta": naive_zeta,
                    "expected_continuum_scalar_zeta": expected,
                    "naive_over_expected": naive_zeta / expected,
                    "same_sign_as_expected": naive_zeta * expected > 0,
                    "within_factor_two": 0.5 <= abs(naive_zeta / expected) <= 2.0,
                }
            )
    return rows


def Euclidean_Ricci_flat_no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "gauge_fix",
            "equation": "partial^mu(h_mn-delta_mn h/2)=0",
            "result": "Euclidean de Donder gauge on the flat periodic background",
        },
        {
            "step": "linearized_Ricci",
            "equation": "R_mn^(1)=-(1/2) partial^2 h_mn",
            "result": "Ricci-flat requires each physical Fourier mode to be harmonic",
        },
        {
            "step": "periodic_harmonic_kernel",
            "equation": "partial^2 h_mn=0 on T4",
            "result": "only the zero-momentum constant tensor survives",
        },
        {
            "step": "curvature",
            "equation": "partial h_constant=0",
            "result": "Riemann^(1)=Weyl^(1)=0",
        },
        {
            "step": "theorem",
            "equation": "real periodic Euclidean Ricci-flat perturbation with nonzero Weyl does not exist",
            "result": "one TT triplet cannot be both real-periodic and an on-shell C3 projector",
        },
    ]


def raw_a6_contaminant_rows() -> list[dict[str, Any]]:
    return [
        {"class": "derivative", "operator": "(nabla R)^2", "survives_off_shell_TT": True},
        {"class": "derivative", "operator": "(nabla R_mn)^2 and crossed Ricci derivatives", "survives_off_shell_TT": True},
        {"class": "derivative", "operator": "(nabla R_mnrs)^2", "survives_off_shell_TT": True},
        {"class": "cubic", "operator": "R^3", "survives_off_shell_TT": True},
        {"class": "cubic", "operator": "R R_mn R^mn", "survives_off_shell_TT": True},
        {"class": "cubic", "operator": "R R_mnrs R^mnrs", "survives_off_shell_TT": True},
        {"class": "cubic", "operator": "R_m^n R_n^r R_r^m", "survives_off_shell_TT": True},
        {"class": "cubic", "operator": "R_mn R_rs R^mrns", "survives_off_shell_TT": True},
        {"class": "cubic", "operator": "R_mn R_mabc R_n^abc", "survives_off_shell_TT": True},
        {"class": "cubic", "operator": "Riemann cubic I1", "survives_off_shell_TT": True},
        {"class": "cubic", "operator": "Riemann cubic I2", "survives_off_shell_TT": True},
    ]


def projector_options_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "single_real_Euclidean_TT_triplet",
            "status": "REJECTED",
            "reason": "nonzero real periodic mode is off shell and carries Ricci contamination",
            "interacting_Monte_Carlo_compatible": True,
        },
        {
            "route": "full_off_shell_a6_template_matrix",
            "status": "SELECTED",
            "reason": "measure enough independent source triples to solve derivative and cubic curvature coefficients before the Ricci-flat projection",
            "interacting_Monte_Carlo_compatible": True,
        },
        {
            "route": "complex_null_on_shell_amplitude",
            "status": "ANALYTIC_CROSSCHECK",
            "reason": "isolates the on-shell Weyl amplitude but requires analytic continuation from Euclidean Monte Carlo data",
            "interacting_Monte_Carlo_compatible": False,
        },
        {
            "route": "Ricci_flat_curved_background",
            "status": "OPTIONAL_STRONG_FIELD_CROSSCHECK",
            "reason": "avoids flat-torus no-go but needs a separate curved lattice and boundary construction",
            "interacting_Monte_Carlo_compatible": False,
        },
    ]


def full_basis_projector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "stage": "basis_reduction",
            "equation": "choose integrated O_A^(6) after boundary, Bianchi and integration-by-parts identities",
            "acceptance": "no raw a6 invariant is silently dropped before its identity is proved",
        },
        {
            "stage": "geometric_templates",
            "equation": "M_rA=partial_1 partial_2 partial_3 int sqrt(g) O_A^(6)[g_r] at epsilon=0",
            "acceptance": "templates include nonlinear curvature and metric-volume terms",
        },
        {
            "stage": "response_subtraction",
            "equation": "y_r=W_123,r - y_r^(q0) - y_r^(q2) - y_r^(q4)",
            "acceptance": "at least four momentum scales per tensor geometry",
        },
        {
            "stage": "rank_gate",
            "equation": "rank(M)=number of retained independent O_A^(6)",
            "acceptance": "singular values and condition number reported before inversion",
        },
        {
            "stage": "correlated_inverse",
            "equation": "c=(M^T Sigma^-1 M)^-1 M^T Sigma^-1 y",
            "acceptance": "full Monte Carlo covariance Sigma and leave-one-geometry stability",
        },
        {
            "stage": "Ricci_flat_map",
            "equation": "zeta_C3=v_A c_A where O_A^(6)|Ricci=0=v_A C^3 plus boundary identities",
            "acceptance": "free scalar recovers 1/[30240(4pi)^2 m^2] before interacting use",
        },
        {
            "stage": "regulator_limit",
            "equation": "a m -> 0; N a m -> infinity; zeta_C3 m^2 common across stencils",
            "acceptance": "cutoff volume and alternative-stencil extrapolations agree",
        },
        {
            "stage": "Ward_and_on_shell_crosscheck",
            "equation": "lattice contact Ward identities plus analytically continued complex-null amplitude",
            "acceptance": "longitudinal residuals vanish and parity-odd scalar coefficient is zero",
        },
    ]


def local_limit_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "massless_spin2_pole",
            "status": "UNCHANGED",
            "reason": "no residual coefficient is activated and C3 has no flat quadratic variation",
        },
        {
            "arena": "Newton_and_PPN",
            "status": "UNCHANGED",
            "reason": "the once-calibrated M_R and linear source exchange are untouched",
        },
        {
            "arena": "Maxwell_and_Poynting",
            "status": "UNCHANGED",
            "reason": "no mixed metric-electromagnetic operator is generated by the projector exercise",
        },
        {
            "arena": "motion_scalar_mass_pilot",
            "status": "RETAINED_NONCLAIM",
            "reason": "projector failure concerns c6 and does not erase the finite-cutoff two-point calculation",
        },
        {
            "arena": "future_strong_gravity",
            "status": "CONDITIONAL",
            "reason": "a future zeta must satisfy |zeta| q^4/M_R^2 much less than one in local arenas",
        },
        {
            "arena": "Gamma_MTS_res",
            "status": "ZERO",
            "reason": "neither the naive fit nor the diagnostic free-pole value is promoted",
        },
    ]


def run() -> dict[str, Any]:
    sources = source_contract()
    dense = dense_momentum_validation()
    grid = free_TTT_grid()
    fits = naive_fit_rows(grid["rows"])
    expected = 1.0 / (30240.0 * (4.0 * math.pi) ** 2)
    failure = {
        "expected_continuum_scalar_zeta": expected,
        "fit_count": len(fits),
        "minimum_absolute_naive_over_expected": min(
            abs(row["naive_over_expected"]) for row in fits
        ),
        "maximum_absolute_naive_over_expected": max(
            abs(row["naive_over_expected"]) for row in fits
        ),
        "same_sign_fit_count": sum(row["same_sign_as_expected"] for row in fits),
        "within_factor_two_fit_count": sum(row["within_factor_two"] for row in fits),
        "naive_projector_pass": False,
        "interpretation": "the q6 coefficient of one real Euclidean TT response is an off-shell mixture and also retains finite-lattice regulator effects",
    }
    no_go = Euclidean_Ricci_flat_no_go_rows()
    contaminants = raw_a6_contaminant_rows()
    options = projector_options_rows()
    projector_contract = full_basis_projector_contract_rows()
    local_limits = local_limit_gate_rows()
    interacting_gate = [
        {
            "gate": "free_triangle_and_seagulls",
            "status": "PASS",
            "reason": "dense and momentum implementations agree below 1e-13",
        },
        {
            "gate": "free_known_C3_recovery",
            "status": "FAIL",
            "reason": "single-triplet q6 division misses magnitude and sign",
        },
        {
            "gate": "real_Euclidean_on_shell_projection",
            "status": "THEOREM_BLOCKED",
            "reason": "nontrivial periodic Ricci-flat perturbation has zero Weyl",
        },
        {
            "gate": "full_off_shell_template_rank",
            "status": "NOT_YET_CONSTRUCTED",
            "reason": "raw a6 derivative and Ricci templates must be included",
        },
        {
            "gate": "interacting_TTT_long_run",
            "status": "DO_NOT_RUN",
            "reason": "its numerator cannot yet be mapped uniquely to C3",
        },
        {
            "gate": "active_residual",
            "status": "ZERO_PRESERVED",
            "reason": "no coefficient is promoted from the failed projector",
        },
    ]
    all_checks = (
        sources["passed"]
        and dense["passed"]
        and grid["maximum_imaginary_residual"] < 1e-12
        and failure["minimum_absolute_naive_over_expected"] > 100.0
        and failure["same_sign_fit_count"] == 0
        and failure["within_factor_two_fit_count"] == 0
    )
    return {
        "sources": sources,
        "dense": dense,
        "grid": grid,
        "fits": fits,
        "failure": failure,
        "no_go": no_go,
        "contaminants": contaminants,
        "options": options,
        "projector_contract": projector_contract,
        "local_limits": local_limits,
        "interacting_gate": interacting_gate,
        "Gamma_MTS_res": 0,
        "c6_promoted": False,
        "next_target": NEXT_TARGET,
        "decision": "EXACT_FREE_LATTICE_METRIC_TTT_IMPLEMENTED_AND_DENSE_VALIDATED_NAIVE_SINGLE_TT_Q6_OVER_WEYL_PROJECTOR_FAILS_MAGNITUDE_AND_SIGN_REAL_PERIODIC_EUCLIDEAN_RICCI_FLAT_NONZERO_WEYL_PROJECTOR_PROVED_IMPOSSIBLE_FULL_OFF_SHELL_A6_TEMPLATE_BASIS_SELECTED_INTERACTING_LONG_RUN_WITHHELD_ACTIVE_RESIDUAL_ZERO_PRIVATE_NONCLAIM",
        "all_checks_pass": all_checks,
    }


def write_outputs(result: dict[str, Any]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_SOURCE_REGISTER.csv",
        tagged(result["sources"]["rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_DENSE_MOMENTUM_VALIDATION.csv",
        tagged(result["dense"]["rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_FREE_TTT_GRID.csv",
        tagged(result["grid"]["rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_NAIVE_C3_FITS.csv",
        tagged(result["fits"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_PROJECTOR_FAILURE.csv",
        tagged([result["failure"]]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_EUCLIDEAN_RICCI_FLAT_NO_GO.csv",
        tagged(result["no_go"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_A6_CONTAMINANTS.csv",
        tagged(result["contaminants"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_PROJECTOR_OPTIONS.csv",
        tagged(result["options"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_FULL_BASIS_PROJECTOR_CONTRACT.csv",
        tagged(result["projector_contract"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_LOCAL_LIMIT_GATE.csv",
        tagged(result["local_limits"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_INTERACTING_RUN_GATE.csv",
        tagged(result["interacting_gate"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4910_DECISION.csv",
        tagged(
            [
                {
                    "overall_decision": result["decision"],
                    "Gamma_MTS_res": result["Gamma_MTS_res"],
                    "c6_promoted": result["c6_promoted"],
                    "next_target": result["next_target"],
                    "all_checks_pass": result["all_checks_pass"],
                    "elapsed_seconds": result["grid"]["elapsed_seconds"],
                }
            ]
        ),
    )


def main() -> int:
    result = run()
    write_outputs(result)
    print(result["decision"])
    print(
        "dense={} imag={:.3g} min_abs_ratio={:.3f} same_sign={} "
        "interacting_run=withheld gamma_res={}".format(
            result["dense"]["passed"],
            result["grid"]["maximum_imaginary_residual"],
            result["failure"]["minimum_absolute_naive_over_expected"],
            result["failure"]["same_sign_fit_count"],
            result["Gamma_MTS_res"],
        )
    )
    return 0 if result["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
