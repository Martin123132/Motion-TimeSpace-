from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5049 = POST / "scripts" / "Y5_R2FR_5049_restricted_coarse_E040_multilevel_reaudit.py"
SCRIPT_5050 = POST / "scripts" / "Y5_R2FR_5050_restricted_symmetric_hybrid_fidelity_reaudit.py"
SOURCE_5049 = POST / "source-intake" / "functional_rg" / "5049"
SOURCE_5050 = POST / "source-intake" / "functional_rg" / "5050"
SOURCE = POST / "source-intake" / "functional_rg" / "5051"
RESULT_JSON = SOURCE / "phase_covariant_complex_control_gate.json"
CANDIDATE_CSV = SOURCE / "phase_control_candidate_comparison.csv"
COMPONENT_CSV = SOURCE / "selected_phase_control_components.csv"
LOCK_JSON = SOURCE / "locked_phase_control_pilot_contract.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5051_VALIDATION.csv"
)
MARKER = "MTS_5051_PHASE_COVARIANT_COMPLEX_CONTROL_GATE"
REVISION = "restricted-phase-control-crossfit-v1"
PROFILE = "coarse12"
EXECUTION_CAP_HOURS = 10.0
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
CANDIDATE_NAMES = (
    "unit_10_richardson_identity",
    "unit_real_5_imaginary_zero",
    "scalar_10_channel_reference",
    "complex_5_phase_covariant",
    "shared_complex_phase_covariant",
    "real_5_imaginary_zero_fallback",
)
PARAMETER_FREE_CANDIDATES = (
    "unit_10_richardson_identity",
    "unit_real_5_imaginary_zero",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5049 = load_module("mts_5049_for_phase_control", SCRIPT_5049)
M5050 = load_module("mts_5050_for_phase_control", SCRIPT_5050)
M5044 = M5050.M5044


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def complex_beta(low: np.ndarray, high: np.ndarray) -> complex:
    centered_low = low - np.mean(low)
    centered_high = high - np.mean(high)
    denominator = float(np.vdot(centered_low, centered_low).real)
    if denominator <= 1.0e-24:
        return 0.0j
    return complex(np.vdot(centered_low, centered_high) / denominator)


def complex_block(matrix: np.ndarray, index: int, coefficient: complex) -> None:
    real = float(coefficient.real)
    imaginary = float(coefficient.imag)
    matrix[index, index] = real
    matrix[index, index + 5] = -imaginary
    matrix[index + 5, index] = imaginary
    matrix[index + 5, index + 5] = real


def fit_matrix(
    candidate: str,
    low_complex: np.ndarray,
    high_complex: np.ndarray,
    low_channels: np.ndarray,
    high_channels: np.ndarray,
    selected: np.ndarray,
) -> tuple[np.ndarray, dict[str, Any]]:
    matrix = np.zeros((10, 10), dtype=float)
    if candidate == "unit_10_richardson_identity":
        np.fill_diagonal(matrix, 1.0)
        return matrix, {
            "exact_unit_coefficient": True,
            "richardson_correction": "H-L=2*(R(E020)-R(E040))",
        }
    if candidate == "unit_real_5_imaginary_zero":
        for index in range(5):
            matrix[index, index] = 1.0
        return matrix, {
            "exact_unit_real_coefficient": True,
            "imaginary_coefficients_fixed_to_zero": True,
            "richardson_real_correction": "Re(H-L)=2*Re(R(E020)-R(E040))",
        }
    if candidate == "scalar_10_channel_reference":
        coefficients = [
            M5049.M5043.scalar_beta(
                low_channels[selected, index], high_channels[selected, index]
            )
            for index in range(10)
        ]
        np.fill_diagonal(matrix, coefficients)
        return matrix, {"real_coefficients": coefficients}
    if candidate == "real_5_imaginary_zero_fallback":
        coefficients = [
            M5049.M5043.scalar_beta(
                low_channels[selected, index], high_channels[selected, index]
            )
            for index in range(5)
        ]
        for index, coefficient in enumerate(coefficients):
            matrix[index, index] = coefficient
        return matrix, {
            "real_coefficients": coefficients,
            "imaginary_coefficients_fixed_to_zero": True,
        }
    if candidate == "complex_5_phase_covariant":
        coefficients = [
            complex_beta(low_complex[selected, index], high_complex[selected, index])
            for index in range(5)
        ]
        for index, coefficient in enumerate(coefficients):
            complex_block(matrix, index, coefficient)
        return matrix, {
            "complex_coefficients": [
                {"real": value.real, "imaginary": value.imag} for value in coefficients
            ]
        }
    if candidate == "shared_complex_phase_covariant":
        centered_low = low_complex[selected] - np.mean(
            low_complex[selected], axis=0, keepdims=True
        )
        centered_high = high_complex[selected] - np.mean(
            high_complex[selected], axis=0, keepdims=True
        )
        coefficient = complex_beta(centered_low.reshape(-1), centered_high.reshape(-1))
        for index in range(5):
            complex_block(matrix, index, coefficient)
        return matrix, {
            "shared_complex_coefficient": {
                "real": coefficient.real,
                "imaginary": coefficient.imag,
            }
        }
    raise ValueError(f"unknown candidate {candidate}")


def transformed(low_channels: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return low_channels @ matrix.T


def crossfit_candidate(
    candidate: str,
    rows: list[dict[str, Any]],
    low_complex: np.ndarray,
    high_complex: np.ndarray,
    low_channels: np.ndarray,
    high_channels: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]], dict[str, Any]]:
    seeds = sorted({int(row["seed"]) for row in rows})
    correction_pairs = []
    folds = []
    for held_seed in seeds:
        training = np.asarray([int(row["seed"]) != held_seed for row in rows])
        held = ~training
        matrix, coefficients = fit_matrix(
            candidate,
            low_complex,
            high_complex,
            low_channels,
            high_channels,
            training,
        )
        correction_pairs.append(
            np.mean(high_channels[held] - transformed(low_channels[held], matrix), axis=0)
        )
        folds.append(
            {
                "held_seed": held_seed,
                "training_seeds": [seed for seed in seeds if seed != held_seed],
                "coefficients": coefficients,
                "matrix_frobenius_norm": float(np.linalg.norm(matrix)),
                "matrix_max_absolute_entry": float(np.max(np.abs(matrix))),
            }
        )
    selected = np.ones(len(rows), dtype=bool)
    full_matrix, full_coefficients = fit_matrix(
        candidate,
        low_complex,
        high_complex,
        low_channels,
        high_channels,
        selected,
    )
    return np.stack(correction_pairs), full_matrix, folds, full_coefficients


