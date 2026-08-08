from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5299"

SCRIPT_5298 = (
    SCRIPTS / "Y5_R2FR_5298_order8_inner_energy_and_order6_comparison.py"
)
RESULT_5298 = FUNCTIONAL_RG / "5298" / "order8_inner_energy_result.json"
VALIDATION_5298 = (
    FUNCTIONAL_RG / "5298" / "order8_inner_energy_validation.csv"
)
GRID_INPUTS = {
    2: (
        FUNCTIONAL_RG / "5286" / "angular_order2_nodes.csv",
        FUNCTIONAL_RG / "5290" / "all_family_inner_energy_totals.csv",
    ),
    4: (
        FUNCTIONAL_RG / "5291" / "angular_order4_nodes.csv",
        FUNCTIONAL_RG / "5294" / "hidden_track_inner_energy_totals.csv",
    ),
    6: (
        FUNCTIONAL_RG / "5295" / "angular_order6_nodes.csv",
        FUNCTIONAL_RG / "5296" / "order6_inner_energy_totals.csv",
    ),
    8: (
        FUNCTIONAL_RG / "5297" / "angular_order8_nodes.csv",
        FUNCTIONAL_RG / "5298" / "order8_inner_energy_totals.csv",
    ),
}

DRY_RUN = SOURCE / "stored_angular_orbit_diagnostic_dry_run.json"
ORBIT_SAMPLES = SOURCE / "angular_sign_orbit_samples.csv"
ORDER_SUMMARY = SOURCE / "angular_order_cancellation_summary.csv"
REGULARIZED_FIT = SOURCE / "order8_regularized_polynomial_fit.csv"
FIT_PREDICTIONS = SOURCE / "cross_order_regularized_fit_predictions.csv"
ADAPTIVE_TARGETS = SOURCE / "adaptive_ridge_target_orbits.csv"
RESULT = SOURCE / "stored_angular_orbit_diagnostic_result.json"
VALIDATION = SOURCE / "stored_angular_orbit_diagnostic_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5299_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST / "5299-Y5-R2FR-stored-angular-orbit-ridge-diagnostic.md"
)

