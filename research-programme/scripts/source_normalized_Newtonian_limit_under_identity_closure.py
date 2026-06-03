from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-normalized-Newtonian-limit-under-identity-closure"
STATUS = "source_normalized_Newtonian_limit_under_identity_attempt_written_constant_GM_absorption_conditional_not_parent_derived_deltaG_Gdot_fifth_force_rows_retained_no_local_GR_pass"
CLAIM_CEILING = "source_normalized_Newtonian_limit_under_identity_only_no_Newton_PPN_EH_source_fifth_force_or_local_GR_pass"
NEXT_TARGET = "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md"


SOURCE_DOCS = [
    {
        "path": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "conditional M_eff monopole flux theorem and radial memory-hair warning",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "conditional EH weak-field branch that needs source normalization",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "source-normalization operator residues and modified-gravity ledger",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "fifth-force range/coupling contract and GM absorption tests",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "pre-identity source-normalization/GM absorption gate matrix",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X force law and source-normalized alpha_X(lambda_X) debt",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent source-normalization action block",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner states for delta_G/fifth-force/Gdot/source rows",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "GR/null baseline and source-lock budgets",
    },
    {
        "path": "391-local-GR-stack-after-identity-coframe-closure.md",
        "role": "identity closure stack with source-normalized Newtonian limit as active blocker",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "conditional EH selection and source normalization as next target",
    },
]


WEAK_FIELD_DERIVATION_STEPS = [
    {
        "step": 1,
        "assumption_or_equation": "identity matter coframe",
        "mathematical_form": "S_matter = sum_A S_A[Psi_A, e, omega[e], theta_A]",
        "result": "test matter moves on the same weak-field metric potential Phi",
        "status": "closure_zero_not_derived_zero",
    },
    {
        "step": 2,
        "assumption_or_equation": "conditional EH exterior",
        "mathematical_form": "G_{mu nu} + Lambda g_{mu nu} = kappa_eff T_{mu nu}^{eff}",
        "result": "EH-shaped field equation only if checkpoint 392 premises are assumed",
        "status": "conditional_not_parent_derived",
    },
    {
        "step": 3,
        "assumption_or_equation": "weak-field metric",
        "mathematical_form": "g_00 = -1 - 2 Phi/c^2 + O(c^-4)",
        "result": "G_00 = 2 nabla^2 Phi/c^2 + O(c^-4)",
        "status": "standard_local_limit_contract",
    },
    {
        "step": 4,
        "assumption_or_equation": "nonrelativistic source",
        "mathematical_form": "T_00^{eff} = rho_eff c^2 + O(c^0)",
        "result": "nabla^2 Phi = (kappa_eff c^4/2) rho_eff",
        "status": "conditional_on_source_map",
    },
    {
        "step": 5,
        "assumption_or_equation": "define local Newton coupling",
        "mathematical_form": "G_eff := kappa_eff c^4/(8 pi)",
        "result": "nabla^2 Phi = 4 pi G_eff rho_eff",
        "status": "definition_if_EH_branch_holds",
    },
    {
        "step": 6,
        "assumption_or_equation": "define source charge",
        "mathematical_form": "M_eff(r) := int_{B_r} rho_eff d^3x = (4 pi G_ref)^-1 int_{S^2_r} Pi_M J",
        "result": "M_eff is the source mass only if Pi_M J calibration and flux closure hold",
        "status": "conditional_from_244_not_parent_calibrated",
    },
    {
        "step": 7,
        "assumption_or_equation": "observed Kepler parameter",
        "mathematical_form": "mu_obs(r,t,A) := r^2 partial_r Phi_A = G_eff(r,t,A) M_eff(r,t) + mu_extra(r,t,A)",
        "result": "orbits measure mu_obs, not G_eff and M_eff separately",
        "status": "exposed_contract",
    },
    {
        "step": 8,
        "assumption_or_equation": "safe absorption condition",
        "mathematical_form": "mu_obs = constant universal GM_measured",
        "result": "only constant, universal, range-independent normalization can be absorbed into measured GM",
        "status": "conditional_pass_rule",
    },
]


