from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-GR-reduction-sufficiency-stack-audit"
STATUS = "local_GR_reduction_sufficiency_stack_audit_written_identity_branch_clean_but_EH_source_boundary_bulk_domain_PPN_gates_open_runner_v3_ready_no_local_GR_pass"
CLAIM_CEILING = "local_GR_sufficiency_stack_audit_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass"
NEXT_TARGET = "397-local-bound-runner-v3-from-identity-stack.md"


SOURCE_DOCS = [
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "source locks for preferred-frame, xi, fifth-force policy, and Gdot/G",
    },
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "older preferred-frame coefficient map and vector no-hair theorem shape",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "alpha(lambda) force-law contract and GM absorption warning",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "M_eff flux theorem import and GM absorption gates",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "class-only boundary no-angular kill switch and retained boundary coefficients",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X mass-gap/no-hair and alpha_X(lambda_X) contract",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent local action contract and original local-GR sufficiency stack",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner state taxonomy for derived/conditional/closure/budget/unscored rows",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "same-pipeline GR/null sanity and source-locked local rows",
    },
    {
        "path": "391-local-GR-stack-after-identity-coframe-closure.md",
        "role": "identity closure stack and post-WEP local-GR blocker queue",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "EH operator selection under identity closure and non-EH ledger",
    },
    {
        "path": "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "role": "weak-field source-normalization algebra and GM absorption contract",
    },
    {
        "path": "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md",
        "role": "joint boundary/bulk no-hair and force/flux runner",
    },
    {
        "path": "395-preferred-frame-domain-nohair-under-identity-closure.md",
        "role": "preferred-frame/domain no-hair under identity closure",
    },
]


STATUS_LEGEND = [
    {
        "status_label": "derived_zero",
        "meaning": "a parent theorem derives zero or harmless form",
        "promotion_use": "can be used for local-GR reduction if source path is recorded",
    },
    {
        "status_label": "closure_zero",
        "meaning": "set to zero by explicit branch assumption",
        "promotion_use": "usable for branch testing, not public parent-derived claim",
    },
    {
        "status_label": "conditional_theorem",
        "meaning": "the theorem is correct if extra premises are assumed",
        "promotion_use": "cannot promote until premises are parent-derived",
    },
    {
        "status_label": "retained_residual",
        "meaning": "coefficient/operator remains in the modified-gravity ledger",
        "promotion_use": "must be scored, budgeted, or kept explicit",
    },
    {
        "status_label": "budget_ready",
        "meaning": "external/internal source lock exists but MTS coefficient is missing",
        "promotion_use": "runner can emit budget, not pass",
    },
    {
        "status_label": "unscored_parameterized",
        "meaning": "force/range/source profile missing, so no scalar score is valid",
        "promotion_use": "retain until alpha(lambda) or equivalent profile is derived",
    },
    {
        "status_label": "failed_open",
        "meaning": "required parent premise is not derived",
        "promotion_use": "blocks local-GR promotion",
    },
]


