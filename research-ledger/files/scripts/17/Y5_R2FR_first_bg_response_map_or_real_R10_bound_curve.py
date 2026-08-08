from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1741"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1741 - First b_g Response Map Or Real R10 Bound Curve"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1741_0_1740_doc",
        "source_key": "1740_handoff_doc",
        "source_path": ROOT / "1740-Y5-R2FR-no-shadow-frame-zero-or-bg-bound-projection-map.md",
        "needles": ["NEXT1740_0_primary", "VAL1740_OVERALL"],
    },
    {
        "source_id": "SRC1741_1_1740_projection_map",
        "source_key": "1740_bg_projection_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_BG_BOUND_PROJECTION_MAP.csv",
        "needles": ["BMAP1740_1_gamma_beta", "LOCAL_BOUND_AVAILABLE_RESPONSE_MAP_MISSING"],
    },
    {
        "source_id": "SRC1741_2_1740_bound_inputs",
        "source_key": "1740_bg_bound_inputs",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_BG_BOUND_INPUT_ROWS.csv",
        "needles": ["BBR1740_0_epsilon_shadow_abs", "RETAINED_NONCLAIM_BOUND_INPUT"],
    },
    {
        "source_id": "SRC1741_3_1739_bg_rows",
        "source_key": "1739_bg_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv",
        "needles": ["BG1739_0_generic", "RETAINED_NONCLAIM_BG_ROW"],
    },
    {
        "source_id": "SRC1741_4_local_bounds",
        "source_key": "local_bound_claims",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["Cassini_Shapiro_gamma_2003", "R3_gamma"],
    },
    {
        "source_id": "SRC1741_5_R10_curve",
        "source_key": "R10_alpha_lambda_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needles": ["MISSING_DIGITIZED_ALPHA_BOUND", "template_invalid_missing_digitized_curve"],
    },
    {
        "source_id": "SRC1741_6_785_ppn_chain",
        "source_key": "785_GR_Newton_reduction",
        "source_path": RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv",
        "needles": ["PMC785_7_GR_Newton_reduction", "not_closed"],
    },
    {
        "source_id": "SRC1741_7_1504_countermodel",
        "source_key": "1504_common_frame_countermodel",
        "source_path": RESIDUALS / "P8_Y5_R10_1504_OBSERVED_COFRAME_INDEPENDENCE_AUDIT.csv",
        "needles": ["OC1504_3_universal_conformal_countermodel", "COUNTERMODEL_SURVIVES"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_SOURCE_REGISTER.csv",
    "bg_response_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_BG_RESPONSE_MAP.csv",
    "ppn_gamma_bound_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_PPN_GAMMA_BOUND_BRIDGE.csv",
    "r10_curve_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_R10_CURVE_STATUS.csv",
    "response_claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_RESPONSE_CLAIM_GATE.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1741_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1741_VALIDATION.csv",
}


COPY_MAP = {
    "bg_response_map": "R2FR_1741_BG_RESPONSE_MAP.csv",
    "ppn_gamma_bound_bridge": "R2FR_1741_PPN_GAMMA_BOUND_BRIDGE.csv",
    "r10_curve_status": "R2FR_1741_R10_CURVE_STATUS.csv",
    "response_claim_gate": "R2FR_1741_RESPONSE_CLAIM_GATE.csv",
    "runner_refusal": "R2FR_1741_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1741_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1741_CLAIM_GATE.csv",
    "next_target": "R2FR_1741_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def gamma_bound_row() -> dict[str, str]:
    rows = read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    for row in rows:
        if row.get("row_id") == "R3_gamma":
            return row
    raise RuntimeError("R3_gamma bound row not found")


def r10_curve_rows() -> list[dict[str, str]]:
    return read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv")


def bg_response_map_rows() -> list[dict[str, Any]]:
    gamma = gamma_bound_row()
    gamma_upper = gamma.get("upper_bound", "MISSING_GAMMA_BOUND")
    try:
        sigma_bound_linear = float(gamma_upper) / 2.0
    except ValueError:
        sigma_bound_linear = "MISSING_NUMERIC_GAMMA_BOUND"
    return [
        {
            "branch_id": BRANCH_ID,
            "response_id": "BRM1741_0_conformal_PPN_gamma",
            "route": "first_source_backed_bg_response_map",
            "ansatz": "g_obs=e^(2 sigma_X) g_GR with sigma_X=s_X U/c^2 and s_X=b_g,X x_U",
            "observable": "gamma_minus_1",
            "derived_response": "gamma_eff=(1+s_X)/(1-s_X); gamma_minus_1=2 s_X/(1-s_X) ~= 2 s_X for |s_X|<<1",
            "bound_source_row": "R3_gamma",
            "empirical_upper_bound": gamma_upper,
            "conditional_linear_sX_bound": sigma_bound_linear,
            "required_inputs": "b_g,X;x_U_profile;source_normalization;no_other_PPN_channels;source_path",
            "missing_inputs": "MISSING_BG_VALUE;MISSING_X_U_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_NO_OTHER_CHANNELS",
            "response_source_backed": "True",
            "prediction_source_backed": no(),
            "comparison_ready": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "response_id": "BRM1741_1_WEP_conformal_common_mode_guard",
            "route": "common_mode_not_WEP_by_itself",
            "ansatz": "all ordinary matter sees the same conformal e_obs",
            "observable": "eta_AB",
            "derived_response": "pure universal metric scaling does not produce composition dependence by itself; WEP needs source/readout/marker/species-prefactor leakage",
            "bound_source_row": "R0_identity_coframe_direct;R1_WEP_source_charge",
            "empirical_upper_bound": "2.8e-15",
            "conditional_linear_sX_bound": "NOT_DIRECT_WITHOUT_COMPOSITION_MAP",
            "required_inputs": "source/readout marker map;Delta_w_AB;b_marker_AB;arena response coefficient",
            "missing_inputs": "MISSING_SOURCE_READOUT_MARKER_MAP;MISSING_DELTA_W_AB;MISSING_RESPONSE_COEFFICIENT",
            "response_source_backed": "True",
            "prediction_source_backed": no(),
            "comparison_ready": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def ppn_gamma_bound_bridge_rows() -> list[dict[str, Any]]:
    gamma = gamma_bound_row()
    gamma_upper = gamma.get("upper_bound", "MISSING_GAMMA_BOUND")
    try:
        s_linear_bound = float(gamma_upper) / 2.0
    except ValueError:
        s_linear_bound = "MISSING_NUMERIC_GAMMA_BOUND"
    return [
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "PGB1741_0_Cassini_gamma_bridge",
            "dataset_id": gamma.get("dataset_id", "MISSING_DATASET"),
            "row_id": gamma.get("row_id", "R3_gamma"),
            "observable": gamma.get("observable", "gamma_minus_1"),
            "upper_bound": gamma_upper,
            "units": gamma.get("units", "dimensionless"),
            "reference_path_or_url": gamma.get("reference_path_or_url", "MISSING_REFERENCE"),
            "bridge_formula": "if sigma_X=s_X U/c^2 and no other PPN channels, |2 s_X/(1-s_X)| <= upper_bound",
            "linearized_sX_bound": s_linear_bound,
            "bridge_status": "SOURCE_BACKED_CONDITIONAL_NONCLAIM",
            "why_nonclaim": "s_X=b_g,X x_U is missing and other PPN/source channels are not zero-derived",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
    ]


def r10_curve_status_rows() -> list[dict[str, Any]]:
    rows = []
    for index, row in enumerate(r10_curve_rows()):
        valid = str(row.get("valid_for_claim", "")).lower() == "true"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "curve_row_id": f"R10CURVE1741_{index}",
                "source_bound_id": row.get("bound_id", "MISSING_BOUND_ID"),
                "lambda_value": row.get("lambda_value", "MISSING_NUMERIC_LAMBDA"),
                "lambda_units": row.get("lambda_units", "m"),
                "alpha_bound": row.get("alpha_bound", "MISSING_DIGITIZED_ALPHA_BOUND"),
                "source_file": row.get("source_file", "MISSING_SOURCE_FILE"),
                "digitization_method": row.get("digitization_method", "MISSING_DIGITIZATION_METHOD"),
                "source_valid_for_claim": yesno(valid),
                "curve_status": "REAL_CURVE_AVAILABLE" if valid else "PLACEHOLDER_NONCLAIM",
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def response_claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "RCG1741_0_response_map_exists",
            "claim_piece": "first b_g response map exists",
            "gate_status": "PASS_NONCLAIM",
            "evidence": "BRM1741_0_conformal_PPN_gamma gives source-backed conditional map to Cassini gamma",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "RCG1741_1_numeric_prediction",
            "claim_piece": "MTS predicts gamma_minus_1 from b_g",
            "gate_status": "BLOCKED",
            "evidence": "MISSING_BG_VALUE;MISSING_X_U_PROFILE;MISSING_NO_OTHER_CHANNELS",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "RCG1741_2_R10_curve",
            "claim_piece": "R10 curve is real and score-ready",
            "gate_status": "BLOCKED",
            "evidence": "R10 curve rows remain placeholder/nonclaim",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1741_0_gamma_response_smoke",
            "runner": "b_g to Cassini gamma comparison",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "response map exists, but b_g value, X_U profile and no-other-channel proof are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1741_1_R10_curve_scoring",
            "runner": "R10 alpha(lambda) scoring",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "digitized R10 bound curve remains placeholder/nonclaim",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1741_0_route_choice",
            "decision": "FIRST_BG_RESPONSE_MAP_CHOSEN_OVER_R10_CURVE",
            "reason": "Cassini gamma bound is already locally sourced while R10 curve file is placeholder-only",
            "next_action": "use PPN gamma bridge as first empirical discipline row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1741_1_gamma_bridge",
            "decision": "CONFORMAL_BG_TO_GAMMA_MAP_STAGED",
            "reason": "universal conformal shadow frame produces gamma_eff=(1+s)/(1-s) after Newtonian normalization",
            "next_action": "derive or source s_X=b_g,X x_U profile coefficient",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1741_2_claim_status",
            "decision": "NO_NUMERIC_MTS_PPN_CLAIM",
            "reason": "b_g, X_U profile, source normalization and other channels are missing",
            "next_action": "keep PPN/WEP/R10 claims blocked",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1741_3_best_next_domino",
            "decision": "TARGET_SIGMAX_PROFILE_OR_REAL_R10_CURVE",
            "reason": "the response map is now available; the missing empirical ingredient is either s_X profile or the real R10 curve",
            "next_action": "derive/source x_U for b_g gamma map, or digitize/acquire real R10 alpha(lambda)",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1741_0_response_source",
            "claim": "first b_g response map is source-backed",
            "gate_pass": "True",
            "status": "PASS_NONCLAIM_ONLY",
            "blocker": "claim still blocked by missing b_g and X_U profile",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1741_1_gamma_score",
            "claim": "MTS passes Cassini gamma via b_g map",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_BG_VALUE_AND_X_U_PROFILE",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1741_2_R10_score",
            "claim": "MTS passes R10 shadow-frame bound",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "MISSING_REAL_R10_CURVE_AND_ALPHA_PREDICTION",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1741_0_primary",
            "next_target": "1742-Y5-R2FR-sigmaX-profile-coefficient-or-real-R10-curve.md",
            "script": "scripts/Y5_R2FR_sigmaX_profile_coefficient_or_real_R10_curve.py",
            "objective": "derive or source s_X=b_g,X x_U for the PPN gamma bridge, or replace the placeholder R10 alpha(lambda) curve",
            "success_condition": "finite nonclaim s_X row with units/source path or real digitized R10 curve rows with valid schema",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1741_1_parallel_readout_marker",
            "next_target": "1742b-Y5-R2FR-source-readout-marker-Dq-zero-or-finite-row.md",
            "script": "scripts/Y5_R2FR_source_readout_marker_Dq_zero_or_finite_row.py",
            "objective": "prove source/readout and marker functors descend through q, or keep finite leak rows",
            "success_condition": "source/readout and marker rows source-backed with units and nonclaim comparisons",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "bg_response_map": bg_response_map_rows(),
        "ppn_gamma_bound_bridge": ppn_gamma_bound_bridge_rows(),
        "r10_curve_status": r10_curve_status_rows(),
        "response_claim_gate": response_claim_gate_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1741_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1741_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "accepted_for_scoring",
        "claim_allowed",
        "comparison_ready",
        "prediction_source_backed",
        "score_allowed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
        "accepted_for_scoring",
        "claim_allowed",
        "comparison_ready",
        "prediction_source_backed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1741_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1741_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1741*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    source_register = rows_map["source_register"]
    response = rows_map["bg_response_map"]
    gamma_bridge = rows_map["ppn_gamma_bound_bridge"]
    r10_status = rows_map["r10_curve_status"]
    response_gate = rows_map["response_claim_gate"]
    runner_rows = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1741_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1741_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1741_2_response_map_present", any(row["response_id"] == "BRM1741_0_conformal_PPN_gamma" for row in response), "first conformal b_g to PPN gamma response map exists", "PPN gamma response map missing"),
        check("VAL1741_3_response_source_backed_nonclaim", any(row["response_id"] == "BRM1741_0_conformal_PPN_gamma" and row["response_source_backed"] == "True" and row["valid_for_claim"] == "False" for row in response), "response map is source-backed but nonclaim", "response map is not source-backed nonclaim"),
        check("VAL1741_4_gamma_bound_bridge", any(row["bridge_id"] == "PGB1741_0_Cassini_gamma_bridge" and row["bridge_status"] == "SOURCE_BACKED_CONDITIONAL_NONCLAIM" for row in gamma_bridge), "Cassini gamma bound bridge is recorded", "Cassini gamma bridge missing"),
        check("VAL1741_5_R10_placeholder_blocked", all(row["curve_status"] == "PLACEHOLDER_NONCLAIM" and row["claim_allowed"] == "False" for row in r10_status), "R10 curve remains placeholder/nonclaim", "R10 curve status unexpectedly score-ready"),
        check("VAL1741_6_claim_gate_blocks_numeric", any(row["gate_id"] == "RCG1741_1_numeric_prediction" and row["gate_status"] == "BLOCKED" for row in response_gate), "numeric MTS gamma prediction remains blocked", "numeric gamma prediction gate not blocked"),
        check("VAL1741_7_runners_refuse", all(row["current_status"] == "REFUSE_CLAIM_RUN" and row["claim_allowed"] == "False" for row in runner_rows), "claim runners refuse missing response/R10 inputs", "runner refusal missing or opened claim"),
        check("VAL1741_8_decision_next_domino", any(row["decision_id"] == "DEC1741_3_best_next_domino" and row["decision"] == "TARGET_SIGMAX_PROFILE_OR_REAL_R10_CURVE" for row in decision), "decision selects sigma_X profile or real R10 curve", "decision ledger did not select sigma_X/R10 route"),
        check("VAL1741_9_claim_gates_safe", all(row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1741_10_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1741_11_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked prediction-backed, claim-ready, or score-ready", "a missing row is marked ready"),
        check("VAL1741_12_next_selected", any(row["route_id"] == "NEXT1741_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects sigma_X profile coefficient or real R10 curve", "next target missing selected primary route"),
        check("VAL1741_13_csv_parse", parsed_ok, "all generated 1741 CSVs parse", "one or more generated 1741 CSVs failed to parse"),
        check("VAL1741_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1741_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1741_16_formalization_untouched", formalization_untouched(), "no 1741 outputs found under formalization-workbench", "1741 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1741_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1741 first b_g response map or real R10 bound curve validation" if overall else "one or more 1741 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1741 chooses the first `b_g` response map route because the Cassini PPN gamma bound is already locally sourced, while the R10 curve is still placeholder-only.",
        "- The first source-backed response row is conditional and nonclaim: a universal conformal shadow frame with `sigma_X=s_X U/c^2` gives `gamma_eff=(1+s_X)/(1-s_X)`.",
        "- Linearized, Cassini's `|gamma-1| <= 2.3e-5` implies `|s_X| <= 1.15e-5` only if no other PPN/source channels contribute.",
        "- MTS still has no numeric PPN claim because `b_g`, the `X_U` profile coefficient, source normalization, and no-other-channel theorem are missing.",
        "- R10 remains blocked because the curve file is a placeholder, not a real digitized alpha(lambda) table.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## b_g Response Map",
        markdown_table(rows_map["bg_response_map"], ["response_id", "ansatz", "observable", "derived_response", "empirical_upper_bound", "conditional_linear_sX_bound", "missing_inputs"]),
        "",
        "## PPN Gamma Bound Bridge",
        markdown_table(rows_map["ppn_gamma_bound_bridge"], ["bridge_id", "dataset_id", "observable", "upper_bound", "bridge_formula", "linearized_sX_bound", "bridge_status"]),
        "",
        "## R10 Curve Status",
        markdown_table(rows_map["r10_curve_status"], ["curve_row_id", "source_bound_id", "lambda_value", "alpha_bound", "digitization_method", "curve_status"]),
        "",
        "## Response Claim Gate",
        markdown_table(rows_map["response_claim_gate"], ["gate_id", "claim_piece", "gate_status", "evidence"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["runner_id", "runner", "current_status", "reason"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is the first real counter-punch from the local branch into a published local bound. It does not prove MTS passes Cassini; it tells us exactly what must be derived next: the profile coefficient `s_X=b_g,X x_U`, or a real R10 curve if we want to fight the short-range round instead.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1741-Y5-R2FR-first-bg-response-map-or-real-R10-bound-curve.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1741_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1741 validation FAIL")
    print("1741 validation PASS")


if __name__ == "__main__":
    main()
