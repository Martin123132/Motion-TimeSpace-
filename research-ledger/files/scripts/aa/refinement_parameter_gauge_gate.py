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


def refinement_gauge_proof_rows() -> List[Dict[str, object]]:
    return [
        {
            "proof_id": "RPG4472_0_projective_state_space",
            "required_clause": "parent configurations are equivalence classes or a projective/inverse-limit object over admissible refinements",
            "formal_test": "for every refinement T' -> T there is q_TT' such that Phi_T = q_TT'(Phi_T') and refinement-related representatives are the same physical state",
            "derivation_attempt": "If this holds, ell is not a physical coordinate; changing ell selects a representative of the same parent state.",
            "current_evidence": "QUOTIENT_ROUTE_MATHEMATICALLY_CLEAN_NOT_PARENT_DERIVED",
            "parent_signed": False,
            "if_signed": "cell subdivisions and ell changes are gauge/readout choices, not physical primitive grains",
            "valid_for_claim": False,
        },
        {
            "proof_id": "RPG4472_1_observable_cylindricity",
            "required_clause": "all physical bulk observables are cylindrical under refinement",
            "formal_test": "O_T'(Phi_T') = O_T(q_TT'(Phi_T')) for all admissible refinements",
            "derivation_attempt": "If observables are cylindrical, no observable can depend on fixed cell labels, cell count, or ell except through continuum fields.",
            "current_evidence": "CONDITIONAL_ROUTE_FROM_340_341_NOT_PARENT_SIGNED",
            "parent_signed": False,
            "if_signed": "D_ell O_phys=0 and ell_cell cannot be measured as a local scalar in the tested vacuum branch",
            "valid_for_claim": False,
        },
        {
            "proof_id": "RPG4472_2_action_descent",
            "required_clause": "bulk parent action descends under refinement up to fixed boundary/topological terms",
            "formal_test": "S_T'(Phi_T') = S_T(q_TT'(Phi_T')) + S_boundary/topological, with no cell-count or ell-dependent bulk residue",
            "derivation_attempt": "If the action descends, an ell^2 R^2 visible term is not cylindrical unless its coefficient vanishes or is moved to a sourced counterterm.",
            "current_evidence": "CYLINDRICAL_ACTION_CONTRACT_EXISTS_NOT_PARENT_SIGNED",
            "parent_signed": False,
            "if_signed": "visible c_R2_cell=0 for smooth c2_visible",
            "valid_for_claim": False,
        },
        {
            "proof_id": "RPG4472_3_no_marker_extension",
            "required_clause": "no material marker, active-cell spurion, boundary defect, source dressing, or physical cell species extends the quotient",
            "formal_test": "there is no parent field M_cell whose value marks a preferred cell, cell rank, primitive grain, or active/background channel",
            "derivation_attempt": "340/341 show a covariant marker can descend to an extended quotient while still carrying physical active data, so quotienting alone is insufficient.",
            "current_evidence": "MARKER_EXTENSION_HAZARD_LIVE",
            "parent_signed": False,
            "if_signed": "the physical-grain loophole closes; no hidden ell_cell readout re-enters through a marker",
            "valid_for_claim": False,
        },
        {
            "proof_id": "RPG4472_4_no_circular_scale_normalization",
            "required_clause": "ell_cell is not defined from measured G, Planck length, fitted R10 range, or a post-hoc action normalization",
            "formal_test": "any finite ell_cell row must provide a parent source path and units independent of the local-G calibration it is meant to test",
            "derivation_attempt": "The kappa scale-law audit already forbids using calibrated G as a physical-cell derivation.",
            "current_evidence": "NO_CIRCULAR_SCALE_GUARD_SIGNED",
            "parent_signed": True,
            "if_signed": "finite ell_cell branch remains empirical/source-owned, not a hidden proof of no-grain",
            "valid_for_claim": False,
        },
        {
            "proof_id": "RPG4472_5_no_singular_running_or_counterterm",
            "required_clause": "refinement does not induce c2_visible ~ ell^-2, c_bare, c_measure, c_boundary, or hidden B^T L^-1 B residue",
            "formal_test": "all singular running and renormalized R2 residues are parent-forbidden, topological, boundary-routed, or finite-sourced",
            "derivation_attempt": "Without this clause, ell may be gauge for the visible cell term while total c_R2_eff remains finite.",
            "current_evidence": "TOTAL_RESIDUE_GUARD_RETAINED",
            "parent_signed": False,
            "if_signed": "no-grain route can promote from visible c_R2_cell=0 to total c_R2_eff=0",
            "valid_for_claim": False,
        },
        {
            "proof_id": "RPG4472_6_verdict",
            "required_clause": "RPG4472_0 through RPG4472_5 all sign together",
            "formal_test": "ell is gauge iff projective state space, cylindrical observables, action descent, no marker, no circular scale, and no singular residue all hold",
            "derivation_attempt": "The theorem is exact but not currently parent-signed. Current corpus has quotient/relational templates and no-circular-scale guard, not a full parent origin.",
            "current_evidence": "REFINEMENT_PARAMETER_GAUGE_THEOREM_CONDITIONAL_PARENT_UNSIGNED",
            "parent_signed": False,
            "if_signed": "ell_cell is not physical and visible c_R2_cell=0; total c_R2_eff still requires hidden/bare/measure/boundary clauses",
            "valid_for_claim": False,
        },
    ]


