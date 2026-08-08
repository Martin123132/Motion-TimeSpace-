from __future__ import annotations

import csv
import math
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
DOC = WORK / "2791-Y5-R2FR-WEP-range-owner-or-long-range-limit-theorem-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2791_SOURCE_REGISTER.csv",
    "web_sources": MTS / "P8_Y5_R2FR_2791_WEB_SOURCE_REGISTER.csv",
    "range_attempt": MTS / "P8_Y5_R2FR_2791_RANGE_OWNER_THEOREM_ATTEMPT.csv",
    "thresholds": MTS / "P8_Y5_R2FR_2791_LONG_RANGE_THRESHOLD_TABLE.csv",
    "profile_influence": MTS / "P8_Y5_R2FR_2791_PROFILE_INFLUENCE_READOUT.csv",
    "range_consistency": MTS / "P8_Y5_R2FR_2791_R2FR_WEP_RANGE_CONSISTENCY_LEDGER.csv",
    "acquisition": MTS / "P8_Y5_R2FR_2791_RANGE_ACQUISITION_SCHEMA.csv",
    "candidate": MTS / "P8_Y5_R2FR_2791_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2791_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2791_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2791_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2791_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2791_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2791_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2791_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2791_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "range_attempt_queue": RAB_QUEUE / "JR2791_WEP_RANGE_OWNER_THEOREM_NONCLAIM.csv",
    "threshold_queue": RAB_QUEUE / "JR2791_LONG_RANGE_THRESHOLD_TABLE_NONCLAIM.csv",
    "acquisition_queue": RAB_QUEUE / "JR2791_RANGE_ACQUISITION_SCHEMA_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "WEP_RANGE_OWNER_2791_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_wep_range_owner_2791_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2791_SOURCE_CURRENT_OR_PARENT_DD_MAP_NEXT.csv",
}

RE = 6.371e6
ORBIT_ALTITUDE = 710e3
HBAR_C_EV_M = 1.973269804e-7


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
        ("SRC2791_00_2790_next", "2790_next", MTS / "P8_Y5_R2FR_2790_NEXT_TARGET.csv", "NEXT2790_0_2791", "current handoff into WEP range owner"),
        ("SRC2791_01_2790_validation", "2790_validation", MTS / "P8_Y5_BRR545_2790_VALIDATION.csv", "VAL2790_OVERALL", "2790 validation baseline"),
        ("SRC2791_02_2790_kernel", "2790_kernel", MTS / "P8_Y5_R2FR_2790_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv", "K2790_2_long_range_limit", "R2FR source profile kernel and long-range limit"),
        ("SRC2791_03_2790_profile", "2790_profile", MTS / "P8_Y5_R2FR_2790_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv", "PROFILE2790_lambda_over_RE_1", "R2FR source profile grid"),
        ("SRC2791_04_2790_readout", "2790_readout", MTS / "P8_Y5_R2FR_2790_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG2790_0_CMSM_arrays", "R2FR MICROSCOPE readout import gate"),
        ("SRC2791_05_2788_chain_rule", "2788_chain_rule", MTS / "P8_Y5_R2FR_2788_DD_CHAIN_RULE_MAP_CONTRACT.csv", "DCR2788_2_pullback", "parent-to-DD pullback still missing"),
        ("SRC2791_06_1085_range", "1085_range", MTS / "P8_Y5_R10_1085_RANGE_OWNER_THEOREM_ATTEMPT.csv", "ROW1085_4_verdict", "R10 range owner precedent"),
        ("SRC2791_07_1085_thresholds", "1085_thresholds", MTS / "P8_Y5_R10_1085_LONG_RANGE_THRESHOLD_TABLE.csv", "LRT1085_lambda_over_RE_10", "R10 long-range threshold table"),
        ("SRC2791_08_1085_influence", "1085_influence", MTS / "P8_Y5_R10_1085_PROFILE_INFLUENCE_READOUT.csv", "INF1085_lambda_over_RE_1", "R10 profile influence ledger"),
        ("SRC2791_09_1085_schema", "1085_schema", MTS / "P8_Y5_R10_1085_RANGE_ACQUISITION_SCHEMA.csv", "RAS1085_0_parent_operator", "R10 range acquisition schema"),
        ("SRC2791_10_1086_next", "1086_next", MTS / "P8_Y5_R10_1086_NEXT_TARGET.csv", "NEXT1086_0_1087", "R10 next derivation route"),
        ("SRC2791_11_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_web_sources() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "web_source_id": "WEB2791_0_MICROSCOPE_FINAL",
            "role": "WEP bound source",
            "source_url": "https://arxiv.org/abs/2209.15487",
            "source_title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
            "evidence_used": "eta(Ti,Pt) final-result bound inherited from local_bound_claims.csv",
            "extraction_method": "bound import only; official readout arrays still not imported",
            "confidence_level": "bound_source_backed; prediction_nonclaim",
            "generated_utc": generated,
        }),
        nonclaim({
            "web_source_id": "WEB2791_1_PROFILE_ALGEBRA",
            "role": "finite-range spherical source profile algebra",
            "source_url": "local-derived-contract",
            "source_title": "2790 R2FR source profile kernel ledger",
            "evidence_used": "spherical finite-range radial kernel and long-range bulk limit from K2790 rows",
            "extraction_method": "local derivation carried forward as nonclaim kernel contract",
            "confidence_level": "math_contract_nonclaim",
            "generated_utc": generated,
        }),
    ]


