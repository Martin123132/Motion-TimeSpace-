from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1421-Y5-R10-RAB-WEP-source-worldtube-or-parent-point-source-theorem.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1421_SOURCE_REGISTER.csv"
POINT_SOURCE_THEOREM_PATH = SRC_DIR / "P8_Y5_R10_1421_PARENT_POINT_SOURCE_THEOREM_ATTEMPT.csv"
WORLDTUBE_METADATA_PATH = SRC_DIR / "P8_Y5_R10_1421_WEP_SOURCE_WORLDTUBE_METADATA_ROWS.csv"
SOURCE_LEG_STATUS_PATH = SRC_DIR / "P8_Y5_R10_1421_MWEP_SOURCE_LEG_STATUS_UPDATE.csv"
ACCEPTANCE_GATE_PATH = SRC_DIR / "P8_Y5_R10_1421_SOURCE_LEG_ACCEPTANCE_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1421_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1421_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1421_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1421_VALIDATION.csv"

GENERATED_UTC = datetime.now(timezone.utc).isoformat()
STATUS = "Y5_R10_1421_parent_point_source_theorem_not_proved_source_worldtube_metadata_staged_nonclaim"
CLAIM_CEILING = (
    "WEP_source_worldtube_metadata_and_point_source_theorem_attempt_only_"
    "no_WEP_pass_no_tau_numeric_no_point_source_by_taste_no_measured_G_absorption"
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
            "source_id": "SRC1421_0_1420_doc",
            "source_path": "1420-Y5-R10-RAB-first-executable-WEP-source-projection-row-or-acquisition-checklist.md",
            "anchor": "NEXT1420_0_1421",
            "role": "prior checkpoint selecting WEP source-worldtube or point-source theorem",
        },
        {
            "source_id": "SRC1421_1_1420_checklist",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv",
            "anchor": "WAC1420_0_source_worldtube_profile",
            "role": "source-worldtube checklist row to close",
        },
        {
            "source_id": "SRC1421_2_1420_status",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1420_PMX1419_0_WEP_ROW_STATUS_UPDATE.csv",
            "anchor": "WRS1420_3_verdict",
            "role": "WEP projection row source acquisition required",
        },
        {
            "source_id": "SRC1421_3_1068_worldtube",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
            "anchor": "SWT1068_5_verdict",
            "role": "source worldtube not acquired",
        },
        {
            "source_id": "SRC1421_4_1069_requirements",
            "source_path": "1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
            "anchor": "REQ1069_3_source_worldtube",
            "role": "prior direct-product WEP source-worldtube requirement",
        },
        {
            "source_id": "SRC1421_5_1071_kernel_components",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv",
            "anchor": "KER1071_2_source_gravity_leg",
            "role": "official MICROSCOPE source gravity proxy form",
        },
        {
            "source_id": "SRC1421_6_1071_tau_status",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv",
            "anchor": "TAU1071_1_source_worldtube_proxy",
            "role": "source worldtube proxy form acquired but numeric tau not acquired",
        },
        {
            "source_id": "SRC1421_7_1071_external",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv",
            "anchor": "EXT1071_2_applied_acceleration_eq4",
            "role": "source-backed applied acceleration/source leg form",
        },
        {
            "source_id": "SRC1421_8_1071_segments",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv",
            "anchor": "SUEP1071_210",
            "role": "source-backed SUEP segment metadata",
        },
        {
            "source_id": "SRC1421_9_1071_portal",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv",
            "anchor": "EXT1071_9_onera_data_availability_page",
            "role": "ONERA data portal pointer",
        },
        {
            "source_id": "SRC1421_10_1419_matrix",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1419_QBAR_SOURCE_PROJECTION_MATRIX.csv",
            "anchor": "PMX1419_0_WEP_source_charge",
            "role": "WEP projection matrix row blocked by source leg",
        },
        {
            "source_id": "SRC1421_11_bound",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R1_WEP_source_charge",
            "role": "WEP source-charge bound anchor",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def point_source_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PST1421_0_target",
            "claim_piece": "calibrated point-source/source-worldtube theorem",
            "formal_statement": "replace extended Earth source leg by calibrated g(O_sat) only if all relative source-weight structure is universal/common-mode or bounded",
            "test": "M_WEP,q can use g(O_sat) without source composition/profile dependence or measured-G absorption of relative weights",
            "current_result": "TARGET_EXACT",
            "missing_for_claim": "source-current owner, Earth/source composition map, finite-source/multipole error, and common-mode calibration proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "PST1421_1_universal_exterior",
            "claim_piece": "ordinary universal mass source exterior reduction",
            "formal_statement": "for a universal metric source, the external WEP source leg can be represented by g(O_sat) and T(O_sat) computed from the chosen Earth gravity model",
            "test": "source leg enters only through total calibrated GM and official MICROSCOPE g/T functions",
            "current_result": "CONDITIONAL_FOR_COMMON_MODE_ONLY",
            "missing_for_claim": "does not apply to relative qbar_source_weight unless source composition residual is zero or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "PST1421_2_relative_source_factorization",
            "claim_piece": "relative source weight factorizes over Earth",
            "formal_statement": "rho_qbar(x)=qbar_source_weight*rho_mass(x) with qbar_source_weight constant over the source support",
            "test": "composition/source-charge profile produces no spatially varying or species-dependent source multipoles",
            "current_result": "NOT_PROVED",
            "missing_for_claim": "Earth composition/source-charge convention or parent theorem that source leg is universal/common-mode",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "PST1421_3_common_mode_calibration",
            "claim_piece": "measured GM absorbs only universal common mode",
            "formal_statement": "G_meas M_source calibration may remove kappa_common, but not relative source weights or composition-dependent source charge",
            "test": "relative qbar_source_weight cannot be hidden by calibration convention",
            "current_result": "GUARD_ACTIVE_NOT_NUMERIC",
            "missing_for_claim": "explicit calibration equation and residual decomposition in same parent basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "PST1421_4_finite_source_error",
            "claim_piece": "finite-size/multipole correction is negligible or bounded",
            "formal_statement": "extended-source support, altitude, multipole, and source-composition effects are below declared error or included in M_WEP,q",
            "test": "point-source replacement has a sourced error bound",
            "current_result": "NOT_ACQUIRED",
            "missing_for_claim": "Earth gravity model/source profile, satellite position, finite-source kernel, error budget",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "PST1421_5_MICROSCOPE_proxy",
            "claim_piece": "official MICROSCOPE source leg proxy",
            "formal_statement": "the readout model uses g(O_sat) and gravity-gradient tensor T at satellite centre",
            "test": "use official source-backed proxy form without pretending numeric arrays or qbar composition are filled",
            "current_result": "FORM_SOURCE_BACKED_NOT_NUMERIC",
            "missing_for_claim": "satellite position/velocity, gravity model, exact arrays, and MTS residual coefficient mapping",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "PST1421_6_verdict",
            "claim_piece": "WEP source leg theorem reduction",
            "formal_statement": "M_WEP,q is theorem-reduced to calibrated point-source/proxy g(O_sat)",
            "test": "PST1421_1 through PST1421_5 close without hidden relative source weights",
            "current_result": "POINT_SOURCE_THEOREM_NOT_PROVED",
            "missing_for_claim": "relative source factorization, calibration split, finite-source error, numeric source proxy arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def worldtube_metadata_rows() -> list[dict[str, Any]]:
    return [
        {
            "metadata_id": "WSW1421_0_official_source_proxy_form",
            "input_group": "source_gravity_proxy",
            "artifact": "g(O_sat) and gravity-gradient tensor T at satellite centre",
            "source_status": "SOURCE_BACKED_FORM_ACQUIRED_NOT_NUMERIC",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv",
            "source_anchor": "KER1071_2_source_gravity_leg",
            "units": "g in m s^-2; T in s^-2 once arrays are reconstructed",
            "frame_support": "satellite centre; MICROSCOPE/instrument frame after pointing transform",
            "needed_next": "numeric gx,gz,Sxx,Sxz arrays or reconstruction inputs",
            "fills_or_blocks": "partial form for WAC1420_0 and WAC1420_8; does not fill qbar source composition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "metadata_id": "WSW1421_1_satellite_position_velocity",
            "input_group": "source_gravity_proxy",
            "artifact": "satellite position/velocity and timing products",
            "source_status": "DATA_PRODUCT_REQUIREMENT_SOURCE_BACKED_NOT_DOWNLOADED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv",
            "source_anchor": "EXT1071_0_data_products",
            "units": "position m or km; velocity m s^-1; timestamps declared by product schema",
            "frame_support": "J2000 and instrument pointing transform",
            "needed_next": "CMSM schema/products or equivalent reconstructed orbit table",
            "fills_or_blocks": "blocks numeric g(O_sat) and T(O_sat)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "metadata_id": "WSW1421_2_Earth_gravity_model",
            "input_group": "source_worldtube_profile",
            "artifact": "Earth gravity model or source mass-density profile used to compute g/T",
            "source_status": "MISSING_MODEL_OR_PROFILE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
            "source_anchor": "SWT1068_0_source_stress_profile",
            "units": "density kg m^-3 or gravity-potential coefficients with declared normalization",
            "frame_support": "Earth-fixed/source frame and transform to satellite frame",
            "needed_next": "gravity model/source profile source path or theorem reducing to calibrated point source",
            "fills_or_blocks": "blocks finite-source and point-source error bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "metadata_id": "WSW1421_3_source_composition_charge",
            "input_group": "source_composition",
            "artifact": "Earth/source composition or source-charge convention",
            "source_status": "MISSING_SOURCE_COMPOSITION_MAP",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
            "source_anchor": "SWT1068_1_source_composition",
            "units": "mass fractions or dimensionless source-charge basis",
            "frame_support": "source material labels matching qbar_source_weight basis",
            "needed_next": "composition map or parent theorem that source leg is universal/common-mode",
            "fills_or_blocks": "blocks relative source-weight point-source theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "metadata_id": "WSW1421_4_finite_source_support",
            "input_group": "finite_source_correction",
            "artifact": "finite-size, altitude, multipole, support-shift error bound",
            "source_status": "MISSING_ERROR_BOUND",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
            "source_anchor": "SWT1068_3_finite_source_correction",
            "units": "dimensionless fractional error or arena-specific kernel units",
            "frame_support": "satellite altitude/source support convention",
            "needed_next": "kernel/error calculation or conservative bound",
            "fills_or_blocks": "blocks point-source by theorem rather than taste",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "metadata_id": "WSW1421_5_segment_window_metadata",
            "input_group": "segment_window",
            "artifact": "SUEP segment duration/glitch metadata",
            "source_status": "SOURCE_BACKED_SEGMENT_METADATA_ONLY",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv",
            "source_anchor": "SUEP1071_210",
            "units": "orbits and percent removed samples",
            "frame_support": "segment/window metadata only; exact timestamps/masks still needed",
            "needed_next": "exact timestamps/masks and numeric kernel arrays for one segment",
            "fills_or_blocks": "partial context for WEP source-leg pilot",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "metadata_id": "WSW1421_6_data_portal_pointer",
            "input_group": "data_access",
            "artifact": "ONERA/CMSM MICROSCOPE data portal pointer",
            "source_status": "SOURCE_BACKED_POINTER_ACCESS_UNVERIFIED_OR_BLOCKED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv",
            "source_anchor": "EXT1071_9_onera_data_availability_page",
            "units": "not applicable",
            "frame_support": "data acquisition route",
            "needed_next": "schema/file inventory or equivalent local reconstruction inputs",
            "fills_or_blocks": "blocks numeric source-leg kernel pilot",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "metadata_id": "WSW1421_7_GM_calibration_guard",
            "input_group": "calibration_guard",
            "artifact": "common-mode GM/G calibration separation",
            "source_status": "GUARD_WRITTEN_NOT_NUMERIC",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv",
            "source_anchor": "WAC1420_2_GM_common_mode_guard",
            "units": "dimensionless calibration convention or SI GM units",
            "frame_support": "relative qbar source weights cannot be absorbed into measured GM",
            "needed_next": "calibration equation in same parent residual basis",
            "fills_or_blocks": "blocks fake local-GR/WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "metadata_id": "WSW1421_8_verdict",
            "input_group": "WEP_source_worldtube",
            "artifact": "M_WEP,q source leg",
            "source_status": "FORM_PARTIAL_METADATA_STAGED_NUMERIC_SOURCE_LEG_NOT_ACQUIRED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1421_PARENT_POINT_SOURCE_THEOREM_ATTEMPT.csv",
            "source_anchor": "PST1421_6_verdict",
            "units": "dimensionless final M_WEP,q after projection; intermediate g/T SI units",
            "frame_support": "observed/instrument frame after source and pointing transforms",
            "needed_next": "numeric source proxy arrays or parent point-source theorem with error bound",
            "fills_or_blocks": "M_WEP,q remains not executable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_leg_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "SLS1421_0_WAC1420_0",
            "prior_row": "WAC1420_0_source_worldtube_profile",
            "old_status": "MISSING",
            "new_status": "OFFICIAL_PROXY_FORM_STAGED_PROFILE_NUMERIC_MISSING",
            "filled": False,
            "reason": "official g(O_sat)/T proxy form exists, but source profile/gravity model/numeric arrays are absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "SLS1421_1_WAC1420_1",
            "prior_row": "WAC1420_1_source_composition",
            "old_status": "MISSING",
            "new_status": "SOURCE_COMPOSITION_MAP_MISSING",
            "filled": False,
            "reason": "point-source theorem for relative qbar source requires source composition or universal/common-mode theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "SLS1421_2_WAC1420_2",
            "prior_row": "WAC1420_2_GM_common_mode_guard",
            "old_status": "GUARD_WRITTEN_NOT_NUMERIC",
            "new_status": "GUARD_RETAINED_CALIBRATION_EQUATION_MISSING",
            "filled": False,
            "reason": "common measured GM cannot absorb relative source weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "SLS1421_3_MWEPq",
            "prior_row": "M_WEP,q",
            "old_status": "blocked by WAC1420_0/1/2",
            "new_status": "SOURCE_LEG_METADATA_PARTIAL_NOT_EXECUTABLE",
            "filled": False,
            "reason": "numeric source leg or theorem reduction is still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "SLS1421_4_verdict",
            "prior_row": "WEP source leg",
            "old_status": "SOURCE_ACQUISITION_REQUIRED",
            "new_status": "SOURCE_WORLD_TUBE_METADATA_STAGED_NUMERIC_KERNEL_REQUIRED",
            "filled": False,
            "reason": "next step must acquire/reconstruct g/T arrays or close point-source theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SLG1421_0_point_source_theorem",
            "gate": "parent point-source theorem",
            "opens_if": "PST1421_6 becomes proved with universal/common source and finite-source error bound",
            "current_status": "CLOSED_THEOREM_NOT_PROVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SLG1421_1_numeric_source_proxy",
            "gate": "numeric g/T source proxy",
            "opens_if": "satellite position/velocity, gravity model, pointing, and exact segment masks produce gx/gz/Sxx/Sxz arrays",
            "current_status": "CLOSED_NUMERIC_ARRAYS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SLG1421_2_source_composition",
            "gate": "relative source composition/source-charge map",
            "opens_if": "Earth/source composition map or theorem-zero common-mode source leg is available",
            "current_status": "CLOSED_COMPOSITION_MAP_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SLG1421_3_calibration_guard",
            "gate": "no measured-G absorption",
            "opens_if": "calibration split proves only common mode is absorbed",
            "current_status": "GUARD_ACTIVE_EQUATION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SLG1421_4_overall",
            "gate": "M_WEP,q source leg executability",
            "opens_if": "SLG1421_0 or SLG1421_1+2+3 open",
            "current_status": "SOURCE_LEG_NOT_EXECUTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1421_0_theorem_verdict",
            "decision": "do not promote calibrated point-source theorem",
            "reason": "official g(O_sat) proxy is common-source form only; relative qbar source factorization/composition and finite-source error are missing",
            "next_action": "keep point-source route as conditional theorem target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1421_1_metadata_verdict",
            "decision": "stage source-worldtube metadata rows as partial nonclaim inputs",
            "reason": "1071 source-backed kernel skeleton supplies source proxy form and segment metadata, not numeric arrays",
            "next_action": "acquire/reconstruct numeric gx/gz/Sxx/Sxz source-leg arrays for a pilot segment",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1421_2_best_next",
            "decision": "target MICROSCOPE source-leg data schema or gx/gz/Sxx/Sxz pilot next",
            "reason": "numeric source proxy arrays are the first executable component for M_WEP,q if the theorem remains unsigned",
            "next_action": "try data portal schema/file inventory; if blocked, write reconstruction inputs for one SUEP segment",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1421_0_point_source_claim",
            "claim": "Earth/source leg is theorem-reduced to a calibrated point source",
            "allowed": False,
            "reason": "PST1421_6 is POINT_SOURCE_THEOREM_NOT_PROVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1421_1_source_leg_numeric",
            "claim": "M_WEP,q source leg is numeric/executable",
            "allowed": False,
            "reason": "g/T arrays, source profile, composition, and calibration split are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1421_2_WEP_pass",
            "claim": "WEP source projection can be scored or passed",
            "allowed": False,
            "reason": CLAIM_CEILING,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1421_3_shortcuts",
            "claim": "point-source by taste, tau=1, measured-G absorption, or qbar=0 convention is allowed",
            "allowed": False,
            "reason": "all shortcut routes remain forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1421_0_1422",
            "target_doc": "1422-Y5-R10-RAB-MICROSCOPE-source-leg-data-schema-or-gxgzS-kernel-pilot.md",
            "target_script": "scripts/Y5_R10_RAB_MICROSCOPE_source_leg_data_schema_or_gxgzS_kernel_pilot.py",
            "task": "try to acquire the CMSM/MICROSCOPE data schema or reconstruct a pilot gx,gz,Sxx,Sxz source-leg kernel for one SUEP segment from sourced orbit/attitude/gravity inputs; if blocked, write an exact blocker ledger",
            "success_condition": "numeric source-leg arrays are acquired/reconstructed for a pilot segment, or every missing data/schema input is source-ready and claim-blocked",
            "do_not_claim": "WEP pass; numeric tau_WEP without arrays; guessed masks/phases; measured-G absorption; point-source by taste",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1421_1_parallel_theory",
            "target_doc": "future-relative-source-factorization-theorem.md",
            "target_script": "future_theory_route",
            "task": "try to prove rho_qbar(x) factorizes as a common-mode source profile from the parent source-current owner",
            "success_condition": "relative source composition is theorem-zero/common-mode, or retained as finite source-composition residual",
            "do_not_claim": "source composition cancels by assumption",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    metadata_rows: list[dict[str, Any]],
    status_rows: list[dict[str, Any]],
    acceptance_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        POINT_SOURCE_THEOREM_PATH,
        WORLDTUBE_METADATA_PATH,
        SOURCE_LEG_STATUS_PATH,
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
        "VAL1421_0_sources",
        all(row["path_exists"] and row["anchor_found"] for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1421_1_theorem",
        any(row["theorem_id"] == "PST1421_6_verdict" and row["current_result"] == "POINT_SOURCE_THEOREM_NOT_PROVED" for row in theorem_rows),
        "point-source theorem attempt fails honestly",
    )
    required_metadata = {
        "WSW1421_0_official_source_proxy_form",
        "WSW1421_2_Earth_gravity_model",
        "WSW1421_3_source_composition_charge",
        "WSW1421_8_verdict",
    }
    add(
        "VAL1421_2_metadata",
        required_metadata.issubset({row["metadata_id"] for row in metadata_rows}) and all(row["claim_allowed"] is False for row in metadata_rows),
        "source-worldtube metadata rows exist and remain nonclaim",
    )
    add(
        "VAL1421_3_status",
        any(row["status_id"] == "SLS1421_4_verdict" and row["new_status"] == "SOURCE_WORLD_TUBE_METADATA_STAGED_NUMERIC_KERNEL_REQUIRED" for row in status_rows),
        "source leg status update keeps M_WEP,q non-executable",
    )
    add(
        "VAL1421_4_acceptance",
        any(row["gate_id"] == "SLG1421_4_overall" and row["current_status"] == "SOURCE_LEG_NOT_EXECUTABLE" for row in acceptance_rows),
        "acceptance gate blocks source-leg executability",
    )
    add(
        "VAL1421_5_claim_refusal",
        all(row["allowed"] is False and row["claim_allowed"] is False for row in claim_rows),
        "point-source, numeric source leg, WEP pass, and shortcut claims are refused",
    )
    add(
        "VAL1421_6_decision",
        any(row["decision_id"] == "DEC1421_2_best_next" and "source-leg data schema" in row["decision"] for row in decision_rows_),
        "decision ledger selects source-leg data schema or gx/gz/Sxx/Sxz pilot next",
    )
    add(
        "VAL1421_7_next_target",
        any(row["next_id"] == "NEXT1421_0_1422" for row in next_rows),
        "next target 1422 is staged",
    )
    add(
        "VAL1421_8_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1421_9_overall",
        True,
        "1421 fails point-source theorem and stages WEP source-worldtube metadata as nonclaim",
    )
    if any(row["status"] == "FAIL" for row in rows):
        for row in rows:
            if row["check_id"] == "VAL1421_9_overall":
                row["status"] = "FAIL"
                row["detail"] = "one or more 1421 validation checks failed"
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    metadata_rows: list[dict[str, Any]],
    status_rows: list[dict[str, Any]],
    acceptance_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    doc = f"""# 1421 - WEP Source-Worldtube Or Parent Point-Source Theorem

**Current verdict:** the calibrated point-source/source-worldtube theorem is not proved. The official MICROSCOPE source proxy form `g(O_sat)` / `T(O_sat)` is source-backed as a readout-kernel object, but this does not by itself remove relative `qbar_source_weight`, source composition, finite-source/multipole, calibration, or numeric-array requirements.

**Discipline move:** the WEP source leg now has source-worldtube metadata rows. They are partial, nonclaim rows: official proxy form and segment metadata are staged, while Earth gravity/source profile, source composition, finite-source error, and numeric gx/gz/Sxx/Sxz arrays remain missing.

**Status:** `{STATUS}`

## Source Register

{md_table(sources)}

## Parent Point-Source Theorem Attempt

{md_table(theorem_rows)}

## WEP Source-Worldtube Metadata Rows

{md_table(metadata_rows)}

## M_WEP Source-Leg Status Update

{md_table(status_rows)}

## Source-Leg Acceptance Gate

{md_table(acceptance_rows)}

## Decision Ledger

{md_table(decision_rows_)}

## Claim Gate

{md_table(claim_rows)}

## Next Target

{md_table(next_rows)}

## Validation

{md_table(validation_rows_)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    theorem_rows = point_source_theorem_rows()
    metadata_rows = worldtube_metadata_rows()
    status_rows = source_leg_status_rows()
    acceptance_rows = acceptance_gate_rows()
    decision_rows_ = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()
    validation_rows_ = validation_rows(
        sources,
        theorem_rows,
        metadata_rows,
        status_rows,
        acceptance_rows,
        decision_rows_,
        claim_rows,
        next_rows,
    )

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(POINT_SOURCE_THEOREM_PATH, theorem_rows)
    write_csv(WORLDTUBE_METADATA_PATH, metadata_rows)
    write_csv(SOURCE_LEG_STATUS_PATH, status_rows)
    write_csv(ACCEPTANCE_GATE_PATH, acceptance_rows)
    write_csv(DECISION_PATH, decision_rows_)
    write_csv(CLAIM_GATE_PATH, claim_rows)
    write_csv(NEXT_TARGET_PATH, next_rows)
    write_csv(VALIDATION_PATH, validation_rows_)
    write_doc(sources, theorem_rows, metadata_rows, status_rows, acceptance_rows, decision_rows_, claim_rows, next_rows, validation_rows_)

    if any(row["status"] != "PASS" for row in validation_rows_):
        raise SystemExit("1421 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
