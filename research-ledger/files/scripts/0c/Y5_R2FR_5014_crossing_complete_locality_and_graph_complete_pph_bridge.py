from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from numba import njit, prange
from scipy.stats import qmc


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5014"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5011 = POST / "scripts" / "Y5_R2FR_5011_coupled_outer_partial_wave_cancellation_test.py"
CHECKPOINT_4988 = POST / "4988-Y5-R2FR-renormalized-scalar-two-particle-cut-and-exact-partial-wave-projection.md"
CHECKPOINT_4990 = POST / "4990-Y5-R2FR-crossing-complete-D1-scheme-separation-and-hh-scope-correction.md"
CHECKPOINT_5012 = POST / "5012-Y5-R2FR-nested-soft-forward-angular-first-projection.md"
CHECKPOINT_5013 = POST / "5013-Y5-R2FR-direct-channel-D1-support-and-three-particle-locality-sum-rule.md"
RESULT_5012 = SOURCE.parent / "5012" / "nested_soft_forward_results.json"
HH_TOWER = SOURCE.parent / "5008" / "hh_wigner_partial_wave_tower.csv"
BERN_SOURCE = SOURCE.parent / "4987" / "sources" / "bern_parra_sawyer" / "smeft2.tex"

PAIR_MAP_CSV = SOURCE / "Luna_pairwise_soft_channel_map.csv"
PAIR_CHECK_CSV = SOURCE / "pairwise_Ward_and_soft_factor_checks.csv"
COUNTEREXAMPLE_CSV = SOURCE / "direct_channel_locality_counterexample.csv"
ENDPOINT_CSV = SOURCE / "graph_complete_matched_endpoint_scan.csv"
SCHEME_CSV = SOURCE / "pph_raw_vs_graph_complete_plus_moments.csv"
SUPERSESSION_CSV = SOURCE / "5013_supersession_matrix.csv"
GATE_CSV = SOURCE / "crossing_complete_bridge_gate.csv"
RESULT_JSON = SOURCE / "crossing_complete_graph_complete_pph_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5014-Y5-R2FR-crossing-complete-locality-and-graph-complete-pph-bridge.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5014_VALIDATION.csv"

MARKER = "MTS_5014_CROSSING_COMPLETE_LOCALITY_GRAPH_COMPLETE_PPH_BRIDGE"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_5011() -> Any:
    specification = importlib.util.spec_from_file_location("mts_checkpoint_5011_for_5014", SCRIPT_5011)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load checkpoint 5011")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


BASE = load_5011()
PAIRING_S = np.asarray([[0, 1], [2, 3]], dtype=np.int64)
PAIRINGS = BASE.PAIRINGS

minkowski = BASE.minkowski
direction = BASE.direction
sequential_three_body = BASE.sequential_three_body
external_momenta = BASE.external_momenta
circular_polarization = BASE.circular_polarization
luna_pair = BASE.luna_pair
invariant_sum = BASE.invariant_sum
vector_soft = BASE.vector_soft
scalar_sets = BASE.scalar_sets
pph_product_raw = BASE.pph_product


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


def source_locks() -> dict[str, bool]:
    required = (
        SCRIPT_5011,
        CHECKPOINT_4988,
        CHECKPOINT_4990,
        CHECKPOINT_5012,
        CHECKPOINT_5013,
        RESULT_5012,
        HH_TOWER,
        BERN_SOURCE,
    )
    bern = BERN_SOURCE.read_text(encoding="utf-8", errors="ignore")
    checkpoint_4990 = CHECKPOINT_4990.read_text(encoding="utf-8")
    checkpoint_5013 = CHECKPOINT_5013.read_text(encoding="utf-8")
    return {
        "required_paths": all(path.exists() for path in required),
        "Bern_real_master": "\\text{Re}(\\M) \\text{Re}(F_i)" in bern,
        "Bern_three_particle_tree_product": "A^{(0)}(1,\\cdots,k,-\\ell_1^{-h_1},-\\ell_2^{-h_2},-\\ell_3^{-h_3})" in bern,
        "4990_crossing_complete_warning": "crossing object on both sides" in checkpoint_4990,
        "5013_direct_sum_rule_present": "D_hhh,J + D_phiphih,J = -D_hh,J" in checkpoint_5013,
        "5012_exact_matched_endpoint": bool(read_json(RESULT_5012)["exact_matched_soft_endpoint"]),
    }