SOURCE_NORMALIZATION_CONTRACT = [
    {
        "contract_item": "kappa_to_Geff",
        "required_form": "G_eff = kappa_eff c^4/(8 pi) in the local metric/EH branch",
        "why_needed": "fixes the conversion between curvature and Newtonian acceleration",
        "current_status": "conditional_EH_branch_only_not_parent_derived",
    },
    {
        "contract_item": "PiM_to_Meff_calibration",
        "required_form": "M_eff = (4 pi G_ref)^-1 int_{S^2} Pi_M J with parent-fixed G_ref and physical mass units",
        "why_needed": "prevents arbitrary source rescaling",
        "current_status": "flux_conditional_calibration_open",
    },
    {
        "contract_item": "radial_conservation",
        "required_form": "partial_r M_eff = 0 in compact ordinary exterior",
        "why_needed": "prevents radial memory hair from becoming fifth force or beta residual",
        "current_status": "conditional_from_244_not_global",
    },
    {
        "contract_item": "time_constancy",
        "required_form": "partial_t ln(G_eff M_eff) = 0 locally",
        "why_needed": "prevents Gdot/G and secular orbital drift",
        "current_status": "not_parent_derived",
    },
    {
        "contract_item": "species_universality",
        "required_form": "partial_A ln mu_obs = 0 for all matter, clocks, and compositions",
        "why_needed": "prevents source-normalization WEP leakage",
        "current_status": "identity_branch_closes_direct_matter_coupling_only",
    },
    {
        "contract_item": "range_independence",
        "required_form": "mu_extra(r,lambda) = 0 or alpha(lambda) is derived and scored",
        "why_needed": "prevents finite-range force from being hidden as GM",
        "current_status": "not_derived",
    },
    {
        "contract_item": "Ward_owned_flux",
        "required_form": "all boundary/projector/domain/bulk source flux is owned in the total Ward ledger",
        "why_needed": "prevents fake conserved mass from unowned energy/momentum exchange",
        "current_status": "mapped_not_closed",
    },
]


ABSORPTION_CONDITIONS_UNDER_IDENTITY = [
    {
        "condition": "constant_monopole_only",
        "mathematical_test": "partial_r mu_obs = partial_t mu_obs = partial_A mu_obs = 0",
        "if_satisfied": "absorb into measured GM",
        "if_failed": "retain delta_G, Gdot, WEP, fifth-force, or beta row",
        "status": "not_parent_derived",
    },
    {
        "condition": "no_radial_profile",
        "mathematical_test": "partial_r ln mu_obs = 0 outside compact support",
        "if_satisfied": "no radial source hair",
        "if_failed": "fifth-force/delta_G/beta active",
        "status": "conditional_Meff_only_extra_forces_open",
    },
    {
        "condition": "no_time_drift",
        "mathematical_test": "partial_t ln mu_obs = partial_t ln G_eff + partial_t ln M_eff = 0",
        "if_satisfied": "Gdot row inactive",
        "if_failed": "Gdot/G active at contingent source lock",
        "status": "not_parent_derived",
    },
    {
        "condition": "no_species_or_clock_dependence",
        "mathematical_test": "mu_A - mu_B = 0 for all test species A,B",
        "if_satisfied": "source normalization does not reopen WEP",
        "if_failed": "eta_WEP/composition force active",
        "status": "direct coupling closed by identity; source-side universality still must be derived",
    },
    {
        "condition": "no_finite_range_tail",
        "mathematical_test": "mu_extra/(GM) != alpha(1+r/lambda) exp(-r/lambda)",
        "if_satisfied": "no Yukawa scoring needed",
        "if_failed": "derive alpha(lambda) and score fifth-force row",
        "status": "not_derived",
    },
    {
        "condition": "same_baseline_GR_null",
        "mathematical_test": "GR/null row gives zero residual with the same runner",
        "if_satisfied": "pipeline sanity only",
        "if_failed": "pipeline invalid",
        "status": "pass_from_386_for_runner_sanity",
    },
]


