from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "lifted-C-boundary-primitive-and-domain-Euler-equation"
STATUS = "boundary_primitive_condition_derived_as_fixed_relative_class_admissibility_physical_class_selection_open"
CLAIM_CEILING = "admissibility_derivation_only_no_physical_domain_selector_matter_metric_EH_PPN_or_local_GR_promotion"
NEXT_TARGET = "366-representative-invariant-matter-action-for-lifted-C.md"


SOURCE_DOCS = [
    {
        "path": "277-domain-free-boundary-Euler-equation.md",
        "role": "free-boundary Euler equation and degeneracy for coherent domain selector",
    },
    {
        "path": "278-admissible-domain-class-boundary-current-owner.md",
        "role": "relative class preserving boundary variation rule",
    },
    {
        "path": "279-representative-selection-boundary-polarization-no-go.md",
        "role": "smooth boundary polarization no-go and representative-selection obstruction",
    },
    {
        "path": "287-boundary-current-charge-owner-attempt.md",
        "role": "relative boundary current supports charge invariance but not normalization/occupancy selection",
    },
    {
        "path": "364-lifted-C-sector-form-holonomy-theorem-attempt.md",
        "role": "lifted C Stokes mechanism and missing boundary primitive condition",
    },
    {
        "path": "scripts/lifted_C_sector_form_holonomy_theorem_attempt.py",
        "role": "machine-readable prior lifted C theorem attempt",
    },
]


TARGET_CONDITION = [
    {
        "target": "boundary_primitive_null",
        "formula": "int_boundaryD B_perp = 0",
        "why_needed": "makes delta C_D = N_D^-1 int_boundaryD B_perp vanish for local representative shifts",
        "prior_status": "required_but_not_parent_derived",
    },
    {
        "target": "fixed_relative_class",
        "formula": "delta Q_rel[D] = 0",
        "why_needed": "restricts boundary/domain variations to one physical relative class sector",
        "prior_status": "available_as_admissibility_rule",
    },
    {
        "target": "boundary_exchange",
        "formula": "i_eta j_3 = delta_eta b_2 + d_boundary gamma_1",
        "why_needed": "converts moving-boundary flux into boundary-current bookkeeping",
        "prior_status": "formal_relative_current_contract",
    },
    {
        "target": "physical_class_selection",
        "formula": "Q_rel_local = 0 and Q_rel_FLRW != 0 selected by parent equations",
        "why_needed": "turns admissibility into physical domain ownership",
        "prior_status": "not_derived",
    },
]


VARIATIONAL_DERIVATION = [
    {
        "step": 1,
        "statement": "Use the lifted C relative current pair.",
        "equation": "J_rel = (j_3, b_2), d_rel J_rel = (d j_3, i*j_3 - d_boundary b_2) = 0",
        "status": "formal_current_available",
    },
    {
        "step": 2,
        "statement": "Define the relative domain charge/class.",
        "equation": "Q_rel[D] = int_D j_3 - int_boundaryD b_2",
        "status": "class_observable_definition",
    },
    {
        "step": 3,
        "statement": "Fix a relative class sector during local representative variations.",
        "equation": "delta Q_rel[D] = 0",
        "status": "admissibility_condition",
    },
    {
        "step": 4,
        "statement": "For a pure representative shift with no bulk source, write the lifted residual as an exact current change.",
        "equation": "delta j_3 = d B_perp",
        "status": "lifted_C_representative_shift",
    },
    {
        "step": 5,
        "statement": "Assume the boundary representative shifts consistently, not as an independent physical source.",
        "equation": "delta b_2 = B_perp + d_boundary gamma_1",
        "status": "relative_boundary_exchange_condition",
    },
    {
        "step": 6,
        "statement": "Then fixed relative charge gives the boundary primitive condition.",
        "equation": "0 = delta Q_rel = int_D dB_perp - int_boundaryD B_perp = int_boundaryD B_perp - int_boundaryD B_perp",
        "status": "derived_as_relative_class_admissibility",
    },
    {
        "step": 7,
        "statement": "For the observed class scalar, the local representative part is invisible.",
        "equation": "delta C_D = N_D^-1 int_boundaryD B_perp = 0 inside a fixed local trivial class",
        "status": "conditional_on_fixed_class_and_boundary_exchange",
    },
]


EULER_BRIDGE = [
    {
        "piece": "free_boundary_Euler",
        "formula": "delta C_coh = V_D^-1 int_boundaryD eta[(2a/b)(theta-a)-(a^2/b^2)(R-b)] dSigma",
        "readout": "domain stationarity equation is derived but degenerate",
        "impact_on_primitive": "does not itself force int_boundaryD B_perp=0",
    },
    {
        "piece": "relative_class_admissibility",
        "formula": "delta Q_rel[D] = 0",
        "readout": "boundary displacements are restricted to class-preserving moves",
        "impact_on_primitive": "can own the primitive-null condition for representative shifts",
    },
    {
        "piece": "combined_condition",
        "formula": "Euler stationarity evaluated only on class-preserving eta",
        "readout": "degeneracy is narrowed but not uniquely solved",
        "impact_on_primitive": "primitive silence is derived within a class, not class selection",
    },
    {
        "piece": "missing_parent_step",
        "formula": "delta S_parent/delta class = physical Q_rel branch",
        "readout": "parent still must choose local zero and FLRW nonzero classes",
        "impact_on_primitive": "without this, local silence is branch-admissibility not full derivation",
    },
]


