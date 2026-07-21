from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4637"
CLAIM_ID = "L-479"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_XIAB_ZERO_OR_NUMERIC_4637"
MARKER = "PPC4161_PARENT_XIAB_COEFFICIENT_ZERO_OR_NUMERIC_ROW_4637"
PACKET_MARKER = "PPC4161_PACKET_PARENT_XIAB_ZERO_OR_TAIL_BUDGET_4637"
DECISION = "VISIBLE_HILBERT_MAXWELL_XI_ZERO_IMPORTED_PRIVATE_BRANCH_XI_TAIL_BUDGET_NOW_LIVE_NONCLAIM"
NEXT_TARGET = "4638-Y5-R2FR-Xi-tail-bound-first-component-or-exact-zero.md"

DOC_PATH = POST / "4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md"
FORMAL_PATH = FORMAL / "653-PPC4161-parent-XiAB-coefficient-zero-or-numeric-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

CSV_4636_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4636_VALIDATION.csv"
CSV_4636_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4636_OBSERVABLE_XI_REDUCTION_ROWS.csv"
CSV_4636_ENVELOPE = SOURCE_DIR / "P8_Y5_R2FR_4636_R10_EPSILON_ENVELOPE_ROWS.csv"
CSV_4636_TARGETS = SOURCE_DIR / "P8_Y5_R2FR_4636_PARENT_COEFFICIENT_TARGET_ROWS.csv"
CSV_4636_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4636_NEXT_TARGET.csv"
CSV_4631_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4631_BRANCH_EXTREMUM_DERIVATION_ROWS.csv"
CSV_4632_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4632_IQ_SIGNATURE_HUNT_ROWS.csv"
CSV_4633_SIGNING = SOURCE_DIR / "P8_Y5_R2FR_4633_PARENT_SIGNING_MATRIX.csv"
CSV_4635_CURVE = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"

FW_185_HILBERT = FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md"
FW_226_VISIBLE_IMPORT = FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md"
FW_234_VISIBLE_EM = FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md"
FW_281_MATTER_DOMAIN = FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md"
FW_282_SOURCE_READOUT = FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md"
FW_332_VISIBLE_HILBERT = FORMAL / "332-PPC4161-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4637_SOURCE_REGISTER.csv"
ZERO_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_ZERO_BRANCH_IMPORT_AUDIT.csv"
XI_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_PARENT_XI_SPLIT_ROWS.csv"
TAIL_BUDGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_XI_TAIL_BUDGET_ROWS.csv"
NUMERIC_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_PARENT_XI_NUMERIC_ROW_SCHEMA.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_XI_TAIL_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4637_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4637_VALIDATION.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line_text in enumerate(read_text(path).splitlines(), start=1):
        if needle in line_text:
            return line_number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    separator = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + separator + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def load_curve_points() -> list[tuple[float, float]]:
    return sorted((float(row["lambda_m"]), float(row["alpha_bound_abs"])) for row in read_csv(CSV_4635_CURVE))


