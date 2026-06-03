from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "same-frame-EH-source-derived-stack-audit"
CHECKPOINT_DOC = "405-same-frame-EH-source-derived-stack-audit.md"
STATUS = "same_frame_EH_source_derived_stack_audit_written_local_GR_stack_partitioned_derived_conditional_closure_postulate_retained_no_local_GR_pass"
CLAIM_CEILING = "same_frame_EH_source_stack_audit_only_no_WEP_EH_Newton_PPN_flux_fifth_force_or_local_GR_pass"
NEXT_TARGET = "406-local-runner-v4-derived-vs-closure-queue.py"


SOURCE_DOCS = [
    {
        "path": "397-local-bound-runner-v3-from-identity-stack.md",
        "role": "runner-v3 row states after identity stack",
    },
    {
        "path": "398-parent-action-contract-v2-after-identity-stack.md",
        "role": "parent obligations for non-derived runner-v3 rows",
    },
    {
        "path": "400-runner-v3-numeric-smoke-extension.md",
        "role": "numeric smoke profile and channel-bound pressure",
    },
    {
        "path": "401-parent-matter-selector-theorem-attempt.md",
        "role": "selector-blind matter theorem attempt",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source-normalization pair",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux numeric contract",
    },
    {
        "path": "404-selector-blind-matter-axiom-origin.md",
        "role": "primitive-origin audit for selector/flux silence",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv",
        "role": "hardest local channel bounds",
    },
    {
        "path": "runs/20260602-042500-parent-matter-selector-theorem-attempt/results/row_transition_decision.csv",
        "role": "R0/R1/R2 transition states after selector attempt",
    },
    {
        "path": "runs/20260602-043500-EH-source-normalization-parent-pair/results/row_transition_decision.csv",
        "role": "gamma/beta/Gdot/fifth-force/operator transition states after EH/source attempt",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/family_rollup.csv",
        "role": "flux/domain/source family ceilings",
    },
    {
        "path": "runs/20260602-045500-selector-blind-matter-axiom-origin/results/silence_debt_map.csv",
        "role": "primitive-origin silence debt map",
    },
]