def exact_pair_map() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    s_value, t_value, u_value = sp.symbols("s t u", nonzero=True, real=True)
    c_s = -(t_value - u_value) ** 2 / (4 * s_value)
    c_t = -(s_value - u_value) ** 2 / (4 * t_value)
    c_u = -(s_value - t_value) ** 2 / (4 * u_value)
    c_4 = t_value * u_value / s_value + s_value * u_value / t_value + s_value * t_value / u_value
    c_sing = -s_value**2 / t_value - s_value**2 / u_value
    relation = {u_value: -s_value - t_value}
    checks = {
        "pair_sum": sp.factor((c_s + c_t + c_u - c_4).subs(relation)),
        "tu_block": sp.factor((c_t + c_u - c_sing + sp.Rational(7, 4) * s_value).subs(relation)),
        "s_block": sp.factor((c_s + (t_value - u_value) ** 2 / (4 * s_value)).subs(relation)),
    }
    rows = [
        {
            "pairing": "((0,1),(2,3))",
            "channel": "s",
            "canonical_soft_coefficient": str(c_s),
            "role_in_4988_match": "retained graph block",
            "status": "EXACT",
        },
        {
            "pairing": "((0,2),(1,3))",
            "channel": "t",
            "canonical_soft_coefficient": str(c_t),
            "role_in_4988_match": "removed with hard t/u exchange packet",
            "status": "EXACT",
        },
        {
            "pairing": "((0,3),(1,2))",
            "channel": "u",
            "canonical_soft_coefficient": str(c_u),
            "role_in_4988_match": "removed with hard t/u exchange packet",
            "status": "EXACT",
        },
        {
            "pairing": "sum",
            "channel": "s+t+u",
            "canonical_soft_coefficient": str(c_4),
            "role_in_4988_match": "C4=C4_sing-s(7+z^2)/4",
            "status": "EXACT",
        },
    ]
    return rows, {
        "checks": {key: str(value) for key, value in checks.items()},
        "all_exact": all(value == 0 for value in checks.values()),
        "singular_completion": "M_t+M_u+(7s/4)S_vec",
        "regular_five_point": "M_s-(7s/4)S_vec",
        "soft_regular_tree": "-s(7+z^2)/4",
    }


def pairwise_numeric_checks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    maximum_ward = 0.0
    maximum_soft = 0.0
    cases = (
        (0.27, 0.37, 0.21, 0.69, 0.43),
        (-0.41, 0.18, 0.77, 0.52, 0.31),
    )
    for case_index, (cosine, soft_u, soft_phi, decay_u, decay_phi) in enumerate(cases, start=1):
        soft_direction = direction(soft_u, soft_phi)
        decay_direction = direction(decay_u, decay_phi)
        for soft_energy in (0.4, 0.1, 0.01):
            internal = sequential_three_body(soft_energy, soft_direction, decay_direction)
            left, _ = scalar_sets(internal, cosine)
            graviton = internal[2]
            polarization = circular_polarization(graviton, 1)
            shifted = polarization + (0.37 - 0.22j) * graviton
            for pair_index in range(3):
                amplitude = -luna_pair(left, graviton, polarization, BASE.PAIRINGS[pair_index]) / 8.0
                shifted_amplitude = -luna_pair(left, graviton, shifted, BASE.PAIRINGS[pair_index]) / 8.0
                ward = abs(amplitude - shifted_amplitude) / max(abs(amplitude), 1.0e-30)
                maximum_ward = max(maximum_ward, ward)
                rows.append(
                    {
                        "check_id": f"WARD5014_c{case_index}_x{soft_energy:g}_p{pair_index}",
                        "check_type": "finite_energy_pair_block_Ward",
                        "soft_energy_x": soft_energy,
                        "pair_index": pair_index,
                        "relative_residual": ward,
                        "status": "PASS" if ward < 2.0e-11 else "FAIL",
                    }
                )

        soft_energy = 1.0e-6
        internal = sequential_three_body(soft_energy, soft_direction, decay_direction)
        left, _ = scalar_sets(internal, cosine)
        graviton = internal[2]
        polarization = circular_polarization(graviton, 1)
        soft_factor = vector_soft(left, graviton, polarization)
        s_value = invariant_sum(left[0], left[1])
        t_value = invariant_sum(left[0], left[2])
        u_value = invariant_sum(left[0], left[3])
        coefficients = (
            -(t_value - u_value) ** 2 / (4.0 * s_value),
            -(s_value - u_value) ** 2 / (4.0 * t_value),
            -(s_value - t_value) ** 2 / (4.0 * u_value),
        )
        for pair_index, coefficient in enumerate(coefficients):
            amplitude = -luna_pair(left, graviton, polarization, BASE.PAIRINGS[pair_index]) / 8.0
            ratio = amplitude / (soft_factor * coefficient)
            residual = abs(ratio - 1.0)
            maximum_soft = max(maximum_soft, residual)
            rows.append(
                {
                    "check_id": f"SOFT5014_c{case_index}_p{pair_index}",
                    "check_type": "pairwise_soft_coefficient",
                    "soft_energy_x": soft_energy,
                    "pair_index": pair_index,
                    "relative_residual": residual,
                    "ratio_real": ratio.real,
                    "ratio_imaginary": ratio.imag,
                    "status": "PASS" if residual < 3.0e-5 else "FAIL",
                }
            )
        regular = -luna_pair(left, graviton, polarization, PAIRING_S) / 8.0 - 7.0 * s_value * soft_factor / 4.0
        hard_cosine = (t_value - u_value) / s_value
        target = soft_factor * (-s_value * (7.0 + hard_cosine * hard_cosine) / 4.0)
        residual = abs(regular / target - 1.0)
        maximum_soft = max(maximum_soft, residual)
        rows.append(
            {
                "check_id": f"SOFT5014_c{case_index}_regular",
                "check_type": "graph_complete_regular_soft_limit",
                "soft_energy_x": soft_energy,
                "pair_index": "s-minus-local-completion",
                "relative_residual": residual,
                "status": "PASS" if residual < 3.0e-5 else "FAIL",
            }
        )
    return rows, {
        "maximum_Ward_relative_residual": maximum_ward,
        "maximum_soft_relative_residual": maximum_soft,
        "all_pass": all(row["status"] == "PASS" for row in rows),
    }


