from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5228"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5226 = (
    POST / "scripts" / "Y5_R2FR_5226_physical_permutation_chart_bijection.py"
)
SCRIPT_5227 = (
    POST / "scripts" / "Y5_R2FR_5227_bounded_paired_partition_A00_replay.py"
)
RESULT_5226 = (
    FUNCTIONAL_RG / "5226" / "physical_permutation_chart_bijection_results.json"
)
RESULT_5227 = (
    FUNCTIONAL_RG / "5227" / "bounded_paired_partition_A00_results.json"
)
VALIDATION_5227 = RESIDUALS / "P8_Y5_BRR545_5227_VALIDATION.csv"

ROWS = SOURCE / "cross_sector_soft_boundary_scaling.csv"
RESULT = SOURCE / "one_chart_cross_sector_blend_no_go.json"
DOCUMENT = POST / "5228-Y5-R2FR-one-chart-cross-sector-blend-no-go.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5228_VALIDATION.csv"

MARKER = "MTS_5228_ONE_CHART_CROSS_SECTOR_BLEND_NO_GO"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
LAMBDA_VALUES = (1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4)
SLOPE_TOLERANCE = 0.05


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5226 = load_module(SCRIPT_5226, "mts_5226_for_5228")
M5227 = load_module(SCRIPT_5227, "mts_5227_for_5228")
M5017 = M5227.M5026.M5017


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def validation_all_pass(path: Path) -> bool:
    with path.open(newline="", encoding="utf-8") as handle:
        return all(
            row["passed"].strip().lower() == "true"
            for row in csv.DictReader(handle)
        )


def logarithmic_slope(rows: list[dict[str, Any]], field: str) -> float:
    selected = rows[-4:]
    coordinates = np.log([float(row["lambda"]) for row in selected])
    values = np.log([float(row[field]) for row in selected])
    return float(np.polyfit(coordinates, values, 1)[0])


def scaling_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for soft_energy in LAMBDA_VALUES:
        source_coordinates = np.asarray(
            [soft_energy, 0.23, 0.41, -0.31, 1.13],
            dtype=np.float64,
        )
        source_momenta = M5226.sequential_three_body(source_coordinates)
        internal = np.asarray(
            [source_momenta[2], source_momenta[1], source_momenta[0]],
            dtype=np.complex128,
        )
        energies = np.real(internal[:, 0])
        inverse_squares = energies**-2
        weights = inverse_squares / float(np.sum(inverse_squares))
        amplitude = (
            M5017.hhh_reduced_product(
                internal, complex(-0.6, 0.04), 1.0
            )
            / (M5017.S_VALUE * M5017.S_VALUE)
        )
        original_multiplier = 3.0 * weights[2]
        paired_multiplier = 1.5 * (weights[2] + weights[0])
        rows.append(
            {
                "lambda": soft_energy,
                "energy_1": float(energies[0]),
                "energy_2": float(energies[1]),
                "energy_3": float(energies[2]),
                "w_1": float(weights[0]),
                "w_3": float(weights[2]),
                "absolute_A": abs(amplitude),
                "absolute_W3_A": abs(original_multiplier * amplitude),
                "absolute_W13_A": abs(paired_multiplier * amplitude),
                "lambda_squared_absolute_A": (
                    soft_energy * soft_energy * abs(amplitude)
                ),
                "original_multiplier": float(original_multiplier),
                "paired_multiplier": float(paired_multiplier),
            }
        )
    return rows


