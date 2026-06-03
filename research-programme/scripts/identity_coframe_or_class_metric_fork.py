from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "identity-coframe-or-class-metric-fork"
STATUS = "identity_coframe_local_GR_branch_prioritized_class_metric_pullback_demoted_to_closure_or_counterstress_no_local_GR_pass"
CLAIM_CEILING = "branch_fork_contract_only_no_WEP_PPN_fifth_force_EH_source_boundary_bulk_or_local_GR_pass"
NEXT_TARGET = "388-WEP-species-symmetry-common-F-parent-selector-attempt.md"


SOURCE_DOCS = [
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "conditional universal matter action and fixed-coframe direct vertex theorem",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "representative invariance descends matter to class observables but not species universality",
    },
    {
        "path": "371-WEP-species-universality-or-active-eta-runner.md",
        "role": "eta_WEP active unless species universality/common F is derived",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe/common-F selector audit and WEP closure axioms",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "constant universal normalization and measured-GM absorption limits",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent local action contract and fallback rows",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner v2 residual state machine",
    },
    {
        "path": "384-parent-action-first-variation-obstruction-map.md",
        "role": "first unowned variation term Pi_I^matter",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "legal cancellation fates for coframe pullback",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "GR/null baseline smoke and suppression budgets for retained pullbacks",
    },
    {
        "path": "runs/20260602-014500-local-bound-runner-v2-smoke-matrix/results/suppression_budget_summary.csv",
        "role": "machine-readable local suppression budgets",
    },
]


BRANCHES = [
    {
        "branch_id": "A_identity_metric_coframe",
        "local_matter_coupling": "S_matter[psi_A, e, omega[e], constants_A]",
        "coframe_rule": "ehat_A^a_mu = e^a_mu for every matter species A",
        "Pi_I_matter": "zero if Z_I are nonmetric MTS selector/class/bulk/boundary variables and e is varied independently",
        "local_GR_route": "viable candidate branch",
        "cost": "MTS local effects must enter metric equation, source normalization, nonlocal/cosmological sector, or higher operators; not a matter-visible class metric",
        "current_status": "mathematically clean but parent selection not derived",
    },
    {
        "branch_id": "B_universal_class_metric",
        "local_matter_coupling": "S_matter[psi_A, exp(F(C_D)) e, omega[ehat], constants_A]",
        "coframe_rule": "one common F(C_D) for all species",
        "Pi_I_matter": "common-mode pullback active unless F is constant/gauge/source-normalized or counterstress-owned",
        "local_GR_route": "conditional closure/counterstress branch",
        "cost": "clock, gamma, fifth-force, and Gdot rows remain active unless local silence/source normalization is derived",
        "current_status": "not a local-GR derivation",
    },
    {
        "branch_id": "C_species_class_metric",
        "local_matter_coupling": "sum_A S_A[psi_A, exp(F_A(C_D)) e, omega[ehat_A], constants_A(C_D)]",
        "coframe_rule": "species-dependent class response allowed",
        "Pi_I_matter": "species pullback active",
        "local_GR_route": "fails local-GR route unless parent species symmetry forces F_A=F",
        "cost": "eta_WEP and composition fifth-force rows become hardest active debts",
        "current_status": "demote unless common-F theorem is derived",
    },
    {
        "branch_id": "D_Ward_owned_class_pullback",
        "local_matter_coupling": "class-metric pullback retained with selector equation E_selector,I + Pi_I^matter = 0",
        "coframe_rule": "ehat may depend on class/projector/boundary/bulk data, but selector stress is explicit",
        "Pi_I_matter": "owned rather than erased",
        "local_GR_route": "modified-gravity/counterstress branch",
        "cost": "counterstress must satisfy no-hair/source-budget/local-bound rows",
        "current_status": "honest fallback, not derived local GR",
    },
]


FORK_THEOREMS = [
    {
        "theorem": "identity_coframe_pullback_zero",
        "premises": "all matter species couple to e; e is the metric/tetrad varied in the metric equation; nonmetric Z_I do not enter matter action or matter constants",
        "result": "dS_matter/dZ_I = 0 and Pi_I^matter = 0 for nonmetric selector variables",
        "proof_status": "mathematically_sufficient_given_premises",
        "missing_parent_step": "derive why parent action forbids ehat(C_D), F_A(C_D), constants_A(C_D), and q_A labels",
    },
    {
        "theorem": "universal_class_metric_common_mode_no_local_GR_without_silence",
        "premises": "matter sees ehat = exp(F(C_D)) e with one common F",
        "result": "eta species split may be avoided, but common Pi_C^matter proportional to T partial_C F remains",
        "proof_status": "obstruction",
        "missing_parent_step": "derive F'=0 locally, pure gauge, source-normalized constant mode, or Ward-owned no-hair counterstress",
    },
    {
        "theorem": "species_class_metric_WEP_no_go",
        "premises": "representative invariance only; C_D is physical class observable; F_A(C_D) may differ by species",
        "result": "representative invariance cannot force F_A=F_B; eta_WEP remains active",
        "proof_status": "no_go",
        "missing_parent_step": "derive internal species symmetry/common-F selector",
    },
    {
        "theorem": "counterstress_not_GR_by_itself",
        "premises": "selector equation owns Pi_I^matter in Ward identity",
        "result": "conservation is honest but residual stress may still alter PPN/WEP/fifth-force rows",
        "proof_status": "fallback_only",
        "missing_parent_step": "derive no-hair, boundary-only harmlessness, or source-locked coefficients",
    },
]


