from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional


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


def as_float(value: object) -> Optional[float]:
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or text.upper().startswith("MISSING") or text == "alpha(lambda)":
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def row_by_observable(rows: Iterable[Mapping[str, object]], observable: str) -> Optional[Mapping[str, object]]:
    for row in rows:
        if str(row.get("observable", "")) == observable:
            return row
    return None


def theorem_clause_rows() -> List[Dict[str, object]]:
    return [
        {
            "clause_id": "SCU4465_0_same_metric_matter_functor",
            "clause": "ordinary local matter is a functor of one observed metric/coframe",
            "mathematical_form": "S_A = S_A[Psi_A, g_obs, nabla(g_obs), theta_A] for all ordinary sectors A",
            "what_it_buys": "all inertial and gravitational source readout begins from one Hilbert stress tensor",
            "failure_mode": "a second metric/disformal/source readout gives material-dependent C_A",
            "status": "PRIVATE_BRANCH_CONDITIONAL",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCU4465_1_no_source_Hom",
            "clause": "no source-only homomorphism or material label enters the source side",
            "mathematical_form": "Hom_source(A, X) = empty except through T_H[g_obs] and fixed standard constants",
            "what_it_buys": "there is no independent coefficient K_A multiplying the same mass-energy differently for Ti, Pt, clocks, or bulk sources",
            "failure_mode": "a hidden source label reopens Delta_C_AB and WEP",
            "status": "EXACT_REQUIRED_CLAUSE_NOT_GLOBAL_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCU4465_2_source_label_forgetting",
            "clause": "the parent quotient forgets composition labels after constructing the Hilbert source",
            "mathematical_form": "q_source(A) = T_H[A] with no retained material tag in the field equation",
            "what_it_buys": "composition can change mass value but not charge-per-Hilbert-mass normalization",
            "failure_mode": "material tags survive projection and act as differential charges",
            "status": "DERIVATION_CLAUSE_WRITTEN_PRIVATE_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCU4465_3_constant_sector_silence",
            "clause": "dimensionless internal constants do not vary with the finite local source coordinate",
            "mathematical_form": "d ln alpha_EM/dchi = d ln(m_q/Lambda_QCD)/dchi = d ln(m_e/Lambda_QCD)/dchi = ... = 0",
            "what_it_buys": "binding-energy and composition sensitivities cannot generate a differential scalar/source charge",
            "failure_mode": "varying internal constants generate Delta_C_AB = sum_j (s_Aj-s_Bj) b_j",
            "status": "NEEDED_FOR_STRICT_COMPOSITION_ZERO",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCU4465_4_common_conformal_mode_split",
            "clause": "a common conformal/unit rescaling is separated from composition-dependent charges",
            "mathematical_form": "M_A(chi) = Omega(chi) * Mbar_A(theta_bar) gives C_A = d ln Omega/dchi = C_common",
            "what_it_buys": "Delta_C_AB=0 even when a universal common-mode fifth force remains",
            "failure_mode": "mistaking WEP zero for R10/PPN/orbital safety",
            "status": "EXACT_SPLIT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCU4465_5_worldtube_source_normalization",
            "clause": "source body charge uses the same Hilbert/Hamiltonian worldtube mass as Newton/Poisson",
            "mathematical_form": "C_S = Q_X[S]/M_H^dress[S] with Q_X proportional to M_H^dress or Q_X=0",
            "what_it_buys": "source normalization cannot be chosen after fitting orbital GM",
            "failure_mode": "C_S becomes an independent hidden fitted-source parameter",
            "status": "CONDITIONAL_ON_H_TAU_MHREF_AND_BOUNDARY_SILENCE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_charge_derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "DER4465_0_definition",
            "statement": "define the finite source charge per inertial/Hilbert mass",
            "equation": "C_A = d ln M_A(chi) / d chi",
            "result": "WEP differentials depend on Delta_C_AB = C_A - C_B",
            "status": "DEFINITION",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DER4465_1_composite_decomposition",
            "statement": "composite masses split into a common scale plus dimensionless internal sensitivities",
            "equation": "C_A = C_common + sum_j s_Aj b_j, where s_Aj=d ln M_A/d ln theta_j and b_j=d ln theta_j/dchi",
            "result": "Delta_C_AB = sum_j (s_Aj-s_Bj) b_j",
            "status": "DERIVED_DIFFERENTIAL_CHARGE_LAW",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DER4465_2_source_label_forgetting_zero",
            "statement": "if the parent has no composition source-Hom and all internal dimensionless b_j vanish",
            "equation": "b_j=0 for all j, hence C_A=C_common for every ordinary body A",
            "result": "Delta_C_AB=0 and eta_AB=0 for MICROSCOPE-style differential WEP",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DER4465_3_decoupled_scalar_zero",
            "statement": "if the local finite source coordinate does not enter the matter action",
            "equation": "d S_matter / d chi = 0, hence C_A=C_S=0",
            "result": "WEP, R10 fifth-force alpha, and scalar source response vanish together",
            "status": "STRONG_ZERO_ROUTE_IF_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DER4465_4_common_mode_warning",
            "statement": "universal source charge is not enough for local-GR",
            "equation": "C_A=C_B=C_common != 0 gives eta_AB=0 but alpha_eff ~ C_common*C_S*alpha_0",
            "result": "WEP can pass while R10/PPN/orbital fifth-force rows still fail",
            "status": "COMMON_MODE_SURVIVES_WEP",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DER4465_5_material_vector_fallback",
            "statement": "if any b_j survives, Ti/Pt material sensitivities are required",
            "equation": "|sum_j (s_Ti,j-s_Pt,j) b_j * C_S * alpha_0 * Y(lambda)| <= eta_bound",
            "result": "finite WEP branch is scoreable only with a source-backed material vector and range/profile owner",
            "status": "FALLBACK_OPERATOR_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
    ]


def wep_response_bound_rows(local_bound_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    source = row_by_observable(local_bound_rows, "eta_WEP_source_charge")
    eta_bound = as_float(source.get("upper_bound")) if source else None
    measured = source.get("measured_value", "MISSING") if source else "MISSING"
    sigma = source.get("one_sigma", "MISSING") if source else "MISSING"
    source_ref = source.get("reference_path_or_url", "MISSING_SOURCE") if source else "MISSING_SOURCE"
    eta_bound_text = f"{eta_bound:.12g}" if eta_bound is not None else "MISSING_ETA_BOUND"
    return [
        {
            "runner_id": "WEP4465_0_zero_branch",
            "branch": "source-label-forgetting same-Hilbert branch",
            "prediction": "Delta_C_TiPt = 0; eta_TiPt = 0",
            "bound": eta_bound_text,
            "measured_value": measured,
            "one_sigma": sigma,
            "source_ref": source_ref,
            "score_status": "PASSES_CONDITIONALLY_IF_THEOREM_CLAUSES_SIGNED",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "runner_id": "WEP4465_1_common_mode_branch",
            "branch": "C_A=C_B=C_common nonzero",
            "prediction": "eta_TiPt = 0 but R10/PPN/orbital alpha_common remains",
            "bound": eta_bound_text,
            "measured_value": measured,
            "one_sigma": sigma,
            "source_ref": source_ref,
            "score_status": "WEP_SAFE_ONLY_NOT_LOCAL_GR_SAFE",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "runner_id": "WEP4465_2_finite_material_vector",
            "branch": "composition-dependent charge vector survives",
            "prediction": "|Delta_C_TiPt*C_S*alpha_0*Y(lambda)| <= eta_bound",
            "bound": eta_bound_text,
            "measured_value": measured,
            "one_sigma": sigma,
            "source_ref": source_ref,
            "score_status": "OPERATOR_READY_MATERIAL_VECTOR_AND_RANGE_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def material_vector_fallback_rows(local_bound_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    source = row_by_observable(local_bound_rows, "eta_WEP_source_charge")
    eta_bound = as_float(source.get("upper_bound")) if source else None
    return [
        {
            "fallback_id": "MV4465_0_required_vector",
            "needed_input": "Delta_s_TiPt_j = s_Ti,j - s_Pt,j for each active source coefficient b_j",
            "current_value": "MISSING_SOURCE_BACKED_MATERIAL_SENSITIVITY_VECTOR",
            "formula_use": "Delta_C_TiPt = sum_j Delta_s_TiPt_j * b_j",
            "claim_gate": "valid only if material vector, b_j coefficients, range/profile and readout normalization are same-branch",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "fallback_id": "MV4465_1_required_coefficients",
            "needed_input": "b_j = d ln theta_j / d chi and common alpha_0, C_S, lambda",
            "current_value": "MISSING_PARENT_SOURCE_COEFFICIENTS_AND_RANGE",
            "formula_use": "eta_TiPt = Delta_C_TiPt*C_S*alpha_0*(1+r/lambda)exp(-r/lambda)",
            "claim_gate": "cannot use empirical eta bound as a coefficient",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "fallback_id": "MV4465_2_current_product_bound",
            "needed_input": "source-backed product only",
            "current_value": f"|Delta_C_TiPt*C_S*alpha_0*Y(lambda)| <= {eta_bound:.12g}" if eta_bound else "MISSING_ETA_BOUND",
            "formula_use": "a future vector row must satisfy this product inequality before any WEP pass",
            "claim_gate": "bound exists but prediction side is missing",
            "score_ready": bool(eta_bound),
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4465_0_theorem_result",
            "finding": "Delta_C_AB=0 is exactly derivable under source-label-forgetting and constant-sector silence",
            "consequence": "MICROSCOPE/WEP can be closed in the private same-Hilbert branch without numeric material tuning",
            "next_action": "do not confuse differential WEP closure with common-mode scalar/R10 closure",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4465_1_common_mode_result",
            "finding": "a universal C_common survives WEP because C_A=C_B, but it still sources a common fifth force",
            "consequence": "R10/PPN/orbital tests, not MICROSCOPE, become the pressure point for universal R2/scalar coupling",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4465_2_fallback_result",
            "finding": "finite composition-dependent WEP scoring needs Ti/Pt material sensitivity vectors plus parent b_j coefficients and range/profile",
            "consequence": "the fallback runner is formula-ready but not claim-grade",
            "next_action": "only fill finite WEP vector if source-label-forgetting fails",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    clauses: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    wep_rows: List[Dict[str, object]],
    material_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok = all(bool(row.get("local_path_exists")) and bool(row.get("needle_found")) for row in source_rows)
    has_zero = any(row.get("status") == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in derivations)
    has_common_warning = any(row.get("status") == "COMMON_MODE_SURVIVES_WEP" for row in derivations)
    has_wep_bound = any(row.get("runner_id") == "WEP4465_2_finite_material_vector" and row.get("bound") != "MISSING_ETA_BOUND" for row in wep_rows)
    fallback_blocked = any("MISSING" in str(row.get("current_value")) for row in material_rows[:2])
    no_claims = not any(
        str(row.get("valid_for_claim")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true"
        for row in clauses + derivations + wep_rows + material_rows
    )
    return [
        {
            "gate_id": "CG4465_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": source_ok,
            "claim_allowed": False,
            "detail": "source register validates 4464, 4462, local bounds and prior source-coefficient files",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4465_1_zero_theorem",
            "claim": "Delta_C_AB zero theorem is explicitly derived",
            "gate_pass": has_zero,
            "claim_allowed": False,
            "detail": "conditional theorem: no source-Hom plus source-label-forgetting plus constant-sector silence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4465_2_common_mode_guard",
            "claim": "WEP closure is not mistaken for R10/local-GR closure",
            "gate_pass": has_common_warning,
            "claim_allowed": False,
            "detail": "C_A=C_B can still leave C_common != 0",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4465_3_wep_bound_operator",
            "claim": "MICROSCOPE source-charge bound operator is written",
            "gate_pass": has_wep_bound,
            "claim_allowed": False,
            "detail": "eta <= 2.8e-15 anchors finite product only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4465_4_finite_fallback_blocked",
            "claim": "finite material-vector WEP fallback is claim-ready",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "blocked intentionally until material sensitivity vector, parent coefficients and range/profile are sourced" if fallback_blocked else "unexpected: fallback inputs appear filled",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4465_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR claim evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4465 is private theorem/fallback discipline",
            "valid_for_claim": False,
        },
    ]