def build_range_attempt_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("ROW2791_0_exact_range_relation", "massive scalar-like residual", "lambda_WEP = lambda_X = sqrt(Z_X/M_X^2) after canonicalizing O_X=-nabla_i(Z_X nabla^i)+M_X^2", "2787/2788 define the finite WEP product law, but no parent-owned Z_X/M_X^2 values or units are present in R2FR", "RELATION_DERIVED_VALUES_MISSING", "same-branch Z_X, M_X^2, units, source current, and boundary/readout convention"),
        ("ROW2791_1_no_pole_escape", "no physical X pole / quotient branch", "if X is pure quotient/gauge before variation, lambda_WEP is absent and finite source profile disappears", "local no-pole/descent routes remain unsigned; material descent/current owner is still conditional", "NO_POLE_NOT_CLOSED", "parent Omega, DC_X, all-field v_X, Q_X/K_boundary, degree count, matter descent"),
        ("ROW2791_2_massless_long_range", "massless/common long-range carrier", "M_X^2=0 or protected massless source carrier gives lambda_WEP=infinity and bulk source vector is profile-safe", "no parent Ward/symmetry theorem sets M_X^2=0 while keeping controlled WEP coupling and avoiding existing long-range bounds", "LONG_RANGE_THEOREM_NOT_SIGNED", "symmetry protecting zero mass plus source/readout normalization and no fifth-force contradiction"),
        ("ROW2791_3_short_range_residual", "finite short-range residual", "finite lambda_WEP requires the 2790 profile kernel, orbit attenuation, PREM/shell profile, and official readout", "2790 profile grid shows source vector changes with lambda; readout arrays remain missing", "FINITE_PROFILE_BRANCH_RETAINED", "lambda_WEP owner, PREM/composition shell profile, official MICROSCOPE readout, parent-to-DD map"),
        ("ROW2791_4_bulk_limit_condition", "bulk Earth source vector is allowed", "lambda_WEP >> R_E or exact common-mode/no-pole source theorem", "the condition is now explicit but not parent-signed", "BULK_LIMIT_CONDITIONAL_ONLY", "parent-signed long-range condition or common-mode theorem"),
        ("ROW2791_5_verdict", "2791 range owner", "MTS currently proves lambda_WEP >> R_E or lambda_WEP=infinity", "range relation exists only as a contract; no-pole and massless routes are unsigned", "RANGE_OWNER_NOT_DERIVED", "parent-owned range theorem or sourced finite-range profile/readout branch"),
    ]
    return [
        nonclaim({
            "attempt_id": attempt_id,
            "branch": branch,
            "statement": statement,
            "current_evidence": evidence,
            "result": result,
            "missing_for_claim": missing,
            "generated_utc": generated,
        })
        for attempt_id, branch, statement, evidence, result, missing in rows
    ]


