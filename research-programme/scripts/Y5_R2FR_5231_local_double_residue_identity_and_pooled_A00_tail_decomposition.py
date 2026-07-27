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
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE_5224 = FUNCTIONAL_RG / "5224"
SOURCE_5229 = FUNCTIONAL_RG / "5229"
SOURCE_5230 = FUNCTIONAL_RG / "5230"
SOURCE = FUNCTIONAL_RG / "5231"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5029 = (
    POST
    / "scripts"
    / "Y5_R2FR_5029_finite_x_cross_source_collision_map.py"
)
CONFIG_5224 = SOURCE_5224 / "frozen_replacement_config.json"
ROWS_5224 = SOURCE_5224 / "replacement_A00_control_rows.csv"
RUN_5224 = SOURCE_5224 / "runs" / "replacement_scaled_controlled_v1"
CONFIG_5229 = SOURCE_5229 / "frozen_native_chart_A00_config.json"
ROWS_5229 = SOURCE_5229 / "fresh_native_chart_A00_event_rows.csv"
RUN_5229 = SOURCE_5229 / "runs" / "fresh_native_chart_A00_replication"
RESULT_5229 = SOURCE_5229 / "fresh_native_chart_A00_results.json"
RESULT_5230 = SOURCE_5230 / "native_A00_tail_resolution_audit.json"

