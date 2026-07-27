from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import t


POST = Path(__file__).resolve().parents[1]
SCRIPT_5037 = POST / "scripts" / "Y5_R2FR_5037_paired_outer_precision_reflection_control.py"
SOURCE_5037 = POST / "source-intake" / "functional_rg" / "5037"
SOURCE_5037_RUN = SOURCE_5037 / "runs" / "paired_outer_precision_s4_v1"
SOURCE_5037_RESULT = SOURCE_5037 / "paired_outer_precision_results.json"
SOURCE_5018_TARGET = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5018"
    / "known_master_without_hhh_and_matched_hhh_target.csv"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5040"
RUNS = SOURCE / "runs"
RESULT_JSON = SOURCE / "nested_sobol_results.json"
VECTOR_CSV = SOURCE / "epsilon_cyclic_vector.csv"
DECOMPOSITION_CSV = SOURCE / "local_nonlocal_decomposition.csv"
PAIRED_CSV = SOURCE / "paired_vector_convergence.csv"
TARGET_CSV = SOURCE / "epsilon_zero_target_comparison.csv"
GATE_CSV = SOURCE / "outer_precision_gate.csv"
REFLECTION_CSV = SOURCE / "reflection_control.csv"
PRECISION_CSV = SOURCE / "outer_precision_diagnostic.csv"
DESIGN_JSON = SOURCE / "sequential_sampling_design.json"
AUDIT_JSON = SOURCE / "nested_sobol_variance_audit.json"
TARGET_BUDGET_CSV = SOURCE / "target_precision_budget.csv"
DESIGN_COMPARISON_CSV = SOURCE / "equal_cost_design_comparison.csv"
SEQUENTIAL_GATE_CSV = SOURCE / "sequential_stopping_gate.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
MARKER = "MTS_5040_NESTED_SOBOL_VARIANCE_REDUCTION"
SCHEMA_REVISION = "nested-base2-rqmc-sequential-stopping-v1"
CONFIDENCE = 0.95
SEEDS = (503401, 503402, 503403, 503404)
EPSILON_IDS = ("E080", "E040", "E020")


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5037 = load_module("mts_5037_for_5040", SCRIPT_5037)
M5036 = M5037.M5036
ORIGINAL_SOURCE_MAPS = M5037.source_maps
ORIGINAL_EXPECTED_JOBS = M5036.expected_jobs


def configure_output_modules() -> None:
    M5037.MARKER = MARKER
    M5037.SCHEMA_REVISION = SCHEMA_REVISION
    M5037.SOURCE = SOURCE
    M5037.RUNS = RUNS
    M5037.RESULT_JSON = RESULT_JSON
    M5037.VECTOR_CSV = VECTOR_CSV
    M5037.DECOMPOSITION_CSV = DECOMPOSITION_CSV
    M5037.PAIRED_CSV = PAIRED_CSV
    M5037.TARGET_CSV = TARGET_CSV
    M5037.GATE_CSV = GATE_CSV
    M5037.REFLECTION_CSV = REFLECTION_CSV
    M5037.PRECISION_CSV = PRECISION_CSV
    M5037.PROVENANCE = PROVENANCE
    M5036.MARKER = MARKER
    M5036.SCHEMA_REVISION = SCHEMA_REVISION
    M5036.SOURCE = SOURCE
    M5036.RUNS = RUNS
    M5036.RESULT_JSON = RESULT_JSON
    M5036.VECTOR_CSV = VECTOR_CSV
    M5036.DECOMPOSITION_CSV = DECOMPOSITION_CSV
    M5036.PAIRED_CSV = PAIRED_CSV
    M5036.TARGET_CSV = TARGET_CSV
    M5036.GATE_CSV = GATE_CSV
    M5036.PROVENANCE = PROVENANCE
    M5036.M5035.MARKER = MARKER
    M5036.M5035.M5034.MARKER = MARKER


