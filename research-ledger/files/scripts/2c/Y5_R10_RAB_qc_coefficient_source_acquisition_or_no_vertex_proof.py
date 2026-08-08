from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1311"
TITLE = "1311-Y5-R10-RAB-qc-coefficient-source-acquisition-or-no-vertex-proof"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
NO_VERTEX_PROBE_PATH = OUT_DIR / f"{PACK_ID}_NO_VERTEX_PROBE.csv"
COEFFICIENT_SOURCE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_COEFFICIENT_SOURCE_AUDIT.csv"
THRESHOLD_IMPORT_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_THRESHOLD_IMPORT_AUDIT_NONCLAIM.csv"
RUNNER_DRYRUN_GATE_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_DRYRUN_GATE.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1311_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        NO_VERTEX_PROBE_PATH,
        COEFFICIENT_SOURCE_AUDIT_PATH,
        THRESHOLD_IMPORT_AUDIT_PATH,
        RUNNER_DRYRUN_GATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1311_0_1310_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1310_NEXT_TARGET.csv",
            "needle": "NEXT1310_0_1311",
            "role": "handoff into q_c coefficient source acquisition/no-vertex proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_1_1310_coefficients",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1310_QC_COEFFICIENT_ACQUISITION_NONCLAIM.csv",
            "needle": "QCA1310_6_qc_total",
            "role": "coefficient rows staged by 1310",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_2_1310_templates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1310_R10_QC_TEMPLATE_BRIDGE_NONCLAIM.csv",
            "needle": "RTB1310_3_total_alpha_envelope",
            "role": "nonclaim R10 bridge templates requiring q_c values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_3_1098_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "needle": "OWNER_ACTION_SIGNATURE_NOT_DERIVED",
            "role": "no-vertex owner action signature not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_4_1046_qbar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "needle": "QCC1046_3_qbar_constants_abs",
            "role": "existing qbar coefficient component rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_5_1046_split",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "needle": "CMA1046_5_verdict",
            "role": "constant/marker split says zero is not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_6_1096_candidate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1096_WEP_COEFFICIENT_CANDIDATE_NONCLAIM.csv",
            "needle": "MISSING_C_ALPHA_DD_ZERO_THEOREM_OR_SOURCE_PRIOR",
            "role": "prior WEP coefficient candidate is missing prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_7_1096_import",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1096_WEP_COEFFICIENT_BOUND_IMPORT.csv",
            "needle": "threshold only",
            "role": "threshold import is not an MTS coefficient prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_8_1097_candidate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_COEFFICIENT_CANDIDATE_NONCLAIM.csv",
            "needle": "MISSING_SCOREABLE_CONSTANT_COEFFICIENT",
            "role": "constant coefficient candidate missing prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_9_1097_import",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_COEFFICIENT_BOUND_IMPORT.csv",
            "needle": "threshold only",
            "role": "constant threshold import is not MTS coefficient prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_10_1098_candidate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_CONSTANT_COEFFICIENT_CANDIDATE_NONCLAIM.csv",
            "needle": "MISSING_OWNER_SIGNATURE_OR_SOURCE_BACKED_C_ALPHA",
            "role": "ordinary owner coefficient candidate still missing owner or source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1311_11_1098_import",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_CONSTANT_COEFFICIENT_BOUND_IMPORT.csv",
            "needle": "threshold only",
            "role": "ordinary owner threshold import is not MTS coefficient prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    no_vertex_probe = [
        {
            "probe_id": "NVP1311_0_b_alpha",
            "component": "b_alpha",
            "no_vertex_clause": "unique EM/gauge kinetic owner; forbid f_X(Xhat)F^2 and lambda_A F^2",
            "current_evidence": "1098 says FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL; 1046 keeps alpha_EM open.",
            "result": "NO_VERTEX_NOT_PROVED",
            "coefficient_fallback": "QCSA1311_0_b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "NVP1311_1_b_mA",
            "component": "b_mA",
            "no_vertex_clause": "no Xhat-dependent masses, Yukawas, QCD scale, binding response, or material response slots",
            "current_evidence": "1098 says matter spectrum owner is not parent-signed; 1046 keeps particle masses/mass ratios open.",
            "result": "NO_VERTEX_NOT_PROVED",
            "coefficient_fallback": "QCSA1311_1_b_mA",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "NVP1311_2_qbar_marker",
            "component": "qbar_marker_abs",
            "no_vertex_clause": "material markers, preparation labels, isotope fractions, and shadow-frame slots are absent/pure gauge/source-independent",
            "current_evidence": "1046 says NO_MARKER_THEOREM_NOT_PARENT_SIGNED; 1310 keeps marker row live.",
            "result": "NO_VERTEX_NOT_PROVED",
            "coefficient_fallback": "QCSA1311_4_qbar_marker_abs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "NVP1311_3_source_weight",
            "component": "qbar_source_weight",
            "no_vertex_clause": "no w_A(Xhat)S_A, kappa_A(Xhat)T_A, or source-only material multiplier before variation",
            "current_evidence": "1098 source-weight exclusion is unsigned; 1046 keeps relative source weights parent-unsigned.",
            "result": "NO_VERTEX_NOT_PROVED",
            "coefficient_fallback": "QCSA1311_5_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "NVP1311_4_verdict",
            "component": "q_c total",
            "no_vertex_clause": "all selected no-vertex clauses close together",
            "current_evidence": "no selected clause is parent-signed in current evidence",
            "result": "NO_COMPONENT_THEOREM_ZERO_FOUND",
            "coefficient_fallback": "stage coefficient acquisition blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    coefficient_source_audit = [
        {
            "audit_id": "QCSA1311_0_b_alpha",
            "symbol": "b_alpha",
            "current_best_local_source": "P8_Y5_R10_1096/1097/1098 coefficient candidates and threshold imports",
            "found_value": "NONE",
            "found_bound_or_threshold": "c_alpha_DD threshold 8.3202449332435330e-10 dimensionless, nonclaim threshold only",
            "why_not_scoreable": "threshold is an allowed upper fence, not an MTS-predicted coefficient value or theorem-zero",
            "acquisition_action": "derive no-EM-counterterm theorem or source a real b_alpha/c_alpha coefficient with normalization and material sensitivity map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QCSA1311_1_b_mA",
            "symbol": "b_mA",
            "current_best_local_source": "1046 qbar rows and 1098 owner attempt",
            "found_value": "NONE",
            "found_bound_or_threshold": "NONE",
            "why_not_scoreable": "no mass-ratio/binding coefficient value or theorem-zero source is present",
            "acquisition_action": "derive no-mass/binding hidden vertex theorem or source b_mA/material sensitivity coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QCSA1311_2_b_clock_i",
            "symbol": "b_clock_i",
            "current_best_local_source": "1046 qbar rows",
            "found_value": "NONE",
            "found_bound_or_threshold": "NONE",
            "why_not_scoreable": "clock projection inherits b_alpha/b_mass debt plus missing sensitivity matrix",
            "acquisition_action": "source clock sensitivity matrix and upstream coefficients, or derive clock readout owner theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QCSA1311_3_qbar_constants_abs",
            "symbol": "qbar_constants_abs",
            "current_best_local_source": "1046 qbar constants envelope",
            "found_value": "NONE",
            "found_bound_or_threshold": "NONE",
            "why_not_scoreable": "component coefficients are missing and no-cancellation envelope cannot be evaluated",
            "acquisition_action": "fill b_alpha, b_mA, b_clock_i, and retained charge/source constants or prove all zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QCSA1311_4_qbar_marker_abs",
            "symbol": "qbar_marker_abs",
            "current_best_local_source": "1046 marker split and R10 marker template",
            "found_value": "NONE",
            "found_bound_or_threshold": "NONE",
            "why_not_scoreable": "no marker theorem and no marker coefficient values/source paths exist",
            "acquisition_action": "derive no-marker/no-shadow theorem or source marker sensitivity coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QCSA1311_5_qbar_source_weight",
            "symbol": "qbar_source_weight",
            "current_best_local_source": "1046 source-weight audit and 950 source-normalization countermodel",
            "found_value": "NONE",
            "found_bound_or_threshold": "NONE",
            "why_not_scoreable": "source-weight exclusion is unsigned and no kappa_A/w_A coefficient is sourced",
            "acquisition_action": "derive source-weight exclusion theorem or source qbar_source_weight coefficient with material/source tags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QCSA1311_6_qc_total",
            "symbol": "q_c^T_abs",
            "current_best_local_source": "1310 q_c total envelope",
            "found_value": "NONE",
            "found_bound_or_threshold": "NONE",
            "why_not_scoreable": "all component coefficients are missing or theorem-unsigned",
            "acquisition_action": "only score after components plus lambda_c, Pi_MQ, measured GM, and alpha_bound(lambda) are supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    threshold_import_audit = [
        {
            "threshold_id": "TIA1311_0_1096_c_alpha",
            "source_table": "P8_Y5_R10_1096_WEP_COEFFICIENT_BOUND_IMPORT.csv",
            "quantity": "c_alpha_DD",
            "threshold_value": "8.3202449332435330e-10",
            "units": "dimensionless",
            "status": "THRESHOLD_ONLY_NOT_PREDICTION",
            "use_allowed": "private acceptance fence after MTS coefficient exists",
            "use_forbidden": "do not treat as predicted b_alpha/c_alpha value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "threshold_id": "TIA1311_1_1097_c_alpha",
            "source_table": "P8_Y5_R10_1097_CONSTANT_COEFFICIENT_BOUND_IMPORT.csv",
            "quantity": "c_alpha_DD",
            "threshold_value": "8.3202449332435330e-10",
            "units": "dimensionless",
            "status": "THRESHOLD_ONLY_NOT_PREDICTION",
            "use_allowed": "private acceptance fence after MTS coefficient exists",
            "use_forbidden": "do not treat as source-backed constant-sector coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "threshold_id": "TIA1311_2_1098_c_alpha",
            "source_table": "P8_Y5_R10_1098_CONSTANT_COEFFICIENT_BOUND_IMPORT.csv",
            "quantity": "c_alpha_DD",
            "threshold_value": "8.3202449332435330e-10",
            "units": "dimensionless",
            "status": "THRESHOLD_ONLY_NOT_PREDICTION",
            "use_allowed": "private acceptance fence after MTS coefficient exists",
            "use_forbidden": "do not treat as ordinary-owner coefficient prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_dryrun_gate = [
        {
            "gate_id": "RDG1311_0_lambda",
            "requirement": "lambda_c or lambda grid",
            "current_status": "MISSING",
            "runner_effect": "R10 q_c runner cannot execute",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "RDG1311_1_source_projection",
            "requirement": "Pi_M^H[Q_c^H(lambda)] or source envelope",
            "current_status": "MISSING",
            "runner_effect": "alpha numerator cannot be computed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "RDG1311_2_test_charge",
            "requirement": "q_c component coefficients or theorem-zero",
            "current_status": "MISSING",
            "runner_effect": "test charge cannot be computed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "RDG1311_3_measured_GM",
            "requirement": "same-frame measured GM normalization",
            "current_status": "MISSING",
            "runner_effect": "dimensionless alpha normalization remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "RDG1311_4_bound_curve",
            "requirement": "promoted real alpha_bound(lambda) curve",
            "current_status": "MISSING_OR_NONCLAIM_PRIOR_ONLY",
            "runner_effect": "no R10 claim comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1311_0_no_vertex",
            "claim": "selected no-vertex clauses prove q_c components zero",
            "current_status": "BLOCKED_NO_VERTEX_NOT_PROVED",
            "reason": "owner action signature remains contract/counterexample stage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1311_1_source_backed_coefficients",
            "claim": "q_c coefficients are source-backed",
            "current_status": "BLOCKED_NO_PREDICTED_VALUES_FOUND",
            "reason": "only threshold fences and missing-value candidate rows are present",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1311_2_runner",
            "claim": "R10 q_c runner can execute",
            "current_status": "BLOCKED_DRYRUN_REQUIREMENTS_MISSING",
            "reason": "lambda, Pi_MQ, q_c values, GM normalization, and promoted bound curve are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1311_3_local_GR",
            "claim": "local GR/R10 pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "no source/test charge theorem-zero and no executable residual bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1311_0_no_component_closed",
            "decision": "no q_c component closes at 1311",
            "because": "no no-vertex theorem is parent-signed and no source-backed coefficient prediction is present",
            "next_action": "focus on b_alpha first because it has existing threshold fences and a sharp owner clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1311_1_thresholds_not_predictions",
            "decision": "retain imported thresholds only as acceptance fences",
            "because": "threshold bounds do not supply MTS-predicted coefficients",
            "next_action": "derive or source b_alpha/c_alpha before using the threshold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1311_0_1312",
            "target_file": "1312-Y5-R10-RAB-b-alpha-no-vertex-or-source-backed-coefficient.md",
            "target_script": "scripts/Y5_R10_RAB_b_alpha_no_vertex_or_source_backed_coefficient.py",
            "task": "focus on b_alpha/c_alpha: try to prove the no-EM-counterterm owner clause, or source a real b_alpha/c_alpha coefficient with normalization before applying threshold fences",
            "success_condition": "b_alpha is theorem-zero, source-backed numeric, or demoted to a fully explicit coefficient-acquisition blocker",
            "do_not": "do not use c_alpha_DD thresholds as MTS predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(NO_VERTEX_PROBE_PATH, no_vertex_probe)
    write_csv(COEFFICIENT_SOURCE_AUDIT_PATH, coefficient_source_audit)
    write_csv(THRESHOLD_IMPORT_AUDIT_PATH, threshold_import_audit)
    write_csv(RUNNER_DRYRUN_GATE_PATH, runner_dryrun_gate)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1311_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1311_1_no_vertex_not_proved",
            "selected no-vertex clauses do not prove component zero",
            any(row["probe_id"] == "NVP1311_4_verdict" and row["result"] == "NO_COMPONENT_THEOREM_ZERO_FOUND" for row in no_vertex_probe),
            ";".join(str(row["probe_id"]) + "=" + str(row["result"]) for row in no_vertex_probe),
        )
    )
    validations.append(
        validation_row(
            "VAL1311_2_no_source_backed_values",
            "coefficient source audit finds no source-backed q_c values",
            len(coefficient_source_audit) == 7 and all(str(row["found_value"]) == "NONE" for row in coefficient_source_audit),
            ";".join(str(row["audit_id"]) + "=" + str(row["found_value"]) for row in coefficient_source_audit),
        )
    )
    validations.append(
        validation_row(
            "VAL1311_3_thresholds_nonclaim",
            "threshold imports are classified as thresholds not predictions",
            len(threshold_import_audit) == 3 and all(str(row["status"]) == "THRESHOLD_ONLY_NOT_PREDICTION" for row in threshold_import_audit),
            ";".join(str(row["threshold_id"]) + "=" + str(row["threshold_value"]) for row in threshold_import_audit),
        )
    )
    validations.append(
        validation_row(
            "VAL1311_4_runner_dryrun_blocks",
            "runner dry-run requirements remain missing",
            len(runner_dryrun_gate) == 5 and all(str(row["current_status"]).startswith("MISSING") for row in runner_dryrun_gate),
            ";".join(str(row["gate_id"]) + "=" + str(row["current_status"]) for row in runner_dryrun_gate),
        )
    )
    validations.append(
        validation_row(
            "VAL1311_5_claim_gates_block",
            "claim gates block no-vertex/source-backed coefficient/R10 promotion",
            len(claim_gates) == 4 and all(str(row["current_status"]).startswith("BLOCKED") for row in claim_gates),
            ";".join(str(row["gate_id"]) + "=" + str(row["current_status"]) for row in claim_gates),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        NO_VERTEX_PROBE_PATH,
        COEFFICIENT_SOURCE_AUDIT_PATH,
        THRESHOLD_IMPORT_AUDIT_PATH,
        RUNNER_DRYRUN_GATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as error:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{error}")
    validations.append(validation_row("VAL1311_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1311_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1311_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, no_vertex_probe, coefficient_source_audit, threshold_import_audit, runner_dryrun_gate, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1311_9_next_target_1312",
            "next target routes to b_alpha no-vertex or source-backed coefficient",
            next_target[0]["next_id"] == "NEXT1311_0_1312" and "b-alpha" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1311_10_overall",
            "overall 1311 validation",
            overall_pass,
            "1311 finds no q_c component theorem-zero and no source-backed coefficient values; imported thresholds remain nonclaim fences; runner remains blocked; next target is b_alpha",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1311 Y5 R10 RAB qc coefficient source acquisition or no vertex proof

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** no `q_c` component is theorem-zero or source-backed from the current corpus. The existing `c_alpha_DD` rows are useful threshold fences, but they are **not** MTS coefficient predictions.

**Main progress:** every surviving `q_c` component now has a source-audit row: `b_alpha`, `b_mA`, `b_clock_i`, `qbar_constants_abs`, `qbar_marker_abs`, `qbar_source_weight`, and `q_c^T_abs`. The runner dry-run gate explicitly refuses R10 execution until real values/theorems exist.

**Decision:** focus next on `b_alpha/c_alpha`, because it has the sharpest no-vertex clause and existing threshold fences. Do not use those thresholds as predictions.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## No-Vertex Probe

{markdown_table(no_vertex_probe, ["probe_id", "component", "no_vertex_clause", "current_evidence", "result", "coefficient_fallback", "valid_for_claim", "claim_allowed"])}

## Coefficient Source Audit

{markdown_table(coefficient_source_audit, ["audit_id", "symbol", "current_best_local_source", "found_value", "found_bound_or_threshold", "why_not_scoreable", "acquisition_action", "valid_for_claim", "claim_allowed"])}

## Threshold Import Audit

{markdown_table(threshold_import_audit, ["threshold_id", "source_table", "quantity", "threshold_value", "units", "status", "use_allowed", "use_forbidden", "valid_for_claim", "claim_allowed"])}

## Runner Dry-Run Gate

{markdown_table(runner_dryrun_gate, ["gate_id", "requirement", "current_status", "runner_effect", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
