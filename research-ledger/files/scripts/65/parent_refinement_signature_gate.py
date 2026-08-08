from __future__ import annotations

import csv
import math
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


def as_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def refinement_signature_contract_rows() -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "RGC4460_0_refinement_groupoid",
            "required_signature": "parent configurations are equivalence classes over admissible cell refinements, not labelled physical cell species",
            "formal_test": "there exists q_ref with Phi_parent[T'] -> Phi_parent[T] and physical observables O[T'] = O[T] o q_ref",
            "current_status": "QUOTIENT_ROUTE_IDENTIFIED_NOT_PARENT_DERIVED",
            "if_passes": "subdivision of one physical curvature flux is gauge/readout-silent",
            "if_fails": "cell subdivision can carry physical grain/cutoff data and c2 remains finite",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "contract_id": "RGC4460_1_cylindrical_action",
            "required_signature": "parent action is cylindrical/projectively consistent under refinement",
            "formal_test": "S_T'[Phi'] = S_T[q_ref(Phi')] for refinement-related configurations",
            "current_status": "NOT_PARENT_SIGNED",
            "if_passes": "activates the 4459 condition S_n(delta)=Phi(delta)",
            "if_fails": "refined and unrefined actions can differ by delta^2 or higher response",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "contract_id": "RGC4460_2_flux_additivity",
            "required_signature": "oriented curvature/holonomy flux is additive under refinement",
            "formal_test": "delta_total = sum_i delta_i with equal subdivision delta_i=delta/n on the same physical branch",
            "current_status": "CONDITIONAL_MATH_NOT_PARENT_SIGNED",
            "if_passes": "same-channel higher powers scale as n^(1-m) and fail invariance",
            "if_fails": "the 4459 Taylor-coefficient proof does not apply",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "contract_id": "RGC4460_3_no_physical_marker_or_grain",
            "required_signature": "no physical active marker, cell species label, or fixed primitive grain enters the local action",
            "formal_test": "all marker/cell-label data are quotient-gauge, boundary-routed, or separately retained as finite residuals",
            "current_status": "MARKER_AND_GRAIN_COUNTERMODELS_LIVE",
            "if_passes": "rules out the symmetric-labelled-species loophole from 340/341",
            "if_fails": "finite ell_cell and c2_visible rows are mandatory",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "contract_id": "RGC4460_4_geometry_owner",
            "required_signature": "refinement-equivalent flux is built from parent-owned connection/hinge/coframe variables",
            "formal_test": "Gamma_eff/omega_obs, Log(U_h), and B_h/A_h are owned in one parent action before EH/Regge import",
            "current_status": "FAILED_CURRENT_CORPUS_FROM_1827_2148_2149",
            "if_passes": "ties the refinement theorem to the actual Palatini/Regge local-GR route",
            "if_fails": "c2 zero cannot be promoted even if the abstract refinement theorem is clean",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "contract_id": "RGC4460_5_no_second_channel",
            "required_signature": "no independent density-squared, trace/norm, hidden scalar, marker-prefactor, or memory tower channel survives reduction",
            "formal_test": "all c_R2/c_Ric/c_W/c_Riem owners are zero/topological/vertical or finite-sourced in the 4458 basis",
            "current_status": "OPEN_COUNTERROUTES_RETAINED",
            "if_passes": "would make refinement zero theorem relevant to all local curvature-square channels",
            "if_fails": "zero of Phi''(0) alone does not zero the full curvature-square survivor",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
    ]


def refinement_dichotomy_rows() -> List[Dict[str, object]]:
    return [
        {
            "case_id": "DICH4460_0_exact_refinement_gauge",
            "parent_state": "unlabelled quotient/projective refinement state",
            "action_law": "S_T'[Phi'] = S_T[q_ref(Phi')]",
            "same_flux_test": "S_n(delta)=n Phi(delta/n)=Phi(delta)",
            "c2_status": "c2_visible=0 if all contract rows pass",
            "local_gr_value": "strong zero-selector candidate for visible curvature-square channel",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DICH4460_1_symmetric_labelled_species",
            "parent_state": "labelled cells with permutation symmetry",
            "action_law": "formula can be symmetric while states remain physically distinct",
            "same_flux_test": "label symmetry does not imply refinement equivalence",
            "c2_status": "c2_visible remains legal",
            "local_gr_value": "no zero credit; finite residual route required",
            "current_status": "COUNTERMODEL_LIVE_FROM_340_341",
            "valid_for_claim": False,
        },
        {
            "case_id": "DICH4460_2_physical_grain_cutoff",
            "parent_state": "primitive cells are physical grains with finite ell_cell",
            "action_law": "S_h=A_h[k1 delta_h+c2 delta_h^2+...]",
            "same_flux_test": "subdivision changes the physical system, so 4459 theorem is not activated",
            "c2_status": "finite c_R2_eff ~ shape_factor*c2_visible*ell_cell^2/EH_normalization",
            "local_gr_value": "testable scalar/spin residual, not derived GR",
            "current_status": "FINITE_FALLBACK_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "case_id": "DICH4460_3_trace_norm_holonomy_cost",
            "parent_state": "action depends on class trace/norm/energy of holonomy mismatch",
            "action_law": "Phi(delta)=1-cos(delta) or ||Log U||^2-like",
            "same_flux_test": "natural even cost gives nonzero Phi''(0)",
            "c2_status": "finite c2 prior/source row mandatory",
            "local_gr_value": "must survive R10/PPN/clock/orbital bounds",
            "current_status": "COUNTERMODEL_LIVE_FROM_1824_1826",
            "valid_for_claim": False,
        },
    ]


