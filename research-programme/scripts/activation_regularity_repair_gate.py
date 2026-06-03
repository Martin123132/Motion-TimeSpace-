#!/usr/bin/env python3
"""Define and score parent-safe activation regularity repairs before refitting."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import numpy as np


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(MAIN_SCRIPTS))

from cosmology_background_benchmark import C_KM_S  # noqa: E402
from cosmology_likelihood_smoke import activation_shape_params  # noqa: E402


SOURCE_PATHS = {
    "38_status": Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json"),
    "45_status": Path("runs/20260531-013422-memory-scalar-reconstruction-gate/status.json"),
    "45_endpoint_regularities": Path(
        "runs/20260531-013422-memory-scalar-reconstruction-gate/results/endpoint_regularities.csv"
    ),
    "45_scalar_gates": Path(
        "runs/20260531-013422-memory-scalar-reconstruction-gate/results/scalar_reconstruction_gates.csv"
    ),
}

N_EFF = 3.046
Z_STAR = 1091.5182931260854
SAMPLE_Z = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, Z_STAR]


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
    h = float(params.get("h0", 70.0)) / 100.0
    omega_gamma = 2.469e-5 / (h * h)
    return omega_gamma * (1.0 + 0.22710731766 * N_EFF)


def original_activation(load_n: np.ndarray, params: dict[str, float]) -> np.ndarray:
    u_s, nu_act = activation_shape_params(params)
    scaled = np.maximum(load_n, 0.0) / u_s
    return 1.0 - np.exp(-np.clip(scaled**nu_act, 0.0, 745.0))


def weibull_activation(load_n: np.ndarray, u_s: float, power: float) -> np.ndarray:
    scaled = np.maximum(load_n, 0.0) / u_s
    return 1.0 - np.exp(-np.clip(scaled**power, 0.0, 745.0))


def hill_activation(load_n: np.ndarray, n50: float, power: float) -> np.ndarray:
    scaled_power = np.maximum(load_n, 0.0) ** power
    denominator = scaled_power + n50**power
    return np.divide(scaled_power, denominator, out=np.zeros_like(load_n, dtype=float), where=denominator > 0.0)


def regularized_fractional_activation(load_n: np.ndarray, params: dict[str, float], target_power: float, n_reg: float) -> np.ndarray:
    u_s, nu_act = activation_shape_params(params)
    clipped = np.maximum(load_n, 0.0)
    extra_power = max(target_power - nu_act, 0.0)
    if extra_power == 0.0:
        modifier = np.ones_like(load_n, dtype=float)
    else:
        ratio_power = np.divide(clipped**extra_power, clipped**extra_power + n_reg**extra_power, out=np.zeros_like(load_n), where=(clipped**extra_power + n_reg**extra_power) > 0.0)
        modifier = ratio_power
    exponent = (clipped / u_s) ** nu_act * modifier
    return 1.0 - np.exp(-np.clip(exponent, 0.0, 745.0))


def e2_from_activation(z: np.ndarray, params: dict[str, float], activation: np.ndarray, include_radiation: bool) -> np.ndarray:
    omega_m = float(params["omega_m0"])
    e2 = omega_m * (1.0 + z) ** 3 + 1.0 - omega_m + float(params["b_mem"]) * activation
    if include_radiation:
        e2 = e2 + radiation_density(params) * (1.0 + z) ** 4
    return e2


def dimensionless_comoving_distance(z_max: float, params: dict[str, float], activation_fn: Callable[[np.ndarray], np.ndarray]) -> float:
    grid_count = 20000 if z_max > 100.0 else 5000
    # The change of variable x=ln(1+z) resolves both low-z and recombination.
    x_grid = np.linspace(0.0, math.log1p(z_max), grid_count)
    z_grid = np.expm1(x_grid)
    activation = activation_fn(x_grid)
    e2 = e2_from_activation(z_grid, params, activation, include_radiation=True)
    integrand = (1.0 + z_grid) / np.sqrt(e2)
    return float(np.trapezoid(integrand, x_grid))


def candidate_specs(params: dict[str, float]) -> list[dict[str, Any]]:
    original_u, original_nu = activation_shape_params(params)
    n50 = original_u * math.log(2.0) ** (1.0 / original_nu)
    n90 = original_u * math.log(10.0) ** (1.0 / original_nu)
    n_reg = 0.05
    return [
        {
            "candidate": "original_fractional_weibull",
            "family": "weibull_fractional",
            "endpoint_power": original_nu,
            "u_s": original_u,
            "n50": n50,
            "n90": n90,
            "new_continuous_shape_knob": False,
            "formula": "F=1-exp[-(N/u_s)^nu]",
            "activation_fn": lambda n, p=params: original_activation(n, p),
            "parent_status": "current_fitted_closure",
        },
        {
            "candidate": "weibull_p3_match_N50",
            "family": "weibull_integer_power",
            "endpoint_power": 3.0,
            "u_s": n50 / math.log(2.0) ** (1.0 / 3.0),
            "n50": n50,
            "n90": (n50 / math.log(2.0) ** (1.0 / 3.0)) * math.log(10.0) ** (1.0 / 3.0),
            "new_continuous_shape_knob": False,
            "formula": "F=1-exp[-(N/u_3)^3], u_3 fixed by original N50",
            "activation_fn": lambda n, n50=n50: weibull_activation(n, n50 / math.log(2.0) ** (1.0 / 3.0), 3.0),
            "parent_status": "minimal_C1_potential_repair_candidate",
        },
        {
            "candidate": "weibull_p4_match_N50",
            "family": "weibull_integer_power",
            "endpoint_power": 4.0,
            "u_s": n50 / math.log(2.0) ** (1.0 / 4.0),
            "n50": n50,
            "n90": (n50 / math.log(2.0) ** (1.0 / 4.0)) * math.log(10.0) ** (1.0 / 4.0),
            "new_continuous_shape_knob": False,
            "formula": "F=1-exp[-(N/u_4)^4], u_4 fixed by original N50",
            "activation_fn": lambda n, n50=n50: weibull_activation(n, n50 / math.log(2.0) ** (1.0 / 4.0), 4.0),
            "parent_status": "smoother_integer_repair_candidate",
        },
        {
            "candidate": "hill_p3_match_N50",
            "family": "hill_integer_power",
            "endpoint_power": 3.0,
            "u_s": "",
            "n50": n50,
            "n90": n50 * (9.0 ** (1.0 / 3.0)),
            "new_continuous_shape_knob": False,
            "formula": "F=N^3/(N^3+N50^3)",
            "activation_fn": lambda n, n50=n50: hill_activation(n, n50, 3.0),
            "parent_status": "minimal_rational_repair_candidate",
        },
        {
            "candidate": "hill_p4_match_N50",
            "family": "hill_integer_power",
            "endpoint_power": 4.0,
            "u_s": "",
            "n50": n50,
            "n90": n50 * (9.0 ** (1.0 / 4.0)),
            "new_continuous_shape_knob": False,
            "formula": "F=N^4/(N^4+N50^4)",
            "activation_fn": lambda n, n50=n50: hill_activation(n, n50, 4.0),
            "parent_status": "smoother_rational_repair_candidate",
        },
        {
            "candidate": "regularized_fractional_p3_Nreg_0p05",
            "family": "two_scale_regularized_fractional",
            "endpoint_power": 3.0,
            "u_s": original_u,
            "n50": "",
            "n90": "",
            "new_continuous_shape_knob": True,
            "formula": "F=1-exp[-(N/u)^nu * N^(3-nu)/(N^(3-nu)+N_reg^(3-nu))], N_reg=0.05",
            "activation_fn": lambda n, p=params, nr=n_reg: regularized_fractional_activation(n, p, 3.0, nr),
            "parent_status": "shape_preserving_but_new_scale_repair",
        },
    ]


def regularity_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "endpoint_value",
            "condition": "F(0)=0 and F(N>=0) bounded between 0 and 1",
            "reason": "today's memory load should not add a discontinuous dark-sector jump",
            "promotion_status_if_failed": "reject_as_parent_activation",
        },
        {
            "requirement": "source_onset",
            "condition": "F'(0)=0, equivalent to endpoint power p>1",
            "reason": "memory source should switch on smoothly rather than inject an impulse at the endpoint",
            "promotion_status_if_failed": "closure_only_or_reject",
        },
        {
            "requirement": "C2_endpoint",
            "condition": "endpoint power p>=3 for a clamped/invariant past-branch law",
            "reason": "field equations normally need finite acceleration/source curvature near the endpoint",
            "promotion_status_if_failed": "not_action_safe",
        },
        {
            "requirement": "canonical_scalar_C1_potential",
            "condition": "2(p-1)/(p+1)>=1, so p>=3",
            "reason": "finite dV/dphi at the present endpoint in the canonical proxy",
            "promotion_status_if_failed": "not_canonical_parent_scalar",
        },
        {
            "requirement": "real_time_domain",
            "condition": "law must be real and parent-defined through N=0 and into the future branch",
            "reason": "non-integer fractional powers of signed N are not a global field law",
            "promotion_status_if_failed": "past_branch_fit_only",
        },
        {
            "requirement": "no_rescue_knobs",
            "condition": "any repair must be fixed before data scoring, with no MTS-only nuisance freedom",
            "reason": "regularity repair cannot become a hidden cosmology refit",
            "promotion_status_if_failed": "phenomenology_only",
        },
        {
            "requirement": "same_test_retest",
            "condition": "LCDM, wCDM, CPL, original C0, and repaired C0 receive the same SN/BAO/CMB/growth/H(z) treatment",
            "reason": "a smoother law must earn survival empirically, not inherit the old fitted result",
            "promotion_status_if_failed": "no_evidence_language",
        },
    ]


def activation_domain_status(spec: dict[str, Any]) -> tuple[str, str]:
    family = spec["family"]
    power = float(spec["endpoint_power"])
    if family == "weibull_fractional":
        return "fail_without_load_invariant", "non-integer signed N is not real through N=0"
    if family == "two_scale_regularized_fractional":
        return "fail_without_parent_regularization", "uses fractional powers and an extra scale"
    if family == "weibull_integer_power" and int(power) % 2 == 1:
        return "warn_future_branch", "odd power is real but F becomes negative for N<0 unless parent clips/reroutes future branch"
    if family == "weibull_integer_power" and int(power) % 2 == 0:
        return "conditional_pass", "even power is real but time-symmetric around N=0 without a parent arrow"
    if family == "hill_integer_power" and int(power) % 2 == 1:
        return "warn_pole_or_future_branch", "odd rational law has a future-branch pole at N=-N50"
    if family == "hill_integer_power" and int(power) % 2 == 0:
        return "conditional_pass", "even rational law is real but time-symmetric around N=0"
    return "unknown", "domain not classified"


def candidate_activation_rows(specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in specs:
        power = float(spec["endpoint_power"])
        domain_status, domain_note = activation_domain_status(spec)
        c2_status = "pass" if power >= 3.0 else "fail"
        canonical_status = "pass" if power >= 3.0 else "fail"
        potential_power = 2.0 * (power - 1.0) / (power + 1.0)
        rows.append(
            {
                "candidate": spec["candidate"],
                "family": spec["family"],
                "formula": spec["formula"],
                "endpoint_power": power,
                "potential_endpoint_power_in_phi": potential_power,
                "u_s": spec["u_s"],
                "N50": spec["n50"],
                "N90": spec["n90"],
                "source_onset_status": "pass" if power > 1.0 else "fail",
                "C2_endpoint_status": c2_status,
                "canonical_C1_potential_status": canonical_status,
                "real_time_domain_status": domain_status,
                "domain_note": domain_note,
                "new_continuous_shape_knob": spec["new_continuous_shape_knob"],
                "parent_status": spec["parent_status"],
                "claim_limit": "repair_candidate_requires_retest" if spec["candidate"] != "original_fractional_weibull" else "current_closure_fails_regular_action_gate",
            }
        )
    return rows


def background_deviation_rows(specs: list[dict[str, Any]], params: dict[str, float]) -> list[dict[str, Any]]:
    z_late = np.linspace(0.0, 2.0, 4000)
    n_late = np.log1p(z_late)
    z_star_grid = np.asarray([Z_STAR], dtype=float)
    n_star_grid = np.log1p(z_star_grid)
    original_fn = specs[0]["activation_fn"]
    original_late = original_fn(n_late)
    original_e2_late = e2_from_activation(z_late, params, original_late, include_radiation=False)
    original_dm_z2 = dimensionless_comoving_distance(2.0, params, original_fn)
    original_dm_zstar = dimensionless_comoving_distance(Z_STAR, params, original_fn)
    rows: list[dict[str, Any]] = []
    for spec in specs:
        activation_fn = spec["activation_fn"]
        activation_late = activation_fn(n_late)
        candidate_e2_late = e2_from_activation(z_late, params, activation_late, include_radiation=False)
        max_delta_f = float(np.max(np.abs(activation_late - original_late)))
        max_delta_e2_frac = float(np.max(np.abs(candidate_e2_late / original_e2_late - 1.0)))
        dm_z2 = dimensionless_comoving_distance(2.0, params, activation_fn)
        dm_zstar = dimensionless_comoving_distance(Z_STAR, params, activation_fn)
        row = {
            "candidate": spec["candidate"],
            "max_abs_delta_F_z0_to_2_vs_original": max_delta_f,
            "max_abs_frac_delta_E2_z0_to_2_vs_original": max_delta_e2_frac,
            "frac_delta_DM_z2_vs_original": dm_z2 / original_dm_z2 - 1.0,
            "frac_delta_DM_zstar_vs_original": dm_zstar / original_dm_zstar - 1.0,
            "F_zstar": float(activation_fn(n_star_grid)[0]),
            "requires_full_empirical_retest": spec["candidate"] != "original_fractional_weibull",
        }
        for z in SAMPLE_Z:
            n_value = np.asarray([math.log1p(z)], dtype=float)
            row[f"F_z_{z:g}"] = float(activation_fn(n_value)[0])
            row[f"delta_F_z_{z:g}_vs_original"] = float(activation_fn(n_value)[0] - original_fn(n_value)[0])
        rows.append(row)
    return rows


def retest_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "stage": "predeclare_candidate",
            "action": "choose at most one C2-safe activation law and freeze its formula before scoring",
            "required_output": "candidate_activation_lock.csv with formula, fixed scales, and no hidden shape knobs",
            "claim_limit": "no evidence until retested",
        },
        {
            "stage": "late_background_smoke",
            "action": "evaluate SN, BAO, and H(z) with the repaired law against LCDM/wCDM/CPL and original C0",
            "required_output": "same columns and AIC/BIC/delta-chi2 as earlier robustness passes",
            "claim_limit": "guardrail only",
        },
        {
            "stage": "compressed_CMB_and_growth",
            "action": "repeat fixed-row compressed CMB and growth/H(z) checks without moving parameters",
            "required_output": "prior-edge and no-rescue tables",
            "claim_limit": "closure-candidate survival only",
        },
        {
            "stage": "official_CMB_setup",
            "action": "only after perturbation closure and baseline reproduction, run official spectra/lensing",
            "required_output": "setup manifest, log.txt, status.json, DONE.txt",
            "claim_limit": "kill-screen unless parent perturbations are derived",
        },
        {
            "stage": "parent_derivation",
            "action": "derive the activation law from Gamma/S_memory/psi/C variables, including b_mem and transition scale",
            "required_output": "parent equation variation or theorem, not a fit",
            "claim_limit": "required for theory promotion",
        },
    ]


def gate_rows(candidate_rows: list[dict[str, Any]], deviation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    original = next(row for row in candidate_rows if row["candidate"] == "original_fractional_weibull")
    viable_no_knob_repairs = [
        row
        for row in candidate_rows
        if row["candidate"] != "original_fractional_weibull"
        and row["C2_endpoint_status"] == "pass"
        and row["canonical_C1_potential_status"] == "pass"
        and str(row["new_continuous_shape_knob"]) == "False"
    ]
    min_dm_shift = min(
        abs(float(row["frac_delta_DM_zstar_vs_original"]))
        for row in deviation_rows
        if row["candidate"] != "original_fractional_weibull"
    )
    return [
        {
            "gate": "original_fractional_weibull_parent_safe",
            "status": "fail",
            "detail": f"C2={original['C2_endpoint_status']}; canonical_C1={original['canonical_C1_potential_status']}; domain={original['real_time_domain_status']}",
        },
        {
            "gate": "C2_C1_no_knob_repair_exists",
            "status": "pass",
            "detail": "; ".join(row["candidate"] for row in viable_no_knob_repairs),
        },
        {
            "gate": "repair_preserves_background_without_retest",
            "status": "fail",
            "detail": f"best_abs_frac_delta_DM_zstar_vs_original_among_repairs={min_dm_shift}; any shape replacement must be empirically retested",
        },
        {
            "gate": "support_claim_allowed_after_repair_definition",
            "status": "fail",
            "detail": "regularity repair alone is not evidence and may move the cosmology signal",
        },
        {
            "gate": "official_CMB_support_ready",
            "status": "fail",
            "detail": "parent perturbation/lensing closure remains missing even if activation is smoothed",
        },
        {
            "gate": "next_background_smoke_authorized",
            "status": "pass",
            "detail": "a short no-rescue background smoke is the correct next empirical guardrail",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "activation_regularization_status",
            "status": "original_fails_parent_safe_regular_action_gate",
            "evidence": "nu_act=1.7500073382761008 fails C2 endpoint and canonical C1 potential thresholds",
            "next_action": "do not use original fractional onset as fundamental scalar action",
        },
        {
            "decision": "repair_status",
            "status": "C2_safe_candidates_exist_but_require_same_test_retest",
            "evidence": "integer-power and rational candidates can satisfy p>=3 but change the background shape",
            "next_action": "run a no-rescue background smoke before any stronger interpretation",
        },
        {
            "decision": "recommended_next_target",
            "status": "47-C2-activation-background-smoke.md",
            "evidence": "regularity-safe candidates must be tested against the same late-background/CMB-distance guardrails",
            "next_action": "evaluate selected C2 candidates versus original C0 and baselines without parameter rescue",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Activation regularity repair gate.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    source_38 = load_json("38_status")
    source_45 = load_json("45_status")
    params = {key: float(value) for key, value in json.loads(source_38["frozen_params_json"]).items()}
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-activation-regularity-repair-gate"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    specs = candidate_specs(params)
    requirements = regularity_requirement_rows()
    candidates = candidate_activation_rows(specs)
    deviations = background_deviation_rows(specs, params)
    retest = retest_manifest_rows()
    gates = gate_rows(candidates, deviations)
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "activation_regularity_requirements.csv", requirements, list(requirements[0].keys()))
    write_csv(results_dir / "candidate_activation_laws.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "candidate_background_deviation.csv", deviations, list(deviations[0].keys()))
    write_csv(results_dir / "same_test_retest_manifest.csv", retest, list(retest[0].keys()))
    write_csv(results_dir / "activation_repair_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    repair_rows = [row for row in candidates if row["candidate"] != "original_fractional_weibull"]
    no_knob_c2_count = sum(
        1
        for row in repair_rows
        if row["C2_endpoint_status"] == "pass"
        and row["canonical_C1_potential_status"] == "pass"
        and str(row["new_continuous_shape_knob"]) == "False"
    )
    original_deviation = next(row for row in deviations if row["candidate"] == "original_fractional_weibull")
    best_dm_repair = min(
        deviations,
        key=lambda row: abs(float(row["frac_delta_DM_zstar_vs_original"])) if row["candidate"] != "original_fractional_weibull" else float("inf"),
    )
    status = {
        "status": "complete_activation_regularity_repair_gate",
        "readout": "activation_regularization_gate_requires_C2_parent_safe_retest_no_promotion",
        "recommendation": "run_C2_activation_background_smoke_next",
        "next_target": "47-C2-activation-background-smoke.md",
        "source_45_readout": source_45["readout"],
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "no_knob_C2_repair_candidates": no_knob_c2_count,
        "original_self_deviation_check": original_deviation["frac_delta_DM_zstar_vs_original"],
        "best_abs_frac_delta_DM_zstar_repair_candidate": best_dm_repair["candidate"],
        "best_abs_frac_delta_DM_zstar_repair_value": best_dm_repair["frac_delta_DM_zstar_vs_original"],
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "activation_regularity_requirements": str(results_dir / "activation_regularity_requirements.csv"),
            "candidate_activation_laws": str(results_dir / "candidate_activation_laws.csv"),
            "candidate_background_deviation": str(results_dir / "candidate_background_deviation.csv"),
            "same_test_retest_manifest": str(results_dir / "same_test_retest_manifest.csv"),
            "activation_repair_gates": str(results_dir / "activation_repair_gates.csv"),
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