def interpolate_alpha(points: list[tuple[float, float]], lambda_m: float) -> float | None:
    if not points or lambda_m < points[0][0] or lambda_m > points[-1][0]:
        return None
    log_lambda = math.log10(lambda_m)
    for (left_lambda, left_alpha), (right_lambda, right_alpha) in zip(points, points[1:]):
        if left_lambda <= lambda_m <= right_lambda:
            left_log_lambda = math.log10(left_lambda)
            right_log_lambda = math.log10(right_lambda)
            fraction = 0.0 if abs(right_log_lambda - left_log_lambda) < 1.0e-15 else (log_lambda - left_log_lambda) / (right_log_lambda - left_log_lambda)
            log_alpha = math.log10(left_alpha) + fraction * (math.log10(right_alpha) - math.log10(left_alpha))
            return 10.0**log_alpha
    return points[-1][1]


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4637_00_4636_validation", CSV_4636_VALIDATION, "VAL4636_OVERALL", "4636 validation."),
        ("SRC4637_01_4636_reduction", CSV_4636_REDUCTION, "XI4636_0_define_observable_combo", "Xi_AB reduction."),
        ("SRC4637_02_4636_envelope", CSV_4636_ENVELOPE, "ENV4636_8", "100um envelope."),
        ("SRC4637_03_4636_targets", CSV_4636_TARGETS, "TGT4636_0_XiAB_direct", "parent Xi target."),
        ("SRC4637_04_4636_next", CSV_4636_NEXT, "4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md", "4636 selected 4637."),
        ("SRC4637_05_4631_derivation", CSV_4631_DERIVATION, "DER4631_1_beta_visible_zero", "conditional beta zero theorem."),
        ("SRC4637_06_4632_hunt", CSV_4632_HUNT, "HUNT4632_1_even_matter_scale", "parent signature missing."),
        ("SRC4637_07_4633_signing", CSV_4633_SIGNING, "SIGN4633_4_nonHilbert_guard", "non-Hilbert guard open."),
        ("SRC4637_08_hilbert_source", FW_185_HILBERT, "delta_ZH = 0", "Hilbert source-measure private branch."),
        ("SRC4637_09_visible_import", FW_226_VISIBLE_IMPORT, "S_vis =", "standard visible matter import."),
        ("SRC4637_10_visible_em", FW_234_VISIBLE_EM, "omega_visible_EM_residual", "visible EM residual zero theorem."),
        ("SRC4637_11_matter_domain", FW_281_MATTER_DOMAIN, "Dq_matter = 0", "matter-domain zero theorem."),
        ("SRC4637_12_source_readout", FW_282_SOURCE_READOUT, "Dq_source_readout = 0", "source-readout zero theorem."),
        ("SRC4637_13_visible_hilbert", FW_332_VISIBLE_HILBERT, "N_visible = 0", "visible Hilbert/EM integration."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line": line_of(path, needle),
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": now,
            }
        )
    return rows