def main() -> None:
    required = [
        Path(__file__).resolve(),
        SCRIPT_5226,
        SCRIPT_5227,
        RESULT_5226,
        RESULT_5227,
        VALIDATION_5227,
    ]
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    result_5227 = read_json(RESULT_5227)
    if not (
        result_5227["state"] == "COMPLETE_RETROSPECTIVE_REPLAY"
        and result_5227["decision"]
        == "REJECT_PAIRED_PARTITION_SCALE_WITHOUT_NEW_DERIVATION"
        and result_5227["validation_all_passed"]
        and validation_all_pass(VALIDATION_5227)
    ):
        raise RuntimeError("checkpoint-5227 rejection chain is not closed")

    rows = scaling_rows()
    write_csv(ROWS, rows)
    amplitude_slope = logarithmic_slope(rows, "absolute_A")
    original_slope = logarithmic_slope(rows, "absolute_W3_A")
    paired_slope = logarithmic_slope(rows, "absolute_W13_A")
    plateau = np.asarray(
        [float(row["lambda_squared_absolute_A"]) for row in rows[-4:]]
    )
    plateau_ratio = float(np.max(plateau) / np.min(plateau))
    formal_digest = M5227.tree_digest(FORMAL)

    theorem = {
        "boundary": "energy_1=lambda->0 with energy_2,energy_3=O(1)",
        "partition_limits": {
            "w_1": "1+O(lambda^2)",
            "w_3": "lambda^2/energy_3^2+O(lambda^4)",
        },
        "kernel_limit": "A_hhh=O(lambda^-2)",
        "original_sector": (
            "W3*A=3*w3*A=O(1), preserving the slot-3 chart's "
            "off-sector soft suppression"
        ),
        "constant_cross_sector_mixture": (
            "for W_beta=3*((1-beta)*w3+beta*w1), every constant "
            "beta!=0 gives W_beta*A=O(lambda^-2)"
        ),
        "mean_measure_test": (
            "dPhi3 contains lambda*d(lambda); therefore the mixed "
            "absolute contribution scales as d(lambda)/lambda"
        ),
        "second_moment_test": (
            "the mixed square scales as d(lambda)/lambda^3, so a "
            "finite second moment is impossible without an additional "
            "slot-1 subtraction or native chart"
        ),
        "admissibility_condition": (
            "any slot-1 contamination used in a slot-3 one-soft chart "
            "must vanish faster than lambda^(1+delta) for finite second "
            "moment; the sector weight's O(lambda^2) suppression is safe"
        ),
        "scope": (
            "closes nonzero constant cross-sector mixtures, including "
            "W13 and the pointwise full-S3 constant-weight shortcut; it "
            "does not forbid native multi-chart averaging"
        ),
    }
    result = {
        "checkpoint": 5228,
        "checkpoint_marker": MARKER,
        "decision": (
            "REJECT_NONZERO_CONSTANT_CROSS_SECTOR_MIXTURES_IN_ONE_"
            "SOFT_CHART"
        ),
        "theorem": theorem,
        "numerical_spot_check": {
            "lambda_values": list(LAMBDA_VALUES),
            "fit_uses_smallest_four_values": True,
            "amplitude_log_slope": amplitude_slope,
            "original_W3_A_log_slope": original_slope,
            "paired_W13_A_log_slope": paired_slope,
            "lambda_squared_amplitude_plateau_ratio": plateau_ratio,
            "expected_slopes": {
                "amplitude": -2.0,
                "original_W3_A": 0.0,
                "paired_W13_A": -2.0,
            },
        },
        "checkpoint_5227_observation": {
            "A00_standard_deviation_ratio": result_5227["analysis"][
                "A00_real_standard_deviation_ratio"
            ],
            "local_standard_deviation_ratio": result_5227["analysis"][
                "local_real_standard_deviation_ratio"
            ],
            "mean_difference_standard_errors": result_5227["analysis"][
                "difference_mean_in_standard_errors"
            ],
        },
        "next_route": {
            "selected": (
                "PRESERVE_SECTOR_LOCAL_SOFT_SUPPRESSION_AND_USE_NATIVE_"
                "CHART_STRATIFICATION"
            ),
            "immediate_option": (
                "independent native-chart replicas reduce variance by "
                "sample count without changing the integrand"
            ),
            "advanced_option": (
                "a correlated slot-1/slot-3 estimator requires the full "
                "T13 pullback of soft energy, both polar coordinates, "
                "relative azimuth and all plus-boundary terms before "
                "complex topology is transported"
            ),
            "forbidden_shortcut": (
                "do not replace the slot-3 sector weight by a constant "
                "mixture of w1,w2,w3 in the existing one-soft chart"
            ),
        },
        "source_hashes": {
            str(path): digest(path) for path in required
        },
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }

    validation_rows = [
        {
            "check": "all_source_paths_exist",
            "passed": all(path.is_file() for path in required),
            "detail": str(len(required)),
        },
        {
            "check": "checkpoint_5227_rejection_chain_closed",
            "passed": (
                result_5227["state"] == "COMPLETE_RETROSPECTIVE_REPLAY"
                and result_5227["validation_all_passed"]
                and validation_all_pass(VALIDATION_5227)
            ),
            "detail": result_5227["decision"],
        },
        {
            "check": "soft_amplitude_has_inverse_square_scaling",
            "passed": abs(amplitude_slope + 2.0) <= SLOPE_TOLERANCE,
            "detail": str(amplitude_slope),
        },
        {
            "check": "original_sector_weight_cancels_soft_power",
            "passed": abs(original_slope) <= SLOPE_TOLERANCE,
            "detail": str(original_slope),
        },
        {
            "check": "paired_cross_sector_weight_restores_soft_power",
            "passed": abs(paired_slope + 2.0) <= SLOPE_TOLERANCE,
            "detail": str(paired_slope),
        },
        {
            "check": "lambda_squared_amplitude_reaches_plateau",
            "passed": plateau_ratio <= 1.02,
            "detail": str(plateau_ratio),
        },
        {
            "check": "partition_limits_reached",
            "passed": (
                float(rows[-1]["w_1"]) >= 0.999999
                and float(rows[-1]["w_3"]) <= 2e-8
            ),
            "detail": (
                f"w1={rows[-1]['w_1']}; w3={rows[-1]['w_3']}"
            ),
        },
        {
            "check": "formalization_workbench_unchanged",
            "passed": formal_digest == FORMAL_BASELINE,
            "detail": formal_digest,
        },
        {
            "check": "decision_selects_native_chart_route",
            "passed": result["next_route"]["selected"] == (
                "PRESERVE_SECTOR_LOCAL_SOFT_SUPPRESSION_AND_USE_NATIVE_"
                "CHART_STRATIFICATION"
            ),
            "detail": result["next_route"]["selected"],
        },
        {
            "check": "all_claim_flags_remain_false",
            "passed": not any(
                (
                    result["valid_for_numeric_UV_claim"],
                    result["valid_for_local_GR_claim"],
                    result["valid_for_full_MTS_claim"],
                )
            ),
            "detail": "numeric UV, local GR and full MTS remain false",
        },
    ]
    validation_all_passed = all(
        bool(row["passed"]) for row in validation_rows
    )
    result["validation_all_passed"] = validation_all_passed
    result["validation_check_count"] = len(validation_rows)
    atomic_json(RESULT, result)
    write_csv(VALIDATION, validation_rows)

    document = f"""# 5228 - One-chart cross-sector blend no-go

## Result

Checkpoint 5227 did not merely find an unlucky coefficient. It exposed a
soft-boundary obstruction to the whole constant-mixture shortcut.

Decision:
`{result['decision']}`.

## Derivation

Take the slot-1 soft boundary `E1=lambda->0` while `E2,E3=O(1)`. For

`wi = Ei^-2 / sum_j Ej^-2`,

the weights obey

`w1=1+O(lambda^2)`, `w3=lambda^2/E3^2+O(lambda^4)`.

The crossed `hhh` reduced product has the gravitational soft scaling
`A_hhh=O(lambda^-2)`. The original slot-3 sector factor therefore gives

`3 w3 A_hhh = O(1)`.

For the constant mixture

`W_beta=3[(1-beta)w3+beta w1]`,

every constant `beta != 0` instead gives

`W_beta A_hhh = O(lambda^-2)`.

Since the massless phase-space measure contains `lambda d lambda`, its
absolute mean has the logarithmic boundary `d lambda/lambda`, and its
second moment is stronger still, `d lambda/lambda^3`. A native slot-1
subtraction/chart can regulate that sector; inserting it into the slot-3
one-soft chart cannot.

## Machine check

On a fixed physical geometry, fitting the smallest four `lambda` values
gave:

- `A_hhh` slope: `{amplitude_slope:.9g}`;
- original `3 w3 A_hhh` slope: `{original_slope:.9g}`;
- paired `3(w3+w1)A_hhh/2` slope: `{paired_slope:.9g}`;
- `lambda^2 |A_hhh|` plateau ratio: `{plateau_ratio:.9g}`.

This explains the checkpoint-5227 variance ratios of
`{result_5227['analysis']['A00_real_standard_deviation_ratio']:.9g}` at A00
and `{result_5227['analysis']['local_real_standard_deviation_ratio']:.9g}`
after local projection.

## Consequence

The full-S3 pointwise shortcut `w1+w2+w3=1` is also excluded in this
one-soft chart: algebraic cancellation of the partition denominator would
simultaneously remove the off-sector soft suppression.

The admissible route is now narrower and clearer:

1. preserve each sector's native `O(lambda^2)` suppression;
2. use independent native-chart stratification for immediate variance
   reduction; or
3. build the full correlated `T13` pullback, including transformed outer
   coordinates, relative azimuth, Jacobian and every plus-boundary term,
   before transporting complex topology.

This closes a shortcut class; it does not close the ultraviolet coefficient.

## Claim boundary

No numerical UV coefficient, local-GR result, galaxy result, or full-MTS
claim follows. The result is an estimator-admissibility theorem.

## Evidence

- Scaling rows: `{ROWS}`
- Result: `{RESULT}`
- Validation: `{VALIDATION}`
"""
    atomic_text(DOCUMENT, document)
    if not validation_all_passed:
        raise RuntimeError(
            "checkpoint-5228 validation failed: "
            + json.dumps(
                [row for row in validation_rows if not row["passed"]],
                indent=2,
            )
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
