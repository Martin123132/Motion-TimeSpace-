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
DOC = WORK / "2792-Y5-R2FR-WEP-source-current-zero-or-parent-DD-map-first-row-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2792_SOURCE_REGISTER.csv",
    "zero_attempt": MTS / "P8_Y5_R2FR_2792_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
    "dd_map": MTS / "P8_Y5_R2FR_2792_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv",
    "composition_delta": MTS / "P8_Y5_R2FR_2792_COMPOSITION_DELTA_OBSTRUCTION.csv",
    "pressure": MTS / "P8_Y5_R2FR_2792_NONCLAIM_COEFFICIENT_PRESSURE_ROWS.csv",
    "guards": MTS / "P8_Y5_R2FR_2792_NO_CANCELLATION_GUARD.csv",
    "acquisition": MTS / "P8_Y5_R2FR_2792_ACQUISITION_SCHEMA.csv",
    "candidate": MTS / "P8_Y5_R2FR_2792_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2792_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2792_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2792_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2792_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2792_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2792_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2792_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2792_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "zero_queue": RAB_QUEUE / "JR2792_SOURCE_CURRENT_ZERO_THEOREM_NONCLAIM.csv",
    "map_queue": RAB_QUEUE / "JR2792_PARENT_DD_MAP_FIRST_ROW_NONCLAIM.csv",
    "pressure_queue": RAB_QUEUE / "JR2792_COEFFICIENT_PRESSURE_ROWS_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "WEP_SOURCE_CURRENT_OR_DD_MAP_2792_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_wep_source_current_or_dd_map_2792_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2792_MATTER_DESCENT_OR_COEFFICIENT_PACK_NEXT.csv",
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


def safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return fallback


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
        ("SRC2792_00_2791_next", "2791_next", MTS / "P8_Y5_R2FR_2791_NEXT_TARGET.csv", "NEXT2791_0_2792", "current handoff into source-current zero/DD map route"),
        ("SRC2792_01_2791_validation", "2791_validation", MTS / "P8_Y5_BRR545_2791_VALIDATION.csv", "VAL2791_OVERALL", "2791 validation baseline"),
        ("SRC2792_02_2791_range", "2791_range", MTS / "P8_Y5_R2FR_2791_RANGE_OWNER_THEOREM_ATTEMPT.csv", "ROW2791_5_verdict", "range owner unresolved"),
        ("SRC2792_03_2788_chain", "2788_chain", MTS / "P8_Y5_R2FR_2788_DD_CHAIN_RULE_MAP_CONTRACT.csv", "DCR2788_3_coefficient_projection", "parent-to-DD coefficient projection contract"),
        ("SRC2792_04_2787_dd_delta", "2787_dd_delta", MTS / "P8_Y5_R2FR_2787_DD_MATERIAL_DELTA_IMPORT.csv", "DDM2787_0_delta_alpha", "DD material composition deltas"),
        ("SRC2792_05_2789_pressure", "2789_pressure", MTS / "P8_Y5_R2FR_2789_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv", "DD_PRODUCT2789_0_alpha", "bulk Earth source-material product pressure"),
        ("SRC2792_06_2785_current", "2785_current", MTS / "P8_Y5_R2FR_2785_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv", "NCO2785_5_species_action_weight", "pre-action species weight obstruction"),
        ("SRC2792_07_618_source_zero", "618_source_zero", MTS / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", "SZ618_0_qbar_XT_chain_rule", "conditional source/test zero theorem"),
        ("SRC2792_08_618_no_pole", "618_no_pole", MTS / "P8_Y5_R10_618_NO_POLE_CERTIFICATE_AUDIT.csv", "NPC618_6_no_pole_promotion", "no-pole certificate audit"),
        ("SRC2792_09_1086_zero", "1086_zero", MTS / "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv", "SCZ1086_5_verdict", "R10 source-current precedent"),
        ("SRC2792_10_1086_map", "1086_map", MTS / "P8_Y5_R10_1086_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv", "PDM1086_4_verdict", "R10 parent-DD map precedent"),
        ("SRC2792_11_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def dd_delta_values() -> tuple[float, float]:
    alpha = find_row(MTS / "P8_Y5_R2FR_2787_DD_MATERIAL_DELTA_IMPORT.csv", "delta_id", "DDM2787_0_delta_alpha")
    surface = find_row(MTS / "P8_Y5_R2FR_2787_DD_MATERIAL_DELTA_IMPORT.csv", "delta_id", "DDM2787_1_delta_surface")
    return safe_float(alpha.get("delta_value"), -1.989808886825e-03), safe_float(surface.get("delta_value"), -3.306456347405e-03)


def build_zero_attempt_rows() -> list[dict[str, Any]]:
    generated = ts()
    alpha_delta, surface_delta = dd_delta_values()
    ratio = -alpha_delta / surface_delta if surface_delta else float("nan")
    rows = [
        ("SCZ2792_0_chain_rule_zero", "qbar_XT=0 from matter descent", "if S_matter descends through observed quotient variables and Lie_vX(theta_A)=0, then delta_X S_matter has no material-composition source current", "SZ618_0 gives exactly this as a conditional theorem; R2FR has not parent-signed matter descent", "CONDITIONAL_NOT_PARENT_SIGNED", "parent matter descent; coframe/material constants silence; hidden/source/domain terms"),
        ("SCZ2792_1_Hilbert_current_owner", "Hilbert variation kills post-variation source rescaling", "after one common matter action is fixed, the source tensor is the Hilbert variation and cannot be rescaled by a later material selector", "NCO2785_1 through NCO2785_4 give a conditional subtheorem", "POST_VARIATION_TRICK_CONDITIONALLY_KILLED", "common action and variation-before-readout premises; no pre-action species weights"),
        ("SCZ2792_2_pre_action_weight_leak", "current ownership alone kills species weights inside S_matter", "S_matter=sum_A w_A S_A would still Hilbert-vary to a weighted source if w_A is inserted before variation", "NCO2785_5 leaves pre-action species weights unsigned", "ZERO_PROOF_FAILS_ON_PRE_ACTION_WEIGHTS", "object-language/action-measure clause forbidding species/material weights before variation"),
        ("SCZ2792_3_DD_decomposition_test_pair", "DD alpha/surface composition current vanishes for TA6V-PtRh10", "Delta q_X = c_alpha Delta Q_alpha + c_surface Delta Q_surface + Delta q_tail; both selected Delta Q rows are nonzero", f"Delta Q_alpha={alpha_delta:.15e}, Delta Q_surface={surface_delta:.15e}", "NONZERO_COMPOSITION_DELTAS_BLOCK_AUTOMATIC_ZERO", "c_alpha=0, c_surface=0, tail zero; or parent-signed common-mode/no-pole theorem"),
        ("SCZ2792_4_one_pair_cancellation", "one material pair can be silenced by coefficient ratio", "for this pair alone, Delta q_X=0 if c_surface/c_alpha=-Delta Q_alpha/Delta Q_surface", f"ratio={ratio:.15e}", "FORBIDDEN_CANCELLATION_NOT_THEOREM", "all-material theorem or parent coefficient derivation; one-pair cancellation cannot be used"),
        ("SCZ2792_5_range_pressure", "range owner removes composition current pressure", "a long-range/no-pole theorem can choose source profile but cannot erase nonzero material deltas without a current-zero or coefficient theorem", "ROW2791_5_verdict leaves RANGE_OWNER_NOT_DERIVED", "RANGE_DOES_NOT_SOLVE_COEFFICIENT_ZERO", "parent source-current zero or parent-DD coefficient map"),
        ("SCZ2792_6_verdict", "WEP source/test composition current is theorem-zero", "qbar_XT=0 or DD coefficient vector vanishes from parent action", "conditional descent exists, but pre-action weights, DD coefficients, no-pole, and common-mode routes remain unsigned", "SOURCE_CURRENT_ZERO_NOT_DERIVED", "parent matter descent zero or parent-to-DD zero/coefficients"),
    ]
    return [
        nonclaim({
            "attempt_id": attempt_id,
            "claim": claim,
            "mathematical_statement": statement,
            "current_evidence": evidence,
            "result": result,
            "missing_for_claim": missing,
            "generated_utc": generated,
        })
        for attempt_id, claim, statement, evidence, result, missing in rows
    ]


def build_dd_map_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("PDM2792_0_mass_response_decomposition", "composition-dependent mass response", "partial_X ln m_A = q_0 + c_alpha Q_alpha_Coulomb(A) + c_surface Q_surface_binding(A) + q_tail(A)", "same-branch derivative of ordinary matter masses with respect to X", "DECOMPOSITION_CONTRACT_ONLY", "no parent matter-mass functional m_A[X] exists in the corpus"),
        ("PDM2792_1_alpha_slot", "c_alpha", "c_alpha := N_X * partial_X ln alpha_EM in the DD Q_alpha_Coulomb convention", "signed MTS EM/fine-structure action dependence on X plus field normalization N_X", "MISSING_PARENT_EM_DERIVATIVE", "PTD2788 alpha-channel/pullback remains unsigned"),
        ("PDM2792_2_surface_slot", "c_surface", "c_surface := N_X * partial_X ln a_surface_or_binding in the DD Q_surface_binding convention", "signed nuclear/binding/surface response operator and normalization", "MISSING_PARENT_BINDING_DERIVATIVE", "PTD2788 surface-channel/pullback remains unsigned"),
        ("PDM2792_3_tail_slot", "q_tail(A)", "tail envelope for composition channels not covered by alpha/surface smoke basis", "parent material-response basis or empirical bound over additional materials", "MISSING_TAIL_BASIS", "two DD rows are not a full material basis"),
        ("PDM2792_4_same_branch_units", "C_parent units and signs", "C_parent -> (c_alpha,c_surface,q_tail) with one X normalization, one lambda_X, and one source/readout convention", "Z_X/M_X^2 normalization, K_X, source profile, and MICROSCOPE readout convention", "MISSING_SAME_BRANCH_NORMALIZATION", "range owner, profile/readout, and coefficient units are all missing"),
        ("PDM2792_5_verdict", "first parent-to-DD coefficient row", "C_parent first row can be filled numerically or symbolically from parent action", "real c_alpha or c_surface source path with units/signs", "PARENT_DD_FIRST_ROW_NOT_FILLED", "2792 sharpens the exact row but supplies no parent coefficient"),
    ]
    return [
        nonclaim({
            "map_id": map_id,
            "parent_object": parent_object,
            "candidate_formula": formula,
            "needed_parent_evidence": evidence,
            "current_status": status,
            "gap": gap,
            "generated_utc": generated,
        })
        for map_id, parent_object, formula, evidence, status, gap in rows
    ]


def build_composition_delta_rows() -> list[dict[str, Any]]:
    generated = ts()
    alpha_delta, surface_delta = dd_delta_values()
    ratio = -alpha_delta / surface_delta if surface_delta else float("nan")
    return [
        nonclaim({
            "obstruction_id": "CDO2792_0_alpha_delta",
            "component": "Q_alpha_Coulomb",
            "test_pair": "TA6V_minus_PtRh10",
            "delta_value": f"{alpha_delta:.15e}",
            "delta_abs": f"{abs(alpha_delta):.15e}",
            "meaning": "nonzero DD alpha/Coulomb composition lever",
            "generated_utc": generated,
        }),
        nonclaim({
            "obstruction_id": "CDO2792_1_surface_delta",
            "component": "Q_surface_binding",
            "test_pair": "TA6V_minus_PtRh10",
            "delta_value": f"{surface_delta:.15e}",
            "delta_abs": f"{abs(surface_delta):.15e}",
            "meaning": "nonzero DD surface/binding composition lever",
            "generated_utc": generated,
        }),
        nonclaim({
            "obstruction_id": "CDO2792_2_cancellation_line",
            "component": "c_alpha/c_surface two-component plane",
            "test_pair": "TA6V_minus_PtRh10",
            "delta_value": f"c_surface/c_alpha={ratio:.15e}",
            "delta_abs": "",
            "meaning": "one-pair zero line exists algebraically but is a forbidden cancellation unless parent-derived for all relevant materials",
            "generated_utc": generated,
        }),
    ]


def build_pressure_rows() -> list[dict[str, Any]]:
    generated = ts()
    product_rows = read_csv_rows(MTS / "P8_Y5_R2FR_2789_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv")
    output = []
    for idx, row in enumerate(product_rows):
        component = row.get("component", "")
        if component == "Q_alpha_Coulomb":
            pressure_id = "CPR2792_0_alpha_bulk_Earth"
            blocker = "bulk Earth vector, DD basis, and readout are not parent-owned"
            required = row.get("required_abs_coefficient_max_if_single_component", "")
        elif component == "Q_surface_binding":
            pressure_id = "CPR2792_1_surface_bulk_Earth"
            blocker = "bulk Earth vector, DD basis, and readout are not parent-owned"
            required = row.get("required_abs_coefficient_max_if_single_component", "")
        else:
            pressure_id = "CPR2792_2_equal_two_component_bulk_Earth"
            blocker = "equal-component assumption is not parent-derived and profile/readout gates remain live"
            required = row.get("required_abs_coefficient_max_if_equal_component", "")
        output.append(nonclaim({
            "pressure_id": pressure_id or f"CPR2792_{idx}",
            "component": component,
            "source_material_product_abs": row.get("product_abs", ""),
            "eta_bound": row.get("eta_bound", "2.8e-15"),
            "required_abs_coefficient_max": required,
            "status": "NUMERIC_PRESSURE_NONCLAIM",
            "claim_blocker": blocker,
            "generated_utc": generated,
        }))
    return output


def build_guard_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("NCG2792_0_no_pair_tuning", "choose c_alpha/c_surface to cancel TA6V-PtRh10 only", "one-pair cancellation is not a parent theorem and would fail as soon as another material pair is tested", "derive c_alpha=c_surface=tail=0 or provide a parent coefficient vector and score all rows"),
        ("NCG2792_1_no_measured_G_absorption", "hide source response in measured G", "finite composition-dependent source/test products must be explicit or theorem-zero", "source common-mode theorem or explicit source-profile/readout product"),
        ("NCG2792_2_no_unit_proxy_claim", "use unit source/readout proxy as physical tau_WEP", "unit rows are algebra smoke only", "official MICROSCOPE readout normalization and source profile"),
        ("NCG2792_3_same_branch_lock", "derive lambda from one branch and amplitude from another", "range, coefficient, source, and readout must come from one parent normalization", "same-branch Z_X/M_X^2, C_parent, K_X, Qbar_XH, qbar_XT"),
        ("NCG2792_4_no_tail_erasure", "drop q_tail(A) because alpha/surface rows are convenient", "two DD components are a smoke basis, not a complete material response theorem", "derive tail zero or include an explicit envelope/source pack"),
    ]
    return [
        nonclaim({
            "guard_id": guard_id,
            "forbidden_shortcut": shortcut,
            "reason": reason,
            "required_safe_route": route,
            "generated_utc": generated,
        })
        for guard_id, shortcut, reason, route in rows
    ]


