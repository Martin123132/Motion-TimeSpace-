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

CHECKPOINT = "4632"
CLAIM_ID = "L-474"
BRANCH_ID = "MTS_R2FR_Y5_IQ_SIGNATURE_OR_EPSILONA_RUNNER_4632"
MARKER = "PPC4161_PARENT_VERTICAL_INVOLUTION_SIGNATURE_HUNT_OR_EPSILONA_BOUND_RUNNER_4632"
PACKET_MARKER = "PPC4161_PACKET_IQ_SIGNATURE_OR_EPSILONA_RUNNER_4632"
DECISION = "FULL_IQ_SIGNATURE_NOT_SOURCED_EPSILONA_BOUND_RUNNER_READY_NONCLAIM"
NEXT_TARGET = "4633-Y5-R2FR-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md"

DOC_PATH = POST / "4632-Y5-R2FR-parent-vertical-involution-signature-hunt-or-epsilonA-bound-runner.md"
FORMAL_PATH = FORMAL / "648-PPC4161-parent-vertical-involution-signature-hunt-or-epsilonA-bound-runner.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4632_SOURCE_REGISTER.csv"
HUNT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_IQ_SIGNATURE_HUNT_ROWS.csv"
SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_SIGNATURE_DECISION_MATRIX.csv"
INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_EPSILONA_BOUND_INPUT_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_EPSILONA_BOUND_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4632_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4632_VALIDATION.csv"

