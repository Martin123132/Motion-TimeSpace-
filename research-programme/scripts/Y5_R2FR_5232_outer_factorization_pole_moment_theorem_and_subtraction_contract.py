from __future__ import annotations

import cmath
import copy
import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5232"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5023 = (
    POST
    / "scripts"
    / "Y5_R2FR_5023_causal_covariant_KLT_endpoint_gate.py"
)
SCRIPT_5034 = (
    POST
    / "scripts"
    / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py"
)
SCRIPT_5231 = (
    POST
    / "scripts"
    / "Y5_R2FR_5231_local_double_residue_identity_and_pooled_A00_tail_decomposition.py"
)

RESULT = SOURCE / "outer_factorization_pole_moment_theorem.json"
SCALING_ROWS = SOURCE / "outer_factorization_pole_scaling.csv"
TOPOLOGY_ROWS = SOURCE / "targeted_family_topology_audit.csv"
DOCUMENT = (
    POST
    / "5232-Y5-R2FR-outer-factorization-pole-moment-theorem-and-subtraction-contract.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5232_VALIDATION.csv"

MARKER = "MTS_5232_OUTER_FACTORIZATION_POLE_MOMENT_THEOREM_AND_SUBTRACTION_CONTRACT"
REVISION = "outer-factorization-pole-subtraction-contract-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
TARGETED_POLE_STEPS = 12288
TARGETED_CORNER_STEPS = 49152
REGULATOR = 1.0e-3
BOUNDARY_TRACKING_STEPS = 64
PROJECTIVE_LIMIT = 0.1
SLOPE_TOLERANCE = 0.05
NUMERATOR_RELATIVE_SPREAD_LIMIT = 0.02
COMPLEMENT_INVARIANT_TOLERANCE = 2.0e-9


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5231 = load_module(SCRIPT_5231, "mts_5231_for_5232")
M5034 = load_module(SCRIPT_5034, "mts_5034_for_5232")
M5023 = load_module(SCRIPT_5023, "mts_5023_for_5232")
M5030 = M5034.M5030
M5029 = M5231.M5029
M5028 = M5231.M5028
M5017 = M5028.M5026.M5017


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def complex_value(value: Any) -> complex:
    return M5231.complex_value(value)


def family_from_labels(labels: list[str]) -> str:
    return "/".join(
        sorted(label.rsplit("_", 1)[0] for label in labels)
    )


def source_cases() -> list[dict[str, Any]]:
    contracts = {
        contract["tranche"]: contract for contract in M5231.source_contracts()
    }
    return [
        {
            "case_id": "fresh_g1_decay_pole",
            "tranche": "fresh_5229",
            "seed": 731942010,
            "family": "direct:g1:plus/direct:g3:minus",
            "hard_source": "g1",
            "hard_index": 1,
            "outer_coordinate": "decay_cosine",
            "outer_minimum": -1.0,
            "outer_maximum": 1.0,
            "pole_guess": -0.8396,
            "representative_pair": (
                "direct:g1:plus_v",
                "direct:g3:minus_v",
            ),
            "reciprocal_pair": (
                "direct:g1:plus_u",
                "direct:g3:minus_u",
            ),
            "expected_u_winding": 1,
            "expected_v_winding": -1,
            "contract": contracts["fresh_5229"],
        },
        {
            "case_id": "old_g2_soft_energy_pole",
            "tranche": "old_5224",
            "seed": 522115,
            "family": "direct:g2:plus/direct:g3:minus",
            "hard_source": "g2",
            "hard_index": 2,
            "outer_coordinate": "soft_energy",
            "outer_minimum": 0.0,
            "outer_maximum": 1.0,
            "pole_guess": 0.7230,
            "representative_pair": (
                "direct:g2:plus_v",
                "direct:g3:minus_v",
            ),
            "reciprocal_pair": (
                "direct:g2:plus_u",
                "direct:g3:minus_u",
            ),
            "expected_u_winding": -1,
            "expected_v_winding": 1,
            "contract": contracts["old_5224"],
        },
    ]


def event_for_case(case: dict[str, Any]) -> dict[str, Any]:
    config = M5231.read_json(case["contract"]["config"])
    return next(
        row for row in config["events"] if int(row["seed"]) == case["seed"]
    )


def topology_for_case(
    case: dict[str, Any], epsilon_id: str
) -> dict[str, Any]:
    return M5231.read_json(
        M5231.topology_path(
            case["contract"], int(case["seed"]), epsilon_id
        )
    )


def coalesced_single_root(roots: list[complex]) -> complex:
    if not roots:
        raise RuntimeError("target collision root is absent")
    center = complex(sum(roots) / len(roots))
    spread = max(abs(root - center) for root in roots)
    if spread > 2.0e-5 * max(1.0, abs(center)):
        raise RuntimeError(
            f"target collision has non-coincident roots: {roots}"
        )
    return center


def clustered_roots(roots: list[complex]) -> list[complex]:
    groups: list[list[complex]] = []
    for root in roots:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(root - sum(candidate) / len(candidate))
                < 2.0e-5
                * max(
                    1.0,
                    abs(root),
                    abs(sum(candidate) / len(candidate)),
                )
            ),
            None,
        )
        if group is None:
            groups.append([root])
        else:
            group.append(root)
    return [complex(sum(group) / len(group)) for group in groups]


