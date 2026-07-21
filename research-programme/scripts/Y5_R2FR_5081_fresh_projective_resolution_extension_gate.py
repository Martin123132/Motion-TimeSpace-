from __future__ import annotations

import csv
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
FAILED_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v1"
SOURCE = POST / "source-intake" / "functional_rg" / "5081"
SCRATCH = SOURCE / "scratch_full_target"
RESULT_JSON = SOURCE / "fresh_projective_resolution_extension_gate.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5081_VALIDATION.csv"
MARKER = "MTS_5081_FRESH_PROJECTIVE_RESOLUTION_EXTENSION_GATE"
REVISION = "append-2048-with-full-target-and-kernel-replay-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507602_N0000"
SOURCE_ARGUMENT_ID = "E040_A05"
TARGET_ARGUMENT_ID = "E040_A04"
EXTENDED_LEVELS = (16, 32, 64, 128, 256, 512, 1024, 2048)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module("mts_5077_for_5081", SCRIPT_5077)
M5069 = M5077.M5069
M5061 = M5069.M5061


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def complex_distance(left: complex, right: complex) -> tuple[float, float]:
    absolute = float(abs(left - right))
    relative = float(absolute / max(1.0, abs(left), abs(right)))
    return absolute, relative


def parse_complex(value: Any) -> complex:
    if isinstance(value, dict):
        return complex(float(value["real"]), float(value["imaginary"]))
    return complex(str(value))


