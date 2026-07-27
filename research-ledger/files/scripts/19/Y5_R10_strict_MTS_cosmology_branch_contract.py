from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "845-Y5-R10-strict-MTS-cosmology-branch-contract.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_845_SOURCE_REGISTER.csv"
STRICT_BRANCH_PATH = RESIDUALS / "P8_Y5_R10_845_STRICT_BRANCH_CONTRACT.csv"
PARAMETER_FREEDOM_PATH = RESIDUALS / "P8_Y5_R10_845_PARAMETER_FREEDOM_LEDGER.csv"
TEST_GATE_PATH = RESIDUALS / "P8_Y5_R10_845_STRICT_TEST_GATE.csv"
OUTCOME_RULE_PATH = RESIDUALS / "P8_Y5_R10_845_OUTCOME_LANGUAGE_RULES.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_845_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_845_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_845_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_845_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_845_VALIDATION.csv"

STATUS = "Y5_R10_845_strict_cosmology_branch_contract_locked_nonclaim"
CLAIM_CEILING = "strict_branch_contract_only_no_new_fit_no_support_claim"
NEXT_TARGET = "846-Y5-R10-strict-cosmology-branch-dry-run-spec.md"

SOURCE_SPECS = [
    {
        "source_id": "844_doc",
        "path": POST_CHECKPOINT / "844-Y5-R10-cosmology-evidence-readout-pack.md",
        "needles": [
            "cosmology is alive as a constraint/clue, not as support",
            "C0 is closure benchmark only",
            "strict cosmology branch is required",
            "845-Y5-R10-strict-MTS-cosmology-branch-contract.md",
        ],
        "role": "latest cosmology evidence ledger and strict-branch handoff",
    },
    {
        "source_id": "844_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_844_VALIDATION.csv",
        "needles": [
            "V844_2_latest_cosmology_status_included,pass",
            "V844_6_support_and_death_claims_blocked,pass",
            "V844_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "175_full_joint_radflat_fit",
        "path": FORMALIZATION / "175-full-joint-radflat-phenomenology-fit.md",
        "needles": [
            "C0 frozen is near-competitive by AIC;",
            "b_mem positive-and-stable gate.",
            "no support claim is allowed;",
            "the amplitude moves too much when growth is allowed into the fit;",
        ],
        "role": "full joint radflat fit motivating stricter amplitude discipline",
    },
    {
        "source_id": "176_C0_demotion_decision",
        "path": FORMALIZATION / "176-C0-radflat-demotion-decision.md",
        "needles": [
            "C0_demoted_to_closure_benchmark_parent_amplitude_repair_required",
            "C0_frozen_delta_AIC_vs_best_baseline = 0.36437287900487547",
            "C0_b_mem_fractional_shift = 6.148693776912986",
            "C0 = closure-only benchmark until a parent amplitude contract succeeds.",
        ],
        "role": "C0 closure-benchmark decision",
    },
    {
        "source_id": "177_parent_amplitude_repair_contract",
        "path": FORMALIZATION / "177-parent-amplitude-repair-contract.md",
        "needles": [
            "parent_amplitude_repair_contract_locked_not_satisfied",
            "b_mem = a_F DeltaR / [3 eta^2]",
            "derive the amplitude before fitting it.",
            "do not use the growth/CMB best-fit amplitude as proof;",
        ],
        "role": "parent amplitude repair contract",
    },
    {
        "source_id": "178_parent_amplitude_theorem_attempt",
        "path": FORMALIZATION / "178-parent-amplitude-theorem-attempt.md",
        "needles": [
            "parent_amplitude_theorem_partial_corridor_not_prediction",
            "amplitude corridor derived = true",
            "amplitude prediction derived = false",
            "More C0 fitting would now be rescue-fitting unless a stricter branch is defined.",
        ],
        "role": "latest parent-amplitude theorem attempt",
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


def strict_branch_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "SB845_0_C0_archive",
            "branch_name": "C0_closure_benchmark",
            "purpose": "retain the old C0/radflat shape as a benchmark and diagnostic only",
            "amplitude_rule": "may display fitted b_mem values, but they do not count as predictions or support",
            "free_amplitude_status": "benchmark_only",
            "allowed_use": "pipeline regression, sanity checks, residual anatomy comparison",
            "forbidden_use": "support claim, public evidence pillar, parent amplitude proof",
            "support_claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "SB845_1_parent_predicted",
            "branch_name": "strict_parent_predicted_amplitude",
            "purpose": "the clean route: b_mem fixed before data by a parent amplitude theorem",
            "amplitude_rule": "b_mem = a_F DeltaR / [3 eta^2] or equivalent must be parent-derived with signed inputs",
            "free_amplitude_status": "blocked_until_theorem",
            "allowed_use": "future support-grade branch only after the amplitude prediction is derived",
            "forbidden_use": "running as if b_mem were already predicted",
            "support_claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "SB845_2_predeclared_corridor",
            "branch_name": "strict_predeclared_parent_corridor",
            "purpose": "exploratory route using the derived parent amplitude corridor without treating it as a prediction",
            "amplitude_rule": "b_mem prior/range must be declared before looking at new scores and must not be set by the full-joint best fit",
            "free_amplitude_status": "exploratory_nonclaim",
            "allowed_use": "holdout stress test and branch pruning",
            "forbidden_use": "support claim unless upgraded to parent-predicted amplitude",
            "support_claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "SB845_3_null_control",
            "branch_name": "strict_null_control",
            "purpose": "verify the same pipeline can recover fitted baseline behaviour and reject artificial improvements",
            "amplitude_rule": "b_mem=0 or baseline-equivalent limit",
            "free_amplitude_status": "control",
            "allowed_use": "pipeline and model-selection sanity check",
            "forbidden_use": "MTS support or demotion claim",
            "support_claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parameter_freedom_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "parameter": "F(z)_shape",
            "role": "memory/activation shape",
            "allowed_mode": "fixed_or_predeclared",
            "source_rule": "must come from parent/equality-scale argument or predeclared shape family before scoring",
            "counts_in_AIC_BIC": "true_if_selected_from_family_or_tuned",
            "support_allowed_if_free": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "parameter": "b_mem",
            "role": "memory amplitude",
            "allowed_mode": "parent_predicted_or_predeclared_corridor",
            "source_rule": "parent-predicted for support; predeclared corridor only for exploratory pruning",
            "counts_in_AIC_BIC": "true_if_fitted_or_corridor_selected_after_data",
            "support_allowed_if_free": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "parameter": "z50_act_width_act",
            "role": "transition location/width if used",
            "allowed_mode": "fixed_by_physics_or_counted",
            "source_rule": "must not be edge-seeking or retuned per dataset without parameter penalty",
            "counts_in_AIC_BIC": "true_if_fitted",
            "support_allowed_if_free": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "parameter": "Omega_m0_H0_calibration",
            "role": "background calibration/nuisance",
            "allowed_mode": "same_freedom_as_baselines",
            "source_rule": "MTS and fitted baselines must receive symmetric calibration treatment",
            "counts_in_AIC_BIC": "true_if_fitted",
            "support_allowed_if_free": "only_if_baseline_symmetric_and_other_gates_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "parameter": "sigma8_0",
            "role": "growth nuisance",
            "allowed_mode": "analytic_refit_allowed_if_baselines_same",
            "source_rule": "count as fitted parameter and apply equally to baselines",
            "counts_in_AIC_BIC": "true",
            "support_allowed_if_free": "only_if_baseline_symmetric_and_other_gates_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "parameter": "local_GR_closure",
            "role": "local theory guardrail",
            "allowed_mode": "external_closure_only",
            "source_rule": "cosmology scoring cannot improve or prove local GR status",
            "counts_in_AIC_BIC": "not_applicable",
            "support_allowed_if_free": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def test_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "TG845_0_no_rescue_fit",
            "gate": "no C0 rescue-fitting",
            "pass_condition": "b_mem/shape freedoms are fixed or predeclared before scoring and not chosen from the previous full-joint optimum",
            "failure_consequence": "branch remains closure benchmark only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TG845_1_same_baselines",
            "gate": "same baseline treatment",
            "pass_condition": "LambdaCDM, wCDM, CPL, and MTS receive symmetric nuisance/calibration/covariance treatment",
            "failure_consequence": "readout is pipeline diagnostic, not evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TG845_2_multi_arena_holdout",
            "gate": "multi-arena holdout",
            "pass_condition": "candidate survives SN/BAO, H(z), growth, and compressed CMB gates without relying on one fragile arena",
            "failure_consequence": "label as sector clue or demote to phenomenology",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TG845_3_model_selection",
            "gate": "fair AIC/BIC and residual anatomy",
            "pass_condition": "all fitted freedoms counted and residual anatomy matches the proposed mechanism",
            "failure_consequence": "near-tie language only, no support claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TG845_4_parent_upgrade",
            "gate": "parent-amplitude upgrade",
            "pass_condition": "amplitude corridor becomes a no-fit parent prediction with signed inputs",
            "failure_consequence": "strict branch remains exploratory even if numerically close",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TG845_5_local_gr_firewall",
            "gate": "local GR firewall",
            "pass_condition": "cosmology result does not alter local transition closure-only status",
            "failure_consequence": "interpretation blocked until local closure conflict is resolved",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def outcome_rule_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "outcome_id": "OR845_0_support_grade",
            "condition": "parent-predicted b_mem plus robust multi-arena improvement over fitted baselines",
            "allowed_language": "support-grade empirical clue",
            "forbidden_language": "fundamental theory confirmed or local GR derived",
            "current_status": "not_available",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "outcome_id": "OR845_1_near_competitive",
            "condition": "AIC/BIC near tie or small loss with no edge flag but no parent prediction",
            "allowed_language": "alive as constraint/clue; closure benchmark remains useful",
            "forbidden_language": "evidence pillar",
            "current_status": "current_C0_zone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "outcome_id": "OR845_2_arena_specific",
            "condition": "works in one arena but fails H(z), growth, CMB, or BAO holdout",
            "allowed_language": "sector-specific phenomenology",
            "forbidden_language": "cosmology branch survives",
            "current_status": "possible",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "outcome_id": "OR845_3_failure",
            "condition": "fails symmetric baselines across multiple arenas",
            "allowed_language": "strict branch demoted",
            "forbidden_language": "MTS cosmology is dead",
            "current_status": "future_possible",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG845_0_no_new_fit_claim",
            "claim": "845 provides new cosmology evidence",
            "status": "forbidden",
            "reason": "845 is a contract only; no new fit or optimisation is run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG845_1_no_C0_support",
            "claim": "C0 is support evidence",
            "status": "forbidden",
            "reason": "C0 remains a closure benchmark until amplitude is parent-predicted and stable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG845_2_no_amplitude_prediction",
            "claim": "b_mem is predicted by the parent theory",
            "status": "forbidden",
            "reason": "178 derived a corridor but explicitly not a prediction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG845_3_no_local_gr_claim",
            "claim": "strict cosmology branch helps derive local GR",
            "status": "forbidden",
            "reason": "local GR remains a separate closure-only theory obligation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG845_4_allowed_contract",
            "claim": "a stricter nonclaim cosmology branch contract is now defined",
            "status": "allowed_private_nonclaim",
            "reason": "the output restricts future fitting freedoms and outcome language",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D845_0",
            "finding": "strict branch contract is required before further cosmology fitting",
            "reason": "current C0 is near-competitive but amplitude freedom is not stable or predicted",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D845_1",
            "finding": "clean support route is parent-predicted amplitude",
            "reason": "only a no-fit b_mem theorem escapes rescue-fitting criticism",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D845_2",
            "finding": "operational exploratory route is predeclared parent corridor",
            "reason": "178 gives a plausible corridor but not a unique prediction",
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
            "objective": "turn the strict branch contract into a dry-run scoring specification without running long fits",
            "include": "candidate branch rows, frozen/predeclared parameter file shape, baseline symmetry, data arenas, pass/fail outcomes, no-claim output schema",
            "exclude": "new data fit, GitHub action, formalization-workbench edits, support/death/local-GR claims",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "strict cosmology branch contract installed with explicit amplitude-freedom and outcome-language rules",
            "clean_support_route": "parent-predicted b_mem before data",
            "operational_route": "predeclared parent amplitude corridor for exploratory holdout only",
            "what_is_not_claimed": "new evidence, C0 support, b_mem prediction, dark energy derivation, local GR relevance",
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
    strict_rows: list[dict[str, object]],
    parameter_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    outcome_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_844_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    branch_ids = {row["branch_id"] for row in strict_rows}
    branches_ok = branch_ids == {
        "SB845_0_C0_archive",
        "SB845_1_parent_predicted",
        "SB845_2_predeclared_corridor",
        "SB845_3_null_control",
    }
    bmem_rule = any(row["parameter"] == "b_mem" and row["support_allowed_if_free"] == "false" for row in parameter_rows)
    gates_ok = {row["gate_id"] for row in gate_rows} == {
        "TG845_0_no_rescue_fit",
        "TG845_1_same_baselines",
        "TG845_2_multi_arena_holdout",
        "TG845_3_model_selection",
        "TG845_4_parent_upgrade",
        "TG845_5_local_gr_firewall",
    }
    outcomes_ok = {row["outcome_id"] for row in outcome_rows} == {
        "OR845_0_support_grade",
        "OR845_1_near_competitive",
        "OR845_2_arena_specific",
        "OR845_3_failure",
    }
    no_support = not any(row["support_claim_allowed"] == "true" for row in strict_rows)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    guards_ok = any(row["guard_id"] == "CG845_2_no_amplitude_prediction" and row["status"] == "forbidden" for row in guard_rows)
    nonclaim_ok = all_valid_for_claim_false([source_rows, strict_rows, parameter_rows, gate_rows, outcome_rows, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V845_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V845_1_prior_844_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V845_2_strict_branches_recorded",
            "result": "pass" if branches_ok else "fail",
            "detail": "C0 benchmark, parent-predicted, predeclared-corridor, and null-control branches recorded",
        },
        {
            "check_id": "V845_3_bmem_freedom_restricted",
            "result": "pass" if bmem_rule else "fail",
            "detail": "b_mem free support is forbidden unless parent-predicted",
        },
        {
            "check_id": "V845_4_test_gates_complete",
            "result": "pass" if gates_ok else "fail",
            "detail": "no-rescue, baseline, holdout, model-selection, parent-upgrade, and local-GR gates recorded",
        },
        {
            "check_id": "V845_5_outcome_language_complete",
            "result": "pass" if outcomes_ok else "fail",
            "detail": "support, near-competitive, arena-specific, and failure language rules recorded",
        },
        {
            "check_id": "V845_6_no_support_claim_allowed",
            "result": "pass" if no_support and no_claim and guards_ok else "fail",
            "detail": "no strict branch currently allows support or parent-amplitude prediction claim",
        },
        {
            "check_id": "V845_7_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V845_8_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V845_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V845_10_validation_rows_ready",
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
    strict_rows: list[dict[str, object]],
    parameter_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    outcome_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 845 - Y5 R10 Strict MTS Cosmology Branch Contract",
        "",
        "Current result: **a stricter cosmology branch is now specified as a contract, not as a new fit**. C0 remains a closure-only benchmark. The clean support route is a parent-predicted `b_mem` before data; the operational exploratory route is a predeclared parent-corridor holdout that cannot become support unless upgraded by a parent amplitude theorem.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "clean_support_route", "operational_route", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Strict Branch Contract",
        "",
        csv_table(strict_rows, ["branch_id", "branch_name", "purpose", "amplitude_rule", "free_amplitude_status", "allowed_use", "forbidden_use", "support_claim_allowed", "valid_for_claim"]),
        "",
        "## Parameter Freedom Ledger",
        "",
        csv_table(parameter_rows, ["parameter", "role", "allowed_mode", "source_rule", "counts_in_AIC_BIC", "support_allowed_if_free", "valid_for_claim"]),
        "",
        "## Strict Test Gate",
        "",
        csv_table(gate_rows, ["gate_id", "gate", "pass_condition", "failure_consequence", "valid_for_claim"]),
        "",
        "## Outcome Language Rules",
        "",
        csv_table(outcome_rows, ["outcome_id", "condition", "allowed_language", "forbidden_language", "current_status", "valid_for_claim"]),
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
    strict_rows = strict_branch_rows(generated_utc)
    parameter_rows = parameter_freedom_rows(generated_utc)
    gate_rows = test_gate_rows(generated_utc)
    outcome_rows = outcome_rule_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, strict_rows, parameter_rows, gate_rows, outcome_rows, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(STRICT_BRANCH_PATH, strict_rows, ["branch_id", "branch_name", "purpose", "amplitude_rule", "free_amplitude_status", "allowed_use", "forbidden_use", "support_claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(PARAMETER_FREEDOM_PATH, parameter_rows, ["parameter", "role", "allowed_mode", "source_rule", "counts_in_AIC_BIC", "support_allowed_if_free", "valid_for_claim", "generated_utc"])
    write_csv(TEST_GATE_PATH, gate_rows, ["gate_id", "gate", "pass_condition", "failure_consequence", "valid_for_claim", "generated_utc"])
    write_csv(OUTCOME_RULE_PATH, outcome_rows, ["outcome_id", "condition", "allowed_language", "forbidden_language", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "clean_support_route", "operational_route", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, strict_rows, parameter_rows, gate_rows, outcome_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
