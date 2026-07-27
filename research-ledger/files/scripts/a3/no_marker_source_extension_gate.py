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


def no_marker_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "NME4473_0_parent_field_absence",
            "required_clause": "no parent field, spurion, material marker, active-cell label, boundary defect, or source carrier M_cell exists in the bulk field inventory",
            "formal_test": "M_cell not in Phi_parent; no term S_bulk[g,e,omega,...,M_cell]; no fixed P_active background; no labelled-species component survives quotienting",
            "derivation_attempt": "If the marker is absent from the parent field inventory, it cannot carry ell_cell or c_R2_cell as a physical bulk datum.",
            "current_evidence": "NOT_PARENT_SIGNED",
            "parent_signed": False,
            "if_signed": "marker/source extension route closes at the field-inventory level",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NME4473_1_external_readout_exception",
            "required_clause": "relational/source readout is external dressing only, not a material marker",
            "formal_test": "readout mask R_obs appears only in O_read[Phi;R_obs], not in S_bulk, and delta S_bulk/delta R_obs = 0",
            "derivation_attempt": "340/341 allow relational readout if the reference transforms with the state; this is safe only when the reference has no variational backreaction.",
            "current_evidence": "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "parent_signed": False,
            "if_signed": "observer/source-at-zero readout can be gauge-compatible without reopening c_R2_cell",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NME4473_2_bulk_variational_silence",
            "required_clause": "marker/source dressing has no Hilbert stress, no coframe source, no connection source and no scalar curvature-linear vertex",
            "formal_test": "delta S/delta g|marker = 0, delta S/delta e|marker = 0, delta S/delta omega|marker = 0, and d^2S/(dM_cell dR)=0",
            "derivation_attempt": "If the marker varies in the bulk action, it is a source, not a gauge readout; it can generate c_R2_eff or C_total after elimination.",
            "current_evidence": "OPEN_VARIATIONAL_BACKREACTION_CLAUSE",
            "parent_signed": False,
            "if_signed": "marker cannot contribute to stress, source coupling, c_R2_eff, C_total or PPN/R10 residuals",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NME4473_3_boundary_reference_silence",
            "required_clause": "boundary/reference marker is topological, fixed, no-flux, or Hamiltonian-routed with no local bulk residue",
            "formal_test": "all boundary marker variations either vanish under local compact support, become fixed charges, or are routed outside local PPN/R10 response",
            "derivation_attempt": "A relational boundary reference is safe only if it does not backreact into the local bulk field equations or source-normalization map.",
            "current_evidence": "BOUNDARY_NO_BACKREACTION_UNSIGNED",
            "parent_signed": False,
            "if_signed": "boundary/reference readout cannot reintroduce primitive grain data",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NME4473_4_labelled_species_exclusion",
            "required_clause": "cells are not labelled physical species or material subchannels",
            "formal_test": "the parent variable is an orbit/multiset/spectrum/basis-free fibre object rather than a 27-component species vector",
            "derivation_attempt": "340/341 show the same symmetric formula can describe either quotient gauge labels or physical labelled species; the parent variable definition must decide.",
            "current_evidence": "QUOTIENT_TEMPLATE_EXISTS_SPECIES_EXCLUSION_UNSIGNED",
            "parent_signed": False,
            "if_signed": "cell labels cannot become physical source channels after gauge fixing",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NME4473_5_marker_residual_law",
            "required_clause": "if any marker/source extension remains, it is represented by finite residual coefficients rather than silently treated as gauge",
            "formal_test": "c_R2_marker, C_marker, beta_marker, ell_marker, q_marker and boundary/source rows are declared with units and source paths",
            "derivation_attempt": "A covariant marker can descend to an extended quotient and still carry physical data; such a branch must be bounded, not erased.",
            "current_evidence": "DERIVED_ACCOUNTING_LAW",
            "parent_signed": True,
            "if_signed": "fallback branch becomes testable without granting local-GR credit",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NME4473_6_verdict",
            "required_clause": "NME4473_0 through NME4473_4 sign together, or NME4473_5 finite residual branch is used",
            "formal_test": "no-marker theorem is valid only if field absence, external readout, variational silence, boundary silence and species exclusion all hold",
            "derivation_attempt": "The exact no-marker theorem is now written, but current MTS has not parent-signed the field-inventory and no-backreaction clauses.",
            "current_evidence": "NO_MARKER_THEOREM_CONDITIONAL_PARENT_UNSIGNED",
            "parent_signed": False,
            "if_signed": "marker/source extension cannot carry ell_cell; otherwise finite marker residual rows remain mandatory",
            "valid_for_claim": False,
        },
    ]


