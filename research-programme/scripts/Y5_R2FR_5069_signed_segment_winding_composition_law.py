from __future__ import annotations

import copy
import csv
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5059 = POST / "scripts" / "Y5_R2FR_5059_short_epsilon_segment_transition_certificate.py"
SCRIPT_5061 = POST / "scripts" / "Y5_R2FR_5061_serialized_transport_topology_constructor_dry_run.py"
SOURCE_5057 = POST / "source-intake" / "functional_rg" / "5057"
SOURCE_5065 = POST / "source-intake" / "functional_rg" / "5065"
SOURCE = POST / "source-intake" / "functional_rg" / "5069"
CONSTRUCTED = SOURCE / "composed_topologies"
RESULT_JSON = SOURCE / "signed_segment_winding_composition_law.json"
ROW_CSV = SOURCE / "winding_composition_rows.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5069_VALIDATION.csv"
)
MARKER = "MTS_5069_SIGNED_SEGMENT_WINDING_COMPOSITION_LAW"
REVISION = "canonical-path-difference-plus-pathwise-root-transport-v2"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
STRAIGHT_STEP_LEVELS = (16, 32, 64, 128, 256)
FEYNMAN_STEP_LEVELS = (16, 32, 64, 128, 256, 512, 1024)
PROJECTIVE_LIMIT = 0.1
ROOT_MATCHING_TOLERANCE = 2.0e-5


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5059 = load_module("mts_5059_for_5069", SCRIPT_5059)
M5061 = load_module("mts_5061_for_5069", SCRIPT_5061)


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


def linear_leg(start: complex, end: complex, samples: int) -> list[complex]:
    if abs(end - start) < 1.0e-15:
        return [start]
    return [
        start + index / (samples - 1) * (end - start)
        for index in range(samples)
    ]


def canonical_feynman_difference_path(
    source_document: dict[str, Any], target: complex, samples: int
) -> list[complex]:
    if source_document.get("path_kind") != "feynman":
        raise ValueError("canonical difference path requires path_kind=feynman")
    source = complex(str(source_document["target_cosine"]))
    regulator = float(source_document["regulator"])
    source_floor = complex(source.real, regulator)
    target_floor = complex(target.real, regulator)
    path = [source]
    for endpoint in (source_floor, target_floor, target):
        path.extend(linear_leg(path[-1], endpoint, samples)[1:])
    return path


def endpoint_track_signature(gate: dict[str, Any]) -> tuple[Any, ...]:
    signature = []
    for chamber in gate["endpoint_root_tracks_by_chamber"]:
        rows = []
        for track in chamber:
            source = complex(track["source_root"])
            target = complex(track["target_root"])
            pairs = tuple(
                sorted(tuple(sorted(str(value) for value in pair)) for pair in track["initial_pairs"])
            )
            rows.append(
                (
                    pairs,
                    round(source.real, 8),
                    round(source.imag, 8),
                    round(target.real, 8),
                    round(target.imag, 8),
                )
            )
        signature.append(tuple(sorted(rows)))
    return tuple(signature)


