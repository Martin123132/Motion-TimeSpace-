from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel as parent  # noqa: E402


TARGET = 1.0e-3
K_H_PER_MPC = 1.0e-2
TEMPERATURE = 0.1
FINAL_N_VALUES = (-1.0, -0.5, 0.0)
GRID_POINTS = 8193


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def background_run() -> dict[str, Any]:
    row = next(
        row
        for row in read_csv(OUTPUT / "P8_Y5_R2FR_4890_EARLY_BACKGROUND.csv")
        if float(row["target"]) == TARGET
    )
    run = parent._early_branch_integrator(
        TARGET,
        math.log(float(row["kappa_over_H0_squared"])),
        math.log(float(row["clock_initial_scale"])),
    )
    return {"run": run, "source_row": row}


def system_matrix(
    run: dict[str, Any], n_value: float, kbar: float
) -> np.ndarray:
    basis = np.eye(9)
    return np.column_stack(
        [
            parent._mode_rhs(run, n_value, basis[:, index], kbar)
            for index in range(9)
        ]
    )


def noise_vector(run: dict[str, Any], n_value: float) -> np.ndarray:
    background = parent._background_snapshot(run, n_value)
    vector = np.zeros(9)
    vector[2] = 1.0 / background["E"] ** 2
    vector[4] = -background["field_n"] / 3.0
    return vector