def zero_audit_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "ZA4637_0_standard_visible_import",
            "component": "ordinary visible matter action domain",
            "evidence": str(FW_226_VISIBLE_IMPORT),
            "zero_result": "CONDITIONAL_PRIVATE_ZERO",
            "import_to_Xi": "Xi_visible_Hilbert=0 if S_vis has no direct m/hidden coefficient slot",
            "remaining_tax": "MTS-specific visible deformation terms remain in Xi_hidden_coeff if present",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "ZA4637_1_matter_domain",
            "component": "Dq_matter",
            "evidence": str(FW_281_MATTER_DOMAIN),
            "zero_result": "SIGNED_FOR_STANDARD_BRANCH_ONLY",
            "import_to_Xi": "ordinary matter has no independent parent-field source slot in this branch",
            "remaining_tax": "source weights, coefficient drift, worldtube/readout and hidden matter tails are retained",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "ZA4637_2_source_readout",
            "component": "Hilbert/ADM source readout",
            "evidence": str(FW_282_SOURCE_READOUT),
            "zero_result": "SIGNED_FOR_STANDARD_BRANCH_ONLY",
            "import_to_Xi": "post-solution Hilbert source readout is not a free Xi source",
            "remaining_tax": "coefficient owner and hidden source-current normalization are retained",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "ZA4637_3_visible_EM_Poynting",
            "component": "minimal Maxwell-Hodge/Poynting Hilbert stress",
            "evidence": str(FW_234_VISIBLE_EM),
            "zero_result": "CONDITIONAL_PRIVATE_ZERO",
            "import_to_Xi": "Xi_EM_minimal=0 when Poynting is counted once as Hilbert EM stress with same observed Hodge",
            "remaining_tax": "nonminimal F2/Hodge/current/radiative side channels remain in Xi_hidden_EM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "ZA4637_4_branch_extremum",
            "component": "full parent I_q/even A_m",
            "evidence": str(CSV_4631_DERIVATION),
            "zero_result": "PROVED_CONDITIONAL_PARENT_SIGNATURE_MISSING",
            "import_to_Xi": "would make Xi_AB=0 at first order if signed",
            "remaining_tax": "4632/4633 do not find the full parent signature",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "ZA4637_5_current_verdict",
            "component": "full Xi_AB",
            "evidence": str(CSV_4633_SIGNING),
            "zero_result": "PARTIAL_ZERO_ONLY_FULL_XI_ZERO_NOT_SIGNED",
            "import_to_Xi": "visible Hilbert/EM zero can be used inside the private standard branch",
            "remaining_tax": "Xi_tail = Xi_nonHilbert + Xi_hidden_coeff + Xi_boundary_history + Xi_transition_inner + Xi_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def xi_split_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "split_id": "XS4637_0_full_split",
            "definition": "Xi_AB = Xi_visible_Hilbert + Xi_EM_minimal + Xi_hidden_coeff + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner + Xi_source_weight",
            "status": "SPLIT_DERIVED_NO_CANCELLATION",
            "meaning": "R10 source coupling is decomposed into zero-importable standard pieces plus explicit live tails.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "split_id": "XS4637_1_private_standard_branch",
            "definition": "Xi_visible_Hilbert=0 and Xi_EM_minimal=0",
            "status": "CONDITIONAL_PRIVATE_ZERO_IMPORTED",
            "meaning": "Ordinary visible matter/Maxwell stress is not the live R10 problem inside the calibrated q-basic Hilbert branch.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "split_id": "XS4637_2_live_tail",
            "definition": "Xi_tail := Xi_hidden_coeff + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner + Xi_source_weight",
            "status": "LIVE_PARENT_TARGET",
            "meaning": "The next work is to prove Xi_tail=0 or bound |Xi_tail| by the 4636 R10 envelope.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "split_id": "XS4637_3_tail_bound_law",
            "definition": "|Xi_tail| <= |Xi_hidden_coeff| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| + |Xi_source_weight| <= alpha_bound(lambda_mem)",
            "status": "NUMERIC_BUDGET_READY_AFTER_LAMBDA",
            "meaning": "This turns the loose coupling problem into an absolute residual budget with no cancellation.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def tail_budget_rows(now: str, points: list[tuple[float, float]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, lambda_um in enumerate([30.0, 38.6, 50.0, 100.0, 200.0, 1000.0]):
        lambda_m = lambda_um * 1.0e-6
        alpha_bound = interpolate_alpha(points, lambda_m)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "budget_id": f"TB4637_{index}",
                "lambda_um": f"{lambda_um:.12g}",
                "lambda_m": f"{lambda_m:.12g}",
                "Xi_tail_total_max": "" if alpha_bound is None else f"{alpha_bound:.12g}",
                "tail_budget_law": "|Xi_hidden_coeff|+|Xi_nonHilbert|+|Xi_boundary_history|+|Xi_transition_inner|+|Xi_source_weight| <= Xi_tail_total_max",
                "interpretation": "after visible Hilbert/EM zero import, all live tail pieces must fit inside this absolute budget",
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        )
    return rows