def certify_segment(
    source_document: dict[str, Any], target: complex, suite: str
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    levels = []
    previous = None
    step_levels = (
        STRAIGHT_STEP_LEVELS
        if suite == "E040_TO_E020"
        else FEYNMAN_STEP_LEVELS
    )
    for steps in step_levels:
        if suite == "E040_TO_E020":
            cosines = linear_leg(
                complex(str(source_document["target_cosine"])), target, steps
            )
            path_geometry = "shared-feynman-path vertical difference"
        else:
            cosines = canonical_feynman_difference_path(
                source_document, target, steps
            )
            path_geometry = "reverse-source-vertical plus regulator-floor-horizontal plus target-vertical"
        current = M5059.cosine_path_gate(source_document, cosines)
        current["resolution"] = steps
        current["path_sample_count"] = len(cosines)
        current["path_geometry"] = path_geometry
        current["endpoint_track_signature"] = endpoint_track_signature(current)
        levels.append(current)
        if previous is not None:
            converged = (
                previous["transition_signature"] == current["transition_signature"]
                and previous["endpoint_track_signature"]
                == current["endpoint_track_signature"]
                and previous["groups_consistent"]
                and current["groups_consistent"]
                and max(
                    previous["maximum_projective_assignment_step"],
                    current["maximum_projective_assignment_step"],
                    previous["maximum_boundary_projective_step"],
                    current["maximum_boundary_projective_step"],
                )
                < PROJECTIVE_LIMIT
            )
            if converged:
                return current, levels
        previous = current
    return None, levels


def reduce_crossings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[float, float], list[dict[str, Any]]] = {}
    for row in rows:
        root = complex(row["target_root"])
        groups.setdefault((round(root.real, 8), round(root.imag, 8)), []).append(row)
    reduced = []
    for _, group in sorted(groups.items()):
        winding = sum(int(row["winding_correction"]) for row in group)
        if winding == 0:
            continue
        representative = copy.deepcopy(group[0])
        pairs = {
            tuple(sorted(str(value) for value in pair))
            for row in group
            for pair in row["representing_pairs"]
        }
        representative["representing_pairs"] = [list(pair) for pair in sorted(pairs)]
        representative["multiplicity"] = sum(int(row["multiplicity"]) for row in group)
        representative["winding_correction"] = winding
        representative["composition_source_count"] = len(group)
        reduced.append(representative)
    return reduced


def normalized_pair(pair: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(str(value) for value in pair))


def path_transport_crossing(
    crossing: dict[str, Any], tracks: list[dict[str, Any]]
) -> tuple[dict[str, Any], dict[str, float]]:
    source_root = complex(crossing["target_root"])
    candidates = []
    for pair_values in crossing["representing_pairs"]:
        pair = normalized_pair(pair_values)
        eligible = [
            track
            for track in tracks
            if pair
            in {
                normalized_pair(track_pair)
                for track_pair in track["initial_pairs"]
            }
        ]
        if not eligible:
            raise RuntimeError(f"no path root track represents source pair {pair}")
        selected = min(
            eligible,
            key=lambda track: M5059.M5030.chordal_distance(
                complex(track["source_root"]), source_root
            ),
        )
        candidates.append(
            {
                "source_error": M5059.M5030.chordal_distance(
                    complex(selected["source_root"]), source_root
                ),
                "target_root": complex(selected["target_root"]),
            }
        )
    selected = min(candidates, key=lambda row: row["source_error"])
    transported = copy.deepcopy(crossing)
    transported["target_root"] = str(selected["target_root"])
    return transported, {
        "maximum_source_representation_error": max(
            float(row["source_error"]) for row in candidates
        ),
        "group_candidate_spread": max(
            M5059.M5030.chordal_distance(
                selected["target_root"], row["target_root"]
            )
            for row in candidates
        ),
    }


