from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "observed-coframe-selector-pullback-cancellation-theorem"
STATUS = "observed_coframe_pullback_cancellation_routes_classified_identity_or_gauge_or_constant_or_counterstress_required_not_parent_derived"
CLAIM_CEILING = "coframe_pullback_cancellation_theorem_attempt_only_no_WEP_PPN_EH_source_boundary_bulk_or_local_GR_pass"
NEXT_TARGET = "386-local-bound-runner-v2-smoke-matrix.md"


SOURCE_DOCS = [
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "fixed-observed-coframe direct WEP/clock vertex theorem",
    },
    {
        "path": "361-residual-gauge-principle-for-projected-matter-metric.md",
        "role": "residual gauge/projected matter metric route",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "representative-invariant matter action and class metric route",
    },
    {
        "path": "372-local-phiC-zero-theorem-or-gradient-bound.md",
        "role": "common-mode phi_C zero/gradient fallback",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe/common F closure and WEP residual",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "constant universal normalization versus delta_G/Gdot/source residuals",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent action contract and matter/coframe identity",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner v2 states and eta_WEP pressure",
    },
    {
        "path": "384-parent-action-first-variation-obstruction-map.md",
        "role": "observed-coframe selector pullback obstruction",
    },
]


CANCELLATION_CONDITIONS = [
    {
        "condition": "identity_coframe",
        "mathematical_statement": "partial ehat^a_mu / partial Z_I = 0 for all nonmetric MTS selector variables Z_I",
        "what_it_kills": "Pi_I^matter exactly",
        "what_it_costs": "matter sees the fundamental metric/coframe directly; MTS local effects must live in metric/source/operator sectors",
        "current_status": "clean_route_but_not_parent_selected",
    },
    {
        "condition": "pure_gauge_pullback",
        "mathematical_statement": "delta ehat[Z_I] = L_xi ehat + local Lorentz rotation, with matter action invariant",
        "what_it_kills": "representative/gauge-direction pullback",
        "what_it_costs": "must prove Z_I direction is gauge/exact, not physical class response",
        "current_status": "conditional_for_Cperp_representatives_not_for_C_D_or_species_F_A",
    },
    {
        "condition": "constant_universal_normalization",
        "mathematical_statement": "partial ehat/partial Z_I gives only constant universal scale delta mu/mu with partial_r=partial_t=Delta_species=0",
        "what_it_kills": "local force/clock/WEP effect after unit or measured-GM absorption",
        "what_it_costs": "requires source-normalization and no range/time/species dependence",
        "current_status": "not_parent_derived_after_378",
    },
    {
        "condition": "species_symmetry_common_F",
        "mathematical_statement": "ehat_A=ehat and F_A(C_D)=F(C_D) for every species A",
        "what_it_kills": "species-difference part of Pi_I^matter and eta_WEP direct class split",
        "what_it_costs": "common-mode F(C_D) still needs local silence or source-normalization",
        "current_status": "future_theorem_target_not_supplied",
    },
    {
        "condition": "Ward_owned_selector_counterstress",
        "mathematical_statement": "E_selector,I + Pi_I^matter = 0 with selector stress included in total Ward identity",
        "what_it_kills": "fake conservation problem; owns the pullback rather than erasing it",
        "what_it_costs": "counterstress must be no-hair, boundary-only, or source-budgeted",
        "current_status": "honest_modified_gravity_route_open",
    },
    {
        "condition": "explicit_closure_retention",
        "mathematical_statement": "set Pi_I^matter=0 by labelled closure or retain coefficients c_pullback,I",
        "what_it_kills": "nothing as a derivation; only prevents hidden overclaim",
        "what_it_costs": "no WEP/local-GR promotion",
        "current_status": "allowed_only_as_labelled_closure",
    },
]


