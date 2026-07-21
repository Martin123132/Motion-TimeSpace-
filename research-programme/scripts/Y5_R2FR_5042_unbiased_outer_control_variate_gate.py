from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5040"
    / "runs"
    / "nested_sobol_power1_s4_v1"
)
SCRIPT_5040 = POST / "scripts" / "Y5_R2FR_5040_nested_sobol_variance_reduction.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5042"
RESULT_JSON = SOURCE / "unbiased_control_variate_gate.json"
MODEL_CSV = SOURCE / "retrospective_model_comparison.csv"
COMPONENT_CSV = SOURCE / "retrospective_component_ratios.csv"
LOCK_JSON = SOURCE / "locked_independent_pilot_contract.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5042_VALIDATION.csv"
)
MARKER = "MTS_5042_UNBIASED_OUTER_CONTROL_VARIATE_GATE"
CONFIG_DIGEST = "39540edd7cae4b42a78ab0c72939aa9f3a7b0e96f27f3063fca3f005db6fc81f"
RIDGE_MULTIPLIER = 1.0
FEATURE_LABELS = (
    "soft_L1",
    "soft_L2",
    "soft_cosine_L1",
    "soft_cosine_L2",
    "decay_cosine_L1",
    "decay_cosine_L2",
)
MODEL_SPECS = {
    "soft_L12": (0, 1),
    "soft_L12_angular_L2": (0, 1, 3, 5),
    "all_main_L12": (0, 1, 2, 3, 4, 5),
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5040 = load_module("mts_5040_for_control_variate", SCRIPT_5040)
M5036 = M5040.M5036


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def complex_value(row: dict[str, float]) -> complex:
    return complex(float(row["real"]), float(row["imaginary"]))


def feature_vector(point: list[float]) -> np.ndarray:
    values = []
    for coordinate in point:
        centered = 2.0 * float(coordinate) - 1.0
        values.extend(
            (
                math.sqrt(3.0) * centered,
                math.sqrt(5.0) * 0.5 * (3.0 * centered * centered - 1.0),
            )
        )
    return np.asarray(values, dtype=float)


def load_event_observables(
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, np.ndarray]]:
    jobs = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((RUN / "jobs").glob("*.json"))
    ]
    primary = {
        (job["event_id"], job["epsilon_id"], job["base_argument_id"]): complex_value(
            job["normalized_direct_D_hhh_over_G3"]
        )
        for job in jobs
        if job["tier"] == "primary24"
        and job["status"] in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}
    }
    shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
    rows = []
    nonlocal_values: dict[tuple[str, str], np.ndarray] = {}
    for event in config["events"]:
        for epsilon_id in config["epsilon_ids"]:
            components = []
            for crossing in config["crossings"]:
                s_value = primary[(event["event_id"], epsilon_id, crossing["s_argument_id"])]
                t_value = primary[(event["event_id"], epsilon_id, crossing["t_argument_id"])]
                u_value = primary[(event["event_id"], epsilon_id, crossing["u_argument_id"])]
                components.append(
                    s_value
                    + float(crossing["t_ratio"]) ** 3 * t_value
                    + float(crossing["u_ratio"]) ** 3 * u_value
                )
            vector = np.asarray(components, dtype=np.complex128)
            _, residual, orthogonality = M5036.project_vector(vector, shape)
            if orthogonality > 1.0e-10:
                raise RuntimeError("eventwise local/nonlocal projection lost orthogonality")
            nonlocal_values[(event["event_id"], epsilon_id)] = residual
        e080 = nonlocal_values[(event["event_id"], "E080")]
        e040 = nonlocal_values[(event["event_id"], "E040")]
        e020 = nonlocal_values[(event["event_id"], "E020")]
        step_one = e040 - e080
        step_two = e020 - e040
        rows.append(
            {
                "event_id": event["event_id"],
                "seed": int(event["seed"]),
                "sample_index": int(event["sample_index"]),
                "unit_cube_point": [float(value) for value in event["unit_cube_point"]],
                "features": feature_vector(event["unit_cube_point"]),
            }
        )
        nonlocal_values[(event["event_id"], "richardson")] = 2.0 * e020 - e040
        nonlocal_values[(event["event_id"], "linear_defect")] = step_two - 0.5 * step_one
        nonlocal_values[(event["event_id"], "step_one")] = step_one
        nonlocal_values[(event["event_id"], "step_two")] = step_two
    observables = {
        name: np.stack([nonlocal_values[(row["event_id"], name)] for row in rows])
        for name in ("richardson", "linear_defect", "step_one", "step_two")
    }
    return rows, observables


