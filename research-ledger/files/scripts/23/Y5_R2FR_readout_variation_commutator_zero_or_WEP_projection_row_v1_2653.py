from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2653"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2653-Y5-R2FR-readout-variation-commutator-zero-or-WEP-projection-row-v1.md"

CHECKPOINT = "2653"
BRANCH_ID = "Y5_R2FR_READOUT_VARIATION_COMMUTATOR_OR_WEP_ROW_2653"
PREFIX = "P8_Y5_RVC_WEPROW_2653"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "commutator_attempt": RESIDUALS / f"{PREFIX}_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
    "commutator_gate": RESIDUALS / f"{PREFIX}_COMMUTATOR_GATE.csv",
    "wep_row": RESIDUALS / f"{PREFIX}_WEP_PROJECTION_ROW_V1_NONCLAIM.csv",
    "wep_requirements": RESIDUALS / f"{PREFIX}_WEP_ROW_REQUIREMENTS.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_COMMUTATOR_WEP_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_COMMUTATOR_WEP_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2653_WEP_ROW_REQUIREMENTS_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "WEP_projection_row_v1_2653_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "WEP_PROJECTION_ROW_V1_2653_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2653_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2653_COMMUTATOR_WEP_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2652_doc": {
        "path": ROOT / "2652-Y5-R2FR-action-scale-readout-stability-or-Delta-w-projection-matrix.md",
        "needles": ["ASR2652_6_verdict", "DPM2652_1_WEP_MICROSCOPE", "NEXT2652_0_selected"],
        "role": "immediate stability/projection-matrix handoff",
    },
    "2651_doc": {
        "path": ROOT / "2651-Y5-R2FR-parent-sort-nohom-constructor-or-finite-Delta-w-basis.md",
        "needles": ["PRJ2651_0_WEP", "DWB2651_9_acceptance"],
        "role": "finite Delta_w basis and WEP projection contract",
    },
    "2648_doc": {
        "path": ROOT / "2648-Y5-R2FR-source-functor-label-forgetting-or-Delta-w-WEP-kernel-v0.md",
        "needles": ["SFL2648_5_verdict", "WEPK2648_5_acceptance"],
        "role": "source-label and WEP kernel-v0 blocker",
    },
    "1225_doc": {
        "path": ROOT / "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
        "needles": ["TAU1225_6_verdict", "ACQ1225_0_official_readout_arrays", "ACQ1225_4_material_tensor", "ACQ1225_5_delta_w"],
        "role": "tau/readout/material/residual missing-source ledger",
    },
    "1080_doc": {
        "path": ROOT / "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md",
        "needles": ["BOUND1080_0_MICROSCOPE_WEP_source_charge", "MAT1080_4_full_tensor_upgrade"],
        "role": "MICROSCOPE bound anchor and material tensor acquisition context",
    },
    "1898_doc": {
        "path": ROOT / "1898-Y5-R2FR-readout-variation-commutator-zero-or-wep-projection-row-v1.md",
        "needles": ["RVC1898_5_verdict", "WEP1898_7_verdict", "VAL1898_OVERALL"],
        "role": "older commutator/WEP-row analogue",
    },
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    generated = timestamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2653_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def commutator_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "RVC2653_0_target",
            "claim_piece": "readout/variation commutator zero",
            "formal_statement": "C_R[A] := Pi_CoeffSource([delta_parent,R_A]T_H) + Pi_CoeffSource(delta_pre R_A) + Pi_CoeffSource(delta_cal R_A) must vanish for every WEP/R10/PPN/clock/orbit readout map.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this isolates where downstream readout can become a source coupling instead of harmless measurement",
            "source_anchor": "2652:ASR2652_3_readout_gap;1898:RVC1898_0_target",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RVC2653_1_pure_postprocessing_zero",
            "claim_piece": "pure postprocessing lemma",
            "formal_statement": "If R_post is absent from S_parent, absent from S_eff before variation, and has no codomain in Coeff_active_source, then Pi_CoeffSource([delta_parent,R_post]T_H)=0 by type/order.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "proof_or_obstruction": "a data-only map can report eta, orbit, clock or residual values but cannot redefine the Hilbert/Noether source already produced by variation",
            "source_anchor": "2652:STG2652_2_readout_no_reentry;1898:RVC1898_1_pure_postprocessing_zero",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RVC2653_2_projection_commutator_survives",
            "claim_piece": "projector/source-worldtube obstruction",
            "formal_statement": "For field, support, boundary, domain, material, or source-worldtube dependent projectors, delta(Pi J)=Pi delta J + (delta Pi)J, so C_R[A] can be nonzero.",
            "status": "COUNTERMODEL_ACTIVE",
            "proof_or_obstruction": "MICROSCOPE WEP requires source-worldtube, material tensor, force/readout and orbit kernels; these are not proven pure data-only maps",
            "source_anchor": "2652:DPM2652_1_WEP_MICROSCOPE;1225:ACQ1225_2_source_worldtube",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RVC2653_3_effective_prevariation_survives",
            "claim_piece": "EFT/pre-variation readout obstruction",
            "formal_statement": "If R_A or S_eff[R_A] enters before variation, then its coefficients are not readout-only and can become real source coefficients.",
            "status": "COUNTERMODEL_ACTIVE",
            "proof_or_obstruction": "pre-action weights and effective action/readout branches survive pure-postprocessing arguments",
            "source_anchor": "2652:ASR2652_4_radiative_gap;2650:NSP2650_4_action_scale_measure_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RVC2653_4_wep_specific_gap",
            "claim_piece": "WEP readout commutator",
            "formal_statement": "C_R[WEP]=0 requires source worldtube, TA6V/PtRh10 material tensor, orbit/attitude/readout arrays, eta convention, force map, tau_WEP and residual coefficient values all theorem-zero or source-backed.",
            "status": "WEP_COMMUTATOR_ZERO_NOT_DERIVED",
            "proof_or_obstruction": "the bound anchor and formula exist, but the executable WEP row is missing the objects that decide the commutator",
            "source_anchor": "1225:ACQ1225_0_official_readout_arrays;1225:ACQ1225_4_material_tensor;1080:BOUND1080_0_MICROSCOPE_WEP_source_charge",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RVC2653_5_verdict",
            "claim_piece": "general commutator zero",
            "formal_statement": "Current MTS parent primitives prove C_R[A]=0 for all local readout/effective maps.",
            "status": "PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED",
            "proof_or_obstruction": "pure data postprocessing is safe, but projector/source-worldtube, EFT, calibration feedback, material/clock response and WEP-specific kernels remain finite residual routes",
            "source_anchor": "RVC2653_0_target through RVC2653_4_wep_specific_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def commutator_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "RCG2653_0_pure_postprocess", "required_clause": "readout map is absent from S_parent and S_eff before variation", "current_status": "CONDITIONAL_LEMMA_ONLY", "if_pass": "pure reporting cannot alter parent source", "if_fail": "readout/effective map remains finite source transfer", "source_anchor": "RVC2653_1_pure_postprocessing_zero", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "RCG2653_1_no_projector_stress", "required_clause": "field/support/material/source projectors have zero source-coefficient commutator", "current_status": "PROJECTOR_COMMUTATOR_SURVIVES", "if_pass": "Pi-source terms cannot create source weights", "if_fail": "I_commutator / WEP projection transfer row remains live", "source_anchor": "RVC2653_2_projection_commutator_survives", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "RCG2653_2_no_prevariation_eft", "required_clause": "EFT/radiative/readout maps are not inserted before variation", "current_status": "EFFECTIVE_ACTION_ROUTE_OPEN", "if_pass": "readout coefficients stay downstream", "if_fail": "pre-action coefficient route survives", "source_anchor": "RVC2653_3_effective_prevariation_survives", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "RCG2653_3_wep_inputs", "required_clause": "WEP source worldtube/material/readout/tau/residual values are filled or theorem-zero", "current_status": "WEP_PROJECTION_ROW_NOT_EXECUTABLE", "if_pass": "C_R[WEP] can be bounded or tested", "if_fail": "only nonclaim WEP row v1 can be staged", "source_anchor": "RVC2653_4_wep_specific_gap", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "RCG2653_4_verdict", "required_clause": "commutator zero can support stable source-weight zero", "current_status": "COMMUTATOR_ZERO_CLAIM_BLOCKED", "if_pass": "move to local-GR/WEP/R10 scoring gates", "if_fail": "stage WEP row v1 nonclaim and acquire inputs", "source_anchor": "RCG2653_0_pure_postprocess through RCG2653_3_wep_inputs", "gate_pass": False, "valid_for_claim": False},
    ]