THEOREM_ATTEMPTS = [
    {
        "attempt": "identity_coframe_theorem",
        "premise": "observed coframe is the fundamental local coframe, not a function of class/projector/bulk variables",
        "result": "Pi_I^matter=0 for nonmetric MTS variables",
        "verdict": "mathematically_sufficient",
        "failure": "not derived from MTS parent selector and may push MTS effects into metric/operator/source sectors",
    },
    {
        "attempt": "species_symmetry_theorem",
        "premise": "internal matter-sector symmetry forbids species labels in F_A(C_D), constants_A(C_D), and q_A",
        "result": "Delta F_AB=Delta m_A=Delta alpha_A=q_A-q_B=0",
        "verdict": "would_kill_eta_species_split",
        "failure": "no parent internal symmetry has been supplied; common-mode still open",
    },
    {
        "attempt": "quotient_gauge_theorem",
        "premise": "Cperp and representative data are exact gauge directions of the lifted-C/class sector",
        "result": "pullback along representative directions is pure gauge",
        "verdict": "conditional_support",
        "failure": "does not kill physical class observable C_D or species-common F(C_D)",
    },
    {
        "attempt": "constant_common_mode_theorem",
        "premise": "F(C_D) is locally constant, universal, time-independent, and source-normalized",
        "result": "common-mode pullback becomes unit/GM normalization rather than force/WEP effect",
        "verdict": "conditional_support",
        "failure": "requires 372 phiC zero and 378 source-normalization gates, both open",
    },
    {
        "attempt": "selector_counterstress_theorem",
        "premise": "selector action variation provides a Ward-owned counterstress exactly balancing Pi_I^matter",
        "result": "conservation is honest and pullback is not hidden",
        "verdict": "modified_gravity_fallback",
        "failure": "counterstress coefficients/no-hair not derived; runner rows remain active",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "fixed_ehat_vertex_zero_is_not_total_zero",
        "statement": "delta S_matter/delta Z_I|ehat=0 does not imply dS_matter/dZ_I=0 when ehat depends on Z_I",
        "consequence": "direct WEP vertex theorem is necessary but insufficient",
    },
    {
        "no_go": "representative_invariance_does_not_force_species_universality",
        "statement": "F_A(C_D) can be representative-invariant for every A while F_A != F_B",
        "consequence": "eta_WEP remains active unless a species symmetry/common-F selector is added",
    },
    {
        "no_go": "universal_common_mode_is_not_automatically_safe",
        "statement": "a common F(C_D) avoids composition dependence but can still produce clock/gamma/fifth-force/Gdot effects",
        "consequence": "common-mode silence/source-normalization must be derived",
    },
    {
        "no_go": "exterior_vacuum_T_zero_does_not_set_source_charge_zero",
        "statement": "T=0 outside matter removes local exterior pullback density but not source matching, body charge, or boundary conditions",
        "consequence": "WEP/fifth-force rows still require source-charge control",
    },
    {
        "no_go": "counterstress_is_not_local_GR_by_itself",
        "statement": "Ward-owned selector counterstress keeps conservation honest but can still be a modified-gravity residual",
        "consequence": "counterstress must be no-hair or source-budgeted",
    },
]


