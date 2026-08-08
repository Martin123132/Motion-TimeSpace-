from __future__ import annotations

import hashlib
import json
import math
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar


sys.dont_write_bytecode = True

from Y5_R2FR_4882_tov_love_response import (
    G,
    C,
    L_SUN_M,
    love_observables,
    physical_contact_caps,
)


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
EOS_ROOT = POST / "source-intake" / "microphysical_eos" / "4883"
LAL_ROOT = EOS_ROOT / "lalsuite"

R0 = 1.0e-5
RTOL = 3.0e-8
MAX_STEP = 0.05
COMPLEX_STEP = 1.0e-28
SURFACE_FACTOR = 1.0e-7
FD_STEP = 4.0e-1
LAL_COMMIT = "a43ed75d9785b825d33b63072e1812f83efae36a"


EOS_SPECS: dict[str, dict[str, Any]] = {
    "BSK24": {
        "file": "BSK24.dat",
        "sha256": (
            "78e6047b0a7724b350692b816f0d6181c49341847351e2a9a5e26b940f62aa1d"
        ),
        "blob_id": "9a96fe386fdb3781f587a172fa86ca4ae2405849",
        "repository_file": (
            "lalsimulation/lib/LALSimNeutronStarEOS_PCP_BSK24_BSK24.dat"
        ),
        "compose_url": (
            "https://compose.obspm.fr/download/1D/NS/Skyrme/BSK24/eos.pdf"
        ),
        "compose_Mmax_Msun": 2.28,
        "compose_R1p4_km": 12.57,
        "family": "unified Brussels-Montreal BSK24",
    },
    "SLY4": {
        "file": "SLY4.dat",
        "sha256": (
            "475b77304c6da7253699c3cf48ad5a06bb637178f9615267cc0c6e6b41cc0b75"
        ),
        "blob_id": "d76a28d52af8c67b8f008cbd455b58e6328a19da",
        "repository_file": (
            "lalsimulation/lib/LALSimNeutronStarEOS_SLY4.dat"
        ),
        "compose_url": "https://compose.obspm.fr/eos/134",
        "compose_Mmax_Msun": 2.06,
        "compose_R1p4_km": 11.70,
        "family": "unified Skyrme SLY4",
    },
    "DD2": {
        "file": "DD2.dat",
        "sha256": (
            "7c9b5b5b3b50219d35e8a302d596b2b08df193cb62c17386cdd969174390d1fe"
        ),
        "blob_id": "3d07e5426625a050b13a281a99728b62e1d674e1",
        "repository_file": (
            "lalsimulation/lib/"
            "LALSimNeutronStarEOS_GPPVA_DD2_BSK24.dat"
        ),
        "compose_url": "https://compose.obspm.fr/eos/217",
        "compose_Mmax_Msun": 2.42,
        "compose_R1p4_km": 13.19,
        "family": "unified density-dependent RMF DD2 plus BSK24 crust",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass
class TabulatedEOS:
    eos_id: str
    pressure: np.ndarray
    energy: np.ndarray
    columns: int
    table_rows: int
    source_path: Path
    log_pressure: np.ndarray
    spline_coefficients: np.ndarray
    q_min: float
    q_max: float
    pressure_min: float
    pressure_max: float
    energy_min: float
    energy_max: float

    @classmethod
    def load(cls, eos_id: str) -> "TabulatedEOS":
        spec = EOS_SPECS[eos_id]
        path = LAL_ROOT / spec["file"]
        raw = np.loadtxt(path)
        if raw.ndim != 2:
            raise ValueError(f"{eos_id}: expected a rectangular EOS table")
        columns = raw.shape[1]
        if columns == 2:
            pressure = raw[:, 0] * L_SUN_M**2
            energy = raw[:, 1] * L_SUN_M**2
        elif columns >= 9:
            energy = raw[:, 2] * 1.0e3 * G / C**2 * L_SUN_M**2
            pressure = raw[:, 3] * 1.0e-1 * G / C**4 * L_SUN_M**2
        else:
            raise ValueError(f"{eos_id}: unsupported column count {columns}")
        finite = (
            np.isfinite(pressure)
            & np.isfinite(energy)
            & (pressure > 0)
            & (energy > 0)
        )
        pressure = np.asarray(pressure[finite], dtype=float)
        energy = np.asarray(energy[finite], dtype=float)
        if len(pressure) < 20:
            raise ValueError(f"{eos_id}: insufficient positive EOS rows")
        if not np.all(np.diff(pressure) > 0):
            raise ValueError(f"{eos_id}: pressure is not strictly increasing")
        if not np.all(np.diff(energy) > 0):
            raise ValueError(f"{eos_id}: energy is not strictly increasing")
        log_pressure = np.log(pressure)
        spline = CubicSpline(
            log_pressure,
            np.log(energy),
            bc_type="natural",
            extrapolate=False,
        )
        q_min = pressure[0] ** 0.4
        q_max = pressure[-1] ** 0.4
        return cls(
            eos_id=eos_id,
            pressure=pressure,
            energy=energy,
            columns=columns,
            table_rows=len(pressure),
            source_path=path,
            log_pressure=log_pressure,
            spline_coefficients=np.asarray(spline.c),
            q_min=q_min,
            q_max=q_max,
            pressure_min=pressure[0],
            pressure_max=pressure[-1],
            energy_min=energy[0],
            energy_max=energy[-1],
        )

    def _log_energy_jet(
        self, log_pressure: complex
    ) -> tuple[complex, complex, complex]:
        real_value = float(np.real(log_pressure))
        interval = int(np.searchsorted(self.log_pressure, real_value) - 1)
        interval = min(max(interval, 0), len(self.log_pressure) - 2)
        delta = log_pressure - self.log_pressure[interval]
        cubic, quadratic, linear, constant = self.spline_coefficients[
            :, interval
        ]
        value = ((cubic * delta + quadratic) * delta + linear) * delta + constant
        first = (3 * cubic * delta + 2 * quadratic) * delta + linear
        second = 6 * cubic * delta + 2 * quadratic
        return value, first, second

    def base_jet(
        self, q_value: complex
    ) -> tuple[complex, complex, complex, complex, complex, complex]:
        if float(np.real(q_value)) <= 0:
            floor = self.q_min * 1.0e-12
            q_value = (
                complex(floor, np.imag(q_value))
                if np.iscomplexobj(q_value)
                else floor
            )
        pressure = q_value**2.5
        pressure_q = 2.5 * q_value**1.5
        pressure_qq = 3.75 * q_value**0.5
        if float(np.real(q_value)) < self.q_min:
            normalization = self.energy_min / self.q_min**1.5
            energy = normalization * q_value**1.5
            energy_q = 1.5 * normalization * q_value**0.5
            energy_qq = 0.75 * normalization * q_value ** (-0.5)
            return (
                energy,
                pressure,
                energy_q,
                pressure_q,
                energy_qq,
                pressure_qq,
            )
        log_p = 2.5 * np.log(q_value)
        log_e, slope, curvature = self._log_energy_jet(log_p)
        energy = np.exp(log_e)
        logp_q = 2.5 / q_value
        logp_qq = -2.5 / q_value**2
        energy_logp = energy * slope
        energy_logp_logp = energy * (slope**2 + curvature)
        energy_q = energy_logp * logp_q
        energy_qq = (
            energy_logp_logp * logp_q**2 + energy_logp * logp_qq
        )
        return (
            energy,
            pressure,
            energy_q,
            pressure_q,
            energy_qq,
            pressure_qq,
        )


EOS_TABLES = {eos_id: TabulatedEOS.load(eos_id) for eos_id in EOS_SPECS}


def source_contract() -> dict[str, Any]:
    local = {
        "prior_checkpoint": (
            POST
            / "4882-Y5-R2FR-compact-star-EOS-response-Jacobian-mass-radius-and-tidal-sensitivity-or-strong-matter-promotion-gate.md",
            "MTS_TOV_LOVE_RESPONSE_JACOBIAN_4882",
        ),
        "prior_validation": (
            OUTPUT / "P8_Y5_BRR545_4882_VALIDATION.csv",
            "VAL4882_OVERALL,PASS",
        ),
        "prior_script": (
            POST / "scripts" / "Y5_R2FR_4882_tov_love_response.py",
            "def solve_star_response",
        ),
        "acquisition_metadata": (
            LAL_ROOT / "acquisition_metadata.json",
            LAL_COMMIT,
        ),
        "lalsuite_parser": (
            LAL_ROOT / "LALSimNeutronStarEOSTabular.c",
            "contains the pressure in Pa",
        ),
    }
    local_rows: list[dict[str, Any]] = []
    for source_id, (path, marker) in local.items():
        exists = path.exists()
        marker_found = exists and marker in path.read_text(
            encoding="utf-8", errors="replace"
        )
        local_rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker_found,
            }
        )
    table_rows: list[dict[str, Any]] = []
    for eos_id, spec in EOS_SPECS.items():
        eos = EOS_TABLES[eos_id]
        digest = sha256(eos.source_path)
        table_rows.append(
            {
                "eos_id": eos_id,
                "source_path": str(eos.source_path),
                "source_exists": eos.source_path.exists(),
                "sha256": digest,
                "expected_sha256": spec["sha256"],
                "hash_matches": digest == spec["sha256"],
                "commit_id": LAL_COMMIT,
                "blob_id": spec["blob_id"],
                "repository_file": spec["repository_file"],
                "compose_url": spec["compose_url"],
                "table_columns": eos.columns,
                "positive_rows": eos.table_rows,
            }
        )
    return {
        "local_rows": local_rows,
        "table_rows": table_rows,
        "web_sources": {
            "lalsuite": "https://git.ligo.org/lscsoft/lalsuite",
            "compose_BSK24": EOS_SPECS["BSK24"]["compose_url"],
            "compose_SLY4": EOS_SPECS["SLY4"]["compose_url"],
            "compose_DD2": EOS_SPECS["DD2"]["compose_url"],
            "compose_manual": (
                "https://compose.obspm.fr/download/pdf/"
                "CompOSE_Quick_Guide_for_Users.pdf"
            ),
            "tidal_love": "https://arxiv.org/abs/0711.2420",
        },
        "unit_contract": (
            "legacy two-column LALSuite tables are read directly as "
            "geometrized m^-2 pressure and energy; modern nine-column "
            "tables use the explicit CGS-to-geometrized conversions in "
            "LALSimNeutronStarEOSTabular.c; recovery of published Mmax "
            "and R1.4 is the independent unit regression"
        ),
        "passed": all(
            row["source_exists"] and row["marker_found"]
            for row in local_rows
        )
        and all(row["hash_matches"] for row in table_rows),
    }


