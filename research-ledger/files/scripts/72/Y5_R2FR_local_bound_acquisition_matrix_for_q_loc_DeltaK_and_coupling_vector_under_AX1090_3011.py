from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3011"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3011-Y5-R2FR-local-bound-acquisition-matrix-for-q_loc-DeltaK-and-coupling-vector-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3011_SOURCE_REGISTER.csv",
    "matrix": RESIDUALS / "P8_Y5_R2FR_3011_LOCAL_BOUND_ACQUISITION_MATRIX.csv",
    "required_sources": RESIDUALS / "P8_Y5_R2FR_3011_REQUIRED_SOURCE_FILES.csv",
    "projection_quantities": RESIDUALS / "P8_Y5_R2FR_3011_PROJECTION_QUANTITIES.csv",
    "first_rows": RESIDUALS / "P8_Y5_R2FR_3011_FIRST_NONCLAIM_ROWS.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_3011_ARENA_BLOCKER_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3011_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3011_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3011_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3011_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3011_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "matrix_copy": LOCAL_BOUNDS / "local_bound_acquisition_matrix_3011_NONCLAIM.csv",
    "required_sources_copy": LOCAL_BOUNDS / "required_source_files_3011_NONCLAIM.csv",
    "first_rows_copy": LOCAL_BOUNDS / "first_nonclaim_local_rows_3011_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3011_R10_FIRST_SOURCE_BACKED_BOUND_ROWS_NEXT_NONCLAIM.csv",
}

