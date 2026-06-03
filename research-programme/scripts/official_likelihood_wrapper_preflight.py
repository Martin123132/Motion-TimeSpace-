from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKBENCH = ROOT.parent / "formalization-workbench"
RUN_SLUG = "official-likelihood-wrapper-preflight"
STATUS = "official_likelihood_wrapper_preflight_ready_dryrun_first_no_scores_or_claims"
CLAIM_CEILING = "preflight_and_wrapper_contract_only_no_stable_evidence_or_theory_promotion"


DATA = WORKBENCH / "data" / "cosmology"
PANTHEON = DATA / "pantheon_plus"
DESI_DR2 = DATA / "desi_dr2_bao"
DESI_DR1 = DATA / "desi_dr1_bao"
CC = DATA / "cosmic_chronometers"
GROWTH = DATA / "growth_CMB"
SDSS = GROWTH / "sdss_eboss_dr16"


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


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def file_line_count(path: Path) -> int | str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            return sum(1 for _ in handle)
    except Exception:  # noqa: BLE001 - binary-ish files can report unknown line count.
        return ""


def file_status(path: Path) -> str:
    return "present" if path.exists() else "missing"


def status_or_missing(path: Path, key: str = "status") -> str:
    if not path.exists():
        return "missing"
    try:
        return str(read_json(path).get(key, "missing_key"))
    except Exception as exc:  # noqa: BLE001 - preflight reports parse errors.
        return f"parse_error:{exc}"


def latest_run_status(run_suffix: str, key: str = "status") -> str:
    matches = sorted((ROOT / "runs").glob(f"*-{run_suffix}"))
    if not matches:
        return "missing"
    latest = matches[-1]
    status = status_or_missing(latest / "status.json", key)
    return f"{status} ({relpath(latest)})"


