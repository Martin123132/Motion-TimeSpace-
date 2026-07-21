from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize_scalar


POST = Path(__file__).resolve().parents[1]
SCRIPT_5054 = POST / "scripts" / "Y5_R2FR_5054_projector_stratified_low_stream_allocation_gate.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5054 = POST / "source-intake" / "functional_rg" / "5054"
SOURCE = POST / "source-intake" / "functional_rg" / "5055"
RESULT_JSON = SOURCE / "variance_cost_sample_unit_repair.json"
DESIGN_CSV = SOURCE / "paired_vs_single_sample_designs.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5055_VALIDATION.csv"
)
MARKER = "MTS_5055_VARIANCE_COST_SAMPLE_UNIT_REPAIR"
REVISION = "paired-variance-event-cost-unit-repair-v1"
PROFILE = "coarse12"
HIGH_UNITS = 4
EXECUTION_CAP_HOURS = 10.0
EFFICIENCY_THRESHOLD = 0.8
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5054 = load_module("mts_5054_for_sample_units", SCRIPT_5054)
M5053 = M5054.M5053
M5049 = M5054.M5049
M5044 = M5054.M5044


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def design_metrics(
    name: str,
    evidence_role: str,
    events_per_unit: int,
    variance_high: np.ndarray,
    variance_correction: np.ndarray,
    variance_low: np.ndarray,
    margins: np.ndarray,
    high_primary_event_cost: float,
    paired_high_event_cost: float,
    low_event_cost: float,
) -> dict[str, Any]:
    high_only_unit_cost = events_per_unit * high_primary_event_cost
    correction_unit_cost = events_per_unit * paired_high_event_cost
    low_unit_cost = events_per_unit * low_event_cost
    base_score = float(np.max(np.sqrt(variance_high * high_only_unit_cost) / margins))

    def evaluate(ratio: float) -> tuple[float, np.ndarray, float]:
        variance_cost = (
            variance_correction + variance_low / ratio
        ) * (correction_unit_cost + ratio * low_unit_cost)
        component_ratios = np.sqrt(np.maximum(variance_cost, 0.0)) / margins / base_score
        return float(np.max(component_ratios)), component_ratios, variance_cost.sum()

    optimum = minimize_scalar(
        lambda log_ratio: evaluate(math.exp(log_ratio))[0],
        bounds=(math.log(0.25), math.log(512.0)),
        method="bounded",
        options={"xatol": 1.0e-12},
    )
    optimal_ratio = math.exp(float(optimum.x))
    optimal_score, optimal_components, _ = evaluate(optimal_ratio)
    integer_rows = []
    for low_units in range(1, 513):
        ratio = low_units / HIGH_UNITS
        score, components, _ = evaluate(ratio)
        runtime_hours = (
            HIGH_UNITS * correction_unit_cost + low_units * low_unit_cost
        ) / 3600.0
        integer_rows.append(
            {
                "low_units": low_units,
                "low_to_high_ratio": ratio,
                "score_ratio": score,
                "component_score_ratios": components.tolist(),
                "runtime_hours": runtime_hours,
                "within_cap": runtime_hours <= EXECUTION_CAP_HOURS,
                "passes_efficiency": score < EFFICIENCY_THRESHOLD,
            }
        )
    under_cap = [row for row in integer_rows if row["within_cap"]]
    efficient = [row for row in integer_rows if row["passes_efficiency"]]
    best_under_cap = min(under_cap, key=lambda row: row["score_ratio"]) if under_cap else None
    minimum_runtime_efficient = (
        min(efficient, key=lambda row: (row["runtime_hours"], row["score_ratio"]))
        if efficient
        else None
    )
    return {
        "design": name,
        "evidence_role": evidence_role,
        "events_per_variance_unit": events_per_unit,
        "high_only_unit_cost_seconds": high_only_unit_cost,
        "paired_correction_unit_cost_seconds": correction_unit_cost,
        "low_unit_cost_seconds": low_unit_cost,
        "continuous_optimal_low_to_high_ratio": optimal_ratio,
        "continuous_optimal_score_ratio": optimal_score,
        "continuous_optimal_component_score_ratios": optimal_components.tolist(),
        "best_integer_under_cap": best_under_cap,
        "minimum_runtime_integer_passing_efficiency": minimum_runtime_efficient,
        "sub_10_hour_efficiency_candidate": bool(
            best_under_cap
            and best_under_cap["within_cap"]
            and best_under_cap["passes_efficiency"]
        ),
        "variance_high": variance_high.tolist(),
        "variance_correction": variance_correction.tolist(),
        "variance_low_contribution": variance_low.tolist(),
    }


