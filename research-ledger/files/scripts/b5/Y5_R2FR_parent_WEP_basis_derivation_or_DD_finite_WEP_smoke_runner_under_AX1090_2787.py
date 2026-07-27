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
DOC = WORK / "2787-Y5-R2FR-parent-WEP-basis-derivation-or-DD-finite-WEP-smoke-runner-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2787_SOURCE_REGISTER.csv",
    "basis_attempt": MTS / "P8_Y5_R2FR_2787_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv",
    "response_law": MTS / "P8_Y5_R2FR_2787_CONDITIONAL_RESPONSE_LAW.csv",
    "parent_to_dd": MTS / "P8_Y5_R2FR_2787_PARENT_TO_DD_GATE.csv",
    "dd_schema": MTS / "P8_Y5_R2FR_2787_DD_BASIS_SCHEMA.csv",
    "dd_source_policy": MTS / "P8_Y5_R2FR_2787_DD_SOURCE_PROXY_POLICY.csv",
    "dd_delta": MTS / "P8_Y5_R2FR_2787_DD_MATERIAL_DELTA_IMPORT.csv",
    "dd_unit_runner": MTS / "P8_Y5_R2FR_2787_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
    "dd_smoke_status": MTS / "P8_Y5_R2FR_2787_DD_SMOKE_RUNNER_STATUS.csv",
    "candidate": MTS / "P8_Y5_R2FR_2787_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2787_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2787_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2787_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2787_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2787_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2787_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2787_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2787_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "basis_queue": RAB_QUEUE / "JR2787_PARENT_WEP_BASIS_DERIVATION_NONCLAIM.csv",
    "dd_runner_queue": RAB_QUEUE / "JR2787_DD_FINITE_WEP_SMOKE_RUNNER_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "PARENT_WEP_BASIS_OR_DD_SMOKE_2787_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_dd_finite_wep_smoke_2787_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2787_PARENT_TO_DD_COEFFICIENT_NEXT.csv",
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


def safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return fallback


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2787_00_2786_next", "2786_next", MTS / "P8_Y5_R2FR_2786_NEXT_TARGET.csv", "NEXT2786_0_2787", "current handoff into parent WEP basis/DD smoke route"),
        ("SRC2787_01_2786_validation", "2786_validation", MTS / "P8_Y5_BRR545_2786_VALIDATION.csv", "VAL2786_OVERALL", "2786 validation baseline"),
        ("SRC2787_02_2786_cparent", "2786_cparent", MTS / "P8_Y5_R2FR_2786_C_PARENT_COEFFICIENT_CONTRACT.csv", "CP2786_0_definition", "C_parent missing coefficient contract"),
        ("SRC2787_03_2786_basis_gate", "2786_basis_gate", MTS / "P8_Y5_R2FR_2786_SAME_BASIS_CLOSURE_GATE.csv", "BASIS2786_0_same_basis_formula", "same-basis finite WEP closure gate"),
        ("SRC2787_04_2786_input_pack", "2786_input_pack", MTS / "P8_Y5_R2FR_2786_FINITE_WEP_INPUT_PACK_NONCLAIM.csv", "FIP2786_0_product_formula", "finite WEP input pack"),
        ("SRC2787_05_2786_material", "2786_material", MTS / "P8_Y5_R2FR_2786_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv", "MAT2786_5_full_tensor_upgrade", "material tensor missing status"),
        ("SRC2787_06_2786_readout", "2786_readout", MTS / "P8_Y5_R2FR_2786_MICROSCOPE_READOUT_GATE.csv", "READ2786_3_physical_tau", "physical tau missing status"),
        ("SRC2787_07_1081_basis_precedent", "1081_basis_precedent", MTS / "P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv", "PB1081_4_verdict", "R10 parent WEP basis precedent"),
        ("SRC2787_08_1081_dd_schema", "1081_dd_schema", MTS / "P8_Y5_R10_1081_DD_BASIS_SCHEMA.csv", "DDB1081_0_alpha_Coulomb", "R10 DD basis schema"),
        ("SRC2787_09_1081_dd_delta", "1081_dd_delta", MTS / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "DDM1081_0_delta_alpha", "R10 DD material deltas"),
        ("SRC2787_10_1081_source_policy", "1081_source_policy", MTS / "P8_Y5_R10_1081_DD_SOURCE_PROXY_POLICY.csv", "SPP1081_0_unit_source_proxy", "R10 DD unit source/readout policy"),
        ("SRC2787_11_1081_smoke_runner", "1081_smoke_runner", MTS / "P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv", "DDS1081_0_alpha_unit", "R10 DD unit response smoke rows"),
        ("SRC2787_12_2785_narrow", "2785_narrow", MTS / "P8_Y5_R2FR_2785_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv", "NCO2785_1_hilbert_variation", "Hilbert source subtheorem"),
        ("SRC2787_13_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_basis_attempt_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("PB2787_0_target", "derive the finite WEP parent basis from MTS action slots", "parent vertical/coupling generators e_I -> local matter response components R_A^I and source components R_source^I", "look for a parent-owned basis that simultaneously defines C_parent, R_source^Earth, R_TA6V-PtRh10, and K_MICROSCOPE", "TARGET_SHARPENED", "basis must be derived before any external DD components can become MTS components"),
        ("PB2787_1_variational_response_basis", "a conditional response basis can be defined from a differentiable parent action", "R_A^I := partial ln m_A / partial eps_I for parent vertical generators eps_I before readout", "take variations of matter rest energy/binding response with respect to candidate parent generators", "CONDITIONAL_BASIS_CONSTRUCTION", "requires the actual parent generators eps_I and matter mass/binding functional; not supplied by current corpus as signed objects"),
        ("PB2787_2_common_metric_channel", "pure metric/common Hilbert channel gives universal source response", "universal conformal/metric variation enters all matter as common inertial-gravitational mass scaling", "use 2785 Hilbert-source lemma to classify the common metric leg", "COMMON_MODE_ONLY_IF_METRIC", "this protects GR-like universality but produces no finite composition-dependent WEP signal"),
        ("PB2787_3_nonmetric_material_channel", "composition-sensitive WEP response requires nonmetric/material response channels", "parent generators must act differently on EM binding, nuclear binding, masses, or material composition", "ask whether MTS action currently names these channels with units and coefficients", "NOT_DERIVED", "no signed MTS parent matter functional maps motion/time/space variables to material binding sensitivities"),
        ("PB2787_4_DD_embedding", "Damour-Donoghue alpha/surface components are the MTS parent basis", "MTS parent slots -> DD alpha/Coulomb and surface/binding charge components", "treat DD as an external target basis and search for a functor/coefficient map from MTS parent variables", "EXTERNAL_BASIS_ONLY", "no MTS-to-DD map or parent coefficient vector is signed"),
        ("PB2787_5_coefficient_normalization", "C_parent magnitude and units are fixed by the current-owner proof", "C_parent^I supplies the finite source-material coupling in the same response basis", "reuse Hilbert current-owner uniqueness as coefficient owner", "MISSING_COEFFICIENT_OWNER", "current-owner lemma fixes source definition after action is fixed, not pre-variation coefficient magnitude"),
        ("PB2787_6_verdict", "MTS parent WEP basis is derived", "same-basis C_parent, R_source, R_material, K_readout", "assemble variational basis, common metric channel, nonmetric material channels, DD embedding, and coefficient owner checks", "CONDITIONAL_PARENT_RESPONSE_BASIS_ONLY_NOT_CLAIM_DERIVED", "we have the right formal law shape, but not the signed parent generators or coefficient map"),
    ]
    return [
        nonclaim({
            "basis_attempt_id": row_id,
            "claim": claim,
            "required_map": required_map,
            "proof_move": proof_move,
            "result": result,
            "gap": gap,
            "generated_utc": generated,
        })
        for row_id, claim, required_map, proof_move, result, gap in rows
    ]


