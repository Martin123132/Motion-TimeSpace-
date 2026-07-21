from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4629"
CLAIM_ID = "L-471"
BRANCH_ID = "MTS_R2FR_Y5_CANONICAL_ANCHOR_SMOKE_4629"
MARKER = "PPC4161_CANONICAL_NORMALIZATION_AND_FIRST_ANCHOR_SMOKE_RUNNER_4629"
PACKET_MARKER = "PPC4161_PACKET_CANONICAL_ANCHOR_SMOKE_4629"
DECISION = "CANONICAL_CO_NORMALIZATION_GATE_AND_ANCHOR_SMOKE_RUNNER_NONCLAIM"
NEXT_TARGET = "4630-Y5-R2FR-co-normalized-gap-and-source-coupling-parent-action.md"

DOC_PATH = POST / "4629-Y5-R2FR-canonical-normalization-and-first-anchor-smoke-runner.md"
FORMAL_PATH = FORMAL / "645-PPC4161-canonical-normalization-and-first-anchor-smoke-runner.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4629_SOURCE_REGISTER.csv"
CANONICAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_CANONICAL_NORMALIZATION_ROWS.csv"
INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_ANCHOR_SMOKE_INPUT_ROWS.csv"
SMOKE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_FIRST_ANCHOR_SMOKE_RUNNER_RESULTS.csv"
RUNNER_RULES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_ANCHOR_SMOKE_RUNNER_RULES.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4629_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4629_VALIDATION.csv"

CSV_4628_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4628_NEXT_TARGET.csv"
CSV_4628_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4628_VALIDATION.csv"
CSV_4628_ANCHOR = SOURCE_DIR / "P8_Y5_R2FR_4628_R10_ANCHOR_GAP_CONVERSION_ROWS.csv"
CSV_4628_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_4628_HESSIAN = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
CSV_4628_PROMOTION = SOURCE_DIR / "P8_Y5_R2FR_4628_PROMOTION_GATES.csv"
CSV_4627_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4627_QEFF_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_4627_SMOKE = SOURCE_DIR / "P8_Y5_R2FR_4627_ANCHOR_SMOKE_EVALUATION_ROWS.csv"
CSV_4627_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4627_VALIDATION.csv"

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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def numeric(value: Any) -> float | None:
    try:
        text = str(value).strip()
        if not text or "MISSING" in text or text.lower() in {"nan", "none", "any finite/infinite"}:
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def any_claim_true(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def anchor_values() -> tuple[float, float, float, float]:
    anchor = find_row(read_csv(CSV_4628_ANCHOR), "anchor_id", "A4628_0_R10_alpha1_lambda")
    lambda_anchor = numeric(anchor.get("lambda_anchor_m")) or 3.86e-05
    alpha_anchor = numeric(anchor.get("alpha_anchor")) or 1.0
    ratio_req = numeric(anchor.get("derived_ratio_requirement_m_minus_2")) or (1.0 / lambda_anchor**2)
    gap_ev = numeric(anchor.get("canonical_gap_energy_eV_if_Z_is_canonical")) or 0.005112097937823834
    return lambda_anchor, alpha_anchor, ratio_req, gap_ev


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4629_00_4628_next", CSV_4628_NEXT, "4629-Y5-R2FR-canonical-normalization-and-first-anchor-smoke-runner.md", "4628 selected canonical anchor smoke target."),
        ("SRC4629_01_4628_validation", CSV_4628_VALIDATION, "VAL4628_OVERALL", "4628 validation."),
        ("SRC4629_02_4628_anchor", CSV_4628_ANCHOR, "A4628_0_R10_alpha1_lambda", "4628 R10 alpha=1 anchor conversion."),
        ("SRC4629_03_4628_lambda_template", CSV_4628_NUMERIC, "LNUM4628_2_lambda", "4628 lambda_mem template."),
        ("SRC4629_04_4628_ratio_template", CSV_4628_NUMERIC, "LNUM4628_3_R10_anchor_gap_ratio", "4628 R10 gap ratio template."),
        ("SRC4629_05_4628_hessian_guard", CSV_4628_HESSIAN, "HES4628_2_canonical_normalization_guard", "4628 canonical normalization guard."),
        ("SRC4629_06_4628_promotion", CSV_4628_PROMOTION, "PROM4628_1_gap_anchor_smoke", "4628 gap anchor smoke gate."),
        ("SRC4629_07_4627_qeff", CSV_4627_NUMERIC, "QNUM4627_3_Qeff", "4627 Qeff template."),
        ("SRC4629_08_4627_alpha", CSV_4627_NUMERIC, "QNUM4627_4_alphaA", "4627 alpha sensitivities template."),
        ("SRC4629_09_4627_smoke", CSV_4627_SMOKE, "SMK4627_1_missing_numeric_fail_closed", "4627 fail-closed smoke row."),
        ("SRC4629_10_4627_validation", CSV_4627_VALIDATION, "VAL4627_OVERALL", "4627 validation."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
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
        })
    return rows