LOCAL_GR_SUFFICIENCY_STACK = [
    {
        "rung": 1,
        "premise": "identity_or_parent_selected_observed_coframe",
        "required_for_local_GR": "all matter, photons, clocks, rulers, and standards see one metric/coframe",
        "current_status": "closure_zero",
        "evidence_checkpoint": "391;395",
        "residual_if_not_promoted": "WEP/clock/coframe claims remain branch-labelled, not parent-derived",
        "runner_v3_state": "closure_zero_not_derived_zero",
    },
    {
        "rung": 2,
        "premise": "EH_operator_selection",
        "required_for_local_GR": "surviving compact exterior metric operator is EH plus Lambda and harmless boundary/topological terms",
        "current_status": "failed_open",
        "evidence_checkpoint": "392",
        "residual_if_not_promoted": "non-EH operator ledger retained: R2/fR/Weyl/scalar/vector/nonlocal/source operators",
        "runner_v3_state": "retained_residual_operator_coefficients",
    },
    {
        "rung": 3,
        "premise": "source_normalized_Newtonian_limit",
        "required_for_local_GR": "kappa_eff, G_eff, M_eff, measured GM, range/time/species independence fixed",
        "current_status": "conditional_theorem",
        "evidence_checkpoint": "393",
        "residual_if_not_promoted": "delta_G, Gdot/G, beta, fifth-force, WEP-source exits remain",
        "runner_v3_state": "retained_source_normalization_rows",
    },
    {
        "rung": 4,
        "premise": "boundary_nohair",
        "required_for_local_GR": "boundary data reduce to class-only harmless terms or constant universal monopole with Ward-owned flux",
        "current_status": "conditional_theorem",
        "evidence_checkpoint": "379;394",
        "residual_if_not_promoted": "eps_B_TF, eps_B0i, eps_B_rad, eps_B_flux retained",
        "runner_v3_state": "retained_boundary_coefficients",
    },
    {
        "rung": 5,
        "premise": "bulk_X_nohair_or_scored_force",
        "required_for_local_GR": "bulk X is theorem-zero by positive source-free mass gap, or alpha_X(lambda_X) is derived and scored",
        "current_status": "unscored_parameterized",
        "evidence_checkpoint": "380;394",
        "residual_if_not_promoted": "bulk-X fifth-force/gamma/beta/delta_G residual retained",
        "runner_v3_state": "retained_bulk_X_or_unscored_force_law",
    },
    {
        "rung": 6,
        "premise": "preferred_frame_domain_projector_nohair",
        "required_for_local_GR": "domain/projector/vector/marker/flux residues are gauge, topological, Ward-owned, or zero",
        "current_status": "budget_ready",
        "evidence_checkpoint": "376;395",
        "residual_if_not_promoted": "alpha1, alpha2, alpha3, xi, Gdot/G retained as budget/contingent rows",
        "runner_v3_state": "retained_preferred_frame_domain_rows",
    },
    {
        "rung": 7,
        "premise": "fifth_force_range_coupling",
        "required_for_local_GR": "every finite-range scalar/bulk/boundary/nonlocal force is theorem-zero or alpha(lambda)-scored",
        "current_status": "unscored_parameterized",
        "evidence_checkpoint": "377;393;394",
        "residual_if_not_promoted": "delta_G_or_fifth_force_yukawa remains unscored parameterized",
        "runner_v3_state": "unscored_parameterized_force_row",
    },
    {
        "rung": 8,
        "premise": "PPN_coefficient_derivation",
        "required_for_local_GR": "gamma=beta=1, alpha_i=xi=0, no fifth force, no Gdot/G by parent action",
        "current_status": "budget_ready",
        "evidence_checkpoint": "386;392;393;394;395",
        "residual_if_not_promoted": "all local rows can be budgeted, but no PPN pass is claimable",
        "runner_v3_state": "runner_ready_no_promotion",
    },
    {
        "rung": 9,
        "premise": "total_Ward_force_closure",
        "required_for_local_GR": "all selector/projector/domain/boundary/bulk/source fluxes vanish, cancel, or are explicitly retained",
        "current_status": "retained_residual",
        "evidence_checkpoint": "382;394;395",
        "residual_if_not_promoted": "alpha3, Gdot/G, beta, source drift, and fake-Bianchi hazards retained",
        "runner_v3_state": "retained_Ward_flux_rows",
    },
]


PROMOTION_GATE_MATRIX = [
    {
        "promotion": "identity_branch_testing",
        "required_evidence": "ehat=e branch label plus no direct matter/coframe pullback",
        "current_result": "allowed_internal",
        "allowed_claim": "identity-branch local runner can be tested",
        "forbidden_claim": "parent-derived WEP",
    },
    {
        "promotion": "WEP_parent_derived",
        "required_evidence": "parent action selects one coframe for all matter rather than closure label",
        "current_result": "fail",
        "allowed_claim": "none",
        "forbidden_claim": "public WEP pass",
    },
    {
        "promotion": "EH_local_operator",
        "required_evidence": "metric-only local 4D second-order exterior with all non-EH coefficients theorem-zero or harmless",
        "current_result": "fail",
        "allowed_claim": "conditional theorem shape only",
        "forbidden_claim": "Einstein-Hilbert derived",
    },
    {
        "promotion": "source_normalized_Newtonian_limit",
        "required_evidence": "kappa/G_eff/M_eff/measured GM constant universal absorption derived",
        "current_result": "fail",
        "allowed_claim": "weak-field algebra and conditional source contract",
        "forbidden_claim": "Newtonian reduction derived",
    },
    {
        "promotion": "boundary_bulk_nohair",
        "required_evidence": "class-only boundary, Ward-owned flux, positive source-free bulk-X or alpha_X(lambda_X)",
        "current_result": "fail",
        "allowed_claim": "conditional kill switches and retained coefficients",
        "forbidden_claim": "boundary/bulk no-hair pass",
    },
    {
        "promotion": "preferred_frame_domain_pass",
        "required_evidence": "domain/projector/vector residues theorem-zero, pure gauge, topological, or Ward-owned",
        "current_result": "fail",
        "allowed_claim": "source-locked budget rows",
        "forbidden_claim": "preferred-frame PPN pass",
    },
    {
        "promotion": "fifth_force_pass",
        "required_evidence": "alpha(lambda), source/test charge, range/coupling, or theorem-zero for every finite-range channel",
        "current_result": "fail",
        "allowed_claim": "parameterized unscored row",
        "forbidden_claim": "fifth-force constraint passed",
    },
    {
        "promotion": "local_GR_reduction",
        "required_evidence": "all prior promotions derived or closure-labelled plus all retained residuals controlled without hidden claims",
        "current_result": "fail",
        "allowed_claim": "coherent local-GR programme with runner-v3 readiness",
        "forbidden_claim": "MTS reduces to GR locally",
    },
]


