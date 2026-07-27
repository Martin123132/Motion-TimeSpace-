from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_GK_STRESS_BOUND_DRY_RUN_AND_BASELINE_CONTROL_RUNNER_2564"
CHECKPOINT_ID = "2564"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2564-Y5-R2FR-GK-stress-bound-dry-run-and-baseline-control-runner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2564_SOURCE_REGISTER.csv",
    "dry_run_inputs": OUT / "P8_Y5_NO_SHADOW_2564_DRY_RUN_INPUTS.csv",
    "dry_run_results": OUT / "P8_Y5_NO_SHADOW_2564_DRY_RUN_RESULTS.csv",
    "rejection_ledger": OUT / "P8_Y5_NO_SHADOW_2564_REJECTION_LEDGER.csv",
    "baseline_control": OUT / "P8_Y5_NO_SHADOW_2564_BASELINE_CONTROL_LEDGER.csv",
    "toy_arithmetic": OUT / "P8_Y5_NO_SHADOW_2564_TOY_ARITHMETIC_SMOKE.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2564_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2564_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2564_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2564_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2564_VALIDATION.csv",
}

COPY_TARGETS = {
    "dry_run_results": LOCAL_BOUNDS / "GK_stress_bound_dry_run_results_2564_NONCLAIM.csv",
    "baseline_control": LOCAL_BOUNDS / "GK_stress_bound_baseline_control_2564_NONCLAIM.csv",
    "rejection_queue": QUEUE / "JR2564_GK_STRESS_BOUND_REJECTION_LEDGER_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2564_00_2563_doc",
        "source_path": ROOT / "2563-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
        "needles": ["NEXT2563_0_selected", "BASE2563_0_same_pipeline", "SCHEMA2563_4_block_rule", "VAL2563_OVERALL"],
        "role": "handoff selecting dry-run plus matched-baseline control runner",
    },
    {
        "source_id": "SRC2564_01_2563_schema",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2563_NONCLAIM_RUNNER_SCHEMA.csv",
        "needles": ["SCHEMA2563_2_baseline", "SCHEMA2563_4_block_rule", "MTS row cannot be interpreted unless baseline row also parses"],
        "role": "runner schema requiring baseline status and claim blocking",
    },
    {
        "source_id": "SRC2564_02_2563_arenas",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2563_ARENA_PROJECTION_ROWS.csv",
        "needles": ["ARENA2563_R10", "ARENA2563_PPN", "ARENA2563_LIGHT", "valid_for_claim=false"],
        "role": "local arena projection schema",
    },
    {
        "source_id": "SRC2564_03_2563_baseline_guardrails",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2563_BASELINE_COMPARISON_GUARDRAILS.csv",
        "needles": ["BASE2563_0_same_pipeline", "BASE2563_1_no_fitted_GM_shortcut", "BASE2563_5_data_blindness"],
        "role": "matched-baseline and anti-circularity guardrails",
    },
    {
        "source_id": "SRC2564_04_2563_missing_inputs",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2563_MISSING_INPUTS_LEDGER.csv",
        "needles": ["MISS2563_0_parent_signs", "MISS2563_8_arena_kernels", "MISS2563_10_baselines"],
        "role": "missing parent, kernel, bound-data and baseline inputs",
    },
    {
        "source_id": "SRC2564_05_2474_precedent",
        "source_path": ROOT / "2474-Y5-R2FR-GK-stress-bound-runner-dry-run-and-placeholder-rejection.md",
        "needles": ["DRY2474_1_PPN_toy_nonclaim", "FITTED_GM_FORBIDDEN", "VAL2474_OVERALL"],
        "role": "earlier placeholder rejection runner pattern upgraded with baseline controls",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append(
            {
                **base_row(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": exists,
                "missing_needles": ";".join(missing),
                "source_pass": exists and not missing,
                "role": source["role"],
            }
        )
    return rows


def dry_run_input_rows() -> list[dict[str, Any]]:
    doc_source = str(ROOT / "2563-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md")
    rows = [
        {
            "input_id": "DRY2564_0_R10_missing",
            "arena_id": "ARENA2563_R10",
            "arena": "R10_short_range",
            "E_GK_bound": "",
            "C_metric": "",
            "K_arena": "",
            "extra_leak": "",
            "arena_bound": "",
            "units": "alpha_bound",
            "source_path": "",
            "baseline_model": "Newton_GR_control",
            "baseline_residual": "0.0",
            "baseline_pipeline_status": "PASS",
            "baseline_data_convention": "same_alpha_lambda_parser",
            "valid_for_claim": "false",
            "parent_coefficients_sourced": "false",
            "arena_kernel_sourced": "false",
            "bound_data_sourced": "false",
            "forbidden_marker": "none",
            "input_status": "MISSING_COEFFICIENTS_AND_BOUND_DATA",
        },
        {
            "input_id": "DRY2564_1_PPN_toy_nonclaim",
            "arena_id": "ARENA2563_PPN",
            "arena": "PPN_solar_system",
            "E_GK_bound": "1.0e-12",
            "C_metric": "2.0",
            "K_arena": "3.0",
            "extra_leak": "0.0",
            "arena_bound": "1.0e-10",
            "units": "dimensionless",
            "source_path": "toy_internal",
            "baseline_model": "GR_PPN_zero_residual_control",
            "baseline_residual": "0.0",
            "baseline_pipeline_status": "PASS",
            "baseline_data_convention": "same_ppn_vector_convention",
            "valid_for_claim": "false",
            "parent_coefficients_sourced": "false",
            "arena_kernel_sourced": "false",
            "bound_data_sourced": "false",
            "forbidden_marker": "none",
            "input_status": "TOY_NUMERIC_NONCLAIM",
        },
        {
            "input_id": "DRY2564_2_CLOCK_bad_units",
            "arena_id": "ARENA2563_CLOCK",
            "arena": "clock_redshift_time",
            "E_GK_bound": "1.0e-12",
            "C_metric": "1.0",
            "K_arena": "1.0",
            "extra_leak": "1.0e-16",
            "arena_bound": "1.0e-15",
            "units": "banana_units",
            "source_path": "toy_internal",
            "baseline_model": "GR_clock_redshift_control",
            "baseline_residual": "0.0",
            "baseline_pipeline_status": "PASS",
            "baseline_data_convention": "same_clock_frequency_units",
            "valid_for_claim": "false",
            "parent_coefficients_sourced": "false",
            "arena_kernel_sourced": "false",
            "bound_data_sourced": "false",
            "forbidden_marker": "none",
            "input_status": "BAD_UNITS",
        },
        {
            "input_id": "DRY2564_3_ORBITAL_fitted_GM",
            "arena_id": "ARENA2563_ORBITAL",
            "arena": "orbital_dynamics",
            "E_GK_bound": "1.0e-13",
            "C_metric": "1.0",
            "K_arena": "1.0",
            "extra_leak": "0.0",
            "arena_bound": "1.0e-12",
            "units": "dimensionless",
            "source_path": "toy_internal",
            "baseline_model": "GR_orbital_control",
            "baseline_residual": "0.0",
            "baseline_pipeline_status": "PASS",
            "baseline_data_convention": "same_source_mass_policy",
            "valid_for_claim": "false",
            "parent_coefficients_sourced": "false",
            "arena_kernel_sourced": "false",
            "bound_data_sourced": "false",
            "forbidden_marker": "uses_fitted_GM",
            "input_status": "FITTED_GM_FORBIDDEN",
        },
        {
            "input_id": "DRY2564_4_WEP_missing_baseline",
            "arena_id": "ARENA2563_WEP",
            "arena": "WEP_composition",
            "E_GK_bound": "2.0e-15",
            "C_metric": "4.0",
            "K_arena": "5.0",
            "extra_leak": "0.0",
            "arena_bound": "1.0e-12",
            "units": "dimensionless",
            "source_path": "toy_internal",
            "baseline_model": "",
            "baseline_residual": "",
            "baseline_pipeline_status": "MISSING",
            "baseline_data_convention": "",
            "valid_for_claim": "false",
            "parent_coefficients_sourced": "false",
            "arena_kernel_sourced": "false",
            "bound_data_sourced": "false",
            "forbidden_marker": "none",
            "input_status": "MISSING_BASELINE_CONTROL",
        },
        {
            "input_id": "DRY2564_5_LIGHT_future_shape_missing_parent",
            "arena_id": "ARENA2563_LIGHT",
            "arena": "light_deflection_delay",
            "E_GK_bound": "5.0e-14",
            "C_metric": "1.5",
            "K_arena": "2.0",
            "extra_leak": "0.0",
            "arena_bound": "1.0e-10",
            "units": "dimensionless",
            "source_path": doc_source,
            "baseline_model": "GR_null_geodesic_control",
            "baseline_residual": "0.0",
            "baseline_pipeline_status": "PASS",
            "baseline_data_convention": "same_null_readout_kernel",
            "valid_for_claim": "true",
            "parent_coefficients_sourced": "false",
            "arena_kernel_sourced": "false",
            "bound_data_sourced": "false",
            "forbidden_marker": "none",
            "input_status": "FUTURE_SHAPE_BUT_PARENT_MISSING",
        },
    ]
    return [{**base_row(), **row, "claim_allowed": False} for row in rows]


def parse_float(value: str) -> float | None:
    if value == "":
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    if not math.isfinite(parsed) or parsed < 0:
        return None
    return parsed


def source_is_real(value: str) -> bool:
    if value in {"", "toy_internal", "future_source_required"}:
        return False
    return Path(value).exists()


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def baseline_reasons(row: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if row["baseline_pipeline_status"] != "PASS":
        reasons.append("BASELINE_NOT_PASS")
    if row["baseline_model"] == "":
        reasons.append("MISSING_BASELINE_MODEL")
    if row["baseline_data_convention"] == "":
        reasons.append("MISSING_BASELINE_CONVENTION")
    if parse_float(str(row["baseline_residual"])) is None:
        reasons.append("MISSING_OR_INVALID_BASELINE_RESIDUAL")
    return reasons


def evaluate_row(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]:
    allowed_units = {"dimensionless", "alpha_bound", "fractional_frequency", "radian_per_orbit", "angle", "range_fraction"}
    reasons: list[str] = []
    numeric_values = {field: parse_float(str(row[field])) for field in ["E_GK_bound", "C_metric", "K_arena", "extra_leak", "arena_bound"]}
    if any(value is None for value in numeric_values.values()):
        reasons.append("MISSING_OR_INVALID_NUMERIC_INPUT")
    if row["units"] not in allowed_units:
        reasons.append("BAD_UNITS")
    if not bool_text(row["valid_for_claim"]):
        reasons.append("VALID_FOR_CLAIM_FALSE")
    if not source_is_real(str(row["source_path"])):
        reasons.append("MISSING_REAL_SOURCE_PATH")
    if not bool_text(row["parent_coefficients_sourced"]):
        reasons.append("MISSING_PARENT_COEFFICIENTS")
    if not bool_text(row["arena_kernel_sourced"]):
        reasons.append("MISSING_ARENA_KERNEL")
    if not bool_text(row["bound_data_sourced"]):
        reasons.append("MISSING_BOUND_DATA")
    if row["forbidden_marker"] == "uses_fitted_GM":
        reasons.append("FITTED_GM_FORBIDDEN")
    reasons.extend(baseline_reasons(row))

    residual = None
    ratio = None
    baseline_delta = None
    if not any(reason in reasons for reason in ["MISSING_OR_INVALID_NUMERIC_INPUT", "BAD_UNITS"]):
        residual = numeric_values["E_GK_bound"] * numeric_values["C_metric"] * numeric_values["K_arena"] + numeric_values["extra_leak"]
        ratio = residual / numeric_values["arena_bound"] if numeric_values["arena_bound"] else None
        baseline_value = parse_float(str(row["baseline_residual"]))
        baseline_delta = None if baseline_value is None else residual - baseline_value

    result_status = "CLAIM_BLOCKED"
    if residual is not None and not bool_text(row["valid_for_claim"]):
        result_status = "COMPUTED_TOY_NONCLAIM"
    if residual is not None and bool_text(row["valid_for_claim"]) and reasons:
        result_status = "FUTURE_SHAPE_BLOCKED"
    if residual is not None and not reasons:
        result_status = "FUTURE_CLAIM_SHAPE_ONLY_BLOCKED_BY_DRY_RUN_POLICY"

    result = {
        **base_row(),
        "input_id": row["input_id"],
        "arena_id": row["arena_id"],
        "arena": row["arena"],
        "residual_predicted": "" if residual is None else f"{residual:.6e}",
        "baseline_residual": row["baseline_residual"],
        "delta_vs_baseline": "" if baseline_delta is None else f"{baseline_delta:.6e}",
        "ratio_to_bound": "" if ratio is None else f"{ratio:.6e}",
        "result_status": result_status,
        "block_reasons": ";".join(reasons),
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    baseline = {
        **base_row(),
        "input_id": row["input_id"],
        "arena": row["arena"],
        "baseline_model": row["baseline_model"],
        "baseline_pipeline_status": row["baseline_pipeline_status"],
        "baseline_data_convention": row["baseline_data_convention"],
        "baseline_residual": row["baseline_residual"],
        "baseline_control_status": "PASS_CONTROL" if not baseline_reasons(row) else "BLOCKED_CONTROL",
        "baseline_reasons": ";".join(baseline_reasons(row)),
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    rejection = None
    if reasons:
        rejection = {
            **base_row(),
            "input_id": row["input_id"],
            "arena": row["arena"],
            "rejection_reasons": ";".join(reasons),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    toy = None
    if residual is not None:
        toy = {
            **base_row(),
            "input_id": row["input_id"],
            "arena": row["arena"],
            "calculation": "residual_predicted=E_GK_bound*C_metric*K_arena+extra_leak",
            "numeric_result": f"{residual:.6e}",
            "baseline_delta": "" if baseline_delta is None else f"{baseline_delta:.6e}",
            "toy_only": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    return result, baseline, rejection, toy


def dry_run_outputs(inputs: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    baselines: list[dict[str, Any]] = []
    rejections: list[dict[str, Any]] = []
    toy_rows: list[dict[str, Any]] = []
    for row in inputs:
        result, baseline, rejection, toy = evaluate_row(row)
        results.append(result)
        baselines.append(baseline)
        if rejection:
            rejections.append(rejection)
        if toy:
            toy_rows.append(toy)
    return results, baselines, rejections, toy_rows


def claim_gate_rows(results: list[dict[str, Any]], baselines: list[dict[str, Any]], rejections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        ("GATE2564_0_dry_run", "Dry-run calculator executes.", "PASS", "result rows written", True, False),
        ("GATE2564_1_baseline_controls", "Matched baseline controls are evaluated.", "PASS", "baseline control ledger written", True, False),
        ("GATE2564_2_placeholder_rejection", "Placeholder/missing rows are rejected.", "PASS", f"{len(rejections)} rejection rows written", True, False),
        ("GATE2564_3_bad_units", "Bad units are rejected.", "PASS", "clock bad-unit row blocks", True, False),
        ("GATE2564_4_fitted_GM", "Fitted-GM contamination is rejected.", "PASS", "orbital fitted-GM row blocks", True, False),
        ("GATE2564_5_missing_baseline", "Missing baseline control blocks interpretation.", "PASS", "WEP missing-baseline row blocks", True, False),
        ("GATE2564_6_future_shape", "A valid-looking sourced row with missing parent coefficients remains blocked.", "PASS", "light row blocks on parent/kernel/bound inputs", True, False),
        ("GATE2564_7_claim_rows", "Any current row can support a local-test claim.", "BLOCKED", "all rows have claim_allowed=false and rejection reasons", False, False),
        ("GATE2564_8_local_GR", "local GR/PPN branch is derived.", "BLOCKED", "dry-run compatibility plumbing cannot replace parent no-hair proof", False, False),
        ("GATE2564_9_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private dry-run only", True, False),
    ]
    return [
        {
            **base_row(),
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": gate_status,
            "reason": reason,
            "gate_pass": gate_pass,
            "claim_allowed": claim_allowed,
        }
        for gate_id, claim, gate_status, reason, gate_pass, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2564_0_runner_works", "Keep the dry-run runner pattern.", "it computes toy rows and rejects all placeholder claim routes", "safe to receive real rows later"),
        ("DEC2564_1_baseline_required", "Keep matched GR/Newton controls as mandatory.", "without controls, pipeline failure can masquerade as theory failure", "fair-comparison discipline"),
        ("DEC2564_2_no_claim", "No local compatibility or local-GR claim.", "parent coefficients, kernels, bounds and real sources remain missing", "claim discipline retained"),
        ("DEC2564_3_next", "Acquire first real local bound/source row with baseline metadata, then separately reopen parent-coefficient derivation.", "the harness is ready but has no real inputs", "2565 selected"),
    ]
    return [
        {
            **base_row(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "effect": effect,
        }
        for decision_id, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2564_0_selected",
            "selection_status": "selected",
            "target_file": "2565-Y5-R2FR-first-real-local-bound-source-and-parent-coefficient-blocker.md",
            "target_script": "scripts/Y5_R2FR_first_real_local_bound_source_and_parent_coefficient_blocker_2565.py",
            "task": "source the first real local bound/control row for R10 or PPN with units and baseline metadata, while also recording that parent GK coefficients remain missing and no claim is allowed",
            "acceptance_target": "source acquisition ledger, candidate bound/control row or blocker, parent-coefficient blocker row, units validation, fitted-GM guardrail, claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["dry_run_results"], COPY_TARGETS["dry_run_results"])
    shutil.copyfile(OUTPUTS["baseline_control"], COPY_TARGETS["baseline_control"])
    shutil.copyfile(OUTPUTS["rejection_ledger"], COPY_TARGETS["rejection_queue"])
    source_map = {
        "dry_run_results": OUTPUTS["dry_run_results"],
        "baseline_control": OUTPUTS["baseline_control"],
        "rejection_queue": OUTPUTS["rejection_ledger"],
    }
    return [
        {
            **base_row(),
            "copy_id": copy_id,
            "source_path": str(source_map[copy_id]),
            "target_path": str(target),
            "source_exists": source_map[copy_id].exists(),
            "target_exists": target.exists(),
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    result_by_id = {row["input_id"]: row for row in data["results"]}
    rejection_text = {row["input_id"]: row["rejection_reasons"] for row in data["rejections"]}
    add("VAL2564_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and required needles are present")
    add("VAL2564_01_inputs_written", len(data["inputs"]) == 6, "six dry-run inputs written for R10, PPN, clocks, orbital, WEP and light")
    add("VAL2564_02_results_written", len(data["results"]) == len(data["inputs"]), "one dry-run result per input")
    add("VAL2564_03_all_nonclaim", all(row["claim_allowed"] is False or row["claim_allowed"] == "False" for row in data["results"]), "all result rows claim-blocked")
    add("VAL2564_04_rejections_written", len(data["rejections"]) == len(data["inputs"]), "every dry-run row has at least one rejection reason")
    add("VAL2564_05_baseline_controls", len(data["baselines"]) == len(data["inputs"]) and any(row["baseline_control_status"] == "BLOCKED_CONTROL" for row in data["baselines"]), "baseline control ledger includes pass and blocked controls")
    add("VAL2564_06_toy_arithmetic", len(data["toy"]) >= 4, "toy arithmetic computes where numeric inputs and units allow it")
    add("VAL2564_07_bad_units_rejected", "BAD_UNITS" in rejection_text.get("DRY2564_2_CLOCK_bad_units", ""), "bad-unit row rejected")
    add("VAL2564_08_fitted_GM_rejected", "FITTED_GM_FORBIDDEN" in rejection_text.get("DRY2564_3_ORBITAL_fitted_GM", ""), "fitted-GM row rejected")
    add("VAL2564_09_missing_baseline_rejected", "BASELINE_NOT_PASS" in rejection_text.get("DRY2564_4_WEP_missing_baseline", ""), "missing baseline row rejected")
    add("VAL2564_10_future_shape_blocked", "MISSING_PARENT_COEFFICIENTS" in rejection_text.get("DRY2564_5_LIGHT_future_shape_missing_parent", "") and result_by_id["DRY2564_5_LIGHT_future_shape_missing_parent"]["result_status"] == "FUTURE_SHAPE_BLOCKED", "valid-looking future row blocks on missing parent/kernel/bound inputs")
    add("VAL2564_11_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR or local compatibility claim")
    add("VAL2564_12_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2564_0_selected", "2565 source acquisition and parent blocker target selected")
    add("VAL2564_13_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2564-Y5", "P8_Y5_NO_SHADOW_2564", "P8_Y5_BRR545_2564", "JR2564")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2564_14_no_formalization_artifacts", not formal_hits, "no 2564 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2564_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2564_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2564_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2564_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2564_OVERALL", all(row["status"] == "PASS" for row in rows), "2564 dry-run runner computes toy residuals, checks matched baselines and blocks all claim routes")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2564 Y5 R2FR GK Stress-bound Dry-run And Baseline Control Runner",
        "",
        "**Status:** dry-run runner works and blocks claims. Toy rows compute where allowed, but every row remains nonclaim because at least one of parent coefficients, arena kernels, bound data, real source paths, units or matched baseline controls is missing.",
        "",
        "**Meaning:** the local stress-bound branch now has an executable harness with the fair-comparison rule baked in. If GR/Newton control rows are absent or broken, MTS rows cannot be interpreted; if toy MTS rows compute, they still cannot become evidence without real sourced inputs.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Dry-run Inputs",
        markdown_table(data["inputs"], ["input_id", "arena_id", "arena", "E_GK_bound", "C_metric", "K_arena", "extra_leak", "arena_bound", "units", "source_path", "baseline_model", "baseline_residual", "baseline_pipeline_status", "baseline_data_convention", "valid_for_claim", "parent_coefficients_sourced", "arena_kernel_sourced", "bound_data_sourced", "forbidden_marker", "input_status"]),
        "",
        "## Dry-run Results",
        markdown_table(data["results"], ["input_id", "arena_id", "arena", "residual_predicted", "baseline_residual", "delta_vs_baseline", "ratio_to_bound", "result_status", "block_reasons", "claim_allowed"]),
        "",
        "## Baseline Control Ledger",
        markdown_table(data["baselines"], ["input_id", "arena", "baseline_model", "baseline_pipeline_status", "baseline_data_convention", "baseline_residual", "baseline_control_status", "baseline_reasons", "claim_allowed"]),
        "",
        "## Rejection Ledger",
        markdown_table(data["rejections"], ["input_id", "arena", "rejection_reasons", "claim_allowed"]),
        "",
        "## Toy Arithmetic Smoke",
        markdown_table(data["toy"], ["input_id", "arena", "calculation", "numeric_result", "baseline_delta", "toy_only", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    inputs = dry_run_input_rows()
    results, baselines, rejections, toy = dry_run_outputs(inputs)
    data = {
        "sources": source_register_rows(),
        "inputs": inputs,
        "results": results,
        "baselines": baselines,
        "rejections": rejections,
        "toy": toy,
        "gates": claim_gate_rows(results, baselines, rejections),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["dry_run_inputs"], data["inputs"])
    write_csv(OUTPUTS["dry_run_results"], data["results"])
    write_csv(OUTPUTS["baseline_control"], data["baselines"])
    write_csv(OUTPUTS["rejection_ledger"], data["rejections"])
    write_csv(OUTPUTS["toy_arithmetic"], data["toy"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