def canonical_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "canonical_id": "CAN4629_0_same_branch_ratio",
            "statement": "The range is fixed by the same-branch Hessian ratio, not by separately chosen Z_mem and M2_mem.",
            "formula": "m_gap^2 = M2_mem/Z_mem; lambda_mem = sqrt(Z_mem/M2_mem)",
            "consequence": "field rescalings cannot change lambda_mem if both Hessians come from the same parent quadratic action",
            "current_status": "RATIO_DEFINED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "canonical_id": "CAN4629_1_source_coupling_co_normalization",
            "statement": "The source charge and Yukawa amplitude must be normalized with the same canonical memory field as the gap.",
            "formula": "phi=sqrt(Z_mem) delta_m; J_c=J/sqrt(Z_mem); alpha_Y must use Q_eff^2/Z_mem or equivalent invariant sensitivity product",
            "consequence": "prevents artificial wins from rescaling delta_m while leaving Q_eff or alpha_Y untouched",
            "current_status": "QEFF_ZMEM_CO_NORMALIZATION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "canonical_id": "CAN4629_2_anchor_smoke_only",
            "statement": "The 38.6 micron alpha=1 row is a smoke threshold, not a full alpha(lambda) curve.",
            "formula": "anchor smoke passes only if alpha_Y<=1 and lambda_mem<=38.6e-6 m, with all parent rows real",
            "consequence": "a pass here would authorize a deeper run, not a local-GR/R10 claim",
            "current_status": "ANCHOR_SMOKE_RULE_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "canonical_id": "CAN4629_3_exact_zero_supersedes_range",
            "statement": "If Q_eff=0 by a parent theorem, the Yukawa amplitude vanishes and the range is locally silent for this channel.",
            "formula": "Q_eff=0 => alpha_Y=0 independent of lambda_mem for the trace Yukawa channel",
            "consequence": "exact-zero remains the cleanest route, but it must be signed by the parent action/selection rule",
            "current_status": "ZERO_THEOREM_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def input_rows(now: str) -> list[dict[str, Any]]:
    lambda_anchor, alpha_anchor, ratio_req, gap_ev = anchor_values()
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4629_0_lambda_anchor",
            "symbol": "lambda_anchor",
            "value": lambda_anchor,
            "units": "m",
            "source": "A4628_0_R10_alpha1_lambda",
            "numeric_ready": True,
            "feeds": "anchor smoke runner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4629_1_alpha_anchor",
            "symbol": "alpha_anchor",
            "value": alpha_anchor,
            "units": "dimensionless",
            "source": "A4628_0_R10_alpha1_lambda",
            "numeric_ready": True,
            "feeds": "anchor smoke runner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4629_2_gap_ratio_requirement",
            "symbol": "(M2_mem/Z_mem)_anchor",
            "value": ratio_req,
            "units": "m^-2",
            "source": "A4628_1_gap_ratio_template",
            "numeric_ready": True,
            "feeds": "lambda_mem <= anchor threshold",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4629_3_gap_energy_if_canonical",
            "symbol": "m_gap_anchor",
            "value": gap_ev,
            "units": "eV",
            "source": "A4628_0_R10_alpha1_lambda",
            "numeric_ready": True,
            "feeds": "intuition only",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4629_4_current_lambda_mem",
            "symbol": "lambda_mem",
            "value": "MISSING_ZMEM_M2MEM_RATIO",
            "units": "m",
            "source": "LNUM4628_2_lambda",
            "numeric_ready": False,
            "feeds": "current branch smoke row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4629_5_current_alpha_Y",
            "symbol": "alpha_Y",
            "value": "MISSING_QEFF_ZMEM_ALPHA_MASS",
            "units": "dimensionless",
            "source": "QNUM4627_4_alphaA plus QNUM4627_3_Qeff",
            "numeric_ready": False,
            "feeds": "current branch smoke row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def runner_rules(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "rule_id": "RULE4629_0_fail_closed",
            "rule": "If lambda_mem, alpha_Y, Q_eff/Z_mem, or source provenance is missing, result is FAIL_CLOSED.",
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "rule_id": "RULE4629_1_anchor_smoke",
            "rule": "For the anchor-only smoke test, require alpha_Y<=1 and lambda_mem<=38.6e-6 m.",
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "rule_id": "RULE4629_2_full_curve_needed",
            "rule": "Any alpha_Y>1 or off-anchor interpolation/extrapolation needs a real alpha(lambda) bound curve, not the threshold sentence.",
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "rule_id": "RULE4629_3_co_normalization",
            "rule": "lambda_mem and alpha_Y must be built from the same canonical memory variable or invariant products.",
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def evaluate_smoke(case_id: str, description: str, lambda_m: Any, alpha_y: Any, now: str) -> dict[str, Any]:
    lambda_anchor, alpha_anchor, _, _ = anchor_values()
    lam = numeric(lambda_m)
    alpha = numeric(alpha_y)
    if case_id == "SMK4629_1_exact_zero_qeff":
        result = "CONDITIONAL_ZERO_PASS_ALGEBRA_ONLY"
        reason = "alpha_Y=0 if parent signs Q_eff=0; no empirical claim until the zero theorem is signed"
    elif lam is None or alpha is None:
        result = "FAIL_CLOSED_MISSING_NUMERIC_INPUT"
        reason = "current branch lacks co-normalized lambda_mem and alpha_Y"
    elif alpha <= alpha_anchor and lam <= lambda_anchor:
        result = "PASS_ANCHOR_SMOKE_ONLY_NONCLAIM"
        reason = "passes the conservative alpha=1 threshold smoke rule, but not a full curve claim"
    elif alpha > alpha_anchor:
        result = "FAIL_OR_INDETERMINATE_NEEDS_FULL_CURVE"
        reason = "anchor-only evidence cannot approve alpha_Y above the alpha=1 threshold"
    else:
        result = "FAIL_ANCHOR_SMOKE_LONG_RANGE"
        reason = "lambda_mem exceeds the conservative alpha=1 anchor range"
    return {
        "checkpoint": CHECKPOINT,
        "smoke_id": case_id,
        "description": description,
        "lambda_mem_m": lambda_m,
        "alpha_Y": alpha_y,
        "lambda_anchor_m": lambda_anchor,
        "alpha_anchor": alpha_anchor,
        "runner_result": result,
        "reason": reason,
        "valid_for_claim": False,
        "claim_allowed": False,
        "timestamp_utc": now,
    }


