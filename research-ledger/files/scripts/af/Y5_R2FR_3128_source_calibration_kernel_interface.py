from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3128_SOURCE_CAL_KERNEL_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3128_SOURCE_CAL_KERNEL_INTERFACE_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3128_VALIDATION.csv"
GATE = OUT / "P8_Y5_R2FR_3128_SOURCE_CAL_KERNEL_GATE.csv"


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


def close(left: float | None, right: float | None, tol: float = 1e-24) -> bool:
    if left is None or right is None:
        return False
    return abs(left - right) <= max(tol, 1e-12 * max(abs(left), abs(right), 1.0))


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


def load_sources(inputs: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for row in inputs:
        path = source_path(row.get("source_file", ""))
        source = find_row(read_csv(path), row.get("source_row_id", ""), row.get("row_id_column", ""))
        sources[row.get("role", "")] = {
            "input": row,
            "path": path,
            "row": source,
            "exists": path.exists(),
            "found": source is not None,
        }
    return sources


def local_bound_path(sources: dict[str, dict[str, Any]]) -> Path:
    return sources["local_bounds"]["path"]


def local_bound_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    return read_csv(local_bound_path(sources))


def delta_j_bound(sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get("deltaJ_bound", {}).get("row") or {}
    return parse_float(row.get("numeric_bound_abs", ""))


def wep_delta_cj(sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get("WEP_delta_CJ", {}).get("row") or {}
    value = parse_float(row.get("delta_C_J", ""))
    return abs(value) if value is not None else None


def bound_row(rows: list[dict[str, str]], row_id: str) -> dict[str, str] | None:
    return find_row(rows, row_id, "row_id")


def dimensionless_kernel_row(
    kernel_id: str,
    arena: str,
    row: dict[str, str],
    delta_bound: float,
    projection_assumption: str,
    source_paths: str,
) -> dict[str, Any]:
    upper = parse_float(row.get("upper_bound", ""))
    kernel_max = upper / delta_bound if upper is not None and delta_bound > 0 else None
    issues = ["UNIT_PROJECTION_SENSITIVITY_NOT_CLAIM", "SOURCE_CALIBRATION_KERNEL_UNFILLED"]
    if upper is None:
        issues.append("BOUND_NOT_NUMERIC")
    return {
        "kernel_id": kernel_id,
        "arena": arena,
        "observable": row.get("observable", ""),
        "source_bound_value": upper if upper is not None else row.get("upper_bound", ""),
        "source_bound_units": row.get("units", ""),
        "deltaJ_bound_abs": delta_bound,
        "projection_assumption": projection_assumption,
        "kernel_abs_max_if_static_unit_projection": kernel_max if kernel_max is not None else "",
        "kernel_formula": "abs(DeltaC_Scal * delta_J) <= bound, with DeltaC_Scal=C_J,S^ADM-C_J,cal^ADM",
        "score": "sensitivity_only_nonclaim" if kernel_max is not None else "not_scoreable",
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "issues": ";".join(issues),
        "next_action": "fill actual projection coefficient and source-calibration kernel before scoring",
        "source_paths": source_paths,
        "generated_utc": stamp(),
    }


def gdot_row(row: dict[str, str], delta_bound: float, source_paths: str) -> dict[str, Any]:
    return {
        "kernel_id": "SCK3128_4",
        "arena": "Gdot_time_profile",
        "observable": row.get("observable", ""),
        "source_bound_value": row.get("upper_bound", ""),
        "source_bound_units": row.get("units", ""),
        "deltaJ_bound_abs": delta_bound,
        "projection_assumption": "time-profile branch, not static absolute delta_J",
        "kernel_abs_max_if_static_unit_projection": "",
        "kernel_formula": "abs(DeltaC_Scal*d(delta_J)/dt + d(DeltaC_Scal)/dt*delta_J) <= Gdot/G",
        "score": "not_scoreable_time_profile_required",
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "issues": "TIME_PROFILE_REQUIRED;SOURCE_CALIBRATION_TIME_KERNEL_UNFILLED;DO_NOT_CONVERT_TO_STATIC_DELTAJ_BOUND",
        "next_action": "derive d(delta_J)/dt and d(DeltaC_Scal)/dt before using Gdot",
        "source_paths": source_paths,
        "generated_utc": stamp(),
    }


def output_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    delta_bound = delta_j_bound(sources)
    if delta_bound is None:
        delta_bound = float("nan")
    rows = local_bound_rows(sources)
    paths = lambda *roles: ";".join(str(sources[role]["path"]) for role in roles)
    wep_row = bound_row(rows, "R0_identity_coframe_direct") or {}
    clock_row = bound_row(rows, "R2_clock_redshift") or {}
    gamma_row = bound_row(rows, "R3_gamma") or {}
    beta_row = bound_row(rows, "R4_beta") or {}
    gdot_bound_row = bound_row(rows, "R9_Gdot") or {}
    wep_kernel = dimensionless_kernel_row(
        "SCK3128_0",
        "WEP_material_anchor",
        wep_row,
        delta_bound,
        "eta_AB=abs(DeltaC_AB*delta_J)",
        paths("local_bounds", "deltaJ_bound", "WEP_delta_CJ"),
    )
    wep_kernel["known_delta_CJ_abs_from_3122"] = wep_delta_cj(sources) or ""
    wep_kernel["reproduces_3122_delta_CJ"] = str(close(parse_float(wep_kernel["kernel_abs_max_if_static_unit_projection"]), wep_delta_cj(sources))).lower()
    return [
        {
            "kernel_id": "SCK3128_PRE",
            "arena": "source_calibration_kernel_definition",
            "observable": "DeltaGM_J/GM",
            "source_bound_value": "",
            "source_bound_units": "dimensionless",
            "deltaJ_bound_abs": delta_bound,
            "projection_assumption": "Hilbert-stress source and calibration use the same ADM slice/reference convention",
            "kernel_abs_max_if_static_unit_projection": "",
            "kernel_formula": "DeltaC_Scal=C_J,S^ADM-C_J,cal^ADM=f_EM,S sum_AB w_AB^S K_AB + C_relax,S - C_J,cal^ADM",
            "score": "definition_only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "SOURCE_WEIGHTS_UNFILLED;CALIBRATION_KERNEL_UNFILLED;PARENT_SLOT_UNSIGNED",
            "next_action": "fill source/calibration weights or prove c_A/Z_Q slots vanish",
            "source_paths": paths("Hilbert_weight_measure", "source_GM_bridge"),
            "generated_utc": stamp(),
        },
        wep_kernel,
        dimensionless_kernel_row(
            "SCK3128_1",
            "clock_redshift_unit_projection",
            clock_row,
            delta_bound,
            "unit clock projection placeholder; not a derived PPN/readout coefficient",
            paths("local_bounds", "deltaJ_bound", "Hilbert_weight_measure"),
        ),
        dimensionless_kernel_row(
            "SCK3128_2",
            "PPN_gamma_unit_projection",
            gamma_row,
            delta_bound,
            "unit gamma projection placeholder; K_gamma not derived",
            paths("local_bounds", "deltaJ_bound", "source_GM_bridge"),
        ),
        dimensionless_kernel_row(
            "SCK3128_3",
            "PPN_beta_unit_projection",
            beta_row,
            delta_bound,
            "unit beta projection placeholder; K_beta not derived",
            paths("local_bounds", "deltaJ_bound", "source_GM_bridge"),
        ),
        gdot_row(gdot_bound_row, delta_bound, paths("local_bounds", "deltaJ_bound", "Poynting_guard")),
        {
            "kernel_id": "SCK3128_NEXT",
            "arena": "next_decision",
            "observable": "source_calibration_fill_or_zero",
            "source_bound_value": "",
            "source_bound_units": "n/a",
            "deltaJ_bound_abs": delta_bound,
            "projection_assumption": "nonclaim interface",
            "kernel_abs_max_if_static_unit_projection": "",
            "kernel_formula": "Either fill DeltaC_Scal from Hilbert-stress source/calibration weights or prove DeltaC_Scal=0 by parent grammar/calibration.",
            "score": "route_selector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "NEXT_ROUTE_REQUIRED",
            "next_action": "derive first real source/calibration row for Sun/Earth/lab or attack zero proof",
            "source_paths": paths("Hilbert_weight_measure", "Poynting_guard", "source_GM_bridge"),
            "generated_utc": stamp(),
        },
    ]


def validate(inputs: list[dict[str, str]], sources: dict[str, dict[str, Any]], outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = ["source_id", "role", "source_file", "source_row_id", "row_id_column", "required", "valid_for_claim", "notes"]
    columns = set(inputs[0].keys()) if inputs else set()
    missing_columns = [column for column in required if column not in columns]
    source_status = {
        role: {"exists": payload["exists"], "found": payload["found"], "path": str(payload["path"])}
        for role, payload in sources.items()
    }
    delta_bound = delta_j_bound(sources)
    wep = [row for row in outputs if row.get("kernel_id") == "SCK3128_0"]
    gdot = [row for row in outputs if row.get("kernel_id") == "SCK3128_4"]
    dimensionless = [
        row for row in outputs
        if row.get("kernel_id") in {"SCK3128_0", "SCK3128_1", "SCK3128_2", "SCK3128_3"}
    ]
    return [
        {
            "check_id": "VAL3128_0_input_schema",
            "status": "pass" if inputs and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3128_1_required_source_rows_resolve",
            "status": "pass" if all(payload["exists"] and payload["found"] for payload in sources.values()) else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3128_2_deltaJ_bound_positive",
            "status": "pass" if delta_bound is not None and delta_bound > 0 else "fail",
            "details": str(delta_bound),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3128_3_WEP_kernel_threshold_reproduces_3122_deltaC",
            "status": "pass" if wep and is_true(wep[0].get("reproduces_3122_delta_CJ", "")) else "fail",
            "details": json.dumps(wep, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3128_4_dimensionless_sensitivity_rows_numeric",
            "status": "pass" if dimensionless and all(parse_float(row.get("kernel_abs_max_if_static_unit_projection", "")) is not None for row in dimensionless) else "fail",
            "details": json.dumps(dimensionless, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3128_5_Gdot_not_converted_to_static_bound",
            "status": "pass" if gdot and gdot[0].get("score") == "not_scoreable_time_profile_required" else "fail",
            "details": json.dumps(gdot, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3128_6_all_outputs_nonclaim",
            "status": "pass" if outputs and all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def gate_rows(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row.get("kernel_id", ""): row for row in outputs}
    return [
        {
            "row_id": "SCKG3128_0",
            "gate": "source_calibration_kernel_definition",
            "status": "DeltaC_Scal_interface_derived",
            "claim_allowed": "false",
            "theorem_or_failure": by_id.get("SCK3128_PRE", {}).get("kernel_formula", ""),
            "observable_links": "source_GM;Newtonian_limit;local_GR",
            "next_action": "fill source/calibration weights from Hilbert stress",
            "source_paths": by_id.get("SCK3128_PRE", {}).get("source_paths", ""),
        },
        {
            "row_id": "SCKG3128_1",
            "gate": "WEP_anchor_consistency",
            "status": "3122_deltaC_recovered_from_3125_bound",
            "claim_allowed": "false",
            "theorem_or_failure": f"eta_bound/deltaJ_bound gives DeltaC threshold {by_id.get('SCK3128_0', {}).get('kernel_abs_max_if_static_unit_projection', '')}.",
            "observable_links": "WEP;delta_J;material_CJ",
            "next_action": "use as sanity check only; do not transfer material coefficient into source-GM",
            "source_paths": by_id.get("SCK3128_0", {}).get("source_paths", ""),
        },
        {
            "row_id": "SCKG3128_2",
            "gate": "PPN_clock_sensitivity",
            "status": "unit_projection_thresholds_computed_nonclaim",
            "claim_allowed": "false",
            "theorem_or_failure": "Clock/gamma/beta rows show sensitivity only; actual projection coefficients are not derived.",
            "observable_links": "PPN;clock;source_GM",
            "next_action": "derive K_clock, K_gamma, K_beta before scoring",
            "source_paths": f"{by_id.get('SCK3128_1', {}).get('source_paths', '')};{by_id.get('SCK3128_2', {}).get('source_paths', '')};{by_id.get('SCK3128_3', {}).get('source_paths', '')}",
        },
        {
            "row_id": "SCKG3128_3",
            "gate": "Gdot_time_profile",
            "status": "kept_time_profile_not_static_bound",
            "claim_allowed": "false",
            "theorem_or_failure": by_id.get("SCK3128_4", {}).get("kernel_formula", ""),
            "observable_links": "Gdot;time;orbital",
            "next_action": "derive d(delta_J)/dt and d(DeltaC_Scal)/dt",
            "source_paths": by_id.get("SCK3128_4", {}).get("source_paths", ""),
        },
        {
            "row_id": "SCKG3128_4",
            "gate": "next_target_3129",
            "status": "queued_source_weight_or_zero_proof",
            "claim_allowed": "false",
            "theorem_or_failure": "The decisive next step is actual source/calibration weights or parent zero.",
            "observable_links": "GR_reduction;Newtonian_GM;Maxwell;calibration",
            "next_action": "3129 should target Sun/Earth/lab source-calibration weights from Hilbert stress or prove calibration-only zero",
            "source_paths": OUTPUT,
        },
    ]


def main() -> None:
    inputs = read_csv(INPUT)
    sources = load_sources(inputs)
    outputs = output_rows(sources)
    validations = validate(inputs, sources, outputs)
    write_csv(OUTPUT, outputs)
    write_csv(VALIDATION, validations)
    write_csv(GATE, gate_rows(outputs))
    failing = [row for row in validations if row.get("status") != "pass"]
    if failing:
        raise SystemExit(f"3128 validation failed: {json.dumps(failing, sort_keys=True)}")
    print(f"wrote {OUTPUT}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {GATE}")


if __name__ == "__main__":
    main()
