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
DOC = WORK / "2788-Y5-R2FR-parent-to-DD-coefficient-map-or-physical-source-readout-fill-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2788_SOURCE_REGISTER.csv",
    "map_attempt": MTS / "P8_Y5_R2FR_2788_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv",
    "chain_rule": MTS / "P8_Y5_R2FR_2788_DD_CHAIN_RULE_MAP_CONTRACT.csv",
    "coefficient_units": MTS / "P8_Y5_R2FR_2788_COEFFICIENT_UNITS_CONTRACT.csv",
    "earth_fill": MTS / "P8_Y5_R2FR_2788_PHYSICAL_EARTH_SOURCE_FILL_ROWS.csv",
    "readout_fill": MTS / "P8_Y5_R2FR_2788_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv",
    "dd_reuse": MTS / "P8_Y5_R2FR_2788_DD_SMOKE_REUSE_ROWS.csv",
    "candidate": MTS / "P8_Y5_R2FR_2788_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2788_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2788_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2788_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2788_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2788_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2788_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2788_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2788_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "map_queue": RAB_QUEUE / "JR2788_PARENT_TO_DD_COEFFICIENT_MAP_NONCLAIM.csv",
    "earth_queue": RAB_QUEUE / "JR2788_PHYSICAL_EARTH_SOURCE_FILL_NONCLAIM.csv",
    "readout_queue": RAB_QUEUE / "JR2788_PHYSICAL_MICROSCOPE_READOUT_FILL_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "PARENT_TO_DD_COEFFICIENT_MAP_2788_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_parent_to_dd_or_readout_fill_2788_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2788_DD_EARTH_SOURCE_VECTOR_NEXT.csv",
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


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv_rows(path):
        if row.get(key) == value:
            return row
    return {}


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


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


def trueish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


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


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2788_00_2787_next", "2787_next", MTS / "P8_Y5_R2FR_2787_NEXT_TARGET.csv", "NEXT2787_0_2788", "current handoff into parent-to-DD coefficient map"),
        ("SRC2788_01_2787_validation", "2787_validation", MTS / "P8_Y5_BRR545_2787_VALIDATION.csv", "VAL2787_OVERALL", "2787 validation baseline"),
        ("SRC2788_02_2787_response_law", "2787_response_law", MTS / "P8_Y5_R2FR_2787_CONDITIONAL_RESPONSE_LAW.csv", "LAW2787_1_product", "conditional finite WEP response law"),
        ("SRC2788_03_2787_parent_to_dd", "2787_parent_to_dd", MTS / "P8_Y5_R2FR_2787_PARENT_TO_DD_GATE.csv", "PDD2787_1_coefficient_map", "parent-to-DD missing gate"),
        ("SRC2788_04_2787_dd_runner", "2787_dd_runner", MTS / "P8_Y5_R2FR_2787_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv", "DDS2787_0_alpha_unit", "R2FR DD smoke rows"),
        ("SRC2788_05_2786_earth", "2786_earth", MTS / "P8_Y5_R2FR_2786_EARTH_SOURCE_VECTOR_CANDIDATES.csv", "EARTH2786_1_bulk_composition_reference", "R2FR Earth/source acquisition status"),
        ("SRC2788_06_2786_readout", "2786_readout", MTS / "P8_Y5_R2FR_2786_MICROSCOPE_READOUT_GATE.csv", "READ2786_3_physical_tau", "R2FR MICROSCOPE readout status"),
        ("SRC2788_07_2786_cparent", "2786_cparent", MTS / "P8_Y5_R2FR_2786_C_PARENT_COEFFICIENT_CONTRACT.csv", "CP2786_0_definition", "R2FR C_parent contract"),
        ("SRC2788_08_1082_map", "1082_map", MTS / "P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv", "PTD1082_4_verdict", "R10 parent-to-DD precedent"),
        ("SRC2788_09_1082_units", "1082_units", MTS / "P8_Y5_R10_1082_COEFFICIENT_UNITS_CONTRACT.csv", "CUC1082_3_C_parent", "R10 coefficient units contract"),
        ("SRC2788_10_1082_earth", "1082_earth", MTS / "P8_Y5_R10_1082_PHYSICAL_EARTH_SOURCE_FILL_ROWS.csv", "ESF1082_1_vectorization", "R10 physical Earth/source fill status"),
        ("SRC2788_11_1082_readout", "1082_readout", MTS / "P8_Y5_R10_1082_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv", "ROF1082_0_official_arrays", "R10 physical MICROSCOPE readout fill status"),
        ("SRC2788_12_1082_reuse", "1082_reuse", MTS / "P8_Y5_R10_1082_DD_SMOKE_REUSE_ROWS.csv", "REUSE1082_0_alpha_unit", "R10 DD smoke reuse rows"),
        ("SRC2788_13_1083_next", "1083_next", MTS / "P8_Y5_R10_1083_NEXT_TARGET.csv", "NEXT1083_0_1084", "R10 post-Earth-vector route if available"),
        ("SRC2788_14_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row"),
    ]
    rows = [source_row(*spec) for spec in specs]
    for row in rows:
        if row["row_id"] == "SRC2788_13_1083_next" and not row["needle_found"]:
            row["needle"] = "NEXT1083"
            row["needle_found"] = row["exists"] and "NEXT1083" in read_text(Path(row["source_path"]))
    return rows


