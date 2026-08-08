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

CHECKPOINT = "4633"
CLAIM_ID = "L-475"
BRANCH_ID = "MTS_R2FR_Y5_EPSILONA_NO_SLOT_BRIDGE_4633"
MARKER = "PPC4161_EPSILONA_BOUND_INPUT_ACQUISITION_OR_NO_SOURCE_SLOT_BRIDGE_4633"
PACKET_MARKER = "PPC4161_PACKET_EPSILONA_NO_SLOT_BRIDGE_4633"
DECISION = "NO_SOURCE_SLOT_BRIDGE_SHARP_BUT_UNSIGNED_EPSILONA_ACQUISITION_MANIFEST_READY"
NEXT_TARGET = "4634-Y5-R2FR-epsilonA-first-bound-matrix-or-parent-no-slot-signature.md"

DOC_PATH = POST / "4633-Y5-R2FR-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md"
FORMAL_PATH = FORMAL / "649-PPC4161-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4633_SOURCE_REGISTER.csv"
BRIDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_NO_SOURCE_SLOT_TO_EVEN_AM_BRIDGE_ROWS.csv"
SIGNING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_PARENT_SIGNING_MATRIX.csv"
ACQUISITION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_EPSILONA_INPUT_ACQUISITION_MANIFEST.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_ARENA_READINESS_ROWS.csv"
EVAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_BRIDGE_OR_BOUND_EVALUATION.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4633_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4633_VALIDATION.csv"

CSV_4632_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4632_NEXT_TARGET.csv"
CSV_4632_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4632_VALIDATION.csv"
CSV_4632_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4632_EPSILONA_BOUND_INPUT_ROWS.csv"
CSV_4632_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4632_EPSILONA_BOUND_RUNNER_RESULTS.csv"
CSV_4632_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4632_IQ_SIGNATURE_HUNT_ROWS.csv"
CSV_4631_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4631_BRANCH_EXTREMUM_DERIVATION_ROWS.csv"
CSV_4626_ANCHORS = SOURCE_DIR / "P8_Y5_R2FR_4626_SOURCE_BACKED_BOUND_ANCHORS.csv"
CSV_4626_MAP = SOURCE_DIR / "P8_Y5_R2FR_4626_LOCAL_G_BOUND_MAP_ROWS.csv"
CSV_4628_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_1451_THEOREM = SOURCE_DIR / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv"
CSV_1451_MATRIX = SOURCE_DIR / "P8_Y5_R10_1451_SOURCE_ONLY_SLOT_REDUCTION_MATRIX.csv"
CSV_1451_REQ = SOURCE_DIR / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv"
CSV_1451_SIGN = SOURCE_DIR / "P8_Y5_R10_1451_PARENT_SIGNING_DECISION.csv"
CSV_1452_THEOREM = SOURCE_DIR / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
CSV_1452_AUDIT = SOURCE_DIR / "P8_Y5_R10_1452_ACTION_SCALE_MEASURE_AUDIT.csv"
CSV_1452_UPDATE = SOURCE_DIR / "P8_Y5_R10_1452_EPSILON_JA_REQUIREMENT_UPDATE.csv"
CSV_1452_SIGN = SOURCE_DIR / "P8_Y5_R10_1452_PARENT_SIGNING_DECISION.csv"
CSV_1453_THEOREM = SOURCE_DIR / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv"
CSV_1453_SIGN = SOURCE_DIR / "P8_Y5_R10_1453_PARENT_SIGNING_DECISION.csv"
CSV_1454_THEOREM = SOURCE_DIR / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv"
CSV_1455_DBP = SOURCE_DIR / "P8_Y5_R10_1455_DERIVATIVE_BEFORE_PROJECTION_THEOREM.csv"

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


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4633_00_4632_next", CSV_4632_NEXT, "4633-Y5-R2FR-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md", "4632 selected 4633 target."),
        ("SRC4633_01_4632_validation", CSV_4632_VALIDATION, "VAL4632_OVERALL", "4632 validation."),
        ("SRC4633_02_4632_inputs", CSV_4632_INPUTS, "IN4632_0_epsilonA", "4632 epsilon_A input row."),
        ("SRC4633_03_4632_runner", CSV_4632_RUNNER, "RUN4632_0_current_live_branch", "4632 live branch fail-closed runner."),
        ("SRC4633_04_4632_hunt", CSV_4632_HUNT, "HUNT4632_0_full_Iq_action_invariance", "4632 Iq signature verdict."),
        ("SRC4633_05_4631_beta", CSV_4631_DERIVATION, "DER4631_1_beta_visible_zero", "4631 beta zero bridge target."),
        ("SRC4633_06_4626_anchors", CSV_4626_ANCHORS, "BA4626_0_R10_EOTWASH_ALPHA1", "source-backed local bound anchors."),
        ("SRC4633_07_4626_map", CSV_4626_MAP, "LGM4626_0_R10_alpha", "local-G observable map."),
        ("SRC4633_08_4628_lambda", CSV_4628_NUMERIC, "LNUM4628_2_lambda", "lambda_mem missing parent ratio."),
        ("SRC4633_09_1451_theorem", CSV_1451_THEOREM, "OG1451_6_verdict", "no-source-only-slot theorem verdict."),
        ("SRC4633_10_1451_matrix", CSV_1451_MATRIX, "SM1451_6_verdict", "source-only slot reduction matrix."),
        ("SRC4633_11_1451_req", CSV_1451_REQ, "REQ1451_0_definition", "epsilon_A bound requirements."),
        ("SRC4633_12_1451_sign", CSV_1451_SIGN, "SIGN1451_0_no_slot", "no-slot sign decision."),
        ("SRC4633_13_1452_theorem", CSV_1452_THEOREM, "CMT1452_6_verdict", "common measure/current verdict."),
        ("SRC4633_14_1452_audit", CSV_1452_AUDIT, "ASA1452_4_verdict", "action-scale owner audit."),
        ("SRC4633_15_1452_update", CSV_1452_UPDATE, "UPD1452_0_epsilon_A", "epsilon/J_A requirement update."),
        ("SRC4633_16_1452_sign", CSV_1452_SIGN, "SIGN1452_0_common_measure", "common-measure signing decision."),
        ("SRC4633_17_1453_theorem", CSV_1453_THEOREM, "CSO1453_1_hilbert_variation", "Hilbert source conditional subtheorem."),
        ("SRC4633_18_1453_sign", CSV_1453_SIGN, "SIGN1453_0_current_owner", "current owner signing decision."),
        ("SRC4633_19_1454_theorem", CSV_1454_THEOREM, "VBR1454_1_variational_identity", "variation-before-readout theorem."),
        ("SRC4633_20_1455_dbp", CSV_1455_DBP, "DBP1455_4_conclusion", "derivative-before-projection conclusion."),
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


