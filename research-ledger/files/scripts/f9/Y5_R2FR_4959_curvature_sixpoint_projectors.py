from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import qmc


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4959"

RESULT_JSON = SOURCE / "curvature_sixpoint_projector_results.json"
IDENTITY_CSV = SOURCE / "sixpoint_projector_identity_checks.csv"
REPLICATE_CSV = SOURCE / "sixpoint_projector_QMC_replicates.csv"
GRAM_CSV = SOURCE / "sixpoint_projector_gram_matrix.csv"
TRAJECTORY_CSV = SOURCE / "trajectory_full_amplitude_bounds.csv"
SCALING_CSV = SOURCE / "sixpoint_IR_power_counting.csv"
DECISION_CSV = SOURCE / "sixpoint_projector_decision.csv"

CHECKPOINT_4958 = POST / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
SCRIPT_4958 = POST / "scripts" / "Y5_R2FR_4958_essential_PX_sixpoint_trajectory.py"
RESULT_4958 = POST / "source-intake" / "functional_rg" / "4958" / "essential_PX_sixpoint_trajectory_results.json"
FLOW_4958 = POST / "source-intake" / "functional_rg" / "4958" / "essential_functional_GR_trajectory.csv"
RATE_4954 = POST / "source-intake" / "functional_rg" / "4954" / "offshell_X2_X3_number_change_results.json"
BASIS_SOURCE = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"

EXPECTED_HASHES = {
    CHECKPOINT_4958: "d08b8a0ab6a5317c77a23accd34dc46c5ad6a0bc5aa73e0767c8e0aa0edd5f1c",
    SCRIPT_4958: "521ffed6f208cf4c0db3fd596643fc0970f34e1050de71ab65e37c44906ff77f",
    RESULT_4958: "383e13cd13c3e90be22dbf8ad589c756a26cad002f01da4ce151ad262e48ae67",
    FLOW_4958: "b4317dcc01084a61a6b282bd331d2ce111b835e499c86e65077d0fb98a549081",
    RATE_4954: "523339dd40a835f84c2bbd24a20b7977710f5a71b826dbb3d830089b7445ab45",
    BASIS_SOURCE: "e234ab07031885f79030529bb3dcabc7e928cc4283774f26ebc5dac6b8a226dc",
}

MARKER = "MTS_4959_CURVATURE_SIXPOINT_PROJECTORS"
CHECKED_DATE = "2026-07-13"
PHASE_SEEDS = (495901, 495902, 495903, 495904)
PROJECTOR_NAMES = ("X2_exchange", "X3_contact", "O2_covariant", "O3_C3", "O4_C2X")
ETA = np.diag(np.array([1.0, -1.0, -1.0, -1.0]))
ETA_DIAGONAL = np.diag(ETA)
BIVECTOR_PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
BIVECTOR_SIGNATURE = np.array([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0])
PERMUTATIONS_4 = tuple(itertools.permutations(range(4)))
PAIR_CHOICES_6 = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIR_CHOICES_6)}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
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


