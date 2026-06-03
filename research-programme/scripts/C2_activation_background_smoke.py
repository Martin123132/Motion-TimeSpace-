#!/usr/bin/env python3
"""No-rescue background smoke for C2-safe activation repairs."""

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
from scipy import linalg


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
POST_SCRIPTS = POST_CHECKPOINT / "scripts"
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
REPO_ROOT = MAIN_WORKBENCH.parent
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(POST_SCRIPTS))
sys.path.insert(0, str(MAIN_SCRIPTS))

from activation_regularity_repair_gate import candidate_specs  # noqa: E402
from cosmology_likelihood_smoke import (  # noqa: E402
    bao_model_vector,
    chi2_bao,
    chi2_sn,
    e2_array,
    load_bao,
    load_json,
    load_pantheon,
    select_dataset,
)


SOURCE_PATHS = {
    "38_status": Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json"),
    "46_status": Path("runs/20260531-013929-activation-regularity-repair-gate/status.json"),
    "46_candidate_laws": Path("runs/20260531-013929-activation-regularity-repair-gate/results/candidate_activation_laws.csv"),
    "46_deviation": Path("runs/20260531-013929-activation-regularity-repair-gate/results/candidate_background_deviation.csv"),
}

BACKGROUND_RESULTS = MAIN_WORKBENCH / "runs/20260528-032713-cosmology-smoke-fit/results/smoke_fit_results.csv"
CONFIG_PATH = MAIN_WORKBENCH / "runs/20260528-032702-minimal-memory-predeclared-validation/configs/no_sh0es_dr1_config.json"
HZ_TABLE = MAIN_WORKBENCH / "data/cosmology/cosmic_chronometers/covariance_branch/Hz_CC_Moresco15_BC03.csv"
HZ_MANIFEST = MAIN_WORKBENCH / "data/cosmology/cosmic_chronometers/covariance_branch/row_lock_manifest.json"
LOCKED_MODEL = "M6_min_predeclared_fixed_shape"
ORIGINAL_REPAIR_LABEL = "original_fractional_weibull"
REPAIR_PREFIX = "C2_"


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    paths = dict(SOURCE_PATHS)
    paths.update(
        {
            "background_results": BACKGROUND_RESULTS,
            "config": CONFIG_PATH,
            "Hz_table": HZ_TABLE,
            "Hz_manifest": HZ_MANIFEST,
        }
    )
    rows: list[dict[str, Any]] = []
    for key, path in paths.items():
        absolute = POST_CHECKPOINT / path if not path.is_absolute() else path
        rows.append(
            {
                "source_key": key,
                "path": str(absolute),
                "exists": absolute.exists(),
            }
        )
    missing = [row["path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def source_fit_rows() -> list[dict[str, Any]]:
    rows = read_csv(BACKGROUND_RESULTS)
    keep = {
        "M0": ("LCDM_fixed_fit", "M0", 3),
        "M2_wCDM": ("wCDM_fixed_fit", "M2_wCDM", 4),
        "M2_CPL": ("CPL_fixed_fit", "M2_CPL", 5),
        LOCKED_MODEL: ("locked_C0_no_SH0ES_fit", "M6", 4),
    }
    out: list[dict[str, Any]] = []
    for row in rows:
        if row["branch"] != "no_sh0es" or row["mode"] != "fit" or row["success"] != "True" or row["model"] not in keep:
            continue
        label, physics_model, k_params = keep[row["model"]]
        out.append(
            {
                "label": label,
                "kind": "baseline_or_locked_reference",
                "physics_model": physics_model,
                "params": json.loads(row["params_json"]),
                "activation_candidate": "",
                "parameter_origin": "no_SH0ES_background_fit_reference",
                "n_params_reference": k_params,
                "claim_limit": "reference_only",
            }
        )
    return out


def candidate_law_lookup() -> dict[str, dict[str, str]]:
    return {row["candidate"]: row for row in read_csv(absolute_source("46_candidate_laws"))}


def repair_specs(source_38: dict[str, Any]) -> list[dict[str, Any]]:
    params = {key: float(value) for key, value in json.loads(source_38["frozen_params_json"]).items()}
    law_rows = candidate_law_lookup()
    specs: list[dict[str, Any]] = []
    for spec in candidate_specs(params):
        law_row = law_rows[spec["candidate"]]
        if spec["candidate"] != ORIGINAL_REPAIR_LABEL and str(law_row["new_continuous_shape_knob"]) != "False":
            continue
        if spec["candidate"] != ORIGINAL_REPAIR_LABEL and (
            law_row["C2_endpoint_status"] != "pass" or law_row["canonical_C1_potential_status"] != "pass"
        ):
            continue
        label = (
            "C0_frozen_original_fractional_weibull"
            if spec["candidate"] == ORIGINAL_REPAIR_LABEL
            else REPAIR_PREFIX + spec["candidate"]
        )
        specs.append(
            {
                "label": label,
                "kind": "frozen_activation_candidate",
                "physics_model": "custom_M6",
                "params": dict(params),
                "activation_candidate": spec["candidate"],
                "activation_fn": spec["activation_fn"],
                "parameter_origin": "checkpoint_38_frozen_no_rescue",
                "n_params_reference": 0,
                "claim_limit": "regularity_retest_guardrail_only",
            }
        )
    return specs


def background_grid_custom(params: dict[str, float], activation_fn: Callable[[np.ndarray], np.ndarray], z_max: float, steps: int) -> dict[str, np.ndarray]:
    z_grid = np.linspace(0.0, float(z_max), int(steps))
    n_grid = np.log1p(z_grid)
    activation = activation_fn(n_grid)
    omega_m = float(params["omega_m0"])
    e2 = omega_m * (1.0 + z_grid) ** 3 + 1.0 - omega_m + float(params["b_mem"]) * activation
    if np.any(~np.isfinite(e2)) or np.any(e2 <= 0.0):
        raise ValueError("custom activation produced non-positive E2")
    e_values = np.sqrt(e2)
    integral = np.zeros_like(z_grid)
    if len(z_grid) > 1:
        integral[1:] = np.cumsum(0.5 * np.diff(z_grid) * (1.0 / e_values[:-1] + 1.0 / e_values[1:]))
    d_m = (299792.458 / float(params["h0"])) * integral
    return {"z": z_grid, "e": e_values, "d_m": d_m}


def distance_modulus_custom(params: dict[str, float], activation_fn: Callable[[np.ndarray], np.ndarray], z_cosmo: np.ndarray, z_hel: np.ndarray, steps: int) -> np.ndarray:
    z_max = float(np.max(z_cosmo) * 1.01 + 0.01)
    background = background_grid_custom(params, activation_fn, z_max, steps)
    d_m = np.interp(z_cosmo, background["z"], background["d_m"])
    d_l = (1.0 + z_hel) * d_m
    if np.any(d_l <= 0.0):
        raise ValueError("custom activation produced non-positive luminosity distance")
    return 5.0 * np.log10(d_l) + 25.0


def chi2_sn_custom(params: dict[str, float], activation_fn: Callable[[np.ndarray], np.ndarray], sn: dict[str, Any], steps: int) -> tuple[float, float]:
    mu_model = distance_modulus_custom(params, activation_fn, sn["z_cosmo"], sn["z_hel"], steps)
    residual = sn["mu_obs"] - mu_model
    c_inv_residual = linalg.cho_solve(sn["cho"], residual, check_finite=False)
    best_offset = float(sn["ones"] @ c_inv_residual / sn["ones_cinv_ones"])
    adjusted = residual - best_offset * sn["ones"]
    chi2 = float(adjusted @ linalg.cho_solve(sn["cho"], adjusted, check_finite=False))
    return chi2, best_offset


def bao_model_vector_custom(params: dict[str, float], activation_fn: Callable[[np.ndarray], np.ndarray], bao: dict[str, Any], steps: int) -> np.ndarray:
    z = bao["z"]
    z_max = float(np.max(z) * 1.01 + 0.01)
    background = background_grid_custom(params, activation_fn, z_max, steps)
    d_m = np.interp(z, background["z"], background["d_m"])
    e_values = np.interp(z, background["z"], background["e"])
    d_h = 299792.458 / (float(params["h0"]) * e_values)
    d_v = np.cbrt(z * d_m * d_m * d_h)
    rd = float(params["rd"])
    predicted = []
    for index, quantity in enumerate(bao["quantity"]):
        if quantity == "DM_over_rs":
            predicted.append(d_m[index] / rd)
        elif quantity == "DH_over_rs":
            predicted.append(d_h[index] / rd)
        elif quantity == "DV_over_rs":
            predicted.append(d_v[index] / rd)
        else:
            raise ValueError(f"unsupported BAO quantity: {quantity}")
    return np.asarray(predicted, dtype=float)


def chi2_bao_custom(params: dict[str, float], activation_fn: Callable[[np.ndarray], np.ndarray], bao: dict[str, Any], steps: int) -> tuple[float, float, float]:
    predicted = bao_model_vector_custom(params, activation_fn, bao, steps)
    residual = bao["obs"] - predicted
    chi2 = float(residual @ linalg.cho_solve(bao["cho"], residual, check_finite=False))
    fractional = bao["obs"] / predicted - 1.0
    return chi2, float(np.sqrt(np.mean(fractional**2))), float(np.max(np.abs(fractional)))


def load_hz_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(HZ_TABLE):
        rows.append(
            {
                "index": int(row["branch_index"]),
                "z": float(row["z"]),
                "H": float(row["H"]),
                "sigma": float(row["sigma"]),
                "reference": row.get("reference", ""),
            }
        )
    return rows


def read_hz_covariance() -> np.ndarray:
    manifest = json.loads(HZ_MANIFEST.read_text(encoding="utf-8"))
    relative = Path(manifest["matrix_paths"]["suggested"])
    path = relative if relative.is_absolute() else MAIN_WORKBENCH / relative
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        matrix = np.asarray([[float(value) for value in row[1:]] for row in reader], dtype=float)
    if matrix.shape[0] + 1 != len(header):
        raise ValueError("H(z) covariance header mismatch")
    return matrix


def hz_prediction(spec: dict[str, Any], z: np.ndarray) -> np.ndarray:
    params = {key: float(value) for key, value in spec["params"].items()}
    h0 = float(params["h0"])
    if spec["physics_model"] == "custom_M6":
        activation = spec["activation_fn"](np.log1p(z))
        omega_m = float(params["omega_m0"])
        e2 = omega_m * (1.0 + z) ** 3 + 1.0 - omega_m + float(params["b_mem"]) * activation
    else:
        e2 = e2_array(spec["physics_model"], z, params)
    return h0 * np.sqrt(e2)


def hz_chi2(spec: dict[str, Any], hz_rows: list[dict[str, Any]], covariance: np.ndarray) -> tuple[float, float]:
    z = np.asarray([row["z"] for row in hz_rows], dtype=float)
    observed = np.asarray([row["H"] for row in hz_rows], dtype=float)
    predicted = hz_prediction(spec, z)
    residual = predicted - observed
    lower = np.linalg.cholesky(covariance)
    y = np.linalg.solve(lower, residual)
    weighted = np.linalg.solve(lower.T, y)
    chi2 = float(residual @ weighted)
    diag = np.sqrt(np.diag(covariance))
    rms_pull = float(np.sqrt(np.mean((residual / diag) ** 2)))
    return chi2, rms_pull


def evaluate_spec(spec: dict[str, Any], sn: dict[str, Any], bao: dict[str, Any], hz_rows: list[dict[str, Any]], hz_cov: np.ndarray, steps: int) -> dict[str, Any]:
    params = {key: float(value) for key, value in spec["params"].items()}
    if spec["physics_model"] == "custom_M6":
        sn_chi2, sn_offset = chi2_sn_custom(params, spec["activation_fn"], sn, steps)
        bao_chi2, bao_rms, bao_max = chi2_bao_custom(params, spec["activation_fn"], bao, steps)
    else:
        sn_chi2, sn_offset = chi2_sn(spec["physics_model"], params, sn, steps)
        bao_chi2 = chi2_bao(spec["physics_model"], params, bao, steps)
        predicted_bao = bao_model_vector(spec["physics_model"], params, bao, steps)
        bao_fractional = bao["obs"] / predicted_bao - 1.0
        bao_rms = float(np.sqrt(np.mean(bao_fractional**2)))
        bao_max = float(np.max(np.abs(bao_fractional)))
    hz_value, hz_rms_pull = hz_chi2(spec, hz_rows, hz_cov)
    chi2_late = sn_chi2 + bao_chi2
    chi2_late_hz = chi2_late + hz_value
    n_data_late_hz = int(sn["n"] + bao["n"] + len(hz_rows))
    k_ref = int(spec["n_params_reference"])
    return {
        "model": spec["label"],
        "kind": spec["kind"],
        "physics_model": spec["physics_model"],
        "activation_candidate": spec["activation_candidate"],
        "parameter_origin": spec["parameter_origin"],
        "chi2_sn": sn_chi2,
        "chi2_bao": bao_chi2,
        "chi2_late_SN_BAO": chi2_late,
        "chi2_Hz_suggested": hz_value,
        "chi2_late_plus_Hz": chi2_late_hz,
        "AIC_late_plus_Hz_reference": chi2_late_hz + 2.0 * k_ref,
        "BIC_late_plus_Hz_reference": chi2_late_hz + k_ref * math.log(n_data_late_hz),
        "sn_offset": sn_offset,
        "bao_fractional_rms": bao_rms,
        "bao_fractional_max_abs": bao_max,
        "Hz_diag_rms_pull": hz_rms_pull,
        "n_params_reference": k_ref,
        "n_data_late_plus_Hz": n_data_late_hz,
        "claim_limit": spec["claim_limit"],
        "params_json": json.dumps(params, sort_keys=True),
    }


def add_deltas(rows: list[dict[str, Any]]) -> None:
    original = next(row for row in rows if row["model"] == "C0_frozen_original_fractional_weibull")
    baselines = [row for row in rows if row["model"] in {"LCDM_fixed_fit", "wCDM_fixed_fit", "CPL_fixed_fit"}]
    best_baseline_late = min(baselines, key=lambda row: float(row["chi2_late_SN_BAO"]))
    best_baseline_late_hz = min(baselines, key=lambda row: float(row["chi2_late_plus_Hz"]))
    for row in rows:
        row["delta_late_SN_BAO_vs_original_frozen"] = float(row["chi2_late_SN_BAO"]) - float(original["chi2_late_SN_BAO"])
        row["delta_late_plus_Hz_vs_original_frozen"] = float(row["chi2_late_plus_Hz"]) - float(original["chi2_late_plus_Hz"])
        row["delta_late_SN_BAO_vs_best_baseline"] = float(row["chi2_late_SN_BAO"]) - float(best_baseline_late["chi2_late_SN_BAO"])
        row["delta_late_plus_Hz_vs_best_baseline"] = float(row["chi2_late_plus_Hz"]) - float(best_baseline_late_hz["chi2_late_plus_Hz"])
        row["best_baseline_late_SN_BAO"] = best_baseline_late["model"]
        row["best_baseline_late_plus_Hz"] = best_baseline_late_hz["model"]
        row["model_selection_valid"] = False if row["kind"] == "frozen_activation_candidate" else "reference_only"


def residual_summary_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidate_rows = [row for row in scores if str(row["model"]).startswith(REPAIR_PREFIX)]
    best_by_late = min(candidate_rows, key=lambda row: float(row["delta_late_SN_BAO_vs_original_frozen"]))
    best_by_late_hz = min(candidate_rows, key=lambda row: float(row["delta_late_plus_Hz_vs_original_frozen"]))
    best_by_baseline_gap = min(candidate_rows, key=lambda row: float(row["delta_late_plus_Hz_vs_best_baseline"]))
    return [
        {
            "summary": "best_repair_vs_original_SN_BAO",
            "model": best_by_late["model"],
            "delta": best_by_late["delta_late_SN_BAO_vs_original_frozen"],
            "interpretation": "lowest SN+BAO penalty versus original frozen fractional branch",
        },
        {
            "summary": "best_repair_vs_original_SN_BAO_Hz",
            "model": best_by_late_hz["model"],
            "delta": best_by_late_hz["delta_late_plus_Hz_vs_original_frozen"],
            "interpretation": "lowest SN+BAO+H(z) penalty versus original frozen fractional branch",
        },
        {
            "summary": "best_repair_vs_best_baseline_SN_BAO_Hz",
            "model": best_by_baseline_gap["model"],
            "delta": best_by_baseline_gap["delta_late_plus_Hz_vs_best_baseline"],
            "interpretation": "closest repair to the best standard baseline under this smoke score",
        },
    ]


def gate_rows(source_46: dict[str, Any], scores: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best = next(row for row in summaries if row["summary"] == "best_repair_vs_original_SN_BAO_Hz")
    best_delta = float(best["delta"])
    repair_count = sum(1 for row in scores if str(row["model"]).startswith(REPAIR_PREFIX))
    return [
        {
            "gate": "source_46_complete",
            "status": "pass" if source_46.get("readout") == "activation_regularization_gate_requires_C2_parent_safe_retest_no_promotion" else "fail",
            "detail": str(source_46.get("readout")),
        },
        {
            "gate": "C2_no_knob_repairs_evaluated",
            "status": "pass" if repair_count >= 4 else "fail",
            "detail": f"repair_count={repair_count}",
        },
        {
            "gate": "best_repair_not_worse_than_original_by_3",
            "status": "pass" if best_delta <= 3.0 else "fail",
            "detail": f"best_model={best['model']}; delta_late_plus_Hz_vs_original={best_delta}; threshold=3",
        },
        {
            "gate": "all_repairs_not_promoted",
            "status": "pass",
            "detail": "regularity-safe repairs are smoke-tested closure candidates only",
        },
        {
            "gate": "model_selection_claim_allowed",
            "status": "fail",
            "detail": "frozen repaired rows are not refit and activation law is not parent-derived",
        },
        {
            "gate": "next_growth_CMB_retest_authorized",
            "status": "pass" if best_delta <= 3.0 else "fail",
            "detail": "if the best C2 repair survives late background, repeat compressed CMB/growth/H(z) fixed-row checks",
        },
    ]


def decision_rows(summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best = next(row for row in summaries if row["summary"] == "best_repair_vs_original_SN_BAO_Hz")
    best_delta = float(best["delta"])
    retained = best_delta <= 3.0
    return [
        {
            "decision": "C2_activation_late_background_status",
            "status": "retained_for_next_guardrail" if retained else "demote_C2_scalar_action_route",
            "evidence": f"best_model={best['model']}; delta_late_plus_Hz_vs_original={best_delta}",
            "next_action": "repeat compressed CMB/growth fixed-row guardrail" if retained else "return to parent activation law derivation before more data",
        },
        {
            "decision": "support_claim_status",
            "status": "forbidden",
            "evidence": "regularized activation is not parent-derived and this is a smoke retest",
            "next_action": "keep closure language only",
        },
        {
            "decision": "recommended_next_target",
            "status": "48-C2-activation-growth-CMB-retest.md" if retained else "48-parent-activation-derivation-repair.md",
            "evidence": "late-background smoke decides whether the C2 repair is worth carrying into CMB/growth",
            "next_action": "run fixed-row compressed CMB/growth/H(z) retest for the best retained C2 candidate" if retained else "derive a new parent-safe activation",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="C2 activation no-rescue background smoke.")
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--integration-steps", type=int, default=2048)
    args = parser.parse_args()

    source_register = source_register_rows()
    source_38 = load_json(absolute_source("38_status"))
    source_46 = load_json(absolute_source("46_status"))
    config = load_json(CONFIG_PATH)
    sn = load_pantheon(REPO_ROOT, select_dataset(config, "Pantheon"), branch="no_sh0es")
    bao = load_bao(REPO_ROOT, select_dataset(config, "BAO"))
    hz_rows = load_hz_rows()
    hz_cov = read_hz_covariance()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-C2-activation-background-smoke"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    specs = source_fit_rows() + repair_specs(source_38)
    scores = [evaluate_spec(spec, sn, bao, hz_rows, hz_cov, args.integration_steps) for spec in specs]
    add_deltas(scores)
    summaries = residual_summary_rows(scores)
    gates = gate_rows(source_46, scores, summaries)
    decisions = decision_rows(summaries)
    best = next(row for row in summaries if row["summary"] == "best_repair_vs_original_SN_BAO_Hz")
    retained = next(row for row in decisions if row["decision"] == "C2_activation_late_background_status")["status"] == "retained_for_next_guardrail"

    write_csv(results_dir / "C2_activation_background_scores.csv", scores, list(scores[0].keys()))
    write_csv(results_dir / "C2_activation_background_summary.csv", summaries, list(summaries[0].keys()))
    write_csv(results_dir / "C2_activation_background_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))
    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))

    readout = (
        "C2_activation_background_smoke_retains_best_repair_not_evidence"
        if retained
        else "C2_activation_background_smoke_demotes_regular_scalar_route"
    )
    status = {
        "status": "complete_C2_activation_background_smoke",
        "readout": readout,
        "recommendation": "run_C2_activation_growth_CMB_retest_next" if retained else "return_to_parent_activation_derivation",
        "next_target": "48-C2-activation-growth-CMB-retest.md" if retained else "48-parent-activation-derivation-repair.md",
        "best_repair_model": best["model"],
        "best_repair_delta_late_plus_Hz_vs_original": best["delta"],
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "model_selection_claim_allowed": False,
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "C2_activation_background_scores": str(results_dir / "C2_activation_background_scores.csv"),
            "C2_activation_background_summary": str(results_dir / "C2_activation_background_summary.csv"),
            "C2_activation_background_gates": str(results_dir / "C2_activation_background_gates.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
