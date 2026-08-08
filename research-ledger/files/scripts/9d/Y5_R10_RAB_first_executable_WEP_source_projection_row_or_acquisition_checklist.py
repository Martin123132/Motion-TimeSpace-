from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1420-Y5-R10-RAB-first-executable-WEP-source-projection-row-or-acquisition-checklist.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1420_SOURCE_REGISTER.csv"
FILL_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1420_WEP_PROJECTION_ROW_FILL_ATTEMPT.csv"
ACQUISITION_CHECKLIST_PATH = SRC_DIR / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv"
ROW_STATUS_PATH = SRC_DIR / "P8_Y5_R10_1420_PMX1419_0_WEP_ROW_STATUS_UPDATE.csv"
ACCEPTANCE_GATE_PATH = SRC_DIR / "P8_Y5_R10_1420_WEP_EXECUTABILITY_ACCEPTANCE_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1420_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1420_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1420_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1420_VALIDATION.csv"

GENERATED_UTC = datetime.now(timezone.utc).isoformat()
STATUS = "Y5_R10_1420_WEP_projection_row_not_executable_acquisition_checklist_written_nonclaim"
CLAIM_CEILING = (
    "WEP_source_projection_fill_attempt_and_acquisition_checklist_only_"
    "no_WEP_pass_no_tau_shortcut_no_measured_G_absorption_no_qbar_zero"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1420_0_1419_doc",
            "source_path": "1419-Y5-R10-RAB-direct-source-variation-product-or-qbar-projection-matrix.md",
            "anchor": "NEXT1419_0_1420",
            "role": "prior checkpoint selecting first executable WEP projection row",
        },
        {
            "source_id": "SRC1420_1_1419_matrix",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1419_QBAR_SOURCE_PROJECTION_MATRIX.csv",
            "anchor": "PMX1419_0_WEP_source_charge",
            "role": "WEP projection matrix row to attempt to fill",
        },
        {
            "source_id": "SRC1420_2_1419_coeffs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv",
            "anchor": "SRCV1419_0_qbar_source_weight",
            "role": "residual coefficient vector with qbar_source_weight missing",
        },
        {
            "source_id": "SRC1420_3_1068_tau_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv",
            "anchor": "TAP1068_6_direct_product_fallback",
            "role": "WEP tau/direct product missing pack",
        },
        {
            "source_id": "SRC1420_4_1068_worldtube",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
            "anchor": "SWT1068_5_verdict",
            "role": "source-worldtube requirements remain missing",
        },
        {
            "source_id": "SRC1420_5_1068_material",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv",
            "anchor": "MAT1068_5_verdict",
            "role": "material response tensor requirements remain missing",
        },
        {
            "source_id": "SRC1420_6_1068_orbit",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv",
            "anchor": "ORB1068_5_verdict",
            "role": "orbit/readout requirements remain missing",
        },
        {
            "source_id": "SRC1420_7_1068_force",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv",
            "anchor": "FRM1068_5_verdict",
            "role": "observed-frame force/readout map not derived",
        },
        {
            "source_id": "SRC1420_8_1061_material_smoke",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "anchor": "MCON1061_2_eta_bound",
            "role": "material smoke context and WEP bound anchor, not full tensor",
        },
        {
            "source_id": "SRC1420_9_bound",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R1_WEP_source_charge",
            "role": "MICROSCOPE source-charge proxy bound anchor",
        },
        {
            "source_id": "SRC1420_10_1068_refusal",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv",
            "anchor": "DPF1068_3_refusal_rule",
            "role": "no tau=1/no measured-G absorption/no cancellation refusal rule",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def fill_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "WPF1420_0_target",
            "piece": "PMX1419_0_WEP_source_charge",
            "needed_for_executable_row": "P_WEP = |M_WEP,q qbar_source_weight + M_WEP,J current_rescaling + M_WEP,m marker_source + ...|",
            "available_evidence": "matrix schema and MICROSCOPE R1 bound anchor exist",
            "missing_evidence": "all numeric/theorem-zero residuals and all WEP projection coefficients",
            "current_status": "TARGET_EXACT_NOT_EXECUTABLE",
            "result": "continue acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "WPF1420_1_direct_parent_eta",
            "piece": "direct eta_AB parent variation",
            "needed_for_executable_row": "delta a_AB or eta_AB residual directly from S_parent in MICROSCOPE convention",
            "available_evidence": "1068 names direct route as preferred",
            "missing_evidence": "no parent variation produces eta_AB residual with units/source/readout path",
            "current_status": "MISSING_DIRECT_PARENT_PRODUCT",
            "result": "cannot bypass projection matrix",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "WPF1420_2_residual_vector",
            "piece": "r_source values",
            "needed_for_executable_row": "qbar_source_weight/current_rescaling/source_marker_guard theorem-zero or numeric",
            "available_evidence": "SRCV1419 vector declared",
            "missing_evidence": "qbar_source_weight and current_rescaling are MISSING_*; marker guard not coefficient-filled",
            "current_status": "RESIDUAL_VALUES_MISSING",
            "result": "cannot score matrix product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "WPF1420_3_source_worldtube",
            "piece": "M_WEP source leg",
            "needed_for_executable_row": "Earth/source stress profile, source composition, GM calibration guard, finite-source correction, frame units",
            "available_evidence": "1068 source-worldtube requirement rows",
            "missing_evidence": "T_source^Earth(x), composition map, finite-source kernel, units",
            "current_status": "SOURCE_WORLDTUBE_NOT_ACQUIRED",
            "result": "M_WEP,q cannot be numeric",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "WPF1420_4_material_tensor",
            "piece": "M_WEP material/test-body leg",
            "needed_for_executable_row": "full Ti/Pt relative-source material response tensor or parent theorem reducing it",
            "available_evidence": "Ti/Pt pair and alpha/Coulomb smoke delta exist",
            "missing_evidence": "full material tensor and source-weight response convention",
            "current_status": "MATERIAL_TENSOR_NOT_ACQUIRED",
            "result": "smoke values cannot be promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "WPF1420_5_orbit_readout",
            "piece": "M_WEP orbit/readout kernel",
            "needed_for_executable_row": "orbit ephemeris/average, attitude axis, eta convention, environmental model, average kernel",
            "available_evidence": "MICROSCOPE bound anchor and requirement rows",
            "missing_evidence": "orbit/readout kernel and parent-mapped eta convention",
            "current_status": "ORBIT_READOUT_NOT_ACQUIRED",
            "result": "tau/projection cannot be assigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "WPF1420_6_force_map",
            "piece": "observed-frame force/readout map",
            "needed_for_executable_row": "source residual -> a_A-a_B -> eta_AB in same observed frame with calibration",
            "available_evidence": "conditional same-frame rule and common-mode guard",
            "missing_evidence": "force map not derived; common-mode/relative separation not quantified",
            "current_status": "FORCE_MAP_NOT_DERIVED",
            "result": "no executable eta prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "WPF1420_7_verdict",
            "piece": "first executable WEP source projection row",
            "needed_for_executable_row": "WPF1420_1 through WPF1420_6 all theorem-zero, numeric, or source-backed",
            "available_evidence": "bound anchor and schema",
            "missing_evidence": "direct parent product, residual vector values, source worldtube, full material tensor, orbit/readout, force map",
            "current_status": "WEP_PROJECTION_ROW_NOT_EXECUTABLE",
            "result": "write acquisition checklist and keep WEP claims blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def acquisition_checklist_rows() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "WAC1420_0_source_worldtube_profile",
            "input_group": "source_worldtube",
            "required_artifact": "Earth/source stress or mass-density profile in observed local frame",
            "accepted_form": "sourced table/profile; or parent theorem reducing Earth to calibrated point source with error bound",
            "units_required": "SI density/profile units or dimensionless normalized kernel with declared conversion",
            "sign_or_frame_required": "observed coframe/source frame and altitude/support convention",
            "current_status": "MISSING",
            "blocks_matrix_entry": "M_WEP,q",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_1_source_composition",
            "input_group": "source_worldtube",
            "required_artifact": "Earth/source composition or source-charge convention",
            "accepted_form": "composition/source species map; or theorem that source leg is universal/common-mode",
            "units_required": "mass fractions or declared source-charge basis",
            "sign_or_frame_required": "species/source label convention matching qbar_source_weight basis",
            "current_status": "MISSING",
            "blocks_matrix_entry": "M_WEP,q and measured-G guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_2_GM_common_mode_guard",
            "input_group": "calibration_guard",
            "required_artifact": "measured GM/G calibration rule separating common mode from relative source weight",
            "accepted_form": "explicit calibration equation proving only common universal factors are absorbed",
            "units_required": "dimensionless calibration factor or SI GM convention",
            "sign_or_frame_required": "relative weights cannot be hidden by sign or calibration choice",
            "current_status": "GUARD_WRITTEN_NOT_NUMERIC",
            "blocks_matrix_entry": "fake WEP/local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_3_material_tensor",
            "input_group": "material_response",
            "required_artifact": "full Ti/Pt relative-source material response tensor",
            "accepted_form": "source-backed MICROSCOPE/material model; or parent theorem reducing response to declared Delta_w basis",
            "units_required": "dimensionless sensitivities per source-residual basis entry",
            "sign_or_frame_required": "TA6V-minus-PtRh10 sign convention or absolute-value envelope",
            "current_status": "MISSING_FULL_TENSOR",
            "blocks_matrix_entry": "M_WEP,q;M_WEP,J;M_WEP,m",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_4_smoke_material_context",
            "input_group": "material_response",
            "required_artifact": "Ti/Pt smoke convention and alpha/Coulomb delta",
            "accepted_form": "already present as nonclaim context only",
            "units_required": "dimensionless",
            "sign_or_frame_required": "absolute smoke delta; not full source-weight tensor",
            "current_status": "AVAILABLE_CONTEXT_NOT_CLAIM_INPUT",
            "blocks_matrix_entry": "none alone; cannot replace WAC1420_3",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_5_orbit_ephemeris",
            "input_group": "orbit_readout",
            "required_artifact": "MICROSCOPE orbit/altitude/time sampling or official averaged equivalent",
            "accepted_form": "official/equivalent orbit table or conservative averaged kernel with source path",
            "units_required": "time, radius/altitude, frame units",
            "sign_or_frame_required": "Earth-centered frame and instrument time convention",
            "current_status": "MISSING",
            "blocks_matrix_entry": "M_WEP,* orbit averaging",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_6_attitude_axis_kernel",
            "input_group": "orbit_readout",
            "required_artifact": "instrument sensitive axis, attitude convention, and average kernel",
            "accepted_form": "official readout kernel; or theorem scalar residual is orientation independent with error bound",
            "units_required": "dimensionless projection kernel",
            "sign_or_frame_required": "axis sign and eta_AB sign convention",
            "current_status": "MISSING",
            "blocks_matrix_entry": "M_WEP,* readout projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_7_eta_convention",
            "input_group": "observable_readout",
            "required_artifact": "eta_AB formula, sign, normalization, and absolute-value scoring convention",
            "accepted_form": "parent-mapped eta readout formula tied to MICROSCOPE bound anchor",
            "units_required": "dimensionless",
            "sign_or_frame_required": "TA6V/PtRh10 ordering and absolute claim convention",
            "current_status": "BOUND_ANCHOR_ONLY_FORMULA_NOT_PARENT_MAPPED",
            "blocks_matrix_entry": "comparison to R1 bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_8_force_map",
            "input_group": "observed_force_map",
            "required_artifact": "source residual to acceleration difference map in observed frame",
            "accepted_form": "derived force/readout equation with units and common-mode calibration guard",
            "units_required": "m s^-2 internally and dimensionless eta after normalization",
            "sign_or_frame_required": "same observed coframe for source, force, clocks, and readout",
            "current_status": "MISSING_FORCE_READOUT_MAP",
            "blocks_matrix_entry": "all M_WEP entries",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_9_residual_coefficients",
            "input_group": "source_residual_vector",
            "required_artifact": "qbar_source_weight/current_rescaling/source_marker residual values or theorem-zero certificates",
            "accepted_form": "parent theorem-zero; or source-backed coefficient values with uncertainties, units, signs, and basis",
            "units_required": "dimensionless or declared basis units",
            "sign_or_frame_required": "same parent basis as projection matrix",
            "current_status": "MISSING_RESIDUAL_VALUES",
            "blocks_matrix_entry": "r_source vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "WAC1420_10_executability_verdict",
            "input_group": "WEP_projection_row",
            "required_artifact": "all checklist rows filled or theorem-reduced",
            "accepted_form": "PMX1419_0 row can compute P_WEP with no shortcuts",
            "units_required": "dimensionless final P_WEP",
            "sign_or_frame_required": "absolute/no-cancellation envelope unless signed model permits otherwise",
            "current_status": "NOT_EXECUTABLE",
            "blocks_matrix_entry": "WEP source projection scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def row_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "WRS1420_0_PMX1419_0_status",
            "matrix_id": "PMX1419_0_WEP_source_charge",
            "old_status": "MATRIX_ROW_SCHEMA_READY_VALUES_MISSING",
            "new_status": "ACQUISITION_CHECKLIST_WRITTEN_NOT_EXECUTABLE",
            "executable": False,
            "reason": "direct product, residual values, source worldtube, full material tensor, orbit/readout kernel, eta/force map are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "WRS1420_1_bound_status",
            "matrix_id": "R1_WEP_source_charge",
            "old_status": "numeric bound anchor exists",
            "new_status": "BOUND_AVAILABLE_NOT_PREDICTION",
            "executable": False,
            "reason": "2.8e-15 bound cannot score MTS without P_WEP prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "WRS1420_2_smoke_context_status",
            "matrix_id": "MCON1061 material smoke",
            "old_status": "SMOKE_CONTEXT_AVAILABLE",
            "new_status": "CONTEXT_ONLY_NOT_FULL_TENSOR",
            "executable": False,
            "reason": "alpha/Coulomb smoke value is not the full relative source-weight material tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "WRS1420_3_verdict",
            "matrix_id": "WEP source projection row",
            "old_status": "schema ready",
            "new_status": "SOURCE_ACQUISITION_REQUIRED",
            "executable": False,
            "reason": "acquire WAC1420 checklist or derive direct eta_AB parent product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "WAG1420_0_direct_product",
            "gate": "direct parent eta_AB product",
            "opens_if": "parent variation produces eta_AB residual/theorem-zero with units/source/readout path",
            "current_status": "CLOSED_MISSING_DIRECT_PRODUCT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "WAG1420_1_projection_inputs",
            "gate": "projection coefficient completeness",
            "opens_if": "source worldtube, material tensor, orbit/readout, eta convention, force map all sourced or theorem-reduced",
            "current_status": "CLOSED_CHECKLIST_INCOMPLETE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "WAG1420_2_residual_values",
            "gate": "source residual vector completeness",
            "opens_if": "qbar_source_weight/current_rescaling/marker residuals are theorem-zero or source-backed numeric",
            "current_status": "CLOSED_RESIDUAL_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "WAG1420_3_bound_comparison",
            "gate": "R1 WEP bound comparison",
            "opens_if": "dimensionless P_WEP computed and comparable to 2.8e-15",
            "current_status": "CLOSED_PREDICTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "WAG1420_4_refusal_guards",
            "gate": "shortcut refusal",
            "opens_if": "no tau=1, no measured-G absorption, no cancellation, no qbar=0 by taste",
            "current_status": "GUARDS_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "WAG1420_5_overall",
            "gate": "WEP row executability",
            "opens_if": "WAG1420_0 or WAG1420_1+2+3 open while WAG1420_4 remains satisfied",
            "current_status": "WEP_ROW_NOT_EXECUTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1420_0_fill_verdict",
            "decision": "do not mark WEP row executable",
            "reason": "bound and smoke context exist, but prediction coefficients/projections do not",
            "next_action": "use WAC1420 checklist as source-acquisition contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1420_1_best_first_input",
            "decision": "source-worldtube/readout split should be acquired before numeric scoring",
            "reason": "without source support and eta/readout convention, material or qbar numbers cannot be projected into the bound",
            "next_action": "try parent point-source/source-worldtube theorem or acquire MICROSCOPE/Earth source metadata",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1420_2_best_next",
            "decision": "target WEP source-worldtube or parent point-source theorem next",
            "reason": "this is the first missing projection coefficient for M_WEP,q and blocks every WEP finite comparison",
            "next_action": "derive calibrated point-source theorem; if it fails, build source-backed Earth/MICROSCOPE worldtube metadata rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1420_0_WEP_row_executable",
            "claim": "PMX1419_0 WEP source projection row is executable",
            "allowed": False,
            "reason": "WPF1420_7 verdict is WEP_PROJECTION_ROW_NOT_EXECUTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1420_1_WEP_pass",
            "claim": "MTS passes MICROSCOPE/WEP source-charge bound",
            "allowed": False,
            "reason": "no dimensionless P_WEP prediction exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1420_2_tau_numeric",
            "claim": "tau_WEP or M_WEP projection coefficient is numeric/theorem-zero",
            "allowed": False,
            "reason": "source worldtube, material tensor, orbit/readout, and force map are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1420_3_shortcuts",
            "claim": "tau=1, measured-G absorption, cancellation, or qbar=0 convention may be used",
            "allowed": False,
            "reason": CLAIM_CEILING,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1420_0_1421",
            "target_doc": "1421-Y5-R10-RAB-WEP-source-worldtube-or-parent-point-source-theorem.md",
            "target_script": "scripts/Y5_R10_RAB_WEP_source_worldtube_or_parent_point_source_theorem.py",
            "task": "try to derive a calibrated point-source/source-worldtube theorem for the WEP source leg; if it fails, write source-backed Earth/MICROSCOPE worldtube metadata rows with units, frame, support, and no-claim gates",
            "success_condition": "M_WEP source leg is theorem-reduced or has acquisition-ready source metadata rows",
            "do_not_claim": "WEP pass; tau=1; measured-G absorption; point-source by taste; qbar_source_weight=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1420_1_parallel_material",
            "target_doc": "future-WEP-material-tensor-source-acquisition.md",
            "target_script": "future_source_row_route",
            "task": "after source-worldtube convention is set, acquire or derive the Ti/Pt material tensor in the same basis",
            "success_condition": "material tensor rows have source path, units, sign convention, alloy convention, and projection role",
            "do_not_claim": "alpha/Coulomb smoke delta as full tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    fill_attempt: list[dict[str, Any]],
    checklist: list[dict[str, Any]],
    row_status: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        FILL_ATTEMPT_PATH,
        ACQUISITION_CHECKLIST_PATH,
        ROW_STATUS_PATH,
        ACCEPTANCE_GATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
                "generated_utc": GENERATED_UTC,
            }
        )

    add(
        "VAL1420_0_sources",
        all(row["path_exists"] and row["anchor_found"] for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1420_1_fill_attempt",
        any(row["attempt_id"] == "WPF1420_7_verdict" and row["current_status"] == "WEP_PROJECTION_ROW_NOT_EXECUTABLE" for row in fill_attempt),
        "WEP projection fill attempt fails honestly",
    )
    required_checks = {
        "WAC1420_0_source_worldtube_profile",
        "WAC1420_3_material_tensor",
        "WAC1420_5_orbit_ephemeris",
        "WAC1420_7_eta_convention",
        "WAC1420_8_force_map",
        "WAC1420_9_residual_coefficients",
        "WAC1420_10_executability_verdict",
    }
    add(
        "VAL1420_2_checklist",
        required_checks.issubset({row["check_id"] for row in checklist}) and all(row["claim_allowed"] is False for row in checklist),
        "acquisition checklist contains all required WEP input groups and remains nonclaim",
    )
    add(
        "VAL1420_3_row_status",
        any(row["status_id"] == "WRS1420_3_verdict" and row["new_status"] == "SOURCE_ACQUISITION_REQUIRED" for row in row_status),
        "PMX1419_0 status update keeps row non-executable",
    )
    add(
        "VAL1420_4_acceptance",
        any(row["gate_id"] == "WAG1420_5_overall" and row["current_status"] == "WEP_ROW_NOT_EXECUTABLE" for row in acceptance),
        "acceptance gate blocks WEP executability",
    )
    add(
        "VAL1420_5_claim_refusal",
        all(row["allowed"] is False and row["claim_allowed"] is False for row in claim_gates),
        "WEP row executable, WEP pass, tau numeric, and shortcut claims are refused",
    )
    add(
        "VAL1420_6_decision",
        any(row["decision_id"] == "DEC1420_2_best_next" and "source-worldtube" in row["decision"] for row in decisions),
        "decision ledger selects source-worldtube/point-source theorem next",
    )
    add(
        "VAL1420_7_next_target",
        any(row["next_id"] == "NEXT1420_0_1421" for row in next_targets),
        "next target 1421 is staged",
    )
    add(
        "VAL1420_8_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1420_9_overall",
        True,
        "1420 fails WEP row executability and writes acquisition checklist as nonclaim",
    )
    if any(row["status"] == "FAIL" for row in rows):
        for row in rows:
            if row["check_id"] == "VAL1420_9_overall":
                row["status"] = "FAIL"
                row["detail"] = "one or more 1420 validation checks failed"
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    fill_attempt: list[dict[str, Any]],
    checklist: list[dict[str, Any]],
    row_status: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1420 - First Executable WEP Source Projection Row Or Acquisition Checklist

**Current verdict:** `PMX1419_0_WEP_source_charge` is not executable. The MICROSCOPE `R1_WEP_source_charge` bound and Ti/Pt smoke context exist, but the MTS prediction still lacks direct parent eta variation, source-worldtube support, full material tensor, orbit/readout kernel, observed-frame force map, and residual coefficient values.

**Discipline move:** the WEP row now has a concrete acquisition checklist. This is the first clean bridge from the local coupling theorem work into data work: every future WEP claim must satisfy this checklist or derive a direct parent product.

**Status:** `{STATUS}`

## Source Register

{md_table(sources)}

## WEP Projection Row Fill Attempt

{md_table(fill_attempt)}

## WEP Source Projection Acquisition Checklist

{md_table(checklist)}

## PMX1419_0 Row Status Update

{md_table(row_status)}

## WEP Executability Acceptance Gate

{md_table(acceptance)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(claim_gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    fill_attempt = fill_attempt_rows()
    checklist = acquisition_checklist_rows()
    row_status = row_status_rows()
    acceptance = acceptance_gate_rows()
    decisions = decision_rows()
    claim_gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, fill_attempt, checklist, row_status, acceptance, decisions, claim_gates, next_targets)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(FILL_ATTEMPT_PATH, fill_attempt)
    write_csv(ACQUISITION_CHECKLIST_PATH, checklist)
    write_csv(ROW_STATUS_PATH, row_status)
    write_csv(ACCEPTANCE_GATE_PATH, acceptance)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, claim_gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, fill_attempt, checklist, row_status, acceptance, decisions, claim_gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1420 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
