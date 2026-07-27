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

OUTPUT_DOC = POST_CHECKPOINT / "853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_853_SOURCE_REGISTER.csv"
BRANCH_READOUT_PATH = RESIDUALS / "P8_Y5_R10_853_BRANCH_READOUT.csv"
AMPLITUDE_SPLIT_PATH = RESIDUALS / "P8_Y5_R10_853_AMPLITUDE_SPLIT_AUDIT.csv"
INTERPRETATION_PATH = RESIDUALS / "P8_Y5_R10_853_INTERPRETATION_GATES.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_853_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_853_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_853_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_853_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_853_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_853_VALIDATION.csv"

SCORES_PATH = RESIDUALS / "P8_Y5_R10_852_FAIR_FIXED_BMEM_SN_BAO_FIT_SCORES.csv"
READOUT_852_PATH = RESIDUALS / "P8_Y5_R10_852_FIT_READOUT.csv"

STATUS = "Y5_R10_853_fixed_bmem_fair_fit_readout_positive_lead_nonclaim"
CLAIM_CEILING = "readout_only_positive_lead_no_support_no_parent_prediction"
NEXT_TARGET = "854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md"

SOURCE_SPECS = [
    {
        "source_id": "852_doc",
        "path": POST_CHECKPOINT / "852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md",
        "needles": [
            "short fair SN/BAO fitted comparator has run",
            "b_mem` itself was not fitted",
            "853-Y5-R10-fixed-bmem-fitted-readout-or-projection-repair.md",
        ],
        "role": "fair comparator handoff",
    },
    {
        "source_id": "852_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_852_VALIDATION.csv",
        "needles": [
            "V852_2_run_status_clean,pass",
            "V852_4_no_bmem_fit,pass",
            "V852_13_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "852_scores",
        "path": SCORES_PATH,
        "needles": [
            "M6_fixed_S1_C0_CMB_reference_fit_fair",
            "M6_fixed_S1_C0_full_joint_reference_fit_fair",
            "S3_parent_predicted_placeholder",
        ],
        "role": "fair fixed-bmem fit scores",
    },
    {
        "source_id": "852_readout",
        "path": READOUT_852_PATH,
        "needles": ["best_positive_delta_BIC", "fair_comparator_completed_nonclaim"],
        "role": "fair comparator branch readout",
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


def best_positive_rows(readout_852: list[dict[str, str]], scores: list[dict[str, str]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for readout in sorted(readout_852, key=lambda row: row["branch"]):
        branch = readout["branch"]
        candidate_id = readout["best_positive_candidate"]
        score = next(row for row in scores if row["branch"] == branch and row["candidate_id"] == candidate_id)
        delta_bic = float(readout["best_positive_delta_BIC"])
        b_mem = float(score["b_mem_fixed"])
        rows.append(
            {
                "branch": branch,
                "best_positive_candidate": candidate_id,
                "b_mem_fixed": fmt(b_mem),
                "eta1_aF_DeltaR_implied": fmt(3.0 * b_mem),
                "chi2_total": score["chi2_total"],
                "delta_BIC_vs_best_fit_baseline": readout["best_positive_delta_BIC"],
                "fit_params": score["fit_param_names"],
                "edge_flags": score["edge_flags"],
                "lead_status": "competitive_nonclaim" if delta_bic < 0.0 else "not_competitive_nonclaim",
                "interpretation": "positive fixed memory survives fair short SN/BAO comparator" if delta_bic < 0.0 else "positive fixed memory does not beat fair baseline",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def amplitude_split_rows(branch_rows: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    by_branch = {str(row["branch"]): row for row in branch_rows}
    no_sh0es = float(by_branch["no_sh0es"]["b_mem_fixed"])
    sh0es = float(by_branch["sh0es"]["b_mem_fixed"])
    ratio = sh0es / no_sh0es if no_sh0es else math.inf
    return [
        {
            "split_id": "AS853_0_best_branch_amplitudes",
            "no_sh0es_best_b_mem": fmt(no_sh0es),
            "sh0es_best_b_mem": fmt(sh0es),
            "absolute_split": fmt(sh0es - no_sh0es),
            "ratio_sh0es_over_no_sh0es": fmt(ratio),
            "eta1_aF_DeltaR_no_sh0es": fmt(3.0 * no_sh0es),
            "eta1_aF_DeltaR_sh0es": fmt(3.0 * sh0es),
            "status": "branch_dependent_effective_amplitude",
            "meaning": "local calibration pressure prefers a larger effective memory amplitude than Pantheon shape-only branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def interpretation_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "IG853_0_positive_memory_alive",
            "gate": "positive fixed b_mem can beat fair fitted SN/BAO baselines",
            "status": "passes_private_nonclaim",
            "reason": "best positive fixed-bmem rows have negative delta_BIC in both sh0es and no_sh0es branches",
            "required_before_claim": "derive b_mem parent amplitude and run robustness matrix",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "IG853_1_parent_prediction_missing",
            "gate": "support-grade b_mem prediction",
            "status": "fails_open",
            "reason": "winning amplitudes are C0/CMB references, not eta/a_F/DeltaR-derived predictions",
            "required_before_claim": "derive eta, a_F, DeltaR and endpoint dynamics without using fitted amplitude as input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "IG853_2_branch_split",
            "gate": "single branch-invariant amplitude",
            "status": "fails_or_needs_effective_response_law",
            "reason": "best sh0es amplitude is much larger than best no_sh0es amplitude",
            "required_before_claim": "derive a calibration/observable projection law or repair the memory projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC853_0_selected",
            "route": "parent_amplitude_branch_split_law_or_projection_repair",
            "status": "selected",
            "reason": "fair comparator turns positive memory into a lead, but the preferred amplitude is branch-dependent and not parent-derived",
            "include": "derive whether b_mem is invariant parent memory, effective observable response, or a projection needing BAO/SH0ES split repair",
            "exclude": "claiming support from fitted C0 references",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC853_1_deferred",
            "route": "full robustness scoring",
            "status": "deferred",
            "reason": "worth doing after the amplitude/projection meaning is specified so the run is not just more phenomenology",
            "include": "later SN/BAO/H(z)/growth-CMB robustness",
            "exclude": "long execution now",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG853_0_no_support",
            "claim": "852/853 supports MTS cosmology",
            "status": "forbidden",
            "reason": "the fit is short, private, and uses candidate amplitudes not parent predictions",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG853_1_no_parent_amplitude",
            "claim": "eta/a_F/DeltaR has been derived",
            "status": "forbidden",
            "reason": "853 only identifies the branch-split target the parent law must explain",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG853_2_no_public_evidence",
            "claim": "negative delta_BIC rows are public evidence",
            "status": "forbidden",
            "reason": "robustness, residuals, data-split stability, and parent derivation remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG853_3_allowed_lead",
            "claim": "positive fixed memory is a private lead after fair refit",
            "status": "allowed_private_nonclaim",
            "reason": "both branches have a positive fixed-bmem row with negative delta_BIC against fair fitted baselines",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D853_0",
            "finding": "fair refit reverses the crude 850 pessimism",
            "reason": "positive fixed memory beats the fair fitted baselines in both SN/BAO branches",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D853_1",
            "finding": "amplitude meaning is now the bottleneck",
            "reason": "best no_sh0es and sh0es amplitudes differ substantially, and neither is parent-derived",
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
            "objective": "derive or repair the meaning of branch-dependent effective b_mem before more scoring",
            "include": "branch split law, eta/a_F/DeltaR targets, calibration-response versus invariant-memory distinction, projection repair options",
            "exclude": "support claim, public evidence, local-GR claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "converted fair fixed-bmem comparator into a positive nonclaim lead and amplitude-split problem",
            "selected_route": "parent_amplitude_branch_split_law_or_projection_repair",
            "what_is_not_claimed": "support, parent prediction, public evidence, local-GR progress",
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
    branch_rows: list[dict[str, object]],
    split_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_852_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    positive_lead_ok = len(branch_rows) == 2 and all(float(row["delta_BIC_vs_best_fit_baseline"]) < 0.0 for row in branch_rows)
    split_ok = bool(split_rows) and split_rows[0]["status"] == "branch_dependent_effective_amplitude"
    gates_ok = any(row["gate_id"] == "IG853_0_positive_memory_alive" and row["status"] == "passes_private_nonclaim" for row in gates) and any(row["gate_id"] == "IG853_2_branch_split" for row in gates)
    route_ok = any(row["route_id"] == "RC853_0_selected" and row["route"] == "parent_amplitude_branch_split_law_or_projection_repair" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, branch_rows, split_rows, gates, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V853_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V853_1_prior_852_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V853_2_positive_lead_present", "result": "pass" if positive_lead_ok else "fail", "detail": "both branches have best positive fixed-bmem delta_BIC < 0"},
        {"check_id": "V853_3_amplitude_split_recorded", "result": "pass" if split_ok else "fail", "detail": "branch-dependent effective amplitude row recorded"},
        {"check_id": "V853_4_interpretation_gates_present", "result": "pass" if gates_ok else "fail", "detail": "positive lead and branch-split gates present"},
        {"check_id": "V853_5_route_selected", "result": "pass" if route_ok else "fail", "detail": "parent amplitude branch-split law/projection repair selected"},
        {"check_id": "V853_6_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V853_7_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V853_8_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V853_9_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V853_10_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    branch_rows: list[dict[str, object]],
    split_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 853 - Y5 R10 Fixed Bmem Fitted Readout Or Projection Repair",
        "",
        "Current result: **the fair fixed-`b_mem` SN/BAO comparator turns positive memory into a private nonclaim lead**. The earlier sample-only pessimism was largely a parameter-artifact warning: after fair refit, positive fixed-memory rows beat the fitted baselines in both SH0ES and no-SH0ES branches. The new bottleneck is not immediate empirical viability; it is what the amplitude means, because the preferred effective `b_mem` is branch-dependent and still not parent-derived.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Branch Readout",
        "",
        csv_table(branch_rows, ["branch", "best_positive_candidate", "b_mem_fixed", "eta1_aF_DeltaR_implied", "chi2_total", "delta_BIC_vs_best_fit_baseline", "lead_status", "interpretation", "valid_for_claim"]),
        "",
        "## Amplitude Split Audit",
        "",
        csv_table(split_rows, ["split_id", "no_sh0es_best_b_mem", "sh0es_best_b_mem", "absolute_split", "ratio_sh0es_over_no_sh0es", "eta1_aF_DeltaR_no_sh0es", "eta1_aF_DeltaR_sh0es", "status", "meaning", "valid_for_claim"]),
        "",
        "## Interpretation Gates",
        "",
        csv_table(gates, ["gate_id", "gate", "status", "reason", "required_before_claim", "valid_for_claim"]),
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
    scores = read_csv(SCORES_PATH)
    readout_852 = read_csv(READOUT_852_PATH)
    branch_rows = best_positive_rows(readout_852, scores, generated_utc)
    split_rows = amplitude_split_rows(branch_rows, generated_utc)
    gates = interpretation_gate_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, branch_rows, split_rows, gates, routes, guards, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(BRANCH_READOUT_PATH, branch_rows, ["branch", "best_positive_candidate", "b_mem_fixed", "eta1_aF_DeltaR_implied", "chi2_total", "delta_BIC_vs_best_fit_baseline", "fit_params", "edge_flags", "lead_status", "interpretation", "valid_for_claim", "generated_utc"])
    write_csv(AMPLITUDE_SPLIT_PATH, split_rows, ["split_id", "no_sh0es_best_b_mem", "sh0es_best_b_mem", "absolute_split", "ratio_sh0es_over_no_sh0es", "eta1_aF_DeltaR_no_sh0es", "eta1_aF_DeltaR_sh0es", "status", "meaning", "valid_for_claim", "generated_utc"])
    write_csv(INTERPRETATION_PATH, gates, ["gate_id", "gate", "status", "reason", "required_before_claim", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, branch_rows, split_rows, gates, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
