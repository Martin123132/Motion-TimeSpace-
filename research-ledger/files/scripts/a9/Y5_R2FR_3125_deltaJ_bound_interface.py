from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3125_DELTAJ_BOUND_INTERFACE_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3125_DELTAJ_BOUND_INTERFACE_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3125_VALIDATION.csv"
GATE = OUT / "P8_Y5_R2FR_3125_BOUND_INTERFACE_GATE.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    root_candidate = ROOT / path_text
    if root_candidate.exists():
        return root_candidate
    return OUT / path_text


def find_row(rows: list[dict[str, str]], row_id: str, row_id_column: str = "") -> dict[str, str] | None:
    if not row_id:
        return None
    if row_id_column:
        for row in rows:
            if row.get(row_id_column, "") == row_id:
                return row
    for row in rows:
        if row_id in row.values():
            return row
    return None


def source_row(input_row: dict[str, str]) -> tuple[dict[str, str] | None, Path]:
    path = source_path(input_row.get("source_file", ""))
    row = find_row(read_csv(path), input_row.get("source_row_id", ""), input_row.get("row_id_column", ""))
    return row, path


def nonclaim_markers(*values: object) -> list[str]:
    text = ";".join(str(value) for value in values)
    markers = []
    for marker in (
        "MISSING",
        "SMOKE",
        "NOT_CLAIM",
        "INPUT_VALID_FOR_CLAIM_FALSE",
        "requires",
        "REQUIRES",
        "not_numeric",
        "formula_not_numeric",
    ):
        if marker in text and marker not in markers:
            markers.append(marker)
    return markers


def selected_branch(rows: list[dict[str, str]]) -> tuple[str, bool, str]:
    branch_inputs = [row for row in rows if row.get("lane") == "branch_selection"]
    if not branch_inputs:
        return "", False, "missing_branch_selection_input"
    source, path = source_row(branch_inputs[0])
    if source is None:
        return "", False, f"branch_source_row_missing:{path}"
    branch = source.get("branch", "")
    selected = is_true(source.get("selected_default", ""))
    return branch, selected and branch == branch_inputs[0].get("required_branch", ""), str(path)


def evaluate_row(input_row: dict[str, str], selected: str, branch_ok: bool) -> dict[str, Any]:
    source, path = source_row(input_row)
    issues: list[str] = []
    if not path.exists():
        issues.append("SOURCE_FILE_MISSING")
    if source is None:
        issues.append("SOURCE_ROW_MISSING")

    bound_column = input_row.get("bound_column", "")
    bound_value = ""
    source_units = ""
    source_claim_allowed = ""
    source_valid_for_claim = ""
    source_issues = ""
    if source is not None:
        if bound_column in source:
            bound_value = source.get(bound_column, "")
        else:
            issues.append("BOUND_COLUMN_MISSING")
        source_units = source.get("source_bound_units", source.get("eta_units", source.get("units", "")))
        source_claim_allowed = source.get("claim_allowed", "")
        source_valid_for_claim = source.get("valid_for_claim", "")
        source_issues = source.get("issues", "")

    numeric_bound = parse_float(bound_value)
    units_expected = input_row.get("bound_units_expected", "")
    include = is_true(input_row.get("include_in_strict_rollup", ""))
    if input_row.get("lane") != "branch_selection" and not branch_ok:
        issues.append("REQUIRED_BRANCH_NOT_SELECTED")
    if include and numeric_bound is None:
        issues.append("INCLUDED_BOUND_NOT_NUMERIC")
    if include and units_expected != "dimensionless":
        issues.append("INCLUDED_BOUND_NOT_DIMENSIONLESS")
    if include and numeric_bound is not None and numeric_bound <= 0:
        issues.append("INCLUDED_BOUND_NOT_POSITIVE")
    if not is_true(input_row.get("valid_for_claim", "")):
        issues.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if source_valid_for_claim and not is_true(source_valid_for_claim):
        issues.append("SOURCE_VALID_FOR_CLAIM_FALSE")
    issues.extend(nonclaim_markers(input_row.get("projection_status", ""), source_issues, bound_value, source_valid_for_claim))
    issues = list(dict.fromkeys(issue for issue in issues if issue))

    usable_for_rollup = include and branch_ok and numeric_bound is not None and numeric_bound > 0 and units_expected == "dimensionless"
    claim_allowed = usable_for_rollup and not issues and is_true(input_row.get("valid_for_claim", "")) and is_true(source_valid_for_claim)
    return {
        "interface_id": input_row.get("interface_id", ""),
        "lane": input_row.get("lane", ""),
        "selected_branch": selected,
        "branch_ok": str(branch_ok).lower(),
        "source_file_resolved": str(path),
        "source_row_id": input_row.get("source_row_id", ""),
        "source_row_found": str(source is not None).lower(),
        "bound_column": bound_column,
        "bound_value": bound_value,
        "bound_units_expected": units_expected,
        "source_units": source_units,
        "numeric_bound_abs": numeric_bound if numeric_bound is not None else "",
        "include_in_strict_rollup": str(include).lower(),
        "usable_for_rollup": str(usable_for_rollup).lower(),
        "projection_status": input_row.get("projection_status", ""),
        "source_claim_allowed": source_claim_allowed,
        "source_valid_for_claim": source_valid_for_claim,
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "issues": ";".join(issues),
        "required_inputs": input_row.get("required_inputs", ""),
        "notes": input_row.get("notes", ""),
        "generated_utc": stamp(),
    }


