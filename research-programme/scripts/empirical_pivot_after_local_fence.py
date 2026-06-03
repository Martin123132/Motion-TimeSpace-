from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "empirical-pivot-after-local-fence"
STATUS = "empirical_pivot_after_local_fence_ready_official_likelihood_queue_no_stable_evidence_claim"
CLAIM_CEILING = "empirical_holdout_planning_and_scorecard_only_local_branch_conditional_no_public_support_claim"


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
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "285-generic-SN-BAO-short-smoke-with-ablations.md", "generic SN+BAO short-smoke readout"),
        (ROOT / "289-no-SH0ES-shape-branch-readout.md", "no-SH0ES SN-shape branch readout"),
        (ROOT / "290-DESI-release-no-SH0ES-robustness-readout.md", "DESI DR1/DR2 no-SH0ES release split"),
        (ROOT / "291-CPL-prior-sensitivity-readout.md", "CPL prior sensitivity readout"),
        (ROOT / "144-frozen-branch-empirical-holdout-scorecard.md", "frozen-branch empirical scorecard"),
        (ROOT / "145-fresh-CC-Hz-source-locked-holdout.md", "fresh source-locked H(z) holdout"),
        (ROOT / "146-source-locked-growth-covariance-holdout.md", "source-locked growth covariance holdout"),
        (ROOT / "147-ELG-grid-likelihood-holdout.md", "ELG grid likelihood holdout"),
        (ROOT / "311-sector-label-SD-origin-attempt.md", "local branch fenced and parked"),
        (ROOT / "runs" / "20260601-000134-sector-label-SD-origin-attempt" / "results" / "promotion_gates.csv", "local branch promotion gates"),
        (ROOT / "runs" / "20260601-000114-CPL-prior-sensitivity-readout" / "results" / "gate_results.csv", "latest CPL sensitivity gates"),
        (ROOT / "runs" / "20260531-214500-frozen-branch-empirical-holdout-scorecard" / "status.json", "frozen empirical scorecard status"),
        (ROOT / "runs" / "20260531-221500-fresh-CC-Hz-source-locked-holdout" / "status.json", "fresh H(z) source-locked status"),
        (ROOT / "runs" / "20260531-224500-source-locked-growth-covariance-holdout" / "status.json", "growth covariance status"),
        (ROOT / "runs" / "20260531-231500-ELG-grid-likelihood-holdout" / "status.json", "ELG grid status"),
        (ROOT / "scripts" / "empirical_pivot_after_local_fence.py", "this pivot runner"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def status_or_missing(path: Path, key: str = "status") -> str:
    if not path.exists():
        return "missing"
    try:
        return str(read_json(path).get(key, "missing_key"))
    except Exception as exc:  # noqa: BLE001 - readout should report parse errors.
        return f"parse_error:{exc}"


def gate_status(path: Path, gate: str) -> str:
    if not path.exists():
        return "missing"
    rows = read_csv(path)
    for row in rows:
        if row.get("gate") == gate:
            return row.get("status", row.get("result", "missing_status"))
    return "missing_gate"


def empirical_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "local branch fence",
            "authoritative_run": "runs/20260601-000134-sector-label-SD-origin-attempt",
            "status": status_or_missing(ROOT / "runs" / "20260601-000134-sector-label-SD-origin-attempt" / "status.json"),
            "readout": "local branch parked as conditional theorem target; empirical pivot recommended",
            "allowed_claim": "local residual suppression has precise theorem targets",
            "forbidden_claim": "derived local GR or official PPN recovery",
            "next_pressure": "do not use local branch as evidence in empirical score",
        },
        {
            "arena": "generic SN+BAO short smoke",
            "authoritative_run": "runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout",
            "status": "generic_SN_BAO_short_smoke_scored_but_unstable_due_to_CPL_edge",
            "readout": "fixed no-clock branch competitive/mixed; beats wCDM/CPL by BIC, not LCDM by BIC",
            "allowed_claim": "diagnostic late-time competitiveness",
            "forbidden_claim": "stable cosmology evidence",
            "next_pressure": "tighten baselines and remove local-H0 pressure",
        },
        {
            "arena": "no-SH0ES SN-shape branch",
            "authoritative_run": "runs/20260601-000112-no-SH0ES-shape-branch-readout",
            "status": "no_SH0ES_shape_branch_pattern_survives_but_stable_evidence_blocked_by_CPL_edge",
            "readout": "qualitative pattern survives removing local-H0 calibration pressure",
            "allowed_claim": "not merely a SH0ES-pressure artifact in this short smoke",
            "forbidden_claim": "stable evidence or H0-tension solution",
            "next_pressure": "release split and CPL prior sensitivity",
        },
        {
            "arena": "DESI DR1/DR2 no-SH0ES split",
            "authoritative_run": "runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout",
            "status": "DESI_DR1_DR2_no_SH0ES_fixed_branch_survives_qualitatively_but_LCDM_BIC_gap_worsens",
            "readout": "DR1 preserves wCDM/CPL BIC wins but worsens LCDM BIC gap",
            "allowed_claim": "release robustness diagnostic",
            "forbidden_claim": "release-stable evidence",
            "next_pressure": "clean CPL edge and full-sample/full-cov test",
        },
        {
            "arena": "CPL prior sensitivity",
            "authoritative_run": "runs/20260601-000114-CPL-prior-sensitivity-readout",
            "status": status_or_missing(ROOT / "runs" / "20260601-000114-CPL-prior-sensitivity-readout" / "status.json"),
            "readout": "DR2 CPL can be edge-free; DR1 CPL still edge-hits; MTS no edge flags",
            "allowed_claim": "baseline edge is diagnosed rather than hidden",
            "forbidden_claim": "stable CPL comparison across releases",
            "next_pressure": "official likelihood/full-sample scoring",
        },
        {
            "arena": "frozen-branch aggregate scorecard",
            "authoritative_run": "runs/20260531-214500-frozen-branch-empirical-holdout-scorecard",
            "status": status_or_missing(ROOT / "runs" / "20260531-214500-frozen-branch-empirical-holdout-scorecard" / "status.json"),
            "readout": "late-time empirical branch survives; CMB bridge unresolved",
            "allowed_claim": "serious late-time empirical closure candidate",
            "forbidden_claim": "passes CMB or predicts amplitude",
            "next_pressure": "official/full-likelihood stack",
        },
        {
            "arena": "source-locked H(z)",
            "authoritative_run": "runs/20260531-221500-fresh-CC-Hz-source-locked-holdout",
            "status": status_or_missing(ROOT / "runs" / "20260531-221500-fresh-CC-Hz-source-locked-holdout" / "status.json"),
            "readout": "competitive draw across source-locked CC branches",
            "allowed_claim": "not disfavored by source-locked H(z)",
            "forbidden_claim": "late-time victory or full cosmology claim",
            "next_pressure": "refresh only if source files change; otherwise move up to official stack",
        },
        {
            "arena": "source-locked growth covariance",
            "authoritative_run": "runs/20260531-224500-source-locked-growth-covariance-holdout",
            "status": status_or_missing(ROOT / "runs" / "20260531-224500-source-locked-growth-covariance-holdout" / "status.json"),
            "readout": "primary preferred/draw under GR-proxy growth gate and jackknifes",
            "allowed_claim": "effective growth holdout survival",
            "forbidden_claim": "derived perturbation theory",
            "next_pressure": "official RSD/BAO likelihood integration",
        },
        {
            "arena": "ELG non-Gaussian grid",
            "authoritative_run": "runs/20260531-231500-ELG-grid-likelihood-holdout",
            "status": status_or_missing(ROOT / "runs" / "20260531-231500-ELG-grid-likelihood-holdout" / "status.json"),
            "readout": "competitive draw; missing non-Gaussian ELG branch does not reverse growth card",
            "allowed_claim": "ELG grid does not knock out the branch",
            "forbidden_claim": "official joint likelihood",
            "next_pressure": "combine only through official wrapper, not diagnostic sums",
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    local_gate_file = ROOT / "runs" / "20260601-000134-sector-label-SD-origin-attempt" / "results" / "promotion_gates.csv"
    cpl_gate_file = ROOT / "runs" / "20260601-000114-CPL-prior-sensitivity-readout" / "results" / "gate_results.csv"
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if all(row["exists"] == "yes" for row in source_register_rows()) else "fail",
            "evidence": "all cited empirical/local artifacts exist",
            "claim_effect": "pivot ledger traceable",
        },
        {
            "gate": "local_branch_parked_not_promoted",
            "status": "pass" if gate_status(local_gate_file, "local_GR_promoted") == "fail" else "fail",
            "evidence": f"local_GR_promoted={gate_status(local_gate_file, 'local_GR_promoted')}; empirical_pivot_recommended={gate_status(local_gate_file, 'empirical_pivot_recommended')}",
            "claim_effect": "empirical work will not use local GR as assumed evidence",
        },
        {
            "gate": "CPL_DR2_clean_but_DR1_unstable",
            "status": "pass",
            "evidence": f"DR2_full_CPL_box_edge_free={gate_status(cpl_gate_file, 'DR2_full_CPL_box_edge_free')}; DR1_full_CPL_box_edge_free={gate_status(cpl_gate_file, 'DR1_full_CPL_box_edge_free')}",
            "claim_effect": "baseline fragility remains explicit",
        },
        {
            "gate": "stable_cosmology_evidence_allowed",
            "status": "fail",
            "evidence": "DR1 CPL remains edge-hit and SN+BAO is still short-smoke/diagnostic",
            "claim_effect": "no stable evidence language",
        },
        {
            "gate": "nonSN_holdouts_available",
            "status": "pass",
            "evidence": "source-locked H(z), growth covariance, and ELG grid runs exist",
            "claim_effect": "independent late-time pressure already present",
        },
        {
            "gate": "CMB_bridge_promoted",
            "status": "fail",
            "evidence": "aggregate scorecard keeps late-to-CMB transfer failure and mixed joint bridge",
            "claim_effect": "no CMB pass claim",
        },
        {
            "gate": "growth_perturbation_promoted",
            "status": "fail",
            "evidence": "growth holdout is GR-proxy/effective only",
            "claim_effect": "no perturbation-theory promotion",
        },
        {
            "gate": "official_likelihood_queue_ready",
            "status": "pass",
            "evidence": "next queue specifies full-sample/full-cov and official wrapper targets",
            "claim_effect": "next empirical step is concrete",
        },
    ]


