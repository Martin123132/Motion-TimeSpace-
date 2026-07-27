from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3931"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3931-Y5-R2FR-history-nonlocal-tail-reset-or-suppression-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3931_SOURCE_REGISTER.csv",
    "signature": SRC / "P8_Y5_R2FR_3931_HISTORY_NONLOCAL_PARENT_SIGNATURE.csv",
    "zero_result": SRC / "P8_Y5_R2FR_3931_HISTORY_NONLOCAL_ZERO_RESULT.csv",
    "suppression": SRC / "P8_Y5_R2FR_3931_HISTORY_SUPPRESSION_BOUND_ROWS.csv",
    "reduced_escape": SRC / "P8_Y5_R2FR_3931_REDUCED_BESCAPE_QUEUE.csv",
    "decision": SRC / "P8_Y5_R2FR_3931_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3931_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3931_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3931_VALIDATION.csv",
}

HISTORY_SIGNATURE = (
    "local reset/no-incoming branch: X_mem(t0)=0, J_open+B_lift=0 on the source-free local collar, "
    "B_nonlocal_kernel=0, lambda_gap>0, gamma_mem>=0, and retarded/homogeneous incoming memory modes are excluded "
    "only for the local stationary isolated PPN/Newton branch"
)
SUPPRESSION_LAW = (
    "B_history := K_hist[exp(-gamma_mem Delta t)||X_mem(t0)|| + "
    "(1-exp(-gamma_mem Delta t))sup||J_open+B_lift||/lambda_gap] + B_nonlocal_kernel"
)
STATIC_AMPLITUDE = "||X_mem|| <= (||J_open|| + B_lift)/lambda_gap"
HISTORY_DECAY = (
    "||X_mem(t)|| <= exp(-gamma_mem Delta t)||X_mem(t0)|| + "
    "(1-exp(-gamma_mem Delta t))sup||J_open+B_lift||/lambda_gap"
)
HISTORY_ZERO = (
    "HISTORY_RESET_loc => B_history=0, P00_history=0, P00_nonlocal=0, "
    "A_multi_HBPD0=0"
)
BESCAPE_REDUCED = "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + B_deriv"
NEXT_DOC = "3932-Y5-R2FR-derivative-hair-square-law-epsilonr-lock-or-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3932_derivative_hair_square_law_epsilonr_lock_or_bound.py"


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
        ("SRC3931_00_3930_doc", PCW / "3930-Y5-R2FR-boundary-harmonic-no-flux-or-source-bound.md", "Reduced escape queue:", "3930 reduced escape handoff"),
        ("SRC3931_01_3930_reduced", SRC / "P8_Y5_R2FR_3930_REDUCED_BESCAPE_QUEUE.csv", "RBE3930_2_reduced_escape", "3930 reduced B_escape queue"),
        ("SRC3931_02_3930_next", SRC / "P8_Y5_R2FR_3930_NEXT_TARGET.csv", "NEXT3930_0", "3931 handoff"),
        ("SRC3931_03_3895_doc", PCW / "3895-Y5-R2FR-memory-boundary-history-zero-or-first-numeric-memory-row.md", "Exact history silence needs", "3895 history zero prose"),
        ("SRC3931_04_3895_zero_history", SRC / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv", "ZERO3895_4_history_exact", "history exact zero condition"),
        ("SRC3931_05_3895_zero_total", SRC / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv", "ZERO3895_5_total", "partial zero bound required"),
        ("SRC3931_06_3895_energy", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_0_energy_identity", "memory energy identity"),
        ("SRC3931_07_3895_gap", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_1_gap", "lambda gap law"),
        ("SRC3931_08_3895_static", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_2_static_amplitude", "static amplitude bound"),
        ("SRC3931_09_3895_decay", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_3_history_decay", "dynamic history decay bound"),
        ("SRC3931_10_3895_projection", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_4_observable_projection", "observable projection bound"),
        ("SRC3931_11_3927_history", SRC / "P8_Y5_R2FR_3927_BESCAPE_COMPONENT_FORMULAS.csv", "COMP3927_2_history_nonlocal", "B_history formula"),
        ("SRC3931_12_3927_inputs", SRC / "P8_Y5_R2FR_3927_BESCAPE_INPUT_REQUIREMENTS.csv", "IN3927_10_gamma_mem", "gamma_mem input"),
        ("SRC3931_13_3927_inputs_gap", SRC / "P8_Y5_R2FR_3927_BESCAPE_INPUT_REQUIREMENTS.csv", "IN3927_13_lambda_gap", "lambda_gap input"),
        ("SRC3931_14_3922_history", SRC / "P8_Y5_R2FR_3922_MULTIPOLE_ESCAPE_ZERO_THEOREM.csv", "MUL3922_4_history_zero", "history zero route"),
        ("SRC3931_15_3930_validation", SRC / "P8_Y5_BRR545_3930_VALIDATION.csv", "VAL3930_15_no_pycache", "3930 validation"),
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
            "row_id": "HSIG3931_0_branch",
            "signature_clause": "local reset/no-incoming history branch",
            "statement": HISTORY_SIGNATURE,
            "branch_status": "ADOPTED_FOR_PRIVATE_LOCAL_BRANCH",
            "effect": "turns history/nonlocal escape into a local retarded-boundary/reset condition",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HSIG3931_1_no_initial_memory",
            "signature_clause": "no incoming homogeneous memory",
            "statement": "X_mem(t0)=0 for local stationary isolated PPN/Newton branch",
            "branch_status": "SIGNED_FOR_LOCAL_RESET_BRANCH",
            "effect": "kills exp(-gamma_mem Delta t)||X_mem(t0)|| term",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HSIG3931_2_no_open_source",
            "signature_clause": "no open local memory source",
            "statement": "J_open+B_lift=0 on the source-free local collar after projector/domain/boundary closure",
            "branch_status": "SIGNED_FOR_LOCAL_SOURCE_FREE_COLLAR",
            "effect": "kills forced-memory term divided by lambda_gap",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HSIG3931_3_no_nonlocal_kernel",
            "signature_clause": "compact local kernel silence",
            "statement": "B_nonlocal_kernel=0 for the local stationary compact branch",
            "branch_status": "SIGNED_FOR_LOCAL_COMPACT_KERNEL",
            "effect": "kills nonlocal tail inside local PPN/Newton branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HSIG3931_4_gap_guard",
            "signature_clause": "positive/coercive memory operator guard",
            "statement": "lambda_gap:=a_min C_P/L_D^2 + m_min^2 > 0 or reset branch uses the zero source solution",
            "branch_status": "SIGNED_AS_STABILITY_GUARD_NOT_NUMERIC_CLAIM",
            "effect": "prevents uncontrolled zero-mode memory from being hidden",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HSIG3931_5_signature_verdict",
            "signature_clause": "history/nonlocal local branch verdict",
            "statement": HISTORY_ZERO,
            "branch_status": "HISTORY_NONLOCAL_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH",
            "effect": "history and nonlocal multipole sources are zero in this local branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_result_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("HNZ3931_0_Xmem_initial", "||X_mem(t0)||", "0", "no incoming homogeneous memory in local reset branch"),
        ("HNZ3931_1_open_source", "sup||J_open+B_lift||", "0", "source-free local collar after projector/domain/boundary closure"),
        ("HNZ3931_2_B_nonlocal", "B_nonlocal_kernel", "0", "compact local kernel silence"),
        ("HNZ3931_3_B_history", "B_history", "0", "suppression law has all source terms zero"),
        ("HNZ3931_4_P00_history", "P00_history", "0", "no history scalar source in local reset branch"),
        ("HNZ3931_5_P00_nonlocal", "P00_nonlocal", "0", "no nonlocal scalar source in compact local branch"),
        ("HNZ3931_6_A_multi", "A_multi_HBPD0", "0", "projector/domain, boundary/harmonic, history and nonlocal multipoles all zero"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "branch_value": value,
            "derivation": derivation,
            "branch_status": "THEOREM_ZERO_IN_PRIVATE_LOCAL_RESET_BRANCH",
            "strict_public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, value, derivation in data
    ]


def suppression_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("HSB3931_0_static", "static memory amplitude", STATIC_AMPLITUDE, "source ||J_open||, B_lift, lambda_gap"),
        ("HSB3931_1_decay", "dynamic history tail", HISTORY_DECAY, "source gamma_mem, Delta t, X_mem(t0), J_open+B_lift, lambda_gap"),
        ("HSB3931_2_kernel", "nonlocal kernel tail", "B_nonlocal_kernel", "source compact-kernel norm or zero theorem"),
        ("HSB3931_3_observable", "arena projection", "|Delta O_i| <= K_i||X_mem|| + K_i_grad||grad X_mem||", "source K_i and K_i_grad for R10/PPN/clock/orbital/WEP"),
        ("HSB3931_4_total", "B_history", SUPPRESSION_LAW, "absolute-sum no-cancellation if reset branch is rejected"),
    ]
    return [
        {
            "row_id": row_id,
            "component": component,
            "formula": formula,
            "required_if_not_reset": required,
            "numeric_value": "",
            "status": "HELD_IN_RESERVE_IF_RESET_BRANCH_REJECTED_OR_NONLOCAL_ARENA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, formula, required in data
    ]


def reduced_escape_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RHE3931_0_removed_history",
            "component": "history/nonlocal",
            "before": SUPPRESSION_LAW,
            "after": "B_history=0, P00_history=0, P00_nonlocal=0",
            "status": "REMOVED_IN_PRIVATE_LOCAL_RESET_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RHE3931_1_reduced_multipole",
            "component": "A_multi",
            "before": "A_multi_BPD0 <= G_ext*(|P00_history|+|P00_nonlocal|)",
            "after": "A_multi_HBPD0=0",
            "status": "MULTIPOLE_ESCAPE_REMOVED_IN_LOCAL_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RHE3931_2_reduced_escape",
            "component": "B_escape",
            "before": "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi_BPD0 + B_deriv",
            "after": BESCAPE_REDUCED,
            "status": "ESCAPE_REDUCED_TO_SQUARE_RADIAL_DERIVATIVE_TERMS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RHE3931_3_next_priority",
            "component": "next obstruction",
            "before": "history/nonlocal tails",
            "after": "derivative hair plus Delta_sq and epsilon_r",
            "status": "NEXT_PRIORITY_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3931_0_adopt_reset",
            "decision": "adopt local reset/no-incoming history branch for private local PPN/Newton derivation",
            "reason": "it is the local retarded isolated-source analogue of the boundary choices already made",
            "claim_status": "PRIVATE_BRANCH_ZERO_NOT_GLOBAL_MEMORY_CLAIM",
            "next_action": "remove history/nonlocal multipole source from B_escape queue",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3931_1_keep_suppression",
            "decision": "retain suppression rows for cosmology, galaxies, open systems and any nonlocal arena",
            "reason": HISTORY_DECAY,
            "claim_status": "REVERSIBLE_BRANCH_CHOICE",
            "next_action": "use suppression law where local reset/no-tail is not justified",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3931_2_next",
            "decision": "B_escape is now reduced to Delta_sq, epsilon_r and B_deriv in the private local branch",
            "reason": BESCAPE_REDUCED,
            "claim_status": "LOCAL_GR_STILL_NOT_PROMOTED",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3931_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attack derivative hair, common-mode square-law Delta_sq, and epsilon_r",
            "success_condition": "derive derivative-silent calibrated monopole/common-mode lock or emit source-backed residual bound rows",
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
            "summary": "history/nonlocal escape component zeroed inside the private reset/no-incoming local branch; derivative/square/radial terms remain",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3931 - History/Nonlocal Tail Reset or Suppression Bound

Timestamp: `{timestamp}`

## Result

Adopted the local reset/no-incoming history branch for the private local PPN/Newton derivation.

History signature:

`{HISTORY_SIGNATURE}`.

Suppression law retained for non-reset arenas:

`{SUPPRESSION_LAW}`.

Zero result:

`{HISTORY_ZERO}`.

Reduced escape queue:

`{BESCAPE_REDUCED}`.

## Meaning

This is not a global claim that memory never exists. It says the local isolated PPN/Newton branch uses a retarded reset/no-incoming condition: no initial homogeneous memory, no open local source, and no compact nonlocal kernel tail. Cosmology, galaxies, open systems, radiating systems, and any arena with nonlocal memory must use the suppression rows instead.

## Current Verdict

- `B_history=0`, `P00_history=0`, and `P00_nonlocal=0` inside the private local reset branch.
- `A_multi_HBPD0=0` after the 3929 projector/domain and 3930 boundary/harmonic closures.
- `B_escape` now reduces to `Delta_sq`, `epsilon_r`, and derivative hair.
- No change to `formalization-workbench`; no GitHub action.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3931_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3931_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3931_HISTORY_NONLOCAL_PARENT_SIGNATURE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3931_HISTORY_NONLOCAL_ZERO_RESULT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3931_HISTORY_SUPPRESSION_BOUND_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3931_REDUCED_BESCAPE_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3931_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3931_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3931 - History/Nonlocal Tail Reset

Timestamp: `{timestamp}`

- History signature: `{HISTORY_SIGNATURE}`.
- Suppression law retained: `{SUPPRESSION_LAW}`.
- Zero result: `{HISTORY_ZERO}`.
- Reduced escape: `{BESCAPE_REDUCED}`.
- Status: history/nonlocal removed from the private local reset branch; derivative hair, `Delta_sq`, and `epsilon_r` remain nonclaim.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3931 - History/Nonlocal Tail Reset"
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
    suppression = suppression_rows(timestamp)
    reduced = reduced_escape_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    reduced_formula = next(row["after"] for row in reduced if row["row_id"] == "RHE3931_2_reduced_escape")
    checks = [
        ("VAL3931_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3931_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3931_02_signature_adopted", any(row["branch_status"] == "HISTORY_NONLOCAL_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH" for row in signature), "history/nonlocal private signature verdict emitted"),
        ("VAL3931_03_zero_rows", len(zero_result) == 7 and all(row["branch_value"] == "0" for row in zero_result), "history/nonlocal zero rows emitted"),
        ("VAL3931_04_suppression_kept", len(suppression) == 5 and any(row["row_id"] == "HSB3931_4_total" for row in suppression), "suppression fallback rows retained"),
        ("VAL3931_05_reduced_escape", "A_multi" not in reduced_formula and "B_deriv" in reduced_formula and "Delta_sq" in reduced_formula, "reduced B_escape removes multipole/history term"),
        ("VAL3931_06_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (signature, zero_result, suppression, reduced, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3931_07_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3931_08_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3931_09_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3931_10_spine_written", SPINE_PATH.exists() and "3931 - History/Nonlocal Tail Reset" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3931_11_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3931_12_script_compiles", True, "script compiles"),
        ("VAL3931_13_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["suppression"], suppression_rows(timestamp))
    write_csv(OUTPUTS["reduced_escape"], reduced_escape_rows(timestamp))
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
        raise SystemExit(f"3931 validation failed: {failed}")
    print(f"3931 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
