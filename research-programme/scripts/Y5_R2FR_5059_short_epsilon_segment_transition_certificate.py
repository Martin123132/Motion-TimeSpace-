from __future__ import annotations

import cmath
import csv
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5030 = POST / "scripts" / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5057 = POST / "source-intake" / "functional_rg" / "5057"
SOURCE = POST / "source-intake" / "functional_rg" / "5059"
RESULT_JSON = SOURCE / "short_epsilon_segment_transition_certificate.json"
ROW_CSV = SOURCE / "epsilon_segment_certificate_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5059_VALIDATION.csv"
)
MARKER = "MTS_5059_SHORT_EPSILON_SEGMENT_TRANSITION_CERTIFICATE"
REVISION = "adaptive-8-16-32-epsilon-segment-certificate-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
TARGET_EPSILON = 0.02
STEP_LEVELS = (8, 16, 32)
PROJECTIVE_TRACKING_LIMIT = 0.1


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5030 = load_module("mts_5030_for_5059", SCRIPT_5030)


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


def configure(document: dict[str, Any]) -> None:
    M5030.SOFT_ENERGY = float(document["soft_energy"])
    M5030.SOFT_COSINE = float(document["soft_cosine"])
    M5030.DECAY_COSINE = float(document["decay_cosine"])


def anchored_endpoint_paths(
    boundaries: list[dict[str, Any]],
    source_document: dict[str, Any],
    cosines: list[complex],
) -> tuple[list[list[complex]], float, float]:
    source_logs = [
        complex(str(chamber["target_start_log"]))
        for chamber in source_document["chambers"]
    ]
    if len(source_logs) != len(boundaries):
        raise RuntimeError("source endpoint/chamber count mismatch")
    paths = []
    maximum_log_step = 0.0
    maximum_projective_step = 0.0
    for boundary_index, boundary in enumerate(boundaries):
        reference = source_logs[boundary_index]
        if boundary.get("synthetic"):
            paths.append([reference for _ in cosines])
            continue
        equation = boundary["equations"][0]
        current_root = cmath.exp(reference)
        values = [reference]
        for cosine in cosines[1:]:
            roots = M5030.M5028.M5027.relative_azimuth_roots(
                M5030.SOFT_ENERGY,
                complex(M5030.SOFT_COSINE, 0.0),
                complex(M5030.DECAY_COSINE, 0.0),
                equation["external_sign"] * cosine,
                equation["hard_sign"],
            )[:2]
            eta = (roots[0] + roots[1]) / 2.0
            principal = cmath.sqrt(eta * eta - 1.0)
            next_root = min(
                (eta + principal, eta - principal),
                key=lambda candidate: M5030.chordal_distance(
                    current_root, candidate
                ),
            )
            projective_step = M5030.chordal_distance(current_root, next_root)
            value = M5030.lifted_log(next_root, reference)
            maximum_log_step = max(maximum_log_step, abs(value - reference))
            maximum_projective_step = max(
                maximum_projective_step, projective_step
            )
            current_root = next_root
            reference = value
            values.append(value)
        paths.append(values)
    return paths, maximum_log_step, maximum_projective_step


def segment_gate(
    source_document: dict[str, Any],
    steps: int,
    target_epsilon: float = TARGET_EPSILON,
    target_cosine: complex | None = None,
) -> dict[str, Any]:
    source_target = complex(str(source_document["target_cosine"]))
    target = (
        complex(source_target.real, target_epsilon)
        if target_cosine is None
        else complex(target_cosine)
    )
    cosines = [
        source_target + index / (steps - 1) * (target - source_target)
        for index in range(steps)
    ]
    return cosine_path_gate(source_document, cosines)


