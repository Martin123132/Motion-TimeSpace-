from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3919"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3919-Y5-R2FR-beta-source-second-order-lock-or-common-mode-R11-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3919_SOURCE_REGISTER.csv",
    "beta_lock": SRC / "P8_Y5_R2FR_3919_BETA_SOURCE_LOCK_DERIVATION.csv",
    "common_mode": SRC / "P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv",
    "bound_inputs": SRC / "P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3919_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3919_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3919_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3919_VALIDATION.csv",
}

BETA_DEF = "delta_beta_source = B_source/A_source^2 - 1"
PPN_G00 = "g00=-1+2 A_source U_N - 2 B_source U_N^2 + O(U_N^3)"
BETA_LOCK = "B_source=A_source^2 => delta_beta_source=0"
EH_G00 = "g00_EH=-1+2 U_obs - 2 U_obs^2 + O(U_obs^3)"
COMMON_MODE = "A_eff=1+xi_1, B_eff=1+xi_2, delta_beta_common=(1+xi_2)/(1+xi_1)^2-1"
SQUARE_LAW = "xi_2=2 xi_1+xi_1^2 => delta_beta_common=0"
SMALL_BOUND = "|delta_beta_common| ~= |xi_2-2 xi_1| <= 7.8e-05"
NEXT_DOC = "3920-Y5-R2FR-common-mode-square-law-or-XiN-bound-runner.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3920_common_mode_square_law_or_XiN_bound_runner.py"


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
        ("SRC3919_00_next", SRC / "P8_Y5_R2FR_3918_NEXT_TARGET.csv", "NEXT3918_0", "3918 selected beta/source and common-mode target"),
        ("SRC3919_01_beta_def", SRC / "P8_Y5_R2FR_3917_DELTA_BETA_SOURCE_FILL_ROWS.csv", "BET3917_0_definition", "beta source definition"),
        ("SRC3919_02_beta_zero", SRC / "P8_Y5_R2FR_3917_DELTA_BETA_SOURCE_FILL_ROWS.csv", "BET3917_1_branch_zero", "A_source/B_source branch zero"),
        ("SRC3919_03_beta_split", SRC / "P8_Y5_R2FR_3917_DELTA_BETA_SOURCE_FILL_ROWS.csv", "BET3917_3_R11_split", "beta residual split"),
        ("SRC3919_04_A_source", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_01_A_source", "A_source skeleton"),
        ("SRC3919_05_B_source", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_02_B_source", "B_source skeleton"),
        ("SRC3919_06_delta_beta", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_03_delta_beta_source", "delta beta source skeleton"),
        ("SRC3919_07_GR", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_0_GR", "local GR equation"),
        ("SRC3919_08_Newton", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_1_Newton", "Newtonian source readout"),
        ("SRC3919_09_EM", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_2_Maxwell", "Maxwell stress included in Hilbert source"),
        ("SRC3919_10_stack", SRC / "P8_Y5_R2FR_3914_STATIONARY_SOURCE_COUPLING_STACK.csv", "STK3914_1_stack", "source-coupling chain"),
        ("SRC3919_11_ZPoisson", SRC / "P8_Y5_R2FR_3914_ZPOISSON_ZFRAME_CLOSURE_GATE.csv", "Z3914_0_ZPoisson", "Poisson normalization one"),
        ("SRC3919_12_ZFrame", SRC / "P8_Y5_R2FR_3914_ZPOISSON_ZFRAME_CLOSURE_GATE.csv", "Z3914_1_ZFrame", "same frame readout"),
        ("SRC3919_13_Hilbert", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_0_Hilbert", "same-frame Hilbert bridge"),
        ("SRC3919_14_Poisson", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_2_Poisson", "Poisson coefficient bridge"),
        ("SRC3919_15_GR_reduction", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_1_GR_equation", "GR equation reduction"),
        ("SRC3919_16_Newton_limit", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_3_Newton", "Newton limit"),
        ("SRC3919_17_G_status", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_4_G_constant", "G owner status"),
        ("SRC3919_18_bloc_beta", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_1_beta", "3915 conditional beta zero"),
        ("SRC3919_19_gamma_guard", SRC / "P8_Y5_R2FR_3918_GAMMA_DECISION_GATE.csv", "DEC3918_2_guard", "3918 common-mode guard"),
        ("SRC3919_20_common_mode", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_6_common_mode_separation", "1944 gamma/common-mode separation"),
        ("SRC3919_21_validation", SRC / "P8_Y5_BRR545_3918_VALIDATION.csv", "VAL3918_15_no_pycache", "3918 validation handoff"),
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
                    excerpt = line[:650]
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


def beta_lock_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BETA3919_0_definition", "PPN beta source definition", BETA_DEF, "beta is the quadratic g00 response after Newtonian source normalization", "FORMULA_READY"),
        ("BETA3919_1_expansion", "source expansion", PPN_G00, "A_source is first-order Newton coupling; B_source is second-order source response", "NORMAL_FORM"),
        ("BETA3919_2_Newton_lock", "linear lock", "Z_Poisson=1 and Z_frame=1 set A_source=1 after measured-GM calibration", "same Hilbert source and same observed frame", "CONDITIONAL_A_SOURCE_ONE"),
        ("BETA3919_3_EH_square", "EH nonlinear square law", EH_G00, "stationary one-metric EH/Hilbert branch has beta=1, hence B_source=A_source^2", "CONDITIONAL_B_SOURCE_LOCK"),
        ("BETA3919_4_source_zero", "source beta theorem-zero", BETA_LOCK, "under the 3914/3915 branch, delta_beta_source=0 without fitting a new parameter", "CONDITIONAL_THEOREM_ZERO"),
        ("BETA3919_5_escape", "source-shadow escape", "if matter sees a different frame, non-Hilbert source, or second-order source shadow, keep B_source/A_source^2-1 as an explicit residual", "fallback row remains active outside B_loc", "BOUND_OR_FILL_IF_BRANCH_FAILS"),
    ]
    return [
        {
            "row_id": row_id,
            "piece": piece,
            "formula_or_statement": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, formula, meaning, status in data
    ]


def common_mode_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CM3919_0_gamma_blind", "gamma-blind common mode", "Phi_R11=Psi_R11 does not alter delta_gamma_R11 at linear order", "3918 closes only the STF/slip sector", "ACTIVE_AFTER_GAMMA"),
        ("CM3919_1_effective_coefficients", "effective beta coefficients", COMMON_MODE, "common mode is harmless for beta only if its quadratic coefficient scales as the square of its linear coefficient", "DERIVED_CALIBRATED_FORM"),
        ("CM3919_2_square_law", "mass-renormalization square law", SQUARE_LAW, "a pure GR-like mass rescaling preserves beta after measured-GM calibration", "CONDITIONAL_ZERO"),
        ("CM3919_3_small_bound", "small residual bound", SMALL_BOUND, "if xi_1,xi_2 are small, beta forces the mismatch xi_2-2xi_1 below the PPN beta tolerance", "BOUND_FORMULA"),
        ("CM3919_4_radial_guard", "nonconstant common mode", "radial/time/source-dependent Xi_N cannot be hidden in GM; route it to inverse-square, ephemeris, Gdot and beta residuals", "prevents orbital-GM absorption shortcut", "NO_ABSORPTION_GUARD"),
    ]
    return [
        {
            "row_id": row_id,
            "piece": piece,
            "formula_or_statement": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, formula, meaning, status in data
    ]


def bound_input_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BIN3919_0_A_source", "A_source", "dimensionless", "linear source coefficient", "one by Z_Poisson/Z_frame in B_loc or numeric fallback"),
        ("BIN3919_1_B_source", "B_source", "dimensionless", "quadratic source coefficient", "A_source^2 by EH nonlinear completion or numeric fallback"),
        ("BIN3919_2_xi1", "xi_1", "dimensionless", "linear R11 common-mode coefficient", "constant part may renormalize GM; nonconstant part must be bounded"),
        ("BIN3919_3_xi2", "xi_2", "dimensionless", "quadratic R11 common-mode coefficient", "must satisfy xi_2=2xi_1+xi_1^2 or beta shifts"),
        ("BIN3919_4_delta_beta_common", "delta_beta_common", "dimensionless", "(1+xi_2)/(1+xi_1)^2-1", "compare to 7.8e-05 if square law not proved"),
        ("BIN3919_5_XiN_radial", "d_r Xi_N", "per_length_or_dimensionless_gradient", "radial common-mode drift", "route to inverse-square/ephemeris bound"),
        ("BIN3919_6_XiN_time", "d_t Xi_N", "per_time", "time-dependent common-mode drift", "route to dotG/G bound"),
        ("BIN3919_7_source_shadow", "S_shadow^(2)", "dimensionless_or_stress_response", "second-order non-Hilbert source shadow", "must be zero by same-frame Hilbert descent or bounded"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "units": units,
            "role": role,
            "source_or_zero_rule": rule,
            "numeric_value": "",
            "status": "THEOREM_ZERO_OR_FALLBACK_BOUND_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, role, rule in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3919_0_beta_source",
            "decision": "beta/source has a conditional theorem-zero route",
            "formula": BETA_LOCK,
            "why": "same-frame EH/Hilbert branch fixes the quadratic g00 response once the Newtonian source is calibrated",
            "claim_status": "PRIVATE_CONDITIONAL_RESULT_NOT_PUBLIC_CLAIM",
            "next_action": "prove or bound the common-mode square law",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3919_1_common_mode",
            "decision": "gamma-blind common mode is now the sharp beta/Newton bottleneck",
            "formula": COMMON_MODE,
            "why": "P_TF zero can leave Phi_R11=Psi_R11; beta sees whether the quadratic piece scales correctly",
            "claim_status": "LOCAL_GR_STILL_BLOCKED_BY_COMMON_MODE",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3919_2_no_absorption",
            "decision": "do not hide radial/time common mode inside orbital GM",
            "formula": "constant square-law mass rescaling is calibration; radial/time/source-dependent Xi_N is a residual",
            "why": "keeps Newton, ephemeris and dotG tests honest",
            "claim_status": "NO_CANCELLATION_NO_GM_ABSORPTION_GUARD",
            "next_action": "separate constant square-law Xi_N from radial/time/source-dependent Xi_N",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3919_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove the R11 common-mode square law xi_2=2xi_1+xi_1^2, or build a beta/Newton/ephemeris bound runner for Xi_N",
            "why_this_next": "3918 made gamma STF-only and 3919 made beta source-lock conditional; common mode is the remaining local metric residual that can still spoil GR",
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
            "summary": "beta/source square-law route constructed; common-mode square-law or bound is next",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3919 - Beta Source Second-Order Lock or Common-Mode R11 Bound

Timestamp: `{timestamp}`

## Result

The beta/source piece now has a clean conditional route:

`{PPN_G00}`

with

`{BETA_DEF}`.

Inside the same-frame EH/Hilbert/local source branch, Newton calibration gives `A_source=1`, and the EH nonlinear completion gives:

`{EH_G00}`

therefore:

`{BETA_LOCK}`.

## Common-Mode Residual

3918 showed that `gamma` only sees the traceless/STF slip. A gamma-blind common mode can still survive:

`{COMMON_MODE}`.

The square-law condition for harmless mass renormalization is:

`{SQUARE_LAW}`.

Small-residual fallback:

`{SMALL_BOUND}`.

## Meaning

This is the next real narrowing: `beta` is not just another vague missing coefficient. It splits into a GR/EH source square law plus a common-mode square-law test. Constant square-law mass renormalization can be calibration; radial, time-dependent, or source-dependent common mode cannot be hidden inside orbital `GM`.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3919_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3919_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3919_BETA_SOURCE_LOCK_DERIVATION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3919_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3919_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3919 - Beta Source Lock and Common-Mode Square Law

Timestamp: `{timestamp}`

- Beta source definition: `{BETA_DEF}`.
- EH/source lock: `{BETA_LOCK}` inside the same-frame EH/Hilbert branch.
- Common-mode coefficient law: `{COMMON_MODE}`.
- Harmless common-mode condition: `{SQUARE_LAW}`.
- Small fallback bound: `{SMALL_BOUND}`.
- Status: private conditional progress only; local-GR still requires common-mode square-law proof or source-backed bound.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3919 - Beta Source Lock and Common-Mode Square Law"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    beta_lock = beta_lock_rows(timestamp)
    common = common_mode_rows(timestamp)
    bound_inputs = bound_input_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3919_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3919_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3919_02_beta_lock", any(row["row_id"] == "BETA3919_4_source_zero" for row in beta_lock), "beta source theorem-zero row emitted"),
        ("VAL3919_03_common_square_law", any(row["row_id"] == "CM3919_2_square_law" for row in common), "common-mode square-law row emitted"),
        ("VAL3919_04_small_bound", any(row["row_id"] == "CM3919_3_small_bound" for row in common), "small common-mode beta bound emitted"),
        ("VAL3919_05_bound_inputs", len(bound_inputs) == 8, "all beta/common-mode fallback inputs listed"),
        ("VAL3919_06_no_absorption_guard", any(row["row_id"] == "DEC3919_2_no_absorption" for row in decisions), "no orbital-GM absorption guard emitted"),
        ("VAL3919_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (beta_lock, common, bound_inputs, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3919_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3919_09_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3919_10_spine_written", SPINE_PATH.exists() and "3919 - Beta Source Lock and Common-Mode Square Law" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3919_11_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3919_12_script_compiles", True, "script compiles"),
        ("VAL3919_13_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["beta_lock"], beta_lock_rows(timestamp))
    write_csv(OUTPUTS["common_mode"], common_mode_rows(timestamp))
    write_csv(OUTPUTS["bound_inputs"], bound_input_rows(timestamp))
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
        raise SystemExit(f"3919 validation failed: {failed}")
    print(f"3919 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