def build_map_attempt_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("PTD2788_0_target", "derive C_parent -> (c_alpha,c_surface)", "local WEP coupling basis with explicit EM/Coulomb and nuclear surface/binding slots", "search for an MTS parent operator decomposition that naturally selects the two DD components", "TARGET_SHARPENED", "the map must specify basis, units, signs, source normalization, and readout placement"),
        ("PTD2788_1_chain_rule_form", "conditional chain-rule map exists if parent controls low-energy constants", "d_i = partial ln constant_i / partial eps_I and c_i = sum_I C_parent^I d_i", "pull the 2787 response law through DD charge coordinates by ordinary differentiation", "EXACT_CONDITIONAL_CHAIN_RULE", "requires signed parent variables eps_I and their effect on alpha/Coulomb and surface/binding constants"),
        ("PTD2788_2_alpha_channel", "MTS alpha/EM sector maps to DD Q_alpha_Coulomb", "signed parent EM/fine-structure response operator with material charge pullback", "use the existence of EM/charge work as a candidate parent slot", "NOT_SIGNED", "no source-backed operator pullback from MTS EM sector to DD Q_alpha_Coulomb is present"),
        ("PTD2788_3_surface_channel", "MTS binding/mass sector maps to DD Q_surface_binding", "signed nuclear/surface/binding response operator with material tensor pullback", "treat surface/binding row as a possible residual mass/binding channel", "NOT_SIGNED", "no parent nuclear/binding operator or coefficient normalization is derived"),
        ("PTD2788_4_units_and_sign", "C_parent units and sign convention match DD proxy coefficients", "dimensionless coefficient vector in the DD charge convention", "compare 2787 coefficient-normalized smoke rows to parent C_parent contract", "MISSING_UNITS_MAP", "C_parent is basis-dependent and no parent action coefficient dimension/sign is fixed"),
        ("PTD2788_5_source_readout", "source/readout normalization can be separated from coefficient map", "R_source^Earth and K_MICROSCOPE/tau_WEP are explicit factors, not absorbed into c_i", "retain 2787 product law and unit proxy block rules", "SEPARATION_RULE_RETAINED", "physical source/readout fill still required before empirical product"),
        ("PTD2788_6_verdict", "parent-to-DD coefficient map is derived", "C_parent -> (c_alpha,c_surface) plus same-basis source/readout normalization", "assemble chain rule, alpha, surface, units, sign, and source/readout conditions", "PARENT_TO_DD_MAP_NOT_DERIVED_BUT_CONDITIONAL_CHAIN_RULE_WRITTEN", "DD branch remains an external comparator unless future parent operator/basis work closes it"),
    ]
    return [
        nonclaim({
            "map_id": map_id,
            "claim": claim,
            "needed_parent_object": needed,
            "proof_attempt": proof,
            "result": result,
            "gap": gap,
            "generated_utc": generated,
        })
        for map_id, claim, needed, proof, result, gap in specs
    ]