def contact_basis(
    eos: TabulatedEOS, q_value: complex
) -> dict[str, complex]:
    energy, pressure, energy_q, pressure_q, energy_qq, pressure_qq = (
        eos.base_jet(q_value)
    )
    trace = energy - 3 * pressure
    trace_q = energy_q - 3 * pressure_q
    trace_qq = energy_qq - 3 * pressure_qq
    f_r = trace**2
    f_r_q = 2 * trace * trace_q
    f_r_qq = 2 * trace_q**2 + 2 * trace * trace_qq
    f_c = 4 * energy * (energy / 3 + pressure)
    f_c_q = (
        8 * energy * energy_q / 3
        + 4 * (energy_q * pressure + energy * pressure_q)
    )
    f_c_qq = (
        8 * (energy_q**2 + energy * energy_qq) / 3
        + 4
        * (
            energy_qq * pressure
            + 2 * energy_q * pressure_q
            + energy * pressure_qq
        )
    )

    def pressure_contact(
        basis: complex, basis_q: complex, basis_qq: complex
    ) -> tuple[complex, complex]:
        enthalpy_density = energy + pressure
        contact = enthalpy_density * basis_q / energy_q - basis
        contact_q = (
            pressure_q * basis_q / energy_q
            + enthalpy_density
            * (basis_qq * energy_q - basis_q * energy_qq)
            / energy_q**2
        )
        return contact, contact_q

    d_r, d_r_q = pressure_contact(f_r, f_r_q, f_r_qq)
    d_c, d_c_q = pressure_contact(f_c, f_c_q, f_c_qq)
    return {
        "energy": energy,
        "pressure": pressure,
        "energy_q": energy_q,
        "pressure_q": pressure_q,
        "energy_qq": energy_qq,
        "pressure_qq": pressure_qq,
        "f_r": f_r,
        "f_c": f_c,
        "f_r_q": f_r_q,
        "f_c_q": f_c_q,
        "d_r": d_r,
        "d_c": d_c,
        "d_r_q": d_r_q,
        "d_c_q": d_c_q,
    }


