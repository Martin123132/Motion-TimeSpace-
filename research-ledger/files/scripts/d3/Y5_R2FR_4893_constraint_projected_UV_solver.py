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
K_NODES = (0.1, 0.2, 0.3)
REDSHIFTS = (1100.0, 100.0, 30.0, 10.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.0)
REDUCED_INDICES = (0, 1, 2, 4, 5, 6, 7, 8)


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
    return parent._early_branch_integrator(
        TARGET,
        math.log(float(row["kappa_over_H0_squared"])),
        math.log(float(row["clock_initial_scale"])),
    )


def expand_state(
    run: dict[str, Any],
    kbar: float,
    n_value: float,
    reduced_state: np.ndarray,
) -> np.ndarray:
    state = np.zeros(9)
    state[list(REDUCED_INDICES)] = reduced_state
    algebra = parent._mode_algebra(run, n_value, state, kbar)
    state[3] = (
        2.0
        * algebra["E"]
        * (algebra["phi_metric_n"] + state[0])
        - 3.0 * algebra["other_matter"] * state[6]
        - 4.0 * algebra["radiation"] * state[8]
        - (
            algebra["E"] * algebra["field_n"]
            - parent.background.SIGMA_BAR
        )
        * state[1]
    ) / (3.0 * algebra["clock_density"])
    return state