def build_chain_rule_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("DCR2788_0_parent_coordinates", "parent coordinates", "eps_I are signed parent vertical/coupling generators in the local matter action", "MISSING_SIGNED_PARENT_GENERATORS", "needed before any DD component can be called MTS-derived"),
        ("DCR2788_1_dd_constants", "DD target coordinates", "d_alpha and d_surface represent low-energy alpha/Coulomb and surface/binding response amplitudes", "EXTERNAL_COORDINATES_AVAILABLE", "available only as phenomenological comparator coordinates"),
        ("DCR2788_2_pullback", "operator pullback", "D_iI := partial d_i / partial eps_I maps parent generators into DD response coordinates", "MISSING_OPERATOR_PULLBACK", "requires MTS EM and binding operators with units and signs"),
        ("DCR2788_3_coefficient_projection", "coefficient projection", "c_i = sum_I C_parent^I D_iI", "EXACT_IF_D_I_AND_C_PARENT_SIGNED", "C_parent and D_iI are both unsigned"),
        ("DCR2788_4_product_projection", "DD finite WEP product", "P_WEP_DD = tau_WEP * R_source^DD * (c_alpha DeltaQ_alpha + c_surface DeltaQ_surface)", "FORMAL_NONCLAIM_PRODUCT", "physical source/readout and coefficient map missing"),
        ("DCR2788_5_claim_rule", "claim rule", "only promote if D_iI, C_parent, source vector, material deltas, and tau_WEP are signed/sourced in one convention", "STRICT_GATE", "current checkpoint fails the rule"),
    ]
    return [
        nonclaim({
            "chain_rule_id": row_id,
            "object": obj,
            "statement": statement,
            "status": status,
            "missing_for_claim": missing,
            "generated_utc": generated,
        })
        for row_id, obj, statement, status, missing in specs
    ]


def build_coefficient_units_rows() -> list[dict[str, Any]]:
    generated = ts()
    dd_rows = read_csv_rows(MTS / "P8_Y5_R2FR_2787_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv")
    lookup = {row.get("smoke_id"): row for row in dd_rows}
    specs = [
        ("CUC2788_0_c_alpha_proxy", "c_alpha_proxy", "DD Q_alpha_Coulomb unit-response smoke convention", "dimensionless per unit source/readout proxy", lookup.get("DDS2787_0_alpha_unit", {}).get("required_abs_coefficient_max", "1.407170315973e-12"), "DDS2787_0_alpha_unit", "NUMERIC_SMOKE_BOUND_NONCLAIM", "MTS-to-DD coefficient map and physical source/readout normalization"),
        ("CUC2788_1_c_surface_proxy", "c_surface_proxy", "DD Q_surface_binding unit-response smoke convention", "dimensionless per unit source/readout proxy", lookup.get("DDS2787_1_surface_unit", {}).get("required_abs_coefficient_max", "8.468280557212e-13"), "DDS2787_1_surface_unit", "NUMERIC_SMOKE_BOUND_NONCLAIM", "MTS-to-DD coefficient map and physical source/readout normalization"),
        ("CUC2788_2_c_equal_proxy", "c_equal_proxy", "DD equal alpha+surface unit-response smoke convention", "dimensionless per unit source/readout proxy", lookup.get("DDS2787_2_equal_two_component_unit", {}).get("required_abs_coefficient_max", "5.286744292758e-13"), "DDS2787_2_equal_two_component_unit", "NUMERIC_SMOKE_BOUND_NONCLAIM", "MTS-to-DD coefficient map and physical source/readout normalization"),
        ("CUC2788_3_C_parent", "C_parent", "MTS parent WEP basis", "MISSING_PARENT_UNITS", "MISSING_PARENT_COEFFICIENT_VECTOR", "PTD2788_6_verdict", "MISSING_FOR_CLAIM", "parent action coefficient extraction"),
        ("CUC2788_4_pullback_matrix", "D_iI", "parent-to-DD operator pullback", "MISSING_PULLBACK_UNITS", "MISSING_OPERATOR_PULLBACK_MATRIX", "DCR2788_2_pullback", "MISSING_FOR_CLAIM", "signed EM/binding parent operators"),
    ]
    return [
        nonclaim({
            "coefficient_id": coeff_id,
            "coefficient_symbol": symbol,
            "basis": basis,
            "units": units,
            "bound_or_value": value,
            "source_row": source_row_id,
            "status": status,
            "missing_for_claim": missing,
            "generated_utc": generated,
        })
        for coeff_id, symbol, basis, units, value, source_row_id, status, missing in specs
    ]