def main() -> None:
    source_5053_path = SOURCE_5053 / "high_low_cost_provenance_and_reuse_audit.json"
    source_5054_path = SOURCE_5054 / "projector_stratified_low_stream_allocation_gate.json"
    required = [SCRIPT_5054, source_5053_path, source_5054_path]
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
        rows = M5044.event_dataset(config)
        shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
        projector = np.eye(5) - np.outer(shape, shape) / float(shape @ shape)
        high_complex_rows = []
        correction_channel_rows = []
        low_contribution_rows = []
        for row in rows:
            event_id = str(row["event_id"])
            e020 = {
                base_id: M5049.M5043.complex_value(
                    M5049.M5043.primary_job("E020", event_id, base_id)[
                        "normalized_direct_D_hhh_over_G3"
                    ]
                )
                for base_id in row["coarse"]
            }
            high_raw = 2.0 * M5054.raw_cyclic(config, e020) - M5054.raw_cyclic(
                config, row["full"]
            )
            low_raw = M5054.raw_cyclic(config, row["coarse"])
            high = projector @ high_raw
            correction = projector @ (high_raw - low_raw)
            low = projector @ low_raw
            high_complex_rows.append(high)
            correction_channel_rows.append(
                np.concatenate((correction.real, high.imag))
            )
            low_contribution_rows.append(
                np.concatenate((low.real, np.zeros(5, dtype=float)))
            )
        high_channels = M5049.M5043.channel_matrix(np.stack(high_complex_rows))
        correction_channels = np.stack(correction_channel_rows)
        low_channels = np.stack(low_contribution_rows)
        _, paired_high = M5049.M5043.pair_means(rows, high_channels)
        _, paired_correction = M5049.M5043.pair_means(rows, correction_channels)
        _, paired_low = M5049.M5043.pair_means(rows, low_channels)
        paired_variances = (
            np.var(paired_high, axis=0, ddof=1),
            np.var(paired_correction, axis=0, ddof=1),
            np.var(paired_low, axis=0, ddof=1),
        )
        single_variances = []
        for sample_index in (0, 1):
            selected = np.asarray(
                [int(row["sample_index"]) == sample_index for row in rows]
            )
            single_variances.append(
                (
                    np.var(high_channels[selected], axis=0, ddof=1),
                    np.var(correction_channels[selected], axis=0, ddof=1),
                    np.var(low_channels[selected], axis=0, ddof=1),
                )
            )
        conservative_variances = tuple(
            np.maximum(single_variances[0][index], single_variances[1][index])
            for index in range(3)
        )
        source_5053 = json.loads(source_5053_path.read_text(encoding="utf-8"))
        high_primary_event_cost = float(source_5053["mean_high_primary_event_cost_seconds"])
        paired_high_event_cost = float(
            source_5053["mean_paired_high_correction_event_cost_seconds"]
        )
        low_event_cost = float(source_5053["mean_low_only_total_event_cost_seconds"])
        real_margins = np.asarray(
            [
                float(row["target_equivalence_margin"])
                for row in config["target_precision_budgets"]
            ]
        )
        margins = np.concatenate((real_margins, real_margins))
        designs = [
            design_metrics(
                "paired_nested_two_event",
                "admissible paired design",
                2,
                *paired_variances,
                margins,
                high_primary_event_cost,
                paired_high_event_cost,
                low_event_cost,
            ),
            design_metrics(
                "single_sample_index_0",
                "diagnostic stratum only",
                1,
                *single_variances[0],
                margins,
                high_primary_event_cost,
                paired_high_event_cost,
                low_event_cost,
            ),
            design_metrics(
                "single_sample_index_1",
                "diagnostic stratum only",
                1,
                *single_variances[1],
                margins,
                high_primary_event_cost,
                paired_high_event_cost,
                low_event_cost,
            ),
            design_metrics(
                "single_componentwise_conservative",
                "admissible conservative envelope",
                1,
                *conservative_variances,
                margins,
                high_primary_event_cost,
                paired_high_event_cost,
                low_event_cost,
            ),
        ]
        admissible = [
            row
            for row in designs
            if row["evidence_role"] in {
                "admissible paired design",
                "admissible conservative envelope",
            }
        ]
        sub_cap = [row for row in admissible if row["sub_10_hour_efficiency_candidate"]]
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
                admissible,
                key=lambda row: (
                    row["minimum_runtime_integer_passing_efficiency"]["runtime_hours"]
                    if row["minimum_runtime_integer_passing_efficiency"]
                    else math.inf,
                    row["continuous_optimal_score_ratio"],
                ),
            )
        )
        source_5054 = json.loads(source_5054_path.read_text(encoding="utf-8"))
        paired_source_score = float(
            source_5054["selected_partition"]["continuous_equal_cost_score_ratio"]
        )
        paired_score_difference = abs(
            designs[0]["continuous_optimal_score_ratio"] - paired_source_score
        )
        old_projected_hours = float(
            source_5054["selected_allocation"]["runtime_hours"]
        )
        repaired_paired_threshold = designs[0][
            "minimum_runtime_integer_passing_efficiency"
        ]
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "finding": "paired seed-mean variances require two event runtimes per independent variance unit",
            "designs": designs,
            "admissible_designs": [row["design"] for row in admissible],
            "selected_admissible_design": selected["design"],
            "sub_10_hour_admissible_candidate_count": len(sub_cap),
            "old_unrepaired_paired_threshold_hours": old_projected_hours,
            "repaired_paired_threshold_hours": (
                repaired_paired_threshold["runtime_hours"]
                if repaired_paired_threshold
                else None
            ),
            "single_strata_are_diagnostics_not_posthoc_selection_candidates": True,
            "fresh_kernel_execution_authorized": False,
            "delete_one_seed_reaudit_required": bool(sub_cap),
            "decision": (
                "SUB_10_HOUR_SINGLE_EVENT_ENVELOPE_REQUIRES_JACKKNIFE"
                if sub_cap
                else "NO_UNIT_CONSISTENT_ROUTE_BELOW_10_HOURS"
            ),
            "target_central_values_used": False,
            "retrospective_design_only": True,
            "restricted_scope_audit": scope,
            "source_reproduction": {
                "paired_score_difference_from_5054": paired_score_difference,
            },
            "formalization_workbench_tree_sha256": M5049.M5043.tree_digest(
                POST.parent / "formalization-workbench"
            ),
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(RESULT_JSON, result)
        SOURCE.mkdir(parents=True, exist_ok=True)
        summary_rows = []
        for row in designs:
            under = row["best_integer_under_cap"]
            efficient = row["minimum_runtime_integer_passing_efficiency"]
            summary_rows.append(
                {
                    "design": row["design"],
                    "evidence_role": row["evidence_role"],
                    "events_per_variance_unit": row["events_per_variance_unit"],
                    "continuous_optimal_score_ratio": row[
                        "continuous_optimal_score_ratio"
                    ],
                    "best_under_cap_score_ratio": under["score_ratio"] if under else None,
                    "best_under_cap_runtime_hours": under["runtime_hours"] if under else None,
                    "minimum_efficiency_runtime_hours": (
                        efficient["runtime_hours"] if efficient else None
                    ),
                    "sub_10_hour_efficiency_candidate": row[
                        "sub_10_hour_efficiency_candidate"
                    ],
                }
            )
        with DESIGN_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
            writer.writeheader()
            writer.writerows(summary_rows)
        checks = [
            ("source_5054_exists", source_5054_path.exists(), str(source_5054_path)),
            ("paired_design_uses_two_events", designs[0]["events_per_variance_unit"] == 2, str(designs[0]["events_per_variance_unit"])),
            (
                "paired_score_ratio_reproduced",
                paired_score_difference <= 1.0e-6,
                str(paired_score_difference),
            ),
            (
                "paired_runtime_factor_repaired",
                repaired_paired_threshold is not None
                and repaired_paired_threshold["runtime_hours"] >= 1.99 * old_projected_hours,
                f"old={old_projected_hours}; repaired={repaired_paired_threshold['runtime_hours'] if repaired_paired_threshold else None}",
            ),
            ("both_single_strata_audited", {row["design"] for row in designs[1:3]} == {"single_sample_index_0", "single_sample_index_1"}, "required both"),
            ("single_strata_not_selected_posthoc", result["single_strata_are_diagnostics_not_posthoc_selection_candidates"], "required true"),
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
                    "designs": [
                        {
                            "design": row["design"],
                            "optimal_score": row["continuous_optimal_score_ratio"],
                            "best_under_cap": (
                                row["best_integer_under_cap"]["score_ratio"]
                                if row["best_integer_under_cap"]
                                else None
                            ),
                            "minimum_efficiency_hours": (
                                row["minimum_runtime_integer_passing_efficiency"][
                                    "runtime_hours"
                                ]
                                if row["minimum_runtime_integer_passing_efficiency"]
                                else None
                            ),
                            "sub_10_hour": row["sub_10_hour_efficiency_candidate"],
                        }
                        for row in designs
                    ],
                    "selected_admissible_design": selected["design"],
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
