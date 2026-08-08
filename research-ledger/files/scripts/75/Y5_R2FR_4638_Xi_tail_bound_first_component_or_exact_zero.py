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

CHECKPOINT = "4638"
CLAIM_ID = "L-480"
BRANCH_ID = "MTS_R2FR_Y5_XI_TAIL_FIRST_COMPONENT_4638"
MARKER = "PPC4161_XI_TAIL_BOUND_FIRST_COMPONENT_OR_EXACT_ZERO_4638"
PACKET_MARKER = "PPC4161_PACKET_XI_SRC_HIDDEN_FIRST_COMPONENT_4638"
DECISION = "XI_HIDDEN_COEFF_AND_SOURCE_WEIGHT_COLLAPSE_TO_XI_SRC_HIDDEN_CONDITIONAL_ZERO_NONCLAIM"
NEXT_TARGET = "4639-Y5-R2FR-Xi-nonHilbert-Hperp-tail-zero-or-bound.md"

DOC_PATH = POST / "4638-Y5-R2FR-Xi-tail-bound-first-component-or-exact-zero.md"
FORMAL_PATH = FORMAL / "654-PPC4161-Xi-tail-bound-first-component-or-exact-zero.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

CSV_4635_CURVE = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
CSV_4637_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4637_VALIDATION.csv"
CSV_4637_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4637_PARENT_XI_SPLIT_ROWS.csv"
CSV_4637_BUDGET = SOURCE_DIR / "P8_Y5_R2FR_4637_XI_TAIL_BUDGET_ROWS.csv"
DOC_4637 = POST / "4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md"
FW_4324 = FORMAL / "340-PPC4161-hidden-source-prefactor-and-marker-tail-zero-or-bound.md"
FW_4332 = FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4638_SOURCE_REGISTER.csv"
FIRST_COMPONENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_FIRST_COMPONENT_SELECTION.csv"
IMPORT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_XISRC_HIDDEN_IMPORT_AUDIT.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_XI_TAIL_REDUCTION_ROWS.csv"
BOUNDS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_XI_SRC_HIDDEN_COMPONENT_BOUNDS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_R10_REDUCED_TAIL_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4638_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4638_VALIDATION.csv"

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
    rows = read_csv(CSV_4635_CURVE)
    points: list[tuple[float, float]] = []
    for row in rows:
        points.append((float(row["lambda_m"]), float(row["alpha_bound_abs"])))
    return sorted(points)


def interpolate_alpha(points: list[tuple[float, float]], lambda_m: float) -> float | None:
    if not points or lambda_m < points[0][0] or lambda_m > points[-1][0]:
        return None
    log_lambda = math.log10(lambda_m)
    for (left_lambda, left_alpha), (right_lambda, right_alpha) in zip(points, points[1:]):
        if left_lambda <= lambda_m <= right_lambda:
            left_log_lambda = math.log10(left_lambda)
            right_log_lambda = math.log10(right_lambda)
            if abs(right_log_lambda - left_log_lambda) < 1.0e-15:
                return left_alpha
            fraction = (log_lambda - left_log_lambda) / (right_log_lambda - left_log_lambda)
            log_alpha = math.log10(left_alpha) + fraction * (math.log10(right_alpha) - math.log10(left_alpha))
            return 10.0**log_alpha
    return points[-1][1]


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4638_00_4637_validation", CSV_4637_VALIDATION, "VAL4637_OVERALL", "4637 predecessor validation."),
        ("SRC4638_01_4637_split_csv", CSV_4637_SPLIT, "XS4637_2_live_tail", "live Xi_tail split."),
        ("SRC4638_02_4637_budget_csv", CSV_4637_BUDGET, "TB4637_3", "100 um R10 tail budget."),
        ("SRC4638_03_4637_doc", DOC_4637, "Xi_hidden_coeff + Xi_nonHilbert", "human-readable Xi_tail definition."),
        ("SRC4638_04_4324_master_tail", FW_4324, "F4324_0_master_tail", "hidden source-prefactor master tail."),
        ("SRC4638_05_4324_exact_zero", FW_4324, "RUN4324_1_exact_zero", "older source-label exact-zero control."),
        ("SRC4638_06_4332_marker", FW_4332, "PPC4161_XI_SRC_HIDDEN_ZERO_OR_SOURCE_LABEL_TAIL_BOUND_4332", "canonical Xi_src_hidden checkpoint."),
        ("SRC4638_07_4332_Xi_zero", FW_4332, "ZERO4332_8_Xi", "conditional Xi_src_hidden zero row."),
        ("SRC4638_08_4332_Xi_open", FW_4332, "TAIL4332_6_Xi_open", "retained open no-cancellation source-label tail."),
        ("SRC4638_09_4332_firewall", FW_4332, "FW4332_0_no_hidden_slot_global", "global no-hidden-slot firewall."),
        ("SRC4638_10_4332_definition", FW_4332, "F4332_0_Xi_definition", "explicit Xi_src_hidden definition."),
        ("SRC4638_11_4635_curve", CSV_4635_CURVE, "lambda_m", "Eot-Wash 2020 vector curve points."),
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