CSV_4631_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4631_NEXT_TARGET.csv"
CSV_4631_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4631_VALIDATION.csv"
CSV_4631_SYMMETRY = SOURCE_DIR / "P8_Y5_R2FR_4631_SYMMETRY_ROUTE_AUDIT.csv"
CSV_4631_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4631_BRANCH_EXTREMUM_DERIVATION_ROWS.csv"
CSV_4631_EPSILON = SOURCE_DIR / "P8_Y5_R2FR_4631_EPSILON_A_COEFFICIENT_FILL_ROWS.csv"
CSV_4630_LOCAL_GR = SOURCE_DIR / "P8_Y5_R2FR_4630_CONDITIONAL_LOCAL_GR_THEOREM_ROWS.csv"
CSV_4629_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4629_FIRST_ANCHOR_SMOKE_RUNNER_RESULTS.csv"
CSV_4526_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4526_VERTICAL_INVOLUTION_SOURCE_HUNT.csv"
CSV_4526_BRIDGE = SOURCE_DIR / "P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv"
CSV_4526_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4526_FIRST_SOURCE_NORMALIZED_COEFFICIENT_ROWS.csv"
CSV_4525_SIGNATURE = SOURCE_DIR / "P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv"
CSV_4195_SIGNATURE = SOURCE_DIR / "P8_Y5_R2FR_4195_PARENT_SIGNATURE_AUDIT.csv"
CSV_1451_REQ = SOURCE_DIR / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv"
CSV_1451_SIGN = SOURCE_DIR / "P8_Y5_R10_1451_SIGNOFF_MATRIX.csv"

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
        if not text or "MISSING" in text or text.lower() in {"none", "nan", "exact_zero_theorem"}:
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4632_00_4631_next", CSV_4631_NEXT, "4632-Y5-R2FR-parent-vertical-involution-signature-hunt-or-epsilonA-bound-runner.md", "4631 selected 4632 target."),
        ("SRC4632_01_4631_validation", CSV_4631_VALIDATION, "VAL4631_OVERALL", "4631 validation."),
        ("SRC4632_02_4631_strong", CSV_4631_SYMMETRY, "SYM4631_0_strong_parent_vertical_involution", "strong I_q route."),
        ("SRC4632_03_4631_weak_reject", CSV_4631_SYMMETRY, "REJECTED_FOR_BETA_VISIBLE_ZERO", "weak route rejection."),
        ("SRC4632_04_4631_beta_zero", CSV_4631_DERIVATION, "DER4631_1_beta_visible_zero", "conditional beta zero derivation."),
        ("SRC4632_05_4631_epsilon", CSV_4631_EPSILON, "EPS4631_0_epsilon_A", "epsilon_A fallback."),
        ("SRC4632_06_4630_local_gr", CSV_4630_LOCAL_GR, "TGR4630_0_conditional_statement", "local-GR insert target."),
        ("SRC4632_07_4526_hunt", CSV_4526_HUNT, "HUNT4526_4_parent_action_invariance", "prior parent action invariance missing."),
        ("SRC4632_08_4526_bridge", CSV_4526_BRIDGE, "BRG4526_2_scalar_channel_obstruction", "scalar-channel obstruction."),
        ("SRC4632_09_4526_coeff", CSV_4526_COEFF, "COF4526_6_total_symmetry_breaking_bound", "coefficient fallback envelope."),
        ("SRC4632_10_4525_sig", CSV_4525_SIGNATURE, "SIG4525_0_vertical_involution", "full vertical involution requirement."),
        ("SRC4632_11_4195_sig", CSV_4195_SIGNATURE, "SIG4195_0_parent_action", "leakage parent action invariance missing."),
        ("SRC4632_12_4629_runner", CSV_4629_RUNNER, "SMK4629_0_current_placeholder", "current branch fail-closed runner."),
        ("SRC4632_13_1451_req_optional", CSV_1451_REQ, "epsilon_A", "older epsilon_A bound input requirements if present."),
        ("SRC4632_14_1451_sign_optional", CSV_1451_SIGN, "epsilon_A=0", "older epsilon_A signoff matrix if present."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        optional = source_id.endswith("_optional")
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "optional": optional,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def hunt_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "HUNT4632_0_full_Iq_action_invariance",
            "target_signature": "S_parent[q,z,Psi]=S_parent[q,-z,Psi] under a full I_q on ker(Dq)",
            "evidence_path": str(CSV_4525_SIGNATURE),
            "evidence_needle": "SIG4525_0_vertical_involution",
            "found_status": "REQUIRED_BUT_NOT_FOUND_IN_PRIOR_SOURCE_AUDIT",
            "effect": "cannot promote beta_visible=0 from full parent symmetry",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "HUNT4632_1_even_matter_scale",
            "target_signature": "A_m(q,z)=A_m(q,-z) or no source-only visible matter scale slot",
            "evidence_path": str(CSV_4631_DERIVATION),
            "evidence_needle": "DER4631_0_even_matter_scale",
            "found_status": "THEOREM_SHAPE_DERIVED_PARENT_SIGNATURE_MISSING",
            "effect": "beta_visible zero remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "HUNT4632_2_leakage_subbundle_bridge",
            "target_signature": "R_L extends to full I_q via z_L=P_L z and q o I_q=q",
            "evidence_path": str(CSV_4526_BRIDGE),
            "evidence_needle": "BRG4526_0_embedding",
            "found_status": "CONDITIONAL_BRIDGE_ONLY",
            "effect": "useful route, but not a full scalar/matter proof",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "HUNT4632_3_weak_symmetry_block",
            "target_signature": "ordinary leakage-frame symmetry kills visible scalar beta",
            "evidence_path": str(CSV_4526_BRIDGE),
            "evidence_needle": "BRG4526_2_scalar_channel_obstruction",
            "found_status": "REJECTED",
            "effect": "scalar beta channel must be zeroed by stronger parent signature or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "HUNT4632_4_epsilonA_bound_route",
            "target_signature": "co-normalized epsilon_A bound fallback",
            "evidence_path": str(CSV_4631_EPSILON),
            "evidence_needle": "EPS4631_0_epsilon_A",
            "found_status": "FALLBACK_READY_NONCLAIM",
            "effect": "build bound runner rather than pretending exact local-GR proof exists",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def signature_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIG4632_0_full_Iq",
            "needed": "I_q exists on full local vertical kernel with I_q^2=1 and q o I_q=q",
            "current_evidence": "only conditional theorem/bridge; prior source audit marks full parent signature not found",
            "signed_now": False,
            "if_signed": "beta_visible exact-zero route can progress",
            "if_unsigned": "epsilon_A bound route stays live",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIG4632_1_even_Am",
            "needed": "visible matter scale A_m descends as I_q-even or has no vertical source slot",
            "current_evidence": "4631 derives consequence; no parent source signs premise",
            "signed_now": False,
            "if_signed": "beta_visible=0 follows algebraically",
            "if_unsigned": "epsilon_A := ||P_vert d ln A_m|| must be bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIG4632_2_positive_gap",
            "needed": "Z_mem>0 and M2_mem>0 on same branch",
            "current_evidence": "4628/4630 define ratio and positive branch, numeric parent values missing",
            "signed_now": False,
            "if_signed": "lambda_mem can be evaluated",
            "if_unsigned": "range rows remain placeholder",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIG4632_3_source_boundary_silence",
            "needed": "explicit EM/hidden/source and boundary channels silent on same branch",
            "current_evidence": "prior Poynting/wave/source ledgers keep finite residual branches",
            "signed_now": False,
            "if_signed": "local-GR theorem can close with exact beta zero",
            "if_unsigned": "residual vector feeds bound route",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def input_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4632_0_epsilonA",
            "symbol": "epsilon_A",
            "definition": "visible source/test matter-scale vertical derivative norm",
            "value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "units": "dimensionless",
            "feeds": "alpha_AB <= C_N epsilon_A epsilon_B/Z_min",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4632_1_epsilonB",
            "symbol": "epsilon_B",
            "definition": "second body/test sensitivity derivative norm",
            "value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "units": "dimensionless",
            "feeds": "alpha_AB <= C_N epsilon_A epsilon_B/Z_min",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4632_2_Zmin",
            "symbol": "Z_min",
            "definition": "same-branch lower kinetic Hessian bound",
            "value": "MISSING_ZMEM_PARENT_VALUE",
            "units": "parent normalization",
            "feeds": "alpha_AB and lambda_mem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4632_3_lambda",
            "symbol": "lambda_mem",
            "definition": "same-branch finite range",
            "value": "MISSING_ZMEM_M2MEM_RATIO",
            "units": "m",
            "feeds": "R10/PPN/orbital range gate",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "IN4632_4_CN",
            "symbol": "C_N",
            "definition": "Newton/Planck normalization convention for alpha_AB",
            "value": "MISSING_CONVENTION_OR_CALIBRATION",
            "units": "dimensionless after convention",
            "feeds": "alpha_AB",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def eval_case(case_id: str, case: str, epsilon_a: Any, epsilon_b: Any, z_min: Any, c_n: Any, lambda_m: Any, now: str) -> dict[str, Any]:
    eps_a = numeric(epsilon_a)
    eps_b = numeric(epsilon_b)
    z_value = numeric(z_min)
    c_value = numeric(c_n)
    lam = numeric(lambda_m)
    lambda_anchor = 3.86e-05
    if case_id == "RUN4632_1_exact_Iq_zero":
        alpha = 0.0
        result = "CONDITIONAL_EXACT_ZERO_PASS_ALGEBRA_ONLY"
        reason = "full I_q-even matter descent would make epsilon_A=epsilon_B=0; parent signature is not currently sourced"
    elif None in {eps_a, eps_b, z_value, c_value, lam} or z_value == 0:
        alpha = "MISSING"
        result = "FAIL_CLOSED_MISSING_INPUT"
        reason = "epsilon_A/epsilon_B/Z_min/C_N/lambda_mem are not all numeric and sourced"
    else:
        alpha = c_value * eps_a * eps_b / z_value
        if alpha <= 1.0 and lam <= lambda_anchor:
            result = "PASS_ANCHOR_SMOKE_ONLY_NONCLAIM"
            reason = "control branch passes alpha<=1 and lambda<=38.6e-6 m; full curve still required for claim"
        elif alpha > 1.0:
            result = "FAIL_ALPHA_ABOVE_ANCHOR"
            reason = "co-normalized alpha_AB exceeds alpha=1 anchor threshold"
        else:
            result = "FAIL_RANGE_ABOVE_ANCHOR"
            reason = "lambda_mem exceeds conservative alpha=1 anchor range"
    return {
        "checkpoint": CHECKPOINT,
        "run_id": case_id,
        "case": case,
        "epsilon_A": epsilon_a,
        "epsilon_B": epsilon_b,
        "Z_min": z_min,
        "C_N": c_n,
        "lambda_mem_m": lambda_m,
        "alpha_AB_bound": alpha,
        "lambda_anchor_m": lambda_anchor,
        "result": result,
        "reason": reason,
        "valid_for_claim": False,
        "claim_allowed": False,
        "timestamp_utc": now,
    }


def runner_rows(now: str) -> list[dict[str, Any]]:
    return [
        eval_case("RUN4632_0_current_live_branch", "current placeholders from 4631/4628/4629", "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND", "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND", "MISSING_ZMEM_PARENT_VALUE", "MISSING_CONVENTION_OR_CALIBRATION", "MISSING_ZMEM_M2MEM_RATIO", now),
        eval_case("RUN4632_1_exact_Iq_zero", "full I_q-even A_m theorem if parent-signed", 0.0, 0.0, "any_positive", 1.0, "any_finite", now),
        eval_case("RUN4632_2_small_epsilon_short_range_control", "control: small epsilon and short range", 0.01, 0.01, 1.0, 1.0, 1.93e-05, now),
        eval_case("RUN4632_3_order_one_epsilon_short_range_control", "control: order-one epsilon even at short range", 1.0, 1.0, 0.5, 1.0, 1.93e-05, now),
        eval_case("RUN4632_4_small_epsilon_long_range_control", "control: small epsilon but long range", 0.01, 0.01, 1.0, 1.0, 7.72e-05, now),
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4632_0_no_signature_no_zero",
            "rule": "Do not set epsilon_A=0 unless full I_q/even-A_m or no-source-slot signature is parent-signed.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4632_1_no_bound_without_convention",
            "rule": "Do not score alpha_AB until epsilon_A, epsilon_B, Z_min, C_N and lambda_mem are co-normalized.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4632_2_anchor_not_full_curve",
            "rule": "An alpha=1 short-range pass is smoke only; full R10 alpha(lambda) curve is still required.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4632_0_Iq_signature",
            "blocks": "exact beta_visible zero",
            "missing": "full parent I_q action/measure/projector/boundary and even-A_m descent",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4632_1_epsilon_numeric",
            "blocks": "bound runner live evaluation",
            "missing": "epsilon_A/epsilon_B numeric values or theorem-zero, Z_min, C_N, lambda_mem",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4632_2_bound_curve",
            "blocks": "R10/local-G claim",
            "missing": "full source-backed alpha(lambda) curve beyond anchor smoke",
            "next_action": "after parent coefficients exist",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4632_0_exact_zero",
            "promotion_condition": "Full parent I_q/even-A_m signature is found and paired with positive gap/source-boundary silence.",
            "current_result": "blocked signature not sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4632_1_epsilon_bound",
            "promotion_condition": "epsilon_A, epsilon_B, Z_min, C_N and lambda_mem become parent-owned numeric/source-backed rows and pass bound runners.",
            "current_result": "blocked numeric inputs missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4632_0",
            "decision": DECISION,
            "meaning": "The current corpus does not source the full parent I_q/even-A_m signature. The branch therefore keeps the exact-zero route conditional and activates the epsilon_A co-normalized bound runner, which fails the live branch closed but distinguishes control pass/fail cases.",
            "status": "NONCLAIM_SIGNATURE_HUNT_AND_RUNNER_ADVANCE",
            "best_route": "bridge no-source-slot/common-measure work into even-A_m or fill epsilon_A bound inputs",
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
            "status": "PRIVATE_NONCLAIM_SIGNATURE_HUNT_AND_BOUND_RUNNER",
            "summary": "full I_q/even-A_m signature not sourced; epsilon_A bound runner created and live branch fails closed",
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
            "reason": "4632 converts the unsigned symmetry into a concrete fork: prove even-A_m/no-source-slot, or acquire epsilon_A/Z/lambda/C_N rows.",
            "derive_first": "try no-source-slot/common-measure bridge to A_m even descent",
            "fallback": "fill epsilon_A bound inputs and run R10/WEP/PPN/clocks/orbital matrix",
            "valid_for_claim": False,
        }
    ]