def ridge_coefficients(features: np.ndarray, values: np.ndarray) -> np.ndarray:
    centered_features = features - np.mean(features, axis=0, keepdims=True)
    centered_values = values - np.mean(values, axis=0, keepdims=True)
    gram = centered_features.T @ centered_features
    scale = float(np.trace(gram) / max(1, gram.shape[0]))
    penalty = RIDGE_MULTIPLIER * max(scale, 1.0e-12)
    return np.linalg.solve(
        gram + penalty * np.eye(gram.shape[0]),
        centered_features.T @ centered_values,
    )


def pair_means(
    event_rows: list[dict[str, Any]], values: np.ndarray
) -> tuple[list[int], np.ndarray]:
    seeds = sorted({row["seed"] for row in event_rows})
    result = []
    for seed in seeds:
        indices = [index for index, row in enumerate(event_rows) if row["seed"] == seed]
        if len(indices) != 2:
            raise RuntimeError(f"seed {seed} does not have one nested pair")
        result.append(np.mean(values[indices], axis=0))
    return seeds, np.stack(result)


def crossfit(
    event_rows: list[dict[str, Any]],
    values: np.ndarray,
    feature_indices: tuple[int, ...],
) -> tuple[np.ndarray, list[dict[str, Any]]]:
    seeds = sorted({row["seed"] for row in event_rows})
    features = np.stack([row["features"] for row in event_rows])[:, feature_indices]
    adjusted = []
    folds = []
    for held_seed in seeds:
        train = np.asarray([row["seed"] != held_seed for row in event_rows], dtype=bool)
        held = ~train
        real_beta = ridge_coefficients(features[train], values[train].real)
        imaginary_beta = ridge_coefficients(features[train], values[train].imag)
        held_adjusted = (
            values[held]
            - features[held] @ real_beta
            - 1j * (features[held] @ imaginary_beta)
        )
        adjusted.append(np.mean(held_adjusted, axis=0))
        folds.append(
            {
                "held_seed": held_seed,
                "training_seeds": sorted({row["seed"] for index, row in enumerate(event_rows) if train[index]}),
                "real_coefficients": real_beta.tolist(),
                "imaginary_coefficients": imaginary_beta.tolist(),
            }
        )
    return np.stack(adjusted), folds


def ratios(adjusted: np.ndarray, raw: np.ndarray) -> dict[str, Any]:
    raw_sd = np.std(raw, axis=0, ddof=1)
    adjusted_sd = np.std(adjusted, axis=0, ddof=1)
    ratio = np.divide(
        adjusted_sd,
        raw_sd,
        out=np.full_like(adjusted_sd, math.inf, dtype=float),
        where=raw_sd > 0.0,
    )
    return {
        "raw_sd": raw_sd.tolist(),
        "adjusted_sd": adjusted_sd.tolist(),
        "sd_ratio": ratio.tolist(),
        "components_improved": int(np.sum(ratio < 1.0)),
        "maximum_ratio": float(np.max(ratio)),
        "median_ratio": float(np.median(ratio)),
    }


def serialize_coefficients(values: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in values]


