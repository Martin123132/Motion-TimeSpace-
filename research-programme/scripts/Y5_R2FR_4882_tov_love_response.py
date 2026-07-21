from __future__ import annotations

import json
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar


sys.dont_write_bytecode = True

from Y5_R2FR_4878_local_eft_arena_bounds import (
    LBAR_P2,
    strict_eft_contact_branch,
)


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

C = 299_792_458.0
G = 6.67430e-11
M_SUN_KG = 1.98847e30
L_SUN_M = G * M_SUN_KG / C**2
EOS_K = 100.0
EOS_GAMMA = 2.0
R0 = 1.0e-5
RTOL = 2.0e-9
ATOL = 2.0e-11
MAX_STEP = 0.03
COMPLEX_STEP = 1.0e-28


def source_contract() -> dict[str, Any]:
    sources = {
        "prior_checkpoint": (
            POST
            / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
        ),
        "prior_validation": (
            OUTPUT / "P8_Y5_BRR545_4881_VALIDATION.csv",
            "VAL4881_OVERALL,PASS",
        ),
        "prior_script": (
            POST / "scripts" / "Y5_R2FR_4881_compact_fluid_a6.py",
            "def corrected_tov_map",
        ),
        "strong_field_domain": (
            POST
            / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
        "tolman_background_regression": (
            POST / "scripts" / "Y5_R2FR_4868_fixed_background_variational_remainder.py",
            "def tolman_vii_background",
        ),
    }
    rows: list[dict[str, Any]] = []
    for source_id, (path, marker) in sources.items():
        exists = path.exists()
        marker_found = exists and marker in path.read_text(
            encoding="utf-8", errors="replace"
        )
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker_found,
            }
        )
    return {
        "local_rows": rows,
        "web_sources": {
            "tidal_love": "https://arxiv.org/abs/0711.2420",
            "piecewise_polytropes": "https://arxiv.org/abs/0812.2163",
            "love_surface_guard": "https://arxiv.org/abs/1004.5098",
        },
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


def base_eos(number_density: complex, k_eos: float = EOS_K) -> tuple[complex, ...]:
    pressure = k_eos * number_density**2
    energy = number_density + pressure
    pressure_n = 2 * k_eos * number_density
    energy_n = 1 + 2 * k_eos * number_density
    pressure_nn = 2 * k_eos
    energy_nn = 2 * k_eos
    return energy, pressure, energy_n, pressure_n, energy_nn, pressure_nn


def contact_basis(number_density: complex, k_eos: float = EOS_K) -> dict[str, complex]:
    energy, pressure, energy_n, pressure_n, energy_nn, pressure_nn = (
        base_eos(number_density, k_eos)
    )
    trace_energy = energy - 3 * pressure
    trace_n = energy_n - 3 * pressure_n
    trace_nn = energy_nn - 3 * pressure_nn
    f_r = trace_energy**2
    f_r_n = 2 * trace_energy * trace_n
    f_r_nn = 2 * trace_n**2 + 2 * trace_energy * trace_nn
    f_c = 4 * energy * (energy / 3 + pressure)
    f_c_n = (
        8 * energy * energy_n / 3
        + 4 * (energy_n * pressure + energy * pressure_n)
    )
    f_c_nn = (
        8 * (energy_n**2 + energy * energy_nn) / 3
        + 4
        * (
            energy_nn * pressure
            + 2 * energy_n * pressure_n
            + energy * pressure_nn
        )
    )
    d_r = number_density * f_r_n - f_r
    d_c = number_density * f_c_n - f_c
    return {
        "energy": energy,
        "pressure": pressure,
        "energy_n": energy_n,
        "pressure_n": pressure_n,
        "f_r": f_r,
        "f_c": f_c,
        "f_r_n": f_r_n,
        "f_c_n": f_c_n,
        "f_r_nn": f_r_nn,
        "f_c_nn": f_c_nn,
        "d_r": d_r,
        "d_c": d_c,
    }


def effective_eos(
    number_density: complex,
    lambda_r: complex = 0.0,
    lambda_c: complex = 0.0,
    k_eos: float = EOS_K,
) -> tuple[complex, complex, complex, complex, complex]:
    basis = contact_basis(number_density, k_eos)
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
    energy_n = (
        basis["energy_n"]
        - lambda_r * basis["f_r_n"]
        - lambda_c * basis["f_c_n"]
    )
    pressure_n = (
        basis["pressure_n"]
        - lambda_r * number_density * basis["f_r_nn"]
        - lambda_c * number_density * basis["f_c_nn"]
    )
    sound_squared = pressure_n / energy_n
    return energy, pressure, energy_n, pressure_n, sound_squared


def love_observables(
    mass: complex, radius: complex, y_surface: complex
) -> tuple[complex, complex, complex]:
    compactness = mass / radius
    numerator = (
        8
        * compactness**5
        / 5
        * (1 - 2 * compactness) ** 2
        * (
            2
            + 2 * compactness * (y_surface - 1)
            - y_surface
        )
    )
    denominator = (
        2
        * compactness
        * (
            6
            - 3 * y_surface
            + 3 * compactness * (5 * y_surface - 8)
        )
        + 4
        * compactness**3
        * (
            13
            - 11 * y_surface
            + compactness * (3 * y_surface - 2)
            + 2 * compactness**2 * (1 + y_surface)
        )
        + 3
        * (1 - 2 * compactness) ** 2
        * (
            2
            - y_surface
            + 2 * compactness * (y_surface - 1)
        )
        * np.log(1 - 2 * compactness)
    )
    love_k2 = numerator / denominator
    tidal_lambda = 2 * love_k2 / (3 * compactness**5)
    return compactness, love_k2, tidal_lambda


def rhs_core(
    radius: float,
    state: np.ndarray,
    lambda_r: complex = 0.0,
    lambda_c: complex = 0.0,
    k_eos: float = EOS_K,
) -> np.ndarray:
    mass, number_density, tidal_y = state
    energy, pressure, _, pressure_n, sound_squared = effective_eos(
        number_density, lambda_r, lambda_c, k_eos
    )
    one_minus_two_m_over_r = 1 - 2 * mass / radius
    mass_prime = 4 * np.pi * radius**2 * energy
    pressure_prime = -(
        (energy + pressure)
        * (mass + 4 * np.pi * radius**3 * pressure)
        / (radius**2 * one_minus_two_m_over_r)
    )
    number_prime = pressure_prime / pressure_n
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
        [mass_prime, number_prime, tidal_y_prime],
        dtype=np.result_type(state, lambda_r, lambda_c),
    )


