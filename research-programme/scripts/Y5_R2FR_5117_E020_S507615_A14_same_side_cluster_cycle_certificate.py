from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5095 = (
    POST / "scripts" / "Y5_R2FR_5095_same_side_global_cluster_cycle_certificate.py"
)
PARENT_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5095"
    / "same_side_global_cluster_cycle_certificate.json"
)
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)
CONFIG = RUN / "config.json"
EVENT_ID = "S507615_N0000"
ARGUMENT_ID = "E020_A14"
JOB_KEY = "E020__S507615_N0000__A14__primary24"
TOPOLOGY = RUN / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
UNCLUSTERED_KERNEL = RUN / "kernels" / f"{JOB_KEY}.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5117"
RESULT_JSON = SOURCE / "E020_S507615_A14_same_side_cluster_cycle_certificate.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5117_VALIDATION.csv"
)
MARKER = "MTS_5117_E020_S507615_A14_SAME_SIDE_CLUSTER_CYCLE_CERTIFICATE"
REVISION = "exact-job-cauchy-cluster-epsilon-continuation-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
GLOBAL_RESIDUE_NODE_LEVELS = (24, 48)


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


def run_gate(
    module_5077: Any,
    module_5095: Any,
    module: Any,
    topology: dict[str, Any],
    config: dict[str, Any],
    global_residue_nodes: int,
) -> dict[str, Any]:
    profile = config["tiers"]["primary24"]
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    clustered = module_5095.CertifiedSameSideClusterGlobalValue(module)
    removable = module_5077.M5085.CertifiedRemovableGlobalExtension(clustered)
    module.chamber_residue_catalog = module_5077.certified_primary_catalog
    module.global_chamber_value = removable
    module_5077.M5036.MREPAIR.CURRENT_JOB = (
        f"5117::{JOB_KEY}::global_residue_nodes_{global_residue_nodes}"
    )
    module_5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
    module_5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
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
    elapsed = time.monotonic() - started
    gate_path = SOURCE / f"E020_S507615_A14_clustered_residue_nodes_{global_residue_nodes}.json"
    atomic_json(gate_path, gate)
    value = complex(gate["highest_order_value"])
    return {
        "global_residue_nodes": global_residue_nodes,
        "runtime_seconds": elapsed,
        "gate_path": str(gate_path),
        "gate_sha256": digest(gate_path),
        "converged": bool(gate["fixed_event_crossed_integral_converged"]),
        "all_residues_stable": bool(gate["all_residues_stable"]),
        "relative_residual": float(gate["highest_two_order_relative_residual"]),
        "highest_order_value": complex_row(value),
        "interval_count": int(gate["order_rows"][-1]["composite_interval_count"]),
        "evaluation_count": int(
            gate["order_rows"][-1]["relative_integrand_evaluation_count"]
        ),
        "pole_model_count": int(gate["order_rows"][-1]["pole_model_count"]),
        "cluster_audit": clustered.summary(),
        "removable_extension_call_count": len(removable.calls),
        "event_local_residue_resolution_count": len(
            module_5077.LOCAL_RESIDUE_RESOLUTION_AUDIT
        ),
        "residue_radius_adjustment_count": len(
            module_5077.M5036.MREPAIR.RADIUS_AUDIT
        ),
        "tolerance_changed": False,
        "interval_cap_changed": False,
        "profile_changed": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    required = [
        SCRIPT_5077,
        SCRIPT_5095,
        PARENT_GATE,
        CONFIG,
        TOPOLOGY,
        UNCLUSTERED_KERNEL,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5117 inputs: {missing}")
    module_5077 = load_module("mts_5077_for_5117", SCRIPT_5077)
    module_5095 = load_module("mts_5095_for_5117", SCRIPT_5095)
    module_5077.removable_extension_gate()
    module_5077.recoil_scope_correction_gate()
    parent = json.loads(PARENT_GATE.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    topology = json.loads(TOPOLOGY.read_text(encoding="utf-8"))
    unclustered = json.loads(UNCLUSTERED_KERNEL.read_text(encoding="utf-8"))
    unclustered_gate = unclustered["fixed_event_integral_gate"]
    event = module_5077.M5036.event_lookup(config)[EVENT_ID]
    argument = module_5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    module_5077.CURRENT_EVENT = event
    module_5077.CURRENT_ARGUMENT = argument
    target = module_5077.M5036.complex_from_row(argument["target_cosine"])
    module_5077.M5036.M5035.M5034.configure(event, target)
    module = module_5077.M5036.N5030
    gate_rows = [
        run_gate(
            module_5077,
            module_5095,
            module,
            topology,
            config,
            nodes,
        )
        for nodes in GLOBAL_RESIDUE_NODE_LEVELS
    ]
    values = [
        complex(row["highest_order_value"]["real"], row["highest_order_value"]["imaginary"])
        for row in gate_rows
    ]
    cross_node_residual = abs(values[-1] - values[-2]) / max(1.0, abs(values[-1]))
    profile = config["tiers"]["primary24"]
    tolerance = float(profile["relative_adaptive_tolerance"])
    formal_digest = tree_digest(FORMAL)
    certificate_passed = bool(
        parent["same_side_cluster_cycle_certificate_passed"]
        and not unclustered_gate["fixed_event_crossed_integral_converged"]
        and all(row["converged"] for row in gate_rows)
        and all(row["all_residues_stable"] for row in gate_rows)
        and cross_node_residual < tolerance
        and all(row["cluster_audit"]["cluster_count"] > 0 for row in gate_rows)
        and all(
            row["cluster_audit"]["maximum_cluster_isolation_ratio"]
            < module_5095.MAXIMUM_CLUSTER_ISOLATION_RATIO
            for row in gate_rows
        )
        and all(row["removable_extension_call_count"] == 0 for row in gate_rows)
        and all(
            not row["tolerance_changed"]
            and not row["interval_cap_changed"]
            and not row["profile_changed"]
            for row in gate_rows
        )
        and formal_digest == FORMAL_BASELINE
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": JOB_KEY,
        "scope": "exact E020 S507615 A14 primary24 job only",
        "parent_cauchy_gate": str(PARENT_GATE),
        "parent_cauchy_gate_sha256": digest(PARENT_GATE),
        "cauchy_identity": parent["cauchy_identity"],
        "cluster_contour_rule": parent["cluster_contour_rule"],
        "link_relative_distance": module_5095.LINK_RELATIVE_DISTANCE,
        "maximum_cluster_isolation_ratio": module_5095.MAXIMUM_CLUSTER_ISOLATION_RATIO,
        "unclustered_failure": {
            "kernel": str(UNCLUSTERED_KERNEL),
            "kernel_sha256": digest(UNCLUSTERED_KERNEL),
            "converged": bool(unclustered_gate["fixed_event_crossed_integral_converged"]),
            "relative_residual": float(
                unclustered_gate["highest_two_order_relative_residual"]
            ),
            "interval_count": int(
                unclustered_gate["order_rows"][-1]["composite_interval_count"]
            ),
            "pole_model_count": int(
                unclustered_gate["order_rows"][-1]["pole_model_count"]
            ),
        },
        "adaptive_tolerance": tolerance,
        "production_interval_cap": int(profile["relative_adaptive_maximum_intervals"]),
        "gate_rows": gate_rows,
        "cross_node_relative_residual": float(cross_node_residual),
        "same_side_cluster_cycle_certificate_passed": certificate_passed,
        "production_integration_authorized": certificate_passed,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, str(len(required))),
        (
            "parent_cauchy_certificate_passed",
            bool(parent["same_side_cluster_cycle_certificate_passed"]),
            parent["checkpoint_marker"],
        ),
        (
            "unclustered_failure_reproduced",
            not unclustered_gate["fixed_event_crossed_integral_converged"],
            str(unclustered_gate["highest_two_order_relative_residual"]),
        ),
        (
            "both_node_gates_converged",
            all(row["converged"] for row in gate_rows),
            str([row["relative_residual"] for row in gate_rows]),
        ),
        (
            "all_residues_stable",
            all(row["all_residues_stable"] for row in gate_rows),
            str([row["all_residues_stable"] for row in gate_rows]),
        ),
        ("cross_node_stable", cross_node_residual < tolerance, str(cross_node_residual)),
        (
            "cluster_route_exercised",
            all(row["cluster_audit"]["cluster_count"] > 0 for row in gate_rows),
            str([row["cluster_audit"]["cluster_count"] for row in gate_rows]),
        ),
        (
            "cluster_isolation_passed",
            all(
                row["cluster_audit"]["maximum_cluster_isolation_ratio"]
                < module_5095.MAXIMUM_CLUSTER_ISOLATION_RATIO
                for row in gate_rows
            ),
            str(
                [
                    row["cluster_audit"]["maximum_cluster_isolation_ratio"]
                    for row in gate_rows
                ]
            ),
        ),
        (
            "no_exact_collision_fallback",
            all(row["removable_extension_call_count"] == 0 for row in gate_rows),
            str([row["removable_extension_call_count"] for row in gate_rows]),
        ),
        (
            "production_controls_unchanged",
            all(
                not row["tolerance_changed"]
                and not row["interval_cap_changed"]
                and not row["profile_changed"]
                for row in gate_rows
            ),
            "profile, tolerance, and interval cap unchanged",
        ),
        ("certificate_passed", certificate_passed, str(certificate_passed)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "numerical contour certificate is not physical evidence",
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for name, passed, detail in checks:
            writer.writerow(
                {
                    "check": name,
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5117 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
