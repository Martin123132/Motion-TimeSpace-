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
SCRIPT_5043 = POST / "scripts" / "Y5_R2FR_5043_theorem_first_coarse_E040_multilevel_gate.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5044"
RESULT_JSON = SOURCE / "symmetric_hybrid_fidelity_gate.json"
FAMILY_CSV = SOURCE / "symmetric_threshold_family.csv"
COMPONENT_CSV = SOURCE / "selected_component_gate.csv"
LOCK_JSON = SOURCE / "locked_reserve_multilevel_pilot.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5044_VALIDATION.csv"
)
MARKER = "MTS_5044_SYMMETRIC_HYBRID_FIDELITY_GATE"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
PROFILE = "coarse12"
GROUPS = (
    ("A00", "A14"),
    ("A01", "A13"),
    ("A02", "A12"),
    ("A03", "A11"),
    ("A04", "A10"),
    ("A05", "A09"),
    ("A06", "A08"),
    ("A07",),
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5043 = load_module("mts_5043_for_symmetric_hybrid", SCRIPT_5043)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def residual(config: dict[str, Any], values: dict[str, complex]) -> np.ndarray:
    return M5043.cyclic_nonlocal(
        config, {(base_id, "value"): value for base_id, value in values.items()}
    )


def event_dataset(config: dict[str, Any]) -> list[dict[str, Any]]:
    events = sorted(config["events"], key=lambda row: (row["seed"], row["sample_index"]))
    base_ids = sorted(M5043.argument_lookup(config))
    rows = []
    for event in events:
        event_id = event["event_id"]
        coarse: dict[str, complex] = {}
        full: dict[str, complex] = {}
        e020: dict[str, complex] = {}
        coarse_kernel_costs: dict[str, float] = {}
        full_kernel_costs: dict[str, float] = {}
        high_cost = 0.0
        topology_cost = 0.0
        for base_id in base_ids:
            low_path = M5043.result_path(PROFILE, event_id, base_id)
            low = json.loads(low_path.read_text(encoding="utf-8"))
            if low.get("status") != "COMPLETED_CONVERGED":
                raise RuntimeError(f"5043 source row is not converged: {low_path}")
            e040_job = M5043.primary_job("E040", event_id, base_id)
            e020_job = M5043.primary_job("E020", event_id, base_id)
            coarse[base_id] = M5043.complex_value(
                low["normalized_direct_D_hhh_over_G3"]
            )
            full[base_id] = M5043.complex_value(
                e040_job["normalized_direct_D_hhh_over_G3"]
            )
            e020[base_id] = M5043.complex_value(
                e020_job["normalized_direct_D_hhh_over_G3"]
            )
            e040_runtime, e040_topology, _ = M5043.source_runtime(e040_job)
            e020_runtime, _, _ = M5043.source_runtime(e020_job)
            high_cost += e040_runtime + e020_runtime
            topology_cost += e040_topology
            coarse_kernel_costs[base_id] = float(low["kernel_runtime_seconds"])
            full_kernel_costs[base_id] = max(0.0, e040_runtime - e040_topology)
        rows.append(
            {
                **event,
                "coarse": coarse,
                "full": full,
                "high": 2.0 * residual(config, e020) - residual(config, full),
                "high_cost": high_cost,
                "topology_cost": topology_cost,
                "coarse_kernel_costs": coarse_kernel_costs,
                "full_kernel_costs": full_kernel_costs,
            }
        )
    return rows


def selected_arguments(upgraded_group_count: int) -> set[str]:
    return {
        base_id
        for group in GROUPS[:upgraded_group_count]
        for base_id in group
    }


def hybrid_matrix(
    config: dict[str, Any], rows: list[dict[str, Any]], upgraded_group_count: int
) -> tuple[np.ndarray, float]:
    selected = selected_arguments(upgraded_group_count)
    values = []
    costs = []
    for row in rows:
        arguments = {
            base_id: (
                row["full"][base_id]
                if base_id in selected
                else row["coarse"][base_id]
            )
            for base_id in row["coarse"]
        }
        values.append(residual(config, arguments))
        costs.append(
            row["topology_cost"]
            + sum(
                row["full_kernel_costs"][base_id]
                if base_id in selected
                else row["coarse_kernel_costs"][base_id]
                for base_id in arguments
            )
        )
    return M5043.channel_matrix(np.stack(values)), float(np.mean(costs))


def crossfit(
    rows: list[dict[str, Any]], high: np.ndarray, low: np.ndarray
) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]]]:
    seeds = sorted({int(row["seed"]) for row in rows})
    pairs = []
    folds = []
    for held_seed in seeds:
        train = np.asarray([row["seed"] != held_seed for row in rows], dtype=bool)
        held = ~train
        betas = np.asarray(
            [
                M5043.scalar_beta(low[train, index], high[train, index])
                for index in range(high.shape[1])
            ]
        )
        pairs.append(np.mean(high[held] - low[held] * betas, axis=0))
        folds.append(
            {
                "held_seed": held_seed,
                "training_seeds": [seed for seed in seeds if seed != held_seed],
                "betas": betas.tolist(),
            }
        )
    return np.stack(pairs), np.asarray(
        [M5043.scalar_beta(low[:, index], high[:, index]) for index in range(high.shape[1])]
    ), folds


