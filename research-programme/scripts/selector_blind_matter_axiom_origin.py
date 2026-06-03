from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "selector-blind-matter-axiom-origin"
CHECKPOINT_DOC = "404-selector-blind-matter-axiom-origin.md"
STATUS = "selector_blind_matter_axiom_origin_audit_written_primitive_routes_conditional_no_single_parent_origin_yet_silence_remains_postulate_or_closure_no_local_GR_pass"
CLAIM_CEILING = "selector_blind_matter_axiom_origin_only_no_WEP_EH_Newton_PPN_flux_domain_or_local_GR_pass"
NEXT_TARGET = "405-same-frame-EH-source-derived-stack-audit.md"


SOURCE_DOCS = [
    {
        "path": "00-pre-pivot-checkpoint.md",
        "role": "motion-load simplification hypothesis and protected route policy",
    },
    {
        "path": "01-motion-load-route-contract.md",
        "role": "motion-load primitive scaffold and promotion criteria",
    },
    {
        "path": "02-motion-load-local-GR-reduction.md",
        "role": "conditional p=1/local-GR reading from clock/load reciprocity",
    },
    {
        "path": "03-reciprocal-routing-parent-origin.md",
        "role": "reciprocity parent-origin attempt and failure to derive non-GR stress balance",
    },
    {
        "path": "04-vacuum-reciprocity-action-contract.md",
        "role": "vacuum reciprocal-strain source silence contract",
    },
    {
        "path": "12-gauge-noether-origin-audit.md",
        "role": "Noether/gauge warning: identities do not set residuals zero",
    },
    {
        "path": "299-local-silence-selector-attempt.md",
        "role": "local silence exact if boundary-bath/relative-class selector vanishes",
    },
    {
        "path": "308-selector-parent-theorem-attempt.md",
        "role": "spectral/topological selector theorem conditional route",
    },
    {
        "path": "337-exact-parent-pullback-selection-rule-gate.md",
        "role": "exact parent readout/pullback theorem template",
    },
    {
        "path": "341-indistinguishable-cell-quotient-parent-action-gate.md",
        "role": "unlabelled quotient finite-fibre parent-action gate",
    },
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "fixed relative class boundary primitive and representative-invariance gap",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe closure/selector contract",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "coframe pullback cancellation routes and no-go classification",
    },
    {
        "path": "387-identity-coframe-or-class-metric-fork.md",
        "role": "identity coframe versus class-metric fork",
    },
    {
        "path": "401-parent-matter-selector-theorem-attempt.md",
        "role": "selector-blind matter theorem attempt and exp(F(C_D))e counterexample",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source-normalization pair",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux no-hair numeric contract",
    },
]


