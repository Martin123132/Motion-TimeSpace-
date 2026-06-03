from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-GR-stack-after-identity-coframe-closure"
STATUS = "local_GR_stack_after_identity_coframe_closure_written_WEP_pullback_closed_by_label_remaining_EH_source_boundary_bulk_debts_no_local_GR_pass"
CLAIM_CEILING = "identity_closure_stack_rollup_only_no_WEP_PPN_EH_source_boundary_bulk_fifth_force_or_local_GR_pass"
NEXT_TARGET = "392-EH-operator-selection-under-identity-closure.md"


SOURCE_DOCS = [
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "EH operator selection and modified-gravity residual ledger",
    },
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "preferred-frame/vector no-hair and coefficient rows",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "source normalization and measured-GM absorption gates",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "boundary class-only/no-angular theorem and retained boundary coefficients",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X no-hair or source-normalized force-law contract",
    },
    {
        "path": "381-local-GR-debt-ledger-rollup-after-360-380.md",
        "role": "pre-identity local-GR debt ledger",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent local action sufficiency stack and residual fallbacks",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner state discipline after retained residuals",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "GR/null baseline and local suppression budgets",
    },
    {
        "path": "389-identity-coframe-parent-selection-principle.md",
        "role": "identity coframe as labelled local WEP closure, not parent-derived",
    },
    {
        "path": "390-class-metric-counterstress-nohair-contract.md",
        "role": "class-metric branch demoted to counterstress/modified gravity",
    },
]


IDENTITY_CLOSURE_ASSUMPTIONS = [
    {
        "assumption": "identity_coframe",
        "statement": "all local matter, clocks, photons, rulers, and lab standards use the metric-core coframe e",
        "mathematical_form": "S_matter = sum_A S_A[Psi_A, e, omega[e], theta_A]",
        "status": "closure_zero_not_derived_zero",
        "allowed_effect": "removes matter-coframe pullback ambiguity for this branch",
    },
    {
        "assumption": "no_nonmetric_matter_spurions",
        "statement": "nonmetric MTS selector variables do not enter matter geometry or constants",
        "mathematical_form": "partial_Z e = 0 and partial_Z theta_A = 0 for nonmetric Z",
        "status": "closure_zero_not_derived_zero",
        "allowed_effect": "closes direct WEP/clock/class-spurion rows by label",
    },
    {
        "assumption": "closure_label_visible",
        "statement": "identity coframe is never counted as parent-derived until a parent theorem source exists",
        "mathematical_form": "closure_zero != derived_zero",
        "status": "mandatory_claim_policy",
        "allowed_effect": "prevents false local-GR promotion",
    },
    {
        "assumption": "class_metric_branch_separate",
        "statement": "retained class metric is tested only as modified gravity/counterstress branch",
        "mathematical_form": "E_selector + Pi_matter = 0 plus nohair/source budgets",
        "status": "separate_branch_after_390",
        "allowed_effect": "prevents mixing branch claims",
    },
]


REMAINING_GR_STACK = [
    {
        "gate": "EH_operator_selection",
        "required_for_GR": "surviving compact exterior metric operator is EH plus boundary/Lambda through local PPN order",
        "after_identity_closure": "central remaining blocker",
        "current_state": "not_parent_derived",
        "runner_consequence": "gamma/beta/xi/operator rows remain budget or modified-gravity ledger",
    },
    {
        "gate": "source_normalized_Newtonian_limit",
        "required_for_GR": "kappa, G_eff, M_eff, and measured GM are fixed with no time/range/species dependence",
        "after_identity_closure": "still open",
        "current_state": "M_eff conditional, GM absorption not parent-derived",
        "runner_consequence": "delta_G, Gdot/G, beta, fifth-force source rows remain",
    },
    {
        "gate": "boundary_nohair",
        "required_for_GR": "boundary terms reduce to class-only constant monopole or harmless Ward-owned boundary term",
        "after_identity_closure": "still open",
        "current_state": "angular/vector no-source conditional; radial/flux open",
        "runner_consequence": "gamma, beta, alpha_i, xi, alpha3 rows remain",
    },
    {
        "gate": "bulk_X_nohair_or_force_law",
        "required_for_GR": "bulk X is theorem-zero, massive source-free no-hair, or has source-normalized alpha_X(lambda_X)",
        "after_identity_closure": "still open",
        "current_state": "mass gap and alpha_X(lambda_X) not parent-derived",
        "runner_consequence": "fifth-force remains unscored parameterized; gamma/beta bulk rows remain",
    },
    {
        "gate": "preferred_frame_domain_projector_nohair",
        "required_for_GR": "domain/projector/vector/marker data are gauge, absent, or source-free no-hair",
        "after_identity_closure": "still open",
        "current_state": "vector/domain no-hair conditional only",
        "runner_consequence": "alpha1, alpha2, alpha3, xi remain budget/contingent rows",
    },
    {
        "gate": "fifth_force_range_coupling",
        "required_for_GR": "every finite-range scalar/bulk/boundary/nonlocal force is theorem-zero or scored by alpha(lambda)",
        "after_identity_closure": "still open",
        "current_state": "alpha_Y(lambda_Y) and alpha_X(lambda_X) missing",
        "runner_consequence": "delta_G_or_fifth_force_yukawa remains unscored parameterized",
    },
    {
        "gate": "PPN_coefficient_derivation",
        "required_for_GR": "gamma=beta=1 and alpha_i=xi=0 follow from parent action, not budgets",
        "after_identity_closure": "still open",
        "current_state": "source locks exist, MTS coefficients missing",
        "runner_consequence": "no PPN pass; budget-only stress tests allowed",
    },
]


