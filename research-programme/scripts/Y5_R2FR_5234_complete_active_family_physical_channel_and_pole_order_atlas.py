from __future__ import annotations

import cmath
import csv
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5234"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5024 = (
    POST
    / "scripts"
    / "Y5_R2FR_5024_physical_propagator_pole_classification_and_coupled_cycle_transport.py"
)
SCRIPT_5127 = (
    POST
    / "scripts"
    / "Y5_R2FR_5127_same_sheet_outer_collinear_pole_chart_and_A00_replay.py"
)
SCRIPT_5138 = (
    POST
    / "scripts"
    / "Y5_R2FR_5138_A04_KLT_collinear_pole_order_proof.py"
)
SCRIPT_5231 = (
    POST
    / "scripts"
    / "Y5_R2FR_5231_local_double_residue_identity_and_pooled_A00_tail_decomposition.py"
)
SCRIPT_5232 = (
    POST
    / "scripts"
    / "Y5_R2FR_5232_outer_factorization_pole_moment_theorem_and_subtraction_contract.py"
)

FAMILY_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5231"
    / "pooled_A00_tail_family_decomposition.csv"
)
SCALAR_GRAVITON_PROOF = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5138"
    / "A04_KLT_collinear_pole_order_proof.json"
)
GRAVITON_GRAVITON_PROOF = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5127"
    / "same_sheet_outer_collinear_pole_chart_gate.json"
)

