from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2777-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2777_SOURCE_REGISTER.csv",
    "external": MTS / "P8_Y5_R2FR_2777_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv",
    "eta": MTS / "P8_Y5_R2FR_2777_ETA_READOUT_FORMULA_ROWS.csv",
    "orbit": MTS / "P8_Y5_R2FR_2777_ORBIT_KERNEL_SOURCE_ROWS.csv",
    "readout": MTS / "P8_Y5_R2FR_2777_READOUT_FILL_MATRIX_UPDATE.csv",
    "impact": MTS / "P8_Y5_R2FR_2777_TAU_IMPACT_LEDGER.csv",
    "candidate": MTS / "P8_Y5_R2FR_2777_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2777_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2777_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2777_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2777_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2777_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2777_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2777_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2777_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "readout_queue": RAB_QUEUE / "JR2777_MICROSCOPE_ETA_READOUT_NONCLAIM.csv",
    "orbit_queue": RAB_QUEUE / "JR2777_MICROSCOPE_ORBIT_KERNEL_PARTIAL_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_ETA_READOUT_2777_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_eta_readout_2777_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2777_FULL_ORBIT_OR_SOURCE_WORLDTUBE_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2777_00_2776_next", "2776_next", MTS / "P8_Y5_R2FR_2776_NEXT_TARGET.csv", "NEXT2776_0_2777", "current handoff into eta/readout acquisition"),
        ("SRC2777_01_2776_tau_source", "2776_tau_source", MTS / "P8_Y5_R2FR_2776_FIRST_REAL_TAU_SOURCE_ROW.csv", "WTS2776_0_MICROSCOPE_eta_source_charge_proxy", "current first MICROSCOPE provenance row"),
        ("SRC2777_02_2776_provenance", "2776_provenance", MTS / "P8_Y5_R2FR_2776_MICROSCOPE_PROVENANCE_LEDGER.csv", "PROV2776_0_R1_WEP_source_charge", "current provenance ledger"),
        ("SRC2777_03_2776_fill", "2776_fill", MTS / "P8_Y5_R2FR_2776_READOUT_FILL_MATRIX.csv", "RFM2776_1_eta_formula", "current partial eta formula row"),
        ("SRC2777_04_2776_requirements", "2776_requirements", MTS / "P8_Y5_R2FR_2776_REMAINING_TAU_REQUIREMENTS.csv", "REQ2776_1_readout_formula", "current remaining tau/readout requirements"),
        ("SRC2777_05_2775_orbit", "2775_orbit", MTS / "P8_Y5_R2FR_2775_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv", "ORB2775_2_eta_convention", "current orbit/readout requirements"),
        ("SRC2777_06_2775_force", "2775_force", MTS / "P8_Y5_R2FR_2775_OBSERVED_FRAME_FORCE_MAP.csv", "FRM2775_1_eta_mapping", "current observed-frame eta map requirement"),
        ("SRC2777_07_2775_tau_pack", "2775_tau_pack", MTS / "P8_Y5_R2FR_2775_TAU_WEP_ACQUISITION_PACK.csv", "TAP2775_2_eta_readout", "current tau acquisition pack"),
        ("SRC2777_08_2775_worldtube", "2775_worldtube", MTS / "P8_Y5_R2FR_2775_SOURCE_WORLDTUBE_REQUIREMENTS.csv", "SWT2775_5_verdict", "source worldtube gap"),
        ("SRC2777_09_1061_material", "1061_material", MTS / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "Ti/Pt material convention"),
        ("SRC2777_10_1070_doc", "1070_doc", WORK / "1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md", "ETA1070_0_formula", "prior R10 eta/readout acquisition"),
        ("SRC2777_11_1070_external", "1070_external", MTS / "P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv", "EXT1070_0_CQG_eta_formula", "prior external source ledger"),
        ("SRC2777_12_1070_eta", "1070_eta", MTS / "P8_Y5_R10_1070_ETA_READOUT_FORMULA_ROWS.csv", "ETA1070_4_verdict", "prior eta formula rows"),
        ("SRC2777_13_1070_orbit", "1070_orbit", MTS / "P8_Y5_R10_1070_ORBIT_KERNEL_SOURCE_ROWS.csv", "ORK1070_5_verdict", "prior partial orbit rows"),
        ("SRC2777_14_1070_readout", "1070_readout", MTS / "P8_Y5_R10_1070_READOUT_FILL_MATRIX_UPDATE.csv", "RFM1070_5_full_orbit_kernel", "prior readout fill update"),
        ("SRC2777_15_708_wep", "708_wep", MTS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "WEP source/test charge vector gap"),
        ("SRC2777_16_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE bound source rows"),
        ("SRC2777_17_393_common", "393_common", WORK / "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard"),
    ]
    rows = []
    for row_id, source_key, path, needle, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": exists and needle in text,
            "source_role": role,
        }))
    return rows


