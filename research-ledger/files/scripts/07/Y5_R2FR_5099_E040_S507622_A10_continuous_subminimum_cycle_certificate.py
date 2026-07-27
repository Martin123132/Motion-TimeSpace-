from __future__ import annotations

import cmath
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v10"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5099"
RESULT_JSON = SOURCE / "E040_S507622_A10_continuous_subminimum_cycle_certificate.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5099_VALIDATION.csv"
)
MARKER = "MTS_5099_E040_S507622_A10_CONTINUOUS_SUBMINIMUM_CYCLE_CERTIFICATE"
REVISION = "continuous-subminimum-global-cycle-gauge-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507622_N0000"
ARGUMENT_ID = "E040_A10"
JOB_KEY = "E040__S507622_N0000__A10__coarse12"
SUBMINIMUM_FACTOR = 0.2
MINIMUM_SAMPLED_GLOBAL_POLE_MODULUS = 1.0e-4
GEOMETRY_SAMPLE_COUNT = 2048


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def continuous_subminimum_radius(groups: list[dict[str, Any]]) -> float:
    moduli = [abs(complex(group["root"])) for group in groups]
    if not moduli or not all(math.isfinite(value) and value > 0.0 for value in moduli):
        raise RuntimeError("5099 continuous subminimum cycle has no finite nonzero pole")
    return SUBMINIMUM_FACTOR * min(moduli)


def run_gate(
    module_5077: Any,
    module: Any,
    topology: dict[str, Any],
    config: dict[str, Any],
    global_residue_nodes: int,
) -> dict[str, Any]:
    profile = module_5077.M5043.PROFILES["coarse12"]
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    previous_radius = module.M5028.M5026.conditioned_global_base_radius
    removable = module_5077.M5085.CertifiedRemovableGlobalExtension(previous_global)
    module.chamber_residue_catalog = module_5077.restricted_coarse_catalog
    module.global_chamber_value = removable
    module.M5028.M5026.conditioned_global_base_radius = continuous_subminimum_radius
    module_5077.M5043.CURRENT_JOB = JOB_KEY
    module_5077.M5043.THEOREM_AUDIT.clear()
    module_5077.M5043.CHART_AUDIT.clear()
    module_5077.M5043.NUMERIC_AUDIT.clear()
    module_5077.LOCAL_ZERO_AUDIT.clear()
    module_5077.OUTWARD_CONTOUR_AUDIT.clear()
    module_5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
    started = time.monotonic()
    try:
        gate = module.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in profile["relative_orders"]),
            int(profile["global_nodes"]),
            global_residue_nodes,
            int(profile["relative_residue_nodes"]),
            float(profile["model_distance"]),
            int(config["topology"]["boundary_tracking_steps"]),
            str(profile["relative_quadrature_mode"]),
            float(profile["relative_adaptive_tolerance"]),
            int(profile["relative_adaptive_maximum_intervals"]),
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global
        module.M5028.M5026.conditioned_global_base_radius = previous_radius
    gate_path = SOURCE / f"E040_S507622_A10_subminimum_nodes_{global_residue_nodes}.json"
    atomic_json(gate_path, gate)
    value = complex(gate["highest_order_value"])
    return {
        "global_residue_nodes": global_residue_nodes,
        "runtime_seconds": time.monotonic() - started,
        "gate_path": str(gate_path),
        "gate_sha256": digest(gate_path),
        "converged": bool(gate["fixed_event_crossed_integral_converged"]),
        "all_residues_stable": bool(gate["all_residues_stable"]),
        "relative_residual": float(gate["highest_two_order_relative_residual"]),
        "highest_order_value": complex_row(value),
        "topological_correction": gate["topological_correction"],
        "interval_count": int(gate["order_rows"][-1]["composite_interval_count"]),
        "evaluation_count": int(
            gate["order_rows"][-1]["relative_integrand_evaluation_count"]
        ),
        "maximum_depth_observed": int(
            gate["order_rows"][-1].get("maximum_adaptive_depth", 0)
        ),
        "removable_extension_call_count": len(removable.calls),
        "projective_cluster_zero_count": len(
            module_5077.PROJECTIVE_CLUSTER_ZERO_AUDIT
        ),
        "valid_for_full_MTS_claim": False,
    }


