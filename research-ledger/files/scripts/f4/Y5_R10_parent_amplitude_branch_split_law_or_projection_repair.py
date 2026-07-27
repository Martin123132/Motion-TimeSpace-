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

OUTPUT_DOC = POST_CHECKPOINT / "854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_854_SOURCE_REGISTER.csv"
TARGETS_PATH = RESIDUALS / "P8_Y5_R10_854_BRANCH_SPLIT_TARGETS.csv"
LAW_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_854_BRANCH_SPLIT_LAW_ATTEMPT.csv"
CLAUSE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_854_PARENT_CLAUSE_AUDIT.csv"
REPAIR_OPTIONS_PATH = RESIDUALS / "P8_Y5_R10_854_PROJECTION_REPAIR_OPTIONS.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_854_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_854_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_854_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_854_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_854_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_854_VALIDATION.csv"

BRANCH_READOUT_PATH = RESIDUALS / "P8_Y5_R10_853_BRANCH_READOUT.csv"
AMPLITUDE_SPLIT_PATH = RESIDUALS / "P8_Y5_R10_853_AMPLITUDE_SPLIT_AUDIT.csv"

STATUS = "Y5_R10_854_branch_split_law_contract_ready_nonclaim"
CLAIM_CEILING = "formal_branch_split_contract_only_no_parent_prediction_no_support"
NEXT_TARGET = "855-Y5-R10-calibration-projection-response-estimator-dry-run.md"

