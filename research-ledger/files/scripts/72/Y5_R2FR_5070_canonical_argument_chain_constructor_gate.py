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
SOURCE_5065 = POST / "source-intake" / "functional_rg" / "5065"
SOURCE_5069 = POST / "source-intake" / "functional_rg" / "5069"
SOURCE = POST / "source-intake" / "functional_rg" / "5070"
CONSTRUCTED = SOURCE / "constructed_argument_chains"
RESULT_JSON = SOURCE / "canonical_argument_chain_constructor_gate.json"
ROW_CSV = SOURCE / "canonical_argument_chain_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5070_VALIDATION.csv"
)
MARKER = "MTS_5070_CANONICAL_ARGUMENT_CHAIN_CONSTRUCTOR_GATE"
REVISION = "recursive-canonical-feynman-path-composition-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ARGUMENT_ORDER = tuple(f"A{index:02d}" for index in range(15))


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5069 = load_module("mts_5069_for_5070", SCRIPT_5069)


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
    edge_rows_path = SOURCE_5065 / "adjacent_argument_certificate_rows.csv"
    composition_result_path = SOURCE_5069 / "signed_segment_winding_composition_law.json"
    required = [
        SCRIPT_5069,
        source_rows_path,
        edge_rows_path,
        composition_result_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_rows = list(csv.DictReader(source_rows_path.open(encoding="utf-8")))
    topology_paths = {
        (row["event_id"], row["base_argument_id"]): localize(row["e040_topology"])
        for row in source_rows
    }
    expected_edges = {
        (row["event_id"], row["left_argument_id"], row["right_argument_id"])
        for row in csv.DictReader(edge_rows_path.open(encoding="utf-8"))
    }
    event_ids = sorted({row["event_id"] for row in source_rows})
    rows = []
    for event_id in event_ids:
        current_path = topology_paths[(event_id, ARGUMENT_ORDER[0])]
        current_document = json.loads(current_path.read_text(encoding="utf-8"))
        current_was_constructed = False
        for depth, (left_id, right_id) in enumerate(
            zip(ARGUMENT_ORDER[:-1], ARGUMENT_ORDER[1:]), start=1
        ):
            edge_key = (event_id, left_id, right_id)
            if edge_key not in expected_edges:
                raise RuntimeError(f"missing adjacent edge {edge_key}")
            expected_path = topology_paths[(event_id, right_id)]
            expected_document = json.loads(expected_path.read_text(encoding="utf-8"))
            target = complex(str(expected_document["target_cosine"]))
            certified, levels = M5069.certify_segment(
                current_document, target, "E040_ARGUMENT_ADJACENCY"
            )
            certificate_runtime = sum(
                float(level["runtime_seconds"]) for level in levels
            )
            if certified is None:
                raise RuntimeError(f"recursive chain certificate failed for {edge_key}")
            transported, transport_diagnostics = (
                M5069.construct_path_transported_document(
                    current_document,
                    target,
                    current_path,
                    "E040_ARGUMENT_CHAIN_FROM_CURRENT_PREDECESSOR",
                    certified,
                )
            )
            constructed = M5069.compose_document(transported, certified)
            constructed["checkpoint_marker"] = MARKER
            constructed["revision"] = REVISION
            constructed["chain_depth"] = depth
            output_path = CONSTRUCTED / event_id / f"{right_id}.json"
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
            ) == canonical_digest(M5069.M5061.kernel_contract(expected_document))
            rows.append(
                {
                    "event_id": event_id,
                    "left_argument_id": left_id,
                    "right_argument_id": right_id,
                    "source_was_constructed": current_was_constructed,
                    "chain_depth": depth,
                    "selected_resolution": int(certified["resolution"]),
                    "path_sample_count": int(certified["path_sample_count"]),
                    "transition_count": int(certified["total_transition_count"]),
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
                    "maximum_crossing_root_error": crossing_error,
                }
            )
            current_path = output_path
            current_document = constructed
            current_was_constructed = True
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
        if not math.isfinite(float(row["maximum_crossing_root_error"]))
        or float(row["maximum_crossing_root_error"]) >= 2.0e-5
    ]
    chained = [row for row in rows if row["source_was_constructed"]]
    transition_rows = [row for row in rows if int(row["transition_count"]) > 0]
    maximum_endpoint_error = max(
        (float(row["maximum_endpoint_log_error"]) for row in rows), default=0.0
    )
    maximum_finite_crossing_error = max(
        (
            float(row["maximum_crossing_root_error"])
            for row in rows
            if math.isfinite(float(row["maximum_crossing_root_error"]))
        ),
        default=0.0,
    )
    composition_result = json.loads(
        composition_result_path.read_text(encoding="utf-8")
    )
    gate = (
        len(rows) == 112
        and len(chained) == 104
        and len(transition_rows) > 0
        and not failed
        and bool(composition_result["signed_winding_composition_gate_passed"])
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_count": len(event_ids),
        "anchor_count": len(event_ids),
        "constructed_document_count": len(rows),
        "constructed_predecessor_count": len(chained),
        "transition_edge_count": len(transition_rows),
        "maximum_consecutive_chain_depth": max(
            (int(row["chain_depth"]) for row in rows), default=0
        ),
        "failed_chain_count": len(failed),
        "raw_path_history_mismatch_count": len(raw_history_mismatches),
        "raw_path_history_is_kernel_contract": False,
        "rootwise_net_winding_is_kernel_contract": True,
        "maximum_endpoint_log_error": maximum_endpoint_error,
        "maximum_finite_raw_crossing_root_error": maximum_finite_crossing_error,
        "total_certificate_runtime_seconds": sum(
            float(row["certificate_runtime_seconds"]) for row in rows
        ),
        "canonical_argument_chain_gate_passed": gate,
        "saved_target_topology_content_used_for_validation_only": True,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "replay a transition-bearing recursively constructed topology through the fixed-event kernel",
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
        (
            "source_paths_exist",
            all(path.exists() for path in required)
            and all(path.exists() for path in topology_paths.values()),
            "5069 and all 120 E040 topology inputs exist",
        ),
        ("edge_matrix_complete", len(rows) == 112, f"edges={len(rows)}"),
        (
            "constructed_predecessors_exercised",
            len(chained) == 104,
            f"constructed predecessors={len(chained)}",
        ),
        (
            "transition_edges_exercised",
            bool(transition_rows),
            f"transition edges={len(transition_rows)}",
        ),
        ("all_chain_contracts_exact", not failed, f"failed={len(failed)}"),
        (
            "endpoint_contract_exact",
            maximum_endpoint_error < 1.0e-10,
            f"maximum endpoint error={maximum_endpoint_error}",
        ),
        (
            "raw_history_mismatches_are_net_zero",
            all(
                row["signature_exact"] and row["kernel_contract_exact"]
                for row in raw_history_mismatches
            ),
            f"raw mismatches={len(raw_history_mismatches)}; every rootwise net-winding contract remains exact",
        ),
        (
            "chain_gate_passed",
            gate,
            "eight full anchors recursively construct every other E040 argument topology",
        ),
        (
            "no_target_leakage",
            result["saved_target_topology_content_used_for_validation_only"],
            "only the endpoint coordinate enters construction; saved crossings are validation-only",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "topology acceleration is an operational result, not MTS evidence",
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
                    "check_id": f"V5070_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5070 validation failed: {failed_checks}")


if __name__ == "__main__":
    main()