def build_external_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"external_id": "EXT2777_0_CQG_eta_formula", "doi": "10.1088/1361-6382/ac84be", "source_lines": "1070 external ledger; arXiv/CQG source context", "extracted_item": "eta(A,B)=2(a_A-a_B)/(a_A+a_B)", "source_backed": True}),
        nonclaim({"external_id": "EXT2777_1_CQG_result_readout", "doi": "10.1088/1361-6382/ac84be", "source_lines": "1070 external ledger PDF lines 1216-1223", "extracted_item": "eta(Ti,Pt) is identified with delta_x; final value is [-1.5 +/- 2.3(stat) +/- 1.5(syst)]e-15", "source_backed": True}),
        nonclaim({"external_id": "EXT2777_2_CQG_measurement_axis", "doi": "10.1088/1361-6382/ac84be", "source_lines": "1070 external ledger PDF lines 341-346", "extracted_item": "test-mass accelerations are sampled at 4 Hz and differential acceleration is computed along the sensitive X axis", "source_backed": True}),
        nonclaim({"external_id": "EXT2777_3_CQG_orbit_segments", "doi": "10.1088/1361-6382/ac84be", "source_lines": "1070 external ledger PDF lines 1226-1231", "extracted_item": "SUREF Pt/Pt used 13 segments/598 orbits/41 days; SUEP Pt/Ti used 19 segments/1362 orbits/94 days", "source_backed": True}),
        nonclaim({"external_id": "EXT2777_4_CQG_analysis_band", "doi": "10.1088/1361-6382/ac84be", "source_lines": "1070 external ledger PDF lines 918-924", "extracted_item": "parameter estimation uses bands around f_EP and 2 f_EP; wider-domain check increases uncertainty but does not noticeably shift parameters", "source_backed": True}),
        nonclaim({"external_id": "EXT2777_5_CQG_data_availability", "doi": "10.1088/1361-6382/ac84be", "source_lines": "1070 external ledger PDF lines 1274-1276", "extracted_item": "science data are available from https://cmsm-ds.onera.fr/", "source_backed": True}),
        nonclaim({"external_id": "EXT2777_6_PRL_eta_bound_anchor", "doi": "10.1103/PhysRevLett.129.121102", "source_lines": "arXiv:2209.15487 abstract and local bound row", "extracted_item": "Ti/Pt final result supplies the source-backed 2.8e-15 WEP bound anchor already imported in 2776", "source_backed": True}),
    ]


def build_eta_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({"eta_id": "ETA2777_0_formula", "formula_or_item": "eta_AB = 2(a_A-a_B)/(a_A+a_B)", "units": "dimensionless", "status": "SOURCE_BACKED_FORMULA_FILLED", "MTS_impact": "observable convention acquired; not a tau_WEP prediction"}),
        nonclaim({"eta_id": "ETA2777_1_delta_x_identification", "formula_or_item": "eta(Ti,Pt) approximately equals measured delta_x in the MICROSCOPE convention", "units": "dimensionless", "status": "SOURCE_BACKED_READOUT_IDENTIFICATION_FILLED", "MTS_impact": "links the official eta observable to the instrument differential channel"}),
        nonclaim({"eta_id": "ETA2777_2_result_value", "formula_or_item": f"Ti/Pt eta measured={bound.get('measured_value', '-1.5e-15')}; one_sigma={bound.get('one_sigma', '2.74590604355e-15')}; upper_bound={bound.get('upper_bound', '2.8e-15')}", "units": "dimensionless", "status": "SOURCE_BACKED_RESULT_CONTEXT_FILLED", "MTS_impact": "bound row remains a nonclaim comparator; direct row R0_identity_coframe_direct remains separate"}),
        nonclaim({"eta_id": "ETA2777_3_sign_pair_convention", "formula_or_item": "A/B sign is source-backed for eta_AB, but not yet mapped onto MTS TA6V_minus_PtRh10 sign convention", "units": "dimensionless", "status": "PARTIAL_SIGN_CONTEXT_ONLY", "MTS_impact": "absolute-value score can use the bound, but signed model comparison still needs material/readout orientation"}),
        nonclaim({"eta_id": "ETA2777_4_verdict", "formula_or_item": "eta formula and delta_x readout are filled; tau_WEP and direct product are not", "units": "dimensionless", "status": "FORMULA_FILLED_NOT_TAU", "MTS_impact": "this upgrades data plumbing, not local-GR/WEP closure"}),
    ]


