from __future__ import annotations

import collections
import csv
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5059 = POST / "scripts" / "Y5_R2FR_5059_short_epsilon_segment_transition_certificate.py"
SCRIPT_5061 = POST / "scripts" / "Y5_R2FR_5061_serialized_transport_topology_constructor_dry_run.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5056 = POST / "source-intake" / "functional_rg" / "5056"
SOURCE = POST / "source-intake" / "functional_rg" / "5065"
RESULT_JSON = SOURCE / "adjacent_argument_transport_certificate_benchmark.json"
ROW_CSV = SOURCE / "adjacent_argument_certificate_rows.csv"
EVENT_CSV = SOURCE / "argument_chain_event_costs.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5065_VALIDATION.csv"
)
MARKER = "MTS_5065_ADJACENT_ARGUMENT_TRANSPORT_CERTIFICATE_BENCHMARK"
REVISION = "e040-ordered-argument-chain-certificate-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
STEP_LEVELS = (8, 16, 32)
PROJECTIVE_LIMIT = 0.1
ARGUMENT_ORDER = tuple(f"A{index:02d}" for index in range(15))


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5059 = load_module("mts_5059_for_5065", SCRIPT_5059)
M5061 = load_module("mts_5061_for_5065", SCRIPT_5061)


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


def transport_class(document: dict[str, Any]) -> tuple[Any, ...]:
    chambers = []
    for chamber in document["chambers"]:
        counter = collections.Counter(
            crossing_token(row) for row in chamber["surface_crossings"]
        )
        chambers.append(tuple(sorted((token, count) for token, count in counter.items())))
    return tuple(chambers)


