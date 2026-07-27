from __future__ import annotations

import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"

OUTPUT_DOC = POST_CHECKPOINT / "849-Y5-R10-strict-cosmology-scoring-adapter-or-parent-amplitude-tightening.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_849_SOURCE_REGISTER.csv"
ROUTE_SELECTION_PATH = RESIDUALS / "P8_Y5_R10_849_ROUTE_SELECTION.csv"
PARENT_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_849_PARENT_AMPLITUDE_TIGHTENING_AUDIT.csv"
ADAPTER_RESULT_PATH = RESIDUALS / "P8_Y5_R10_849_ADAPTER_DRY_RUN_RESULT.csv"
COMMAND_PLAN_PATH = RESIDUALS / "P8_Y5_R10_849_COMMAND_PLAN.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_849_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_849_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_849_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_849_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_849_VALIDATION.csv"

CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv"
ADAPTER_PATH = POST_CHECKPOINT / "scripts" / "strict_cosmology_scoring_adapter.py"

STATUS = "Y5_R10_849_scoring_adapter_dry_run_ready_parent_amplitude_still_open_nonclaim"
CLAIM_CEILING = "adapter_dry_run_only_no_score_no_support_no_parent_prediction"
NEXT_TARGET = "850-Y5-R10-fixed-bmem-cosmology-score-evaluator-dry-run.md"

