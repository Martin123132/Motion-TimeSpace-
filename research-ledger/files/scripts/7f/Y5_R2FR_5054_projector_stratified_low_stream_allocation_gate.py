from __future__ import annotations

import csv
import importlib.util
import itertools
import json
import math
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from scipy.optimize import differential_evolution


POST = Path(__file__).resolve().parents[1]
SCRIPT_5053 = POST / "scripts" / "Y5_R2FR_5053_high_low_cost_provenance_and_reuse_audit.py"
SOURCE_5051 = POST / "source-intake" / "functional_rg" / "5051"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE = POST / "source-intake" / "functional_rg" / "5054"
RESULT_JSON = SOURCE / "projector_stratified_low_stream_allocation_gate.json"
PARTITION_CSV = SOURCE / "projector_partition_allocation_comparison.csv"
SELECTED_CSV = SOURCE / "selected_projector_stream_allocation.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5054_VALIDATION.csv"
)
MARKER = "MTS_5054_PROJECTOR_STRATIFIED_LOW_STREAM_ALLOCATION_GATE"
REVISION = "exact-projector-partitioned-low-stream-v1"
PROFILE = "coarse12"
HIGH_UNITS = 4
EXECUTION_CAP_HOURS = 10.0
EFFICIENCY_THRESHOLD = 0.8
DIAGNOSTIC_RUNTIME_HOURS = 48.0
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5053 = load_module("mts_5053_for_projector_streams", SCRIPT_5053)
M5052 = M5053.M5052
M5051 = M5053.M5051
M5049 = M5053.M5049
M5044 = M5053.M5044


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def raw_cyclic(config: dict[str, Any], values: dict[str, complex]) -> np.ndarray:
    return np.asarray(
        [
            values[str(crossing["s_argument_id"])]
            + float(crossing["t_ratio"]) ** 3 * values[str(crossing["t_argument_id"])]
            + float(crossing["u_ratio"]) ** 3 * values[str(crossing["u_argument_id"])]
            for crossing in config["crossings"]
        ],
        dtype=np.complex128,
    )


def set_partitions(values: tuple[int, ...]) -> Iterable[tuple[tuple[int, ...], ...]]:
    if not values:
        yield tuple()
        return
    first = values[0]
    for partition in set_partitions(values[1:]):
        yield ((first,), *partition)
        for index in range(len(partition)):
            block = tuple(sorted((first, *partition[index])))
            yield (*partition[:index], block, *partition[index + 1 :])


def canonical_partition(partition: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((tuple(sorted(block)) for block in partition), key=lambda block: block[0]))


def partition_label(partition: tuple[tuple[int, ...], ...]) -> str:
    return "|".join("{" + ",".join(str(value) for value in block) + "}" for block in partition)


def block_low_variance(
    projector: np.ndarray,
    raw_low_pairs: np.ndarray,
    block: tuple[int, ...],
) -> np.ndarray:
    indices = list(block)
    values = raw_low_pairs[:, indices]
    covariance = np.atleast_2d(np.cov(values, rowvar=False, ddof=1))
    projection = projector[:, indices]
    real_diagonal = np.diag(projection @ covariance @ projection.T)
    return np.concatenate((real_diagonal, np.zeros(5, dtype=float)))


def evaluate_allocation(
    ratios: np.ndarray,
    block_variances: list[np.ndarray],
    block_costs: np.ndarray,
    variance_correction: np.ndarray,
    margins: np.ndarray,
    paired_high_cost: float,
    base_score: float,
) -> tuple[float, float, np.ndarray]:
    effective_variance = variance_correction.copy()
    for ratio, contribution in zip(ratios, block_variances):
        effective_variance += contribution / ratio
    cost = paired_high_cost + float(np.dot(ratios, block_costs))
    component_scores = np.sqrt(np.maximum(effective_variance * cost, 0.0)) / margins
    return float(np.max(component_scores) / base_score), cost, component_scores / base_score


def integer_candidates(
    centers: list[np.ndarray],
    block_costs: np.ndarray,
    paired_high_cost: float,
) -> Iterable[tuple[int, ...]]:
    cap_seconds = DIAGNOSTIC_RUNTIME_HOURS * 3600.0
    minimum_other = float(np.sum(block_costs))
    option_sets = []
    for index, cost in enumerate(block_costs):
        maximum = max(
            1,
            int(
                math.floor(
                    (cap_seconds - HIGH_UNITS * paired_high_cost - minimum_other + cost)
                    / cost
                )
            ),
        )
        options = {1, maximum}
        for center in centers:
            value = int(round(HIGH_UNITS * float(center[index])))
            options.update(range(max(1, value - 4), min(maximum, value + 4) + 1))
        option_sets.append(sorted(options))
    yield from itertools.product(*option_sets)


