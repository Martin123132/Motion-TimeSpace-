#!/usr/bin/env python3
"""Checkpoint 249: projector boundary-only condition or metric-only reduction fail."""

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

CHECKPOINT_249_NAME = "projector-boundary-only-condition-or-metric-only-reduction-fail"
RUN_248 = RUNS_ROOT / "20260601-000065-projector-stress-zero-or-retained-theorem"

STATUS = "projector_boundary_only_condition_not_derived_bulk_projector_stress_blocks_metric_only_EH_no_promotion"
CLAIM_CEILING = "N5_boundary_only_not_derived_metric_only_EH_blocked_no_beta_or_local_GR_promotion"
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
        (Path(__file__).resolve(), "checkpoint 249 runner"),
        (WORK_DIR / "231-Jrel-cohomology-projector-or-local-EH-limit.md", "relative exactness topology gate"),
        (WORK_DIR / "233-boundary-symplectic-metric-or-local-EH-operator.md", "boundary metric candidate"),
        (WORK_DIR / "245-exact-relative-memory-or-projector-stress-bianchi.md", "N4/N5 Bianchi trap"),
        (WORK_DIR / "248-projector-stress-zero-or-retained-theorem.md", "N5 zero/retained fork"),
        (RUN_248 / "status.json", "checkpoint 248 machine status"),
        (RUN_248 / "results" / "EH_stack_implication_after_248.csv", "EH implication table after N5 fork"),
        (RUN_248 / "results" / "zero_stress_route_tests.csv", "zero-stress route tests"),
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


def boundary_only_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "bulk_projected_current_zero",
            "mathematical_form": "P_mem J_rel = d_rel A_rel with A_rel pure gauge and no bulk support",
            "needed_for": "relative-memory contribution is boundary-only",
            "current_status": "conditional_not_parent_derived",
            "failure_mode": "exact current still leaves metric-dependent bulk variation",
        },
        {
            "condition": "bulk_projector_variation_zero",
            "mathematical_form": "delta_g P_mem|bulk = 0",
            "needed_for": "projector stress has no bulk support",
            "current_status": "not_derived",
            "failure_mode": "metric-dependent projector changes exterior equations",
        },
        {
            "condition": "bulk_boundary_metric_variation_zero",
            "mathematical_form": "delta_g B|bulk = 0",
            "needed_for": "boundary/Hodge metric is not an external bulk force",
            "current_status": "not_derived",
            "failure_mode": "orthogonality metric carries hidden stress",
        },
        {
            "condition": "removed_blocks_owned_or_zero",
            "mathematical_form": "delta Pi_M, delta Pi_TF, delta Pi_matter are zero or carried by owned boundary terms",
            "needed_for": "P_mem complement does not hide deleted-sector stress",
            "current_status": "conditional_open",
            "failure_mode": "mass/shear/matter projector stress leaks into bulk",
        },
        {
            "condition": "well_posed_boundary_variation",
            "mathematical_form": "delta S_projector|bulk = 0 and delta S_projector = delta S_boundary on partial E",
            "needed_for": "EH bulk plus boundary term remains valid",
            "current_status": "not_derived",
            "failure_mode": "boundary-only claim is variationally incomplete",
        },
    ]


def bulk_boundary_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece": "relative_exact_current",
            "bulk_status_if_condition_holds": "zero_or_exact_total_derivative",
            "boundary_status_if_condition_holds": "A_rel boundary primitive",
            "current_verdict": "conditional_helpful",
            "EH_effect": "not enough alone",
        },
        {
            "piece": "boundary_metric_B",
            "bulk_status_if_condition_holds": "metric-independent/topological",
            "boundary_status_if_condition_holds": "fixed induced boundary functional",
            "current_verdict": "not_derived",
            "EH_effect": "blocks metric-only if bulk dependent",
        },
        {
            "piece": "projector_variation_delta_Pmem",
            "bulk_status_if_condition_holds": "zero",
            "boundary_status_if_condition_holds": "owned by boundary symplectic variation",
            "current_verdict": "not_derived",
            "EH_effect": "blocks metric-only if bulk dependent",
        },
        {
            "piece": "removed_sector_variations",
            "bulk_status_if_condition_holds": "zero by N1/N2/N3 or separately retained",
            "boundary_status_if_condition_holds": "M_eff/shear/matter ledgers",
            "current_verdict": "conditional_open",
            "EH_effect": "requires parent owners",
        },
        {
            "piece": "bulk_T_projector",
            "bulk_status_if_condition_holds": "absent",
            "boundary_status_if_condition_holds": "boundary-only term",
            "current_verdict": "not_cleared",
            "EH_effect": "metric-only EH blocked until absent",
        },
    ]