SOURCE_SPECS = [
    {
        "source_id": "848_doc",
        "path": POST_CHECKPOINT / "848-Y5-R10-strict-cosmology-input-check-runner.md",
        "needles": [
            "strict cosmology candidate file passes the no-fit input-check runner",
            "849-Y5-R10-strict-cosmology-scoring-adapter-or-parent-amplitude-tightening.md",
        ],
        "role": "input-check handoff",
    },
    {
        "source_id": "848_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_848_VALIDATION.csv",
        "needles": [
            "V848_2_input_check_passed_no_fit,pass",
            "V848_5_parent_placeholder_blocked,pass",
            "V848_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "847_candidates",
        "path": CANDIDATE_PATH,
        "needles": [
            "S0_null_bmem_0",
            "S2_corridor_eta1_aFDeltaR_1p0",
            "S3_parent_predicted_placeholder",
        ],
        "role": "strict fixed-bmem candidate inputs",
    },
    {
        "source_id": "177_parent_amplitude_contract",
        "path": FORMALIZATION / "177-parent-amplitude-repair-contract.md",
        "needles": [
            "derive the amplitude before fitting it",
            "eta = H0 L_cg / c",
            "a_F sign and scale",
        ],
        "role": "parent amplitude theorem obligations",
    },
    {
        "source_id": "178_parent_amplitude_attempt",
        "path": FORMALIZATION / "178-parent-amplitude-theorem-attempt.md",
        "needles": [
            "only a corridor derives",
            "amplitude prediction derived = false",
            "unique no-fit b_mem prediction",
        ],
        "role": "parent corridor and nonprediction source",
    },
    {
        "source_id": "849_adapter_script",
        "path": ADAPTER_PATH,
        "needles": [
            "Dry-run strict cosmology scoring adapter planner.",
            "STRICT_COSMOLOGY_COMMAND_PLAN.csv",
            "fit_executed",
            "claim_allowed",
        ],
        "role": "new no-fit adapter planner",
    },
    {
        "source_id": "SN_BAO_script",
        "path": FORMALIZATION / "scripts" / "cosmology_likelihood_smoke.py",
        "needles": ["--robustness-matrix", "--transition-gate", "M6"],
        "role": "existing SN/BAO likelihood machinery",
    },
    {
        "source_id": "Hz_script",
        "path": FORMALIZATION / "scripts" / "Hz_covariance_likelihood_smoke.py",
        "needles": ["Row-locked 15-point cosmic-chronometer covariance", "M6_min_edge_free_shape"],
        "role": "existing H(z) covariance machinery",
    },
    {
        "source_id": "growth_CMB_script",
        "path": FORMALIZATION / "scripts" / "joint_growth_CMB_radflat_readout.py",
        "needles": ["Combine the radflat calibrated CMB branch with the growth holdout", "growth_fsigma8_radflat"],
        "role": "existing growth/CMB readout machinery",
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


def run_adapter() -> tuple[Path, dict[str, object], str]:
    command = [
        "python",
        str(ADAPTER_PATH),
        "--candidates",
        str(CANDIDATE_PATH),
        "--dry-run",
        "--no-fit",
        "--write-run-dir",
        "--output-root",
        str(RUNS),
    ]
    completed = subprocess.run(
        command,
        cwd=str(POST_CHECKPOINT),
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    run_dir_text = ""
    for line in completed.stdout.splitlines():
        if line.startswith("run_dir="):
            run_dir_text = line.split("=", 1)[1].strip()
            break
    if not run_dir_text:
        raise RuntimeError("adapter did not print run_dir")
    run_dir = Path(run_dir_text)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    return run_dir, status, completed.stdout


def route_selection_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "R849_0_selected",
            "selected_route": "adapter_dry_run_plus_parent_amplitude_tightening_audit",
            "reason": "testing pressure is real, but support-grade cosmology still needs a no-fit parent amplitude or explicitly nonclaim fixed-bmem score",
            "route_status": "selected_private_nonclaim",
            "what_this_does": "maps candidates to existing cosmology arenas and records the remaining adapter gaps",
            "what_this_does_not_do": "derive eta/a_F/DeltaR or run a long score",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "R849_1_rejected",
            "selected_route": "declare_parent_amplitude_solved",
            "reason": "178 only gives a corridor, not a unique b_mem prediction",
            "route_status": "rejected",
            "what_this_does": "none",
            "what_this_does_not_do": "cannot support C0 or M6 as parent-predicted",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PA849_0_corridor_identity",
            "quantity": "b_mem = Omega_Gamma,inf - Omega_Gamma0 = integral S_Gamma dN = a_F DeltaR/(3 eta^2)",
            "status": "survives_as_formal_identity",
            "current_bound_or_value": "0<b_mem<=1/3 if eta=1 and 0<a_F DeltaR<=1",
            "missing_for_prediction": "none for corridor; unique value still missing",
            "next_action": "use as nonclaim corridor only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PA849_1_eta_law",
            "quantity": "eta = H0 L_cg/c",
            "status": "open",
            "current_bound_or_value": "eta=1 used only as horizon-scale probe",
            "missing_for_prediction": "derive L_cg from parent/local transition geometry without cosmology fit input",
            "next_action": "attempt eta theorem or keep eta as explicit corridor coordinate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PA849_2_aF_law",
            "quantity": "a_F",
            "status": "open",
            "current_bound_or_value": "order-one positive corridor assumed, not derived",
            "missing_for_prediction": "derive sign and normalization from trace coupling/current projection",
            "next_action": "connect a_F to the coupling sector before support language",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PA849_3_DeltaR_law",
            "quantity": "DeltaR",
            "status": "open",
            "current_bound_or_value": "endpoint difference required but not computed from dynamics",
            "missing_for_prediction": "derive endpoint ordering and magnitude from memory evolution",
            "next_action": "write the endpoint evolution equation or demote to fitted amplitude",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PA849_4_conservation",
            "quantity": "covariant conservation/Bianchi compatibility",
            "status": "open_guardrail",
            "current_bound_or_value": "must remain compatible with strict baseline parity",
            "missing_for_prediction": "show source-memory projection does not create an unbalanced stress-energy leakage",
            "next_action": "test residual form in fixed-bmem evaluator without calling it proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PA849_5_target_inside_corridor",
            "quantity": "full-joint reference b_mem=0.1124525903286696",
            "status": "inside_corridor_not_prediction",
            "current_bound_or_value": "a_F DeltaR=0.3373577709860088 if eta=1",
            "missing_for_prediction": "derive why this value, not merely that it is plausible",
            "next_action": "score fixed candidates as probes only or derive parent amplitude",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def adapter_result_rows(run_dir: Path, status: dict[str, object], stdout: str, generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "run_id": run_dir.name,
            "run_dir": str(run_dir),
            "status": status.get("status"),
            "dry_run_only": str(status.get("dry_run_only")).lower(),
            "no_fit": str(status.get("no_fit")).lower(),
            "fit_executed": str(status.get("fit_executed")).lower(),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "candidate_count": status.get("candidate_count"),
            "arena_count": status.get("arena_count"),
            "command_plan_row_count": status.get("command_plan_row_count"),
            "blocked_plan_row_count": status.get("blocked_plan_row_count"),
            "run_authorized_row_count": status.get("run_authorized_row_count"),
            "missing_reference_count": status.get("missing_reference_count"),
            "runner_stdout": stdout.replace("\n", " | "),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def command_plan_rows(run_dir: Path, generated_utc: str) -> list[dict[str, object]]:
    plan_path = run_dir / "STRICT_COSMOLOGY_COMMAND_PLAN.csv"
    rows: list[dict[str, object]] = []
    with plan_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append({**row, "generated_utc": generated_utc})
    return rows


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG849_0_no_score",
            "claim": "849 scored cosmology candidates",
            "status": "forbidden",
            "reason": "adapter is dry-run/no-fit only and every command-plan row has run_authorized=false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG849_1_no_parent_prediction",
            "claim": "parent amplitude b_mem is derived",
            "status": "forbidden",
            "reason": "eta, a_F, DeltaR, endpoint dynamics, and conservation compatibility remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG849_2_no_support_language",
            "claim": "fixed-bmem candidates support MTS cosmology",
            "status": "forbidden",
            "reason": "no score has run; even future scores remain nonclaim until parent/source gates close",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG849_3_allowed_progress",
            "claim": "strict scoring adapter gaps are now explicit",
            "status": "allowed_private_nonclaim",
            "reason": "the command plan identifies what must be wrapped before real fixed-bmem scoring",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D849_0",
            "finding": "best route is testing-prep without claim escalation",
            "reason": "the candidate rows are clean enough for adapter planning, but parent amplitude is still only a corridor",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D849_1",
            "finding": "existing cosmology scripts are reference machinery, not yet strict fixed-bmem scorers",
            "reason": "candidate b_mem injection, fixed-parameter penalties, and arena-specific outputs need a post-checkpoint wrapper/evaluator",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D849_2",
            "finding": "parent amplitude tightening remains open",
            "reason": "eta, a_F, and DeltaR are the missing coupling/amplitude locks",
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
            "objective": "build a fixed-b_mem score evaluator dry-run that can score strict candidates against baselines without fitting b_mem",
            "include": "SN/BAO first, same baselines, fixed candidate b_mem injection, AIC/BIC parameter accounting, no support claim",
            "exclude": "long execution without explicit user go-ahead, C0 revival, parent-amplitude proof by fit, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(run_result: dict[str, object], generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "added a no-fit scoring-adapter planner and parent-amplitude tightening audit",
            "adapter_status": run_result.get("status"),
            "parent_amplitude_status": "corridor_survives_but_unique_prediction_missing",
            "what_is_not_claimed": "new cosmology score, support, parent-predicted b_mem, local-GR progress, public evidence",
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
    route_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    run_rows: list[dict[str, object]],
    plan_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_848_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    route_ok = bool(route_rows) and route_rows[0]["selected_route"] == "adapter_dry_run_plus_parent_amplitude_tightening_audit"
    parent_open = all(row["valid_for_claim"] == "false" for row in parent_rows) and any(row["gate_id"] == "PA849_1_eta_law" and row["status"] == "open" for row in parent_rows)
    adapter_ok = bool(run_rows) and run_rows[0]["status"] == "adapter_dry_run_passed_blocked_for_scoring" and run_rows[0]["fit_executed"] == "false"
    no_authorized = all(row["run_authorized"] == "false" for row in plan_rows)
    plan_complete = len(plan_rows) == 28 and len({row["arena"] for row in plan_rows}) == 4 and len({row["candidate_id"] for row in plan_rows}) == 7
    parent_placeholder_blocked = any(row["candidate_id"] == "S3_parent_predicted_placeholder" and row["adapter_status"] == "blocked_candidate_or_parent_prediction" for row in plan_rows)
    missing_refs = bool(run_rows) and str(run_rows[0]["missing_reference_count"]) == "0"
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions) and bool(run_rows) and run_rows[0]["claim_allowed"] == "false"
    nonclaim_ok = all_valid_for_claim_false([source_rows, route_rows, parent_rows, run_rows, plan_rows, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V849_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V849_1_prior_848_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V849_2_route_selected",
            "result": "pass" if route_ok else "fail",
            "detail": "adapter dry-run plus amplitude audit route selected",
        },
        {
            "check_id": "V849_3_parent_amplitude_still_open",
            "result": "pass" if parent_open else "fail",
            "detail": "eta/a_F/DeltaR remain open; no parent prediction claimed",
        },
        {
            "check_id": "V849_4_adapter_dry_run_passed_no_fit",
            "result": "pass" if adapter_ok else "fail",
            "detail": "adapter status passed with fit_executed=false",
        },
        {
            "check_id": "V849_5_command_plan_complete",
            "result": "pass" if plan_complete else "fail",
            "detail": "7 candidates x 4 arenas command plan present",
        },
        {
            "check_id": "V849_6_no_run_authorized",
            "result": "pass" if no_authorized else "fail",
            "detail": "all command-plan rows keep run_authorized=false",
        },
        {
            "check_id": "V849_7_parent_placeholder_blocked",
            "result": "pass" if parent_placeholder_blocked else "fail",
            "detail": "S3 parent-predicted placeholder remains blocked",
        },
        {
            "check_id": "V849_8_references_present",
            "result": "pass" if missing_refs else "fail",
            "detail": "adapter dry-run found all referenced scripts",
        },
        {
            "check_id": "V849_9_claim_allowed_false",
            "result": "pass" if no_claim else "fail",
            "detail": "runner and decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V849_10_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V849_11_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V849_12_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V849_13_validation_rows_ready",
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
    route_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    run_rows: list[dict[str, object]],
    plan_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    compact_plan_rows = [
        {
            "candidate_id": row["candidate_id"],
            "arena": row["arena"],
            "adapter_status": row["adapter_status"],
            "blocker": row["blocker"],
            "run_authorized": row["run_authorized"],
            "valid_for_claim": row["valid_for_claim"],
        }
        for row in plan_rows
    ]
    sections = [
        "# 849 - Y5 R10 Strict Cosmology Scoring Adapter Or Parent Amplitude Tightening",
        "",
        "Current result: **the strict cosmology branch now has a no-fit scoring-adapter dry run and a refreshed parent-amplitude audit**. The adapter maps the seven 847 candidates across four cosmology arenas, but every plan row remains `run_authorized=false`, `fit_executed=false`, and `claim_allowed=false`. The parent amplitude still has only a corridor, not a unique no-fit prediction.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "adapter_status", "parent_amplitude_status", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Route Selection",
        "",
        csv_table(route_rows, ["route_id", "selected_route", "reason", "route_status", "what_this_does", "what_this_does_not_do", "valid_for_claim"]),
        "",
        "## Parent Amplitude Tightening Audit",
        "",
        csv_table(parent_rows, ["gate_id", "quantity", "status", "current_bound_or_value", "missing_for_prediction", "next_action", "valid_for_claim"]),
        "",
        "## Adapter Dry-Run Result",
        "",
        csv_table(run_rows, ["run_id", "run_dir", "status", "dry_run_only", "no_fit", "fit_executed", "claim_allowed", "candidate_count", "arena_count", "command_plan_row_count", "blocked_plan_row_count", "run_authorized_row_count", "missing_reference_count", "valid_for_claim"]),
        "",
        "## Command Plan",
        "",
        csv_table(compact_plan_rows, ["candidate_id", "arena", "adapter_status", "blocker", "run_authorized", "valid_for_claim"]),
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
    route_rows = route_selection_rows(generated_utc)
    parent_rows = parent_audit_rows(generated_utc)
    run_dir, status, stdout = run_adapter()
    run_rows = adapter_result_rows(run_dir, status, stdout, generated_utc)
    plan_rows = command_plan_rows(run_dir, generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(run_rows[0], generated_utc)
    validation = validation_rows(source_rows, route_rows, parent_rows, run_rows, plan_rows, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_SELECTION_PATH, route_rows, ["route_id", "selected_route", "reason", "route_status", "what_this_does", "what_this_does_not_do", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_AUDIT_PATH, parent_rows, ["gate_id", "quantity", "status", "current_bound_or_value", "missing_for_prediction", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(ADAPTER_RESULT_PATH, run_rows, ["run_id", "run_dir", "status", "dry_run_only", "no_fit", "fit_executed", "claim_allowed", "candidate_count", "arena_count", "command_plan_row_count", "blocked_plan_row_count", "run_authorized_row_count", "missing_reference_count", "runner_stdout", "valid_for_claim", "generated_utc"])
    write_csv(COMMAND_PLAN_PATH, plan_rows, ["candidate_id", "branch_class", "claim_label", "b_mem_numeric", "arena", "reference_script", "reference_exists", "baseline_parity", "reference_command", "adapter_status", "blocker", "needed_adapter_change", "run_authorized", "fit_executed", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "adapter_status", "parent_amplitude_status", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, route_rows, parent_rows, run_rows, plan_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"run_dir={run_dir}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
