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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def marker_bulk_zero_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "LMB4475_0_coefficient_definition",
            "clause": "lambda_M is the action coefficient of a physical marker monomial",
            "formal_statement": "Delta S_M = int sqrt(-g) lambda_M F_M(M_cell) O_marker[Phi]; lambda_M = Pi_{F_M O_marker}(S_bulk)",
            "derivation": "A coupling is not a mood or a readout preference; it is the coefficient obtained by projecting the parent bulk action onto a marker-containing local operator.",
            "zero_result": "if S_bulk has no marker-containing operator, Pi_{F_M O_marker}(S_bulk)=0 and lambda_M=0",
            "current_status": "DEFINITION_AND_PROJECTION_LAW_DERIVED",
            "parent_signed": True,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LMB4475_1_external_readout_zero",
            "clause": "external readout cannot generate lambda_M",
            "formal_statement": "S_total=S_bulk[Phi]+S_boundary[Phi]+int J O_read[Phi;R_obs], with J=0 before variation",
            "derivation": "Under the 4474 split, R_obs is outside the bulk action algebra. Since lambda_M is the projection of S_bulk onto a marker monomial, the projection is identically zero.",
            "zero_result": "lambda_M=0 on the external-readout/source-at-zero branch",
            "current_status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LMB4475_2_source_at_zero_firewall",
            "clause": "diagnostic source terms vanish only if the source is truly set to zero",
            "formal_statement": "Delta S_J=int J O_read; lambda_M[J] proportional to J gives lambda_M[0]=0",
            "derivation": "A finite diagnostic source is a physical source extension. A source-at-zero insertion can define correlation/readout derivatives but cannot alter the physical local equations at J=0.",
            "zero_result": "no finite lambda_M may be inferred from a diagnostic source unless J is retained physically and then bounded",
            "current_status": "DERIVED_WITH_FINITE_J_COUNTERROUTE",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LMB4475_3_no_spurion_or_labelled_marker",
            "clause": "active-cell labels and material markers are forbidden on the zero branch",
            "formal_statement": "R_obs not in Phi_parent, not a spurion/background, not a labelled species vector, and not a source-measure multiplier",
            "derivation": "A covariant marker can transform correctly and still be physical. The zero theorem therefore requires absence from the parent action grammar, not only covariance.",
            "zero_result": "no active-label or species coupling contributes to lambda_M",
            "current_status": "CONDITIONAL_NO_SPURION_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LMB4475_4_no_auxiliary_generation",
            "clause": "integrated-out marker auxiliaries are not silently allowed",
            "formal_statement": "no hidden M_aux with B_M^T L_M^-1 B_M projection into F_M O_marker",
            "derivation": "Even if no explicit marker term is written, an integrated-out physical marker sector can regenerate the same operator. The zero theorem requires no hidden auxiliary source.",
            "zero_result": "lambda_M_aux=0 and c_marker_aux=0 only if the auxiliary marker sector is absent or parent-signed silent",
            "current_status": "AUXILIARY_COUNTERROUTE_RETAINED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LMB4475_5_boundary_not_bulk",
            "clause": "boundary marker terms do not count as bulk zero unless routed",
            "formal_statement": "Pi_loc(delta S_boundary/delta R_obs)=0, or boundary_marker is a finite row outside lambda_M_bulk",
            "derivation": "The bulk theorem does not erase boundary/interface matching. A boundary marker can feed local tests without being a bulk lambda_M term.",
            "zero_result": "lambda_M_bulk=0 does not imply boundary_marker=0",
            "current_status": "BOUNDARY_FIREWALL_RETAINED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LMB4475_6_finite_branch_law",
            "clause": "if any marker monomial exists, lambda_M becomes the first finite source row",
            "formal_statement": "if Delta S_M exists, declare O_marker, F_M, lambda_M, support, normalization, sign, units and source path",
            "derivation": "The finite branch is now reduced to one first coefficient: either the parent grammar forbids the marker monomial, or lambda_M must be sourced before c_R2_marker/C_marker can be scored.",
            "zero_result": "no cancellation with other channels is allowed; lambda_M is judged componentwise",
            "current_status": "DERIVED_ACCOUNTING_LAW",
            "parent_signed": True,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LMB4475_7_verdict",
            "clause": "lambda_M zero theorem is exact but parent-conditional",
            "formal_statement": "lambda_M=0 iff the marker-containing bulk operator is absent from S_bulk and no finite J/spurion/auxiliary/boundary route substitutes for it",
            "derivation": "This moves the coupling problem from vague missingness to an action-algebra test. Current MTS has not yet parent-signed the action inventory, so local-GR/R10 claims stay blocked.",
            "zero_result": "conditional lambda_M=0 theorem written; finite lambda_M source row staged",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def lambda_operator_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "LOA4475_0_bulk_marker_monomial",
            "operator_slot": "F_M(M_cell) O_marker in S_bulk",
            "zero_test": "no parent local monomial contains M_cell, R_obs as spurion, active-cell label, or material marker",
            "if_zero": "lambda_M_bulk=0",
            "if_failed": "fill lambda_M finite row",
            "current_status": "PARENT_ACTION_INVENTORY_UNSIGNED",
            "arena_map": "R10;PPN;local_GR",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOA4475_1_diagnostic_source",
            "operator_slot": "J O_read[Phi;R_obs]",
            "zero_test": "J is set to zero before physical variation and never fitted as a material source",
            "if_zero": "lambda_M[J=0]=0",
            "if_failed": "finite J becomes a source extension",
            "current_status": "SOURCE_AT_ZERO_USAGE_UNSIGNED",
            "arena_map": "all_local_arenas",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOA4475_2_spurion_background",
            "operator_slot": "fixed P_active, R_obs, or marker background",
            "zero_test": "no background value selects a cell, source sector, species label, or primitive grain",
            "if_zero": "no spurion-generated lambda_M",
            "if_failed": "lambda_M_spurion must be bounded",
            "current_status": "NO_SPURION_UNSIGNED",
            "arena_map": "R10;WEP;PPN;clock",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOA4475_3_auxiliary_marker_sector",
            "operator_slot": "hidden auxiliary marker with B_M,L_M",
            "zero_test": "no integrated-out marker field projects into the same local operator",
            "if_zero": "lambda_M_aux=0",
            "if_failed": "fill B_M,L_M,c_marker_bare row",
            "current_status": "AUXILIARY_SILENCE_UNSIGNED",
            "arena_map": "R10;PPN",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOA4475_4_boundary_interface",
            "operator_slot": "boundary/reference marker",
            "zero_test": "boundary/reference is fixed, topological, no-flux or Hamiltonian-routed under local compact variations",
            "if_zero": "boundary_marker=0 in local response",
            "if_failed": "fill boundary_marker not lambda_M_bulk",
            "current_status": "BOUNDARY_SILENCE_UNSIGNED",
            "arena_map": "local_GR;clock;orbital",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LOA4475_5_componentwise_guard",
            "operator_slot": "lambda_M cancellation with other channels",
            "zero_test": "each marker component is zero or source-bounded separately",
            "if_zero": "R_marker_abs can drop lambda_M contribution",
            "if_failed": "no sign cancellation credit",
            "current_status": "NO_CANCELLATION_GUARD_ACTIVE",
            "arena_map": "claim_gate_guard",
            "valid_for_claim": False,
        },
    ]


