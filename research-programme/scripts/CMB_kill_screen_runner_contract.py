#!/usr/bin/env python3
"""Write the future CMB spectra kill-screen runner contract without running spectra."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"

CMB_INTERFACE_RUN = RUNS_ROOT / "20260531-235900-Boltzmann-interface-contract"
CMB_INTERFACE_RESULTS = CMB_INTERFACE_RUN / "results"
CMB_INTERFACE_STATUS = CMB_INTERFACE_RUN / "status.json"
CMB_VARIABLE_CONTRACT = CMB_INTERFACE_RESULTS / "Boltzmann_variable_contract.csv"
CMB_INTERFACE_MODES = CMB_INTERFACE_RESULTS / "interface_modes.csv"
CMB_SAFETY_TABLE = CMB_INTERFACE_RESULTS / "CMB_safety_table.csv"
CMB_CALIBRATION_TABLE = CMB_INTERFACE_RESULTS / "calibration_bridge_table.csv"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
CLAIM_CEILING = "CMB_kill_screen_runner_contract_no_spectra_run_no_support_claim"
FUTURE_RUNNER = WORK_DIR / "scripts" / "cmb_kill_screen_long_run.py"


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


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "150-Boltzmann-interface-contract.md",
        WORK_DIR / "149-smooth-memory-or-controlled-growth-theorem.md",
        WORK_DIR / "43-official-CMB-perturbation-contract.md",
        WORK_DIR / "44-minimal-CMB-perturbation-closure-attempt.md",
        WORK_DIR / "120-joint-calibration-red-team-and-repair-options.md",
        CMB_INTERFACE_STATUS,
        CMB_VARIABLE_CONTRACT,
        CMB_INTERFACE_MODES,
        CMB_SAFETY_TABLE,
        CMB_CALIBRATION_TABLE,
        FORMALIZATION_WORKBENCH / "08-long-run-workflow.md",
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": yes_no(exists),
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def source_role(path: Path) -> str:
    name = path.name
    if name == "150-Boltzmann-interface-contract.md":
        return "current Boltzmann interface checkpoint"
    if name == "149-smooth-memory-or-controlled-growth-theorem.md":
        return "late-time high-sound-speed growth suppression theorem"
    if name == "43-official-CMB-perturbation-contract.md":
        return "earlier official CMB support/kill-screen boundary"
    if name == "44-minimal-CMB-perturbation-closure-attempt.md":
        return "effective-fluid/scalar closure precedent"
    if name == "120-joint-calibration-red-team-and-repair-options.md":
        return "calibration bridge blocker"
    if name == "08-long-run-workflow.md":
        return "long-run status/log/DONE workflow"
    if name.endswith(".csv") or name == "status.json":
        return "machine output from checkpoint 150"
    return "script"


def environment_preflight_rows() -> list[dict[str, Any]]:
    checks = [
        {
            "item": "python_executable",
            "status": "present",
            "value": sys.executable,
            "impact": "contract generator can run",
        },
        {
            "item": "camb_python_module",
            "status": "available" if importlib.util.find_spec("camb") else "missing",
            "value": "camb",
            "impact": "needed for a CAMB-based spectra runner",
        },
        {
            "item": "classy_python_module",
            "status": "available" if importlib.util.find_spec("classy") else "missing",
            "value": "classy",
            "impact": "needed for a CLASS Python wrapper runner",
        },
        {
            "item": "class_executable",
            "status": "available" if shutil.which("class") else "missing",
            "value": shutil.which("class") or "",
            "impact": "needed for a standalone CLASS command runner",
        },
        {
            "item": "cobaya_python_module",
            "status": "available" if importlib.util.find_spec("cobaya") else "missing",
            "value": "cobaya",
            "impact": "useful for official likelihood plumbing",
        },
        {
            "item": "montepython_python_module",
            "status": "available" if importlib.util.find_spec("montepython") else "missing",
            "value": "montepython",
            "impact": "useful for CLASS likelihood plumbing",
        },
        {
            "item": "future_runner_script",
            "status": "available" if FUTURE_RUNNER.exists() else "missing",
            "value": str(FUTURE_RUNNER),
            "impact": "must be implemented before spectra can run",
        },
    ]
    return checks


def parameter_lock_rows(interface_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "parameter": "B_mem",
            "value": LOCKED_B_MEM,
            "status": "frozen",
            "allowed_to_vary_in_kill_screen": "no",
            "source": "locked 2/27 branch",
            "failure_if_changed": "turns kill-screen into refit/rescue",
        },
        {
            "parameter": "p",
            "value": LOCKED_P,
            "status": "frozen",
            "allowed_to_vary_in_kill_screen": "no",
            "source": "locked activation shape",
            "failure_if_changed": "activation retune after CMB",
        },
        {
            "parameter": "u3",
            "value": LOCKED_U3,
            "status": "frozen",
            "allowed_to_vary_in_kill_screen": "no",
            "source": "locked activation scale",
            "failure_if_changed": "activation retune after CMB",
        },
        {
            "parameter": "Omega_m0_late_transfer_reference",
            "value": interface_status.get("reference_Omega_m_late", ""),
            "status": "predeclared_bridge_input",
            "allowed_to_vary_in_kill_screen": "profile only in explicitly named CMB-only control",
            "source": "checkpoint 150 transfer reference",
            "failure_if_changed": "late-to-CMB bridge tension hidden",
        },
        {
            "parameter": "h_profiled_reference",
            "value": interface_status.get("reference_h_profiled", ""),
            "status": "predeclared_bridge_input",
            "allowed_to_vary_in_kill_screen": "only under declared calibration branch",
            "source": "checkpoint 150 transfer reference",
            "failure_if_changed": "absolute calibration bridge hidden",
        },
        {
            "parameter": "c_s_eff_squared",
            "value": "1 for high-c_s effective closure; not applicable for exact auxiliary closure",
            "status": "closure_choice",
            "allowed_to_vary_in_kill_screen": "no",
            "source": "checkpoints 149-150",
            "failure_if_changed": "becomes fitted dark-sector sound speed",
        },
        {
            "parameter": "sigma_mem",
            "value": "0",
            "status": "closure_choice",
            "allowed_to_vary_in_kill_screen": "no",
            "source": "effective scalar / exact auxiliary route",
            "failure_if_changed": "introduces fitted slip/lensing rescue",
        },
    ]


def run_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "LCDM_baseline_reproduction",
            "model": "LCDM",
            "closure": "standard_GR",
            "calibration_policy": "same likelihoods and nuisance treatment as MTS branches",
            "purpose": "prove pipeline reproduces baseline spectra/likelihood before reading MTS",
            "interpretation_allowed": "yes_baseline_only",
        },
        {
            "run_id": "MTS_exact_auxiliary_transfer_locked",
            "model": "MTS_locked_2over27",
            "closure": "exact_auxiliary_smooth_memory",
            "calibration_policy": "late Omega_m transfer branch; no hidden Omega_m reset",
            "purpose": "strict kill-screen of the cleanest no-clustering memory closure",
            "interpretation_allowed": "kill_screen_only",
        },
        {
            "run_id": "MTS_high_cs_transfer_locked",
            "model": "MTS_locked_2over27",
            "closure": "high_sound_speed_effective_scalar",
            "calibration_policy": "late Omega_m transfer branch; no fitted sound speed",
            "purpose": "test the effective c_s^2=1 route implied by checkpoint 149",
            "interpretation_allowed": "kill_screen_only",
        },
        {
            "run_id": "MTS_exact_auxiliary_joint_calibration",
            "model": "MTS_locked_2over27",
            "closure": "exact_auxiliary_smooth_memory",
            "calibration_policy": "joint h-r_d-alpha-SN-offset branch logged separately",
            "purpose": "test whether spectra survive the existing mixed calibration bridge",
            "interpretation_allowed": "diagnostic_only_until_calibration_theorem",
        },
        {
            "run_id": "MTS_high_cs_joint_calibration",
            "model": "MTS_locked_2over27",
            "closure": "high_sound_speed_effective_scalar",
            "calibration_policy": "joint h-r_d-alpha-SN-offset branch logged separately",
            "purpose": "test effective scalar closure under shared calibration stress",
            "interpretation_allowed": "diagnostic_only_until_calibration_theorem",
        },
        {
            "run_id": "MTS_CMB_only_control",
            "model": "MTS_locked_2over27",
            "closure": "high_sound_speed_effective_scalar_or_exact_auxiliary",
            "calibration_policy": "CMB-only refit clearly labelled control",
            "purpose": "separate CMB spectra compatibility from late-to-CMB transfer failure",
            "interpretation_allowed": "control_only_no_late_bridge_claim",
        },
    ]


def output_artifact_rows() -> list[dict[str, Any]]:
    return [
        {"artifact": "run_config.json", "required": "yes", "purpose": "records exact frozen parameters, closure mode, engine, and likelihood list"},
        {"artifact": "log.txt", "required": "yes", "purpose": "append-only run log; Codex should not watch terminal output for hours"},
        {"artifact": "status.json", "required": "yes", "purpose": "queued/running/done/failed status with current step and progress"},
        {"artifact": "DONE.txt or FAILED.txt", "required": "yes", "purpose": "single completion marker"},
        {"artifact": "engine_version.json", "required": "yes", "purpose": "CLASS/CAMB/Cobaya/likelihood version lock"},
        {"artifact": "baseline_reproduction.csv", "required": "yes", "purpose": "baseline sanity check before MTS interpretation"},
        {"artifact": "background_functions.csv", "required": "yes", "purpose": "H(a), rho_mem, w_mem, Omega fractions actually passed to engine"},
        {"artifact": "spectra_TT_TE_EE.csv", "required": "yes", "purpose": "C_ell comparison table"},
        {"artifact": "lensing_phi_phi.csv", "required": "yes", "purpose": "CMB lensing kernel check"},
        {"artifact": "late_ISW_diagnostics.csv", "required": "yes", "purpose": "detect whether low-l/ISW dominates failure"},
        {"artifact": "likelihood_scorecard.csv", "required": "yes", "purpose": "Delta chi2 by sector against baseline"},
        {"artifact": "claim_gate_results.csv", "required": "yes", "purpose": "machine-readable pass/draw/fail and claim ceiling"},
    ]


def score_band_rows() -> list[dict[str, Any]]:
    return [
        {"metric": "baseline_reproduction", "band": "required_first", "threshold": "must reproduce configured LCDM reference before MTS is read", "decision": "otherwise pipeline fail"},
        {"metric": "Delta_chi2_total_vs_baseline", "band": "competitive_draw", "threshold": "<= 2", "decision": "survives kill-screen only; not support"},
        {"metric": "Delta_chi2_total_vs_baseline", "band": "mild_tension", "threshold": "> 2 and <= 6", "decision": "inspect sector residuals before demotion"},
        {"metric": "Delta_chi2_total_vs_baseline", "band": "serious_tension", "threshold": "> 6 and <= 10", "decision": "branch needs repair or derived reason"},
        {"metric": "Delta_chi2_total_vs_baseline", "band": "hard_fail", "threshold": "> 10", "decision": "CMB kill-screen rejects that closure/calibration branch"},
        {"metric": "sector_degradation", "band": "hard_sector_fail", "threshold": "any TT/TE/EE/lensing sector degradation > 6", "decision": "do not hide sector failure in total score"},
        {"metric": "edge_or_rescue_knob", "band": "invalid", "threshold": "B_mem,p,u3,c_s_eff,sigma_mem or closure mode changed after seeing CMB", "decision": "discard run"},
    ]


def long_run_workflow_rows(run_dir: Path) -> list[dict[str, Any]]:
    config_dir = run_dir / "configs"
    dry_config = config_dir / "MTS_high_cs_transfer_locked.blueprint.json"
    return [
        {
            "step": "1",
            "phase": "implement future runner",
            "command": f"create {FUTURE_RUNNER}",
            "expected_output": "dry-run-capable long runner using this contract",
            "watch_policy": "do_not_start_long_run_until_dry_run_passes",
        },
        {
            "step": "2",
            "phase": "dry run",
            "command": f'& "{sys.executable}" "{FUTURE_RUNNER}" --config "{dry_config}" --dry-run',
            "expected_output": "validates engine, likelihood paths, output folder, parameter locks",
            "watch_policy": "short_interactive_ok",
        },
        {
            "step": "3",
            "phase": "launch from VS Code terminal",
            "command": f'& "{sys.executable}" "{FUTURE_RUNNER}" --config "{dry_config}"',
            "expected_output": "writes log.txt, status.json, results, DONE.txt or FAILED.txt",
            "watch_policy": "launch_then_stop_spending_tokens",
        },
        {
            "step": "4",
            "phase": "return prompt",
            "command": f'inspect run {run_dir}',
            "expected_output": "Codex reads status/log/results after user returns",
            "watch_policy": "inspect_after_completion",
        },
    ]


def failure_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "baseline_reproduction_fails",
            "decision": "fix pipeline before reading MTS",
            "claim_allowed": "none",
        },
        {
            "case": "MTS_exact_auxiliary_passes_or_draws",
            "decision": "closure survives CMB kill-screen; still requires parent constraint derivation",
            "claim_allowed": "private survival result only",
        },
        {
            "case": "MTS_high_cs_passes_or_draws",
            "decision": "effective scalar route survives; still no parent support claim",
            "claim_allowed": "private kill-screen survival only",
        },
        {
            "case": "both_smooth_modes_fail",
            "decision": "return to controlled modified growth or demote CMB branch",
            "claim_allowed": "late-time branch only, CMB rejected for current closure",
        },
        {
            "case": "spectra_survive_but_calibration_bridge_fails",
            "decision": "separate CMB perturbation compatibility from late-to-CMB calibration promotion",
            "claim_allowed": "no unified cosmology claim",
        },
        {
            "case": "spectra_survive_and_calibration_bridge_survives",
            "decision": "promote to stronger private candidate; still needs parent action/local GR/amplitude derivation",
            "claim_allowed": "serious CMB-compatible candidate, not completed theory",
        },
    ]


def gate_rows(environment: list[dict[str, Any]]) -> list[dict[str, Any]]:
    engine_available = any(
        row["status"] == "available"
        for row in environment
        if row["item"] in {"camb_python_module", "classy_python_module", "class_executable"}
    )
    future_runner_available = any(
        row["item"] == "future_runner_script" and row["status"] == "available"
        for row in environment
    )
    return [
        {
            "gate": "checkpoint_150_interface_available",
            "status": "pass",
            "evidence": str(CMB_INTERFACE_STATUS),
        },
        {
            "gate": "parameter_locks_declared",
            "status": "pass",
            "evidence": "B_mem,p,u3,c_s_eff,sigma_mem lock policy written",
        },
        {
            "gate": "baseline_parity_declared",
            "status": "pass",
            "evidence": "LCDM baseline reproduction must pass before MTS interpretation",
        },
        {
            "gate": "long_run_artifacts_declared",
            "status": "pass",
            "evidence": "run_config, log, status, DONE/FAILED, spectra, lensing, scorecards specified",
        },
        {
            "gate": "engine_dependency_available_now",
            "status": "pass" if engine_available else "blocked_for_execution",
            "evidence": "CLASS/CAMB executable/module detected" if engine_available else "no CLASS/CAMB engine detected in current Python/PATH",
        },
        {
            "gate": "future_runner_available_now",
            "status": "pass" if future_runner_available else "blocked_for_execution",
            "evidence": str(FUTURE_RUNNER),
        },
        {
            "gate": "CMB_support_claim",
            "status": "fail",
            "evidence": "contract only; no spectra/lensing likelihood run",
        },
    ]


def decision_rows(environment: list[dict[str, Any]]) -> list[dict[str, Any]]:
    engine_available = any(
        row["status"] == "available"
        for row in environment
        if row["item"] in {"camb_python_module", "classy_python_module", "class_executable"}
    )
    runner_available = any(
        row["item"] == "future_runner_script" and row["status"] == "available"
        for row in environment
    )
    execution_status = (
        "ready_for_dry_run"
        if engine_available and runner_available
        else "contract_ready_execution_blocked_by_missing_engine_or_runner"
    )
    return [
        {
            "item": "status",
            "verdict": "CMB_kill_screen_runner_contract_written_no_spectra_run",
            "evidence": "run matrix, locks, artifacts, score bands, workflow, and decision tree generated",
        },
        {
            "item": "execution_status",
            "verdict": execution_status,
            "evidence": "environment preflight records current CLASS/CAMB/runner availability",
        },
        {
            "item": "best_next_target",
            "verdict": "implement_cmb_kill_screen_long_run_stub_or_return_to_calibration_theorem",
            "evidence": "next implementation needs a real engine wrapper or a derived h-r_d-alpha calibration relation",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no spectra computed; this only prevents future CMB testing from becoming a free rescue fit",
        },
    ]


def config_blueprints(run_dir: Path, interface_status: dict[str, Any]) -> list[dict[str, Any]]:
    config_dir = run_dir / "configs"
    common = {
        "schema": "MTS_CMB_KILL_SCREEN_BLUEPRINT_V1",
        "dry_run_blueprint_only": True,
        "claim_ceiling": CLAIM_CEILING,
        "output_contract": {
            "status_json": "status.json",
            "log": "log.txt",
            "completion_marker": "DONE.txt or FAILED.txt",
            "results": [
                "baseline_reproduction.csv",
                "background_functions.csv",
                "spectra_TT_TE_EE.csv",
                "lensing_phi_phi.csv",
                "late_ISW_diagnostics.csv",
                "likelihood_scorecard.csv",
                "claim_gate_results.csv",
            ],
        },
        "likelihood_blocks": [
            "temperature_TT",
            "polarization_TE_EE",
            "low_l",
            "lensing_phi_phi",
        ],
        "fixed_mts_parameters": {
            "B_mem": LOCKED_B_MEM,
            "p": LOCKED_P,
            "u3": LOCKED_U3,
            "Omega_m0_late_reference": interface_status.get("reference_Omega_m_late", ""),
            "h_profiled_reference": interface_status.get("reference_h_profiled", ""),
        },
        "no_rescue_rules": [
            "do_not_refit_B_mem",
            "do_not_refit_p_or_u3",
            "do_not_fit_c_s_eff",
            "do_not_fit_sigma_mem_or_slip",
            "log_calibration_branch_separately",
        ],
    }
    configs = [
        {
            **common,
            "config_id": "LCDM_baseline_reproduction",
            "engine": "CLASS_or_CAMB",
            "model": "LCDM",
            "closure_mode": "standard_GR",
            "calibration_policy": "baseline parity reproduction before MTS interpretation",
        },
        {
            **common,
            "config_id": "MTS_exact_auxiliary_transfer_locked",
            "engine": "CLASS_or_CAMB_custom_module",
            "model": "MTS_locked_2over27",
            "closure_mode": "exact_auxiliary_smooth_memory",
            "calibration_policy": "late Omega_m transfer; no hidden reset",
        },
        {
            **common,
            "config_id": "MTS_high_cs_transfer_locked",
            "engine": "CLASS_or_CAMB_effective_fluid_or_PPF",
            "model": "MTS_locked_2over27",
            "closure_mode": "high_sound_speed_effective_scalar",
            "calibration_policy": "late Omega_m transfer; c_s_eff^2 fixed to 1",
        },
    ]
    rows = []
    for config in configs:
        path = config_dir / f"{config['config_id']}.blueprint.json"
        write_json(path, config)
        rows.append(
            {
                "config_id": config["config_id"],
                "path": str(path),
                "engine": config["engine"],
                "model": config["model"],
                "closure_mode": config["closure_mode"],
                "calibration_policy": config["calibration_policy"],
                "dry_run_blueprint_only": "yes",
            }
        )
    return rows


def write_launch_commands(run_dir: Path, workflow: list[dict[str, Any]]) -> None:
    lines = [
        "# CMB kill-screen future launch commands",
        "# Generated as a contract only. Do not run until scripts\\cmb_kill_screen_long_run.py exists and dry-run passes.",
        f'Set-Location -LiteralPath "{WORK_DIR}"',
        "",
    ]
    for row in workflow:
        lines.append(f"# Step {row['step']}: {row['phase']}")
        lines.append(str(row["command"]))
        lines.append("")
    (run_dir / "launch_commands.ps1").write_text("\n".join(lines), encoding="utf-8")


def run_contract(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-CMB-kill-screen-runner-contract"
    results_dir = run_dir / "results"
    run_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing_sources = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing_sources:
        raise FileNotFoundError(f"missing required source files: {missing_sources}")

    interface_status = read_json(CMB_INTERFACE_STATUS)
    environment = environment_preflight_rows()
    parameter_locks = parameter_lock_rows(interface_status)
    run_matrix = run_matrix_rows()
    artifacts = output_artifact_rows()
    score_bands = score_band_rows()
    failure_tree = failure_decision_rows()
    config_rows = config_blueprints(run_dir, interface_status)
    workflow = long_run_workflow_rows(run_dir)
    gates = gate_rows(environment)
    decisions = decision_rows(environment)

    write_launch_commands(run_dir, workflow)
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "environment_preflight.csv", environment, ["item", "status", "value", "impact"])
    write_csv(
        results_dir / "parameter_lock_manifest.csv",
        parameter_locks,
        ["parameter", "value", "status", "allowed_to_vary_in_kill_screen", "source", "failure_if_changed"],
    )
    write_csv(
        results_dir / "kill_screen_run_matrix.csv",
        run_matrix,
        ["run_id", "model", "closure", "calibration_policy", "purpose", "interpretation_allowed"],
    )
    write_csv(
        results_dir / "config_blueprint_register.csv",
        config_rows,
        ["config_id", "path", "engine", "model", "closure_mode", "calibration_policy", "dry_run_blueprint_only"],
    )
    write_csv(results_dir / "output_artifact_contract.csv", artifacts, ["artifact", "required", "purpose"])
    write_csv(results_dir / "score_band_policy.csv", score_bands, ["metric", "band", "threshold", "decision"])
    write_csv(results_dir / "failure_decision_tree.csv", failure_tree, ["case", "decision", "claim_allowed"])
    write_csv(results_dir / "long_run_workflow.csv", workflow, ["step", "phase", "command", "expected_output", "watch_policy"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    execution_status = next(row["verdict"] for row in decisions if row["item"] == "execution_status")
    status = {
        "status": status_value,
        "execution_status": execution_status,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "generated": [
            "source_register.csv",
            "environment_preflight.csv",
            "parameter_lock_manifest.csv",
            "kill_screen_run_matrix.csv",
            "config_blueprint_register.csv",
            "output_artifact_contract.csv",
            "score_band_policy.csv",
            "failure_decision_tree.csv",
            "long_run_workflow.csv",
            "gate_results.csv",
            "decision.csv",
            "launch_commands.ps1",
            "configs/*.blueprint.json",
        ],
        "next_target": "implement_cmb_kill_screen_long_run_stub_or_return_to_calibration_theorem",
    }
    write_json(run_dir / "status.json", status)
    (run_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (run_dir / "DONE.txt").write_text(status_value + "\n", encoding="utf-8")
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
