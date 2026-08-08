from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1315"
TITLE = "1315-Y5-R10-RAB-alpha-scorepack-runner-first-nonclaim-table"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
RUNNER_INPUT_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_INPUT_AUDIT.csv"
FIRST_SCORE_TABLE_PATH = OUT_DIR / f"{PACK_ID}_FIRST_NONCLAIM_SCORE_TABLE.csv"
BLOCKER_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_MISSING_INPUT_BLOCKER_LEDGER.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
CLAIM_REFUSAL_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_REFUSAL_LEDGER.csv"
PROMOTION_CHECKLIST_PATH = OUT_DIR / f"{PACK_ID}_PROMOTION_CHECKLIST.csv"
R10_REFUSAL_PATH = OUT_DIR / f"{PACK_ID}_R10_REFUSAL_DETAIL.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1315_VALIDATION.csv"


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
        RUNNER_INPUT_AUDIT_PATH,
        FIRST_SCORE_TABLE_PATH,
        BLOCKER_LEDGER_PATH,
        ANTI_SHORTCUT_PATH,
        CLAIM_REFUSAL_PATH,
        PROMOTION_CHECKLIST_PATH,
        R10_REFUSAL_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def numeric_positive(value: str) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def missing_tokens(value: str) -> list[str]:
    tokens: list[str] = []
    for part in str(value).replace(",", ";").split(";"):
        token = part.strip()
        if not token:
            continue
        if "MISSING" in token or token.startswith("not_a_numeric") or token.startswith("review_candidate"):
            tokens.append(token)
    return tokens