def response_jacobian(
    radius: float, state: np.ndarray, k_eos: float = EOS_K
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    state_complex = np.asarray(state, dtype=complex)
    jacobian = np.empty((3, 3), dtype=float)
    for column in range(3):
        shifted = state_complex.copy()
        shifted[column] += 1j * COMPLEX_STEP
        jacobian[:, column] = np.imag(
            rhs_core(radius, shifted, 0.0, 0.0, k_eos)
        ) / COMPLEX_STEP
    source_r = np.imag(
        rhs_core(
            radius,
            state_complex,
            1j * COMPLEX_STEP,
            0.0,
            k_eos,
        )
    ) / COMPLEX_STEP
    source_c = np.imag(
        rhs_core(
            radius,
            state_complex,
            0.0,
            1j * COMPLEX_STEP,
            k_eos,
        )
    ) / COMPLEX_STEP
    return jacobian, source_r, source_c


def _initial_state(
    central_density: float,
    k_eos: float,
    with_response: bool,
) -> np.ndarray:
    basis = contact_basis(central_density, k_eos)
    mass = 4 * math.pi * float(basis["energy"]) * R0**3 / 3
    base = np.asarray([mass, central_density, 2.0], dtype=float)
    if not with_response:
        return base
    tangent_r = np.asarray(
        [
            -4 * math.pi * float(basis["f_r"]) * R0**3 / 3,
            0.0,
            0.0,
        ]
    )
    tangent_c = np.asarray(
        [
            -4 * math.pi * float(basis["f_c"]) * R0**3 / 3,
            0.0,
            0.0,
        ]
    )
    tangent_n = np.asarray(
        [
            4 * math.pi * float(basis["energy_n"]) * R0**3 / 3,
            1.0,
            0.0,
        ]
    )
    return np.concatenate([base, tangent_r, tangent_c, tangent_n])


def _surface_base_derivatives(
    mass: float, radius: float, tidal_y: float, k_eos: float
) -> tuple[float, float]:
    number_prime = -mass / (
        2 * k_eos * radius * (radius - 2 * mass)
    )
    one_minus_two_m_over_r = 1 - 2 * mass / radius
    tidal_f = 1 / one_minus_two_m_over_r
    tidal_q = (
        4 * math.pi / (2 * k_eos * one_minus_two_m_over_r)
        - 6 / (radius**2 * one_minus_two_m_over_r)
        - 4
        * mass**2
        / (radius**4 * one_minus_two_m_over_r**2)
    )
    tidal_prime = -(
        tidal_y**2 + tidal_y * tidal_f + radius**2 * tidal_q
    ) / radius
    return number_prime, tidal_prime


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
    base_surface: np.ndarray,
    tangent: np.ndarray,
    k_eos: float,
) -> dict[str, float]:
    mass, radius, tidal_y = base_surface
    number_prime, tidal_prime = _surface_base_derivatives(
        mass, radius, tidal_y, k_eos
    )
    radius_response = -tangent[1] / number_prime
    mass_response = tangent[0]
    tidal_y_response = tangent[2] + tidal_prime * radius_response
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