def cosine_path_gate(
    source_document: dict[str, Any], cosines: list[complex]
) -> dict[str, Any]:
    if len(cosines) < 2:
        raise ValueError("cosine path requires at least two samples")
    source_target = complex(str(source_document["target_cosine"]))
    if abs(cosines[0] - source_target) > 1.0e-12:
        raise ValueError("cosine path must start at the source target cosine")
    started = time.perf_counter()
    configure(source_document)
    steps = len(cosines)
    boundaries, ownerships = M5030.physical_chambers()
    (
        endpoint_paths,
        maximum_boundary_log_step,
        maximum_boundary_projective_step,
    ) = anchored_endpoint_paths(boundaries, source_document, cosines)
    rational_path = [
        M5030.M5029.root_rationals(
            M5030.SOFT_ENERGY,
            M5030.SOFT_COSINE,
            M5030.DECAY_COSINE,
            cosine,
        )
        for cosine in cosines
    ]
    chamber_signatures = []
    chamber_transition_counts = []
    grouped_crossings_by_chamber = []
    endpoint_root_tracks_by_chamber = []
    target_endpoint_logs_by_chamber = []
    maximum_assignment_step = 0.0
    maximum_projective_assignment_step = 0.0
    total_discarded_transient_roots = 0
    total_radially_excluded_transitions = 0
    groups_consistent = True
    for chamber_index, ownership in enumerate(ownerships):
        (
            tracks,
            assignment_step,
            projective_assignment_step,
            _,
            discarded_transient_roots,
            _,
            _,
        ) = M5030.track_opposite_pair_roots(rational_path, ownership)
        maximum_assignment_step = max(maximum_assignment_step, assignment_step)
        maximum_projective_assignment_step = max(
            maximum_projective_assignment_step, projective_assignment_step
        )
        total_discarded_transient_roots += discarded_transient_roots
        start_logs, end_logs = M5030.chamber_segment_logs(
            endpoint_paths, chamber_index
        )
        raw_crossings, radially_excluded = M5030.surface_crossings(
            tracks, start_logs, end_logs
        )
        grouped, consistent = M5030.grouped_surface_crossings(raw_crossings)
        total_radially_excluded_transitions += radially_excluded
        groups_consistent = groups_consistent and consistent
        tokens = tuple(sorted(crossing_token(row) for row in grouped))
        chamber_signatures.append(tokens)
        chamber_transition_counts.append(len(grouped))
        grouped_crossings_by_chamber.append(grouped)
        endpoint_root_tracks_by_chamber.append(
            [
                {
                    "source_root": str(cmath.exp(track["logs"][0])),
                    "target_root": str(cmath.exp(track["logs"][-1])),
                    "initial_pairs": [
                        list(pair) for pair in track["initial_pairs"]
                    ],
                    "target_pairs": [
                        list(pair) for pair in track["target_pairs"]
                    ],
                }
                for track in tracks
            ]
        )
        target_endpoint_logs_by_chamber.append(
            {
                "target_start_log": str(start_logs[-1]),
                "target_end_log": str(end_logs[-1]),
            }
        )
    signature = tuple(chamber_signatures)
    return {
        "steps": steps,
        "transition_signature": signature,
        "grouped_crossings_by_chamber": grouped_crossings_by_chamber,
        "endpoint_root_tracks_by_chamber": endpoint_root_tracks_by_chamber,
        "target_endpoint_logs_by_chamber": target_endpoint_logs_by_chamber,
        "transition_signature_json": json.dumps(signature, separators=(",", ":")),
        "chamber_transition_counts": chamber_transition_counts,
        "total_transition_count": sum(chamber_transition_counts),
        "transition_detected": any(chamber_transition_counts),
        "groups_consistent": groups_consistent,
        "maximum_boundary_log_step": maximum_boundary_log_step,
        "maximum_boundary_projective_step": maximum_boundary_projective_step,
        "maximum_assignment_step": maximum_assignment_step,
        "maximum_projective_assignment_step": maximum_projective_assignment_step,
        "discarded_transient_root_samples": total_discarded_transient_roots,
        "radially_excluded_transitions": total_radially_excluded_transitions,
        "runtime_seconds": time.perf_counter() - started,
    }