def latest_run_status_path(run_suffix: str) -> Path | None:
    matches = sorted((ROOT / "runs").glob(f"*-{run_suffix}"))
    if not matches:
        return None
    return matches[-1] / "status.json"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "312-empirical-pivot-after-local-fence.md", "empirical pivot and wrapper target"),
        (ROOT / "329-source-locked-growth-after-projector-fence.md", "post-projector growth refresh checkpoint"),
        (ROOT / "170-no-clock-official-source-refresh-runner.md", "official/source refresh preflight checkpoint"),
        (ROOT / "145-fresh-CC-Hz-source-locked-holdout.md", "source-locked H(z) checkpoint"),
        (ROOT / "146-source-locked-growth-covariance-holdout.md", "growth covariance checkpoint"),
        (ROOT / "147-ELG-grid-likelihood-holdout.md", "ELG grid checkpoint"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "SN+BAO dry-run/short-smoke runner"),
        (ROOT / "scripts" / "fresh_CC_Hz_source_locked_holdout.py", "H(z) source-lock runner"),
        (ROOT / "scripts" / "source_locked_growth_covariance_holdout.py", "growth covariance source-lock runner"),
        (ROOT / "scripts" / "ELG_grid_likelihood_holdout.py", "ELG grid likelihood runner"),
        (ROOT / "scripts" / "no_clock_official_source_refresh.py", "official source refresh runner"),
        (ROOT / "runs" / "20260531-235959-no-clock-official-source-refresh" / "status.json", "official source refresh status"),
        (ROOT / "runs" / "20260601-000135-empirical-pivot-after-local-fence" / "status.json", "empirical pivot status"),
        (latest_run_status_path("source-locked-growth-covariance-holdout") or ROOT / "runs" / "missing-latest-growth" / "status.json", "latest source-locked growth status"),
        (ROOT / "scripts" / "official_likelihood_wrapper_preflight.py", "this preflight runner"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def data_asset_rows() -> list[dict[str, Any]]:
    assets = [
        ("SN", "Pantheon+SH0ES data", PANTHEON / "Pantheon+SH0ES.dat", "full/full-cov and no-SH0ES shape branch"),
        ("SN", "Pantheon+ full covariance", PANTHEON / "Pantheon+SH0ES_STAT+SYS.cov", "full covariance scoring"),
        ("SN", "Pantheon+ stat-only covariance", PANTHEON / "Pantheon+SH0ES_STATONLY.cov", "sensitivity/diagnostic covariance"),
        ("BAO", "DESI DR2 mean", DESI_DR2 / "desi_gaussian_bao_ALL_GCcomb_mean.txt", "primary BAO release"),
        ("BAO", "DESI DR2 covariance", DESI_DR2 / "desi_gaussian_bao_ALL_GCcomb_cov.txt", "primary BAO covariance"),
        ("BAO", "DESI DR1 mean", DESI_DR1 / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt", "release split"),
        ("BAO", "DESI DR1 covariance", DESI_DR1 / "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt", "release split covariance"),
        ("H_z", "CC32 source table", CC / "data_CC_unibo_raw.dat", "diagonal sensitivity"),
        ("H_z", "CC15 BC03 covariance-branch rows", CC / "covariance_branch" / "Hz_CC_Moresco15_BC03.csv", "primary source-locked H(z) branch"),
        ("H_z", "CC15 suggested covariance", CC / "covariance_branch" / "covariance_suggested.csv", "primary H(z) covariance"),
        ("growth", "SDSS/eBOSS source manifest", GROWTH / "source_manifest.csv", "source hash and URL manifest"),
        ("growth", "SDSS BAO-plus LRG vector", SDSS / "BAO-plus" / "sdss_DR16_LRG_FSBAO_DMDHfs8.txt", "growth covariance branch"),
        ("growth", "SDSS BAO-plus LRG covariance", SDSS / "BAO-plus" / "sdss_DR16_LRG_FSBAO_DMDHfs8_covtot.txt", "growth covariance branch"),
        ("growth", "ELG grid likelihood", SDSS / "BAO-plus" / "sdss_DR16_ELG_FSBAO_DMDHfs8gridlikelihood.txt", "non-Gaussian ELG branch"),
        ("CMB", "Planck 2018 distance-prior vector", GROWTH / "planck2018_distance_priors" / "planck2018_distance_prior_vector.csv", "CMB bridge diagnostic only"),
        ("CMB", "Planck 2018 distance-prior covariance", GROWTH / "planck2018_distance_priors" / "planck2018_distance_prior_covariance.csv", "CMB bridge diagnostic only"),
    ]
    return [
        {
            "sector": sector,
            "asset": name,
            "path": str(path),
            "status": file_status(path),
            "bytes": path.stat().st_size if path.exists() and path.is_file() else "",
            "line_count": file_line_count(path),
            "role": role,
        }
        for sector, name, path, role in assets
    ]


def wrapper_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "component": "SN_full_cov_noSH0ES",
            "source_runner": "scripts/cosmo_SN_BAO_closure_runner.py",
            "current_status": "runner supports --sn-covariance-mode full, --sn-max-rows 0, mb-corr, calibrators excluded by default",
            "next_action": "dry-run full Pantheon+ shape/cov branch against DESI DR2 and DR1",
            "claim_limit": "late-time background only",
        },
        {
            "component": "DESI_DR1_DR2_BAO_release_split",
            "source_runner": "scripts/cosmo_SN_BAO_closure_runner.py",
            "current_status": "DR1/DR2 mean and covariance files present",
            "next_action": "score both releases with identical model/nuisance policy and wide CPL priors",
            "claim_limit": "release robustness only",
        },
        {
            "component": "CC_Hz_source_lock",
            "source_runner": "scripts/fresh_CC_Hz_source_locked_holdout.py",
            "current_status": latest_run_status("fresh-CC-Hz-source-locked-holdout"),
            "next_action": "refresh only if external source lock is needed for writeup",
            "claim_limit": "independent H(z) holdout only",
        },
        {
            "component": "growth_covariance_source_lock",
            "source_runner": "scripts/source_locked_growth_covariance_holdout.py",
            "current_status": latest_run_status("source-locked-growth-covariance-holdout"),
            "next_action": "integrate results into wrapper without treating GR-proxy growth as perturbation theory",
            "claim_limit": "effective growth holdout only",
        },
        {
            "component": "ELG_grid_nonGaussian",
            "source_runner": "scripts/ELG_grid_likelihood_holdout.py",
            "current_status": latest_run_status("ELG-grid-likelihood-holdout"),
            "next_action": "include as separate grid-likelihood branch, not a Gaussian covariance shortcut",
            "claim_limit": "ELG branch only; no official joint claim",
        },
        {
            "component": "CMB_bridge_contract",
            "source_runner": "scripts/official_CMB_perturbation_contract.py",
            "current_status": "contract/readiness only; bridge unresolved",
            "next_action": "keep CMB outside support claim until perturbation/parameter map gates close",
            "claim_limit": "no CMB pass claim",
        },
    ]