def marker_residual_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "MR4473_0_marker_existence",
            "quantity": "M_cell",
            "definition": "physical marker/source/boundary variable that can select active cell, primitive grain, or relational reference data",
            "formula_or_test": "M_cell absent from parent bulk action for zero theorem; if present, declare field type and support",
            "needed_inputs": "parent field inventory; support; source path; bulk/boundary classification",
            "current_value": "MISSING_PARENT_FIELD_INVENTORY_CERTIFICATE",
            "units": "field_or_boolean_certificate",
            "arena_map": "local_GR;R10;PPN;clock;orbital;WEP",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MR4473_1_marker_bulk_coupling",
            "quantity": "lambda_M",
            "definition": "bulk coupling of marker to local curvature/source/grain operator",
            "formula_or_test": "Delta S_M contains lambda_M F_M(M_cell) O_grain or zero by theorem",
            "needed_inputs": "operator O_grain; normalization; sign; source path; no-cancellation guard",
            "current_value": "MISSING_MARKER_BULK_COUPLING",
            "units": "declared_by_operator_dimension",
            "arena_map": "c_R2_eff;C_total;R10;PPN",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MR4473_2_marker_length",
            "quantity": "ell_marker",
            "definition": "physical marker/grain length if marker carries primitive cell scale",
            "formula_or_test": "ell_marker must be parent-sourced, not Planck/measured-G/fitted-range by declaration",
            "needed_inputs": "non-circular length source; uncertainty; support; units",
            "current_value": "MISSING_NONCIRCULAR_MARKER_LENGTH",
            "units": "meters",
            "arena_map": "c_R2_marker;R10_lambda;PPN_range",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MR4473_3_marker_cR2",
            "quantity": "c_R2_marker",
            "definition": "curvature-square coefficient induced by marker/grain extension",
            "formula_or_test": "c_R2_marker = zeta_M*lambda_M*ell_marker^2/N_EH + c_marker_bare + 0.5*B_M^T*L_M^-1*B_M",
            "needed_inputs": "lambda_M; ell_marker; zeta_M; N_EH; c_marker_bare; B_M; L_M; source paths",
            "current_value": "MISSING_MARKER_CR2_COMPONENTS",
            "units": "length_squared_after_EH_normalization",
            "arena_map": "R10_alpha_lambda;PPN_gamma_beta;R11",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MR4473_4_marker_source_coupling",
            "quantity": "C_marker",
            "definition": "marker contribution to common-mode or source-label coupling",
            "formula_or_test": "C_total = C_explicit_Achi + C_metric_pole + C_hidden_source + C_marker",
            "needed_inputs": "marker source charge; matter-frame normalization; screening/body-charge branch; source path",
            "current_value": "MISSING_MARKER_SOURCE_COUPLING",
            "units": "dimensionless",
            "arena_map": "R10_alpha;WEP;PPN;clock;orbital",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MR4473_5_variational_backreaction",
            "quantity": "T_marker_or_J_marker",
            "definition": "stress/source current generated by marker variation",
            "formula_or_test": "T_marker^{mu nu}=(-2/sqrt(-g)) delta S_marker/delta g_{mu nu}; J_marker=delta S_marker/delta M_cell",
            "needed_inputs": "S_marker; variation convention; support; boundary routing; source path",
            "current_value": "MISSING_MARKER_VARIATION",
            "units": "stress_or_source_units",
            "arena_map": "local_GR;Newton_source;EM_stress;PPN",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MR4473_6_no_cancellation_guard",
            "quantity": "marker_residual_norm",
            "definition": "absolute marker residual envelope; no sign cancellation with other channels",
            "formula_or_test": "R_marker_abs = abs(c_R2_marker)+abs(C_marker)+abs(T_marker_projection)+abs(boundary_marker)",
            "needed_inputs": "all marker components individually zero or source-bounded",
            "current_value": "MISSING_MARKER_COMPONENT_VALUES",
            "units": "mixed_declared_components",
            "arena_map": "claim_gate_guard",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def readout_classification_rows() -> List[Dict[str, object]]:
    return [
        {
            "class_id": "RC4473_0_external_observer_readout",
            "readout_type": "external observer/source-at-zero dressing",
            "bulk_action_slot": "absent",
            "variation_status": "delta S_bulk/delta R_obs=0",
            "effect": "safe conditional readout; no marker c_R2 or source coupling",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "class_id": "RC4473_1_relational_boundary_reference",
            "readout_type": "boundary/reference mask transforming with state",
            "bulk_action_slot": "allowed only if boundary/topological/Hamiltonian-routed",
            "variation_status": "local compact-support variation must vanish",
            "effect": "safe only with no-flux/no-backreaction theorem",
            "current_status": "BOUNDARY_SILENCE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "class_id": "RC4473_2_material_marker",
            "readout_type": "physical material marker or active-cell spurion",
            "bulk_action_slot": "present or potentially present",
            "variation_status": "can produce stress/source/current",
            "effect": "finite marker residual row required",
            "current_status": "COUNTERMODEL_LIVE",
            "valid_for_claim": False,
        },
        {
            "class_id": "RC4473_3_labelled_species",
            "readout_type": "physical labelled cell species or subchannel",
            "bulk_action_slot": "same symmetric formula can still describe physical species",
            "variation_status": "species selection can become physical after gauge fixing",
            "effect": "quotient gauge proof fails; finite c_R2_cell branch retained",
            "current_status": "COUNTERMODEL_LIVE",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4473_0_no_marker_contract",
            "finding": "no-marker is not one condition; it requires field absence, external readout, variational silence, boundary silence and species exclusion",
            "consequence": "the marker loophole is now a finite theorem contract",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4473_1_current_parent_status",
            "finding": "current corpus does not parent-sign field absence or no-backreaction for relational/source markers",
            "consequence": "the gauge/no-grain route remains conditional",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4473_2_residual_branch_ready",
            "finding": "marker residual branch now has named slots for M_cell, lambda_M, ell_marker, c_R2_marker, C_marker and T_marker/J_marker",
            "consequence": "if the proof fails, local tests can bound a marker branch rather than absorbing it into words",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4473_3_next_target",
            "finding": "the next best target is external readout no-backreaction, because that is the safest way to keep relational readout without physical marker debt",
            "consequence": "prove source-at-zero/readout dressing has no variational source or fill marker coupling rows",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    residual_rows: List[Dict[str, object]],
    readout_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    theorem_written = any(row.get("theorem_id") == "NME4473_6_verdict" for row in theorem_rows)
    no_marker_signed = any(row.get("theorem_id") == "NME4473_6_verdict" and row.get("parent_signed") is True for row in theorem_rows)
    marker_countermodel_retained = any(row.get("class_id") == "RC4473_2_material_marker" for row in readout_rows)
    residual_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("status") != "BLOCKED_SOURCE_READY"
        for row in residual_rows
    )
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, theorem_rows, residual_rows, readout_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4473_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4472, 340/341 marker hazards, and refinement/ellcell rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4473_1_no_marker_contract_written",
            "claim": "no-marker/source-extension theorem contract is explicit",
            "gate_pass": theorem_written,
            "claim_allowed": False,
            "detail": "field absence, external readout, variational silence, boundary silence and species exclusion clauses are written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4473_2_no_marker_parent_signed",
            "claim": "MTS parent excludes marker/source extension",
            "gate_pass": no_marker_signed,
            "claim_allowed": False,
            "detail": "field-inventory and no-backreaction clauses remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4473_3_marker_countermodel_retained",
            "claim": "material marker countermodel is excluded",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "material marker countermodel is deliberately retained" if marker_countermodel_retained else "marker countermodel row missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4473_4_marker_residual_ready",
            "claim": "finite marker residual branch is score-ready",
            "gate_pass": residual_ready,
            "claim_allowed": False,
            "detail": "marker residual rows are explicit but still contain missing values/source paths",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4473_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4473 is a conditional theorem contract plus finite marker residual row only",
            "valid_for_claim": False,
        },
    ]
