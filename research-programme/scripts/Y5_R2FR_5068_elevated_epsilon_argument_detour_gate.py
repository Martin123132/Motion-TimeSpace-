from __future__ import annotations

import csv
import importlib.util
import json
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5059 = POST / "scripts" / "Y5_R2FR_5059_short_epsilon_segment_transition_certificate.py"
SCRIPT_5061 = POST / "scripts" / "Y5_R2FR_5061_serialized_transport_topology_constructor_dry_run.py"
SOURCE_5065 = POST / "source-intake" / "functional_rg" / "5065"
SOURCE_5066 = POST / "source-intake" / "functional_rg" / "5066"
SOURCE = POST / "source-intake" / "functional_rg" / "5068"
RESULT_JSON = SOURCE / "elevated_epsilon_argument_detour_gate.json"
ROW_CSV = SOURCE / "argument_detour_rows.csv"
EVENT_CSV = SOURCE / "detour_argument_chain_event_costs.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5068_VALIDATION.csv"
)
MARKER = "MTS_5068_ELEVATED_EPSILON_ARGUMENT_DETOUR_GATE"
REVISION = "predeclared-epsilon-height-detour-hierarchy-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
HEIGHTS = (0.08, 0.16, 0.32, 0.64)
PROJECTIVE_LIMIT = 0.1


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5059 = load_module("mts_5059_for_5068", SCRIPT_5059)
M5061 = load_module("mts_5061_for_5068", SCRIPT_5061)


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


def detour_path(source: complex, target: complex, height: float, steps: int) -> list[complex]:
    if height <= max(source.imag, target.imag):
        raise ValueError("detour height must exceed endpoint epsilon")
    waypoints = (
        source,
        complex(source.real, height),
        complex(target.real, height),
        target,
    )
    values = [waypoints[0]]
    for left, right in zip(waypoints[:-1], waypoints[1:]):
        values.extend(
            left + index / (steps - 1) * (right - left)
            for index in range(1, steps)
        )
    return values


