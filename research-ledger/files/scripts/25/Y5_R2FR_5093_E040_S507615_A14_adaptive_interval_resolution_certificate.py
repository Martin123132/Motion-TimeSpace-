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
RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v8"
SOURCE = POST / "source-intake" / "functional_rg" / "5093"
RESULT_JSON = SOURCE / "E040_S507615_A14_adaptive_interval_resolution_certificate.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5093_VALIDATION.csv"
MARKER = "MTS_5093_E040_S507615_A14_ADAPTIVE_INTERVAL_RESOLUTION_CERTIFICATE"
REVISION = "fixed-tolerance-adaptive-interval-cap-ladder-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507615_N0000"
ARGUMENT_ID = "E040_A14"
JOB_KEY = "E040__S507615_N0000__A14__coarse12"
INTERVAL_CAPS = (2048, 4096)


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


def run_cap(
    module_5077: Any,
    module: Any,
    topology: dict[str, Any],
    config: dict[str, Any],
    cap: int,
) -> dict[str, Any]:
    profile = module_5077.M5043.PROFILES["coarse12"]
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    removable = module_5077.M5085.CertifiedRemovableGlobalExtension(previous_global)
    module.chamber_residue_catalog = module_5077.restricted_coarse_catalog
    module.global_chamber_value = removable
    module_5077.M5043.CURRENT_JOB = f"5093::{JOB_KEY}::cap{cap}"
    module_5077.M5043.THEOREM_AUDIT.clear()
    module_5077.M5043.CHART_AUDIT.clear()
    module_5077.M5043.NUMERIC_AUDIT.clear()
    module_5077.LOCAL_ZERO_AUDIT.clear()
    module_5077.OUTWARD_CONTOUR_AUDIT.clear()
    started = time.monotonic()
    try:
        gate = module.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in profile["relative_orders"]),
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            float(profile["model_distance"]),
            int(config["topology"]["boundary_tracking_steps"]),
            str(profile["relative_quadrature_mode"]),
            float(profile["relative_adaptive_tolerance"]),
            cap,
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global
    elapsed = time.monotonic() - started
    value = complex(gate["highest_order_value"])
    gate_path = SOURCE / f"E040_S507615_A14_cap{cap}_gate.json"
    atomic_json(gate_path, gate)
    return {
        "interval_cap": cap,
        "runtime_seconds": elapsed,
        "gate_path": str(gate_path),
        "gate_sha256": digest(gate_path),
        "converged": bool(gate["fixed_event_crossed_integral_converged"]),
        "all_residues_stable": bool(gate["all_residues_stable"]),
        "highest_two_order_relative_residual": float(
            gate["highest_two_order_relative_residual"]
        ),
        "highest_order_value": module_5077.M5036.complex_row(value),
        "composite_interval_count": int(
            gate["order_rows"][-1]["composite_interval_count"]
        ),
        "relative_integrand_evaluation_count": int(
            gate["order_rows"][-1]["relative_integrand_evaluation_count"]
        ),
        "topological_correction": gate["topological_correction"],
        "numerical_removable_extension_call_count": len(removable.calls),
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    failed_job = RUN / "jobs" / f"{JOB_KEY}.json"
    failed_kernel = RUN / "kernels" / f"{JOB_KEY}.json"
    topology_path = RUN / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    required = [SCRIPT_5077, RUN / "config.json", failed_job, failed_kernel, topology_path, FORMAL]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5093 inputs: {missing}")
    M5077 = load_module("mts_5077_for_5093", SCRIPT_5077)
    M5077.removable_extension_gate()
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    event = M5077.M5036.event_lookup(config)[EVENT_ID]
    argument = M5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = M5077.M5036.complex_from_row(argument["target_cosine"])
    M5077.M5043.M5034.configure(event, target)
    module = M5077.M5043.N5030
    topology = json.loads(topology_path.read_text(encoding="utf-8"))
    source_job = json.loads(failed_job.read_text(encoding="utf-8"))
    source_gate = json.loads(failed_kernel.read_text(encoding="utf-8"))[
        "fixed_event_integral_gate"
    ]
    rows = [run_cap(M5077, module, topology, config, cap) for cap in INTERVAL_CAPS]
    values = [M5077.M5036.complex_from_row(row["highest_order_value"]) for row in rows]
    cross_cap_relative_difference = abs(values[-1] - values[-2]) / max(
        1.0, abs(values[-1])
    )
    tolerance = float(M5077.M5043.PROFILES["coarse12"]["relative_adaptive_tolerance"])
    formal_digest = tree_digest(FORMAL)
    resolution_supported = bool(
        rows[-1]["converged"]
        and rows[-1]["all_residues_stable"]
        and rows[-1]["highest_two_order_relative_residual"] < tolerance
        and cross_cap_relative_difference < tolerance
        and all(row["numerical_removable_extension_call_count"] == 0 for row in rows)
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": JOB_KEY,
        "source_status": source_job["status"],
        "source_interval_cap": int(source_gate["relative_adaptive_maximum_intervals"]),
        "source_interval_count": int(source_gate["order_rows"][-1]["composite_interval_count"]),
        "source_relative_residual": float(source_gate["highest_two_order_relative_residual"]),
        "source_residues_stable": bool(source_gate["all_residues_stable"]),
        "adaptive_tolerance": tolerance,
        "interval_cap_rows": rows,
        "cross_cap_relative_difference": float(cross_cap_relative_difference),
        "fixed_tolerance_resolution_supported": resolution_supported,
        "recommended_job_interval_cap": INTERVAL_CAPS[-1] if resolution_supported else None,
        "tolerance_relaxed": False,
        "residue_rule_changed": False,
        "topology_changed": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all 5093 inputs exist"),
        ("source_is_target_failure", source_job["status"] == "COMPLETED_UNCONVERGED" and source_gate["all_residues_stable"], source_job["status"]),
        ("cap_ladder_increases_only_resolution", list(INTERVAL_CAPS) == [2048, 4096] and not result["tolerance_relaxed"] and not result["residue_rule_changed"] and not result["topology_changed"], str(INTERVAL_CAPS)),
        ("finest_gate_converged", rows[-1]["converged"], str(rows[-1]["highest_two_order_relative_residual"])),
        ("finest_residues_stable", rows[-1]["all_residues_stable"], str(rows[-1]["all_residues_stable"])),
        ("cross_cap_stable", cross_cap_relative_difference < tolerance, str(cross_cap_relative_difference)),
        ("no_collision_fallback", all(row["numerical_removable_extension_call_count"] == 0 for row in rows), str([row["numerical_removable_extension_call_count"] for row in rows])),
        ("resolution_supported", resolution_supported, str(resolution_supported)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "resolution certificate is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow({"check_id": f"V5093_{index:02d}_{name}", "passed": passed, "detail": detail, "checkpoint_marker": MARKER})
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5093 validation failed: {failed}")


if __name__ == "__main__":
    main()