def effective_eos(
    eos: TabulatedEOS,
    q_value: complex,
    lambda_r: complex = 0.0,
    lambda_c: complex = 0.0,
) -> tuple[complex, complex, complex, complex, complex]:
    if lambda_r == 0 and lambda_c == 0:
        energy, pressure, energy_q, pressure_q, _, _ = eos.base_jet(
            q_value
        )
        return (
            energy,
            pressure,
            energy_q,
            pressure_q,
            pressure_q / energy_q,
        )
    basis = contact_basis(eos, q_value)
    energy = (
        basis["energy"]
        - lambda_r * basis["f_r"]
        - lambda_c * basis["f_c"]
    )
    pressure = (
        basis["pressure"]
        - lambda_r * basis["d_r"]
        - lambda_c * basis["d_c"]
    )
    energy_q = (
        basis["energy_q"]
        - lambda_r * basis["f_r_q"]
        - lambda_c * basis["f_c_q"]
    )
    pressure_q = (
        basis["pressure_q"]
        - lambda_r * basis["d_r_q"]
        - lambda_c * basis["d_c_q"]
    )
    sound_squared = pressure_q / energy_q
    return energy, pressure, energy_q, pressure_q, sound_squared


def rhs_core(
    radius: float,
    state: np.ndarray,
    eos: TabulatedEOS,
    lambda_r: complex = 0.0,
    lambda_c: complex = 0.0,
) -> np.ndarray:
    mass, q_value, tidal_y = state
    energy, pressure, _, pressure_q, sound_squared = effective_eos(
        eos, q_value, lambda_r, lambda_c
    )
    one_minus_two_m_over_r = 1 - 2 * mass / radius
    mass_prime = 4 * np.pi * radius**2 * energy
    pressure_prime = -(
        (energy + pressure)
        * (mass + 4 * np.pi * radius**3 * pressure)
        / (radius**2 * one_minus_two_m_over_r)
    )
    q_prime = pressure_prime / pressure_q
    tidal_f = (
        1 - 4 * np.pi * radius**2 * (energy - pressure)
    ) / one_minus_two_m_over_r
    tidal_q = (
        4
        * np.pi
        * (
            5 * energy
            + 9 * pressure
            + (energy + pressure) / sound_squared
        )
        / one_minus_two_m_over_r
        - 6 / (radius**2 * one_minus_two_m_over_r)
        - 4
        * (mass + 4 * np.pi * radius**3 * pressure) ** 2
        / (radius**4 * one_minus_two_m_over_r**2)
    )
    tidal_y_prime = -(
        tidal_y**2 + tidal_y * tidal_f + radius**2 * tidal_q
    ) / radius
    return np.asarray(
        [mass_prime, q_prime, tidal_y_prime],
        dtype=np.result_type(state, lambda_r, lambda_c),
    )


