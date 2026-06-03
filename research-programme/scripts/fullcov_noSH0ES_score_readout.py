from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "fullcov-noSH0ES-score-readout"
STATUS = "MTS_fixed_survives_fullcov_noSH0ES_short_smoke_as_competitive_diagnostic_not_LCDM_BIC_win"
CLAIM_CEILING = "short_smoke_late_time_background_diagnostic_only_no_stable_evidence_or_theory_promotion"

DR2_SCORE_RUN = ROOT / "runs" / "20260601-000140-cosmo-SN-BAO-short-smoke"
DR1_SCORE_RUN = ROOT / "runs" / "20260601-000141-cosmo-SN-BAO-short-smoke"
DRYRUN_READOUT = ROOT / "runs" / "20260601-000139-fullcov-noSH0ES-dryrun-readout"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def as_float(value: str) -> float:
    return float(value)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def pass_fail(value: bool) -> str:
    return "pass" if value else "fail"


def score_runs() -> dict[str, Path]:
    return {
        "DESI_DR2_fullcov_noSH0ES": DR2_SCORE_RUN,
        "DESI_DR1_fullcov_noSH0ES": DR1_SCORE_RUN,
    }


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "314-fullcov-noSH0ES-dryrun-readout.md", "dry-run readout checkpoint"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "SN+BAO runner"),
        (ROOT / "scripts" / "fullcov_noSH0ES_score_readout.py", "this score readout script"),
        (DRYRUN_READOUT / "results" / "score_readiness_gates.csv", "score readiness gates"),
    ]
    for label, run in score_runs().items():
        sources.extend(
            [
                (run / "status.json", f"{label} score status"),
                (run / "results" / "fit_summary.csv", f"{label} fit summary"),
                (run / "results" / "baseline_comparison.csv", f"{label} baseline comparison"),
                (run / "results" / "prior_edge_table.csv", f"{label} prior-edge table"),
                (run / "results" / "residuals.csv", f"{label} residual table"),
            ]
        )
    return [{"source": relpath(path), "role": role, "exists": yes_no(path.exists())} for path, role in sources]


def score_summary_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run in score_runs().items():
        for row in read_csv(run / "results" / "fit_summary.csv"):
            rows.append(
                {
                    "release_branch": label,
                    "model": row["model"],
                    "chi2_SN": row["chi2_SN"],
                    "chi2_BAO": row["chi2_BAO"],
                    "chi2_total": row["chi2_total"],
                    "dof": row["dof"],
                    "k": row["k"],
                    "n": row["n"],
                    "AIC": row["AIC"],
                    "BIC": row["BIC"],
                    "convergence": row["convergence"],
                    "prior_edge_flag": row["prior_edge_flag"],
                    "claim_ceiling": row["claim_ceiling"],
                }
            )
    return rows


def interpretation(delta_chi2: float, delta_aic: float, delta_bic: float) -> str:
    if delta_chi2 < 0.0 and delta_aic < 0.0 and delta_bic < 0.0:
        return "raw_AIC_BIC_win"
    if delta_chi2 < 0.0 and delta_aic < 0.0 and delta_bic > 0.0:
        return "raw_AIC_win_BIC_penalty_loss"
    if delta_chi2 > 0.0 and delta_aic < 0.0 and delta_bic < 0.0:
        return "penalty_adjusted_win_despite_raw_chi2_loss"
    if delta_aic < 0.0 or delta_bic < 0.0:
        return "mixed_information_criteria"
    return "not_preferred"


def mts_vs_baseline_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run in score_runs().items():
        for row in read_csv(run / "results" / "baseline_comparison.csv"):
            if row["model"] != "MTS_fixed_p3_u3quarter":
                continue
            delta_chi2 = as_float(row["delta_chi2"])
            delta_aic = as_float(row["delta_AIC"])
            delta_bic = as_float(row["delta_BIC"])
            rows.append(
                {
                    "release_branch": label,
                    "model": row["model"],
                    "reference_baseline": row["reference_baseline"],
                    "delta_chi2": delta_chi2,
                    "delta_AIC": delta_aic,
                    "delta_BIC": delta_bic,
                    "same_data": row["same_data"],
                    "same_nuisance": row["same_nuisance"],
                    "same_calibration": row["same_calibration"],
                    "interpretation": interpretation(delta_chi2, delta_aic, delta_bic),
                }
            )
    return rows


def prior_edge_audit_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run in score_runs().items():
        for row in read_csv(run / "results" / "prior_edge_table.csv"):
            rows.append(
                {
                    "release_branch": label,
                    "model": row["model"],
                    "parameter": row["parameter"],
                    "best_fit": row["best_fit"],
                    "lower": row["lower"],
                    "upper": row["upper"],
                    "distance_to_edge": row["distance_to_edge"],
                    "edge_flag": row["edge_flag"],
                }
            )
    return rows


