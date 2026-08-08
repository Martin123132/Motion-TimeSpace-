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

CHECKPOINT = "4628"
CLAIM_ID = "L-470"
BRANCH_ID = "MTS_R2FR_Y5_LAMBDA_MEM_PARENT_HESSIAN_4628"
MARKER = "PPC4161_LAMBDA_MEM_GAP_ROW_OR_ZMEM_M2MEM_PARENT_HESSIAN_4628"
PACKET_MARKER = "PPC4161_PACKET_LAMBDA_MEM_PARENT_HESSIAN_4628"
DECISION = "LAMBDA_MEM_REDUCED_TO_PARENT_HESSIAN_OR_R10_ANCHOR_GAP_TEMPLATE_NONCLAIM"
NEXT_TARGET = "4629-Y5-R2FR-canonical-normalization-and-first-anchor-smoke-runner.md"

DOC_PATH = POST / "4628-Y5-R2FR-lambda-mem-gap-row-or-Zmem-M2mem-parent-hessian.md"
FORMAL_PATH = FORMAL / "644-PPC4161-lambda-mem-gap-row-or-Zmem-M2mem-parent-hessian.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4628_SOURCE_REGISTER.csv"
HESSIAN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
GAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_LAMBDA_MEM_GAP_ROWS.csv"
ANCHOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_R10_ANCHOR_GAP_CONVERSION_ROWS.csv"
NUMERIC_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4628_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4628_VALIDATION.csv"

CSV_4627_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4627_NEXT_TARGET.csv"
CSV_4627_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4627_QEFF_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_4627_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4627_CLAIM_BLOCKERS.csv"
CSV_4627_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4627_VALIDATION.csv"
CSV_4626_ANCHOR = SOURCE_DIR / "P8_Y5_R2FR_4626_SOURCE_BACKED_BOUND_ANCHORS.csv"
CSV_4626_MAP = SOURCE_DIR / "P8_Y5_R2FR_4626_LOCAL_G_BOUND_MAP_ROWS.csv"
CSV_4626_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4626_MTS_YUKAWA_INPUT_REQUIREMENTS.csv"
CSV_4625_SCREEN = SOURCE_DIR / "P8_Y5_R2FR_4625_SCREENING_OR_MASS_GAP_ROWS.csv"
CSV_4625_YUKAWA = SOURCE_DIR / "P8_Y5_R2FR_4625_YUKAWA_BOUND_MAPPING_ROWS.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
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
        ("SRC4628_00_4627_next", CSV_4627_NEXT, "4628-Y5-R2FR-lambda-mem-gap-row-or-Zmem-M2mem-parent-hessian.md", "4627 selected lambda_mem/gap target."),
        ("SRC4628_01_4627_qeff_template", CSV_4627_NUMERIC, "QNUM4627_3_Qeff", "4627 Qeff template."),
        ("SRC4628_02_4627_lambda_blocker", CSV_4627_BLOCKERS, "BLK4627_2_lambda_gap", "4627 lambda gap blocker."),
        ("SRC4628_03_4627_validation", CSV_4627_VALIDATION, "VAL4627_OVERALL", "4627 validation."),
        ("SRC4628_04_4626_anchor", CSV_4626_ANCHOR, "BA4626_0_R10_EOTWASH_ALPHA1", "4626 R10 source-backed anchor."),
        ("SRC4628_05_4626_map", CSV_4626_MAP, "LGM4626_0_R10_alpha", "4626 alpha map."),
        ("SRC4628_06_4626_input", CSV_4626_INPUTS, "MIN4626_0_lambda_mem", "4626 lambda input row."),
        ("SRC4628_07_4625_screen", CSV_4625_SCREEN, "SCR4625_0_large_gap", "4625 large gap route."),
        ("SRC4628_08_4625_yukawa", CSV_4625_YUKAWA, "YB4625_0_alpha_yukawa_map", "4625 Yukawa map."),
        ("SRC4628_09_4621_operator", CSV_4621_IDENTITY, "MPI4621_0_local_memory_operator", "4621 local memory operator."),
        ("SRC4628_10_4621_nohair", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "4621 nohair theorem."),
        ("SRC4628_11_4621_Zmem", CSV_4621_SOURCE, "ZMR4621_0_Zmem_min", "4621 Zmem row."),
        ("SRC4628_12_4621_M2mem", CSV_4621_SOURCE, "ZMR4621_1_M2mem_min", "4621 M2mem row."),
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


