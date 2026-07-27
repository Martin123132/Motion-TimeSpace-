from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1898"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1898-Y5-R2FR-readout-variation-commutator-zero-or-wep-projection-row-v1.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1897_doc": ROOT / "1897-Y5-R2FR-action-scale-readout-stability-or-deltaw-projection-matrix.md",
    "1897_validation": OUT / "P8_Y5_BRR545_1897_VALIDATION.csv",
    "1897_stability": OUT / "P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv",
    "1897_projection_matrix": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "1897_next": OUT / "P8_Y5_PARENT_QLOC_1897_NEXT_TARGET.csv",
    "1701_no_reentry": OUT / "P8_Y5_PARENT_QLOC_1701_NO_REENTRY_THEOREM_ATTEMPT.csv",
    "1701_commutator": OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv",
    "1701_finite_map": OUT / "P8_Y5_PARENT_QLOC_1701_ARENA_FINITE_PRODUCT_MAP.csv",
    "1701_runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1701_RUNNER_REFUSAL.csv",
    "1816_variation_before_readout": OUT / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv",
    "1454_ca_split": OUT / "P8_Y5_R10_1454_C_A_READOUT_CALIBRATION_SPLIT.csv",
    "1420_wep_fill_attempt": OUT / "P8_Y5_R10_1420_WEP_PROJECTION_ROW_FILL_ATTEMPT.csv",
    "1420_wep_checklist": OUT / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv",
    "1695_tau_wep": OUT / "P8_Y5_PARENT_QLOC_1695_TAU_WEP_PROJECTION_READINESS.csv",
    "1066_tau_contract": OUT / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
    "1225_tau_attempt": OUT / "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
    "1061_material_convention": OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}