def rollup_row(outputs: list[dict[str, Any]], selected: str, branch_ok: bool) -> dict[str, Any]:
    usable = [
        row
        for row in outputs
        if is_true(row.get("usable_for_rollup", ""))
        and parse_float(row.get("numeric_bound_abs", "")) is not None
    ]
    bound_values = [parse_float(row.get("numeric_bound_abs", "")) for row in usable]
    finite = [value for value in bound_values if value is not None and value > 0]
    strictest = min(finite) if finite else None
    source_ids = ";".join(row.get("interface_id", "") for row in usable)
    issues = []
    if not branch_ok:
        issues.append("REQUIRED_BRANCH_NOT_SELECTED")
    if strictest is None:
        issues.append("NO_FINITE_STRICT_ROLLUP_BOUND")
    if any(not is_true(row.get("claim_allowed", "")) for row in usable):
        issues.append("ROLLUP_INPUTS_NONCLAIM")
    return {
        "interface_id": "ROLL3125_STRICT_NONCLAIM",
        "lane": "strict_rollup",
        "selected_branch": selected,
        "branch_ok": str(branch_ok).lower(),
        "source_file_resolved": ";".join(row.get("source_file_resolved", "") for row in usable),
        "source_row_id": source_ids,
        "source_row_found": str(bool(usable)).lower(),
        "bound_column": "min(deltaJ_bound_abs)",
        "bound_value": strictest if strictest is not None else "",
        "bound_units_expected": "dimensionless",
        "source_units": "dimensionless",
        "numeric_bound_abs": strictest if strictest is not None else "",
        "include_in_strict_rollup": "false",
        "usable_for_rollup": str(strictest is not None).lower(),
        "projection_status": "strictest_available_nonclaim_deltaJ_bound",
        "source_claim_allowed": "false",
        "source_valid_for_claim": "false",
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "issues": ";".join(issues),
        "required_inputs": "replace smoke C_J tensor with parent-owned material/source/current coefficients before claim",
        "notes": "Strictest finite bound interface only; not evidence of a local-GR/R10/source-GM pass.",
        "generated_utc": stamp(),
    }