def numeric_schema_rows(now: str) -> list[dict[str, Any]]:
    fields = [
        ("system_id", "local system/branch identifier", "required"),
        ("lambda_mem_m", "sqrt(Z_mem/M2_mem) from same parent branch", "required"),
        ("Xi_hidden_coeff", "hidden/nonminimal coefficient contribution", "required_or_zero_certificate"),
        ("Xi_nonHilbert", "non-Hilbert source contribution", "required_or_zero_certificate"),
        ("Xi_boundary_history", "boundary/history/flux contribution", "required_or_zero_certificate"),
        ("Xi_transition_inner", "transition or inner-source contribution", "required_or_zero_certificate"),
        ("Xi_source_weight", "source/species/readout weight contribution", "required_or_zero_certificate"),
        ("Xi_tail_total_abs_bound", "absolute sum of the live components", "computed"),
        ("source_path", "path to parent derivation or data source", "required"),
        ("valid_for_claim", "true only after every component is numeric or zero-certified", "false_now"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "schema_id": f"XSCH4637_{index}",
            "field": field,
            "meaning": meaning,
            "requirement": requirement,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for index, (field, meaning, requirement) in enumerate(fields)
    ]


def runner_rows(now: str, points: list[tuple[float, float]]) -> list[dict[str, Any]]:
    scenarios = [
        ("RUN4637_0_current_live", None, None, "FAIL_CLOSED_MISSING_XI_TAIL_AND_LAMBDA", "current branch has no parent Xi_tail/lambda row"),
        ("RUN4637_1_visible_EM_zero_all_tail_zero", 0.0, 1000.0e-6, "CONDITIONAL_EXACT_ZERO_PASS_ALGEBRA_ONLY", "if all live tails are also zero, R10 is silent"),
        ("RUN4637_2_tail_0p05_at_100um", 0.05, 100.0e-6, "EVALUATE", "tail below 100um envelope"),
        ("RUN4637_3_tail_0p1_at_100um", 0.1, 100.0e-6, "EVALUATE", "tail above 100um envelope"),
        ("RUN4637_4_tail_0p02_at_1mm", 0.02, 1000.0e-6, "EVALUATE", "tail just above 1mm envelope"),
        ("RUN4637_5_tail_0p01_at_1mm", 0.01, 1000.0e-6, "EVALUATE", "tail below 1mm envelope"),
        ("RUN4637_6_order_one_tail_at_30um", 1.0, 30.0e-6, "EVALUATE", "short-range order-one tail smoke"),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, xi_tail, lambda_m, preset, reason in scenarios:
        alpha_bound = interpolate_alpha(points, lambda_m) if lambda_m is not None else None
        if preset != "EVALUATE":
            result = preset
        elif alpha_bound is None:
            result = "FAIL_CLOSED_LAMBDA_OUTSIDE_CURVE"
        elif xi_tail is not None and xi_tail <= alpha_bound:
            result = "PASS_TAIL_ENVELOPE_SMOKE_ONLY_NONCLAIM"
        else:
            result = "FAIL_TAIL_ABOVE_R10_ENVELOPE"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "run_id": run_id,
                "Xi_tail_abs": "MISSING_PARENT_TAIL_ROW" if xi_tail is None else f"{xi_tail:.12g}",
                "lambda_mem_m": "MISSING_PARENT_HESSIAN_RATIO" if lambda_m is None else f"{lambda_m:.12g}",
                "alpha_bound_vector": "" if alpha_bound is None else f"{alpha_bound:.12g}",
                "result": result,
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        )
    return rows


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4637_0_private_branch_not_global_claim",
            "rule": "Visible Hilbert/EM zero imports are private standard-branch clauses, not global MTS proof.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4637_1_no_tail_cancellation",
            "rule": "Xi_tail components are absolute-summed; no hidden cancellation may be used to pass R10.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4637_2_no_R10_to_WEP_shortcut",
            "rule": "Even if Xi_tail passes R10, WEP/PPN still require split/composition/projection rows.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4637_0_Xi_tail",
            "blocks": "finite R10/local-G source coupling branch",
            "missing": "zero certificate or numeric absolute bound for Xi_hidden_coeff, Xi_nonHilbert, Xi_boundary_history, Xi_transition_inner and Xi_source_weight",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4637_1_lambda_mem",
            "blocks": "use of the R10 curve at a parent range",
            "missing": "parent M2_mem/Z_mem ratio or exact source-zero theorem",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4637_2_full_local_GR",
            "blocks": "local-GR/Newton/PPN claim",
            "missing": "global parent adoption, WEP/PPN split, metric EH limit, source mass readout and curve QA promotion",
            "next_action": "do not promote; continue tail/metric/source proof chain",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4637_0",
            "decision": DECISION,
            "meaning": "The R10 Xi problem is narrowed: ordinary visible matter and minimal Maxwell/Poynting are not the live coupling leak inside the private calibrated Hilbert branch. The live target is the explicit Xi_tail residual budget.",
            "status": "NONCLAIM_PARTIAL_ZERO_AND_TAIL_BUDGET_READY",
            "best_route": "try exact-zero for the largest Xi_tail component first; otherwise fill one numeric tail row and compare to the 4636 envelope",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "status": "PASS_NONCLAIM_ARTIFACTS_WRITTEN",
            "github_action": "NONE_LOCAL_ONLY",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "Xi_tail is now the live coupling problem; attack the first component zero/bound instead of re-auditing the whole matter sector.",
            "timestamp_utc": now,
        }
    ]


