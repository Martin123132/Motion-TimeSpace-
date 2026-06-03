#!/usr/bin/env python3
"""Checkpoint 190: matched mock CMB likelihood proxy or derivation pivot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_190_NAME = "CMB-matched-mock-likelihood-or-derivation-pivot"
CHECKPOINT_189_RUN = RUNS_ROOT / "20260601-000006-CMB-profiled-shape-residual-and-likelihood-readiness"
CHECKPOINT_188_RUN = RUNS_ROOT / "20260601-000005-CMB-theta-compensation-theorem-or-profiled-fit-gate"
CHECKPOINT_187_RUN = RUNS_ROOT / "20260601-000004-CAMB-density-convention-and-locked-transfer-theta-gate"

STATUS = "CMB_matched_mock_likelihood_proxy_same_density_competitive_locked_branch_pivot_to_derivation"
CLAIM_CEILING = "mock_likelihood_proxy_only_no_official_CMB_likelihood_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

RESIDUALS = CHECKPOINT_189_RUN / "results" / "extended_spectra_residuals_vs_control.csv"
BRANCH_SUMMARY = CHECKPOINT_189_RUN / "results" / "extended_branch_run_summary.csv"
SHAPE_SUMMARY = CHECKPOINT_189_RUN / "results" / "shape_residual_band_summary.csv"
READINESS = CHECKPOINT_189_RUN / "results" / "likelihood_readiness_matrix.csv"
H0_PROFILE = CHECKPOINT_188_RUN / "results" / "H0_profile_results.csv"

BANDS = [
    ("low_ell_2_29", 2, 29),
    ("acoustic_30_200", 30, 200),
    ("extended_201_1000", 201, 1000),
    ("all_2_1000", 2, 1000),
]
DATA_VECTORS = [
    ("TT", ["TT_cv_z_proxy"]),
    ("EE", ["EE_cv_z_proxy"]),
    ("TT_plus_EE", ["TT_cv_z_proxy", "EE_cv_z_proxy"]),
]
BASELINE_MODELS = [
    ("LCDM_profiled_control", 0, "nested/synthetic control", "chi2=0 by construction"),
    ("wCDM_nested_control", 1, "baseline comparator", "can reduce to LCDM at w=-1; extra parameter penalized"),
    ("CPL_nested_control", 2, "baseline comparator", "can reduce to LCDM at w0=-1,wa=0; two extra parameters penalized"),
]
MTS_BRANCHES = {
    "same_physical_densities_MTS_high_cs_fluid_H0_profiled": {
        "arena": "same_physical_densities",
        "model": "MTS_high_cs_fixed_profiled",
        "k_extra": 0,
        "readout": "competitive_proxy_after_theta_profile",
    },
    "locked_Omega_m_neutrino_subtracted_MTS_high_cs_fluid_H0_profiled": {
        "arena": "locked_Omega_m_neutrino_subtracted",
        "model": "MTS_high_cs_fixed_profiled",
        "k_extra": 0,
        "readout": "pressure_branch_after_theta_profile",
    },
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 190 matched mock likelihood script"),
        (WORK_DIR / "189-CMB-profiled-shape-residual-and-likelihood-readiness.md", "profiled shape residual checkpoint"),
        (CHECKPOINT_189_RUN / "status.json", "checkpoint 189 machine status"),
        (RESIDUALS, "checkpoint 189 extended residuals"),
        (BRANCH_SUMMARY, "checkpoint 189 branch summary"),
        (SHAPE_SUMMARY, "checkpoint 189 band summary"),
        (READINESS, "checkpoint 189 readiness matrix"),
        (WORK_DIR / "188-CMB-theta-compensation-theorem-or-profiled-fit-gate.md", "theta profile checkpoint"),
        (CHECKPOINT_188_RUN / "status.json", "checkpoint 188 machine status"),
        (H0_PROFILE, "checkpoint 188 H0 profile results"),
        (WORK_DIR / "187-CAMB-density-convention-and-locked-transfer-theta-gate.md", "locked theta gate checkpoint"),
        (CHECKPOINT_187_RUN / "status.json", "checkpoint 187 machine status"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def mock_likelihood_definition_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "synthetic data",
            "definition": "matched profiled LCDM control spectrum in each arena",
            "reason": "tests shape pressure under equal rules without claiming Planck likelihood",
            "limitation": "not real CMB data",
        },
        {
            "item": "covariance proxy",
            "definition": "independent cosmic-variance fractional sigma sqrt(2/(2ell+1)) for TT and EE",
            "reason": "quick pressure gauge for residual magnitude",
            "limitation": "ignores TT/TE/EE covariance, lensing likelihood, noise, masks, foregrounds, calibration, beams",
        },
        {
            "item": "TE treatment",
            "definition": "reported as residual diagnostics in checkpoint 189, excluded from mock chi2",
            "reason": "fractional TE residuals are unstable near zero crossings without full covariance",
            "limitation": "official likelihood must include TE correctly",
        },
        {
            "item": "shared H0/theta profile",
            "definition": "H0/theta profiling treated as common nuisance freedom for LCDM/wCDM/CPL/MTS",
            "reason": "prevents asymmetric guilty-until-proven-innocent scoring",
            "limitation": "does not derive theta compensation",
        },
        {
            "item": "model penalties",
            "definition": "AIC/BIC use only model-specific extra parameters beyond the shared profile",
            "reason": "wCDM and CPL nested controls get fair penalties; fixed MTS keeps B,p,u locked",
            "limitation": "if B,p,u are later freed, MTS must be re-penalized",
        },
    ]


def model_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "LCDM_profiled_control",
            "shared_profile": "H0/theta",
            "extra_parameters_counted": 0,
            "score_role": "synthetic-data control",
            "rule": "chi2=0 by construction in each arena",
        },
        {
            "model": "wCDM_nested_control",
            "shared_profile": "H0/theta",
            "extra_parameters_counted": 1,
            "score_role": "baseline flexibility comparator",
            "rule": "nested at w=-1, so chi2=0 plus AIC/BIC penalty",
        },
        {
            "model": "CPL_nested_control",
            "shared_profile": "H0/theta",
            "extra_parameters_counted": 2,
            "score_role": "baseline flexibility comparator",
            "rule": "nested at w0=-1, wa=0, so chi2=0 plus AIC/BIC penalty",
        },
        {
            "model": "MTS_high_cs_fixed_profiled",
            "shared_profile": "H0/theta",
            "extra_parameters_counted": 0,
            "score_role": "fixed MTS branch",
            "rule": "B_mem=2/27, p=3, u3=1/4, cs2=1 fixed; H0 profile not counted because baselines receive same freedom",
        },
        {
            "model": "MTS_if_Bpu_freed_later",
            "shared_profile": "H0/theta",
            "extra_parameters_counted": 3,
            "score_role": "future warning row",
            "rule": "if B_mem,p,u3 are fitted to CMB, add penalties and demote fixed-branch evidence",
        },
    ]


def rows_for_branch(residual_rows: list[dict[str, str]], branch: str, ell_min: int, ell_max: int) -> list[dict[str, str]]:
    return [row for row in residual_rows if row["branch"] == branch and ell_min <= int(row["ell"]) <= ell_max]


def chi2_for(rows: list[dict[str, str]], z_columns: list[str]) -> float:
    total = 0.0
    for row in rows:
        for column in z_columns:
            value = float(row[column])
            if math.isfinite(value):
                total += value * value
    return total


def score_row(
    arena: str,
    model: str,
    band: str,
    data_vector: str,
    chi2: float,
    k_extra: int,
    n_data: int,
    role: str,
    readout: str,
) -> dict[str, Any]:
    aic = chi2 + 2.0 * k_extra
    bic = chi2 + k_extra * math.log(max(n_data, 1))
    return {
        "arena": arena,
        "model": model,
        "band": band,
        "data_vector": data_vector,
        "chi2_proxy": chi2,
        "k_extra": k_extra,
        "n_data": n_data,
        "AIC_proxy": aic,
        "BIC_proxy": bic,
        "delta_AIC_vs_LCDM": aic,
        "delta_BIC_vs_LCDM": bic,
        "role": role,
        "readout": readout,
        "claim_limit": "mock proxy only; no official likelihood",
    }


def scorecard_rows(residual_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    arenas = sorted({info["arena"] for info in MTS_BRANCHES.values()})
    for arena in arenas:
        for band, ell_min, ell_max in BANDS:
            n_ell = ell_max - ell_min + 1
            for data_vector, z_columns in DATA_VECTORS:
                n_data = n_ell * len(z_columns)
                for baseline_model, k_extra, role, readout in BASELINE_MODELS:
                    rows.append(score_row(arena, baseline_model, band, data_vector, 0.0, k_extra, n_data, role, readout))
                for branch, info in MTS_BRANCHES.items():
                    if info["arena"] != arena:
                        continue
                    selected = rows_for_branch(residual_rows, branch, ell_min, ell_max)
                    chi2 = chi2_for(selected, z_columns)
                    rows.append(
                        score_row(
                            arena,
                            info["model"],
                            band,
                            data_vector,
                            chi2,
                            int(info["k_extra"]),
                            n_data,
                            "fixed MTS branch",
                            info["readout"],
                        )
                    )
    return rows


def decision_snapshot_rows(score_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    snapshots: list[dict[str, Any]] = []
    for arena in sorted({row["arena"] for row in score_rows}):
        for data_vector in ["TT", "EE", "TT_plus_EE"]:
            mts = next(
                row
                for row in score_rows
                if row["arena"] == arena
                and row["model"] == "MTS_high_cs_fixed_profiled"
                and row["band"] == "all_2_1000"
                and row["data_vector"] == data_vector
            )
            chi2 = float(mts["chi2_proxy"])
            if chi2 < 2.0:
                verdict = "competitive_draw_proxy"
            elif chi2 < 10.0:
                verdict = "mild_pressure_proxy"
            elif chi2 < 50.0:
                verdict = "strong_pressure_proxy"
            else:
                verdict = "fails_mock_proxy_badly"
            snapshots.append(
                {
                    "arena": arena,
                    "data_vector": data_vector,
                    "MTS_chi2_proxy": chi2,
                    "MTS_delta_AIC_vs_LCDM": mts["delta_AIC_vs_LCDM"],
                    "MTS_delta_BIC_vs_LCDM": mts["delta_BIC_vs_LCDM"],
                    "verdict": verdict,
                    "interpretation": "synthetic LCDM/cosmic-variance proxy; not real CMB likelihood",
                }
            )
    return snapshots


def derivation_pivot_rows(snapshot_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    same_tt_ee = next(row for row in snapshot_rows if row["arena"] == "same_physical_densities" and row["data_vector"] == "TT_plus_EE")
    locked_tt_ee = next(row for row in snapshot_rows if row["arena"] == "locked_Omega_m_neutrino_subtracted" and row["data_vector"] == "TT_plus_EE")
    return [
        {
            "route": "same-density matched mock likelihood",
            "status": "worth_running_next",
            "evidence": f"TT+EE proxy chi2={same_tt_ee['MTS_chi2_proxy']}",
            "theory_cost": "requires H0≈65.92 and Omega_m drift; theta compensation not derived",
            "next_derivation_needed": "derive why MTS should predict this lower-H0 compensation rather than merely profile it",
        },
        {
            "route": "locked-Omega_m CMB branch",
            "status": "pivot_to_derivation_before_claim",
            "evidence": f"TT+EE proxy chi2={locked_tt_ee['MTS_chi2_proxy']}",
            "theory_cost": "percent-level shape residual survives theta profile",
            "next_derivation_needed": "derive a locked-matter theta/shape compensation mechanism or demote locked CMB branch",
        },
        {
            "route": "official likelihood",
            "status": "not_ready_but_now_well_scoped",
            "evidence": "mock likelihood proxy and branch policies are now machine-logged",
            "theory_cost": "official Planck/ACT/SPT likelihood assets still absent locally",
            "next_derivation_needed": "none directly; this is infrastructure, not theory",
        },
        {
            "route": "fundamental-theory promotion",
            "status": "blocked_by_derivation_debts",
            "evidence": "B_mem, theta compensation, exact perturbations, local GR are not derived",
            "theory_cost": "cannot promote CMB fit into fundamental theory without parent owners",
            "next_derivation_needed": "parent action and GR/local fixed-point mechanism",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], score_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    same = next(
        row
        for row in score_rows
        if row["arena"] == "same_physical_densities"
        and row["model"] == "MTS_high_cs_fixed_profiled"
        and row["band"] == "all_2_1000"
        and row["data_vector"] == "TT_plus_EE"
    )
    locked = next(
        row
        for row in score_rows
        if row["arena"] == "locked_Omega_m_neutrino_subtracted"
        and row["model"] == "MTS_high_cs_fixed_profiled"
        and row["band"] == "all_2_1000"
        and row["data_vector"] == "TT_plus_EE"
    )
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "mock proxy only",
        },
        {
            "gate": "equal baseline policy logged",
            "status": "pass",
            "evidence": "LCDM/wCDM/CPL/MTS scored with shared H0/theta profile policy",
            "claim_allowed": "fair proxy comparison",
        },
        {
            "gate": "same-density proxy competitive",
            "status": "pass" if float(same["chi2_proxy"]) < 2.0 else "warning",
            "evidence": f"TT+EE all-band chi2_proxy={same['chi2_proxy']}",
            "claim_allowed": "mock-likelihood next step",
        },
        {
            "gate": "locked-Omega_m proxy competitive",
            "status": "fail" if float(locked["chi2_proxy"]) > 50.0 else "warning",
            "evidence": f"TT+EE all-band chi2_proxy={locked['chi2_proxy']}",
            "claim_allowed": "derivation pivot before claim",
        },
        {
            "gate": "theta compensation derived",
            "status": "fail",
            "evidence": "checkpoint 188 theorem gate failed",
            "claim_allowed": "no theory promotion",
        },
        {
            "gate": "official CMB likelihood",
            "status": "not_run",
            "evidence": "no Planck/ACT/SPT likelihood called",
            "claim_allowed": "no CMB support claim",
        },
        {
            "gate": "support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(snapshot_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    same = next(row for row in snapshot_rows if row["arena"] == "same_physical_densities" and row["data_vector"] == "TT_plus_EE")
    locked = next(row for row in snapshot_rows if row["arena"] == "locked_Omega_m_neutrino_subtracted" and row["data_vector"] == "TT_plus_EE")
    return [
        {
            "decision": STATUS,
            "meaning": "same-density profiled branch is mock-competitive under equal rules; locked-Omega_m branch fails this proxy and should pivot to derivation before CMB claims",
            "same_density_TT_EE_chi2_proxy": same["MTS_chi2_proxy"],
            "locked_Omega_m_TT_EE_chi2_proxy": locked["MTS_chi2_proxy"],
            "next_target": "191-CMB-same-density-mock-likelihood-and-theta-derivation-bridge.md",
            "MTS_spectra_run": "false",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_190_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    residual_rows = read_csv_rows(RESIDUALS)
    mock_definition = mock_likelihood_definition_rows()
    model_policy = model_policy_rows()
    scores = scorecard_rows(residual_rows)
    snapshots = decision_snapshot_rows(scores)
    pivots = derivation_pivot_rows(snapshots)
    gates = claim_gate_rows(source_rows, scores)
    decision = decision_rows(snapshots)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "mock_likelihood_definition.csv": (
            mock_definition,
            ["item", "definition", "reason", "limitation"],
        ),
        "model_freedom_policy.csv": (
            model_policy,
            ["model", "shared_profile", "extra_parameters_counted", "score_role", "rule"],
        ),
        "mock_scorecard.csv": (
            scores,
            [
                "arena",
                "model",
                "band",
                "data_vector",
                "chi2_proxy",
                "k_extra",
                "n_data",
                "AIC_proxy",
                "BIC_proxy",
                "delta_AIC_vs_LCDM",
                "delta_BIC_vs_LCDM",
                "role",
                "readout",
                "claim_limit",
            ],
        ),
        "decision_snapshot.csv": (
            snapshots,
            ["arena", "data_vector", "MTS_chi2_proxy", "MTS_delta_AIC_vs_LCDM", "MTS_delta_BIC_vs_LCDM", "verdict", "interpretation"],
        ),
        "derivation_pivot_ledger.csv": (
            pivots,
            ["route", "status", "evidence", "theory_cost", "next_derivation_needed"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "same_density_TT_EE_chi2_proxy",
                "locked_Omega_m_TT_EE_chi2_proxy",
                "next_target",
                "MTS_spectra_run",
                "official_likelihood_run",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "same_density_TT_EE_chi2_proxy": decision[0]["same_density_TT_EE_chi2_proxy"],
        "locked_Omega_m_TT_EE_chi2_proxy": decision[0]["locked_Omega_m_TT_EE_chi2_proxy"],
        "MTS_spectra_run": False,
        "official_likelihood_run": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
