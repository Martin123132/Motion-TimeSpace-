from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1295"
TITLE = "1295-Y5-R10-RAB-Csign-promotion-test-or-first-response-operator-source"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PROMOTION_TEST_PATH = OUT_DIR / f"{PACK_ID}_CSIGN_PROMOTION_TEST.csv"
ABS_BOUND_ROW_PATH = OUT_DIR / f"{PACK_ID}_ABS_CSIGN_BOUND_INPUT_ROW.csv"
RUNNER_PREVIEW_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_INPUT_PREVIEW_NONCLAIM.csv"
RESPONSE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_RESPONSE_OPERATOR_SOURCE_ATTEMPT.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1295_VALIDATION.csv"

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


def is_true(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        PROMOTION_TEST_PATH,
        ABS_BOUND_ROW_PATH,
        RUNNER_PREVIEW_PATH,
        RESPONSE_ATTEMPT_PATH,
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


def preview_required_inputs(required_inputs: str) -> tuple[str, bool, list[str]]:
    tokens = split_semicolon(required_inputs)
    applied = "MISSING_C_SIGN" in tokens
    preview_tokens = ["ABS_C_SIGN_EQ_1_BOUND_ONLY" if token == "MISSING_C_SIGN" else token for token in tokens]
    remaining = [token for token in preview_tokens if token.startswith("MISSING")]
    return ";".join(preview_tokens), applied, remaining


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    runner_rows = read_csv(INPUT_PATH)

    source_register = [
        {
            "source_id": "SRC1295_0_1294_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1294_NEXT_TARGET.csv",
            "needle": "NEXT1294_0_1295",
            "role": "handoff into Csign promotion test",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1295_1_1294_Csign_candidate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1294_C_SIGN_CONVENTION_CANDIDATE.csv",
            "needle": "SOURCE_BACKED_CONVENTION_CANDIDATE_NOT_PROMOTED",
            "role": "prior Csign convention candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1295_2_runner_abs_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "needle": "abs(C_sign)",
            "role": "runner prediction forms only require absolute Csign in current bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1295_3_GK_action",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
            "needle": "T_GK^{mu nu} = Gamma_eff g^{mu nu} - K_metric^{mu nu}",
            "role": "oriented sign convention branch for stress versus Kmetric response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1295_4_derivative_chain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "needle": "C_sign fixed by Hilbert-stress convention",
            "role": "Csign is a convention sign, not a fitted amplitude coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1295_5_GK_contract",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "K_hat is exactly the metric response of Gamma_eff",
            "role": "blocks oriented physical sign promotion without Khat/Kmetric closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1295_6_Kgamma_volume",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "needle": "fixed sign/volume convention matching 514/733",
            "role": "blocks full sign/volume claim promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1295_7_response_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "needle": "no arena is scoreable until response operators and observable limits are sourced",
            "role": "response operator route remains the next scoring bottleneck",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1295_8_KL_budget",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "needle": "q_loc=0 does not set the PPN residual vector to zero",
            "role": "why a response operator is still required even after Csign bound input is filled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    promotion_test = [
        {
            "test_id": "CPT1295_0_action_stress_convention",
            "clause": "GK514 gives a concrete action/stress convention branch",
            "evidence": "S_GK=-int sqrt(-g) Gamma_eff and T_GK=Gamma_eff g-K_metric",
            "source_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
            "source_anchor": "GK514_A_metric_response_scalar_density",
            "result": "PASS_CONVENTION_BRANCH",
            "consequence": "oriented Csign can be discussed relative to K_metric, not as free physics",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1295_1_Csign_is_sign_not_coupling",
            "clause": "C_sign is fixed by a Hilbert-stress convention",
            "evidence": "1289 labels C_sign as fixed by Hilbert-stress convention in the Kmetric_chain row",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "result": "PASS_ABSOLUTE_MAGNITUDE_ONLY",
            "consequence": "for absolute-value bounds, |C_sign|=1 can be used as a nonclaim bound input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1295_2_runner_uses_abs_Csign",
            "clause": "current R_m and R_L prediction forms use abs(C_sign)",
            "evidence": "RRI1292_0 and RRI1292_1 bound forms contain abs(C_sign)",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "source_anchor": "RRI1292_0_m_chain;RRI1292_1_Lcg_chain",
            "result": "PASS_FOR_BOUND_RUNNER_PREVIEW",
            "consequence": "MISSING_C_SIGN can be replaced by ABS_C_SIGN_EQ_1_BOUND_ONLY in absolute-bound preview rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1295_3_oriented_sign",
            "clause": "physical/oriented sign of the stress contribution is fixed for all equations",
            "evidence": "volume subtraction and covariant/contravariant metric variation convention are not locked",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "source_anchor": "KGL776_0_volume_piece",
            "result": "BLOCKED_ORIENTED_SIGN_NOT_PROMOTED",
            "consequence": "do not use C_sign to make cancellation or physical-source-sign claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1295_4_Khat_Kmetric_match",
            "clause": "K_hat is exactly K_metric including derivative and boundary terms",
            "evidence": "MR514 requires this; KGL776 still records missing explicit Khat-Kgamma match and derivative/boundary terms",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "source_anchor": "MR514_1_Khat_metric_response;KGL776_4_current_Khat_match",
            "result": "BLOCKED_KHAT_MATCH_NOT_PROVEN",
            "consequence": "no local-GR or q_loc owner claim follows from the sign split",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1295_5_response_operator",
            "clause": "local response operator exists for scoring",
            "evidence": "1288 and 796 keep response matrices and local observable maps missing",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "source_anchor": "RMR1288_7_response_verdict;KLB796_5_acceptance_condition",
            "result": "BLOCKED_RESPONSE_OPERATOR_MISSING",
            "consequence": "runner remains no-score after Csign absolute bound input is filled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    abs_bound_row = [
        {
            "input_id": "ACB1295_0_abs_Csign_bound_only",
            "input_name": "abs_C_sign",
            "input_value": "1",
            "scope": "absolute_value_residual_bounds_only",
            "derived_from": "C_sign is a Hilbert-stress convention sign and current RRI1292 prediction forms use abs(C_sign)",
            "replaces_missing_token": "MISSING_C_SIGN in RRI1292_0_m_chain and RRI1292_1_Lcg_chain bound previews only",
            "usable_in_abs_bound_runner": True,
            "usable_in_oriented_equations": False,
            "blocks_before_claim": "ORIENTED_SIGN_LOCK;VOLUME_SUBTRACTION;KHAT_KMETRIC_MATCH;RESPONSE_OPERATOR;OTHER_INPUTS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00;RRI1292_0_m_chain;RRI1292_1_Lcg_chain",
            "current_status": "PROMOTED_FOR_ABSOLUTE_BOUND_PREVIEW_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    runner_preview = []
    for row in runner_rows:
        preview_inputs, applied, remaining = preview_required_inputs(row.get("required_inputs", ""))
        runner_preview.append(
            {
                "preview_id": f"RIP1295_{len(runner_preview)}",
                "runner_id": row.get("runner_id", ""),
                "residual_component": row.get("residual_component", ""),
                "abs_Csign_bound_applied": applied,
                "required_inputs_original": row.get("required_inputs", ""),
                "required_inputs_preview": preview_inputs,
                "remaining_missing_count": len(remaining),
                "remaining_missing_tokens": ";".join(remaining) if remaining else "NONE",
                "score_emitted": False,
                "score_value": "",
                "runner_status": "PARTIALLY_FILLED_STILL_REJECTED_NONCLAIM_NO_SCORE" if remaining else "FILLED_FOR_THIS_TOKEN_ONLY_STILL_NONCLAIM_NO_SCORE",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    response_attempt = [
        {
            "attempt_id": "ROA1295_0_response_operator_not_acquired_this_step",
            "route": "response_operator_source",
            "attempt_result": "DEFERRED_AFTER_ABS_CSIGN_PROGRESS",
            "reason": "1295 produced a legitimate bound-only Csign input; response operator remains the next scoring bottleneck and needs a dedicated source acquisition pass",
            "best_next_source_targets": "linearized_GR_or_PPN_metric_response;Newton_source_normalization;clock_orbital_R10_readout",
            "current_blockers": "MISSING_RESPONSE_MATRIX;MISSING_KBAR_L_LOC_00;MISSING_R_PPN_GAMMA;MISSING_R_CLOCK;MISSING_R_ORBITAL;MISSING_R_R10_LAMBDA",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "source_anchor": "RMR1288_7_response_verdict;KLB796_5_acceptance_condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "CG1295_0_abs_Csign_bound_input",
            "claim": "|C_sign|=1 may be used in absolute residual bound previews",
            "current_status": "SATISFIED_FOR_NONCLAIM_ABS_BOUND_ONLY",
            "reason": "Csign is a convention sign and the active bound rows use abs(C_sign)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1295_1_oriented_Csign",
            "claim": "oriented physical C_sign is promoted",
            "current_status": "BLOCKED_ORIENTED_SIGN_NOT_PROMOTED",
            "reason": "volume subtraction, Hilbert variation convention, Khat/Kmetric match, and boundary terms remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1295_2_runner_score",
            "claim": "runner can emit residual/local-GR scores",
            "current_status": "BLOCKED_REMAINING_MISSING_INPUTS",
            "reason": "m, L_cg, F/Fprime, metric kernels, CDB bounds, and response operators remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1295_3_response_operator",
            "claim": "first local response operator is sourced",
            "current_status": "BLOCKED_DEDICATED_SOURCE_PASS_REQUIRED",
            "reason": "current files contain requirements/templates, not a source-backed response operator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1295_4_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "absolute Csign is a useful input-pack fill, not a response or recovery proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1295_0_split_Csign_gate",
            "decision": "split Csign into absolute-bound and oriented-physical gates",
            "because": "the runner bound formulas only need abs(C_sign), while physical stress/cancellation signs need stronger convention closure",
            "next_action": "use ABS_C_SIGN_EQ_1_BOUND_ONLY in preview rows but do not score until remaining inputs and response operators exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1295_1_no_oriented_promotion",
            "decision": "do not promote oriented Csign",
            "because": "Khat/Kmetric equality and sign/volume conventions remain open in 514/776/1287",
            "next_action": "retain oriented sign as a closure target, not an empirical claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1295_2_next_bottleneck",
            "decision": "route next checkpoint to response-operator sourcing",
            "because": "after the Csign token is neutralized for absolute bounds, every local score still dies on response maps and observable limits",
            "next_action": "source a linearized-GR/Newton/PPN response operator or record a hard blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1295_0_1296",
            "target_file": "1296-Y5-R10-RAB-linearized-GR-response-operator-source-or-hard-blocker.md",
            "target_script": "scripts/Y5_R10_RAB_linearized_GR_response_operator_source_or_hard_blocker.py",
            "task": "acquire the first source-backed local response operator, starting from linearized GR/Newton source normalization and then mapping to PPN/clock/orbital/R10 requirements",
            "success_condition": "one response operator row becomes source-backed nonclaim with clear units and domain, or a blocker ledger proves no usable source has been acquired",
            "do_not": "do not emit local-GR scores until response operators, remaining numeric/theorem inputs, and claim gates all pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PROMOTION_TEST_PATH, promotion_test)
    write_csv(ABS_BOUND_ROW_PATH, abs_bound_row)
    write_csv(RUNNER_PREVIEW_PATH, runner_preview)
    write_csv(RESPONSE_ATTEMPT_PATH, response_attempt)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1295_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    abs_passes = [row for row in promotion_test if str(row["result"]).startswith("PASS")]
    blocked_rows = [row for row in promotion_test if str(row["result"]).startswith("BLOCKED")]
    validations.append(
        validation_row(
            "VAL1295_1_promotion_split_recorded",
            "promotion test splits absolute-bound pass from oriented-sign blockers",
            len(abs_passes) == 3 and len(blocked_rows) == 3,
            f"pass_rows={len(abs_passes)};blocked_rows={len(blocked_rows)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1295_2_abs_Csign_bound_row",
            "absolute Csign row is usable only for nonclaim bound previews",
            len(abs_bound_row) == 1
            and is_true(abs_bound_row[0]["usable_in_abs_bound_runner"])
            and is_false(abs_bound_row[0]["usable_in_oriented_equations"])
            and str(abs_bound_row[0]["input_value"]) == "1",
            str(abs_bound_row[0]["current_status"]),
        )
    )
    applied_rows = [row for row in runner_preview if row["abs_Csign_bound_applied"] is True]
    validations.append(
        validation_row(
            "VAL1295_3_runner_preview_updates_two_rows",
            "runner preview replaces MISSING_C_SIGN in exactly the m and Lcg rows",
            len(applied_rows) == 2
            and all("ABS_C_SIGN_EQ_1_BOUND_ONLY" in row["required_inputs_preview"] for row in applied_rows),
            ";".join(row["runner_id"] for row in applied_rows),
        )
    )
    validations.append(
        validation_row(
            "VAL1295_4_runner_still_rejected",
            "all runner preview rows remain no-score with missing inputs",
            all(int(row["remaining_missing_count"]) > 0 and is_false(row["score_emitted"]) for row in runner_preview),
            ";".join(f"{row['runner_id']}={row['remaining_missing_count']}" for row in runner_preview),
        )
    )
    validations.append(
        validation_row(
            "VAL1295_5_response_operator_not_claimed",
            "response operator remains unacquired and routed to next target",
            response_attempt[0]["attempt_result"] == "DEFERRED_AFTER_ABS_CSIGN_PROGRESS"
            and "MISSING_RESPONSE_MATRIX" in response_attempt[0]["current_blockers"],
            str(response_attempt[0]["reason"]),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        PROMOTION_TEST_PATH,
        ABS_BOUND_ROW_PATH,
        RUNNER_PREVIEW_PATH,
        RESPONSE_ATTEMPT_PATH,
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
    validations.append(validation_row("VAL1295_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1295_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1295_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, promotion_test, abs_bound_row, runner_preview, response_attempt, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1295_9_next_target_1296",
            "next target routes to linearized GR response operator acquisition",
            next_target[0]["next_id"] == "NEXT1295_0_1296" and "linearized-GR-response-operator" in next_target[0]["target_file"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1295_10_overall",
            "overall 1295 validation",
            overall_pass,
            "1295 promotes |C_sign|=1 for absolute bound previews only, keeps oriented sign/claims blocked, preserves no-score status, and routes to response-operator sourcing",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1295 Y5 R10 RAB Csign promotion test or first response-operator source

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1295 gets a real small win without cheating: the oriented physical `C_sign` is **not** promoted, but `|C_sign|=1` is promoted for absolute-value residual-bound previews only. The reason is that the current `RRI1292` bound formulas use `abs(C_sign)`, and 1289 identifies `C_sign` as a Hilbert-stress convention sign rather than a fitted coupling amplitude.

**Main progress:** the `MISSING_C_SIGN` token is now removable in the two bound rows where it appears, but only as `ABS_C_SIGN_EQ_1_BOUND_ONLY`. This reduces the m-chain and `L_cg`-chain missing-input counts by one each while preserving the runner rejection/no-score guard.

**Still blocked:** oriented stress signs, local-GR claims, and q_loc ownership remain blocked by sign/volume convention closure, `K_hat=K_metric`, derivative/boundary terms, and response operators. The next useful bottleneck is now the first source-backed local response operator.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Csign Promotion Test

{markdown_table(promotion_test, ["test_id", "clause", "evidence", "source_path", "source_anchor", "result", "consequence", "valid_for_claim", "claim_allowed"])}

## Absolute Csign Bound Input Row

{markdown_table(abs_bound_row, ["input_id", "input_name", "input_value", "scope", "derived_from", "replaces_missing_token", "usable_in_abs_bound_runner", "usable_in_oriented_equations", "blocks_before_claim", "source_path", "source_anchor", "current_status", "valid_for_claim", "claim_allowed"])}

## Runner Input Preview

{markdown_table(runner_preview, ["preview_id", "runner_id", "residual_component", "abs_Csign_bound_applied", "required_inputs_preview", "remaining_missing_count", "remaining_missing_tokens", "score_emitted", "score_value", "runner_status", "valid_for_claim", "claim_allowed"])}

## Response Operator Source Attempt

{markdown_table(response_attempt, ["attempt_id", "route", "attempt_result", "reason", "best_next_source_targets", "current_blockers", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

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