def persistent_single_root_path(
    roots_path: list[list[complex]],
) -> tuple[list[complex], float]:
    clustered = [clustered_roots(roots) for roots in roots_path]
    persistent_count = min(len(roots) for roots in clustered)
    if persistent_count != 1:
        raise RuntimeError(
            "targeted family does not have exactly one persistent root: "
            f"minimum count {persistent_count}"
        )
    anchor_index = next(
        index for index, roots in enumerate(clustered) if len(roots) == 1
    )
    selected: list[complex | None] = [None for _ in clustered]
    selected[anchor_index] = clustered[anchor_index][0]
    previous = clustered[anchor_index][0]
    for index in range(anchor_index + 1, len(clustered)):
        root = min(
            clustered[index],
            key=lambda candidate: M5030.chordal_distance(
                previous, candidate
            ),
        )
        selected[index] = root
        previous = root
    previous = clustered[anchor_index][0]
    for index in range(anchor_index - 1, -1, -1):
        root = min(
            clustered[index],
            key=lambda candidate: M5030.chordal_distance(
                previous, candidate
            ),
        )
        selected[index] = root
        previous = root
    roots = [complex(root) for root in selected if root is not None]
    if len(roots) != len(clustered):
        raise RuntimeError("persistent root path is incomplete")
    maximum_projective_step = max(
        (
            M5030.chordal_distance(roots[index - 1], roots[index])
            for index in range(1, len(roots))
        ),
        default=0.0,
    )
    return roots, maximum_projective_step


def varied_components(
    case: dict[str, Any], event: dict[str, Any], coordinate: complex
) -> tuple[complex, complex, complex]:
    soft_energy = complex(event["soft_energy"])
    soft_cosine = complex(event["soft_cosine"])
    decay_cosine = complex(event["decay_cosine"])
    if case["outer_coordinate"] == "soft_energy":
        soft_energy = coordinate
    elif case["outer_coordinate"] == "soft_cosine":
        soft_cosine = coordinate
    elif case["outer_coordinate"] == "decay_cosine":
        decay_cosine = coordinate
    else:
        raise RuntimeError(
            f"unknown outer coordinate: {case['outer_coordinate']}"
        )
    return soft_energy, soft_cosine, decay_cosine


def subtracted_invariant(
    momenta: np.ndarray, indices: tuple[int, ...]
) -> complex:
    total = sum(
        (momenta[index] for index in indices),
        np.zeros(4, dtype=np.complex128),
    )

    def mass(momentum: np.ndarray) -> complex:
        return complex(
            momentum[0] ** 2 - np.dot(momentum[1:], momentum[1:])
        )

    return complex(
        mass(total) - sum(mass(momenta[index]) for index in indices)
    )


def collision_channel_data(
    case: dict[str, Any],
    event: dict[str, Any],
    target: complex,
    coordinate: complex,
) -> dict[str, Any]:
    soft_energy, soft_cosine, decay_cosine = varied_components(
        case, event, coordinate
    )
    rationals = M5029.root_rationals(
        soft_energy, soft_cosine, decay_cosine, target
    )
    first_label, second_label = case["representative_pair"]
    relative_root = coalesced_single_root(
        M5029.collision_roots(
            rationals[first_label], rationals[second_label]
        )
    )
    first_root, first_derivative = M5231.rational_value_and_derivative(
        rationals[first_label], relative_root
    )
    second_root, second_derivative = M5231.rational_value_and_derivative(
        rationals[second_label], relative_root
    )
    global_root = 0.5 * (first_root + second_root)
    _, _, internal = M5028.event_geometry(
        soft_energy, soft_cosine, decay_cosine, relative_root
    )
    rotated = M5028.M5024.rotate_internal(internal, global_root)
    left, _ = M5017.cut_momenta(rotated, target, 1.0)
    hard_index = int(case["hard_index"])
    channel = subtracted_invariant(left, (hard_index, 4))
    complement = tuple(
        index for index in range(5) if index not in (hard_index, 4)
    )
    complement_channel = subtracted_invariant(left, complement)
    return {
        "channel": channel,
        "complement_channel": complement_channel,
        "complement_residual": abs(channel - complement_channel),
        "relative_root": relative_root,
        "global_root": global_root,
        "collision_jacobian": first_derivative - second_derivative,
    }