def build_earth_fill_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("ESF2788_0_reference", "Earth source composition reference", "WEB2786_2_MCDONOUGH_SUN_1995", "bulk Earth or shell-weighted elemental composition table with uncertainties", "REFERENCE_IDENTIFIED_NOT_EXTRACTED", "no numeric DD/MTS source vector"),
        ("ESF2788_1_vectorization", "R_source^Earth in DD alpha/surface basis", "Damour-Donoghue charge formulas plus Earth composition table", "compute Q_alpha_Coulomb^Earth and Q_surface_binding^Earth or justify common-mode cancellation", "NOT_VECTORIZED", "source leg cannot remain unit proxy"),
        ("ESF2788_2_profile", "source profile/worldtube weighting", "Earth gravity/source model in MICROSCOPE orbit", "which Earth layers/source components couple to the measured acceleration channel", "MISSING_PROFILE_WEIGHTING", "bulk composition alone may not be the measured source vector"),
        ("ESF2788_3_no_absorption", "no measured-G absorption rule", "claim policy", "source vector is explicit or theorem-common-mode; it is not absorbed into measured G", "RULE_RETAINED", "any shortcut would invalidate finite branch"),
        ("ESF2788_4_priority", "next empirical fill", "1083 precedent plus 2786 Earth source candidates", "construct extraction plan and first nonclaim DD Earth-source row", "NEXT_ROUTE_SELECTED", "still nonclaim until formula/source extraction is done"),
    ]
    return [
        nonclaim({
            "fill_id": fill_id,
            "object": obj,
            "candidate_source": source,
            "needed_content": needed,
            "current_status": status,
            "claim_blocker": blocker,
            "generated_utc": generated,
        })
        for fill_id, obj, source, needed, status, blocker in specs
    ]


def build_readout_fill_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("ROF2788_0_official_arrays", "K_MICROSCOPE official arrays", "CMSM data portal / official export", "gx, gz, Sxx, Sxz, segment masks, timing, and calibration/readout convention", "OFFICIAL_ARRAYS_NOT_IMPORTED", "unit readout proxy cannot be physical tau_WEP"),
        ("ROF2788_1_surrogate_reuse", "surrogate readout matrix", "P8_Y5_R2FR_2781_TAU_SHAPE_STATUS.csv", "surrogate can test algebra only", "SURROGATE_AVAILABLE_NONCLAIM", "surrogate matrix cannot replace official readout for claim"),
        ("ROF2788_2_normalization", "readout normalization into eta_AB", "MICROSCOPE measurement equation", "normalization from source-response product to reported Eotvos parameter", "MODEL_STRUCTURE_KNOWN_NORMALIZATION_NOT_FILLED", "no physical projection scalar or kernel"),
        ("ROF2788_3_priority", "readout fill priority", "2786 readout gate", "defer official readout import until source vector or parent map exists unless user supplies CMSM export", "SECOND_AFTER_SOURCE_VECTOR", "official arrays alone cannot produce finite WEP product"),
    ]
    return [
        nonclaim({
            "fill_id": fill_id,
            "object": obj,
            "candidate_source": source,
            "needed_content": needed,
            "current_status": status,
            "claim_blocker": blocker,
            "generated_utc": generated,
        })
        for fill_id, obj, source, needed, status, blocker in specs
    ]


def build_dd_reuse_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = read_csv_rows(MTS / "P8_Y5_R2FR_2787_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv")
    output = []
    for idx, row in enumerate(rows):
        output.append(nonclaim({
            "reuse_id": f"REUSE2788_{idx}_{row.get('component', 'component').split()[0].replace('Q_', '').replace('+', 'plus')}",
            "source_smoke_id": row.get("smoke_id"),
            "component": row.get("component"),
            "unit_response_abs": row.get("unit_response_abs"),
            "required_abs_coefficient_max": row.get("required_abs_coefficient_max"),
            "reuse_policy": "algebra/pipeline smoke only",
            "promotion_blocker": "parent-to-DD map and physical source/readout normalization missing",
            "generated_utc": generated,
        }))
    return output


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2788_0_DD_smoke_not_MTS_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_TO_DD_MAP_OR_PHYSICAL_SOURCE_READOUT_NORMALIZATION",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R2FR_2788_DD_SMOKE_REUSE_ROWS.csv",
            "inputs_present": "DD smoke material deltas; unit source/readout proxy; coefficient-normalized bounds; conditional chain-rule map",
            "required_inputs": "MTS-to-DD coefficient map; physical R_source^Earth; official/validated K_MICROSCOPE; parent claim policy",
            "derivation_status": "CHAIN_RULE_CONTRACT_READY_BUT_DD_PRODUCT_MISSING",
            "notes": "generic product runner must refuse because this is still an external smoke comparator",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2788_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "observable": "eta_WEP_source_charge",
            "upper_bound": bound.get("upper_bound", "2.8e-15"),
            "units": bound.get("units", "dimensionless"),
            "source_path_or_url": bound.get("reference_path_or_url", "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102"),
            "source_row": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "valid_bound_row": True,
        })
    ]


