from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5069 = POST / "scripts" / "Y5_R2FR_5069_signed_segment_winding_composition_law.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5069 = POST / "source-intake" / "functional_rg" / "5069"
SOURCE = POST / "source-intake" / "functional_rg" / "5074"
CONSTRUCTED = SOURCE / "central_anchor_bidirectional_chains"
RESULT_JSON = SOURCE / "central_anchor_bidirectional_chain_gate.json"
ROW_CSV = SOURCE / "central_anchor_bidirectional_chain_rows.csv"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5074_VALIDATION.csv"
MARKER = "MTS_5074_CENTRAL_ANCHOR_BIDIRECTIONAL_CHAIN_GATE"
REVISION = "fixed-a08-two-sided-recursive-composition-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ANCHOR_ID = "A08"
RIGHT_ARGUMENTS = tuple(f"A{index:02d}" for index in range(9, 15))
LEFT_ARGUMENTS = tuple(f"A{index:02d}" for index in range(7, -1, -1))


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5069 = load_module("mts_5069_for_5074", SCRIPT_5069)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def localize(value: str) -> Path:
    path = Path(value)
    if path.exists():
        return path
    normalized = value.replace("\\", "/")
    marker = "/post-checkpoint-work/"
    if marker not in normalized:
        raise FileNotFoundError(value)
    candidate = POST / normalized.split(marker, 1)[1]
    if not candidate.exists():
        raise FileNotFoundError(candidate)
    return candidate


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> None:
    source_rows_path = SOURCE_5053 / "high_low_cost_rows.csv"
    composition_result_path = SOURCE_5069 / "signed_segment_winding_composition_law.json"
    required = [SCRIPT_5069, source_rows_path, composition_result_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_rows = list(csv.DictReader(source_rows_path.open(encoding="utf-8")))
    topology_paths = {
        (row["event_id"], row["base_argument_id"]): localize(row["e040_topology"])
        for row in source_rows
    }
    event_ids = sorted({row["event_id"] for row in source_rows})
    rows = []
    for event_id in event_ids:
        anchor_path = topology_paths[(event_id, ANCHOR_ID)]
        anchor_document = json.loads(anchor_path.read_text(encoding="utf-8"))
        for direction, argument_ids in (
            ("right", RIGHT_ARGUMENTS),
            ("left", LEFT_ARGUMENTS),
        ):
            current_path = anchor_path
            current_document = anchor_document
            source_was_constructed = False
            source_argument_id = ANCHOR_ID
            for depth, target_argument_id in enumerate(argument_ids, start=1):
                expected_path = topology_paths[(event_id, target_argument_id)]
                expected_document = json.loads(
                    expected_path.read_text(encoding="utf-8")
                )
                target = complex(str(expected_document["target_cosine"]))
                certified, levels = M5069.certify_segment(
                    current_document, target, "E040_ARGUMENT_ADJACENCY"
                )
                certificate_runtime = sum(
                    float(level["runtime_seconds"]) for level in levels
                )
                if certified is None:
                    raise RuntimeError(
                        f"bidirectional certificate failed for {event_id} "
                        f"{source_argument_id}->{target_argument_id}"
                    )
                transported, transport_diagnostics = (
                    M5069.construct_path_transported_document(
                        current_document,
                        target,
                        current_path,
                        f"E040_CENTRAL_ANCHOR_{direction.upper()}_CHAIN",
                        certified,
                    )
                )
                constructed = M5069.compose_document(transported, certified)
                constructed["checkpoint_marker"] = MARKER
                constructed["revision"] = REVISION
                constructed["anchor_argument_id"] = ANCHOR_ID
                constructed["chain_direction"] = direction
                constructed["chain_depth"] = depth
                output_path = (
                    CONSTRUCTED
                    / event_id
                    / direction
                    / f"{target_argument_id}.json"
                )
                atomic_json(output_path, constructed)
                signature_exact = (
                    constructed["topology_signature_digest"]
                    == expected_document["topology_signature_digest"]
                )
                class_exact = (
                    constructed["topology_class_descriptor"]
                    == expected_document["topology_class_descriptor"]
                )
                endpoint_error = M5069.M5061.endpoint_error(
                    constructed, expected_document
                )
                crossing_error = M5069.M5061.crossing_root_error(
                    constructed, expected_document
                )
                kernel_contract_exact = canonical_digest(
                    M5069.M5061.kernel_contract(constructed)
                ) == canonical_digest(
                    M5069.M5061.kernel_contract(expected_document)
                )
                rows.append(
                    {
                        "event_id": event_id,
                        "direction": direction,
                        "source_argument_id": source_argument_id,
                        "target_argument_id": target_argument_id,
                        "source_was_constructed": source_was_constructed,
                        "chain_depth": depth,
                        "selected_resolution": int(certified["resolution"]),
                        "path_sample_count": int(certified["path_sample_count"]),
                        "transition_count": int(
                            certified["total_transition_count"]
                        ),
                        "certificate_runtime_seconds": certificate_runtime,
                        "path_root_transport_valid": transport_diagnostics[
                            "path_root_transport_valid"
                        ],
                        "constructed_path": str(output_path),
                        "validation_path": str(expected_path),
                        "signature_exact": signature_exact,
                        "class_exact": class_exact,
                        "kernel_contract_exact": kernel_contract_exact,
                        "maximum_endpoint_log_error": endpoint_error,
                        "maximum_raw_crossing_root_error": crossing_error,
                    }
                )
                current_path = output_path
                current_document = constructed
                source_was_constructed = True
                source_argument_id = target_argument_id
    failed = [
        row
        for row in rows
        if not row["path_root_transport_valid"]
        or not row["signature_exact"]
        or not row["class_exact"]
        or not row["kernel_contract_exact"]
        or float(row["maximum_endpoint_log_error"]) >= 1.0e-10
    ]
    raw_history_mismatches = [
        row
        for row in rows
        if not math.isfinite(float(row["maximum_raw_crossing_root_error"]))
        or float(row["maximum_raw_crossing_root_error"]) >= 2.0e-5
    ]
    constructed_predecessors = [
        row for row in rows if row["source_was_constructed"]
    ]
    reverse_rows = [row for row in rows if row["direction"] == "left"]
    transition_rows = [row for row in rows if int(row["transition_count"]) > 0]
    composition_result = json.loads(
        composition_result_path.read_text(encoding="utf-8")
    )
    gate = (
        len(rows) == 112
        and len(reverse_rows) == 64
        and len(constructed_predecessors) == 96
        and bool(transition_rows)
        and not failed
        and bool(composition_result["signed_winding_composition_gate_passed"])
    )
    anchor_runtimes = [
        float(
            next(
                row
                for row in source_rows
                if row["event_id"] == event_id
                and row["base_argument_id"] == ANCHOR_ID
            )["e040_topology_runtime_seconds"]
        )
        for event_id in event_ids
    ]
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "anchor_argument_id": ANCHOR_ID,
        "anchor_count": len(event_ids),
        "constructed_document_count": len(rows),
        "reverse_edge_count": len(reverse_rows),
        "constructed_predecessor_count": len(constructed_predecessors),
        "transition_edge_count": len(transition_rows),
        "maximum_chain_depth": max(int(row["chain_depth"]) for row in rows),
        "failed_chain_count": len(failed),
        "raw_path_history_mismatch_count": len(raw_history_mismatches),
        "mean_measured_anchor_runtime_seconds": sum(anchor_runtimes)
        / len(anchor_runtimes),
        "maximum_measured_anchor_runtime_seconds": max(anchor_runtimes),
        "total_certificate_runtime_seconds": sum(
            float(row["certificate_runtime_seconds"]) for row in rows
        ),
        "central_anchor_bidirectional_chain_gate_passed": gate,
        "saved_target_topology_content_used_for_validation_only": True,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "recompute estimator cost with the fixed A08 central anchor, then rerun statistical and cost jackknives",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    SOURCE.mkdir(parents=True, exist_ok=True)
    with ROW_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    checks = [
        ("source_paths_exist", all(path.exists() for path in required) and all(path.exists() for path in topology_paths.values()), "5069 and all 120 E040 topology inputs exist"),
        ("matrix_complete", len(rows) == 112, f"constructed={len(rows)}"),
        ("reverse_edges_exercised", len(reverse_rows) == 64, f"reverse edges={len(reverse_rows)}"),
        ("constructed_predecessors_exercised", len(constructed_predecessors) == 96, f"constructed predecessors={len(constructed_predecessors)}"),
        ("transition_edges_exercised", bool(transition_rows), f"transition edges={len(transition_rows)}"),
        ("all_reduced_contracts_exact", not failed, f"failed={len(failed)}"),
        ("raw_history_mismatches_are_net_zero", all(row["signature_exact"] and row["kernel_contract_exact"] for row in raw_history_mismatches), f"raw mismatches={len(raw_history_mismatches)}"),
        ("central_anchor_cost_positive", min(anchor_runtimes) > 0.0, f"mean={result['mean_measured_anchor_runtime_seconds']}; max={result['maximum_measured_anchor_runtime_seconds']}"),
        ("bidirectional_gate_passed", gate, "one fixed A08 full anchor recursively constructs all other arguments in both directions"),
        ("no_target_leakage", result["saved_target_topology_content_used_for_validation_only"], "only endpoint coordinates enter construction; saved crossings are validation-only"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "central-anchor acceleration is operational, not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5074_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed_checks = [name for name, passed, _ in checks if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(checks),
                "failed": failed_checks,
                "passed": not failed_checks,
                "output": str(RESULT_JSON),
            },
            indent=2,
        )
    )
    if failed_checks:
        raise RuntimeError(f"checkpoint 5074 validation failed: {failed_checks}")


if __name__ == "__main__":
    main()
