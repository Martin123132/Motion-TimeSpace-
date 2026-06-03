#!/usr/bin/env python3
"""Audit the late-CMB calibration bridge and write the owner/no-go contract."""

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
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"

SHARED_CAL_RUN = RUNS_ROOT / "20260531-171500-shared-calibration-relation-attempt"
SHARED_CAL_RESULTS = SHARED_CAL_RUN / "results"
SHARED_AGGREGATE = SHARED_CAL_RESULTS / "aggregate_targets.csv"
SHARED_DECISION = SHARED_CAL_RESULTS / "decision.csv"

OMEGA_MAP_RUN = RUNS_ROOT / "20260531-172300-early-late-Omega-map-theorem-attempt"
OMEGA_MAP_RESULTS = OMEGA_MAP_RUN / "results"
OMEGA_AGGREGATE = OMEGA_MAP_RESULTS / "aggregate_map_diagnostics.csv"
OMEGA_CANDIDATES = OMEGA_MAP_RESULTS / "candidate_map_audit.csv"
OMEGA_DECISION = OMEGA_MAP_RESULTS / "decision.csv"

BOLTZMANN_RUN = RUNS_ROOT / "20260531-235900-Boltzmann-interface-contract"
BOLTZMANN_RESULTS = BOLTZMANN_RUN / "results"
CMB_SAFETY = BOLTZMANN_RESULTS / "CMB_safety_table.csv"
CMB_CALIBRATION = BOLTZMANN_RESULTS / "calibration_bridge_table.csv"
BOLTZMANN_STATUS = BOLTZMANN_RUN / "status.json"

KILL_SCREEN_RUN = RUNS_ROOT / "20260531-235950-CMB-kill-screen-runner-contract"
KILL_SCREEN_STATUS = KILL_SCREEN_RUN / "status.json"

LOCKED_B_MEM = 2.0 / 27.0
DELTA_R_TARGET = 2.0 / 9.0
B_MEM_DELTA_R = LOCKED_B_MEM * DELTA_R_TARGET
CLAIM_CEILING = "calibration_bridge_no_go_owner_contract_no_CMB_promotion"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "118-locked-2over27-joint-late-CMB-calibration-contract.md",
        WORK_DIR / "119-locked-2over27-joint-late-CMB-calibration-runner.md",
        WORK_DIR / "120-joint-calibration-red-team-and-repair-options.md",
        WORK_DIR / "121-shared-calibration-relation-derivation-attempt.md",
        WORK_DIR / "122-early-late-Omega-map-theorem-attempt.md",
        WORK_DIR / "123-CMB-bridge-demotion-and-next-test-route.md",
        WORK_DIR / "150-Boltzmann-interface-contract.md",
        WORK_DIR / "151-CMB-kill-screen-runner-contract.md",
        SHARED_CAL_RUN / "status.json",
        SHARED_AGGREGATE,
        SHARED_DECISION,
        OMEGA_MAP_RUN / "status.json",
        OMEGA_AGGREGATE,
        OMEGA_CANDIDATES,
        OMEGA_DECISION,
        BOLTZMANN_STATUS,
        CMB_SAFETY,
        CMB_CALIBRATION,
        KILL_SCREEN_STATUS,
        FORMALIZATION_WORKBENCH / "08-long-run-workflow.md",
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("118-"):
        return "joint late-CMB calibration contract"
    if name.startswith("119-"):
        return "joint calibration runner result"
    if name.startswith("120-"):
        return "calibration red-team"
    if name.startswith("121-"):
        return "alpha/r_d relation audit"
    if name.startswith("122-"):
        return "early-late Omega map attempt"
    if name.startswith("123-"):
        return "CMB bridge demotion route"
    if name.startswith("150-"):
        return "Boltzmann interface contract"
    if name.startswith("151-"):
        return "CMB kill-screen contract"
    if name == "08-long-run-workflow.md":
        return "future long-run workflow"
    if name.endswith(".csv") or name == "status.json":
        return "machine source output"
    return "script"


def value_map(rows: list[dict[str, str]], key_field: str = "quantity", value_field: str = "value") -> dict[str, float]:
    values = {}
    for row in rows:
        key = row[key_field]
        value = row[value_field]
        try:
            values[key] = float(value)
        except (TypeError, ValueError):
            continue
    return values


def cmb_recombination_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv_rows(CMB_SAFETY)
        if 1000.0 < float(row["z"]) < 1200.0
    ]


def calibration_bridge_rows() -> list[dict[str, str]]:
    return read_csv_rows(CMB_CALIBRATION)


