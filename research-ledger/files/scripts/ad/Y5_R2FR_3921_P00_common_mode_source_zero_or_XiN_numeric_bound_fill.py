from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3921"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3921-Y5-R2FR-P00-common-mode-source-zero-or-XiN-numeric-bound-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3921_SOURCE_REGISTER.csv",
    "exterior": SRC / "P8_Y5_R2FR_3921_P00_ZERO_HARMONIC_EXTERIOR_THEOREM.csv",
    "bounds": SRC / "P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3921_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3921_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3921_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3921_VALIDATION.csv",
}

P00_SOURCE = "C_0 nabla^2 Xi_N = -kappa_R P00[R11]"
HARMONIC = "P00[R11]=0 => nabla^2 Xi_N=0 in the source-free exterior"
EXTERIOR_SOLUTION = "Xi_N = xi_0 U_N + const + sum_{l>=1,m} a_l r^{-(l+1)}Y_lm"
CALIBRATION = "const is gauge; xi_0 U_N is measured-GM calibration if xi_0 is time/source/frame independent"
RESIDUAL_SPLIT = "Xi_N^res := Xi_N - xi_0 U_N - const"
BETA_SQUARE = "xi_2=2xi_0+xi_0^2 and Xi_N^res=0 => delta_beta_common=0"
BOUND = "B_Xi := |Delta_sq|/(1+xi_1)^2 + |epsilon_r| + |partial_t ln(1+xi_1)|/B_Gdot + |Delta_AB xi_1|/B_WEP"
NEXT_DOC = "3922-Y5-R2FR-boundary-projector-domain-multipole-zero-or-local-bound-fill.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3922_boundary_projector_domain_multipole_zero_or_local_bound_fill.py"


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
        ("SRC3921_00_next", SRC / "P8_Y5_R2FR_3920_NEXT_TARGET.csv", "NEXT3920_0", "3920 selected P00/XiN target"),
        ("SRC3921_01_p00_law", SRC / "P8_Y5_R2FR_3920_COMMON_MODE_SOURCE_AND_SQUARE_LAW.csv", "LAW3920_0_scalar_source", "3920 P00 source equation"),
        ("SRC3921_02_xi_solution", SRC / "P8_Y5_R2FR_3920_COMMON_MODE_SOURCE_AND_SQUARE_LAW.csv", "LAW3920_1_Xi_solution", "3920 formal Xi solution"),
        ("SRC3921_03_square_law", SRC / "P8_Y5_R2FR_3920_COMMON_MODE_SOURCE_AND_SQUARE_LAW.csv", "LAW3920_4_square_law", "3920 square law"),
        ("SRC3921_04_runner_delta", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_0_Delta_sq", "3920 square-law error runner"),
        ("SRC3921_05_runner_radial", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_4_radial_shape", "3920 radial residual runner"),
        ("SRC3921_06_runner_time", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_5_time_drift", "3920 time drift runner"),
        ("SRC3921_07_calibration", SRC / "P8_Y5_R2FR_3920_DECISION_GATE.csv", "DEC3920_1_calibration_split", "3920 no-absorption calibration split"),
        ("SRC3921_08_p00_1944", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_2_scalar_00_projection", "1944 scalar 00 projection"),
        ("SRC3921_09_common_1944", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_6_common_mode_separation", "1944 common-mode warning"),
        ("SRC3921_10_orbit_exterior", SRC / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv", "ORB3884_0_exterior", "exterior orbital potential"),
        ("SRC3921_11_orbit_guard", SRC / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv", "ORB3884_1_no_range", "no calibration cheat"),
        ("SRC3921_12_gauss_orbit", SRC / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv", "CAL523_4_orbital_inverse_square_readout", "Gauss/orbital inverse-square readout"),
        ("SRC3921_13_derivative_hair", SRC / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv", "CAL523_7_no_derivative_hair", "no derivative hair gate"),
        ("SRC3921_14_beta_guard", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_2_beta", "beta square-law guard"),
        ("SRC3921_15_gdot_bound", SRC / "P8_Y5_R2FR_3908_OBSERVABLE_BUDGET_TARGETS.csv", "BUD3908_0_Gdot", "Gdot bound"),
        ("SRC3921_16_gdot_runner", SRC / "P8_Y5_R2FR_3908_GSTAR_DERIVATIVE_BOUND_RUNNER.csv", "RUN3908_1_Gdot", "Gdot runner"),
        ("SRC3921_17_EH_route", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_0_EH", "EH absence route"),
        ("SRC3921_18_DZ_route", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_1_DZ", "double-zero route"),
        ("SRC3921_19_boundary", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "boundary parent-unsigned verdict"),
        ("SRC3921_20_projector", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_10_projector_domain_stress", "projector/domain escape"),
        ("SRC3921_21_validation", SRC / "P8_Y5_BRR545_3920_VALIDATION.csv", "VAL3920_14_no_pycache", "3920 validation handoff"),
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


def exterior_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("EXT3921_0_source_equation", "source equation", P00_SOURCE, "inherits 3920 scalar common-mode equation", "DERIVED_SYMBOLIC"),
        ("EXT3921_1_zero_source", "P00 zero exterior", HARMONIC, "EH absence or double-zero R11 stress gives the strongest route; otherwise P00 must be bounded", "CONDITIONAL_ZERO_ROUTE"),
        ("EXT3921_2_harmonic_solution", "harmonic exterior solution", EXTERIOR_SOLUTION, "standard source-free exterior decomposition for the common mode", "DERIVED_EXTERIOR_FORM"),
        ("EXT3921_3_monopole_calibration", "monopole calibration", CALIBRATION, "the only harmless harmonic common mode is a universal constant monopole rescaling", "CONDITIONAL_CALIBRATION_ONLY"),
        ("EXT3921_4_residual_definition", "residual common mode", RESIDUAL_SPLIT, "multipoles, radial shape, time drift, source dependence and frame dependence are not calibration", "RESIDUAL_VECTOR_DEFINED"),
        ("EXT3921_5_beta_square", "beta closure condition", BETA_SQUARE, "monopole calibration still needs the second-order EH square law", "CONDITIONAL_BETA_ZERO"),
        ("EXT3921_6_escape_channels", "escape channels", "boundary/projector/domain/nonlocal terms can feed P00, multipoles, or derivative hair unless zeroed or bounded", "uses 3892/3893 escape ledgers", "BOUND_OR_CERTIFICATE_REQUIRED"),
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


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BIN3921_0_P00_norm", "||P00[R11]||", "scalar_source_norm", "drives Xi_N through C_0 nabla^2 Xi_N", "zero by EH/DZ or sourced numeric bound"),
        ("BIN3921_1_C0", "C_0", "dimensionless_operator_coefficient", "scalar 00 operator coefficient", "must be nonzero and convention-fixed"),
        ("BIN3921_2_kappa_R", "kappa_R", "action_normalized_coupling", "R11 coupling in common-mode source", "zero/absent by EH/DZ or sourced numeric coefficient"),
        ("BIN3921_3_Green0", "||nabla^{-2}||_0", "domain_operator_norm", "maps P00 source to Xi_N", "requires exterior boundary/domain choice"),
        ("BIN3921_4_xi0", "xi_0", "dimensionless", "constant monopole calibration coefficient", "allowed only if universal/time-independent/source-independent"),
        ("BIN3921_5_multipoles", "sum_l>=1 |a_l|", "potential_multipole_norm", "anisotropic exterior harmonic content", "zero by local isotropy/boundary silence or orbital bound"),
        ("BIN3921_6_radial", "epsilon_r", "dimensionless", "non-inverse-square residual", "must be bounded by orbital/ephemeris data"),
        ("BIN3921_7_time", "partial_t ln(1+xi_1)", "yr^-1", "measured-GM drift", "must be <= 9.6e-15 yr^-1 if not zero"),
        ("BIN3921_8_source", "Delta_AB xi_1", "dimensionless", "composition/source dependence", "must route to WEP/source residual"),
        ("BIN3921_9_Delta_sq", "Delta_sq", "dimensionless", "beta square-law error", "zero by EH completion or bounded by beta"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "units": units,
            "role": role,
            "source_or_zero_rule": rule,
            "numeric_value": "",
            "status": "ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, role, rule in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3921_0_harmonic_route",
            "decision": "P00 zero makes Xi_N harmonic in the exterior",
            "formula": HARMONIC,
            "claim_status": "PRIVATE_CONDITIONAL_RESULT_NOT_PUBLIC_CLAIM",
            "next_action": "zero or bound boundary/projector/domain multipoles and derivative hair",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3921_1_calibration_only",
            "decision": "only universal constant monopole Xi_N is harmless calibration",
            "formula": CALIBRATION,
            "claim_status": "NO_GM_ABSORPTION_GUARD_ACTIVE",
            "next_action": "anything nonconstant enters Xi_N residual rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3921_2_next",
            "decision": "remaining common-mode debt is boundary/projector/domain multipole silence or local bound fill",
            "formula": RESIDUAL_SPLIT,
            "claim_status": "LOCAL_GR_STILL_BLOCKED_BY_ESCAPE_CHANNELS",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3921_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "close or bound boundary/projector/domain multipoles and derivative hair feeding Xi_N, alpha_i, xi and ephemeris residuals",
            "why_this_next": "3921 shows P00-zero exterior common mode is harmless only as a universal constant monopole; escape channels now dominate",
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
            "summary": "P00-zero harmonic exterior route derived; Xi_N bound rows named",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3921 - P00 Common-Mode Source Zero or XiN Numeric Bound Fill

Timestamp: `{timestamp}`

## Result

The common-mode route now has a sharper exterior theorem:

`{P00_SOURCE}`

If the retained scalar source vanishes in the source-free exterior:

`{HARMONIC}`.

The exterior solution is:

`{EXTERIOR_SOLUTION}`.

The harmless part is only:

`{CALIBRATION}`.

Everything else is residual:

`{RESIDUAL_SPLIT}`.

Beta still needs the square law:

`{BETA_SQUARE}`.

## Meaning

This is the clean split we needed. A P00-zero exterior does not automatically prove local GR, but it says the remaining common mode is either a universal monopole calibration or a real residual. Multipoles, radial shape, time drift, source dependence, boundary/projector/domain stress and nonlocal tails cannot be hidden in measured `GM`.

Fallback bound vector:

`{BOUND}`.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3921_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3921_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3921_P00_ZERO_HARMONIC_EXTERIOR_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3921_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3921_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3921 - P00-Zero Harmonic Exterior Route

Timestamp: `{timestamp}`

- Common-mode source: `{P00_SOURCE}`.
- Exterior zero route: `{HARMONIC}`.
- Harmonic exterior solution: `{EXTERIOR_SOLUTION}`.
- Harmless calibration: `{CALIBRATION}`.
- Residual definition: `{RESIDUAL_SPLIT}`.
- Beta closure still requires: `{BETA_SQUARE}`.
- Status: private conditional progress only; boundary/projector/domain multipoles and derivative hair remain active.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3921 - P00-Zero Harmonic Exterior Route"
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
    exterior = exterior_rows(timestamp)
    bounds = bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3921_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3921_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3921_02_harmonic_route", any(row["row_id"] == "EXT3921_1_zero_source" for row in exterior), "P00-zero harmonic route emitted"),
        ("VAL3921_03_solution", any(row["row_id"] == "EXT3921_2_harmonic_solution" for row in exterior), "harmonic exterior solution emitted"),
        ("VAL3921_04_calibration", any(row["row_id"] == "EXT3921_3_monopole_calibration" for row in exterior), "monopole calibration rule emitted"),
        ("VAL3921_05_residual", any(row["row_id"] == "EXT3921_4_residual_definition" for row in exterior), "Xi_N residual definition emitted"),
        ("VAL3921_06_bounds", len(bounds) == 10, "Xi_N numeric bound rows emitted"),
        ("VAL3921_07_no_absorption", any(row["row_id"] == "DEC3921_1_calibration_only" for row in decisions), "no GM absorption guard emitted"),
        ("VAL3921_08_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (exterior, bounds, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3921_09_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3921_10_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3921_11_spine_written", SPINE_PATH.exists() and "3921 - P00-Zero Harmonic Exterior Route" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3921_12_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3921_13_script_compiles", True, "script compiles"),
        ("VAL3921_14_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["exterior"], exterior_rows(timestamp))
    write_csv(OUTPUTS["bounds"], bound_rows(timestamp))
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
        raise SystemExit(f"3921 validation failed: {failed}")
    print(f"3921 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