def model_baseline_rows() -> list[dict[str, Any]]:
    return [
        {"model": "LCDM", "role": "baseline", "free_nuisance": "same SN offset/calibration and sigma8 treatment where applicable", "edge_policy": "report edges; no edge-based evidence"},
        {"model": "wCDM", "role": "baseline", "free_nuisance": "same rows and nuisance policy", "edge_policy": "report edges; no edge-based evidence"},
        {"model": "CPL", "role": "flexible_baseline", "free_nuisance": "wide w0/wa boxes and edge reporting", "edge_policy": "DR1 edge instability blocks stable evidence"},
        {"model": "MTS_fixed_2over27_no_clock", "role": "primary_closure", "free_nuisance": "B_mem fixed; no local branch promotion; same background nuisance", "edge_policy": "any MTS edge blocks claim"},
        {"model": "MTS_Bmem_zero", "role": "negative_control", "free_nuisance": "must reproduce LCDM limit", "edge_policy": "control failure blocks scoring"},
        {"model": "MTS_fitted_p_or_u3", "role": "ablation_only", "free_nuisance": "not promotable unless AIC/BIC tax wins across splits", "edge_policy": "diagnostic only"},
    ]


def likelihood_run_graph_rows() -> list[dict[str, Any]]:
    return [
        {
            "phase": 1,
            "name": "source_and_schema_preflight",
            "action": "verify files, hashes/row locks where available, covariance shapes, model matrix, nuisance policy",
            "must_complete_before": "any score",
            "long_run_policy": "safe and cheap",
        },
        {
            "phase": 2,
            "name": "SN_BAO_full_cov_noSH0ES_release_split",
            "action": "run full selected Pantheon+ no-SH0ES with DESI DR2 and DR1 under wide CPL priors",
            "must_complete_before": "wrapper scorecard",
            "long_run_policy": "run from VS Code terminal and wait for COMPLETE marker",
        },
        {
            "phase": 3,
            "name": "nonSN_source_locked_refresh_optional",
            "action": "refresh H(z), growth covariance, and ELG grid only if source-lock update is required",
            "must_complete_before": "external writeup, not required for immediate preflight",
            "long_run_policy": "growth/ELG may be long; no token-watching",
        },
        {
            "phase": 4,
            "name": "component_scorecard_aggregation",
            "action": "aggregate SN+BAO, H(z), growth, ELG with claim ceilings and no diagnostic over-combination",
            "must_complete_before": "any evidence language",
            "long_run_policy": "readout only",
        },
        {
            "phase": 5,
            "name": "CMB_bridge_contract",
            "action": "keep CMB as unresolved contract until perturbation and parameter-map gates pass",
            "must_complete_before": "CMB claim",
            "long_run_policy": "contract/readiness only",
        },
    ]


