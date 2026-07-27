from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3470-Y5-R2FR-executable-coefficient-vector-runner-and-input-templates.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
ETA_TIPT_BOUND = 2.8e-15

SOURCES: dict[str, dict[str, Any]] = {
    "script_3470": {"type": "local", "path": Path(__file__).resolve(), "role": "generator and dry-run runner"},
    "doc_3469": {"type": "local", "path": ROOT / "3469-Y5-R2FR-visible-coefficient-owner-contract-or-multiarena-vector-runner.md", "role": "3469 handoff"},
    "next_3469": {"type": "local", "path": OUT / "P8_Y5_R2FR_3469_NEXT_TARGET.csv", "role": "3470 target statement"},
    "contract_3469": {"type": "local", "path": OUT / "P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv", "role": "visible coefficient owner contract"},
    "schema_3469": {"type": "local", "path": OUT / "P8_Y5_R2FR_3469_MULTIARENA_VECTOR_RUNNER_SCHEMA.csv", "role": "multi-arena schema"},
    "dryrun_3469": {"type": "local", "path": OUT / "P8_Y5_R2FR_3469_WEP_VECTOR_DRYRUN.csv", "role": "previous WEP dry-run"},
    "blockers_3469": {"type": "local", "path": OUT / "P8_Y5_R2FR_3469_BLOCKER_LEDGER.csv", "role": "previous blocker ledger"},
    "vector_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv", "role": "retained coefficient vector"},
    "envelope_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_NO_CANCELLATION_VECTOR_ENVELOPE.csv", "role": "no-cancellation envelope"},
    "alpha_bound_3465": {"type": "local", "path": OUT / "P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv", "role": "alpha WEP bound"},
    "mass_row_3466": {"type": "local", "path": OUT / "P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv", "role": "mass WEP bound"},
    "local_bounds": {"type": "local", "path": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv", "role": "empirical local bounds"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        values = [
            str(row.get(field, "")).replace("\n", "<br>").replace("|", "/")
            for field in fields
        ]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if "MISSING" in text or "FOLDED" in text or text in {"not_WEP_source_charge", "not_applicable"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    rows: list[dict[str, Any]] = []
    for source_id, meta in SOURCES.items():
        path = meta.get("path")
        rows.append({
            "timestamp_utc": stamp,
            "source_id": source_id,
            "source_type": meta["type"],
            "source_path": str(path) if path else "",
            "source_url": meta.get("url", ""),
            "exists_or_url_present": bool(path.exists()) if isinstance(path, Path) else bool(meta.get("url", "")),
            "role": meta["role"],
            "valid_for_claim": False,
        })
    return rows


def load_known_numbers() -> dict[str, float]:
    alpha_rows = read_csv(SOURCES["alpha_bound_3465"]["path"])
    mass_rows = read_csv(SOURCES["mass_row_3466"]["path"])
    return {
        "alpha_sensitivity": parse_float(next(row for row in alpha_rows if row["calc_id"] == "AOB3465_1_delta_Q_alpha")["value"]) or 0.0,
        "alpha_product_bound": parse_float(next(row for row in alpha_rows if row["calc_id"] == "AOB3465_2_D_e_bound")["value"]) or 0.0,
        "mhat_sensitivity": parse_float(next(row for row in mass_rows if row["component_id"] == "MASS3466_1_alloy_material_charge")["bound_or_value"]) or 0.0,
        "mhat_product_bound": parse_float(next(row for row in mass_rows if row["component_id"] == "MASS3466_2_alloy_single_channel_bound")["bound_or_value"]) or 0.0,
    }


def arena_config_template() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ARENA3470_0_WEP_TiPt",
            "arena": "WEP_MICROSCOPE_TiPt",
            "observable": "eta_TiPt_abs",
            "bound_abs": f"{ETA_TIPT_BOUND:.12e}",
            "bound_units": "dimensionless",
            "pass_rule": "all included live rows numeric or theorem_zero; absolute_sum <= bound_abs; no signed cancellation",
            "claim_policy": "valid_for_claim only if every live row has source path and no MISSING markers",
            "status": "EXECUTABLE_NOW_FOR_DRYRUN",
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA3470_1_CLOCKS",
            "arena": "CLOCKS_SPECTRA",
            "observable": "delta_ln_frequency",
            "bound_abs": "MISSING_CLOCK_BOUND",
            "bound_units": "dimensionless",
            "pass_rule": "schema hook only until clock sensitivity rows exist",
            "claim_policy": "blocked",
            "status": "HOOK_ONLY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA3470_2_R10",
            "arena": "R10_SHORT_RANGE",
            "observable": "alpha_lambda_prediction",
            "bound_abs": "MISSING_BOUND_CURVE_ROW_SELECTION",
            "bound_units": "dimensionless",
            "pass_rule": "schema hook only until MTS numerator and lambda row exist",
            "claim_policy": "blocked",
            "status": "HOOK_ONLY_NUMERATOR_MISSING",
            "valid_for_claim": False,
        },
    ]