def build_response_law_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("LAW2787_0_definition", "conditional finite WEP response basis", "If parent vertical generators eps_I are signed, define R_A^I = partial ln m_A / partial eps_I and R_S^I = partial ln M_S / partial eps_I", "EXACT_CONDITIONAL", "requires differentiable matter/source mass functionals in parent variables", False),
        ("LAW2787_1_product", "finite WEP product law", "P_WEP = tau_WEP * sum_I C_parent^I R_source_I^Earth (R_TA6V^I - R_PtRh10^I)", "FORMAL_LAW_READY", "C_parent, R_source, DeltaR_material, and tau_WEP are missing in one signed basis", False),
        ("LAW2787_2_gr_limit", "GR/local universality limit", "If only the common metric/Hilbert channel is present or all DeltaR_material^I=0, then P_WEP=0", "USEFUL_LIMIT_STATEMENT", "this is a consistency limit, not a proof that nonmetric channels vanish", False),
        ("LAW2787_3_dd_projection", "DD projection as comparator", "For an external DD basis, replace I with alpha_Coulomb and surface_binding smoke components", "COMPARATOR_ONLY", "requires MTS-to-DD coefficient map before it can be called MTS", False),
        ("LAW2787_4_claim_rule", "claim rule", "A row becomes claim-eligible only when all product factors are numeric, source-backed, same-basis, and parent-derived or explicitly labelled phenomenological", "STRICT_GATE", "current rows fail this rule", False),
    ]
    return [
        nonclaim({
            "law_id": row_id,
            "object": obj,
            "statement": statement,
            "status": status,
            "missing_for_claim": missing,
            "claim_allowed": claim_allowed,
            "generated_utc": generated,
        })
        for row_id, obj, statement, status, missing, claim_allowed in rows
    ]


def build_parent_to_dd_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("PDD2787_0_parent_basis", "MTS parent WEP basis", "CONDITIONAL_ONLY_NOT_DERIVED", "DD smoke basis cannot be called MTS basis", False),
        ("PDD2787_1_coefficient_map", "C_parent -> (c_alpha_proxy,c_surface_proxy)", "MISSING", "no MTS coefficient vector in DD basis", False),
        ("PDD2787_2_alpha_channel", "parent generator for alpha/Coulomb response", "MISSING_PARENT_GENERATOR", "cannot identify c_alpha_proxy with MTS parameter", False),
        ("PDD2787_3_surface_channel", "parent generator for surface/binding response", "MISSING_PARENT_GENERATOR", "cannot identify c_surface_proxy with MTS parameter", False),
        ("PDD2787_4_source_vector", "R_source^Earth in DD/MTS basis", "MISSING", "unit source proxy is nonphysical", False),
        ("PDD2787_5_readout_kernel", "K_MICROSCOPE official/validated readout", "SURROGATE_ONLY", "unit readout proxy is nonphysical", False),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "needed_object": needed,
            "current_status": status,
            "blocks": blocks,
            "claim_allowed": claim_allowed,
            "generated_utc": generated,
        })
        for gate_id, needed, status, blocks, claim_allowed in rows
    ]


def build_dd_schema_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("DDB2787_0_alpha_Coulomb", "Q_alpha_Coulomb", "WEB2786_1_DAMOUR_DONOGHUE_2010; WCM1053_4; DDM1081_0_delta_alpha", "DDM1081_0_delta_alpha", "c_alpha_proxy", "EXTERNAL_PHENOMENOLOGICAL_SMOKE_BASIS", "not MTS-derived; comparator/smoke only"),
        ("DDB2787_1_surface_binding", "Q_surface_binding", "WEB2786_1_DAMOUR_DONOGHUE_2010; WCM1053_5; DDM1081_1_delta_surface", "DDM1081_1_delta_surface", "c_surface_proxy", "EXTERNAL_PHENOMENOLOGICAL_SMOKE_BASIS", "not MTS-derived; comparator/smoke only"),
        ("DDB2787_2_two_component_proxy", "Q_alpha_Coulomb + Q_surface_binding", "DDM1081_0_delta_alpha; DDM1081_1_delta_surface", "sum of absolute smoke deltas", "c_equal_proxy", "PIPELINE_STRESS_TEST_BASIS", "tests algebra and signs only; no physical coefficient vector"),
    ]
    return [
        nonclaim({
            "basis_id": basis_id,
            "component": component,
            "basis_source": basis_source,
            "material_delta_source": delta_source,
            "coefficient_symbol": coeff,
            "status": status,
            "claim_policy": policy,
            "generated_utc": generated,
        })
        for basis_id, component, basis_source, delta_source, coeff, status, policy in rows
    ]


