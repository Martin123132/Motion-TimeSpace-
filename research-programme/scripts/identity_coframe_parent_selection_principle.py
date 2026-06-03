from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "identity-coframe-parent-selection-principle"
STATUS = "identity_coframe_selection_principle_conditional_clean_local_GR_route_not_parent_derived_closure_label_required"
CLAIM_CEILING = "identity_coframe_selection_attempt_only_no_WEP_PPN_fifth_force_EH_source_boundary_bulk_or_local_GR_pass"
NEXT_TARGET = "390-class-metric-counterstress-nohair-contract.md"


SOURCE_DOCS = [
    {
        "path": "179-local-GR-PPN-silence-contract.md",
        "role": "minimal metric coupling and local PPN silence fence",
    },
    {
        "path": "268-projected-matter-metric-parent-action-or-closure.md",
        "role": "projected matter metric action skeleton and closure risk",
    },
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "one observed coframe direct WEP/clock vertex theorem",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe/common-F not parent-derived",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent local action contract and local-GR sufficiency stack",
    },
    {
        "path": "384-parent-action-first-variation-obstruction-map.md",
        "role": "coframe selector pullback as first parent variation obstruction",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "identity coframe as clean pullback cancellation route",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "local suppression budgets showing vague smallness is insufficient",
    },
    {
        "path": "387-identity-coframe-or-class-metric-fork.md",
        "role": "identity coframe branch prioritized; class metric demoted",
    },
    {
        "path": "388-WEP-species-symmetry-common-F-parent-selector-attempt.md",
        "role": "common-F theorem conditional; identity coframe next target",
    },
]


SELECTION_ATTEMPTS = [
    {
        "attempt": "diffeomorphism_and_local_Lorentz",
        "premise": "parent action is covariant and matter actions use local Lorentz frames",
        "result": "allows one metric/coframe but does not force ehat=e",
        "verdict": "insufficient",
        "reason": "universal conformal/class metric exp(F(C_D))e is still covariant",
    },
    {
        "attempt": "weak_equivalence_principle",
        "premise": "all freely falling test bodies follow one geometry",
        "result": "forces one observed geometry if imposed exactly, but not identity with parent metric e",
        "verdict": "empirical_principle_or_closure",
        "reason": "WEP selects universality of ehat, not whether ehat equals the metric core variable",
    },
    {
        "attempt": "strong_equivalence_minimal_metric_coupling",
        "premise": "local non-gravitational physics is special-relativistic in the same frame that defines the gravitational metric core",
        "result": "ehat=e if the metric core is also the matter clock/rod metric",
        "verdict": "conditional_theorem_if_parent_adopts_SEP",
        "reason": "this is the needed local parent principle, but it has not been derived from MTS sectors",
    },
    {
        "attempt": "no_local_class_spurion",
        "premise": "no local scalar/class/projector/bulk/boundary variable may enter the matter geometry map",
        "result": "partial ehat/partial Z_I=0 and ehat=e up to constant normalization",
        "verdict": "conditional_theorem",
        "reason": "forbids F(C_D), F_A(C_D), and selector pullbacks by action structure",
    },
    {
        "attempt": "constant_universal_normalization",
        "premise": "ehat=A0 e with A0 constant, universal, source-normalized, and time-independent",
        "result": "identity by unit choice after GM/unit absorption",
        "verdict": "conditional_support",
        "reason": "requires source-normalization/clock no-drift theorem still open after 378",
    },
    {
        "attempt": "field_redefinition_eprime_equals_ehat",
        "premise": "rename the matter coframe eprime=ehat",
        "result": "hides rather than removes class pullback unless the entire parent action is rewritten EH-only in eprime",
        "verdict": "not_a_derivation",
        "reason": "field redefinition can move couplings into gravitational/MTS sectors and PPN rows",
    },
    {
        "attempt": "representative_gauge_invariance",
        "premise": "Cperp/representative variables are gauge and invisible to matter",
        "result": "forbids representative pullback but permits physical common C_D class metric",
        "verdict": "partial_only",
        "reason": "gauge quotient cannot kill a physical class observable without local trivial-class theorem",
    },
]