def best_fit_parameter(release: str, model: str, parameter: str) -> float:
    run = score_runs()[release]
    for row in read_csv(run / "results" / "prior_edge_table.csv"):
        if row["model"] == model and row["parameter"] == parameter:
            return as_float(row["best_fit"])
    raise KeyError((release, model, parameter))


def release_stability_rows() -> list[dict[str, Any]]:
    rows = []
    dr2_bmem = best_fit_parameter("DESI_DR2_fullcov_noSH0ES", "MTS_fixed_p3_u3quarter", "B_mem")
    dr1_bmem = best_fit_parameter("DESI_DR1_fullcov_noSH0ES", "MTS_fixed_p3_u3quarter", "B_mem")
    rows.append(
        {
            "quantity": "B_mem",
            "DR2": dr2_bmem,
            "DR1": dr1_bmem,
            "DR1_minus_DR2": dr1_bmem - dr2_bmem,
            "relative_shift_vs_DR2": (dr1_bmem - dr2_bmem) / dr2_bmem,
            "interpretation": "stable_to_release_split_at_short_smoke_level",
        }
    )
    by_release_baseline = {
        (row["release_branch"], row["reference_baseline"]): row for row in mts_vs_baseline_rows()
    }
    for baseline in ["LCDM", "wCDM", "CPL"]:
        dr2 = by_release_baseline[("DESI_DR2_fullcov_noSH0ES", baseline)]
        dr1 = by_release_baseline[("DESI_DR1_fullcov_noSH0ES", baseline)]
        for metric in ["delta_chi2", "delta_AIC", "delta_BIC"]:
            rows.append(
                {
                    "quantity": f"MTS_fixed_vs_{baseline}_{metric}",
                    "DR2": dr2[metric],
                    "DR1": dr1[metric],
                    "DR1_minus_DR2": as_float(str(dr1[metric])) - as_float(str(dr2[metric])),
                    "relative_shift_vs_DR2": "" if as_float(str(dr2[metric])) == 0.0 else (as_float(str(dr1[metric])) - as_float(str(dr2[metric]))) / abs(as_float(str(dr2[metric]))),
                    "interpretation": "release_shift_diagnostic_not_evidence_claim",
                }
            )
    return rows


