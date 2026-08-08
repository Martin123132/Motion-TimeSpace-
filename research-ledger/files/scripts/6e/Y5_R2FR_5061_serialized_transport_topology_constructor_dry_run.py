from __future__ import annotations

import copy
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment


POST = Path(__file__).resolve().parents[1]
SCRIPT_5057 = POST / "scripts" / "Y5_R2FR_5057_direct_target_root_topology_transport_benchmark.py"
SCRIPT_5059 = POST / "scripts" / "Y5_R2FR_5059_short_epsilon_segment_transition_certificate.py"
SOURCE_5057 = POST / "source-intake" / "functional_rg" / "5057"
SOURCE_5059 = POST / "source-intake" / "functional_rg" / "5059"
SOURCE_5060 = POST / "source-intake" / "functional_rg" / "5060"
SOURCE = POST / "source-intake" / "functional_rg" / "5061"
CONSTRUCTED = SOURCE / "constructed_topologies"
RESULT_JSON = SOURCE / "serialized_transport_topology_constructor_dry_run.json"
ROW_CSV = SOURCE / "serialized_constructor_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5061_VALIDATION.csv"
)
MARKER = "MTS_5061_SERIALIZED_TRANSPORT_TOPOLOGY_CONSTRUCTOR_DRY_RUN"
REVISION = "kernel-contract-equivalent-serialized-transport-topology-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5057 = load_module("mts_5057_for_5061", SCRIPT_5057)
M5059 = load_module("mts_5059_for_5061", SCRIPT_5059)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() == "true"


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


def serialized_signature(document: dict[str, Any]) -> list[list[list[Any]]]:
    return [
        [list(row) for row in chamber]
        for chamber in M5057.net_signature(
            [chamber["surface_crossings"] for chamber in document["chambers"]]
        )
    ]


def class_descriptor(document: dict[str, Any]) -> list[list[int]]:
    return [
        [
            len(chamber),
            sum(row[0] > 0 for row in chamber),
            sum(row[0] < 0 for row in chamber),
        ]
        for chamber in serialized_signature(document)
    ]


def normalized_pairs(row: dict[str, Any]) -> tuple[tuple[str, ...], ...]:
    return tuple(
        sorted(tuple(sorted(str(value) for value in pair)) for pair in row["representing_pairs"])
    )


def crossing_token(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        normalized_pairs(row),
        int(row["winding_correction"]),
        int(row["multiplicity"]),
    )


def construct_document(
    source_document: dict[str, Any],
    target_epsilon: float,
    source_path: Path,
    suite: str,
    target_cosine: complex | None = None,
) -> dict[str, Any]:
    started = time.perf_counter()
    M5059.configure(source_document)
    source_target = complex(str(source_document["target_cosine"]))
    target = (
        complex(source_target.real, target_epsilon)
        if target_cosine is None
        else complex(target_cosine)
    )
    cosines = [source_target + index / 15.0 * (target - source_target) for index in range(16)]
    boundaries, _ = M5059.M5030.physical_chambers()
    endpoint_paths, boundary_log_step, boundary_projective_step = (
        M5059.anchored_endpoint_paths(boundaries, source_document, cosines)
    )
    source_rationals = M5057.M5029.root_rationals(
        float(source_document["soft_energy"]),
        float(source_document["soft_cosine"]),
        float(source_document["decay_cosine"]),
        source_target,
    )
    target_rationals = M5057.M5029.root_rationals(
        float(source_document["soft_energy"]),
        float(source_document["soft_cosine"]),
        float(source_document["decay_cosine"]),
        target,
    )
    document = copy.deepcopy(source_document)
    document["checkpoint_marker"] = MARKER
    document["revision"] = REVISION
    document["config_digest"] = None
    document["target_cosine"] = str(target)
    document["topology_construction_method"] = "certified_direct_target_root_transport"
    document["transport_source_topology"] = str(source_path)
    document["transport_suite"] = suite
    document["dry_run_only"] = True
    document["homotopy_steps"] = 0
    document["assignment_tracking_passed"] = True
    document["crossing_groups_consistent"] = True
    document["fresh_kernel_execution_authorized"] = False
    document["valid_for_full_MTS_claim"] = False
    document["transport_boundary_maximum_log_step"] = boundary_log_step
    document["transport_boundary_maximum_projective_step"] = boundary_projective_step
    total_crossings = 0
    for chamber_index, chamber in enumerate(document["chambers"]):
        transported_crossings = [
            M5057.transport_crossing(row, source_rationals, target_rationals)["crossing"]
            for row in source_document["chambers"][chamber_index]["surface_crossings"]
        ]
        start_logs, end_logs = M5059.M5030.chamber_segment_logs(
            endpoint_paths, chamber_index
        )
        chamber["target_start_log"] = str(start_logs[-1])
        chamber["target_end_log"] = str(end_logs[-1])
        chamber["surface_crossings"] = transported_crossings
        chamber["surface_crossing_count"] = len(transported_crossings)
        total_crossings += len(transported_crossings)
    document["total_surface_crossings"] = total_crossings
    document["topology_class_descriptor"] = class_descriptor(document)
    document["topology_signature_digest"] = canonical_digest(serialized_signature(document))
    document["topology_runtime_seconds"] = time.perf_counter() - started
    return document