IDENTITY_THEOREM_CONTRACT = [
    {
        "contract_item": "metric_core_is_observed_geometry",
        "required_statement": "the same coframe e varied in S_EH_or_metric_core is the coframe used by all matter, clocks, photons, rulers, and standards",
        "mathematical_form": "S_matter = sum_A S_A[Psi_A, e, omega[e], theta_A]",
        "current_status": "conditional premise, not parent-derived",
    },
    {
        "contract_item": "no_matter_geometry_spurions",
        "required_statement": "no class, projector, bulk, boundary, source-normalization, domain, or species spurion enters the matter geometry map",
        "mathematical_form": "partial ehat/partial Z_I = 0 for nonmetric Z_I",
        "current_status": "needed selection rule",
    },
    {
        "contract_item": "constants_class_independent",
        "required_statement": "matter constants may differ by species but are not functions of C_D or other MTS selector variables",
        "mathematical_form": "partial_Z theta_A = 0",
        "current_status": "needed for clock/WEP rows",
    },
    {
        "contract_item": "normalization_fixed",
        "required_statement": "any universal constant scaling between ehat and e is unit/GM absorbed and has no time/source/species dependence",
        "mathematical_form": "ehat=A0 e, partial_t A0=partial_r A0=Delta_A A0=0",
        "current_status": "source-normalization theorem open",
    },
    {
        "contract_item": "EH_operator_in_same_frame",
        "required_statement": "the local exterior gravitational operator is EH-only in the same metric that matter sees",
        "mathematical_form": "S_ext[e]=S_EH[e]+boundary through local PPN order",
        "current_status": "EH/operator stack still open",
    },
]


PROOF_SKETCH = [
    {
        "step": 1,
        "statement": "Assume S_matter depends on e and species-internal constants theta_A only.",
        "consequence": "No direct nonmetric MTS matter arguments exist at fixed e.",
    },
    {
        "step": 2,
        "statement": "For every nonmetric selector variable Z_I, partial e/partial Z_I=0 and partial theta_A/partial Z_I=0.",
        "consequence": "dS_matter/dZ_I=0, including the coframe-pullback term.",
    },
    {
        "step": 3,
        "statement": "Thus Pi_I^matter=(delta S_matter/delta e)(partial e/partial Z_I)=0.",
        "consequence": "WEP/coframe pullback rows move to derived-zero only if premises are parent-derived.",
    },
    {
        "step": 4,
        "statement": "If ehat=A0 e with A0 constant universal, the difference is unit normalization.",
        "consequence": "Identity can be chosen after source/clock normalization if A0 has no local/time/species dependence.",
    },
    {
        "step": 5,
        "statement": "If ehat=exp(F(C_D))e with F' not parent-zero, the proof fails.",
        "consequence": "Common-mode pullback returns in clock/gamma/fifth-force/Gdot rows.",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "WEP_universality_does_not_select_identity",
        "statement": "universal ehat can satisfy WEP while ehat differs from e by a class metric",
        "consequence": "identity requires more than one observed coframe",
    },
    {
        "no_go": "covariance_allows_class_metric",
        "statement": "S_matter[psi, exp(F(C_D))e] is covariant and local if C_D is allowed",
        "consequence": "diffeomorphism/local Lorentz invariance alone cannot force ehat=e",
    },
    {
        "no_go": "field_redefinition_not_free",
        "statement": "renaming ehat as the metric shifts MTS/class couplings into the gravitational action",
        "consequence": "must re-check EH/operator/source/PPN stack in the renamed frame",
    },
    {
        "no_go": "constant_scale_not_automatic",
        "statement": "ehat=A(C_D)e is safe only if A is constant, universal, and source-normalized",
        "consequence": "source-normalization and clock drift gates remain open",
    },
    {
        "no_go": "identity_closure_not_derivation",
        "statement": "choosing ehat=e is a powerful local branch principle but not yet produced by MTS variation",
        "consequence": "may be used as labelled closure, not local-GR proof",
    },
]


RUNNER_TRANSITIONS = [
    {
        "runner_row": "eta_WEP",
        "if_identity_parent_derived": "derived_zero for matter coframe/species geometry split",
        "current_transition": "closure_zero_if_assumed",
        "remaining_debt": "parent selector proof or source-locked eta budget",
    },
    {
        "runner_row": "alpha_clock_redshift",
        "if_identity_parent_derived": "direct class-metric clock pullback removed if constants class-independent",
        "current_transition": "conditional_zero_only",
        "remaining_debt": "constants/no-drift/source-normalization",
    },
    {
        "runner_row": "gamma_minus_1/beta_minus_1",
        "if_identity_parent_derived": "matter pullback contribution removed",
        "current_transition": "budget_only_for_EH_boundary_bulk_operator_rows",
        "remaining_debt": "EH-only exterior, boundary/bulk no-hair",
    },
    {
        "runner_row": "alpha1/alpha2/xi",
        "if_identity_parent_derived": "domain/projector coframe matter slip removed",
        "current_transition": "budget_only_for_domain_boundary_leakage",
        "remaining_debt": "covariant domain/projector and boundary no-hair",
    },
    {
        "runner_row": "Gdot/fifth_force",
        "if_identity_parent_derived": "class-metric common-mode force removed from matter coframe",
        "current_transition": "unscored_or_contingent_for_source_bulk_boundary",
        "remaining_debt": "source normalization and bulk/boundary force-law contracts",
    },
]


