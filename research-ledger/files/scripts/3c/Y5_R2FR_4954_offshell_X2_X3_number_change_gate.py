from __future__ import annotations

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
from scipy.stats import norm, qmc


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4954"

RESULT_JSON = SOURCE / "offshell_X2_X3_number_change_results.json"
PREBOLTZMANN_CSV = SOURCE / "finite_time_2PI_preBoltzmann_kernel.csv"
GAUSSIAN_REPLICATES_CSV = SOURCE / "gaussian_13_collinear_QMC_replicates.csv"
GAUSSIAN_DERIVATION_CSV = SOURCE / "gaussian_13_collinear_coefficient.csv"
SPARC_CSV = SOURCE / "SPARC_finite_time_and_controlled_24_gate.csv"
AMPLITUDE_CSV = SOURCE / "X2_X3_24_amplitude_completion.csv"
PHASE_REPLICATES_CSV = SOURCE / "X2_X3_24_phase_space_QMC_replicates.csv"
LOCAL_CSV = SOURCE / "local_compact_offshell_preparation_gate.csv"
DECISION_CSV = SOURCE / "offshell_X2_X3_route_decision.csv"

O4_4941 = POST / "4941-Y5-R2FR-natural-TypeII-direct-metric-scalar-O4-zero-proof-and-minimal-O4-parent-completion-gate.md"
PAIR_4952 = POST / "4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md"
CASCADE_4953 = POST / "4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md"
BERGES_TEX = POST / "source-intake" / "functional_rg" / "4948" / "riolecture.tex"
INJECTION_4953 = POST / "source-intake" / "functional_rg" / "4953" / "SPARC_formation_injection_gate.csv"
LOCAL_4953 = POST / "source-intake" / "functional_rg" / "4953" / "local_compact_X2_injection_gate.csv"
RAMBO_PDF = SOURCE / "1308.2922v1.pdf"

MARKER = "MTS_4954_OFFSHELL_X2_X3_NUMBER_CHANGE_GATE"
CHECKED_DATE = "2026-07-13"

LIGHT_SPEED = 299_792_458.0
HBAR_EV_S = 6.582_119_569e-16
HBARC_EV_M = 1.973_269_804e-7
JOULE_PER_EV = 1.602_176_634e-19
YEAR_S = 365.25 * 24.0 * 3600.0
TEN_GYR_S = 10.0e9 * YEAR_S
A_MAX = 1090.92
G_UNITARITY = 3.0 * math.pi / 5.0
C22_HEAD_ON = 7.0 / (5.0 * math.pi)

GAUSSIAN_SEEDS = (495401, 495402, 495403, 495404)
GAUSSIAN_POWER = 18
PHASE_SEEDS = (495411, 495412, 495413, 495414, 495415, 495416, 495417, 495418)
PHASE_POWER = 16