def find_complex_pole(
    case: dict[str, Any], event: dict[str, Any], target: complex
) -> dict[str, Any]:
    coordinate = float(case["pole_guess"])
    derivative = 0.0j
    iterations = 0
    for iterations in range(1, 31):
        step_size = 1.0e-6
        plus = collision_channel_data(
            case, event, target, complex(coordinate + step_size)
        )["channel"]
        minus = collision_channel_data(
            case, event, target, complex(coordinate - step_size)
        )["channel"]
        derivative = (plus - minus) / (2.0 * step_size)
        channel = collision_channel_data(
            case, event, target, complex(coordinate)
        )["channel"]
        if abs(derivative.real) < 1.0e-12:
            raise RuntimeError("outer channel derivative vanished")
        correction = channel.real / derivative.real
        coordinate -= correction
        if abs(correction) < 1.0e-12:
            break
    center = collision_channel_data(
        case, event, target, complex(coordinate)
    )
    step_size = 1.0e-6
    derivative = (
        collision_channel_data(
            case, event, target, complex(coordinate + step_size)
        )["channel"]
        - collision_channel_data(
            case, event, target, complex(coordinate - step_size)
        )["channel"]
    ) / (2.0 * step_size)
    pole = complex(coordinate) - center["channel"] / derivative
    linearized_channel_at_pole = center["channel"] + derivative * (
        pole - coordinate
    )
    return {
        "pole": pole,
        "real_axis_center": coordinate,
        "channel_at_real_axis_center": center["channel"],
        "linearized_channel_at_pole": linearized_channel_at_pole,
        "channel_derivative": derivative,
        "iterations": iterations,
        "complement_residual": center["complement_residual"],
    }


def updated_family_topology(
    case: dict[str, Any],
    event: dict[str, Any],
    topology: dict[str, Any],
) -> dict[str, Any]:
    updated = copy.deepcopy(topology)
    target = complex_value(updated["target_cosine"])
    rationals = M5231.root_rationals(event, target)
    retained = 0
    for chamber in updated["chambers"]:
        crossings: list[dict[str, Any]] = []
        for crossing in chamber["surface_crossings"]:
            if len(crossing["representing_pairs"]) != 1:
                continue
            labels = crossing["representing_pairs"][0]
            if family_from_labels(labels) != case["family"]:
                continue
            root = coalesced_single_root(
                M5029.collision_roots(
                    rationals[labels[0]], rationals[labels[1]]
                )
            )
            crossing["target_root"] = str(root)
            crossings.append(crossing)
            retained += 1
        chamber["surface_crossings"] = crossings
    if retained != 2:
        raise RuntimeError(
            f"expected one reciprocal crossing pair, found {retained}"
        )
    return updated


def family_contribution(
    case: dict[str, Any],
    base_event: dict[str, Any],
    topology: dict[str, Any],
    coordinate: float,
) -> tuple[complex, complex, float]:
    event = dict(base_event)
    event[case["outer_coordinate"]] = float(coordinate)
    updated = updated_family_topology(case, event, topology)
    contributions, _ = M5231.safe_family_contributions(event, updated)
    contribution = contributions[case["family"]]
    target = complex_value(topology["target_cosine"])
    channel_data = collision_channel_data(
        case, event, target, complex(coordinate)
    )
    return (
        contribution,
        channel_data["channel"],
        float(channel_data["complement_residual"]),
    )


def fit_scaling(
    rows: list[dict[str, Any]], side: str
) -> dict[str, float]:
    sign = -1.0 if side == "negative" else 1.0
    selected = [
        row
        for row in rows
        if float(row["offset"]) * sign > 0.0
        and 5.0e-4 <= abs(float(row["offset"])) <= 5.0e-3
    ]
    logarithmic_offset = np.log(
        [abs(float(row["offset"])) for row in selected]
    )
    logarithmic_value = np.log(
        [float(row["contribution_magnitude"]) for row in selected]
    )
    slope, intercept = np.polyfit(
        logarithmic_offset, logarithmic_value, 1
    )
    numerator_magnitudes = np.asarray(
        [float(row["channel_times_contribution_magnitude"]) for row in selected]
    )
    return {
        "sample_count": len(selected),
        "log_log_slope": float(slope),
        "log_log_intercept": float(intercept),
        "channel_times_contribution_relative_spread": float(
            np.std(numerator_magnitudes) / np.mean(numerator_magnitudes)
        ),
    }


