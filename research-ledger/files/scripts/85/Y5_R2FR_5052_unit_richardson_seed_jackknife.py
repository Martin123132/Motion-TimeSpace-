from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5051 = POST / "scripts" / "Y5_R2FR_5051_phase_covariant_complex_control_gate.py"
SOURCE_5051 = POST / "source-intake" / "functional_rg" / "5051"
SOURCE = POST / "source-intake" / "functional_rg" / "5052"
RESULT_JSON = SOURCE / "unit_richardson_seed_jackknife.json"
PANEL_CSV = SOURCE / "unit_richardson_jackknife_panels.csv"
COMPONENT_CSV = SOURCE / "unit_richardson_jackknife_components.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5052_VALIDATION.csv"
)
MARKER = "MTS_5052_UNIT_RICHARDSON_SEED_JACKKNIFE"
REVISION = "unit-real-control-delete-one-seed-v1"
EXECUTION_CAP_HOURS = 10.0
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5051 = load_module("mts_5051_for_unit_jackknife", SCRIPT_5051)
M5049 = M5051.M5049
M5044 = M5051.M5044


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def assess_panel(
    label: str,
    omitted_seed: int | None,
    seeds: list[int],
    high_pairs: np.ndarray,
    low_pairs: np.ndarray,
    margins: np.ndarray,
    high_cost: float,
    low_cost: float,
) -> dict[str, Any]:
    selected = np.asarray(
        [seed != omitted_seed for seed in seeds] if omitted_seed is not None else [True] * len(seeds)
    )
    panel_high = high_pairs[selected]
    panel_low = low_pairs[selected]
    matrix = np.zeros((10, 10), dtype=float)
    for index in range(5):
        matrix[index, index] = 1.0
    panel_correction = panel_high - panel_low @ matrix.T
    panel_low_contribution = panel_low @ matrix.T
    variance_high = np.var(panel_high, axis=0, ddof=1)
    variance_correction = np.var(panel_correction, axis=0, ddof=1)
    variance_low = np.var(panel_low_contribution, axis=0, ddof=1)
    raw_sd = np.sqrt(variance_high)
    correction_sd = np.sqrt(variance_correction)
    crossfit_ratios = np.divide(
        correction_sd,
        raw_sd,
        out=np.full_like(raw_sd, math.inf),
        where=raw_sd > 0.0,
    )
    base_score = float(np.max(np.sqrt(variance_high * high_cost) / margins))
    options = []
    for sample_ratio in np.geomspace(0.25, 512.0, 4097):
        variance_cost = (
            variance_correction + variance_low / sample_ratio
        ) * (high_cost + sample_ratio * low_cost)
        score = float(np.max(np.sqrt(np.maximum(variance_cost, 0.0)) / margins))
        options.append((float(sample_ratio), score, variance_cost))
    sample_ratio, score, variance_cost = min(options, key=lambda row: row[1])
    component_cost_ratios = np.sqrt(
        np.divide(
            variance_cost,
            variance_high * high_cost,
            out=np.full_like(variance_cost, math.inf),
            where=variance_high > 0.0,
        )
    )
    minimum_high_units = 4
    minimum_low_units = math.ceil(minimum_high_units * sample_ratio)
    projected_hours = (
        minimum_high_units * high_cost + minimum_low_units * low_cost
    ) / 3600.0
    return {
        "panel": label,
        "omitted_seed": omitted_seed,
        "included_seeds": [seed for seed in seeds if seed != omitted_seed],
        "seed_count": int(np.sum(selected)),
        "crossfit_sd_ratios": crossfit_ratios.tolist(),
        "worst_active_real_sd_ratio": float(np.max(crossfit_ratios[:5])),
        "inactive_imaginary_ratios": crossfit_ratios[5:].tolist(),
        "all_active_real_channels_improve": bool(np.all(crossfit_ratios[:5] < 1.0)),
        "inactive_imaginary_channels_unchanged": bool(
            np.all(np.abs(crossfit_ratios[5:] - 1.0) <= 1.0e-12)
        ),
        "optimal_low_to_high_sample_ratio": sample_ratio,
        "target_normalized_score": score,
        "equal_cost_score_ratio": score / base_score,
        "efficiency_gate_below_0p8": bool(score / base_score < 0.8),
        "equal_cost_component_sd_ratios": component_cost_ratios.tolist(),
        "minimum_high_units": minimum_high_units,
        "minimum_low_units": minimum_low_units,
        "projected_minimum_pilot_hours": projected_hours,
    }