def wep_input_template(numbers: dict[str, float]) -> list[dict[str, Any]]:
    vector_path = str(SOURCES["vector_3468"]["path"])
    return [
        {
            "input_id": "WVI3470_0_b_alpha",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "b_alpha",
            "component_role": "visible_alpha_product",
            "include_in_envelope": True,
            "theorem_zero": False,
            "sensitivity_abs": f"{numbers['alpha_sensitivity']:.12e}",
            "product_abs_bound": f"{numbers['alpha_product_bound']:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["alpha_bound_3465"]["path"]),
            "status": "NUMERIC_SINGLE_CHANNEL_BOUND",
            "missing_marker": "",
            "valid_for_claim": False,
        },
        {
            "input_id": "WVI3470_1_b_mhat",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "b_mhat",
            "component_role": "visible_mass_ratio_product",
            "include_in_envelope": True,
            "theorem_zero": False,
            "sensitivity_abs": f"{numbers['mhat_sensitivity']:.12e}",
            "product_abs_bound": f"{numbers['mhat_product_bound']:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["mass_row_3466"]["path"]),
            "status": "NUMERIC_SINGLE_CHANNEL_BOUND",
            "missing_marker": "",
            "valid_for_claim": False,
        },
        {
            "input_id": "WVI3470_2_b_me",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "b_me",
            "component_role": "electron_mass_or_yukawa_product",
            "include_in_envelope": True,
            "theorem_zero": False,
            "sensitivity_abs": "MISSING_DELTA_Q_ME_TIPT",
            "product_abs_bound": "MISSING_D_ME_EFF_BOUND",
            "units": "dimensionless",
            "source_path": vector_path,
            "status": "MISSING_LIVE_COMPONENT",
            "missing_marker": "MISSING_DELTA_Q_ME_TIPT;MISSING_D_ME_EFF_BOUND",
            "valid_for_claim": False,
        },
        {
            "input_id": "WVI3470_3_b_bind",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "b_bind",
            "component_role": "nuclear_binding_product",
            "include_in_envelope": True,
            "theorem_zero": False,
            "sensitivity_abs": "MISSING_EXACT_BINDING_TENSOR",
            "product_abs_bound": "FOLDED_ONLY_IN_PROXY_MASS_CHANNEL",
            "units": "dimensionless",
            "source_path": vector_path,
            "status": "MISSING_OR_FOLDED_LIVE_COMPONENT",
            "missing_marker": "MISSING_EXACT_BINDING_TENSOR;MISSING_SEPARATE_D_BIND_EFF_BOUND",
            "valid_for_claim": False,
        },
        {
            "input_id": "WVI3470_4_b_readout",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "b_readout",
            "component_role": "readout_radiative_product",
            "include_in_envelope": True,
            "theorem_zero": False,
            "sensitivity_abs": "MISSING_READOUT_SENSITIVITY",
            "product_abs_bound": "MISSING_D_READOUT_EFF_BOUND",
            "units": "dimensionless",
            "source_path": vector_path,
            "status": "MISSING_LIVE_COMPONENT",
            "missing_marker": "MISSING_READOUT_SENSITIVITY;MISSING_D_READOUT_EFF_BOUND",
            "valid_for_claim": False,
        },
        {
            "input_id": "WVI3470_5_direct_shadow_projector",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "direct_shadow_projector",
            "component_role": "nonconstant_source_residual",
            "include_in_envelope": True,
            "theorem_zero": False,
            "sensitivity_abs": "1.0",
            "product_abs_bound": "MISSING_DIRECT_SHADOW_PROJECTOR_BOUND",
            "units": "dimensionless",
            "source_path": str(SOURCES["blockers_3469"]["path"]),
            "status": "MISSING_LIVE_COMPONENT",
            "missing_marker": "MISSING_DIRECT_SHADOW_PROJECTOR_BOUND",
            "valid_for_claim": False,
        },
        {
            "input_id": "WVI3470_6_b_common",
            "arena": "WEP_MICROSCOPE_TiPt",
            "symbol": "b_common",
            "component_role": "common_calibration_mode",
            "include_in_envelope": False,
            "theorem_zero": True,
            "sensitivity_abs": "0.0",
            "product_abs_bound": "0.0",
            "units": "dimensionless",
            "source_path": str(SOURCES["contract_3469"]["path"]),
            "status": "IGNORED_COMMON_MODE_NOT_WEP_NUMERATOR",
            "missing_marker": "",
            "valid_for_claim": False,
        },
    ]