def bridge_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": "BR4633_0_no_slot_implies_q_basic_Am",
            "statement": "If ordinary visible matter has no source-only vertical/hidden coefficient slot, then the visible matter scale is q-basic: A_m=A_m(q,theta_fixed).",
            "derivation": "No Hom(hidden/vertical, visible coefficient) plus label-forgotten source category plus common measure/current forbids A_m(q,z,species) dependence on vertical z or source label.",
            "result": "P_vert d ln A_m=0, stronger than even-A_m",
            "current_status": "CONDITIONAL_THEOREM_SHAPE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": "BR4633_1_q_basic_Am_implies_epsilon_zero",
            "statement": "If A_m is q-basic, then epsilon_A=||P_vert d ln A_m||=0.",
            "derivation": "For any vertical v in ker(Dq), dA_m[v]=dA_m[Dq v]=0.",
            "result": "beta_visible=0 and 4631 even-A_m/extremum route is satisfied",
            "current_status": "PROVED_CONDITIONAL_ON_BR4633_0",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": "BR4633_2_hilbert_source_subtheorem",
            "statement": "Once a common S_matter is fixed, Hilbert variation gives one source tensor before readout.",
            "derivation": "T_H is the functional derivative of S_matter with respect to the metric/coframe before material masks or readout maps.",
            "result": "post-variation c_A cannot redefine the parent source",
            "current_status": "USEFUL_CONDITIONAL_SUBTHEOREM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": "BR4633_3_pre_action_weight_obstruction",
            "statement": "A pre-variation S_matter=sum_A w_A S_A is still a legal countermodel unless the no-source-slot grammar forbids it.",
            "derivation": "Classical matter EOM may be unchanged, but Hilbert variation gives T_source=sum_A w_A T_A.",
            "result": "epsilon_A cannot be killed by covariance or field equations alone",
            "current_status": "OBSTRUCTION_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": "BR4633_4_bridge_verdict",
            "statement": "No-source-slot would bridge to even-A_m and exact epsilon_A=0, but current corpus does not sign the required premises.",
            "derivation": "1451/1452 signing decisions refuse zero import because no-hidden-visible-Hom, label forgetting, common measure/current and non-Hilbert guard are unsigned.",
            "result": "keep epsilon_A acquisition manifest live",
            "current_status": "ZERO_IMPORT_REFUSED_BOUND_ROUTE_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def signing_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIGN4633_0_no_hidden_visible_Hom",
            "needed_for": "A_m q-basic / no source-only slot",
            "current_state": "UNSIGNED_AX1090_1",
            "evidence": "OG1451_1_visible_coefficient_algebra",
            "epsilon_zero_allowed": False,
            "next_action": "source parent coefficient grammar or keep epsilon_A",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIGN4633_1_label_forgetting",
            "needed_for": "species labels cannot form source coefficients",
            "current_state": "UNSIGNED",
            "evidence": "OG1451_2_species_label_domain",
            "epsilon_zero_allowed": False,
            "next_action": "derive source category forgets material labels before variation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIGN4633_2_common_measure_current",
            "needed_for": "no species action scale/J_A/c_A source normalization",
            "current_state": "UNSIGNED_AX1090_2",
            "evidence": "CMT1452_6_verdict",
            "epsilon_zero_allowed": False,
            "next_action": "source hbar_parent/measure/current owner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIGN4633_3_variation_before_readout",
            "needed_for": "post-variation readout cannot re-enter source",
            "current_state": "CONDITIONAL_SUBTHEOREM_UNSIGNED_DOMAIN",
            "evidence": "VBR1454_1_variational_identity; DBP1455_4_conclusion",
            "epsilon_zero_allowed": False,
            "next_action": "sign parent action/domain order and official readout separation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "signature_id": "SIGN4633_4_nonHilbert_guard",
            "needed_for": "no bypass of Hilbert source theorem",
            "current_state": "OPEN",
            "evidence": "CMT1452_5_nonHilbert_bypass",
            "epsilon_zero_allowed": False,
            "next_action": "prove non-Hilbert currents absent/exact/projected silent or bound zeta_A",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def acquisition_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": "ACQ4633_0_parent_zero_route",
            "symbol": "epsilon_A=0",
            "needed_input": "signed no-source-slot / q-basic A_m theorem",
            "candidate_source": "1451 no-source-only-slot + 1452 common measure/current + 1454/1455 variation-before-readout",
            "current_status": "THEOREM_SHAPE_READY_SIGNATURES_UNSIGNED",
            "next_action": "try to source no-hidden-visible-Hom and common measure/current owner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "ACQ4633_1_epsilon_convention",
            "symbol": "epsilon_A, epsilon_B",
            "needed_input": "reference convention, source/test body classes, common-mode removal",
            "candidate_source": "1451 requirement rows",
            "current_status": "MISSING_CONVENTION_AND_PARENT_ZERO",
            "next_action": "define ordinary-visible material/source basis and no-cancellation norm",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "ACQ4633_2_Zmin",
            "symbol": "Z_min",
            "needed_input": "same-branch kinetic Hessian lower bound",
            "candidate_source": "4628 parent Hessian row",
            "current_status": "MISSING_PARENT_HESSIAN_VALUE",
            "next_action": "derive from parent quadratic memory action or keep Z_min symbolic in bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "ACQ4633_3_lambda_mem",
            "symbol": "lambda_mem",
            "needed_input": "M2_mem/Z_mem ratio or exact short-range theorem",
            "candidate_source": "4628 lambda row",
            "current_status": "MISSING_ZMEM_M2MEM_RATIO",
            "next_action": "fill parent gap ratio or use source-backed anchor only for nonclaim smoke",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "ACQ4633_4_C_N",
            "symbol": "C_N",
            "needed_input": "Newton/Planck normalization convention mapping beta/Z to alpha_AB",
            "candidate_source": "4630 alpha_AB invariant row plus calibrated local G branch",
            "current_status": "MISSING_CONVENTION_OR_CALIBRATION",
            "next_action": "define C_N in the same convention as the R10/Yukawa comparator",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "ACQ4633_5_alpha_curve",
            "symbol": "alpha_bound(lambda)",
            "needed_input": "full source-backed R10 alpha(lambda) curve",
            "candidate_source": "4626 Eot-Wash alpha=1 anchor",
            "current_status": "ANCHOR_ONLY_FULL_CURVE_MISSING",
            "next_action": "digitize/acquire full curve after MTS lambda/alpha inputs exist",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def arena_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "ARENA4633_0_R10",
            "arena": "R10 short-range",
            "available_bound": "BA4626_0_R10_EOTWASH_ALPHA1 anchor",
            "needed_projection": "alpha_AB(lambda)=C_N epsilon_A epsilon_B/Z_min plus lambda_mem",
            "readiness": "SMOKE_ONLY_ANCHOR_FULL_CURVE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "ARENA4633_1_WEP",
            "arena": "MICROSCOPE/WEP",
            "available_bound": "BA4626_1_WEP_MICROSCOPE_TiPt conservative eta gate",
            "needed_projection": "Ti/Pt sensitivity map and epsilon source/test convention",
            "readiness": "BOUND_ANCHOR_EXISTS_PROJECTION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "ARENA4633_2_PPN",
            "arena": "Cassini/PPN",
            "available_bound": "BA4626_2_PPN_CASSINI_GAMMA",
            "needed_projection": "c_gamma(lambda) from epsilon_A scalar branch to gamma/beta residual",
            "readiness": "BOUND_ANCHOR_EXISTS_PROJECTION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "ARENA4633_3_clocks",
            "arena": "clock/redshift",
            "available_bound": "none in current local packet",
            "needed_projection": "source potential calibration and clock sensitivity separation",
            "readiness": "BOUND_AND_PROJECTION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "ARENA4633_4_orbital",
            "arena": "orbital/Newtonian",
            "available_bound": "none source-backed in current local packet",
            "needed_projection": "worldtube/Gauss/source-measure law and measured GM calibration",
            "readiness": "BOUND_AND_PROJECTION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def eval_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "eval_id": "EVAL4633_0_no_slot_if_signed",
            "case": "all no-source-slot/common-measure/no-Hom/readout signatures signed",
            "result": "CONDITIONAL_EPSILON_ZERO_ROUTE",
            "meaning": "A_m is q-basic; epsilon_A=0; feeds 4631/4630 exact local-GR route",
            "claim_allowed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "eval_id": "EVAL4633_1_current_corpus",
            "case": "current 1451/1452/1453/1454/1455 evidence",
            "result": "REFUSE_ZERO_IMPORT",
            "meaning": "the theorem shape is sharp but parent signatures remain unsigned",
            "claim_allowed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "eval_id": "EVAL4633_2_bound_route",
            "case": "epsilon_A not zeroed",
            "result": "ACQUIRE_INPUTS_BEFORE_SCORING",
            "meaning": "epsilon_A, epsilon_B, Z_min, lambda_mem, C_N and arena projections are acquisition targets",
            "claim_allowed_now": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4633_0_no_covariance_shortcut",
            "rule": "Do not claim epsilon_A=0 from covariance or unchanged matter EOM; Hilbert variation still sees pre-action weights.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4633_1_no_zero_import",
            "rule": "Do not import no-source-slot zero until no-hidden-visible-Hom, label forgetting, common measure/current and non-Hilbert guard are signed together.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4633_2_anchor_smoke_only",
            "rule": "Do not treat 4626 R10 alpha=1 threshold as a full curve claim.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4633_0_no_slot_signatures",
            "blocks": "epsilon_A exact zero",
            "missing": "no-hidden-visible-Hom, label forgetting, common measure/current, no spurion return, non-Hilbert guard",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4633_1_bound_inputs",
            "blocks": "epsilon_A bound scoring",
            "missing": "epsilon convention, epsilon_A/B, Z_min, lambda_mem, C_N",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4633_2_arena_projections",
            "blocks": "R10/WEP/PPN/clock/orbital claim",
            "missing": "full R10 curve, WEP sensitivity map, PPN projection, clock/orbital source maps",
            "next_action": "after epsilon/Z/lambda/C_N inputs are parent-owned",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4633_0_zero_bridge",
            "promotion_condition": "No-source-slot/common-measure/no-Hom theorem is parent-signed and proves A_m q-basic.",
            "current_result": "blocked unsigned signatures",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4633_1_bound_runner",
            "promotion_condition": "epsilon_A/B, Z_min, lambda_mem and C_N become source-backed and pass arena-specific bound runners.",
            "current_result": "blocked acquisition inputs missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4633_0",
            "decision": DECISION,
            "meaning": "No-source-slot/common-measure work provides the exact bridge that would make A_m q-basic and epsilon_A=0, but current signing decisions refuse zero import. The epsilon_A acquisition manifest is now explicit and arena-separated.",
            "status": "NONCLAIM_BRIDGE_AND_ACQUISITION_ADVANCE",
            "best_route": "attempt parent no-source-slot/common-measure signature first; otherwise fill epsilon_A/Z/lambda/C_N inputs and run matrix",
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
            "status": "PRIVATE_NONCLAIM_BRIDGE_AND_ACQUISITION_ADVANCE",
            "summary": "no-source-slot bridges to q-basic A_m conditionally, zero import refused now, epsilon_A acquisition manifest ready",
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
            "reason": "4633 bridges no-source-slot to q-basic A_m but refuses zero import; next either signs the parent no-slot clauses or instantiates the first bound matrix.",
            "derive_first": "try parent no-hidden-visible-Hom/common-measure/no-source-slot signature",
            "fallback": "build first epsilon_A bound matrix with explicit missing-input failures",
            "valid_for_claim": False,
        }
    ]


