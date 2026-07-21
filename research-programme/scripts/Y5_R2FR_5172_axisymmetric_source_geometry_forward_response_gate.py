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

sys.dont_write_bytecode = True

import numpy as np
from scipy import fft
from scipy.interpolate import PchipInterpolator


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5169_pair_consistent_transport_forward_response_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5169-Y5-R2FR-pair-consistent-capacity-bounded-transport-forward-response-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5169"
    / "pair_consistent_transport_forward_response_results.json"
)
PREVIOUS_SCORE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5169"
    / "transported_radial_source_forward_scores.csv"
)
PREVIOUS_PROFILE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5169"
    / "transported_radial_source_forward_profiles.csv"
)
PREVIOUS_VALIDATION = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5169_VALIDATION.csv"
)
VISIBLE_PROFILE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5163"
    / "visible_baryon_source_profile.csv"
)
OUT = POST / "source-intake" / "functional_rg" / "5172"
CACHE = OUT / "evolution-cache"
CONTRACT_CSV = OUT / "source_geometry_contract.csv"
FORCE_AUDIT_CSV = OUT / "axisymmetric_source_force_audit.csv"
SCORE_CSV = OUT / "axisymmetric_geometry_forward_scores.csv"
CONTROL_CSV = OUT / "geometry_numerical_controls.csv"
PROFILE_CSV = OUT / "axisymmetric_vs_spherical_profiles.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "axisymmetric_source_geometry_forward_response_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5172_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5172-Y5-R2FR-source-backed-axisymmetric-baryon-geometry-forward-response-gate.md"
)

MARKER = "MTS_5172_AXISYMMETRIC_SOURCE_GEOMETRY_FORWARD_RESPONSE_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
SELECTED_BRANCH = ("ISOBARIC", 0.3)
RADIAL_BINS = 26
COST_POWER = 1
PRIMARY_STEPS = 64
REFINED_STEPS = 128
TRANSFORM_POINTS = 4096
TRANSFORM_MIN_KPC = 1.0e-4
TRANSFORM_MAX_KPC = 1.0e5
VERTICAL_POINTS = 192
VERTICAL_MAX_KPC = 5.0e3
PRIMARY_AXIS = np.asarray([0.0, 0.0, 1.0])
ORIENTATION_AXES = {
    "AXIS_Z_PRIMARY": PRIMARY_AXIS,
    "AXIS_X_CONTROL": np.asarray([1.0, 0.0, 0.0]),
    "AXIS_Y_CONTROL": np.asarray([0.0, 1.0, 0.0]),
}


specification = importlib.util.spec_from_file_location(
    "mts_checkpoint_5169_for_5172", PREVIOUS_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {PREVIOUS_SCRIPT}")
V = importlib.util.module_from_spec(specification)
specification.loader.exec_module(V)
Q = V.Q
R = V.R
DYNAMICS = V.DYNAMICS
G = DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_5169_script": PREVIOUS_SCRIPT,
        "checkpoint_5169_document": PREVIOUS_DOCUMENT,
        "checkpoint_5169_result": PREVIOUS_RESULT,
        "checkpoint_5169_score": PREVIOUS_SCORE,
        "checkpoint_5169_profile": PREVIOUS_PROFILE,
        "checkpoint_5169_validation": PREVIOUS_VALIDATION,
        "checkpoint_5163_visible_profile": VISIBLE_PROFILE,
        "checkpoint_5172_script": Path(__file__).resolve(),
    }


def configurations() -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": run_id,
            "axis_x": float(axis[0]),
            "axis_y": float(axis[1]),
            "axis_z": float(axis[2]),
            "steps_per_inner_orbit": PRIMARY_STEPS,
            "run_role": "PRIMARY" if run_id == "AXIS_Z_PRIMARY" else "ORIENTATION_CONTROL",
        }
        for run_id, axis in ORIENTATION_AXES.items()
    ]
    rows.append(
        {
            "run_id": "AXIS_Z_TIME_REFINEMENT",
            "axis_x": 0.0,
            "axis_y": 0.0,
            "axis_z": 1.0,
            "steps_per_inner_orbit": REFINED_STEPS,
            "run_role": "TIME_REFINEMENT",
        }
    )
    return [
        {
            **row,
            "thermal_mode": SELECTED_BRANCH[0],
            "metallicity_Zsun": SELECTED_BRANCH[1],
            "radial_bins": RADIAL_BINS,
            "cost_power": COST_POWER,
            "same_G_N": True,
            "same_parent_state": True,
            "same_frozen_source_history": True,
            "target_q_used_to_define_geometry": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for row in rows
    ]


def contract_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "G1_MEASURED_MIDPLANE_FORCE",
            "v_flat^2(R)=v_gas|v_gas|+0.5 v_disk^2 is read from the frozen UGC09133 source table",
            "source_backed",
        ),
        (
            "G2_HANKEL_COMPLETION",
            "H(k)=k integral dR v_flat^2(R) J1(kR)",
            "derived_axisymmetric_thin_disk_completion",
        ),
        (
            "G3_OFF_PLANE_FORCE",
            "g_R=-integral dk H(k)J1(kR)exp(-k zeta); g_z=-(z/zeta)integral dk H(k)J0(kR)exp(-k zeta)",
            "derived_from_Plummer_softened_Green_function",
        ),
        (
            "G4_BULGE",
            "M_b(r)=r[0.7 v_bulge^2(r)]/G_N with nonnegative monotone enclosed-mass regularization",
            "source_backed_spherical_completion",
        ),
        (
            "G5_UNCHANGED_HISTORY",
            "checkpoint-5169 isobaric Z=0.3 transport fractions, arrival clock, particle state and calibrated G_N are frozen",
            "exact_replay",
        ),
        (
            "G6_NO_EXTRA_RESPONSE",
            "checkpoint-5171 linear Vlasov kernel is not added to the already nonlinear checkpoint-5169 characteristics",
            "double_counting_excluded",
        ),
        (
            "G7_ORIENTATION_CONTROL",
            "the same isotropic realization is replayed about three predeclared orthogonal disk axes",
            "numerical_geometry_control",
        ),
        (
            "G8_NONCLAIM",
            "the razor-thin off-plane completion is a source-geometry test and not yet a parent matter-action derivation",
            "explicit_limitation",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "contract": contract,
            "status": status,
            "target_q_used": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for clause_id, contract, status in clauses
    ]