SOURCE_PATHS = {
    "SRC3011_00_3010_doc": ROOT / "3010-Y5-R2FR-first-Gamma-Khat-response-operator-row-or-q_loc-coupling-bound-interface-under-AX1090.md",
    "SRC3011_01_3010_arena_matrix": RESIDUALS / "P8_Y5_R2FR_3010_LOCAL_ARENA_ACQUISITION_MATRIX.csv",
    "SRC3011_02_3010_q_loc_interface": RESIDUALS / "P8_Y5_R2FR_3010_QLOC_COUPLING_BOUND_INTERFACE.csv",
    "SRC3011_03_R10_bound_contract_2702": RESIDUALS / "P8_Y5_R2FR_2702_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv",
    "SRC3011_04_R10_anchor_gate_2410": RESIDUALS / "P8_Y5_PARENT_QLOC_2410_BOUND_CURVE_ADMISSION_GATE.csv",
    "SRC3011_05_PPN_bound_interface_2513": RESIDUALS / "P8_Y5_NO_SHADOW_2513_PPN_BOUND_INTERFACE.csv",
    "SRC3011_06_PPN_normalized_inputs_1640": RESIDUALS / "P8_Y5_PARENT_QLOC_1640_NORMALIZED_PPN_BOUND_INPUTS.csv",
    "SRC3011_07_WEP_input_pack_1899": RESIDUALS / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
    "SRC3011_08_clock_bound_fill_2675": RESIDUALS / "P8_Y5_R2FR_2675_SPECIES_CLOCK_FIRST_BOUND_FILL_NONCLAIM.csv",
    "SRC3011_09_clock_tau_pack_2599": RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv",
    "SRC3011_10_clock_bound_import_1321": RESIDUALS / "P8_Y5_R10_1321_CLOCK_BOUND_IMPORT.csv",
    "SRC3011_11_clock_alpha_sensitivity_646": RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
    "SRC3011_12_orbit_template_1735": ROOT
    / "source-intake"
    / "microscope"
    / "branch_locked_wep"
    / "residuals"
    / "R2FR_1735_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE.csv",
    "SRC3011_13_measured_GM_guard_2513": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Measured_GM_no_absorb_guard_2513_NONCLAIM.csv",
    "SRC3011_14_GM_transfer_PiM_2595": LOCAL_BOUNDS / "GM_transfer_PiM_component_rows_2595_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        read_rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": {
                "SRC3011_00_3010_doc": "parent checkpoint narrative and guardrails",
                "SRC3011_01_3010_arena_matrix": "3010 arena handoff",
                "SRC3011_02_3010_q_loc_interface": "q_loc/Delta_K/coupling bound interface",
                "SRC3011_03_R10_bound_contract_2702": "R10 bound curve digitization contract",
                "SRC3011_04_R10_anchor_gate_2410": "R10 anchor-only admission gate",
                "SRC3011_05_PPN_bound_interface_2513": "existing PPN comparator rows",
                "SRC3011_06_PPN_normalized_inputs_1640": "PPN missing-input ledger",
                "SRC3011_07_WEP_input_pack_1899": "WEP executable input pack ledger",
                "SRC3011_08_clock_bound_fill_2675": "clock/species first-fill ledger",
                "SRC3011_09_clock_tau_pack_2599": "clock tau source pack",
                "SRC3011_10_clock_bound_import_1321": "clock bound import ledger",
                "SRC3011_11_clock_alpha_sensitivity_646": "clock alpha sensitivity source ledger",
                "SRC3011_12_orbit_template_1735": "PPN/WEP/clock/orbit source-pack template",
                "SRC3011_13_measured_GM_guard_2513": "measured-GM no-absorb guard",
                "SRC3011_14_GM_transfer_PiM_2595": "GM/source-normalization obstruction rows",
            }[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

arena_matrix = [
    base(
        {
            "matrix_id": "LAM3011_0_R10",
            "arena": "R10 short-range",
            "observable": "alpha(lambda)",
            "input_from_3010": "ARENA3010_0_R10; BI3010_0_q_DeltaK; BI3010_3_coupling_vector",
            "required_projection_quantities": "K_R10(lambda,x); lambda_X; C_q_to_alpha; source charge normalization; q_loc profile/support",
            "required_bound_data": "full source-backed alpha_bound(lambda) curve or machine-readable table; anchors are smoke-only",
            "current_evidence": "2702 contract plus 2410 Eot-Wash 2020/2007 alpha=1 threshold anchors",
            "units_needed": "lambda in m; alpha dimensionless; source kernel declared in same normalization as q_loc",
            "blocker_status": "MISSING_FULL_CURVE_AND_QLOC_TO_YUKAWA_MAP",
            "first_acquisition_row": "FNR3011_0_R10_2020_anchor_smoke; FNR3011_1_R10_2007_anchor_smoke; FNR3011_2_R10_full_curve_requirement",
            "priority": "1",
            "next_action": "acquire/digitize Eot-Wash 2020 full curve or official table, then dry-run schema without scoring MTS",
        }
    ),
    base(
        {
            "matrix_id": "LAM3011_1_PPN",
            "arena": "PPN",
            "observable": "gamma-1; beta-1; alpha_i; zeta_i; xi",
            "input_from_3010": "ARENA3010_1_PPN; ROP3010_0_PPN_GK_lowered_operator",
            "required_projection_quantities": "K_PPN^a_nu(x,xprime); weak-field gauge; source frame; fixed measured-GM convention; q_loc radial/profile normalization",
            "required_bound_data": "current source-backed PPN comparator table and matching MTS prediction vector in same convention",
            "current_evidence": "2513 comparator rows exist; 1640 says source mass, boundary, gamma source, and no-cancellation inputs remain missing",
            "units_needed": "dimensionless PPN residual vector; fixed-GM convention stated",
            "blocker_status": "MISSING_K_PPN_AND_SOURCE_NORMALIZATION",
            "first_acquisition_row": "FNR3011_3_PPN_comparator_smoke",
            "priority": "2",
            "next_action": "bind PPN comparator rows to K_PPN prediction rows and no-absorb measured-GM guard",
        }
    ),
    base(
        {
            "matrix_id": "LAM3011_2_clocks_EM",
            "arena": "clocks/EM",
            "observable": "redshift; clock drift; alpha_EM variation",
            "input_from_3010": "ARENA3010_2_clocks_EM; BI3010_3_coupling_vector",
            "required_projection_quantities": "P_clock; tau_clock_time; dln(alpha_EM)/dXhat or theorem-zero EM owner; clock species sensitivities",
            "required_bound_data": "clock drift/redshift bounds with species/readout convention and time units",
            "current_evidence": "2675, 2599, 1321 and 646 ledgers exist; parent b_alpha and tau_clock_time remain unsigned",
            "units_needed": "dimensionless redshift or yr^-1 drift; alpha variation dimensionless per time",
            "blocker_status": "MISSING_ALPHA_OWNER_AND_TAU_CLOCK_MAP",
            "first_acquisition_row": "FNR3011_4_clock_alpha_smoke",
            "priority": "3",
            "next_action": "derive no alpha_EM(X) vertex or source b_alpha and tau_clock_time before any clock score",
        }
    ),
    base(
        {
            "matrix_id": "LAM3011_3_WEP",
            "arena": "WEP/composition",
            "observable": "eta_AB; source/test composition residual",
            "input_from_3010": "ARENA3010_3_WEP; BI3010_2_matter_source; BI3010_3_coupling_vector",
            "required_projection_quantities": "P_WEP_eta_AB; material tensor; source worldtube/composition; tau_WEP; force/readout map; parent residual vector",
            "required_bound_data": "MICROSCOPE or equivalent official bound/readout plus material/source maps",
            "current_evidence": "1899 has MICROSCOPE PDF bound anchor cached, but executable rows WIP1899_1 through WIP1899_7 missing",
            "units_needed": "dimensionless eta after m s^-2 readout normalization",
            "blocker_status": "BOUND_ANCHOR_PRESENT_EXECUTABLE_INPUTS_MISSING",
            "first_acquisition_row": "FNR3011_5_WEP_input_pack_smoke",
            "priority": "4",
            "next_action": "fill official material/source/readout maps or prove theorem reductions before WEP scoring",
        }
    ),
    base(
        {
            "matrix_id": "LAM3011_4_orbital",
            "arena": "orbital/source mass",
            "observable": "extra acceleration; source-mass drift; orbital residuals",
            "input_from_3010": "ARENA3010_4_orbital; BI3010_0_q_DeltaK; BI3010_4_total_no_cancellation",
            "required_projection_quantities": "P_orbital_accel; tau_orbital; source mass frame; q_loc acceleration map; no orbital-GM denominator absorption",
            "required_bound_data": "orbit residual threshold/readout in same source frame plus measured-GM guard",
            "current_evidence": "1735 orbit source-pack template, 2513 measured-GM guard and 2595 GM-transfer rows exist; no executable orbital prediction row",
            "units_needed": "m s^-2 acceleration residual or dimensionless post-GM vector with stated denominator",
            "blocker_status": "MISSING_ORBITAL_ACCELERATION_MAP_AND_GM_DENOMINATOR_OWNER",
            "first_acquisition_row": "FNR3011_6_orbital_source_pack_smoke",
            "priority": "5",
            "next_action": "derive acceleration projection without importing orbital GM as the residual denominator",
        }
    ),
    base(
        {
            "matrix_id": "LAM3011_5_total",
            "arena": "all local arenas",
            "observable": "local GR/Newton/PPN/WEP/R10 gate",
            "input_from_3010": "ARENA3010_5_total; BI3010_4_total_no_cancellation",
            "required_projection_quantities": "all arena projections plus absolute no-cancellation envelope",
            "required_bound_data": "theorem-zero rows or source-backed numeric bounds for every retained residual",
            "current_evidence": "component families are schema-ready but not theorem-zero or numeric-complete",
            "units_needed": "one declared residual norm per arena plus common bookkeeping convention",
            "blocker_status": "TOTAL_LOCAL_CLAIM_BLOCKED",
            "first_acquisition_row": "FNR3011_7_total_no_claim_guard",
            "priority": "6",
            "next_action": "complete R10 first, then PPN, before broad local-GR promotion attempt",
        }
    ),
]

required_sources = [
    base(
        {
            "source_req_id": "RSF3011_0_R10_full_curve",
            "arena": "R10 short-range",
            "artifact_or_target": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "existing_source_ref": str(SOURCE_PATHS["SRC3011_03_R10_bound_contract_2702"]),
            "requirement": "positive numeric alpha_bound(lambda) rows from Eot-Wash 2020 full curve or official table",
            "current_status": "MISSING_FULL_CURVE",
            "units": "lambda m; alpha dimensionless",
            "valid_row_policy": "valid_for_claim may become true only for full-curve/source-backed rows, never for threshold anchors alone",
            "next_action": "digitize curve with figure/table provenance and extraction confidence",
        }
    ),
    base(
        {
            "source_req_id": "RSF3011_1_R10_anchor_smoke",
            "arena": "R10 short-range",
            "artifact_or_target": "anchor-only rows from 2410 gate",
            "existing_source_ref": str(SOURCE_PATHS["SRC3011_04_R10_anchor_gate_2410"]),
            "requirement": "keep Eot-Wash 2020/2007 threshold anchors as nonclaim schema smoke rows",
            "current_status": "ANCHORS_PRESENT_NONCURVE",
            "units": "lambda m; alpha dimensionless",
            "valid_row_policy": "valid_for_claim=false because interpolation/envelope scoring needs a curve",
            "next_action": "copy anchors only to smoke row ledger, not live claim file",
        }
    ),
    base(
        {
            "source_req_id": "RSF3011_2_R10_projection",
            "arena": "R10 short-range",
            "artifact_or_target": "q_loc_to_Yukawa_source_map_3012_candidate.csv",
            "existing_source_ref": str(SOURCE_PATHS["SRC3011_02_3010_q_loc_interface"]),
            "requirement": "derive K_R10(lambda,x), lambda_X and source charge normalization from q_loc/Delta_K/coupling rows",
            "current_status": "MISSING_QLOC_TO_YUKAWA_MAP",
            "units": "declared q_loc source units to dimensionless alpha",
            "valid_row_policy": "prediction row stays false until parent coefficients and kernel are sourced",
            "next_action": "build R10 dry-run schema and fail closed when kernel/source normalization missing",
        }
    ),
    base(
        {
            "source_req_id": "RSF3011_3_PPN_bounds",
            "arena": "PPN",
            "artifact_or_target": "PPN comparator rows",
            "existing_source_ref": str(SOURCE_PATHS["SRC3011_05_PPN_bound_interface_2513"]),
            "requirement": "reverify comparator rows before scoring and bind to same fixed-GM gauge/readout convention",
            "current_status": "COMPARATOR_PRESENT_NOT_MTS_PREDICTION",
            "units": "dimensionless",
            "valid_row_policy": "bound row alone is not a prediction row",
            "next_action": "connect comparator to K_PPN kernel and measured-GM no-absorb guard",
        }
    ),
    base(
        {
            "source_req_id": "RSF3011_4_PPN_projection",
            "arena": "PPN",
            "artifact_or_target": "K_PPN_response_kernel_3012_or_later.csv",
            "existing_source_ref": str(SOURCE_PATHS["SRC3011_06_PPN_normalized_inputs_1640"]),
            "requirement": "same-frame source mass, boundary guard, gamma source and no-cancellation vector",
            "current_status": "MISSING_SOURCE_NORMALIZATION_AND_KERNELS",
            "units": "dimensionless residual vector plus source mass/frame metadata",
            "valid_row_policy": "all local PPN rows remain nonclaim while any MISSING_* remains",
            "next_action": "derive or source K_PPN and source-normalization inputs",
        }
    ),
    base(
        {
            "source_req_id": "RSF3011_5_clock_pack",
            "arena": "clocks/EM",
            "artifact_or_target": "clock_alpha_tau_bound_pack_3012_or_later.csv",
            "existing_source_ref": str(SOURCE_PATHS["SRC3011_08_clock_bound_fill_2675"]),
            "requirement": "b_alpha, tau_clock_time, clock readout convention and species sensitivity rows",
            "current_status": "MISSING_PARENT_ALPHA_OWNER_AND_TAU_CLOCK",
            "units": "yr^-1 or dimensionless per declared time coordinate",
            "valid_row_policy": "comparison-side bounds can be present while prediction rows remain invalid",
            "next_action": "prove EM owner zero or source b_alpha and tau_clock_time",
        }
    ),
    base(
        {
            "source_req_id": "RSF3011_6_WEP_pack",
            "arena": "WEP/composition",
            "artifact_or_target": "P_WEP_executable_input_pack_3012_or_later.csv",
            "existing_source_ref": str(SOURCE_PATHS["SRC3011_07_WEP_input_pack_1899"]),
            "requirement": "source worldtube, source composition, material tensor, readout arrays, force map, tau_WEP and parent residuals",
            "current_status": "BOUND_ANCHOR_ONLY_INPUT_PACK_NOT_EXECUTABLE",
            "units": "dimensionless eta after acceleration normalization",
            "valid_row_policy": "MICROSCOPE anchor does not make MTS WEP score-ready",
            "next_action": "fill WIP1899_1 through WIP1899_7 or theorem-reduce them",
        }
    ),
    base(
        {
            "source_req_id": "RSF3011_7_orbital_pack",
            "arena": "orbital/source mass",
            "artifact_or_target": "orbital_acceleration_source_pack_3012_or_later.csv",
            "existing_source_ref": str(SOURCE_PATHS["SRC3011_12_orbit_template_1735"]),
            "requirement": "orbital residual threshold, acceleration map, same-frame source mass and no orbital-GM denominator absorption",
            "current_status": "TEMPLATE_PRESENT_EXECUTABLE_ROW_MISSING",
            "units": "m s^-2 or dimensionless fixed-GM vector",
            "valid_row_policy": "cannot divide by fitted orbital GM unless denominator ownership is proved",
            "next_action": "derive q_loc acceleration map and bind to measured-GM guard",
        }
    ),
]

projection_quantities = [
    base(
        {
            "quantity_id": "PQ3011_0_K_R10",
            "arena": "R10 short-range",
            "symbol": "K_R10(lambda,x)",
            "definition_needed": "Yukawa/source projection kernel mapping q_loc support to alpha(lambda)",
            "required_units": "kernel units inverse to q_loc volume/source units, final alpha dimensionless",
            "current_status": "MISSING_DERIVED_KERNEL",
            "source_anchor": "BI3010_0_q_DeltaK; BI3010_3_coupling_vector",
        }
    ),
    base(
        {
            "quantity_id": "PQ3011_1_lambda_X",
            "arena": "R10 short-range",
            "symbol": "lambda_X",
            "definition_needed": "range scale of retained local residual mode or spectral envelope",
            "required_units": "m",
            "current_status": "MISSING_PARENT_RANGE_MAP",
            "source_anchor": "2702 R10 profile/input schema",
        }
    ),
    base(
        {
            "quantity_id": "PQ3011_2_C_q_to_alpha",
            "arena": "R10 short-range",
            "symbol": "C_q_to_alpha",
            "definition_needed": "normalization converting q_loc/Delta_K/coupling residual to dimensionless Yukawa alpha",
            "required_units": "dimensionless after declared source normalization",
            "current_status": "MISSING_SOURCE_CHARGE_NORMALIZATION",
            "source_anchor": "3010 q_loc coupling interface",
        }
    ),
    base(
        {
            "quantity_id": "PQ3011_3_K_PPN",
            "arena": "PPN",
            "symbol": "K_PPN^a_nu",
            "definition_needed": "weak-field kernel mapping q_loc source vector to each PPN residual",
            "required_units": "dimensionless residual per q_loc unit",
            "current_status": "MISSING_KERNEL_AND_GAUGE",
            "source_anchor": "2513 PPN response kernel requirement",
        }
    ),
    base(
        {
            "quantity_id": "PQ3011_4_P_clock",
            "arena": "clocks/EM",
            "symbol": "P_clock",
            "definition_needed": "clock/readout projection including observed time vector and species sensitivity",
            "required_units": "yr^-1 or dimensionless per clock observable",
            "current_status": "MISSING_TAU_CLOCK_AND_ALPHA_OWNER",
            "source_anchor": "2675;2599;1321;646",
        }
    ),
    base(
        {
            "quantity_id": "PQ3011_5_P_WEP_eta",
            "arena": "WEP/composition",
            "symbol": "P_WEP_eta_AB",
            "definition_needed": "differential acceleration/material/source projection from parent residual vector",
            "required_units": "dimensionless eta",
            "current_status": "MISSING_MATERIAL_SOURCE_READOUT_MAPS",
            "source_anchor": "1899 WEP input pack",
        }
    ),
    base(
        {
            "quantity_id": "PQ3011_6_P_orbital",
            "arena": "orbital/source mass",
            "symbol": "P_orbital_accel",
            "definition_needed": "map q_loc residual to observable acceleration/orbit residual without absorbing into fitted GM",
            "required_units": "m s^-2 or declared dimensionless fixed-GM vector",
            "current_status": "MISSING_ACCELERATION_MAP",
            "source_anchor": "1735 source pack; 2513 measured-GM guard; 2595 GM transfer",
        }
    ),
    base(
        {
            "quantity_id": "PQ3011_7_total_no_cancellation",
            "arena": "all local arenas",
            "symbol": "epsilon_local_total_abs",
            "definition_needed": "absolute sum of q_DeltaK, Ward/Euler, matter/coupling and projection tails",
            "required_units": "declared residual norm per arena",
            "current_status": "COMPONENTS_MISSING_TOTAL_BLOCKED",
            "source_anchor": "BI3010_4_total_no_cancellation",
        }
    ),
]

first_rows = [
    base(
        {
            "row_id": "FNR3011_0_R10_2020_anchor_smoke",
            "arena": "R10 short-range",
            "row_type": "bound_anchor_smoke",
            "source": "Eot-Wash 2020 PRL / PubMed 32216404 / arXiv:2002.11761 as recorded in 2410",
            "lambda_value": "3.86e-5",
            "lambda_units": "m",
            "alpha_bound": "1.0",
            "bound_units": "dimensionless",
            "status": "ANCHOR_ONLY_NON_CURVE",
            "blocker": "cannot interpolate arbitrary lambda/support from one threshold anchor",
            "next_action": "replace or supplement with full curve rows in 3012",
        }
    ),
    base(
        {
            "row_id": "FNR3011_1_R10_2007_anchor_smoke",
            "arena": "R10 short-range",
            "row_type": "bound_anchor_smoke",
            "source": "Eot-Wash 2007 PRL / arXiv:hep-ph/0611184 as recorded in 2410",
            "lambda_value": "5.6e-5",
            "lambda_units": "m",
            "alpha_bound": "1.0",
            "bound_units": "dimensionless",
            "status": "ANCHOR_ONLY_NON_CURVE",
            "blocker": "continuity anchor only; not modern dense bound curve",
            "next_action": "keep for provenance continuity only",
        }
    ),
    base(
        {
            "row_id": "FNR3011_2_R10_full_curve_requirement",
            "arena": "R10 short-range",
            "row_type": "required_full_curve",
            "source": "future digitized Eot-Wash 2020 figure/table",
            "lambda_value": "MISSING_DENSE_GRID",
            "lambda_units": "m",
            "alpha_bound": "MISSING_ALPHA_BOUND_CURVE",
            "bound_units": "dimensionless",
            "status": "MISSING_FULL_CURVE",
            "blocker": "R10 scoring requires positive numeric curve rows and q_loc-to-alpha projection",
            "next_action": "3012 source-backed curve acquisition or blocker ledger",
        }
    ),
    base(
        {
            "row_id": "FNR3011_3_PPN_comparator_smoke",
            "arena": "PPN",
            "row_type": "comparator_bundle_smoke",
            "source": "2513 PPN bound interface",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "alpha_bound": "not_applicable",
            "bound_units": "dimensionless PPN residuals",
            "status": "COMPARATOR_PRESENT_NOT_MTS_PREDICTION",
            "blocker": "K_PPN/source normalization/no-cancellation vector missing",
            "next_action": "bind comparator to actual MTS prediction vector",
        }
    ),
    base(
        {
            "row_id": "FNR3011_4_clock_alpha_smoke",
            "arena": "clocks/EM",
            "row_type": "clock_bound_bundle_smoke",
            "source": "2675/2599/1321/646 clock ledgers",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "alpha_bound": "not_applicable",
            "bound_units": "yr^-1 or dimensionless redshift",
            "status": "COMPARISON_SIDE_ONLY_NONCLAIM",
            "blocker": "b_alpha and tau_clock_time missing",
            "next_action": "derive EM owner zero or source clock projection",
        }
    ),
    base(
        {
            "row_id": "FNR3011_5_WEP_input_pack_smoke",
            "arena": "WEP/composition",
            "row_type": "WEP_input_pack_smoke",
            "source": "1899 MICROSCOPE WEP input pack",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "alpha_bound": "not_applicable",
            "bound_units": "dimensionless eta",
            "status": "BOUND_ANCHOR_PRESENT_EXECUTABLE_INPUTS_MISSING",
            "blocker": "source/material/readout/tau/parent residual rows missing",
            "next_action": "fill WIP1899_1-WIP1899_7 or theorem-reduce",
        }
    ),
    base(
        {
            "row_id": "FNR3011_6_orbital_source_pack_smoke",
            "arena": "orbital/source mass",
            "row_type": "orbital_source_pack_smoke",
            "source": "1735 orbit source-pack template; 2513 measured-GM guard; 2595 GM-transfer rows",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "alpha_bound": "not_applicable",
            "bound_units": "m s^-2 or dimensionless fixed-GM residual",
            "status": "TEMPLATE_PRESENT_EXECUTABLE_ROW_MISSING",
            "blocker": "acceleration map and denominator ownership missing",
            "next_action": "derive q_loc acceleration map without orbital-GM shortcut",
        }
    ),
    base(
        {
            "row_id": "FNR3011_7_total_no_claim_guard",
            "arena": "all local arenas",
            "row_type": "no_claim_guard",
            "source": "3010 BI3010_4_total_no_cancellation",
            "lambda_value": "not_applicable",
            "lambda_units": "not_applicable",
            "alpha_bound": "not_applicable",
            "bound_units": "per-arena residual norm",
            "status": "TOTAL_LOCAL_CLAIM_BLOCKED",
            "blocker": "component residuals not theorem-zero or source-backed numeric",
            "next_action": "complete R10 and PPN first",
        }
    ),
]

blockers = [
    base(
        {
            "blocker_id": "BLK3011_0_R10_curve",
            "arena": "R10 short-range",
            "blocking_condition": "MISSING_FULL_CURVE",
            "why_it_matters": "threshold anchors cannot decide a predicted range or spectral envelope",
            "unblocks_when": "dense source-backed alpha_bound(lambda) curve or official machine-readable table is present",
        }
    ),
    base(
        {
            "blocker_id": "BLK3011_1_R10_projection",
            "arena": "R10 short-range",
            "blocking_condition": "MISSING_QLOC_TO_YUKAWA_MAP",
            "why_it_matters": "MTS prediction cannot be compared to alpha(lambda) until q_loc normalization is owned",
            "unblocks_when": "K_R10, lambda_X and C_q_to_alpha are derived or source-backed",
        }
    ),
    base(
        {
            "blocker_id": "BLK3011_2_PPN_kernel",
            "arena": "PPN",
            "blocking_condition": "MISSING_K_PPN_AND_GAUGE",
            "why_it_matters": "PPN bounds are vector components in a fixed weak-field convention",
            "unblocks_when": "K_PPN prediction rows exist in same source/frame/readout convention as comparator rows",
        }
    ),
    base(
        {
            "blocker_id": "BLK3011_3_clock_owner",
            "arena": "clocks/EM",
            "blocking_condition": "MISSING_ALPHA_OWNER_AND_TAU_CLOCK",
            "why_it_matters": "clock/EM readout can otherwise hide the coupling problem",
            "unblocks_when": "no alpha_EM(X) vertex is proved or finite b_alpha and tau_clock_time rows are sourced",
        }
    ),
    base(
        {
            "blocker_id": "BLK3011_4_WEP_executability",
            "arena": "WEP/composition",
            "blocking_condition": "WIP1899_1_TO_WIP1899_7_MISSING",
            "why_it_matters": "MICROSCOPE bound alone is not an MTS WEP prediction",
            "unblocks_when": "source/material/readout/force/tau/residual inputs are filled or theorem-reduced",
        }
    ),
    base(
        {
            "blocker_id": "BLK3011_5_orbital_GM",
            "arena": "orbital/source mass",
            "blocking_condition": "MISSING_ORBITAL_ACCELERATION_MAP_AND_GM_DENOMINATOR_OWNER",
            "why_it_matters": "using fitted orbital GM as the denominator could erase the residual being tested",
            "unblocks_when": "acceleration projection is derived and measured-GM absorption guard passes",
        }
    ),
    base(
        {
            "blocker_id": "BLK3011_6_total_no_cancellation",
            "arena": "all local arenas",
            "blocking_condition": "NO_CANCELLATION_ENVELOPE_NOT_NUMERIC",
            "why_it_matters": "local GR/Newton reduction must not rely on hidden cancellations between unrelated residuals",
            "unblocks_when": "each retained component is theorem-zero or bounded in an absolute residual norm",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3011_0_source_register",
            "gate": "all cited local source refs exist",
            "result": all(boolish(row["exists"]) for row in source_register),
            "claim_impact": "hard fail if false",
            "notes": "3011 only cites existing local ledgers as evidence; future targets may be missing artifacts",
        }
    ),
    base(
        {
            "gate_id": "GATE3011_1_nonclaim_policy",
            "gate": "every generated arena/input row remains nonclaim",
            "result": True,
            "claim_impact": "required",
            "notes": "3011 is acquisition plumbing, not evidence of local-GR pass",
        }
    ),
    base(
        {
            "gate_id": "GATE3011_2_R10_anchor_policy",
            "gate": "R10 threshold anchors never become valid curve rows",
            "result": True,
            "claim_impact": "required",
            "notes": "anchors are preserved as smoke/provenance only",
        }
    ),
    base(
        {
            "gate_id": "GATE3011_3_projection_required",
            "gate": "no bound row is score-ready without same-arena projection quantities",
            "result": True,
            "claim_impact": "required",
            "notes": "matrix explicitly separates bound data from q_loc/Delta_K/coupling projection",
        }
    ),
    base(
        {
            "gate_id": "GATE3011_4_GM_guard",
            "gate": "orbital/PPN lanes cannot absorb residuals into fitted GM",
            "result": True,
            "claim_impact": "required",
            "notes": "2513 measured-GM no-absorb guard is linked before any orbital/PPN score",
        }
    ),
    base(
        {
            "gate_id": "GATE3011_5_local_claims",
            "gate": "local GR/Newton/PPN/WEP/R10 pass allowed",
            "result": False,
            "claim_impact": "must remain false",
            "notes": "component projections and full bound rows are still missing",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3011_0_status",
            "decision": "3011 converts 3010 into a source-acquisition matrix, not a claim.",
            "rationale": "The local bridge now has explicit q_loc/Delta_K/coupling interfaces, but every arena still lacks at least one required projection or source-backed bound artifact.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3011_1_priority",
            "decision": "R10 is selected as the first executable acquisition lane.",
            "rationale": "R10 has the cleanest observable target alpha(lambda), existing source hierarchy, and a well-defined curve-vs-anchor blocker.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3011_2_PPN_second",
            "decision": "PPN remains second because it is the real local-GR guardrail.",
            "rationale": "PPN catches fake GR recovery, but needs a source-frame/gauge kernel before it can score MTS.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3011_3_total_branch",
            "decision": "Total local-GR/Newton branch stays blocked until no-cancellation residual envelope is theorem-zero or numeric.",
            "rationale": "A serious field-theory claim cannot rest on cancellation between Delta_K, Ward, matter and readout terms.",
            "claim_allowed_after_decision": False,
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3011_0_3012",
            "priority": "selected_primary",
            "target_doc": "3012-Y5-R2FR-R10-first-source-backed-bound-rows-and-dryrun-schema-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_R10_first_source_backed_bound_rows_and_dryrun_schema_under_AX1090_3012.py",
            "mission": "Acquire or stage real source-backed R10 alpha_bound(lambda) rows and dry-run the q_loc-to-alpha schema while keeping all MTS prediction rows nonclaim unless parent coefficients are sourced.",
            "success_condition": "full curve rows or an explicit blocker ledger exist; anchors remain valid_for_claim=false; dry-run refuses to score without K_R10, lambda_X and source normalization.",
            "fallback_if_fail": "write blocker ledger naming the exact figure/table/access problem and keep 3011 matrix as the controlling route map.",
            "guardrails": "no R10 pass claim; no anchor-only curve claim; no hidden coupling; no bound inversion; no GitHub; no formalization-workbench edits",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["matrix"], arena_matrix)
write_csv(OUTPUTS["required_sources"], required_sources)
write_csv(OUTPUTS["projection_quantities"], projection_quantities)
write_csv(OUTPUTS["first_rows"], first_rows)
write_csv(OUTPUTS["blockers"], blockers)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("matrix_copy", "matrix"),
    ("required_sources_copy", "required_sources"),
    ("first_rows_copy", "first_rows"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3011_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
claim_false_rows = arena_matrix + required_sources + projection_quantities + first_rows + blockers + promotion_gates + decision + next_target
r10_numeric_anchors_ok = all(
    float(row["lambda_value"]) > 0 and float(row["alpha_bound"]) > 0
    for row in first_rows[:2]
)

validation_rows = [
    {
        "validation_id": "VAL3011_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3011_01_csv_parse",
        "passed": all(csv_ok(path) for path in list(OUTPUTS.values()) if path.suffix == ".csv"),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3011_02_r10_anchors_positive",
        "passed": r10_numeric_anchors_ok,
        "requirement": "anchor smoke rows have positive numeric lambda and alpha values",
        "evidence": "FNR3011_0 and FNR3011_1",
    },
    {
        "validation_id": "VAL3011_03_no_claim_rows",
        "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in claim_false_rows),
        "requirement": "no 3011 row is valid for claim or claim allowed",
        "evidence": "base() claim fields",
    },
    {
        "validation_id": "VAL3011_04_anchor_only_not_curve",
        "passed": all(row["status"] == "ANCHOR_ONLY_NON_CURVE" and not boolish(row["valid_for_claim"]) for row in first_rows[:2]),
        "requirement": "R10 threshold anchors remain noncurve nonclaim rows",
        "evidence": "FNR3011_0 and FNR3011_1",
    },
    {
        "validation_id": "VAL3011_05_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in first_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "first nonclaim row ledger",
    },
    {
        "validation_id": "VAL3011_06_local_claims_blocked",
        "passed": not any(boolish(row.get("claim_allowed")) for row in claim_false_rows),
        "requirement": "local GR/Newton/PPN/WEP/R10 claim remains blocked",
        "evidence": "claim flags false across ledgers",
    },
    {
        "validation_id": "VAL3011_07_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3011_08_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3011_09_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3012-Y5-R2FR-R10"),
        "requirement": "next target selects R10 first source-backed acquisition",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3011_99_overall",
        "passed": overall_pass,
        "requirement": "all 3011 validation checks pass",
        "evidence": "aggregate of VAL3011_00 through VAL3011_09",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3011 — Local-Bound Acquisition Matrix for `q_loc`, `Delta_K`, and the Coupling Vector under AX1090

Status: `Y5_R2FR_3011_local_bound_acquisition_matrix_staged_R10_first_3012_next`

## Verdict

3011 turns the 3010 local-residual interface into a concrete acquisition board. It does **not** claim local GR, Newton, PPN, WEP, clock/EM or R10 success.

The useful gain is that the missing pieces are now split by arena instead of being one foggy phrase called "the coupling":

- R10 needs a real `alpha_bound(lambda)` curve **and** a `q_loc -> alpha(lambda)` normalization.
- PPN needs the weak-field response kernel and fixed measured-GM/source-frame convention.
- clocks/EM need the `alpha_EM` owner or theorem-zero plus `tau_clock`.
- WEP needs the executable material/source/readout/tau pack, not just the MICROSCOPE bound anchor.
- orbital tests need an acceleration projection that does not hide the residual inside fitted orbital GM.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Acquisition Matrix

{md_table(arena_matrix, ["matrix_id", "arena", "observable", "blocker_status", "first_acquisition_row", "priority"])}

## Required Source Files

{md_table(required_sources, ["source_req_id", "arena", "current_status", "units", "next_action"])}

## Projection Quantities

{md_table(projection_quantities, ["quantity_id", "arena", "symbol", "current_status", "required_units"])}

## First Nonclaim Rows

{md_table(first_rows, ["row_id", "arena", "row_type", "status", "blocker"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "arena", "blocking_condition", "unblocks_when"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["matrix"]}`
- `{OUTPUTS["required_sources"]}`
- `{OUTPUTS["projection_quantities"]}`
- `{OUTPUTS["first_rows"]}`
- `{OUTPUTS["blockers"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["matrix_copy"]}`
- `{BRANCH_OUTPUTS["required_sources_copy"]}`
- `{BRANCH_OUTPUTS["first_rows_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No local-GR/Newton/PPN/WEP/R10 pass claim.
- No anchor-only R10 curve claim.
- No hidden-coupling cancellation.
- No bound inversion.
- No EH-only import.
- No orbital-GM denominator shortcut.
- No GitHub action.
- No `formalization-workbench` edits.
"""

DOC.write_text(doc, encoding="utf-8")