def assess(
    config: dict[str, Any],
    rows: list[dict[str, Any]],
    upgraded_group_count: int,
    high: np.ndarray,
    raw_pairs: np.ndarray,
    variance_high: np.ndarray,
    high_cost: float,
    margins: np.ndarray,
    base_score: float,
) -> dict[str, Any]:
    low, low_cost = hybrid_matrix(config, rows, upgraded_group_count)
    correction_pairs, beta, folds = crossfit(rows, high, low)
    _, low_pairs = M5043.pair_means(rows, low)
    variance_correction = np.var(correction_pairs, axis=0, ddof=1)
    variance_low = np.var(low_pairs, axis=0, ddof=1)
    raw_sd = np.std(raw_pairs, axis=0, ddof=1)
    correction_sd = np.std(correction_pairs, axis=0, ddof=1)
    crossfit_ratio = np.divide(
        correction_sd,
        raw_sd,
        out=np.full_like(raw_sd, math.inf),
        where=raw_sd > 0.0,
    )
    allocation_rows = []
    for sample_ratio in np.geomspace(0.25, 512.0, 4097):
        variance_cost = (
            variance_correction + beta * beta * variance_low / sample_ratio
        ) * (high_cost + sample_ratio * low_cost)
        score = float(
            np.max(np.sqrt(np.maximum(variance_cost, 0.0)) / margins)
        )
        allocation_rows.append((float(sample_ratio), score, score / base_score))
    optimal_ratio, optimal_score, score_ratio = min(
        allocation_rows, key=lambda row: row[1]
    )
    selected = sorted(selected_arguments(upgraded_group_count))
    return {
        "upgraded_group_count": upgraded_group_count,
        "upgraded_argument_count": len(selected),
        "upgraded_arguments": selected,
        "coarse_arguments": sorted(set(rows[0]["coarse"]) - set(selected)),
        "minimum_upgraded_absolute_argument": (
            min(
                abs(float(M5043.argument_lookup(config)[base_id]["argument"]))
                for base_id in selected
            )
            if selected
            else None
        ),
        "mean_low_event_cost_seconds": low_cost,
        "low_to_high_cost_ratio": low_cost / high_cost,
        "optimal_low_to_high_sample_ratio": optimal_ratio,
        "target_normalized_score": optimal_score,
        "equal_cost_score_ratio": score_ratio,
        "worst_crossfit_sd_ratio": float(np.max(crossfit_ratio)),
        "components_improved_crossfit": int(np.sum(crossfit_ratio < 1.0)),
        "crossfit_sd_ratios": crossfit_ratio.tolist(),
        "fixed_full_matrix_betas": beta.tolist(),
        "crossfit_folds": folds,
        "variance_high": variance_high.tolist(),
        "variance_crossfit_correction": variance_correction.tolist(),
        "variance_low": variance_low.tolist(),
    }