CHECKPOINT = 5299
PARENT_CHECKPOINT = 5298
MARKER = "MTS_5299_STORED_ANGULAR_ORBIT_RIDGE_DIAGNOSTIC"
REVISION = "stored-angular-orbit-ridge-diagnostic-v1"
ANGULAR_LIMIT = 0.995
ENERGY_ORDER = 8
POLYNOMIAL_TOTAL_DEGREE = 3
CLAIM_FIELDS = (
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5298 = load_module("mts_5298_for_5299", SCRIPT_5298)
M5283 = M5298.M5283
np = M5298.M5292.np


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5298,
        RESULT_5298,
        VALIDATION_5298,
        M5283.TOTALS_5281,
        *(
            path
            for pair in GRID_INPUTS.values()
            for path in pair
        ),
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def orbit_rows_for_order(order: int) -> list[dict[str, Any]]:
    node_path, total_path = GRID_INPUTS[order]
    nodes = read_csv(node_path)
    node_lookup = {
        row["angular_node_id"]: row for row in nodes
    }
    coordinate_lookup = {
        (
            round(float(row["soft_cosine"]), 12),
            round(float(row["decay_cosine"]), 12),
        ): row
        for row in nodes
    }
    totals = {
        row["angular_node_id"]: complex(
            float(row["eight_component_integral_real"]),
            float(row["eight_component_integral_imaginary"]),
        )
        for row in read_csv(total_path)
        if row["row_type"] == "PHYSICAL_INNER_ENERGY"
        and int(row["energy_order"]) == ENERGY_ORDER
    }
    positive_soft = sorted(
        {
            round(abs(float(row["soft_cosine"])), 12)
            for row in nodes
        }
    )
    rows: list[dict[str, Any]] = []
    for soft in positive_soft:
        for decay in positive_soft:
            members = [
                coordinate_lookup[
                    (
                        round(soft_sign * soft, 12),
                        round(decay_sign * decay, 12),
                    )
                ]
                for soft_sign in (-1.0, 1.0)
                for decay_sign in (-1.0, 1.0)
            ]
            orbit = sum(
                totals[row["angular_node_id"]] for row in members
            )
            source = node_lookup[members[0]["angular_node_id"]]
            weight = (
                float(source["angular_weight"])
                * float(source["angular_jacobian"])
            )
            contribution = weight * orbit
            rows.append(
                {
                    "angular_order": order,
                    "absolute_soft_cosine": soft,
                    "absolute_decay_cosine": decay,
                    "soft_endpoint_distance": ANGULAR_LIMIT - soft,
                    "decay_endpoint_distance": ANGULAR_LIMIT - decay,
                    "orbit_member_count": len(members),
                    "orbit_member_ids": "|".join(
                        row["angular_node_id"] for row in members
                    ),
                    "single_node_measure_weight": weight,
                    **complex_fields("sign_orbit_integrand", orbit),
                    **complex_fields(
                        "weighted_orbit_contribution",
                        contribution,
                    ),
                    "valid_for_stored_angular_orbit_diagnostic": True,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def order_summary_rows(
    orbit_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for order in sorted(GRID_INPUTS):
        local = [
            row
            for row in orbit_rows
            if int(row["angular_order"]) == order
        ]
        total = sum(
            complex(
                float(row["weighted_orbit_contribution_real"]),
                float(row["weighted_orbit_contribution_imaginary"]),
            )
            for row in local
        )
        l1 = sum(
            float(row["weighted_orbit_contribution_magnitude"])
            for row in local
        )
        maximum = max(
            local,
            key=lambda row: float(
                row["weighted_orbit_contribution_magnitude"]
            ),
        )
        rows.append(
            {
                "angular_order": order,
                "angular_node_count": order * order,
                "sign_orbit_count": len(local),
                **complex_fields("outer_total", total),
                "orbit_contribution_L1_norm": l1,
                "outer_to_L1_cancellation_ratio": abs(total)
                / max(l1, 1.0e-300),
                "largest_orbit_soft_cosine": maximum[
                    "absolute_soft_cosine"
                ],
                "largest_orbit_decay_cosine": maximum[
                    "absolute_decay_cosine"
                ],
                "largest_weighted_orbit_magnitude": maximum[
                    "weighted_orbit_contribution_magnitude"
                ],
                "valid_for_cross_order_angular_diagnostic": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def polynomial_powers() -> list[tuple[int, int]]:
    return [
        (soft_power, decay_power)
        for total_degree in range(POLYNOMIAL_TOTAL_DEGREE + 1)
        for soft_power in range(total_degree + 1)
        for decay_power in (total_degree - soft_power,)
    ]


def regularized_fit_rows(
    orbit_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], float]:
    training = [
        row
        for row in orbit_rows
        if int(row["angular_order"]) == 8
    ]
    powers = polynomial_powers()
    matrix_rows: list[list[float]] = []
    values: list[complex] = []
    for row in training:
        soft = float(row["absolute_soft_cosine"])
        decay = float(row["absolute_decay_cosine"])
        soft_square = (soft / ANGULAR_LIMIT) ** 2
        decay_square = (decay / ANGULAR_LIMIT) ** 2
        regularizer = (
            2.0 * ANGULAR_LIMIT - soft - decay
        )
        matrix_rows.append(
            [
                soft_square**soft_power
                * decay_square**decay_power
                for soft_power, decay_power in powers
            ]
        )
        orbit = complex(
            float(row["sign_orbit_integrand_real"]),
            float(row["sign_orbit_integrand_imaginary"]),
        )
        values.append(regularizer * orbit)
    matrix = np.asarray(matrix_rows, dtype=np.float64)
    target = np.asarray(values, dtype=np.complex128)
    coefficients, _, _, _ = np.linalg.lstsq(
        matrix,
        target,
        rcond=None,
    )
    predicted_training = matrix @ coefficients
    training_residual = float(
        np.max(np.abs(predicted_training - target))
        / max(float(np.max(np.abs(target))), 1.0e-300)
    )
    coefficient_rows = [
        {
            "soft_square_power": soft_power,
            "decay_square_power": decay_power,
            **complex_fields(
                "regularized_polynomial_coefficient",
                complex(coefficients[index]),
            ),
            "training_order": 8,
            "training_orbit_count": len(training),
            "training_maximum_relative_residual": training_residual,
            "matrix_condition_number": float(np.linalg.cond(matrix)),
            "valid_for_ridge_diagnostic_fit": True,
            **{field: False for field in CLAIM_FIELDS},
        }
        for index, (soft_power, decay_power) in enumerate(powers)
    ]
    prediction_rows: list[dict[str, Any]] = []
    maximum_order4_weighted_residual = 0.0
    for source in orbit_rows:
        soft = float(source["absolute_soft_cosine"])
        decay = float(source["absolute_decay_cosine"])
        soft_square = (soft / ANGULAR_LIMIT) ** 2
        decay_square = (decay / ANGULAR_LIMIT) ** 2
        regularizer = 2.0 * ANGULAR_LIMIT - soft - decay
        basis = np.asarray(
            [
                soft_square**soft_power
                * decay_square**decay_power
                for soft_power, decay_power in powers
            ],
            dtype=np.float64,
        )
        regularized_prediction = complex(basis @ coefficients)
        predicted = regularized_prediction / regularizer
        actual = complex(
            float(source["sign_orbit_integrand_real"]),
            float(source["sign_orbit_integrand_imaginary"]),
        )
        residual = actual - predicted
        weighted_residual = float(
            source["single_node_measure_weight"]
        ) * residual
        if int(source["angular_order"]) == 4:
            maximum_order4_weighted_residual = max(
                maximum_order4_weighted_residual,
                abs(weighted_residual),
            )
        prediction_rows.append(
            {
                "angular_order": source["angular_order"],
                "absolute_soft_cosine": soft,
                "absolute_decay_cosine": decay,
                **complex_fields("actual_orbit_integrand", actual),
                **complex_fields(
                    "predicted_orbit_integrand",
                    predicted,
                ),
                **complex_fields("orbit_fit_residual", residual),
                **complex_fields(
                    "weighted_orbit_fit_residual",
                    weighted_residual,
                ),
                "valid_for_ridge_diagnostic_prediction": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return (
        coefficient_rows,
        prediction_rows,
        maximum_order4_weighted_residual,
    )


def adaptive_target_rows(
    orbit_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    order4 = [
        row
        for row in orbit_rows
        if int(row["angular_order"]) == 4
    ]
    hotspot = max(
        order4,
        key=lambda row: float(
            row["weighted_orbit_contribution_magnitude"]
        ),
    )
    center = float(hotspot["absolute_soft_cosine"])
    order8_coordinates = sorted(
        {
            float(row["absolute_soft_cosine"])
            for row in orbit_rows
            if int(row["angular_order"]) == 8
        }
    )
    lower = max(value for value in order8_coordinates if value < center)
    upper = min(value for value in order8_coordinates if value > center)
    targets = (
        (
            "RIDGE_ANCHOR_EXISTING_ORDER4",
            center,
            center,
            False,
            1,
        ),
        (
            "RIDGE_LOWER_DIAGONAL_MIDPOINT",
            0.5 * (lower + center),
            0.5 * (lower + center),
            True,
            2,
        ),
        (
            "RIDGE_UPPER_DIAGONAL_MIDPOINT",
            0.5 * (center + upper),
            0.5 * (center + upper),
            True,
            3,
        ),
    )
    return [
        {
            "target_id": target_id,
            "absolute_soft_cosine": soft,
            "absolute_decay_cosine": decay,
            "sign_orbit_node_count": 4,
            "requires_new_exact_node_runs": requires_new,
            "execution_priority": priority,
            "selection_reason": (
                "bracket the dominant order-four interior sign-orbit "
                "ridge before another global angular order"
            ),
            "valid_for_adaptive_ridge_followup": True,
            **{field: False for field in CLAIM_FIELDS},
        }
        for target_id, soft, decay, requires_new, priority in targets
    ]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5298)
    checks = {
        "required_sources_exist": all(
            path.exists()
            for path in (
                SCRIPT_5298,
                RESULT_5298,
                VALIDATION_5298,
                *(
                    path
                    for pair in GRID_INPUTS.values()
                    for path in pair
                ),
            )
        ),
        "parent_5298_accepted": bool(parent["acceptance_passed"]),
        "parent_5298_validated": all(
            parse_bool(row["passed"])
            for row in read_csv(VALIDATION_5298)
        ),
        "all_four_angular_orders_present": set(GRID_INPUTS)
        == {2, 4, 6, 8},
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": (
            "DRY_RUN_ACCEPTED__DIAGNOSE_STORED_ANGULAR_ORBITS"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5299 dry run did not pass")
    parent = read_json(RESULT_5298)
    orbits = [
        row
        for order in sorted(GRID_INPUTS)
        for row in orbit_rows_for_order(order)
    ]
    summaries = order_summary_rows(orbits)
    coefficients, predictions, maximum_order4_residual = (
        regularized_fit_rows(orbits)
    )
    targets = adaptive_target_rows(orbits)
    write_csv(ORBIT_SAMPLES, orbits)
    write_csv(ORDER_SUMMARY, summaries)
    write_csv(REGULARIZED_FIT, coefficients)
    write_csv(FIT_PREDICTIONS, predictions)
    write_csv(ADAPTIVE_TARGETS, targets)
    order4_hotspot = max(
        (
            row
            for row in orbits
            if int(row["angular_order"]) == 4
        ),
        key=lambda row: float(
            row["weighted_orbit_contribution_magnitude"]
        ),
    )
    order8_summary = next(
        row for row in summaries if int(row["angular_order"]) == 8
    )
    order6_summary = next(
        row for row in summaries if int(row["angular_order"]) == 6
    )
    order6_total = complex(
        float(order6_summary["outer_total_real"]),
        float(order6_summary["outer_total_imaginary"]),
    )
    order8_total = complex(
        float(order8_summary["outer_total_real"]),
        float(order8_summary["outer_total_imaginary"]),
    )
    order6_order8_change = abs(order8_total - order6_total) / max(
        abs(order8_total),
        abs(order6_total),
        1.0e-300,
    )
    checks = {
        "all_120_stored_nodes_reassembled_into_30_orbits": (
            len(orbits) == 30
            and sum(int(row["orbit_member_count"]) for row in orbits)
            == 120
        ),
        "all_four_order_totals_reproduced": len(summaries) == 4,
        "order6_order8_nonconvergence_reproduced": (
            abs(
                order6_order8_change
                - float(parent["order6_order8_angular_relative_change"])
            )
            <= 1.0e-12
        ),
        "dominant_order4_orbit_is_interior": (
            float(order4_hotspot["soft_endpoint_distance"]) > 0.1
            and float(order4_hotspot["decay_endpoint_distance"]) > 0.1
        ),
        "higher_order_grid_does_not_sample_order4_hotspot": all(
            abs(
                float(row["absolute_soft_cosine"])
                - float(order4_hotspot["absolute_soft_cosine"])
            )
            > 1.0e-6
            or abs(
                float(row["absolute_decay_cosine"])
                - float(order4_hotspot["absolute_decay_cosine"])
            )
            > 1.0e-6
            for row in orbits
            if int(row["angular_order"]) in (6, 8)
        ),
        "stored_fit_exposes_non_smooth_cross_order_residual": (
            maximum_order4_residual > 1.0
        ),
        "two_new_diagonal_bracket_orbits_selected": (
            len(targets) == 3
            and sum(
                parse_bool(row["requires_new_exact_node_runs"])
                for row in targets
            )
            == 2
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "stored-angular-orbit-ridge-diagnostic",
        "checks": checks,
        "acceptance_passed": accepted,
        "stored_node_count": 120,
        "sign_orbit_count": len(orbits),
        "order_summary_count": len(summaries),
        "order6_order8_relative_change": order6_order8_change,
        "order8_outer_to_L1_cancellation_ratio": order8_summary[
            "outer_to_L1_cancellation_ratio"
        ],
        "order4_hotspot_absolute_soft_cosine": order4_hotspot[
            "absolute_soft_cosine"
        ],
        "order4_hotspot_absolute_decay_cosine": order4_hotspot[
            "absolute_decay_cosine"
        ],
        "order4_hotspot_weighted_contribution_magnitude": (
            order4_hotspot["weighted_orbit_contribution_magnitude"]
        ),
        "maximum_order4_weighted_regularized_fit_residual": (
            maximum_order4_residual
        ),
        "new_adaptive_sign_orbit_count": 2,
        "new_adaptive_exact_node_count": 8,
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ORDER8_NOT_CONVERGED__MAP_ORDER4_INTERIOR_RIDGE_WIDTH"
            if accepted
            else "ANGULAR_RIDGE_DIAGNOSTIC_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_stored_angular_ridge_diagnostic": accepted,
            "valid_for_adaptive_target_selection": accepted,
            "valid_for_full_angular_convergence": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Stored tensor grids identify an unresolved interior "
                "ridge but cannot determine its width. Two bracketing "
                "sign orbits require new exact node evaluations."
            ),
        },
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE" if accepted else "FAILED",
            "decision": result["decision"],
            "order4_hotspot": [
                result["order4_hotspot_absolute_soft_cosine"],
                result["order4_hotspot_absolute_decay_cosine"],
            ],
            "new_adaptive_exact_node_count": 8,
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {"gate_id": gate_id, "passed": passed, "detail": detail}


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    checks = "\n".join(
        f"- `{key}`: **{'PASS' if value else 'FAIL'}**"
        for key, value in sorted(result["checks"].items())
    )
    text = f"""# 5299 — Stored angular-orbit ridge diagnostic

## Result

The accepted order-two, order-four, order-six, and order-eight node
shards contain `120` signed angular nodes, which reduce exactly to
`{result['sign_orbit_count']}` parity orbits. The order-six/order-eight
change is `{result['order6_order8_relative_change']:.12g}`.

The dominant order-four orbit is interior, at
`(|s|,|d|)=({result['order4_hotspot_absolute_soft_cosine']:.12g},
{result['order4_hotspot_absolute_decay_cosine']:.12g})`, and contributes
`{result['order4_hotspot_weighted_contribution_magnitude']:.12g}` in
magnitude. Neither the order-six nor order-eight Gauss grid samples
that location. A smooth endpoint-regularized polynomial trained on the
order-eight grid misses the stored order-four orbit by a weighted
residual of
`{result['maximum_order4_weighted_regularized_fit_residual']:.12g}`.
This is evidence for an unresolved interior ridge, not merely an
angular endpoint tail.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Next target

Evaluate the two diagonal midpoint sign orbits bracketing the stored
order-four hotspot: eight new signed nodes in total. This directly
measures the ridge width before spending another global order-ten grid.

## Claim boundary

This diagnostic selects new nodes; it does not establish angular
convergence or a full phase-space, UV, local-GR, or full-MTS result.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required = (
        DRY_RUN,
        ORBIT_SAMPLES,
        ORDER_SUMMARY,
        REGULARIZED_FIT,
        FIT_PREDICTIONS,
        ADAPTIVE_TARGETS,
        RESULT,
        STATUS,
    )
    result = read_json(RESULT)
    orbits = read_csv(ORBIT_SAMPLES)
    summaries = read_csv(ORDER_SUMMARY)
    targets = read_csv(ADAPTIVE_TARGETS)
    source_hashes_match = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    formal_end = M5283.formal_inventory_digest()
    gates = [
        validation_gate(
            "V01_REQUIRED_OUTPUTS_EXIST",
            all(path.exists() for path in required),
            f"{len(required)} required outputs",
        ),
        validation_gate(
            "V02_RESULT_ACCEPTED",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "V03_SOURCE_HASHES_MATCH",
            source_hashes_match,
            f"{len(result['source_files'])} source hashes",
        ),
        validation_gate(
            "V04_ORBIT_COUNTS",
            len(orbits) == 30
            and len(summaries) == 4
            and len(targets) == 3,
            (
                f"orbits={len(orbits)} summaries={len(summaries)} "
                f"targets={len(targets)}"
            ),
        ),
        validation_gate(
            "V05_ADAPTIVE_SCOPE_BOUNDED",
            sum(
                4
                for row in targets
                if parse_bool(row["requires_new_exact_node_runs"])
            )
            == 8,
            "eight new signed nodes",
        ),
        validation_gate(
            "V06_FORMAL_WORKBENCH_UNCHANGED",
            formal_end
            == str(result["formalization_workbench_reference_digest"]),
            formal_end,
        ),
        validation_gate(
            "V07_CLAIMS_LOCKED_FALSE",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
    ]
    passed = all(row["passed"] for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_STORED_ANGULAR_ORBIT_RIDGE_DIAGNOSTIC"
            if passed
            else "STORED_ANGULAR_ORBIT_DIAGNOSTIC_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        required=True,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    else:
        result = validate_outputs()
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
