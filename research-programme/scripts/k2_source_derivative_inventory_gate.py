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


def derivative_inventory_rows() -> List[Dict[str, object]]:
    return [
        {
            "inventory_id": "KDI4486_0_master_variation",
            "source_channel": "delta_sigma E_metric",
            "derivative_object": "partial_sigma[ G+Lambda g-kappa_eff T_H-E_res-B_l2-R_readout ]",
            "derived_law": "delta_sigma A_surface=P_surf,l2 G_EH[kappa_eff partial_sigma T_H+partial_sigma E_res+partial_sigma B_l2+partial_sigma R_readout]",
            "current_evidence": "4485 exact functional; 4484 EH weak-field operator; 4483 exterior Green owner",
            "branch_result": "EXACT_INVENTORY_IDENTITY",
            "needed_to_close": "source signatures for all four derivative channels or finite source rows",
            "valid_for_claim": False,
        },
        {
            "inventory_id": "KDI4486_1_hilbert_stress",
            "source_channel": "partial_sigma T_H",
            "derivative_object": "same-frame Hilbert stress derivative wrt sigma_K2",
            "derived_law": "partial_sigma T_H=0 if sigma_K2 is not in S_matter/S_src and no material marker/source extension names it",
            "current_evidence": "4485 current audit finds no deltaT_H_K2; 4474 no-backreaction lemma covers external/source-at-zero readout only",
            "branch_result": "CURRENT_ARTIFACT_ZERO_PARENT_GLOBAL_UNSIGNED",
            "needed_to_close": "parent action inventory proving sigma_K2 absent from material matter/EM/source action",
            "valid_for_claim": False,
        },
        {
            "inventory_id": "KDI4486_2_residual_equation",
            "source_channel": "partial_sigma E_res",
            "derivative_object": "extra MTS residual equation derivative wrt sigma_K2",
            "derived_law": "partial_sigma E_res=0 on source-silent branch; finite branch is K_L/Hessian or an explicit K_hat source kernel",
            "current_evidence": "3175/3178 find no live Khat source owner; 3179/3180 derive a conditional Hessian moment with leakage gates",
            "branch_result": "FINITE_HESSIAN_CANDIDATE_ROW_AVAILABLE_NONCLAIM",
            "needed_to_close": "parent adoption of K_L as live K_hat source or a zero theorem for all Khat residual derivatives",
            "valid_for_claim": False,
        },
        {
            "inventory_id": "KDI4486_3_boundary_matching",
            "source_channel": "partial_sigma B_l2",
            "derivative_object": "boundary, shell, matching and asymptotic l=2 derivative",
            "derived_law": "partial_sigma B_l2=0 only under fixed/no-flux/asymptotically silent boundary data; Hessian core/exterior glue creates shell terms unless owned",
            "current_evidence": "3180 sharp shell check; 4485 boundary derivative unsigned",
            "branch_result": "BOUNDARY_DERIVATIVE_LIVE_UNLESS_ZERO_CERTIFIED",
            "needed_to_close": "fixed-boundary theorem or explicit shell/layer source amplitude",
            "valid_for_claim": False,
        },
        {
            "inventory_id": "KDI4486_4_public_readout",
            "source_channel": "partial_sigma R_readout",
            "derivative_object": "public metric/readout deformation wrt sigma_K2",
            "derived_law": "partial_sigma R_readout=0 if K2 is post-solution diagnostic or source-at-zero before variation",
            "current_evidence": "4474 external readout lemma; 4485 readout role remains parent-unsigned",
            "branch_result": "CONDITIONAL_ZERO_NOT_GLOBAL",
            "needed_to_close": "signature that K2 never deforms the public metric readout or a bounded readout deformation row",
            "valid_for_claim": False,
        },
        {
            "inventory_id": "KDI4486_5_source_domain_transfer",
            "source_channel": "T_source",
            "derivative_object": "map from local K2/source lane into solar or laboratory source domain",
            "derived_law": "finite J2/PPN/R10 use requires the same source, radius, coframe and normalization convention as the public metric comparator",
            "current_evidence": "4484/4485 keep T_source missing; 4483 only owns the exterior profile after a surface amplitude exists",
            "branch_result": "SOURCE_DOMAIN_TRANSFER_MISSING",
            "needed_to_close": "solar-domain source transfer or proof that the lane is source-silent",
            "valid_for_claim": False,
        },
    ]