def schema_hooks() -> list[dict[str, Any]]:
    return [
        {
            "hook_id": "HOOK3470_0_WEP",
            "arena": "WEP_MICROSCOPE_TiPt",
            "input_file": "P8_Y5_R2FR_3470_WEP_VECTOR_INPUT_TEMPLATE.csv",
            "runner_output": "P8_Y5_R2FR_3470_WEP_VECTOR_RUNNER_RESULTS.csv",
            "next_fill": "replace MISSING markers with sourced numeric sensitivity/product rows or theorem_zero=true",
            "status": "EXECUTABLE",
            "valid_for_claim": False,
        },
        {
            "hook_id": "HOOK3470_1_CLOCKS",
            "arena": "CLOCKS_SPECTRA",
            "input_file": "future_CLOCK_VECTOR_INPUT_TEMPLATE.csv",
            "runner_output": "future_CLOCK_VECTOR_RUNNER_RESULTS.csv",
            "next_fill": "clock sensitivity coefficients and clock bounds",
            "status": "SCHEMA_HOOK_ONLY",
            "valid_for_claim": False,
        },
        {
            "hook_id": "HOOK3470_2_R10",
            "arena": "R10_SHORT_RANGE",
            "input_file": "future_R10_ALPHA_NUMERATOR_INPUT_TEMPLATE.csv",
            "runner_output": "future_R10_ALPHA_RUNNER_RESULTS.csv",
            "next_fill": "lambda row, bound curve row, MTS alpha numerator/source-test normalization",
            "status": "SCHEMA_HOOK_ONLY",
            "valid_for_claim": False,
        },
    ]