def lambda_source_row_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "LMR4475_0_zero_certificate",
            "quantity": "Z_lambda_M",
            "definition": "certificate that marker bulk coupling is absent from the parent bulk action",
            "formula_or_test": "Z_lambda_M=True iff Pi_{F_M O_marker}(S_bulk)=0 and no finite J/spurion/auxiliary substitute exists",
            "needed_inputs": "parent action inventory; field list; external-readout/source-at-zero signature; auxiliary silence",
            "current_value": "MISSING_PARENT_ZERO_CERTIFICATE",
            "units": "boolean_certificate",
            "arena_map": "local_GR;R10;PPN",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "LMR4475_1_lambda_M",
            "quantity": "lambda_M",
            "definition": "bulk coupling of marker to the first local marker operator",
            "formula_or_test": "Delta S_M = int sqrt(-g) lambda_M F_M(M_cell) O_marker",
            "needed_inputs": "operator definition; normalization; sign; dimensionality; parent source path",
            "current_value": "MISSING_LAMBDA_M_NUMERIC_OR_ZERO",
            "units": "operator_dimension_dependent",
            "arena_map": "c_R2_eff;C_total;R10;PPN",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "LMR4475_2_O_marker",
            "quantity": "O_marker",
            "definition": "local curvature/source/grain operator coupled to the marker",
            "formula_or_test": "O_marker in {R, R^2, Ricci^2, Weyl^2, source density, Z_H, Gamma_eff, K_hat, boundary projection, other declared}",
            "needed_inputs": "basis choice; derivative order; covariance; local support",
            "current_value": "MISSING_MARKER_OPERATOR_BASIS",
            "units": "operator_units",
            "arena_map": "R10;PPN;source_coupling",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "LMR4475_3_F_M",
            "quantity": "F_M(M_cell)",
            "definition": "marker profile/selection functional",
            "formula_or_test": "profile must be external-readout zero, compact support, boundary-routed, or physical material profile",
            "needed_inputs": "support; normalization; transformation law; whether varied",
            "current_value": "MISSING_MARKER_PROFILE",
            "units": "profile_units",
            "arena_map": "local_GR;R10;clock;orbital",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "LMR4475_4_N_M",
            "quantity": "N_M",
            "definition": "normalization converting lambda_M O_marker into canonical residual rows",
            "formula_or_test": "lambda_M^canon = lambda_M/N_M or declared equivalent",
            "needed_inputs": "EH normalization; source measure; units; sign convention",
            "current_value": "MISSING_MARKER_NORMALIZATION",
            "units": "normalization_units",
            "arena_map": "c_R2_marker;C_marker;T_marker",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "LMR4475_5_projection_targets",
            "quantity": "Pi_local(lambda_M)",
            "definition": "projection of marker coupling into local observable residuals",
            "formula_or_test": "lambda_M -> {c_R2_marker, C_marker, T_marker/J_marker, boundary_marker}",
            "needed_inputs": "projection map; arena; no-cancellation envelope",
            "current_value": "MISSING_LAMBDAM_PROJECTION_MAP",
            "units": "declared_by_target",
            "arena_map": "R10;WEP;PPN;clock;orbital",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4475_0_lambdaM_is_action_projection",
            "finding": "lambda_M is now defined as a parent-action projection coefficient, not an undefined coupling vibe",
            "consequence": "zero proof reduces to absence of marker monomials in S_bulk plus finite-source/auxiliary/boundary firewalls",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4475_1_zero_theorem_conditional",
            "finding": "external readout/source-at-zero implies lambda_M=0 exactly, but only if the parent readout role is signed",
            "consequence": "the route toward local GR is sharper but still parent-conditional",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4475_2_next_component",
            "finding": "if lambda_M is not parent-zero, the next non-handwavy job is the projection map into c_R2_marker and C_marker",
            "consequence": "the next target should either sign the action inventory or derive the first projection from lambda_M to local residuals",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    audit_rows: List[Dict[str, object]],
    source_row_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    theorem_written = any(row.get("theorem_id") == "LMB4475_7_verdict" for row in theorem_rows)
    projection_law = any(row.get("theorem_id") == "LMB4475_0_coefficient_definition" and row.get("parent_signed") is True for row in theorem_rows)
    parent_zero_signed = any(row.get("theorem_id") == "LMB4475_7_verdict" and row.get("parent_signed") is True for row in theorem_rows)
    finite_rows_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("status") != "BLOCKED_SOURCE_READY"
        for row in source_row_rows
    )
    audit_has_open_parent_clauses = any("UNSIGNED" in str(row.get("current_status")) for row in audit_rows)
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, theorem_rows, audit_rows, source_row_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4475_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4474 lambda_M target, 4473 marker rows, and earlier source-at-zero forks",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4475_1_projection_law_written",
            "claim": "lambda_M is defined as a parent-action projection coefficient",
            "gate_pass": theorem_written and projection_law,
            "claim_allowed": False,
            "detail": "this is a useful definition, not a local-GR claim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4475_2_parent_zero_signed",
            "claim": "MTS parent proves lambda_M=0",
            "gate_pass": parent_zero_signed,
            "claim_allowed": False,
            "detail": "parent action inventory/readout role/auxiliary silence remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4475_3_operator_audit_blocks_claim",
            "claim": "no marker operator slots remain open",
            "gate_pass": not audit_has_open_parent_clauses,
            "claim_allowed": False,
            "detail": "operator audit keeps bulk, source, spurion, auxiliary and boundary clauses live",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4475_4_lambda_source_row_claim_ready",
            "claim": "finite lambda_M branch is source/numeric ready",
            "gate_pass": finite_rows_ready,
            "claim_allowed": False,
            "detail": "lambda_M source rows are explicit but still missing parent values or zero certificate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4475_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4475 is a conditional zero theorem plus first finite coupling intake",
            "valid_for_claim": False,
        },
    ]