def build_dd_source_policy_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("SPP2787_0_unit_source_proxy", "DD source proxy", "set source_proxy_norm=1 only to compute coefficient-normalized sensitivity rows", "pipeline algebra smoke; required coefficient bound per unit source/readout convention", "physical tau_WEP, Earth source vector, measured-G absorption, or MTS claim", "BLOCK_CLAIM"),
        ("SPP2787_1_readout_proxy", "K_MICROSCOPE proxy", "set readout_proxy_norm=1 only in the same coefficient-normalized smoke convention", "unit-response and coefficient-bound sanity checks", "replacement for official gx,gz,Sxx,Sxz arrays or physical tau_WEP", "BLOCK_CLAIM"),
        ("SPP2787_2_parent_map", "MTS-to-DD map", "no MTS-to-DD map exists in this checkpoint", "external comparator branch only", "call DD smoke coefficients MTS-derived", "BLOCK_CLAIM"),
    ]
    return [
        nonclaim({
            "policy_id": policy_id,
            "object": obj,
            "policy": policy,
            "allowed_use": allowed,
            "forbidden_use": forbidden,
            "claim_gate": gate,
            "generated_utc": generated,
        })
        for policy_id, obj, policy, allowed, forbidden, gate in rows
    ]


def build_dd_delta_rows() -> list[dict[str, Any]]:
    generated = ts()
    alpha = find_row(MTS / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "delta_id", "DDM1081_0_delta_alpha")
    surface = find_row(MTS / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "delta_id", "DDM1081_1_delta_surface")
    return [
        nonclaim({
            "delta_id": "DDM2787_0_delta_alpha",
            "component": "Q_alpha_Coulomb",
            "test_pair": "TA6V_minus_PtRh10",
            "delta_value": alpha.get("delta_value", "-1.989808886825e-03"),
            "delta_abs": alpha.get("delta_abs", "0.001989808886825"),
            "source_row": "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv:DDM1081_0_delta_alpha",
            "status": "NUMERIC_SMOKE_DELTA_NONCLAIM",
            "generated_utc": generated,
        }),
        nonclaim({
            "delta_id": "DDM2787_1_delta_surface",
            "component": "Q_surface_binding",
            "test_pair": "TA6V_minus_PtRh10",
            "delta_value": surface.get("delta_value", "-3.306456347405e-03"),
            "delta_abs": surface.get("delta_abs", "0.003306456347405"),
            "source_row": "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv:DDM1081_1_delta_surface",
            "status": "NUMERIC_SMOKE_DELTA_NONCLAIM",
            "generated_utc": generated,
        }),
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2787_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "observable": "eta_WEP_source_charge",
            "upper_bound": bound.get("upper_bound", "2.8e-15"),
            "units": bound.get("units", "dimensionless"),
            "source_path_or_url": bound.get("reference_path_or_url", "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102"),
            "source_row": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "valid_bound_row": True,
        })
    ]


