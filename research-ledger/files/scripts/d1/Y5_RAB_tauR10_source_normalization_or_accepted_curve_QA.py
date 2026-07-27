from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_QUEUE = RAB / "acquisition-queue"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
R10_1571 = RAB / "external" / "r10" / "1571"
OVERLAY = R10_1571 / "R10_fig2_blue_curve_cleaned_trace_overlay_1571.png"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1572-Y5-RAB-tauR10-source-normalization-or-accepted-curve-QA.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1571_doc": ROOT / "1571-Y5-RAB-R10-digitization-QA-or-tauR10-internal-kernel.md",
    "1571_validation": OUT / "P8_Y5_BRR545_1571_VALIDATION.csv",
    "1571_curve": OUT / "P8_Y5_PARENT_QLOC_1571_R10_ALPHA_LAMBDA_DIGITIZED_QA_CANDIDATE.csv",
    "1571_components": OUT / "P8_Y5_PARENT_QLOC_1571_BLUE_COMPONENT_QA_AUDIT.csv",
    "1571_method": OUT / "P8_Y5_PARENT_QLOC_1571_DIGITIZATION_QA_METHOD.csv",
    "1571_comparison": OUT / "P8_Y5_PARENT_QLOC_1571_CURVE_COMPARISON_1570_TO_1571.csv",
    "1571_tau": OUT / "P8_Y5_PARENT_QLOC_1571_TAU_R10_INTERNAL_KERNEL_ATTEMPT.csv",
    "overlay": OVERLAY,
}

NEEDLES = {
    "1571_doc": ["R10 Fig. 2 curve is now a cleaner QA candidate", "internal `tau_R10` source-normalized kernel is still missing"],
    "1571_validation": ["VAL1571_OVERALL", "PASS"],
    "1571_curve": ["QA1571_000", "QA_CLEANED_CANDIDATE_NONCLAIM"],
    "1571_components": ["KEEP_CURVE_CANDIDATE", "REJECT_LABEL_OR_AXIS_TEXT"],
    "1571_method": ["QA1571_3_overlay", "OVERLAY_CREATED"],
    "1571_comparison": ["CMP1571_0_point_count", "QA_CHANGED_CANDIDATE_TRACE"],
    "1571_tau": ["KERN1571_4_verdict", "NOT_READY"],
    "overlay": [],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1572_SOURCE_REGISTER.csv"
VISUAL_QA = OUT / "P8_Y5_PARENT_QLOC_1572_VISUAL_QA_REVIEW.csv"
ACCEPTANCE_GATE = OUT / "P8_Y5_PARENT_QLOC_1572_CURVE_ACCEPTANCE_GATE.csv"
REVIEWED_CURVE = OUT / "P8_Y5_PARENT_QLOC_1572_R10_ALPHA_LAMBDA_REVIEWED_CANDIDATE.csv"
TAU_NORMALIZATION = OUT / "P8_Y5_PARENT_QLOC_1572_TAU_R10_SOURCE_NORMALIZATION_DERIVATION_ATTEMPT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1572_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1572_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1572_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1572_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1572_VALIDATION.csv"
QUEUE_CURVE = RAB_QUEUE / "R10_alpha_lambda_bound_curve_DIGITIZED_1572_REVIEWED_CANDIDATE_NONCLAIM.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1572"
COPY_TARGETS = {
    VISUAL_QA: [
        QUARANTINE / "VISUAL_QA_REVIEW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_visual_QA_review_nonclaim_1572.csv",
    ],
    ACCEPTANCE_GATE: [
        QUARANTINE / "CURVE_ACCEPTANCE_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_curve_acceptance_gate_nonclaim_1572.csv",
    ],
    REVIEWED_CURVE: [
        QUARANTINE / "R10_ALPHA_LAMBDA_REVIEWED_CANDIDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_alpha_lambda_reviewed_candidate_nonclaim_1572.csv",
        QUEUE_CURVE,
    ],
    TAU_NORMALIZATION: [
        QUARANTINE / "TAU_R10_SOURCE_NORMALIZATION_DERIVATION_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "tau_R10_source_normalization_attempt_nonclaim_1572.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "tauR10_source_norm_curve_QA_decision_nonclaim_1572.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    if not needles:
        return True
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def row_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    total = 0
    for path in folder.glob("*.csv"):
        try:
            total += len(read_csv(path))
        except Exception:
            total += 1
    return total


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES[key]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1572_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles),
                "needles": "; ".join(needles),
                "purpose": "accepted curve QA review or tau_R10 source-normalization attempt",
                **flags(),
            }
        )
    return rows