def construct_path_transported_document(
    source_document: dict[str, Any],
    target: complex,
    source_path: Path,
    suite: str,
    gate: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, float | bool]]:
    document = copy.deepcopy(source_document)
    track_chambers = gate["endpoint_root_tracks_by_chamber"]
    endpoint_chambers = gate["target_endpoint_logs_by_chamber"]
    if not (
        len(document["chambers"])
        == len(track_chambers)
        == len(endpoint_chambers)
    ):
        raise RuntimeError("path transport chamber count mismatch")
    diagnostics = []
    total_crossings = 0
    for chamber, tracks, endpoints in zip(
        document["chambers"], track_chambers, endpoint_chambers
    ):
        transported_rows = []
        for crossing in chamber["surface_crossings"]:
            transported, diagnostic = path_transport_crossing(crossing, tracks)
            transported_rows.append(transported)
            diagnostics.append(diagnostic)
        chamber["surface_crossings"] = transported_rows
        chamber["surface_crossing_count"] = len(transported_rows)
        chamber["target_start_log"] = endpoints["target_start_log"]
        chamber["target_end_log"] = endpoints["target_end_log"]
        total_crossings += len(transported_rows)
    maximum_source_error = max(
        (
            float(row["maximum_source_representation_error"])
            for row in diagnostics
        ),
        default=0.0,
    )
    maximum_group_spread = max(
        (float(row["group_candidate_spread"]) for row in diagnostics),
        default=0.0,
    )
    document["checkpoint_marker"] = MARKER
    document["revision"] = REVISION
    document["config_digest"] = None
    document["target_cosine"] = str(target)
    document["topology_construction_method"] = (
        "canonical_path_difference_with_pathwise_root_transport"
    )
    document["transport_source_topology"] = str(source_path)
    document["transport_suite"] = suite
    document["transport_path_geometry"] = gate["path_geometry"]
    document["dry_run_only"] = True
    document["homotopy_steps"] = 0
    document["assignment_tracking_passed"] = True
    document["crossing_groups_consistent"] = bool(gate["groups_consistent"])
    document["fresh_kernel_execution_authorized"] = False
    document["valid_for_full_MTS_claim"] = False
    document["total_surface_crossings"] = total_crossings
    document["topology_class_descriptor"] = M5061.class_descriptor(document)
    document["topology_signature_digest"] = M5061.canonical_digest(
        M5061.serialized_signature(document)
    )
    return document, {
        "maximum_source_representation_error": maximum_source_error,
        "maximum_group_candidate_spread": maximum_group_spread,
        "path_root_transport_valid": (
            maximum_source_error < ROOT_MATCHING_TOLERANCE
            and maximum_group_spread < ROOT_MATCHING_TOLERANCE
        ),
    }


def compose_document(
    transported_source: dict[str, Any], segment_gate: dict[str, Any]
) -> dict[str, Any]:
    document = copy.deepcopy(transported_source)
    total = 0
    for chamber_index, (chamber, segment_crossings) in enumerate(zip(
        document["chambers"], segment_gate["grouped_crossings_by_chamber"]
    )):
        chamber["surface_crossings"] = reduce_crossings(
            [*chamber["surface_crossings"], *segment_crossings]
        )
        endpoint_tracks = segment_gate["endpoint_root_tracks_by_chamber"][
            chamber_index
        ]
        for crossing in chamber["surface_crossings"]:
            root = complex(crossing["target_root"])
            matching_tracks = [
                track
                for track in endpoint_tracks
                if M5059.M5030.chordal_distance(
                    complex(track["target_root"]), root
                )
                < ROOT_MATCHING_TOLERANCE
            ]
            if not matching_tracks:
                raise RuntimeError(
                    f"no endpoint collision track represents composed root {root}"
                )
            pairs = {
                normalized_pair(pair)
                for track in matching_tracks
                for pair in track["target_pairs"]
            }
            crossing["representing_pairs"] = [
                list(pair) for pair in sorted(pairs)
            ]
            crossing["multiplicity"] = len(matching_tracks)
        chamber["surface_crossing_count"] = len(chamber["surface_crossings"])
        total += len(chamber["surface_crossings"])
    document["checkpoint_marker"] = MARKER
    document["revision"] = REVISION
    document["topology_construction_method"] = (
        "transported_source_winding_plus_signed_segment_crossings"
    )
    document["segment_transition_count"] = int(
        segment_gate["total_transition_count"]
    )
    document["total_surface_crossings"] = total
    document["topology_class_descriptor"] = M5061.class_descriptor(document)
    document["topology_signature_digest"] = M5061.canonical_digest(
        M5061.serialized_signature(document)
    )
    document["fresh_kernel_execution_authorized"] = False
    document["valid_for_full_MTS_claim"] = False
    return document


