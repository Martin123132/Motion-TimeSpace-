from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3158_INPUTS.csv"
DOMAIN = OUT / "P8_Y5_R2FR_3158_SOURCE_DOMAIN_SELECTION.csv"
SOURCES = OUT / "P8_Y5_R2FR_3158_SOURCE_VALUES.csv"
SMOKE = OUT / "P8_Y5_R2FR_3158_REVERSE_CAP_NUMERIC_SMOKE.csv"
DECISION = OUT / "P8_Y5_R2FR_3158_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3158_VALIDATION.csv"


CAP_SINGLE = 5.970964001482571e-4
CAP_EQUAL = 9.951606669137618e-5

C = 299_792_458.0
AU_M = 149_597_870_700.0
GM_SUN_M3_S2 = 1.32712440041279419e20
GM_EARTH_M3_S2 = 398_600.435507e9
GM_MOON_M3_S2 = 4_902.800118e9
R_EARTH_EQ_M = 6_378.1366e3
MOON_DISTANCE_M = 384_400e3
C20_ZT = -0.48416948e-3


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def fmt(value: float) -> str:
    return f"{value:.15e}"


def internal(path: str) -> str:
    return str((ROOT / path).resolve())


def source_rows() -> list[dict[str, object]]:
    now = stamp()
    j2 = math.sqrt(5.0) * abs(C20_ZT)
    epsilon_g = GM_EARTH_M3_S2 / (C * C * R_EARTH_EQ_M)
    moon_tide_norm = 2.0 * GM_MOON_M3_S2 / (MOON_DISTANCE_M**3)
    sun_tide_norm = 2.0 * GM_SUN_M3_S2 / (AU_M**3)
    return [
        {
            "value_id": "SV3158_0_speed_of_light",
            "quantity": "c",
            "value": fmt(C),
            "units": "m s^-1",
            "role": "SI light speed for dimensionless weak-field reductions",
            "source_url": "https://ssd.jpl.nasa.gov/astro_par.html",
            "source_line_ref": "lines 91-95",
            "extraction_method": "JPL astrodynamic parameter table",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_1_earth_GM",
            "quantity": "GM_Earth",
            "value": fmt(GM_EARTH_M3_S2),
            "units": "m^3 s^-2",
            "role": "Earth monopole in epsilon_G",
            "source_url": "https://ssd.jpl.nasa.gov/astro_par.html",
            "source_line_ref": "lines 103-109, DE440 planetary GM table",
            "extraction_method": "converted 398600.435507 km^3 s^-2 to SI",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_2_earth_equatorial_radius",
            "quantity": "R_Earth_equatorial",
            "value": fmt(R_EARTH_EQ_M),
            "units": "m",
            "role": "source radius and evaluation radius for equatorial exterior shell",
            "source_url": "https://ssd.jpl.nasa.gov/planets/phys_par.html",
            "source_line_ref": "lines 121-123",
            "extraction_method": "converted 6378.1366 km to SI",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_3_C20_zero_tide",
            "quantity": "Cbar20_zero_tide",
            "value": fmt(C20_ZT),
            "units": "dimensionless fully_normalized",
            "role": "conventional geopotential source for J2 smoke value",
            "source_url": "https://iers-conventions.obspm.fr/content/chapter6/icc6.pdf",
            "source_line_ref": "lines 93-97",
            "extraction_method": "IERS Table 6.2 Cbar20 zero-tide coefficient",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_4_J2_from_C20",
            "quantity": "J2",
            "value": fmt(j2),
            "units": "dimensionless",
            "role": "derived J2 for first reverse cap smoke",
            "source_url": "https://iers-conventions.obspm.fr/content/chapter6/icc6.pdf",
            "source_line_ref": "derived as J2=sqrt(5)*abs(Cbar20_zero_tide)",
            "extraction_method": "fully-normalized zonal conversion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_5_epsilon_G",
            "quantity": "epsilon_G_Earth_equator",
            "value": fmt(epsilon_g),
            "units": "dimensionless",
            "role": "GM_Earth/(c^2 R_Earth_equatorial)",
            "source_url": "derived_from_SV3158_0_SV3158_1_SV3158_2",
            "source_line_ref": "derived",
            "extraction_method": "direct weak-field compactness calculation",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_6_moon_GM",
            "quantity": "GM_Moon",
            "value": fmt(GM_MOON_M3_S2),
            "units": "m^3 s^-2",
            "role": "lunar tide source",
            "source_url": "https://ssd.jpl.nasa.gov/astro_par.html",
            "source_line_ref": "lines 103-109, DE440 planetary GM table",
            "extraction_method": "converted 4902.800118 km^3 s^-2 to SI",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_7_moon_distance",
            "quantity": "Earth_Moon_average_distance",
            "value": fmt(MOON_DISTANCE_M),
            "units": "m",
            "role": "smoke-domain lunar tide distance",
            "source_url": "https://spaceplace.nasa.gov/moon-distance/en/",
            "source_line_ref": "lines 17-24",
            "extraction_method": "converted 384400 km to SI",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_8_lunar_radial_tide",
            "quantity": "E_moon_radial_eigenvalue",
            "value": fmt(moon_tide_norm),
            "units": "s^-2",
            "role": "2 GM_Moon/d_Moon^3 radial eigenvalue magnitude",
            "source_url": "derived_from_SV3158_6_SV3158_7",
            "source_line_ref": "derived",
            "extraction_method": "Newtonian electric tidal tensor radial eigenvalue",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "value_id": "SV3158_9_solar_radial_tide",
            "quantity": "E_sun_radial_eigenvalue",
            "value": fmt(sun_tide_norm),
            "units": "s^-2",
            "role": "2 GM_Sun/AU^3 radial eigenvalue magnitude",
            "source_url": "https://ssd.jpl.nasa.gov/astro_par.html",
            "source_line_ref": "lines 91-100",
            "extraction_method": "Newtonian electric tidal tensor radial eigenvalue using JPL GM_sun and au",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    inputs = [
        "3157-Y5-R2FR-LWlambda-factor-or-first-source-domain-multipole-fill-under-AX1090.md",
        "source-intake/mts_residuals/P8_Y5_R2FR_3157_REVERSE_SOURCE_CAPS.csv",
        "source-intake/mts_residuals/P8_Y5_R2FR_3156_FIRST_MULTIPOLE_CAP_CONTRACT.csv",
        "000-private-fork-heuristics-for-martin-style-search.md",
    ]
    return [
        {
            "input_id": f"IN3158_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(
            zip(
                inputs,
                [
                    "3157 product/reverse cap contract",
                    "symbolic reverse cap formulas",
                    "3156 AX1090 inherited cap constants",
                    "private time-flow fork heuristic, non-theorem",
                ],
                strict=True,
            )
        )
    ]


def domain_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "domain_id": "DOM3158_0_earth_equatorial_exterior_shell",
            "domain": "Earth equatorial exterior shell at R=R_Earth_equatorial",
            "why_selected": "J2, GM, and radius are public source-backed values and directly match the 3156 quadrupole reverse cap",
            "primary_component": "Earth J2 quadrupole",
            "secondary_component": "Sun+Moon radial tidal eigenvalue smoke comparison",
            "excluded_component": "spin/frame dragging",
            "exclusion_reason": "requires a separate source-backed Earth angular momentum or inertia convention before use",
            "claim_status": "nonclaim_smoke_domain_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def smoke_rows(values: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    epsilon_g = values["epsilon_G_Earth_equator"]
    j2 = values["J2"]
    radius = values["R_Earth_equatorial"]
    lunar_tide = values["E_moon_radial_eigenvalue"]
    solar_tide = values["E_sun_radial_eigenvalue"]
    j2_component = epsilon_g * j2
    moon_component = lunar_tide * radius * radius / (C * C)
    sun_component = solar_tide * radius * radius / (C * C)
    tide_component = moon_component + sun_component
    rows = [
        {
            "smoke_id": "RC3158_0_J2_unit_C2",
            "component": "Earth_J2_quadrupole",
            "dimensionless_B_component_per_unit_coefficient": fmt(j2_component),
            "single_cap_required_LWlambda_per_unit_coefficient": fmt(CAP_SINGLE / j2_component),
            "equal_cap_required_LWlambda_per_unit_coefficient": fmt(CAP_EQUAL / j2_component),
            "formula_used": "B_J2_per_C2 = epsilon_G * |J2| * (R_body/R)^2 with R_body/R=1",
            "interpretation": "for C2=1 diagnostic, Earth J2 is far below AX1090 cap unless L_Wphys_Lambda is very large",
            "missing_for_claim": "C2 angular/projection coefficient; parent-owned L_Wphys_Lambda; same norm convention",
            "status": "numeric_reverse_cap_smoke_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "smoke_id": "RC3158_1_lunar_tide_unit_Ctide",
            "component": "Moon_radial_tide",
            "dimensionless_B_component_per_unit_coefficient": fmt(moon_component),
            "single_cap_required_LWlambda_per_unit_coefficient": fmt(CAP_SINGLE / moon_component),
            "equal_cap_required_LWlambda_per_unit_coefficient": fmt(CAP_EQUAL / moon_component),
            "formula_used": "B_tide_per_Ctide = (2 GM_Moon/d_Moon^3) R^2/c^2",
            "interpretation": "lunar tide is weaker than the Earth J2 quadrupole in this local cap smoke",
            "missing_for_claim": "Ctide projection coefficient; frame convention; parent-owned L_Wphys_Lambda",
            "status": "numeric_reverse_cap_smoke_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "smoke_id": "RC3158_2_solar_tide_unit_Ctide",
            "component": "Sun_radial_tide",
            "dimensionless_B_component_per_unit_coefficient": fmt(sun_component),
            "single_cap_required_LWlambda_per_unit_coefficient": fmt(CAP_SINGLE / sun_component),
            "equal_cap_required_LWlambda_per_unit_coefficient": fmt(CAP_EQUAL / sun_component),
            "formula_used": "B_tide_per_Ctide = (2 GM_Sun/AU^3) R^2/c^2",
            "interpretation": "solar tide is also far below the AX1090 cap for unit projection coefficient",
            "missing_for_claim": "Ctide projection coefficient; ephemeris phase/domain convention; parent-owned L_Wphys_Lambda",
            "status": "numeric_reverse_cap_smoke_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "smoke_id": "RC3158_3_sun_moon_combined_tide_unit_Ctide",
            "component": "Sun_plus_Moon_radial_tide_upper_smoke",
            "dimensionless_B_component_per_unit_coefficient": fmt(tide_component),
            "single_cap_required_LWlambda_per_unit_coefficient": fmt(CAP_SINGLE / tide_component),
            "equal_cap_required_LWlambda_per_unit_coefficient": fmt(CAP_EQUAL / tide_component),
            "formula_used": "B_tide_sum_per_Ctide = (E_moon+E_sun) R^2/c^2 using radial eigenvalue magnitudes",
            "interpretation": "even combined Sun+Moon radial tide smoke gives a loose reverse ceiling compared with J2",
            "missing_for_claim": "Ctide projection coefficient; tensor norm convention; phase/domain convention; parent-owned L_Wphys_Lambda",
            "status": "numeric_reverse_cap_smoke_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]
    rows.sort(key=lambda row: float(row["single_cap_required_LWlambda_per_unit_coefficient"]))
    return rows


def decision_rows(smoke: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    strongest = smoke[0]
    return [
        {
            "decision_id": "D3158_0_first_domain_result",
            "decision": "Earth equatorial exterior J2 is the tightest of the first source-domain smoke rows",
            "evidence": strongest["smoke_id"],
            "effect": "the first sourced local source-domain does not force L_Wphys_Lambda to be tiny for unit projection coefficients",
            "next_action": "derive C2/Ctide and L_Wphys_Lambda in the same norm convention, then rerun as a real gate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3158_1_coupling_lesson",
            "decision": "the coupling problem is not yet a numerical Earth-J2 blow-up; it is a derivation/normalization problem",
            "evidence": "all reverse ceilings remain large under C2=Ctide=1 smoke diagnostics",
            "effect": "push next toward parent-owned projection coefficients rather than another abstract missing ledger",
            "next_action": "3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(inputs: list[dict[str, object]], sources: list[dict[str, object]], smoke: list[dict[str, object]], decisions: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    numeric_source_ok = True
    for row in sources:
        try:
            value = float(str(row["value"]))
        except ValueError:
            numeric_source_ok = False
            continue
        if row["quantity"] != "Cbar20_zero_tide" and value <= 0:
            numeric_source_ok = False
    j2_row = next(row for row in sources if row["quantity"] == "J2")
    c20_row = next(row for row in sources if row["quantity"] == "Cbar20_zero_tide")
    j2_ok = math.isclose(float(j2_row["value"]), math.sqrt(5.0) * abs(float(c20_row["value"])), rel_tol=1e-12)
    smoke_ok = all(
        float(str(row["dimensionless_B_component_per_unit_coefficient"])) > 0.0
        and float(str(row["single_cap_required_LWlambda_per_unit_coefficient"])) > 0.0
        and float(str(row["equal_cap_required_LWlambda_per_unit_coefficient"])) > 0.0
        for row in smoke
    )
    no_claim = all(str(row.get("valid_for_claim", "")).lower() == "false" for rows in [inputs, sources, smoke, decisions] for row in rows)
    return [
        {
            "check_id": "V3158_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3158_1_source_values_numeric",
            "status": "pass" if numeric_source_ok else "fail",
            "detail": "all source/derived values numeric with only Cbar20 allowed negative",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3158_2_J2_conversion",
            "status": "pass" if j2_ok else "fail",
            "detail": "J2=sqrt(5)*abs(Cbar20_zero_tide)",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3158_3_reverse_caps_positive",
            "status": "pass" if smoke_ok else "fail",
            "detail": "all B components and reverse ceilings positive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3158_4_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "every 3158 row valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    sources = source_rows()
    values = {str(row["quantity"]): float(str(row["value"])) for row in sources}
    inputs = input_rows()
    domain = domain_rows()
    smoke = smoke_rows(values)
    decisions = decision_rows(smoke)
    validations = validation_rows(inputs, sources, smoke, decisions)
    write_csv(INPUTS, inputs)
    write_csv(DOMAIN, domain)
    write_csv(SOURCES, sources)
    write_csv(SMOKE, smoke)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3158 validation failed: {failures}")


if __name__ == "__main__":
    main()