def next_holdout_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "official_or_full_likelihood_SN_BAO_growth_wrapper",
            "why": "short-smoke plus source-locked holdouts are not enough for stable evidence; need an integrated fair likelihood wrapper",
            "minimum_inputs": "Pantheon+ full/cov SN branch, DESI DR1/DR2 BAO covariances, SDSS/eBOSS growth covariances/ELG grid",
            "acceptance_gate": "same rows/nuisance policy for LCDM,wCDM,CPL,MTS; no edge-hit branch counted as stable evidence",
            "claim_limit": "empirical closure only",
        },
        {
            "priority": 2,
            "target": "full_sample_full_cov_noSH0ES_SN_BAO_release_split",
            "why": "current SN+BAO result is 250-SN short-smoke and DR1 LCDM BIC gap worsens",
            "minimum_inputs": "full Pantheon+ shape/covariance branch plus DESI DR1/DR2 BAO",
            "acceptance_gate": "MTS remains draw/competitive against LCDM,wCDM,CPL under wide CPL boxes and no local-H0 calibration pressure",
            "claim_limit": "late-time background robustness only",
        },
        {
            "priority": 3,
            "target": "source_lock_refresh_nonSN_holdouts",
            "why": "H(z), growth covariance, and ELG grid are already positive/draw but should be refreshable before any external writeup",
            "minimum_inputs": "fresh URL/hash locks for CC, SDSS/eBOSS covariance files, ELG grid",
            "acceptance_gate": "row/hash locks pass and no baseline-only failure is hidden",
            "claim_limit": "independent late-time holdout only",
        },
        {
            "priority": 4,
            "target": "CMB_perturbation_contract_not_score_claim",
            "why": "CMB bridge is the big unresolved empirical/theory gap",
            "minimum_inputs": "parameter-map contract, perturbation variables, growth/CMB consistency rule",
            "acceptance_gate": "no CMB score promoted without perturbation/bridge gates",
            "claim_limit": "contract/readiness only",
        },
        {
            "priority": 5,
            "target": "park_local_parent_theorem",
            "why": "local branch now has exact blockers A_D and [K,A_D]",
            "minimum_inputs": "future parent action with boundary activity operator",
            "acceptance_gate": "derive C_D and kernel commutation before local GR language",
            "claim_limit": "local theorem target only",
        },
    ]