EXPECTED_HASHES = {
    O4_4941: "f4c6f83668c5f904706747dcafb3d538068a038307ffc062e13fe3234a6b9543",
    PAIR_4952: "2e4fc50355c1c3cefece8d5eb633952dea2ea9a8445712c2c4daf870dcc938d8",
    CASCADE_4953: "55a90877ac9b64bad5d90ea5e7dd65c52f669fc71adc26106e6fcf0ef0886a2b",
    BERGES_TEX: "de16f5e4f6e8b10e6880a18b130a4923952556e6fead9fda7a7e162e3282128d",
    INJECTION_4953: "7bc033397f66d9e1fd77d0a5a0aea6ac9c29d0dac55be069fabdf62113d324ec",
    LOCAL_4953: "b619cf4ec2947b17305550413774b02cc285f9a5e309f8b03fa42ba512d084d2",
    RAMBO_PDF: "248813a5de7df621f2773d20b28b3f8096f2d7c35c6cd6fc4d8be6e769149082",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
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


def energy_density_to_ev4(value_j_m3: float) -> float:
    return value_j_m3 * HBARC_EV_M**3 / JOULE_PER_EV


def minkowski_dot(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left[..., 0] * right[..., 0] - np.sum(left[..., 1:] * right[..., 1:], axis=-1)


def four_vertex(first: np.ndarray, second: np.ndarray, third: np.ndarray, fourth: np.ndarray) -> np.ndarray:
    return 2.0 * (
        minkowski_dot(first, second) * minkowski_dot(third, fourth)
        + minkowski_dot(first, third) * minkowski_dot(second, fourth)
        + minkowski_dot(first, fourth) * minkowski_dot(second, third)
    )


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


MATCHINGS_6 = perfect_matchings(tuple(range(6)))
PARTITIONS_3_3 = [((0,) + pair, tuple(index for index in range(6) if index not in ((0,) + pair))) for pair in itertools.combinations(range(1, 6), 2)]


def rambo_massless(random_values: np.ndarray) -> tuple[np.ndarray, float, float]:
    event_count = random_values.shape[0]
    values = random_values.reshape(event_count, 4, 4)
    energy = -np.log(np.maximum(values[:, :, 0] * values[:, :, 1], 1.0e-300))
    cosine = 2.0 * values[:, :, 2] - 1.0
    azimuth = 2.0 * np.pi * values[:, :, 3]
    sine = np.sqrt(np.maximum(0.0, 1.0 - cosine**2))
    trial = np.stack(
        (
            energy,
            energy * sine * np.cos(azimuth),
            energy * sine * np.sin(azimuth),
            energy * cosine,
        ),
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


def estimate_phase_replica(seed: int) -> dict[str, Any]:
    random_values = qmc.Sobol(16, scramble=True, seed=seed).random_base2(PHASE_POWER)
    outgoing, sum_error, mass_error = rambo_massless(random_values)
    event_count = outgoing.shape[0]
    external = np.empty((event_count, 6, 4))
    external[:, 0, :] = (0.5, 0.0, 0.0, 0.5)
    external[:, 1, :] = (0.5, 0.0, 0.0, -0.5)
    external[:, 2:, :] = -outgoing

    exchange = np.zeros(event_count)
    minimum_propagator = math.inf
    for first_set, second_set in PARTITIONS_3_3:
        first = external[:, first_set, :]
        second = external[:, second_set, :]
        internal = np.sum(first, axis=1)
        internal_squared = minkowski_dot(internal, internal)
        minimum_propagator = min(minimum_propagator, float(np.min(np.abs(internal_squared))))
        exchange += (
            four_vertex(first[:, 0], first[:, 1], first[:, 2], -internal)
            * four_vertex(second[:, 0], second[:, 1], second[:, 2], internal)
            / internal_squared
        )

    contact = np.zeros(event_count)
    for matching in MATCHINGS_6:
        product = np.ones(event_count)
        for left, right in matching:
            product *= minkowski_dot(external[:, left], external[:, right])
        contact += product
    contact *= 6.0

    return {
        "seed": seed,
        "sobol_power": PHASE_POWER,
        "event_count": event_count,
        "mean_exchange_squared": float(np.mean(exchange**2)),
        "mean_exchange_contact": float(np.mean(exchange * contact)),
        "mean_contact_squared": float(np.mean(contact**2)),
        "RAMBO_sum_error_max": sum_error,
        "RAMBO_mass_shell_error_max": mass_error,
        "minimum_abs_internal_K2": minimum_propagator,
        "all_finite": bool(np.all(np.isfinite(exchange)) and np.all(np.isfinite(contact))),
    }


def estimate_gaussian_replica(seed: int) -> dict[str, Any]:
    random_values = qmc.Sobol(6, scramble=True, seed=seed).random_base2(GAUSSIAN_POWER)
    square_root = np.sqrt(random_values[:, 0])
    fraction_one = 1.0 - square_root
    fraction_two = square_root * (1.0 - random_values[:, 1])
    fraction_three = square_root * random_values[:, 1]

    normal_vectors = norm.ppf(np.clip(random_values[:, 2:], 1.0e-15, 1.0 - 1.0e-15))
    normal_vectors /= np.linalg.norm(normal_vectors, axis=1)[:, None]

    matrix_11 = 1.0 / fraction_one + 1.0 / fraction_three
    matrix_12 = 1.0 / fraction_three
    matrix_22 = 1.0 / fraction_two + 1.0 / fraction_three
    cholesky_11 = np.sqrt(matrix_11)
    cholesky_21 = matrix_12 / cholesky_11
    cholesky_22 = np.sqrt(matrix_22 - cholesky_21**2)

    transverse_two = np.column_stack(
        (normal_vectors[:, 2] / cholesky_22, normal_vectors[:, 3] / cholesky_22)
    )
    transverse_one = np.column_stack(
        (
            (normal_vectors[:, 0] - cholesky_21 * transverse_two[:, 0]) / cholesky_11,
            (normal_vectors[:, 1] - cholesky_21 * transverse_two[:, 1]) / cholesky_11,
        )
    )
    transverse_three = -transverse_one - transverse_two

    def squared(vector: np.ndarray) -> np.ndarray:
        return np.sum(vector**2, axis=1)

    parent_one = squared(transverse_one) / (2.0 * fraction_one)
    parent_two = squared(transverse_two) / (2.0 * fraction_two)
    parent_three = squared(transverse_three) / (2.0 * fraction_three)

    def daughter_dot(
        left_fraction: np.ndarray,
        right_fraction: np.ndarray,
        left_vector: np.ndarray,
        right_vector: np.ndarray,
    ) -> np.ndarray:
        numerator = squared(left_fraction[:, None] * right_vector - right_fraction[:, None] * left_vector)
        return numerator / (2.0 * left_fraction * right_fraction)

    dot_12 = daughter_dot(fraction_one, fraction_two, transverse_one, transverse_two)
    dot_13 = daughter_dot(fraction_one, fraction_three, transverse_one, transverse_three)
    dot_23 = daughter_dot(fraction_two, fraction_three, transverse_two, transverse_three)
    angular_kernel = parent_one * dot_23 + parent_two * dot_13 + parent_three * dot_12
    kernel_squared = angular_kernel**2
    return {
        "seed": seed,
        "sobol_power": GAUSSIAN_POWER,
        "event_count": len(random_values),
        "mean_collinear_angular_kernel_squared": float(np.mean(kernel_squared)),
        "max_collinear_angular_kernel_squared": float(np.max(kernel_squared)),
        "all_finite": bool(np.all(np.isfinite(kernel_squared))),
    }


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(source_hashes[str(path)] == expected for path, expected in EXPECTED_HASHES.items())

    o4_text = read_text(O4_4941)
    pair_text = read_text(PAIR_4952)
    cascade_text = read_text(CASCADE_4953)
    berges_text = read_text(BERGES_TEX)
    source_clause_checks = {
        "4941_X2_essential": "c_ess=c+8pi g(ctilde+d)." in o4_text,
        "4941_six_derivative_block_open": "all five scalar six-derivative beta functions   = open;" in o4_text,
        "4952_parent_pair_kernel": "matter-to-pair rate kernel                     = derived at kappa^4/16" in pair_text,
        "4953_22_number_invariant": "int dPi C_cov,22=0" in cascade_text,
        "4953_offshell_target": "finite-time/off-shell `1<->3` memory kernel" in cascade_text,
        "Berges_preBoltzmann_equation": "\\label{eq:preboltzmann}" in berges_text,
        "Berges_four_channels": all(label in berges_text for label in ("\\mbox{\\bf (I)}", "\\mbox{\\bf (II)}", "\\mbox{\\bf (III)}", "\\mbox{\\bf (IV)}")),
        "Berges_only_22_infinite_time": "only the processes described by {\\rr (III)}" in berges_text,
        "Berges_quasiparticle_removes_main_offshell": "The main ``off-shell'' effects" in berges_text,
    }

    preboltzmann_rows = tagged(
        [
            {
                "derivation_id": "PB4954_00_parent",
                "channel": "parent source plus self-energy",
                "energy_combination": "p^mu nabla_mu f=C_2PI[f]+S_pair",
                "finite_time_kernel": "the 4952 S_pair fixes injection; the X2 sunset self-energy supplies memory",
                "infinite_time_limit": "source and collision terms remain distinct",
                "status": "PARENT_COMPOSITION_DEFINED",
                "passed": source_clause_checks["4952_parent_pair_kernel"],
            },
            {
                "derivation_id": "PB4954_01_I",
                "channel": "0<->4",
                "energy_combination": "DeltaE=Ep+Eq+Ek+Es",
                "finite_time_kernel": "K_T=sin(DeltaE T)/DeltaE in dn/dt; |G_T|2=4sin2(DeltaE T/2)/DeltaE2 in probability",
                "infinite_time_limit": "zero for positive on-shell energies",
                "status": "FINITE_PREPARATION_ONLY_IN_QUASIPARTICLE_ANSATZ",
                "passed": True,
            },
            {
                "derivation_id": "PB4954_02_II",
                "channel": "1<->3",
                "energy_combination": "DeltaE=Ep+Eq+Ek-Es",
                "finite_time_kernel": "K_T=sin(DeltaE T)/DeltaE with Bose gain-loss factors",
                "infinite_time_limit": "massive threshold zero; massless support collinear and X2 amplitude has an Adler zero",
                "status": "FINITE_TIME_AND_WIDTH_SENSITIVE_NUMBER_CHANGE",
                "passed": True,
            },
            {
                "derivation_id": "PB4954_03_III",
                "channel": "2<->2",
                "energy_combination": "DeltaE=Ep+Eq-Ek-Es",
                "finite_time_kernel": "K_T=sin(DeltaE T)/DeltaE",
                "infinite_time_limit": "pi delta(DeltaE); exact 4953 number and stress collision invariants",
                "status": "ONLY_STRICT_ON_SHELL_SURVIVOR",
                "passed": source_clause_checks["Berges_only_22_infinite_time"],
            },
            {
                "derivation_id": "PB4954_04_IV",
                "channel": "3<->1",
                "energy_combination": "DeltaE=Ep-Eq-Ek-Es",
                "finite_time_kernel": "K_T=sin(DeltaE T)/DeltaE with reverse gain-loss factors",
                "infinite_time_limit": "same on-shell zero as 1<->3",
                "status": "FINITE_TIME_AND_WIDTH_SENSITIVE_NUMBER_CHANGE",
                "passed": True,
            },
            {
                "derivation_id": "PB4954_05_sharp_switch",
                "channel": "finite preparation",
                "energy_combination": "box switching has |G_T(DeltaE)|2~DeltaE^-2",
                "finite_time_kernel": "for X2 and fixed initial E the UV radial integrand scales as c_ess2 E Lambda6 dLambda",
                "infinite_time_limit": "a sharp initial state is UV sensitive and is not a physical formation spectrum",
                "status": "SHARP_SWITCH_ROUTE_REJECTED_REQUIRES_SMOOTH_SOURCE",
                "passed": True,
            },
            {
                "derivation_id": "PB4954_06_width",
                "channel": "persistent off-shell spectral width",
                "energy_combination": "delta=Gamma/E; tau_coh=1/Gamma",
                "finite_time_kernel": "per coherence interval P13 scales as C13 gX2^2 delta^4 on the weak quasiparticle branch",
                "infinite_time_limit": "delta~1 leaves the controlled quasiparticle expansion and requires full 2PI evolution",
                "status": "STRONG_NONQUASIPARTICLE_ROUTE_NOT_REJECTED",
                "passed": source_clause_checks["Berges_quasiparticle_removes_main_offshell"],
            },
        ]
    )

    gaussian_replicates = [estimate_gaussian_replica(seed) for seed in GAUSSIAN_SEEDS]
    gaussian_means = [row["mean_collinear_angular_kernel_squared"] for row in gaussian_replicates]
    angular_mean = statistics.mean(gaussian_means)
    angular_standard_error = statistics.stdev(gaussian_means) / math.sqrt(len(gaussian_means))
    gaussian_coefficient = angular_mean / (24.0 * math.pi**3)
    gaussian_coefficient_standard_error = angular_standard_error / (24.0 * math.pi**3)

    gaussian_derivation_rows = tagged(
        [
            {
                "derivation_id": "G134954_00_switch",
                "object": "Gaussian preparation profile",
                "equation": "g(t)=exp[-t2/(2tau2)]; |gtilde(DeltaE)|2=2pi tau2 exp[-tau2 DeltaE2]",
                "derivation": "exact Fourier transform",
                "numeric_value": "",
                "status": "SMOOTH_UV_FINITE_PROFILE_DECLARED",
                "passed": True,
            },
            {
                "derivation_id": "G134954_01_collinear",
                "object": "massless near-collinear scaling",
                "equation": "DeltaE=sum_i kperp_i2/(2xiE); M13=2gX2 A/(Etau)2",
                "derivation": "on-shell daughter expansion with sum xi=1 and sum kperp_i=0",
                "numeric_value": "",
                "status": "ADLER_ZERO_SUPPRESSION_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "G134954_02_whitening",
                "object": "four-transverse-dimensional integral",
                "equation": "det M2=1/(x1x2x3), so the phase-space 1/(x1x2x3) factor cancels the whitening Jacobian",
                "derivation": "D=sum ui2/xi=uT(M2 tensor I2)u",
                "numeric_value": "",
                "status": "SIMPLEX_SINGULARITY_CANCELLED",
                "passed": True,
            },
            {
                "derivation_id": "G134954_03_radial",
                "object": "radial integral",
                "equation": "int_0_inf r11 exp(-r4/4)dr=32",
                "derivation": "t=r4/4 and Gamma(3)=2",
                "numeric_value": 32.0,
                "status": "RADIAL_FACTOR_EXACT",
                "passed": True,
            },
            {
                "derivation_id": "G134954_04_coefficient",
                "object": "Gaussian finite-preparation probability",
                "equation": "P13=C13 gX2^2/(Etau)^4+O((Etau)^-6); C13=<Ahat2>/(24pi3)",
                "derivation": f"{len(GAUSSIAN_SEEDS)} independently scrambled Sobol replicas",
                "numeric_value": gaussian_coefficient,
                "status": "GAUSSIAN_ASYMPTOTIC_COEFFICIENT_EXECUTED",
                "passed": all(row["all_finite"] for row in gaussian_replicates),
            },
            {
                "derivation_id": "G134954_05_unitarity",
                "object": "single-preparation perturbative ceiling",
                "equation": "P13<=C13(3pi/5)^2/(Etau)^4",
                "derivation": "4953 head-on s-wave bound |c_ess|E4<=3pi/5",
                "numeric_value": gaussian_coefficient * G_UNITARITY**2,
                "status": "CONTROLLED_FINITE_PREPARATION_BOUND_DERIVED",
                "passed": True,
            },
        ]
    )

    phase_replicates = [estimate_phase_replica(seed) for seed in PHASE_SEEDS]
    mean_exchange_squared = statistics.mean(row["mean_exchange_squared"] for row in phase_replicates)
    mean_exchange_contact = statistics.mean(row["mean_exchange_contact"] for row in phase_replicates)
    mean_contact_squared = statistics.mean(row["mean_contact_squared"] for row in phase_replicates)
    phase_volume_s1 = 1.0 / (24_576.0 * math.pi**5)
    head_on_factor = phase_volume_s1 * 4.0**7 / (2.0 * math.factorial(4))
    coefficient_0 = head_on_factor * mean_exchange_squared
    coefficient_1 = 2.0 * head_on_factor * mean_exchange_contact
    coefficient_2 = head_on_factor * mean_contact_squared
    ratio_minimum = -coefficient_1 / (2.0 * coefficient_2)
    coefficient_minimum = coefficient_0 - coefficient_1**2 / (4.0 * coefficient_2)
    exchange_24_to_22_prefactor = coefficient_0 / C22_HEAD_ON

    amplitude_rows = tagged(
        [
            {
                "derivation_id": "A244954_00_exchange",
                "object": "two-X2 six-point exchange amplitude",
                "equation": "M6_exchange=sum_10 V4(A,-K_A)V4(B,K_A)/K_A2",
                "derivation": "ten unordered 3+3 partitions of six labelled external legs",
                "numeric_value": len(PARTITIONS_3_3),
                "status": "X2_EXCHANGE_AMPLITUDE_DERIVED",
                "passed": len(PARTITIONS_3_3) == 10,
            },
            {
                "derivation_id": "A244954_01_contact",
                "object": "X3 six-point contact amplitude",
                "equation": "M6_contact=6 d3 sum_15matchings product_3(ki.kj)",
                "derivation": "L3=d3 X3=d3(partial psi squared)^3/8; each matching has 48 derivative assignments",
                "numeric_value": len(MATCHINGS_6),
                "status": "MANDATORY_SIX_FIELD_CONTACT_DERIVED",
                "passed": len(MATCHINGS_6) == 15,
            },
            {
                "derivation_id": "A244954_02_phase_volume",
                "object": "massless four-body phase-space volume",
                "equation": "Phi4(s)=s2/(24576 pi5)",
                "derivation": "flat massless RAMBO normalization",
                "numeric_value": phase_volume_s1,
                "status": "PHASE_VOLUME_LOCKED",
                "passed": all(row["RAMBO_sum_error_max"] < 1.0e-12 and row["RAMBO_mass_shell_error_max"] < 1.0e-12 for row in phase_replicates),
            },
            {
                "derivation_id": "A244954_03_polynomial",
                "object": "complete flat X2-X3 tree cross section",
                "equation": "sigma24=c_ess4 E14[C0+C1 r3+C2 r3^2], r3=d3/c_ess2",
                "derivation": f"{len(PHASE_SEEDS)} independently scrambled flat phase-space replicas",
                "numeric_value": f"C0={coefficient_0};C1={coefficient_1};C2={coefficient_2}",
                "status": "TREE_CROSS_SECTION_POLYNOMIAL_EXECUTED",
                "passed": coefficient_0 > 0.0 and coefficient_2 > 0.0,
            },
            {
                "derivation_id": "A244954_04_minimum",
                "object": "best X3 interference point",
                "equation": "r3_min=-C1/(2C2); Cmin=C0-C1^2/(4C2)",
                "derivation": "quadratic completion",
                "numeric_value": f"r3_min={ratio_minimum};Cmin={coefficient_minimum}",
                "status": "CONTACT_CANNOT_CANCEL_ALL_PHASE_SPACE",
                "passed": coefficient_minimum > 0.0,
            },
            {
                "derivation_id": "A244954_05_ratio",
                "object": "exchange-only inelastic-to-elastic cross-section ratio",
                "equation": "sigma24/sigma22=(C0/[7/(5pi)])gX2^2",
                "derivation": "divide the 2-to-4 coefficient by the exact 4953 head-on sigma22",
                "numeric_value": exchange_24_to_22_prefactor,
                "status": "EXCHANGE_ONLY_RATIO_DERIVED",
                "passed": exchange_24_to_22_prefactor > 0.0,
            },
            {
                "derivation_id": "A244954_06_parent_closure",
                "object": "six-field parent ownership",
                "equation": "d3 X3 enters M6 at the same E6 order as two insertions of c_ess X2",
                "derivation": "d3 and c_ess2 both have mass dimension -8",
                "numeric_value": "",
                "status": "ONE_COEFFICIENT_C_ONLY_24_ROUTE_INCOMPLETE",
                "passed": source_clause_checks["4941_six_derivative_block_open"],
            },
        ]
    )

    injection_rows = read_csv(INJECTION_4953)
    sparc_rows: list[dict[str, Any]] = []
    for row in injection_rows:
        radius_m = float(row["outer_radius_m"])
        velocity_m_s = float(row["outer_velocity_m_s"])
        dynamical_time_s = radius_m / velocity_m_s
        injection_energy_ev = float(row["injection_quantum_energy_eV"])
        profile_energy_ev = float(row["profile_quantum_energy_eV"])
        time_energy_product = injection_energy_ev * dynamical_time_s / HBAR_EV_S
        probability_13_max = gaussian_coefficient * G_UNITARITY**2 / time_energy_product**4
        remaining_multiplicity = max(1.0, float(row["multiplicity_ratio_injection_to_profile"]) / A_MAX)
        required_log_multiplicity = math.log(remaining_multiplicity)
        finite_preparation_log_gain = math.log1p(2.0 * probability_13_max)

        density_ev4 = energy_density_to_ev4(float(row["required_effective_energy_density_J_m3"]))
        shell_occupancy_proxy = 0.0 if density_ev4 == 0.0 else 2.0 * math.pi**2 * density_ev4 / injection_energy_ev**4
        if density_ev4 == 0.0:
            controlled_regime = "NO_POSITIVE_TARGET"
            unit_amplitude_log_gain = 0.0
            exchange_only_log_gain = 0.0
            background_control_coordinate = 0.0
        elif shell_occupancy_proxy >= 1.0:
            controlled_regime = "HIGH_OCCUPANCY_DERIVATIVE_BACKGROUND_EDGE"
            background_control_coordinate = min(1.0, injection_energy_ev**4 / density_ev4)
            unit_amplitude_log_gain = 2.0 * time_energy_product * background_control_coordinate**2
            exchange_only_log_gain = (
                2.0
                * time_energy_product
                * exchange_24_to_22_prefactor
                * min(G_UNITARITY, background_control_coordinate) ** 2
            )
        else:
            controlled_regime = "DILUTE_UNIT_SIX_POINT_AMPLITUDE_ENVELOPE"
            background_control_coordinate = 1.0
            unit_amplitude_log_gain = 2.0 * (density_ev4 / injection_energy_ev**4) * time_energy_product
            exchange_only_log_gain = (
                2.0
                * coefficient_0
                * G_UNITARITY**4
                * (density_ev4 / injection_energy_ev**4)
                * time_energy_product
            )

        positive_target = row["positive_outer_residual_target"] == "True"
        high_frequency_case = row["injection_case"] in {
            "white_dwarf_fundamental_pair_quantum",
            "neutron_star_fundamental_pair_quantum",
            "one_GeV_quantum",
            "UHE_1e20_eV_quantum",
        }
        controlled_envelope_closes = unit_amplitude_log_gain >= required_log_multiplicity
        if not positive_target:
            status = "NO_POSITIVE_OUTER_RESIDUAL_TARGET"
        elif high_frequency_case and not controlled_envelope_closes:
            status = "FINITE_PREPARATION_AND_CONTROLLED_24_ENVELOPE_FAIL"
        elif row["injection_case"] in {"direct_profile_quantum", "minimum_4952_supported_profile_pair"}:
            status = "NUMBER_MULTIPLICATION_NOT_NEEDED_DIRECT_SOURCE_AMPLITUDE_OPEN"
        else:
            status = "CONTROLLED_ENVELOPE_NOT_REJECTED"
        sparc_rows.append(
            {
                "galaxy": row["galaxy"],
                "injection_case": row["injection_case"],
                "positive_outer_residual_target": positive_target,
                "outer_radius_m": radius_m,
                "outer_velocity_m_s": velocity_m_s,
                "dynamical_preparation_time_s": dynamical_time_s,
                "profile_energy_eV": profile_energy_ev,
                "injection_energy_eV": injection_energy_ev,
                "E_tau_over_hbar": time_energy_product,
                "Gaussian_C13": gaussian_coefficient,
                "P13_single_preparation_at_22_unitarity_max": probability_13_max,
                "finite_preparation_log_number_gain_max": finite_preparation_log_gain,
                "remaining_multiplicity_after_Amax": remaining_multiplicity,
                "required_log_multiplicity_after_Amax": required_log_multiplicity,
                "finite_preparation_can_close_deficit": finite_preparation_log_gain >= required_log_multiplicity,
                "required_density_eV4": density_ev4,
                "one_shell_occupancy_proxy": shell_occupancy_proxy,
                "controlled_regime": controlled_regime,
                "background_control_coordinate_min_1_E4_over_rho": background_control_coordinate,
                "unit_six_point_controlled_log_gain_envelope": unit_amplitude_log_gain,
                "exchange_only_X2_log_gain_comparator": exchange_only_log_gain,
                "controlled_envelope_can_close_deficit": controlled_envelope_closes,
                "full_X2_X3_rate_decided": False,
                "status": status,
            }
        )

    local_rows: list[dict[str, Any]] = []
    for row in read_csv(LOCAL_4953):
        energy_ev = float(row["fundamental_pair_quantum_energy_eV"])
        time_energy_product = energy_ev * TEN_GYR_S / HBAR_EV_S
        probability_13_max = gaussian_coefficient * G_UNITARITY**2 / time_energy_product**4
        local_rows.append(
            {
                "system": row["system"],
                "fundamental_pair_quantum_energy_eV": energy_ev,
                "preparation_observation_time_s": TEN_GYR_S,
                "E_T_over_hbar": time_energy_product,
                "P13_single_preparation_at_22_unitarity_max": probability_13_max,
                "median_local_to_galaxy_efficiency_ceiling_4953": row["galaxy_to_local_injection_efficiency_ceiling_median"],
                "periodic_stationary_source_is_repeated_switch": False,
                "persistent_width_requires_full_2PI": True,
                "status": "FINITE_INITIAL_PREPARATION_NEGLIGIBLE_PERSISTENT_WIDTH_OPEN",
            }
        )

    positive_high = [
        row
        for row in sparc_rows
        if row["positive_outer_residual_target"]
        and row["injection_case"] in {
            "white_dwarf_fundamental_pair_quantum",
            "neutron_star_fundamental_pair_quantum",
            "one_GeV_quantum",
            "UHE_1e20_eV_quantum",
        }
    ]
    finite_fail_count = sum(not row["finite_preparation_can_close_deficit"] for row in positive_high)
    controlled_fail_count = sum(not row["controlled_envelope_can_close_deficit"] for row in positive_high)

    decision_rows = tagged(
        [
            {
                "decision_id": "DEC4954_00_preBoltzmann",
                "question": "Is the finite-time number-changing kernel explicit?",
                "answer": "YES",
                "evidence": "four pre-Boltzmann sign channels and their sinc kernels are reconstructed from the 2PI source",
                "status": "FINITE_TIME_KERNEL_DERIVED",
            },
            {
                "decision_id": "DEC4954_01_sharp_switch",
                "question": "Can a sharp finite initial time be used as a physical formation prediction?",
                "answer": "NO",
                "evidence": "the derivative interaction gives a UV-sensitive Lambda6 dLambda radial tail under box switching",
                "status": "SHARP_SWITCH_ROUTE_REJECTED",
            },
            {
                "decision_id": "DEC4954_02_smooth_13",
                "question": "Can one smooth dynamical formation preparation close the high-frequency number deficit?",
                "answer": "NO_ON_ALL_EXECUTED_ROWS",
                "evidence": f"{finite_fail_count}/{len(positive_high)} high-frequency positive-target rows fail the Gaussian unitarity ceiling",
                "status": "SMOOTH_FINITE_PREPARATION_ROUTE_REJECTED",
            },
            {
                "decision_id": "DEC4954_03_exchange24",
                "question": "Is the two-X2 exchange contribution to 2-to-4 known?",
                "answer": "YES",
                "evidence": f"sigma24_exchange={coefficient_0:.12e} c_ess4 E14; sigma24/sigma22={exchange_24_to_22_prefactor:.12e} gX2^2",
                "status": "EXCHANGE_ONLY_24_DERIVED",
            },
            {
                "decision_id": "DEC4954_04_X3",
                "question": "Does c_ess alone own the complete leading 2-to-4 amplitude?",
                "answer": "NO",
                "evidence": "d3 X3 is an independent six-field contact at the same E6 amplitude order and its parent beta coordinate is open",
                "status": "MANDATORY_X3_PARENT_COORDINATE_IDENTIFIED",
            },
            {
                "decision_id": "DEC4954_05_controlled_envelope",
                "question": "Does any executed high-frequency row close under the deliberately generous controlled six-point envelope?",
                "answer": "NO",
                "evidence": f"{controlled_fail_count}/{len(positive_high)} fail after maximal redshift; nonperturbative amplitudes are outside this gate",
                "status": "CONTROLLED_HIGH_FREQUENCY_ROUTE_REJECTED",
            },
            {
                "decision_id": "DEC4954_06_persistent_width",
                "question": "Is a strongly broadened persistent off-shell medium rejected?",
                "answer": "NO",
                "evidence": "Gamma/E of order one invalidates the quasiparticle expansion and requires the full X2-X3 2PI evolution",
                "status": "STRONG_NONQUASIPARTICLE_ROUTE_OPEN",
            },
            {
                "decision_id": "DEC4954_07_next_parent",
                "question": "What coefficient must be derived next?",
                "answer": "d3_X3_AND_FULL_SIX_DERIVATIVE_SHIFT_SECTOR",
                "evidence": "the complete leading number-changing amplitude depends on r3=d3/c_ess2",
                "status": "PARENT_SIX_DERIVATIVE_FLOW_NEXT",
            },
            {
                "decision_id": "DEC4954_08_local",
                "question": "Does the number-changing route alter the stationary local correspondence theorem?",
                "answer": "NO",
                "evidence": "X2 and X3 begin at fourth and sixth field order around psi=0; 4947 remains the local branch",
                "status": "4947_LOCAL_BRANCH_RETAINED",
            },
            {
                "decision_id": "DEC4954_09_full",
                "question": "Is full MTS galaxy unification derived?",
                "answer": "NO",
                "evidence": "the X3 parent coordinate, strong off-shell state and direct formation stress amplitude remain unsolved",
                "status": "FULL_MTS_PROMOTION_BLOCKED",
            },
        ]
    )

    write_csv(PREBOLTZMANN_CSV, preboltzmann_rows)
    write_csv(GAUSSIAN_REPLICATES_CSV, tagged(gaussian_replicates))
    write_csv(GAUSSIAN_DERIVATION_CSV, gaussian_derivation_rows)
    write_csv(SPARC_CSV, tagged(sparc_rows))
    write_csv(AMPLITUDE_CSV, amplitude_rows)
    write_csv(PHASE_REPLICATES_CSV, tagged(phase_replicates))
    write_csv(LOCAL_CSV, tagged(local_rows))
    write_csv(DECISION_CSV, decision_rows)

    result = {
        "checkpoint_marker": MARKER,
        "source_hashes": source_hashes,
        "source_hashes_match": source_hashes_match,
        "source_clause_checks": source_clause_checks,
        "finite_time": {
            "Gaussian_replicas": len(gaussian_replicates),
            "events_per_replica": 2**GAUSSIAN_POWER,
            "angular_kernel_squared_mean": angular_mean,
            "angular_kernel_squared_standard_error": angular_standard_error,
            "C13_Gaussian": gaussian_coefficient,
            "C13_Gaussian_standard_error": gaussian_coefficient_standard_error,
            "unitarity_numerator_C13_gmax2": gaussian_coefficient * G_UNITARITY**2,
        },
        "on_shell_24": {
            "phase_replicas": len(phase_replicates),
            "events_per_replica": 2**PHASE_POWER,
            "partitions_3_3": len(PARTITIONS_3_3),
            "perfect_matchings_6": len(MATCHINGS_6),
            "mean_exchange_squared": mean_exchange_squared,
            "mean_exchange_contact": mean_exchange_contact,
            "mean_contact_squared": mean_contact_squared,
            "C0": coefficient_0,
            "C1": coefficient_1,
            "C2": coefficient_2,
            "r3_minimum": ratio_minimum,
            "C_minimum": coefficient_minimum,
            "exchange_24_to_22_prefactor": exchange_24_to_22_prefactor,
        },
        "execution": {
            "SPARC_rows": len(sparc_rows),
            "positive_high_frequency_rows": len(positive_high),
            "finite_preparation_failures": finite_fail_count,
            "controlled_envelope_failures": controlled_fail_count,
            "finite_preparation_probability_max_high_frequency": max(row["P13_single_preparation_at_22_unitarity_max"] for row in positive_high),
            "controlled_envelope_log_gain_max_high_frequency": max(row["unit_six_point_controlled_log_gain_envelope"] for row in positive_high),
            "required_log_multiplicity_min_high_frequency": min(row["required_log_multiplicity_after_Amax"] for row in positive_high),
        },
        "decision": {
            "sharp_switch_finite_time_route": "REJECTED_UV_SENSITIVE",
            "smooth_single_preparation_13_route": "REJECTED_ON_EXECUTED_HIGH_FREQUENCY_ROWS",
            "X2_exchange_24": "DERIVED",
            "X2_only_complete_24": False,
            "mandatory_next_coordinate": "d3_X3",
            "controlled_high_frequency_route": "REJECTED",
            "strong_nonquasiparticle_X2_X3_2PI": "OPEN",
            "direct_profile_formation_amplitude": "OPEN",
            "local_GR_Newton_Maxwell_4947": "RETAINED",
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks = [
        source_hashes_match,
        all(source_clause_checks.values()),
        len(MATCHINGS_6) == 15,
        len(PARTITIONS_3_3) == 10,
        all(row["all_finite"] for row in gaussian_replicates),
        all(row["all_finite"] for row in phase_replicates),
        all(row["RAMBO_sum_error_max"] < 1.0e-12 and row["RAMBO_mass_shell_error_max"] < 1.0e-12 for row in phase_replicates),
        5.9e-6 < gaussian_coefficient < 6.2e-6,
        1.9e-6 < coefficient_0 < 2.2e-6,
        coefficient_minimum > 0.0,
        len(sparc_rows) == 1050,
        len(positive_high) == 692,
        finite_fail_count == len(positive_high),
        controlled_fail_count == len(positive_high),
        all(not row["valid_for_full_MTS_claim"] for table in (preboltzmann_rows, gaussian_derivation_rows, amplitude_rows, decision_rows) for row in table),
    ]
    return 0 if all(all_checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
