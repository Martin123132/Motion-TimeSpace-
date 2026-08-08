from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
import traceback
from pathlib import Path
from typing import Any, Callable


POST = Path(__file__).resolve().parents[1]
REPAIR_SCRIPT = POST / "scripts" / "Y5_R2FR_5037_chart_origin_collision_repair.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5037"
RUNS = SOURCE / "runs"
DIAGNOSTICS = SOURCE / "diagnostics"
MARKER = "MTS_5037_A14_OWNERSHIP_PINCH_DIAGNOSTIC"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


REPAIR = load_module("mts_5037_repair_for_A14_diagnostic", REPAIR_SCRIPT)
N5030 = REPAIR.N5030
M5035 = REPAIR.M5035
M5036 = REPAIR.M5036


def serialized_complex(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def ownership_digest(ownership: dict[str, bool]) -> str:
    payload = json.dumps(ownership, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def conflict_rows(
    internal: Any,
    soft_direction: Any,
    decay_direction: Any,
    scattering_cosine: complex,
    ownership: dict[str, bool],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, direction in N5030.M5028.source_directions(
        internal, soft_direction, decay_direction
    ).items():
        roots = N5030.M5028.M5024.all_factor_roots(direction, scattering_cosine)
        for label in N5030.M5028.ROOT_LABELS:
            key = f"{source}:{label}"
            rows.append(
                {
                    "label": key,
                    "root": complex(roots[label]),
                    "desired_inside": bool(ownership[key]),
                }
            )
    groups: list[list[dict[str, Any]]] = []
    tolerance = N5030.M5028.ROOT_COINCIDENCE_RELATIVE_TOLERANCE
    for row in rows:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(row["root"] - candidate[0]["root"])
                < tolerance
                * max(1.0, abs(row["root"]), abs(candidate[0]["root"]))
            ),
            None,
        )
        if group is None:
            groups.append([row])
        else:
            group.append(row)
    conflicts: list[dict[str, Any]] = []
    for group in groups:
        if len({row["desired_inside"] for row in group}) == 1:
            continue
        maximum_separation = max(
            abs(first["root"] - second["root"])
            for first in group
            for second in group
        )
        conflicts.append(
            {
                "labels": [row["label"] for row in group],
                "desired_inside": [row["desired_inside"] for row in group],
                "roots": {
                    row["label"]: serialized_complex(row["root"]) for row in group
                },
                "maximum_absolute_separation": float(maximum_separation),
                "coincidence_tolerance": float(tolerance),
            }
        )
    return conflicts


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    run_directory = RUNS / arguments.run_id
    config = json.loads((run_directory / "config.json").read_text(encoding="utf-8"))
    job_path = run_directory / "jobs" / f"{arguments.job_key}.json"
    job = json.loads(job_path.read_text(encoding="utf-8"))
    event = M5035.event_lookup(config)[job["event_id"]]
    argument = M5035.argument_lookup(config)[job["argument_id"]]
    tier = config["tiers"][job["tier"]]
    topology_path = M5035.M5034.topology_path(
        run_directory, job["event_id"], job["argument_id"]
    )
    topology = json.loads(topology_path.read_text(encoding="utf-8"))
    target = M5035.complex_from_row(argument["target_cosine"])
    M5035.M5034.configure(event, target)
    REPAIR.CURRENT_JOB = job["job_key"]
    REPAIR.EXCLUSION_AUDIT.clear()
    REPAIR.RADIUS_AUDIT.clear()

    context: dict[str, Any] = {"stage": "setup"}
    failures: list[dict[str, Any]] = []
    counts = {
        "fixed_ownership_calls": 0,
        "global_chamber_calls": 0,
        "collision_local_global_residue_calls": 0,
        "pair_local_relative_residue_calls": 0,
        "catalog_calls": 0,
    }
    original_fixed = N5030.M5028.fixed_ownership_groups
    original_global = N5030.global_chamber_value
    original_collision = N5030.collision_local_global_residue
    original_pair = N5030.pair_local_relative_residue
    original_catalog = N5030.chamber_residue_catalog

    def with_context(stage: str, details: dict[str, Any], call: Callable[[], Any]) -> Any:
        previous = dict(context)
        context.clear()
        context.update(previous)
        context.update({"stage": stage, **details})
        try:
            return call()
        finally:
            context.clear()
            context.update(previous)

    def diagnostic_fixed(
        internal: Any,
        soft_direction: Any,
        decay_direction: Any,
        scattering_cosine: complex,
        ownership: dict[str, bool],
    ) -> list[dict[str, Any]]:
        counts["fixed_ownership_calls"] += 1
        try:
            return original_fixed(
                internal,
                soft_direction,
                decay_direction,
                scattering_cosine,
                ownership,
            )
        except RuntimeError as error:
            failures.append(
                {
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "context": dict(context),
                    "scattering_cosine": serialized_complex(scattering_cosine),
                    "ownership_digest": ownership_digest(ownership),
                    "conflicts": conflict_rows(
                        internal,
                        soft_direction,
                        decay_direction,
                        scattering_cosine,
                        ownership,
                    ),
                    "stack": traceback.format_stack(limit=12),
                }
            )
            raise

    def diagnostic_global(
        relative_circle: complex,
        ownership: dict[str, bool],
        global_nodes: int,
        global_residue_nodes: int,
    ) -> complex:
        counts["global_chamber_calls"] += 1
        return with_context(
            "global_chamber_value",
            {
                "relative_circle": serialized_complex(relative_circle),
                "ownership_digest": ownership_digest(ownership),
                "global_nodes": int(global_nodes),
                "global_residue_nodes": int(global_residue_nodes),
            },
            lambda: original_global(
                relative_circle, ownership, global_nodes, global_residue_nodes
            ),
        )

    def diagnostic_collision(
        relative_circle: complex,
        collision_pairs: list[tuple[str, str]],
        ownership: dict[str, bool],
        global_residue_nodes: int,
    ) -> complex:
        counts["collision_local_global_residue_calls"] += 1
        return with_context(
            "collision_local_global_residue",
            {
                "relative_circle": serialized_complex(relative_circle),
                "collision_pairs": [list(pair) for pair in collision_pairs],
                "ownership_digest": ownership_digest(ownership),
                "global_residue_nodes": int(global_residue_nodes),
            },
            lambda: original_collision(
                relative_circle,
                collision_pairs,
                ownership,
                global_residue_nodes,
            ),
        )

    def diagnostic_pair(
        root: complex,
        radius: float,
        nodes: int,
        collision_pairs: list[tuple[str, str]],
        ownership: dict[str, bool],
        global_residue_nodes: int,
    ) -> complex:
        counts["pair_local_relative_residue_calls"] += 1
        return with_context(
            "pair_local_relative_residue",
            {
                "pair_root": serialized_complex(root),
                "pair_radius": float(radius),
                "pair_nodes": int(nodes),
                "collision_pairs": [list(pair) for pair in collision_pairs],
                "ownership_digest": ownership_digest(ownership),
            },
            lambda: original_pair(
                root,
                radius,
                nodes,
                collision_pairs,
                ownership,
                global_residue_nodes,
            ),
        )

    def diagnostic_catalog(*catalog_arguments: Any, **catalog_keywords: Any) -> Any:
        counts["catalog_calls"] += 1
        ownership = catalog_arguments[0]
        return with_context(
            "chamber_residue_catalog",
            {
                "catalog_index": counts["catalog_calls"] - 1,
                "ownership_digest": ownership_digest(ownership),
                "start_log": serialized_complex(catalog_arguments[1]),
                "end_log": serialized_complex(catalog_arguments[2]),
            },
            lambda: REPAIR.repaired_chamber_residue_catalog(
                *catalog_arguments, **catalog_keywords
            ),
        )

    N5030.M5028.fixed_ownership_groups = diagnostic_fixed
    N5030.global_chamber_value = diagnostic_global
    N5030.collision_local_global_residue = diagnostic_collision
    N5030.pair_local_relative_residue = diagnostic_pair
    N5030.chamber_residue_catalog = diagnostic_catalog
    started = time.monotonic()
    gate: dict[str, Any] | None = None
    terminal_error: dict[str, str] | None = None
    try:
        gate = N5030.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in tier["relative_orders"]),
            int(tier["global_nodes"]),
            int(tier["global_residue_nodes"]),
            int(tier["relative_residue_nodes"]),
            float(tier["model_distance"]),
            int(config["topology"]["boundary_tracking_steps"]),
            str(tier["relative_quadrature_mode"]),
            float(tier["relative_adaptive_tolerance"]),
            int(tier["relative_adaptive_maximum_intervals"]),
        )
    except Exception as error:
        terminal_error = {
            "error_type": type(error).__name__,
            "error": str(error),
        }
    finally:
        N5030.M5028.fixed_ownership_groups = original_fixed
        N5030.global_chamber_value = original_global
        N5030.collision_local_global_residue = original_collision
        N5030.pair_local_relative_residue = original_pair
        N5030.chamber_residue_catalog = original_catalog

    document = {
        "checkpoint_marker": MARKER,
        "run_id": arguments.run_id,
        "job_key": job["job_key"],
        "job_file": str(job_path),
        "job_file_sha256": M5036.file_digest(job_path),
        "topology_file": str(topology_path),
        "topology_file_sha256": M5036.file_digest(topology_path),
        "repair_script": str(REPAIR_SCRIPT),
        "repair_script_sha256": M5036.file_digest(REPAIR_SCRIPT),
        "diagnostic_script": str(Path(__file__).resolve()),
        "diagnostic_script_sha256": M5036.file_digest(Path(__file__).resolve()),
        "target_cosine": serialized_complex(target),
        "counts": counts,
        "terminal_error": terminal_error,
        "ownership_failures": failures,
        "chart_origin_exclusions": list(REPAIR.EXCLUSION_AUDIT),
        "radius_audit": list(REPAIR.RADIUS_AUDIT),
        "gate_completed": gate is not None,
        "runtime_seconds": time.monotonic() - started,
        "valid_for_full_MTS_claim": False,
    }
    output = DIAGNOSTICS / arguments.diagnostic_id / "diagnostic.json"
    M5036.atomic_json(output, document)
    print(json.dumps(document, indent=2))
    return document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="paired_outer_precision_s4_v1")
    parser.add_argument(
        "--job-key", default="E040__S503403_N0000__A14__primary24"
    )
    parser.add_argument("--diagnostic-id", default="A14_ownership_pinch_v1")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
