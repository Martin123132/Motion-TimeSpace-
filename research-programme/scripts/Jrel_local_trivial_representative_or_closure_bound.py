#!/usr/bin/env python3
"""Checkpoint 220: attempt local trivial J_rel representative or retain closure bound."""

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

CHECKPOINT_220_NAME = "Jrel-local-trivial-representative-or-closure-bound"
CHECKPOINT_219_RUN = RUNS_ROOT / "20260601-000036-compact-shell-q_loc-source-projection-attempt"

STATUS = "Jrel_local_trivial_representative_conditional_exactness_missing_closure_bound_retained"
CLAIM_CEILING = "Jrel_exactness_attempt_no_local_GR_or_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 220 J_rel representative script"),
        (WORK_DIR / "219-compact-shell-q_loc-source-projection-attempt.md", "q_loc source-projection theorem target"),
        (CHECKPOINT_219_RUN / "status.json", "checkpoint 219 machine status"),
        (CHECKPOINT_219_RUN / "results" / "source_leakage_budget.csv", "checkpoint 219 leakage budget"),
        (WORK_DIR / "60-relative-cohomology-boundary-contract.md", "relative cohomology boundary contract"),
        (WORK_DIR / "71-relative-boundary-current-construction-attempt.md", "formal J_rel construction"),
        (WORK_DIR / "72-relative-current-action-owner-attempt.md", "relative-current action owner attempt"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "Bianchi/projector accounting"),
        (WORK_DIR / "215-QJrel-load-morphology-parent-owner-attempt.md", "Q/J_rel morphology owner status"),
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


def representative_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "R1_zero_by_declaration",
            "statement": "Set J_rel=0 in compact local shells by definition.",
            "status": "rejected",
            "gain": "would silence q_loc immediately",
            "blocker": "this is the forbidden plateau/silence axiom in different notation",
        },
        {
            "route": "R2_exact_memory_sector_representative",
            "statement": "Require J_rel=d_rel A_rel in the projected memory-exchange sector, with the boundary primitive vanishing on the compact shell collar.",
            "status": "conditional_pass",
            "gain": "Stokes then kills integrated memory exchange through a stationary collar",
            "blocker": "parent action has not forced exactness or selected A_rel boundary data",
        },
        {
            "route": "R3_closed_nonexact_relative_class",
            "statement": "Allow d_rel J_rel=0 but keep a closed non-exact relative class.",
            "status": "danger_open",
            "gain": "matches the formal relative cohomology language",
            "blocker": "a closed non-exact class can carry a memory charge even in a compact collar unless its charge is separately zero",
        },
        {
            "route": "R4_BF_flatness_with_zero_boundary_polarization",
            "statement": "Use a BF-like local flatness condition plus Pi(C_coh)=0 on stationary compact shells.",
            "status": "conditional_pass",
            "gain": "keeps local propagating boundary hair suppressed",
            "blocker": "Pi(C_coh) and the physical representative are still not parent-derived",
        },
        {
            "route": "R5_stationary_no_domain_wall_flux",
            "statement": "Use fixed compact-shell boundaries and no relative domain-wall flux to set the collar exchange integral to zero.",
            "status": "conditional_integrated_only",
            "gain": "gives a clean no-through-flow condition",
            "blocker": "integrated no-flux is weaker than pointwise P_loc d_rel J_rel^nu=0",
        },
        {
            "route": "R6_identify_Jrel_with_ordinary_gravity_flux",
            "statement": "Let J_rel track ordinary Gauss/gravitational mass flux in the local shell.",
            "status": "rejected",
            "gain": "would make J_rel visibly physical",
            "blocker": "ordinary compact masses have nonzero gravitational flux, so this would not be locally trivial and would endanger PPN silence",
        },
    ]


