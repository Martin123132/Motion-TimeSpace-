from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-bulk-nohair-joint-runner-under-identity-closure"
STATUS = "boundary_bulk_nohair_joint_runner_under_identity_written_conditional_kill_switches_not_parent_derived_boundary_bulk_residuals_retained_no_local_GR_pass"
CLAIM_CEILING = "boundary_bulk_nohair_joint_runner_under_identity_only_no_boundary_bulk_PPN_fifth_force_source_or_local_GR_pass"
NEXT_TARGET = "395-preferred-frame-domain-nohair-under-identity-closure.md"


SOURCE_DOCS = [
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "boundary residual split and symbolic PPN vector",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward force ledger with boundary and bulk force channels",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-owned no-hair policy and retained PPN residual vector",
    },
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "preferred-frame/vector coefficient rows fed by boundary/domain leakage",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "range/coupling contract for finite-range boundary or bulk forces",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "constant universal GM absorption gates",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "class-only boundary no-angular kill switch and retained boundary coefficients",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X mass-gap no-hair and alpha_X(lambda_X) force-law contract",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent action blocks for boundary, bulk-X, Ward closure, and residual fallbacks",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "GR/null baseline and local source-lock budgets",
    },
    {
        "path": "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "role": "source-normalized Newtonian algebra and boundary/bulk flux as next target",
    },
]


JOINT_WARD_FLUX_CONTRACT = [
    {
        "contract_item": "joint_local_force_vector",
        "mathematical_form": "q_BX^nu := P_loc[n_mu B^{mu nu} + F_X^nu + F_boundary^nu]",
        "required_result": "q_BX^nu = 0, pure gauge, constant monopole, Ward-owned exchange, or retained source-budget",
        "current_status": "mapped_not_closed",
        "failure_rows": "alpha3; Gdot/G; beta; fifth_force; source_normalization",
    },
    {
        "contract_item": "boundary_class_only_kill_switch",
        "mathematical_form": "S_boundary = S_boundary(Q_rel, M_eff, V_scalar, I_top)",
        "required_result": "delta S_boundary/delta B_TF = delta S_boundary/delta B_0i = 0",
        "current_status": "conditional_not_parent_derived",
        "failure_rows": "gamma; xi; alpha1; alpha2",
    },
    {
        "contract_item": "boundary_radial_monopole_split",
        "mathematical_form": "B_tr = B_tr^mono + B_tr^rad(r,t)",
        "required_result": "B_tr^mono constant universal only; B_tr^rad = 0 or scored",
        "current_status": "not_parent_derived",
        "failure_rows": "delta_G; beta; fifth_force; Gdot/G",
    },
    {
        "contract_item": "bulk_X_mass_gap_kill_switch",
        "mathematical_form": "(-Delta + m_X^2)X = 0, m_X^2 > 0 with decaying regular data",
        "required_result": "X = 0 and grad X = 0 in the local exterior",
        "current_status": "conditional_not_parent_derived",
        "failure_rows": "fifth_force; gamma; beta; delta_G",
    },
    {
        "contract_item": "bulk_X_force_law_exit",
        "mathematical_form": "(-Delta + m_X^2)X = q_X rho_source",
        "required_result": "derive alpha_X(lambda_X), source charge, test charge, and measured-GM normalization",
        "current_status": "alphaX_lambdaX_missing",
        "failure_rows": "fifth_force_unscored; WEP_if_species_charge",
    },
    {
        "contract_item": "source_absorption_permission",
        "mathematical_form": "mu_extra_BX = constant universal monopole only",
        "required_result": "absorb into measured GM only if checkpoint 393 gates pass",
        "current_status": "conditional_safe_case_not_parent_derived",
        "failure_rows": "delta_G; Gdot/G; fifth_force; beta",
    },
]


