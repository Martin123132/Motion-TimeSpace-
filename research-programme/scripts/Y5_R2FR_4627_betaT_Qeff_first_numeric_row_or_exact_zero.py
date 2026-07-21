from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4627"
CLAIM_ID = "L-469"
BRANCH_ID = "MTS_R2FR_Y5_BETAT_QEFF_ZERO_OR_FIRST_NUMERIC_4627"
MARKER = "PPC4161_BETAT_QEFF_FIRST_NUMERIC_ROW_OR_EXACT_ZERO_4627"
PACKET_MARKER = "PPC4161_PACKET_BETAT_QEFF_ZERO_OR_FIRST_NUMERIC_4627"
DECISION = "BETAT_QEFF_EXACT_ZERO_ROUTES_AND_FIRST_NUMERIC_TEMPLATE_READY_NONCLAIM"
NEXT_TARGET = "4628-Y5-R2FR-lambda-mem-gap-row-or-Zmem-M2mem-parent-hessian.md"

DOC_PATH = POST / "4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md"
FORMAL_PATH = FORMAL / "643-PPC4161-betaT-Qeff-first-numeric-row-or-exact-zero.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4627_SOURCE_REGISTER.csv"
OWNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_BETAT_OWNER_THEOREM_ROWS.csv"
ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_BETAT_QEFF_ZERO_ROUTES.csv"
NUMERIC_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_QEFF_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
SMOKE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_ANCHOR_SMOKE_EVALUATION_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4627_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4627_VALIDATION.csv"

CSV_4626_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4626_NEXT_TARGET.csv"
CSV_4626_ANCHORS = SOURCE_DIR / "P8_Y5_R2FR_4626_SOURCE_BACKED_BOUND_ANCHORS.csv"
CSV_4626_LOCAL_MAP = SOURCE_DIR / "P8_Y5_R2FR_4626_LOCAL_G_BOUND_MAP_ROWS.csv"
CSV_4626_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4626_MTS_YUKAWA_INPUT_REQUIREMENTS.csv"
CSV_4626_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4626_BOUND_RUNNER_DRYRUN_ROWS.csv"
CSV_4626_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4626_VALIDATION.csv"
CSV_4625_CHARGE = SOURCE_DIR / "P8_Y5_R2FR_4625_TRACE_CHARGE_DERIVATION_ROWS.csv"
CSV_4625_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4625_QMEM_ZERO_ROUTES.csv"
CSV_4625_SCREEN = SOURCE_DIR / "P8_Y5_R2FR_4625_SCREENING_OR_MASS_GAP_ROWS.csv"
CSV_4625_YUKAWA = SOURCE_DIR / "P8_Y5_R2FR_4625_YUKAWA_BOUND_MAPPING_ROWS.csv"
CSV_4623_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4623_PARENT_SELECTION_THEOREMS.csv"
CSV_4623_BETA = SOURCE_DIR / "P8_Y5_R2FR_4623_BETA_OWNERSHIP_MATRIX.csv"
CSV_4623_TRACE = SOURCE_DIR / "P8_Y5_R2FR_4623_TRACE_BRANCH_ROWS.csv"
CSV_4621_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"

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
        ("SRC4627_00_4626_next", CSV_4626_NEXT, "4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md", "4626 selected beta_T/Q_eff target."),
        ("SRC4627_01_4626_anchor", CSV_4626_ANCHORS, "BA4626_0_R10_EOTWASH_ALPHA1", "4626 R10 anchor."),
        ("SRC4627_02_4626_map", CSV_4626_LOCAL_MAP, "LGM4626_0_R10_alpha", "4626 local-G alpha map."),
        ("SRC4627_03_4626_input", CSV_4626_INPUTS, "MIN4626_1_Qeff", "4626 Qeff missing input."),
        ("SRC4627_04_4626_runner", CSV_4626_RUNNER, "RUN4626_1_missing_mts_inputs", "4626 fail-closed runner row."),
        ("SRC4627_05_4626_validation", CSV_4626_VALIDATION, "VAL4626_OVERALL", "4626 validation."),
        ("SRC4627_06_4625_charge", CSV_4625_CHARGE, "QDER4625_0_gauss_law", "4625 Qmem charge law."),
        ("SRC4627_07_4625_trace", CSV_4625_CHARGE, "QDER4625_1_trace_source", "4625 trace charge first estimate."),
        ("SRC4627_08_4625_zero", CSV_4625_ZERO, "QZ4625_0_parent_decoupling", "4625 beta_T zero route."),
        ("SRC4627_09_4625_screen", CSV_4625_SCREEN, "SCR4625_0_large_gap", "4625 large gap route."),
        ("SRC4627_10_4625_yukawa", CSV_4625_YUKAWA, "YB4625_0_alpha_yukawa_map", "4625 Yukawa alpha map."),
        ("SRC4627_11_4623_trace_theorem", CSV_4623_THEOREM, "PSEL4623_1_trace_branch", "4623 trace branch theorem."),
        ("SRC4627_12_4623_betaT", CSV_4623_BETA, "BOWN4623_1_beta_T", "4623 beta_T owner row."),
        ("SRC4627_13_4623_trace", CSV_4623_TRACE, "TR4623_0_minimal_trace_branch", "4623 trace branch row."),
        ("SRC4627_14_4621_Zmem", CSV_4621_SOURCE, "ZMR4621_0_Zmem_min", "4621 Zmem requirement."),
        ("SRC4627_15_4621_M2mem", CSV_4621_SOURCE, "ZMR4621_1_M2mem_min", "4621 M2mem requirement."),
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