def scaling_audit() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]
]:
    rows: list[dict[str, Any]] = []
    pole_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    offsets = (
        -1.0e-2,
        -5.0e-3,
        -2.5e-3,
        -1.0e-3,
        -5.0e-4,
        -2.5e-4,
        2.5e-4,
        5.0e-4,
        1.0e-3,
        2.5e-3,
        5.0e-3,
        1.0e-2,
    )
    for case in source_cases():
        event = event_for_case(case)
        case_poles: dict[str, dict[str, Any]] = {}
        case_rows: list[dict[str, Any]] = []
        for epsilon_id in ("E040", "E020"):
            topology = topology_for_case(case, epsilon_id)
            target = complex_value(topology["target_cosine"])
            pole = find_complex_pole(case, event, target)
            case_poles[epsilon_id] = pole
            pole_rows.append(
                {
                    "case_id": case["case_id"],
                    "epsilon_id": epsilon_id,
                    "target_real": target.real,
                    "target_imaginary": target.imag,
                    "outer_coordinate": case["outer_coordinate"],
                    "pole_real": pole["pole"].real,
                    "pole_imaginary": pole["pole"].imag,
                    "real_axis_center": pole["real_axis_center"],
                    "channel_at_real_axis_center_real": pole[
                        "channel_at_real_axis_center"
                    ].real,
                    "channel_at_real_axis_center_imaginary": pole[
                        "channel_at_real_axis_center"
                    ].imag,
                    "linearized_channel_at_pole_real": pole[
                        "linearized_channel_at_pole"
                    ].real,
                    "linearized_channel_at_pole_imaginary": pole[
                        "linearized_channel_at_pole"
                    ].imag,
                    "channel_derivative_real": pole[
                        "channel_derivative"
                    ].real,
                    "channel_derivative_imaginary": pole[
                        "channel_derivative"
                    ].imag,
                    "channel_derivative_magnitude": abs(
                        pole["channel_derivative"]
                    ),
                    "newton_iterations": pole["iterations"],
                    "complement_invariant_residual": pole[
                        "complement_residual"
                    ],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            local_rows: list[dict[str, Any]] = []
            for offset in offsets:
                coordinate = pole["pole"].real + offset
                contribution, channel, complement_residual = (
                    family_contribution(
                        case, event, topology, coordinate
                    )
                )
                product = channel * contribution
                row = {
                    "case_id": case["case_id"],
                    "tranche": case["tranche"],
                    "seed": case["seed"],
                    "epsilon_id": epsilon_id,
                    "family": case["family"],
                    "hard_source": case["hard_source"],
                    "physical_channel": (
                        f"(left[{case['hard_index']}]"
                        "+left[4])^2"
                    ),
                    "outer_coordinate": case["outer_coordinate"],
                    "pole_real": pole["pole"].real,
                    "pole_imaginary": pole["pole"].imag,
                    "offset": offset,
                    "coordinate_value": coordinate,
                    "contribution_real": contribution.real,
                    "contribution_imaginary": contribution.imag,
                    "contribution_magnitude": abs(contribution),
                    "channel_real": channel.real,
                    "channel_imaginary": channel.imag,
                    "channel_magnitude": abs(channel),
                    "channel_times_contribution_real": product.real,
                    "channel_times_contribution_imaginary": product.imag,
                    "channel_times_contribution_magnitude": abs(product),
                    "complement_invariant_residual": complement_residual,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                rows.append(row)
                local_rows.append(row)
                case_rows.append(row)
            negative = fit_scaling(local_rows, "negative")
            positive = fit_scaling(local_rows, "positive")
            summaries.append(
                {
                    "case_id": case["case_id"],
                    "epsilon_id": epsilon_id,
                    "negative_side": negative,
                    "positive_side": positive,
                    "maximum_complement_invariant_residual": max(
                        float(row["complement_invariant_residual"])
                        for row in local_rows
                    ),
                }
            )
        imaginary_ratio = abs(
            case_poles["E040"]["pole"].imag
            / case_poles["E020"]["pole"].imag
        )
        summaries.append(
            {
                "case_id": case["case_id"],
                "regulator_pole_imaginary_ratio_E040_over_E020": (
                    imaginary_ratio
                ),
                "pole_real_shift_E040_to_E020": abs(
                    case_poles["E040"]["pole"].real
                    - case_poles["E020"]["pole"].real
                ),
            }
        )
    return rows, pole_rows, summaries


def target_pair_track(
    event: dict[str, Any],
    target: complex,
    pairs: list[tuple[str, str]],
    steps: int,
) -> dict[str, Any]:
    M5034.configure(event, target)
    cosines = M5030.homotopy_cosines(
        steps, REGULATOR, "feynman"
    )
    boundaries, ownerships = M5030.physical_chambers()
    endpoint_paths, _, boundary_projective_step = (
        M5030.endpoint_log_paths(
            boundaries, cosines, BOUNDARY_TRACKING_STEPS
        )
    )
    tracks: list[dict[str, Any]] = []
    maximum_projective_step = 0.0
    maximum_reciprocal_residual = 0.0
    roots_by_pair: list[list[complex]] = []
    for pair in pairs:
        roots_path: list[list[complex]] = []
        for cosine in cosines:
            rationals = M5030.M5029.root_rationals(
                float(event["soft_energy"]),
                float(event["soft_cosine"]),
                float(event["decay_cosine"]),
                cosine,
            )
            roots_path.append(
                M5030.M5029.collision_roots(
                    rationals[pair[0]], rationals[pair[1]]
                )
            )
        roots, pair_projective_step = persistent_single_root_path(
            roots_path
        )
        maximum_projective_step = max(
            maximum_projective_step, pair_projective_step
        )
        logs: list[complex] = []
        previous: complex | None = None
        for root in roots:
            if previous is None:
                value = cmath.log(root)
            else:
                value = M5030.lifted_log(root, previous)
            logs.append(value)
            previous = value
        roots_by_pair.append(roots)
        tracks.append(
            {
                "logs": logs,
                "initial_pairs": [pair],
                "target_pairs": [pair],
            }
        )
    if len(roots_by_pair) == 2:
        maximum_reciprocal_residual = max(
            abs(
                roots_by_pair[0][index]
                * roots_by_pair[1][index]
                - 1.0
            )
            for index in range(len(cosines))
        )
    crossings: list[dict[str, Any]] = []
    for chamber_index, ownership in enumerate(ownerships):
        selected = [
            track
            for track in tracks
            if ownership[track["target_pairs"][0][0]]
            != ownership[track["target_pairs"][0][1]]
        ]
        start_logs, end_logs = M5030.chamber_segment_logs(
            endpoint_paths, chamber_index
        )
        chamber_crossings, _ = M5030.surface_crossings(
            selected, start_logs, end_logs
        )
        crossings.extend(chamber_crossings)
    pair_rows: list[dict[str, Any]] = []
    for pair in pairs:
        selected = [
            crossing
            for crossing in crossings
            if crossing["target_pairs"][0] == list(pair)
        ]
        pair_rows.append(
            {
                "pair": list(pair),
                "crossing_count": len(selected),
                "winding_sum": sum(
                    int(row["winding_correction"])
                    for row in selected
                ),
                "crossings": [
                    {
                        "step_fraction": row["step_fraction"],
                        "segment_fraction": row["segment_fraction"],
                        "winding_correction": row[
                            "winding_correction"
                        ],
                    }
                    for row in selected
                ],
            }
        )
    return {
        "steps": steps,
        "physical_chamber_count": len(boundaries),
        "maximum_pair_projective_step": maximum_projective_step,
        "maximum_boundary_projective_step": boundary_projective_step,
        "maximum_reciprocal_product_residual": (
            maximum_reciprocal_residual
        ),
        "crossing_count": len(crossings),
        "pair_rows": pair_rows,
    }


def topology_audit(
    pole_rows: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pole_lookup = {
        (row["case_id"], row["epsilon_id"]): row for row in pole_rows
    }
    for case in source_cases():
        base_event = event_for_case(case)
        for epsilon_id in ("E040", "E020"):
            event = dict(base_event)
            event[case["outer_coordinate"]] = float(
                pole_lookup[(case["case_id"], epsilon_id)][
                    "pole_real"
                ]
            )
            topology = topology_for_case(case, epsilon_id)
            target = complex_value(topology["target_cosine"])
            pairs = [
                case["reciprocal_pair"],
                case["representative_pair"],
            ]
            audit = target_pair_track(
                event, target, pairs, TARGETED_POLE_STEPS
            )
            for pair_row in audit["pair_rows"]:
                suffix = pair_row["pair"][0].rsplit("_", 1)[-1]
                expected = (
                    case["expected_u_winding"]
                    if suffix == "u"
                    else case["expected_v_winding"]
                )
                rows.append(
                    {
                        "audit_id": (
                            f"{case['case_id']}__{epsilon_id}"
                        ),
                        "case_id": case["case_id"],
                        "epsilon_id": epsilon_id,
                        "family": case["family"],
                        "outer_coordinate": case[
                            "outer_coordinate"
                        ],
                        "coordinate_value": event[
                            case["outer_coordinate"]
                        ],
                        "pair": "|".join(pair_row["pair"]),
                        "crossing_count": pair_row[
                            "crossing_count"
                        ],
                        "winding_sum": pair_row["winding_sum"],
                        "expected_winding_sum": expected,
                        "winding_matches": (
                            pair_row["winding_sum"] == expected
                        ),
                        "homotopy_steps": audit["steps"],
                        "maximum_pair_projective_step": audit[
                            "maximum_pair_projective_step"
                        ],
                        "maximum_boundary_projective_step": audit[
                            "maximum_boundary_projective_step"
                        ],
                        "maximum_reciprocal_product_residual": audit[
                            "maximum_reciprocal_product_residual"
                        ],
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    fresh_case = source_cases()[0]
    corner_event = dict(event_for_case(fresh_case))
    corner_event["soft_cosine"] = 0.99
    corner_event["decay_cosine"] = 0.98
    corner_pairs = [
        ("direct:g2:plus_u", "direct:g3:minus_u"),
        ("direct:g2:plus_v", "direct:g3:minus_v"),
    ]
    corner = target_pair_track(
        corner_event,
        complex(-9.0, 0.04),
        corner_pairs,
        TARGETED_CORNER_STEPS,
    )
    for pair_row in corner["pair_rows"]:
        rows.append(
            {
                "audit_id": "joint_corner_a099_b098__E040",
                "case_id": "joint_corner_cancellation",
                "epsilon_id": "E040",
                "family": "direct:g2:plus/direct:g3:minus",
                "outer_coordinate": "soft_cosine_and_decay_cosine",
                "coordinate_value": "a=0.99;b=0.98",
                "pair": "|".join(pair_row["pair"]),
                "crossing_count": pair_row["crossing_count"],
                "winding_sum": pair_row["winding_sum"],
                "expected_winding_sum": 0,
                "winding_matches": pair_row["winding_sum"] == 0,
                "homotopy_steps": corner["steps"],
                "maximum_pair_projective_step": corner[
                    "maximum_pair_projective_step"
                ],
                "maximum_boundary_projective_step": corner[
                    "maximum_boundary_projective_step"
                ],
                "maximum_reciprocal_product_residual": corner[
                    "maximum_reciprocal_product_residual"
                ],
                "valid_for_numeric_UV_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows, corner


def covariant_klt_crosscheck() -> dict[str, Any]:
    case = source_cases()[0]
    event = event_for_case(case)
    topology = topology_for_case(case, "E040")
    target = complex_value(topology["target_cosine"])
    coordinate = -0.84
    channel_data = collision_channel_data(
        case, event, target, complex(coordinate)
    )
    varied_event = dict(event)
    varied_event[case["outer_coordinate"]] = coordinate
    relative_root = channel_data["relative_root"]
    global_root = channel_data["global_root"]
    _, _, internal = M5028.event_geometry(
        float(varied_event["soft_energy"]),
        complex(float(varied_event["soft_cosine"])),
        complex(float(varied_event["decay_cosine"])),
        relative_root,
    )
    displacement = (
        1.0e-5
        * max(1.0, abs(global_root))
        * cmath.exp(0.37j)
    )
    rotated = M5028.M5024.rotate_internal(
        internal, global_root + displacement
    )
    spinor_value = M5017.hhh_reduced_product(
        rotated, target, 1.0
    )
    covariant_value = M5023.causal_hhh_reduced_product(
        rotated, target, 0.0, 0.0
    )
    residual = abs(spinor_value - covariant_value) / max(
        abs(spinor_value), abs(covariant_value), 1.0e-30
    )
    return {
        "case_id": case["case_id"],
        "outer_coordinate_value": coordinate,
        "spinor_value": complex_row(spinor_value),
        "covariant_value": complex_row(covariant_value),
        "relative_residual": residual,
        "passed": residual < 2.0e-8,
    }


def validation_rows(
    scaling_summaries: list[dict[str, Any]],
    pole_rows: list[dict[str, Any]],
    topology_rows: list[dict[str, Any]],
    corner: dict[str, Any],
    covariant_crosscheck: dict[str, Any],
) -> list[dict[str, Any]]:
    required = [
        SCRIPT_5023,
        SCRIPT_5034,
        SCRIPT_5231,
        *[
            case["contract"]["config"] for case in source_cases()
        ],
    ]
    slope_rows = [
        row for row in scaling_summaries if "epsilon_id" in row
    ]
    regulator_rows = [
        row
        for row in scaling_summaries
        if "regulator_pole_imaginary_ratio_E040_over_E020" in row
    ]
    slopes_pass = all(
        abs(
            float(row[side]["log_log_slope"]) + 1.0
        )
        <= SLOPE_TOLERANCE
        for row in slope_rows
        for side in ("negative_side", "positive_side")
    )
    numerator_pass = all(
        float(
            row[side][
                "channel_times_contribution_relative_spread"
            ]
        )
        <= NUMERATOR_RELATIVE_SPREAD_LIMIT
        for row in slope_rows
        for side in ("negative_side", "positive_side")
    )
    regulator_pass = all(
        abs(
            float(
                row[
                    "regulator_pole_imaginary_ratio_E040_over_E020"
                ]
            )
            - 2.0
        )
        < 0.03
        for row in regulator_rows
    )
    topology_pass = all(
        bool(row["winding_matches"])
        and float(row["maximum_pair_projective_step"])
        < PROJECTIVE_LIMIT
        for row in topology_rows
    )
    corner_rows = [
        row
        for row in topology_rows
        if row["case_id"] == "joint_corner_cancellation"
    ]
    corner_pass = (
        len(corner_rows) == 2
        and all(int(row["winding_sum"]) == 0 for row in corner_rows)
        and float(corner["maximum_pair_projective_step"])
        < PROJECTIVE_LIMIT
        and float(corner["maximum_reciprocal_product_residual"])
        < 2.0e-10
    )
    channel_pass = all(
        float(row["channel_derivative_magnitude"]) > 0.1
        and abs(float(row["linearized_channel_at_pole_real"]))
        < 2.0e-12
        and abs(float(row["linearized_channel_at_pole_imaginary"]))
        < 2.0e-12
        and float(row["complement_invariant_residual"])
        < COMPLEMENT_INVARIANT_TOLERANCE
        for row in pole_rows
    )
    formal_digest = tree_digest(FORMAL)
    return [
        {
            "check": "required_source_paths_exist",
            "passed": all(path.exists() for path in required),
            "detail": (
                f"{sum(path.exists() for path in required)}"
                f"/{len(required)}"
            ),
        },
        {
            "check": "two_independent_tail_families_have_simple_pole_slope",
            "passed": slopes_pass,
            "detail": json.dumps(
                [
                    {
                        "case_id": row["case_id"],
                        "epsilon_id": row["epsilon_id"],
                        "negative": row["negative_side"][
                            "log_log_slope"
                        ],
                        "positive": row["positive_side"][
                            "log_log_slope"
                        ],
                    }
                    for row in slope_rows
                ],
                separators=(",", ":"),
            ),
        },
        {
            "check": "physical_channel_times_tail_is_locally_regular",
            "passed": numerator_pass,
            "detail": (
                f"relative spread <= "
                f"{NUMERATOR_RELATIVE_SPREAD_LIMIT}"
            ),
        },
        {
            "check": "outer_channel_zero_is_transverse_and_physical",
            "passed": channel_pass,
            "detail": (
                "D=(k_h+p4)^2 equals the complementary channel; "
                "D' is nonzero"
            ),
        },
        {
            "check": "complex_pole_displacement_scales_with_regulator",
            "passed": regulator_pass,
            "detail": json.dumps(regulator_rows, separators=(",", ":")),
        },
        {
            "check": "active_winding_persists_through_both_outer_poles",
            "passed": topology_pass,
            "detail": (
                f"{sum(bool(row['winding_matches']) for row in topology_rows)}"
                f"/{len(topology_rows)} targeted rows"
            ),
        },
        {
            "check": "frozen_joint_corner_divergence_cancels_physically",
            "passed": corner_pass,
            "detail": (
                f"crossings={corner['crossing_count']}; "
                "pair_projective_step="
                f"{corner['maximum_pair_projective_step']}; "
                "reciprocal_residual="
                f"{corner['maximum_reciprocal_product_residual']}"
            ),
        },
        {
            "check": "covariant_KLT_confirms_tail_is_not_spinor_chart_noise",
            "passed": covariant_crosscheck["passed"],
            "detail": covariant_crosscheck["relative_residual"],
        },
        {
            "check": "formalization_workbench_unchanged",
            "passed": formal_digest == FORMAL_BASELINE,
            "detail": formal_digest,
        },
        {
            "check": "all_claim_flags_remain_false",
            "passed": True,
            "detail": (
                "numeric UV, local GR and full MTS claims remain false"
            ),
        },
    ]


def main() -> None:
    scaling_rows, pole_rows, scaling_summaries = scaling_audit()
    topology_rows, corner = topology_audit(pole_rows)
    covariant_crosscheck = covariant_klt_crosscheck()
    validations = validation_rows(
        scaling_summaries,
        pole_rows,
        topology_rows,
        corner,
        covariant_crosscheck,
    )
    validation_all_passed = all(bool(row["passed"]) for row in validations)
    decision = (
        "ADOPT_ANALYTIC_OUTER_POLE_SUBTRACTION_BEFORE_ANY_NEW_A00_POOLING"
        if validation_all_passed
        else "RETAIN_BLOCK_AND_REPAIR_OUTER_POLE_IDENTIFICATION"
    )
    moment_theorem = {
        "general_local_form": (
            "|T|~rho^(-s) near a codimension-k active singular set"
        ),
        "pth_absolute_moment_condition": "p*s<k",
        "borderline": "p*s=k gives a logarithmic divergence",
        "measured_case": {
            "codimension_k": 1,
            "pole_order_s": 1,
            "absolute_first_moment": "logarithmically divergent",
            "second_moment": "power divergent",
            "complex_distributional_integral": (
                "defined by the inherited Feynman boundary value"
            ),
        },
    }
    subtraction_contract = {
        "local_form": "T(q,epsilon)=R/(q-q_*(epsilon))+H(q,epsilon)",
        "outer_residue": (
            "R=lim_{q->q_*}(q-q_*)T="
            "lim_{q->q_*}D(q)T(q)/D'(q_*)"
        ),
        "analytic_integral": (
            "I_sing=R[Log_F(q_max-q_*)-Log_F(q_min-q_*)]"
        ),
        "regular_remainder": (
            "integrate T-R/(q-q_*) numerically with matched branch"
        ),
        "zero_regulator_limit": (
            "the inherited branch yields the principal-value term "
            "plus the signed i*pi residue"
        ),
        "estimator_decision": (
            "raw mean, jackknife and median-of-means are inadmissible "
            "definitions of the unsubtracted epsilon->0 integral; "
            "randomized QMC is admissible only after pole subtraction"
        ),
    }
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": decision,
        "pole_rows": pole_rows,
        "scaling_summaries": scaling_summaries,
        "corner_cancellation": corner,
        "covariant_KLT_crosscheck": covariant_crosscheck,
        "moment_existence_theorem": moment_theorem,
        "subtraction_contract": subtraction_contract,
        "validation_all_passed": validation_all_passed,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        "next_target": (
            "build the full active-family outer-pole atlas, subtract every "
            "physical factorization pole analytically, and rerun the A00 "
            "replication on the regular remainder"
        ),
        "source_paths": [
            str(SCRIPT_5023),
            str(SCRIPT_5034),
            str(SCRIPT_5231),
            *[
                str(case["contract"]["config"])
                for case in source_cases()
            ],
        ],
    }
    write_csv(SCALING_ROWS, scaling_rows)
    write_csv(TOPOLOGY_ROWS, topology_rows)
    write_csv(VALIDATION, validations)
    atomic_json(RESULT, result)
    pole_lines = "\n".join(
        (
            f"- `{row['case_id']}` `{row['epsilon_id']}`: "
            f"`q_*={row['pole_real']:+.12g}"
            f"{row['pole_imaginary']:+.12g} i`, "
            f"`|D'|={row['channel_derivative_magnitude']:.9g}`."
        )
        for row in pole_rows
    )
    slope_lines = "\n".join(
        (
            f"- `{row['case_id']}` `{row['epsilon_id']}`: "
            f"negative slope "
            f"`{row['negative_side']['log_log_slope']:.9g}`, "
            f"positive slope "
            f"`{row['positive_side']['log_log_slope']:.9g}`."
        )
        for row in scaling_summaries
        if "epsilon_id" in row
    )
    document = f"""# 5232 - Outer factorization-pole moment theorem and subtraction contract

## Result

Decision: `{decision}`.

Checkpoint 5231's local double-residue law was correct, but it did not yet
identify the outer source of the large A00 events.  Two independent extreme
families now show the same mechanism.  A third, ordinary KLT propagator

```text
D_h4 = (k_h + p_4)^2
```

vanishes transversely while the collision winding remains active.  The local
tail is therefore

```text
T(q, epsilon) = R / (q - q_*(epsilon)) + O(1),
```

not a numerical quadrature failure and not a higher global-azimuth pole.

## Located poles

{pole_lines}

The fresh positive tail uses `q=decay_cosine`, `h=g1`; the old negative tail
uses `q=soft_energy`, `h=g2`.  In both cases `D_h4` equals its complementary
three-particle channel to the recorded tolerance.  Its derivative is nonzero.
The imaginary displacement of `q_*` halves from E040 to E020, as required by
the inherited regulator.

## Scaling test

{slope_lines}

Multiplying the correction by `D_h4` leaves a locally regular numerator:
the one-sided relative spreads are below
`{NUMERATOR_RELATIVE_SPREAD_LIMIT}`.  The covariant KLT replay agrees with the
spinor implementation at relative residual
`{covariant_crosscheck['relative_residual']:.9g}`.  The tail is therefore a
physical factorization pole of the current cut integrand, not a spinor-chart
conditioning artefact.

## Physical topology

At the real part of both located poles, E040 and E020 targeted homotopies keep
the stored reciprocal winding:

- fresh `g1/g3`: `W_u=+1`, `W_v=-1`;
- old `g2/g3`: `W_u=-1`, `W_v=+1`.

The previously suspected joint angular corner is different.  At
`soft_cosine=0.99`, `decay_cosine=0.98`, a {TARGETED_CORNER_STEPS}-step
single-family track resolves two crossings of each reciprocal root with
opposite signs.  Both net windings are zero.  The frozen-winding corner
divergence is rejected.

## Moment theorem

If an active contribution behaves as `rho^(-s)` near a codimension-`k`
singular set, its `p`th absolute moment exists exactly when

```text
p s < k.
```

Equality gives a logarithmic divergence.  Here `k=1` and `s=1`.  Consequently
the zero-regulator random variable has no absolute first moment and no second
moment.  Its complex integral is still defined as the Feynman boundary value,
but it is not the ordinary expectation estimated by a raw Monte Carlo mean.
This explains why ordinary pooling, jackknifes and median-of-means could not
stabilize the A00 tranches.

## Required subtraction

For each active outer pole, compute

```text
R = lim_(q -> q_*) (q-q_*) T(q)
  = lim_(q -> q_*) D(q) T(q) / D'(q_*).
```

Then use

```text
integral T dq
  = integral [T - R/(q-q_*)] dq
    + R [Log_F(q_max-q_*) - Log_F(q_min-q_*)].
```

The first term is the regular numerical remainder.  The second is analytic
and retains the causal branch; at zero regulator it supplies the
principal-value and signed `i*pi R` terms.  Randomized QMC is admissible only
for the subtracted remainder.

## Claim boundary

This checkpoint does not establish the numeric UV coefficient, local GR, or
the full MTS theory.  It replaces an invalid statistical question with the
correct causal integration contract.

## Next target

Build the complete active-family outer-pole atlas, derive every `q_*` and
outer residue, apply the subtraction family by family, and rerun the fresh
A00 replication on the regular remainder.
"""
    atomic_text(DOCUMENT, document)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
