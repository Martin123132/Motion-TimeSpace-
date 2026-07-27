from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1901"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1901-Y5-R2FR-measured-G-common-mode-guard-or-source-vector-fill.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1900_doc": ROOT / "1900-Y5-R2FR-wep-source-worldtube-point-source-reduction-or-official-readout-data-runner.md",
    "1900_validation": OUT / "P8_Y5_BRR545_1900_VALIDATION.csv",
    "1900_point_source": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv",
    "1900_residuals": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv",
    "1900_next": OUT / "P8_Y5_PARENT_QLOC_1900_NEXT_TARGET.csv",
    "1064_common_guard": OUT / "P8_Y5_R10_1064_COMMON_MODE_GUARD.csv",
    "1083_common_alt": OUT / "P8_Y5_R10_1083_COMMON_MODE_ALTERNATIVE.csv",
    "1332_common_theorem": OUT / "P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv",
    "1337_common_update": OUT / "P8_Y5_R10_1337_COMMON_MODE_THEOREM_UPDATE.csv",
    "1338_common_status": OUT / "P8_Y5_R10_1338_COMMON_MODE_THEOREM_STATUS.csv",
    "1425_g_guard": OUT / "P8_Y5_R10_1425_MEASURED_G_COMMON_MODE_GUARD.csv",
    "1425_wep_zero": OUT / "P8_Y5_R10_1425_COMMON_MODE_WEP_ZERO_PROOF_ATTEMPT.csv",
    "1450_absorption": OUT / "P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv",
    "1602_zero": OUT / "P8_Y5_PARENT_QLOC_1602_COMMON_MODE_ZERO_THEOREM_ATTEMPT.csv",
    "1080_earth_candidates": OUT / "P8_Y5_R10_1080_EARTH_SOURCE_VECTOR_CANDIDATES.csv",
    "1083_dd_earth": OUT / "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv",
    "1083_caveat": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "1419_source_residual": OUT / "P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv",
    "1424_source_contract": OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}


