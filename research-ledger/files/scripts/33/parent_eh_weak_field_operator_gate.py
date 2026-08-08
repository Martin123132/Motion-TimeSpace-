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


def eh_weak_field_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "EHW4484_0_selector_to_metric_equation",
            "object": "conditional_EH_public_metric_equation",
            "derivation": "Use the existing Lovelock/Palatini selector chain: if the observed branch is same-coframe, local, four-dimensional, diffeomorphism invariant, metric/coframe-only after constraints, second order through 2PN, and same-source, the left-hand equation is EH plus explicit residuals.",
            "formula": "G_munu[g_obs]+Lambda_eff g_munu = kappa_eff T_H_munu + E_res_munu",
            "result": "The EH weak-field operator is conditionally available as a theorem chain, not as an unconditional parent signature.",
            "status": "CONDITIONAL_EH_OPERATOR_AVAILABLE_WITH_RESIDUALS",
            "valid_for_claim": False,
        },
        {
            "row_id": "EHW4484_1_linearized_operator",
            "object": "linearized_EH_operator",
            "derivation": "Linearize g_obs=eta+h about the local asymptotically flat exterior branch and impose harmonic gauge on the trace-reversed perturbation.",
            "formula": "partial^mu hbar_munu=0; Box hbar_munu = -2 kappa_eff T_H_munu - 2 E_res_munu",
            "result": "Every non-EH or MTS extra contribution is a right-hand residual/source for the public metric equation, not a hidden change of the operator.",
            "status": "DERIVED_CONDITIONAL_LINEARIZED_EH_OPERATOR",
            "valid_for_claim": False,
        },
        {
            "row_id": "EHW4484_2_static_exterior_l2",
            "object": "exterior_l2_metric_operator",
            "derivation": "Outside compact Hilbert source, outside retained residual support, and after boundary silence, the static equation becomes source-free.",
            "formula": "nabla^2 hbar_munu^ext = 0; P_l2 gives r^2 R_2''+2r R_2'-6R_2=0",
            "result": "The 4483 r^-3 Green theorem is inherited by the EH branch exactly under these support/silence conditions.",
            "status": "CONDITIONAL_MATCH_TO_4483_PUBLIC_GREEN_OPERATOR",
            "valid_for_claim": False,
        },
        {
            "row_id": "EHW4484_3_metric_readout_identity",
            "object": "E_metric_on_EH_branch",
            "derivation": "If the observed coframe/metric is the one varied in S_EH and the same one used by matter, clocks, EM and PPN readouts, the parent-to-public metric readout is identity on g_obs perturbations.",
            "formula": "delta g_public = delta g_obs + delta g_readout_extra",
            "result": "E_metric=I only on the same-coframe branch and only if delta g_readout_extra=0 or bounded.",
            "status": "CONDITIONAL_IDENTITY_READOUT_WITH_REACTIVATION_GUARD",
            "valid_for_claim": False,
        },
        {
            "row_id": "EHW4484_4_K2_source_fork",
            "object": "K2_lane_in_EH_equation",
            "derivation": "Differentiate the conditional EH/residual equation with respect to sigma_K2=K2*C_K2_unit.",
            "formula": "partial_sigma G_munu[g_obs] = kappa_eff partial_sigma T_H_munu + partial_sigma E_res_munu",
            "result": "If K2 is not in T_H, E_res, boundary data or readout, the public metric response is zero; if it is present, Pi_J2_metric is an EH Green functional of that sourced l=2 content.",
            "status": "ZERO_OR_SOURCE_FUNCTIONAL_FORK_DERIVED",
            "valid_for_claim": False,
        },
        {
            "row_id": "EHW4484_5_verdict",
            "object": "parent_EH_operator_signature",
            "derivation": "Combine 4086/4278 with 4483 and 3173.",
            "formula": "operator_match_l2 closes only on the conditional EH branch; Pi_J2_metric closes only after partial_sigma(T_H,E_res,boundary,readout) is known",
            "result": "4484 promotes the operator part to a conditional theorem and narrows Pi_J2_metric to a zero-or-sourced functional, but does not claim local GR.",
            "status": "OPERATOR_CONDITIONALLY_DERIVED_PIJ2_SOURCE_OWNER_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def pij2_transfer_rows(c_k2_unit: float, two_epsilon: float, half_bound: float) -> List[Dict[str, object]]:
    return [
        {
            "transfer_id": "PI4484_0_sigma_definition",
            "quantity": "sigma_K2",
            "branch": "shared",
            "formula": f"sigma_K2 = K2*C_K2_unit = K2*{c_k2_unit:.15e}",
            "meaning": "The finite l=2 lane amplitude that may or may not enter the parent EH/residual equation.",
            "required_owner": "parent source/boundary/readout variation with respect to sigma_K2",
            "status": "DEFINED_AS_LANE_NOT_SOURCE",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "PI4484_1_clean_EH_silent_branch",
            "quantity": "Pi_J2_metric_zero",
            "branch": "K2_source_silent",
            "formula": "partial_sigma T_H_munu = partial_sigma E_res_munu = partial_sigma B_l2 = partial_sigma g_readout_extra = 0 => A_surface_K2 = 0",
            "meaning": "On the strict same-source EH branch, an internal K2 bookkeeping lane that never enters the variational equation produces no public J2 metric amplitude.",
            "required_owner": "prove K2 source silence in Hilbert stress, residual tensor, boundary data and readout",
            "status": "CONDITIONAL_ZERO_THEOREM_AVAILABLE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "PI4484_2_finite_source_functional",
            "quantity": "Pi_J2_metric_source",
            "branch": "K2_sources_public_metric",
            "formula": "A_surface_K2 = P_surf,l2 G_EH[ kappa_eff deltaT_H_K2 + deltaE_res_K2 + deltaB_l2 + deltaReadout_l2 ]",
            "meaning": "If K2 survives as a real source/residual, its public quadrupole amplitude is not a free constant; it is the EH Green projection of the sourced tracefree l=2 content.",
            "required_owner": "deltaT_H_K2, deltaE_res_K2, boundary l2 data, readout l2 data and same radius/coframe normalization",
            "status": "EXACT_FUNCTIONAL_FORM_AVAILABLE_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "PI4484_3_Upsilon_factorization",
            "quantity": "Upsilon_J2",
            "branch": "finite_source",
            "formula": "Upsilon_J2 = Pi_J2_metric*T_source*G_ext_l2_surface = A_surface_K2/(K2*C_K2_unit)",
            "meaning": "At rho=1, the 4483 Green factor is one after A_surface is owned; the remaining transfer is source/projection ownership.",
            "required_owner": "nonzero A_surface_K2 or a signed zero theorem",
            "status": "FACTOR_REDUCED_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "PI4484_4_J2_pressure_row",
            "quantity": "K2_bound_half_range",
            "branch": "finite_source",
            "formula": f"K2 <= {half_bound:.15e}/|Pi_J2_metric*T_source*G_ext_l2_surface|",
            "meaning": "The previous J2 pressure row remains usable only after the transfer functional has a source-backed value or bound.",
            "required_owner": f"A_surface_K2 compared with 2 epsilon J2 using two_epsilon={two_epsilon:.15e}",
            "status": "CONDITIONAL_PRESSURE_ROW_NO_CLAIM",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "PI4484_5_no_identity_shortcut",
            "quantity": "Pi_J2_metric_not_one_by_default",
            "branch": "guardrail",
            "formula": "Pi_J2_metric=1 is allowed only if P_surf,l2 G_EH[...] = K2*C_K2_unit in the same solar/coframe/radius convention",
            "meaning": "The EH operator being correct does not normalize the K2 lane into a unit public metric source.",
            "required_owner": "explicit equality proof or measured/source-backed transfer row",
            "status": "IDENTITY_SHORTCUT_REJECTED",
            "valid_for_claim": False,
        },
    ]


def k2_source_owner_rows() -> List[Dict[str, object]]:
    return [
        {
            "owner_id": "KSO4484_0_Hilbert_source_derivative",
            "object": "deltaT_H_K2",
            "definition": "Hilbert/coframe stress response of the same-frame matter/EM/source action to sigma_K2",
            "zero_condition": "partial_sigma T_H_munu = 0",
            "finite_condition": "source-backed tracefree l=2 stress derivative exists with units and support",
            "needed_for": "decide whether K2 is source-silent or finite-sourced",
            "status": "MISSING_PARENT_SOURCE_DERIVATIVE",
            "valid_for_claim": False,
        },
        {
            "owner_id": "KSO4484_1_residual_equation_derivative",
            "object": "deltaE_res_K2",
            "definition": "extra MTS local field-equation residual response to sigma_K2 after EH baseline subtraction",
            "zero_condition": "partial_sigma E_res_munu = 0",
            "finite_condition": "operator coefficients and l=2 projection are sourced and bounded",
            "needed_for": "finite Pi_J2_metric functional or residual-l2 scorer",
            "status": "MISSING_RESIDUAL_DERIVATIVE",
            "valid_for_claim": False,
        },
        {
            "owner_id": "KSO4484_2_boundary_l2_derivative",
            "object": "deltaB_l2_K2",
            "definition": "l=2 boundary or matching-data response of the parent exterior problem to sigma_K2",
            "zero_condition": "fixed/asymptotically flat/no-flux boundary data independent of sigma_K2",
            "finite_condition": "boundary l=2 amplitude and radius normalization are source-backed",
            "needed_for": "exclude hidden growing/incoming/tidal l=2 pieces",
            "status": "MISSING_BOUNDARY_DERIVATIVE",
            "valid_for_claim": False,
        },
        {
            "owner_id": "KSO4484_3_readout_l2_derivative",
            "object": "deltaReadout_l2_K2",
            "definition": "public metric/readout deformation response to sigma_K2 not already in g_obs",
            "zero_condition": "same observed metric readout with no K2-dependent shadow/disformal term",
            "finite_condition": "readout l=2 projector coefficient is source-backed and bounded",
            "needed_for": "prevent Pi_J2_metric from being hidden in the observer map",
            "status": "MISSING_READOUT_DERIVATIVE",
            "valid_for_claim": False,
        },
        {
            "owner_id": "KSO4484_4_source_domain_transfer",
            "object": "T_source",
            "definition": "solar-domain construction or universality map for sigma_K2",
            "zero_condition": "the local K2 lane is not a solar exterior source variable",
            "finite_condition": "direct solar K2 construction or source-domain theorem",
            "needed_for": "use solar J2/Shapiro/orbital bounds against K2",
            "status": "MISSING_SOLAR_SOURCE_DOMAIN_TRANSFER",
            "valid_for_claim": False,
        },
        {
            "owner_id": "KSO4484_5_verdict",
            "object": "K2_metric_source_status",
            "definition": "all four derivative channels plus source-domain transfer decide Pi_J2_metric",
            "zero_condition": "KSO4484_0 through KSO4484_4 all sign the zero/silent branch",
            "finite_condition": "at least one finite derivative channel has a source-backed amplitude and no-cancellation scorer",
            "needed_for": "local-GR/J2/PPN claim gate",
            "status": "ZERO_OR_FINITE_SOURCE_NOT_DECIDED",
            "valid_for_claim": False,
        },
    ]


def residual_interface_rows() -> List[Dict[str, object]]:
    return [
        {
            "interface_id": "RIF4484_0_master_equation",
            "residual": "DeltaE_nonEH_plus_K2",
            "formula": "DeltaE_total = E_res + kappa_eff deltaT_H_K2 + deltaB_l2 + deltaReadout_l2",
            "projection": "P_surf,l2 G_EH[DeltaE_total]",
            "test_route": "J2/Shapiro/PPN/clock/orbital residual-l2 scorer",
            "status": "SYMBOLIC_INTERFACE_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "interface_id": "RIF4484_1_gamma_beta",
            "residual": "tracefree_spatial_and_2PN_00",
            "formula": "delta_gamma, delta_beta = Pi_PPN[DeltaE_total]",
            "projection": "use 4086 nonEH PPN projection formulas",
            "test_route": "Cassini/gamma, beta, preferred-frame and conservation gates",
            "status": "BOUND_ROUTE_IMPORTED_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "interface_id": "RIF4484_2_local_R10_tail",
            "residual": "finite_range_or_unscreened_tail",
            "formula": "alpha_X(lambda_X) only if a non-EH/K2 mode has q_X != 0 and finite range",
            "projection": "R10 alpha(lambda) runner after source charges exist",
            "test_route": "R10/WEP/fifth-force",
            "status": "ROUTE_RETAINED_IF_MODE_SURVIVES",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    eh_rows: List[Dict[str, object]],
    pi_rows: List[Dict[str, object]],
    owner_rows: List[Dict[str, object]],
    residual_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4484_0_sources",
            "gate": "all cited source paths and needles exist",
            "gate_pass": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "detail": "source hygiene only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4484_1_EH_operator_conditional",
            "gate": "EH weak-field exterior operator is derived conditionally",
            "gate_pass": any(row.get("row_id") == "EHW4484_2_static_exterior_l2" for row in eh_rows),
            "claim_allowed": False,
            "detail": "conditional on selector, same coframe, residual silence and boundary support",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4484_2_parent_signature_unconditional",
            "gate": "full MTS parent signs the EH selector premises",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "existing evidence is a conditional chain, not a fully parent-signed local-GR theorem",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4484_3_PiJ2_identity",
            "gate": "Pi_J2_metric equals one or any numeric value",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "identity shortcut rejected; exact source functional written but inputs are missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4484_4_K2_zero_or_source_decided",
            "gate": "K2 is proven source-silent or given a sourced finite quadrupole amplitude",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "deltaT_H_K2, deltaE_res_K2, boundary/readout and T_source remain missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4484_5_no_generated_claim_rows",
            "gate": "generated rows remain private nonclaim",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [sources, eh_rows, pi_rows, owner_rows, residual_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "no local-GR, J2, PPN, R10, clock, orbital or EM claim is promoted",
            "valid_for_claim": False,
        },
    ]