def assess_candidate(
    candidate: str,
    rows: list[dict[str, Any]],
    low_complex: np.ndarray,
    high_complex: np.ndarray,
    low_channels: np.ndarray,
    high_channels: np.ndarray,
    high_pairs: np.ndarray,
    low_pairs: np.ndarray,
    variance_high: np.ndarray,
    margins: np.ndarray,
    high_cost: float,
    low_cost: float,
    base_score: float,
) -> dict[str, Any]:
    correction_pairs, matrix, folds, coefficients = crossfit_candidate(
        candidate,
        rows,
        low_complex,
        high_complex,
        low_channels,
        high_channels,
    )
    low_contribution_pairs = transformed(low_pairs, matrix)
    variance_correction = np.var(correction_pairs, axis=0, ddof=1)
    variance_low_contribution = np.var(low_contribution_pairs, axis=0, ddof=1)
    raw_sd = np.std(high_pairs, axis=0, ddof=1)
    correction_sd = np.std(correction_pairs, axis=0, ddof=1)
    crossfit_ratios = np.divide(
        correction_sd,
        raw_sd,
        out=np.full_like(raw_sd, math.inf),
        where=raw_sd > 0.0,
    )
    allocation_rows = []
    for sample_ratio in np.geomspace(0.25, 512.0, 4097):
        variance_cost = (
            variance_correction + variance_low_contribution / sample_ratio
        ) * (high_cost + sample_ratio * low_cost)
        score = float(np.max(np.sqrt(np.maximum(variance_cost, 0.0)) / margins))
        allocation_rows.append((float(sample_ratio), score, variance_cost))
    optimal_ratio, optimal_score, variance_cost = min(
        allocation_rows, key=lambda row: row[1]
    )
    active = np.linalg.norm(matrix, axis=1) > 1.0e-12
    active_ratios = crossfit_ratios[active]
    inactive_ratios = crossfit_ratios[~active]
    active_noninflating = bool(np.all(active_ratios < 1.0))
    inactive_unchanged = bool(
        inactive_ratios.size == 0 or np.all(np.abs(inactive_ratios - 1.0) <= 1.0e-12)
    )
    finite = bool(
        np.all(np.isfinite(matrix))
        and np.all(np.isfinite(correction_pairs))
        and np.all(np.isfinite(crossfit_ratios))
    )
    efficiency = bool(optimal_score / base_score < 0.8)
    improved = int(np.sum(crossfit_ratios < 1.0 - 1.0e-12))
    statistically_eligible = bool(
        finite
        and efficiency
        and active_noninflating
        and inactive_unchanged
        and improved >= 5
    )
    minimum_high_units = 4
    minimum_low_units = math.ceil(minimum_high_units * optimal_ratio)
    projected_hours = (
        minimum_high_units * high_cost + minimum_low_units * low_cost
    ) / 3600.0
    equal_cost_component_ratios = np.sqrt(
        np.divide(
            variance_cost,
            variance_high * high_cost,
            out=np.full_like(variance_cost, math.inf),
            where=variance_high > 0.0,
        )
    )
    return {
        "candidate": candidate,
        "coefficient_contract": coefficients,
        "full_control_matrix": matrix.tolist(),
        "folds": folds,
        "active_output_channels": np.flatnonzero(active).tolist(),
        "inactive_output_channels": np.flatnonzero(~active).tolist(),
        "crossfit_sd_ratios": crossfit_ratios.tolist(),
        "worst_crossfit_sd_ratio": float(np.max(crossfit_ratios)),
        "components_improved_crossfit": improved,
        "active_channels_noninflating": active_noninflating,
        "inactive_channels_unchanged": inactive_unchanged,
        "all_values_finite": finite,
        "variance_high": variance_high.tolist(),
        "variance_crossfit_correction": variance_correction.tolist(),
        "variance_low_contribution": variance_low_contribution.tolist(),
        "optimal_low_to_high_sample_ratio": optimal_ratio,
        "target_normalized_score": optimal_score,
        "equal_cost_score_ratio": optimal_score / base_score,
        "equal_cost_component_sd_ratios": equal_cost_component_ratios.tolist(),
        "efficiency_gate_below_0p8": efficiency,
        "statistically_eligible": statistically_eligible,
        "minimum_high_units": minimum_high_units,
        "minimum_low_units": minimum_low_units,
        "projected_minimum_pilot_hours": projected_hours,
    }