LOCAL_GR_STACK_RUNG_STATUS = [
    {
        "rung": "G0_GR_null_pipeline_sanity",
        "required_for_local_GR": "same evaluator does not fail the GR/null comparator",
        "current_status": "verified_sanity_not_theory",
        "evidence": "checkpoint 400 GR_null_baseline sane",
        "blocks_promotion": False,
        "runner_v4_state": "baseline_sanity",
    },
    {
        "rung": "G1_selector_blind_matter",
        "required_for_local_GR": "delta S_matter/delta Z_I|e=0 for nonmetric selectors",
        "current_status": "sufficient_conditional_theorem_not_parent_derived",
        "evidence": "checkpoint 401 selector-blind axiom sufficient but exp(F(C_D))e counterexample remains",
        "blocks_promotion": True,
        "runner_v4_state": "postulate_or_closure_zero",
    },
    {
        "rung": "G2_one_observed_coframe",
        "required_for_local_GR": "matter/clocks/rulers/photons use one observed metric/coframe in the local frame",
        "current_status": "closure_zero_not_derived_zero",
        "evidence": "identity branch closes direct coframe row only by label",
        "blocks_promotion": True,
        "runner_v4_state": "closure_zero",
    },
    {
        "rung": "G3_species_source_charge_universality",
        "required_for_local_GR": "no species/source/bulk/boundary/domain charge split",
        "current_status": "contingent_budget_not_parent_derived",
        "evidence": "R1 remains contingent; source-charge floor 1e-14 fails WEP-source smoke",
        "blocks_promotion": True,
        "runner_v4_state": "retained_contingent_budget",
    },
    {
        "rung": "G4_same_matter_metric_frame",
        "required_for_local_GR": "EH/operator/source theorems are stated in the same frame matter sees",
        "current_status": "conditional_only",
        "evidence": "checkpoint 402 same-frame pair available but not parent-derived",
        "blocks_promotion": True,
        "runner_v4_state": "conditional_theorem",
    },
    {
        "rung": "G5_EH_operator_selection",
        "required_for_local_GR": "local compact exterior is metric-only, 4D, local, second-order EH plus Lambda",
        "current_status": "conditional_lovelock_route_not_parent_derived",
        "evidence": "checkpoint 402 EH parent-derived gate fails",
        "blocks_promotion": True,
        "runner_v4_state": "conditional_theorem",
    },
    {
        "rung": "G6_nonEH_operator_elimination",
        "required_for_local_GR": "R2/fR/Weyl/scalar/vector/nonlocal/source operators zero or explicitly retained",
        "current_status": "retained_residual",
        "evidence": "R11 operator ledger remains retained",
        "blocks_promotion": True,
        "runner_v4_state": "retained_residual",
    },
    {
        "rung": "G7_source_normalized_measured_GM",
        "required_for_local_GR": "mu_obs=G_eff M_eff is constant, universal, conserved, and range-independent",
        "current_status": "conditional_only_not_parent_derived",
        "evidence": "checkpoint 402 source_normalization_parent_derived gate fails",
        "blocks_promotion": True,
        "runner_v4_state": "conditional_theorem",
    },
    {
        "rung": "G8_boundary_bulk_radial_nohair",
        "required_for_local_GR": "boundary/bulk radial hair absent, constant monopole, or alpha(lambda)-scored",
        "current_status": "conditional_not_parent_derived",
        "evidence": "checkpoint 403 gamma/beta/fifth-force hair family retained",
        "blocks_promotion": True,
        "runner_v4_state": "retained_budget",
    },
    {
        "rung": "G9_domain_projector_nohair",
        "required_for_local_GR": "domain/projector vector, anisotropy, topology, and stress are gauge/topological or retained",
        "current_status": "conditional_template_not_parent_derived",
        "evidence": "checkpoint 403 domain_projector_nohair_parent_derived gate fails",
        "blocks_promotion": True,
        "runner_v4_state": "retained_budget",
    },
    {
        "rung": "G10_Ward_flux_silence",
        "required_for_local_GR": "alpha3 flux channels theorem-zero, exactly Ward-cancelled, or retained",
        "current_status": "mapped_not_parent_derived",
        "evidence": "checkpoint 403 alpha3 flux ceiling 4e-20; Ward owner not derived",
        "blocks_promotion": True,
        "runner_v4_state": "retained_contingent_budget",
    },
    {
        "rung": "G11_Gdot_drift_silence",
        "required_for_local_GR": "partial_t ln(G_eff M_eff), memory, flux, and domain drift vanish or are retained",
        "current_status": "contingent_budget_not_parent_derived",
        "evidence": "checkpoint 403 Gdot drift ceiling 9.6e-15 yr^-1",
        "blocks_promotion": True,
        "runner_v4_state": "retained_contingent_budget",
    },
    {
        "rung": "G12_fifth_force_law_or_zero",
        "required_for_local_GR": "mu_extra=0 theorem or alpha(lambda), range, charge, screening profile",
        "current_status": "unscored_parameterized",
        "evidence": "R10 fifth-force remains unscored; alpha(lambda) contract missing",
        "blocks_promotion": True,
        "runner_v4_state": "unscored_parameterized",
    },
    {
        "rung": "G13_PPN_residual_vector",
        "required_for_local_GR": "gamma=beta=1, alpha_i=xi=0, no WEP/clock/Gdot/fifth-force residual",
        "current_status": "not_promoted",
        "evidence": "all non-baseline local rows remain closure/conditional/retained/budgeted/unscored",
        "blocks_promotion": True,
        "runner_v4_state": "promotion_blocked",
    },
]


STATUS_DEFINITIONS = [
    {
        "status": "verified_sanity_not_theory",
        "meaning": "pipeline sanity check passed but proves no MTS theorem",
        "promotion_policy": "supporting evidence only",
    },
    {
        "status": "closure_zero_not_derived_zero",
        "meaning": "row is zero only by explicit branch assumption",
        "promotion_policy": "not a public derivation",
    },
    {
        "status": "sufficient_conditional_theorem_not_parent_derived",
        "meaning": "mathematical theorem works if extra axiom is assumed",
        "promotion_policy": "needs parent origin",
    },
    {
        "status": "conditional_lovelock_route_not_parent_derived",
        "meaning": "EH follows under metric-only/local/second-order premises",
        "promotion_policy": "not promoted until premises are derived",
    },
    {
        "status": "retained_residual",
        "meaning": "operator/stress family remains in modified-gravity ledger",
        "promotion_policy": "blocks local-GR claim",
    },
    {
        "status": "retained_contingent_budget",
        "meaning": "guardrail applies if channel exists; channel relevance not closed",
        "promotion_policy": "no pass/fail promotion",
    },
    {
        "status": "unscored_parameterized",
        "meaning": "profile/range/coupling law missing",
        "promotion_policy": "cannot scalar-score or pass",
    },
]