def validate(inputs: list[dict[str, str]], outputs: list[dict[str, Any]], selected: str, branch_ok: bool) -> list[dict[str, Any]]:
    required = [
        "interface_id",
        "lane",
        "source_file",
        "source_row_id",
        "row_id_column",
        "bound_column",
        "bound_units_expected",
        "include_in_strict_rollup",
        "projection_status",
        "required_branch",
        "required_inputs",
        "valid_for_claim",
    ]
    columns = set(inputs[0].keys()) if inputs else set()
    missing_columns = [column for column in required if column not in columns]
    source_status = {
        row.get("interface_id", ""): Path(row.get("source_file_resolved", "")).exists()
        for row in outputs
        if row.get("interface_id") != "ROLL3125_STRICT_NONCLAIM"
    }
    rollups = [row for row in outputs if row.get("interface_id") == "ROLL3125_STRICT_NONCLAIM"]
    rollup_bound = parse_float(rollups[0].get("numeric_bound_abs", "")) if rollups else None
    source_gm_claims = [
        row for row in outputs
        if row.get("lane") in {"source_GM_static", "Gdot_time_profile", "R10_product", "readout_guard", "calibration_guard"}
        and is_true(row.get("claim_allowed", ""))
    ]
    validations: list[dict[str, Any]] = [
        {
            "check_id": "VAL3125_0_input_schema",
            "status": "pass" if inputs and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3125_1_source_paths_resolve",
            "status": "pass" if source_status and all(source_status.values()) else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3125_2_before_variation_branch_selected",
            "status": "pass" if branch_ok and selected == "FINITE_BEFORE_VARIATION_PROJECTS_BOTH" else "fail",
            "details": selected,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3125_3_wep_CJ_bound_numeric",
            "status": "pass" if any(row.get("interface_id") == "DBI3125_1" and parse_float(row.get("numeric_bound_abs", "")) is not None for row in outputs) else "fail",
            "details": json.dumps([row for row in outputs if row.get("interface_id") == "DBI3125_1"], sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3125_4_exactly_one_finite_nonclaim_rollup",
            "status": "pass" if len(rollups) == 1 and rollup_bound is not None and rollup_bound > 0 and not is_true(rollups[0].get("claim_allowed", "")) else "fail",
            "details": json.dumps(rollups, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3125_5_non_WEP_lanes_do_not_claim_direct_deltaJ_bound",
            "status": "pass" if not source_gm_claims else "fail",
            "details": json.dumps(source_gm_claims, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3125_6_all_outputs_nonclaim",
            "status": "pass" if outputs and all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return validations


def gate_rows(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row.get("interface_id", ""): row for row in outputs}
    rollup = by_id.get("ROLL3125_STRICT_NONCLAIM", {})
    wep = by_id.get("DBI3125_1", {})
    source_gm = by_id.get("DBI3125_2", {})
    gdot = by_id.get("DBI3125_3", {})
    r10 = by_id.get("DBI3125_4", {})
    readout = by_id.get("DBI3125_5", {})
    calibration = by_id.get("DBI3125_6", {})
    return [
        {
            "row_id": "DBIG3125_0",
            "gate": "selected_before_variation_branch",
            "status": "finite_before_variation_selected_nonclaim" if is_true(rollup.get("branch_ok", "")) else "blocked_wrong_branch",
            "claim_allowed": "false",
            "theorem_or_failure": "3124 selects FINITE_BEFORE_VARIATION_PROJECTS_BOTH, so finite current insertion must be bounded rather than hidden inside calibration.",
            "observable_links": "WEP;source_GM;R10;EM_stress",
            "next_action": "use strict nonclaim bound interface until no-cA/current-owner proof closes",
            "source_paths": by_id.get("DBI3125_0", {}).get("source_file_resolved", ""),
        },
        {
            "row_id": "DBIG3125_1",
            "gate": "WEP_material_CJ_deltaJ_bound",
            "status": "finite_nonclaim_bound_available",
            "claim_allowed": "false",
            "theorem_or_failure": f"One-channel no-cancellation smoke gives |delta_J| <= {wep.get('numeric_bound_abs', '')}; input remains nonclaim because the parent material tensor/source current map is not signed.",
            "observable_links": "WEP;material_Coulomb;delta_J",
            "next_action": "replace tau_EM=1,C_relax=0 Coulomb smoke with parent-owned material/source coefficient tensor",
            "source_paths": wep.get("source_file_resolved", ""),
        },
        {
            "row_id": "DBIG3125_2",
            "gate": "source_GM_bridge",
            "status": "blocked_missing_source_and_calibration_kernels",
            "claim_allowed": "false",
            "theorem_or_failure": "The bridge Delta(GM)/GM=[C_J,S^ADM-C_J,cal^ADM]delta_J is derived, but C_J,S^ADM and C_J,cal^ADM are not filled.",
            "observable_links": "Newtonian_GM;local_GR;orbital",
            "next_action": "derive or source tau_EM_source, f_EM_ADM_source, C_relax_source and calibration reference",
            "source_paths": source_gm.get("source_file_resolved", ""),
        },
        {
            "row_id": "DBIG3125_3",
            "gate": "Gdot_time_profile_guard",
            "status": "blocked_derivative_not_absolute_deltaJ_bound",
            "claim_allowed": "false",
            "theorem_or_failure": f"Gdot row carries {gdot.get('bound_value', '')} {gdot.get('source_units', '')}, but this constrains a time profile, not absolute delta_J without kernels.",
            "observable_links": "Gdot;orbital;time_profile",
            "next_action": "derive time-profile map d(delta_J)/dt and source/calibration time kernels before scoring",
            "source_paths": gdot.get("source_file_resolved", ""),
        },
        {
            "row_id": "DBIG3125_4",
            "gate": "R10_product_guard",
            "status": "blocked_missing_R10_product_inputs",
            "claim_allowed": "false",
            "theorem_or_failure": "R10 needs K_X^R10(lambda), beta_s_J, beta_t_J, epsilon_tail_J and valid alpha_bound(lambda); current row is formula-only.",
            "observable_links": "R10;short_range;alpha_lambda",
            "next_action": "either prove current-owner zero or fill source/test current product coefficients with a real bound curve",
            "source_paths": r10.get("source_file_resolved", ""),
        },
        {
            "row_id": "DBIG3125_5",
            "gate": "readout_and_calibration_separation",
            "status": "guards_retained_not_scored_as_source_GM",
            "claim_allowed": "false",
            "theorem_or_failure": "Calibration-only and readout-only branches are explicitly separated from before-variation source coupling.",
            "observable_links": "readout;calibration;WEP;R10",
            "next_action": "do not convert universal current-unit shifts or post-variation readouts into source-GM evidence",
            "source_paths": f"{readout.get('source_file_resolved', '')};{calibration.get('source_file_resolved', '')}",
        },
        {
            "row_id": "DBIG3125_6",
            "gate": "next_target_3126",
            "status": "queued_private_derivation",
            "claim_allowed": "false",
            "theorem_or_failure": "The useful leap is now clear: derive the parent material/source current coefficient tensor or close no-cA/current-owner zero.",
            "observable_links": "delta_J;GR_reduction;Newtonian_GM;EM_stress",
            "next_action": "3126 should target parent-owned C_J tensor/source-current map rather than another missing-input ledger",
            "source_paths": OUTPUT,
        },
    ]


def main() -> None:
    inputs = read_csv(INPUT)
    selected, branch_ok, _branch_path = selected_branch(inputs)
    outputs = [evaluate_row(row, selected, branch_ok) for row in inputs]
    outputs.append(rollup_row(outputs, selected, branch_ok))
    validations = validate(inputs, outputs, selected, branch_ok)
    write_csv(OUTPUT, outputs)
    write_csv(VALIDATION, validations)
    write_csv(GATE, gate_rows(outputs))
    failing = [row for row in validations if row.get("status") != "pass"]
    if failing:
        raise SystemExit(f"3125 validation failed: {json.dumps(failing, sort_keys=True)}")
    print(f"wrote {OUTPUT}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {GATE}")


if __name__ == "__main__":
    main()