def solve_projected(run: dict[str, Any], k_h_per_mpc: float) -> dict[str, Any]:
    kbar = parent._kbar_from_h_per_mpc(k_h_per_mpc)
    initial_full = parent._initial_mode_state(run, kbar, 1.0e-5)
    initial_reduced = initial_full[list(REDUCED_INDICES)]

    def rhs(n_value: float, values: np.ndarray) -> np.ndarray:
        state = expand_state(run, kbar, n_value, values)
        return parent._mode_rhs(run, n_value, state, kbar)[
            list(REDUCED_INDICES)
        ]

    started = time.perf_counter()
    solution = solve_ivp(
        rhs,
        (parent.EARLY_INITIAL_N, 0.0),
        initial_reduced,
        method="DOP853",
        rtol=3.0e-10,
        atol=2.0e-14,
        max_step=min(0.01, 0.75 / max(kbar, 1.0)),
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(f"projected UV solve failed at k={k_h_per_mpc}")
    n_grid = np.linspace(-7.0, 0.0, 4001)
    states = np.asarray(
        [
            expand_state(run, kbar, float(n_value), solution.sol(n_value))
            for n_value in n_grid
        ]
    )
    clock_potential_n = np.gradient(states[:, 3], n_grid, edge_order=2)
    clock_target = np.asarray(
        [
            states[index, 0]
            / parent._background_snapshot(run, float(n_value))["E"]
            for index, n_value in enumerate(n_grid)
        ]
    )
    residual = clock_potential_n - clock_target
    return {
        "solution": solution,
        "kbar": kbar,
        "elapsed_seconds": time.perf_counter() - started,
        "nfev": int(solution.nfev),
        "clock_constraint_max_relative": float(
            np.max(np.abs(residual))
            / (np.max(np.abs(clock_target)) + 1.0e-30)
        ),
        "clock_constraint_rms_relative": float(
            np.sqrt(np.mean(residual**2))
            / (np.sqrt(np.mean(clock_target**2)) + 1.0e-30)
        ),
    }


def main() -> int:
    run = background_run()
    raw_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4893_SOLVED_TAIL_RESPONSE.csv")
    raw_lookup = {
        (float(row["k_h_per_Mpc"]), float(row["redshift"])): row
        for row in raw_rows
    }
    strict_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4891_PARENT_RESPONSE.csv")
    strict_lookup = {
        (float(row["k_h_per_Mpc"]), float(row["redshift"])): row
        for row in strict_rows
    }
    projected_rows: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    for k_h_per_mpc in K_NODES:
        calculation = solve_projected(run, k_h_per_mpc)
        profile_rows.append(
            {
                "k_h_per_Mpc": k_h_per_mpc,
                "elapsed_seconds": calculation["elapsed_seconds"],
                "nfev": calculation["nfev"],
                "clock_constraint_max_relative": calculation[
                    "clock_constraint_max_relative"
                ],
                "clock_constraint_rms_relative": calculation[
                    "clock_constraint_rms_relative"
                ],
            }
        )
        for redshift in REDSHIFTS:
            n_value = -math.log1p(redshift)
            state = expand_state(
                run,
                calculation["kbar"],
                n_value,
                calculation["solution"].sol(n_value),
            )
            raw = raw_lookup[(k_h_per_mpc, redshift)]
            matched_gr_phi = float(raw["matched_GR_Phi"])
            projected_ratio = float(state[0] / matched_gr_phi)
            raw_ratio = float(raw["Weyl_response_ratio"])
            algebra = parent._mode_algebra(
                run, n_value, state, calculation["kbar"]
            )
            momentum_scale = (
                abs(algebra["momentum_lhs"])
                + abs(algebra["momentum_rhs"])
                + 1.0e-20
            )
            projected_rows.append(
                {
                    "k_h_per_Mpc": k_h_per_mpc,
                    "redshift": redshift,
                    "N": n_value,
                    "projected_Weyl_response_ratio": projected_ratio,
                    "raw_full_system_Weyl_response_ratio": raw_ratio,
                    "projected_minus_raw_response": projected_ratio - raw_ratio,
                    "response_envelope_min": min(projected_ratio, raw_ratio),
                    "response_envelope_max": max(projected_ratio, raw_ratio),
                    "response_envelope_width": abs(projected_ratio - raw_ratio),
                    "relative_momentum_residual": abs(
                        algebra["momentum_residual"]
                    )
                    / momentum_scale,
                }
            )
    strict_repeat_residual = max(
        abs(
            row["projected_Weyl_response_ratio"]
            - float(
                strict_lookup[(0.1, row["redshift"])][
                    "Weyl_response_ratio"
                ]
            )
        )
        for row in projected_rows
        if row["k_h_per_Mpc"] == 0.1
    )
    summary = {
        "projected_k_nodes": len(K_NODES),
        "projected_rows": len(projected_rows),
        "maximum_response_envelope_width": max(
            row["response_envelope_width"] for row in projected_rows
        ),
        "maximum_projected_momentum_residual": max(
            row["relative_momentum_residual"] for row in projected_rows
        ),
        "maximum_clock_constraint_relative": max(
            row["clock_constraint_max_relative"] for row in profile_rows
        ),
        "maximum_clock_constraint_rms_relative": max(
            row["clock_constraint_rms_relative"] for row in profile_rows
        ),
        "projected_k0p1_to_strict_4891_max_abs_response_residual": (
            strict_repeat_residual
        ),
        "interpretation": (
            "raw full-system integration preserves the clock equation but loses "
            "the momentum constraint at high k; projected integration enforces "
            "momentum but leaves a measured clock-equation residual; their "
            "difference is retained as a nonclaim UV response envelope"
        ),
        "UV_point_prediction_allowed": False,
        "UV_envelope_allowed": True,
    }
    summary["passed"] = bool(
        summary["maximum_response_envelope_width"] < 2.0e-4
        and summary["maximum_projected_momentum_residual"] < 1.0e-12
        and summary["maximum_clock_constraint_relative"] < 3.0e-2
        and strict_repeat_residual < 1.0e-4
        and not summary["UV_point_prediction_allowed"]
    )
    timestamp = datetime.now(timezone.utc).isoformat()
    for rows in (projected_rows, profile_rows, [summary]):
        for row in rows:
            row["valid_for_claim"] = False
            row["timestamp_utc"] = timestamp
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_PROJECTED_UV_RESPONSE.csv",
        projected_rows,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_PROJECTED_UV_PROFILE.csv",
        profile_rows,
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4893_PROJECTED_UV_SUMMARY.csv",
        [summary],
    )
    print(
        "P8_Y5_R2FR_4893_PROJECTED_UV_BOUND_PASS"
        if summary["passed"]
        else "P8_Y5_R2FR_4893_PROJECTED_UV_BOUND_FAIL"
    )
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