def main() -> None:
    required = [
        SCRIPT_5049,
        SCRIPT_5050,
        SOURCE_5049 / "restricted_multilevel_coarse_E040_gate.json",
        SOURCE_5049 / "runs" / PROFILE / "status.json",
        SOURCE_5050 / "restricted_symmetric_hybrid_fidelity_gate.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing corrected-source inputs: {missing}")
    M5049.configure_modules()
    try:
        scope = M5049.strict_scope_audit(PROFILE)
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
        _, high_pairs = M5049.M5043.pair_means(rows, high_channels)
        _, low_pairs = M5049.M5043.pair_means(rows, low_channels)
        variance_high = np.var(high_pairs, axis=0, ddof=1)
        high_cost = float(np.mean([row["high_cost"] for row in rows]))
        _, low_cost = M5044.hybrid_matrix(config, rows, 0)
        real_margins = np.asarray(
            [
                float(row["target_equivalence_margin"])
                for row in config["target_precision_budgets"]
            ]
        )
        margins = np.concatenate((real_margins, real_margins))
        base_score = float(np.max(np.sqrt(variance_high * high_cost) / margins))
        candidates = [
            assess_candidate(
                candidate,
                rows,
                low_complex,
                high_complex,
                low_channels,
                high_channels,
                high_pairs,
                low_pairs,
                variance_high,
                margins,
                high_cost,
                low_cost,
                base_score,
            )
            for candidate in CANDIDATE_NAMES
        ]
        eligible = [row for row in candidates if row["statistically_eligible"]]
        parameter_free_eligible = [
            row for row in eligible if row["candidate"] in PARAMETER_FREE_CANDIDATES
        ]
        selected_pool = parameter_free_eligible or eligible
        selected = (
            min(selected_pool, key=lambda row: row["equal_cost_score_ratio"])
            if selected_pool
            else None
        )
        execution_authorized = bool(
            selected
            and selected["projected_minimum_pilot_hours"] <= EXECUTION_CAP_HOURS
        )
        channel_order = [
            *[f"real_z{value:+.1f}" for value in config["physical_cosines"]],
            *[f"imag_z{value:+.1f}" for value in config["physical_cosines"]],
        ]
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "estimator_contract": "mean_H(H-BL)+B*mean_L(L)",
            "unbiased_for_any_fixed_B": True,
            "coefficient_training": "leave-one-independent-scramble-out",
            "complex_action": "cL=(Re(c)Re(L)-Im(c)Im(L))+i(Re(c)Im(L)+Im(c)Re(L))",
            "candidate_family_predeclared": list(CANDIDATE_NAMES),
            "candidate_selection_rule": "prefer stable parameter-free Richardson controls, then minimize equal-cost score",
            "channel_order": channel_order,
            "candidates": candidates,
            "selected_candidate": selected["candidate"] if selected else None,
            "selected": selected,
            "mean_high_event_cost_seconds": high_cost,
            "mean_low_event_cost_seconds": low_cost,
            "low_to_high_cost_ratio": low_cost / high_cost,
            "high_only_target_normalized_score": base_score,
            "execution_cap_hours": EXECUTION_CAP_HOURS,
            "fresh_pilot_authorized": execution_authorized,
            "decision": (
                "FRESH_PILOT_AUTHORIZED_WITHIN_CAP"
                if execution_authorized
                else (
                    "LOCK_STATISTICAL_DESIGN_BUT_DEFER_LONG_PILOT"
                    if selected
                    else "NO_STABLE_PHASE_CONTROL_SELECTED"
                )
            ),
            "target_central_values_used_to_fit_or_select": False,
            "retrospective_design_only": True,
            "fresh_independent_samples_required_for_evidence": True,
            "restricted_scope_audit": scope,
            "source_5049_result_sha256": M5049.digest(
                SOURCE_5049 / "restricted_multilevel_coarse_E040_gate.json"
            ),
            "source_5050_result_sha256": M5049.digest(
                SOURCE_5050 / "restricted_symmetric_hybrid_fidelity_gate.json"
            ),
            "formalization_workbench_tree_sha256": M5049.M5043.tree_digest(
                POST.parent / "formalization-workbench"
            ),
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(RESULT_JSON, result)
        SOURCE.mkdir(parents=True, exist_ok=True)
        candidate_fields = (
            "candidate",
            "worst_crossfit_sd_ratio",
            "components_improved_crossfit",
            "active_channels_noninflating",
            "inactive_channels_unchanged",
            "equal_cost_score_ratio",
            "optimal_low_to_high_sample_ratio",
            "minimum_low_units",
            "projected_minimum_pilot_hours",
            "statistically_eligible",
        )
        with CANDIDATE_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=candidate_fields)
            writer.writeheader()
            writer.writerows(
                {field: row[field] for field in candidate_fields} for row in candidates
            )
        selected_rows = []
        if selected:
            for index, label in enumerate(channel_order):
                selected_rows.append(
                    {
                        "component": label,
                        "active_control": index in selected["active_output_channels"],
                        "crossfit_sd_ratio": selected["crossfit_sd_ratios"][index],
                        "equal_cost_component_sd_ratio": selected[
                            "equal_cost_component_sd_ratios"
                        ][index],
                        "target_margin": float(margins[index]),
                    }
                )
        with COMPONENT_CSV.open("w", newline="", encoding="utf-8") as handle:
            fields = (
                "component",
                "active_control",
                "crossfit_sd_ratio",
                "equal_cost_component_sd_ratio",
                "target_margin",
            )
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(selected_rows)
        lock = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "selected_candidate": result["selected_candidate"],
            "statistical_design_locked": selected is not None,
            "execution_authorized": execution_authorized,
            "execution_blocker": (
                f"projected minimum {selected['projected_minimum_pilot_hours']:.3f} h exceeds the {EXECUTION_CAP_HOURS:g} h cap"
                if selected and not execution_authorized
                else None
            ),
            "estimator": result["estimator_contract"],
            "fixed_control_matrix": selected["full_control_matrix"] if selected else None,
            "fixed_low_to_high_sample_ratio": (
                selected["optimal_low_to_high_sample_ratio"] if selected else None
            ),
            "channel_order": channel_order,
            "future_samples_independent_of_training_data_through_checkpoint": 5051,
            "pilot_is_not_production_evidence": True,
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(LOCK_JSON, lock)
        reference = next(
            row for row in candidates if row["candidate"] == "scalar_10_channel_reference"
        )
        source_5050 = json.loads(
            (SOURCE_5050 / "restricted_symmetric_hybrid_fidelity_gate.json").read_text(
                encoding="utf-8"
            )
        )["selected"]
        reference_difference = float(
            np.max(
                np.abs(
                    np.asarray(reference["crossfit_sd_ratios"])
                    - np.asarray(source_5050["crossfit_sd_ratios"])
                )
            )
        )
        checks = [
            ("corrected_5049_source_exists", required[2].exists(), str(required[2])),
            ("restricted_matrix_complete", required[3].exists(), str(required[3])),
            (
                "restricted_scope_passes",
                scope["all_theorem_zeros_within_restricted_scope"],
                f"strict={scope['strict_scope_rows']}; total={scope['theorem_zero_rows']}",
            ),
            (
                "candidate_family_complete",
                [row["candidate"] for row in candidates] == list(CANDIDATE_NAMES),
                str([row["candidate"] for row in candidates]),
            ),
            (
                "scalar_reference_reproduced",
                reference_difference <= 1.0e-12,
                f"max_ratio_difference={reference_difference}",
            ),
            (
                "all_candidate_values_finite",
                all(row["all_values_finite"] for row in candidates),
                "required true",
            ),
            (
                "target_central_values_not_fit",
                not result["target_central_values_used_to_fit_or_select"],
                "required false",
            ),
            (
                "fresh_evidence_not_claimed",
                not result["valid_for_full_MTS_claim"],
                "required false",
            ),
            (
                "execution_cap_respected",
                not execution_authorized
                or selected["projected_minimum_pilot_hours"] <= EXECUTION_CAP_HOURS,
                f"authorized={execution_authorized}",
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
                    "candidates": [
                        {
                            "candidate": row["candidate"],
                            "score_ratio": row["equal_cost_score_ratio"],
                            "worst_crossfit_ratio": row["worst_crossfit_sd_ratio"],
                            "improved": row["components_improved_crossfit"],
                            "eligible": row["statistically_eligible"],
                        }
                        for row in candidates
                    ],
                    "selected_candidate": result["selected_candidate"],
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