def dryrun_command_rows() -> list[dict[str, Any]]:
    sn_data = PANTHEON / "Pantheon+SH0ES.dat"
    sn_cov = PANTHEON / "Pantheon+SH0ES_STAT+SYS.cov"
    dr2_mean = DESI_DR2 / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
    dr2_cov = DESI_DR2 / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
    dr1_mean = DESI_DR1 / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt"
    dr1_cov = DESI_DR1 / "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt"
    base = "python scripts/cosmo_SN_BAO_closure_runner.py"
    common = f"--sn-data \"{sn_data}\" --sn-cov \"{sn_cov}\" --sn-covariance-mode full --sn-observable mb-corr --sn-max-rows 0"
    cpl = "--cpl-w0-lower -4 --cpl-w0-upper 1 --cpl-wa-lower -5 --cpl-wa-upper 5"
    return [
        {
            "task": "DR2_fullcov_noSH0ES_dryrun",
            "command": f"{base} --phase dry-run {common} --bao-data \"{dr2_mean}\" --bao-cov \"{dr2_cov}\" --bao-label DESI_DR2_fullcov_noSH0ES --timestamp <timestamp>",
            "run_policy": "dry-run first; no scores",
            "notes": "no --exclude-calibrators flag: calibrators are excluded by default unless --include-calibrators is set",
        },
        {
            "task": "DR1_fullcov_noSH0ES_dryrun",
            "command": f"{base} --phase dry-run {common} --bao-data \"{dr1_mean}\" --bao-cov \"{dr1_cov}\" --bao-label DESI_DR1_fullcov_noSH0ES --timestamp <timestamp>",
            "run_policy": "dry-run first; no scores",
            "notes": "release split must use same SN rows/nuisance policy",
        },
        {
            "task": "DR2_fullcov_noSH0ES_score",
            "command": f"{base} --phase short-smoke {common} --bao-data \"{dr2_mean}\" --bao-cov \"{dr2_cov}\" --bao-label DESI_DR2_fullcov_noSH0ES {cpl} --timestamp <timestamp> --max-iter 180",
            "run_policy": "only after DR2 dry-run pass",
            "notes": "may be long; run from VS Code and wait for completion marker",
        },
        {
            "task": "DR1_fullcov_noSH0ES_score",
            "command": f"{base} --phase short-smoke {common} --bao-data \"{dr1_mean}\" --bao-cov \"{dr1_cov}\" --bao-label DESI_DR1_fullcov_noSH0ES {cpl} --timestamp <timestamp> --max-iter 180",
            "run_policy": "only after DR1 dry-run pass",
            "notes": "may be long; run from VS Code and wait for completion marker",
        },
        {
            "task": "growth_ELG_refresh_optional",
            "command": "python scripts/source_locked_growth_covariance_holdout.py --timestamp <timestamp>; python scripts/ELG_grid_likelihood_holdout.py --timestamp <timestamp>",
            "run_policy": "optional refresh before external writeup",
            "notes": "do not combine diagnostic sums as official joint likelihood",
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_register_rows())
    assets = data_asset_rows()
    missing_assets = [row["asset"] for row in assets if row["status"] != "present"]
    source_refresh_status_path = latest_run_status_path("no-clock-official-source-refresh")
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": "all wrapper source/checkpoint paths exist" if sources_ok else ";".join(row["source"] for row in source_register_rows() if row["exists"] != "yes"),
            "claim_effect": "preflight traceable",
        },
        {
            "gate": "data_assets_present",
            "status": "pass" if not missing_assets else "fail",
            "evidence": "all required local data assets present" if not missing_assets else ";".join(missing_assets),
            "claim_effect": "wrapper can proceed to dry-run",
        },
        {
            "gate": "official_source_refresh_available",
            "status": "pass" if source_refresh_status_path and source_refresh_status_path.exists() else "fail",
            "evidence": status_or_missing(source_refresh_status_path) if source_refresh_status_path else "missing",
            "claim_effect": "source/manifest guard exists",
        },
        {
            "gate": "dryrun_commands_corrected",
            "status": "pass",
            "evidence": "commands use default calibrator exclusion and do not include nonexistent --exclude-calibrators flag",
            "claim_effect": "next run commands are executable in current CLI",
        },
        {
            "gate": "baseline_parity_defined",
            "status": "pass",
            "evidence": "LCDM/wCDM/CPL/MTS fixed/MTS zero controls listed with same nuisance policy",
            "claim_effect": "MTS and baselines face the same judges",
        },
        {
            "gate": "wrapper_scores_executed",
            "status": "fail",
            "evidence": "this checkpoint is preflight/contract only",
            "claim_effect": "no new evidence claim",
        },
        {
            "gate": "stable_evidence_allowed",
            "status": "fail",
            "evidence": "full-cov release split has not been executed and CMB/perturbation bridge remains unresolved",
            "claim_effect": "no stable cosmology evidence language",
        },
        {
            "gate": "long_run_policy_written",
            "status": "pass",
            "evidence": "VS Code/COMPLETE-marker policy in run graph and commands",
            "claim_effect": "future long jobs do not waste token budget",
        },
    ]


