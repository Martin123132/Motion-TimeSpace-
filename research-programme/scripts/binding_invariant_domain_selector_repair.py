from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "binding-invariant-domain-selector-repair"
CHECKPOINT_DOC = "416-binding-invariant-domain-selector-repair.md"
STATUS = "binding_invariant_domain_selector_repair_written_best_auxiliary_Cexp_route_retained_as_contract_not_parent_derivation_no_local_GR_pass"
CLAIM_CEILING = "binding_invariant_domain_selector_repair_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "417-boundary-exchange-nohair-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "64-binding-invariant-domain-selector-attempt.md",
        "role": "C_coh/C_exp candidate invariant and nonimport guardrail",
    },
    {
        "path": "65-Ccoh-phase-field-selector-attempt.md",
        "role": "phase-field selector equation and threshold/scale risks",
    },
    {
        "path": "66-chiD-stress-and-scale-gate.md",
        "role": "dynamic chi_D stress and scale gate",
    },
    {
        "path": "67-auxiliary-selector-parent-contract.md",
        "role": "auxiliary/topological selector parent contract",
    },
    {
        "path": "68-chiD-gated-memory-conservation-contract.md",
        "role": "Bianchi/conservation contract for chi_D-gated memory",
    },
    {
        "path": "415-local-trivial-class-selector-theorem-attempt.md",
        "role": "local zero-class chain requiring parent chi_D selector",
    },
    {
        "path": "runs/20260531-111219-binding-invariant-domain-selector-attempt/results/candidate_invariant_ledger.csv",
        "role": "candidate invariant ledger",
    },
    {
        "path": "runs/20260531-111219-binding-invariant-domain-selector-attempt/results/invariant_equation_chain.csv",
        "role": "C_coh/C_exp equation chain",
    },
    {
        "path": "runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/phase_action_candidates.csv",
        "role": "phase action candidates",
    },
    {
        "path": "runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/parameter_risk_register.csv",
        "role": "phase selector parameter risks",
    },
    {
        "path": "runs/20260531-111832-chiD-stress-and-scale-gate/results/scale_option_ledger.csv",
        "role": "chi_D stress/scale options",
    },
    {
        "path": "runs/20260531-112108-auxiliary-selector-parent-contract/results/candidate_parent_routes.csv",
        "role": "auxiliary selector parent routes",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states",
    },
]


REPAIR_REQUIREMENTS = [
    {
        "requirement": "no_lower_limit_import",
        "test": "selector cannot use Newtonian binding energy, GR turnaround, or empirical residual scoring",
        "status": "pass_as_guardrail",
    },
    {
        "requirement": "arena_separation",
        "test": "FLRW coherent expansion active while stationary local bound domains are quiet",
        "status": "kinematic_support",
    },
    {
        "requirement": "parent_variational_selector",
        "test": "E_chi=0 follows from S_parent and selects chi_D/domain",
        "status": "not_derived",
    },
    {
        "requirement": "no_new_local_stress",
        "test": "chi_D has no independent propagating stress or fifth-force scale",
        "status": "contract_only",
    },
    {
        "requirement": "no_fitted_threshold",
        "test": "threshold/epsilon/transition scale is universal, limiting, or parent-derived",
        "status": "open",
    },
    {
        "requirement": "Bianchi_safe_gate",
        "test": "nabla_mu(T_mem[chi_D]+T_aux+T_boundary)^munu=0 on shell",
        "status": "not_derived",
    },
    {
        "requirement": "boundary_exchange_owned",
        "test": "T_memory nabla chi_D and relative boundary exchange are varied and owned",
        "status": "not_derived",
    },
]


CANDIDATE_SELECTOR_ROUTES = [
    {
        "route": "auxiliary_signed_Cexp_projector",
        "schematic": "S_aux=int sqrt(-g) lambda_chi(chi_D-Pi[C_exp])",
        "strength": "best_current_contract",
        "failure": "Pi, epsilon, averaging domain, and Bianchi/boundary ownership are not parent-derived",
    },
    {
        "route": "topological_boundary_projector",
        "schematic": "S_aux=<chi_D,J_rel>_boundary/relative class",
        "strength": "best_for_no_local_stress",
        "failure": "boundary exchange/no-hair equation and physical class selection remain open",
    },
    {
        "route": "phase_field_Ccoh_relaxation",
        "schematic": "ell_chi^2 D^2 chi_D-(chi_D-C_coh)=0",
        "strength": "explicit selector equation",
        "failure": "introduces ell_chi and T_chi unless converted to auxiliary limit",
    },
    {
        "route": "double_well_threshold",
        "schematic": "U=lambda chi^2(1-chi)^2/4 - mu(C-C_star)chi",
        "strength": "binary domain selection",
        "failure": "C_star risks fitted threshold unless parent-derived",
    },
    {
        "route": "hard_step_selector",
        "schematic": "chi_D=Heaviside(C-C_star)",
        "strength": "simple closure map",
        "failure": "singular and not variational without extra distributional rules",
    },
    {
        "route": "empirical_domain_window",
        "schematic": "choose chi_D to minimize residuals",
        "strength": "none_for_theory",
        "failure": "forbidden rescue knob",
    },
]


