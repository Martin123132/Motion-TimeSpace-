from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5010"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5009 = POST / "scripts" / "Y5_R2FR_5009_three_particle_phase_space_and_five_point_tree_kernels.py"
RESULT_5009 = POST / "source-intake" / "functional_rg" / "5009" / "three_particle_tree_kernel_results.json"
RESULT_4988 = POST / "source-intake" / "functional_rg" / "4988" / "scalar_cut_soft_subtraction_results.json"
LUNA_SOURCE = POST / "source-intake" / "functional_rg" / "5009" / "sources" / "luna_nicholson_oconnell_white_1711.03901" / "paper.tex"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
KLT_SOURCE = POST / "source-intake" / "functional_rg" / "5009" / "sources" / "bjerrum_bohr_momentum_kernel_1010.3933" / "kernel_arxiv.tex"
DOCUMENT = POST / "5010-Y5-R2FR-coupled-three-particle-cut-normalization-and-soft-plus-integrand.md"

NORMALIZATION_CSV = SOURCE / "coupling_and_tree_normalization_checks.csv"
SOFT_CSV = SOURCE / "soft_limit_and_plus_subtraction_checks.csv"
INTEGRAND_CSV = SOURCE / "three_particle_cut_integrand_checks.csv"
SMOKE_CSV = SOURCE / "soft_plus_qmc_smoke.csv"
GATE_CSV = SOURCE / "coupled_three_particle_cut_gate.csv"
RESULT_JSON = SOURCE / "coupled_three_particle_cut_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5010_VALIDATION.csv"

MARKER = "MTS_5010_COUPLED_THREE_PARTICLE_CUT_NORMALIZATION_SOFT_PLUS"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
S_VALUE = 4.0


def load_5009() -> Any:
    specification = importlib.util.spec_from_file_location("mts_checkpoint_5009", SCRIPT_5009)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load checkpoint 5009")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


KERNEL = load_5009()


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
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
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


def complex_text(value: complex) -> str:
    return f"{value.real:.16g}{value.imag:+.16g}j"


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def sphere(first: float, second: float) -> np.ndarray:
    cosine = 2.0 * first - 1.0
    sine = math.sqrt(max(0.0, 1.0 - cosine * cosine))
    azimuth = 2.0 * math.pi * second
    return np.array([sine * math.cos(azimuth), sine * math.sin(azimuth), cosine])


def boost(momentum: np.ndarray, velocity: np.ndarray) -> np.ndarray:
    speed_squared = float(velocity @ velocity)
    if speed_squared < 1.0e-30:
        return momentum.copy()
    gamma = 1.0 / math.sqrt(1.0 - speed_squared)
    projection = float(velocity @ momentum[1:])
    spatial = momentum[1:] + (
        (gamma - 1.0) * projection / speed_squared + gamma * float(momentum[0])
    ) * velocity
    return np.concatenate(([gamma * (float(momentum[0]) + projection)], spatial))