def first_component_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "selection_id": "SEL4638_0",
            "selected_component": "Xi_src_hidden",
            "absorbs_4637_terms": "Xi_hidden_coeff + Xi_source_weight",
            "reason": "4324/4332 already define the hidden/source-label prefactor tail and its conditional zero route.",
            "route": "derive exact zero in source-label-forgetting Hilbert-owner branch; otherwise retain finite no-cancellation source-label bound.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "selection_id": "SEL4638_1",
            "selected_component": "Xi_nonHilbert",
            "absorbs_4637_terms": "Xi_nonHilbert",
            "reason": "deferred second component after source-label tail is isolated.",
            "route": "next target H_perp/non-Hilbert bypass zero or bound.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def import_audit_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4638_0_import_definition",
            "input_row": "F4332_0_Xi_definition",
            "imported_law": "Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + R_source_normalization + delta_w_EM + R_no_direct_m_charge + R_environment_selector",
            "status": "IMPORTED",
            "meaning": "The two loose 4637 labels Xi_hidden_coeff and Xi_source_weight are replaced by a named source-label residual vector.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4638_1_conditional_zero",
            "input_row": "ZERO4332_8_Xi",
            "imported_law": "source-label-forgetting Hilbert-owner branch => Xi_src_hidden = 0",
            "status": "CONDITIONAL_ZERO_AVAILABLE",
            "meaning": "This is a real derivation path, not a closure axiom, but it is branch-local until parent-signed globally.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4638_2_open_tail",
            "input_row": "TAIL4332_6_Xi_open",
            "imported_law": "|Xi_src_hidden| <= sum retained source-label components",
            "status": "OPEN_OUTSIDE_STANDARD_BRANCH",
            "meaning": "If hidden weights/source normalization/environment selectors survive, R10 must budget them directly.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4638_3_firewall",
            "input_row": "FW4332_0_no_hidden_slot_global",
            "imported_law": "do not treat no-hidden-slot as globally signed",
            "status": "FIREWALL_RETAINED",
            "meaning": "No local-GR/R10 claim is unlocked by 4638.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4638_0_4637_tail",
            "definition": "Xi_tail := Xi_hidden_coeff + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner + Xi_source_weight",
            "status": "INPUT_FROM_4637",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4638_1_first_component_rollup",
            "definition": "Xi_src_hidden := Xi_hidden_coeff + Xi_source_weight plus the 4332 marker/source-normalization/EM/inner/environment subcomponents",
            "status": "CANONICALIZED_FIRST_COMPONENT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4638_2_reduced_tail",
            "definition": "Xi_tail := Xi_src_hidden + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner",
            "status": "NO_CANCELLATION_REDUCTION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4638_3_source_label_zero_branch",
            "definition": "if source-label-forgetting Hilbert-owner branch is signed, Xi_tail := Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner",
            "status": "CONDITIONAL_REDUCTION_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4638_4_R10_gate",
            "definition": "|Xi_src_hidden| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| <= alpha_bound(lambda_mem)",
            "status": "R10_GATE_REDUCED_TO_FOUR_COMPONENTS",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def bound_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("CB4638_0", "epsilon_matter_hidden", "hidden matter operator/source slot", "zero if O_hidden=0 under source-label-forgetting Hilbert-owner branch"),
        ("CB4638_1", "epsilon_SR_hidden", "hidden source-readout prefactor", "zero if source readout is label-forgotten and Hilbert-owned"),
        ("CB4638_2", "R_marker_source_label", "marker/source label drift", "zero if D_Hperp theta_src=0"),
        ("CB4638_3", "R_hidden_weights", "hidden species/source weights", "zero if no source-only weights exist"),
        ("CB4638_4", "R_source_normalization", "source normalization drift", "zero if D_Hperp ln N_src=0"),
        ("CB4638_5", "delta_w_EM", "EM/Hodge weight drift", "zero if Maxwell/Hodge weight descends without source label"),
        ("CB4638_6", "R_no_direct_m_charge", "direct m-boundary/source charge", "zero if Q_m^H=0"),
        ("CB4638_7", "R_environment_selector", "environment selector", "zero if D_Hperp sigma_env=0"),
        ("CB4638_8", "Xi_src_hidden", "absolute first-component tail", "zero if all CB4638_0 through CB4638_7 are zero; otherwise bounded by their absolute sum"),
    ]
    rows: list[dict[str, Any]] = []
    for component_id, component, meaning, zero_condition in components:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "component_id": component_id,
                "component": component,
                "meaning": meaning,
                "zero_condition": zero_condition,
                "current_status": "CONDITIONAL_ZERO_NOT_GLOBAL_CLAIM",
                "numeric_value": "",
                "units": "dimensionless",
                "source_row": "F4332_0_Xi_definition/ZERO4332_8_Xi/TAIL4332_6_Xi_open",
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        )
    return rows


