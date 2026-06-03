from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-trivial-class-selector-theorem-attempt"
CHECKPOINT_DOC = "415-local-trivial-class-selector-theorem-attempt.md"
STATUS = "local_trivial_class_selector_theorem_attempt_written_conditional_zero_class_chain_parent_selector_topology_boundary_exchange_open_no_local_GR_pass"
CLAIM_CEILING = "local_trivial_class_selector_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "416-binding-invariant-domain-selector-repair.md"


SOURCE_DOCS = [
    {
        "path": "61-bound-domain-boundary-theorem-attempt.md",
        "role": "stationary/extremal volume-flow boundary partial theorem",
    },
    {
        "path": "62-domain-field-chiD-action-contract.md",
        "role": "chi_D domain selector action contract",
    },
    {
        "path": "63-chiD-variation-to-boundary-equation-attempt.md",
        "role": "chi_D variation failure and binding-invariant need",
    },
    {
        "path": "64-binding-invariant-domain-selector-attempt.md",
        "role": "coherent-expansion invariant found, full binding derivation absent",
    },
    {
        "path": "65-Ccoh-phase-field-selector-attempt.md",
        "role": "explicit selector equation with stress/scale caveat",
    },
    {
        "path": "66-chiD-stress-and-scale-gate.md",
        "role": "dynamic chi_D stress blocks promotion",
    },
    {
        "path": "67-auxiliary-selector-parent-contract.md",
        "role": "auxiliary/topological selector route",
    },
    {
        "path": "68-chiD-gated-memory-conservation-contract.md",
        "role": "chi_D gated memory conservation contract and boundary exchange open",
    },
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "fixed relative-class admissibility derives primitive-null condition",
    },
    {
        "path": "414-local-quotient-invariant-algebra-triviality-gate.md",
        "role": "local invariant algebra gate naming relative/domain class obstruction",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states",
    },
    {
        "path": "runs/20260602-064500-local-quotient-invariant-algebra-triviality-gate/results/invariant_generators.csv",
        "role": "machine-readable invariant generator register",
    },
]


SELECTOR_REQUIREMENTS = [
    {
        "requirement": "stationary_bound_domain",
        "symbolic_form": "dV_D/dtau = integral_boundary v_n dA = 0",
        "current_support": "partial_theorem_from_volume_flow_if_domain_is_already_selected",
        "missing": "parent selection of D",
    },
    {
        "requirement": "fixed_relative_class_admissibility",
        "symbolic_form": "delta Q_rel = 0 for admissible local variations",
        "current_support": "derived_inside_fixed_class_variations",
        "missing": "physical selection of trivial class",
    },
    {
        "requirement": "trivial_relative_cohomology_or_no_defect",
        "symbolic_form": "H_rel(D,partial D)=0 and no local topological/source defect",
        "current_support": "not_derived",
        "missing": "topology/no-defect premise from parent theory",
    },
    {
        "requirement": "zero_boundary_exchange_current",
        "symbolic_form": "i*j_3 - d_boundary b_2 = 0 on partial D",
        "current_support": "boundary bookkeeping exists",
        "missing": "boundary exchange/no-hair equation",
    },
    {
        "requirement": "parent_chiD_selector",
        "symbolic_form": "E_chi = delta S_parent/delta chi_D selects local bound domain",
        "current_support": "chi_D action contract written",
        "missing": "binding/coherence invariant without Newtonian/GR/data import",
    },
    {
        "requirement": "auxiliary_no_stress_selector",
        "symbolic_form": "T_chi=0 on shell or conserved boundary bookkeeping",
        "current_support": "auxiliary route preferred",
        "missing": "full Bianchi/Noether derivation",
    },
    {
        "requirement": "local_cosmology_split",
        "symbolic_form": "Q_rel(local)=0 while Q_rel(FLRW) can be nonzero",
        "current_support": "conceptual split supported by stationary vs coherent expansion domains",
        "missing": "single parent selector deriving both branches",
    },
]


