from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3129_VALIDATION.csv"
GATE = OUT / "P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_GATE.csv"


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


def delta_j_bound(sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get("deltaJ_bound", {}).get("row") or {}
    return parse_float(row.get("numeric_bound_abs", ""))


def wep_threshold(sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get("WEP_threshold", {}).get("row") or {}
    return parse_float(row.get("kernel_abs_max_if_static_unit_projection", ""))


def wep_bound(sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get("local_bounds", {}).get("row") or {}
    return parse_float(row.get("upper_bound", ""))


def earth_bulk_values(sources: dict[str, dict[str, Any]]) -> dict[str, float | None]:
    row = sources.get("Earth_bulk_DD_context", {}).get("row") or {}
    return {
        "Q_alpha_Coulomb_Earth": parse_float(row.get("Q_alpha_Coulomb_Earth", "")),
        "Q_surface_binding_Earth": parse_float(row.get("Q_surface_binding_Earth", "")),
        "Q_bulk_abs_L1": parse_float(row.get("Q_bulk_abs_L1", "")),
    }


def channel_row(
    row_id: str,
    channel: str,
    coefficient: float | None,
    delta_bound: float | None,
    threshold: float | None,
    eta_bound: float | None,
    formula: str,
    notes: str,
    source_paths: str,
) -> dict[str, Any]:
    predicted = abs(coefficient * delta_bound) if coefficient is not None and delta_bound is not None else None
    threshold_margin = threshold - abs(coefficient) if coefficient is not None and threshold is not None else None
    eta_margin = eta_bound - predicted if eta_bound is not None and predicted is not None else None
    sensitivity_status = "not_scoreable"
    if threshold_margin is not None:
        sensitivity_status = "below_WEP_threshold_nonclaim" if threshold_margin >= 0 else "above_WEP_threshold_hazard_nonclaim"
    return {
        "row_id": row_id,
        "channel": channel,
        "coefficient_formula": formula,
        "coefficient_value": coefficient if coefficient is not None else "",
        "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
        "predicted_abs_at_deltaJ_bound": predicted if predicted is not None else "",
        "WEP_kernel_threshold_abs": threshold if threshold is not None else "",
        "threshold_margin": threshold_margin if threshold_margin is not None else "",
        "WEP_eta_bound": eta_bound if eta_bound is not None else "",
        "eta_margin": eta_margin if eta_margin is not None else "",
        "sensitivity_status": sensitivity_status,
        "score": "sensitivity_only_nonclaim",
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "issues": "BULK_NOT_PROFILE_WEIGHTED;CALIBRATION_KERNEL_MISSING;PARENT_COEFFICIENT_VECTOR_MISSING;INPUT_VALID_FOR_CLAIM_FALSE",
        "notes": notes,
        "next_action": "derive profile/worldtube source vector and calibration vector before scoring",
        "source_paths": source_paths,
        "generated_utc": stamp(),
    }


def output_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    delta_bound = delta_j_bound(sources)
    threshold = wep_threshold(sources)
    eta = wep_bound(sources)
    earth = earth_bulk_values(sources)
    q_alpha = earth["Q_alpha_Coulomb_Earth"]
    q_surface = earth["Q_surface_binding_Earth"]
    q_l1 = earth["Q_bulk_abs_L1"]
    alpha_cj = 2.0 * q_alpha if q_alpha is not None else None
    paths = lambda *roles: ";".join(str(sources[role]["path"]) for role in roles)
    rows = [
        {
            "row_id": "ESC3129_0",
            "channel": "calibration_only_zero_theorem",
            "coefficient_formula": "If C_J,S^ADM and C_J,cal^ADM are the same common-mode Hilbert-stress functional, DeltaC_Scal=0.",
            "coefficient_value": "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "predicted_abs_at_deltaJ_bound": "",
            "WEP_kernel_threshold_abs": threshold if threshold is not None else "",
            "threshold_margin": "",
            "WEP_eta_bound": eta if eta is not None else "",
            "eta_margin": "",
            "sensitivity_status": "exact_conditional_zero_not_signed",
            "score": "theorem_target_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "COMMON_MODE_THEOREM_UNSIGNED;RELATIVE_SOURCE_VECTOR_LIVE;CALIBRATION_VECTOR_MISSING",
            "notes": "This is the clean zero route, but 2125 keeps relative source residuals live.",
            "next_action": "prove NoSourceOnlySpeciesSlot/source-label forgetting/readout no-reentry or keep finite source vector",
            "source_paths": paths("calibration_guard", "source_calibration_interface"),
            "generated_utc": stamp(),
        },
        channel_row(
            "ESC3129_1",
            "Earth_bulk_Coulomb_alpha_smoke",
            alpha_cj,
            delta_bound,
            threshold,
            eta,
            "DeltaC_Earth_bulk_alpha_smoke=2*Q_alpha_Coulomb_Earth with tau_EM=1,zeta_Q=0,C_relax=0,C_cal=0",
            "Coulomb-only bulk Earth channel sits just below the WEP-set coefficient threshold, but is not profile/worldtube weighted.",
            paths("Earth_bulk_DD_context", "WEP_threshold", "deltaJ_bound"),
        ),
        channel_row(
            "ESC3129_2",
            "Earth_bulk_surface_binding_raw_DD",
            q_surface,
            delta_bound,
            threshold,
            eta,
            "DeltaC_Earth_surface_raw=Q_surface_binding_Earth",
            "Raw surface/binding DD component is larger than the WEP-set threshold unless suppressed, calibrated, or projected silent.",
            paths("Earth_bulk_DD_context", "WEP_threshold", "deltaJ_bound"),
        ),
        channel_row(
            "ESC3129_3",
            "Earth_bulk_L1_worst_channel_envelope",
            q_l1,
            delta_bound,
            threshold,
            eta,
            "DeltaC_Earth_bulk_L1=Q_bulk_abs_L1",
            "L1 bulk envelope is a no-cancellation hazard row, not a prediction.",
            paths("Earth_bulk_DD_context", "WEP_threshold", "deltaJ_bound"),
        ),
        {
            "row_id": "ESC3129_4",
            "channel": "profile_weighting_refusal",
            "coefficient_formula": "bulk Earth vector != MICROSCOPE/orbit/profile/worldtube source vector",
            "coefficient_value": "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "predicted_abs_at_deltaJ_bound": "",
            "WEP_kernel_threshold_abs": threshold if threshold is not None else "",
            "threshold_margin": "",
            "WEP_eta_bound": eta if eta is not None else "",
            "eta_margin": "",
            "sensitivity_status": "profile_required_before_claim",
            "score": "refusal_guard",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "MISSING_PROFILE_WEIGHTED_VALUE;BULK_AS_PROFILE_REFUSED",
            "notes": "2125 explicitly refuses using bulk Earth vector as profile/worldtube vector.",
            "next_action": "derive shell/orbit/source support weighting before local source-GM/WEP scoring",
            "source_paths": paths("Earth_profile_missing", "Earth_bulk_DD_context"),
            "generated_utc": stamp(),
        },
        {
            "row_id": "ESC3129_5",
            "channel": "next_decision",
            "coefficient_formula": "Either suppress/calibrate surface-binding/source vector through parent grammar or fill real source/calibration profiles.",
            "coefficient_value": "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "predicted_abs_at_deltaJ_bound": "",
            "WEP_kernel_threshold_abs": threshold if threshold is not None else "",
            "threshold_margin": "",
            "WEP_eta_bound": eta if eta is not None else "",
            "eta_margin": "",
            "sensitivity_status": "surface_binding_channel_is_next_pressure_point",
            "score": "route_selector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "NEXT_ROUTE_REQUIRED",
            "notes": "The finite path is no longer vague: alpha channel is mild; binding/source channel is the pressure point.",
            "next_action": "3130 should derive/calibrate/suppress Q_surface_binding or fill profile-weighted source-calibration vector",
            "source_paths": paths("Earth_bulk_DD_context", "calibration_guard", "source_calibration_interface"),
            "generated_utc": stamp(),
        },
    ]
    return rows


def validate(inputs: list[dict[str, str]], sources: dict[str, dict[str, Any]], outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = ["source_id", "role", "source_file", "source_row_id", "row_id_column", "required", "valid_for_claim", "notes"]
    columns = set(inputs[0].keys()) if inputs else set()
    missing_columns = [column for column in required if column not in columns]
    source_status = {
        role: {"exists": payload["exists"], "found": payload["found"], "path": str(payload["path"])}
        for role, payload in sources.items()
    }
    alpha = [row for row in outputs if row.get("row_id") == "ESC3129_1"]
    surface = [row for row in outputs if row.get("row_id") == "ESC3129_2"]
    profile = [row for row in outputs if row.get("row_id") == "ESC3129_4"]
    return [
        {
            "check_id": "VAL3129_0_input_schema",
            "status": "pass" if inputs and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3129_1_required_source_rows_resolve",
            "status": "pass" if all(payload["exists"] and payload["found"] for payload in sources.values()) else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3129_2_alpha_channel_below_WEP_threshold",
            "status": "pass" if alpha and alpha[0].get("sensitivity_status") == "below_WEP_threshold_nonclaim" else "fail",
            "details": json.dumps(alpha, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3129_3_surface_binding_hazard_detected",
            "status": "pass" if surface and surface[0].get("sensitivity_status") == "above_WEP_threshold_hazard_nonclaim" else "fail",
            "details": json.dumps(surface, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3129_4_profile_refusal_retained",
            "status": "pass" if profile and "BULK_AS_PROFILE_REFUSED" in profile[0].get("issues", "") else "fail",
            "details": json.dumps(profile, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3129_5_all_outputs_nonclaim",
            "status": "pass" if outputs and all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def gate_rows(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row.get("row_id", ""): row for row in outputs}
    return [
        {
            "row_id": "ESCG3129_0",
            "gate": "calibration_only_zero_route",
            "status": "conditional_zero_not_signed",
            "claim_allowed": "false",
            "theorem_or_failure": by_id.get("ESC3129_0", {}).get("coefficient_formula", ""),
            "observable_links": "source_GM;calibration;local_GR",
            "next_action": by_id.get("ESC3129_0", {}).get("next_action", ""),
            "source_paths": by_id.get("ESC3129_0", {}).get("source_paths", ""),
        },
        {
            "row_id": "ESCG3129_1",
            "gate": "Earth_bulk_alpha_smoke",
            "status": "below_WEP_threshold_nonclaim",
            "claim_allowed": "false",
            "theorem_or_failure": f"alpha smoke coefficient {by_id.get('ESC3129_1', {}).get('coefficient_value', '')} gives residual {by_id.get('ESC3129_1', {}).get('predicted_abs_at_deltaJ_bound', '')}",
            "observable_links": "Earth_source;Coulomb;source_GM",
            "next_action": "replace bulk smoke with profile/worldtube source vector",
            "source_paths": by_id.get("ESC3129_1", {}).get("source_paths", ""),
        },
        {
            "row_id": "ESCG3129_2",
            "gate": "Earth_binding_hazard",
            "status": "above_WEP_threshold_hazard_nonclaim",
            "claim_allowed": "false",
            "theorem_or_failure": f"surface/binding raw coefficient {by_id.get('ESC3129_2', {}).get('coefficient_value', '')} exceeds WEP-set threshold {by_id.get('ESC3129_2', {}).get('WEP_kernel_threshold_abs', '')}",
            "observable_links": "Earth_source;binding;WEP;source_GM",
            "next_action": "derive why binding channel is suppressed/calibrated/projected silent, or carry it as the finite pressure channel",
            "source_paths": by_id.get("ESC3129_2", {}).get("source_paths", ""),
        },
        {
            "row_id": "ESCG3129_3",
            "gate": "profile_weighting_guard",
            "status": "bulk_not_profile_claim_blocked",
            "claim_allowed": "false",
            "theorem_or_failure": by_id.get("ESC3129_4", {}).get("notes", ""),
            "observable_links": "MICROSCOPE;Earth_profile;source_worldtube",
            "next_action": by_id.get("ESC3129_4", {}).get("next_action", ""),
            "source_paths": by_id.get("ESC3129_4", {}).get("source_paths", ""),
        },
        {
            "row_id": "ESCG3129_4",
            "gate": "next_target_3130",
            "status": "queued_binding_suppression_or_profile_fill",
            "claim_allowed": "false",
            "theorem_or_failure": "Finite source side now has a concrete pressure channel: Earth surface/binding DD component.",
            "observable_links": "GR_reduction;Newtonian_GM;WEP;source_calibration",
            "next_action": "3130 should target Q_surface_binding suppression/calibration/projection or profile-weighted source vector fill",
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
        raise SystemExit(f"3129 validation failed: {json.dumps(failing, sort_keys=True)}")
    print(f"wrote {OUTPUT}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {GATE}")


if __name__ == "__main__":
    main()