def claim_ceiling_rows() -> list[dict[str, Any]]:
    return [
        {
            "topic": "wrapper preflight",
            "allowed": "ready for dry-run/schema verification",
            "forbidden": "new score or evidence",
            "reason": "no scoring executed in this checkpoint",
        },
        {
            "topic": "SN+BAO full-cov release split",
            "allowed": "future late-time background robustness if run passes",
            "forbidden": "current stable evidence claim",
            "reason": "full-cov release split still queued",
        },
        {
            "topic": "growth/ELG",
            "allowed": "source-locked holdout components",
            "forbidden": "official joint likelihood or perturbation theory",
            "reason": "growth remains proxy/effective and ELG combination is diagnostic",
        },
        {
            "topic": "CMB",
            "allowed": "contract/readiness only",
            "forbidden": "CMB pass",
            "reason": "bridge and perturbation map unresolved",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "decision": "official/full-likelihood-style wrapper preflight is ready for dry-run, but no scores were executed",
            "recommended_next": "run DR2 and DR1 full-cov no-SH0ES dry-runs from VS Code; score only after schema gates pass",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    outputs = {
        "source_register": source_register_rows(),
        "data_asset_inventory": data_asset_rows(),
        "wrapper_components": wrapper_component_rows(),
        "model_baseline_matrix": model_baseline_rows(),
        "likelihood_run_graph": likelihood_run_graph_rows(),
        "dryrun_command_queue": dryrun_command_rows(),
        "acceptance_gates": acceptance_gate_rows(),
        "claim_ceilings": claim_ceiling_rows(),
        "decision": decision_rows(),
    }

    write_csv(results_dir / "source_register.csv", outputs["source_register"], ["source", "role", "exists"])
    write_csv(results_dir / "data_asset_inventory.csv", outputs["data_asset_inventory"], ["sector", "asset", "path", "status", "bytes", "line_count", "role"])
    write_csv(results_dir / "wrapper_components.csv", outputs["wrapper_components"], ["component", "source_runner", "current_status", "next_action", "claim_limit"])
    write_csv(results_dir / "model_baseline_matrix.csv", outputs["model_baseline_matrix"], ["model", "role", "free_nuisance", "edge_policy"])
    write_csv(results_dir / "likelihood_run_graph.csv", outputs["likelihood_run_graph"], ["phase", "name", "action", "must_complete_before", "long_run_policy"])
    write_csv(results_dir / "dryrun_command_queue.csv", outputs["dryrun_command_queue"], ["task", "command", "run_policy", "notes"])
    write_csv(results_dir / "acceptance_gates.csv", outputs["acceptance_gates"], ["gate", "status", "evidence", "claim_effect"])
    write_csv(results_dir / "claim_ceilings.csv", outputs["claim_ceilings"], ["topic", "allowed", "forbidden", "reason"])
    write_csv(results_dir / "decision.csv", outputs["decision"], ["status", "claim_ceiling", "decision", "recommended_next"])

    payload = {
        "run_slug": RUN_SLUG,
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": relpath(run_dir),
        "outputs": {name: len(rows) for name, rows in outputs.items()},
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Build preflight contract for the official/full-likelihood-style empirical wrapper.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
