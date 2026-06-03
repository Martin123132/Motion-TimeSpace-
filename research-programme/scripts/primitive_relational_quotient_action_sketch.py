from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "primitive-relational-quotient-action-sketch"
CHECKPOINT_DOC = "407-primitive-relational-quotient-action-sketch.md"
STATUS = "primitive_relational_quotient_action_sketch_written_candidate_parent_origin_formalized_but_no_marker_matter_functor_flux_and_EH_proofs_open_no_local_GR_pass"
CLAIM_CEILING = "primitive_relational_quotient_action_sketch_only_no_selector_blind_WEP_EH_Newton_PPN_flux_or_local_GR_pass"
NEXT_TARGET = "408-local-bound-data-runner-v4-smoke.py"


SOURCE_DOCS = [
    {
        "path": "337-exact-parent-pullback-selection-rule-gate.md",
        "role": "exact parent readout/pullback theorem template",
    },
    {
        "path": "341-indistinguishable-cell-quotient-parent-action-gate.md",
        "role": "quotient orbit/finite-fibre parent-action gate and marker hazard",
    },
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "fixed-relative-class boundary primitive and representative-invariance gap",
    },
    {
        "path": "404-selector-blind-matter-axiom-origin.md",
        "role": "primitive-origin audit and best candidate",
    },
    {
        "path": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "local-GR stack rungs and nearest derivation targets",
    },
    {
        "path": "406-local-runner-v4-derived-vs-closure-queue.md",
        "role": "runner-v4 state queue and theorem-zero separation",
    },
    {
        "path": "runs/20260602-045500-selector-blind-matter-axiom-origin/results/theorem_chain_attempt.csv",
        "role": "primitive theorem-chain attempt",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 state matrix",
    },
]


CONFIGURATION_SPACE_SKETCH = [
    {
        "object": "observed_geometry",
        "symbolic_form": "e or g[e]",
        "quotient_status": "physical local frame",
        "allowed_in_bulk_action": True,
        "open_issue": "same-frame EH/source theorem still separate",
    },
    {
        "object": "relational_MTS_state",
        "symbolic_form": "[R_MTS] = orbit(R_MTS)/G_rel",
        "quotient_status": "unlabelled relational orbit",
        "allowed_in_bulk_action": True,
        "open_issue": "G_rel not yet formalized as parent symmetry",
    },
    {
        "object": "finite_cell_fibre",
        "symbolic_form": "[h] in Fibre/S_n or spectrum/trace data",
        "quotient_status": "basis-free finite fibre",
        "allowed_in_bulk_action": True,
        "open_issue": "parent has not proven cells are basis labels rather than species",
    },
    {
        "object": "readout_projection",
        "symbolic_form": "P_read applied after parent variation",
        "quotient_status": "observable/readout only",
        "allowed_in_bulk_action": False,
        "open_issue": "must prove exact readout not reduced EFT action",
    },
    {
        "object": "active_marker",
        "symbolic_form": "P_active as material/background variable",
        "quotient_status": "forbidden marker extension",
        "allowed_in_bulk_action": False,
        "open_issue": "no-marker theorem not derived",
    },
    {
        "object": "boundary_domain_class",
        "symbolic_form": "[J_rel], Q_rel, I_top",
        "quotient_status": "relative/topological class",
        "allowed_in_bulk_action": True,
        "open_issue": "physical local/FLRW class selection remains open",
    },
]


ACTION_SKELETON_BLOCKS = [
    {
        "block": "S_geom_same_frame",
        "sketch": "S_geom[e] with candidate EH/local metric core",
        "variation_target": "metric/coframe equations in matter frame",
        "pays_debts": "same_frame_EH_source; EH_operator_selection",
        "current_status": "conditional_not_derived",
    },
    {
        "block": "S_relational_MTS",
        "sketch": "S_rel[[R_MTS], [h], [J_rel], Q_rel, I_top]",
        "variation_target": "equations depend only on quotient/readout-invariant data",
        "pays_debts": "selector_blind_matter; domain_projector_nohair",
        "current_status": "sketch_only",
    },
    {
        "block": "S_boundary_domain",
        "sketch": "S_BD[Q_rel, M_eff, V_scalar, I_top] with class-preserving admissible variations",
        "variation_target": "no B_TF/B_0i/vector marker leakage; fixed relative class boundary primitive",
        "pays_debts": "boundary_bulk_radial_hair; domain_projector_nohair",
        "current_status": "conditional_boundary_admissibility",
    },
    {
        "block": "S_total_Ward_owner",
        "sketch": "all boundary/bulk/domain/projector/source flux terms varied in one total ledger",
        "variation_target": "P_loc[nB+F_X+F_D+F_P+F_source]=0 or explicit retained current",
        "pays_debts": "Ward_silent_flux; Gdot_drift_silence",
        "current_status": "mapped_not_derived",
    },
    {
        "block": "S_matter_quotient_functor",
        "sketch": "sum_A S_A[Psi_A, e, omega[e], theta_A] with theta_A independent of representative selectors",
        "variation_target": "delta S_matter/delta Z_I|e=0",
        "pays_debts": "selector_blind_matter; one_observed_coframe; WEP_source_charge",
        "current_status": "sufficient_axiom_not_derived",
    },
    {
        "block": "S_readout_observables",
        "sketch": "observables are exact parent readouts after variation, not independent reduced action terms",
        "variation_target": "forbid P_active counterterms in the bulk action",
        "pays_debts": "exact_readout; no_marker_extension",
        "current_status": "conditional_template",
    },
]