SOURCE_NEEDLES = {
    "1897_doc": ["Action-Scale Readout Stability", "ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED"],
    "1897_validation": ["VAL1897_OVERALL,PASS"],
    "1897_stability": ["ASR1897_3_readout_gap", "READOUT_NO_REENTRY_UNSIGNED"],
    "1897_projection_matrix": ["DPM1897_1_WEP_MICROSCOPE", "DPM1897_6_no_cancellation_policy"],
    "1897_next": ["NEXT1897_0_primary", "1898-Y5-R2FR-readout-variation-commutator-zero-or-wep-projection-row-v1.md"],
    "1701_no_reentry": ["NRE1701_5_verdict", "PURE_POSTPROCESSING_ONLY_GENERAL_BLOCKED"],
    "1701_commutator": ["RC1701_6_verdict", "GENERAL_NO_REENTRY_NOT_DERIVED"],
    "1701_finite_map": ["FPM1701_0_WEP_source_weight", "MISSING_DELTA_W_OR_TAU_WEP_OR_OFFICIAL_READOUT"],
    "1701_runner_refusal": ["RUN1701_4_score_products", "REJECT_SCORE"],
    "1816_variation_before_readout": ["VBR1816_6_verdict", "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF"],
    "1454_ca_split": ["CAS1454_4_verdict", "PARTIAL_NOT_CLAIM"],
    "1420_wep_fill_attempt": ["WPF1420_7_verdict", "WEP_PROJECTION_ROW_NOT_EXECUTABLE"],
    "1420_wep_checklist": ["WAC1420_10_executability_verdict", "NOT_EXECUTABLE"],
    "1695_tau_wep": ["TAU1695_7_parser_status", "BLOCKED"],
    "1066_tau_contract": ["TWP1066_7_verdict", "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED"],
    "1225_tau_attempt": ["TAU1225_6_verdict", "TAU_WEP_PROJECTION_NOT_DERIVED"],
    "1061_material_convention": ["MCON1061_2_eta_bound", "numeric_bound_anchor_filled"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "local_bound_claims": ["R1_WEP_source_charge", "2.8e-15"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1898_SOURCE_REGISTER.csv",
    "commutator_attempt": OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
    "commutator_gate": OUT / "P8_Y5_PARENT_QLOC_1898_COMMUTATOR_GATE.csv",
    "wep_row": OUT / "P8_Y5_PARENT_QLOC_1898_WEP_PROJECTION_ROW_V1_NONCLAIM.csv",
    "wep_requirements": OUT / "P8_Y5_PARENT_QLOC_1898_WEP_ROW_REQUIREMENTS.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1898_COMMUTATOR_WEP_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1898_COMMUTATOR_WEP_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1898_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1898_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1898_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1898_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1898_VALIDATION.csv",
}


BRANCH_COPIES = {
    "commutator_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["commutator_attempt"].name,
    "wep_row": SOURCE_WEIGHT_DOCS / "WEP_PROJECTION_ROW_V1_1898_NONCLAIM.csv",
    "wep_requirements": QUEUE / "JR1898_WEP_ROW_REQUIREMENTS_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = SOURCE_NEEDLES[source_id]
        missing_needles = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(needles),
                "missing_needles": "; ".join(missing_needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing_needles else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def commutator_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "RVC1898_0_target",
            "claim_piece": "readout/variation commutator zero",
            "formal_statement": "C_R[A] := Pi_CoeffSource([delta_parent,R_A]T_H) + Pi_CoeffSource(delta_pre R_A) + Pi_CoeffSource(delta_cal R_A) must vanish for every WEP/R10/PPN/clock/orbit readout map.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this isolates the exact place where downstream readout can become a source coupling instead of a harmless measurement",
            "source_anchor": "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv:RC1701_0_define_residual; P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv:ASR1897_3_readout_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "RVC1898_1_pure_postprocessing_zero",
            "claim_piece": "pure postprocessing lemma",
            "formal_statement": "If R_post: Sol(S_parent)/G -> Data_A is absent from S_parent, absent from S_eff before variation, and has no codomain in Coeff_active_source, then Pi_CoeffSource([delta_parent,R_post]T_H)=0 by type/order.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "proof_or_obstruction": "a data-only map can report eta, orbit, clock, or residual values but cannot redefine the Hilbert/Noether source already produced by variation",
            "source_anchor": "P8_Y5_PARENT_QLOC_1701_NO_REENTRY_THEOREM_ATTEMPT.csv:NRE1701_0_type_theorem; P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv:VBR1816_1_variation_operator",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "RVC1898_2_projection_commutator_survives",
            "claim_piece": "projector/source-worldtube obstruction",
            "formal_statement": "For field, support, boundary, domain, material, or source-worldtube dependent projectors, delta(Pi J)=Pi delta J + (delta Pi)J, so C_R[A] can be nonzero.",
            "status": "COUNTERMODEL_ACTIVE",
            "proof_or_obstruction": "MICROSCOPE WEP requires source worldtube, material tensor, force/readout, and orbit kernels; those are not proven pure data-only maps",
            "source_anchor": "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv:RC1701_2_projection_operator; P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_0_source_worldtube_profile",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "RVC1898_3_effective_prevariation_survives",
            "claim_piece": "EFT/pre-variation readout obstruction",
            "formal_statement": "If R_A or S_eff[R_A] enters before variation, then its coefficients are not readout-only and can become real source coefficients.",
            "status": "COUNTERMODEL_ACTIVE",
            "proof_or_obstruction": "pre-action weights and effective action/readout branches survive all pure-postprocessing arguments",
            "source_anchor": "P8_Y5_PARENT_QLOC_1701_NO_REENTRY_THEOREM_ATTEMPT.csv:NRE1701_2_preaction_weights; P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv:RC1701_3_effective_action",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "RVC1898_4_wep_specific_gap",
            "claim_piece": "WEP readout commutator",
            "formal_statement": "C_R[WEP]=0 requires source worldtube, Ti/Pt material tensor, orbit/attitude/readout arrays, eta convention, force map, tau_WEP, and residual coefficient values all theorem-zero or source-backed.",
            "status": "WEP_COMMUTATOR_ZERO_NOT_DERIVED",
            "proof_or_obstruction": "the bound anchor and material smoke convention exist, but the executable WEP row is missing exactly the objects that would decide the commutator",
            "source_anchor": "P8_Y5_R10_1420_WEP_PROJECTION_ROW_FILL_ATTEMPT.csv:WPF1420_7_verdict; P8_Y5_PARENT_QLOC_1695_TAU_WEP_PROJECTION_READINESS.csv:TAU1695_7_parser_status",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "RVC1898_5_verdict",
            "claim_piece": "general commutator zero",
            "formal_statement": "Current MTS parent primitives prove C_R[A]=0 for all local readout/effective maps.",
            "status": "PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED",
            "proof_or_obstruction": "pure data postprocessing is safe, but projector/source-worldtube, EFT, calibration feedback, material/clock response, and WEP-specific kernels remain finite residual routes",
            "source_anchor": "RVC1898_0_target through RVC1898_4_wep_specific_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def commutator_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "RCG1898_0_pure_postprocess", "required_clause": "readout map is absent from S_parent and S_eff before variation", "current_status": "CONDITIONAL_LEMMA_ONLY", "if_pass": "pure reporting cannot alter parent source", "if_fail": "readout/effective map remains finite source transfer", "source_anchor": "P8_Y5_PARENT_QLOC_1701_NO_REENTRY_THEOREM_ATTEMPT.csv:NRE1701_0_type_theorem", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "RCG1898_1_no_projector_stress", "required_clause": "field/support/material/source projectors have zero source-coefficient commutator", "current_status": "PROJECTOR_COMMUTATOR_SURVIVES", "if_pass": "Pi-source terms cannot create source weights", "if_fail": "I_commutator / WEP projection transfer row remains live", "source_anchor": "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv:RC1701_2_projection_operator", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "RCG1898_2_no_prevariation_eft", "required_clause": "EFT/radiative/readout maps are not inserted before variation", "current_status": "EFFECTIVE_ACTION_ROUTE_OPEN", "if_pass": "readout coefficients stay downstream", "if_fail": "pre-action coefficient route survives", "source_anchor": "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv:RC1701_3_effective_action", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "RCG1898_3_wep_inputs", "required_clause": "WEP source worldtube/material/readout/tau/residual values are filled or theorem-zero", "current_status": "WEP_PROJECTION_ROW_NOT_EXECUTABLE", "if_pass": "C_R[WEP] can be bounded or tested", "if_fail": "only nonclaim WEP row v1 can be staged", "source_anchor": "P8_Y5_R10_1420_WEP_PROJECTION_ROW_FILL_ATTEMPT.csv:WPF1420_7_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "RCG1898_4_verdict", "required_clause": "commutator zero can support stable source-weight zero", "current_status": "COMMUTATOR_ZERO_CLAIM_BLOCKED", "if_pass": "move to local-GR/WEP/R10 scoring gates", "if_fail": "stage WEP row v1 nonclaim and acquire inputs", "source_anchor": "RCG1898_0_pure_postprocess through RCG1898_3_wep_inputs", "gate_pass": False, "valid_for_claim": False},
    ]


def wep_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "WEP1898_0_bound_anchor",
            "object": "MICROSCOPE Ti/Pt WEP bound anchor",
            "formula_or_value": "eta_TiPt_bound = 2.8e-15 dimensionless, from R1_WEP_source_charge proxy row",
            "required_inputs": "none for anchor recording; full projection inputs required before prediction comparison",
            "current_status": "BOUND_ANCHOR_RECORDED_NOT_PREDICTION",
            "source_anchor": "local_bound_claims.csv:R1_WEP_source_charge; P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_2_eta_bound",
            "units": "dimensionless eta",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "WEP1898_1_projection_formula_v1",
            "object": "first WEP finite projection row",
            "formula_or_value": "eta_TiPt^MTS = tau_WEP * K_WEP[Earth,orbit,readout,TiPt] dot Delta_w_eff, with abs/no-cancellation envelope",
            "required_inputs": "Delta_w_eff parent values; tau_WEP; K_WEP; source worldtube; Ti/Pt material tensor; force/readout convention",
            "current_status": "FORMULA_STAGED_SYMBOLIC_NONCLAIM",
            "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_1_WEP_MICROSCOPE; P8_Y5_PARENT_QLOC_1701_ARENA_FINITE_PRODUCT_MAP.csv:FPM1701_0_WEP_source_weight",
            "units": "dimensionless eta",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "WEP1898_2_residual_vector",
            "object": "Delta_w_eff residual vector",
            "formula_or_value": "Delta_w_eff = P_perp(Delta_w_species + c_A_current_rescale + Delta_w_marker_hidden) + J_NH_retained + Delta_mu_projector",
            "required_inputs": "parent numeric values, uncertainties, or theorem-zero certificates for each component",
            "current_status": "PARENT_RESIDUAL_VALUES_MISSING",
            "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_0_core_vector",
            "units": "dimensionless or declared current/projector units",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "WEP1898_3_source_worldtube",
            "object": "Earth/source worldtube leg",
            "formula_or_value": "K_source = functional[T_source^Earth(x), composition/source-charge convention, finite-source kernel, observed coframe]",
            "required_inputs": "Earth stress/profile table or parent theorem reducing source to calibrated point source with error bound",
            "current_status": "SOURCE_WORLDTUBE_NOT_ACQUIRED",
            "source_anchor": "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_0_source_worldtube_profile; WAC1420_1_source_composition",
            "units": "SI density/profile or normalized dimensionless kernel",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "WEP1898_4_material_tensor",
            "object": "Ti/Pt material response tensor",
            "formula_or_value": "K_material = response(TA6V - PtRh10) to Delta_w_eff in the same source-weight basis",
            "required_inputs": "full Ti/Pt relative-source material response tensor or parent theorem reducing response to declared basis",
            "current_status": "MISSING_FULL_TENSOR",
            "source_anchor": "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_3_material_tensor; P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_0_test_pair",
            "units": "dimensionless sensitivities per source-residual basis entry",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "WEP1898_5_orbit_readout_force",
            "object": "orbit/attitude/force/readout kernel",
            "formula_or_value": "K_readout maps parent source residual -> a_Ti-a_Pt -> eta_TiPt in the observed frame",
            "required_inputs": "official MICROSCOPE arrays or exact equivalent; attitude axis; eta convention; force map; common-mode guard",
            "current_status": "OFFICIAL_ARRAYS_AND_FORCE_MAP_MISSING",
            "source_anchor": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays; P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_8_force_map",
            "units": "m s^-2 internally; dimensionless eta after normalization",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "WEP1898_6_tau_wep",
            "object": "tau_WEP contraction/projection factor",
            "formula_or_value": "tau_WEP = functional[source worldtube, orbit average, observed coframe, material tensor, force readout]",
            "required_inputs": "numeric sourced tau, theorem-zero, or retained nuisance with prior; unity shortcut forbidden",
            "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED",
            "source_anchor": "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv:TAU1225_6_verdict; P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_5_no_unity_shortcut",
            "units": "dimensionless projection/contraction factor",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "WEP1898_7_verdict",
            "object": "WEP projection row v1 executability",
            "formula_or_value": "|eta_TiPt^MTS| <= eta_TiPt_bound can be evaluated only after WEP1898_2 through WEP1898_6 are filled or theorem-zero",
            "required_inputs": "parent residual values; tau/K/source/material/readout kernels; no-cancellation envelope; source paths",
            "current_status": "WEP_PROJECTION_ROW_V1_NOT_EXECUTABLE_NONCLAIM",
            "source_anchor": "WEP1898_0_bound_anchor through WEP1898_6_tau_wep",
            "units": "dimensionless eta",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def wep_requirement_rows() -> list[dict[str, Any]]:
    return [
        {"requirement_id": "WRQ1898_0_parent_values", "needed_for": "Delta_w_eff", "required_artifact": "parent residual coefficients or theorem-zero certificates", "current_status": "MISSING_RESIDUAL_VALUES", "source_anchor": "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_9_residual_coefficients", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ1898_1_source_worldtube", "needed_for": "K_source", "required_artifact": "Earth/source stress profile and composition/source convention", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "source_anchor": "P8_Y5_PARENT_QLOC_1695_TAU_WEP_PROJECTION_READINESS.csv:TAU1695_2_source_worldtube", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ1898_2_material_tensor", "needed_for": "K_material", "required_artifact": "full Ti/Pt material response tensor in Delta_w basis", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "source_anchor": "P8_Y5_PARENT_QLOC_1695_TAU_WEP_PROJECTION_READINESS.csv:TAU1695_3_material_tensor", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ1898_3_readout_arrays", "needed_for": "K_readout", "required_artifact": "official MICROSCOPE CMSM/export arrays or validated exact equivalent", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "source_anchor": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ1898_4_force_map", "needed_for": "eta convention", "required_artifact": "source residual to differential acceleration map in same observed frame", "current_status": "MISSING_FORCE_READOUT_MAP", "source_anchor": "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv:WAC1420_8_force_map", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ1898_5_tau_wep", "needed_for": "projection product", "required_artifact": "derived or sourced tau_WEP; tau_WEP=1 shortcut forbidden", "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED", "source_anchor": "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv:TAU1225_6_verdict", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ1898_6_no_cancellation", "needed_for": "comparison policy", "required_artifact": "absolute/no-cancellation envelope unless a parent identity proves signed cancellation", "current_status": "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_6_no_cancellation_policy", "blocks_claim": True, "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1898_0_general_commutator", "pure_postprocess_only": False, "general_commutator_signed": False, "parent_values_present": False, "source_worldtube_present": False, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_GENERAL_COMMUTATOR_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1898_1_pure_overpromotion", "pure_postprocess_only": True, "general_commutator_signed": False, "parent_values_present": False, "source_worldtube_present": False, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_PURE_POSTPROCESSING_OVERPROMOTION", "valid_for_claim": False},
        {"case_id": "DRY1898_2_parent_values", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": False, "source_worldtube_present": False, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEP_PARENT_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1898_3_source_worldtube", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": False, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEP_SOURCE_WORLDTUBE_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1898_4_material", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEP_MATERIAL_TENSOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1898_5_readout", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": True, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEP_READOUT_ARRAYS_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1898_6_tau", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": True, "readout_arrays_present": True, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_TAU_WEP_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1898_7_bound_anchor", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": True, "readout_arrays_present": True, "tau_wep_present": True, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_BOUND_ANCHOR_ONLY", "valid_for_claim": False},
        {"case_id": "DRY1898_8_cancellation", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": True, "readout_arrays_present": True, "tau_wep_present": True, "bound_anchor_only": False, "uses_cancellation": True, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    pure_postprocess_only = bool_string(row["pure_postprocess_only"]) == "true"
    general_commutator_signed = bool_string(row["general_commutator_signed"]) == "true"
    parent_values_present = bool_string(row["parent_values_present"]) == "true"
    source_worldtube_present = bool_string(row["source_worldtube_present"]) == "true"
    material_tensor_present = bool_string(row["material_tensor_present"]) == "true"
    readout_arrays_present = bool_string(row["readout_arrays_present"]) == "true"
    tau_wep_present = bool_string(row["tau_wep_present"]) == "true"
    bound_anchor_only = bool_string(row["bound_anchor_only"]) == "true"
    uses_cancellation = bool_string(row["uses_cancellation"]) == "true"

    if pure_postprocess_only and not general_commutator_signed:
        status = "REFUSED_PURE_POSTPROCESSING_OVERPROMOTION"
    elif not general_commutator_signed:
        status = "REFUSED_GENERAL_COMMUTATOR_NOT_DERIVED"
    elif not parent_values_present:
        status = "REFUSED_WEP_PARENT_VALUES_MISSING"
    elif not source_worldtube_present:
        status = "REFUSED_WEP_SOURCE_WORLDTUBE_MISSING"
    elif not material_tensor_present:
        status = "REFUSED_WEP_MATERIAL_TENSOR_MISSING"
    elif not readout_arrays_present:
        status = "REFUSED_WEP_READOUT_ARRAYS_MISSING"
    elif not tau_wep_present:
        status = "REFUSED_TAU_WEP_NOT_DERIVED"
    elif bound_anchor_only:
        status = "REFUSED_BOUND_ANCHOR_ONLY"
    elif uses_cancellation:
        status = "REFUSED_CANCELLATION_ONLY"
    else:
        status = "WOULD_REQUIRE_FULL_NUMERIC_NONCLAIM_REVIEW"

    return {
        "case_id": row["case_id"],
        "computed_status": status,
        "expected_status": row["expected_status"],
        "status_match": status == row["expected_status"],
        "claim_allowed": False,
        "valid_for_claim": False,
        "generated_utc": GENERATED_UTC,
    }


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in cases]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG1898_0_commutator", "condition": "general readout/variation commutator zero is parent-signed", "current_status": "FAIL_PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv:RVC1898_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1898_1_wep_executable", "condition": "WEP row has parent values plus tau/K/source/material/readout inputs", "current_status": "FAIL_WEP_PROJECTION_ROW_V1_NOT_EXECUTABLE_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1898_WEP_PROJECTION_ROW_V1_NONCLAIM.csv:WEP1898_7_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1898_2_bound_not_prediction", "condition": "MICROSCOPE bound anchor is not mistaken for an MTS prediction", "current_status": "PASS_GUARD_ENFORCED_BUT_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1898_WEP_PROJECTION_ROW_V1_NONCLAIM.csv:WEP1898_0_bound_anchor", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1898_3_no_cancellation", "condition": "WEP pass does not rely on fitted cancellation", "current_status": "PASS_POLICY_ENFORCED_BUT_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1898_WEP_ROW_REQUIREMENTS.csv:WRQ1898_6_no_cancellation", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1898_4_verdict", "condition": "readout commutator or WEP row supports local-GR/WEP claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1898_0_commutator through CG1898_3_no_cancellation", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1898_0_commutator", "decision": "do not promote general readout-variation commutator zero", "reason": "pure postprocessing is safe, but WEP-style projectors/source-worldtube/material/readout maps are not proven pure and can carry finite transfer residuals", "status": "COMMUTATOR_ROUTE_NARROWED_NOT_CLOSED", "next_dependency": "prove no projector stress/source-worldtube reentry or retain WEP input row", "valid_for_claim": False},
        {"decision_id": "DEC1898_1_wep_row", "decision": "stage WEP projection row v1 as nonclaim", "reason": "the bound anchor and formula are recorded, but parent residual values, source worldtube, material tensor, readout arrays, force map, and tau_WEP are missing", "status": "WEP_ROW_V1_STAGED_NONCLAIM", "next_dependency": "source WEP inputs or derive action/current owner lemma", "valid_for_claim": False},
        {"decision_id": "DEC1898_2_next", "decision": "attack WEP input pack or action/current owner next", "reason": "this gives the best split: one path toward real testing, one path toward derived local-GR source universality", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1899 WEP source-worldtube/material tensor acquisition or action-owner lemma", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1898_0_primary",
            "selection_status": "selected",
            "target_doc": "1899-Y5-R2FR-wep-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md",
            "target_script": "scripts/Y5_R2FR_wep_source_worldtube_material_tensor_acquisition_or_action_owner_lemma_1899.py",
            "objective": "try to derive the action/current owner needed to zero WEP source weights; if it fails, acquire/source-ready WEP worldtube, material tensor, readout, force-map, and tau_WEP inputs as nonclaim rows",
            "success_condition": "parent-signed action/current owner or a WEP input pack that makes the row executable without claiming a pass",
            "do_not": "do not claim WEP/local-GR from the MICROSCOPE bound anchor, do not set tau_WEP=1, and do not score until parent residual values or theorem-zero certificates exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1898_0_theory", "area": "readout no-reentry", "summary": "pure postprocessing is mathematically harmless, but general readout/effective/projector commutator zero is not derived", "risk_level": "COMMUTATOR_NARROWED_NOT_CLOSED", "project_meaning": "the route to local-GR source universality now has a precise obstruction rather than a vague coupling worry", "next_action": "prove no projector stress/source-worldtube reentry or action/current ownership", "valid_for_claim": False},
        {"status_id": "STAT1898_1_wep", "area": "WEP empirical branch", "summary": "the first WEP projection row is written with the real MICROSCOPE bound anchor but remains non-executable", "risk_level": "TEST_ROW_STRUCTURED_MISSING_INPUTS", "project_meaning": "we are close to a real WEP test scaffold, not close to a WEP claim", "next_action": "fill source worldtube, material tensor, official readout/force map, tau_WEP, and parent residual values", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "commutator_attempt": commutator_attempt_rows(),
        "commutator_gate": commutator_gate_rows(),
        "wep_row": wep_row_rows(),
        "wep_requirements": wep_requirement_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "SYMBOLIC", "NONCLAIM", "CLAIM_BLOCKED", "NOT_EXECUTABLE"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            text = " ".join(str(value) for value in row.values())
            if any(marker in text for marker in markers):
                for field in fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/nonclaim rows are not score-ready"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1898_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all source paths exist and needles found", "valid_for_claim": False})
    commutator_rows = csv_rows(OUTPUTS["commutator_attempt"])
    checks.append({"validation_id": "VAL1898_01_commutator_verdict", "status": "PASS" if any(row["attempt_id"] == "RVC1898_5_verdict" and row["status"] == "PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED" for row in commutator_rows) else "FAIL", "detail": "general readout/variation commutator zero remains unsigned", "valid_for_claim": False})
    wep_rows = csv_rows(OUTPUTS["wep_row"])
    checks.append({"validation_id": "VAL1898_02_wep_row", "status": "PASS" if len(wep_rows) >= 8 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in wep_rows) else "FAIL", "detail": "WEP row v1 is nonclaim/not score-ready", "valid_for_claim": False})
    requirement_rows = csv_rows(OUTPUTS["wep_requirements"])
    checks.append({"validation_id": "VAL1898_03_requirements_block", "status": "PASS" if all(row["blocks_claim"] == "True" and row["valid_for_claim"] == "False" for row in requirement_rows) else "FAIL", "detail": "all WEP requirements block claims until sourced", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1898_04_dryrun", "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows) else "FAIL", "detail": "dry-run refuses commutator overpromotion and missing WEP inputs", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1898_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1898_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1898_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1898_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1899 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1898_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1898_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1898_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1898_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1898_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = list(FORMALIZATION.rglob("*1898*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1898_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1898_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1898_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1898 readout-variation commutator zero or WEP projection row v1", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1898 - Readout-Variation Commutator Zero Or WEP Projection Row V1

## Purpose

This checkpoint tries to prove the narrower readout/variation commutator zero:

`C_R[A] := Pi_CoeffSource([delta_parent,R_A]T_H) + Pi_CoeffSource(delta_pre R_A) + Pi_CoeffSource(delta_cal R_A) = 0`.

If that general theorem does not close, it stages the first WEP projection row v1 with the real MICROSCOPE bound anchor but keeps it nonclaim.

## Result

- Pure postprocessing is safe: a data-only readout after variation cannot redefine the parent source.
- General readout/effective/projector commutator zero is not derived.
- WEP row v1 is now explicit, including bound anchor, formula, residual vector, source worldtube, material tensor, readout/force map, and tau_WEP.
- The row is not executable and no WEP/local-GR claim is made.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Readout-Variation Commutator Attempt

{markdown_table(rows_by_name["commutator_attempt"])}

## Commutator Gate

{markdown_table(rows_by_name["commutator_gate"])}

## WEP Projection Row V1

{markdown_table(rows_by_name["wep_row"])}

## WEP Row Requirements

{markdown_table(rows_by_name["wep_requirements"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