PULLBACK_CLASSIFICATION = [
    {
        "pullback_piece": "representative_Cperp",
        "classification": "conditional_gauge_zero",
        "needed_theorem": "Cperp exact/representative gauge theorem",
        "fallback_row": "clock/gamma if representative leaks",
    },
    {
        "pullback_piece": "physical_class_C_D_common",
        "classification": "conditional_common_mode",
        "needed_theorem": "local phiC zero or constant universal GM/unit absorption",
        "fallback_row": "clock; gamma; fifth_force; Gdot",
    },
    {
        "pullback_piece": "physical_class_C_D_species",
        "classification": "active_WEP_residual",
        "needed_theorem": "species symmetry/common F(C_D)",
        "fallback_row": "eta_WEP; composition_fifth_force",
    },
    {
        "pullback_piece": "projector_or_domain_selector",
        "classification": "active_preferred_frame_or_anisotropy_residual",
        "needed_theorem": "covariant topological projector/domain selector and owned stress",
        "fallback_row": "alpha1; alpha2; xi; gamma",
    },
    {
        "pullback_piece": "boundary_selector",
        "classification": "active_boundary_residual",
        "needed_theorem": "class-only boundary action and Ward-owned flux",
        "fallback_row": "gamma; beta; alpha_i; xi; WEP_boundary",
    },
    {
        "pullback_piece": "bulk_X_selector_or_charge",
        "classification": "active_bulk_or_fifth_force_residual",
        "needed_theorem": "X no-hair/gauge or source-normalized alpha_X(lambda_X)",
        "fallback_row": "fifth_force; gamma; beta; eta_WEP_if_charged",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "eta_WEP",
        "after_385": "remains hardest active ready row unless identity coframe or species symmetry is parent-derived",
        "state": "budget_only",
    },
    {
        "runner_row": "alpha_clock_redshift",
        "after_385": "common-mode pullback needs local silence or constant normalization",
        "state": "budget_only",
    },
    {
        "runner_row": "gamma_minus_1_beta_minus_1",
        "after_385": "selector/boundary/bulk pullbacks remain coefficient rows",
        "state": "budget_only",
    },
    {
        "runner_row": "preferred_frame_xi",
        "after_385": "projector/domain/boundary anisotropic pullbacks remain budget rows",
        "state": "budget_only_or_contingent",
    },
    {
        "runner_row": "delta_G_or_fifth_force",
        "after_385": "common-mode, boundary, and bulk-X pullbacks remain range/coupling dependent",
        "state": "unscored_parameterized",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The observed-coframe selector pullback can be cancelled only by identity coframe, pure gauge pullback, constant universal normalization, species symmetry/common F plus common-mode silence, or Ward-owned selector counterstress. None is parent-derived in the current branch. Therefore Pi_I^matter remains the first active obstruction and eta_WEP remains the hardest ready local row.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "run a small local-bound runner v2 smoke matrix using retained pullback residual rows and GR/null baselines",
        "pass_condition": "budget rows populate with no pass claims and eta_WEP pressure remains explicit",
    },
    {
        "priority": 2,
        "target": "387-identity-coframe-or-class-metric-fork.md",
        "task": "decide whether the local branch should pivot to strict identity coframe locally or keep class-metric pullback as closure/counterstress",
        "pass_condition": "identity-coframe and class-metric routes are separated with costs",
    },
    {
        "priority": 3,
        "target": "388-species-symmetry-common-F-theorem-attempt.md",
        "task": "try to derive an internal species symmetry forcing F_A(C_D)=F(C_D)",
        "pass_condition": "species split is theorem-zero or eta_WEP remains active",
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
            "gate": "cancellation_conditions_classified",
            "status": "pass",
            "evidence": f"{len(CANCELLATION_CONDITIONS)} legal fates for Pi_I^matter classified",
        },
        {
            "gate": "theorem_attempts_written",
            "status": "pass",
            "evidence": f"{len(THEOREM_ATTEMPTS)} cancellation routes tested at theorem-contract level",
        },
        {
            "gate": "no_go_results_written",
            "status": "pass",
            "evidence": f"{len(NO_GO_RESULTS)} no-go shortcuts recorded",
        },
        {
            "gate": "pullback_classification_written",
            "status": "pass",
            "evidence": f"{len(PULLBACK_CLASSIFICATION)} pullback pieces classified",
        },
        {
            "gate": "Pi_I_matter_cancelled_or_owned",
            "status": "fail",
            "evidence": "no identity coframe, species symmetry, constant-normalization theorem, or counterstress derivation supplied",
        },
        {
            "gate": "WEP_or_local_GR_promoted",
            "status": "fail",
            "evidence": "eta_WEP remains active and local-GR stack remains open",
        },
        {
            "gate": "runner_update_preserves_residuals",
            "status": "pass",
            "evidence": "pullback-driven residuals retained as budget or unscored rows",
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
    write_csv(results_dir / "cancellation_conditions.csv", CANCELLATION_CONDITIONS)
    write_csv(results_dir / "theorem_attempts.csv", THEOREM_ATTEMPTS)
    write_csv(results_dir / "no_go_results.csv", NO_GO_RESULTS)
    write_csv(results_dir / "pullback_classification.csv", PULLBACK_CLASSIFICATION)
    write_csv(results_dir / "runner_update.csv", RUNNER_UPDATE)
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
        "cancellation_conditions": len(CANCELLATION_CONDITIONS),
        "theorem_attempts": len(THEOREM_ATTEMPTS),
        "no_go_results": len(NO_GO_RESULTS),
        "Pi_I_matter_cancelled_or_owned": False,
        "eta_WEP_active": True,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 385 observed-coframe selector pullback cancellation artifacts."
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