def main() -> None:
    config = M5043.load_config()
    rows = event_dataset(config)
    high = M5043.channel_matrix(np.stack([row["high"] for row in rows]))
    _, raw_pairs = M5043.pair_means(rows, high)
    variance_high = np.var(raw_pairs, axis=0, ddof=1)
    high_cost = float(np.mean([row["high_cost"] for row in rows]))
    real_margins = np.asarray(
        [
            float(row["target_equivalence_margin"])
            for row in config["target_precision_budgets"]
        ]
    )
    margins = np.concatenate((real_margins, real_margins))
    base_score = float(np.max(np.sqrt(variance_high * high_cost) / margins))
    family = [
        assess(
            config,
            rows,
            upgraded_group_count,
            high,
            raw_pairs,
            variance_high,
            high_cost,
            margins,
            base_score,
        )
        for upgraded_group_count in range(len(GROUPS) + 1)
    ]
    selected = min(family, key=lambda row: row["equal_cost_score_ratio"])
    selected_index = int(selected["upgraded_group_count"])
    neighbors = [
        row
        for row in family
        if abs(int(row["upgraded_group_count"]) - selected_index) == 1
    ]
    efficiency_gate = bool(selected["equal_cost_score_ratio"] < 0.8)
    crossfit_gate = bool(selected["worst_crossfit_sd_ratio"] < 1.5)
    breadth_gate = bool(selected["components_improved_crossfit"] >= 7)
    neighborhood_gate = bool(
        len(neighbors) == 2
        and all(row["equal_cost_score_ratio"] < 0.8 for row in neighbors)
    )
    statistically_locked = bool(
        efficiency_gate and crossfit_gate and breadth_gate and neighborhood_gate
    )
    minimum_high_units = 4
    minimum_low_units = math.ceil(
        minimum_high_units * float(selected["optimal_low_to_high_sample_ratio"])
    )
    projected_pilot_hours = (
        minimum_high_units * high_cost
        + minimum_low_units * float(selected["mean_low_event_cost_seconds"])
    ) / 3600.0
    operationally_authorized = bool(
        statistically_locked and projected_pilot_hours <= 4.0
    )
    labels = [
        *[f"real_z{value:+.1f}" for value in config["physical_cosines"]],
        *[f"imag_z{value:+.1f}" for value in config["physical_cosines"]],
    ]
    component_rows = [
        {
            "component": label,
            "fixed_beta": selected["fixed_full_matrix_betas"][index],
            "crossfit_sd_ratio": selected["crossfit_sd_ratios"][index],
            "variance_high": selected["variance_high"][index],
            "variance_crossfit_correction": selected[
                "variance_crossfit_correction"
            ][index],
            "variance_low": selected["variance_low"][index],
            "target_margin": float(margins[index]),
        }
        for index, label in enumerate(labels)
    ]
    result = {
        "checkpoint_marker": MARKER,
        "source_script": str(SCRIPT_5043),
        "source_script_sha256": digest(SCRIPT_5043),
        "source_profile": PROFILE,
        "source_profile_digest": M5043.profile_digest(PROFILE),
        "selection_family": "nine nested reflection-symmetric exterior-fidelity thresholds",
        "selection_rule": "minimum cross-fitted target-margin-normalized equal-cost score",
        "family": family,
        "selected": selected,
        "channel_order": labels,
        "mean_high_event_cost_seconds": high_cost,
        "high_only_target_normalized_score": base_score,
        "efficiency_gate_below_0p8": efficiency_gate,
        "crossfit_instability_gate_below_1p5": crossfit_gate,
        "crossfit_breadth_gate_at_least_7_of_10": breadth_gate,
        "adjacent_threshold_stability_gate": neighborhood_gate,
        "statistical_design_locked_for_fresh_pilot": statistically_locked,
        "minimum_high_units": minimum_high_units,
        "minimum_low_units": minimum_low_units,
        "projected_minimum_pilot_hours": projected_pilot_hours,
        "four_hour_execution_cap": 4.0,
        "pilot_execution_authorized": operationally_authorized,
        "decision": (
            "LOCK_AS_RESERVE_BUT_DO_NOT_RUN; derive a cheaper topology-conditioned or analytic variance control first"
            if statistically_locked and not operationally_authorized
            else "REJECT_OR_REVISE_HYBRID_ROUTE"
        ),
        "retrospective_model_selection_only": True,
        "target_values_used_to_fit_betas": False,
        "fresh_samples_required_for_any_evidence": True,
        "valid_for_full_MTS_claim": False,
        "formalization_workbench_tree_sha256": M5043.tree_digest(
            POST.parent / "formalization-workbench"
        ),
    }
    atomic_json(RESULT_JSON, result)
    SOURCE.mkdir(parents=True, exist_ok=True)
    family_fields = (
        "upgraded_group_count",
        "upgraded_argument_count",
        "minimum_upgraded_absolute_argument",
        "mean_low_event_cost_seconds",
        "low_to_high_cost_ratio",
        "optimal_low_to_high_sample_ratio",
        "equal_cost_score_ratio",
        "worst_crossfit_sd_ratio",
        "components_improved_crossfit",
    )
    with FAMILY_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=family_fields)
        writer.writeheader()
        writer.writerows(
            {field: row[field] for field in family_fields} for row in family
        )
    with COMPONENT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(component_rows[0]))
        writer.writeheader()
        writer.writerows(component_rows)
    lock = {
        "checkpoint_marker": MARKER,
        "statistical_design_locked": statistically_locked,
        "execution_authorized": operationally_authorized,
        "execution_blocker": (
            f"projected minimum {projected_pilot_hours:.3f} h exceeds the 4 h cap"
            if not operationally_authorized
            else None
        ),
        "high_observable": "Y=2*R(E020_primary24)-R(E040_primary24)",
        "low_observable": (
            "reflection-symmetric hybrid R(E040): primary24 for |argument|>=1.5, "
            "coarse12 for |argument|<=0.6"
        ),
        "upgraded_arguments": selected["upgraded_arguments"],
        "coarse_arguments": selected["coarse_arguments"],
        "channel_order": labels,
        "fixed_betas": selected["fixed_full_matrix_betas"],
        "fixed_low_to_high_sample_ratio": selected[
            "optimal_low_to_high_sample_ratio"
        ],
        "estimator": "mean_H(Y-beta*X)+beta*mean_L(X)",
        "future_samples_independent_of_5034_through_5044_training_data": True,
        "pilot_is_not_production_evidence": True,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(LOCK_JSON, lock)
    checks = [
        ("source_5043_exists", SCRIPT_5043.exists(), str(SCRIPT_5043)),
        ("source_matrix_complete", all(M5043.result_path(PROFILE, row["event_id"], base_id).exists() for row in rows for base_id in M5043.argument_lookup(config)), "120 required"),
        ("selected_design_is_reflection_symmetric", set(selected["upgraded_arguments"]) == selected_arguments(selected_index), str(selected["upgraded_arguments"])),
        ("target_values_not_fit", not result["target_values_used_to_fit_betas"], "required false"),
        ("fresh_evidence_not_claimed", not result["valid_for_full_MTS_claim"], "required false"),
        ("long_pilot_not_authorized", not result["pilot_execution_authorized"], f"hours={projected_pilot_hours}"),
        ("formalization_workbench_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
    ]
    validation_rows = [
        {"check": name, "passed": str(passed).lower(), "evidence": evidence}
        for name, passed, evidence in checks
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
        writer.writeheader()
        writer.writerows(validation_rows)
    print(
        json.dumps(
            {
                "selected_upgraded_arguments": selected["upgraded_arguments"],
                "equal_cost_score_ratio": selected["equal_cost_score_ratio"],
                "worst_crossfit_sd_ratio": selected["worst_crossfit_sd_ratio"],
                "components_improved_crossfit": selected[
                    "components_improved_crossfit"
                ],
                "projected_minimum_pilot_hours": projected_pilot_hours,
                "statistical_design_locked": statistically_locked,
                "execution_authorized": operationally_authorized,
                "validation_passed": sum(row["passed"] == "true" for row in validation_rows),
                "validation_total": len(validation_rows),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
