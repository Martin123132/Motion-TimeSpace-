from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5124 = POST / "scripts" / "Y5_R2FR_5124_crossed_hhh_two_stratum_derivation.py"
SOURCE_5124 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5124"
    / "crossed_hhh_two_stratum_derivation.json"
)
PHYSICAL_ROWS_5123 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5123"
    / "physical_replacement_crossed_remainder_rows.csv"
)
RESULT_5123 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5123"
    / "physical_hhh_angular_first_and_crossed_remainder_results.json"
)
DESIGN_LOCK = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5125"
    / "reciprocal_stratified_fresh_pilot_design_lock.json"
)
SOURCE = DESIGN_LOCK.parent
RUNS = SOURCE / "runs"
CONFIG_JSON = SOURCE / "reciprocal_stratified_locked_config.json"
SCHEDULE_JSON = SOURCE / "reciprocal_stratified_locked_schedule.json"
ACTIVATION_JSON = SOURCE / "reciprocal_stratified_activation.json"
DRY_RUN_JSON = SOURCE / "reciprocal_stratified_dry_run.json"
ANALYSIS_JSON = SOURCE / "reciprocal_stratified_fresh_pilot_analysis.json"
EVENT_CSV = SOURCE / "reciprocal_stratified_event_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5125_VALIDATION.csv"
)
DOCUMENT = POST / "5125-Y5-R2FR-reciprocal-stratified-fresh-pilot.md"
V12_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v12"
)
CONTROL_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)

MARKER = "MTS_5125_RECIPROCAL_STRATIFIED_FRESH_PILOT"
REVISION = "fresh-independent-reciprocal-stratified-runner-v1"
RUN_ID = "reciprocal_stratified_fresh_pilot_v1"
CHECKED_DATE = "2026-07-19"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
MAXIMUM_INVOCATION_HOURS = 4.0
PHYSICAL_COSINES = np.asarray((-0.6, -0.3, 0.0, 0.3, 0.6), dtype=float)
LOCAL_SHAPE = 1.0 - PHYSICAL_COSINES**2
LOCAL_WEIGHTS = LOCAL_SHAPE / float(LOCAL_SHAPE @ LOCAL_SHAPE)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module("mts_5077_for_5125", SCRIPT_5077)
M5124 = load_module("mts_5124_for_5125", SCRIPT_5124)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, default=json_default),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, default=json_default) + "\n")