def ellcell_source_normalization_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "ELL4472_0_gauge_zero_switch",
            "quantity": "Z_ell_gauge",
            "definition": "true iff ell is refinement gauge by parent state-space/action/observable descent and no marker/singular residue clauses",
            "required_source_or_proof": "projective parent configuration theorem; cylindrical observables; action descent; no marker; no singular running",
            "current_value": "CONDITIONAL_PARENT_UNSIGNED",
            "units": "boolean_certificate",
            "status": "ZERO_SWITCH_NOT_CLAIMED",
            "valid_for_claim": False,
        },
        {
            "row_id": "ELL4472_1_physical_scale_source",
            "quantity": "ell_cell",
            "definition": "physical primitive cell/cutoff/grain length if refinement is not gauge",
            "required_source_or_proof": "parent-owned length/cutoff/field-density scale with units; not Planck length or measured-G by declaration",
            "current_value": "MISSING_NONCIRCULAR_PARENT_LENGTH_SCALE",
            "units": "meters",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "ELL4472_2_shape_factor",
            "quantity": "xi_shape",
            "definition": "cell/hinge geometry factor mapping sum A_h delta_h^2 to ell_cell^2 integral sqrt(-g) R^2",
            "required_source_or_proof": "declared cell family or continuum averaging theorem; uncertainty convention; source path",
            "current_value": "MISSING_CELL_GEOMETRY_SHAPE_FACTOR",
            "units": "dimensionless",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "ELL4472_3_EH_normalization",
            "quantity": "N_EH",
            "definition": "normalization matching the primitive linear deficit term to the calibrated EH coefficient",
            "required_source_or_proof": "same convention as kappa_eff/G_cal bridge; cannot absorb c_R2 into fitted G",
            "current_value": "MISSING_EH_NORMALIZATION_CONVENTION",
            "units": "declared_action_normalization",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "ELL4472_4_visible_c2",
            "quantity": "c2_visible",
            "definition": "half the second derivative of the primitive deficit response in the selected local branch",
            "required_source_or_proof": "parent Phi(delta), sign, normalization, uncertainty, or parent oddness/refinement theorem",
            "current_value": "MISSING_PARENT_PHI_DOUBLE_PRIME_OR_ZERO_SIGNATURE",
            "units": "dimensionless_deficit_response",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "ELL4472_5_visible_cR2_cell",
            "quantity": "c_R2_cell",
            "definition": "visible grain/cell contribution to curvature-square coefficient",
            "required_source_or_proof": "xi_shape*c2_visible*ell_cell^2/N_EH, or Z_ell_gauge=true",
            "current_value": "MISSING_VISIBLE_COMPONENT_OR_ZERO_SWITCH",
            "units": "length_squared_after_EH_normalization",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "ELL4472_6_total_cR2_eff",
            "quantity": "c_R2_eff_total",
            "definition": "visible cell plus bare, hidden, measure and boundary residues",
            "required_source_or_proof": "c_R2_cell + c_bare + 0.5 B^T L^-1 B + c_measure + c_boundary",
            "current_value": "MISSING_TOTAL_RESIDUE_COMPONENTS",
            "units": "length_squared_or_declared_operator_units",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def gauge_vs_grain_decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "case_id": "GVG4472_0_true_gauge",
            "state_space": "projective quotient over refinements",
            "observable_status": "cylindrical",
            "action_status": "descends without bulk ell residue",
            "marker_status": "no physical marker",
            "result": "ell is gauge; visible c_R2_cell=0 for smooth c2_visible",
            "claim_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "GVG4472_1_labelled_species",
            "state_space": "labelled cells with permutation symmetry",
            "observable_status": "symmetric formulas may exist",
            "action_status": "same formula can describe physical species",
            "marker_status": "active sector can become physical after selection",
            "result": "ell/cell labels are not gauge; finite c_R2_cell branch retained",
            "claim_status": "COUNTERMODEL_LIVE",
            "valid_for_claim": False,
        },
        {
            "case_id": "GVG4472_2_marker_extended_quotient",
            "state_space": "quotient of state plus material marker",
            "observable_status": "formally invariant relational readout",
            "action_status": "marker can backreact or carry source data",
            "marker_status": "physical marker present",
            "result": "quotienting alone fails; finite source/marker residual row required",
            "claim_status": "COUNTERMODEL_LIVE",
            "valid_for_claim": False,
        },
        {
            "case_id": "GVG4472_3_physical_grain",
            "state_space": "primitive cells are physical microstructure",
            "observable_status": "ell_cell is measurable or source-normalized",
            "action_status": "finite c_R2_cell = xi_shape*c2_visible*ell_cell^2/N_EH",
            "marker_status": "may be absent; physical scale alone is enough",
            "result": "finite branch is honest and testable, not derived local GR",
            "claim_status": "SOURCE_AND_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4472_0_exact_contract",
            "finding": "ell is gauge only under projective state-space, cylindrical observables, action descent, no-marker and no-singular-residue clauses",
            "consequence": "the no-grain route is now a precise theorem contract, not a slogan",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4472_1_parent_status",
            "finding": "current corpus has quotient templates but does not parent-sign the quotient/refinement state space or marker exclusion",
            "consequence": "visible c_R2_cell=0 remains conditional; finite ell_cell rows stay live",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4472_2_fallback_ready",
            "finding": "ell_cell, xi_shape, N_EH, c2_visible and total c_R2_eff source-normalization slots are explicit",
            "consequence": "if proof fails, the local branch can be bounded with named inputs rather than hidden assumptions",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4472_3_next_best_target",
            "finding": "the marker/source extension is now the sharpest obstruction to the gauge route",
            "consequence": "next target should prove no physical marker/source dressing can carry the primitive grain data, or source that marker residual",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    proof_rows: List[Dict[str, object]],
    ell_rows: List[Dict[str, object]],
    decision_matrix: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    contract_written = any(row.get("proof_id") == "RPG4472_6_verdict" for row in proof_rows)
    gauge_signed = any(row.get("proof_id") == "RPG4472_6_verdict" and row.get("parent_signed") is True for row in proof_rows)
    marker_hazard_present = any(row.get("case_id") == "GVG4472_2_marker_extended_quotient" for row in decision_matrix)
    finite_rows_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("status") not in {"BLOCKED_SOURCE_READY", "ZERO_SWITCH_NOT_CLAIMED"}
        for row in ell_rows
    )
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, proof_rows, ell_rows, decision_matrix]
        for row in group
    )
    return [
        {
            "gate_id": "CG4472_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4471, 340/341 quotient hazards, 4460 refinement, and scale/no-grain inputs",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4472_1_contract_written",
            "claim": "refinement-parameter gauge theorem contract is explicit",
            "gate_pass": contract_written,
            "claim_allowed": False,
            "detail": "projective state, cylindrical observables, action descent, no marker, no circular scale and no singular residue clauses are written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4472_2_parent_gauge_signed",
            "claim": "ell is parent-signed gauge, not physical grain",
            "gate_pass": gauge_signed,
            "claim_allowed": False,
            "detail": "quotient/refinement and marker-exclusion clauses are not parent-derived",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4472_3_marker_hazard_retained",
            "claim": "marker extension hazard is excluded",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "marker hazard is deliberately retained" if marker_hazard_present else "marker hazard row missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4472_4_finite_ell_rows_ready",
            "claim": "ell_cell finite branch is score-ready",
            "gate_pass": finite_rows_ready,
            "claim_allowed": False,
            "detail": "ell_cell, xi_shape, N_EH, c2_visible and total c_R2_eff values remain missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4472_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4472 is a conditional theorem contract plus finite normalization row only",
            "valid_for_claim": False,
        },
    ]