PRIMITIVE_CANDIDATE_AUDIT = [
    {
        "candidate": "motion_load_clock_space_capacity",
        "primitive_claim": "c^2 = v_space^2 + v_clock^2 + v_load^2 with reciprocal clock/spatial routing",
        "can_pay": "local weak-field p=1/gamma-like routing if reciprocity is assumed",
        "cannot_pay_yet": "selector-blind matter, EH operator selection, Ward-silent flux",
        "status": "conditional_motivator_not_parent_origin",
    },
    {
        "candidate": "vacuum_reciprocity_source_silence",
        "primitive_claim": "local vacuum has no reciprocal-strain source/current",
        "can_pay": "would make motion-load local GR route cleaner",
        "cannot_pay_yet": "vacuum silence equation J_R=0 is not derived from the parent action",
        "status": "contract_target_not_derived",
    },
    {
        "candidate": "gauge_noether_observer_split",
        "primitive_claim": "observer-splitting symmetry or Noether identity constrains residual sectors",
        "can_pay": "can organize Ward identities and force ledgers",
        "cannot_pay_yet": "Noether identities relate equations; they do not set residual stress/flux zero without action equations",
        "status": "no_go_as_silence_origin",
    },
    {
        "candidate": "spectral_topological_local_selector",
        "primitive_claim": "local domains are projected-boundary gapped/closed or relative-current trivial",
        "can_pay": "exact local open-sector silence sigma_D=0 if premises hold",
        "cannot_pay_yet": "parent action has not derived local gap/trivial class or protected ordinary local EM/matter baths",
        "status": "conditional_silence_theorem",
    },
    {
        "candidate": "exact_parent_pullback_readout",
        "primitive_claim": "all effective corrections are pullbacks of parent-invariant readout/quotient maps",
        "can_pay": "forbids some active-label counterterms under exact readout",
        "cannot_pay_yet": "parent action has not proven exact readout rather than Wilsonian EFT correction",
        "status": "conditional_readout_template",
    },
    {
        "candidate": "indistinguishable_cell_quotient",
        "primitive_claim": "finite cells are unlabelled/basis labels in an internal quotient fibre",
        "can_pay": "forbids fixed active spurions if parent variables are quotient orbits",
        "cannot_pay_yet": "parent variable origin and no-marker-extension theorem remain open",
        "status": "conditional_quotient_template",
    },
    {
        "candidate": "fixed_relative_class_boundary_primitive",
        "primitive_claim": "boundary primitive null follows inside class-preserving domain variations",
        "can_pay": "turns some boundary primitive silence from naked axiom into admissibility condition",
        "cannot_pay_yet": "physical class/domain selection and representative-invariant matter action remain open",
        "status": "conditional_boundary_admissibility",
    },
    {
        "candidate": "identity_metric_coframe_selector",
        "primitive_claim": "local matter couples only to the metric-core coframe e",
        "can_pay": "delta S_matter/delta Z_I|e=0 by chain rule if matter constants are selector-blind",
        "cannot_pay_yet": "existing parent premises allow universal ehat=exp(F(C_D))e counterexample",
        "status": "sufficient_axiom_not_derived",
    },
    {
        "candidate": "Ward_owned_flux_silence",
        "primitive_claim": "all boundary/bulk/domain/projector/source flux is owned by one total Ward ledger",
        "can_pay": "could close alpha3/Gdot hard rows by exact cancellation",
        "cannot_pay_yet": "ledger is mapped, but total flux owner/no-hair equations are not parent-derived",
        "status": "necessary_contract_not_derived",
    },
]


SILENCE_DEBT_MAP = [
    {
        "debt": "selector_blind_matter",
        "needed_statement": "S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A] and partial_Z theta_A=0",
        "best_candidate_origin": "identity_metric_coframe_selector plus representative-invariant matter",
        "current_status": "sufficient_conditional_theorem_not_parent_derived",
        "blocking_counterexample": "universal class metric ehat=exp(F(C_D))e",
    },
    {
        "debt": "same_frame_EH_source",
        "needed_statement": "EH operator and measured-GM source normalization are derived in the matter frame",
        "best_candidate_origin": "motion-load reciprocity plus same-frame parent action",
        "current_status": "conditional_route_not_parent_derived",
        "blocking_counterexample": "EH-shaped equations with drifting G_eff M_eff are not Newton",
    },
    {
        "debt": "Ward_silent_flux",
        "needed_statement": "P_loc[nB+F_X+F_domain+F_projector+F_source]=0 or retained with coefficient",
        "best_candidate_origin": "total Ward-owned flux silence",
        "current_status": "mapped_not_parent_derived",
        "blocking_counterexample": "Noether/Ward identity alone does not make flux zero",
    },
    {
        "debt": "domain_projector_nohair",
        "needed_statement": "domain/projector vector and anisotropic representatives are gauge/topological or explicitly retained",
        "best_candidate_origin": "spectral/topological selector plus quotient/readout theorem",
        "current_status": "conditional_template_not_parent_derived",
        "blocking_counterexample": "physical domain vector or marker extension can survive quotient language",
    },
    {
        "debt": "boundary_bulk_radial_hair",
        "needed_statement": "boundary/bulk radial hair is absent, constant universal monopole, or alpha(lambda)-scored",
        "best_candidate_origin": "fixed relative class boundary primitive plus source-free bulk mass gap",
        "current_status": "conditional_not_full_local_nohair",
        "blocking_counterexample": "sourced/boundary-resourced X or radial boundary gradient remains a fifth force",
    },
]


