from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5215"
RUNS = SOURCE / "runs"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5212 = (
    POST
    / "scripts"
    / "Y5_R2FR_5212_fresh_crossed_hhh_two_stratum_pilot.py"
)
SCRIPT_5214 = (
    POST
    / "scripts"
    / "Y5_R2FR_5214_A00_source_pole_control_variate.py"
)
AUDIT_5214 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5214"
    / "A00_source_pole_family_audit.json"
)
GATE_5213 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5213"
    / "source_separated_additive_cluster_cauchy_zero.json"
)
SOURCE_CONFIG_5212 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5212"
    / "runs"
    / "fresh_two_stratum_pilot_v2"
    / "config.json"
)

MANIFEST = SOURCE / "frozen_A00_control_pilot_manifest.json"
FROZEN_CONFIG = SOURCE / "frozen_A00_control_pilot_config.json"
FROZEN_SCHEDULE = SOURCE / "frozen_A00_control_pilot_schedule.csv"
PROTOCOL_LOCK = SOURCE / "frozen_A00_control_pilot_lock.json"
ACTIVATION_JSON = SOURCE / "fresh_A00_control_pilot_activation.json"
EVENT_ROWS_CSV = SOURCE / "fresh_A00_control_pilot_event_rows.csv"
PAIR_ROWS_CSV = SOURCE / "fresh_A00_control_pilot_pair_rows.csv"
RESULT_JSON = SOURCE / "fresh_A00_control_pilot_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = (
    POST
    / "5215-Y5-R2FR-fresh-A00-identical-graviton-permutation-control-pilot.md"
)
VALIDATION_CSV = (
    RESIDUALS / "P8_Y5_BRR545_5215_VALIDATION.csv"
)

MARKER = "MTS_5215_FRESH_A00_PERMUTATION_CONTROL_PILOT"
REVISION = "fresh-a00-permutation-control-pilot-v1"
MAXIMUM_WALL_HOURS = 4.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5214 = load_module(SCRIPT_5214, "mts_5214_for_5215")
M5212 = M5214.M5212


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(
        item for item in path.rglob("*") if item.is_file()
    ):
        value.update(
            candidate.relative_to(path).as_posix().encode("utf-8")
        )
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    return M5212.M5077.M5036.canonical_digest(value)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def row_complex(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(value, sort_keys=True, allow_nan=False) + "\n"
        )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        atomic_text(path, "")
        return
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def make_config(
    manifest: dict[str, Any], run_id: str
) -> dict[str, Any]:
    config = M5212.make_config(manifest, run_id)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["pilot_manifest"] = str(MANIFEST)
    config["pilot_manifest_digest"] = digest(MANIFEST)
    config["fresh_A00_control_contract"] = {
        "control_identity": manifest["control_identity"],
        "dominant_family_signature": manifest[
            "dominant_family_signature"
        ],
        "permuted_family_signature": manifest[
            "permuted_family_signature"
        ],
        "partition_ratio": manifest["partition_ratio"],
        "real_control_coefficient": manifest[
            "real_control_coefficient"
        ],
        "imaginary_control_coefficient": manifest[
            "imaginary_control_coefficient"
        ],
        "control_application": manifest["control_application"],
        "acceptance_thresholds": manifest["acceptance_thresholds"],
        "diagnostic_only": manifest["diagnostic_only"],
        "scale_decision": manifest["scale_decision"],
    }
    config["two_stratum_contract"]["full_seeds"] = []
    config["two_stratum_contract"]["topological_seeds"] = list(
        manifest["fresh_topological_scramble_seeds"]
    )
    config["two_stratum_contract"]["required_base_argument_ids"] = [
        "A00"
    ]
    config["two_stratum_contract"]["epsilon_ids"] = list(
        manifest["epsilon_ids"]
    )
    config["two_stratum_contract"]["pilot_only"] = True
    config["source_files"][str(Path(__file__).resolve())] = digest(
        Path(__file__).resolve()
    )
    config["source_files"][str(SCRIPT_5212)] = digest(SCRIPT_5212)
    config["source_files"][str(SCRIPT_5214)] = digest(SCRIPT_5214)
    config["source_files"][str(AUDIT_5214)] = digest(AUDIT_5214)
    config["source_files"][str(GATE_5213)] = digest(GATE_5213)
    config["source_files"][str(SOURCE_CONFIG_5212)] = digest(
        SOURCE_CONFIG_5212
    )
    config.pop("config_digest", None)
    config["config_digest"] = canonical_digest(config)
    return config


