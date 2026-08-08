from __future__ import annotations

import csv
import shutil
from collections import defaultdict
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
DOC = WORK / "2782-Y5-R2FR-WEP-parent-material-source-map-or-official-CMSM-import-gate-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2782_SOURCE_REGISTER.csv",
    "inputs": MTS / "P8_Y5_R2FR_2782_EXISTING_WEP_INPUT_STATUS.csv",
    "toy": MTS / "P8_Y5_R2FR_2782_TOY_MATERIAL_VECTOR_FROM_651.csv",
    "contract": MTS / "P8_Y5_R2FR_2782_PARENT_PRODUCT_CONTRACT_UPDATE.csv",
    "derivation": MTS / "P8_Y5_R2FR_2782_PARENT_MAP_DERIVATION_ATTEMPT.csv",
    "owners": MTS / "P8_Y5_R2FR_2782_COUPLING_OWNER_GATES.csv",
    "import_gate": MTS / "P8_Y5_R2FR_2782_OFFICIAL_CMSM_IMPORT_GATE.csv",
    "candidate": MTS / "P8_Y5_R2FR_2782_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2782_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2782_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2782_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2782_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2782_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2782_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2782_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2782_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_queue": RAB_QUEUE / "JR2782_WEP_PARENT_PRODUCT_CONTRACT_NONCLAIM.csv",
    "toy_queue": RAB_QUEUE / "JR2782_TOY_MATERIAL_VECTOR_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_PARENT_MAP_GATE_2782_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_parent_map_gate_2782_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2782_PARENT_COUPLING_OWNER_THEOREM_NEXT.csv",
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def source_row(row_id: str, source_key: str, path: Path, needle: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    exists = path.exists()
    return nonclaim({
        "row_id": row_id,
        "source_key": source_key,
        "source_path": str(path),
        "exists": exists,
        "needle": needle,
        "needle_found": exists and needle in text,
        "source_role": role,
    })


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2782_00_2781_next", "2781_next", MTS / "P8_Y5_R2FR_2781_NEXT_TARGET.csv", "NEXT2781_0_2782", "current handoff into parent material/source map gate"),
        ("SRC2782_01_2781_validation", "2781_validation", MTS / "P8_Y5_BRR545_2781_VALIDATION.csv", "VAL2781_OVERALL", "current validation baseline"),
        ("SRC2782_02_2781_replacement", "2781_replacement", MTS / "P8_Y5_R2FR_2781_REPLACEMENT_GATES.csv", "RG2781_2_material_source_map", "current parent material/source blocker"),
        ("SRC2782_03_2781_tau", "2781_tau", MTS / "P8_Y5_R2FR_2781_TAU_SHAPE_STATUS.csv", "TAUSHAPE2781_2_physics_tau", "current physical tau blocker"),
        ("SRC2782_04_1061_material", "1061_material", MTS / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "Ti/Pt convention and alpha smoke charge"),
        ("SRC2782_05_651_material", "651_material", MTS / "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv", "MM651_TA6V_V", "nominal alloy composition for toy vector only"),
        ("SRC2782_06_1068_material_req", "1068_material_req", MTS / "P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv", "MAT1068_5_verdict", "full material response not acquired"),
        ("SRC2782_07_1068_worldtube_req", "1068_worldtube_req", MTS / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv", "SWT1068_5_verdict", "source worldtube not acquired"),
        ("SRC2782_08_1062_parent", "1062_parent", MTS / "P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_6_verdict", "parent product theorem not closed"),
        ("SRC2782_09_1066_scalar", "1066_scalar", MTS / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "source scalar exclusion conditional"),
        ("SRC2782_10_1067_action", "1067_action", MTS / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "action-scale owner conditional"),
        ("SRC2782_11_708_map", "708_map", MTS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "source/test charge vector missing"),
        ("SRC2782_12_2779_schema", "2779_schema", MTS / "P8_Y5_R2FR_2779_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv", "ARR2779_3_gx", "official CMSM array import contract"),
        ("SRC2782_13_1077_precedent", "1077_precedent", WORK / "1077-Y5-R10-parent-WEP-coupling-owner-theorem-or-material-vector-source-row.md", "Coupling-owner theorem attempt", "R10 precedent for next theorem-owner route"),
        ("SRC2782_14_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_existing_input_rows() -> list[dict[str, Any]]:
    material_convention = read_csv_rows(MTS / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv")
    delta_q = next((row for row in material_convention if row.get("row_id") == "MCON1061_1_delta_Q_alpha"), {})
    return [
        nonclaim({"input_id": "IN2782_0_TiPt_pair", "object": "MICROSCOPE Ti/Pt pair", "current_value_or_status": "TA6V_minus_PtRh10", "source": "MCON1061_0_test_pair", "gap_remaining": "does not define parent response vector"}),
        nonclaim({"input_id": "IN2782_1_alpha_smoke_charge", "object": "Delta_Q_alpha_Coulomb_abs", "current_value_or_status": delta_q.get("value", "0.001989808886825"), "source": "MCON1061_1_delta_Q_alpha", "gap_remaining": "not full Ti/Pt material tensor and not parent-derived"}),
        nonclaim({"input_id": "IN2782_2_nominal_alloy_table", "object": "PtRh10 and TA6V nominal alloy composition", "current_value_or_status": "5 source rows parsed", "source": "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv", "gap_remaining": "not isotope/chemical/material tensor and not source-backed enough for WEP claim"}),
        nonclaim({"input_id": "IN2782_3_source_worldtube", "object": "Earth/source leg", "current_value_or_status": "SOURCE_WORLDTUBE_NOT_ACQUIRED", "source": "SWT1068_5_verdict", "gap_remaining": "source profile/composition/common-mode theorem missing"}),
        nonclaim({"input_id": "IN2782_4_CMSM_arrays", "object": "official MICROSCOPE gx/gz/Sxx/Sxz arrays", "current_value_or_status": "MISSING_OFFICIAL_ARRAYS", "source": "ARR2779_3_gx; RG2781_0_official_arrays", "gap_remaining": "can be imported later, but does not by itself derive material/source coupling"}),
        nonclaim({"input_id": "IN2782_5_surrogate_matrix", "object": "surrogate design matrix", "current_value_or_status": "RANK_8_SMOKE_RUNNER_AVAILABLE", "source": "DIAG2781_1_rank", "gap_remaining": "pipeline diagnostic only; no physical tau_WEP"}),
    ]


def build_toy_material_vectors() -> list[dict[str, Any]]:
    rows = read_csv_rows(MTS / "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv")
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["material_id"]].append(row)

    def compute(material_id: str) -> dict[str, Any]:
        material_rows = grouped[material_id]
        q_z = sum(float(row["mass_fraction"]) * float(row["Z"]) / float(row["A_used"]) for row in material_rows)
        q_neutron = sum(float(row["mass_fraction"]) * (float(row["A_used"]) - 2.0 * float(row["Z"])) / float(row["A_used"]) for row in material_rows)
        z_mean = sum(float(row["mass_fraction"]) * float(row["Z"]) for row in material_rows)
        a_mean = sum(float(row["mass_fraction"]) * float(row["A_used"]) for row in material_rows)
        return {
            "source_rows": ";".join(row["material_model_id"] for row in material_rows),
            "q_Z_over_A_toy": q_z,
            "q_neutron_excess_toy": q_neutron,
            "Z_mean_toy": z_mean,
            "A_mean_toy": a_mean,
        }

    pt = compute("PtRh10")
    ti = compute("TA6V")
    delta = {
        "source_rows": "MV2782_TA6V;MV2782_PtRh10;MCON1061_0_test_pair",
        "q_Z_over_A_toy": ti["q_Z_over_A_toy"] - pt["q_Z_over_A_toy"],
        "q_neutron_excess_toy": ti["q_neutron_excess_toy"] - pt["q_neutron_excess_toy"],
        "Z_mean_toy": ti["Z_mean_toy"] - pt["Z_mean_toy"],
        "A_mean_toy": ti["A_mean_toy"] - pt["A_mean_toy"],
    }
    return [
        nonclaim({"material_vector_id": "MV2782_PtRh10", "material_id": "PtRh10", **pt, "model_status": "TOY_FROM_651_NOMINAL_ALLOY_NOT_PARENT_RESPONSE"}),
        nonclaim({"material_vector_id": "MV2782_TA6V", "material_id": "TA6V", **ti, "model_status": "TOY_FROM_651_NOMINAL_ALLOY_NOT_PARENT_RESPONSE"}),
        nonclaim({"material_vector_id": "MV2782_delta_TA6V_minus_PtRh10", "material_id": "TA6V_minus_PtRh10", **delta, "model_status": "TOY_DIFFERENCE_NOT_DELTA_W_NOT_PARENT_DERIVED"}),
    ]


def build_contract_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"contract_id": "PWC2782_0_direct_product", "object": "direct WEP parent product", "formal_contract": "P_WEP = abs(Readout_MICROSCOPE[delta a_TA6V - delta a_PtRh10]) derived directly from delta S_parent", "current_status": "MISSING_DIRECT_PARENT_PRODUCT"}),
        nonclaim({"contract_id": "PWC2782_1_factorized_product", "object": "finite factorized WEP product", "formal_contract": "P_WEP = abs(<R_source^Earth, C_parent (R_TA6V - R_PtRh10)>_K)", "current_status": "FORMAL_SHAPE_STAGED_FACTORS_MISSING"}),
        nonclaim({"contract_id": "PWC2782_2_theorem_zero", "object": "universal metric/coframe theorem-zero", "formal_contract": "If C_parent has only universal metric/coframe coupling and no species/source labels, then R_TA6V - R_PtRh10 is invisible to WEP and P_WEP=0", "current_status": "CONDITIONAL_ZERO_UNSIGNED"}),
        nonclaim({"contract_id": "PWC2782_3_CMSM_import_gate", "object": "official array import alternative", "formal_contract": "CMSM official gx/gz/Sxx/Sxz arrays may replace surrogate kernel columns but do not replace R_source/R_material/C_parent", "current_status": "ARRAY_GATE_OPEN_COUPLING_GATE_CLOSED"}),
    ]


