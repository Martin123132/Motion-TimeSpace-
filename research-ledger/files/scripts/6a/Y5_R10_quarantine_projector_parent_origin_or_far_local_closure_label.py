from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "841-Y5-R10-quarantine-projector-parent-origin-or-far-local-closure-label.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_841_SOURCE_REGISTER.csv"
THEOREM_CHAIN_PATH = RESIDUALS / "P8_Y5_R10_841_PROJECTOR_THEOREM_CHAIN.csv"
CLOSURE_LABEL_PATH = RESIDUALS / "P8_Y5_R10_841_LOCAL_BRANCH_CLOSURE_LABEL.csv"
NEXT_ROUTE_PATH = RESIDUALS / "P8_Y5_R10_841_NEXT_THEOREM_ROUTE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_841_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_841_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_841_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_841_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_841_VALIDATION.csv"

STATUS = "Y5_R10_841_quarantine_projector_not_derived_far_local_closure_label_installed_nonclaim"
CLAIM_CEILING = "far_local_conditional_plus_quarantine_contract_only_no_derived_local_GR_pass"
NEXT_TARGET = "842-Y5-R10-doubled-open-system-metric-null-theorem-or-closure-demotion.md"

SOURCE_SPECS = [
    {
        "source_id": "840_doc",
        "path": POST_CHECKPOINT / "840-Y5-R10-parent-sign-F2-CDU-or-transition-quarantine-contract.md",
        "needles": [
            "quarantine projector is now the best next derivation target",
            "841-Y5-R10-quarantine-projector-parent-origin-or-far-local-closure-label.md",
            "V840_9_formalization_workbench_untouched",
        ],
        "role": "immediate parent-sign route handoff",
    },
    {
        "source_id": "840_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_840_VALIDATION.csv",
        "needles": [
            "V840_5_quarantine_route_ranked_first,pass",
            "V840_6_claim_guards_forbid_overclaim,pass",
            "V840_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "135_projector_origin",
        "path": FORMALIZATION / "135-quarantine-projector-parent-origin.md",
        "needles": [
            "quarantine_projector_parent_origin_not_derived_kernel_route_identified",
            "R_loc q_tr = 0",
            "projector parent origin = candidate route identified, not derived",
        ],
        "role": "projector-origin theorem gate",
    },
    {
        "source_id": "136_response_kernel",
        "path": FORMALIZATION / "136-metric-response-kernel-theorem.md",
        "needles": [
            "metric_response_kernel_formal_only_source_lift_missing_parent_theorem_not_derived",
            "q_tr source lift parent-derived = false",
            "R_loc[delta K_matter] -> GR/Newton",
        ],
        "role": "response-kernel theorem gate",
    },
    {
        "source_id": "137_source_lift",
        "path": FORMALIZATION / "137-transition-source-lift-action-block.md",
        "needles": [
            "transition source lift = not derived",
            "action-block orthogonality = not derived",
            "derived local GR = false",
        ],
        "role": "source-lift action block gate",
    },
    {
        "source_id": "138_metric_null_contract",
        "path": FORMALIZATION / "138-metric-null-action-block-contract.md",
        "needles": [
            "metric_null_action_block_contract_defined_not_derived_route_contract_only",
            "derived_local_GR = false",
            "the transition route survives only as contract-only closure",
        ],
        "role": "metric-null action-block contract",
    },
    {
        "source_id": "139_covariance_route",
        "path": FORMALIZATION / "139-covariance-escape-route-selection.md",
        "needles": [
            "covariance_escape_route_selected_doubled_open_system_not_derived_contract_only",
            "Primary selected route:",
            "the transition route survives as contract-only closure with a selected doubled-action theorem target",
        ],
        "role": "selected next theorem route",
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


def theorem_chain_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "chain_id": "TC841_0_projector_origin",
            "gate": "quarantine projector parent origin",
            "result": "candidate_kernel_route_identified_not_derived",
            "useful_output": "P_metric,loc q_tr=0 can be reframed as R_loc q_tr=0",
            "remaining_gap": "R_loc is not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "TC841_1_response_kernel",
            "gate": "metric response kernel theorem",
            "result": "formal_Rloc_chain_defined_source_lift_missing",
            "useful_output": "R_loc[q]=P_PPN G_loc Sigma_metric[q] and matter response must remain GR/Newton",
            "remaining_gap": "Sigma_metric[q_tr] and kernel condition are not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "TC841_2_source_lift",
            "gate": "transition source-lift action block",
            "result": "source_lift_and_action_block_orthogonality_not_derived",
            "useful_output": "exact source-lift/action-block conditions are known",
            "remaining_gap": "current parent scaffold cannot derive Sigma_metric[q_tr]=0 or R_loc[q_tr]=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "TC841_3_metric_null_contract",
            "gate": "metric-null action-block contract",
            "result": "C0_C9_contract_defined_not_derived",
            "useful_output": "future parent action has an exact contract preserving matter GR response",
            "remaining_gap": "parent v1 does not derive the contract",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "TC841_4_covariance_route",
            "gate": "covariance escape route selection",
            "result": "doubled_open_system_route_selected_not_derived",
            "useful_output": "best next theorem target aligns with open-system/exchange-current scaffold",
            "remaining_gap": "no doubled action currently proves Sigma_metric[q_tr]=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def closure_label_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "label_id": "CL841_0_local_GR_status",
            "branch": "local_GR_reduction",
            "label": "far_local_conditional_plus_quarantine_contract_only",
            "allowed_use": "private theorem target, smoke runners, far-local conditional estimates, explicit closure-labelled tests",
            "forbidden_use": "derived local GR/Newton, transition-shell PPN pass, public local-GR claim",
            "exit_condition": "derive doubled/open-system or equivalent parent action satisfying C0-C9 and preserving matter GR response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "label_id": "CL841_1_transition_shell_status",
            "branch": "transition_shell",
            "label": "quarantine_projector_not_parent_derived",
            "allowed_use": "explicit conservation-owned quarantine closure and next theorem construction",
            "forbidden_use": "claim P_metric,loc=0 follows from current parent theory",
            "exit_condition": "parent-derived R_loc q_tr=0 or Sigma_metric[q_tr]=0 with matter GR response intact",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "label_id": "CL841_2_far_local_status",
            "branch": "far_local",
            "label": "conditional_U_B2_suppression_plumbing_only",
            "allowed_use": "nonclaim coefficient and q-gradient smoke checks away from transition shells",
            "forbidden_use": "extend far-local suppression through U_B=O(1) shells",
            "exit_condition": "separate shell theorem or closure demotion remains explicit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "NR841_0_primary",
            "route": "doubled_open_system_metric_null_theorem",
            "why_selected": "139 ranks it as most aligned with current open-system/exchange-current scaffold",
            "must_prove": "a covariant doubled action makes Sigma_metric[q_tr]=0 or R_loc[q_tr]=0 while matter still sources GR/Newton",
            "failure_consequence": "demote transition-shell local GR to explicit closure-only, or try boundary/topological backup route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "NR841_1_backup",
            "route": "boundary_or_topological_metric_null_backup",
            "why_selected": "138/139 keep it as backup if doubled route fails",
            "must_prove": "transition source lift is pure boundary/topological improvement with no local metric response and no boundary mass flux",
            "failure_consequence": "residual-bound local branch only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG841_0_no_projector_claim",
            "claim": "quarantine projector is parent-derived",
            "status": "forbidden",
            "reason": "135-138 identify theorem shape/contract but repeatedly mark parent derivation false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG841_1_no_local_GR_claim",
            "claim": "MTS reduces to GR/Newton locally through transition shells",
            "status": "forbidden",
            "reason": "transition-shell metric-null action block remains contract-only closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG841_2_allowed_private_result",
            "claim": "local branch is far-local conditional plus quarantine contract-only, with doubled-route theorem target selected",
            "status": "allowed_private_nonclaim",
            "reason": "this is a closure label and route selector, not a physics claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D841_0",
            "finding": "projector-origin chain does not derive local GR",
            "reason": "R_loc, Sigma_metric[q_tr], action-block orthogonality, and metric-null contract remain parent-unsigned",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D841_1",
            "finding": "closure label installed",
            "reason": "current local branch is far-local conditional plus quarantine contract-only",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D841_2",
            "finding": "next derivation route selected",
            "reason": "doubled open-system action is the cleanest covariance escape route currently identified",
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
            "objective": "try the doubled open-system metric-null theorem; if it fails, keep transition-shell local GR closure-only",
            "include": "doubled action variables, metric variation audit, owner equations, matter GR preservation, no-current-erasure guard, fail/demote rule",
            "exclude": "local-GR claim, transition-shell handwave, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "installed far-local/quarantine closure label and selected doubled open-system theorem route",
            "what_is_not_claimed": "parent-derived projector, R_loc kernel, source-lift action block, metric-null contract, local GR/Newton",
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
    chain_rows: list[dict[str, object]],
    label_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_840_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    chain_complete = {row["chain_id"] for row in chain_rows} == {
        "TC841_0_projector_origin",
        "TC841_1_response_kernel",
        "TC841_2_source_lift",
        "TC841_3_metric_null_contract",
        "TC841_4_covariance_route",
    }
    closure_installed = any(row["label"] == "far_local_conditional_plus_quarantine_contract_only" for row in label_rows)
    projector_forbidden = any(row["guard_id"] == "CG841_0_no_projector_claim" and row["status"] == "forbidden" for row in guard_rows)
    doubled_selected = bool(route_rows) and route_rows[0]["route"] == "doubled_open_system_metric_null_theorem"
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, chain_rows, label_rows, route_rows, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V841_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V841_1_prior_840_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V841_2_theorem_chain_recorded",
            "result": "pass" if chain_complete else "fail",
            "detail": "projector, kernel, source-lift, metric-null, and covariance gates recorded",
        },
        {
            "check_id": "V841_3_closure_label_installed",
            "result": "pass" if closure_installed else "fail",
            "detail": "far-local conditional plus quarantine contract-only label installed",
        },
        {
            "check_id": "V841_4_projector_claim_forbidden",
            "result": "pass" if projector_forbidden else "fail",
            "detail": "parent-derived projector claim forbidden",
        },
        {
            "check_id": "V841_5_doubled_route_selected",
            "result": "pass" if doubled_selected else "fail",
            "detail": "doubled open-system theorem route selected",
        },
        {
            "check_id": "V841_6_no_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no local-GR or Newton claim allowed",
        },
        {
            "check_id": "V841_7_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V841_8_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V841_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V841_10_validation_rows_ready",
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
    chain_rows: list[dict[str, object]],
    label_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 841 - Y5 R10 Quarantine Projector Parent Origin Or Far-Local Closure Label",
        "",
        "Current result: **the quarantine projector is not parent-derived in the current corpus, so the local branch is now explicitly labelled `far_local_conditional_plus_quarantine_contract_only`**. The theorem chain is still alive as a target: `R_loc q_tr=0`, `Sigma_metric[q_tr]=0`, and the C0-C9 metric-null contract are all clean shapes. But `135` through `139` do not derive them. The selected next route is a doubled open-system metric-null theorem; if that fails, transition-shell local GR stays closure-only.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Projector Theorem Chain",
        "",
        csv_table(chain_rows, ["chain_id", "gate", "result", "useful_output", "remaining_gap", "claim_allowed", "valid_for_claim"]),
        "",
        "## Local Branch Closure Label",
        "",
        csv_table(label_rows, ["label_id", "branch", "label", "allowed_use", "forbidden_use", "exit_condition", "valid_for_claim"]),
        "",
        "## Next Theorem Route",
        "",
        csv_table(route_rows, ["route_id", "route", "why_selected", "must_prove", "failure_consequence", "valid_for_claim"]),
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
    chain_rows = theorem_chain_rows(generated_utc)
    label_rows = closure_label_rows(generated_utc)
    route_rows = next_route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, chain_rows, label_rows, route_rows, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(THEOREM_CHAIN_PATH, chain_rows, ["chain_id", "gate", "result", "useful_output", "remaining_gap", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_LABEL_PATH, label_rows, ["label_id", "branch", "label", "allowed_use", "forbidden_use", "exit_condition", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_ROUTE_PATH, route_rows, ["route_id", "route", "why_selected", "must_prove", "failure_consequence", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, chain_rows, label_rows, route_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