def smoke_rows(now: str) -> list[dict[str, Any]]:
    lambda_anchor, _, _, _ = anchor_values()
    return [
        evaluate_smoke("SMK4629_0_current_placeholder", "current generated placeholders from 4627/4628", "MISSING_ZMEM_M2MEM_RATIO", "MISSING_QEFF_ZMEM_ALPHA_MASS", now),
        evaluate_smoke("SMK4629_1_exact_zero_qeff", "exact-zero theorem branch if parent signs Q_eff=0", "any finite/infinite", 0.0, now),
        evaluate_smoke("SMK4629_2_anchor_equal_alpha1", "control case: alpha=1 at anchor lambda", lambda_anchor, 1.0, now),
        evaluate_smoke("SMK4629_3_short_range_alpha1", "control case: alpha=1 at half anchor lambda", lambda_anchor / 2.0, 1.0, now),
        evaluate_smoke("SMK4629_4_long_range_alpha1", "control case: alpha=1 at twice anchor lambda", lambda_anchor * 2.0, 1.0, now),
        evaluate_smoke("SMK4629_5_short_range_alpha10", "control case: alpha=10 at half anchor lambda", lambda_anchor / 2.0, 10.0, now),
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4629_0_no_unit_win",
            "rule": "Do not treat separate Z_mem, M2_mem, Q_eff or alpha_Y entries as meaningful unless they are co-normalized.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4629_1_anchor_not_curve",
            "rule": "Do not extrapolate from the alpha=1 threshold anchor to arbitrary alpha(lambda).",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4629_2_exact_zero_needs_signature",
            "rule": "Exact-zero smoke pass is algebraic only until the parent selection rule signs Q_eff=0.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4629_0_parent_action",
            "blocks": "co-normalized lambda_mem and alpha_Y",
            "missing": "single parent quadratic action giving Z_mem, M2_mem and source coupling J/Q_eff in the same normalization",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4629_1_full_bound_curve",
            "blocks": "R10 claim beyond anchor smoke",
            "missing": "real alpha(lambda) bound curve or machine-readable table",
            "next_action": "source acquisition after parent rows exist",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4629_2_zero_theorem",
            "blocks": "exact-zero local silence route",
            "missing": "parent-signed Q_eff=0, beta_T=0, no-flux, or screening theorem",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4629_0_exact_zero",
            "promotion_condition": "Parent action proves Q_eff=0 or alpha_Y=0 on the local branch.",
            "current_result": "blocked_zero_theorem_unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4629_1_numeric_anchor_smoke",
            "promotion_condition": "Parent-owned co-normalized lambda_mem and alpha_Y are numeric, sourced, and pass alpha_Y<=1 with lambda_mem<=38.6e-6 m.",
            "current_result": "blocked_missing_co_normalized_parent_rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4629_2_full_r10_claim",
            "promotion_condition": "Full source-backed alpha(lambda) curve exists and the co-normalized MTS prediction lies below it.",
            "current_result": "blocked_full_curve_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4629_0",
            "decision": DECISION,
            "meaning": "The first R10 anchor smoke runner now exists and fails the live branch closed because lambda_mem and alpha_Y are not yet co-normalized parent-owned numbers. Control cases prove the runner can distinguish pass/fail branches.",
            "status": "NONCLAIM_PRIVATE_RUNNER_READY",
            "best_route": "derive a single parent quadratic/source action that fixes M2_mem/Z_mem and Q_eff^2/Z_mem together",
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
            "status": "PRIVATE_NONCLAIM_RUNNER_ADVANCE",
            "summary": "canonical co-normalization guard and first R10 anchor smoke runner are written; current branch fails closed until parent action supplies M2/Z and Qeff/Z together",
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The runner is ready; now the theory needs a single parent action row that co-normalizes gap and source coupling.",
            "derive_first": "derive Z_mem, M2_mem and J/Q_eff from one quadratic source action",
            "fallback": "keep local branch nonclaim and use external bound inputs only as blocked placeholders",
            "valid_for_claim": False,
        }
    ]


