from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "class-metric-counterstress-nohair-contract"
STATUS = "class_metric_counterstress_nohair_contract_written_not_satisfied_pullback_branch_demoted_modified_gravity_no_local_GR_pass"
CLAIM_CEILING = "class_metric_counterstress_contract_only_no_WEP_PPN_fifth_force_EH_source_boundary_bulk_or_local_GR_pass"
NEXT_TARGET = "391-local-GR-stack-after-identity-coframe-closure.md"


SOURCE_DOCS = [
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "preferred-frame/vector no-hair and coefficient budgets",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "constant universal GM/source-normalization absorption gates",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "boundary class-only/no-angular and flux residuals",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk no-hair or source-normalized force-law contract",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner v2 retained residual state machine",
    },
    {
        "path": "384-parent-action-first-variation-obstruction-map.md",
        "role": "Pi_I^matter as first parent variation obstruction",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "Ward-owned selector counterstress route",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "local source-locked budgets and GR/null baseline",
    },
    {
        "path": "387-identity-coframe-or-class-metric-fork.md",
        "role": "class-metric branch demoted unless pullback is owned/silent",
    },
    {
        "path": "389-identity-coframe-parent-selection-principle.md",
        "role": "identity branch closure and class-metric fallback target",
    },
    {
        "path": "runs/20260602-014500-local-bound-runner-v2-smoke-matrix/results/suppression_budget_summary.csv",
        "role": "machine-readable local suppression budgets",
    },
]


COUNTERSTRESS_CONTRACT = [
    {
        "contract_item": "selector_equation_owns_pullback",
        "mathematical_form": "E_selector,I + Pi_I^matter = 0",
        "required_meaning": "the matter pullback appears as a source in a varied selector equation, not as a dropped term",
        "current_status": "contract_written_not_derived",
    },
    {
        "contract_item": "total_Ward_identity",
        "mathematical_form": "nabla_mu(T_matter + T_metric + T_selector + T_boundary + T_bulk)^mu_nu = 0",
        "required_meaning": "counterstress contributes to total conservation/Bianchi ledger",
        "current_status": "mapped_not_closed",
    },
    {
        "contract_item": "species_universal_geometry",
        "mathematical_form": "F_A(C_D)=F(C_D), no q_A(C_D), no theta_A(C_D)",
        "required_meaning": "counterstress is not composition dependent",
        "current_status": "conditional_after_388_not_parent_derived",
    },
    {
        "contract_item": "common_mode_nohair_or_constant",
        "mathematical_form": "partial_C F = 0 locally, pure gauge, or delta(GM)/(GM)=constant",
        "required_meaning": "common pullback does not become clock/gamma/fifth-force/Gdot residual",
        "current_status": "not_parent_derived",
    },
    {
        "contract_item": "source_budget_if_retained",
        "mathematical_form": "all surviving c_i eps_i are mapped to eta, clock, PPN, preferred-frame, Gdot, fifth-force rows",
        "required_meaning": "retained class-metric stress is scored as modified gravity, not local GR",
        "current_status": "required_fallback",
    },
]


NOHAIR_CONDITIONS = [
    {
        "condition": "positive_operator_or_constraint",
        "required_form": "L_C sigma = 0 with L_C positive, or an algebraic constraint that removes sigma",
        "kills": "regular exterior common-mode class hair",
        "current_status": "not_parent_derived",
    },
    {
        "condition": "source_free_compact_exterior",
        "required_form": "no matter, boundary, bulk, projector, or domain source for sigma outside compact body",
        "kills": "radial fifth-force and beta/gamma source hair",
        "current_status": "not_parent_derived",
    },
    {
        "condition": "regular_decaying_boundary_data",
        "required_form": "surface term vanishes or is a constant universal monopole",
        "kills": "boundary-resourced class metric hair",
        "current_status": "open_after_379",
    },
    {
        "condition": "Ward_owned_flux",
        "required_form": "n_mu T_counter^mu_nu is balanced by varied boundary/source charges",
        "kills": "alpha3, Gdot, fake conservation failure",
        "current_status": "mapped_not_proved",
    },
    {
        "condition": "constant_universal_GM_absorption",
        "required_form": "partial_r mu=partial_t mu=Delta_species mu=0 and no finite-range profile",
        "kills": "delta_G/Gdot/fifth-force source-normalization rows",
        "current_status": "not_parent_derived_after_378",
    },
    {
        "condition": "no_preferred_frame_counterstress",
        "required_form": "counterstress has no vector, domain-normal, marker, or trace-free anisotropic components",
        "kills": "alpha1, alpha2, xi, vector coframe slip",
        "current_status": "not_parent_derived_after_376",
    },
]