def build_schedule(
    config: dict[str, Any], manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    jobs = M5212.build_schedule(config, manifest)
    if not all(
        job["stratum"] == "topological"
        and job["base_argument_id"] == "A00"
        and job["profile"] == "primary24"
        for job in jobs
    ):
        raise RuntimeError("5215 schedule escaped its A00 topological scope")
    return jobs


def prior_seed_occurrences(
    seeds: tuple[int, ...],
) -> list[dict[str, Any]]:
    functional = POST / "source-intake" / "functional_rg"
    candidates = {
        *functional.rglob("config.json"),
        *functional.rglob("*manifest*.json"),
        *functional.rglob("*activation*.json"),
    }
    source_resolved = SOURCE.resolve()
    expression = re.compile(
        r"(?<![0-9])(?:"
        + "|".join(str(seed) for seed in seeds)
        + r")(?![0-9])"
    )
    rows: list[dict[str, Any]] = []
    for candidate in sorted(candidates):
        try:
            candidate.resolve().relative_to(source_resolved)
            continue
        except ValueError:
            pass
        text = candidate.read_text(encoding="utf-8", errors="ignore")
        matches = sorted({int(value) for value in expression.findall(text)})
        if matches:
            rows.append(
                {
                    "path": relative(candidate),
                    "seeds": matches,
                }
            )
    return rows


def locked_source_rows(
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for declaration in manifest["locked_sources"]:
        path = POST / declaration["path"]
        actual = digest(path) if path.is_file() else ""
        rows.append(
            {
                "path": str(path),
                "exists": path.is_file(),
                "expected_sha256": declaration["sha256"],
                "actual_sha256": actual,
                "matches": (
                    path.is_file() and actual == declaration["sha256"]
                ),
            }
        )
    return rows


def activation_record(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    seeds = tuple(
        int(value)
        for value in manifest["fresh_topological_scramble_seeds"]
    )
    source_rows = locked_source_rows(manifest)
    audit = read_json(AUDIT_5214)
    prior_occurrences = prior_seed_occurrences(seeds)
    thresholds = manifest["acceptance_thresholds"]
    config_events = {
        int(event["seed"]) for event in config["events"]
    }
    schedule_seeds = {int(job["seed"]) for job in jobs}
    prerequisites = {
        "all_locked_sources_match": all(
            row["matches"] for row in source_rows
        ),
        "checkpoint_5214_passed": bool(audit["passed"]),
        "checkpoint_5214_authorized_fresh_pilot": bool(
            audit["fresh_independent_control_pilot_authorized"]
        ),
        "control_identity_matches_5214": (
            manifest["control_identity"]
            == audit["permutation_control"]["identity"]
        ),
        "dominant_signature_matches_5214": (
            manifest["dominant_family_signature"]
            == M5214.DOMINANT_FAMILY_SIGNATURE
        ),
        "permuted_signature_matches_5214": (
            manifest["permuted_family_signature"]
            == M5214.PERMUTED_FAMILY_SIGNATURE
        ),
        "coefficient_is_fixed_not_fitted": (
            float(manifest["real_control_coefficient"]) == 1.0
            and float(manifest["imaginary_control_coefficient"]) == 0.0
        ),
        "retrospective_thresholds_are_retained": (
            float(
                thresholds[
                    "maximum_absolute_control_mean_standard_errors"
                ]
            )
            == 2.0
            and float(
                thresholds[
                    "maximum_A00_real_standard_deviation_ratio"
                ]
            )
            == 0.5
            and not bool(
                thresholds["threshold_retuning_after_outcomes_allowed"]
            )
        ),
        "fresh_seeds_are_unique": len(set(seeds)) == len(seeds),
        "fresh_seeds_absent_from_prior_protocols": not prior_occurrences,
        "config_contains_exact_fresh_seed_set": config_events == set(seeds),
        "schedule_contains_exact_fresh_seed_set": schedule_seeds == set(
            seeds
        ),
        "schedule_has_exactly_24_jobs": (
            len(jobs)
            == int(manifest["expected_job_count"])
            == 24
        ),
        "schedule_is_A00_topological_only": all(
            job["stratum"] == "topological"
            and job["base_argument_id"] == "A00"
            and job["epsilon_id"] in {"E020", "E040"}
            for job in jobs
        ),
        "allocation_locked_before_outcomes": bool(
            manifest["allocation_locked_before_fresh_outcomes"]
        ),
        "wall_cap_is_four_hours": math.isclose(
            float(manifest["maximum_wall_hours_per_invocation"]),
            MAXIMUM_WALL_HOURS,
        ),
        "formalization_workbench_unchanged": (
            tree_digest(FORMAL)
            == manifest["formalization_workbench_tree_sha256"]
        ),
        "pilot_is_nonclaim": (
            bool(manifest["pilot_only"])
            and not bool(manifest["valid_for_numeric_UV_claim"])
            and not bool(manifest["valid_for_local_GR_claim"])
            and not bool(manifest["valid_for_full_MTS_claim"])
        ),
    }
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "manifest": relative(MANIFEST),
        "manifest_sha256": digest(MANIFEST),
        "runner_sha256": digest(Path(__file__).resolve()),
        "config_digest": config["config_digest"],
        "schedule_digest": canonical_digest(jobs),
        "expected_job_count": len(jobs),
        "fresh_seeds": list(seeds),
        "locked_source_rows": source_rows,
        "prior_seed_occurrences": prior_occurrences,
        "prerequisites": prerequisites,
        "execution_authorized": all(prerequisites.values()),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def protocol_contract(
    activation: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "manifest_sha256": activation["manifest_sha256"],
        "runner_sha256": activation["runner_sha256"],
        "config_digest": config["config_digest"],
        "schedule_digest": canonical_digest(jobs),
        "locked_source_digests": {
            row["path"]: row["actual_sha256"]
            for row in activation["locked_source_rows"]
        },
        "acceptance_thresholds": config[
            "fresh_A00_control_contract"
        ]["acceptance_thresholds"],
        "control_identity": config["fresh_A00_control_contract"][
            "control_identity"
        ],
    }


def lock_protocol(
    activation: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    contract = protocol_contract(activation, config, jobs)
    if PROTOCOL_LOCK.exists():
        locked = read_json(PROTOCOL_LOCK)
        if locked["contract"] != contract:
            raise RuntimeError(
                "checkpoint-5215 protocol changed after its lock"
            )
        if digest(FROZEN_CONFIG) != locked["frozen_config_sha256"]:
            raise RuntimeError("frozen 5215 config file changed")
        if digest(FROZEN_SCHEDULE) != locked["frozen_schedule_sha256"]:
            raise RuntimeError("frozen 5215 schedule file changed")
        return locked

    atomic_json(FROZEN_CONFIG, config)
    write_csv(FROZEN_SCHEDULE, jobs)
    locked = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "contract": contract,
        "frozen_config": relative(FROZEN_CONFIG),
        "frozen_config_sha256": digest(FROZEN_CONFIG),
        "frozen_schedule": relative(FROZEN_SCHEDULE),
        "frozen_schedule_sha256": digest(FROZEN_SCHEDULE),
        "outcomes_present_at_lock": False,
        "threshold_retuning_allowed": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(PROTOCOL_LOCK, locked)
    return locked


def output_path(
    run_directory: Path, job: dict[str, Any]
) -> Path:
    return (
        run_directory
        / "topological-jobs"
        / f"{job['job_key']}.json"
    )


def cached_result(
    run_directory: Path,
    config: dict[str, Any],
    job: dict[str, Any],
) -> dict[str, Any] | None:
    path = output_path(run_directory, job)
    if not path.exists():
        return None
    row = read_json(path)
    if (
        row.get("config_digest") == config["config_digest"]
        and row.get("status") == "COMPLETED_CONVERGED"
    ):
        return {**row, "resumed_from_cache": True}
    return None


def execute_job(
    run_directory: Path,
    config: dict[str, Any],
    manager: Any,
    job: dict[str, Any],
) -> dict[str, Any]:
    cached = cached_result(run_directory, config, job)
    if cached is not None:
        return cached

    output = output_path(run_directory, job)
    event = manager.events[job["event_id"]]
    argument = manager.arguments[
        f"{job['epsilon_id']}_{job['base_argument_id']}"
    ]
    started = time.monotonic()
    previous_event = M5212.M5077.CURRENT_EVENT
    previous_argument = M5212.M5077.CURRENT_ARGUMENT
    try:
        topology, topology_path, topology_runtime = manager.obtain(
            job["event_id"],
            job["epsilon_id"],
            job["base_argument_id"],
        )
        target = M5212.M5077.M5036.complex_from_row(
            argument["target_cosine"]
        )
        M5212.M5077.CURRENT_EVENT = event
        M5212.M5077.CURRENT_ARGUMENT = argument
        module = M5212.M5077.M5036.N5030
        M5212.M5077.M5036.M5035.M5034.configure(event, target)
        profile = config["tiers"]["primary24"]
        previous_catalog = module.chamber_residue_catalog
        previous_global_value = module.global_chamber_value
        previous_job = M5212.M5077.M5036.MREPAIR.CURRENT_JOB
        module.chamber_residue_catalog = M5212.certified_5212_catalog
        M5212.M5077.M5036.MREPAIR.CURRENT_JOB = job["job_key"]
        M5212.M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
        M5212.M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
        M5212.M5077.OUTWARD_CONTOUR_AUDIT.clear()
        M5212.M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
        M5212.SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT.clear()
        M5212.M5077.removable_extension_gate()
        extension = M5212.AdaptiveRemovableGlobalExtension(
            previous_global_value
        )
        module.global_chamber_value = extension
        kernel_started = time.monotonic()
        try:
            (
                raw_total,
                residues_stable,
                catalog_row_count,
                safe_pair_count,
                unsafe_pair_count,
                pair_rows,
            ) = M5214.decompose_topological_value(
                module,
                topology,
                profile,
            )
        finally:
            module.chamber_residue_catalog = previous_catalog
            module.global_chamber_value = previous_global_value
            M5212.M5077.M5036.MREPAIR.CURRENT_JOB = previous_job
        kernel_runtime = time.monotonic() - kernel_started

        normalized_total = M5214.KERNEL_MULTIPLIER * raw_total
        family_total = 0.0j
        dominant_value = 0.0j
        weighted_permuted = 0.0j
        augmented_pairs: list[dict[str, Any]] = []
        selected_pair_count = 0
        selected_pairs_safe_and_direct = True
        all_partition_ratios_finite = True
        for pair in pair_rows:
            augmented = dict(pair)
            normalized = row_complex(pair["normalized_contribution"])
            family_total += normalized
            signature = pair["family_signature"]
            if signature == M5214.DOMINANT_FAMILY_SIGNATURE:
                dominant_value += normalized
                selected_pair_count += 1
                selected_pairs_safe_and_direct = (
                    selected_pairs_safe_and_direct
                    and bool(pair["safe"])
                    and "subtraction:" not in signature
                )
            first_ratio = 0.0j
            second_ratio = 0.0j
            weighted_contribution = 0.0j
            if signature == M5214.PERMUTED_FAMILY_SIGNATURE:
                selected_pair_count += 1
                selected_pairs_safe_and_direct = (
                    selected_pairs_safe_and_direct
                    and bool(pair["safe"])
                    and "subtraction:" not in signature
                )
                first_ratio = M5214.permutation_partition_ratio(
                    event,
                    row_complex(pair["first_root"]),
                )
                second_ratio = M5214.permutation_partition_ratio(
                    event,
                    row_complex(pair["second_root"]),
                )
                all_partition_ratios_finite = (
                    all_partition_ratios_finite
                    and finite_complex(first_ratio)
                    and finite_complex(second_ratio)
                )
                weighted_contribution = M5214.KERNEL_MULTIPLIER * (
                    first_ratio
                    * int(pair["first_winding"])
                    * row_complex(pair["first_residue"])
                    + second_ratio
                    * int(pair["second_winding"])
                    * row_complex(pair["second_residue"])
                )
                weighted_permuted += weighted_contribution
            augmented["first_permutation_partition_ratio"] = complex_row(
                first_ratio
            )
            augmented["second_permutation_partition_ratio"] = complex_row(
                second_ratio
            )
            augmented["weighted_permuted_contribution"] = complex_row(
                weighted_contribution
            )
            augmented_pairs.append(augmented)

        control_value = dominant_value - weighted_permuted
        family_closure = abs(family_total - normalized_total)
        crossing_count = sum(
            len(chamber["surface_crossings"])
            for chamber in topology["chambers"]
        )
        pair_coverage = (
            2 * (safe_pair_count + unsafe_pair_count)
            == crossing_count
        )
        maximum_catalog_root_residual = max(
            (
                max(
                    float(pair["first_catalog_root_residual"]),
                    float(pair["second_catalog_root_residual"]),
                )
                for pair in pair_rows
            ),
            default=0.0,
        )
        converged = bool(
            residues_stable
            and pair_coverage
            and finite_complex(normalized_total)
            and finite_complex(control_value)
            and family_closure
            <= float(
                config["fresh_A00_control_contract"][
                    "acceptance_thresholds"
                ]["maximum_event_family_closure"]
            )
            and selected_pairs_safe_and_direct
            and all_partition_ratios_finite
        )
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "config_digest": config["config_digest"],
            **job,
            "status": (
                "COMPLETED_CONVERGED"
                if converged
                else "COMPLETED_UNCONVERGED"
            ),
            "integral_converged": converged,
            "residues_stable": bool(residues_stable),
            "all_crossings_reciprocally_paired": pair_coverage,
            "crossing_count": crossing_count,
            "safe_pair_count": safe_pair_count,
            "unsafe_pair_count": unsafe_pair_count,
            "catalog_row_count": catalog_row_count,
            "pair_rows": augmented_pairs,
            "raw_topological_correction": complex_row(raw_total),
            "normalized_topological_D_hhh_over_G3": complex_row(
                normalized_total
            ),
            "family_sum": complex_row(family_total),
            "family_closure": float(family_closure),
            "dominant_family_value": complex_row(dominant_value),
            "weighted_permuted_family_value": complex_row(
                weighted_permuted
            ),
            "permutation_zero_control": complex_row(control_value),
            "selected_control_pair_count": selected_pair_count,
            "selected_control_pairs_safe_and_direct": (
                selected_pairs_safe_and_direct
            ),
            "all_partition_ratios_finite": (
                all_partition_ratios_finite
            ),
            "maximum_catalog_root_relative_residual": (
                maximum_catalog_root_residual
            ),
            "topology_file": str(topology_path),
            "topology_runtime_seconds": topology_runtime,
            "kernel_runtime_seconds": kernel_runtime,
            "job_runtime_seconds": time.monotonic() - started,
            "source_separated_cluster_zero_count": len(
                M5212.SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT
            ),
            "adaptive_removable_extension_count": len(extension.calls),
            "resumed_from_cache": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    except Exception as error:
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "config_digest": config["config_digest"],
            **job,
            "status": "FAILED",
            "error_type": type(error).__name__,
            "error": str(error),
            "job_runtime_seconds": time.monotonic() - started,
            "resumed_from_cache": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    finally:
        M5212.M5077.CURRENT_EVENT = previous_event
        M5212.M5077.CURRENT_ARGUMENT = previous_argument
    atomic_json(output, result)
    return result


def run_counts(
    run_directory: Path,
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, int]:
    counts = {
        "completed_converged": 0,
        "completed_unconverged": 0,
        "failed": 0,
        "missing": 0,
    }
    for job in jobs:
        path = output_path(run_directory, job)
        if not path.exists():
            counts["missing"] += 1
            continue
        row = read_json(path)
        if row.get("config_digest") != config["config_digest"]:
            counts["missing"] += 1
            continue
        status = row.get("status")
        if status == "COMPLETED_CONVERGED":
            counts["completed_converged"] += 1
        elif status == "COMPLETED_UNCONVERGED":
            counts["completed_unconverged"] += 1
        else:
            counts["failed"] += 1
    return counts


def scalar_summary(values: np.ndarray) -> dict[str, Any]:
    count = int(values.size)
    standard_deviation = (
        float(np.std(values, ddof=1)) if count > 1 else 0.0
    )
    return {
        "count": count,
        "mean": float(np.mean(values)) if count else 0.0,
        "median": float(np.median(values)) if count else 0.0,
        "minimum": float(np.min(values)) if count else 0.0,
        "maximum": float(np.max(values)) if count else 0.0,
        "sample_standard_deviation": standard_deviation,
        "standard_error": (
            standard_deviation / math.sqrt(count) if count else 0.0
        ),
        "median_absolute_deviation": (
            float(np.median(np.abs(values - np.median(values))))
            if count
            else 0.0
        ),
    }


def exact_sign_flip_p(values: np.ndarray) -> float:
    count = int(values.size)
    if count == 0:
        return 1.0
    observed = abs(float(np.mean(values)))
    exceedances = 0
    total = 1 << count
    for mask in range(total):
        signs = np.fromiter(
            (
                1.0 if (mask >> index) & 1 else -1.0
                for index in range(count)
            ),
            dtype=np.float64,
            count=count,
        )
        statistic = abs(float(np.mean(signs * values)))
        if statistic + 1.0e-15 >= observed:
            exceedances += 1
    return exceedances / total


def bootstrap_standard_deviation_ratio(
    raw: np.ndarray,
    adjusted: np.ndarray,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    diagnostics = manifest["diagnostic_only"]
    replicates = int(
        diagnostics["bootstrap_standard_deviation_ratio_replicates"]
    )
    random = np.random.default_rng(int(diagnostics["bootstrap_seed"]))
    indices = random.integers(
        0,
        raw.size,
        size=(replicates, raw.size),
        endpoint=False,
    )
    raw_samples = raw[indices]
    adjusted_samples = adjusted[indices]
    raw_sd = np.std(raw_samples, axis=1, ddof=1)
    adjusted_sd = np.std(adjusted_samples, axis=1, ddof=1)
    valid = raw_sd > 0.0
    ratios = adjusted_sd[valid] / raw_sd[valid]
    quantiles = diagnostics["bootstrap_interval"]
    return {
        "replicates_requested": replicates,
        "replicates_valid": int(ratios.size),
        "seed": int(diagnostics["bootstrap_seed"]),
        "lower_quantile": float(quantiles[0]),
        "upper_quantile": float(quantiles[1]),
        "lower": float(np.quantile(ratios, quantiles[0])),
        "upper": float(np.quantile(ratios, quantiles[1])),
        "median": float(np.median(ratios)),
        "used_for_acceptance": False,
    }


def analyse(
    run_directory: Path,
    config: dict[str, Any],
    manifest: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    counts = run_counts(run_directory, config, jobs)
    if counts["completed_converged"] != len(jobs):
        return (
            {
                "complete": False,
                "counts": counts,
                "fresh_control_pilot_passed": False,
                "scale_decision": "RESUME_OR_REPAIR_WITHOUT_RETUNING",
                "valid_for_numeric_UV_claim": False,
            },
            [],
            [],
        )

    completed = [
        read_json(output_path(run_directory, job)) for job in jobs
    ]
    lookup = {
        (int(row["seed"]), row["epsilon_id"]): row
        for row in completed
    }
    seeds = tuple(
        int(value)
        for value in manifest["fresh_topological_scramble_seeds"]
    )
    expected_keys = {
        (seed, epsilon_id)
        for seed in seeds
        for epsilon_id in ("E020", "E040")
    }
    if set(lookup) != expected_keys:
        raise RuntimeError("fresh A00 pilot matrix is incomplete")

    pair_csv_rows: list[dict[str, Any]] = []
    for row in completed:
        for pair in row["pair_rows"]:
            pair_csv_rows.append(
                {
                    "seed": row["seed"],
                    "event_id": row["event_id"],
                    "epsilon_id": row["epsilon_id"],
                    "pair_index": pair["pair_index"],
                    "safe": pair["safe"],
                    "family_signature": pair["family_signature"],
                    "normalized_contribution": json.dumps(
                        pair["normalized_contribution"],
                        sort_keys=True,
                    ),
                    "first_root": json.dumps(
                        pair["first_root"], sort_keys=True
                    ),
                    "second_root": json.dumps(
                        pair["second_root"], sort_keys=True
                    ),
                    "first_winding": pair["first_winding"],
                    "second_winding": pair["second_winding"],
                    "first_partition_ratio": json.dumps(
                        pair[
                            "first_permutation_partition_ratio"
                        ],
                        sort_keys=True,
                    ),
                    "second_partition_ratio": json.dumps(
                        pair[
                            "second_permutation_partition_ratio"
                        ],
                        sort_keys=True,
                    ),
                    "weighted_permuted_contribution": json.dumps(
                        pair["weighted_permuted_contribution"],
                        sort_keys=True,
                    ),
                    "reciprocal_root_residual": pair[
                        "reciprocal_root_residual"
                    ],
                    "first_catalog_root_residual": pair[
                        "first_catalog_root_residual"
                    ],
                    "second_catalog_root_residual": pair[
                        "second_catalog_root_residual"
                    ],
                    "status": "FRESH_A00_PAIR_CONTRIBUTION",
                    "valid_for_numeric_UV_claim": False,
                }
            )

    event_by_seed = {
        int(row["seed"]): row for row in config["events"]
    }
    physical_weight = float(
        manifest["physical_A00_weight_at_z_minus_0p6"]
    )
    raw_values: list[complex] = []
    control_values: list[complex] = []
    adjusted_values: list[complex] = []
    event_rows: list[dict[str, Any]] = []
    thresholds = manifest["acceptance_thresholds"]
    nonzero_tolerance = float(
        thresholds["relative_nonzero_control_tolerance"]
    )
    nonzero_control_count = 0
    for seed in seeds:
        raw_e020 = row_complex(
            lookup[(seed, "E020")][
                "normalized_topological_D_hhh_over_G3"
            ]
        )
        raw_e040 = row_complex(
            lookup[(seed, "E040")][
                "normalized_topological_D_hhh_over_G3"
            ]
        )
        control_e020 = row_complex(
            lookup[(seed, "E020")]["permutation_zero_control"]
        )
        control_e040 = row_complex(
            lookup[(seed, "E040")]["permutation_zero_control"]
        )
        raw = physical_weight * (2.0 * raw_e020 - raw_e040)
        control = physical_weight * (
            2.0 * control_e020 - control_e040
        )
        adjusted = complex(raw.real - control.real, raw.imag)
        is_nonzero = abs(control.real) > nonzero_tolerance * max(
            1.0, abs(raw.real)
        )
        nonzero_control_count += int(is_nonzero)
        raw_values.append(raw)
        control_values.append(control)
        adjusted_values.append(adjusted)
        event = event_by_seed[seed]
        event_rows.append(
            {
                "seed": seed,
                "event_id": event["event_id"],
                "soft_energy": event["soft_energy"],
                "soft_cosine": event["soft_cosine"],
                "decay_cosine": event["decay_cosine"],
                "raw_A00_real": raw.real,
                "raw_A00_imaginary": raw.imag,
                "control_real": control.real,
                "control_imaginary_diagnostic_only": control.imag,
                "control_nonzero_under_frozen_tolerance": is_nonzero,
                "adjusted_A00_real": adjusted.real,
                "adjusted_A00_imaginary_unchanged": adjusted.imag,
                "E020_selected_control_pair_count": lookup[
                    (seed, "E020")
                ]["selected_control_pair_count"],
                "E040_selected_control_pair_count": lookup[
                    (seed, "E040")
                ]["selected_control_pair_count"],
                "primary_control_applied_to": "real_part_only",
                "status": "FRESH_A00_CONTROL_EVENT",
                "valid_for_numeric_UV_claim": False,
            }
        )

    raw_array = np.asarray(raw_values, dtype=np.complex128)
    control_array = np.asarray(control_values, dtype=np.complex128)
    adjusted_array = np.asarray(
        adjusted_values, dtype=np.complex128
    )
    raw_real = raw_array.real
    adjusted_real = adjusted_array.real
    raw_summary = scalar_summary(raw_real)
    adjusted_summary = scalar_summary(adjusted_real)
    control_summary = scalar_summary(control_array.real)
    raw_sd = float(raw_summary["sample_standard_deviation"])
    adjusted_sd = float(
        adjusted_summary["sample_standard_deviation"]
    )
    standard_deviation_ratio = (
        adjusted_sd / raw_sd if raw_sd > 0.0 else None
    )
    variance_reduction_factor = (
        1.0 / standard_deviation_ratio**2
        if standard_deviation_ratio is not None
        and standard_deviation_ratio > 0.0
        else None
    )
    control_standard_error = float(control_summary["standard_error"])
    if control_standard_error > 0.0:
        control_mean_standard_errors = abs(
            float(control_summary["mean"])
        ) / control_standard_error
    elif float(control_summary["mean"]) == 0.0:
        control_mean_standard_errors = 0.0
    else:
        control_mean_standard_errors = None
    control_mean_zero_compatible = (
        control_mean_standard_errors is not None
        and control_mean_standard_errors
        <= float(
            thresholds[
                "maximum_absolute_control_mean_standard_errors"
            ]
        )
    )
    efficiency_reproduced = (
        standard_deviation_ratio is not None
        and standard_deviation_ratio
        < float(
            thresholds[
                "maximum_A00_real_standard_deviation_ratio"
            ]
        )
    )
    enough_nonzero_controls = nonzero_control_count >= int(
        thresholds["minimum_nonzero_control_events"]
    )
    structural_gate = bool(
        all(row["residues_stable"] for row in completed)
        and all(
            row["all_crossings_reciprocally_paired"]
            for row in completed
        )
        and all(
            row["selected_control_pairs_safe_and_direct"]
            for row in completed
        )
        and all(
            row["all_partition_ratios_finite"]
            for row in completed
        )
        and max(float(row["family_closure"]) for row in completed)
        <= float(thresholds["maximum_event_family_closure"])
        and max(
            float(row["maximum_catalog_root_relative_residual"])
            for row in completed
        )
        <= float(
            thresholds["maximum_catalog_root_relative_residual"]
        )
    )
    fresh_control_pilot_passed = bool(
        structural_gate
        and control_mean_zero_compatible
        and efficiency_reproduced
        and enough_nonzero_controls
    )
    delete_one_ratios: list[dict[str, Any]] = []
    for index, seed in enumerate(seeds):
        keep = np.ones(len(seeds), dtype=bool)
        keep[index] = False
        raw_delete_sd = float(np.std(raw_real[keep], ddof=1))
        adjusted_delete_sd = float(
            np.std(adjusted_real[keep], ddof=1)
        )
        delete_one_ratios.append(
            {
                "held_seed": seed,
                "standard_deviation_ratio": (
                    adjusted_delete_sd / raw_delete_sd
                    if raw_delete_sd > 0.0
                    else None
                ),
            }
        )
    covariance = float(
        np.cov(raw_real, control_array.real, ddof=1)[0, 1]
    )
    correlation = (
        float(np.corrcoef(raw_real, control_array.real)[0, 1])
        if np.std(raw_real, ddof=1) > 0.0
        and np.std(control_array.real, ddof=1) > 0.0
        else 0.0
    )
    scale_decision = (
        "AUTHORIZE_SCALED_CONTROLLED_TOPOLOGICAL_RUN"
        if fresh_control_pilot_passed
        else "REJECT_SCALING_AND_DERIVE_A_NEW_ESTIMATOR"
    )
    audit_5214 = read_json(AUDIT_5214)
    analysis = {
        "complete": True,
        "counts": counts,
        "event_count": len(seeds),
        "raw_A00_real": raw_summary,
        "adjusted_A00_real": adjusted_summary,
        "control_real": control_summary,
        "raw_A00_imaginary": scalar_summary(raw_array.imag),
        "control_imaginary_diagnostic_only": scalar_summary(
            control_array.imag
        ),
        "standard_deviation_ratio": standard_deviation_ratio,
        "variance_reduction_factor": variance_reduction_factor,
        "bootstrap_standard_deviation_ratio": (
            bootstrap_standard_deviation_ratio(
                raw_real,
                adjusted_real,
                manifest,
            )
        ),
        "control_mean_in_standard_errors": (
            control_mean_standard_errors
        ),
        "control_exact_sign_flip_p": exact_sign_flip_p(
            control_array.real
        ),
        "raw_control_covariance": covariance,
        "raw_control_correlation": correlation,
        "nonzero_control_event_count": nonzero_control_count,
        "delete_one_standard_deviation_ratios": delete_one_ratios,
        "maximum_event_family_closure": max(
            float(row["family_closure"]) for row in completed
        ),
        "maximum_catalog_root_relative_residual": max(
            float(row["maximum_catalog_root_relative_residual"])
            for row in completed
        ),
        "selected_control_pair_count": sum(
            int(row["selected_control_pair_count"])
            for row in completed
        ),
        "source_separated_cluster_zero_count": sum(
            int(row["source_separated_cluster_zero_count"])
            for row in completed
        ),
        "adaptive_removable_extension_count": sum(
            int(row["adaptive_removable_extension_count"])
            for row in completed
        ),
        "structural_gate_passed": structural_gate,
        "control_mean_zero_compatible": (
            control_mean_zero_compatible
        ),
        "efficiency_reproduced": efficiency_reproduced,
        "enough_nonzero_controls": enough_nonzero_controls,
        "fresh_control_pilot_passed": fresh_control_pilot_passed,
        "scale_decision": scale_decision,
        "thresholds_used": thresholds,
        "retrospective_A00_standard_deviation_ratio": audit_5214[
            "permutation_control"
        ]["A00_real_variance"]["standard_deviation_ratio"],
        "retrospective_control_mean_in_standard_errors": audit_5214[
            "permutation_control"
        ]["control_mean_in_standard_errors"],
        "thresholds_retuned_after_outcomes": False,
        "numeric_UV_coefficient_complete": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return analysis, event_rows, pair_csv_rows


def validation_rows(
    state: str,
    activation: dict[str, Any],
    protocol_lock: dict[str, Any],
    counts: dict[str, int],
    analysis: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        (
            "activation_prerequisites_complete",
            all(activation["prerequisites"].values()),
            json.dumps(
                activation["prerequisites"], sort_keys=True
            ),
        ),
        (
            "protocol_locked_before_outcomes",
            not bool(protocol_lock["outcomes_present_at_lock"])
            and not bool(protocol_lock["threshold_retuning_allowed"]),
            protocol_lock["locked_at_utc"],
        ),
        (
            "fresh_seed_scan_is_clean",
            not activation["prior_seed_occurrences"],
            json.dumps(
                activation["prior_seed_occurrences"],
                sort_keys=True,
            ),
        ),
        (
            "checkpoint_remains_nonclaim",
            not bool(analysis["valid_for_numeric_UV_claim"])
            and not bool(
                analysis.get("valid_for_local_GR_claim", False)
            )
            and not bool(
                analysis.get("valid_for_full_MTS_claim", False)
            ),
            "numeric_UV=false; local_GR=false; full_MTS=false",
        ),
    ]
    if state != "DRY_RUN":
        thresholds = analysis["thresholds_used"]
        recomputed_mean_gate = bool(
            analysis["control_mean_in_standard_errors"] is not None
            and analysis["control_mean_in_standard_errors"]
            <= float(
                thresholds[
                    "maximum_absolute_control_mean_standard_errors"
                ]
            )
        )
        recomputed_efficiency_gate = bool(
            analysis["standard_deviation_ratio"] is not None
            and analysis["standard_deviation_ratio"]
            < float(
                thresholds[
                    "maximum_A00_real_standard_deviation_ratio"
                ]
            )
        )
        recomputed_nonzero_gate = bool(
            analysis["nonzero_control_event_count"]
            >= int(thresholds["minimum_nonzero_control_events"])
        )
        recomputed_pilot_gate = bool(
            analysis["structural_gate_passed"]
            and recomputed_mean_gate
            and recomputed_efficiency_gate
            and recomputed_nonzero_gate
        )
        checks.extend(
            [
                (
                    "all_24_fresh_jobs_converged",
                    counts["completed_converged"] == 24
                    and counts["completed_unconverged"] == 0
                    and counts["failed"] == 0
                    and counts["missing"] == 0,
                    json.dumps(counts, sort_keys=True),
                ),
                (
                    "fresh_control_structural_gate",
                    bool(analysis["structural_gate_passed"]),
                    json.dumps(
                        {
                            "family_closure": analysis[
                                "maximum_event_family_closure"
                            ],
                            "catalog_root_residual": analysis[
                                "maximum_catalog_root_relative_residual"
                            ],
                        },
                        sort_keys=True,
                    ),
                ),
                (
                    "scientific_decision_recomputed_from_frozen_gates",
                    recomputed_pilot_gate
                    == bool(
                        analysis["fresh_control_pilot_passed"]
                    )
                    and recomputed_mean_gate
                    == bool(
                        analysis[
                            "control_mean_zero_compatible"
                        ]
                    )
                    and recomputed_efficiency_gate
                    == bool(analysis["efficiency_reproduced"])
                    and recomputed_nonzero_gate
                    == bool(analysis["enough_nonzero_controls"]),
                    analysis["scale_decision"],
                ),
                (
                    "no_threshold_retuning_after_outcomes",
                    not bool(
                        analysis[
                            "thresholds_retuned_after_outcomes"
                        ]
                    ),
                    json.dumps(thresholds, sort_keys=True),
                ),
                (
                    "scale_decision_is_fail_closed",
                    analysis["scale_decision"]
                    in {
                        "AUTHORIZE_SCALED_CONTROLLED_TOPOLOGICAL_RUN",
                        "REJECT_SCALING_AND_DERIVE_A_NEW_ESTIMATOR",
                    },
                    analysis["scale_decision"],
                ),
            ]
        )
    return [
        {
            "check": name,
            "passed": bool(passed),
            "detail": detail,
            "status": "PASS" if passed else "FAIL",
            "checkpoint_marker": MARKER,
        }
        for name, passed, detail in checks
    ]


def write_document(
    state: str,
    result: dict[str, Any],
) -> None:
    analysis = result["analysis"]
    if state == "DRY_RUN":
        result_section = """## Locked experiment

The protocol is frozen before outcomes. It contains twelve fresh independent
topological events, two epsilon values and only the `A00` crossed argument:
`12 x 2 x 1 = 24` jobs. No checkpoint-5215 topology or residue value existed
when the lock was written.

Execution has not yet started."""
        decision = "FROZEN_AWAITING_EXECUTION"
    else:
        bootstrap = analysis["bootstrap_standard_deviation_ratio"]
        result_section = f"""## Fresh result

- Completed jobs: `{analysis['counts']['completed_converged']}/24`.
- Raw real `A00` mean: `{analysis['raw_A00_real']['mean']:.12g}`.
- Raw real `A00` standard deviation:
  `{analysis['raw_A00_real']['sample_standard_deviation']:.12g}`.
- Controlled real `A00` mean:
  `{analysis['adjusted_A00_real']['mean']:.12g}`.
- Controlled real `A00` standard deviation:
  `{analysis['adjusted_A00_real']['sample_standard_deviation']:.12g}`.
- Fresh standard-deviation ratio:
  `{analysis['standard_deviation_ratio']:.12g}`.
- Fresh variance-reduction factor:
  `{analysis['variance_reduction_factor']:.12g}`.
- Diagnostic paired-bootstrap ratio interval:
  `[{bootstrap['lower']:.12g}, {bootstrap['upper']:.12g}]`.
- Control mean in standard errors:
  `{analysis['control_mean_in_standard_errors']:.12g}`.
- Exact sign-flip diagnostic `p`:
  `{analysis['control_exact_sign_flip_p']:.12g}`.
- Nonzero controlled events:
  `{analysis['nonzero_control_event_count']}/12`.
- Selected source-pair rows:
  `{analysis['selected_control_pair_count']}`.
- Maximum event-family closure:
  `{analysis['maximum_event_family_closure']:.3e}`.

The structural gate is `{analysis['structural_gate_passed']}`, mean-zero
compatibility is `{analysis['control_mean_zero_compatible']}`, and fresh
efficiency reproduction is `{analysis['efficiency_reproduced']}`."""
        decision = analysis["scale_decision"]

    document = f"""# 5215 - Fresh A00 identical-graviton permutation-control pilot

## Decision

`{decision}`

This checkpoint executes the fresh experiment authorized by checkpoint 5214.
It does not select a friendlier source family, refit the control coefficient,
or change the acceptance thresholds after observing outcomes.

## Frozen estimator

The exact identical-graviton identity is

`C_13 = Y[g1+,g3-] - (w1/w3)Y[g1-,g3+]`,

with

`w1/w3 = (E3/E1)^2`

inserted independently at each reciprocal root before winding-weighted
residue summation. The real control coefficient is exactly `1`; the
imaginary coefficient is exactly `0`.

The physical `A00` row uses the frozen extrapolation

`A00(0) = 2 A00(E020) - A00(E040)`

and the fixed `z=-0.6` weight `-0.008`.

{result_section}

## Frozen acceptance rule

Scaling is authorized only when all 24 jobs converge, every structural gate
passes, the absolute control mean is at most two standard errors, at least two
events carry a nonzero control under the frozen tolerance, and

`SD(controlled A00 real) / SD(raw A00 real) < 0.5`.

The bootstrap interval and exact sign-flip result are diagnostics only.

## Claim boundary

This pilot tests estimator bias and efficiency. It does not establish a
canonical two-loop coefficient. Numeric UV, all-operator local GR and full
MTS flags remain false. The exact checkpoint-5211 two-derivative
GR+Lambda+SM+Maxwell branch is unchanged.

## Machine-readable evidence

- `{MANIFEST}`
- `{PROTOCOL_LOCK}`
- `{ACTIVATION_JSON}`
- `{FROZEN_CONFIG}`
- `{FROZEN_SCHEDULE}`
- `{EVENT_ROWS_CSV}`
- `{PAIR_ROWS_CSV}`
- `{RESULT_JSON}`
- `{VALIDATION_CSV}`
- `{PROVENANCE}`
"""
    atomic_text(DOCUMENT, document)


def write_provenance(
    state: str,
    result: dict[str, Any],
) -> None:
    lines = [
        "# Checkpoint 5215 provenance",
        "",
        f"- Marker: `{MARKER}`.",
        f"- State: `{state}`.",
        f"- Manifest SHA-256: `{digest(MANIFEST)}`.",
        f"- Protocol-lock SHA-256: `{digest(PROTOCOL_LOCK)}`.",
        f"- Runner SHA-256: `{digest(Path(__file__).resolve())}`.",
        f"- Parent 5212 runner SHA-256: `{digest(SCRIPT_5212)}`.",
        f"- Parent 5214 runner SHA-256: `{digest(SCRIPT_5214)}`.",
        f"- Checkpoint-5214 audit SHA-256: `{digest(AUDIT_5214)}`.",
        (
            "- Formalization-workbench SHA-256: "
            f"`{result['formalization_workbench_tree_sha256']}`."
        ),
        f"- Run id: `{result['run_id']}`.",
        f"- Validation: `{result['validation_check_count']}/"
        f"{result['validation_check_count']}` rows recorded; "
        f"all pass = `{result['validation_all_passed']}`.",
        "",
        "No public repository, galaxy repository or formalization-workbench",
        "file is modified by this runner. All outputs remain private and",
        "non-claim.",
    ]
    atomic_text(PROVENANCE, "\n".join(lines) + "\n")


def finalize(
    run_id: str,
    state: str,
    activation: dict[str, Any],
    protocol_lock: dict[str, Any],
    counts: dict[str, int],
    analysis: dict[str, Any],
    event_rows: list[dict[str, Any]],
    pair_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    if event_rows:
        write_csv(EVENT_ROWS_CSV, event_rows)
    if pair_rows:
        write_csv(PAIR_ROWS_CSV, pair_rows)
    formal_digest = tree_digest(FORMAL)
    result = {
        "checkpoint": 5215,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": run_id,
        "state": state,
        "counts": counts,
        "analysis": analysis,
        "manifest_sha256": activation["manifest_sha256"],
        "protocol_lock_sha256": digest(PROTOCOL_LOCK),
        "config_digest": activation["config_digest"],
        "schedule_digest": activation["schedule_digest"],
        "formalization_workbench_tree_sha256": formal_digest,
        "numeric_UV_coefficient_complete": False,
        "local_GR_claim": False,
        "full_MTS_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = validation_rows(
        state,
        activation,
        protocol_lock,
        counts,
        analysis,
    )
    result["validation_all_passed"] = all(
        row["passed"] for row in validations
    )
    result["validation_check_count"] = len(validations)
    atomic_json(RESULT_JSON, result)
    write_csv(VALIDATION_CSV, validations)
    write_document(state, result)
    write_provenance(state, result)
    return result


def execute(
    run_id: str,
    activation: dict[str, Any],
    protocol_lock: dict[str, Any],
    config: dict[str, Any],
    manifest: dict[str, Any],
    jobs: list[dict[str, Any]],
    wall_cap_hours: float,
    maximum_new_jobs: int,
) -> dict[str, Any]:
    if not activation["execution_authorized"]:
        raise RuntimeError("checkpoint-5215 prerequisites are incomplete")
    if not (0.0 < wall_cap_hours <= MAXIMUM_WALL_HOURS):
        raise ValueError(
            "wall cap must be positive and no greater than four hours"
        )
    run_directory = RUNS / run_id
    run_directory.mkdir(parents=True, exist_ok=True)
    run_config = run_directory / "config.json"
    if run_config.exists():
        existing = read_json(run_config)
        if existing["config_digest"] != config["config_digest"]:
            raise RuntimeError("run config changed; use the frozen run id")
    else:
        atomic_json(run_config, config)
    atomic_json(run_directory / "activation.json", activation)
    M5212.source_separated_cluster_gate()
    M5212.M5077.certified_primary_catalog = (
        M5212.certified_5212_catalog
    )
    M5212.M5077.M5085.CertifiedRemovableGlobalExtension = (
        M5212.AdaptiveRemovableGlobalExtension
    )
    M5212.M5077.install_history_invariant_breakpoints(
        M5212.M5077.M5036.N5030
    )
    manager = M5212.M5077.CentralTopologyManager(
        run_directory, config
    )
    started = time.monotonic()
    newly_executed = 0
    resumed = 0
    state = "RUNNING"
    blocking_job: dict[str, Any] | None = None
    last_schedule_key: str | None = None
    for index, job in enumerate(jobs, start=1):
        if (time.monotonic() - started) / 3600.0 >= wall_cap_hours:
            state = "PAUSED_WALL_CAP"
            break
        row = execute_job(run_directory, config, manager, job)
        last_schedule_key = job["schedule_key"]
        if row.get("resumed_from_cache"):
            resumed += 1
        else:
            newly_executed += 1
        log_row = {
            "checkpoint_marker": MARKER,
            "schedule_index": index,
            "expected_job_count": len(jobs),
            "schedule_key": job["schedule_key"],
            "status": row["status"],
            "resumed_from_cache": bool(
                row.get("resumed_from_cache")
            ),
            "recorded_job_runtime_seconds": row[
                "job_runtime_seconds"
            ],
            "invocation_elapsed_seconds": (
                time.monotonic() - started
            ),
        }
        append_jsonl(run_directory / "log.jsonl", log_row)
        counts = run_counts(run_directory, config, jobs)
        atomic_json(
            run_directory / "status.json",
            {
                "checkpoint_marker": MARKER,
                "revision": REVISION,
                "run_id": run_id,
                "state": "RUNNING",
                "schedule_index": index,
                "last_schedule_key": last_schedule_key,
                "newly_executed_this_invocation": newly_executed,
                "resumed_this_invocation": resumed,
                "invocation_elapsed_seconds": (
                    time.monotonic() - started
                ),
                **counts,
                "valid_for_numeric_UV_claim": False,
            },
        )
        print(json.dumps(log_row), flush=True)
        if row["status"] != "COMPLETED_CONVERGED":
            state = "BLOCKED_JOB_FAILURE"
            blocking_job = row
            break
        if (
            maximum_new_jobs > 0
            and newly_executed >= maximum_new_jobs
        ):
            state = "PAUSED_JOB_CAP"
            break

    counts = run_counts(run_directory, config, jobs)
    if counts["completed_converged"] == len(jobs):
        state = "COMPLETE"
    analysis, event_rows, pair_rows = analyse(
        run_directory,
        config,
        manifest,
        jobs,
    )
    status = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": run_id,
        "state": state,
        "expected_job_count": len(jobs),
        "newly_executed_this_invocation": newly_executed,
        "resumed_this_invocation": resumed,
        "last_schedule_key": last_schedule_key,
        "blocking_job": blocking_job,
        "invocation_elapsed_seconds": time.monotonic() - started,
        **counts,
        "analysis": analysis,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(run_directory / "status.json", status)
    if state == "COMPLETE":
        atomic_json(run_directory / "COMPLETED.json", status)
    return finalize(
        run_id,
        state,
        activation,
        protocol_lock,
        counts,
        analysis,
        event_rows,
        pair_rows,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "analyse"),
        default="dry-run",
    )
    parser.add_argument(
        "--run-id",
        default="fresh_A00_control_pilot_v1",
    )
    parser.add_argument(
        "--wall-cap-hours",
        type=float,
        default=4.0,
    )
    parser.add_argument(
        "--maximum-new-jobs",
        type=int,
        default=0,
    )
    arguments = parser.parse_args()

    manifest = read_json(MANIFEST)
    if manifest["checkpoint_marker"] != MARKER:
        raise RuntimeError("checkpoint-5215 manifest marker changed")
    config = make_config(manifest, arguments.run_id)
    jobs = build_schedule(config, manifest)
    activation = activation_record(manifest, config, jobs)
    atomic_json(ACTIVATION_JSON, activation)
    protocol_lock = lock_protocol(activation, config, jobs)

    if arguments.mode == "dry-run":
        counts = {
            "completed_converged": 0,
            "completed_unconverged": 0,
            "failed": 0,
            "missing": len(jobs),
        }
        analysis = {
            "complete": False,
            "counts": counts,
            "fresh_control_pilot_passed": False,
            "scale_decision": "FROZEN_AWAITING_EXECUTION",
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        result = finalize(
            arguments.run_id,
            "DRY_RUN",
            activation,
            protocol_lock,
            counts,
            analysis,
            [],
            [],
        )
    elif arguments.mode == "run":
        result = execute(
            arguments.run_id,
            activation,
            protocol_lock,
            config,
            manifest,
            jobs,
            arguments.wall_cap_hours,
            arguments.maximum_new_jobs,
        )
    else:
        run_directory = RUNS / arguments.run_id
        if not (run_directory / "config.json").exists():
            raise RuntimeError(f"run does not exist: {run_directory}")
        existing = read_json(run_directory / "config.json")
        if existing["config_digest"] != config["config_digest"]:
            raise RuntimeError("frozen run config changed")
        counts = run_counts(run_directory, config, jobs)
        state = (
            "COMPLETE"
            if counts["completed_converged"] == len(jobs)
            else "INCOMPLETE_ANALYSIS"
        )
        analysis, event_rows, pair_rows = analyse(
            run_directory,
            config,
            manifest,
            jobs,
        )
        result = finalize(
            arguments.run_id,
            state,
            activation,
            protocol_lock,
            counts,
            analysis,
            event_rows,
            pair_rows,
        )

    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "state": result["state"],
                "counts": result["counts"],
                "scale_decision": result["analysis"][
                    "scale_decision"
                ],
                "fresh_control_pilot_passed": result["analysis"][
                    "fresh_control_pilot_passed"
                ],
                "validation_all_passed": result[
                    "validation_all_passed"
                ],
                "valid_for_numeric_UV_claim": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
