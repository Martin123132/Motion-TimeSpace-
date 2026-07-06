from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    row_list = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_silence_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "KZS4485_0_variational_derivative",
            "object": "sigma_K2_source_derivative",
            "statement": "Let sigma_K2=K2*C_K2_unit. The K2 contribution to the same-frame EH metric equation is obtained by differentiating the action-derived sources and residuals with respect to sigma_K2 before solving the public metric equation.",
            "formula": "partial_sigma E_metric = kappa_eff partial_sigma T_H + partial_sigma E_res + partial_sigma B_l2 + partial_sigma R_readout",
            "derived_result": "K2 can source a public quadrupole only through Hilbert stress, residual equation, boundary data, or readout deformation.",
            "current_status": "EXACT_SOURCE_DERIVATIVE_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KZS4485_1_clean_zero_theorem",
            "object": "K2_source_silent_branch",
            "statement": "If sigma_K2 is absent from S_src, S_extra, boundary/matching data and public readout, then all four source derivatives vanish.",
            "formula": "partial_sigma T_H=partial_sigma E_res=partial_sigma B_l2=partial_sigma R_readout=0 => A_surface_K2=0",
            "derived_result": "On the strict source-silent branch, Pi_J2_metric*K2=0; the K2 bookkeeping lane produces no public J2 metric amplitude.",
            "current_status": "CONDITIONAL_ZERO_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KZS4485_2_current_artifact_audit",
            "object": "current_owned_K2_source",
            "statement": "The current corpus defines K2 as an unsigned scalar residual/projection lane and repeatedly refuses a live source-owned Khat/STF kernel.",
            "formula": "K2:=|W2 M_Lambda|; current_owned(deltaT_H_K2, deltaE_res_K2, deltaB_l2_K2, deltaReadout_l2_K2)=none",
            "derived_result": "No current source-owned finite A_surface_K2 row is available; using K2*C_K2_unit as a public metric amplitude remains blocked.",
            "current_status": "NO_OWNED_SOURCE_DERIVATIVE_FOUND",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KZS4485_3_hessian_counterroute",
            "object": "finite_Khat_source_counterroute",
            "statement": "The tracefree-Hessian/improvement candidate can provide a finite quadrupole source if, and only if, the parent adopts it as live Khat and controls leakage/conservation.",
            "formula": "deltaK_STF^ij = sigma_K2 R_K2(r)Y_a^ij; M2_K2=-(kappa_STF/5)I4[hat_R]",
            "derived_result": "The finite branch is mathematically organized but parent unsigned, so it stays as a product-bound route.",
            "current_status": "FINITE_COUNTERROUTE_RETAINED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KZS4485_4_no_identity_or_cancellation",
            "object": "guardrail",
            "statement": "Neither source silence nor finite-source failure allows setting Pi_J2_metric=1 or hiding K2 in another residual by cancellation.",
            "formula": "Pi_J2_metric=1 only if P_surf,l2 G_EH[source_K2]=K2*C_K2_unit in the same source/coframe/radius convention",
            "derived_result": "Identity shortcuts and cross-channel cancellation are rejected.",
            "current_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KZS4485_5_verdict",
            "object": "K2_source_status",
            "statement": "The present owned branch is source-silent by lack of parent source derivative; the physical parent-zero claim remains unsigned because the parent action inventory is not globally signed.",
            "formula": "owned_source_response=0; parent_global_zero=false; finite_fallback_rows_required=true",
            "derived_result": "This advances the framework: K2 is not allowed to masquerade as a metric source, but a finite source branch remains available if the parent later supplies real derivative data.",
            "current_status": "OWNED_SOURCE_RESPONSE_ZERO_GLOBAL_PARENT_ZERO_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def current_source_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "CSA4485_0_K2_definition",
            "source_slot": "sigma_K2",
            "current_evidence": "K2 is defined as an unsigned magnitude |W2 M_Lambda| with C_K2_unit supplying a dimensionless per-unit residual coefficient.",
            "owned_zero_result": "not a source by itself",
            "finite_branch_if_failed": "recover signed s_K2 and source tensor basis before any metric amplitude can be computed",
            "status": "LANE_DEFINED_NOT_ACTION_SOURCE",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CSA4485_1_Hilbert_source",
            "source_slot": "partial_sigma T_H",
            "current_evidence": "No source-owned same-frame matter/EM action derivative with respect to sigma_K2 is present.",
            "owned_zero_result": "current owned Hilbert derivative is zero/absent",
            "finite_branch_if_failed": "declare a Hilbert stress derivative deltaT_H_K2 with support, units and tracefree projection",
            "status": "NO_OWNED_HILBERT_SOURCE_DERIVATIVE",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CSA4485_2_residual_equation",
            "source_slot": "partial_sigma E_res",
            "current_evidence": "3175/3178 do not find a live source-owned Khat kernel; 3179/3180 keep Hessian leakage as conditional.",
            "owned_zero_result": "current owned residual derivative is absent",
            "finite_branch_if_failed": "adopt Khat/Hessian source with kappa_STF, R_K2 or c_ext and leakage/conservation bounds",
            "status": "NO_OWNED_RESIDUAL_SOURCE_DERIVATIVE",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CSA4485_3_boundary",
            "source_slot": "partial_sigma B_l2",
            "current_evidence": "Boundary/matching response to sigma_K2 is not parent-owned; sharp matching creates shell/layer terms if a Hessian profile is adopted.",
            "owned_zero_result": "no owned boundary amplitude",
            "finite_branch_if_failed": "source deltaB_l2_K2 or prove fixed/no-flux/asymptotic boundary silence",
            "status": "BOUNDARY_DERIVATIVE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CSA4485_4_readout",
            "source_slot": "partial_sigma R_readout",
            "current_evidence": "External-readout no-backreaction theorem applies only if K2/readout is post-solution or source-at-zero, not material.",
            "owned_zero_result": "conditional readout derivative zero",
            "finite_branch_if_failed": "declare a K2-dependent public metric/readout deformation and bound it",
            "status": "READOUT_ZERO_CONDITIONAL_PARENT_ROLE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CSA4485_5_source_domain",
            "source_slot": "T_source",
            "current_evidence": "Solar-source transfer for the local K2 lane remains missing.",
            "owned_zero_result": "no direct solar bound applies to current K2 lane",
            "finite_branch_if_failed": "construct direct solar K2 source lane or universality theorem",
            "status": "SOLAR_SOURCE_TRANSFER_MISSING",
            "valid_for_claim": False,
        },
    ]