def geometry_audit(
    module: Any,
    topology: dict[str, Any],
) -> list[dict[str, Any]]:
    _, ownerships = module.physical_chambers()
    rows: list[dict[str, Any]] = []
    original_radius = module.M5028.M5026.conditioned_global_base_radius
    for chamber_index, ownership in enumerate(ownerships):
        chamber = topology["chambers"][chamber_index]
        start = complex(chamber["target_start_log"])
        end = complex(chamber["target_end_log"])
        minimum_modulus = math.inf
        minimum_row: dict[str, Any] | None = None
        old_selector_branch_changes = 0
        old_selector_previous: str | None = None
        old_radius_jumps = 0
        old_radius_previous: float | None = None
        maximum_subminimum_ratio_error = 0.0
        for index in range(GEOMETRY_SAMPLE_COUNT):
            parameter = (index + 0.371) / GEOMETRY_SAMPLE_COUNT
            relative_circle = cmath.exp(start + parameter * (end - start))
            soft_direction, decay_direction, internal = module.M5028.event_geometry(
                module.SOFT_ENERGY,
                complex(module.SOFT_COSINE, 0.0),
                complex(module.DECAY_COSINE, 0.0),
                relative_circle,
            )
            groups = module.M5028.fixed_ownership_groups(
                internal,
                soft_direction,
                decay_direction,
                module.TARGET_COSINE,
                ownership,
            )
            local_minimum = min(abs(complex(group["root"])) for group in groups)
            subminimum = continuous_subminimum_radius(groups)
            old_radius = original_radius(groups)
            branch = (
                "subminimum"
                if SUBMINIMUM_FACTOR * local_minimum
                >= module.M5028.M5026.MINIMUM_CONDITIONED_BASE_RADIUS
                else "maximal_annulus"
            )
            if old_selector_previous is not None and branch != old_selector_previous:
                old_selector_branch_changes += 1
            if old_radius_previous is not None:
                ratio = max(old_radius, old_radius_previous) / max(
                    min(old_radius, old_radius_previous), 1.0e-300
                )
                if ratio > 2.0:
                    old_radius_jumps += 1
            old_selector_previous = branch
            old_radius_previous = old_radius
            maximum_subminimum_ratio_error = max(
                maximum_subminimum_ratio_error,
                abs(subminimum / local_minimum - SUBMINIMUM_FACTOR),
            )
            if local_minimum < minimum_modulus:
                minimum_modulus = local_minimum
                minimum_row = {
                    "parameter": parameter,
                    "relative_circle": complex_row(relative_circle),
                    "minimum_global_pole_modulus": local_minimum,
                    "continuous_subminimum_radius": subminimum,
                    "old_conditioned_radius": old_radius,
                    "old_selector_branch": branch,
                }
        rows.append(
            {
                "chamber_index": chamber_index,
                "sample_count": GEOMETRY_SAMPLE_COUNT,
                "minimum_sample": minimum_row,
                "minimum_sampled_global_pole_modulus": minimum_modulus,
                "old_selector_branch_changes": old_selector_branch_changes,
                "old_radius_large_jump_count": old_radius_jumps,
                "maximum_subminimum_ratio_error": maximum_subminimum_ratio_error,
            }
        )
    return rows