SOURCE_NEEDLES = {
    "1900_doc": ["SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED", "NEXT1900_0_primary"],
    "1900_validation": ["VAL1900_OVERALL,PASS"],
    "1900_point_source": ["PSR1900_2_no_relative_hiding", "SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED"],
    "1900_residuals": ["PSE1900_2_measured_G_guard", "POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM"],
    "1900_next": ["NEXT1900_0_primary", "measured GM absorbs only universal common-mode"],
    "1064_common_guard": ["CMG1064_0_common_absorption", "relative/source-normalization residual remains physical"],
    "1083_common_alt": ["CMA1083_2_verdict", "SOURCE_COMMON_MODE_NOT_SIGNED"],
    "1332_common_theorem": ["CMT1332_0_common_mode_source_coupling", "COMMON_MODE_ROUTE_IDENTIFIED_NOT_PROMOTED"],
    "1337_common_update": ["THM1337_1_no_source_slot_is_minimal", "NEXT_TARGET_OBJECT_LANGUAGE_DERIVATION"],
    "1338_common_status": ["THMSTAT1338_1_common_mode", "CONDITIONAL_LOCAL_GR_SOURCE_ROUTE"],
    "1425_g_guard": ["GCG1425_0_common_scale", "GUARD_ACTIVE_NOT_NUMERIC"],
    "1425_wep_zero": ["CMZ1425_5_verdict", "NOT_PROVED_DEMOTE_FINITE_WEP_TO_SOURCED_INPUT_ONLY"],
    "1450_absorption": ["CMA1450_3_verdict", "GUARD_RETAINED"],
    "1602_zero": ["CMZ1602_3_verdict", "COMMON_MODE_ZERO_THEOREM_NOT_CLOSED"],
    "1080_earth_candidates": ["EARTH1080_3_common_mode_alternative", "THEOREM_ROUTE_NOT_SIGNED"],
    "1083_dd_earth": ["DD_EARTH1083_0_bulk_weighted", "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM"],
    "1083_caveat": ["SCG1083_3_no_measured_G_absorption", "NO_ABSORPTION_SHORTCUT_ALLOWED"],
    "1419_source_residual": ["SRCV1419_5_verdict", "VECTOR_DECLARED_VALUES_MISSING"],
    "1424_source_contract": ["SRCMAP1424_0_R_source", "MISSING_SOURCE_VECTOR"],
    "local_bound_claims": ["R1_WEP_source_charge", "2.8e-15"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1901_SOURCE_REGISTER.csv",
    "gm_guard_attempt": OUT / "P8_Y5_PARENT_QLOC_1901_MEASURED_G_COMMON_MODE_GUARD_ATTEMPT.csv",
    "absorption_algebra": OUT / "P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv",
    "source_vector_fill": OUT / "P8_Y5_PARENT_QLOC_1901_SOURCE_VECTOR_FILL_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1901_GUARD_SOURCE_VECTOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1901_GUARD_SOURCE_VECTOR_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1901_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1901_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1901_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1901_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1901_VALIDATION.csv",
}


BRANCH_COPIES = {
    "gm_guard_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["gm_guard_attempt"].name,
    "absorption_algebra": SOURCE_WEIGHT_DOCS / "COMMON_MODE_ABSORPTION_ALGEBRA_1901.csv",
    "source_vector_fill": QUEUE / "JR1901_SOURCE_VECTOR_FILL_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = SOURCE_NEEDLES[source_id]
        missing_needles = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(needles),
                "missing_needles": "; ".join(missing_needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing_needles else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def gm_guard_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "GMG1901_0_target",
            "claim_piece": "measured-G common-mode guard",
            "formal_statement": "Measured G_N or GM may absorb one universal, constant, same-frame, range-independent source normalization, but cannot absorb material/source-relative residuals.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the exact calibration rule needed to keep Newton/GR reduction honest",
            "source_anchor": "P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv:CMA1450_0_common_G; P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv:PSE1900_2_measured_G_guard",
            "algebra_proved": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "GMG1901_1_algebraic_absorption",
            "claim_piece": "one scalar removes one scalar",
            "formal_statement": "If source strength is S_A = G_ref M_E w_common (1+epsilon_A), choosing measured GM absorbs w_common only; epsilon_A remains observable in contrasts unless Delta_AB epsilon=0.",
            "status": "EXACT_ALGEBRA_GUARD_DERIVED",
            "proof_or_obstruction": "a single calibration scalar cannot erase a nonconstant vector over materials, source profiles, ranges, or frames",
            "source_anchor": "P8_Y5_R10_1064_COMMON_MODE_GUARD.csv:CMG1064_1_relative_not_absorbable; P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv:CMA1450_1_relative_weight",
            "algebra_proved": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "GMG1901_2_range_frame_guard",
            "claim_piece": "range/time/frame modes are not calibration",
            "formal_statement": "A local measured GM cannot absorb D_lambda, D_r, D_t, or frame-dependent source weights across WEP/R10/orbital/PPN arenas.",
            "status": "EXACT_GUARD_POLICY_DERIVED",
            "proof_or_obstruction": "range- or frame-dependent terms would change between arenas and must be retained as residual rows",
            "source_anchor": "P8_Y5_R10_1064_COMMON_MODE_GUARD.csv:CMG1064_2_range_not_absorbable; P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv:CMA1450_2_range_dependence",
            "algebra_proved": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "GMG1901_3_parent_zero_missing",
            "claim_piece": "relative source vector is theorem-zero",
            "formal_statement": "To claim local GR/WEP zero, MTS must prove epsilon_A=0 or Delta_AB epsilon=0 before calibration, from parent object language/action-current ownership.",
            "status": "RELATIVE_SOURCE_ZERO_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "common-mode route is conditional; no-source-slot/source-label forgetting is still unsigned",
            "source_anchor": "P8_Y5_R10_1337_COMMON_MODE_THEOREM_UPDATE.csv:THM1337_1_no_source_slot_is_minimal; P8_Y5_PARENT_QLOC_1602_COMMON_MODE_ZERO_THEOREM_ATTEMPT.csv:CMZ1602_3_verdict",
            "algebra_proved": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "GMG1901_4_source_vector_fallback",
            "claim_piece": "source vector fill fallback",
            "formal_statement": "If relative source zero is not derived, the source vector must be filled as explicit profile/composition/worldtube data in the same basis as material and parent coefficients.",
            "status": "SOURCE_VECTOR_FILL_REQUIRED_NONCLAIM",
            "proof_or_obstruction": "bulk Earth DD vector exists only as nonclaim context; profile/worldtube weighting and parent basis map are missing",
            "source_anchor": "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv:DD_EARTH1083_0_bulk_weighted; P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv:SRCMAP1424_0_R_source",
            "algebra_proved": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "GMG1901_5_verdict",
            "claim_piece": "measured-G guard closes WEP/local-GR source branch",
            "formal_statement": "The current corpus proves measured GM absorbs only common mode and also proves all relative source weights vanish.",
            "status": "GUARD_ALGEBRA_DERIVED_RELATIVE_ZERO_NOT_DERIVED",
            "proof_or_obstruction": "the anti-hiding guard is solid, but it does not by itself prove relative source-vector zero; source-label/no-source-slot theorem or finite source vector still needed",
            "source_anchor": "GMG1901_0_target through GMG1901_4_source_vector_fallback",
            "algebra_proved": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def absorption_algebra_rows() -> list[dict[str, Any]]:
    return [
        {"algebra_id": "ALG1901_0_decomposition", "statement": "w_A = w_common * (1 + epsilon_A)", "result": "calibration may choose G_meas = G_ref * w_common", "surviving_term": "epsilon_A", "why_it_matters": "one scalar calibration cannot remove a material/source vector", "status": "ALGEBRA_ACCEPTED_GUARD", "valid_for_claim": False},
        {"algebra_id": "ALG1901_1_contrast", "statement": "Delta_AB ln a = epsilon_A - epsilon_B + higher order", "result": "relative WEP/source contrast survives measured GM", "surviving_term": "Delta_AB epsilon", "why_it_matters": "WEP tests are contrast tests; common mode cancels, relative mode does not", "status": "ALGEBRA_ACCEPTED_GUARD", "valid_for_claim": False},
        {"algebra_id": "ALG1901_2_range", "statement": "w(lambda,r,t,frame) cannot be represented by one constant G_meas", "result": "range/time/frame hair must be retained", "surviving_term": "D_lambda w; D_r w; D_t w; Delta_frame w", "why_it_matters": "prevents transfer of one local calibration across R10/orbit/PPN", "status": "ALGEBRA_ACCEPTED_GUARD", "valid_for_claim": False},
        {"algebra_id": "ALG1901_3_claim_limit", "statement": "guard != zero theorem", "result": "guard blocks cheating but does not prove epsilon_A=0", "surviving_term": "source-vector or no-source-slot theorem", "why_it_matters": "this is a discipline theorem, not a local-GR pass", "status": "NO_CLAIM_PROMOTION", "valid_for_claim": False},
    ]


def source_vector_fill_rows() -> list[dict[str, Any]]:
    return [
        {"fill_id": "SVF1901_0_bulk_dd_context", "object": "bulk Earth DD vector", "current_value": "Q_alpha=1.691260686750872e-03; Q_surface=-1.211918219995745e-02", "current_status": "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM", "missing_for_claim": "profile/worldtube weighting, MTS parent basis map, material tensor matching", "source_anchor": "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv:DD_EARTH1083_0_bulk_weighted", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "SVF1901_1_profile_weighting", "object": "profile/worldtube weighted Earth source vector", "current_value": "MISSING", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "missing_for_claim": "Earth profile or point-source/common-mode theorem with residual bound", "source_anchor": "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_0_profile_weighting", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "SVF1901_2_parent_basis_map", "object": "MTS parent basis to source-vector basis", "current_value": "MISSING", "current_status": "MISSING_PARENT_OPERATOR_BASIS_MAP", "missing_for_claim": "map from parent residual vector to DD/source/material response basis", "source_anchor": "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_1_parent_to_DD_map", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "SVF1901_3_source_vector_contract", "object": "R_source^Earth", "current_value": "MISSING_SOURCE_VECTOR", "current_status": "SOURCE_VECTOR_CONTRACT_OPEN", "missing_for_claim": "derive common-mode theorem or source-backed composition/worldtube vector", "source_anchor": "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv:SRCMAP1424_0_R_source", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "SVF1901_4_residual_coefficients", "object": "r_source residual coefficients", "current_value": "VECTOR_DECLARED_VALUES_MISSING", "current_status": "PARENT_RESIDUAL_COEFFICIENTS_MISSING", "missing_for_claim": "qbar_source_weight/current_rescaling/non-Hilbert/geometric/readout coefficients", "source_anchor": "P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv:SRCV1419_5_verdict", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "SVF1901_5_absorption_guard", "object": "measured GM guard", "current_value": "algebra accepted; no relative absorption", "current_status": "GUARD_DERIVED_NONCLAIM", "missing_for_claim": "relative source vector theorem-zero or executable finite vector", "source_anchor": "P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv:ALG1901_3_claim_limit", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "SVF1901_6_verdict", "object": "source-vector executable branch", "current_value": "NONCLAIM_LEDGER_ONLY", "current_status": "SOURCE_VECTOR_NOT_EXECUTABLE_NONCLAIM", "missing_for_claim": "SVF1901_1 through SVF1901_4 filled or theorem-zero", "source_anchor": "SVF1901_0_bulk_dd_context through SVF1901_5_absorption_guard", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1901_0_use_guard_as_zero", "guard_algebra_ok": True, "relative_zero_proved": False, "source_vector_filled": False, "uses_bulk_as_profile": False, "uses_measured_g_hiding": False, "score_attempt": False, "expected_status": "REFUSED_GUARD_IS_NOT_ZERO_THEOREM", "valid_for_claim": False},
        {"case_id": "DRY1901_1_measured_g_hiding", "guard_algebra_ok": True, "relative_zero_proved": False, "source_vector_filled": False, "uses_bulk_as_profile": False, "uses_measured_g_hiding": True, "score_attempt": False, "expected_status": "REFUSED_MEASURED_G_RELATIVE_HIDING", "valid_for_claim": False},
        {"case_id": "DRY1901_2_bulk_as_profile", "guard_algebra_ok": True, "relative_zero_proved": False, "source_vector_filled": False, "uses_bulk_as_profile": True, "uses_measured_g_hiding": False, "score_attempt": False, "expected_status": "REFUSED_BULK_VECTOR_AS_PROFILE_WEIGHTED_SOURCE", "valid_for_claim": False},
        {"case_id": "DRY1901_3_source_missing", "guard_algebra_ok": True, "relative_zero_proved": False, "source_vector_filled": False, "uses_bulk_as_profile": False, "uses_measured_g_hiding": False, "score_attempt": True, "expected_status": "REFUSED_SOURCE_VECTOR_NOT_EXECUTABLE", "valid_for_claim": False},
        {"case_id": "DRY1901_4_guard_missing", "guard_algebra_ok": False, "relative_zero_proved": True, "source_vector_filled": True, "uses_bulk_as_profile": False, "uses_measured_g_hiding": False, "score_attempt": False, "expected_status": "REFUSED_GUARD_ALGEBRA_MISSING", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    guard_algebra_ok = bool_string(row["guard_algebra_ok"]) == "true"
    relative_zero_proved = bool_string(row["relative_zero_proved"]) == "true"
    source_vector_filled = bool_string(row["source_vector_filled"]) == "true"
    uses_bulk_as_profile = bool_string(row["uses_bulk_as_profile"]) == "true"
    uses_measured_g_hiding = bool_string(row["uses_measured_g_hiding"]) == "true"
    score_attempt = bool_string(row["score_attempt"]) == "true"
    if not guard_algebra_ok:
        status = "REFUSED_GUARD_ALGEBRA_MISSING"
    elif uses_measured_g_hiding:
        status = "REFUSED_MEASURED_G_RELATIVE_HIDING"
    elif uses_bulk_as_profile:
        status = "REFUSED_BULK_VECTOR_AS_PROFILE_WEIGHTED_SOURCE"
    elif not relative_zero_proved and not source_vector_filled and score_attempt:
        status = "REFUSED_SOURCE_VECTOR_NOT_EXECUTABLE"
    elif not relative_zero_proved:
        status = "REFUSED_GUARD_IS_NOT_ZERO_THEOREM"
    else:
        status = "WOULD_REQUIRE_FULL_NUMERIC_NONCLAIM_REVIEW"
    return {
        "case_id": row["case_id"],
        "computed_status": status,
        "expected_status": row["expected_status"],
        "status_match": status == row["expected_status"],
        "claim_allowed": False,
        "valid_for_claim": False,
        "generated_utc": GENERATED_UTC,
    }


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in cases]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG1901_0_guard", "condition": "measured-G common-mode absorption algebra is explicit", "current_status": "PASS_ALGEBRA_GUARD_DERIVED_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv:ALG1901_0_decomposition", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1901_1_relative_zero", "condition": "relative source vector is parent theorem-zero", "current_status": "FAIL_RELATIVE_SOURCE_ZERO_NOT_PARENT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1901_MEASURED_G_COMMON_MODE_GUARD_ATTEMPT.csv:GMG1901_3_parent_zero_missing", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1901_2_source_vector", "condition": "finite source vector is profile-weighted and executable if not zero", "current_status": "FAIL_SOURCE_VECTOR_NOT_EXECUTABLE_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1901_SOURCE_VECTOR_FILL_NONCLAIM.csv:SVF1901_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1901_3_verdict", "condition": "measured-G/source-vector branch supports WEP/local-GR claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1901_0_guard through CG1901_2_source_vector", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1901_0_guard", "decision": "accept measured-G guard as an algebraic discipline theorem", "reason": "one scalar calibration removes one universal scalar only; it cannot remove relative source vectors, range hair, or frame/time hair", "status": "GUARD_ALGEBRA_ACCEPTED_NONCLAIM", "next_dependency": "relative source zero theorem or source-vector fill", "valid_for_claim": False},
        {"decision_id": "DEC1901_1_zero", "decision": "do not claim source-vector zero", "reason": "no-source-slot/source-label forgetting and common-mode zero theorem are not parent-signed", "status": "RELATIVE_SOURCE_ZERO_UNSIGNED", "next_dependency": "source-label forgetting before GM calibration", "valid_for_claim": False},
        {"decision_id": "DEC1901_2_next", "decision": "attack source-label forgetting before GM calibration", "reason": "it is the minimal theorem that would turn the guard from anti-cheat rule into local-GR source universality", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1902 source-label forgetting or profile source-vector map", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1901_0_primary",
            "selection_status": "selected",
            "target_doc": "1902-Y5-R2FR-source-label-forgetting-before-GM-calibration-or-profile-source-vector-map.md",
            "target_script": "scripts/Y5_R2FR_source_label_forgetting_before_GM_calibration_or_profile_source_vector_map_1902.py",
            "objective": "try to prove source labels are forgotten before measured-G calibration; if it fails, build a profile/worldtube source-vector map as nonclaim",
            "success_condition": "parent-signed source-label forgetting/no-source-slot theorem, or source-vector profile map rows with no measured-G hiding",
            "do_not": "do not treat the measured-G guard as a zero theorem, do not use bulk Earth DD vector as profile-weighted source, and do not score WEP from unfilled source vectors",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1901_0_positive", "area": "Newton/GR calibration discipline", "summary": "measured-G/common-mode absorption is now an explicit algebraic guard", "risk_level": "ANTI_CHEAT_GUARD_STRONG", "project_meaning": "this strengthens the derivation discipline: Newtonian calibration cannot hide WEP-active source weights", "next_action": "prove source-label forgetting or fill finite source vector", "valid_for_claim": False},
        {"status_id": "STAT1901_1_open", "area": "local-GR source universality", "summary": "relative source-vector zero remains unproved and source vector is not executable", "risk_level": "CORE_COUPLING_GAP_REMAINS", "project_meaning": "we have a good guardrail, not yet a local-GR source theorem", "next_action": "1902 source-label forgetting before GM calibration", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "gm_guard_attempt": gm_guard_attempt_rows(),
        "absorption_algebra": absorption_algebra_rows(),
        "source_vector_fill": source_vector_fill_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "NONCLAIM", "CLAIM_BLOCKED", "NOT_EXECUTABLE", "REFUSED"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            text = " ".join(str(value) for value in row.values())
            if any(marker in text for marker in markers):
                for field in fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/nonclaim rows are not score-ready"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1901_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    guard_rows = csv_rows(OUTPUTS["gm_guard_attempt"])
    checks.append({"validation_id": "VAL1901_01_guard_verdict", "status": "PASS" if any(row["attempt_id"] == "GMG1901_5_verdict" and row["status"] == "GUARD_ALGEBRA_DERIVED_RELATIVE_ZERO_NOT_DERIVED" for row in guard_rows) else "FAIL", "detail": "measured-G guard algebra accepted but relative zero remains unsigned", "valid_for_claim": False})
    algebra_rows = csv_rows(OUTPUTS["absorption_algebra"])
    checks.append({"validation_id": "VAL1901_02_algebra", "status": "PASS" if len(algebra_rows) >= 4 and all(row["valid_for_claim"] == "False" for row in algebra_rows) else "FAIL", "detail": "absorption algebra rows recorded as guard/nonclaim", "valid_for_claim": False})
    source_rows = csv_rows(OUTPUTS["source_vector_fill"])
    checks.append({"validation_id": "VAL1901_03_source_vector", "status": "PASS" if len(source_rows) >= 7 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in source_rows) else "FAIL", "detail": "source-vector fill rows remain nonclaim/not executable", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1901_04_dryrun", "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows) else "FAIL", "detail": "dry-run refuses guard-as-zero, measured-G hiding, bulk-as-profile, missing vector, and missing guard", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1901_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1901_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1901_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1901_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1902 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1901_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1901_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1901_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1901_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1901_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = list(FORMALIZATION.rglob("*1901*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1901_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1901_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1901_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1901 measured-G common-mode guard or source-vector fill", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1901 - Measured-G Common-Mode Guard Or Source-Vector Fill

## Purpose

This checkpoint tests whether measured `G_N` / `GM` can absorb source-weight effects without cheating. It accepts the algebraic common-mode guard if valid, then checks whether the relative source vector is actually zero or executable.

## Result

- A single measured-`GM` calibration can absorb one universal common scalar.
- It cannot absorb relative material/source vectors, range dependence, frame dependence, or time dependence.
- This is a real algebraic guardrail, but it is not a parent theorem that relative source weights vanish.
- Bulk Earth DD numbers remain context only; they are not a profile/worldtube-weighted source vector.
- No WEP/local-GR claim is made.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Measured-G Guard Attempt

{markdown_table(rows_by_name["gm_guard_attempt"])}

## Common-Mode Absorption Algebra

{markdown_table(rows_by_name["absorption_algebra"])}

## Source-Vector Fill Nonclaim

{markdown_table(rows_by_name["source_vector_fill"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
