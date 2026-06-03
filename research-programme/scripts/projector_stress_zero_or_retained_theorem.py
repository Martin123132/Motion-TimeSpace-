#!/usr/bin/env python3
"""Checkpoint 248: projector-stress zero or retained theorem."""

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

CHECKPOINT_248_NAME = "projector-stress-zero-or-retained-theorem"
RUN_247 = RUNS_ROOT / "20260601-000064-local-EH-exterior-sufficiency-stack-no-promotion"

STATUS = "projector_stress_zero_route_not_derived_retained_Bianchi_ledger_written_metric_only_gate_open_no_promotion"
CLAIM_CEILING = "N5_projector_stress_fork_no_metric_only_EH_beta_or_local_GR_promotion"
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
        (Path(__file__).resolve(), "checkpoint 248 runner"),
        (WORK_DIR / "234-boundary-metric-variation-and-Bianchi-ledger.md", "projector stress ledger"),
        (WORK_DIR / "235-projector-stress-variation-or-nohair-constraint-algebra.md", "projector variation split"),
        (WORK_DIR / "245-exact-relative-memory-or-projector-stress-bianchi.md", "N4/N5 exactness and Bianchi trap"),
        (WORK_DIR / "247-local-EH-exterior-sufficiency-stack-no-promotion.md", "EH stack with N5 open"),
        (RUN_247 / "status.json", "checkpoint 247 machine status"),
        (RUN_247 / "results" / "EH_premise_status_table.csv", "EH premise status before N5"),
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


def variation_term_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "delta_boundary_metric_B",
            "schematic_variation": "1/2 <J, delta_g B P_mem J>",
            "stress_owner": "T_boundary_metric",
            "zero_route_requirement": "B is topological/metric-independent or current support is pure boundary zero",
            "retained_route_requirement": "vary B and include its stress in T_total",
            "status_after_248": "open",
        },
        {
            "term": "delta_Pi_M",
            "schematic_variation": "-1/2 <J, B delta_g Pi_M J>",
            "stress_owner": "T_Meff + T_projector_M",
            "zero_route_requirement": "Pi_M is fixed harmonic class with conserved M_eff and no radial profile",
            "retained_route_requirement": "include monopole/projector variation stress",
            "status_after_248": "conditional_N1_plus_parent_gap",
        },
        {
            "term": "delta_Pi_TF",
            "schematic_variation": "-1/2 <J, B delta_g Pi_TF J>",
            "stress_owner": "T_TF + T_projector_TF",
            "zero_route_requirement": "N2 scalar-boundary theorem sets TF sector to zero",
            "retained_route_requirement": "include anisotropic stress explicitly",
            "status_after_248": "conditional_N2",
        },
        {
            "term": "delta_Pi_matter",
            "schematic_variation": "-1/2 <J, B delta_g Pi_matter J>",
            "stress_owner": "T_matter_vertex + T_projector_matter",
            "zero_route_requirement": "N3 strict coframe forbids direct matter block",
            "retained_route_requirement": "include direct coupling stress, which would break WEP route",
            "status_after_248": "conditional_N3",
        },
        {
            "term": "delta_Pmem_relative",
            "schematic_variation": "1/2 <J, B delta_g P_mem J> in relative sector",
            "stress_owner": "T_rel + T_projector_rel + T_boundary",
            "zero_route_requirement": "N4 exact pure-gauge relative current makes bulk support vanish",
            "retained_route_requirement": "include relative/projector/boundary stress",
            "status_after_248": "open",
        },
        {
            "term": "delta_Arel_boundary",
            "schematic_variation": "boundary variation of A_rel and primitive choice",
            "stress_owner": "T_boundary_Arel",
            "zero_route_requirement": "A_rel is pure gauge on boundary",
            "retained_route_requirement": "retain boundary exchange stress",
            "status_after_248": "open",
        },
    ]