def main() -> None:
    topology_path = RUN / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    failed_job_path = RUN / "jobs" / f"{JOB_KEY}.json"
    required = [SCRIPT_5077, RUN / "config.json", topology_path, failed_job_path, FORMAL]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5099 inputs: {missing}")
    module_5077 = load_module("mts_5077_for_5099", SCRIPT_5077)
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    event = module_5077.M5036.event_lookup(config)[EVENT_ID]
    argument = module_5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = module_5077.M5036.complex_from_row(argument["target_cosine"])
    module_5077.M5043.M5034.configure(event, target)
    module = module_5077.M5043.N5030
    module_5077.install_history_invariant_breakpoints(module)
    topology = json.loads(topology_path.read_text(encoding="utf-8"))
    failed_job = json.loads(failed_job_path.read_text(encoding="utf-8"))
    failed_kernel = json.loads(Path(failed_job["kernel_file"]).read_text(encoding="utf-8"))
    failed_gate = failed_kernel["fixed_event_integral_gate"]
    geometry_rows = geometry_audit(module, topology)
    gate_rows = [
        run_gate(module_5077, module, topology, config, nodes) for nodes in (12, 24)
    ]
    values = [
        complex(row["highest_order_value"]["real"], row["highest_order_value"]["imaginary"])
        for row in gate_rows
    ]
    cross_node_residual = abs(values[-1] - values[-2]) / max(1.0, abs(values[-1]))
    profile = module_5077.M5043.PROFILES["coarse12"]
    tolerance = float(profile["relative_adaptive_tolerance"])
    formal_digest = tree_digest(FORMAL)
    guards = {
        "original_failure_is_adaptive_only": not bool(
            failed_gate["fixed_event_crossed_integral_converged"]
        )
        and bool(failed_gate["all_residues_stable"]),
        "old_radius_selector_is_discontinuous": any(
            row["old_selector_branch_changes"] > 0
            or row["old_radius_large_jump_count"] > 0
            for row in geometry_rows
        ),
        "sampled_global_poles_stay_nonzero": all(
            row["minimum_sampled_global_pole_modulus"]
            > MINIMUM_SAMPLED_GLOBAL_POLE_MODULUS
            for row in geometry_rows
        ),
        "subminimum_contour_is_strictly_inside_all_poles": all(
            row["maximum_subminimum_ratio_error"] < 2.0e-14
            for row in geometry_rows
        )
        and 0.0 < SUBMINIMUM_FACTOR < 1.0,
        "both_node_gates_converged": all(row["converged"] for row in gate_rows),
        "all_residues_stable": all(row["all_residues_stable"] for row in gate_rows),
        "cross_node_stable": cross_node_residual < tolerance,
        "production_tolerance_unchanged": all(
            row["relative_residual"] < tolerance for row in gate_rows
        ),
        "no_exact_collision_fallback": all(
            row["removable_extension_call_count"] == 0 for row in gate_rows
        ),
        "no_unrelated_projective_zero_route": all(
            row["projective_cluster_zero_count"] == 0 for row in gate_rows
        ),
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
    }
    certificate_passed = all(guards.values())
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "job_key": JOB_KEY,
        "source_failed_job": str(failed_job_path),
        "source_failed_job_sha256_before_repair": digest(failed_job_path),
        "source_config": str(RUN / "config.json"),
        "source_config_sha256": digest(RUN / "config.json"),
        "subminimum_factor": SUBMINIMUM_FACTOR,
        "cycle_identity": (
            "For each relative q, choose the global base circle r(q)=eta min_j|z_j(q)| "
            "with 0<eta<1. The circle encloses no finite global pole. Adding exactly "
            "the residues of the causally owned poles gives the same physical global "
            "cycle by Cauchy's theorem. This representation is continuous wherever "
            "the regulated path has no chart-origin pole and removes the discontinuous "
            "maximal-annulus gauge switches of the old numerical selector."
        ),
        "geometry_audit": geometry_rows,
        "original_relative_residual": float(
            failed_gate["highest_two_order_relative_residual"]
        ),
        "original_interval_count": int(
            failed_gate["order_rows"][-1]["composite_interval_count"]
        ),
        "gate_rows": gate_rows,
        "cross_node_relative_residual": float(cross_node_residual),
        "guards": guards,
        "continuous_subminimum_cycle_certificate_passed": certificate_passed,
        "runner_integration_authorized": certificate_passed,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all 5099 sources exist"),
        (
            "failure_localized_to_adaptive_gate",
            guards["original_failure_is_adaptive_only"],
            str(result["original_relative_residual"]),
        ),
        (
            "old_selector_discontinuous",
            guards["old_radius_selector_is_discontinuous"],
            str(geometry_rows),
        ),
        (
            "subminimum_cycle_isolated",
            guards["sampled_global_poles_stay_nonzero"]
            and guards["subminimum_contour_is_strictly_inside_all_poles"],
            str([row["minimum_sampled_global_pole_modulus"] for row in geometry_rows]),
        ),
        (
            "both_node_gates_converged",
            guards["both_node_gates_converged"],
            str([row["relative_residual"] for row in gate_rows]),
        ),
        (
            "residues_stable",
            guards["all_residues_stable"],
            str([row["all_residues_stable"] for row in gate_rows]),
        ),
        ("cross_node_stable", guards["cross_node_stable"], str(cross_node_residual)),
        (
            "production_controls_unchanged",
            guards["production_tolerance_unchanged"],
            "tolerance and interval cap unchanged",
        ),
        (
            "no_unrelated_fallback",
            guards["no_exact_collision_fallback"]
            and guards["no_unrelated_projective_zero_route"],
            "no 5085 or 5097 fallback",
        ),
        ("certificate_passed", certificate_passed, str(certificate_passed)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "contour-gauge certificate is not physical evidence",
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5099_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5099 validation failed: {failed}")


if __name__ == "__main__":
    main()
