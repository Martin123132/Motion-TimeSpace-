from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5030 = (
    POST
    / "scripts"
    / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py"
)
GRID_EVENTS = (
    {
        "event_id": "E00_baseline",
        "soft_energy": 0.37,
        "soft_cosine": 0.23,
        "decay_cosine": -0.31,
    },
    {
        "event_id": "E01_low_mixed",
        "soft_energy": 0.12,
        "soft_cosine": -0.65,
        "decay_cosine": 0.45,
    },
    {
        "event_id": "E02_low_opposite",
        "soft_energy": 0.20,
        "soft_cosine": 0.62,
        "decay_cosine": -0.55,
    },
    {
        "event_id": "E03_mid_negative",
        "soft_energy": 0.32,
        "soft_cosine": -0.25,
        "decay_cosine": -0.70,
    },
    {
        "event_id": "E04_mid_mixed",
        "soft_energy": 0.48,
        "soft_cosine": 0.70,
        "decay_cosine": 0.12,
    },
    {
        "event_id": "E05_high_negative",
        "soft_energy": 0.65,
        "soft_cosine": -0.72,
        "decay_cosine": -0.18,
    },
    {
        "event_id": "E06_high_positive",
        "soft_energy": 0.82,
        "soft_cosine": 0.35,
        "decay_cosine": 0.72,
    },
    {
        "event_id": "E07_central_symmetric",
        "soft_energy": 0.50,
        "soft_cosine": 0.0,
        "decay_cosine": 0.0,
    },
    {
        "event_id": "E08_near_polar",
        "soft_energy": 0.72,
        "soft_cosine": 0.82,
        "decay_cosine": -0.78,
    },
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5030 = load_module("mts_5030_for_5032", SCRIPT_5030)


def configure_event(event: dict[str, Any]) -> None:
    M5030.SOFT_ENERGY = float(event["soft_energy"])
    M5030.SOFT_COSINE = float(event["soft_cosine"])
    M5030.DECAY_COSINE = float(event["decay_cosine"])


def topology_signature(document: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(net_chamber_signature(chamber) for chamber in document["chambers"])


def net_chamber_signature(chamber: dict[str, Any]) -> tuple[Any, ...]:
    windings: dict[tuple[float, float], int] = {}
    for row in chamber["surface_crossings"]:
        root = complex(row["target_root"])
        key = (round(root.real, 8), round(root.imag, 8))
        windings[key] = windings.get(key, 0) + int(
            row["winding_correction"]
        )
    return tuple(
        sorted(
            (winding, root[0], root[1])
            for root, winding in windings.items()
            if winding != 0
        )
    )


def topology_class_descriptor(document: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(
        (
            len(signature),
            sum(row[0] > 0 for row in signature),
            sum(row[0] < 0 for row in signature),
        )
        for signature in topology_signature(document)
    )


def minimum_crossing_margin(document: dict[str, Any]) -> float:
    margins = [
        min(
            float(row["segment_fraction"]),
            1.0 - float(row["segment_fraction"]),
        )
        for chamber in document["chambers"]
        for row in chamber["surface_crossings"]
    ]
    return min(margins) if margins else 1.0


def event_summary(
    event: dict[str, Any], document: dict[str, Any], output_name: str
) -> dict[str, Any]:
    descriptor = topology_class_descriptor(document)
    return {
        **event,
        "output_file": output_name,
        "physical_chamber_count": len(document["chambers"]),
        "path_kind": document["path_kind"],
        "homotopy_steps": document["homotopy_steps"],
        "crossing_counts": [
            len(signature) for signature in topology_signature(document)
        ],
        "raw_crossing_counts": [
            chamber["surface_crossing_count"] for chamber in document["chambers"]
        ],
        "winding_balance": [
            sum(
                row["winding_correction"]
                for row in chamber["surface_crossings"]
            )
            for chamber in document["chambers"]
        ],
        "topology_class_descriptor": [list(row) for row in descriptor],
        "maximum_assignment_log_step": document[
            "maximum_collision_assignment_log_step"
        ],
        "maximum_assignment_projective_step": document[
            "maximum_collision_assignment_projective_step"
        ],
        "maximum_boundary_assignment_log_step": document[
            "maximum_boundary_assignment_log_step"
        ],
        "maximum_boundary_assignment_projective_step": document[
            "maximum_boundary_assignment_projective_step"
        ],
        "radially_excluded_transition_count": document[
            "radially_excluded_transition_count"
        ],
        "assignment_tracking_passed": document[
            "assignment_tracking_passed"
        ],
        "crossing_groups_consistent": document[
            "crossing_groups_consistent"
        ],
        "minimum_crossing_segment_margin": minimum_crossing_margin(
            document
        ),
        "topology_scan_passed": document["assignment_tracking_passed"]
        and document["crossing_groups_consistent"],
    }


def run_event(
    event: dict[str, Any],
    steps: int,
    regulator: float,
    path_kind: str,
    boundary_tracking_steps: int,
    output_directory: Path,
    reuse_existing: bool = True,
) -> tuple[dict[str, Any], str]:
    output_name = (
        f"{event['event_id']}_{path_kind}_reg{regulator:.0e}_steps{steps}.json"
    )
    output_path = output_directory / output_name
    if reuse_existing and output_path.exists():
        candidate = json.loads(output_path.read_text(encoding="utf-8"))
        expected_parameterization = (
            "piecewise linear +i0 with projective root tracking"
            if path_kind == "feynman"
            else "piecewise linear"
        )
        if (
            candidate.get("event_id") == event["event_id"]
            and candidate.get("homotopy_steps") == steps
            and candidate.get("regulator") == regulator
            and candidate.get("path_kind") == path_kind
            and candidate.get("soft_energy") == event["soft_energy"]
            and candidate.get("soft_cosine") == event["soft_cosine"]
            and candidate.get("decay_cosine") == event["decay_cosine"]
            and candidate.get("path_parameterization")
            == expected_parameterization
            and "maximum_collision_assignment_projective_step" in candidate
            and "maximum_boundary_assignment_projective_step" in candidate
            and "radially_excluded_transition_count" in candidate
        ):
            return candidate, output_name
    configure_event(event)
    document = M5030.homotopy_gate(
        steps,
        regulator,
        path_kind,
        boundary_tracking_steps,
    )
    document["event_id"] = event["event_id"]
    output_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return document, output_name


def run_event_adaptive(
    event: dict[str, Any],
    steps: int,
    regulator: float,
    path_kind: str,
    boundary_tracking_steps: int,
    output_directory: Path,
    maximum_steps: int,
) -> tuple[dict[str, Any], str]:
    current_steps = steps
    while True:
        document, output_name = run_event(
            event,
            current_steps,
            regulator,
            path_kind,
            boundary_tracking_steps,
            output_directory,
        )
        if (
            document["assignment_tracking_passed"]
            and document["crossing_groups_consistent"]
        ):
            return document, output_name
        if current_steps >= maximum_steps:
            return document, output_name
        current_steps *= 2


def class_key(row: dict[str, Any]) -> str:
    return json.dumps(row["topology_class_descriptor"], separators=(",", ":"))


def select_representatives(rows: list[dict[str, Any]]) -> list[str]:
    classes: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        classes.setdefault(class_key(row), []).append(row)
    representatives: list[str] = []
    for members in classes.values():
        representative = min(
            members,
            key=lambda row: (
                row["minimum_crossing_segment_margin"],
                -row["maximum_assignment_projective_step"],
            ),
        )
        representatives.append(representative["event_id"])
    return representatives


def refinement_variants(
    effective_steps: int, base_regulator: float
) -> tuple[dict[str, Any], ...]:
    return (
        {
            "variant": "smaller_regulator",
            "steps": effective_steps,
            "regulator": base_regulator / 10.0,
            "path_kind": "feynman",
            "required_for_gate": True,
        },
        {
            "variant": "double_steps",
            "steps": 2 * effective_steps,
            "regulator": base_regulator,
            "path_kind": "feynman",
            "required_for_gate": True,
        },
        {
            "variant": "raised_path_diagnostic",
            "steps": min(2 * effective_steps, 6144),
            "regulator": base_regulator,
            "path_kind": "raised",
            "required_for_gate": False,
        },
        {
            "variant": "direct_path_diagnostic",
            "steps": min(2 * effective_steps, 6144),
            "regulator": base_regulator,
            "path_kind": "direct",
            "required_for_gate": False,
        },
    )


def multi_event_gate(
    steps: int,
    regulator: float,
    boundary_tracking_steps: int,
    output_directory: Path,
) -> dict[str, Any]:
    output_directory.mkdir(parents=True, exist_ok=True)
    grid_rows: list[dict[str, Any]] = []
    base_documents: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, Any]] = []
    for event in GRID_EVENTS:
        try:
            document, output_name = run_event_adaptive(
                event,
                steps,
                regulator,
                "feynman",
                boundary_tracking_steps,
                output_directory,
                16 * steps,
            )
            base_documents[event["event_id"]] = document
            grid_rows.append(event_summary(event, document, output_name))
        except Exception as error:
            failures.append(
                {
                    "event_id": event["event_id"],
                    "stage": "base_scan",
                    "required_for_gate": True,
                    "error": f"{type(error).__name__}: {error}",
                }
            )
    representatives = select_representatives(grid_rows)
    event_lookup = {event["event_id"]: event for event in GRID_EVENTS}
    refinement_rows: list[dict[str, Any]] = []
    for event_id in representatives:
        event = event_lookup[event_id]
        base = base_documents[event_id]
        base_signature = topology_signature(base)
        for variant in refinement_variants(
            int(base["homotopy_steps"]), regulator
        ):
            try:
                document, output_name = run_event_adaptive(
                    event,
                    variant["steps"],
                    variant["regulator"],
                    variant["path_kind"],
                    boundary_tracking_steps,
                    output_directory,
                    4 * variant["steps"],
                )
                signature_match = topology_signature(document) == base_signature
                refinement_rows.append(
                    {
                        "event_id": event_id,
                        **variant,
                        "output_file": output_name,
                        "signature_matches_base": signature_match,
                        "assignment_tracking_passed": document[
                            "assignment_tracking_passed"
                        ],
                        "crossing_groups_consistent": document[
                            "crossing_groups_consistent"
                        ],
                        "maximum_assignment_log_step": document[
                            "maximum_collision_assignment_log_step"
                        ],
                        "maximum_assignment_projective_step": document[
                            "maximum_collision_assignment_projective_step"
                        ],
                        "maximum_boundary_assignment_log_step": document[
                            "maximum_boundary_assignment_log_step"
                        ],
                        "maximum_boundary_assignment_projective_step": document[
                            "maximum_boundary_assignment_projective_step"
                        ],
                        "radially_excluded_transition_count": document[
                            "radially_excluded_transition_count"
                        ],
                        "effective_homotopy_steps": document[
                            "homotopy_steps"
                        ],
                        "refinement_passed": signature_match
                        and document["assignment_tracking_passed"]
                        and document["crossing_groups_consistent"],
                    }
                )
            except Exception as error:
                failures.append(
                    {
                        "event_id": event_id,
                        "stage": variant["variant"],
                        "required_for_gate": variant[
                            "required_for_gate"
                        ],
                        "error": f"{type(error).__name__}: {error}",
                    }
                )
    class_rows: list[dict[str, Any]] = []
    classes: dict[str, list[dict[str, Any]]] = {}
    for row in grid_rows:
        classes.setdefault(class_key(row), []).append(row)
    for index, (descriptor, members) in enumerate(sorted(classes.items())):
        class_rows.append(
            {
                "class_id": f"C{index}",
                "descriptor": json.loads(descriptor),
                "event_ids": [row["event_id"] for row in members],
                "representative_event_id": next(
                    event_id
                    for event_id in representatives
                    if event_id in {row["event_id"] for row in members}
                ),
            }
        )
    required_failures = [
        row for row in failures if row["required_for_gate"]
    ]
    required_refinements = [
        row for row in refinement_rows if row["required_for_gate"]
    ]
    diagnostic_refinements = [
        row for row in refinement_rows if not row["required_for_gate"]
    ]
    grid_passed = (
        len(grid_rows) == len(GRID_EVENTS)
        and not any(row["stage"] == "base_scan" for row in required_failures)
        and all(row["topology_scan_passed"] for row in grid_rows)
    )
    refinement_passed = (
        len(required_refinements) == 2 * len(representatives)
        and not any(
            row["stage"] != "base_scan" for row in required_failures
        )
        and all(row["refinement_passed"] for row in required_refinements)
    )
    return {
        "grid_design": (
            "nine-point deterministic space-filling stress grid with "
            "canonical fixed-+i0 Feynman continuation followed by a "
            "vertical lift to the target complex kinematics; roots are "
            "tracked projectively across zero and infinity"
        ),
        "soft_energy_range": [
            min(event["soft_energy"] for event in GRID_EVENTS),
            max(event["soft_energy"] for event in GRID_EVENTS),
        ],
        "soft_cosine_range": [
            min(event["soft_cosine"] for event in GRID_EVENTS),
            max(event["soft_cosine"] for event in GRID_EVENTS),
        ],
        "decay_cosine_range": [
            min(event["decay_cosine"] for event in GRID_EVENTS),
            max(event["decay_cosine"] for event in GRID_EVENTS),
        ],
        "base_steps": steps,
        "base_regulator": regulator,
        "grid_rows": grid_rows,
        "topology_classes": class_rows,
        "representative_event_ids": representatives,
        "refinement_rows": refinement_rows,
        "failures": failures,
        "required_failure_count": len(required_failures),
        "required_refinement_count": len(required_refinements),
        "diagnostic_refinement_count": len(diagnostic_refinements),
        "path_diagnostic_match_count": sum(
            row["refinement_passed"] for row in diagnostic_refinements
        ),
        "path_diagnostic_total": len(diagnostic_refinements),
        "grid_event_count": len(grid_rows),
        "topology_class_count": len(class_rows),
        "grid_topology_gate_passed": grid_passed,
        "class_refinement_gate_passed": refinement_passed,
        "multi_event_causal_topology_gate_passed": grid_passed
        and refinement_passed,
        "event_integrals_evaluated": False,
        "outer_phase_space_integration_complete": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=768)
    parser.add_argument("--regulator", type=float, default=1.0e-5)
    parser.add_argument("--boundary-tracking-steps", type=int, default=64)
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=POST / "source-intake" / "functional_rg" / "5032" / "events",
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = multi_event_gate(
        arguments.steps,
        arguments.regulator,
        arguments.boundary_tracking_steps,
        arguments.output_directory,
    )
    serialized = json.dumps(result, indent=2)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
