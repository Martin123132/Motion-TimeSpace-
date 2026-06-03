#!/usr/bin/env python3
"""Checkpoint 180: choose CMB kill-screen tooling or another amplitude-owner attempt."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_178_RUN = RUNS_ROOT / "20260531-235959-memory-perturbation-owner-derivation-attempt"
CHECKPOINT_179_RUN = RUNS_ROOT / "20260531-235959-local-GR-PPN-silence-contract"
CMB_CONTRACT_RUN = RUNS_ROOT / "20260531-235950-CMB-kill-screen-runner-contract"
AMPLITUDE_RUN = RUNS_ROOT / "20260531-204500-boundary-charge-amplitude-decision-gate"
OFFICIAL_DECISION_RUN = RUNS_ROOT / "20260531-235959-official-refresh-decision-gate"

STATUS_PASS = "decision_prioritize_CMB_engine_readiness_then_kill_screen_keep_amplitude_as_theorem_debt"
CLAIM_CEILING = "decision_gate_no_CMB_run_no_amplitude_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 180 decision script"),
        (WORK_DIR / "178-memory-perturbation-owner-attempt.md", "P06 effective owner checkpoint"),
        (CHECKPOINT_178_RUN / "status.json", "P06 effective owner status"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "P08 local screening checkpoint"),
        (CHECKPOINT_179_RUN / "status.json", "P08 local screening status"),
        (WORK_DIR / "150-Boltzmann-interface-contract.md", "Boltzmann interface contract"),
        (WORK_DIR / "151-CMB-kill-screen-runner-contract.md", "CMB kill-screen runner contract"),
        (CMB_CONTRACT_RUN / "status.json", "CMB kill-screen contract status"),
        (CMB_CONTRACT_RUN / "results" / "environment_preflight.csv", "CMB engine readiness preflight"),
        (CMB_CONTRACT_RUN / "results" / "kill_screen_run_matrix.csv", "CMB kill-screen branch matrix"),
        (WORK_DIR / "91-Bmem-p-u3-parent-ownership-gate.md", "p/u3/Bmem ownership checkpoint"),
        (WORK_DIR / "140-boundary-charge-amplitude-decision-gate.md", "2/27 amplitude decision gate"),
        (AMPLITUDE_RUN / "status.json", "amplitude decision status"),
        (AMPLITUDE_RUN / "results" / "factor_ownership_ledger.csv", "amplitude ownership factor ledger"),
        (OFFICIAL_DECISION_RUN / "results" / "promotion_requirement_matrix.csv", "active promotion blocker matrix"),
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


def environment_preflight_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "camb_python_module",
            "status": "available" if importlib.util.find_spec("camb") else "missing",
            "impact": "needed for CAMB-based spectra kill-screen",
        },
        {
            "item": "classy_python_module",
            "status": "available" if importlib.util.find_spec("classy") else "missing",
            "impact": "needed for CLASS Python wrapper kill-screen",
        },
        {
            "item": "class_executable",
            "status": "available" if shutil.which("class") else "missing",
            "impact": "needed for standalone CLASS kill-screen",
        },
        {
            "item": "cobaya_python_module",
            "status": "available" if importlib.util.find_spec("cobaya") else "missing",
            "impact": "useful for official likelihood plumbing",
        },
        {
            "item": "cmb_long_run_script",
            "status": "available" if (WORK_DIR / "scripts" / "cmb_kill_screen_long_run.py").exists() else "missing",
            "impact": "must exist before any dry-run or long spectra run",
        },
    ]


def blocker_state_rows() -> list[dict[str, Any]]:
    promotion_rows = read_csv_rows(OFFICIAL_DECISION_RUN / "results" / "promotion_requirement_matrix.csv")
    effects_178 = {row["gate_id"]: row for row in read_csv_rows(CHECKPOINT_178_RUN / "results" / "promotion_gate_effects.csv")}
    effects_179 = {row["gate_id"]: row for row in read_csv_rows(CHECKPOINT_179_RUN / "results" / "promotion_gate_effects.csv")}
    rows: list[dict[str, Any]] = []
    for row in promotion_rows:
        gate_id = row["gate_id"]
        if gate_id not in {"P04", "P06", "P07", "P08", "P09", "P10"}:
            continue
        effect_178 = effects_178.get(gate_id, {}).get("effect_of_checkpoint_178", "")
        effect_179 = effects_179.get(gate_id, {}).get("effect_of_checkpoint_179", "")
        if gate_id == "P06":
            revised = "partial_effective_not_parent_cleared"
        elif gate_id == "P08":
            revised = "screened_effective_not_parent_cleared"
        else:
            revised = "blocking"
        rows.append(
            {
                "gate_id": gate_id,
                "requirement": row["requirement"],
                "checkpoint_176_status": row["current_status"],
                "checkpoint_178_effect": effect_178,
                "checkpoint_179_effect": effect_179,
                "revised_status": revised,
                "next_pressure": next_pressure(gate_id),
            }
        )
    return rows


def next_pressure(gate_id: str) -> str:
    return {
        "P04": "parent action still needed, but not solved by immediate CMB or amplitude scoring",
        "P06": "effective owner now testable through CMB/growth machinery",
        "P07": "next empirical/theory kill-screen because spectra/lensing/ISW remain unrun",
        "P08": "safe effective local fence exists; keep open as derivation debt",
        "P09": "domain selector remains open, but old hidden-selector route is demoted",
        "P10": "amplitude remains empirical theorem target; no new parent mechanism since checkpoint 140",
    }[gate_id]


def option_scorecard_rows(env_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    engine_available = any(row["status"] == "available" for row in env_rows if row["item"] in {"camb_python_module", "classy_python_module", "class_executable"})
    runner_available = any(row["item"] == "cmb_long_run_script" and row["status"] == "available" for row in env_rows)
    return [
        {
            "option": "CMB_engine_readiness_then_kill_screen",
            "primary_gate": "P07",
            "theory_value": 8,
            "empirical_falsification_value": 10,
            "readiness": 6 if engine_available and runner_available else 4,
            "new_information_expected": 9,
            "overclaim_risk_if_guarded": 3,
            "reason": "P06/P08 now have effective fences, so spectra/lensing/ISW is the next honest pressure test; execution needs engine/wrapper first",
            "decision": "select_next",
        },
        {
            "option": "parent_Bmem_2over27_amplitude_owner_attempt",
            "primary_gate": "P10",
            "theory_value": 10,
            "empirical_falsification_value": 4,
            "readiness": 3,
            "new_information_expected": 5,
            "overclaim_risk_if_guarded": 5,
            "reason": "highest fundamental debt, but checkpoint 140 already found no parent arrow/charge unit; another attempt needs a genuinely new boundary-action idea",
            "decision": "defer_until_new_mechanism",
        },
        {
            "option": "return_to_broader_late_time_scoring",
            "primary_gate": "empirical_bookkeeping",
            "theory_value": 3,
            "empirical_falsification_value": 5,
            "readiness": 8,
            "new_information_expected": 3,
            "overclaim_risk_if_guarded": 4,
            "reason": "170-175 already reproduced the late-time/non-CMB card; more scoring does not remove promotion blockers",
            "decision": "defer",
        },
        {
            "option": "reopen_old_local_selector_route",
            "primary_gate": "P08/P09",
            "theory_value": 5,
            "empirical_falsification_value": 2,
            "readiness": 2,
            "new_information_expected": 2,
            "overclaim_risk_if_guarded": 8,
            "reason": "checkpoint 81 demoted the hidden-selector route; reopening it would violate current guardrails",
            "decision": "reject",
        },
    ]


def selected_work_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "engine_readiness",
            "required_artifact": "181-CMB-engine-readiness-and-dryrun-wrapper.md",
            "pass_condition": "detect available CLASS/CAMB route or write a no-run wrapper that fails cleanly with install instructions/status.json",
            "claim_limit": "no spectra, no CMB support claim",
        },
        {
            "step": "long_run_wrapper",
            "required_artifact": "scripts/cmb_kill_screen_long_run.py",
            "pass_condition": "supports --dry-run, writes run_config.json/log.txt/status.json/DONE or FAILED, and enforces B_mem,p,u3,c_s,sigma locks",
            "claim_limit": "tooling only until a real engine runs",
        },
        {
            "step": "baseline_parity",
            "required_artifact": "baseline_reproduction.csv",
            "pass_condition": "LCDM baseline reproduces configured spectra/likelihood before MTS result is read",
            "claim_limit": "pipeline validation, not MTS evidence",
        },
        {
            "step": "MTS_kill_screen",
            "required_artifact": "likelihood_scorecard.csv and claim_gate_results.csv",
            "pass_condition": "MTS exact-auxiliary/high-cs fixed branches are scored against the same baseline with no rescue knobs",
            "claim_limit": "survival/draw/fail only; no theory promotion",
        },
    ]


def deferred_amplitude_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "debt": "boundary_charge_unit",
            "needed_for_reopening": "derive Q_* normalization before data scoring",
            "current_status": "missing",
        },
        {
            "debt": "endpoint_coefficients",
            "needed_for_reopening": "derive coefficients 27 and 12 in 27R^2-12R+1=0 from a parent boundary action",
            "current_status": "formal_target_only",
        },
        {
            "debt": "endpoint_arrow",
            "needed_for_reopening": "derive the cosmological direction 1/3 -> 1/9 rather than relying on a formal potential with wrong stability direction",
            "current_status": "missing",
        },
        {
            "debt": "density_amplitude_map",
            "needed_for_reopening": "derive B_mem=DeltaR/3 from stress normalization or conserved charge",
            "current_status": "empirical_locked_closure",
        },
    ]


def risk_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "risk": "CMB engine unavailable",
            "mitigation": "next checkpoint is engine readiness/dry-run wrapper, not long spectra execution",
            "decision_effect": "does not block meaningful progress",
        },
        {
            "risk": "CMB compressed-distance confusion",
            "mitigation": "use spectra/lensing/ISW kill-screen contract, not compressed priors as support",
            "decision_effect": "prevents false CMB pass",
        },
        {
            "risk": "amplitude numerology loop",
            "mitigation": "defer P10 until a new boundary-charge mechanism exists",
            "decision_effect": "avoids re-proving 2/27 from itself",
        },
        {
            "risk": "baseline unfairness",
            "mitigation": "LCDM baseline reproduction and shared score bands are mandatory",
            "decision_effect": "keeps the boxing-card rule fair",
        },
        {
            "risk": "P06/P08 overpromotion",
            "mitigation": "label both as effective/screened, not parent-cleared",
            "decision_effect": "preserves claim ceiling",
        },
    ]


def acceptance_gate_rows(
    sources: list[dict[str, Any]],
    options: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    selected = [row for row in options if row["decision"] == "select_next"]
    p07_blocker = next(row for row in blockers if row["gate_id"] == "P07")
    p10_blocker = next(row for row in blockers if row["gate_id"] == "P10")
    return [
        {
            "gate": "all_cited_sources_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all registered paths found" if not missing else "; ".join(missing),
        },
        {
            "gate": "single_next_option_selected",
            "status": "pass" if len(selected) == 1 else "fail",
            "evidence": "; ".join(row["option"] for row in selected),
        },
        {
            "gate": "P07_remains_blocking",
            "status": "pass" if p07_blocker["revised_status"] == "blocking" else "fail",
            "evidence": p07_blocker["next_pressure"],
        },
        {
            "gate": "P10_deferred_not_promoted",
            "status": "pass" if p10_blocker["revised_status"] == "blocking" else "fail",
            "evidence": p10_blocker["next_pressure"],
        },
        {
            "gate": "no_CMB_run_performed",
            "status": "pass",
            "evidence": "decision only; spectra execution not attempted",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(env_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    engine_status = "; ".join(f"{row['item']}={row['status']}" for row in env_rows)
    return [
        {
            "item": "status",
            "verdict": STATUS_PASS,
            "evidence": "P07 is the next highest-value pressure test after P06/P08 effective screening",
        },
        {
            "item": "selected_next_route",
            "verdict": "CMB_engine_readiness_then_kill_screen",
            "evidence": "CMB spectra/lensing/ISW can now test the effective scalar closure; amplitude has no new owner mechanism",
        },
        {
            "item": "amplitude_route",
            "verdict": "defer_as_theorem_debt",
            "evidence": "B_mem=2/27 remains empirical locked closure until boundary-charge unit, endpoint arrow, and density map are derived",
        },
        {
            "item": "environment_snapshot",
            "verdict": engine_status,
            "evidence": "current readiness check; no installation or long run performed",
        },
        {
            "item": "promotion_allowed",
            "verdict": False,
            "evidence": "decision gate only; no CMB spectra, no parent amplitude derivation",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "private route-selection gate",
        },
        {
            "item": "next_target",
            "verdict": "181-CMB-engine-readiness-and-dryrun-wrapper.md",
            "evidence": "build or fail-cleanly preflight the long-run wrapper before any spectra execution",
        },
    ]


def run_decision(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-CMB-kill-screen-or-parent-amplitude-owner-decision"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    env = environment_preflight_rows()
    blockers = blocker_state_rows()
    options = option_scorecard_rows(env)
    selected_work = selected_work_contract_rows()
    amplitude_debt = deferred_amplitude_contract_rows()
    risks = risk_register_rows()
    gates = acceptance_gate_rows(sources, options, blockers)
    decisions = decision_rows(env)

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "purpose": "choose next route after checkpoint 178/179 effective screening",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "environment_preflight.csv", env, ["item", "status", "impact"])
    write_csv(
        results_dir / "post_179_blocker_state.csv",
        blockers,
        [
            "gate_id",
            "requirement",
            "checkpoint_176_status",
            "checkpoint_178_effect",
            "checkpoint_179_effect",
            "revised_status",
            "next_pressure",
        ],
    )
    write_csv(
        results_dir / "option_scorecard.csv",
        options,
        [
            "option",
            "primary_gate",
            "theory_value",
            "empirical_falsification_value",
            "readiness",
            "new_information_expected",
            "overclaim_risk_if_guarded",
            "reason",
            "decision",
        ],
    )
    write_csv(
        results_dir / "selected_CMB_next_work_contract.csv",
        selected_work,
        ["step", "required_artifact", "pass_condition", "claim_limit"],
    )
    write_csv(
        results_dir / "deferred_amplitude_theorem_debt.csv",
        amplitude_debt,
        ["debt", "needed_for_reopening", "current_status"],
    )
    write_csv(results_dir / "risk_register.csv", risks, ["risk", "mitigation", "decision_effect"])
    write_csv(results_dir / "acceptance_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": STATUS_PASS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "selected_next_route": "CMB_engine_readiness_then_kill_screen",
        "amplitude_route": "defer_as_theorem_debt",
        "promotion_allowed": False,
        "generated": [
            "source_register.csv",
            "environment_preflight.csv",
            "post_179_blocker_state.csv",
            "option_scorecard.csv",
            "selected_CMB_next_work_contract.csv",
            "deferred_amplitude_theorem_debt.csv",
            "risk_register.csv",
            "acceptance_gates.csv",
            "decision.csv",
        ],
        "next_target": "181-CMB-engine-readiness-and-dryrun-wrapper.md",
    }
    write_json(run_dir / "status.json", status)
    (run_dir / "DONE.txt").write_text(f"{STATUS_PASS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_decision(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
