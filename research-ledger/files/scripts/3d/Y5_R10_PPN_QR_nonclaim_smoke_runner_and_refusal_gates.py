from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1241"
TITLE = "1241-Y5-R10-PPN-QR-nonclaim-smoke-runner-and-refusal-gates"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
RUNNER_RULES_PATH = OUT_DIR / f"{PACK_ID}_NONCLAIM_RUNNER_RULES.csv"
SMOKE_CASES_PATH = OUT_DIR / f"{PACK_ID}_SMOKE_CASES.csv"
SMOKE_RESULTS_PATH = OUT_DIR / f"{PACK_ID}_SMOKE_RESULTS.csv"
REFUSAL_GATES_PATH = OUT_DIR / f"{PACK_ID}_REFUSAL_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1241_VALIDATION.csv"


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


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def is_missing(value: object) -> bool:
    text = str(value).strip().upper()
    return text == "" or text.startswith("MISSING")


def compute_smoke(case: dict[str, object]) -> dict[str, object]:
    branch_type = str(case["branch_type"])
    value_mode = str(case["value_mode"])
    q_value = case.get("q_R_hat", "")
    n_sigma = case.get("N_sigma", "")
    sigma_gamma = case.get("sigma_gamma", "")

    gamma_projection = ""
    abs_gamma_projection = ""
    pass_rule_evaluated = False
    raw_pass = False

    if not is_missing(q_value):
        q_numeric = float(q_value)
        gamma_projection = -0.5 * q_numeric
        abs_gamma_projection = abs(gamma_projection)
        if not is_missing(n_sigma) and not is_missing(sigma_gamma):
            pass_rule_evaluated = True
            raw_pass = abs_gamma_projection <= float(n_sigma) * float(sigma_gamma)

    if branch_type == "closure_benchmark":
        status = "REFUSED_CLOSURE_NOT_EVIDENCE"
        reason = "closure q_R=0 may be displayed as private baseline but cannot pass as evidence"
    elif value_mode == "comparator_only":
        status = "REFUSED_COMPARATOR_ONLY"
        reason = "Cassini comparator exists but no MTS q_R_hat prediction/value is supplied"
    elif is_missing(q_value):
        status = "REFUSED_MISSING_QR"
        reason = "finite residual row lacks numeric q_R_hat or derived zero theorem"
    elif is_missing(n_sigma) or is_missing(sigma_gamma):
        status = "REFUSED_MISSING_STATISTICAL_POLICY"
        reason = "numeric q_R_hat exists but no N_sigma/sigma_gamma pass policy is supplied"
    elif str(case.get("source_status", "")).startswith("hypothetical"):
        status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
        reason = "synthetic value exercises arithmetic only; it is not a sourced MTS prediction"
    elif raw_pass:
        status = "READY_NONCLAIM_NUMERIC_PASS"
        reason = "would pass the numeric inequality, but valid_for_claim remains false until source and model gates close"
    else:
        status = "READY_NONCLAIM_NUMERIC_FAIL"
        reason = "numeric inequality fails under declared policy"

    return {
        "case_id": case["case_id"],
        "branch_type": branch_type,
        "q_R_hat": q_value,
        "gamma_minus_1_QR": gamma_projection,
        "abs_gamma_minus_1_QR": abs_gamma_projection,
        "N_sigma": n_sigma,
        "sigma_gamma": sigma_gamma,
        "pass_rule_evaluated": pass_rule_evaluated,
        "raw_numeric_pass": raw_pass,
        "runner_status": status,
        "refusal_or_status_reason": reason,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1241_0_1240_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_NEXT_TARGET.csv",
            "needle": "NEXT1240_0_1241",
            "purpose": "1240 handoff to Q_R nonclaim smoke runner",
        },
        {
            "source_id": "SRC1241_1_1240_bound_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv",
            "needle": "QB1240_0_qR_input",
            "purpose": "Q_R bound input schema",
        },
        {
            "source_id": "SRC1241_2_1240_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "QMAP1240_3_gamma_projection",
            "purpose": "Q_R to gamma projection schema",
        },
        {
            "source_id": "SRC1241_3_1240_comparator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_PPN_COMPARATOR_LEDGER.csv",
            "needle": "COMP1240_0_gamma_Cassini",
            "purpose": "Cassini gamma comparator status",
        },
        {
            "source_id": "SRC1241_4_1240_zero_attempt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv",
            "needle": "ZQR1240_5_verdict",
            "purpose": "Q_R zero theorem refused",
        },
        {
            "source_id": "SRC1241_5_1239_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1239_BRANCH_INPUT_ROWS_TEMPLATE.csv",
            "needle": "IN1239_1_QR_finite",
            "purpose": "finite Q_R input row from 1239",
        },
        {
            "source_id": "SRC1241_6_1181_gamma",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv",
            "needle": "PPNV1181_0_gamma",
            "purpose": "gamma comparator source row",
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

    runner_rules = [
        {
            "rule_id": "RULE1241_0_projection",
            "rule": "gamma_minus_1_QR = -0.5*q_R_hat",
            "applies_to": "finite_residual rows with numeric q_R_hat",
            "refusal_if": "q_R_hat missing or not normalized",
            "claim_policy": "nonclaim projection schema only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1241_1_closure",
            "rule": "branch_type=closure_benchmark can compute gamma=0 but must return REFUSED_CLOSURE_NOT_EVIDENCE",
            "applies_to": "closure q_R=0 rows",
            "refusal_if": "always refused as evidence",
            "claim_policy": "private baseline only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1241_2_comparator",
            "rule": "Cassini gamma comparator cannot score without an MTS q_R_hat prediction/value",
            "applies_to": "comparator-only rows",
            "refusal_if": "no q_R_hat supplied",
            "claim_policy": "comparator is not a prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1241_3_pass_policy",
            "rule": "pass_rule requires N_sigma and sigma_gamma",
            "applies_to": "numeric finite rows",
            "refusal_if": "statistical policy missing",
            "claim_policy": "even numeric pass remains nonclaim until source/model gates close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    smoke_cases = [
        {
            "case_id": "CASE1241_0_closure_zero",
            "description": "closure benchmark q_R_hat=0",
            "branch_type": "closure_benchmark",
            "value_mode": "closure_value",
            "q_R_hat": "0",
            "N_sigma": "MISSING_STATISTICAL_POLICY",
            "sigma_gamma": "2.3e-5",
            "source_status": "closure_only",
            "expected_status": "REFUSED_CLOSURE_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1241_1_finite_missing_qR",
            "description": "finite row from 1239/1240 with q_R_hat missing",
            "branch_type": "finite_residual",
            "value_mode": "missing_source",
            "q_R_hat": "MISSING_QR_VALUE",
            "N_sigma": "MISSING_STATISTICAL_POLICY",
            "sigma_gamma": "2.3e-5",
            "source_status": "missing_source",
            "expected_status": "REFUSED_MISSING_QR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1241_2_comparator_only",
            "description": "Cassini comparator loaded without MTS q_R_hat",
            "branch_type": "finite_residual",
            "value_mode": "comparator_only",
            "q_R_hat": "MISSING_QR_VALUE",
            "N_sigma": "1",
            "sigma_gamma": "2.3e-5",
            "source_status": "comparator_available_prediction_missing",
            "expected_status": "REFUSED_COMPARATOR_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1241_3_numeric_no_policy",
            "description": "numeric q_R_hat supplied but pass policy missing",
            "branch_type": "finite_residual",
            "value_mode": "numeric_value",
            "q_R_hat": "1.0e-5",
            "N_sigma": "MISSING_STATISTICAL_POLICY",
            "sigma_gamma": "2.3e-5",
            "source_status": "hypothetical_schema_math_only",
            "expected_status": "REFUSED_MISSING_STATISTICAL_POLICY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1241_4_hypothetical_numeric",
            "description": "synthetic numeric row exercises arithmetic only",
            "branch_type": "finite_residual",
            "value_mode": "numeric_value",
            "q_R_hat": "1.0e-5",
            "N_sigma": "1",
            "sigma_gamma": "2.3e-5",
            "source_status": "hypothetical_schema_math_only",
            "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    smoke_results = [compute_smoke(case) for case in smoke_cases]

    refusal_gates = [
        {
            "gate_id": "REF1241_0_closure_refused",
            "refusal": "closure q_R=0 cannot pass as evidence",
            "case_id": "CASE1241_0_closure_zero",
            "expected_status": "REFUSED_CLOSURE_NOT_EVIDENCE",
            "observed_status": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_0_closure_zero"),
            "gate_pass": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_0_closure_zero") == "REFUSED_CLOSURE_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "REF1241_1_missing_qR_refused",
            "refusal": "finite row with missing q_R_hat cannot score",
            "case_id": "CASE1241_1_finite_missing_qR",
            "expected_status": "REFUSED_MISSING_QR",
            "observed_status": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_1_finite_missing_qR"),
            "gate_pass": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_1_finite_missing_qR") == "REFUSED_MISSING_QR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "REF1241_2_comparator_only_refused",
            "refusal": "Cassini comparator alone cannot become an MTS prediction",
            "case_id": "CASE1241_2_comparator_only",
            "expected_status": "REFUSED_COMPARATOR_ONLY",
            "observed_status": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_2_comparator_only"),
            "gate_pass": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_2_comparator_only") == "REFUSED_COMPARATOR_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "REF1241_3_policy_refused",
            "refusal": "numeric q_R_hat without statistical policy cannot score",
            "case_id": "CASE1241_3_numeric_no_policy",
            "expected_status": "REFUSED_MISSING_STATISTICAL_POLICY",
            "observed_status": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_3_numeric_no_policy"),
            "gate_pass": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_3_numeric_no_policy") == "REFUSED_MISSING_STATISTICAL_POLICY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "REF1241_4_hypothetical_nonclaim",
            "refusal": "synthetic numeric arithmetic is not evidence",
            "case_id": "CASE1241_4_hypothetical_numeric",
            "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "observed_status": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_4_hypothetical_numeric"),
            "gate_pass": next(row["runner_status"] for row in smoke_results if row["case_id"] == "CASE1241_4_hypothetical_numeric") == "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1241_0_runner_refuses_correctly",
            "decision": "keep Q_R smoke runner as refusal-first nonclaim tool",
            "because": "closure, missing finite, comparator-only, missing-policy, and hypothetical rows are all blocked from claims",
            "next_action": "acquire real q_R_hat or derive Q_R=0 before any numeric score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1241_1_next_input",
            "decision": "next useful work is q_R_hat source/theorem acquisition",
            "because": "the runner logic is ready but the physics input remains missing",
            "next_action": "write source/theorem intake contract for q_R_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1241_0_smoke_runner",
            "claim": "nonclaim smoke runner exists",
            "status": "PASS_NONCLAIM",
            "reason": "smoke cases and refusal gates generated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1241_1_QR_numeric_pass",
            "claim": "finite Q_R passes gamma bound",
            "status": "BLOCKED",
            "reason": "no sourced q_R_hat and no statistical policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1241_2_closure_evidence",
            "claim": "closure Q_R=0 counts as evidence",
            "status": "BLOCKED",
            "reason": "CASE1241_0 is refused as closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1241_3_local_GR",
            "claim": "derived local GR/Newton pass",
            "status": "BLOCKED",
            "reason": "Q_R finite input/theorem, beta, source, and conservation remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1241_0_1242",
            "target_file": "1242-Y5-R10-QR-hat-source-or-zero-theorem-input-contract.md",
            "target_script": "scripts/Y5_R10_QR_hat_source_or_zero_theorem_input_contract.py",
            "task": "define the exact acceptable input contract for q_R_hat: either a parent zero-charge theorem source or a finite normalized q_R_hat value with GM convention, units, statistical policy, and provenance",
            "success_condition": "future Q_R smoke runner can load a real candidate row or reject it for precise missing fields",
            "do_not_do": "do not fabricate q_R_hat, do not use closure zero as input evidence, and do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        RUNNER_RULES_PATH,
        SMOKE_CASES_PATH,
        SMOKE_RESULTS_PATH,
        REFUSAL_GATES_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(RUNNER_RULES_PATH, runner_rules)
    write_csv(SMOKE_CASES_PATH, smoke_cases)
    write_csv(SMOKE_RESULTS_PATH, smoke_results)
    write_csv(REFUSAL_GATES_PATH, refusal_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            runner_rules,
            smoke_cases,
            smoke_results,
            refusal_gates,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    all_refusal_gates_pass = all(parse_bool(row["gate_pass"]) for row in refusal_gates)
    closure_refused = any(row["runner_status"] == "REFUSED_CLOSURE_NOT_EVIDENCE" for row in smoke_results)
    missing_qr_refused = any(row["runner_status"] == "REFUSED_MISSING_QR" for row in smoke_results)
    comparator_refused = any(row["runner_status"] == "REFUSED_COMPARATOR_ONLY" for row in smoke_results)
    hypothetical_nonclaim = any(row["runner_status"] == "SCHEMA_MATH_ONLY_NOT_EVIDENCE" for row in smoke_results)
    no_claim_pass = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    next_is_1242 = next_target[0]["target_file"].startswith("1242-Y5-R10-QR-hat")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1241_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1241_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1241_2_refusal_gates",
            "all refusal gates pass",
            all_refusal_gates_pass,
            f"refusal_gates={sum(parse_bool(row['gate_pass']) for row in refusal_gates)}/{len(refusal_gates)}",
        ),
        validation_row(
            "VAL1241_3_closure_refused",
            "closure Q_R=0 is refused as evidence",
            closure_refused,
            "REFUSED_CLOSURE_NOT_EVIDENCE present",
        ),
        validation_row(
            "VAL1241_4_missing_qR_refused",
            "finite row missing q_R_hat is refused",
            missing_qr_refused,
            "REFUSED_MISSING_QR present",
        ),
        validation_row(
            "VAL1241_5_comparator_refused",
            "comparator-only row is refused",
            comparator_refused,
            "REFUSED_COMPARATOR_ONLY present",
        ),
        validation_row(
            "VAL1241_6_hypothetical_nonclaim",
            "hypothetical arithmetic row remains nonclaim",
            hypothetical_nonclaim,
            "SCHEMA_MATH_ONLY_NOT_EVIDENCE present",
        ),
        validation_row(
            "VAL1241_7_claim_gates",
            "claim gates remain blocked/nonclaim",
            no_claim_pass,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1241_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1241_9_next_target_1242",
            "next target is q_R_hat input contract",
            next_is_1242,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1241_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1241_11_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1241_12_overall",
            "overall 1241 validation",
            all(row["status"] == "PASS" for row in validation),
            "1241 builds a refusal-first nonclaim Q_R smoke runner and proves closure/comparator/missing-source rows cannot pass as evidence",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1241 builds the `Q_R -> gamma` nonclaim smoke runner and it refuses the dangerous cases correctly: closure zero, missing finite `q_R_hat`, comparator-only, and missing statistical policy.",
        "",
        "**Main progress:** the local-GR testing lane now has executable refusal logic. A sourced finite `q_R_hat` or a real zero-charge theorem is still missing, but the runner will no longer confuse closure with evidence.",
        "",
        "**No-claim guard:** no derived GR, local-GR pass, PPN pass, WEP/R10 pass, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Nonclaim Runner Rules",
        markdown_table(runner_rules, list(runner_rules[0].keys())),
        "",
        "## Smoke Cases",
        markdown_table(smoke_cases, list(smoke_cases[0].keys())),
        "",
        "## Smoke Results",
        markdown_table(smoke_results, list(smoke_results[0].keys())),
        "",
        "## Refusal Gates",
        markdown_table(refusal_gates, list(refusal_gates[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