BRANCH_READOUT = [
    {
        "branch": "stationary_local_vacuum",
        "class_assignment": "Q_rel = 0",
        "primitive_status": "int_boundaryD B_perp = 0 for fixed-class representative shifts",
        "promotion_status": "conditional_silence_not_physical_class_selection",
    },
    {
        "branch": "FLRW_coherent_domain",
        "class_assignment": "Q_rel != 0 with int_D J_C roughly det(Q_coh)",
        "primitive_status": "local exact representative shifts do not erase global class",
        "promotion_status": "conditional_memory_survival_normalization_open",
    },
    {
        "branch": "tracefree_shear_or_GW",
        "class_assignment": "no scalar coherent volume class if P_coh removes tracefree sector",
        "primitive_status": "safe only if shear does not source boundary class change",
        "promotion_status": "conditional",
    },
    {
        "branch": "collapse_merger_transition",
        "class_assignment": "possible class-changing event",
        "primitive_status": "primitive need not vanish if source/event changes Q_rel",
        "promotion_status": "open_event_source_law",
    },
    {
        "branch": "matter_coupling",
        "class_assignment": "matter should see C_D/P_D C only",
        "primitive_status": "invisible only if representative-invariant action is proved",
        "promotion_status": "next_theorem_target",
    },
]


NO_OVERCLAIM_RULES = [
    {
        "rule": "primitive_null_is_admissibility_not_full_parent_selection",
        "meaning": "int_boundaryD B_perp=0 is derived only inside fixed relative class variations",
        "forbidden_claim": "physical local domain is fully selected",
    },
    {
        "rule": "class_selection_still_open",
        "meaning": "parent theory still must choose Q_rel=0 locally and nonzero FLRW class",
        "forbidden_claim": "local GR follows",
    },
    {
        "rule": "matter_selector_still_open",
        "meaning": "representative-invariant matter action has not been proven",
        "forbidden_claim": "WEP/clock/PPN passed",
    },
    {
        "rule": "boundary_current_not_amplitude_owner_yet",
        "meaning": "relative current gives invariance but not u3, B_mem, charge level, or endpoints",
        "forbidden_claim": "cosmology amplitude derived",
    },
]


GATE_TEMPLATE = [
    {
        "gate": "source_paths_exist",
        "status": "computed",
        "evidence": "computed at runtime",
    },
    {
        "gate": "free_boundary_Euler_equation_imported",
        "status": "pass",
        "evidence": "checkpoint 277 provides derived shape derivative and Euler condition",
    },
    {
        "gate": "relative_class_admissibility_imported",
        "status": "pass",
        "evidence": "checkpoint 278 provides delta Q_rel=0 admissible variation rule",
    },
    {
        "gate": "boundary_primitive_null_derived_inside_fixed_class",
        "status": "conditional_pass",
        "evidence": "delta Q_rel=0 with delta j_3=dB_perp and delta b_2=B_perp+d_boundary gamma gives boundary cancellation",
    },
    {
        "gate": "physical_domain_class_selected",
        "status": "fail",
        "evidence": "the parent action still does not choose local Q_rel=0 and FLRW nonzero class",
    },
    {
        "gate": "smooth_boundary_polarization_rescue",
        "status": "fail",
        "evidence": "checkpoint 279 shows endpoint/regularity constraints underselect polarization functions",
    },
    {
        "gate": "matter_metric_parent_derived",
        "status": "fail",
        "evidence": "representative-invariant matter action remains the next theorem target",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "EH operator, matter selector, residual vector, and class selection remain open",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The boundary primitive condition is no longer a naked axiom inside fixed relative class sectors, but physical class/domain selection remains open.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "prove or reject that matter actions depend only on the lifted class observable C_D/P_D C and not on representative data",
        "pass_condition": "exp(P_D C)g becomes a selector theorem instead of closure",
    },
    {
        "priority": 2,
        "target": "367-topological-class-selection-or-local-GR-closure-ledger.md",
        "task": "attempt a topological/discrete relative class selection rule after smooth polarization failed",
        "pass_condition": "local Q_rel=0 and FLRW Q_rel nonzero are parent-selected without arbitrary smoothing scale",
    },
    {
        "priority": 3,
        "target": "368-EH-exterior-reduction-after-lifted-C-gate.md",
        "task": "if matter selector passes, reconnect to Einstein-Hilbert exterior operator gate",
        "pass_condition": "metric-only second-order exterior operator follows or residual operator is bounded",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    rows: list[dict[str, Any]] = []
    for gate in GATE_TEMPLATE:
        if gate["gate"] == "source_paths_exist":
            rows.append(
                {
                    "gate": gate["gate"],
                    "status": "pass" if not missing_sources else "fail",
                    "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
                }
            )
        else:
            rows.append(gate)
    return rows


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "target_condition.csv", TARGET_CONDITION)
    write_csv(results_dir / "variational_derivation.csv", VARIATIONAL_DERIVATION)
    write_csv(results_dir / "Euler_to_primitive_bridge.csv", EULER_BRIDGE)
    write_csv(results_dir / "branch_readout.csv", BRANCH_READOUT)
    write_csv(results_dir / "no_overclaim_rules.csv", NO_OVERCLAIM_RULES)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 365 lifted C boundary primitive and domain Euler artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