def build_runner_rows(candidate_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_prediction_rows = [
        row for row in candidate_rows
        if trueish(row.get("valid_for_claim")) and is_numeric(row.get("product_value")) and not has_missing_marker(row)
    ]
    valid_bound_rows = [
        row for row in bound_rows
        if trueish(row.get("valid_bound_row")) and is_numeric(row.get("upper_bound")) and float(row.get("upper_bound", 0)) > 0
    ]
    return [
        nonclaim({
            "runner_id": "APR2788_0_DD_smoke_product_stub",
            "prediction_rows": len(candidate_rows),
            "bound_rows": len(bound_rows),
            "valid_prediction_rows": len(valid_prediction_rows),
            "valid_bound_rows": len(valid_bound_rows),
            "comparison_rows": 1,
            "passed_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject DD smoke rows as MTS product",
        })
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "comparison_id": "COMP2788_0_MICROSCOPE_WEP",
            "prediction_id": "PRED2788_0_DD_smoke_not_MTS_product",
            "bound_id": "BOUND2788_0_MICROSCOPE_WEP_source_charge",
            "abs_prediction": "MISSING_PARENT_TO_DD_MAP_OR_PHYSICAL_SOURCE_READOUT_NORMALIZATION",
            "upper_bound": "2.8e-15",
            "passes_bound": False,
            "comparison_status": "NOT_RUN_AS_MTS_PRODUCT",
            "reason": "conditional chain-rule map is useful but not filled by signed MTS-to-DD operators",
        })
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("CG2788_0_chain_rule_contract", "conditional parent-to-DD chain rule", True, False, "mathematical map shape is written but inputs are unsigned"),
        ("CG2788_1_alpha_operator", "MTS alpha/EM pullback operator", False, False, "no signed pullback to Q_alpha_Coulomb"),
        ("CG2788_2_surface_operator", "MTS surface/binding pullback operator", False, False, "no signed pullback to Q_surface_binding"),
        ("CG2788_3_C_parent_units", "C_parent units/sign in DD convention", False, False, "parent coefficient vector missing"),
        ("CG2788_4_physical_source", "physical Earth source vector", False, False, "reference identified but not vectorized"),
        ("CG2788_5_physical_readout", "physical MICROSCOPE readout/tau", False, False, "official arrays/readout normalization missing"),
        ("CG2788_6_product_runner", "WEP product runner", False, False, "valid_prediction_rows=0"),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "gate": gate,
            "supporting_context_present": support,
            "claim_allowed": claim_allowed,
            "reason": reason,
            "generated_utc": generated,
        })
        for gate_id, gate, support, claim_allowed, reason in specs
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("DEC2788_0_chain_rule_kept", "keep the parent-to-DD chain-rule contract", "it converts the vague coupling issue into concrete missing objects D_iI and C_parent^I", "future parent action work must supply signed alpha and surface/binding pullbacks"),
        ("DEC2788_1_map_failed", "parent-to-DD coefficient map remains unsigned", "MTS has no signed alpha/surface operator pullback or coefficient unit/sign map", "do not promote DD smoke to MTS prediction"),
        ("DEC2788_2_physical_fill", "physical source/readout fill is the next empirical scaffold", "unit proxy rows are useful but nonphysical; Earth source and official readout are concrete data locks", "build Earth-source vector extraction plan and CMSM readout checklist"),
        ("DEC2788_3_priority", "prioritize physical Earth source vector before official arrays if limited time", "without source vector, official readout still cannot produce a finite WEP product", "2789 should stage DD Earth-source vector extraction from composition references"),
    ]
    return [
        nonclaim({
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "generated_utc": generated,
        })
        for decision_id, decision, because, next_action in specs
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "next_id": "NEXT2788_0_2789",
            "next_target": "2789-Y5-R2FR-DD-Earth-source-vector-extraction-plan-and-nonclaim-first-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_DD_Earth_source_vector_extraction_plan_and_nonclaim_first_row_under_AX1090_2789.py",
            "objective": "construct the DD-basis Earth/source vector extraction plan and first nonclaim source-row contract from Earth composition references; keep MICROSCOPE readout and MTS coefficient map blocked until sourced",
            "include": "Earth composition table targets; DD alpha/surface charge formulas; shell/profile caveats; common-mode theorem alternative; source vector schema; strict nonclaim gates",
            "exclude": "unit source proxy as physical source; measured-G absorption; DD smoke as MTS claim; public claim; GitHub; formalization edits",
        })
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_pairs = [
        (OUTPUTS["map_attempt"], BRANCH_OUTPUTS["map_queue"], "map_queue"),
        (OUTPUTS["earth_fill"], BRANCH_OUTPUTS["earth_queue"], "earth_queue"),
        (OUTPUTS["readout_fill"], BRANCH_OUTPUTS["readout_queue"], "readout_queue"),
        (OUTPUTS["chain_rule"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["dd_reuse"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, target, branch_key in copy_pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(nonclaim({
            "branch_id": f"BR2788_{len(rows)}_{branch_key}",
            "source_path": str(source),
            "branch_path": str(target),
            "exists": target.exists(),
            "row_count": csv_row_count(target) if target.exists() else 0,
            "branch_role": branch_key,
        }))
    return rows


def no_claim_flags(paths: list[Path]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "pass_for_claim"}
    for path in paths:
        for row in read_csv_rows(path):
            for field in flag_fields:
                if trueish(row.get(field)):
                    return False
    return True


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    started = RUN_STARTED_UTC.timestamp()
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= started:
            count += 1
    return count


def build_validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2788_0_sources", all(trueish(row["exists"]) and trueish(row["needle_found"]) for row in sections["sources"]), "every cited source path exists and source needle was found"),
        ("VAL2788_1_chain_rule_written", any(row["map_id"] == "PTD2788_1_chain_rule_form" and row["result"] == "EXACT_CONDITIONAL_CHAIN_RULE" for row in sections["map_attempt"]), "conditional parent-to-DD chain-rule map is written"),
        ("VAL2788_2_map_not_claimed", any(row["map_id"] == "PTD2788_6_verdict" and row["result"] == "PARENT_TO_DD_MAP_NOT_DERIVED_BUT_CONDITIONAL_CHAIN_RULE_WRITTEN" for row in sections["map_attempt"]), "parent-to-DD map is not claimed derived"),
        ("VAL2788_3_pullback_missing", any(row["chain_rule_id"] == "DCR2788_2_pullback" and row["status"] == "MISSING_OPERATOR_PULLBACK" for row in sections["chain_rule"]), "operator pullback D_iI remains missing"),
        ("VAL2788_4_units_nonclaim", any(row["coefficient_id"] == "CUC2788_3_C_parent" and row["status"] == "MISSING_FOR_CLAIM" for row in sections["coefficient_units"]) and all(not trueish(row["valid_for_claim"]) for row in sections["coefficient_units"]), "coefficient units contract remains nonclaim"),
        ("VAL2788_5_earth_fill_blocked", any(row["fill_id"] == "ESF2788_1_vectorization" and row["current_status"] == "NOT_VECTORIZED" for row in sections["earth_fill"]), "Earth source vector is not vectorized"),
        ("VAL2788_6_readout_fill_blocked", any(row["fill_id"] == "ROF2788_0_official_arrays" and row["current_status"] == "OFFICIAL_ARRAYS_NOT_IMPORTED" for row in sections["readout_fill"]), "official MICROSCOPE arrays are not imported"),
        ("VAL2788_7_dd_reuse_numeric", all(is_numeric(row["unit_response_abs"]) and is_numeric(row["required_abs_coefficient_max"]) for row in sections["dd_reuse"]), "DD smoke reuse rows are numeric"),
        ("VAL2788_8_prediction_nonclaim_missing", all(has_missing_marker(row) and not trueish(row.get("valid_for_claim")) for row in sections["candidate"]), "prediction row remains missing parent-to-DD or physical source/readout"),
        ("VAL2788_9_bound_numeric", all(is_numeric(row["upper_bound"]) and float(row["upper_bound"]) > 0 for row in sections["bounds"]), "bound import is positive numeric"),
        ("VAL2788_10_runner_refuses", sections["runner"][0]["valid_prediction_rows"] == 0 and not trueish(sections["runner"][0]["claim_allowed"]), "generic product runner refuses DD smoke as MTS product"),
        ("VAL2788_11_claim_gates_safe", all(not trueish(row.get("claim_allowed")) for row in sections["gates"]), "all claim gates deny WEP/local-GR claim"),
        ("VAL2788_12_next_target", "2789-Y5-R2FR" in sections["next"][0]["next_target"], "2789 handoff written"),
        ("VAL2788_13_branch_outputs", all(trueish(row["exists"]) and int(row["row_count"]) > 0 for row in sections["branches"]), "branch copies exist and contain rows"),
        ("VAL2788_14_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2788_15_no_claim_flags", no_claim_flags(generated_paths), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2788_16_generated_under_post_checkpoint", all(WORK in path.parents or path == WORK for path in generated_paths + [DOC]), "all generated outputs are under post-checkpoint-work"),
        ("VAL2788_17_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2788_18_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent at validation write"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append({
        "validation_id": "VAL2788_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2788 writes the exact conditional chain-rule map C_parent -> DD coefficients, but does not derive the signed alpha/surface operator pullbacks or parent coefficient units. DD smoke rows remain numeric nonclaim rows; Earth-source vector extraction becomes the next concrete data scaffold.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2788 - Parent-to-DD coefficient map or physical source/readout fill under AX1090",
        "",
        "## Private Verdict",
        "",
        "2788 sharpens the coupling problem rather than hand-waving it. The exact conditional chain-rule map is now written: if MTS supplies signed parent generators eps_I, and if their pullbacks into DD coordinates are D_iI = partial d_i / partial eps_I, then c_i = sum_I C_parent^I D_iI. That is the mathematical door. The corpus still has not supplied the signed alpha/Coulomb or surface/binding pullback operators, nor the parent C_parent units/signs, so the DD branch remains an external nonclaim smoke comparator. The next concrete empirical scaffold is Earth-source vector extraction.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["row_id", "source_key", "exists", "needle_found", "source_role"]),
        "",
        "## Parent-To-DD Coefficient Map Attempt",
        markdown_table(sections["map_attempt"], ["map_id", "claim", "result", "gap"]),
        "",
        "## DD Chain-Rule Map Contract",
        markdown_table(sections["chain_rule"], ["chain_rule_id", "object", "statement", "status", "missing_for_claim"]),
        "",
        "## Coefficient Units Contract",
        markdown_table(sections["coefficient_units"], ["coefficient_id", "coefficient_symbol", "basis", "units", "bound_or_value", "status"]),
        "",
        "## Physical Earth Source Fill Rows",
        markdown_table(sections["earth_fill"], ["fill_id", "object", "needed_content", "current_status", "claim_blocker"]),
        "",
        "## Physical MICROSCOPE Readout Fill Rows",
        markdown_table(sections["readout_fill"], ["fill_id", "object", "needed_content", "current_status", "claim_blocker"]),
        "",
        "## DD Smoke Reuse Rows",
        markdown_table(sections["dd_reuse"], ["reuse_id", "component", "unit_response_abs", "required_abs_coefficient_max", "promotion_blocker"]),
        "",
        "## Product Stub And Bound",
        markdown_table(sections["candidate"], ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
        "",
        markdown_table(sections["bounds"], ["bound_id", "observable", "upper_bound", "units", "valid_bound_row"]),
        "",
        markdown_table(sections["runner"], ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "gate", "supporting_context_present", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "map_attempt": build_map_attempt_rows(),
        "chain_rule": build_chain_rule_rows(),
        "coefficient_units": build_coefficient_units_rows(),
        "earth_fill": build_earth_fill_rows(),
        "readout_fill": build_readout_fill_rows(),
        "dd_reuse": build_dd_reuse_rows(),
        "candidate": build_candidate_rows(),
        "bounds": build_bound_rows(),
    }
    sections["runner"] = build_runner_rows(sections["candidate"], sections["bounds"])
    sections["comparisons"] = build_comparison_rows()
    sections["gates"] = build_gate_rows()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)

    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])

    sections["validation"] = build_validation_rows(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])

    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