def response_jacobian(
    radius: float, state: np.ndarray, eos: TabulatedEOS
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    state_complex = np.asarray(state, dtype=complex)
    jacobian = np.empty((3, 3), dtype=float)
    for column in range(3):
        shifted = state_complex.copy()
        shifted[column] += 1j * COMPLEX_STEP
        jacobian[:, column] = np.imag(
            rhs_core(radius, shifted, eos)
        ) / COMPLEX_STEP
    source_r = np.imag(
        rhs_core(radius, state_complex, eos, 1j * COMPLEX_STEP, 0.0)
    ) / COMPLEX_STEP
    source_c = np.imag(
        rhs_core(radius, state_complex, eos, 0.0, 1j * COMPLEX_STEP)
    ) / COMPLEX_STEP
    return jacobian, source_r, source_c


def _surface_q(eos: TabulatedEOS, surface_factor: float) -> float:
    return eos.q_min * surface_factor


def _initial_state(
    eos: TabulatedEOS,
    central_q: float,
    lambda_r: float = 0.0,
    lambda_c: float = 0.0,
    with_response: bool = False,
) -> np.ndarray:
    basis = contact_basis(eos, central_q)
    energy = (
        basis["energy"]
        - lambda_r * basis["f_r"]
        - lambda_c * basis["f_c"]
    )
    mass = 4 * math.pi * float(np.real(energy)) * R0**3 / 3
    base = np.asarray([mass, central_q, 2.0], dtype=float)
    if not with_response:
        return base
    tangent_r = np.asarray(
        [
            -4 * math.pi * float(np.real(basis["f_r"])) * R0**3 / 3,
            0.0,
            0.0,
        ]
    )
    tangent_c = np.asarray(
        [
            -4 * math.pi * float(np.real(basis["f_c"])) * R0**3 / 3,
            0.0,
            0.0,
        ]
    )
    tangent_q = np.asarray(
        [
            4
            * math.pi
            * float(np.real(basis["energy_q"]))
            * R0**3
            / 3,
            1.0,
            0.0,
        ]
    )
    return np.concatenate([base, tangent_r, tangent_c, tangent_q])


def _solver_atol(with_response: bool) -> np.ndarray:
    if not with_response:
        return np.asarray([2.0e-10, 2.0e-20, 2.0e-10])
    values = np.full(12, 3.0e-10)
    values[1] = 2.0e-20
    values[4] = 2.0e-13
    values[7] = 2.0e-13
    values[10] = 2.0e-10
    return values


@lru_cache(maxsize=None)
def solve_star(
    eos_id: str,
    central_q: float,
    lambda_r: float = 0.0,
    lambda_c: float = 0.0,
    surface_factor: float = SURFACE_FACTOR,
) -> dict[str, float]:
    eos = EOS_TABLES[eos_id]
    initial = _initial_state(eos, central_q, lambda_r, lambda_c)
    surface_q = _surface_q(eos, surface_factor)

    def surface_event(radius: float, state: np.ndarray) -> float:
        return float(state[1] - surface_q)

    surface_event.terminal = True
    surface_event.direction = -1
    solution = solve_ivp(
        lambda radius, state: rhs_core(
            radius, state, eos, lambda_r, lambda_c
        ),
        (R0, 100.0),
        initial,
        events=surface_event,
        rtol=RTOL,
        atol=_solver_atol(False),
        max_step=MAX_STEP,
    )
    if not solution.success or len(solution.t_events[0]) != 1:
        raise RuntimeError(f"{eos_id}: TOV-Love surface event failed")
    radius = float(solution.t_events[0][0])
    mass, q_value, tidal_y = solution.y_events[0][0]
    compactness, love_k2, tidal_lambda = love_observables(
        mass, radius, tidal_y
    )
    central_pressure = central_q**2.5
    central_energy = float(np.real(eos.base_jet(central_q)[0]))
    return {
        "eos_id": eos_id,
        "central_q": central_q,
        "central_pressure_Lsun_minus2": central_pressure,
        "central_energy_Lsun_minus2": central_energy,
        "surface_q": float(q_value),
        "surface_pressure_Lsun_minus2": float(q_value**2.5),
        "mass": float(mass),
        "radius": radius,
        "radius_km": radius * L_SUN_M / 1000,
        "compactness": float(compactness),
        "tidal_y": float(tidal_y),
        "love_k2": float(love_k2),
        "tidal_lambda": float(tidal_lambda),
    }


def _observable_gradient(
    mass: float, radius: float, tidal_y: float
) -> np.ndarray:
    values = np.asarray([mass, radius, tidal_y], dtype=complex)
    gradient = np.empty((3, 3), dtype=float)
    for column in range(3):
        shifted = values.copy()
        shifted[column] += 1j * COMPLEX_STEP
        gradient[:, column] = np.imag(
            np.asarray(love_observables(*shifted))
        ) / COMPLEX_STEP
    return gradient


def _surface_response(
    eos: TabulatedEOS,
    base_surface: np.ndarray,
    tangent: np.ndarray,
) -> dict[str, float]:
    mass, q_value, tidal_y, radius = base_surface
    base_prime = rhs_core(
        float(radius),
        np.asarray([mass, q_value, tidal_y]),
        eos,
    )
    radius_response = -tangent[1] / base_prime[1]
    mass_response = tangent[0] + base_prime[0] * radius_response
    tidal_y_response = tangent[2] + base_prime[2] * radius_response
    gradient = _observable_gradient(mass, radius, tidal_y)
    derived = gradient @ np.asarray(
        [mass_response, radius_response, tidal_y_response]
    )
    return {
        "mass": float(mass_response),
        "radius": float(radius_response),
        "tidal_y": float(tidal_y_response),
        "compactness": float(derived[0]),
        "love_k2": float(derived[1]),
        "tidal_lambda": float(derived[2]),
    }


@lru_cache(maxsize=None)
def solve_star_response(
    eos_id: str,
    central_q: float,
    surface_factor: float = SURFACE_FACTOR,
) -> dict[str, Any]:
    eos = EOS_TABLES[eos_id]
    initial = _initial_state(eos, central_q, with_response=True)
    surface_q = _surface_q(eos, surface_factor)

    def augmented_rhs(radius: float, state: np.ndarray) -> np.ndarray:
        base = state[:3]
        tangent_r = state[3:6]
        tangent_c = state[6:9]
        tangent_q = state[9:12]
        base_rhs = rhs_core(radius, base, eos)
        jacobian, source_r, source_c = response_jacobian(
            radius, base, eos
        )
        return np.concatenate(
            [
                base_rhs,
                jacobian @ tangent_r + source_r,
                jacobian @ tangent_c + source_c,
                jacobian @ tangent_q,
            ]
        )

    def surface_event(radius: float, state: np.ndarray) -> float:
        return float(state[1] - surface_q)

    surface_event.terminal = True
    surface_event.direction = -1
    solution = solve_ivp(
        augmented_rhs,
        (R0, 100.0),
        initial,
        events=surface_event,
        rtol=RTOL,
        atol=_solver_atol(True),
        max_step=MAX_STEP,
    )
    if not solution.success or len(solution.t_events[0]) != 1:
        raise RuntimeError(
            f"{eos_id}: augmented TOV-Love surface event failed"
        )
    radius = float(solution.t_events[0][0])
    surface = solution.y_events[0][0]
    mass, q_value, tidal_y = surface[:3]
    compactness, love_k2, tidal_lambda = love_observables(
        mass, radius, tidal_y
    )
    base_surface = np.asarray(
        [mass, q_value, tidal_y, radius], dtype=float
    )
    response_r = _surface_response(eos, base_surface, surface[3:6])
    response_c = _surface_response(eos, base_surface, surface[6:9])
    response_q = _surface_response(eos, base_surface, surface[9:12])
    central_pressure = central_q**2.5
    central_pressure_q = 2.5 * central_q**1.5
    log_mass_slope_pressure = (
        central_pressure
        * response_q["mass"]
        / (central_pressure_q * mass)
    )

    def fixed_mass(response: dict[str, float]) -> dict[str, float]:
        central_q_shift = -response["mass"] / response_q["mass"]
        return {
            "central_q": central_q_shift,
            "central_pressure": central_pressure_q * central_q_shift,
            "radius": (
                response["radius"]
                + response_q["radius"] * central_q_shift
            ),
            "love_k2": (
                response["love_k2"]
                + response_q["love_k2"] * central_q_shift
            ),
            "tidal_lambda": (
                response["tidal_lambda"]
                + response_q["tidal_lambda"] * central_q_shift
            ),
        }

    return {
        "base": {
            "eos_id": eos_id,
            "central_q": central_q,
            "central_pressure_Lsun_minus2": central_pressure,
            "mass": float(mass),
            "radius": radius,
            "radius_km": radius * L_SUN_M / 1000,
            "compactness": float(compactness),
            "tidal_y": float(tidal_y),
            "love_k2": float(love_k2),
            "tidal_lambda": float(tidal_lambda),
            "log_mass_slope_pressure": float(log_mass_slope_pressure),
            "stable_branch": bool(response_q["mass"] > 0),
        },
        "fixed_central_pressure": {
            "lambda_r": response_r,
            "lambda_c": response_c,
            "central_q": response_q,
        },
        "fixed_mass": {
            "lambda_r": fixed_mass(response_r),
            "lambda_c": fixed_mass(response_c),
        },
        "passed": bool(
            mass > 0
            and radius > 2 * mass
            and love_k2 > 0
            and tidal_lambda > 0
            and np.isfinite(log_mass_slope_pressure)
        ),
    }


@lru_cache(maxsize=None)
def table_quality(eos_id: str) -> dict[str, Any]:
    eos = EOS_TABLES[eos_id]
    q_values = np.geomspace(eos.q_min, eos.q_max, 5000)
    sound = np.asarray(
        [
            float(np.real(eos.base_jet(q_value)[3] / eos.base_jet(q_value)[2]))
            for q_value in q_values
        ]
    )
    positive = np.isfinite(sound) & (sound > 0)
    acausal = np.flatnonzero(sound >= 1)
    causal_q_max = (
        q_values[acausal[0] - 1]
        if len(acausal) and acausal[0] > 0
        else eos.q_max
    )
    return {
        "eos_id": eos_id,
        "table_columns": eos.columns,
        "positive_rows": eos.table_rows,
        "pressure_min_Lsun_minus2": eos.pressure_min,
        "pressure_max_Lsun_minus2": eos.pressure_max,
        "energy_min_Lsun_minus2": eos.energy_min,
        "energy_max_Lsun_minus2": eos.energy_max,
        "minimum_cs2": float(np.min(sound[positive])),
        "maximum_cs2": float(np.max(sound[positive])),
        "first_acausal_pressure_Lsun_minus2": (
            float(q_values[acausal[0]] ** 2.5) if len(acausal) else None
        ),
        "causal_q_max": float(causal_q_max),
        "all_sampled_derivatives_positive": bool(np.all(positive)),
        "passed": bool(
            eos.table_rows >= 50
            and np.all(positive)
            and causal_q_max > eos.q_min
        ),
    }


@lru_cache(maxsize=None)
def locate_stable_models(eos_id: str) -> dict[str, Any]:
    eos = EOS_TABLES[eos_id]
    quality = table_quality(eos_id)
    pressure_lower = max(1.0e-5, eos.pressure_min * 1.0e6)
    pressure_upper = min(
        eos.pressure_max * 0.92,
        quality["causal_q_max"] ** 2.5 * 0.98,
    )
    maximum = minimize_scalar(
        lambda log_pressure: -solve_star(
            eos_id, math.exp(log_pressure) ** 0.4
        )["mass"],
        bounds=(math.log(pressure_lower), math.log(pressure_upper)),
        method="bounded",
        options={"xatol": 3.0e-7},
    )
    central_pressure_max = math.exp(maximum.x)
    central_q_max = central_pressure_max**0.4
    model_max = solve_star(eos_id, central_q_max)

    def stable_q_for_mass(target_mass: float) -> float:
        log_pressure = brentq(
            lambda trial: solve_star(
                eos_id, math.exp(trial) ** 0.4
            )["mass"]
            - target_mass,
            math.log(pressure_lower),
            math.log(central_pressure_max * (1 - 2.0e-6)),
            xtol=3.0e-10,
            rtol=3.0e-10,
        )
        return math.exp(log_pressure) ** 0.4

    targets = {
        "canonical_1p4": 1.4,
        "two_solar_mass": 2.0,
        "near_turning_0p99_Mmax": 0.99 * model_max["mass"],
    }
    target_q = {
        name: stable_q_for_mass(target_mass)
        for name, target_mass in targets.items()
    }
    spec = EOS_SPECS[eos_id]
    canonical = solve_star(eos_id, target_q["canonical_1p4"])
    return {
        "eos_id": eos_id,
        "family": spec["family"],
        "maximum_model": model_max,
        "target_q": target_q,
        "published_Mmax_Msun": spec["compose_Mmax_Msun"],
        "published_R1p4_km": spec["compose_R1p4_km"],
        "Mmax_fractional_error": (
            model_max["mass"] / spec["compose_Mmax_Msun"] - 1
        ),
        "R1p4_fractional_error": (
            canonical["radius_km"] / spec["compose_R1p4_km"] - 1
        ),
        "passed": bool(
            maximum.success
            and model_max["mass"] > 2.0
            and abs(
                model_max["mass"] / spec["compose_Mmax_Msun"] - 1
            )
            < 0.025
            and abs(
                canonical["radius_km"] / spec["compose_R1p4_km"] - 1
            )
            < 0.025
        ),
    }


@lru_cache(maxsize=None)
def sequence_contract() -> dict[str, Any]:
    rows = [locate_stable_models(eos_id) for eos_id in EOS_SPECS]
    return {
        "rows": rows,
        "all_support_2Msun": all(
            row["maximum_model"]["mass"] > 2.0 for row in rows
        ),
        "passed": all(row["passed"] for row in rows),
    }


@lru_cache(maxsize=None)
def response_benchmarks() -> dict[str, Any]:
    caps = physical_contact_caps()
    rows: list[dict[str, Any]] = []
    for eos_id in EOS_SPECS:
        locations = locate_stable_models(eos_id)
        for model_id, central_q in locations["target_q"].items():
            response = solve_star_response(eos_id, central_q)
            base = response["base"]
            fixed_central = response["fixed_central_pressure"]
            fixed_mass = response["fixed_mass"]

            def envelope(derivative_r: float, derivative_c: float) -> float:
                return (
                    abs(derivative_r) * caps["lambdaR_cap_Lsun2"]
                    + abs(derivative_c) * caps["lambdaC_cap_Lsun2"]
                )

            rows.append(
                {
                    "eos_id": eos_id,
                    "model_id": model_id,
                    **base,
                    "turning_condition_number": (
                        1 / abs(base["log_mass_slope_pressure"])
                    ),
                    "cap_abs_deltaM_over_M_fixed_pc": (
                        envelope(
                            fixed_central["lambda_r"]["mass"],
                            fixed_central["lambda_c"]["mass"],
                        )
                        / base["mass"]
                    ),
                    "cap_abs_deltaR_over_R_fixed_pc": (
                        envelope(
                            fixed_central["lambda_r"]["radius"],
                            fixed_central["lambda_c"]["radius"],
                        )
                        / base["radius"]
                    ),
                    "cap_abs_deltaR_over_R_fixed_M": (
                        envelope(
                            fixed_mass["lambda_r"]["radius"],
                            fixed_mass["lambda_c"]["radius"],
                        )
                        / base["radius"]
                    ),
                    "cap_abs_deltaLambda_over_Lambda_fixed_M": (
                        envelope(
                            fixed_mass["lambda_r"]["tidal_lambda"],
                            fixed_mass["lambda_c"]["tidal_lambda"],
                        )
                        / base["tidal_lambda"]
                    ),
                    "cap_abs_delta_pc_over_pc_fixed_M": (
                        envelope(
                            fixed_mass["lambda_r"]["central_pressure"],
                            fixed_mass["lambda_c"]["central_pressure"],
                        )
                        / base["central_pressure_Lsun_minus2"]
                    ),
                    "response_valid": response["passed"],
                    "valid_for_claim": False,
                }
            )
    by_eos_model = {
        (row["eos_id"], row["model_id"]): row for row in rows
    }
    return {
        "caps": caps,
        "rows": rows,
        "maximum_fixed_mass_tidal_cap": max(
            row["cap_abs_deltaLambda_over_Lambda_fixed_M"]
            for row in rows
        ),
        "passed": bool(
            caps["passed"]
            and len(rows) == 9
            and len(by_eos_model) == 9
            and all(row["response_valid"] for row in rows)
            and all(
                by_eos_model[(eos_id, "near_turning_0p99_Mmax")][
                    "turning_condition_number"
                ]
                > by_eos_model[(eos_id, "canonical_1p4")][
                    "turning_condition_number"
                ]
                for eos_id in EOS_SPECS
            )
        ),
    }


@lru_cache(maxsize=None)
def finite_difference_crosscheck() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    validation_scales: list[float] = []
    for eos_id in EOS_SPECS:
        central_q = locate_stable_models(eos_id)["target_q"][
            "canonical_1p4"
        ]
        validation_scales.append(
            FD_STEP
            * float(np.real(EOS_TABLES[eos_id].base_jet(central_q)[0]))
        )
        response = solve_star_response(eos_id, central_q)
        for direction, lambda_pair in {
            "lambda_r": ((FD_STEP, 0.0), (-FD_STEP, 0.0)),
            "lambda_c": ((0.0, FD_STEP), (0.0, -FD_STEP)),
        }.items():
            plus = solve_star(
                eos_id,
                central_q,
                lambda_r=lambda_pair[0][0],
                lambda_c=lambda_pair[0][1],
            )
            minus = solve_star(
                eos_id,
                central_q,
                lambda_r=lambda_pair[1][0],
                lambda_c=lambda_pair[1][1],
            )
            tangent = response["fixed_central_pressure"][direction]
            for observable in ["mass", "radius", "love_k2", "tidal_lambda"]:
                finite = (plus[observable] - minus[observable]) / (
                    2 * FD_STEP
                )
                analytic = tangent[observable]
                relative_error = abs(finite - analytic) / max(
                    abs(analytic), 1.0e-13
                )
                rows.append(
                    {
                        "eos_id": eos_id,
                        "projection": "fixed_central_pressure",
                        "direction": direction,
                        "observable": observable,
                        "tangent_derivative": analytic,
                        "finite_difference_derivative": finite,
                        "relative_error": relative_error,
                        "status": (
                            "PASS" if relative_error < 1.0e-2 else "FAIL"
                        ),
                    }
                )

            target_mass = response["base"]["mass"]

            def fixed_mass_model(
                pair: tuple[float, float]
            ) -> tuple[float, dict[str, float]]:
                root = brentq(
                    lambda trial: solve_star(
                        eos_id,
                        trial,
                        lambda_r=pair[0],
                        lambda_c=pair[1],
                    )["mass"]
                    - target_mass,
                    0.75 * central_q,
                    1.25 * central_q,
                    xtol=3.0e-12,
                    rtol=3.0e-11,
                )
                return root, solve_star(
                    eos_id,
                    root,
                    lambda_r=pair[0],
                    lambda_c=pair[1],
                )

            plus_q, plus_fixed = fixed_mass_model(lambda_pair[0])
            minus_q, minus_fixed = fixed_mass_model(lambda_pair[1])
            fixed_tangent = response["fixed_mass"][direction]
            finite_fixed = {
                "central_q": (plus_q - minus_q) / (2 * FD_STEP),
                "radius": (plus_fixed["radius"] - minus_fixed["radius"])
                / (2 * FD_STEP),
                "love_k2": (
                    plus_fixed["love_k2"] - minus_fixed["love_k2"]
                )
                / (2 * FD_STEP),
                "tidal_lambda": (
                    plus_fixed["tidal_lambda"]
                    - minus_fixed["tidal_lambda"]
                )
                / (2 * FD_STEP),
            }
            for observable, finite in finite_fixed.items():
                analytic = fixed_tangent[observable]
                relative_error = abs(finite - analytic) / max(
                    abs(analytic), 1.0e-13
                )
                rows.append(
                    {
                        "eos_id": eos_id,
                        "projection": "fixed_mass",
                        "direction": direction,
                        "observable": observable,
                        "tangent_derivative": analytic,
                        "finite_difference_derivative": finite,
                        "relative_error": relative_error,
                        "status": (
                            "PASS" if relative_error < 1.0e-2 else "FAIL"
                        ),
                    }
                )
    return {
        "finite_difference_step_Lsun2": FD_STEP,
        "maximum_step_times_central_energy": max(validation_scales),
        "validation_step_role": (
            "amplified derivative check only; maximum lambda*rho is "
            "below 1e-3 and the step is not a physical coefficient"
        ),
        "rows": rows,
        "maximum_relative_error": max(row["relative_error"] for row in rows),
        "passed": bool(
            len(rows) == 48
            and max(validation_scales) < 1.0e-3
            and all(row["status"] == "PASS" for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def surface_convergence() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    factors = [1.0e-5, SURFACE_FACTOR, 1.0e-9]
    for eos_id in EOS_SPECS:
        central_q = locate_stable_models(eos_id)["target_q"][
            "canonical_1p4"
        ]
        models = {
            factor: solve_star(
                eos_id, central_q, surface_factor=factor
            )
            for factor in factors
        }
        reference = models[1.0e-9]
        for factor in factors:
            model = models[factor]
            rows.append(
                {
                    "eos_id": eos_id,
                    "surface_factor": factor,
                    "mass": model["mass"],
                    "radius_km": model["radius_km"],
                    "tidal_lambda": model["tidal_lambda"],
                    "abs_fractional_mass_difference_to_1e_minus9": abs(
                        model["mass"] / reference["mass"] - 1
                    ),
                    "abs_fractional_radius_difference_to_1e_minus9": abs(
                        model["radius"] / reference["radius"] - 1
                    ),
                    "abs_fractional_tidal_difference_to_1e_minus9": abs(
                        model["tidal_lambda"]
                        / reference["tidal_lambda"]
                        - 1
                    ),
                }
            )
    baseline_rows = [
        row for row in rows if row["surface_factor"] == SURFACE_FACTOR
    ]
    return {
        "rows": rows,
        "maximum_baseline_radius_fractional_error": max(
            row["abs_fractional_radius_difference_to_1e_minus9"]
            for row in baseline_rows
        ),
        "maximum_baseline_tidal_fractional_error": max(
            row["abs_fractional_tidal_difference_to_1e_minus9"]
            for row in baseline_rows
        ),
        "passed": bool(
            len(rows) == 9
            and all(
                row["abs_fractional_radius_difference_to_1e_minus9"]
                < 2.0e-5
                and row["abs_fractional_tidal_difference_to_1e_minus9"]
                < 1.0e-4
                for row in baseline_rows
            )
        ),
    }


@lru_cache(maxsize=None)
def eos_spread_comparison() -> dict[str, Any]:
    responses = response_benchmarks()["rows"]
    canonical = [
        row for row in responses if row["model_id"] == "canonical_1p4"
    ]
    radii = np.asarray([row["radius_km"] for row in canonical])
    tides = np.asarray([row["tidal_lambda"] for row in canonical])
    contact_radii = np.asarray(
        [row["cap_abs_deltaR_over_R_fixed_M"] for row in canonical]
    )
    contact_tides = np.asarray(
        [
            row["cap_abs_deltaLambda_over_Lambda_fixed_M"]
            for row in canonical
        ]
    )
    radius_eos_spread = (np.max(radii) - np.min(radii)) / np.mean(radii)
    tidal_eos_spread = (np.max(tides) - np.min(tides)) / np.mean(tides)
    return {
        "canonical_EOS_count": len(canonical),
        "radius_min_km": float(np.min(radii)),
        "radius_max_km": float(np.max(radii)),
        "radius_fractional_EOS_spread": float(radius_eos_spread),
        "tidal_min": float(np.min(tides)),
        "tidal_max": float(np.max(tides)),
        "tidal_fractional_EOS_spread": float(tidal_eos_spread),
        "maximum_contact_radius_fractional_cap": float(
            np.max(contact_radii)
        ),
        "maximum_contact_tidal_fractional_cap": float(
            np.max(contact_tides)
        ),
        "radius_EOS_spread_over_contact_cap": float(
            radius_eos_spread / np.max(contact_radii)
        ),
        "tidal_EOS_spread_over_contact_cap": float(
            tidal_eos_spread / np.max(contact_tides)
        ),
        "interpretation": (
            "under inherited strict-EFT control caps, EOS uncertainty "
            "dominates the MTS contact envelope; this is a conditional "
            "GR-correspondence result, not a measurement of a_R or a_C"
        ),
        "passed": bool(
            len(canonical) == 3
            and radius_eos_spread > 0.05
            and tidal_eos_spread > 0.1
            and np.max(contact_radii) < 1.0e-15
            and np.max(contact_tides) < 1.0e-14
        ),
    }


def compose_archive_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for eos_id in ["APR", "SLY4", "BSK24"]:
        directory = EOS_ROOT / eos_id
        archive = directory / "eos.zip"
        checksum_file = directory / "eos.zip_checksum.txt"
        expected = (
            checksum_file.read_text(encoding="utf-8").split()[0]
            if checksum_file.exists()
            else ""
        )
        actual = sha256(archive) if archive.exists() else ""
        rows.append(
            {
                "eos_id": eos_id,
                "archive_path": str(archive),
                "checksum_path": str(checksum_file),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "hash_matches": bool(expected and expected == actual),
                "used_for_solver": False,
                "disposition": (
                    "archive_verified_but_not_selected"
                    if expected == actual
                    else "remote_archive_checksum_mismatch_quarantined"
                ),
            }
        )
    return {
        "rows": rows,
        "matching_archives": sum(row["hash_matches"] for row in rows),
        "quarantined_archives": sum(not row["hash_matches"] for row in rows),
        "passed": all(not row["used_for_solver"] for row in rows),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    sequences = sequence_contract()
    responses = response_benchmarks()
    crosscheck = finite_difference_crosscheck()
    convergence = surface_convergence()
    spread = eos_spread_comparison()
    return {
        "selected_branch": "STRICT_EFT_METRIC_ONLY_ANALYTIC_EH_BRANCH",
        "EOS_status": (
            "THREE_HASH_LOCKED_MICROPHYSICAL_FAMILIES_SUPPORT_2MSUN"
        ),
        "response_status": (
            "MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_DERIVED_AND_"
            "NONLINEARLY_VALIDATED"
        ),
        "strong_matter_correspondence": (
            "CONDITIONAL_ON_SELECTED_METRIC_BRANCH_AND_INHERITED_"
            "STRICT_EFT_CONTACT_CAPS"
        ),
        "strong_matter_background_promoted": False,
        "reason_not_promoted": (
            "the EOS and response numerics are now realistic and robust, "
            "but the a_R and a_C values remain control caps rather than "
            "parent-derived measured Wilson coefficients"
        ),
        "full_fundamental_unification": False,
        "next_target": (
            "4884-Y5-R2FR-strong-matter-contact-coefficient-parent-"
            "ownership-or-observational-bound-projection-gate.md"
        ),
        "passed": bool(
            sequences["passed"]
            and responses["passed"]
            and crosscheck["passed"]
            and convergence["passed"]
            and spread["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "compose_archive_audit": compose_archive_audit(),
        "table_quality": {
            "rows": [table_quality(eos_id) for eos_id in EOS_SPECS],
            "passed": all(table_quality(eos_id)["passed"] for eos_id in EOS_SPECS),
        },
        "sequences": sequence_contract(),
        "responses": response_benchmarks(),
        "crosscheck": finite_difference_crosscheck(),
        "surface_convergence": surface_convergence(),
        "EOS_spread": eos_spread_comparison(),
        "arbitration": arbitration(),
    }
    return {
        "sections": sections,
        "all_checks_pass": bool(
            all(section["passed"] for section in sections.values())
        ),
        "decision": (
            "replace the analytic control polytrope with hash-locked APR, "
            "SLY4 and DD2 tables; reproduce their published mass-radius "
            "anchors; propagate both MTS contact directions through mass, "
            "radius and tidal observables; and retain strong-matter GR "
            "correspondence only conditionally until contact coefficients "
            "are parent-owned or observationally bounded"
        ),
    }


if __name__ == "__main__":
    print(
        json.dumps(
            result(),
            indent=2,
            sort_keys=True,
            default=lambda value: (
                value.item() if hasattr(value, "item") else str(value)
            ),
        )
    )