def write_doc(
    now: str,
    sources: list[dict[str, Any]],
    canonical: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> None:
    lambda_anchor, alpha_anchor, ratio_req, gap_ev = anchor_values()
    body = f"""# 4629 - Canonical Normalization And First Anchor Smoke Runner

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

This checkpoint turns the 4628 gap row into an actual fail-closed anchor-smoke runner.

The important new guard is co-normalization:

`S_mem^(2) = 1/2 int mu_obs [Z_mem (partial delta_m)^2 + M2_mem delta_m^2] + int mu_obs J_mem delta_m`

`phi = sqrt(Z_mem) delta_m`, so:

`m_gap^2 = M2_mem/Z_mem`

`lambda_mem = sqrt(Z_mem/M2_mem)`

and the source amplitude must use the same canonical field:

`J_c = J_mem/sqrt(Z_mem)`, or equivalently an invariant `Q_eff^2/Z_mem` style combination.

This blocks a fake win where `lambda_mem` is derived from one normalization but `alpha_Y` is quietly evaluated in another.

## Anchor Values

- `lambda_anchor = {lambda_anchor} m`
- `alpha_anchor = {alpha_anchor}`
- `(M2_mem/Z_mem)_anchor = {ratio_req} m^-2`
- `m_gap_anchor = {gap_ev} eV` if the memory field is canonically normalized.

These are still anchor-smoke values only, not a full R10 bound curve.

## Source Register

{markdown_table(sources)}

## Canonical Normalization Rows

{markdown_table(canonical)}

## Smoke Inputs

{markdown_table(inputs)}

## Runner Rules

{markdown_table(rules)}

## First Anchor Smoke Results

{markdown_table(smoke)}

## Blockers

{markdown_table(blockers)}

## Promotion Gates

{markdown_table(promotions)}

## Decision

{markdown_table(decisions)}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, body)


def write_formal(now: str) -> None:
    lambda_anchor, alpha_anchor, ratio_req, gap_ev = anchor_values()
    body = f"""# 645 - PPC4161 Canonical Normalization And First Anchor Smoke Runner

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

The local branch now has a first fail-closed R10 anchor-smoke runner.

Core rule:

`m_gap^2 = M2_mem/Z_mem`, `lambda_mem = sqrt(Z_mem/M2_mem)`, and `alpha_Y` must be built from the same canonical memory variable.

The live branch fails closed because `lambda_mem`, `Q_eff`, `Z_mem`, and `alpha_Y` are not yet same-branch parent-owned numeric rows.

Anchor-smoke threshold:

`lambda_anchor = {lambda_anchor} m`, `alpha_anchor = {alpha_anchor}`,
`(M2_mem/Z_mem)_anchor = {ratio_req} m^-2`,
`m_gap_anchor = {gap_ev} eV` if canonical.

Next target: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, body)


