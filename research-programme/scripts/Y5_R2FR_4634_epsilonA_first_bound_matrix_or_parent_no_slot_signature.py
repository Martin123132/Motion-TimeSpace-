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

CHECKPOINT = "4634"
CLAIM_ID = "L-476"
BRANCH_ID = "MTS_R2FR_Y5_EPSILONA_FIRST_BOUND_MATRIX_4634"
MARKER = "PPC4161_EPSILONA_FIRST_BOUND_MATRIX_OR_PARENT_NO_SLOT_SIGNATURE_4634"
PACKET_MARKER = "PPC4161_PACKET_EPSILONA_FIRST_BOUND_MATRIX_4634"
DECISION = "FIRST_EPSILONA_BOUND_MATRIX_READY_LIVE_BRANCH_FAILS_CLOSED_PARENT_NO_SLOT_UNSIGNED"
NEXT_TARGET = "4635-Y5-R2FR-epsilonA-R10-curve-and-projection-inputs-or-no-slot-source-hunt.md"

DOC_PATH = POST / "4634-Y5-R2FR-epsilonA-first-bound-matrix-or-parent-no-slot-signature.md"
FORMAL_PATH = FORMAL / "650-PPC4161-epsilonA-first-bound-matrix-or-parent-no-slot-signature.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4634_SOURCE_REGISTER.csv"
NO_SLOT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_PARENT_NO_SLOT_SIGNATURE_EVALUATION.csv"
BOUND_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_EPSILONA_FIRST_BOUND_MATRIX.csv"
THRESHOLD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_SYMBOLIC_THRESHOLD_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_BOUND_MATRIX_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4634_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4634_VALIDATION.csv"

CSV_4633_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4633_NEXT_TARGET.csv"
CSV_4633_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4633_VALIDATION.csv"
CSV_4633_BRIDGE = SOURCE_DIR / "P8_Y5_R2FR_4633_NO_SOURCE_SLOT_TO_EVEN_AM_BRIDGE_ROWS.csv"
CSV_4633_SIGN = SOURCE_DIR / "P8_Y5_R2FR_4633_PARENT_SIGNING_MATRIX.csv"
CSV_4633_ACQ = SOURCE_DIR / "P8_Y5_R2FR_4633_EPSILONA_INPUT_ACQUISITION_MANIFEST.csv"
CSV_4633_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4633_ARENA_READINESS_ROWS.csv"
CSV_4632_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4632_EPSILONA_BOUND_RUNNER_RESULTS.csv"
CSV_4626_ANCHORS = SOURCE_DIR / "P8_Y5_R2FR_4626_SOURCE_BACKED_BOUND_ANCHORS.csv"
CSV_4626_MAP = SOURCE_DIR / "P8_Y5_R2FR_4626_LOCAL_G_BOUND_MAP_ROWS.csv"
CSV_4628_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_1451_THEOREM = SOURCE_DIR / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv"
CSV_1451_SIGN = SOURCE_DIR / "P8_Y5_R10_1451_PARENT_SIGNING_DECISION.csv"
CSV_1452_SIGN = SOURCE_DIR / "P8_Y5_R10_1452_PARENT_SIGNING_DECISION.csv"

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


