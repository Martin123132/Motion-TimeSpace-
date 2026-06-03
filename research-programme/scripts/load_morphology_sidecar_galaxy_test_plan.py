#!/usr/bin/env python3
"""Checkpoint 216: no-fit load-morphology sidecar plan for future local/galaxy tests."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_216_NAME = "load-morphology-sidecar-galaxy-test-plan"
CHECKPOINT_215_RUN = RUNS_ROOT / "20260601-000032-QJrel-load-morphology-parent-owner-attempt"
CHECKPOINT_214_RUN = RUNS_ROOT / "20260601-000031-compact-vs-extended-load-invariant-attempt"

STATUS = "load_morphology_sidecar_plan_locked_no_fit_no_galaxy_repo_touch"
CLAIM_CEILING = "sidecar_plan_only_no_galaxy_local_or_field_theory_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 216 sidecar plan script"),
        (WORK_DIR / "215-QJrel-load-morphology-parent-owner-attempt.md", "Q/Jrel owner checkpoint"),
        (CHECKPOINT_215_RUN / "status.json", "checkpoint 215 machine status"),
        (CHECKPOINT_215_RUN / "results" / "owner_candidate_ledger.csv", "checkpoint 215 owner candidate ledger"),
        (CHECKPOINT_215_RUN / "results" / "parent_gap_ledger.csv", "checkpoint 215 parent gaps"),
        (WORK_DIR / "214-compact-vs-extended-load-invariant-attempt.md", "compact-vs-extended invariant checkpoint"),
        (CHECKPOINT_214_RUN / "results" / "proxy_profile_classification.csv", "checkpoint 214 proxy classification"),
        (WORK_DIR / "213-fixed-GK-domain-selector-contract.md", "domain selector contract checkpoint"),
        (WORK_DIR / "212-composite-GK-local-BAO-galaxy-safety-gate.md", "composite G_K safety gate"),
        (WORK_DIR / "01-motion-load-route-contract.md", "required local/cosmology/galaxy gate contract"),
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


def frozen_sidecar_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule_item": "load_score",
            "symbol": "E_L",
            "frozen_definition": "E_L=s80*(1+A_I)/2+F_edge",
            "status": "locked_from_checkpoint_214",
            "fit_permission": "no_fit",
            "notes": "weights are frozen for sidecar testing; not parent-derived",
        },
        {
            "rule_item": "compact_shell_class",
            "symbol": "compact_vacuum_shell",
            "frozen_definition": "vacuum_collar_fraction>0.5 and E_L<0.25",
            "status": "locked_from_checkpoint_214",
            "fit_permission": "no_fit",
            "notes": "intended for local PPN shell preclassification only",
        },
        {
            "rule_item": "extended_load_class",
            "symbol": "extended_load",
            "frozen_definition": "E_L>0.40 or F_edge>0.05",
            "status": "locked_from_checkpoint_214",
            "fit_permission": "no_fit",
            "notes": "intended for galaxy/load-domain preclassification only",
        },
        {
            "rule_item": "ambiguous_class",
            "symbol": "ambiguous",
            "frozen_definition": "not compact_vacuum_shell and not extended_load",
            "status": "locked_from_checkpoint_214",
            "fit_permission": "no_fit",
            "notes": "ambiguous cases must be flagged, not forced into favorable bins",
        },
        {
            "rule_item": "edge_owner",
            "symbol": "F_edge",
            "frozen_definition": "outer-collar load/current proxy until J_rel is derived",
            "status": "closure_only",
            "fit_permission": "no_fit",
            "notes": "cannot be adjusted from galaxy residuals",
        },
    ]


def sidecar_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "column": "object_id",
            "required": "yes",
            "type": "string",
            "source": "catalog identifier",
            "may_use_rotation_residuals": "no",
            "notes": "join key only",
        },
        {
            "column": "domain_radius_kpc",
            "required": "yes",
            "type": "float",
            "source": "predeclared photometric/load-domain radius or local shell radius",
            "may_use_rotation_residuals": "no",
            "notes": "must be fixed before scoring",
        },
        {
            "column": "s80_r80_over_RD",
            "required": "yes",
            "type": "float",
            "source": "load/matter support cumulative profile",
            "may_use_rotation_residuals": "no",
            "notes": "radius enclosing 80 percent support divided by domain radius",
        },
        {
            "column": "s99_r99_over_RD",
            "required": "yes",
            "type": "float",
            "source": "load/matter support cumulative profile",
            "may_use_rotation_residuals": "no",
            "notes": "sets vacuum_collar_fraction=max(0,1-s99)",
        },
        {
            "column": "A_I",
            "required": "yes",
            "type": "float",
            "source": "support inertia tensor or axis-ratio proxy",
            "may_use_rotation_residuals": "no",
            "notes": "dimensionless load anisotropy",
        },
        {
            "column": "F_edge",
            "required": "yes",
            "type": "float",
            "source": "outer-collar load fraction or predeclared J_rel proxy",
            "may_use_rotation_residuals": "no",
            "notes": "edge/current term; closure until J_rel is derived",
        },
        {
            "column": "E_L",
            "required": "computed",
            "type": "float",
            "source": "sidecar formula",
            "may_use_rotation_residuals": "no",
            "notes": "E_L=s80*(1+A_I)/2+F_edge",
        },
        {
            "column": "morphology_class",
            "required": "computed",
            "type": "enum",
            "source": "sidecar formula",
            "may_use_rotation_residuals": "no",
            "notes": "compact_vacuum_shell, extended_load, or ambiguous",
        },
        {
            "column": "quality_flag",
            "required": "yes",
            "type": "enum",
            "source": "input data completeness",
            "may_use_rotation_residuals": "no",
            "notes": "complete, missing_profile, extrapolated, ambiguous_domain",
        },
    ]


def no_fit_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy": "no residual access",
            "rule": "sidecar classification must be computed before reading galaxy/local fit residuals",
            "failure_if_broken": "post-hoc selector",
        },
        {
            "policy": "no threshold tuning",
            "rule": "0.25, 0.40, 0.50, and 0.05 thresholds stay fixed for first sidecar test",
            "failure_if_broken": "hidden fit knob",
        },
        {
            "policy": "no galaxy repo mutation",
            "rule": "sidecar files are generated under post-checkpoint-work/runs only; galaxy-work and MTS-Galaxy-Lab remain read-only",
            "failure_if_broken": "scope violation",
        },
        {
            "policy": "ambiguous means ambiguous",
            "rule": "ambiguous objects must be reported separately and not assigned to the favorable branch",
            "failure_if_broken": "selection bias",
        },
        {
            "policy": "baseline comparison",
            "rule": "if MTS is jackknifed or split-tested, comparable baselines must be split-tested where the baseline can meaningfully run",
            "failure_if_broken": "unfair scoring",
        },
    ]


def galaxy_test_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "phase": "G0_schema_dryrun",
            "action": "validate sidecar schema on a tiny hand/manifest sample before any fit join",
            "input": "object_id plus predeclared support-profile columns",
            "output": "sidecar rows with E_L and morphology_class",
            "pass_condition": "all required columns present; no residual columns read",
        },
        {
            "phase": "G1_read_only_join",
            "action": "join sidecar classifications to existing galaxy result tables without changing galaxy code",
            "input": "existing galaxy outputs plus sidecar CSV",
            "output": "stratified diagnostics by compact/extended/ambiguous class",
            "pass_condition": "join keys match; raw galaxy results unchanged",
        },
        {
            "phase": "G2_stratified_residual_audit",
            "action": "check whether extended_load class carries the expected galaxy signal while compact/ambiguous classes are not used as wins",
            "input": "joined diagnostics",
            "output": "class-by-class residual and outlier table",
            "pass_condition": "no claim from ambiguous objects; failures trigger theory audit not threshold tuning",
        },
        {
            "phase": "G3_fair_baseline_split",
            "action": "apply comparable split/jackknife to baselines that can accept the same object partitions",
            "input": "same sidecar partition",
            "output": "baseline-vs-MTS split card",
            "pass_condition": "baseline failures are reported, not silently ignored",
        },
    ]


def local_test_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "phase": "L0_shell_manifest",
            "action": "define local shell cases and support inputs before PPN residual calculation",
            "input": "Sun/Earth compact profiles and shell radii",
            "output": "compact_vacuum_shell sidecar classifications",
            "pass_condition": "local cases classify compact without using PPN residuals",
        },
        {
            "phase": "L1_q_loc_proxy",
            "action": "combine compact class with fixed G_K/local gradient proxy to estimate q_loc residual vector",
            "input": "sidecar class plus fixed G_K branch",
            "output": "gamma-1, beta-1, q_loc proxy ledger",
            "pass_condition": "no plateau axiom; q_loc row remains explicit if not derived",
        },
        {
            "phase": "L2_baseline_GR_control",
            "action": "record GR baseline as exact local control where applicable",
            "input": "standard local observables",
            "output": "MTS residual compared to GR control",
            "pass_condition": "MTS does not receive easier gates than GR/control baselines",
        },
    ]


def failure_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "failure": "sidecar flips many known extended galaxies to ambiguous/compact",
            "interpretation": "morphology invariant likely wrong or unsupported by available data",
            "response": "do not retune thresholds; inspect load measure/domain definition",
        },
        {
            "failure": "sidecar class strongly tracks residual sign after threshold changes",
            "interpretation": "post-hoc selection risk",
            "response": "discard tuned branch; revert to frozen thresholds",
        },
        {
            "failure": "compact local shells classify extended",
            "interpretation": "support profile or shell-domain definition is inconsistent",
            "response": "audit domain radius and dmu_L definition before local claims",
        },
        {
            "failure": "MTS only improves after excluding ambiguous objects",
            "interpretation": "possible selection bias",
            "response": "report both full and stratified results; no public support claim",
        },
        {
            "failure": "baseline and MTS respond differently to same sidecar split",
            "interpretation": "could be real or pipeline artifact",
            "response": "run fair baseline split diagnostics before theory interpretation",
        },
    ]


def dryrun_command_rows() -> list[dict[str, Any]]:
    return [
        {
            "name": "future_schema_dryrun",
            "command": "python scripts/load_morphology_sidecar_builder.py --input <profile_manifest.csv> --output runs/<timestamp>/sidecar.csv --dry-run",
            "allowed_now": "no",
            "reason": "builder not implemented; this checkpoint only locks the contract",
        },
        {
            "name": "future_read_only_join",
            "command": "python scripts/load_morphology_sidecar_join.py --sidecar <sidecar.csv> --galaxy-results <existing-results.csv> --read-only",
            "allowed_now": "no",
            "reason": "join script deferred; must not modify galaxy repo",
        },
        {
            "name": "future_local_manifest",
            "command": "python scripts/load_morphology_local_shell_manifest.py --output runs/<timestamp>/local_shell_sidecar.csv --dry-run",
            "allowed_now": "no",
            "reason": "local q_loc residual calculation is not yet implemented",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal sidecar planning",
        },
        {
            "gate": "sidecar formula frozen",
            "status": "pass",
            "evidence": "E_L and class thresholds locked from checkpoint 214",
            "claim_allowed": "future no-fit dryrun",
        },
        {
            "gate": "no galaxy repo mutation",
            "status": "pass",
            "evidence": "plan writes only post-checkpoint run artifacts",
            "claim_allowed": "scope-safe plan",
        },
        {
            "gate": "input schema specified",
            "status": "pass",
            "evidence": "required columns and no-residual rule defined",
            "claim_allowed": "schema contract",
        },
        {
            "gate": "actual SPARC/ETG data run",
            "status": "not_run",
            "evidence": "deferred by design",
            "claim_allowed": "no galaxy evidence claim",
        },
        {
            "gate": "local q_loc/PPN residual run",
            "status": "not_run",
            "evidence": "deferred by design",
            "claim_allowed": "no local GR promotion",
        },
        {
            "gate": "sidecar promoted as parent theory",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The load-morphology invariant is now locked as a future no-fit sidecar plan. It specifies frozen thresholds, required input columns, no-residual/no-threshold-tuning policy, read-only galaxy integration, local shell manifest requirements, and fair-baseline split rules. No SPARC/ETG/local run has been made and no promotion is allowed.",
            "main_gain": "the bridge from theory closure to future empirical testing is now disciplined and precommitted",
            "main_failure": "builder/join scripts and real data runs are deferred; parent derivation still missing",
            "next_target": "217-load-morphology-sidecar-builder-dryrun.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_216_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    frozen_rows = frozen_sidecar_rule_rows()
    schema_rows = sidecar_schema_rows()
    policy_rows = no_fit_policy_rows()
    galaxy_rows = galaxy_test_plan_rows()
    local_rows = local_test_plan_rows()
    failure_rows = failure_mode_rows()
    command_rows = dryrun_command_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "frozen_sidecar_rules.csv": (
            frozen_rows,
            ["rule_item", "symbol", "frozen_definition", "status", "fit_permission", "notes"],
        ),
        "sidecar_input_schema.csv": (
            schema_rows,
            ["column", "required", "type", "source", "may_use_rotation_residuals", "notes"],
        ),
        "no_fit_policy.csv": (
            policy_rows,
            ["policy", "rule", "failure_if_broken"],
        ),
        "galaxy_test_plan.csv": (
            galaxy_rows,
            ["phase", "action", "input", "output", "pass_condition"],
        ),
        "local_test_plan.csv": (
            local_rows,
            ["phase", "action", "input", "output", "pass_condition"],
        ),
        "failure_modes.csv": (
            failure_rows,
            ["failure", "interpretation", "response"],
        ),
        "future_dryrun_commands.csv": (
            command_rows,
            ["name", "command", "allowed_now", "reason"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "sidecar_formula_frozen": True,
        "input_schema_specified": True,
        "no_fit_policy_locked": True,
        "galaxy_repo_mutated": False,
        "actual_galaxy_data_run": False,
        "local_PPN_residual_run": False,
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