def owner_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "owner_id": "BTO4627_0_matter_scale_owner",
            "statement": "beta_T is the selected-branch derivative of the visible matter scale: beta_T := partial_m ln A_m|branch, or the corresponding species mass derivative partial_m ln m_s.",
            "derivation": "In the trace branch, variation of the matter metric/mass scale gives delta S_matter proportional to T_obs delta ln A_m. Therefore beta_T is parent-owned by A_m(m_mem), not an empirical free knob.",
            "result": "BETAT_OWNER_IDENTIFIED",
            "status": "PARENT_A_M_FUNCTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "owner_id": "BTO4627_1_Qmem_to_Qeff",
            "statement": "Q_eff := S_scr Q_mem, with Q_mem ~= beta_T I_T + corrections and I_T := int_body T_obs dV.",
            "derivation": "4625 gives the Gauss/flux charge law; screening, if present, multiplies the exterior integration constant by a parent-derived suppression factor.",
            "result": "QEFF_OWNER_CHAIN_IDENTIFIED",
            "status": "BETAT_I_T_SSCR_NUMERIC_ROWS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "owner_id": "BTO4627_2_universal_trace_split",
            "statement": "Universal beta_T can suppress WEP composition differences if alpha_A=alpha_B, but it does not remove the universal Yukawa/inverse-square residual.",
            "derivation": "eta_AB depends on alpha_A-alpha_B, while alpha_Y depends on alpha_A Q_eff_source. Universality kills the difference channel only.",
            "result": "WEP_ZERO_NOT_LOCAL_G_ZERO",
            "status": "UNIVERSALITY_AND_ALPHA_ROWS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def zero_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "BTZ4627_0_parent_decoupling",
            "target": "beta_T",
            "route": "A_m independent of m_mem",
            "condition": "partial_m ln A_m|branch = 0 and species masses do not depend on m_mem",
            "result": "beta_T=0 and weak trace Q_mem=0",
            "status": "EXACT_IF_PARENT_SIGNED_NOT_CURRENTLY_SIGNED",
            "risk": "removes trace matter coupling; any desired cosmology/local coupling must be owned elsewhere",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "BTZ4627_1_branch_extremum",
            "target": "beta_T",
            "route": "matter-scale extremum/double-zero",
            "condition": "A_m(m)=A0+1/2 A2 delta_m^2+... at the selected branch",
            "result": "partial_m ln A_m|0=0, so first-order beta_T=0",
            "status": "EXACT_CONDITIONAL_EXTREMUM_ROUTE_UNSIGNED",
            "risk": "quadratic trace charge can still source second-order effects if delta_m is not zero",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "BTZ4627_2_memory_parity",
            "target": "beta_T",
            "route": "odd memory / even trace selection symmetry",
            "condition": "m_mem is odd under a parent symmetry while visible matter trace and A_m are even",
            "result": "linear beta_T forbidden",
            "status": "SYMMETRY_ROUTE_OPEN_UNSIGNED",
            "risk": "requires anomaly/readout stability and does not automatically kill even powers",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "QEZ4627_3_parent_screening_zero",
            "target": "Q_eff",
            "route": "S_scr=0 parent screening or no-flux matching",
            "condition": "parent derives a thin-shell/no-flux mechanism forcing the exterior integration constant to vanish",
            "result": "Q_eff=0 even if beta_T I_T is nonzero internally",
            "status": "EXACT_IF_PARENT_SCREENING_SIGNED",
            "risk": "screening cannot be inserted as closure; must come from V_parent/Z_mem/M2_mem/boundary matching",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "QEZ4627_4_body_scalar_neutrality",
            "target": "Q_mem",
            "route": "body scalar neutrality",
            "condition": "beta_T I_T plus binding/frame terms cancel for a specified body class",
            "result": "Q_mem=0 for that source class",
            "status": "BODY_DEPENDENT_NOT_GENERAL",
            "risk": "composition-specific cancellation is dangerous for WEP and cannot support universal local-GR recovery alone",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def numeric_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QNUM4627_0_betaT",
            "symbol": "beta_T",
            "definition": "partial_m ln A_m|branch or species mass derivative",
            "value": "MISSING_PARENT_VALUE_OR_EXACT_ZERO",
            "units": "per memory-field unit",
            "feeds": "Q_mem ~= beta_T I_T",
            "required_source": "parent matter-scale function A_m(m_mem) or exact zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QNUM4627_1_I_T_source",
            "symbol": "I_T_source",
            "definition": "int_body T_obs dV including sign/unit convention and binding/frame corrections",
            "value": "MISSING_BODY_TRACE_INTEGRAL",
            "units": "stress trace times volume",
            "feeds": "Q_mem",
            "required_source": "source body model and trace convention",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QNUM4627_2_Sscr",
            "symbol": "S_scr",
            "definition": "parent-derived exterior charge suppression factor",
            "value": "MISSING_SCREENING_OR_SET_TO_ONE_FOR_UNSCREENED_SMOKE",
            "units": "dimensionless",
            "feeds": "Q_eff = S_scr Q_mem",
            "required_source": "parent screening law or explicit unscreened assumption",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QNUM4627_3_Qeff",
            "symbol": "Q_eff_source",
            "definition": "S_scr * (beta_T I_T_source + corrections)",
            "value": "MISSING_QEFF_OR_EXACT_ZERO",
            "units": "memory charge units",
            "feeds": "alpha_Y and eta_AB",
            "required_source": "beta_T, I_T_source, S_scr and corrections",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QNUM4627_4_alphaA",
            "symbol": "alpha_A, alpha_B",
            "definition": "test-body memory sensitivities",
            "value": "MISSING_UNIVERSAL_OR_COMPOSITION_DEPENDENT_VALUES",
            "units": "dimensionless or per memory-field convention",
            "feeds": "alpha_Y_AB and eta_AB",
            "required_source": "species/universality theorem or material sensitivity rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def smoke_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMK4627_0_exact_zero_branch",
            "case": "beta_T=0 or Q_eff=0 theorem signed",
            "alpha_Y_anchor": 0.0,
            "eta_AB": 0.0,
            "result": "would pass R10/WEP smoke algebraically",
            "claim_status": "BLOCKED_UNTIL_PARENT_ZERO_THEOREM_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMK4627_1_missing_numeric_fail_closed",
            "case": "current first numeric template",
            "alpha_Y_anchor": "MISSING_QEFF_ZMEM_ALPHA_MASS",
            "eta_AB": "MISSING_QEFF_ALPHA_DIFFERENCE_GEOMETRY",
            "result": "must fail closed before comparison",
            "claim_status": "FAIL_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMK4627_2_universal_nonzero",
            "case": "alpha_A=alpha_B and Q_eff nonzero",
            "alpha_Y_anchor": "requires numeric Q_eff/Z_mem/M_source",
            "eta_AB": 0.0,
            "result": "WEP difference can vanish while universal Yukawa/local-G residual remains",
            "claim_status": "BOUND_REQUIRED_NOT_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTL4627_0_no_free_betaT", "rule": "beta_T must come from a parent matter-scale derivative or an exact zero theorem.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4627_1_universal_not_zero", "rule": "Universal trace coupling may remove WEP composition difference but not universal Yukawa/local-G residual.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4627_2_no_screening_closure", "rule": "S_scr=0 or small S_scr must be parent-derived from screening/gap/boundary matching.", "violation_blocks_claim": True, "timestamp_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4627_0_parent_Am", "blocks": "beta_T exact zero or numeric value", "missing": "parent A_m(m_mem) function, extremum/symmetry theorem, or species mass derivative", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4627_1_Qeff_numeric", "blocks": "anchor smoke run", "missing": "I_T_source, S_scr, Q_eff_source, Z_mem, source mass and alpha_A/B", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4627_2_lambda_gap", "blocks": "which empirical bound applies", "missing": "lambda_mem = sqrt(Z_mem/M2_mem) from parent Hessian/gap row", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4627_0_exact_zero", "promotion_condition": "Parent signs beta_T=0, Q_eff=0, or no-flux screening theorem on the same branch.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4627_1_first_numeric_smoke", "promotion_condition": "beta_T, I_T, S_scr, Q_eff, Z_mem, lambda_mem and alpha_A/B numeric rows exist and pass fail-closed schema.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4627_2_universal_trace_bound", "promotion_condition": "Universal sensitivities are derived, WEP eta cancels, and universal alpha_Y passes source-backed local-G bounds.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4627_0",
            "decision": DECISION,
            "meaning": "beta_T and Q_eff now have exact-zero routes and first numeric row templates. Current branch remains nonclaim because parent A_m, Q_eff, sensitivities and lambda_mem are not numeric/source-backed.",
            "status": "NONCLAIM_PRIVATE_DERIVATION_AND_SMOKE_TEMPLATE_STAGE",
            "best_route": "try matter-scale extremum/symmetry or parent decoupling first; otherwise fill numeric Q_eff row after lambda_mem/gap row",
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
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "beta_T owner, Q_eff chain, zero routes and first numeric row templates are written; lambda_mem/Zmem/M2mem gap row is next.",
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
            "reason": "Even with Q_eff owned, empirical comparison needs lambda_mem=sqrt(Z_mem/M2_mem) and a gap/screening row.",
            "derive_first": "derive Z_mem/M2_mem parent Hessian or gap theorem",
            "fallback": "stage first numeric nonclaim lambda_mem row for anchor smoke",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join([
        "# 4627 - betaT/Qeff First Numeric Row Or Exact Zero",
        "",
        f"Timestamp UTC: `{now}`",
        f"Branch: `{BRANCH_ID}`",
        f"Marker: `{MARKER}`",
        f"Decision: `{DECISION}`",
        "",
        "## Result",
        "",
        "4627 attacks the current bottleneck directly: `beta_T` is not a fit knob. It is the branch derivative of the parent matter scale.",
        "",
        "`beta_T := partial_m ln A_m|branch`",
        "",
        "and the exterior charge chain is:",
        "",
        "`Q_mem ~= beta_T I_T_source + corrections`, `Q_eff = S_scr Q_mem`.",
        "",
        "The exact-zero exits are parent decoupling, branch extremum, memory parity, parent screening/no-flux, or body-specific scalar neutrality. If none is signed, the first numeric row is staged but remains fail-closed.",
        "",
        "Important: universal nonzero trace coupling can cancel WEP composition difference but still leaves a universal Yukawa/local-G residual.",
        "",
        "## Sources",
        markdown_table(tables["sources"]),
        "",
        "## betaT Owner Theorem Rows",
        markdown_table(tables["owners"]),
        "",
        "## betaT/Qeff Zero Routes",
        markdown_table(tables["zero"]),
        "",
        "## Qeff First Numeric Template",
        markdown_table(tables["numeric"]),
        "",
        "## Anchor Smoke Evaluation Rows",
        markdown_table(tables["smoke"]),
        "",
        "## Controls",
        markdown_table(tables["controls"]),
        "",
        "## Blockers",
        markdown_table(tables["blockers"]),
        "",
        "## Promotion Gates",
        markdown_table(tables["promotion"]),
        "",
        "## Decision",
        markdown_table(tables["decision"]),
        "",
        "## Status",
        markdown_table(tables["status"]),
        "",
        "## Next Target",
        markdown_table(tables["next"]),
        "",
        "## Claim Safety",
        "",
        "All rows remain `valid_for_claim=false`. Exact-zero routes are conditional; numeric rows are templates until parent values exist.",
    ]).strip() + "\n"


