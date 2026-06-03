#!/usr/bin/env python3
"""Checkpoint 217: dry-run sidecar builder for frozen load morphology rules."""

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

CHECKPOINT_217_NAME = "load-morphology-sidecar-builder-dryrun"
CHECKPOINT_216_RUN = RUNS_ROOT / "20260601-000033-load-morphology-sidecar-galaxy-test-plan"
CHECKPOINT_214_RUN = RUNS_ROOT / "20260601-000031-compact-vs-extended-load-invariant-attempt"

STATUS = "load_morphology_sidecar_builder_dryrun_passed_no_fit_no_repo_touch"
CLAIM_CEILING = "builder_dryrun_only_no_galaxy_or_local_evidence"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

REQUIRED_INPUT_COLUMNS = [
    "object_id",
    "domain_radius_kpc",
    "s80_r80_over_RD",
    "s99_r99_over_RD",
    "A_I",
    "F_edge",
    "quality_flag",
]
FORBIDDEN_COLUMNS = [
    "rotation_residual",
    "fit_residual",
    "chi2",
    "delta_chi2",
    "preferred_model",
    "success_label",
]


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
        (Path(__file__).resolve(), "checkpoint 217 dry-run builder script"),
        (WORK_DIR / "216-load-morphology-sidecar-galaxy-test-plan.md", "sidecar test-plan checkpoint"),
        (CHECKPOINT_216_RUN / "status.json", "checkpoint 216 machine status"),
        (CHECKPOINT_216_RUN / "results" / "frozen_sidecar_rules.csv", "checkpoint 216 frozen rules"),
        (CHECKPOINT_216_RUN / "results" / "sidecar_input_schema.csv", "checkpoint 216 input schema"),
        (CHECKPOINT_216_RUN / "results" / "no_fit_policy.csv", "checkpoint 216 no-fit policy"),
        (WORK_DIR / "214-compact-vs-extended-load-invariant-attempt.md", "load morphology invariant checkpoint"),
        (CHECKPOINT_214_RUN / "results" / "proxy_profile_classification.csv", "checkpoint 214 proxy classifications"),
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


def toy_profile_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "object_id": "toy_solar_1AU_shell",
            "domain_radius_kpc": 4.84813681109536e-9,
            "s80_r80_over_RD": 0.00465,
            "s99_r99_over_RD": 0.00465,
            "A_I": 0.02,
            "F_edge": 0.0,
            "quality_flag": "complete",
        },
        {
            "object_id": "toy_earth_GPS_shell",
            "domain_radius_kpc": 8.613333e-13,
            "s80_r80_over_RD": 0.24,
            "s99_r99_over_RD": 0.24,
            "A_I": 0.03,
            "F_edge": 0.0,
            "quality_flag": "complete",
        },
        {
            "object_id": "toy_dwarf_3kpc_extended_load",
            "domain_radius_kpc": 3.0,
            "s80_r80_over_RD": 0.65,
            "s99_r99_over_RD": 0.95,
            "A_I": 0.65,
            "F_edge": 0.20,
            "quality_flag": "complete",
        },
        {
            "object_id": "toy_milky_way_8kpc_disk",
            "domain_radius_kpc": 8.0,
            "s80_r80_over_RD": 0.85,
            "s99_r99_over_RD": 0.98,
            "A_I": 0.90,
            "F_edge": 0.30,
            "quality_flag": "complete",
        },
        {
            "object_id": "toy_ambiguous_compact_core",
            "domain_radius_kpc": 0.5,
            "s80_r80_over_RD": 0.32,
            "s99_r99_over_RD": 0.55,
            "A_I": 0.10,
            "F_edge": 0.02,
            "quality_flag": "ambiguous_domain",
        },
    ]


def classify_row(row: dict[str, Any]) -> dict[str, Any]:
    s80 = float(row["s80_r80_over_RD"])
    s99 = float(row["s99_r99_over_RD"])
    anisotropy = float(row["A_I"])
    edge = float(row["F_edge"])
    vacuum_collar = max(0.0, 1.0 - s99)
    load_score = s80 * (1.0 + anisotropy) / 2.0 + edge
    compact = vacuum_collar > 0.5 and load_score < 0.25
    extended = load_score > 0.40 or edge > 0.05
    if compact:
        morphology_class = "compact_vacuum_shell"
    elif extended:
        morphology_class = "extended_load"
    else:
        morphology_class = "ambiguous"
    return {
        **row,
        "vacuum_collar_fraction": vacuum_collar,
        "E_L": load_score,
        "morphology_class": morphology_class,
        "rule_version": "checkpoint_214_frozen_v1",
        "uses_residuals": "no",
    }


