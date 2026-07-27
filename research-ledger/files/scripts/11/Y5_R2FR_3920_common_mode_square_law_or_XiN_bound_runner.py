from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3920"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3920-Y5-R2FR-common-mode-square-law-or-XiN-bound-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3920_SOURCE_REGISTER.csv",
    "law": SRC / "P8_Y5_R2FR_3920_COMMON_MODE_SOURCE_AND_SQUARE_LAW.csv",
    "runner": SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv",
    "arenas": SRC / "P8_Y5_R2FR_3920_NEWTON_EPHEMERIS_GDOT_LINKS.csv",
    "decision": SRC / "P8_Y5_R2FR_3920_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3920_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3920_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3920_VALIDATION.csv",
}

P00_SOURCE = "C_0 nabla^2 Xi_N = -kappa_R P00[R11], with C_0:=C00_Phi+C00_Psi and Phi_R11=Psi_R11=Xi_N"
XIN_SOLUTION = "Xi_N = -(kappa_R/C_0) nabla^{-2} P00[R11]"
BETA_EXACT = "delta_beta_common = (1+xi_2)/(1+xi_1)^2 - 1 = (xi_2-2 xi_1-xi_1^2)/(1+xi_1)^2"
SQUARE_LAW = "Delta_sq:=xi_2-2 xi_1-xi_1^2=0"
BETA_BOUND = "|Delta_sq| <= 7.8e-05*(1+xi_1)^2"
NEWTON_SHAPE = "a_obs/a_N = (1+xi_1)-r partial_r xi_1; constant xi_1 is GM calibration, nonconstant xi_1 is a Newton/ephemeris residual"
GDOT_LINK = "partial_t ln(GM_obs)=partial_t ln(1+xi_1)"
NEXT_DOC = "3921-Y5-R2FR-P00-common-mode-source-zero-or-XiN-numeric-bound-fill.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3921_P00_common_mode_source_zero_or_XiN_numeric_bound_fill.py"


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
        ("SRC3920_00_next", SRC / "P8_Y5_R2FR_3919_NEXT_TARGET.csv", "NEXT3919_0", "3919 selected common-mode square-law/XiN target"),
        ("SRC3920_01_cm_gamma", SRC / "P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv", "CM3919_0_gamma_blind", "gamma-blind common mode"),
        ("SRC3920_02_cm_coeff", SRC / "P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv", "CM3919_1_effective_coefficients", "effective beta common-mode coefficients"),
        ("SRC3920_03_cm_square", SRC / "P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv", "CM3919_2_square_law", "3919 square-law condition"),
        ("SRC3920_04_cm_bound", SRC / "P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv", "CM3919_3_small_bound", "3919 beta common-mode bound"),
        ("SRC3920_05_cm_radial", SRC / "P8_Y5_R2FR_3919_COMMON_MODE_SQUARE_LAW.csv", "CM3919_4_radial_guard", "3919 radial/time guard"),
        ("SRC3920_06_bin_xi1", SRC / "P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv", "BIN3919_2_xi1", "xi1 fallback input"),
        ("SRC3920_07_bin_xi2", SRC / "P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv", "BIN3919_3_xi2", "xi2 fallback input"),
        ("SRC3920_08_bin_radial", SRC / "P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv", "BIN3919_5_XiN_radial", "XiN radial fallback input"),
        ("SRC3920_09_bin_time", SRC / "P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv", "BIN3919_6_XiN_time", "XiN time fallback input"),
        ("SRC3920_10_dec_common", SRC / "P8_Y5_R2FR_3919_DECISION_GATE.csv", "DEC3919_1_common_mode", "3919 common-mode decision"),
        ("SRC3920_11_no_absorb", SRC / "P8_Y5_R2FR_3919_DECISION_GATE.csv", "DEC3919_2_no_absorption", "no orbital-GM absorption guard"),
        ("SRC3920_12_scalar00", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_2_scalar_00_projection", "1944 scalar/common-mode equation"),
        ("SRC3920_13_common_sep", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_6_common_mode_separation", "1944 common-mode separation"),
        ("SRC3920_14_orbit_exterior", SRC / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv", "ORB3884_0_exterior", "orbital exterior potential"),
        ("SRC3920_15_orbit_guard", SRC / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv", "ORB3884_1_no_range", "no calibration cheat guard"),
        ("SRC3920_16_ppn_beta", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_2_beta", "beta square-law guard"),
        ("SRC3920_17_ppn_orbit_beta", SRC / "P8_Y5_R2FR_3652_PPN_ORBITAL_RESIDUAL_VECTOR_ROWS.csv", "PVR3652_1_beta", "PPN beta residual row"),
        ("SRC3920_18_ppn_orbit_gdot", SRC / "P8_Y5_R2FR_3652_PPN_ORBITAL_RESIDUAL_VECTOR_ROWS.csv", "PVR3652_6_Gdot", "Gdot orbital residual row"),
        ("SRC3920_19_gdot_bound", SRC / "P8_Y5_R2FR_3908_OBSERVABLE_BUDGET_TARGETS.csv", "BUD3908_0_Gdot", "Gdot budget target"),
        ("SRC3920_20_gdot_runner", SRC / "P8_Y5_R2FR_3908_GSTAR_DERIVATIVE_BOUND_RUNNER.csv", "RUN3908_1_Gdot", "Gdot derivative runner"),
        ("SRC3920_21_validation", SRC / "P8_Y5_BRR545_3919_VALIDATION.csv", "VAL3919_13_no_pycache", "3919 validation handoff"),
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
                    excerpt = line[:700]
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


def law_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LAW3920_0_scalar_source", "scalar common-mode source equation", P00_SOURCE, "when P_TF=0, the remaining linear R11 common mode is the scalar 00 source", "DERIVED_FROM_1944_SYMBOLIC"),
        ("LAW3920_1_Xi_solution", "formal Xi_N solution", XIN_SOLUTION, "turns common mode into a P00/source and boundary-domain problem", "FORMAL_SOLUTION_INPUTS_MISSING"),
        ("LAW3920_2_xi1", "linear common-mode coefficient", "xi_1 := Xi_N/U_N", "constant xi_1 is a measured-GM calibration; gradients/time/source dependence are residuals", "COEFFICIENT_DEFINED"),
        ("LAW3920_3_beta_exact", "exact beta common-mode identity", BETA_EXACT, "the square-law error is not approximate; only the small-bound simplification is approximate", "EXACT_ALGEBRAIC_IDENTITY"),
        ("LAW3920_4_square_law", "harmless square law", SQUARE_LAW, "equivalent to beta_common=0 for finite 1+xi_1", "CONDITIONAL_THEOREM_ZERO"),
        ("LAW3920_5_beta_bound", "fallback beta bound", BETA_BOUND, "if square law is not derived, this is the no-cancellation beta gate", "BOUND_INTERFACE_READY"),
        ("LAW3920_6_EH_completion", "EH completion route", "if the common mode is just U_obs=(1+xi_1)U_N inside one EH metric, the O(U^2) term forces xi_2=2xi_1+xi_1^2", "this is the clean derivation route, not a fitted cancellation", "CONDITIONAL_SQUARE_LAW_FROM_ONE_METRIC_EH"),
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


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN3920_0_Delta_sq", "Delta_sq", "xi_2-2xi_1-xi_1^2", "square-law error", "zero by EH completion or compare with beta bound"),
        ("RUN3920_1_beta_common", "delta_beta_common", "(xi_2-2xi_1-xi_1^2)/(1+xi_1)^2", "exact beta residual", "requires xi_1 != -1 and sourced xi rows"),
        ("RUN3920_2_beta_acceptance", "beta acceptance", BETA_BOUND, "PPN beta gate", "use absolute no-cancellation rule"),
        ("RUN3920_3_Xi_source", "Xi_N source", XIN_SOLUTION, "derive xi_1 from P00", "requires kappa_R,C_0,P00,boundary domain"),
        ("RUN3920_4_radial_shape", "Newton radial residual", "epsilon_r(r)=|((1+xi_1)-r partial_r xi_1)/(1+xi_ref)-1|", "inverse-square/ephemeris residual", "constant xi_ref may calibrate GM; gradients cannot"),
        ("RUN3920_5_time_drift", "Gdot residual", "|partial_t ln(1+xi_1)| <= 9.6e-15 yr^-1", "dotG/G channel", "uses 3908 bound if xi_1 is time-dependent"),
        ("RUN3920_6_source_dependence", "source dependence", "Delta_AB xi_1 and Delta_AB Delta_sq", "WEP/source-shadow channel", "composition/source dependence cannot be hidden in GM"),
        ("RUN3920_7_no_absorption", "guard", "constant square-law Xi_N is calibration; radial/time/source-dependent Xi_N is residual", "policy gate", "prevents fake local-GR pass"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "observable_role": role,
            "required_inputs_or_rule": inputs,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, role, inputs in data
    ]


def arena_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ARE3920_0_beta", "PPN beta", BETA_EXACT, "pass only if Delta_sq=0 theorem or |Delta_sq| below bound", "NOT_CLAIMED"),
        ("ARE3920_1_Newton", "Newton/inverse-square", NEWTON_SHAPE, "constant xi_1 can be GM calibration; radial xi_1 creates force-law residual", "BOUND_REQUIRED_IF_NONCONSTANT"),
        ("ARE3920_2_ephemeris", "orbital/ephemeris", "epsilon_r and any finite-range shape are scored against orbital residual rows", "do not absorb range/radial/source hair into the monopole", "BOUND_REQUIRED_IF_NONCONSTANT"),
        ("ARE3920_3_Gdot", "dotG/G", GDOT_LINK, "time-varying common mode enters measured GM drift", "BOUND_REQUIRED_IF_TIME_DEPENDENT"),
        ("ARE3920_4_WEP_source", "source/WEP", "Delta_AB xi_1 or Delta_AB Delta_sq", "source-composition dependence is not universal calibration", "BOUND_REQUIRED_IF_SOURCE_DEPENDENT"),
    ]
    return [
        {
            "row_id": row_id,
            "arena": arena,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, arena, formula, meaning, status in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3920_0_square_law",
            "decision": "common-mode beta is reduced to one exact square-law error",
            "formula": BETA_EXACT,
            "claim_status": "PRIVATE_CONDITIONAL_RESULT_NOT_PUBLIC_CLAIM",
            "next_action": "prove P00/square-law zero or source xi_1,xi_2 inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3920_1_calibration_split",
            "decision": "constant square-law Xi_N is calibration; nonconstant Xi_N is not",
            "formula": NEWTON_SHAPE,
            "claim_status": "NO_GM_ABSORPTION_GUARD_ACTIVE",
            "next_action": "split xi_1 into constant, radial, time and source-dependent pieces",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3920_2_next",
            "decision": "next target is P00 common-mode source zero or numeric bound fill",
            "formula": P00_SOURCE,
            "claim_status": "LOCAL_GR_STILL_BLOCKED_BY_P00_OR_XIN_INPUTS",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3920_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive P00[R11]=0/common-mode square-law from EH/DZ/source descent, or fill numeric Xi_N rows for beta, Newton, ephemeris and Gdot",
            "why_this_next": "3920 makes the common-mode obstruction exact: Delta_sq for beta plus gradients/time/source dependence for Newton/orbits/Gdot",
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
            "summary": "common-mode square-law identity and Xi_N bound runner constructed",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3920 - Common-Mode Square Law or XiN Bound Runner

Timestamp: `{timestamp}`

## Result

The common-mode obstruction has been turned into exact algebra plus a bound runner.

Linear common-mode source:

`{P00_SOURCE}`

so formally:

`{XIN_SOLUTION}`.

Define `xi_1:=Xi_N/U_N`. The exact beta residual is:

`{BETA_EXACT}`.

Therefore the harmless square-law condition is:

`{SQUARE_LAW}`.

Fallback beta gate:

`{BETA_BOUND}`.

## Calibration Split

`{NEWTON_SHAPE}`.

This is the useful split: constant square-law common mode can be measured-`GM` calibration, but radial, time-dependent, finite-range, or source-dependent common mode is a real residual. For time dependence:

`{GDOT_LINK}`.

## Meaning

This is a leap forward in the local-GR route: the common-mode problem is no longer a vague complaint. It is either an EH one-metric square law, or it becomes explicit rows for `Delta_sq`, `P00[R11]`, `partial_r xi_1`, `partial_t xi_1`, and source-dependence.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3920_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3920_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3920_COMMON_MODE_SOURCE_AND_SQUARE_LAW.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3920_NEWTON_EPHEMERIS_GDOT_LINKS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3920_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3920_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3920 - Common-Mode Square Law or XiN Bound Runner

Timestamp: `{timestamp}`

- Linear common-mode source: `{P00_SOURCE}`.
- Exact beta residual: `{BETA_EXACT}`.
- Harmless square law: `{SQUARE_LAW}`.
- Beta fallback gate: `{BETA_BOUND}`.
- Newton/orbital calibration split: `{NEWTON_SHAPE}`.
- Gdot link: `{GDOT_LINK}`.
- Status: private conditional progress only; local-GR still requires P00/common-mode zero or source-backed Xi_N bounds.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3920 - Common-Mode Square Law or XiN Bound Runner"
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
    laws = law_rows(timestamp)
    runners = runner_rows(timestamp)
    arenas = arena_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3920_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3920_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3920_02_p00_source", any(row["row_id"] == "LAW3920_0_scalar_source" for row in laws), "P00 common-mode source equation emitted"),
        ("VAL3920_03_exact_beta_identity", any(row["row_id"] == "LAW3920_3_beta_exact" for row in laws), "exact beta common-mode identity emitted"),
        ("VAL3920_04_square_law", any(row["row_id"] == "LAW3920_4_square_law" for row in laws), "square-law condition emitted"),
        ("VAL3920_05_runner_rows", len(runners) == 8, "Xi_N runner rows emitted"),
        ("VAL3920_06_arena_links", len(arenas) == 5, "Newton/ephemeris/Gdot/WEP arena links emitted"),
        ("VAL3920_07_no_absorption", any(row["row_id"] == "DEC3920_1_calibration_split" for row in decisions), "calibration split guard emitted"),
        ("VAL3920_08_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (laws, runners, arenas, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3920_09_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3920_10_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3920_11_spine_written", SPINE_PATH.exists() and "3920 - Common-Mode Square Law or XiN Bound Runner" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3920_12_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3920_13_script_compiles", True, "script compiles"),
        ("VAL3920_14_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["law"], law_rows(timestamp))
    write_csv(OUTPUTS["runner"], runner_rows(timestamp))
    write_csv(OUTPUTS["arenas"], arena_rows(timestamp))
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
        raise SystemExit(f"3920 validation failed: {failed}")
    print(f"3920 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