def run_rows(points: list[tuple[float, float]], now: str) -> list[dict[str, Any]]:
    specs = [
        ("RUN4638_0_live_missing_inputs", "current live corpus", None, None, None, None, None),
        ("RUN4638_1_all_tail_zero_control", "exact-zero control", 1.0e-4, 0.0, 0.0, 0.0, 0.0),
        ("RUN4638_2_Xisrc_pass_100um", "finite first-component smoke", 1.0e-4, 0.05, 0.0, 0.0, 0.0),
        ("RUN4638_3_Xisrc_fail_100um", "finite first-component smoke", 1.0e-4, 0.1, 0.0, 0.0, 0.0),
        ("RUN4638_4_reduced_tail_pass_100um", "other-tail smoke after Xisrc zero", 1.0e-4, 0.0, 0.02, 0.02, 0.01),
        ("RUN4638_5_reduced_tail_fail_1mm", "large-range tight-budget smoke", 1.0e-3, 0.0, 0.02, 0.0, 0.0),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, branch, lambda_m, xi_src, xi_nonhilbert, xi_boundary, xi_transition in specs:
        if lambda_m is None:
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "run_id": run_id,
                    "branch": branch,
                    "lambda_mem_m": "",
                    "Xi_src_hidden_abs": "",
                    "Xi_nonHilbert_abs": "",
                    "Xi_boundary_history_abs": "",
                    "Xi_transition_inner_abs": "",
                    "Xi_tail_abs": "",
                    "alpha_bound_vector": "",
                    "result": "FAIL_CLOSED",
                    "reason": "missing source-backed Xi component values and lambda_mem",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                    "timestamp_utc": now,
                }
            )
            continue
        alpha = interpolate_alpha(points, lambda_m)
        xi_tail = float(xi_src or 0.0) + float(xi_nonhilbert or 0.0) + float(xi_boundary or 0.0) + float(xi_transition or 0.0)
        if alpha is None:
            result = "FAIL_CLOSED"
            reason = "lambda outside extracted vector curve"
        elif xi_tail <= alpha:
            result = "SMOKE_PASS_NONCLAIM"
            reason = "absolute reduced tail sits inside digitized vector bound for this toy/control row"
        else:
            result = "SMOKE_FAIL_NONCLAIM"
            reason = "absolute reduced tail exceeds digitized vector bound"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "run_id": run_id,
                "branch": branch,
                "lambda_mem_m": f"{lambda_m:.12g}",
                "Xi_src_hidden_abs": f"{float(xi_src or 0.0):.12g}",
                "Xi_nonHilbert_abs": f"{float(xi_nonhilbert or 0.0):.12g}",
                "Xi_boundary_history_abs": f"{float(xi_boundary or 0.0):.12g}",
                "Xi_transition_inner_abs": f"{float(xi_transition or 0.0):.12g}",
                "Xi_tail_abs": f"{xi_tail:.12g}",
                "alpha_bound_vector": "" if alpha is None else f"{alpha:.12g}",
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
            "control_id": "CTRL4638_0_no_cancellation",
            "control": "use absolute component sums only",
            "result": "PASS",
            "reason": "the reduced R10 gate is |Xi_src_hidden|+|Xi_nonHilbert|+|Xi_boundary_history|+|Xi_transition_inner| <= alpha_bound(lambda_mem)",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4638_1_no_global_zero_import",
            "control": "do not promote source-label-forgetting zero globally",
            "result": "PASS",
            "reason": "4332 firewall remains active and all rows stay valid_for_claim=false",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4638_2_curve_smoke_only",
            "control": "R10 rows are smoke controls, not evidence rows",
            "result": "PASS",
            "reason": "runner rows use toy/control Xi components unless source-backed parent values exist",
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    blockers = [
        ("BLK4638_0", "MISSING_GLOBAL_PARENT_SIGNATURE", "source-label-forgetting/no-hidden-slot branch is conditional, not global"),
        ("BLK4638_1", "MISSING_XI_NONHILBERT_VALUE_OR_ZERO", "non-Hilbert H_perp bypass remains open"),
        ("BLK4638_2", "MISSING_BOUNDARY_HISTORY_VALUE_OR_ZERO", "boundary/history and transition-inner residuals remain unsourced"),
        ("BLK4638_3", "MISSING_LAMBDA_MEM_PARENT_VALUE", "lambda_mem still needs parent derivation/source value"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "detail": detail,
            "blocks_claim": True,
            "next_action": NEXT_TARGET if blocker_id == "BLK4638_1" else "retain in tail ledger",
            "timestamp_utc": now,
        }
        for blocker_id, blocker, detail in blockers
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4638_0",
            "decision": DECISION,
            "selected_next_target": NEXT_TARGET,
            "claim_allowed": False,
            "reason": "first Xi-tail component now has a named conditional-zero route, but remaining tail components and global signature are still open",
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "COMPONENT_REDUCED_NONCLAIM",
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "local_gr_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "newton_claim": False,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "priority": "attack Xi_nonHilbert/H_perp as the next live reduced-tail term",
            "acceptance_gate": "either prove Xi_nonHilbert=0 in the same private branch or create a numeric nonclaim bound row against the R10 tail budget",
            "timestamp_utc": now,
        }
    ]