CONDITIONAL_ZERO_CLASS_CHAIN = [
    {
        "step": 1,
        "claim": "Local domain is parent-selected, not hand-drawn.",
        "identity": "E_chi[D]=0 selects chi_D or equivalent boundary current",
        "status": "not_derived",
    },
    {
        "step": 2,
        "claim": "Selected local domain is stationary/virialized in coherent volume flow.",
        "identity": "dV_D/dtau=0",
        "status": "conditional_partial_support",
    },
    {
        "step": 3,
        "claim": "Relative current has no boundary exchange in local vacuum.",
        "identity": "d_rel J_rel=0 and boundary exchange term vanishes",
        "status": "not_derived",
    },
    {
        "step": 4,
        "claim": "Relative cohomology/topological defect class is trivial.",
        "identity": "H_rel(D,partial D)=0 or [J_rel]=0",
        "status": "not_derived",
    },
    {
        "step": 5,
        "claim": "Then the relative charge/class is exact or zero.",
        "identity": "Q_rel = integral_D j_3 - integral_boundary b_2 = 0",
        "status": "conditional_theorem_if_steps_1_to_4_hold",
    },
    {
        "step": 6,
        "claim": "Domain selector contributes no local matter-visible generator.",
        "identity": "chi_D is boundary bookkeeping/pure selector, not a material scalar",
        "status": "not_derived",
    },
    {
        "step": 7,
        "claim": "Local invariant algebra loses relative/domain class generators.",
        "identity": "I_loc(Q)/I(e_obs) has no Q_rel, chi_D, or boundary flux generator",
        "status": "conditional_target_not_promoted",
    },
]


SELECTOR_BRANCH_TESTS = [
    {
        "branch": "stationary_volume_flow",
        "test": "dV_D/dtau=0 after D is selected",
        "result": "conditional_support",
        "failure_mode": "does not select D by itself",
    },
    {
        "branch": "fixed_relative_class",
        "test": "delta Q_rel=0 admissible variations",
        "result": "conditional_support",
        "failure_mode": "fixed class can be nontrivial",
    },
    {
        "branch": "trivial_relative_cohomology",
        "test": "H_rel(D,partial D)=0/no defect",
        "result": "fail_open",
        "failure_mode": "not derived from parent configuration",
    },
    {
        "branch": "chiD_advection",
        "test": "u^mu nabla_mu chi_D=0",
        "result": "fail_as_selector",
        "failure_mode": "transports a chosen domain; does not choose it",
    },
    {
        "branch": "Ccoh_phase_selector",
        "test": "ell_chi^2 D^2 chi - (chi-Ccoh)=0",
        "result": "support_with_stress_scale_risk",
        "failure_mode": "introduces ell_chi and T_chi unless auxiliary/topological",
    },
    {
        "branch": "auxiliary_selector",
        "test": "chi_D=Ccoh with lambda_chi constraints",
        "result": "best_route_contract",
        "failure_mode": "Bianchi/boundary exchange derivation still open",
    },
    {
        "branch": "empirical_window",
        "test": "choose D to fit local/cosmology residuals",
        "result": "forbidden",
        "failure_mode": "turns domain selector into data-tuned rescue knob",
    },
]


COUNTEREXAMPLE_CLASSES = [
    {
        "counterexample": "nontrivial_fixed_relative_class",
        "construction": "delta Q_rel=0 but Q_rel != 0",
        "damage": "fixed-class admissibility preserves a nonzero local marker",
        "needed_blocker": "physical trivial-class selector",
    },
    {
        "counterexample": "boundary_exchange_hair",
        "construction": "i*j_3 - d_boundary b_2 != 0 at partial D",
        "damage": "domain/projector flux feeds alpha3/Gdot/preferred-frame rows",
        "needed_blocker": "boundary exchange no-hair theorem",
    },
    {
        "counterexample": "topological_defect_or_hole",
        "construction": "H_rel(D,partial D) nontrivial",
        "damage": "relative charge survives even with local stationarity",
        "needed_blocker": "parent no-defect/topology condition",
    },
    {
        "counterexample": "cosmology_dragged_local_domain",
        "construction": "local domain inherits FLRW coherent class",
        "damage": "cosmology activity leaks into local PPN",
        "needed_blocker": "single parent selector separating bound local and coherent FLRW branches",
    },
    {
        "counterexample": "dynamical_chiD_stress",
        "construction": "chi_D is a propagating scalar with T_chi and ell_chi",
        "damage": "new local stress/fifth-force/preferred-frame channel",
        "needed_blocker": "auxiliary/topological no-stress selector theorem",
    },
    {
        "counterexample": "posthoc_window_selector",
        "construction": "choose chi_D after fitting PPN, SPARC, Pantheon, BAO, or CMB",
        "damage": "not a field theory; empirical rescue window",
        "needed_blocker": "parent-derived selector before data scoring",
    },
]


