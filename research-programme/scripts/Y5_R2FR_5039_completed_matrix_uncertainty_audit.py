from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import f, t


POST = Path(__file__).resolve().parents[1]
SOURCE_5037 = POST / "source-intake" / "functional_rg" / "5037"
RESULT_5037 = SOURCE_5037 / "paired_outer_precision_results.json"
RUN_STATUS = SOURCE_5037 / "runs" / "paired_outer_precision_s4_v1" / "status.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5039"
OUTPUT = SOURCE / "completed_matrix_uncertainty_audit.json"
CONTRACTION_CSV = SOURCE / "contraction_uncertainty.csv"
TARGET_CSV = SOURCE / "fixed_target_uncertainty.csv"
REFLECTION_CSV = SOURCE / "reflection_uncertainty.csv"
MARKER = "MTS_5039_COMPLETED_MATRIX_UNCERTAINTY_AUDIT"
PHYSICAL_COSINES = np.asarray((-0.6, -0.3, 0.0, 0.3, 0.6), dtype=float)
PHI = 1.0 - PHYSICAL_COSINES**2
EPSILON_IDS = ("E080", "E040", "E020")
CONFIDENCE = 0.95


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def complex_from_row(row: dict[str, Any]) -> complex:
    return complex(float(row["real"]), float(row["imaginary"]))


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def mean_row(values: np.ndarray) -> dict[str, Any]:
    mean = complex(np.mean(values))
    count = len(values)
    return {
        "mean": complex_row(mean),
        "real_standard_error": float(np.std(values.real, ddof=1) / math.sqrt(count)),
        "imaginary_standard_error": float(
            np.std(values.imag, ddof=1) / math.sqrt(count)
        ),
        "replicate_count": count,
    }


def real_interval(values: np.ndarray) -> dict[str, Any]:
    values = np.asarray(values, dtype=float)
    count = len(values)
    mean = float(np.mean(values))
    standard_error = float(np.std(values, ddof=1) / math.sqrt(count))
    critical = float(t.ppf(0.5 + CONFIDENCE / 2.0, count - 1))
    half_width = critical * standard_error
    return {
        "mean": mean,
        "standard_error": standard_error,
        "confidence": CONFIDENCE,
        "lower": mean - half_width,
        "upper": mean + half_width,
        "contains_zero": mean - half_width <= 0.0 <= mean + half_width,
    }


def hotelling_zero_test(values: np.ndarray) -> dict[str, Any]:
    sample = np.column_stack((values.real, values.imag))
    count, dimension = sample.shape
    mean = np.mean(sample, axis=0)
    covariance = np.cov(sample, rowvar=False, ddof=1)
    inverse = np.linalg.pinv(covariance, rcond=1.0e-12)
    statistic = float(count * mean @ inverse @ mean)
    critical = float(
        dimension
        * (count - 1)
        / (count - dimension)
        * f.ppf(CONFIDENCE, dimension, count - dimension)
    )
    observed = abs(complex(mean[0], mean[1]))
    signflip_statistics = []
    for signs in itertools.product((-1.0, 1.0), repeat=count):
        signed = values * np.asarray(signs)
        signflip_statistics.append(abs(complex(np.mean(signed))))
    exact_signflip_p = sum(
        statistic_value >= observed - 1.0e-15
        for statistic_value in signflip_statistics
    ) / len(signflip_statistics)
    return {
        "hotelling_T2": statistic,
        "hotelling_95_critical": critical,
        "zero_inside_hotelling_95": statistic <= critical,
        "covariance_rank": int(np.linalg.matrix_rank(covariance)),
        "exact_euclidean_signflip_p": float(exact_signflip_p),
        "signflip_assignments": len(signflip_statistics),
    }


