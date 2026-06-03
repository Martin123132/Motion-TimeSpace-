from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Ward-owned-local-nohair-or-retained-PPN-residual-map"
STATUS = "Ward_force_channels_mapped_to_nohair_conditions_or_retained_PPN_residuals_no_local_GR_promotion"
CLAIM_CEILING = "force_channel_map_and_symbolic_bound_contract_only_no_local_GR_no_PPN_pass_no_nohair_theorem"
NEXT_TARGET = "358-local-EH-exterior-operator-from-Ward-closed-action.md"


SOURCE_DOCS = [
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "boundary residual decomposition and symbolic PPN owner map",
    },
    {
        "path": "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
        "role": "A1-A7 no-hair attempt and residual amplitude scaffold",
    },
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "source-locked local target scales and open-sector quarantine",
    },
    {
        "path": "355-GR-reduction-and-derivation-priority-ledger.md",
        "role": "GR-first derivation-first priority ledger",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "Ward force ledger F_X/F_P/F_boundary/F_domain/nonmetric matter",
    },
    {
        "path": "runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/force_ledger.csv",
        "role": "machine-readable force channels from checkpoint 356",
    },
    {
        "path": "runs/20260601-234500-official-local-bound-source-lock-or-nohair-proof-deepening/results/source_locked_bound_manifest.csv",
        "role": "machine-readable source-locked local target scales from checkpoint 354",
    },
]


FORCE_FATE_MAP = [
    {
        "force": "F_X^nu",
        "theorem_zero_route": "positive elliptic/massive local operator with no exterior source plus regularity/asymptotic zero implies X residual vanishes by maximum-principle/no-source theorem",
        "boundary_only_route": "X reduces to conserved monopole charge absorbed into measured GM",
        "retained_residual_if_open": "epsilon_bulk, epsilon_rad",
        "PPN_targets": "gamma_minus_1; beta_minus_1; delta_G_or_fifth_force",
        "current_verdict": "open_retained_until_local_X_operator_and_source_terms_are_derived",
        "next_derivation_needed": "derive local X equation, sign of effective mass/operator, source-free exterior condition, and boundary regularity",
    },
    {
        "force": "F_P^nu",
        "theorem_zero_route": "metric-independent diffeomorphism-covariant topological P_D with owned relative-chain constraint gives F_P_bulk=0",
        "boundary_only_route": "projector charge is boundary-supported and class-only, with no angular/vector representative data",
        "retained_residual_if_open": "epsilon_TF, epsilon_vec, epsilon_P_bulk",
        "PPN_targets": "gamma_minus_1; preferred_frame_alpha1_alpha2; xi_preferred_location_anisotropy",
        "current_verdict": "conditional_bulk_zero_only_boundary_and_parent_selection_open",
        "next_derivation_needed": "derive P_D from parent variables and prove boundary projector charge is monopole/class-only or retain residual",
    },
    {
        "force": "F_boundary^nu",
        "theorem_zero_route": "boundary action depends only on conserved total relative class, forbidding radial, trace-free, vector, clock, and WEP hair",
        "boundary_only_route": "pure conserved trace monopole mass renormalization",
        "retained_residual_if_open": "epsilon_rad, epsilon_TF, epsilon_vec, epsilon_clock_boundary, epsilon_WEP_boundary",
        "PPN_targets": "gamma_minus_1; beta_minus_1; preferred_frame_alpha1_alpha2; alpha_clock_redshift; eta_WEP",
        "current_verdict": "monopole_safe_condition_known_but_nohair_not_derived",
        "next_derivation_needed": "prove class-only boundary action and regular asymptotic matching or retain each boundary multipole residual",
    },
    {
        "force": "F_domain^nu",
        "theorem_zero_route": "domain selector, normal, and L_cg are covariant functionals of local fields with no independent preferred frame/location",
        "boundary_only_route": "domain variation contributes only to global matching data, not compact local bulk",
        "retained_residual_if_open": "epsilon_domain_vec, epsilon_domain_aniso, epsilon_Lcg_grad",
        "PPN_targets": "preferred_frame_alpha1_alpha2; xi_preferred_location_anisotropy; delta_G_or_fifth_force",
        "current_verdict": "open_quarantined_preferred_frame_and_anisotropy_sectors",
        "next_derivation_needed": "derive domain variables as covariant/dynamical or carry preferred-frame/location residuals",
    },
    {
        "force": "F_matter_nonmetric^nu",
        "theorem_zero_route": "universal single metric/coframe coupling for matter, photons, clocks, rods, and lab standards; no species-dependent MTS charge",
        "boundary_only_route": "none; nonmetric matter coupling is local and cannot hide as a safe boundary monopole",
        "retained_residual_if_open": "epsilon_clock, epsilon_WEP, epsilon_nonmetric_light",
        "PPN_targets": "alpha_clock_redshift; eta_WEP; gamma_minus_1",
        "current_verdict": "hard_open_until_universal_coupling_theorem",
        "next_derivation_needed": "derive single physical metric/coframe and universal matter action from parent structure",
    },
]


