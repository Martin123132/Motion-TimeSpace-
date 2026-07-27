from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point as checkpoint_4909
import Y5_R2FR_4911_full_offshell_a6_template_projector as checkpoint_4911
import Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector as checkpoint_4912
import Y5_R2FR_4913_matched_interacting_TTT_smoke as checkpoint_4913


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT = POST / "source-intake" / "mts_residuals"
MARKER = "MTS_COMPLEX_SOURCE_TAYLOR_TTT_REPLICA_4914"
FORMAL_MARKER = "PPC4161_COMPLEX_SOURCE_TTT_ARBITRATION_4914"
CHECKED_DATE = "2026-07-12"
DIMENSIONS = 4
SERIES_ORDER = 6
SOURCE_STENCILS = checkpoint_4913.SOURCE_STENCILS
PAIR_ORDER = ((0, 1), (0, 2), (1, 2))
NEXT_TARGET = (
    "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-"
    "measured-G-calibration-or-closure-demotion.md"
)


@dataclass(frozen=True)
class ReplicaConfig:
    label: str
    size: int
    mu_hat: float
    thermal_sweeps: int
    observations: int
    thin_sweeps: int
    overrelax_sweeps: int
    seed: int

    @property
    def coupling(self) -> float:
        return self.mu_hat ** (8.0 / 3.0)

    @property
    def volume(self) -> int:
        return self.size**DIMENSIONS