def finite_quadrupole_rows(c_k2_unit: float, half_bound: float) -> List[Dict[str, object]]:
    return [
        {
            "amp_id": "FQA4485_0_general_functional",
            "quantity": "A_surface_K2",
            "branch": "finite_source_general",
            "formula": "A_surface_K2=P_surf,l2 G_EH[kappa_eff deltaT_H_K2 + deltaE_res_K2 + deltaB_l2 + deltaReadout_l2]",
            "meaning": "The only honest finite public quadrupole amplitude if K2 is not source-silent.",
            "needed_inputs": "deltaT_H_K2; deltaE_res_K2; deltaB_l2; deltaReadout_l2; T_source; support/radius/coframe normalization",
            "status": "EXACT_FUNCTIONAL_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "amp_id": "FQA4485_1_signed_source_moment",
            "quantity": "A_surface_K2",
            "branch": "signed_STF_moment",
            "formula": f"A_surface_K2=s_K2*{c_k2_unit:.15e}*M2_K2",
            "meaning": "3176/3177 signed STF branch once s_K2 and M2_K2 are parent-owned.",
            "needed_inputs": "signed s_K2, parent axis, R_K2(r), kappa_STF, q_K2 conservation closure",
            "status": "SOURCE_MOMENT_FORMULA_AVAILABLE_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "amp_id": "FQA4485_2_hessian_projected_moment",
            "quantity": "M2_K2_projected",
            "branch": "tracefree_Hessian_candidate",
            "formula": "M2_K2=-(kappa_STF/5)I4[hat_R]; quadratic/exterior projected branch gives M2_K2^proj=(4/25)kappa_STF*c_ext",
            "meaning": "The best finite candidate has a concrete source moment, but parent adoption and leakage silence remain unsigned.",
            "needed_inputs": "kappa_STF, c_ext or I4[hat_R], leakage DeltaK_TF, metric-response safety",
            "status": "CONDITIONAL_HESSIAN_PRODUCT_BOUND_BRANCH",
            "valid_for_claim": False,
        },
        {
            "amp_id": "FQA4485_3_product_bound",
            "quantity": "s_K2_M2_K2_bound",
            "branch": "nonclaim_bound",
            "formula": f"|s_K2*M2_K2| <= {half_bound:.15e}",
            "meaning": "If either s_K2 or M2_K2 is later derived, this becomes a bound on the other; if both are derived, the local STF/J2 branch becomes testable.",
            "needed_inputs": "source-backed s_K2 and/or M2_K2",
            "status": "PRODUCT_BOUND_CARRIED_FORWARD_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "amp_id": "FQA4485_4_zero_branch_pressure",
            "quantity": "J2_pressure_on_current_owned_K2",
            "branch": "source_silent",
            "formula": "A_surface_K2=0 => no J2 pressure from current owned K2 source derivative",
            "meaning": "This removes one fake pressure route; it is not a proof of full local GR because parent EH selector, source-domain and residual gates remain conditional.",
            "needed_inputs": "parent signature if promoted from current-owned response to global theorem",
            "status": "CURRENT_OWNED_RESPONSE_ZERO_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def next_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "input_id": "NI4485_0_Z_K2_source_silence",
            "symbol": "Z_K2_source",
            "definition": "boolean certificate that sigma_K2 is absent from S_src, S_extra, boundary data and readout",
            "current_value": "CURRENT_OWNED_RESPONSE_ZERO_BUT_PARENT_CERTIFICATE_MISSING",
            "needed_for": "promote source-silent K2 branch",
            "valid_for_claim": False,
        },
        {
            "input_id": "NI4485_1_deltaT_H_K2",
            "symbol": "deltaT_H_K2",
            "definition": "tracefree l=2 Hilbert stress derivative with respect to sigma_K2",
            "current_value": "MISSING",
            "needed_for": "finite A_surface_K2",
            "valid_for_claim": False,
        },
        {
            "input_id": "NI4485_2_deltaE_res_K2",
            "symbol": "deltaE_res_K2",
            "definition": "extra MTS residual equation derivative after EH baseline subtraction",
            "current_value": "MISSING; Hessian candidate conditional only",
            "needed_for": "finite A_surface_K2 or residual-l2 scorer",
            "valid_for_claim": False,
        },
        {
            "input_id": "NI4485_3_M2_K2",
            "symbol": "M2_K2",
            "definition": "dimensionless compact source moment converting signed K2 amplitude into surface quadrupole amplitude",
            "current_value": "FORMULA_DERIVED_INPUTS_MISSING",
            "needed_for": "direct STF/J2 product bound",
            "valid_for_claim": False,
        },
        {
            "input_id": "NI4485_4_DeltaK_TF",
            "symbol": "DeltaK_TF",
            "definition": "tracefree tensor-harmonic leakage beyond pure projected Hessian moment",
            "current_value": "MISSING_BOUND",
            "needed_for": "Hessian finite branch safety",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    audit_rows: List[Dict[str, object]],
    amplitude_rows: List[Dict[str, object]],
    input_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4485_0_sources",
            "gate": "all cited source paths and needles exist",
            "gate_pass": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "detail": "source hygiene only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4485_1_source_silence_theorem_written",
            "gate": "K2 source-silent theorem is written",
            "gate_pass": any(row.get("theorem_id") == "KZS4485_1_clean_zero_theorem" for row in theorem_rows),
            "claim_allowed": False,
            "detail": "conditional theorem, not full parent signature",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4485_2_current_owned_source_response_zero",
            "gate": "current source-owned K2 derivative is absent",
            "gate_pass": any(row.get("theorem_id") == "KZS4485_2_current_artifact_audit" for row in theorem_rows),
            "claim_allowed": False,
            "detail": "blocks fake J2 source claim from current K2 artifact",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4485_3_parent_global_zero_signed",
            "gate": "parent action signs full K2 source silence",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "parent action inventory/readout/boundary/source-domain signatures remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4485_4_finite_amplitude_ready",
            "gate": "finite A_surface_K2 has source-backed values",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "deltaT_H_K2, deltaE_res_K2, M2_K2 and DeltaK_TF remain missing or conditional",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4485_5_no_generated_claim_rows",
            "gate": "generated rows remain private nonclaim",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [sources, theorem_rows, audit_rows, amplitude_rows, input_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "no local-GR, J2, PPN, R10, clock, orbital or EM claim is promoted",
            "valid_for_claim": False,
        },
    ]