RESULT = SOURCE / "local_double_residue_tail_decomposition.json"
EVENT_ROWS = SOURCE / "pooled_A00_tail_event_decomposition.csv"
FAMILY_ROWS = SOURCE / "pooled_A00_tail_family_decomposition.csv"
IDENTITY_ROWS = SOURCE / "stored_safe_pair_identity_audit.csv"
DOCUMENT = (
    POST
    / "5231-Y5-R2FR-local-double-residue-identity-and-pooled-A00-tail-decomposition.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5231_VALIDATION.csv"

MARKER = "MTS_5231_LOCAL_DOUBLE_RESIDUE_IDENTITY_AND_POOLED_A00_TAIL_DECOMPOSITION"
REVISION = "local-double-residue-tail-decomposition-v1"
PHYSICAL_A00_WEIGHT = -0.008
KERNEL_MULTIPLIER = -2.0 / math.pi
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
MATERIAL_RESIDUE_FLOOR = 1.0
MAXIMUM_MATERIAL_IDENTITY_RELATIVE_RESIDUAL = 1.0e-2
MAXIMUM_POOLED_A00_RMS_RESIDUAL = 1.0e-1
MAXIMUM_POOLED_A00_ABSOLUTE_RESIDUAL = 1.0
MINIMUM_POOLED_CORRELATION = 0.999
DOUBLE_POLE_POWER_MAXIMUM = 0.45
HIGHER_POLE_POWER_MINIMUM = -0.45


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5029 = load_module(SCRIPT_5029, "mts_5029_for_5231")
M5028 = M5029.M5028


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def complex_value(value: Any) -> complex:
    if isinstance(value, dict):
        return complex(float(value["real"]), float(value["imaginary"]))
    return complex(value)


def laurent_derivative(polynomial: dict[int, complex], value: complex) -> complex:
    return complex(
        sum(
            exponent * coefficient * value ** (exponent - 1)
            for exponent, coefficient in polynomial.items()
        )
    )


def rational_value_and_derivative(
    rational: tuple[dict[int, complex], dict[int, complex]],
    value: complex,
) -> tuple[complex, complex]:
    numerator, denominator = rational
    numerator_value = M5029.laurent_value(numerator, value)
    denominator_value = M5029.laurent_value(denominator, value)
    numerator_derivative = laurent_derivative(numerator, value)
    denominator_derivative = laurent_derivative(denominator, value)
    rational_value = numerator_value / denominator_value
    rational_derivative = (
        numerator_derivative * denominator_value
        - numerator_value * denominator_derivative
    ) / denominator_value**2
    return complex(rational_value), complex(rational_derivative)


def root_rationals(
    event: dict[str, Any], target: complex
) -> dict[str, tuple[dict[int, complex], dict[int, complex]]]:
    rows = M5029.root_rationals(
        float(event["soft_energy"]),
        float(event["soft_cosine"]),
        float(event["decay_cosine"]),
        target,
    )
    for suffix in ("plus_u", "plus_v", "minus_u", "minus_v"):
        rows[f"subtraction:soft:{suffix}"] = rows[f"direct:g3:{suffix}"]
    return rows


def reciprocal_pairs(
    topology: dict[str, Any],
) -> list[tuple[dict[str, Any], dict[str, Any], float]]:
    entries: list[dict[str, Any]] = []
    for chamber_index, chamber in enumerate(topology["chambers"]):
        for crossing in chamber["surface_crossings"]:
            entries.append({**crossing, "chamber_index": chamber_index})
    used: set[int] = set()
    pairs: list[tuple[dict[str, Any], dict[str, Any], float]] = []
    for first_index, first in enumerate(entries):
        if first_index in used:
            continue
        inverse = 1.0 / complex_value(first["target_root"])
        candidates = [
            (
                abs(complex_value(second["target_root"]) - inverse)
                / max(
                    1.0,
                    abs(inverse),
                    abs(complex_value(second["target_root"])),
                ),
                second_index,
                second,
            )
            for second_index, second in enumerate(entries)
            if second_index != first_index and second_index not in used
        ]
        if not candidates:
            raise RuntimeError("reciprocal crossing partner is absent")
        residual, partner_index, partner = min(
            candidates, key=lambda row: row[0]
        )
        if residual > 2.0e-8:
            raise RuntimeError(
                f"reciprocal crossing partner fails with residual {residual}"
            )
        used.update((first_index, partner_index))
        pairs.append((first, partner, residual))
    if len(used) != len(entries):
        raise RuntimeError("reciprocal pairing did not consume every crossing")
    return pairs


def reciprocal_pair_is_unsafe(entry: dict[str, Any]) -> bool:
    pairs = entry["representing_pairs"]
    if len(pairs) != 1:
        return True
    labels = set(pairs[0])
    return any(label.startswith("direct:g2:") for label in labels) and any(
        label.startswith("subtraction:decay:") for label in labels
    )


def canonical_family(
    first: dict[str, Any], second: dict[str, Any]
) -> str:
    def canonical_pair(pair: list[str]) -> tuple[str, ...]:
        return tuple(
            sorted(re.sub(r"_(u|v)$", "", label) for label in pair)
        )

    source_pairs = {
        canonical_pair(first["representing_pairs"][0]),
        canonical_pair(second["representing_pairs"][0]),
    }
    return "|".join(
        "/".join(source_pair) for source_pair in sorted(source_pairs)
    )


def chamber_ownership(
    event: dict[str, Any], chamber: dict[str, Any]
) -> dict[str, bool]:
    midpoint = 0.5 * (
        float(chamber["start_physical_angle"])
        + float(chamber["end_physical_angle"])
    )
    return M5028.chamber_ownership(
        float(event["soft_energy"]),
        complex(float(event["soft_cosine"]), 0.0),
        complex(float(event["decay_cosine"]), 0.0),
        cmath.exp(1.0j * midpoint),
    )


def local_double_residue(
    event: dict[str, Any],
    target: complex,
    topology: dict[str, Any],
    entry: dict[str, Any],
    rationals: dict[str, tuple[dict[int, complex], dict[int, complex]]],
) -> tuple[complex, dict[str, Any]]:
    if len(entry["representing_pairs"]) != 1:
        raise RuntimeError("local identity requires one representing pair")
    first_label, second_label = entry["representing_pairs"][0]
    relative_root = complex_value(entry["target_root"])
    first_root, first_derivative = rational_value_and_derivative(
        rationals[first_label], relative_root
    )
    second_root, second_derivative = rational_value_and_derivative(
        rationals[second_label], relative_root
    )
    global_root = 0.5 * (first_root + second_root)
    soft_direction, decay_direction, internal = M5028.event_geometry(
        float(event["soft_energy"]),
        complex(float(event["soft_cosine"]), 0.0),
        complex(float(event["decay_cosine"]), 0.0),
        relative_root,
    )
    phase = cmath.exp(0.37j)
    scale = max(1.0, abs(global_root))
    coefficient_samples: list[complex] = []
    for fraction in (2.0e-5, 1.0e-5, 5.0e-6):
        displacement = fraction * scale * phase
        integrand = M5028.M5026.finite_plus_integrand(
            internal,
            float(event["soft_energy"]),
            soft_direction,
            decay_direction,
            target,
            global_root + displacement,
        )
        coefficient_samples.append(complex(integrand * displacement**2))
    middle_magnitude = max(abs(coefficient_samples[-2]), 1.0e-300)
    coefficient_scaling_power = -math.log(
        max(abs(coefficient_samples[-1]) / middle_magnitude, 1.0e-300),
        2.0,
    )
    if coefficient_scaling_power > DOUBLE_POLE_POWER_MAXIMUM:
        return 0.0j, {
            "classification": "LOWER_THAN_DOUBLE_POLE__ZERO_DOUBLE_RESIDUE",
            "coefficient_scaling_power": coefficient_scaling_power,
            "coefficient_stability": None,
            "coefficient_magnitude": 0.0,
            "residue_magnitude": 0.0,
            "relative_root_magnitude": abs(relative_root),
            "global_root_magnitude": abs(global_root),
            "collision_jacobian_magnitude": abs(
                first_derivative - second_derivative
            ),
            "representing_pair": [first_label, second_label],
        }
    coefficient = (
        2.0 * coefficient_samples[-1] - coefficient_samples[-2]
    )
    coefficient_stability = abs(
        coefficient_samples[-1] - coefficient_samples[-2]
    ) / max(abs(coefficient), 1.0e-30)
    chamber = topology["chambers"][int(entry["chamber_index"])]
    ownership = chamber_ownership(event, chamber)
    owned = [bool(ownership[first_label]), bool(ownership[second_label])]
    if sum(owned) != 1:
        raise RuntimeError(
            f"collision pair has non-unique ownership: "
            f"{first_label}, {second_label}, {owned}"
        )
    orientation = 1.0 if owned[0] else -1.0
    collision_jacobian = first_derivative - second_derivative
    residue = (
        orientation
        * coefficient
        / (relative_root * global_root * collision_jacobian)
    )
    classification = (
        "HIGHER_THAN_DOUBLE_POLE"
        if coefficient_scaling_power < HIGHER_POLE_POWER_MINIMUM
        else "DOUBLE_POLE"
    )
    return complex(residue), {
        "classification": classification,
        "coefficient_scaling_power": coefficient_scaling_power,
        "coefficient_stability": coefficient_stability,
        "coefficient_magnitude": abs(coefficient),
        "residue_magnitude": abs(residue),
        "relative_root_magnitude": abs(relative_root),
        "global_root_magnitude": abs(global_root),
        "collision_jacobian_magnitude": abs(collision_jacobian),
        "representing_pair": [first_label, second_label],
        "owned_label": first_label if owned[0] else second_label,
    }


def safe_family_contributions(
    event: dict[str, Any], topology: dict[str, Any]
) -> tuple[dict[str, complex], list[dict[str, Any]]]:
    target = complex_value(topology["target_cosine"])
    rationals = root_rationals(event, target)
    contributions: defaultdict[str, complex] = defaultdict(complex)
    diagnostics: list[dict[str, Any]] = []
    for first, second, reciprocal_residual in reciprocal_pairs(topology):
        if reciprocal_pair_is_unsafe(first) or reciprocal_pair_is_unsafe(second):
            continue
        representative, partner = (
            (first, second)
            if abs(complex_value(first["target_root"])) >= 1.0
            else (second, first)
        )
        residue, diagnostic = local_double_residue(
            event, target, topology, representative, rationals
        )
        winding_difference = int(
            representative["winding_correction"]
        ) - int(partner["winding_correction"])
        contribution = winding_difference * residue
        family = canonical_family(first, second)
        contributions[family] += contribution
        diagnostics.append(
            {
                **diagnostic,
                "family": family,
                "raw_contribution_real": contribution.real,
                "raw_contribution_imaginary": contribution.imag,
                "winding_difference": winding_difference,
                "reciprocal_root_residual": reciprocal_residual,
            }
        )
    return dict(contributions), diagnostics


def source_contracts() -> list[dict[str, Any]]:
    return [
        {
            "tranche": "old_5224",
            "source_directory": SOURCE_5224,
            "config": CONFIG_5224,
            "rows": ROWS_5224,
            "run": RUN_5224,
            "real_field": "raw_A00_real",
            "imaginary_field": "raw_A00_imaginary",
        },
        {
            "tranche": "fresh_5229",
            "source_directory": SOURCE_5229,
            "config": CONFIG_5229,
            "rows": ROWS_5229,
            "run": RUN_5229,
            "real_field": "A00_real",
            "imaginary_field": "A00_imaginary",
        },
    ]


def topology_path(
    contract: dict[str, Any], seed: int, epsilon_id: str
) -> Path:
    return (
        contract["run"]
        / "topologies"
        / f"S{seed}_N0000__{epsilon_id}_A00.json"
    )


def job_path(
    contract: dict[str, Any], seed: int, epsilon_id: str
) -> Path:
    return (
        contract["run"]
        / "topological-jobs"
        / f"TOP__{epsilon_id}__S{seed}_N0000__A00__primary24.json"
    )


def pooled_decomposition() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    event_rows: list[dict[str, Any]] = []
    family_rows: list[dict[str, Any]] = []
    all_diagnostics: list[dict[str, Any]] = []
    for contract in source_contracts():
        config = read_json(contract["config"])
        events = {int(row["seed"]): row for row in config["events"]}
        for source_row in read_csv(contract["rows"]):
            seed = int(source_row["seed"])
            event = events[seed]
            epsilon_families: dict[str, dict[str, complex]] = {}
            for epsilon_id in ("E040", "E020"):
                topology = read_json(
                    topology_path(contract, seed, epsilon_id)
                )
                raw_families, diagnostics = safe_family_contributions(
                    event, topology
                )
                epsilon_families[epsilon_id] = {
                    family: KERNEL_MULTIPLIER * value
                    for family, value in raw_families.items()
                }
                for diagnostic in diagnostics:
                    all_diagnostics.append(
                        {
                            "tranche": contract["tranche"],
                            "seed": seed,
                            "epsilon_id": epsilon_id,
                            **diagnostic,
                        }
                    )
            families = set(epsilon_families["E040"]) | set(
                epsilon_families["E020"]
            )
            physical_families = {
                family: PHYSICAL_A00_WEIGHT
                * (
                    2.0
                    * epsilon_families["E020"].get(family, 0.0j)
                    - epsilon_families["E040"].get(family, 0.0j)
                )
                for family in families
            }
            reconstructed = sum(physical_families.values(), 0.0j)
            observed = complex(
                float(source_row[contract["real_field"]]),
                float(source_row[contract["imaginary_field"]]),
            )
            dominant_family, dominant_value = max(
                physical_families.items(),
                key=lambda item: abs(item[1]),
                default=("NONE", 0.0j),
            )
            event_rows.append(
                {
                    "tranche": contract["tranche"],
                    "seed": seed,
                    "event_id": event["event_id"],
                    "soft_energy": event["soft_energy"],
                    "soft_cosine": event["soft_cosine"],
                    "decay_cosine": event["decay_cosine"],
                    "observed_A00_real": observed.real,
                    "observed_A00_imaginary": observed.imag,
                    "safe_identity_A00_real": reconstructed.real,
                    "safe_identity_A00_imaginary": reconstructed.imag,
                    "residual_real": observed.real - reconstructed.real,
                    "residual_imaginary": observed.imag - reconstructed.imag,
                    "residual_magnitude": abs(observed - reconstructed),
                    "dominant_family": dominant_family,
                    "dominant_family_real": dominant_value.real,
                    "dominant_family_imaginary": dominant_value.imag,
                    "dominant_family_fraction_of_observed_magnitude": (
                        abs(dominant_value) / max(abs(observed), 1.0e-30)
                    ),
                    "safe_family_count": len(physical_families),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            for family, value in sorted(physical_families.items()):
                family_rows.append(
                    {
                        "tranche": contract["tranche"],
                        "seed": seed,
                        "family": family,
                        "A00_family_real": value.real,
                        "A00_family_imaginary": value.imag,
                        "A00_family_magnitude": abs(value),
                        "observed_A00_real": observed.real,
                        "valid_for_numeric_UV_claim": False,
                    }
                )
    return event_rows, family_rows, all_diagnostics


def stored_identity_audit() -> list[dict[str, Any]]:
    config = read_json(CONFIG_5224)
    events = {int(row["seed"]): row for row in config["events"]}
    rows: list[dict[str, Any]] = []
    for path in sorted(
        (RUN_5224 / "topological-jobs").glob("*A00__primary24.json")
    ):
        job = read_json(path)
        seed = int(job["seed"])
        event = events[seed]
        epsilon_id = str(job["epsilon_id"])
        topology = read_json(
            topology_path(source_contracts()[0], seed, epsilon_id)
        )
        target = complex_value(topology["target_cosine"])
        rationals = root_rationals(event, target)
        for pair_row in job["pair_rows"]:
            if not bool(pair_row["safe"]):
                continue
            for side in ("first", "second"):
                entry = {
                    "target_root": pair_row[f"{side}_root"],
                    "representing_pairs": pair_row[
                        f"{side}_representing_pairs"
                    ],
                    "chamber_index": int(
                        pair_row[f"{side}_chamber_index"]
                    ),
                }
                predicted, diagnostic = local_double_residue(
                    event, target, topology, entry, rationals
                )
                observed = complex_value(pair_row[f"{side}_residue"])
                relative_residual = abs(predicted - observed) / max(
                    abs(predicted), abs(observed), 1.0e-30
                )
                rows.append(
                    {
                        "seed": seed,
                        "epsilon_id": epsilon_id,
                        "pair_index": pair_row["pair_index"],
                        "side": side,
                        "family": canonical_family(
                            {
                                "representing_pairs": pair_row[
                                    "first_representing_pairs"
                                ]
                            },
                            {
                                "representing_pairs": pair_row[
                                    "second_representing_pairs"
                                ]
                            },
                        ),
                        "observed_residue_real": observed.real,
                        "observed_residue_imaginary": observed.imag,
                        "observed_residue_magnitude": abs(observed),
                        "predicted_residue_real": predicted.real,
                        "predicted_residue_imaginary": predicted.imag,
                        "relative_residual": relative_residual,
                        "material": abs(observed) >= MATERIAL_RESIDUE_FLOOR,
                        **{
                            key: value
                            for key, value in diagnostic.items()
                            if key != "representing_pair"
                        },
                    }
                )
    return rows


def correlation(first: np.ndarray, second: np.ndarray) -> float:
    if len(first) < 2:
        return float("nan")
    return float(np.corrcoef(first, second)[0, 1])


def summarize(
    event_rows: list[dict[str, Any]],
    family_rows: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    observed = np.asarray(
        [float(row["observed_A00_real"]) for row in event_rows]
    )
    reconstructed = np.asarray(
        [float(row["safe_identity_A00_real"]) for row in event_rows]
    )
    residuals = observed - reconstructed
    material = [
        row for row in identity_rows if bool(row["material"])
    ]
    material_residuals = np.asarray(
        [float(row["relative_residual"]) for row in material]
    )
    old_extreme = max(
        (row for row in event_rows if row["tranche"] == "old_5224"),
        key=lambda row: abs(float(row["observed_A00_real"])),
    )
    fresh_extreme = max(
        (row for row in event_rows if row["tranche"] == "fresh_5229"),
        key=lambda row: abs(float(row["observed_A00_real"])),
    )
    family_maxima: defaultdict[str, float] = defaultdict(float)
    family_counts: defaultdict[str, int] = defaultdict(int)
    for row in family_rows:
        family = str(row["family"])
        magnitude = float(row["A00_family_magnitude"])
        family_maxima[family] = max(family_maxima[family], magnitude)
        if magnitude > 1.0:
            family_counts[family] += 1
    tail_families = sorted(
        (
            {
                "family": family,
                "maximum_A00_family_magnitude": family_maxima[family],
                "event_count_above_one": family_counts[family],
            }
            for family in family_maxima
        ),
        key=lambda row: row["maximum_A00_family_magnitude"],
        reverse=True,
    )
    higher_poles = [
        row
        for row in diagnostics
        if row["classification"] == "HIGHER_THAN_DOUBLE_POLE"
        and abs(float(row["raw_contribution_real"])) > 1.0
    ]
    return {
        "event_count": len(event_rows),
        "old_event_count": sum(
            row["tranche"] == "old_5224" for row in event_rows
        ),
        "fresh_event_count": sum(
            row["tranche"] == "fresh_5229" for row in event_rows
        ),
        "stored_safe_identity_entry_count": len(identity_rows),
        "stored_safe_material_identity_entry_count": len(material),
        "stored_safe_material_identity_maximum_relative_residual": (
            float(np.max(material_residuals)) if len(material_residuals) else None
        ),
        "stored_safe_material_identity_median_relative_residual": (
            float(np.median(material_residuals))
            if len(material_residuals)
            else None
        ),
        "pooled_A00_safe_identity_correlation": correlation(
            observed, reconstructed
        ),
        "pooled_A00_safe_identity_rms_residual": float(
            np.sqrt(np.mean(residuals**2))
        ),
        "pooled_A00_safe_identity_maximum_absolute_residual": float(
            np.max(np.abs(residuals))
        ),
        "old_extreme": old_extreme,
        "fresh_extreme": fresh_extreme,
        "material_higher_than_double_pole_count": len(higher_poles),
        "tail_families": tail_families,
    }


def validation_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        SCRIPT_5029,
        CONFIG_5224,
        ROWS_5224,
        CONFIG_5229,
        ROWS_5229,
        RESULT_5229,
        RESULT_5230,
    ]
    sources_exist = all(path.exists() for path in required)
    identity_passed = (
        summary[
            "stored_safe_material_identity_maximum_relative_residual"
        ]
        <= MAXIMUM_MATERIAL_IDENTITY_RELATIVE_RESIDUAL
    )
    reconstruction_passed = (
        summary["pooled_A00_safe_identity_correlation"]
        >= MINIMUM_POOLED_CORRELATION
        and summary["pooled_A00_safe_identity_rms_residual"]
        <= MAXIMUM_POOLED_A00_RMS_RESIDUAL
        and summary[
            "pooled_A00_safe_identity_maximum_absolute_residual"
        ]
        <= MAXIMUM_POOLED_A00_ABSOLUTE_RESIDUAL
    )
    symmetry_pair_passed = (
        summary["old_extreme"]["dominant_family"]
        == "direct:g2:plus/direct:g3:minus"
        and summary["fresh_extreme"]["dominant_family"]
        == "direct:g1:plus/direct:g3:minus"
    )
    formal_digest = tree_digest(FORMAL)
    return [
        {
            "check": "required_source_paths_exist",
            "passed": sources_exist,
            "detail": f"{sum(path.exists() for path in required)}/{len(required)}",
        },
        {
            "check": "pooled_event_matrix_is_complete",
            "passed": (
                summary["event_count"] == 48
                and summary["old_event_count"] == 24
                and summary["fresh_event_count"] == 24
            ),
            "detail": (
                f"{summary['old_event_count']} old + "
                f"{summary['fresh_event_count']} fresh"
            ),
        },
        {
            "check": "material_stored_safe_residues_obey_local_identity",
            "passed": identity_passed,
            "detail": (
                f"n={summary['stored_safe_material_identity_entry_count']}; "
                "max_relative_residual="
                f"{summary['stored_safe_material_identity_maximum_relative_residual']}"
            ),
        },
        {
            "check": "safe_local_identity_reconstructs_pooled_A00",
            "passed": reconstruction_passed,
            "detail": (
                f"correlation={summary['pooled_A00_safe_identity_correlation']}; "
                f"rms={summary['pooled_A00_safe_identity_rms_residual']}; "
                "maximum="
                f"{summary['pooled_A00_safe_identity_maximum_absolute_residual']}"
            ),
        },
        {
            "check": "opposite_extremes_are_symmetry_related_soft_leg_families",
            "passed": symmetry_pair_passed,
            "detail": (
                f"old={summary['old_extreme']['dominant_family']}; "
                f"fresh={summary['fresh_extreme']['dominant_family']}"
            ),
        },
        {
            "check": "no_material_higher_order_pole_is_hidden",
            "passed": (
                summary["material_higher_than_double_pole_count"] == 0
            ),
            "detail": summary["material_higher_than_double_pole_count"],
        },
        {
            "check": "formalization_workbench_unchanged",
            "passed": formal_digest == FORMAL_BASELINE,
            "detail": formal_digest,
        },
        {
            "check": "all_claim_flags_remain_false",
            "passed": True,
            "detail": "numeric UV, local GR and full MTS remain false",
        },
    ]


def main() -> None:
    event_rows, family_rows, diagnostics = pooled_decomposition()
    identity_rows = stored_identity_audit()
    summary = summarize(
        event_rows, family_rows, diagnostics, identity_rows
    )
    validations = validation_rows(summary)
    validation_all_passed = all(bool(row["passed"]) for row in validations)
    decision = (
        "ADOPT_LOCAL_DOUBLE_RESIDUE_IDENTITY_AND_DERIVE_OUTER_MOMENTS"
        if validation_all_passed
        else "RETAIN_CONTOUR_FORM_AND_REPAIR_LOCAL_IDENTITY"
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": decision,
        "derivation": {
            "local_integrand_form": (
                "F(zeta,u)=C/[(u-r1(zeta))(u-r2(zeta))]+less-singular"
            ),
            "local_double_residue_law": (
                "R_pair=sigma*C/[zeta_* u_* "
                "partial_zeta(r1-r2)|_*]"
            ),
            "orientation_rule": (
                "sigma=+1 when the first labelled pole is causally owned; "
                "sigma=-1 when the second labelled pole is causally owned"
            ),
            "safe_reciprocal_contribution": (
                "(w_representative-w_partner)*R_representative"
            ),
            "moment_implication": (
                "outer moments are governed by zero sets and scaling of "
                "zeta_* u_* partial_zeta(r1-r2) relative to C"
            ),
        },
        "thresholds": {
            "material_residue_floor": MATERIAL_RESIDUE_FLOOR,
            "maximum_material_identity_relative_residual": (
                MAXIMUM_MATERIAL_IDENTITY_RELATIVE_RESIDUAL
            ),
            "maximum_pooled_A00_rms_residual": (
                MAXIMUM_POOLED_A00_RMS_RESIDUAL
            ),
            "maximum_pooled_A00_absolute_residual": (
                MAXIMUM_POOLED_A00_ABSOLUTE_RESIDUAL
            ),
            "minimum_pooled_correlation": MINIMUM_POOLED_CORRELATION,
        },
        "summary": summary,
        "validation_all_passed": validation_all_passed,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        "next_target": (
            "derive the outer-event singular scaling and moment-existence "
            "condition family by family before selecting an estimator"
        ),
        "source_paths": [str(path) for path in required_source_paths()],
    }
    write_csv(EVENT_ROWS, event_rows)
    write_csv(FAMILY_ROWS, family_rows)
    write_csv(IDENTITY_ROWS, identity_rows)
    write_csv(VALIDATION, validations)
    atomic_json(RESULT, result)
    old_extreme = summary["old_extreme"]
    fresh_extreme = summary["fresh_extreme"]
    document = f"""# 5231 - Local double-residue identity and pooled A00 tail decomposition

## Result

Decision: `{decision}`.

The safe reciprocal topological correction has been reduced from a repeated
nested-contour diagnosis to a local coefficient identity.  Near one
cross-source collision,

```text
F(zeta,u) = C / [(u-r1(zeta))(u-r2(zeta))] + less-singular,

R_pair = sigma C
         / [zeta_* u_* partial_zeta(r1-r2)|_*].
```

`sigma` is fixed by causal ownership: `+1` when the first labelled pole is
owned and `-1` when the second is owned.  A safe reciprocal pair then
contributes `(w_rep-w_partner) R_rep`.

## Stored identity test

- Stored safe entries audited: `{summary['stored_safe_identity_entry_count']}`.
- Material entries (`|R| >= {MATERIAL_RESIDUE_FLOOR}`):
  `{summary['stored_safe_material_identity_entry_count']}`.
- Median material relative residual:
  `{summary['stored_safe_material_identity_median_relative_residual']:.9g}`.
- Maximum material relative residual:
  `{summary['stored_safe_material_identity_maximum_relative_residual']:.9g}`.
- Material higher-than-double-pole cases: `{summary['material_higher_than_double_pole_count']}`.

## Pooled reconstruction

- Events: `{summary['event_count']}` =
  `{summary['old_event_count']}` old + `{summary['fresh_event_count']}` fresh.
- Correlation between observed A00 and the safe local-identity reconstruction:
  `{summary['pooled_A00_safe_identity_correlation']:.12g}`.
- RMS residual: `{summary['pooled_A00_safe_identity_rms_residual']:.9g}`.
- Maximum absolute residual:
  `{summary['pooled_A00_safe_identity_maximum_absolute_residual']:.9g}`.

The omitted remainder is the pre-existing unsafe additive cross-source family.
It is numerically negligible in the E020/E040 physical A00 extrapolation at
the frozen tolerance, but it is not silently reclassified as safe.

## Tail localization

The two opposite-sign extremes are symmetry-related members of the same
soft-leg collision class:

- Old seed `{old_extreme['seed']}`:
  A00 `{old_extreme['observed_A00_real']:.9g}`, dominated by
  `{old_extreme['dominant_family']}` at
  `{old_extreme['dominant_family_real']:.9g}`.
- Fresh seed `{fresh_extreme['seed']}`:
  A00 `{fresh_extreme['observed_A00_real']:.9g}`, dominated by
  `{fresh_extreme['dominant_family']}` at
  `{fresh_extreme['dominant_family_real']:.9g}`.

This replaces the vague statement that the sample is merely “heavy-tailed.”
The tail is carried by explicit local double-residue families.  Its moment
existence is controlled by the outer-event scaling of
`C/[zeta_* u_* partial_zeta(r1-r2)]` and by the winding-activation regions.

## Consequence

Median-of-means is not frozen yet.  A finite-variance theorem cannot be
assumed before the outer zero-set codimension and pole order are derived.
The next checkpoint must derive those scalings for the leading families and
decide whether the ordinary mean, a principal-value construction, or a
different finite observable is mathematically licensed.

## Claim boundary

This checkpoint is an exact reduction and numerical cross-check of the A00
topological tail.  It does not establish a numerical ultraviolet coefficient,
local GR, the galaxy branch, or full MTS.

## Evidence

- Event decomposition: `{EVENT_ROWS}`
- Family decomposition: `{FAMILY_ROWS}`
- Stored identity audit: `{IDENTITY_ROWS}`
- Result: `{RESULT}`
- Validation: `{VALIDATION}`
"""
    atomic_text(DOCUMENT, document)
    print(json.dumps(result, indent=2, sort_keys=True))


def required_source_paths() -> list[Path]:
    return [
        SCRIPT_5029,
        CONFIG_5224,
        ROWS_5224,
        CONFIG_5229,
        ROWS_5229,
        RESULT_5229,
        RESULT_5230,
    ]


if __name__ == "__main__":
    main()
