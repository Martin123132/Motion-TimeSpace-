from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def scale_law_attempt_rows() -> List[Dict[str, object]]:
    return [
        {
            "route_id": "KSL4463_0_topological_lock",
            "candidate_scale_law": "S_top^kappa=C_top int A_3 wedge d ln(kappa_*/kappa_0)",
            "what_it_derives": "d ln(kappa_*/kappa_0)=0 on connected local domains",
            "what_it_does_not_derive": "the numerical value of kappa_0 or kappa_eff",
            "needed_to_predict_G": "parent-owned kappa_0 or quantized flux normalization with dimensions of kappa_eff",
            "verdict": "LOCKS_CONSTANCY_NOT_VALUE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "KSL4463_1_flux_quantization",
            "candidate_scale_law": "integral dA_3 = n q_3 and a parent normalization converts flux to ln(kappa_*/kappa_0)",
            "what_it_derives": "possible discrete superselection labels for kappa_*",
            "what_it_does_not_derive": "absolute dimensionful kappa unless q_3, C_top, and kappa_0 are parent-normalized",
            "needed_to_predict_G": "source-backed q_3/C_top/kappa_0 with units and no measured-G input",
            "verdict": "POSSIBLE_ROUTE_UNSIGNED_AND_VALUE_FREE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "KSL4463_2_induced_metric_scale",
            "candidate_scale_law": "1/kappa_eff ~ C_psi * Lambda_UV^2 or C_psi/ell_micro^2 from emergent psi metric covariance",
            "what_it_derives": "a structural way to obtain an EH coefficient from a microscopic cutoff/field density",
            "what_it_does_not_derive": "Lambda_UV, ell_micro, C_psi, field measure, or sign from current corpus",
            "needed_to_predict_G": "parent cutoff/cell density and induced-action calculation",
            "verdict": "PROMISING_BUT_UNSOURCED_SCALE_INPUT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "KSL4463_3_cell_or_refinement_scale",
            "candidate_scale_law": "kappa_eff proportional to ell_cell^2/(hbar*c) or equivalent action-normalized cell area",
            "what_it_derives": "dimensionally plausible coupling from a physical grain scale",
            "what_it_does_not_derive": "ell_cell, shape factor, action normalization, or why the grain is not a gauge refinement",
            "needed_to_predict_G": "parent-owned physical cell scale not defined using Planck length or measured G",
            "verdict": "CIRCULAR_IF_ELL_CELL_EQUALS_L_PLANCK_BY_DECLARATION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "KSL4463_4_PhiG_gamma_inversion",
            "candidate_scale_law": "gamma = Phi_G * sqrt(c^5/(G*hbar)) implies G = Phi_G^2*c^5/(gamma^2*hbar)",
            "what_it_derives": "an algebraic inversion if gamma and Phi_G are independently parent-predicted",
            "what_it_does_not_derive": "independent gamma, independent Phi_G, or an operational measurement not already using G",
            "needed_to_predict_G": "parent derivation of gamma and Phi_G from non-gravitational data",
            "verdict": "CURRENTLY_CIRCULAR_NUMEROLOGY_RISK",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "KSL4463_5_dimensionful_no_go",
            "candidate_scale_law": "dimensionless/topological/local covariance data alone cannot fix a dimensionful kappa_eff",
            "what_it_derives": "a no-go guard: constancy and universality are separable from numerical value",
            "what_it_does_not_derive": "numeric G",
            "needed_to_predict_G": "at least one non-circular parent dimensionful invariant: length, action scale, mass scale, flux quantum, cutoff, or density",
            "verdict": "NUMERIC_G_REMAINS_EMPIRICAL_CALIBRATION_UNTIL_SCALE_OWNER_EXISTS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def dimensional_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "DIM4463_0_kappa_units",
            "quantity": "kappa_eff",
            "units_statement": "SI: s^2/(kg*m); natural units hbar=c=1: length^2",
            "implication": "requires a dimensionful parent scale",
            "current_owner": "MISSING_NONCIRCULAR_PARENT_SCALE",
            "valid_for_claim": False,
        },
        {
            "audit_id": "DIM4463_1_G_units",
            "quantity": "G_cal",
            "units_statement": "G_cal=c^4*kappa_eff/(8*pi)",
            "implication": "G value follows only after kappa_eff value is fixed",
            "current_owner": "CALIBRATED_EMPIRICALLY_LIKE_GR",
            "valid_for_claim": False,
        },
        {
            "audit_id": "DIM4463_2_topological_sector",
            "quantity": "C_top,A_3,kappa_0",
            "units_statement": "topological variation fixes d ln(kappa/kappa0), not kappa0",
            "implication": "a dimensionful reference remains free unless parent-normalized",
            "current_owner": "CONSTANCY_OWNER_ONLY",
            "valid_for_claim": False,
        },
        {
            "audit_id": "DIM4463_3_psi_cutoff",
            "quantity": "Lambda_UV or ell_micro",
            "units_statement": "cutoff length/mass scale could set induced EH coefficient",
            "implication": "promising future derivation route but currently unsourced",
            "current_owner": "MISSING_PSI_MEASURE_AND_CUTOFF",
            "valid_for_claim": False,
        },
        {
            "audit_id": "DIM4463_4_hbar_measure",
            "quantity": "hbar/action-density line",
            "units_statement": "common action scale can remove species weights but does not by itself fix gravitational kappa",
            "implication": "helps universality/WEP, not numeric G",
            "current_owner": "CONDITIONAL_HBAR_MEASURE_BRANCH",
            "valid_for_claim": False,
        },
    ]