RESIDUAL_AMPLITUDE_LAWS = [
    {
        "residual_channel": "delta_mu_over_mu",
        "amplitude_law": "delta_mu/mu = delta G_eff/G_eff + delta M_eff/M_eff + mu_extra/(G_eff M_eff)",
        "observable_rows": "delta_G_or_fifth_force_yukawa; Newtonian_limit",
        "zero_condition": "all three terms are constant universal calibration or theorem-zero",
        "current_status": "terms_not_parent_derived",
    },
    {
        "residual_channel": "radial_source_hair",
        "amplitude_law": "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r[mu_extra/(GM)]",
        "observable_rows": "fifth_force; beta_minus_1; delta_G",
        "zero_condition": "closed Pi_M flux plus no radial G_eff or extra force profile",
        "current_status": "M_eff conditional; G_eff/extra profile open",
    },
    {
        "residual_channel": "time_drift",
        "amplitude_law": "Gdot_obs/G_obs = partial_t ln(G_eff M_eff)",
        "observable_rows": "Gdot_over_G; secular_orbital_drift",
        "zero_condition": "G_eff and M_eff are time-independent or drift cancels by Ward theorem",
        "current_status": "not_parent_derived",
    },
    {
        "residual_channel": "finite_range_force",
        "amplitude_law": "a_extra/a_GR = alpha(lambda)(1+r/lambda) exp(-r/lambda)",
        "observable_rows": "delta_G_or_fifth_force_yukawa",
        "zero_condition": "alpha(lambda)=0 by theorem or source-normalized range/coupling is scored",
        "current_status": "range/coupling missing",
    },
    {
        "residual_channel": "source_normalization_PPN_beta",
        "amplitude_law": "beta_SN ~ d ln(G_eff M_eff)/d(U/c^2) plus nonlinear source-hair terms",
        "observable_rows": "beta_minus_1",
        "zero_condition": "source normalization has no potential/self-energy dependence",
        "current_status": "coefficient map not derived",
    },
    {
        "residual_channel": "species_source_charge",
        "amplitude_law": "eta_SN ~ Delta_A ln mu_obs",
        "observable_rows": "eta_WEP; composition_force",
        "zero_condition": "identity coframe plus source charge universality",
        "current_status": "direct coframe closure yes; source charge theorem open",
    },
]


RUNNER_ROW_TRANSITIONS = [
    {
        "runner_row": "Newtonian_limit",
        "state_after_393": "conditional_theorem_not_promoted",
        "reason": "weak-field algebra written but kappa/G_eff/M_eff/GM parent calibration remains open",
    },
    {
        "runner_row": "delta_G_or_fifth_force_yukawa",
        "state_after_393": "retained_unscored_parameterized",
        "reason": "radial/range/source-normalization residues need alpha(lambda) or constant-monopole theorem",
    },
    {
        "runner_row": "Gdot_over_G",
        "state_after_393": "retained_contingent_budget",
        "reason": "partial_t ln(G_eff M_eff)=0 not parent-derived",
    },
    {
        "runner_row": "beta_minus_1",
        "state_after_393": "retained_budget_only",
        "reason": "nonlinear source-normalization and radial hair coefficient map missing",
    },
    {
        "runner_row": "eta_WEP",
        "state_after_393": "direct_coframe_closure_only_source_charge_still_guarded",
        "reason": "identity closure closes matter geometry but not source-charge universality by itself",
    },
    {
        "runner_row": "gamma_minus_1",
        "state_after_393": "unchanged_retained",
        "reason": "source normalization alone does not close EH/operator/boundary/bulk slip residues",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "EH_shape_is_not_Newtonian_source_normalization",
        "statement": "Even if the exterior equation is EH-shaped, the measured Newtonian limit needs kappa, G_eff, M_eff, and GM fixed.",
        "consequence": "no Newtonian/local-GR pass from EH shape alone",
    },
    {
        "no_go": "Meff_conservation_is_not_GM_absorption",
        "statement": "Radially conserved M_eff is necessary, but not sufficient, because G_eff, calibration, time drift, and range dependence can still vary.",
        "consequence": "delta_G/Gdot/fifth-force rows remain",
    },
    {
        "no_go": "identity_coframe_is_not_source_charge_universality",
        "statement": "Putting matter on one coframe does not prove every source-normalization charge is universal.",
        "consequence": "WEP is closed only on the direct matter geometry side",
    },
    {
        "no_go": "constant_monopole_only_is_the_safe_absorption_case",
        "statement": "Only a constant universal source rescaling can disappear into measured GM.",
        "consequence": "radial, temporal, species, environmental, or finite-range pieces must be retained",
    },
    {
        "no_go": "source_normalization_cannot_hide_boundary_or_bulk_flux",
        "statement": "Unowned boundary/bulk/projector flux cannot be called mass conservation.",
        "consequence": "boundary/bulk no-hair remains the next target",
    },
]


