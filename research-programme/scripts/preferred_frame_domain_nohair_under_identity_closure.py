from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "preferred-frame-domain-nohair-under-identity-closure"
STATUS = "preferred_frame_domain_nohair_under_identity_written_coframe_slip_closed_by_label_domain_projector_vector_residues_retained_no_PPN_or_local_GR_pass"
CLAIM_CEILING = "preferred_frame_domain_nohair_under_identity_only_no_preferred_frame_PPN_domain_projector_or_local_GR_pass"
NEXT_TARGET = "396-local-GR-reduction-sufficiency-stack-audit.md"


SOURCE_DOCS = [
    {
        "path": "207-domain-projector-action-and-Bianchi-identity.md",
        "role": "formal variational domain/projector action and Bianchi bookkeeping if all stresses are retained",
    },
    {
        "path": "208-domain-representative-selection-law.md",
        "role": "conditional domain representative law and missing parent domain scale/transition selection",
    },
    {
        "path": "242-strict-local-coframe-branch-or-domain-projector-action.md",
        "role": "strict local coframe branch and domain projector retained for cosmology unless parent-derived locally",
    },
    {
        "path": "276-coherent-domain-projector-from-parent-variables.md",
        "role": "fixed-domain coherent projection derived; physical domain selector remains open",
    },
    {
        "path": "293-domain-topology-selection-attempt.md",
        "role": "domain topology/cycle selection conditional, H1/H2 vector-like sectors not parent-forbidden",
    },
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "boundary primitive/admissibility condition and physical domain/class selection still open",
    },
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "source locks for alpha1, alpha2, alpha3, xi, and contingent Gdot/G",
    },
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "preferred-frame coefficient map and conditional vector no-hair theorem",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "same-pipeline local runner sanity and preferred-frame source locks",
    },
    {
        "path": "391-local-GR-stack-after-identity-coframe-closure.md",
        "role": "identity coframe closure as branch label, not parent-derived theorem",
    },
    {
        "path": "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md",
        "role": "boundary/bulk residuals retained; B0i, B_TF, flux, and domain residues feed preferred-frame rows",
    },
]


IDENTITY_BRANCH_VECTOR_SPLIT = [
    {
        "channel": "coframe_slip",
        "mathematical_form": "delta ehat^i := ehat^i - e^i",
        "identity_branch_status": "closure_zero_not_derived_zero",
        "observable_rows": "alpha1; clock; WEP",
        "policy": "closed only inside identity branch; do not count as parent-derived vector no-hair",
    },
    {
        "channel": "boundary_vector_B0i",
        "mathematical_form": "B_0i",
        "identity_branch_status": "retained",
        "observable_rows": "alpha1; alpha2; alpha3_if_flux",
        "policy": "zero only if class-only/no-marker boundary theorem is parent-derived",
    },
    {
        "channel": "domain_vector",
        "mathematical_form": "u_D^i, n_D^i, or local domain velocity/normal",
        "identity_branch_status": "retained",
        "observable_rows": "alpha1; alpha2; xi",
        "policy": "zero only if domain selector is scalar/topological/covariant with no physical vector marker",
    },
    {
        "channel": "projector_vector_leakage",
        "mathematical_form": "P_D^i or representative vector of relative-chain/projector data",
        "identity_branch_status": "retained",
        "observable_rows": "alpha1; alpha2; xi; gamma_if_stress",
        "policy": "zero only if projector is metric-independent/topological or all projector stress is retained and budgeted",
    },
    {
        "channel": "domain_anisotropy",
        "mathematical_form": "D_l>=2, external domain anisotropy, H1/H2 cycle data",
        "identity_branch_status": "retained",
        "observable_rows": "xi; gamma; lensing_slip",
        "policy": "zero only if topology/representative/boundary Euler theorem removes anisotropic modes",
    },
    {
        "channel": "unowned_flux",
        "mathematical_form": "F_domain^i + F_projector^i + n_mu B^{mu i}",
        "identity_branch_status": "retained",
        "observable_rows": "alpha3; Gdot/G; secular_drift; beta",
        "policy": "zero only if total Ward identity owns the flux",
    },
]