def path_gate(
    source_document: dict[str, Any],
    target: complex,
    height: float,
    steps: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    M5059.configure(source_document)
    source = complex(str(source_document["target_cosine"]))
    cosines = detour_path(source, target, height, steps)
    boundaries, ownerships = M5059.M5030.physical_chambers()
    endpoint_paths, _, maximum_boundary_projective_step = (
        M5059.anchored_endpoint_paths(boundaries, source_document, cosines)
    )
    rational_path = [
        M5059.M5030.M5029.root_rationals(
            M5059.M5030.SOFT_ENERGY,
            M5059.M5030.SOFT_COSINE,
            M5059.M5030.DECAY_COSINE,
            cosine,
        )
        for cosine in cosines
    ]
    signatures = []
    total_transitions = 0
    maximum_projective_assignment_step = 0.0
    groups_consistent = True
    for chamber_index, ownership in enumerate(ownerships):
        (
            tracks,
            _,
            projective_assignment_step,
            _,
            _,
            _,
            _,
        ) = M5059.M5030.track_opposite_pair_roots(rational_path, ownership)
        maximum_projective_assignment_step = max(
            maximum_projective_assignment_step, projective_assignment_step
        )
        start_logs, end_logs = M5059.M5030.chamber_segment_logs(
            endpoint_paths, chamber_index
        )
        raw_crossings, _ = M5059.M5030.surface_crossings(
            tracks, start_logs, end_logs
        )
        grouped, consistent = M5059.M5030.grouped_surface_crossings(raw_crossings)
        groups_consistent = groups_consistent and consistent
        tokens = tuple(sorted(M5059.crossing_token(row) for row in grouped))
        signatures.append(tokens)
        total_transitions += len(grouped)
    return {
        "height": height,
        "steps_per_leg": steps,
        "transition_signature": tuple(signatures),
        "transition_count": total_transitions,
        "transition_detected": total_transitions > 0,
        "groups_consistent": groups_consistent,
        "maximum_projective_step": max(
            maximum_projective_assignment_step,
            maximum_boundary_projective_step,
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def main() -> None:
    source_rows_path = SOURCE_5065 / "adjacent_argument_certificate_rows.csv"
    source_event_path = SOURCE_5065 / "argument_chain_event_costs.csv"
    source_result_path = SOURCE_5065 / "adjacent_argument_transport_certificate_benchmark.json"
    chain_result_path = SOURCE_5066 / "argument_chain_constructed_predecessor_gate.json"
    required = [
        SCRIPT_5059,
        SCRIPT_5061,
        source_rows_path,
        source_event_path,
        source_result_path,
        chain_result_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_rows = list(csv.DictReader(source_rows_path.open(encoding="utf-8")))
    source_events = {
        row["event_id"]: row
        for row in csv.DictReader(source_event_path.open(encoding="utf-8"))
    }
    rows = []
    for source_row in source_rows:
        base = dict(source_row)
        if source_row["decision"] == "DIRECT_ROOT_TRANSPORT":
            rows.append(
                {
                    **base,
                    "detour_attempted": False,
                    "detour_heights_attempted": "[]",
                    "chosen_detour_height": None,
                    "detour_certificate_runtime_seconds": 0.0,
                    "detour_recovered_transport": False,
                    "final_decision": "DIRECT_ROOT_TRANSPORT",
                    "detour_constructed_signature_exact": None,
                    "detour_constructed_class_exact": None,
                    "detour_maximum_endpoint_log_error": None,
                    "detour_maximum_crossing_root_error": None,
                    "detour_constructor_runtime_seconds": 0.0,
                    "detour_false_negative": False,
                }
            )
            continue
        source_path = localize(source_row["source_path"])
        target_path = localize(source_row["target_path"])
        source_document = json.loads(source_path.read_text(encoding="utf-8"))
        target_document = json.loads(target_path.read_text(encoding="utf-8"))
        target = complex(str(target_document["target_cosine"]))
        attempts = []
        chosen = None
        for height in HEIGHTS:
            level8 = path_gate(source_document, target, height, 8)
            level16 = path_gate(source_document, target, height, 16)
            attempt = {
                "height": height,
                "level8_transition_count": level8["transition_count"],
                "level16_transition_count": level16["transition_count"],
                "level8_runtime_seconds": level8["runtime_seconds"],
                "level16_runtime_seconds": level16["runtime_seconds"],
                "converged_8_16": level8["transition_signature"]
                == level16["transition_signature"],
                "groups_consistent_8_16": level8["groups_consistent"]
                and level16["groups_consistent"],
                "maximum_projective_step_8_16": max(
                    level8["maximum_projective_step"],
                    level16["maximum_projective_step"],
                ),
            }
            attempts.append(attempt)
            candidate = (
                attempt["converged_8_16"]
                and attempt["groups_consistent_8_16"]
                and attempt["maximum_projective_step_8_16"] < PROJECTIVE_LIMIT
                and level16["transition_count"] == 0
            )
            if not candidate:
                continue
            level32 = path_gate(source_document, target, height, 32)
            attempt.update(
                {
                    "level32_transition_count": level32["transition_count"],
                    "level32_runtime_seconds": level32["runtime_seconds"],
                    "converged_16_32": level16["transition_signature"]
                    == level32["transition_signature"],
                    "groups_consistent_32": level32["groups_consistent"],
                    "maximum_projective_step_32": level32[
                        "maximum_projective_step"
                    ],
                }
            )
            if (
                attempt["converged_16_32"]
                and attempt["groups_consistent_32"]
                and attempt["maximum_projective_step_32"] < PROJECTIVE_LIMIT
                and level32["transition_count"] == 0
            ):
                chosen = height
                break
        total_detour_runtime = sum(
            float(attempt.get("level8_runtime_seconds", 0.0))
            + float(attempt.get("level16_runtime_seconds", 0.0))
            + float(attempt.get("level32_runtime_seconds", 0.0))
            for attempt in attempts
        )
        recovered = chosen is not None
        signature_exact = None
        class_exact = None
        endpoint_maximum = None
        crossing_maximum = None
        constructor_runtime = 0.0
        if recovered:
            constructed = M5061.construct_document(
                source_document,
                target.imag,
                source_path,
                "E040_ARGUMENT_ELEVATED_EPSILON_DETOUR",
                target,
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
            crossing_maximum = M5061.crossing_root_error(constructed, target_document)
            constructor_runtime = float(constructed["topology_runtime_seconds"])
        expected_class_equal = source_row["full_topology_transport_class_equal"] == "True"
        rows.append(
            {
                **base,
                "detour_attempted": True,
                "detour_heights_attempted": json.dumps(attempts, separators=(",", ":")),
                "chosen_detour_height": chosen,
                "detour_certificate_runtime_seconds": total_detour_runtime,
                "detour_recovered_transport": recovered,
                "final_decision": "DIRECT_ROOT_TRANSPORT_DETOUR"
                if recovered
                else source_row["decision"],
                "detour_constructed_signature_exact": signature_exact,
                "detour_constructed_class_exact": class_exact,
                "detour_maximum_endpoint_log_error": endpoint_maximum,
                "detour_maximum_crossing_root_error": crossing_maximum,
                "detour_constructor_runtime_seconds": constructor_runtime,
                "detour_false_negative": recovered and not expected_class_equal,
            }
        )
    recovered = [row for row in rows if str(row["detour_recovered_transport"]) == "True" or row["detour_recovered_transport"] is True]
    false_negatives = [row for row in rows if str(row["detour_false_negative"]) == "True" or row["detour_false_negative"] is True]
    failed_recoveries = [
        row
        for row in recovered
        if not row["detour_constructed_signature_exact"]
        or not row["detour_constructed_class_exact"]
        or float(row["detour_maximum_endpoint_log_error"]) >= 1.0e-10
        or float(row["detour_maximum_crossing_root_error"]) >= 2.0e-5
    ]
    event_rows = []
    for event_id, source_event in sorted(source_events.items()):
        event_edges = [row for row in rows if row["event_id"] == event_id]
        detour_overhead = sum(
            float(row["detour_certificate_runtime_seconds"]) for row in event_edges
        )
        recovered_savings = sum(
            float(row["target_full_topology_runtime_seconds"])
            - float(row["detour_constructor_runtime_seconds"])
            for row in event_edges
            if str(row["detour_recovered_transport"]) == "True"
            or row["detour_recovered_transport"] is True
        )
        old_chain = float(source_event["projected_chain_topology_seconds"])
        new_chain = old_chain + detour_overhead - recovered_savings
        event_rows.append(
            {
                "event_id": event_id,
                "straight_chain_topology_seconds": old_chain,
                "detour_search_overhead_seconds": detour_overhead,
                "recovered_full_topology_savings_seconds": recovered_savings,
                "detour_chain_topology_seconds": new_chain,
                "detour_chain_net_savings_vs_full_seconds": float(
                    source_event["current_e040_topology_seconds"]
                )
                - new_chain,
                "recovered_transport_count": sum(
                    str(row["detour_recovered_transport"]) == "True"
                    or row["detour_recovered_transport"] is True
                    for row in event_edges
                ),
            }
        )
    mean_straight = sum(row["straight_chain_topology_seconds"] for row in event_rows) / len(
        event_rows
    )
    mean_detour = sum(row["detour_chain_topology_seconds"] for row in event_rows) / len(
        event_rows
    )
    source_result = json.loads(source_result_path.read_text(encoding="utf-8"))
    chain_result = json.loads(chain_result_path.read_text(encoding="utf-8"))
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "predeclared_height_hierarchy": list(HEIGHTS),
        "straight_transport_count": int(source_result["direct_transport_edge_count"]),
        "candidate_zero_detour_count": len(recovered),
        "adopted_detour_transport_count": 0,
        "adopted_transport_count": int(source_result["direct_transport_edge_count"]),
        "remaining_fallback_count": 112
        - int(source_result["direct_transport_edge_count"]),
        "false_negative_count": len(false_negatives),
        "failed_recovery_count": len(failed_recoveries),
        "mean_straight_chain_topology_seconds": mean_straight,
        "mean_detour_chain_topology_seconds": mean_detour,
        "mean_additional_topology_savings_seconds": mean_straight - mean_detour,
        "detour_gate_passed": False,
        "elevated_epsilon_detour_rejected": bool(false_negatives)
        or bool(failed_recoveries)
        or mean_detour >= mean_straight,
        "decision": "REJECT_ELEVATED_EPSILON_DETOUR_HIERARCHY",
        "retrospective_path_search_uses_target_topology_only_for_validation": True,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "retain the straight certified argument chain; refine only uncertified same-class edges without accepting zero-detour signatures",
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
            "5059, 5061, 5065, and 5066 inputs exist",
        ),
        (
            "edge_matrix_complete",
            len(rows) == 112,
            f"edges={len(rows)}",
        ),
        (
            "unsafe_detour_candidates_exposed",
            bool(false_negatives) and bool(failed_recoveries),
            f"false zero certificates={len(false_negatives)}; failed candidates={len(failed_recoveries)}",
        ),
        (
            "no_detour_candidates_adopted",
            result["adopted_detour_transport_count"] == 0
            and result["adopted_transport_count"]
            == int(source_result["direct_transport_edge_count"]),
            "unsafe candidate detours do not alter the accepted chain",
        ),
        (
            "cost_penalty_recorded",
            mean_detour > mean_straight,
            f"straight={mean_straight}; rejected detour={mean_detour}",
        ),
        (
            "chain_gate_inherited",
            bool(chain_result["constructed_predecessor_gate_passed"]),
            "straight-path constructed-predecessor gate passed",
        ),
        (
            "detour_rejection_gate",
            result["elevated_epsilon_detour_rejected"]
            and not result["detour_gate_passed"]
            and result["decision"]
            == "REJECT_ELEVATED_EPSILON_DETOUR_HIERARCHY",
            "finite height hierarchy is explicitly rejected after unsafe zero certificates",
        ),
        (
            "no_fresh_kernel_execution",
            not result["fresh_kernel_execution_authorized"],
            "detour search uses saved topology validation only",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            result["retrospective_path_search_uses_target_topology_only_for_validation"]
            and not result["valid_for_full_MTS_claim"],
            "detour hierarchy is an operational path certificate",
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
                    "check_id": f"V5068_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5068 validation failed: {failed}")


if __name__ == "__main__":
    main()