def build_dd_unit_runner_rows(dd_delta_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = ts()
    eta_bound = safe_float(bound_rows[0].get("upper_bound"), 2.8e-15)
    alpha_abs = safe_float(dd_delta_rows[0].get("delta_abs"), 0.001989808886825)
    surface_abs = safe_float(dd_delta_rows[1].get("delta_abs"), 0.003306456347405)
    total_abs = alpha_abs + surface_abs
    specs = [
        ("DDS2787_0_alpha_unit", "Q_alpha_Coulomb", alpha_abs, "c_alpha_proxy", "DDM2787_0_delta_alpha"),
        ("DDS2787_1_surface_unit", "Q_surface_binding", surface_abs, "c_surface_proxy", "DDM2787_1_delta_surface"),
        ("DDS2787_2_equal_two_component_unit", "Q_alpha_Coulomb + Q_surface_binding", total_abs, "c_equal_proxy", "DDM2787_0_delta_alpha;DDM2787_1_delta_surface"),
    ]
    rows = []
    for smoke_id, component, response_abs, coeff, source_rows in specs:
        required = eta_bound / response_abs if response_abs > 0 else float("inf")
        rows.append(nonclaim({
            "smoke_id": smoke_id,
            "component": component,
            "unit_source_proxy": "1_nonphysical_coefficient_normalization",
            "unit_readout_proxy": "1_nonphysical_coefficient_normalization",
            "unit_response_abs": f"{response_abs:.12e}",
            "eta_bound": f"{eta_bound:.12e}",
            "required_abs_coefficient_max": f"{required:.12e}",
            "coefficient_symbol": coeff,
            "source_rows": source_rows,
            "status": "NUMERIC_UNIT_RESPONSE_SMOKE_NONCLAIM",
            "claim_blocker": "source/readout proxy is nonphysical and MTS-to-DD map is unsigned",
            "generated_utc": generated,
        }))
    return rows


def build_dd_smoke_status_rows(dd_unit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        nonclaim({
            "runner_id": "DDS2787_RUNNER_0_unit_response",
            "smoke_rows": len(dd_unit_rows),
            "numeric_unit_response_rows": sum(1 for row in dd_unit_rows if is_numeric(row["unit_response_abs"])),
            "positive_coefficient_bound_rows": sum(1 for row in dd_unit_rows if is_numeric(row["required_abs_coefficient_max"]) and float(row["required_abs_coefficient_max"]) > 0),
            "physical_source_vector_present": False,
            "physical_readout_kernel_present": False,
            "MTS_to_DD_map_present": False,
            "claim_allowed": False,
            "expected_result": "numeric smoke rows exist but cannot be promoted to MTS prediction",
        })
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2787_0_DD_smoke_not_MTS_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_TO_DD_MAP_OR_PHYSICAL_SOURCE_READOUT_NORMALIZATION",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R2FR_2787_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
            "inputs_present": "DD smoke material deltas; unit source/readout proxy; MICROSCOPE bound; conditional response law",
            "required_inputs": "MTS-to-DD coefficient map; physical R_source^Earth; official/validated K_MICROSCOPE; parent claim policy",
            "derivation_status": "DD_SMOKE_NUMERIC_BUT_MTS_PRODUCT_MISSING",
            "notes": "generic product runner must refuse because this is an external smoke comparator",
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
            "runner_id": "APR2787_0_DD_smoke_product_stub",
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
            "comparison_id": "COMP2787_0_MICROSCOPE_WEP",
            "prediction_id": "PRED2787_0_DD_smoke_not_MTS_product",
            "bound_id": "BOUND2787_0_MICROSCOPE_WEP_source_charge",
            "abs_prediction": "MISSING_PARENT_TO_DD_MAP_OR_PHYSICAL_SOURCE_READOUT_NORMALIZATION",
            "upper_bound": "2.8e-15",
            "passes_bound": False,
            "comparison_status": "NOT_RUN_AS_MTS_PRODUCT",
            "reason": "DD unit-response rows are numeric but not an MTS prediction",
        })
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("CG2787_0_conditional_response_law", "conditional parent response law", True, False, "formal law shape is useful but inputs are not signed"),
        ("CG2787_1_parent_basis", "MTS parent finite WEP basis", False, False, "parent generators and matter response functionals are not signed"),
        ("CG2787_2_parent_to_DD_map", "MTS-to-DD coefficient map", False, False, "no map from MTS variables to alpha/surface DD coefficients"),
        ("CG2787_3_physical_source_readout", "physical source/readout normalization", False, False, "unit proxies are nonphysical; tau_WEP not acquired"),
        ("CG2787_4_DD_smoke_rows", "DD smoke numeric rows", True, False, "usable for pipeline sanity only, not MTS evidence"),
        ("CG2787_5_product_runner", "WEP product runner", False, False, "valid_prediction_rows=0"),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "gate": gate,
            "supporting_context_present": context,
            "claim_allowed": claim_allowed,
            "reason": reason,
            "generated_utc": generated,
        })
        for gate_id, gate, context, claim_allowed, reason in specs
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("DEC2787_0_real_progress", "keep the conditional parent response law", "R_A^I = partial ln m_A / partial eps_I and P_WEP product law give the right mathematical slot for the coupling problem", "use it as the exact contract future parent action must satisfy"),
        ("DEC2787_1_not_derived", "do not call the parent WEP basis derived", "actual parent vertical generators, material binding response, and C_parent coefficient map are unsigned", "keep WEP/local-GR claim blocked"),
        ("DEC2787_2_smoke_runner", "retain DD alpha/surface rows as an external smoke runner", "they test algebra and bound scales without pretending to be MTS-derived", "use only with strict nonclaim/source-proxy policy"),
        ("DEC2787_3_next", "attack the coefficient map next", "the coupling is now the bottleneck: parent variables must map to DD-like material channels or supply their own basis", "derive C_parent -> (c_alpha,c_surface) or fill physical source/readout rows without claim"),
    ]
    return [
        nonclaim({
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "generated_utc": generated,
        })
        for decision_id, decision, reason, next_action in specs
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "next_id": "NEXT2787_0_2788",
            "next_target": "2788-Y5-R2FR-parent-to-DD-coefficient-map-or-physical-source-readout-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_to_DD_coefficient_map_or_physical_source_readout_fill_under_AX1090_2788.py",
            "objective": "try to derive the MTS-to-DD alpha/surface coefficient map C_parent -> (c_alpha,c_surface); if it remains unsigned, acquire physical Earth-source and MICROSCOPE readout normalization rows for the DD smoke branch without claiming an MTS pass",
            "include": "parent-to-DD map; coefficient units; Earth source vector policy; official readout normalization; DD smoke runner reuse; strict claim gates",
            "exclude": "DD smoke as MTS claim; unit source/readout as tau_WEP; measured-G absorption; public claim; GitHub; formalization edits",
        })
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_pairs = [
        (OUTPUTS["basis_attempt"], BRANCH_OUTPUTS["basis_queue"], "basis_queue"),
        (OUTPUTS["dd_unit_runner"], BRANCH_OUTPUTS["dd_runner_queue"], "dd_runner_queue"),
        (OUTPUTS["response_law"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["dd_smoke_status"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, target, branch_key in copy_pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(nonclaim({
            "branch_id": f"BR2787_{len(rows)}_{branch_key}",
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
        ("VAL2787_0_sources", all(trueish(row["exists"]) and trueish(row["needle_found"]) for row in sections["sources"]), "every cited source path exists and source needle was found"),
        ("VAL2787_1_conditional_basis_law", any(row["basis_attempt_id"] == "PB2787_1_variational_response_basis" and row["result"] == "CONDITIONAL_BASIS_CONSTRUCTION" for row in sections["basis_attempt"]), "conditional variational response basis is written"),
        ("VAL2787_2_parent_basis_not_claimed", any(row["basis_attempt_id"] == "PB2787_6_verdict" and row["result"] == "CONDITIONAL_PARENT_RESPONSE_BASIS_ONLY_NOT_CLAIM_DERIVED" for row in sections["basis_attempt"]), "parent WEP basis is not claimed derived"),
        ("VAL2787_3_response_product_law", any(row["law_id"] == "LAW2787_1_product" and row["status"] == "FORMAL_LAW_READY" for row in sections["response_law"]), "finite WEP product law is staged as formal law"),
        ("VAL2787_4_parent_to_DD_blocked", all(not trueish(row["claim_allowed"]) for row in sections["parent_to_dd"]) and any(row["gate_id"] == "PDD2787_1_coefficient_map" and row["current_status"] == "MISSING" for row in sections["parent_to_dd"]), "parent-to-DD map remains blocked"),
        ("VAL2787_5_dd_schema_nonclaim", len(sections["dd_schema"]) >= 2 and all(not trueish(row["valid_for_claim"]) for row in sections["dd_schema"]), "DD schema rows are nonclaim"),
        ("VAL2787_6_source_policy_blocks", all(row["claim_gate"] == "BLOCK_CLAIM" for row in sections["dd_source_policy"]), "DD source/readout proxy policy blocks claims"),
        ("VAL2787_7_dd_deltas_numeric", all(is_numeric(row["delta_abs"]) and float(row["delta_abs"]) > 0 for row in sections["dd_delta"]), "DD material deltas are numeric smoke rows"),
        ("VAL2787_8_dd_unit_runner_numeric", all(is_numeric(row["required_abs_coefficient_max"]) and float(row["required_abs_coefficient_max"]) > 0 for row in sections["dd_unit_runner"]), "DD unit-response smoke runner computes positive coefficient bounds"),
        ("VAL2787_9_dd_smoke_status_refuses", sections["dd_smoke_status"][0]["MTS_to_DD_map_present"] is False and not trueish(sections["dd_smoke_status"][0]["claim_allowed"]), "DD smoke status refuses MTS promotion"),
        ("VAL2787_10_prediction_nonclaim_missing", all(has_missing_marker(row) and not trueish(row.get("valid_for_claim")) for row in sections["candidate"]), "prediction row remains missing parent-to-DD or physical source/readout"),
        ("VAL2787_11_bound_numeric", all(is_numeric(row["upper_bound"]) and float(row["upper_bound"]) > 0 for row in sections["bounds"]), "bound import is positive numeric"),
        ("VAL2787_12_runner_refuses", sections["runner"][0]["valid_prediction_rows"] == 0 and not trueish(sections["runner"][0]["claim_allowed"]), "generic product runner refuses DD smoke as MTS product"),
        ("VAL2787_13_claim_gates_safe", all(not trueish(row.get("claim_allowed")) for row in sections["gates"]), "all claim gates deny WEP/local-GR claim"),
        ("VAL2787_14_next_target", "2788-Y5-R2FR" in sections["next"][0]["next_target"], "2788 handoff written"),
        ("VAL2787_15_branch_outputs", all(trueish(row["exists"]) and int(row["row_count"]) > 0 for row in sections["branches"]), "branch copies exist and contain rows"),
        ("VAL2787_16_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2787_17_no_claim_flags", no_claim_flags(generated_paths), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2787_18_generated_under_post_checkpoint", all(WORK in path.parents or path == WORK for path in generated_paths + [DOC]), "all generated outputs are under post-checkpoint-work"),
        ("VAL2787_19_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2787_20_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent at validation write"),
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
        "validation_id": "VAL2787_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2787 derives the conditional response-law shape for finite WEP, but does not derive the signed parent WEP basis or C_parent map. DD alpha/surface rows are instantiated as numeric nonclaim smoke/comparator rows only; all product and claim gates remain blocked until parent-to-DD or physical source/readout inputs are supplied.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2787 - Parent WEP basis derivation or DD finite WEP smoke runner under AX1090",
        "",
        "## Private Verdict",
        "",
        "2787 gets a useful mathematical contract but not the full coupling derivation. The clean conditional law is now explicit: if the parent action supplies signed vertical generators eps_I, define material/source responses by variations of log rest-energy/binding content, then the WEP product is a same-basis contraction of C_parent, R_source, DeltaR_material, and tau_WEP. The current corpus still does not sign the parent generators or the C_parent -> DD coefficient map, so DD alpha/surface rows stay as nonclaim smoke/comparator rows.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["row_id", "source_key", "exists", "needle_found", "source_role"]),
        "",
        "## Parent WEP Basis Derivation Attempt",
        markdown_table(sections["basis_attempt"], ["basis_attempt_id", "claim", "result", "gap"]),
        "",
        "## Conditional Response Law",
        markdown_table(sections["response_law"], ["law_id", "object", "statement", "status", "missing_for_claim"]),
        "",
        "## Parent-To-DD Gate",
        markdown_table(sections["parent_to_dd"], ["gate_id", "needed_object", "current_status", "blocks", "claim_allowed"]),
        "",
        "## DD Basis Schema",
        markdown_table(sections["dd_schema"], ["basis_id", "component", "coefficient_symbol", "status", "claim_policy"]),
        "",
        "## DD Source Proxy Policy",
        markdown_table(sections["dd_source_policy"], ["policy_id", "object", "allowed_use", "forbidden_use", "claim_gate"]),
        "",
        "## DD Material Delta Import",
        markdown_table(sections["dd_delta"], ["delta_id", "component", "delta_value", "delta_abs", "status"]),
        "",
        "## DD Unit Response Smoke Runner",
        markdown_table(sections["dd_unit_runner"], ["smoke_id", "component", "unit_response_abs", "eta_bound", "required_abs_coefficient_max", "claim_blocker"]),
        "",
        markdown_table(sections["dd_smoke_status"], ["runner_id", "smoke_rows", "numeric_unit_response_rows", "positive_coefficient_bound_rows", "MTS_to_DD_map_present", "claim_allowed"]),
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
        markdown_table(sections["decision"], ["decision_id", "decision", "reason", "next_action"]),
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
        "basis_attempt": build_basis_attempt_rows(),
        "response_law": build_response_law_rows(),
        "parent_to_dd": build_parent_to_dd_rows(),
        "dd_schema": build_dd_schema_rows(),
        "dd_source_policy": build_dd_source_policy_rows(),
        "dd_delta": build_dd_delta_rows(),
        "bounds": build_bound_rows(),
    }
    sections["dd_unit_runner"] = build_dd_unit_runner_rows(sections["dd_delta"], sections["bounds"])
    sections["dd_smoke_status"] = build_dd_smoke_status_rows(sections["dd_unit_runner"])
    sections["candidate"] = build_candidate_rows()
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