DOMAIN_PROJECTOR_NOHAIR_CONTRACT = [
    {
        "premise": "scalar_or_topological_domain_selector",
        "required_statement": "domain selection depends only on invariant scalar/topological data, not a local velocity/normal vector",
        "would_kill": "eps_domain_vec; eps_external_domain_aniso",
        "current_status": "not_parent_derived",
    },
    {
        "premise": "metric_independent_projector_or_retained_stress",
        "required_statement": "P_D is topological/metric-independent, or its stress T_Pi/T_D/T_boundary is retained in the equations",
        "would_kill": "fake Bianchi closure and hidden projector vector force",
        "current_status": "conditional_formal_action_only",
    },
    {
        "premise": "representative_invariance",
        "required_statement": "matter and local observables depend only on invariant C_D/P_D C, not angular/vector representatives",
        "would_kill": "representative vector leakage and anisotropic class response",
        "current_status": "open",
    },
    {
        "premise": "topology_cycle_silence",
        "required_statement": "H1/H2 vector/cavity/cycle memory sectors are absent, pure gauge, or source-budgeted",
        "would_kill": "domain vector/cavity preferred-location modes",
        "current_status": "not_parent_derived",
    },
    {
        "premise": "free_boundary_Euler_no_vector_normal",
        "required_statement": "domain boundary variation selects an admissible class without a physical preferred normal/patch marker",
        "would_kill": "normal-frame and boundary-domain marker residues",
        "current_status": "admissibility_conditional_physical_selection_open",
    },
    {
        "premise": "Ward_owned_domain_flux",
        "required_statement": "domain/projector/boundary flux is zero or exactly balanced in the total Ward ledger",
        "would_kill": "alpha3, Gdot/G, secular drift, fake source-normalization conservation",
        "current_status": "mapped_not_proved",
    },
]


PREFERRED_FRAME_COEFFICIENT_MAP_UNDER_IDENTITY = [
    {
        "residual": "preferred_frame_alpha1",
        "source_lock": "1.0e-4 internal conservative row; 4.0e-5 stricter context retained",
        "symbolic_map_under_identity": "alpha1 = C1B eps_B0i + C1D eps_domain_vec + C1P eps_P_vector + C1M eps_marker",
        "closed_terms": "eps_coframe_slip closed by identity label only",
        "equal_share_ceiling": "2.5e-5 for four retained terms; 1.0e-5 under stricter context",
        "state": "budget_only_coefficients_missing",
    },
    {
        "residual": "preferred_frame_alpha2",
        "source_lock": "2.0e-9",
        "symbolic_map_under_identity": "alpha2 = C2B eps_B0i + C2D eps_domain_vec + C2A eps_domain_aniso + C2P eps_P_vector",
        "closed_terms": "direct coframe anisotropic slip closed by identity label only",
        "equal_share_ceiling": "5.0e-10 for four retained terms",
        "state": "budget_only_coefficients_missing",
    },
    {
        "residual": "preferred_frame_alpha3",
        "source_lock": "4.0e-20 contingent",
        "symbolic_map_under_identity": "alpha3 = C3F eps_unowned_flux + C3D eps_domain_momentum_drift + C3B eps_boundary_flux",
        "closed_terms": "none; use only if momentum-nonconservation/preferred-frame channel exists",
        "equal_share_ceiling": "1.33e-20 for three retained terms, contingent",
        "state": "contingent_budget_only",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "source_lock": "4.0e-9",
        "symbolic_map_under_identity": "xi = CxiTF eps_B_TF_l>=2 + CxiD eps_domain_aniso + CxiExt eps_external_domain_aniso + CxiTopo eps_H1H2_cycle",
        "closed_terms": "none from identity closure",
        "equal_share_ceiling": "1.0e-9 for four retained terms",
        "state": "budget_only_coefficients_missing",
    },
    {
        "residual": "Gdot_over_G",
        "source_lock": "9.6e-15 yr^-1 contingent",
        "symbolic_map_under_identity": "Gdot/G = CGF eps_unowned_flux_dot + CGD eps_domain_scale_dot + CGM eps_Meff_dot + CGK eps_memory_kernel_drift",
        "closed_terms": "none from identity closure",
        "equal_share_ceiling": "2.4e-15 yr^-1 for four retained terms, contingent",
        "state": "contingent_budget_only",
    },
]