def wep_row_rows() -> list[dict[str, Any]]:
    return [
        {"row_id": "WEP2653_0_bound_anchor", "object": "MICROSCOPE Ti/Pt WEP bound anchor", "formula_or_value": "eta_TiPt_bound = 2.8e-15 dimensionless", "required_inputs": "none for anchor recording; full projection inputs required before prediction comparison", "current_status": "BOUND_ANCHOR_RECORDED_NOT_PREDICTION", "source_anchor": "1080:BOUND1080_0_MICROSCOPE_WEP_source_charge", "units": "dimensionless eta", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"row_id": "WEP2653_1_projection_formula_v1", "object": "first WEP finite projection row", "formula_or_value": "eta_TiPt_MTS = tau_WEP * K_WEP[Earth,orbit,readout,TA6V-PtRh10] dot Delta_w_eff with absolute/no-cancellation envelope", "required_inputs": "Delta_w_eff parent values; tau_WEP; K_WEP; source worldtube; TA6V/PtRh10 material tensor; force/readout convention", "current_status": "FORMULA_STAGED_SYMBOLIC_NONCLAIM", "source_anchor": "2652:DPM2652_1_WEP_MICROSCOPE;2651:PRJ2651_0_WEP", "units": "dimensionless eta", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"row_id": "WEP2653_2_residual_vector", "object": "Delta_w_eff residual vector", "formula_or_value": "Delta_w_eff=P_perp(Delta_w_species+c_A_current_rescale+Delta_w_marker_hidden+Delta_w_measure)+J_NH_retained+Delta_mu_projector+R_material_X", "required_inputs": "parent numeric values, uncertainties, or theorem-zero certificates for each component", "current_status": "PARENT_RESIDUAL_VALUES_MISSING", "source_anchor": "2651:DWB2651_9_acceptance;2652:DPM2652_0_core_vector", "units": "dimensionless or declared current/projector units", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"row_id": "WEP2653_3_source_worldtube", "object": "Earth/source worldtube leg", "formula_or_value": "K_source=functional[T_source^Earth(x), composition/source-charge convention, finite-source kernel, observed coframe]", "required_inputs": "Earth stress/profile table or parent theorem reducing source to calibrated point source with error bound", "current_status": "SOURCE_WORLDTUBE_NOT_ACQUIRED", "source_anchor": "1225:ACQ1225_2_source_worldtube", "units": "SI density/profile or normalized dimensionless kernel", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"row_id": "WEP2653_4_material_tensor", "object": "TA6V/PtRh10 material response tensor", "formula_or_value": "K_material=response(TA6V - PtRh10) to Delta_w_eff in the same source-weight basis", "required_inputs": "full relative-source material response tensor or parent theorem reducing response to declared basis", "current_status": "MISSING_FULL_TENSOR", "source_anchor": "1225:ACQ1225_4_material_tensor;1080:MAT1080_4_full_tensor_upgrade", "units": "dimensionless sensitivities per source-residual basis entry", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"row_id": "WEP2653_5_orbit_readout_force", "object": "orbit/attitude/force/readout kernel", "formula_or_value": "K_readout maps parent source residual -> a_TA6V-a_PtRh10 -> eta_TiPt in the observed frame", "required_inputs": "official MICROSCOPE arrays or exact equivalent; attitude axis; eta convention; force map; common-mode guard", "current_status": "OFFICIAL_ARRAYS_AND_FORCE_MAP_MISSING", "source_anchor": "1225:ACQ1225_0_official_readout_arrays", "units": "m s^-2 internally; dimensionless eta after normalization", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"row_id": "WEP2653_6_tau_wep", "object": "tau_WEP contraction/projection factor", "formula_or_value": "tau_WEP=functional[source worldtube, orbit average, observed coframe, material tensor, force readout]", "required_inputs": "numeric sourced tau, theorem-zero, or retained nuisance with prior; unity shortcut forbidden", "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED", "source_anchor": "1225:TAU1225_6_verdict;1066:TWP1066_7_verdict", "units": "dimensionless projection/contraction factor", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"row_id": "WEP2653_7_verdict", "object": "WEP projection row v1 executability", "formula_or_value": "|eta_TiPt_MTS| <= eta_TiPt_bound can be evaluated only after WEP2653_2 through WEP2653_6 are filled or theorem-zero", "required_inputs": "parent residual values; tau/K/source/material/readout kernels; no-cancellation envelope; source paths", "current_status": "WEP_PROJECTION_ROW_V1_NOT_EXECUTABLE_NONCLAIM", "source_anchor": "WEP2653_0_bound_anchor through WEP2653_6_tau_wep", "units": "dimensionless eta", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def wep_requirement_rows() -> list[dict[str, Any]]:
    return [
        {"requirement_id": "WRQ2653_0_parent_values", "needed_for": "Delta_w_eff", "required_artifact": "parent residual coefficients or theorem-zero certificates", "current_status": "MISSING_RESIDUAL_VALUES", "source_anchor": "2651:DWB2651_9_acceptance", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ2653_1_source_worldtube", "needed_for": "K_source", "required_artifact": "Earth/source stress profile and composition/source convention", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "source_anchor": "1225:ACQ1225_2_source_worldtube", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ2653_2_material_tensor", "needed_for": "K_material", "required_artifact": "full TA6V/PtRh10 material response tensor in Delta_w basis", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "source_anchor": "1225:ACQ1225_4_material_tensor", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ2653_3_readout_arrays", "needed_for": "K_readout", "required_artifact": "official MICROSCOPE CMSM/export arrays or validated exact equivalent", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "source_anchor": "1225:ACQ1225_0_official_readout_arrays", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ2653_4_force_map", "needed_for": "eta convention", "required_artifact": "source residual to differential acceleration map in same observed frame", "current_status": "MISSING_FORCE_READOUT_MAP", "source_anchor": "2652:DPM2652_1_WEP_MICROSCOPE", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ2653_5_tau_wep", "needed_for": "projection product", "required_artifact": "derived or sourced tau_WEP; tau_WEP=1 shortcut forbidden", "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED", "source_anchor": "1225:TAU1225_6_verdict", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "WRQ2653_6_no_cancellation", "needed_for": "comparison policy", "required_artifact": "absolute/no-cancellation envelope unless a parent identity proves signed cancellation", "current_status": "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM", "source_anchor": "2651:DWB2651_8_no_cancellation_policy", "blocks_claim": True, "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY2653_0_general_commutator", "pure_postprocess_only": False, "general_commutator_signed": False, "parent_values_present": False, "source_worldtube_present": False, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_GENERAL_COMMUTATOR_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY2653_1_pure_overpromotion", "pure_postprocess_only": True, "general_commutator_signed": False, "parent_values_present": False, "source_worldtube_present": False, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_PURE_POSTPROCESSING_OVERPROMOTION", "valid_for_claim": False},
        {"case_id": "DRY2653_2_parent_values", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": False, "source_worldtube_present": False, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEP_PARENT_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2653_3_source_worldtube", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": False, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEP_SOURCE_WORLDTUBE_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2653_4_material", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": False, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEP_MATERIAL_TENSOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2653_5_readout", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": True, "readout_arrays_present": False, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_WEP_READOUT_ARRAYS_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2653_6_tau", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": True, "readout_arrays_present": True, "tau_wep_present": False, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_TAU_WEP_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY2653_7_bound_anchor", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": True, "readout_arrays_present": True, "tau_wep_present": True, "bound_anchor_only": True, "uses_cancellation": False, "expected_status": "REFUSED_BOUND_ANCHOR_ONLY", "valid_for_claim": False},
        {"case_id": "DRY2653_8_cancellation", "pure_postprocess_only": False, "general_commutator_signed": True, "parent_values_present": True, "source_worldtube_present": True, "material_tensor_present": True, "readout_arrays_present": True, "tau_wep_present": True, "bound_anchor_only": False, "uses_cancellation": True, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
    ]


def evaluate_dryrun(row: dict[str, Any]) -> str:
    if row["pure_postprocess_only"] and not row["general_commutator_signed"]:
        return "REFUSED_PURE_POSTPROCESSING_OVERPROMOTION"
    if not row["general_commutator_signed"]:
        return "REFUSED_GENERAL_COMMUTATOR_NOT_DERIVED"
    if not row["parent_values_present"]:
        return "REFUSED_WEP_PARENT_VALUES_MISSING"
    if not row["source_worldtube_present"]:
        return "REFUSED_WEP_SOURCE_WORLDTUBE_MISSING"
    if not row["material_tensor_present"]:
        return "REFUSED_WEP_MATERIAL_TENSOR_MISSING"
    if not row["readout_arrays_present"]:
        return "REFUSED_WEP_READOUT_ARRAYS_MISSING"
    if not row["tau_wep_present"]:
        return "REFUSED_TAU_WEP_NOT_DERIVED"
    if row["bound_anchor_only"]:
        return "REFUSED_BOUND_ANCHOR_ONLY"
    if row["uses_cancellation"]:
        return "REFUSED_CANCELLATION_ONLY"
    return "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = timestamp()
    return [
        {
            "case_id": row["case_id"],
            "computed_status": evaluate_dryrun(row),
            "expected_status": row["expected_status"],
            "status_match": evaluate_dryrun(row) == row["expected_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in cases
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG2653_0_commutator", "condition": "general readout/variation commutator zero is parent-signed", "current_status": "FAIL_PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED", "source_anchor": f"{OUTPUTS['commutator_attempt'].name}:RVC2653_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2653_1_wep_executable", "condition": "WEP row has parent values plus tau/K/source/material/readout inputs", "current_status": "FAIL_WEP_PROJECTION_ROW_V1_NOT_EXECUTABLE_NONCLAIM", "source_anchor": f"{OUTPUTS['wep_row'].name}:WEP2653_7_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2653_2_bound_not_prediction", "condition": "MICROSCOPE bound anchor is not mistaken for an MTS prediction", "current_status": "PASS_GUARD_ENFORCED_BUT_NONCLAIM", "source_anchor": f"{OUTPUTS['wep_row'].name}:WEP2653_0_bound_anchor", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2653_3_no_cancellation", "condition": "WEP pass does not rely on fitted cancellation", "current_status": "PASS_POLICY_ENFORCED_BUT_NONCLAIM", "source_anchor": f"{OUTPUTS['wep_requirements'].name}:WRQ2653_6_no_cancellation", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2653_4_verdict", "condition": "readout commutator or WEP row supports local-GR/WEP claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG2653_0_commutator through CG2653_3_no_cancellation", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2653_0_commutator", "decision": "DO_NOT_PROMOTE_GENERAL_READOUT_VARIATION_COMMUTATOR_ZERO", "reason": "pure postprocessing is safe, but WEP-style projectors/source-worldtube/material/readout maps are not proven pure and can carry finite transfer residuals", "status": "COMMUTATOR_ROUTE_NARROWED_NOT_CLOSED", "next_dependency": "prove no projector stress/source-worldtube reentry or retain WEP input row", "valid_for_claim": False},
        {"decision_id": "DEC2653_1_wep_row", "decision": "WEP_PROJECTION_ROW_V1_STAGED_NONCLAIM", "reason": "the bound anchor and formula are recorded, but parent residual values, source worldtube, material tensor, readout arrays, force map and tau_WEP are missing", "status": "WEP_ROW_V1_STAGED_NONCLAIM", "next_dependency": "source WEP inputs or derive action/current owner lemma", "valid_for_claim": False},
        {"decision_id": "DEC2653_2_next", "decision": "SELECT_2654_WEP_INPUT_PACK_OR_ACTION_CURRENT_OWNER", "reason": "this split gives one path toward real testing and one path toward derived local-GR source universality", "status": "NEXT_TARGET_SELECTED", "next_dependency": "2654 WEP source-worldtube/material tensor acquisition or action-owner lemma", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2653_0_selected",
            "status": "selected",
            "next_doc": "2654-Y5-R2FR-WEP-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md",
            "next_script": "scripts/Y5_R2FR_WEP_source_worldtube_material_tensor_acquisition_or_action_owner_lemma_2654.py",
            "target": "Try to derive the action/current owner needed to zero WEP source weights; if it fails, acquire/source-ready WEP worldtube, material tensor, readout, force-map and tau_WEP inputs as nonclaim rows.",
            "must_include": "action/current owner lemma; WEP source-worldtube row; TA6V/PtRh10 material tensor row; readout arrays; force map; tau_WEP; refusal states",
            "must_exclude": "WEP/local-GR claim from MICROSCOPE bound anchor, tau_WEP=1 shortcut, symbolic Delta_w scoring, cancellation-only pass, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT2653_0_theory", "area": "readout no-reentry", "summary": "pure postprocessing is harmless, but general readout/effective/projector commutator zero is not derived", "risk_level": "COMMUTATOR_NARROWED_NOT_CLOSED", "project_meaning": "the local-GR source-universality route has a precise obstruction rather than a vague coupling worry", "next_action": "prove no projector stress/source-worldtube reentry or action/current ownership", "valid_for_claim": False},
        {"status_id": "STAT2653_1_wep", "area": "WEP empirical branch", "summary": "the first WEP projection row is written with the MICROSCOPE bound anchor but remains non-executable", "risk_level": "TEST_ROW_STRUCTURED_MISSING_INPUTS", "project_meaning": "we are close to a real WEP test scaffold, not close to a WEP claim", "next_action": "fill source worldtube, material tensor, official readout/force map, tau_WEP and parent residual values", "valid_for_claim": False},
        {"status_id": "STAT2653_2_project_overview", "area": "GR/Newton reduction bridge", "summary": "source universality still fails as a theorem, but now has a WEP test row and exact missing inputs", "risk_level": "ACTIONABLE_INPUT_DEBT", "project_meaning": "the theory branch and empirical branch are now cleanly split", "next_action": "2654 WEP input pack or action/current owner", "valid_for_claim": False},
    ]


def branch_copy_rows(commutator_rows: list[dict[str, Any]], wep_rows: list[dict[str, Any]], req_rows: list[dict[str, Any]], dryrun_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    write_csv(BRANCH_COPIES["queue"], req_rows)
    write_csv(BRANCH_COPIES["local_bounds"], wep_rows)
    write_csv(BRANCH_COPIES["source_weight"], wep_rows)
    write_csv(BRANCH_COPIES["microscope"], commutator_rows)
    write_csv(BRANCH_COPIES["quarantine"], dryrun_rows)
    return [
        {"copy_id": copy_id, "path": str(path), "exists": path.exists(), "parseable_csv": path.exists() and len(csv_rows(path)) >= 1, "purpose": "2653 commutator/WEP-row nonclaim handoff", "valid_for_claim": False}
        for copy_id, path in BRANCH_COPIES.items()
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    commutator = commutator_attempt_rows()
    wep = wep_row_rows()
    req = wep_requirement_rows()
    cases = dryrun_case_rows()
    dry = dryrun_result_rows(cases)
    rows = {
        "source_register": source_register_rows(),
        "commutator_attempt": commutator,
        "commutator_gate": commutator_gate_rows(),
        "wep_row": wep,
        "wep_requirements": req,
        "dryrun_cases": cases,
        "dryrun_results": dry,
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["branch_copies"] = branch_copy_rows(commutator, wep, req, dry)
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2653-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2653*",
        "*Y5_R2FR_readout_variation_commutator_zero_or_WEP_projection_row_v1_2653*",
        "*JR2653*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    commutator_ok = any(row["attempt_id"] == "RVC2653_5_verdict" and row["status"] == "PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED" for row in rows["commutator_attempt"])
    wep_ok = len(rows["wep_row"]) >= 8 and all(not row["score_ready"] and not row["valid_prediction_row"] for row in rows["wep_row"])
    requirements_ok = all(row["blocks_claim"] and not row["valid_for_claim"] for row in rows["wep_requirements"])
    dry_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = any(row["gate_id"] == "CG2653_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] for row in rows["claim_gates"])
    next_ok = any("2654-Y5-R2FR-WEP-source-worldtube-material-tensor" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2653_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2653_01_commutator_verdict", commutator_ok, "general readout/variation commutator zero remains unsigned"),
        ("VAL2653_02_wep_row", wep_ok, "WEP row v1 is nonclaim/not score-ready"),
        ("VAL2653_03_requirements_block", requirements_ok, "all WEP requirements block claims until sourced"),
        ("VAL2653_04_dryrun", dry_ok, "dry-run refuses commutator overpromotion and missing WEP inputs"),
        ("VAL2653_05_claim_gates_false", claim_ok, "claim remains blocked"),
        ("VAL2653_06_next_target", next_ok, "2654 target is recorded"),
        ("VAL2653_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2653_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2653_09_formalization_untouched", formal_ok, "no 2653 outputs are written under formalization-workbench"),
        ("VAL2653_10_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = timestamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2653_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2653 keeps general readout commutator zero unsigned, stages WEP projection row v1, and selects WEP input pack or action-owner lemma next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2653 - Readout-Variation Commutator Zero Or WEP Projection Row V1

## Purpose

This checkpoint tests the narrow readout no-reentry route: prove `[delta_parent, R_readout]` has no source-only coefficient codomain, or stage the first WEP projection row with every missing input explicit.

## Result

- Pure postprocessing is safe as a conditional lemma, but general readout/projector/source-worldtube commutator zero is not parent-derived.
- The WEP projection formula is now a concrete row, not just a vague test idea.
- The MICROSCOPE bound anchor is recorded, but it is not an MTS prediction and cannot score the row.
- WEP row v1 remains non-executable until parent residual values, source worldtube, material tensor, official readout/force map and tau_WEP are filled or theorem-zero.

## Source Register

{markdown_table(rows["source_register"])}

## Readout-Variation Commutator Attempt

{markdown_table(rows["commutator_attempt"])}

## Commutator Gate

{markdown_table(rows["commutator_gate"])}

## WEP Projection Row V1

{markdown_table(rows["wep_row"])}

## WEP Row Requirements

{markdown_table(rows["wep_requirements"])}

## Dry-Run Cases

{markdown_table(rows["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows["dryrun_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows = build_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