BRANCH_POLICY = [
    {
        "branch": "identity_coframe_as_parent_principle",
        "status": "best_local_GR_candidate",
        "allowed_claim": "conditional local WEP/coframe-pullback zero theorem",
        "forbidden_claim": "derived local GR until parent selection and EH/source/boundary/bulk stacks close",
    },
    {
        "branch": "identity_coframe_as_closure",
        "status": "allowed_labelled_closure",
        "allowed_claim": "test the remaining EH/source/boundary/bulk debts with WEP pullback closed by axiom",
        "forbidden_claim": "MTS has derived equivalence principle",
    },
    {
        "branch": "class_metric_retained",
        "status": "modified_gravity_counterstress_route",
        "allowed_claim": "retain pullback with no-hair/source-budget contract",
        "forbidden_claim": "local GR without counterstress/no-hair proof",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The identity-coframe route is mathematically sufficient to remove the observed-coframe pullback: if all matter sees the metric core coframe e, and no nonmetric MTS selector or class spurion enters matter geometry or constants, then Pi_I^matter=0 for nonmetric Z_I. However the current MTS branch has not derived the parent principle that forbids a universal class metric exp(F(C_D))e or a constant/source-normalization ambiguity. Therefore ehat=e is the clean local-GR theorem target or labelled WEP closure, not a derived local-GR result.",
        "identity_theorem_status": "conditional_sufficient_not_parent_derived",
        "recommended_branch": "use_identity_coframe_as_explicit_local_closure_when_testing_EH_stack",
        "fallback_branch": "class_metric_counterstress_nohair_contract",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "write exact no-hair/source-budget contract for the retained class-metric counterstress branch",
        "pass_condition": "class metric pullback is no-hair, source-budgeted, or demoted as modified gravity",
    },
    {
        "priority": 2,
        "target": "391-local-GR-stack-after-identity-coframe-closure.md",
        "task": "roll the local-GR stack forward assuming identity coframe as labelled closure, then isolate EH/operator/source/boundary/bulk debts",
        "pass_condition": "remaining GR-reduction blockers are listed without WEP pullback ambiguity",
    },
    {
        "priority": 3,
        "target": "392-identity-coframe-parent-action-search-manifest.md",
        "task": "search the wider corpus for any parent principle that can forbid local class spurions in matter geometry",
        "pass_condition": "existing corpus either supplies a candidate theorem route or identity coframe stays closure",
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
            "gate": "selection_attempts_written",
            "status": "pass",
            "evidence": f"{len(SELECTION_ATTEMPTS)} identity-selection routes audited",
        },
        {
            "gate": "identity_coframe_mathematically_sufficient",
            "status": "conditional_pass",
            "evidence": "Pi_I^matter=0 if ehat=e and nonmetric Z_I do not enter matter constants",
        },
        {
            "gate": "identity_parent_principle_derived",
            "status": "fail",
            "evidence": "no MTS variation currently forbids universal class metric or local class spurions",
        },
        {
            "gate": "field_redefinition_rejected_as_proof",
            "status": "pass",
            "evidence": "renaming ehat shifts debts into EH/operator/source stack",
        },
        {
            "gate": "identity_closure_label_required",
            "status": "pass",
            "evidence": "ehat=e can be used only as explicit local WEP closure unless parent-derived",
        },
        {
            "gate": "WEP_PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "identity selection attempt only; EH/source/boundary/bulk debts remain",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "selection_attempts.csv", SELECTION_ATTEMPTS)
    write_csv(results_dir / "identity_theorem_contract.csv", IDENTITY_THEOREM_CONTRACT)
    write_csv(results_dir / "proof_sketch.csv", PROOF_SKETCH)
    write_csv(results_dir / "no_go_results.csv", NO_GO_RESULTS)
    write_csv(results_dir / "runner_transitions.csv", RUNNER_TRANSITIONS)
    write_csv(results_dir / "branch_policy.csv", BRANCH_POLICY)
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
        "selection_attempts": len(SELECTION_ATTEMPTS),
        "identity_coframe_mathematically_sufficient": True,
        "identity_parent_principle_derived": False,
        "identity_closure_label_required": True,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 389 identity coframe parent selection artifacts."
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