def no_go_assumption_rows() -> list[dict[str, Any]]:
    return [
        {
            "assumption_id": "A1",
            "assumption": "single metric background",
            "consequence": "the same H(a) and distance integrals govern CMB, BAO, and SN once parameters are fixed",
            "breaks_if": "two-metric, disformal, or environment-dependent ruler map is derived",
            "status": "retained_conservative_default",
        },
        {
            "assumption_id": "A2",
            "assumption": "ordinary matter is separately conserved",
            "consequence": "rho_m(a)=rho_m0 a^-3 and Omega_m0^early=Omega_m0^late",
            "breaks_if": "a covariant Q^nu exchange is derived with local Q^nu -> 0",
            "status": "retained_until_Qnu_parent_exists",
        },
        {
            "assumption_id": "A3",
            "assumption": "standard BAO ruler relation",
            "consequence": "alpha_BAO=c/(100 h r_d) is the only scalar absolute-calibration relation",
            "breaks_if": "a memory-sector r_d or BAO-shape deformation is parent-derived",
            "status": "retained_by_checkpoint_121",
        },
        {
            "assumption_id": "A4",
            "assumption": "memory fraction negligible at recombination",
            "consequence": "primary plasma background does not naturally shift Omega_m0 by percent-level amounts",
            "breaks_if": "Boltzmann spectra show an inference-level shift despite tiny background fraction",
            "status": "supported_by_checkpoint_150",
        },
        {
            "assumption_id": "A5",
            "assumption": "no private MTS rescue knobs",
            "consequence": "any map must also state baseline treatment and B_mem->0 identity limit",
            "breaks_if": "none allowed; this is a fairness rule",
            "status": "hard_rule",
        },
    ]


def evidence_rows() -> list[dict[str, Any]]:
    shared = value_map(read_csv_rows(SHARED_AGGREGATE))
    omega = value_map(read_csv_rows(OMEGA_AGGREGATE))
    recomb = cmb_recombination_rows()
    max_omega_mem_recomb = max(float(row["Omega_mem_fraction_with_radiation"]) for row in recomb)
    max_one_plus_w_recomb = max(abs(float(row["one_plus_w_mem"])) for row in recomb)
    joint_shift = omega["joint_shift_needed_mean"]
    failing_shift = shared["failing_gate_Omega_m0_shift_vs_T7"]
    ratio_mean_to_recomb = joint_shift / max_omega_mem_recomb if max_omega_mem_recomb else math.inf
    ratio_failing_to_recomb = failing_shift / max_omega_mem_recomb if max_omega_mem_recomb else math.inf
    return [
        {
            "item": "late_only_target",
            "value": "Omega_m0=0.3032827426766658; alpha_BAO=30.012562164133616",
            "readout": "late SN+BAO locked branch target",
            "source": str(SHARED_AGGREGATE),
        },
        {
            "item": "alpha_tie_not_problem",
            "value": f"xi_same_shape_mean={shared['same_shape_xi_required_mean']}; tied_alpha_penalty_mean={shared['BAO_calibration_penalty_same_shape_mean']}",
            "readout": "alpha_BAO=c/(100hr_d) is already effectively the fixed-shape optimum",
            "source": str(SHARED_AGGREGATE),
        },
        {
            "item": "BAO_shape_penalty",
            "value": f"mean_free_alpha_shape_penalty={shared['BAO_shape_penalty_free_vs_T7_mean']}; failing_gate_shape_penalty={shared['failing_gate_BAO_shape_penalty_free_vs_T7']}",
            "readout": "residual is background-shape/Omega_m0 driven, not scalar alpha calibration",
            "source": str(SHARED_AGGREGATE),
        },
        {
            "item": "Omega_shift_target",
            "value": f"joint_mean_shift={joint_shift}; failing_gate_shift={failing_shift}",
            "readout": "needed shift is percent-level in Omega_m0",
            "source": str(OMEGA_AGGREGATE),
        },
        {
            "item": "Bmem_DeltaR_coincidence",
            "value": f"Bmem_DeltaR={B_MEM_DELTA_R}; joint_mean_residual={omega['joint_Bmem_DeltaR_residual_mean']}; worst_joint_residual={omega['joint_Bmem_DeltaR_abs_residual_max']}",
            "readout": "centers joint rows strikingly well but is not exact or parent-derived",
            "source": str(OMEGA_AGGREGATE),
        },
        {
            "item": "CMB_only_not_repaired",
            "value": f"best_CMB_only_residual_after_Bmem_DeltaR={omega['CMB_locked_to_T7_Bmem_DeltaR_abs_residual_min']}",
            "readout": "Bmem_DeltaR is not a full CMB-to-late transfer theorem",
            "source": str(OMEGA_AGGREGATE),
        },
        {
            "item": "recombination_memory_fraction",
            "value": f"max_Omega_mem_recombination={max_omega_mem_recomb}; max_abs_1_plus_w={max_one_plus_w_recomb}",
            "readout": "primary-era background injection is tiny",
            "source": str(CMB_SAFETY),
        },
        {
            "item": "shift_vs_recombination_fraction",
            "value": f"joint_shift/recomb_fraction={ratio_mean_to_recomb}; failing_shift/recomb_fraction={ratio_failing_to_recomb}",
            "readout": "the bridge shift cannot be explained as direct primary-era memory density under conservative assumptions",
            "source": f"{OMEGA_AGGREGATE}; {CMB_SAFETY}",
        },
    ]


