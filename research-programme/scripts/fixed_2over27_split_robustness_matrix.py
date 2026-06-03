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
from scipy import linalg


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import cosmo_SN_BAO_closure_runner as closure_runner  # noqa: E402
import fixed_2over27_fullcov_noSH0ES_release_matrix as release_matrix  # noqa: E402


RUN_SLUG = "fixed-2over27-split-robustness-matrix"
STATUS_SURVIVES = "fixed_2over27_split_robustness_survives_first_pass_diagnostic_only"
STATUS_MIXED = "fixed_2over27_split_robustness_mixed_first_pass"
STATUS_FAILS = "fixed_2over27_split_robustness_fails_first_pass"
CLAIM_CEILING = "late_time_background_split_diagnostic_only_no_parent_CMB_or_local_GR_promotion"
LEAD_BRANCH = release_matrix.LEAD_BRANCH
CONTROL_BRANCH = "MTS_Bmem_zero"
BASELINES = ["LCDM", "wCDM", "CPL"]
MODEL_ORDER = ["LCDM", "wCDM", "CPL", LEAD_BRANCH, CONTROL_BRANCH]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def pass_fail(value: bool) -> str:
    return "pass" if value else "fail"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    sources = [
        (script_path, "this split robustness runner"),
        (ROOT / "318-fixed-2over27-fullcov-noSH0ES-release-matrix.md", "parent release-matrix checkpoint"),
        (ROOT / "316-FLRW-memory-projection-amplitude-contract.md", "FLRW memory-shape derivation checkpoint"),
        (ROOT / "317-kappa-mem-Ward-scale-lock-attempt.md", "amplitude-normalization no-go checkpoint"),
        (SCRIPTS_ROOT / "fixed_2over27_fullcov_noSH0ES_release_matrix.py", "strict fixed-branch scorer"),
        (SCRIPTS_ROOT / "cosmo_SN_BAO_closure_runner.py", "shared SN+BAO likelihood engine"),
        (release_matrix.SN_PATH, "Pantheon+SH0ES SN source"),
        (release_matrix.SN_COV, "Pantheon+SH0ES full covariance"),
    ]
    for release_label, paths in release_matrix.BAO_RELEASES.items():
        sources.append((paths["mean"], f"{release_label} BAO mean"))
        sources.append((paths["cov"], f"{release_label} BAO covariance"))
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": yes_no(path.exists()),
            "bytes": path.stat().st_size if path.exists() else 0,
        }
        for path, role in sources
    ]


def subset_sn(sn: dict[str, Any], mask: np.ndarray, label: str) -> dict[str, Any]:
    indices = np.flatnonzero(np.asarray(mask, dtype=bool))
    if len(indices) < 20:
        raise ValueError(f"SN split {label} leaves too few rows: {len(indices)}")
    output = dict(sn)
    for key in ["z", "mu", "sigma", "row_indices"]:
        output[key] = np.asarray(sn[key])[indices]
    if sn.get("covariance_mode") == "full":
        covariance = np.asarray(sn["covariance"], dtype=float)[np.ix_(indices, indices)]
        output["covariance"] = covariance
        output["inv_covariance"] = linalg.inv(covariance)
    output["split_label"] = label
    return output


def subset_bao(bao: dict[str, Any], indices: list[int], label: str) -> dict[str, Any]:
    if len(indices) < 2:
        raise ValueError(f"BAO split {label} leaves too few rows: {len(indices)}")
    covariance = np.asarray(bao["covariance"], dtype=float)[np.ix_(indices, indices)]
    output = dict(bao)
    output["rows"] = [bao["rows"][index] for index in indices]
    output["covariance"] = covariance
    output["split_label"] = label
    return output


def bao_quantity_list(bao: dict[str, Any]) -> str:
    quantities = sorted({str(row["quantity"]) for row in bao["rows"]})
    return ";".join(quantities)


def scenario_row(release: str, scenario_id: str, scenario_type: str, description: str, sn: dict[str, Any], bao: dict[str, Any]) -> dict[str, Any]:
    sn_z = np.asarray(sn["z"], dtype=float)
    bao_z = np.asarray([row["z"] for row in bao["rows"]], dtype=float)
    return {
        "release_branch": release,
        "scenario_id": scenario_id,
        "scenario_type": scenario_type,
        "description": description,
        "sn_rows": int(len(sn_z)),
        "bao_rows": int(len(bao["rows"])),
        "sn_z_min": float(np.min(sn_z)),
        "sn_z_max": float(np.max(sn_z)),
        "bao_z_min": float(np.min(bao_z)),
        "bao_z_max": float(np.max(bao_z)),
        "bao_quantities": bao_quantity_list(bao),
        "same_nuisance_policy": "SN analytic offset plus BAO analytic alpha for every model",
        "same_calibration_policy": "no SH0ES calibrators; Pantheon+ shape offset only",
    }