def build_orbit_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"orbit_id": "ORK2777_0_sampling_axis", "component": "sample/readout axis", "source_backed_value": "4 Hz acceleration sampling; differential acceleration along sensitive X axis", "status": "SOURCE_BACKED_PARTIAL_READOUT_ROW", "missing_for_tau": "full map from parent residual to X-axis eta channel"}),
        nonclaim({"orbit_id": "ORK2777_1_segments_orbits", "component": "segment/orbit exposure", "source_backed_value": "SUEP Pt/Ti 19 segments, 1362 orbits, 94 days; SUREF Pt/Pt 13 segments, 598 orbits, 41 days", "status": "SOURCE_BACKED_PARTIAL_ORBIT_ROW", "missing_for_tau": "time-dependent orbit/attitude weights and source line-of-sight kernel"}),
        nonclaim({"orbit_id": "ORK2777_2_spin_session", "component": "spin/session planning", "source_backed_value": "analysis is organized around f_EP and 2f_EP bands; earlier session metadata references V2/V3 spin rates and long sessions", "status": "SOURCE_BACKED_PARTIAL_SPIN_ROW", "missing_for_tau": "machine-readable attitude/spin kernel"}),
        nonclaim({"orbit_id": "ORK2777_3_frequency_band", "component": "frequency-domain analysis band", "source_backed_value": "fit bands around f_EP and 2 f_EP", "status": "SOURCE_BACKED_PARTIAL_ANALYSIS_KERNEL", "missing_for_tau": "exact weighting/filter operator for an MTS predicted signal"}),
        nonclaim({"orbit_id": "ORK2777_4_data_availability", "component": "data portal", "source_backed_value": "https://cmsm-ds.onera.fr/", "status": "SOURCE_BACKED_DATA_PORTAL", "missing_for_tau": "downloaded data products, schema, and reproducible kernel extraction"}),
        nonclaim({"orbit_id": "ORK2777_5_verdict", "component": "orbit/averaging kernel verdict", "source_backed_value": "partial metadata acquired, not a full orbit/attitude/averaging kernel", "status": "PARTIAL_ORBIT_METADATA_NOT_TAU_KERNEL", "missing_for_tau": "full kernel or source-worldtube row"}),
    ]