NOHAIR_MECHANISM_CANDIDATES = [
    {
        "mechanism": "maximum_principle_mass_gap",
        "applies_to": "F_X^nu / nonprojector bulk residual",
        "needed_equation": "(-Delta + m_eff^2) phi = 0 in local exterior, m_eff^2 > 0, regular boundary/asymptotic data",
        "would_prove": "phi=0 or exponentially screened residual; epsilon_bulk and epsilon_rad vanish or are bounded",
        "current_status": "candidate_not_derived",
        "failure_mode": "massless/tachyonic/source-driven local scalar hair remains",
    },
    {
        "mechanism": "topological_relative_chain_exactness",
        "applies_to": "F_P^nu / projector force",
        "needed_equation": "P_D is metric-independent, diffeo-covariant, and enforced by relative-chain constraint C[P_D]=0",
        "would_prove": "F_P_bulk=0 and no hidden projector stress in compact exterior",
        "current_status": "conditional_from_348_but_parent_selection_open",
        "failure_mode": "metric-dependent or fixed external projector produces retained stress",
    },
    {
        "mechanism": "class_only_boundary_action",
        "applies_to": "F_boundary^nu",
        "needed_equation": "S_boundary = S_boundary(Q_total, area/volume monopole) with no angular representative dependence",
        "would_prove": "only conserved monopole trace survives; B_TF, B_0i, B_tr_rad vanish",
        "current_status": "not_derived",
        "failure_mode": "angular/radial/vector boundary hair remains and feeds PPN residuals",
    },
    {
        "mechanism": "covariant_domain_selector",
        "applies_to": "F_domain^nu",
        "needed_equation": "chi_D, n_mu, L_cg are scalar/tensor functionals of the local solution, not fixed external labels",
        "would_prove": "no preferred local frame/location force from the domain construction",
        "current_status": "not_derived",
        "failure_mode": "alpha1/alpha2/xi sectors remain quarantined",
    },
    {
        "mechanism": "universal_matter_coupling",
        "applies_to": "F_matter_nonmetric^nu",
        "needed_equation": "S_matter = S_matter[g_or_e, psi] only, with no species-dependent MTS charge",
        "would_prove": "clock/redshift/WEP nonmetric residuals vanish at the action level",
        "current_status": "not_derived",
        "failure_mode": "WEP and redshift residuals are retained and tightly bounded",
    },
]


RESIDUAL_VECTOR_MAP = [
    {
        "residual": "gamma_minus_1",
        "symbolic_formula": "C_TF epsilon_TF + C_rad epsilon_rad + C_bulk epsilon_bulk + C_nonmetric epsilon_nonmetric_light",
        "force_sources": "F_P^nu; F_boundary^nu; F_X^nu; F_matter_nonmetric^nu",
        "zero_conditions": "no trace-free projector/boundary stress, no radial scalar hair, no bulk MTS source, universal light/matter metric",
        "target_status": "source_locked_numeric",
    },
    {
        "residual": "beta_minus_1",
        "symbolic_formula": "C_rad2 epsilon_rad + C_nl epsilon_boundary_nonlinear + C_bulk2 epsilon_bulk",
        "force_sources": "F_boundary^nu; F_X^nu",
        "zero_conditions": "trace boundary is conserved monopole only; nonlinear scalar/boundary hair absent",
        "target_status": "source_locked_numeric",
    },
    {
        "residual": "eta_WEP",
        "symbolic_formula": "C_WEP epsilon_WEP + C_comp epsilon_species_charge + C_boundary epsilon_WEP_boundary",
        "force_sources": "F_matter_nonmetric^nu; F_boundary^nu",
        "zero_conditions": "universal matter coupling; no species-dependent MTS charge; no composition-dependent boundary hair",
        "target_status": "source_locked_numeric",
    },
    {
        "residual": "alpha_clock_redshift",
        "symbolic_formula": "C_clock epsilon_clock + C_nonmetric epsilon_clock_metric_mismatch",
        "force_sources": "F_matter_nonmetric^nu; F_boundary^nu",
        "zero_conditions": "single metric/coframe clock coupling and no direct local clock charge",
        "target_status": "source_locked_numeric",
    },
    {
        "residual": "preferred_frame_alpha1_alpha2",
        "symbolic_formula": "C_vec epsilon_vec + C_domain epsilon_domain_vec + C_P epsilon_P_vector",
        "force_sources": "F_domain^nu; F_P^nu; F_boundary^nu",
        "zero_conditions": "no local vector/domain frame; covariant projector and domain selection",
        "target_status": "quarantined_until_numeric_source_lock",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "symbolic_formula": "C_TF2 epsilon_TF_lge2 + C_domain2 epsilon_domain_aniso + C_ext epsilon_external_aniso",
        "force_sources": "F_domain^nu; F_P^nu; F_boundary^nu",
        "zero_conditions": "no trace-free multipole boundary/projector/domain anisotropy",
        "target_status": "quarantined_until_numeric_source_lock",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "symbolic_formula": "C_bulkG epsilon_bulk + C_radG epsilon_rad + C_L epsilon_Lcg_grad",
        "force_sources": "F_X^nu; F_boundary^nu; F_domain^nu",
        "zero_conditions": "no bulk MTS source, no radial scalar hair, no local L_cg gradient force",
        "target_status": "quarantined_until_numeric_source_lock",
    },
]


