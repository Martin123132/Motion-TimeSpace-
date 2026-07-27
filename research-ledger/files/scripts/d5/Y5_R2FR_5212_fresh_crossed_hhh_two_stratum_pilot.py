from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5212"
RUNS = SOURCE / "runs"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5123 = POST / "scripts" / "Y5_R2FR_5123_physical_hhh_angular_first_and_crossed_remainder_audit.py"
SCRIPT_5124 = POST / "scripts" / "Y5_R2FR_5124_crossed_hhh_two_stratum_derivation.py"
SCRIPT_5213 = POST / "scripts" / "Y5_R2FR_5213_source_separated_additive_cluster_cauchy_zero.py"
CHECKPOINT_4987 = POST / "4987-Y5-R2FR-full-finite-scheme-orbit-and-irreducible-two-loop-cut-reduction.md"
CHECKPOINT_5123 = POST / "5123-Y5-R2FR-physical-hhh-angular-first-and-crossed-remainder-audit.md"
CHECKPOINT_5124 = POST / "5124-Y5-R2FR-crossed-hhh-two-stratum-derivation.md"
CHECKPOINT_5213 = POST / "5213-Y5-R2FR-source-separated-additive-cluster-Cauchy-zero-theorem.md"
MANIFEST = SOURCE / "locked_two_stratum_pilot_manifest.json"
DESIGN_5124 = POST / "source-intake" / "functional_rg" / "5124" / "crossed_hhh_two_stratum_derivation.json"
PHYSICAL_ROWS_5123 = POST / "source-intake" / "functional_rg" / "5123" / "physical_hhh_angular_first_rows.csv"
TARGET_5018 = POST / "source-intake" / "functional_rg" / "5018" / "hh_Hadamard_crossing_completion_results.json"
LOCKED_MANIFEST_5076 = POST / "source-intake" / "functional_rg" / "5076" / "locked_central_anchor_pilot_manifest.json"
GATE_5213 = POST / "source-intake" / "functional_rg" / "5213" / "source_separated_additive_cluster_cauchy_zero.json"

ACTIVATION_JSON = SOURCE / "fresh_two_stratum_pilot_activation.json"
EVENT_ROWS_CSV = SOURCE / "fresh_two_stratum_completed_event_rows.csv"
RESULT_JSON = SOURCE / "fresh_two_stratum_pilot_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5212-Y5-R2FR-fresh-crossed-hhh-two-stratum-pilot.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5212_VALIDATION.csv"

MARKER = "MTS_5212_FRESH_CROSSED_HHH_TWO_STRATUM_PILOT"
REVISION = "fresh-independent-two-stratum-reciprocal-reduced-v2"
CHECKED_DATE = "2026-07-24"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
MAXIMUM_WALL_HOURS = 4.0
PHYSICAL_COSINES = np.asarray((-0.6, -0.3, 0.0, 0.3, 0.6), dtype=np.float64)
KNOWN_MASTER_LOCAL_COEFFICIENT = 161.42318077192922
COMPONENTS = ("topological", "naive", "total")
ADAPTIVE_REMOVABLE_LEVELS = (
    3.125e-5,
    1.5625e-5,
    7.8125e-6,
    3.90625e-6,
    1.953125e-6,
)
ADAPTIVE_REMOVABLE_TOLERANCE = 1.0e-7


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module(SCRIPT_5077, "mts_5077_for_5212")
M5124 = load_module(SCRIPT_5124, "mts_5124_for_5212")
M5213 = load_module(SCRIPT_5213, "mts_5213_for_5212")
ORIGINAL_CERTIFIED_PRIMARY_CATALOG = M5077.certified_primary_catalog
SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT: list[dict[str, Any]] = []


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
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def row_complex(value: Any) -> complex:
    if isinstance(value, str):
        return complex(value)
    return complex(float(value["real"]), float(value["imaginary"]))


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def source_separated_cluster_gate() -> dict[str, Any]:
    if not GATE_5213.exists():
        raise FileNotFoundError(GATE_5213)
    gate = read_json(GATE_5213)
    if not gate["passed"] or not gate["runner_integration_authorized"]:
        raise RuntimeError("5213 source-separated Cauchy gate is not accepted")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5213 formalization baseline changed")
    if gate["source_topology_sha256"] != digest(Path(gate["source_topology"])):
        raise RuntimeError("5213 source topology changed")
    historical = gate["historical_falsification"]
    historical_path = Path(historical["source"])
    if (
        not historical_path.exists()
        or historical["source_sha256"] != digest(historical_path)
    ):
        raise RuntimeError("5213 historical falsification corpus changed")
    return gate


def certified_5212_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    catalog, stable = ORIGINAL_CERTIFIED_PRIMARY_CATALOG(
        ownership,
        start,
        end,
        required_roots,
        global_nodes,
        global_residue_nodes,
        relative_residue_nodes,
        model_distance,
    )
    if stable:
        return catalog, stable
    gate = source_separated_cluster_gate()
    repairs: list[dict[str, Any]] = []
    catalog, stable = M5213.apply_source_separated_cluster_zero(
        catalog,
        ownership,
        M5077.M5036.N5030,
        M5077.M5036.MREPAIR.CURRENT_JOB,
        repairs,
        gate["historical_falsification"],
    )
    for repair in repairs:
        audited = {
            **repair,
            "gate": str(GATE_5213),
            "gate_sha256": digest(GATE_5213),
            "theorem_script": str(SCRIPT_5213),
            "theorem_script_sha256": digest(SCRIPT_5213),
        }
        SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT.append(audited)
        M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.append(audited)
    return catalog, stable


ORIGINAL_REMOVABLE_EXTENSION = M5077.M5085.CertifiedRemovableGlobalExtension