def build_derivation_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"attempt_id": "DER2782_0_material_response_definition", "claim": "define material response vector from parent matter action", "result": "DEFINITION_SHARPENED_NOT_DERIVED", "gap": "parent fields/coupling basis X_I and mass/current normalization owner are not signed"}),
        nonclaim({"attempt_id": "DER2782_1_source_leg_definition", "claim": "derive Earth/source response vector", "result": "SOURCE_LEG_FORM_ONLY", "gap": "source worldtube/profile/composition and common-mode theorem missing"}),
        nonclaim({"attempt_id": "DER2782_2_coupling_owner", "claim": "one parent coupling owner C_parent controls material and source legs", "result": "OWNER_REQUIRED_NOT_FOUND", "gap": "source-scalar exclusion and action-scale owner remain conditional in 1066/1067"}),
        nonclaim({"attempt_id": "DER2782_3_toy_material_vector", "claim": "use 651 alloy table to create a placeholder material vector", "result": "TOY_VECTOR_AVAILABLE_NONCLAIM", "gap": "toy vector is not Delta_w, not full material tensor, and not parent-derived"}),
        nonclaim({"attempt_id": "DER2782_4_zero_branch", "claim": "close WEP by theorem-zero rather than finite product", "result": "BEST_DERIVATION_ROUTE_BUT_UNSIGNED", "gap": "must prove parent object-language/current/action-measure owner"}),
        nonclaim({"attempt_id": "DER2782_5_verdict", "claim": "parent material/source map derivation", "result": "NOT_DERIVED_CURRENT_CORPUS", "gap": "exact contract staged; coupling-owner theorem is next"}),
    ]