def solve_star(
    central_density: float,
    lambda_r: float = 0.0,
    lambda_c: float = 0.0,
    k_eos: float = EOS_K,
) -> dict[str, float]:
    initial = _initial_state(central_density, k_eos, False)
    basis = contact_basis(central_density, k_eos)
    initial[0] = 4 * math.pi * float(
        basis["energy"]
        - lambda_r * basis["f_r"]
        - lambda_c * basis["f_c"]
    ) * R0**3 / 3

    def surface_event(radius: float, state: np.ndarray) -> float:
        return float(state[1])

    surface_event.terminal = True
    surface_event.direction = -1
    solution = solve_ivp(
        lambda radius, state: rhs_core(
            radius, state, lambda_r, lambda_c, k_eos
        ),
        (R0, 100.0),
        initial,
        events=surface_event,
        rtol=RTOL,
        atol=ATOL,
        max_step=MAX_STEP,
    )
    if not solution.success or len(solution.t_events[0]) != 1:
        raise RuntimeError("TOV-Love surface event failed")
    radius = float(solution.t_events[0][0])
    mass, _, tidal_y = solution.y_events[0][0]
    compactness, love_k2, tidal_lambda = love_observables(
        mass, radius, tidal_y
    )
    return {
        "central_density": central_density,
        "mass": float(mass),
        "radius": radius,
        "radius_km": radius * L_SUN_M / 1000,
        "compactness": float(compactness),
        "tidal_y": float(tidal_y),
        "love_k2": float(love_k2),
        "tidal_lambda": float(tidal_lambda),
    }


def solve_star_response(
    central_density: float, k_eos: float = EOS_K
) -> dict[str, Any]:
    initial = _initial_state(central_density, k_eos, True)

    def augmented_rhs(radius: float, state: np.ndarray) -> np.ndarray:
        base = state[:3]
        tangent_r = state[3:6]
        tangent_c = state[6:9]
        tangent_n = state[9:12]
        base_rhs = rhs_core(radius, base, 0.0, 0.0, k_eos)
        jacobian, source_r, source_c = response_jacobian(
            radius, base, k_eos
        )
        return np.concatenate(
            [
                base_rhs,
                jacobian @ tangent_r + source_r,
                jacobian @ tangent_c + source_c,
                jacobian @ tangent_n,
            ]
        )

    def surface_event(radius: float, state: np.ndarray) -> float:
        return float(state[1])

    surface_event.terminal = True
    surface_event.direction = -1
    solution = solve_ivp(
        augmented_rhs,
        (R0, 100.0),
        initial,
        events=surface_event,
        rtol=RTOL,
        atol=ATOL,
        max_step=MAX_STEP,
    )
    if not solution.success or len(solution.t_events[0]) != 1:
        raise RuntimeError("augmented TOV-Love surface event failed")
    radius = float(solution.t_events[0][0])
    surface = solution.y_events[0][0]
    mass, _, tidal_y = surface[:3]
    compactness, love_k2, tidal_lambda = love_observables(
        mass, radius, tidal_y
    )
    base_surface = np.asarray([mass, radius, tidal_y], dtype=float)
    response_r = _surface_response(base_surface, surface[3:6], k_eos)
    response_c = _surface_response(base_surface, surface[6:9], k_eos)
    response_n = _surface_response(base_surface, surface[9:12], k_eos)
    log_mass_slope = central_density * response_n["mass"] / mass

    def fixed_mass(response: dict[str, float]) -> dict[str, float]:
        central_shift = -response["mass"] / response_n["mass"]
        return {
            "central_density": central_shift,
            "radius": (
                response["radius"]
                + response_n["radius"] * central_shift
            ),
            "love_k2": (
                response["love_k2"]
                + response_n["love_k2"] * central_shift
            ),
            "tidal_lambda": (
                response["tidal_lambda"]
                + response_n["tidal_lambda"] * central_shift
            ),
        }

    return {
        "base": {
            "central_density": central_density,
            "mass": float(mass),
            "radius": radius,
            "radius_km": radius * L_SUN_M / 1000,
            "compactness": float(compactness),
            "tidal_y": float(tidal_y),
            "love_k2": float(love_k2),
            "tidal_lambda": float(tidal_lambda),
            "log_mass_slope": float(log_mass_slope),
            "stable_branch": bool(response_n["mass"] > 0),
        },
        "fixed_central_density": {
            "lambda_r": response_r,
            "lambda_c": response_c,
            "central_density": response_n,
        },
        "fixed_mass": {
            "lambda_r": fixed_mass(response_r),
            "lambda_c": fixed_mass(response_c),
        },
        "passed": (
            mass > 0
            and radius > 2 * mass
            and love_k2 > 0
            and tidal_lambda > 0
            and np.isfinite(log_mass_slope)
        ),
    }