DOMAIN_TO_OBSERVABLE_LEDGER = [
    {
        "domain_piece": "fixed_domain_coherent_projection",
        "status": "mathematically_sharpened",
        "local_risk": "does not derive physical domain selector",
        "observable_rows": "none if fixed/gauge; xi/gamma if physical anisotropy leaks",
    },
    {
        "domain_piece": "physical_domain_selector",
        "status": "not_parent_derived",
        "local_risk": "can introduce preferred local frame/normal or tuned domain scale",
        "observable_rows": "alpha1; alpha2; xi",
    },
    {
        "domain_piece": "domain_boundary_Euler",
        "status": "admissibility_conditional_physical_selection_open",
        "local_risk": "boundary normal/patch marker becomes physical",
        "observable_rows": "alpha1; alpha2; alpha3; xi",
    },
    {
        "domain_piece": "H1_H2_cycles_or_cavity_modes",
        "status": "not_parent_forbidden",
        "local_risk": "vector/cycle memory creates preferred-location or preferred-frame hair",
        "observable_rows": "xi; alpha1; alpha2",
    },
    {
        "domain_piece": "projector_stress_dropped",
        "status": "forbidden_shortcut",
        "local_risk": "fake Bianchi closure or hidden source drift",
        "observable_rows": "alpha3; Gdot/G; beta",
    },
    {
        "domain_piece": "representative_dependent_matter_action",
        "status": "open_but_direct_coframe_branch_excludes_matter_geometry_dependence_by_label",
        "local_risk": "clock/WEP/preferred-frame channels reopen outside identity branch",
        "observable_rows": "clock; eta_WEP; alpha1",
    },
]


NOHAIR_OR_BUDGET_DECISION_TREE = [
    {
        "condition": "coframe vector slip only",
        "decision": "closure_zero_inside_identity_branch",
        "reason": "ehat=e by branch label",
        "forbidden_inference": "parent-derived WEP/vector no-hair",
    },
    {
        "condition": "domain/projector vector pure gauge or topological",
        "decision": "derived_zero_if_parent_action_proves_gauge_status",
        "reason": "no physical local vector remains",
        "forbidden_inference": "assuming covariance alone proves this",
    },
    {
        "condition": "domain/projector stress retained and source-locked",
        "decision": "budget_only",
        "reason": "physical but testable residual coefficient exists",
        "forbidden_inference": "dropping stress after using projector",
    },
    {
        "condition": "unowned flux or momentum nonconservation",
        "decision": "contingent_budget_alpha3_Gdot",
        "reason": "only score if channel exists, but cannot erase without Ward owner",
        "forbidden_inference": "using alpha3 as unconditional penalty or ignoring it completely",
    },
    {
        "condition": "domain anisotropy or topology cycles survive",
        "decision": "budget_xi_and_related_gamma_slip",
        "reason": "preferred-location anisotropy is not the same row as gamma",
        "forbidden_inference": "folding xi into gamma only",
    },
]


