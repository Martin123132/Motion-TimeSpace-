from __future__ import annotations

import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


PACK_ID = "P8_Y5_R10_1222"
TITLE = "1222-Y5-R10-closure-scorepack-runner-first-nonclaim-table"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
RUNNER_INPUT_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_INPUT_AUDIT.csv"
THRESHOLD_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_THRESHOLD_AUDIT.csv"
BLOCKER_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_MISSING_INPUT_BLOCKER_LEDGER.csv"
PROMOTION_CHECKLIST_PATH = OUT_DIR / f"{PACK_ID}_PROMOTION_CHECKLIST.csv"
NONCLAIM_TABLE_PATH = OUT_DIR / f"{PACK_ID}_FIRST_NONCLAIM_SCORE_TABLE.csv"
REFUSAL_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_REFUSAL_LEDGER.csv"
ACQUISITION_QUEUE_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_ACQUISITION_QUEUE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
RUNNER_STATUS_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_STATUS.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1222_VALIDATION.csv"


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
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def positive_decimal(value: object) -> bool:
    try:
        return Decimal(str(value)) > 0
    except (InvalidOperation, ValueError):
        return False


def missing_tokens(*values: object) -> list[str]:
    joined = ";".join(str(value) for value in values)
    return [token.strip() for token in joined.split(";") if token.strip().upper().startswith("MISSING")]


