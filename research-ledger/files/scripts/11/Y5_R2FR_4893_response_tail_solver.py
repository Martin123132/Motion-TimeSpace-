from __future__ import annotations

import csv
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel as parent  # noqa: E402


TARGET = 1.0e-3
AMPLITUDE = 1.0e-5
REDShIFTS = (1100.0, 100.0, 30.0, 10.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.0)
SOLVED_K_NODES = (
    0.0,
    1.0e-5,
    3.0e-5,
    1.0e-4,
    3.0e-4,
    5.0e-4,
    7.0e-4,
    1.0e-1,
    2.0e-1,
    3.0e-1,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def validated_background() -> dict[str, Any]:
    path = OUTPUT / "P8_Y5_R2FR_4890_EARLY_BACKGROUND.csv"
    row = next(
        row for row in read_csv(path) if float(row["target"]) == TARGET
    )
    kappa = float(row["kappa_over_H0_squared"])
    clock_scale = float(row["clock_initial_scale"])
    run = parent._early_branch_integrator(
        TARGET, math.log(kappa), math.log(clock_scale)
    )
    early_matter = (
        parent.background.OMEGA_OTHER_M
        + parent.background.OMEGA_X * clock_scale
    )
    return {
        "source_path": str(path),
        "source_row": row,
        "run": run,
        "kappa": kappa,
        "clock_scale": clock_scale,
        "early_matter": early_matter,
        "passed": bool(
            abs(run["memory_today"] - TARGET) < 1.0e-12
            and abs(run["clock_today"] - parent.background.OMEGA_X) < 1.0e-12
            and abs(run["E_today"] - 1.0) < 1.0e-12
        ),
    }


def gr_algebra(
    early_matter: float,
    n_value: float,
    state: np.ndarray,
    kbar: float,
) -> dict[str, float]:
    radiation = parent.background.OMEGA_R * math.exp(-4.0 * n_value)
    matter = early_matter * math.exp(-3.0 * n_value)
    cosmological_constant = 1.0 - parent.background.OMEGA_R - early_matter
    e_squared = radiation + matter + cosmological_constant
    e_value = math.sqrt(e_squared)
    k2 = kbar**2 * math.exp(-2.0 * n_value)
    phi_metric, matter_delta, _, radiation_delta, _ = state
    phi_metric_n = (
        -phi_metric
        - k2 * phi_metric / (3.0 * e_squared)
        - (matter * matter_delta + radiation * radiation_delta)
        / (2.0 * e_squared)
    )
    return {
        "radiation": radiation,
        "matter": matter,
        "E": e_value,
        "k2": k2,
        "phi_metric_n": phi_metric_n,
    }


def solve_gr_mode(early_matter: float, k_h_per_mpc: float) -> dict[str, Any]:
    kbar = parent._kbar_from_h_per_mpc(k_h_per_mpc)
    n_initial = parent.EARLY_INITIAL_N
    state = np.asarray(
        [AMPLITUDE, -1.5 * AMPLITUDE, 0.0, -2.0 * AMPLITUDE, 0.0]
    )
    initial = gr_algebra(early_matter, n_initial, state, kbar)
    denominator = 3.0 * initial["matter"] + 4.0 * initial["radiation"]
    common_potential = (
        2.0
        * initial["E"]
        * (initial["phi_metric_n"] + AMPLITUDE)
        / denominator
    )
    state[2] = common_potential
    state[4] = common_potential

    def rhs(n_value: float, values: np.ndarray) -> np.ndarray:
        local = gr_algebra(early_matter, n_value, values, kbar)
        metric, _, matter_potential, radiation_delta, radiation_potential = values
        return np.asarray(
            [
                local["phi_metric_n"],
                3.0 * local["phi_metric_n"]
                - local["k2"] * matter_potential / local["E"],
                metric / local["E"],
                4.0 * local["phi_metric_n"]
                - 4.0
                * local["k2"]
                * radiation_potential
                / (3.0 * local["E"]),
                radiation_potential
                + (metric + radiation_delta / 4.0) / local["E"],
            ]
        )

    high_k = k_h_per_mpc >= 5.0e-2
    rtol = 3.0e-8 if high_k else 3.0e-10
    atol = 3.0e-12 if high_k else 2.0e-14
    max_step = (
        min(0.02, 2.5 / max(kbar, 1.0))
        if high_k
        else min(0.01, 0.75 / max(kbar, 1.0))
    )
    started = time.perf_counter()
    solution = solve_ivp(
        rhs,
        (n_initial, 0.0),
        state,
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(f"matched GR tail mode failed at k={k_h_per_mpc}")
    return {
        "solution": solution,
        "elapsed_seconds": time.perf_counter() - started,
        "nfev": int(solution.nfev),
        "rtol": rtol,
        "atol": atol,
        "max_step": max_step,
    }


def solve_parent_mode(run: dict[str, Any], k_h_per_mpc: float) -> dict[str, Any]:
    kbar = parent._kbar_from_h_per_mpc(k_h_per_mpc)
    state = parent._initial_mode_state(run, kbar, AMPLITUDE)
    high_k = k_h_per_mpc >= 5.0e-2
    rtol = 3.0e-8 if high_k else 3.0e-10
    atol = 3.0e-12 if high_k else 2.0e-14
    max_step = (
        min(0.02, 2.5 / max(kbar, 1.0))
        if high_k
        else min(0.01, 0.75 / max(kbar, 1.0))
    )
    started = time.perf_counter()
    solution = solve_ivp(
        lambda n_value, values: parent._mode_rhs(
            run, n_value, values, kbar
        ),
        (parent.EARLY_INITIAL_N, 0.0),
        state,
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(f"parent tail mode failed at k={k_h_per_mpc}")
    initial_bg = parent._background_snapshot(run, parent.EARLY_INITIAL_N)
    initial_k_over_a_h = (
        kbar
        * math.exp(-parent.EARLY_INITIAL_N)
        / initial_bg["E"]
    )
    return {
        "solution": solution,
        "elapsed_seconds": time.perf_counter() - started,
        "nfev": int(solution.nfev),
        "rtol": rtol,
        "atol": atol,
        "max_step": max_step,
        "initial_k_over_aH": initial_k_over_a_h,
    }


def solve_response() -> dict[str, Any]:
    background = validated_background()
    run = background["run"]
    response_rows: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    for k_h_per_mpc in SOLVED_K_NODES:
        parent_mode = solve_parent_mode(run, k_h_per_mpc)
        gr_mode = solve_gr_mode(background["early_matter"], k_h_per_mpc)
        profile_rows.append(
            {
                "k_h_per_Mpc": k_h_per_mpc,
                "parent_elapsed_seconds": parent_mode["elapsed_seconds"],
                "GR_elapsed_seconds": gr_mode["elapsed_seconds"],
                "parent_nfev": parent_mode["nfev"],
                "GR_nfev": gr_mode["nfev"],
                "rtol": parent_mode["rtol"],
                "atol": parent_mode["atol"],
                "max_step": parent_mode["max_step"],
                "initial_k_over_aH": parent_mode["initial_k_over_aH"],
            }
        )
        kbar = parent._kbar_from_h_per_mpc(k_h_per_mpc)
        for redshift in REDShIFTS:
            n_value = -math.log1p(redshift)
            parent_state = parent_mode["solution"].sol(n_value)
            gr_state = gr_mode["solution"].sol(n_value)
            parent_phi = float(parent_state[0])
            gr_phi = float(gr_state[0])
            algebra = parent._mode_algebra(run, n_value, parent_state, kbar)
            momentum_scale = (
                abs(algebra["momentum_lhs"])
                + abs(algebra["momentum_rhs"])
                + 1.0e-20
            )
            response_rows.append(
                {
                    "k_h_per_Mpc": k_h_per_mpc,
                    "redshift": redshift,
                    "N": n_value,
                    "parent_Phi": parent_phi,
                    "matched_GR_Phi": gr_phi,
                    "Weyl_response_ratio": parent_phi / gr_phi,
                    "fractional_Weyl_response": parent_phi / gr_phi - 1.0,
                    "relative_momentum_residual": abs(
                        algebra["momentum_residual"]
                    )
                    / momentum_scale,
                }
            )
    return {
        "background": background,
        "response_rows": response_rows,
        "profile_rows": profile_rows,
    }


def asymptotic_rows(response_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lookup = {
        (row["k_h_per_Mpc"], row["redshift"]): row[
            "Weyl_response_ratio"
        ]
        for row in response_rows
    }
    existing = read_csv(OUTPUT / "P8_Y5_R2FR_4891_PARENT_RESPONSE.csv")
    for row in existing:
        lookup[(float(row["k_h_per_Mpc"]), float(row["redshift"]))] = float(
            row["Weyl_response_ratio"]
        )
    rows: list[dict[str, Any]] = []
    fit_k = np.asarray([0.1, 0.2, 0.3])
    fit_x = 1.0 / fit_k**2
    for redshift in REDShIFTS:
        fit_y = np.asarray([lookup[(k_value, redshift)] for k_value in fit_k])
        coefficient, intercept = np.polyfit(fit_x, fit_y, 1)
        predicted = intercept + coefficient * fit_x
        rows.append(
            {
                "redshift": redshift,
                "N": -math.log1p(redshift),
                "R_W_infinity": float(intercept),
                "inverse_k_squared_coefficient": float(coefficient),
                "maximum_abs_fit_residual": float(
                    np.max(np.abs(predicted - fit_y))
                ),
                "fit_k_min_h_per_Mpc": 0.1,
                "fit_k_max_h_per_Mpc": 0.3,
                "asymptotic_equation": "R_W=R_infinity+A_2/k_h^2+O(k_h^-4)",
            }
        )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    calculation = solve_response()
    response_rows = calculation["response_rows"]
    profile_rows = calculation["profile_rows"]
    asymptotic = asymptotic_rows(response_rows)
    prior_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4891_PARENT_RESPONSE.csv")
    prior_lookup = {
        (float(row["k_h_per_Mpc"]), float(row["redshift"])): float(
            row["Weyl_response_ratio"]
        )
        for row in prior_rows
    }
    new_lookup = {
        (row["k_h_per_Mpc"], row["redshift"]): row[
            "Weyl_response_ratio"
        ]
        for row in response_rows
    }
    repeat_residual = max(
        abs(new_lookup[(0.1, redshift)] - prior_lookup[(0.1, redshift)])
        for redshift in REDShIFTS
    )
    ir_continuity = max(
        abs(
            new_lookup[(1.0e-5, redshift)]
            - new_lookup[(0.0, redshift)]
        )
        for redshift in REDShIFTS
    )
    summary = {
        "target": TARGET,
        "N_initial": parent.EARLY_INITIAL_N,
        "solved_k_nodes": len(SOLVED_K_NODES),
        "response_rows": len(response_rows),
        "repeat_k0p1_max_abs_R_residual": repeat_residual,
        "IR_k1e5_to_k0_max_abs_R_residual": ir_continuity,
        "UV_max_abs_inverse_k2_fit_residual": max(
            row["maximum_abs_fit_residual"] for row in asymptotic
        ),
        "maximum_relative_momentum_residual": max(
            row["relative_momentum_residual"] for row in response_rows
        ),
        "maximum_initial_k_over_aH": max(
            row["initial_k_over_aH"] for row in profile_rows
        ),
        "elapsed_seconds": time.perf_counter() - started,
        "background_source": calculation["background"]["source_path"],
        "background_passed": calculation["background"]["passed"],
    }
    summary["passed"] = bool(
        summary["background_passed"]
        and repeat_residual < 2.0e-5
        and ir_continuity < 1.0e-6
        and summary["maximum_relative_momentum_residual"] < 5.0e-3
        and summary["maximum_initial_k_over_aH"] < 0.1
    )
    timestamp = datetime.now(timezone.utc).isoformat()
    for rows in (response_rows, profile_rows, asymptotic, [summary]):
        for row in rows:
            row["valid_for_claim"] = False
            row["timestamp_utc"] = timestamp
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_SOLVED_TAIL_RESPONSE.csv",
        response_rows,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_TAIL_SOLVER_PROFILE.csv",
        profile_rows,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_UV_ASYMPTOTIC.csv",
        asymptotic,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_TAIL_SOLVER_SUMMARY.csv",
        [summary],
    )
    print(
        "P8_Y5_R2FR_4893_TAIL_SOLVER_PASS"
        if summary["passed"]
        else "P8_Y5_R2FR_4893_TAIL_SOLVER_FAIL"
    )
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