def replica_configurations(profile: str) -> list[ReplicaConfig]:
    if profile == "smoke":
        return [
            ReplicaConfig(
                "N12_mu0p6_replica_smoke", 12, 0.6, 180, 160, 1, 1, 491411
            )
        ]
    if profile == "checkpoint":
        return [
            ReplicaConfig(
                "N12_mu0p6_replica", 12, 0.6, 400, 500, 2, 1, 491411
            ),
            ReplicaConfig(
                "N16_mu0p4_replica", 16, 0.4, 550, 450, 2, 1, 491412
            ),
        ]
    raise ValueError(f"unknown replica profile: {profile}")


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def series_convolve(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    shape = np.broadcast_shapes(left.shape[:-1], right.shape[:-1])
    output = np.zeros(shape + (SERIES_ORDER + 1,), dtype=np.complex128)
    for total in range(SERIES_ORDER + 1):
        for first in range(total + 1):
            output[..., total] += (
                left[..., first] * right[..., total - first]
            )
    return output


def cosine_series(scale: float) -> np.ndarray:
    output = np.zeros(SERIES_ORDER + 1, dtype=float)
    for order in range(0, SERIES_ORDER + 1, 2):
        output[order] = (
            (-1.0) ** (order // 2)
            * scale**order
            / math.factorial(order)
        )
    return output


def half_link_factor_series(momentum: np.ndarray) -> np.ndarray:
    output = np.empty(
        (SERIES_ORDER + 1, DIMENSIONS, DIMENSIONS), dtype=float
    )
    for first in range(DIMENSIONS):
        for second in range(DIMENSIONS):
            output[:, first, second] = series_convolve(
                cosine_series(float(momentum[first]) / 2.0),
                cosine_series(float(momentum[second]) / 2.0),
            ).real
    return output


def coordinate_grid(size: int, origin: np.ndarray | None = None) -> np.ndarray:
    coordinates = np.indices((size,) * DIMENSIONS, dtype=float).reshape(
        DIMENSIONS, -1
    )
    if origin is None:
        origin = np.full(DIMENSIONS, (size - 1.0) / 2.0)
    return coordinates - np.asarray(origin, dtype=float)[:, np.newaxis]


def plane_wave_jet(momentum: np.ndarray, coordinates: np.ndarray) -> np.ndarray:
    argument = np.asarray(momentum, dtype=float) @ coordinates
    output = np.empty((SERIES_ORDER + 1, argument.size), dtype=np.complex128)
    for order in range(SERIES_ORDER + 1):
        output[order] = (-1j * argument) ** order / math.factorial(order)
    return output


def build_jet_plan(
    size: int,
    ensemble: list[dict[str, Any]],
    origin: np.ndarray | None = None,
) -> dict[str, Any]:
    coordinates = coordinate_grid(size, origin)
    weights = np.empty(
        (
            len(ensemble),
            3,
            SERIES_ORDER + 1,
            size**DIMENSIONS,
        ),
        dtype=np.complex128,
    )
    contacts: list[dict[str, Any]] = []
    half_factors = np.empty(
        (
            len(ensemble),
            3,
            SERIES_ORDER + 1,
            DIMENSIONS,
            DIMENSIONS,
        ),
        dtype=float,
    )
    for geometry, source in enumerate(ensemble):
        first, pair, triple = checkpoint_4912.determinant_volume_derivatives(
            source["polarizations"]
        )
        contacts.append({"first": first, "pair": pair, "triple": triple})
        for source_index in range(3):
            momentum = np.asarray(
                source["momenta"][source_index], dtype=float
            )
            weights[geometry, source_index] = plane_wave_jet(
                momentum, coordinates
            )
            half_factors[geometry, source_index] = half_link_factor_series(
                momentum
            )
    return {
        "coordinates": coordinates,
        "weights": weights,
        "contacts": contacts,
        "half_factors": half_factors,
        "polarizations": np.asarray(
            [source["polarizations"] for source in ensemble], dtype=float
        ),
    }


def bilinear_density(field: np.ndarray) -> np.ndarray:
    forward = np.stack(
        [np.roll(field, -1, axis=axis) - field for axis in range(DIMENSIONS)]
    )
    backward = np.stack(
        [field - np.roll(field, 1, axis=axis) for axis in range(DIMENSIONS)]
    )
    return 0.25 * (
        np.einsum("m...,n...->mn...", forward, forward)
        + np.einsum("m...,n...->mn...", backward, backward)
    )


def measure_complex_jet_observables(
    field: np.ndarray,
    coupling: float,
    mass_squared: float,
    ensemble: list[dict[str, Any]],
    plan: dict[str, Any],
) -> np.ndarray:
    potential = (
        0.75 * coupling * np.abs(field) ** (4.0 / 3.0)
        + 0.5 * mass_squared * field**2
    ).reshape(-1)
    bilinear = bilinear_density(field).reshape(
        DIMENSIONS, DIMENSIONS, -1
    )
    weights = plan["weights"]
    potential_moments = np.einsum(
        "gsox,x->gso", weights, potential, optimize=True
    )
    bilinear_moments = np.einsum(
        "gsox,mnx->gsomn", weights, bilinear, optimize=True
    )
    output = np.zeros(
        (
            len(SOURCE_STENCILS),
            len(ensemble),
            7,
            SERIES_ORDER + 1,
        ),
        dtype=np.complex128,
    )
    total_potential = float(np.sum(potential))
    for geometry, source in enumerate(ensemble):
        contact = plan["contacts"][geometry]
        for source_index in range(3):
            polarization = np.asarray(
                source["polarizations"][source_index], dtype=float
            )
            site_kinetic = np.einsum(
                "mn,omn->o",
                polarization,
                bilinear_moments[geometry, source_index],
                optimize=True,
            )
            half_kinetic = np.zeros(SERIES_ORDER + 1, dtype=np.complex128)
            factors = plan["half_factors"][geometry, source_index]
            for total in range(SERIES_ORDER + 1):
                for plane_order in range(total + 1):
                    factor_order = total - plane_order
                    half_kinetic[total] += np.einsum(
                        "mn,mn,mn->",
                        polarization,
                        factors[factor_order],
                        bilinear_moments[
                            geometry, source_index, plane_order
                        ],
                        optimize=True,
                    )
            potential_first = (
                float(contact["first"][source_index])
                * potential_moments[geometry, source_index]
            )
            output[0, geometry, source_index] = (
                site_kinetic + potential_first
            )
            output[1, geometry, source_index] = (
                half_kinetic + potential_first
            )
        for pair_index, pair in enumerate(PAIR_ORDER):
            omitted = next(index for index in range(3) if index not in pair)
            pair_moment = np.conjugate(
                potential_moments[geometry, omitted]
            )
            value = float(contact["pair"][pair]) * pair_moment
            output[:, geometry, 3 + pair_index] = value
        output[:, geometry, 6, 0] = (
            float(contact["triple"]) * total_potential
        )
    return output


def measure_site_complex_jet_observables(
    field: np.ndarray,
    coupling: float,
    mass_squared: float,
    ensemble: list[dict[str, Any]],
    plan: dict[str, Any],
) -> np.ndarray:
    potential = (
        0.75 * coupling * np.abs(field) ** (4.0 / 3.0)
        + 0.5 * mass_squared * field**2
    ).reshape(-1)
    bilinear = bilinear_density(field).reshape(
        DIMENSIONS, DIMENSIONS, -1
    )
    weights = plan["weights"]
    kinetic_density = np.einsum(
        "gsmn,mnx->gsx",
        plan["polarizations"],
        bilinear,
        optimize=True,
    )
    potential_moments = np.einsum(
        "gsox,x->gso", weights, potential, optimize=True
    )
    kinetic_moments = np.einsum(
        "gsox,gsx->gso", weights, kinetic_density, optimize=True
    )
    output = np.zeros(
        (len(ensemble), 7, SERIES_ORDER + 1), dtype=np.complex128
    )
    total_potential = float(np.sum(potential))
    for geometry in range(len(ensemble)):
        contact = plan["contacts"][geometry]
        for source_index in range(3):
            output[geometry, source_index] = (
                kinetic_moments[geometry, source_index]
                + float(contact["first"][source_index])
                * potential_moments[geometry, source_index]
            )
        for pair_index, pair in enumerate(PAIR_ORDER):
            omitted = next(index for index in range(3) if index not in pair)
            output[geometry, 3 + pair_index] = (
                float(contact["pair"][pair])
                * np.conjugate(potential_moments[geometry, omitted])
            )
        output[geometry, 6, 0] = (
            float(contact["triple"]) * total_potential
        )
    return output


def measure_complex_scale_observables(
    field: np.ndarray,
    coupling: float,
    mass_squared: float,
    ensemble: list[dict[str, Any]],
    plan: dict[str, Any],
) -> np.ndarray:
    size = field.shape[0]
    potential = (
        0.75 * coupling * np.abs(field) ** (4.0 / 3.0)
        + 0.5 * mass_squared * field**2
    )
    potential_transform = np.fft.fftn(potential)
    bilinear_transform = checkpoint_4913.gradient_bilinear_transforms(field)
    output = np.empty(
        (
            len(SOURCE_STENCILS),
            len(ensemble),
            len(plan["scales"]),
            7,
        ),
        dtype=np.complex128,
    )
    for geometry, source in enumerate(ensemble):
        contact = plan["contacts"][geometry]
        for scale_index, scale in enumerate(plan["scales"]):
            integer_momenta = [
                np.asarray(scale * source["momenta"][index], dtype=int)
                for index in range(3)
            ]
            potential_first = []
            for momentum in integer_momenta:
                index = tuple(int(value) % size for value in momentum)
                potential_first.append(potential_transform[index])
            for stencil_index, stencil in enumerate(SOURCE_STENCILS):
                first_values: list[complex] = []
                for source_index in range(3):
                    momentum = integer_momenta[source_index]
                    index = tuple(int(value) % size for value in momentum)
                    polarization = plan["effective_polarizations"][stencil][
                        geometry, scale_index, source_index
                    ]
                    kinetic = np.einsum(
                        "mn,mn->",
                        polarization,
                        bilinear_transform[
                            (slice(None), slice(None)) + index
                        ],
                        optimize=True,
                    )
                    first_values.append(
                        kinetic
                        + float(contact["first"][source_index])
                        * potential_first[source_index]
                    )
                output[stencil_index, geometry, scale_index, :3] = (
                    first_values
                )
                for pair_index, pair in enumerate(PAIR_ORDER):
                    momentum = (
                        integer_momenta[pair[0]]
                        + integer_momenta[pair[1]]
                    )
                    index = tuple(int(value) % size for value in momentum)
                    output[
                        stencil_index, geometry, scale_index, 3 + pair_index
                    ] = (
                        float(contact["pair"][pair])
                        * potential_transform[index]
                    )
                total_momentum = sum(integer_momenta)
                total_index = tuple(
                    int(value) % size for value in total_momentum
                )
                output[stencil_index, geometry, scale_index, 6] = (
                    float(contact["triple"])
                    * potential_transform[total_index]
                )
    return output


def direct_plane_wave(
    momentum: np.ndarray, coordinates: np.ndarray, q: float
) -> np.ndarray:
    return np.exp(
        -1j * q * (np.asarray(momentum, dtype=float) @ coordinates)
    )


def measure_complex_q_observables(
    field: np.ndarray,
    coupling: float,
    mass_squared: float,
    ensemble: list[dict[str, Any]],
    plan: dict[str, Any],
    q: float,
) -> np.ndarray:
    potential = (
        0.75 * coupling * np.abs(field) ** (4.0 / 3.0)
        + 0.5 * mass_squared * field**2
    ).reshape(-1)
    bilinear = bilinear_density(field).reshape(
        DIMENSIONS, DIMENSIONS, -1
    )
    coordinates = plan["coordinates"]
    output = np.zeros(
        (len(SOURCE_STENCILS), len(ensemble), 7), dtype=np.complex128
    )
    for geometry, source in enumerate(ensemble):
        contact = plan["contacts"][geometry]
        source_waves: list[np.ndarray] = []
        for source_index in range(3):
            momentum = np.asarray(
                source["momenta"][source_index], dtype=float
            )
            wave = direct_plane_wave(momentum, coordinates, q)
            source_waves.append(wave)
            polarization = np.asarray(
                source["polarizations"][source_index], dtype=float
            )
            potential_first = float(contact["first"][source_index]) * (
                wave @ potential
            )
            site_kinetic = np.einsum(
                "mn,mnx,x->",
                polarization,
                bilinear,
                wave,
                optimize=True,
            )
            half_polarization = checkpoint_4913.half_link_polarization(
                polarization, q * momentum
            )
            half_kinetic = np.einsum(
                "mn,mnx,x->",
                half_polarization,
                bilinear,
                wave,
                optimize=True,
            )
            output[0, geometry, source_index] = (
                site_kinetic + potential_first
            )
            output[1, geometry, source_index] = (
                half_kinetic + potential_first
            )
        for pair_index, pair in enumerate(PAIR_ORDER):
            wave = source_waves[pair[0]] * source_waves[pair[1]]
            output[:, geometry, 3 + pair_index] = (
                float(contact["pair"][pair]) * (wave @ potential)
            )
        triple_wave = (
            source_waves[0] * source_waves[1] * source_waves[2]
        )
        output[:, geometry, 6] = (
            float(contact["triple"]) * (triple_wave @ potential)
        )
    return output


def connected_complex_response(observations: np.ndarray) -> np.ndarray:
    means = np.mean(observations, axis=0)
    centered_first = observations[..., :3] - means[..., :3]
    centered_pairs = observations[..., 3:6] - means[..., 3:6]
    return (
        means[..., 6]
        - np.mean(centered_first[..., 0] * centered_pairs[..., 2], axis=0)
        - np.mean(centered_first[..., 1] * centered_pairs[..., 1], axis=0)
        - np.mean(centered_first[..., 2] * centered_pairs[..., 0], axis=0)
        + np.mean(
            centered_first[..., 0]
            * centered_first[..., 1]
            * centered_first[..., 2],
            axis=0,
        )
    )


def connected_complex_jet(observations: np.ndarray) -> np.ndarray:
    means = np.mean(observations, axis=0)
    centered_first = observations[..., :3, :] - means[..., :3, :]
    centered_pairs = observations[..., 3:6, :] - means[..., 3:6, :]
    first_pair = (
        series_convolve(centered_first[..., 0, :], centered_pairs[..., 2, :])
        + series_convolve(
            centered_first[..., 1, :], centered_pairs[..., 1, :]
        )
        + series_convolve(
            centered_first[..., 2, :], centered_pairs[..., 0, :]
        )
    )
    triple = series_convolve(
        series_convolve(
            centered_first[..., 0, :], centered_first[..., 1, :]
        ),
        centered_first[..., 2, :],
    )
    return (
        means[..., 6, :]
        - np.mean(first_pair, axis=0)
        + np.mean(triple, axis=0)
    )


def evaluate_series(series: np.ndarray, q: float) -> np.ndarray:
    powers = q ** np.arange(SERIES_ORDER + 1, dtype=float)
    return np.einsum("...o,o->...", series, powers)


def complex_to_cosine_q6(
    response: np.ndarray,
    ensemble: list[dict[str, Any]],
    phase_sign: float = -1.0,
) -> np.ndarray:
    output = np.empty(response.shape[:-1], dtype=float)
    for geometry, source in enumerate(ensemble):
        phase = np.exp(
            phase_sign * 1j * float(np.sum(source["phases"]))
        )
        output[:, geometry] = 0.25 * np.real(
            phase * response[:, geometry, SERIES_ORDER]
        )
    return output


def complex_amplitude_to_cosine(
    response: np.ndarray, ensemble: list[dict[str, Any]]
) -> np.ndarray:
    output = np.empty(response.shape, dtype=float)
    for geometry, source in enumerate(ensemble):
        phase = np.exp(-1j * float(np.sum(source["phases"])))
        output[..., geometry] = 0.25 * np.real(
            phase * response[..., geometry]
        )
    return output


def algebra_validation() -> list[dict[str, Any]]:
    rng = np.random.default_rng(491400)
    size = 8
    ensemble = checkpoint_4911.random_source_ensemble(3)
    fields = rng.normal(size=(20,) + (size,) * DIMENSIONS)
    plan = build_jet_plan(size, ensemble)
    jet_observations = np.asarray(
        [
            measure_complex_jet_observables(
                field, 0.37, 0.0, ensemble, plan
            )
            for field in fields
        ]
    )
    jet_response = connected_complex_jet(jet_observations)
    optimized_site = measure_site_complex_jet_observables(
        fields[0], 0.37, 0.0, ensemble, plan
    )
    optimized_residual = float(
        np.max(np.abs(optimized_site - jet_observations[0, 0]))
        / max(float(np.max(np.abs(jet_observations[0, 0]))), 1e-30)
    )
    small_q = 2.0e-3
    direct_small = connected_complex_response(
        np.asarray(
            [
                measure_complex_q_observables(
                    field, 0.37, 0.0, ensemble, plan, small_q
                )
                for field in fields
            ]
        )
    )
    reconstructed_small = evaluate_series(jet_response, small_q)
    series_residual = float(
        np.max(np.abs(direct_small - reconstructed_small))
        / max(float(np.max(np.abs(direct_small))), 1e-30)
    )

    shifted_plan = build_jet_plan(
        size, ensemble, np.array([0.3, 1.7, -0.4, 2.2])
    )
    shifted_response = connected_complex_jet(
        np.asarray(
            [
                measure_complex_jet_observables(
                    field, 0.37, 0.0, ensemble, shifted_plan
                )
                for field in fields
            ]
        )
    )
    origin_residual = float(
        np.max(np.abs(jet_response - shifted_response))
        / max(float(np.max(np.abs(jet_response))), 1e-30)
    )

    integer_q = 2.0 * math.pi / size
    real_plan = checkpoint_4913.source_plan(size, 1, ensemble)
    complex_integer = connected_complex_response(
        np.asarray(
            [
                measure_complex_q_observables(
                    field, 0.37, 0.0, ensemble, plan, integer_q
                )
                for field in fields
            ]
        )
    ) / size**DIMENSIONS
    complex_scale_response = connected_complex_response(
        np.asarray(
            [
                measure_complex_scale_observables(
                    field, 0.37, 0.0, ensemble, real_plan
                )
                for field in fields
            ]
        )
    ) / size**DIMENSIONS
    complex_fft_residual = float(
        np.max(
            np.abs(complex_scale_response[..., 1] - complex_integer)
        )
        / max(float(np.max(np.abs(complex_integer))), 1e-30)
    )
    real_observations = np.asarray(
        [
            checkpoint_4913.measure_source_observables(
                field, 0.37, 0.0, ensemble, real_plan
            )
            for field in fields
        ]
    )
    real_response = checkpoint_4913.analytic_cosine_channel_projection(
        checkpoint_4913.connected_response(real_observations)
        / size**DIMENSIONS,
        ensemble,
    )
    signed_responses: dict[tuple[int, int, int], np.ndarray] = {}
    reconstructed_real = np.zeros_like(complex_integer)
    for signs in itertools.product((-1, 1), repeat=3):
        signed_ensemble: list[dict[str, Any]] = []
        for source in ensemble:
            signed_source = dict(source)
            signed_source["momenta"] = (
                np.asarray(source["momenta"], dtype=float)
                * np.asarray(signs, dtype=float)[:, np.newaxis]
            )
            signed_ensemble.append(signed_source)
        signed_response = connected_complex_response(
            np.asarray(
                [
                    measure_complex_q_observables(
                        field,
                        0.37,
                        0.0,
                        signed_ensemble,
                        plan,
                        integer_q,
                    )
                    for field in fields
                ]
            )
        ) / size**DIMENSIONS
        signed_responses[signs] = signed_response
        for geometry, source in enumerate(ensemble):
            effective_phases = np.asarray(source["phases"], dtype=float) + (
                integer_q
                * np.asarray(source["momenta"], dtype=float)
                @ np.full(DIMENSIONS, (size - 1.0) / 2.0)
            )
            phase = np.exp(
                -1j
                * float(
                    np.dot(
                        np.asarray(signs, dtype=float),
                        effective_phases,
                    )
                )
            )
            reconstructed_real[:, geometry] += phase * signed_response[
                :, geometry
            ] / 8.0
    sign_expansion_residual = float(
        np.max(
            np.abs(reconstructed_real.real - real_response[..., 1])
        )
        / max(float(np.max(np.abs(real_response[..., 1]))), 1e-30)
    )
    conjugate_residual = float(
        np.max(
            np.abs(
                signed_responses[(-1, -1, -1)]
                - np.conjugate(signed_responses[(1, 1, 1)])
            )
        )
        / max(
            float(np.max(np.abs(signed_responses[(1, 1, 1)]))), 1e-30
        )
    )
    conserving_pair = np.empty_like(real_response[..., 1])
    for geometry, source in enumerate(ensemble):
        phase = np.exp(-1j * float(np.sum(source["phases"])))
        conserving_pair[:, geometry] = 0.25 * np.real(
            phase * complex_integer[:, geometry]
        )
    leakage_fraction = float(
        np.max(np.abs(real_response[..., 1] - conserving_pair))
        / max(float(np.max(np.abs(real_response[..., 1]))), 1e-30)
    )
    rows = [
        {
            "test": "optimized_site_jet_matches_full_jet",
            "metric": optimized_residual,
            "acceptance": 2e-13,
            "passed": optimized_residual < 2e-13,
        },
        {
            "test": "complex_jet_reconstructs_finite_q_response",
            "metric": series_residual,
            "acceptance": 2e-12,
            "passed": series_residual < 2e-12,
        },
        {
            "test": "complex_jet_origin_invariance",
            "metric": origin_residual,
            "acceptance": 2e-11,
            "passed": origin_residual < 2e-11,
        },
        {
            "test": "complex_FFT_matches_direct_integer_momentum",
            "metric": complex_fft_residual,
            "acceptance": 2e-12,
            "passed": complex_fft_residual < 2e-12,
        },
        {
            "test": "eight_complex_channels_reconstruct_real_cosine",
            "metric": sign_expansion_residual,
            "acceptance": 2e-12,
            "passed": sign_expansion_residual < 2e-12,
            "selected_phase": "minus_for_exp_minus_i_qx_convention",
        },
        {
            "test": "all_minus_is_all_plus_conjugate",
            "metric": conjugate_residual,
            "acceptance": 2e-12,
            "passed": conjugate_residual < 2e-12,
        },
        {
            "test": "finite_sample_nonconserving_channel_fraction",
            "metric": leakage_fraction,
            "acceptance": "diagnostic_only",
            "passed": math.isfinite(leakage_fraction),
        },
    ]
    return tagged(rows)


def sample_free_field(
    size: int, mass: float, rng: np.random.Generator
) -> np.ndarray:
    frequencies = 2.0 * math.pi * np.fft.fftfreq(size)
    mesh = np.meshgrid(
        frequencies, frequencies, frequencies, frequencies, indexing="ij"
    )
    kernel = np.full((size,) * DIMENSIONS, mass**2, dtype=float)
    for component in mesh:
        kernel += 4.0 * np.sin(component / 2.0) ** 2
    white = rng.normal(size=(size,) * DIMENSIONS)
    transformed = np.fft.fftn(white, norm="ortho") / np.sqrt(kernel)
    return np.fft.ifftn(transformed, norm="ortho").real


def exact_free_site_q6(
    size: int, mass: float, ensemble: list[dict[str, Any]]
) -> np.ndarray:
    output = np.empty(len(ensemble), dtype=float)
    for geometry, source in enumerate(ensemble):
        series, residual = checkpoint_4912.complex_TTT_series_density(
            size,
            np.asarray(source["momenta"], dtype=float),
            np.asarray(source["polarizations"], dtype=float),
            mass,
            "nearest",
        )
        if residual > 1e-10:
            raise RuntimeError(
                f"free Taylor inverse residual too large: {residual}"
            )
        phase = np.exp(1j * float(np.sum(source["phases"])))
        output[geometry] = 0.25 * float(np.real(phase * series[6]))
    return output


def jackknife_q6(
    observations: np.ndarray,
    ensemble: list[dict[str, Any]],
    volume: int,
    block_count: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if observations.ndim == 4:
        observations = observations[:, np.newaxis, ...]
    used = len(observations) // block_count * block_count
    observations = observations[:used]
    block_size = used // block_count
    full_response = connected_complex_jet(observations) / volume
    full_q6 = complex_to_cosine_q6(full_response, ensemble)
    samples: list[np.ndarray] = []
    for block in range(block_count):
        keep = np.ones(used, dtype=bool)
        keep[block * block_size : (block + 1) * block_size] = False
        response = connected_complex_jet(observations[keep]) / volume
        samples.append(complex_to_cosine_q6(response, ensemble))
    jackknife = np.asarray(samples)
    centered = jackknife - np.mean(jackknife, axis=0)
    covariance = (
        (block_count - 1.0)
        / block_count
        * np.einsum("bsg,bsh->sgh", centered, centered)
    )
    return full_q6, jackknife, covariance


def free_determinant_smoke(sample_count: int) -> list[dict[str, Any]]:
    size = 4
    mass = 1.0
    block_count = 40 if sample_count >= 800 else 20
    rng = np.random.default_rng(491401)
    ensemble = checkpoint_4911.random_source_ensemble(12)
    plan = build_jet_plan(size, ensemble)
    observations: list[np.ndarray] = []
    start = time.perf_counter()
    for sample in range(sample_count):
        field = sample_free_field(size, mass, rng)
        observations.append(
            measure_complex_jet_observables(
                field, 0.0, mass**2, ensemble, plan
            )
        )
        if (sample + 1) % max(100, sample_count // 5) == 0:
            print(f"4914 free sample {sample + 1}/{sample_count}", flush=True)
    full_q6, _, covariance = jackknife_q6(
        np.asarray(observations),
        ensemble,
        size**DIMENSIONS,
        block_count,
    )
    candidate = full_q6[0]
    target = exact_free_site_q6(size, mass, ensemble)
    standard_error = np.sqrt(np.maximum(np.diag(covariance[0]), 0.0))
    pulls = (candidate - target) / standard_error
    eigenvalues, eigenvectors = np.linalg.eigh(
        0.5 * (covariance[0] + covariance[0].T)
    )
    positive = eigenvalues[eigenvalues > 0]
    floor = max(
        float(np.median(positive)) * 1e-5 if len(positive) else 1e-20,
        float(np.max(eigenvalues)) * 1e-9 if len(eigenvalues) else 1e-20,
        1e-30,
    )
    inverse = (
        eigenvectors * (1.0 / np.maximum(eigenvalues, floor))
    ) @ eigenvectors.T
    difference = candidate - target
    raw_chi_squared = float(difference @ inverse @ difference)
    dimensions = len(ensemble)
    hartlap_factor = (
        (block_count - dimensions - 2.0) / (block_count - 1.0)
        if block_count > dimensions + 2
        else 0.0
    )
    chi_squared = hartlap_factor * raw_chi_squared
    rows: list[dict[str, Any]] = []
    for geometry, source in enumerate(ensemble):
        rows.append(
            {
                "row_type": "geometry",
                "geometry_id": source["geometry_id"],
                "size": size,
                "mass": mass,
                "samples": sample_count,
                "candidate_site_q6": candidate[geometry],
                "exact_site_q6": target[geometry],
                "standard_error": standard_error[geometry],
                "pull": pulls[geometry],
                "passed": abs(pulls[geometry]) < 4.0,
            }
        )
    rows.append(
        {
            "row_type": "summary",
            "geometry_id": "all",
            "size": size,
            "mass": mass,
            "samples": sample_count,
            "candidate_site_q6": "not_applicable",
            "exact_site_q6": "not_applicable",
            "standard_error": "not_applicable",
            "pull": "not_applicable",
            "raw_chi_squared": raw_chi_squared,
            "hartlap_factor": hartlap_factor,
            "chi_squared": chi_squared,
            "degrees_of_freedom": dimensions,
            "reduced_chi_squared": chi_squared / dimensions,
            "maximum_absolute_pull": float(np.max(np.abs(pulls))),
            "elapsed_seconds": time.perf_counter() - start,
            "passed": hartlap_factor > 0.0
            and chi_squared / dimensions < 3.0
            and float(np.max(np.abs(pulls))) < 4.0,
        }
    )
    return tagged(rows)


def mass_jackknife_samples(
    correlations: np.ndarray, size: int, block_count: int
) -> np.ndarray:
    used = len(correlations) // block_count * block_count
    correlations = correlations[:used]
    block_size = used // block_count
    total = np.sum(correlations, axis=0)
    estimates = np.empty(block_count, dtype=float)
    for block in range(block_count):
        start = block * block_size
        stop = start + block_size
        leave_one_out = (
            total - np.sum(correlations[start:stop], axis=0)
        ) / (used - block_size)
        estimates[block] = checkpoint_4909.fit_periodic_mass(
            leave_one_out, size
        )
    return estimates


def exact_free_site_q6_at_pole(
    size: int, pole_mass: float, ensemble: list[dict[str, Any]]
) -> np.ndarray:
    bare_mass = 2.0 * math.sinh(pole_mass / 2.0)
    return exact_free_site_q6(size, bare_mass, ensemble)


def run_replica_chain(
    config: ReplicaConfig,
    ensemble: list[dict[str, Any]],
    matrix_density: np.ndarray,
) -> dict[str, Any]:
    rng = np.random.default_rng(config.seed)
    shape = (config.size,) * DIMENSIONS
    field = np.zeros(shape, dtype=float)
    parity = (np.indices(shape).sum(axis=0) & 1).astype(bool)
    plan = build_jet_plan(config.size, ensemble)
    step = 1.0
    thermal_acceptance: list[float] = []
    start = time.perf_counter()
    for sweep in range(config.thermal_sweeps):
        acceptance = checkpoint_4909.metropolis_sweep(
            field,
            parity,
            config.coupling,
            0.0,
            step,
            rng,
        )
        for _ in range(config.overrelax_sweeps):
            checkpoint_4909.overrelaxation_sweep(
                field, parity, config.coupling, 0.0, rng
            )
        thermal_acceptance.append(acceptance)
        if (sweep + 1) % 50 == 0:
            recent = float(np.mean(thermal_acceptance[-50:]))
            if recent > 0.58:
                step *= 1.08
            elif recent < 0.42:
                step /= 1.08

    observations: list[np.ndarray] = []
    correlations: list[np.ndarray] = []
    zero_mode_squared: list[float] = []
    acceptances: list[float] = []
    overrelax_acceptances: list[float] = []
    for observation in range(config.observations):
        for _ in range(config.thin_sweeps):
            acceptances.append(
                checkpoint_4909.metropolis_sweep(
                    field,
                    parity,
                    config.coupling,
                    0.0,
                    step,
                    rng,
                )
            )
            for _ in range(config.overrelax_sweeps):
                overrelax_acceptances.append(
                    checkpoint_4909.overrelaxation_sweep(
                        field, parity, config.coupling, 0.0, rng
                    )
                )
        if rng.random() < 0.5:
            field *= -1.0
        shifts = tuple(int(value) for value in rng.integers(0, config.size, 4))
        translated = np.roll(field, shifts, axis=(0, 1, 2, 3))
        observations.append(
            measure_site_complex_jet_observables(
                translated, config.coupling, 0.0, ensemble, plan
            )
        )
        correlations.append(checkpoint_4909.measure_plane_correlation(field))
        zero_mode_squared.append(float(np.mean(field) ** 2))
        if (observation + 1) % max(20, config.observations // 5) == 0:
            print(
                f"4914 {config.label} observation {observation + 1}/"
                f"{config.observations}",
                flush=True,
            )

    observation_array = np.asarray(observations)
    correlation_array = np.asarray(correlations)
    tau = checkpoint_4909.integrated_autocorrelation(
        np.asarray(zero_mode_squared)
    )
    mass_fit = checkpoint_4909.jackknife_mass(
        correlation_array, config.size, tau
    )
    pole_mass = float(mass_fit["mass"])
    pole_mass_error = float(mass_fit["mass_standard_error"])
    block_size = max(4, int(math.ceil(2.0 * tau)))
    block_count = config.observations // block_size
    if block_count < 20:
        block_count = min(20, config.observations // 2)
        block_size = config.observations // block_count
    used = block_count * block_size
    observation_array = observation_array[:used]
    correlation_array = correlation_array[:used]
    full_q6, jackknife, _ = jackknife_q6(
        observation_array, ensemble, config.volume, block_count
    )
    interacting_q6 = full_q6[0]
    interacting_jackknife = jackknife[:, 0]
    mass_jackknife = mass_jackknife_samples(
        correlation_array, config.size, block_count
    )
    finite_mass = np.isfinite(mass_jackknife)
    mass_jackknife[~finite_mass] = pole_mass

    exact_start = time.perf_counter()
    exact_center = exact_free_site_q6_at_pole(
        config.size, pole_mass, ensemble
    )
    derivative_step = max(0.01 * pole_mass, 0.002)
    lower_pole = max(pole_mass - derivative_step, 0.02)
    upper_pole = pole_mass + derivative_step
    exact_lower = exact_free_site_q6_at_pole(
        config.size, lower_pole, ensemble
    )
    exact_upper = exact_free_site_q6_at_pole(
        config.size, upper_pole, ensemble
    )
    exact_derivative = (exact_upper - exact_lower) / (
        upper_pole - lower_pole
    )
    linearization_residual = float(
        np.linalg.norm(0.5 * (exact_upper + exact_lower) - exact_center)
        / max(float(np.linalg.norm(exact_center)), 1e-30)
    )
    exact_elapsed = time.perf_counter() - exact_start

    delta_q6 = interacting_q6 - exact_center
    delta_jackknife = (
        interacting_jackknife
        - exact_center[np.newaxis, :]
        - (mass_jackknife - pole_mass)[:, np.newaxis] * exact_derivative
    )
    centered = delta_jackknife - np.mean(delta_jackknife, axis=0)
    covariance = (
        (block_count - 1.0) / block_count * centered.T @ centered
    )
    recovered = checkpoint_4913.correlated_quotient_recovery(
        matrix_density, delta_q6, covariance
    )
    jackknife_zeta = np.asarray(
        [
            checkpoint_4913.correlated_quotient_recovery(
                matrix_density, sample, covariance
            )["zeta"]
            for sample in delta_jackknife
        ]
    )
    zeta_error = math.sqrt(
        (block_count - 1.0)
        / block_count
        * float(
            np.sum((jackknife_zeta - np.mean(jackknife_zeta)) ** 2)
        )
    )
    derivative_recovery = checkpoint_4913.correlated_quotient_recovery(
        matrix_density, exact_derivative, covariance
    )
    mass_error_projection = (
        abs(float(derivative_recovery["zeta"])) * pole_mass_error
    )
    zeta_renormalized = (
        checkpoint_4913.TARGET_ZETA_M2 / pole_mass**2
        + float(recovered["zeta"])
    )
    response_errors = np.sqrt(np.maximum(np.diag(covariance), 0.0))

    predecessor_label = (
        "N12_mu0p6" if config.size == 12 else "N16_mu0p4"
    )
    predecessor_rows = [
        row
        for row in read_csv(
            OUTPUT / "P8_Y5_R2FR_4913_PROJECTED_RECOVERY.csv"
        )
        if row["config"] == predecessor_label and row["stencil"] == "site"
    ]
    if len(predecessor_rows) != 1:
        raise RuntimeError("missing unique 4913 site predecessor row")
    predecessor = predecessor_rows[0]
    predecessor_zeta = float(predecessor["zeta"])
    predecessor_error = float(
        predecessor["zeta_delta_standard_error"]
    )
    independent_shift = abs(
        float(recovered["zeta"]) - predecessor_zeta
    ) / math.hypot(zeta_error, predecessor_error)
    return {
        "config": config,
        "summary": {
            **asdict(config),
            "coupling": config.coupling,
            "proposal_step": step,
            "mean_metropolis_acceptance": float(np.mean(acceptances)),
            "mean_overrelax_acceptance": float(
                np.mean(overrelax_acceptances)
            ),
            "tau_zero_mode_observations": tau,
            "block_size": block_size,
            "block_count": block_count,
            "used_observations": used,
            "pole_mass": pole_mass,
            "pole_mass_standard_error": pole_mass_error,
            "finite_mass_jackknife_fraction": float(np.mean(finite_mass)),
            "exact_free_derivative_step": derivative_step,
            "exact_free_linearization_residual": linearization_residual,
            "exact_free_elapsed_seconds": exact_elapsed,
            "elapsed_seconds": time.perf_counter() - start,
        },
        "interacting_q6": interacting_q6,
        "exact_free_q6": exact_center,
        "exact_free_mass_derivative": exact_derivative,
        "delta_q6": delta_q6,
        "response_errors": response_errors,
        "covariance": covariance,
        "recovery": {
            **recovered,
            "zeta_delta_standard_error": zeta_error,
            "zeta_delta_significance": float(recovered["zeta"])
            / zeta_error
            if zeta_error > 0
            else math.nan,
            "mass_error_projection": mass_error_projection,
            "zeta_renormalized": zeta_renormalized,
            "zeta_renormalized_times_mu2": zeta_renormalized
            * config.mu_hat**2,
            "predecessor_4913_zeta": predecessor_zeta,
            "predecessor_4913_standard_error": predecessor_error,
            "independent_4913_shift_sigma": independent_shift,
        },
    }


def discrete_fit_parameters(size: int) -> tuple[int, int]:
    if size == 12:
        return 3, 3
    if size == 16:
        return 4, 3
    raise ValueError(f"no discrete fit window for N={size}")


def complex_discrete_q6(
    observations: np.ndarray,
    ensemble: list[dict[str, Any]],
    volume: int,
    size: int,
    maximum_scale: int,
    fit_degree: int,
) -> np.ndarray:
    response = connected_complex_response(observations) / volume
    scales = np.arange(maximum_scale + 1, dtype=float)
    x = (2.0 * math.pi * scales / size) ** 2
    design = np.vander(x, fit_degree + 1, increasing=True)
    weights = np.linalg.pinv(design, rcond=1e-13)[3]
    complex_coefficient = np.einsum(
        "tgs,s->tg", response, weights, optimize=True
    )
    return complex_amplitude_to_cosine(complex_coefficient, ensemble)


def run_discrete_replica_chain(
    config: ReplicaConfig,
    ensemble: list[dict[str, Any]],
    matrix_density: np.ndarray,
) -> dict[str, Any]:
    maximum_scale, fit_degree = discrete_fit_parameters(config.size)
    rng = np.random.default_rng(config.seed + 100)
    shape = (config.size,) * DIMENSIONS
    field = np.zeros(shape, dtype=float)
    parity = (np.indices(shape).sum(axis=0) & 1).astype(bool)
    plan = checkpoint_4913.source_plan(
        config.size, maximum_scale, ensemble
    )
    step = 1.0
    thermal_acceptance: list[float] = []
    start = time.perf_counter()
    for sweep in range(config.thermal_sweeps):
        acceptance = checkpoint_4909.metropolis_sweep(
            field,
            parity,
            config.coupling,
            0.0,
            step,
            rng,
        )
        for _ in range(config.overrelax_sweeps):
            checkpoint_4909.overrelaxation_sweep(
                field, parity, config.coupling, 0.0, rng
            )
        thermal_acceptance.append(acceptance)
        if (sweep + 1) % 50 == 0:
            recent = float(np.mean(thermal_acceptance[-50:]))
            if recent > 0.58:
                step *= 1.08
            elif recent < 0.42:
                step /= 1.08

    observations: list[np.ndarray] = []
    correlations: list[np.ndarray] = []
    zero_mode_squared: list[float] = []
    acceptances: list[float] = []
    overrelax_acceptances: list[float] = []
    for observation in range(config.observations):
        for _ in range(config.thin_sweeps):
            acceptances.append(
                checkpoint_4909.metropolis_sweep(
                    field,
                    parity,
                    config.coupling,
                    0.0,
                    step,
                    rng,
                )
            )
            for _ in range(config.overrelax_sweeps):
                overrelax_acceptances.append(
                    checkpoint_4909.overrelaxation_sweep(
                        field, parity, config.coupling, 0.0, rng
                    )
                )
        if rng.random() < 0.5:
            field *= -1.0
        shifts = tuple(int(value) for value in rng.integers(0, config.size, 4))
        translated = np.roll(field, shifts, axis=(0, 1, 2, 3))
        observations.append(
            measure_complex_scale_observables(
                translated, config.coupling, 0.0, ensemble, plan
            )
        )
        correlations.append(checkpoint_4909.measure_plane_correlation(field))
        zero_mode_squared.append(float(np.mean(field) ** 2))
        if (observation + 1) % max(20, config.observations // 5) == 0:
            print(
                f"4914 complex {config.label} observation {observation + 1}/"
                f"{config.observations}",
                flush=True,
            )

    observation_array = np.asarray(observations)
    correlation_array = np.asarray(correlations)
    tau = checkpoint_4909.integrated_autocorrelation(
        np.asarray(zero_mode_squared)
    )
    mass_fit = checkpoint_4909.jackknife_mass(
        correlation_array, config.size, tau
    )
    pole_mass = float(mass_fit["mass"])
    pole_mass_error = float(mass_fit["mass_standard_error"])
    block_size = max(4, int(math.ceil(2.0 * tau)))
    block_count = config.observations // block_size
    if block_count < 20:
        block_count = min(20, config.observations // 2)
        block_size = config.observations // block_count
    used = block_count * block_size
    observation_array = observation_array[:used]
    full_interacting_q6 = complex_discrete_q6(
        observation_array,
        ensemble,
        config.volume,
        config.size,
        maximum_scale,
        fit_degree,
    )
    jackknife_q6_rows: list[np.ndarray] = []
    for block in range(block_count):
        keep = np.ones(used, dtype=bool)
        keep[block * block_size : (block + 1) * block_size] = False
        jackknife_q6_rows.append(
            complex_discrete_q6(
                observation_array[keep],
                ensemble,
                config.volume,
                config.size,
                maximum_scale,
                fit_degree,
            )
        )
    jackknife_q6_array = np.asarray(jackknife_q6_rows)

    exact_config = checkpoint_4913.InteractingConfig(
        config.label,
        config.size,
        config.mu_hat,
        config.thermal_sweeps,
        config.observations,
        config.thin_sweeps,
        config.overrelax_sweeps,
        config.seed,
        maximum_scale,
        fit_degree,
        pole_mass,
    )
    exact_start = time.perf_counter()
    exact_grid, exact_elapsed = checkpoint_4913.exact_free_response_grid(
        exact_config, ensemble, pole_mass
    )
    exact_free_q6 = checkpoint_4913.q6_fit(exact_grid, exact_config)
    exact_elapsed = max(
        exact_elapsed, time.perf_counter() - exact_start
    )
    delta_q6 = full_interacting_q6 - exact_free_q6
    delta_jackknife = (
        jackknife_q6_array - exact_free_q6[np.newaxis, ...]
    )
    flattened = delta_jackknife.reshape(block_count, -1)
    flattened_centered = flattened - np.mean(flattened, axis=0)
    cross_stencil_covariance = (
        (block_count - 1.0)
        / block_count
        * flattened_centered.T
        @ flattened_centered
    )

    recoveries: list[dict[str, Any]] = []
    covariance_rows: list[np.ndarray] = []
    response_errors = np.empty_like(delta_q6)
    predecessor_label = (
        "N12_mu0p6" if config.size == 12 else "N16_mu0p4"
    )
    predecessor_table = read_csv(
        OUTPUT / "P8_Y5_R2FR_4913_PROJECTED_RECOVERY.csv"
    )
    for stencil_index, stencil in enumerate(SOURCE_STENCILS):
        samples = delta_jackknife[:, stencil_index]
        centered = samples - np.mean(samples, axis=0)
        covariance = (
            (block_count - 1.0) / block_count * centered.T @ centered
        )
        covariance_rows.append(covariance)
        response_errors[stencil_index] = np.sqrt(
            np.maximum(np.diag(covariance), 0.0)
        )
        recovered = checkpoint_4913.correlated_quotient_recovery(
            matrix_density, delta_q6[stencil_index], covariance
        )
        jackknife_zeta = np.asarray(
            [
                checkpoint_4913.correlated_quotient_recovery(
                    matrix_density, sample, covariance
                )["zeta"]
                for sample in samples
            ]
        )
        zeta_error = math.sqrt(
            (block_count - 1.0)
            / block_count
            * float(
                np.sum(
                    (jackknife_zeta - np.mean(jackknife_zeta)) ** 2
                )
            )
        )
        predecessor_rows = [
            row
            for row in predecessor_table
            if row["config"] == predecessor_label
            and row["stencil"] == stencil
        ]
        if len(predecessor_rows) != 1:
            raise RuntimeError("missing unique 4913 predecessor row")
        predecessor = predecessor_rows[0]
        predecessor_zeta = float(predecessor["zeta"])
        predecessor_error = float(
            predecessor["zeta_delta_standard_error"]
        )
        independent_shift = abs(
            float(recovered["zeta"]) - predecessor_zeta
        ) / math.hypot(zeta_error, predecessor_error)
        zeta_renormalized = (
            checkpoint_4913.TARGET_ZETA_M2 / pole_mass**2
            + float(recovered["zeta"])
        )
        recoveries.append(
            {
                "stencil": stencil,
                **recovered,
                "zeta_delta_standard_error": zeta_error,
                "zeta_delta_significance": float(recovered["zeta"])
                / zeta_error
                if zeta_error > 0
                else math.nan,
                "zeta_renormalized": zeta_renormalized,
                "zeta_renormalized_times_mu2": zeta_renormalized
                * config.mu_hat**2,
                "predecessor_4913_zeta": predecessor_zeta,
                "predecessor_4913_standard_error": predecessor_error,
                "independent_4913_shift_sigma": independent_shift,
            }
        )
    scales = np.arange(maximum_scale + 1, dtype=float)
    design = np.vander(
        (2.0 * math.pi * scales / config.size) ** 2,
        fit_degree + 1,
        increasing=True,
    )
    return {
        "config": config,
        "summary": {
            **asdict(config),
            "estimator": "all_plus_complex_discrete_FFT",
            "coupling": config.coupling,
            "maximum_scale": maximum_scale,
            "fit_degree": fit_degree,
            "q6_design_condition": float(np.linalg.cond(design)),
            "q6_weight_l2": float(
                np.linalg.norm(np.linalg.pinv(design, rcond=1e-13)[3])
            ),
            "proposal_step": step,
            "mean_metropolis_acceptance": float(np.mean(acceptances)),
            "mean_overrelax_acceptance": float(
                np.mean(overrelax_acceptances)
            ),
            "tau_zero_mode_observations": tau,
            "block_size": block_size,
            "block_count": block_count,
            "used_observations": used,
            "pole_mass": pole_mass,
            "pole_mass_standard_error": pole_mass_error,
            "mass_uncertainty_propagated": False,
            "exact_free_elapsed_seconds": exact_elapsed,
            "elapsed_seconds": time.perf_counter() - start,
        },
        "interacting_q6": full_interacting_q6,
        "exact_free_q6": exact_free_q6,
        "delta_q6": delta_q6,
        "response_errors": response_errors,
        "covariances": covariance_rows,
        "cross_stencil_covariance": cross_stencil_covariance,
        "recoveries": recoveries,
    }


def run_discrete_replica(profile: str) -> dict[str, Any]:
    geometry_ids, matrix_density = checkpoint_4913.load_geometric_matrix()
    ensemble = checkpoint_4911.random_source_ensemble(len(geometry_ids))
    if [source["geometry_id"] for source in ensemble] != geometry_ids:
        raise RuntimeError("4914 discrete source ensemble order mismatch")
    start = time.perf_counter()
    results = [
        run_discrete_replica_chain(config, ensemble, matrix_density)
        for config in replica_configurations(profile)
    ]
    return {
        "profile": profile,
        "geometry_ids": geometry_ids,
        "results": results,
        "elapsed_seconds": time.perf_counter() - start,
    }


def write_discrete_replica_outputs(result: dict[str, Any]) -> None:
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_CHAIN_SUMMARY.csv",
        tagged([item["summary"] for item in result["results"]]),
    )
    response_rows: list[dict[str, Any]] = []
    covariance_rows: list[dict[str, Any]] = []
    cross_rows: list[dict[str, Any]] = []
    recovery_rows: list[dict[str, Any]] = []
    for item in result["results"]:
        config = item["config"]
        for stencil_index, stencil in enumerate(SOURCE_STENCILS):
            for geometry, geometry_id in enumerate(result["geometry_ids"]):
                response_rows.append(
                    {
                        "config": config.label,
                        "stencil": stencil,
                        "geometry_id": geometry_id,
                        "interacting_complex_q6": item["interacting_q6"][
                            stencil_index, geometry
                        ],
                        "exact_mass_matched_free_q6": item["exact_free_q6"][
                            stencil_index, geometry
                        ],
                        "matched_delta_q6": item["delta_q6"][
                            stencil_index, geometry
                        ],
                        "matched_delta_standard_error": item[
                            "response_errors"
                        ][stencil_index, geometry],
                    }
                )
            covariance = item["covariances"][stencil_index]
            for first, first_id in enumerate(result["geometry_ids"]):
                for second, second_id in enumerate(result["geometry_ids"]):
                    covariance_rows.append(
                        {
                            "config": config.label,
                            "stencil": stencil,
                            "geometry_i": first_id,
                            "geometry_j": second_id,
                            "covariance": covariance[first, second],
                        }
                    )
            recovery = item["recoveries"][stencil_index]
            recovery_rows.append(
                {
                    "config": config.label,
                    **{
                        key: value
                        for key, value in recovery.items()
                        if key not in {"coefficients", "reconstructed"}
                    },
                }
            )
        labels = [
            f"{stencil}:{geometry_id}"
            for stencil in SOURCE_STENCILS
            for geometry_id in result["geometry_ids"]
        ]
        for first, first_label in enumerate(labels):
            for second, second_label in enumerate(labels):
                cross_rows.append(
                    {
                        "config": config.label,
                        "channel_i": first_label,
                        "channel_j": second_label,
                        "covariance": item["cross_stencil_covariance"][
                            first, second
                        ],
                    }
                )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_Q6_RESPONSES.csv",
        tagged(response_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_Q6_COVARIANCE.csv",
        tagged(covariance_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_CROSS_STENCIL_COVARIANCE.csv",
        tagged(cross_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_PROJECTED_REPLICA.csv",
        tagged(recovery_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_REPLICA_RUN_STATUS.csv",
        tagged(
            [
                {
                    "profile": result["profile"],
                    "config_count": len(result["results"]),
                    "elapsed_seconds": result["elapsed_seconds"],
                    "next_target": NEXT_TARGET,
                }
            ]
        ),
    )


def mass_propagation() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    geometry_ids, matrix_density = checkpoint_4913.load_geometric_matrix()
    ensemble = checkpoint_4911.random_source_ensemble(len(geometry_ids))
    summaries = read_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_CHAIN_SUMMARY.csv"
    )
    responses = read_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_Q6_RESPONSES.csv"
    )
    covariance_table = read_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_DISCRETE_Q6_COVARIANCE.csv"
    )
    projected_table = read_csv(
        OUTPUT / "P8_Y5_R2FR_4914_COMPLEX_PROJECTED_REPLICA.csv"
    )
    geometry_rows: list[dict[str, Any]] = []
    projected_rows: list[dict[str, Any]] = []
    for summary in summaries:
        label = summary["label"]
        size = int(summary["size"])
        pole_mass = float(summary["pole_mass"])
        pole_mass_error = float(summary["pole_mass_standard_error"])
        maximum_scale = int(summary["maximum_scale"])
        fit_degree = int(summary["fit_degree"])
        derivative_step = max(0.01 * pole_mass, 0.002)
        lower_pole = max(pole_mass - derivative_step, 0.02)
        upper_pole = pole_mass + derivative_step
        exact_config = checkpoint_4913.InteractingConfig(
            label,
            size,
            float(summary["mu_hat"]),
            int(summary["thermal_sweeps"]),
            int(summary["observations"]),
            int(summary["thin_sweeps"]),
            int(summary["overrelax_sweeps"]),
            int(summary["seed"]),
            maximum_scale,
            fit_degree,
            pole_mass,
        )
        lower_grid, lower_elapsed = checkpoint_4913.exact_free_response_grid(
            exact_config, ensemble, lower_pole
        )
        upper_grid, upper_elapsed = checkpoint_4913.exact_free_response_grid(
            exact_config, ensemble, upper_pole
        )
        lower_q6 = checkpoint_4913.q6_fit(lower_grid, exact_config)
        upper_q6 = checkpoint_4913.q6_fit(upper_grid, exact_config)
        derivative = (upper_q6 - lower_q6) / (
            upper_pole - lower_pole
        )
        center = np.empty((len(SOURCE_STENCILS), len(geometry_ids)))
        for stencil_index, stencil in enumerate(SOURCE_STENCILS):
            selected = [
                row
                for row in responses
                if row["config"] == label and row["stencil"] == stencil
            ]
            selected_map = {row["geometry_id"]: row for row in selected}
            for geometry, geometry_id in enumerate(geometry_ids):
                center[stencil_index, geometry] = float(
                    selected_map[geometry_id]["exact_mass_matched_free_q6"]
                )
                geometry_rows.append(
                    {
                        "config": label,
                        "stencil": stencil,
                        "geometry_id": geometry_id,
                        "pole_mass": pole_mass,
                        "pole_mass_standard_error": pole_mass_error,
                        "derivative_step": derivative_step,
                        "exact_free_q6_center": center[
                            stencil_index, geometry
                        ],
                        "exact_free_q6_lower": lower_q6[
                            stencil_index, geometry
                        ],
                        "exact_free_q6_upper": upper_q6[
                            stencil_index, geometry
                        ],
                        "d_exact_free_q6_d_pole_mass": derivative[
                            stencil_index, geometry
                        ],
                    }
                )
        midpoint = 0.5 * (lower_q6 + upper_q6)
        linearization_residual = float(
            np.linalg.norm(midpoint - center)
            / max(float(np.linalg.norm(center)), 1e-30)
        )
        for stencil_index, stencil in enumerate(SOURCE_STENCILS):
            covariance = np.empty((len(geometry_ids), len(geometry_ids)))
            selected_covariance = [
                row
                for row in covariance_table
                if row["config"] == label and row["stencil"] == stencil
            ]
            covariance_map = {
                (row["geometry_i"], row["geometry_j"]): row
                for row in selected_covariance
            }
            for first, first_id in enumerate(geometry_ids):
                for second, second_id in enumerate(geometry_ids):
                    covariance[first, second] = float(
                        covariance_map[(first_id, second_id)]["covariance"]
                    )
            derivative_recovery = (
                checkpoint_4913.correlated_quotient_recovery(
                    matrix_density, derivative[stencil_index], covariance
                )
            )
            selected_projected = [
                row
                for row in projected_table
                if row["config"] == label and row["stencil"] == stencil
            ]
            if len(selected_projected) != 1:
                raise RuntimeError("missing unique projected mass row")
            projected = selected_projected[0]
            zeta = float(projected["zeta"])
            statistical_error = float(
                projected["zeta_delta_standard_error"]
            )
            mass_component = (
                abs(float(derivative_recovery["zeta"])) * pole_mass_error
            )
            quadrature_error = math.hypot(
                statistical_error, mass_component
            )
            conservative_error = statistical_error + mass_component
            projected_rows.append(
                {
                    "config": label,
                    "stencil": stencil,
                    "zeta_delta": zeta,
                    "statistical_standard_error": statistical_error,
                    "d_zeta_free_d_pole_mass": float(
                        derivative_recovery["zeta"]
                    ),
                    "mass_standard_error_component": mass_component,
                    "quadrature_standard_error": quadrature_error,
                    "conservative_standard_error": conservative_error,
                    "quadrature_significance": zeta / quadrature_error
                    if quadrature_error > 0
                    else math.nan,
                    "conservative_significance": zeta
                    / conservative_error
                    if conservative_error > 0
                    else math.nan,
                    "exact_free_linearization_residual": linearization_residual,
                    "exact_derivative_elapsed_seconds": lower_elapsed
                    + upper_elapsed,
                    "mass_TTT_cross_covariance_included": False,
                    "promotion_allowed": False,
                }
            )
    return tagged(geometry_rows), tagged(projected_rows)


def run_replica(profile: str) -> dict[str, Any]:
    geometry_ids, matrix_density = checkpoint_4913.load_geometric_matrix()
    ensemble = checkpoint_4911.random_source_ensemble(len(geometry_ids))
    if [source["geometry_id"] for source in ensemble] != geometry_ids:
        raise RuntimeError("4914 source ensemble order mismatch")
    start = time.perf_counter()
    results = [
        run_replica_chain(config, ensemble, matrix_density)
        for config in replica_configurations(profile)
    ]
    return {
        "profile": profile,
        "geometry_ids": geometry_ids,
        "results": results,
        "elapsed_seconds": time.perf_counter() - start,
    }


def write_replica_outputs(result: dict[str, Any]) -> None:
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_REPLICA_CHAIN_SUMMARY.csv",
        tagged([item["summary"] for item in result["results"]]),
    )
    response_rows: list[dict[str, Any]] = []
    covariance_rows: list[dict[str, Any]] = []
    recovery_rows: list[dict[str, Any]] = []
    for item in result["results"]:
        config = item["config"]
        for geometry, geometry_id in enumerate(result["geometry_ids"]):
            response_rows.append(
                {
                    "config": config.label,
                    "geometry_id": geometry_id,
                    "interacting_direct_q6": item["interacting_q6"][geometry],
                    "exact_mass_matched_free_q6": item["exact_free_q6"][
                        geometry
                    ],
                    "exact_free_mass_derivative": item[
                        "exact_free_mass_derivative"
                    ][geometry],
                    "matched_delta_q6": item["delta_q6"][geometry],
                    "matched_delta_standard_error": item["response_errors"][
                        geometry
                    ],
                }
            )
        for first, first_id in enumerate(result["geometry_ids"]):
            for second, second_id in enumerate(result["geometry_ids"]):
                covariance_rows.append(
                    {
                        "config": config.label,
                        "geometry_i": first_id,
                        "geometry_j": second_id,
                        "covariance": item["covariance"][first, second],
                    }
                )
        recovery_rows.append(
            {
                "config": config.label,
                **{
                    key: value
                    for key, value in item["recovery"].items()
                    if key not in {"coefficients", "reconstructed"}
                },
            }
        )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_DIRECT_Q6_RESPONSES.csv",
        tagged(response_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_DIRECT_Q6_COVARIANCE.csv",
        tagged(covariance_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_PROJECTED_REPLICA.csv",
        tagged(recovery_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4914_REPLICA_RUN_STATUS.csv",
        tagged(
            [
                {
                    "profile": result["profile"],
                    "config_count": len(result["results"]),
                    "elapsed_seconds": result["elapsed_seconds"],
                    "next_target": NEXT_TARGET,
                }
            ]
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("algebra", "free", "replica", "mass"),
        default="algebra",
    )
    parser.add_argument("--free-samples", type=int, default=400)
    parser.add_argument(
        "--replica-profile", choices=("smoke", "checkpoint"), default="smoke"
    )
    parser.add_argument(
        "--replica-estimator",
        choices=("direct_jet", "complex_discrete"),
        default="complex_discrete",
    )
    parser.add_argument("--run-directory", type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if arguments.mode == "mass":
        geometry_rows, projected_rows = mass_propagation()
        write_csv(
            OUTPUT / "P8_Y5_R2FR_4914_EXACT_FREE_MASS_DERIVATIVE.csv",
            geometry_rows,
        )
        write_csv(
            OUTPUT / "P8_Y5_R2FR_4914_MASS_AUGMENTED_PROJECTION.csv",
            projected_rows,
        )
        passed = all(
            row["exact_free_linearization_residual"] < 0.02
            and not row["promotion_allowed"]
            for row in projected_rows
        )
        print(
            "P8_Y5_R2FR_4914_MASS_PROPAGATION_PASS"
            if passed
            else "P8_Y5_R2FR_4914_MASS_PROPAGATION_FAIL"
        )
        for row in projected_rows:
            print(row)
        return 0 if passed else 1
    if arguments.mode == "replica":
        if arguments.run_directory:
            arguments.run_directory.mkdir(parents=True, exist_ok=True)
            (arguments.run_directory / "status.json").write_text(
                json.dumps(
                    {
                        "status": "RUNNING",
                        "profile": arguments.replica_profile,
                        "estimator": arguments.replica_estimator,
                        "started_unix": time.time(),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        try:
            if arguments.replica_estimator == "direct_jet":
                result = run_replica(arguments.replica_profile)
                write_replica_outputs(result)
                summaries = [
                    {
                        "config": item["config"].label,
                        "stencil": "site",
                        "zeta_delta": item["recovery"]["zeta"],
                        "zeta_delta_standard_error": item["recovery"][
                            "zeta_delta_standard_error"
                        ],
                        "euclidean_residual": item["recovery"][
                            "euclidean_residual"
                        ],
                        "independent_4913_shift_sigma": item["recovery"][
                            "independent_4913_shift_sigma"
                        ],
                    }
                    for item in result["results"]
                ]
            else:
                result = run_discrete_replica(arguments.replica_profile)
                write_discrete_replica_outputs(result)
                summaries = [
                    {
                        "config": item["config"].label,
                        "stencil": recovered["stencil"],
                        "zeta_delta": recovered["zeta"],
                        "zeta_delta_standard_error": recovered[
                            "zeta_delta_standard_error"
                        ],
                        "euclidean_residual": recovered[
                            "euclidean_residual"
                        ],
                        "independent_4913_shift_sigma": recovered[
                            "independent_4913_shift_sigma"
                        ],
                    }
                    for item in result["results"]
                    for recovered in item["recoveries"]
                ]
            if arguments.run_directory:
                (arguments.run_directory / "status.json").write_text(
                    json.dumps(
                        {
                            "status": "COMPLETE",
                            "profile": arguments.replica_profile,
                            "estimator": arguments.replica_estimator,
                            "elapsed_seconds": result["elapsed_seconds"],
                            "summary": summaries,
                        },
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                (arguments.run_directory / "COMPLETE.marker").write_text(
                    "MTS_4914_REPLICA_COMPLETE\n", encoding="utf-8"
                )
            print(
                f"4914 replica profile={arguments.replica_profile} "
                f"estimator={arguments.replica_estimator} "
                f"elapsed={result['elapsed_seconds']:.3f}s"
            )
            for summary in summaries:
                print(summary)
            return 0
        except Exception as error:
            if arguments.run_directory:
                (arguments.run_directory / "status.json").write_text(
                    json.dumps(
                        {
                            "status": "ERROR",
                            "profile": arguments.replica_profile,
                            "estimator": arguments.replica_estimator,
                            "error": repr(error),
                        },
                        indent=2,
                    ),
                    encoding="utf-8",
                )
            raise
    rows: list[dict[str, Any]] = []
    if arguments.mode == "algebra":
        algebra_rows = algebra_validation()
        write_csv(
            OUTPUT / "P8_Y5_R2FR_4914_JET_ALGEBRA_VALIDATION.csv",
            algebra_rows,
        )
        rows.extend(algebra_rows)
    if arguments.mode == "free":
        free_rows = free_determinant_smoke(arguments.free_samples)
        write_csv(
            OUTPUT / "P8_Y5_R2FR_4914_FREE_DETERMINANT_JET_SMOKE.csv",
            free_rows,
        )
        rows.extend(free_rows)
    passed = all(row["passed"] for row in rows)
    print(
        "P8_Y5_R2FR_4914_COMPLEX_JET_VALIDATION_PASS"
        if passed
        else "P8_Y5_R2FR_4914_COMPLEX_JET_VALIDATION_FAIL"
    )
    for row in rows:
        print(row)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