NONIMPORT_GUARDRAILS = [
    {
        "forbidden_import": "Newtonian_binding_energy",
        "reason": "imports the lower-limit theory we are trying to derive",
        "status": "blocked",
    },
    {
        "forbidden_import": "GR_turnaround_surface",
        "reason": "imports the GR reduction before deriving it",
        "status": "blocked",
    },
    {
        "forbidden_import": "empirical_domain_score",
        "reason": "turns chi_D into a data-fitted window",
        "status": "blocked",
    },
    {
        "forbidden_import": "per_system_ell_chi",
        "reason": "creates adjustable local/cosmology transition knob",
        "status": "blocked",
    },
    {
        "forbidden_import": "delete_T_chi_by_hand",
        "reason": "stress must vanish by constraint/topology or be conserved",
        "status": "blocked",
    },
]


CONDITIONAL_REPAIR_CHAIN = [
    {
        "step": 1,
        "claim": "Use purely kinematic motion/volume-flow invariant.",
        "identity": "C_exp = sign(<theta>_D)<theta>_D^2/(<theta^2>_D+<sigma^2>_D+<omega^2>_D+eps)",
        "status": "candidate_supported",
    },
    {
        "step": 2,
        "claim": "FLRW and stationary local domains separate.",
        "identity": "FLRW -> C_exp~+1; stationary bound -> C_exp~0",
        "status": "kinematic_support",
    },
    {
        "step": 3,
        "claim": "Promote C_exp to a parent selector source without adding stress.",
        "identity": "chi_D=Pi[C_exp] via auxiliary/topological constraint",
        "status": "contract_not_derived",
    },
    {
        "step": 4,
        "claim": "Avoid a fitted threshold/scale.",
        "identity": "Pi, eps, and any transition scale are universal or parent-derived",
        "status": "open",
    },
    {
        "step": 5,
        "claim": "Own Bianchi and boundary exchange terms.",
        "identity": "T_memory nabla chi_D + T_aux + T_boundary cancels/vanishes on shell",
        "status": "not_derived",
    },
    {
        "step": 6,
        "claim": "Then local trivial class selector becomes parent-derived.",
        "identity": "E_chi=0 selects local Q_rel=0 and active FLRW class from one rule",
        "status": "conditional_target_not_promoted",
    },
]


BLOCKER_MATRIX = [
    {
        "blocker": "averaging_domain_circularity",
        "why_it_matters": "C_exp[D] is defined on a domain D, but D is what chi_D must select",
        "repair_needed": "local candidate domains generated by parent boundary/current variables, not data windows",
    },
    {
        "blocker": "epsilon_or_threshold_origin",
        "why_it_matters": "eps_D, C_star, or Pi can become hidden fit knobs",
        "repair_needed": "limiting prescription or universal parent-derived constants",
    },
    {
        "blocker": "chiD_stress",
        "why_it_matters": "dynamic selector adds local scalar stress/fifth force",
        "repair_needed": "auxiliary/topological no-stress route",
    },
    {
        "blocker": "Bianchi_boundary_exchange",
        "why_it_matters": "gated memory stress produces T_memory nabla chi_D terms",
        "repair_needed": "boundary exchange/no-hair theorem",
    },
    {
        "blocker": "single_rule_local_FLRW_split",
        "why_it_matters": "the same parent selector must silence bound local domains while preserving cosmology",
        "repair_needed": "derive arena split from C_exp/C_coh dynamics, not separate axioms",
    },
]