def local_trivial_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "compact_vacuum_collar",
            "mathematical_form": "dmu_L|_C = 0 with sidecar class compact_vacuum_shell",
            "status": "conditional_pass",
            "if_missing": "extended loads cannot use the local shell theorem",
        },
        {
            "condition": "memory_sector_not_ordinary_Gauss_flux",
            "mathematical_form": "J_rel projects only memory/domain exchange, not the GR mass flux that sources the Newtonian field",
            "status": "contract_required",
            "if_missing": "solar/planetary compact systems carry nonzero flux and local triviality fails",
        },
        {
            "condition": "relative_exactness",
            "mathematical_form": "J_rel = d_rel A_rel in the projected local memory sector",
            "status": "not_derived",
            "if_missing": "closed non-exact local memory charge can remain",
        },
        {
            "condition": "vanishing_boundary_primitive",
            "mathematical_form": "A_rel|_inner_boundary = A_rel|_outer_boundary = 0 or matching pure gauge",
            "status": "not_derived",
            "if_missing": "Stokes leaves a boundary-memory exchange term",
        },
        {
            "condition": "stationary_domain_boundary",
            "mathematical_form": "v_boundary^rel = 0 and no domain-wall crossing of the compact collar",
            "status": "conditional_pass",
            "if_missing": "dynamic shells/mergers activate J_rel",
        },
        {
            "condition": "Noether_source_identity",
            "mathematical_form": "nabla_mu Khat^{mu nu}-nabla^nu Gamma_eff = S_L^nu + d_rel J_rel^nu",
            "status": "missing_external_clause",
            "if_missing": "J_rel exactness alone cannot prove q_loc^nu=0",
        },
        {
            "condition": "pointwise_projector_annihilation",
            "mathematical_form": "P_loc d_rel J_rel^nu = 0 in the collar, not merely integral_C d_rel J_rel = 0",
            "status": "not_derived",
            "if_missing": "only an averaged closure bound is available",
        },
    ]


def derivation_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Use the formal relative current J_rel=(j_3,b_2) with d_rel(j_3,b_2)=(d j_3, i_star j_3 - d_boundary b_2).",
            "result": "available_from_checkpoint_71",
            "gap": "",
        },
        {
            "step": 2,
            "statement": "In a compact stationary vacuum collar, matter/load support S_L^nu vanishes in the projected memory channel.",
            "result": "conditional_from_sidecar",
            "gap": "depends on fixed compact-shell morphology closure",
        },
        {
            "step": 3,
            "statement": "If J_rel=d_rel A_rel and the boundary primitive is zero or pure gauge on both collar boundaries, Stokes gives zero integrated relative exchange.",
            "result": "conditional_integrated_zero",
            "gap": "exactness and boundary data are not parent-selected",
        },
        {
            "step": 4,
            "statement": "If the same parent action also gives pointwise projector annihilation P_loc d_rel J_rel^nu=0, then the J_rel part of q_loc^nu vanishes.",
            "result": "conditional_pointwise_route",
            "gap": "pointwise projector annihilation is stronger than integrated exactness",
        },
        {
            "step": 5,
            "statement": "If the Noether/source identity from checkpoint 219 is added, q_loc^nu=-P_loc(S_L^nu+d_rel J_rel^nu)=0 in the compact collar.",
            "result": "conditional_local_theorem",
            "gap": "Noether/source identity still missing",
        },
        {
            "step": 6,
            "statement": "Therefore the derivation fails as a theorem today, but gives a precise closure bound on P_loc d_rel J_rel^nu leakage.",
            "result": "closure_bound_retained",
            "gap": "local GR not promoted",
        },
    ]


def closure_bound_rows() -> list[dict[str, Any]]:
    rows_219 = read_csv_rows(CHECKPOINT_219_RUN / "results" / "source_leakage_budget.csv")
    rows: list[dict[str, Any]] = []
    for source_budget in rows_219:
        use_in_gate = source_budget["use_in_gate"]
        leakage_budget = float(source_budget["remaining_unmodeled_source_leakage_budget"])
        rows.append(
            {
                "case": source_budget["case"],
                "use_in_gate": use_in_gate,
                "q_R_like_gate": float(source_budget["q_R_like_gate"]),
                "q_proxy_before_Jrel_leakage": float(source_budget["q_total_proxy_before_source_leakage"]),
                "max_allowed_abs_Ploc_drel_Jrel_leakage": leakage_budget,
                "max_allowed_fraction_of_gate": float(source_budget["remaining_budget_fraction_of_gate"]),
                "bound_statement": "|P_loc d_rel J_rel| must remain below this value unless the exact local representative is derived",
                "status": "closure_bound_positive" if leakage_budget > 0 else "closure_bound_failed",
            }
        )
    return rows


