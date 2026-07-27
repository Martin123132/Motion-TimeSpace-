from __future__ import annotations

import csv
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import brentq


sys.dont_write_bytecode = True

from Y5_R2FR_4876_integrated_H_matching import result as result_4876
from Y5_R2FR_4877_spectrum_nonlocal_vacuum import result as result_4877
from Y5_R2FR_4878_local_eft_arena_bounds import (
    LBAR_P2,
    strict_eft_contact_branch,
)
from Y5_R2FR_4883_multi_eos_tov_love_response import (
    EOS_TABLES,
    L_SUN_M,
    contact_basis,
    solve_star,
)


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4884"
MBAR_PL_EV = 2.435e27
HBAR_C_EV_M = 1.973269804e-7
CONTACT_M2_PER_A = 8 * math.pi * LBAR_P2
A_PER_LSUN2 = L_SUN_M**2 / CONTACT_M2_PER_A
NEXT_TARGET = (
    "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-"
    "from-closed-bath-or-three-boson-branch-demotion-gate.md"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


@lru_cache(maxsize=None)
def prior_contract() -> dict[str, Any]:
    prior_4876 = result_4876()
    prior_4877 = result_4877()
    heat = prior_4876["sections"]["heat_kernel"]
    poles = prior_4876["sections"]["quadratic_poles"]
    newton = prior_4876["sections"]["newton_matching"]
    branches = prior_4877["sections"]["branch_tests"]["scenarios"]
    validation_4883 = read_csv(
        OUTPUT / "P8_Y5_BRR545_4883_VALIDATION.csv"
    )
    passed = bool(
        prior_4876["all_checks_pass"]
        and prior_4877["all_checks_pass"]
        and heat["a_R_loop"]
        == "L*N_s*(6*xi - 1)**2/(1152*pi**2)"
        and heat["a_C_loop"] == "L*N_s/(1920*pi**2)"
        and poles["m0_squared"] == "Lambda_UV**2/(L*h)"
        and newton["measured_combination"]
        == "N_s(1-6xi)Lambda_UV^2=12 pi/G_N"
        and len(branches) == 7
        and validation_4883
        and all(row["status"] == "PASS" for row in validation_4883)
    )
    rows = [
        {
            "quantity": "a_R_loop",
            "formula": "L*S_h2/(1152*pi^2)",
            "ownership": "DERIVED_UNIVERSAL_MATTER_LOOP",
            "remaining_terms": (
                "finite renormalized matching plus integrated-H/ghost and "
                "threshold-complete spectrum"
            ),
        },
        {
            "quantity": "a_C_loop",
            "formula": "L*W_C/(1920*pi^2)",
            "ownership": "DERIVED_UNIVERSAL_MATTER_LOOP",
            "remaining_terms": (
                "finite renormalized matching plus integrated-H/ghost and "
                "threshold-complete spectrum"
            ),
        },
        {
            "quantity": "a_R_total(mu)",
            "formula": (
                "a_R,fin(mu0)+L*S_h2/(1152*pi^2)+"
                "a_R,Hghost(mu)+a_R,threshold(mu)"
            ),
            "ownership": "PARTIAL_PARENT_OWNERSHIP",
            "remaining_terms": "finite and omitted signed-spectrum pieces",
        },
        {
            "quantity": "a_C_total(mu)",
            "formula": (
                "a_C,fin(mu0)+L*W_C/(1920*pi^2)+"
                "a_C,Hghost(mu)+a_C,threshold(mu)"
            ),
            "ownership": "PARTIAL_PARENT_OWNERSHIP",
            "remaining_terms": "finite and omitted signed-spectrum pieces",
        },
        {
            "quantity": "Newton_matching",
            "formula": "W1*Lambda_UV^2=96*pi^2*Mbar_Pl^2",
            "ownership": "DERIVED_MATCHING_RELATION",
            "remaining_terms": "one microscopic scale or weight must be fixed",
        },
    ]
    return {
        "rows": rows,
        "branches": branches,
        "passed": passed,
    }


@lru_cache(maxsize=None)
def spectrum_rescue() -> dict[str, Any]:
    scenarios = prior_contract()["branches"]
    rows: list[dict[str, Any]] = []
    for scenario in scenarios:
        scalar_count = float(scenario["N_s"])
        dirac_count = float(scenario["N_D"])
        vector_count = float(scenario["N_V"])
        h_floor = (4 * vector_count - 2 * dirac_count) / scalar_count
        h_floor = max(0.0, h_floor)
        xi_boundary = (1 - h_floor) / 6
        weyl_weight = scalar_count + 6 * dirac_count + 12 * vector_count
        scalar_square_at_floor = scalar_count * h_floor**2
        ratio_floor = (
            (5 / 3) * scalar_square_at_floor / weyl_weight
            if h_floor > 0
            else 0.0
        )
        rows.append(
            {
                "branch": scenario["branch"],
                "N_s": scalar_count,
                "N_D": dirac_count,
                "N_V": vector_count,
                "W1_common_h": (
                    f"{scalar_count:g}*h+{2*dirac_count-4*vector_count:g}"
                ),
                "positive_EH_h_condition": (
                    f"h>{h_floor:.15g}"
                    if h_floor > 0
                    else "h>0"
                ),
                "xi_condition": (
                    f"xi<{xi_boundary:.15g}"
                    if h_floor >= 1
                    else "xi<1/6 with branch-specific lower weight"
                ),
                "W_C": weyl_weight,
                "aR_over_aC_at_EH_boundary": ratio_floor,
                "ownership": scenario["ownership"],
                "minimal_h_positive_EH": scenario["positive_EH"],
            }
        )
    candidate = next(
        row
        for row in rows
        if row["branch"] == "complex_psi_Gamma_plus_public_U1"
    )
    real_candidate = next(
        row
        for row in rows
        if row["branch"] == "real_psi_plus_public_U1"
    )
    passed = bool(
        math.isclose(
            float(candidate["positive_EH_h_condition"].split(">", 1)[1]),
            4 / 3,
            rel_tol=1e-12,
        )
        and math.isclose(
            float(candidate["xi_condition"].split("<", 1)[1]),
            -1 / 18,
            rel_tol=1e-12,
        )
        and math.isclose(
            candidate["aR_over_aC_at_EH_boundary"],
            16 / 27,
            rel_tol=1e-12,
        )
        and real_candidate["positive_EH_h_condition"] == "h>4"
    )
    return {
        "rows": rows,
        "candidate_branch": (
            "complex_psi_Gamma_plus_public_U1 with common h>4/3"
        ),
        "candidate_formula": (
            "W1=3h-4; S_h2=3h^2; W_C=15; "
            "a_R/a_C=h^2/3"
        ),
        "interpretation": (
            "the existing maximal three-real-scalar plus U(1) reading can "
            "have positive induced Einstein stiffness without adding two "
            "more scalar species, but the common nonminimal weight and the "
            "Gamma determinant are not yet primitive-derived"
        ),
        "passed": passed,
    }


def _target_rows() -> list[dict[str, str]]:
    return read_csv(OUTPUT / "P8_Y5_R2FR_4883_TARGET_LOCATIONS.csv")


@lru_cache(maxsize=None)
def curvature_stability() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for source in _target_rows():
        eos_id = source["eos_id"]
        central_q = float(source["central_q"])
        energy, pressure, *_ = EOS_TABLES[eos_id].base_jet(central_q)
        ricci_lsun_minus2 = 8 * math.pi * float(energy - 3 * pressure)
        ricci_m_minus2 = ricci_lsun_minus2 / L_SUN_M**2
        rows.append(
            {
                "eos_id": eos_id,
                "model_id": source["model_id"],
                "central_energy_Lsun_minus2": float(energy),
                "central_pressure_Lsun_minus2": float(pressure),
                "central_R_Lsun_minus2": ricci_lsun_minus2,
                "central_R_m_minus2": ricci_m_minus2,
            }
        )
    maximum_positive = max(row["central_R_m_minus2"] for row in rows)
    maximum_row = max(rows, key=lambda row: row["central_R_m_minus2"])
    mass_floor_factor = HBAR_C_EV_M * math.sqrt(maximum_positive / 6)
    return {
        "rows": rows,
        "maximum_positive_R_m_minus2": maximum_positive,
        "maximum_positive_R_eos": maximum_row["eos_id"],
        "maximum_positive_R_model": maximum_row["model_id"],
        "mass_floor_eV_per_sqrt_h_minus_1": mass_floor_factor,
        "stability_law": (
            "m_s^2+xi*R>=0; for h=1-6xi>1 and R>0, "
            "m_s[eV]>=8.02675e-12*sqrt(h-1) on the sampled stars"
        ),
        "passed": bool(
            9.9e-9 < maximum_positive < 1.0e-8
            and 8.0e-12 < mass_floor_factor < 8.1e-12
        ),
    }


def observational_windows() -> list[dict[str, Any]]:
    return [
        {
            "window_id": "GW170817_Lambda1p4_90pct",
            "observable": "tidal_lambda",
            "lower": 70.0,
            "central": 190.0,
            "upper": 580.0,
            "unit": "dimensionless",
            "mass_Msun": 1.4,
            "credible_level": "90 percent common-EOS estimate",
            "source": "https://dcc.ligo.org/ligo-p1800115/public",
            "local_source": str(
                POST
                / "source-intake"
                / "strong_matter"
                / "4884"
                / "GW170817_EOS_PRL_P1800115_v12.pdf"
            ),
            "projection_scope": "direct canonical deformability interval",
        },
        {
            "window_id": "GW170817_common_EOS_radius_90pct",
            "observable": "radius_km",
            "lower": 10.5,
            "central": 11.9,
            "upper": 13.3,
            "unit": "km",
            "mass_Msun": 1.4,
            "credible_level": "90 percent component-radius estimate",
            "source": "https://dcc.ligo.org/ligo-p1800115/public",
            "local_source": str(
                POST
                / "source-intake"
                / "strong_matter"
                / "4884"
                / "GW170817_EOS_PRL_P1800115_v12.pdf"
            ),
            "projection_scope": (
                "broad canonical proxy; component masses are not exactly 1.4"
            ),
        },
        {
            "window_id": "NICER_J0030_radius_68pct",
            "observable": "radius_km",
            "lower": 11.96,
            "central": 13.02,
            "upper": 14.26,
            "unit": "km",
            "mass_Msun": 1.44,
            "credible_level": "68 percent marginal interval",
            "source": "https://arxiv.org/abs/1912.05705",
            "local_source": str(
                POST
                / "source-intake"
                / "strong_matter"
                / "4884"
                / "NICER_J0030_Miller_1912.05705.pdf"
            ),
            "projection_scope": (
                "near-canonical direct-radius proxy; joint M-R posterior not used"
            ),
        },
    ]


@lru_cache(maxsize=None)
def canonical_response() -> dict[str, Any]:
    backgrounds = {
        row["eos_id"]: row
        for row in read_csv(
            OUTPUT / "P8_Y5_R2FR_4883_RESPONSE_BENCHMARKS.csv"
        )
        if row["model_id"] == "canonical_1p4"
    }
    derivatives: dict[tuple[str, str, str], float] = {}
    for row in read_csv(
        OUTPUT / "P8_Y5_R2FR_4883_FINITE_DIFFERENCE.csv"
    ):
        if row["projection"] != "fixed_mass":
            continue
        if row["observable"] not in {
            "central_q",
            "radius",
            "tidal_lambda",
        }:
            continue
        derivatives[(row["eos_id"], row["direction"], row["observable"])] = (
            float(row["tangent_derivative"])
        )
    basis: dict[str, dict[str, float]] = {}
    for eos_id, background in backgrounds.items():
        raw = contact_basis(EOS_TABLES[eos_id], float(background["central_q"]))
        basis[eos_id] = {
            key: float(np.real(raw[key]))
            for key in ("energy", "pressure", "f_r", "f_c", "d_r", "d_c")
        }
    passed = bool(
        len(backgrounds) == 3
        and len(derivatives) == 18
        and all(float(row["mass"]) > 1.399 for row in backgrounds.values())
    )
    return {
        "backgrounds": backgrounds,
        "derivatives": derivatives,
        "basis": basis,
        "passed": passed,
    }


def _observable_value(background: dict[str, str], observable: str) -> float:
    return float(background[observable])


def _observable_slope(
    derivatives: dict[tuple[str, str, str], float],
    eos_id: str,
    direction: str,
    observable: str,
) -> float:
    raw_observable = "radius" if observable == "radius_km" else observable
    slope = derivatives[(eos_id, direction, raw_observable)]
    if observable == "radius_km":
        slope *= L_SUN_M / 1000
    return slope


def _contact_control(
    basis: dict[str, float], lambda_r: float, lambda_c: float
) -> tuple[float, float]:
    energy_fraction = (
        abs(lambda_r) * abs(basis["f_r"])
        + abs(lambda_c) * abs(basis["f_c"])
    ) / basis["energy"]
    pressure_fraction = (
        abs(lambda_r) * abs(basis["d_r"])
        + abs(lambda_c) * abs(basis["d_c"])
    ) / basis["pressure"]
    return energy_fraction, pressure_fraction


@lru_cache(maxsize=None)
def observational_projection() -> dict[str, Any]:
    response = canonical_response()
    backgrounds = response["backgrounds"]
    derivatives = response["derivatives"]
    bases = response["basis"]
    windows = observational_windows()
    one_at_a_time: list[dict[str, Any]] = []
    for window in windows:
        observable = window["observable"]
        for eos_id, background in backgrounds.items():
            base = _observable_value(background, observable)
            for direction in ("lambda_r", "lambda_c"):
                slope = _observable_slope(
                    derivatives, eos_id, direction, observable
                )
                endpoints = sorted(
                    [
                        (window["lower"] - base) / slope,
                        (window["upper"] - base) / slope,
                    ]
                )
                controls = [
                    _contact_control(
                        bases[eos_id],
                        endpoint if direction == "lambda_r" else 0.0,
                        endpoint if direction == "lambda_c" else 0.0,
                    )
                    for endpoint in endpoints
                ]
                one_at_a_time.append(
                    {
                        "window_id": window["window_id"],
                        "eos_id": eos_id,
                        "observable": observable,
                        "direction": direction,
                        "base_value": base,
                        "slope_per_Lsun2": slope,
                        "lambda_lower_Lsun2": endpoints[0],
                        "lambda_upper_Lsun2": endpoints[1],
                        "a_lower": endpoints[0] * A_PER_LSUN2,
                        "a_upper": endpoints[1] * A_PER_LSUN2,
                        "zero_inside_interval": endpoints[0] <= 0 <= endpoints[1],
                        "max_endpoint_energy_contact_fraction": max(
                            control[0] for control in controls
                        ),
                        "max_endpoint_pressure_contact_fraction": max(
                            control[1] for control in controls
                        ),
                        "linear_10pct_control": max(
                            max(control) for control in controls
                        )
                        <= 0.1,
                        "status": "LINEAR_INTERVAL_PROJECTION_NONCLAIM",
                    }
                )

    tidal_window = next(
        row for row in windows if row["observable"] == "tidal_lambda"
    )
    radius_windows = [row for row in windows if row["observable"] == "radius_km"]
    joint_vertices: list[dict[str, Any]] = []
    for radius_window in radius_windows:
        for eos_id, background in backgrounds.items():
            radius_slopes = [
                _observable_slope(
                    derivatives, eos_id, direction, "radius_km"
                )
                for direction in ("lambda_r", "lambda_c")
            ]
            tidal_slopes = [
                _observable_slope(
                    derivatives, eos_id, direction, "tidal_lambda"
                )
                for direction in ("lambda_r", "lambda_c")
            ]
            determinant = (
                radius_slopes[0] * tidal_slopes[1]
                - radius_slopes[1] * tidal_slopes[0]
            )
            normalized_determinant = abs(determinant) / (
                math.hypot(*radius_slopes) * math.hypot(*tidal_slopes)
            )
            for radius_side, radius_target in (
                ("lower", radius_window["lower"]),
                ("upper", radius_window["upper"]),
            ):
                for tidal_side, tidal_target in (
                    ("lower", tidal_window["lower"]),
                    ("upper", tidal_window["upper"]),
                ):
                    radius_delta = radius_target - float(background["radius_km"])
                    tidal_delta = tidal_target - float(
                        background["tidal_lambda"]
                    )
                    lambda_r = (
                        radius_delta * tidal_slopes[1]
                        - radius_slopes[1] * tidal_delta
                    ) / determinant
                    lambda_c = (
                        radius_slopes[0] * tidal_delta
                        - radius_delta * tidal_slopes[0]
                    ) / determinant
                    energy_fraction, pressure_fraction = _contact_control(
                        bases[eos_id], lambda_r, lambda_c
                    )
                    joint_vertices.append(
                        {
                            "radius_window": radius_window["window_id"],
                            "tidal_window": tidal_window["window_id"],
                            "eos_id": eos_id,
                            "radius_side": radius_side,
                            "tidal_side": tidal_side,
                            "target_radius_km": radius_target,
                            "target_tidal_lambda": tidal_target,
                            "lambda_r_Lsun2": lambda_r,
                            "lambda_c_Lsun2": lambda_c,
                            "a_R": lambda_r * A_PER_LSUN2,
                            "a_C": lambda_c * A_PER_LSUN2,
                            "normalized_response_determinant": normalized_determinant,
                            "energy_contact_fraction": energy_fraction,
                            "pressure_contact_fraction": pressure_fraction,
                            "linear_10pct_control": max(
                                energy_fraction, pressure_fraction
                            )
                            <= 0.1,
                            "status": "JOINT_BOX_VERTEX_LINEAR_NONCLAIM",
                        }
                    )

    halfspans = [
        0.5 * abs(row["a_upper"] - row["a_lower"])
        for row in one_at_a_time
    ]
    return {
        "windows": windows,
        "one_at_a_time": one_at_a_time,
        "joint_vertices": joint_vertices,
        "minimum_a_halfspan": min(halfspans),
        "maximum_joint_pressure_contact_fraction": max(
            row["pressure_contact_fraction"] for row in joint_vertices
        ),
        "all_response_directions_independent": all(
            row["normalized_response_determinant"] > 0.1
            for row in joint_vertices
        ),
        "claim_ready": False,
        "reason_nonclaim": (
            "interval boxes are not likelihoods, EOS rows are alternatives, "
            "mass-radius covariance is omitted, and many projected vertices "
            "leave the ten-percent contact-linearization corridor"
        ),
        "passed": bool(
            len(one_at_a_time) == 18
            and len(joint_vertices) == 24
            and all(
                math.isfinite(row["a_lower"])
                and math.isfinite(row["a_upper"])
                for row in one_at_a_time
            )
            and not all(row["linear_10pct_control"] for row in joint_vertices)
        ),
    }


def _linear_control_caps(eos_id: str, fraction: float) -> dict[str, float]:
    basis = canonical_response()["basis"][eos_id]
    return {
        "lambda_r": min(
            fraction * basis["energy"] / abs(basis["f_r"]),
            fraction * basis["pressure"] / abs(basis["d_r"]),
        ),
        "lambda_c": min(
            fraction * basis["energy"] / abs(basis["f_c"]),
            fraction * basis["pressure"] / abs(basis["d_c"]),
        ),
    }


def _fixed_mass_star(
    eos_id: str,
    central_q: float,
    q_guess: float,
    target_mass: float,
    lambda_r: float,
    lambda_c: float,
) -> dict[str, float]:
    eos = EOS_TABLES[eos_id]

    def residual(trial_q: float) -> float:
        return (
            solve_star(eos_id, trial_q, lambda_r, lambda_c)["mass"]
            - target_mass
        )

    lower = max(eos.q_min * 2, 0.85 * q_guess)
    upper = min(eos.q_max * 0.9, 1.15 * q_guess)
    lower_value = residual(lower)
    upper_value = residual(upper)
    if lower_value * upper_value > 0:
        samples = np.geomspace(
            max(eos.q_min * 2, 0.65 * q_guess),
            min(eos.q_max * 0.9, 1.4 * q_guess),
            12,
        )
        values = [residual(float(sample)) for sample in samples]
        brackets = [
            (float(left), float(right))
            for left, right, value_left, value_right in zip(
                samples[:-1], samples[1:], values[:-1], values[1:]
            )
            if value_left * value_right <= 0
        ]
        if not brackets:
            raise RuntimeError(f"{eos_id}: no stable fixed-mass bracket")
        lower, upper = min(
            brackets,
            key=lambda pair: abs(math.log(math.sqrt(pair[0] * pair[1]) / central_q)),
        )
    root = brentq(
        residual,
        lower,
        upper,
        xtol=3.0e-12,
        rtol=3.0e-11,
    )
    return solve_star(eos_id, root, lambda_r, lambda_c)


@lru_cache(maxsize=None)
def nonlinear_control_robustness() -> dict[str, Any]:
    response = canonical_response()
    rows: list[dict[str, Any]] = []
    fraction = 0.01
    for eos_id, background in response["backgrounds"].items():
        central_q = float(background["central_q"])
        target_mass = float(background["mass"])
        base_radius = float(background["radius"])
        base_tidal = float(background["tidal_lambda"])
        caps = _linear_control_caps(eos_id, fraction)
        for direction in ("lambda_r", "lambda_c"):
            for sign in (-1.0, 1.0):
                coefficient = sign * caps[direction]
                lambda_r = coefficient if direction == "lambda_r" else 0.0
                lambda_c = coefficient if direction == "lambda_c" else 0.0
                q_guess = central_q + response["derivatives"][(
                    eos_id,
                    direction,
                    "central_q",
                )] * coefficient
                model = _fixed_mass_star(
                    eos_id,
                    central_q,
                    q_guess,
                    target_mass,
                    lambda_r,
                    lambda_c,
                )
                radius_derivative = response["derivatives"][(
                    eos_id,
                    direction,
                    "radius",
                )]
                tidal_derivative = response["derivatives"][(
                    eos_id,
                    direction,
                    "tidal_lambda",
                )]
                linear_radius = base_radius + radius_derivative * coefficient
                linear_tidal = base_tidal + tidal_derivative * coefficient
                nonlinear_radius_delta = model["radius"] - base_radius
                nonlinear_tidal_delta = model["tidal_lambda"] - base_tidal
                linear_radius_delta = linear_radius - base_radius
                linear_tidal_delta = linear_tidal - base_tidal
                energy_fraction, pressure_fraction = _contact_control(
                    response["basis"][eos_id], lambda_r, lambda_c
                )
                rows.append(
                    {
                        "eos_id": eos_id,
                        "direction": direction,
                        "sign": int(sign),
                        "coefficient_Lsun2": coefficient,
                        "target_contact_fraction": fraction,
                        "energy_contact_fraction": energy_fraction,
                        "pressure_contact_fraction": pressure_fraction,
                        "fixed_mass_Msun": model["mass"],
                        "central_q_nonlinear": model["central_q"],
                        "radius_km_nonlinear": model["radius_km"],
                        "tidal_lambda_nonlinear": model["tidal_lambda"],
                        "radius_linear_delta_Lsun": linear_radius_delta,
                        "radius_nonlinear_delta_Lsun": nonlinear_radius_delta,
                        "radius_delta_relative_error": abs(
                            nonlinear_radius_delta - linear_radius_delta
                        )
                        / max(abs(linear_radius_delta), 1.0e-14),
                        "tidal_linear_delta": linear_tidal_delta,
                        "tidal_nonlinear_delta": nonlinear_tidal_delta,
                        "tidal_delta_relative_error": abs(
                            nonlinear_tidal_delta - linear_tidal_delta
                        )
                        / max(abs(linear_tidal_delta), 1.0e-12),
                        "status": "NONLINEAR_ONE_PERCENT_CORRIDOR_SOLVED",
                    }
                )
    return {
        "rows": rows,
        "maximum_radius_delta_relative_error": max(
            row["radius_delta_relative_error"] for row in rows
        ),
        "maximum_tidal_delta_relative_error": max(
            row["tidal_delta_relative_error"] for row in rows
        ),
        "interpretation": (
            "the one-percent central contact corridor is solved nonlinearly; "
            "the tangent remains a local derivative, and observational-box "
            "vertices outside this corridor are not promoted as bounds"
        ),
        "passed": bool(
            len(rows) == 12
            and all(abs(row["fixed_mass_Msun"] - 1.4) < 1.0e-5 for row in rows)
            and all(
                row["energy_contact_fraction"] <= fraction + 1.0e-10
                and row["pressure_contact_fraction"] <= fraction + 1.0e-10
                for row in rows
            )
        ),
    }


def _loop_prediction_row(
    branch: str,
    scalar_count: float,
    dirac_count: float,
    vector_count: float,
    h: float,
    ownership: str,
) -> dict[str, Any]:
    response = canonical_response()
    w1 = scalar_count * h + 2 * dirac_count - 4 * vector_count
    sh2 = scalar_count * h**2
    wc = scalar_count + 6 * dirac_count + 12 * vector_count
    cutoff_ratio = math.sqrt(96 * math.pi**2 / w1)
    cutoff_eV = cutoff_ratio * MBAR_PL_EV
    q_ns_eV = HBAR_C_EV_M / 12_000.0
    log_ns = math.log(cutoff_eV / q_ns_eV)
    a_r = log_ns * sh2 / (1152 * math.pi**2)
    a_c = log_ns * wc / (1920 * math.pi**2)
    lambda_r = CONTACT_M2_PER_A * a_r / L_SUN_M**2
    lambda_c = CONTACT_M2_PER_A * a_c / L_SUN_M**2
    radius_shifts: list[float] = []
    tidal_shifts: list[float] = []
    for eos_id in response["backgrounds"]:
        radius_shift_lsun = (
            response["derivatives"][(eos_id, "lambda_r", "radius")]
            * lambda_r
            + response["derivatives"][(eos_id, "lambda_c", "radius")]
            * lambda_c
        )
        tidal_shift = (
            response["derivatives"][(
                eos_id,
                "lambda_r",
                "tidal_lambda",
            )]
            * lambda_r
            + response["derivatives"][(
                eos_id,
                "lambda_c",
                "tidal_lambda",
            )]
            * lambda_c
        )
        radius_shifts.append(radius_shift_lsun * L_SUN_M / 1000)
        tidal_shifts.append(tidal_shift)
    strict = strict_eft_contact_branch()
    maximum_radius_shift = max(abs(value) for value in radius_shifts)
    maximum_tidal_shift = max(abs(value) for value in tidal_shifts)
    observation_fraction = max(
        maximum_radius_shift / 1.15,
        maximum_tidal_shift / 255.0,
    )
    stability = curvature_stability()
    return {
        "branch": branch,
        "N_s": scalar_count,
        "N_D": dirac_count,
        "N_V": vector_count,
        "h": h,
        "xi": (1 - h) / 6,
        "W1": w1,
        "S_h2": sh2,
        "W_C": wc,
        "LambdaUV_over_MbarPl": cutoff_ratio,
        "LambdaUV_eV": cutoff_eV,
        "mu_NS_12km_eV": q_ns_eV,
        "L_NS": log_ns,
        "a_R_loop_NS": a_r,
        "a_C_loop_NS": a_c,
        "aR_over_aC": a_r / a_c,
        "lambda_R_loop_Lsun2": lambda_r,
        "lambda_C_loop_Lsun2": lambda_c,
        "maximum_abs_radius_shift_km": maximum_radius_shift,
        "maximum_abs_tidal_shift": maximum_tidal_shift,
        "orders_below_observational_width": -math.log10(
            observation_fraction
        ),
        "orders_below_strict_aR_cap": math.log10(
            strict["aR_abs_control_cap"] / abs(a_r)
        ),
        "orders_below_strict_aC_cap": math.log10(
            strict["aC_abs_control_cap"] / abs(a_c)
        ),
        "curvature_stability_mass_floor_eV": (
            stability["mass_floor_eV_per_sqrt_h_minus_1"]
            * math.sqrt(max(h - 1, 0.0))
        ),
        "ownership": ownership,
        "status": "PARENT_LOOP_RAY_CONDITIONAL_NONCLAIM",
    }


@lru_cache(maxsize=None)
def parent_loop_predictions() -> dict[str, Any]:
    candidate_rows: list[dict[str, Any]] = []
    for cutoff_ratio in (1.0, 4 * math.pi, 4 * math.pi * math.sqrt(6)):
        w1 = 96 * math.pi**2 / cutoff_ratio**2
        h = (w1 + 4) / 3
        candidate_rows.append(
            _loop_prediction_row(
                branch=f"three_boson_U1_rUV_{cutoff_ratio:.9g}",
                scalar_count=3,
                dirac_count=0,
                vector_count=1,
                h=h,
                ownership=(
                    "maximal explicit MTS bosonic reading; common xi and "
                    "Gamma determinant conditional"
                ),
            )
        )
    reference_rows = [
        _loop_prediction_row(
            "five_minimal_scalars_plus_U1",
            5,
            0,
            1,
            1,
            "unowned minimum positive-EH bosonic completion",
        ),
        _loop_prediction_row(
            "imported_SM_without_RH_neutrinos",
            4,
            22.5,
            12,
            1,
            "external correspondence benchmark",
        ),
    ]
    rows = candidate_rows + reference_rows
    selected = candidate_rows[-1]
    passed = bool(
        len(rows) == 5
        and math.isclose(selected["W1"], 1.0, rel_tol=1e-12)
        and math.isclose(selected["h"], 5 / 3, rel_tol=1e-12)
        and math.isclose(selected["xi"], -1 / 9, rel_tol=1e-12)
        and all(row["orders_below_observational_width"] > 65 for row in rows)
        and all(row["orders_below_strict_aR_cap"] > 50 for row in rows)
        and all(row["orders_below_strict_aC_cap"] > 50 for row in rows)
    )
    return {
        "rows": rows,
        "selected_conditional_anchor": selected["branch"],
        "selected_anchor_result": (
            "at the same W1=1 and cutoff ratio 4*pi*sqrt(6) as the "
            "five-minimal-scalar completion, the existing three-scalar plus "
            "U(1) reading needs h=5/3 (xi=-1/9) and has a_R/a_C=25/27"
        ),
        "minimal_induced_boundary": (
            "a_R,fin(LambdaUV)=a_C,fin(LambdaUV)=0 is a falsifiable "
            "Wilsonian branch condition, not a derived identity"
        ),
        "passed": passed,
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    ownership = prior_contract()
    rescue = spectrum_rescue()
    stability = curvature_stability()
    projection = observational_projection()
    nonlinear = nonlinear_control_robustness()
    predictions = parent_loop_predictions()
    strict = strict_eft_contact_branch()
    strong_matter_weaker_orders = math.log10(
        projection["minimum_a_halfspan"]
        / max(strict["aR_abs_control_cap"], strict["aC_abs_control_cap"])
    )
    return {
        "loop_coefficient_ownership": (
            "UNIVERSAL_MATTER_LOOP_PIECES_DERIVED"
        ),
        "total_coefficient_ownership": (
            "OPEN_FINITE_HGHOST_THRESHOLD_MATCHING"
        ),
        "three_boson_nonminimal_route": (
            "ALGEBRAICALLY_VIABLE_FOR_H_GT_4_OVER_3"
        ),
        "three_boson_parent_promotion": False,
        "reason_not_parent_promoted": (
            "Gamma must be proven to own a real UV determinant and xi or the "
            "cutoff ratio must descend from the closed bath"
        ),
        "observational_projection": (
            "SOURCE_BACKED_INTERVAL_PROJECTION_AND_NONLINEAR_CONTROL_TEST_DONE"
        ),
        "observational_bound_claim": False,
        "reason_no_observational_claim": projection["reason_nonclaim"],
        "strong_matter_interval_weaker_than_local_control_orders": (
            strong_matter_weaker_orders
        ),
        "parent_loop_strong_matter_correspondence": (
            "PASSES_CONDITIONALLY_BY_MORE_THAN_65_ORDERS"
        ),
        "total_strong_matter_correspondence": (
            "CONDITIONAL_ON_FINITE_MATCHING_TERMS_REMAINING_IN_CONTROL_CORRIDOR"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            ownership["passed"]
            and rescue["passed"]
            and stability["passed"]
            and projection["passed"]
            and nonlinear["passed"]
            and predictions["passed"]
            and strong_matter_weaker_orders > 15
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "prior_contract": prior_contract(),
        "spectrum_rescue": spectrum_rescue(),
        "curvature_stability": curvature_stability(),
        "canonical_response": canonical_response(),
        "observational_projection": observational_projection(),
        "nonlinear_control": nonlinear_control_robustness(),
        "parent_predictions": parent_loop_predictions(),
        "arbitration": arbitration(),
    }
    all_checks_pass = all(
        section.get("passed", True) for section in sections.values()
    )
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "all_checks_pass": all_checks_pass,
        "decision": (
            "correct the ownership diagnosis: a_R and a_C loop pieces are "
            "derived, construct the viable three-boson nonminimal ray, "
            "prove its stellar curvature stability threshold is tiny, and "
            "show source-backed strong-matter intervals are far weaker than "
            "the strict-EFT corridor; retain total coefficients as finite "
            "matching data until Gamma, xi and omitted determinants close"
        ),
    }


if __name__ == "__main__":
    calculation = result()
    print("MTS_CONTACT_COEFFICIENT_OWNERSHIP_AND_BOUNDS_4884")
    print(f"all_checks_pass={calculation['all_checks_pass']}")
    print(calculation["decision"])