def finite_c2_bound_rows(d0_bound_m2: float | None = None) -> List[Dict[str, object]]:
    d0_bound = d0_bound_m2 if d0_bound_m2 is not None else ""
    ell_limit_expr = ""
    if d0_bound_m2 is not None:
        ell_limit_expr = "ell_cell <= sqrt(D0_bound/(12*shape_factor*abs(c2_visible))) for pure-R2 scalar-only normalization"
    return [
        {
            "row_id": "FC24460_0_missing_phi",
            "quantity": "c2_visible",
            "formula": "c2_visible = 1/2 Phi''(0)",
            "required_inputs": "parent Phi(delta); sign; normalization; uncertainty/prior; source path",
            "current_value": "MISSING_PARENT_PHI_DOUBLE_PRIME_0",
            "units": "dimensionless_deficit_response",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "FC24460_1_cell_scale",
            "quantity": "ell_cell",
            "formula": "c_R2_eff ~ shape_factor*c2_visible*ell_cell^2/EH_normalization",
            "required_inputs": "physical cell scale or proof no physical grain exists; shape factor; EH normalization",
            "current_value": "MISSING_CELL_SCALE_SHAPE_FACTOR_EH_NORMALIZATION",
            "units": "meters",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "FC24460_2_pure_R2_pressure",
            "quantity": "pure_R2_candidate_bound_pressure",
            "formula": ell_limit_expr or "requires D0_bound from 4457/4458 and finite c2/ell_cell inputs",
            "required_inputs": "D0_bound; c2_visible; ell_cell; shape_factor; EH_normalization",
            "current_value": d0_bound,
            "units": "m^2_for_D0_bound",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "FC24460_3_basis_coefficients",
            "quantity": "c_R2,c_Ric,c_W,c_Riem",
            "formula": "evaluate with 4458 D0/D2 maps once coefficients exist",
            "required_inputs": "source-backed MTS basis coefficient row with m^2 units and topological flags",
            "current_value": "MISSING_PARENT_BASIS_COEFFICIENTS",
            "units": "m^2",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "FC24460_4_observable_projection",
            "quantity": "scalaron/PPN/R10/local observable map",
            "formula": "lambda, alpha, gamma-1, beta-1, clock/orbital rows after linearized response",
            "required_inputs": "weak-field linearization; matter coupling; full alpha(lambda) curve; PPN response; no-cancellation vector",
            "current_value": "MISSING_OBSERVABLE_PROJECTION",
            "units": "mixed_declared_per_arena",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4460_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "source validation is performed by generator.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4460_1_signature_contract",
            "claim": "parent refinement-gauge signature contract is explicit",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "quotient/projective/cylindrical/refinement conditions written.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4460_2_parent_signed",
            "claim": "MTS parent signs refinement gauge equivalence",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "quotient state-space and cylindrical action are not derived from MTS primitives.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4460_3_c2_zero",
            "claim": "c2/c_R2/c_Ric/c_W are zero by parent theorem",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "geometry owner and no-second-channel clauses remain open.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4460_4_finite_row_score",
            "claim": "finite c2/basis coefficient branch is score-ready",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "Phi'', ell_cell, shape factor, coefficients and projections are missing.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4460_5_local_GR",
            "claim": "local GR/Newton reduction follows from 4460",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "4460 sharpens the operator selector but does not close source, connection, PPN or Newton gates.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4460_6_next_target",
            "claim": "next hinge is selected",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "4461-Y5-R2FR-connection-hinge-refinement-owner-or-c2-scalaron-map.md",
            "valid_for_claim": False,
        },
    ]