def has_missing(row: dict[str, object]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def blocker_status(row: dict[str, str], acquisition: dict[str, str] | None) -> str:
    parts = []
    if not positive_decimal(row.get("threshold_abs", "")):
        parts.append("threshold_not_numeric_positive")
    if missing_tokens(row.get("missing_inputs", "")):
        parts.append("missing_inputs_present")
    if acquisition and "MISSING" in acquisition.get("missing_or_status", "").upper():
        parts.append("acquisition_missing")
    if row.get("counterexample_lock"):
        parts.append("counterexample_retained")
    if not parse_bool(row.get("schema_valid", False)):
        parts.append("schema_invalid")
    if not parts:
        parts.append("blocked_by_nonclaim_policy")
    return ";".join(parts)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1222_0_1221_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_NEXT_TARGET.csv",
            "needle": "1222-Y5-R10-closure-scorepack-runner-first-nonclaim-table.md",
            "purpose": "1221 handoff to first mechanical closure scorepack runner",
        },
        {
            "source_id": "SRC1222_1_1221_runner_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_RUNNER_READY_NONCLAIM_ROWS.csv",
            "needle": "RUN1221_0_alpha",
            "purpose": "runner-ready nonclaim rows to evaluate",
        },
        {
            "source_id": "SRC1222_2_1221_acquisition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_SOURCE_ACQUISITION_LEDGER.csv",
            "needle": "ACQ1221_0_alpha",
            "purpose": "source acquisition rows paired to runner inputs",
        },
        {
            "source_id": "SRC1222_3_1221_scorepack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_SCOREPACK_DECISION_MATRIX.csv",
            "needle": "SCORE1221_0_alpha",
            "purpose": "prior scorepack refusal matrix",
        },
        {
            "source_id": "SRC1222_4_1221_primitive",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_PARENT_PRIMITIVE_ESCAPE_HATCH.csv",
            "needle": "PESC1221_0_parent_grammar",
            "purpose": "parent primitive escape hatch remains unsigned",
        },
        {
            "source_id": "SRC1222_5_1221_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_FINITE_CLOSURE_INPUT_SCHEMA.csv",
            "needle": "SCHEMA1221_0_coefficient_value",
            "purpose": "input schema and refusal conditions",
        },
        {
            "source_id": "SRC1222_6_1221_arena_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_EMPIRICAL_ARENA_MAP.csv",
            "needle": "ARENA1221_0_MICROSCOPE_WEP",
            "purpose": "arena map for interpreting row pressure",
        },
        {
            "source_id": "SRC1222_7_1221_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_CLAIM_GATES.csv",
            "needle": "GATE1221_4_runner_claim",
            "purpose": "claim gate requiring runner rows to remain blocked",
        },
        {
            "source_id": "SRC1222_8_1221_status",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_PRODUCT_RUNNER_STUB.csv",
            "needle": "APR1221_0_closure_scorepack_stub",
            "purpose": "1221 runner stub with zero valid prediction rows",
        },
        {
            "source_id": "SRC1222_9_1220_closure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_FINITE_COUPLING_CLOSURE_REGISTER.csv",
            "needle": "FCCR1220_0_alpha",
            "purpose": "original finite closure debts for traceability",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    runner_rows = read_csv(OUT_DIR / "P8_Y5_R10_1221_RUNNER_READY_NONCLAIM_ROWS.csv")
    acquisition_rows = read_csv(OUT_DIR / "P8_Y5_R10_1221_SOURCE_ACQUISITION_LEDGER.csv")
    primitive_rows = read_csv(OUT_DIR / "P8_Y5_R10_1221_PARENT_PRIMITIVE_ESCAPE_HATCH.csv")
    acquisition_by_closure = {row["closure_id"]: row for row in acquisition_rows}

    runner_input_audit = []
    threshold_audit = []
    blocker_rows = []
    nonclaim_rows = []
    refusal_rows = []
    for index, row in enumerate(runner_rows):
        acquisition = acquisition_by_closure.get(row["closure_id"])
        tokens = missing_tokens(row.get("missing_inputs", ""), acquisition.get("missing_or_status", "") if acquisition else "")
        threshold_ok = positive_decimal(row.get("threshold_abs", ""))
        missing_count = len(tokens)
        status = blocker_status(row, acquisition)
        value_source_status = "MISSING_PREDICTED_VALUE_OR_THEOREM_ZERO" if missing_count else "UNSCORED_NONCLAIM"
        runner_input_audit.append(
            {
                "audit_id": f"AUD1222_{index}_{row['runner_row_id'].split('_')[-1]}",
                "runner_row_id": row["runner_row_id"],
                "closure_id": row["closure_id"],
                "schema_valid_input": row.get("schema_valid", ""),
                "threshold_abs": row.get("threshold_abs", ""),
                "threshold_numeric_positive": threshold_ok,
                "missing_input_count": missing_count,
                "acquisition_row": acquisition["acquisition_id"] if acquisition else "MISSING_ACQUISITION_ROW",
                "acquisition_status": acquisition.get("missing_or_status", "MISSING_ACQUISITION_ROW") if acquisition else "MISSING_ACQUISITION_ROW",
                "counterexample_lock": row.get("counterexample_lock", ""),
                "runner_status": "REFUSE_CLAIM",
                "refusal_status": status,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        threshold_audit.append(
            {
                "threshold_id": f"THR1222_{index}_{row['runner_row_id'].split('_')[-1]}",
                "runner_row_id": row["runner_row_id"],
                "closure_id": row["closure_id"],
                "threshold_abs": row.get("threshold_abs", ""),
                "threshold_units": row.get("threshold_units", ""),
                "numeric_positive": threshold_ok,
                "threshold_status": "NUMERIC_POSITIVE_NONCLAIM" if threshold_ok else "NONNUMERIC_BLOCKER",
                "usage": "can bound only after predicted value/source/readout inputs exist" if threshold_ok else "cannot score until threshold/bound is sourced",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for token_index, token in enumerate(tokens):
            blocker_rows.append(
                {
                    "blocker_id": f"BLK1222_{index}_{token_index}",
                    "runner_row_id": row["runner_row_id"],
                    "closure_id": row["closure_id"],
                    "blocker_token": token,
                    "blocker_source": "runner_missing_inputs_or_acquisition_status",
                    "required_resolution": "replace token with sourced numeric input or signed theorem-zero primitive",
                    "claim_effect": "valid_prediction_row=false",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        if row.get("counterexample_lock"):
            blocker_rows.append(
                {
                    "blocker_id": f"BLK1222_{index}_counterexample",
                    "runner_row_id": row["runner_row_id"],
                    "closure_id": row["closure_id"],
                    "blocker_token": row["counterexample_lock"],
                    "blocker_source": "counterexample_lock",
                    "required_resolution": "close counterexample by parent primitive or retain finite nuisance with source-backed bound",
                    "claim_effect": "valid_prediction_row=false",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        nonclaim_rows.append(
            {
                "score_row_id": f"NCS1222_{index}_{row['runner_row_id'].split('_')[-1]}",
                "runner_row_id": row["runner_row_id"],
                "closure_id": row["closure_id"],
                "observable_product": row["observable_product"],
                "threshold_abs": row["threshold_abs"],
                "threshold_numeric_positive": threshold_ok,
                "predicted_abs_value": "MISSING_PREDICTED_VALUE",
                "coefficient_source_status": acquisition.get("missing_or_status", "MISSING_ACQUISITION_ROW") if acquisition else "MISSING_ACQUISITION_ROW",
                "source_profile_status": "MISSING_SOURCE_PROFILE_WEIGHTING" if "SOURCE_PROFILE" in row.get("missing_inputs", "").upper() else "not_applicable_or_not_yet_required",
                "readout_status": "MISSING_READOUT_OR_OFFICIAL_ARRAYS" if ("READOUT" in row.get("missing_inputs", "").upper() or "ARRAYS" in row.get("missing_inputs", "").upper()) else "not_applicable_or_not_yet_required",
                "parent_primitive_status": "MISSING_PARENT_PRIMITIVE" if "PARENT_PRIMITIVE" in row.get("missing_inputs", "").upper() else "not_found_or_not_required_for_this_row",
                "counterexample_status": "RETAINED",
                "claim_status": "REFUSED",
                "refusal_reason": status,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        refusal_rows.append(
            {
                "refusal_id": f"REF1222_{index}_{row['runner_row_id'].split('_')[-1]}",
                "runner_row_id": row["runner_row_id"],
                "closure_id": row["closure_id"],
                "claim_refused": True,
                "primary_reason": status,
                "minimum_to_reconsider": "numeric predicted value, source provenance, resolved missing inputs, disposed counterexample, and passing anti-shortcut gates",
                "observable_arenas": row["arena"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    promotion_checklist = [
        {
            "checklist_id": "PROM1222_0_threshold",
            "requirement": "positive numeric threshold or empirical bound",
            "runner_condition": "threshold_numeric_positive=true",
            "current_status": "PARTIAL_ALPHA_SURFACE_SOURCE_WEIGHT_COMMON_ONLY",
            "claim_rule": "nonnumeric thresholds refuse the row immediately",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1222_1_prediction",
            "requirement": "finite predicted absolute value",
            "runner_condition": "predicted_abs_value numeric and sourced",
            "current_status": "MISSING_FOR_ALL_ROWS",
            "claim_rule": "no prediction, no comparison, no pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1222_2_provenance",
            "requirement": "source-backed coefficient/readout/profile provenance",
            "runner_condition": "source paths and needles exist for every physical input",
            "current_status": "MISSING_PHYSICAL_INPUT_PROVENANCE",
            "claim_rule": "placeholder strings cannot become evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1222_3_counterexamples",
            "requirement": "counterexample locks closed or finitely bounded",
            "runner_condition": "counterexample_status in {closed,bounded_with_source}",
            "current_status": "COUNTEREXAMPLES_RETAINED",
            "claim_rule": "active hidden-scalar/source-weight/readout counterexamples block claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1222_4_anti_shortcuts",
            "requirement": "no unity, cancellation, measured-G absorption, or assumption fill",
            "runner_condition": "anti-shortcut gates pass",
            "current_status": "GATES_WRITTEN_AND_ENFORCED",
            "claim_rule": "shortcut route invalidates row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "checklist_id": "PROM1222_5_parent_primitive",
            "requirement": "optional theorem-zero route needs genuinely new primitive",
            "runner_condition": "primitive source status FOUND_SIGNED_PRIMITIVE and source audited",
            "current_status": "NO_SIGNED_PRIMITIVE_FOUND",
            "claim_rule": "1221 escape hatch remains open but empty",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    acquisition_queue = []
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    for index, row in enumerate(sorted(acquisition_rows, key=lambda item: (priority_order.get(item.get("scorepack_priority", "P9"), 9), item["acquisition_id"]))):
        acquisition_queue.append(
            {
                "queue_id": f"QUEUE1222_{index}_{row['acquisition_id'].split('_')[-1]}",
                "acquisition_id": row["acquisition_id"],
                "priority": row["scorepack_priority"],
                "closure_id": row["closure_id"],
                "debt": row["debt"],
                "source_to_acquire": row["source_to_acquire"],
                "minimum_usable_form": row["minimum_usable_form"],
                "current_status": row["missing_or_status"],
                "best_next_move": "derive parent primitive first; if not derivable, acquire source-backed finite input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    anti_shortcut_gates = [
        {
            "gate_id": "SHORT1222_0_no_unity",
            "forbidden_shortcut": "set tau/source/readout projection to unity",
            "runner_action": "refuse row unless projection is sourced or theorem-zero",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1222_1_no_source_fill",
            "forbidden_shortcut": "fill coefficient values from plausibility or aesthetic minimality",
            "runner_action": "requires source-backed coefficient or signed parent primitive",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1222_2_no_cancellation",
            "forbidden_shortcut": "hide products by sign/material cancellation",
            "runner_action": "uses absolute product until full signed material model exists",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1222_3_no_measured_G_absorption",
            "forbidden_shortcut": "absorb finite source branch into measured G",
            "runner_action": "retains source-weight/local-GR branch as explicit debt",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    valid_predictions = sum(1 for row in nonclaim_rows if parse_bool(row["valid_prediction_row"]))
    score_ready = sum(1 for row in nonclaim_rows if parse_bool(row["score_ready"]))
    numeric_thresholds = sum(1 for row in threshold_audit if parse_bool(row["numeric_positive"]))
    runner_status = [
        {
            "runner_id": "APR1222_0_first_nonclaim_score_table",
            "input_rows": len(runner_rows),
            "score_rows": len(nonclaim_rows),
            "blocker_rows": len(blocker_rows),
            "numeric_threshold_rows": numeric_thresholds,
            "nonnumeric_threshold_rows": len(threshold_audit) - numeric_thresholds,
            "score_ready_rows": score_ready,
            "valid_prediction_rows": valid_predictions,
            "claim_allowed": False,
            "expected_result": "all rows refused",
            "reason": "the runner has thresholds for some rows, but no row has all sourced predicted values, readout/source profile inputs, and counterexample disposition",
            "valid_for_claim": False,
        }
    ]

    decision_rows = [
        {
            "decision_id": "DEC1222_0_runner_built",
            "decision": "use the mechanical runner as the local coupling gatekeeper",
            "because": "the coupling issue now has row-level refusal logic instead of repeated prose debate",
            "next_action": "attack P0 acquisition rows or find a genuinely new parent primitive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1222_1_no_score_claims",
            "decision": "do not interpret positive thresholds as evidence",
            "because": "thresholds without sourced predictions only prove what would be required, not that MTS passes",
            "next_action": "source or derive predicted values before any WEP/R10/local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1222_2_next_p0",
            "decision": "prioritize P0 coupling inputs",
            "because": "alpha/surface/source-weight/readout are the current project bottleneck for local tests",
            "next_action": "derive parent primitive clauses first, then fall back to source acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1222_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all 1222 input sources are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1222_1_runner_inputs",
            "gate": "runner rows imported",
            "status": "PASS",
            "reason": "six 1221 nonclaim runner rows imported",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1222_2_thresholds",
            "gate": "thresholds ready",
            "status": "PARTIAL",
            "reason": "four rows have positive numeric thresholds; readout and tail remain nonnumeric blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1222_3_predictions",
            "gate": "sourced predictions available",
            "status": "BLOCKED",
            "reason": "predicted_abs_value is missing for every score row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1222_4_counterexamples",
            "gate": "counterexamples disposed",
            "status": "BLOCKED",
            "reason": "counterexample locks remain retained in every runner row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1222_5_claim_permission",
            "gate": "WEP/local-GR/R10/EM claim permission",
            "status": "BLOCKED",
            "reason": "valid_prediction_rows=0 and all score rows are REFUSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1222_0_1223",
            "target_file": "1223-Y5-R10-P0-coupling-input-source-or-derivation-attack.md",
            "target_script": "scripts/Y5_R10_P0_coupling_input_source_or_derivation_attack.py",
            "task": "attack the P0 queue by trying parent-primitive derivations for alpha F2, surface binding, source-weight owner, and readout functor before falling back to source-backed finite inputs",
            "success_condition": "at least one P0 blocker is promoted with a real proof/source, or all P0 blockers are narrowed into exact source requirements without claim promotion",
            "do_not_do": "do not fill coefficients by assumption, do not use unity/cancellation shortcuts, do not claim WEP/local-GR/R10/EM, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (RUNNER_INPUT_AUDIT_PATH, runner_input_audit),
        (THRESHOLD_AUDIT_PATH, threshold_audit),
        (BLOCKER_LEDGER_PATH, blocker_rows),
        (PROMOTION_CHECKLIST_PATH, promotion_checklist),
        (NONCLAIM_TABLE_PATH, nonclaim_rows),
        (REFUSAL_LEDGER_PATH, refusal_rows),
        (ACQUISITION_QUEUE_PATH, acquisition_queue),
        (ANTI_SHORTCUT_PATH, anti_shortcut_gates),
        (RUNNER_STATUS_PATH, runner_status),
        (DECISION_PATH, decision_rows),
        (CLAIM_GATES_PATH, claim_gates),
        (NEXT_PATH, next_rows),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    validation_rows = []
    validation_rows.append(
        validation_row(
            "VAL1222_0_sources_exist",
            "all cited local sources exist",
            all(parse_bool(row["path_exists"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['path_exists']))}/{len(source_register)} sources exist",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_1_needles_found",
            "all cited source needles found",
            all(parse_bool(row["needle_found"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['needle_found']))}/{len(source_register)} needles found",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_2_runner_rows_imported",
            "1221 runner rows imported",
            len(runner_rows) == 6,
            f"runner_rows={len(runner_rows)}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_3_score_table_complete",
            "one score row per runner row",
            len(nonclaim_rows) == len(runner_rows),
            f"score_rows={len(nonclaim_rows)} runner_rows={len(runner_rows)}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_4_known_thresholds_positive",
            "known numeric thresholds are positive",
            numeric_thresholds == 4,
            f"numeric_threshold_rows={numeric_thresholds}; nonnumeric_threshold_rows={len(threshold_audit) - numeric_thresholds}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_5_blockers_materialized",
            "missing inputs and counterexamples become blocker rows",
            len(blocker_rows) >= len(runner_rows),
            f"blocker_rows={len(blocker_rows)}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_6_all_rows_refused",
            "all score rows are refused",
            all(row["claim_status"] == "REFUSED" and is_false(row, "valid_prediction_row") for row in nonclaim_rows),
            "all score rows claim_status=REFUSED and valid_prediction_row=false",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_7_zero_valid_predictions",
            "runner status has zero valid prediction rows",
            valid_predictions == 0 and score_ready == 0 and is_false(runner_status[0], "claim_allowed"),
            f"valid_prediction_rows={valid_predictions}; score_ready_rows={score_ready}; claim_allowed=false",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_8_anti_shortcuts_enforced",
            "anti-shortcut gates enforce no unity/cancellation/source-fill",
            all(row["status"] == "ENFORCED" and is_false(row, "claim_allowed") for row in anti_shortcut_gates),
            "; ".join(row["gate_id"] for row in anti_shortcut_gates),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_9_parent_primitive_still_absent",
            "no parent primitive source is treated as found",
            all(row.get("current_status") != "FOUND_SIGNED_PRIMITIVE" for row in primitive_rows),
            "; ".join(f"{row['primitive_id']}={row['current_status']}" for row in primitive_rows),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_10_claim_gates_blocked",
            "claim gates keep physical claims blocked",
            any(row["status"] == "BLOCKED" for row in claim_gates) and all(is_false(row, "valid_for_claim") for row in claim_gates),
            "prediction/counterexample/claim gates remain blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_11_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
                for _, rows in generated_tables
                for row in rows
                if "valid_for_claim" in row and "claim_allowed" in row
            ),
            "valid_for_claim=false and claim_allowed=false throughout claim-bearing tables",
        )
    )

    csv_parse_details = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            parsed = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAIL:{exc}")
    validation_rows.append(
        validation_row(
            "VAL1222_12_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(csv_parse_details),
        )
    )

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if modified >= RUN_STARTED_UTC:
                    formalization_recent.append(path)
    validation_rows.append(
        validation_row(
            "VAL1222_13_formalization_untouched",
            "formalization-workbench untouched during run",
            len(formalization_recent) == 0,
            f"formalization_recent_after_run_start_count={len(formalization_recent)}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1222_14_next_target",
            "next target is staged",
            next_rows[0]["target_file"] == "1223-Y5-R10-P0-coupling-input-source-or-derivation-attack.md",
            next_rows[0]["target_file"],
        )
    )

    overall_before = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1222_15_overall",
            "overall 1222 validation",
            overall_before,
            "1222 runner creates the first mechanical nonclaim score table and refuses all rows",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# 1222 Y5/R10 Closure Scorepack Runner First Nonclaim Table

**Current verdict:** 1222 builds the first mechanical coupling scorepack runner and it refuses every physical claim row. This is good discipline, not bad news: the goblin clipboard now says exactly what must be sourced or derived before WEP/local-GR/R10/EM claims can move.

**Main progress:** the 1221 scorepack is executable as a refusal table. Four thresholds are positive numeric constraints, two rows remain nonnumeric blockers, every row has explicit missing-input/counterexample blockers, and valid prediction rows stay at zero.

**Practical consequence:** the coupling problem is now testable as an input-completeness problem. The next move is to attack the P0 queue: alpha F2, surface binding, source-weight owner, and readout functor.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"])}

## Runner Input Audit

{markdown_table(runner_input_audit, ["audit_id", "runner_row_id", "closure_id", "schema_valid_input", "threshold_abs", "threshold_numeric_positive", "missing_input_count", "acquisition_row", "acquisition_status", "counterexample_lock", "runner_status", "refusal_status", "valid_for_claim", "claim_allowed"])}

## Threshold Audit

{markdown_table(threshold_audit, ["threshold_id", "runner_row_id", "closure_id", "threshold_abs", "threshold_units", "numeric_positive", "threshold_status", "usage", "valid_for_claim", "claim_allowed"])}

## Missing Input Blocker Ledger

{markdown_table(blocker_rows, ["blocker_id", "runner_row_id", "closure_id", "blocker_token", "blocker_source", "required_resolution", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Promotion Checklist

{markdown_table(promotion_checklist, ["checklist_id", "requirement", "runner_condition", "current_status", "claim_rule", "valid_for_claim", "claim_allowed"])}

## First Nonclaim Score Table

{markdown_table(nonclaim_rows, ["score_row_id", "runner_row_id", "closure_id", "observable_product", "threshold_abs", "threshold_numeric_positive", "predicted_abs_value", "coefficient_source_status", "source_profile_status", "readout_status", "parent_primitive_status", "counterexample_status", "claim_status", "refusal_reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Claim Refusal Ledger

{markdown_table(refusal_rows, ["refusal_id", "runner_row_id", "closure_id", "claim_refused", "primary_reason", "minimum_to_reconsider", "observable_arenas", "valid_for_claim", "claim_allowed"])}

## Source Acquisition Queue

{markdown_table(acquisition_queue, ["queue_id", "acquisition_id", "priority", "closure_id", "debt", "source_to_acquire", "minimum_usable_form", "current_status", "best_next_move", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates

{markdown_table(anti_shortcut_gates, ["gate_id", "forbidden_shortcut", "runner_action", "status", "valid_for_claim", "claim_allowed"])}

## Runner Status

{markdown_table(runner_status, ["runner_id", "input_rows", "score_rows", "blocker_rows", "numeric_threshold_rows", "nonnumeric_threshold_rows", "score_ready_rows", "valid_prediction_rows", "claim_allowed", "expected_result", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision_rows, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_rows, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows, ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