def hessian_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "hessian_id": "HES4628_0_quadratic_memory_action",
            "statement": "The local gap must come from the quadratic parent memory action, not from a bound fit.",
            "normal_form": "S_mem^(2)=1/2 int mu_obs [Z_mem h^ij partial_i delta_m partial_j delta_m + M2_mem delta_m^2]",
            "identification": "Z_mem is the kinetic Hessian; M2_mem is the effective branch Hessian/gap.",
            "status": "NORMAL_FORM_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "hessian_id": "HES4628_1_parent_hessian_definitions",
            "statement": "For a parent density L(m,partial m), Z_mem := partial^2 L / partial(partial_i m) partial(partial^i m)|branch and M2_mem := partial^2 V_eff / partial m^2|branch plus environment/source corrections.",
            "normal_form": "L_mem = -nabla_i(Z_mem nabla^i delta_m)+M2_mem delta_m",
            "identification": "lambda_mem=sqrt(Z_mem/M2_mem) when both coefficients are positive and in the same normalization.",
            "status": "EXACT_CONDITIONAL_DEFINITION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "hessian_id": "HES4628_2_canonical_normalization_guard",
            "statement": "Only the ratio M2_mem/Z_mem fixes lambda_mem; rescaling m_mem changes Z_mem and M2_mem separately but not their same-branch ratio.",
            "normal_form": "m_canonical=sqrt(Z_mem) delta_m, m_gap^2=M2_mem/Z_mem",
            "identification": "lambda_mem=1/m_gap in c=hbar=1 units, or hbar/(m_gap c) in SI particle units.",
            "status": "NORMALIZATION_GUARD_READY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def gap_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gap_id": "GAP4628_0_exact_positive_gap",
            "condition": "Z_mem_min>0 and M2_mem_min>0 on the selected branch",
            "formula": "lambda_mem <= sqrt(Z_mem_max/M2_mem_min) with a stated domain/norm; constant coefficient case lambda_mem=sqrt(Z_mem/M2_mem)",
            "consequence": "finite Yukawa range and 4621 coercive nohair/bound theorem applies",
            "status": "PARENT_HESSIAN_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gap_id": "GAP4628_1_massless_fail",
            "condition": "M2_mem=0 or zero-mode not removed",
            "formula": "lambda_mem -> infinity",
            "consequence": "local GR likely fails unless Q_eff=0 exactly; long-range WEP/orbital/PPN bounds become mandatory",
            "status": "FAIL_BRANCH_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gap_id": "GAP4628_2_tachyon_fail",
            "condition": "M2_mem<0 on the local branch",
            "formula": "lambda_mem imaginary / instability scale",
            "consequence": "local branch is unstable, not a GR recovery branch",
            "status": "FAIL_BRANCH_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gap_id": "GAP4628_3_constraint_limit",
            "condition": "M2_mem/Z_mem -> infinity or m_mem is nondynamical after parent constraint elimination",
            "formula": "lambda_mem -> 0",
            "consequence": "memory-mediated local force is contact/absent, but parent constraint proof is required",
            "status": "EXACT_CONDITIONAL_CONSTRAINT_ROUTE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def anchor_rows(now: str) -> list[dict[str, Any]]:
    lambda_anchor_m = 38.6e-6
    inverse_lambda_sq_m2 = 1.0 / (lambda_anchor_m * lambda_anchor_m)
    hbar_c_ev_m = 1.973269804e-7
    canonical_gap_ev = hbar_c_ev_m / lambda_anchor_m
    return [
        {
            "checkpoint": CHECKPOINT,
            "anchor_id": "A4628_0_R10_alpha1_lambda",
            "source_anchor": "BA4626_0_R10_EOTWASH_ALPHA1",
            "lambda_anchor_m": lambda_anchor_m,
            "alpha_anchor": 1.0,
            "derived_ratio_requirement_m_minus_2": inverse_lambda_sq_m2,
            "canonical_gap_energy_eV_if_Z_is_canonical": canonical_gap_ev,
            "meaning": "For an alpha=1 Yukawa smoke, lambda_mem shorter than this anchor is the first conservative R10 threshold; this is not a full curve pass.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "anchor_id": "A4628_1_gap_ratio_template",
            "source_anchor": "A4628_0_R10_alpha1_lambda",
            "lambda_anchor_m": lambda_anchor_m,
            "alpha_anchor": 1.0,
            "derived_ratio_requirement_m_minus_2": inverse_lambda_sq_m2,
            "canonical_gap_energy_eV_if_Z_is_canonical": canonical_gap_ev,
            "meaning": "If M2_mem/Z_mem >= 1/lambda_anchor^2 and alpha_Y<=1, the anchor-smoke condition can be evaluated; full alpha(lambda) curve still required for claim.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def numeric_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LNUM4628_0_Zmem",
            "symbol": "Z_mem",
            "definition": "same-branch kinetic Hessian of memory field",
            "value": "MISSING_PARENT_HESSIAN_VALUE",
            "units": "depends on memory normalization",
            "feeds": "lambda_mem and coercive nohair bound",
            "required_source": "parent quadratic action expansion",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LNUM4628_1_M2mem",
            "symbol": "M2_mem",
            "definition": "same-branch positive mass/gap Hessian",
            "value": "MISSING_PARENT_HESSIAN_VALUE_OR_GAP_THEOREM",
            "units": "Z_mem / length^2 in local units",
            "feeds": "lambda_mem",
            "required_source": "parent effective potential/Hessian or constraint proof",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LNUM4628_2_lambda",
            "symbol": "lambda_mem",
            "definition": "sqrt(Z_mem/M2_mem)",
            "value": "MISSING_ZMEM_M2MEM_RATIO",
            "units": "length",
            "feeds": "R10/WEP/orbital/PPN bound selection",
            "required_source": "Z_mem and M2_mem same-branch ratio",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LNUM4628_3_R10_anchor_gap_ratio",
            "symbol": "(M2_mem/Z_mem)_anchor",
            "definition": "1/(38.6e-6 m)^2 for alpha=1 anchor smoke",
            "value": f"{1.0 / (38.6e-6 * 38.6e-6):.12g}",
            "units": "m^-2",
            "feeds": "anchor smoke only",
            "required_source": "Eot-Wash alpha=1 threshold anchor plus canonical same-branch ratio",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LNUM4628_4_canonical_gap_energy",
            "symbol": "m_gap_anchor",
            "definition": "hbar c / 38.6e-6 m if memory is canonically normalized",
            "value": f"{1.973269804e-7 / 38.6e-6:.12g}",
            "units": "eV",
            "feeds": "intuition only; not claim unless canonical normalization is parent-owned",
            "required_source": "canonical normalization theorem and R10 anchor",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTL4628_0_ratio_not_separate_values", "rule": "Only same-branch M2_mem/Z_mem fixes lambda_mem; separate fitted Z and M2 values are not meaningful without normalization.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4628_1_no_anchor_curve_overclaim", "rule": "The 38.6 um alpha=1 threshold is an anchor-smoke gate, not a full alpha(lambda) bound curve.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4628_2_massless_branch_warn", "rule": "If M2_mem=0, local GR requires exact Q_eff=0; do not call the massless branch screened.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4628_3_tachyon_reject", "rule": "Negative M2_mem is an instability branch and cannot be used for local GR recovery.", "violation_blocks_claim": True, "timestamp_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4628_0_parent_hessian", "blocks": "lambda_mem numeric value", "missing": "parent quadratic action/Hessian giving Z_mem and M2_mem", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4628_1_normalization", "blocks": "canonical gap energy use", "missing": "canonical memory normalization or invariant ratio proof", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4628_2_Qeff_pairing", "blocks": "anchor smoke pass", "missing": "lambda_mem paired with Q_eff, alpha_A and source mass on same branch", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4628_0_exact_constraint", "promotion_condition": "Parent proves memory is nondynamical/constraint-eliminated or M2/Z infinite on local branch.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4628_1_gap_anchor_smoke", "promotion_condition": "Parent-owned M2/Z gives lambda_mem <= 38.6e-6 m and 4627 gives alpha_Y<=1 at anchor.", "current_result": "blocked_missing_M2_Z_Qeff", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4628_2_full_curve", "promotion_condition": "lambda_mem and alpha_Y are compared against a full source-backed alpha(lambda) curve and WEP/orbital maps.", "current_result": "blocked_full_curve_missing", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4628_0",
            "decision": DECISION,
            "meaning": "lambda_mem is now reduced to a parent Hessian ratio M2_mem/Z_mem. R10 anchor conversion is staged for smoke only; no local-GR claim until the same-branch Hessian ratio and Qeff/sensitivities exist.",
            "status": "NONCLAIM_PRIVATE_DERIVATION_AND_ANCHOR_TEMPLATE_STAGE",
            "best_route": "derive parent quadratic memory action/Hessian; if impossible, keep lambda_mem as a first numeric nonclaim row",
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
            "summary": "lambda_mem gap reduced to parent Hessian ratio; R10 anchor gap conversion and fail branches are explicit.",
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
            "reason": "The Hessian ratio is now defined, but anchor smoke needs canonical normalization and paired Qeff/alpha inputs.",
            "derive_first": "canonical normalization/invariant ratio theorem for M2_mem/Z_mem",
            "fallback": "first anchor smoke runner that fails closed unless lambda_mem, Qeff, Zmem and alpha_A exist",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join([
        "# 4628 - lambda_mem Gap Row Or Zmem/M2mem Parent Hessian",
        "",
        f"Timestamp UTC: `{now}`",
        f"Branch: `{BRANCH_ID}`",
        f"Marker: `{MARKER}`",
        f"Decision: `{DECISION}`",
        "",
        "## Result",
        "",
        "4628 turns the range problem into a parent-Hessian problem. `lambda_mem` is not chosen from the bound; it is fixed by the same-branch quadratic memory operator.",
        "",
        "`S_mem^(2)=1/2 int mu_obs [Z_mem h^ij partial_i delta_m partial_j delta_m + M2_mem delta_m^2]`",
        "",
        "`lambda_mem = sqrt(Z_mem/M2_mem)` when `Z_mem>0` and `M2_mem>0` in the same normalization.",
        "",
        "The R10 anchor conversion is staged only for smoke discipline:",
        "",
        "`lambda_anchor = 38.6e-6 m`, so `(M2_mem/Z_mem)_anchor = 1/lambda_anchor^2`.",
        "",
        "If `M2_mem=0`, the force is long-range unless `Q_eff=0` exactly. If `M2_mem<0`, the branch is unstable and cannot be a local-GR recovery branch.",
        "",
        "## Sources",
        markdown_table(tables["sources"]),
        "",
        "## Parent Hessian Rows",
        markdown_table(tables["hessian"]),
        "",
        "## lambda_mem Gap Rows",
        markdown_table(tables["gap"]),
        "",
        "## R10 Anchor Gap Conversion Rows",
        markdown_table(tables["anchor"]),
        "",
        "## Zmem/M2mem First Numeric Template",
        markdown_table(tables["numeric"]),
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
        "All rows remain `valid_for_claim=false`. The gap/range is derived as a parent Hessian ratio or remains a fail-closed numeric template.",
    ]).strip() + "\n"


def build_formal(now: str) -> str:
    return f"""# 644 - PPC4161 lambda_mem Gap Row Or Zmem/M2mem Parent Hessian

Timestamp UTC: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Branch: `{BRANCH_ID}`

## Gap Gate

The parent quadratic memory action must supply:

`S_mem^(2)=1/2 int mu_obs [Z_mem h^ij partial_i delta_m partial_j delta_m + M2_mem delta_m^2]`.

The invariant local range is:

`lambda_mem = sqrt(Z_mem/M2_mem)`.

For the R10 alpha=1 anchor:

`lambda_anchor = 38.6e-6 m`,

so

`(M2_mem/Z_mem)_anchor = 1/lambda_anchor^2 = {1.0 / (38.6e-6 * 38.6e-6):.12g} m^-2`.

If canonical normalization is parent-owned, this corresponds to a gap energy of approximately `{1.973269804e-7 / 38.6e-6:.12g} eV`.

This is anchor-smoke only, not a full bound-curve pass.

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4628 reduces lambda_mem to the parent Hessian ratio M2_mem/Z_mem and stages the R10 anchor gap conversion as nonclaim smoke input.",
        "current_evidence": "Generated source register, parent Hessian rows, gap rows, R10 anchor conversion, numeric templates, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "lambda_mem_parent_hessian_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Choosing lambda_mem from empirical bounds instead of deriving the parent Hessian ratio.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/Newton/WEP/PPN pass until M2_mem/Z_mem, Qeff and sensitivities are same-branch source-backed or exact-zero.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4628_00_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in tables["sources"]), "all cited paths/needles found")
    csv_paths = [SOURCE_REGISTER, HESSIAN_CSV, GAP_CSV, ANCHOR_CSV, NUMERIC_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    parsed = {path.name: len(read_csv(path)) for path in csv_paths if path.exists()}
    add("VAL4628_01_csv_parse", len(parsed) == len(csv_paths) and all(count > 0 for count in parsed.values()), ";".join(f"{name}:{count}" for name, count in parsed.items()))
    add("VAL4628_02_hessian_normal_form", any(row["hessian_id"] == "HES4628_0_quadratic_memory_action" for row in tables["hessian"]), "quadratic memory action row present")
    add("VAL4628_03_gap_fail_branches", any(row["gap_id"] == "GAP4628_1_massless_fail" for row in tables["gap"]) and any(row["gap_id"] == "GAP4628_2_tachyon_fail" for row in tables["gap"]), "massless/tachyon fail branches present")
    anchor = [row for row in tables["anchor"] if row["anchor_id"] == "A4628_0_R10_alpha1_lambda"]
    add("VAL4628_04_anchor_conversion_positive", bool(anchor) and float(anchor[0]["lambda_anchor_m"]) > 0 and float(anchor[0]["derived_ratio_requirement_m_minus_2"]) > 0, "positive R10 anchor conversion")
    add("VAL4628_05_numeric_template", len(tables["numeric"]) >= 5 and any(row["symbol"] == "lambda_mem" for row in tables["numeric"]), "lambda numeric template present")
    add("VAL4628_06_all_rows_nonclaim", not any(any_claim_true(rows) for rows in tables.values()), "no generated row promotes a claim")
    add("VAL4628_07_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4628_08_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4628_09_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4628_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4628_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4628_12_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4628_13_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4628_14_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4628_OVERALL", all(row["status"] == "PASS" for row in rows), "4628 lambda_mem parent hessian checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "hessian": hessian_rows(now),
        "gap": gap_rows(now),
        "anchor": anchor_rows(now),
        "numeric": numeric_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(HESSIAN_CSV, tables["hessian"])
    write_csv(GAP_CSV, tables["gap"])
    write_csv(ANCHOR_CSV, tables["anchor"])
    write_csv(NUMERIC_CSV, tables["numeric"])
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
## PPC4161 Local Addendum - lambda_mem Gap Row Or Zmem/M2mem Parent Hessian

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4628 reduces `lambda_mem` to the same-branch parent Hessian ratio: `lambda_mem=sqrt(Z_mem/M2_mem)`. The R10 alpha=1 anchor `lambda=38.6e-6 m` implies `(M2_mem/Z_mem)_anchor={1.0 / (38.6e-6 * 38.6e-6):.12g} m^-2` for smoke only. Massless and tachyonic branches are retained as fail branches unless `Q_eff=0` or parent constraint elimination is signed.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - lambda_mem Gap Row Or Zmem/M2mem Parent Hessian

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now requires a parent Hessian ratio before any Yukawa/local-G anchor smoke can pass. Next target: `{NEXT_TARGET}`.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4628 validation failed: {failed}")
    print(f"4628 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