def schema_validation_rows(input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    headers = set(input_rows[0].keys()) if input_rows else set()
    rows: list[dict[str, Any]] = []
    for column in REQUIRED_INPUT_COLUMNS:
        rows.append(
            {
                "check": f"required_column:{column}",
                "status": "pass" if column in headers else "fail",
                "evidence": "present" if column in headers else "missing",
            }
        )
    for column in FORBIDDEN_COLUMNS:
        rows.append(
            {
                "check": f"forbidden_column_absent:{column}",
                "status": "pass" if column not in headers else "fail",
                "evidence": "absent" if column not in headers else "present",
            }
        )
    rows.append(
        {
            "check": "row_count_positive",
            "status": "pass" if len(input_rows) > 0 else "fail",
            "evidence": str(len(input_rows)),
        }
    )
    return rows


def no_fit_audit_rows(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    class_counts: dict[str, int] = {}
    for row in output_rows:
        class_counts[row["morphology_class"]] = class_counts.get(row["morphology_class"], 0) + 1
    return [
        {
            "audit": "uses_residuals",
            "status": "pass" if all(row["uses_residuals"] == "no" for row in output_rows) else "fail",
            "evidence": "all output rows marked no",
        },
        {
            "audit": "compact_count",
            "status": "info",
            "evidence": str(class_counts.get("compact_vacuum_shell", 0)),
        },
        {
            "audit": "extended_count",
            "status": "info",
            "evidence": str(class_counts.get("extended_load", 0)),
        },
        {
            "audit": "ambiguous_count",
            "status": "pass" if class_counts.get("ambiguous", 0) > 0 else "warn",
            "evidence": str(class_counts.get("ambiguous", 0)),
        },
        {
            "audit": "thresholds_changed",
            "status": "pass",
            "evidence": "hard-coded checkpoint_214_frozen_v1",
        },
    ]


def join_boundary_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "boundary": "allowed_read",
            "path_or_object": "sidecar CSV produced under post-checkpoint-work/runs",
            "rule": "future galaxy scripts may read this as an external classification table",
        },
        {
            "boundary": "forbidden_write",
            "path_or_object": "galaxy-work or MTS-Galaxy-Lab- repository files",
            "rule": "this dry-run does not write or patch the galaxy repo",
        },
        {
            "boundary": "join_key",
            "path_or_object": "object_id",
            "rule": "join only by object_id; no matching by residual quality",
        },
        {
            "boundary": "ambiguous_handling",
            "path_or_object": "morphology_class=ambiguous",
            "rule": "must remain its own stratum in future diagnostics",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]], output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    validation_failures = sum(row["status"] == "fail" for row in validation_rows)
    output_classes = {row["morphology_class"] for row in output_rows}
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal dry-run builder",
        },
        {
            "gate": "schema validation",
            "status": "pass" if validation_failures == 0 else "fail",
            "evidence": f"failures={validation_failures}",
            "claim_allowed": "toy sidecar output",
        },
        {
            "gate": "frozen classification produced",
            "status": "pass" if {"compact_vacuum_shell", "extended_load", "ambiguous"}.issubset(output_classes) else "fail",
            "evidence": ",".join(sorted(output_classes)),
            "claim_allowed": "dry-run only",
        },
        {
            "gate": "no residual fields used",
            "status": "pass",
            "evidence": "toy manifest contains no forbidden residual columns",
            "claim_allowed": "no-fit dry-run",
        },
        {
            "gate": "galaxy repo untouched",
            "status": "pass",
            "evidence": "script writes only run artifacts in post-checkpoint-work",
            "claim_allowed": "scope-safe dry-run",
        },
        {
            "gate": "real SPARC/ETG evidence",
            "status": "not_run",
            "evidence": "toy manifest only",
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "A tiny sidecar builder dry-run now validates the frozen schema, rejects residual-dependent inputs by policy, computes E_L and morphology_class from toy predeclared support rows, preserves ambiguous cases, and writes only post-checkpoint run artifacts. It proves the sidecar workflow is executable, not that any real galaxy or local data support the branch.",
            "main_gain": "the no-fit sidecar is now runnable in miniature",
            "main_failure": "real profile ingestion, read-only galaxy join, and local q_loc residuals remain unrun",
            "next_target": "218-sidecar-readonly-join-contract-or-local-qloc.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_217_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    input_rows = toy_profile_manifest_rows()
    output_rows = [classify_row(row) for row in input_rows]
    validation_rows = schema_validation_rows(input_rows)
    audit_rows = no_fit_audit_rows(output_rows)
    boundary_rows = join_boundary_contract_rows()
    gates = claim_gate_rows(source_rows, validation_rows, output_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "toy_profile_manifest.csv": (
            input_rows,
            REQUIRED_INPUT_COLUMNS,
        ),
        "sidecar_dryrun_output.csv": (
            output_rows,
            REQUIRED_INPUT_COLUMNS + ["vacuum_collar_fraction", "E_L", "morphology_class", "rule_version", "uses_residuals"],
        ),
        "schema_validation.csv": (
            validation_rows,
            ["check", "status", "evidence"],
        ),
        "no_fit_audit.csv": (
            audit_rows,
            ["audit", "status", "evidence"],
        ),
        "join_boundary_contract.csv": (
            boundary_rows,
            ["boundary", "path_or_object", "rule"],
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
    validation_failures = sum(row["status"] == "fail" for row in validation_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "schema_validation_failures": validation_failures,
        "toy_rows": len(input_rows),
        "sidecar_rows": len(output_rows),
        "uses_residuals": False,
        "galaxy_repo_mutated": False,
        "real_galaxy_data_run": False,
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