def zero_route_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "projector_metric_independent",
            "required_for_zero_stress": "delta_g B = 0 and delta_g P_mem = 0 in exterior",
            "current_evidence": "boundary Hodge/DeWitt metric is metric-dependent candidate",
            "status": "fail_not_derived",
            "readout": "zero route cannot rely on fixed external projector metric",
        },
        {
            "test": "projected_current_bulk_zero",
            "required_for_zero_stress": "P_mem J_rel=dA_rel with pure-gauge/boundary-only support",
            "current_evidence": "N4 conditional exactness only",
            "status": "conditional_open",
            "readout": "helps but does not kill metric variation by itself",
        },
        {
            "test": "removed_blocks_zero_or_owned",
            "required_for_zero_stress": "Pi_M/Pi_TF/Pi_matter variations vanish by N1/N2/N3",
            "current_evidence": "N1-N3 are conditional, not parent-owned",
            "status": "conditional_open",
            "readout": "zero route depends on earlier gates becoming parent theorems",
        },
        {
            "test": "boundary_primitive_pure_gauge",
            "required_for_zero_stress": "A_rel boundary variation is gauge/cancelled",
            "current_evidence": "representative not selected",
            "status": "fail_not_derived",
            "readout": "boundary stress can still carry memory hair",
        },
        {
            "test": "zero_route_verdict",
            "required_for_zero_stress": "all zero-stress tests pass together",
            "current_evidence": "multiple open/fail rows",
            "status": "not_derived",
            "readout": "T_projector=0 is not earned in the current corpus",
        },
    ]


def retained_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "stress": "T_metric",
            "origin": "variation of metric-only exterior action",
            "retained_identity_role": "baseline gravitational Bianchi term",
            "EH_compatibility": "compatible",
            "status": "required",
        },
        {
            "stress": "T_Meff",
            "origin": "Pi_M/M_eff monopole flux and shell boundary",
            "retained_identity_role": "conserved mass boundary label",
            "EH_compatibility": "compatible_if_boundary_or_constant_Meff",
            "status": "conditional_N1",
        },
        {
            "stress": "T_TF",
            "origin": "trace-free/shear projector sector",
            "retained_identity_role": "anisotropic stress bookkeeping",
            "EH_compatibility": "must_vanish_for_metric_only_EH",
            "status": "conditional_N2_or_non_EH",
        },
        {
            "stress": "T_rel",
            "origin": "relative memory exact/boundary sector",
            "retained_identity_role": "relative memory exchange bookkeeping",
            "EH_compatibility": "compatible_if_pure_boundary_or_zero",
            "status": "conditional_N4",
        },
        {
            "stress": "T_projector",
            "origin": "metric variation of B, Pi_M, Pi_TF, Pi_matter, P_mem",
            "retained_identity_role": "prevents fake conservation",
            "EH_compatibility": "must_vanish_or_be_boundary_only_for_metric_only_EH",
            "status": "open_N5",
        },
        {
            "stress": "T_X",
            "origin": "X multiplier/boundary momentum sector",
            "retained_identity_role": "source-identity/no-hair bookkeeping",
            "EH_compatibility": "must_have_no_bulk_exterior_hair",
            "status": "open_N6",
        },
        {
            "stress": "T_boundary",
            "origin": "collar/boundary primitive/domain exchange",
            "retained_identity_role": "boundary flux and variational well-posedness",
            "EH_compatibility": "compatible_if_boundary_term_only",
            "status": "open_boundary_owner",
        },
    ]


def EH_implication_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "T_projector_zero",
            "Bianchi_status": "safe_if_zero_theorem_parent_derived",
            "metric_only_EH_status": "can_continue",
            "local_claim": "conditional_only",
            "why": "no bulk projector stress remains",
        },
        {
            "case": "T_projector_boundary_only",
            "Bianchi_status": "safe_if_boundary_variation_retained",
            "metric_only_EH_status": "can_continue_with_boundary_term",
            "local_claim": "conditional_only",
            "why": "bulk exterior remains metric-only",
        },
        {
            "case": "T_projector_retained_bulk",
            "Bianchi_status": "conserved_total_stress_possible",
            "metric_only_EH_status": "fails_metric_only_EH",
            "local_claim": "modified_exterior_not_local_GR",
            "why": "bulk non-metric stress remains in exterior equations",
        },
        {
            "case": "T_projector_dropped",
            "Bianchi_status": "invalid",
            "metric_only_EH_status": "fake",
            "local_claim": "forbidden",
            "why": "conservation is manufactured by omission",
        },
    ]


