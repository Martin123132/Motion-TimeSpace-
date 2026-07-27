from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3169_INPUTS.csv"
SOURCES = OUT / "P8_Y5_R2FR_3169_STF_SOURCE_REGISTER.csv"
TRANSFER = OUT / "P8_Y5_R2FR_3169_SOLAR_J2_EQUIVALENT_TRANSFER.csv"
BOUND = OUT / "P8_Y5_R2FR_3169_EQUIVALENT_J2_K2_BOUNDS.csv"
DECISION = OUT / "P8_Y5_R2FR_3169_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3169_VALIDATION.csv"

C_LIGHT = 299_792_458.0
GM_SUN_OVER_C2_M = 1476.0
SOLAR_J2_ADOPTED_ZK = 2.0e-7
SOLAR_J2_RANGE_LOW = 1.66e-7
SOLAR_J2_RANGE_HIGH = 2.32e-7


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
    gamma_gate = next(
        row
        for row in read_csv(OUT / "P8_Y5_R2FR_3166_K2_GAMMA_EMPIRICAL_GATE.csv")
        if row["gate_id"] == "KG3166_2_abs_2sigma_default"
    )
    return {
        "c_k2_unit": c_k2_unit,
        "internal_cap": internal_cap,
        "cassini_scalar_smoke_bound": float(gamma_gate["K2_bound_unit_projection"]),
        "j2_center": 0.5 * (SOLAR_J2_RANGE_LOW + SOLAR_J2_RANGE_HIGH),
        "j2_half_range": 0.5 * (SOLAR_J2_RANGE_HIGH - SOLAR_J2_RANGE_LOW),
        "zk_shapiro_len_m": 3.0 * SOLAR_J2_ADOPTED_ZK * GM_SUN_OVER_C2_M,
    }


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3168-Y5-R2FR-anisotropic-Shapiro-quadrupole-kernel-or-source-transfer-contract-under-AX1090.md", "3168 kernel handoff"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3168_QUADRUPOLE_GATE_CONTRACT.csv", "epsilon_quad missing gate"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3168_LOS_KERNEL_DERIVATION.csv", "line-of-sight kernel"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv", "C_K2_unit"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv", "internal K2 cap"),
    ]
    return [
        {
            "input_id": f"IN3169_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def source_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "source_id": "SRC3169_0_Zschocke_Klioner_2009",
            "role": "primary_formula_source_for_quadrupole_time_delay_upper_bound",
            "title": "The post-linear quadrupole light deflection and time delay in the field of the solar system bodies",
            "url": "https://arxiv.org/abs/0907.4318",
            "doi_or_arxiv": "arXiv:0907.4318",
            "recorded_fact": "strict upper bound for quadrupole time delay c*delta_tau_Q <= 3 J2 GM/c^2; for Sun J2=2e-7 gives about 0.89 mm",
            "numeric_value": fmt(v["zk_shapiro_len_m"]),
            "units": "m",
            "confidence": "source_backed_formula_and_scale_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "source_id": "SRC3169_1_Rozelot_2022_solar_J2_range",
            "role": "solar_J2_scale_source_for_equivalent_transfer_gate",
            "title": "The quadrupole moment of the Sun: Where are we?",
            "url": "https://arxiv.org/abs/2208.06779",
            "doi_or_arxiv": "arXiv:2208.06779",
            "recorded_fact": "reported solar oblateness/quadrupole estimates roughly J2_sun=(1.66 to 2.32)e-7 in the paper abstract/summary",
            "numeric_low": fmt(SOLAR_J2_RANGE_LOW),
            "numeric_high": fmt(SOLAR_J2_RANGE_HIGH),
            "numeric_center": fmt(v["j2_center"]),
            "numeric_half_range": fmt(v["j2_half_range"]),
            "units": "dimensionless_J2",
            "confidence": "source_backed_range_summary_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "source_id": "SRC3169_2_Kopeikin_Makarov_2007",
            "role": "supporting_STF_light_deflection_theory_source",
            "title": "Gravitational bending of light by planetary multipoles and its measurement with microarcsecond astronomical interferometers",
            "url": "https://arxiv.org/abs/0712.0417",
            "doi_or_arxiv": "arXiv:0712.0417",
            "recorded_fact": "multipolar light-deflection observables are a real STF/anisotropic channel, not the same as scalar PPN gamma",
            "numeric_value": "not_used_for_bound_in_3169",
            "units": "not_applicable",
            "confidence": "theory_support_only_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def transfer_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    c_unit = v["c_k2_unit"]
    k2_one_j2 = c_unit
    shapiro_len_k2_one = 3.0 * GM_SUN_OVER_C2_M * k2_one_j2
    return [
        {
            "transfer_id": "TR3169_0_equivalent_J2_definition",
            "quantity": "J2_eff",
            "definition": "J2_eff := K2*C_K2_unit under the solar quadrupole-normalized radial profile and source-domain transfer",
            "formula": "J2_eff = K2*C_K2_unit",
            "value_if_K2_equals_1": fmt(k2_one_j2),
            "required_for_claim": "prove MTS K2 radial profile/source-domain normalization equals solar exterior quadrupole J2 convention",
            "status": "conditional_transfer_definition_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "transfer_id": "TR3169_1_quadrupole_Shapiro_length",
            "quantity": "c_delta_tau_Q_MTS",
            "definition": "solar quadrupole-equivalent Shapiro length under Zschocke-Klioner strict envelope",
            "formula": "c_delta_tau_Q_MTS <= 3*GM_sun/c^2*K2*C_K2_unit",
            "GM_sun_over_c2_m": fmt(GM_SUN_OVER_C2_M),
            "value_if_K2_equals_1_m": fmt(shapiro_len_k2_one),
            "required_for_claim": "same radial profile plus same observable convention; otherwise this is only a transfer smoke row",
            "status": "conditional_length_map_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "transfer_id": "TR3169_2_transfer_blocker",
            "quantity": "Earth_to_solar_K2_transfer",
            "definition": "K2_solar = T_source K2_earth or independent solar-domain K2 construction",
            "formula": "T_source = MISSING_PARENT_SOURCE_DOMAIN_UNIVERSALITY",
            "required_for_claim": "source universality theorem or direct solar K2 derivation",
            "status": "transfer_missing_claim_blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    c_unit = v["c_k2_unit"]
    rows_spec = [
        (
            "JB3169_0_ZK_adopted_solar_J2_scale",
            "adopted_solar_J2_scale",
            SOLAR_J2_ADOPTED_ZK,
            "Zschocke-Klioner Sun time-delay example uses J2=2e-7",
            "scale_only_nonclaim",
        ),
        (
            "JB3169_1_Rozelot_total_high",
            "solar_J2_total_high",
            SOLAR_J2_RANGE_HIGH,
            "upper edge of reported solar J2 range; total solar quadrupole scale, not anomaly allowance",
            "total_scale_nonclaim",
        ),
        (
            "JB3169_2_Rozelot_half_range_anomaly_scale",
            "solar_J2_half_range_proxy",
            v["j2_half_range"],
            "half-width of reported J2 range as a crude anomaly pressure scale; not a covariance or formal uncertainty",
            "rough_pressure_nonclaim",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, bound_name, j2_bound, meaning, status in rows_spec:
        k2_bound = j2_bound / c_unit
        rows.append(
            {
                "bound_id": row_id,
                "bound_name": bound_name,
                "assumption": "J2_eff=K2*C_K2_unit and solar quadrupole radial/profile normalization is parent-signed",
                "J2_eff_bound": fmt(j2_bound),
                "C_K2_unit": fmt(c_unit),
                "K2_equivalent_bound": fmt(k2_bound),
                "ratio_to_internal_AX1090_K2_cap": fmt(k2_bound / v["internal_cap"]),
                "ratio_to_3166_scalar_gamma_smoke_bound": fmt(k2_bound / v["cassini_scalar_smoke_bound"]),
                "meaning": meaning,
                "status": status,
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def decision_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    half_range_bound = v["j2_half_range"] / v["c_k2_unit"]
    return [
        {
            "decision_id": "D3169_0_real_STF_source_hook_found",
            "decision": "a real quadrupole Shapiro/light-deflection source hook exists through solar J2/STF literature",
            "evidence": "SRC3169_0 and SRC3169_2",
            "effect": "epsilon_quad can be replaced by a J2-equivalent transfer gate if normalization is derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3169_1_equivalent_bound_pressure",
            "decision": "under J2_eff=K2*C_K2_unit, even a rough solar-J2 half-range proxy pressures K2 far below the internal cap",
            "evidence": f"K2_half_range_proxy={fmt(half_range_bound)}",
            "effect": "this is potentially a stronger local gate than scalar gamma smoke, but remains transfer-conditional",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3169_2_next_target",
            "decision": "derive the solar-domain K2 radial/profile normalization or refuse J2-equivalent scoring",
            "evidence": "TR3169_2 marks Earth-to-solar transfer missing",
            "effect": "3170 should attack J2_eff=K2*C_K2_unit from the metric/source-domain side, not just source more bounds",
            "next_action": "3170-Y5-R2FR-solar-domain-K2-J2eff-normalization-or-refusal-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    sources: list[dict[str, object]],
    transfers: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    v: dict[str, float],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    source_urls_ok = all(str(row.get("url", "")).startswith("https://") for row in sources)
    zschocke_len = next(row for row in sources if row["source_id"] == "SRC3169_0_Zschocke_Klioner_2009")
    zschocke_ok = 0.00088 <= float(str(zschocke_len["numeric_value"])) <= 0.00089
    bound_positive = all(float(str(row["K2_equivalent_bound"])) > 0.0 for row in bounds)
    stronger_than_internal = all(float(str(row["ratio_to_internal_AX1090_K2_cap"])) < 1.0 for row in bounds)
    transfer_block = any(row["status"] == "transfer_missing_claim_blocked" for row in transfers)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, sources, transfers, bounds, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3169_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3169_1_source_urls_recorded",
            "status": "pass" if source_urls_ok else "fail",
            "detail": "all external source rows have https URLs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3169_2_zschocke_shapiro_scale_reproduced",
            "status": "pass" if zschocke_ok else "fail",
            "detail": "3*J2*GM/c^2 with J2=2e-7 reproduces about 0.89 mm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3169_3_equivalent_bounds_positive",
            "status": "pass" if bound_positive else "fail",
            "detail": "all equivalent-J2 K2 bounds are positive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3169_4_equivalent_bounds_tighter_than_internal",
            "status": "pass" if stronger_than_internal else "fail",
            "detail": "all equivalent-J2 transfer bounds are below internal AX1090 cap",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3169_5_transfer_block_retained",
            "status": "pass" if transfer_block else "fail",
            "detail": "source-domain normalization/transfer remains missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3169_6_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3169 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    v = values()
    inputs = input_rows()
    sources = source_rows(v)
    transfers = transfer_rows(v)
    bounds = bound_rows(v)
    decisions = decision_rows(v)
    validations = validation_rows(inputs, sources, transfers, bounds, decisions, v)
    write_csv(INPUTS, inputs)
    write_csv(SOURCES, sources)
    write_csv(TRANSFER, transfers)
    write_csv(BOUND, bounds)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3169 validation failed: {failures}")


if __name__ == "__main__":
    main()