@lru_cache(maxsize=None)
def locate_stable_models(k_eos: float = EOS_K) -> dict[str, Any]:
    maximum = minimize_scalar(
        lambda log_density: -solve_star(
            math.exp(log_density), k_eos=k_eos
        )["mass"],
        bounds=(math.log(2e-4), math.log(1e-2)),
        method="bounded",
        options={"xatol": 2e-6},
    )
    central_max = math.exp(maximum.x)
    model_max = solve_star(central_max, k_eos=k_eos)

    def stable_density_for_mass(target_mass: float) -> float:
        return brentq(
            lambda density: solve_star(density, k_eos=k_eos)["mass"]
            - target_mass,
            2e-4,
            central_max * (1 - 2e-5),
            xtol=2e-11,
            rtol=2e-10,
        )

    targets = {
        "one_solar_mass": 1.0,
        "canonical_1p4": 1.4,
        "near_turning_0p99_Mmax": 0.99 * model_max["mass"],
    }
    densities = {
        name: stable_density_for_mass(target)
        for name, target in targets.items()
    }
    return {
        "EOS": "Gamma=2 relativistic polytrope",
        "K_Lsun2": k_eos,
        "length_unit_m": L_SUN_M,
        "maximum_model": model_max,
        "target_densities": densities,
        "passed": bool(
            maximum.success
            and model_max["mass"] > 1.6
            and model_max["mass"] < 1.7
            and all(2e-4 < value < central_max for value in densities.values())
        ),
    }


def physical_contact_caps() -> dict[str, float | bool]:
    strict = strict_eft_contact_branch()
    lambda_r_m2 = (
        8 * math.pi * strict["aR_abs_control_cap"] * LBAR_P2
    )
    lambda_c_m2 = (
        8 * math.pi * strict["aC_abs_control_cap"] * LBAR_P2
    )
    lambda_r = lambda_r_m2 / L_SUN_M**2
    lambda_c = lambda_c_m2 / L_SUN_M**2
    return {
        "lambdaR_cap_m2": lambda_r_m2,
        "lambdaC_cap_m2": lambda_c_m2,
        "lambdaR_cap_Lsun2": lambda_r,
        "lambdaC_cap_Lsun2": lambda_c,
        "ratio": lambda_c / lambda_r,
        "passed": (
            5.6e-11 < lambda_r_m2 < 5.7e-11
            and 1.69e-10 < lambda_c_m2 < 1.71e-10
            and abs(lambda_c / lambda_r - 3) < 1e-12
        ),
    }