def residual_runner_rows() -> List[Dict[str, object]]:
    return [
        {
            "run_id": "CGR4463_0_clean_calibrated_GR",
            "branch": "same Hilbert source + constant kappa_eff + no scalar/frame/connection/EM leakage",
            "input_vector": "delta_kappa=0; Delta_C_AB=0; c_D=0; DeltaGamma_WEP=0; alpha_eff=0; epsilon_EM=0",
            "prediction": "G_cal constant; eta_AB=0; gamma-1=0; beta-1=0; alpha(lambda)=0; orbital GM source-owned",
            "status": "CONDITIONAL_SELECTOR_SMOKE",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "CGR4463_1_numeric_G_prediction_refusal",
            "branch": "attempt to infer numeric G from topological lock alone",
            "input_vector": "d ln kappa=0 only",
            "prediction": "constant but arbitrary kappa_eff",
            "status": "REFUSE_NUMERIC_G_CLAIM",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "CGR4463_2_universal_R2_scalar",
            "branch": "finite c2 pure metric scalar with universal Hilbert trace coupling",
            "input_vector": "C_matter=1; alpha_eff=1/3; lambda_R2 from c_R2_eff",
            "prediction": "Yukawa alpha=1/3 unless c2=0, C_matter=0, screening, or bound-passing short range is parent-signed",
            "status": "NEEDS_R10_PPN_ORBITAL_BOUND_CURVE_AND_C2_SOURCE",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "CGR4463_3_species_charge_WEP",
            "branch": "finite nonuniversal source charge",
            "input_vector": "Delta_C_AB=C_A-C_B; C_S; alpha_0; lambda",
            "prediction": "eta_AB ~= Delta_C_AB*C_S*alpha_0*(1+r/lambda)*exp(-r/lambda)",
            "status": "NEEDS_SPECIES_SOURCE_VECTOR_AND_WEP_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "CGR4463_4_G_drift",
            "branch": "finite source-coupling drift",
            "input_vector": "D_t ln kappa_eff or D_A ln(kappa_* Z_H)",
            "prediction": "Gdot/G = D_t ln kappa_eff plus readout corrections",
            "status": "NEEDS_DRIFT_PROFILE_OR_ZERO_THEOREM",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "CGR4463_5_frame_or_connection_leak",
            "branch": "second coframe/disformal/DeltaGamma leakage",
            "input_vector": "c_D,qbar_geom,DeltaGamma_WEP",
            "prediction": "WEP, clock, lightcone, PPN gamma and source-normalization residuals reopen",
            "status": "NEEDS_PROJECTION_MATRIX_AND_COMPONENT_VALUES",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4463_0_scale_law_result",
            "finding": "no current parent-owned non-circular dimensionful scale fixes kappa_eff",
            "consequence": "numeric G remains an empirical calibrated constant, which is fair for GR reduction",
            "next_action": "do not spend tokens trying to magic numeric G; test residual drift/species/range/frame/source deviations",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4463_1_best_derivation_route",
            "finding": "the only serious future numeric-G route is a parent scale owner: psi cutoff/cell density/flux quantum/action-scale law",
            "consequence": "write it as a source-owner theorem target, not as a claim",
            "next_action": "derive or source one scale owner before revisiting numeric G prediction",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4463_2_testing_route",
            "finding": "local competitiveness does not require numeric G prediction; it requires universal constant G and no residual leakage",
            "consequence": "residual runner becomes the empirical pressure point",
            "next_action": "build first score-ready residual runner for delta_kappa/species/R2/WEP/R10/PPN/orbital channels",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4463_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "source validation is performed by the generator",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4463_1_scale_law_attempted",
            "claim": "parent kappa scale-law routes have been tested",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "topological, flux, induced, cell, and Phi_G/gamma routes are audited",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4463_2_numeric_G_prediction",
            "claim": "MTS predicts numerical G",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "no non-circular dimensionful parent scale owner exists in current corpus",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4463_3_calibrated_G_policy",
            "claim": "calibrated universal G is acceptable for private local GR reduction",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "same standard as GR, with stricter residual no-absorption gates",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4463_4_residual_runner",
            "claim": "calibrated-G residual runner is staged",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "runner rows exist but are not score-ready until source/bound inputs are filled",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4463_5_next_target",
            "claim": "next residual scoring target selected",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "4464-Y5-R2FR-first-calibrated-G-residual-score-pack-WEP-R10-PPN-or-source-zero.md",
            "valid_for_claim": False,
        },
    ]