BOUNDARY_BULK_CHANNEL_LEDGER = [
    {
        "channel": "B_TF_tracefree_shear",
        "sector": "boundary",
        "schematic_residue": "epsilon_B_TF B_TF,ij",
        "zero_or_safe_condition": "class-only boundary action forbids angular/l>=2 representatives",
        "current_status": "not_parent_derived",
        "observable_rows": "gamma_minus_1; xi; lensing_slip",
    },
    {
        "channel": "B_0i_vector_boundary",
        "sector": "boundary",
        "schematic_residue": "epsilon_B0i B_0i",
        "zero_or_safe_condition": "no boundary marker, preferred normal, vector frame, or patch label",
        "current_status": "not_parent_derived",
        "observable_rows": "alpha1; alpha2; alpha3_if_flux",
    },
    {
        "channel": "B_rad_radial_trace",
        "sector": "boundary",
        "schematic_residue": "epsilon_B_rad B_tr^rad(r,t)",
        "zero_or_safe_condition": "radial trace hair absent; only constant universal monopole survives",
        "current_status": "not_parent_derived",
        "observable_rows": "beta_minus_1; delta_G_or_fifth_force; perihelion; Gdot/G_if_time_dependent",
    },
    {
        "channel": "B_flux_unowned",
        "sector": "boundary",
        "schematic_residue": "epsilon_B_flux n_mu B^{mu nu}",
        "zero_or_safe_condition": "owned total Ward/Bianchi boundary current",
        "current_status": "mapped_not_proved",
        "observable_rows": "alpha3; Gdot/G; beta; secular_drift",
    },
    {
        "channel": "B_mono_constant",
        "sector": "boundary",
        "schematic_residue": "epsilon_B_mono constant monopole",
        "zero_or_safe_condition": "constant universal calibrated GM rescaling",
        "current_status": "conditionally_absorbable_only_if_393_gates_pass",
        "observable_rows": "measured_GM_only_if_safe; otherwise_delta_G",
    },
    {
        "channel": "X_source_free_massive",
        "sector": "bulk_X",
        "schematic_residue": "(-Delta + m_X^2)X = 0",
        "zero_or_safe_condition": "m_X^2>0, no source, regular decaying boundary data",
        "current_status": "conditional_not_parent_derived",
        "observable_rows": "none_if_theorem_zero; otherwise_bulk_rows",
    },
    {
        "channel": "X_sourced_Yukawa",
        "sector": "bulk_X",
        "schematic_residue": "X(r)=Q_X exp(-r/lambda_X)/(4 pi r)",
        "zero_or_safe_condition": "alpha_X(lambda_X) derived and scored, or q_X/Q_X theorem-zero",
        "current_status": "alphaX_lambdaX_missing",
        "observable_rows": "delta_G_or_fifth_force; eta_WEP_if_species_charge",
    },
    {
        "channel": "X_boundary_resourced",
        "sector": "bulk_X_boundary_mix",
        "schematic_residue": "n.grad X or boundary/class transition source",
        "zero_or_safe_condition": "boundary does not resource X or flux is Ward-owned",
        "current_status": "open_after_379_380",
        "observable_rows": "fifth_force; beta; Gdot/G; alpha3",
    },
    {
        "channel": "X_nonlocal_spectral",
        "sector": "bulk_X_nonlocal",
        "schematic_residue": "integral dmu rho_X(mu) exp(-mu r)/r",
        "zero_or_safe_condition": "kernel silence/screening spectrum derived",
        "current_status": "unscored_modified_gravity_residual",
        "observable_rows": "scale_dependent_delta_G; fifth_force; Gdot/G",
    },
]