def build_readout_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"fill_id": "RFM2777_0_eta_bound", "component": "MICROSCOPE eta bound", "current_status": "SOURCE_BACKED_BOUND_ANCHOR_PRESENT", "evidence_rows": "WTS2776_0; ETA2777_2", "blocks_claim": False}),
        nonclaim({"fill_id": "RFM2777_1_eta_formula", "component": "eta_AB formula", "current_status": "SOURCE_BACKED_FORMULA_FILLED", "evidence_rows": "ETA2777_0", "blocks_claim": False}),
        nonclaim({"fill_id": "RFM2777_2_delta_x", "component": "eta to delta_x readout identification", "current_status": "SOURCE_BACKED_READOUT_IDENTIFICATION_FILLED", "evidence_rows": "ETA2777_1", "blocks_claim": False}),
        nonclaim({"fill_id": "RFM2777_3_sampling_axis", "component": "4 Hz X-axis measurement row", "current_status": "SOURCE_BACKED_PARTIAL_READOUT_ROW", "evidence_rows": "ORK2777_0", "blocks_claim": True}),
        nonclaim({"fill_id": "RFM2777_4_orbit_metadata", "component": "orbit/segment metadata", "current_status": "SOURCE_BACKED_PARTIAL_ORBIT_ROW", "evidence_rows": "ORK2777_1; ORK2777_3", "blocks_claim": True}),
        nonclaim({"fill_id": "RFM2777_5_full_orbit_kernel", "component": "full orbit/attitude/averaging kernel", "current_status": "MISSING_FULL_KERNEL", "evidence_rows": "none", "blocks_claim": True}),
        nonclaim({"fill_id": "RFM2777_6_source_worldtube", "component": "Earth/source worldtube", "current_status": "MISSING_SOURCE_WORLDTUBE", "evidence_rows": "SWT2775_5_verdict", "blocks_claim": True}),
        nonclaim({"fill_id": "RFM2777_7_material_tensor", "component": "Ti/Pt material response tensor", "current_status": "MISSING_MATERIAL_TENSOR", "evidence_rows": "MCON1061_0_test_pair", "blocks_claim": True}),
        nonclaim({"fill_id": "RFM2777_8_direct_product", "component": "direct P_WEP product", "current_status": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL", "evidence_rows": "DWT2776_5_verdict", "blocks_claim": True}),
    ]


def build_impact_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"impact_id": "TAI2777_0_formula_does_not_define_tau", "new_input": "eta_AB formula", "impact": "defines the observable normalization only", "remaining_gap": "tau_WEP/source product still absent", "claim_policy": "no scoreable MTS prediction"}),
        nonclaim({"impact_id": "TAI2777_1_readout_axis_partial", "new_input": "4 Hz X-axis readout row", "impact": "constrains the observed channel", "remaining_gap": "no parent residual to X-axis projection operator", "claim_policy": "partial kernel only"}),
        nonclaim({"impact_id": "TAI2777_2_orbit_partial", "new_input": "segment/orbit/frequency metadata", "impact": "identifies exposure and analysis bands", "remaining_gap": "no machine-readable orbit/attitude/averaging kernel", "claim_policy": "partial source-backed acquisition"}),
        nonclaim({"impact_id": "TAI2777_3_no_unity_shortcut", "new_input": "bound plus formula", "impact": "does not license tau_WEP=1 or Delta_w=0", "remaining_gap": "direct product theorem or full projection kernel", "claim_policy": "shortcut forbidden"}),
        nonclaim({"impact_id": "TAI2777_4_verdict", "new_input": "2777 acquisition pack", "impact": "readout plumbing improved", "remaining_gap": "tau_WEP remains missing", "claim_policy": "WEP/local-GR claim remains blocked"}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2777_0_WEP_eta_formula_or_orbit_kernel_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL",
            "product_units": "dimensionless",
            "derivation_status": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL",
            "notes": "eta formula and partial orbit metadata do not define an MTS product",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2777_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": bound.get("upper_bound", "2.8e-15"),
            "bound_units": bound.get("units", "dimensionless"),
            "bound_type": "source_backed_upper_bound_anchor",
            "bound_valid_for_internal_runner": True,
        })
    ]