def main() -> None:
    epsilon_rows_path = SOURCE_5057 / "epsilon_transport_rows.csv"
    argument_rows_path = SOURCE_5065 / "adjacent_argument_certificate_rows.csv"
    required = [SCRIPT_5059, SCRIPT_5061, epsilon_rows_path, argument_rows_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    cases = []
    for row in csv.DictReader(epsilon_rows_path.open(encoding="utf-8")):
        cases.append(
            {
                "suite": "E040_TO_E020",
                "event_id": row["event_id"],
                "segment_id": row["base_argument_id"],
                "source_path": localize(row["e040_source_path"]),
                "target_path": localize(row["e020_validation_path"]),
            }
        )
    for row in csv.DictReader(argument_rows_path.open(encoding="utf-8")):
        cases.append(
            {
                "suite": "E040_ARGUMENT_ADJACENCY",
                "event_id": row["event_id"],
                "segment_id": f"{row['left_argument_id']}_{row['right_argument_id']}",
                "source_path": localize(row["source_path"]),
                "target_path": localize(row["target_path"]),
            }
        )
    rows = []
    for case in cases:
        source_document = json.loads(case["source_path"].read_text(encoding="utf-8"))
        target_document = json.loads(case["target_path"].read_text(encoding="utf-8"))
        target = complex(str(target_document["target_cosine"]))
        certified, levels = certify_segment(
            source_document, target, case["suite"]
        )
        certificate_runtime = sum(
            float(level["runtime_seconds"]) for level in levels
        )
        if certified is None:
            rows.append(
                {
                    "suite": case["suite"],
                    "event_id": case["event_id"],
                    "segment_id": case["segment_id"],
                    "source_path": str(case["source_path"]),
                    "target_path": str(case["target_path"]),
                    "certified": False,
                    "selected_steps": None,
                    "path_sample_count": None,
                    "path_geometry": levels[-1]["path_geometry"],
                    "segment_transition_count": None,
                    "maximum_projective_assignment_step": max(
                        float(level["maximum_projective_assignment_step"])
                        for level in levels
                    ),
                    "certificate_runtime_seconds": certificate_runtime,
                    "constructed_path": "",
                    "path_root_transport_valid": None,
                    "maximum_source_representation_error": None,
                    "maximum_group_candidate_spread": None,
                    "signature_exact": None,
                    "class_exact": None,
                    "kernel_contract_exact": None,
                    "maximum_endpoint_log_error": None,
                }
            )
            continue
        transported, transport_diagnostics = construct_path_transported_document(
            source_document,
            target,
            case["source_path"],
            case["suite"],
            certified,
        )
        composed = compose_document(transported, certified)
        output_path = (
            CONSTRUCTED
            / case["suite"]
            / f"{case['event_id']}__{case['segment_id']}.json"
        )
        atomic_json(output_path, composed)
        signature_exact = (
            composed["topology_signature_digest"]
            == target_document["topology_signature_digest"]
        )
        class_exact = (
            composed["topology_class_descriptor"]
            == target_document["topology_class_descriptor"]
        )
        contract_exact = M5061.canonical_digest(M5061.kernel_contract(composed)) == M5061.canonical_digest(
            M5061.kernel_contract(target_document)
        )
        endpoint_maximum = M5061.endpoint_error(composed, target_document)
        rows.append(
            {
                "suite": case["suite"],
                "event_id": case["event_id"],
                "segment_id": case["segment_id"],
                "source_path": str(case["source_path"]),
                "target_path": str(case["target_path"]),
                "certified": True,
                "selected_steps": int(certified["resolution"]),
                "path_sample_count": int(certified["path_sample_count"]),
                "path_geometry": certified["path_geometry"],
                "segment_transition_count": int(
                    certified["total_transition_count"]
                ),
                "maximum_projective_assignment_step": float(
                    certified["maximum_projective_assignment_step"]
                ),
                "certificate_runtime_seconds": certificate_runtime,
                "constructed_path": str(output_path),
                "path_root_transport_valid": transport_diagnostics[
                    "path_root_transport_valid"
                ],
                "maximum_source_representation_error": transport_diagnostics[
                    "maximum_source_representation_error"
                ],
                "maximum_group_candidate_spread": transport_diagnostics[
                    "maximum_group_candidate_spread"
                ],
                "signature_exact": signature_exact,
                "class_exact": class_exact,
                "kernel_contract_exact": contract_exact,
                "maximum_endpoint_log_error": endpoint_maximum,
            }
        )
    certified_rows = [row for row in rows if row["certified"]]
    transition_rows = [
        row
        for row in certified_rows
        if int(row["segment_transition_count"]) > 0
    ]
    uncertified_rows = [row for row in rows if not row["certified"]]
    failed_rows = [
        row
        for row in certified_rows
        if not row["path_root_transport_valid"]
        or not row["signature_exact"]
        or not row["class_exact"]
        or not row["kernel_contract_exact"]
        or float(row["maximum_endpoint_log_error"]) >= 1.0e-10
    ]
    selected_step_counts: dict[str, int] = {}
    for row in certified_rows:
        key = str(row["selected_steps"])
        selected_step_counts[key] = selected_step_counts.get(key, 0) + 1
    maximum_source_error = max(
        (
            float(row["maximum_source_representation_error"])
            for row in certified_rows
        ),
        default=0.0,
    )
    maximum_group_spread = max(
        (
            float(row["maximum_group_candidate_spread"])
            for row in certified_rows
        ),
        default=0.0,
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "composition_law": "W(canonical target)=path-transport[W(canonical source)]+W(reverse source vertical + regulator-floor horizontal + target vertical)",
        "case_count": len(rows),
        "epsilon_case_count": sum(row["suite"] == "E040_TO_E020" for row in rows),
        "argument_case_count": sum(
            row["suite"] == "E040_ARGUMENT_ADJACENCY" for row in rows
        ),
        "certified_case_count": len(certified_rows),
        "certified_transition_case_count": len(transition_rows),
        "uncertified_case_count": len(uncertified_rows),
        "failed_composition_count": len(failed_rows),
        "selected_step_counts": selected_step_counts,
        "maximum_source_representation_error": maximum_source_error,
        "maximum_group_candidate_spread": maximum_group_spread,
        "maximum_endpoint_log_error": max(
            (float(row["maximum_endpoint_log_error"]) for row in certified_rows),
            default=0.0,
        ),
        "signed_winding_composition_gate_passed": (
            len(rows) == 232
            and len(certified_rows) == len(rows)
            and not failed_rows
            and bool(transition_rows)
        ),
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "build complete E040 argument chains using canonical path composition, then replay one transition kernel",
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
            "all epsilon and argument source/target topology paths exist",
        ),
        (
            "case_matrix_complete",
            len(rows) == 232,
            f"cases={len(rows)}",
        ),
        (
            "transition_cases_exercised",
            bool(transition_rows),
            f"certified transitions={len(transition_rows)}",
        ),
        (
            "all_certified_signatures_exact",
            not failed_rows,
            f"failed={len(failed_rows)}/{len(certified_rows)}",
        ),
        (
            "all_paths_certified",
            len(certified_rows) == len(rows),
            f"certified={len(certified_rows)}/{len(rows)}",
        ),
        (
            "pathwise_root_transport_bounded",
            maximum_source_error < ROOT_MATCHING_TOLERANCE
            and maximum_group_spread < ROOT_MATCHING_TOLERANCE,
            f"source={maximum_source_error}; spread={maximum_group_spread}",
        ),
        (
            "kernel_contracts_exact",
            all(row["kernel_contract_exact"] for row in certified_rows),
            f"exact={sum(bool(row['kernel_contract_exact']) for row in certified_rows)}/{len(certified_rows)}",
        ),
        (
            "endpoint_contract_exact",
            result["maximum_endpoint_log_error"] < 1.0e-10,
            f"maximum error={result['maximum_endpoint_log_error']}",
        ),
        (
            "composition_gate_passed",
            result["signed_winding_composition_gate_passed"],
            "path-transported source winding plus canonical path difference reproduces every full target",
        ),
        (
            "no_fresh_kernel_execution",
            not result["fresh_kernel_execution_authorized"],
            "composition gate compares saved topology contracts only",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "homotopy composition is an operational identity, not MTS evidence",
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
                    "check_id": f"V5069_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5069 validation failed: {failed_checks}")


if __name__ == "__main__":
    main()