JOINT_NOHAIR_MECHANISMS = [
    {
        "mechanism": "class_only_boundary",
        "would_kill": "B_TF and B_0i angular/vector sources",
        "does_not_kill": "radial scalar hair, time-dependent monopole, unowned flux, bulk X",
        "proof_status": "conditional_not_parent_derived",
        "runner_policy": "retain eps_B_TF, eps_B0i, eps_B_rad, eps_B_flux",
    },
    {
        "mechanism": "positive_source_free_bulk_mass_gap",
        "would_kill": "regular decaying source-free X",
        "does_not_kill": "sourced Yukawa X, boundary-resourced X, nonlocal kernels, source-charge WEP leakage",
        "proof_status": "conditional_not_parent_derived",
        "runner_policy": "retain epsilon_bulk_X or alpha_X(lambda_X) debt",
    },
    {
        "mechanism": "constant_universal_monopole_absorption",
        "would_kill": "only a constant calibrated GM rescaling",
        "does_not_kill": "radial/time/species/range dependence",
        "proof_status": "conditional_safe_case_not_parent_derived",
        "runner_policy": "retain delta_G/Gdot/fifth-force exits unless all 393 gates pass",
    },
    {
        "mechanism": "Ward_owned_flux",
        "would_kill": "fake Bianchi/source drift from boundary/bulk exchange",
        "does_not_kill": "unowned boundary current or unbalanced X flux",
        "proof_status": "mapped_not_closed",
        "runner_policy": "retain alpha3/Gdot/beta/secular flux rows",
    },
    {
        "mechanism": "source_budget_exit",
        "would_kill": "nothing; it makes residuals honest",
        "does_not_kill": "the residual itself",
        "proof_status": "available_policy",
        "runner_policy": "budget gamma/beta/alpha_i/xi/Gdot and quarantine fifth-force until alpha(lambda)",
    },
]


JOINT_RESIDUAL_AMPLITUDE_LAWS = [
    {
        "observable_row": "gamma_minus_1",
        "amplitude_law": "gamma-1 ~ c_TF eps_B_TF + c_rad eps_B_rad + c_X eps_bulk_X + c_slip eps_nonEH",
        "safe_condition": "all coefficients theorem-zero or below source lock with same-pipeline baseline",
        "current_status": "retained_budget_only",
    },
    {
        "observable_row": "beta_minus_1",
        "amplitude_law": "beta-1 ~ c_rad eps_B_rad + c_flux eps_B_flux + c_X2 eps_bulk_X^2 + c_SN beta_SN",
        "safe_condition": "radial hair and unowned flux zero/owned; nonlinear source map derived",
        "current_status": "retained_budget_only",
    },
    {
        "observable_row": "alpha1_alpha2",
        "amplitude_law": "alpha_i ~ c_vec eps_B0i + c_marker eps_marker + c_domain eps_domain",
        "safe_condition": "no boundary marker/vector/domain preferred-frame data",
        "current_status": "retained_budget_only",
    },
    {
        "observable_row": "alpha3",
        "amplitude_law": "alpha3 ~ c_flux eps_B_flux + c_Xflux eps_X_flux",
        "safe_condition": "total boundary/bulk flux is Ward-owned or absent",
        "current_status": "contingent_budget_only",
    },
    {
        "observable_row": "xi",
        "amplitude_law": "xi ~ c_xi eps_B_TF_l>=2 + c_domain eps_external_domain",
        "safe_condition": "trace-free boundary shear and domain anisotropy theorem-zero",
        "current_status": "retained_budget_only",
    },
    {
        "observable_row": "delta_G_or_fifth_force_yukawa",
        "amplitude_law": "a_extra/a_GR = alpha_X(lambda_X)(1+r/lambda_X)e^{-r/lambda_X} + alpha_B(lambda_B)(1+r/lambda_B)e^{-r/lambda_B} + partial_r eps_B_rad",
        "safe_condition": "finite-range pieces theorem-zero or alpha(lambda) derived and scored",
        "current_status": "parameterized_unscored",
    },
    {
        "observable_row": "Gdot_over_G",
        "amplitude_law": "Gdot_obs/G_obs ~ partial_t ln[GM + mu_extra_BX]",
        "safe_condition": "no time-dependent monopole, boundary flux, X charge, or source normalization",
        "current_status": "contingent_budget_only",
    },
    {
        "observable_row": "eta_WEP_source_charge",
        "amplitude_law": "eta_SN ~ Delta_A ln[mu_obs_A] + Delta_A q_X/q_m",
        "safe_condition": "identity coframe plus source-charge universality and no species X charge",
        "current_status": "direct_coframe_closed_source_charge_open",
    },
]


