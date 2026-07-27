from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1245"
TITLE = "1245-Y5-R10-PPN-QR-policy-fed-smoke-runner-and-source-hunt-update"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
POLICY_FED_CASES_PATH = OUT_DIR / f"{PACK_ID}_POLICY_FED_CASES.csv"
POLICY_FED_RESULTS_PATH = OUT_DIR / f"{PACK_ID}_POLICY_FED_RESULTS.csv"
BLOCKER_DELTA_PATH = OUT_DIR / f"{PACK_ID}_BLOCKER_DELTA.csv"
SOURCE_HUNT_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_HUNT_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1245_VALIDATION.csv"


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


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def is_missing(value: object) -> bool:
    text = str(value).strip()
    return text == "" or text.startswith("MISSING")


def is_false(row: dict[str, object], key: str) -> bool:
    return str(row.get(key, "")).strip().lower() in {"false", "0", "no"}


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def evaluate_case(case: dict[str, object]) -> dict[str, object]:
    branch_type = str(case["branch_type"])
    value_mode = str(case["value_mode"])
    source_status = str(case.get("source_status", ""))
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
        reason = "closure q_R=0 remains a private baseline and is not evidence"
    elif value_mode == "comparator_only":
        status = "REFUSED_COMPARATOR_ONLY"
        reason = "comparator and policy exist, but no MTS q_R_hat prediction/value is supplied"
    elif is_missing(q_value):
        status = "REFUSED_MISSING_QR"
        reason = "policy and GM convention are now present; finite q_R_hat or zero theorem is still missing"
    elif is_missing(n_sigma) or is_missing(sigma_gamma):
        status = "REFUSED_MISSING_STATISTICAL_POLICY"
        reason = "numeric q_R_hat exists but policy fields are missing"
    elif source_status.startswith("hypothetical"):
        status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
        reason = "synthetic value proves the policy-fed arithmetic only; it is not sourced MTS evidence"
    elif raw_pass:
        status = "READY_NONCLAIM_NUMERIC_PASS"
        reason = "numeric row passes strict smoke arithmetic but remains nonclaim pending source gates"
    else:
        status = "READY_NONCLAIM_NUMERIC_FAIL"
        reason = "numeric row fails strict smoke arithmetic and remains nonclaim"

    return {
        "case_id": case["case_id"],
        "branch_type": branch_type,
        "value_mode": value_mode,
        "q_R_hat": q_value,
        "gamma_minus_1_QR": gamma_projection,
        "abs_gamma_minus_1_QR": abs_gamma_projection,
        "N_sigma": n_sigma,
        "sigma_gamma": sigma_gamma,
        "pass_rule_evaluated": pass_rule_evaluated,
        "raw_numeric_pass": raw_pass,
        "runner_status": status,
        "runner_reason": reason,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def recent_formalization_writes() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    recent: list[Path] = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if mtime >= RUN_STARTED_UTC:
                recent.append(path)
    return recent


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1245_0_1244_feed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "needle": "RPF1244_0_policy",
            "purpose": "policy feed carrying N_sigma, sigma_gamma, q_R_hat guardrail, and missing q_R status",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1245_1_1244_stat_policy",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_PPN_GAMMA_STATISTICAL_POLICY.csv",
            "needle": "STAT1244_0_default_smoke",
            "purpose": "strict one-sigma nonclaim PPN gamma policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1245_2_1244_GM",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            "needle": "GM1244_0_qR_definition",
            "purpose": "GM/source convention contract for q_R_hat normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1245_3_1241_cases",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1241_SMOKE_CASES.csv",
            "needle": "CASE1241_1_finite_missing_qR",
            "purpose": "pre-policy-fix runner case showing finite q_R was missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1245_4_1241_results",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1241_SMOKE_RESULTS.csv",
            "needle": "REFUSED_MISSING_STATISTICAL_POLICY",
            "purpose": "legacy runner result proving numeric rows previously failed missing-policy gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1245_5_1243_hunt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1243_SOURCE_HUNT_LEDGER.csv",
            "needle": "HUNT1243_2_GM_policy",
            "purpose": "source-hunt ledger with GM/statistical policy previously missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1245_6_1240_mapping",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "QMAP1240_3_gamma_projection",
            "purpose": "nonclaim gamma projection map used by runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1245_7_1242_contract",
            "local_path": "1242-Y5-R10-QR-hat-source-or-zero-theorem-input-contract.md",
            "needle": "finite_qR_hat",
            "purpose": "candidate input contract for future finite q_R_hat rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv"))[0]
    n_sigma = feed["N_sigma"]
    sigma_gamma = feed["sigma_gamma"]
    q_guardrail = feed["q_R_hat_abs_guardrail"]

    policy_fed_cases = [
        {
            "case_id": "CASE1245_0_policy_fed_missing_qR",
            "description": "finite MTS row after policy feed; only q_R_hat/source theorem remains missing",
            "branch_type": "finite_residual",
            "value_mode": "missing_source",
            "q_R_hat": "MISSING_QR_VALUE",
            "N_sigma": n_sigma,
            "sigma_gamma": sigma_gamma,
            "GM_convention_status": feed["GM_convention_status"],
            "source_status": "missing_finite_qR_or_zero_theorem",
            "expected_status": "REFUSED_MISSING_QR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1245_1_policy_fed_comparator_only",
            "description": "Cassini comparator plus 1244 policy, still without an MTS q_R_hat prediction",
            "branch_type": "finite_residual",
            "value_mode": "comparator_only",
            "q_R_hat": "MISSING_QR_VALUE",
            "N_sigma": n_sigma,
            "sigma_gamma": sigma_gamma,
            "GM_convention_status": feed["GM_convention_status"],
            "source_status": "comparator_available_prediction_missing",
            "expected_status": "REFUSED_COMPARATOR_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1245_2_policy_fed_hypothetical_pass",
            "description": "synthetic q_R_hat inside strict guardrail; proves arithmetic only",
            "branch_type": "finite_residual",
            "value_mode": "numeric_value",
            "q_R_hat": "1.0e-5",
            "N_sigma": n_sigma,
            "sigma_gamma": sigma_gamma,
            "GM_convention_status": feed["GM_convention_status"],
            "source_status": "hypothetical_schema_math_only",
            "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1245_3_policy_fed_hypothetical_fail",
            "description": "synthetic q_R_hat outside strict guardrail; proves fail path only",
            "branch_type": "finite_residual",
            "value_mode": "numeric_value",
            "q_R_hat": "5.0e-5",
            "N_sigma": n_sigma,
            "sigma_gamma": sigma_gamma,
            "GM_convention_status": feed["GM_convention_status"],
            "source_status": "hypothetical_schema_math_only",
            "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    policy_fed_results = [evaluate_case(row) for row in policy_fed_cases]

    blocker_delta = [
        {
            "blocker_id": "BD1245_0_missing_stat_policy",
            "before_1244": "BLOCKED",
            "after_1245": "CLEARED_NONCLAIM",
            "evidence": "STAT1244_0_default_smoke and RPF1244_0_policy provide N_sigma=1, sigma_gamma=2.3e-5",
            "claim_effect": "no claim; only runner plumbing improved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BD1245_1_missing_GM_convention",
            "before_1244": "BLOCKED",
            "after_1245": "CLEARED_NONCLAIM_CONTRACT_ONLY",
            "evidence": "GM1244_0_qR_definition declares q_R_hat = Q_R c^2/(G M_source)",
            "claim_effect": "no claim; future rows still need source body/GM provenance or direct dimensionless q_R_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BD1245_2_missing_qR_or_zero_theorem",
            "before_1244": "BLOCKED",
            "after_1245": "STILL_BLOCKED",
            "evidence": "RPF1244_0_policy keeps q_R_hat_status=MISSING_QR_VALUE_UNCHANGED; CASE1245_0 returns REFUSED_MISSING_QR",
            "claim_effect": "dominant remaining local-PPN blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BD1245_3_closure_as_evidence",
            "before_1244": "BLOCKED",
            "after_1245": "STILL_BLOCKED_AS_DESIRED",
            "evidence": "1241 closure refusal unchanged; 1245 does not reintroduce closure zero as evidence",
            "claim_effect": "protects derivation discipline",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_hunt_update = [
        {
            "hunt_id": "HUNT1245_0_parent_zero",
            "target": "parent Q_R=0 theorem",
            "status_after_1245": "MISSING",
            "minimum_evidence": "source path proving Q_R=0 from parent action/constraint/topological source representation without assuming R_AB=0 closure",
            "next_action": "derive parent no-charge theorem or explicitly fail it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1245_1_finite_qR_model",
            "target": "finite q_R_hat model",
            "status_after_1245": "MISSING",
            "minimum_evidence": "numeric q_R_hat with source path, units, GM convention, and derivation status; or accepted parent-derived zero theorem",
            "next_action": "build/source finite residual model only after parent terms are signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1245_2_GM_policy",
            "target": "GM/source convention",
            "status_after_1245": "FILLED_NONCLAIM_CONTRACT_ONLY",
            "minimum_evidence": "GM1244_0..3 convention rows",
            "next_action": "future finite rows must bind to this convention or override it explicitly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1245_3_statistical_policy",
            "target": "PPN gamma pass policy",
            "status_after_1245": "FILLED_NONCLAIM",
            "minimum_evidence": "STAT1244_0 strict one-sigma policy and q_R_hat guardrail abs(q_R_hat)<=4.6e-5",
            "next_action": "use only as smoke guardrail until q_R input is sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1245_0_policy_feed_success",
            "decision": "feed 1244 policy into Q_R runner",
            "because": "1241 missing-policy refusal is no longer the live blocker for policy-fed cases",
            "result": "CASE1245_0 refuses for missing q_R_hat, not missing statistical policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1245_1_qR_missing_is_dominant",
            "decision": "treat parent zero theorem or finite q_R_hat as next bottleneck",
            "because": "GM and statistical plumbing are now declared, but q_R_hat_status remains missing",
            "result": "local PPN branch is better isolated but still blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1245_2_no_public_claim",
            "decision": "do not claim local GR/PPN pass",
            "because": "policy-fed arithmetic is not a sourced MTS prediction",
            "result": "all 1245 rows remain private nonclaim rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1245_0_policy_fed_runner",
            "claim": "policy-fed Q_R smoke runner is available",
            "status": "PASS_NONCLAIM",
            "reason": "1244 policy and GM convention feed into 1245 cases",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1245_1_missing_policy_blocker",
            "claim": "missing statistical policy is still the blocker",
            "status": "CLEARED_NONCLAIM",
            "reason": "1245 cases carry N_sigma=1 and sigma_gamma=2.3e-5; no 1245 row returns REFUSED_MISSING_STATISTICAL_POLICY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1245_2_qR_value_or_theorem",
            "claim": "q_R_hat value or Q_R=0 theorem exists",
            "status": "BLOCKED",
            "reason": "CASE1245_0 returns REFUSED_MISSING_QR and feed says MISSING_QR_VALUE_UNCHANGED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1245_3_local_GR",
            "claim": "derived local GR/Newton/PPN pass",
            "status": "BLOCKED",
            "reason": "policy plumbing is not a parent source theorem, finite residual value, beta map, or conservation proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1245_0_1246",
            "target_file": "1246-Y5-R10-parent-QR-zero-theorem-or-finite-residual-source-hunt.md",
            "target_script": "scripts/Y5_R10_parent_QR_zero_theorem_or_finite_residual_source_hunt.py",
            "task": "attack the remaining bottleneck directly: either derive a parent-signed Q_R=0 theorem without closure, or create a finite q_R_hat source-hunt ledger with no claim promotion",
            "success_condition": "missing-policy and GM blockers stay cleared; q_R theorem/value either becomes sourced or remains the sole explicit blocker",
            "do_not": "do not use closure zero, hypothetical q_R_hat, or comparator-only rows as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_sets = [
        source_register,
        policy_fed_cases,
        policy_fed_results,
        blocker_delta,
        source_hunt_update,
        decisions,
        claim_gates,
        next_target,
    ]

    output_paths = [
        SOURCE_REGISTER_PATH,
        POLICY_FED_CASES_PATH,
        POLICY_FED_RESULTS_PATH,
        BLOCKER_DELTA_PATH,
        SOURCE_HUNT_UPDATE_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(POLICY_FED_CASES_PATH, policy_fed_cases)
    write_csv(POLICY_FED_RESULTS_PATH, policy_fed_results)
    write_csv(BLOCKER_DELTA_PATH, blocker_delta)
    write_csv(SOURCE_HUNT_UPDATE_PATH, source_hunt_update)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)

    missing_policy_absent = all(row["runner_status"] != "REFUSED_MISSING_STATISTICAL_POLICY" for row in policy_fed_results)
    missing_qr_refused = any(
        row["case_id"] == "CASE1245_0_policy_fed_missing_qR" and row["runner_status"] == "REFUSED_MISSING_QR"
        for row in policy_fed_results
    )
    comparator_still_refused = any(
        row["case_id"] == "CASE1245_1_policy_fed_comparator_only" and row["runner_status"] == "REFUSED_COMPARATOR_ONLY"
        for row in policy_fed_results
    )
    hypothetical_rows_nonclaim = all(
        row["runner_status"] == "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
        for row in policy_fed_results
        if str(row["case_id"]).startswith("CASE1245_2") or str(row["case_id"]).startswith("CASE1245_3")
    )
    policy_numbers_ok = n_sigma == "1" and sigma_gamma == "2.3e-5" and q_guardrail == "4.6e-05"
    hunt_updated_ok = any(row["status_after_1245"] == "FILLED_NONCLAIM" for row in source_hunt_update) and any(
        row["status_after_1245"] == "MISSING" and row["target"] == "parent Q_R=0 theorem" for row in source_hunt_update
    )
    qR_still_missing = feed["q_R_hat_status"] == "MISSING_QR_VALUE_UNCHANGED" and any(
        row["after_1245"] == "STILL_BLOCKED" for row in blocker_delta
    )
    no_claim_pass = all(
        row["status"] in {"PASS_NONCLAIM", "CLEARED_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and (("claim_allowed" not in row) or is_false(row, "claim_allowed"))
        for rows in generated_sets
        for row in rows
        if "valid_for_claim" in row
    )
    next_is_1246 = next_target[0]["next_id"] == "NEXT1245_0_1246"

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in output_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:PARSE_FAIL:{exc}")

    fw_recent = recent_formalization_writes()

    validation = [
        validation_row("VAL1245_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1245_1_needles_found", "all cited local needles found", all_needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1245_2_policy_numbers", "1244 policy feed numbers are loaded", policy_numbers_ok, f"N_sigma={n_sigma} sigma_gamma={sigma_gamma} q_guardrail={q_guardrail}"),
        validation_row("VAL1245_3_missing_policy_absent", "policy-fed cases no longer fail missing-policy gate", missing_policy_absent, "no 1245 runner_status is REFUSED_MISSING_STATISTICAL_POLICY"),
        validation_row("VAL1245_4_missing_qR_refused", "remaining finite MTS row refuses missing q_R", missing_qr_refused, "CASE1245_0_policy_fed_missing_qR -> REFUSED_MISSING_QR"),
        validation_row("VAL1245_5_comparator_refused", "comparator-only branch still cannot count as prediction", comparator_still_refused, "CASE1245_1_policy_fed_comparator_only -> REFUSED_COMPARATOR_ONLY"),
        validation_row("VAL1245_6_hypothetical_nonclaim", "hypothetical arithmetic remains nonclaim", hypothetical_rows_nonclaim, "synthetic pass/fail cases return SCHEMA_MATH_ONLY_NOT_EVIDENCE"),
        validation_row("VAL1245_7_hunt_update", "source-hunt ledger updates policy/GM while keeping q_R missing", hunt_updated_ok, "GM/stat policy filled; parent zero and finite q_R targets remain missing"),
        validation_row("VAL1245_8_qR_still_missing", "q_R theorem/value remains the dominant blocker", qR_still_missing, "MISSING_QR_VALUE_UNCHANGED and blocker delta STILL_BLOCKED"),
        validation_row("VAL1245_9_claim_gates", "claim gates remain nonclaim/blocked", no_claim_pass, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1245_10_nonclaim_policy", "all generated rows remain nonclaim", all_generated_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1245_11_next_target_1246", "next target attacks Q_R theorem/value bottleneck", next_is_1246, next_target[0]["target_file"]),
        validation_row("VAL1245_12_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parsed_counts)),
        validation_row("VAL1245_13_formalization_untouched", "formalization-workbench untouched during run", len(fw_recent) == 0, f"formalization_recent_write_count_since_run_start={len(fw_recent)}"),
    ]
    validation.append(
        validation_row(
            "VAL1245_14_overall",
            "overall 1245 validation",
            all(row["status"] == "PASS" for row in validation),
            "1245 proves policy/GM plumbing is no longer the live runner blocker; q_R theorem/value remains missing and no claim is promoted",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1245 successfully policy-feeds the Q_R PPN smoke runner: the missing-statistical-policy blocker is cleared, and the live finite-row refusal has narrowed to missing `q_R_hat` or a parent `Q_R=0` theorem.",
        "",
        "**Main progress:** this is small but useful plumbing discipline. We have stopped the runner failing for the wrong reason; it now fails at the real physics bottleneck.",
        "",
        "**No-claim guard:** no local-GR, PPN, R10, WEP, clock, orbital, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Policy-Fed Cases",
        markdown_table(policy_fed_cases, list(policy_fed_cases[0].keys())),
        "",
        "## Policy-Fed Results",
        markdown_table(policy_fed_results, list(policy_fed_results[0].keys())),
        "",
        "## Blocker Delta",
        markdown_table(blocker_delta, list(blocker_delta[0].keys())),
        "",
        "## Source Hunt Update",
        markdown_table(source_hunt_update, list(source_hunt_update[0].keys())),
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