DEPENDENCY_EDGES = [
    {"from_rung": "G1_selector_blind_matter", "to_rung": "G2_one_observed_coframe", "dependency": "selector-blind matter can turn coframe closure into theorem"},
    {"from_rung": "G2_one_observed_coframe", "to_rung": "G4_same_matter_metric_frame", "dependency": "same-frame theorem needs matter frame identified"},
    {"from_rung": "G4_same_matter_metric_frame", "to_rung": "G5_EH_operator_selection", "dependency": "EH must be selected in matter frame"},
    {"from_rung": "G5_EH_operator_selection", "to_rung": "G7_source_normalized_measured_GM", "dependency": "Poisson/Newton algebra needs EH-shaped equations"},
    {"from_rung": "G7_source_normalized_measured_GM", "to_rung": "G11_Gdot_drift_silence", "dependency": "Gdot closes only if measured GM is time-independent"},
    {"from_rung": "G8_boundary_bulk_radial_nohair", "to_rung": "G12_fifth_force_law_or_zero", "dependency": "radial/bulk hair must become zero or force-law scored"},
    {"from_rung": "G9_domain_projector_nohair", "to_rung": "G10_Ward_flux_silence", "dependency": "domain/projector flux feeds alpha3/Gdot hard rows"},
    {"from_rung": "G10_Ward_flux_silence", "to_rung": "G13_PPN_residual_vector", "dependency": "unowned flux blocks preferred-frame PPN pass"},
]


CLAIM_TIERS = [
    {
        "tier": "private_status",
        "allowed_claim": "MTS has a coherent conditional local-GR reduction stack and numeric residual contracts",
        "allowed": True,
    },
    {
        "tier": "internal_test_ready",
        "allowed_claim": "runner-v4 can test retained residual coefficients against source locks",
        "allowed": True,
    },
    {
        "tier": "public_WEP_derivation",
        "allowed_claim": "MTS derives WEP/one coframe",
        "allowed": False,
    },
    {
        "tier": "public_EH_Newton_derivation",
        "allowed_claim": "MTS derives EH plus Newtonian measured GM",
        "allowed": False,
    },
    {
        "tier": "public_PPN_local_GR_pass",
        "allowed_claim": "MTS reduces to local GR/PPN",
        "allowed": False,
    },
]


