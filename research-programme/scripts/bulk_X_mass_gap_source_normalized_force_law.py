from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "bulk-X-mass-gap-source-normalized-force-law"
STATUS = "bulk_X_mass_gap_and_source_normalized_force_law_not_parent_derived_alphaX_lambdaX_missing_residual_retained"
CLAIM_CEILING = "bulk_X_force_law_contract_only_no_fifth_force_PPN_EH_WEP_or_local_GR_pass"
NEXT_TARGET = "381-local-GR-debt-ledger-rollup-after-360-380.md"


SOURCE_DOCS = [
    {
        "path": "222-parent-X-sector-degree-count-and-boundary-action.md",
        "role": "first-order X-sector route, regular kinetic X rejection, boundary momentum contract",
    },
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "bulk residual E_bulk mapping into gamma, beta, and fifth-force rows",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward force ledger where F_X feeds local residuals unless closed",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "mass-gap/no-source theorem target for F_X and retained PPN residual map",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "direct matter charge and WEP closure constraints for any X-mediated force",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "non-EH scalar/vector/bulk residual operators must be theorem-zero or retained",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "Yukawa force-law contract requiring m_X, q_X, source charge, alpha_X(lambda_X)",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "source-normalization and measured-GM absorption gates",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "boundary hair remains active unless class-only/Ward-owned restrictions are parent-derived",
    },
]


BULK_X_OPERATOR_ROUTES = [
    {
        "route": "source_free_massive_nohair",
        "equation": "(-Delta + m_X^2) X = 0, m_X^2 > 0",
        "would_give": "regular decaying exterior X is zero or exponentially suppressed",
        "required_parent_data": "positive elliptic operator, no exterior source, regular/decaying boundary conditions",
        "current_status": "conditional_theorem_target_not_parent_derived",
    },
    {
        "route": "source_normalized_Yukawa",
        "equation": "(-Delta + m_X^2) X = q_X rho_source",
        "would_give": "lambda_X = 1/m_X and X(r) = Q_X exp(-r/lambda_X)/(4 pi r)",
        "required_parent_data": "m_X, q_X, source charge Q_X, test coupling, G/M normalization",
        "current_status": "force_law_contract_only_alphaX_missing",
    },
    {
        "route": "first_order_constraint_X",
        "equation": "S_X = int sqrt(-g) [P^{mu nu} nabla_mu X_nu + J_eff^nu X_nu] + S_boundary",
        "would_give": "source identity without regular quadratic X waves",
        "required_parent_data": "closed constraint algebra and boundary primitive/no-hair",
        "current_status": "rank_zero_route_not_mass_gap_or_force_law",
    },
    {
        "route": "massless_X",
        "equation": "-Delta X = q_X rho_source",
        "would_give": "long-range 1/r extra force unless q_X is zero or pure universal GM normalization",
        "required_parent_data": "q_X=0 theorem, exact gauge redundancy, or safe GM absorption",
        "current_status": "local_branch_danger_if_allowed",
    },
    {
        "route": "tachyonic_or_wrong_sign_X",
        "equation": "(-Delta - |m_X|^2) X = q_X rho_source",
        "would_give": "local instability or growing exterior mode",
        "required_parent_data": "operator sign must be rejected by parent positivity",
        "current_status": "reject_for_local_GR_route",
    },
    {
        "route": "nonlocal_or_spectral_X_kernel",
        "equation": "X(r) = integral dmu rho_X(mu) Q_X(mu) exp(-mu r)/(4 pi r)",
        "would_give": "multi-range fifth-force/spectral residual",
        "required_parent_data": "kernel spectrum, weights, source normalization, regularity",
        "current_status": "unscored_modified_gravity_residual_until_kernel_derived",
    },
]


MASS_GAP_CONDITIONS = [
    {
        "condition": "positive_elliptic_operator",
        "required_form": "L_X = -Delta + m_X^2 with m_X^2 > 0 on the local exterior domain",
        "why_it_matters": "energy identity becomes positive definite",
        "current_status": "not_parent_derived",
    },
    {
        "condition": "source_free_exterior",
        "required_form": "J_X = 0 outside the compact source, including projector/domain/boundary contributions",
        "why_it_matters": "no-hair theorem cannot run with an exterior source",
        "current_status": "not_parent_derived",
    },
    {
        "condition": "regular_decaying_boundary_data",
        "required_form": "X finite at regular boundaries and X -> 0 or constant pure gauge at infinity",
        "why_it_matters": "surface terms in the no-hair integral vanish",
        "current_status": "boundary_conditions_open",
    },
    {
        "condition": "boundary_and_domain_do_not_resource_X",
        "required_form": "n dot grad X, boundary flux, class transition, and L_cg gradients vanish or are Ward-owned",
        "why_it_matters": "boundary source can mimic a bulk charge",
        "current_status": "open_after_379",
    },
    {
        "condition": "single_coframe_no_species_charge",
        "required_form": "matter couples universally and no body-dependent X charge survives",
        "why_it_matters": "otherwise eta_WEP and composition fifth-force rows activate",
        "current_status": "closure_required_after_373",
    },
    {
        "condition": "source_normalized_charge",
        "required_form": "Q_X and q_test are calibrated against measured GM and G_eff",
        "why_it_matters": "alpha_X cannot be defined without source normalization",
        "current_status": "open_after_378",
    },
]