def theorem_gate_rows(source_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(source["exists"] != "yes" for source in source_rows)
    compact_bounds = [row for row in bound_rows if row["use_in_gate"] == "yes"]
    compact_bound_failures = sum(row["status"] != "closure_bound_positive" for row in compact_bounds)
    worst_compact_bound = min(float(row["max_allowed_abs_Ploc_drel_Jrel_leakage"]) for row in compact_bounds)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "formal J_rel object exists",
            "status": "pass",
            "evidence": "checkpoint 71 relative pair J_rel=(j_3,b_2)",
            "claim_allowed": "formal language",
        },
        {
            "gate": "zero by declaration avoided",
            "status": "pass",
            "evidence": "R1 rejected",
            "claim_allowed": "no plateau axiom",
        },
        {
            "gate": "exact local representative parent-derived",
            "status": "fail",
            "evidence": "no action-level selection of J_rel=d_rel A_rel with compact-shell boundary data",
            "claim_allowed": "no theorem",
        },
        {
            "gate": "closed non-exact local class excluded",
            "status": "fail",
            "evidence": "topology/relative closure alone does not eliminate nonzero memory charge",
            "claim_allowed": "no theorem",
        },
        {
            "gate": "ordinary gravity flux separated from J_rel",
            "status": "conditional_pass",
            "evidence": "R6 rejected; J_rel must be memory/domain exchange only",
            "claim_allowed": "contract requirement",
        },
        {
            "gate": "integrated exchange killed by Stokes",
            "status": "conditional_pass",
            "evidence": "requires exact representative and vanishing boundary primitive",
            "claim_allowed": "integrated conditional lemma",
        },
        {
            "gate": "pointwise P_loc d_rel J_rel^nu zero derived",
            "status": "fail",
            "evidence": "integrated exactness is weaker than pointwise local PPN silence",
            "claim_allowed": "no local-GR promotion",
        },
        {
            "gate": "closure leakage bounds positive",
            "status": "pass" if compact_bound_failures == 0 else "fail",
            "evidence": f"compact_bound_failures={compact_bound_failures}; worst_compact_bound={worst_compact_bound}",
            "claim_allowed": "bounded residual closure",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(worst_compact_bound: float) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The only non-cheating route to local J_rel silence is exactness in the projected memory sector, vanishing compact-shell boundary primitive, separation from ordinary gravitational Gauss flux, and the checkpoint-219 Noether/source identity. That would derive q_loc silence, but the parent action has not forced those clauses. Therefore local J_rel silence remains a named closure bound.",
            "main_gain": "zero-by-declaration is rejected and replaced by exactness plus boundary-data theorem clauses",
            "main_failure": "exact representative, boundary primitive selection, and pointwise projector annihilation are not parent-derived",
            "worst_compact_bound": worst_compact_bound,
            "next_target": "221-Noether-source-identity-or-compact-PPN-closure-map.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_220_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    route_rows = representative_route_rows()
    condition_rows = local_trivial_condition_rows()
    derivation_rows = derivation_attempt_rows()
    bound_rows = closure_bound_rows()
    gate_rows = theorem_gate_rows(source_rows, bound_rows)
    compact_bounds = [row for row in bound_rows if row["use_in_gate"] == "yes"]
    worst_compact_bound = min(float(row["max_allowed_abs_Ploc_drel_Jrel_leakage"]) for row in compact_bounds)
    decision = decision_rows(worst_compact_bound)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "representative_route_tests.csv": (
            route_rows,
            ["route", "statement", "status", "gain", "blocker"],
        ),
        "local_trivial_conditions.csv": (
            condition_rows,
            ["condition", "mathematical_form", "status", "if_missing"],
        ),
        "derivation_attempt_chain.csv": (
            derivation_rows,
            ["step", "statement", "result", "gap"],
        ),
        "Jrel_closure_bound_table.csv": (
            bound_rows,
            [
                "case",
                "use_in_gate",
                "q_R_like_gate",
                "q_proxy_before_Jrel_leakage",
                "max_allowed_abs_Ploc_drel_Jrel_leakage",
                "max_allowed_fraction_of_gate",
                "bound_statement",
                "status",
            ],
        ),
        "theorem_gate_results.csv": (
            gate_rows,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "worst_compact_bound",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(source["exists"] != "yes" for source in source_rows)
    compact_bound_failures = sum(bound["status"] != "closure_bound_positive" for bound in compact_bounds)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "zero_by_declaration_rejected": True,
        "J_rel_exact_local_representative_derived": False,
        "ordinary_gravity_flux_identification_rejected": True,
        "integrated_triviality_conditional": True,
        "pointwise_Ploc_drel_Jrel_zero_derived": False,
        "Noether_source_identity_derived": False,
        "compact_closure_bound_failures": compact_bound_failures,
        "worst_remaining_compact_Jrel_leakage_bound": worst_compact_bound,
        "q_loc_pointwise_zero_promoted": False,
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
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