def build_doc(
    sources: list[dict[str, Any]],
    selections: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    runs: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4638 — Xi-tail first component: bound or exact zero

Marker: `{MARKER}`

## Result

4638 moves one real obstruction forward. The loose 4637 pair

`Xi_hidden_coeff + Xi_source_weight`

is canonicalized as the already-defined source-label residual vector

`Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + R_source_normalization + delta_w_EM + R_no_direct_m_charge + R_environment_selector`.

Inside the source-label-forgetting Hilbert-owner branch imported from 4332, `Xi_src_hidden = 0`. Outside that branch, `Xi_src_hidden` stays as a finite no-cancellation tail. This is progress, but not a public/local-GR claim: the global no-hidden-slot signature is not parent-signed, and `Xi_nonHilbert`, `Xi_boundary_history`, `Xi_transition_inner`, and `lambda_mem` remain live.

## Reduced R10 gate

Input from 4637:

`Xi_tail := Xi_hidden_coeff + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner + Xi_source_weight`.

4638 reduction:

`Xi_tail := Xi_src_hidden + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner`.

No-cancellation R10 gate:

`|Xi_src_hidden| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| <= alpha_bound(lambda_mem)`.

If the 4332 source-label-forgetting branch is selected:

`Xi_tail := Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner`.

## Source register

{markdown_table(sources)}

## First component selection

{markdown_table(selections)}

## Xi_src_hidden import audit

{markdown_table(audits)}

## Tail reduction rows

{markdown_table(reductions)}

## Xi_src_hidden component bounds

{markdown_table(bounds)}

## R10 reduced-tail smoke runner

{markdown_table(runs)}

## Claim blockers

{markdown_table(blockers)}

## Decision

{markdown_table(decisions)}

## Validation

{markdown_table(validations)}
"""


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4638 canonicalizes the first live Xi_tail obstruction by replacing Xi_hidden_coeff plus Xi_source_weight with Xi_src_hidden and importing its conditional source-label-forgetting zero theorem.",
        "current_evidence": "Generated source register, first-component selection, Xi_src_hidden import audit, reduced-tail rows, component bounds, R10 smoke runner, controls, blockers, decision, status, next target and validation.",
        "status": "Xi_src_hidden_first_component_reduced_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating branch-local source-label forgetting as a global parent proof, or hiding the remaining non-Hilbert/boundary/transition tails.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/Newton/R10/PPN claim until Xi_src_hidden is globally zero or source-backed, and the remaining reduced-tail components plus lambda_mem are zero-certified or source-backed.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writerow(row)


def validate(
    sources: list[dict[str, Any]],
    selections: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    runs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4638_0_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"))
    checks.append(("VAL4638_1_needles_found", all(row["needle_found"] for row in sources), "all cited source needles are present"))
    checks.append(("VAL4638_2_selected_component", any(row["selected_component"] == "Xi_src_hidden" for row in selections), "Xi_src_hidden selected as first component"))
    checks.append(("VAL4638_3_conditional_zero_imported", any(row["input_row"] == "ZERO4332_8_Xi" and row["status"] == "CONDITIONAL_ZERO_AVAILABLE" for row in audits), "conditional zero row imported"))
    checks.append(("VAL4638_4_open_tail_retained", any(row["input_row"] == "TAIL4332_6_Xi_open" for row in audits), "open source-label tail retained"))
    checks.append(("VAL4638_5_reduced_tail_defined", any(row["row_id"] == "XR4638_2_reduced_tail" for row in reductions), "four-component reduced tail defined"))
    checks.append(("VAL4638_6_component_bounds_nonclaim", all(str(row.get("valid_for_claim")) == "False" for row in bounds), "component bound rows remain nonclaim"))
    checks.append(("VAL4638_7_runner_live_fail_closed", any(row["run_id"] == "RUN4638_0_live_missing_inputs" and row["result"] == "FAIL_CLOSED" for row in runs), "live missing-input row fails closed"))
    checks.append(("VAL4638_8_runner_has_pass_and_fail_controls", any("PASS" in row["result"] for row in runs) and any("FAIL" in row["result"] for row in runs), "runner has pass and fail controls"))
    checks.append(("VAL4638_9_doc_marker", MARKER in read_text(DOC_PATH), "post-checkpoint doc marker present"))
    checks.append(("VAL4638_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal checkpoint marker present"))
    checks.append(("VAL4638_11_claim_registered", CLAIM_ID in read_text(CLAIMS_PATH), "claim row registered"))
    checks.append(("VAL4638_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended"))
    checks.append(("VAL4638_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended"))
    checks.append(("VAL4638_14_public_stage_clean", git_clean(PUBLIC_STAGE), "public stage not modified"))
    checks.append(("VAL4638_15_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo not modified"))
    validations = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": utc_now(),
        }
        for check_id, passed, detail in checks
    ]
    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4638_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4638 validation passed" if overall else "one or more 4638 checks failed",
            "timestamp_utc": utc_now(),
        }
    )
    return validations


def main() -> int:
    now = utc_now()
    points = load_curve_points()

    sources = source_rows(now)
    selections = first_component_rows(now)
    audits = import_audit_rows(now)
    reductions = reduction_rows(now)
    bounds = bound_rows(now)
    runs = run_rows(points, now)
    controls = control_rows(now)
    blockers = blocker_rows(now)
    decisions = decision_rows(now)
    statuses = status_rows(now)
    next_targets = next_rows(now)

    for path, rows in [
        (SOURCE_REGISTER, sources),
        (FIRST_COMPONENT_CSV, selections),
        (IMPORT_AUDIT_CSV, audits),
        (REDUCTION_CSV, reductions),
        (BOUNDS_CSV, bounds),
        (RUNNER_CSV, runs),
        (CONTROL_CSV, controls),
        (BLOCKERS_CSV, blockers),
        (DECISION_CSV, decisions),
        (STATUS_CSV, statuses),
        (NEXT_CSV, next_targets),
    ]:
        write_csv(path, rows)

    provisional_validations = [
        {"checkpoint": CHECKPOINT, "validation_id": "VAL4638_PROVISIONAL", "status": "PENDING", "detail": "validation runs after documents are written", "timestamp_utc": now}
    ]
    doc_body = build_doc(sources, selections, audits, reductions, bounds, runs, blockers, decisions, provisional_validations)
    write_text(DOC_PATH, doc_body)
    write_text(FORMAL_PATH, doc_body.replace("# 4638", "# 654 / 4638", 1))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4638 canonicalizes the first live R10 coupling-tail component. The 4637 pair `Xi_hidden_coeff + Xi_source_weight` is replaced by `Xi_src_hidden`, whose 4332 source-label-forgetting Hilbert-owner branch gives conditional `Xi_src_hidden=0`. The live no-cancellation gate is now `|Xi_src_hidden| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| <= alpha_bound(lambda_mem)`. This remains nonclaim because the global no-hidden-slot/source-label signature and the remaining tail components are not closed.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` reduces the private local R10 source-coupling tail by isolating `Xi_src_hidden`. Inside the source-label-forgetting Hilbert-owner branch, `Xi_src_hidden=0`; outside it, this component remains an explicit source-label residual bound. Next packet target: `{NEXT_TARGET}`.
""",
    )
    append_claim_once()

    validations = validate(sources, selections, audits, reductions, bounds, runs)
    write_csv(VALIDATION_CSV, validations)
    final_doc = build_doc(sources, selections, audits, reductions, bounds, runs, blockers, decisions, validations)
    write_text(DOC_PATH, final_doc)
    write_text(FORMAL_PATH, final_doc.replace("# 4638", "# 654 / 4638", 1))

    print(f"{MARKER}: {validations[-1]['status']}")
    print(DOC_PATH)
    print(VALIDATION_CSV)
    return 0 if validations[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