SOURCE_SPECS = [
    {
        "source_id": "853_doc",
        "path": POST_CHECKPOINT / "853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md",
        "needles": [
            "private nonclaim lead",
            "branch-dependent",
            "854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md",
        ],
        "role": "positive lead and branch-split handoff",
    },
    {
        "source_id": "853_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_853_VALIDATION.csv",
        "needles": [
            "V853_2_positive_lead_present,pass",
            "V853_3_amplitude_split_recorded,pass",
            "V853_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "853_branch_readout",
        "path": BRANCH_READOUT_PATH,
        "needles": ["no_sh0es", "sh0es", "competitive_nonclaim"],
        "role": "best branch fixed-bmem amplitudes",
    },
    {
        "source_id": "853_amplitude_split",
        "path": AMPLITUDE_SPLIT_PATH,
        "needles": ["branch_dependent_effective_amplitude", "ratio_sh0es_over_no_sh0es"],
        "role": "branch amplitude split summary",
    },
    {
        "source_id": "177_parent_amplitude_contract",
        "path": FORMALIZATION / "177-parent-amplitude-repair-contract.md",
        "needles": ["derive the amplitude before fitting it", "b_mem = a_F DeltaR / [3 eta^2]", "covariant conservation compatibility"],
        "role": "parent amplitude obligations",
    },
    {
        "source_id": "178_parent_amplitude_attempt",
        "path": FORMALIZATION / "178-parent-amplitude-theorem-attempt.md",
        "needles": ["only a corridor derives", "amplitude prediction derived = false", "unique no-fit b_mem prediction"],
        "role": "prior theorem attempt and open gaps",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def finite_float(value: object) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: object) -> str:
    number = finite_float(value)
    return "" if number is None else f"{number:.12g}"


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


def target_rows(branch_readout: list[dict[str, str]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in branch_readout:
        b_mem = float(row["b_mem_fixed"])
        rows.append(
            {
                "branch": row["branch"],
                "empirical_best_positive_candidate": row["best_positive_candidate"],
                "b_eff_target": fmt(b_mem),
                "eta1_aF_DeltaR_target": fmt(3.0 * b_mem),
                "delta_BIC_vs_best_fit_baseline": row["delta_BIC_vs_best_fit_baseline"],
                "target_status": "private_nonclaim_target_for_parent_law",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def law_attempt_rows(targets: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    no_sh0es = next(row for row in targets if row["branch"] == "no_sh0es")
    sh0es = next(row for row in targets if row["branch"] == "sh0es")
    b_parent_probe = float(no_sh0es["b_eff_target"])
    b_sh0es = float(sh0es["b_eff_target"])
    response = b_sh0es - b_parent_probe
    return [
        {
            "law_id": "BSL854_0_parent_identity",
            "statement": "b_parent = a_F DeltaR/(3 eta^2)",
            "status": "formal_identity_survives",
            "numeric_target_or_coefficient": "not_unique",
            "derivation_status": "corridor_only_from_178",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "BSL854_1_effective_branch_law",
            "statement": "b_eff[B] = b_parent + Pi_B(calibration/local-offset response)",
            "status": "proposed_contract_not_derived",
            "numeric_target_or_coefficient": f"b_parent_probe={fmt(b_parent_probe)}; response_sh0es_minus_no_sh0es={fmt(response)}",
            "derivation_status": "requires projection operator from SN calibration/marginalization geometry",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "BSL854_2_linear_response_estimator",
            "statement": "delta b_B = (J_b^T W_B P_B J_cal)/(J_b^T W_B P_B J_b) delta cal_B",
            "status": "least_squares_projection_candidate",
            "numeric_target_or_coefficient": "must reproduce response_sh0es_minus_no_sh0es without fitting b_mem",
            "derivation_status": "algebraic estimator can be tested next; parent physical origin not yet signed",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "BSL854_3_multiplicative_response_fallback",
            "statement": "b_eff[B] = R_B b_parent",
            "status": "fallback_phenomenological_parameterization",
            "numeric_target_or_coefficient": f"R_sh0es_over_no_sh0es={fmt(b_sh0es / b_parent_probe)}",
            "derivation_status": "not acceptable as final theory unless R_B is derived from observables",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def clause_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "PC854_0_eta",
            "parent_clause": "eta = H0 L_cg/c",
            "required_for_branch_law": "derive whether L_cg is invariant or observer/calibration projected",
            "status": "open",
            "next_test": "calibration projection estimator cannot prove eta but can tell whether branch split is observational",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC854_1_aF",
            "parent_clause": "a_F sign and normalization",
            "required_for_branch_law": "derive trace-coupling normalization and whether it couples to local calibration sector",
            "status": "open",
            "next_test": "if response term aligns with calibration projection, a_F may remain invariant while Pi_B changes",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC854_2_DeltaR",
            "parent_clause": "DeltaR endpoint memory dynamics",
            "required_for_branch_law": "derive whether endpoint difference is single cosmic memory or branch-effective observable memory",
            "status": "open",
            "next_test": "projection estimator should separate invariant shape-only target from SH0ES response excess",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC854_3_conservation",
            "parent_clause": "covariant conservation/Bianchi compatibility",
            "required_for_branch_law": "response term must be observational/projection-level or have conserved stress-energy source",
            "status": "open_guardrail",
            "next_test": "do not promote response_B to physical field term unless conservation accounting is signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def repair_option_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "option_id": "RO854_0_observable_projection",
            "option": "b_eff is branch-projected while b_parent is invariant",
            "pros": "explains why no_SH0ES and SH0ES prefer different effective amplitudes without making parent memory inconsistent",
            "risk": "can become post-hoc unless projection operator predicts the split before scoring",
            "next_action": "estimate Pi_B from SN covariance/calibration vectors and BAO response",
            "selected": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "option_id": "RO854_1_projection_repair",
            "option": "current M6 memory projection shape is incomplete",
            "pros": "directly addresses branch split if response estimator fails",
            "risk": "too much freedom if alpha/nu or shape are opened without parent derivation",
            "next_action": "only after calibration projection estimator fails",
            "selected": "fallback",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "option_id": "RO854_2_single_amplitude_claim",
            "option": "declare one branch amplitude fundamental",
            "pros": "simple",
            "risk": "ignores observed branch dependence and would be weak/overclaiming",
            "next_action": "reject for now",
            "selected": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC854_0_selected",
            "route": "calibration_projection_response_estimator",
            "status": "selected",
            "reason": "branch split can be a principled observable response only if a projection estimator predicts the SH0ES excess from data geometry",
            "include": "SN branch masks, nuisance offset/calibrator vector, J_b response, BAO response, no b_mem fitting",
            "exclude": "support claim, branch-amplitude assertion, parent derivation by fitted target",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC854_1_deferred",
            "route": "projection_shape_repair",
            "status": "deferred",
            "reason": "only needed if calibration projection fails to account for the branch split",
            "include": "activation-shape or BAO-response repair contract",
            "exclude": "opening free shape parameters now",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG854_0_no_parent_prediction",
            "claim": "854 derives b_parent",
            "status": "forbidden",
            "reason": "854 proposes a branch-split law contract; eta/a_F/DeltaR remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG854_1_no_response_claim",
            "claim": "SH0ES excess is proven calibration response",
            "status": "forbidden",
            "reason": "projection estimator has not yet been run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG854_2_no_support",
            "claim": "positive fixed memory is public support",
            "status": "forbidden",
            "reason": "positive lead remains private and parent/robustness gates are open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG854_3_allowed_contract",
            "claim": "a concrete branch-split law contract is ready to test",
            "status": "allowed_private_nonclaim",
            "reason": "854 converts the amplitude split into a falsifiable projection-estimator target",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D854_0",
            "finding": "branch split should not be collapsed into a single fitted amplitude",
            "reason": "no_SH0ES and SH0ES prefer different effective amplitudes after fair refit",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D854_1",
            "finding": "observable projection law is the least-ad-hoc next route",
            "reason": "it can be tested against SN calibration/marginalization geometry before changing the physics projection",
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
            "objective": "estimate whether the SH0ES/no-SH0ES b_eff split follows from calibration projection geometry rather than a new fitted field amplitude",
            "include": "linear response estimator, SN branch masks, calibrator/local-offset vector, finite-difference J_b, BAO penalty, no support claim",
            "exclude": "fitting b_mem, deriving eta from the fitted split, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "converted branch-dependent b_eff into a formal parent-plus-projection contract",
            "selected_route": "calibration_projection_response_estimator",
            "what_is_not_claimed": "parent amplitude, calibration proof, support, public evidence, local-GR progress",
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
    targets: list[dict[str, object]],
    law_rows: list[dict[str, object]],
    clauses: list[dict[str, object]],
    repairs: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_853_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    targets_ok = len(targets) == 2 and {row["branch"] for row in targets} == {"no_sh0es", "sh0es"}
    law_ok = any(row["law_id"] == "BSL854_1_effective_branch_law" for row in law_rows) and any(row["law_id"] == "BSL854_2_linear_response_estimator" for row in law_rows)
    clauses_open = len(clauses) == 4 and all(str(row["status"]).startswith("open") for row in clauses)
    repair_selected = any(row["option_id"] == "RO854_0_observable_projection" and row["selected"] == "true" for row in repairs)
    route_ok = any(row["route_id"] == "RC854_0_selected" and row["route"] == "calibration_projection_response_estimator" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, targets, law_rows, clauses, repairs, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V854_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V854_1_prior_853_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V854_2_branch_targets_present", "result": "pass" if targets_ok else "fail", "detail": "no_sh0es and sh0es b_eff targets present"},
        {"check_id": "V854_3_branch_split_law_contract_present", "result": "pass" if law_ok else "fail", "detail": "parent-plus-projection and linear estimator laws recorded"},
        {"check_id": "V854_4_parent_clauses_remain_open", "result": "pass" if clauses_open else "fail", "detail": "eta/a_F/DeltaR/conservation clauses remain open"},
        {"check_id": "V854_5_observable_projection_selected", "result": "pass" if repair_selected and route_ok else "fail", "detail": "calibration projection estimator selected"},
        {"check_id": "V854_6_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V854_7_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V854_8_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V854_9_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V854_10_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    targets: list[dict[str, object]],
    law_rows: list[dict[str, object]],
    clauses: list[dict[str, object]],
    repairs: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 854 - Y5 R10 Parent Amplitude Branch Split Law Or Projection Repair",
        "",
        "Current result: **the branch-dependent fixed-`b_mem` lead has been converted into a parent-plus-observable-projection contract, not a claim**. The least-ad-hoc route is to treat `b_parent = a_F DeltaR/(3 eta^2)` as the invariant corridor quantity and test whether SH0ES/no-SH0ES differences arise from an observable calibration projection, `b_eff[B] = b_parent + Pi_B(...)`. If that estimator fails, the memory projection itself must be repaired before more scoring.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Branch Targets",
        "",
        csv_table(targets, ["branch", "empirical_best_positive_candidate", "b_eff_target", "eta1_aF_DeltaR_target", "delta_BIC_vs_best_fit_baseline", "target_status", "valid_for_claim"]),
        "",
        "## Branch Split Law Attempt",
        "",
        csv_table(law_rows, ["law_id", "statement", "status", "numeric_target_or_coefficient", "derivation_status", "blocks_claim", "valid_for_claim"]),
        "",
        "## Parent Clause Audit",
        "",
        csv_table(clauses, ["clause_id", "parent_clause", "required_for_branch_law", "status", "next_test", "valid_for_claim"]),
        "",
        "## Projection Repair Options",
        "",
        csv_table(repairs, ["option_id", "option", "pros", "risk", "next_action", "selected", "valid_for_claim"]),
        "",
        "## Route Choice",
        "",
        csv_table(routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
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
    branch_readout = read_csv(BRANCH_READOUT_PATH)
    targets = target_rows(branch_readout, generated_utc)
    law_rows = law_attempt_rows(targets, generated_utc)
    clauses = clause_audit_rows(generated_utc)
    repairs = repair_option_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, targets, law_rows, clauses, repairs, routes, guards, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(TARGETS_PATH, targets, ["branch", "empirical_best_positive_candidate", "b_eff_target", "eta1_aF_DeltaR_target", "delta_BIC_vs_best_fit_baseline", "target_status", "valid_for_claim", "generated_utc"])
    write_csv(LAW_ATTEMPT_PATH, law_rows, ["law_id", "statement", "status", "numeric_target_or_coefficient", "derivation_status", "blocks_claim", "valid_for_claim", "generated_utc"])
    write_csv(CLAUSE_AUDIT_PATH, clauses, ["clause_id", "parent_clause", "required_for_branch_law", "status", "next_test", "valid_for_claim", "generated_utc"])
    write_csv(REPAIR_OPTIONS_PATH, repairs, ["option_id", "option", "pros", "risk", "next_action", "selected", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, targets, law_rows, clauses, repairs, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