RESULT = SOURCE / "complete_active_family_physical_channel_and_pole_order_atlas.json"
FAMILY_ROWS = SOURCE / "active_residue_family_inventory.csv"
COMPONENT_ROWS = SOURCE / "active_residue_component_and_summand_ownership.csv"
COLLISION_ROWS = SOURCE / "source_label_physical_channel_witness.csv"
FORMULA_ROWS = SOURCE / "physical_channel_equation_witness.csv"
SURFACE_ROWS = SOURCE / "physical_channel_surface_definitions.csv"
ATLAS_ROWS = SOURCE / "complete_active_family_pole_atlas.csv"
SCALING_ROWS = SOURCE / "active_internal_collinear_simple_pole_scaling.csv"
DOCUMENT = (
    POST
    / "5234-Y5-R2FR-complete-active-family-physical-channel-and-pole-order-atlas.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5234_VALIDATION.csv"

MARKER = "MTS_5234_COMPLETE_ACTIVE_FAMILY_PHYSICAL_CHANNEL_AND_POLE_ORDER_ATLAS"
REVISION = "complete-active-family-channel-atlas-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
ACTIVE_FAMILY_FLOOR = 1.0e-12
OWNER_FRACTION_MINIMUM = 0.999
CHANNEL_ZERO_RELATIVE_TOLERANCE = 2.0e-7
FORMULA_RELATIVE_TOLERANCE = 2.0e-10
SCALING_SLOPE_TOLERANCE = 0.07
REGULAR_NUMERATOR_SPREAD_LIMIT = 0.03
PROJECTIVE_LIMIT = 0.1
TOPOLOGY_STEPS = 12288


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5232 = load_module(SCRIPT_5232, "mts_5232_for_5234")
M5231 = M5232.M5231
M5024 = M5232.M5028.M5024
M5023 = M5232.M5023
M5022 = M5232.M5028.M5026.M5022
M5017 = M5232.M5017


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def pair_invariant(momenta: np.ndarray, first: int, second: int) -> complex:
    return M5232.subtracted_invariant(momenta, (first, second))


def vector_invariant(first: np.ndarray, second: np.ndarray) -> complex:
    return complex(2.0 * M5023.minkowski(first, second))


def active_family_inventory() -> list[dict[str, Any]]:
    with FAMILY_SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    grouped: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        grouped[row["family"]].append(row)
    maxima: list[dict[str, Any]] = []
    for family, rows in grouped.items():
        maximum_row = max(
            rows, key=lambda row: float(row["A00_family_magnitude"])
        )
        maximum = float(maximum_row["A00_family_magnitude"])
        if maximum <= ACTIVE_FAMILY_FLOOR:
            continue
        maxima.append(
            {
                "family": family,
                "maximum_A00_family_magnitude": maximum,
                "nonzero_event_count": sum(
                    float(row["A00_family_magnitude"])
                    > ACTIVE_FAMILY_FLOOR
                    for row in rows
                ),
                "representative_tranche": maximum_row["tranche"],
                "representative_seed": int(maximum_row["seed"]),
                "representative_A00_family_real": float(
                    maximum_row["A00_family_real"]
                ),
                "representative_A00_family_imaginary": float(
                    maximum_row["A00_family_imaginary"]
                ),
                "source_path": str(FAMILY_SOURCE),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    maxima.sort(
        key=lambda row: float(row["maximum_A00_family_magnitude"]),
        reverse=True,
    )
    for index, row in enumerate(maxima, start=1):
        row["family_id"] = f"AF{index:02d}"
    return maxima


def event_for_inventory(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = next(
        contract
        for contract in M5231.source_contracts()
        if contract["tranche"] == row["representative_tranche"]
    )
    configuration = M5231.read_json(contract["config"])
    event = next(
        event
        for event in configuration["events"]
        if int(event["seed"]) == int(row["representative_seed"])
    )
    return contract, event


def component_inventory(
    family_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    components: list[dict[str, Any]] = []
    for family_row in family_rows:
        contract, event = event_for_inventory(family_row)
        topology = M5231.read_json(
            M5231.topology_path(
                contract, int(family_row["representative_seed"]), "E020"
            )
        )
        target = M5231.complex_value(topology["target_cosine"])
        family_pairs = [
            (first, second, residual)
            for first, second, residual in M5231.reciprocal_pairs(topology)
            if M5231.canonical_family(first, second) == family_row["family"]
        ]
        for component_index, (first, second, reciprocal_residual) in enumerate(
            family_pairs, start=1
        ):
            representative, partner = (
                (first, second)
                if abs(M5231.complex_value(first["target_root"])) >= 1.0
                else (second, first)
            )
            labels = list(representative["representing_pairs"][0])
            predicted_owner = (
                "endpoint_subtraction"
                if any(
                    label.startswith("subtraction:decay:") for label in labels
                )
                else "direct_five_point"
            )
            components.append(
                {
                    "component_id": (
                        f"{family_row['family_id']}_C{component_index:02d}"
                    ),
                    "family_id": family_row["family_id"],
                    "family": family_row["family"],
                    "component_index": component_index,
                    "tranche": family_row["representative_tranche"],
                    "seed": int(family_row["representative_seed"]),
                    "epsilon_id": "E020",
                    "target": target,
                    "event": event,
                    "topology": topology,
                    "representative": representative,
                    "partner": partner,
                    "representative_labels": labels,
                    "partner_labels": list(
                        partner["representing_pairs"][0]
                    ),
                    "predicted_owner": predicted_owner,
                    "reciprocal_root_residual": float(reciprocal_residual),
                    "source_topology": str(
                        M5231.topology_path(
                            contract,
                            int(family_row["representative_seed"]),
                            "E020",
                        )
                    ),
                }
            )
    return components


def entry_geometry(
    component: dict[str, Any], entry: dict[str, Any]
) -> dict[str, Any]:
    event = component["event"]
    target = component["target"]
    labels = list(entry["representing_pairs"][0])
    relative_root = M5231.complex_value(entry["target_root"])
    rationals = M5231.root_rationals(event, target)
    global_values = [
        M5231.rational_value_and_derivative(
            rationals[label], relative_root
        )[0]
        for label in labels
    ]
    global_root = complex(sum(global_values) / len(global_values))
    soft_direction, decay_direction, internal = M5232.M5028.event_geometry(
        float(event["soft_energy"]),
        complex(float(event["soft_cosine"])),
        complex(float(event["decay_cosine"])),
        relative_root,
    )
    rotated_internal = M5024.rotate_internal(internal, global_root)
    left, right = M5017.cut_momenta(rotated_internal, target, 1.0)
    return {
        "labels": labels,
        "relative_root": relative_root,
        "global_root": global_root,
        "global_root_spread": max(
            abs(value - global_root) for value in global_values
        ),
        "soft_direction": soft_direction,
        "decay_direction": decay_direction,
        "internal": internal,
        "rotated_internal": rotated_internal,
        "left": left,
        "right": right,
    }


def split_double_residue_owner(component: dict[str, Any]) -> dict[str, Any]:
    geometry = entry_geometry(component, component["representative"])
    event = component["event"]
    target = component["target"]
    global_root = geometry["global_root"]
    internal = geometry["internal"]
    soft_direction = geometry["soft_direction"]
    decay_direction = geometry["decay_direction"]
    soft_energy = float(event["soft_energy"])
    scale = max(1.0, abs(global_root))
    phase = cmath.exp(0.37j)
    samples: list[tuple[complex, complex, complex]] = []
    for fraction in (1.0e-5, 5.0e-6):
        displacement = fraction * scale * phase
        rotated = M5024.rotate_internal(
            internal, global_root + displacement
        )
        inverse_energy_square_sum = sum(
            1.0 / (momentum[0] * momentum[0]) for momentum in rotated
        )
        multiplier = (
            3.0
            / (rotated[2, 0] * rotated[2, 0])
            / inverse_energy_square_sum
        )
        direct = (
            soft_energy
            * soft_energy
            * multiplier
            * M5017.hhh_reduced_product(rotated, target, 1.0)
            / (M5017.S_VALUE * M5017.S_VALUE)
        )
        endpoint = M5022.endpoint_value(
            soft_direction,
            decay_direction,
            target,
            global_root + displacement,
        )
        direct_coefficient = direct / soft_energy * displacement**2
        endpoint_coefficient = -endpoint / soft_energy * displacement**2
        samples.append(
            (
                complex(direct_coefficient),
                complex(endpoint_coefficient),
                complex(direct_coefficient + endpoint_coefficient),
            )
        )
    direct_coefficient = 2.0 * samples[-1][0] - samples[-2][0]
    endpoint_coefficient = 2.0 * samples[-1][1] - samples[-2][1]
    full_coefficient = 2.0 * samples[-1][2] - samples[-2][2]
    direct_magnitude = abs(direct_coefficient)
    endpoint_magnitude = abs(endpoint_coefficient)
    denominator = max(direct_magnitude + endpoint_magnitude, 1.0e-300)
    measured_owner = (
        "direct_five_point"
        if direct_magnitude >= endpoint_magnitude
        else "endpoint_subtraction"
    )
    owner_fraction = max(direct_magnitude, endpoint_magnitude) / denominator
    closure_residual = abs(
        full_coefficient - direct_coefficient - endpoint_coefficient
    ) / max(abs(full_coefficient), 1.0e-30)
    return {
        "direct_double_coefficient": direct_coefficient,
        "endpoint_double_coefficient": endpoint_coefficient,
        "full_double_coefficient": full_coefficient,
        "direct_double_coefficient_magnitude": direct_magnitude,
        "endpoint_double_coefficient_magnitude": endpoint_magnitude,
        "measured_owner": measured_owner,
        "owner_fraction": owner_fraction,
        "owner_matches_prediction": (
            measured_owner == component["predicted_owner"]
        ),
        "summand_split_relative_closure_residual": closure_residual,
    }


def serialize_components(
    components: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    owner_results: dict[str, dict[str, Any]] = {}
    for component in components:
        owner = split_double_residue_owner(component)
        owner_results[component["component_id"]] = owner
        rows.append(
            {
                "component_id": component["component_id"],
                "family_id": component["family_id"],
                "family": component["family"],
                "component_index": component["component_index"],
                "tranche": component["tranche"],
                "seed": component["seed"],
                "epsilon_id": component["epsilon_id"],
                "representative_labels": "|".join(
                    component["representative_labels"]
                ),
                "partner_labels": "|".join(
                    component["partner_labels"]
                ),
                "representative_relative_root": component[
                    "representative"
                ]["target_root"],
                "partner_relative_root": component["partner"]["target_root"],
                "representative_winding": int(
                    component["representative"]["winding_correction"]
                ),
                "partner_winding": int(
                    component["partner"]["winding_correction"]
                ),
                "predicted_owner": component["predicted_owner"],
                "measured_owner": owner["measured_owner"],
                "owner_fraction": owner["owner_fraction"],
                "owner_matches_prediction": owner[
                    "owner_matches_prediction"
                ],
                "direct_double_coefficient_real": owner[
                    "direct_double_coefficient"
                ].real,
                "direct_double_coefficient_imaginary": owner[
                    "direct_double_coefficient"
                ].imag,
                "direct_double_coefficient_magnitude": owner[
                    "direct_double_coefficient_magnitude"
                ],
                "endpoint_double_coefficient_real": owner[
                    "endpoint_double_coefficient"
                ].real,
                "endpoint_double_coefficient_imaginary": owner[
                    "endpoint_double_coefficient"
                ].imag,
                "endpoint_double_coefficient_magnitude": owner[
                    "endpoint_double_coefficient_magnitude"
                ],
                "summand_split_relative_closure_residual": owner[
                    "summand_split_relative_closure_residual"
                ],
                "reciprocal_root_residual": component[
                    "reciprocal_root_residual"
                ],
                "source_topology": component["source_topology"],
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows, owner_results


def direct_label_surface(label: str) -> tuple[str, tuple[int, int]]:
    match = re.fullmatch(r"direct:g([123]):(plus|minus)_[uv]", label)
    if match is None:
        raise RuntimeError(f"not a direct source label: {label}")
    internal = int(match.group(1))
    sign = match.group(2)
    if sign == "plus":
        return f"direct:R:s0{internal}", (0, internal)
    return f"direct:R:s{internal}4", (internal, 4)


def endpoint_label_surface(
    label: str,
) -> tuple[str, str, tuple[int, int] | None]:
    direct_match = re.fullmatch(
        r"direct:g3:(plus|minus)_[uv]", label
    )
    if direct_match is not None:
        if direct_match.group(1) == "plus":
            return "endpoint:R:soft:s03", "03", None
        return "endpoint:R:soft:s34", "34", None
    decay_match = re.fullmatch(
        r"subtraction:decay:(plus|minus)_[uv]", label
    )
    if decay_match is None:
        raise RuntimeError(f"not an endpoint source label: {label}")
    if decay_match.group(1) == "plus":
        return "endpoint:R:hard:s01=s24", "01=24", (0, 1)
    return "endpoint:R:hard:s02=s14", "02=14", (0, 2)


def collision_channel_witnesses(
    components: list[dict[str, Any]],
    owner_results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for component in components:
        owner = owner_results[component["component_id"]]["measured_owner"]
        for reciprocal_member, entry in (
            ("representative", component["representative"]),
            ("partner", component["partner"]),
        ):
            geometry = entry_geometry(component, entry)
            endpoint_left: np.ndarray | None = None
            endpoint_right: np.ndarray | None = None
            soft_left: np.ndarray | None = None
            soft_right: np.ndarray | None = None
            if owner == "endpoint_subtraction":
                soft_rotated = M5022.rotate_vector(
                    geometry["soft_direction"], geometry["global_root"]
                )
                decay_rotated = M5022.rotate_vector(
                    geometry["decay_direction"], geometry["global_root"]
                )
                endpoint_internal = np.zeros(
                    (3, 4), dtype=np.complex128
                )
                endpoint_internal[0] = np.concatenate(
                    ([1.0], decay_rotated)
                )
                endpoint_internal[1] = np.concatenate(
                    ([1.0], -decay_rotated)
                )
                endpoint_left, endpoint_right = M5017.cut_momenta(
                    endpoint_internal, component["target"], 1.0
                )
                soft_left = np.concatenate(([1.0], soft_rotated)).astype(
                    np.complex128
                )
                soft_right = -soft_left
            for label in geometry["labels"]:
                if owner == "direct_five_point":
                    surface_id, pair = direct_label_surface(label)
                    value = pair_invariant(
                        geometry["right"], pair[0], pair[1]
                    )
                    scale = max(
                        1.0,
                        abs(geometry["right"][pair[0], 0])
                        * abs(geometry["right"][pair[1], 0]),
                    )
                    aliases = surface_id.rsplit(":", 1)[-1]
                else:
                    surface_id, aliases, hard_pair = (
                        endpoint_label_surface(label)
                    )
                    if hard_pair is not None:
                        if endpoint_right is None:
                            raise RuntimeError("endpoint momenta are absent")
                        value = pair_invariant(
                            endpoint_right, hard_pair[0], hard_pair[1]
                        )
                        scale = max(
                            1.0,
                            abs(endpoint_right[hard_pair[0], 0])
                            * abs(endpoint_right[hard_pair[1], 0]),
                        )
                    else:
                        if endpoint_right is None or soft_right is None:
                            raise RuntimeError("endpoint soft data are absent")
                        hard_index = 0 if aliases == "03" else 4
                        value = vector_invariant(
                            endpoint_right[hard_index], soft_right
                        )
                        scale = max(
                            1.0,
                            abs(endpoint_right[hard_index, 0])
                            * abs(soft_right[0]),
                        )
                rows.append(
                    {
                        "component_id": component["component_id"],
                        "family": component["family"],
                        "owner_summand": owner,
                        "reciprocal_member": reciprocal_member,
                        "source_label": label,
                        "surface_id": surface_id,
                        "channel_aliases": aliases,
                        "channel_value_real": value.real,
                        "channel_value_imaginary": value.imag,
                        "channel_value_magnitude": abs(value),
                        "relative_zero_residual": abs(value) / scale,
                        "global_root_spread": geometry[
                            "global_root_spread"
                        ],
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return rows


def direct_surface_definitions() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "surface_id": "direct:shared:s12",
            "summand": "direct_five_point",
            "side": "shared",
            "channel_aliases": "s12",
            "equation": "D12=4(1-e)",
            "zero_set": "e=1 phase-space endpoint",
            "surface_class": "endpoint_internal_collinear",
            "maximum_pole_order": 1,
            "fixed_nonzero": False,
        },
        {
            "surface_id": "direct:shared:s13",
            "summand": "direct_five_point",
            "side": "shared",
            "channel_aliases": "s13",
            "equation": "D13=2 e (1-C)",
            "zero_set": "C=+1 or e=0",
            "surface_class": "hard_soft_collinear",
            "maximum_pole_order": 1,
            "fixed_nonzero": False,
        },
        {
            "surface_id": "direct:shared:s23",
            "summand": "direct_five_point",
            "side": "shared",
            "channel_aliases": "s23",
            "equation": "D23=2 e (1+C)",
            "zero_set": "C=-1 or e=0",
            "surface_class": "hard_soft_collinear",
            "maximum_pole_order": 1,
            "fixed_nonzero": False,
        },
        {
            "surface_id": "direct:shared:s04",
            "summand": "direct_five_point",
            "side": "shared",
            "channel_aliases": "s04=s123",
            "equation": "D04=4",
            "zero_set": "none in normalized cut kinematics",
            "surface_class": "fixed_cut_invariant",
            "maximum_pole_order": 0,
            "fixed_nonzero": True,
        },
    ]
    for side in ("L", "R"):
        for internal in (1, 2, 3):
            if side == "L":
                plus_equation = f"D0{internal}=-2 E{internal}(1-h{internal})"
                minus_equation = f"D{internal}4=-2 E{internal}(1+h{internal})"
                plus_zero = f"h{internal}=+1"
                minus_zero = f"h{internal}=-1"
            else:
                plus_equation = (
                    f"D0{internal}=-2 E{internal}(1-o.n{internal})"
                )
                minus_equation = (
                    f"D{internal}4=-2 E{internal}(1+o.n{internal})"
                )
                plus_zero = f"o.n{internal}=+1"
                minus_zero = f"o.n{internal}=-1"
            rows.extend(
                [
                    {
                        "surface_id": f"direct:{side}:s0{internal}",
                        "summand": "direct_five_point",
                        "side": side,
                        "channel_aliases": f"s0{internal}",
                        "equation": plus_equation,
                        "zero_set": plus_zero,
                        "surface_class": "scalar_graviton_factorization",
                        "maximum_pole_order": 1,
                        "fixed_nonzero": False,
                    },
                    {
                        "surface_id": f"direct:{side}:s{internal}4",
                        "summand": "direct_five_point",
                        "side": side,
                        "channel_aliases": f"s{internal}4",
                        "equation": minus_equation,
                        "zero_set": minus_zero,
                        "surface_class": "scalar_graviton_factorization",
                        "maximum_pole_order": 1,
                        "fixed_nonzero": False,
                    },
                ]
            )
    return rows


def endpoint_surface_definitions() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "surface_id": "endpoint:shared:soft:s13",
            "summand": "endpoint_subtraction",
            "side": "shared",
            "channel_aliases": "s13",
            "equation": "D13=2(1-d.n_s)",
            "zero_set": "d.n_s=+1",
            "surface_class": "soft_factor_hard_leg",
            "maximum_pole_order": 1,
            "fixed_nonzero": False,
        },
        {
            "surface_id": "endpoint:shared:soft:s23",
            "summand": "endpoint_subtraction",
            "side": "shared",
            "channel_aliases": "s23",
            "equation": "D23=2(1+d.n_s)",
            "zero_set": "d.n_s=-1",
            "surface_class": "soft_factor_hard_leg",
            "maximum_pole_order": 1,
            "fixed_nonzero": False,
        },
        {
            "surface_id": "endpoint:shared:hard:s12=s04",
            "summand": "endpoint_subtraction",
            "side": "shared",
            "channel_aliases": "s12=s04",
            "equation": "D12=D04=4",
            "zero_set": "none in normalized endpoint kinematics",
            "surface_class": "fixed_cut_invariant",
            "maximum_pole_order": 0,
            "fixed_nonzero": True,
        },
    ]
    for side in ("L", "R"):
        if side == "L":
            hard_plus = "D01=D24=-2(1-d_z)"
            hard_minus = "D02=D14=-2(1+d_z)"
            soft_plus = "D03=-2(1-n_s,z)"
            soft_minus = "D34=-2(1+n_s,z)"
            hard_plus_zero = "d_z=+1"
            hard_minus_zero = "d_z=-1"
            soft_plus_zero = "n_s,z=+1"
            soft_minus_zero = "n_s,z=-1"
        else:
            hard_plus = "D01=D24=-2(1-o.d)"
            hard_minus = "D02=D14=-2(1+o.d)"
            soft_plus = "D03=-2(1-o.n_s)"
            soft_minus = "D34=-2(1+o.n_s)"
            hard_plus_zero = "o.d=+1"
            hard_minus_zero = "o.d=-1"
            soft_plus_zero = "o.n_s=+1"
            soft_minus_zero = "o.n_s=-1"
        rows.extend(
            [
                {
                    "surface_id": f"endpoint:{side}:hard:s01=s24",
                    "summand": "endpoint_subtraction",
                    "side": side,
                    "channel_aliases": "s01=s24",
                    "equation": hard_plus,
                    "zero_set": hard_plus_zero,
                    "surface_class": "hard_four_point_factorization",
                    "maximum_pole_order": 1,
                    "fixed_nonzero": False,
                },
                {
                    "surface_id": f"endpoint:{side}:hard:s02=s14",
                    "summand": "endpoint_subtraction",
                    "side": side,
                    "channel_aliases": "s02=s14",
                    "equation": hard_minus,
                    "zero_set": hard_minus_zero,
                    "surface_class": "hard_four_point_factorization",
                    "maximum_pole_order": 1,
                    "fixed_nonzero": False,
                },
                {
                    "surface_id": f"endpoint:{side}:soft:s03",
                    "summand": "endpoint_subtraction",
                    "side": side,
                    "channel_aliases": "s03",
                    "equation": soft_plus,
                    "zero_set": soft_plus_zero,
                    "surface_class": "soft_factor_scalar_leg",
                    "maximum_pole_order": 1,
                    "fixed_nonzero": False,
                },
                {
                    "surface_id": f"endpoint:{side}:soft:s34",
                    "summand": "endpoint_subtraction",
                    "side": side,
                    "channel_aliases": "s34",
                    "equation": soft_minus,
                    "zero_set": soft_minus_zero,
                    "surface_class": "soft_factor_scalar_leg",
                    "maximum_pole_order": 1,
                    "fixed_nonzero": False,
                },
            ]
        )
    return rows


def surface_definitions() -> list[dict[str, Any]]:
    rows = direct_surface_definitions() + endpoint_surface_definitions()
    for row in rows:
        row.update(
            {
                "pole_order_basis": (
                    "tree factorization plus linear commuting collision residue"
                    if not row["fixed_nonzero"]
                    else "kinematic identity"
                ),
                "intersection_rule": (
                    "do not multiply codimension-one orders blindly; "
                    "audit the full local multivariate residue"
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def intended_surface_ids(
    component: dict[str, Any], owner: str
) -> set[str]:
    surfaces: set[str] = set()
    for label in component["representative_labels"]:
        if owner == "direct_five_point":
            surface_id, _ = direct_label_surface(label)
        else:
            surface_id, _, _ = endpoint_label_surface(label)
        surfaces.add(surface_id)
    return surfaces


def family_atlas(
    components: list[dict[str, Any]],
    owner_results: dict[str, dict[str, Any]],
    surfaces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for component in components:
        owner = owner_results[component["component_id"]]["measured_owner"]
        intended = intended_surface_ids(component, owner)
        owner_surfaces = [
            surface for surface in surfaces if surface["summand"] == owner
        ]
        for surface in owner_surfaces:
            if bool(surface["fixed_nonzero"]):
                status = "KINEMATICALLY_FIXED_NONZERO"
                subtraction_required = False
            elif surface["surface_id"] in intended:
                status = "CONSUMED_BY_LOCAL_DOUBLE_COLLISION_RESIDUE"
                subtraction_required = False
            else:
                status = "ENUMERATE_ROOT_AND_SUBTRACT_IF_DOMAIN_INTERSECTS"
                subtraction_required = True
            rows.append(
                {
                    "component_id": component["component_id"],
                    "family_id": component["family_id"],
                    "family": component["family"],
                    "owner_summand": owner,
                    "surface_id": surface["surface_id"],
                    "side": surface["side"],
                    "channel_aliases": surface["channel_aliases"],
                    "surface_class": surface["surface_class"],
                    "equation": surface["equation"],
                    "zero_set": surface["zero_set"],
                    "maximum_codimension_one_pole_order": surface[
                        "maximum_pole_order"
                    ],
                    "atlas_status": status,
                    "analytic_subtraction_required_if_intersected": (
                        subtraction_required
                    ),
                    "root_finding_contract": (
                        "solve D(q)=0 on inherited Feynman sheet; verify "
                        "winding; compute R=lim D*T/Dprime; integrate the "
                        "matched causal logarithm"
                        if subtraction_required
                        else "not applicable"
                    ),
                    "intersection_rule": surface["intersection_rule"],
                    "source_topology": component["source_topology"],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def add_formula_row(
    rows: list[dict[str, Any]],
    sample_id: str,
    summand: str,
    side: str,
    channel: str,
    actual: complex,
    predicted: complex,
) -> None:
    scale = max(abs(actual), abs(predicted), 1.0)
    rows.append(
        {
            "sample_id": sample_id,
            "summand": summand,
            "side": side,
            "channel": channel,
            "actual_real": actual.real,
            "actual_imaginary": actual.imag,
            "predicted_real": predicted.real,
            "predicted_imaginary": predicted.imag,
            "relative_residual": abs(actual - predicted) / scale,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )


def channel_formula_witnesses() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    samples = (
        (0.11, -0.62, 0.41, 0.37, 0.19),
        (0.37, 0.23, -0.31, 1.13, 0.71),
        (0.73, 0.51, 0.66, 2.07, 1.47),
        (0.89, -0.18, -0.77, 2.61, 2.33),
    )
    target = complex(-9.0, 0.04)
    for sample_index, (
        soft_energy,
        soft_cosine,
        decay_cosine,
        relative_phase,
        global_phase,
    ) in enumerate(samples, start=1):
        sample_id = f"CFW{sample_index:02d}"
        relative_circle = cmath.exp(1.0j * relative_phase)
        global_circle = cmath.exp(1.0j * global_phase)
        soft_direction, decay_direction, internal = (
            M5232.M5028.event_geometry(
                soft_energy,
                complex(soft_cosine),
                complex(decay_cosine),
                relative_circle,
            )
        )
        rotated = M5024.rotate_internal(internal, global_circle)
        left, right = M5017.cut_momenta(rotated, target, 1.0)
        relative_cosine = complex(
            np.dot(soft_direction, decay_direction)
        )
        internal_predictions = {
            (1, 2): complex(4.0 * (1.0 - soft_energy)),
            (1, 3): complex(
                2.0 * soft_energy * (1.0 - relative_cosine)
            ),
            (2, 3): complex(
                2.0 * soft_energy * (1.0 + relative_cosine)
            ),
        }
        for pair, predicted in internal_predictions.items():
            add_formula_row(
                rows,
                sample_id,
                "direct_five_point",
                "shared_left",
                f"s{pair[0]}{pair[1]}",
                pair_invariant(left, pair[0], pair[1]),
                predicted,
            )
            add_formula_row(
                rows,
                sample_id,
                "direct_five_point",
                "shared_right",
                f"s{pair[0]}{pair[1]}",
                pair_invariant(right, pair[0], pair[1]),
                predicted,
            )
        for side, momenta in (("L", left), ("R", right)):
            outgoing_direction = (
                momenta[0, 1:] / momenta[0, 0]
                if side == "R"
                else None
            )
            for internal_index in (1, 2, 3):
                energy = complex(rotated[internal_index - 1, 0])
                direction = (
                    rotated[internal_index - 1, 1:] / energy
                )
                if side == "L":
                    predicted_plus = -2.0 * energy * (
                        1.0 - direction[2]
                    )
                    predicted_minus = -2.0 * energy * (
                        1.0 + direction[2]
                    )
                else:
                    dot = complex(np.dot(outgoing_direction, direction))
                    predicted_plus = -2.0 * energy * (1.0 - dot)
                    predicted_minus = -2.0 * energy * (1.0 + dot)
                add_formula_row(
                    rows,
                    sample_id,
                    "direct_five_point",
                    side,
                    f"s0{internal_index}",
                    pair_invariant(momenta, 0, internal_index),
                    complex(predicted_plus),
                )
                add_formula_row(
                    rows,
                    sample_id,
                    "direct_five_point",
                    side,
                    f"s{internal_index}4",
                    pair_invariant(momenta, internal_index, 4),
                    complex(predicted_minus),
                )
            add_formula_row(
                rows,
                sample_id,
                "direct_five_point",
                side,
                "s04",
                pair_invariant(momenta, 0, 4),
                4.0 + 0.0j,
            )

        soft_rotated = M5022.rotate_vector(
            soft_direction, global_circle
        )
        decay_rotated = M5022.rotate_vector(
            decay_direction, global_circle
        )
        endpoint_internal = np.zeros((3, 4), dtype=np.complex128)
        endpoint_internal[0] = np.concatenate(([1.0], decay_rotated))
        endpoint_internal[1] = np.concatenate(([1.0], -decay_rotated))
        endpoint_left, endpoint_right = M5017.cut_momenta(
            endpoint_internal, target, 1.0
        )
        endpoint_soft_left = np.concatenate(
            ([1.0], soft_rotated)
        ).astype(np.complex128)
        endpoint_soft_right = -endpoint_soft_left
        endpoint_relative_cosine = complex(
            np.dot(soft_rotated, decay_rotated)
        )
        for side, momenta, soft in (
            ("L", endpoint_left, endpoint_soft_left),
            ("R", endpoint_right, endpoint_soft_right),
        ):
            if side == "L":
                hard_plus = -2.0 * (1.0 - decay_rotated[2])
                hard_minus = -2.0 * (1.0 + decay_rotated[2])
                soft_plus = -2.0 * (1.0 - soft_rotated[2])
                soft_minus = -2.0 * (1.0 + soft_rotated[2])
            else:
                outgoing_direction = momenta[0, 1:] / momenta[0, 0]
                hard_dot = complex(
                    np.dot(outgoing_direction, decay_rotated)
                )
                soft_dot = complex(
                    np.dot(outgoing_direction, soft_rotated)
                )
                hard_plus = -2.0 * (1.0 - hard_dot)
                hard_minus = -2.0 * (1.0 + hard_dot)
                soft_plus = -2.0 * (1.0 - soft_dot)
                soft_minus = -2.0 * (1.0 + soft_dot)
            for channel, actual, predicted in (
                ("s01=s24", pair_invariant(momenta, 0, 1), hard_plus),
                ("s02=s14", pair_invariant(momenta, 0, 2), hard_minus),
                ("s03", vector_invariant(momenta[0], soft), soft_plus),
                ("s34", vector_invariant(momenta[4], soft), soft_minus),
                (
                    "s13",
                    vector_invariant(momenta[1], soft),
                    2.0 * (1.0 - endpoint_relative_cosine),
                ),
                (
                    "s23",
                    vector_invariant(momenta[2], soft),
                    2.0 * (1.0 + endpoint_relative_cosine),
                ),
                ("s12=s04", pair_invariant(momenta, 1, 2), 4.0),
            ):
                add_formula_row(
                    rows,
                    sample_id,
                    "endpoint_subtraction",
                    side,
                    channel,
                    complex(actual),
                    complex(predicted),
                )
    return rows


def normalize_direct_channel_label(label: str) -> set[str]:
    final = label.split(":")[-1]
    triple = re.fullmatch(r"s_g([123])g([123])g([123])", final)
    if triple is not None:
        return {"04"}
    scalar_left = re.fullmatch(r"s_P0g([123])", final)
    if scalar_left is not None:
        return {f"0{scalar_left.group(1)}"}
    scalar_right = re.fullmatch(r"s_g([123])P4", final)
    if scalar_right is not None:
        return {f"{scalar_right.group(1)}4"}
    internal = re.fullmatch(r"s_g([123])g([123])", final)
    if internal is not None:
        return {"".join(sorted(internal.groups()))}
    return set()


def normalize_endpoint_channel_label(label: str) -> set[str]:
    final = label.split(":")[-1]
    soft = re.fullmatch(r"kdotp([0124])", final)
    if soft is not None:
        return {"".join(sorted(("3", soft.group(1))))}
    hard = normalize_direct_channel_label(label)
    expanded: set[str] = set()
    for channel in hard:
        if channel == "01":
            expanded.update(("01", "24"))
        elif channel == "02":
            expanded.update(("02", "14"))
        elif channel == "12":
            expanded.update(("12", "04"))
        else:
            expanded.add(channel)
    return expanded


def implemented_channel_orbits() -> dict[str, Any]:
    soft_energy = 0.37
    soft_cosine = 0.23
    decay_cosine = -0.31
    relative_circle = cmath.exp(0.71j)
    soft_direction, decay_direction, internal = (
        M5232.M5028.event_geometry(
            soft_energy,
            complex(soft_cosine),
            complex(decay_cosine),
            relative_circle,
        )
    )
    target = complex(-9.0, 0.04)
    global_circle = cmath.exp(0.37j)
    direct_labels = M5024.finite_channels(
        internal, target, global_circle
    )
    direct_orbit: set[str] = set()
    for label in direct_labels:
        direct_orbit.update(normalize_direct_channel_label(label))
    endpoint_labels = M5024.endpoint_channels(
        soft_direction,
        decay_direction,
        target,
        global_circle,
    )
    endpoint_orbit: set[str] = set()
    for label in endpoint_labels:
        endpoint_orbit.update(normalize_endpoint_channel_label(label))
    expected = {
        "01",
        "02",
        "03",
        "04",
        "12",
        "13",
        "14",
        "23",
        "24",
        "34",
    }
    return {
        "expected_pair_channel_orbit": sorted(expected),
        "direct_implemented_pair_channel_orbit": sorted(direct_orbit),
        "endpoint_implemented_pair_channel_orbit_with_complements": sorted(
            endpoint_orbit
        ),
        "direct_orbit_complete": direct_orbit == expected,
        "endpoint_orbit_complete": endpoint_orbit == expected,
        "direct_raw_channel_label_count": len(direct_labels),
        "endpoint_raw_channel_label_count": len(endpoint_labels),
    }


def internal_collinear_channel(
    case: dict[str, Any],
    event: dict[str, Any],
    target: complex,
    coordinate: complex,
) -> complex:
    soft_energy, soft_cosine, decay_cosine = M5232.varied_components(
        case, event, coordinate
    )
    rationals = M5232.M5029.root_rationals(
        soft_energy, soft_cosine, decay_cosine, target
    )
    first_label, second_label = case["representative_pair"]
    relative_root = M5232.coalesced_single_root(
        M5232.M5029.collision_roots(
            rationals[first_label], rationals[second_label]
        )
    )
    first_root, _ = M5231.rational_value_and_derivative(
        rationals[first_label], relative_root
    )
    second_root, _ = M5231.rational_value_and_derivative(
        rationals[second_label], relative_root
    )
    global_root = 0.5 * (first_root + second_root)
    _, _, internal = M5232.M5028.event_geometry(
        soft_energy, soft_cosine, decay_cosine, relative_root
    )
    rotated = M5024.rotate_internal(internal, global_root)
    left, _ = M5017.cut_momenta(rotated, target, 1.0)
    return pair_invariant(left, 1, 3)


def internal_collinear_scaling_witness() -> tuple[
    list[dict[str, Any]], dict[str, Any]
]:
    case = M5232.source_cases()[0]
    event = M5232.event_for_case(case)
    topology = M5232.topology_for_case(case, "E020")
    target = M5231.complex_value(topology["target_cosine"])
    center = -0.32437
    derivative = 0.0j
    for _ in range(30):
        step = 1.0e-6
        plus = internal_collinear_channel(
            case, event, target, center + step
        )
        minus = internal_collinear_channel(
            case, event, target, center - step
        )
        derivative = (plus - minus) / (2.0 * step)
        value = internal_collinear_channel(
            case, event, target, center
        )
        correction = value.real / derivative.real
        center -= correction
        if abs(correction) < 1.0e-13:
            break
    value = internal_collinear_channel(case, event, target, center)
    pole = complex(center) - value / derivative
    offsets = (
        -5.0e-3,
        -2.5e-3,
        -1.0e-3,
        -5.0e-4,
        5.0e-4,
        1.0e-3,
        2.5e-3,
        5.0e-3,
    )
    rows: list[dict[str, Any]] = []
    for offset in offsets:
        coordinate = center + offset
        contribution = M5232.family_contribution(
            case, event, topology, coordinate
        )[0]
        channel = internal_collinear_channel(
            case, event, target, coordinate
        )
        rows.append(
            {
                "case_id": "fresh_g1_g3_shared_s13",
                "family": case["family"],
                "epsilon_id": "E020",
                "outer_coordinate": case["outer_coordinate"],
                "center": center,
                "complex_pole_real": pole.real,
                "complex_pole_imaginary": pole.imag,
                "offset": offset,
                "coordinate": coordinate,
                "channel_real": channel.real,
                "channel_imaginary": channel.imag,
                "contribution_magnitude": abs(contribution),
                "channel_times_contribution_magnitude": abs(
                    channel * contribution
                ),
                "channel_squared_times_contribution_magnitude": abs(
                    channel * channel * contribution
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    fits: dict[str, Any] = {}
    for side_name, sign in (("negative", -1.0), ("positive", 1.0)):
        selected = [
            row for row in rows if float(row["offset"]) * sign > 0.0
        ]
        slope, intercept = np.polyfit(
            np.log([abs(float(row["offset"])) for row in selected]),
            np.log(
                [float(row["contribution_magnitude"]) for row in selected]
            ),
            1,
        )
        numerator = np.asarray(
            [
                float(row["channel_times_contribution_magnitude"])
                for row in selected
            ]
        )
        fits[side_name] = {
            "log_log_slope": float(slope),
            "log_log_intercept": float(intercept),
            "channel_times_contribution_relative_spread": float(
                np.std(numerator) / np.mean(numerator)
            ),
        }
    near_second = np.mean(
        [
            float(row["channel_squared_times_contribution_magnitude"])
            for row in rows
            if abs(float(row["offset"])) == 5.0e-4
        ]
    )
    far_second = np.mean(
        [
            float(row["channel_squared_times_contribution_magnitude"])
            for row in rows
            if abs(float(row["offset"])) == 5.0e-3
        ]
    )
    pole_event = dict(event)
    pole_event[case["outer_coordinate"]] = center
    topology_audit = M5232.target_pair_track(
        pole_event,
        target,
        [case["reciprocal_pair"], case["representative_pair"]],
        TOPOLOGY_STEPS,
    )
    winding_rows = {
        row["pair"][0].rsplit("_", 1)[-1]: row
        for row in topology_audit["pair_rows"]
    }
    summary = {
        "case_id": "fresh_g1_g3_shared_s13",
        "family": case["family"],
        "channel": "shared s13",
        "outer_coordinate": case["outer_coordinate"],
        "real_axis_center": center,
        "channel_at_center": complex_row(value),
        "channel_derivative": complex_row(derivative),
        "complex_pole": complex_row(pole),
        "negative_side": fits["negative"],
        "positive_side": fits["positive"],
        "near_to_far_D2T_ratio": float(near_second / far_second),
        "topology_steps": TOPOLOGY_STEPS,
        "maximum_pair_projective_step": topology_audit[
            "maximum_pair_projective_step"
        ],
        "maximum_reciprocal_product_residual": topology_audit[
            "maximum_reciprocal_product_residual"
        ],
        "u_winding": winding_rows["u"]["winding_sum"],
        "v_winding": winding_rows["v"]["winding_sum"],
        "expected_u_winding": case["expected_u_winding"],
        "expected_v_winding": case["expected_v_winding"],
    }
    return rows, summary


def validation_rows(
    family_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    collision_rows: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    surfaces: list[dict[str, Any]],
    atlas_rows: list[dict[str, Any]],
    channel_orbits: dict[str, Any],
    scaling: dict[str, Any],
    scalar_proof: dict[str, Any],
    graviton_proof: dict[str, Any],
) -> list[dict[str, Any]]:
    required = [
        SCRIPT_5024,
        SCRIPT_5127,
        SCRIPT_5138,
        SCRIPT_5231,
        SCRIPT_5232,
        FAMILY_SOURCE,
        SCALAR_GRAVITON_PROOF,
        GRAVITON_GRAVITON_PROOF,
        *[Path(row["source_topology"]) for row in component_rows],
    ]
    maximum_collision_residual = max(
        float(row["relative_zero_residual"]) for row in collision_rows
    )
    maximum_formula_residual = max(
        float(row["relative_residual"]) for row in formula_rows
    )
    owner_pass = all(
        bool(row["owner_matches_prediction"])
        and float(row["owner_fraction"]) >= OWNER_FRACTION_MINIMUM
        and float(row["summand_split_relative_closure_residual"])
        < 1.0e-12
        for row in component_rows
    )
    scaling_pass = (
        all(
            abs(float(scaling[side]["log_log_slope"]) + 1.0)
            <= SCALING_SLOPE_TOLERANCE
            and float(
                scaling[side][
                    "channel_times_contribution_relative_spread"
                ]
            )
            <= REGULAR_NUMERATOR_SPREAD_LIMIT
            for side in ("negative_side", "positive_side")
        )
        and float(scaling["near_to_far_D2T_ratio"]) < 0.2
        and int(scaling["u_winding"])
        == int(scaling["expected_u_winding"])
        and int(scaling["v_winding"])
        == int(scaling["expected_v_winding"])
        and float(scaling["maximum_pair_projective_step"])
        < PROJECTIVE_LIMIT
    )
    atlas_pass = all(
        int(row["maximum_codimension_one_pole_order"]) in (0, 1)
        and row["atlas_status"]
        in {
            "KINEMATICALLY_FIXED_NONZERO",
            "CONSUMED_BY_LOCAL_DOUBLE_COLLISION_RESIDUE",
            "ENUMERATE_ROOT_AND_SUBTRACT_IF_DOMAIN_INTERSECTS",
        }
        for row in atlas_rows
    )
    intended_count = sum(
        row["atlas_status"]
        == "CONSUMED_BY_LOCAL_DOUBLE_COLLISION_RESIDUE"
        for row in atlas_rows
    )
    formal_digest = tree_digest(FORMAL)
    checks = [
        (
            "required_source_paths_exist",
            all(path.exists() for path in required),
            f"{sum(path.exists() for path in required)}/{len(required)}",
        ),
        (
            "all_ten_nonzero_families_are_inventoried",
            len(family_rows) == 10
            and all(
                float(row["maximum_A00_family_magnitude"])
                > ACTIVE_FAMILY_FLOOR
                for row in family_rows
            ),
            f"families={len(family_rows)}",
        ),
        (
            "two_double_branch_families_expand_to_twelve_components",
            len(component_rows) == 12,
            f"components={len(component_rows)}",
        ),
        (
            "double_residue_summand_owner_is_measured_not_assumed",
            owner_pass,
            (
                f"minimum_owner_fraction="
                f"{min(float(row['owner_fraction']) for row in component_rows)}"
            ),
        ),
        (
            "source_labels_map_to_the_claimed_physical_channels",
            maximum_collision_residual
            <= CHANNEL_ZERO_RELATIVE_TOLERANCE,
            f"maximum_relative_zero_residual={maximum_collision_residual}",
        ),
        (
            "closed_form_channel_equations_match_cut_kinematics",
            maximum_formula_residual <= FORMULA_RELATIVE_TOLERANCE,
            f"maximum_relative_residual={maximum_formula_residual}",
        ),
        (
            "implemented_KLT_and_endpoint_channel_orbits_are_complete",
            bool(channel_orbits["direct_orbit_complete"])
            and bool(channel_orbits["endpoint_orbit_complete"]),
            json.dumps(channel_orbits, separators=(",", ":")),
        ),
        (
            "scalar_graviton_tree_poles_are_at_most_simple",
            bool(
                scalar_proof[
                    "simple_pole_order_proved_for_implemented_integrand"
                ]
            )
            and bool(
                scalar_proof[
                    "double_pole_excluded_for_implemented_integrand"
                ]
            )
            and int(
                scalar_proof["maximum_scalar_KLT_tree_pole_order"]
            )
            == 1,
            str(
                scalar_proof["maximum_scalar_KLT_tree_pole_order"]
            ),
        ),
        (
            "graviton_graviton_orbit_has_simple_active_witness",
            bool(graviton_proof["gate_accepted"])
            and bool(graviton_proof["all_charts_accepted"])
            and scaling_pass,
            json.dumps(
                {
                    "negative_slope": scaling["negative_side"][
                        "log_log_slope"
                    ],
                    "positive_slope": scaling["positive_side"][
                        "log_log_slope"
                    ],
                    "u_winding": scaling["u_winding"],
                    "v_winding": scaling["v_winding"],
                },
                separators=(",", ":"),
            ),
        ),
        (
            "every_owner_surface_is_classified_with_no_higher_pole_smuggling",
            atlas_pass and intended_count == 24,
            (
                f"atlas_rows={len(atlas_rows)};"
                f"consumed_collision_surfaces={intended_count}"
            ),
        ),
        (
            "fixed_s04_and_endpoint_hard_invariants_remain_nonzero",
            all(
                int(row["maximum_pole_order"]) == 0
                for row in surfaces
                if bool(row["fixed_nonzero"])
            ),
            "D04=4; endpoint D12=D04=4",
        ),
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "all_claim_flags_remain_false",
            True,
            "numeric UV, local GR and full MTS claims remain false",
        ),
    ]
    return [
        {
            "check": check,
            "passed": bool(passed),
            "detail": detail,
            "checkpoint_marker": MARKER,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for check, passed, detail in checks
    ]


def main() -> None:
    families = active_family_inventory()
    components = component_inventory(families)
    serialized_components, owner_results = serialize_components(components)
    collisions = collision_channel_witnesses(components, owner_results)
    formulas = channel_formula_witnesses()
    surfaces = surface_definitions()
    atlas = family_atlas(components, owner_results, surfaces)
    channel_orbits = implemented_channel_orbits()
    scaling_rows, scaling = internal_collinear_scaling_witness()
    scalar_proof = read_json(SCALAR_GRAVITON_PROOF)
    graviton_proof = read_json(GRAVITON_GRAVITON_PROOF)
    validations = validation_rows(
        families,
        serialized_components,
        collisions,
        formulas,
        surfaces,
        atlas,
        channel_orbits,
        scaling,
        scalar_proof,
        graviton_proof,
    )
    validation_all_passed = all(bool(row["passed"]) for row in validations)
    decision = (
        "ADOPT_COMPLETE_PHYSICAL_CHANNEL_ATLAS_AND_BUILD_DYNAMIC_ROOT_ENUMERATOR"
        if validation_all_passed
        else "RETAIN_BLOCK_AND_REPAIR_CHANNEL_ATLAS"
    )
    owner_counts: defaultdict[str, int] = defaultdict(int)
    for row in serialized_components:
        owner_counts[str(row["measured_owner"])] += 1
    candidate_count = sum(
        row["atlas_status"]
        == "ENUMERATE_ROOT_AND_SUBTRACT_IF_DOMAIN_INTERSECTS"
        for row in atlas
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": decision,
        "active_family_count": len(families),
        "active_reciprocal_component_count": len(components),
        "summand_owner_counts": dict(owner_counts),
        "minimum_summand_owner_fraction": min(
            float(row["owner_fraction"]) for row in serialized_components
        ),
        "maximum_collision_channel_relative_zero_residual": max(
            float(row["relative_zero_residual"]) for row in collisions
        ),
        "maximum_closed_form_channel_equation_relative_residual": max(
            float(row["relative_residual"]) for row in formulas
        ),
        "implemented_channel_orbits": channel_orbits,
        "pole_order_theorem": {
            "local_tree_factorization": (
                "M5 -> sum_h M_L M_R / D + O(1), so every isolated "
                "physical factorization divisor D=0 is at most simple"
            ),
            "KLT_representation_guard": (
                "apparent Parke-Taylor double denominators cancel through "
                "the momentum kernel and permutation sum; 5138 proves the "
                "scalar-graviton representative and 5127 plus the fresh "
                "5234 witness checks the graviton-graviton representative"
            ),
            "commuting_collision_residue_lemma": (
                "if F(z,q)=C/[A(z,q)B(z,q)D(q)] with D transverse to the "
                "A=B=0 collision, then Res_z^(A,B) F=C_eff(q)/D(q); the "
                "linear local residue cannot raise the D pole order"
            ),
            "intersection_guard": (
                "when another divisor shares the collision stratum, use a "
                "full multivariate residue audit; never infer a product pole "
                "by multiplying one-dimensional orders"
            ),
            "maximum_isolated_codimension_one_pole_order": 1,
        },
        "exact_channel_equations": {
            "direct_internal": {
                "s12": "4(1-e)",
                "s13": "2 e (1-C)",
                "s23": "2 e (1+C)",
                "s04": "4",
            },
            "direct_left_scalar": (
                "s0i=-2 E_i(1-h_i), si4=-2 E_i(1+h_i)"
            ),
            "direct_right_scalar": (
                "s0i=-2 E_i(1-o.n_i), si4=-2 E_i(1+o.n_i)"
            ),
            "endpoint_hard": (
                "s01=s24, s02=s14, s12=s04=4"
            ),
            "endpoint_soft": (
                "s13=2(1-d.n_s), s23=2(1+d.n_s), with left/right "
                "scalar-soft channels obtained by beam/outgoing alignment"
            ),
        },
        "internal_collinear_simple_pole_witness": scaling,
        "surface_definition_count": len(surfaces),
        "family_atlas_row_count": len(atlas),
        "candidate_root_surface_count": candidate_count,
        "validation_all_passed": validation_all_passed,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        "next_target": (
            "implement the dynamic family-component root enumerator over "
            "every atlas surface, validate the inherited winding at each "
            "interior or endpoint root, and run a completely pole-subtracted "
            "small A00 pilot"
        ),
        "source_paths": [
            str(SCRIPT_5024),
            str(SCRIPT_5127),
            str(SCRIPT_5138),
            str(SCRIPT_5231),
            str(SCRIPT_5232),
            str(FAMILY_SOURCE),
            str(SCALAR_GRAVITON_PROOF),
            str(GRAVITON_GRAVITON_PROOF),
        ],
    }
    write_csv(FAMILY_ROWS, families)
    write_csv(COMPONENT_ROWS, serialized_components)
    write_csv(COLLISION_ROWS, collisions)
    write_csv(FORMULA_ROWS, formulas)
    write_csv(SURFACE_ROWS, surfaces)
    write_csv(ATLAS_ROWS, atlas)
    write_csv(SCALING_ROWS, scaling_rows)
    write_csv(VALIDATION, validations)
    atomic_json(RESULT, result)

    owner_lines = "\n".join(
        (
            f"- `{row['component_id']}` `{row['family']}`: "
            f"`{row['measured_owner']}` at owner fraction "
            f"`{float(row['owner_fraction']):.12g}`."
        )
        for row in serialized_components
    )
    document = f"""# 5234 - Complete active-family physical-channel and pole-order atlas

## Decision

`{decision}`.

This checkpoint replaces the phrase “the A00 tails have more missing poles”
with a finite, source-backed atlas.  The 5231 pool contains exactly ten
nonzero canonical families and twelve reciprocal components.  The two extra
components are the second collision branches of the `g1/g2` families.

## The summand owner is now measured

The finite-plus integrand is the difference of a direct five-point KLT term
and its endpoint subtraction.  Their local double coefficients were separated
before taking the family residue:

```text
C_total = lim_(delta->0) delta^2 (T_direct - T_endpoint) / e
        = C_direct + C_endpoint.
```

The result is not an assumption:

{owner_lines}

All direct/direct families are direct-five-point owned.  Every
`g3/subtraction:decay` family is endpoint owned because `direct:g3` is the
same direction as the endpoint soft leg, while `subtraction:decay` supplies
the hard four-point factor.  The minimum measured owner fraction is
`{result['minimum_summand_owner_fraction']:.12g}`.

## Exact channel equations

Write `e=E_3` and `C=n_s.d` for the soft energy and soft/decay relative
cosine.  Momentum conservation gives the three shared internal invariants
without fitting:

```text
s12 = 4(1-e),
s13 = 2 e (1-C),
s23 = 2 e (1+C).
```

For either hard or soft internal leg `i`, the scalar channels are

```text
left:  s0i=-2 E_i(1-h_i),      si4=-2 E_i(1+h_i),
right: s0i=-2 E_i(1-o.n_i),    si4=-2 E_i(1+o.n_i).
```

The scalar-pair/complement channel is fixed: `s04=s123=4`.  In the endpoint
subtraction the hard aliases are `s01=s24`, `s02=s14`, and `s12=s04=4`;
the soft-factor channels are `s03,s13,s23,s34`.  The implementation exposes
the full ten-pair orbit after these complement aliases are expanded.

Across `{len(formulas)}` independent direct and endpoint checks, the largest
relative equation residual is
`{result['maximum_closed_form_channel_equation_relative_residual']:.9g}`.
Every source label in every reciprocal component also lands on its stated
right-cut physical channel; the largest relative zero residual is
`{result['maximum_collision_channel_relative_zero_residual']:.9g}`.

## Pole-order theorem

An isolated tree factorization divisor has

```text
M_5 = sum_h M_L M_R / D + O(1).
```

It is therefore at most simple.  Checkpoint 5138 proves this explicitly for
one scalar-graviton KLT representative, including cancellation of the apparent
Parke-Taylor double denominator.  Graviton permutation and scalar crossing
cover the six scalar-graviton channels.  Checkpoint 5127 supplies the existing
full-amplitude graviton-graviton witness; the fresh active-family `s13`
witness here has slopes
`{scaling['negative_side']['log_log_slope']:.9g}` and
`{scaling['positive_side']['log_log_slope']:.9g}`, regular `D*T`, vanishing
`D^2*T`, and retained windings
`({scaling['u_winding']},{scaling['v_winding']})`.

Taking the local collision residue is linear.  If the already-consumed
collision factors are `A(z,q)B(z,q)` and a third transverse channel is
`D(q)`, then

```text
Res_z^[A,B] C/[A B D] = C_eff(q)/D(q).
```

The collision residue cannot raise the third-channel order.  At genuine
intersections the code must inspect the full multivariate residue; the atlas
explicitly forbids multiplying one-dimensional pole orders by hand.

## What is and is not closed

All `{len(atlas)}` owner-surface rows are classified as:

1. already consumed by the local double-collision residue;
2. fixed and nonzero; or
3. a simple candidate whose root must be enumerated and causally subtracted
   if it intersects the integration domain.

This is a complete structural pole atlas, not yet the completed A00 integral.
It does not establish the UV coefficient, local GR, or the full MTS theory.

## Next target

Build the dynamic root enumerator from these exact equations, retain only
roots on the inherited Feynman sheet with active winding, subtract each
certified simple pole analytically, and run a small all-channel A00 pilot.
"""
    atomic_text(DOCUMENT, document)
    print(json.dumps(result, indent=2, sort_keys=True))
    if not validation_all_passed:
        raise RuntimeError("5234 complete physical-channel atlas failed")


if __name__ == "__main__":
    main()