def adaptive_symmetric_richardson_extension(
    relative_circle: complex,
    ownership: dict[str, bool],
    global_nodes: int,
    global_residue_nodes: int,
    original: Any,
    labels: tuple[str, ...],
) -> tuple[complex, dict[str, Any]]:
    if not M5077.M5085.eligible_collision(labels, ownership):
        raise RuntimeError(
            f"same-source collision is outside adaptive 5212 scope: {labels}"
        )
    scale = max(abs(relative_circle), 1.0e-6)
    direction_rows: list[dict[str, Any]] = []
    directional_richardson: list[list[complex]] = []
    for direction in M5077.M5085.DIRECTIONS:
        averages: list[complex] = []
        level_rows: list[dict[str, Any]] = []
        for fraction in ADAPTIVE_REMOVABLE_LEVELS:
            offset = fraction * scale * direction
            minus = original(
                relative_circle - offset,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            plus = original(
                relative_circle + offset,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            average = (minus + plus) / 2.0
            averages.append(average)
            level_rows.append(
                {
                    "fraction": fraction,
                    "minus": complex_row(minus),
                    "plus": complex_row(plus),
                    "symmetric_average": complex_row(average),
                    "side_difference": float(abs(minus - plus)),
                }
            )
        richardson = [
            (4.0 * averages[index] - averages[index - 1]) / 3.0
            for index in range(1, len(averages))
        ]
        directional_richardson.append(richardson)
        direction_rows.append(
            {
                "direction": complex_row(direction),
                "levels": level_rows,
                "richardson_limits": [
                    complex_row(value) for value in richardson
                ],
            }
        )

    selected_depth: int | None = None
    selected_limits: list[complex] = []
    selected_convergence = math.inf
    selected_spread = math.inf
    depth_rows: list[dict[str, Any]] = []
    for depth in range(1, len(ADAPTIVE_REMOVABLE_LEVELS) - 1):
        limits = [values[depth] for values in directional_richardson]
        previous = [values[depth - 1] for values in directional_richardson]
        mean_limit = sum(limits) / len(limits)
        convergence = max(
            abs(value - earlier) / max(1.0, abs(value))
            for value, earlier in zip(limits, previous)
        )
        spread = max(
            abs(value - mean_limit) for value in limits
        ) / max(1.0, abs(mean_limit))
        accepted = bool(
            convergence < ADAPTIVE_REMOVABLE_TOLERANCE
            and spread < ADAPTIVE_REMOVABLE_TOLERANCE
            and math.isfinite(mean_limit.real)
            and math.isfinite(mean_limit.imag)
        )
        depth_rows.append(
            {
                "finest_fraction": ADAPTIVE_REMOVABLE_LEVELS[depth + 1],
                "maximum_successive_richardson_change": float(convergence),
                "direction_independence_relative_spread": float(spread),
                "accepted": accepted,
            }
        )
        if accepted:
            selected_depth = depth
            selected_limits = limits
            selected_convergence = float(convergence)
            selected_spread = float(spread)
            break
    if selected_depth is None:
        raise RuntimeError(
            "5212 adaptive removable extension did not converge: "
            f"convergence={depth_rows[-1]['maximum_successive_richardson_change']}, "
            f"direction_spread={depth_rows[-1]['direction_independence_relative_spread']}"
        )
    returned = sum(selected_limits) / len(selected_limits)
    return returned, {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "relative_circle": complex_row(relative_circle),
        "labels": list(labels),
        "ownership_digest": M5077.M5085.ownership_digest(ownership),
        "global_nodes": global_nodes,
        "global_residue_nodes": global_residue_nodes,
        "directions": direction_rows,
        "depth_audit": depth_rows,
        "selected_finest_fraction": ADAPTIVE_REMOVABLE_LEVELS[
            selected_depth + 1
        ],
        "maximum_successive_richardson_change": selected_convergence,
        "direction_independence_relative_spread": selected_spread,
        "returned_limit": complex_row(returned),
        "accepted": True,
        "analytic_contract": (
            "a removable holomorphic collision has an even symmetric expansion "
            "A(h)=L+c2*h^2+c4*h^4+...; Richardson removes c2 and successive "
            "extrapolants test the remaining O(h^4) term"
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_full_MTS_claim": False,
    }


class AdaptiveRemovableGlobalExtension:
    def __init__(self, original: Any) -> None:
        self.original = original
        self.primary = ORIGINAL_REMOVABLE_EXTENSION(original)
        self.calls: list[dict[str, Any]] = []
        self.cache: dict[tuple[Any, ...], complex] = {}
        self.primary_call_cursor = 0

    def sync_primary_calls(self) -> None:
        if len(self.primary.calls) > self.primary_call_cursor:
            self.calls.extend(self.primary.calls[self.primary_call_cursor :])
            self.primary_call_cursor = len(self.primary.calls)

    def __call__(
        self,
        relative_circle: complex,
        ownership: dict[str, bool],
        global_nodes: int,
        global_residue_nodes: int,
    ) -> complex:
        try:
            value = self.primary(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            self.sync_primary_calls()
            return value
        except RuntimeError as error:
            self.sync_primary_calls()
            if not str(error).startswith(
                "5085 removable extension did not converge:"
            ):
                raise
            try:
                self.original(
                    relative_circle,
                    ownership,
                    global_nodes,
                    global_residue_nodes,
                )
            except RuntimeError as original_error:
                labels = M5077.M5085.labels_from_error(original_error)
                original_error_text = str(original_error)
            else:
                raise RuntimeError(
                    "adaptive extension could not reproduce the underlying collision"
                ) from error
            if not M5077.M5085.eligible_collision(labels, ownership):
                raise
            key = (
                round(relative_circle.real, 11),
                round(relative_circle.imag, 11),
                tuple(sorted(labels)),
                M5077.M5085.ownership_digest(ownership),
                int(global_nodes),
                int(global_residue_nodes),
            )
            if key in self.cache:
                return self.cache[key]
            value, audit = adaptive_symmetric_richardson_extension(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
                self.original,
                labels,
            )
            audit["superseded_fixed_grid_error"] = str(error)
            audit["original_collision_error"] = original_error_text
            self.calls.append(audit)
            self.cache[key] = value
            return value


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def make_config(manifest: dict[str, Any], run_id: str) -> dict[str, Any]:
    config = M5077.make_config(manifest, run_id)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["pilot_manifest"] = str(MANIFEST)
    config["pilot_manifest_digest"] = digest(MANIFEST)
    config["two_stratum_design_source"] = str(DESIGN_5124)
    config["two_stratum_design_source_digest"] = digest(DESIGN_5124)
    config["two_stratum_contract"] = {
        "full_seeds": manifest["fresh_full_scramble_seeds"],
        "topological_seeds": manifest["fresh_topological_scramble_seeds"],
        "required_base_argument_ids": manifest["required_base_argument_ids"],
        "epsilon_ids": manifest["epsilon_ids"],
        "profile": manifest["profile"],
        "pole_model_and_smooth_must_remain_paired": True,
        "unsafe_reciprocal_pairs_evaluate_both_roots": True,
        "pilot_only": True,
    }
    config["adaptive_removable_extension_policy"] = {
        "base_gate": str(M5077.REMOVABLE_EXTENSION_GATE),
        "base_gate_sha256": digest(M5077.REMOVABLE_EXTENSION_GATE),
        "activation": "only after the fixed-grid 5085 extension fails convergence",
        "levels": list(ADAPTIVE_REMOVABLE_LEVELS),
        "successive_richardson_tolerance": ADAPTIVE_REMOVABLE_TOLERANCE,
        "direction_spread_tolerance": ADAPTIVE_REMOVABLE_TOLERANCE,
        "scope": "the unchanged 5085 eligible direct:g1/direct:g2 same-source collisions",
        "threshold_relaxed": False,
        "failure_action": "fail closed",
    }
    config.pop("config_digest", None)
    config["config_digest"] = M5077.M5036.canonical_digest(config)
    return config


def event_jobs(
    event: dict[str, Any],
    stratum: str,
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id in manifest["epsilon_ids"]:
        for base_id in manifest["required_base_argument_ids"]:
            core = f"{epsilon_id}__{event['event_id']}__{base_id}__primary24"
            job_key = core if stratum == "full" else f"TOP__{core}"
            rows.append(
                {
                    "schedule_key": f"{stratum.upper()}__{core}",
                    "stratum": stratum,
                    "job_key": job_key,
                    "profile": "primary24",
                    "epsilon_id": epsilon_id,
                    "event_id": event["event_id"],
                    "seed": int(event["seed"]),
                    "base_argument_id": base_id,
                }
            )
    return rows


def build_schedule(
    config: dict[str, Any], manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    events = {int(row["seed"]): row for row in config["events"]}
    full_seeds = [int(value) for value in manifest["fresh_full_scramble_seeds"]]
    topological_seeds = [
        int(value) for value in manifest["fresh_topological_scramble_seeds"]
    ]
    groups: list[tuple[str, int]] = []
    for index, full_seed in enumerate(full_seeds):
        groups.append(("full", full_seed))
        if index < len(topological_seeds):
            groups.append(("topological", topological_seeds[index]))
    groups.extend(
        ("topological", seed) for seed in topological_seeds[len(full_seeds) :]
    )
    jobs: list[dict[str, Any]] = []
    for stratum, seed in groups:
        jobs.extend(event_jobs(events[seed], stratum, manifest))
    return jobs


def output_path(run_directory: Path, job: dict[str, Any]) -> Path:
    directory = "jobs" if job["stratum"] == "full" else "topological-jobs"
    return run_directory / directory / f"{job['job_key']}.json"


def cached_result(
    run_directory: Path, config: dict[str, Any], job: dict[str, Any]
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


def execute_topological(
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
    previous_event = M5077.CURRENT_EVENT
    previous_argument = M5077.CURRENT_ARGUMENT
    try:
        topology, topology_path, topology_runtime = manager.obtain(
            job["event_id"], job["epsilon_id"], job["base_argument_id"]
        )
        target = M5077.M5036.complex_from_row(argument["target_cosine"])
        M5077.CURRENT_EVENT = event
        M5077.CURRENT_ARGUMENT = argument
        module = M5077.M5036.N5030
        M5077.M5036.M5035.M5034.configure(event, target)
        profile = config["tiers"]["primary24"]
        previous_catalog = module.chamber_residue_catalog
        previous_global_value = module.global_chamber_value
        previous_job = M5077.M5036.MREPAIR.CURRENT_JOB
        module.chamber_residue_catalog = certified_5212_catalog
        M5077.M5036.MREPAIR.CURRENT_JOB = job["job_key"]
        M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
        M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
        M5077.OUTWARD_CONTOUR_AUDIT.clear()
        M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
        SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT.clear()
        M5077.removable_extension_gate()
        extension = M5077.M5085.CertifiedRemovableGlobalExtension(
            previous_global_value
        )
        module.global_chamber_value = extension
        kernel_started = time.monotonic()
        try:
            (
                raw_topological,
                residues_stable,
                catalog_rows,
                safe_pair_count,
                unsafe_pair_count,
            ) = M5124.reciprocal_reduced_topological_value(
                module, topology, profile
            )
        finally:
            module.chamber_residue_catalog = previous_catalog
            module.global_chamber_value = previous_global_value
            M5077.M5036.MREPAIR.CURRENT_JOB = previous_job
        kernel_runtime = time.monotonic() - kernel_started
        crossing_count = sum(
            len(chamber["surface_crossings"]) for chamber in topology["chambers"]
        )
        pair_coverage = (
            2 * (safe_pair_count + unsafe_pair_count) == crossing_count
        )
        normalized = M5124.KERNEL_MULTIPLIER * raw_topological
        converged = bool(
            residues_stable and pair_coverage and finite_complex(normalized)
        )
        result = {
            "checkpoint_marker": MARKER,
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
            "catalog_row_count": catalog_rows,
            "raw_topological_correction": complex_row(raw_topological),
            "normalized_topological_D_hhh_over_G3": complex_row(normalized),
            "topology_file": str(topology_path),
            "topology_runtime_seconds": topology_runtime,
            "kernel_runtime_seconds": kernel_runtime,
            "job_runtime_seconds": time.monotonic() - started,
            "residue_radius_adjustment_count": len(
                M5077.M5036.MREPAIR.RADIUS_AUDIT
            ),
            "event_local_residue_resolution_count": len(
                M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT
            ),
            "source_separated_cluster_zero_count": len(
                SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT
            ),
            "source_separated_cluster_zero_rows": list(
                SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT
            ),
            "outward_contour_repair_count": len(
                M5077.OUTWARD_CONTOUR_AUDIT
            ),
            "removable_global_collision_extension_count": len(extension.calls),
            "resumed_from_cache": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    except Exception as error:
        result = {
            "checkpoint_marker": MARKER,
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
        M5077.CURRENT_EVENT = previous_event
        M5077.CURRENT_ARGUMENT = previous_argument
    atomic_json(output, result)
    return result


def execute_job(
    run_directory: Path,
    config: dict[str, Any],
    manager: Any,
    job: dict[str, Any],
) -> dict[str, Any]:
    SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT.clear()
    if job["stratum"] == "full":
        runner_job = {
            key: job[key]
            for key in (
                "job_key",
                "profile",
                "epsilon_id",
                "event_id",
                "base_argument_id",
            )
        }
        result = M5077.execute_kernel(
            run_directory, config, manager, runner_job
        )
        if (
            SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT
            and not result.get("resumed_from_cache")
        ):
            result["source_separated_cluster_zero_count"] = len(
                SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT
            )
            result["source_separated_cluster_zero_rows"] = list(
                SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT
            )
            atomic_json(output_path(run_directory, job), result)
        return result
    return execute_topological(run_directory, config, manager, job)


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
        elif row.get("status") == "COMPLETED_CONVERGED":
            counts["completed_converged"] += 1
        elif row.get("status") == "COMPLETED_UNCONVERGED":
            counts["completed_unconverged"] += 1
        elif row.get("status") == "FAILED":
            counts["failed"] += 1
        else:
            counts["missing"] += 1
    return counts


def runtime_repair_summary(
    run_directory: Path,
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    source_jobs = {"full": 0, "topological": 0}
    source_rows = {"full": 0, "topological": 0}
    adaptive_jobs = {"full": 0, "topological": 0}
    adaptive_calls = {"full": 0, "topological": 0}
    certificates: list[dict[str, Any]] = []
    for job in jobs:
        path = output_path(run_directory, job)
        if not path.exists():
            continue
        row = read_json(path)
        if row.get("config_digest") != config["config_digest"]:
            continue
        stratum = str(job["stratum"])
        source_count = int(row.get("source_separated_cluster_zero_count", 0))
        if source_count:
            source_jobs[stratum] += 1
            source_rows[stratum] += source_count
            certificates.extend(
                row.get("source_separated_cluster_zero_rows", [])
            )
        if stratum == "full":
            adaptive_count = int(
                row.get("profile_audit", {}).get(
                    "removable_global_collision_extension_count", 0
                )
            )
        else:
            adaptive_count = int(
                row.get("removable_global_collision_extension_count", 0)
            )
        if adaptive_count:
            adaptive_jobs[stratum] += 1
            adaptive_calls[stratum] += adaptive_count
    gate_hash = digest(GATE_5213)
    return {
        "source_separated_cluster_zero_jobs": source_jobs,
        "source_separated_cluster_zero_rows": source_rows,
        "source_separated_cluster_zero_total_rows": sum(
            source_rows.values()
        ),
        "adaptive_removable_extension_jobs": adaptive_jobs,
        "adaptive_removable_extension_calls": adaptive_calls,
        "adaptive_removable_extension_total_calls": sum(
            adaptive_calls.values()
        ),
        "all_source_separated_certificates_passed": all(
            bool(row.get("certificate", {}).get("passed"))
            for row in certificates
        ),
        "all_source_separated_gate_hashes_current": all(
            row.get("gate_sha256") == gate_hash for row in certificates
        ),
        "source_separated_gate_sha256": gate_hash,
    }


def event_complete(
    run_directory: Path,
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    stratum: str,
    seed: int,
) -> bool:
    selected = [
        job
        for job in jobs
        if job["stratum"] == stratum and int(job["seed"]) == seed
    ]
    return bool(selected) and all(
        (
            path := output_path(run_directory, job)
        ).exists()
        and read_json(path).get("config_digest") == config["config_digest"]
        and read_json(path).get("status") == "COMPLETED_CONVERGED"
        for job in selected
    )


def projected_event(
    run_directory: Path,
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    stratum: str,
    seed: int,
) -> dict[str, Any]:
    event = next(row for row in config["events"] if int(row["seed"]) == seed)
    argument_lookup = {
        round(float(row["argument"]), 12): row["argument_id"]
        for row in config["base_arguments"]
    }
    selected_jobs = {
        (job["epsilon_id"], job["base_argument_id"]): job
        for job in jobs
        if job["stratum"] == stratum and int(job["seed"]) == seed
    }
    runtime = sum(
        float(read_json(output_path(run_directory, job))["job_runtime_seconds"])
        for job in selected_jobs.values()
    )

    def components(epsilon_id: str, argument: float) -> dict[str, complex]:
        base_id = argument_lookup[round(float(argument), 12)]
        job = selected_jobs[(epsilon_id, base_id)]
        row = read_json(output_path(run_directory, job))
        if stratum == "full":
            kernel_path = Path(row["kernel_file"])
            values, closure = M5124.split_kernel(kernel_path)
            if closure > 1.0e-8:
                raise RuntimeError(f"component closure failed for {kernel_path}")
            return {key: values[key] for key in COMPONENTS}
        value = row_complex(row["normalized_topological_D_hhh_over_G3"])
        return {"topological": value}

    def extrapolated(argument: float) -> dict[str, complex]:
        e040 = components("E040", argument)
        e020 = components("E020", argument)
        return {key: 2.0 * e020[key] - e040[key] for key in e020}

    cyclic: dict[str, list[complex]] = {}
    for cosine in PHYSICAL_COSINES:
        t_ratio = -(1.0 - cosine) / 2.0
        u_ratio = -(1.0 + cosine) / 2.0
        z_t = (3.0 + cosine) / (1.0 - cosine)
        z_u = -(3.0 - cosine) / (1.0 + cosine)
        t_values = extrapolated(float(z_t))
        u_values = extrapolated(float(z_u))
        for key in t_values:
            cyclic.setdefault(key, []).append(
                t_ratio**3 * t_values[key] + u_ratio**3 * u_values[key]
            )
    shape = 1.0 - PHYSICAL_COSINES**2
    weights = shape / float(shape @ shape)
    arrays = {
        key: np.asarray(values, dtype=np.complex128)
        for key, values in cyclic.items()
    }
    local = {
        key: complex(weights @ values) for key, values in arrays.items()
    }
    return {
        "stratum": stratum,
        "seed": seed,
        "event_id": event["event_id"],
        "runtime_seconds": runtime,
        "cyclic": arrays,
        "local": local,
    }


def physical_samples_5123() -> np.ndarray:
    rows: dict[int, dict[float, float]] = {}
    with PHYSICAL_ROWS_5123.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if (
                row["status"] != "PHYSICAL_ANGULAR_FIRST_SEED"
                or int(row["sample_power"]) != 13
                or int(row["gauss_order"]) != 20
            ):
                continue
            rows.setdefault(int(row["seed"]), {})[
                round(float(row["physical_cosine"]), 12)
            ] = float(row["even_symmetrized_D_real"])
    samples = [
        [
            values[round(float(cosine), 12)]
            for cosine in PHYSICAL_COSINES
        ]
        for _, values in sorted(rows.items())
    ]
    result = np.asarray(samples, dtype=np.float64)
    if result.shape != (8, 5):
        raise RuntimeError(f"unexpected 5123 physical sample shape {result.shape}")
    return result


def covariance_of_mean(values: np.ndarray) -> np.ndarray:
    return np.atleast_2d(np.cov(values, rowvar=False, ddof=1)) / len(values)


def complex_sample_summary(values: np.ndarray) -> dict[str, Any]:
    count = len(values)
    mean = complex(np.mean(values)) if count else 0.0j
    real_error = (
        float(np.std(values.real, ddof=1) / math.sqrt(count))
        if count >= 2
        else None
    )
    imaginary_error = (
        float(np.std(values.imag, ddof=1) / math.sqrt(count))
        if count >= 2
        else None
    )
    return {
        "count": count,
        "mean": complex_row(mean),
        "real_standard_error": real_error,
        "imaginary_standard_error": imaginary_error,
    }


def scalar_distribution_diagnostics(
    values: np.ndarray, seeds: list[int]
) -> dict[str, Any]:
    array = np.asarray(values, dtype=np.float64)
    count = len(array)
    if count != len(seeds) or count < 2:
        raise ValueError("distribution diagnostics require matched seeds and n>=2")
    mean = float(np.mean(array))
    sample_standard_deviation = float(np.std(array, ddof=1))
    standard_error = sample_standard_deviation / math.sqrt(count)
    median = float(np.median(array))
    median_absolute_deviation = float(np.median(np.abs(array - median)))
    population_standard_deviation = float(np.std(array))
    if population_standard_deviation > 0.0:
        standardized = (array - mean) / population_standard_deviation
        skewness = float(np.mean(standardized**3))
        excess_kurtosis = float(np.mean(standardized**4) - 3.0)
    else:
        skewness = 0.0
        excess_kurtosis = -3.0
    absolute_total = float(np.sum(np.abs(array)))
    leave_one_out = np.asarray(
        [(float(np.sum(array)) - value) / (count - 1) for value in array],
        dtype=np.float64,
    )
    sorted_values = np.sort(array)
    trim_count = 1 if count >= 10 else 0
    trimmed = (
        sorted_values[trim_count:-trim_count]
        if trim_count
        else sorted_values
    )
    if trim_count:
        winsorized = sorted_values.copy()
        winsorized[:trim_count] = sorted_values[trim_count]
        winsorized[-trim_count:] = sorted_values[-trim_count - 1]
    else:
        winsorized = sorted_values
    half = count // 2
    first = array[:half]
    second = array[half:]
    half_difference = float(np.mean(first) - np.mean(second))
    half_difference_error = math.sqrt(
        float(np.var(first, ddof=1) / len(first))
        + float(np.var(second, ddof=1) / len(second))
    )
    ranking = np.argsort(np.abs(array))[::-1]
    return {
        "count": count,
        "mean": mean,
        "sample_standard_deviation": sample_standard_deviation,
        "standard_error": standard_error,
        "mean_to_standard_error": abs(mean)
        / max(standard_error, 1.0e-300),
        "median": median,
        "median_absolute_deviation": median_absolute_deviation,
        "scaled_median_absolute_deviation": 1.4826
        * median_absolute_deviation,
        "mean_minus_median_in_standard_errors": abs(mean - median)
        / max(standard_error, 1.0e-300),
        "minimum": float(np.min(array)),
        "maximum": float(np.max(array)),
        "quantiles": {
            "q05": float(np.quantile(array, 0.05)),
            "q25": float(np.quantile(array, 0.25)),
            "q75": float(np.quantile(array, 0.75)),
            "q95": float(np.quantile(array, 0.95)),
        },
        "skewness": skewness,
        "excess_kurtosis": excess_kurtosis,
        "maximum_absolute_event_share": float(np.max(np.abs(array)))
        / max(absolute_total, 1.0e-300),
        "leave_one_out_mean_minimum": float(np.min(leave_one_out)),
        "leave_one_out_mean_maximum": float(np.max(leave_one_out)),
        "maximum_leave_one_out_shift_standard_errors": float(
            np.max(np.abs(leave_one_out - mean))
        )
        / max(standard_error, 1.0e-300),
        "ten_percent_trimmed_mean": float(np.mean(trimmed)),
        "ten_percent_winsorized_mean": float(np.mean(winsorized)),
        "ordered_half_means": {
            "first": float(np.mean(first)),
            "second": float(np.mean(second)),
            "difference": half_difference,
            "difference_standard_error": half_difference_error,
            "difference_sigma": abs(half_difference)
            / max(half_difference_error, 1.0e-300),
        },
        "largest_absolute_events": [
            {"seed": int(seeds[index]), "value": float(array[index])}
            for index in ranking[: min(4, count)]
        ],
    }


def event_rows(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in events:
        row: dict[str, Any] = {
            "stratum": event["stratum"],
            "seed": event["seed"],
            "event_id": event["event_id"],
            "runtime_seconds": event["runtime_seconds"],
            "status": "COMPLETE_EVENT_ESTIMATE",
            "checkpoint_marker": MARKER,
            "valid_for_numeric_UV_claim": False,
        }
        for key, value in event["local"].items():
            row[f"{key}_local_real"] = value.real
            row[f"{key}_local_imaginary"] = value.imag
        for key, values in event["cyclic"].items():
            for index, cosine in enumerate(PHYSICAL_COSINES):
                label = f"z{cosine:+.1f}".replace("+", "p").replace("-", "m").replace(".", "p")
                row[f"{key}_{label}_real"] = values[index].real
                row[f"{key}_{label}_imaginary"] = values[index].imag
        rows.append(row)
    return rows


def analyse(
    run_directory: Path,
    config: dict[str, Any],
    manifest: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    completed: list[dict[str, Any]] = []
    for stratum, seeds in (
        ("full", manifest["fresh_full_scramble_seeds"]),
        ("topological", manifest["fresh_topological_scramble_seeds"]),
    ):
        for seed_value in seeds:
            seed = int(seed_value)
            if event_complete(
                run_directory, config, jobs, stratum, seed
            ):
                completed.append(
                    projected_event(
                        run_directory, config, jobs, stratum, seed
                    )
                )
    rows = event_rows(completed)
    full = [row for row in completed if row["stratum"] == "full"]
    topological = [
        row for row in completed if row["stratum"] == "topological"
    ]
    counts = run_counts(run_directory, config, jobs)
    repairs = runtime_repair_summary(run_directory, config, jobs)
    analysis: dict[str, Any] = {
        "complete_full_events": len(full),
        "expected_full_events": len(manifest["fresh_full_scramble_seeds"]),
        "complete_topological_events": len(topological),
        "expected_topological_events": len(
            manifest["fresh_topological_scramble_seeds"]
        ),
        "full_matrix_complete": (
            len(full) == len(manifest["fresh_full_scramble_seeds"])
        ),
        "topological_matrix_complete": (
            len(topological)
            == len(manifest["fresh_topological_scramble_seeds"])
        ),
        "independent_stratified_estimate_available": False,
        "runtime_repair_summary": repairs,
        "pilot_only": True,
        "numeric_UV_coefficient_complete": False,
        "valid_for_numeric_UV_claim": False,
    }
    if full:
        analysis["paired_full_local"] = complex_sample_summary(
            np.asarray(
                [row["local"]["total"] for row in full],
                dtype=np.complex128,
            )
        )
        analysis["full_naive_local"] = complex_sample_summary(
            np.asarray(
                [row["local"]["naive"] for row in full],
                dtype=np.complex128,
            )
        )
        analysis["mean_full_event_runtime_seconds"] = float(
            np.mean([row["runtime_seconds"] for row in full])
        )
    if topological:
        analysis["independent_topological_local"] = complex_sample_summary(
            np.asarray(
                [row["local"]["topological"] for row in topological],
                dtype=np.complex128,
            )
        )
        analysis["mean_topological_event_runtime_seconds"] = float(
            np.mean([row["runtime_seconds"] for row in topological])
        )
    if len(full) < 2 or len(topological) < 2:
        analysis["remaining_action"] = (
            "resume until at least two complete events exist in both strata"
        )
        return analysis, rows

    naive_local = np.asarray(
        [row["local"]["naive"] for row in full], dtype=np.complex128
    )
    paired_local = np.asarray(
        [row["local"]["total"] for row in full], dtype=np.complex128
    )
    top_local = np.asarray(
        [row["local"]["topological"] for row in topological],
        dtype=np.complex128,
    )
    topological_seeds = [int(row["seed"]) for row in topological]
    topological_distribution = {
        "real": scalar_distribution_diagnostics(
            top_local.real, topological_seeds
        ),
        "imaginary": scalar_distribution_diagnostics(
            top_local.imag, topological_seeds
        ),
    }
    crossed_local = complex(np.mean(naive_local) + np.mean(top_local))
    crossed_real_variance = float(
        np.var(naive_local.real, ddof=1) / len(naive_local)
        + np.var(top_local.real, ddof=1) / len(top_local)
    )
    crossed_imaginary_variance = float(
        np.var(naive_local.imag, ddof=1) / len(naive_local)
        + np.var(top_local.imag, ddof=1) / len(top_local)
    )

    physical_samples = physical_samples_5123()
    shape = 1.0 - PHYSICAL_COSINES**2
    weights = shape / float(shape @ shape)
    physical_local_samples = physical_samples @ weights
    physical_local = float(np.mean(physical_local_samples))
    physical_local_variance = float(
        np.var(physical_local_samples, ddof=1) / len(physical_local_samples)
    )
    hhh_local = physical_local + crossed_local
    hhh_real_error = math.sqrt(
        physical_local_variance + crossed_real_variance
    )
    hhh_imaginary_error = math.sqrt(crossed_imaginary_variance)
    full_master = KNOWN_MASTER_LOCAL_COEFFICIENT + 2.0 * hhh_local
    k_mu = -4.0 * full_master
    k_mu_real_error = 8.0 * hhh_real_error
    k_mu_imaginary_error = 8.0 * hhh_imaginary_error

    naive_cyclic = np.asarray(
        [row["cyclic"]["naive"] for row in full], dtype=np.complex128
    )
    top_cyclic = np.asarray(
        [row["cyclic"]["topological"] for row in topological],
        dtype=np.complex128,
    )
    angle_diagnostics = [
        {
            "physical_cosine": float(cosine),
            "real": scalar_distribution_diagnostics(
                top_cyclic[:, index].real, topological_seeds
            ),
            "imaginary": scalar_distribution_diagnostics(
                top_cyclic[:, index].imag, topological_seeds
            ),
        }
        for index, cosine in enumerate(PHYSICAL_COSINES)
    ]
    dominant_real_angle = max(
        angle_diagnostics,
        key=lambda row: float(row["real"]["sample_standard_deviation"]),
    )
    crossed_cyclic = np.mean(naive_cyclic, axis=0) + np.mean(
        top_cyclic, axis=0
    )
    real_covariance = (
        covariance_of_mean(naive_cyclic.real)
        + covariance_of_mean(top_cyclic.real)
        + covariance_of_mean(physical_samples)
    )
    imaginary_covariance = (
        covariance_of_mean(naive_cyclic.imag)
        + covariance_of_mean(top_cyclic.imag)
    )
    hybrid_cyclic = np.mean(physical_samples, axis=0) + crossed_cyclic
    projector = np.eye(len(shape)) - np.outer(shape, weights)
    nonlocal_value = projector @ hybrid_cyclic
    nonlocal_real_covariance = projector @ real_covariance @ projector.T
    target = np.asarray(
        read_json(TARGET_5018)["target"]["required_hhh_nonlocal"],
        dtype=np.float64,
    )
    mismatch = nonlocal_value.real - target
    mismatch_error = np.sqrt(
        np.maximum(np.diag(nonlocal_real_covariance), 0.0)
    )
    maximum_mismatch_sigma = float(
        np.max(np.abs(mismatch) / np.maximum(mismatch_error, 1.0e-30))
    )

    full_cost = float(np.mean([row["runtime_seconds"] for row in full]))
    topological_cost = float(
        np.mean([row["runtime_seconds"] for row in topological])
    )
    total_cost = len(full) * full_cost + len(topological) * topological_cost
    equivalent_paired_events = total_cost / max(full_cost, 1.0e-30)
    efficiency: dict[str, Any] = {}
    for part in ("real", "imaginary"):
        naive_values = (
            naive_local.real if part == "real" else naive_local.imag
        )
        top_values = top_local.real if part == "real" else top_local.imag
        paired_values = (
            paired_local.real if part == "real" else paired_local.imag
        )
        stratified_variance = float(
            np.var(naive_values, ddof=1) / len(naive_values)
            + np.var(top_values, ddof=1) / len(top_values)
        )
        equal_cost_paired_variance = float(
            np.var(paired_values, ddof=1)
            / max(equivalent_paired_events, 1.0)
        )
        efficiency[part] = {
            "stratified_mean_variance": stratified_variance,
            "equal_cost_paired_mean_variance": equal_cost_paired_variance,
            "realized_equal_cost_speedup": (
                equal_cost_paired_variance
                / max(stratified_variance, 1.0e-300)
            ),
        }

    matrix_complete = bool(
        analysis["full_matrix_complete"]
        and analysis["topological_matrix_complete"]
        and counts["failed"] == 0
        and counts["completed_unconverged"] == 0
    )
    precision_gate = bool(
        k_mu_real_error <= 0.2 * max(abs(k_mu.real), 1.0)
        and abs(k_mu.imag) <= 3.0 * max(k_mu_imaginary_error, 1.0e-30)
        and maximum_mismatch_sigma <= 4.0
    )
    real_distribution = topological_distribution["real"]
    imaginary_distribution = topological_distribution["imaginary"]
    tail_convergence_demonstrated = bool(
        len(topological) >= 30
        and real_distribution[
            "maximum_leave_one_out_shift_standard_errors"
        ]
        <= 0.5
        and real_distribution["ordered_half_means"]["difference_sigma"]
        <= 1.0
        and real_distribution["maximum_absolute_event_share"] <= 0.2
    )
    estimator_decision = {
        "real_equal_cost_efficiency_gain": efficiency["real"][
            "realized_equal_cost_speedup"
        ]
        > 1.0,
        "imaginary_equal_cost_efficiency_gain": efficiency["imaginary"][
            "realized_equal_cost_speedup"
        ]
        > 1.0,
        "real_mean_resolved_at_two_sigma": real_distribution[
            "mean_to_standard_error"
        ]
        >= 2.0,
        "imaginary_mean_consistent_with_zero_at_three_sigma": (
            imaginary_distribution["mean_to_standard_error"] <= 3.0
        ),
        "delete_one_real_mean_stable_within_one_standard_error": (
            real_distribution[
                "maximum_leave_one_out_shift_standard_errors"
            ]
            <= 1.0
        ),
        "ordered_half_real_means_agree_within_two_sigma": (
            real_distribution["ordered_half_means"]["difference_sigma"]
            <= 2.0
        ),
        "tail_convergence_demonstrated": tail_convergence_demonstrated,
        "coefficient_precision_gate": precision_gate,
        "blind_scaled_sampling_authorized": False,
        "selected_next_route": (
            "derive an analytic control variate for the dominant A00/"
            "z=-0.6 topological residue family before buying more events"
        ),
        "interpretation": (
            "The complete pilot establishes finite broad variance, not a "
            "stable numeric UV coefficient. Its real equal-cost efficiency "
            "is below one and twelve events cannot establish tail convergence."
        ),
    }
    analysis.update(
        {
            "independent_stratified_estimate_available": True,
            "crossed_local_coefficient": {
                "value": complex_row(crossed_local),
                "real_standard_error": math.sqrt(crossed_real_variance),
                "imaginary_standard_error": math.sqrt(
                    crossed_imaginary_variance
                ),
            },
            "physical_local_coefficient": {
                "value": physical_local,
                "standard_error": math.sqrt(physical_local_variance),
            },
            "hhh_local_coefficient": {
                "value": complex_row(hhh_local),
                "real_standard_error": hhh_real_error,
                "imaginary_standard_error": hhh_imaginary_error,
            },
            "candidate_K_mu": {
                "value": complex_row(k_mu),
                "real_standard_error": k_mu_real_error,
                "imaginary_standard_error": k_mu_imaginary_error,
            },
            "maximum_nonlocal_mismatch_sigma": maximum_mismatch_sigma,
            "topological_distribution_diagnostics": (
                topological_distribution
            ),
            "topological_angle_diagnostics": angle_diagnostics,
            "dominant_real_variance_angle": {
                "physical_cosine": dominant_real_angle[
                    "physical_cosine"
                ],
                "sample_standard_deviation": dominant_real_angle["real"][
                    "sample_standard_deviation"
                ],
                "largest_absolute_events": dominant_real_angle["real"][
                    "largest_absolute_events"
                ],
            },
            "realized_efficiency": efficiency,
            "estimator_decision": estimator_decision,
            "pilot_matrix_complete": matrix_complete,
            "coefficient_precision_gate": precision_gate,
            "numeric_UV_coefficient_complete": False,
            "valid_for_numeric_UV_claim": False,
            "remaining_action": (
                "derive an analytic control variate for the dominant "
                "A00/z=-0.6 topological residue family; do not scale the "
                "current estimator blindly"
            ),
        }
    )
    return analysis, rows


def activation_record(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    old_manifest = read_json(LOCKED_MANIFEST_5076)
    old_seeds = {
        *[int(value) for value in old_manifest["fresh_high_scramble_seeds"]],
        *[int(value) for value in old_manifest["fresh_low_scramble_seeds"]],
    }
    full = {int(value) for value in manifest["fresh_full_scramble_seeds"]}
    topological = {
        int(value) for value in manifest["fresh_topological_scramble_seeds"]
    }
    expected_jobs = (
        len(full) + len(topological)
    ) * len(manifest["epsilon_ids"]) * len(
        manifest["required_base_argument_ids"]
    )
    base_ids = {row["argument_id"] for row in config["base_arguments"]}
    prerequisites = {
        "all_source_paths_exist": all(
            path.exists()
            for path in (
                SCRIPT_5077,
                SCRIPT_5123,
                SCRIPT_5124,
                SCRIPT_5213,
                CHECKPOINT_4987,
                CHECKPOINT_5123,
                CHECKPOINT_5124,
                CHECKPOINT_5213,
                MANIFEST,
                DESIGN_5124,
                PHYSICAL_ROWS_5123,
                TARGET_5018,
                LOCKED_MANIFEST_5076,
                GATE_5213,
            )
        ),
        "allocation_locked_before_outcomes": bool(
            manifest["allocation_locked_before_fresh_outcomes"]
        ),
        "fresh_seeds_disjoint_from_5076": not bool(
            (full | topological) & old_seeds
        ),
        "strata_seed_sets_disjoint": not bool(full & topological),
        "declared_counts_match": (
            len(full) == int(manifest["full_event_count"])
            and len(topological)
            == int(manifest["topological_event_count"])
        ),
        "allocation_ratio_matches": math.isclose(
            len(topological) / len(full),
            float(manifest["topological_per_full_ratio"]),
        ),
        "required_arguments_exist": set(
            manifest["required_base_argument_ids"]
        ).issubset(base_ids),
        "schedule_count_matches": len(jobs) == expected_jobs,
        "all_jobs_primary24": all(
            job["profile"] == "primary24" for job in jobs
        ),
        "pole_and_smooth_remain_paired": bool(
            manifest["pole_model_and_smooth_must_remain_paired"]
        ),
        "unsafe_pairs_fail_closed": bool(
            manifest["unsafe_reciprocal_pairs_evaluate_both_roots"]
        ),
        "adaptive_removable_extension_is_refinement_not_threshold_relaxation": (
            config["adaptive_removable_extension_policy"]["threshold_relaxed"]
            is False
            and config["adaptive_removable_extension_policy"][
                "failure_action"
            ]
            == "fail closed"
        ),
        "wall_cap_is_four_hours": math.isclose(
            float(manifest["maximum_wall_hours_per_invocation"]),
            MAXIMUM_WALL_HOURS,
        ),
        "pilot_is_nonclaim": bool(manifest["pilot_only"])
        and not bool(manifest["valid_for_numeric_UV_claim"]),
    }
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "manifest": relative(MANIFEST),
        "manifest_sha256": digest(MANIFEST),
        "config_digest": config["config_digest"],
        "schedule_digest": M5077.M5036.canonical_digest(jobs),
        "expected_job_count": expected_jobs,
        "expected_full_job_count": len(full)
        * len(manifest["epsilon_ids"])
        * len(manifest["required_base_argument_ids"]),
        "expected_topological_job_count": len(topological)
        * len(manifest["epsilon_ids"])
        * len(manifest["required_base_argument_ids"]),
        "prerequisites": prerequisites,
        "execution_authorized": all(prerequisites.values()),
        "default_enabled": False,
        "stop_on_first_failed_or_unconverged_job": True,
        "resume_completed_converged_jobs": True,
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def validation_rows(
    activation: dict[str, Any],
    counts: dict[str, int] | None,
    analysis: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    cluster_gate = source_separated_cluster_gate()
    checks: list[tuple[str, bool, str]] = [
        (
            "activation_prerequisites_complete",
            all(activation["prerequisites"].values()),
            json.dumps(activation["prerequisites"], sort_keys=True),
        ),
        (
            "formalization_unchanged",
            activation["formalization_workbench_tree_sha256"]
            == FORMAL_BASELINE,
            activation["formalization_workbench_tree_sha256"],
        ),
        (
            "manifest_and_schedule_locked",
            bool(activation["manifest_sha256"])
            and bool(activation["schedule_digest"]),
            f"{activation['manifest_sha256']} {activation['schedule_digest']}",
        ),
        (
            "execution_default_off",
            not activation["default_enabled"],
            "explicit --mode run required",
        ),
        (
            "claim_discipline",
            not activation["valid_for_numeric_UV_claim"]
            and not activation["valid_for_local_GR_claim"]
            and not activation["valid_for_full_MTS_claim"],
            "pilot activation is not a coefficient or theory claim",
        ),
        (
            "source_separated_cluster_zero_gate_accepted",
            bool(cluster_gate["passed"])
            and bool(cluster_gate["runner_integration_authorized"]),
            digest(GATE_5213),
        ),
        (
            "source_separated_cluster_zero_is_guarded_nonclaim",
            not cluster_gate["valid_for_numeric_UV_claim"]
            and not cluster_gate["valid_for_local_GR_claim"]
            and not cluster_gate["valid_for_full_MTS_claim"],
            cluster_gate["authorized_scope"],
        ),
    ]
    if counts is not None:
        checks.extend(
            [
                (
                    "no_failed_jobs",
                    counts["failed"] == 0,
                    str(counts),
                ),
                (
                    "no_unconverged_jobs",
                    counts["completed_unconverged"] == 0,
                    str(counts),
                ),
                (
                    "run_count_closure",
                    sum(counts.values())
                    == activation["expected_job_count"],
                    str(counts),
                ),
            ]
        )
    if analysis is not None:
        checks.extend(
            [
                (
                    "partial_result_cannot_claim",
                    (
                        analysis["full_matrix_complete"]
                        and analysis["topological_matrix_complete"]
                    )
                    or not analysis["valid_for_numeric_UV_claim"],
                    json.dumps(
                        {
                            "full": analysis["complete_full_events"],
                            "topological": analysis[
                                "complete_topological_events"
                            ],
                            "claim": analysis[
                                "valid_for_numeric_UV_claim"
                            ],
                        },
                        sort_keys=True,
                    ),
                ),
                (
                    "pilot_remains_nonclaim",
                    not analysis["numeric_UV_coefficient_complete"]
                    and not analysis["valid_for_numeric_UV_claim"],
                    "tail convergence and complete K_mu cut closure are not promoted",
                ),
            ]
        )
        if analysis.get("pilot_matrix_complete"):
            decision = analysis["estimator_decision"]
            repairs = analysis["runtime_repair_summary"]
            checks.extend(
                [
                    (
                        "complete_pilot_matrix_recorded",
                        analysis["complete_full_events"] == 2
                        and analysis["complete_topological_events"] == 12,
                        json.dumps(
                            {
                                "full": analysis["complete_full_events"],
                                "topological": analysis[
                                    "complete_topological_events"
                                ],
                            }
                        ),
                    ),
                    (
                        "real_efficiency_failure_not_promoted",
                        not decision["real_equal_cost_efficiency_gain"]
                        and not analysis["valid_for_numeric_UV_claim"],
                        str(
                            analysis["realized_efficiency"]["real"][
                                "realized_equal_cost_speedup"
                            ]
                        ),
                    ),
                    (
                        "tail_convergence_failure_not_promoted",
                        not decision["tail_convergence_demonstrated"]
                        and not decision["blind_scaled_sampling_authorized"],
                        decision["selected_next_route"],
                    ),
                    (
                        "runtime_repairs_are_fully_certified",
                        repairs[
                            "all_source_separated_certificates_passed"
                        ]
                        and repairs[
                            "all_source_separated_gate_hashes_current"
                        ],
                        json.dumps(
                            {
                                "source_zero_rows": repairs[
                                    "source_separated_cluster_zero_total_rows"
                                ],
                                "adaptive_calls": repairs[
                                    "adaptive_removable_extension_total_calls"
                                ],
                            }
                        ),
                    ),
                ]
            )
    return [
        {
            "check_id": f"VAL5212_{index:02d}_{name}",
            "check": name,
            "passed": passed,
            "detail": detail,
            "status": "PASS" if passed else "FAIL",
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]


def write_provenance(
    activation: dict[str, Any], run_id: str, state: str
) -> None:
    paths = (
        Path(__file__),
        SCRIPT_5077,
        SCRIPT_5123,
        SCRIPT_5124,
        SCRIPT_5213,
        CHECKPOINT_4987,
        CHECKPOINT_5123,
        CHECKPOINT_5124,
        CHECKPOINT_5213,
        MANIFEST,
        DESIGN_5124,
        PHYSICAL_ROWS_5123,
        TARGET_5018,
        LOCKED_MANIFEST_5076,
        GATE_5213,
        M5213.HISTORICAL_FALSIFICATION,
    )
    lines = [
        "# 5212 provenance",
        "",
        f"- Marker: `{MARKER}`",
        f"- Checked: `{CHECKED_DATE}`",
        f"- Run id: `{run_id}`",
        f"- Current state: `{state}`",
        f"- Manifest digest: `{activation['manifest_sha256']}`",
        f"- Schedule digest: `{activation['schedule_digest']}`",
        "- Fresh full and topological seeds were fixed before any 5212 numerical outcome.",
        "- The full stratum keeps pole-model and smooth terms paired as one naive contribution.",
        "- The topological stratum uses one residue for each safe reciprocal pair and both residues for every unsafe pair.",
        "- A failed fixed-grid 5085 removable limit may use adaptive symmetric Richardson refinement; the acceptance tolerance and collision scope are unchanged.",
        "- A numerically unstable residue is replaced by zero only when the 5213 source-separated additive-cluster Cauchy guard passes in full; same-summand and g3/soft-alias rows remain excluded.",
        "- No outlier deletion, target fitting, equation retuning, local-GR claim, or GitHub action is permitted.",
        "",
        "## Source locks",
        "",
    ]
    for path in paths:
        lines.append(f"- `{relative(path)}` — `{digest(path)}`")
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_document(result: dict[str, Any]) -> None:
    analysis = result.get("analysis", {})
    estimate = analysis.get("candidate_K_mu")
    if estimate is None:
        estimate_text = (
            "No independent coefficient estimate is reported yet because fewer "
            "than two complete events exist in one or both strata."
        )
    else:
        value = estimate["value"]
        estimate_text = (
            "The current independent pilot gives the non-claim candidate "
            f"`K_mu={value['real']:.10g}{value['imaginary']:+.10g} i`, "
            f"with real/imaginary standard errors "
            f"`{estimate['real_standard_error']:.6g}` and "
            f"`{estimate['imaginary_standard_error']:.6g}`. "
            f"The maximum nonlocal mismatch is "
            f"`{analysis['maximum_nonlocal_mismatch_sigma']:.6g} sigma`."
        )
    efficiency = analysis.get("realized_efficiency")
    if efficiency is None:
        efficiency_text = "Realized cost-variance efficiency is not available yet."
    else:
        efficiency_text = (
            "At the completed-event count, the realized equal-cost speedups are "
            f"`{efficiency['real']['realized_equal_cost_speedup']:.6g}` "
            f"(real) and "
            f"`{efficiency['imaginary']['realized_equal_cost_speedup']:.6g}` "
            "(imaginary)."
        )
    distribution = analysis.get("topological_distribution_diagnostics")
    if distribution is None:
        distribution_text = (
            "Robust event-distribution diagnostics are not available yet."
        )
    else:
        real = distribution["real"]
        imaginary = distribution["imaginary"]
        dominant = analysis["dominant_real_variance_angle"]
        distribution_text = (
            f"The 12-event topological real mean is `{real['mean']:.6g}` "
            f"with SE `{real['standard_error']:.6g}`, median "
            f"`{real['median']:.6g}`, one-event-trimmed mean "
            f"`{real['ten_percent_trimmed_mean']:.6g}`, and maximum "
            f"delete-one shift `{real['maximum_leave_one_out_shift_standard_errors']:.6g}` "
            "SE. The ordered half means differ by "
            f"`{real['ordered_half_means']['difference_sigma']:.6g}` sigma. "
            f"The imaginary mean is `{imaginary['mean']:.6g}` with SE "
            f"`{imaginary['standard_error']:.6g}`. The largest real variance "
            f"occurs at physical cosine `{dominant['physical_cosine']:.1f}`."
        )
    decision = analysis.get("estimator_decision")
    if decision is None:
        decision_text = (
            "The pilot has not yet selected between more sampling and an "
            "analytic control variate."
        )
    else:
        decision_text = (
            "Blind scaled sampling is not authorized. The selected next route "
            f"is to {decision['selected_next_route']}."
        )
    repairs = analysis.get("runtime_repair_summary")
    if repairs is None:
        repair_text = "Runtime repair accounting is not available yet."
    else:
        repair_text = (
            "Across the completed matrix, the source-separated theorem "
            f"certified `{repairs['source_separated_cluster_zero_total_rows']}` "
            "exact zero rows, while the adaptive removable extension was used "
            f"`{repairs['adaptive_removable_extension_total_calls']}` times. "
            "All recorded theorem certificates and gate hashes validate."
        )
    DOCUMENT.write_text(
        f"""# 5212 — fresh crossed-hhh two-stratum pilot

## Result

This checkpoint executes the calculation prescribed by checkpoint 5124 rather
than making another target inventory. It estimates the crossed `hhh`
contribution with two independent outer-event strata:

```text
E[H_crossed] = E[H_naive, full] + E[H_topological, independent].
```

The full stratum keeps `pole_model+smooth` paired. The topological stratum uses
the reciprocal residue theorem only for certified safe pairs and evaluates both
members of every unsafe pair. Fresh seeds and the 2:12 allocation were locked
before outcomes.

The fresh `E040/A10` witness exposed a fixed-grid removable-limit convergence
miss. The repair keeps the original `10^-7` acceptance threshold and collision
scope, but refines the symmetric step and checks successive Richardson limits.
This follows the even expansion of a removable holomorphic collision and still
fails closed if convergence or direction independence is not obtained.

Fresh seed `521213/A00` then exposed four unstable nested residue contours.
Checkpoint 5213 proves that all four are strict cross-additive `D-S` clusters:
the componentwise Cauchy sums are holomorphic in the relative coordinate,
their nearest same-summand singularities lie at least 4660 production contour
radii away, and the historical 601-row stable-nonzero corpus contains no
in-scope counterexample. Only rows passing that complete theorem guard are
replaced by the exact residue zero; same-summand and `g3/soft`-alias rows
remain fail-closed.

Current run state: `{result['state']}`. Completed jobs:
`{result['counts']['completed_converged']}/{result['expected_job_count']}`.
Complete full events: `{analysis.get('complete_full_events', 0)}/2`; complete
topological events: `{analysis.get('complete_topological_events', 0)}/12`.

{estimate_text}

{efficiency_text}

{distribution_text}

{decision_text}

{repair_text}

## Physics status

- Exact local GR+Maxwell truncation from checkpoint 5211 is unchanged.
- This calculation attacks the finite crossed-`hhh` motion-sector amplitude
  uncertainty that blocks the canonical `K_mu` coefficient.
- A partial or pilot matrix is not promoted to a UV coefficient measurement.
- The pilot does not by itself complete the other surviving cut classes or the
  full MTS parent action.
- Numeric UV, local-GR, galaxy-law and full-MTS claims remain false.

## Decision rule

The locked pilot is complete. Its imaginary component shows an observed
cost-variance gain, but its real component does not, the real mean is not
resolved at two standard errors, and 12 events do not establish tail
convergence. The next derivation target is therefore the dominant
`A00/z=-0.6` topological residue family and an analytic control variate, not
more blind brute-force sampling.
""",
        encoding="utf-8",
    )


def finalize(
    run_id: str,
    state: str,
    activation: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    counts: dict[str, int],
    analysis: dict[str, Any],
    rows: list[dict[str, Any]],
    elapsed_seconds: float,
) -> dict[str, Any]:
    write_csv(EVENT_ROWS_CSV, rows)
    result = {
        "checkpoint": 5212,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": run_id,
        "state": state,
        "expected_job_count": len(jobs),
        "counts": counts,
        "analysis": analysis,
        "elapsed_seconds_this_invocation": elapsed_seconds,
        "manifest_sha256": activation["manifest_sha256"],
        "schedule_digest": activation["schedule_digest"],
        "source_separated_cluster_zero_gate": relative(GATE_5213),
        "source_separated_cluster_zero_gate_sha256": digest(GATE_5213),
        "formalization_workbench_tree_sha256": activation[
            "formalization_workbench_tree_sha256"
        ],
        "numeric_UV_coefficient_complete": False,
        "local_GR_claim": False,
        "full_MTS_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    validations = validation_rows(activation, counts, analysis)
    write_csv(VALIDATION_CSV, validations)
    result["validation_all_passed"] = all(
        row["passed"] for row in validations
    )
    result["validation_check_count"] = len(validations)
    atomic_json(RESULT_JSON, result)
    write_provenance(activation, run_id, state)
    write_document(result)
    return result


def execute(
    run_id: str,
    activation: dict[str, Any],
    config: dict[str, Any],
    manifest: dict[str, Any],
    jobs: list[dict[str, Any]],
    wall_cap_hours: float,
    maximum_new_jobs: int,
) -> dict[str, Any]:
    if not activation["execution_authorized"]:
        raise RuntimeError("5212 execution prerequisites are not complete")
    if not (0.0 < wall_cap_hours <= MAXIMUM_WALL_HOURS):
        raise ValueError("wall cap must be positive and no greater than four hours")
    run_directory = RUNS / run_id
    run_directory.mkdir(parents=True, exist_ok=True)
    config_path = run_directory / "config.json"
    if config_path.exists():
        existing = read_json(config_path)
        if existing["config_digest"] != config["config_digest"]:
            raise RuntimeError("config changed; use a new run id")
    else:
        atomic_json(config_path, config)
    atomic_json(run_directory / "activation.json", activation)
    source_separated_cluster_gate()
    M5077.certified_primary_catalog = certified_5212_catalog
    M5077.M5085.CertifiedRemovableGlobalExtension = (
        AdaptiveRemovableGlobalExtension
    )
    M5077.install_history_invariant_breakpoints(M5077.M5036.N5030)
    manager = M5077.CentralTopologyManager(run_directory, config)
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
            "stratum": job["stratum"],
            "status": row["status"],
            "resumed_from_cache": bool(row.get("resumed_from_cache")),
            "recorded_job_runtime_seconds": row["job_runtime_seconds"],
            "invocation_elapsed_seconds": time.monotonic() - started,
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
                "invocation_elapsed_seconds": time.monotonic() - started,
                **counts,
                "valid_for_numeric_UV_claim": False,
            },
        )
        print(json.dumps(log_row), flush=True)
        if row["status"] != "COMPLETED_CONVERGED":
            state = "BLOCKED_JOB_FAILURE"
            blocking_job = row
            break
        if maximum_new_jobs > 0 and newly_executed >= maximum_new_jobs:
            state = "PAUSED_JOB_CAP"
            break
    counts = run_counts(run_directory, config, jobs)
    if counts["completed_converged"] == len(jobs):
        state = "COMPLETE"
    analysis, rows = analyse(
        run_directory, config, manifest, jobs
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
        config,
        jobs,
        counts,
        analysis,
        rows,
        time.monotonic() - started,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "analyse"), default="dry-run"
    )
    parser.add_argument("--run-id", default="fresh_two_stratum_pilot_v1")
    parser.add_argument("--wall-cap-hours", type=float, default=4.0)
    parser.add_argument("--maximum-new-jobs", type=int, default=0)
    arguments = parser.parse_args()

    manifest = read_json(MANIFEST)
    config = make_config(manifest, arguments.run_id)
    jobs = build_schedule(config, manifest)
    activation = activation_record(manifest, config, jobs)
    atomic_json(ACTIVATION_JSON, activation)

    if arguments.mode == "dry-run":
        counts = {
            "completed_converged": 0,
            "completed_unconverged": 0,
            "failed": 0,
            "missing": len(jobs),
        }
        analysis = {
            "complete_full_events": 0,
            "expected_full_events": len(
                manifest["fresh_full_scramble_seeds"]
            ),
            "complete_topological_events": 0,
            "expected_topological_events": len(
                manifest["fresh_topological_scramble_seeds"]
            ),
            "full_matrix_complete": False,
            "topological_matrix_complete": False,
            "independent_stratified_estimate_available": False,
            "pilot_only": True,
            "numeric_UV_coefficient_complete": False,
            "valid_for_numeric_UV_claim": False,
        }
        result = finalize(
            arguments.run_id,
            "DRY_RUN",
            activation,
            config,
            jobs,
            counts,
            analysis,
            [],
            0.0,
        )
    elif arguments.mode == "analyse":
        run_directory = RUNS / arguments.run_id
        if not (run_directory / "config.json").exists():
            raise RuntimeError(f"run does not exist: {run_directory}")
        existing = read_json(run_directory / "config.json")
        if existing["config_digest"] != config["config_digest"]:
            raise RuntimeError("run config digest does not match")
        counts = run_counts(run_directory, config, jobs)
        analysis, rows = analyse(
            run_directory, config, manifest, jobs
        )
        state = (
            "COMPLETE"
            if counts["completed_converged"] == len(jobs)
            else "ANALYSED_PARTIAL"
        )
        result = finalize(
            arguments.run_id,
            state,
            activation,
            config,
            jobs,
            counts,
            analysis,
            rows,
            0.0,
        )
    else:
        result = execute(
            arguments.run_id,
            activation,
            config,
            manifest,
            jobs,
            arguments.wall_cap_hours,
            arguments.maximum_new_jobs,
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