def main() -> None:
    source_result_path = SOURCE_5051 / "phase_covariant_complex_control_gate.json"
    if not SCRIPT_5051.exists() or not source_result_path.exists():
        raise FileNotFoundError("checkpoint 5051 inputs are missing")
    source_result = json.loads(source_result_path.read_text(encoding="utf-8"))
    if source_result.get("selected_candidate") != "unit_real_5_imaginary_zero":
        raise RuntimeError("5051 did not select the parameter-free unit-real control")
    M5049.configure_modules()
    try:
        scope = M5049.strict_scope_audit(M5051.PROFILE)
        if not scope["all_theorem_zeros_within_restricted_scope"]:
            raise RuntimeError("restricted theorem-scope audit failed")
        M5044.M5043 = M5049.M5043
        config = M5049.M5043.load_config()
        rows = M5044.event_dataset(config)
        high_complex = np.stack([row["high"] for row in rows])
        low_complex = np.stack(
            [M5044.residual(config, row["coarse"]) for row in rows]
        )
        high_channels = M5049.M5043.channel_matrix(high_complex)
        low_channels = M5049.M5043.channel_matrix(low_complex)
        seeds, high_pairs = M5049.M5043.pair_means(rows, high_channels)
        low_seeds, low_pairs = M5049.M5043.pair_means(rows, low_channels)
        if seeds != low_seeds:
            raise RuntimeError("high/low seed pairing differs")
        real_margins = np.asarray(
            [
                float(row["target_equivalence_margin"])
                for row in config["target_precision_budgets"]
            ]
        )
        margins = np.concatenate((real_margins, real_margins))
        high_cost = float(np.mean([row["high_cost"] for row in rows]))
        _, low_cost = M5044.hybrid_matrix(config, rows, 0)
        full = assess_panel(
            "all_four_seeds",
            None,
            seeds,
            high_pairs,
            low_pairs,
            margins,
            high_cost,
            low_cost,
        )
        jackknife = [
            assess_panel(
                f"omit_{seed}",
                seed,
                seeds,
                high_pairs,
                low_pairs,
                margins,
                high_cost,
                low_cost,
            )
            for seed in seeds
        ]
        all_panels = [full, *jackknife]
        all_real_improve = all(row["all_active_real_channels_improve"] for row in all_panels)
        all_imaginary_unchanged = all(
            row["inactive_imaginary_channels_unchanged"] for row in all_panels
        )
        all_efficiency = all(row["efficiency_gate_below_0p8"] for row in all_panels)
        jackknife_score_ratios = [row["equal_cost_score_ratio"] for row in jackknife]
        maximum_score_ratio = max(jackknife_score_ratios)
        minimum_score_ratio = min(jackknife_score_ratios)
        robustness_passed = bool(
            all_real_improve and all_imaginary_unchanged and all_efficiency
        )
        projected_hours = full["projected_minimum_pilot_hours"]
        execution_authorized = bool(
            robustness_passed and projected_hours <= EXECUTION_CAP_HOURS
        )
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "tested_control": "B=diag(1,1,1,1,1,0,0,0,0,0)",
            "exact_correction_identity": "Re(H-L)=2*Re(R(E020)-R(E040))",
            "coefficient_fit_required": False,
            "full_panel": full,
            "delete_one_seed_panels": jackknife,
            "all_active_real_channels_improve_in_every_panel": all_real_improve,
            "all_inactive_imaginary_channels_unchanged_in_every_panel": all_imaginary_unchanged,
            "all_panels_pass_efficiency_gate": all_efficiency,
            "jackknife_equal_cost_score_ratio_range": [
                minimum_score_ratio,
                maximum_score_ratio,
            ],
            "robustness_gate_passed": robustness_passed,
            "execution_cap_hours": EXECUTION_CAP_HOURS,
            "fresh_pilot_authorized": execution_authorized,
            "decision": (
                "UNIT_REAL_CONTROL_ROBUST_BUT_LONG_PILOT_DEFERRED"
                if robustness_passed and not execution_authorized
                else (
                    "UNIT_REAL_CONTROL_PILOT_AUTHORIZED"
                    if execution_authorized
                    else "UNIT_REAL_CONTROL_PROVISIONAL_JACKKNIFE_FAILURE"
                )
            ),
            "retrospective_design_only": True,
            "fresh_independent_samples_required_for_evidence": True,
            "target_central_values_used": False,
            "restricted_scope_audit": scope,
            "source_5051_result_sha256": M5049.digest(source_result_path),
            "formalization_workbench_tree_sha256": M5049.M5043.tree_digest(
                POST.parent / "formalization-workbench"
            ),
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(RESULT_JSON, result)
        SOURCE.mkdir(parents=True, exist_ok=True)
        panel_fields = (
            "panel",
            "omitted_seed",
            "seed_count",
            "worst_active_real_sd_ratio",
            "all_active_real_channels_improve",
            "inactive_imaginary_channels_unchanged",
            "optimal_low_to_high_sample_ratio",
            "equal_cost_score_ratio",
            "efficiency_gate_below_0p8",
            "minimum_low_units",
            "projected_minimum_pilot_hours",
        )
        with PANEL_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=panel_fields)
            writer.writeheader()
            writer.writerows(
                {field: row[field] for field in panel_fields} for row in all_panels
            )
        channel_order = [
            *[f"real_z{value:+.1f}" for value in config["physical_cosines"]],
            *[f"imag_z{value:+.1f}" for value in config["physical_cosines"]],
        ]
        component_rows = []
        for panel in all_panels:
            for index, component in enumerate(channel_order):
                component_rows.append(
                    {
                        "panel": panel["panel"],
                        "component": component,
                        "active_control": index < 5,
                        "correction_sd_ratio": panel["crossfit_sd_ratios"][index],
                        "equal_cost_component_sd_ratio": panel[
                            "equal_cost_component_sd_ratios"
                        ][index],
                    }
                )
        with COMPONENT_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(component_rows[0]))
            writer.writeheader()
            writer.writerows(component_rows)
        source_score = float(source_result["selected"]["equal_cost_score_ratio"])
        checks = [
            ("source_5051_exists", source_result_path.exists(), str(source_result_path)),
            (
                "source_selected_unit_real_control",
                source_result["selected_candidate"] == "unit_real_5_imaginary_zero",
                str(source_result["selected_candidate"]),
            ),
            (
                "full_panel_reproduces_5051",
                abs(full["equal_cost_score_ratio"] - source_score) <= 1.0e-12,
                f"difference={abs(full['equal_cost_score_ratio'] - source_score)}",
            ),
            (
                "all_delete_one_panels_present",
                len(jackknife) == len(seeds) == 4,
                f"panels={len(jackknife)}",
            ),
            ("all_active_real_channels_improve", all_real_improve, "required true"),
            (
                "all_inactive_imaginary_channels_unchanged",
                all_imaginary_unchanged,
                "required true",
            ),
            ("all_panels_efficiency_below_0p8", all_efficiency, str(jackknife_score_ratios)),
            (
                "restricted_scope_passes",
                scope["all_theorem_zeros_within_restricted_scope"],
                f"strict={scope['strict_scope_rows']}; total={scope['theorem_zero_rows']}",
            ),
            ("target_central_values_not_used", not result["target_central_values_used"], "required false"),
            ("fresh_evidence_not_claimed", not result["valid_for_full_MTS_claim"], "required false"),
            (
                "execution_cap_respected",
                not execution_authorized or projected_hours <= EXECUTION_CAP_HOURS,
                f"hours={projected_hours}",
            ),
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
                    "full_score_ratio": full["equal_cost_score_ratio"],
                    "jackknife_score_ratio_range": [minimum_score_ratio, maximum_score_ratio],
                    "jackknife_worst_real_ratios": [
                        row["worst_active_real_sd_ratio"] for row in jackknife
                    ],
                    "robustness_gate_passed": robustness_passed,
                    "projected_minimum_pilot_hours": projected_hours,
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