def any_claim_true(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def numeric(value: Any) -> float | None:
    try:
        text = str(value).strip()
        if not text or "MISSING" in text or text.lower() in {"none", "nan", "exact_zero", "not_applicable"}:
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4634_00_4633_next", CSV_4633_NEXT, "4634-Y5-R2FR-epsilonA-first-bound-matrix-or-parent-no-slot-signature.md", "4633 selected first matrix target."),
        ("SRC4634_01_4633_validation", CSV_4633_VALIDATION, "VAL4633_OVERALL", "4633 validation."),
        ("SRC4634_02_4633_bridge", CSV_4633_BRIDGE, "BR4633_0_no_slot_implies_q_basic_Am", "q-basic A_m bridge."),
        ("SRC4634_03_4633_zero_refused", CSV_4633_BRIDGE, "ZERO_IMPORT_REFUSED_BOUND_ROUTE_ACTIVE", "zero import refused."),
        ("SRC4634_04_4633_sign", CSV_4633_SIGN, "SIGN4633_0_no_hidden_visible_Hom", "parent signing matrix."),
        ("SRC4634_05_4633_acq", CSV_4633_ACQ, "ACQ4633_1_epsilon_convention", "epsilon acquisition manifest."),
        ("SRC4634_06_4633_arena", CSV_4633_ARENA, "ARENA4633_0_R10", "arena readiness."),
        ("SRC4634_07_4632_runner", CSV_4632_RUNNER, "RUN4632_0_current_live_branch", "current fail-closed epsilon runner."),
        ("SRC4634_08_4626_anchor", CSV_4626_ANCHORS, "BA4626_0_R10_EOTWASH_ALPHA1", "R10/WEP/PPN anchors."),
        ("SRC4634_09_4626_map", CSV_4626_MAP, "LGM4626_0_R10_alpha", "local-G map."),
        ("SRC4634_10_4628_lambda", CSV_4628_NUMERIC, "LNUM4628_3_R10_anchor_gap_ratio", "R10 gap anchor ratio."),
        ("SRC4634_11_1451_theorem", CSV_1451_THEOREM, "OG1451_6_verdict", "no-source-slot theorem verdict."),
        ("SRC4634_12_1451_sign", CSV_1451_SIGN, "SIGN1451_0_no_slot", "1451 zero import refusal."),
        ("SRC4634_13_1452_sign", CSV_1452_SIGN, "SIGN1452_0_common_measure", "1452 common-measure refusal."),
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


def no_slot_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_eval_id": "NS4634_0_exact_zero_if_signed",
            "case": "all no-source-slot/common-measure/no-Hom/non-Hilbert signatures signed",
            "epsilon_A": 0.0,
            "epsilon_B": 0.0,
            "result": "CONDITIONAL_PARENT_ZERO_ROUTE",
            "current_status": "NOT_SIGNED_NOW",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "signature_eval_id": "NS4634_1_current_signing_state",
            "case": "current 1451/1452/4633 signing state",
            "epsilon_A": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "epsilon_B": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "result": "ZERO_IMPORT_REFUSED",
            "current_status": "BOUND_MATRIX_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def bound_matrix_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "matrix_id": "BM4634_0_R10",
            "arena": "R10 short-range",
            "observable": "Yukawa alpha(lambda)",
            "prediction": "alpha_AB=C_N epsilon_A epsilon_B/Z_min; lambda_mem=sqrt(Z_mem/M2_mem)",
            "bound": "alpha_AB<=alpha_bound(lambda); current anchor alpha=1 at lambda<=38.6e-6 m",
            "current_evaluation": "FAIL_CLOSED_MISSING_EPSILON_Z_CN_LAMBDA_FULL_CURVE",
            "required_inputs": "epsilon_A, epsilon_B, Z_min, C_N, lambda_mem, full alpha(lambda) curve",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "matrix_id": "BM4634_1_WEP",
            "arena": "MICROSCOPE/WEP",
            "observable": "eta_AB",
            "prediction": "eta_AB ~ K_WEP(lambda,source,test) * (epsilon_A-epsilon_B) * epsilon_source/Z_min",
            "bound": "use BA4626_1 conservative Ti/Pt eta gate after composition/projection map",
            "current_evaluation": "FAIL_CLOSED_MISSING_SENSITIVITY_AND_SOURCE_GEOMETRY",
            "required_inputs": "Ti/Pt sensitivity map, source/test convention, epsilon source vector, covariance",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "matrix_id": "BM4634_2_PPN",
            "arena": "Cassini/PPN",
            "observable": "gamma-1, beta-1, preferred-frame/source residuals",
            "prediction": "Delta_PPN = P_PPN(lambda) * alpha_AB plus metric-sector residual vector",
            "bound": "use BA4626_2 gamma gate only after c_gamma(lambda) is parent-derived",
            "current_evaluation": "FAIL_CLOSED_MISSING_PPN_PROJECTION",
            "required_inputs": "c_gamma(lambda), beta/preferred-frame projection, metric residual separation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "matrix_id": "BM4634_3_clocks",
            "arena": "clock/redshift",
            "observable": "clock sensitivity / redshift residual",
            "prediction": "Delta_clock = P_clock(lambda,clock) * alpha_AB plus EM/mass-constant sensitivity terms",
            "bound": "no source-backed local clock bound row in this packet yet",
            "current_evaluation": "FAIL_CLOSED_BOUND_AND_PROJECTION_MISSING",
            "required_inputs": "clock species sensitivities, source potential calibration, bound source",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "matrix_id": "BM4634_4_orbital",
            "arena": "orbital/Newtonian",
            "observable": "delta a/a_N, GM drift, inverse-square residual",
            "prediction": "delta a/a_N ~ alpha_AB exp(-r/lambda)(1+r/lambda) plus source-worldtube terms",
            "bound": "no source-backed orbital/local-G curve row in this packet yet",
            "current_evaluation": "FAIL_CLOSED_BOUND_AND_WORLDTUBE_MAP_MISSING",
            "required_inputs": "source-backed orbital bound, worldtube/Gauss map, GM calibration convention",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def threshold_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "threshold_id": "TH4634_0_R10_anchor_epsilon_product",
            "condition": "lambda_mem <= 38.6e-6 m and anchor-only alpha_bound=1",
            "inequality": "C_N epsilon_A epsilon_B/Z_min <= 1",
            "equivalent": "epsilon_A epsilon_B <= Z_min/C_N",
            "status": "SYMBOLIC_THRESHOLD_READY_ZMIN_CN_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "threshold_id": "TH4634_1_symmetric_epsilon_anchor",
            "condition": "epsilon_A=epsilon_B=epsilon and same R10 anchor-only rule",
            "inequality": "epsilon <= sqrt(Z_min/C_N)",
            "equivalent": "requires parent-owned Z_min and C_N",
            "status": "SYMBOLIC_THRESHOLD_READY_NOT_NUMERIC",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "threshold_id": "TH4634_2_exact_no_slot",
            "condition": "q-basic A_m/no-source-slot theorem signed",
            "inequality": "epsilon_A epsilon_B = 0",
            "equivalent": "alpha_AB=0 independent of R10 range for this channel",
            "status": "CONDITIONAL_ZERO_ROUTE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def eval_bound(case_id: str, arena: str, epsilon_a: Any, epsilon_b: Any, z_min: Any, c_n: Any, lambda_m: Any, now: str) -> dict[str, Any]:
    eps_a = numeric(epsilon_a)
    eps_b = numeric(epsilon_b)
    z_value = numeric(z_min)
    c_value = numeric(c_n)
    lam = numeric(lambda_m)
    lambda_anchor = 3.86e-05
    if case_id == "RUN4634_1_parent_no_slot_zero":
        alpha = 0.0
        result = "CONDITIONAL_EXACT_ZERO_PASS_ALGEBRA_ONLY"
        reason = "q-basic A_m/no-source-slot would set epsilon_A=epsilon_B=0, but signatures remain unsigned"
    elif None in {eps_a, eps_b, z_value, c_value, lam} or z_value == 0:
        alpha = "MISSING"
        result = "FAIL_CLOSED_MISSING_INPUT"
        reason = "epsilon_A/epsilon_B/Z_min/C_N/lambda_mem are not co-normalized numeric inputs"
    else:
        alpha = c_value * eps_a * eps_b / z_value
        if arena == "R10" and alpha <= 1.0 and lam <= lambda_anchor:
            result = "PASS_R10_ANCHOR_SMOKE_ONLY_NONCLAIM"
            reason = "control row passes anchor smoke only; full curve and source-backed inputs still required"
        elif arena == "R10" and alpha > 1.0:
            result = "FAIL_R10_ALPHA_ABOVE_ANCHOR"
            reason = "co-normalized alpha exceeds alpha=1 anchor threshold"
        elif arena == "R10":
            result = "FAIL_R10_RANGE_ABOVE_ANCHOR"
            reason = "lambda exceeds anchor range"
        else:
            result = "FAIL_CLOSED_PROJECTION_MISSING"
            reason = f"{arena} projection coefficient and source geometry are missing"
    return {
        "checkpoint": CHECKPOINT,
        "run_id": case_id,
        "arena": arena,
        "epsilon_A": epsilon_a,
        "epsilon_B": epsilon_b,
        "Z_min": z_min,
        "C_N": c_n,
        "lambda_mem_m": lambda_m,
        "alpha_AB": alpha,
        "result": result,
        "reason": reason,
        "valid_for_claim": False,
        "claim_allowed": False,
        "timestamp_utc": now,
    }


def runner_rows(now: str) -> list[dict[str, Any]]:
    return [
        eval_bound("RUN4634_0_current_live_R10", "R10", "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND", "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND", "MISSING_ZMEM_PARENT_VALUE", "MISSING_CONVENTION_OR_CALIBRATION", "MISSING_ZMEM_M2MEM_RATIO", now),
        eval_bound("RUN4634_1_parent_no_slot_zero", "R10", 0.0, 0.0, "not_applicable", 1.0, "not_applicable", now),
        eval_bound("RUN4634_2_R10_small_control", "R10", 0.01, 0.01, 1.0, 1.0, 1.93e-05, now),
        eval_bound("RUN4634_3_R10_order_one_control", "R10", 1.0, 1.0, 0.5, 1.0, 1.93e-05, now),
        eval_bound("RUN4634_4_R10_long_range_control", "R10", 0.01, 0.01, 1.0, 1.0, 7.72e-05, now),
        eval_bound("RUN4634_5_WEP_projection_missing", "WEP", 0.01, 0.02, 1.0, 1.0, 1.93e-05, now),
        eval_bound("RUN4634_6_PPN_projection_missing", "PPN", 0.01, 0.01, 1.0, 1.0, 1.93e-05, now),
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4634_0_no_zero_without_signature",
            "rule": "No-source-slot/q-basic A_m may set epsilon_A=0 only after all parent signatures are signed.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": "4634",
            "control_id": "CTL4634_1_no_R10_curve_overclaim",
            "rule": "R10 alpha=1 threshold is a smoke anchor, not a full alpha(lambda) claim.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4634_2_no_arena_projection_skip",
            "rule": "WEP/PPN/clock/orbital rows cannot score until their projection maps exist.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4634_0_parent_no_slot",
            "blocks": "exact epsilon zero",
            "missing": "parent no-hidden-visible-Hom, label forgetting, common measure/current, no-spurion return and non-Hilbert guard",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4634_1_R10_full_score",
            "blocks": "R10 claim",
            "missing": "source-backed epsilon/Z/C_N/lambda values and full alpha(lambda) curve",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4634_2_other_arenas",
            "blocks": "WEP/PPN/clock/orbital claim",
            "missing": "arena projection coefficients and source-backed bounds/maps",
            "next_action": "after R10/effective epsilon matrix stabilizes",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4634_0_parent_zero",
            "promotion_condition": "q-basic A_m/no-source-slot theorem is parent-signed; epsilon_A=0 feeds exact local route.",
            "current_result": "blocked unsigned signatures",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4634_1_R10_bound",
            "promotion_condition": "epsilon_A/B, Z_min, C_N, lambda_mem and full alpha(lambda) curve are real and pass.",
            "current_result": "blocked missing inputs/full curve",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4634_0",
            "decision": DECISION,
            "meaning": "The first epsilon_A bound matrix is now executable and fail-closed. Exact-zero remains the preferred route if parent no-source-slot signatures are signed; otherwise R10/WEP/PPN/clock/orbital rows need explicit inputs before scoring.",
            "status": "NONCLAIM_FIRST_BOUND_MATRIX_READY",
            "best_route": "try to sign parent no-source-slot; in parallel acquire R10 curve and co-normalized epsilon/Z/C_N/lambda inputs",
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
            "status": "PRIVATE_NONCLAIM_FIRST_BOUND_MATRIX_READY",
            "summary": "epsilon_A first bound matrix written; live branch fails closed; R10 controls pass/fail; WEP/PPN projections remain missing",
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
            "reason": "The bound matrix is now explicit; next should either source the R10 curve/projection inputs or make a stronger parent no-slot signature hunt.",
            "derive_first": "parent no-source-slot/q-basic A_m signature",
            "fallback": "acquire R10 alpha(lambda) curve and co-normalized epsilon/Z/lambda/C_N rows",
            "valid_for_claim": False,
        }
    ]