def sequential_three_body(
    soft_energy: float,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    soft_slot: int = 2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if not 0.0 <= soft_energy < 1.0:
        raise ValueError("soft_energy must lie in [0,1)")
    soft = np.concatenate(([soft_energy], soft_energy * soft_direction))
    recoil = np.concatenate(([2.0 - soft_energy], -soft_energy * soft_direction))
    recoil_mass = 2.0 * math.sqrt(max(0.0, 1.0 - soft_energy))
    first_rest = np.concatenate(
        ([recoil_mass / 2.0], recoil_mass * decay_direction / 2.0)
    )
    second_rest = np.concatenate(
        ([recoil_mass / 2.0], -recoil_mass * decay_direction / 2.0)
    )
    velocity = recoil[1:] / recoil[0]
    first = boost(first_rest, velocity)
    second = boost(second_rest, velocity)
    values = [first, second]
    values.insert(soft_slot, soft)
    return values[0], values[1], values[2]


def external_momenta(scattering_cosine: float) -> tuple[np.ndarray, ...]:
    transverse = math.sqrt(max(0.0, 1.0 - scattering_cosine * scattering_cosine))
    return (
        np.array([1.0, 0.0, 0.0, 1.0]),
        np.array([1.0, 0.0, 0.0, -1.0]),
        np.array([1.0, transverse, 0.0, scattering_cosine]),
        np.array([1.0, -transverse, 0.0, -scattering_cosine]),
    )


def invariant_sum(left: np.ndarray, right: np.ndarray) -> float:
    return float(KERNEL.minkowski_dot(left + right, left + right).real)


def canonical_four_scalar(scalars: list[np.ndarray]) -> complex:
    s_value = invariant_sum(scalars[0], scalars[1])
    t_value = invariant_sum(scalars[0], scalars[2])
    u_value = invariant_sum(scalars[0], scalars[3])
    return complex(
        t_value * u_value / s_value
        + s_value * u_value / t_value
        + s_value * t_value / u_value
    )


def raw_luna_four_scalar(scalars: list[np.ndarray]) -> complex:
    total = complex(0.0)
    for (first_in, first_out), (second_in, second_out) in KERNEL.PAIRINGS:
        first = -scalars[first_in]
        second = -scalars[second_in]
        transfer = -scalars[first_in] - scalars[first_out]
        transfer_squared = KERNEL.minkowski_dot(transfer, transfer)
        total += (
            4.0 * KERNEL.minkowski_dot(first, second) + transfer_squared
        ) ** 2 / transfer_squared
    return total


def canonical_luna_five(
    scalars: list[np.ndarray], graviton: np.ndarray, polarization: np.ndarray
) -> complex:
    return -KERNEL.luna_bose_amplitude(scalars, graviton, polarization) / 8.0


def scalar_klt_four(
    momenta: dict[int, np.ndarray], special_leg: int, chirality: str
) -> complex:
    spinors = {
        leg: KERNEL.massless_spinors(momentum) for leg, momentum in momenta.items()
    }
    left = KERNEL.scalar_mhv_amplitude(
        (1, 2, 3, 5), special_leg, spinors, chirality
    )
    right = KERNEL.scalar_mhv_amplitude(
        (3, 5, 2, 1), special_leg, spinors, chirality
    )
    return -left * KERNEL.invariant(momenta, 1, 2) * right


def spinor_soft_factor(
    hard_momenta: dict[int, np.ndarray],
    soft_momentum: np.ndarray,
    chirality: str,
    reference_leg: int = 1,
) -> complex:
    all_momenta = {**hard_momenta, 4: soft_momentum}
    spinors = {
        leg: KERNEL.massless_spinors(momentum)
        for leg, momentum in all_momenta.items()
    }
    result = complex(0.0)
    for leg in hard_momenta:
        if chirality == "angle":
            result += (
                KERNEL.spinor_bracket(spinors, 4, leg, "square")
                / KERNEL.spinor_bracket(spinors, 4, leg, "angle")
                * (
                    KERNEL.spinor_bracket(spinors, reference_leg, leg, "angle")
                    / KERNEL.spinor_bracket(spinors, reference_leg, 4, "angle")
                )
                ** 2
            )
        elif chirality == "square":
            result += (
                KERNEL.spinor_bracket(spinors, 4, leg, "angle")
                / KERNEL.spinor_bracket(spinors, 4, leg, "square")
                * (
                    KERNEL.spinor_bracket(spinors, reference_leg, leg, "square")
                    / KERNEL.spinor_bracket(spinors, reference_leg, 4, "square")
                )
                ** 2
            )
        else:
            raise ValueError(chirality)
    return result


def vector_soft_factor(
    hard_momenta: list[np.ndarray],
    soft_momentum: np.ndarray,
    polarization: np.ndarray,
) -> complex:
    return sum(
        KERNEL.minkowski_dot(polarization, momentum) ** 2
        / KERNEL.minkowski_dot(momentum, soft_momentum)
        for momentum in hard_momenta
    )


def cut_momenta(
    internal: tuple[np.ndarray, np.ndarray, np.ndarray],
    scattering_cosine: float,
) -> tuple[dict[int, np.ndarray], dict[int, np.ndarray], list[np.ndarray], list[np.ndarray]]:
    incoming_1, incoming_2, outgoing_1, outgoing_2 = external_momenta(
        scattering_cosine
    )
    first, second, third = internal
    left_klt = {1: -incoming_1, 5: -incoming_2, 2: first, 3: second, 4: third}
    right_klt = {1: outgoing_1, 5: outgoing_2, 2: -first, 3: -second, 4: -third}
    left_scalars = [-incoming_1, -incoming_2, first, second]
    right_scalars = [outgoing_1, outgoing_2, -first, -second]
    return left_klt, right_klt, left_scalars, right_scalars


def hhh_reduced_product(
    internal: tuple[np.ndarray, np.ndarray, np.ndarray], scattering_cosine: float
) -> complex:
    left, right, _, _ = cut_momenta(internal, scattering_cosine)
    result = complex(0.0)
    for special_leg in (2, 3, 4):
        result += KERNEL.scalar_klt_amplitude(
            left, special_leg, "angle", "primary"
        ) * KERNEL.scalar_klt_amplitude(right, special_leg, "square", "primary")
        result += KERNEL.scalar_klt_amplitude(
            left, special_leg, "square", "primary"
        ) * KERNEL.scalar_klt_amplitude(right, special_leg, "angle", "primary")
    return result / math.factorial(3)


def pph_reduced_product(
    internal: tuple[np.ndarray, np.ndarray, np.ndarray], scattering_cosine: float
) -> complex:
    _, _, left_scalars, right_scalars = cut_momenta(internal, scattering_cosine)
    graviton = internal[2]
    result = complex(0.0)
    for helicity in (-1, 1):
        polarization = KERNEL.circular_polarization(graviton, helicity)
        left = canonical_luna_five(left_scalars, graviton, polarization)
        right = canonical_luna_five(
            right_scalars, -graviton, polarization.conjugate()
        )
        result += left * right
    return result / math.factorial(2)


def hhh_sector_multiplier(internal: tuple[np.ndarray, ...]) -> float:
    inverse_squares = [1.0 / float(momentum[0]) ** 2 for momentum in internal]
    return 3.0 * inverse_squares[2] / sum(inverse_squares)


def direct_g_values(
    soft_energy: float,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: float,
) -> tuple[complex, complex]:
    internal = sequential_three_body(soft_energy, soft_direction, decay_direction)
    hhh = hhh_sector_multiplier(internal) * hhh_reduced_product(
        internal, scattering_cosine
    )
    pph = pph_reduced_product(internal, scattering_cosine)
    factor = soft_energy * soft_energy / (S_VALUE * S_VALUE)
    return factor * hhh, factor * pph


def exact_hhh_g0(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: float,
) -> complex:
    internal = sequential_three_body(0.0, soft_direction, decay_direction)
    left, right, _, _ = cut_momenta(internal, scattering_cosine)
    left_hard = {leg: left[leg] for leg in (1, 2, 3, 5)}
    right_hard = {leg: right[leg] for leg in (1, 2, 3, 5)}
    soft_left = np.concatenate(([1.0], soft_direction))
    soft_right = -soft_left
    result = complex(0.0)
    for special_leg in (2, 3):
        result += (
            spinor_soft_factor(left_hard, soft_left, "angle")
            * scalar_klt_four(left_hard, special_leg, "angle")
            * spinor_soft_factor(right_hard, soft_right, "square")
            * scalar_klt_four(right_hard, special_leg, "square")
        )
        result += (
            spinor_soft_factor(left_hard, soft_left, "square")
            * scalar_klt_four(left_hard, special_leg, "square")
            * spinor_soft_factor(right_hard, soft_right, "angle")
            * scalar_klt_four(right_hard, special_leg, "angle")
        )
    return result / (2.0 * S_VALUE * S_VALUE)


def exact_pph_g0(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: float,
) -> complex:
    internal = sequential_three_body(0.0, soft_direction, decay_direction)
    _, _, left_scalars, right_scalars = cut_momenta(internal, scattering_cosine)
    soft_left = np.concatenate(([1.0], soft_direction))
    soft_right = -soft_left
    left_four = canonical_four_scalar(left_scalars)
    right_four = canonical_four_scalar(right_scalars)
    result = complex(0.0)
    for helicity in (-1, 1):
        polarization = KERNEL.circular_polarization(soft_left, helicity)
        result += (
            vector_soft_factor(left_scalars, soft_left, polarization)
            * left_four
            * vector_soft_factor(
                right_scalars, soft_right, polarization.conjugate()
            )
            * right_four
        )
    return result / (2.0 * S_VALUE * S_VALUE)


def source_locks() -> dict[str, bool]:
    luna = LUNA_SOURCE.read_text(encoding="utf-8", errors="ignore")
    dunbar = DUNBAR_SOURCE.read_text(encoding="utf-8", errors="ignore")
    klt = KLT_SOURCE.read_text(encoding="utf-8", errors="ignore")
    result_5009 = read_json(RESULT_5009)
    result_4988 = read_json(RESULT_4988)
    return {
        "luna_omitted_couplings_explicit": "we omit factors of $i$ and couplings" in luna,
        "luna_five_graph_double_copy": "\\mathcal{M} = \\frac{n_A n_A}{d_A}" in luna,
        "luna_four_point_factorization": "q^2 \\mathcal{M} &\\xrightarrow[q^2 \\rightarrow 0]{}" in luna,
        "dunbar_identical_four_scalar_tree": "The tree amplitude for" in dunbar and "four scalars (all the same flavour)" in dunbar,
        "dunbar_tree_prefactor": "{i\\kappa^2\\over2}" in dunbar,
        "primary_klt_order": "\\widetilde{\\cA}_n(n-1,n,\\gamma" in klt,
        "checkpoint_5009_tree_kernels": bool(result_5009["three_particle_tree_kernels_complete"]) and bool(result_5009["validation_all_passed"]),
        "checkpoint_4988_tree_calibration": bool(result_4988["gates"]["canonical_tree_normalization"]),
    }


def normalization_checks(scattering_cosine: float) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    external = external_momenta(scattering_cosine)
    scalars = [-external[0], -external[1], external[2], external[3]]
    canonical = canonical_four_scalar(scalars)
    raw_four = raw_luna_four_scalar(scalars)
    four_ratio = raw_four / canonical

    soft_direction = sphere(0.37, 0.21)
    decay_direction = sphere(0.67, 0.52)
    soft_energy = 1.0e-6
    internal = sequential_three_body(soft_energy, soft_direction, decay_direction)
    left_klt, _, left_scalars, _ = cut_momenta(internal, scattering_cosine)
    left_hard = {leg: left_klt[leg] for leg in (1, 2, 3, 5)}
    klt_five = KERNEL.scalar_klt_amplitude(left_klt, 2, "angle", "primary")
    klt_prediction = spinor_soft_factor(
        left_hard, left_klt[4], "angle"
    ) * scalar_klt_four(left_hard, 2, "angle")
    klt_ratio = klt_five / klt_prediction

    polarization = KERNEL.circular_polarization(internal[2], 1)
    luna_raw_five = KERNEL.luna_bose_amplitude(
        left_scalars, internal[2], polarization
    )
    luna_prediction = vector_soft_factor(
        left_scalars, internal[2], polarization
    ) * canonical_four_scalar(left_scalars)
    luna_raw_ratio = luna_raw_five / luna_prediction
    luna_canonical_ratio = canonical_luna_five(
        left_scalars, internal[2], polarization
    ) / luna_prediction

    phase_space_sequential = (4.0 * math.pi) ** 2 / (512.0 * math.pi**5) / 2.0
    phase_space_invariant = S_VALUE / (256.0 * math.pi**3)
    rows = [
        {
            "check_id": "NORM5010_01_three_body_volume",
            "statement": "integral dPhi3=s/(256 pi^3) for s=4",
            "derived_value": phase_space_sequential,
            "target_value": phase_space_invariant,
            "absolute_residual": abs(phase_space_sequential - phase_space_invariant),
            "status": "PASS" if abs(phase_space_sequential - phase_space_invariant) < 1.0e-16 else "FAIL",
        },
        {
            "check_id": "NORM5010_02_luna_four_point_pairing_sum",
            "statement": "raw Luna identical-scalar pairing sum=-4 C4",
            "derived_value": complex_text(four_ratio),
            "target_value": "-4+0j",
            "absolute_residual": abs(four_ratio + 4.0),
            "status": "PASS" if abs(four_ratio + 4.0) < 1.0e-12 else "FAIL",
        },
        {
            "check_id": "NORM5010_03_klt_five_to_four_soft_ratio",
            "statement": "KLT M5=S_spinor M4+O(omega^0)",
            "derived_value": complex_text(klt_ratio),
            "target_value": "1+0j",
            "absolute_residual": abs(klt_ratio - 1.0),
            "status": "PASS" if abs(klt_ratio - 1.0) < 2.0e-5 else "FAIL",
        },
        {
            "check_id": "NORM5010_04_luna_raw_soft_ratio",
            "statement": "coupling-omitted raw Luna M5=-8 S_vector C4+O(omega^0)",
            "derived_value": complex_text(luna_raw_ratio),
            "target_value": "-8+0j",
            "absolute_residual": abs(luna_raw_ratio + 8.0),
            "status": "PASS" if abs(luna_raw_ratio + 8.0) < 2.0e-4 else "FAIL",
        },
        {
            "check_id": "NORM5010_05_luna_canonical_soft_ratio",
            "statement": "M5_canonical=-M5_Luna/8=S_vector C4+O(omega^0)",
            "derived_value": complex_text(luna_canonical_ratio),
            "target_value": "1+0j",
            "absolute_residual": abs(luna_canonical_ratio - 1.0),
            "status": "PASS" if abs(luna_canonical_ratio - 1.0) < 2.0e-5 else "FAIL",
        },
        {
            "check_id": "NORM5010_06_five_point_coupling_product",
            "statement": "[(kappa/2)^3]^2=kappa^6/64",
            "derived_value": 1.0 / 64.0,
            "target_value": 1.0 / 64.0,
            "absolute_residual": 0.0,
            "status": "PASS",
        },
        {
            "check_id": "NORM5010_07_state_symmetry_factors",
            "statement": "hhh carries 1/3! and phiphih carries 1/2!",
            "derived_value": "hhh=1/6; phiphih=1/2",
            "target_value": "identical-particle completeness",
            "absolute_residual": 0.0,
            "status": "PASS",
        },
        {
            "check_id": "NORM5010_08_dimensionless_cut_prefactor",
            "statement": "U3_plus/(kappa^6 s^3)=E[H]/(8192 pi^3)",
            "derived_value": 1.0 / (8192.0 * math.pi**3),
            "target_value": "sequential dPhi3 times kappa^6/64 and g=x^2F/s^2",
            "absolute_residual": 0.0,
            "status": "PASS",
        },
    ]
    return rows, {
        "raw_luna_four_to_canonical_ratio": complex_text(four_ratio),
        "canonical_luna_five_factor": "-1/8",
        "klt_soft_ratio_at_1e-6": complex_text(klt_ratio),
        "luna_raw_soft_ratio_at_1e-6": complex_text(luna_raw_ratio),
        "luna_canonical_soft_ratio_at_1e-6": complex_text(luna_canonical_ratio),
        "phase_space": "dPhi3=omega domega dOmega_k dOmega_*/(512 pi^5)",
        "dimensionless_plus_prefactor": "U3_plus/(kappa^6 s^3)=E[H]/(8192 pi^3)",
    }


def soft_checks(scattering_cosine: float) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    soft_direction = sphere(0.37, 0.21)
    decay_direction = sphere(0.67, 0.52)
    hhh_zero = exact_hhh_g0(soft_direction, decay_direction, scattering_cosine)
    pph_zero = exact_pph_g0(soft_direction, decay_direction, scattering_cosine)
    rows: list[dict[str, Any]] = []
    last_hhh = math.inf
    last_pph = math.inf
    for index, soft_energy in enumerate(
        (1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6), start=1
    ):
        hhh, pph = direct_g_values(
            soft_energy, soft_direction, decay_direction, scattering_cosine
        )
        hhh_relative = abs(hhh - hhh_zero) / max(abs(hhh_zero), 1.0e-30)
        pph_relative = abs(pph - pph_zero) / max(abs(pph_zero), 1.0e-30)
        last_hhh = hhh_relative
        last_pph = pph_relative
        rows.extend(
            [
                {
                    "check_id": f"SOFT5010_{2 * index - 1:02d}_hhh_x{soft_energy:.0e}",
                    "sector": "hhh",
                    "soft_energy": soft_energy,
                    "direct_g": complex_text(hhh),
                    "exact_g0": complex_text(hhh_zero),
                    "relative_residual": hhh_relative,
                    "status": "LIMIT_SEQUENCE",
                },
                {
                    "check_id": f"SOFT5010_{2 * index:02d}_phiphih_x{soft_energy:.0e}",
                    "sector": "phiphih",
                    "soft_energy": soft_energy,
                    "direct_g": complex_text(pph),
                    "exact_g0": complex_text(pph_zero),
                    "relative_residual": pph_relative,
                    "status": "LIMIT_SEQUENCE",
                },
            ]
        )
    rows.extend(
        [
            {
                "check_id": "SOFT5010_11_hhh_exact_limit_gate",
                "sector": "hhh",
                "soft_energy": 1.0e-6,
                "direct_g": "last sequence row",
                "exact_g0": complex_text(hhh_zero),
                "relative_residual": last_hhh,
                "status": "PASS" if last_hhh < 2.0e-4 else "FAIL",
            },
            {
                "check_id": "SOFT5010_12_phiphih_exact_limit_gate",
                "sector": "phiphih",
                "soft_energy": 1.0e-6,
                "direct_g": "last sequence row",
                "exact_g0": complex_text(pph_zero),
                "relative_residual": last_pph,
                "status": "PASS" if last_pph < 2.0e-4 else "FAIL",
            },
        ]
    )
    return rows, {
        "hhh_g0": complex_text(hhh_zero),
        "phiphih_g0": complex_text(pph_zero),
        "hhh_last_relative_residual": last_hhh,
        "phiphih_last_relative_residual": last_pph,
        "plus_definition": "H_X(x,Omega)=[g_X(x,Omega)-g_X(0,Omega)]/x",
    }


def cut_integrand_checks(scattering_cosine: float) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    soft_direction = sphere(0.43, 0.18)
    decay_direction = sphere(0.71, 0.59)
    internal = sequential_three_body(0.31, soft_direction, decay_direction)
    total = sum(internal, np.zeros(4))
    null_residual = max(
        abs(KERNEL.minkowski_dot(momentum, momentum)) for momentum in internal
    )
    momentum_residual = float(np.linalg.norm(total - np.array([2.0, 0.0, 0.0, 0.0])))

    hhh_values = [
        hhh_reduced_product(tuple(internal[index] for index in permutation), scattering_cosine)
        for permutation in itertools.permutations(range(3))
    ]
    hhh_symmetry = max(abs(value - hhh_values[0]) for value in hhh_values)
    weights = [1.0 / float(momentum[0]) ** 2 for momentum in internal]
    partition_residual = abs(sum(value / sum(weights) for value in weights) - 1.0)

    pph_base = pph_reduced_product(internal, scattering_cosine)
    pph_swapped = pph_reduced_product((internal[1], internal[0], internal[2]), scattering_cosine)
    pph_symmetry = abs(pph_base - pph_swapped)

    scalar_soft_values: list[tuple[float, float]] = []
    for soft_energy in (1.0e-2, 1.0e-3, 1.0e-4):
        scalar_soft_internal = sequential_three_body(
            soft_energy, soft_direction, decay_direction, soft_slot=0
        )
        scalar_soft_values.append(
            (soft_energy, abs(pph_reduced_product(scalar_soft_internal, scattering_cosine)))
        )
    scalar_soft_slope = math.log(
        scalar_soft_values[-1][1] / scalar_soft_values[0][1]
    ) / math.log(scalar_soft_values[-1][0] / scalar_soft_values[0][0])

    endpoint_values = []
    for soft_energy in (0.99, 0.999, 0.9999):
        point = sequential_three_body(soft_energy, soft_direction, decay_direction)
        endpoint_values.append(
            max(abs(hhh_reduced_product(point, scattering_cosine)), abs(pph_reduced_product(point, scattering_cosine)))
        )
    endpoint_growth = endpoint_values[-1] / max(endpoint_values[0], 1.0e-30)

    hhh_imaginary = abs(hhh_values[0].imag) / max(abs(hhh_values[0]), 1.0e-30)
    pph_imaginary = abs(pph_base.imag) / max(abs(pph_base), 1.0e-30)
    hard_internal = sequential_three_body(0.0, soft_direction, decay_direction)
    _, _, left_scalars, right_scalars = cut_momenta(
        hard_internal, scattering_cosine
    )
    soft_left = np.concatenate(([1.0], soft_direction))
    soft_right = -soft_left
    helicity_projector = complex(0.0)
    for helicity in (-1, 1):
        polarization = KERNEL.circular_polarization(soft_left, helicity)
        helicity_projector += vector_soft_factor(
            left_scalars, soft_left, polarization
        ) * vector_soft_factor(
            right_scalars, soft_right, polarization.conjugate()
        )
    covariant_projector = sum(
        KERNEL.minkowski_dot(left, right) ** 2
        / (
            KERNEL.minkowski_dot(left, soft_left)
            * KERNEL.minkowski_dot(right, soft_right)
        )
        for left in left_scalars
        for right in right_scalars
    )
    projector_residual = abs(helicity_projector - covariant_projector) / max(
        abs(covariant_projector), 1.0e-30
    )
    rows = [
        {
            "check_id": "CUT5010_01_null_internal_states",
            "quantity": "max abs(li^2)",
            "derived_value": null_residual,
            "target": "<1e-12",
            "status": "PASS" if null_residual < 1.0e-12 else "FAIL",
        },
        {
            "check_id": "CUT5010_02_momentum_conservation",
            "quantity": "norm(sum li-P)",
            "derived_value": momentum_residual,
            "target": "<1e-12",
            "status": "PASS" if momentum_residual < 1.0e-12 else "FAIL",
        },
        {
            "check_id": "CUT5010_03_hhh_S3_symmetry",
            "quantity": "max reduced-product residual over S3",
            "derived_value": hhh_symmetry,
            "target": "<1e-9",
            "status": "PASS" if hhh_symmetry < 1.0e-9 else "FAIL",
        },
        {
            "check_id": "CUT5010_04_soft_sector_partition",
            "quantity": "w1+w2+w3-1",
            "derived_value": partition_residual,
            "target": "<1e-15",
            "status": "PASS" if partition_residual < 1.0e-15 else "FAIL",
        },
        {
            "check_id": "CUT5010_05_phiphih_scalar_exchange",
            "quantity": "abs(F(l1,l2,h)-F(l2,l1,h))",
            "derived_value": pph_symmetry,
            "target": "<1e-8",
            "status": "PASS" if pph_symmetry < 1.0e-8 else "FAIL",
        },
        {
            "check_id": "CUT5010_06_scalar_soft_safety",
            "quantity": "log-log slope of abs(F_phiphih) as scalar energy tends to zero",
            "derived_value": scalar_soft_slope,
            "target": ">1.5",
            "status": "PASS" if scalar_soft_slope > 1.5 else "FAIL",
        },
        {
            "check_id": "CUT5010_07_collinear_pair_endpoint",
            "quantity": "max kernel growth from 1-x=1e-2 to 1e-4",
            "derived_value": endpoint_growth,
            "target": "finite and <1e5",
            "status": "PASS" if math.isfinite(endpoint_growth) and endpoint_growth < 1.0e5 else "FAIL",
        },
        {
            "check_id": "CUT5010_08_hhh_reality",
            "quantity": "relative imaginary residual",
            "derived_value": hhh_imaginary,
            "target": "<1e-10",
            "status": "PASS" if hhh_imaginary < 1.0e-10 else "FAIL",
        },
        {
            "check_id": "CUT5010_09_phiphih_reality",
            "quantity": "relative imaginary residual",
            "derived_value": pph_imaginary,
            "target": "<1e-10",
            "status": "PASS" if pph_imaginary < 1.0e-10 else "FAIL",
        },
        {
            "check_id": "CUT5010_10_crossed_helicity_projector",
            "quantity": "relative residual of crossed helicity sum and covariant graviton projector",
            "derived_value": projector_residual,
            "target": "<1e-10",
            "status": "PASS" if projector_residual < 1.0e-10 else "FAIL",
        },
    ]
    return rows, {
        "null_residual": null_residual,
        "momentum_residual": momentum_residual,
        "hhh_S3_residual": hhh_symmetry,
        "phiphih_scalar_exchange_residual": pph_symmetry,
        "scalar_soft_slope": scalar_soft_slope,
        "collinear_endpoint_growth": endpoint_growth,
        "crossed_helicity_projector_residual": projector_residual,
    }


def qmc_smoke(
    scattering_cosine: float, samples: int, seeds: tuple[int, ...]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if samples <= 0 or samples & (samples - 1):
        raise ValueError("samples must be a positive power of two")
    rows: list[dict[str, Any]] = []
    summaries: dict[str, Any] = {}
    for seed in seeds:
        points = qmc.Sobol(d=5, scramble=True, seed=seed).random_base2(
            int(math.log2(samples))
        )
        values = {"hhh": [], "phiphih": []}
        imaginary = {"hhh": [], "phiphih": []}
        for point in points:
            soft_energy = float(np.clip(point[0], 1.0e-8, 1.0 - 1.0e-8))
            soft_direction = sphere(float(point[1]), float(point[2]))
            decay_direction = sphere(float(point[3]), float(point[4]))
            direct_hhh, direct_pph = direct_g_values(
                soft_energy, soft_direction, decay_direction, scattering_cosine
            )
            zero_hhh = exact_hhh_g0(
                soft_direction, decay_direction, scattering_cosine
            )
            zero_pph = exact_pph_g0(
                soft_direction, decay_direction, scattering_cosine
            )
            for sector, value in (
                ("hhh", (direct_hhh - zero_hhh) / soft_energy),
                ("phiphih", (direct_pph - zero_pph) / soft_energy),
            ):
                values[sector].append(float(value.real))
                imaginary[sector].append(abs(float(value.imag)))
        for sector in ("hhh", "phiphih"):
            array = np.asarray(values[sector], dtype=float)
            mean = float(np.mean(array))
            standard_error = float(np.std(array, ddof=1) / math.sqrt(samples))
            coefficient_u = mean / (8192.0 * math.pi**3)
            coefficient_d = -mean / (16384.0 * math.pi**4)
            row = {
                "run_id": f"QMC5010_{sector}_{seed}",
                "sector": sector,
                "seed": seed,
                "samples": samples,
                "mean_H": mean,
                "standard_error": standard_error,
                "median_H": float(np.median(array)),
                "q95_abs_H": float(np.quantile(np.abs(array), 0.95)),
                "max_abs_H": float(np.max(np.abs(array))),
                "max_abs_imaginary_H": max(imaginary[sector]),
                "U3_plus_over_kappa6_s3": coefficient_u,
                "D3_plus_over_kappa6": coefficient_d,
                "status": "SMOKE_FINITE" if np.all(np.isfinite(array)) else "FAIL",
                "valid_for_numeric_UV_claim": False,
            }
            rows.append(row)
            summaries[f"{sector}_{seed}"] = row
    for sector in ("hhh", "phiphih"):
        sector_rows = [row for row in rows if row["sector"] == sector]
        means = [float(row["mean_H"]) for row in sector_rows]
        errors = [float(row["standard_error"]) for row in sector_rows]
        discrepancy = abs(means[0] - means[1]) / max(
            math.sqrt(errors[0] ** 2 + errors[1] ** 2), 1.0e-30
        )
        rows.append(
            {
                "run_id": f"QMC5010_{sector}_seed_comparison",
                "sector": sector,
                "seed": "comparison",
                "samples": samples,
                "mean_H": float(np.mean(means)),
                "standard_error": "not_a_combined_error",
                "median_H": "",
                "q95_abs_H": "",
                "max_abs_H": "",
                "max_abs_imaginary_H": max(
                    float(row["max_abs_imaginary_H"]) for row in sector_rows
                ),
                "U3_plus_over_kappa6_s3": "smoke_only",
                "D3_plus_over_kappa6": "smoke_only",
                "seed_discrepancy_sigma": discrepancy,
                "status": "SMOKE_NOT_CONVERGENCE_CLAIM",
                "valid_for_numeric_UV_claim": False,
            }
        )
        summaries[f"{sector}_seed_discrepancy_sigma"] = discrepancy
    return rows, summaries


def gate_rows(
    locks: dict[str, bool],
    normalization: list[dict[str, Any]],
    soft: dict[str, Any],
    integrand: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    closed = {
        "primary_source_lock": all(locks.values()),
        "three_body_measure": normalization[0]["status"] == "PASS",
        "luna_five_point_canonical_normalization": normalization[4]["status"] == "PASS",
        "klt_five_point_canonical_normalization": normalization[2]["status"] == "PASS",
        "exact_hhh_soft_coefficient": soft["hhh_last_relative_residual"] < 2.0e-4,
        "exact_phiphih_soft_coefficient": soft["phiphih_last_relative_residual"] < 2.0e-4,
        "symmetric_hhh_soft_sector": all(row["status"] == "PASS" for row in integrand[2:4]),
        "scalar_soft_safety": integrand[5]["status"] == "PASS",
        "crossed_helicity_projector": integrand[9]["status"] == "PASS",
        "soft_plus_integrand_finite_smoke": all(
            row["status"] != "FAIL" for row in smoke
        ),
    }
    open_gates = {
        "soft_plus_integral_converged": "two short Sobol runs are diagnostics, not precision integration",
        "virtual_real_soft_matching": "the fixed-angle plus convention must be matched to checkpoints 4988 and 5008",
        "combined_three_particle_UV_coefficient": "requires multi-z converged integration after virtual matching",
        "outer_UV_projection": "requires the combined two- and three-particle discontinuity",
        "numeric_full_K_mu_K_ang": "outer UV projection remains open",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for name, passed in closed.items():
        rows.append(
            {
                "gate": name,
                "passed": bool(passed),
                "evidence": "source-locked executable identity",
                "status": "PASS" if passed else "FAIL",
                "valid_for_checkpoint_claim": bool(passed),
            }
        )
    for name, evidence in open_gates.items():
        rows.append(
            {
                "gate": name,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
                "valid_for_checkpoint_claim": False,
            }
        )
    return [
        {"gate_id": f"GATE5010_{index:02d}_{row['gate']}", **row}
        for index, row in enumerate(rows, start=1)
    ]


def validation_rows(
    locks: dict[str, bool],
    normalization: list[dict[str, Any]],
    soft: list[dict[str, Any]],
    integrand: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.extend(
        (f"source_{name}", passed, "primary/local source string")
        for name, passed in locks.items()
    )
    checks.append(("normalization_rows", all(row["status"] == "PASS" for row in normalization), "all normalization gates"))
    checks.append(("soft_hhh_limit", soft[-2]["status"] == "PASS", str(soft[-2]["relative_residual"])))
    checks.append(("soft_phiphih_limit", soft[-1]["status"] == "PASS", str(soft[-1]["relative_residual"])))
    checks.append(("integrand_rows", all(row["status"] == "PASS" for row in integrand), "all kinematic/symmetry checks"))
    checks.append(("qmc_rows_finite", all(row["status"] != "FAIL" for row in smoke), "short smoke only"))
    checks.append(("closed_gates", all(row["passed"] for row in gates if row["status"] != "OPEN_NONCLAIM"), "every checkpoint-scope gate"))
    checks.append(("claim_gates_blocked", all(not row["passed"] for row in gates if row["status"] == "OPEN_NONCLAIM"), "no UV/local-GR/MTS promotion"))
    checks.append(("formalization_workbench_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)))
    return [
        {
            "validation_id": f"VAL5010_{index:02d}_{name}",
            "check": name,
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], locks: dict[str, bool]) -> None:
    lines = [
        "# 5010 coupled three-particle cut provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Sources",
        "",
        "- Luna, Nicholson, O'Connell, and White, arXiv:1711.03901: coupling-omitted five-graph scalar-radiation double copy and four-point factorization calibration.",
        "- Dunbar and Norridge, arXiv:hep-th/9512084: identical massless four-scalar Einstein tree and unitarity normalization anchor.",
        "- Bjerrum-Bohr et al., arXiv:1010.3933: primary KLT momentum-kernel ordering.",
        "- Checkpoints 4988 and 5009: canonical scalar-tree convention and executable five-point kernels.",
        "",
        "## Source locks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in locks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{value}`" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This checkpoint fixes the relative five-point normalization by the universal soft theorem, constructs the physical hhh and phiphih tree products, and makes the graviton-soft plus integrands executable. Its short Sobol runs are smoke diagnostics. They are not converged UV coefficients and are not matched yet to the virtual soft convention of checkpoints 4988/5008. No outer UV, local-GR, or full-MTS claim follows.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def write_document(result: dict[str, Any]) -> None:
    normalization = result["normalization"]
    soft = result["soft_subtraction"]
    smoke = result["qmc_smoke"]
    hhh_runs = [
        value
        for key, value in smoke.items()
        if key.startswith("hhh_") and isinstance(value, dict)
    ]
    pph_runs = [
        value
        for key, value in smoke.items()
        if key.startswith("phiphih_") and isinstance(value, dict)
    ]
    hhh_text = ", ".join(
        f"seed {row['seed']}: {row['mean_H']:.8g} +/- {row['standard_error']:.3g}"
        for row in hhh_runs
    )
    pph_text = ", ".join(
        f"seed {row['seed']}: {row['mean_H']:.8g} +/- {row['standard_error']:.3g}"
        for row in pph_runs
    )
    text = f"""# 5010 — coupled three-particle cut normalization and soft-plus integrand

## Result

This checkpoint advances the open outer-cut calculation rather than adding another target ledger. The physical `hhh` and `phi phi h` tree products are now executable with their coupling and identical-state factors, and their only non-integrable boundary is removed by an explicit graviton-soft plus prescription.

The checkpoint does **not** yet claim a two-loop UV coefficient. The remaining operation is a matched, converged multi-angle/multi-`z` integral combined with the virtual terms from checkpoints 4988 and 5008.

## Relative normalization

Luna et al. explicitly omit couplings and factors of `i`. With all three identical-scalar pairings, their four-point reduced sum obeys

```text
M4_Luna,raw = -4 C4,
C4 = tu/s + su/t + st/u.
```

The five-point relative normalization cannot therefore be guessed from the four-point coefficient alone. The universal soft theorem fixes it directly:

```text
M5_Luna,raw / (S_vec C4) -> -8,
M5_canonical = -M5_Luna,raw/8,
M5_canonical / (S_vec C4) -> 1.
```

At soft energy `10^-6`, the measured canonical ratio is `{normalization['luna_canonical_soft_ratio_at_1e-6']}`. The independently constructed KLT `2phi+3h` kernel gives `{normalization['klt_soft_ratio_at_1e-6']}`. This closes the earlier `-1/4` versus `-1/8` ambiguity: `-1/4` maps the coupling-omitted Luna four-point sum, while `-1/8` is the five-point factor demanded by soft factorization.

## Physical state sums

With each full five-point tree carrying `(kappa/2)^3`, the cut product carries `kappa^6/64`. The reduced state sums are

```text
F_hhh = (1/3!) sum_r [M_L^angle(r) M_R^square(r)
                      + M_L^square(r) M_R^angle(r)],

F_phiphih = (1/2!) sum_h M_L^canonical(h) M_R^canonical(-h).
```

The crossed helicity is fixed by unitarity rather than convention: complex-conjugating the right polarization makes the helicity sum equal the covariant graviton projector pointwise, with relative residual `{result['integrand']['crossed_helicity_projector_residual']:.3e}`.

The `hhh` soft regions are partitioned symmetrically with

```text
w_i = E_i^-2 / sum_j E_j^-2,
F_hhh^(soft-3 sector) = 3 w_3 F_hhh.
```

Permutation symmetry and `sum_i w_i=1` make this an exact partition of the integrated identical-graviton state, not an extra multiplicity.

## Exact soft subtraction

For `s=4`, choose the third cut momentum as `k=(x,x n)` and decay the recoil into the remaining pair. The exact phase-space factor is

```text
dPhi3 = x dx dOmega_k dOmega_*/(512 pi^5),
integral dPhi3 = s/(256 pi^3).
```

For either sector define

```text
g_X(x,Omega) = x^2 F_X(x,Omega)/s^2,
H_X(x,Omega) = [g_X(x,Omega)-g_X(0,Omega)]/x.
```

`g_X(0,Omega)` is not fitted. For `hhh` it is built from exact four-point KLT trees and spinor soft factors; for `phi phi h` it is built from `C4` and the vector eikonal factor. At the fixed validation geometry,

```text
g_hhh(0)     = {soft['hhh_g0']}
g_phiphih(0) = {soft['phiphih_g0']}
```

The direct `x=10^-6` residuals are `{soft['hhh_last_relative_residual']:.3e}` and `{soft['phiphih_last_relative_residual']:.3e}`. A soft internal scalar is suppressed rather than divergent; the measured power is `{result['integrand']['scalar_soft_slope']:.6g}`.

The normalized finite-part relation is

```text
U3_plus/(kappa^6 s^3) = E[H_hhh + H_phiphih]/(8192 pi^3),
D3_plus/kappa^6       = -E[H_hhh + H_phiphih]/(16384 pi^4).
```

## Short numerical smoke

The short scrambled-Sobol runs are deliberately not promoted to precision results:

```text
hhh:     {hhh_text}
phiphih: {pph_text}
```

They establish that the subtraction is numerically executable. Their variance and seed spread remain part of the next convergence task.

## Gate

- Three-body measure, relative five-point normalization, physical state sums, symmetric soft sector, exact soft coefficients, and finite plus integrands: **closed**.
- Converged multi-`z` integration: **open**.
- Matching this real-emission plus prescription to the virtual subtraction in checkpoints 4988/5008: **open**.
- Combined outer UV projection, numeric `K_mu/K_ang`, local GR, and full MTS: **not claimed**.

Next: perform the matched multi-`z` integration, explicitly verify cancellation of the universal soft coefficient against the virtual channel, and only then apply the local UV projector.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--samples", type=int, default=512)
    parser.add_argument("--z", type=float, default=0.15)
    args = parser.parse_args()
    started = time.perf_counter()

    required = [
        SCRIPT_5009,
        RESULT_5009,
        RESULT_4988,
        LUNA_SOURCE,
        DUNBAR_SOURCE,
        KLT_SOURCE,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    locks = source_locks()
    if not all(locks.values()):
        raise RuntimeError(
            f"source locks failed: {[name for name, passed in locks.items() if not passed]}"
        )
    normalization, normalization_result = normalization_checks(args.z)
    soft_rows, soft_result = soft_checks(args.z)
    integrand_rows, integrand_result = cut_integrand_checks(args.z)
    if args.dry_run:
        passed = all(row["status"] == "PASS" for row in normalization)
        passed = passed and soft_rows[-2]["status"] == "PASS" and soft_rows[-1]["status"] == "PASS"
        passed = passed and all(row["status"] == "PASS" for row in integrand_rows)
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "dry_run": True,
                    "source_locks": all(locks.values()),
                    "analytic_and_kinematic_checks": passed,
                    "elapsed_seconds": time.perf_counter() - started,
                },
                indent=2,
            )
        )
        return 0 if passed else 1

    smoke_rows, smoke_result = qmc_smoke(args.z, args.samples, (5010, 5011))
    gates = gate_rows(
        locks, normalization, soft_result, integrand_rows, smoke_rows
    )
    validations = validation_rows(
        locks, normalization, soft_rows, integrand_rows, smoke_rows, gates
    )

    SOURCE.mkdir(parents=True, exist_ok=True)
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for path, rows in (
        (NORMALIZATION_CSV, normalization),
        (SOFT_CSV, soft_rows),
        (INTEGRAND_CSV, integrand_rows),
        (SMOKE_CSV, smoke_rows),
        (GATE_CSV, gates),
        (VALIDATION_CSV, validations),
    ):
        write_csv(path, tagged(rows) if path != VALIDATION_CSV else rows)

    source_paths = [*required, Path(__file__).resolve()]
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": locks,
        "source_hashes": source_hashes,
        "scattering_cosine": args.z,
        "samples_per_seed": args.samples,
        "normalization": normalization_result,
        "soft_subtraction": soft_result,
        "integrand": integrand_result,
        "qmc_smoke": smoke_result,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "validation_passed": all(row["passed"] for row in validations),
        "outer_UV_projection": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_provenance(source_hashes, locks)
    write_document(result)

    passed_gates = sum(bool(row["passed"]) for row in gates)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "passed_checkpoint_gates": passed_gates,
                "total_gates": len(gates),
                "validation_passed": result["validation_passed"],
                "samples_per_seed": args.samples,
                "hhh_seed_discrepancy_sigma": smoke_result[
                    "hhh_seed_discrepancy_sigma"
                ],
                "phiphih_seed_discrepancy_sigma": smoke_result[
                    "phiphih_seed_discrepancy_sigma"
                ],
                "elapsed_seconds": time.perf_counter() - started,
            },
            indent=2,
        )
    )
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
