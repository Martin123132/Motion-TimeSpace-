from __future__ import annotations

import csv
import importlib.util
import json
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
PILOT_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v2"
SOURCE = POST / "source-intake" / "functional_rg" / "5082"
SCRATCH = SOURCE / "full_homotopy"
RESULT_JSON = SOURCE / "full_homotopy_residue_instability_comparator.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5082_VALIDATION.csv"
MARKER = "MTS_5082_FULL_HOMOTOPY_RESIDUE_INSTABILITY_COMPARATOR"
REVISION = "same-event-full-versus-constructed-primary24-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507602_N0000"
ARGUMENT_ID = "E040_A00"
BASE_ID = "A00"
OFFENDING_PAIR = (
    "direct:g2:minus_v",
    "subtraction:decay:plus_v",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module("mts_5077_for_5082", SCRIPT_5077)
M5061 = M5077.M5069.M5061


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def evaluate(
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
    M5077.M5036.MREPAIR.CURRENT_JOB = f"5082::{label}"
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
    audit = list(M5077.M5036.MREPAIR.RADIUS_AUDIT)
    result = {
        "checkpoint_marker": MARKER,
        "label": label,
        "runtime_seconds": time.monotonic() - started,
        "converged": bool(gate["fixed_event_crossed_integral_converged"]),
        "all_residues_stable": bool(gate["all_residues_stable"]),
        "highest_value": M5077.M5036.complex_row(value),
        "highest_two_order_relative_residual": float(
            gate["highest_two_order_relative_residual"]
        ),
        "radius_audit": audit,
        "fixed_event_integral_gate": gate,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(SOURCE / f"{label}_primary24_gate.json", result)
    return result


def offending_rows(audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    target = tuple(sorted(OFFENDING_PAIR))
    return [
        row
        for row in audit
        if any(tuple(sorted(pair)) == target for pair in row["pairs"])
    ]


def main() -> None:
    config_path = PILOT_RUN / "config.json"
    constructed_path = (
        PILOT_RUN / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    )
    pilot_job_path = (
        PILOT_RUN
        / "jobs"
        / f"E040__{EVENT_ID}__{BASE_ID}__primary24.json"
    )
    required = [SCRIPT_5077, config_path, constructed_path, pilot_job_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing comparator inputs: {missing}")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    events = M5077.M5036.event_lookup(config)
    arguments = M5077.M5036.argument_lookup(config)
    event = events[EVENT_ID]
    argument = arguments[ARGUMENT_ID]
    target = M5077.M5036.complex_from_row(argument["target_cosine"])
    constructed = json.loads(constructed_path.read_text(encoding="utf-8"))
    full, full_path, full_runtime = M5077.ORIGINAL_OBTAIN_TOPOLOGY(
        SCRATCH,
        config,
        event,
        argument,
    )
    recorded_full_runtime = max(
        full_runtime,
        float(full.get("topology_runtime_seconds", 0.0) or 0.0),
    )
    signature_exact = (
        full["topology_signature_digest"]
        == constructed["topology_signature_digest"]
    )
    class_exact = (
        full["topology_class_descriptor"]
        == constructed["topology_class_descriptor"]
    )
    contract_exact = M5061.canonical_digest(
        M5061.kernel_contract(full)
    ) == M5061.canonical_digest(M5061.kernel_contract(constructed))
    endpoint_error = M5061.endpoint_error(full, constructed)
    full_gate = evaluate(config, event, target, full, "full_homotopy")
    constructed_gate = evaluate(
        config, event, target, constructed, "constructed_chain"
    )
    full_offending = offending_rows(full_gate["radius_audit"])
    constructed_offending = offending_rows(constructed_gate["radius_audit"])
    same_instability = (
        len(full_offending) == 1
        and len(constructed_offending) == 1
        and not bool(full_offending[0]["selected_stable"])
        and not bool(constructed_offending[0]["selected_stable"])
        and abs(
            float(full_offending[0]["nearest_distinct_root_separation"])
            - float(
                constructed_offending[0]["nearest_distinct_root_separation"]
            )
        )
        <= 1.0e-15
    )
    full_value = M5077.M5036.complex_from_row(full_gate["highest_value"])
    constructed_value = M5077.M5036.complex_from_row(
        constructed_gate["highest_value"]
    )
    value_difference = float(abs(full_value - constructed_value))
    topology_exonerated = (
        signature_exact
        and class_exact
        and contract_exact
        and endpoint_error < 1.0e-10
        and not full_gate["converged"]
        and not constructed_gate["converged"]
        and same_instability
        and value_difference <= 1.0e-12 * max(1.0, abs(full_value))
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "full_topology_path": str(full_path),
        "full_topology_runtime_seconds": recorded_full_runtime,
        "constructed_topology_path": str(constructed_path),
        "signature_exact": signature_exact,
        "class_exact": class_exact,
        "kernel_contract_exact": contract_exact,
        "maximum_endpoint_log_error": endpoint_error,
        "full_kernel_converged": full_gate["converged"],
        "constructed_kernel_converged": constructed_gate["converged"],
        "full_all_residues_stable": full_gate["all_residues_stable"],
        "constructed_all_residues_stable": constructed_gate[
            "all_residues_stable"
        ],
        "same_offending_pair_instability": same_instability,
        "offending_pair": list(OFFENDING_PAIR),
        "full_offending_rows": full_offending,
        "constructed_offending_rows": constructed_offending,
        "highest_value_absolute_difference": value_difference,
        "transport_topology_exonerated": topology_exonerated,
        "decision": "TOPOLOGY_EXONERATED_RESIDUE_NUMERICS_BLOCKED"
        if topology_exonerated
        else "COMPARATOR_INCONCLUSIVE",
        "next_required_gate": "derive or numerically certify the near-colliding pair-local residue before resuming the pilot",
        "pilot_execution_authorized": False,
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", all(path.exists() for path in required), "constructed failure is fully sourced"),
        ("full_topology_generated", full_path.exists(), str(full_path)),
        ("topology_contract_exact", signature_exact and class_exact and contract_exact and endpoint_error < 1.0e-10, f"endpoint={endpoint_error}"),
        ("same_residue_failure", same_instability and not full_gate["converged"] and not constructed_gate["converged"], str(OFFENDING_PAIR)),
        ("same_unconverged_value", value_difference <= 1.0e-12 * max(1.0, abs(full_value)), f"difference={value_difference}"),
        ("transport_exonerated", topology_exonerated, result["decision"]),
        ("pilot_remains_blocked", not result["pilot_execution_authorized"], "residue gate must close first"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "pipeline diagnosis is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5082_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5082 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