configure_output_modules()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def target_budget_rows() -> list[dict[str, Any]]:
    rows = []
    for source in read_csv(SOURCE_5018_TARGET):
        residual = float(source["known_nonlocal_residual"])
        target = float(source["required_matched_hhh_nonlocal_cyclic_D_over_G3"])
        if not math.isclose(target, -0.5 * residual, rel_tol=0.0, abs_tol=1.0e-12):
            raise RuntimeError("5018 hhh target is not the signed half-residual")
        target_error = 0.5 * float(source["known_master_error"])
        rows.append(
            {
                "physical_s_channel_cosine": float(source["physical_s_channel_cosine"]),
                "fixed_target": target,
                "known_master_error": float(source["known_master_error"]),
                "target_equivalence_margin": target_error,
                "statistical_halfwidth_budget": 0.5 * target_error,
                "epsilon_bias_budget": 0.5 * target_error,
                "margin_derivation": "target=-known_nonlocal_residual/2; margin=known_master_error/2",
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def source_maps() -> list[tuple[str, dict[Any, Any], dict[Any, Any]]]:
    mapping, events = M5036.source_job_map(
        SOURCE_5037_RUN, "5037_complete_four_scramble_sample0"
    )
    return [
        ("5037_complete_four_scramble_sample0", mapping, events),
        *ORIGINAL_SOURCE_MAPS(),
    ]


M5037.source_maps = source_maps


def expected_jobs(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows = ORIGINAL_EXPECTED_JOBS(config)
    central = min(
        config["crossings"],
        key=lambda row: abs(row["physical_s_channel_cosine"]),
    )
    central_ids = (
        central["s_argument_id"],
        central["t_argument_id"],
        central["u_argument_id"],
    )
    audit_events = [
        row for row in config["events"] if row["seed"] == config["audit_seed"]
    ]
    existing = {row["job_key"] for row in rows}
    for epsilon_label, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        for event in audit_events:
            for base_id in central_ids:
                job_key = (
                    f"{epsilon_label}__{event['event_id']}__{base_id}__audit32"
                )
                if job_key in existing:
                    continue
                rows.append(
                    {
                        "job_key": job_key,
                        "epsilon_id": epsilon_label,
                        "evaluation_epsilon": epsilon,
                        "event_id": event["event_id"],
                        "argument_id": f"{epsilon_label}_{base_id}",
                        "base_argument_id": base_id,
                        "tier": "audit32",
                    }
                )
                existing.add(job_key)
    return rows


M5036.expected_jobs = expected_jobs


def make_config(arguments: argparse.Namespace) -> dict[str, Any]:
    if arguments.power != 1:
        raise ValueError("5040 locks the nested Sobol pilot to power=1")
    requested_seeds = tuple(M5036.parse_csv_ints(arguments.seeds))
    if requested_seeds != SEEDS:
        raise ValueError("5040 locks the four existing independent scramble seeds")
    config = M5037.make_config(arguments)
    config.pop("config_digest", None)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = SCHEMA_REVISION
    config["source_reuse"]["complete_5037_sample0_matrix"] = str(SOURCE_5037_RUN)
    config["source_reuse"]["nested_event_identity_required"] = True
    config["outer_precision_contract"].update(
        {
            "design": "four independent Owen scrambles with a nested base-2 pair in each scramble",
            "sample0_source": "immutable 5037 four-scramble matrix",
            "samples_per_scramble": 2,
            "new_sample_indices": [1],
            "equal_cost_independent_comparator": "eight independent one-point scrambles",
            "minimum_scrambles_for_target_verdict": 4,
            "production_precision_claimed": False,
        }
    )
    margins = target_budget_rows()
    normal_critical = float(t.ppf(0.5 + CONFIDENCE / 2.0, 10_000_000))
    nested_critical = float(t.ppf(0.5 + CONFIDENCE / 2.0, 3))
    independent_critical = float(t.ppf(0.5 + CONFIDENCE / 2.0, 7))
    sd_ratio_threshold = independent_critical / nested_critical * math.sqrt(4.0 / 8.0)
    config["equal_cost_design_contract"] = {
        "new_event_points_per_arm": 4,
        "independent_arm": "add four one-point scrambles, yielding n=8",
        "nested_arm": "add sample index 1 to each existing scramble, yielding n=4,m=2",
        "independent_halfwidth_model": "t_7*s_m1/sqrt(8)",
        "nested_halfwidth_model": "t_3*s_m2/sqrt(4)",
        "nested_sd_ratio_required_to_beat_independent": sd_ratio_threshold,
        "selection_metric": "maximum target-margin-normalized 95% halfwidth over five components",
        "selection_deferred_until_four_nested_replicates": True,
    }
    config["sequential_stopping_contract"] = {
        "confidence": CONFIDENCE,
        "fixed_target_fitted": False,
        "target_margin_source": str(SOURCE_5018_TARGET),
        "target_margin_formula": "known_master_error/2 because hhh target=-known_nonlocal_residual/2",
        "target_equivalence_gate": "abs(mean residual)+t halfwidth+(2/3) linear-defect upper bound <= target margin",
        "imaginary_gate": "abs(mean imaginary)+t halfwidth+(2/3) linear-defect upper bound <= target margin",
        "contraction_gate": "upper 95% bound of |step_2|-|step_1| is below zero for every component",
        "reflection_gate": "odd target residual obeys its propagated source margin; symmetry is not imposed",
        "quadrature_gate": "all primary24 rows converge and declared audit32 rows agree",
        "optional_stopping_for_success": "all gates pass simultaneously",
        "optional_stopping_for_failure": "a target residual interval is disjoint from its equivalence band after regulator-bias accounting",
        "otherwise": "continue the selected nested or independent ladder",
        "normal_critical_for_planning_only": normal_critical,
    }
    config["source_files"].update(
        {
            str(Path(__file__).resolve()): digest(Path(__file__).resolve()),
            str(SOURCE_5037_RUN / "config.json"): digest(SOURCE_5037_RUN / "config.json"),
            str(SOURCE_5037_RUN / "status.json"): digest(SOURCE_5037_RUN / "status.json"),
            str(SOURCE_5037_RUN / "COMPLETE"): digest(SOURCE_5037_RUN / "COMPLETE"),
            str(SOURCE_5037_RESULT): digest(SOURCE_5037_RESULT),
            str(SOURCE_5018_TARGET): digest(SOURCE_5018_TARGET),
        }
    )
    config["target_precision_budgets"] = margins
    config["target_fitted"] = False
    config["epsilon_limit_complete"] = False
    config["production_precision_complete"] = False
    config["valid_for_full_MTS_claim"] = False
    config["config_digest"] = M5036.canonical_digest(config)
    return config


def execution_order(
    config: dict[str, Any], expected: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    events = M5036.event_lookup(config)
    seed_index = {int(seed): index for index, seed in enumerate(config["seeds"])}
    epsilon_index = {"E040": 0, "E020": 1, "E080": 2}
    base_index = {
        value: index for index, value in enumerate(M5036.ordered_base_argument_ids(config))
    }
    return sorted(
        expected,
        key=lambda row: (
            int(events[row["event_id"]]["sample_index"]),
            seed_index[int(events[row["event_id"]]["seed"])],
            0 if row["tier"] == "primary24" else 1,
            epsilon_index[row["epsilon_id"]],
            base_index[row["base_argument_id"]],
        ),
    )


def complex_array(row: list[dict[str, float]]) -> np.ndarray:
    return np.asarray([M5036.complex_from_row(value) for value in row], dtype=np.complex128)


def complete_vectors(result: dict[str, Any]) -> dict[tuple[int, str], np.ndarray]:
    return {
        (int(row["seed"]), str(row["epsilon_id"])): complex_array(row["cyclic_vector"])
        for row in result["cyclic_vectors_per_seed"]
        if row.get("cyclic_vector") is not None
        and row["completed_samples"] == row["expected_samples"]
    }


def projected_ladder(
    vectors: dict[tuple[int, str], np.ndarray], seeds: list[int]
) -> dict[str, np.ndarray]:
    shape = 1.0 - np.asarray((-0.6, -0.3, 0.0, 0.3, 0.6), dtype=float) ** 2
    nonlocal_rows: dict[tuple[int, str], np.ndarray] = {}
    for seed in seeds:
        for epsilon_id in EPSILON_IDS:
            vector = vectors[(seed, epsilon_id)]
            _, residual, _ = M5036.project_vector(vector, shape)
            nonlocal_rows[(seed, epsilon_id)] = residual
    step_one = np.stack(
        [nonlocal_rows[(seed, "E040")] - nonlocal_rows[(seed, "E080")] for seed in seeds]
    )
    step_two = np.stack(
        [nonlocal_rows[(seed, "E020")] - nonlocal_rows[(seed, "E040")] for seed in seeds]
    )
    return {
        "step_one": step_one,
        "step_two": step_two,
        "linear_defect": step_two - 0.5 * step_one,
        "richardson": np.stack(
            [
                2.0 * nonlocal_rows[(seed, "E020")]
                - nonlocal_rows[(seed, "E040")]
                for seed in seeds
            ]
        ),
    }


def interval(values: np.ndarray) -> dict[str, Any] | None:
    values = np.asarray(values, dtype=float)
    if len(values) < 2:
        return None
    mean = float(np.mean(values))
    sd = float(np.std(values, ddof=1))
    standard_error = sd / math.sqrt(len(values))
    critical = float(t.ppf(0.5 + CONFIDENCE / 2.0, len(values) - 1))
    halfwidth = critical * standard_error
    return {
        "count": len(values),
        "mean": mean,
        "sample_sd": sd,
        "standard_error": standard_error,
        "critical": critical,
        "halfwidth": halfwidth,
        "lower": mean - halfwidth,
        "upper": mean + halfwidth,
    }


def planning_count(sample_sd: float, halfwidth_budget: float) -> int:
    if sample_sd == 0.0:
        return 2
    count = max(2, math.ceil((1.96 * sample_sd / halfwidth_budget) ** 2))
    for _ in range(12):
        critical = float(t.ppf(0.5 + CONFIDENCE / 2.0, count - 1))
        updated = max(2, math.ceil((critical * sample_sd / halfwidth_budget) ** 2))
        if updated == count:
            break
        count = updated
    return count


def one_point_design() -> dict[str, Any]:
    source_result = json.loads(SOURCE_5037_RESULT.read_text(encoding="utf-8"))
    vectors = complete_vectors(source_result)
    seeds = sorted({seed for seed, epsilon_id in vectors if epsilon_id == "E020"})
    ladder = projected_ladder(vectors, seeds)
    budgets = target_budget_rows()
    rows = []
    for component_index, budget in enumerate(budgets):
        residuals = ladder["richardson"][:, component_index].real - budget["fixed_target"]
        residual_interval = interval(residuals)
        if residual_interval is None:
            raise RuntimeError("5037 does not contain four one-point replicates")
        strict_count = planning_count(
            residual_interval["sample_sd"], budget["statistical_halfwidth_budget"]
        )
        rows.append(
            {
                **budget,
                "sample0_residual_mean": residual_interval["mean"],
                "sample0_residual_sd": residual_interval["sample_sd"],
                "sample0_residual_95_halfwidth": residual_interval["halfwidth"],
                "normal_approximate_replicates_for_strict_statistical_budget": strict_count,
                "brute_independent_sampling_practical": strict_count <= 10_000,
            }
        )
    maximum_count = max(row["normal_approximate_replicates_for_strict_statistical_budget"] for row in rows)
    return {
        "source_result": str(SOURCE_5037_RESULT),
        "source_result_sha256": digest(SOURCE_5037_RESULT),
        "sample0_scrambles": len(seeds),
        "rows": rows,
        "maximum_strict_planning_count": maximum_count,
        "brute_independent_route_rejected_as_primary": maximum_count > 10_000,
        "reason": "source-derived target margins make one-point Monte Carlo prohibitively expensive; test nested randomized-QMC variance reduction first",
    }


def nested_audit(config: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    source_result = json.loads(SOURCE_5037_RESULT.read_text(encoding="utf-8"))
    source_vectors = complete_vectors(source_result)
    nested_vectors = complete_vectors(summary)
    complete_seeds = [
        int(seed)
        for seed in config["seeds"]
        if all((int(seed), epsilon_id) in nested_vectors for epsilon_id in EPSILON_IDS)
    ]
    source_ladder = projected_ladder(source_vectors, list(SEEDS))
    budgets = target_budget_rows()
    comparison_rows: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []
    design_decision = "PENDING_FOUR_COMPLETE_NESTED_REPLICATES"
    nested_metric = None
    independent_metric = None
    strict_target_gate = False
    contraction_gate = False
    imaginary_gate = False
    if complete_seeds:
        current_ladder = projected_ladder(nested_vectors, complete_seeds)
    else:
        current_ladder = None
    for component_index, budget in enumerate(budgets):
        source_sd = float(np.std(source_ladder["richardson"][:, component_index].real, ddof=1))
        independent_halfwidth = float(t.ppf(0.975, 7) * source_sd / math.sqrt(8.0))
        row: dict[str, Any] = {
            "component_index": component_index,
            "physical_s_channel_cosine": budget["physical_s_channel_cosine"],
            "target_equivalence_margin": budget["target_equivalence_margin"],
            "sample0_sd": source_sd,
            "expected_eight_independent_halfwidth": independent_halfwidth,
            "nested_complete_scrambles": len(complete_seeds),
            "nested_sd": None,
            "nested_halfwidth": None,
            "nested_to_independent_halfwidth_ratio": None,
            "nested_to_sample0_sd_ratio": None,
            "target_total_bound": None,
            "target_equivalent": False,
            "imaginary_total_bound": None,
            "imaginary_equivalent": False,
            "contraction_upper_95": None,
            "contraction_supported": False,
            "valid_for_full_MTS_claim": False,
        }
        if current_ladder is not None and len(complete_seeds) >= 2:
            richardson = current_ladder["richardson"][:, component_index]
            residual_interval = interval(richardson.real - budget["fixed_target"])
            imaginary_interval = interval(richardson.imag)
            defect_real_interval = interval(current_ladder["linear_defect"][:, component_index].real)
            defect_imaginary_interval = interval(current_ladder["linear_defect"][:, component_index].imag)
            contraction_interval = interval(
                np.abs(current_ladder["step_two"][:, component_index])
                - np.abs(current_ladder["step_one"][:, component_index])
            )
            if None in (
                residual_interval,
                imaginary_interval,
                defect_real_interval,
                defect_imaginary_interval,
                contraction_interval,
            ):
                raise RuntimeError("nested interval unexpectedly unavailable")
            nested_sd = residual_interval["sample_sd"]
            nested_halfwidth = residual_interval["halfwidth"]
            real_bias_bound = 2.0 / 3.0 * max(
                abs(defect_real_interval["lower"]), abs(defect_real_interval["upper"])
            )
            imaginary_bias_bound = 2.0 / 3.0 * max(
                abs(defect_imaginary_interval["lower"]),
                abs(defect_imaginary_interval["upper"]),
            )
            target_total_bound = (
                abs(residual_interval["mean"])
                + residual_interval["halfwidth"]
                + real_bias_bound
            )
            imaginary_total_bound = (
                abs(imaginary_interval["mean"])
                + imaginary_interval["halfwidth"]
                + imaginary_bias_bound
            )
            row.update(
                {
                    "nested_sd": nested_sd,
                    "nested_halfwidth": nested_halfwidth,
                    "nested_to_independent_halfwidth_ratio": nested_halfwidth / independent_halfwidth,
                    "nested_to_sample0_sd_ratio": nested_sd / source_sd,
                    "target_total_bound": target_total_bound,
                    "target_equivalent": target_total_bound <= budget["target_equivalence_margin"],
                    "imaginary_total_bound": imaginary_total_bound,
                    "imaginary_equivalent": imaginary_total_bound <= budget["target_equivalence_margin"],
                    "contraction_upper_95": contraction_interval["upper"],
                    "contraction_supported": contraction_interval["upper"] < 0.0,
                }
            )
        comparison_rows.append(row)
    if len(complete_seeds) == 4:
        nested_metric = max(
            row["nested_halfwidth"] / row["target_equivalence_margin"]
            for row in comparison_rows
        )
        independent_metric = max(
            row["expected_eight_independent_halfwidth"]
            / row["target_equivalence_margin"]
            for row in comparison_rows
        )
        design_decision = (
            "CONTINUE_NESTED_BASE2_LADDER"
            if nested_metric < independent_metric
            else "SWITCH_TO_ADDITIONAL_INDEPENDENT_SCRAMBLES"
        )
        strict_target_gate = all(row["target_equivalent"] for row in comparison_rows)
        imaginary_gate = all(row["imaginary_equivalent"] for row in comparison_rows)
        contraction_gate = all(row["contraction_supported"] for row in comparison_rows)
    primary_sample1 = 0
    audit_sample1 = 0
    jobs = M5036.load_jobs(RUNS / config["run_id"])
    for job in jobs.values():
        if int(job.get("sample_index", -1)) != 1:
            continue
        if job.get("status") not in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}:
            continue
        if job["tier"] == "primary24":
            primary_sample1 += 1
        else:
            audit_sample1 += 1
    gate_rows.extend(
        [
            {
                "gate": "four_nested_scrambles_complete",
                "passed": len(complete_seeds) == 4,
                "detail": f"{len(complete_seeds)}/4",
            },
            {
                "gate": "strict_target_equivalence",
                "passed": strict_target_gate,
                "detail": "source-derived margins with statistical and epsilon-bias bounds",
            },
            {
                "gate": "imaginary_zero_equivalence",
                "passed": imaginary_gate,
                "detail": "same source-derived margins",
            },
            {
                "gate": "all_components_contract",
                "passed": contraction_gate,
                "detail": "upper paired 95% magnitude-delta bound below zero",
            },
            {
                "gate": "production_precision_complete",
                "passed": False,
                "detail": "cannot pass before design selection and sequential continuation",
            },
            {
                "gate": "valid_for_full_MTS_claim",
                "passed": False,
                "detail": "numerical hhh subproblem only",
            },
        ]
    )
    return {
        "checkpoint_marker": MARKER,
        "run_state": summary["run_state"],
        "complete_nested_scrambles": complete_seeds,
        "sample1_primary_jobs_converged": primary_sample1,
        "sample1_primary_jobs_expected": 180,
        "sample1_audit_jobs_converged": audit_sample1,
        "sample1_audit_jobs_expected": 9,
        "equal_cost_design_decision": design_decision,
        "nested_worst_target_normalized_halfwidth": nested_metric,
        "independent_worst_target_normalized_halfwidth": independent_metric,
        "component_rows": comparison_rows,
        "gate_rows": gate_rows,
        "target_fitted": False,
        "reflection_symmetry_imposed": False,
        "epsilon_zero_claimed": False,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def write_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    M5036.write_csv(path, rows, fieldnames)


def write_5040_artifacts(
    config: dict[str, Any], summary: dict[str, Any], run_directory: Path
) -> dict[str, Any]:
    M5037.write_checkpoint_artifacts(config, summary, run_directory)
    design = one_point_design()
    audit = nested_audit(config, summary)
    M5036.atomic_json(
        DESIGN_JSON,
        {
            "checkpoint_marker": MARKER,
            "config_digest": config["config_digest"],
            "equal_cost_design_contract": config["equal_cost_design_contract"],
            "sequential_stopping_contract": config["sequential_stopping_contract"],
            "one_point_baseline": design,
            "selected_pilot": "nested power=1 base-2 pair on the same four independent scrambles",
            "selection_reason": "equal event cost also measures whether scrambled-net stratification beats simply doubling independent replicates",
            "target_fitted": False,
            "valid_for_full_MTS_claim": False,
        },
    )
    M5036.atomic_json(AUDIT_JSON, audit)
    write_rows(
        TARGET_BUDGET_CSV,
        design["rows"],
        list(design["rows"][0]),
    )
    write_rows(
        DESIGN_COMPARISON_CSV,
        audit["component_rows"],
        list(audit["component_rows"][0]),
    )
    write_rows(
        SEQUENTIAL_GATE_CSV,
        [
            {**row, "valid_for_full_MTS_claim": False}
            for row in audit["gate_rows"]
        ],
        ["gate", "passed", "detail", "valid_for_full_MTS_claim"],
    )
    M5036.atomic_text(
        PROVENANCE,
        f"""# 5040 provenance

- Marker: `{MARKER}`.
- Run directory: `{run_directory}`.
- Config digest: `{config['config_digest']}`.
- Immutable sample-0 source: `{SOURCE_5037_RUN}`.
- Sample-0 result SHA-256: `{digest(SOURCE_5037_RESULT)}`.
- Fixed-target source: `{SOURCE_5018_TARGET}`.
- Fixed-target source SHA-256: `{digest(SOURCE_5018_TARGET)}`.
- Every import requires exact epsilon, seed, sample index, argument and tier identity plus a source-job SHA-256.
- The second Sobol point is nested inside each of the same four Owen scrambles; no point or target is fitted.
- The equal-cost comparator is four additional independent one-point scrambles.
- Source-derived target margins are half the 5018 known-master errors because the required hhh target is the signed half-residual.
- This is a variance-reduction pilot. It is not an epsilon-zero, production hhh, local-GR or full-MTS claim.
""",
    )
    return audit


def dry_run_summary(config: dict[str, Any]) -> dict[str, Any]:
    expected = M5036.expected_jobs(config)
    mappings = source_maps()
    reusable = [
        row for row in expected if M5037.reusable_source(row, config, mappings) is not None
    ]
    design = one_point_design()
    return {
        "checkpoint_marker": MARKER,
        "dry_run": True,
        "run_id": config["run_id"],
        "config_digest": config["config_digest"],
        "power": config["power"],
        "samples_per_seed": config["samples_per_seed"],
        "expected_jobs": len(expected),
        "source_locked_imports": len(reusable),
        "new_kernels_required": len(expected) - len(reusable),
        "sample0_strict_planning_counts": [
            row["normal_approximate_replicates_for_strict_statistical_budget"]
            for row in design["rows"]
        ],
        "brute_independent_route_rejected_as_primary": design[
            "brute_independent_route_rejected_as_primary"
        ],
        "target_fitted": False,
        "valid_for_full_MTS_claim": False,
    }


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    config = make_config(arguments)
    expected = M5036.expected_jobs(config)
    if arguments.dry_run:
        return dry_run_summary(config)
    run_directory = RUNS / config["run_id"]
    config = M5036.load_or_create_config(run_directory, config)
    started = time.monotonic()
    jobs = M5036.load_jobs(run_directory)
    imported = M5037.import_reusable_jobs(run_directory, config, jobs)
    summary = M5037.write_augmented_status(run_directory, config, jobs, "RUNNING", started)
    M5036.append_log(
        run_directory,
        f"invocation start terminal={len(jobs)} expected={len(expected)} imports={imported} max_wall={arguments.max_wall_seconds}",
    )
    new_kernels = 0
    state = "COMPLETE"
    M5036.N5030.chamber_residue_catalog = M5036.MREPAIR.repaired_chamber_residue_catalog
    try:
        for job in execution_order(config, expected):
            if job["job_key"] in jobs:
                continue
            if time.monotonic() - started >= arguments.max_wall_seconds:
                state = "PAUSED_DEADLINE"
                break
            if arguments.max_new_kernels is not None and new_kernels >= arguments.max_new_kernels:
                state = "PAUSED_JOB_LIMIT"
                break
            M5036.append_log(run_directory, f"starting {job['job_key']}")
            result = M5036.execute_new_job(run_directory, config, job)
            jobs[job["job_key"]] = result
            new_kernels += 1
            M5036.append_log(
                run_directory,
                f"finished {job['job_key']} status={result['status']} seconds={result['job_runtime_seconds']:.3f}",
            )
            summary = M5037.write_augmented_status(
                run_directory, config, jobs, "RUNNING", started
            )
            print(
                json.dumps(
                    {
                        "job": job["job_key"],
                        "status": result["status"],
                        "seconds": result["job_runtime_seconds"],
                        "terminal": len(jobs),
                        "expected": len(expected),
                    }
                ),
                flush=True,
            )
    finally:
        M5036.N5030.chamber_residue_catalog = M5036.ORIGINAL_CATALOG
    expected_keys = {row["job_key"] for row in expected}
    if len(set(jobs) & expected_keys) < len(expected_keys) and state == "COMPLETE":
        state = "PAUSED"
    summary = M5037.write_augmented_status(run_directory, config, jobs, state, started)
    if state == "COMPLETE":
        M5036.atomic_text(
            run_directory / "COMPLETE",
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "completed_at": M5036.utc_now(),
                    "failed_jobs": summary["failed_jobs"],
                    "unconverged_jobs": summary["unconverged_jobs"],
                },
                indent=2,
            )
            + "\n",
        )
    else:
        (run_directory / "COMPLETE").unlink(missing_ok=True)
    M5036.append_log(
        run_directory,
        f"invocation stop state={state} terminal={summary['terminal_jobs']} remaining={summary['remaining_jobs']}",
    )
    audit = write_5040_artifacts(config, summary, run_directory)
    return {**summary, "nested_variance_audit": audit}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="nested_sobol_power1_s4_v1")
    parser.add_argument("--physical-cosines", default="-0.6,-0.3,0,0.3,0.6")
    parser.add_argument("--epsilons", default="0.08,0.04,0.02")
    parser.add_argument("--seeds", default="503401,503402,503403,503404")
    parser.add_argument("--power", type=int, default=1)
    parser.add_argument("--topology-steps", type=int, default=96)
    parser.add_argument("--topology-maximum-steps", type=int, default=49152)
    parser.add_argument("--regulator", type=float, default=1.0e-3)
    parser.add_argument("--boundary-tracking-steps", type=int, default=64)
    parser.add_argument("--max-wall-seconds", type=float, default=9000.0)
    parser.add_argument("--max-new-kernels", type=int)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0:
        raise ValueError("max wall seconds must be positive")
    result = run(arguments)
    if result.get("dry_run"):
        console = result
    else:
        audit = result["nested_variance_audit"]
        console = {
            "checkpoint_marker": MARKER,
            "run_state": result["run_state"],
            "expected_jobs": result["expected_jobs"],
            "terminal_jobs": result["terminal_jobs"],
            "remaining_jobs": result["remaining_jobs"],
            "failed_jobs": result["failed_jobs"],
            "unconverged_jobs": result["unconverged_jobs"],
            "sample1_primary_jobs_converged": audit["sample1_primary_jobs_converged"],
            "sample1_audit_jobs_converged": audit["sample1_audit_jobs_converged"],
            "complete_nested_scrambles": audit["complete_nested_scrambles"],
            "equal_cost_design_decision": audit["equal_cost_design_decision"],
            "production_precision_complete": False,
            "valid_for_full_MTS_claim": False,
        }
    print(json.dumps(console, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