@lru_cache(maxsize=None)
def response_benchmarks() -> dict[str, Any]:
    locations = locate_stable_models()
    caps = physical_contact_caps()
    rows: list[dict[str, Any]] = []
    for model_id, central_density in locations["target_densities"].items():
        response = solve_star_response(central_density)
        base = response["base"]
        fixed_central = response["fixed_central_density"]
        fixed_mass = response["fixed_mass"]

        def envelope(
            derivative_r: float, derivative_c: float
        ) -> float:
            return (
                abs(derivative_r) * caps["lambdaR_cap_Lsun2"]
                + abs(derivative_c) * caps["lambdaC_cap_Lsun2"]
            )

        mass_shift = envelope(
            fixed_central["lambda_r"]["mass"],
            fixed_central["lambda_c"]["mass"],
        )
        radius_shift_fixed_central = envelope(
            fixed_central["lambda_r"]["radius"],
            fixed_central["lambda_c"]["radius"],
        )
        radius_shift_fixed_mass = envelope(
            fixed_mass["lambda_r"]["radius"],
            fixed_mass["lambda_c"]["radius"],
        )
        tidal_shift_fixed_mass = envelope(
            fixed_mass["lambda_r"]["tidal_lambda"],
            fixed_mass["lambda_c"]["tidal_lambda"],
        )
        central_shift_fixed_mass = envelope(
            fixed_mass["lambda_r"]["central_density"],
            fixed_mass["lambda_c"]["central_density"],
        )
        rows.append(
            {
                "model_id": model_id,
                **base,
                "turning_condition_number": 1 / abs(base["log_mass_slope"]),
                "cap_abs_deltaM_over_M_fixed_nc": mass_shift / base["mass"],
                "cap_abs_deltaR_over_R_fixed_nc": (
                    radius_shift_fixed_central / base["radius"]
                ),
                "cap_abs_deltaR_over_R_fixed_M": (
                    radius_shift_fixed_mass / base["radius"]
                ),
                "cap_abs_deltaLambda_over_Lambda_fixed_M": (
                    tidal_shift_fixed_mass / base["tidal_lambda"]
                ),
                "cap_abs_delta_nc_over_nc_fixed_M": (
                    central_shift_fixed_mass / central_density
                ),
                "response_valid": response["passed"],
                "valid_for_claim": False,
            }
        )
    by_id = {row["model_id"]: row for row in rows}
    return {
        "EOS": locations["EOS"],
        "K_Lsun2": locations["K_Lsun2"],
        "maximum_model": locations["maximum_model"],
        "caps": caps,
        "rows": rows,
        "interpretation": (
            "The tangent system gives derivatives at fixed central "
            "density. Fixed-mass responses project along the stable "
            "sequence using delta n_c=-M_lambda/M_nc. The projection "
            "becomes ill-conditioned as dM/dn_c approaches zero."
        ),
        "passed": (
            locations["passed"]
            and caps["passed"]
            and len(rows) == 3
            and all(row["response_valid"] for row in rows)
            and by_id["canonical_1p4"]["stable_branch"]
            and by_id["near_turning_0p99_Mmax"][
                "turning_condition_number"
            ]
            > by_id["canonical_1p4"]["turning_condition_number"]
        ),
    }


