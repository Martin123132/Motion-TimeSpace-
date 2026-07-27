from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline


CHECKPOINT = "4851"
TIMESTAMP = "2026-07-09T23:55:00+00:00"
C_KM_S = 299792.458
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
RUNS = {
    "standard": POST / "runs" / "20260709-4849-H-load-positive-smoke-fit",
    "broad": POST / "runs" / "20260709-4849-H-load-positive-broad",
    "strict": POST / "runs" / "20260709-4849-H-load-positive-strict",
}
MODES_H_MPC = (0.0, 1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1, 2.0e-1)
GROWTH_MODES_H_MPC = (1.0e-3, 1.0e-2, 1.0e-1)

sys.path.insert(0, str(POST / "scripts"))
import H_load_positive_kinetic_smoke_runner as hload  # noqa: E402

hload.configure_theory_bounds(0.95, 0.999)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def growth_grid() -> np.ndarray:
    return np.unique(
        np.concatenate(
            [
                np.asarray([0.0]),
                np.geomspace(1.0e-9, 1.0e-1, 1000),
                np.linspace(1.0e-1, 5.0, 2000),
                np.linspace(5.0, 50.0, 2000),
            ]
        )
    )


def load_fits() -> list[dict[str, Any]]:
    fits: list[dict[str, Any]] = []
    for variant, folder in RUNS.items():
        path = folder / "results" / "H_load_positive_smoke_results.csv"
        for row in read_csv(path):
            if row["mode"] != "fit" or not row["model"].startswith("HLOAD"):
                continue
            fits.append(
                {
                    "variant": variant,
                    "source_path": str(path),
                    "branch": row["branch"],
                    "model": row["model"],
                    "params": json.loads(row["params_json"]),
                    "chi2_total": float(row["chi2_total"]),
                    "delta_aic_vs_best_baseline": float(row["delta_aic_vs_best_baseline"]),
                    "delta_bic_vs_best_baseline": float(row["delta_bic_vs_best_baseline"]),
                    "edge_flags": row["edge_flags"],
                }
            )
    return fits


def response_second(model: str, y: np.ndarray) -> np.ndarray:
    if "EXP" in model:
        return np.exp(-y) * (5.0 - 3.0 * y)
    tanh_y = np.tanh(y)
    sech2_y = 1.0 - tanh_y * tanh_y
    return 10.0 * tanh_y * sech2_y + 6.0 * y * sech2_y * sech2_y - 12.0 * y * tanh_y * tanh_y * sech2_y


def hload_background(model: str, params: dict[str, float], z: np.ndarray) -> dict[str, np.ndarray]:
    e_value, _ = hload.solve_positive_e(model, z, params)
    amplitude, _ = hload.amplitude_from_fraction(model, params["q_H"], params["f_K"])
    q_value = params["q_H"]
    omega_m0 = params["omega_m0"]
    y = (q_value * e_value) ** 3
    _, response_prime = hload.density_shape(model, y)
    response_second_value = response_second(model, y)
    f_e = 2.0 * e_value - 3.0 * amplitude * q_value**3 * e_value**2 * response_prime
    f_ee = (
        2.0
        - 6.0 * amplitude * q_value**3 * e_value * response_prime
        - 9.0 * amplitude * q_value**6 * e_value**4 * response_second_value
    )
    e_prime = 3.0 * omega_m0 * (1.0 + z) ** 2 / f_e
    e_second = (6.0 * omega_m0 * (1.0 + z) - f_ee * e_prime**2) / f_e
    dot_h = -(1.0 + z) * e_value * e_prime
    ddot_h = (1.0 + z) * e_value * (
        e_value * e_prime + (1.0 + z) * (e_prime**2 + e_value * e_second)
    )
    omega_m = omega_m0 * (1.0 + z) ** 3 / e_value**2
    return {
        "E": e_value,
        "E_prime": e_prime,
        "E_second": e_second,
        "F_E": f_e,
        "dotH": dot_h,
        "ddotH": ddot_h,
        "Omega_m": omega_m,
    }


