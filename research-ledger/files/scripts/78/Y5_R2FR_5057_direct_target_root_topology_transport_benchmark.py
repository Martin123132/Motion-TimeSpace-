from __future__ import annotations

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
SCRIPT_5029 = POST / "scripts" / "Y5_R2FR_5029_finite_x_cross_source_collision_map.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5056 = POST / "source-intake" / "functional_rg" / "5056"
SOURCE = POST / "source-intake" / "functional_rg" / "5057"
RESULT_JSON = SOURCE / "direct_target_root_topology_transport_benchmark.json"
ROW_CSV = SOURCE / "epsilon_transport_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5057_VALIDATION.csv"
)
MARKER = "MTS_5057_DIRECT_TARGET_ROOT_TOPOLOGY_TRANSPORT_BENCHMARK"
REVISION = "validated-e040-to-e020-target-root-transport-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
RESIDUE_MATCHING_TOLERANCE = 2.0e-5


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5029 = load_module("mts_5029_for_5057", SCRIPT_5029)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    if not path.exists():
        return "MISSING"
    for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(file_path.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(file_path).encode("ascii"))
    return value.hexdigest()


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


def chordal_distance(first: complex, second: complex) -> float:
    return abs(first - second) / math.sqrt(
        (1.0 + abs(first) ** 2) * (1.0 + abs(second) ** 2)
    )


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


