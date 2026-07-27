from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5036"
RUN = SOURCE / "runs" / "paired_full_vector_s2_v1"
RESULT = SOURCE / "paired_full_vector_results.json"
DOCUMENT = (
    POST
    / "5036-Y5-R2FR-paired-epsilon-full-cyclic-vector-and-local-nonlocal-decomposition.md"
)
PROVENANCE = SOURCE / "PROVENANCE.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
VECTOR_CSV = SOURCE / "epsilon_cyclic_vector.csv"
DECOMPOSITION_CSV = SOURCE / "local_nonlocal_decomposition.csv"
PAIRED_CSV = SOURCE / "paired_vector_convergence.csv"
TARGET_CSV = SOURCE / "epsilon_zero_target_comparison.csv"
GATE_CSV = SOURCE / "full_vector_ladder_gate.csv"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5036_VALIDATION.csv"
)
RUNNER = POST / "scripts" / "Y5_R2FR_5036_paired_full_vector_ladder.py"
REPAIR = POST / "scripts" / "Y5_R2FR_5035_pair_local_residue_radius_repair.py"
MARKER = "MTS_5036_PAIRED_EPSILON_FULL_CYCLIC_VECTOR"
CONFIG_DIGEST = "c0aa91447dc8a438175bd493f32a9b9fff8d04037c640dfb55d4737c67972c81"
RADIUS_REVISION = "pair-local-double-residue-shrinking-radius-v4"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def complex_from_row(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def close(value: float, expected: float, tolerance: float = 2.0e-10) -> bool:
    return abs(value - expected) <= tolerance * max(1.0, abs(expected))


def close_complex(value: complex, expected: complex) -> bool:
    return close(value.real, expected.real) and close(value.imag, expected.imag)


def finite_complex_row(value: dict[str, Any]) -> bool:
    return math.isfinite(float(value["real"])) and math.isfinite(
        float(value["imaginary"])
    )


def aggregate(values: list[complex]) -> dict[str, Any]:
    count = len(values)
    mean = sum(values, 0j) / count
    if count > 1:
        real_variance = sum((value.real - mean.real) ** 2 for value in values) / (
            count - 1
        )
        imaginary_variance = sum(
            (value.imag - mean.imag) ** 2 for value in values
        ) / (count - 1)
        real_standard_error = math.sqrt(real_variance / count)
        imaginary_standard_error = math.sqrt(imaginary_variance / count)
    else:
        real_standard_error = 0.0
        imaginary_standard_error = 0.0
    return {
        "mean": mean,
        "real_standard_error": real_standard_error,
        "imaginary_standard_error": imaginary_standard_error,
        "replicate_count": count,
    }


def estimate_matches(actual: dict[str, Any] | None, values: list[complex]) -> bool:
    if actual is None or not values:
        return False
    expected = aggregate(values)
    return (
        close_complex(complex_from_row(actual["mean"]), expected["mean"])
        and close(
            float(actual["real_standard_error"]),
            float(expected["real_standard_error"]),
        )
        and close(
            float(actual["imaginary_standard_error"]),
            float(expected["imaginary_standard_error"]),
        )
        and int(actual["replicate_count"]) == expected["replicate_count"]
    )


def project(
    vector: list[complex], shape: list[float]
) -> tuple[complex, list[complex], float]:
    denominator = sum(component * component for component in shape)
    coefficient = sum(
        component * value for component, value in zip(shape, vector)
    ) / denominator
    residual = [
        value - coefficient * component
        for component, value in zip(shape, vector)
    ]
    orthogonality = abs(
        sum(component * value for component, value in zip(shape, residual))
    )
    return coefficient, residual, orthogonality


def vector_norm(vector: list[complex]) -> float:
    return math.sqrt(sum(abs(value) ** 2 for value in vector))


def expected_job_keys(config: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    central = min(
        config["crossings"],
        key=lambda row: abs(float(row["physical_s_channel_cosine"])),
    )
    for epsilon_id in config["epsilon_ids"]:
        for event in config["events"]:
            for argument in config["base_arguments"]:
                keys.add(
                    f"{epsilon_id}__{event['event_id']}__{argument['argument_id']}__primary24"
                )
        for field in ("s_argument_id", "t_argument_id", "u_argument_id"):
            keys.add(
                f"{epsilon_id}__S{config['audit_seed']}_N0000__{central[field]}__audit32"
            )
    return keys


def direct_lookup(
    jobs: list[dict[str, Any]],
) -> dict[tuple[str, str, int, int, str], complex]:
    return {
        (
            row["tier"],
            row["epsilon_id"],
            int(row["seed"]),
            int(row["sample_index"]),
            row["base_argument_id"],
        ): complex_from_row(row["normalized_direct_D_hhh_over_G3"])
        for row in jobs
    }


def rebuild_vectors(
    config: dict[str, Any],
    direct: dict[tuple[str, str, int, int, str], complex],
) -> dict[tuple[str, int], list[complex]]:
    vectors: dict[tuple[str, int], list[complex]] = {}
    for epsilon_id in config["epsilon_ids"]:
        for seed in config["seeds"]:
            values: list[complex] = []
            for crossing in config["crossings"]:
                keys = [
                    ("primary24", epsilon_id, seed, 0, crossing[field])
                    for field in (
                        "s_argument_id",
                        "t_argument_id",
                        "u_argument_id",
                    )
                ]
                values.append(
                    direct[keys[0]]
                    + float(crossing["t_ratio"]) ** 3 * direct[keys[1]]
                    + float(crossing["u_ratio"]) ** 3 * direct[keys[2]]
                )
            vectors[(epsilon_id, seed)] = values
    return vectors


def independent_global_audit(
    config: dict[str, Any],
    direct: dict[tuple[str, str, int, int, str], complex],
) -> list[dict[str, Any]]:
    central = min(
        config["crossings"],
        key=lambda row: abs(float(row["physical_s_channel_cosine"])),
    )
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        values: dict[str, complex] = {}
        for tier in ("primary24", "audit32"):
            keys = [
                (
                    tier,
                    epsilon_id,
                    int(config["audit_seed"]),
                    0,
                    central[field],
                )
                for field in (
                    "s_argument_id",
                    "t_argument_id",
                    "u_argument_id",
                )
            ]
            values[tier] = (
                direct[keys[0]]
                + float(central["t_ratio"]) ** 3 * direct[keys[1]]
                + float(central["u_ratio"]) ** 3 * direct[keys[2]]
            )
        difference = values["audit32"] - values["primary24"]
        rows.append(
            {
                "epsilon": float(epsilon),
                "primary24": values["primary24"],
                "audit32": values["audit32"],
                "difference": difference,
                "relative_difference": abs(difference)
                / max(abs(values["audit32"]), 1.0),
            }
        )
    return rows


def check_rows() -> list[tuple[str, bool, str]]:
    config = load_json(RUN / "config.json")
    unsigned_config = dict(config)
    supplied_config_digest = unsigned_config.pop("config_digest")
    status = load_json(RUN / "status.json")
    result = load_json(RESULT)
    jobs = [load_json(path) for path in sorted((RUN / "jobs").glob("*.json"))]
    imported = [row for row in jobs if row["status"] == "IMPORTED_CONVERGED"]
    computed = [row for row in jobs if row["status"] == "COMPLETED_CONVERGED"]
    computed_kernels = [
        load_json(RUN / "kernels" / f"{row['job_key']}.json") for row in computed
    ]
    expected = expected_job_keys(config)
    actual = {row["job_key"] for row in jobs}
    source_digests_match = all(
        expected_digest is not None
        and Path(path).exists()
        and digest(Path(path)) == expected_digest
        for path, expected_digest in config["source_files"].items()
    )
    imported_sources_match = all(
        Path(row["imported_from"]["source_job"]).exists()
        and digest(Path(row["imported_from"]["source_job"]))
        == row["imported_from"]["source_job_sha256"]
        for row in imported
    )
    direct = direct_lookup(jobs)
    rebuilt_vectors = rebuild_vectors(config, direct)
    serialized_vectors = {
        (row["epsilon_id"], int(row["seed"])): [
            complex_from_row(value) for value in row["cyclic_vector"]
        ]
        for row in result["cyclic_vectors_per_seed"]
        if row["cyclic_vector"] is not None
    }
    per_seed_vectors_match = set(serialized_vectors) == set(rebuilt_vectors) and all(
        all(close_complex(value, expected_value) for value, expected_value in zip(
            serialized_vectors[key], rebuilt_vectors[key]
        ))
        for key in rebuilt_vectors
    )
    shape = [
        1.0 - float(cosine) ** 2 for cosine in config["physical_cosines"]
    ]
    summary_lookup = {
        row["epsilon_id"]: row for row in result["vector_summaries"]
    }
    summaries_match = True
    projection_residuals: list[float] = []
    projected: dict[tuple[str, int], tuple[complex, list[complex]]] = {}
    for epsilon_id in config["epsilon_ids"]:
        vectors = [
            rebuilt_vectors[(epsilon_id, int(seed))] for seed in config["seeds"]
        ]
        coefficients: list[complex] = []
        residuals: list[list[complex]] = []
        for seed, vector in zip(config["seeds"], vectors):
            coefficient, residual, orthogonality = project(vector, shape)
            projected[(epsilon_id, int(seed))] = (coefficient, residual)
            coefficients.append(coefficient)
            residuals.append(residual)
            projection_residuals.append(orthogonality)
        summary = summary_lookup[epsilon_id]
        summaries_match = summaries_match and (
            int(summary["complete_scrambles"]) == len(config["seeds"])
            and estimate_matches(summary["local_coefficient"], coefficients)
            and close(
                float(summary["maximum_eventwise_projection_orthogonality_residual"]),
                max(projection_residuals[-len(config["seeds"]):]),
            )
        )
        for index in range(len(shape)):
            summaries_match = summaries_match and estimate_matches(
                summary["cyclic_components"][index]["estimate"],
                [vector[index] for vector in vectors],
            ) and estimate_matches(
                summary["nonlocal_components"][index]["estimate"],
                [residual[index] for residual in residuals],
            )
    paired_match = True
    full_steps: list[float] = []
    local_steps: list[float] = []
    nonlocal_steps: list[list[float]] = []
    for step_index, (from_id, to_id) in enumerate(
        zip(config["epsilon_ids"], config["epsilon_ids"][1:])
    ):
        vector_differences: list[list[complex]] = []
        local_differences: list[complex] = []
        residual_differences: list[list[complex]] = []
        for seed in config["seeds"]:
            from_vector = rebuilt_vectors[(from_id, int(seed))]
            to_vector = rebuilt_vectors[(to_id, int(seed))]
            vector_differences.append(
                [to_value - from_value for to_value, from_value in zip(to_vector, from_vector)]
            )
            from_local, from_residual = projected[(from_id, int(seed))]
            to_local, to_residual = projected[(to_id, int(seed))]
            local_differences.append(to_local - from_local)
            residual_differences.append(
                [to_value - from_value for to_value, from_value in zip(to_residual, from_residual)]
            )
        mean_vector_difference = [
            sum(values, 0j) / len(values)
            for values in zip(*vector_differences)
        ]
        mean_residual_difference = [
            sum(values, 0j) / len(values)
            for values in zip(*residual_differences)
        ]
        full_step = vector_norm(mean_vector_difference)
        local_step = abs(sum(local_differences, 0j) / len(local_differences))
        component_steps = [abs(value) for value in mean_residual_difference]
        full_steps.append(full_step)
        local_steps.append(local_step)
        nonlocal_steps.append(component_steps)
        actual_step = result["paired_convergence"][step_index]
        paired_match = paired_match and (
            int(actual_step["paired_scrambles"]) == len(config["seeds"])
            and close(float(actual_step["full_vector_mean_step_L2"]), full_step)
            and close(
                float(actual_step["local_coefficient_mean_step_magnitude"]),
                local_step,
            )
            and all(
                close(float(actual_value), expected_value)
                for actual_value, expected_value in zip(
                    actual_step["nonlocal_mean_step_magnitudes"], component_steps
                )
            )
            and estimate_matches(
                actual_step["local_coefficient_difference"], local_differences
            )
        )
        for index in range(len(shape)):
            paired_match = paired_match and estimate_matches(
                actual_step["cyclic_component_differences"][index]["estimate"],
                [difference[index] for difference in vector_differences],
            ) and estimate_matches(
                actual_step["nonlocal_component_differences"][index]["estimate"],
                [difference[index] for difference in residual_differences],
            )
    diagnostics = result["convergence_diagnostics"]
    expected_full_order = math.log(full_steps[0] / full_steps[1], 2.0)
    expected_local_order = math.log(local_steps[0] / local_steps[1], 2.0)
    diagnostics_match = (
        close(float(diagnostics["full_vector_effective_order"]), expected_full_order)
        and close(
            float(diagnostics["local_coefficient_effective_order"]),
            expected_local_order,
        )
        and bool(diagnostics["full_vector_step_contracts"])
        == (full_steps[1] < full_steps[0])
        and bool(diagnostics["local_coefficient_step_contracts"])
        == (local_steps[1] < local_steps[0])
    )
    for index, row in enumerate(diagnostics["nonlocal_component_diagnostics"]):
        expected_order = math.log(
            nonlocal_steps[0][index] / nonlocal_steps[1][index], 2.0
        )
        diagnostics_match = diagnostics_match and (
            close(float(row["effective_order"]), expected_order)
            and bool(row["contracts"])
            == (nonlocal_steps[1][index] < nonlocal_steps[0][index])
        )
    extrapolated_vectors: list[list[complex]] = []
    extrapolated_coefficients: list[complex] = []
    extrapolated_residuals: list[list[complex]] = []
    extrapolated_orthogonalities: list[float] = []
    for seed in config["seeds"]:
        larger = rebuilt_vectors[(config["epsilon_ids"][-2], int(seed))]
        smaller = rebuilt_vectors[(config["epsilon_ids"][-1], int(seed))]
        extrapolated = [
            2.0 * smaller_value - larger_value
            for smaller_value, larger_value in zip(smaller, larger)
        ]
        coefficient, residual, orthogonality = project(extrapolated, shape)
        extrapolated_vectors.append(extrapolated)
        extrapolated_coefficients.append(coefficient)
        extrapolated_residuals.append(residual)
        extrapolated_orthogonalities.append(orthogonality)
    linear = result["linear_epsilon_zero_diagnostic"]
    linear_match = (
        linear["available"]
        and int(linear["paired_scrambles"]) == len(config["seeds"])
        and estimate_matches(linear["local_coefficient"], extrapolated_coefficients)
        and close(
            float(linear["maximum_eventwise_projection_orthogonality_residual"]),
            max(extrapolated_orthogonalities),
        )
    )
    for index in range(len(shape)):
        linear_match = linear_match and estimate_matches(
            linear["cyclic_components"][index]["estimate"],
            [vector[index] for vector in extrapolated_vectors],
        ) and estimate_matches(
            linear["nonlocal_components"][index]["estimate"],
            [residual[index] for residual in extrapolated_residuals],
        )
    target_lookup = {
        float(row["physical_s_channel_cosine"]): float(
            row["required_matched_hhh_nonlocal_cyclic_D_over_G3"]
        )
        for row in config["target_rows"]
    }
    target_match = True
    target_differences: list[float] = []
    for index, row in enumerate(linear["fixed_5018_target_comparison"]):
        cosine = float(config["physical_cosines"][index])
        estimate = aggregate(
            [residual[index] for residual in extrapolated_residuals]
        )
        expected_target = target_lookup[cosine]
        difference = estimate["mean"].real - expected_target
        target_differences.append(difference)
        target_match = target_match and (
            close(float(row["predicted_extrapolated_nonlocal_real"]), estimate["mean"].real)
            and close(float(row["RQMC_standard_error"]), estimate["real_standard_error"])
            and close(float(row["fixed_5018_target"]), expected_target)
            and close(float(row["predicted_minus_target"]), difference)
        )
    target_rms = math.sqrt(
        sum(value * value for value in target_differences) / len(target_differences)
    )
    target_match = target_match and close(
        float(linear["RMS_nonlocal_target_difference"]), target_rms
    )
    rebuilt_audit = independent_global_audit(config, direct)
    audit_match = len(rebuilt_audit) == len(result["global_tier_audit"])
    for expected_audit, actual_audit in zip(
        rebuilt_audit, result["global_tier_audit"]
    ):
        audit_match = audit_match and (
            actual_audit["complete"]
            and close(float(actual_audit["epsilon"]), expected_audit["epsilon"])
            and close_complex(
                complex_from_row(actual_audit["primary24"]),
                expected_audit["primary24"],
            )
            and close_complex(
                complex_from_row(actual_audit["audit32"]),
                expected_audit["audit32"],
            )
            and close(
                float(actual_audit["relative_difference"]),
                expected_audit["relative_difference"],
            )
        )
    audit_threshold = float(
        config["numerical_gate_thresholds"][
            "maximum_global_tier_relative_difference"
        ]
    )
    projection_threshold = float(
        config["numerical_gate_thresholds"][
            "maximum_projection_orthogonality_residual"
        ]
    )
    all_numeric = actual == expected and all(
        row["integral_converged"]
        and row["topology_passed"]
        and finite_complex_row(row["normalized_direct_D_hhh_over_G3"])
        for row in jobs
    )
    audit_within = max(
        row["relative_difference"] for row in rebuilt_audit
    ) <= audit_threshold
    projection_exact = max(projection_residuals) <= projection_threshold
    nonlocal_contract = all(
        second < first
        for first, second in zip(nonlocal_steps[0], nonlocal_steps[1])
    )
    expected_gate = {
        "all_expected_jobs_numeric_and_converged": all_numeric,
        "all_three_primary_vectors_complete": len(rebuilt_vectors) == 6,
        "global24_global32_audit_complete": len(rebuilt_audit) == 3,
        "global24_global32_within_threshold": audit_within,
        "eventwise_local_nonlocal_projection_orthogonal": projection_exact,
        "full_vector_mean_step_contracts": full_steps[1] < full_steps[0],
        "local_coefficient_mean_step_contracts": local_steps[1] < local_steps[0],
        "all_five_nonlocal_mean_steps_contract": nonlocal_contract,
        "paired_full_vector_ladder_stable": (
            all_numeric
            and len(rebuilt_vectors) == 6
            and len(rebuilt_audit) == 3
            and audit_within
            and projection_exact
            and full_steps[1] < full_steps[0]
            and local_steps[1] < local_steps[0]
            and nonlocal_contract
        ),
        "epsilon_zero_limit_complete": False,
        "production_precision_complete": False,
        "crossing_complete_hhh_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    vector_csv = read_csv(VECTOR_CSV)
    decomposition_csv = read_csv(DECOMPOSITION_CSV)
    paired_csv = read_csv(PAIRED_CSV)
    target_csv = read_csv(TARGET_CSV)
    gate_csv = read_csv(GATE_CSV)
    csv_gate = {row["check"]: row["passed"].lower() == "true" for row in gate_csv}
    document_text = DOCUMENT.read_text(encoding="utf-8")
    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    resume_text = RESUME.read_text(encoding="utf-8")
    runner_text = RUNNER.read_text(encoding="utf-8")
    decomposition_precedes_target = (
        runner_text.index(
            "coefficient, residual, orthogonality = project_vector(vector, shape)"
        )
        < runner_text.index("target = {")
    )
    cited_relative_paths = [
        ROOT / value
        for value in re.findall(r"`(post-checkpoint-work/[^`]+)`", provenance_text)
    ]
    authoritative = (
        DOCUMENT,
        PROVENANCE,
        RESULT,
        VECTOR_CSV,
        DECOMPOSITION_CSV,
        PAIRED_CSV,
        TARGET_CSV,
        GATE_CSV,
    )
    formal_digest = tree_digest(FORMAL)
    return [
        (
            "scripts_ast_parse",
            all(
                ast.parse(path.read_text(encoding="utf-8")) is not None
                for path in (RUNNER, REPAIR, Path(__file__).resolve())
            ),
            "runner, v4 radius rule and final validator parse",
        ),
        (
            "immutable_config_digest",
            supplied_config_digest == CONFIG_DIGEST
            and supplied_config_digest == canonical_digest(unsigned_config),
            supplied_config_digest,
        ),
        (
            "source_digest_lock",
            source_digests_match,
            f"{len(config['source_files'])} config source hashes match",
        ),
        (
            "terminal_job_matrix",
            status["state"] == "COMPLETE"
            and status["expected_jobs"] == 99
            and status["terminal_jobs"] == 99
            and status["remaining_jobs"] == 0
            and status["failed_jobs"] == 0
            and status["unconverged_jobs"] == 0
            and len(jobs) == 99
            and len(imported) == 51
            and len(computed) == 48
            and (RUN / "COMPLETE").exists(),
            "99/99 terminal: 51 exact imports plus 48 computed",
        ),
        (
            "expected_job_identity",
            actual == expected,
            f"expected={len(expected)} actual={len(actual)}",
        ),
        (
            "exact_import_provenance",
            imported_sources_match
            and all(row["integral_converged"] and row["topology_passed"] for row in imported),
            "all 51 imported source-job SHA-256 chains validate",
        ),
        (
            "computed_topologies_and_kernels",
            len(computed_kernels) == 48
            and len(list((RUN / "topologies").glob("*.json"))) == 48
            and len(list((RUN / "kernels").glob("*.json"))) == 48
            and all(Path(row["topology_file"]).exists() for row in computed)
            and all(Path(row["kernel_file"]).exists() for row in computed)
            and all(
                kernel["fixed_event_integral_gate"]["fixed_event_crossed_integral_converged"]
                and kernel["fixed_event_integral_gate"]["all_residues_stable"]
                for kernel in computed_kernels
            ),
            "48 target-specific topology/kernel pairs close their gates",
        ),
        (
            "finite_direct_values",
            all_numeric,
            "all 99 expected normalized direct values are finite and converged",
        ),
        (
            "shrinking_radius_contract",
            all(
                row["residue_radius_contract"]["revision"] == RADIUS_REVISION
                and row["residue_radius_contract"]["adjustment_count"] == 0
                and row["residue_radius_contract"]["repair_script_sha256"]
                == digest(REPAIR)
                for row in computed
            )
            and all(
                kernel["fixed_event_integral_gate"]["relative_residue_revision"]
                == RADIUS_REVISION
                for kernel in computed_kernels
            ),
            "v4 active on 48/48 new kernels; zero radius adjustments",
        ),
        (
            "cyclic_vectors_rebuilt",
            per_seed_vectors_match,
            "all six cyclic vectors independently rebuilt from 99 direct jobs",
        ),
        (
            "eventwise_decomposition_rebuilt",
            summaries_match and projection_exact,
            f"max independent projection residual={max(projection_residuals):.6g}",
        ),
        (
            "paired_steps_rebuilt",
            paired_match and [row["paired_scrambles"] for row in result["paired_convergence"]] == [2, 2],
            f"full steps={full_steps}; local steps={local_steps}",
        ),
        (
            "convergence_diagnostics_rebuilt",
            diagnostics_match
            and full_steps[1] < full_steps[0]
            and local_steps[1] < local_steps[0]
            and nonlocal_contract,
            "full/local/all-five-nonlocal paired mean steps contract",
        ),
        (
            "global_tier_audit_rebuilt",
            audit_match and audit_within,
            f"max relative difference={max(row['relative_difference'] for row in rebuilt_audit):.6g}",
        ),
        (
            "linear_diagnostic_rebuilt",
            linear_match,
            "2*C(0.02)-C(0.04) independently reproduced for two scrambles",
        ),
        (
            "fixed_target_comparison_rebuilt",
            target_match
            and linear["target_loaded_after_decomposition"]
            and not linear["target_fitted"]
            and decomposition_precedes_target,
            f"untouched 5018 target comparison RMS={target_rms:.9g}",
        ),
        (
            "gate_truth_table",
            result["gate"] == expected_gate and csv_gate == expected_gate,
            "serialized JSON/CSV gates equal independent gate reconstruction",
        ),
        (
            "claim_boundary",
            result["gate"]["paired_full_vector_ladder_stable"]
            and not result["epsilon_limit_complete"]
            and not result["production_precision_complete"]
            and not result["valid_for_full_MTS_claim"]
            and not result["target_fitted"]
            and not linear["epsilon_zero_claimed"],
            "numerical smoke passes; epsilon zero, production and MTS claims remain false",
        ),
        (
            "csv_outputs_parse",
            len(vector_csv) == 15
            and len(decomposition_csv) == 15
            and len(paired_csv) == 2
            and len(target_csv) == 5
            and len(gate_csv) == len(expected_gate),
            "vector=15 decomposition=15 paired=2 target=5 gate=13 rows",
        ),
        (
            "provenance_paths_exist",
            len(cited_relative_paths) >= 4
            and all(path.exists() for path in cited_relative_paths),
            f"all {len(cited_relative_paths)} relative provenance paths exist",
        ),
        (
            "completed_handoff_recorded",
            "**Status: COMPLETE" in document_text
            and CONFIG_DIGEST in document_text
            and MARKER in document_text
            and MARKER in resume_text
            and "5037-Y5-R2FR-paired-outer-precision" in resume_text
            and "No GitHub action was taken" in resume_text,
            "completed checkpoint, boundaries and next target recorded",
        ),
        (
            "no_missing_markers",
            all(
                "MISSING_" not in path.read_text(encoding="utf-8", errors="ignore")
                for path in authoritative
            ),
            "no placeholder marker in authoritative 5036 artifacts",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "pycache_removed",
            not any(path.is_dir() for path in POST.rglob("__pycache__")),
            "no __pycache__ directory under post-checkpoint-work",
        ),
    ]


def main() -> None:
    rows = check_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(rows, start=1):
            writer.writerow(
                {
                    "check_id": f"V5036_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in rows if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(rows),
                "failed": failed,
                "passed": not failed,
                "output": str(OUTPUT),
            },
            indent=2,
        )
    )
    if failed:
        raise RuntimeError(f"checkpoint 5036 validation failed: {failed}")


if __name__ == "__main__":
    main()