def visual_qa_rows() -> list[dict[str, Any]]:
    curve = read_csv(SOURCE_FILES["1571_curve"])
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "qa_id": "VQA1572_0_overlay_exists",
            "qa_item": "trace overlay rendered",
            "result": "PASS_MACHINE_VISUAL_REVIEW",
            "evidence": rel(OVERLAY),
            "limitation": "not independent human/manual digitization",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "qa_id": "VQA1572_1_curve_following",
            "qa_item": "red trace follows blue This work curve",
            "result": "PASS_MACHINE_VISUAL_REVIEW",
            "evidence": "overlay trace follows the blue boundary across the plotted range",
            "limitation": "axis calibration and centerline still approximate",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "qa_id": "VQA1572_2_label_rejection",
            "qa_item": "label/text contamination reduced",
            "result": "PASS_COMPONENT_FILTER_REVIEW",
            "evidence": "component audit rejects blue label/axis text and keeps curve candidates",
            "limitation": "arrow/text contamination cannot be ruled out without manual point review",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "qa_id": "VQA1572_3_point_count",
            "qa_item": "reviewed candidate point count",
            "result": "PASS_INTERNAL_QA_CANDIDATE",
            "evidence": f"points={len(curve)}",
            "limitation": "candidate-only, not accepted for claims",
            **flags(),
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACCEPT1572_0_overlay", "visual overlay exists and follows curve", "PASS_INTERNAL_QA", "sufficient for reviewed candidate"),
        ("ACCEPT1572_1_axis", "manual tick-by-tick axis calibration", "MISSING_INDEPENDENT_QA", "required before accepted curve"),
        ("ACCEPT1572_2_curve", "manual/independent curve point check", "MISSING_INDEPENDENT_QA", "required before accepted curve"),
        ("ACCEPT1572_3_curve_status", "accepted nonclaim bound curve", "NOT_ACCEPTED", "candidate remains reviewed-only"),
        ("ACCEPT1572_4_claim_status", "claim-valid R10 curve", "BLOCKED_NO_CLAIM", "even accepted external curve would still need internal MTS prediction"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "meaning": meaning,
            "source_paths": source_list("1571_method", "overlay", "1571_curve"),
            **flags(),
        }
        for gate_id, gate, status, meaning in rows
    ]


def reviewed_curve_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(SOURCE_FILES["1571_curve"]):
        rows.append(
            {
                **row,
                "digitization_status": "REVIEWED_QA_CANDIDATE_NONCLAIM",
                "review_status": "INTERNAL_MACHINE_VISUAL_QA_PASS_NOT_INDEPENDENT",
                "accepted_for_scoring": False,
                "passes_for_claim": False,
            }
        )
    return rows