def write_doc(now: str, groups: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4634 - EpsilonA First Bound Matrix Or Parent No-Slot Signature

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

4634 instantiates the first `epsilon_A` bound matrix.

Exact-zero route:

`NoSourceOnlySlot/q-basic A_m -> epsilon_A=epsilon_B=0 -> alpha_AB=0`.

Current corpus: parent no-slot signatures remain unsigned, so this stays conditional.

Bound route:

`alpha_AB = C_N epsilon_A epsilon_B/Z_min`

`lambda_mem = sqrt(Z_mem/M2_mem)`.

The live row fails closed because `epsilon_A`, `epsilon_B`, `Z_min`, `C_N`, `lambda_mem`, and the full R10 `alpha(lambda)` curve are not yet all source-backed. R10 has control pass/fail rows; WEP/PPN/clocks/orbits are matrix rows with missing projection maps, not claims.

## Source Register

{markdown_table(groups["sources"])}

## Parent No-Slot Signature Evaluation

{markdown_table(groups["no_slot"])}

## First Epsilon-A Bound Matrix

{markdown_table(groups["bound_matrix"])}

## Symbolic Thresholds

{markdown_table(groups["thresholds"])}

## Runner Results

{markdown_table(groups["runner"])}

## Controls

{markdown_table(groups["controls"])}

## Blockers

{markdown_table(groups["blockers"])}

## Promotion Gates

{markdown_table(groups["promotions"])}

## Decision

{markdown_table(groups["decisions"])}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, body)