@lru_cache(maxsize=None)
def finite_difference_crosscheck() -> dict[str, Any]:
    locations = locate_stable_models()
    central_density = locations["target_densities"]["canonical_1p4"]
    response = solve_star_response(central_density)
    step = 1.0e-2
    rows: list[dict[str, Any]] = []
    for direction, lambda_pair in {
        "lambda_r": ((step, 0.0), (-step, 0.0)),
        "lambda_c": ((0.0, step), (0.0, -step)),
    }.items():
        plus = solve_star(
            central_density,
            lambda_r=lambda_pair[0][0],
            lambda_c=lambda_pair[0][1],
        )
        minus = solve_star(
            central_density,
            lambda_r=lambda_pair[1][0],
            lambda_c=lambda_pair[1][1],
        )
        tangent = response["fixed_central_density"][direction]
        for observable in ["mass", "radius", "love_k2", "tidal_lambda"]:
            finite = (plus[observable] - minus[observable]) / (2 * step)
            analytic = tangent[observable]
            relative_error = abs(finite - analytic) / max(
                abs(analytic), 1e-14
            )
            rows.append(
                {
                    "projection": "fixed_central_density",
                    "direction": direction,
                    "observable": observable,
                    "tangent_derivative": analytic,
                    "finite_difference_derivative": finite,
                    "relative_error": relative_error,
                    "status": "PASS" if relative_error < 2e-3 else "FAIL",
                }
            )

        target_mass = response["base"]["mass"]

        def fixed_mass_model(pair: tuple[float, float]) -> tuple[float, dict[str, float]]:
            density = brentq(
                lambda trial: solve_star(
                    trial,
                    lambda_r=pair[0],
                    lambda_c=pair[1],
                )["mass"]
                - target_mass,
                0.8 * central_density,
                1.2 * central_density,
                xtol=2e-12,
                rtol=2e-11,
            )
            return density, solve_star(
                density,
                lambda_r=pair[0],
                lambda_c=pair[1],
            )

        plus_density, plus_fixed = fixed_mass_model(lambda_pair[0])
        minus_density, minus_fixed = fixed_mass_model(lambda_pair[1])
        fixed_tangent = response["fixed_mass"][direction]
        finite_fixed = {
            "central_density": (plus_density - minus_density) / (2 * step),
            "radius": (plus_fixed["radius"] - minus_fixed["radius"])
            / (2 * step),
            "love_k2": (plus_fixed["love_k2"] - minus_fixed["love_k2"])
            / (2 * step),
            "tidal_lambda": (
                plus_fixed["tidal_lambda"] - minus_fixed["tidal_lambda"]
            )
            / (2 * step),
        }
        for observable, finite in finite_fixed.items():
            analytic = fixed_tangent[observable]
            relative_error = abs(finite - analytic) / max(
                abs(analytic), 1e-14
            )
            rows.append(
                {
                    "projection": "fixed_mass",
                    "direction": direction,
                    "observable": observable,
                    "tangent_derivative": analytic,
                    "finite_difference_derivative": finite,
                    "relative_error": relative_error,
                    "status": "PASS" if relative_error < 2e-3 else "FAIL",
                }
            )
    return {
        "central_density": central_density,
        "finite_difference_step_Lsun2": step,
        "rows": rows,
        "maximum_relative_error": max(row["relative_error"] for row in rows),
        "passed": all(row["status"] == "PASS" for row in rows),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    benchmarks = response_benchmarks()
    crosscheck = finite_difference_crosscheck()
    return {
        "selected_branch": "STRICT_EFT_METRIC_ONLY_ANALYTIC_EH_BRANCH",
        "response_operator": (
            "TOV_LOVE_TANGENT_JACOBIAN_DERIVED_AND_FINITE_DIFFERENCE_"
            "VALIDATED"
        ),
        "fixed_mass_projection": (
            "DERIVED_ON_STABLE_BRANCH_WITH_EXPLICIT_TURNING_CONDITION"
        ),
        "contact_observable_status": (
            "COMPUTABLE_EOS_CONDITIONAL_MASS_RADIUS_TIDAL_ENVELOPES"
        ),
        "strong_matter_background_promoted": False,
        "reason_not_promoted": (
            "the current Gamma=2 polytrope is a controlled benchmark, "
            "not an independently fixed microphysical neutron-star EOS; "
            "the response becomes singular at the maximum-mass turning "
            "point"
        ),
        "full_fundamental_unification": False,
        "next_target": (
            "4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-"
            "multi-EOS-mass-radius-tidal-contact-response-gate.md"
        ),
        "passed": benchmarks["passed"] and crosscheck["passed"],
    }


def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "EOS_contract": {
            "EOS": "p=K n^2; rho=n+p; Gamma=2",
            "K_Lsun2": EOS_K,
            "sound_speed": "c_s^2=2Kn/(1+2Kn), so 0<=c_s^2<1",
            "surface_density": 0.0,
            "surface_jump_correction_required": False,
            "observationally_viable_2Msun_EOS": False,
            "role": "controlled analytic response benchmark, not microphysical claim",
            "passed": EOS_GAMMA == 2 and EOS_K == 100,
        },
        "locations": locate_stable_models(),
        "caps": physical_contact_caps(),
        "responses": response_benchmarks(),
        "crosscheck": finite_difference_crosscheck(),
        "arbitration": arbitration(),
    }
    return {
        "sections": sections,
        "all_checks_pass": bool(
            all(section["passed"] for section in sections.values())
        ),
        "decision": (
            "derive and validate the coupled TOV-Love tangent response, "
            "project contact corrections at fixed mass along the stable "
            "sequence, quantify turning-point conditioning, and retain "
            "the results as EOS-conditional benchmarks pending a "
            "tabulated microphysical multi-EOS run"
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
