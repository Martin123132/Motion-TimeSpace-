from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3927"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3927-Y5-R2FR-Bescape-component-bound-pack-projector-domain-boundary-history.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3927_SOURCE_REGISTER.csv",
    "components": SRC / "P8_Y5_R2FR_3927_BESCAPE_COMPONENT_FORMULAS.csv",
    "inputs": SRC / "P8_Y5_R2FR_3927_BESCAPE_INPUT_REQUIREMENTS.csv",
    "runner": SRC / "P8_Y5_R2FR_3927_BESCAPE_RUNNER_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3927_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3927_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3927_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3927_VALIDATION.csv",
}

PROJECTOR_DOMAIN = (
    "epsilon_domain_projector_abs <= "
    "C_Pi_g||delta_g P_D||op||J_H||*/M_H_ref + "
    "C_Pi_D||D_D P_D||op||delta D||||J_H||*/M_H_ref + "
    "C_chi||delta_g chi_D|| + |Phi_D|/M_H_ref"
)
BOUNDARY_HARMONIC = (
    "B_boundary_harmonic := |P00_boundary| + |B_harmonic_boundary| + |Phi_B|/M_H_ref + |tau_wall_TF|/M_H_ref"
)
HISTORY_NONLOCAL = (
    "B_history := K_hist[exp(-gamma_mem Delta t)||X_mem(t0)|| + (1-exp(-gamma_mem Delta t))sup||J_open+B_lift||/lambda_gap] + B_nonlocal_kernel"
)
DERIVATIVE_HAIR = "B_deriv := |partial_t xi_1| + |partial_r xi_1| + |Delta_AB xi_1| + |delta_frame xi_1|"
A_MULTI = (
    "A_multi <= G_ext*(|P00_boundary|+|P00_projector|+|P00_domain|+|P00_history|+|P00_nonlocal|)+B_harmonic_boundary"
)
BESCAPE = "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi + B_deriv + epsilon_domain_projector_abs"
NEXT_DOC = "3928-Y5-R2FR-projector-domain-certificate-or-first-Bescape-source-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3928_projector_domain_certificate_or_first_Bescape_source_values.py"


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
        ("SRC3927_00_next", SRC / "P8_Y5_R2FR_3926_NEXT_TARGET.csv", "NEXT3926_0", "3926 selected B_escape component pack"),
        ("SRC3927_01_priority", SRC / "P8_Y5_R2FR_3926_ESCAPE_BOUND_PRIORITY_MATRIX.csv", "PRI3926_0_projector_domain", "projector/domain first priority"),
        ("SRC3927_02_action_projector", SRC / "P8_Y5_R2FR_3926_CERTIFICATE_OR_BOUND_ACTION_QUEUE.csv", "ACT3926_0_projector", "projector action queue"),
        ("SRC3927_03_action_history", SRC / "P8_Y5_R2FR_3926_CERTIFICATE_OR_BOUND_ACTION_QUEUE.csv", "ACT3926_3_history", "history bound action"),
        ("SRC3927_04_escape_total", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_9_total", "B_escape formula"),
        ("SRC3927_05_A_multi", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_6_multipole_total", "A_multi bound"),
        ("SRC3927_06_deriv", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_7_derivative_hair", "B_deriv row"),
        ("SRC3927_07_domain_total", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_8_projector_domain_total", "domain/projector total"),
        ("SRC3927_08_DPOB0", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv", "DPOB3431_0_projector_derivative", "projector derivative bound"),
        ("SRC3927_09_DPOB1", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv", "DPOB3431_1_domain_motion", "domain motion bound"),
        ("SRC3927_10_DPOB2", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv", "DPOB3431_2_selector_metric_stress", "selector metric stress bound"),
        ("SRC3927_11_DPOB3", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv", "DPOB3431_3_boundary_flux", "domain boundary flux bound"),
        ("SRC3927_12_DPOB4", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv", "DPOB3431_4_total_domain_projector", "domain projector total"),
        ("SRC3927_13_boundary", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_2_scalar_monopole", "boundary scalar monopole policy"),
        ("SRC3927_14_boundary_bound", SRC / "P8_Y5_R2FR_3834_BOUNDARY_HARMONIC_ELLIPTIC_ZERO_THEOREM.csv", "BH3834_2_bound_contract", "boundary harmonic bound contract"),
        ("SRC3927_15_history_zero", SRC / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv", "ZERO3895_4_history_exact", "history not global exact zero"),
        ("SRC3927_16_history_law", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_3_history_decay", "history decay law"),
        ("SRC3927_17_memory_amp", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_2_static_amplitude", "static memory amplitude"),
        ("SRC3927_18_beta_common", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_0_Delta_sq", "Delta_sq runner"),
        ("SRC3927_19_validation", SRC / "P8_Y5_BRR545_3926_VALIDATION.csv", "VAL3926_13_no_pycache", "3926 validation handoff"),
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


def component_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("COMP3927_0_projector_domain", "projector/domain stress", PROJECTOR_DOMAIN, "first-priority escape component"),
        ("COMP3927_1_boundary_harmonic", "boundary/harmonic", BOUNDARY_HARMONIC, "boundary P00 and free harmonic exterior data"),
        ("COMP3927_2_history_nonlocal", "history/nonlocal", HISTORY_NONLOCAL, "history tail and nonlocal kernel residual"),
        ("COMP3927_3_derivative_hair", "derivative hair", DERIVATIVE_HAIR, "time/radial/source/frame derivatives of common mode"),
        ("COMP3927_4_multipole", "multipole total", A_MULTI, "l>=1 harmonic exterior multipole total"),
        ("COMP3927_5_total", "B_escape total", BESCAPE, "escape component of local-GR residual envelope"),
    ]
    return [
        {
            "row_id": row_id,
            "component": component,
            "formula": formula,
            "role": role,
            "numeric_value": "",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, formula, role in data
    ]


def input_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("IN3927_0_delta_g_PD", "||delta_g P_D||op", "operator_norm", "projector metric derivative norm", "projector/domain"),
        ("IN3927_1_DD_PD", "||D_D P_D||op", "operator_norm", "domain derivative norm", "projector/domain"),
        ("IN3927_2_deltaD", "||delta D||", "domain_motion_amplitude", "moving support/domain amplitude", "projector/domain"),
        ("IN3927_3_JH", "||J_H||*", "source_norm", "dual Hilbert source norm", "projector/domain"),
        ("IN3927_4_MHref", "M_H_ref", "mass", "reference Hilbert mass denominator", "normalization"),
        ("IN3927_5_chi", "||delta_g chi_D||", "selector_metric_norm", "selector metric stress", "domain"),
        ("IN3927_6_PhiD", "Phi_D", "flux_or_stress", "domain boundary/collar flux", "domain/boundary"),
        ("IN3927_7_P00_boundary", "P00_boundary", "scalar_source_norm", "boundary common-mode source", "boundary"),
        ("IN3927_8_Bharm", "B_harmonic_boundary", "potential_multipole_norm", "free harmonic boundary amplitude", "boundary"),
        ("IN3927_9_tauwall", "tau_wall_TF", "stress_norm", "boundary wall anisotropic stress", "boundary"),
        ("IN3927_10_gamma_mem", "gamma_mem", "per_time", "history decay rate", "history"),
        ("IN3927_11_Deltat", "Delta t", "time", "history decay interval", "history"),
        ("IN3927_12_X0", "||X_mem(t0)||", "field_amplitude", "incoming memory amplitude", "history"),
        ("IN3927_13_lambda_gap", "lambda_gap", "operator_gap", "memory elliptic/coercive gap", "history"),
        ("IN3927_14_Jopen", "sup||J_open+B_lift||", "source_norm", "open memory source and boundary lift", "history"),
        ("IN3927_15_Bnonlocal", "B_nonlocal_kernel", "source_norm", "nonlocal kernel tail bound", "nonlocal"),
        ("IN3927_16_derivatives", "partial_t/r/A/frame xi_1", "mixed_derivative", "common-mode derivative hair", "derivative"),
        ("IN3927_17_Deltasq", "Delta_sq", "dimensionless", "common-mode square-law error", "beta/common"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "units": units,
            "definition": definition,
            "component": component,
            "numeric_value": "",
            "source_status": "SOURCE_VALUE_REQUIRED_OR_THEOREM_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, definition, component in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN3927_0_projector_domain", "epsilon_domain_projector_abs", PROJECTOR_DOMAIN, "score only after all projector/domain inputs sourced or zeroed"),
        ("RUN3927_1_boundary", "B_boundary_harmonic", BOUNDARY_HARMONIC, "score only after boundary/harmonic source amplitudes sourced or zeroed"),
        ("RUN3927_2_history", "B_history", HISTORY_NONLOCAL, "score only after decay/gap/history inputs sourced or reset theorem signed"),
        ("RUN3927_3_derivative", "B_deriv", DERIVATIVE_HAIR, "score only after derivative hair inputs sourced or derivative silence proved"),
        ("RUN3927_4_multipole", "A_multi", A_MULTI, "score after source split plus boundary harmonic amplitude"),
        ("RUN3927_5_escape", "B_escape", BESCAPE, "absolute-sum no-cancellation component; not score-ready with placeholders"),
    ]
    return [
        {
            "row_id": row_id,
            "runner_target": target,
            "formula": formula,
            "acceptance_rule": rule,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, target, formula, rule in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3927_0_pack",
            "decision": "B_escape component formulas are now explicit",
            "formula": BESCAPE,
            "claim_status": "NONCLAIM_FORMULA_PACK_VALUES_MISSING",
            "next_action": "try projector/domain certificate or source values first",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3927_1_priority",
            "decision": "projector/domain remains first because it feeds the broadest set of local residuals",
            "formula": PROJECTOR_DOMAIN,
            "claim_status": "FIRST_BOUND_OR_CERTIFICATE_TARGET",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3927_2_no_score",
            "decision": "B_escape cannot be scored yet",
            "formula": "source values missing for projector/domain, boundary/harmonic, history/nonlocal and derivative hair",
            "claim_status": "SCORE_BLOCKED_VALUES_MISSING",
            "next_action": "source or theorem-zero the first component",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3927_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attempt the projector/domain certificate first; if not signed, fill first source-backed epsilon_domain_projector_abs values",
            "why_this_next": "projector/domain stress is the rank-1 B_escape component and has the broadest PPN/local-GR impact",
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
            "summary": "B_escape component formula/input/runner pack built; projector/domain selected first",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3927 - B_escape Component Bound Pack: Projector/Domain, Boundary, History

Timestamp: `{timestamp}`

## Result

Built the `B_escape` component formula pack.

Projector/domain:

`{PROJECTOR_DOMAIN}`.

Boundary/harmonic:

`{BOUNDARY_HARMONIC}`.

History/nonlocal:

`{HISTORY_NONLOCAL}`.

Derivative hair:

`{DERIVATIVE_HAIR}`.

Total:

`{BESCAPE}`.

## Meaning

The escape obstruction is now executable in structure: every major term has a formula, input list, and runner row. It is still not score-ready because source values or theorem-zero certificates are missing. The first target is projector/domain stress because it feeds the widest set of local-GR residuals.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3927_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3927_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3927_BESCAPE_COMPONENT_FORMULAS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3927_BESCAPE_INPUT_REQUIREMENTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3927_BESCAPE_RUNNER_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3927_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3927_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3927 - B_escape Component Bound Pack

Timestamp: `{timestamp}`

- Projector/domain: `{PROJECTOR_DOMAIN}`.
- Boundary/harmonic: `{BOUNDARY_HARMONIC}`.
- History/nonlocal: `{HISTORY_NONLOCAL}`.
- Derivative hair: `{DERIVATIVE_HAIR}`.
- Total: `{BESCAPE}`.
- Status: formulas/input rows ready; source values or theorem-zero certificates still required.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3927 - B_escape Component Bound Pack"
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
    components = component_rows(timestamp)
    inputs = input_rows(timestamp)
    runners = runner_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3927_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3927_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3927_02_components", len(components) == 6, "B_escape component formulas emitted"),
        ("VAL3927_03_inputs", len(inputs) == 18, "B_escape input requirements emitted"),
        ("VAL3927_04_runners", len(runners) == 6, "B_escape runner rows emitted"),
        ("VAL3927_05_projector_first", any(row["row_id"] == "DEC3927_1_priority" for row in decisions), "projector/domain priority decision emitted"),
        ("VAL3927_06_not_score_ready", all(str(row.get("score_ready")) == "False" for row in runners), "runner rows are not score-ready with placeholders"),
        ("VAL3927_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (components, inputs, runners, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3927_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3927_09_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3927_10_spine_written", SPINE_PATH.exists() and "3927 - B_escape Component Bound Pack" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3927_11_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3927_12_script_compiles", True, "script compiles"),
        ("VAL3927_13_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["components"], component_rows(timestamp))
    write_csv(OUTPUTS["inputs"], input_rows(timestamp))
    write_csv(OUTPUTS["runner"], runner_rows(timestamp))
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
        raise SystemExit(f"3927 validation failed: {failed}")
    print(f"3927 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