def build_formal(now: str) -> str:
    return f"""# 643 - PPC4161 betaT/Qeff First Numeric Row Or Exact Zero

Timestamp UTC: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Branch: `{BRANCH_ID}`

## betaT/Qeff Gate

`beta_T := partial_m ln A_m|branch`.

`Q_mem ~= beta_T I_T_source + corrections`.

`Q_eff = S_scr Q_mem`.

Exact-zero exits:

1. `partial_m ln A_m=0` by parent matter decoupling;
2. selected branch extremum `A_m=A0+1/2 A2 delta_m^2+...`;
3. odd memory/even matter trace symmetry;
4. parent screening/no-flux gives `S_scr=0`;
5. body-specific scalar neutrality.

If these fail, the first numeric row requires `beta_T`, `I_T_source`, `S_scr`, `Q_eff`, `Z_mem`, `lambda_mem`, and `alpha_A/B`. Missing inputs must fail closed.

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4627 identifies beta_T as a parent matter-scale derivative, builds Q_eff exact-zero routes, and stages fail-closed first numeric rows.",
        "current_evidence": "Generated source register, betaT owner rows, zero routes, Qeff numeric templates, smoke rows, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "betaT_Qeff_zero_or_first_numeric_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating beta_T, screening, or Q_eff as adjustable closure instead of parent-owned quantities.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/Newton/WEP/PPN pass until beta_T/Q_eff/lambda_mem are exact-zero or source-backed numeric rows.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4627_00_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in tables["sources"]), "all cited paths/needles found")
    csv_paths = [SOURCE_REGISTER, OWNER_CSV, ZERO_CSV, NUMERIC_CSV, SMOKE_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    parsed = {path.name: len(read_csv(path)) for path in csv_paths if path.exists()}
    add("VAL4627_01_csv_parse", len(parsed) == len(csv_paths) and all(count > 0 for count in parsed.values()), ";".join(f"{name}:{count}" for name, count in parsed.items()))
    add("VAL4627_02_betat_owner", any(row["owner_id"] == "BTO4627_0_matter_scale_owner" for row in tables["owners"]), "beta_T owner row present")
    add("VAL4627_03_zero_routes", len(tables["zero"]) >= 5 and any(row["zero_id"] == "BTZ4627_1_branch_extremum" for row in tables["zero"]), "zero routes present")
    add("VAL4627_04_numeric_template", len(tables["numeric"]) >= 5 and any(row["symbol"] == "Q_eff_source" for row in tables["numeric"]), "Qeff numeric template present")
    add("VAL4627_05_fail_closed_smoke", any(row["smoke_id"] == "SMK4627_1_missing_numeric_fail_closed" for row in tables["smoke"]), "missing-input fail-closed smoke present")
    add("VAL4627_06_universal_warning", any(row["control_id"] == "CTL4627_1_universal_not_zero" for row in tables["controls"]), "universal trace warning present")
    add("VAL4627_07_all_rows_nonclaim", not any(any_claim_true(rows) for rows in tables.values()), "no generated row promotes a claim")
    add("VAL4627_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4627_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4627_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4627_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4627_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4627_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4627_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4627_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4627_OVERALL", all(row["status"] == "PASS" for row in rows), "4627 betaT/Qeff gate checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "owners": owner_rows(now),
        "zero": zero_rows(now),
        "numeric": numeric_rows(now),
        "smoke": smoke_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(OWNER_CSV, tables["owners"])
    write_csv(ZERO_CSV, tables["zero"])
    write_csv(NUMERIC_CSV, tables["numeric"])
    write_csv(SMOKE_CSV, tables["smoke"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - betaT/Qeff First Numeric Row Or Exact Zero

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4627 identifies `beta_T := partial_m ln A_m|branch` and chains `Q_eff = S_scr Q_mem`, `Q_mem ~= beta_T I_T_source + corrections`. Exact-zero exits are parent decoupling, branch extremum, memory parity, parent screening/no-flux, or body scalar neutrality. If none closes, the first numeric rows remain fail-closed until `beta_T`, `I_T`, `S_scr`, `Q_eff`, `Z_mem`, `lambda_mem`, and sensitivities are source-backed.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - betaT/Qeff First Numeric Row Or Exact Zero

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now has a betaT/Qeff exact-zero-or-first-row gate. Next target: `{NEXT_TARGET}`.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4627 validation failed: {failed}")
    print(f"4627 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