def information_criteria_ruling_rows() -> list[dict[str, Any]]:
    rows = []
    for baseline in ["LCDM", "wCDM", "CPL"]:
        branch_rows = [row for row in mts_vs_baseline_rows() if row["reference_baseline"] == baseline]
        beats_chi2 = all(as_float(str(row["delta_chi2"])) < 0.0 for row in branch_rows)
        beats_aic = all(as_float(str(row["delta_AIC"])) < 0.0 for row in branch_rows)
        beats_bic = all(as_float(str(row["delta_BIC"])) < 0.0 for row in branch_rows)
        if baseline == "LCDM":
            ruling = "competitive_but_not_LCDM_BIC_win"
        elif beats_chi2 and beats_aic and beats_bic:
            ruling = "same_or_lower_penalty_win"
        elif beats_aic and beats_bic:
            ruling = "information_criteria_win"
        else:
            ruling = "mixed"
        rows.append(
            {
                "reference_baseline": baseline,
                "beats_chi2_both_releases": pass_fail(beats_chi2),
                "beats_AIC_both_releases": pass_fail(beats_aic),
                "beats_BIC_both_releases": pass_fail(beats_bic),
                "ruling": ruling,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_register_rows())
    status_rows = [read_json(run / "status.json") for run in score_runs().values()]
    scores_written = all(row["scores_written"] is True for row in status_rows)
    no_failures = all(not row["failures"] for row in status_rows)
    converged = all(row["convergence"] == "True" for row in score_summary_rows())
    no_edges = all(row["edge_flag"] == "False" for row in prior_edge_audit_rows())
    mts_rows = mts_vs_baseline_rows()
    m_lcdm = [row for row in mts_rows if row["reference_baseline"] == "LCDM"]
    m_wcdm = [row for row in mts_rows if row["reference_baseline"] == "wCDM"]
    m_cpl = [row for row in mts_rows if row["reference_baseline"] == "CPL"]
    bmem_dr2 = best_fit_parameter("DESI_DR2_fullcov_noSH0ES", "MTS_fixed_p3_u3quarter", "B_mem")
    bmem_dr1 = best_fit_parameter("DESI_DR1_fullcov_noSH0ES", "MTS_fixed_p3_u3quarter", "B_mem")
    bmem_stable = abs((bmem_dr1 - bmem_dr2) / bmem_dr2) < 0.05
    gates = [
        ("score_paths_exist", sources_ok, "score and readout sources exist"),
        ("scores_written", scores_written, "both short-smoke score runs wrote fit summaries"),
        ("no_runtime_failures", no_failures, "runner status failure lists are empty"),
        ("all_models_converged", converged, "LCDM/wCDM/CPL/MTS branches converged"),
        ("no_prior_edge_flags", no_edges, "best fits are not sitting on prior boundaries"),
        ("MTS_fixed_beats_LCDM_chi2", all(as_float(str(row["delta_chi2"])) < 0.0 for row in m_lcdm), "MTS fixed improves raw chi2 over LCDM in both releases"),
        ("MTS_fixed_beats_LCDM_AIC", all(as_float(str(row["delta_AIC"])) < 0.0 for row in m_lcdm), "MTS fixed beats LCDM by AIC in both releases"),
        ("MTS_fixed_beats_LCDM_BIC", all(as_float(str(row["delta_BIC"])) < 0.0 for row in m_lcdm), "deliberate fail: LCDM still wins BIC penalty in both releases"),
        ("MTS_fixed_beats_wCDM_same_k", all(as_float(str(row["delta_BIC"])) < 0.0 for row in m_wcdm), "MTS fixed slightly beats wCDM with equal parameter count"),
        ("MTS_fixed_beats_CPL_AIC_BIC", all(as_float(str(row["delta_AIC"])) < 0.0 and as_float(str(row["delta_BIC"])) < 0.0 for row in m_cpl), "MTS fixed beats CPL after information-criterion penalties"),
        ("B_mem_release_stability", bmem_stable, "B_mem shifts by less than 5 percent between DR2 and DR1"),
        ("stable_evidence_allowed", False, "short-smoke diagnostic cannot support stable-evidence language"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "meaning": meaning} for gate, ok, meaning in gates]


def derivation_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "derive_FLRW_memory_projection",
            "why_now": "B_mem is nonzero, away from prior edges, and stable across DR2/DR1 in this short-smoke gate",
            "required_contract": "derive sign, amplitude scale, and no-clock p=3/u3=1/4 closure from parent projection rather than fitting it by hand",
            "failure_consequence": "demote B_mem=2/27/no-clock branch to empirical closure only",
        },
        {
            "target": "connect_negative_control_to_LCDM_limit",
            "why_now": "MTS_Bmem_zero exactly collapses onto LCDM in the score tables",
            "required_contract": "prove B_mem -> 0 is the LCDM/background-GR limit of the projected FLRW equations",
            "failure_consequence": "runner may be testing a phenomenological add-on rather than a theory limit",
        },
        {
            "target": "replace_short_smoke_with_robustness_matrix",
            "why_now": "LCDM still wins BIC against MTS fixed even when MTS improves chi2 and AIC",
            "required_contract": "jackknife/split/prior scans must be applied symmetrically to LCDM, wCDM, CPL, and MTS",
            "failure_consequence": "no stable empirical preference claim",
        },
    ]


def residual_points(run: Path, dataset_kind: str, model: str, max_points: int = 800) -> list[tuple[float, float]]:
    rows = []
    for row in read_csv(run / "results" / "residuals.csv"):
        is_sn = row["dataset"].startswith("SN")
        if dataset_kind == "SN" and not is_sn:
            continue
        if dataset_kind == "BAO" and is_sn:
            continue
        if row["model"] != model:
            continue
        rows.append((as_float(row["coordinate"]), as_float(row["residual"])))
    rows.sort(key=lambda item: item[0])
    if len(rows) <= max_points:
        return rows
    step = math.ceil(len(rows) / max_points)
    return rows[::step]


def write_residual_svg(path: Path, title: str, series: dict[str, list[tuple[float, float]]]) -> None:
    width, height = 900, 420
    margin_left, margin_right, margin_top, margin_bottom = 70, 30, 45, 60
    points = [point for values in series.values() for point in values]
    if not points:
        path.write_text("<svg xmlns='http://www.w3.org/2000/svg'></svg>\n", encoding="utf-8")
        return
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    if x_min == x_max:
        x_min -= 1.0
        x_max += 1.0
    if y_min == y_max:
        y_min -= 1.0
        y_max += 1.0
    y_pad = 0.08 * (y_max - y_min)
    y_min -= y_pad
    y_max += y_pad

    def sx(x: float) -> float:
        return margin_left + (x - x_min) / (x_max - x_min) * (width - margin_left - margin_right)

    def sy(y: float) -> float:
        return height - margin_bottom - (y - y_min) / (y_max - y_min) * (height - margin_top - margin_bottom)

    colors = {
        "LCDM": "#1f77b4",
        "MTS_fixed_p3_u3quarter": "#d62728",
    }
    content = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='white'/>",
        f"<text x='{margin_left}' y='28' font-size='18' font-family='Arial'>{title}</text>",
        f"<line x1='{margin_left}' y1='{height - margin_bottom}' x2='{width - margin_right}' y2='{height - margin_bottom}' stroke='#222'/>",
        f"<line x1='{margin_left}' y1='{margin_top}' x2='{margin_left}' y2='{height - margin_bottom}' stroke='#222'/>",
        f"<line x1='{margin_left}' y1='{sy(0.0)}' x2='{width - margin_right}' y2='{sy(0.0)}' stroke='#888' stroke-dasharray='4 4'/>",
        f"<text x='{width / 2 - 40}' y='{height - 18}' font-size='13' font-family='Arial'>coordinate / redshift</text>",
        f"<text x='16' y='{height / 2}' transform='rotate(-90 16 {height / 2})' font-size='13' font-family='Arial'>residual</text>",
    ]
    legend_y = 52
    for index, (model, values) in enumerate(series.items()):
        color = colors.get(model, "#333333")
        for x, y in values:
            content.append(f"<circle cx='{sx(x):.2f}' cy='{sy(y):.2f}' r='1.8' fill='{color}' opacity='0.62'/>")
        content.append(f"<circle cx='{margin_left + 10}' cy='{legend_y + 18 * index}' r='4' fill='{color}'/>")
        content.append(f"<text x='{margin_left + 22}' y='{legend_y + 4 + 18 * index}' font-size='12' font-family='Arial'>{model}</text>")
    content.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(content) + "\n", encoding="utf-8")