VARIATIONAL_TESTS = [
    {
        "test": "quotient_invariance",
        "required_identity": "S_parent[x]=S_parent[g.x] for g in G_rel/S_n/basis relabeling",
        "would_pay": "no active-label counterterms",
        "current_verdict": "conditional_pass_template",
    },
    {
        "test": "no_marker_extension",
        "required_identity": "delta S_parent/delta P_active = 0 because P_active is not a parent variable",
        "would_pay": "prevents material active spurion",
        "current_verdict": "fail_open",
    },
    {
        "test": "matter_quotient_functor",
        "required_identity": "partial_Z e=0 and partial_Z theta_A=0 for representative selectors",
        "would_pay": "R0 closure_zero could become theorem_zero",
        "current_verdict": "fail_open",
    },
    {
        "test": "readout_after_variation",
        "required_identity": "delta(S_parent)/delta x=0 first, then P_read observable map",
        "would_pay": "forbids independent reduced EFT correction terms",
        "current_verdict": "conditional_template",
    },
    {
        "test": "boundary_domain_class_selection",
        "required_identity": "local bound domains select Q_rel=0/trivial projected class while FLRW can have Q_rel != 0",
        "would_pay": "local silence without silencing cosmology",
        "current_verdict": "fail_open",
    },
    {
        "test": "Ward_flux_owner",
        "required_identity": "P_loc[nB+F_X+F_D+F_P+F_source]=0 or retained coefficient current",
        "would_pay": "alpha3/Gdot hard channels",
        "current_verdict": "fail_open",
    },
    {
        "test": "same_frame_EH_source",
        "required_identity": "variation of S_geom in matter frame gives EH and constant measured GM",
        "would_pay": "Newton/PPN route",
        "current_verdict": "conditional_not_derived",
    },
]


NO_CHEAT_CONSTRAINTS = [
    {
        "constraint": "quotient not labelled species",
        "forbidden_move": "use symmetric labelled species action and call it quotient",
        "safe_requirement": "parent configuration space itself is orbit/spectrum/basis-free",
    },
    {
        "constraint": "no active marker",
        "forbidden_move": "let P_active enter as covariant material/background marker",
        "safe_requirement": "active readout is observable-only or source-at-zero, not bulk variable",
    },
    {
        "constraint": "readout after variation",
        "forbidden_move": "vary an independent reduced action S_reduced[P_active]",
        "safe_requirement": "vary S_parent first, then apply P_read",
    },
    {
        "constraint": "matter functor not a vibe",
        "forbidden_move": "say matter sees quotient geometry without writing S_matter arguments",
        "safe_requirement": "S_matter[Psi,e,omega[e],theta_A] with selector-independent theta_A",
    },
    {
        "constraint": "Ward identity not silence",
        "forbidden_move": "use conservation identity to erase flux",
        "safe_requirement": "derive flux absence/cancellation or retain coefficient current",
    },
]


