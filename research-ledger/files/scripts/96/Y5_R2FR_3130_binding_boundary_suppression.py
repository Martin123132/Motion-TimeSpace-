from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3130_VALIDATION.csv"
GATE = OUT / "P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_GATE.csv"


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


def coefficient(role: str, sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get(role, {}).get("row") or {}
    value = parse_float(row.get("coefficient_value", ""))
    return abs(value) if value is not None else None


def threshold(sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get("surface_binding_hazard", {}).get("row") or {}
    return parse_float(row.get("WEP_kernel_threshold_abs", ""))


def delta_j_bound(sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get("surface_binding_hazard", {}).get("row") or {}
    return parse_float(row.get("deltaJ_bound_abs", ""))


def eta_bound(sources: dict[str, dict[str, Any]]) -> float | None:
    row = sources.get("surface_binding_hazard", {}).get("row") or {}
    return parse_float(row.get("WEP_eta_bound", ""))


def bound_factors(channel: str, coeff: float | None, limit: float | None, delta_bound: float | None) -> dict[str, Any]:
    if coeff is None or limit is None or coeff <= 0:
        return {
            "residual_factor_max": "",
            "suppression_min": "",
            "predicted_abs_unsuppressed": "",
            "predicted_abs_at_required_factor": "",
            "status": "not_scoreable",
        }
    residual_factor = limit / coeff
    suppression = max(0.0, 1.0 - residual_factor)
    predicted = coeff * delta_bound if delta_bound is not None else None
    predicted_at_factor = limit * delta_bound if delta_bound is not None else None
    return {
        "residual_factor_max": residual_factor,
        "suppression_min": suppression,
        "predicted_abs_unsuppressed": predicted if predicted is not None else "",
        "predicted_abs_at_required_factor": predicted_at_factor if predicted_at_factor is not None else "",
        "status": "requires_suppression_nonclaim" if residual_factor < 1.0 else "already_below_threshold_nonclaim",
    }


def output_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    surf = coefficient("surface_binding_hazard", sources)
    l1 = coefficient("L1_envelope_hazard", sources)
    limit = threshold(sources)
    delta_bound = delta_j_bound(sources)
    eta = eta_bound(sources)
    surf_factors = bound_factors("surface", surf, limit, delta_bound)
    l1_factors = bound_factors("L1", l1, limit, delta_bound)
    paths = lambda *roles: ";".join(str(sources[role]["path"]) for role in roles)
    return [
        {
            "row_id": "BBS3130_0",
            "route": "boundary_exact_common_mode_zero",
            "target_channel": "surface_binding",
            "statement": "If Q_surface_binding is an exact boundary partition term and source plus calibration use the same fixed Hilbert-stress worldtube functional, its common-mode contribution cancels from DeltaC_Scal.",
            "coefficient_abs": surf if surf is not None else "",
            "WEP_kernel_threshold_abs": limit if limit is not None else "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "residual_factor_max": "0_if_exact_boundary_common_mode",
            "suppression_min": "1_if_exact_boundary_common_mode",
            "predicted_abs_unsuppressed": surf_factors["predicted_abs_unsuppressed"],
            "predicted_abs_at_required_factor": "0",
            "status": "exact_conditional_zero_not_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "BOUNDARY_EXACTNESS_UNSIGNED;SAME_WORLDTUBE_CALIBRATION_UNSIGNED;RELATIVE_SOURCE_VECTOR_LIVE",
            "next_action": "prove boundary exactness plus same source/calibration worldtube, or use finite suppression bound",
            "source_paths": paths("surface_binding_hazard", "calibration_zero_route", "source_descent_guard"),
            "generated_utc": stamp(),
        },
        {
            "row_id": "BBS3130_1",
            "route": "surface_binding_profile_or_calibration_bound",
            "target_channel": "surface_binding",
            "statement": "For a residual profile/calibration mismatch rho_surf, require |rho_surf Q_surface_binding| <= WEP-set DeltaC threshold.",
            "coefficient_abs": surf if surf is not None else "",
            "WEP_kernel_threshold_abs": limit if limit is not None else "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "residual_factor_max": surf_factors["residual_factor_max"],
            "suppression_min": surf_factors["suppression_min"],
            "predicted_abs_unsuppressed": surf_factors["predicted_abs_unsuppressed"],
            "predicted_abs_at_required_factor": eta if eta is not None else "",
            "status": surf_factors["status"],
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "PROFILE_FACTOR_UNFILLED;CALIBRATION_MISMATCH_UNFILLED;BULK_NOT_PROFILE_WEIGHTED",
            "next_action": "derive rho_surf from profile/worldtube weighting or calibration mismatch",
            "source_paths": paths("surface_binding_hazard", "profile_missing"),
            "generated_utc": stamp(),
        },
        {
            "row_id": "BBS3130_2",
            "route": "L1_worst_channel_bound",
            "target_channel": "bulk_L1_envelope",
            "statement": "For no-cancellation bulk L1 envelope, require |rho_L1 Q_bulk_abs_L1| <= WEP-set DeltaC threshold.",
            "coefficient_abs": l1 if l1 is not None else "",
            "WEP_kernel_threshold_abs": limit if limit is not None else "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "residual_factor_max": l1_factors["residual_factor_max"],
            "suppression_min": l1_factors["suppression_min"],
            "predicted_abs_unsuppressed": l1_factors["predicted_abs_unsuppressed"],
            "predicted_abs_at_required_factor": eta if eta is not None else "",
            "status": l1_factors["status"],
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "NO_CANCELLATION_ENVELOPE_ONLY;PROFILE_FACTOR_UNFILLED;NOT_A_PREDICTION",
            "next_action": "replace L1 envelope with signed source coefficient vector or zero theorem",
            "source_paths": paths("L1_envelope_hazard", "profile_missing"),
            "generated_utc": stamp(),
        },
        {
            "row_id": "BBS3130_3",
            "route": "profile_weighting_required",
            "target_channel": "Earth_profile_worldtube",
            "statement": "Bulk Earth DD values cannot score local source-GM/WEP; the profile/worldtube source vector must be filled before any claim.",
            "coefficient_abs": "",
            "WEP_kernel_threshold_abs": limit if limit is not None else "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "residual_factor_max": "",
            "suppression_min": "",
            "predicted_abs_unsuppressed": "",
            "predicted_abs_at_required_factor": "",
            "status": "profile_required_before_claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "MISSING_PROFILE_WEIGHTED_VALUE;BULK_AS_PROFILE_REFUSED",
            "next_action": "fill shell/orbit/source support weighting or keep 3129 as smoke only",
            "source_paths": paths("profile_missing", "profile_refusal"),
            "generated_utc": stamp(),
        },
        {
            "row_id": "BBS3130_4",
            "route": "next_decision",
            "target_channel": "binding_or_profile_fork",
            "statement": "The binding channel can pass only by exact boundary/common-mode zero or by a residual profile/calibration factor below the computed cap.",
            "coefficient_abs": surf if surf is not None else "",
            "WEP_kernel_threshold_abs": limit if limit is not None else "",
            "deltaJ_bound_abs": delta_bound if delta_bound is not None else "",
            "residual_factor_max": surf_factors["residual_factor_max"],
            "suppression_min": surf_factors["suppression_min"],
            "predicted_abs_unsuppressed": surf_factors["predicted_abs_unsuppressed"],
            "predicted_abs_at_required_factor": eta if eta is not None else "",
            "status": "queued_boundary_zero_or_profile_fill",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "NEXT_ROUTE_REQUIRED",
            "next_action": "3131 should attempt the boundary exactness/common-worldtube proof; if it fails, fill rho_surf profile factor",
            "source_paths": paths("surface_binding_hazard", "profile_missing", "source_descent_guard"),
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
    surface = [row for row in outputs if row.get("row_id") == "BBS3130_1"]
    l1 = [row for row in outputs if row.get("row_id") == "BBS3130_2"]
    profile = [row for row in outputs if row.get("row_id") == "BBS3130_3"]
    return [
        {
            "check_id": "VAL3130_0_input_schema",
            "status": "pass" if inputs and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3130_1_required_source_rows_resolve",
            "status": "pass" if all(payload["exists"] and payload["found"] for payload in sources.values()) else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3130_2_surface_residual_factor_computed",
            "status": "pass" if surface and parse_float(surface[0].get("residual_factor_max", "")) is not None and parse_float(surface[0].get("residual_factor_max", "")) < 1 else "fail",
            "details": json.dumps(surface, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3130_3_L1_residual_factor_computed",
            "status": "pass" if l1 and parse_float(l1[0].get("residual_factor_max", "")) is not None and parse_float(l1[0].get("residual_factor_max", "")) < 1 else "fail",
            "details": json.dumps(l1, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3130_4_profile_refusal_retained",
            "status": "pass" if profile and "BULK_AS_PROFILE_REFUSED" in profile[0].get("issues", "") else "fail",
            "details": json.dumps(profile, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3130_5_all_outputs_nonclaim",
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
            "row_id": "BBSG3130_0",
            "gate": "boundary_exact_zero_route",
            "status": "conditional_zero_not_signed",
            "claim_allowed": "false",
            "theorem_or_failure": by_id.get("BBS3130_0", {}).get("statement", ""),
            "observable_links": "source_GM;boundary;calibration",
            "next_action": by_id.get("BBS3130_0", {}).get("next_action", ""),
            "source_paths": by_id.get("BBS3130_0", {}).get("source_paths", ""),
        },
        {
            "row_id": "BBSG3130_1",
            "gate": "surface_binding_suppression_bound",
            "status": "finite_residual_cap_computed",
            "claim_allowed": "false",
            "theorem_or_failure": f"Need |rho_surf| <= {by_id.get('BBS3130_1', {}).get('residual_factor_max', '')} or suppression >= {by_id.get('BBS3130_1', {}).get('suppression_min', '')}.",
            "observable_links": "Earth_binding;WEP;source_GM",
            "next_action": by_id.get("BBS3130_1", {}).get("next_action", ""),
            "source_paths": by_id.get("BBS3130_1", {}).get("source_paths", ""),
        },
        {
            "row_id": "BBSG3130_2",
            "gate": "L1_envelope_suppression_bound",
            "status": "finite_L1_cap_computed",
            "claim_allowed": "false",
            "theorem_or_failure": f"Need |rho_L1| <= {by_id.get('BBS3130_2', {}).get('residual_factor_max', '')} for the no-cancellation envelope.",
            "observable_links": "Earth_source;WEP;no_cancellation",
            "next_action": by_id.get("BBS3130_2", {}).get("next_action", ""),
            "source_paths": by_id.get("BBS3130_2", {}).get("source_paths", ""),
        },
        {
            "row_id": "BBSG3130_3",
            "gate": "profile_weighting_required",
            "status": "claim_blocked_until_profile_filled",
            "claim_allowed": "false",
            "theorem_or_failure": by_id.get("BBS3130_3", {}).get("statement", ""),
            "observable_links": "MICROSCOPE;Earth_profile;source_worldtube",
            "next_action": by_id.get("BBS3130_3", {}).get("next_action", ""),
            "source_paths": by_id.get("BBS3130_3", {}).get("source_paths", ""),
        },
        {
            "row_id": "BBSG3130_4",
            "gate": "next_target_3131",
            "status": "queued_boundary_exactness_or_profile_fill",
            "claim_allowed": "false",
            "theorem_or_failure": "Surface-binding route now has an exact zero target and a finite residual cap.",
            "observable_links": "GR_reduction;Newtonian_GM;WEP;boundary",
            "next_action": "3131 should prove boundary exactness/common-worldtube cancellation or fill rho_surf profile factor",
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
        raise SystemExit(f"3130 validation failed: {json.dumps(failing, sort_keys=True)}")
    print(f"wrote {OUTPUT}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {GATE}")


if __name__ == "__main__":
    main()