THEOREM_CHAIN_ATTEMPT = [
    {
        "stage": 1,
        "desired_step": "motion/time/space primitives define only relational capacity/load/routing, not matter-visible selector labels",
        "status": "not_yet_formalized",
        "if_successful": "selector variables become representative/gauge data",
    },
    {
        "stage": 2,
        "desired_step": "parent variables are quotient/readout objects, not labelled active spurions",
        "status": "conditional_template",
        "if_successful": "active marker and species spurion routes are forbidden",
    },
    {
        "stage": 3,
        "desired_step": "matter actions are functions only of observed geometry and internal constants",
        "status": "sufficient_axiom_not_derived",
        "if_successful": "delta S_matter/delta Z_I|e=0",
    },
    {
        "stage": 4,
        "desired_step": "local domains are projected-boundary gapped/trivial in the MTS channel",
        "status": "conditional_spectral_topological_theorem",
        "if_successful": "open-sector local silence sigma_D=0",
    },
    {
        "stage": 5,
        "desired_step": "boundary/domain/projector/bulk fluxes are absent, gauge/topological, or Ward-owned",
        "status": "mapped_not_parent_derived",
        "if_successful": "alpha3 and Gdot/G hard rows close by theorem, not tuning",
    },
    {
        "stage": 6,
        "desired_step": "same matter frame selects EH exterior and constant measured GM",
        "status": "conditional_route_not_parent_derived",
        "if_successful": "Newton/PPN reduction stack can move from closure to theorem",
    },
]


POSTULATE_OPTIONS = [
    {
        "option": "P1_selector_blind_matter",
        "postulate": "nonmetric MTS selectors are unobservable representative variables for local matter",
        "buys": "R0 direct matter/coframe pullback closes",
        "cost": "WEP/source charges, EH/source, and flux/domain no-hair still need separate theorems",
        "public_claim_policy": "postulate_or_closure_only",
    },
    {
        "option": "P2_local_projected_silence",
        "postulate": "local bound domains have zero projected MTS boundary bath/current class",
        "buys": "open-sector local silence and reduced local fifth-force pressure",
        "cost": "ordinary EM/matter bath contamination and horizons/galaxies need separate treatment",
        "public_claim_policy": "closure_only_until_projector_theorem",
    },
    {
        "option": "P3_total_Ward_flux_owner",
        "postulate": "all local boundary/bulk/domain/projector flux is exactly owned/cancelled in total Ward identity",
        "buys": "alpha3/Gdot hard rows close if exact",
        "cost": "must be action-derived to avoid being a hidden GR-import/source erasure",
        "public_claim_policy": "closure_only_until_variation_proof",
    },
    {
        "option": "P4_primitive_relational_quotient",
        "postulate": "MTS primitives are relational quotient/readout objects with no active material markers",
        "buys": "possible unified origin for selector-blind matter and no spurions",
        "cost": "needs formal parent configuration space and matter functor",
        "public_claim_policy": "promising_theorem_target_not_claim",
    },
]


NO_GO_RESULTS = [
    {
        "shortcut": "motion-load reciprocity alone",
        "why_it_fails": "can motivate p=1 but does not forbid matter selector pullback or flux channels",
    },
    {
        "shortcut": "Noether/Ward identity alone",
        "why_it_fails": "identity organizes exchange but does not set residual source/flux zero",
    },
    {
        "shortcut": "one observed coframe as WEP intuition",
        "why_it_fails": "WEP/covariance allow universal class metric ehat=exp(F(C_D))e",
    },
    {
        "shortcut": "quotient language alone",
        "why_it_fails": "marker extensions and relational readouts can carry physical active data",
    },
    {
        "shortcut": "local silence selector by local curvature threshold",
        "why_it_fails": "ordinary local systems could accidentally activate the sector",
    },
    {
        "shortcut": "GM absorption of all radial/source residues",
        "why_it_fails": "only constant universal range-independent monopole absorption is safe",
    },
]


