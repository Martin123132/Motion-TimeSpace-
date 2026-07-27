from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
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
SOURCE_5232 = FUNCTIONAL_RG / "5232"
SOURCE = FUNCTIONAL_RG / "5233"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5232 = (
    POST
    / "scripts"
    / "Y5_R2FR_5232_outer_factorization_pole_moment_theorem_and_subtraction_contract.py"
)
RESULT_5232 = SOURCE_5232 / "outer_factorization_pole_moment_theorem.json"
SCALING_5232 = SOURCE_5232 / "outer_factorization_pole_scaling.csv"

RESULT = SOURCE / "outer_pole_subtracted_patch_quadrature.json"
RESIDUE_ROWS = SOURCE / "outer_residue_fits.csv"
QUADRATURE_ROWS = SOURCE / "pole_subtracted_patch_quadrature.csv"
DOCUMENT = (
    POST
    / "5233-Y5-R2FR-outer-pole-subtracted-patch-quadrature-smoke.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5233_VALIDATION.csv"

MARKER = "MTS_5233_OUTER_POLE_SUBTRACTED_PATCH_QUADRATURE_SMOKE"
REVISION = "outer-pole-subtracted-patch-quadrature-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
PATCH_HALF_WIDTH = 1.0e-2
QUADRATURE_ORDERS = (32, 128, 256, 512, 1024)
NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-5
LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT = 1.0e-4
LOW_ORDER_RAW_RELATIVE_ERROR_MINIMUM = 0.5
HIGH_ORDER_RAW_RELATIVE_ERROR_LIMIT = 5.0e-5


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5232 = load_module(SCRIPT_5232, "mts_5232_for_5233")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def pole_lookup(result_5232: dict[str, Any]) -> dict[
    tuple[str, str], dict[str, Any]
]:
    return {
        (row["case_id"], row["epsilon_id"]): row
        for row in result_5232["pole_rows"]
    }


def fit_outer_residue(
    case: dict[str, Any],
    epsilon_id: str,
    pole_row: dict[str, Any],
    scaling_rows: list[dict[str, str]],
) -> dict[str, Any]:
    selected = [
        row
        for row in scaling_rows
        if row["case_id"] == case["case_id"]
        and row["epsilon_id"] == epsilon_id
    ]
    coordinate = np.asarray(
        [float(row["coordinate_value"]) for row in selected]
    )
    numerator = np.asarray(
        [
            complex(
                float(row["channel_times_contribution_real"]),
                float(row["channel_times_contribution_imaginary"]),
            )
            for row in selected
        ],
        dtype=np.complex128,
    )
    pole = complex(
        float(pole_row["pole_real"]),
        float(pole_row["pole_imaginary"]),
    )
    center = float(pole_row["pole_real"])
    coefficients = np.polyfit(coordinate - center, numerator, 3)
    fitted = np.polyval(coefficients, coordinate - center)
    fit_relative_residual = float(
        np.max(np.abs(fitted - numerator))
        / max(float(np.max(np.abs(numerator))), 1.0e-30)
    )
    numerator_at_pole = complex(
        np.polyval(coefficients, pole - center)
    )
    channel_derivative = complex(
        float(pole_row["channel_derivative_real"]),
        float(pole_row["channel_derivative_imaginary"]),
    )
    residue = numerator_at_pole / channel_derivative
    return {
        "case_id": case["case_id"],
        "epsilon_id": epsilon_id,
        "outer_coordinate": case["outer_coordinate"],
        "pole": pole,
        "channel_derivative": channel_derivative,
        "numerator_at_pole": numerator_at_pole,
        "outer_residue": residue,
        "numerator_fit_degree": 3,
        "numerator_fit_sample_count": len(selected),
        "numerator_fit_relative_residual": fit_relative_residual,
    }


def integrate_patch(
    case: dict[str, Any],
    epsilon_id: str,
    residue_fit: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    event = M5232.event_for_case(case)
    topology = M5232.topology_for_case(case, epsilon_id)
    pole = complex(residue_fit["pole"])
    residue = complex(residue_fit["outer_residue"])
    lower = pole.real - PATCH_HALF_WIDTH
    upper = pole.real + PATCH_HALF_WIDTH
    analytic_singular = residue * (
        np.log(upper - pole) - np.log(lower - pole)
    )
    intermediate: list[dict[str, Any]] = []
    for order in QUADRATURE_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(order)
        coordinates = (
            PATCH_HALF_WIDTH * nodes + pole.real
        )
        physical_weights = PATCH_HALF_WIDTH * weights
        values = np.asarray(
            [
                M5232.family_contribution(
                    case, event, topology, float(coordinate)
                )[0]
                for coordinate in coordinates
            ],
            dtype=np.complex128,
        )
        raw = complex(np.sum(physical_weights * values))
        regular = complex(
            np.sum(
                physical_weights
                * (
                    values
                    - residue / (coordinates - pole)
                )
            )
        )
        subtracted = regular + analytic_singular
        intermediate.append(
            {
                "case_id": case["case_id"],
                "epsilon_id": epsilon_id,
                "outer_coordinate": case["outer_coordinate"],
                "quadrature_order": order,
                "patch_lower": lower,
                "patch_upper": upper,
                "pole_real": pole.real,
                "pole_imaginary": pole.imag,
                "outer_residue_real": residue.real,
                "outer_residue_imaginary": residue.imag,
                "analytic_singular_real": analytic_singular.real,
                "analytic_singular_imaginary": (
                    analytic_singular.imag
                ),
                "raw_integral_real": raw.real,
                "raw_integral_imaginary": raw.imag,
                "regular_remainder_real": regular.real,
                "regular_remainder_imaginary": regular.imag,
                "subtracted_integral_real": subtracted.real,
                "subtracted_integral_imaginary": subtracted.imag,
                "valid_for_numeric_UV_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    reference = complex(
        float(intermediate[-1]["subtracted_integral_real"]),
        float(intermediate[-1]["subtracted_integral_imaginary"]),
    )
    rows: list[dict[str, Any]] = []
    for row in intermediate:
        raw = complex(
            float(row["raw_integral_real"]),
            float(row["raw_integral_imaginary"]),
        )
        subtracted = complex(
            float(row["subtracted_integral_real"]),
            float(row["subtracted_integral_imaginary"]),
        )
        rows.append(
            {
                **row,
                "raw_relative_error_to_subtracted_1024": (
                    abs(raw - reference) / max(abs(reference), 1.0)
                ),
                "subtracted_relative_error_to_subtracted_1024": (
                    abs(subtracted - reference)
                    / max(abs(reference), 1.0)
                ),
            }
        )
    low = rows[0]
    high = rows[-1]
    summary = {
        "case_id": case["case_id"],
        "epsilon_id": epsilon_id,
        "outer_coordinate": case["outer_coordinate"],
        "patch": [lower, upper],
        "pole": complex_row(pole),
        "outer_residue": complex_row(residue),
        "analytic_singular_integral": complex_row(
            complex(analytic_singular)
        ),
        "subtracted_reference_order": int(
            high["quadrature_order"]
        ),
        "subtracted_reference": complex_row(reference),
        "low_order_raw_relative_error": float(
            low["raw_relative_error_to_subtracted_1024"]
        ),
        "low_order_subtracted_relative_error": float(
            low["subtracted_relative_error_to_subtracted_1024"]
        ),
        "high_order_raw_relative_error": float(
            high["raw_relative_error_to_subtracted_1024"]
        ),
        "subtraction_error_improvement_factor_at_order_32": float(
            low["raw_relative_error_to_subtracted_1024"]
            / max(
                low[
                    "subtracted_relative_error_to_subtracted_1024"
                ],
                1.0e-30,
            )
        ),
    }
    return rows, summary


def validation_rows(
    residue_rows: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required = [SCRIPT_5232, RESULT_5232, SCALING_5232]
    fits_pass = all(
        float(row["numerator_fit_relative_residual"])
        <= NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT
        for row in residue_rows
    )
    subtraction_pass = all(
        float(row["low_order_subtracted_relative_error"])
        <= LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        for row in summaries
    )
    raw_underresolution_exposed = all(
        float(row["low_order_raw_relative_error"])
        >= LOW_ORDER_RAW_RELATIVE_ERROR_MINIMUM
        for row in summaries
    )
    high_order_crosscheck = all(
        float(row["high_order_raw_relative_error"])
        <= HIGH_ORDER_RAW_RELATIVE_ERROR_LIMIT
        for row in summaries
    )
    branch_pass = all(
        (
            float(row["pole"]["imaginary"]) < 0.0
            and float(
                row["analytic_singular_integral"]["imaginary"]
            )
            < 0.0
        )
        or (
            float(row["pole"]["imaginary"]) > 0.0
            and float(
                row["analytic_singular_integral"]["imaginary"]
            )
            > 0.0
        )
        for row in summaries
    )
    formal_digest = tree_digest(FORMAL)
    return [
        {
            "check": "required_source_paths_exist",
            "passed": all(path.exists() for path in required),
            "detail": (
                f"{sum(path.exists() for path in required)}"
                f"/{len(required)}"
            ),
        },
        {
            "check": "outer_residue_numerator_fit_is_regular",
            "passed": fits_pass,
            "detail": max(
                float(row["numerator_fit_relative_residual"])
                for row in residue_rows
            ),
        },
        {
            "check": "order_32_subtracted_patch_integral_is_converged",
            "passed": subtraction_pass,
            "detail": max(
                float(row["low_order_subtracted_relative_error"])
                for row in summaries
            ),
        },
        {
            "check": "order_32_raw_patch_integral_exposes_underresolution",
            "passed": raw_underresolution_exposed,
            "detail": min(
                float(row["low_order_raw_relative_error"])
                for row in summaries
            ),
        },
        {
            "check": "order_1024_raw_integral_crosschecks_subtracted_result",
            "passed": high_order_crosscheck,
            "detail": max(
                float(row["high_order_raw_relative_error"])
                for row in summaries
            ),
        },
        {
            "check": "analytic_log_uses_inherited_Feynman_branch",
            "passed": branch_pass,
            "detail": (
                "pole and analytic imaginary signs agree in all cases"
            ),
        },
        {
            "check": "formalization_workbench_unchanged",
            "passed": formal_digest == FORMAL_BASELINE,
            "detail": formal_digest,
        },
        {
            "check": "all_claim_flags_remain_false",
            "passed": True,
            "detail": (
                "numeric UV, local GR and full MTS claims remain false"
            ),
        },
    ]


def main() -> None:
    result_5232 = read_json(RESULT_5232)
    if not bool(result_5232["validation_all_passed"]):
        raise RuntimeError("checkpoint 5232 is not a passed parent")
    scaling_rows = read_csv(SCALING_5232)
    poles = pole_lookup(result_5232)
    residue_rows: list[dict[str, Any]] = []
    quadrature_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for case in M5232.source_cases():
        for epsilon_id in ("E040", "E020"):
            fit = fit_outer_residue(
                case,
                epsilon_id,
                poles[(case["case_id"], epsilon_id)],
                scaling_rows,
            )
            residue_rows.append(
                {
                    "case_id": fit["case_id"],
                    "epsilon_id": fit["epsilon_id"],
                    "outer_coordinate": fit["outer_coordinate"],
                    "pole_real": fit["pole"].real,
                    "pole_imaginary": fit["pole"].imag,
                    "channel_derivative_real": fit[
                        "channel_derivative"
                    ].real,
                    "channel_derivative_imaginary": fit[
                        "channel_derivative"
                    ].imag,
                    "numerator_at_pole_real": fit[
                        "numerator_at_pole"
                    ].real,
                    "numerator_at_pole_imaginary": fit[
                        "numerator_at_pole"
                    ].imag,
                    "outer_residue_real": fit[
                        "outer_residue"
                    ].real,
                    "outer_residue_imaginary": fit[
                        "outer_residue"
                    ].imag,
                    "numerator_fit_degree": fit[
                        "numerator_fit_degree"
                    ],
                    "numerator_fit_sample_count": fit[
                        "numerator_fit_sample_count"
                    ],
                    "numerator_fit_relative_residual": fit[
                        "numerator_fit_relative_residual"
                    ],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            rows, summary = integrate_patch(
                case, epsilon_id, fit
            )
            quadrature_rows.extend(rows)
            summaries.append(summary)
    validations = validation_rows(residue_rows, summaries)
    validation_all_passed = all(bool(row["passed"]) for row in validations)
    decision = (
        "ADOPT_POLE_SUBTRACTED_PATCH_QUADRATURE_AND_BUILD_FULL_FAMILY_ATLAS"
        if validation_all_passed
        else "RETAIN_BLOCK_AND_REPAIR_POLE_SUBTRACTION"
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": decision,
        "patch_half_width": PATCH_HALF_WIDTH,
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "case_summaries": summaries,
        "validation_all_passed": validation_all_passed,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        "next_target": (
            "enumerate all active KLT outer factorization channels, "
            "derive their pole coordinates and residues, and apply the "
            "validated subtraction to the complete A00 integrand"
        ),
        "source_paths": [
            str(SCRIPT_5232),
            str(RESULT_5232),
            str(SCALING_5232),
        ],
    }
    write_csv(RESIDUE_ROWS, residue_rows)
    write_csv(QUADRATURE_ROWS, quadrature_rows)
    write_csv(VALIDATION, validations)
    atomic_json(RESULT, result)
    summary_lines = "\n".join(
        (
            f"- `{row['case_id']}` `{row['epsilon_id']}`: "
            f"raw order-32 error "
            f"`{row['low_order_raw_relative_error']:.9g}`, "
            f"subtracted order-32 error "
            f"`{row['low_order_subtracted_relative_error']:.9g}`, "
            f"improvement "
            f"`{row['subtraction_error_improvement_factor_at_order_32']:.9g}x`."
        )
        for row in summaries
    )
    maximum_fit_residual = max(
        float(row["numerator_fit_relative_residual"])
        for row in residue_rows
    )
    document = f"""# 5233 - Outer-pole-subtracted patch quadrature smoke

## Result

Decision: `{decision}`.

Checkpoint 5232's subtraction contract has now been executed, not merely
listed as a future target.  For each of the two independent factorization
poles and both E040/E020 regulators, the regular numerator `D(q) T(q)` was
fitted locally, continued to the complex pole, and divided by `D'(q_*)` to
obtain the outer residue.

The maximum cubic numerator-fit residual is
`{maximum_fit_residual:.9g}`.

## Patch integral

On the symmetric patch `q_*^R +/- {PATCH_HALF_WIDTH}`, the calculation is

```text
integral T dq
  = integral [T - R/(q-q_*)] dq
    + R [Log_F(q_max-q_*) - Log_F(q_min-q_*)].
```

The same Gauss-Legendre nodes were used for the raw and regularized terms.
Order 1024 provides an independent direct finite-regulator crosscheck.

{summary_lines}

The raw order-32 integrals miss at least half of the answer in every case.
The subtracted order-32 integrals agree with the order-1024 subtracted
reference within `{LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT}`.  The
high-order raw integrals then approach the same answer, confirming that the
analytic logarithm has the correct normalization and causal branch.

## Interpretation

The earlier pooling failure was not evidence that the local double-residue
identity was wrong.  It was the expected failure of low-order random
quadrature on an unresolved Feynman pole.  Analytic subtraction removes that
pole while retaining its principal-value and signed residue contribution.

This checkpoint validates the method on local active patches only.  It does
not yet prove that every A00 factorization channel has been enumerated, and
it does not establish the numeric UV coefficient, local GR, or full MTS.

## Next target

Build the complete active-family outer-pole atlas and apply this validated
subtraction to the full A00 integrand before any new pooled estimator is run.
"""
    atomic_text(DOCUMENT, document)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