def build_threshold_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = []
    for ratio in [1, 3, 10, 30, 100, 1000]:
        lambda_m = ratio * RE
        mass_ev = HBAR_C_EV_M / lambda_m
        status = "profile_sensitive" if ratio < 10 else "bulk_limit_candidate_nonclaim"
        rows.append(nonclaim({
            "threshold_id": f"LRT2791_lambda_over_RE_{ratio}",
            "lambda_over_R_E": ratio,
            "lambda_m": f"{lambda_m:.15e}",
            "equivalent_m_X_eV_if_relativistic": f"{mass_ev:.15e}",
            "static_operator_condition": f"M_X^2/Z_X <= 1/({ratio} R_E)^2",
            "bulk_vector_status": status,
            "claim_condition": "parent must derive this lower bound on lambda_WEP; empirical fit cannot choose it after the fact",
            "generated_utc": generated,
        }))
    return rows


def build_profile_influence_rows() -> list[dict[str, Any]]:
    generated = ts()
    profile_rows = read_csv_rows(MTS / "P8_Y5_R2FR_2790_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv")
    long_row = next((row for row in profile_rows if row.get("profile_row_id") == "PROFILE2790_long_range_mass_average"), {})
    long_alpha = safe_float(long_row.get("Q_alpha_Coulomb_eff"), 0.0)
    long_surface = safe_float(long_row.get("Q_surface_binding_eff"), 0.0)
    output = []
    for row in profile_rows:
        alpha_delta = safe_float(row.get("Q_alpha_Coulomb_eff")) - long_alpha
        surface_delta = safe_float(row.get("Q_surface_binding_eff")) - long_surface
        max_shift = max(abs(alpha_delta), abs(surface_delta))
        ratio_text = row.get("lambda_over_R_E", "inf")
        if ratio_text == "inf":
            attenuation = 1.0
            interpretation = "bulk_limit"
        else:
            ratio = safe_float(ratio_text)
            attenuation = math.exp(-ORBIT_ALTITUDE / (ratio * RE)) if ratio > 0 else 0.0
            interpretation = "bulk_limit" if ratio >= 10 else "finite_profile_live"
        output.append(nonclaim({
            "influence_id": row.get("profile_row_id", "").replace("PROFILE2790", "INF2791"),
            "lambda_label": row.get("lambda_label"),
            "lambda_over_R_E": row.get("lambda_over_R_E"),
            "delta_alpha_vs_two_layer_long_range": f"{alpha_delta:.15e}",
            "delta_surface_vs_two_layer_long_range": f"{surface_delta:.15e}",
            "max_abs_profile_shift": f"{max_shift:.15e}",
            "surface_orbit_attenuation_exp_minus_h_over_lambda": f"{attenuation:.15e}",
            "interpretation": interpretation,
            "generated_utc": generated,
        }))
    return output


def build_range_consistency_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("RWC2791_0_same_lambda_object", "local/R10 lambda_X and WEP lambda_WEP are the same parent range", "NOT_PARENT_SIGNED", "short-range R10 candidates cannot simultaneously justify bulk Earth WEP source vector; long-range WEP candidates must face long-range fifth-force/WEP constraints", "single parent kinetic/mass operator and arena projection showing the same lambda in both observables"),
        ("RWC2791_1_independent_lambdas", "R10 lambda and WEP lambda are independent", "FORBIDDEN_UNLESS_PARENT_SPLITS_FIELDS", "requires two distinct fields/operators, otherwise range choice is post hoc", "field decomposition with separate Z/M blocks and separate source/readout maps"),
        ("RWC2791_2_bulk_shortcut", "use 2789 bulk Earth vector without lambda theorem", "REJECTED", "would hide the finite-range source-profile dependence found in 2790", "lambda_WEP >> R_E or source common-mode/no-pole theorem"),
        ("RWC2791_3_r10_pressure", "R10 bound curve can score this branch now", "REJECTED", "would require alpha(lambda), K_X(lambda), Qbar_XH(lambda), qbar_XT, and real bound curve in one convention", "R10 projection stack plus parent range owner"),
        ("RWC2791_4_readout_pressure", "MICROSCOPE readout import can replace range derivation", "REJECTED_AS_SUBSTITUTE", "official readout can project a chosen range branch but cannot choose lambda_WEP by itself", "range owner or explicit lambda-dependent branch plus readout arrays"),
    ]
    return [
        nonclaim({
            "consistency_id": consistency_id,
            "claim": claim,
            "current_status": status,
            "implication_if_true": implication,
            "required_evidence": evidence,
            "generated_utc": generated,
        })
        for consistency_id, claim, status, implication, evidence in rows
    ]