SOURCE_LOCKED_BOUNDS = [
    {
        "residual": "gamma_minus_1",
        "source_locked_scale_abs": 2.3e-5,
        "runner_status": "source_locked_ready",
    },
    {
        "residual": "beta_minus_1",
        "source_locked_scale_abs": 7.8e-5,
        "runner_status": "source_locked_ready",
    },
    {
        "residual": "eta_WEP",
        "source_locked_scale_abs": 2.8e-15,
        "runner_status": "source_locked_ready",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale_abs": 3.1e-5,
        "runner_status": "source_locked_ready",
    },
    {
        "residual": "preferred_frame_alpha1_alpha2",
        "source_locked_scale_abs": "",
        "runner_status": "quarantined_until_numeric_source_lock",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "source_locked_scale_abs": "",
        "runner_status": "quarantined_until_numeric_source_lock",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "source_locked_scale_abs": "",
        "runner_status": "quarantined_until_numeric_source_lock",
    },
]


def source_locked_join_rows() -> list[dict[str, Any]]:
    bounds = {row["residual"]: row for row in SOURCE_LOCKED_BOUNDS}
    rows: list[dict[str, Any]] = []
    for residual in RESIDUAL_VECTOR_MAP:
        bound = bounds[residual["residual"]]
        rows.append(
            {
                "residual": residual["residual"],
                "force_sources": residual["force_sources"],
                "symbolic_formula": residual["symbolic_formula"],
                "source_locked_scale_abs": bound["source_locked_scale_abs"],
                "runner_status": bound["runner_status"],
                "allowed_use_now": "internal_numeric_guardrail" if bound["runner_status"] == "source_locked_ready" else "quarantine_no_numeric_pass",
            }
        )
    return rows