OBSERVABLE_ROW_ROLLUP = [
    {
        "observable_row": "eta_WEP",
        "source_lock_or_status": "closure-zero inside identity branch; not parent-derived",
        "active_sources_after_396": "source-charge universality if boundary/bulk/source charges survive",
        "runner_v3_policy": "closure_zero for direct coframe row; guarded source-charge note",
    },
    {
        "observable_row": "alpha_clock_redshift",
        "source_lock_or_status": "3.1e-5 budget row",
        "active_sources_after_396": "nonlocal/source drift/class-metric counterstress branch outside identity",
        "runner_v3_policy": "budget or closure-dependent, no pass",
    },
    {
        "observable_row": "gamma_minus_1",
        "source_lock_or_status": "2.3e-5 budget row",
        "active_sources_after_396": "non-EH operators, boundary shear/radial hair, bulk-X, domain/projector stress",
        "runner_v3_policy": "retained budget-only",
    },
    {
        "observable_row": "beta_minus_1",
        "source_lock_or_status": "7.8e-5/8e-5 budget row",
        "active_sources_after_396": "source normalization, boundary radial/flux, nonlinear bulk/source hair",
        "runner_v3_policy": "retained budget-only",
    },
    {
        "observable_row": "alpha1",
        "source_lock_or_status": "1.0e-4 internal; 4.0e-5 stricter context retained",
        "active_sources_after_396": "B0i, domain vector, projector vector, marker leakage",
        "runner_v3_policy": "retained budget-only",
    },
    {
        "observable_row": "alpha2",
        "source_lock_or_status": "2.0e-9",
        "active_sources_after_396": "B0i, domain vector/aniso, projector vector",
        "runner_v3_policy": "retained budget-only",
    },
    {
        "observable_row": "alpha3",
        "source_lock_or_status": "4.0e-20 contingent",
        "active_sources_after_396": "unowned boundary/bulk/domain/projector flux or momentum nonconservation",
        "runner_v3_policy": "contingent budget-only if channel exists",
    },
    {
        "observable_row": "xi",
        "source_lock_or_status": "4.0e-9",
        "active_sources_after_396": "boundary trace-free shear, domain anisotropy, topology cycles, external-domain anisotropy",
        "runner_v3_policy": "retained budget-only; keep separate from gamma",
    },
    {
        "observable_row": "Gdot_over_G",
        "source_lock_or_status": "9.6e-15 yr^-1 contingent",
        "active_sources_after_396": "time-varying G_eff/M_eff, memory kernels, unowned flux, domain scale drift",
        "runner_v3_policy": "contingent budget-only if time-drift channel exists",
    },
    {
        "observable_row": "delta_G_or_fifth_force_yukawa",
        "source_lock_or_status": "alpha(lambda) required; not scalar-scored",
        "active_sources_after_396": "bulk-X, boundary radial hair, scalar/class/nonlocal source-normalization residues",
        "runner_v3_policy": "unscored parameterized until range/coupling/source charge derived",
    },
]