def build_acquisition_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("RAS2791_0_parent_operator", "O_X=-nabla_i(Z_X nabla^i)+M_X^2", "branch_id;field_id;Z_X;M_X2;Z_units;M_units;source_path;valid_for_claim", "MISSING_PARENT_HESSIAN_VALUES", "lambda cannot be owned without same-branch Z_X and M_X^2"),
        ("RAS2791_1_long_range_certificate", "lambda_WEP lower bound or zero-mass theorem", "branch_id;lambda_lower_bound_m;mass_upper_bound_eV;theorem_or_source;source_path;valid_for_claim", "MISSING_LONG_RANGE_THEOREM", "bulk Earth source vector remains conditional"),
        ("RAS2791_2_finite_profile", "finite lambda source-profile branch", "branch_id;lambda_m;rho_profile;composition_profile;Q_eff_alpha;Q_eff_surface;source_path;valid_for_claim", "MISSING_PREM_AND_LAMBDA_OWNER", "2790 two-layer grid is smoke only"),
        ("RAS2791_3_readout_product", "MICROSCOPE readout normalization", "segment;time;gx;gz;Sxx;Sxz;masks;K_MICROSCOPE;eta_normalization;source_path;valid_for_claim", "OFFICIAL_ARRAYS_NOT_IMPORTED", "source profile alone is not a reported Eotvos prediction"),
        ("RAS2791_4_parent_to_DD_map", "C_parent -> (c_alpha,c_surface)", "branch_id;C_parent;c_alpha;c_surface;units;sign;source_path;valid_for_claim", "PARENT_TO_DD_MAP_NOT_DERIVED", "DD source vector remains external comparator"),
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
            "prediction_id": "PRED2791_0_WEP_range_owner_not_MTS_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_RANGE_OWNER_OR_LONG_RANGE_THEOREM",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R2FR_2791_RANGE_OWNER_THEOREM_ATTEMPT.csv",
            "inputs_present": "range relation contract; long-range threshold table; lambda-dependent profile grid; MICROSCOPE bound",
            "required_inputs": "parent-owned Z_X/M_X^2 or massless/no-pole theorem; parent-to-DD map; physical profile/readout branch",
            "derivation_status": "RANGE_OWNER_NOT_DERIVED",
            "notes": "generic product runner must refuse because bulk or finite-profile source branch lacks parent range owner",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2791_0_MICROSCOPE_WEP_source_charge",
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
            "runner_id": "APR2791_0_WEP_range_owner_product_stub",
            "prediction_rows": len(candidate_rows),
            "bound_rows": len(bound_rows),
            "valid_prediction_rows": len(valid_prediction_rows),
            "valid_bound_rows": len(valid_bound_rows),
            "comparison_rows": 1,
            "passed_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject WEP range owner rows as MTS product",
        })
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "comparison_id": "COMP2791_0_MICROSCOPE_WEP",
            "prediction_id": "PRED2791_0_WEP_range_owner_not_MTS_product",
            "bound_id": "BOUND2791_0_MICROSCOPE_WEP_source_charge",
            "abs_prediction": "MISSING_PARENT_RANGE_OWNER_OR_LONG_RANGE_THEOREM",
            "upper_bound": "2.8e-15",
            "passes_bound": False,
            "comparison_status": "NOT_RUN_AS_MTS_PRODUCT",
            "reason": "range owner, parent-to-DD map, and physical profile/readout branch are missing",
        })
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("CG2791_0_range_relation", "lambda_WEP relation", "conditional", False, "lambda=sqrt(Z/M2) relation is a contract but Z_X/M_X2 values are missing"),
        ("CG2791_1_long_range_bulk", "bulk Earth source vector suffices", "conditional", False, "requires parent-signed lambda_WEP >> R_E or massless/common carrier"),
        ("CG2791_2_no_pole_common_mode", "no-pole/common-mode escape", "false", False, "quotient/no-pole and source common-mode routes remain unsigned"),
        ("CG2791_3_parent_to_DD", "MTS parent-to-DD map", "false", False, "still not derived"),
        ("CG2791_4_readout", "MICROSCOPE official readout", "false", False, "CMSM/export arrays and eta normalization not imported"),
        ("CG2791_5_product_runner", "WEP product runner", "false", False, "valid_prediction_rows=0"),
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
        ("DECISION2791_0", "long-range bulk shortcut is not available yet", "lambda_WEP >> R_E is a theorem condition, not a data-fitting convenience, and current parent files only provide the lambda relation", "attack parent source-current/coupling zero or fill the finite-profile/readout inputs"),
        ("DECISION2791_1", "range and amplitude cannot be chosen independently", "the same parent operator must own lambda_X, K_X, Qbar_XH/qbar_XT, and the DD coefficient map", "return to the coupling/source-current owner before scoring WEP"),
        ("DECISION2791_2", "finite profile branch remains live", "2790 profile grid shows finite-range source-vector drift and no parent range theorem has removed it", "retain lambda-dependent profile rows unless 2792 proves source-current zero/no-pole/common-mode"),
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
            "next_id": "NEXT2791_0_2792",
            "next_target": "2792-Y5-R2FR-WEP-source-current-zero-or-parent-DD-map-first-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_WEP_source_current_zero_or_parent_DD_map_first_row_under_AX1090_2792.py",
            "objective": "try the derivation-first route for WEP: prove the parent source/test composition current vanishes or map the first parent coefficient into the DD alpha/surface basis; if neither closes, retain finite-profile/readout acquisition",
            "include": "J_X/qbar_XT source-current zero attempt; C_parent to DD coefficient map; same-branch normalization; no-pole/common-mode alternatives; nonclaim fallback rows",
            "exclude": "measured-G absorption; fitted lambda choice; unit source proxy; DD smoke as MTS claim; GitHub; formalization edits",
        })
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_pairs = [
        (OUTPUTS["range_attempt"], BRANCH_OUTPUTS["range_attempt_queue"], "range_attempt_queue"),
        (OUTPUTS["thresholds"], BRANCH_OUTPUTS["threshold_queue"], "threshold_queue"),
        (OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_queue"], "acquisition_queue"),
        (OUTPUTS["range_attempt"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["profile_influence"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, target, branch_key in copy_pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(nonclaim({
            "branch_id": f"BR2791_{len(rows)}_{branch_key}",
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
        ("VAL2791_0_sources", all(trueish(row["exists"]) and trueish(row["needle_found"]) for row in sections["sources"]), "every cited source path exists and source needle was found"),
        ("VAL2791_1_range_relation_contract", any(row["attempt_id"] == "ROW2791_0_exact_range_relation" and row["result"] == "RELATION_DERIVED_VALUES_MISSING" for row in sections["range_attempt"]), "range relation is retained as missing-values contract"),
        ("VAL2791_2_range_not_derived", any(row["attempt_id"] == "ROW2791_5_verdict" and row["result"] == "RANGE_OWNER_NOT_DERIVED" for row in sections["range_attempt"]), "range owner is not claimed derived"),
        ("VAL2791_3_thresholds_numeric", len(sections["thresholds"]) >= 6 and all(is_numeric(row["lambda_m"]) and is_numeric(row["equivalent_m_X_eV_if_relativistic"]) for row in sections["thresholds"]), "long-range threshold table is numeric"),
        ("VAL2791_4_profile_influence_numeric", len(sections["profile_influence"]) >= 7 and all(is_numeric(row["max_abs_profile_shift"]) and is_numeric(row["surface_orbit_attenuation_exp_minus_h_over_lambda"]) for row in sections["profile_influence"]), "profile influence rows are numeric"),
        ("VAL2791_5_consistency_blocks_shortcut", any(row["consistency_id"] == "RWC2791_2_bulk_shortcut" and row["current_status"] == "REJECTED" for row in sections["range_consistency"]), "bulk shortcut is rejected without lambda theorem"),
        ("VAL2791_6_acquisition_schema_blocks", all(not trueish(row["valid_for_claim"]) for row in sections["acquisition"]) and any(row["schema_id"] == "RAS2791_0_parent_operator" and row["current_status"] == "MISSING_PARENT_HESSIAN_VALUES" for row in sections["acquisition"]), "range acquisition schema remains blocked"),
        ("VAL2791_7_prediction_nonclaim_missing", all(has_missing_marker(row) and not trueish(row["valid_for_claim"]) for row in sections["candidate"]), "prediction row remains missing parent range owner"),
        ("VAL2791_8_bound_numeric", all(is_numeric(row["upper_bound"]) and float(row["upper_bound"]) > 0 for row in sections["bounds"]), "bound import is positive numeric"),
        ("VAL2791_9_runner_refuses", sections["runner"][0]["valid_prediction_rows"] == 0 and not trueish(sections["runner"][0]["claim_allowed"]), "generic product runner refuses range owner rows as MTS product"),
        ("VAL2791_10_claim_gates_safe", all(not trueish(row.get("claim_allowed")) for row in sections["gates"]), "all claim gates deny WEP/local-GR claim"),
        ("VAL2791_11_next_target", "2792-Y5-R2FR" in sections["next"][0]["next_target"], "2792 handoff written"),
        ("VAL2791_12_branch_outputs", all(trueish(row["exists"]) and int(row["row_count"]) > 0 for row in sections["branches"]), "branch copies exist and contain rows"),
        ("VAL2791_13_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2791_14_no_claim_flags", no_claim_flags(generated_paths), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2791_15_generated_under_post_checkpoint", all(WORK in path.parents or path == WORK for path in generated_paths + [DOC]), "all generated outputs are under post-checkpoint-work"),
        ("VAL2791_16_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2791_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent at validation write"),
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
        "validation_id": "VAL2791_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2791 keeps the exact range relation and long-range threshold table, but does not derive a parent WEP range owner or long-range theorem. The bulk Earth source vector remains conditional; finite-profile/readout acquisition remains live; next target returns to source-current zero or parent-DD coefficient mapping.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2791 - WEP range owner or long-range limit theorem under AX1090",
        "",
        "## Private Verdict",
        "",
        "2791 closes the route-choice honestly: the bulk Earth source vector cannot be promoted yet. The useful relation is lambda_WEP = sqrt(Z_X/M_X^2), or lambda=infinity if a massless/no-pole/common-mode theorem is parent-signed. But the parent operator values, no-pole certificate, massless symmetry, parent-to-DD map, and official readout are still unsigned. Therefore the bulk vector is conditional and the finite-profile branch remains live.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["row_id", "source_key", "exists", "needle_found", "source_role"]),
        "",
        "## Range Owner Theorem Attempt",
        markdown_table(sections["range_attempt"], ["attempt_id", "branch", "result", "missing_for_claim"]),
        "",
        "## Long-Range Threshold Table",
        markdown_table(sections["thresholds"], ["threshold_id", "lambda_over_R_E", "lambda_m", "equivalent_m_X_eV_if_relativistic", "bulk_vector_status", "claim_condition"]),
        "",
        "## Profile Influence Readout",
        markdown_table(sections["profile_influence"], ["influence_id", "lambda_label", "lambda_over_R_E", "max_abs_profile_shift", "surface_orbit_attenuation_exp_minus_h_over_lambda", "interpretation"]),
        "",
        "## R2FR WEP Range Consistency Ledger",
        markdown_table(sections["range_consistency"], ["consistency_id", "claim", "current_status", "required_evidence"]),
        "",
        "## Range Acquisition Schema",
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
        "web_sources": build_web_sources(),
        "range_attempt": build_range_attempt_rows(),
        "thresholds": build_threshold_rows(),
        "profile_influence": build_profile_influence_rows(),
        "range_consistency": build_range_consistency_rows(),
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