def has_any_claim(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def validation_rows(
    sources: list[dict[str, Any]],
    zero_audit: list[dict[str, Any]],
    split: list[dict[str, Any]],
    tail_budget: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups = [sources, zero_audit, split, tail_budget, schema, runner, controls, blockers, decisions, status, next_target]
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL4637_00_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in sources), "all cited paths/needles found")
    csv_paths = [
        SOURCE_REGISTER,
        ZERO_AUDIT_CSV,
        XI_SPLIT_CSV,
        TAIL_BUDGET_CSV,
        NUMERIC_SCHEMA_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    csv_ok = True
    details = []
    for csv_path in csv_paths:
        try:
            details.append(f"{csv_path.name}:{len(read_csv(csv_path))}")
        except csv.Error as exc:
            csv_ok = False
            details.append(f"{csv_path.name}:CSV_ERROR:{exc}")
    add("VAL4637_01_csv_parse", csv_ok, ";".join(details))
    add("VAL4637_02_partial_zero_imported", any(row["zero_result"] == "PARTIAL_ZERO_ONLY_FULL_XI_ZERO_NOT_SIGNED" for row in zero_audit), "partial zero verdict present")
    add("VAL4637_03_Xi_tail_split_present", any(row["split_id"] == "XS4637_2_live_tail" for row in split), "Xi_tail live target present")
    add("VAL4637_04_tail_budget_key_lambdas", {"38.6", "100", "1000"}.issubset({row["lambda_um"] for row in tail_budget}), "tail budgets include 38.6, 100 and 1000 um")
    add("VAL4637_05_schema_fields_present", {"Xi_hidden_coeff", "Xi_nonHilbert", "Xi_tail_total_abs_bound", "source_path"}.issubset({row["field"] for row in schema}), "numeric schema has core tail fields")
    add("VAL4637_06_runner_controls", any(row["result"].startswith("PASS") for row in runner) and any(row["result"].startswith("FAIL_TAIL") for row in runner) and any(row["result"] == "FAIL_CLOSED_MISSING_XI_TAIL_AND_LAMBDA" for row in runner), "runner has live fail and pass/fail controls")
    add("VAL4637_07_all_rows_nonclaim", not any(has_any_claim(group) for group in groups), "no generated row promotes a claim")
    add("VAL4637_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4637_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4637_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4637_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4637_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4637_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4637_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4637_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4637_OVERALL", all(row["status"] == "PASS" for row in checks), "4637 parent Xi tail checkpoint")
    return checks


def write_docs(
    now: str,
    sources: list[dict[str, Any]],
    zero_audit: list[dict[str, Any]],
    split: list[dict[str, Any]],
    tail_budget: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> None:
    body = f"""# 4637 - Parent XiAB Coefficient Zero Or Numeric Row

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

4637 narrows the coupling problem.

From 4636, R10 asks for:

`|Xi_AB| <= alpha_bound(lambda_mem)`.

The parent split is now:

`Xi_AB = Xi_visible_Hilbert + Xi_EM_minimal + Xi_tail`.

Inside the private calibrated Hilbert branch, the ordinary visible matter piece and minimal Maxwell/Poynting Hilbert-stress piece are conditionally zero:

`Xi_visible_Hilbert = 0`, `Xi_EM_minimal = 0`.

The live problem is therefore:

`Xi_tail = Xi_hidden_coeff + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner + Xi_source_weight`.

This is not a final claim. It is a real narrowing: stop treating all matter coupling as mysterious, and attack/bound the tail components one by one.

## Source Register

{markdown_table(sources)}

## Zero Branch Import Audit

{markdown_table(zero_audit)}

## Parent Xi Split

{markdown_table(split)}

## Tail Budgets

{markdown_table(tail_budget)}

## Numeric Row Schema

{markdown_table(schema)}

## Runner Results

{markdown_table(runner)}

## Controls

{markdown_table(controls)}

## Blockers

{markdown_table(blockers)}

## Decision

{markdown_table(decisions)}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, body)
    formal_body = f"""# 653 - PPC4161 Parent XiAB Coefficient Zero Or Numeric Row

Marker: `{MARKER}`

Source checkpoint: `{DOC_PATH}`

4637 imports the private calibrated Hilbert/visible/Maxwell zero branches into the R10 `Xi_AB` problem without overclaiming them. The ordinary visible Hilbert piece and minimal Maxwell/Poynting Hilbert-stress piece can be zero on the standard branch. The live R10 coefficient is therefore the explicit no-cancellation tail:

`Xi_tail = Xi_hidden_coeff + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner + Xi_source_weight`.

At `100 um`, the tail budget is about `0.0756`; at `1 mm`, about `0.0191`, using the 4635 vector curve. Next work should target a real zero/bound for one tail component, not re-audit the whole matter sector.

Decision: `{DECISION}`.

Next: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, formal_body)


def append_integrations() -> None:
    spine_block = f"""
## PPC4161 Parent XiAB Coefficient Zero Or Numeric Row 4637

Marker: `{MARKER}`

4637 narrows the R10 coupling bottleneck. In the private calibrated Hilbert branch, ordinary visible matter and minimal Maxwell/Poynting Hilbert stress do not supply the live `Xi_AB` leak. The remaining coefficient is an explicit no-cancellation tail: `Xi_tail = Xi_hidden_coeff + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner + Xi_source_weight`. R10 now gives numeric budgets for that tail at each `lambda_mem`.

Next: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)
    packet_block = f"""
## PPC4161 Packet - Parent XiAB Zero Or Tail Budget 4637

Marker: `{PACKET_MARKER}`

Local packet update: the coupling problem is no longer the entire visible matter sector. The useful live target is `Xi_tail`, with absolute budgets from the R10 curve. Attack one tail component next.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def append_claim_register() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "area": "local_gr_empirical_interface",
        "claim": "4637 imports private visible Hilbert/Maxwell zero branches into the R10 Xi_AB split and reduces the live coupling problem to an explicit Xi_tail budget.",
        "support": "Generated source register, zero-branch import audit, Xi split rows, tail budgets, numeric schema, runner results, controls, blockers, decision, status, next target and validation.",
        "status": "parent_Xi_tail_budget_nonclaim",
        "next": NEXT_TARGET,
        "risk": "Treating private visible/EM zero imports as global MTS proof, or using cancellation between tail components.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_path": NEXT_TARGET,
        "notes": "No local-GR/Newton/R10/PPN claim until Xi_tail and lambda_mem are zero-certified or source-backed and projection gates close.",
    }
    file_exists = CLAIMS_PATH.exists()
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists or CLAIMS_PATH.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    now = utc_now()
    points = load_curve_points()
    sources = source_rows(now)
    zero_audit = zero_audit_rows(now)
    split = xi_split_rows(now)
    tail_budget = tail_budget_rows(now, points)
    schema = numeric_schema_rows(now)
    runner = runner_rows(now, points)
    controls = control_rows(now)
    blockers = blocker_rows(now)
    decisions = decision_rows(now)
    status = status_rows(now)
    next_target = next_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT_CSV, zero_audit)
    write_csv(XI_SPLIT_CSV, split)
    write_csv(TAIL_BUDGET_CSV, tail_budget)
    write_csv(NUMERIC_SCHEMA_CSV, schema)
    write_csv(RUNNER_CSV, runner)
    write_csv(CONTROL_CSV, controls)
    write_csv(BLOCKERS_CSV, blockers)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    write_docs(now, sources, zero_audit, split, tail_budget, schema, runner, controls, blockers, decisions)
    append_integrations()
    append_claim_register()

    validation = validation_rows(sources, zero_audit, split, tail_budget, schema, runner, controls, blockers, decisions, status, next_target)
    write_csv(VALIDATION_CSV, validation)
    print(f"wrote {DOC_PATH}")
    print(f"validation {VALIDATION_CSV}")
    print(f"next {NEXT_TARGET}")


if __name__ == "__main__":
    main()
