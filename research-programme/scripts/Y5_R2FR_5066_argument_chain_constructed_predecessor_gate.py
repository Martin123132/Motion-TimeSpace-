from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5061 = POST / "scripts" / "Y5_R2FR_5061_serialized_transport_topology_constructor_dry_run.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5065 = POST / "source-intake" / "functional_rg" / "5065"
SOURCE = POST / "source-intake" / "functional_rg" / "5066"
CONSTRUCTED = SOURCE / "constructed_argument_chains"
RESULT_JSON = SOURCE / "argument_chain_constructed_predecessor_gate.json"
ROW_CSV = SOURCE / "argument_chain_constructor_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5066_VALIDATION.csv"
)
MARKER = "MTS_5066_ARGUMENT_CHAIN_CONSTRUCTED_PREDECESSOR_GATE"
REVISION = "transported-predecessor-chain-equivalence-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ARGUMENT_ORDER = tuple(f"A{index:02d}" for index in range(15))


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5061 = load_module("mts_5061_for_5066", SCRIPT_5061)


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
    source_result_path = SOURCE_5065 / "adjacent_argument_transport_certificate_benchmark.json"
    required = [SCRIPT_5061, source_rows_path, edge_rows_path, source_result_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_rows = list(csv.DictReader(source_rows_path.open(encoding="utf-8")))
    topology_paths = {
        (row["event_id"], row["base_argument_id"]): localize(row["e040_topology"])
        for row in source_rows
    }
    edge_rows = {
        (row["event_id"], row["left_argument_id"], row["right_argument_id"]): row
        for row in csv.DictReader(edge_rows_path.open(encoding="utf-8"))
    }
    event_ids = sorted({row["event_id"] for row in source_rows})
    rows = []
    maximum_chain_depth = 0
    for event_id in event_ids:
        current_path = topology_paths[(event_id, ARGUMENT_ORDER[0])]
        current_document = json.loads(current_path.read_text(encoding="utf-8"))
        current_was_constructed = False
        chain_depth = 0
        for left_id, right_id in zip(ARGUMENT_ORDER[:-1], ARGUMENT_ORDER[1:]):
            edge = edge_rows[(event_id, left_id, right_id)]
            expected_path = topology_paths[(event_id, right_id)]
            expected_document = json.loads(expected_path.read_text(encoding="utf-8"))
            if edge["decision"] != "DIRECT_ROOT_TRANSPORT":
                rows.append(
                    {
                        "event_id": event_id,
                        "left_argument_id": left_id,
                        "right_argument_id": right_id,
                        "source_was_constructed": current_was_constructed,
                        "incoming_chain_depth": chain_depth,
                        "decision": edge["decision"],
                        "constructed_path": "",
                        "signature_exact": None,
                        "class_exact": None,
                        "kernel_contract_exact": None,
                        "maximum_endpoint_log_error": None,
                        "maximum_crossing_root_error": None,
                    }
                )
                current_path = expected_path
                current_document = expected_document
                current_was_constructed = False
                chain_depth = 0
                continue
            target_cosine = complex(str(expected_document["target_cosine"]))
            constructed = M5061.construct_document(
                current_document,
                target_cosine.imag,
                current_path,
                "E040_ARGUMENT_CHAIN_FROM_CURRENT_PREDECESSOR",
                target_cosine,
            )
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
            endpoint_maximum = M5061.endpoint_error(constructed, expected_document)
            crossing_maximum = M5061.crossing_root_error(
                constructed, expected_document
            )
            contract_exact = canonical_digest(M5061.kernel_contract(constructed)) == canonical_digest(
                M5061.kernel_contract(expected_document)
            )
            incoming_depth = chain_depth
            chain_depth += 1
            maximum_chain_depth = max(maximum_chain_depth, chain_depth)
            rows.append(
                {
                    "event_id": event_id,
                    "left_argument_id": left_id,
                    "right_argument_id": right_id,
                    "source_was_constructed": current_was_constructed,
                    "incoming_chain_depth": incoming_depth,
                    "decision": "DIRECT_ROOT_TRANSPORT",
                    "constructed_path": str(output_path),
                    "signature_exact": signature_exact,
                    "class_exact": class_exact,
                    "kernel_contract_exact": contract_exact,
                    "maximum_endpoint_log_error": endpoint_maximum,
                    "maximum_crossing_root_error": crossing_maximum,
                }
            )
            current_path = output_path
            current_document = constructed
            current_was_constructed = True
    transported = [row for row in rows if row["decision"] == "DIRECT_ROOT_TRANSPORT"]
    chained = [row for row in transported if row["source_was_constructed"]]
    failed = [
        row
        for row in transported
        if not row["signature_exact"]
        or not row["class_exact"]
        or not row["kernel_contract_exact"]
        or float(row["maximum_endpoint_log_error"]) >= 1.0e-10
        or float(row["maximum_crossing_root_error"]) >= 2.0e-5
    ]
    maximum_endpoint_error = max(
        (float(row["maximum_endpoint_log_error"]) for row in transported),
        default=0.0,
    )
    maximum_crossing_error = max(
        (float(row["maximum_crossing_root_error"]) for row in transported),
        default=0.0,
    )
    source_result = json.loads(source_result_path.read_text(encoding="utf-8"))
    gate = (
        len(rows) == 112
        and len(transported) == int(source_result["direct_transport_edge_count"])
        and not failed
        and bool(chained)
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "edge_count": len(rows),
        "transported_document_count": len(transported),
        "transported_predecessor_count": len(chained),
        "maximum_consecutive_transport_depth": maximum_chain_depth,
        "failed_chain_transport_count": len(failed),
        "maximum_endpoint_log_error": maximum_endpoint_error,
        "maximum_crossing_root_error": maximum_crossing_error,
        "constructed_predecessor_gate_passed": gate,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "recompute unit-consistent estimator cost with both epsilon and argument topology transport",
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
            "5061, 5065, and all E040 topology inputs exist",
        ),
        (
            "edge_matrix_complete",
            len(rows) == 112,
            f"edges={len(rows)}",
        ),
        (
            "transport_count_reproduced",
            len(transported) == int(source_result["direct_transport_edge_count"]),
            f"transport={len(transported)}",
        ),
        (
            "constructed_sources_exercised",
            bool(chained) and maximum_chain_depth >= 2,
            f"constructed sources={len(chained)}; max depth={maximum_chain_depth}",
        ),
        (
            "all_chain_signatures_exact",
            not failed,
            f"failed={len(failed)}",
        ),
        (
            "endpoint_contract_exact",
            maximum_endpoint_error < 1.0e-10,
            f"maximum endpoint error={maximum_endpoint_error}",
        ),
        (
            "crossing_contract_exact",
            maximum_crossing_error < 2.0e-5,
            f"maximum crossing error={maximum_crossing_error}",
        ),
        (
            "chain_gate_passed",
            gate,
            "transport remains exact when its predecessor is itself constructed",
        ),
        (
            "no_fresh_kernel_execution",
            not result["fresh_kernel_execution_authorized"],
            "chain gate compares saved full topology contracts only",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "argument-chain acceleration is not a physical claim",
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
                    "check_id": f"V5066_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5066 validation failed: {failed_checks}")


if __name__ == "__main__":
    main()