def write_doc(now: str, groups: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4632 - Parent Vertical Involution Signature Hunt Or EpsilonA Bound Runner

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

4632 performs the hard fork after 4631.

The source hunt does **not** find a currently signed full parent `I_q`/even-`A_m` signature. It finds only conditional theorem shapes and prior audits that explicitly keep the full parent action invariance unsigned.

Therefore:

- Exact `beta_visible=0` remains conditional.
- Weak leakage-frame symmetry remains rejected for scalar beta zero.
- The bound route is now executable as a fail-closed `epsilon_A` runner:

`epsilon_A := ||P_vert d ln A_m/dz|0||`

`alpha_AB <= C_N epsilon_A epsilon_B / Z_min`

with the same `lambda_mem=sqrt(Z_mem/M2_mem)` range gate.

The live branch fails closed because `epsilon_A`, `epsilon_B`, `Z_min`, `C_N`, and `lambda_mem` are not yet co-normalized parent-owned numbers.

## Source Register

{markdown_table(groups["sources"])}

## Iq Signature Hunt

{markdown_table(groups["hunt"])}

## Signature Decision Matrix

{markdown_table(groups["signatures"])}

## Epsilon-A Bound Inputs

{markdown_table(groups["inputs"])}

## Epsilon-A Bound Runner

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
    body = f"""# 648 - PPC4161 Parent Vertical Involution Signature Hunt Or EpsilonA Bound Runner

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

4632 result: the current corpus does not source the full parent `I_q`/even-`A_m` signature needed to promote `beta_visible=0`.

The exact-zero route is retained only as a conditional theorem. The live route is the explicit co-normalized bound branch:

`epsilon_A := ||P_vert d ln A_m/dz|0||`

`alpha_AB <= C_N epsilon_A epsilon_B/Z_min`

with `lambda_mem=sqrt(Z_mem/M2_mem)`.

The live branch fails closed until `epsilon_A`, `epsilon_B`, `Z_min`, `C_N`, and `lambda_mem` are parent-owned numeric/source-backed rows or exact-zero theorems.

Next target: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, body)


def append_integrations() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Parent Vertical Involution Signature Hunt Or EpsilonA Bound Runner 4632

Marker: `{MARKER}`

4632 searches the available parent-involution/even-matter evidence and does not find a signed full `I_q`/even-`A_m` theorem. The exact-zero branch is retained conditionally; the active nonclaim fallback is now a co-normalized `epsilon_A` bound runner, failing closed until `epsilon_A`, `epsilon_B`, `Z_min`, `C_N`, and `lambda_mem` are real parent-owned rows.

Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet - Iq Signature Or EpsilonA Runner 4632

Marker: `{PACKET_MARKER}`

Local packet update: no closure smuggling. Either prove full parent `I_q`/even visible matter descent, or score a real `epsilon_A` coefficient through the bound matrix. The current live branch fails closed.

Next: `{NEXT_TARGET}`.
""",
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                CLAIM_ID,
                "local_gr_derivation",
                "4632 performs the parent I_q/even-A_m signature hunt and creates the epsilon_A co-normalized bound runner.",
                "Generated source register, signature hunt rows, decision matrix, epsilon input rows, runner results, controls, blockers, promotion gates, decision, status, next target and validation.",
                "Iq_signature_missing_epsilonA_runner_nonclaim",
                NEXT_TARGET,
                "Treating conditional I_q/even-A_m theorem shape as sourced, or scoring epsilon_A without co-normalized inputs.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No local-GR/Newton/PPN/R10 pass until exact-zero signature is sourced or epsilon_A bound route passes with source-backed values.",
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

    required_sources = [row for row in groups["sources"] if not row["optional"]]
    all_sources = all(row["path_exists"] and row["needle_found"] for row in required_sources)
    add("VAL4632_00_required_sources_exist_and_needles_found", all_sources, "all required cited paths/needles found" if all_sources else "missing required source path or needle")

    csv_paths = [
        SOURCE_REGISTER,
        HUNT_CSV,
        SIGNATURE_CSV,
        INPUT_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for path in csv_paths:
        try:
            parse_details.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{path.name}:ERROR:{exc}")
    add("VAL4632_01_csv_parse", parse_ok, ";".join(parse_details))

    add("VAL4632_02_signature_not_sourced", "REQUIRED_BUT_NOT_FOUND_IN_PRIOR_SOURCE_AUDIT" in read_text(HUNT_CSV), "full I_q route not currently sourced")
    add("VAL4632_03_epsilon_inputs_present", "IN4632_0_epsilonA" in read_text(INPUT_CSV), "epsilon_A input row present")
    add("VAL4632_04_live_branch_fails_closed", "RUN4632_0_current_live_branch" in read_text(RUNNER_CSV) and "FAIL_CLOSED_MISSING_INPUT" in read_text(RUNNER_CSV), "current live branch fails closed")
    add("VAL4632_05_runner_controls", "PASS_ANCHOR_SMOKE_ONLY_NONCLAIM" in read_text(RUNNER_CSV) and "FAIL_ALPHA_ABOVE_ANCHOR" in read_text(RUNNER_CSV) and "FAIL_RANGE_ABOVE_ANCHOR" in read_text(RUNNER_CSV), "runner has pass/fail controls")

    generated_groups = list(groups.values())
    no_claims = not any(any_claim_true(group) for group in generated_groups)
    add("VAL4632_06_all_rows_nonclaim", no_claims, "no generated row promotes a claim")
    add("VAL4632_07_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4632_08_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4632_09_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4632_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4632_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4632_12_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4632_13_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4632_14_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))

    overall = all(row["status"] == "PASS" for row in checks)
    add("VAL4632_OVERALL", overall, "4632 Iq signature hunt / epsilonA runner checkpoint")
    return checks


def main() -> None:
    now = utc_now()
    groups = {
        "sources": source_rows(now),
        "hunt": hunt_rows(now),
        "signatures": signature_rows(now),
        "inputs": input_rows(now),
        "runner": runner_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotions": promotion_rows(now),
        "decisions": decision_rows(now),
        "statuses": status_rows(now),
        "nexts": next_rows(now),
    }

    write_csv(SOURCE_REGISTER, groups["sources"])
    write_csv(HUNT_CSV, groups["hunt"])
    write_csv(SIGNATURE_CSV, groups["signatures"])
    write_csv(INPUT_CSV, groups["inputs"])
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

    print(f"4632 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