def adjoint_kernel(run: dict[str, Any], final_n: float) -> dict[str, Any]:
    kbar = parent._kbar_from_h_per_mpc(K_H_PER_MPC)

    def rhs(n_value: float, adjoint: np.ndarray) -> np.ndarray:
        return -system_matrix(run, n_value, kbar).T @ adjoint

    terminal = np.zeros(9)
    terminal[0] = 1.0
    solution = solve_ivp(
        rhs,
        (final_n, parent.EARLY_INITIAL_N),
        terminal,
        method="DOP853",
        rtol=1.0e-8,
        atol=1.0e-11,
        max_step=0.01,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(f"adjoint integration failed at Nf={final_n}")
    n_values = np.linspace(parent.EARLY_INITIAL_N, final_n, GRID_POINTS)
    adjoints = solution.sol(n_values).T
    forcing = np.asarray(
        [noise_vector(run, float(n_value)) for n_value in n_values]
    )
    kernel = np.sum(adjoints * forcing, axis=1)
    delta_n = float(n_values[1] - n_values[0])
    transform = delta_n * np.fft.rfft(kernel)
    frequencies = 2.0 * math.pi * np.fft.rfftfreq(
        len(n_values), d=delta_n
    )
    return {
        "solution": solution,
        "N": n_values,
        "kernel": kernel,
        "frequency": frequencies,
        "transform": transform,
        "white_response_norm": float(
            np.trapezoid(kernel**2, x=n_values)
        ),
        "maximum_abs_kernel": float(np.max(np.abs(kernel))),
    }


def filtered_variance(
    calculation: dict[str, Any], cutoff: float, temperature: float
) -> float:
    frequency = calculation["frequency"]
    spectral_density = frequency / (
        1.0 + (frequency / cutoff) ** 2
    ) ** 2
    thermal = np.ones_like(frequency)
    positive = frequency > 0.0
    if temperature > 0.0:
        arguments = frequency[positive] / (2.0 * temperature)
        thermal[positive] = np.where(
            arguments > 30.0,
            1.0,
            1.0 / np.tanh(arguments),
        )
    spectral_density[0] = 0.0
    return float(
        np.trapezoid(
            spectral_density
            * thermal
            * np.abs(calculation["transform"]) ** 2,
            x=frequency,
        )
        / math.pi
    )


def main() -> int:
    background = background_run()
    run = background["run"]
    fdt_summary = read_csv(OUTPUT / "P8_Y5_R2FR_4891_FDT_SUMMARY.csv")[0]
    metric_power_budget = float(fdt_summary["allowed_metric_noise_power"])
    calculations = {
        final_n: adjoint_kernel(run, final_n) for final_n in FINAL_N_VALUES
    }
    response_rows: list[dict[str, Any]] = []
    cutoffs = (0.1, 0.2, 0.3, 0.4342224743487917, 1.0, 3.0, 15.0)
    for final_n, calculation in calculations.items():
        local = parent._background_snapshot(run, final_n)
        effective_mass_over_h = math.sqrt(
            3.0 * run["kappa_bar"] * local["field"] ** 2
        ) / local["E"]
        damping_over_h = parent.background.GAMMA_BAR / local["E"]
        def budget_residual(cutoff: float) -> float:
            return (
                filtered_variance(calculation, cutoff, TEMPERATURE)
                - metric_power_budget
            )

        upper_cutoff = 0.1
        while budget_residual(upper_cutoff) < 0.0 and upper_cutoff < 1.0e6:
            upper_cutoff *= 2.0
        cutoff_limit = (
            brentq(budget_residual, 1.0e-3, upper_cutoff)
            if budget_residual(upper_cutoff) >= 0.0
            else math.inf
        )
        for cutoff in cutoffs:
            variance = filtered_variance(
                calculation, cutoff, TEMPERATURE
            )
            response_rows.append(
                {
                    "final_N": final_n,
                    "final_redshift": math.exp(-final_n) - 1.0,
                    "k_h_per_Mpc": K_H_PER_MPC,
                    "temperature_per_efold": TEMPERATURE,
                    "cutoff_per_efold": cutoff,
                    "metric_noise_variance": variance,
                    "metric_power_budget": metric_power_budget,
                    "variance_to_budget_ratio": variance
                    / metric_power_budget,
                    "allowed": variance <= metric_power_budget,
                    "exact_cutoff_limit": cutoff_limit,
                    "damping_over_H": damping_over_h,
                    "memory_effective_mass_over_H": effective_mass_over_h,
                    "cutoff_limit_over_damping": cutoff_limit
                    / damping_over_h,
                    "cutoff_limit_over_memory_mass": cutoff_limit
                    / effective_mass_over_h,
                }
            )
    impulse_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4890_NOISE_RESPONSES.csv")
    final_calculation = calculations[0.0]
    impulse_checks: list[dict[str, Any]] = []
    for row in impulse_rows:
        injection_n = float(row["injection_N"])
        predicted = float(
            final_calculation["solution"].sol(injection_n)
            @ noise_vector(run, injection_n)
        )
        expected = float(row["final_metric_response"])
        impulse_checks.append(
            {
                "injection_N": injection_n,
                "adjoint_final_metric_response": predicted,
                "forward_4890_final_metric_response": expected,
                "absolute_residual": abs(predicted - expected),
                "relative_residual": abs(predicted - expected)
                / (abs(expected) + 1.0e-30),
            }
        )
    h0_per_second = (
        67.4 * 1000.0 / 3.0856775814913673e22
    )
    hbar_ev_second = 6.582119569e-16
    h0_ev = hbar_ev_second * h0_per_second
    carrier_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4890_MASS_FLOORS.csv")
    largest_carrier_floor_ev = max(
        float(row["minimum_carrier_mass_eV"]) for row in carrier_rows
    )
    today_rows = [row for row in response_rows if row["final_N"] == 0.0]
    today_cutoff_limit = today_rows[0]["exact_cutoff_limit"]
    summary = {
        "adjoint_outputs": len(FINAL_N_VALUES),
        "frequency_grid_points": GRID_POINTS // 2 + 1,
        "maximum_impulse_relative_residual": max(
            row["relative_residual"] for row in impulse_checks
        ),
        "maximum_impulse_absolute_residual": max(
            row["absolute_residual"] for row in impulse_checks
        ),
        "today_exact_cutoff_limit_at_Theta0p1": today_cutoff_limit,
        "today_candidate_Lambda0p3_variance": next(
            row["metric_noise_variance"]
            for row in today_rows
            if row["cutoff_per_efold"] == 0.3
        ),
        "today_candidate_Lambda0p3_to_budget": next(
            row["variance_to_budget_ratio"]
            for row in today_rows
            if row["cutoff_per_efold"] == 0.3
        ),
        "today_Lambda1_to_budget": next(
            row["variance_to_budget_ratio"]
            for row in today_rows
            if row["cutoff_per_efold"] == 1.0
        ),
        "today_Lambda15_to_budget": next(
            row["variance_to_budget_ratio"]
            for row in today_rows
            if row["cutoff_per_efold"] == 15.0
        ),
        "H0_eV": h0_ev,
        "largest_carrier_mass_floor_eV": largest_carrier_floor_ev,
        "largest_carrier_mass_floor_over_H0": largest_carrier_floor_ev
        / h0_ev,
        "parent_cutoff_selected": False,
        "normalized_candidate_4892_survives_exact_filter": next(
            row["allowed"]
            for row in today_rows
            if row["cutoff_per_efold"] == 0.3
        ),
        "decision": (
            "EXACT_ADJOINT_FILTER_REJECTS_THE_4892_LAMBDA0P3_STATE_AT_THE_"
            "ONE_PERCENT_TODAY_METRIC_GATE_AND_NO_EXISTING_PARENT_MASS_OR_"
            "DAMPING_SCALE_SELECTS_THE_SMALLER_ALLOWED_CUTOFF"
        ),
    }
    summary["passed"] = bool(
        summary["maximum_impulse_relative_residual"] < 1.0e-4
        and not summary["parent_cutoff_selected"]
        and not summary["normalized_candidate_4892_survives_exact_filter"]
        and today_cutoff_limit < 0.3
    )
    timestamp = datetime.now(timezone.utc).isoformat()
    for rows in (response_rows, impulse_checks, [summary]):
        for row in rows:
            row["valid_for_claim"] = False
            row["timestamp_utc"] = timestamp
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_RESPONSE.csv",
        response_rows,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_IMPULSE_CHECK.csv",
        impulse_checks,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_SUMMARY.csv",
        [summary],
    )
    print(
        "P8_Y5_R2FR_4893_FDT_ADJOINT_FILTER_PASS"
        if summary["passed"]
        else "P8_Y5_R2FR_4893_FDT_ADJOINT_FILTER_FAIL"
    )
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