def kernel_gate(
    config: dict[str, Any],
    event: dict[str, Any],
    target: complex,
    topology: dict[str, Any],
    label: str,
) -> dict[str, Any]:
    module = M5077.M5036.N5030
    M5077.install_history_invariant_breakpoints(module)
    M5077.M5036.M5035.M5034.configure(event, target)
    profile = config["tiers"]["primary24"]
    previous_catalog = module.chamber_residue_catalog
    module.chamber_residue_catalog = (
        M5077.M5036.MREPAIR.repaired_chamber_residue_catalog
    )
    M5077.M5036.MREPAIR.CURRENT_JOB = f"5081::{label}"
    M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
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
            int(profile["relative_adaptive_maximum_intervals"]),
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
    value = M5077.M5036.M5035.M5034.highest_value(gate)
    result = {
        "checkpoint_marker": MARKER,
        "label": label,
        "runtime_seconds": time.monotonic() - started,
        "converged": bool(gate["fixed_event_crossed_integral_converged"]),
        "highest_value": M5077.M5036.complex_row(value),
        "topological_correction": gate["topological_correction"],
        "radius_adjustments": list(M5077.M5036.MREPAIR.RADIUS_AUDIT),
        "fixed_event_integral_gate": gate,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(SOURCE / f"{label}_kernel_gate.json", result)
    return result


def main() -> None:
    config_path = FAILED_RUN / "config.json"
    source_path = (
        FAILED_RUN / "topologies" / f"{EVENT_ID}__{SOURCE_ARGUMENT_ID}.json"
    )
    failed_job = FAILED_RUN / "jobs" / f"E040__{EVENT_ID}__A00__primary24.json"
    required = [SCRIPT_5077, config_path, source_path, failed_job]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5081 source inputs: {missing}")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    source_document = json.loads(source_path.read_text(encoding="utf-8"))
    events = M5077.M5036.event_lookup(config)
    arguments = M5077.M5036.argument_lookup(config)
    event = events[EVENT_ID]
    target_argument = arguments[TARGET_ARGUMENT_ID]
    target = M5077.M5036.complex_from_row(target_argument["target_cosine"])
    original_levels = tuple(M5069.FEYNMAN_STEP_LEVELS)
    original_certificate, original_rows = M5069.certify_segment(
        source_document, target, "E040_ARGUMENT_ADJACENCY"
    )
    M5069.FEYNMAN_STEP_LEVELS = EXTENDED_LEVELS
    try:
        certificate, extended_rows = M5069.certify_segment(
            source_document, target, "E040_ARGUMENT_ADJACENCY"
        )
    finally:
        M5069.FEYNMAN_STEP_LEVELS = original_levels
    if certificate is None:
        raise RuntimeError("the appended 2048 level did not certify the fresh segment")
    transported, transport_diagnostics = M5069.construct_path_transported_document(
        source_document,
        target,
        source_path,
        "E040_ARGUMENT_ADJACENCY",
        certificate,
    )
    constructed = M5069.compose_document(transported, certificate)
    constructed.update(
        {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "config_digest": config["config_digest"],
            "event_id": EVENT_ID,
            "argument_id": TARGET_ARGUMENT_ID,
            "valid_for_full_MTS_claim": False,
        }
    )
    constructed_path = SOURCE / "constructed_E040_A04.json"
    atomic_json(constructed_path, constructed)
    full_document, full_path, full_runtime = M5077.ORIGINAL_OBTAIN_TOPOLOGY(
        SCRATCH,
        config,
        event,
        target_argument,
    )
    recorded_full_runtime = max(
        full_runtime,
        float(full_document.get("topology_runtime_seconds", 0.0) or 0.0),
    )
    signature_exact = (
        constructed["topology_signature_digest"]
        == full_document["topology_signature_digest"]
    )
    class_exact = (
        constructed["topology_class_descriptor"]
        == full_document["topology_class_descriptor"]
    )
    contract_exact = M5061.canonical_digest(
        M5061.kernel_contract(constructed)
    ) == M5061.canonical_digest(M5061.kernel_contract(full_document))
    endpoint_error = M5061.endpoint_error(constructed, full_document)
    full_gate = kernel_gate(config, event, target, full_document, "full_target")
    constructed_gate = kernel_gate(
        config, event, target, constructed, "constructed_target"
    )
    full_value = M5077.M5036.complex_from_row(full_gate["highest_value"])
    constructed_value = M5077.M5036.complex_from_row(
        constructed_gate["highest_value"]
    )
    kernel_absolute, kernel_relative = complex_distance(
        full_value, constructed_value
    )
    full_correction = parse_complex(full_gate["topological_correction"])
    constructed_correction = parse_complex(
        constructed_gate["topological_correction"]
    )
    correction_absolute, correction_relative = complex_distance(
        full_correction, constructed_correction
    )
    original_last = original_rows[-1]
    extended_selected = int(certificate["resolution"])
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "source_argument_id": SOURCE_ARGUMENT_ID,
        "target_argument_id": TARGET_ARGUMENT_ID,
        "original_levels": list(original_levels),
        "extended_levels": list(EXTENDED_LEVELS),
        "extension_is_append_only": tuple(EXTENDED_LEVELS[:-1])
        == original_levels,
        "original_certificate_failed": original_certificate is None,
        "original_final_resolution": int(original_last["resolution"]),
        "original_final_transition_count": int(
            original_last["total_transition_count"]
        ),
        "original_final_maximum_projective_step": float(
            original_last["maximum_projective_assignment_step"]
        ),
        "extended_selected_resolution": extended_selected,
        "extended_transition_count": int(certificate["total_transition_count"]),
        "extended_maximum_projective_step": float(
            certificate["maximum_projective_assignment_step"]
        ),
        "path_root_transport_valid": bool(
            transport_diagnostics["path_root_transport_valid"]
        ),
        "signature_exact": signature_exact,
        "class_exact": class_exact,
        "kernel_contract_exact": contract_exact,
        "maximum_endpoint_log_error": endpoint_error,
        "full_target_path": str(full_path),
        "full_target_runtime_seconds": recorded_full_runtime,
        "constructed_target_path": str(constructed_path),
        "full_kernel_converged": full_gate["converged"],
        "constructed_kernel_converged": constructed_gate["converged"],
        "kernel_absolute_difference": kernel_absolute,
        "kernel_relative_difference": kernel_relative,
        "topological_correction_absolute_difference": correction_absolute,
        "topological_correction_relative_difference": correction_relative,
        "production_resolution_extension_supported": all(
            (
                signature_exact,
                class_exact,
                contract_exact,
                endpoint_error < 1.0e-10,
                full_gate["converged"],
                constructed_gate["converged"],
                kernel_relative <= 1.0e-12,
                correction_relative <= 1.0e-12,
            )
        ),
        "pilot_execution_authorized": False,
        "next_required_gate": "install the append-only 2048 level in a new runner revision and restart under a new config digest",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", all(path.exists() for path in required), "failed fresh segment is fully sourced"),
        ("old_failure_reproduced", result["original_certificate_failed"], f"last={result['original_final_resolution']}"),
        ("append_only_extension", result["extension_is_append_only"], str(result["extended_levels"])),
        ("extended_certificate", extended_selected == 2048 and result["extended_maximum_projective_step"] < M5069.PROJECTIVE_LIMIT, f"selected={extended_selected}; step={result['extended_maximum_projective_step']}"),
        ("full_target_equivalence", signature_exact and class_exact and contract_exact and endpoint_error < 1.0e-10, f"endpoint={endpoint_error}"),
        ("kernel_replay_equivalence", full_gate["converged"] and constructed_gate["converged"] and kernel_relative <= 1.0e-12 and correction_relative <= 1.0e-12, f"kernel={kernel_relative}; correction={correction_relative}"),
        ("production_extension_supported", result["production_resolution_extension_supported"], "all topology and kernel gates pass"),
        ("restart_required", not result["pilot_execution_authorized"], "new config digest required before resuming"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "resolution repair is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5081_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5081 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