RUNNER_POLICY_ROWS = [
    {
        "runner_row": "alpha1",
        "state_after_395": "retained_budget_only",
        "policy": "coframe slip removed by identity label; boundary/domain/projector/marker terms retained",
    },
    {
        "runner_row": "alpha2",
        "state_after_395": "retained_budget_only",
        "policy": "domain anisotropy and boundary/projector vector terms retained",
    },
    {
        "runner_row": "alpha3",
        "state_after_395": "retained_contingent_budget",
        "policy": "apply only to actual unowned flux/momentum-drift channels; do not claim Ward ownership",
    },
    {
        "runner_row": "xi",
        "state_after_395": "retained_budget_only",
        "policy": "domain anisotropy, boundary shear, external-domain, and topology-cycle residues retained",
    },
    {
        "runner_row": "Gdot_over_G",
        "state_after_395": "retained_contingent_budget",
        "policy": "domain scale drift, unowned flux drift, memory-kernel drift, and source-normalization drift remain contingent",
    },
    {
        "runner_row": "local_GR_reduction",
        "state_after_395": "fail_promotion",
        "policy": "preferred-frame/domain no-hair not parent-derived",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "covariance_does_not_kill_physical_domain_vectors",
        "statement": "A covariant action can still contain a physical vector, marker, domain normal, or aether-like field.",
        "consequence": "domain/projector vector gauge status must be derived, not assumed.",
    },
    {
        "no_go": "identity_coframe_does_not_kill_domain_anisotropy",
        "statement": "ehat=e removes coframe slip but does not remove domain vectors, boundary shear, topology cycles, or projector stress.",
        "consequence": "alpha_i and xi rows remain active after identity closure.",
    },
    {
        "no_go": "formal_projector_Bianchi_is_not_physical_selector",
        "statement": "Writing a variational projector action closes bookkeeping only if all stresses are kept; it does not select the physical domain.",
        "consequence": "domain selector and domain-scale debts remain.",
    },
    {
        "no_go": "xi_is_not_gamma",
        "statement": "Preferred-location anisotropy cannot be hidden inside ordinary gamma/slip bookkeeping.",
        "consequence": "xi keeps its own source-locked row.",
    },
    {
        "no_go": "alpha3_is_contingent_not_optional",
        "statement": "alpha3 is only relevant if a momentum-nonconservation/preferred-frame flux channel exists, but such a channel cannot be erased without a Ward owner.",
        "consequence": "alpha3 remains a contingent guardrail.",
    },
]