def ordered_crossings(chamber: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(chamber["surface_crossings"], key=lambda row: float(row["step_fraction"]))


def structurally_compatible(
    source_document: dict[str, Any], target_document: dict[str, Any]
) -> bool:
    if len(source_document["chambers"]) != len(target_document["chambers"]):
        return False
    for source_chamber, target_chamber in zip(
        source_document["chambers"], target_document["chambers"]
    ):
        source_tokens = [crossing_token(row) for row in ordered_crossings(source_chamber)]
        target_tokens = [crossing_token(row) for row in ordered_crossings(target_chamber)]
        if source_tokens != target_tokens:
            return False
    return True


def assigned_target_root(
    pair: tuple[str, str],
    source_rationals: dict[str, Any],
    target_rationals: dict[str, Any],
    stored_source_root: complex,
) -> dict[str, Any]:
    source_roots = M5029.collision_roots(
        source_rationals[pair[0]], source_rationals[pair[1]]
    )
    target_roots = M5029.collision_roots(
        target_rationals[pair[0]], target_rationals[pair[1]]
    )
    if not source_roots or not target_roots:
        raise RuntimeError(f"collision root disappeared for {pair}")
    costs = np.asarray(
        [
            [chordal_distance(source_root, target_root) for target_root in target_roots]
            for source_root in source_roots
        ],
        dtype=float,
    )
    source_indices, target_indices = linear_sum_assignment(costs)
    assignment = dict(zip(source_indices.tolist(), target_indices.tolist()))
    source_errors = [chordal_distance(root, stored_source_root) for root in source_roots]
    source_index = int(np.argmin(source_errors))
    if source_index not in assignment:
        raise RuntimeError(f"stored source branch was not assigned for {pair}")
    target_index = assignment[source_index]
    ordered_costs = sorted(float(value) for value in costs[source_index])
    alternative_gap = (
        ordered_costs[1] - ordered_costs[0]
        if len(ordered_costs) > 1
        else math.inf
    )
    return {
        "pair": pair,
        "source_root": source_roots[source_index],
        "target_root": target_roots[target_index],
        "source_representation_error": source_errors[source_index],
        "projective_transport_step": float(costs[source_index, target_index]),
        "assignment_alternative_gap": alternative_gap,
        "source_root_count": len(source_roots),
        "target_root_count": len(target_roots),
    }


def transport_crossing(
    crossing: dict[str, Any],
    source_rationals: dict[str, Any],
    target_rationals: dict[str, Any],
) -> dict[str, Any]:
    stored_source_root = complex(crossing["target_root"])
    candidates = [
        assigned_target_root(
            tuple(sorted(str(value) for value in pair)),
            source_rationals,
            target_rationals,
            stored_source_root,
        )
        for pair in normalized_pairs(crossing)
    ]
    selected = min(
        candidates,
        key=lambda row: (row["source_representation_error"], row["pair"]),
    )
    transported_root = complex(selected["target_root"])
    group_spread = max(
        chordal_distance(transported_root, complex(row["target_root"]))
        for row in candidates
    )
    transported = dict(crossing)
    transported["target_root"] = str(transported_root)
    return {
        "crossing": transported,
        "transported_root": transported_root,
        "maximum_source_representation_error": max(
            float(row["source_representation_error"]) for row in candidates
        ),
        "selected_source_representation_error": float(
            selected["source_representation_error"]
        ),
        "maximum_projective_transport_step": max(
            float(row["projective_transport_step"]) for row in candidates
        ),
        "minimum_assignment_alternative_gap": min(
            float(row["assignment_alternative_gap"]) for row in candidates
        ),
        "group_candidate_spread": group_spread,
        "selected_pair": list(selected["pair"]),
    }


def net_signature(crossings_by_chamber: list[list[dict[str, Any]]]) -> tuple[Any, ...]:
    result = []
    for crossings in crossings_by_chamber:
        windings: dict[tuple[float, float], int] = {}
        for row in crossings:
            root = complex(row["target_root"])
            key = (round(root.real, 8), round(root.imag, 8))
            windings[key] = windings.get(key, 0) + int(row["winding_correction"])
        result.append(
            tuple(
                sorted(
                    (winding, root[0], root[1])
                    for root, winding in windings.items()
                    if winding != 0
                )
            )
        )
    return tuple(result)


def signature_transport_error(
    transported: tuple[Any, ...], expected: tuple[Any, ...]
) -> float:
    if len(transported) != len(expected):
        return math.inf
    maximum = 0.0
    for transported_chamber, expected_chamber in zip(transported, expected):
        transported_by_winding: dict[int, list[complex]] = {}
        expected_by_winding: dict[int, list[complex]] = {}
        for winding, real, imaginary in transported_chamber:
            transported_by_winding.setdefault(int(winding), []).append(complex(real, imaginary))
        for winding, real, imaginary in expected_chamber:
            expected_by_winding.setdefault(int(winding), []).append(complex(real, imaginary))
        if set(transported_by_winding) != set(expected_by_winding):
            return math.inf
        for winding in transported_by_winding:
            left = transported_by_winding[winding]
            right = expected_by_winding[winding]
            if len(left) != len(right):
                return math.inf
            costs = np.asarray(
                [[chordal_distance(first, second) for second in right] for first in left],
                dtype=float,
            )
            left_indices, right_indices = linear_sum_assignment(costs)
            if len(left_indices):
                maximum = max(
                    maximum,
                    max(float(costs[i, j]) for i, j in zip(left_indices, right_indices)),
                )
    return maximum


def complex_target(document: dict[str, Any]) -> complex:
    return complex(str(document["target_cosine"]))


def transport_pair(
    source_document: dict[str, Any], target_document: dict[str, Any]
) -> dict[str, Any]:
    started = time.perf_counter()
    source_rationals = M5029.root_rationals(
        float(source_document["soft_energy"]),
        float(source_document["soft_cosine"]),
        float(source_document["decay_cosine"]),
        complex_target(source_document),
    )
    target_rationals = M5029.root_rationals(
        float(target_document["soft_energy"]),
        float(target_document["soft_cosine"]),
        float(target_document["decay_cosine"]),
        complex_target(target_document),
    )
    transported_chambers: list[list[dict[str, Any]]] = []
    diagnostics: list[dict[str, Any]] = []
    expected_root_errors: list[float] = []
    for source_chamber, target_chamber in zip(
        source_document["chambers"], target_document["chambers"]
    ):
        source_crossings = ordered_crossings(source_chamber)
        target_crossings = ordered_crossings(target_chamber)
        transported_rows = []
        for source_crossing, target_crossing in zip(source_crossings, target_crossings):
            transported = transport_crossing(
                source_crossing, source_rationals, target_rationals
            )
            transported_rows.append(transported["crossing"])
            diagnostics.append(transported)
            expected_root_errors.append(
                chordal_distance(
                    transported["transported_root"],
                    complex(target_crossing["target_root"]),
                )
            )
        transported_chambers.append(transported_rows)
    transported_signature = net_signature(transported_chambers)
    expected_signature = net_signature(
        [ordered_crossings(chamber) for chamber in target_document["chambers"]]
    )
    return {
        "transport_runtime_seconds": time.perf_counter() - started,
        "crossing_count": sum(len(rows) for rows in transported_chambers),
        "exact_numeric_signature_equal": transported_signature == expected_signature,
        "signature_transport_error": signature_transport_error(
            transported_signature, expected_signature
        ),
        "maximum_expected_crossing_root_error": max(expected_root_errors, default=0.0),
        "maximum_source_representation_error": max(
            (row["maximum_source_representation_error"] for row in diagnostics),
            default=0.0,
        ),
        "maximum_projective_transport_step": max(
            (row["maximum_projective_transport_step"] for row in diagnostics),
            default=0.0,
        ),
        "minimum_assignment_alternative_gap": min(
            (row["minimum_assignment_alternative_gap"] for row in diagnostics),
            default=math.inf,
        ),
        "maximum_group_candidate_spread": max(
            (row["group_candidate_spread"] for row in diagnostics),
            default=0.0,
        ),
    }


def main() -> None:
    source_rows_path = SOURCE_5053 / "high_low_cost_rows.csv"
    structural_rows_path = SOURCE_5056 / "epsilon_pair_structural_comparison.csv"
    required = [SCRIPT_5029, source_rows_path, structural_rows_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_rows = list(csv.DictReader(source_rows_path.open(encoding="utf-8")))
    structural_rows = {
        (row["event_id"], row["base_argument_id"]): row
        for row in csv.DictReader(structural_rows_path.open(encoding="utf-8"))
    }
    rows = []
    for source_row in source_rows:
        event_id = source_row["event_id"]
        base_argument_id = source_row["base_argument_id"]
        key = (event_id, base_argument_id)
        source_path = localize(source_row["e040_topology"])
        target_path = localize(source_row["e020_topology"])
        source_document = json.loads(source_path.read_text(encoding="utf-8"))
        target_document = json.loads(target_path.read_text(encoding="utf-8"))
        compatible = structurally_compatible(source_document, target_document)
        sweep_compatible = all(
            structural_rows[key][field] == "True"
            for field in (
                "class_descriptor_equal",
                "surface_crossing_counts_equal",
                "crossing_multisets_equal",
                "pair_winding_balances_equal",
            )
        )
        base = {
            "event_id": event_id,
            "base_argument_id": base_argument_id,
            "e040_source_path": str(source_path),
            "e020_validation_path": str(target_path),
            "structurally_compatible": compatible,
            "agrees_with_5056_structural_gate": compatible == sweep_compatible,
            "fallback_required": not compatible,
            "transport_attempted": compatible,
        }
        if compatible:
            transported = transport_pair(source_document, target_document)
            row = {
                **base,
                **transported,
                "transport_within_residue_tolerance": (
                    transported["signature_transport_error"]
                    < RESIDUE_MATCHING_TOLERANCE
                    and transported["maximum_expected_crossing_root_error"]
                    < RESIDUE_MATCHING_TOLERANCE
                ),
            }
        else:
            row = {
                **base,
                "transport_runtime_seconds": 0.0,
                "crossing_count": 0,
                "exact_numeric_signature_equal": False,
                "signature_transport_error": None,
                "maximum_expected_crossing_root_error": None,
                "maximum_source_representation_error": None,
                "maximum_projective_transport_step": None,
                "minimum_assignment_alternative_gap": None,
                "maximum_group_candidate_spread": None,
                "transport_within_residue_tolerance": False,
            }
        rows.append(row)
    attempted = [row for row in rows if row["transport_attempted"]]
    fallback = [row for row in rows if row["fallback_required"]]
    successful = [row for row in attempted if row["transport_within_residue_tolerance"]]
    exact = [row for row in attempted if row["exact_numeric_signature_equal"]]
    maximum_signature_error = max(
        float(row["signature_transport_error"]) for row in attempted
    )
    maximum_crossing_error = max(
        float(row["maximum_expected_crossing_root_error"]) for row in attempted
    )
    maximum_source_error = max(
        float(row["maximum_source_representation_error"]) for row in attempted
    )
    maximum_transport_step = max(
        float(row["maximum_projective_transport_step"]) for row in attempted
    )
    maximum_group_spread = max(
        float(row["maximum_group_candidate_spread"]) for row in attempted
    )
    total_runtime = sum(float(row["transport_runtime_seconds"]) for row in attempted)
    hybrid_authorized = (
        len(rows) == 120
        and len(attempted) == 119
        and len(fallback) == 1
        and len(successful) == len(attempted)
    )
    formal_digest = tree_digest(POST.parent / "formalization-workbench")
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "pair_count": len(rows),
        "transport_attempt_count": len(attempted),
        "full_homotopy_fallback_count": len(fallback),
        "full_homotopy_fallback_keys": [
            [row["event_id"], row["base_argument_id"]] for row in fallback
        ],
        "transport_tolerance_pass_count": len(successful),
        "exact_numeric_signature_count": len(exact),
        "maximum_signature_transport_error": maximum_signature_error,
        "maximum_expected_crossing_root_error": maximum_crossing_error,
        "maximum_source_representation_error": maximum_source_error,
        "maximum_projective_transport_step": maximum_transport_step,
        "maximum_group_candidate_spread": maximum_group_spread,
        "total_transport_runtime_seconds": total_runtime,
        "mean_transport_runtime_seconds": total_runtime / len(attempted),
        "residue_matching_tolerance": RESIDUE_MATCHING_TOLERANCE,
        "construction_uses_saved_e020_target_roots": False,
        "saved_e020_topologies_used_for_validation_only": True,
        "hybrid_e040_to_e020_transport_authorized_for_benchmark": hybrid_authorized,
        "universal_transport_authorized": len(fallback) == 0 and hybrid_authorized,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": (
            "project measured topology savings into unit-consistent estimator cost"
            if hybrid_authorized
            else "reject direct target-root transport"
        ),
        "formalization_workbench_tree_sha256": formal_digest,
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
            "5029, 5053, and 5056 source inputs exist",
        ),
        (
            "pair_matrix_complete",
            len(rows) == 120,
            f"{len(rows)} epsilon pairs audited",
        ),
        (
            "structural_sweep_reproduced",
            all(row["agrees_with_5056_structural_gate"] for row in rows),
            "direct structural comparison agrees with 5056",
        ),
        (
            "single_explicit_fallback",
            len(fallback) == 1
            and fallback[0]["event_id"] == "S503402_N0000"
            and fallback[0]["base_argument_id"] == "A06",
            f"fallbacks={[(row['event_id'], row['base_argument_id']) for row in fallback]}",
        ),
        (
            "all_seedable_pairs_transported",
            len(attempted) == 119 and len(successful) == 119,
            f"successful={len(successful)}/{len(attempted)}",
        ),
        (
            "residue_matching_tolerance",
            maximum_signature_error < RESIDUE_MATCHING_TOLERANCE
            and maximum_crossing_error < RESIDUE_MATCHING_TOLERANCE,
            f"signature={maximum_signature_error}; crossing={maximum_crossing_error}",
        ),
        (
            "source_branch_represented",
            maximum_source_error < RESIDUE_MATCHING_TOLERANCE,
            f"maximum source representation error={maximum_source_error}",
        ),
        (
            "projective_step_bounded",
            maximum_transport_step < 0.1,
            f"maximum direct transport step={maximum_transport_step}",
        ),
        (
            "hybrid_transport_gate",
            hybrid_authorized and not result["universal_transport_authorized"],
            "119 direct transports plus one mandatory full-homotopy fallback",
        ),
        (
            "no_target_leakage",
            not result["construction_uses_saved_e020_target_roots"]
            and result["saved_e020_topologies_used_for_validation_only"],
            "E020 full topology is an out-of-sample validation target only",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "claim_discipline",
            not result["fresh_kernel_execution_authorized"]
            and not result["valid_for_full_MTS_claim"],
            "transport benchmark does not authorize a physics claim or fresh kernel run",
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
                    "check_id": f"V5057_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5057 validation failed: {failed}")


if __name__ == "__main__":
    main()