def build_scenarios(release: str, sn: dict[str, Any], bao: dict[str, Any], include_bao_jackknife: bool) -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = [
        {
            "scenario_id": "full_reference",
            "scenario_type": "full",
            "description": "full Pantheon+ no-SH0ES shape plus full BAO covariance",
            "sn": sn,
            "bao": bao,
        }
    ]

    median_sn_z = float(np.median(sn["z"]))
    scenarios.extend(
        [
            {
                "scenario_id": "SN_low_z_half_plus_all_BAO",
                "scenario_type": "SN_redshift_split",
                "description": f"SN z <= median {median_sn_z:.6g}; all BAO rows retained",
                "sn": subset_sn(sn, np.asarray(sn["z"]) <= median_sn_z, "SN_low_z_half"),
                "bao": bao,
            },
            {
                "scenario_id": "SN_high_z_half_plus_all_BAO",
                "scenario_type": "SN_redshift_split",
                "description": f"SN z > median {median_sn_z:.6g}; all BAO rows retained",
                "sn": subset_sn(sn, np.asarray(sn["z"]) > median_sn_z, "SN_high_z_half"),
                "bao": bao,
            },
        ]
    )

    all_bao_indices = list(range(len(bao["rows"])))
    for quantity in sorted({str(row["quantity"]) for row in bao["rows"]}):
        keep = [index for index, row in enumerate(bao["rows"]) if str(row["quantity"]) != quantity]
        scenarios.append(
            {
                "scenario_id": f"BAO_without_{quantity}",
                "scenario_type": "BAO_quantity_leaveout",
                "description": f"full SN retained; BAO observable class {quantity} removed",
                "sn": sn,
                "bao": subset_bao(bao, keep, f"BAO_without_{quantity}"),
            }
        )

    bao_z = np.asarray([row["z"] for row in bao["rows"]], dtype=float)
    median_bao_z = float(np.median(bao_z))
    low_bao = [index for index, z_value in enumerate(bao_z) if z_value <= median_bao_z]
    high_bao = [index for index, z_value in enumerate(bao_z) if z_value > median_bao_z]
    scenarios.extend(
        [
            {
                "scenario_id": "BAO_low_z_half_plus_all_SN",
                "scenario_type": "BAO_redshift_split",
                "description": f"full SN retained; BAO z <= median {median_bao_z:.6g}",
                "sn": sn,
                "bao": subset_bao(bao, low_bao, "BAO_low_z_half"),
            },
            {
                "scenario_id": "BAO_high_z_half_plus_all_SN",
                "scenario_type": "BAO_redshift_split",
                "description": f"full SN retained; BAO z > median {median_bao_z:.6g}",
                "sn": sn,
                "bao": subset_bao(bao, high_bao, "BAO_high_z_half"),
            },
        ]
    )

    if include_bao_jackknife:
        for index in all_bao_indices:
            row = bao["rows"][index]
            keep = [candidate for candidate in all_bao_indices if candidate != index]
            scenarios.append(
                {
                    "scenario_id": f"BAO_leave_one_row_{index:02d}",
                    "scenario_type": "BAO_row_jackknife",
                    "description": f"full SN retained; removed BAO row {index} ({row['quantity']} at z={row['z']})",
                    "sn": sn,
                    "bao": subset_bao(bao, keep, f"BAO_leave_one_row_{index:02d}"),
                }
            )
    return scenarios


def score_one_model(model: str, sn: dict[str, Any], bao: dict[str, Any], max_iter: int) -> dict[str, Any]:
    if model == LEAD_BRANCH:
        score = release_matrix.score_fixed_bmem(sn, bao, max_iter=max_iter)
    elif model == "CPL":
        score = closure_runner.score_model("CPL", sn, bao, max_iter=max_iter, prior_config=release_matrix.CPL_WIDE_PRIORS)
    else:
        score = closure_runner.score_model(model, sn, bao, max_iter=max_iter)
    score.setdefault("role", "baseline" if model in BASELINES else "control")
    score.setdefault("source_model_key", model)
    return score