NOHAIR_STEPS = [
    {
        "step": 1,
        "statement": "Assume a scalar or scalar-reduced bulk X equation on a local exterior annulus.",
        "equation": "L_X X = 0, L_X = -Delta + m_X^2",
        "status": "setup_only",
    },
    {
        "step": 2,
        "statement": "Multiply by X and integrate by parts.",
        "equation": "int_D X L_X X = int_D (|grad X|^2 + m_X^2 X^2) - int_boundary X n dot grad X",
        "status": "formal_identity",
    },
    {
        "step": 3,
        "statement": "If boundary terms vanish and m_X^2 is positive, the integral is non-negative.",
        "equation": "int_D (|grad X|^2 + m_X^2 X^2) = 0",
        "status": "conditional_nohair",
    },
    {
        "step": 4,
        "statement": "The only regular decaying source-free solution is zero.",
        "equation": "X = 0 and grad X = 0",
        "status": "conditional_result",
    },
    {
        "step": 5,
        "statement": "If a compact source remains, the exterior is Yukawa rather than theorem-zero.",
        "equation": "X(r) = Q_X exp(-m_X r)/(4 pi r) + higher multipoles",
        "status": "force_law_branch",
    },
    {
        "step": 6,
        "statement": "The acceleration ratio needs parent-normalized source and test charges.",
        "equation": "a_X/a_GR = alpha_X (1 + r/lambda_X) exp(-r/lambda_X)",
        "status": "alphaX_lambdaX_missing",
    },
]


SOURCE_NORMALIZED_FORCE_LAW = [
    {
        "quantity": "lambda_X",
        "definition": "lambda_X = 1/m_X",
        "needed_to_score": "finite range of the bulk-X mediated force",
        "current_status": "m_X_not_parent_derived",
    },
    {
        "quantity": "Q_X",
        "definition": "Q_X = integral d^3x q_X rho_source plus owned boundary/projector pieces",
        "needed_to_score": "source charge sourcing the exterior X profile",
        "current_status": "source_charge_not_parent_derived",
    },
    {
        "quantity": "q_test",
        "definition": "charge with which a test body responds to X",
        "needed_to_score": "force on matter and WEP/composition status",
        "current_status": "direct_matter_charge_forbidden_only_if_373_closes",
    },
    {
        "quantity": "alpha_X",
        "definition": "alpha_X proportional to Q_X q_test divided by measured G M_source m_test",
        "needed_to_score": "Yukawa strength compared with local fifth-force bounds",
        "current_status": "normalization_missing_do_not_score",
    },
    {
        "quantity": "bulk_residual_budget",
        "definition": "epsilon_bulk maps into gamma, beta, delta_G, and fifth-force rows if alpha_X cannot be computed",
        "needed_to_score": "fallback modified-gravity residual accounting",
        "current_status": "retained",
    },
]


OBSERVABLE_IMPACT_MAP = [
    {
        "observable": "delta_G_or_fifth_force_yukawa",
        "bulk_X_input": "alpha_X(lambda_X) or theorem-zero X",
        "current_policy": "parameterized_unscored_until_m_X_q_X_Q_X_are_derived",
    },
    {
        "observable": "gamma_minus_1",
        "bulk_X_input": "C_bulk epsilon_bulk plus any scalar-tensor/light-cone contribution",
        "current_policy": "budget_only_no_PPN_pass",
    },
    {
        "observable": "beta_minus_1",
        "bulk_X_input": "C_bulk2 epsilon_bulk plus nonlinear/radial source terms",
        "current_policy": "budget_only_no_PPN_pass",
    },
    {
        "observable": "eta_WEP",
        "bulk_X_input": "species-dependent q_test or body-dependent Q_X/M",
        "current_policy": "must vanish by universal coupling or remain source-locked",
    },
    {
        "observable": "Gdot_over_G",
        "bulk_X_input": "time-dependent m_X, q_X, Q_X, or source normalization",
        "current_policy": "contingent_active_if_time_drift_not_forbidden",
    },
    {
        "observable": "preferred_frame_alpha_i_or_xi",
        "bulk_X_input": "vector/tensor components or boundary/domain X source",
        "current_policy": "route through preferred-frame/boundary coefficient maps if present",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "bulk_X_nohair",
        "before_380": "mass-gap/no-source mechanism named but not written as force-law gate",
        "after_380": "conditional no-hair identity written; parent operator/source conditions fail open",
        "claim_status": "conditional_only",
    },
    {
        "runner_row": "delta_G_or_fifth_force_yukawa",
        "before_380": "bulk X required m_X and q_X",
        "after_380": "alpha_X(lambda_X) contract written but m_X/q_X/Q_X not derived",
        "claim_status": "parameterized_unscored",
    },
    {
        "runner_row": "gamma_minus_1_beta_minus_1",
        "before_380": "bulk residual epsilon_bulk retained",
        "after_380": "epsilon_bulk remains until X theorem-zero or scored force law exists",
        "claim_status": "budget_only",
    },
    {
        "runner_row": "eta_WEP",
        "before_380": "one-coframe/WEP closure required",
        "after_380": "direct X matter charge must be zero/universal or WEP row stays active",
        "claim_status": "source_locked_budget_only",
    },
    {
        "runner_row": "local_GR_reduction",
        "before_380": "bulk X was one of the open local force monsters",
        "after_380": "bulk X is caged but not killed; local GR still not derived",
        "claim_status": "no_promotion",
    },
]