def minkowski_dot(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.einsum("...i,i,...i->...", left, ETA_DIAGONAL, right)


def lower(vector: np.ndarray) -> np.ndarray:
    return vector * ETA_DIAGONAL


def h_contract(left: np.ndarray, metric_mode: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.einsum("...i,...ij,...j->...", left, metric_mode, right)


def trace_h(metric_mode: np.ndarray) -> np.ndarray:
    return np.einsum("i,...ii->...", ETA_DIAGONAL, metric_mode)


def perfect_matchings(items: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not items:
        return [tuple()]
    first = items[0]
    rows: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(items)):
        second = items[index]
        remainder = items[1:index] + items[index + 1 :]
        for matching in perfect_matchings(remainder):
            rows.append(((first, second),) + matching)
    return rows


MATCHINGS_6 = tuple(perfect_matchings(tuple(range(6))))
PARTITIONS_3_3 = tuple(
    ((0,) + pair, tuple(index for index in range(6) if index not in ((0,) + pair)))
    for pair in itertools.combinations(range(1, 6), 2)
)


def four_vertex(first: np.ndarray, second: np.ndarray, third: np.ndarray, fourth: np.ndarray) -> np.ndarray:
    return 2.0 * (
        minkowski_dot(first, second) * minkowski_dot(third, fourth)
        + minkowski_dot(first, third) * minkowski_dot(second, fourth)
        + minkowski_dot(first, fourth) * minkowski_dot(second, third)
    )


def o2_flat_vertex(momenta: np.ndarray) -> np.ndarray:
    value = np.zeros(momenta.shape[0])
    for permutation in PERMUTATIONS_4:
        first, second, third, fourth = (momenta[:, index] for index in permutation)
        value -= minkowski_dot(first, second) * minkowski_dot(third, fourth) ** 2
    return value


def canonical_h2_vertex(first: np.ndarray, second: np.ndarray, metric_mode: np.ndarray) -> np.ndarray:
    return h_contract(first, metric_mode, second) - 0.5 * trace_h(metric_mode) * minkowski_dot(first, second)


def o2_contact_4scalar_h(graviton: np.ndarray, metric_mode: np.ndarray, momenta: np.ndarray) -> np.ndarray:
    value = np.zeros(momenta.shape[0])
    metric_trace = trace_h(metric_mode)
    for permutation in PERMUTATIONS_4:
        first, second, third, fourth = (momenta[:, index] for index in permutation)
        x_zero = -minkowski_dot(first, second)
        third_fourth = minkowski_dot(third, fourth)
        y_zero = third_fourth**2
        delta_x = h_contract(first, metric_mode, second)
        third_h_fourth = h_contract(third, metric_mode, fourth)
        delta_y_metric = -2.0 * third_fourth * third_h_fourth
        delta_y_connection = -(
            minkowski_dot(graviton, fourth) + minkowski_dot(graviton, third)
        ) * third_h_fourth + 0.5 * (
            minkowski_dot(graviton, third) * h_contract(fourth, metric_mode, fourth)
            + minkowski_dot(graviton, fourth) * h_contract(third, metric_mode, third)
        )
        value += (
            0.5 * metric_trace * x_zero * y_zero
            + delta_x * y_zero
            + x_zero * (delta_y_metric + delta_y_connection)
        )
    return value


def o2_gauge_complete_4scalar_h(graviton: np.ndarray, metric_mode: np.ndarray, momenta: np.ndarray) -> np.ndarray:
    value = o2_contact_4scalar_h(graviton, metric_mode, momenta)
    for external_index in range(4):
        external = momenta[:, external_index]
        internal = graviton + external
        remainder = [index for index in range(4) if index != external_index]
        o2_arguments = np.stack(
            (internal, momenta[:, remainder[0]], momenta[:, remainder[1]], momenta[:, remainder[2]]),
            axis=1,
        )
        value -= (
            canonical_h2_vertex(external, -internal, metric_mode)
            * o2_flat_vertex(o2_arguments)
            / minkowski_dot(internal, internal)
        )
    return value


def pair_metric_response(first: np.ndarray, second: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    momentum = first + second
    denominator = minkowski_dot(momentum, momentum)
    first_lower = lower(first)
    second_lower = lower(second)
    response = (
        np.einsum("...i,...j->...ij", first_lower, second_lower)
        + np.einsum("...i,...j->...ij", second_lower, first_lower)
    ) / denominator[..., None, None]
    return momentum, response


def linear_weyl_bivector(momentum: np.ndarray, metric_mode: np.ndarray) -> tuple[np.ndarray, dict[str, float]]:
    momentum_lower = lower(momentum)
    event_count = momentum.shape[0]
    riemann = np.empty((event_count, 4, 4, 4, 4))
    for first in range(4):
        for second in range(4):
            for third in range(4):
                for fourth in range(4):
                    riemann[:, first, second, third, fourth] = 0.5 * (
                        momentum_lower[:, third] * momentum_lower[:, second] * metric_mode[:, first, fourth]
                        + momentum_lower[:, fourth] * momentum_lower[:, first] * metric_mode[:, second, third]
                        - momentum_lower[:, fourth] * momentum_lower[:, second] * metric_mode[:, first, third]
                        - momentum_lower[:, third] * momentum_lower[:, first] * metric_mode[:, second, fourth]
                    )
    ricci = np.zeros((event_count, 4, 4))
    for second in range(4):
        for fourth in range(4):
            for first in range(4):
                ricci[:, second, fourth] += ETA_DIAGONAL[first] * riemann[:, first, second, first, fourth]
    scalar = np.einsum("i,...ii->...", ETA_DIAGONAL, ricci)
    weyl = np.empty_like(riemann)
    for first in range(4):
        for second in range(4):
            for third in range(4):
                for fourth in range(4):
                    trace_piece = (
                        ETA[first, third] * ricci[:, fourth, second]
                        - ETA[first, fourth] * ricci[:, third, second]
                        - ETA[second, third] * ricci[:, fourth, first]
                        + ETA[second, fourth] * ricci[:, third, first]
                    )
                    scalar_piece = (
                        ETA[first, third] * ETA[fourth, second]
                        - ETA[first, fourth] * ETA[third, second]
                    )
                    weyl[:, first, second, third, fourth] = (
                        riemann[:, first, second, third, fourth]
                        - 0.5 * trace_piece
                        + scalar * scalar_piece / 6.0
                    )
    bivector = np.empty((event_count, 6, 6))
    for left_index, (first, second) in enumerate(BIVECTOR_PAIRS):
        for right_index, (third, fourth) in enumerate(BIVECTOR_PAIRS):
            bivector[:, left_index, right_index] = weyl[:, first, second, third, fourth]
    mixed = bivector * BIVECTOR_SIGNATURE[None, None, :]
    ricci_trace = np.zeros((event_count, 4, 4))
    for second in range(4):
        for fourth in range(4):
            for first in range(4):
                ricci_trace[:, second, fourth] += ETA_DIAGONAL[first] * weyl[:, first, second, first, fourth]
    diagnostics = {
        "weyl_trace_max": float(np.max(np.abs(ricci_trace))),
        "weyl_pair_exchange_max": float(np.max(np.abs(weyl - np.transpose(weyl, (0, 3, 4, 1, 2))))),
        "weyl_first_pair_antisymmetry_max": float(np.max(np.abs(weyl + np.swapaxes(weyl, 1, 2)))),
    }
    return mixed, diagnostics


def all_projectors(external: np.ndarray) -> tuple[np.ndarray, dict[str, float]]:
    event_count = external.shape[0]
    exchange = np.zeros(event_count)
    for first_set, second_set in PARTITIONS_3_3:
        first = external[:, first_set, :]
        second = external[:, second_set, :]
        internal = np.sum(first, axis=1)
        exchange += (
            four_vertex(first[:, 0], first[:, 1], first[:, 2], -internal)
            * four_vertex(second[:, 0], second[:, 1], second[:, 2], internal)
            / minkowski_dot(internal, internal)
        )

    contact = np.zeros(event_count)
    for matching in MATCHINGS_6:
        product = np.ones(event_count)
        for left, right in matching:
            product *= minkowski_dot(external[:, left], external[:, right])
        contact += product
    contact *= 6.0

    o2_projector = np.zeros(event_count)
    pair_mixed_weyl: list[np.ndarray] = []
    weyl_trace_max = 0.0
    weyl_symmetry_max = 0.0
    for first, second in PAIR_CHOICES_6:
        graviton, response = pair_metric_response(external[:, first], external[:, second])
        remainder = [index for index in range(6) if index not in (first, second)]
        o2_projector += o2_gauge_complete_4scalar_h(graviton, response, external[:, remainder, :])
        mixed_weyl, diagnostics = linear_weyl_bivector(graviton, response)
        pair_mixed_weyl.append(mixed_weyl)
        weyl_trace_max = max(weyl_trace_max, diagnostics["weyl_trace_max"])
        weyl_symmetry_max = max(
            weyl_symmetry_max,
            diagnostics["weyl_pair_exchange_max"],
            diagnostics["weyl_first_pair_antisymmetry_max"],
        )

    o3_projector = np.zeros(event_count)
    o4_projector = np.zeros(event_count)
    for matching in MATCHINGS_6:
        matrices = [pair_mixed_weyl[PAIR_INDEX[tuple(sorted(pair))]] for pair in matching]
        first, second, third = matrices
        o3_projector += 24.0 * (
            np.einsum("...ij,...jk,...ki->...", first, second, third)
            + np.einsum("...ij,...jk,...ki->...", first, third, second)
        )
        for explicit_index in range(3):
            scalar_pair = matching[explicit_index]
            curvature_indices = [index for index in range(3) if index != explicit_index]
            curvature_first = matrices[curvature_indices[0]]
            curvature_second = matrices[curvature_indices[1]]
            contraction = 4.0 * np.einsum("...ij,...ji->...", curvature_first, curvature_second)
            o4_projector += 4.0 * minkowski_dot(
                external[:, scalar_pair[0]], external[:, scalar_pair[1]]
            ) * contraction

    values = np.column_stack((exchange, contact, o2_projector, o3_projector, o4_projector))
    diagnostics = {
        "weyl_trace_max": weyl_trace_max,
        "weyl_symmetry_max": weyl_symmetry_max,
        "all_finite": bool(np.all(np.isfinite(values))),
    }
    return values, diagnostics


def rambo_massless(random_values: np.ndarray) -> tuple[np.ndarray, float, float]:
    event_count = random_values.shape[0]
    values = random_values.reshape(event_count, 4, 4)
    energy = -np.log(np.maximum(values[:, :, 0] * values[:, :, 1], 1.0e-300))
    cosine = 2.0 * values[:, :, 2] - 1.0
    azimuth = 2.0 * np.pi * values[:, :, 3]
    sine = np.sqrt(np.maximum(0.0, 1.0 - cosine**2))
    trial = np.stack(
        (energy, energy * sine * np.cos(azimuth), energy * sine * np.sin(azimuth), energy * cosine),
        axis=2,
    )
    total = np.sum(trial, axis=1)
    beta = total[:, 1:] / total[:, 0, None]
    beta_squared = np.sum(beta**2, axis=1)
    gamma = 1.0 / np.sqrt(1.0 - beta_squared)
    beta_dot = np.sum(trial[:, :, 1:] * beta[:, None, :], axis=2)
    boosted = np.empty_like(trial)
    boosted[:, :, 0] = gamma[:, None] * (trial[:, :, 0] - beta_dot)
    coefficient = (gamma - 1.0) / beta_squared
    boosted[:, :, 1:] = trial[:, :, 1:] + (
        coefficient[:, None, None] * beta_dot[:, :, None]
        - gamma[:, None, None] * trial[:, :, 0, None]
    ) * beta[:, None, :]
    invariant_mass = np.sqrt(total[:, 0] ** 2 - np.sum(total[:, 1:] ** 2, axis=1))
    momenta = boosted / invariant_mass[:, None, None]
    sum_error = max(
        float(np.max(np.abs(np.sum(momenta, axis=1)[:, 0] - 1.0))),
        float(np.max(np.abs(np.sum(momenta, axis=1)[:, 1:]))),
    )
    mass_error = float(np.max(np.abs(momenta[:, :, 0] ** 2 - np.sum(momenta[:, :, 1:] ** 2, axis=2))))
    return momenta, sum_error, mass_error


def external_from_outgoing(outgoing: np.ndarray) -> np.ndarray:
    external = np.empty((outgoing.shape[0], 6, 4))
    external[:, 0, :] = (0.5, 0.0, 0.0, 0.5)
    external[:, 1, :] = (0.5, 0.0, 0.0, -0.5)
    external[:, 2:, :] = -outgoing
    return external


def symmetric_event() -> np.ndarray:
    directions = np.array(
        ((1.0, 1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, 1.0, -1.0), (-1.0, -1.0, 1.0))
    ) / math.sqrt(3.0)
    outgoing = np.column_stack((np.full(4, 0.25), 0.25 * directions))[None, :, :]
    return external_from_outgoing(outgoing)


def planar_event(energy_x: float) -> np.ndarray:
    energy_y = 0.5 - energy_x
    outgoing = np.array(
        [[
            [energy_x, energy_x, 0.0, 0.0],
            [energy_x, -energy_x, 0.0, 0.0],
            [energy_y, 0.0, energy_y, 0.0],
            [energy_y, 0.0, -energy_y, 0.0],
        ]]
    )
    return external_from_outgoing(outgoing)


def identity_checks() -> list[dict[str, Any]]:
    event = symmetric_event()
    values, diagnostics = all_projectors(event)
    rows: list[dict[str, Any]] = []

    momenta_22 = np.array(
        [[[0.5, 0.0, 0.0, 0.5], [0.5, 0.0, 0.0, -0.5], [-0.5, -0.3, 0.0, -0.4], [-0.5, 0.3, 0.0, 0.4]]]
    )
    s_value = minkowski_dot(momenta_22[:, 0] + momenta_22[:, 1], momenta_22[:, 0] + momenta_22[:, 1])[0]
    t_value = minkowski_dot(momenta_22[:, 0] + momenta_22[:, 2], momenta_22[:, 0] + momenta_22[:, 2])[0]
    u_value = minkowski_dot(momenta_22[:, 0] + momenta_22[:, 3], momenta_22[:, 0] + momenta_22[:, 3])[0]
    o2_value = o2_flat_vertex(momenta_22)[0]
    o2_expected = -3.0 * s_value * t_value * u_value
    rows.append({
        "check": "O2_flat_2to2_equals_minus_3stu",
        "value": o2_value,
        "reference": o2_expected,
        "residual": abs(o2_value - o2_expected),
        "passed": abs(o2_value - o2_expected) < 1.0e-13,
    })

    source_pair = (0, 1)
    graviton = event[:, source_pair[0]] + event[:, source_pair[1]]
    random_vector = np.array([[0.37, -0.23, 0.41, 0.19]])
    graviton_lower = lower(graviton)
    random_lower = lower(random_vector)
    pure_gauge = (
        np.einsum("...i,...j->...ij", graviton_lower, random_lower)
        + np.einsum("...i,...j->...ij", random_lower, graviton_lower)
    )
    remainder = [index for index in range(6) if index not in source_pair]
    ward_value = o2_gauge_complete_4scalar_h(graviton, pure_gauge, event[:, remainder, :])[0]
    rows.append({
        "check": "O2_contact_plus_legs_Ward_identity",
        "value": ward_value,
        "reference": 0.0,
        "residual": abs(ward_value),
        "passed": abs(ward_value) < 1.0e-13,
    })

    mixed_original, _ = linear_weyl_bivector(graviton, np.zeros_like(pure_gauge))
    mixed_gauge, _ = linear_weyl_bivector(graviton, pure_gauge)
    gauge_weyl_residual = float(np.max(np.abs(mixed_original - mixed_gauge)))
    rows.append({
        "check": "linear_Weyl_pure_gauge_zero",
        "value": gauge_weyl_residual,
        "reference": 0.0,
        "residual": gauge_weyl_residual,
        "passed": gauge_weyl_residual < 1.0e-13,
    })

    maximum_permutation_residual = 0.0
    for permutation in ((1, 0, 2, 3, 4, 5), (2, 4, 1, 5, 0, 3), (5, 4, 3, 2, 1, 0)):
        permuted, _ = all_projectors(event[:, permutation, :])
        maximum_permutation_residual = max(
            maximum_permutation_residual, float(np.max(np.abs(permuted - values)))
        )
    rows.append({
        "check": "all_projectors_permutation_symmetric",
        "value": maximum_permutation_residual,
        "reference": 0.0,
        "residual": maximum_permutation_residual,
        "passed": maximum_permutation_residual < 1.0e-12,
    })

    scaled, _ = all_projectors(1.7 * event)
    homogeneity_residual = float(np.max(np.abs(scaled / (1.7**6) - values)))
    rows.append({
        "check": "all_projectors_degree_six",
        "value": homogeneity_residual,
        "reference": 0.0,
        "residual": homogeneity_residual,
        "passed": homogeneity_residual < 1.0e-11,
    })
    rows.append({
        "check": "Weyl_trace_and_index_symmetries",
        "value": max(diagnostics["weyl_trace_max"], diagnostics["weyl_symmetry_max"]),
        "reference": 0.0,
        "residual": max(diagnostics["weyl_trace_max"], diagnostics["weyl_symmetry_max"]),
        "passed": max(diagnostics["weyl_trace_max"], diagnostics["weyl_symmetry_max"]) < 1.0e-12,
    })

    planar_equal, _ = all_projectors(planar_event(0.25))
    planar_unequal, _ = all_projectors(planar_event(1.0 / 6.0))
    planar_equal_reference = np.array((-39.0 / 128.0, 21.0 / 128.0, 21.0 / 1024.0, 7.0 / 96.0, -1.0 / 32.0))
    planar_unequal_reference = np.array((-13.0 / 54.0, 7.0 / 54.0, 163.0 / 3888.0, 14.0 / 243.0, -2.0 / 81.0))
    planar_reference_residual = float(
        max(
            np.max(np.abs(planar_equal[0] - planar_equal_reference)),
            np.max(np.abs(planar_unequal[0] - planar_unequal_reference)),
        )
    )
    rows.append({
        "check": "two_rational_planar_projector_vectors",
        "value": planar_reference_residual,
        "reference": "(-39/128,21/128,21/1024,7/96,-1/32);(-13/54,7/54,163/3888,14/243,-2/81)",
        "residual": planar_reference_residual,
        "passed": planar_reference_residual < 1.0e-13,
    })
    two_event_determinant = (
        planar_equal[0, 1] * planar_unequal[0, 2]
        - planar_equal[0, 2] * planar_unequal[0, 1]
    )
    determinant_reference = 175.0 / 41472.0
    rows.append({
        "check": "X3_O2_exact_nonproportionality_witness",
        "value": float(two_event_determinant),
        "reference": "175/41472",
        "residual": abs(float(two_event_determinant) - determinant_reference),
        "passed": abs(float(two_event_determinant) - determinant_reference) < 1.0e-13,
    })
    for index, name in enumerate(PROJECTOR_NAMES):
        rows.append({
            "check": f"symmetric_event_{name}_finite_nonzero",
            "value": float(values[0, index]),
            "reference": "finite_nonzero",
            "residual": "",
            "passed": bool(np.isfinite(values[0, index]) and abs(values[0, index]) > 1.0e-16),
        })
    return rows


def estimate_replica(seed: int, phase_power: int) -> tuple[dict[str, Any], np.ndarray]:
    random_values = qmc.Sobol(16, scramble=True, seed=seed).random_base2(phase_power)
    outgoing, sum_error, mass_error = rambo_massless(random_values)
    projectors, diagnostics = all_projectors(external_from_outgoing(outgoing))
    gram = projectors.T @ projectors / projectors.shape[0]
    x3_o2_schur = gram[1, 1] - gram[1, 2] ** 2 / gram[2, 2]
    row = {
        "seed": seed,
        "sobol_power": phase_power,
        "event_count": projectors.shape[0],
        "RAMBO_sum_error_max": sum_error,
        "RAMBO_mass_shell_error_max": mass_error,
        "weyl_trace_max": diagnostics["weyl_trace_max"],
        "weyl_symmetry_max": diagnostics["weyl_symmetry_max"],
        "all_finite": diagnostics["all_finite"],
        "gram_minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(gram))),
        "projector_absolute_maximum": float(np.max(np.abs(projectors))),
        "X3_O2_gram_determinant": float(np.linalg.det(gram[np.ix_((1, 2), (1, 2))])),
        "X3_O2_schur_complement": float(x3_o2_schur),
        "X3_O2_residual_fraction": float(x3_o2_schur / gram[1, 1]),
        "best_kappa_w_over_v_X3": float(-gram[1, 2] / gram[2, 2]),
    }
    for left, left_name in enumerate(PROJECTOR_NAMES):
        for right, right_name in enumerate(PROJECTOR_NAMES[left:], start=left):
            row[f"G_{left_name}__{right_name}"] = float(gram[left, right])
    return row, gram


def trajectory_endpoints() -> list[dict[str, str]]:
    rows = read_csv(FLOW_4958)
    grouped: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row["scheme"], row["polynomial_order"])
        if key not in grouped or int(row["sample_index"]) > int(grouped[key]["sample_index"]):
            grouped[key] = row
    return [grouped[key] for key in sorted(grouped)]


def trajectory_bounds(gram: np.ndarray, head_on_factor: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    x3_o2_schur = gram[1, 1] - gram[1, 2] ** 2 / gram[2, 2]
    cancellation_ratio = -gram[1, 2] / gram[2, 2]
    for endpoint in trajectory_endpoints():
        gravity = float(endpoint["g"])
        a2 = float(endpoint["a2"])
        a3 = float(endpoint["a3"])
        h_c3 = float(endpoint["h_C3"])
        u_o4 = float(endpoint["u_O4"])
        kappa = 16.0 * math.pi * gravity
        u_x2 = 4.0 * a2
        v_x3 = 8.0 * a3
        coefficients = np.array((u_x2**2, v_x3, 0.0, kappa**3 * h_c3, kappa**2 * u_o4))
        projection_on_o2 = float(coefficients @ gram[:, 2])
        kappa_w_optimum = -projection_on_o2 / gram[2, 2]
        optimized = coefficients.copy()
        optimized[2] = kappa_w_optimum
        known_without_o2 = head_on_factor * float(coefficients @ gram @ coefficients)
        optimized_kernel = head_on_factor * float(optimized @ gram @ optimized)
        leading_lower_bound = head_on_factor * v_x3**2 * x3_o2_schur
        old_scalar_kernel = float(endpoint["dimensionless_sigma24_essential_scalar_kernel"])
        corrected_scalar_kernel = 256.0 * old_scalar_kernel
        rows.append({
            "scheme": endpoint["scheme"],
            "polynomial_order": endpoint["polynomial_order"],
            "g_endpoint": gravity,
            "u_X2_recent": u_x2,
            "v_X3_recent": v_x3,
            "kappa_16pi_g": kappa,
            "h_C3": h_c3,
            "u_O4": u_o4,
            "r_X3": v_x3 / u_x2**2,
            "r_O3": kappa**3 * h_c3 / u_x2**2,
            "r_O4": kappa**2 * u_o4 / u_x2**2,
            "O2_to_X3_cancellation_ratio_kappa_w_over_v": cancellation_ratio,
            "w_O2_optimum": kappa_w_optimum / kappa,
            "W_O2_optimum_over_g2": (kappa_w_optimum / kappa) / gravity**2,
            "beta_w_g2_source_optimum_if_beta_w_eq_6w_plus_Sg2": -2.0
            * (kappa_w_optimum / kappa)
            / gravity**2,
            "old_4958_scalar_kernel": old_scalar_kernel,
            "corrected_scalar_kernel_factor_256": corrected_scalar_kernel,
            "known_X2_X3_O3_O4_kernel_without_O2": known_without_o2,
            "full_basis_kernel_minimized_over_O2": optimized_kernel,
            "asymptotic_X3_O2_lower_bound": leading_lower_bound,
            "optimized_fraction_of_known_without_O2": optimized_kernel / known_without_o2,
            "curvature_fraction_relative_to_corrected_scalar": known_without_o2 / corrected_scalar_kernel - 1.0,
            "coefficient_ratio_X2_exchange_to_X3": u_x2**2 / v_x3,
            "coefficient_ratio_O3_to_X3": kappa**3 * h_c3 / v_x3,
            "coefficient_ratio_O4_to_X3": kappa**2 * u_o4 / v_x3,
            "minimum_positive": bool(optimized_kernel > 0.0 and leading_lower_bound > 0.0),
            "status": "FULL_P6_RATE_BOUNDED_FOR_ARBITRARY_O2_COEFFICIENT",
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-power", type=int, default=15)
    parser.add_argument("--checks-only", action="store_true")
    arguments = parser.parse_args()

    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(source_hashes[str(path)] == expected for path, expected in EXPECTED_HASHES.items())
    identity_rows = identity_checks()
    identity_pass = all(bool(row["passed"]) for row in identity_rows)
    print(f"{MARKER}_IDENTITIES pass={identity_pass}", flush=True)
    if arguments.checks_only:
        for row in identity_rows:
            print(row, flush=True)
        return 0 if identity_pass and source_hashes_match else 1

    SOURCE.mkdir(parents=True, exist_ok=True)
    replicas: list[dict[str, Any]] = []
    grams: list[np.ndarray] = []
    for seed in PHASE_SEEDS:
        row, gram = estimate_replica(seed, arguments.phase_power)
        replicas.append(row)
        grams.append(gram)
        print(
            f"{MARKER}_QMC seed={seed} events={row['event_count']} min_eig={row['gram_minimum_eigenvalue']:.6e}",
            flush=True,
        )
    gram = np.mean(np.stack(grams), axis=0)
    gram_standard_error = np.std(np.stack(grams), axis=0, ddof=1) / math.sqrt(len(grams))
    gram_eigenvalues = np.linalg.eigvalsh(gram)
    phase_volume_s1 = 1.0 / (24_576.0 * math.pi**5)
    head_on_factor = phase_volume_s1 * 4.0**7 / (2.0 * math.factorial(4))

    gram_rows: list[dict[str, Any]] = []
    for left, left_name in enumerate(PROJECTOR_NAMES):
        for right, right_name in enumerate(PROJECTOR_NAMES):
            gram_rows.append({
                "row_projector": left_name,
                "column_projector": right_name,
                "mean_product": float(gram[left, right]),
                "standard_error": float(gram_standard_error[left, right]),
                "cross_section_weight": float(head_on_factor * gram[left, right]),
                "correlation": float(gram[left, right] / math.sqrt(gram[left, left] * gram[right, right])),
            })

    x3_o2_determinant = float(np.linalg.det(gram[np.ix_((1, 2), (1, 2))]))
    x3_o2_schur = float(gram[1, 1] - gram[1, 2] ** 2 / gram[2, 2])
    x3_o2_residual_fraction = x3_o2_schur / gram[1, 1]
    trajectory_rows = trajectory_bounds(gram, head_on_factor)
    replica_schur = [float(row["X3_O2_schur_complement"]) for row in replicas]
    replica_residual_fraction = [float(row["X3_O2_residual_fraction"]) for row in replicas]
    replica_best_ratio = [float(row["best_kappa_w_over_v_X3"]) for row in replicas]
    rate_4954 = json.loads(RATE_4954.read_text(encoding="utf-8"))["on_shell_24"]
    scalar_calibration = {
        "C0_recomputed": float(head_on_factor * gram[0, 0]),
        "C1_recomputed": float(2.0 * head_on_factor * gram[0, 1]),
        "C2_recomputed": float(head_on_factor * gram[1, 1]),
        "C0_4954": float(rate_4954["C0"]),
        "C1_4954": float(rate_4954["C1"]),
        "C2_4954": float(rate_4954["C2"]),
    }
    scalar_calibration["maximum_relative_difference"] = max(
        abs(scalar_calibration[f"C{index}_recomputed"] - scalar_calibration[f"C{index}_4954"])
        / abs(scalar_calibration[f"C{index}_4954"])
        for index in range(3)
    )

    scaling_rows = [
        {
            "operator": "O1=X_source^3",
            "six_scalar_coefficient": "v_X3=8e",
            "IR_scaling": "g^3",
            "derivation": "4958 trajectory has finite e/g^3 and nonzero gravity-forced beta_e at the matter origin",
            "role": "LEADING_FORCED_SIX_SCALAR_CONTACT",
        },
        {
            "operator": "O2=X_source(nabla_nabla_phi)^2",
            "six_scalar_coefficient": "kappa*w_O2",
            "IR_scaling": "g^3 if the Wilsonian g^2 source S_O2 is nonzero; g^4 for the homogeneous w~g^3 branch",
            "derivation": "beta_w=6w+S_O2*g^2 gives w=-(S_O2/2)g^2+C_w*g^3; the four-scalar one-loop source first occurs at G^2",
            "role": "POTENTIALLY_COLEADING_BUT_CANNOT_CANCEL_O1",
        },
        {
            "operator": "two O(X_source^2) insertions",
            "six_scalar_coefficient": "u_X2^2=(4a2)^2",
            "IR_scaling": "g^4 times the squared resonant logarithm",
            "derivation": "a2~g^2[C+log(k)] on the Gaussian-connected branch",
            "role": "SUBLEADING_EXCHANGE",
        },
        {
            "operator": "O3=C^3",
            "six_scalar_coefficient": "kappa^3*h_C3",
            "IR_scaling": "g^4",
            "derivation": "4958 trajectory has finite h_C3/g",
            "role": "SUBLEADING_CURVATURE_PROJECTOR",
        },
        {
            "operator": "O4=C^2 X_source",
            "six_scalar_coefficient": "kappa^2*u_O4",
            "IR_scaling": "g^4",
            "derivation": "4958 trajectory has finite u_O4/g^2",
            "role": "SUBLEADING_CURVATURE_PROJECTOR",
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC4959_01_projectors",
            "question": "Are the O2 O3 O4 external-scalar projectors explicit and gauge complete?",
            "answer": "yes",
            "status": "O2_O3_O4_PROJECTORS_DERIVED",
            "next_action": "use the full five-projector Gram matrix",
        },
        {
            "decision_id": "DEC4959_02_O2_Ward",
            "question": "Does the O2 metric contact satisfy the Ward identity by itself?",
            "answer": "no; the four scalar-leg attachments are mandatory and their sum closes the identity",
            "status": "O2_CONTACT_PLUS_LEGS_GAUGE_COMPLETION_DERIVED",
            "next_action": "reject contact-only O2 projections",
        },
        {
            "decision_id": "DEC4959_03_cancellation",
            "question": "Can an arbitrary O2 coefficient cancel the gravity-forced X3 amplitude over four-body phase space?",
            "answer": "no" if x3_o2_schur > 0.0 else "undetermined",
            "status": "X3_O2_POSITIVE_SCHUR_LOWER_BOUND" if x3_o2_schur > 0.0 else "X3_O2_BOUND_FAILED",
            "next_action": "derive the O2 momentum-dependent flow for the physical rate, not for existence of number change",
        },
        {
            "decision_id": "DEC4959_04_normalization",
            "question": "Was the 4958 absolute scalar kernel in recent-field normalization?",
            "answer": "no; u_X2=4a2 requires an exact factor 4^4=256 in the absolute kernel",
            "status": "4957_4958_ABSOLUTE_KERNEL_NORMALIZATION_CORRECTED",
            "next_action": "retain ratios and trajectories; use corrected kernels from 4959",
        },
        {
            "decision_id": "DEC4959_05_full",
            "question": "Does this establish full MTS or the calibrated local source coupling?",
            "answer": "no",
            "status": "FULL_MTS_AND_LOCAL_SOURCE_COUPLING_OPEN",
            "next_action": "project the O2 four-scalar p6 flow and then return to the universal local source map",
        },
    ]

    identity_rows = tagged(identity_rows)
    replicas = tagged(replicas)
    gram_rows = tagged(gram_rows)
    trajectory_rows = tagged(trajectory_rows)
    scaling_rows = tagged(scaling_rows)
    decision_rows = tagged(decision_rows)
    write_csv(IDENTITY_CSV, identity_rows)
    write_csv(REPLICATE_CSV, replicas)
    write_csv(GRAM_CSV, gram_rows)
    write_csv(TRAJECTORY_CSV, trajectory_rows)
    write_csv(SCALING_CSV, scaling_rows)
    write_csv(DECISION_CSV, decision_rows)

    result = {
        "checkpoint_marker": MARKER,
        "source_hashes": source_hashes,
        "source_hashes_match": source_hashes_match,
        "identity_checks_pass": identity_pass,
        "projector_basis": list(PROJECTOR_NAMES),
        "projector_convention": {
            "all_external_momenta": "incoming; eta=diag(+---); sum_i k_i=0; k_i^2=0",
            "amplitude": "M6=u_X2^2 P_X2+v_X3 P_X3+kappa w_O2 P_O2+kappa^3 h_C3 P_O3+kappa^2 u_O4 P_O4",
            "kappa": "16 pi g",
            "u_X2_recent": "4 a2_source",
            "v_X3_recent": "8 a3_source",
            "O2_flat_vertex": "-3 s t u",
            "O2_gauge_completion": "metric contact minus four scalar-leg attachments",
            "O3_projector": "24 sum_matchings[Tr(A1A2A3)+Tr(A1A3A2)]",
            "O4_projector": "4 sum_roles[(ki.kj)(Ca.Cb)]",
        },
        "qmc": {
            "seeds": list(PHASE_SEEDS),
            "sobol_power": arguments.phase_power,
            "events_per_replica": 2**arguments.phase_power,
            "gram_eigenvalues": [float(value) for value in gram_eigenvalues],
            "gram_positive_definite": bool(np.min(gram_eigenvalues) > 0.0),
            "scalar_calibration": scalar_calibration,
        },
        "x3_o2_no_cancellation": {
            "gram_determinant": x3_o2_determinant,
            "schur_complement": x3_o2_schur,
            "residual_fraction_after_best_O2_cancellation": x3_o2_residual_fraction,
            "best_kappa_w_over_v_X3": float(-gram[1, 2] / gram[2, 2]),
            "schur_standard_error_across_replicas": statistics.stdev(replica_schur) / math.sqrt(len(replica_schur)),
            "residual_fraction_standard_error_across_replicas": statistics.stdev(replica_residual_fraction) / math.sqrt(len(replica_residual_fraction)),
            "best_ratio_standard_error_across_replicas": statistics.stdev(replica_best_ratio) / math.sqrt(len(replica_best_ratio)),
            "exact_two_event_nonproportionality_determinant": "175/41472",
            "strict_positive": bool(x3_o2_determinant > 0.0 and x3_o2_schur > 0.0),
        },
        "normalization_erratum": {
            "old_4957_4958_prefactor": "a2^4",
            "correct_recent_field_prefactor": "(4a2)^4",
            "exact_multiplicative_correction": 256.0,
            "ratios_fixed_points_and_trajectory_shapes_affected": False,
        },
        "trajectory_bounds": trajectory_rows,
        "gates": {
            "O2_projector": "DERIVED_GAUGE_COMPLETE",
            "O3_projector": "DERIVED_WEYL_GAUGE_INVARIANT",
            "O4_projector": "DERIVED_WEYL_GAUGE_INVARIANT",
            "five_projector_gram": "DERIVED",
            "arbitrary_O2_cannot_cancel_X3_rate": bool(x3_o2_schur > 0.0),
            "O2_parent_coefficient": "OPEN_MOMENTUM_DEPENDENT_FLOW",
            "full_MTS": False,
            "local_GR_Newton_Maxwell_4947": "RETAINED",
        },
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"{MARKER}_DONE identities={identity_pass} gram_pd={np.min(gram_eigenvalues) > 0.0} "
        f"x3_o2_bound={x3_o2_schur > 0.0} full_MTS=False",
        flush=True,
    )
    return 0 if identity_pass and source_hashes_match and np.min(gram_eigenvalues) > 0.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