DEBT_TRANSITIONS = [
    {
        "debt": "WEP_species_geometry_split",
        "before_identity_closure": "active eta_WEP budget row",
        "after_identity_closure": "closure_zero",
        "claim_status": "closed only by labelled identity assumption, not parent theorem",
    },
    {
        "debt": "coframe_pullback_Pi_I_matter",
        "before_identity_closure": "first parent-variation obstruction",
        "after_identity_closure": "closure_zero for nonmetric Z_I",
        "claim_status": "branch assumption; derived route still open",
    },
    {
        "debt": "common_class_metric_pullback",
        "before_identity_closure": "active clock/gamma/fifth-force/Gdot branch",
        "after_identity_closure": "removed from GR-facing branch; retained separately as class-metric counterstress branch",
        "claim_status": "separate modified-gravity branch after 390",
    },
    {
        "debt": "EH_operator_selection",
        "before_identity_closure": "central blocker",
        "after_identity_closure": "central blocker",
        "claim_status": "unchanged; next theory target",
    },
    {
        "debt": "source_boundary_bulk_preferred_frame",
        "before_identity_closure": "active retained residuals",
        "after_identity_closure": "still active retained residuals",
        "claim_status": "must be theorem-zero, no-hair, source-budgeted, or unscored",
    },
]


PROMOTION_GATE_MATRIX = [
    {
        "promotion": "WEP_closed_under_identity_closure",
        "required_evidence": "labelled closure assumption ehat=e and no class spurions",
        "current_result": "conditional closure only",
        "allowed_claim": "WEP pullback closed within this branch for testing",
    },
    {
        "promotion": "WEP_parent_derived",
        "required_evidence": "parent theorem selecting ehat=e or species-blind geometry plus no common pullback",
        "current_result": "fail",
        "allowed_claim": "not allowed",
    },
    {
        "promotion": "EH_local_operator_derived",
        "required_evidence": "metric-only 4D second-order diffeo exterior with no residual operators",
        "current_result": "fail",
        "allowed_claim": "not allowed",
    },
    {
        "promotion": "Newtonian_limit_derived",
        "required_evidence": "kappa/G_eff/M_eff/measured GM source-normalization theorem",
        "current_result": "fail",
        "allowed_claim": "not allowed",
    },
    {
        "promotion": "PPN_pass",
        "required_evidence": "parent-derived coefficients satisfy gamma, beta, alpha_i, xi rows with same baseline pipeline",
        "current_result": "fail",
        "allowed_claim": "not allowed",
    },
    {
        "promotion": "local_GR_reduction",
        "required_evidence": "identity coframe derived or labelled closure plus EH/source/boundary/bulk/preferred-frame/fifth-force stack closed",
        "current_result": "fail",
        "allowed_claim": "not allowed",
    },
]


TEST_QUEUE_AFTER_IDENTITY = [
    {
        "priority": 1,
        "test_or_derivation": "EH_operator_selection_under_identity_closure",
        "rows": "gamma; beta; xi; modified-gravity operator ledger",
        "purpose": "see whether the remaining metric operator can be forced to EH once WEP pullback is closure-closed",
    },
    {
        "priority": 2,
        "test_or_derivation": "source_normalized_Newtonian_limit",
        "rows": "delta_G; Gdot/G; beta; fifth-force",
        "purpose": "derive kappa/G_eff/M_eff/measured GM or retain source-normalization residuals",
    },
    {
        "priority": 3,
        "test_or_derivation": "boundary_bulk_nohair_joint_budget",
        "rows": "gamma; beta; alpha_i; xi; fifth-force",
        "purpose": "budget boundary and bulk residuals after identity closure removes matter pullback ambiguity",
    },
    {
        "priority": 4,
        "test_or_derivation": "preferred_frame_nohair_under_identity",
        "rows": "alpha1; alpha2; alpha3; xi",
        "purpose": "separate coframe slip from domain/projector/boundary vector debts",
    },
    {
        "priority": 5,
        "test_or_derivation": "GR_null_baseline_regression",
        "rows": "all local numeric rows",
        "purpose": "keep same-pipeline GR/null sanity checks before scoring retained residuals",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "identity_closure_is_not_parent_derivation",
        "statement": "closing WEP by ehat=e as a branch assumption does not prove MTS derived the equivalence principle",
        "consequence": "WEP closure can support testing, not public local-GR claim",
    },
    {
        "no_go": "WEP_closure_does_not_imply_EH",
        "statement": "even with matter on e, the exterior metric operator can still be f(R), scalar-tensor, vector, nonlocal, or higher-curvature",
        "consequence": "EH operator selection remains the main GR-facing theorem target",
    },
    {
        "no_go": "GM_absorption_not_automatic",
        "statement": "constant universal monopole can be absorbed, but radial/time/species/range dependence cannot",
        "consequence": "source normalization remains open",
    },
    {
        "no_go": "boundary_bulk_hair_not_removed_by_WEP",
        "statement": "identity matter coupling does not kill boundary shear, flux, radial hair, or bulk X sources",
        "consequence": "boundary/bulk coefficients remain active",
    },
    {
        "no_go": "budget_tie_not_GR_reduction",
        "statement": "residuals that fit source locks are still retained modified-gravity controls unless theorem-zero",
        "consequence": "empirical robustness is allowed, but local-GR promotion is blocked",
    },
]


