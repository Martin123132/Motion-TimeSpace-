from __future__ import annotations

import csv
import math
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any


C_LIGHT = 299_792_458.0

FORBIDDEN_SOURCE_TOKENS = (
    "ORBITAL_GM_DEFINITION",
    "GM_AS_SOURCE",
    "FITTED_ACCELERATION",
    "OBSERVED_GM_SOURCE",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
    "PPN_FIT_AS_SOURCE",
    "CLOCK_CALIBRATION_AS_SOURCE",
    "R10_BOUND_AS_SOURCE",
)

REQUIRED_RESIDUALS = (
    "R_eq_abs_kg",
    "B_zero_abs_kg",
    "boundary_flux_abs_kg",
    "open_EM_abs_kg",
    "nonEM_owner_gap_abs_kg",
    "projector_comm_abs_kg",
    "domain_shadow_abs_kg",
    "kappa_drift_abs_kg",
)

RESIDUAL_ALIASES = {
    "R_EQ": "R_eq_abs_kg",
    "REQ": "R_eq_abs_kg",
    "B_ZERO": "B_zero_abs_kg",
    "BZERO": "B_zero_abs_kg",
    "BOUNDARY_FLUX": "boundary_flux_abs_kg",
    "BOUNDARY": "boundary_flux_abs_kg",
    "OPEN_EM": "open_EM_abs_kg",
    "OPENEM": "open_EM_abs_kg",
    "NONEM_OWNER_GAP": "nonEM_owner_gap_abs_kg",
    "NONEM": "nonEM_owner_gap_abs_kg",
    "PROJECTOR_COMM": "projector_comm_abs_kg",
    "PROJECTOR": "projector_comm_abs_kg",
    "DOMAIN_SHADOW": "domain_shadow_abs_kg",
    "DOMAIN": "domain_shadow_abs_kg",
    "KAPPA_DRIFT": "kappa_drift_abs_kg",
    "KAPPA": "kappa_drift_abs_kg",
}


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE"}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def row_is_counterfactual(row: dict[str, Any]) -> bool:
    text = str(row.get("row_status", "")).strip().lower()
    return text.startswith("counterfactual") or "counterfactual" in text