def build_acquisition_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("AS2792_0_matter_descent_zero", "qbar_XT=0 theorem", "branch_id;S_matter_descends;Lie_vX_theta_A;hidden_terms_zero;source_path;valid_for_claim", "CONDITIONAL_NOT_PARENT_SIGNED", "SZ618_0 has theorem shape but no parent signature"),
        ("AS2792_1_alpha_coefficient", "c_alpha", "branch_id;field_id;c_alpha;definition;units;sign;source_path;valid_for_claim", "MISSING_PARENT_EM_DERIVATIVE", "alpha/EM parent operator pullback missing"),
        ("AS2792_2_surface_coefficient", "c_surface", "branch_id;field_id;c_surface;definition;units;sign;source_path;valid_for_claim", "MISSING_PARENT_BINDING_DERIVATIVE", "nuclear/binding parent operator missing"),
        ("AS2792_3_tail_envelope", "q_tail(A) absolute envelope", "branch_id;tail_basis;tail_bound;materials_covered;source_path;valid_for_claim", "MISSING_TAIL_BASIS", "two DD rows are not a full material basis"),
        ("AS2792_4_physical_product", "finite WEP product", "branch_id;lambda_WEP;K_MICROSCOPE;Q_source_eff;c_alpha;c_surface;q_tail;eta_pred;source_paths;valid_for_claim", "MISSING_RANGE_PROFILE_READOUT_AND_COEFFICIENTS", "2789-2791 gates remain live"),
    ]
    return [
        nonclaim({
            "schema_id": schema_id,
            "needed_object": needed,
            "required_columns": columns,
            "current_status": status,
            "claim_blocker": blocker,
            "generated_utc": generated,
        })
        for schema_id, needed, columns, status, blocker in rows
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2792_0_WEP_source_current_or_DD_map_not_MTS_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_SOURCE_CURRENT_ZERO_OR_PARENT_DD_COEFFICIENT_ROW",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R2FR_2792_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
            "inputs_present": "conditional descent theorem; DD deltas; coefficient pressure rows; no-cancellation guards",
            "required_inputs": "parent matter descent zero or parent c_alpha/c_surface/tail coefficients; same-branch range/profile/readout",
            "derivation_status": "SOURCE_CURRENT_ZERO_AND_PARENT_DD_ROW_MISSING",
            "notes": "generic product runner must refuse because zero-current proof and first coefficient row are both unsigned",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2792_0_MICROSCOPE_WEP_source_charge",
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
            "runner_id": "APR2792_0_WEP_source_current_or_DD_map_product_stub",
            "prediction_rows": len(candidate_rows),
            "bound_rows": len(bound_rows),
            "valid_prediction_rows": len(valid_prediction_rows),
            "valid_bound_rows": len(valid_bound_rows),
            "comparison_rows": 1,
            "passed_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject source-current/DD-map rows as MTS product",
        })
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "comparison_id": "COMP2792_0_MICROSCOPE_WEP",
            "prediction_id": "PRED2792_0_WEP_source_current_or_DD_map_not_MTS_product",
            "bound_id": "BOUND2792_0_MICROSCOPE_WEP_source_charge",
            "abs_prediction": "MISSING_SOURCE_CURRENT_ZERO_OR_PARENT_DD_COEFFICIENT_ROW",
            "upper_bound": "2.8e-15",
            "passes_bound": False,
            "comparison_status": "NOT_RUN_AS_MTS_PRODUCT",
            "reason": "source-current zero theorem and parent DD coefficient row are missing",
        })
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("CG2792_0_source_current_zero", "qbar_XT=0 theorem", "conditional", False, "matter descent and material silence are not parent-signed"),
        ("CG2792_1_parent_DD_map", "first parent-to-DD coefficient row", "false", False, "c_alpha/c_surface/tail coefficients are missing"),
        ("CG2792_2_no_cancellation", "no one-pair cancellation", "true", False, "guard retained; not a claim gate"),
        ("CG2792_3_range_profile_readout", "same-branch range/profile/readout", "false", False, "2791 range and readout gates remain live"),
        ("CG2792_4_product_runner", "WEP product runner", "false", False, "valid_prediction_rows=0"),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "claim_component": component,
            "gate_pass": gate_pass,
            "claim_allowed": claim_allowed,
            "reason": reason,
            "generated_utc": generated,
        })
        for gate_id, component, gate_pass, claim_allowed, reason in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("DECISION2792_0", "source-current zero is not derived", "conditional matter descent exists but parent matter descent, material silence, and pre-action species-weight exclusions remain unsigned", "try to parent-sign matter descent and Lie_vX material silence next"),
        ("DECISION2792_1", "first parent-DD coefficient row is not filled", "alpha/surface pullbacks and same-branch normalization are still missing", "build a coefficient source-pack contract if descent cannot be signed"),
        ("DECISION2792_2", "one-pair cancellation is forbidden", "TA6V-PtRh10 admits an algebraic cancellation line but this is not an all-material parent theorem", "keep no-cancellation guards in every finite WEP runner"),
        ("DECISION2792_3", "finite-profile/readout acquisition remains fallback", "range/profile/readout gates remain live and no theorem-zero route has closed", "retain acquisition schema while attacking parent descent/coefficient source pack"),
    ]
    return [
        nonclaim({
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "generated_utc": generated,
        })
        for decision_id, decision, because, next_action in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "next_id": "NEXT2792_0_2793",
            "next_target": "2793-Y5-R2FR-parent-matter-descent-zero-current-or-DD-coefficient-source-pack-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_matter_descent_zero_current_or_DD_coefficient_source_pack_under_AX1090_2793.py",
            "objective": "try to parent-sign S_matter descent and Lie_vX material silence for qbar_XT=0; if that fails, build a source-pack contract for c_alpha, c_surface, and tail coefficients with units and no-cancellation guards",
            "include": "matter action object-language; coframe/material parameter descent; hidden/source/domain terms; DD coefficient source schema; all-material no-cancellation policy",
            "exclude": "measured-G absorption; fitted cancellation line; unit source proxy; DD smoke as MTS claim; GitHub; formalization edits",
        })
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_pairs = [
        (OUTPUTS["zero_attempt"], BRANCH_OUTPUTS["zero_queue"], "zero_queue"),
        (OUTPUTS["dd_map"], BRANCH_OUTPUTS["map_queue"], "map_queue"),
        (OUTPUTS["pressure"], BRANCH_OUTPUTS["pressure_queue"], "pressure_queue"),
        (OUTPUTS["zero_attempt"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["guards"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, target, branch_key in copy_pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(nonclaim({
            "branch_id": f"BR2792_{len(rows)}_{branch_key}",
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
        ("VAL2792_0_sources", all(trueish(row["exists"]) and trueish(row["needle_found"]) for row in sections["sources"]), "every cited source path exists and source needle was found"),
        ("VAL2792_1_zero_not_derived", any(row["attempt_id"] == "SCZ2792_6_verdict" and row["result"] == "SOURCE_CURRENT_ZERO_NOT_DERIVED" for row in sections["zero_attempt"]), "source-current zero theorem is not claimed"),
        ("VAL2792_2_pre_action_weight_blocks", any(row["attempt_id"] == "SCZ2792_2_pre_action_weight_leak" and row["result"] == "ZERO_PROOF_FAILS_ON_PRE_ACTION_WEIGHTS" for row in sections["zero_attempt"]), "pre-action species weight obstruction is retained"),
        ("VAL2792_3_dd_map_not_filled", any(row["map_id"] == "PDM2792_5_verdict" and row["current_status"] == "PARENT_DD_FIRST_ROW_NOT_FILLED" for row in sections["dd_map"]), "first parent-DD map row is not filled"),
        ("VAL2792_4_deltas_nonzero", all(is_numeric(row["delta_abs"]) and float(row["delta_abs"]) > 0 for row in sections["composition_delta"] if row["delta_abs"]), "DD composition delta obstruction rows are numeric/nonzero"),
        ("VAL2792_5_pressure_numeric", all(is_numeric(row["source_material_product_abs"]) and is_numeric(row["required_abs_coefficient_max"]) for row in sections["pressure"] if row["required_abs_coefficient_max"]), "coefficient pressure rows are numeric"),
        ("VAL2792_6_guards_present", len(sections["guards"]) >= 4 and all(not trueish(row["valid_for_claim"]) for row in sections["guards"]), "no-cancellation guards are present and nonclaim"),
        ("VAL2792_7_acquisition_blocks", all(not trueish(row["valid_for_claim"]) for row in sections["acquisition"]) and any(row["schema_id"] == "AS2792_0_matter_descent_zero" for row in sections["acquisition"]), "acquisition schema remains blocked"),
        ("VAL2792_8_prediction_nonclaim_missing", all(has_missing_marker(row) and not trueish(row["valid_for_claim"]) for row in sections["candidate"]), "prediction row remains missing zero theorem or parent coefficient"),
        ("VAL2792_9_bound_numeric", all(is_numeric(row["upper_bound"]) and float(row["upper_bound"]) > 0 for row in sections["bounds"]), "bound import is positive numeric"),
        ("VAL2792_10_runner_refuses", sections["runner"][0]["valid_prediction_rows"] == 0 and not trueish(sections["runner"][0]["claim_allowed"]), "generic product runner refuses source-current/DD-map rows as MTS product"),
        ("VAL2792_11_claim_gates_safe", all(not trueish(row.get("claim_allowed")) for row in sections["gates"]), "all claim gates deny WEP/local-GR claim"),
        ("VAL2792_12_next_target", "2793-Y5-R2FR" in sections["next"][0]["next_target"], "2793 handoff written"),
        ("VAL2792_13_branch_outputs", all(trueish(row["exists"]) and int(row["row_count"]) > 0 for row in sections["branches"]), "branch copies exist and contain rows"),
        ("VAL2792_14_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2792_15_no_claim_flags", no_claim_flags(generated_paths), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2792_16_generated_under_post_checkpoint", all(WORK in path.parents or path == WORK for path in generated_paths + [DOC]), "all generated outputs are under post-checkpoint-work"),
        ("VAL2792_17_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2792_18_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent at validation write"),
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
        "validation_id": "VAL2792_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2792 attempts the derivation-first WEP route. Conditional matter descent and Hilbert-current lemmas are retained, but pre-action weights, nonzero DD composition deltas, missing alpha/surface parent pullbacks, and same-branch range/readout normalization prevent a theorem-zero claim. A DD coefficient source-pack route becomes the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2792 - WEP source-current zero or parent-DD map first row under AX1090",
        "",
        "## Private Verdict",
        "",
        "2792 hits the WEP coupling boss directly. The good news is that the zero-current theorem has a clean conditional form: if the matter action descends through observed variables and material constants are silent along the X direction, then qbar_XT vanishes. The bad news is still the honest news: that descent is not parent-signed, pre-action species weights survive, the DD alpha/surface material deltas are nonzero, and no parent alpha/surface coefficient row exists. So no WEP/local-GR claim follows; the next move is parent matter descent or a DD coefficient source pack.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["row_id", "source_key", "exists", "needle_found", "source_role"]),
        "",
        "## Source-Current Zero Theorem Attempt",
        markdown_table(sections["zero_attempt"], ["attempt_id", "claim", "result", "missing_for_claim"]),
        "",
        "## Parent-DD Map First Row Attempt",
        markdown_table(sections["dd_map"], ["map_id", "parent_object", "current_status", "gap"]),
        "",
        "## Composition Delta Obstruction",
        markdown_table(sections["composition_delta"], ["obstruction_id", "component", "delta_value", "delta_abs", "meaning"]),
        "",
        "## Nonclaim Coefficient Pressure Rows",
        markdown_table(sections["pressure"], ["pressure_id", "component", "source_material_product_abs", "eta_bound", "required_abs_coefficient_max", "claim_blocker"]),
        "",
        "## No-Cancellation Guard",
        markdown_table(sections["guards"], ["guard_id", "forbidden_shortcut", "reason", "required_safe_route"]),
        "",
        "## Acquisition Schema",
        markdown_table(sections["acquisition"], ["schema_id", "needed_object", "current_status", "claim_blocker"]),
        "",
        "## Product Stub And Bound",
        markdown_table(sections["candidate"], ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
        "",
        markdown_table(sections["bounds"], ["bound_id", "observable", "upper_bound", "units", "valid_bound_row"]),
        "",
        markdown_table(sections["runner"], ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
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
        "zero_attempt": build_zero_attempt_rows(),
        "dd_map": build_dd_map_rows(),
        "composition_delta": build_composition_delta_rows(),
        "pressure": build_pressure_rows(),
        "guards": build_guard_rows(),
        "acquisition": build_acquisition_rows(),
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