def write_formal() -> None:
    body = f"""# 650 - PPC4161 EpsilonA First Bound Matrix Or Parent No-Slot Signature

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

4634 writes the first executable epsilon_A matrix.

Exact-zero fork:

`q-basic A_m/no-source-slot => epsilon_A=epsilon_B=0 => alpha_AB=0`.

Current status: unsigned.

Bound fork:

`alpha_AB = C_N epsilon_A epsilon_B/Z_min`,

`lambda_mem=sqrt(Z_mem/M2_mem)`.

R10 anchor-smoke threshold:

`epsilon_A epsilon_B <= Z_min/C_N` if `lambda_mem <= 38.6e-6 m`.

Live branch fails closed; WEP/PPN/clock/orbital rows require projection maps before scoring.

Next target: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, body)


def append_integrations() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 EpsilonA First Bound Matrix Or Parent No-Slot Signature 4634

Marker: `{MARKER}`

4634 makes the epsilon-bound route executable. Exact zero remains available only if parent no-source-slot/q-basic `A_m` is signed. Otherwise the first matrix is `alpha_AB=C_N epsilon_A epsilon_B/Z_min` with `lambda_mem=sqrt(Z_mem/M2_mem)`. The live branch fails closed; R10 has smoke controls, and WEP/PPN/clock/orbital rows expose their missing projection maps.

Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet - EpsilonA First Bound Matrix 4634

Marker: `{PACKET_MARKER}`

Local packet update: the bound route has a first arena matrix and symbolic thresholds. No exact-zero or local-GR claim is made.

Next: `{NEXT_TARGET}`.
""",
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                CLAIM_ID,
                "local_gr_empirical_interface",
                "4634 creates the first epsilon_A local bound matrix while preserving the parent no-slot exact-zero fork.",
                "Generated source register, parent no-slot evaluation, bound matrix, symbolic thresholds, runner results, controls, blockers, promotion gates, decision, status, next target and validation.",
                "epsilonA_first_bound_matrix_nonclaim",
                NEXT_TARGET,
                "Scoring local-GR/R10/WEP/PPN before epsilon/Z/C_N/lambda/projection inputs are source-backed.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No local-GR/Newton/PPN/R10 pass until exact-zero no-slot theorem is signed or the matrix passes with source-backed inputs.",
            ])