def evaluate_wep_vector(input_rows: list[dict[str, Any]], arena_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    arena = next(row for row in arena_rows if row["arena"] == "WEP_MICROSCOPE_TiPt")
    bound = parse_float(arena["bound_abs"])
    if bound is None:
        raise ValueError("WEP bound is not numeric")

    results: list[dict[str, Any]] = []
    known_sum = 0.0
    blockers: list[str] = []
    included_live_rows = 0
    numeric_live_rows = 0
    zero_rows = 0

    for row in input_rows:
        include = parse_bool(row["include_in_envelope"])
        theorem_zero = parse_bool(row["theorem_zero"])
        symbol = row["symbol"]
        if not include:
            results.append({
                "result_id": f"WRR3470_{len(results)}_{symbol}",
                "symbol": symbol,
                "include_in_envelope": include,
                "theorem_zero": theorem_zero,
                "sensitivity_abs": row["sensitivity_abs"],
                "product_abs_bound": row["product_abs_bound"],
                "abs_contribution": "0.000000000000e+00",
                "row_status": "IGNORED_COMMON_MODE_OR_NOT_IN_WEP_NUMERATOR",
                "blocker": "",
                "source_path": row["source_path"],
                "valid_for_claim": False,
            })
            continue

        included_live_rows += 1
        if theorem_zero:
            zero_rows += 1
            results.append({
                "result_id": f"WRR3470_{len(results)}_{symbol}",
                "symbol": symbol,
                "include_in_envelope": include,
                "theorem_zero": theorem_zero,
                "sensitivity_abs": row["sensitivity_abs"],
                "product_abs_bound": row["product_abs_bound"],
                "abs_contribution": "0.000000000000e+00",
                "row_status": "THEOREM_ZERO",
                "blocker": "",
                "source_path": row["source_path"],
                "valid_for_claim": False,
            })
            continue

        sensitivity = parse_float(row["sensitivity_abs"])
        product = parse_float(row["product_abs_bound"])
        if sensitivity is None or product is None or row["missing_marker"]:
            blocker = row["missing_marker"] or "MISSING_NUMERIC_INPUT"
            blockers.append(f"{symbol}:{blocker}")
            results.append({
                "result_id": f"WRR3470_{len(results)}_{symbol}",
                "symbol": symbol,
                "include_in_envelope": include,
                "theorem_zero": theorem_zero,
                "sensitivity_abs": row["sensitivity_abs"],
                "product_abs_bound": row["product_abs_bound"],
                "abs_contribution": "MISSING",
                "row_status": "BLOCKING_MISSING_LIVE_INPUT",
                "blocker": blocker,
                "source_path": row["source_path"],
                "valid_for_claim": False,
            })
            continue

        numeric_live_rows += 1
        contribution = abs(sensitivity * product)
        known_sum += contribution
        results.append({
            "result_id": f"WRR3470_{len(results)}_{symbol}",
            "symbol": symbol,
            "include_in_envelope": include,
            "theorem_zero": theorem_zero,
            "sensitivity_abs": f"{sensitivity:.12e}",
            "product_abs_bound": f"{product:.12e}",
            "abs_contribution": f"{contribution:.12e}",
            "row_status": "NUMERIC_LIVE_COMPONENT",
            "blocker": "",
            "source_path": row["source_path"],
            "valid_for_claim": False,
        })

    fail_reasons: list[str] = []
    if blockers:
        fail_reasons.append("MISSING_LIVE_COMPONENTS")
    if known_sum > bound:
        fail_reasons.append("KNOWN_ABS_SUM_EXCEEDS_BOUND")
    if not fail_reasons:
        pass_status = "PASS_NONCLAIM_SCHEMA_ONLY"
    else:
        pass_status = "FAIL_BLOCKED_" + "_AND_".join(fail_reasons)

    results.append({
        "result_id": "WRR3470_SUMMARY",
        "symbol": "WEP_VECTOR_SUMMARY",
        "include_in_envelope": True,
        "theorem_zero": False,
        "sensitivity_abs": f"included_live_rows={included_live_rows};numeric_live_rows={numeric_live_rows};theorem_zero_rows={zero_rows}",
        "product_abs_bound": f"eta_bound={bound:.12e}",
        "abs_contribution": f"{known_sum:.12e}",
        "row_status": pass_status,
        "blocker": ";".join(blockers),
        "source_path": str(SOURCES["script_3470"]["path"]),
        "valid_for_claim": False,
    })
    return results


def refusal_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "REF3470_0_missing_live",
            "condition": "any included row has MISSING marker and theorem_zero=false",
            "runner_action": "fail blocked; do not claim",
            "valid_for_claim": False,
        },
        {
            "rule_id": "REF3470_1_known_sum_exceeds",
            "condition": "known absolute contribution sum exceeds arena bound",
            "runner_action": "fail blocked even before missing rows are filled",
            "valid_for_claim": False,
        },
        {
            "rule_id": "REF3470_2_no_cancellation",
            "condition": "signed cancellation is required for pass",
            "runner_action": "fail blocked; absolute envelope only",
            "valid_for_claim": False,
        },
        {
            "rule_id": "REF3470_3_common_mode",
            "condition": "row is common calibration mode",
            "runner_action": "exclude from WEP numerator but keep Newton/G guard",
            "valid_for_claim": False,
        },
    ]