def row_is_private(row: dict[str, Any]) -> bool:
    text = str(row.get("row_status", "")).strip().lower()
    return text.startswith("private") or "private" in text


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in (
            "source_path",
            "component_source",
            "normalization_source",
            "residual_source",
            "extraction_method",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def all_profile_clauses_signed(rows: list[dict[str, Any]]) -> bool:
    clause_fields = (
        "parent_action_signed",
        "same_frame_signed",
        "variation_before_readout_signed",
        "compact_support_signed",
        "volume_measure_signed",
        "positive_energy_signed",
        "poynting_once_signed",
        "no_flux_or_flux_row_signed",
        "no_species_prefactor_signed",
        "no_postfit_signed",
        "shared_profile_signed",
    )
    return all(all(bool_text(row.get(field)) for field in clause_fields) for row in rows)


def profile_status_text(rows: list[dict[str, Any]]) -> str:
    for row in rows:
        status = str(row.get("row_status", "")).strip()
        if status:
            return status
    return ""


def profile_is_counterfactual(rows: list[dict[str, Any]]) -> bool:
    return any(row_is_counterfactual(row) for row in rows)


def profile_is_private(rows: list[dict[str, Any]]) -> bool:
    return any(row_is_private(row) for row in rows)


def shell_volume(row: dict[str, Any]) -> tuple[float | None, str]:
    volume = parse_float(row.get("volume_m3"))
    if volume is not None:
        return volume if volume > 0 else None, "VOLUME_INPUT" if volume > 0 else "INVALID_VOLUME_INPUT"

    r_inner = parse_float(row.get("r_inner_m"))
    r_outer = parse_float(row.get("r_outer_m"))
    if r_inner is None or r_outer is None:
        return None, "MISSING_VOLUME_OR_RADII"
    if r_inner < 0 or r_outer <= r_inner:
        return None, "INVALID_SHELL_RADII"
    return (4.0 * math.pi / 3.0) * (r_outer**3 - r_inner**3), "SPHERICAL_SHELL_VOLUME"


def mass_component(row: dict[str, Any]) -> tuple[float | None, str]:
    explicit_mass = parse_float(row.get("component_mass_kg"))
    if explicit_mass is not None:
        return explicit_mass, "COMPONENT_MASS_INPUT"

    volume, volume_mode = shell_volume(row)
    if volume is None:
        return None, volume_mode

    rho_h = parse_float(row.get("rho_H_kg_m3"))
    if rho_h is not None:
        return rho_h * volume, "RHO_H_TIMES_VOLUME"

    tnn_density = parse_float(row.get("T_total_nn_J_m3"))
    c_value = parse_float(row.get("c_m_s")) or C_LIGHT
    if tnn_density is not None and c_value > 0:
        return tnn_density * volume / (c_value * c_value), "T_TOTAL_NN_VOLUME_OVER_C2"

    return None, "MISSING_MASS_DENSITY_OR_TNN"


def residual_field(row: dict[str, Any]) -> str | None:
    symbol = str(row.get("residual_symbol", "")).strip()
    if not symbol:
        return None
    normalized = symbol.upper().replace("-", "_").replace(" ", "_")
    return RESIDUAL_ALIASES.get(normalized)


def compute_profile(profile_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    counterfactual = profile_is_counterfactual(rows)
    private = profile_is_private(rows)
    clauses_signed = all_profile_clauses_signed(rows)
    circular_source = any(forbidden_source_used(row) for row in rows)
    input_valid = all(bool_text(row.get("valid_for_claim")) for row in rows)
    row_status = profile_status_text(rows)

    output: dict[str, Any] = {
        "profile_id": profile_id,
        "row_status_input": row_status,
        "input_valid_for_claim": input_valid,
        "valid_for_claim": False,
        "claim_allowed": False,
        "profile_clauses_signed": clauses_signed,
        "mass_component_count": 0,
        "residual_component_count": 0,
    }

    if circular_source and not counterfactual:
        output.update(
            {
                "rho_H_integral_kg": "MISSING_NUMERIC_VALUE",
                **{field: "MISSING_NUMERIC_VALUE" for field in REQUIRED_RESIDUALS},
                "Delta_H_abs_kg": "MISSING_NUMERIC_VALUE",
                "source_profile_mode": "FAILED_FORBIDDEN_SOURCE",
                "residual_radius_mode": "FAILED_FORBIDDEN_SOURCE",
                "runner_status": "FAILED_CIRCULAR_SOURCE_PROFILE",
                "anti_circularity_status": "FAIL_OBSERVED_OR_FITTED_QUANTITY_USED_AS_PROFILE_SOURCE",
            }
        )
        return output

    total_mass = 0.0
    mass_count = 0
    missing_mass_modes: list[str] = []
    negative_mass_present = False
    source_modes: list[str] = []
    residuals: dict[str, float] = {field: 0.0 for field in REQUIRED_RESIDUALS}
    residual_seen: set[str] = set()
    residual_count = 0

    for row in rows:
        kind = str(row.get("component_kind", "")).strip().lower()
        if kind in {"mass", "density", "tnn", "source_mass", ""}:
            mass_value, source_mode = mass_component(row)
            source_modes.append(source_mode)
            if mass_value is None:
                missing_mass_modes.append(source_mode)
                continue
            mass_count += 1
            total_mass += mass_value
            negative_mass_present = negative_mass_present or mass_value < 0
            continue

        if kind in {"residual", "radius", "residual_radius"}:
            field = residual_field(row)
            residual_value = parse_float(row.get("residual_abs_kg"))
            if field is not None and residual_value is not None:
                residuals[field] += abs(residual_value)
                residual_seen.add(field)
                residual_count += 1
            continue

    output["mass_component_count"] = mass_count
    output["residual_component_count"] = residual_count

    if mass_count == 0:
        output.update(
            {
                "rho_H_integral_kg": "MISSING_NUMERIC_VALUE",
                **{field: "MISSING_NUMERIC_VALUE" for field in REQUIRED_RESIDUALS},
                "Delta_H_abs_kg": "MISSING_NUMERIC_VALUE",
                "source_profile_mode": ";".join(sorted(set(missing_mass_modes))) or "MISSING_PROFILE_COMPONENTS",
                "residual_radius_mode": "NOT_COMPUTED_WITHOUT_PROFILE",
                "runner_status": "BLOCKED_MISSING_SOURCE_PROFILE_COMPONENTS",
                "anti_circularity_status": "PASS_NO_GM_BACKFILL",
            }
        )
        return output

    missing_residuals = [field for field in REQUIRED_RESIDUALS if field not in residual_seen]
    residual_radius = sum(residuals.values()) if not missing_residuals else None
    source_profile_mode = "+".join(sorted(set(source_modes))) if source_modes else "PROFILE_INTEGRAL_INPUT"
    if negative_mass_present and not all(bool_text(row.get("positive_energy_signed")) for row in rows):
        runner_status = "PROFILE_INTEGRAL_COMPUTED_SIGN_UNRESOLVED_NONCLAIM"
    elif missing_residuals:
        runner_status = "PROFILE_INTEGRAL_COMPUTED_RESIDUALS_MISSING_NONCLAIM"
    elif counterfactual:
        runner_status = "PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
    elif private and clauses_signed and residual_radius == 0:
        runner_status = "PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM"
    elif clauses_signed:
        runner_status = "PROFILE_INTEGRAL_AND_RADIUS_COMPUTED_NONCLAIM"
    else:
        runner_status = "PROFILE_INTEGRAL_COMPUTED_PARENT_UNSIGNED_NONCLAIM"

    output.update(
        {
            "rho_H_integral_kg": format_float(total_mass),
            **{field: format_float(residuals[field]) if field in residual_seen else "MISSING_NUMERIC_VALUE" for field in REQUIRED_RESIDUALS},
            "Delta_H_abs_kg": format_float(residual_radius),
            "source_profile_mode": source_profile_mode,
            "residual_radius_mode": "RESIDUAL_COMPONENT_SUM" if residual_radius is not None else "MISSING_" + ";".join(missing_residuals),
            "runner_status": runner_status,
            "anti_circularity_status": "PASS_PROFILE_SOURCE_USED_NO_GM_BACKFILL",
        }
    )
    return output


def run(input_csv: Path, output_csv: Path) -> None:
    with input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"input CSV has no rows: {input_csv}")

    grouped: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for row in rows:
        profile_id = str(row.get("profile_id", "")).strip() or "UNNAMED_SOURCE_PROFILE"
        grouped.setdefault(profile_id, []).append(row)

    outputs = [compute_profile(profile_id, profile_rows) for profile_id, profile_rows in grouped.items()]
    fieldnames: list[str] = []
    for output in outputs:
        for key in output:
            if key not in fieldnames:
                fieldnames.append(key)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(outputs)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: source_profile_integral_radius_runner.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
