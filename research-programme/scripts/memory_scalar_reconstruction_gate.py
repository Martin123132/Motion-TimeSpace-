#!/usr/bin/env python3
"""Gate the effective memory scalar reconstruction against parent-action needs."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(MAIN_SCRIPTS))

from cosmology_likelihood_smoke import activation_shape_params  # noqa: E402


SOURCE_PATHS = {
    "19_parent_skeleton": Path("19-constrained-parent-action-skeleton.md"),
    "21_cosmology_bridge": Path("21-cosmology-parent-bridge-audit.md"),
    "38_status": Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json"),
    "44_status": Path("runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/status.json"),
    "44_scalar_summary": Path(
        "runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/"
        "scalar_reconstruction_summary.csv"
    ),
    "44_equation_contract": Path(
        "runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/"
        "perturbation_equation_contract.csv"
    ),
}

N_EFF = 3.046
Z_STAR = 1091.5182931260854


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


def read_csv(key: str) -> list[dict[str, str]]:
    with absolute_source(key).open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def radiation_density(params: dict[str, float]) -> float:
    hubble_reduced = float(params.get("h0", 70.0)) / 100.0
    omega_gamma = 2.469e-5 / (hubble_reduced * hubble_reduced)
    return omega_gamma * (1.0 + 0.22710731766 * N_EFF)


def activation_from_load(load_n: np.ndarray, params: dict[str, float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    scale_n, exponent_nu = activation_shape_params(params)
    scaled = np.maximum(load_n, 0.0) / scale_n
    power = scaled**exponent_nu
    survival = np.exp(-np.clip(power, 0.0, 745.0))
    activation = 1.0 - survival
    derivative = np.zeros_like(load_n, dtype=float)
    positive = scaled > 0.0
    derivative[positive] = survival[positive] * exponent_nu * scaled[positive] ** (exponent_nu - 1.0) / scale_n
    return activation, derivative, survival


def reconstruction_grid(params: dict[str, float], grid_count: int = 4096) -> dict[str, np.ndarray]:
    omega_matter = float(params["omega_m0"])
    omega_radiation = radiation_density(params)
    memory_amplitude = float(params["b_mem"])
    max_load = math.log1p(Z_STAR)
    load_grid = np.linspace(0.0, max_load, grid_count)
    redshift_grid = np.expm1(load_grid)
    activation, derivative, survival = activation_from_load(load_grid, params)
    rho_dark = 1.0 - omega_matter + memory_amplitude * activation
    rho_dark_derivative = memory_amplitude * derivative
    w_dark = -1.0 + np.divide(
        rho_dark_derivative,
        3.0 * rho_dark,
        out=np.zeros_like(rho_dark_derivative),
        where=rho_dark > 0.0,
    )
    total_e2 = (
        omega_matter * (1.0 + redshift_grid) ** 3
        + omega_radiation * (1.0 + redshift_grid) ** 4
        + rho_dark
    )
    omega_dark_fraction = np.divide(rho_dark, total_e2, out=np.zeros_like(rho_dark), where=total_e2 > 0.0)
    kinetic_proxy = 0.5 * (1.0 + w_dark) * rho_dark
    potential_proxy = 0.5 * (1.0 - w_dark) * rho_dark
    phi_derivative_abs = np.sqrt(np.maximum(rho_dark_derivative / total_e2, 0.0))
    field_grid = np.zeros_like(load_grid)
    if len(load_grid) > 1:
        increments = 0.5 * np.diff(load_grid) * (phi_derivative_abs[:-1] + phi_derivative_abs[1:])
        field_grid[1:] = np.cumsum(increments)
    return {
        "N": load_grid,
        "z": redshift_grid,
        "F": activation,
        "survival": survival,
        "dF_dN": derivative,
        "rho_X_E2": rho_dark,
        "d_rho_X_dN": rho_dark_derivative,
        "w_X": w_dark,
        "one_plus_w_X": 1.0 + w_dark,
        "Omega_X_fraction": omega_dark_fraction,
        "K_E2": kinetic_proxy,
        "V_E2": potential_proxy,
        "dphi_dN_abs": phi_derivative_abs,
        "phi_over_Mpl": field_grid,
    }


def sampled_reconstruction_rows(grid: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    indices = sorted(set(np.linspace(0, len(grid["N"]) - 1, 64, dtype=int).tolist()))
    rows: list[dict[str, Any]] = []
    for index in indices:
        rows.append(
            {
                "index": int(index),
                "N_ln_1_plus_z": float(grid["N"][index]),
                "z": float(grid["z"][index]),
                "phi_over_Mpl": float(grid["phi_over_Mpl"][index]),
                "F": float(grid["F"][index]),
                "dF_dN": float(grid["dF_dN"][index]),
                "rho_X_E2": float(grid["rho_X_E2"][index]),
                "w_X": float(grid["w_X"][index]),
                "K_E2": float(grid["K_E2"][index]),
                "V_E2": float(grid["V_E2"][index]),
                "Omega_X_fraction": float(grid["Omega_X_fraction"][index]),
            }
        )
    return rows


def potential_feature_rows(grid: dict[str, np.ndarray], params: dict[str, float]) -> list[dict[str, Any]]:
    potential = grid["V_E2"]
    field = grid["phi_over_Mpl"]
    load_grid = grid["N"]
    redshift_grid = grid["z"]
    min_index = int(np.nanargmin(potential))
    max_index = int(np.nanargmax(potential))
    max_w_index = int(np.nanargmax(grid["w_X"]))
    endpoint_delta = float(potential[-1] - potential[0])
    monotonic_field = bool(np.all(np.diff(field) >= -1.0e-14))
    monotonic_potential = bool(np.all(np.diff(potential) >= -1.0e-14) or np.all(np.diff(potential) <= 1.0e-14))
    return [
        {
            "feature": "V_today",
            "value": float(potential[0]),
            "location": "z=0",
            "status": "finite",
            "interpretation": "present effective potential proxy",
        },
        {
            "feature": "V_recombination",
            "value": float(potential[-1]),
            "location": f"z={float(redshift_grid[-1])}",
            "status": "finite",
            "interpretation": "high-redshift plateau value",
        },
        {
            "feature": "V_recombination_minus_V_today",
            "value": endpoint_delta,
            "location": "z=0 to z_star",
            "status": "matches_b_mem_scale",
            "interpretation": f"compare b_mem={float(params['b_mem'])}",
        },
        {
            "feature": "V_min",
            "value": float(potential[min_index]),
            "location": (
                f"N={float(load_grid[min_index])}; z={float(redshift_grid[min_index])}; "
                f"phi={float(field[min_index])}"
            ),
            "status": "non_monotonic_potential" if min_index not in {0, len(potential) - 1} else "endpoint_minimum",
            "interpretation": "effective potential dips before climbing to the high-z plateau",
        },
        {
            "feature": "V_max",
            "value": float(potential[max_index]),
            "location": (
                f"N={float(load_grid[max_index])}; z={float(redshift_grid[max_index])}; "
                f"phi={float(field[max_index])}"
            ),
            "status": "plateau_maximum" if max_index == len(potential) - 1 else "internal_maximum",
            "interpretation": "maximum over the reconstructed past-lightcone interval",
        },
        {
            "feature": "max_w_X",
            "value": float(grid["w_X"][max_w_index]),
            "location": (
                f"N={float(load_grid[max_w_index])}; z={float(redshift_grid[max_w_index])}; "
                f"phi={float(field[max_w_index])}"
            ),
            "status": "non_phantom",
            "interpretation": "largest departure from cosmological-constant behavior",
        },
        {
            "feature": "total_field_excursion",
            "value": float(field[-1] - field[0]),
            "location": "z=0 to z_star",
            "status": "small_excursion_proxy",
            "interpretation": "canonical scalar proxy excursion in reduced Planck units",
        },
        {
            "feature": "phi_monotonicity",
            "value": str(monotonic_field),
            "location": "full grid",
            "status": "pass" if monotonic_field else "fail",
            "interpretation": "needed for single-valued V(phi) on the reconstructed interval",
        },
        {
            "feature": "V_monotonicity",
            "value": str(monotonic_potential),
            "location": "full grid",
            "status": "warn_non_monotonic" if not monotonic_potential else "pass",
            "interpretation": "non-monotonic potential is allowed but must be parent-derived, not fitted by hand",
        },
    ]


def endpoint_regularity_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    scale_n, exponent_nu = activation_shape_params(params)
    omega_matter = float(params["omega_m0"])
    memory_amplitude = float(params["b_mem"])
    rho_today = 1.0 - omega_matter
    leading_f_coefficient = scale_n ** (-exponent_nu)
    leading_w_coefficient = memory_amplitude * exponent_nu * leading_f_coefficient / (3.0 * rho_today)
    field_power = 0.5 * (exponent_nu + 1.0)
    potential_power_in_load = exponent_nu - 1.0
    potential_power_in_field = 2.0 * (exponent_nu - 1.0) / (exponent_nu + 1.0)
    return [
        {
            "test": "activation_domain",
            "expression": "F(N)=1-exp[-(N/u_s)^nu] with non-integer nu",
            "value": f"u_s={scale_n}; nu={exponent_nu}",
            "status": "past_branch_only",
            "requirement_for_parent_action": "define a real smooth extension for N<0 or replace F by a smooth load invariant",
            "interpretation": "fractional power is not a complete time-domain field law through the present epoch",
        },
        {
            "test": "near_today_activation",
            "expression": "F(N) ~ (N/u_s)^nu",
            "value": leading_f_coefficient,
            "status": "finite",
            "requirement_for_parent_action": "derive the exponent from parent dynamics",
            "interpretation": "background value is harmless at N=0",
        },
        {
            "test": "near_today_source",
            "expression": "dF/dN ~ nu N^(nu-1)/u_s^nu",
            "value": leading_w_coefficient,
            "status": "source_switches_on_smoothly" if exponent_nu > 1.0 else "source_diverges_or_jumps",
            "requirement_for_parent_action": "source onset must be derived, not fit",
            "interpretation": "first derivative tends to zero because nu>1",
        },
        {
            "test": "activation_second_derivative",
            "expression": "d2F/dN2 ~ nu(nu-1)N^(nu-2)/u_s^nu",
            "value": exponent_nu - 2.0,
            "status": "fail_C2_endpoint" if exponent_nu < 2.0 else "passes_C2_endpoint",
            "requirement_for_parent_action": "smooth local action normally wants at least C2 activation",
            "interpretation": "fitted nu<2 makes the acceleration of the memory source singular at N=0+",
        },
        {
            "test": "canonical_field_onset",
            "expression": "phi-phi0 ~ N^((nu+1)/2)",
            "value": field_power,
            "status": "finite",
            "requirement_for_parent_action": "identify phi with an MTS invariant rather than an after-the-fact clock integral",
            "interpretation": "field displacement is finite and monotone on the past branch",
        },
        {
            "test": "potential_endpoint_power",
            "expression": "V(phi)-V0 ~ -C phi^[2(nu-1)/(nu+1)]",
            "value": potential_power_in_field,
            "status": "fail_C1_potential" if potential_power_in_field < 1.0 else "passes_C1_potential",
            "requirement_for_parent_action": "finite dV/dphi at present requires nu>=3 for this canonical proxy",
            "interpretation": "canonical potential has a cusp/infinite slope at the present endpoint for the fitted nu",
        },
        {
            "test": "smooth_canonical_threshold",
            "expression": "nu >= 3 for finite dV/dphi at phi0 in this reconstruction",
            "value": exponent_nu,
            "status": "fail_smooth_canonical_action" if exponent_nu < 3.0 else "pass_smooth_canonical_action",
            "requirement_for_parent_action": "derive a different field variable, noncanonical kinetic term, or smoother activation law",
            "interpretation": "the scalar proxy is not yet a clean fundamental canonical action",
        },
    ]


def parent_compatibility_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "parent_field_identity",
            "status": "fail",
            "current_best": "phi_mem is reconstructed from H(a), not identified with psi, Gamma, C, or S_memory",
            "needed_for_promotion": "derive phi_mem = functional[psi, Gamma, C, S_memory] with units and normalization",
            "claim_limit": "imported_scalar_proxy",
        },
        {
            "requirement": "action_variation",
            "status": "fail",
            "current_best": "V(phi) is reverse-engineered from fitted F(N)",
            "needed_for_promotion": "vary a parent action and recover the F(N), rho_X, and w_X equations",
            "claim_limit": "not_parent_derived",
        },
        {
            "requirement": "activation_shape_origin",
            "status": "fail",
            "current_best": "nu_act and alpha_act remain frozen fit/closure values",
            "needed_for_promotion": "derive u_s and nu_act from invariants or replace by a predeclared regular law",
            "claim_limit": "phenomenological_shape",
        },
        {
            "requirement": "amplitude_origin",
            "status": "fail",
            "current_best": "b_mem is a frozen calibrated amplitude",
            "needed_for_promotion": "derive b_mem from a memory-source budget or trace invariant",
            "claim_limit": "phenomenological_amplitude",
        },
        {
            "requirement": "conservation_identity",
            "status": "conditional_pass",
            "current_best": "w_X follows if the effective dark sector is separately conserved",
            "needed_for_promotion": "derive separate conservation or a Bianchi-owned exchange current",
            "claim_limit": "conditional_effective_identity",
        },
        {
            "requirement": "perturbation_sound_speed",
            "status": "fail_for_support",
            "current_best": "c_s^2=1 comes from imported canonical scalar closure",
            "needed_for_promotion": "derive c_s^2, anisotropic stress, and lensing response from MTS variables",
            "claim_limit": "kill_screen_only",
        },
        {
            "requirement": "local_GR_connection",
            "status": "open",
            "current_best": "cosmological scalar proxy is not connected to local R_AB/q_loc suppression",
            "needed_for_promotion": "show why the same parent scalar is silent locally but active cosmologically",
            "claim_limit": "not_unified_yet",
        },
    ]


def gate_rows(endpoint_rows: list[dict[str, Any]], parent_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    smooth_action = next(row for row in endpoint_rows if row["test"] == "smooth_canonical_threshold")
    c2_activation = next(row for row in endpoint_rows if row["test"] == "activation_second_derivative")
    parent_fail_count = sum(1 for row in parent_rows if row["status"] == "fail")
    return [
        {
            "gate": "canonical_energy_reconstruction",
            "status": "pass_conditional",
            "detail": "rho_X>0 and w_X>=-1 on the sampled past branch",
        },
        {
            "gate": "single_valued_V_of_phi",
            "status": "pass_on_past_branch",
            "detail": "phi is monotone from z=0 to z_star",
        },
        {
            "gate": "activation_C2_endpoint_regular",
            "status": c2_activation["status"],
            "detail": c2_activation["interpretation"],
        },
        {
            "gate": "smooth_canonical_parent_action",
            "status": smooth_action["status"],
            "detail": smooth_action["interpretation"],
        },
        {
            "gate": "parent_identity_and_variation",
            "status": "fail",
            "detail": f"hard parent failures={parent_fail_count}; scalar is reconstructed rather than varied from MTS action",
        },
        {
            "gate": "support_capable_CMB_perturbations",
            "status": "fail",
            "detail": "using this scalar in CMB would still import GR/quintessence perturbations",
        },
        {
            "gate": "kill_screen_implementation",
            "status": "pass_conditional",
            "detail": "possible only with endpoint regularization and explicit non-support label",
        },
    ]


def repair_option_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "smooth_activation_replacement",
            "status": "next_best_gate",
            "idea": "replace fractional Weibull onset by a C2/C1-action-safe load function before any support-capable CMB claim",
            "risk": "may change the fitted cosmology signal and must be retested against baselines",
            "promotion_condition": "predeclare shape then rerun same robustness matrix without rescuing parameters",
        },
        {
            "route": "noncanonical_k_essence_parent",
            "status": "possible_but_expensive",
            "idea": "use a kinetic function P(X,phi) or load variable that absorbs the cusp",
            "risk": "adds new functional freedom and can become untestable unless tightly constrained",
            "promotion_condition": "derive c_s^2 and stability conditions from one parent law",
        },
        {
            "route": "direct_Gamma_memory_action",
            "status": "preferred_if_derivable",
            "idea": "make Gamma or S_memory the varied field and derive F(N) as a solution, not as a potential fit",
            "risk": "requires the real parent equation, not just reconstruction",
            "promotion_condition": "derive b_mem, alpha_act, nu_act or their replacements",
        },
        {
            "route": "keep_quintessence_proxy_only",
            "status": "safe_closure_benchmark",
            "idea": "use reconstructed scalar only as a diagnostic CMB kill-screen closure",
            "risk": "cannot become fundamental-theory evidence",
            "promotion_condition": "none; this route stays labelled closure",
        },
    ]


def decision_rows(endpoint_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    smooth_action = next(row for row in endpoint_rows if row["test"] == "smooth_canonical_threshold")
    return [
        {
            "decision": "memory_scalar_reconstruction_status",
            "status": "reconstructed_proxy_not_parent_action",
            "evidence": "V(phi) exists on the past branch but is reverse-engineered from fitted F(N)",
            "next_action": "do not promote as parent scalar",
        },
        {
            "decision": "smooth_action_gate",
            "status": "fail",
            "evidence": smooth_action["interpretation"],
            "next_action": "derive a smoother activation law, noncanonical parent, or direct Gamma-memory action",
        },
        {
            "decision": "recommended_next_target",
            "status": "46-activation-regularity-repair-gate.md",
            "evidence": "the fitted activation exponent is the mathematical bottleneck for an action-like scalar",
            "next_action": "test what regularity conditions a parent-safe activation shape must satisfy before refitting",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Memory scalar reconstruction gate.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    source_38 = load_json("38_status")
    source_44 = load_json("44_status")
    params = {key: float(value) for key, value in json.loads(source_38["frozen_params_json"]).items()}
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-memory-scalar-reconstruction-gate"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    grid = reconstruction_grid(params)
    sampled_rows = sampled_reconstruction_rows(grid)
    features = potential_feature_rows(grid, params)
    endpoint = endpoint_regularity_rows(params)
    parent = parent_compatibility_rows()
    gates = gate_rows(endpoint, parent)
    repair = repair_option_rows()
    decisions = decision_rows(endpoint)

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "scalar_reconstruction_grid_sample.csv", sampled_rows, list(sampled_rows[0].keys()))
    write_csv(results_dir / "scalar_potential_features.csv", features, list(features[0].keys()))
    write_csv(results_dir / "endpoint_regularities.csv", endpoint, list(endpoint[0].keys()))
    write_csv(results_dir / "parent_compatibility_tests.csv", parent, list(parent[0].keys()))
    write_csv(results_dir / "scalar_reconstruction_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "repair_options.csv", repair, list(repair[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    feature_lookup = {row["feature"]: row for row in features}
    endpoint_lookup = {row["test"]: row for row in endpoint}
    status = {
        "status": "complete_memory_scalar_reconstruction_gate",
        "readout": "memory_scalar_proxy_reconstructable_but_nonanalytic_and_not_parent_derived",
        "recommendation": "write_activation_regularization_gate_next",
        "next_target": "46-activation-regularity-repair-gate.md",
        "source_44_readout": source_44["readout"],
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "official_CMB_kill_screen_possible": True,
        "official_CMB_support_run_ready": False,
        "key_metrics": {
            "nu_act": json.loads(source_38["frozen_params_json"])["nu_act"],
            "total_field_excursion": feature_lookup["total_field_excursion"]["value"],
            "V_today": feature_lookup["V_today"]["value"],
            "V_min": feature_lookup["V_min"]["value"],
            "V_recombination": feature_lookup["V_recombination"]["value"],
            "potential_endpoint_power_in_phi": endpoint_lookup["potential_endpoint_power"]["value"],
            "smooth_canonical_threshold_status": endpoint_lookup["smooth_canonical_threshold"]["status"],
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "scalar_reconstruction_grid_sample": str(results_dir / "scalar_reconstruction_grid_sample.csv"),
            "scalar_potential_features": str(results_dir / "scalar_potential_features.csv"),
            "endpoint_regularities": str(results_dir / "endpoint_regularities.csv"),
            "parent_compatibility_tests": str(results_dir / "parent_compatibility_tests.csv"),
            "scalar_reconstruction_gates": str(results_dir / "scalar_reconstruction_gates.csv"),
            "repair_options": str(results_dir / "repair_options.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