def owner_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "identity_map",
            "mechanism": "Omega_m0^early = Omega_m0^late",
            "status": "derived_under_conservative_assumptions",
            "helps_bridge": "no",
            "required_owner": "separately conserved dust and single metric",
            "fatal_issue": "empirically fails the late-to-CMB transfer target",
        },
        {
            "candidate": "alpha_or_r_d_scalar_calibration",
            "mechanism": "alpha_BAO -> xi alpha_BAO or r_d_eff",
            "status": "rejected_as_primary_repair",
            "helps_bridge": "no_at_fixed_shape",
            "required_owner": "already encoded by c/(100 h r_d)",
            "fatal_issue": "same-shape xi is 1+O(1e-8); remaining cost is BAO shape",
        },
        {
            "candidate": "Bmem_DeltaR_closure",
            "mechanism": "Omega_m0_late = Omega_m0_source - B_mem*(2/9)",
            "status": "useful_empirical_coincidence",
            "helps_bridge": "partial_joint_centering",
            "required_owner": "boundary/current normalization that predicts DeltaR=2/9 map",
            "fatal_issue": "branch-dependent residuals and CMB-only transfer not repaired",
        },
        {
            "candidate": "Qnu_memory_matter_exchange",
            "mechanism": "nabla_mu T_m^{mu nu}=Q^nu, nabla_mu T_mem^{mu nu}=-Q^nu",
            "status": "allowed_only_if_parent_derived",
            "helps_bridge": "possible",
            "required_owner": "covariant exchange current with local Q^nu -> 0 and no fitted growth fudge",
            "fatal_issue": "would threaten local GR/PPN and growth if not screened",
        },
        {
            "candidate": "BAO_shape_correction",
            "mechanism": "F_BAO -> F_BAO + delta F_mem(z)",
            "status": "live_theorem_target",
            "helps_bridge": "possible",
            "required_owner": "memory-sector ruler/drag/redshift projection derived from parent action",
            "fatal_issue": "forbidden as ad hoc residual patch",
        },
        {
            "candidate": "full_Boltzmann_inference_map",
            "mechanism": "CMB-inferred Omega_m0 shifts through TT/TE/EE/lensing response, not compressed priors",
            "status": "not_run",
            "helps_bridge": "unknown",
            "required_owner": "CMB spectra kill-screen runner and perturbation closure from checkpoints 150-151",
            "fatal_issue": "no engine/wrapper yet and no support claim without spectra",
        },
    ]


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "identity_limit",
            "required_condition": "B_mem -> 0 implies Omega_m0^late = Omega_m0^early and delta F_BAO -> 0",
            "status": "mandatory",
            "failure_if_missing": "baseline parity violation",
        },
        {
            "gate": "parent_owner",
            "required_condition": "derive the map from action/current/projection equations, not from likelihood residuals",
            "status": "missing",
            "failure_if_missing": "closure-only",
        },
        {
            "gate": "local_screening",
            "required_condition": "any Q^nu or ruler deformation must vanish in local/PPN regimes",
            "status": "missing",
            "failure_if_missing": "local GR branch fails",
        },
        {
            "gate": "growth_consistency",
            "required_condition": "do not spoil the high-c_s growth suppression result or add fitted mu/sigma8 rescue",
            "status": "mandatory",
            "failure_if_missing": "growth holdout loses interpretation",
        },
        {
            "gate": "CMB_spectra_consistency",
            "required_condition": "survive TT/TE/EE/lensing kill-screen under the same calibration branch",
            "status": "not_run",
            "failure_if_missing": "no CMB support claim",
        },
        {
            "gate": "late_branch_preservation",
            "required_condition": "recover Omega_m0_late ~= 0.3032827426766658 and the existing late-time wins/draws",
            "status": "mandatory",
            "failure_if_missing": "bridge repairs CMB by breaking the successful late branch",
        },
        {
            "gate": "no_hidden_amplitude_refit",
            "required_condition": "B_mem=2/27 remains frozen and does not become a map-fitting knob",
            "status": "mandatory",
            "failure_if_missing": "amplitude overclaim/rescue fit",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    shared = value_map(read_csv_rows(SHARED_AGGREGATE))
    omega = value_map(read_csv_rows(OMEGA_AGGREGATE))
    recomb = cmb_recombination_rows()
    max_omega_mem_recomb = max(float(row["Omega_mem_fraction_with_radiation"]) for row in recomb)
    alpha_penalty = shared["BAO_calibration_penalty_same_shape_mean"]
    shape_penalty = shared["BAO_shape_penalty_free_vs_T7_mean"]
    bmem_residual = omega["joint_Bmem_DeltaR_abs_residual_max"]
    cmb_only_residual = omega["CMB_locked_to_T7_Bmem_DeltaR_abs_residual_min"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "all cited source artifacts exist",
        },
        {
            "gate": "alpha_r_d_repair",
            "status": "fail_as_primary_repair",
            "evidence": f"same-shape tied-alpha penalty={alpha_penalty:.6g}; remaining BAO shape penalty={shape_penalty:.6g}",
        },
        {
            "gate": "identity_map_under_conservative_assumptions",
            "status": "pass_no_go",
            "evidence": "separately conserved dust and single metric force the trivial map",
        },
        {
            "gate": "Bmem_DeltaR_bridge",
            "status": "partial_empirical_coincidence",
            "evidence": f"Bmem*2/9={B_MEM_DELTA_R:.12g}; worst joint residual={bmem_residual:.6g}; CMB-only residual={cmb_only_residual:.6g}",
        },
        {
            "gate": "primary_CMB_background_owner",
            "status": "not_enough",
            "evidence": f"max recombination Omega_mem={max_omega_mem_recomb:.6g}; direct primary-era density is too small for percent-level Omega bridge",
        },
        {
            "gate": "bridge_promotion",
            "status": "fail",
            "evidence": "no parent Q^nu, BAO-shape owner, or full Boltzmann inference map has been derived",
        },
        {
            "gate": "claim_discipline",
            "status": "pass_control",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    shared = value_map(read_csv_rows(SHARED_AGGREGATE))
    omega = value_map(read_csv_rows(OMEGA_AGGREGATE))
    return [
        {
            "item": "status",
            "verdict": "calibration_bridge_no_go_under_conservative_assumptions_owner_contract_written",
            "evidence": "identity map follows under separate conservation; alpha/r_d repair is ruled out as primary lever; nontrivial bridge needs new owner",
        },
        {
            "item": "strongest_positive_clue",
            "verdict": "Bmem_DeltaR_joint_centering_coincidence",
            "evidence": f"Bmem*2/9={B_MEM_DELTA_R:.12g}; joint mean residual={omega['joint_Bmem_DeltaR_residual_mean']:.6g}; mean target shift={omega['joint_shift_needed_mean']:.6g}",
        },
        {
            "item": "strongest_negative_result",
            "verdict": "alpha_r_d_scalar_calibration_not_the_repair",
            "evidence": f"xi spread={shared['same_shape_xi_required_max_spread']:.6g}; failing same-shape alpha penalty={shared['failing_gate_BAO_calibration_penalty_same_shape']:.6g}",
        },
        {
            "item": "promotion_allowed",
            "verdict": "false",
            "evidence": "no CMB promotion; bridge remains closure-only until Q^nu/BAO-shape/full-Boltzmann owner exists",
        },
        {
            "item": "next_target",
            "verdict": "153-BAO-shape-or-Qnu-bridge-owner.md",
            "evidence": "the only live theorem routes are a parent-owned BAO-shape correction, a screened Q^nu map, or a full Boltzmann inference map",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "private no-go/owner contract only",
        },
    ]


def run_contract(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-calibration-bridge-no-go-owner-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    assumptions = no_go_assumption_rows()
    evidence = evidence_rows()
    candidates = owner_candidate_rows()
    theorem_contract = theorem_contract_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "no_go_assumptions.csv", assumptions, ["assumption_id", "assumption", "consequence", "breaks_if", "status"])
    write_csv(results_dir / "calibration_evidence_table.csv", evidence, ["item", "value", "readout", "source"])
    write_csv(results_dir / "owner_candidate_matrix.csv", candidates, ["candidate", "mechanism", "status", "helps_bridge", "required_owner", "fatal_issue"])
    write_csv(results_dir / "theorem_contract.csv", theorem_contract, ["gate", "required_condition", "status", "failure_if_missing"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "locked_B_mem": LOCKED_B_MEM,
        "DeltaR_target": DELTA_R_TARGET,
        "B_mem_DeltaR": B_MEM_DELTA_R,
        "generated": [
            "source_register.csv",
            "no_go_assumptions.csv",
            "calibration_evidence_table.csv",
            "owner_candidate_matrix.csv",
            "theorem_contract.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "153-BAO-shape-or-Qnu-bridge-owner.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_contract(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