def validation_rows(groups: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
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

    all_sources = all(row["path_exists"] and row["needle_found"] for row in groups["sources"])
    add("VAL4634_00_sources_exist_and_needles_found", all_sources, "all cited paths/needles found" if all_sources else "missing source path or needle")

    csv_paths = [
        SOURCE_REGISTER,
        NO_SLOT_CSV,
        BOUND_MATRIX_CSV,
        THRESHOLD_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            details.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    add("VAL4634_01_csv_parse", parse_ok, ";".join(details))

    matrix_text = read_text(BOUND_MATRIX_CSV)
    runner_text = read_text(RUNNER_CSV)
    add("VAL4634_02_matrix_has_core_arenas", all(token in matrix_text for token in ["BM4634_0_R10", "BM4634_1_WEP", "BM4634_2_PPN", "BM4634_3_clocks", "BM4634_4_orbital"]), "R10/WEP/PPN/clock/orbital matrix rows present")
    add("VAL4634_03_live_branch_fails_closed", "RUN4634_0_current_live_R10" in runner_text and "FAIL_CLOSED_MISSING_INPUT" in runner_text, "current live branch fails closed")
    add("VAL4634_04_runner_controls", all(token in runner_text for token in ["PASS_R10_ANCHOR_SMOKE_ONLY_NONCLAIM", "FAIL_R10_ALPHA_ABOVE_ANCHOR", "FAIL_R10_RANGE_ABOVE_ANCHOR"]), "R10 pass/fail controls present")
    add("VAL4634_05_symbolic_thresholds", "TH4634_0_R10_anchor_epsilon_product" in read_text(THRESHOLD_CSV), "symbolic R10 epsilon threshold present")
    add("VAL4634_06_no_slot_unsigned", "ZERO_IMPORT_REFUSED" in read_text(NO_SLOT_CSV), "current no-slot zero import refused")

    generated_groups = list(groups.values())
    no_claims = not any(any_claim_true(group) for group in generated_groups)
    add("VAL4634_07_all_rows_nonclaim", no_claims, "no generated row promotes a claim")
    add("VAL4634_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4634_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4634_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4634_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4634_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4634_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4634_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4634_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))

    overall = all(row["status"] == "PASS" for row in checks)
    add("VAL4634_OVERALL", overall, "4634 epsilonA first bound matrix checkpoint")
    return checks


def main() -> None:
    now = utc_now()
    groups = {
        "sources": source_rows(now),
        "no_slot": no_slot_rows(now),
        "bound_matrix": bound_matrix_rows(now),
        "thresholds": threshold_rows(now),
        "runner": runner_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotions": promotion_rows(now),
        "decisions": decision_rows(now),
        "statuses": status_rows(now),
        "nexts": next_rows(now),
    }

    write_csv(SOURCE_REGISTER, groups["sources"])
    write_csv(NO_SLOT_CSV, groups["no_slot"])
    write_csv(BOUND_MATRIX_CSV, groups["bound_matrix"])
    write_csv(THRESHOLD_CSV, groups["thresholds"])
    write_csv(RUNNER_CSV, groups["runner"])
    write_csv(CONTROL_CSV, groups["controls"])
    write_csv(BLOCKERS_CSV, groups["blockers"])
    write_csv(PROMOTION_CSV, groups["promotions"])
    write_csv(DECISION_CSV, groups["decisions"])
    write_csv(STATUS_CSV, groups["statuses"])
    write_csv(NEXT_CSV, groups["nexts"])

    write_doc(now, groups)
    write_formal()
    append_integrations()
    write_csv(VALIDATION_CSV, validation_rows(groups))

    print(f"4634 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