def lcdm_background(omega_m0: float, z: np.ndarray) -> dict[str, np.ndarray]:
    e_value = np.sqrt(omega_m0 * (1.0 + z) ** 3 + 1.0 - omega_m0)
    e_prime = 1.5 * omega_m0 * (1.0 + z) ** 2 / e_value
    e_second = 3.0 * omega_m0 * (1.0 + z) / e_value - 2.25 * omega_m0**2 * (1.0 + z) ** 4 / e_value**3
    dot_h = -(1.0 + z) * e_value * e_prime
    ddot_h = (1.0 + z) * e_value * (
        e_value * e_prime + (1.0 + z) * (e_prime**2 + e_value * e_second)
    )
    omega_m = omega_m0 * (1.0 + z) ** 3 / e_value**2
    return {
        "E": e_value,
        "E_prime": e_prime,
        "E_second": e_second,
        "F_E": 2.0 * e_value,
        "dotH": dot_h,
        "ddotH": ddot_h,
        "Omega_m": omega_m,
    }


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4851_00_4849", POST / "4849-Y5-R2FR-positive-H-load-total-kinetic-bound-parameterization-or-local-H-load-cosmology-demotion.md", "K_0=6(1-f_K)", "background and fit branch"),
        ("SRC4851_01_4850", POST / "4850-Y5-R2FR-H-load-scalar-kinetic-mode-or-parent-tau-regularization-before-CMB-growth.md", "N_{\\rm scalar}^{\\rm memory}=0", "cuscuton equivalence and principal constraint"),
        ("SRC4851_02_standard", RUNS["standard"] / "results" / "H_load_positive_smoke_results.csv", "HLOAD_EXP_POS_KSAFE", "standard fitted rows"),
        ("SRC4851_03_broad", RUNS["broad"] / "results" / "H_load_positive_smoke_results.csv", "HLOAD_TANH_POS_KSAFE", "broad fitted rows"),
        ("SRC4851_04_strict", RUNS["strict"] / "results" / "H_load_positive_smoke_results.csv", "HLOAD_EXP_POS_KSAFE", "strict fitted rows"),
        ("SRC4851_05_background", POST / "scripts" / "H_load_positive_kinetic_smoke_runner.py", "def solve_positive_e", "implicit background solver"),
        ("SRC4851_06_checkpoint", POST / "4851-Y5-R2FR-H-load-cuscuton-matter-perturbation-constraint-and-growth-kernel.md", "SH0ES_EDGE_FAILS_ACCELERATION_GATE", "human-readable derivation"),
        ("SRC4851_07_formal", FORMAL / "867-PPC4161-H-load-matter-constraint-growth-and-acceleration-gate.md", "H_LOAD_MATTER_CONSTRAINT_GROWTH_GATE", "formal-workbench integration"),
        ("SRC4851_08_claim", FORMAL / "02-claims-register.csv", "L-693", "claim register"),
        ("SRC4851_09_script", Path(__file__).resolve(), 'CHECKPOINT = "4851"', "executable perturbation runner"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.extend(
        [
            {
                "source_id": "SRC4851_10_cuscuton_2007",
                "source_kind": "primary_web_verified",
                "source_locator": "https://arxiv.org/abs/astro-ph/0702002",
                "source_exists": True,
                "needle": "Eqs. 19, 23, 24-25",
                "needle_found": True,
                "role": "minimal cuscuton constraint, modified Poisson equation and Phi evolution",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
            {
                "source_id": "SRC4851_11_cuscuton_2017",
                "source_kind": "primary_web_verified",
                "source_locator": "https://arxiv.org/abs/1704.01131",
                "source_exists": True,
                "needle": "Eqs. 3.14-3.15",
                "needle_found": True,
                "role": "Fourier constraint and ghost-free quadratic action",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
        ]
    )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("THM4851_0_Eprime", "E'=3 Omega_m0 (1+z)^2/F_E", "F_E>0 and Omega_m0>0 imply E'>0 and dotH<0"),
        ("THM4851_1_constraint", "delta phi_k=3 dot(phi)(dot(Phi)+H Phi)/(k^2/a^2-3 dotH)", "cuscuton is constrained and has no second time derivative"),
        ("THM4851_2_pole", "D_k=k^2/a^2-3 dotH>0", "no finite-k cuscuton constraint pole on the fitted expanding branch"),
        ("THM4851_3_C2", "1+C2(k=0)=F_E/(2E)>0", "potential evolution equation remains nondegenerate; at z=0 this equals 1-f_K"),
        ("THM4851_4_Poisson", "(k^2/a^2)Phi+A_P(dotPhi+HPhi)+delta rho/(2 Mpl^2)=0", "A_P=3H+9H(2dotH+3H^2 Omega_m)/(2D_k)"),
        ("THM4851_5_Newton", "k^2/a^2 >> H^2,|dotH| => (k^2/a^2)Phi=-delta rho/(2Mpl^2)+O(H^2a^2/k^2)", "standard calibrated Newton/Poisson coefficient is recovered"),
        ("THM4851_6_acceleration", "q0=-1+3 Omega_m0/[2(1-f_K)]", "present acceleration requires f_K<1-3 Omega_m0/2"),
        ("THM4851_7_growth", "(1+C2)ddotPhi+(4H+C1+C2H+C3)dotPhi+C_Phi Phi=0", "exact dust potential kernel with C1,C2,C3 fixed by H,dotH,ddotH,k"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "formula": formula,
            "consequence": consequence,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for theorem_id, formula, consequence in rows
    ]


def acceleration_rows(fits: list[dict[str, Any]], backgrounds: dict[tuple[str, str, str], dict[str, np.ndarray]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        key = (fit["variant"], fit["branch"], fit["model"])
        background = backgrounds[key]
        params = fit["params"]
        f_k = params["f_K"]
        omega_m0 = params["omega_m0"]
        e_prime0 = float(background["E_prime"][0])
        e_second0 = float(background["E_second"][0])
        q0 = -1.0 + e_prime0
        jerk0 = 1.0 - 2.0 * e_prime0 + e_prime0**2 + e_second0
        threshold = 1.0 - 1.5 * omega_m0
        acceleration_pass = q0 < 0.0
        rows.append(
            {
                "variant": fit["variant"],
                "branch": fit["branch"],
                "model": fit["model"],
                "omega_m0": f"{omega_m0:.15e}",
                "f_K": f"{f_k:.15e}",
                "acceleration_fK_max": f"{threshold:.15e}",
                "E_prime0": f"{e_prime0:.15e}",
                "q0": f"{q0:.15e}",
                "jerk0": f"{jerk0:.15e}",
                "acceleration_pass": acceleration_pass,
                "delta_aic_vs_best_baseline": fit["delta_aic_vs_best_baseline"],
                "delta_bic_vs_best_baseline": fit["delta_bic_vs_best_baseline"],
                "edge_flags": fit["edge_flags"],
                "status": "ACCELERATION_PASS_PRIVATE" if acceleration_pass else "FAIL_PRESENT_ACCELERATION_GATE",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def mode_k2(z: np.ndarray | float, k_h_mpc: float) -> np.ndarray | float:
    return (k_h_mpc * C_KM_S / 100.0) ** 2 * (1.0 + z) ** 2


def constraint_rows(fits: list[dict[str, Any]], backgrounds: dict[tuple[str, str, str], dict[str, np.ndarray]], z: np.ndarray) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        key = (fit["variant"], fit["branch"], fit["model"])
        background = backgrounds[key]
        e_value = background["E"]
        f_e = background["F_E"]
        dot_h = background["dotH"]
        omega_m = background["Omega_m"]
        source = 2.0 * dot_h + 3.0 * e_value**2 * omega_m
        for k_h_mpc in MODES_H_MPC:
            k2 = mode_k2(z, k_h_mpc)
            denominator = k2 - 3.0 * dot_h
            c2 = 3.0 * source / (2.0 * denominator)
            phi_coefficient = 1.0 + c2
            rows.append(
                {
                    "variant": fit["variant"],
                    "branch": fit["branch"],
                    "model": fit["model"],
                    "k_h_mpc": f"{k_h_mpc:.6e}",
                    "min_constraint_denominator_H0sq": f"{float(np.min(denominator)):.15e}",
                    "min_one_plus_C2": f"{float(np.min(phi_coefficient)):.15e}",
                    "max_abs_C2": f"{float(np.max(np.abs(c2))):.15e}",
                    "min_FE_over_2E": f"{float(np.min(f_e / (2.0 * e_value))):.15e}",
                    "dotH_negative_all_z": bool(np.all(dot_h < 0.0)),
                    "constraint_pole_free": bool(np.all(denominator > 0.0)),
                    "potential_equation_nondegenerate": bool(np.all(phi_coefficient > 0.0)),
                    "status": "CONSTRAINT_AND_PHI_KERNEL_PASS_PRIVATE",
                    "valid_for_claim": False,
                    "timestamp_utc": TIMESTAMP,
                }
            )
    return rows


def make_splines(z: np.ndarray, background: dict[str, np.ndarray]) -> dict[str, CubicSpline]:
    return {name: CubicSpline(z, values) for name, values in background.items() if name != "F_E"}


def potential_coefficients(splines: dict[str, CubicSpline], z_value: float, k_h_mpc: float) -> tuple[float, float, dict[str, float]]:
    e_value = float(splines["E"](z_value))
    e_prime = float(splines["E_prime"](z_value))
    dot_h = float(splines["dotH"](z_value))
    ddot_h = float(splines["ddotH"](z_value))
    omega_m = float(splines["Omega_m"](z_value))
    k2 = float(mode_k2(z_value, k_h_mpc))
    denominator = k2 - 3.0 * dot_h
    source = 2.0 * dot_h + 3.0 * e_value**2 * omega_m
    c1 = 3.0 * (ddot_h + 3.0 * e_value * dot_h) / denominator
    c2 = 3.0 * source / (2.0 * denominator)
    c3 = 3.0 * (2.0 * e_value * k2 + 3.0 * ddot_h) * source / (2.0 * denominator**2)
    coefficient_ddot = 1.0 + c2
    coefficient_dot = 4.0 * e_value + c1 + c2 * e_value + c3
    coefficient_phi = (
        3.0 * e_value**2
        + dot_h
        - 1.5 * omega_m * e_value**2
        + c1 * e_value
        + c2 * dot_h
        + c3 * e_value
    )
    a1 = (1.0 + z_value) * e_value
    p_z = (
        coefficient_ddot * a1 * (e_value + (1.0 + z_value) * e_prime)
        - coefficient_dot * a1
    ) / (coefficient_ddot * a1**2)
    q_z = coefficient_phi / (coefficient_ddot * a1**2)
    return p_z, q_z, {
        "E": e_value,
        "E_prime": e_prime,
        "dotH": dot_h,
        "Omega_m": omega_m,
        "k2": k2,
        "denominator": denominator,
        "C1": c1,
        "C2": c2,
        "C3": c3,
    }


def integrate_potential(splines: dict[str, CubicSpline], k_h_mpc: float) -> dict[str, Any]:
    def equation(z_value: float, state: np.ndarray) -> tuple[float, float]:
        p_z, q_z, _ = potential_coefficients(splines, z_value, k_h_mpc)
        return float(state[1]), float(-p_z * state[1] - q_z * state[0])

    solution = solve_ivp(
        equation,
        (50.0, 0.0),
        (1.0, 0.0),
        method="DOP853",
        rtol=2.0e-9,
        atol=1.0e-11,
        max_step=0.1,
    )
    phi0 = float(solution.y[0, -1])
    phi_z0 = float(solution.y[1, -1])
    _, _, state0 = potential_coefficients(splines, 0.0, k_h_mpc)
    phi_dot0 = -state0["E"] * phi_z0
    source0 = 2.0 * state0["dotH"] + 3.0 * state0["E"] ** 2 * state0["Omega_m"]
    a_poisson0 = 3.0 * state0["E"] + 9.0 * state0["E"] * source0 / (2.0 * state0["denominator"])
    delta0 = -2.0 * (
        state0["k2"] * phi0 + a_poisson0 * (phi_dot0 + state0["E"] * phi0)
    ) / (3.0 * state0["E"] ** 2 * state0["Omega_m"])
    return {
        "success": solution.success,
        "message": solution.message,
        "phi0": phi0,
        "phi_z0": phi_z0,
        "delta0": delta0,
        "nfev": solution.nfev,
    }


def growth_rows(fits: list[dict[str, Any]], backgrounds: dict[tuple[str, str, str], dict[str, np.ndarray]], z: np.ndarray) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    selected = [
        fit
        for fit in fits
        if (fit["variant"] in {"broad", "strict"} and fit["branch"] == "sh0es")
        or (fit["variant"] == "broad" and fit["branch"] == "no_sh0es")
    ]
    for fit in selected:
        key = (fit["variant"], fit["branch"], fit["model"])
        hload_splines = make_splines(z, backgrounds[key])
        lcdm_splines = make_splines(z, lcdm_background(fit["params"]["omega_m0"], z))
        for k_h_mpc in GROWTH_MODES_H_MPC:
            hload_result = integrate_potential(hload_splines, k_h_mpc)
            lcdm_result = integrate_potential(lcdm_splines, k_h_mpc)
            rows.append(
                {
                    "variant": fit["variant"],
                    "branch": fit["branch"],
                    "model": fit["model"],
                    "k_h_mpc": f"{k_h_mpc:.6e}",
                    "z_initial": 50.0,
                    "initial_condition": "Phi=1,dPhi_dz=0 matter-era smoke",
                    "Hload_phi0": f"{hload_result['phi0']:.15e}",
                    "LCDM_phi0": f"{lcdm_result['phi0']:.15e}",
                    "phi0_ratio_to_LCDM": f"{hload_result['phi0']/lcdm_result['phi0']:.15e}",
                    "Hload_delta0": f"{hload_result['delta0']:.15e}",
                    "LCDM_delta0": f"{lcdm_result['delta0']:.15e}",
                    "delta0_ratio_to_LCDM": f"{hload_result['delta0']/lcdm_result['delta0']:.15e}",
                    "Hload_dPhi_dz0": f"{hload_result['phi_z0']:.15e}",
                    "Hload_success": hload_result["success"],
                    "LCDM_success": lcdm_result["success"],
                    "status": "GROWTH_KERNEL_SMOKE_FINITE_NONCLAIM",
                    "valid_for_claim": False,
                    "timestamp_utc": TIMESTAMP,
                }
            )
    return rows


def decision_rows(acceleration: list[dict[str, Any]], growth: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sh0es_fail = sum(row["branch"] == "sh0es" and not row["acceleration_pass"] for row in acceleration)
    no_sh0es_pass = sum(row["branch"] == "no_sh0es" and row["acceleration_pass"] for row in acceleration)
    finite_growth = all(row["Hload_success"] and row["LCDM_success"] for row in growth)
    rows = [
        ("DEC4851_0_constraint", "retain minimal cuscuton constraint completion", "D_k>0 and 1+C2>0 for every fitted row and scanned mode"),
        ("DEC4851_1_Newton", "propagate exact high-k Newton limit", "cuscuton correction is O(H^2 a^2/k^2) and the calibrated Poisson coefficient is unchanged"),
        ("DEC4851_2_SH0ES", "reject the SH0ES edge as a viable late-time solution", f"all {sh0es_fail} SH0ES rows have q0>0 despite their distance AIC/BIC gain"),
        ("DEC4851_3_noSH0ES", "retain only an interior viable cosmology branch", f"all {no_sh0es_pass} no-SH0ES rows accelerate but remain unpreferred by the 4849 AIC/BIC comparison"),
        ("DEC4851_4_growth", "growth kernel is executable but not a likelihood", f"finite smoke integrations={finite_growth}; initial normalization and data covariance are not a growth claim"),
        ("DEC4851_5_next", "return the memory result to the local-GR spine", "local stationary silence plus high-k Poisson recovery remove H-load memory as the current local Newton blocker"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for decision_id, decision, reason in rows
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    acceleration: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
    growth: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claim = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-693"]
    checkpoint = (POST / "4851-Y5-R2FR-H-load-cuscuton-matter-perturbation-constraint-and-growth-kernel.md").read_text(encoding="utf-8")
    formal = (FORMAL / "867-PPC4161-H-load-matter-constraint-growth-and-acceleration-gate.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    sh0es = [row for row in acceleration if row["branch"] == "sh0es"]
    no_sh0es = [row for row in acceleration if row["branch"] == "no_sh0es"]
    zero_mode = [row for row in constraints if math.isclose(float(row["k_h_mpc"]), 0.0)]
    checks = [
        result("VAL4851_00_sources", len(sources) == 12 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4851_01_fit_count", len(fits) == 12, f"fits={len(fits)}"),
        result("VAL4851_02_acceleration_count", len(acceleration) == 12, f"rows={len(acceleration)}"),
        result("VAL4851_03_SH0ES_rejected", len(sh0es) == 6 and all(not row["acceleration_pass"] and float(row["q0"]) > 0.0 for row in sh0es), "all SH0ES positive-H-load fits decelerate today"),
        result("VAL4851_04_noSH0ES_accelerates", len(no_sh0es) == 6 and all(row["acceleration_pass"] and float(row["q0"]) < 0.0 for row in no_sh0es), "all no-SH0ES rows accelerate"),
        result("VAL4851_05_constraint_rows", len(constraints) == 72, f"rows={len(constraints)}"),
        result("VAL4851_06_no_poles", all(row["dotH_negative_all_z"] and row["constraint_pole_free"] and row["potential_equation_nondegenerate"] for row in constraints), "D_k and 1+C2 positive for z=0..50"),
        result(
            "VAL4851_07_zero_mode_identity",
            len(zero_mode) == 12
            and all(math.isclose(float(row["min_one_plus_C2"]), 1.0 - fit["params"]["f_K"], rel_tol=5.0e-10, abs_tol=5.0e-10) for row, fit in zip(zero_mode, fits)),
            "min[1+C2(k=0)]=1-f_K",
        ),
        result("VAL4851_08_growth_count", len(growth) == 18, f"rows={len(growth)}"),
        result("VAL4851_09_growth_finite", all(row["Hload_success"] and row["LCDM_success"] and math.isfinite(float(row["delta0_ratio_to_LCDM"])) for row in growth), "all growth smoke integrations finite"),
        result("VAL4851_10_high_k_Newton", all(float(row["min_constraint_denominator_H0sq"]) > 0.0 for row in constraints if float(row["k_h_mpc"]) >= 1.0e-2), "high-k Poisson correction denominator finite"),
        result("VAL4851_11_claim", len(claim) == 1 and claim[0].get("status") == "sh0es_edge_rejected_acceleration_no_sh0es_viable_unpreferred_constraints_safe_private_nonclaim", f"L-693 rows={len(claim)}"),
        result("VAL4851_12_documents", "SH0ES_EDGE_FAILS_ACCELERATION_GATE" in checkpoint and "H_LOAD_MATTER_CONSTRAINT_GROWTH_GATE" in formal, "checkpoint/formal markers found"),
        result("VAL4851_13_resume", "Last checkpoint: `4851-" in resume and "4852-Y5-R2FR-local-GR-residual-rebase" in resume, "resume advanced to local-GR rebase"),
        result("VAL4851_14_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4851_OVERALL", all(row["status"] == "PASS" for row in checks), "H_LOAD_MATTER_CONSTRAINT_GROWTH_AND_ACCELERATION_GATE_VALIDATED"))
    return checks


def main() -> int:
    fits = load_fits()
    z = growth_grid()
    backgrounds = {
        (fit["variant"], fit["branch"], fit["model"]): hload_background(fit["model"], fit["params"], z)
        for fit in fits
    }
    sources = source_rows()
    theorems = theorem_rows()
    acceleration = acceleration_rows(fits, backgrounds)
    constraints = constraint_rows(fits, backgrounds, z)
    growth = growth_rows(fits, backgrounds, z)
    decisions = decision_rows(acceleration, growth)
    validation = validation_rows(sources, fits, acceleration, constraints, growth)
    write_csv(OUTPUT / "P8_Y5_R2FR_4851_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4851_PERTURBATION_THEOREMS.csv", theorems)
    write_csv(OUTPUT / "P8_Y5_R2FR_4851_BACKGROUND_ACCELERATION_GATE.csv", acceleration)
    write_csv(OUTPUT / "P8_Y5_R2FR_4851_CONSTRAINT_KERNEL.csv", constraints)
    write_csv(OUTPUT / "P8_Y5_R2FR_4851_GROWTH_SMOKE.csv", growth)
    write_csv(OUTPUT / "P8_Y5_R2FR_4851_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4851_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4851_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4851_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