GATE_POLICY = [
    {
        "gate": "identity_coframe_slip_closed_by_label",
        "current_result": "closure_pass",
        "meaning": "direct observed-coframe vector slip is removed inside the identity branch",
        "claim_policy": "not parent-derived vector no-hair",
    },
    {
        "gate": "domain_projector_nohair_parent_derived",
        "current_result": "fail",
        "meaning": "domain selector, projector gauge status, topology-cycle silence, and boundary Euler selection remain open",
        "claim_policy": "no preferred-frame/domain pass",
    },
    {
        "gate": "preferred_frame_coefficient_map_updated",
        "current_result": "pass",
        "meaning": "alpha1/alpha2/alpha3/xi/Gdot maps now separate identity-closed coframe from retained domain/projector residues",
        "claim_policy": "budget runner only",
    },
    {
        "gate": "Ward_flux_owned",
        "current_result": "fail",
        "meaning": "domain/projector/boundary flux is mapped but not proven owned",
        "claim_policy": "alpha3/Gdot remain contingent",
    },
    {
        "gate": "residuals_retained",
        "current_result": "pass",
        "meaning": "domain/projector/vector residues feed explicit local rows",
        "claim_policy": "testable modified-gravity residual branch retained",
    },
    {
        "gate": "local_GR_promoted",
        "current_result": "fail",
        "meaning": "preferred-frame/domain no-hair is not parent-derived",
        "claim_policy": "no local-GR claim",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Under identity closure, direct coframe vector slip is closed by branch label, but preferred-frame/domain no-hair is not derived. Boundary vector hair, domain selector vectors, projector representative leakage, domain anisotropy, H1/H2 topology cycles, and unowned domain/projector/boundary flux remain retained residuals. The alpha1, alpha2, alpha3, xi, and contingent Gdot/G coefficient maps are updated so identity-closed coframe terms are not double-counted while real domain/projector residues stay budgeted. No preferred-frame, PPN, domain-projector, or local-GR pass is claimed.",
        "coframe_slip_state": "closure_zero_not_derived_zero",
        "domain_projector_nohair_parent_derived": False,
        "preferred_frame_residuals_retained": True,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "roll up identity, EH, source, boundary, bulk, preferred-frame, and domain gates into one local-GR sufficiency audit",
        "pass_condition": "every local-GR premise is classified as derived, closure-only, conditional, retained, failed, or ready for runner-v3",
    },
    {
        "priority": 2,
        "target": "397-local-bound-runner-v3-from-identity-stack.md",
        "task": "update the local runner with identity-branch closures and retained source/boundary/bulk/domain residuals",
        "pass_condition": "same-pipeline GR/null baseline plus retained rows are emitted without promotion",
    },
    {
        "priority": 3,
        "target": "398-parent-action-contract-v2-after-identity-stack.md",
        "task": "write the next parent-action contract needed to derive the remaining closure-only and retained premises",
        "pass_condition": "future parent action must satisfy explicit operator/source/no-hair/domain/Ward conditions",
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
            "gate": "identity_coframe_slip_closed_by_label",
            "status": "closure_pass",
            "evidence": "eps_coframe_slip removed only inside identity branch",
        },
        {
            "gate": "domain_projector_nohair_parent_derived",
            "status": "fail",
            "evidence": "domain selector, projector gauge status, topology-cycle silence, and boundary Euler selection remain open",
        },
        {
            "gate": "preferred_frame_coefficient_map_updated",
            "status": "pass",
            "evidence": f"{len(PREFERRED_FRAME_COEFFICIENT_MAP_UNDER_IDENTITY)} residual maps updated under identity closure",
        },
        {
            "gate": "Ward_flux_owned",
            "status": "fail",
            "evidence": "domain/projector/boundary flux mapped, not Ward-owned",
        },
        {
            "gate": "xi_kept_separate",
            "status": "pass",
            "evidence": "domain anisotropy/topology cycles remain in xi row rather than folded into gamma",
        },
        {
            "gate": "preferred_frame_or_PPN_promoted",
            "status": "fail",
            "evidence": "alpha_i/xi/Gdot coefficients remain missing or contingent",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "preferred-frame/domain no-hair is conditional or retained only",
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
    write_csv(results_dir / "identity_branch_vector_split.csv", IDENTITY_BRANCH_VECTOR_SPLIT)
    write_csv(results_dir / "domain_projector_nohair_contract.csv", DOMAIN_PROJECTOR_NOHAIR_CONTRACT)
    write_csv(results_dir / "preferred_frame_coefficient_map_under_identity.csv", PREFERRED_FRAME_COEFFICIENT_MAP_UNDER_IDENTITY)
    write_csv(results_dir / "domain_to_observable_ledger.csv", DOMAIN_TO_OBSERVABLE_LEDGER)
    write_csv(results_dir / "nohair_or_budget_decision_tree.csv", NOHAIR_OR_BUDGET_DECISION_TREE)
    write_csv(results_dir / "runner_policy_rows.csv", RUNNER_POLICY_ROWS)
    write_csv(results_dir / "no_go_results.csv", NO_GO_RESULTS)
    write_csv(results_dir / "gate_policy.csv", GATE_POLICY)
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
        "coframe_slip_state": "closure_zero_not_derived_zero",
        "domain_projector_nohair_parent_derived": False,
        "preferred_frame_maps_updated": len(PREFERRED_FRAME_COEFFICIENT_MAP_UNDER_IDENTITY),
        "Ward_flux_owned": False,
        "preferred_frame_or_PPN_claim_allowed": False,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 395 preferred-frame/domain no-hair under identity closure artifacts."
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