def failed_score(model: str, scenario: dict[str, Any], exc: Exception) -> dict[str, Any]:
    n_points = int(len(scenario["sn"]["z"]) + len(scenario["bao"]["rows"]))
    return {
        "model": model,
        "source_model_key": model,
        "role": "failed",
        "params": {},
        "chi2_SN": math.inf,
        "chi2_BAO": math.inf,
        "chi2_total": math.inf,
        "AIC": math.inf,
        "BIC": math.inf,
        "n": n_points,
        "k": "",
        "dof": "",
        "convergence": False,
        "prior_edge_flag": True,
        "claim_ceiling": CLAIM_CEILING,
        "sn_offset": "",
        "bao_alpha": "",
        "optimizer_message": f"{type(exc).__name__}: {exc}",
        "edge_rows": [
            {
                "model": model,
                "parameter": "fit",
                "best_fit": "",
                "lower": "",
                "upper": "",
                "distance_to_edge": "",
                "edge_flag": True,
            }
        ],
    }


def score_scenario(release: str, scenario: dict[str, Any], max_iter: int) -> list[dict[str, Any]]:
    scores = []
    for model in MODEL_ORDER:
        try:
            score = score_one_model(model, scenario["sn"], scenario["bao"], max_iter=max_iter)
        except (ValueError, FloatingPointError, linalg.LinAlgError, RuntimeError) as exc:
            score = failed_score(model, scenario, exc)
        score["release_branch"] = release
        score["scenario_id"] = scenario["scenario_id"]
        score["scenario_type"] = scenario["scenario_type"]
        scores.append(score)
    return scores