def build_owner_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "OWN2782_0_parent_object_language", "owner_object": "parent coupling basis X_I", "current_status": "MISSING_PARENT_COUPLING_BASIS", "blocks": "R_A^I and R_source^I definitions"}),
        nonclaim({"gate_id": "OWN2782_1_species_blind_measure", "owner_object": "action-scale/measure owner", "current_status": "CONDITIONAL_NOT_PARENT_DERIVED", "blocks": "theorem-zero WEP closure"}),
        nonclaim({"gate_id": "OWN2782_2_current_owner", "owner_object": "current/source normalization", "current_status": "MISSING_CURRENT_OWNER", "blocks": "source-only weight exclusion"}),
        nonclaim({"gate_id": "OWN2782_3_material_tensor", "owner_object": "Ti/Pt material response tensor", "current_status": "TOY_VECTOR_ONLY", "blocks": "finite WEP product"}),
        nonclaim({"gate_id": "OWN2782_4_source_worldtube", "owner_object": "Earth/source response", "current_status": "MISSING_SOURCE_WORLDTUBE", "blocks": "finite WEP product"}),
        nonclaim({"gate_id": "OWN2782_5_CMSM_arrays", "owner_object": "official MICROSCOPE readout arrays", "current_status": "MISSING_OFFICIAL_ARRAYS", "blocks": "empirical readout scoring but not parent coupling derivation"}),
    ]