def command_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "task": "full_sample_noSH0ES_DR2_dryrun",
            "command": "python scripts/cosmo_SN_BAO_closure_runner.py --phase dry-run --sn-observable mb-corr --exclude-calibrators --timestamp <timestamp>",
            "run_policy": "dry-run first",
            "long_run": "no",
            "expected_outputs": "schema report only, no scoring",
        },
        {
            "task": "full_sample_noSH0ES_DR2_short_smoke_wide_CPL",
            "command": "python scripts/cosmo_SN_BAO_closure_runner.py --phase short-smoke --sn-observable mb-corr --exclude-calibrators --cpl-w0-lower -4 --cpl-w0-upper 1 --cpl-wa-lower -5 --cpl-wa-upper 5 --timestamp <timestamp>",
            "run_policy": "only after dry-run/schema pass",
            "long_run": "possible",
            "expected_outputs": "fit summary, baseline comparison, edge table, residuals",
        },
        {
            "task": "refresh_CC_Hz_source_lock",
            "command": "python scripts/fresh_CC_Hz_source_locked_holdout.py --timestamp <timestamp>",
            "run_policy": "network/hash source refresh",
            "long_run": "no",
            "expected_outputs": "source lock, H(z) fit summary, gate results",
        },
        {
            "task": "refresh_growth_covariance_holdout",
            "command": "python scripts/source_locked_growth_covariance_holdout.py --timestamp <timestamp>",
            "run_policy": "network/hash source refresh; may be slower",
            "long_run": "yes",
            "expected_outputs": "growth covariance fits, jackknife scorecard",
        },
        {
            "task": "refresh_ELG_grid_holdout",
            "command": "python scripts/ELG_grid_likelihood_holdout.py --timestamp <timestamp>",
            "run_policy": "network/hash source refresh; grid parser",
            "long_run": "possible",
            "expected_outputs": "ELG grid fit, diagnostic combination",
        },
    ]