NEAREST_DERIVATION_TARGETS = [
    {
        "priority": 1,
        "target": "primitive relational quotient/readout parent principle",
        "pays_rungs": "G1;G2;G9;possibly G10",
        "why": "best chance to replace selector-blind matter and domain silence postulates with one origin",
    },
    {
        "priority": 2,
        "target": "total Ward flux owner/no-hair theorem",
        "pays_rungs": "G10;G11;part of G7",
        "why": "alpha3 4e-20 row is too hard for tuning; needs exact cancellation or theorem-zero",
    },
    {
        "priority": 3,
        "target": "same-frame EH/source theorem pair",
        "pays_rungs": "G4;G5;G7;G13",
        "why": "GR/Newton reduction needs EH and measured GM in the same matter frame",
    },
    {
        "priority": 4,
        "target": "alpha(lambda) fifth-force/source-charge map",
        "pays_rungs": "G8;G12",
        "why": "if hair survives, it must become a real force-law score instead of vague residual",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The local GR/Newton stack is now partitioned. Only the evaluator sanity row is verified; no physics rung is parent-derived enough for public promotion. The strongest honest private claim is that MTS has a coherent conditional stack: selector-blind matter, same-frame EH/source, boundary/domain no-hair, Ward flux silence, and fifth-force law are now exact theorem targets with numeric guardrails. The local branch is not dead, but every public GR/Newton claim remains blocked until runner-v4 can separate theorem-zero from closure-zero/postulate-zero/retained rows.",
        "physics_rungs_total": 13,
        "physics_rungs_parent_derived": 0,
        "local_GR_claim_allowed": False,
        "runner_v4_ready": True,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "convert the 405 stack statuses into runner-v4 states and outputs",
        "pass_condition": "runner-v4 distinguishes theorem_zero, postulate_zero, closure_zero, conditional, retained, contingent, and unscored rows",
    },
    {
        "priority": 2,
        "target": "407-primitive-relational-quotient-action-sketch.md",
        "task": "try a formal parent action/configuration-space sketch for the primitive quotient/readout origin",
        "pass_condition": "selector-blind matter/domain silence has a variational route or is explicitly postulated",
    },
    {
        "priority": 3,
        "target": "408-local-bound-data-runner-v4-smoke.py",
        "task": "run numeric residual coefficients with runner-v4 state labels",
        "pass_condition": "baseline and retained rows are evaluated without promoting closure rows",
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


def stack_summary_rows() -> list[dict[str, Any]]:
    rows = LOCAL_GR_STACK_RUNG_STATUS
    return [
        {"metric": "total_rungs", "value": len(rows)},
        {"metric": "baseline_sanity_rungs", "value": sum(1 for row in rows if row["runner_v4_state"] == "baseline_sanity")},
        {"metric": "physics_rungs_parent_derived", "value": 0},
        {"metric": "blocking_rungs", "value": sum(1 for row in rows if row["blocks_promotion"])},
        {"metric": "runner_v4_ready", "value": True},
        {"metric": "local_GR_claim_allowed", "value": False},
    ]


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    blocking_rungs = [row["rung"] for row in LOCAL_GR_STACK_RUNG_STATUS if row["blocks_promotion"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "local_GR_stack_partitioned",
            "status": "pass",
            "evidence": f"{len(LOCAL_GR_STACK_RUNG_STATUS)} rungs labelled",
        },
        {
            "gate": "status_definitions_written",
            "status": "pass",
            "evidence": f"{len(STATUS_DEFINITIONS)} status definitions written",
        },
        {
            "gate": "dependency_edges_written",
            "status": "pass",
            "evidence": f"{len(DEPENDENCY_EDGES)} dependency edges written",
        },
        {
            "gate": "claim_tiers_written",
            "status": "pass",
            "evidence": f"{len(CLAIM_TIERS)} claim tiers written",
        },
        {
            "gate": "physics_rungs_parent_derived",
            "status": "fail",
            "evidence": "0 physics rungs are parent-derived enough for public local-GR promotion",
        },
        {
            "gate": "blocking_rungs_retained",
            "status": "pass",
            "evidence": f"{len(blocking_rungs)} blocking rungs retained",
        },
        {
            "gate": "runner_v4_ready",
            "status": "pass",
            "evidence": "derived/closure/postulate/retained state map is ready",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "stack audit only; no GR/Newton theorem promoted",
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
    stack_rows = [
        {
            "rung": row["rung"],
            "status": row["current_status"],
            "v4_state": row["runner_v4_state"],
        }
        for row in LOCAL_GR_STACK_RUNG_STATUS
    ]
    claim_rows = [
        {
            "tier": row["tier"],
            "allowed": row["allowed"],
            "claim": row["allowed_claim"],
        }
        for row in CLAIM_TIERS
    ]
    target_rows = [
        {
            "priority": row["priority"],
            "target": row["target"],
            "pays": row["pays_rungs"],
        }
        for row in NEAREST_DERIVATION_TARGETS
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 405 - Same-Frame EH Source Derived Stack Audit

Private local-GR/Newton stack checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoints 401-404 isolated the exact local-GR blockers. This file rolls them into one stack so the project stops losing the plot in scattered caveats.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/same_frame_EH_source_derived_stack_audit.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Stack Rungs

{markdown_table(stack_rows, ["rung", "status", "v4_state"])}

## 4. Claim Tiers

{markdown_table(claim_rows, ["tier", "allowed", "claim"])}

## 5. Nearest Derivation Targets

{markdown_table(target_rows, ["priority", "target", "pays"])}

## 6. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 7. Decision

{DECISION[0]["decision"]}

Practical read: the theory is now in a much better engineering state. The problem is not vague anymore. The next useful move is not another prose derivation claim; it is runner-v4, where closure-zero and theorem-zero are different machine states.

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
    write_csv(results_dir / "local_GR_stack_rung_status.csv", LOCAL_GR_STACK_RUNG_STATUS)
    write_csv(results_dir / "status_definitions.csv", STATUS_DEFINITIONS)
    write_csv(results_dir / "dependency_edges.csv", DEPENDENCY_EDGES)
    write_csv(results_dir / "claim_tiers.csv", CLAIM_TIERS)
    write_csv(results_dir / "nearest_derivation_targets.csv", NEAREST_DERIVATION_TARGETS)
    write_csv(results_dir / "stack_summary.csv", stack_summary_rows())
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
        "local_GR_stack_rungs": len(LOCAL_GR_STACK_RUNG_STATUS),
        "physics_rungs_parent_derived": 0,
        "blocking_rungs": sum(1 for row in LOCAL_GR_STACK_RUNG_STATUS if row["blocks_promotion"]),
        "runner_v4_ready": True,
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
        description="Write checkpoint 405 local-GR derived-vs-closure stack audit artifacts."
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