def json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, complex):
        return complex_row(value)
    raise TypeError(type(value).__name__)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def tagged(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint_marker": MARKER,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def validate_wall_cap(hours: float) -> None:
    if not 0.0 < hours <= MAXIMUM_INVOCATION_HOURS:
        raise ValueError(f"wall cap must be in (0,{MAXIMUM_INVOCATION_HOURS}]")


def build_config(lock: dict[str, Any]) -> dict[str, Any]:
    manifest = {
        "fresh_high_scramble_seeds": lock["full_remainder_seeds"],
        "fresh_low_scramble_seeds": lock["reciprocal_topological_seeds"],
        "argument_topology_rule": lock["argument_topology_rule"],
        "epsilon_topology_rule": lock["epsilon_topology_rule"],
        "quadrature_breakpoint_rule": lock["quadrature_breakpoint_rule"],
    }
    config = M5077.make_config(manifest, RUN_ID)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["pilot_manifest"] = relative(DESIGN_LOCK)
    config["pilot_manifest_digest"] = digest(DESIGN_LOCK)
    config["stratified_contract"] = {
        "full_remainder_seeds": lock["full_remainder_seeds"],
        "reciprocal_topological_seeds": lock["reciprocal_topological_seeds"],
        "crossed_base_argument_ids": lock["crossed_base_argument_ids"],
        "epsilon_ids": lock["epsilon_ids"],
        "allocation_ratio": lock["topological_to_full_allocation_ratio"],
        "estimator": lock["estimator"],
        "unsafe_reciprocal_policy": "evaluate both roots fail-closed",
    }
    config["source_files"][str(Path(__file__).resolve())] = digest(
        Path(__file__).resolve()
    )
    config["source_files"][str(SCRIPT_5124)] = digest(SCRIPT_5124)
    config["source_files"][str(DESIGN_LOCK)] = digest(DESIGN_LOCK)
    config["source_files"][str(SOURCE_5124)] = digest(SOURCE_5124)
    config.pop("config_digest", None)
    config["config_digest"] = M5077.M5036.canonical_digest(config)
    return config


def crossed_base_ids(config: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for crossing in config["crossings"]:
        for key in ("t_argument_id", "u_argument_id"):
            argument_id = str(crossing[key])
            if argument_id not in values:
                values.append(argument_id)
    return values


def build_jobs(config: dict[str, Any], lock: dict[str, Any]) -> list[dict[str, Any]]:
    event_lookup = {int(row["seed"]): row for row in config["events"]}
    base_ids = crossed_base_ids(config)
    rows: list[dict[str, Any]] = []
    strata = (
        ("full_remainder", lock["full_remainder_seeds"]),
        ("reciprocal_topological", lock["reciprocal_topological_seeds"]),
    )
    for stratum, seeds in strata:
        for seed_value in seeds:
            event = event_lookup[int(seed_value)]
            for epsilon_id in lock["epsilon_ids"]:
                for base_id in base_ids:
                    rows.append(
                        {
                            "stratum": stratum,
                            "seed": int(seed_value),
                            "event_id": str(event["event_id"]),
                            "epsilon_id": str(epsilon_id),
                            "base_argument_id": base_id,
                            "profile": "primary24",
                            "job_key": f"{epsilon_id}__{event['event_id']}__{base_id}__primary24",
                        }
                    )
    return rows


def prior_seed_locations(selected_seeds: set[int]) -> dict[int, list[str]]:
    locations = {seed_value: [] for seed_value in selected_seeds}
    functional = POST / "source-intake" / "functional_rg"
    for path in functional.rglob("config.json"):
        if SOURCE in path.parents:
            continue
        try:
            document = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        present = {int(value) for value in document.get("seeds", [])}
        present.update(
            int(row["seed"])
            for row in document.get("events", [])
            if "seed" in row
        )
        for seed_value in selected_seeds.intersection(present):
            locations[seed_value].append(relative(path))
    return locations


def projected_speedup(source: dict[str, Any], ratio: float, channel: str) -> float:
    values = source["stratified_design"]["channels"][channel]
    cost_ratio = float(source["benchmark"]["reciprocal_reduced_cost_fraction"])
    sigma_topological = float(values["sigma_topological"])
    sigma_naive = float(values["sigma_naive"])
    sigma_total = float(values["sigma_total"])
    denominator = (1.0 + cost_ratio * ratio) * (
        sigma_naive**2 + sigma_topological**2 / ratio
    )
    return sigma_total**2 / denominator


def validation_rows(checks: list[tuple[str, bool, str]]) -> list[dict[str, Any]]:
    return [
        tagged({"check_id": name, "passed": passed, "detail": detail})
        for name, passed, detail in checks
    ]


def dry_run() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    required = (
        SCRIPT_5077,
        SCRIPT_5124,
        SOURCE_5124,
        PHYSICAL_ROWS_5123,
        RESULT_5123,
        DESIGN_LOCK,
        FORMAL,
        V12_RUN,
        CONTROL_RUN,
    )
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    lock = read_json(DESIGN_LOCK)
    source = read_json(SOURCE_5124)
    config = build_config(lock)
    jobs = build_jobs(config, lock)
    full_seeds = {int(value) for value in lock["full_remainder_seeds"]}
    topological_seeds = {
        int(value) for value in lock["reciprocal_topological_seeds"]
    }
    selected_seeds = full_seeds | topological_seeds
    prior_locations = prior_seed_locations(selected_seeds)
    ratio = len(topological_seeds) / len(full_seeds)
    real_projection = projected_speedup(source, ratio, "real")
    imaginary_projection = projected_speedup(source, ratio, "imaginary")
    full_jobs = [row for row in jobs if row["stratum"] == "full_remainder"]
    topological_jobs = [
        row for row in jobs if row["stratum"] == "reciprocal_topological"
    ]
    checks = [
        ("all_required_paths_exist", not missing, str(len(required))),
        (
            "source_5124_digest_locked",
            digest(SOURCE_5124) == lock["source_checkpoint_sha256"],
            digest(SOURCE_5124),
        ),
        (
            "source_5124_reciprocal_gate_passed",
            int(source["reciprocal_audit"]["safe_pair_failures"]) == 0
            and float(
                source["reciprocal_audit"][
                    "maximum_topological_reconstruction_relative_residual"
                ]
            )
            < 2.0e-6,
            str(source["reciprocal_audit"]["safe_pair_count"]),
        ),
        (
            "fresh_seed_strata_are_disjoint",
            not full_seeds.intersection(topological_seeds)
            and len(selected_seeds) == 28,
            f"{len(full_seeds)}+{len(topological_seeds)}",
        ),
        (
            "fresh_seeds_absent_from_prior_functional_configs",
            not any(prior_locations.values()),
            json.dumps({key: value for key, value in prior_locations.items() if value}),
        ),
        (
            "allocation_locked_at_ratio_six",
            ratio == float(lock["topological_to_full_allocation_ratio"]) == 6.0,
            str(ratio),
        ),
        (
            "locked_ratio_projects_both_channel_gains",
            real_projection > 1.0 and imaginary_projection > 1.0,
            f"real={real_projection};imaginary={imaginary_projection}",
        ),
        (
            "crossed_argument_scope_is_exact",
            set(crossed_base_ids(config)) == set(lock["crossed_base_argument_ids"])
            and len(crossed_base_ids(config)) == 10,
            ",".join(crossed_base_ids(config)),
        ),
        (
            "full_job_scope_is_exact",
            len(full_jobs) == int(lock["expected_full_job_count"]) == 80,
            str(len(full_jobs)),
        ),
        (
            "topological_job_scope_is_exact",
            len(topological_jobs)
            == int(lock["expected_topological_job_count"])
            == 480,
            str(len(topological_jobs)),
        ),
        (
            "total_schedule_unique_and_exact",
            len(jobs) == int(lock["expected_total_job_count"]) == 560
            and len({(row["stratum"], row["job_key"]) for row in jobs}) == 560,
            str(len(jobs)),
        ),
        (
            "only_locked_epsilon_and_primary_profile_used",
            all(
                row["epsilon_id"] in {"E040", "E020"}
                and row["profile"] == "primary24"
                for row in jobs
            ),
            "E040,E020/primary24",
        ),
        (
            "config_digest_is_self_consistent",
            M5077.M5036.source_config_valid(config),
            config["config_digest"],
        ),
        (
            "four_hour_cap_is_locked",
            float(lock["maximum_invocation_wall_hours"])
            == MAXIMUM_INVOCATION_HOURS,
            str(MAXIMUM_INVOCATION_HOURS),
        ),
        (
            "formalization_workbench_unchanged",
            tree_digest(FORMAL) == FORMAL_BASELINE,
            tree_digest(FORMAL),
        ),
        (
            "claim_and_github_actions_remain_disabled",
            not lock["numeric_UV_claim_allowed"]
            and not lock["local_GR_claim_allowed"]
            and not lock["full_MTS_claim_allowed"]
            and not lock["github_action_allowed"],
            "private nonclaim pilot",
        ),
    ]
    execution_authorized = all(passed for _, passed, _ in checks)
    activation = tagged(
        {
            "revision": REVISION,
            "run_id": RUN_ID,
            "config_digest": config["config_digest"],
            "design_lock": relative(DESIGN_LOCK),
            "design_lock_sha256": digest(DESIGN_LOCK),
            "source_5124_sha256": digest(SOURCE_5124),
            "v12_tree_sha256_before_execution": tree_digest(V12_RUN),
            "control_tree_sha256_before_execution": tree_digest(CONTROL_RUN),
            "formal_tree_sha256_before_execution": tree_digest(FORMAL),
            "expected_job_count": len(jobs),
            "projected_speedup_real": real_projection,
            "projected_speedup_imaginary": imaginary_projection,
            "execution_authorized": execution_authorized,
            "default_enabled": False,
        }
    )
    dry = tagged(
        {
            "revision": REVISION,
            "dry_run": True,
            "fresh_execution_started": False,
            "execution_authorized": execution_authorized,
            "expected_full_job_count": len(full_jobs),
            "expected_topological_job_count": len(topological_jobs),
            "expected_total_job_count": len(jobs),
            "fresh_event_count": len(selected_seeds),
            "prior_seed_locations": prior_locations,
            "checks": {name: passed for name, passed, _ in checks},
        }
    )
    atomic_json(CONFIG_JSON, config)
    atomic_json(SCHEDULE_JSON, tagged({"jobs": jobs, "job_count": len(jobs)}))
    atomic_json(ACTIVATION_JSON, activation)
    atomic_json(DRY_RUN_JSON, dry)
    write_csv(VALIDATION_CSV, validation_rows(checks))
    if not execution_authorized:
        failures = [name for name, passed, _ in checks if not passed]
        raise RuntimeError(f"5125 dry-run validation failed: {failures}")
    return activation, config, jobs


def cached_job(path: Path, config_digest: str, stratum: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    row = read_json(path)
    if (
        row.get("config_digest") == config_digest
        and row.get("stratum") == stratum
        and row.get("status") == "COMPLETED_CONVERGED"
        and (
            stratum != "full_remainder"
            or row.get("strict_adaptive_validated") is True
        )
    ):
        return {**row, "resumed_from_cache": True}
    return None


def topological_output_path(run_directory: Path, job: dict[str, Any]) -> Path:
    return run_directory / "topological_jobs" / f"{job['job_key']}.json"


def execute_topological_job(
    run_directory: Path,
    config: dict[str, Any],
    manager: Any,
    job: dict[str, Any],
) -> dict[str, Any]:
    output = topological_output_path(run_directory, job)
    cached = cached_job(output, config["config_digest"], job["stratum"])
    if cached is not None:
        return cached
    event = manager.events[job["event_id"]]
    argument = manager.arguments[f"{job['epsilon_id']}_{job['base_argument_id']}"]
    M5077.CURRENT_EVENT = event
    M5077.CURRENT_ARGUMENT = argument
    started = time.monotonic()
    try:
        topology, topology_path, topology_runtime = manager.obtain(
            job["event_id"], job["epsilon_id"], job["base_argument_id"]
        )
        target = M5077.M5036.complex_from_row(argument["target_cosine"])
        module = M5077.M5036.N5030
        M5077.M5036.M5035.M5034.configure(event, target)
        profile = config["tiers"]["primary24"]
        previous_catalog = module.chamber_residue_catalog
        previous_global_value = module.global_chamber_value
        module.chamber_residue_catalog = M5077.certified_primary_catalog
        M5077.M5036.MREPAIR.CURRENT_JOB = job["job_key"]
        M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
        M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
        M5077.OUTWARD_CONTOUR_AUDIT.clear()
        M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
        M5077.removable_extension_gate()
        removable_extension = M5077.M5085.CertifiedRemovableGlobalExtension(
            previous_global_value
        )
        module.global_chamber_value = removable_extension
        kernel_started = time.monotonic()
        try:
            (
                topological,
                residues_stable,
                selected_catalog_rows,
                safe_pair_count,
                unsafe_pair_count,
            ) = M5124.reciprocal_reduced_topological_value(
                module, topology, profile
            )
        finally:
            module.chamber_residue_catalog = previous_catalog
            module.global_chamber_value = previous_global_value
        kernel_runtime = time.monotonic() - kernel_started
        normalized = M5124.KERNEL_MULTIPLIER * topological
        finite = all(
            math.isfinite(value)
            for value in (
                topological.real,
                topological.imag,
                normalized.real,
                normalized.imag,
            )
        )
        converged = bool(residues_stable and finite)
        result = tagged(
            {
                **job,
                "config_digest": config["config_digest"],
                "status": (
                    "COMPLETED_CONVERGED"
                    if converged
                    else "COMPLETED_UNCONVERGED"
                ),
                "integral_converged": converged,
                "topology_file": str(topology_path),
                "topology_file_sha256": digest(Path(topology_path)),
                "raw_topological_correction": complex_row(topological),
                "normalized_topological_D_hhh_over_G3": complex_row(normalized),
                "residues_stable": bool(residues_stable),
                "selected_catalog_rows": int(selected_catalog_rows),
                "safe_reciprocal_pair_count": int(safe_pair_count),
                "unsafe_fail_closed_pair_count": int(unsafe_pair_count),
                "residue_radius_adjustment_count": len(
                    M5077.M5036.MREPAIR.RADIUS_AUDIT
                ),
                "removable_extension_count": len(removable_extension.calls),
                "topology_runtime_seconds": topology_runtime,
                "kernel_runtime_seconds": kernel_runtime,
                "job_runtime_seconds": time.monotonic() - started,
                "resumed_from_cache": False,
            }
        )
    except Exception as error:
        result = tagged(
            {
                **job,
                "config_digest": config["config_digest"],
                "status": "FAILED",
                "error_type": type(error).__name__,
                "error": str(error),
                "job_runtime_seconds": time.monotonic() - started,
                "resumed_from_cache": False,
            }
        )
    atomic_json(output, result)
    return result


def full_output_path(run_directory: Path, job: dict[str, Any]) -> Path:
    return run_directory / "jobs" / f"{job['job_key']}.json"


def execute_full_job(
    run_directory: Path,
    config: dict[str, Any],
    manager: Any,
    job: dict[str, Any],
) -> dict[str, Any]:
    output = full_output_path(run_directory, job)
    cached = cached_job(output, config["config_digest"], job["stratum"])
    if cached is not None:
        return cached
    row = M5077.execute_kernel(run_directory, config, manager, job)
    row = {**row, "stratum": job["stratum"]}
    atomic_json(output, row)
    return row


def run_counts(
    run_directory: Path, config_digest: str, jobs: list[dict[str, Any]]
) -> dict[str, int]:
    counts = {
        "completed_converged": 0,
        "completed_unconverged": 0,
        "failed": 0,
        "missing": 0,
    }
    for job in jobs:
        path = (
            full_output_path(run_directory, job)
            if job["stratum"] == "full_remainder"
            else topological_output_path(run_directory, job)
        )
        if not path.exists():
            counts["missing"] += 1
            continue
        row = read_json(path)
        if row.get("config_digest") != config_digest:
            counts["missing"] += 1
        elif row.get("status") == "COMPLETED_CONVERGED":
            counts["completed_converged"] += 1
        elif row.get("status") == "COMPLETED_UNCONVERGED":
            counts["completed_unconverged"] += 1
        elif row.get("status") == "FAILED":
            counts["failed"] += 1
        else:
            counts["missing"] += 1
    return counts


def event_runtime(
    run_directory: Path,
    config_digest: str,
    jobs: list[dict[str, Any]],
    stratum: str,
    seed_value: int,
) -> float:
    total = 0.0
    for job in jobs:
        if job["stratum"] != stratum or int(job["seed"]) != seed_value:
            continue
        path = (
            full_output_path(run_directory, job)
            if stratum == "full_remainder"
            else topological_output_path(run_directory, job)
        )
        row = read_json(path)
        if row.get("config_digest") != config_digest:
            raise RuntimeError(f"runtime row digest mismatch: {path}")
        total += float(row["job_runtime_seconds"])
    return total


def normalized_topological_value(path: Path) -> complex:
    row = read_json(path)["normalized_topological_D_hhh_over_G3"]
    return complex(float(row["real"]), float(row["imaginary"]))


def event_components(
    run_directory: Path,
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    stratum: str,
    seed_value: int,
) -> dict[str, Any]:
    crossings = sorted(
        config["crossings"],
        key=lambda row: float(row["physical_s_channel_cosine"]),
    )
    components = (
        ("naive", "topological", "total")
        if stratum == "full_remainder"
        else ("topological",)
    )
    epsilon_vectors: dict[str, dict[str, np.ndarray]] = {}
    maximum_closure = 0.0
    for epsilon_id in ("E040", "E020"):
        values = {component: [] for component in components}
        for crossing in crossings:
            channel_values: dict[str, dict[str, complex]] = {}
            for channel, argument_key in (
                ("t", "t_argument_id"),
                ("u", "u_argument_id"),
            ):
                base_id = str(crossing[argument_key])
                event_id = next(
                    row["event_id"]
                    for row in jobs
                    if row["stratum"] == stratum
                    and int(row["seed"]) == seed_value
                )
                job_key = f"{epsilon_id}__{event_id}__{base_id}__primary24"
                if stratum == "full_remainder":
                    kernel_path = run_directory / "kernels" / f"{job_key}.json"
                    split, closure = M5124.split_kernel(kernel_path)
                    maximum_closure = max(maximum_closure, closure)
                    channel_values[channel] = split
                else:
                    output = run_directory / "topological_jobs" / f"{job_key}.json"
                    channel_values[channel] = {
                        "topological": normalized_topological_value(output)
                    }
            for component in components:
                values[component].append(
                    float(crossing["t_ratio"]) ** 3
                    * channel_values["t"][component]
                    + float(crossing["u_ratio"]) ** 3
                    * channel_values["u"][component]
                )
        epsilon_vectors[epsilon_id] = {
            component: np.asarray(rows, dtype=np.complex128)
            for component, rows in values.items()
        }
    extrapolated = {
        component: 2.0 * epsilon_vectors["E020"][component]
        - epsilon_vectors["E040"][component]
        for component in components
    }
    local = {
        component: complex(vector @ LOCAL_WEIGHTS)
        for component, vector in extrapolated.items()
    }
    if stratum == "full_remainder":
        maximum_closure = max(
            maximum_closure,
            abs(local["naive"] + local["topological"] - local["total"]),
            float(
                np.max(
                    np.abs(
                        extrapolated["naive"]
                        + extrapolated["topological"]
                        - extrapolated["total"]
                    )
                )
            ),
        )
    return {
        "local": local,
        "vectors": extrapolated,
        "maximum_closure": maximum_closure,
        "runtime_seconds": event_runtime(
            run_directory, config["config_digest"], jobs, stratum, seed_value
        ),
    }


def sample_variance(values: np.ndarray, channel: str) -> float:
    selected = values.real if channel == "real" else values.imag
    return float(np.var(selected, ddof=1))


def channel_analysis(
    full_naive: np.ndarray,
    full_topological: np.ndarray,
    full_total: np.ndarray,
    independent_topological: np.ndarray,
    mean_full_cost: float,
    mean_topological_cost: float,
    channel: str,
) -> dict[str, Any]:
    full_count = len(full_naive)
    topological_count = len(independent_topological)
    naive_variance = sample_variance(full_naive, channel)
    topological_variance = sample_variance(independent_topological, channel)
    full_topological_variance = sample_variance(full_topological, channel)
    total_variance = sample_variance(full_total, channel)
    naive_values = full_naive.real if channel == "real" else full_naive.imag
    topological_values = (
        independent_topological.real
        if channel == "real"
        else independent_topological.imag
    )
    full_topological_values = (
        full_topological.real if channel == "real" else full_topological.imag
    )
    total_values = full_total.real if channel == "real" else full_total.imag
    estimate = float(np.mean(naive_values) + np.mean(topological_values))
    stratified_variance = (
        naive_variance / full_count + topological_variance / topological_count
    )
    total_cost = (
        full_count * mean_full_cost + topological_count * mean_topological_cost
    )
    equivalent_full_count = total_cost / mean_full_cost
    paired_equal_cost_variance = total_variance / equivalent_full_count
    topological_difference = float(
        np.mean(topological_values) - np.mean(full_topological_values)
    )
    topological_difference_variance = (
        topological_variance / topological_count
        + full_topological_variance / full_count
    )
    return {
        "stratified_estimate": estimate,
        "stratified_standard_error": math.sqrt(max(stratified_variance, 0.0)),
        "paired_full_seed_mean": float(np.mean(total_values)),
        "paired_full_seed_standard_error": math.sqrt(total_variance / full_count),
        "naive_sample_standard_deviation": math.sqrt(naive_variance),
        "independent_topological_sample_standard_deviation": math.sqrt(
            topological_variance
        ),
        "paired_total_sample_standard_deviation": math.sqrt(total_variance),
        "mean_topological_bank_difference": topological_difference,
        "topological_bank_difference_z": (
            abs(topological_difference)
            / math.sqrt(max(topological_difference_variance, 1.0e-300))
        ),
        "mean_full_event_cost_seconds": mean_full_cost,
        "mean_topological_event_cost_seconds": mean_topological_cost,
        "topological_to_full_cost_ratio": mean_topological_cost / mean_full_cost,
        "pilot_total_recorded_cost_seconds": total_cost,
        "equivalent_paired_full_event_count": equivalent_full_count,
        "paired_equal_cost_standard_error": math.sqrt(
            max(paired_equal_cost_variance, 0.0)
        ),
        "realized_cost_normalized_speedup": (
            paired_equal_cost_variance / stratified_variance
            if stratified_variance > 0.0
            else 0.0
        ),
    }


def physical_contract() -> dict[str, Any]:
    rows = [
        row
        for row in read_csv(PHYSICAL_ROWS_5123)
        if row["row_type"] == "summary"
    ]
    rows.sort(key=lambda row: float(row["physical_cosine"]))
    values = np.asarray(
        [float(row["physical_angular_first_mean_real"]) for row in rows],
        dtype=float,
    )
    required_nonlocal = np.asarray(
        [float(row["required_hhh_nonlocal"]) for row in rows], dtype=float
    )
    coefficient_row = next(
        row
        for row in read_csv(PHYSICAL_ROWS_5123)
        if row["row_type"] == "coefficient"
    )
    result = read_json(RESULT_5123)
    return {
        "vector": values,
        "required_nonlocal": required_nonlocal,
        "local_coefficient": float(values @ LOCAL_WEIGHTS),
        "local_standard_error": float(
            result["hybrid"]["physical_a_standard_error"]
        ),
        "known_master_without_hhh": float(
            coefficient_row["known_master_local_coefficient_without_hhh"]
        ),
    }


def analyze(
    activation: dict[str, Any], config: dict[str, Any], jobs: list[dict[str, Any]]
) -> dict[str, Any]:
    run_directory = RUNS / RUN_ID
    counts = run_counts(run_directory, config["config_digest"], jobs)
    if counts["completed_converged"] != len(jobs):
        raise RuntimeError(f"cannot analyze incomplete 5125 run: {counts}")
    lock = read_json(DESIGN_LOCK)
    full_seeds = [int(value) for value in lock["full_remainder_seeds"]]
    topological_seeds = [
        int(value) for value in lock["reciprocal_topological_seeds"]
    ]
    full_events = {
        seed_value: event_components(
            run_directory, config, jobs, "full_remainder", seed_value
        )
        for seed_value in full_seeds
    }
    topological_events = {
        seed_value: event_components(
            run_directory, config, jobs, "reciprocal_topological", seed_value
        )
        for seed_value in topological_seeds
    }
    full_naive = np.asarray(
        [full_events[seed_value]["local"]["naive"] for seed_value in full_seeds]
    )
    full_topological = np.asarray(
        [
            full_events[seed_value]["local"]["topological"]
            for seed_value in full_seeds
        ]
    )
    full_total = np.asarray(
        [full_events[seed_value]["local"]["total"] for seed_value in full_seeds]
    )
    independent_topological = np.asarray(
        [
            topological_events[seed_value]["local"]["topological"]
            for seed_value in topological_seeds
        ]
    )
    mean_full_cost = float(
        np.mean([full_events[seed_value]["runtime_seconds"] for seed_value in full_seeds])
    )
    mean_topological_cost = float(
        np.mean(
            [
                topological_events[seed_value]["runtime_seconds"]
                for seed_value in topological_seeds
            ]
        )
    )
    channels = {
        channel: channel_analysis(
            full_naive,
            full_topological,
            full_total,
            independent_topological,
            mean_full_cost,
            mean_topological_cost,
            channel,
        )
        for channel in ("real", "imaginary")
    }
    full_naive_vectors = np.asarray(
        [full_events[seed_value]["vectors"]["naive"] for seed_value in full_seeds]
    )
    topological_vectors = np.asarray(
        [
            topological_events[seed_value]["vectors"]["topological"]
            for seed_value in topological_seeds
        ]
    )
    crossed_mean_vector = np.mean(full_naive_vectors, axis=0) + np.mean(
        topological_vectors, axis=0
    )
    physical = physical_contract()
    hybrid_vector = crossed_mean_vector + physical["vector"]
    hybrid_local = complex(hybrid_vector @ LOCAL_WEIGHTS)
    hybrid_nonlocal = hybrid_vector - hybrid_local * LOCAL_SHAPE
    crossed_real_covariance = (
        np.cov(full_naive_vectors.real, rowvar=False, ddof=1) / len(full_seeds)
        + np.cov(topological_vectors.real, rowvar=False, ddof=1)
        / len(topological_seeds)
    )
    crossed_imaginary_covariance = (
        np.cov(full_naive_vectors.imag, rowvar=False, ddof=1) / len(full_seeds)
        + np.cov(topological_vectors.imag, rowvar=False, ddof=1)
        / len(topological_seeds)
    )
    local_real_error = math.sqrt(
        max(float(LOCAL_WEIGHTS @ crossed_real_covariance @ LOCAL_WEIGHTS), 0.0)
        + physical["local_standard_error"] ** 2
    )
    local_imaginary_error = math.sqrt(
        max(
            float(LOCAL_WEIGHTS @ crossed_imaginary_covariance @ LOCAL_WEIGHTS),
            0.0,
        )
    )
    known_master = float(physical["known_master_without_hhh"])
    candidate_master = complex(known_master, 0.0) + 2.0 * hybrid_local
    candidate_k_mu = -4.0 * candidate_master
    maximum_closure = max(
        [full_events[seed_value]["maximum_closure"] for seed_value in full_seeds]
        + [
            topological_events[seed_value]["maximum_closure"]
            for seed_value in topological_seeds
        ]
    )
    event_rows: list[dict[str, Any]] = []
    for stratum, seeds, event_map in (
        ("full_remainder", full_seeds, full_events),
        ("reciprocal_topological", topological_seeds, topological_events),
    ):
        for seed_value in seeds:
            event = event_map[seed_value]
            row: dict[str, Any] = {
                "stratum": stratum,
                "seed": seed_value,
                "runtime_seconds": event["runtime_seconds"],
                "maximum_closure": event["maximum_closure"],
            }
            for component, value in event["local"].items():
                row[f"{component}_local_real"] = value.real
                row[f"{component}_local_imaginary"] = value.imag
            event_rows.append(tagged(row))
    write_csv(EVENT_CSV, event_rows)
    result = tagged(
        {
            "revision": REVISION,
            "run_id": RUN_ID,
            "config_digest": config["config_digest"],
            "run_complete": True,
            "counts": counts,
            "full_event_count": len(full_seeds),
            "topological_event_count": len(topological_seeds),
            "allocation_ratio": len(topological_seeds) / len(full_seeds),
            "channels": channels,
            "maximum_component_closure": maximum_closure,
            "crossed_stratified_mean_vector": [complex_row(value) for value in crossed_mean_vector],
            "physical_controlled_vector": physical["vector"].tolist(),
            "hybrid_hhh_vector": [complex_row(value) for value in hybrid_vector],
            "hybrid_a_hhh": {
                **complex_row(hybrid_local),
                "real_standard_error": local_real_error,
                "imaginary_standard_error": local_imaginary_error,
            },
            "hybrid_nonlocal_vector": [complex_row(value) for value in hybrid_nonlocal],
            "required_hhh_nonlocal_real": physical["required_nonlocal"].tolist(),
            "candidate_full_master_local_coefficient": complex_row(candidate_master),
            "candidate_K_mu": {
                **complex_row(candidate_k_mu),
                "real_standard_error": 8.0 * local_real_error,
                "imaginary_standard_error": 8.0 * local_imaginary_error,
            },
            "efficiency_pass_real": channels["real"][
                "realized_cost_normalized_speedup"
            ]
            > 1.0,
            "efficiency_pass_imaginary": channels["imaginary"][
                "realized_cost_normalized_speedup"
            ]
            > 1.0,
            "independent_efficiency_result": True,
            "numeric_UV_coefficient_complete": False,
            "reason_numeric_UV_remains_nonclaim": "four full events make this a fresh efficiency pilot, not a production coefficient determination",
            "governing_cog_condition": "preserve local GR/Newton while deriving galactic activation from the same parent mechanism",
            "protected_v12_unchanged": tree_digest(V12_RUN)
            == activation["v12_tree_sha256_before_execution"],
            "protected_control_unchanged": tree_digest(CONTROL_RUN)
            == activation["control_tree_sha256_before_execution"],
            "formalization_unchanged": tree_digest(FORMAL) == FORMAL_BASELINE,
        }
    )
    atomic_json(ANALYSIS_JSON, result)
    checks = [
        ("all_560_jobs_completed_converged", counts["completed_converged"] == 560, str(counts)),
        ("no_failed_or_unconverged_jobs", counts["failed"] == 0 and counts["completed_unconverged"] == 0, str(counts)),
        ("event_matrix_has_4_plus_24_rows", len(event_rows) == 28, str(len(event_rows))),
        ("exact_component_decomposition_closes", maximum_closure < 1.0e-7, str(maximum_closure)),
        ("all_channel_statistics_finite", all(math.isfinite(float(value)) for channel in channels.values() for value in channel.values()), "real and imaginary"),
        ("efficiency_outcome_recorded_without_forcing_pass", all("realized_cost_normalized_speedup" in channels[channel] for channel in channels), f"real={channels['real']['realized_cost_normalized_speedup']};imaginary={channels['imaginary']['realized_cost_normalized_speedup']}"),
        ("numeric_UV_result_remains_nonclaim", not result["numeric_UV_coefficient_complete"] and not result["valid_for_numeric_UV_claim"], result["reason_numeric_UV_remains_nonclaim"]),
        ("protected_v12_unchanged", result["protected_v12_unchanged"], tree_digest(V12_RUN)),
        ("protected_control_unchanged", result["protected_control_unchanged"], tree_digest(CONTROL_RUN)),
        ("formalization_workbench_unchanged", result["formalization_unchanged"], tree_digest(FORMAL)),
    ]
    write_csv(VALIDATION_CSV, validation_rows(checks))
    if not all(passed for _, passed, _ in checks):
        failures = [name for name, passed, _ in checks if not passed]
        raise RuntimeError(f"5125 completed-run validation failed: {failures}")
    write_document(result)
    return result


def write_document(result: dict[str, Any]) -> None:
    real = result["channels"]["real"]
    imaginary = result["channels"]["imaginary"]
    text = f"""# 5125 - reciprocal-stratified fresh pilot

## Locked calculation

The seeds, ratio-six allocation, 560-job scope, estimator, stopping rule and
efficiency criterion were locked before any fresh event was evaluated. Four
fresh events evaluate the complete gate and retain the exactly paired
`naive=pole_model+smooth` remainder. Twenty-four disjoint fresh events
evaluate only the reciprocal-reduced topological term. Unsafe reciprocal
families still evaluate both roots.

## Fresh result

All 560 jobs converge. The measured topological/full event cost ratio is
`{real['topological_to_full_cost_ratio']:.6g}`. At equal recorded cost, the
realized stratified speedups are `{real['realized_cost_normalized_speedup']:.6g}`
real and `{imaginary['realized_cost_normalized_speedup']:.6g}` imaginary.
The efficiency route is therefore classified independently rather than
rescued by changing seeds or allocation.

The fresh stratified crossed coefficient gives the provisional combined
`a_hhh = {result['hybrid_a_hhh']['real']:.9g} +
{result['hybrid_a_hhh']['imaginary']:.9g} i`, with standard errors
`{result['hybrid_a_hhh']['real_standard_error']:.6g}` and
`{result['hybrid_a_hhh']['imaginary_standard_error']:.6g}`. The corresponding
nonclaim `K_mu` smoke value is
`{result['candidate_K_mu']['real']:.9g} +
{result['candidate_K_mu']['imaginary']:.9g} i`.

## Claim discipline

This is an independent efficiency pilot, not a production UV coefficient:
only four expensive remainder events determine its limiting variance. It
does not establish source coupling, local GR/Newton, Maxwell, galaxies or
full MTS. No field equation or empirical target was fitted.

The governing cog condition remains unchanged: one parent theory must keep
the tested local GR/Newton cogs turning while deriving any galactic-scale
activation without a manual switch.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def execute(
    activation: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    wall_cap_hours: float,
    maximum_new_jobs: int,
) -> dict[str, Any]:
    if not activation["execution_authorized"]:
        raise RuntimeError("5125 dry-run did not authorize execution")
    validate_wall_cap(wall_cap_hours)
    run_directory = RUNS / RUN_ID
    run_directory.mkdir(parents=True, exist_ok=True)
    run_config = run_directory / "config.json"
    if run_config.exists():
        existing = read_json(run_config)
        if existing.get("config_digest") != config["config_digest"]:
            raise RuntimeError("5125 run config changed; use no alternate run id")
    else:
        atomic_json(run_config, config)
    atomic_json(run_directory / "activation.json", activation)
    M5077.install_history_invariant_breakpoints(M5077.M5036.N5030)
    manager = M5077.CentralTopologyManager(run_directory, config)
    started = time.monotonic()
    newly_executed = 0
    resumed = 0
    state = "RUNNING"
    last_job_key: str | None = None
    blocking_job: dict[str, Any] | None = None
    for schedule_index, job in enumerate(jobs, start=1):
        if (time.monotonic() - started) / 3600.0 >= wall_cap_hours:
            state = "PAUSED_WALL_CAP"
            break
        row = (
            execute_full_job(run_directory, config, manager, job)
            if job["stratum"] == "full_remainder"
            else execute_topological_job(run_directory, config, manager, job)
        )
        last_job_key = job["job_key"]
        if row.get("resumed_from_cache"):
            resumed += 1
        else:
            newly_executed += 1
        log_row = tagged(
            {
                "schedule_index": schedule_index,
                "expected_job_count": len(jobs),
                "stratum": job["stratum"],
                "job_key": job["job_key"],
                "status": row["status"],
                "resumed_from_cache": bool(row.get("resumed_from_cache")),
                "recorded_job_runtime_seconds": float(row["job_runtime_seconds"]),
                "invocation_elapsed_seconds": time.monotonic() - started,
            }
        )
        append_jsonl(run_directory / "log.jsonl", log_row)
        atomic_json(
            run_directory / "status.json",
            tagged(
                {
                    **log_row,
                    "revision": REVISION,
                    "run_id": RUN_ID,
                    "state": "RUNNING",
                    "newly_executed_this_invocation": newly_executed,
                    "resumed_this_invocation": resumed,
                }
            ),
        )
        print(json.dumps(log_row), flush=True)
        if row["status"] != "COMPLETED_CONVERGED":
            state = "BLOCKED_JOB_FAILURE"
            blocking_job = row
            break
        if maximum_new_jobs > 0 and newly_executed >= maximum_new_jobs:
            state = "PAUSED_JOB_CAP"
            break
    counts = run_counts(run_directory, config["config_digest"], jobs)
    if counts["completed_converged"] == len(jobs):
        state = "COMPLETE"
    if tree_digest(V12_RUN) != activation["v12_tree_sha256_before_execution"]:
        raise RuntimeError("protected v12 run changed during 5125")
    if tree_digest(CONTROL_RUN) != activation["control_tree_sha256_before_execution"]:
        raise RuntimeError("protected control run changed during 5125")
    if tree_digest(FORMAL) != FORMAL_BASELINE:
        raise RuntimeError("formalization-workbench changed during 5125")
    status = tagged(
        {
            "revision": REVISION,
            "run_id": RUN_ID,
            "state": state,
            "expected_job_count": len(jobs),
            "newly_executed_this_invocation": newly_executed,
            "resumed_this_invocation": resumed,
            "last_job_key": last_job_key,
            "blocking_job": blocking_job,
            "invocation_elapsed_seconds": time.monotonic() - started,
            "wall_cap_hours": wall_cap_hours,
            "maximum_new_jobs": maximum_new_jobs,
            **counts,
        }
    )
    atomic_json(run_directory / "status.json", status)
    if state == "COMPLETE":
        result = analyze(activation, config, jobs)
        atomic_json(run_directory / "COMPLETED.json", {**status, "analysis": result})
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "analyze"), default="dry-run"
    )
    parser.add_argument("--wall-cap-hours", type=float, default=4.0)
    parser.add_argument("--maximum-new-jobs", type=int, default=0)
    arguments = parser.parse_args()
    activation, config, jobs = dry_run()
    if arguments.mode == "dry-run":
        result: dict[str, Any] = read_json(DRY_RUN_JSON)
    elif arguments.mode == "run":
        result = execute(
            activation,
            config,
            jobs,
            arguments.wall_cap_hours,
            arguments.maximum_new_jobs,
        )
    else:
        result = analyze(activation, config, jobs)
    print(json.dumps(result, indent=2, default=json_default))


if __name__ == "__main__":
    main()