ROW_TRANSITION_ATTEMPT = [
    {
        "row_id": "R0_identity_coframe_direct",
        "result": "not_upgraded",
        "new_state": "closure_zero",
        "reason": "selector repair is still a contract, not a no-marker/local-class theorem",
    },
    {
        "row_id": "R5_alpha1",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "domain vector leakage remains if chi_D selector is material/dynamic",
    },
    {
        "row_id": "R6_alpha2",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "selector anisotropy/vector channels remain retained",
    },
    {
        "row_id": "R7_alpha3",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "boundary exchange and momentum flux are not owned",
    },
    {
        "row_id": "R8_xi",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "preferred-location/domain class route remains open",
    },
    {
        "row_id": "R9_Gdot",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "domain scale drift is not theorem-zero",
    },
    {
        "row_id": "R10_fifth_force",
        "result": "not_upgraded",
        "new_state": "unscored_parameterized",
        "reason": "dynamic selector/transition scale can look like fifth-force physics",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The binding/coherence repair improves the selector route but does not derive it. The best current candidate is an auxiliary or topological projector driven by the signed coherent expansion invariant C_exp, because it avoids Newtonian binding energy, GR turnaround, empirical windows, and independent chi_D stress in principle. But it is still a contract: the averaging-domain circularity, epsilon/threshold origin, Bianchi-safe stress cancellation, and boundary exchange ownership are not derived. Therefore the local trivial-class selector remains conditional closure, not local GR.",
        "best_route": "auxiliary_signed_Cexp_projector_or_topological_boundary_projector",
        "Newton_GR_import_blocked": True,
        "parent_selector_derived": False,
        "Bianchi_boundary_exchange_derived": False,
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
        "task": "derive or bound the boundary exchange current that blocks chi_D-gated memory conservation",
        "pass_condition": "boundary exchange is theorem-zero, coefficient-bounded, or retained explicitly",
    },
    {
        "priority": 2,
        "target": "418-Cexp-domain-candidate-generator.md",
        "task": "remove averaging-domain circularity by defining parent-generated candidate domains before C_exp scoring",
        "pass_condition": "C_exp evaluates domains generated by parent variables, not by data/posthoc windows",
    },
    {
        "priority": 3,
        "target": "419-finite-fibre-spectrum-decoupling-theorem-attempt.md",
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
                "new_state": transition["new_state"],
                "result": transition["result"],
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
            "gate": "nonimport_guardrails_enforced",
            "status": "pass",
            "evidence": f"{len(NONIMPORT_GUARDRAILS)} forbidden imports blocked",
        },
        {
            "gate": "Cexp_kinematic_separator_supported",
            "status": "conditional_pass",
            "evidence": "C_exp separates FLRW coherent expansion from stationary bound volume flow kinematically",
        },
        {
            "gate": "auxiliary_Cexp_route_written",
            "status": "conditional_pass",
            "evidence": "best route is auxiliary/topological projector driven by C_exp",
        },
        {
            "gate": "parent_selector_derived",
            "status": "fail",
            "evidence": "E_chi=0 selector remains contract-level",
        },
        {
            "gate": "averaging_domain_circularity_resolved",
            "status": "fail",
            "evidence": "C_exp[D] still needs parent-generated candidate domains",
        },
        {
            "gate": "epsilon_threshold_origin_derived",
            "status": "fail",
            "evidence": "Pi, eps_D, C_star, or transition prescription are not parent-derived",
        },
        {
            "gate": "Bianchi_boundary_exchange_derived",
            "status": "fail",
            "evidence": "T_memory grad chi_D and boundary exchange remain unowned",
        },
        {
            "gate": "chiD_local_stress_removed_by_theorem",
            "status": "fail",
            "evidence": "auxiliary/topological no-stress route is preferred but not derived",
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
            "evidence": "binding selector repair only; no EH/Newton/PPN/local-GR pass",
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
            "status": row["status"],
            "test": row["test"],
        }
        for row in REPAIR_REQUIREMENTS
    ]
    route_table_rows = [
        {
            "route": row["route"],
            "strength": row["strength"],
            "failure": row["failure"],
        }
        for row in CANDIDATE_SELECTOR_ROUTES
    ]
    chain_table_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in CONDITIONAL_REPAIR_CHAIN
    ]
    blocker_table_rows = [
        {
            "blocker": row["blocker"],
            "repair_needed": row["repair_needed"],
        }
        for row in BLOCKER_MATRIX
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
    text = f"""# 416 - Binding-Invariant Domain Selector Repair

Private selector/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 415 showed that local zero class needs a parent-selected local domain. This checkpoint revisits the binding/coherence selector route and asks whether `C_coh/C_exp` can be promoted from classifier to parent selector without importing Newtonian binding, GR turnaround, empirical windows, or a new local scalar stress.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/binding_invariant_domain_selector_repair.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Repair Requirements

{markdown_table(requirement_table_rows, ["requirement", "status", "test"])}

## 4. Candidate Selector Routes

{markdown_table(route_table_rows, ["route", "strength", "failure"])}

## 5. Conditional Repair Chain

{markdown_table(chain_table_rows, ["step", "claim", "status"])}

## 6. Blocker Matrix

{markdown_table(blocker_table_rows, ["blocker", "repair_needed"])}

## 7. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "previous_state", "new_state", "result"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: `C_exp` is still the right footwork, not a knockout. It gives a clean local/cosmology separator without cheating, but it must be embedded into a Bianchi-safe auxiliary/topological selector before we can call local trivial class derived.

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
    write_csv(results_dir / "repair_requirements.csv", REPAIR_REQUIREMENTS)
    write_csv(results_dir / "candidate_selector_routes.csv", CANDIDATE_SELECTOR_ROUTES)
    write_csv(results_dir / "nonimport_guardrails.csv", NONIMPORT_GUARDRAILS)
    write_csv(results_dir / "conditional_repair_chain.csv", CONDITIONAL_REPAIR_CHAIN)
    write_csv(results_dir / "blocker_matrix.csv", BLOCKER_MATRIX)
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
        "Newton_GR_import_blocked": True,
        "best_route": "auxiliary_signed_Cexp_projector_or_topological_boundary_projector",
        "parent_selector_derived": False,
        "Bianchi_boundary_exchange_derived": False,
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
        description="Write checkpoint 416 binding-invariant domain selector repair artifacts."
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