def locality_counterexample(spins: tuple[int, ...]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    z = sp.symbols("z", real=True)
    s_value, t_value = sp.symbols("s t", nonzero=True, real=True)
    u_value = -s_value - t_value
    denominator = s_value**4 + t_value**4 + u_value**4
    weights = (s_value**4 / denominator, t_value**4 / denominator, u_value**4 / denominator)
    crossing_residual = sp.factor(sum(weights) * s_value * t_value * u_value - s_value * t_value * u_value)
    direct_function = 2 * (1 - z**2) / (z**2 + 3) ** 2
    rows: list[dict[str, Any]] = []
    high_spin_nonzero = True
    for spin in spins:
        moment = sp.factor(
            sp.integrate(sp.legendre(spin, z) * direct_function, (z, -1, 1)) / 2
        )
        if spin >= 4:
            high_spin_nonzero = high_spin_nonzero and moment != 0
        rows.append(
            {
                "mode_id": f"COUNTER5014_J{spin:03d}",
                "spin_J": spin,
                "direct_function": str(direct_function),
                "direct_partial_wave_exact": str(moment),
                "direct_partial_wave_numeric": float(sp.N(moment, 18)),
                "cyclic_sum": "stu",
                "cyclic_residual": str(crossing_residual),
                "status": "NONZERO_DIRECT_HIGH_SPIN_WITH_EXACT_LOCAL_CYCLIC_SUM" if spin >= 4 else "LOCAL_LOW_MODE",
            }
        )
    return rows, {
        "weight_identity": "w_s+w_t+w_u=1, w_q=q^4/(s^4+t^4+u^4)",
        "direct_reduced_function": str(direct_function),
        "crossing_residual": str(crossing_residual),
        "high_spin_nonzero": high_spin_nonzero,
        "per_J_direct_locality_inference_valid": False,
    }


@njit
def regular_five_amplitude(
    scalars: np.ndarray, graviton: np.ndarray, polarization: np.ndarray
) -> complex:
    s_value = invariant_sum(scalars[0], scalars[1])
    s_pair = -luna_pair(scalars, graviton, polarization, PAIRING_S) / 8.0
    return s_pair - 7.0 * s_value * vector_soft(scalars, graviton, polarization) / 4.0


@njit
def pph_product_regular(internal: np.ndarray, scattering_cosine: float) -> complex:
    left_scalars, right_scalars = scalar_sets(internal, scattering_cosine)
    graviton = internal[2]
    result = 0.0j
    for helicity in (-1, 1):
        polarization = circular_polarization(graviton, helicity)
        left = regular_five_amplitude(left_scalars, graviton, polarization)
        right = regular_five_amplitude(right_scalars, -graviton, np.conjugate(polarization))
        result += left * right
    return result / 2.0


@njit
def pph_products_both(
    internal: np.ndarray, scattering_cosine: float
) -> tuple[complex, complex]:
    left_scalars, right_scalars = scalar_sets(internal, scattering_cosine)
    graviton = internal[2]
    raw_result = 0.0j
    regular_result = 0.0j
    left_s = invariant_sum(left_scalars[0], left_scalars[1])
    right_s = invariant_sum(right_scalars[0], right_scalars[1])
    for helicity in (-1, 1):
        polarization = circular_polarization(graviton, helicity)
        right_polarization = np.conjugate(polarization)
        left_full = 0.0j
        right_full = 0.0j
        left_s_pair = 0.0j
        right_s_pair = 0.0j
        for pair_index in range(3):
            left_pair = -luna_pair(
                left_scalars, graviton, polarization, PAIRINGS[pair_index]
            ) / 8.0
            right_pair = -luna_pair(
                right_scalars,
                -graviton,
                right_polarization,
                PAIRINGS[pair_index],
            ) / 8.0
            left_full += left_pair
            right_full += right_pair
            if pair_index == 0:
                left_s_pair = left_pair
                right_s_pair = right_pair
        left_regular = left_s_pair - 7.0 * left_s * vector_soft(
            left_scalars, graviton, polarization
        ) / 4.0
        right_regular = right_s_pair - 7.0 * right_s * vector_soft(
            right_scalars, -graviton, right_polarization
        ) / 4.0
        raw_result += left_full * right_full
        regular_result += left_regular * right_regular
    return raw_result / 2.0, regular_result / 2.0


@njit
def axes_for_cosine(scattering_cosine: float) -> np.ndarray:
    transverse = math.sqrt(max(0.0, 1.0 - scattering_cosine * scattering_cosine))
    axes = np.empty((4, 3), dtype=np.float64)
    axes[0] = np.array([0.0, 0.0, 1.0])
    axes[1] = np.array([0.0, 0.0, -1.0])
    axes[2] = np.array([transverse, 0.0, scattering_cosine])
    axes[3] = -axes[2]
    return axes


@njit
def endpoint_mixture(unit: float, power: float) -> tuple[float, float]:
    if unit < 0.5:
        radius = max(2.0 * unit, 1.0e-15)
        value = radius**power
    else:
        radius = max(2.0 * unit - 1.0, 1.0e-15)
        value = 1.0 - radius**power
    clipped = min(max(value, 1.0e-15), 1.0 - 1.0e-15)
    exponent = 1.0 / power - 1.0
    density = (clipped**exponent + (1.0 - clipped) ** exponent) / (2.0 * power)
    return clipped, density


@njit
def sphere_mixture(
    unit_channel: float, unit_phi: float, axes: np.ndarray, power: float
) -> tuple[np.ndarray, float]:
    scaled = min(max(4.0 * unit_channel, 0.0), 4.0 - 1.0e-14)
    channel = int(scaled)
    radius = max(scaled - channel, 1.0e-15)
    y_value = radius**power
    cosine = 1.0 - 2.0 * y_value
    sine = math.sqrt(max(0.0, 1.0 - cosine * cosine))
    axis = axes[channel]
    reference = np.array([0.0, 0.0, 1.0])
    if abs(axis[2]) > 0.9:
        reference = np.array([0.0, 1.0, 0.0])
    first = np.cross(reference, axis)
    first /= math.sqrt(first @ first)
    second = np.cross(axis, first)
    azimuth = 2.0 * math.pi * unit_phi
    result = cosine * axis + sine * (
        math.cos(azimuth) * first + math.sin(azimuth) * second
    )
    exponent = 1.0 / power - 1.0
    density = 0.0
    for index in range(4):
        separation = max((1.0 - axes[index] @ result) / 2.0, 1.0e-15)
        density += separation**exponent
    density /= 4.0 * power
    return result, density


@njit(parallel=True)
def importance_geometry(points: np.ndarray, mixture_power: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    count = points.shape[0]
    cosines = np.empty(count, dtype=np.float64)
    soft_directions = np.empty((count, 3), dtype=np.float64)
    decay_directions = np.empty((count, 3), dtype=np.float64)
    inverse_densities = np.empty(count, dtype=np.float64)
    for index in prange(count):
        angle_x, angle_density = endpoint_mixture(points[index, 0], mixture_power)
        cosine = 1.0 - 2.0 * angle_x
        axes = axes_for_cosine(cosine)
        soft_direction, soft_density = sphere_mixture(
            points[index, 1], points[index, 2], axes, mixture_power
        )
        decay_direction, decay_density = sphere_mixture(
            points[index, 3], points[index, 4], axes, mixture_power
        )
        cosines[index] = cosine
        soft_directions[index] = soft_direction
        decay_directions[index] = decay_direction
        inverse_densities[index] = 1.0 / (angle_density * soft_density * decay_density)
    return cosines, soft_directions, decay_directions, inverse_densities


@njit(parallel=True)
def direct_g_many_batch(
    cosines: np.ndarray,
    soft_directions: np.ndarray,
    decay_directions: np.ndarray,
    inverse_densities: np.ndarray,
    soft_energies: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    sample_count = len(cosines)
    energy_count = len(soft_energies)
    raw_values = np.empty((energy_count, sample_count), dtype=np.float64)
    regular_values = np.empty((energy_count, sample_count), dtype=np.float64)
    for flat_index in prange(energy_count * sample_count):
        energy_index = flat_index // sample_count
        index = flat_index - energy_index * sample_count
        soft_energy = soft_energies[energy_index]
        internal = sequential_three_body(
            soft_energy, soft_directions[index], decay_directions[index]
        )
        raw_product, regular_product = pph_products_both(internal, cosines[index])
        common = soft_energy * soft_energy * inverse_densities[index] / 16.0
        raw_values[energy_index, index] = float((common * raw_product).real)
        regular_values[energy_index, index] = float((common * regular_product).real)
    return raw_values, regular_values


def legendre_values(cosines: np.ndarray, spins: tuple[int, ...]) -> dict[int, np.ndarray]:
    values: dict[int, np.ndarray] = {}
    for spin in spins:
        coefficients = np.zeros(spin + 1)
        coefficients[-1] = 1.0
        values[spin] = np.polynomial.legendre.legval(cosines, coefficients)
    return values


def aggregate(values: list[float]) -> tuple[float, float]:
    array = np.asarray(values, dtype=float)
    return float(np.mean(array)), float(np.std(array, ddof=1) / math.sqrt(len(array)))


def numerical_plus_integrals(
    power: int,
    seeds: tuple[int, ...],
    spins: tuple[int, ...],
    gauss_order: int,
    mixture_power: float,
    endpoint_energies: tuple[float, ...],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    matched_data = read_json(RESULT_5012)["matched_soft_endpoint"]["modes"]
    matched_endpoints = {spin: float(matched_data[str(spin)]["numeric"]) for spin in spins}
    raw_fit_energies = np.asarray((0.005, 0.002, 0.001, 0.0005, 0.0002), dtype=float)
    raw_design = np.column_stack(
        (np.ones(len(raw_fit_energies)), raw_fit_energies * np.log(raw_fit_energies), raw_fit_energies)
    )
    nodes, quadrature_weights = np.polynomial.legendre.leggauss(gauss_order)
    energy_nodes = (nodes + 1.0) / 2.0
    quadrature_weights = quadrature_weights / 2.0

    endpoint_rows: list[dict[str, Any]] = []
    endpoint_values: dict[tuple[float, int], list[float]] = {
        (energy, spin): [] for energy in endpoint_energies for spin in spins
    }
    raw_endpoint_by_spin: dict[int, list[float]] = {spin: [] for spin in spins}
    integrals: dict[tuple[str, int], list[float]] = {
        (scheme, spin): [] for scheme in ("raw_angular_first", "graph_complete_4988") for spin in spins
    }

    for seed in seeds:
        points = qmc.Sobol(d=5, scramble=True, seed=seed).random_base2(power)
        cosines, soft_directions, decay_directions, inverse_densities = importance_geometry(
            points, mixture_power
        )
        polynomials = legendre_values(cosines, spins)

        all_energies = np.concatenate(
            (raw_fit_energies, energy_nodes, np.asarray(endpoint_energies, dtype=float))
        )
        raw_all, matched_all = direct_g_many_batch(
            cosines,
            soft_directions,
            decay_directions,
            inverse_densities,
            all_energies,
        )
        raw_slice = slice(0, len(raw_fit_energies))
        gauss_slice = slice(
            len(raw_fit_energies), len(raw_fit_energies) + len(energy_nodes)
        )
        endpoint_start = len(raw_fit_energies) + len(energy_nodes)

        raw_small_curves: dict[int, list[float]] = {spin: [] for spin in spins}
        for energy_index, _ in enumerate(raw_fit_energies):
            values = raw_all[raw_slice][energy_index]
            for spin in spins:
                raw_small_curves[spin].append(float(np.mean(polynomials[spin] * values)))
        raw_endpoints: dict[int, float] = {}
        for spin in spins:
            coefficients = np.linalg.lstsq(
                raw_design, np.asarray(raw_small_curves[spin]), rcond=None
            )[0]
            raw_endpoints[spin] = float(coefficients[0])
            raw_endpoint_by_spin[spin].append(float(coefficients[0]))

        matched_curves: dict[int, list[float]] = {spin: [] for spin in spins}
        raw_curves: dict[int, list[float]] = {spin: [] for spin in spins}
        for energy_index, _ in enumerate(energy_nodes):
            matched_values = matched_all[gauss_slice][energy_index]
            raw_values = raw_all[gauss_slice][energy_index]
            for spin in spins:
                matched_curves[spin].append(float(np.mean(polynomials[spin] * matched_values)))
                raw_curves[spin].append(float(np.mean(polynomials[spin] * raw_values)))
        for spin in spins:
            matched_integral = float(
                np.sum(
                    quadrature_weights
                    * (np.asarray(matched_curves[spin]) - matched_endpoints[spin])
                    / energy_nodes
                )
            )
            raw_integral = float(
                np.sum(
                    quadrature_weights
                    * (np.asarray(raw_curves[spin]) - raw_endpoints[spin])
                    / energy_nodes
                )
            )
            integrals[("graph_complete_4988", spin)].append(matched_integral)
            integrals[("raw_angular_first", spin)].append(raw_integral)

        for endpoint_index, energy in enumerate(endpoint_energies):
            values = matched_all[endpoint_start + endpoint_index]
            for spin in spins:
                estimate = float(np.mean(polynomials[spin] * values))
                endpoint_values[(energy, spin)].append(estimate)
                endpoint_rows.append(
                    {
                        "run_id": f"END5014_x{energy:g}_seed{seed}_J{spin}",
                        "soft_energy_x": energy,
                        "seed": seed,
                        "spin_J": spin,
                        "G_J_x": estimate,
                        "exact_G_J_0": matched_endpoints[spin],
                        "status": "GRAPH_COMPLETE_FIXED_X_RUN",
                    }
                )

    for energy in endpoint_energies:
        for spin in spins:
            mean, error = aggregate(endpoint_values[(energy, spin)])
            endpoint = matched_endpoints[spin]
            endpoint_rows.append(
                {
                    "run_id": f"END5014_x{energy:g}_aggregate_J{spin}",
                    "soft_energy_x": energy,
                    "seed": "aggregate",
                    "spin_J": spin,
                    "G_J_x": mean,
                    "RQMC_standard_error": error,
                    "exact_G_J_0": endpoint,
                    "endpoint_difference": mean - endpoint,
                    "status": "APPROACHES_EXACT_5012_ENDPOINT",
                }
            )

    scheme_rows: list[dict[str, Any]] = []
    summaries: dict[str, dict[str, Any]] = {}
    for scheme in ("raw_angular_first", "graph_complete_4988"):
        summaries[scheme] = {}
        for spin in spins:
            integral_mean, integral_error = aggregate(integrals[(scheme, spin)])
            reduced_mean = -2.0 * integral_mean / math.pi
            reduced_error = 2.0 * integral_error / math.pi
            if scheme == "raw_angular_first":
                endpoint_mean, endpoint_error = aggregate(raw_endpoint_by_spin[spin])
                endpoint_exact = "fitted_angular_first_distribution"
            else:
                endpoint_mean = matched_endpoints[spin]
                endpoint_error = 0.0
                endpoint_exact = matched_data[str(spin)]["exact"]
            scheme_rows.append(
                {
                    "scheme": scheme,
                    "spin_J": spin,
                    "endpoint_exact_or_fit": endpoint_exact,
                    "endpoint_numeric": endpoint_mean,
                    "endpoint_RQMC_error": endpoint_error,
                    "plus_integral_I_J": integral_mean,
                    "plus_integral_RQMC_error": integral_error,
                    "D_pph_J_over_G3": reduced_mean,
                    "D_pph_J_RQMC_error": reduced_error,
                    "eligible_for_4988_common_scheme": scheme == "graph_complete_4988",
                    "eligible_as_per_J_locality_target": False,
                    "status": "SELECTED_GRAPH_COMPLETE_COMMON_SCHEME" if scheme == "graph_complete_4988" else "RAW_SCHEME_DIAGNOSTIC_ONLY",
                }
            )
            summaries[scheme][str(spin)] = {
                "endpoint": endpoint_mean,
                "endpoint_error": endpoint_error,
                "I_J": integral_mean,
                "I_J_error": integral_error,
                "D_over_G3": reduced_mean,
                "D_error": reduced_error,
            }
    return endpoint_rows, scheme_rows, {
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "gauss_order": gauss_order,
        "mixture_power": mixture_power,
        "summaries": summaries,
    }


def supersession_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "5013_direct_D1_object",
            "former_statement": "only the ln(-s) coefficient can enter",
            "5014_decision": "REJECTED_FOR_REAL_TWO_LOOP_MASTER",
            "reason": "Bern equation (2.22) uses the full crossing-complete Re(M)Re(F) object",
            "replacement": "insert D1 ReF1 only after constructing the same full real crossing object",
        },
        {
            "claim_id": "5013_D1_high_spin",
            "former_statement": "Pi_J Disc_s(D1F1)=0 for J>=4",
            "5014_decision": "TRUE_BUT_NOT_THE_RELEVANT_MASTER_OBJECT",
            "reason": "the direct discontinuity and full real kernel are different channel objects",
            "replacement": "retain the nonzero full-real F1 high-spin moments derived in 5013",
        },
        {
            "claim_id": "5013_per_J_sum_rule",
            "former_statement": "D_3,J=-D_hh,J for every even J>=4",
            "5014_decision": "REJECTED",
            "reason": "crossing mixes the complete infinite direct-channel tower before locality is tested",
            "replacement": "test locality on sum_cyclic q^3 D((p-r)/q), not mode by mode in one channel",
        },
        {
            "claim_id": "5013_two_number_reduction",
            "former_statement": "only J=0 and J=2 three-particle numbers remain",
            "5014_decision": "REJECTED",
            "reason": "it depended entirely on the invalid per-J direct-channel sum rule",
            "replacement": "retain the finite direct function or a controlled analytic continuation/crossing kernel",
        },
        {
            "claim_id": "5013_J4_validation_target",
            "former_statement": "three-particle J4 must equal 1.32106223583",
            "5014_decision": "REJECTED_AS_A_VALIDATION_GATE",
            "reason": "a local cyclic sum can have nonzero direct J>=4 moments",
            "replacement": "use graph-complete scheme matching and crossing-complete locality as the validation gates",
        },
    ]


def gate_rows(
    locks: dict[str, bool],
    pair_map: dict[str, Any],
    pair_checks: dict[str, Any],
    counterexample: dict[str, Any],
    numerical: dict[str, Any],
) -> list[dict[str, Any]]:
    finite_numerics = all(
        math.isfinite(mode["D_over_G3"])
        for scheme in numerical["summaries"].values()
        for mode in scheme.values()
    )
    closed = {
        "primary_source_lock": all(locks.values()),
        "exact_Luna_pair_soft_map": pair_map["all_exact"],
        "pair_blocks_individually_Ward_safe": pair_checks["maximum_Ward_relative_residual"] < 2.0e-11,
        "pairwise_soft_factorization": pair_checks["maximum_soft_relative_residual"] < 3.0e-5,
        "graph_complete_4988_five_point_match": pair_checks["all_pass"],
        "direct_per_J_locality_counterexample": counterexample["crossing_residual"] == "0" and counterexample["high_spin_nonzero"],
        "5013_invalid_sum_rule_superseded": True,
        "raw_and_matched_plus_integrals_executable": finite_numerics,
    }
    open_gates = {
        "crossing_complete_pph_continuation": "the selected direct function must be continued into the crossed t/u physical sheets",
        "graph_complete_hhh_plus": "the hhh finite-energy plus integral remains to be placed in the same common scheme",
        "combined_crossing_locality": "must be tested only after hh, hhh, and pph are combined as full crossing functions",
        "numeric_full_K_mu_K_ang": "the crossing-complete coupled outer cut is not yet projected",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for name, passed in closed.items():
        rows.append(
            {
                "gate": name,
                "passed": bool(passed),
                "evidence": "exact/source-locked derivation or multi-seed RQMC",
                "status": "PASS" if passed else "FAIL",
            }
        )
    for name, evidence in open_gates.items():
        rows.append(
            {
                "gate": name,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
            }
        )
    return rows


def validation_rows(
    locks: dict[str, bool],
    pair_map: dict[str, Any],
    pair_checks: dict[str, Any],
    counterexample: dict[str, Any],
    scheme_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks = [
        ("source_locks", all(locks.values()), str(locks)),
        ("pair_map_exact", pair_map["all_exact"], str(pair_map["checks"])),
        ("pair_checks", pair_checks["all_pass"], str(pair_checks)),
        ("locality_counterexample", counterexample["crossing_residual"] == "0" and counterexample["high_spin_nonzero"], str(counterexample)),
        ("scheme_rows_finite", all(math.isfinite(float(row["D_pph_J_over_G3"])) for row in scheme_rows), f"rows={len(scheme_rows)}"),
        ("matched_scheme_selected", all(row["eligible_for_4988_common_scheme"] == (row["scheme"] == "graph_complete_4988") for row in scheme_rows), "raw excluded; graph-complete selected"),
        ("no_per_J_target", all(row["eligible_as_per_J_locality_target"] is False for row in scheme_rows), "all direct modes are non-target diagnostics"),
        ("closed_gates_pass", all(row["passed"] for row in gates if row["status"] != "OPEN_NONCLAIM"), "all closed gates"),
        ("formalization_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)),
    ]
    return [
        {
            "check_id": f"VALID5014_{index:02d}_{name}",
            "passed": bool(passed),
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str]) -> None:
    lines = [
        "# 5014 crossing-complete bridge provenance",
        "",
        "This checkpoint corrects a channel-object error and evaluates the graph-complete `phi phi h` plus integral. It is private and does not establish local GR or full MTS.",
        "",
        "## Sources",
        "",
    ]
    for path, checksum in source_hashes.items():
        lines.append(f"- `{path}` — SHA-256 `{checksum}`")
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "The exact claims are the pairwise Luna soft map, the graph-complete 4988 subtraction, and the counterexample to direct-channel mode-by-mode locality. Numerical `pph` values are multi-seed RQMC results in the declared schemes. The crossing continuation, coupled outer cut, local GR, and full MTS remain open.",
        ]
    )
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_document(result: dict[str, Any], scheme_rows: list[dict[str, Any]]) -> None:
    selected = {
        int(row["spin_J"]): row
        for row in scheme_rows
        if row["scheme"] == "graph_complete_4988"
    }
    raw = {
        int(row["spin_J"]): row
        for row in scheme_rows
        if row["scheme"] == "raw_angular_first"
    }
    table = [
        "| J | raw angular-first D/G^3 | graph-complete 4988 D/G^3 |",
        "|---:|---:|---:|",
    ]
    for spin in sorted(selected):
        table.append(
            f"| {spin} | {raw[spin]['D_pph_J_over_G3']:.9g} +/- {raw[spin]['D_pph_J_RQMC_error']:.2g} | "
            f"{selected[spin]['D_pph_J_over_G3']:.9g} +/- {selected[spin]['D_pph_J_RQMC_error']:.2g} |"
        )
    DOCUMENT.write_text(
        f"""# 5014 — crossing-complete locality and graph-complete pph bridge

## Result

The `J=4` target introduced in checkpoint 5013 is not a legal locality test. Bern's sourced real two-loop equation contains the full crossing object `[Re(M) Re(F)]^(2)`, whereas 5013 imposed locality mode by mode on one direct-channel discontinuity. Crossing acts on the complete infinite tower before locality is assessed.

An exact counterexample makes this decisive. Define

```text
w_q=q^4/(s^4+t^4+u^4),
F_q=w_q stu,
d_s(z)=F_s/s^3=2(1-z^2)/(z^2+3)^2.
```

Every even direct partial wave of `d_s`, including `J>=4`, is nonzero, but `F_s+F_t+F_u=stu` exactly. Therefore neither `D_3,J=-D_hh,J` nor the claimed reduction of the three-particle problem to only `J=0,2` follows from locality. Checkpoint 5013 is superseded on those statements; its exact full-real `F1` moments remain useful.

## Graph-complete 4988 match

The three independently Ward-safe Luna Bose pairings have exact soft coefficients

```text
C_s=-(t-u)^2/(4s),
C_t=-(s-u)^2/(4t),
C_u=-(s-t)^2/(4u),
C_s+C_t+C_u=C4.
```

On `s+t+u=0`,

```text
C_t+C_u=-s^2/t-s^2/u-7s/4.
```

Hence the hard exchange packet removed in checkpoint 4988 has the unique graph-complete five-point lift

```text
M5_sing=M_t+M_u+(7s/4)S_vec,
M5_reg=M_s-(7s/4)S_vec.
```

No coefficient was fitted. Every pair block and `S_vec` is separately Ward safe, and the measured soft-factor residual is `{result['pair_checks']['maximum_soft_relative_residual']:.3e}`.

## Integrated direct-channel result

The robust sampler uses two-endpoint importance sampling for the external angle and four-axis mixtures around both incoming and outgoing hard directions for each internal sphere. It integrates the angular-first plus distribution with `{result['numerics']['gauss_order']}`-point Gauss-Legendre quadrature and `{result['numerics']['samples_per_seed']}` Sobol geometries per seed.

{chr(10).join(table)}

The raw column retains the hard `t/u` exchange packet and is a scheme diagnostic only. The graph-complete column is the direct `phi phi h` contribution matched to checkpoint 4988. Neither column is compared to the rejected 5013 `J=4` target.

## Status

- Pairwise Luna soft-channel map and Ward identities: **derived and checked**.
- Graph-complete finite-`x` 4988 subtraction: **derived, not fitted**.
- Angular-first raw and matched plus integrals: **executed with multi-seed RQMC**.
- Checkpoint 5013 direct per-`J` locality rule: **superseded**.
- Crossing continuation of the direct function and graph-complete `hhh` integral: **next active calculation**.
- Coupled crossing-local projection, numeric `K_mu/K_ang`, exact local GR, and full MTS: **not claimed**.

Next: analytically continue the graph-complete direct kernels into the crossed `t/u` sheets (or derive the equivalent crossing kernel), add the `hhh` sector, and test locality only on the complete cyclic object.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=15)
    parser.add_argument("--seeds", default="1103,2207,3301,4409")
    parser.add_argument("--spins", default="0,2,4,6,8")
    parser.add_argument("--gauss-order", type=int, default=20)
    parser.add_argument("--mixture-power", type=float, default=2.0)
    parser.add_argument("--endpoint-energies", default="0.03,0.01,0.003")
    arguments = parser.parse_args()
    if arguments.power < 10 or arguments.gauss_order < 8:
        raise ValueError("power >=10 and gauss-order >=8 are required")
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    spins = tuple(int(value) for value in arguments.spins.split(","))
    endpoint_energies = tuple(float(value) for value in arguments.endpoint_energies.split(","))
    if len(seeds) < 3 or any(spin < 0 or spin % 2 for spin in spins):
        raise ValueError("at least three seeds and nonnegative even spins are required")

    started = time.perf_counter()
    locks = source_locks()
    pair_rows, pair_map = exact_pair_map()
    pair_check_rows, pair_checks = pairwise_numeric_checks()
    counter_rows, counterexample = locality_counterexample(spins)
    endpoint_rows, scheme_rows, numerical = numerical_plus_integrals(
        arguments.power,
        seeds,
        spins,
        arguments.gauss_order,
        arguments.mixture_power,
        endpoint_energies,
    )
    supersession = supersession_rows()
    gates = gate_rows(locks, pair_map, pair_checks, counterexample, numerical)
    validation = validation_rows(
        locks, pair_map, pair_checks, counterexample, scheme_rows, gates
    )

    for path, rows in (
        (PAIR_MAP_CSV, pair_rows),
        (PAIR_CHECK_CSV, pair_check_rows),
        (COUNTEREXAMPLE_CSV, counter_rows),
        (ENDPOINT_CSV, endpoint_rows),
        (SCHEME_CSV, scheme_rows),
        (SUPERSESSION_CSV, supersession),
        (GATE_CSV, gates),
        (VALIDATION_CSV, validation),
    ):
        write_csv(path, tagged(rows))

    source_paths = (
        BERN_SOURCE,
        CHECKPOINT_4988,
        CHECKPOINT_4990,
        CHECKPOINT_5012,
        CHECKPOINT_5013,
        SCRIPT_5011,
        RESULT_5012,
        HH_TOWER,
    )
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_locks": locks,
        "pair_map": pair_map,
        "pair_checks": pair_checks,
        "locality_counterexample": counterexample,
        "numerics": numerical,
        "5013_per_J_locality_rule_valid": False,
        "selected_pph_scheme": "graph_complete_4988",
        "crossing_complete_pph": False,
        "graph_complete_hhh": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "validation_all_pass": all(row["passed"] for row in validation),
        "formalization_workbench_digest": tree_digest(FORMAL),
        "source_hashes": source_hashes,
        "elapsed_seconds": time.perf_counter() - started,
    }
    SOURCE.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes)
    write_document(result, scheme_rows)
    if not result["validation_all_pass"]:
        failed = [row["check_id"] for row in validation if not row["passed"]]
        raise RuntimeError(f"5014 validation failed: {failed}")
    print(json.dumps({
        "status": "PASS",
        "marker": MARKER,
        "selected_pph": numerical["summaries"]["graph_complete_4988"],
        "raw_diagnostic": numerical["summaries"]["raw_angular_first"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