def build_import_gate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"import_id": "IMP2782_0_official_arrays", "artifact": "CMSM gx/gz/Sxx/Sxz arrays", "current_status": "NOT_IMPORTED", "effect_if_imported": "replaces surrogate kernel columns in 2781 design matrix", "remaining_after_import": "parent material/source map and coupling owner still required"}),
        nonclaim({"import_id": "IMP2782_1_exact_masks", "artifact": "exact MICROSCOPE segment masks", "current_status": "NOT_IMPORTED", "effect_if_imported": "replaces all-unmasked surrogate rows", "remaining_after_import": "official acceleration/readout and parent product still required"}),
        nonclaim({"import_id": "IMP2782_2_kernel_score", "artifact": "official-kernel WEP design matrix", "current_status": "NOT_BUILDABLE", "effect_if_imported": "allows data-side score runner", "remaining_after_import": "MTS prediction still invalid until P_WEP or tau_WEP product is derived"}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2782_0_WEP_parent_material_source_map_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_MATERIAL_SOURCE_MAP_AND_OFFICIAL_ARRAYS",
            "product_units": "dimensionless",
            "derivation_status": "CONTRACT_STAGED_PRODUCT_MISSING",
            "notes": "toy material vector and surrogate matrix do not define a parent WEP product",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2782_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": bound.get("upper_bound", "2.8e-15"),
            "bound_units": bound.get("units", "dimensionless"),
            "bound_type": "source_backed_upper_bound_anchor",
            "source_row_id": "R1_WEP_source_charge",
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
        nonclaim({"comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS", "comparison_status": "not_run", "pass_for_claim": False, "issues": "no valid MTS tau_WEP/direct-product prediction rows"})
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2782_0_WEP_parent_map_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "claim_allowed": False,
            "expected_result": "reject missing parent material/source map and keep claim false",
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2782_0_toy_material_vector", "claim_component": "toy Ti/Pt material vector", "gate_pass": True, "claim_allowed": False, "reason": "toy vector is useful but not parent response"}),
        nonclaim({"gate_id": "CG2782_1_parent_coupling_owner", "claim_component": "parent coupling owner", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_PARENT_COUPLING_BASIS_AND_OWNER"}),
        nonclaim({"gate_id": "CG2782_2_source_worldtube", "claim_component": "Earth/source response leg", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_SOURCE_WORLDTUBE"}),
        nonclaim({"gate_id": "CG2782_3_official_CMSM_arrays", "claim_component": "official MICROSCOPE kernel arrays", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_OFFICIAL_ARRAYS"}),
        nonclaim({"gate_id": "CG2782_4_product_runner", "claim_component": "WEP product runner", "gate_pass": False, "claim_allowed": False, "reason": "valid_prediction_rows=0"}),
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2782_0_parent_map_not_derived", "decision": "parent material/source response map is not derived by current corpus", "evidence": "DER2782_5_verdict; OWN2782_0_parent_object_language", "consequence": "WEP/local-GR product remains blocked"}),
        nonclaim({"decision_id": "DEC2782_1_toy_vector_staged", "decision": "toy Ti/Pt material vector is staged for nonclaim algebra tests", "evidence": "MV2782_delta_TA6V_minus_PtRh10", "consequence": "can test map plumbing but not score MICROSCOPE"}),
        nonclaim({"decision_id": "DEC2782_2_best_next", "decision": "best next move is the parent WEP coupling-owner theorem", "evidence": "DER2782_4_zero_branch; OWN2782_1_species_blind_measure", "consequence": "try to close theorem-zero or explicitly demote WEP finite branch to sourced-input route"}),
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2782_0_2783",
            "next_target": "2783-Y5-R2FR-parent-WEP-coupling-owner-theorem-or-material-vector-source-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_WEP_coupling_owner_theorem_or_material_vector_source_row_under_AX1090_2783.py",
            "objective": "attempt the parent WEP coupling-owner theorem: either prove ordinary matter has only universal metric/coframe coupling with species-blind action measure/current owner, yielding theorem-zero WEP, or explicitly require sourced finite material/source vectors",
            "include": "parent object-language typing; species-blind action measure; current/source normalization owner; Ti/Pt toy vector demotion; Earth/source leg; no measured-G absorption; product-runner refusal",
            "exclude": "Delta_w=0 by taste; tau=1; cancellation tuning; treating toy material vector as evidence; public WEP/local-GR claim; GitHub; formalization edits",
        })
    ]


def copy_branch_outputs(
    inputs: list[dict[str, Any]],
    toy: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    import_gate: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    contract_rows = inputs + contract + derivation + owners + candidate + gates
    toy_rows = toy + owners + candidate + gates
    beta_rows = contract + derivation + owners + next_rows
    microscope_rows = inputs + toy + contract + derivation + owners + import_gate + candidate + next_rows
    specs = [
        ("BR2782_0_contract_queue", "contract", contract_rows, OUTPUTS["contract"], BRANCH_OUTPUTS["contract_queue"], "WEP parent product contract nonclaim copy"),
        ("BR2782_1_toy_queue", "toy", toy_rows, OUTPUTS["toy"], BRANCH_OUTPUTS["toy_queue"], "toy material vector nonclaim copy"),
        ("BR2782_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["derivation"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing parent map gate copy"),
        ("BR2782_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE parent-map gate copy"),
        ("BR2782_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next parent coupling-owner theorem route"),
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
    inputs = rows_by_name["inputs"]
    toy = rows_by_name["toy"]
    contract = rows_by_name["contract"]
    derivation = rows_by_name["derivation"]
    owners = rows_by_name["owners"]
    import_gate = rows_by_name["import_gate"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2782_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2782_1_inputs_staged", len(inputs) >= 6 and any(row["input_id"] == "IN2782_4_CMSM_arrays" and row["current_value_or_status"] == "MISSING_OFFICIAL_ARRAYS" for row in inputs), "existing WEP inputs staged as nonclaim"),
        ("VAL2782_2_material_toy_vector", len(toy) == 3 and any(row["material_vector_id"] == "MV2782_delta_TA6V_minus_PtRh10" and row["model_status"] == "TOY_DIFFERENCE_NOT_DELTA_W_NOT_PARENT_DERIVED" for row in toy), "toy Ti/Pt material vectors computed and nonclaim"),
        ("VAL2782_3_product_contract", len(contract) == 4 and any(row["contract_id"] == "PWC2782_2_theorem_zero" for row in contract), "factorized/zero parent product contract staged"),
        ("VAL2782_4_derivation_not_closed", any(row["attempt_id"] == "DER2782_5_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in derivation), "derivation verdict remains not closed"),
        ("VAL2782_5_owner_gates_block", len(owners) == 6 and any(row["gate_id"] == "OWN2782_2_current_owner" and "MISSING" in row["current_status"] for row in owners), "parent coupling/source owner gates block claims"),
        ("VAL2782_6_import_gate_open_not_sufficient", len(import_gate) == 3 and any(row["import_id"] == "IMP2782_0_official_arrays" and row["remaining_after_import"].startswith("parent material/source map") for row in import_gate), "official import gate remains staged but nonclaim"),
        ("VAL2782_7_prediction_nonclaim_missing", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "prediction row remains missing parent map"),
        ("VAL2782_8_bound_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and float(str(bounds[0]["bound_value"])) > 0.0 and bounds[0]["bound_valid_for_internal_runner"] is True, "bound import is positive numeric"),
        ("VAL2782_9_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "runner reports no valid prediction rows and claim false"),
        ("VAL2782_10_claim_gates_safe", all(row["claim_allowed"] is False for row in gates) and any(row["gate_id"] == "CG2782_1_parent_coupling_owner" and row["gate_pass"] is False for row in gates), "all claim gates deny WEP/local-GR claim"),
        ("VAL2782_11_next_target", any(row["row_id"] == "NEXT2782_0_2783" and "parent-WEP-coupling-owner-theorem" in row["next_target"] for row in next_rows), "2783 handoff written"),
        ("VAL2782_12_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2782_13_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2782_14_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2782_15_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2782_16_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2782_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2782_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2782 does not derive the parent material/source response map. It stages the exact WEP product contract, computes a toy Ti/Pt material vector from the nominal alloy table, records coupling-owner/source-worldtube/CMSM gates, refuses WEP/local-GR scoring, and selects the parent WEP coupling-owner theorem as 2783.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2782 - Y5 R2/f(R): WEP Parent Material/Source Map Or Official CMSM Import Gate Under AX1090",
        "## Private Verdict\n\n2782 does not derive the parent material/source response map. It does the necessary hardening: the WEP product contract is explicit, a toy Ti/Pt vector is staged only for algebra tests, official CMSM import stays open but insufficient, and the real blocker is named cleanly as the parent coupling owner/current/source normalization problem.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## Existing Input Status\n\n" + markdown_table(rows_by_name["inputs"], ["input_id", "object", "current_value_or_status", "source", "gap_remaining", "valid_for_claim"]),
        "## Toy Material Vector\n\n" + markdown_table(rows_by_name["toy"], ["material_vector_id", "material_id", "source_rows", "q_Z_over_A_toy", "q_neutron_excess_toy", "Z_mean_toy", "A_mean_toy", "model_status", "valid_for_claim"]),
        "## Parent Product Contract\n\n" + markdown_table(rows_by_name["contract"], ["contract_id", "object", "formal_contract", "current_status", "valid_for_claim"]),
        "## Derivation Attempt\n\n" + markdown_table(rows_by_name["derivation"], ["attempt_id", "claim", "result", "gap", "valid_for_claim"]),
        "## Coupling Owner Gates\n\n" + markdown_table(rows_by_name["owners"], ["gate_id", "owner_object", "current_status", "blocks", "valid_for_claim"]),
        "## Official CMSM Import Gate\n\n" + markdown_table(rows_by_name["import_gate"], ["import_id", "artifact", "current_status", "effect_if_imported", "remaining_after_import", "valid_for_claim"]),
        "## Nonclaim Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "derivation_status", "notes", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "source_row_id", "bound_valid_for_internal_runner", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "evidence", "consequence", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is the moment the branch stops hiding behind data plumbing. The surrogate math works; the CMSM gate matters later. The physics question is now sharper: does the parent action forbid species/source weighting by construction, or do we need real finite material/source vectors?",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    inputs = build_existing_input_rows()
    toy = build_toy_material_vectors()
    contract = build_contract_rows()
    derivation = build_derivation_rows()
    owners = build_owner_rows()
    import_gate = build_import_gate_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decision_rows()
    next_rows = build_next_rows()

    for key, rows in [
        ("sources", sources), ("inputs", inputs), ("toy", toy), ("contract", contract),
        ("derivation", derivation), ("owners", owners), ("import_gate", import_gate),
        ("candidate", candidate), ("bounds", bounds), ("runner", runner),
        ("comparisons", comparisons), ("gates", gates), ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(inputs, toy, contract, derivation, owners, import_gate, candidate, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "inputs": inputs,
        "toy": toy,
        "contract": contract,
        "derivation": derivation,
        "owners": owners,
        "import_gate": import_gate,
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

    overall = next(row for row in validation if row["validation_id"] == "VAL2782_OVERALL")
    print(f"2782 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