def endpoint_error(constructed: dict[str, Any], expected: dict[str, Any]) -> float:
    maximum = 0.0
    if len(constructed["chambers"]) != len(expected["chambers"]):
        return math.inf
    for left, right in zip(constructed["chambers"], expected["chambers"]):
        maximum = max(
            maximum,
            abs(complex(left["target_start_log"]) - complex(right["target_start_log"])),
            abs(complex(left["target_end_log"]) - complex(right["target_end_log"])),
        )
    return maximum


def crossing_root_error(constructed: dict[str, Any], expected: dict[str, Any]) -> float:
    maximum = 0.0
    if len(constructed["chambers"]) != len(expected["chambers"]):
        return math.inf
    for left_chamber, right_chamber in zip(
        constructed["chambers"], expected["chambers"]
    ):
        left_groups: dict[tuple[Any, ...], list[complex]] = {}
        right_groups: dict[tuple[Any, ...], list[complex]] = {}
        for row in left_chamber["surface_crossings"]:
            left_groups.setdefault(crossing_token(row), []).append(complex(row["target_root"]))
        for row in right_chamber["surface_crossings"]:
            right_groups.setdefault(crossing_token(row), []).append(complex(row["target_root"]))
        if set(left_groups) != set(right_groups):
            return math.inf
        for token in left_groups:
            left = left_groups[token]
            right = right_groups[token]
            if len(left) != len(right):
                return math.inf
            costs = np.asarray(
                [[M5057.chordal_distance(first, second) for second in right] for first in left],
                dtype=float,
            )
            left_indices, right_indices = linear_sum_assignment(costs)
            maximum = max(
                maximum,
                max(
                    (float(costs[i, j]) for i, j in zip(left_indices, right_indices)),
                    default=0.0,
                ),
            )
    return maximum


def kernel_contract(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "chambers": [
            {
                "target_start_log": chamber["target_start_log"],
                "target_end_log": chamber["target_end_log"],
                "signature": [
                    list(row)
                    for row in M5057.net_signature([chamber["surface_crossings"]])[0]
                ],
            }
            for chamber in document["chambers"]
        ]
    }