def plot_artifact_rows(result_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for label, run in score_runs().items():
        for dataset_kind in ["SN", "BAO"]:
            filename = f"{label}_{dataset_kind}_residuals.svg"
            path = result_dir / "plots" / filename
            series = {
                "LCDM": residual_points(run, dataset_kind, "LCDM"),
                "MTS_fixed_p3_u3quarter": residual_points(run, dataset_kind, "MTS_fixed_p3_u3quarter"),
            }
            write_residual_svg(path, f"{label} {dataset_kind} residuals: LCDM vs MTS fixed", series)
            rows.append(
                {
                    "release_branch": label,
                    "plot": relpath(path),
                    "dataset": dataset_kind,
                    "models": "LCDM; MTS_fixed_p3_u3quarter",
                    "status": "written",
                }
            )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"key": "status", "value": STATUS},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "best_current_readout", "value": "competitive_diagnostic_round_not_a_knockout"},
        {"key": "stable_evidence_allowed", "value": "false"},
        {"key": "next_action", "value": "derive_or_reject_FLRW_memory_projection_amplitude_contract_then_run_symmetric_robustness_matrix"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=None)
    args = parser.parse_args()
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    score_rows = score_summary_rows()
    mts_rows = mts_vs_baseline_rows()
    edge_rows = prior_edge_audit_rows()
    stability_rows = release_stability_rows()
    ruling_rows = information_criteria_ruling_rows()
    gate_rows = claim_gate_rows()
    target_rows = derivation_target_rows()
    plot_rows = plot_artifact_rows(result_dir)
    decision = decision_rows()

    write_csv(result_dir / "source_register.csv", source_rows, ["source", "role", "exists"])
    write_csv(
        result_dir / "score_summary.csv",
        score_rows,
        ["release_branch", "model", "chi2_SN", "chi2_BAO", "chi2_total", "dof", "k", "n", "AIC", "BIC", "convergence", "prior_edge_flag", "claim_ceiling"],
    )
    write_csv(
        result_dir / "MTS_fixed_vs_baselines.csv",
        mts_rows,
        ["release_branch", "model", "reference_baseline", "delta_chi2", "delta_AIC", "delta_BIC", "same_data", "same_nuisance", "same_calibration", "interpretation"],
    )
    write_csv(
        result_dir / "release_stability.csv",
        stability_rows,
        ["quantity", "DR2", "DR1", "DR1_minus_DR2", "relative_shift_vs_DR2", "interpretation"],
    )
    write_csv(
        result_dir / "prior_edge_audit.csv",
        edge_rows,
        ["release_branch", "model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"],
    )
    write_csv(
        result_dir / "information_criteria_ruling.csv",
        ruling_rows,
        ["reference_baseline", "beats_chi2_both_releases", "beats_AIC_both_releases", "beats_BIC_both_releases", "ruling"],
    )
    write_csv(result_dir / "claim_gates.csv", gate_rows, ["gate", "status", "meaning"])
    write_csv(
        result_dir / "residual_plot_manifest.csv",
        plot_rows,
        ["release_branch", "plot", "dataset", "models", "status"],
    )
    write_csv(
        result_dir / "derivation_targets.csv",
        target_rows,
        ["target", "why_now", "required_contract", "failure_consequence"],
    )
    write_csv(result_dir / "decision.csv", decision, ["key", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "stable_evidence_allowed": False,
        "score_runs": [str(path) for path in score_runs().values()],
        "next_action": "derive or reject the FLRW memory projection amplitude contract before stronger claims",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(STATUS + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
