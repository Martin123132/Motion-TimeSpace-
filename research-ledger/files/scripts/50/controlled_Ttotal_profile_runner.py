from __future__ import annotations

import csv
import math
import sys
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

CLAUSE_FIELDS = (
    "parent_action_signed",
    "same_frame_signed",
    "variation_before_readout_signed",
    "compact_support_signed",
    "volume_measure_signed",
    "positive_energy_signed",
    "poynting_once_signed",
    "no_flux_or_residual_signed",
    "no_species_prefactor_signed",
    "no_postfit_signed",
    "shared_profile_signed",
)


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
            "model_source",
            "density_source",
            "volume_source",
            "EM_source",
            "normalization_source",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def clauses_signed(row: dict[str, Any]) -> bool:
    return all(bool_text(row.get(field)) for field in CLAUSE_FIELDS)


def resolve_volume(row: dict[str, Any]) -> tuple[float | None, str]:
    volume = parse_float(row.get("volume_m3"))
    if volume is not None:
        if volume > 0:
            return volume, "VOLUME_INPUT"
        return None, "INVALID_VOLUME_INPUT"

    r_inner = parse_float(row.get("r_inner_m"))
    r_outer = parse_float(row.get("r_outer_m"))
    if r_inner is None or r_outer is None:
        return None, "MISSING_VOLUME_OR_RADII"
    if r_inner < 0 or r_outer <= r_inner:
        return None, "INVALID_SHELL_RADII"
    return (4.0 * math.pi / 3.0) * (r_outer**3 - r_inner**3), "SPHERICAL_SHELL_VOLUME"


def resolve_ttotal_density(row: dict[str, Any]) -> tuple[float | None, str]:
    explicit = parse_float(row.get("T_total_nn_J_m3"))
    if explicit is not None:
        return explicit, "T_TOTAL_NN_INPUT"

    rest_density = parse_float(row.get("rest_mass_density_kg_m3"))
    internal_energy = parse_float(row.get("internal_energy_density_J_m3")) or 0.0
    em_energy = parse_float(row.get("EM_energy_density_J_m3")) or 0.0
    radiation_energy = parse_float(row.get("radiation_energy_density_J_m3")) or 0.0
    if rest_density is None:
        return None, "MISSING_REST_MASS_OR_TTOTAL_DENSITY"

    return rest_density * C_LIGHT * C_LIGHT + internal_energy + em_energy + radiation_energy, "REST_PLUS_INTERNAL_PLUS_EM_ENERGY_DENSITY"


def compute_row(row: dict[str, Any]) -> dict[str, Any]:
    model_id = str(row.get("model_id", "")).strip() or "UNNAMED_CONTROLLED_MODEL"
    profile_id = str(row.get("profile_id", "")).strip() or model_id
    volume, volume_mode = resolve_volume(row)
    ttotal_density, ttotal_mode = resolve_ttotal_density(row)
    pressure = parse_float(row.get("pressure_Pa"))
    signed = clauses_signed(row)
    private = row_is_private(row)
    counterfactual = row_is_counterfactual(row)
    circular = forbidden_source_used(row)

    output: dict[str, Any] = {
        "model_id": model_id,
        "profile_id": profile_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
        "profile_clauses_signed": signed,
        "volume_mode": volume_mode,
        "T_total_mode": ttotal_mode,
    }

    if circular and not counterfactual:
        output.update(
            {
                "volume_m3": "MISSING_NUMERIC_VALUE",
                "T_total_nn_J_m3": "MISSING_NUMERIC_VALUE",
                "rho_H_kg_m3": "MISSING_NUMERIC_VALUE",
                "rho_H_integral_kg": "MISSING_NUMERIC_VALUE",
                "pressure_to_energy_ratio": "MISSING_NUMERIC_VALUE",
                "runner_status": "FAILED_CIRCULAR_TTOTAL_PROFILE_SOURCE",
                "anti_circularity_status": "FAIL_OBSERVED_OR_FITTED_QUANTITY_USED_AS_TTOTAL_SOURCE",
            }
        )
        return output

    if volume is None or ttotal_density is None:
        output.update(
            {
                "volume_m3": format_float(volume),
                "T_total_nn_J_m3": format_float(ttotal_density),
                "rho_H_kg_m3": "MISSING_NUMERIC_VALUE",
                "rho_H_integral_kg": "MISSING_NUMERIC_VALUE",
                "pressure_to_energy_ratio": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_CONTROLLED_TTOTAL_PROFILE_INPUTS",
                "anti_circularity_status": "PASS_NO_GM_BACKFILL",
            }
        )
        return output

    rho_h_density = ttotal_density / (C_LIGHT * C_LIGHT)
    rho_integral = rho_h_density * volume
    pressure_ratio = pressure / ttotal_density if pressure is not None and ttotal_density != 0 else None

    if ttotal_density <= 0 or rho_integral <= 0:
        runner_status = "FAILED_NONPOSITIVE_TTOTAL_PROFILE"
    elif counterfactual:
        runner_status = "CONTROLLED_TTOTAL_PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
    elif private and signed:
        runner_status = "CONTROLLED_TTOTAL_PROFILE_PRIVATE_NONCLAIM"
    elif signed:
        runner_status = "CONTROLLED_TTOTAL_PROFILE_COMPUTED_NONCLAIM"
    else:
        runner_status = "CONTROLLED_TTOTAL_PROFILE_PARENT_UNSIGNED_NONCLAIM"

    output.update(
        {
            "volume_m3": format_float(volume),
            "T_total_nn_J_m3": format_float(ttotal_density),
            "rho_H_kg_m3": format_float(rho_h_density),
            "rho_H_integral_kg": format_float(rho_integral),
            "pressure_to_energy_ratio": format_float(pressure_ratio),
            "runner_status": runner_status,
            "anti_circularity_status": "PASS_TTOTAL_PROFILE_USED_NO_GM_BACKFILL",
        }
    )
    return output


def run(input_csv: Path, output_csv: Path) -> None:
    with input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"input CSV has no rows: {input_csv}")

    outputs = [compute_row(row) for row in rows]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(outputs[0].keys()))
        writer.writeheader()
        writer.writerows(outputs)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: controlled_Ttotal_profile_runner.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