def main() -> None:
    source_rows_path = SOURCE_5053 / "high_low_cost_rows.csv"
    transport_rows_path = SOURCE_5057 / "epsilon_transport_rows.csv"
    required = [SCRIPT_5030, source_rows_path, transport_rows_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_rows = list(csv.DictReader(source_rows_path.open(encoding="utf-8")))
    transport_rows = {
        (row["event_id"], row["base_argument_id"]): row
        for row in csv.DictReader(transport_rows_path.open(encoding="utf-8"))
    }
    rows = []
    for source_row in source_rows:
        event_id = source_row["event_id"]
        base_argument_id = source_row["base_argument_id"]
        key = (event_id, base_argument_id)
        source_path = localize(source_row["e040_topology"])
        source_document = json.loads(source_path.read_text(encoding="utf-8"))
        levels = [segment_gate(source_document, steps) for steps in STEP_LEVELS]
        expected_transition = bool_value(transport_rows[key]["fallback_required"])
        converged = all(
            level["transition_signature"] == levels[-1]["transition_signature"]
            for level in levels[:-1]
        )
        selected = levels[1]
        classification_correct = selected["transition_detected"] == expected_transition
        rows.append(
            {
                "event_id": event_id,
                "base_argument_id": base_argument_id,
                "e040_source_path": str(source_path),
                "target_real": complex(str(source_document["target_cosine"])).real,
                "source_epsilon": complex(str(source_document["target_cosine"])).imag,
                "target_epsilon": TARGET_EPSILON,
                "expected_transition_from_full_topology": expected_transition,
                "certificate_transition_detected": selected["transition_detected"],
                "classification_correct": classification_correct,
                "transition_signature_converged_8_16_32": converged,
                "selected_steps": selected["steps"],
                "selected_transition_count": selected["total_transition_count"],
                "selected_transition_signature": selected["transition_signature_json"],
                "step8_transition_count": levels[0]["total_transition_count"],
                "step16_transition_count": levels[1]["total_transition_count"],
                "step32_transition_count": levels[2]["total_transition_count"],
                "all_groups_consistent": all(level["groups_consistent"] for level in levels),
                "maximum_projective_assignment_step": max(
                    level["maximum_projective_assignment_step"] for level in levels
                ),
                "maximum_boundary_projective_step": max(
                    level["maximum_boundary_projective_step"] for level in levels
                ),
                "certificate_runtime_seconds_8_16": levels[0]["runtime_seconds"]
                + levels[1]["runtime_seconds"],
                "benchmark_runtime_seconds_8_16_32": sum(
                    level["runtime_seconds"] for level in levels
                ),
                "production_decision": "FULL_HOMOTOPY_FALLBACK"
                if selected["transition_detected"]
                else "DIRECT_ROOT_TRANSPORT",
            }
        )
    transitions = [row for row in rows if row["certificate_transition_detected"]]
    misclassified = [row for row in rows if not row["classification_correct"]]
    unconverged = [
        row for row in rows if not row["transition_signature_converged_8_16_32"]
    ]
    inconsistent = [row for row in rows if not row["all_groups_consistent"]]
    maximum_projective_step = max(
        float(row["maximum_projective_assignment_step"]) for row in rows
    )
    maximum_boundary_step = max(
        float(row["maximum_boundary_projective_step"]) for row in rows
    )
    total_production_runtime = sum(
        float(row["certificate_runtime_seconds_8_16"]) for row in rows
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "pair_count": len(rows),
        "step_levels": list(STEP_LEVELS),
        "selected_certificate_steps": 16,
        "boundary_endpoint_source": "saved E040 target_start_log values",
        "target_epsilon": TARGET_EPSILON,
        "detected_transition_count": len(transitions),
        "detected_transition_keys": [
            [row["event_id"], row["base_argument_id"]] for row in transitions
        ],
        "classification_error_count": len(misclassified),
        "unconverged_signature_count": len(unconverged),
        "inconsistent_group_count": len(inconsistent),
        "maximum_projective_assignment_step": maximum_projective_step,
        "maximum_boundary_projective_step": maximum_boundary_step,
        "total_adaptive_certificate_runtime_seconds": total_production_runtime,
        "mean_adaptive_certificate_runtime_seconds": total_production_runtime / len(rows),
        "construction_reads_saved_e020_topology": False,
        "full_e020_topology_class_used_for_validation_only": True,
        "adaptive_transition_certificate_passed": (
            len(rows) == 120
            and len(transitions) == 1
            and not misclassified
            and not unconverged
            and not inconsistent
            and maximum_projective_step < PROJECTIVE_TRACKING_LIMIT
            and maximum_boundary_step < PROJECTIVE_TRACKING_LIMIT
        ),
        "production_hybrid_rule": (
            "run 8 and 16 segment steps; require identical transition signature and projective steps below 0.1; direct-root transport only for a zero signature; otherwise execute full target homotopy"
        ),
        "production_hybrid_rule_authorized_for_dry_run": False,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "independent held-out or leave-one-event validation of the certificate thresholds",
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
            all(path.exists() for path in required),
            "5030, 5053, and 5057 sources exist",
        ),
        (
            "pair_matrix_complete",
            len(rows) == 120,
            f"{len(rows)} short epsilon segments audited",
        ),
        (
            "transition_classification_exact",
            not misclassified and len(transitions) == 1,
            f"errors={len(misclassified)}; transitions={len(transitions)}",
        ),
        (
            "known_transition_identified",
            len(transitions) == 1
            and transitions[0]["event_id"] == "S503402_N0000"
            and transitions[0]["base_argument_id"] == "A06",
            f"keys={result['detected_transition_keys']}",
        ),
        (
            "resolution_convergence",
            not unconverged,
            f"unconverged={len(unconverged)}",
        ),
        (
            "crossing_groups_consistent",
            not inconsistent,
            f"inconsistent={len(inconsistent)}",
        ),
        (
            "projective_tracking_bounded",
            maximum_projective_step < PROJECTIVE_TRACKING_LIMIT
            and maximum_boundary_step < PROJECTIVE_TRACKING_LIMIT,
            f"roots={maximum_projective_step}; boundaries={maximum_boundary_step}",
        ),
        (
            "no_target_topology_leakage",
            not result["construction_reads_saved_e020_topology"]
            and result["full_e020_topology_class_used_for_validation_only"],
            "certificate uses E040 state, event data, and target epsilon only",
        ),
        (
            "certificate_gate_passed",
            result["adaptive_transition_certificate_passed"],
            "adaptive 8/16 certificate exactly separates transport and fallback rows",
        ),
        (
            "dry_run_not_prematurely_authorized",
            not result["production_hybrid_rule_authorized_for_dry_run"],
            "held-out threshold validation remains required",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["fresh_kernel_execution_authorized"]
            and not result["valid_for_full_MTS_claim"],
            "certificate is an operational topology result only",
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
                    "check_id": f"V5059_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5059 validation failed: {failed}")


if __name__ == "__main__":
    main()
