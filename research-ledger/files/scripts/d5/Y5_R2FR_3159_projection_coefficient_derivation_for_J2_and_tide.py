from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3159_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3159_PROJECTION_COEFFICIENT_DERIVATION.csv"
NUMERIC = OUT / "P8_Y5_R2FR_3159_NUMERIC_REVERSE_CAP_WITH_DERIVED_COEFFICIENTS.csv"
GATES = OUT / "P8_Y5_R2FR_3159_GATE_STATUS.csv"
DECISION = OUT / "P8_Y5_R2FR_3159_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3159_VALIDATION.csv"

CAP_SINGLE = 5.970964001482571e-4
CAP_EQUAL = 9.951606669137618e-5


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fmt(value: float) -> str:
    return f"{value:.15e}"


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_value(quantity: str) -> float:
    rows = read_csv(OUT / "P8_Y5_R2FR_3158_SOURCE_VALUES.csv")
    for row in rows:
        if row.get("quantity") == quantity:
            return float(row["value"])
    raise KeyError(f"missing 3158 source quantity {quantity}")


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "3158-Y5-R2FR-first-source-domain-selection-and-reverse-cap-smoke-under-AX1090.md",
            "3158 source-domain selection and smoke result",
        ),
        (
            "source-intake/mts_residuals/P8_Y5_R2FR_3158_SOURCE_VALUES.csv",
            "source-backed Earth/tide values",
        ),
        (
            "source-intake/mts_residuals/P8_Y5_R2FR_3158_REVERSE_CAP_NUMERIC_SMOKE.csv",
            "unit-coefficient reverse-cap smoke rows",
        ),
        (
            "source-intake/mts_residuals/P8_Y5_R2FR_3157_LWLAMBDA_PRODUCT_CONTRACT.csv",
            "unresolved product contract",
        ),
    ]
    return [
        {
            "input_id": f"IN3159_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def derivation_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "derivation_id": "PC3159_0_metric_projection_map",
            "object": "weak_field_metric_projection",
            "assumption": "local weak-field GR/PPN-gamma=1 projection used only as a coefficient map",
            "derivation": "g00=-(1+2 Phi/c^2)+O(Phi^2); gij=(1-2 Phi/c^2) delta_ij+O(Phi^2)",
            "coefficient_result": "metric perturbation amplitude carries factor 2 relative to potential Phi/c^2",
            "numeric_coefficient": fmt(2.0),
            "scope": "coefficient derivation, not MTS local-GR proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "PC3159_1_J2_full_shell_sup",
            "object": "C2_full_shell_sup_norm",
            "assumption": "Phi_J2=(GM/R) J2 (R_body/R)^2 P2(cos theta), max_shell |P2|=1",
            "derivation": "B_metric=max |2 Phi_J2/c^2| = 2 epsilon_G |J2| (R_body/R)^2",
            "coefficient_result": "C2_full_shell=2",
            "numeric_coefficient": fmt(2.0),
            "scope": "conservative full-angular-shell metric-component sup norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "PC3159_2_J2_equatorial_point",
            "object": "C2_equatorial_point",
            "assumption": "local equatorial point theta=pi/2, P2(0)=-1/2",
            "derivation": "B_metric=|2 epsilon_G J2 P2(0)| = epsilon_G |J2|",
            "coefficient_result": "C2_equatorial=1",
            "numeric_coefficient": fmt(1.0),
            "scope": "local equatorial lab/readout point, not full-shell safety norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "PC3159_3_tide_spectral_metric_projection",
            "object": "Ctide_spectral_norm",
            "assumption": "Phi_tide=-1/2 E_ij x^i x^j and ||E|| is the spectral norm/radial eigenvalue magnitude",
            "derivation": "h00=2 Phi_tide/c^2=-E_ij x^i x^j/c^2, so |h00| <= ||E|| R^2/c^2",
            "coefficient_result": "Ctide_spectral=1",
            "numeric_coefficient": fmt(1.0),
            "scope": "Newtonian electric tidal tensor in local public frame",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "PC3159_4_norm_warning",
            "object": "projection_convention_warning",
            "assumption": "3156 cap is a metric-component product cap",
            "derivation": "using potential-only norms would halve J2 and tide coefficients; using full metric component norms keeps C2=2/full-shell or 1/equator and Ctide=1",
            "coefficient_result": "do not mix potential-only and metric-component conventions",
            "numeric_coefficient": "not_applicable",
            "scope": "guard against normalization cheating",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def numeric_rows(values: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    epsilon_g = values["epsilon_G_Earth_equator"]
    j2 = values["J2"]
    radius = values["R_Earth_equatorial"]
    light_speed = values["c"]
    lunar_tide = values["E_moon_radial_eigenvalue"]
    solar_tide = values["E_sun_radial_eigenvalue"]

    base_j2 = epsilon_g * abs(j2)
    base_moon = lunar_tide * radius * radius / (light_speed * light_speed)
    base_sun = solar_tide * radius * radius / (light_speed * light_speed)
    base_tide_sum = base_moon + base_sun

    variants = [
        (
            "NB3159_0_J2_equatorial_metric",
            "Earth_J2_equatorial_metric_projection",
            base_j2,
            1.0,
            "C2_equatorial=1 from 2|P2(0)|",
            "least conservative local equatorial readout",
        ),
        (
            "NB3159_1_J2_full_shell_metric",
            "Earth_J2_full_shell_metric_projection",
            base_j2,
            2.0,
            "C2_full_shell=2 from 2 max|P2|",
            "conservative full angular shell metric-component sup norm",
        ),
        (
            "NB3159_2_moon_tide_spectral_metric",
            "Moon_tide_metric_projection",
            base_moon,
            1.0,
            "Ctide=1 from |E_ij x^i x^j| <= ||E|| R^2",
            "lunar tide spectral/radial eigenvalue convention",
        ),
        (
            "NB3159_3_sun_tide_spectral_metric",
            "Sun_tide_metric_projection",
            base_sun,
            1.0,
            "Ctide=1 from |E_ij x^i x^j| <= ||E|| R^2",
            "solar tide spectral/radial eigenvalue convention",
        ),
        (
            "NB3159_4_sun_moon_tide_spectral_metric",
            "Sun_plus_Moon_tide_metric_projection",
            base_tide_sum,
            1.0,
            "Ctide=1 applied to summed radial-eigenvalue smoke upper value",
            "combined tide smoke diagnostic",
        ),
    ]

    rows: list[dict[str, object]] = []
    for row_id, component, base_component, coefficient, formula, interpretation in variants:
        projected = base_component * coefficient
        rows.append(
            {
                "bound_id": row_id,
                "component": component,
                "base_dimensionless_component": fmt(base_component),
                "derived_projection_coefficient": fmt(coefficient),
                "projected_B_metric": fmt(projected),
                "single_cap_required_LWlambda": fmt(CAP_SINGLE / projected),
                "equal_cap_required_LWlambda": fmt(CAP_EQUAL / projected),
                "formula_used": formula,
                "interpretation": interpretation,
                "remaining_missing_for_claim": "parent-owned L_Wphys_Lambda; exact MTS-to-public metric map; same S/norm convention",
                "status": "derived_projection_numeric_gate_nonclaim",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    rows.sort(key=lambda row: float(str(row["single_cap_required_LWlambda"])))
    return rows


def gate_rows(numeric: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    tightest = numeric[0]
    return [
        {
            "gate_id": "G3159_0_C2_derived",
            "gate": "C2 weak-field metric projection",
            "status": "pass_nonclaim",
            "detail": "C2=1 for local equatorial point; C2=2 for full angular shell sup norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3159_1_Ctide_derived",
            "gate": "Ctide weak-field spectral projection",
            "status": "pass_nonclaim",
            "detail": "Ctide=1 when E_ext is the spectral norm/radial eigenvalue magnitude",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3159_2_tightest_numeric_ceiling",
            "gate": "tightest first-domain reverse ceiling",
            "status": "pass_nonclaim",
            "detail": f"{tightest['component']} requires L_Wphys_Lambda <= {tightest['single_cap_required_LWlambda']} under the single cap",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3159_3_parent_product_missing",
            "gate": "parent L_Wphys_Lambda derivation",
            "status": "fail_for_claim",
            "detail": "L_Wphys_Lambda is still not parent-derived or source-bounded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3159_4_local_GR_claim",
            "gate": "local GR/Newton/PPN claim",
            "status": "blocked_for_claim",
            "detail": "projection coefficients are not enough without the MTS-to-public metric map and product bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(numeric: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    tightest = numeric[0]
    return [
        {
            "decision_id": "D3159_0_coefficient_result",
            "decision": "C2 and Ctide are no longer free knobs under the selected weak-field metric projection",
            "evidence": "C2=1 equatorial, C2=2 full shell, Ctide=1 spectral",
            "effect": "3158 reverse caps become coefficient-derived numeric ceilings",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3159_1_tightest_local_domain",
            "decision": "conservative full-shell Earth J2 is the tightest first-domain row",
            "evidence": tightest["bound_id"],
            "effect": f"single-cap ceiling is L_Wphys_Lambda <= {tightest['single_cap_required_LWlambda']}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3159_2_next_attack",
            "decision": "move from coefficient derivation to parent product derivation or bound",
            "evidence": "G3159_3_parent_product_missing",
            "effect": "next checkpoint should derive/bound L_Wphys_Lambda itself using Wbar derivative/Hodge primitive route",
            "next_action": "3160-Y5-R2FR-LWphysLambda-parent-product-bound-or-zero-theorem-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    derivations: list[dict[str, object]],
    numeric: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    coefficients = {
        row["object"]: row["numeric_coefficient"]
        for row in derivations
        if row["numeric_coefficient"] != "not_applicable"
    }
    coeff_ok = (
        math.isclose(float(str(coefficients["C2_full_shell_sup_norm"])), 2.0)
        and math.isclose(float(str(coefficients["C2_equatorial_point"])), 1.0)
        and math.isclose(float(str(coefficients["Ctide_spectral_norm"])), 1.0)
    )
    numeric_ok = all(
        float(str(row["projected_B_metric"])) > 0.0
        and float(str(row["single_cap_required_LWlambda"])) > 0.0
        and float(str(row["equal_cap_required_LWlambda"])) > 0.0
        for row in numeric
    )
    tightest_ok = numeric[0]["component"] == "Earth_J2_full_shell_metric_projection"
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, derivations, numeric, gates, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3159_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3159_1_coefficients_derived",
            "status": "pass" if coeff_ok else "fail",
            "detail": "C2_full_shell=2, C2_equatorial=1, Ctide=1",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3159_2_numeric_bounds_positive",
            "status": "pass" if numeric_ok else "fail",
            "detail": "all projected B metrics and reverse ceilings positive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3159_3_tightest_row_expected",
            "status": "pass" if tightest_ok else "fail",
            "detail": str(numeric[0]["component"]),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3159_4_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3159 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    values = {
        "c": source_value("c"),
        "GM_Earth": source_value("GM_Earth"),
        "R_Earth_equatorial": source_value("R_Earth_equatorial"),
        "J2": source_value("J2"),
        "epsilon_G_Earth_equator": source_value("epsilon_G_Earth_equator"),
        "E_moon_radial_eigenvalue": source_value("E_moon_radial_eigenvalue"),
        "E_sun_radial_eigenvalue": source_value("E_sun_radial_eigenvalue"),
    }
    inputs = input_rows()
    derivations = derivation_rows()
    numeric = numeric_rows(values)
    gates = gate_rows(numeric)
    decisions = decision_rows(numeric)
    validations = validation_rows(inputs, derivations, numeric, gates, decisions)
    write_csv(INPUTS, inputs)
    write_csv(DERIVATION, derivations)
    write_csv(NUMERIC, numeric)
    write_csv(GATES, gates)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3159 validation failed: {failures}")


if __name__ == "__main__":
    main()