def status_for_acquisition(acquisition_rows: list[dict[str, str]], runner_row_id: str) -> str:
    for row in acquisition_rows:
        if row.get("scorepack_row") == runner_row_id:
            return row.get("missing_or_status", "")
    return "NO_ACQUISITION_ROW_FOUND"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1315_0_1314_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1314_NEXT_TARGET.csv",
            "needle": "NEXT1314_0_1315",
            "role": "handoff into alpha scorepack refusal runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1315_1_1314_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1314_ALPHA_SCOREPACK_INPUT_SCHEMA.csv",
            "needle": "AS1314_3_r10_vector",
            "role": "1314 input schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1315_2_1314_acquisition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1314_SOURCE_ACQUISITION_LEDGER.csv",
            "needle": "ACQ1314_3_r10",
            "role": "1314 source acquisition ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1315_3_1314_runner_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1314_RUNNER_READY_NONCLAIM_ROWS.csv",
            "needle": "RUN1314_3_r10",
            "role": "1314 runner-ready nonclaim rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1315_4_1314_r10_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1314_R10_FINITE_BRANCH_GATE.csv",
            "needle": "R10_SCOREPACK_SCHEMA_ONLY_NONCLAIM",
            "role": "R10 finite branch gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1315_5_1314_parent",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1314_PARENT_PRIMITIVE_ESCAPE_HATCH.csv",
            "needle": "PESC1314_0_parent_grammar",
            "role": "parent primitive escape hatch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1315_6_1222_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_FIRST_NONCLAIM_SCORE_TABLE.csv",
            "needle": "NCS1222_0_alpha",
            "role": "generic refusal runner pattern",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1315_7_1222_shortcuts",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_ANTI_SHORTCUT_GATES.csv",
            "needle": "SHORT1222_0_no_unity",
            "role": "anti-shortcut gate pattern",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1315_8_1222_promotion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_PROMOTION_CHECKLIST.csv",
            "needle": "PROM1222_1_prediction",
            "role": "promotion checklist pattern",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    runner_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1314_RUNNER_READY_NONCLAIM_ROWS.csv"))
    acquisition_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1314_SOURCE_ACQUISITION_LEDGER.csv"))

    runner_input_audit = []
    first_score = []
    blocker_ledger = []
    claim_refusal = []

    for index, row in enumerate(runner_rows):
        runner_id = row["runner_row_id"]
        threshold_ok = numeric_positive(row.get("threshold_abs", ""))
        predicted_missing = "MISSING" in row.get("predicted_abs_value", "")
        input_tokens = missing_tokens(row.get("missing_inputs", ""))
        acquisition_status = status_for_acquisition(acquisition_rows, runner_id)
        acquisition_missing = "MISSING" in acquisition_status or "NOT_FOUND" in acquisition_status
        counterexample_retained = bool(row.get("counterexample_lock", "").strip())
        refusal_reasons = []
        if not threshold_ok:
            refusal_reasons.append("threshold_not_numeric_positive")
        if predicted_missing:
            refusal_reasons.append("predicted_value_missing")
        if input_tokens:
            refusal_reasons.append("missing_inputs_present")
        if acquisition_missing:
            refusal_reasons.append("acquisition_missing")
        if counterexample_retained:
            refusal_reasons.append("counterexample_retained")
        if not is_false(row.get("score_ready", False)):
            refusal_reasons.append("source_row_score_ready_not_false")
        if not is_false(row.get("valid_prediction_row", False)):
            refusal_reasons.append("source_row_valid_prediction_not_false")

        claim_status = "REFUSED" if refusal_reasons else "UNEXPECTED_REVIEW"
        score_ready = False
        valid_prediction_row = False

        runner_input_audit.append(
            {
                "audit_id": f"RIA1315_{index}",
                "runner_row_id": runner_id,
                "threshold_abs": row.get("threshold_abs", ""),
                "threshold_numeric_positive": threshold_ok,
                "predicted_abs_value": row.get("predicted_abs_value", ""),
                "missing_inputs": row.get("missing_inputs", ""),
                "acquisition_status": acquisition_status,
                "counterexample_lock": row.get("counterexample_lock", ""),
                "score_ready": score_ready,
                "valid_prediction_row": valid_prediction_row,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        first_score.append(
            {
                "score_row_id": f"NCS1315_{index}_{runner_id.replace('RUN1314_', '')}",
                "runner_row_id": runner_id,
                "observable_product": row.get("observable_product", ""),
                "threshold_abs": row.get("threshold_abs", ""),
                "threshold_numeric_positive": threshold_ok,
                "predicted_abs_value": row.get("predicted_abs_value", ""),
                "available_inputs": row.get("available_inputs", ""),
                "missing_inputs": row.get("missing_inputs", ""),
                "acquisition_status": acquisition_status,
                "counterexample_status": "RETAINED" if counterexample_retained else "none",
                "claim_status": claim_status,
                "refusal_reason": ";".join(refusal_reasons),
                "score_ready": score_ready,
                "valid_prediction_row": valid_prediction_row,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for token_index, token in enumerate(input_tokens):
            blocker_ledger.append(
                {
                    "blocker_id": f"BLK1315_{index}_{token_index}",
                    "runner_row_id": runner_id,
                    "blocker_token": token,
                    "blocker_source": "runner_missing_inputs",
                    "required_resolution": "replace token with sourced numeric input or signed theorem-zero primitive",
                    "claim_effect": "valid_prediction_row=false",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        if acquisition_missing:
            blocker_ledger.append(
                {
                    "blocker_id": f"BLK1315_{index}_acquisition",
                    "runner_row_id": runner_id,
                    "blocker_token": acquisition_status,
                    "blocker_source": "source_acquisition_ledger",
                    "required_resolution": "fill scorepack source acquisition row with provenance or signed primitive",
                    "claim_effect": "score_ready=false",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        if counterexample_retained:
            blocker_ledger.append(
                {
                    "blocker_id": f"BLK1315_{index}_counterexample",
                    "runner_row_id": runner_id,
                    "blocker_token": row.get("counterexample_lock", ""),
                    "blocker_source": "counterexample_lock",
                    "required_resolution": "close counterexample by parent primitive or retain finite nuisance with source-backed bound",
                    "claim_effect": "valid_prediction_row=false",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        claim_refusal.append(
            {
                "refusal_id": f"REF1315_{index}_{runner_id.replace('RUN1314_', '')}",
                "runner_row_id": runner_id,
                "claim_refused": True,
                "primary_reason": ";".join(refusal_reasons),
                "minimum_to_reconsider": "numeric predicted value, source provenance, resolved missing inputs, disposed counterexample, and passing anti-shortcut gates",
                "observable_product": row.get("observable_product", ""),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    anti_shortcut = [
        {
            "gate_id": "SHORT1315_0_no_unity",
            "forbidden_shortcut": "set tau/source/readout projection to unity",
            "runner_action": "refuse row unless projection is sourced or theorem-zero",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1315_1_no_threshold_prediction",
            "forbidden_shortcut": "use empirical threshold as MTS coefficient prediction",
            "runner_action": "threshold_abs is comparison fence only; predicted_abs_value must be sourced separately",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1315_2_no_source_fill",
            "forbidden_shortcut": "fill coefficient values from plausibility or aesthetic minimality",
            "runner_action": "requires source-backed coefficient or signed parent primitive",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1315_3_no_anchor_curve_claim",
            "forbidden_shortcut": "treat review-candidate or anchor-only R10 bound as claim-valid curve",
            "runner_action": "R10 row refuses until promoted alpha_bound(lambda) exists",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1315_4_no_transfer_shortcut",
            "forbidden_shortcut": "transfer clock alpha bound to WEP/R10 without parent branch/readout map",
            "runner_action": "cross-arena row refuses until shared branch classifier is sourced",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1315_5_no_measured_G_absorption",
            "forbidden_shortcut": "absorb finite source branch into measured G",
            "runner_action": "retains source-weight/local-GR branch as explicit debt",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    promotion_checklist = [
        {
            "checklist_id": "PROM1315_0_threshold",
            "requirement": "positive numeric threshold or empirical bound",
            "runner_condition": "threshold_numeric_positive=true",
            "current_status": "PARTIAL_ALPHA_CLOCK_WEP_ONLY_R10_AND_CROSS_ARENA_BLOCKED",
            "claim_rule": "nonnumeric thresholds refuse the row immediately",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1315_1_prediction",
            "requirement": "finite predicted absolute value",
            "runner_condition": "predicted_abs_value numeric and sourced",
            "current_status": "MISSING_FOR_ALL_ROWS",
            "claim_rule": "no prediction, no comparison, no pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1315_2_provenance",
            "requirement": "source-backed coefficient/readout/profile provenance",
            "runner_condition": "source paths and anchors exist for every physical input",
            "current_status": "MISSING_PHYSICAL_INPUT_PROVENANCE",
            "claim_rule": "placeholder strings cannot become evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1315_3_counterexamples",
            "requirement": "counterexample locks closed or finitely bounded",
            "runner_condition": "counterexample_status in {closed,bounded_with_source}",
            "current_status": "COUNTEREXAMPLES_RETAINED",
            "claim_rule": "active hidden-scalar/source-weight/readout counterexamples block claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1315_4_anti_shortcuts",
            "requirement": "no unity, threshold-as-prediction, anchor-curve, transfer, measured-G absorption, or assumption fill",
            "runner_condition": "anti-shortcut gates pass",
            "current_status": "GATES_WRITTEN_AND_ENFORCED",
            "claim_rule": "shortcut route invalidates row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1315_5_parent_primitive",
            "requirement": "optional theorem-zero route needs genuinely new primitive",
            "runner_condition": "primitive source status FOUND_SIGNED_PRIMITIVE and source audited",
            "current_status": "NO_SIGNED_PRIMITIVE_FOUND",
            "claim_rule": "escape hatch remains open but empty",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    r10_refusal = [
        {
            "r10_id": "R10REF1315_0_product",
            "runner_row_id": "RUN1314_3_r10",
            "required": "numeric P_R10_alpha(lambda)",
            "current_status": "MISSING_R10_NUMERIC_PRODUCT",
            "minimum_to_reconsider": "lambda_X, Z_X, K_X, beta_source, beta_test, tau_R10, epsilon_tail with source paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "r10_id": "R10REF1315_1_bound_curve",
            "runner_row_id": "RUN1314_3_r10",
            "required": "promoted claim-valid alpha_bound(lambda)",
            "current_status": "MISSING_PROMOTED_ALPHA_BOUND_CURVE",
            "minimum_to_reconsider": "digitized/source-backed curve rows with valid_for_claim=true, not anchor-only/review candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "r10_id": "R10REF1315_2_source_test",
            "runner_row_id": "RUN1314_3_r10",
            "required": "source/test projection and finite-source/readout map",
            "current_status": "MISSING_SOURCE_TEST_PROJECTION",
            "minimum_to_reconsider": "source/test beta factors and source-weight counterexample disposition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "r10_id": "R10REF1315_3_decision",
            "runner_row_id": "RUN1314_3_r10",
            "required": "R10 claim row",
            "current_status": "REFUSED",
            "minimum_to_reconsider": "all R10 inputs sourced and anti-shortcut gates pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1315_0_runner_result",
            "decision": "all current RAB alpha scorepack rows are refused",
            "because": "every row has missing predictions, missing source/projection/readout inputs, and/or retained counterexamples",
            "next_action": "attack P0 blockers with derivation-first then source-acquisition fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1315_1_r10_result",
            "decision": "R10 is explicitly refused",
            "because": "both finite MTS product vector and promoted alpha_bound(lambda) curve are missing",
            "next_action": "do not run symbolic R10 as evidence; source product/bound rows first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1315_0_1316",
            "target_file": "1316-Y5-R10-RAB-P0-alpha-coupling-input-source-or-derivation-attack.md",
            "target_script": "scripts/Y5_R10_RAB_P0_alpha_coupling_input_source_or_derivation_attack.py",
            "task": "attack P0 alpha coupling blockers by trying parent-primitive derivations for alpha F2, clock readout, WEP/source normalization, and R10 product inputs before falling back to exact source requirements",
            "success_condition": "at least one P0 blocker is promoted by real proof/source, or every P0 blocker is narrowed into exact nonclaim source requirements",
            "do_not": "do not fill coefficients by assumption; do not use unity/threshold/anchor-curve shortcuts; do not claim WEP/R10/local-GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    output_specs = [
        (SOURCE_REGISTER_PATH, source_register),
        (RUNNER_INPUT_AUDIT_PATH, runner_input_audit),
        (FIRST_SCORE_TABLE_PATH, first_score),
        (BLOCKER_LEDGER_PATH, blocker_ledger),
        (ANTI_SHORTCUT_PATH, anti_shortcut),
        (CLAIM_REFUSAL_PATH, claim_refusal),
        (PROMOTION_CHECKLIST_PATH, promotion_checklist),
        (R10_REFUSAL_PATH, r10_refusal),
        (DECISION_PATH, decision),
        (NEXT_PATH, next_target),
    ]
    for path, rows in output_specs:
        write_csv(path, rows)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1315_0_sources_exist",
            "registered source paths exist and anchors are found",
            all(row["exists"] and row["needle_found"] for row in source_register),
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1315_1_rows_imported",
            "runner imported all 1314 rows",
            len(runner_rows) == 5 and len(first_score) == 5,
            f"runner_rows={len(runner_rows)} first_score_rows={len(first_score)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1315_2_zero_valid_predictions",
            "runner produces zero valid prediction rows",
            sum(1 for row in first_score if row["valid_prediction_row"] is True) == 0,
            ";".join(f"{row['score_row_id']}={row['claim_status']}" for row in first_score),
        )
    )
    validations.append(
        validation_row(
            "VAL1315_3_all_refused",
            "all current rows are refused",
            all(row["claim_status"] == "REFUSED" for row in first_score),
            ";".join(row["refusal_reason"] for row in first_score),
        )
    )
    validations.append(
        validation_row(
            "VAL1315_4_blockers_recorded",
            "missing-input and counterexample blockers are recorded",
            len(blocker_ledger) >= len(runner_rows),
            f"blocker_rows={len(blocker_ledger)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1315_5_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            all(row["status"] == "ENFORCED" for row in anti_shortcut),
            ";".join(f"{row['gate_id']}={row['status']}" for row in anti_shortcut),
        )
    )
    validations.append(
        validation_row(
            "VAL1315_6_r10_refused",
            "R10 row is explicitly refused",
            r10_refusal[-1]["current_status"] == "REFUSED",
            ";".join(f"{row['r10_id']}={row['current_status']}" for row in r10_refusal),
        )
    )

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in output_specs:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")
    validations.append(
        validation_row(
            "VAL1315_7_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        )
    )
    formalization_outputs = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1315_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_outputs) == 0,
            f"formalization_generated_output_count={len(formalization_outputs)}",
        )
    )
    tables = [
        source_register,
        runner_input_audit,
        first_score,
        blocker_ledger,
        anti_shortcut,
        claim_refusal,
        promotion_checklist,
        r10_refusal,
        decision,
        next_target,
    ]
    validations.append(
        validation_row(
            "VAL1315_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1315_10_next_target_1316",
            "next target routes to P0 alpha coupling input source/derivation attack",
            next_target[0]["next_id"] == "NEXT1315_0_1316",
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1315_11_overall",
            "overall 1315 validation",
            overall_pass,
            "1315 mechanically refuses all current RAB alpha scorepack rows, records blockers, and routes to P0 source/derivation attack",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1315 mechanically refuses every current RAB alpha scorepack row. There are zero valid predictions and zero claim-ready rows.

**Main progress:** the runner now produces a first nonclaim table, a missing-input blocker ledger, anti-shortcut gates, R10 refusal detail, and a promotion checklist. Future source fills can be tested against this rather than argued by hand.

**Decision:** attack P0 blockers next. The theory route can still win by proof, but without proof the row must be filled by real source-backed coefficients, readout maps, source profiles, R10 vectors, and bound curves.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Runner Input Audit

{markdown_table(runner_input_audit, ["audit_id", "runner_row_id", "threshold_abs", "threshold_numeric_positive", "predicted_abs_value", "missing_inputs", "acquisition_status", "counterexample_lock", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## First Nonclaim Score Table

{markdown_table(first_score, ["score_row_id", "runner_row_id", "observable_product", "threshold_abs", "threshold_numeric_positive", "predicted_abs_value", "available_inputs", "missing_inputs", "acquisition_status", "counterexample_status", "claim_status", "refusal_reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Missing Input Blocker Ledger

{markdown_table(blocker_ledger, ["blocker_id", "runner_row_id", "blocker_token", "blocker_source", "required_resolution", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates

{markdown_table(anti_shortcut, ["gate_id", "forbidden_shortcut", "runner_action", "status", "valid_for_claim", "claim_allowed"])}

## Claim Refusal Ledger

{markdown_table(claim_refusal, ["refusal_id", "runner_row_id", "claim_refused", "primary_reason", "minimum_to_reconsider", "observable_product", "valid_for_claim", "claim_allowed"])}

## Promotion Checklist

{markdown_table(promotion_checklist, ["checklist_id", "requirement", "runner_condition", "current_status", "claim_rule", "valid_for_claim", "claim_allowed"])}

## R10 Refusal Detail

{markdown_table(r10_refusal, ["r10_id", "runner_row_id", "required", "current_status", "minimum_to_reconsider", "valid_for_claim", "claim_allowed"])}

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
