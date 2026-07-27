from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3170_INPUTS.csv"
SOURCES = OUT / "P8_Y5_R2FR_3170_CONSTANT_SOURCE_REGISTER.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3170_SOLAR_J2_NORMALIZATION_DERIVATION.csv"
AUDIT = OUT / "P8_Y5_R2FR_3170_3169_SHORTCUT_AUDIT.csv"
BOUNDS = OUT / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
DECISION = OUT / "P8_Y5_R2FR_3170_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3170_VALIDATION.csv"

C_LIGHT = 299_792_458.0
GM_SUN_NOMINAL = 1.3271244e20
R_SUN_NOMINAL = 6.957e8
J2_ADOPTED_SOLAR_SCALE = 2.0e-7
J2_RANGE_HIGH = 2.32e-7
J2_HALF_RANGE_PROXY = 3.3e-8


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fmt(value: float) -> str:
    return f"{value:.15e}"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
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


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def csv_value(path: Path, key: str, value: str, column: str) -> str:
    for row in read_csv(path):
        if row.get(key) == value:
            return row[column]
    raise KeyError(f"missing {key}={value} in {path}")


def values() -> dict[str, float]:
    c_k2_unit = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv",
            "unit_id",
            "KU3165_0_definition",
            "value",
        )
    )
    internal_cap = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv",
            "quantity",
            "K_2",
            "required_bound_l2",
        )
    )
    epsilon_sun = GM_SUN_NOMINAL / (C_LIGHT * C_LIGHT * R_SUN_NOMINAL)
    two_epsilon = 2.0 * epsilon_sun
    shortcut_bound = next(
        row
        for row in read_csv(OUT / "P8_Y5_R2FR_3169_EQUIVALENT_J2_K2_BOUNDS.csv")
        if row["bound_id"] == "JB3169_2_Rozelot_half_range_anomaly_scale"
    )
    return {
        "c_k2_unit": c_k2_unit,
        "internal_cap": internal_cap,
        "epsilon_sun_surface": epsilon_sun,
        "two_epsilon_sun_surface": two_epsilon,
        "gm_sun_over_c2_m": GM_SUN_NOMINAL / (C_LIGHT * C_LIGHT),
        "shortcut_half_range_k2": float(shortcut_bound["K2_equivalent_bound"]),
    }


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3169-Y5-R2FR-STF-Shapiro-source-bound-or-solar-domain-K2-transfer-under-AX1090.md", "3169 transfer shortcut to audit"),
        ("3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.md", "weak-field metric projection normalization"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3159_PROJECTION_COEFFICIENT_DERIVATION.csv", "J2 metric coefficient derivation"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3169_EQUIVALENT_J2_K2_BOUNDS.csv", "3169 shortcut bounds"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv", "C_K2_unit"),
    ]
    return [
        {
            "input_id": f"IN3170_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def derivation_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    rho = 1.0
    j2_eff_k2_1 = v["c_k2_unit"] * rho**3 / v["two_epsilon_sun_surface"]
    shapiro_len_k2_1 = 3.0 * v["gm_sun_over_c2_m"] * j2_eff_k2_1
    return [
        {
            "derivation_id": "JN3170_0_metric_projection_convention",
            "object": "solar_exterior_J2_metric_amplitude",
            "statement": "For Phi_J2=(GM/r) J2 (R_s/r)^2 P2, the public metric-component P2 amplitude is A_metric=2 GM/(c^2 r) J2 (R_s/r)^2.",
            "formula": "A_metric(r)=2 epsilon_sun_surface J2 rho^-3, rho=r/R_s",
            "result": "J2 is not equal to A_metric unless 2 epsilon rho^-3 is set to one, which it is not",
            "status": "derived_normalization_map",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "JN3170_1_corrected_J2eff_map",
            "object": "J2_eff_from_K2",
            "statement": "If the MTS residual amplitude A_metric=K2*C_K2_unit is evaluated in the same solar exterior convention, then J2_eff=K2*C_K2_unit*rho^3/(2 epsilon_sun_surface).",
            "formula": "J2_eff = K2*C_K2_unit*rho^3/(2*epsilon_sun_surface)",
            "rho": fmt(rho),
            "epsilon_sun_surface": fmt(v["epsilon_sun_surface"]),
            "two_epsilon_sun_surface": fmt(v["two_epsilon_sun_surface"]),
            "J2_eff_if_K2_equals_1_surface": fmt(j2_eff_k2_1),
            "status": "conditional_corrected_transfer",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "JN3170_2_corrected_Shapiro_length",
            "object": "c_delta_tau_Q_for_K2_equals_1",
            "statement": "Using Zschocke-Klioner c delta tau_Q <= 3 J2 GM/c^2 after the corrected J2 map.",
            "formula": "c_delta_tau_Q(K2=1) <= 3*(GM_sun/c^2)*C_K2_unit/(2 epsilon_sun_surface)",
            "value_m": fmt(shapiro_len_k2_1),
            "status": "conditional_length_map_corrected",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "JN3170_3_radius_profile_warning",
            "object": "rho_dependence",
            "statement": "If K2*C_K2_unit is not a solar-surface exterior metric amplitude, the conversion carries rho^3 and/or a different radial profile factor.",
            "formula": "J2_eff = K2*C_K2_unit*rho^3/(2 epsilon_sun_surface) only for a J2 radial profile r^-3",
            "result": "profile/source-domain normalization remains the claim blocker",
            "status": "transfer_not_claim_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def source_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "source_id": "SRC3170_0_IAU_nominal_solar_constants",
            "role": "solar GM and radius constants for epsilon_sun_surface",
            "title": "Nominal values for selected solar and planetary quantities: IAU 2015 Resolution B3",
            "url": "https://arxiv.org/abs/1605.09788",
            "doi_or_arxiv": "arXiv:1605.09788",
            "GM_sun_m3_s2": fmt(GM_SUN_NOMINAL),
            "R_sun_m": fmt(R_SUN_NOMINAL),
            "epsilon_sun_surface": fmt(v["epsilon_sun_surface"]),
            "two_epsilon_sun_surface": fmt(v["two_epsilon_sun_surface"]),
            "status": "constant_source_recorded_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "source_id": "SRC3170_1_3159_metric_projection",
            "role": "local weak-field J2 metric amplitude convention",
            "title": "3159 projection coefficient derivation for J2 and tide",
            "url": internal("3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.md"),
            "doi_or_arxiv": "local_checkpoint",
            "GM_sun_m3_s2": "not_applicable",
            "R_sun_m": "not_applicable",
            "epsilon_sun_surface": "not_applicable",
            "two_epsilon_sun_surface": "not_applicable",
            "status": "local_metric_convention_source_recorded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def audit_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    correction_factor = v["two_epsilon_sun_surface"]
    inverse_factor = 1.0 / correction_factor
    return [
        {
            "audit_id": "SA3170_0_3169_shortcut_missing_metric_factor",
            "prior_formula": "J2_eff := K2*C_K2_unit",
            "corrected_formula_surface": "J2_eff := K2*C_K2_unit/(2 epsilon_sun_surface)",
            "missing_factor": "1/(2 epsilon_sun_surface)",
            "two_epsilon_sun_surface": fmt(correction_factor),
            "shortcut_J2_eff_too_small_by": fmt(inverse_factor),
            "effect_on_K2_bounds": "corrected surface bounds are smaller by factor 2 epsilon_sun_surface",
            "status": "shortcut_demoted_to_wrong_normalization_smoke",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "SA3170_1_half_range_shortcut_comparison",
            "prior_formula": "K2_bound_3169=J2_bound/C_K2_unit",
            "corrected_formula_surface": "K2_bound_surface=2 epsilon_sun_surface J2_bound/C_K2_unit",
            "prior_half_range_K2_bound": fmt(v["shortcut_half_range_k2"]),
            "corrected_half_range_K2_bound": fmt(v["shortcut_half_range_k2"] * correction_factor),
            "ratio_corrected_to_prior": fmt(correction_factor),
            "status": "corrected_bound_tighter_if_surface_profile_owned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for bound_id, name, j2_bound, status in [
        ("CJ3170_0_ZK_adopted_solar_J2_scale", "adopted_solar_J2_scale", J2_ADOPTED_SOLAR_SCALE, "scale_only_nonclaim"),
        ("CJ3170_1_Rozelot_total_high", "solar_J2_total_high", J2_RANGE_HIGH, "total_scale_nonclaim"),
        ("CJ3170_2_Rozelot_half_range_proxy", "solar_J2_half_range_proxy", J2_HALF_RANGE_PROXY, "rough_pressure_nonclaim"),
    ]:
        amplitude_bound = v["two_epsilon_sun_surface"] * j2_bound
        k2_bound = amplitude_bound / v["c_k2_unit"]
        rows.append(
            {
                "bound_id": bound_id,
                "bound_name": name,
                "assumption": "K2*C_K2_unit is the solar-surface public metric P2 amplitude with standard exterior J2 radial profile",
                "J2_eff_bound": fmt(j2_bound),
                "two_epsilon_sun_surface": fmt(v["two_epsilon_sun_surface"]),
                "A_metric_bound_surface": fmt(amplitude_bound),
                "C_K2_unit": fmt(v["c_k2_unit"]),
                "K2_corrected_surface_bound": fmt(k2_bound),
                "ratio_to_internal_AX1090_K2_cap": fmt(k2_bound / v["internal_cap"]),
                "radius_profile_scaling": "multiply K2_bound by rho^-3 if the same J2 profile is evaluated at r=rho*R_sun",
                "status": status,
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def decision_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    corrected_half = v["shortcut_half_range_k2"] * v["two_epsilon_sun_surface"]
    return [
        {
            "decision_id": "D3170_0_shortcut_corrected",
            "decision": "3169 J2_eff=K2*C_K2_unit is not the correct public metric normalization",
            "evidence": "3159 metric convention gives A_metric=2 epsilon J2 rho^-3",
            "effect": "replace 3169 shortcut by J2_eff=K2*C_K2_unit*rho^3/(2 epsilon_sun_surface)",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3170_1_pressure_stronger_if_surface_profile_owned",
            "decision": "if the solar-surface J2 profile transfer is derived, the rough half-range K2 pressure is much tighter than 3169",
            "evidence": f"K2_half_range_corrected_surface={fmt(corrected_half)}",
            "effect": "local quadrupole branch is not numerically dead for K2=1 but high-K2 closure lanes would be strongly constrained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3170_2_next_target",
            "decision": "derive the radial/source-domain profile owner or demote J2-equivalent bounds to transfer-only",
            "evidence": "rho/profile/source-domain factor remains unsigned",
            "effect": "3171 should attack whether K2*C_K2_unit is actually a solar exterior J2-profile metric amplitude",
            "next_action": "3171-Y5-R2FR-K2-radial-profile-owner-or-J2-transfer-demotion-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    audits: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    source_ok = any(
        row["source_id"] == "SRC3170_0_IAU_nominal_solar_constants"
        and row["url"] == "https://arxiv.org/abs/1605.09788"
        for row in sources
    )
    epsilon_row = next(row for row in derivations if row["derivation_id"] == "JN3170_1_corrected_J2eff_map")
    epsilon_ok = 4.2e-6 < float(str(epsilon_row["two_epsilon_sun_surface"])) < 4.3e-6
    audit_ok = any(row["audit_id"] == "SA3170_0_3169_shortcut_missing_metric_factor" for row in audits)
    bounds_positive = all(float(str(row["K2_corrected_surface_bound"])) > 0.0 for row in bounds)
    stronger_than_internal = all(float(str(row["ratio_to_internal_AX1090_K2_cap"])) < 1.0 for row in bounds)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, sources, derivations, audits, bounds, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3170_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3170_1_solar_metric_factor_numeric",
            "status": "pass" if epsilon_ok else "fail",
            "detail": "2 epsilon_sun_surface is in the expected ~4.25e-6 range",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3170_1b_constant_source_recorded",
            "status": "pass" if source_ok else "fail",
            "detail": "IAU nominal solar constants source row recorded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3170_2_shortcut_audit_written",
            "status": "pass" if audit_ok else "fail",
            "detail": "3169 shortcut explicitly audited and demoted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3170_3_corrected_bounds_positive",
            "status": "pass" if bounds_positive else "fail",
            "detail": "all corrected surface bounds are positive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3170_4_corrected_bounds_tighter_than_internal",
            "status": "pass" if stronger_than_internal else "fail",
            "detail": "all corrected surface bounds sit below internal AX1090 cap",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3170_5_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3170 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    v = values()
    inputs = input_rows()
    sources = source_rows(v)
    derivations = derivation_rows(v)
    audits = audit_rows(v)
    bounds = bound_rows(v)
    decisions = decision_rows(v)
    validations = validation_rows(inputs, sources, derivations, audits, bounds, decisions)
    write_csv(INPUTS, inputs)
    write_csv(SOURCES, sources)
    write_csv(DERIVATION, derivations)
    write_csv(AUDIT, audits)
    write_csv(BOUNDS, bounds)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3170 validation failed: {failures}")


if __name__ == "__main__":
    main()