ROW_TRANSITION_ATTEMPT = [
    {
        "row_id": "R0_identity_coframe_direct",
        "attempted_upgrade": "closure_zero -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "closure_zero",
        "reason": "local trivial class would help no-marker route, but selector/topology/boundary premises are not derived",
    },
    {
        "row_id": "R5_alpha1",
        "attempted_upgrade": "retained_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "domain vector/marker leakage remains possible",
    },
    {
        "row_id": "R6_alpha2",
        "attempted_upgrade": "retained_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "domain vector/anistropy selector channels remain open",
    },
    {
        "row_id": "R7_alpha3",
        "attempted_upgrade": "retained_contingent_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "boundary/domain flux no-hair is not derived",
    },
    {
        "row_id": "R8_xi",
        "attempted_upgrade": "retained_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "preferred-location/domain class marker remains possible",
    },
    {
        "row_id": "R9_Gdot",
        "attempted_upgrade": "retained_contingent_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "domain scale drift and boundary exchange are not theorem-zero",
    },
    {
        "row_id": "R10_fifth_force",
        "attempted_upgrade": "unscored_parameterized -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "unscored_parameterized",
        "reason": "dynamical chi_D/class scalar fifth-force route remains a counterexample",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "A useful conditional zero-class theorem is now explicit: if the parent action selects the local bound domain, the selected domain is stationary in coherent volume flow, local relative cohomology/topological charge is trivial, boundary exchange current vanishes, and chi_D is auxiliary/topological with no local stress, then Q_rel=[J_rel]=0 locally and the relative/domain class stops being an independent local invariant generator. But the existing corpus does not derive the parent selector, topology/no-defect condition, boundary exchange no-hair equation, or Bianchi-safe auxiliary chi_D route. Therefore local trivial class is a theorem target, not a theorem. The local branch may be tested as fixed-class closure, but it is not a GR derivation.",
        "conditional_zero_class_theorem_written": True,
        "stationary_volume_flow_partial_support": True,
        "physical_local_class_selector_derived": False,
        "boundary_exchange_nohair_derived": False,
        "trivial_relative_cohomology_derived": False,
        "theorem_zero_upgrades": 0,
        "R0_new_state": "closure_zero",
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "revisit binding/coherence selector without importing Newtonian binding, GR turnaround, or data windows",
        "pass_condition": "chi_D/local domain selector is parent-derived or explicitly demoted to closure",
    },
    {
        "priority": 2,
        "target": "417-boundary-exchange-nohair-theorem-attempt.md",
        "task": "derive or bound the boundary exchange current that feeds flux/domain rows",
        "pass_condition": "boundary exchange is theorem-zero, bounded, or retained with coefficients",
    },
    {
        "priority": 3,
        "target": "418-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "task": "test whether finite-cell fibre spectra can be integrated out or reduced to universal constants",
        "pass_condition": "finite fibre does not create local matter-visible marker channels",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def row_transition_rows() -> list[dict[str, Any]]:
    matrix_by_id = {row["row_id"]: row for row in runner_v4_rows()}
    rows: list[dict[str, Any]] = []
    for transition in ROW_TRANSITION_ATTEMPT:
        matrix_row = matrix_by_id.get(transition["row_id"], {})
        rows.append(
            {
                "row_id": transition["row_id"],
                "previous_state": matrix_row.get("runner_v4_state", "missing"),
                "previous_zero_kind": matrix_row.get("zero_kind", "missing"),
                "attempted_upgrade": transition["attempted_upgrade"],
                "result": transition["result"],
                "new_state": transition["new_state"],
                "theorem_credit_allowed": False,
                "claim_allowed": False,
                "reason": transition["reason"],
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_rows = [row for row in transition_rows if row["theorem_credit_allowed"]]
    claim_rows = [row for row in transition_rows if row["claim_allowed"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "selector_requirements_written",
            "status": "pass",
            "evidence": f"{len(SELECTOR_REQUIREMENTS)} selector requirements recorded",
        },
        {
            "gate": "stationary_volume_flow_support",
            "status": "conditional_pass",
            "evidence": "zero coherent boundary volume flux supports local scalar silence if D is selected",
        },
        {
            "gate": "fixed_relative_class_admissibility_support",
            "status": "conditional_pass",
            "evidence": "primitive-null condition is derived inside fixed relative-class variations",
        },
        {
            "gate": "physical_local_class_selector_derived",
            "status": "fail",
            "evidence": "chi_D/boundary selector is contracted but not parent-derived",
        },
        {
            "gate": "trivial_relative_cohomology_derived",
            "status": "fail",
            "evidence": "H_rel(D,partial D)=0/no-defect condition is not derived",
        },
        {
            "gate": "boundary_exchange_nohair_derived",
            "status": "fail",
            "evidence": "boundary exchange current remains open",
        },
        {
            "gate": "auxiliary_chiD_Bianchi_safe",
            "status": "fail",
            "evidence": "auxiliary/topological route is preferred but Bianchi derivation remains open",
        },
        {
            "gate": "local_cosmology_split_derived",
            "status": "fail",
            "evidence": "single parent selector separating local Q_rel=0 from active FLRW is not derived",
        },
        {
            "gate": "runner_rows_promoted_to_theorem_zero",
            "status": "fail",
            "evidence": f"{len(theorem_rows)} theorem-credit row upgrades",
        },
        {
            "gate": "claim_leaks",
            "status": "pass" if not claim_rows else "fail",
            "evidence": f"{len(claim_rows)} claim-allowed rows",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "local class selector attempt only; no EH/Newton/PPN/local-GR pass",
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


def write_checkpoint_markdown(
    run_dir: Path,
    transition_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    requirement_table_rows = [
        {
            "requirement": row["requirement"],
            "support": row["current_support"],
            "missing": row["missing"],
        }
        for row in SELECTOR_REQUIREMENTS
    ]
    chain_table_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in CONDITIONAL_ZERO_CLASS_CHAIN
    ]
    branch_table_rows = [
        {
            "branch": row["branch"],
            "result": row["result"],
            "failure_mode": row["failure_mode"],
        }
        for row in SELECTOR_BRANCH_TESTS
    ]
    counterexample_table_rows = [
        {
            "counterexample": row["counterexample"],
            "needed_blocker": row["needed_blocker"],
        }
        for row in COUNTEREXAMPLE_CLASSES
    ]
    transition_table_rows = [
        {
            "row_id": row["row_id"],
            "previous_state": row["previous_state"],
            "new_state": row["new_state"],
            "result": row["result"],
        }
        for row in transition_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 415 - Local Trivial Class Selector Theorem Attempt

Private local-class/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 414 stated the local invariant-algebra burden. This checkpoint attacks its most immediate generator: the relative boundary/domain class. The question is whether local `Q_rel=[J_rel]=0` can be derived from local-vacuum/domain physics rather than imposed as a plateau or closure axiom.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_trivial_class_selector_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Selector Requirements

{markdown_table(requirement_table_rows, ["requirement", "support", "missing"])}

## 4. Conditional Zero-Class Chain

{markdown_table(chain_table_rows, ["step", "claim", "status"])}

## 5. Branch Tests

{markdown_table(branch_table_rows, ["branch", "result", "failure_mode"])}

## 6. Counterexample Classes

{markdown_table(counterexample_table_rows, ["counterexample", "needed_blocker"])}

## 7. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "previous_state", "new_state", "result"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: this is progress, but not the golden ticket. We have a clean conditional theorem for local zero class; we do not yet have the parent selector that chooses the premises. That means local testing can use this as an explicitly labelled closure branch, not a derived GR limit.

## 10. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    transition_rows = row_transition_rows()
    gate_result_rows = gate_rows(source_rows, transition_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "selector_requirements.csv", SELECTOR_REQUIREMENTS)
    write_csv(results_dir / "conditional_zero_class_chain.csv", CONDITIONAL_ZERO_CLASS_CHAIN)
    write_csv(results_dir / "selector_branch_tests.csv", SELECTOR_BRANCH_TESTS)
    write_csv(results_dir / "counterexample_classes.csv", COUNTEREXAMPLE_CLASSES)
    write_csv(results_dir / "row_transition_attempt.csv", transition_rows)
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
        "selector_requirements": len(SELECTOR_REQUIREMENTS),
        "conditional_zero_class_theorem_written": True,
        "stationary_volume_flow_partial_support": True,
        "physical_local_class_selector_derived": False,
        "boundary_exchange_nohair_derived": False,
        "trivial_relative_cohomology_derived": False,
        "theorem_zero_upgrades": 0,
        "R0_new_state": "closure_zero",
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, transition_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 415 local trivial class selector theorem attempt artifacts."
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
