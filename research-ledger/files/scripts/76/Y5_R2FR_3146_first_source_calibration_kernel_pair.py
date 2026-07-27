from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3146_INPUTS.csv"
PAIR = OUT / "P8_Y5_R2FR_3146_SOURCE_CALIBRATION_KERNEL_PAIR.csv"
COMBO = OUT / "P8_Y5_R2FR_3146_NO_CANCELLATION_COMBO_SCORE.csv"
GATES = OUT / "P8_Y5_R2FR_3146_GATES.csv"
DECISION = OUT / "P8_Y5_R2FR_3146_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3146_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(relative: str) -> str:
    return str((ROOT / relative).resolve())


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def find_row(rows: list[dict[str, str]], column: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(column) == value:
            return row
    raise ValueError(f"row not found: {column}={value}")


def fmt(value: float | None) -> str:
    if value is None:
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def input_rows() -> list[dict[str, str]]:
    now = stamp()
    rows = [
        {
            "source_id": "SRC3146_0_3145_doc",
            "path": source_path("3145-Y5-R2FR-deltaJ-before-source-GM-kernel-derivation-under-AX1090.md"),
            "role": "derived source-GM kernel law",
        },
        {
            "source_id": "SRC3146_1_3145_kernel",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3145_DELTAJ_BEFORE_GM_KERNEL.csv"),
            "role": "kernel formula rows",
        },
        {
            "source_id": "SRC3146_2_3128_interface",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3128_SOURCE_CAL_KERNEL_INTERFACE_OUTPUT.csv"),
            "role": "sensitivity threshold and source-calibration interface",
        },
        {
            "source_id": "SRC3146_3_3129_smoke",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv"),
            "role": "Earth bulk Coulomb and raw surface/binding smoke rows",
        },
        {
            "source_id": "SRC3146_4_3130_suppression",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_OUTPUT.csv"),
            "role": "surface-binding suppression cap",
        },
        {
            "source_id": "SRC3146_5_3133_profile",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3133_RHO_PROFILE_WORLDTUBE_FIRST_ROW.csv"),
            "role": "first profile/worldtube smoke row",
        },
        {
            "source_id": "SRC3146_6_3132_allocator",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3132_RHO_SURF_ALLOCATOR.csv"),
            "role": "absolute rho allocator/no-cancellation policy",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def extracted_values() -> dict[str, float | None]:
    rows_3128 = read_csv(OUT / "P8_Y5_R2FR_3128_SOURCE_CAL_KERNEL_INTERFACE_OUTPUT.csv")
    rows_3129 = read_csv(OUT / "P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv")
    rows_3130 = read_csv(OUT / "P8_Y5_R2FR_3130_BINDING_BOUNDARY_SUPPRESSION_OUTPUT.csv")
    rows_3133 = read_csv(OUT / "P8_Y5_R2FR_3133_RHO_PROFILE_WORLDTUBE_FIRST_ROW.csv")

    row_3128_wep = find_row(rows_3128, "kernel_id", "SCK3128_0")
    row_coulomb = find_row(rows_3129, "row_id", "ESC3129_1")
    row_binding = find_row(rows_3129, "row_id", "ESC3129_2")
    row_suppression = find_row(rows_3130, "row_id", "BBS3130_1")
    row_profile_summary = find_row(rows_3133, "row_id", "RHO3133_0_profile_worldtube_summary")
    row_profile_signed = find_row(rows_3133, "row_id", "RHO3133_7_lambda_over_RE_0p03")

    return {
        "delta_j_bound_abs": parse_float(row_3128_wep.get("deltaJ_bound_abs")),
        "wep_kernel_threshold_abs": parse_float(row_3128_wep.get("kernel_abs_max_if_static_unit_projection")),
        "wep_eta_bound": parse_float(row_coulomb.get("WEP_eta_bound")),
        "coulomb_delta_k": parse_float(row_coulomb.get("coefficient_value")),
        "surface_binding_raw": parse_float(row_binding.get("coefficient_value")),
        "rho_surf_cap": parse_float(row_suppression.get("residual_factor_max")),
        "profile_delta_abs_max": parse_float(row_profile_summary.get("delta_surface_vs_bulk")),
        "profile_rho_abs_max": parse_float(row_profile_summary.get("rho_profile_abs")),
        "profile_delta_signed": parse_float(row_profile_signed.get("delta_surface_vs_bulk")),
    }


def pair_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    delta = values["delta_j_bound_abs"]
    threshold = values["wep_kernel_threshold_abs"]
    coulomb = values["coulomb_delta_k"]
    binding = values["surface_binding_raw"]
    profile_abs = values["profile_delta_abs_max"]
    profile_signed = values["profile_delta_signed"]

    def predicted_abs(coefficient: float | None) -> str:
        if coefficient is None or delta is None:
            return "MISSING_NUMERIC_VALUE"
        return fmt(abs(coefficient) * delta)

    def threshold_status(abs_coefficient: float | None) -> str:
        if abs_coefficient is None or threshold is None:
            return "not_scoreable_missing_numeric"
        if abs_coefficient <= threshold:
            return "below_WEP_set_coefficient_threshold_nonclaim"
        return "above_WEP_set_coefficient_threshold_pressure"

    return [
        {
            "pair_id": "PAIR3146_0_common_mode_zero",
            "kernel_pair": "K_GM_J[S]-K_GM_J[cal]",
            "source_kernel": "K_common",
            "calibration_kernel": "K_common",
            "deltaK_value": "0_if_same_worldtube_common_mode",
            "deltaK_abs": "0_if_theorem_signed",
            "predicted_abs_at_deltaJ_bound": "0_if_theorem_signed",
            "threshold_status": "exact_conditional_zero_not_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "COMMON_MODE_THEOREM_UNSIGNED;SAME_WORLDTUBE_CALIBRATION_UNSIGNED",
            "source_paths": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv"),
            "generated_utc": now,
        },
        {
            "pair_id": "PAIR3146_1_earth_bulk_coulomb",
            "kernel_pair": "K_Earth_bulk_alpha-K_cal",
            "source_kernel": fmt(coulomb),
            "calibration_kernel": "0_smoke_convention",
            "deltaK_value": fmt(coulomb),
            "deltaK_abs": fmt(abs(coulomb) if coulomb is not None else None),
            "predicted_abs_at_deltaJ_bound": predicted_abs(coulomb),
            "threshold_status": threshold_status(abs(coulomb) if coulomb is not None else None),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "BULK_NOT_PROFILE_WEIGHTED;CALIBRATION_KERNEL_MISSING;SMOKE_CONVENTION",
            "source_paths": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv"),
            "generated_utc": now,
        },
        {
            "pair_id": "PAIR3146_2_earth_surface_binding_raw",
            "kernel_pair": "K_Earth_surface_binding_raw-K_cal",
            "source_kernel": fmt(binding),
            "calibration_kernel": "0_smoke_convention",
            "deltaK_value": fmt(binding),
            "deltaK_abs": fmt(abs(binding) if binding is not None else None),
            "predicted_abs_at_deltaJ_bound": predicted_abs(binding),
            "threshold_status": threshold_status(abs(binding) if binding is not None else None),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "RAW_BINDING_CHANNEL_OVER_THRESHOLD;BULK_NOT_PROFILE_WEIGHTED;CALIBRATION_KERNEL_MISSING",
            "source_paths": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv"),
            "generated_utc": now,
        },
        {
            "pair_id": "PAIR3146_3_profile_worldtube_smoke_delta",
            "kernel_pair": "K_profile_worldtube-K_bulk_binding",
            "source_kernel": "profile_weighted_binding_smoke",
            "calibration_kernel": "bulk_binding_reference_smoke",
            "deltaK_value": fmt(profile_signed),
            "deltaK_abs": fmt(profile_abs),
            "predicted_abs_at_deltaJ_bound": predicted_abs(profile_abs),
            "threshold_status": threshold_status(profile_abs),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "TWO_LAYER_SMOKE_ONLY;PREM_PROFILE_MISSING;PARENT_LAMBDA_READOUT_UNSIGNED",
            "source_paths": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3133_RHO_PROFILE_WORLDTUBE_FIRST_ROW.csv"),
            "generated_utc": now,
        },
    ]


def combo_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    delta = values["delta_j_bound_abs"]
    threshold = values["wep_kernel_threshold_abs"]
    coulomb = values["coulomb_delta_k"]
    profile_abs = values["profile_delta_abs_max"]
    profile_signed = values["profile_delta_signed"]
    binding = values["surface_binding_raw"]
    rho_cap = values["rho_surf_cap"]
    rho_profile = values["profile_rho_abs_max"]

    abs_combo = None if coulomb is None or profile_abs is None else abs(coulomb) + abs(profile_abs)
    signed_combo = None if coulomb is None or profile_signed is None else coulomb + profile_signed
    raw_binding_abs = None if binding is None else abs(binding)
    required_rho_for_abs_combo = None
    if threshold is not None and coulomb is not None and raw_binding_abs not in (None, 0):
        required_rho_for_abs_combo = max(0.0, (threshold - abs(coulomb)) / raw_binding_abs)

    def eta(coefficient: float | None) -> str:
        if coefficient is None or delta is None:
            return "MISSING_NUMERIC_VALUE"
        return fmt(abs(coefficient) * delta)

    def pass_status(coefficient: float | None, allow_sign: bool) -> str:
        if coefficient is None or threshold is None:
            return "not_scoreable_missing_numeric"
        if abs(coefficient) <= threshold:
            return "below_threshold_nonclaim_sign_allowed" if allow_sign else "below_threshold_nonclaim_absolute"
        return "above_threshold_pressure_absolute" if not allow_sign else "above_threshold_pressure"

    return [
        {
            "combo_id": "COMBO3146_0_absolute_coulomb_plus_profile",
            "rule": "no_cancellation_absolute_sum",
            "coefficient_formula": "|DeltaK_coulomb_bulk| + |DeltaK_profile_worldtube_smoke|",
            "coefficient_abs": fmt(abs_combo),
            "threshold_abs": fmt(threshold),
            "predicted_eta_abs_at_deltaJ_bound": eta(abs_combo),
            "score": pass_status(abs_combo, allow_sign=False),
            "interpretation": "current smoke/profile pair is slightly above the WEP-set coefficient threshold under strict absolute addition",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "ABSOLUTE_COMBO_OVER_THRESHOLD;SMOKE_PROFILE;CALIBRATION_KERNEL_MISSING",
            "generated_utc": now,
        },
        {
            "combo_id": "COMBO3146_1_signed_coulomb_plus_profile",
            "rule": "signed_sum_only_if_parent_map_locks_signs",
            "coefficient_formula": "DeltaK_coulomb_bulk + DeltaK_profile_worldtube_signed",
            "coefficient_abs": fmt(abs(signed_combo) if signed_combo is not None else None),
            "threshold_abs": fmt(threshold),
            "predicted_eta_abs_at_deltaJ_bound": eta(signed_combo),
            "score": pass_status(signed_combo, allow_sign=True),
            "interpretation": "the smoke signs would pass, but sign-cancellation is not allowed until the parent-to-DD map and source profile are signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "SIGN_CANCELLATION_NOT_CLAIMABLE;PARENT_TO_DD_MAP_UNSIGNED;SMOKE_PROFILE",
            "generated_utc": now,
        },
        {
            "combo_id": "COMBO3146_2_required_surface_rho_after_coulomb",
            "rule": "absolute_budget_remaining_after_coulomb",
            "coefficient_formula": "rho_required <= (threshold-|DeltaK_coulomb|)/|Q_surface_binding_raw|",
            "coefficient_abs": fmt(required_rho_for_abs_combo),
            "threshold_abs": fmt(rho_cap),
            "predicted_eta_abs_at_deltaJ_bound": "rho_limit_not_direct_eta",
            "score": (
                "current_profile_rho_above_remaining_absolute_budget"
                if required_rho_for_abs_combo is not None and rho_profile is not None and rho_profile > required_rho_for_abs_combo
                else "not_scoreable_or_below_remaining_budget"
            ),
            "interpretation": "after the Coulomb channel, the profile/binding residual must be tighter than the old standalone rho_surf cap",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "REMAINING_BUDGET_TIGHTER_THAN_STANDALONE_SURFACE_CAP;NEEDS_REAL_PROFILE",
            "generated_utc": now,
        },
    ]


def gate_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3146_0_kernel_pair_built",
            "gate": "first_K_source_minus_K_cal_pair_exists",
            "status": "pass_nonclaim",
            "reason": "3146 gives common-mode, Coulomb, raw binding, profile-worldtube and combo rows in 3145 kernel language",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3146_1_common_mode_zero",
            "gate": "K_source_equals_K_cal_theorem",
            "status": "fail_for_claim",
            "reason": "same-worldtube/common-mode calibration theorem remains unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3146_2_absolute_combo",
            "gate": "absolute_no_cancellation_combo_below_threshold",
            "status": "fail_for_claim_pressure",
            "reason": "Coulomb + profile smoke residual is above threshold under strict absolute addition",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3146_3_signed_combo",
            "gate": "signed_combo_pass_allowed",
            "status": "fail_for_claim",
            "reason": "smoke signs would pass but parent-to-DD/source-profile sign map is not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3146_4_real_profile",
            "gate": "PREM_or_equivalent_profile_worldtube_imported",
            "status": "fail_for_claim",
            "reason": "3133 profile row is two-layer smoke, not source-backed PREM/worldtube/readout",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3146_0_consolidation",
            "decision": "first source/calibration kernel pair is staged in 3145 variables",
            "effect": "DeltaK_GM_J is now represented by explicit common-mode, Coulomb, binding, profile, and combo rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3146_1_pressure_point",
            "decision": "absolute Coulomb plus profile/binding smoke is the live pressure point",
            "effect": "local branch needs either a stronger profile suppression, a signed cancellation/orthogonality theorem, or common-mode calibration",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3146_2_next",
            "decision": "next target is a real profile/worldtube source vector or a parent sign/orthogonality theorem",
            "effect": "3147 should replace the two-layer smoke profile with PREM/shell/readout data, or prove Coulomb and surface channels cannot be added absolutely",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    pairs: list[dict[str, str]],
    combos: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    numerics_present = all(value is not None for value in values.values())
    required_pairs = {"PAIR3146_0_common_mode_zero", "PAIR3146_1_earth_bulk_coulomb", "PAIR3146_2_earth_surface_binding_raw", "PAIR3146_3_profile_worldtube_smoke_delta"}
    pair_cover = required_pairs.issubset({row["pair_id"] for row in pairs})
    required_combos = {"COMBO3146_0_absolute_coulomb_plus_profile", "COMBO3146_1_signed_coulomb_plus_profile", "COMBO3146_2_required_surface_rho_after_coulomb"}
    combo_cover = required_combos.issubset({row["combo_id"] for row in combos})
    absolute_pressure = any(
        row["combo_id"] == "COMBO3146_0_absolute_coulomb_plus_profile"
        and row["score"] == "above_threshold_pressure_absolute"
        for row in combos
    )
    no_claim_leak = all(row.get("claim_allowed", "false") == "false" for row in pairs + combos + gates)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    return [
        {
            "check_id": "V3146_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3146_1_numeric_values_extracted",
            "status": "pass" if numerics_present else "fail",
            "details": json.dumps({key: fmt(value) for key, value in values.items()}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3146_2_pair_rows_cover_routes",
            "status": "pass" if pair_cover else "fail",
            "details": json.dumps([row["pair_id"] for row in pairs], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3146_3_combo_rows_cover_scores",
            "status": "pass" if combo_cover else "fail",
            "details": json.dumps([row["combo_id"] for row in combos], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3146_4_absolute_combo_pressure_detected",
            "status": "pass" if absolute_pressure else "fail",
            "details": "strict no-cancellation combo should remain a pressure row, not a pass claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3146_5_no_claim_leak",
            "status": "pass" if no_claim_leak and decisions_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    values = extracted_values()
    pairs = pair_rows(values)
    combos = combo_rows(values)
    gates = gate_rows(values)
    decisions = decision_rows()
    validations = validation_rows(inputs, pairs, combos, gates, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(PAIR, pairs)
    write_csv(COMBO, combos)
    write_csv(GATES, gates)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
