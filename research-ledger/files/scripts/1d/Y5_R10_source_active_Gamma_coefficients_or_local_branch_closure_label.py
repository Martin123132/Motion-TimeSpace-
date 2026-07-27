from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "837-Y5-R10-source-active-Gamma-coefficients-or-local-branch-closure-label.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_837_SOURCE_REGISTER.csv"
COEFFICIENT_HUNT_PATH = RESIDUALS / "P8_Y5_R10_837_COEFFICIENT_HUNT_LEDGER.csv"
CLOSURE_LABEL_PATH = RESIDUALS / "P8_Y5_R10_837_LOCAL_BRANCH_CLOSURE_LABEL.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_837_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_837_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_837_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_837_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_837_VALIDATION.csv"

STATUS = "Y5_R10_837_local_branch_closure_label_installed_coefficients_response_missing_nonclaim"
CLAIM_CEILING = "closure_label_and_coefficient_hunt_ledger_only_no_local_GR_pass"
NEXT_TARGET = "838-Y5-R10-active-Gamma-coefficient-source-pack-or-parent-derivation.md"

SOURCE_SPECS = [
    {
        "source_id": "836_doc",
        "path": POST_CHECKPOINT / "836-Y5-R10-fill-active-Gamma-bound-from-source-support-or-demote-local-branch.md",
        "needles": [
            "source-support fills useful form and proxy small-parameter values",
            "DG836_3_demote_or_continue",
            "837-Y5-R10-source-active-Gamma-coefficients-or-local-branch-closure-label.md",
        ],
        "role": "immediate demotion handoff",
    },
    {
        "source_id": "836_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_836_VALIDATION.csv",
        "needles": [
            "V836_2_proxy_values_extracted,pass",
            "V836_7_demote_claim_not_route,pass",
            "V836_11_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "835_runner",
        "path": POST_CHECKPOINT / "835-Y5-R10-Gamma-active-mode-bound-and-local-response-runner.md",
        "needles": [
            "active-Gamma local-test runner now exists",
            "active_gamma_coeff",
            "missing_response_matrix",
        ],
        "role": "runner fields that remain unfilled",
    },
    {
        "source_id": "800_support_power_warning",
        "path": POST_CHECKPOINT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
        "needles": [
            "pT=2 is not derived by Pi_B",
            "pL=2 is not derived by Pi_B",
            "not_derived_as_parent_theorem",
        ],
        "role": "support-power closure warning",
    },
    {
        "source_id": "equation_register_coeff_form",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "L_cg^-2 F_L = Lambda_loc + D_L^2 F_2",
            "L_cg^-2 F_L - Lambda_loc = O(U_B^2)",
            "D_L derivation overclaim",
        ],
        "role": "coefficient-form source without claimable coefficient extraction",
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


def coefficient_hunt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "item_id": "CH837_0_C_D",
            "coefficient": "C_D",
            "candidate_formula": "Gamma_eff-Lambda_loc = C_D D_L^2 + O(D_L^3)",
            "current_evidence": "equation register has D_L^2 form but D_L derivation is flagged overclaim",
            "status": "not_sourced",
            "needed_to_promote": "derive D_L and C_D from parent expansion or provide sourced bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "CH837_1_C_U",
            "coefficient": "C_U",
            "candidate_formula": "Gamma_eff-Lambda_loc = C_U U_B^2 + O(U_B^3)",
            "current_evidence": "source-support provides U_B^2 forms and proxy values, not C_U",
            "status": "not_sourced",
            "needed_to_promote": "derive C_U from F_L/L_cg expansion or source a rigorous upper bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "CH837_2_K00_projection",
            "coefficient": "f_00",
            "candidate_formula": "|Kbar_00| <= f_00 sqrt(n/(n-1)) C_gamma s^p",
            "current_evidence": "Khat component/readout theorem remains missing",
            "status": "not_sourced",
            "needed_to_promote": "derive carrier component map in the matter frame",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "CH837_3_response_matrix",
            "coefficient": "R_metric",
            "candidate_formula": "observable_residual <= R_metric f_00 sqrt(n/(n-1)) C_gamma s^p/K_matter",
            "current_evidence": "PPN/R10/clock/orbital/WEP response matrices are missing",
            "status": "not_sourced",
            "needed_to_promote": "source or derive arena response coefficients and limits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def closure_label_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "label_id": "CL837_0_local_branch_status",
            "branch": "local_GR_reduction",
            "label": "closure_input_acquisition_not_derived_local_GR",
            "allowed_use": "private derivation target, symbolic runner, source-acquisition ledger, nonclaim smoke rows",
            "forbidden_use": "public/local-GR pass, PPN pass, R10 pass, WEP pass, or claim that MTS reduces to GR",
            "exit_condition": "C_D/C_U, D_L/U_B, Khat projection, matter descent, response matrices, and arena bounds sourced and passing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "label_id": "CL837_1_route_status",
            "branch": "tracefree_Khat_active_Gamma_route",
            "label": "mathematically_live_but_unscored",
            "allowed_use": "continue deriving coefficients and response maps",
            "forbidden_use": "treat small U_B proxies as proof",
            "exit_condition": "active-Gamma runner rows become fully numeric, sourced, and pass all local arenas",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG837_0_no_reduction_claim",
            "claim": "MTS reduces to GR/Newton locally",
            "status": "forbidden",
            "reason": "active-Gamma coefficients and response matrices are not sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG837_1_no_proxy_claim",
            "claim": "tiny U_B^2 proxy proves local safety",
            "status": "forbidden",
            "reason": "proxy lacks C_gamma, Khat readout, matter curvature, and observable response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG837_2_allowed_statement",
            "claim": "MTS has a precise local closure/input-acquisition gate",
            "status": "allowed_private_nonclaim",
            "reason": "836/837 identify exact missing fields and exit conditions",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D837_0",
            "finding": "local branch closure label installed",
            "reason": "coefficients, Khat projection, matter descent, and response matrices are still missing",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D837_1",
            "finding": "next work should source active-Gamma coefficients first",
            "reason": "response work is meaningless unless C_D/C_U or a rigorous bound exists",
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
            "objective": "derive or source C_D/C_U from active-Gamma expansions before further local-response scoring",
            "include": "F_L/L_cg expansion, D_L/U_B relation, coefficient upper bound, source paths, nonclaim runner update",
            "exclude": "local-GR claim, proxy-only pass, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "installed machine-readable closure label and coefficient hunt ledger",
            "what_is_not_claimed": "local GR, Newton limit, PPN/R10/WEP pass, sourced C_D/C_U, response matrix",
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
    coefficient_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_836_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    coefficients_missing = all(row["status"] == "not_sourced" for row in coefficient_rows)
    closure_installed = any(row["label"] == "closure_input_acquisition_not_derived_local_GR" for row in closure_rows)
    guards_forbid = {"CG837_0_no_reduction_claim", "CG837_1_no_proxy_claim"}.issubset(
        {row["guard_id"] for row in guard_rows if row["status"] == "forbidden"}
    )
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, coefficient_rows, closure_rows, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V837_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V837_1_prior_836_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V837_2_coefficients_remain_unsourced",
            "result": "pass" if coefficients_missing else "fail",
            "detail": "C_D, C_U, K00 projection, and response matrix remain unsourced",
        },
        {
            "check_id": "V837_3_closure_label_installed",
            "result": "pass" if closure_installed else "fail",
            "detail": "local branch labelled closure/input-acquisition",
        },
        {
            "check_id": "V837_4_claim_guards_forbid_overclaim",
            "result": "pass" if guards_forbid else "fail",
            "detail": "local-GR and proxy-only claims forbidden",
        },
        {
            "check_id": "V837_5_no_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no local-GR or arena claim allowed",
        },
        {
            "check_id": "V837_6_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V837_7_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V837_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V837_9_validation_rows_ready",
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
    coefficient_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 837 - Y5 R10 Source Active-Gamma Coefficients Or Local Branch Closure Label",
        "",
        "Current result: **the local branch is now explicitly labelled as closure/input-acquisition, not derived local GR**. The route remains mathematically live, but the claim is locked until `C_D/C_U`, `Khat` projection, matter descent, and local response matrices are sourced and pass the runner.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Coefficient Hunt Ledger",
        "",
        csv_table(coefficient_rows, ["item_id", "coefficient", "candidate_formula", "current_evidence", "status", "needed_to_promote", "valid_for_claim"]),
        "",
        "## Closure Label",
        "",
        csv_table(closure_rows, ["label_id", "branch", "label", "allowed_use", "forbidden_use", "exit_condition", "valid_for_claim"]),
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
    coefficient_rows = coefficient_hunt_rows(generated_utc)
    closure_rows = closure_label_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, coefficient_rows, closure_rows, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(COEFFICIENT_HUNT_PATH, coefficient_rows, ["item_id", "coefficient", "candidate_formula", "current_evidence", "status", "needed_to_promote", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_LABEL_PATH, closure_rows, ["label_id", "branch", "label", "allowed_use", "forbidden_use", "exit_condition", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, coefficient_rows, closure_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