def run_product_runner(predictions: list[dict[str, Any]], bounds: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid_predictions = [
        row for row in predictions
        if row.get("valid_for_claim") is True
        and is_numeric(row.get("product_value"))
        and not has_missing_marker(row)
    ]
    valid_bounds = [
        row for row in bounds
        if row.get("bound_valid_for_internal_runner") is True
        and is_numeric(row.get("bound_value"))
        and float(str(row["bound_value"])) > 0.0
        and not has_missing_marker(row)
    ]
    comparisons = [
        nonclaim({"comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS", "comparison_status": "not_run", "pass_for_claim": False, "issues": "no valid MTS direct/tau WEP product prediction rows"})
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2777_0_WEP_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "claim_allowed": False,
            "expected_result": "reject eta/readout-only placeholder prediction and keep claim false",
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2777_0_eta_formula_acquired", "claim_component": "eta formula", "gate_pass": True, "claim_allowed": False, "reason": "source-backed observable definition, not an MTS prediction"}),
        nonclaim({"gate_id": "CG2777_1_orbit_metadata_partial", "claim_component": "orbit/readout metadata", "gate_pass": True, "claim_allowed": False, "reason": "partial metadata only; full kernel missing"}),
        nonclaim({"gate_id": "CG2777_2_full_orbit_kernel", "claim_component": "full orbit/attitude/averaging kernel", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_FULL_KERNEL"}),
        nonclaim({"gate_id": "CG2777_3_tau_WEP_numeric", "claim_component": "tau_WEP numeric/direct product", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL"}),
        nonclaim({"gate_id": "CG2777_4_product_runner", "claim_component": "WEP product runner", "gate_pass": False, "claim_allowed": False, "reason": "valid_prediction_rows=0"}),
        nonclaim({"gate_id": "CG2777_5_local_GR_WEP_claim", "claim_component": "local-GR/WEP pass", "gate_pass": False, "claim_allowed": False, "reason": "eta formula acquired but WEP product remains unscored"}),
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2777_0_readout_acquired", "decision": "eta formula and delta_x identification are source-backed nonclaim rows", "evidence": "ETA2777_0_formula; ETA2777_1_delta_x_identification", "consequence": "readout convention no longer the first blocker"}),
        nonclaim({"decision_id": "DEC2777_1_orbit_partial_only", "decision": "orbit/readout metadata is useful but not a tau kernel", "evidence": "ORK2777_5_verdict", "consequence": "do not score MTS against MICROSCOPE yet"}),
        nonclaim({"decision_id": "DEC2777_2_best_next", "decision": "move to full orbit kernel or source-worldtube acquisition", "evidence": "RFM2777_5_full_orbit_kernel; RFM2777_6_source_worldtube", "consequence": "2778 should try the first tau_WEP projection component"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2777_0_2778",
            "next_target": "2778-Y5-R2FR-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_full_orbit_kernel_or_source_worldtube_row_under_AX1090_2778.py",
            "objective": "acquire or derive the first full tau_WEP projection component: either an official MICROSCOPE orbit/attitude/averaging kernel usable in the eta readout map, or an Earth/source-worldtube row; keep product scoring blocked until all required tau/direct-product components exist",
            "include": "orbit ephemeris/attitude/averaging kernel; source worldtube profile; eta formula integration; material tensor; Xhat normalization; URL/DOI/data portal provenance; refusal gates",
            "exclude": "tau=1; Delta_w=0 by taste; measured-G absorption of relative weights; cancellation; public WEP/local-GR claim; GitHub; formalization edits",
        })
    ]


def copy_branch_outputs(
    external: list[dict[str, Any]],
    eta: list[dict[str, Any]],
    orbit: list[dict[str, Any]],
    readout: list[dict[str, Any]],
    impact: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    readout_rows = external + eta + readout + impact + gates
    orbit_rows = orbit + readout + candidate + gates
    beta_rows = eta + impact + next_rows
    microscope_rows = external + eta + orbit + readout + impact + candidate + bounds + next_rows
    specs = [
        ("BR2777_0_readout_queue", "readout", readout_rows, OUTPUTS["eta"], BRANCH_OUTPUTS["readout_queue"], "MICROSCOPE eta/readout nonclaim copy"),
        ("BR2777_1_orbit_queue", "orbit", orbit_rows, OUTPUTS["orbit"], BRANCH_OUTPUTS["orbit_queue"], "partial orbit kernel nonclaim copy"),
        ("BR2777_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["impact"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing eta readout copy"),
        ("BR2777_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE eta/readout acquisition copy"),
        ("BR2777_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next full orbit/source-worldtube target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("pass_for_claim", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    external = rows_by_name["external"]
    eta = rows_by_name["eta"]
    orbit = rows_by_name["orbit"]
    readout = rows_by_name["readout"]
    impact = rows_by_name["impact"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2777_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2777_1_external_provenance", any(row["external_id"] == "EXT2777_0_CQG_eta_formula" and row["source_backed"] is True for row in external) and any(row["external_id"] == "EXT2777_5_CQG_data_availability" for row in external), "CQG DOI and data portal recorded"),
        ("VAL2777_2_eta_formula_dimensionless", any(row["eta_id"] == "ETA2777_0_formula" and row["units"] == "dimensionless" and row["status"] == "SOURCE_BACKED_FORMULA_FILLED" for row in eta), "eta formula filled as dimensionless"),
        ("VAL2777_3_bound_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and bounds[0]["bound_valid_for_internal_runner"] is True, "bound import has positive numeric value"),
        ("VAL2777_4_orbit_partial_not_kernel", any(row["orbit_id"] == "ORK2777_5_verdict" and row["status"] == "PARTIAL_ORBIT_METADATA_NOT_TAU_KERNEL" for row in orbit), "orbit acquisition remains partial"),
        ("VAL2777_5_full_kernel_still_missing", any(row["fill_id"] == "RFM2777_5_full_orbit_kernel" and row["current_status"] == "MISSING_FULL_KERNEL" for row in readout), "full kernel is not silently filled"),
        ("VAL2777_6_tau_still_missing", any(row["impact_id"] == "TAI2777_4_verdict" and row["remaining_gap"] == "tau_WEP remains missing" for row in impact), "tau verdict remains blocked"),
        ("VAL2777_7_prediction_nonclaim_missing", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "prediction row stays nonclaim and missing"),
        ("VAL2777_8_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "runner reports no valid prediction rows and claim false"),
        ("VAL2777_9_claim_gates_safe", all(row["claim_allowed"] is False for row in gates) and any(row["gate_id"] == "CG2777_0_eta_formula_acquired" and row["gate_pass"] is True for row in gates), "claim gates allow source acquisition only as nonclaim plumbing"),
        ("VAL2777_10_next_target", any(row["row_id"] == "NEXT2777_0_2778" and "full-orbit-kernel" in row["next_target"] for row in next_rows), "next target selects full orbit kernel or source-worldtube acquisition"),
        ("VAL2777_11_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2777_12_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2777_13_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2777_14_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2777_15_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2777_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2777_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2777 ports the MICROSCOPE eta/readout formula acquisition into the current R2/f(R) branch, records source-backed eta definition, delta_x readout identification, partial X-axis/orbit/frequency metadata and data portal, keeps full orbit kernel/source worldtube/material tensor/direct product missing, refuses eta-only WEP scoring, blocks WEP/local-GR claims, and selects full orbit kernel or source-worldtube row as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2777 - Y5 R2/f(R): MICROSCOPE eta Readout Formula Or Orbit-Kernel Acquisition Under AX1090",
        "## Private Verdict\n\n2777 closes a real plumbing gap: the official MICROSCOPE eta definition and delta_x readout identification are now source-backed in the live R2/f(R) branch. It does not close the WEP/local-GR branch, because the full tau_WEP projection, source worldtube, material tensor, and direct parent product are still absent.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## External MICROSCOPE Source Ledger\n\n" + markdown_table(rows_by_name["external"], ["external_id", "doi", "source_lines", "extracted_item", "source_backed", "valid_for_claim"]),
        "## Eta Readout Rows\n\n" + markdown_table(rows_by_name["eta"], ["eta_id", "formula_or_item", "units", "status", "MTS_impact", "valid_for_claim"]),
        "## Orbit / Readout Kernel Source Rows\n\n" + markdown_table(rows_by_name["orbit"], ["orbit_id", "component", "source_backed_value", "status", "missing_for_tau", "valid_for_claim"]),
        "## Readout Fill Matrix Update\n\n" + markdown_table(rows_by_name["readout"], ["fill_id", "component", "current_status", "evidence_rows", "blocks_claim", "valid_for_claim"]),
        "## Tau Impact Ledger\n\n" + markdown_table(rows_by_name["impact"], ["impact_id", "new_input", "impact", "remaining_gap", "claim_policy", "valid_for_claim"]),
        "## Nonclaim Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "derivation_status", "notes", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "bound_valid_for_internal_runner", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "evidence", "consequence", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nGood plumbing, no victory lap. The observable is less fuzzy now: eta formula, delta_x readout, partial X-axis/orbit metadata, and data portal are recorded. But the full kernel that would turn an MTS parent residual into a MICROSCOPE eta prediction is still missing.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    external = build_external_rows()
    eta = build_eta_rows()
    orbit = build_orbit_rows()
    readout = build_readout_rows()
    impact = build_impact_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decisions()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("external", external), ("eta", eta), ("orbit", orbit),
        ("readout", readout), ("impact", impact), ("candidate", candidate), ("bounds", bounds),
        ("runner", runner), ("comparisons", comparisons), ("gates", gates), ("decision", decision),
        ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(external, eta, orbit, readout, impact, candidate, bounds, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "external": external,
        "eta": eta,
        "orbit": orbit,
        "readout": readout,
        "impact": impact,
        "candidate": candidate,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2777_OVERALL")
    print(f"2777 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