RUNNER_POLICY_ROWS = [
    {
        "runner_row": "boundary_nohair",
        "state_after_394": "conditional_only",
        "policy": "do not zero boundary coefficients unless class-only/no-marker/Ward-owned/radial-monopole premises are derived",
    },
    {
        "runner_row": "bulk_X_nohair",
        "state_after_394": "conditional_only",
        "policy": "do not zero X unless positive source-free mass-gap conditions and boundary data are derived",
    },
    {
        "runner_row": "constant_monopole_absorption",
        "state_after_394": "conditional_only",
        "policy": "absorb only constant universal calibrated GM rescaling; retain radial/time/species/range exits",
    },
    {
        "runner_row": "fifth_force",
        "state_after_394": "retained_unscored_parameterized",
        "policy": "derive alpha_X(lambda_X) or alpha_B(lambda_B) before scalar scoring",
    },
    {
        "runner_row": "preferred_frame_and_xi",
        "state_after_394": "retained_budget_only",
        "policy": "boundary vector/shear/domain residues feed alpha1/alpha2/alpha3/xi until no-hair theorem",
    },
    {
        "runner_row": "source_normalization",
        "state_after_394": "retained",
        "policy": "boundary/bulk flux cannot be hidden inside M_eff or measured GM",
    },
    {
        "runner_row": "local_GR_reduction",
        "state_after_394": "fail_promotion",
        "policy": "no local GR claim until boundary/bulk/preferred-frame/source/EH stack closes",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "class_only_boundary_is_not_full_boundary_nohair",
        "statement": "Class-only boundary dependence kills angular/vector sources only if parent-derived; it does not automatically kill radial hair or flux.",
        "consequence": "eps_B_rad and eps_B_flux remain active.",
    },
    {
        "no_go": "bulk_mass_gap_is_not_available_without_source_free_conditions",
        "statement": "The X no-hair integral requires positive operator, no exterior source, and harmless boundary terms.",
        "consequence": "bulk-X residual is retained unless every premise is derived.",
    },
    {
        "no_go": "GM_absorption_cannot_hide_flux",
        "statement": "Unowned boundary/bulk flux is not a measured mass calibration.",
        "consequence": "alpha3, Gdot/G, beta, and source-normalization rows stay active.",
    },
    {
        "no_go": "fifth_force_needs_range_and_coupling",
        "statement": "A radial boundary or bulk-X profile cannot be scored as one scalar without alpha(lambda).",
        "consequence": "fifth-force row remains parameterized/unscored.",
    },
    {
        "no_go": "identity_closure_is_not_source_charge_universality",
        "statement": "ehat=e closes direct matter geometry but does not prove universal boundary/bulk source charge.",
        "consequence": "WEP-source and composition-force guards remain.",
    },
]