ROW_UPGRADE_ATTEMPT = [
    {
        "runner_row": "R0_identity_coframe_direct",
        "current_v4_state": "closure_zero",
        "upgrade_if_sketch_proven": "theorem_zero",
        "current_result": "not_upgraded",
        "missing_proof": "matter quotient functor/no-marker selector proof",
    },
    {
        "runner_row": "R1_WEP_source_charge",
        "current_v4_state": "retained_contingent_budget",
        "upgrade_if_sketch_proven": "theorem_zero or retained source-charge coefficient",
        "current_result": "not_upgraded",
        "missing_proof": "species/source charge universality in quotient matter functor",
    },
    {
        "runner_row": "R7_alpha3",
        "current_v4_state": "retained_contingent_budget",
        "upgrade_if_sketch_proven": "theorem_zero if exact Ward flux owner derives",
        "current_result": "not_upgraded",
        "missing_proof": "total Ward flux owner/no-hair variation",
    },
    {
        "runner_row": "R9_Gdot",
        "current_v4_state": "retained_contingent_budget",
        "upgrade_if_sketch_proven": "theorem_zero if source/flux/domain drift silence derives",
        "current_result": "not_upgraded",
        "missing_proof": "time-independent measured GM and flux/domain drift closure",
    },
    {
        "runner_row": "R11_EH_operator_ledger",
        "current_v4_state": "retained_residual",
        "upgrade_if_sketch_proven": "conditional_theorem or theorem_zero only after same-frame EH proof",
        "current_result": "not_upgraded",
        "missing_proof": "metric-only local second-order same-frame exterior",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "A primitive relational quotient/readout parent-action sketch is now formalized. It is the best current candidate for unifying selector-blind matter, no active markers, local domain/projector silence, and exact readout discipline. It does not yet derive those facts. The sketch still needs four hard proofs: parent configuration space is genuinely quotient/basis-free, no material marker extension exists, matter is a quotient functor of the observed frame, and total boundary/domain/bulk/projector flux is varied and owned. Therefore no runner-v4 row is upgraded to theorem_zero.",
        "action_sketch_written": True,
        "theorem_zero_upgrades": 0,
        "no_marker_theorem_derived": False,
        "matter_quotient_functor_derived": False,
        "Ward_flux_owner_derived": False,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "run local residual profiles using runner-v4 state labels",
        "pass_condition": "closure, retained, contingent, and unscored rows are evaluated without theorem promotion",
    },
    {
        "priority": 2,
        "target": "409-runner-v4-red-team.md",
        "task": "red-team whether the quotient sketch or runner-v4 hides any closure as theorem",
        "pass_condition": "all false-promotion routes are named and blocked",
    },
    {
        "priority": 3,
        "target": "410-quotient-matter-functor-theorem-attempt.md",
        "task": "attempt the hardest subproof: matter action depends only on observed quotient geometry",
        "pass_condition": "R0 can move toward theorem_zero or stays closure_zero",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
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
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "configuration_space_sketch_written",
            "status": "pass",
            "evidence": f"{len(CONFIGURATION_SPACE_SKETCH)} configuration objects recorded",
        },
        {
            "gate": "action_skeleton_written",
            "status": "pass",
            "evidence": f"{len(ACTION_SKELETON_BLOCKS)} action blocks recorded",
        },
        {
            "gate": "variational_tests_written",
            "status": "pass",
            "evidence": f"{len(VARIATIONAL_TESTS)} variational tests recorded",
        },
        {
            "gate": "no_marker_theorem_derived",
            "status": "fail",
            "evidence": "marker/background extension remains open",
        },
        {
            "gate": "matter_quotient_functor_derived",
            "status": "fail",
            "evidence": "matter functor is sketched but not parent-derived",
        },
        {
            "gate": "Ward_flux_owner_derived",
            "status": "fail",
            "evidence": "total flux owner equation is a target, not a theorem",
        },
        {
            "gate": "runner_rows_upgraded_to_theorem_zero",
            "status": "fail",
            "evidence": "0 rows upgraded",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "action sketch only; no GR/Newton theorem promoted",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    config_rows = [
        {
            "object": row["object"],
            "status": row["quotient_status"],
            "bulk": row["allowed_in_bulk_action"],
            "open": row["open_issue"],
        }
        for row in CONFIGURATION_SPACE_SKETCH
    ]
    block_rows = [
        {
            "block": row["block"],
            "status": row["current_status"],
            "pays": row["pays_debts"],
        }
        for row in ACTION_SKELETON_BLOCKS
    ]
    upgrade_rows = [
        {
            "row": row["runner_row"],
            "current": row["current_v4_state"],
            "result": row["current_result"],
            "missing": row["missing_proof"],
        }
        for row in ROW_UPGRADE_ATTEMPT
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 407 - Primitive Relational Quotient Action Sketch

Private parent-action sketch checkpoint. This is not a public selector-blind matter, WEP, Einstein-Hilbert, Newtonian-limit, PPN, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 406 made the machine honest: no theorem-zero rows. This checkpoint asks whether the best primitive-origin candidate from checkpoint 404 can be stated as a real parent action sketch rather than a vibe.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/primitive_relational_quotient_action_sketch.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Configuration-Space Sketch

{markdown_table(config_rows, ["object", "status", "bulk", "open"])}

## 4. Action Skeleton

{markdown_table(block_rows, ["block", "status", "pays"])}

## 5. Row Upgrade Attempt

{markdown_table(upgrade_rows, ["row", "current", "result", "missing"])}

## 6. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 7. Decision

{DECISION[0]["decision"]}

Practical read: this is a good theorem target. It is not a theorem. If the quotient/readout sketch becomes a proper variational principle, it could pay several local-GR debts at once. Until then, runner-v4 correctly keeps every row non-promoted.

## 8. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "configuration_space_sketch.csv", CONFIGURATION_SPACE_SKETCH)
    write_csv(results_dir / "action_skeleton_blocks.csv", ACTION_SKELETON_BLOCKS)
    write_csv(results_dir / "variational_tests.csv", VARIATIONAL_TESTS)
    write_csv(results_dir / "no_cheat_constraints.csv", NO_CHEAT_CONSTRAINTS)
    write_csv(results_dir / "row_upgrade_attempt.csv", ROW_UPGRADE_ATTEMPT)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
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
        "configuration_objects": len(CONFIGURATION_SPACE_SKETCH),
        "action_blocks": len(ACTION_SKELETON_BLOCKS),
        "variational_tests": len(VARIATIONAL_TESTS),
        "theorem_zero_upgrades": 0,
        "matter_quotient_functor_derived": False,
        "Ward_flux_owner_derived": False,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 407 primitive relational quotient action sketch artifacts."
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