LOCAL_GR_REQUIREMENTS = [
    {
        "requirement": "universal_metric_matter",
        "identity_branch_status": "satisfied_if_parent_selects_identity_coframe",
        "class_metric_status": "conditional_common_metric_only; species branch fails",
        "runner_impact": "eta_WEP direct row can become theorem-zero only on identity/common-F branch",
    },
    {
        "requirement": "no_selector_pullback_force",
        "identity_branch_status": "satisfied_for_nonmetric_Z_I by partial e/partial Z_I = 0",
        "class_metric_status": "fails unless F'=0/gauge/source-normalized/counterstress-owned",
        "runner_impact": "clock/gamma/fifth-force/Gdot stay active on common class metric",
    },
    {
        "requirement": "matter_Ward_identity",
        "identity_branch_status": "ordinary matter Ward identity on e",
        "class_metric_status": "needs selector stress in total Ward ledger",
        "runner_impact": "unowned counterstress maps to preferred-frame/boundary/source rows",
    },
    {
        "requirement": "Newton_GR_limit",
        "identity_branch_status": "can target EH/operator/source-normalization stack after WEP pullback is removed",
        "class_metric_status": "cannot claim local GR until pullback residuals are no-hair or source-budgeted",
        "runner_impact": "gamma/beta/EH operator rows remain open in both branches",
    },
    {
        "requirement": "empirical_local_budget",
        "identity_branch_status": "still must pass PPN/EH/source rows, but avoids matter-coframe pullback budgets",
        "class_metric_status": "must meet 386 suppression budgets or demote to closure",
        "runner_impact": "eta_WEP ceiling 2.8e-15 remains decisive for species class branch",
    },
]


RUNNER_IMPACT = [
    {
        "observable": "eta_WEP",
        "identity_branch": "direct pullback theorem-zero if identity coframe parent-selected",
        "universal_class_branch": "species split avoided only if common F parent-derived",
        "species_class_branch": "active hardest ready row",
        "counterstress_branch": "must show no composition-dependent source charge",
        "decision": "target species symmetry/common-F next",
    },
    {
        "observable": "alpha_clock_redshift",
        "identity_branch": "ordinary metric clock if constants independent",
        "universal_class_branch": "common F(C_D) can be clock visible",
        "species_class_branch": "clock plus composition risk",
        "counterstress_branch": "budget or no-hair required",
        "decision": "derive constant independence/local silence",
    },
    {
        "observable": "gamma_minus_1/beta_minus_1",
        "identity_branch": "moves pressure to EH/operator/source stack",
        "universal_class_branch": "scalar/common-mode and selector stress remain",
        "species_class_branch": "fails before clean PPN due WEP split",
        "counterstress_branch": "source-budget stress coefficients required",
        "decision": "no PPN promotion yet",
    },
    {
        "observable": "alpha1/alpha2/xi",
        "identity_branch": "projector/domain variables must be absent from matter coframe",
        "universal_class_branch": "domain/projector selector leakage remains possible",
        "species_class_branch": "same plus WEP split",
        "counterstress_branch": "preferred-frame no-hair/covariance proof required",
        "decision": "remain budget rows",
    },
    {
        "observable": "Gdot/fifth_force",
        "identity_branch": "only source-normalization/bulk/boundary force-law channels remain",
        "universal_class_branch": "common F(C_D) can generate time drift or radial force unless normalized",
        "species_class_branch": "composition fifth-force risk",
        "counterstress_branch": "range/coupling/source-charge contract required",
        "decision": "fifth-force stays unscored parameterized",
    },
]


BRANCH_DEMOTION_RULES = [
    {
        "condition": "identity coframe is assumed without a parent selector",
        "allowed_label": "local WEP closure branch",
        "forbidden_label": "derived local GR",
    },
    {
        "condition": "common class metric has F'(C_D) not derived zero",
        "allowed_label": "common-mode residual/counterstress branch",
        "forbidden_label": "local GR reduction",
    },
    {
        "condition": "species class functions F_A(C_D) are allowed",
        "allowed_label": "active WEP residual branch",
        "forbidden_label": "WEP-safe branch",
    },
    {
        "condition": "selector counterstress is invoked",
        "allowed_label": "modified-gravity counterstress branch",
        "forbidden_label": "GR unless no-hair/source-budget is derived",
    },
]