FAILURE_MODES = [
    {
        "failure": "calling_rank_zero_a_mass_gap",
        "meaning": "using first-order/constraint rank information as if it proves (-Delta+m^2) positivity",
        "consequence": "false X no-hair pass",
    },
    {
        "failure": "forgetting_exterior_X_sources",
        "meaning": "running the no-hair integral while boundary/domain/projector terms still source X",
        "consequence": "bulk residual hidden as boundary hair",
    },
    {
        "failure": "using_alphaX_without_source_normalization",
        "meaning": "scoring a Yukawa force before Q_X, q_test, G_eff, and measured GM are fixed",
        "consequence": "fake fifth-force comparison",
    },
    {
        "failure": "massless_X_called_harmless",
        "meaning": "allowing a 1/r X field without gauge zero, universal GM absorption, or WEP closure",
        "consequence": "long-range fifth force or PPN residual",
    },
    {
        "failure": "tachyonic_or_wrong_sign_operator_retained",
        "meaning": "negative mass-squared or non-positive operator in the local exterior",
        "consequence": "instability or growing local mode",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "A valid bulk-X local pass needs either a positive source-free mass-gap theorem or a source-normalized Yukawa force law. The mathematical contract is now explicit, but the parent action has not derived the operator sign, mass gap, exterior source-free condition, X charge, test coupling, or alpha_X(lambda_X). Bulk X therefore remains retained as an active residual, not a local-GR pass.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "roll up local-GR debts after checkpoints 360-380 into ready, conditional, retained, and failed-open rows",
        "pass_condition": "project has a compact debt ledger showing what remains before derived local GR",
    },
    {
        "priority": 2,
        "target": "382-parent-local-action-minimal-contract.md",
        "task": "write the minimal parent action contract that would close coframe, Ward, EH, boundary, source, and bulk-X gates together",
        "pass_condition": "future derivations know the exact action-level obligations",
    },
    {
        "priority": 3,
        "target": "383-local-bound-runner-v2-from-retained-residuals.md",
        "task": "convert retained residual coefficients into a no-claim local bound runner plan",
        "pass_condition": "all non-derived rows can be stress-tested without claiming local GR",
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
            "gate": "mass_gap_nohair_identity_written",
            "status": "conditional_pass",
            "evidence": "energy identity shows source-free positive massive X has zero regular decaying exterior",
        },
        {
            "gate": "source_normalized_force_law_contract_written",
            "status": "pass",
            "evidence": "lambda_X, Q_X, q_test, alpha_X and a_X/a_GR relation recorded",
        },
        {
            "gate": "positive_X_operator_parent_derived",
            "status": "fail",
            "evidence": "parent action has not derived L_X = -Delta + m_X^2 with m_X^2 > 0",
        },
        {
            "gate": "source_free_exterior_parent_derived",
            "status": "fail",
            "evidence": "boundary, projector, domain, and matter charges can still re-source X",
        },
        {
            "gate": "alphaX_lambdaX_parent_derived",
            "status": "fail",
            "evidence": "m_X, q_X, Q_X, q_test, and measured-GM normalization are missing",
        },
        {
            "gate": "bulk_X_residual_retained",
            "status": "pass",
            "evidence": "epsilon_bulk and delta_G/fifth-force rows remain active rather than erased",
        },
        {
            "gate": "fifth_force_or_PPN_pass_claimed",
            "status": "fail",
            "evidence": "force-law/no-hair contract only; no local bound score or PPN pass claimed",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "bulk X, boundary, source normalization, universal coupling, and EH gates remain open",
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
    write_csv(results_dir / "bulk_X_operator_routes.csv", BULK_X_OPERATOR_ROUTES)
    write_csv(results_dir / "mass_gap_conditions.csv", MASS_GAP_CONDITIONS)
    write_csv(results_dir / "nohair_steps.csv", NOHAIR_STEPS)
    write_csv(results_dir / "source_normalized_force_law.csv", SOURCE_NORMALIZED_FORCE_LAW)
    write_csv(results_dir / "observable_impact_map.csv", OBSERVABLE_IMPACT_MAP)
    write_csv(results_dir / "runner_update.csv", RUNNER_UPDATE)
    write_csv(results_dir / "failure_modes.csv", FAILURE_MODES)
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
        "operator_routes_mapped": len(BULK_X_OPERATOR_ROUTES),
        "mass_gap_conditions": len(MASS_GAP_CONDITIONS),
        "alphaX_lambdaX_parent_derived": False,
        "bulk_X_nohair_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 380 bulk-X mass-gap and source-normalized force-law artifacts."
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