def projection(vector: np.ndarray) -> tuple[complex, np.ndarray, float]:
    coefficient = complex(np.dot(PHI, vector) / np.dot(PHI, PHI))
    nonlocal_vector = vector - coefficient * PHI
    residual = float(abs(np.dot(PHI, nonlocal_vector)))
    return coefficient, nonlocal_vector, residual


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    result = json.loads(RESULT_5037.read_text(encoding="utf-8"))
    status = json.loads(RUN_STATUS.read_text(encoding="utf-8"))
    if not (
        result["run_state"] == "COMPLETE"
        and result["expected_jobs"] == 189
        and result["failed_jobs"] == 0
        and result["unconverged_jobs"] == 0
        and status["state"] == "COMPLETE"
    ):
        raise RuntimeError("5037 matrix is not complete and clean")

    vectors: dict[tuple[int, str], np.ndarray] = {}
    for row in result["cyclic_vectors_per_seed"]:
        vectors[(int(row["seed"]), str(row["epsilon_id"]))] = np.asarray(
            [complex_from_row(value) for value in row["cyclic_vector"]],
            dtype=np.complex128,
        )
    seeds = sorted({seed for seed, _ in vectors})
    if len(seeds) != 4 or len(vectors) != 12:
        raise RuntimeError("expected four paired seeds at three epsilon values")

    local: dict[tuple[int, str], complex] = {}
    nonlocal_values: dict[tuple[int, str], np.ndarray] = {}
    projection_residuals: list[float] = []
    for key, vector in vectors.items():
        coefficient, nonlocal_vector, residual = projection(vector)
        local[key] = coefficient
        nonlocal_values[key] = nonlocal_vector
        projection_residuals.append(residual)

    step_one = np.asarray(
        [nonlocal_values[(seed, "E040")] - nonlocal_values[(seed, "E080")] for seed in seeds]
    )
    step_two = np.asarray(
        [nonlocal_values[(seed, "E020")] - nonlocal_values[(seed, "E040")] for seed in seeds]
    )
    linear_defect = step_two - 0.5 * step_one
    richardson = np.asarray(
        [2.0 * nonlocal_values[(seed, "E020")] - nonlocal_values[(seed, "E040")] for seed in seeds]
    )
    local_step_one = np.asarray(
        [local[(seed, "E040")] - local[(seed, "E080")] for seed in seeds]
    )
    local_step_two = np.asarray(
        [local[(seed, "E020")] - local[(seed, "E040")] for seed in seeds]
    )
    local_linear_defect = local_step_two - 0.5 * local_step_one
    local_richardson = np.asarray(
        [2.0 * local[(seed, "E020")] - local[(seed, "E040")] for seed in seeds]
    )

    contraction_rows: list[dict[str, Any]] = []
    contraction_csv_rows: list[dict[str, Any]] = []
    for component_index, cosine in enumerate(PHYSICAL_COSINES):
        first = step_one[:, component_index]
        second = step_two[:, component_index]
        magnitude_delta = np.abs(second) - np.abs(first)
        interval = real_interval(magnitude_delta)
        if interval["upper"] < 0.0:
            classification = "contraction_supported_95"
        elif interval["lower"] > 0.0:
            classification = "noncontraction_supported_95"
        else:
            classification = "unresolved_at_four_scrambles"
        defect_test = hotelling_zero_test(linear_defect[:, component_index])
        first_mean = complex(np.mean(first))
        second_mean = complex(np.mean(second))
        row = {
            "component_index": component_index,
            "physical_s_channel_cosine": float(cosine),
            "first_step": mean_row(first),
            "second_step": mean_row(second),
            "first_mean_magnitude": float(abs(first_mean)),
            "second_mean_magnitude": float(abs(second_mean)),
            "raw_mean_step_contracts": abs(second_mean) < abs(first_mean),
            "eventwise_magnitude_delta_interval": interval,
            "contraction_classification": classification,
            "linear_scaling_defect": mean_row(linear_defect[:, component_index]),
            "linear_scaling_defect_test": defect_test,
        }
        contraction_rows.append(row)
        contraction_csv_rows.append(
            {
                "component_index": component_index,
                "physical_s_channel_cosine": float(cosine),
                "first_mean_magnitude": abs(first_mean),
                "second_mean_magnitude": abs(second_mean),
                "raw_mean_step_contracts": row["raw_mean_step_contracts"],
                "magnitude_delta_mean": interval["mean"],
                "magnitude_delta_95_lower": interval["lower"],
                "magnitude_delta_95_upper": interval["upper"],
                "classification": classification,
                "linear_defect_zero_inside_hotelling_95": defect_test[
                    "zero_inside_hotelling_95"
                ],
                "linear_defect_signflip_p": defect_test[
                    "exact_euclidean_signflip_p"
                ],
                "valid_for_full_MTS_claim": False,
            }
        )

    target_rows_source = result["linear_epsilon_zero_diagnostic"][
        "fixed_5018_target_comparison"
    ]
    target = np.asarray([float(row["fixed_5018_target"]) for row in target_rows_source])
    target_rows: list[dict[str, Any]] = []
    target_csv_rows: list[dict[str, Any]] = []
    for component_index, cosine in enumerate(PHYSICAL_COSINES):
        residuals = richardson[:, component_index].real - target[component_index]
        real_residual_interval = real_interval(residuals)
        imaginary_interval = real_interval(richardson[:, component_index].imag)
        sample_sd = float(np.std(residuals, ddof=1))
        observed_residual = abs(float(np.mean(residuals)))
        planning_count = (
            math.ceil((1.96 * sample_sd / observed_residual) ** 2)
            if observed_residual > 0.0
            else None
        )
        row = {
            "component_index": component_index,
            "physical_s_channel_cosine": float(cosine),
            "fixed_target": float(target[component_index]),
            "richardson_estimate": mean_row(richardson[:, component_index]),
            "real_target_residual_interval": real_residual_interval,
            "imaginary_zero_interval": imaginary_interval,
            "target_excluded_95": not real_residual_interval["contains_zero"],
            "imaginary_zero_excluded_95": not imaginary_interval["contains_zero"],
            "normal_approximate_count_to_resolve_observed_real_residual": planning_count,
        }
        target_rows.append(row)
        target_csv_rows.append(
            {
                "component_index": component_index,
                "physical_s_channel_cosine": float(cosine),
                "fixed_target": target[component_index],
                "predicted_real_mean": np.mean(richardson[:, component_index].real),
                "predicted_real_standard_error": np.std(
                    richardson[:, component_index].real, ddof=1
                )
                / math.sqrt(len(seeds)),
                "residual_95_lower": real_residual_interval["lower"],
                "residual_95_upper": real_residual_interval["upper"],
                "target_excluded_95": row["target_excluded_95"],
                "imaginary_zero_excluded_95": row["imaginary_zero_excluded_95"],
                "planning_count": planning_count,
                "valid_for_full_MTS_claim": False,
            }
        )

    reflection_rows: list[dict[str, Any]] = []
    reflection_csv_rows: list[dict[str, Any]] = []
    for left_index, right_index in ((0, 4), (1, 3)):
        absolute_cosine = abs(float(PHYSICAL_COSINES[left_index]))
        odd = 0.5 * (richardson[:, left_index] - richardson[:, right_index])
        target_odd = 0.5 * (target[left_index] - target[right_index])
        real_interval_row = real_interval(odd.real - target_odd)
        imaginary_interval_row = real_interval(odd.imag)
        row = {
            "absolute_cosine": absolute_cosine,
            "odd_estimate": mean_row(odd),
            "fixed_target_odd": float(target_odd),
            "odd_minus_target_real_interval": real_interval_row,
            "odd_imaginary_zero_interval": imaginary_interval_row,
            "target_odd_excluded_95": not real_interval_row["contains_zero"],
            "imaginary_zero_excluded_95": not imaginary_interval_row["contains_zero"],
        }
        reflection_rows.append(row)
        reflection_csv_rows.append(
            {
                "absolute_cosine": absolute_cosine,
                "odd_real_mean": np.mean(odd.real),
                "odd_real_standard_error": np.std(odd.real, ddof=1)
                / math.sqrt(len(seeds)),
                "fixed_target_odd": target_odd,
                "residual_95_lower": real_interval_row["lower"],
                "residual_95_upper": real_interval_row["upper"],
                "target_odd_excluded_95": row["target_odd_excluded_95"],
                "imaginary_zero_excluded_95": row["imaginary_zero_excluded_95"],
                "valid_for_full_MTS_claim": False,
            }
        )

    local_defect_test = hotelling_zero_test(local_linear_defect)
    raw_failed = [
        row["component_index"] for row in contraction_rows if not row["raw_mean_step_contracts"]
    ]
    supported_noncontraction = [
        row["component_index"]
        for row in contraction_rows
        if row["contraction_classification"] == "noncontraction_supported_95"
    ]
    document = {
        "checkpoint_marker": MARKER,
        "source_result": str(RESULT_5037),
        "source_result_sha256": digest(RESULT_5037),
        "source_status": str(RUN_STATUS),
        "source_status_sha256": digest(RUN_STATUS),
        "script": str(Path(__file__).resolve()),
        "script_sha256": digest(Path(__file__).resolve()),
        "paired_scrambles": len(seeds),
        "seeds": seeds,
        "physical_s_channel_cosines": PHYSICAL_COSINES.tolist(),
        "projection_vector": PHI.tolist(),
        "maximum_recomputed_projection_residual": max(projection_residuals),
        "contraction_rows": contraction_rows,
        "local_coefficient": {
            "first_step": mean_row(local_step_one),
            "second_step": mean_row(local_step_two),
            "linear_scaling_defect": mean_row(local_linear_defect),
            "linear_scaling_defect_test": local_defect_test,
            "richardson_estimate": mean_row(local_richardson),
        },
        "fixed_target_rows": target_rows,
        "reflection_rows": reflection_rows,
        "summary": {
            "raw_mean_contraction_failed_components": raw_failed,
            "noncontraction_supported_95_components": supported_noncontraction,
            "all_linear_defects_include_zero_in_hotelling_95": all(
                row["linear_scaling_defect_test"]["zero_inside_hotelling_95"]
                for row in contraction_rows
            )
            and local_defect_test["zero_inside_hotelling_95"],
            "fixed_target_components_excluded_95": [
                row["component_index"] for row in target_rows if row["target_excluded_95"]
            ],
            "imaginary_zero_excluded_95_components": [
                row["component_index"]
                for row in target_rows
                if row["imaginary_zero_excluded_95"]
            ],
            "reflection_target_odd_excluded_95": [
                row["absolute_cosine"]
                for row in reflection_rows
                if row["target_odd_excluded_95"]
            ],
            "four_scramble_result": (
                "raw contraction failures are not statistically resolved as "
                "noncontraction; the fixed target is neither excluded nor matched"
            ),
            "next_evidence_gate": (
                "increase independent paired outer information under a sequential "
                "stopping rule; do not promote the predeclared eight-scramble "
                "minimum into a guaranteed precision claim"
            ),
        },
        "target_fitted": False,
        "epsilon_zero_claimed": False,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    SOURCE.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    write_csv(CONTRACTION_CSV, contraction_csv_rows)
    write_csv(TARGET_CSV, target_csv_rows)
    write_csv(REFLECTION_CSV, reflection_csv_rows)
    print(json.dumps(document["summary"], indent=2))


if __name__ == "__main__":
    main()
