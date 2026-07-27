from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1293"
TITLE = "1293-Y5-R10-RAB-chain-kernel-residual-runner-schema-and-rejection-smoke"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
RUNNER_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_CHAIN_KERNEL_RESIDUAL_RUNNER_SCHEMA.csv"
REJECTION_RESULTS_PATH = OUT_DIR / f"{PACK_ID}_REJECTION_SMOKE_RESULTS.csv"
RESPONSE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_RESPONSE_OPERATOR_REQUIREMENTS.csv"
NO_SCORE_GUARD_PATH = OUT_DIR / f"{PACK_ID}_NO_SCORE_GUARD.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1293_VALIDATION.csv"
INPUT_PATH = OUT_DIR / "P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv"


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


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        RUNNER_SCHEMA_PATH,
        REJECTION_RESULTS_PATH,
        RESPONSE_REQUIREMENTS_PATH,
        NO_SCORE_GUARD_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def missing_tokens(value: str) -> list[str]:
    return [token for token in split_semicolon(value) if token.startswith("MISSING")]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    input_rows = read_csv(INPUT_PATH)

    source_register = [
        {
            "source_id": "SRC1293_0_1292_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1292_NEXT_TARGET.csv",
            "needle": "NEXT1292_0_1293",
            "role": "handoff into chain-kernel residual runner schema and rejection smoke",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1293_1_1292_runner_input",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "needle": "RRI1292_3_chain_vector",
            "role": "input rows consumed by rejection smoke runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1293_2_1292_adoption",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1292_STRICT_DOUBLE_ZERO_ADOPTION_VERDICT.csv",
            "needle": "SDA1292_4_overall",
            "role": "strict double-zero adoption failed into residual runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1293_3_1292_claim_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CLAIM_GATES.csv",
            "needle": "CG1292_3_residual_runner",
            "role": "runner is blocked by input templates only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1293_4_1291_bounds",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "needle": "KRB1291_3_residual_verdict",
            "role": "bound formulas behind RRI1292 rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1293_5_response_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "needle": "RMR1288_7_response_verdict",
            "role": "local response matrix remains missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1293_6_ppn_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv",
            "needle": "PBR794_0_PPN_metric",
            "role": "PPN/Newton/orbital/clock/R10 requirements remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    runner_schema = [
        {
            "schema_id": "CKR1293_0_required_columns",
            "requirement": "each runner row must declare runner_id, residual_component, prediction_form, zero_condition, required_inputs, maps_to_tests, source_path, source_anchor, current_status, valid_for_claim, claim_allowed",
            "pass_condition": "all required columns are present and non-empty",
            "on_fail": "reject row with STRUCTURE_FAIL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "CKR1293_1_missing_input_policy",
            "requirement": "required_inputs must contain no MISSING_* tokens before any score is emitted",
            "pass_condition": "missing_token_count=0",
            "on_fail": "reject row with MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "CKR1293_2_claim_flag_policy",
            "requirement": "valid_for_claim and claim_allowed must both be true before score export is possible",
            "pass_condition": "valid_for_claim=true and claim_allowed=true after source validation",
            "on_fail": "reject row with NONCLAIM_FLAGS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "CKR1293_3_source_anchor_policy",
            "requirement": "source_path must exist and source_anchor must be found in the source text",
            "pass_condition": "source_exists=true and anchor_found=true",
            "on_fail": "reject row with SOURCE_ANCHOR_FAIL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "CKR1293_4_response_policy",
            "requirement": "local response operator/observable limit must be sourced for every mapped arena",
            "pass_condition": "response operator fields are present and sourced",
            "on_fail": "reject row with RESPONSE_OPERATOR_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "CKR1293_5_score_policy",
            "requirement": "score fields remain blank unless all prior gates pass",
            "pass_condition": "score_emitted=false for current smoke; future score only after all gates pass",
            "on_fail": "abort runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    required_columns = [
        "runner_id",
        "branch",
        "residual_component",
        "prediction_form",
        "zero_condition",
        "required_inputs",
        "source_path",
        "source_anchor",
        "maps_to_tests",
        "current_status",
        "valid_for_claim",
        "claim_allowed",
    ]

    rejection_results = []
    for row in input_rows:
        row_missing_tokens = missing_tokens(row.get("required_inputs", ""))
        structural_missing = [column for column in required_columns if not row.get(column)]
        source_exists, anchor_found = exists_and_contains(row.get("source_path", ""), row.get("source_anchor", ""))
        reject_codes: list[str] = []
        if structural_missing:
            reject_codes.append("STRUCTURE_FAIL")
        if row_missing_tokens:
            reject_codes.append("MISSING_INPUTS")
        if is_false(row.get("valid_for_claim", False)) or is_false(row.get("claim_allowed", False)):
            reject_codes.append("NONCLAIM_FLAGS")
        if not source_exists or not anchor_found:
            reject_codes.append("SOURCE_ANCHOR_FAIL")
        if "MISSING_RESPONSE_OPERATOR" in row_missing_tokens or "MISSING_OBSERVABLE_RESPONSE_MATRIX" in row_missing_tokens or "MISSING_LOCAL_RESPONSE_LIMITS" in row_missing_tokens:
            reject_codes.append("RESPONSE_OPERATOR_MISSING")
        runner_status = "REJECTED_NONCLAIM_NO_SCORE" if reject_codes else "ELIGIBLE_FOR_FUTURE_SCORE"
        rejection_results.append(
            {
                "runner_id": row.get("runner_id", ""),
                "residual_component": row.get("residual_component", ""),
                "mapped_tests": row.get("maps_to_tests", ""),
                "source_exists": source_exists,
                "anchor_found": anchor_found,
                "missing_token_count": len(row_missing_tokens),
                "missing_tokens": ";".join(row_missing_tokens),
                "structural_missing": ";".join(structural_missing) if structural_missing else "NONE",
                "reject_codes": ";".join(reject_codes) if reject_codes else "NONE",
                "score_emitted": False,
                "score_value": "",
                "runner_status": runner_status,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    response_requirements = [
        {
            "requirement_id": "ROR1293_0_Newton_source",
            "arena": "Newton/source normalization",
            "required_operator": "R_Newton_chain or K00/source-normalization map from R_chain^{00} to epsilon_Newton",
            "current_evidence": "1288 and 794 keep source model/K00 response missing",
            "status": "MISSING_RESPONSE_OPERATOR",
            "blocks_runner_rows": "RRI1292_0_m_chain;RRI1292_1_Lcg_chain;RRI1292_3_chain_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "ROR1293_1_PPN",
            "arena": "PPN gamma/beta/preferred-frame",
            "required_operator": "R_PPN_chain mapping R_chain^{00}, anisotropic tails, and boundary/domain pieces to PPN vector",
            "current_evidence": "RMR1288_1 and PBR794_0 keep response matrix missing",
            "status": "MISSING_RESPONSE_OPERATOR",
            "blocks_runner_rows": "RRI1292_0_m_chain;RRI1292_1_Lcg_chain;RRI1292_2_cdb_chain;RRI1292_3_chain_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "ROR1293_2_clock_orbital",
            "arena": "clock/orbital",
            "required_operator": "R_clock_chain and R_orbital_chain with domain/source normalization",
            "current_evidence": "RMR1288_3, RMR1288_4, PBR794_2, and PBR794_3 are missing",
            "status": "MISSING_RESPONSE_OPERATOR",
            "blocks_runner_rows": "RRI1292_0_m_chain;RRI1292_1_Lcg_chain;RRI1292_2_cdb_chain;RRI1292_3_chain_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "ROR1293_3_R10",
            "arena": "R10 short-range/fifth-force",
            "required_operator": "R_R10_chain(lambda) plus range profile and real alpha_bound(lambda)",
            "current_evidence": "RMR1288_5 and PBR794_3 keep R10 projection missing",
            "status": "MISSING_RESPONSE_OPERATOR",
            "blocks_runner_rows": "RRI1292_0_m_chain_if_finite_range;RRI1292_3_chain_vector_if_finite_range",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "ROR1293_4_all_local",
            "arena": "all_local",
            "required_operator": "full local response matrix and observable limits",
            "current_evidence": "RMR1288_7 says no arena is scoreable until response operators and observable limits are sourced",
            "status": "MISSING_FULL_RESPONSE_MATRIX",
            "blocks_runner_rows": "all RRI1292 rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    no_score_guard = [
        {
            "guard_id": "NSG1293_0_rows_rejected",
            "policy": "all current input rows must be rejected because they contain MISSING inputs and nonclaim flags",
            "observed": f"rejected_rows={sum(1 for row in rejection_results if row['runner_status'] == 'REJECTED_NONCLAIM_NO_SCORE')};total_rows={len(rejection_results)}",
            "status": "PASS" if all(row["runner_status"] == "REJECTED_NONCLAIM_NO_SCORE" for row in rejection_results) else "FAIL",
            "score_emitted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "NSG1293_1_no_numeric_invention",
            "policy": "runner must not invent numeric m, L_cg, kernel, or response values",
            "observed": "score_value blank for every rejection row",
            "status": "PASS" if all(not row["score_value"] for row in rejection_results) else "FAIL",
            "score_emitted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "NSG1293_2_no_local_GR_score",
            "policy": "no local-GR/Newton/PPN/R10 score can be emitted from current rows",
            "observed": "strict adoption failed and response matrix remains missing",
            "status": "PASS",
            "score_emitted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1293_0_sources",
            "claim": "private runner provenance",
            "current_status": "SATISFIED_FOR_PRIVATE_CHECKPOINT",
            "reason": "registered runner source paths and anchors are validated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1293_1_structural_runner",
            "claim": "runner schema can parse current input",
            "current_status": "PASS_STRUCTURE_ONLY",
            "reason": "input rows have required schema columns, but remain rejected by missing inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1293_2_current_scoring",
            "claim": "current rows can be scored",
            "current_status": "BLOCKED_REJECTED_NONCLAIM",
            "reason": "all rows contain MISSING inputs and nonclaim flags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1293_3_response_matrix",
            "claim": "local response matrix exists",
            "current_status": "BLOCKED_MISSING_RESPONSE_OPERATOR",
            "reason": "response operator requirements remain missing across Newton/PPN/clock/orbital/R10",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1293_4_local_GR",
            "claim": "local GR/Newton/PPN recovery",
            "current_status": "BLOCKED_NO_SCORE_EMITTED",
            "reason": "runner emits no score and rejects every current row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1293_0_runner_built",
            "decision": "build the chain-kernel residual runner as a rejection smoke test",
            "because": "1292 produced runner templates with missing inputs after strict double-zero source-match failed",
            "next_action": "fill theorem/numeric input packs or response operator rows before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1293_1_no_score",
            "decision": "emit no residual/local-GR score from current rows",
            "because": "every row has MISSING inputs, nonclaim flags, and response operator gaps",
            "next_action": "1294 should prioritize response operator/input pack acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1293_2_progress",
            "decision": "residual branch is now machine-gated",
            "because": "future rows must satisfy explicit schema/source/response gates rather than prose confidence",
            "next_action": "source first input pack or keep local branch blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1293_0_1294",
            "target_file": "1294-Y5-R10-RAB-chain-kernel-response-operator-or-input-pack-acquisition.md",
            "target_script": "scripts/Y5_R10_RAB_chain_kernel_response_operator_or_input_pack_acquisition.py",
            "task": "acquire the first source-backed response operator/input pack needed by the chain-kernel runner, prioritizing C_sign, response operator, m profile, L_cg bound, or kernel bounds",
            "success_condition": "at least one RRI1292 missing input is replaced by a source-backed nonclaim row, or a blocker ledger proves no source exists yet",
            "do_not": "do not score the chain residual or claim local GR until the runner accepts rows without MISSING inputs and with response operators",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(RUNNER_SCHEMA_PATH, runner_schema)
    write_csv(REJECTION_RESULTS_PATH, rejection_results)
    write_csv(RESPONSE_REQUIREMENTS_PATH, response_requirements)
    write_csv(NO_SCORE_GUARD_PATH, no_score_guard)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1293_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    structural_ok = all(not row["structural_missing"] or row["structural_missing"] == "NONE" for row in rejection_results)
    validations.append(
        validation_row(
            "VAL1293_1_schema_structural_pass",
            "runner input rows have required structural columns",
            structural_ok and len(rejection_results) == 4,
            f"runner_rows={len(rejection_results)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1293_2_all_rows_rejected",
            "all current rows are rejected as nonclaim/no-score",
            all(row["runner_status"] == "REJECTED_NONCLAIM_NO_SCORE" for row in rejection_results),
            ";".join(f"{row['runner_id']}:{row['reject_codes']}" for row in rejection_results),
        )
    )
    validations.append(
        validation_row(
            "VAL1293_3_missing_inputs_detected",
            "missing inputs are detected on every current row",
            all(int(row["missing_token_count"]) > 0 for row in rejection_results),
            ";".join(f"{row['runner_id']}={row['missing_token_count']}" for row in rejection_results),
        )
    )
    validations.append(
        validation_row(
            "VAL1293_4_no_score_emitted",
            "runner emits no score values",
            all(not row["score_value"] and row["score_emitted"] is False for row in rejection_results),
            "score_value blank and score_emitted=false for every row",
        )
    )
    validations.append(
        validation_row(
            "VAL1293_5_response_requirements_blocked",
            "response operator requirements remain blocked",
            all("MISSING" in row["status"] for row in response_requirements),
            f"response_requirement_rows={len(response_requirements)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1293_6_no_score_guard_pass",
            "no-score guard rows pass",
            all(row["status"] == "PASS" and is_false(row["score_emitted"]) for row in no_score_guard),
            f"guard_rows={len(no_score_guard)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1293_7_claim_gates_blocked",
            "claim gates block local GR/PPN promotion",
            all(is_false(row["claim_allowed"]) for row in claim_gates)
            and any("BLOCKED" in row["current_status"] for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        RUNNER_SCHEMA_PATH,
        REJECTION_RESULTS_PATH,
        RESPONSE_REQUIREMENTS_PATH,
        NO_SCORE_GUARD_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1293_8_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1293_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1293_10_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, runner_schema, rejection_results, response_requirements, no_score_guard, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1293_11_next_target_1294",
            "next target routes to response operator/input pack acquisition",
            next_target[0]["next_id"] == "NEXT1293_0_1294" and "input pack" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1293_12_overall",
            "overall 1293 validation",
            overall_pass,
            "1293 builds a structural residual runner schema, rejects all current rows due missing/nonclaim inputs, emits no score, and routes to response/input acquisition",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1293 Y5 R10 RAB chain-kernel residual runner schema and rejection smoke

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1293 builds the chain-kernel residual runner as a hard rejection gate. It consumes the `RRI1292` rows, validates their structure, and rejects every current row because theorem/numeric inputs and response operators are still missing. No score is emitted.

**Main progress:** the local residual branch is now machine-gated. Future work cannot accidentally turn the strict double-zero closure or symbolic residual formulas into a Newton/PPN/R10/local-GR claim: the runner requires no `MISSING_*` tokens, sourced anchors, claim flags, and response operators before scoring.

**Next derivation target:** acquire the first source-backed input pack or response operator needed by the runner, prioritizing `C_sign`, `m` profile, `L_cg` bounds, metric-kernel bounds, and local response operators.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Runner Schema

{markdown_table(runner_schema, ["schema_id", "requirement", "pass_condition", "on_fail", "valid_for_claim", "claim_allowed"])}

## Rejection Smoke Results

{markdown_table(rejection_results, ["runner_id", "residual_component", "mapped_tests", "source_exists", "anchor_found", "missing_token_count", "missing_tokens", "structural_missing", "reject_codes", "score_emitted", "score_value", "runner_status", "valid_for_claim", "claim_allowed"])}

## Response Operator Requirements

{markdown_table(response_requirements, ["requirement_id", "arena", "required_operator", "current_evidence", "status", "blocks_runner_rows", "valid_for_claim", "claim_allowed"])}

## No-Score Guard

{markdown_table(no_score_guard, ["guard_id", "policy", "observed", "status", "score_emitted", "valid_for_claim", "claim_allowed"])}

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
