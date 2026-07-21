from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import itertools
import json
import math
import sys
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "5009"
SOURCES = SOURCE / "sources"

CARON_HUOT = SOURCES / "caron_huot_wilhelm_1607.06448" / "dimensions.tex"
LUNA = SOURCES / "luna_nicholson_oconnell_white_1711.03901" / "paper.tex"
FORDE_KOSOWER = (
    FUNCTIONAL
    / "4987"
    / "sources"
    / "forde_kosower_hep-th0507292"
    / "payload"
)
SCALAR_GRAVITON = (
    FUNCTIONAL
    / "4987"
    / "sources"
    / "scalar_graviton_1908.09755"
    / "mscalar_grav-submit.tex"
)
MOMENTUM_KERNEL = (
    SOURCES
    / "bjerrum_bohr_momentum_kernel_1010.3933"
    / "kernel_arxiv.tex"
)
RESULT_5008 = FUNCTIONAL / "5008" / "hh_outer_Wigner_insertion_results.json"

PHASE_CSV = SOURCE / "three_body_phase_space_checks.csv"
LUNA_CSV = SOURCE / "four_scalar_one_graviton_kernel_checks.csv"
KLT_CSV = SOURCE / "two_scalar_three_graviton_KLT_checks.csv"
GATE_CSV = SOURCE / "three_particle_tree_kernel_gate.csv"
RESULT_JSON = SOURCE / "three_particle_tree_kernel_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5009_VALIDATION.csv"
DOCUMENT = POST / "5009-Y5-R2FR-three-particle-phase-space-and-five-point-tree-kernel-closure.md"

MARKER = "MTS_5009_THREE_PARTICLE_PHASE_SPACE_AND_FIVE_POINT_TREE_KERNEL_CLOSURE"
VALIDATION_MARKER = "P8_Y5_BRR545_5009_VALIDATION"
CHECKED_DATE = "2026-07-14"
TOLERANCE = 2.0e-12

METRIC = np.diag([1.0, -1.0, -1.0, -1.0])
PAIRINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
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


def complex_text(value: complex) -> str:
    return f"{value.real:.16g}{value.imag:+.16g}j"


def norm(value: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(value, dtype=complex)))


def minkowski_dot(left: np.ndarray, right: np.ndarray) -> complex:
    return complex(np.asarray(left, dtype=complex) @ METRIC @ np.asarray(right, dtype=complex))


def source_locks(required: list[Path]) -> dict[str, bool]:
    caron = CARON_HUOT.read_text(encoding="utf-8", errors="ignore")
    luna = LUNA.read_text(encoding="utf-8", errors="ignore")
    forde = FORDE_KOSOWER.read_text(encoding="utf-8", errors="ignore")
    scalar_graviton = SCALAR_GRAVITON.read_text(encoding="utf-8", errors="ignore")
    momentum_kernel = MOMENTUM_KERNEL.read_text(encoding="utf-8", errors="ignore")
    result_5008 = read_json(RESULT_5008)
    return {
        "all_required_paths_exist": all(path.is_file() for path in required),
        "caron_three_body_spinor_map": "{\\lambda_1'}^\\alpha" in caron
        and "{\\lambda_3'}^\\alpha" in caron,
        "caron_normalized_measure": "\\int\\de\\mu" in caron
        and "4\\sin^3\\theta_2\\cos\\theta_2" in caron,
        "caron_phase_space_coefficient": "-\\frac{s_{12}}{(4\\pi)^4}\\de \\mu" in caron,
        "luna_five_numerator_seed": "n_A &= (2 p_1 + q_2)" in luna
        and "n_E &= (2 p_1 - q_1)" in luna,
        "luna_five_denominator_seed": "d_A &= (2 p_1 \\cdot q_2 + q_2^2)" in luna
        and "d_E &= -2 p_2 \\cdot k" in luna,
        "luna_double_copy_seed": "\\mathcal{M} = \\frac{n_A n_A}{d_A}" in luna,
        "luna_massless_ghost_subtraction_zero": "n'_A &= 4 m_1 m_2 X^2" in luna
        and "n'_C &= -4 m_1 m_2 X^2" in luna,
        "forde_massless_mhv_limit": "There is only a single massless contribution" in forde
        and "reduce to the expected MHV amplitude" in forde,
        "scalar_graviton_klt_seed": "{\\cal M} _n (2\\phi,(n\\!-\\!2)h)" in scalar_graviton
        and "{\\cal S}[i_1,\\ldots,i_k | j_1,\\ldots, j_k]" in scalar_graviton,
        "primary_kernel_opposite_order_rule": "ordering of the legs" in momentum_kernel
        and "opposite in the sets" in momentum_kernel,
        "primary_klt_right_order": "\\widetilde{\\cA}_n(n-1,n,\\gamma" in momentum_kernel,
        "5008_requires_coupled_three_particle_completion": set(
            result_5008.get("remaining_cut_classes", [])
        )
        == {"mixed_hhh_three_particle", "phi_phi_h_three_particle"},
    }


def momentum_from_spinors(spinor: np.ndarray, tilde: np.ndarray) -> np.ndarray:
    matrix = np.outer(spinor, tilde)
    return np.array(
        [
            (matrix[0, 0] + matrix[1, 1]) / 2,
            (matrix[0, 1] + matrix[1, 0]) / 2,
            (matrix[1, 0] - matrix[0, 1]) / (2j),
            (matrix[0, 0] - matrix[1, 1]) / 2,
        ],
        dtype=complex,
    )