def source_silence_scorecard_rows() -> List[Dict[str, object]]:
    return [
        {
            "score_id": "SSS4486_0_current_artifact",
            "question": "Does the currently owned K2 artifact source the public metric?",
            "answer": "no owned source derivative is present",
            "proof_level": "CURRENT_ARTIFACT_SOURCE_SILENT",
            "what_this_allows": "block K2*C_K2_unit from being used as public J2 amplitude",
            "what_this_does_not_allow": "full local-GR, PPN, R10, clock or orbital claim",
            "valid_for_claim": False,
        },
        {
            "score_id": "SSS4486_1_parent_global_zero",
            "question": "Has the parent action globally proved sigma_K2 absent from all source/readout/boundary channels?",
            "answer": "not yet",
            "proof_level": "PARENT_GLOBAL_ZERO_UNSIGNED",
            "what_this_allows": "keep the zero branch as a clean theorem target",
            "what_this_does_not_allow": "turn absence of current source rows into a universal theorem",
            "valid_for_claim": False,
        },
        {
            "score_id": "SSS4486_2_finite_branch",
            "question": "Is there a mathematically usable finite K2 source input row?",
            "answer": "yes, a projected Hessian moment exists conditionally",
            "proof_level": "FIRST_SYMBOLIC_INPUT_ROW_FILLED",
            "what_this_allows": "test the product-bound route once kappa_STF, c_ext, s_K2 and leakage are sourced",
            "what_this_does_not_allow": "claim the finite branch is physical before parent adoption and leakage control",
            "valid_for_claim": False,
        },
        {
            "score_id": "SSS4486_3_best_next",
            "question": "What is the sharpest next physical fork?",
            "answer": "adopt or reject the Hessian carrier as a live metric source",
            "proof_level": "NEXT_TARGET_SELECTED",
            "what_this_allows": "stop circling K2 generally and attack K_L -> K_hat / DeltaK_TF directly",
            "what_this_does_not_allow": "skip the coupling/source-owner decision",
            "valid_for_claim": False,
        },
    ]


def first_m2k2_input_rows(product_bound: float, recast_bound: float) -> List[Dict[str, object]]:
    return [
        {
            "input_id": "M2I4486_0_projected_hessian_moment",
            "quantity": "M2_K2_projected_candidate",
            "formula": "M2_K2^proj=(4/25)*kappa_STF*c_ext",
            "derivation": "3179 gives P_Y[K_L]=D2[F]Y_a; 3180 integration by parts gives I4_D2=-4*c_ext/5; 3177 normalization gives M2_K2=-(kappa_STF/5)I4_D2",
            "source_status": "SYMBOLIC_SOURCE_READY_NONCLAIM",
            "needed_numeric_inputs": "kappa_STF; c_ext; signed s_K2; live K_L->K_hat adoption; DeltaK_TF bound",
            "parent_adoption_required": True,
            "valid_for_claim": False,
        },
        {
            "input_id": "M2I4486_1_surface_amplitude_candidate",
            "quantity": "A_surface_K2_projected_candidate",
            "formula": "A_surface_K2^proj=s_K2*C_K2_unit*(4/25)*kappa_STF*c_ext",
            "derivation": "4485 signed source-moment branch with 3180 projected Hessian moment inserted",
            "source_status": "SYMBOLIC_TRANSFER_ROW_NONCLAIM",
            "needed_numeric_inputs": "C_K2_unit already owned; s_K2; kappa_STF; c_ext; source-domain transfer; leakage/readout/boundary safety",
            "parent_adoption_required": True,
            "valid_for_claim": False,
        },
        {
            "input_id": "M2I4486_2_product_bound_carry",
            "quantity": "s_K2_M2_K2_product_bound",
            "formula": f"|s_K2*M2_K2| <= {product_bound:.15e}",
            "derivation": "4485 carries the tight local product-bound row from 3170/3177",
            "source_status": "BOUND_CARRIED_NONCLAIM",
            "needed_numeric_inputs": "source-backed s_K2 or M2_K2",
            "parent_adoption_required": True,
            "valid_for_claim": False,
        },
        {
            "input_id": "M2I4486_3_recast_hessian_product_bound",
            "quantity": "s_K2_kappa_STF_c_ext_bound",
            "formula": f"|s_K2*kappa_STF*c_ext| <= {recast_bound:.15e}",
            "derivation": "3180 substitutes M2_K2^proj=(4/25)kappa_STF*c_ext into |s_K2*M2_K2| <= B_product",
            "source_status": "FIRST_FINITE_SCORER_INPUT_NONCLAIM",
            "needed_numeric_inputs": "one of s_K2, kappa_STF or c_ext plus bounds on the others; DeltaK_TF leakage bound",
            "parent_adoption_required": True,
            "valid_for_claim": False,
        },
    ]