def optimize_partition(
    partition: tuple[tuple[int, ...], ...],
    block_variances: list[np.ndarray],
    block_costs: np.ndarray,
    variance_correction: np.ndarray,
    margins: np.ndarray,
    paired_high_cost: float,
    base_score: float,
    seed: int,
) -> dict[str, Any]:
    dimension = len(partition)
    bounds = [(math.log(0.25), math.log(512.0))] * dimension

    def metrics(log_ratios: np.ndarray) -> tuple[float, float, np.ndarray]:
        return evaluate_allocation(
            np.exp(log_ratios),
            block_variances,
            block_costs,
            variance_correction,
            margins,
            paired_high_cost,
            base_score,
        )

    equal = differential_evolution(
        lambda values: metrics(values)[0],
        bounds,
        seed=seed,
        popsize=8,
        maxiter=80,
        tol=1.0e-9,
        polish=True,
        workers=1,
    )
    cap_cost_per_high = EXECUTION_CAP_HOURS * 3600.0 / HIGH_UNITS

    def cap_objective(values: np.ndarray) -> float:
        score, cost, _ = metrics(values)
        excess = max(0.0, cost / cap_cost_per_high - 1.0)
        return score + 1.0e3 * excess * excess + 1.0e3 * excess

    cap = differential_evolution(
        cap_objective,
        bounds,
        seed=seed + 1000,
        popsize=8,
        maxiter=100,
        tol=1.0e-9,
        polish=True,
        workers=1,
    )

    def threshold_objective(values: np.ndarray) -> float:
        score, cost, _ = metrics(values)
        excess = max(0.0, score / EFFICIENCY_THRESHOLD - 1.0)
        return cost / cap_cost_per_high + 1.0e4 * excess * excess + 1.0e4 * excess

    threshold = differential_evolution(
        threshold_objective,
        bounds,
        seed=seed + 2000,
        popsize=8,
        maxiter=100,
        tol=1.0e-9,
        polish=True,
        workers=1,
    )
    centers = [np.exp(equal.x), np.exp(cap.x), np.exp(threshold.x)]
    feasible = []
    for counts in integer_candidates(centers, block_costs, paired_high_cost):
        ratios = np.asarray(counts, dtype=float) / HIGH_UNITS
        score, cost, component_ratios = evaluate_allocation(
            ratios,
            block_variances,
            block_costs,
            variance_correction,
            margins,
            paired_high_cost,
            base_score,
        )
        runtime_hours = HIGH_UNITS * cost / 3600.0
        feasible.append(
            {
                "low_unit_counts": list(counts),
                "low_to_high_ratios": ratios.tolist(),
                "score_ratio": score,
                "runtime_hours": runtime_hours,
                "component_score_ratios": component_ratios.tolist(),
                "within_execution_cap": runtime_hours <= EXECUTION_CAP_HOURS + 1.0e-12,
                "passes_efficiency": score < EFFICIENCY_THRESHOLD,
            }
        )
    cap_feasible = [row for row in feasible if row["within_execution_cap"]]
    efficient = [row for row in feasible if row["passes_efficiency"]]
    best_under_cap = min(cap_feasible, key=lambda row: row["score_ratio"])
    minimum_runtime_efficient = (
        min(efficient, key=lambda row: (row["runtime_hours"], row["score_ratio"]))
        if efficient
        else None
    )
    equal_ratios = np.exp(equal.x)
    equal_score, equal_cost, _ = evaluate_allocation(
        equal_ratios,
        block_variances,
        block_costs,
        variance_correction,
        margins,
        paired_high_cost,
        base_score,
    )
    return {
        "partition": [list(block) for block in partition],
        "partition_label": partition_label(partition),
        "block_count": dimension,
        "block_costs_seconds": block_costs.tolist(),
        "continuous_equal_cost_ratios": equal_ratios.tolist(),
        "continuous_equal_cost_score_ratio": equal_score,
        "continuous_equal_cost_runtime_for_four_high_hours": HIGH_UNITS * equal_cost / 3600.0,
        "best_integer_under_cap": best_under_cap,
        "minimum_runtime_integer_passing_efficiency": minimum_runtime_efficient,
        "sub_10_hour_efficiency_candidate": bool(
            best_under_cap["passes_efficiency"] and best_under_cap["within_execution_cap"]
        ),
    }