GATE_POLICY = [
    {
        "gate": "joint_boundary_bulk_contract_written",
        "current_result": "pass",
        "meaning": "boundary and bulk force channels are joined into q_BX^nu rather than treated as separate loopholes",
        "claim_policy": "internal runner discipline",
    },
    {
        "gate": "boundary_class_only_parent_derived",
        "current_result": "fail",
        "meaning": "B_TF, B_0i, B_rad, and B_flux coefficients are not theorem-zero",
        "claim_policy": "no boundary no-hair pass",
    },
    {
        "gate": "bulk_X_mass_gap_parent_derived",
        "current_result": "fail",
        "meaning": "positive source-free X operator and boundary data are not parent-derived",
        "claim_policy": "no bulk no-hair pass",
    },
    {
        "gate": "joint_Ward_flux_owned",
        "current_result": "fail",
        "meaning": "n_mu B^{mu nu}+F_X^nu is mapped but not owned/zero-derived",
        "claim_policy": "no source-normalization or Bianchi shortcut",
    },
    {
        "gate": "residuals_retained",
        "current_result": "pass",
        "meaning": "boundary/bulk coefficients feed explicit runner rows",
        "claim_policy": "testable modified-gravity residual branch retained",
    },
    {
        "gate": "local_GR_promoted",
        "current_result": "fail",
        "meaning": "boundary, bulk, source, preferred-frame, and EH premises remain incomplete",
        "claim_policy": "no local-GR claim",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Boundary and bulk residues are now joined into a single no-hair/flux runner. The class-only boundary action and the positive source-free bulk-X mass-gap identity are both useful conditional kill switches, but neither is parent-derived. A constant universal monopole may be absorbed only if the source-normalization gates from checkpoint 393 pass. Radial boundary hair, unowned flux, sourced X, boundary-resourced X, nonlocal kernels, and species-dependent source charges remain explicit residuals feeding gamma, beta, alpha_i, xi, delta_G/fifth-force, Gdot/G, and WEP-source rows. No boundary no-hair, bulk no-hair, PPN, fifth-force, source-normalization, or local-GR pass is claimed.",
        "boundary_nohair_parent_derived": False,
        "bulk_X_nohair_parent_derived": False,
        "joint_Ward_flux_owned": False,
        "boundary_bulk_residuals_retained": True,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive or budget preferred-frame/domain/projector residues after identity and boundary-bulk gates",
        "pass_condition": "alpha1/alpha2/alpha3/xi are theorem-zero, pure gauge, source-budgeted, or coefficient-mapped",
    },
    {
        "priority": 2,
        "target": "396-local-GR-reduction-sufficiency-stack-audit.md",
        "task": "roll up identity, EH, source, boundary, bulk, and preferred-frame gates into one GR-reduction scorecard",
        "pass_condition": "every local-GR premise is classified as derived, conditional, retained, failed, or closure-only",
    },
    {
        "priority": 3,
        "target": "397-local-bound-runner-v3-from-identity-stack.md",
        "task": "update the local runner with identity-branch closure labels and retained boundary/bulk/source residuals",
        "pass_condition": "same-pipeline GR/null baseline plus retained residual rows are emitted without promotion",
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
            "gate": "joint_boundary_bulk_contract_written",
            "status": "pass",
            "evidence": "q_BX^nu contract and residual ledger written",
        },
        {
            "gate": "boundary_nohair_parent_derived",
            "status": "fail",
            "evidence": "class-only/no-marker/radial/flux premises remain conditional or open",
        },
        {
            "gate": "bulk_X_nohair_parent_derived",
            "status": "fail",
            "evidence": "positive source-free mass-gap and harmless boundary data not derived",
        },
        {
            "gate": "joint_Ward_flux_owned",
            "status": "fail",
            "evidence": "boundary/bulk flux mapped, not Ward-owned or zero-derived",
        },
        {
            "gate": "fifth_force_scored",
            "status": "fail",
            "evidence": "alpha_X(lambda_X) or alpha_B(lambda_B) missing",
        },
        {
            "gate": "residual_runner_rows_retained",
            "status": "pass",
            "evidence": f"{len(JOINT_RESIDUAL_AMPLITUDE_LAWS)} observable amplitude rows retained",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "boundary/bulk no-hair is conditional only",
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
    write_csv(results_dir / "joint_Ward_flux_contract.csv", JOINT_WARD_FLUX_CONTRACT)
    write_csv(results_dir / "boundary_bulk_channel_ledger.csv", BOUNDARY_BULK_CHANNEL_LEDGER)
    write_csv(results_dir / "joint_nohair_mechanisms.csv", JOINT_NOHAIR_MECHANISMS)
    write_csv(results_dir / "joint_residual_amplitude_laws.csv", JOINT_RESIDUAL_AMPLITUDE_LAWS)
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
        "joint_boundary_bulk_contract_written": True,
        "boundary_nohair_parent_derived": False,
        "bulk_X_nohair_parent_derived": False,
        "joint_Ward_flux_owned": False,
        "fifth_force_scored": False,
        "boundary_bulk_residuals_retained": True,
        "derived_boundary_bulk_or_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 394 boundary/bulk no-hair joint runner under identity closure artifacts."
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