def metric_only_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "boundary_only_projector_stress_derived",
            "bulk_equation": "G_mu_nu + Lambda g_mu_nu = 0 in E",
            "boundary_equation": "well-posed boundary projector variation",
            "metric_only_EH_status": "can_continue",
            "current_status": "not_derived",
        },
        {
            "case": "bulk_projector_stress_present",
            "bulk_equation": "G_mu_nu + Lambda g_mu_nu = 8 pi G T_projector_mu_nu",
            "boundary_equation": "may still be Bianchi-consistent",
            "metric_only_EH_status": "fails_metric_only_reduction",
            "current_status": "cannot_be_used_for_local_GR_promotion",
        },
        {
            "case": "projector_stress_dropped",
            "bulk_equation": "fake vacuum equation",
            "boundary_equation": "missing variation",
            "metric_only_EH_status": "invalid",
            "current_status": "rejected",
        },
        {
            "case": "current_checkpoint_verdict",
            "bulk_equation": "boundary-only condition not proved",
            "boundary_equation": "boundary primitive not parent-selected",
            "metric_only_EH_status": "blocked_not_dead",
            "current_status": "open theorem target",
        },
    ]


def local_branch_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "N5_projector_stress",
            "status_after_249": "blocked_until_boundary_only_or_zero",
            "meaning": "bulk projector stress is incompatible with metric-only EH",
            "next_action": "derive delta_g P_mem|bulk=0 or mark modified exterior branch",
        },
        {
            "gate": "N4_exact_relative_memory",
            "status_after_249": "still_conditional_helpful",
            "meaning": "exactness supports boundary-only route but does not prove stress localization",
            "next_action": "derive A_rel pure-gauge boundary representative",
        },
        {
            "gate": "metric_only_EH_exterior",
            "status_after_249": "blocked_by_N5",
            "meaning": "EH stack cannot be promoted while T_projector may be bulk",
            "next_action": "resolve N5 before beta/local GR promotion",
        },
        {
            "gate": "N6_auxiliary_nohair",
            "status_after_249": "unchanged_open",
            "meaning": "auxiliary hair still blocks metric-only exterior separately",
            "next_action": "return after parent symplectic structure or EH stack stabilization",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "boundary-only condition written",
            "status": "pass",
            "evidence": "bulk current, projector variation, boundary metric, and boundary variation conditions listed",
            "claim_allowed": "theorem target only",
        },
        {
            "gate": "projector stress boundary-only derived",
            "status": "fail",
            "evidence": "delta_g P_mem|bulk and A_rel boundary representative not parent-derived",
            "claim_allowed": "no",
        },
        {
            "gate": "metric-only EH reduction cleared",
            "status": "fail",
            "evidence": "bulk projector stress not excluded",
            "claim_allowed": "no",
        },
        {
            "gate": "metric-only reduction fail condition recorded",
            "status": "pass",
            "evidence": "bulk T_projector implies modified exterior, not vacuum EH",
            "claim_allowed": "negative gate only",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The condition for projector stress to be compatible with metric-only EH is now exact: it must be zero or boundary-only in the bulk exterior. Exact relative memory helps, but it does not prove the boundary-only claim because the projector metric, projector variation, and boundary primitive remain parent-unowned. Therefore metric-only EH reduction is blocked by N5 unless the next theorem proves T_projector has no bulk support.",
            "main_gain": "N5 is no longer vague: bulk projector stress explicitly means modified exterior rather than local GR",
            "main_failure": "boundary-only projector stress is not derived",
            "next_target": "250-local-GR-gate-scorecard-and-test-readiness.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_249_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    condition_rows = boundary_only_condition_rows()
    decomposition_rows = bulk_boundary_decomposition_rows()
    verdict_rows = metric_only_verdict_rows()
    update_rows = local_branch_update_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "boundary_only_conditions.csv": (
            condition_rows,
            ["condition", "mathematical_form", "needed_for", "current_status", "failure_mode"],
        ),
        "bulk_boundary_decomposition.csv": (
            decomposition_rows,
            ["piece", "bulk_status_if_condition_holds", "boundary_status_if_condition_holds", "current_verdict", "EH_effect"],
        ),
        "metric_only_reduction_verdict.csv": (
            verdict_rows,
            ["case", "bulk_equation", "boundary_equation", "metric_only_EH_status", "current_status"],
        ),
        "local_branch_update_after_249.csv": (
            update_rows,
            ["gate", "status_after_249", "meaning", "next_action"],
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
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": sum(row["exists"] != "yes" for row in source_rows),
        "boundary_only_condition_written": True,
        "projector_stress_boundary_only_derived": False,
        "metric_only_EH_reduction_cleared": False,
        "bulk_projector_stress_blocks_metric_only_EH": True,
        "local_GR_promoted": False,
        "PPN_promoted": False,
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
    print(json.dumps(run(args.timestamp), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