THEOREM_VS_CLOSURE_INVENTORY = [
    {
        "item": "identity coframe",
        "type": "closure_zero",
        "earned_value": "removes direct coframe pullback for identity-branch testing",
        "remaining_debt": "parent selection theorem if public WEP/local-GR claim is desired",
    },
    {
        "item": "EH operator theorem",
        "type": "conditional_theorem",
        "earned_value": "right Lovelock-style sufficiency shape written",
        "remaining_debt": "derive metric-only local 4D second-order exterior and delete/score non-EH operators",
    },
    {
        "item": "Newtonian source algebra",
        "type": "conditional_theorem",
        "earned_value": "kappa_eff -> G_eff -> Poisson -> mu_obs contract explicit",
        "remaining_debt": "derive constant universal measured-GM absorption",
    },
    {
        "item": "class-only boundary kill switch",
        "type": "conditional_theorem",
        "earned_value": "kills angular/vector boundary sources if parent-derived",
        "remaining_debt": "radial hair, flux ownership, and parent class-only boundary action",
    },
    {
        "item": "bulk-X mass-gap kill switch",
        "type": "conditional_theorem",
        "earned_value": "kills regular source-free massive X if premises hold",
        "remaining_debt": "m_X, source-free exterior, boundary data, alpha_X(lambda_X) if sourced",
    },
    {
        "item": "preferred-frame/domain split",
        "type": "budget_ready",
        "earned_value": "coframe slip not double-counted; domain/projector residues kept honest",
        "remaining_debt": "domain selector, projector gauge status, topology-cycle silence, Ward flux",
    },
    {
        "item": "local runner v2 sanity",
        "type": "budget_ready",
        "earned_value": "GR/null baseline and source locks are usable",
        "remaining_debt": "runner-v3 must encode identity closure and retained post-396 residual vector",
    },
]


RUNNER_V3_READINESS = [
    {
        "runner_component": "same_pipeline_GR_null_baseline",
        "input_status": "ready_from_386",
        "needed_change_for_v3": "keep GR/null zero residual sanity and do not compare MTS-only jackknife without baseline",
    },
    {
        "runner_component": "identity_branch_labels",
        "input_status": "ready_from_391_395",
        "needed_change_for_v3": "mark direct WEP/coframe slip as closure_zero, not derived_zero",
    },
    {
        "runner_component": "operator_residuals",
        "input_status": "ready_from_392",
        "needed_change_for_v3": "retain non-EH coefficients as symbolic rows rather than claiming EH",
    },
    {
        "runner_component": "source_normalization_rows",
        "input_status": "ready_from_393",
        "needed_change_for_v3": "emit delta_mu/mu amplitude laws and keep delta_G/Gdot/fifth-force exits active",
    },
    {
        "runner_component": "boundary_bulk_rows",
        "input_status": "ready_from_394",
        "needed_change_for_v3": "emit q_BX residual families and alpha_X/alpha_B unscored force contracts",
    },
    {
        "runner_component": "preferred_frame_domain_rows",
        "input_status": "ready_from_395",
        "needed_change_for_v3": "separate identity-closed coframe slip from retained alpha_i/xi domain/projector rows",
    },
    {
        "runner_component": "promotion_policy",
        "input_status": "ready_from_396",
        "needed_change_for_v3": "no model/branch marked pass if any residual is closure-only, conditional, retained, or unscored",
    },
]