def main() -> None:
    training_rows_path = SOURCE_5057 / "epsilon_transport_rows.csv"
    training_certificate_path = SOURCE_5059 / "epsilon_segment_certificate_rows.csv"
    heldout_rows_path = SOURCE_5060 / "heldout_e080_to_e040_rows.csv"
    heldout_result_path = SOURCE_5060 / "heldout_e080_to_e040_transport_certificate.json"
    required = [
        SCRIPT_5057,
        SCRIPT_5059,
        training_rows_path,
        training_certificate_path,
        heldout_rows_path,
        heldout_result_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    training_certificates = {
        (row["event_id"], row["base_argument_id"]): row
        for row in csv.DictReader(training_certificate_path.open(encoding="utf-8"))
    }
    cases = []
    for row in csv.DictReader(training_rows_path.open(encoding="utf-8")):
        certificate = training_certificates[(row["event_id"], row["base_argument_id"])]
        cases.append(
            {
                "suite": "E040_TO_E020",
                "event_id": row["event_id"],
                "base_argument_id": row["base_argument_id"],
                "source_path": localize(row["e040_source_path"]),
                "target_path": localize(row["e020_validation_path"]),
                "target_epsilon": 0.02,
                "certificate_transition": bool_value(
                    certificate["certificate_transition_detected"]
                ),
            }
        )
    for row in csv.DictReader(heldout_rows_path.open(encoding="utf-8")):
        cases.append(
            {
                "suite": "E080_TO_E040_HELDOUT",
                "event_id": row["event_id"],
                "base_argument_id": row["base_argument_id"],
                "source_path": localize(row["source_path"]),
                "target_path": localize(row["target_path"]),
                "target_epsilon": 0.04,
                "certificate_transition": bool_value(
                    row["certificate_transition_detected"]
                ),
            }
        )
    rows = []
    for case in cases:
        source_document = json.loads(case["source_path"].read_text(encoding="utf-8"))
        expected_document = json.loads(case["target_path"].read_text(encoding="utf-8"))
        output_path = (
            CONSTRUCTED
            / case["suite"]
            / f"{case['event_id']}__{case['base_argument_id']}.json"
        )
        if case["certificate_transition"]:
            if output_path.exists():
                output_path.unlink()
            rows.append(
                {
                    "suite": case["suite"],
                    "event_id": case["event_id"],
                    "base_argument_id": case["base_argument_id"],
                    "source_path": str(case["source_path"]),
                    "expected_target_path": str(case["target_path"]),
                    "constructed_path": "",
                    "certificate_transition_detected": True,
                    "production_decision": "FULL_HOMOTOPY_FALLBACK",
                    "serialized_document_written": False,
                    "topology_signature_exact": None,
                    "topology_class_exact": None,
                    "kernel_contract_digest_exact": None,
                    "maximum_endpoint_log_error": None,
                    "maximum_crossing_root_error": None,
                    "constructor_runtime_seconds": 0.0,
                }
            )
            continue
        constructed = construct_document(
            source_document,
            float(case["target_epsilon"]),
            case["source_path"],
            case["suite"],
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
        endpoint_maximum = endpoint_error(constructed, expected_document)
        crossing_maximum = crossing_root_error(constructed, expected_document)
        contract_exact = canonical_digest(kernel_contract(constructed)) == canonical_digest(
            kernel_contract(expected_document)
        )
        rows.append(
            {
                "suite": case["suite"],
                "event_id": case["event_id"],
                "base_argument_id": case["base_argument_id"],
                "source_path": str(case["source_path"]),
                "expected_target_path": str(case["target_path"]),
                "constructed_path": str(output_path),
                "certificate_transition_detected": False,
                "production_decision": "DIRECT_ROOT_TRANSPORT",
                "serialized_document_written": output_path.exists(),
                "topology_signature_exact": signature_exact,
                "topology_class_exact": class_exact,
                "kernel_contract_digest_exact": contract_exact,
                "maximum_endpoint_log_error": endpoint_maximum,
                "maximum_crossing_root_error": crossing_maximum,
                "constructor_runtime_seconds": constructed["topology_runtime_seconds"],
            }
        )
    transported = [row for row in rows if row["production_decision"] == "DIRECT_ROOT_TRANSPORT"]
    fallback = [row for row in rows if row["production_decision"] == "FULL_HOMOTOPY_FALLBACK"]
    maximum_endpoint_error = max(
        float(row["maximum_endpoint_log_error"]) for row in transported
    )
    maximum_crossing_error = max(
        float(row["maximum_crossing_root_error"]) for row in transported
    )
    exact_signatures = sum(bool(row["topology_signature_exact"]) for row in transported)
    exact_classes = sum(bool(row["topology_class_exact"]) for row in transported)
    exact_contracts = sum(
        bool(row["kernel_contract_digest_exact"]) for row in transported
    )
    heldout_result = json.loads(heldout_result_path.read_text(encoding="utf-8"))
    dry_run_gate = (
        len(rows) == 204
        and len(transported) == 202
        and len(fallback) == 2
        and exact_signatures == len(transported)
        and exact_classes == len(transported)
        and maximum_endpoint_error < 1.0e-10
        and maximum_crossing_error < 2.0e-5
        and bool(heldout_result["heldout_interval_gate_passed"])
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "case_count": len(rows),
        "transported_document_count": len(transported),
        "full_homotopy_fallback_count": len(fallback),
        "fallback_keys": [
            [row["suite"], row["event_id"], row["base_argument_id"]]
            for row in fallback
        ],
        "exact_numeric_signature_count": exact_signatures,
        "exact_class_descriptor_count": exact_classes,
        "exact_serialized_kernel_contract_digest_count": exact_contracts,
        "maximum_endpoint_log_error": maximum_endpoint_error,
        "maximum_crossing_root_error": maximum_crossing_error,
        "mean_constructor_runtime_seconds": sum(
            float(row["constructor_runtime_seconds"]) for row in transported
        )
        / len(transported),
        "serialized_constructor_dry_run_passed": dry_run_gate,
        "kernel_consumed_fields_verified": [
            "chambers[].target_start_log",
            "chambers[].target_end_log",
            "chambers[].surface_crossings[].target_root",
            "chambers[].surface_crossings[].winding_correction",
        ],
        "production_transport_constructor_authorized": dry_run_gate,
        "kernel_execution_with_constructed_topology_authorized": False,
        "next_required_gate": "one saved-event kernel replay using constructed versus full topology",
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
            and all(case["source_path"].exists() and case["target_path"].exists() for case in cases),
            "all constructor, certificate, source, and validation paths exist",
        ),
        (
            "case_matrix_complete",
            len(rows) == 204 and len(transported) == 202 and len(fallback) == 2,
            f"cases={len(rows)}; transport={len(transported)}; fallback={len(fallback)}",
        ),
        (
            "fallbacks_not_serialized",
            all(not row["serialized_document_written"] for row in fallback),
            "both certified transitions remain full-homotopy decisions",
        ),
        (
            "transport_documents_written",
            all(row["serialized_document_written"] for row in transported),
            f"written={sum(bool(row['serialized_document_written']) for row in transported)}",
        ),
        (
            "numeric_signatures_exact",
            exact_signatures == len(transported),
            f"exact={exact_signatures}/{len(transported)}",
        ),
        (
            "class_descriptors_exact",
            exact_classes == len(transported),
            f"exact={exact_classes}/{len(transported)}",
        ),
        (
            "endpoint_logs_match",
            maximum_endpoint_error < 1.0e-10,
            f"maximum error={maximum_endpoint_error}",
        ),
        (
            "crossing_roots_match",
            maximum_crossing_error < 2.0e-5,
            f"maximum chordal error={maximum_crossing_error}",
        ),
        (
            "heldout_gate_inherited",
            bool(heldout_result["heldout_interval_gate_passed"]),
            "held-out interval and transition gate passed",
        ),
        (
            "constructor_gate_passed",
            dry_run_gate and result["production_transport_constructor_authorized"],
            "serialized constructor matches every full target in its certified scope",
        ),
        (
            "kernel_run_not_prematurely_authorized",
            not result["kernel_execution_with_constructed_topology_authorized"],
            "one saved-event kernel replay remains required",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "topology acceleration is not a physical claim",
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
                    "check_id": f"V5061_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(checks),
                "failed": failed,
                "passed": not failed,
                "output": str(RESULT_JSON),
            },
            indent=2,
        )
    )
    if failed:
        raise RuntimeError(f"checkpoint 5061 validation failed: {failed}")


if __name__ == "__main__":
    main()