def claim_gates(results: list[dict[str, Any]], input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = next(row for row in results if row["result_id"] == "WRR3470_SUMMARY")
    missing_count = sum(1 for row in results if row["row_status"] == "BLOCKING_MISSING_LIVE_INPUT")
    numeric_count = sum(1 for row in results if row["row_status"] == "NUMERIC_LIVE_COMPONENT")
    return [
        {
            "gate_id": "CG3470_0_templates_written",
            "gate": "WEP vector input and arena config templates exist",
            "pass": len(input_rows) >= 6,
            "detail": f"input_rows={len(input_rows)}",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3470_1_runner_executes",
            "gate": "runner evaluates numeric, missing and common-mode rows",
            "pass": True,
            "detail": f"numeric={numeric_count};missing={missing_count};summary={summary['row_status']}",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3470_2_WEP_pass",
            "gate": "WEP vector passes absolute envelope",
            "pass": summary["row_status"].startswith("PASS"),
            "detail": summary["row_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3470_3_multiarena_hooks",
            "gate": "clock and R10 hooks are present",
            "pass": True,
            "detail": "hooks written but input rows missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3470_4_local_GR_claim",
            "gate": "local GR/Newton/Maxwell source coupling derived",
            "pass": False,
            "detail": "blocked by WEP vector failure and missing clock/R10/local source rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = next(row for row in results if row["result_id"] == "WRR3470_SUMMARY")
    return [
        {
            "decision_id": "DEC3470_0_runner_progress",
            "decision": "Use the 3470 WEP vector runner as the reusable local-source discipline tool.",
            "reason": "It reads templates, computes absolute contributions, and refuses missing/cancellation passes.",
            "next_action": "Fill or zero the highest-pressure missing WEP rows.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3470_1_current_WEP_status",
            "decision": "Current WEP vector is blocked, not failed as a theory claim.",
            "reason": summary["row_status"],
            "next_action": "Either theorem-zero b_alpha/b_mhat via visible coefficient owner, or fill b_me/b_bind/readout/direct residual rows and lower the absolute sum.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3470_2_next",
            "decision": "Next best move is first missing-row fill: b_me/clock-material sensitivity or theorem-zero contract.",
            "reason": "The runner is now reusable; progress comes from filling rows or proving them zero.",
            "next_action": "3471 should target b_me and clock/material sensitivity, or derive no electron-mass coefficient from the visible coefficient owner contract.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [{
        "next_doc": "3471-Y5-R2FR-bme-clock-material-row-or-electron-mass-zero-theorem.md",
        "next_script": "scripts/Y5_R2FR_3471_bme_clock_material_row_or_electron_mass_zero_theorem.py",
        "objective": "Try to prove b_me=0 from the visible coefficient owner contract; if not, fill the first electron-mass/clock-material sensitivity row needed by the 3470 vector runner.",
        "success_gate": "Either b_me is theorem-zero, or WEP/clocks receive a sourced b_me sensitivity/product row that the 3470 runner can read.",
        "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; cancellation pass.",
        "claim_allowed": False,
        "valid_for_claim": False,
    }]


def validate(
    outputs: dict[str, Path],
    source_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    results: list[dict[str, Any]],
    hooks: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    stamp = now()
    local_sources_ok = all(row["exists_or_url_present"] for row in source_rows if row["source_type"] == "local")
    summary = next(row for row in results if row["result_id"] == "WRR3470_SUMMARY")
    missing_rows = [row for row in results if row["row_status"] == "BLOCKING_MISSING_LIVE_INPUT"]
    numeric_rows = [row for row in results if row["row_status"] == "NUMERIC_LIVE_COMPONENT"]
    known_sum = parse_float(summary["abs_contribution"]) or 0.0
    runner_blocks_correctly = (
        summary["row_status"] == "FAIL_BLOCKED_MISSING_LIVE_COMPONENTS_AND_KNOWN_ABS_SUM_EXCEEDS_BOUND"
        and known_sum > ETA_TIPT_BOUND
        and len(missing_rows) >= 3
        and len(numeric_rows) == 2
    )
    common_mode_ignored = any(row["symbol"] == "b_common" and not parse_bool(row["include_in_envelope"]) for row in input_rows)
    hooks_ok = {row["arena"] for row in hooks} >= {"WEP_MICROSCOPE_TiPt", "CLOCKS_SPECTRA", "R10_SHORT_RANGE"}
    templates_ok = len(input_rows) >= 7 and any(row["arena"] == "WEP_MICROSCOPE_TiPt" for row in arena_rows)
    local_gr_blocked = any(row["gate_id"] == "CG3470_4_local_GR_claim" and row["pass"] is False for row in gates)
    no_claim_rows = not any(
        str(value).lower() == "true"
        for rows in (input_rows, arena_rows, results, hooks, gates)
        for row in rows
        for key, value in row.items()
        if key in {"claim_allowed", "valid_for_claim"}
    )
    parse_counts: list[str] = []
    csv_parse_ok = True
    for label, path in outputs.items():
        if label == "validation":
            continue
        try:
            parse_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            parse_counts.append(f"{path.name}:ERROR:{exc}")
            csv_parse_ok = False
    formalization_ok = True
    formalization_detail = "formalization_exists=False"
    if FORMALIZATION.exists():
        matches = list(FORMALIZATION.rglob("*3470*"))
        formalization_ok = not matches
        formalization_detail = f"formalization_exists=True; 3470_outputs_in_formalization={len(matches)}"

    rows = [
        {"validation_id": "VAL3470_0_local_sources_exist", "pass": local_sources_ok, "detail": "all local sources exist", "timestamp_utc": stamp},
        {"validation_id": "VAL3470_1_templates_written", "pass": templates_ok, "detail": f"input_rows={len(input_rows)};arena_rows={len(arena_rows)}", "timestamp_utc": stamp},
        {"validation_id": "VAL3470_2_runner_blocks_correctly", "pass": runner_blocks_correctly, "detail": summary["row_status"], "timestamp_utc": stamp},
        {"validation_id": "VAL3470_3_common_mode_ignored", "pass": common_mode_ignored, "detail": "b_common excluded from WEP numerator", "timestamp_utc": stamp},
        {"validation_id": "VAL3470_4_hooks_present", "pass": hooks_ok, "detail": ";".join(sorted(row["arena"] for row in hooks)), "timestamp_utc": stamp},
        {"validation_id": "VAL3470_5_local_GR_claim_blocked", "pass": local_gr_blocked, "detail": "local source claim remains false", "timestamp_utc": stamp},
        {"validation_id": "VAL3470_6_no_claim_rows", "pass": no_claim_rows, "detail": "all claim_allowed and valid_for_claim flags remain false", "timestamp_utc": stamp},
        {"validation_id": "VAL3470_7_csv_parse", "pass": csv_parse_ok, "detail": ";".join(parse_counts), "timestamp_utc": stamp},
        {"validation_id": "VAL3470_8_formalization_untouched_by_3470", "pass": formalization_ok, "detail": formalization_detail, "timestamp_utc": stamp},
    ]
    rows.append({
        "validation_id": "VAL3470_SUMMARY",
        "pass": all(str(row["pass"]).lower() == "true" for row in rows),
        "detail": "PASS" if all(str(row["pass"]).lower() == "true" for row in rows) else "FAIL",
        "timestamp_utc": stamp,
    })
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    hooks: list[dict[str, Any]],
    results: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    summary = next(row for row in results if row["result_id"] == "WRR3470_SUMMARY")
    doc = f"""# 3470 - Executable Coefficient Vector Runner And Input Templates

**Current verdict:** the WEP-first coefficient-vector runner is now executable. It reads row templates, separates numeric, missing, theorem-zero and common-mode rows, and refuses both missing-input and cancellation-style passes.

**Concrete progress:** current dry-run result is `{summary['row_status']}` with known absolute contribution `{summary['abs_contribution']}` against `eta_bound=2.800000000000e-15`. This is exactly the discipline gate we needed: fill or prove rows, then rerun.

## Source Register
{md_table(source_rows)}

## Arena Config Template
{md_table(arena_rows)}

## WEP Vector Input Template
{md_table(input_rows)}

## Multi-Arena Schema Hooks
{md_table(hooks)}

## WEP Vector Runner Results
{md_table(results)}

## Runner Refusal Rules
{md_table(rules)}

## Claim Gates
{md_table(gates)}

## Decision Ledger
{md_table(decisions)}

## Validation
{md_table(validation_rows)}

## Next Target
{md_table(next_rows)}

## Short Readout
- Executable now: WEP vector dry-run.
- Numeric now: alpha and `b_mhat` one-channel rows.
- Blocking now: `b_me`, `b_bind`, `b_readout`, direct/shadow/projector, plus known absolute sum already above the bound.
- Next move: fill or theorem-zero the first missing live row, probably `b_me`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    numbers = load_known_numbers()
    source_rows = source_register()
    arena_rows = arena_config_template()
    input_rows = wep_input_template(numbers)
    hooks = schema_hooks()
    results = evaluate_wep_vector(input_rows, arena_rows)
    rules = refusal_rules()
    gates = claim_gates(results, input_rows)
    decisions = decision_ledger(results)
    next_rows = next_target()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3470_SOURCE_REGISTER.csv",
        "arena_config": OUT / "P8_Y5_R2FR_3470_ARENA_CONFIG_TEMPLATE.csv",
        "wep_inputs": OUT / "P8_Y5_R2FR_3470_WEP_VECTOR_INPUT_TEMPLATE.csv",
        "hooks": OUT / "P8_Y5_R2FR_3470_MULTIARENA_SCHEMA_HOOKS.csv",
        "wep_results": OUT / "P8_Y5_R2FR_3470_WEP_VECTOR_RUNNER_RESULTS.csv",
        "refusal": OUT / "P8_Y5_R2FR_3470_RUNNER_REFUSAL_RULES.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3470_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3470_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3470_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3470_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["arena_config"], arena_rows)
    write_csv(outputs["wep_inputs"], input_rows)
    write_csv(outputs["hooks"], hooks)
    write_csv(outputs["wep_results"], results)
    write_csv(outputs["refusal"], rules)
    write_csv(outputs["claim_gates"], gates)
    write_csv(outputs["decision"], decisions)
    write_csv(outputs["next"], next_rows)
    validation_rows = validate(outputs, source_rows, input_rows, arena_rows, results, hooks, gates)
    write_csv(outputs["validation"], validation_rows)
    write_doc(source_rows, arena_rows, input_rows, hooks, results, rules, gates, decisions, validation_rows, next_rows)

    summary = next(row for row in validation_rows if row["validation_id"] == "VAL3470_SUMMARY")
    print(summary["detail"])
    print(DOC)


if __name__ == "__main__":
    main()