FAILURE_TO_ACTION_MAP = [
    {
        "blocker": "EH_operator_parent_derived_false",
        "next_action": "retain non-EH operator ledger in runner-v3 and/or write parent operator-selection contract v2",
        "claim_policy": "no EH claim",
    },
    {
        "blocker": "GM_absorption_parent_derived_false",
        "next_action": "retain delta_G/Gdot/source-normalization rows and require constant universal monopole proof",
        "claim_policy": "no Newtonian source pass",
    },
    {
        "blocker": "boundary_bulk_nohair_parent_derived_false",
        "next_action": "retain q_BX and boundary/bulk coefficient families",
        "claim_policy": "no no-hair pass",
    },
    {
        "blocker": "domain_projector_nohair_parent_derived_false",
        "next_action": "retain alpha_i/xi/domain/projector maps",
        "claim_policy": "no preferred-frame pass",
    },
    {
        "blocker": "alpha_lambda_missing",
        "next_action": "keep fifth-force row unscored parameterized until alpha(lambda), range, source/test charge exist",
        "claim_policy": "no fifth-force pass",
    },
    {
        "blocker": "PPN_coefficients_missing",
        "next_action": "run budget-only diagnostics and compare same-pipeline GR/null baseline",
        "claim_policy": "no PPN pass",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The identity branch is now clean enough for runner-v3, but it is not a derived local-GR reduction. Direct coframe/WEP pullback is closure-zero by label; EH operator selection, source-normalized Newtonian limit, boundary/bulk no-hair, domain/projector preferred-frame no-hair, fifth-force alpha(lambda), and PPN coefficient derivation remain conditional, retained, budget-only, or unscored. This is good progress: the local-GR programme is coherent and test-ready as a disciplined residual stack, but no WEP/EH/Newton/PPN/fifth-force/boundary/bulk/domain/local-GR pass is claimable.",
        "identity_branch_runner_ready": True,
        "derived_local_GR_claim_allowed": False,
        "runner_v3_next": True,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "implement local runner v3 from the post-identity sufficiency stack",
        "pass_condition": "same-pipeline GR/null baseline and all retained identity/EH/source/boundary/bulk/domain rows emitted without promotion",
    },
    {
        "priority": 2,
        "target": "398-parent-action-contract-v2-after-identity-stack.md",
        "task": "write the exact parent action obligations needed to turn closure/conditional rows into derived rows",
        "pass_condition": "future parent action contract names every missing variation, Ward identity, and operator/source/no-hair condition",
    },
    {
        "priority": 3,
        "target": "399-local-GR-status-for-human-review.md",
        "task": "write a concise private status memo: strongest progress, remaining debts, and next empirical/theory tests",
        "pass_condition": "human-readable project overview with no public overclaim",
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
    non_derived_rungs = [
        row for row in LOCAL_GR_SUFFICIENCY_STACK if row["current_status"] != "derived_zero"
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "status_legend_written",
            "status": "pass",
            "evidence": f"{len(STATUS_LEGEND)} status classes recorded",
        },
        {
            "gate": "local_GR_stack_classified",
            "status": "pass",
            "evidence": f"{len(LOCAL_GR_SUFFICIENCY_STACK)} local-GR sufficiency rungs classified",
        },
        {
            "gate": "identity_branch_runner_ready",
            "status": "pass",
            "evidence": "identity/coframe closure, retained residual rows, and no-promotion policy are explicit",
        },
        {
            "gate": "non_derived_rungs_remain",
            "status": "fail",
            "evidence": ";".join(row["premise"] for row in non_derived_rungs),
        },
        {
            "gate": "observable_rollup_written",
            "status": "pass",
            "evidence": f"{len(OBSERVABLE_ROW_ROLLUP)} local observable rows rolled up",
        },
        {
            "gate": "runner_v3_readiness_written",
            "status": "pass",
            "evidence": f"{len(RUNNER_V3_READINESS)} runner-v3 components specified",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "EH/source/boundary/bulk/domain/fifth-force/PPN premises remain conditional, retained, budget-only, or unscored",
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
    write_csv(results_dir / "status_legend.csv", STATUS_LEGEND)
    write_csv(results_dir / "local_GR_sufficiency_stack.csv", LOCAL_GR_SUFFICIENCY_STACK)
    write_csv(results_dir / "promotion_gate_matrix.csv", PROMOTION_GATE_MATRIX)
    write_csv(results_dir / "observable_row_rollup.csv", OBSERVABLE_ROW_ROLLUP)
    write_csv(results_dir / "theorem_vs_closure_inventory.csv", THEOREM_VS_CLOSURE_INVENTORY)
    write_csv(results_dir / "runner_v3_readiness.csv", RUNNER_V3_READINESS)
    write_csv(results_dir / "failure_to_action_map.csv", FAILURE_TO_ACTION_MAP)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    non_derived_rungs = [
        row["premise"]
        for row in LOCAL_GR_SUFFICIENCY_STACK
        if row["current_status"] != "derived_zero"
    ]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "sufficiency_rungs": len(LOCAL_GR_SUFFICIENCY_STACK),
        "non_derived_rungs": non_derived_rungs,
        "identity_branch_runner_ready": True,
        "derived_local_GR_claim_allowed": False,
        "runner_v3_next": True,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 396 local-GR reduction sufficiency stack audit artifacts."
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