BRANCH_POLICY = [
    {
        "branch": "GR_facing_identity_closure",
        "definition": "use ehat=e as explicit closure to remove WEP pullback and test remaining GR stack",
        "allowed": "derive/test EH, source, boundary, bulk, preferred-frame residuals cleanly",
        "forbidden": "claim parent-derived WEP or local GR",
    },
    {
        "branch": "class_metric_counterstress",
        "definition": "retain class metric as modified-gravity/counterstress branch after 390",
        "allowed": "source-budget/no-hair tests",
        "forbidden": "borrow identity-closure WEP/local-GR claims",
    },
    {
        "branch": "full_parent_derivation",
        "definition": "future parent action derives identity coframe plus EH/source/boundary/bulk stack",
        "allowed": "candidate local-GR reduction if every gate closes",
        "forbidden": "mark complete from current evidence",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Under labelled identity-coframe closure, the WEP/coframe-pullback obstruction is closed for the GR-facing branch, but only as closure_zero. This lets the local stack move forward without class-metric ambiguity. The remaining blockers are EH operator selection, source-normalized Newtonian limit, boundary no-hair, bulk-X no-hair or force law, preferred-frame/domain no-hair, fifth-force alpha(lambda), and actual PPN coefficient derivation. No WEP parent derivation, PPN pass, EH derivation, or local-GR reduction is claimed.",
        "WEP_pullback_state": "closure_zero_not_derived_zero",
        "primary_remaining_blocker": "EH_operator_selection",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt EH/operator selection in the identity-closure branch, or retain explicit modified-gravity operator coefficients",
        "pass_condition": "EH-only exterior is parent-derived under identity closure or all non-EH operators stay in the ledger",
    },
    {
        "priority": 2,
        "target": "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "task": "derive kappa/G_eff/M_eff/measured GM map with no drift/range/species dependence",
        "pass_condition": "Newtonian source normalization is derived or delta_G/Gdot/fifth-force rows remain active",
    },
    {
        "priority": 3,
        "target": "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md",
        "task": "jointly budget boundary and bulk residuals now that matter-coframe pullback is closure-closed",
        "pass_condition": "boundary/bulk rows are theorem-zero, budgeted, or unscored with no local-GR claim",
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
            "gate": "identity_closure_assumptions_written",
            "status": "pass",
            "evidence": f"{len(IDENTITY_CLOSURE_ASSUMPTIONS)} labelled closure assumptions recorded",
        },
        {
            "gate": "WEP_pullback_closed_for_identity_branch",
            "status": "closure_pass",
            "evidence": "closed as closure_zero under ehat=e, not as parent-derived theorem",
        },
        {
            "gate": "remaining_GR_stack_written",
            "status": "pass",
            "evidence": f"{len(REMAINING_GR_STACK)} post-WEP local-GR blockers listed",
        },
        {
            "gate": "EH_operator_selection_derived",
            "status": "fail",
            "evidence": "EH-only exterior remains next theorem target",
        },
        {
            "gate": "source_boundary_bulk_stack_closed",
            "status": "fail",
            "evidence": "source normalization, boundary no-hair, and bulk-X no-hair remain open",
        },
        {
            "gate": "PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "identity closure is not a PPN/EH/local-GR pass",
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
    write_csv(results_dir / "identity_closure_assumptions.csv", IDENTITY_CLOSURE_ASSUMPTIONS)
    write_csv(results_dir / "remaining_GR_stack.csv", REMAINING_GR_STACK)
    write_csv(results_dir / "debt_transitions.csv", DEBT_TRANSITIONS)
    write_csv(results_dir / "promotion_gate_matrix.csv", PROMOTION_GATE_MATRIX)
    write_csv(results_dir / "test_queue_after_identity.csv", TEST_QUEUE_AFTER_IDENTITY)
    write_csv(results_dir / "no_go_results.csv", NO_GO_RESULTS)
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
        "identity_closure_assumptions": len(IDENTITY_CLOSURE_ASSUMPTIONS),
        "remaining_GR_stack_rows": len(REMAINING_GR_STACK),
        "WEP_pullback_state": "closure_zero_not_derived_zero",
        "EH_operator_selection_derived": False,
        "source_boundary_bulk_stack_closed": False,
        "PPN_or_local_GR_promotion_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 391 local-GR stack after identity coframe closure artifacts."
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