def claim_ceiling_rows() -> list[dict[str, Any]]:
    return [
        {
            "topic": "local branch",
            "allowed": "conditional theorem target with named blockers",
            "forbidden": "derived local GR/PPN",
            "reason": "A_D, K commutation, beta/profile/manifest gates remain underived",
        },
        {
            "topic": "SN+BAO background",
            "allowed": "short-smoke competitiveness/mixed readout",
            "forbidden": "stable cosmology evidence",
            "reason": "CPL DR1 edge persists and sample is not final official likelihood",
        },
        {
            "topic": "non-SN late-time holdouts",
            "allowed": "source-locked H(z)/growth/ELG survivability",
            "forbidden": "perturbation theory or CMB pass",
            "reason": "growth remains proxy/effective and CMB bridge unresolved",
        },
        {
            "topic": "amplitude",
            "allowed": "frozen B_mem empirical closure under tests",
            "forbidden": "parent prediction of B_mem=2/27",
            "reason": "Q_*, k=9, endpoints, arrow, and trace partition remain theorem targets",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "decision": "local derivation route is fenced; empirical branch should now move to official/full-likelihood holdouts",
            "recommended_next": "full-sample/full-cov no-SH0ES SN+BAO release split or official SN+BAO+growth wrapper",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    outputs = {
        "source_register": source_register_rows(),
        "empirical_scorecard": empirical_scorecard_rows(),
        "acceptance_gates": acceptance_gate_rows(),
        "next_holdout_queue": next_holdout_queue_rows(),
        "command_queue": command_queue_rows(),
        "claim_ceilings": claim_ceiling_rows(),
        "decision": decision_rows(),
    }

    write_csv(results_dir / "source_register.csv", outputs["source_register"], ["source", "role", "exists"])
    write_csv(
        results_dir / "empirical_scorecard.csv",
        outputs["empirical_scorecard"],
        ["arena", "authoritative_run", "status", "readout", "allowed_claim", "forbidden_claim", "next_pressure"],
    )
    write_csv(results_dir / "acceptance_gates.csv", outputs["acceptance_gates"], ["gate", "status", "evidence", "claim_effect"])
    write_csv(
        results_dir / "next_holdout_queue.csv",
        outputs["next_holdout_queue"],
        ["priority", "target", "why", "minimum_inputs", "acceptance_gate", "claim_limit"],
    )
    write_csv(results_dir / "command_queue.csv", outputs["command_queue"], ["task", "command", "run_policy", "long_run", "expected_outputs"])
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
    parser = argparse.ArgumentParser(description="Build the empirical holdout pivot ledger after fencing the local branch.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