ROW_IMPACT = [
    {
        "runner_row": "R0_identity_coframe_direct",
        "impact_if_origin_derived": "closure_zero could become derived_zero",
        "current_state": "closure_zero",
    },
    {
        "runner_row": "R1_WEP_source_charge",
        "impact_if_origin_derived": "species/source charge rows could move toward theorem-zero",
        "current_state": "contingent_budget",
    },
    {
        "runner_row": "R3_gamma",
        "impact_if_origin_derived": "domain/projector/boundary slip channels could be removed before EH test",
        "current_state": "budget_only",
    },
    {
        "runner_row": "R7_alpha3",
        "impact_if_origin_derived": "Ward flux hard row could close exactly rather than meet 4e-20 tuning",
        "current_state": "contingent_budget",
    },
    {
        "runner_row": "R9_Gdot",
        "impact_if_origin_derived": "secular source/flux/domain drift could close",
        "current_state": "contingent_budget",
    },
    {
        "runner_row": "R11_EH_operator_ledger",
        "impact_if_origin_derived": "same-frame local EH theorem becomes cleaner but still separate",
        "current_state": "retained_residual",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The primitive-origin audit finds no single currently derived MTS principle that simultaneously makes matter selector-blind, selects the same metric frame, and silences boundary/domain/flux channels. The strongest unifying candidate is a relational quotient/readout origin: MTS primitives are unlabelled motion/time/space relational structures, selectors are representative data, and local matter couples only to the observed quotient geometry. That would be powerful, but it is not yet derived. Existing motion-load, selector, quotient, boundary-primitive, and Ward routes are conditional templates. Therefore selector-blind matter and local flux silence remain postulate/closure targets, not derived GR.",
        "single_parent_origin_found": False,
        "best_candidate": "primitive_relational_quotient_readout_plus_selector_blind_matter",
        "selector_blind_matter_derived": False,
        "Ward_flux_silence_derived": False,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "combine checkpoints 401-404 into one strict local-GR stack with derived/conditional/postulate/retained labels",
        "pass_condition": "every local GR/Newton rung has a current status and no closure is mistaken for theorem",
    },
    {
        "priority": 2,
        "target": "406-local-runner-v4-derived-vs-closure-queue.py",
        "task": "turn the derived-vs-closure audit into runner-v4 row states",
        "pass_condition": "runner-v4 separates theorem_zero, postulate_zero, closure_zero, conditional, and retained rows",
    },
    {
        "priority": 3,
        "target": "407-primitive-relational-quotient-action-sketch.md",
        "task": "attempt a formal parent action/configuration-space sketch for the relational quotient origin",
        "pass_condition": "either a real variational route appears or the primitive quotient stays a named postulate",
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
            "gate": "primitive_candidates_audited",
            "status": "pass",
            "evidence": f"{len(PRIMITIVE_CANDIDATE_AUDIT)} candidate origins audited",
        },
        {
            "gate": "silence_debt_map_written",
            "status": "pass",
            "evidence": f"{len(SILENCE_DEBT_MAP)} silence debts mapped",
        },
        {
            "gate": "conditional_theorem_chain_written",
            "status": "pass",
            "evidence": f"{len(THEOREM_CHAIN_ATTEMPT)} chain stages written",
        },
        {
            "gate": "single_parent_origin_found",
            "status": "fail",
            "evidence": "no current primitive route derives selector-blind matter plus same-frame EH/source plus Ward-silent flux",
        },
        {
            "gate": "best_candidate_identified",
            "status": "conditional_pass",
            "evidence": "primitive relational quotient/readout route is the best unifying theorem target",
        },
        {
            "gate": "postulate_options_written",
            "status": "pass",
            "evidence": f"{len(POSTULATE_OPTIONS)} explicit postulate/closure options recorded",
        },
        {
            "gate": "shortcut_no_go_results_written",
            "status": "pass",
            "evidence": f"{len(NO_GO_RESULTS)} no-go shortcuts recorded",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "primitive origin audit only; no local-GR theorem promoted",
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
    candidate_rows = [
        {
            "candidate": row["candidate"],
            "status": row["status"],
            "cannot_pay_yet": row["cannot_pay_yet"],
        }
        for row in PRIMITIVE_CANDIDATE_AUDIT
    ]
    debt_rows = [
        {
            "debt": row["debt"],
            "best_origin": row["best_candidate_origin"],
            "status": row["current_status"],
        }
        for row in SILENCE_DEBT_MAP
    ]
    postulate_rows = [
        {
            "option": row["option"],
            "buys": row["buys"],
            "policy": row["public_claim_policy"],
        }
        for row in POSTULATE_OPTIONS
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 404 - Selector-Blind Matter Axiom Origin

Private primitive-origin/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoints 401-403 made the local-GR blocker very exact:

- matter must be selector-blind;
- EH/source normalization must be in the same frame matter sees;
- boundary/domain/projector/bulk flux must be theorem-zero, gauge/topological, Ward-owned, or explicitly retained.

This checkpoint asks whether the older motion/time/space primitive trail already derives that silence.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/selector_blind_matter_axiom_origin.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Primitive Candidate Audit

{markdown_table(candidate_rows, ["candidate", "status", "cannot_pay_yet"])}

## 4. Silence Debt Map

{markdown_table(debt_rows, ["debt", "best_origin", "status"])}

## 5. Best Candidate

The strongest unifying target is:

```text
primitive relational quotient/readout
  -> selector variables are representative, not matter-visible
  -> matter couples only to observed quotient geometry
  -> local projected boundary/domain flux is gauge/topological or Ward-owned
```

If this were derived, it could pay several debts at once. But in the current corpus it is still a theorem target, not a theorem.

## 6. Postulate Options

{markdown_table(postulate_rows, ["option", "buys", "policy"])}

## 7. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 8. Decision

{DECISION[0]["decision"]}

Practical read: we have not found magic, but we have found the right place to look. The “motion/time/space” route should not be used as a vibe to silence local rows. It must become a relational quotient/readout parent principle, or remain an explicit closure/postulate.

## 9. Next Target

`{NEXT_TARGET}`

Roll checkpoints 401-404 into a strict local-GR stack audit so we can see, in one file, which rungs are derived, conditional, postulated, closure-only, retained, or failed.
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "primitive_candidate_audit.csv", PRIMITIVE_CANDIDATE_AUDIT)
    write_csv(results_dir / "silence_debt_map.csv", SILENCE_DEBT_MAP)
    write_csv(results_dir / "theorem_chain_attempt.csv", THEOREM_CHAIN_ATTEMPT)
    write_csv(results_dir / "postulate_options.csv", POSTULATE_OPTIONS)
    write_csv(results_dir / "no_go_results.csv", NO_GO_RESULTS)
    write_csv(results_dir / "row_impact.csv", ROW_IMPACT)
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
        "primitive_candidates_audited": len(PRIMITIVE_CANDIDATE_AUDIT),
        "silence_debts_mapped": len(SILENCE_DEBT_MAP),
        "single_parent_origin_found": False,
        "best_candidate": "primitive_relational_quotient_readout_plus_selector_blind_matter",
        "selector_blind_matter_derived": False,
        "Ward_flux_silence_derived": False,
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
        description="Write checkpoint 404 selector-blind matter axiom origin artifacts."
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
