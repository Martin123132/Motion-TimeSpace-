from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_847_SOURCE_REGISTER.csv"
CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv"
AMPLITUDE_LAW_PATH = RESIDUALS / "P8_Y5_R10_847_PARENT_AMPLITUDE_LAW_STATUS.csv"
ELIGIBILITY_PATH = RESIDUALS / "P8_Y5_R10_847_EXECUTION_ELIGIBILITY.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_847_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_847_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_847_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_847_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_847_VALIDATION.csv"

STATUS = "Y5_R10_847_strict_candidate_file_created_parent_amplitude_still_not_predicted_nonclaim"
CLAIM_CEILING = "candidate_file_for_dry_run_only_no_parent_amplitude_prediction_no_support"
NEXT_TARGET = "848-Y5-R10-strict-cosmology-input-check-runner.md"

FULL_JOINT_B_MEM = 0.1124525903286696
CMB_ONLY_B_MEM = 0.015730508794745142

SOURCE_SPECS = [
    {
        "source_id": "846_doc",
        "path": POST_CHECKPOINT / "846-Y5-R10-strict-cosmology-branch-dry-run-spec.md",
        "needles": [
            "the strict cosmology branch now has a dry-run specification",
            "b_mem_value_or_range",
            "847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md",
        ],
        "role": "dry-run schema handoff",
    },
    {
        "source_id": "846_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_846_VALIDATION.csv",
        "needles": [
            "V846_3_candidate_schema_blocks_missing_values,pass",
            "V846_6_no_long_run_authorized,pass",
            "V846_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "176_C0_demotion_decision",
        "path": FORMALIZATION / "176-C0-radflat-demotion-decision.md",
        "needles": [
            "C0_demoted_to_closure_benchmark_parent_amplitude_repair_required",
            "C0_reference_b_mem = 0.015730508794745142",
            "C0_full_joint_b_mem = 0.1124525903286696",
            "C0_b_mem_fractional_shift = 6.148693776912986",
        ],
        "role": "benchmark amplitude source",
    },
    {
        "source_id": "177_parent_amplitude_repair_contract",
        "path": FORMALIZATION / "177-parent-amplitude-repair-contract.md",
        "needles": [
            "b_mem = a_F DeltaR / [3 eta^2]",
            "without using the full-joint best-fit `b_mem` as input.",
            "The contract is locked, but not satisfied.",
        ],
        "role": "parent amplitude law contract",
    },
    {
        "source_id": "178_parent_amplitude_theorem_attempt",
        "path": FORMALIZATION / "178-parent-amplitude-theorem-attempt.md",
        "needles": [
            "parent_amplitude_theorem_partial_corridor_not_prediction",
            "0 < a_F DeltaR <= 1",
            "eta <= 1.7216887463098034",
            "amplitude prediction derived = false",
        ],
        "role": "parent corridor and nonprediction source",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def b_mem_from_parent_corridor(a_f_delta_r: float, eta: float = 1.0) -> float:
    return a_f_delta_r / (3.0 * eta * eta)


def candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    corridor_values = [
        ("S2_corridor_eta1_aFDeltaR_0p1", 0.1, b_mem_from_parent_corridor(0.1), "low_order_one_parent_corridor_probe"),
        ("S2_corridor_eta1_aFDeltaR_0p3", 0.3, b_mem_from_parent_corridor(0.3), "middle_order_one_parent_corridor_probe"),
        ("S2_corridor_eta1_aFDeltaR_1p0", 1.0, b_mem_from_parent_corridor(1.0), "upper_order_one_parent_corridor_probe"),
    ]
    rows: list[dict[str, object]] = [
        {
            "candidate_id": "S0_null_bmem_0",
            "branch_class": "null_control",
            "b_mem_mode": "zero_control",
            "b_mem_value_or_range": "0.0",
            "b_mem_numeric": "0.0",
            "eta_assumption": "not_applicable",
            "a_F_DeltaR_assumption": "not_applicable",
            "shape_source": "baseline_equivalent_null_control",
            "parameter_count_delta": "0",
            "family_selection_penalty": "0",
            "claim_label": "benchmark_only",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "null control for pipeline and model-selection sanity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "S1_C0_CMB_reference",
            "branch_class": "C0_benchmark",
            "b_mem_mode": "benchmark_display_only",
            "b_mem_value_or_range": f"{CMB_ONLY_B_MEM:.18g}",
            "b_mem_numeric": f"{CMB_ONLY_B_MEM:.18g}",
            "eta_assumption": "not_parent_predicted",
            "a_F_DeltaR_assumption": "not_parent_predicted",
            "shape_source": "176_CMB_only_reference_demoted",
            "parameter_count_delta": "0",
            "family_selection_penalty": "0",
            "claim_label": "benchmark_only",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "demoted CMB-only reference amplitude; not stable support",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "S1_C0_full_joint_reference",
            "branch_class": "C0_benchmark",
            "b_mem_mode": "benchmark_display_only",
            "b_mem_value_or_range": f"{FULL_JOINT_B_MEM:.18g}",
            "b_mem_numeric": f"{FULL_JOINT_B_MEM:.18g}",
            "eta_assumption": "not_parent_predicted",
            "a_F_DeltaR_assumption": "not_parent_predicted",
            "shape_source": "176_full_joint_fit_reference_demoted",
            "parameter_count_delta": "0",
            "family_selection_penalty": "0",
            "claim_label": "benchmark_only",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "full-joint reference amplitude; included only as C0 closure benchmark, not as predeclared support",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]
    for candidate_id, a_f_delta_r, b_mem, note in corridor_values:
        rows.append(
            {
                "candidate_id": candidate_id,
                "branch_class": "predeclared_corridor",
                "b_mem_mode": "fixed_predeclared",
                "b_mem_value_or_range": f"{b_mem:.18g}",
                "b_mem_numeric": f"{b_mem:.18g}",
                "eta_assumption": "eta=1",
                "a_F_DeltaR_assumption": f"{a_f_delta_r:.18g}",
                "shape_source": "178_parent_corridor_order_one_aFDeltaR_probe",
                "parameter_count_delta": "0",
                "family_selection_penalty": "1",
                "claim_label": "exploratory_nonclaim",
                "execution_eligible_for_input_check": "true",
                "execution_eligible_for_scoring": "true",
                "support_claim_allowed": "false",
                "notes": note,
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    rows.append(
        {
            "candidate_id": "S3_parent_predicted_placeholder",
            "branch_class": "parent_predicted",
            "b_mem_mode": "fixed_parent",
            "b_mem_value_or_range": "BLOCKED_NO_UNIQUE_PARENT_PREDICTION",
            "b_mem_numeric": "",
            "eta_assumption": "MISSING_PARENT_ETA",
            "a_F_DeltaR_assumption": "MISSING_PARENT_AF_DELTAR",
            "shape_source": "178_parent_amplitude_prediction_missing",
            "parameter_count_delta": "0",
            "family_selection_penalty": "0",
            "claim_label": "support_grade_candidate_blocked",
            "execution_eligible_for_input_check": "false",
            "execution_eligible_for_scoring": "false",
            "support_claim_allowed": "false",
            "notes": "clean support route exists only after eta, a_F, and DeltaR are parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    )
    return rows


def amplitude_law_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "AL847_0_identity",
            "statement": "b_mem = Omega_Gamma,inf - Omega_Gamma0 = integral S_Gamma dN = a_F DeltaR / (3 eta^2)",
            "status": "formal_identity_survives",
            "source": "177,178",
            "numeric_value": "",
            "blocks_support": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "AL847_1_corridor",
            "statement": "with eta=1 and 0<a_F DeltaR<=1, exploratory b_mem probes may span 0<b_mem<=1/3",
            "status": "predeclared_corridor_only",
            "source": "178",
            "numeric_value": "(0,0.3333333333333333]",
            "blocks_support": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "AL847_2_target_consistency",
            "statement": "full-joint target b_mem=0.1124525903286696 corresponds to a_F DeltaR=0.3373577709860088 if eta=1",
            "status": "target_inside_corridor_not_prediction",
            "source": "178",
            "numeric_value": "0.3373577709860088",
            "blocks_support": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "AL847_3_missing_prediction",
            "statement": "eta, a_F, DeltaR, and endpoint dynamics are not parent-signed into a unique no-fit b_mem",
            "status": "prediction_missing",
            "source": "178",
            "numeric_value": "",
            "blocks_support": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def eligibility_rows(candidates: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    required_schema = {
        "candidate_id",
        "branch_class",
        "b_mem_mode",
        "b_mem_value_or_range",
        "shape_source",
        "parameter_count_delta",
        "claim_label",
    }
    for candidate in candidates:
        missing = [field for field in required_schema if not str(candidate.get(field, ""))]
        has_blocker = "BLOCKED" in str(candidate.get("b_mem_value_or_range", "")) or "MISSING" in str(candidate.get("eta_assumption", "")) or "MISSING" in str(candidate.get("a_F_DeltaR_assumption", ""))
        numeric_ok = False
        if candidate.get("b_mem_numeric"):
            try:
                numeric_ok = math.isfinite(float(str(candidate["b_mem_numeric"])))
            except ValueError:
                numeric_ok = False
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "schema_complete": str(not missing).lower(),
                "numeric_b_mem_available": str(numeric_ok).lower(),
                "contains_blocker_marker": str(has_blocker).lower(),
                "input_check_allowed": candidate["execution_eligible_for_input_check"],
                "scoring_allowed_after_user_go_ahead": candidate["execution_eligible_for_scoring"],
                "support_claim_allowed": candidate["support_claim_allowed"],
                "eligibility_status": "blocked_parent_prediction" if has_blocker else "eligible_for_nonclaim_dry_run_input_check",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG847_0_no_parent_prediction",
            "claim": "847 derives a parent-predicted b_mem",
            "status": "forbidden",
            "reason": "only a corridor and benchmark candidates are produced; the parent-predicted row remains blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG847_1_no_support_from_candidates",
            "claim": "candidate rows provide cosmology support",
            "status": "forbidden",
            "reason": "candidate rows only permit nonclaim input-check/scoring preparation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG847_2_no_full_joint_reuse_as_prediction",
            "claim": "full-joint best-fit b_mem is a predeclared prediction",
            "status": "forbidden",
            "reason": "full-joint b_mem is included only as demoted C0 benchmark/reference",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG847_3_allowed_candidate_file",
            "claim": "strict nonclaim candidate file exists for future input-check runner",
            "status": "allowed_private_nonclaim",
            "reason": "candidate file has numeric benchmark/corridor rows and explicit blocked parent-predicted row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D847_0",
            "finding": "strict candidate file created",
            "reason": "null, C0 benchmark, and parent-corridor probe rows now satisfy 846 schema for nonclaim input checks",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D847_1",
            "finding": "parent amplitude law still not predictive",
            "reason": "eta, a_F, DeltaR, and endpoint memory dynamics remain unsigned",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D847_2",
            "finding": "next step is runner/input-check, not scoring",
            "reason": "candidate file exists but no long fit is authorized and support claims remain forbidden",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "build a no-fit input-check runner that validates candidate rows against the 846 schema and writes run/log/status outputs",
            "include": "candidate CSV parser, schema validation, numeric b_mem checks, blocker handling, baseline matrix presence, dry-run-only status.json/log output",
            "exclude": "long scoring run, support claim, death claim, local-GR claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "created strict nonclaim candidate file with null, C0 benchmark, and parent-corridor probe rows",
            "parent_amplitude_status": "formal law and corridor survive; unique b_mem prediction still missing",
            "what_is_not_claimed": "new score, support, parent-predicted b_mem, C0 revival, local-GR progress",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    candidates: list[dict[str, object]],
    laws: list[dict[str, object]],
    eligibility: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_846_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    candidate_ids = {row["candidate_id"] for row in candidates}
    expected_candidates = {
        "S0_null_bmem_0",
        "S1_C0_CMB_reference",
        "S1_C0_full_joint_reference",
        "S2_corridor_eta1_aFDeltaR_0p1",
        "S2_corridor_eta1_aFDeltaR_0p3",
        "S2_corridor_eta1_aFDeltaR_1p0",
        "S3_parent_predicted_placeholder",
    }
    candidates_ok = candidate_ids == expected_candidates
    numeric_rows_ok = True
    for row in candidates:
        if row["execution_eligible_for_scoring"] == "true":
            try:
                numeric_rows_ok = numeric_rows_ok and math.isfinite(float(row["b_mem_numeric"]))
            except ValueError:
                numeric_rows_ok = False
    no_support = not any(row["support_claim_allowed"] == "true" for row in candidates)
    parent_blocked = any(row["candidate_id"] == "S3_parent_predicted_placeholder" and row["execution_eligible_for_scoring"] == "false" for row in candidates)
    law_nonprediction = any(row["law_id"] == "AL847_3_missing_prediction" and row["status"] == "prediction_missing" for row in laws)
    eligibility_ok = any(row["candidate_id"] == "S3_parent_predicted_placeholder" and row["eligibility_status"] == "blocked_parent_prediction" for row in eligibility)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    guard_ok = any(row["guard_id"] == "CG847_0_no_parent_prediction" and row["status"] == "forbidden" for row in guard_rows)
    nonclaim_ok = all_valid_for_claim_false([source_rows, candidates, laws, eligibility, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V847_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V847_1_prior_846_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V847_2_candidate_file_complete",
            "result": "pass" if candidates_ok else "fail",
            "detail": "null, C0 reference, corridor probes, and blocked parent-predicted rows present",
        },
        {
            "check_id": "V847_3_numeric_candidates_ready",
            "result": "pass" if numeric_rows_ok else "fail",
            "detail": "all scoring-eligible candidate rows have finite numeric b_mem",
        },
        {
            "check_id": "V847_4_no_support_claim_allowed",
            "result": "pass" if no_support and no_claim and guard_ok else "fail",
            "detail": "no candidate row permits support or parent prediction claim",
        },
        {
            "check_id": "V847_5_parent_prediction_blocked",
            "result": "pass" if parent_blocked and law_nonprediction and eligibility_ok else "fail",
            "detail": "parent-predicted row remains blocked because unique b_mem law is missing",
        },
        {
            "check_id": "V847_6_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V847_7_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V847_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V847_9_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    candidates: list[dict[str, object]],
    laws: list[dict[str, object]],
    eligibility: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 847 - Y5 R10 Strict Cosmology Candidate File Or Parent Amplitude Law",
        "",
        "Current result: **the strict candidate file now exists, but the parent amplitude law is still not predictive**. The file contains numeric null/control, C0 benchmark, and parent-corridor probe rows for future nonclaim input checks. The clean support-grade parent-predicted row remains blocked because `eta`, `a_F`, `DeltaR`, and endpoint dynamics are not signed into a unique no-fit `b_mem`.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "parent_amplitude_status", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Strict Cosmology Candidates",
        "",
        csv_table(candidates, ["candidate_id", "branch_class", "b_mem_mode", "b_mem_value_or_range", "b_mem_numeric", "eta_assumption", "a_F_DeltaR_assumption", "shape_source", "parameter_count_delta", "family_selection_penalty", "claim_label", "execution_eligible_for_input_check", "execution_eligible_for_scoring", "support_claim_allowed", "valid_for_claim"]),
        "",
        "## Parent Amplitude Law Status",
        "",
        csv_table(laws, ["law_id", "statement", "status", "source", "numeric_value", "blocks_support", "valid_for_claim"]),
        "",
        "## Execution Eligibility",
        "",
        csv_table(eligibility, ["candidate_id", "schema_complete", "numeric_b_mem_available", "contains_blocker_marker", "input_check_allowed", "scoring_allowed_after_user_go_ahead", "support_claim_allowed", "eligibility_status", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    candidates = candidate_rows(generated_utc)
    laws = amplitude_law_rows(generated_utc)
    eligibility = eligibility_rows(candidates, generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, candidates, laws, eligibility, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(
        CANDIDATE_PATH,
        candidates,
        [
            "candidate_id",
            "branch_class",
            "b_mem_mode",
            "b_mem_value_or_range",
            "b_mem_numeric",
            "eta_assumption",
            "a_F_DeltaR_assumption",
            "shape_source",
            "parameter_count_delta",
            "family_selection_penalty",
            "claim_label",
            "execution_eligible_for_input_check",
            "execution_eligible_for_scoring",
            "support_claim_allowed",
            "notes",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(AMPLITUDE_LAW_PATH, laws, ["law_id", "statement", "status", "source", "numeric_value", "blocks_support", "valid_for_claim", "generated_utc"])
    write_csv(ELIGIBILITY_PATH, eligibility, ["candidate_id", "schema_complete", "numeric_b_mem_available", "contains_blocker_marker", "input_check_allowed", "scoring_allowed_after_user_go_ahead", "support_claim_allowed", "eligibility_status", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "parent_amplitude_status", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, candidates, laws, eligibility, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={CANDIDATE_PATH}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