PARENT_SELECTOR_CONTRACT = [
    {
        "contract_item": "identity_or_common_metric_selector",
        "required_statement": "the parent local action selects exactly one matter coframe and does not allow species-labelled observed geometries",
        "minimum_form": "ehat_A^a_mu = e^a_mu or ehat_A^a_mu = ehat^a_mu for all A with common F",
        "strong_local_GR_preference": "identity ehat=e",
    },
    {
        "contract_item": "forbid_class_dependence_of_constants",
        "required_statement": "m_A, alpha_EM,A, clock constants, and charges do not depend on C_D except through universal metric units",
        "minimum_form": "partial_C m_A = partial_C alpha_A = q_A = 0, or universal absorbed constant",
        "strong_local_GR_preference": "no direct C_D dependence",
    },
    {
        "contract_item": "selector_pullback_ownership",
        "required_statement": "if ehat depends on Z_I, then Pi_I^matter is zero, pure gauge, constant-normalized, or Ward-owned",
        "minimum_form": "partial ehat/partial Z_I = 0 or E_selector,I + Pi_I^matter = 0",
        "strong_local_GR_preference": "partial e/partial Z_I = 0 for nonmetric Z_I",
    },
    {
        "contract_item": "runner_state_transition",
        "required_statement": "any row promoted from budget to zero must cite a parent theorem source",
        "minimum_form": "budget_only -> derived_zero only with theorem path",
        "strong_local_GR_preference": "eta_WEP theorem-zero first",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The local theory should now be forked explicitly. The identity/metric coframe branch is the only clean local-GR candidate because Pi_I^matter vanishes for nonmetric selector variables if matter sees e directly. But this is not yet parent-derived, so it is a theorem target, not a pass. The class-metric pullback branch remains useful only as a labelled closure/counterstress/modified-gravity branch unless common-mode silence, source normalization, species symmetry, or no-hair is derived.",
        "primary_local_GR_candidate": "A_identity_metric_coframe",
        "demoted_branch": "B/C/D class-metric pullback branches remain closure/counterstress until parent-owned",
        "hardest_next_row": "eta_WEP",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt a parent species symmetry/common-F selector, or prove identity coframe is the only local matter coupling",
        "pass_condition": "F_A(C_D)=F(C_D) is parent-derived or eta_WEP remains explicit closure/budget debt",
    },
    {
        "priority": 2,
        "target": "389-identity-coframe-parent-selection-principle.md",
        "task": "try to derive identity coframe from local equivalence principle, diffeomorphism invariance, and absence of species charges",
        "pass_condition": "identity ehat=e becomes parent theorem or stays closure",
    },
    {
        "priority": 3,
        "target": "390-class-metric-counterstress-nohair-contract.md",
        "task": "if class metric is retained, write exact counterstress/no-hair/source-budget contract",
        "pass_condition": "retained pullback stress is no-hair, source-budgeted, or demoted",
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
            "gate": "fork_branches_written",
            "status": "pass",
            "evidence": f"{len(BRANCHES)} local coupling branches classified",
        },
        {
            "gate": "identity_branch_mathematically_sufficient",
            "status": "conditional_pass",
            "evidence": "Pi_I^matter vanishes if matter sees e and nonmetric Z_I do not enter matter constants",
        },
        {
            "gate": "identity_branch_parent_derived",
            "status": "fail",
            "evidence": "no parent selector yet forbids class-metric/coframe functions",
        },
        {
            "gate": "class_metric_demoted",
            "status": "pass",
            "evidence": "class-metric pullback is closure/counterstress unless silence/source-normalization/species symmetry/no-hair is derived",
        },
        {
            "gate": "eta_WEP_resolved",
            "status": "fail",
            "evidence": "species common-F selector remains next target",
        },
        {
            "gate": "WEP_PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "branch fork only; no row moves to derived_zero",
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
    write_csv(results_dir / "branch_fork_table.csv", BRANCHES)
    write_csv(results_dir / "fork_theorems.csv", FORK_THEOREMS)
    write_csv(results_dir / "local_GR_requirements.csv", LOCAL_GR_REQUIREMENTS)
    write_csv(results_dir / "runner_impact.csv", RUNNER_IMPACT)
    write_csv(results_dir / "branch_demotion_rules.csv", BRANCH_DEMOTION_RULES)
    write_csv(results_dir / "parent_selector_contract.csv", PARENT_SELECTOR_CONTRACT)
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
        "branches": len(BRANCHES),
        "fork_theorems": len(FORK_THEOREMS),
        "identity_branch_mathematically_sufficient": True,
        "identity_branch_parent_derived": False,
        "class_metric_pullback_demoted": True,
        "eta_WEP_resolved": False,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 387 identity-coframe or class-metric fork artifacts."
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