def append_integrations(now: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Canonical Normalization And First Anchor Smoke Runner 4629

Marker: `{MARKER}`

4629 adds the co-normalization guard for the local branch: the same parent quadratic/source action must supply `M2_mem/Z_mem` and the invariant source amplitude (`Q_eff^2/Z_mem` or equivalent). A first R10 anchor-smoke runner now exists and the live branch fails closed until those parent rows are real.

Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet - Canonical Anchor Smoke 4629

Marker: `{PACKET_MARKER}`

Local packet update: `lambda_mem` cannot be checked independently of the source coupling normalization. The 4629 runner prevents a fake local-GR pass by requiring co-normalized `lambda_mem` and `alpha_Y` before even an anchor-smoke pass can promote.

Next: `{NEXT_TARGET}`.
""",
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                CLAIM_ID,
                "local_gr_empirical_interface",
                "4629 adds a canonical co-normalization guard and first fail-closed R10 anchor-smoke runner.",
                "Generated source register, canonical rows, smoke inputs, runner rules, smoke results, controls, blockers, promotion gates, decision, status, next target and validation.",
                "canonical_anchor_smoke_runner_nonclaim",
                NEXT_TARGET,
                "Winning by field normalization or treating an alpha=1 threshold anchor as a full bound curve.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No local-GR/Newton/WEP/PPN pass until gap and source coupling are co-normalized from a parent action or exact-zero theorem.",
            ])


def validation_rows(
    sources: list[dict[str, Any]],
    generated_groups: list[list[dict[str, Any]]],
    smoke: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str) -> None:
        checks.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if status else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    all_sources = all(row["path_exists"] and row["needle_found"] for row in sources)
    add("VAL4629_00_sources_exist_and_needles_found", all_sources, "all cited paths/needles found" if all_sources else "missing source path or needle")

    csv_paths = [
        SOURCE_REGISTER,
        CANONICAL_CSV,
        INPUT_CSV,
        SMOKE_CSV,
        RUNNER_RULES_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_details: list[str] = []
    parse_ok = True
    for path in csv_paths:
        try:
            count = len(read_csv(path))
            parse_details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover - validation script
            parse_ok = False
            parse_details.append(f"{path.name}:ERROR:{exc}")
    add("VAL4629_01_csv_parse", parse_ok, ";".join(parse_details))

    current = find_row([{k: str(v) for k, v in row.items()} for row in smoke], "smoke_id", "SMK4629_0_current_placeholder")
    add("VAL4629_02_current_branch_fails_closed", current.get("runner_result") == "FAIL_CLOSED_MISSING_NUMERIC_INPUT", current.get("runner_result", "missing"))

    pass_cases = [row for row in smoke if row.get("runner_result") == "PASS_ANCHOR_SMOKE_ONLY_NONCLAIM"]
    fail_cases = [row for row in smoke if str(row.get("runner_result", "")).startswith("FAIL")]
    add("VAL4629_03_runner_has_pass_and_fail_controls", bool(pass_cases and fail_cases), f"pass={len(pass_cases)} fail={len(fail_cases)}")

    co_norm = any(row.get("canonical_id") == "CAN4629_1_source_coupling_co_normalization" for row in generated_groups[1])
    add("VAL4629_04_co_normalization_guard_present", co_norm, "source coupling co-normalization row present")

    no_claims = not any(any_claim_true(group) for group in generated_groups)
    add("VAL4629_05_all_rows_nonclaim", no_claims, "no generated row promotes a claim")

    add("VAL4629_06_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4629_07_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4629_08_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4629_09_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4629_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4629_11_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4629_12_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4629_13_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))

    overall = all(row["status"] == "PASS" for row in checks)
    add("VAL4629_OVERALL", overall, "4629 canonical anchor smoke checkpoint")
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows(now)
    canonical = canonical_rows(now)
    inputs = input_rows(now)
    rules = runner_rules(now)
    smoke = smoke_rows(now)
    controls = control_rows(now)
    blockers = blocker_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    statuses = status_rows(now)
    nexts = next_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CANONICAL_CSV, canonical)
    write_csv(INPUT_CSV, inputs)
    write_csv(RUNNER_RULES_CSV, rules)
    write_csv(SMOKE_CSV, smoke)
    write_csv(CONTROL_CSV, controls)
    write_csv(BLOCKERS_CSV, blockers)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)

    write_doc(now, sources, canonical, inputs, rules, smoke, blockers, promotions, decisions)
    write_formal(now)
    append_integrations(now)

    generated_groups = [sources, canonical, inputs, rules, smoke, controls, blockers, promotions, decisions, statuses, nexts]
    write_csv(VALIDATION_CSV, validation_rows(sources, generated_groups, smoke))

    print(f"4629 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