SOURCE_BUDGET_CONTRACT = [
    {
        "observable": "eta_WEP",
        "source_lock": "2.8e-15",
        "class_metric_failure": "species-dependent F_A, q_A, source normalization, or composition charge",
        "required_exit": "species-blind geometry theorem, identity coframe, or source-locked coefficient",
    },
    {
        "observable": "alpha_clock_redshift",
        "source_lock": "3.1e-5",
        "class_metric_failure": "common F(C_D) changes clock metric or constants",
        "required_exit": "identity coframe, local silence, constant normalization, or clock coefficient budget",
    },
    {
        "observable": "gamma_minus_1",
        "source_lock": "2.3e-5",
        "class_metric_failure": "counterstress scalar/boundary/bulk operator modifies curvature/light",
        "required_exit": "EH/no-hair theorem or coefficient budget",
    },
    {
        "observable": "beta_minus_1",
        "source_lock": "7.8e-5",
        "class_metric_failure": "radial nonlinear source hair or boundary flux",
        "required_exit": "radial no-hair/source-normalization or coefficient budget",
    },
    {
        "observable": "alpha1_alpha2_xi",
        "source_lock": "1.0e-4;2.0e-9;4.0e-9",
        "class_metric_failure": "vector/domain/projector/boundary anisotropic counterstress",
        "required_exit": "vector/domain no-hair or preferred-frame coefficient budget",
    },
    {
        "observable": "alpha3",
        "source_lock": "4.0e-20 contingent",
        "class_metric_failure": "unowned momentum flux or nonconservation channel",
        "required_exit": "Ward-owned flux or contingent budget",
    },
    {
        "observable": "Gdot_over_G",
        "source_lock": "9.6e-15 yr^-1 contingent",
        "class_metric_failure": "time-dependent common mode, source normalization, or boundary flux",
        "required_exit": "time-independence theorem or contingent budget",
    },
    {
        "observable": "delta_G_or_fifth_force_yukawa",
        "source_lock": "alpha(lambda)",
        "class_metric_failure": "finite-range radial common mode or bulk/boundary charge",
        "required_exit": "alpha(lambda) force law, no-hair theorem, or unscored retained row",
    },
]


COUNTERSTRESS_FATES = [
    {
        "fate": "derived_zero",
        "requirements": "identity coframe, F'=0, or positive source-free no-hair theorem",
        "allowed_claim": "row-specific theorem zero if source path is recorded",
        "current_status": "not_available",
    },
    {
        "fate": "pure_gauge",
        "requirements": "class-metric pullback direction is exact representative gauge, not physical C_D",
        "allowed_claim": "representative leakage removed",
        "current_status": "available_only_for_Cperp_like_directions",
    },
    {
        "fate": "constant_universal_monopole",
        "requirements": "constant source-normalized GM/unit calibration only",
        "allowed_claim": "measured-GM absorption after 378 gates",
        "current_status": "not_parent_derived",
    },
    {
        "fate": "Ward_owned_nohair_counterstress",
        "requirements": "selector stress varied, conserved, no-hair/boundary-only harmless",
        "allowed_claim": "modified-gravity branch may be locally budget-safe",
        "current_status": "contract_only",
    },
    {
        "fate": "source_budgeted_residual",
        "requirements": "coefficients/range/coupling mapped to local runner rows",
        "allowed_claim": "testable retained modified-gravity residual",
        "current_status": "required_if_no_theorem",
    },
    {
        "fate": "demoted_open",
        "requirements": "no theorem, no coefficient, no range, no closure label",
        "allowed_claim": "blocks local-GR branch",
        "current_status": "default_for_unowned_class_metric_pullback",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "Ward_ownership_is_not_nohair",
        "statement": "E_selector + Pi_matter = 0 makes conservation honest but does not make the counterstress locally invisible",
        "consequence": "PPN/WEP/fifth-force rows remain unless no-hair or budgets are supplied",
    },
    {
        "no_go": "common_F_is_not_local_GR",
        "statement": "F_A=F removes species split but leaves T partial_C F",
        "consequence": "clock/gamma/fifth-force/Gdot rows remain active",
    },
    {
        "no_go": "boundary_monopole_is_not_radial_hair",
        "statement": "constant conserved monopole can be GM-absorbed, radial or time-dependent hair cannot",
        "consequence": "source-normalization and boundary no-hair gates are mandatory",
    },
    {
        "no_go": "counterstress_cannot_be_hidden_in_Bianchi",
        "statement": "dropping selector stress while using its cancellation is fake conservation",
        "consequence": "total Ward ledger must retain every stress component",
    },
    {
        "no_go": "budget_safe_is_not_GR_derived",
        "statement": "a small fitted or bounded counterstress is modified-gravity evidence/control, not a GR reduction theorem",
        "consequence": "class metric branch stays demoted unless theorem-zero/no-hair closes it",
    },
]


