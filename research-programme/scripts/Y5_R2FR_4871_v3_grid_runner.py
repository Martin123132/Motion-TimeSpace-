from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from Y5_R2FR_4871_v3_asymptotic_response import solve_v3_profile


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    ROOT
    / "post-checkpoint-work"
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4871_V3_ASYMPTOTIC_RESPONSE.csv"
)
CONFIGURATIONS = (
    (0.03, 1 / 3),
    (0.10, 1 / 3),
    (0.20, 1 / 3),
    (0.30, 1 / 3),
    (0.30, 1 / 12),
)
OUTER_RADII = (100.0, 200.0, 400.0)
EXTRAPOLATION_WEIGHTS = (1 / 3, -2.0, 8 / 3)


def surface_responses(
    compactness: float,
    ratio: float,
    radial_tail_1: float,
    angular_tail_1: float,
    radial_tail_3: float,
    angular_tail_3: float,
) -> tuple[float, float]:
    first_numerator = (
        3 * radial_tail_1 * ratio**2
        + 6 * radial_tail_1 * ratio
        + radial_tail_1
        + 4 * angular_tail_1
        + compactness * (6 * ratio**2 + 18 * ratio + 8)
    )
    quartic_numerator = (
        21 * radial_tail_1 * ratio**2
        + 48 * radial_tail_1 * ratio
        + radial_tail_1
        + 15 * radial_tail_3 * ratio**2
        + 30 * radial_tail_3 * ratio
        + 5 * radial_tail_3
        - 6 * angular_tail_1 * ratio**2
        - 48 * angular_tail_1 * ratio
        + 34 * angular_tail_1
        + 20 * angular_tail_3
        + compactness * (60 * ratio**2 + 180 * ratio + 80)
    )
    return (
        first_numerator / (18 * compactness * (1 + ratio)),
        -quartic_numerator / (360 * compactness * (1 + ratio)),
    )


def extrapolate(values: list[float]) -> float:
    return sum(
        weight * value
        for weight, value in zip(EXTRAPOLATION_WEIGHTS, values)
    )


def run_grid(tolerance: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for compactness, ratio in CONFIGURATIONS:
        raw = [
            solve_v3_profile(
                compactness,
                ratio,
                maximum_radius,
                tolerance,
            )
            for maximum_radius in OUTER_RADII
        ]
        keys = (
            "f_action",
            "kappa4_action",
            "q1_radial_tail",
            "q1_angular_tail",
            "q3_radial_tail",
            "q3_angular_tail",
            "l2_first_variation_q3",
        )
        extrapolated = {
            key: extrapolate([float(result[key]) for result in raw])
            for key in keys
        }
        first_surface, quartic_surface = surface_responses(
            compactness,
            ratio,
            extrapolated["q1_radial_tail"],
            extrapolated["q1_angular_tail"],
            extrapolated["q3_radial_tail"],
            extrapolated["q3_angular_tail"],
        )
        rows.append(
            {
                "row_id": f"V3_4871_C{compactness:.3f}_r{ratio:.8f}",
                "compactness": compactness,
                "ratio": ratio,
                "outer_radii": "100;200;400",
                "outer_extrapolation": "quadratic in 1/Rmax",
                "f_action_extrapolated": extrapolated["f_action"],
                "f_surface_extrapolated": first_surface,
                "f_absolute_difference": abs(
                    extrapolated["f_action"] - first_surface
                ),
                "kappa4_action_extrapolated": extrapolated[
                    "kappa4_action"
                ],
                "kappa4_surface_extrapolated": quartic_surface,
                "kappa4_absolute_difference": abs(
                    extrapolated["kappa4_action"] - quartic_surface
                ),
                "q1_radial_tail_extrapolated": extrapolated[
                    "q1_radial_tail"
                ],
                "q1_angular_tail_extrapolated": extrapolated[
                    "q1_angular_tail"
                ],
                "q3_radial_tail_extrapolated": extrapolated[
                    "q3_radial_tail"
                ],
                "q3_angular_tail_extrapolated": extrapolated[
                    "q3_angular_tail"
                ],
                "l2_first_variation_extrapolated": extrapolated[
                    "l2_first_variation_q3"
                ],
                "maximum_leading_residual": max(
                    float(result["leading_maximum_rms_residual"])
                    for result in raw
                ),
                "maximum_v3_residual": max(
                    float(result["v3_maximum_rms_residual"])
                    for result in raw
                ),
                "status": (
                    "PASS"
                    if abs(extrapolated["f_action"] - first_surface)
                    < 2.0e-6
                    and abs(
                        extrapolated["kappa4_action"] - quartic_surface
                    )
                    < 2.0e-6
                    else "FAIL"
                ),
                "valid_for_claim": False,
            }
        )
    return rows


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--tolerance", type=float, default=2.0e-7)
    arguments = parser.parse_args()
    rows = run_grid(arguments.tolerance)
    write_rows(arguments.output, rows)
    for row in rows:
        print(
            row["row_id"],
            row["kappa4_action_extrapolated"],
            row["kappa4_surface_extrapolated"],
            row["status"],
        )
    return 0 if all(row["status"] == "PASS" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