THEOREM_OR_RETAIN_DECISIONS = [
    {
        "sector": "bulk_X",
        "best_case": "maximum-principle/mass-gap theorem sets epsilon_bulk=epsilon_rad=0",
        "current_decision": "retain_symbolic_residual",
        "why": "local X operator, source terms, and sign conditions are not derived",
    },
    {
        "sector": "projector_bulk",
        "best_case": "topological P_D gives F_P_bulk=0",
        "current_decision": "conditional_zero_not_full_promotion",
        "why": "parent selection and boundary charge closure remain open",
    },
    {
        "sector": "boundary_multipoles",
        "best_case": "class-only boundary action leaves only conserved monopole",
        "current_decision": "retain_symbolic_residual",
        "why": "class-only action, no angular representative, and regular matching are not derived",
    },
    {
        "sector": "domain_preferred_frame",
        "best_case": "covariant domain selector produces no local preferred-frame/location residual",
        "current_decision": "retain_quarantined_residual",
        "why": "preferred-frame and xi numeric source locks are not ingested yet",
    },
    {
        "sector": "matter_nonmetric",
        "best_case": "single metric/coframe universal coupling kills WEP/clock residuals",
        "current_decision": "retain_source_locked_residual",
        "why": "universal coupling theorem is not derived and WEP/clock bounds are already source-locked",
    },
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive the local EH exterior operator after imposing Ward-closed/nohair conditions as explicit assumptions",
        "pass_condition": "show the surviving weak-field operator is EH plus Lambda with no extra propagating local modes",
    },
    {
        "priority": 2,
        "target": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "task": "turn the symbolic residual vector into a source-locked numeric budget runner",
        "pass_condition": "ready sectors compare to source-locked gamma/beta/WEP/clock scales and quarantined sectors remain quarantined",
    },
    {
        "priority": 3,
        "target": "360-universal-matter-coupling-theorem-attempt.md",
        "task": "attack the most dangerous local coupling debt directly",
        "pass_condition": "derive one metric/coframe coupling or explicitly retain WEP/clock residuals",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for doc in SOURCE_DOCS:
        source_path = ROOT / doc["path"]
        rows.append(
            {
                "source_file": doc["path"],
                "exists": source_path.exists(),
                "role": doc["role"],
            }
        )
    return rows


def gate_result_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["source_file"] for row in source_rows if not row["exists"]]
    ready_bounds = sum(1 for row in SOURCE_LOCKED_BOUNDS if row["runner_status"] == "source_locked_ready")
    quarantined = sum(1 for row in SOURCE_LOCKED_BOUNDS if row["runner_status"].startswith("quarantined"))
    retained = sum(1 for row in THEOREM_OR_RETAIN_DECISIONS if "retain" in row["current_decision"])
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all cited source files exist" if not missing else "; ".join(missing),
        },
        {
            "gate": "Ward_forces_mapped",
            "status": "pass",
            "evidence": f"{len(FORCE_FATE_MAP)} force channels mapped to theorem-zero, boundary-only, or retained residual outcomes",
        },
        {
            "gate": "nohair_mechanisms_identified",
            "status": "pass",
            "evidence": f"{len(NOHAIR_MECHANISM_CANDIDATES)} candidate mechanisms written with needed equations and failure modes",
        },
        {
            "gate": "source_locked_bounds_joined",
            "status": "pass",
            "evidence": f"{ready_bounds} numeric ready sectors; {quarantined} quarantined sectors",
        },
        {
            "gate": "retained_residuals_carried",
            "status": "pass",
            "evidence": f"{retained} sectors retained rather than set to zero by assertion",
        },
        {
            "gate": "local_nohair_theorem_proved",
            "status": "fail",
            "evidence": "candidate mechanisms are identified but key parent equations/signs/couplings are not derived",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "force channels remain conditional or retained; EH exterior not yet derived",
        },
        {
            "gate": "PPN_pass_claimed",
            "status": "fail",
            "evidence": "numeric comparison runner deferred until residual coefficients/equations exist",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "local_nohair_proved": False,
            "local_GR_promoted": False,
            "PPN_pass_claimed": False,
            "main_result": "Ward force channels now have legal fates: theorem-zero, boundary-only, or retained symbolic PPN residual with source-lock status",
            "next_target": NEXT_TARGET,
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    run_dir = ROOT / "runs" / f"{args.timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    source_join = source_locked_join_rows()
    gates = gate_result_rows(source_rows)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": source_rows,
        "force_fate_map.csv": FORCE_FATE_MAP,
        "nohair_mechanism_candidates.csv": NOHAIR_MECHANISM_CANDIDATES,
        "retained_residual_vector.csv": RESIDUAL_VECTOR_MAP,
        "source_locked_residual_join.csv": source_join,
        "theorem_or_retain_decisions.csv": THEOREM_OR_RETAIN_DECISIONS,
        "next_queue.csv": NEXT_QUEUE,
        "gate_results.csv": gates,
        "decision.csv": decisions,
    }
    for name, rows in outputs.items():
        write_csv(results_dir / name, rows)

    status = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "generated": sorted(outputs),
        "source_paths_missing": sum(1 for row in source_rows if not row["exists"]),
        "force_channels_mapped": len(FORCE_FATE_MAP),
        "nohair_mechanisms": len(NOHAIR_MECHANISM_CANDIDATES),
        "residuals_mapped": len(RESIDUAL_VECTOR_MAP),
        "numeric_source_locked_sectors": sum(1 for row in SOURCE_LOCKED_BOUNDS if row["runner_status"] == "source_locked_ready"),
        "quarantined_sectors": sum(1 for row in SOURCE_LOCKED_BOUNDS if row["runner_status"].startswith("quarantined")),
        "local_nohair_proved": False,
        "local_GR_promoted": False,
        "PPN_pass_claimed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