def N5_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "zero_stress_route",
            "decision": "not_derived",
            "reason": "projector metric and boundary primitive are not proven metric-independent/pure gauge",
            "next_action": "derive topological/metric-independent projector or pure-boundary support",
        },
        {
            "route": "retained_stress_route",
            "decision": "formal_Bianchi_contract_written",
            "reason": "diffeomorphism invariance can conserve total stress only if projector stress is included",
            "next_action": "derive parent variational identity and check whether stress is bulk or boundary",
        },
        {
            "route": "bulk_retained_stress_to_EH",
            "decision": "rejected_for_metric_only_EH",
            "reason": "bulk retained projector stress means exterior is not metric-only vacuum Einstein",
            "next_action": "use only as modified-exterior branch, not local-GR promotion",
        },
        {
            "route": "drop_projector_stress",
            "decision": "rejected",
            "reason": "fake conservation",
            "next_action": "never use in local tests",
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
            "gate": "projector zero-stress theorem derived",
            "status": "fail",
            "evidence": "metric dependence and boundary primitive remain unproved",
            "claim_allowed": "no",
        },
        {
            "gate": "retained projector-stress ledger written",
            "status": "pass",
            "evidence": "T_projector included in total Bianchi ledger",
            "claim_allowed": "formal conservation contract only",
        },
        {
            "gate": "metric-only EH compatible N5 cleared",
            "status": "fail",
            "evidence": "bulk-vs-boundary status of T_projector not derived",
            "claim_allowed": "no",
        },
        {
            "gate": "dropped projector stress route rejected",
            "status": "pass",
            "evidence": "explicitly forbidden as fake conservation",
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
            "meaning": "N5 is now split cleanly. The zero-stress route is not derived because the projector metric, projector variations, and boundary primitive are not proven metric-independent or pure gauge. The retained-stress route is the only honest Bianchi contract: include T_projector in the total stress. But if T_projector is a bulk exterior stress, the metric-only EH stack fails. For local GR, T_projector must be zero or boundary-only by parent theorem.",
            "main_gain": "projector stress can no longer hide; the EH stack now knows exactly what N5 must prove",
            "main_failure": "T_projector zero/boundary-only status is still not parent-derived",
            "next_target": "249-projector-boundary-only-condition-or-metric-only-reduction-fail.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_248_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    variation_rows = variation_term_rows()
    zero_rows = zero_route_test_rows()
    ledger_rows = retained_ledger_rows()
    implication_rows = EH_implication_rows()
    decision_matrix = N5_decision_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "projector_stress_variation_terms.csv": (
            variation_rows,
            ["term", "schematic_variation", "stress_owner", "zero_route_requirement", "retained_route_requirement", "status_after_248"],
        ),
        "zero_stress_route_tests.csv": (
            zero_rows,
            ["test", "required_for_zero_stress", "current_evidence", "status", "readout"],
        ),
        "retained_stress_Bianchi_ledger.csv": (
            ledger_rows,
            ["stress", "origin", "retained_identity_role", "EH_compatibility", "status"],
        ),
        "EH_stack_implication_after_248.csv": (
            implication_rows,
            ["case", "Bianchi_status", "metric_only_EH_status", "local_claim", "why"],
        ),
        "N5_decision_matrix.csv": (
            decision_matrix,
            ["route", "decision", "reason", "next_action"],
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
        "projector_zero_stress_derived": False,
        "retained_projector_stress_ledger_written": True,
        "metric_only_EH_compatible_N5_cleared": False,
        "dropped_projector_stress_route_rejected": True,
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