def main() -> None:
    source_5053_path = SOURCE_5053 / "high_low_cost_provenance_and_reuse_audit.json"
    cost_rows_path = SOURCE_5053 / "high_low_cost_rows.csv"
    source_5051_path = SOURCE_5051 / "phase_covariant_complex_control_gate.json"
    required = [SCRIPT_5053, source_5053_path, cost_rows_path, source_5051_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    M5049.configure_modules()
    try:
        scope = M5049.strict_scope_audit(PROFILE)
        if not scope["all_theorem_zeros_within_restricted_scope"]:
            raise RuntimeError("restricted theorem-scope audit failed")
        M5044.M5043 = M5049.M5043
        config = M5049.M5043.load_config()
        event_rows = M5044.event_dataset(config)
        raw_high = []
        raw_low = []
        projected_high = []
        projected_correction = []
        for row in event_rows:
            event_id = str(row["event_id"])
            e020_values = {
                base_id: M5049.M5043.complex_value(
                    M5049.M5043.primary_job("E020", event_id, base_id)[
                        "normalized_direct_D_hhh_over_G3"
                    ]
                )
                for base_id in row["coarse"]
            }
            e040_values = row["full"]
            low_values = row["coarse"]
            high_vector = 2.0 * raw_cyclic(config, e020_values) - raw_cyclic(
                config, e040_values
            )
            low_vector = raw_cyclic(config, low_values)
            shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
            projector = np.eye(5) - np.outer(shape, shape) / float(shape @ shape)
            high_residual = projector @ high_vector
            correction = projector @ (high_vector - low_vector)
            raw_high.append(high_vector)
            raw_low.append(low_vector)
            projected_high.append(high_residual)
            projected_correction.append(correction)
        raw_high_array = np.stack(raw_high)
        raw_low_array = np.stack(raw_low)
        high_complex = np.stack(projected_high)
        correction_complex = np.stack(projected_correction)
        high_channels = M5049.M5043.channel_matrix(high_complex)
        correction_channels = np.concatenate(
            (correction_complex.real, high_complex.imag), axis=1
        )
        seeds, high_pairs = M5049.M5043.pair_means(event_rows, high_channels)
        correction_seeds, correction_pairs = M5049.M5043.pair_means(
            event_rows, correction_channels
        )
        raw_seeds, raw_low_pairs = M5049.M5043.pair_means(
            event_rows, raw_low_array.real
        )
        if seeds != correction_seeds or seeds != raw_seeds:
            raise RuntimeError("paired seed order differs")
        variance_high = np.var(high_pairs, axis=0, ddof=1)
        variance_correction = np.var(correction_pairs, axis=0, ddof=1)
        source_5051 = json.loads(source_5051_path.read_text(encoding="utf-8"))
        selected_5051 = source_5051["selected"]
        high_variance_difference = float(
            np.max(
                np.abs(
                    variance_high
                    - np.asarray(selected_5051["variance_high"], dtype=float)
                )
            )
        )
        correction_variance_difference = float(
            np.max(
                np.abs(
                    variance_correction
                    - np.asarray(
                        selected_5051["variance_crossfit_correction"], dtype=float
                    )
                )
            )
        )
        source_5053 = json.loads(source_5053_path.read_text(encoding="utf-8"))
        high_only_cost = float(source_5053["mean_high_primary_event_cost_seconds"])
        paired_high_cost = float(
            source_5053["mean_paired_high_correction_event_cost_seconds"]
        )
        cost_rows = list(csv.DictReader(cost_rows_path.open(encoding="utf-8")))
        cost_lookup = {
            (row["event_id"], row["base_argument_id"]): float(
                row["e040_topology_runtime_seconds"]
            )
            + float(row["low_kernel_runtime_seconds"])
            for row in cost_rows
        }
        crossing_arguments = [
            (
                str(crossing["s_argument_id"]),
                str(crossing["t_argument_id"]),
                str(crossing["u_argument_id"]),
            )
            for crossing in config["crossings"]
        ]
        flattened_arguments = [value for group in crossing_arguments for value in group]
        disjoint_argument_partition = len(flattened_arguments) == len(set(flattened_arguments)) == 15
        component_costs = []
        for arguments in crossing_arguments:
            per_event = [
                sum(cost_lookup[(str(event["event_id"]), base_id)] for base_id in arguments)
                for event in config["events"]
            ]
            component_costs.append(float(np.mean(per_event)))
        component_costs_array = np.asarray(component_costs, dtype=float)
        low_cost_reproduction_difference = abs(
            float(np.sum(component_costs_array))
            - float(source_5053["mean_low_only_total_event_cost_seconds"])
        )
        real_margins = np.asarray(
            [
                float(row["target_equivalence_margin"])
                for row in config["target_precision_budgets"]
            ]
        )
        margins = np.concatenate((real_margins, real_margins))
        base_score = float(np.max(np.sqrt(variance_high * high_only_cost) / margins))
        unique_partitions = sorted(
            {canonical_partition(value) for value in set_partitions(tuple(range(5)))},
            key=lambda value: (len(value), partition_label(value)),
        )
        partition_results = []
        for index, partition in enumerate(unique_partitions):
            block_variances = [
                block_low_variance(projector, raw_low_pairs, block) for block in partition
            ]
            block_costs = np.asarray(
                [sum(component_costs[value] for value in block) for block in partition],
                dtype=float,
            )
            partition_results.append(
                optimize_partition(
                    partition,
                    block_variances,
                    block_costs,
                    variance_correction,
                    margins,
                    paired_high_cost,
                    base_score,
                    505400 + index,
                )
            )
        sub_cap = [row for row in partition_results if row["sub_10_hour_efficiency_candidate"]]
        efficient_runtime = [
            (row, row["minimum_runtime_integer_passing_efficiency"])
            for row in partition_results
            if row["minimum_runtime_integer_passing_efficiency"] is not None
        ]
        selected = (
            min(
                sub_cap,
                key=lambda row: (
                    row["best_integer_under_cap"]["runtime_hours"],
                    row["best_integer_under_cap"]["score_ratio"],
                ),
            )
            if sub_cap
            else min(
                efficient_runtime,
                key=lambda pair: (
                    pair[1]["runtime_hours"],
                    pair[1]["score_ratio"],
                ),
            )[0]
        )
        selected_allocation = (
            selected["best_integer_under_cap"]
            if selected["sub_10_hour_efficiency_candidate"]
            else selected["minimum_runtime_integer_passing_efficiency"]
        )
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "exact_estimator": "mean_H(P(Hraw-Lraw))+P*independent_component_stream_means(Lraw)",
            "projector": projector.tolist(),
            "raw_component_crossing_arguments": [list(value) for value in crossing_arguments],
            "raw_component_mean_costs_seconds": component_costs,
            "raw_components_use_disjoint_argument_sets": disjoint_argument_partition,
            "partition_family_complete": len(unique_partitions) == 52,
            "partition_count": len(unique_partitions),
            "high_units": HIGH_UNITS,
            "high_only_event_cost_seconds": high_only_cost,
            "paired_high_correction_event_cost_seconds": paired_high_cost,
            "execution_cap_hours": EXECUTION_CAP_HOURS,
            "efficiency_threshold": EFFICIENCY_THRESHOLD,
            "partition_results": partition_results,
            "sub_10_hour_efficiency_candidate_count": len(sub_cap),
            "selected_partition": selected,
            "selected_allocation": selected_allocation,
            "delete_one_seed_reaudit_required": bool(sub_cap),
            "fresh_kernel_execution_authorized": False,
            "decision": (
                "SUB_10_HOUR_PROJECTOR_STREAM_CANDIDATE_REQUIRES_JACKKNIFE"
                if sub_cap
                else "NO_PROJECTOR_STREAM_ROUTE_BELOW_10_HOURS"
            ),
            "target_central_values_used": False,
            "retrospective_design_only": True,
            "restricted_scope_audit": scope,
            "source_reproduction": {
                "maximum_high_variance_difference": high_variance_difference,
                "maximum_correction_variance_difference": correction_variance_difference,
                "low_cost_reproduction_difference_seconds": low_cost_reproduction_difference,
            },
            "formalization_workbench_tree_sha256": M5049.M5043.tree_digest(
                POST.parent / "formalization-workbench"
            ),
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(RESULT_JSON, result)
        SOURCE.mkdir(parents=True, exist_ok=True)
        summary_rows = []
        for row in partition_results:
            threshold = row["minimum_runtime_integer_passing_efficiency"]
            summary_rows.append(
                {
                    "partition_label": row["partition_label"],
                    "block_count": row["block_count"],
                    "continuous_equal_cost_score_ratio": row[
                        "continuous_equal_cost_score_ratio"
                    ],
                    "best_under_cap_score_ratio": row["best_integer_under_cap"][
                        "score_ratio"
                    ],
                    "best_under_cap_runtime_hours": row["best_integer_under_cap"][
                        "runtime_hours"
                    ],
                    "sub_10_hour_efficiency_candidate": row[
                        "sub_10_hour_efficiency_candidate"
                    ],
                    "minimum_efficiency_runtime_hours": (
                        threshold["runtime_hours"] if threshold else None
                    ),
                }
            )
        with PARTITION_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
            writer.writeheader()
            writer.writerows(summary_rows)
        selected_rows = []
        for block, cost, count, ratio in zip(
            selected["partition"],
            selected["block_costs_seconds"],
            selected_allocation["low_unit_counts"],
            selected_allocation["low_to_high_ratios"],
        ):
            selected_rows.append(
                {
                    "raw_component_indices": ",".join(str(value) for value in block),
                    "physical_cosines": ",".join(
                        f"{config['physical_cosines'][value]:+.1f}" for value in block
                    ),
                    "argument_ids": ",".join(
                        value for index in block for value in crossing_arguments[index]
                    ),
                    "mean_stream_cost_seconds": cost,
                    "low_units": count,
                    "low_to_high_ratio": ratio,
                }
            )
        with SELECTED_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(selected_rows[0]))
            writer.writeheader()
            writer.writerows(selected_rows)
        checks = [
            ("source_5053_exists", source_5053_path.exists(), str(source_5053_path)),
            ("all_five_raw_components_present", len(crossing_arguments) == 5, str(len(crossing_arguments))),
            ("raw_argument_groups_disjoint", disjoint_argument_partition, str(crossing_arguments)),
            ("complete_set_partition_family", len(unique_partitions) == 52, str(len(unique_partitions))),
            (
                "high_variance_reproduced",
                high_variance_difference <= 1.0e-9,
                str(high_variance_difference),
            ),
            (
                "unit_correction_variance_reproduced",
                correction_variance_difference <= 1.0e-9,
                str(correction_variance_difference),
            ),
            (
                "low_cost_reproduced",
                low_cost_reproduction_difference <= 1.0e-9,
                str(low_cost_reproduction_difference),
            ),
            (
                "all_partition_outputs_finite",
                all(
                    math.isfinite(row["best_integer_under_cap"]["score_ratio"])
                    for row in partition_results
                ),
                "required true",
            ),
            ("fresh_kernels_not_authorized", not result["fresh_kernel_execution_authorized"], "required false"),
            ("target_central_values_not_used", not result["target_central_values_used"], "required false"),
            (
                "restricted_scope_passes",
                scope["all_theorem_zeros_within_restricted_scope"],
                f"strict={scope['strict_scope_rows']}; total={scope['theorem_zero_rows']}",
            ),
            ("fresh_evidence_not_claimed", not result["valid_for_full_MTS_claim"], "required false"),
            (
                "formalization_workbench_unchanged",
                result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
                result["formalization_workbench_tree_sha256"],
            ),
        ]
        validation = [
            {"check": name, "passed": str(bool(passed)).lower(), "evidence": evidence}
            for name, passed, evidence in checks
        ]
        VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
        with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
            writer.writeheader()
            writer.writerows(validation)
        print(
            json.dumps(
                {
                    "partition_count": len(unique_partitions),
                    "component_costs_seconds": component_costs,
                    "sub_10_hour_candidates": len(sub_cap),
                    "selected_partition": selected["partition_label"],
                    "selected_counts": selected_allocation["low_unit_counts"],
                    "selected_score_ratio": selected_allocation["score_ratio"],
                    "selected_runtime_hours": selected_allocation["runtime_hours"],
                    "decision": result["decision"],
                    "validation_passed": sum(row["passed"] == "true" for row in validation),
                    "validation_total": len(validation),
                },
                indent=2,
            )
        )
    finally:
        M5049.restore_modules()


if __name__ == "__main__":
    main()