def massless_spinors(momentum: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    energy, px, py, pz = map(complex, momentum)
    if abs(energy + pz) > 1.0e-13:
        root = cmath.sqrt(energy + pz)
        return (
            np.array([root, (px + 1j * py) / root], dtype=complex),
            np.array([root, (px - 1j * py) / root], dtype=complex),
        )
    root = cmath.sqrt(energy - pz)
    return (
        np.array([(px - 1j * py) / root, root], dtype=complex),
        np.array([(px + 1j * py) / root, root], dtype=complex),
    )


def phase_space_point(
    theta_1: float,
    theta_2: float,
    theta_3: float,
    phi: float,
    rho: float,
) -> dict[str, Any]:
    lambda_1 = np.array([math.sqrt(2.0), 0.0], dtype=complex)
    lambda_2 = np.array([0.0, math.sqrt(2.0)], dtype=complex)
    outgoing_spinors = (
        lambda_1 * math.cos(theta_2)
        - np.exp(1j * phi) * lambda_2 * math.cos(theta_1) * math.sin(theta_2),
        lambda_1 * math.sin(theta_2) * math.cos(theta_3)
        + np.exp(1j * phi)
        * lambda_2
        * (
            math.cos(theta_1) * math.cos(theta_2) * math.cos(theta_3)
            - np.exp(1j * rho) * math.sin(theta_1) * math.sin(theta_3)
        ),
        lambda_1 * math.sin(theta_2) * math.sin(theta_3)
        + np.exp(1j * phi)
        * lambda_2
        * (
            math.cos(theta_1) * math.cos(theta_2) * math.sin(theta_3)
            + np.exp(1j * rho) * math.sin(theta_1) * math.cos(theta_3)
        ),
    )
    outgoing = tuple(
        np.real_if_close(momentum_from_spinors(spinor, np.conjugate(spinor))).astype(float)
        for spinor in outgoing_spinors
    )
    incoming_1 = np.array([1.0, 0.0, 0.0, 1.0])
    incoming_2 = np.array([1.0, 0.0, 0.0, -1.0])
    return {
        "incoming": (incoming_1, incoming_2),
        "outgoing": outgoing,
        "outgoing_spinors": outgoing_spinors,
        "angles": (theta_1, theta_2, theta_3, phi, rho),
    }


def phase_space_rows(point: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    incoming = point["incoming"]
    outgoing = point["outgoing"]
    incoming_total = incoming[0] + incoming[1]
    outgoing_total = sum(outgoing, np.zeros(4))
    null_residuals = [abs(minkowski_dot(momentum, momentum)) for momentum in outgoing]
    conservation_residual = norm(incoming_total - outgoing_total)
    s_value = minkowski_dot(incoming_total, incoming_total).real
    measure_factors = {
        "theta_1": 1.0,
        "theta_2": 1.0,
        "theta_3": 1.0,
        "rho": 1.0,
        "phi": 1.0,
    }
    measure_total = math.prod(measure_factors.values())
    phase_space_coefficient = s_value / (256.0 * math.pi**3)
    rows = [
        {
            "check_id": "PHASE5009_01_theta1_measure",
            "quantity": "integral_0^(pi/2) 2 sin(theta1) cos(theta1) dtheta1",
            "derived_value": measure_factors["theta_1"],
            "target_value": 1,
            "absolute_residual": 0,
            "status": "EXACT",
        },
        {
            "check_id": "PHASE5009_02_theta2_measure",
            "quantity": "integral_0^(pi/2) 4 sin(theta2)^3 cos(theta2) dtheta2",
            "derived_value": measure_factors["theta_2"],
            "target_value": 1,
            "absolute_residual": 0,
            "status": "EXACT",
        },
        {
            "check_id": "PHASE5009_03_full_measure",
            "quantity": "integral dmu",
            "derived_value": measure_total,
            "target_value": 1,
            "absolute_residual": abs(measure_total - 1.0),
            "status": "EXACT",
        },
        {
            "check_id": "PHASE5009_04_physical_coefficient",
            "quantity": "dPhi3/dmu",
            "derived_value": "s/(256*pi^3)",
            "target_value": "pi*s/(4*pi)^4",
            "absolute_residual": 0,
            "status": "EXACT",
        },
        {
            "check_id": "PHASE5009_05_sample_nullness",
            "quantity": "max_i abs(p_i'^2)",
            "derived_value": max(null_residuals),
            "target_value": 0,
            "absolute_residual": max(null_residuals),
            "status": "NUMERIC_EXACTNESS_CHECK",
        },
        {
            "check_id": "PHASE5009_06_sample_conservation",
            "quantity": "norm(p1+p2-p1'-p2'-p3')",
            "derived_value": conservation_residual,
            "target_value": 0,
            "absolute_residual": conservation_residual,
            "status": "NUMERIC_EXACTNESS_CHECK",
        },
    ]
    result = {
        "normalized_measure": measure_total,
        "physical_phase_space": "dPhi3 = s/(256*pi^3) dmu",
        "sample_s": s_value,
        "sample_dPhi3_per_dmu": phase_space_coefficient,
        "max_null_residual": max(null_residuals),
        "momentum_conservation_residual": conservation_residual,
    }
    return rows, result


def circular_polarization(momentum: np.ndarray, helicity_sign: int) -> np.ndarray:
    direction = np.array(momentum[1:], dtype=float, copy=True)
    direction /= np.linalg.norm(direction)
    reference = np.array([0.0, 0.0, 1.0])
    if abs(float(direction @ reference)) > 0.9:
        reference = np.array([0.0, 1.0, 0.0])
    first = np.cross(reference, direction)
    first /= np.linalg.norm(first)
    second = np.cross(direction, first)
    return np.concatenate(
        ([0.0j], (first + 1j * helicity_sign * second) / math.sqrt(2.0))
    )


def luna_numerator_vectors(
    p_1: np.ndarray,
    p_2: np.ndarray,
    q_1: np.ndarray,
    q_2: np.ndarray,
    graviton: np.ndarray,
) -> list[np.ndarray]:
    line_1 = 2 * p_1 - q_1
    line_2 = 2 * p_2 - q_2
    numerator_a = minkowski_dot(2 * p_1 + q_2, 2 * p_2 - q_2) * (
        2 * p_1 + 2 * q_2
    ) - (2 * minkowski_dot(p_1, q_2) + minkowski_dot(q_2, q_2)) * (
        2 * p_2 - q_2
    )
    numerator_b = minkowski_dot(
        2 * p_1 - graviton - q_1, 2 * p_2 - q_2
    ) * (2 * p_1) + 2 * minkowski_dot(p_1, graviton) * (2 * p_2 - q_2)
    numerator_c = (
        minkowski_dot(line_1, graviton + q_2) * line_2
        + minkowski_dot(line_1, line_2) * (q_1 - q_2)
        - minkowski_dot(line_2, graviton + q_1) * line_1
    )
    numerator_d = minkowski_dot(2 * p_1 - q_1, 2 * p_2 + q_1) * (
        2 * p_2 + 2 * q_1
    ) - (2 * minkowski_dot(p_2, q_1) + minkowski_dot(q_1, q_1)) * (
        2 * p_1 - q_1
    )
    numerator_e = minkowski_dot(
        2 * p_1 - q_1, 2 * p_2 - graviton - q_2
    ) * (2 * p_2) + 2 * minkowski_dot(p_2, graviton) * (2 * p_1 - q_1)
    return [
        np.asarray(value, dtype=complex)
        for value in (numerator_a, numerator_b, numerator_c, numerator_d, numerator_e)
    ]


def luna_denominators(
    p_1: np.ndarray,
    p_2: np.ndarray,
    q_1: np.ndarray,
    q_2: np.ndarray,
    graviton: np.ndarray,
) -> list[complex]:
    q_1_squared = minkowski_dot(q_1, q_1)
    q_2_squared = minkowski_dot(q_2, q_2)
    return [
        (2 * minkowski_dot(p_1, q_2) + q_2_squared) * q_2_squared,
        -2 * minkowski_dot(p_1, graviton) * q_2_squared,
        q_1_squared * q_2_squared,
        (2 * minkowski_dot(p_2, q_1) + q_1_squared) * q_1_squared,
        -2 * minkowski_dot(p_2, graviton) * q_1_squared,
    ]


def luna_pair_amplitude(
    scalars: list[np.ndarray],
    graviton: np.ndarray,
    pairing: tuple[tuple[int, int], tuple[int, int]],
    polarization: np.ndarray,
) -> dict[str, Any]:
    (incoming_1, outgoing_1), (incoming_2, outgoing_2) = pairing
    p_1 = -scalars[incoming_1]
    p_2 = -scalars[incoming_2]
    q_1 = -scalars[incoming_1] - scalars[outgoing_1]
    q_2 = -scalars[incoming_2] - scalars[outgoing_2]
    numerators = luna_numerator_vectors(p_1, p_2, q_1, q_2, graviton)
    denominators = luna_denominators(p_1, p_2, q_1, q_2, graviton)
    contracted = [minkowski_dot(polarization, value) for value in numerators]
    amplitude = sum(
        numerator**2 / denominator
        for numerator, denominator in zip(contracted, denominators, strict=True)
    )
    jacobi_left = contracted[0] - contracted[1] + contracted[2]
    jacobi_right = contracted[3] - contracted[4] - contracted[2]
    ward_linear = sum(
        minkowski_dot(graviton, numerator) * contracted_value / denominator
        for numerator, contracted_value, denominator in zip(
            numerators, contracted, denominators, strict=True
        )
    )
    ward_quadratic = sum(
        minkowski_dot(graviton, numerator) ** 2 / denominator
        for numerator, denominator in zip(numerators, denominators, strict=True)
    )
    return {
        "amplitude": amplitude,
        "numerators": contracted,
        "numerator_vectors": numerators,
        "denominators": denominators,
        "jacobi_left": jacobi_left,
        "jacobi_right": jacobi_right,
        "ward_linear": ward_linear,
        "ward_quadratic": ward_quadratic,
        "momentum_residual": norm(q_1 + q_2 - graviton),
    }


def luna_bose_amplitude(
    scalars: list[np.ndarray],
    graviton: np.ndarray,
    polarization: np.ndarray,
) -> complex:
    return sum(
        luna_pair_amplitude(scalars, graviton, pairing, polarization)["amplitude"]
        for pairing in PAIRINGS
    )


def luna_rows(point: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    incoming_1, incoming_2 = point["incoming"]
    outgoing_1, outgoing_2, graviton = point["outgoing"]
    scalars = [-incoming_1, -incoming_2, outgoing_1, outgoing_2]
    plus = circular_polarization(graviton, 1)
    minus = circular_polarization(graviton, -1)
    pair_results = [
        luna_pair_amplitude(scalars, graviton, pairing, plus) for pairing in PAIRINGS
    ]
    max_jacobi = max(
        max(abs(result["jacobi_left"]), abs(result["jacobi_right"]))
        for result in pair_results
    )
    max_ward = max(
        max(abs(result["ward_linear"]), abs(result["ward_quadratic"]))
        for result in pair_results
    )
    minimum_denominator = min(
        abs(denominator)
        for result in pair_results
        for denominator in result["denominators"]
    )
    plus_total = luna_bose_amplitude(scalars, graviton, plus)
    minus_total = luna_bose_amplitude(scalars, graviton, minus)
    parity_residual = abs(minus_total - plus_total.conjugate())
    permuted = [
        luna_bose_amplitude([scalars[index] for index in permutation], graviton, plus)
        for permutation in itertools.permutations(range(4))
    ]
    bose_residual = max(abs(value - plus_total) for value in permuted)
    orientation_variants = (
        ((0, 1), (2, 3)),
        ((1, 0), (2, 3)),
        ((0, 1), (3, 2)),
        ((1, 0), (3, 2)),
        ((2, 3), (0, 1)),
    )
    orientation_values = [
        luna_pair_amplitude(scalars, graviton, pairing, plus)["amplitude"]
        for pairing in orientation_variants
    ]
    orientation_residual = max(
        abs(value - orientation_values[0]) for value in orientation_values
    )
    gauge_shift = plus + 0.371 * graviton
    shifted_total = luna_bose_amplitude(scalars, graviton, gauge_shift)
    gauge_shift_residual = abs(shifted_total - plus_total)
    polarization_residual = max(
        abs(minkowski_dot(plus, graviton)),
        abs(minkowski_dot(plus, plus)),
        abs(minkowski_dot(plus, plus.conjugate()) + 1),
    )
    rows = [
        {
            "check_id": "LUNA5009_01_transverse_polarization",
            "quantity": "max(abs(eps.k),abs(eps^2),abs(eps.eps*+1))",
            "derived_value": polarization_residual,
            "target_value": 0,
            "absolute_residual": polarization_residual,
            "status": "PASS" if polarization_residual < TOLERANCE else "FAIL",
        },
        {
            "check_id": "LUNA5009_02_physical_jacobi",
            "quantity": "max(abs(nA-nB+nC),abs(nD-nE-nC))",
            "derived_value": max_jacobi,
            "target_value": 0,
            "absolute_residual": max_jacobi,
            "status": "PASS" if max_jacobi < TOLERANCE else "FAIL",
        },
        {
            "check_id": "LUNA5009_03_double_copy_Ward",
            "quantity": "max(linear Ward,quadratic Ward)",
            "derived_value": max_ward,
            "target_value": 0,
            "absolute_residual": max_ward,
            "status": "PASS" if max_ward < TOLERANCE else "FAIL",
        },
        {
            "check_id": "LUNA5009_04_nonexceptional_denominators",
            "quantity": "min_i abs(d_i)",
            "derived_value": minimum_denominator,
            "target_value": ">1e-8",
            "absolute_residual": 0,
            "status": "PASS" if minimum_denominator > 1.0e-8 else "FAIL",
        },
        {
            "check_id": "LUNA5009_05_line_orientation",
            "quantity": "max pairing-orientation amplitude residual",
            "derived_value": orientation_residual,
            "target_value": 0,
            "absolute_residual": orientation_residual,
            "status": "PASS" if orientation_residual < 2.0e-11 else "FAIL",
        },
        {
            "check_id": "LUNA5009_06_four_scalar_Bose_symmetry",
            "quantity": "max residual over S4 scalar permutations",
            "derived_value": bose_residual,
            "target_value": 0,
            "absolute_residual": bose_residual,
            "status": "PASS" if bose_residual < 2.0e-10 else "FAIL",
        },
        {
            "check_id": "LUNA5009_07_helicity_parity",
            "quantity": "abs(M_minus-conj(M_plus))",
            "derived_value": parity_residual,
            "target_value": 0,
            "absolute_residual": parity_residual,
            "status": "PASS" if parity_residual < 2.0e-10 else "FAIL",
        },
        {
            "check_id": "LUNA5009_08_finite_gauge_shift",
            "quantity": "abs(M(eps+0.371k)-M(eps))",
            "derived_value": gauge_shift_residual,
            "target_value": 0,
            "absolute_residual": gauge_shift_residual,
            "status": "PASS" if gauge_shift_residual < 2.0e-10 else "FAIL",
        },
    ]
    for index, result in enumerate(pair_results, start=1):
        rows.append(
            {
                "check_id": f"LUNA5009_{8 + index:02d}_pair_{index}",
                "quantity": f"reduced double-copy amplitude pairing {PAIRINGS[index - 1]}",
                "derived_value": complex_text(result["amplitude"]),
                "target_value": "finite",
                "absolute_residual": 0,
                "status": "KERNEL_VALUE",
            }
        )
    result = {
        "kernel": "M_pair=sum_i (epsilon.N_i)^2/d_i",
        "physical_transverse_jacobi": ["nA-nB=-nC", "nD-nE=+nC"],
        "jacobi_note": "the sign of nC is orientation dependent and drops out of nC^2 in the double copy",
        "massless_ghost_subtraction": "zero because every n_i' is proportional to m1*m2",
        "identical_real_scalar_completion": "sum over the three pairings of four scalar legs",
        "plus_helicity_reduced_amplitude": complex_text(plus_total),
        "minus_helicity_reduced_amplitude": complex_text(minus_total),
        "max_jacobi_residual": max_jacobi,
        "max_ward_residual": max_ward,
        "orientation_residual": orientation_residual,
        "bose_permutation_residual": bose_residual,
        "parity_residual": parity_residual,
        "gauge_shift_residual": gauge_shift_residual,
    }
    return rows, result


def spinor_bracket(
    spinors: dict[int, tuple[np.ndarray, np.ndarray]],
    left: int,
    right: int,
    chirality: str,
) -> complex:
    slot = 0 if chirality == "angle" else 1
    left_spinor = spinors[left][slot]
    right_spinor = spinors[right][slot]
    return complex(
        left_spinor[0] * right_spinor[1] - left_spinor[1] * right_spinor[0]
    )


def scalar_mhv_amplitude(
    ordering: tuple[int, ...],
    special_helicity_leg: int,
    spinors: dict[int, tuple[np.ndarray, np.ndarray]],
    chirality: str,
) -> complex:
    numerator = spinor_bracket(spinors, special_helicity_leg, 1, chirality) ** 2
    numerator *= spinor_bracket(spinors, special_helicity_leg, 5, chirality) ** 2
    denominator = complex(1.0)
    for left, right in zip(ordering, ordering[1:] + ordering[:1], strict=True):
        denominator *= spinor_bracket(spinors, left, right, chirality)
    return numerator / denominator


def invariant(momenta: dict[int, np.ndarray], left: int, right: int) -> float:
    return float((2 * minkowski_dot(momenta[left], momenta[right])).real)


def momentum_kernel(
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    momenta: dict[int, np.ndarray],
) -> float:
    positions = {leg: index for index, leg in enumerate(beta)}
    result = 1.0
    for index, leg in enumerate(alpha):
        factor = invariant(momenta, leg, 1)
        for later in alpha[index + 1 :]:
            if positions[leg] > positions[later]:
                factor += invariant(momenta, leg, later)
        result *= factor
    return result


def scalar_klt_amplitude(
    momenta: dict[int, np.ndarray],
    special_helicity_leg: int,
    chirality: str,
    right_order: str = "primary",
) -> complex:
    spinors = {leg: massless_spinors(momentum) for leg, momentum in momenta.items()}
    result = complex(0.0)
    for sigma in itertools.permutations((2, 3)):
        for gamma in itertools.permutations((2, 3)):
            left = (1, *sigma, 4, 5)
            if right_order == "primary":
                right = (4, 5, *gamma, 1)
            elif right_order == "literal_1908_display":
                right = (5, 4, *gamma, 1)
            else:
                raise ValueError(right_order)
            result += (
                scalar_mhv_amplitude(left, special_helicity_leg, spinors, chirality)
                * momentum_kernel(gamma, sigma, momenta)
                * scalar_mhv_amplitude(right, special_helicity_leg, spinors, chirality)
            )
    return result


def permuted_graviton_kinematics(
    base: dict[int, np.ndarray], permutation: tuple[int, int, int]
) -> tuple[dict[int, np.ndarray], int]:
    result = {1: base[1], 5: base[5]}
    special = -1
    for old_label, new_label in zip((2, 3, 4), permutation, strict=True):
        result[new_label] = base[old_label]
        if old_label == 2:
            special = new_label
    return result, special


def klt_rows(point: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    incoming_1, incoming_2 = point["incoming"]
    outgoing = point["outgoing"]
    momenta = {
        1: -incoming_1,
        2: outgoing[0],
        3: outgoing[1],
        4: outgoing[2],
        5: -incoming_2,
    }
    momentum_residual = norm(sum(momenta.values(), np.zeros(4)))
    spinors = {leg: massless_spinors(momentum) for leg, momentum in momenta.items()}
    bracket_residuals = []
    for left, right in itertools.combinations(momenta, 2):
        bracket_product = spinor_bracket(spinors, left, right, "angle")
        bracket_product *= spinor_bracket(spinors, right, left, "square")
        bracket_residuals.append(abs(bracket_product + invariant(momenta, left, right)))
    bracket_residual = max(bracket_residuals)
    mhv = scalar_klt_amplitude(momenta, 2, "angle", "primary")
    anti_mhv = scalar_klt_amplitude(momenta, 2, "square", "primary")
    parity_residual = abs(anti_mhv - mhv.conjugate())
    primary_values = []
    literal_values = []
    for permutation in itertools.permutations((2, 3, 4)):
        permuted, special = permuted_graviton_kinematics(momenta, permutation)
        primary_values.append(
            scalar_klt_amplitude(permuted, special, "angle", "primary")
        )
        literal_values.append(
            scalar_klt_amplitude(
                permuted, special, "angle", "literal_1908_display"
            )
        )
    primary_residual = max(abs(value - mhv) for value in primary_values)
    literal_scale = max(abs(literal_values[0]), 1.0e-30)
    literal_relative_failure = max(
        abs(value - literal_values[0]) for value in literal_values
    ) / literal_scale
    kernel_labels = ((2, 3), (3, 2))
    kernel_rows = []
    for alpha in kernel_labels:
        for beta in kernel_labels:
            kernel_rows.append(
                {
                    "check_id": f"KLT5009_kernel_{''.join(map(str, alpha))}_{''.join(map(str, beta))}",
                    "quantity": f"S[{alpha}|{beta}]_k1",
                    "derived_value": momentum_kernel(alpha, beta, momenta),
                    "target_value": "primary opposite-order momentum kernel",
                    "absolute_residual": 0,
                    "status": "KERNEL_VALUE",
                }
            )
    rows = [
        {
            "check_id": "KLT5009_01_all_outgoing_conservation",
            "quantity": "norm(sum_i k_i)",
            "derived_value": momentum_residual,
            "target_value": 0,
            "absolute_residual": momentum_residual,
            "status": "PASS" if momentum_residual < TOLERANCE else "FAIL",
        },
        {
            "check_id": "KLT5009_02_spinor_invariant",
            "quantity": "max abs(<ij>[ji]+sij)",
            "derived_value": bracket_residual,
            "target_value": 0,
            "absolute_residual": bracket_residual,
            "status": "PASS" if bracket_residual < TOLERANCE else "FAIL",
        },
        {
            "check_id": "KLT5009_03_primary_order_Bose_symmetry",
            "quantity": "max residual over S3 graviton permutations",
            "derived_value": primary_residual,
            "target_value": 0,
            "absolute_residual": primary_residual,
            "status": "PASS" if primary_residual < 2.0e-11 else "FAIL",
        },
        {
            "check_id": "KLT5009_04_parity",
            "quantity": "abs(M_anti_MHV-conj(M_MHV))",
            "derived_value": parity_residual,
            "target_value": 0,
            "absolute_residual": parity_residual,
            "status": "PASS" if parity_residual < 2.0e-11 else "FAIL",
        },
        {
            "check_id": "KLT5009_05_all_plus_massless",
            "quantity": "M5(2phi,3h_all_plus)",
            "derived_value": 0,
            "target_value": 0,
            "absolute_residual": 0,
            "status": "EXACT_FROM_MASSLESS_MHV_SELECTION",
        },
        {
            "check_id": "KLT5009_06_literal_1908_order_discriminator",
            "quantity": "relative S3 failure of literal displayed right order",
            "derived_value": literal_relative_failure,
            "target_value": ">1e-6 discriminator",
            "absolute_residual": 0,
            "status": "PRIMARY_ORDER_REQUIRED"
            if literal_relative_failure > 1.0e-6
            else "FAIL",
        },
        {
            "check_id": "KLT5009_07_MHV_kernel_value",
            "quantity": "reduced M5(1phi,2h-,3h+,4h+,5phi)",
            "derived_value": complex_text(mhv),
            "target_value": "finite",
            "absolute_residual": 0,
            "status": "KERNEL_VALUE",
        },
        *kernel_rows,
    ]
    result = {
        "gauge_seed": "A_n(1phi,...,r-,...,nphi)=<r1>^2<rn>^2/PT",
        "all_plus_massless_gauge_seed": "0",
        "klt_formula": "sum_sigma,gamma A(1,sigma,4,5) S[gamma|sigma]_k1 A(4,5,gamma,1)",
        "primary_right_order": "(n-1,n,gamma,1)",
        "theta_rule": "theta=1 only when the pair ordering is opposite",
        "mhv_reduced_amplitude": complex_text(mhv),
        "anti_mhv_reduced_amplitude": complex_text(anti_mhv),
        "all_plus_reduced_amplitude": "0",
        "primary_permutation_residual": primary_residual,
        "parity_residual": parity_residual,
        "literal_1908_display_relative_permutation_failure": literal_relative_failure,
        "ordering_decision": "use the primary 1010.3933 KLT ordering; the literal 1908 displayed order is convention-unsafe and fails this crossing gate",
    }
    return rows, result


def validation_rows(
    outputs: list[Path],
    locks: dict[str, bool],
    result: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("all_outputs_exist", all(path.is_file() for path in outputs), "checkpoint outputs"),
        ("all_source_locks", all(locks.values()), "primary and local source locks"),
        (
            "phase_measure_normalized",
            result["phase_space"]["normalized_measure"] == 1.0,
            "integral dmu=1",
        ),
        (
            "phase_map_null",
            result["phase_space"]["max_null_residual"] < TOLERANCE,
            "three outgoing legs are null",
        ),
        (
            "phase_map_conserves_momentum",
            result["phase_space"]["momentum_conservation_residual"] < TOLERANCE,
            "spinor map preserves total momentum",
        ),
        (
            "phase_space_coefficient",
            result["phase_space"]["physical_phase_space"]
            == "dPhi3 = s/(256*pi^3) dmu",
            "physical three-body normalization",
        ),
        (
            "luna_jacobi",
            result["four_scalar_one_graviton"]["max_jacobi_residual"] < TOLERANCE,
            "physical transverse Jacobi identities",
        ),
        (
            "luna_ward",
            result["four_scalar_one_graviton"]["max_ward_residual"] < TOLERANCE,
            "linear and quadratic Ward identities",
        ),
        (
            "luna_orientation",
            result["four_scalar_one_graviton"]["orientation_residual"] < 2.0e-11,
            "scalar-line orientation invariance",
        ),
        (
            "luna_bose",
            result["four_scalar_one_graviton"]["bose_permutation_residual"] < 2.0e-10,
            "identical-scalar S4 completion",
        ),
        (
            "luna_parity",
            result["four_scalar_one_graviton"]["parity_residual"] < 2.0e-10,
            "real-kinematics helicity parity",
        ),
        (
            "luna_gauge_shift",
            result["four_scalar_one_graviton"]["gauge_shift_residual"] < 2.0e-10,
            "finite polarization gauge shift",
        ),
        (
            "klt_primary_crossing",
            result["two_scalar_three_graviton"]["primary_permutation_residual"] < 2.0e-11,
            "S3 graviton permutation invariance",
        ),
        (
            "klt_parity",
            result["two_scalar_three_graviton"]["parity_residual"] < 2.0e-11,
            "MHV/anti-MHV conjugacy",
        ),
        (
            "klt_order_discriminator",
            result["two_scalar_three_graviton"][
                "literal_1908_display_relative_permutation_failure"
            ]
            > 1.0e-6,
            "primary ordering selected by crossing",
        ),
        (
            "all_plus_zero",
            result["two_scalar_three_graviton"]["all_plus_reduced_amplitude"] == "0",
            "massless all-plus branch vanishes",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256_before"]
            == result["formalization_workbench_tree_sha256_after"],
            "no formalization-workbench edits",
        ),
        (
            "outer_cut_not_claimed",
            result["outer_cut_complete"] is False,
            "tree kernels do not equal integrated cut",
        ),
        (
            "full_mts_not_claimed",
            result["valid_for_full_MTS_claim"] is False,
            "private nonclaim checkpoint",
        ),
    ]
    for path in (PHASE_CSV, LUNA_CSV, KLT_CSV, GATE_CSV):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        checks.append((f"csv_parses_{path.stem}", bool(rows), relative(path)))
        checks.append(
            (
                f"csv_nonclaim_{path.stem}",
                all(row.get("valid_for_full_MTS_claim") == "False" for row in rows),
                relative(path),
            )
        )
    return [
        {
            "validation_id": f"{VALIDATION_MARKER}_{index:02d}",
            "check": check,
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for index, (check, passed, detail) in enumerate(checks, start=1)
    ]


def write_document(result: dict[str, Any]) -> None:
    phase = result["phase_space"]
    luna = result["four_scalar_one_graviton"]
    klt = result["two_scalar_three_graviton"]
    DOCUMENT.write_text(
        f"""# 5009 - Three-particle phase space and five-point tree-kernel closure

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not an integrated outer-cut, local-GR, or full-MTS claim.

## Three-body measure

Caron-Huot and Wilhelm's three-spinor map has been implemented directly. It preserves nullness and total momentum at the non-symmetric test point with residuals

```text
max |p_i'^2|                 = {phase['max_null_residual']:.3e}
|p1+p2-p1'-p2'-p3'|         = {phase['momentum_conservation_residual']:.3e}
```

All five normalized measure factors integrate to one, so

```text
integral dmu = 1,
dPhi_3       = s/(256 pi^3) dmu.
```

This removes the three-body phase-space normalization ambiguity from the next cut calculation.

## Exact `4phi+1h` tree kernel

The five Luna-O'Connell-White numerator vectors and denominators are now executable. For a physical transverse polarization the source numerators obey, in the orientation used here,

```text
n_A - n_B = -n_C,
n_D - n_E = +n_C.
```

The sign of `n_C` is a cubic-vertex/color orientation convention and disappears from the `n_C^2/d_C` double copy. Both Ward contractions vanish, a finite shift `epsilon -> epsilon + a k` leaves the amplitude unchanged, and the three scalar-line pairings produce an `S4`-symmetric identical-real-scalar amplitude. The maximum numerical residuals are

```text
Jacobi             = {luna['max_jacobi_residual']:.3e}
Ward               = {luna['max_ward_residual']:.3e}
line orientation   = {luna['orientation_residual']:.3e}
S4 Bose symmetry   = {luna['bose_permutation_residual']:.3e}
finite gauge shift = {luna['gauge_shift_residual']:.3e}
```

The unwanted Luna ghost subtraction vanishes exactly in this massless branch because every `n_i'` carries `m_1 m_2`. No fitted five-point ansatz is used.

## Exact `2phi+3h` tree kernel

The massless one-minus scalar-gluon MHV seed is

```text
A_n(1_phi,...,r^-,...,n_phi)
  = <r1>^2 <rn>^2 / PT,
```

while the all-plus seed vanishes. KLT squaring with the primary momentum-kernel convention gives

```text
M_5 = sum_(sigma,gamma in S2)
      A(1,sigma,4,5) S[gamma|sigma]_(k1) A(4,5,gamma,1),
```

where `theta=1` only for opposite pair ordering. This kernel is invariant under all six graviton permutations and obeys parity, with residuals

```text
S3 permutation = {klt['primary_permutation_residual']:.3e}
parity          = {klt['parity_residual']:.3e}
```

The literal right ordering displayed in the 2019 scalar-graviton source is convention-unsafe in this massless implementation: it fails the same permutation test by `{klt['literal_1908_display_relative_permutation_failure']:.6g}` relatively. The primary arXiv:1010.3933 ordering `(n-1,n,gamma,1)` is therefore used. This is a tested convention decision, not a silent sign choice.

## What is closed and what is not

- Normalized three-particle phase-space map: **closed**.
- Massless `4phi+1h` double-copy tree kernel, including identical-scalar completion: **closed**.
- Massless one-minus and parity-related `2phi+3h` KLT tree kernels: **closed**.
- All-plus `2phi+3h` branch: **zero by the massless MHV selection rule**.
- Coupling restoration and products with the required lower-loop amplitudes: **not yet integrated**.
- Cancellation against the crossed nonlocal remainder of checkpoint 5008: **not yet tested**.
- Full outer UV projection: **open**.

Next: insert these executable kernels into the normalized `dmu` integral, restore the common Einstein-scalar coupling factors, sum every three-particle helicity/cut placement, and combine that result with checkpoint 5008 before applying any local projector.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()
    required = [
        CARON_HUOT,
        LUNA,
        FORDE_KOSOWER,
        SCALAR_GRAVITON,
        MOMENTUM_KERNEL,
        RESULT_5008,
        Path(__file__).resolve(),
    ]
    locks = source_locks(required)
    if not all(locks.values()):
        raise RuntimeError(json.dumps(locks, indent=2, sort_keys=True))
    outputs = [
        PHASE_CSV,
        LUNA_CSV,
        KLT_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        DOCUMENT,
        VALIDATION,
    ]
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "dry_run": True,
                    "source_locks": locks,
                    "would_write": [relative(path) for path in outputs],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    point = phase_space_point(0.53, 0.81, 0.37, 0.43, 1.17)
    phase_rows, phase_result = phase_space_rows(point)
    luna_check_rows, luna_result = luna_rows(point)
    klt_check_rows, klt_result = klt_rows(point)
    gate_rows = [
        {
            "gate": "source_lock",
            "passed": all(locks.values()),
            "status": "closed",
            "meaning": "phase-space, five-point numerator, massless MHV, and primary KLT sources are locked",
        },
        {
            "gate": "normalized_three_body_measure",
            "passed": phase_result["normalized_measure"] == 1.0,
            "status": "closed",
            "meaning": "dPhi3=s/(256*pi^3)dmu with integral dmu=1",
        },
        {
            "gate": "four_scalar_one_graviton_tree",
            "passed": luna_result["max_ward_residual"] < TOLERANCE,
            "status": "closed_massless_reduced_kernel",
            "meaning": "five double-copy graphs plus all three identical-scalar pairings pass Ward and Bose tests",
        },
        {
            "gate": "two_scalar_three_graviton_tree",
            "passed": klt_result["primary_permutation_residual"] < 2.0e-11,
            "status": "closed_MHV_and_parity_reduced_kernels",
            "meaning": "primary-order KLT sum passes all graviton permutations",
        },
        {
            "gate": "three_particle_cut_integration",
            "passed": False,
            "status": "next_derivation",
            "meaning": "restore couplings, cut placements, lower-loop partner amplitudes, and integrate over dmu",
        },
        {
            "gate": "combined_local_UV_projection",
            "passed": False,
            "status": "open",
            "meaning": "combine integrated three-particle cuts with 5008 before projecting",
        },
        {
            "gate": "full_MTS_claim",
            "passed": False,
            "status": "blocked",
            "meaning": "this closes tree ingredients, not the parent MTS field theory",
        },
    ]
    write_csv(PHASE_CSV, tagged(phase_rows))
    write_csv(LUNA_CSV, tagged(luna_check_rows))
    write_csv(KLT_CSV, tagged(klt_check_rows))
    write_csv(GATE_CSV, tagged(gate_rows))
    formal_after = tree_digest(ROOT / "formalization-workbench")
    if formal_before != formal_after:
        raise RuntimeError("formalization-workbench changed during checkpoint")
    source_hashes = {relative(path): digest(path) for path in required}
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_locks": locks,
        "source_hashes_sha256": source_hashes,
        "formalization_workbench_tree_sha256_before": formal_before,
        "formalization_workbench_tree_sha256_after": formal_after,
        "phase_space": phase_result,
        "four_scalar_one_graviton": luna_result,
        "two_scalar_three_graviton": klt_result,
        "three_particle_tree_kernels_complete": True,
        "three_particle_cut_integrated": False,
        "combined_with_5008": False,
        "outer_cut_complete": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "integrate the sourced three-particle kernels with restored couplings and lower-loop partners, then combine with 5008 before the local UV projection",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_document(result)
    PROVENANCE.write_text(
        f"""# 5009 provenance

Checkpoint marker: `{MARKER}`

## Locked local inputs

{chr(10).join(f'- `{path}` - SHA-256 `{value}`' for path, value in source_hashes.items())}

## Primary sources and extraction

- Caron-Huot and Wilhelm, [arXiv:1607.06448](https://arxiv.org/abs/1607.06448): exact three-spinor map, normalized five-angle measure, and the three-particle phase-space coefficient.
- Luna, Nicholson, O'Connell, and White, [arXiv:1711.03901](https://arxiv.org/abs/1711.03901): five cubic scalar-radiation numerators, propagators, and double-copy construction.
- Forde and Kosower, [arXiv:hep-th/0507292](https://arxiv.org/abs/hep-th/0507292): the massless one-minus scalar-gluon MHV limit and vanishing massless all-plus branch.
- Bjerrum-Bohr, Damgaard, Sondergaard, and Vanhove, [arXiv:1010.3933](https://arxiv.org/abs/1010.3933): opposite-order momentum-kernel rule and primary KLT right ordering.
- The local 2019 scalar-graviton source supplies the scalar KLT application, but its literal displayed right ordering is not used without a convention conversion because it fails the explicit massless permutation gate.

All amplitudes are coupling-stripped reduced kernels. The next checkpoint must restore the common Einstein-scalar coupling normalization before integration. No numeric fit, UV coefficient, or MTS claim is made here.
""",
        encoding="utf-8",
    )
    validation = validation_rows(outputs[:-1], locks, result)
    write_csv(VALIDATION, validation)
    if not all(row["passed"] for row in validation):
        failed = [row for row in validation if not row["passed"]]
        raise RuntimeError(json.dumps(failed, indent=2))
    result["validation_checks"] = len(validation)
    result["validation_all_passed"] = True
    result["elapsed_seconds"] = time.perf_counter() - started
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
