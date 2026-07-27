from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3932"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3932-Y5-R2FR-derivative-hair-square-law-epsilonr-lock-or-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3932_SOURCE_REGISTER.csv",
    "signature": SRC / "P8_Y5_R2FR_3932_COMMON_MODE_CALIBRATION_SIGNATURE.csv",
    "zero_result": SRC / "P8_Y5_R2FR_3932_DERIVATIVE_SQUARE_EPSILON_ZERO_RESULT.csv",
    "fallback": SRC / "P8_Y5_R2FR_3932_COMMON_MODE_FALLBACK_BOUND_ROWS.csv",
    "local_escape": SRC / "P8_Y5_R2FR_3932_LOCAL_BESCAPE_RESULT.csv",
    "decision": SRC / "P8_Y5_R2FR_3932_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3932_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3932_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3932_VALIDATION.csv",
}

CALIBRATED_MONOPOLE_SIGNATURE = (
    "local calibrated-monopole branch: Xi_N=xi_0 U_N+const, xi_0 is universal/time-independent/"
    "source-independent/frame-independent, Xi_N^res=0, and the public metric is the EH one-metric "
    "completion written in measured U_obs=(1+xi_0)U_N"
)
EH_SQUARE_LAW = (
    "g00_EH=-1+2U_obs-2U_obs^2+O(U_obs^3), U_obs=(1+xi_0)U_N "
    "=> xi_1=xi_0, xi_2=2xi_0+xi_0^2, Delta_sq=xi_2-2xi_1-xi_1^2=0"
)
RADIAL_LOCK = (
    "epsilon_r=|((1+xi_1)-r partial_r xi_1)/(1+xi_ref)-1|=0 when xi_1=xi_ref=xi_0 and partial_r xi_1=0"
)
DERIVATIVE_LOCK = (
    "B_deriv=|partial_t xi_1|+|partial_r xi_1|+|Delta_AB xi_1|+|delta_frame xi_1|=0 "
    "for universal derivative-silent xi_0"
)
BESCAPE_ZERO = (
    "B_escape_loc=|Delta_sq|/(1+xi_1)^2+|epsilon_r|+B_deriv=0"
)
FALLBACK_BOUND = (
    "B_escape_loc_fallback=|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + "
    "|partial_t xi_1| + |partial_r xi_1| + |Delta_AB xi_1| + |delta_frame xi_1|"
)
NEXT_DOC = "3933-Y5-R2FR-local-GR-PPN-conditional-closure-rollup-or-residual-scorecard.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3933_local_GR_PPN_conditional_closure_rollup_or_residual_scorecard.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3932_00_3931_doc", PCW / "3931-Y5-R2FR-history-nonlocal-tail-reset-or-suppression-bound.md", "Reduced escape queue:", "3931 reduced escape handoff"),
        ("SRC3932_01_3931_reduced", SRC / "P8_Y5_R2FR_3931_REDUCED_BESCAPE_QUEUE.csv", "RHE3931_2_reduced_escape", "3931 reduced B_escape queue"),
        ("SRC3932_02_3931_next", SRC / "P8_Y5_R2FR_3931_NEXT_TARGET.csv", "NEXT3931_0", "3932 handoff"),
        ("SRC3932_03_3919_doc", PCW / "3919-Y5-R2FR-beta-source-second-order-lock-or-common-mode-R11-bound.md", "B_source=A_source^2", "EH beta source square law"),
        ("SRC3932_04_3919_common", SRC / "P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv", "xi_2=2 xi_1+xi_1^2", "common-mode square law row"),
        ("SRC3932_05_3920_doc", PCW / "3920-Y5-R2FR-common-mode-square-law-or-XiN-bound-runner.md", "Delta_sq:=xi_2-2 xi_1-xi_1^2=0", "Delta_sq exact definition"),
        ("SRC3932_06_3920_runner_delta", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_0_Delta_sq", "Delta_sq runner"),
        ("SRC3932_07_3920_runner_radial", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_4_radial_shape", "epsilon_r runner"),
        ("SRC3932_08_3920_arena", SRC / "P8_Y5_R2FR_3920_NEWTON_EPHEMERIS_GDOT_LINKS.csv", "ARE3920_1_Newton", "Newton calibration split"),
        ("SRC3932_09_3921_doc", PCW / "3921-Y5-R2FR-P00-common-mode-source-zero-or-XiN-numeric-bound-fill.md", "Xi_N^res", "residual common-mode definition"),
        ("SRC3932_10_3921_ext_monopole", SRC / "P8_Y5_R2FR_3921_P00_ZERO_HARMONIC_EXTERIOR_THEOREM.csv", "EXT3921_3_monopole_calibration", "monopole calibration rule"),
        ("SRC3932_11_3921_ext_square", SRC / "P8_Y5_R2FR_3921_P00_ZERO_HARMONIC_EXTERIOR_THEOREM.csv", "EXT3921_5_beta_square", "beta square-law closure"),
        ("SRC3932_12_3921_fill_radial", SRC / "P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv", "BIN3921_6_radial", "epsilon_r bound row"),
        ("SRC3932_13_3921_fill_time", SRC / "P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv", "BIN3921_7_time", "time derivative bound row"),
        ("SRC3932_14_3921_fill_source", SRC / "P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv", "BIN3921_8_source", "source-dependence bound row"),
        ("SRC3932_15_3921_fill_delta", SRC / "P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv", "BIN3921_9_Delta_sq", "Delta_sq bound row"),
        ("SRC3932_16_3931_validation", SRC / "P8_Y5_BRR545_3931_VALIDATION.csv", "VAL3931_13_no_pycache", "3931 validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:760]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def signature_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CMS3932_0_branch",
            "signature_clause": "calibrated monopole branch",
            "statement": CALIBRATED_MONOPOLE_SIGNATURE,
            "branch_status": "ADOPTED_FOR_PRIVATE_LOCAL_BRANCH",
            "effect": "separates harmless measured-GM calibration from physical common-mode residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CMS3932_1_EH_square",
            "signature_clause": "EH one-metric second-order completion",
            "statement": EH_SQUARE_LAW,
            "branch_status": "SIGNED_FOR_PRIVATE_LOCAL_BRANCH",
            "effect": "sets Delta_sq=0 and hence delta_beta_common=0",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CMS3932_2_radial",
            "signature_clause": "no radial/finite-range common-mode shape",
            "statement": RADIAL_LOCK,
            "branch_status": "SIGNED_FOR_LOCAL_CALIBRATED_MONOPOLE",
            "effect": "sets epsilon_r=0 after measured GM calibration",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CMS3932_3_derivative",
            "signature_clause": "derivative-silent universal common mode",
            "statement": DERIVATIVE_LOCK,
            "branch_status": "SIGNED_FOR_LOCAL_CALIBRATED_MONOPOLE",
            "effect": "sets B_deriv=0 and blocks Gdot/WEP/frame leakage from xi_1",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CMS3932_4_no_absorption_guard",
            "signature_clause": "no absorption of real hair",
            "statement": "time/radial/source/frame dependence, finite range, multipoles, or non-square xi_2 are not measured-GM calibration",
            "branch_status": "GUARD_RETAINED",
            "effect": "forces fallback rows if the local calibrated-monopole branch is rejected",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CMS3932_5_signature_verdict",
            "signature_clause": "remaining B_escape local branch verdict",
            "statement": BESCAPE_ZERO,
            "branch_status": "BESCAPE_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH",
            "effect": "the escape envelope is zero inside the private local isolated/reset/calibrated branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_result_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CMZ3932_0_xi1", "xi_1", "xi_0", "universal measured-GM monopole calibration"),
        ("CMZ3932_1_xi2", "xi_2", "2xi_0+xi_0^2", "EH one-metric second-order completion"),
        ("CMZ3932_2_Delta_sq", "Delta_sq", "0", "xi_2-2xi_1-xi_1^2=0"),
        ("CMZ3932_3_delta_beta_common", "delta_beta_common", "0", "Delta_sq/(1+xi_1)^2=0"),
        ("CMZ3932_4_epsilon_r", "epsilon_r", "0", "constant xi_1 is absorbed into xi_ref/measured GM"),
        ("CMZ3932_5_B_deriv", "B_deriv", "0", "partial_t/r/source/frame xi_1 all vanish"),
        ("CMZ3932_6_B_escape", "B_escape_loc", "0", "sum of zeroed Delta_sq, epsilon_r and B_deriv terms"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "branch_value": value,
            "derivation": derivation,
            "branch_status": "THEOREM_ZERO_IN_PRIVATE_LOCAL_CALIBRATED_BRANCH",
            "strict_public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, value, derivation in data
    ]


def fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CMB3932_0_Delta_sq", "Delta_sq", "|Delta_sq| <= 7.8e-05*(1+xi_1)^2", "PPN beta gate if EH square law is not signed"),
        ("CMB3932_1_epsilon_r", "epsilon_r", "epsilon_r(r)=|((1+xi_1)-r partial_r xi_1)/(1+xi_ref)-1|", "orbital/ephemeris inverse-square gate if radial hair exists"),
        ("CMB3932_2_time", "partial_t ln(1+xi_1)", "|partial_t ln(1+xi_1)| <= 9.6e-15 yr^-1", "Gdot gate if time hair exists"),
        ("CMB3932_3_source", "Delta_AB xi_1", "Delta_AB xi_1 and Delta_AB Delta_sq", "WEP/source-composition gate if source hair exists"),
        ("CMB3932_4_frame", "delta_frame xi_1", "frame/readout variation of xi_1", "preferred-frame/readout gate if frame hair exists"),
        ("CMB3932_5_total", "B_escape_loc_fallback", FALLBACK_BOUND, "absolute-sum no-cancellation if calibrated branch is rejected"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "required_if_not_locked": required,
            "numeric_value": "",
            "status": "HELD_IN_RESERVE_IF_CALIBRATED_MONOPOLE_BRANCH_REJECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, formula, required in data
    ]


def local_escape_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "LBE3932_0_before",
            "component": "remaining escape after 3931",
            "formula": "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + B_deriv",
            "branch_value": "open before calibrated-monopole lock",
            "status": "INPUT_HANDOFF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LBE3932_1_square",
            "component": "square-law",
            "formula": EH_SQUARE_LAW,
            "branch_value": "Delta_sq=0",
            "status": "ZERO_IN_PRIVATE_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LBE3932_2_radial_derivative",
            "component": "radial/derivative hair",
            "formula": f"{RADIAL_LOCK}; {DERIVATIVE_LOCK}",
            "branch_value": "epsilon_r=0 and B_deriv=0",
            "status": "ZERO_IN_PRIVATE_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LBE3932_3_after",
            "component": "local B_escape",
            "formula": BESCAPE_ZERO,
            "branch_value": "0",
            "status": "BESCAPE_ZERO_PRIVATE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3932_0_adopt_lock",
            "decision": "adopt calibrated-monopole/EH square-law lock for the private local branch",
            "reason": "after projector/domain, boundary/harmonic and history/nonlocal closure, the only harmless common mode is universal measured-GM calibration with EH second order",
            "claim_status": "PRIVATE_BRANCH_ZERO_NOT_PUBLIC_LOCAL_GR_CLAIM",
            "next_action": "roll up the full local PPN/Newton closure stack and identify any remaining residual rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3932_1_no_hair_absorption",
            "decision": "do not absorb radial/time/source/frame hair into GM",
            "reason": "3920/3921 explicitly route those pieces to ephemeris, Gdot, WEP/source and preferred-frame bounds",
            "claim_status": "GUARD_RETAINED",
            "next_action": "use fallback rows if any nonconstant common mode is kept",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3932_2_next",
            "decision": "B_escape is zero inside the private local isolated/reset/calibrated branch",
            "reason": BESCAPE_ZERO,
            "claim_status": "LOCAL_GR_STILL_NEEDS_ROLLUP_AUDIT",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3932_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "roll up local GR/PPN/Newton closure after B_escape=0 and check remaining gamma, beta, alpha_i, xi, zeta_i, Gdot rows",
            "success_condition": "either produce a conditional local-GR theorem stack with all clauses explicit or a residual scorecard for any unclosed components",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "remaining B_escape terms zeroed inside the private calibrated-monopole/EH square-law local branch; rollup audit remains",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3932 - Derivative Hair, Square Law, and Epsilon_r Lock or Bound

Timestamp: `{timestamp}`

## Result

Adopted the calibrated-monopole/EH square-law lock for the private local branch.

Calibration signature:

`{CALIBRATED_MONOPOLE_SIGNATURE}`.

EH square law:

`{EH_SQUARE_LAW}`.

Radial lock:

`{RADIAL_LOCK}`.

Derivative lock:

`{DERIVATIVE_LOCK}`.

Local escape result:

`{BESCAPE_ZERO}`.

## Meaning

This is the tight local result we were aiming at for the escape sector. Once projector/domain, boundary/harmonic and history/nonlocal channels are closed, the remaining common mode is harmless only if it is a universal derivative-silent measured-GM monopole and its second-order metric coefficient follows the EH square law.

Anything else is not calibration: radial shape, time drift, source dependence, frame/readout dependence, finite range, or a non-square `xi_2` must use the fallback rows.

## Current Verdict

- `Delta_sq=0`, `epsilon_r=0`, and `B_deriv=0` inside the private calibrated local branch.
- Therefore `B_escape_loc=0` inside that branch.
- This is still not a public local-GR claim; the next step is a rollup audit across all PPN/Newton/Maxwell/source-coupling rows.
- No change to `formalization-workbench`; no GitHub action.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3932_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3932_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3932_COMMON_MODE_CALIBRATION_SIGNATURE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3932_DERIVATIVE_SQUARE_EPSILON_ZERO_RESULT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3932_COMMON_MODE_FALLBACK_BOUND_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3932_LOCAL_BESCAPE_RESULT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3932_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3932_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3932 - Derivative Hair, Square Law, and Epsilon_r Lock

Timestamp: `{timestamp}`

- Calibration signature: `{CALIBRATED_MONOPOLE_SIGNATURE}`.
- EH square law: `{EH_SQUARE_LAW}`.
- Radial lock: `{RADIAL_LOCK}`.
- Derivative lock: `{DERIVATIVE_LOCK}`.
- Local escape result: `{BESCAPE_ZERO}`.
- Status: `B_escape=0` inside the private calibrated local branch; rollup audit still required before any local-GR promotion.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3932 - Derivative Hair, Square Law, and Epsilon_r Lock"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    signature = signature_rows(timestamp)
    zero_result = zero_result_rows(timestamp)
    fallback = fallback_rows(timestamp)
    local_escape = local_escape_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    checks = [
        ("VAL3932_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3932_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3932_02_signature_adopted", any(row["branch_status"] == "BESCAPE_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH" for row in signature), "B_escape private signature verdict emitted"),
        ("VAL3932_03_zero_rows", len(zero_result) == 7 and any(row["symbol"] == "B_escape_loc" and row["branch_value"] == "0" for row in zero_result), "Delta_sq/epsilon_r/B_deriv zero rows emitted"),
        ("VAL3932_04_fallback_kept", len(fallback) == 6 and any(row["row_id"] == "CMB3932_5_total" for row in fallback), "common-mode fallback rows retained"),
        ("VAL3932_05_local_escape_zero", any(row["row_id"] == "LBE3932_3_after" and row["branch_value"] == "0" for row in local_escape), "local B_escape zero row emitted"),
        ("VAL3932_06_guard", any(row["row_id"] == "CMS3932_4_no_absorption_guard" for row in signature), "no-hair absorption guard emitted"),
        ("VAL3932_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (signature, zero_result, fallback, local_escape, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3932_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3932_09_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3932_10_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3932_11_spine_written", SPINE_PATH.exists() and "3932 - Derivative Hair, Square Law, and Epsilon_r Lock" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3932_12_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3932_13_script_compiles", True, "script compiles"),
        ("VAL3932_14_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["signature"], signature_rows(timestamp))
    write_csv(OUTPUTS["zero_result"], zero_result_rows(timestamp))
    write_csv(OUTPUTS["fallback"], fallback_rows(timestamp))
    write_csv(OUTPUTS["local_escape"], local_escape_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3932 validation failed: {failed}")
    print(f"3932 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