def deltak_tf_rows() -> List[Dict[str, object]]:
    return [
        {
            "leak_id": "DTF4486_0_definition",
            "quantity": "DeltaK_TF",
            "definition": "DeltaK_TF^{ij}:=K_L^{<ij>}-P_Y[K_L]^{ij}",
            "derived_condition": "DeltaK_TF=0 only if the parent projects out all non-Y_a tensor harmonics or the Hessian carrier is metric-null",
            "current_status": "MISSING_ZERO_OR_BOUND",
            "needed_for": "promote projected M2_K2 branch from symbolic to testable",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DTF4486_1_Bprime_condition",
            "quantity": "K_perp_layer",
            "definition": "B(r):=(3/2)F(r)/r^2; non-pure tensor pieces are driven by B'(r)",
            "derived_condition": "pure Y_a Hessian branch requires B'(r)=0; compact core/exterior matching generally violates this",
            "current_status": "FINITE_LAYER_LEAKAGE_LIVE",
            "needed_for": "boundary or smooth profile leakage envelope",
            "valid_for_claim": False,
        },
        {
            "leak_id": "DTF4486_2_metric_response_bound",
            "quantity": "DeltaA_surface_TF",
            "definition": "DeltaA_surface_TF=P_surf,l2 G_EH[DeltaK_TF plus any induced boundary/readout terms]",
            "derived_condition": "local safety needs DeltaA_surface_TF=0 or a no-cancellation bound against J2/PPN/clock/orbital thresholds",
            "current_status": "BOUND_ROW_REQUIRED",
            "needed_for": "finite local comparator if Hessian carrier survives",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4486_0_inventory_identity",
            "finding": "K2 metric response is completely localized to four derivative channels",
            "reason": "differentiating the same-frame EH equation wrt sigma_K2 exposes Hilbert, residual, boundary and readout terms",
            "effect": "future work can no longer hide K2 as a metric amplitude without naming the derivative channel",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4486_1_zero_branch_status",
            "finding": "current owned K2 artifact is source-silent, but global parent-zero remains unsigned",
            "reason": "absence of current delta rows is enough to block fake amplitude, not enough to prove parent action exhaustion",
            "effect": "zero theorem remains a disciplined branch rather than an overclaim",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4486_2_first_finite_input",
            "finding": "first finite projected M2_K2 input row is now explicit",
            "reason": "3179/3180 derive M2_K2^proj=(4/25)kappa_STF c_ext and the recast product bound",
            "effect": "the next coupling hunt has an actual symbolic scorer instead of a vague missing coefficient",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4486_3_leakage_frontier",
            "finding": "DeltaK_TF is the live obstruction for the finite Hessian route",
            "reason": "projected moment can vanish or be bounded while full tensor-harmonic Hessian leakage survives",
            "effect": "next checkpoint should decide K_L metric-nullity/adoption or fill DeltaK_TF bound rows",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    inventory: List[Dict[str, object]],
    scorecard: List[Dict[str, object]],
    m2_rows: List[Dict[str, object]],
    leakage_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4486_0_sources",
            "gate": "all cited source paths and needles exist",
            "gate_pass": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "detail": "source hygiene only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4486_1_inventory_identity_written",
            "gate": "K2 source derivative inventory identity exists",
            "gate_pass": any(row.get("inventory_id") == "KDI4486_0_master_variation" for row in inventory),
            "claim_allowed": False,
            "detail": "derivation written, not a local-GR pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4486_2_current_artifact_zero_only",
            "gate": "current artifact source silence is separated from parent global zero",
            "gate_pass": any("CURRENT_ARTIFACT_SOURCE_SILENT" in str(row.get("proof_level")) for row in scorecard)
            and any("PARENT_GLOBAL_ZERO_UNSIGNED" in str(row.get("proof_level")) for row in scorecard),
            "claim_allowed": False,
            "detail": "prevents overclaiming absence of current rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4486_3_first_m2_input_row_exists",
            "gate": "projected Hessian M2_K2 input row exists",
            "gate_pass": any(row.get("input_id") == "M2I4486_0_projected_hessian_moment" for row in m2_rows),
            "claim_allowed": False,
            "detail": "symbolic source-ready row only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4486_4_deltak_tf_not_silenced",
            "gate": "DeltaK_TF remains explicit and unsilenced",
            "gate_pass": any(row.get("leak_id") == "DTF4486_0_definition" and "MISSING" in str(row.get("current_status")) for row in leakage_rows),
            "claim_allowed": False,
            "detail": "finite Hessian branch remains leakage-gated",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4486_5_no_generated_claim_rows",
            "gate": "all generated rows remain private nonclaim",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [sources, inventory, scorecard, m2_rows, leakage_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "no local-GR, J2, PPN, R10, clock, orbital or EM claim is promoted",
            "valid_for_claim": False,
        },
    ]