def fit_locked_model(
    event_rows: list[dict[str, Any]],
    observables: dict[str, np.ndarray],
    feature_indices: tuple[int, ...],
) -> dict[str, Any]:
    features = np.stack([row["features"] for row in event_rows])[:, feature_indices]
    result = {}
    for name in ("richardson", "linear_defect", "step_one", "step_two"):
        values = observables[name]
        result[name] = {
            "real_coefficients": serialize_coefficients(
                ridge_coefficients(features, values.real)
            ),
            "imaginary_coefficients": serialize_coefficients(
                ridge_coefficients(features, values.imag)
            ),
        }
    return result


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    if config["config_digest"] != CONFIG_DIGEST:
        raise RuntimeError("locked 5040 config changed")
    status = json.loads((RUN / "status.json").read_text(encoding="utf-8"))
    if status["state"] != "COMPLETE" or status["failed_jobs"] or status["unconverged_jobs"]:
        raise RuntimeError("5040 matrix is not production-clean and complete")
    event_rows, observables = load_event_observables(config)
    feature_means = np.mean(np.stack([row["features"] for row in event_rows]), axis=0)
    budgets = config["target_precision_budgets"]
    margins = np.asarray([float(row["target_equivalence_margin"]) for row in budgets])
    model_rows = []
    component_rows = []
    model_details: dict[str, Any] = {}
    for model_name, feature_indices in MODEL_SPECS.items():
        detail: dict[str, Any] = {
            "feature_indices": list(feature_indices),
            "feature_labels": [FEATURE_LABELS[index] for index in feature_indices],
            "observables": {},
        }
        for observable_name, values in observables.items():
            seeds, raw = pair_means(event_rows, values)
            adjusted, folds = crossfit(event_rows, values, feature_indices)
            real = ratios(adjusted.real, raw.real)
            imaginary = ratios(adjusted.imag, raw.imag)
            detail["observables"][observable_name] = {
                "seeds": seeds,
                "raw_pair_values": {
                    "real": raw.real.tolist(),
                    "imaginary": raw.imag.tolist(),
                },
                "adjusted_pair_values": {
                    "real": adjusted.real.tolist(),
                    "imaginary": adjusted.imag.tolist(),
                },
                "real": real,
                "imaginary": imaginary,
                "folds": folds,
            }
            for part, metrics in (("real", real), ("imaginary", imaginary)):
                for component_index, ratio in enumerate(metrics["sd_ratio"]):
                    component_rows.append(
                        {
                            "model": model_name,
                            "observable": observable_name,
                            "part": part,
                            "component_index": component_index,
                            "physical_s_channel_cosine": config["physical_cosines"][component_index],
                            "raw_sd": metrics["raw_sd"][component_index],
                            "adjusted_sd": metrics["adjusted_sd"][component_index],
                            "sd_ratio": ratio,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
        richardson_real = detail["observables"]["richardson"]["real"]
        richardson_imaginary = detail["observables"]["richardson"]["imaginary"]
        defect_real = detail["observables"]["linear_defect"]["real"]
        defect_imaginary = detail["observables"]["linear_defect"]["imaginary"]
        raw_target_metric = max(
            value / margin for value, margin in zip(richardson_real["raw_sd"], margins)
        )
        adjusted_target_metric = max(
            value / margin
            for value, margin in zip(richardson_real["adjusted_sd"], margins)
        )
        target_metric_ratio = adjusted_target_metric / raw_target_metric
        retrospective_gate = bool(
            target_metric_ratio < 0.9
            and richardson_real["components_improved"] >= 3
            and richardson_real["maximum_ratio"] < 1.5
            and richardson_imaginary["maximum_ratio"] < 2.0
            and defect_real["maximum_ratio"] < 2.0
            and defect_imaginary["maximum_ratio"] < 2.0
        )
        detail["target_normalized_metrics"] = {
            "raw_worst_sd_over_margin": raw_target_metric,
            "adjusted_worst_sd_over_margin": adjusted_target_metric,
            "ratio": target_metric_ratio,
        }
        detail["retrospective_gate"] = retrospective_gate
        model_rows.append(
            {
                "model": model_name,
                "feature_count": len(feature_indices),
                "richardson_real_components_improved": richardson_real["components_improved"],
                "richardson_real_maximum_ratio": richardson_real["maximum_ratio"],
                "richardson_real_median_ratio": richardson_real["median_ratio"],
                "worst_target_normalized_sd_ratio": target_metric_ratio,
                "richardson_imaginary_maximum_ratio": richardson_imaginary["maximum_ratio"],
                "defect_real_maximum_ratio": defect_real["maximum_ratio"],
                "defect_imaginary_maximum_ratio": defect_imaginary["maximum_ratio"],
                "retrospective_gate": retrospective_gate,
                "valid_for_full_MTS_claim": False,
            }
        )
        model_details[model_name] = detail
    eligible = [row for row in model_rows if row["retrospective_gate"]]
    selected = (
        min(eligible, key=lambda row: row["worst_target_normalized_sd_ratio"])["model"]
        if eligible
        else None
    )
    lock = {
        "checkpoint_marker": MARKER,
        "selection_status": "LOCKED_FOR_FRESH_INDEPENDENT_PILOT" if selected else "NO_MODEL_AUTHORIZED",
        "selected_model": selected,
        "selection_used_fixed_target_values": False,
        "selection_metric": "leave-one-independent-scramble-out worst target-margin-normalized Richardson-real SD",
        "selection_data_reused_for_claim": False,
        "fresh_pilot_required": bool(selected),
        "fresh_pilot_seeds": [504201, 504202, 504203, 504204] if selected else [],
        "fresh_pilot_acceptance": {
            "all_jobs_numeric_and_converged": True,
            "coefficient_refit_forbidden": True,
            "worst_target_normalized_sd_ratio_below": 0.9,
            "richardson_real_components_improved_at_least": 3,
            "maximum_richardson_real_component_ratio_below": 1.5,
            "target_fit_or_reselection_forbidden": True,
        },
        "feature_expectation": "exactly zero under each independent Owen scramble because every shifted Legendre basis function has uniform integral zero",
        "unbiasedness_identity": "E[Y-B_train h(U) | B_train] = E[Y] when B_train is fixed independently of the fresh scramble and E[h(U)]=0",
        "locked_coefficients": (
            fit_locked_model(event_rows, observables, MODEL_SPECS[selected])
            if selected
            else None
        ),
        "valid_for_production_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    result = {
        "checkpoint_marker": MARKER,
        "config_digest": config["config_digest"],
        "completed_event_count": len(event_rows),
        "independent_scramble_count": len({row["seed"] for row in event_rows}),
        "samples_per_scramble": 2,
        "feature_labels": list(FEATURE_LABELS),
        "feature_uniform_expectations": [0.0] * len(FEATURE_LABELS),
        "empirical_feature_means_not_used_as_expectations": feature_means.tolist(),
        "ridge_multiplier": RIDGE_MULTIPLIER,
        "models": model_details,
        "model_rows": model_rows,
        "selected_model": selected,
        "fresh_pilot_authorized": bool(selected),
        "target_values_used_in_regression": False,
        "retrospective_result_valid_for_production_estimate": False,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    SOURCE.mkdir(parents=True, exist_ok=True)
    M5036.atomic_json(RESULT_JSON, result)
    M5036.atomic_json(LOCK_JSON, lock)
    write_csv(MODEL_CSV, model_rows, list(model_rows[0]))
    write_csv(COMPONENT_CSV, component_rows, list(component_rows[0]))
    validation = [
        {
            "gate": "completed_5040_source",
            "passed": status["state"] == "COMPLETE" and status["terminal_jobs"] == 378,
            "detail": "378/378, zero failed/unconverged",
        },
        {
            "gate": "exact_zero_mean_features",
            "passed": True,
            "detail": "normalized shifted Legendre L1/L2 on three uniform coordinates",
        },
        {
            "gate": "independent_leave_one_scramble_out",
            "passed": all(
                len(detail["observables"]["richardson"]["folds"]) == 4
                for detail in model_details.values()
            ),
            "detail": "each coefficient fit excludes the held Owen scramble",
        },
        {
            "gate": "target_blind_regression",
            "passed": not result["target_values_used_in_regression"],
            "detail": "target margins score variance only; target values never fit coefficients",
        },
        {
            "gate": "fresh_pilot_authorized",
            "passed": bool(selected),
            "detail": selected or "no retrospective model passes the authorization gate",
        },
        {
            "gate": "production_precision_complete",
            "passed": False,
            "detail": "retrospective design test only",
        },
        {
            "gate": "valid_for_full_MTS_claim",
            "passed": False,
            "detail": "numerical hhh variance subproblem only",
        },
    ]
    write_csv(
        VALIDATION_CSV,
        [{**row, "valid_for_full_MTS_claim": False} for row in validation],
        ["gate", "passed", "detail", "valid_for_full_MTS_claim"],
    )
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "model_rows": model_rows,
                "selected_model": selected,
                "fresh_pilot_authorized": bool(selected),
                "production_precision_complete": False,
                "valid_for_full_MTS_claim": False,
            },
            indent=2,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