BRANCH_GATE_MATRIX = [
    {
        "gate": "counterstress_equation_varied",
        "required": "derive E_selector,I + Pi_I^matter = 0 from parent action",
        "current_result": "not derived",
        "branch_status": "open",
    },
    {
        "gate": "counterstress_nohair",
        "required": "prove retained stress vanishes or is boundary-only constant in compact local exterior",
        "current_result": "not derived",
        "branch_status": "open",
    },
    {
        "gate": "source_budget_coefficients",
        "required": "derive coefficients/ranges/couplings for every surviving residual",
        "current_result": "missing",
        "branch_status": "budget_or_unscored",
    },
    {
        "gate": "GR_promotion",
        "required": "all class-metric counterstress rows theorem-zero or harmless constant monopole",
        "current_result": "failed",
        "branch_status": "demoted_modified_gravity",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The retained class-metric branch now has an exact counterstress contract: the pullback must be varied as E_selector,I + Pi_I^matter = 0, included in the total Ward ledger, and then shown to be no-hair, pure gauge, constant-universal GM normalization, or source-budgeted against local rows. None of those exits is parent-derived in the current branch. Therefore class metric remains a legitimate modified-gravity/counterstress test branch, but not a local-GR reduction.",
        "class_metric_branch_status": "demoted_to_modified_gravity_counterstress_or_source_budget",
        "identity_branch_status": "clean_local_closure_or_theorem_target_after_389",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "roll the local-GR stack forward assuming identity coframe as labelled closure, then isolate EH/operator/source/boundary/bulk debts",
        "pass_condition": "remaining GR-reduction blockers are listed without WEP/class-metric pullback ambiguity",
    },
    {
        "priority": 2,
        "target": "392-identity-coframe-parent-action-search-manifest.md",
        "task": "search wider corpus for an existing parent principle that could forbid local class spurions in matter geometry",
        "pass_condition": "candidate source paths are found or identity coframe remains closure",
    },
    {
        "priority": 3,
        "target": "393-class-metric-counterstress-source-budget-runner.md",
        "task": "if class metric is retained empirically, run a coefficient/range budget matrix for the counterstress branch",
        "pass_condition": "retained counterstress rows become theorem-zero, budgeted, or unscored with no local-GR claim",
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
            "gate": "counterstress_contract_written",
            "status": "pass",
            "evidence": f"{len(COUNTERSTRESS_CONTRACT)} required counterstress contract items written",
        },
        {
            "gate": "nohair_conditions_written",
            "status": "pass",
            "evidence": f"{len(NOHAIR_CONDITIONS)} no-hair/source-normalization conditions listed",
        },
        {
            "gate": "source_budget_contract_written",
            "status": "pass",
            "evidence": f"{len(SOURCE_BUDGET_CONTRACT)} observable rows mapped to source budgets",
        },
        {
            "gate": "counterstress_parent_derived",
            "status": "fail",
            "evidence": "E_selector + Pi_matter and no-hair/source-normalization exits are contract-only",
        },
        {
            "gate": "class_metric_local_GR_promotion",
            "status": "fail",
            "evidence": "class-metric branch remains modified-gravity/counterstress branch",
        },
        {
            "gate": "identity_branch_preserved",
            "status": "pass",
            "evidence": "identity coframe remains the clean local closure/theorem target from 389",
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
    write_csv(results_dir / "counterstress_contract.csv", COUNTERSTRESS_CONTRACT)
    write_csv(results_dir / "nohair_conditions.csv", NOHAIR_CONDITIONS)
    write_csv(results_dir / "source_budget_contract.csv", SOURCE_BUDGET_CONTRACT)
    write_csv(results_dir / "counterstress_fates.csv", COUNTERSTRESS_FATES)
    write_csv(results_dir / "no_go_results.csv", NO_GO_RESULTS)
    write_csv(results_dir / "branch_gate_matrix.csv", BRANCH_GATE_MATRIX)
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
        "counterstress_contract_items": len(COUNTERSTRESS_CONTRACT),
        "nohair_conditions": len(NOHAIR_CONDITIONS),
        "source_budget_rows": len(SOURCE_BUDGET_CONTRACT),
        "counterstress_parent_derived": False,
        "class_metric_local_GR_promotion_allowed": False,
        "identity_branch_preserved": True,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 390 class-metric counterstress no-hair contract artifacts."
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