def write_doc(now: str, groups: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4633 - EpsilonA Bound Input Acquisition Or No-Source-Slot Bridge

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

4633 connects the old no-source-slot/common-measure work to the new `epsilon_A` branch.

The clean theorem shape is:

`NoSourceOnlySlot + NoHiddenVisibleHom + LabelForgetting + CommonMeasureCurrent + NoSpurionReturn + NonHilbertGuard`

implies

`A_m = A_m(q, theta_fixed)`.

Since vertical directions satisfy `Dq[v]=0`,

`d ln A_m[v] = 0`,

so

`epsilon_A := ||P_vert d ln A_m|| = 0`.

That is stronger than the 4631 even-`A_m` route and would feed the 4630 local-GR theorem.

Current verdict: the bridge is mathematically sharp, but the corpus still refuses zero import because the required parent signatures are unsigned. The bound path therefore stays live, now with an explicit acquisition manifest.

## Source Register

{markdown_table(groups["sources"])}

## No-Source-Slot To Even-A_m Bridge

{markdown_table(groups["bridge"])}

## Parent Signing Matrix

{markdown_table(groups["signing"])}

## Epsilon-A Input Acquisition Manifest

{markdown_table(groups["acquisition"])}

## Arena Readiness

{markdown_table(groups["arena"])}

## Bridge Or Bound Evaluation

{markdown_table(groups["evaluation"])}

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
    body = f"""# 649 - PPC4161 EpsilonA Bound Input Acquisition Or No-Source-Slot Bridge

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

4633 theorem bridge:

If the parent action grammar has no source-only/vertical slot for visible matter coefficients, then `A_m=A_m(q,theta_fixed)`. For every vertical `v in ker(Dq)`, `d ln A_m[v]=0`, hence `epsilon_A=||P_vert d ln A_m||=0`.

Current corpus verdict: zero import is refused because no-hidden-visible-Hom, label forgetting, common measure/current, no-spurion return and non-Hilbert guard are not signed together.

Bound path remains:

`alpha_AB <= C_N epsilon_A epsilon_B/Z_min`,

`lambda_mem=sqrt(Z_mem/M2_mem)`.

Next target: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, body)


def append_integrations() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 EpsilonA Bound Input Acquisition Or No-Source-Slot Bridge 4633

Marker: `{MARKER}`

4633 bridges old no-source-slot/common-measure work to the new memory-source branch: if visible matter coefficients are q-basic and have no source-only vertical slot, then `epsilon_A=0`. The bridge is sharp but unsigned in the current corpus, so the zero import is refused and the explicit acquisition manifest for `epsilon_A`, `Z_min`, `lambda_mem`, `C_N`, and arena projections remains live.

Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet - EpsilonA No-Slot Bridge 4633

Marker: `{PACKET_MARKER}`

Local packet update: the no-source-slot theorem would kill `epsilon_A` by making `A_m` q-basic, but the parent signatures are still unsigned. The bound route is now acquisition-ready rather than vague.

Next: `{NEXT_TARGET}`.
""",
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                CLAIM_ID,
                "local_gr_derivation",
                "4633 bridges no-source-slot/common-measure work to q-basic A_m and prepares the epsilon_A acquisition manifest.",
                "Generated source register, bridge rows, parent signing matrix, acquisition manifest, arena readiness, evaluation, controls, blockers, promotion gates, decision, status, next target and validation.",
                "no_slot_bridge_unsigned_epsilonA_acquisition_nonclaim",
                NEXT_TARGET,
                "Importing epsilon_A=0 before the no-source-slot/common-measure/no-Hom signatures are parent-signed.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No local-GR/Newton/PPN/R10 pass until q-basic A_m is parent-signed or epsilon_A bound matrix passes with source-backed inputs.",
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
    add("VAL4633_00_sources_exist_and_needles_found", all_sources, "all cited paths/needles found" if all_sources else "missing source path or needle")

    csv_paths = [
        SOURCE_REGISTER,
        BRIDGE_CSV,
        SIGNING_CSV,
        ACQUISITION_CSV,
        ARENA_CSV,
        EVAL_CSV,
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
    add("VAL4633_01_csv_parse", parse_ok, ";".join(details))

    add("VAL4633_02_bridge_to_qbasic_Am", "BR4633_0_no_slot_implies_q_basic_Am" in read_text(BRIDGE_CSV), "no-slot to q-basic A_m bridge present")
    add("VAL4633_03_zero_import_refused", "ZERO_IMPORT_REFUSED_BOUND_ROUTE_ACTIVE" in read_text(BRIDGE_CSV), "zero import refused in current corpus")
    add("VAL4633_04_acquisition_manifest_core", all(token in read_text(ACQUISITION_CSV) for token in ["ACQ4633_1_epsilon_convention", "ACQ4633_2_Zmin", "ACQ4633_3_lambda_mem", "ACQ4633_4_C_N"]), "core acquisition inputs present")
    add("VAL4633_05_arena_readiness", all(token in read_text(ARENA_CSV) for token in ["ARENA4633_0_R10", "ARENA4633_1_WEP", "ARENA4633_2_PPN"]), "R10/WEP/PPN arena rows present")
    add("VAL4633_06_current_eval_refuses_zero", "REFUSE_ZERO_IMPORT" in read_text(EVAL_CSV), "current evaluation refuses zero import")

    generated_groups = list(groups.values())
    no_claims = not any(any_claim_true(group) for group in generated_groups)
    add("VAL4633_07_all_rows_nonclaim", no_claims, "no generated row promotes a claim")
    add("VAL4633_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4633_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4633_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4633_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4633_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4633_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4633_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4633_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))

    overall = all(row["status"] == "PASS" for row in checks)
    add("VAL4633_OVERALL", overall, "4633 epsilonA bridge/acquisition checkpoint")
    return checks


def main() -> None:
    now = utc_now()
    groups = {
        "sources": source_rows(now),
        "bridge": bridge_rows(now),
        "signing": signing_rows(now),
        "acquisition": acquisition_rows(now),
        "arena": arena_rows(now),
        "evaluation": eval_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotions": promotion_rows(now),
        "decisions": decision_rows(now),
        "statuses": status_rows(now),
        "nexts": next_rows(now),
    }

    write_csv(SOURCE_REGISTER, groups["sources"])
    write_csv(BRIDGE_CSV, groups["bridge"])
    write_csv(SIGNING_CSV, groups["signing"])
    write_csv(ACQUISITION_CSV, groups["acquisition"])
    write_csv(ARENA_CSV, groups["arena"])
    write_csv(EVAL_CSV, groups["evaluation"])
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

    print(f"4633 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