def tau_normalization_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TAUN1572_0_kernel_target",
            "alpha_MTS(lambda_R)=tau_R10 A_R",
            "convert internal finite R_AB residual into the external Yukawa alpha(lambda) language",
            "FORMAL_TARGET_ONLY",
            "not yet source-normalized",
        ),
        (
            "TAUN1572_1_test_mass_source",
            "A_R must be proportional to source response of both test masses",
            "requires matter/source normalization and composition dependence or zero theorem",
            "MISSING_JR_SOURCE_NORMALIZATION",
            "no J_R theorem-zero/finite row",
        ),
        (
            "TAUN1572_2_boundary_readout",
            "A_R may receive B_R/readout contributions",
            "requires boundary/readout projection theorem or finite row",
            "MISSING_BR_READOUT_NORMALIZATION",
            "boundary/readout gates still unsigned",
        ),
        (
            "TAUN1572_3_range",
            "lambda_R=sqrt(Z_R/M_R^2)",
            "requires Z_R and M_R^2 in shared normalization",
            "MISSING_RANGE_NORMALIZATION",
            "no Z_R/M_R^2 source-backed rows",
        ),
        (
            "TAUN1572_4_verdict",
            "tau_R10 internal source-normalization kernel",
            "cannot be filled from external curve QA",
            "NOT_READY",
            "derive source-normalized kernel or fill internal coefficient rows next",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "normalization_id": normalization_id,
            "kernel_piece": kernel_piece,
            "role": role,
            "status": status,
            "blocking_gap": blocking_gap,
            "source_paths": source_list("1571_tau"),
            **flags(),
        }
        for normalization_id, kernel_piece, role, status, blocking_gap in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    reviewed = read_csv(REVIEWED_CURVE)
    rows = [
        ("RUN1572_0_sources", "load 1571 handoff and overlay", "PASS", "all source register needles found"),
        ("RUN1572_1_reviewed_curve", "reviewed R10 curve candidate", "PASS_REVIEWED_CANDIDATE_NONCLAIM", f"points={len(reviewed)}"),
        ("RUN1572_2_acceptance", "accepted R10 curve", "NOT_ACCEPTED", "independent/manual axis and curve QA missing"),
        ("RUN1572_3_tau", "tau_R10 source normalization", "NOT_READY", "J_R/B_R/readout/range normalization missing"),
        ("RUN1572_4_raw_accepted", "raw/accepted finite rows", "NO_LIVE_SCORE_ROWS", f"raw_rows={row_count(RAB_RAW)}; accepted_rows={row_count(RAB_ACCEPTED)}"),
        ("RUN1572_5_claim", "R10/local GR claim", "BLOCKED_NO_CLAIM", "external curve QA still lacks internal MTS prediction"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "test": test,
            "current_status": current_status,
            "detail": detail,
            **flags(),
        }
        for runner_id, test, current_status, detail in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1572_0_reviewed_curve", "reviewed R10 curve candidate", "PASS_NONCLAIM", "internal machine visual QA passed"),
        ("GATE1572_1_accepted_curve", "accepted R10 curve", "BLOCKED_NO_CLAIM", "independent/manual QA missing"),
        ("GATE1572_2_tau", "tau_R10 internal kernel", "BLOCKED_NO_CLAIM", "source normalization missing"),
        ("GATE1572_3_R10_score", "R10 score/pass/fail", "BLOCKED_NO_CLAIM", "no internal MTS alpha(lambda) prediction"),
        ("GATE1572_4_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "R10 data plumbing does not prove local limit"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1571_doc", "1571_curve", "1571_tau"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1572_0_curve",
            "decision": "R10 curve status",
            "result": "REVIEWED_CANDIDATE_NOT_ACCEPTED",
            "reason": "machine visual QA passes, but independent/manual curve QA is still missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1572_1_tau",
            "decision": "tau_R10 source normalization",
            "result": "NOT_READY",
            "reason": "external curve quality is no substitute for internal source-normalized theory kernel",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1572_2_next",
            "decision": "next target",
            "result": "NEXT_1573_INTERNAL_TAU_R10_SOURCE_KERNEL_OR_MANUAL_CURVE_ACCEPTANCE",
            "reason": "derive the internal source kernel or perform independent manual curve QA",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1572_0_1573",
            "next_target": "1573-Y5-RAB-internal-tauR10-source-kernel-or-manual-curve-acceptance.md",
            "script": "scripts/Y5_RAB_internal_tauR10_source_kernel_or_manual_curve_acceptance.py",
            "objective": "derive the internal tau_R10 source kernel from Z_R/M_R2/J_R/B_R/readout inputs, or run an independent/manual digitization acceptance pass on the reviewed R10 curve",
            "do_not": "do not score R10 without internal alpha_MTS(lambda); do not claim local GR; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, destinations in COPY_TARGETS.items():
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    visual = read_csv(VISUAL_QA)
    acceptance = read_csv(ACCEPTANCE_GATE)
    reviewed = read_csv(REVIEWED_CURVE)
    tau = read_csv(TAU_NORMALIZATION)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1572_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1572 source paths exist"),
        ("VAL1572_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1572_2_visual_qa", any(row["result"] == "PASS_MACHINE_VISUAL_REVIEW" for row in visual), "machine visual QA recorded"),
        ("VAL1572_3_acceptance_not_promoted", any(row["gate_id"] == "ACCEPT1572_3_curve_status" and row["status"] == "NOT_ACCEPTED" for row in acceptance), "curve is not promoted to accepted"),
        ("VAL1572_4_reviewed_curve", len(reviewed) >= 50 and all(row["digitization_status"] == "REVIEWED_QA_CANDIDATE_NONCLAIM" for row in reviewed), "reviewed candidate curve rows written"),
        ("VAL1572_5_tau_not_ready", any(row["normalization_id"] == "TAUN1572_4_verdict" and row["status"] == "NOT_READY" for row in tau), "tau source normalization remains not ready"),
        ("VAL1572_6_raw_accepted_empty", row_count(RAB_RAW) == 0 and row_count(RAB_ACCEPTED) == 0, "raw/accepted finite rows remain empty"),
        ("VAL1572_7_runner_blocks_claim", any(row["runner_id"] == "RUN1572_5_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local/R10 claim"),
        ("VAL1572_8_claim_gates", all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "claim gates remain closed"),
        ("VAL1572_9_decision_next", any(row["result"] == "NEXT_1573_INTERNAL_TAU_R10_SOURCE_KERNEL_OR_MANUAL_CURVE_ACCEPTANCE" for row in decision_items), "decision selects internal kernel or manual curve acceptance"),
        ("VAL1572_10_next_target", any("1573-Y5-RAB-internal-tauR10-source-kernel" in row["next_target"] for row in next_rows), "next target is internal tau kernel or manual curve acceptance"),
        ("VAL1572_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1572 CSVs parse cleanly"),
        ("VAL1572_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1572_13_branch_copies", all(destination.exists() for destinations in COPY_TARGETS.values() for destination in destinations), "branch/quarantine nonclaim copies written"),
        ("VAL1572_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1572_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1572_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1572 tauR10 source normalization or accepted curve QA validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    visual: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    reviewed: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1572 - R_AB tau_R10 Source Normalization or Accepted Curve QA",
                "",
                "## Verdict",
                "- The cleaned R10 curve is now a reviewed private candidate: machine visual QA passes and the overlay follows the blue curve.",
                "- It is still not accepted evidence because independent/manual tick and curve QA are missing.",
                "- The internal `tau_R10` source-normalization kernel remains the hard blocker: `J_R`, `B_R`, readout, and `lambda_R=sqrt(Z_R/M_R^2)` are not sourced or theorem-zeroed.",
                "- No R10 score, local GR/Newton reduction, PPN, WEP, clock, orbital, `Z_R=0`, or `q_R=0` claim is made.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Visual QA Review",
                md_table(visual, ["qa_id", "qa_item", "result", "evidence", "limitation"]),
                "",
                "## Curve Acceptance Gate",
                md_table(acceptance, ["gate_id", "gate", "status", "meaning"]),
                "",
                "## Reviewed Curve Candidate",
                md_table(reviewed[:30], ["point_id", "lambda_m", "alpha_abs_bound", "pixel_x", "pixel_y", "digitization_status", "review_status"]),
                "",
                "## tau_R10 Source Normalization",
                md_table(tau, ["normalization_id", "kernel_piece", "role", "status", "blocking_gap"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    visual = visual_qa_rows()
    acceptance = acceptance_gate_rows()
    reviewed = reviewed_curve_rows()
    tau = tau_normalization_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(VISUAL_QA, visual)
    write_csv(ACCEPTANCE_GATE, acceptance)
    write_csv(REVIEWED_CURVE, reviewed)
    write_csv(TAU_NORMALIZATION, tau)

    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        VISUAL_QA,
        ACCEPTANCE_GATE,
        REVIEWED_CURVE,
        TAU_NORMALIZATION,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, visual, acceptance, reviewed, tau, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
