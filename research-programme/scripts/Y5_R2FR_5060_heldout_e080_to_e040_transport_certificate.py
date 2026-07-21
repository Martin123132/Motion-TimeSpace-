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
SCRIPT_5057 = POST / "scripts" / "Y5_R2FR_5057_direct_target_root_topology_transport_benchmark.py"
SCRIPT_5059 = POST / "scripts" / "Y5_R2FR_5059_short_epsilon_segment_transition_certificate.py"
SOURCE_5040 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5040"
    / "runs"
    / "nested_sobol_power1_s4_v1"
    / "topologies"
)
SOURCE_5037 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5037"
    / "runs"
    / "paired_outer_precision_s4_v1"
    / "topologies"
)
SOURCE_5059 = POST / "source-intake" / "functional_rg" / "5059"
SOURCE = POST / "source-intake" / "functional_rg" / "5060"
RESULT_JSON = SOURCE / "heldout_e080_to_e040_transport_certificate.json"
ROW_CSV = SOURCE / "heldout_e080_to_e040_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5060_VALIDATION.csv"
)
MARKER = "MTS_5060_HELDOUT_E080_TO_E040_TRANSPORT_CERTIFICATE"
REVISION = "out-of-interval-e080-e040-certificate-validation-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
TARGET_EPSILON = 0.04
STEP_LEVELS = (8, 16, 32)
PROJECTIVE_TRACKING_LIMIT = 0.1


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5057 = load_module("mts_5057_for_5060", SCRIPT_5057)
M5059 = load_module("mts_5059_for_5060", SCRIPT_5059)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


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
    training_result_path = SOURCE_5059 / "short_epsilon_segment_transition_certificate.json"
    required = [
        SCRIPT_5057,
        SCRIPT_5059,
        SOURCE_5037,
        SOURCE_5040,
        training_result_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_paths = sorted(
        [
            *SOURCE_5037.glob("*__E080_A*.json"),
            *SOURCE_5040.glob("*__E080_A*.json"),
        ]
    )
    pairs = []
    for source_path in source_paths:
        target_path = source_path.with_name(source_path.name.replace("__E080_", "__E040_"))
        if not target_path.exists():
            raise FileNotFoundError(target_path)
        pairs.append((source_path, target_path))
    rows = []
    for source_path, target_path in pairs:
        source_document = json.loads(source_path.read_text(encoding="utf-8"))
        target_document = json.loads(target_path.read_text(encoding="utf-8"))
        expected_transport_class_equal = (
            transport_class(source_document) == transport_class(target_document)
        )
        levels = [
            M5059.segment_gate(source_document, steps, TARGET_EPSILON)
            for steps in STEP_LEVELS
        ]
        selected = levels[1]
        converged = all(
            level["transition_signature"] == levels[-1]["transition_signature"]
            for level in levels[:-1]
        )
        transition_detected = bool(selected["transition_detected"])
        transport = (
            M5057.transport_pair(source_document, target_document)
            if not transition_detected
            else None
        )
        event_id = str(source_document["event_id"])
        argument_id = str(source_document["argument_id"]).split("_", 1)[-1]
        rows.append(
            {
                "event_id": event_id,
                "base_argument_id": argument_id,
                "source_path": str(source_path),
                "target_path": str(target_path),
                "source_epsilon": complex(str(source_document["target_cosine"])).imag,
                "target_epsilon": TARGET_EPSILON,
                "full_topology_transport_class_equal": expected_transport_class_equal,
                "certificate_transition_detected": transition_detected,
                "false_negative": (not expected_transport_class_equal)
                and not transition_detected,
                "conservative_fallback": expected_transport_class_equal
                and transition_detected,
                "transition_signature_converged_8_16_32": converged,
                "step8_transition_count": levels[0]["total_transition_count"],
                "step16_transition_count": levels[1]["total_transition_count"],
                "step32_transition_count": levels[2]["total_transition_count"],
                "maximum_projective_assignment_step": max(
                    level["maximum_projective_assignment_step"] for level in levels
                ),
                "maximum_boundary_projective_step": max(
                    level["maximum_boundary_projective_step"] for level in levels
                ),
                "certificate_runtime_seconds_8_16": levels[0]["runtime_seconds"]
                + levels[1]["runtime_seconds"],
                "transport_attempted": transport is not None,
                "transport_exact_numeric_signature": (
                    bool(transport["exact_numeric_signature_equal"])
                    if transport is not None
                    else None
                ),
                "transport_signature_error": (
                    float(transport["signature_transport_error"])
                    if transport is not None
                    else None
                ),
                "production_decision": "FULL_HOMOTOPY_FALLBACK"
                if transition_detected
                else "DIRECT_ROOT_TRANSPORT",
            }
        )
    false_negatives = [row for row in rows if row["false_negative"]]
    conservative_fallbacks = [row for row in rows if row["conservative_fallback"]]
    transition_rows = [row for row in rows if row["certificate_transition_detected"]]
    transport_rows = [row for row in rows if row["transport_attempted"]]
    failed_transports = [
        row for row in transport_rows if not row["transport_exact_numeric_signature"]
    ]
    unconverged = [
        row for row in rows if not row["transition_signature_converged_8_16_32"]
    ]
    maximum_projective_step = max(
        float(row["maximum_projective_assignment_step"]) for row in rows
    )
    maximum_boundary_step = max(
        float(row["maximum_boundary_projective_step"]) for row in rows
    )
    training_result = json.loads(training_result_path.read_text(encoding="utf-8"))
    heldout_gate = (
        len(rows) == 84
        and not false_negatives
        and not failed_transports
        and not unconverged
        and bool(transition_rows)
        and maximum_projective_step < PROJECTIVE_TRACKING_LIMIT
        and maximum_boundary_step < PROJECTIVE_TRACKING_LIMIT
        and bool(training_result["adaptive_transition_certificate_passed"])
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "validation_role": "held-out epsilon interval and event rows; E080-to-E040 was not used to select the E040-to-E020 certificate result",
        "pair_count": len(rows),
        "event_count": len({row["event_id"] for row in rows}),
        "source_epsilon": 0.08,
        "target_epsilon": TARGET_EPSILON,
        "full_topology_class_change_count": sum(
            not row["full_topology_transport_class_equal"] for row in rows
        ),
        "certificate_transition_count": len(transition_rows),
        "false_negative_count": len(false_negatives),
        "conservative_fallback_count": len(conservative_fallbacks),
        "direct_transport_count": len(transport_rows),
        "exact_direct_transport_count": len(transport_rows) - len(failed_transports),
        "failed_direct_transport_count": len(failed_transports),
        "unconverged_signature_count": len(unconverged),
        "maximum_projective_assignment_step": maximum_projective_step,
        "maximum_boundary_projective_step": maximum_boundary_step,
        "mean_certificate_runtime_seconds": sum(
            float(row["certificate_runtime_seconds_8_16"]) for row in rows
        )
        / len(rows),
        "heldout_interval_gate_passed": heldout_gate,
        "production_hybrid_rule_authorized_for_dry_run": heldout_gate,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": (
            "build a dry-run topology constructor and verify serialized documents against saved full homotopies"
            if heldout_gate
            else "repair or reject the segment certificate"
        ),
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
            and all(source.exists() and target.exists() for source, target in pairs),
            "all held-out E080/E040 topology pairs exist",
        ),
        (
            "heldout_matrix_complete",
            len(rows) == 84 and len({row["event_id"] for row in rows}) == 6,
            f"pairs={len(rows)}; events={len({row['event_id'] for row in rows})}",
        ),
        (
            "no_transition_false_negatives",
            not false_negatives,
            f"false negatives={len(false_negatives)}",
        ),
        (
            "all_selected_transports_exact",
            transport_rows and not failed_transports,
            f"exact={len(transport_rows) - len(failed_transports)}/{len(transport_rows)}",
        ),
        (
            "resolution_convergence",
            not unconverged,
            f"unconverged={len(unconverged)}",
        ),
        (
            "projective_tracking_bounded",
            maximum_projective_step < PROJECTIVE_TRACKING_LIMIT
            and maximum_boundary_step < PROJECTIVE_TRACKING_LIMIT,
            f"roots={maximum_projective_step}; boundaries={maximum_boundary_step}",
        ),
        (
            "training_gate_inherited",
            bool(training_result["adaptive_transition_certificate_passed"]),
            "E040-to-E020 120-pair gate passed",
        ),
        (
            "heldout_gate_passed",
            heldout_gate,
            "out-of-interval certificate has no unsafe transport decisions",
        ),
        (
            "dry_run_scope_only",
            result["production_hybrid_rule_authorized_for_dry_run"]
            and not result["fresh_kernel_execution_authorized"],
            "authorization is limited to serialized topology construction",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "held-out operational validation is not a physical claim",
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
                    "check_id": f"V5060_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5060 validation failed: {failed}")


if __name__ == "__main__":
    main()