def main() -> None:
    source_rows_path = SOURCE_5053 / "high_low_cost_rows.csv"
    adjacency_path = SOURCE_5056 / "argument_adjacency_structural_comparison.csv"
    required = [SCRIPT_5059, SCRIPT_5061, source_rows_path, adjacency_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_rows = list(csv.DictReader(source_rows_path.open(encoding="utf-8")))
    row_map = {
        (row["event_id"], row["base_argument_id"]): row for row in source_rows
    }
    event_ids = sorted({row["event_id"] for row in source_rows})
    adjacency = {
        (row["event_id"], row["left_argument_id"], row["right_argument_id"]): row
        for row in csv.DictReader(adjacency_path.open(encoding="utf-8"))
        if row["epsilon_id"] == "E040"
    }
    rows = []
    for event_id in event_ids:
        for left_id, right_id in zip(ARGUMENT_ORDER[:-1], ARGUMENT_ORDER[1:]):
            source_row = row_map[(event_id, left_id)]
            target_row = row_map[(event_id, right_id)]
            source_path = localize(source_row["e040_topology"])
            target_path = localize(target_row["e040_topology"])
            source_document = json.loads(source_path.read_text(encoding="utf-8"))
            target_document = json.loads(target_path.read_text(encoding="utf-8"))
            target_cosine = complex(str(target_document["target_cosine"]))
            expected_class_equal = (
                transport_class(source_document) == transport_class(target_document)
            )
            sweep_equal = (
                adjacency[(event_id, left_id, right_id)]["crossing_multisets_equal"]
                == "True"
            )
            levels = [
                M5059.segment_gate(
                    source_document,
                    steps,
                    target_cosine.imag,
                    target_cosine,
                )
                for steps in STEP_LEVELS
            ]
            selected = levels[1]
            converged = all(
                level["transition_signature"] == levels[-1]["transition_signature"]
                for level in levels[:-1]
            )
            groups_consistent = all(level["groups_consistent"] for level in levels)
            maximum_projective_step = max(
                max(
                    level["maximum_projective_assignment_step"],
                    level["maximum_boundary_projective_step"],
                )
                for level in levels
            )
            certified = (
                converged
                and groups_consistent
                and maximum_projective_step < PROJECTIVE_LIMIT
            )
            transition_detected = bool(selected["transition_detected"])
            if not certified:
                decision = "FULL_HOMOTOPY_FALLBACK_UNCERTIFIED"
            elif transition_detected:
                decision = "FULL_HOMOTOPY_FALLBACK_TRANSITION"
            else:
                decision = "DIRECT_ROOT_TRANSPORT"
            constructed = None
            signature_exact = None
            class_exact = None
            endpoint_maximum = None
            crossing_maximum = None
            constructor_runtime = 0.0
            if decision == "DIRECT_ROOT_TRANSPORT":
                constructed = M5061.construct_document(
                    source_document,
                    target_cosine.imag,
                    source_path,
                    "E040_ARGUMENT_CHAIN",
                    target_cosine,
                )
                signature_exact = (
                    constructed["topology_signature_digest"]
                    == target_document["topology_signature_digest"]
                )
                class_exact = (
                    constructed["topology_class_descriptor"]
                    == target_document["topology_class_descriptor"]
                )
                endpoint_maximum = M5061.endpoint_error(constructed, target_document)
                crossing_maximum = M5061.crossing_root_error(
                    constructed, target_document
                )
                constructor_runtime = float(constructed["topology_runtime_seconds"])
            false_negative = decision == "DIRECT_ROOT_TRANSPORT" and not expected_class_equal
            rows.append(
                {
                    "event_id": event_id,
                    "left_argument_id": left_id,
                    "right_argument_id": right_id,
                    "source_path": str(source_path),
                    "target_path": str(target_path),
                    "left_argument": complex(str(source_document["target_cosine"])).real,
                    "right_argument": target_cosine.real,
                    "full_topology_transport_class_equal": expected_class_equal,
                    "agrees_with_5056_multiset_gate": expected_class_equal == sweep_equal,
                    "certificate_converged_8_16_32": converged,
                    "crossing_groups_consistent": groups_consistent,
                    "certificate_transition_detected": transition_detected,
                    "maximum_projective_step": maximum_projective_step,
                    "decision": decision,
                    "false_negative": false_negative,
                    "conservative_fallback": expected_class_equal
                    and decision != "DIRECT_ROOT_TRANSPORT",
                    "step8_transition_count": levels[0]["total_transition_count"],
                    "step16_transition_count": levels[1]["total_transition_count"],
                    "step32_transition_count": levels[2]["total_transition_count"],
                    "certificate_runtime_seconds_8_16": levels[0]["runtime_seconds"]
                    + levels[1]["runtime_seconds"],
                    "benchmark_runtime_seconds_8_16_32": sum(
                        level["runtime_seconds"] for level in levels
                    ),
                    "constructed_signature_exact": signature_exact,
                    "constructed_class_exact": class_exact,
                    "maximum_endpoint_log_error": endpoint_maximum,
                    "maximum_crossing_root_error": crossing_maximum,
                    "constructor_runtime_seconds": constructor_runtime,
                    "target_full_topology_runtime_seconds": float(
                        target_row["e040_topology_runtime_seconds"]
                    ),
                }
            )
    transports = [row for row in rows if row["decision"] == "DIRECT_ROOT_TRANSPORT"]
    fallback = [row for row in rows if row["decision"] != "DIRECT_ROOT_TRANSPORT"]
    false_negatives = [row for row in rows if row["false_negative"]]
    failed_transports = [
        row
        for row in transports
        if not row["constructed_signature_exact"]
        or not row["constructed_class_exact"]
        or float(row["maximum_endpoint_log_error"]) >= 1.0e-10
        or float(row["maximum_crossing_root_error"]) >= 2.0e-5
    ]
    event_rows = []
    for event_id in event_ids:
        event_source_rows = [row_map[(event_id, base_id)] for base_id in ARGUMENT_ORDER]
        event_edges = [row for row in rows if row["event_id"] == event_id]
        current_topology = sum(
            float(row["e040_topology_runtime_seconds"]) for row in event_source_rows
        )
        anchor_cost = float(
            row_map[(event_id, ARGUMENT_ORDER[0])]["e040_topology_runtime_seconds"]
        )
        fallback_cost = sum(
            float(row["target_full_topology_runtime_seconds"])
            for row in event_edges
            if row["decision"] != "DIRECT_ROOT_TRANSPORT"
        )
        certificate_cost = sum(
            float(row["certificate_runtime_seconds_8_16"]) for row in event_edges
        )
        constructor_cost = sum(
            float(row["constructor_runtime_seconds"])
            for row in event_edges
            if row["decision"] == "DIRECT_ROOT_TRANSPORT"
        )
        chain_cost = anchor_cost + fallback_cost + certificate_cost + constructor_cost
        event_rows.append(
            {
                "event_id": event_id,
                "current_e040_topology_seconds": current_topology,
                "chain_anchor_count": 1
                + sum(row["decision"] != "DIRECT_ROOT_TRANSPORT" for row in event_edges),
                "transport_edge_count": sum(
                    row["decision"] == "DIRECT_ROOT_TRANSPORT" for row in event_edges
                ),
                "full_anchor_seconds": anchor_cost + fallback_cost,
                "certificate_seconds": certificate_cost,
                "constructor_seconds": constructor_cost,
                "projected_chain_topology_seconds": chain_cost,
                "net_savings_seconds": current_topology - chain_cost,
            }
        )
    maximum_endpoint_error = max(
        (float(row["maximum_endpoint_log_error"]) for row in transports),
        default=0.0,
    )
    maximum_crossing_error = max(
        (float(row["maximum_crossing_root_error"]) for row in transports),
        default=0.0,
    )
    mean_current = sum(row["current_e040_topology_seconds"] for row in event_rows) / len(
        event_rows
    )
    mean_chain = sum(row["projected_chain_topology_seconds"] for row in event_rows) / len(
        event_rows
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "adjacent_edge_count": len(rows),
        "event_count": len(event_ids),
        "full_topology_class_equal_edge_count": sum(
            bool(row["full_topology_transport_class_equal"]) for row in rows
        ),
        "direct_transport_edge_count": len(transports),
        "full_homotopy_fallback_edge_count": len(fallback),
        "false_negative_count": len(false_negatives),
        "failed_transport_count": len(failed_transports),
        "conservative_fallback_count": sum(
            bool(row["conservative_fallback"]) for row in rows
        ),
        "unconverged_certificate_count": sum(
            not bool(row["certificate_converged_8_16_32"]) for row in rows
        ),
        "projective_limit_exceeded_count": sum(
            float(row["maximum_projective_step"]) >= PROJECTIVE_LIMIT for row in rows
        ),
        "maximum_endpoint_log_error": maximum_endpoint_error,
        "maximum_crossing_root_error": maximum_crossing_error,
        "mean_current_e040_topology_seconds": mean_current,
        "mean_projected_argument_chain_topology_seconds": mean_chain,
        "mean_projected_topology_savings_seconds": mean_current - mean_chain,
        "projected_topology_cost_reduction_fraction": (mean_current - mean_chain)
        / mean_current,
        "argument_chain_certificate_gate_passed": (
            len(rows) == 112
            and not false_negatives
            and not failed_transports
            and bool(transports)
        ),
        "retrospective_cost_projection_only": True,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "construct full chained documents from transported predecessors and validate held-out chain equivalence",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    SOURCE.mkdir(parents=True, exist_ok=True)
    with ROW_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with EVENT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(event_rows[0]))
        writer.writeheader()
        writer.writerows(event_rows)
    checks = [
        (
            "source_paths_exist",
            all(path.exists() for path in required),
            "5053, 5056, 5059, and 5061 inputs exist",
        ),
        (
            "adjacency_matrix_complete",
            len(rows) == 112 and len(event_ids) == 8,
            f"edges={len(rows)}; events={len(event_ids)}",
        ),
        (
            "structural_sweep_reproduced",
            all(row["agrees_with_5056_multiset_gate"] for row in rows),
            "direct class comparison agrees with 5056",
        ),
        (
            "no_unsafe_transports",
            not false_negatives,
            f"false negatives={len(false_negatives)}",
        ),
        (
            "all_selected_transports_exact",
            transports and not failed_transports,
            f"exact={len(transports) - len(failed_transports)}/{len(transports)}",
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
            "positive_projected_savings",
            mean_chain < mean_current,
            f"current={mean_current}; chain={mean_chain}",
        ),
        (
            "certificate_gate_passed",
            result["argument_chain_certificate_gate_passed"],
            "all zero-transition decisions are exact and all uncertain edges fall back",
        ),
        (
            "no_fresh_kernel_execution",
            not result["fresh_kernel_execution_authorized"],
            "adjacency benchmark uses saved topology documents only",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            result["retrospective_cost_projection_only"]
            and not result["valid_for_full_MTS_claim"],
            "argument transport is operational rather than physical evidence",
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
                    "check_id": f"V5065_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5065 validation failed: {failed}")


if __name__ == "__main__":
    main()