class AxisymmetricVisibleSource:
    def __init__(self, rows: list[dict[str, str]], softening_kpc: float) -> None:
        self.data_radii = np.asarray([float(row["radius_kpc"]) for row in rows])
        gas = np.asarray([float(row["gas_velocity_km_s"]) for row in rows])
        disk = np.asarray([float(row["disk_velocity_km_s"]) for row in rows])
        bulge = np.asarray([float(row["bulge_velocity_km_s"]) for row in rows])
        self.flat_velocity_squared = gas * np.abs(gas) + 0.5 * disk**2
        self.bulge_velocity_squared = 0.7 * bulge**2
        self.total_velocity_squared = (
            self.flat_velocity_squared + self.bulge_velocity_squared
        )
        self.flat_interpolator = PchipInterpolator(
            self.data_radii, self.flat_velocity_squared
        )
        bulge_mass_raw = (
            self.data_radii * self.bulge_velocity_squared / G
        )
        self.bulge_mass_raw = bulge_mass_raw
        monotone_bulge_mass = np.maximum.accumulate(np.maximum(bulge_mass_raw, 0.0))
        self.bulge_mass = (
            monotone_bulge_mass
            * bulge_mass_raw[-1]
            / monotone_bulge_mass[-1]
        )
        self.bulge_interpolator = PchipInterpolator(
            self.data_radii, self.bulge_mass
        )
        total_mass_raw = self.data_radii * self.total_velocity_squared / G
        self.total_mass = np.maximum.accumulate(np.maximum(total_mass_raw, 0.0))
        self.total_mass_interpolator = PchipInterpolator(
            self.data_radii, self.total_mass
        )
        self.flat_outer_mass = (
            self.data_radii[-1] * self.flat_velocity_squared[-1] / G
        )
        self.bulge_outer_mass = float(self.bulge_mass[-1])
        self.total_outer_mass = float(self.total_mass[-1])
        self.softening_kpc = float(softening_kpc)
        self.log_radius = np.linspace(
            math.log(TRANSFORM_MIN_KPC),
            math.log(TRANSFORM_MAX_KPC),
            TRANSFORM_POINTS,
        )
        self.transform_radii = np.exp(self.log_radius)
        self.dln = float(self.log_radius[1] - self.log_radius[0])
        self.offset = float(fft.fhtoffset(self.dln, mu=1.0, initial=0.0, bias=0.0))
        self.wavenumber = np.exp(self.offset) / self.transform_radii[::-1]
        input_velocity = self._flat_velocity_at(self.transform_radii)
        self.hankel_amplitude = fft.fht(
            input_velocity,
            self.dln,
            mu=1.0,
            offset=self.offset,
            bias=0.0,
        )
        self.reconstructed_velocity = fft.ifht(
            self.hankel_amplitude,
            self.dln,
            mu=1.0,
            offset=self.offset,
            bias=0.0,
        )
        self.surface_density = (
            fft.ifht(
                self.hankel_amplitude,
                self.dln,
                mu=0.0,
                offset=self.offset,
                bias=0.0,
            )
            / self.transform_radii
            / (2.0 * math.pi * G)
        )
        self.vertical_grid = np.geomspace(
            self.softening_kpc,
            max(VERTICAL_MAX_KPC, self.softening_kpc * 1.001),
            VERTICAL_POINTS,
        )
        self.log_vertical = np.log(self.vertical_grid)
        self.vertical_dln = float(self.log_vertical[1] - self.log_vertical[0])
        self.radial_acceleration_table = np.empty(
            (VERTICAL_POINTS, TRANSFORM_POINTS), dtype=float
        )
        self.vertical_integral_table = np.empty_like(
            self.radial_acceleration_table
        )
        for index, vertical in enumerate(self.vertical_grid):
            damped = self.hankel_amplitude * np.exp(-self.wavenumber * vertical)
            radial_velocity_squared = fft.ifht(
                damped,
                self.dln,
                mu=1.0,
                offset=self.offset,
                bias=0.0,
            )
            vertical_integral = (
                fft.ifht(
                    damped,
                    self.dln,
                    mu=0.0,
                    offset=self.offset,
                    bias=0.0,
                )
                / self.transform_radii
            )
            self.radial_acceleration_table[index] = (
                -radial_velocity_squared / self.transform_radii
            )
            self.vertical_integral_table[index] = vertical_integral

    def _flat_velocity_at(self, radius: np.ndarray) -> np.ndarray:
        result = np.empty_like(radius)
        inner = radius < self.data_radii[0]
        middle = (radius >= self.data_radii[0]) & (radius <= self.data_radii[-1])
        outer = radius > self.data_radii[-1]
        result[inner] = self.flat_velocity_squared[0] * (
            radius[inner] / self.data_radii[0]
        ) ** 2
        result[middle] = self.flat_interpolator(radius[middle])
        result[outer] = (
            self.flat_velocity_squared[-1]
            * self.data_radii[-1]
            / radius[outer]
        )
        return result

    def _mass_at(
        self,
        radius_kpc: np.ndarray,
        masses: np.ndarray,
        interpolator: PchipInterpolator,
    ) -> np.ndarray:
        radius = np.asarray(radius_kpc, dtype=float)
        result = np.empty_like(radius)
        inner = radius < self.data_radii[0]
        middle = (radius >= self.data_radii[0]) & (radius <= self.data_radii[-1])
        outer = radius > self.data_radii[-1]
        result[inner] = masses[0] * (radius[inner] / self.data_radii[0]) ** 3
        result[middle] = interpolator(radius[middle])
        result[outer] = masses[-1]
        return result

    def bulge_mass_at(self, radius_kpc: np.ndarray) -> np.ndarray:
        return self._mass_at(radius_kpc, self.bulge_mass, self.bulge_interpolator)

    def total_equivalent_mass_at(self, radius_kpc: np.ndarray) -> np.ndarray:
        return self._mass_at(
            radius_kpc, self.total_mass, self.total_mass_interpolator
        )

    def _bilinear(self, table: np.ndarray, radius: np.ndarray, vertical: np.ndarray) -> np.ndarray:
        clipped_radius = np.clip(
            radius, self.transform_radii[0], self.transform_radii[-1]
        )
        radial_coordinate = (
            np.log(clipped_radius) - self.log_radius[0]
        ) / self.dln
        radial_index = np.clip(
            np.floor(radial_coordinate).astype(np.int64),
            0,
            TRANSFORM_POINTS - 2,
        )
        radial_fraction = radial_coordinate - radial_index
        clipped_vertical = np.clip(
            vertical, self.vertical_grid[0], self.vertical_grid[-1]
        )
        vertical_coordinate = (
            np.log(clipped_vertical) - self.log_vertical[0]
        ) / self.vertical_dln
        vertical_index = np.clip(
            np.floor(vertical_coordinate).astype(np.int64),
            0,
            VERTICAL_POINTS - 2,
        )
        vertical_fraction = vertical_coordinate - vertical_index
        lower = (
            table[vertical_index, radial_index] * (1.0 - radial_fraction)
            + table[vertical_index, radial_index + 1] * radial_fraction
        )
        upper = (
            table[vertical_index + 1, radial_index] * (1.0 - radial_fraction)
            + table[vertical_index + 1, radial_index + 1] * radial_fraction
        )
        return lower * (1.0 - vertical_fraction) + upper * vertical_fraction

    def acceleration(self, positions: np.ndarray, axis: np.ndarray) -> np.ndarray:
        axis = np.asarray(axis, dtype=float)
        axis = axis / np.linalg.norm(axis)
        axial_position = positions @ axis
        radial_vectors = positions - axial_position[:, None] * axis[None, :]
        cylindrical_radius = np.linalg.norm(radial_vectors, axis=1)
        vertical = np.sqrt(axial_position**2 + self.softening_kpc**2)
        radial_acceleration = self._bilinear(
            self.radial_acceleration_table, cylindrical_radius, vertical
        )
        vertical_integral = self._bilinear(
            self.vertical_integral_table, cylindrical_radius, vertical
        )
        disk = np.zeros_like(positions)
        positive = cylindrical_radius > 0.0
        disk[positive] = (
            radial_acceleration[positive, None]
            * radial_vectors[positive]
            / cylindrical_radius[positive, None]
        )
        disk += (
            -(axial_position / vertical) * vertical_integral
        )[:, None] * axis[None, :]
        radii = np.linalg.norm(positions, axis=1)
        bulge_mass = self.bulge_mass_at(radii)
        denominator = (radii**2 + self.softening_kpc**2) ** 1.5
        bulge = np.zeros_like(positions)
        finite = denominator > 0.0
        bulge[finite] = (
            -G * bulge_mass[finite] / denominator[finite]
        )[:, None] * positions[finite]
        outside = (cylindrical_radius > self.transform_radii[-2]) | (
            vertical > self.vertical_grid[-2]
        )
        if np.any(outside):
            denominator_disk = (
                cylindrical_radius[outside] ** 2
                + axial_position[outside] ** 2
                + self.softening_kpc**2
            ) ** 1.5
            disk[outside] = (
                -G * self.flat_outer_mass / denominator_disk
            )[:, None] * positions[outside]
        return disk + bulge

    def audit(self) -> tuple[list[dict[str, Any]], dict[str, float]]:
        reconstructed = np.interp(
            np.log(self.data_radii), self.log_radius, self.reconstructed_velocity
        )
        relative = np.abs(reconstructed - self.flat_velocity_squared) / np.maximum(
            np.abs(self.flat_velocity_squared), 1.0
        )
        rows: list[dict[str, Any]] = []
        for radius, reference, derived, error in zip(
            self.data_radii,
            self.flat_velocity_squared,
            reconstructed,
            relative,
        ):
            rows.append(
                {
                    "audit_type": "midplane_Hankel_reconstruction",
                    "radius_kpc": radius,
                    "z_kpc": 0.0,
                    "quantity": "gas_plus_disk_velocity_squared",
                    "reference_value": reference,
                    "derived_value": derived,
                    "relative_error": error,
                    "units": "km2_s2",
                    "passed": error < 1.0e-3,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        surface_mask = (
            (self.transform_radii >= 0.05)
            & (self.transform_radii <= 500.0)
        )
        selected_radius = self.transform_radii[surface_mask]
        selected_surface = self.surface_density[surface_mask]
        positive_mass = float(
            2.0
            * math.pi
            * np.trapezoid(
                np.maximum(selected_surface, 0.0) * selected_radius,
                selected_radius,
            )
        )
        negative_mass = float(
            2.0
            * math.pi
            * np.trapezoid(
                np.maximum(-selected_surface, 0.0) * selected_radius,
                selected_radius,
            )
        )
        probes = [(36.439, 0.0), (100.0, 100.0), (300.0, 300.0)]
        for radius, height in probes:
            point = np.asarray([[radius, 0.0, height]], dtype=float)
            acceleration = self.acceleration(point, PRIMARY_AXIS)[0]
            disk_acceleration = acceleration.copy()
            spherical_radius = math.sqrt(radius**2 + height**2)
            bulge_mass = float(self.bulge_mass_at(np.asarray([spherical_radius]))[0])
            bulge = -G * bulge_mass * point[0] / (
                spherical_radius**2 + self.softening_kpc**2
            ) ** 1.5
            disk_acceleration -= bulge
            point_mass = -G * self.flat_outer_mass * point[0] / (
                spherical_radius**2 + self.softening_kpc**2
            ) ** 1.5
            relative_error = float(
                np.linalg.norm(disk_acceleration - point_mass)
                / max(np.linalg.norm(point_mass), 1.0e-300)
            )
            rows.append(
                {
                    "audit_type": "far_field_disk_force_probe",
                    "radius_kpc": radius,
                    "z_kpc": height,
                    "quantity": "vector_acceleration_difference_from_point_mass",
                    "reference_value": float(np.linalg.norm(point_mass)),
                    "derived_value": float(np.linalg.norm(disk_acceleration)),
                    "relative_error": relative_error,
                    "units": "km2_s2_kpc",
                    "passed": relative_error < (0.35 if radius <= 100.0 else 0.1),
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        summary = {
            "reconstruction_rms_relative_error": float(
                math.sqrt(np.mean(relative**2))
            ),
            "reconstruction_max_relative_error": float(np.max(relative)),
            "minimum_surface_density_Msun_kpc2_0p05_to_500": float(
                np.min(selected_surface)
            ),
            "positive_surface_mass_Msun_0p05_to_500": positive_mass,
            "negative_surface_mass_Msun_0p05_to_500": negative_mass,
            "negative_surface_mass_fraction": negative_mass
            / max(positive_mass, 1.0),
            "flat_outer_mass_Msun": self.flat_outer_mass,
            "bulge_outer_mass_Msun": self.bulge_outer_mass,
            "total_outer_mass_Msun": self.total_outer_mass,
            "outer_component_mass_relative_residual": abs(
                self.flat_outer_mass + self.bulge_outer_mass - self.total_outer_mass
            )
            / max(self.total_outer_mass, 1.0),
            "bulge_monotone_regularization_fraction": float(
                np.max(np.abs(self.bulge_mass - self.bulge_mass_raw))
                / max(self.bulge_outer_mass, 1.0)
            ),
        }
        return rows, summary


def combined_acceleration(
    positions: np.ndarray,
    particle_weight: np.ndarray,
    particle_mass: float,
    transfer_per_particle: np.ndarray,
    condensed_fraction: float,
    source: AxisymmetricVisibleSource,
    axis: np.ndarray,
) -> np.ndarray:
    radii = np.linalg.norm(positions, axis=1)
    order = np.argsort(radii)
    sorted_radii = radii[order]
    gravitational_masses = particle_weight * (
        particle_mass - transfer_per_particle
    )
    if np.any(gravitational_masses < -1.0e-6):
        raise RuntimeError("negative transported particle mass")
    sorted_masses = gravitational_masses[order]
    enclosed_particles = np.cumsum(sorted_masses) - 0.5 * sorted_masses
    background = (
        4.0
        * math.pi
        * DYNAMICS.PM.RHO_M_MSUN_MPC3
        * (sorted_radii / 1000.0) ** 3
        / 3.0
    )
    diffuse = enclosed_particles - background
    spherical_proxy = condensed_fraction * source.total_equivalent_mass_at(
        sorted_radii
    )
    diffuse = np.maximum(diffuse, -spherical_proxy)
    denominator = (sorted_radii**2 + source.softening_kpc**2) ** 1.5
    coefficient = np.zeros_like(sorted_radii)
    positive = denominator > 0.0
    coefficient[positive] = -G * diffuse[positive] / denominator[positive]
    result = np.empty_like(positions)
    result[order] = coefficient[:, None] * positions[order]
    if condensed_fraction > 0.0:
        result += condensed_fraction * source.acceleration(positions, axis)
    return result


def evolve(
    snapshot: dict[str, Any],
    plan: dict[str, Any],
    source: AxisymmetricVisibleSource,
    axis: np.ndarray,
    profile_radii_kpc: np.ndarray,
    transition_orbit: float,
    inner_orbit: float,
    steps_per_inner_orbit: int,
    source_enabled: bool,
) -> dict[str, Any]:
    positions = np.asarray(snapshot["positions_kpc"], dtype=float).copy()
    velocities = np.asarray(snapshot["velocities_km_s"], dtype=float).copy()
    particle_count = len(positions)
    particle_weight = np.asarray(
        snapshot.get("particle_weight", np.ones(particle_count)), dtype=float
    )
    initial_radius = np.asarray(snapshot["initial_radius_kpc"], dtype=float)
    particle_mass = float(snapshot["particle_mass_Msun"][0])
    edge_radius = float(snapshot["edge_radius_kpc"][0])
    common_duration = float(plan["endpoint_time_internal"])
    total_time = common_duration + DYNAMICS.SETTLING_ORBITS * transition_orbit
    averaging_time = DYNAMICS.AVERAGING_ORBITS * transition_orbit
    nominal_dt = inner_orbit / steps_per_inner_orbit
    steps = max(1, int(math.ceil(total_time / nominal_dt)))
    time_step = total_time / steps
    averaging_start = max(total_time - averaging_time, 0.0)
    sample_stride = max(
        1,
        int(
            round(
                max(1.0, averaging_time / time_step)
                / DYNAMICS.PROFILE_AVERAGE_SAMPLES
            )
        ),
    )
    axis = np.asarray(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    initial_angular_momentum = np.cross(positions, velocities)
    initial_axis_angular_momentum = initial_angular_momentum @ axis
    initial_com = np.average(positions, axis=0, weights=particle_weight)
    zero_transfer = np.zeros(particle_count, dtype=float)
    start = time.perf_counter()

    def current_transfer(current_time: float) -> tuple[np.ndarray, float]:
        if not source_enabled:
            return zero_transfer, 0.0
        return V.transfer_at(plan, current_time)

    transfer, condensed_fraction = current_transfer(0.0)
    force = combined_acceleration(
        positions,
        particle_weight,
        particle_mass,
        transfer,
        condensed_fraction,
        source,
        axis,
    )
    half_velocity = velocities + 0.5 * time_step * force
    count_samples: list[np.ndarray] = []
    final_fraction = condensed_fraction
    final_transfer = transfer
    for step in range(steps):
        positions += time_step * half_velocity
        current_time = (step + 1) * time_step
        final_transfer, final_fraction = current_transfer(current_time)
        force = combined_acceleration(
            positions,
            particle_weight,
            particle_mass,
            final_transfer,
            final_fraction,
            source,
            axis,
        )
        if step < steps - 1:
            half_velocity += time_step * force
        else:
            velocities = half_velocity + 0.5 * time_step * force
        if current_time >= averaging_start and (
            step % sample_stride == 0 or step == steps - 1
        ):
            count_samples.append(
                DYNAMICS.cumulative_counts(
                    positions, profile_radii_kpc, particle_weight
                )
            )
    averaged_counts = np.mean(np.asarray(count_samples), axis=0)
    final_angular_momentum = np.cross(positions, velocities)
    final_axis_angular_momentum = final_angular_momentum @ axis
    axis_angular_residual = float(
        math.sqrt(
            np.sum(
                particle_weight
                * (final_axis_angular_momentum - initial_axis_angular_momentum) ** 2
            )
            / max(
                np.sum(particle_weight * initial_axis_angular_momentum**2),
                1.0e-300,
            )
        )
    )
    full_angular_change = float(
        math.sqrt(
            np.sum(
                particle_weight[:, None]
                * (final_angular_momentum - initial_angular_momentum) ** 2
            )
            / max(
                np.sum(
                    particle_weight[:, None] * initial_angular_momentum**2
                ),
                1.0e-300,
            )
        )
    )
    final_radii = np.linalg.norm(positions, axis=1)
    boundary_ingress = float(
        np.sum(
            particle_weight[
                (
                    initial_radius
                    > 0.9 * DYNAMICS.ISOLATION_EDGE_MULTIPLE * edge_radius
                )
                & (final_radii <= DYNAMICS.SCORE_EDGE_FRACTION * edge_radius)
            ]
        )
    )
    final_inside = max(
        float(
            np.sum(
                particle_weight[
                    final_radii <= DYNAMICS.SCORE_EDGE_FRACTION * edge_radius
                ]
            )
        ),
        1.0,
    )
    represented_transfer = float(np.sum(particle_weight * final_transfer))
    condensed = float(plan["condensed_Msun"])
    return {
        "averaged_counts": averaged_counts,
        "steps": steps,
        "time_step_internal": time_step,
        "profile_sample_count": len(count_samples),
        "final_assembly_fraction": final_fraction,
        "final_transferred_mass_Msun": represented_transfer,
        "final_transfer_relative_residual": (
            abs(represented_transfer - condensed) / max(condensed, 1.0)
            if source_enabled
            else 0.0
        ),
        "maximum_transfer_fraction_of_available_baryons": float(
            np.max(final_transfer)
            / max(float(plan["baryon_available_per_particle_Msun"]), 1.0e-300)
        ),
        "axis_angular_momentum_relative_residual": axis_angular_residual,
        "full_vector_angular_momentum_relative_change": full_angular_change,
        "center_of_mass_drift_kpc": float(
            np.linalg.norm(
                np.average(positions, axis=0, weights=particle_weight) - initial_com
            )
        ),
        "outer_boundary_ingress_fraction": boundary_ingress / final_inside,
        "wall_seconds": time.perf_counter() - start,
        "softening_kpc": source.softening_kpc,
    }


def evolution_signature(
    source_hashes: dict[str, str],
    run_key: str,
    phase_sign: int,
    source_enabled: bool,
    axis: np.ndarray,
    steps_per_inner_orbit: int,
) -> str:
    payload = {
        "source_hashes": source_hashes,
        "run_key": run_key,
        "phase_sign": phase_sign,
        "source_enabled": source_enabled,
        "axis": [float(value) for value in axis],
        "steps_per_inner_orbit": steps_per_inner_orbit,
        "marker": MARKER,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def run_or_load_evolution(
    run_key: str,
    source_hashes: dict[str, str],
    snapshot: dict[str, Any],
    plan: dict[str, Any],
    source: AxisymmetricVisibleSource,
    axis: np.ndarray,
    profile_radii_kpc: np.ndarray,
    transition_orbit: float,
    inner_orbit: float,
    steps_per_inner_orbit: int,
    source_enabled: bool,
    phase_sign: int,
    force: bool,
) -> dict[str, Any]:
    signature = evolution_signature(
        source_hashes,
        run_key,
        phase_sign,
        source_enabled,
        axis,
        steps_per_inner_orbit,
    )
    stem = f"{run_key}_PHASE_{phase_sign:+d}".replace("+", "PLUS").replace("-", "MINUS")
    array_path = CACHE / f"{stem}.npz"
    metadata_path = CACHE / f"{stem}.json"
    if not force and array_path.is_file() and metadata_path.is_file():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("cache_signature") == signature:
            with np.load(array_path) as archive:
                averaged_counts = np.asarray(archive["averaged_counts"], dtype=float)
            return {**metadata["diagnostics"], "averaged_counts": averaged_counts}
    print(f"START {run_key} phase={phase_sign:+d}", flush=True)
    result = evolve(
        snapshot,
        plan,
        source,
        axis,
        profile_radii_kpc,
        transition_orbit,
        inner_orbit,
        steps_per_inner_orbit,
        source_enabled,
    )
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(array_path, averaged_counts=result["averaged_counts"])
    diagnostics = {
        key: value for key, value in result.items() if key != "averaged_counts"
    }
    Q.write_json(
        metadata_path,
        {"cache_signature": signature, "diagnostics": diagnostics},
    )
    print(
        f"DONE {run_key} phase={phase_sign:+d} wall={diagnostics['wall_seconds']:.3f}s",
        flush=True,
    )
    return result


def previous_selected() -> tuple[dict[str, str], list[dict[str, str]]]:
    score = next(
        row
        for row in read_csv(PREVIOUS_SCORE)
        if row["run_id"]
        == "ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY"
    )
    profiles = [
        row
        for row in read_csv(PREVIOUS_PROFILE)
        if row["run_id"] == score["run_id"]
    ]
    profiles.sort(key=lambda row: float(row["radius_kpc"]))
    return score, profiles


def run_configuration(
    configuration: dict[str, Any],
    context: dict[str, Any],
    solution: dict[str, Any],
    data: dict[str, Any],
    transport: dict[str, Any],
    sources: dict[int, AxisymmetricVisibleSource],
    source_hashes: dict[str, str],
    force: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[int, np.ndarray]]:
    axis = np.asarray(
        [
            configuration["axis_x"],
            configuration["axis_y"],
            configuration["axis_z"],
        ],
        dtype=float,
    )
    steps = int(configuration["steps_per_inner_orbit"])
    phase_mass: dict[int, np.ndarray] = {}
    controls: list[dict[str, Any]] = []
    for phase_sign in (-1, 1):
        snapshot = context["snapshots"][phase_sign]
        plan = V.phase_plan(snapshot, solution, data, transport, phase_sign)
        source = sources[phase_sign]
        control = run_or_load_evolution(
            f"SPHERICAL_FREE_CONTROL_S{steps}",
            source_hashes,
            snapshot,
            plan,
            source,
            PRIMARY_AXIS,
            context["radii"],
            context["transition_orbit"],
            context["inner_orbit"],
            steps,
            False,
            phase_sign,
            force,
        )
        source_run = run_or_load_evolution(
            str(configuration["run_id"]),
            source_hashes,
            snapshot,
            plan,
            source,
            axis,
            context["radii"],
            context["transition_orbit"],
            context["inner_orbit"],
            steps,
            True,
            phase_sign,
            force,
        )
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        background = (
            4.0
            * math.pi
            * DYNAMICS.PM.RHO_M_MSUN_MPC3
            * (context["radii"] / 1000.0) ** 3
            / 3.0
        )
        source_mass = DYNAMICS.PM.MOTION_FRACTION * np.maximum(
            source_run["averaged_counts"] * particle_mass - background, 0.0
        )
        control_mass = DYNAMICS.PM.MOTION_FRACTION * np.maximum(
            control["averaged_counts"] * particle_mass - background, 0.0
        )
        ratio = np.ones_like(context["radii"])
        positive = control_mass > 0.0
        ratio[positive] = source_mass[positive] / control_mass[positive]
        phase_mass[phase_sign] = context["initial_phase_mass"][phase_sign] * ratio
        controls.append(
            {
                "run_id": configuration["run_id"],
                "run_role": configuration["run_role"],
                "phase_sign": phase_sign,
                "axis_x": configuration["axis_x"],
                "axis_y": configuration["axis_y"],
                "axis_z": configuration["axis_z"],
                "response_particle_count": len(snapshot["positions_kpc"]),
                "steps_per_inner_orbit": steps,
                "source_steps": source_run["steps"],
                "control_steps": control["steps"],
                "source_axis_angular_momentum_relative_residual": source_run[
                    "axis_angular_momentum_relative_residual"
                ],
                "source_full_vector_angular_momentum_relative_change": source_run[
                    "full_vector_angular_momentum_relative_change"
                ],
                "control_axis_angular_momentum_relative_residual": control[
                    "axis_angular_momentum_relative_residual"
                ],
                "source_final_transfer_relative_residual": source_run[
                    "final_transfer_relative_residual"
                ],
                "source_center_of_mass_drift_kpc": source_run[
                    "center_of_mass_drift_kpc"
                ],
                "control_center_of_mass_drift_kpc": control[
                    "center_of_mass_drift_kpc"
                ],
                "source_outer_boundary_ingress_fraction": source_run[
                    "outer_boundary_ingress_fraction"
                ],
                "control_outer_boundary_ingress_fraction": control[
                    "outer_boundary_ingress_fraction"
                ],
                "source_wall_seconds": source_run["wall_seconds"],
                "control_wall_seconds": control["wall_seconds"],
                "softening_kpc": source["softening_kpc"] if isinstance(source, dict) else source.softening_kpc,
                "target_q_used": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    corrected_mass = 0.5 * (phase_mass[-1] + phase_mass[1])
    score = DYNAMICS.score_profile(
        context["radii"],
        corrected_mass,
        context["target_velocity"],
        context["score_mask"],
        context["transition_radius"],
        context["edge_radius"],
        context["target_edge_mass"],
    )
    q_parent = float(context["q_row"]["q_parent"])
    q_envelope = float(context["q_row"]["q_uncertainty_envelope"])
    score_row = {
        **configuration,
        "common_endpoint_Gyr": float(solution["endpoint_time_Gyr"]),
        "q_parent": q_parent,
        "q_envelope": q_envelope,
        "corrected_q": score["q"],
        "corrected_q_absolute_difference": abs(float(score["q"]) - q_parent),
        "corrected_q_compatible": abs(float(score["q"]) - q_parent) <= q_envelope,
        "corrected_velocity_squared_log10_RMSE": score[
            "velocity_squared_log10_RMSE"
        ],
        "baseline_velocity_squared_log10_RMSE": context["baseline_score"][
            "velocity_squared_log10_RMSE"
        ],
        "corrected_RMSE_improves_free_baseline": score[
            "velocity_squared_log10_RMSE"
        ]
        < context["baseline_score"]["velocity_squared_log10_RMSE"],
        "corrected_transition_velocity_squared_ratio_to_target": score[
            "transition_velocity_squared_ratio_to_target"
        ],
        "corrected_edge_mass_ratio_to_target": score["edge_mass_ratio_to_target"],
        "response_efficiency_fitted": False,
        "geometry_parameter_fitted": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    return score_row, controls, phase_mass


def add_validation(
    rows: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "evidence": json.dumps(evidence, sort_keys=True),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    score_lines = "\n".join(
        f"- `{row['run_id']}`: q=`{row['corrected_q']}`, "
        f"RMSE=`{row['corrected_velocity_squared_log10_RMSE']}` dex, "
        f"compatible=`{row['corrected_q_compatible']}`"
        for row in summary["scores"]
    )
    return f"""# 5172 - Source-backed axisymmetric baryon geometry forward response gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Question

Checkpoint 5169 evolved the measured visible source as a spherical-equivalent
mass. Checkpoint 5171 showed that adding a separate static Vlasov response
would double-count those same characteristics. This checkpoint therefore asks
the narrower forward question: does the measured non-spherical source geometry
close the remaining response gap with the parent state, source history and
calibrated `G_N` held fixed?

## Derived geometry operator

The frozen SPARC components define

```text
v_flat^2(R)=v_gas(R)|v_gas(R)|+0.5 v_disk^2(R).
```

For the unique razor-thin axisymmetric completion of that midplane force,

```text
H(k)=k integral dR v_flat^2(R) J1(kR),
zeta=sqrt(z^2+epsilon^2),
g_R(R,z)=-integral dk H(k)J1(kR)exp(-k zeta),
g_z(R,z)=-(z/zeta)integral dk H(k)J0(kR)exp(-k zeta).
```

The exponential is the exact Hankel form of the same Plummer-softened Green
function used by the particle calculation. The measured `0.7 v_bulge^2`
component remains spherical. No galaxy target, response amplitude or new
coupling appears in this construction.

The Hankel reconstruction has RMS relative error
`{summary['force_audit']['reconstruction_rms_relative_error']}` and maximum
error `{summary['force_audit']['reconstruction_max_relative_error']}`. The
reconstructed surface-density negative-mass fraction over `0.05--500 kpc` is
`{summary['force_audit']['negative_surface_mass_fraction']}`. The component
outer masses close to relative residual
`{summary['force_audit']['outer_component_mass_relative_residual']}`.

## Forward replay

The checkpoint-5169 isobaric `Z=0.3` transport, arrival clock and full
antithetic states are replayed without alteration about three orthogonal disk
axes. A doubled time resolution is also run for the primary axis.

{score_lines}

The checkpoint-5169 spherical result was q=`{summary['spherical_q']}` and
RMSE=`{summary['spherical_RMSE']}` dex. The primary geometry shifts these by
`Delta q={summary['primary_delta_q_from_spherical']}` and
`Delta RMSE={summary['primary_delta_RMSE_from_spherical']}` dex. The maximum
orthogonal-axis displacement from the primary is
`{summary['maximum_orientation_delta_q']}`, and the doubled-time-step
displacement is `{summary['time_refinement_delta_q']}`.

## Decision

`{result['route_decision']}`.

This is a controlled source-geometry gate. It does not derive the thin-disk
completion from the parent matter action, validate a full local PPN branch, or
authorize a galaxy/full-MTS claim. It does remove spherical source projection
as an untested approximation while retaining the same state and one calibrated
`G_N`.

```text
measured source components used                = yes;
same parent state and source history           = yes;
same calibrated G_N                            = yes;
new response coefficient                       = no;
checkpoint-5171 response added                 = no;
orientation and time controls run              = yes;
galaxy or full-MTS claim                       = false.
```

All `{result['validation_count']}` validation rows pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = Q.tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: Q.file_digest(path) for key, path in paths.items()}
    run_rows = configurations()
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "run_ids": [row["run_id"] for row in run_rows],
                    "same_parent_state": True,
                    "same_G_N": True,
                    "target_q_used": False,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
    context, polynomial, _, solutions = R.build_parent_state()
    solution = solutions[SELECTED_BRANCH]
    data = R.binned_inputs(context, solution, polynomial, RADIAL_BINS)
    transport = R.solve_transport(data, COST_POWER)
    source_rows = read_csv(VISIBLE_PROFILE)
    softening_by_phase = {
        phase_sign: DYNAMICS.SOFTENING_CELL_MULTIPLE
        * float(context["snapshots"][phase_sign]["local_force_cell_kpc"][0])
        for phase_sign in (-1, 1)
    }
    sources = {
        phase_sign: AxisymmetricVisibleSource(source_rows, softening)
        for phase_sign, softening in softening_by_phase.items()
    }
    force_audit_rows, force_audit = sources[-1].audit()
    scores: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    masses: dict[str, dict[int, np.ndarray]] = {}
    for configuration in run_rows:
        score, run_controls, phase_mass = run_configuration(
            configuration,
            context,
            solution,
            data,
            transport,
            sources,
            hashes_before,
            arguments.force,
        )
        scores.append(score)
        controls.extend(run_controls)
        masses[str(configuration["run_id"])] = phase_mass
        print(
            f"SCORE {configuration['run_id']} q={score['corrected_q']} "
            f"RMSE={score['corrected_velocity_squared_log10_RMSE']}",
            flush=True,
        )
    spherical_score, spherical_profiles = previous_selected()
    spherical_mass = np.asarray(
        [float(row["corrected_motion_mass_Msun"]) for row in spherical_profiles]
    )
    primary = next(row for row in scores if row["run_id"] == "AXIS_Z_PRIMARY")
    refined = next(
        row for row in scores if row["run_id"] == "AXIS_Z_TIME_REFINEMENT"
    )
    orientation = [row for row in scores if row["run_role"] == "ORIENTATION_CONTROL"]
    primary_mass = 0.5 * (
        masses["AXIS_Z_PRIMARY"][-1] + masses["AXIS_Z_PRIMARY"][1]
    )
    profile_rows: list[dict[str, Any]] = []
    for index, radius in enumerate(context["radii"]):
        profile_rows.append(
            {
                "radius_kpc": radius,
                "radius_over_transition": radius / context["transition_radius"],
                "axisymmetric_primary_motion_mass_Msun": primary_mass[index],
                "spherical_checkpoint_5169_motion_mass_Msun": spherical_mass[index],
                "axisymmetric_minus_spherical_mass_Msun": primary_mass[index]
                - spherical_mass[index],
                "axisymmetric_to_spherical_mass_ratio": primary_mass[index]
                / max(spherical_mass[index], 1.0),
                "target_motion_v2_km2_s2": context["target_velocity"][index],
                "inside_scoring_window": bool(context["score_mask"][index]),
                "target_q_used": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    parent_lower = float(context["q_row"]["q_parent"]) - float(
        context["q_row"]["q_uncertainty_envelope"]
    )
    parent_upper = float(context["q_row"]["q_parent"]) + float(
        context["q_row"]["q_uncertainty_envelope"]
    )
    maximum_orientation_delta = max(
        abs(float(row["corrected_q"]) - float(primary["corrected_q"]))
        for row in orientation
    )
    time_delta = abs(float(refined["corrected_q"]) - float(primary["corrected_q"]))
    all_axis_compatible = all(bool(row["corrected_q_compatible"]) for row in scores[:3])
    primary_gap = max(
        parent_lower - float(primary["corrected_q"]),
        float(primary["corrected_q"]) - parent_upper,
        0.0,
    )
    spherical_gap = max(
        parent_lower - float(spherical_score["corrected_q"]),
        float(spherical_score["corrected_q"]) - parent_upper,
        0.0,
    )
    robust_numerics = maximum_orientation_delta < 0.02 and time_delta < 0.01
    if all_axis_compatible and robust_numerics:
        route_decision = (
            "SOURCE_BACKED_AXISYMMETRIC_GEOMETRY_CLOSES_THE_SELECTED_EMPIRICAL_Q_GATE_ACROSS_ORIENTATION_AND_TIME_CONTROLS_BUT_REMAINS_A_THIN_DISK_SOURCE_COMPLETION_REQUIRING_PARENT_MATTER_ACTION_DERIVATION"
        )
    elif primary_gap < spherical_gap and robust_numerics:
        route_decision = (
            "SOURCE_BACKED_AXISYMMETRIC_GEOMETRY_REDUCES_BUT_DOES_NOT_CLOSE_THE_PARENT_Q_GAP_SO_SPHERICAL_PROJECTION_WAS_PART_OF_THE_RESIDUAL_BUT_IS_NOT_THE_MISSING_PARENT_PHYSICS"
        )
    elif not robust_numerics:
        route_decision = (
            "THE_AXISYMMETRIC_SOURCE_RESPONSE_IS_ORIENTATION_OR_TIME_SENSITIVE_AND_CANNOT_BE_PROMOTED_MOVE_TO_STATE_ISOTROPY_AND_FORCE_RESOLUTION_BEFORE_NEW_PHYSICS"
        )
    else:
        route_decision = (
            "SOURCE_BACKED_AXISYMMETRIC_GEOMETRY_DOES_NOT_IMPROVE_THE_PARENT_Q_GATE_SO_THE_CURRENT_OCCUPIED_STATE_SOURCE_BRIDGE_REQUIRES_NEW_PARENT_PHYSICS_NOT_A_GEOMETRY_OR_COUPLING_PATCH"
        )
    decisions = [
        {
            "route": "source_backed_axisymmetric_geometry",
            "result": route_decision,
            "evidence": (
                f"spherical_q={spherical_score['corrected_q']}; "
                f"axisymmetric_q={primary['corrected_q']}; "
                f"primary_gap={primary_gap}; spherical_gap={spherical_gap}; "
                f"orientation_delta={maximum_orientation_delta}; time_delta={time_delta}"
            ),
            "next_requirement": (
                "derive the source geometry from the parent matter action and replicate all physical clocks"
                if all_axis_compatible and robust_numerics
                else "test whether a different parent occupied state or genuinely new nonclassical stress supplies the remaining compensated response"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    hashes_after = {key: Q.file_digest(path) for key, path in paths.items()}
    formal_after = Q.tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "all_sources_exist", not missing, missing)
    add_validation(
        validation, "source_hashes_unchanged", hashes_before == hashes_after, hashes_after
    )
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "Hankel_midplane_reconstruction",
        force_audit["reconstruction_max_relative_error"] < 1.0e-3,
        force_audit,
    )
    add_validation(
        validation,
        "nonnegative_reconstructed_surface_source",
        force_audit["negative_surface_mass_fraction"] < 1.0e-6,
        force_audit["negative_surface_mass_fraction"],
    )
    add_validation(
        validation,
        "outer_component_mass_closure",
        force_audit["outer_component_mass_relative_residual"] < 1.0e-12,
        force_audit["outer_component_mass_relative_residual"],
    )
    add_validation(
        validation,
        "all_runs_finite",
        all(
            math.isfinite(float(row["corrected_q"]))
            and math.isfinite(float(row["corrected_velocity_squared_log10_RMSE"]))
            for row in scores
        ),
        [row["run_id"] for row in scores],
    )
    add_validation(
        validation,
        "phase_transfer_conserved",
        max(
            float(row["source_final_transfer_relative_residual"])
            for row in controls
        )
        < 1.0e-10,
        max(
            float(row["source_final_transfer_relative_residual"])
            for row in controls
        ),
    )
    add_validation(
        validation,
        "axis_angular_momentum_conserved",
        max(
            float(row["source_axis_angular_momentum_relative_residual"])
            for row in controls
        )
        < 1.0e-10,
        max(
            float(row["source_axis_angular_momentum_relative_residual"])
            for row in controls
        ),
    )
    add_validation(
        validation,
        "orientation_control_bounded",
        maximum_orientation_delta < 0.02,
        maximum_orientation_delta,
    )
    add_validation(
        validation,
        "time_refinement_bounded",
        time_delta < 0.01,
        time_delta,
    )
    add_validation(
        validation,
        "same_parent_and_G_N",
        all(bool(row["same_parent_state"]) and bool(row["same_G_N"]) for row in scores),
        G,
    )
    add_validation(
        validation,
        "no_target_or_fitted_geometry",
        all(
            not bool(row["target_q_used_to_define_geometry"])
            and not bool(row["geometry_parameter_fitted"])
            and not bool(row["response_efficiency_fitted"])
            for row in scores
        ),
        [row["run_id"] for row in scores],
    )
    all_output_rows = (
        contract_rows()
        + force_audit_rows
        + scores
        + controls
        + profile_rows
        + decisions
    )
    add_validation(
        validation,
        "all_rows_nonclaim",
        all(not bool(row["valid_for_claim"]) for row in all_output_rows),
        len(all_output_rows),
    )
    add_validation(
        validation,
        "no_placeholder_tokens",
        "MISSING_"
        not in json.dumps(all_output_rows, sort_keys=True, default=str),
        len(all_output_rows),
    )
    if not all(row["passed"] for row in validation):
        failures = [row for row in validation if not row["passed"]]
        raise RuntimeError(f"validation failures: {failures}")
    provenance = [
        {
            "source_id": key,
            "source_type": "local_file",
            "source_path": str(path),
            "sha256": hashes_after[key],
            "status": "immutable_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    summary = {
        "force_audit": force_audit,
        "scores": scores,
        "spherical_q": float(spherical_score["corrected_q"]),
        "spherical_RMSE": float(
            spherical_score["corrected_velocity_squared_log10_RMSE"]
        ),
        "primary_delta_q_from_spherical": float(primary["corrected_q"])
        - float(spherical_score["corrected_q"]),
        "primary_delta_RMSE_from_spherical": float(
            primary["corrected_velocity_squared_log10_RMSE"]
        )
        - float(spherical_score["corrected_velocity_squared_log10_RMSE"]),
        "maximum_orientation_delta_q": maximum_orientation_delta,
        "time_refinement_delta_q": time_delta,
        "parent_q_lower": parent_lower,
        "parent_q_upper": parent_upper,
        "primary_q_gap": primary_gap,
        "spherical_q_gap": spherical_gap,
        "all_axis_compatible": all_axis_compatible,
        "robust_numerics": robust_numerics,
    }
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "summary": summary,
        "route_decision": route_decision,
        "validation_count": len(validation),
        "formalization_workbench_tree_sha256": formal_after,
        "valid_for_claim": False,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    Q.write_csv(CONTRACT_CSV, contract_rows())
    Q.write_csv(FORCE_AUDIT_CSV, force_audit_rows)
    Q.write_csv(SCORE_CSV, scores)
    Q.write_csv(CONTROL_CSV, controls)
    Q.write_csv(PROFILE_CSV, profile_rows)
    Q.write_csv(DECISION_CSV, decisions)
    Q.write_csv(PROVENANCE_CSV, provenance)
    Q.write_csv(VALIDATION_CSV, validation)
    Q.write_json(RESULT_JSON, result)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