GATE_POLICY = [
    {
        "gate": "conditional_Newtonian_algebra_written",
        "current_result": "pass",
        "meaning": "if EH and source conditions hold, nabla^2 Phi = 4 pi G_eff rho_eff with G_eff=kappa_eff c^4/(8 pi)",
        "claim_policy": "conditional theorem only",
    },
    {
        "gate": "M_eff_flux_conservation_available",
        "current_result": "conditional_pass",
        "meaning": "checkpoint 244 provides closed Pi_M flux if its parent source identity premises hold",
        "claim_policy": "may be imported as conditional, not global source proof",
    },
    {
        "gate": "measured_GM_absorption_parent_derived",
        "current_result": "fail",
        "meaning": "constant universal G_eff M_eff = GM_measured is not derived",
        "claim_policy": "no Newtonian/source pass",
    },
    {
        "gate": "deltaG_Gdot_fifth_force_rows_retained",
        "current_result": "pass",
        "meaning": "failed source-normalization exits remain explicit",
        "claim_policy": "runner discipline intact",
    },
    {
        "gate": "boundary_bulk_flux_owned",
        "current_result": "fail",
        "meaning": "source normalization still depends on boundary/bulk/projector Ward ownership",
        "claim_policy": "next derivation target",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The weak-field source-normalization algebra is now explicit: under identity closure and a conditional EH exterior, G_eff = kappa_eff c^4/(8 pi), nabla^2 Phi = 4 pi G_eff rho_eff, and the measured Kepler parameter is mu_obs = G_eff M_eff plus any extra force/source residue. A constant universal mu_obs can be absorbed into measured GM, but MTS has not parent-derived kappa calibration, G_eff constancy, M_eff calibration, source-charge universality, no finite-range residue, or Ward-owned boundary/bulk flux. Therefore Newtonian reduction remains conditional only, and delta_G, Gdot/G, beta, WEP-source, and fifth-force rows stay retained.",
        "conditional_Newtonian_algebra_written": True,
        "measured_GM_absorption_parent_derived": False,
        "deltaG_Gdot_fifth_force_rows_retained": True,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive or budget boundary and bulk Ward-owned flux/no-hair under identity closure",
        "pass_condition": "boundary/bulk flux is theorem-zero, pure gauge, constant monopole, source-budgeted, or explicitly retained",
    },
    {
        "priority": 2,
        "target": "395-preferred-frame-domain-nohair-under-identity-closure.md",
        "task": "derive or budget vector/domain/projector residues after source-normalization gates",
        "pass_condition": "alpha1/alpha2/alpha3/xi are theorem-zero or coefficient-mapped",
    },
    {
        "priority": 3,
        "target": "396-local-GR-reduction-sufficiency-stack-audit.md",
        "task": "roll up identity, EH, source, boundary, bulk, and preferred-frame gates into one sufficiency stack",
        "pass_condition": "every local-GR promotion premise is derived, conditional, retained, or failed-open",
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
            "gate": "conditional_Newtonian_algebra_written",
            "status": "pass",
            "evidence": "weak-field chain kappa_eff -> G_eff -> Poisson -> mu_obs recorded",
        },
        {
            "gate": "M_eff_flux_conservation_imported",
            "status": "conditional_pass",
            "evidence": "checkpoint 244 gives M_eff conservation under closed Pi_M flux premises",
        },
        {
            "gate": "kappa_to_Geff_parent_calibrated",
            "status": "fail",
            "evidence": "G_eff = kappa_eff c^4/(8 pi) written only inside conditional EH branch",
        },
        {
            "gate": "measured_GM_absorption_parent_derived",
            "status": "fail",
            "evidence": "constant universal G_eff M_eff = GM_measured not derived",
        },
        {
            "gate": "range_time_species_independence_derived",
            "status": "fail",
            "evidence": "radial/time/species/range dependence exits remain open",
        },
        {
            "gate": "deltaG_Gdot_fifth_force_rows_retained",
            "status": "pass",
            "evidence": "runner rows remain retained or unscored when absorption gates fail",
        },
        {
            "gate": "Newtonian_or_local_GR_promoted",
            "status": "fail",
            "evidence": "source-normalized Newtonian limit is conditional only",
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
    write_csv(results_dir / "weak_field_derivation_steps.csv", WEAK_FIELD_DERIVATION_STEPS)
    write_csv(results_dir / "source_normalization_contract.csv", SOURCE_NORMALIZATION_CONTRACT)
    write_csv(results_dir / "absorption_conditions_under_identity.csv", ABSORPTION_CONDITIONS_UNDER_IDENTITY)
    write_csv(results_dir / "residual_amplitude_laws.csv", RESIDUAL_AMPLITUDE_LAWS)
    write_csv(results_dir / "runner_row_transitions.csv", RUNNER_ROW_TRANSITIONS)
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
        "conditional_Newtonian_algebra_written": True,
        "M_eff_flux_conservation_imported": True,
        "kappa_to_Geff_parent_calibrated": False,
        "measured_GM_absorption_parent_derived": False,
        "range_time_species_independence_derived": False,
        "deltaG_Gdot_fifth_force_rows_retained": True,
        "derived_Newtonian_or_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 393 source-normalized Newtonian limit under identity closure artifacts."
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