def fit_summary_rows(all_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for score in all_scores:
        params = score.get("params", {})
        rows.append(
            {
                "release_branch": score["release_branch"],
                "scenario_id": score["scenario_id"],
                "scenario_type": score["scenario_type"],
                "model": score["model"],
                "role": score.get("role", ""),
                "source_model_key": score.get("source_model_key", score["model"]),
                "chi2_SN": score["chi2_SN"],
                "chi2_BAO": score["chi2_BAO"],
                "chi2_total": score["chi2_total"],
                "AIC": score["AIC"],
                "BIC": score["BIC"],
                "n": score["n"],
                "k": score["k"],
                "dof": score["dof"],
                "convergence": score["convergence"],
                "prior_edge_flag": score["prior_edge_flag"],
                "Omega_m": params.get("Omega_m", ""),
                "w": params.get("w", ""),
                "w0": params.get("w0", ""),
                "wa": params.get("wa", ""),
                "B_mem": params.get("B_mem", ""),
                "p": params.get("p", ""),
                "u3": params.get("u3", ""),
                "sn_offset": score["sn_offset"],
                "bao_alpha": score["bao_alpha"],
                "claim_ceiling": score["claim_ceiling"],
                "optimizer_message": score["optimizer_message"],
            }
        )
    return rows


def prior_edge_rows(all_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for score in all_scores:
        for edge in score.get("edge_rows", []):
            rows.append(
                {
                    "release_branch": score["release_branch"],
                    "scenario_id": score["scenario_id"],
                    "scenario_type": score["scenario_type"],
                    **edge,
                }
            )
    return rows


def comparison_readout(delta_chi2: float, delta_aic: float, delta_bic: float) -> str:
    if delta_chi2 < 0.0 and delta_aic < 0.0 and delta_bic < 0.0:
        return "raw_AIC_BIC_win"
    if delta_chi2 < 0.0 and delta_aic < 0.0 and delta_bic > 0.0:
        return "raw_AIC_win_BIC_penalty_loss"
    if delta_bic < 0.0:
        return "BIC_win"
    if delta_bic < 2.0:
        return "close_round_BIC_loss_under_2"
    if delta_bic < 6.0:
        return "moderate_BIC_loss_2_to_6"
    return "strong_BIC_loss_over_6"


def baseline_comparison_rows(all_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    scenario_keys = sorted({(score["release_branch"], score["scenario_id"]) for score in all_scores})
    for release, scenario_id in scenario_keys:
        subset = [score for score in all_scores if score["release_branch"] == release and score["scenario_id"] == scenario_id]
        by_model = {score["model"]: score for score in subset}
        for model in MODEL_ORDER:
            if model not in by_model:
                continue
            score = by_model[model]
            for reference in MODEL_ORDER:
                if reference == model or reference not in by_model:
                    continue
                base = by_model[reference]
                delta_chi2 = float(score["chi2_total"] - base["chi2_total"])
                delta_aic = float(score["AIC"] - base["AIC"])
                delta_bic = float(score["BIC"] - base["BIC"])
                rows.append(
                    {
                        "release_branch": release,
                        "scenario_id": scenario_id,
                        "scenario_type": score["scenario_type"],
                        "model": model,
                        "reference_baseline": reference,
                        "delta_chi2": delta_chi2,
                        "delta_AIC": delta_aic,
                        "delta_BIC": delta_bic,
                        "model_k": score["k"],
                        "reference_k": base["k"],
                        "same_data": True,
                        "same_nuisance": True,
                        "same_calibration": True,
                        "readout": comparison_readout(delta_chi2, delta_aic, delta_bic),
                    }
                )
    return rows


def primary_stability_rows(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for baseline in BASELINES:
        subset = [
            row
            for row in comparisons
            if row["model"] == LEAD_BRANCH and row["reference_baseline"] == baseline
        ]
        delta_bic = np.asarray([float(row["delta_BIC"]) for row in subset], dtype=float)
        delta_aic = np.asarray([float(row["delta_AIC"]) for row in subset], dtype=float)
        delta_chi2 = np.asarray([float(row["delta_chi2"]) for row in subset], dtype=float)
        scenario_count = int(len(subset))
        bic_wins = int(np.sum(delta_bic < 0.0))
        aic_wins = int(np.sum(delta_aic < 0.0))
        raw_wins = int(np.sum(delta_chi2 < 0.0))
        if scenario_count == 0:
            readout = "not_scored"
        elif bic_wins == scenario_count:
            readout = "clean_BIC_win_all_splits"
        elif bic_wins >= math.ceil(0.6 * scenario_count) and float(np.max(delta_bic)) < 2.0:
            readout = "survives_as_close_rounds"
        elif float(np.max(delta_bic)) < 6.0:
            readout = "mixed_but_no_strong_BIC_loss"
        else:
            readout = "stress_or_failure_strong_BIC_loss_present"
        rows.append(
            {
                "model": LEAD_BRANCH,
                "reference_baseline": baseline,
                "scenario_count": scenario_count,
                "raw_chi2_wins": raw_wins,
                "AIC_wins": aic_wins,
                "BIC_wins": bic_wins,
                "BIC_win_fraction": "" if scenario_count == 0 else bic_wins / scenario_count,
                "median_delta_BIC": "" if scenario_count == 0 else float(np.median(delta_bic)),
                "worst_delta_BIC": "" if scenario_count == 0 else float(np.max(delta_bic)),
                "best_delta_BIC": "" if scenario_count == 0 else float(np.min(delta_bic)),
                "readout": readout,
            }
        )
    return rows


def zero_memory_control_rows(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    subset = [
        row
        for row in comparisons
        if row["model"] == CONTROL_BRANCH and row["reference_baseline"] == "LCDM"
    ]
    return [
        {
            "release_branch": row["release_branch"],
            "scenario_id": row["scenario_id"],
            "delta_chi2_vs_LCDM": row["delta_chi2"],
            "delta_AIC_vs_LCDM": row["delta_AIC"],
            "delta_BIC_vs_LCDM": row["delta_BIC"],
            "tracks_LCDM": abs(float(row["delta_chi2"])) < 1.0e-5 and abs(float(row["delta_AIC"])) < 1.0e-5 and abs(float(row["delta_BIC"])) < 1.0e-5,
        }
        for row in subset
    ]


def gate_rows(
    source_rows: list[dict[str, Any]],
    scenario_rows: list[dict[str, Any]],
    fit_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    stability_rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    scenario_count = len(scenario_rows)
    expected_fits = scenario_count * len(MODEL_ORDER)
    sources_ok = all(row["exists"] == "yes" for row in source_rows)
    all_scored = len(fit_rows) == expected_fits
    all_converged = all(str(row["convergence"]) == "True" or row["convergence"] is True for row in fit_rows)
    no_edges = all(str(row["edge_flag"]) == "False" or row["edge_flag"] is False for row in edge_rows)
    fixed_edges = [
        row
        for row in edge_rows
        if row["model"] == LEAD_BRANCH and not (str(row["edge_flag"]) == "False" or row["edge_flag"] is False)
    ]
    fixed_no_edges = len(fixed_edges) == 0

    primary_vs_lcdm = [
        row for row in comparisons if row["model"] == LEAD_BRANCH and row["reference_baseline"] == "LCDM"
    ]
    no_strong_lcdm_loss = bool(primary_vs_lcdm) and all(float(row["delta_BIC"]) < 6.0 for row in primary_vs_lcdm)
    majority_bic_wins = {
        row["reference_baseline"]: float(row["BIC_win_fraction"]) >= 0.5
        for row in stability_rows
        if row["BIC_win_fraction"] != ""
    }
    zero_tracks = bool(control_rows) and all(str(row["tracks_LCDM"]) == "True" or row["tracks_LCDM"] is True for row in control_rows)
    gates = [
        ("source_paths_exist", sources_ok, "all runner, checkpoint, SN, SN-covariance, and BAO source paths exist"),
        ("all_scenarios_scored", all_scored, f"{len(fit_rows)} fits written for {scenario_count} scenarios and {len(MODEL_ORDER)} models"),
        ("all_models_converged", all_converged, "all baselines, fixed branch, and zero-memory controls converged or are explicitly failed"),
        ("no_prior_edge_flags_any_model", no_edges, "no fitted branch, including baselines, sits on an optimizer prior edge"),
        ("fixed_no_prior_edge_flags", fixed_no_edges, "strict fixed branch has no fitted parameter on a prior edge"),
        ("fixed_no_strong_BIC_loss_vs_LCDM", no_strong_lcdm_loss, "no split gives the fixed branch a strong BIC loss > 6 against LCDM"),
        ("fixed_BIC_win_majority_vs_LCDM", majority_bic_wins.get("LCDM", False), "fixed branch wins at least half the split scenarios by BIC against LCDM"),
        ("fixed_BIC_win_majority_vs_wCDM", majority_bic_wins.get("wCDM", False), "fixed branch wins at least half the split scenarios by BIC against wCDM"),
        ("fixed_BIC_win_majority_vs_CPL", majority_bic_wins.get("CPL", False), "fixed branch wins at least half the split scenarios by BIC against CPL"),
        ("Bmem_zero_tracks_LCDM", zero_tracks, "zero-memory control collapses onto LCDM in every split"),
        ("Bmem_parent_derived", False, "2/27 remains locked empirical closure/theorem target, not parent-derived"),
        ("stable_evidence_allowed", False, "split robustness is still diagnostic; no public claim promotion"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def decision_rows(gates: list[dict[str, Any]], stability_rows: list[dict[str, Any]], include_bao_jackknife: bool) -> list[dict[str, Any]]:
    gates_by_name = {row["gate"]: row["status"] for row in gates}
    key_gates = [
        "source_paths_exist",
        "all_scenarios_scored",
        "all_models_converged",
        "fixed_no_prior_edge_flags",
        "fixed_no_strong_BIC_loss_vs_LCDM",
        "Bmem_zero_tracks_LCDM",
    ]
    core_ok = all(gates_by_name.get(gate) == "pass" for gate in key_gates)
    majority_all = all(
        gates_by_name.get(gate) == "pass"
        for gate in [
            "fixed_BIC_win_majority_vs_LCDM",
            "fixed_BIC_win_majority_vs_wCDM",
            "fixed_BIC_win_majority_vs_CPL",
        ]
    )
    if core_ok and majority_all:
        status = STATUS_SURVIVES
        readout = "fixed_2over27_survives_symmetric_split_first_pass_without_claim_promotion"
    elif core_ok:
        status = STATUS_MIXED
        readout = "fixed_2over27_is_still_alive_but_split_score_is_mixed"
    else:
        status = STATUS_FAILS
        readout = "fixed_2over27_needs_repair_or_demotion_on_this_split_matrix"
    return [
        {"key": "status", "value": status},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "readout", "value": readout},
        {"key": "BAO_row_jackknife_included", "value": str(include_bao_jackknife).lower()},
        {"key": "stable_evidence_allowed", "value": "false"},
        {"key": "parent_amplitude_derived", "value": "false"},
        {"key": "next_action", "value": "derive_or_reject_parent_origin_of_Bmem_2over27_and_then_run_external_Hz_growth_or_CMB_bridge_tests"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=120)
    parser.add_argument("--include-bao-jackknife", action="store_true")
    args = parser.parse_args()

    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    script_path = Path(__file__).resolve()
    sources = source_register_rows(script_path)
    missing = [row["source"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing source artifacts: {missing}")

    scenario_register: list[dict[str, Any]] = []
    all_scores: list[dict[str, Any]] = []
    for release in release_matrix.BAO_RELEASES:
        sn, bao, _config = release_matrix.load_release_data(release)
        scenarios = build_scenarios(release, sn, bao, include_bao_jackknife=args.include_bao_jackknife)
        for scenario in scenarios:
            scenario_register.append(
                scenario_row(
                    release,
                    scenario["scenario_id"],
                    scenario["scenario_type"],
                    scenario["description"],
                    scenario["sn"],
                    scenario["bao"],
                )
            )
            all_scores.extend(score_scenario(release, scenario, max_iter=args.max_iter))

    fit_rows = fit_summary_rows(all_scores)
    edge_rows = prior_edge_rows(all_scores)
    comparisons = baseline_comparison_rows(all_scores)
    stability = primary_stability_rows(comparisons)
    control = zero_memory_control_rows(comparisons)
    gates = gate_rows(sources, scenario_register, fit_rows, edge_rows, comparisons, stability, control)
    decisions = decision_rows(gates, stability, include_bao_jackknife=args.include_bao_jackknife)
    status = next(row["value"] for row in decisions if row["key"] == "status")

    write_csv(result_dir / "source_register.csv", sources, ["source", "role", "exists", "bytes"])
    write_csv(
        result_dir / "scenario_register.csv",
        scenario_register,
        [
            "release_branch",
            "scenario_id",
            "scenario_type",
            "description",
            "sn_rows",
            "bao_rows",
            "sn_z_min",
            "sn_z_max",
            "bao_z_min",
            "bao_z_max",
            "bao_quantities",
            "same_nuisance_policy",
            "same_calibration_policy",
        ],
    )
    write_csv(
        result_dir / "split_fit_summary.csv",
        fit_rows,
        [
            "release_branch",
            "scenario_id",
            "scenario_type",
            "model",
            "role",
            "source_model_key",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "AIC",
            "BIC",
            "n",
            "k",
            "dof",
            "convergence",
            "prior_edge_flag",
            "Omega_m",
            "w",
            "w0",
            "wa",
            "B_mem",
            "p",
            "u3",
            "sn_offset",
            "bao_alpha",
            "claim_ceiling",
            "optimizer_message",
        ],
    )
    write_csv(
        result_dir / "split_baseline_comparison.csv",
        comparisons,
        [
            "release_branch",
            "scenario_id",
            "scenario_type",
            "model",
            "reference_baseline",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "model_k",
            "reference_k",
            "same_data",
            "same_nuisance",
            "same_calibration",
            "readout",
        ],
    )
    write_csv(
        result_dir / "split_stability_summary.csv",
        stability,
        [
            "model",
            "reference_baseline",
            "scenario_count",
            "raw_chi2_wins",
            "AIC_wins",
            "BIC_wins",
            "BIC_win_fraction",
            "median_delta_BIC",
            "worst_delta_BIC",
            "best_delta_BIC",
            "readout",
        ],
    )
    write_csv(
        result_dir / "zero_memory_control.csv",
        control,
        ["release_branch", "scenario_id", "delta_chi2_vs_LCDM", "delta_AIC_vs_LCDM", "delta_BIC_vs_LCDM", "tracks_LCDM"],
    )
    write_csv(
        result_dir / "split_prior_edge_table.csv",
        edge_rows,
        ["release_branch", "scenario_id", "scenario_type", "model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"],
    )
    write_csv(result_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decisions, ["key", "value"])

    payload = {
        "script": str(script_path),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "claim_ceiling": CLAIM_CEILING,
        "stable_evidence_allowed": False,
        "parent_amplitude_derived": False,
        "release_branches": list(release_matrix.BAO_RELEASES),
        "scenario_count": len(scenario_register),
        "models": MODEL_ORDER,
        "max_iter": args.max_iter,
        "include_bao_jackknife": args.include_bao_jackknife,
        "next_action": "derive_or_reject_parent_origin_of_Bmem_2over27_and_then_extend_to_external_Hz_growth_or_CMB_bridge_gates",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(status + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
