from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "846-Y5-R10-strict-cosmology-branch-dry-run-spec.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_846_SOURCE_REGISTER.csv"
DRY_RUN_INPUTS_PATH = RESIDUALS / "P8_Y5_R10_846_DRY_RUN_INPUTS.csv"
CANDIDATE_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_846_CANDIDATE_BRANCH_SCHEMA.csv"
BASELINE_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_846_BASELINE_SYMMETRY_MATRIX.csv"
OUTPUT_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_846_OUTPUT_SCHEMA.csv"
COMMANDS_PATH = RESIDUALS / "P8_Y5_R10_846_DRY_RUN_COMMANDS.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_846_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_846_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_846_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_846_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_846_VALIDATION.csv"

STATUS = "Y5_R10_846_strict_cosmology_dry_run_spec_ready_nonclaim"
CLAIM_CEILING = "dry_run_spec_only_no_fit_no_support_claim"
NEXT_TARGET = "847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md"

SOURCE_SPECS = [
    {
        "source_id": "845_doc",
        "path": POST_CHECKPOINT / "845-Y5-R10-strict-MTS-cosmology-branch-contract.md",
        "needles": [
            "a stricter cosmology branch is now specified as a contract, not as a new fit",
            "strict_predeclared_parent_corridor",
            "846-Y5-R10-strict-cosmology-branch-dry-run-spec.md",
        ],
        "role": "strict branch contract handoff",
    },
    {
        "source_id": "845_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_845_VALIDATION.csv",
        "needles": [
            "V845_3_bmem_freedom_restricted,pass",
            "V845_6_no_support_claim_allowed,pass",
            "V845_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "cosmology_likelihood_smoke_script",
        "path": FORMALIZATION / "scripts" / "cosmology_likelihood_smoke.py",
        "needles": [],
        "role": "existing SN/BAO cosmology likelihood machinery",
    },
    {
        "source_id": "Hz_covariance_likelihood_script",
        "path": FORMALIZATION / "scripts" / "Hz_covariance_likelihood_smoke.py",
        "needles": [],
        "role": "existing H(z) covariance smoke machinery",
    },
    {
        "source_id": "full_joint_radflat_script",
        "path": FORMALIZATION / "scripts" / "full_joint_radflat_phenomenology_fit.py",
        "needles": [],
        "role": "existing full joint radflat fit machinery",
    },
    {
        "source_id": "joint_growth_CMB_radflat_script",
        "path": FORMALIZATION / "scripts" / "joint_growth_CMB_radflat_readout.py",
        "needles": [],
        "role": "existing growth/CMB radflat readout machinery",
    },
    {
        "source_id": "pantheon_plus_data",
        "path": FORMALIZATION / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES.dat",
        "needles": [],
        "role": "SN data availability check",
    },
    {
        "source_id": "desi_dr2_bao_mean",
        "path": FORMALIZATION / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt",
        "needles": [],
        "role": "BAO mean data availability check",
    },
    {
        "source_id": "Hz_data",
        "path": FORMALIZATION / "data" / "cosmology" / "cosmic_chronometers" / "Hz.csv",
        "needles": [],
        "role": "chronometer data availability check",
    },
    {
        "source_id": "growth_data",
        "path": FORMALIZATION / "data" / "cosmology" / "growth_CMB" / "sdss_eboss_dr16" / "BAO-plus" / "sdss_DR12_LRG_FSBAO_DMDHfs8.txt",
        "needles": [],
        "role": "growth/BAO-plus data availability check",
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
    if not path.exists():
        return "missing_path"
    if not needles:
        return "pass"
    text = read_text(path)
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


def dry_run_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "input_id": "IN846_0_contract",
            "input_type": "contract",
            "path": str(OUTPUT_DOC),
            "required_for": "dry-run interpretation",
            "exists_now": str(OUTPUT_DOC.exists()).lower(),
            "execution_status": "generated_by_this_checkpoint",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN846_1_candidate_file",
            "input_type": "candidate_branch_file",
            "path": str(RESIDUALS / "P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv"),
            "required_for": "actual dry-run execution",
            "exists_now": "false",
            "execution_status": "blocked_until_847_candidate_file_or_parent_amplitude_law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN846_2_SN_BAO_script",
            "input_type": "script",
            "path": str(FORMALIZATION / "scripts" / "cosmology_likelihood_smoke.py"),
            "required_for": "SN/BAO baseline parity",
            "exists_now": str((FORMALIZATION / "scripts" / "cosmology_likelihood_smoke.py").exists()).lower(),
            "execution_status": "available_reference_do_not_modify",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN846_3_Hz_script",
            "input_type": "script",
            "path": str(FORMALIZATION / "scripts" / "Hz_covariance_likelihood_smoke.py"),
            "required_for": "H(z) guardrail",
            "exists_now": str((FORMALIZATION / "scripts" / "Hz_covariance_likelihood_smoke.py").exists()).lower(),
            "execution_status": "available_reference_do_not_modify",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN846_4_growth_CMB_script",
            "input_type": "script",
            "path": str(FORMALIZATION / "scripts" / "joint_growth_CMB_radflat_readout.py"),
            "required_for": "growth/CMB guardrail",
            "exists_now": str((FORMALIZATION / "scripts" / "joint_growth_CMB_radflat_readout.py").exists()).lower(),
            "execution_status": "available_reference_do_not_modify",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def candidate_schema_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "field": "candidate_id",
            "required": "true",
            "allowed_values_or_rule": "unique stable identifier",
            "example": "S2_corridor_mid",
            "blocks_execution_if_missing": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "branch_class",
            "required": "true",
            "allowed_values_or_rule": "C0_benchmark|parent_predicted|predeclared_corridor|null_control",
            "example": "predeclared_corridor",
            "blocks_execution_if_missing": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "b_mem_mode",
            "required": "true",
            "allowed_values_or_rule": "fixed_parent|fixed_predeclared|corridor_predeclared|zero_control|benchmark_display_only",
            "example": "corridor_predeclared",
            "blocks_execution_if_missing": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "b_mem_value_or_range",
            "required": "true",
            "allowed_values_or_rule": "numeric fixed value or closed numeric range declared before scoring; no MISSING placeholders",
            "example": "[0.03,0.12]",
            "blocks_execution_if_missing": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "shape_source",
            "required": "true",
            "allowed_values_or_rule": "parent/equality-scale derivation path or predeclared benchmark source",
            "example": "178_parent_corridor",
            "blocks_execution_if_missing": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "parameter_count_delta",
            "required": "true",
            "allowed_values_or_rule": "integer penalty relative to baseline, including amplitude/shape freedom",
            "example": "1",
            "blocks_execution_if_missing": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "claim_label",
            "required": "true",
            "allowed_values_or_rule": "benchmark_only|exploratory_nonclaim|support_grade_candidate_blocked",
            "example": "exploratory_nonclaim",
            "blocks_execution_if_missing": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def baseline_matrix_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "arena": "SN_BAO_background",
            "required_baselines": "LambdaCDM,wCDM,CPL",
            "required_MTS_branches": "null_control,C0_benchmark,predeclared_corridor,parent_predicted_if_available",
            "symmetry_rule": "same nuisance offsets, covariance choice, calibration freedom, and AIC/BIC parameter counting",
            "pass_output": "delta_chi2_delta_AIC_delta_BIC_residuals_edge_flags",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena": "Hz_chronometer",
            "required_baselines": "M0_or_LambdaCDM,wCDM_if_available",
            "required_MTS_branches": "same candidate set as SN_BAO where formula is defined",
            "symmetry_rule": "same diagonal/covariance branch and same redshift windows",
            "pass_output": "delta_chi2_covariance_verdict_windowed_verdict",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena": "growth_CMB_radflat",
            "required_baselines": "LCDM_radflat,wCDM_or_best_available_growth_baseline",
            "required_MTS_branches": "C0_benchmark,predeclared_corridor,parent_predicted_if_available",
            "symmetry_rule": "same sigma8_0 refit rule and same compressed CMB distance-prior treatment",
            "pass_output": "growth_chi2_CMB_chi2_joint_AIC_BIC_parameter_penalties",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def output_schema_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "output_file": "runs/<timestamp>/log.txt",
            "purpose": "human-readable dry-run or future execution log",
            "required_fields": "start time, command, dry_run_only flag, source hashes/paths, warnings",
            "created_by_846": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "output_file": "runs/<timestamp>/status.json",
            "purpose": "machine-readable status for VS Code/phone handoff",
            "required_fields": "status, dry_run_only, candidate_file, all_inputs_present, claim_allowed=false",
            "created_by_846": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "output_file": "runs/<timestamp>/STRICT_BRANCH_SCORECARD.csv",
            "purpose": "future score table across candidates and baselines",
            "required_fields": "arena,candidate,baseline,chi2,AIC,BIC,delta_AIC,delta_BIC,edge_flag,claim_label",
            "created_by_846": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "output_file": "runs/<timestamp>/COMPLETE.marker",
            "purpose": "completion marker for long-run workflow",
            "required_fields": "plain marker only after dry-run/execution completes",
            "created_by_846": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def command_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "command_id": "CMD846_0_schema_only",
            "command": "python post-checkpoint-work\\scripts\\Y5_R10_strict_cosmology_branch_dry_run_spec.py",
            "mode": "schema_generation_only",
            "dry_run_only": "true",
            "long_fit_allowed": "false",
            "requires_847": "false",
            "expected_runtime": "seconds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "command_id": "CMD846_1_future_input_check",
            "command": "python post-checkpoint-work\\scripts\\strict_cosmology_branch_runner.py --candidates source-intake\\mts_residuals\\P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv --dry-run --no-fit",
            "mode": "future_candidate_input_check",
            "dry_run_only": "true",
            "long_fit_allowed": "false",
            "requires_847": "true",
            "expected_runtime": "seconds_to_minutes",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "command_id": "CMD846_2_future_scoring_run",
            "command": "python post-checkpoint-work\\scripts\\strict_cosmology_branch_runner.py --candidates source-intake\\mts_residuals\\P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv --run-score --write-run-dir",
            "mode": "future_explicit_execution_only",
            "dry_run_only": "false",
            "long_fit_allowed": "only_after_user_go_ahead",
            "requires_847": "true",
            "expected_runtime": "unknown_may_be_long",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG846_0_no_fit",
            "claim": "846 runs or scores cosmology models",
            "status": "forbidden",
            "reason": "846 is only a dry-run specification and schema checkpoint",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG846_1_no_candidate_ready",
            "claim": "strict branch is ready for execution now",
            "status": "forbidden",
            "reason": "candidate file and parent amplitude law/range are deferred to 847",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG846_2_no_support",
            "claim": "dry-run setup permits support language",
            "status": "forbidden",
            "reason": "all dry-run outputs must keep claim_allowed=false until data and parent-amplitude gates pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG846_3_allowed_spec",
            "claim": "future strict cosmology run now has an input/output dry-run specification",
            "status": "allowed_private_nonclaim",
            "reason": "this is an execution discipline artifact, not evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D846_0",
            "finding": "dry-run spec is ready",
            "reason": "candidate schema, baseline matrix, output schema, and command modes are defined",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D846_1",
            "finding": "actual execution remains blocked",
            "reason": "847 must provide a candidate file or parent amplitude law before any strict branch input check",
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
            "objective": "create the strict candidate file or derive/fix the parent amplitude law before any scoring run",
            "include": "candidate rows, numeric b_mem fixed/range values, shape source, parameter penalties, claim labels, execution eligibility",
            "exclude": "long fit, support claim, death claim, local-GR claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "future strict cosmology run now has dry-run input, candidate, baseline, output, and command schemas",
            "what_blocks_execution": "missing 847 candidate file or parent amplitude law/range",
            "what_is_not_claimed": "new score, model support, branch death, local-GR progress, candidate execution readiness",
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
    input_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    baseline_rows: list[dict[str, object]],
    output_rows: list[dict[str, object]],
    command_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_845_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    available_inputs_ok = all(row["exists_now"] == "true" for row in input_rows if row["execution_status"] == "available_reference_do_not_modify")
    candidate_schema_ok = all(row["required"] == "true" and row["blocks_execution_if_missing"] == "true" for row in candidate_rows)
    baseline_ok = {row["arena"] for row in baseline_rows} == {"SN_BAO_background", "Hz_chronometer", "growth_CMB_radflat"}
    output_ok = {row["output_file"] for row in output_rows} == {
        "runs/<timestamp>/log.txt",
        "runs/<timestamp>/status.json",
        "runs/<timestamp>/STRICT_BRANCH_SCORECARD.csv",
        "runs/<timestamp>/COMPLETE.marker",
    }
    no_long_run = all(row["long_fit_allowed"] in {"false", "only_after_user_go_ahead"} for row in command_rows_)
    blocked_now = any(row["input_id"] == "IN846_1_candidate_file" and row["execution_status"].startswith("blocked") for row in input_rows)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    guard_blocks = any(row["guard_id"] == "CG846_1_no_candidate_ready" and row["status"] == "forbidden" for row in guard_rows)
    nonclaim_ok = all_valid_for_claim_false([source_rows, input_rows, candidate_rows, baseline_rows, output_rows, command_rows_, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V846_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V846_1_prior_845_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V846_2_reference_inputs_exist",
            "result": "pass" if available_inputs_ok else "fail",
            "detail": "referenced formalization scripts/data exist",
        },
        {
            "check_id": "V846_3_candidate_schema_blocks_missing_values",
            "result": "pass" if candidate_schema_ok else "fail",
            "detail": "candidate schema requires predeclared numeric amplitude/source/penalty fields",
        },
        {
            "check_id": "V846_4_baseline_matrix_complete",
            "result": "pass" if baseline_ok else "fail",
            "detail": "SN/BAO, H(z), and growth/CMB arenas included",
        },
        {
            "check_id": "V846_5_output_schema_complete",
            "result": "pass" if output_ok else "fail",
            "detail": "log, status, scorecard, and completion marker schemas included",
        },
        {
            "check_id": "V846_6_no_long_run_authorized",
            "result": "pass" if no_long_run and blocked_now else "fail",
            "detail": "future scoring is blocked until 847 and long run requires explicit go-ahead",
        },
        {
            "check_id": "V846_7_no_claims",
            "result": "pass" if no_claim and guard_blocks else "fail",
            "detail": "candidate readiness and support claims forbidden",
        },
        {
            "check_id": "V846_8_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V846_9_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V846_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V846_11_validation_rows_ready",
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
    input_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    baseline_rows: list[dict[str, object]],
    output_rows: list[dict[str, object]],
    command_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 846 - Y5 R10 Strict Cosmology Branch Dry-Run Spec",
        "",
        "Current result: **the strict cosmology branch now has a dry-run specification, but it is not ready for scoring**. Execution is blocked until `847` supplies a candidate file or a parent amplitude law/range with numeric `b_mem`, shape source, and parameter-penalty fields. No long fit is authorized here.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_blocks_execution", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Dry-Run Inputs",
        "",
        csv_table(input_rows, ["input_id", "input_type", "path", "required_for", "exists_now", "execution_status", "valid_for_claim"]),
        "",
        "## Candidate Branch Schema",
        "",
        csv_table(candidate_rows, ["field", "required", "allowed_values_or_rule", "example", "blocks_execution_if_missing", "valid_for_claim"]),
        "",
        "## Baseline Symmetry Matrix",
        "",
        csv_table(baseline_rows, ["arena", "required_baselines", "required_MTS_branches", "symmetry_rule", "pass_output", "valid_for_claim"]),
        "",
        "## Output Schema",
        "",
        csv_table(output_rows, ["output_file", "purpose", "required_fields", "created_by_846", "valid_for_claim"]),
        "",
        "## Dry-Run Commands",
        "",
        csv_table(command_rows_, ["command_id", "command", "mode", "dry_run_only", "long_fit_allowed", "requires_847", "expected_runtime", "valid_for_claim"]),
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
    input_rows = dry_run_input_rows(generated_utc)
    candidate_rows = candidate_schema_rows(generated_utc)
    baseline_rows = baseline_matrix_rows(generated_utc)
    output_rows = output_schema_rows(generated_utc)
    command_rows_ = command_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, input_rows, candidate_rows, baseline_rows, output_rows, command_rows_, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(DRY_RUN_INPUTS_PATH, input_rows, ["input_id", "input_type", "path", "required_for", "exists_now", "execution_status", "valid_for_claim", "generated_utc"])
    write_csv(CANDIDATE_SCHEMA_PATH, candidate_rows, ["field", "required", "allowed_values_or_rule", "example", "blocks_execution_if_missing", "valid_for_claim", "generated_utc"])
    write_csv(BASELINE_MATRIX_PATH, baseline_rows, ["arena", "required_baselines", "required_MTS_branches", "symmetry_rule", "pass_output", "valid_for_claim", "generated_utc"])
    write_csv(OUTPUT_SCHEMA_PATH, output_rows, ["output_file", "purpose", "required_fields", "created_by_846", "valid_for_claim", "generated_utc"])
    write_csv(COMMANDS_PATH, command_rows_, ["command_id", "command", "mode", "dry_run_only", "long_fit_allowed", "requires_847", "expected_runtime", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_blocks_execution", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, input_rows, candidate_rows, baseline_rows, output_rows, command_rows_, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
