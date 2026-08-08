from __future__ import annotations

import argparse
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
SOURCE = POST / "source-intake" / "functional_rg" / "5214"
RUN_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5212"
    / "runs"
    / "fresh_two_stratum_pilot_v2"
)
REPLAY = SOURCE / "runs" / "a00_pair_replay_v1"
REPLAY_JOBS = REPLAY / "jobs"
SCRIPT_5212 = (
    POST / "scripts" / "Y5_R2FR_5212_fresh_crossed_hhh_two_stratum_pilot.py"
)
GATE_5213 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5213"
    / "source_separated_additive_cluster_cauchy_zero.json"
)
EVENT_ROWS_5212 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5212"
    / "fresh_two_stratum_completed_event_rows.csv"
)
RESULT_5212 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5212"
    / "fresh_two_stratum_pilot_results.json"
)
PAIR_ROWS_CSV = SOURCE / "A00_pair_contributions.csv"
FAMILY_ROWS_CSV = SOURCE / "A00_event_family_contributions.csv"
EVENT_ROWS_CSV = SOURCE / "A00_event_decomposition.csv"
AUDIT_JSON = SOURCE / "A00_source_pole_family_audit.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5214_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5214-Y5-R2FR-A00-identical-graviton-permutation-control-variate.md"
)
RESULT_5010 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5010"
    / "coupled_three_particle_cut_results.json"
)
INTEGRAND_CHECKS_5010 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5010"
    / "three_particle_cut_integrand_checks.csv"
)
DOCUMENT_5010 = (
    POST
    / "5010-Y5-R2FR-coupled-three-particle-cut-normalization-and-soft-plus-integrand.md"
)
SCRIPT_5017 = (
    POST
    / "scripts"
    / "Y5_R2FR_5017_complex_safe_hhh_crossed_integrand_and_coupled_locality_smoke.py"
)

MARKER = "MTS_5214_A00_SOURCE_POLE_CONTROL_VARIATE"
REPLAY_REVISION = "a00-pair-residue-replay-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
KERNEL_MULTIPLIER = -2.0 / math.pi
A00_PHYSICAL_WEIGHT = -0.008
SOURCE_CONFIG_DIGEST = (
    "029d1c238303ab54a90b3b523aa360c6e5191bed55cc3411998700e265d371e3"
)
DOMINANT_SOURCE_GROUPS = (
    ("direct:g1:plus_u", "direct:g3:minus_u"),
    ("direct:g1:plus_v", "direct:g3:minus_v"),
)
PERMUTED_SOURCE_GROUPS = (
    ("direct:g1:minus_u", "direct:g3:plus_u"),
    ("direct:g1:minus_v", "direct:g3:plus_v"),
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5212 = load_module(SCRIPT_5212, "mts_5212_for_5214")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(
        candidate for candidate in path.rglob("*") if candidate.is_file()
    ):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def row_complex(value: dict[str, float]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


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
        raise RuntimeError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def normalized_pair_groups(entry: dict[str, Any]) -> tuple[tuple[str, ...], ...]:
    return tuple(
        sorted(
            tuple(sorted(str(label) for label in pair))
            for pair in entry["representing_pairs"]
        )
    )


def family_signature(
    first: dict[str, Any], second: dict[str, Any], safe: bool
) -> str:
    groups = tuple(
        sorted(
            {
                *normalized_pair_groups(first),
                *normalized_pair_groups(second),
            }
        )
    )
    return json.dumps(
        {"safe": safe, "source_pairs": groups},
        sort_keys=True,
        separators=(",", ":"),
    )


def signature_from_groups(groups: tuple[tuple[str, str], ...]) -> str:
    return json.dumps(
        {
            "safe": True,
            "source_pairs": tuple(
                sorted(tuple(sorted(group)) for group in groups)
            ),
        },
        sort_keys=True,
        separators=(",", ":"),
    )


DOMINANT_FAMILY_SIGNATURE = signature_from_groups(DOMINANT_SOURCE_GROUPS)
PERMUTED_FAMILY_SIGNATURE = signature_from_groups(PERMUTED_SOURCE_GROUPS)


def permutation_partition_ratio(
    event: dict[str, Any], relative_root: complex
) -> complex:
    _, _, internal = (
        M5212.M5077.M5036.N5030.M5028.event_geometry(
            float(event["soft_energy"]),
            complex(float(event["soft_cosine"]), 0.0),
            complex(float(event["decay_cosine"]), 0.0),
            relative_root,
        )
    )
    energy_g1 = complex(internal[0, 0])
    energy_g3 = complex(internal[2, 0])
    if abs(energy_g1) <= 1.0e-12 or abs(energy_g3) <= 1.0e-12:
        raise RuntimeError("permutation partition ratio is singular")
    return (energy_g3 / energy_g1) ** 2


def decompose_topological_value(
    module: Any,
    topology: dict[str, Any],
    profile: dict[str, Any],
) -> tuple[complex, bool, int, int, int, list[dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    for chamber_index, chamber in enumerate(topology["chambers"]):
        for crossing in chamber["surface_crossings"]:
            entries.append({**crossing, "chamber_index": chamber_index})
    reciprocal_pairs = M5212.M5124.pair_reciprocal_entries(entries)

    selected: dict[int, list[complex]] = {
        index: [] for index in range(len(topology["chambers"]))
    }
    contracts: list[dict[str, Any]] = []
    safe_pair_count = 0
    unsafe_pair_count = 0
    for first, second, root_residual in reciprocal_pairs:
        unsafe = M5212.M5124.reciprocal_unsafe_pairs(
            first["representing_pairs"]
        ) or M5212.M5124.reciprocal_unsafe_pairs(
            second["representing_pairs"]
        )
        if unsafe:
            unsafe_pair_count += 1
            selected[first["chamber_index"]].append(
                complex(first["target_root"])
            )
            selected[second["chamber_index"]].append(
                complex(second["target_root"])
            )
            contracts.append(
                {
                    "safe": False,
                    "first": first,
                    "second": second,
                    "root_residual": root_residual,
                }
            )
        else:
            safe_pair_count += 1
            representative, partner = (
                (first, second)
                if abs(complex(first["target_root"])) >= 1.0
                else (second, first)
            )
            selected[representative["chamber_index"]].append(
                complex(representative["target_root"])
            )
            contracts.append(
                {
                    "safe": True,
                    "representative": representative,
                    "partner": partner,
                    "root_residual": root_residual,
                }
            )

    _, ownerships = module.physical_chambers()
    residues: dict[tuple[int, complex], dict[str, Any]] = {}
    all_stable = True
    catalog_row_count = 0
    for chamber_index, ownership in enumerate(ownerships):
        required_roots = selected[chamber_index]
        if not required_roots:
            continue
        chamber = topology["chambers"][chamber_index]
        catalog, stable = module.chamber_residue_catalog(
            ownership,
            complex(chamber["target_start_log"]),
            complex(chamber["target_end_log"]),
            required_roots,
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            -1.0,
        )
        all_stable = all_stable and stable
        catalog_row_count += len(catalog)
        for root in required_roots:
            match = min(
                catalog, key=lambda row: abs(complex(row["root"]) - root)
            )
            matching_residual = abs(complex(match["root"]) - root) / max(
                1.0, abs(root), abs(complex(match["root"]))
            )
            if matching_residual > 2.0e-5:
                raise RuntimeError(
                    "5214 reciprocal-reduced residue root mismatch"
                )
            residues[(chamber_index, root)] = {
                "residue": complex(match["residue"]),
                "catalog_pairs": match["pairs"],
                "matching_residual": matching_residual,
            }

    total = 0.0j
    pair_rows: list[dict[str, Any]] = []
    for pair_index, contract in enumerate(contracts):
        if contract["safe"]:
            first = contract["representative"]
            second = contract["partner"]
            first_record = residues[
                (first["chamber_index"], complex(first["target_root"]))
            ]
            first_residue = first_record["residue"]
            second_residue = -first_residue
            contribution = (
                int(first["winding_correction"])
                - int(second["winding_correction"])
            ) * first_residue
            second_record: dict[str, Any] | None = None
        else:
            first = contract["first"]
            second = contract["second"]
            first_record = residues[
                (first["chamber_index"], complex(first["target_root"]))
            ]
            second_record = residues[
                (second["chamber_index"], complex(second["target_root"]))
            ]
            first_residue = first_record["residue"]
            second_residue = second_record["residue"]
            contribution = (
                int(first["winding_correction"]) * first_residue
                + int(second["winding_correction"]) * second_residue
            )
        total += contribution
        pair_rows.append(
            {
                "pair_index": pair_index,
                "safe": bool(contract["safe"]),
                "family_signature": family_signature(
                    first, second, bool(contract["safe"])
                ),
                "first_chamber_index": int(first["chamber_index"]),
                "second_chamber_index": int(second["chamber_index"]),
                "first_root": complex_row(complex(first["target_root"])),
                "second_root": complex_row(complex(second["target_root"])),
                "first_winding": int(first["winding_correction"]),
                "second_winding": int(second["winding_correction"]),
                "first_representing_pairs": first["representing_pairs"],
                "second_representing_pairs": second["representing_pairs"],
                "first_catalog_pairs": first_record["catalog_pairs"],
                "second_catalog_pairs": (
                    second_record["catalog_pairs"]
                    if second_record is not None
                    else first_record["catalog_pairs"]
                ),
                "first_residue": complex_row(first_residue),
                "second_residue": complex_row(second_residue),
                "raw_contribution": complex_row(contribution),
                "normalized_contribution": complex_row(
                    KERNEL_MULTIPLIER * contribution
                ),
                "reciprocal_root_residual": float(
                    contract["root_residual"]
                ),
                "first_catalog_root_residual": float(
                    first_record["matching_residual"]
                ),
                "second_catalog_root_residual": (
                    float(second_record["matching_residual"])
                    if second_record is not None
                    else float(first_record["matching_residual"])
                ),
            }
        )
    return (
        total,
        all_stable,
        catalog_row_count,
        safe_pair_count,
        unsafe_pair_count,
        pair_rows,
    )


def replay_digest(config: dict[str, Any]) -> str:
    return canonical_digest(
        {
            "revision": REPLAY_REVISION,
            "source_config_digest": config["config_digest"],
            "script_5212_sha256": digest(SCRIPT_5212),
            "gate_5213_sha256": digest(GATE_5213),
        }
    )


def replay_job(
    manager: Any,
    config: dict[str, Any],
    replay_config_digest: str,
    epsilon_id: str,
    seed: int,
) -> dict[str, Any]:
    job_key = f"TOP__{epsilon_id}__S{seed}_N0000__A00__primary24"
    source_job_path = RUN_SOURCE / "topological-jobs" / f"{job_key}.json"
    source_job = read_json(source_job_path)
    topology_path = Path(source_job["topology_file"])
    output = REPLAY_JOBS / f"{job_key}.json"
    source_job_sha256 = digest(source_job_path)
    source_topology_sha256 = digest(topology_path)
    if output.exists():
        cached = read_json(output)
        if (
            cached.get("status") == "COMPLETE"
            and cached.get("replay_config_digest") == replay_config_digest
            and cached.get("source_job_sha256") == source_job_sha256
            and cached.get("source_topology_sha256")
            == source_topology_sha256
        ):
            return cached

    event_id = f"S{seed}_N0000"
    event = manager.events[event_id]
    argument = manager.arguments[f"{epsilon_id}_A00"]
    topology = read_json(topology_path)
    target = M5212.M5077.M5036.complex_from_row(
        argument["target_cosine"]
    )
    module = M5212.M5077.M5036.N5030
    previous_event = M5212.M5077.CURRENT_EVENT
    previous_argument = M5212.M5077.CURRENT_ARGUMENT
    previous_catalog = module.chamber_residue_catalog
    previous_global_value = module.global_chamber_value
    previous_job = M5212.M5077.M5036.MREPAIR.CURRENT_JOB
    try:
        M5212.M5077.CURRENT_EVENT = event
        M5212.M5077.CURRENT_ARGUMENT = argument
        M5212.M5077.M5036.M5035.M5034.configure(event, target)
        module.chamber_residue_catalog = M5212.certified_5212_catalog
        M5212.M5077.M5036.MREPAIR.CURRENT_JOB = job_key
        M5212.M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
        M5212.M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
        M5212.M5077.OUTWARD_CONTOUR_AUDIT.clear()
        M5212.M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
        M5212.SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT.clear()
        M5212.M5077.removable_extension_gate()
        extension = M5212.AdaptiveRemovableGlobalExtension(
            previous_global_value
        )
        module.global_chamber_value = extension
        (
            raw_total,
            residues_stable,
            catalog_row_count,
            safe_pair_count,
            unsafe_pair_count,
            pair_rows,
        ) = decompose_topological_value(
            module, topology, config["tiers"]["primary24"]
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global_value
        M5212.M5077.M5036.MREPAIR.CURRENT_JOB = previous_job
        M5212.M5077.CURRENT_EVENT = previous_event
        M5212.M5077.CURRENT_ARGUMENT = previous_argument

    normalized_total = KERNEL_MULTIPLIER * raw_total
    stored_total = row_complex(
        source_job["normalized_topological_D_hhh_over_G3"]
    )
    reproduction_relative_residual = abs(
        normalized_total - stored_total
    ) / max(1.0, abs(stored_total))
    result = {
        "checkpoint_marker": MARKER,
        "revision": REPLAY_REVISION,
        "replay_config_digest": replay_config_digest,
        "job_key": job_key,
        "epsilon_id": epsilon_id,
        "seed": seed,
        "event_id": event_id,
        "base_argument_id": "A00",
        "status": "COMPLETE",
        "residues_stable": bool(residues_stable),
        "catalog_row_count": catalog_row_count,
        "safe_pair_count": safe_pair_count,
        "unsafe_pair_count": unsafe_pair_count,
        "pair_rows": pair_rows,
        "raw_total": complex_row(raw_total),
        "normalized_total": complex_row(normalized_total),
        "stored_normalized_total": complex_row(stored_total),
        "reproduction_relative_residual": float(
            reproduction_relative_residual
        ),
        "source_separated_zero_count": len(
            M5212.SOURCE_SEPARATED_CLUSTER_ZERO_AUDIT
        ),
        "adaptive_removable_extension_count": len(extension.calls),
        "source_job": str(source_job_path),
        "source_job_sha256": source_job_sha256,
        "source_topology": str(topology_path),
        "source_topology_sha256": source_topology_sha256,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if (
        not residues_stable
        or not finite_complex(normalized_total)
        or reproduction_relative_residual > 1.0e-9
    ):
        raise RuntimeError(f"5214 replay failed for {job_key}: {result}")
    atomic_json(output, result)
    return result


def scalar_summary(values: np.ndarray) -> dict[str, float]:
    return {
        "count": int(len(values)),
        "mean": float(np.mean(values)),
        "sample_standard_deviation": float(np.std(values, ddof=1)),
        "standard_error": float(
            np.std(values, ddof=1) / math.sqrt(len(values))
        ),
        "minimum": float(np.min(values)),
        "maximum": float(np.max(values)),
    }


def load_physical_rows() -> dict[int, dict[str, str]]:
    with EVENT_ROWS_5212.open(newline="", encoding="utf-8") as handle:
        return {
            int(row["seed"]): row
            for row in csv.DictReader(handle)
            if row["stratum"] == "topological"
        }


def analyse(
    config: dict[str, Any],
    replay_config_digest: str,
    replayed: list[dict[str, Any]],
) -> dict[str, Any]:
    expected_seeds = tuple(
        int(value)
        for value in config["two_stratum_contract"]["topological_seeds"]
    )
    lookup = {
        (int(row["seed"]), row["epsilon_id"]): row for row in replayed
    }
    if set(lookup) != {
        (seed, epsilon_id)
        for seed in expected_seeds
        for epsilon_id in ("E020", "E040")
    }:
        raise RuntimeError("A00 replay matrix is incomplete")

    pair_csv_rows: list[dict[str, Any]] = []
    family_by_event_epsilon: dict[
        tuple[int, str, str], complex
    ] = {}
    weighted_permuted_by_event_epsilon: dict[
        tuple[int, str], complex
    ] = {}
    family_safe: dict[str, bool] = {}
    event_lookup = {
        int(row["seed"]): row for row in config["events"]
    }
    for row in replayed:
        for pair in row["pair_rows"]:
            normalized = row_complex(pair["normalized_contribution"])
            signature = pair["family_signature"]
            key = (int(row["seed"]), row["epsilon_id"], signature)
            family_by_event_epsilon[key] = (
                family_by_event_epsilon.get(key, 0.0j) + normalized
            )
            family_safe[signature] = bool(pair["safe"])
            first_partition_ratio = 0.0j
            second_partition_ratio = 0.0j
            weighted_permuted = 0.0j
            if signature == PERMUTED_FAMILY_SIGNATURE:
                first_partition_ratio = permutation_partition_ratio(
                    event_lookup[int(row["seed"])],
                    row_complex(pair["first_root"]),
                )
                second_partition_ratio = permutation_partition_ratio(
                    event_lookup[int(row["seed"])],
                    row_complex(pair["second_root"]),
                )
                weighted_permuted = KERNEL_MULTIPLIER * (
                    first_partition_ratio
                    * int(pair["first_winding"])
                    * row_complex(pair["first_residue"])
                    + second_partition_ratio
                    * int(pair["second_winding"])
                    * row_complex(pair["second_residue"])
                )
                weighted_key = (int(row["seed"]), row["epsilon_id"])
                weighted_permuted_by_event_epsilon[weighted_key] = (
                    weighted_permuted_by_event_epsilon.get(
                        weighted_key, 0.0j
                    )
                    + weighted_permuted
                )
            pair_csv_rows.append(
                {
                    "seed": row["seed"],
                    "event_id": row["event_id"],
                    "epsilon_id": row["epsilon_id"],
                    "pair_index": pair["pair_index"],
                    "safe": pair["safe"],
                    "family_signature": signature,
                    "first_root_real": pair["first_root"]["real"],
                    "first_root_imaginary": pair["first_root"]["imaginary"],
                    "second_root_real": pair["second_root"]["real"],
                    "second_root_imaginary": pair["second_root"]["imaginary"],
                    "first_winding": pair["first_winding"],
                    "second_winding": pair["second_winding"],
                    "normalized_real": normalized.real,
                    "normalized_imaginary": normalized.imag,
                    "first_permutation_partition_ratio_real": (
                        first_partition_ratio.real
                        if signature == PERMUTED_FAMILY_SIGNATURE
                        else ""
                    ),
                    "first_permutation_partition_ratio_imaginary": (
                        first_partition_ratio.imag
                        if signature == PERMUTED_FAMILY_SIGNATURE
                        else ""
                    ),
                    "second_permutation_partition_ratio_real": (
                        second_partition_ratio.real
                        if signature == PERMUTED_FAMILY_SIGNATURE
                        else ""
                    ),
                    "second_permutation_partition_ratio_imaginary": (
                        second_partition_ratio.imag
                        if signature == PERMUTED_FAMILY_SIGNATURE
                        else ""
                    ),
                    "weighted_permuted_real": (
                        weighted_permuted.real
                        if signature == PERMUTED_FAMILY_SIGNATURE
                        else ""
                    ),
                    "weighted_permuted_imaginary": (
                        weighted_permuted.imag
                        if signature == PERMUTED_FAMILY_SIGNATURE
                        else ""
                    ),
                    "source_job": row["source_job"],
                    "status": "REPLAYED_PAIR_CONTRIBUTION",
                    "valid_for_numeric_UV_claim": False,
                }
            )

    dominant_pair_rows = [
        row
        for row in pair_csv_rows
        if row["family_signature"] == DOMINANT_FAMILY_SIGNATURE
    ]
    permuted_pair_rows = [
        row
        for row in pair_csv_rows
        if row["family_signature"] == PERMUTED_FAMILY_SIGNATURE
    ]
    if not dominant_pair_rows or not permuted_pair_rows:
        raise RuntimeError("permutation-control source families are incomplete")
    if not all(bool(row["safe"]) for row in dominant_pair_rows + permuted_pair_rows):
        raise RuntimeError("permutation-control source family is not reciprocal-safe")

    signatures = sorted(family_safe)
    family_csv_rows: list[dict[str, Any]] = []
    event_family_values: dict[tuple[int, str], complex] = {}
    for seed in expected_seeds:
        for signature in signatures:
            value_e020 = family_by_event_epsilon.get(
                (seed, "E020", signature), 0.0j
            )
            value_e040 = family_by_event_epsilon.get(
                (seed, "E040", signature), 0.0j
            )
            extrapolated = 2.0 * value_e020 - value_e040
            physical = A00_PHYSICAL_WEIGHT * extrapolated
            event_family_values[(seed, signature)] = physical
            family_csv_rows.append(
                {
                    "seed": seed,
                    "family_signature": signature,
                    "safe": family_safe[signature],
                    "E020_real": value_e020.real,
                    "E020_imaginary": value_e020.imag,
                    "E040_real": value_e040.real,
                    "E040_imaginary": value_e040.imag,
                    "extrapolated_A00_real": extrapolated.real,
                    "extrapolated_A00_imaginary": extrapolated.imag,
                    "physical_zm0p6_weight": A00_PHYSICAL_WEIGHT,
                    "physical_A00_real": physical.real,
                    "physical_A00_imaginary": physical.imag,
                    "status": "SOURCE_FAMILY_DECOMPOSITION",
                    "valid_for_numeric_UV_claim": False,
                }
            )

    physical_rows = load_physical_rows()
    event_csv_rows: list[dict[str, Any]] = []
    event_totals: list[complex] = []
    control_values: list[complex] = []
    adjusted_a00_real_values: list[float] = []
    raw_zm0p6_values: list[complex] = []
    adjusted_zm0p6_real_values: list[float] = []
    raw_local_values: list[complex] = []
    adjusted_local_real_values: list[float] = []
    physical_shape = 1.0 - np.asarray(
        config["physical_cosines"], dtype=np.float64
    ) ** 2
    local_weights = physical_shape / float(physical_shape @ physical_shape)
    zm0p6_local_weight = float(local_weights[0])
    for seed in expected_seeds:
        value_e020 = row_complex(lookup[(seed, "E020")]["normalized_total"])
        value_e040 = row_complex(lookup[(seed, "E040")]["normalized_total"])
        extrapolated = 2.0 * value_e020 - value_e040
        physical_a00 = A00_PHYSICAL_WEIGHT * extrapolated
        family_sum = sum(
            (
                event_family_values[(seed, signature)]
                for signature in signatures
            ),
            0.0j,
        )
        stored_physical = complex(
            float(physical_rows[seed]["topological_zm0p6_real"]),
            float(physical_rows[seed]["topological_zm0p6_imaginary"]),
        )
        dominant_e020 = family_by_event_epsilon.get(
            (seed, "E020", DOMINANT_FAMILY_SIGNATURE), 0.0j
        )
        dominant_e040 = family_by_event_epsilon.get(
            (seed, "E040", DOMINANT_FAMILY_SIGNATURE), 0.0j
        )
        dominant_physical = A00_PHYSICAL_WEIGHT * (
            2.0 * dominant_e020 - dominant_e040
        )
        weighted_permuted_e020 = (
            weighted_permuted_by_event_epsilon.get(
                (seed, "E020"), 0.0j
            )
        )
        weighted_permuted_e040 = (
            weighted_permuted_by_event_epsilon.get(
                (seed, "E040"), 0.0j
            )
        )
        weighted_permuted_physical = A00_PHYSICAL_WEIGHT * (
            2.0 * weighted_permuted_e020
            - weighted_permuted_e040
        )
        control_value = dominant_physical - weighted_permuted_physical
        adjusted_a00_real = physical_a00.real - control_value.real
        adjusted_zm0p6_real = (
            stored_physical.real - control_value.real
        )
        raw_local = complex(
            float(physical_rows[seed]["topological_local_real"]),
            float(physical_rows[seed]["topological_local_imaginary"]),
        )
        adjusted_local_real = (
            raw_local.real
            - zm0p6_local_weight * control_value.real
        )
        event_totals.append(physical_a00)
        control_values.append(control_value)
        adjusted_a00_real_values.append(adjusted_a00_real)
        raw_zm0p6_values.append(stored_physical)
        adjusted_zm0p6_real_values.append(adjusted_zm0p6_real)
        raw_local_values.append(raw_local)
        adjusted_local_real_values.append(adjusted_local_real)
        event_csv_rows.append(
            {
                "seed": seed,
                "soft_energy": next(
                    float(row["soft_energy"])
                    for row in config["events"]
                    if int(row["seed"]) == seed
                ),
                "soft_cosine": next(
                    float(row["soft_cosine"])
                    for row in config["events"]
                    if int(row["seed"]) == seed
                ),
                "decay_cosine": next(
                    float(row["decay_cosine"])
                    for row in config["events"]
                    if int(row["seed"]) == seed
                ),
                "A00_extrapolated_real": extrapolated.real,
                "A00_extrapolated_imaginary": extrapolated.imag,
                "physical_A00_real": physical_a00.real,
                "physical_A00_imaginary": physical_a00.imag,
                "family_sum_real": family_sum.real,
                "family_sum_imaginary": family_sum.imag,
                "family_closure": abs(family_sum - physical_a00),
                "stored_full_zm0p6_real": stored_physical.real,
                "stored_full_zm0p6_imaginary": stored_physical.imag,
                "A10_remainder_real": (
                    stored_physical - physical_a00
                ).real,
                "A10_remainder_imaginary": (
                    stored_physical - physical_a00
                ).imag,
                "dominant_family_real": dominant_physical.real,
                "dominant_family_imaginary": dominant_physical.imag,
                "weighted_permuted_family_real": (
                    weighted_permuted_physical.real
                ),
                "weighted_permuted_family_imaginary": (
                    weighted_permuted_physical.imag
                ),
                "permutation_zero_control_real": control_value.real,
                "permutation_zero_control_imaginary": (
                    control_value.imag
                ),
                "adjusted_A00_real": adjusted_a00_real,
                "adjusted_full_zm0p6_real": adjusted_zm0p6_real,
                "raw_topological_local_real": raw_local.real,
                "adjusted_topological_local_real": adjusted_local_real,
                "zm0p6_local_projector_weight": zm0p6_local_weight,
                "primary_control_applied_to": "real_part_only",
                "status": (
                    "A00_PERMUTATION_CONTROL_RETROSPECTIVE_TEST"
                ),
                "valid_for_numeric_UV_claim": False,
            }
        )

    total_array = np.asarray(event_totals, dtype=np.complex128)
    family_diagnostics: list[dict[str, Any]] = []
    total_real_variance = float(np.var(total_array.real, ddof=1))
    for signature in signatures:
        values = np.asarray(
            [
                event_family_values[(seed, signature)]
                for seed in expected_seeds
            ],
            dtype=np.complex128,
        )
        covariance = float(
            np.cov(values.real, total_array.real, ddof=1)[0, 1]
        )
        family_diagnostics.append(
            {
                "family_signature": signature,
                "safe": family_safe[signature],
                "nonzero_event_count": int(np.count_nonzero(values)),
                "real": scalar_summary(values.real),
                "imaginary": scalar_summary(values.imag),
                "covariance_with_total_real": covariance,
                "covariance_fraction_of_total_variance": (
                    covariance / total_real_variance
                    if total_real_variance > 0.0
                    else 0.0
                ),
                "largest_absolute_events": [
                    {
                        "seed": int(expected_seeds[index]),
                        "value": float(values.real[index]),
                    }
                    for index in np.argsort(np.abs(values.real))[::-1][:4]
                ],
            }
        )
    family_diagnostics.sort(
        key=lambda row: abs(
            float(row["covariance_fraction_of_total_variance"])
        ),
        reverse=True,
    )

    if DOMINANT_FAMILY_SIGNATURE not in signatures:
        raise RuntimeError("dominant source family is absent")
    if PERMUTED_FAMILY_SIGNATURE not in signatures:
        raise RuntimeError("permuted source family is absent")
    dominant_rank = next(
        index
        for index, row in enumerate(family_diagnostics, start=1)
        if row["family_signature"] == DOMINANT_FAMILY_SIGNATURE
    )
    leave_one_out_ranks: list[dict[str, Any]] = []
    family_arrays = {
        signature: np.asarray(
            [
                event_family_values[(seed, signature)].real
                for seed in expected_seeds
            ],
            dtype=np.float64,
        )
        for signature in signatures
    }
    for held_index, held_seed in enumerate(expected_seeds):
        training = np.ones(len(expected_seeds), dtype=bool)
        training[held_index] = False
        training_total = total_array.real[training]
        ranking = sorted(
            signatures,
            key=lambda signature: abs(
                float(
                    np.cov(
                        family_arrays[signature][training],
                        training_total,
                        ddof=1,
                    )[0, 1]
                )
            ),
            reverse=True,
        )
        leave_one_out_ranks.append(
            {
                "held_seed": held_seed,
                "dominant_family_rank": (
                    ranking.index(DOMINANT_FAMILY_SIGNATURE) + 1
                ),
                "training_selected_family": ranking[0],
                "training_selection_matches": (
                    ranking[0] == DOMINANT_FAMILY_SIGNATURE
                ),
            }
        )

    control_array = np.asarray(
        control_values, dtype=np.complex128
    )
    adjusted_a00_real_array = np.asarray(
        adjusted_a00_real_values, dtype=np.float64
    )
    raw_zm0p6_array = np.asarray(
        raw_zm0p6_values, dtype=np.complex128
    )
    adjusted_zm0p6_real_array = np.asarray(
        adjusted_zm0p6_real_values, dtype=np.float64
    )
    raw_local_array = np.asarray(
        raw_local_values, dtype=np.complex128
    )
    adjusted_local_real_array = np.asarray(
        adjusted_local_real_values, dtype=np.float64
    )

    def variance_comparison(
        raw_values: np.ndarray, adjusted_values: np.ndarray
    ) -> dict[str, Any]:
        raw_summary = scalar_summary(raw_values)
        adjusted_summary = scalar_summary(adjusted_values)
        ratio = (
            adjusted_summary["sample_standard_deviation"]
            / raw_summary["sample_standard_deviation"]
        )
        return {
            "raw": raw_summary,
            "adjusted": adjusted_summary,
            "standard_deviation_ratio": ratio,
            "variance_reduction_factor": 1.0 / (ratio * ratio),
        }

    a00_variance = variance_comparison(
        total_array.real, adjusted_a00_real_array
    )
    zm0p6_variance = variance_comparison(
        raw_zm0p6_array.real, adjusted_zm0p6_real_array
    )
    local_variance = variance_comparison(
        raw_local_array.real, adjusted_local_real_array
    )
    result_5212 = read_json(RESULT_5212)["analysis"]
    old_hhh_real_error = float(
        result_5212["hhh_local_coefficient"]["real_standard_error"]
    )
    raw_topological_local_se = float(
        np.std(raw_local_array.real, ddof=1)
        / math.sqrt(len(raw_local_array))
    )
    adjusted_topological_local_se = float(
        np.std(adjusted_local_real_array, ddof=1)
        / math.sqrt(len(adjusted_local_real_array))
    )
    adjusted_hhh_real_error = math.sqrt(
        max(
            0.0,
            old_hhh_real_error**2
            - raw_topological_local_se**2
            + adjusted_topological_local_se**2,
        )
    )
    old_candidate = row_complex(
        result_5212["candidate_K_mu"]["value"]
    )
    control_local_mean = float(
        zm0p6_local_weight * np.mean(control_array.real)
    )
    adjusted_candidate = complex(
        old_candidate.real + 8.0 * control_local_mean,
        old_candidate.imag,
    )
    coefficient_projection = {
        "raw_candidate_K_mu": complex_row(old_candidate),
        "raw_real_standard_error": float(
            result_5212["candidate_K_mu"]["real_standard_error"]
        ),
        "retrospective_controlled_candidate_K_mu": complex_row(
            adjusted_candidate
        ),
        "retrospective_controlled_real_standard_error": (
            8.0 * adjusted_hhh_real_error
        ),
        "raw_topological_local_standard_error": (
            raw_topological_local_se
        ),
        "controlled_topological_local_standard_error": (
            adjusted_topological_local_se
        ),
        "control_local_sample_mean": control_local_mean,
        "valid_for_numeric_UV_claim": False,
    }
    control_real_summary = scalar_summary(control_array.real)
    control_mean_in_standard_errors = abs(control_real_summary["mean"]) / max(
        control_real_summary["standard_error"], 1.0e-300
    )
    result_5010 = read_json(RESULT_5010)
    with INTEGRAND_CHECKS_5010.open(newline="", encoding="utf-8") as handle:
        checks_5010 = {
            row["check_id"]: row for row in csv.DictReader(handle)
        }
    soft_partition_residual = float(
        checks_5010["CUT5010_04_soft_sector_partition"]["derived_value"]
    )
    permutation_control = {
        "identity": (
            "C_13=Y[g1+,g3-]-(w1/w3)Y[g1-,g3+], "
            "E[C_13]=0"
        ),
        "partition_weights": (
            "w_i=E_i^-2/sum_j(E_j^-2); "
            "w1/w3=(E3/E1)^2 at the relative residue"
        ),
        "proof": (
            "the identical-graviton phase-space measure and direct KLT "
            "state sum are invariant under g1<->g3; the source-pole "
            "family maps to its permuted family and 3w3 maps to 3w1"
        ),
        "phase_space_jacobian": (
            "under g1<->g3, x3'=E1 and physical-measure invariance gives "
            "dq'=E3/E1 dq; the x3' Jacobian product returns x3, so only "
            "w1/w3 multiplies the permuted direct family"
        ),
        "rootwise_weighting": (
            "each reciprocal root is multiplied by (E3/E1)^2 before its "
            "winding-weighted residue is summed"
        ),
        "dominant_pair_row_count": len(dominant_pair_rows),
        "permuted_pair_row_count": len(permuted_pair_rows),
        "all_control_pairs_reciprocal_safe": True,
        "all_control_sources_direct": all(
            "subtraction:" not in row["family_signature"]
            for row in dominant_pair_rows + permuted_pair_rows
        ),
        "all_partition_ratios_finite": all(
            finite_complex(
                complex(
                    float(row["first_permutation_partition_ratio_real"]),
                    float(row["first_permutation_partition_ratio_imaginary"]),
                )
            )
            and finite_complex(
                complex(
                    float(row["second_permutation_partition_ratio_real"]),
                    float(row["second_permutation_partition_ratio_imaginary"]),
                )
            )
            for row in permuted_pair_rows
        ),
        "source_S3_residual_5010": float(
            result_5010["integrand"]["hhh_S3_residual"]
        ),
        "source_soft_partition_residual_5010": float(
            soft_partition_residual
        ),
        "subtraction_contamination": False,
        "coefficient_fitted": False,
        "real_control_coefficient": 1.0,
        "imaginary_control_coefficient": 0.0,
        "control_distribution": {
            "real": control_real_summary,
            "imaginary": scalar_summary(control_array.imag),
        },
        "control_mean_in_standard_errors": control_mean_in_standard_errors,
        "A00_real_variance": a00_variance,
        "full_zm0p6_real_variance": zm0p6_variance,
        "topological_local_real_variance": local_variance,
        "coefficient_projection": coefficient_projection,
        "dominant_family_global_rank": dominant_rank,
        "leave_one_event_out_selection": leave_one_out_ranks,
        "leave_one_event_out_selection_unanimous": all(
            row["training_selection_matches"]
            for row in leave_one_out_ranks
        ),
        "retrospective_design_gate": bool(
            a00_variance["standard_deviation_ratio"] < 0.5
            and local_variance["standard_deviation_ratio"] < 0.75
            and all(
                row["training_selection_matches"]
                for row in leave_one_out_ranks
            )
        ),
        "fresh_independent_pilot_required": True,
        "valid_for_numeric_UV_claim": False,
    }

    write_csv(PAIR_ROWS_CSV, pair_csv_rows)
    write_csv(FAMILY_ROWS_CSV, family_csv_rows)
    write_csv(EVENT_ROWS_CSV, event_csv_rows)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REPLAY_REVISION,
        "replay_config_digest": replay_config_digest,
        "source_config_digest": config["config_digest"],
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "replayed_job_count": len(replayed),
        "expected_replayed_job_count": 2 * len(expected_seeds),
        "all_replays_reproduce_source": all(
            float(row["reproduction_relative_residual"]) <= 1.0e-9
            for row in replayed
        ),
        "maximum_reproduction_relative_residual": max(
            float(row["reproduction_relative_residual"])
            for row in replayed
        ),
        "maximum_event_family_closure": max(
            float(row["family_closure"]) for row in event_csv_rows
        ),
        "A00_physical_weight_at_zm0p6": A00_PHYSICAL_WEIGHT,
        "A00_physical_real_distribution": scalar_summary(
            total_array.real
        ),
        "A00_physical_imaginary_distribution": scalar_summary(
            total_array.imag
        ),
        "family_count": len(signatures),
        "family_diagnostics": family_diagnostics,
        "dominant_family": family_diagnostics[0],
        "permutation_control": permutation_control,
        "next_action": (
            "if the exact permutation-control gate passes, lock it before "
            "fresh independent topological events; otherwise reject it"
        ),
        "control_variate_derived": True,
        "control_variate_retrospective_gate": permutation_control[
            "retrospective_design_gate"
        ],
        "fresh_independent_control_pilot_required": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(AUDIT_JSON, result)
    return result


def write_checkpoint_outputs(result: dict[str, Any]) -> dict[str, Any]:
    control = result["permutation_control"]
    required_sources = (
        SCRIPT_5212,
        GATE_5213,
        EVENT_ROWS_5212,
        RESULT_5212,
        RESULT_5010,
        INTEGRAND_CHECKS_5010,
        DOCUMENT_5010,
        SCRIPT_5017,
        RUN_SOURCE / "config.json",
    )
    source_rows = [
        {
            "path": str(path),
            "exists": path.exists(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in required_sources
    ]
    formal_digest = tree_digest(FORMAL)
    checks = [
        (
            "all_cited_source_paths_exist",
            all(row["exists"] for row in source_rows),
            str(sum(row["exists"] for row in source_rows)),
        ),
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "locked_5212_source_configuration_retained",
            result["source_config_digest"] == SOURCE_CONFIG_DIGEST,
            result["source_config_digest"],
        ),
        (
            "all_24_A00_jobs_replayed_exactly",
            result["replayed_job_count"]
            == result["expected_replayed_job_count"]
            == 24
            and result["all_replays_reproduce_source"]
            and result["maximum_reproduction_relative_residual"] <= 1.0e-9,
            str(result["maximum_reproduction_relative_residual"]),
        ),
        (
            "event_family_decomposition_closes",
            result["maximum_event_family_closure"] <= 1.0e-9,
            str(result["maximum_event_family_closure"]),
        ),
        (
            "source_identical_graviton_S3_gate_retained",
            control["source_S3_residual_5010"] < 1.0e-9,
            str(control["source_S3_residual_5010"]),
        ),
        (
            "source_soft_partition_gate_retained",
            control["source_soft_partition_residual_5010"] <= 1.0e-15,
            str(control["source_soft_partition_residual_5010"]),
        ),
        (
            "control_source_families_are_direct_and_reciprocal_safe",
            control["all_control_pairs_reciprocal_safe"]
            and control["all_control_sources_direct"]
            and not control["subtraction_contamination"],
            json.dumps(
                {
                    "dominant_rows": control["dominant_pair_row_count"],
                    "permuted_rows": control["permuted_pair_row_count"],
                },
                sort_keys=True,
            ),
        ),
        (
            "partition_ratios_are_finite_and_rootwise",
            control["all_partition_ratios_finite"]
            and "each reciprocal root" in control["rootwise_weighting"],
            control["rootwise_weighting"],
        ),
        (
            "control_coefficient_is_symmetry_fixed_not_fitted",
            not control["coefficient_fitted"]
            and control["real_control_coefficient"] == 1.0
            and control["imaginary_control_coefficient"] == 0.0,
            "real=1; imaginary=0",
        ),
        (
            "dominant_family_is_global_rank_one",
            control["dominant_family_global_rank"] == 1,
            str(control["dominant_family_global_rank"]),
        ),
        (
            "dominant_family_selection_is_leave_one_out_stable",
            control["leave_one_event_out_selection_unanimous"],
            str(control["leave_one_event_out_selection_unanimous"]),
        ),
        (
            "control_sample_mean_is_zero_compatible",
            control["control_mean_in_standard_errors"] <= 2.0,
            str(control["control_mean_in_standard_errors"]),
        ),
        (
            "A00_real_variance_reduction_gate",
            control["A00_real_variance"]["standard_deviation_ratio"] < 0.5,
            str(
                control["A00_real_variance"]["standard_deviation_ratio"]
            ),
        ),
        (
            "topological_local_real_variance_reduction_gate",
            control["topological_local_real_variance"][
                "standard_deviation_ratio"
            ]
            < 0.75,
            str(
                control["topological_local_real_variance"][
                    "standard_deviation_ratio"
                ]
            ),
        ),
        (
            "retrospective_design_gate_passes",
            control["retrospective_design_gate"],
            str(control["retrospective_design_gate"]),
        ),
        (
            "fresh_independent_pilot_remains_required",
            control["fresh_independent_pilot_required"]
            and result["fresh_independent_control_pilot_required"],
            "retrospective efficiency is not promoted",
        ),
        (
            "checkpoint_remains_nonclaim",
            not result["valid_for_numeric_UV_claim"]
            and not result["valid_for_local_GR_claim"]
            and not result["valid_for_full_MTS_claim"],
            "numeric_UV=false; local_GR=false; full_MTS=false",
        ),
    ]
    result["formalization_workbench_tree_sha256"] = formal_digest
    result["source_files"] = source_rows
    result["replay_job_tree_sha256"] = tree_digest(REPLAY_JOBS)
    result["checks"] = [
        {
            "check": name,
            "passed": bool(passed),
            "detail": detail,
            "status": "PASS" if passed else "FAIL",
            "checkpoint_marker": MARKER,
        }
        for name, passed, detail in checks
    ]
    result["passed"] = all(passed for _, passed, _ in checks)
    result["fresh_independent_control_pilot_authorized"] = result["passed"]
    result["next_action"] = (
        "freeze this coefficient-free permutation control and run it on "
        "fresh independent topological seeds before any larger coefficient run"
    )
    atomic_json(AUDIT_JSON, result)
    write_csv(VALIDATION_CSV, result["checks"])

    raw = control["topological_local_real_variance"]
    projection = control["coefficient_projection"]
    document = f"""# 5214 - A00 identical-graviton permutation control variate

## Decision

The dominant `A00` source-pole fluctuation now has a derived, coefficient-free
control variate. On the locked twelve-event `5212` sample it cuts the real
topological-local standard deviation by a factor
`{raw['standard_deviation_ratio']:.9g}` and passes the retrospective design
gate. This authorizes a fresh independent pilot; it does not establish the UV
coefficient.

## Exact identity

The identical-graviton cut is partitioned by

`w_i = E_i^-2 / sum_j E_j^-2`

and the working chart carries `3 w_3`. The dominant direct source family

`Y_13 = Y[g1+,g3-]`

is mapped by the exact `g1 <-> g3` permutation to

`Y_31 = Y[g1-,g3+]`.

The physical phase-space measure is invariant. In the sequential chart,
`x_3'=E_1` and the induced coordinate Jacobian obeys
`dq'=(E_3/E_1)dq`; hence the exchanged soft-energy factor and Jacobian return
the original `x_3` measure. The only remaining local reweighting is

`w_1/w_3 = (E_3/E_1)^2`.

Therefore

`C_13 = Y_13 - (w_1/w_3) Y_31`, with `E[C_13]=0`.

The coefficient is fixed to one by permutation symmetry; it is not fitted to
the twelve events. Both families are direct terms, so the soft subtraction is
not imported into the identity. The imaginary component remains uncontrolled
because the earlier imaginary-reflection proposal was rejected.

## Reciprocal-root implementation

The ratio `(E_3/E_1)^2` is inserted before residue summation. Each reciprocal
root receives its own analytic ratio and winding:

`R_w = kappa_R [r_+ n_+ Res_+ + r_- n_- Res_-]`.

This avoids the invalid shortcut of multiplying an already reciprocal-reduced
pair by only one root's ratio. All `{control['permuted_pair_row_count']}`
permuted-family rows and `{control['dominant_pair_row_count']}` dominant-family
rows are reciprocal-safe, direct, and finite.

## Locked retrospective result

- Replayed A00 jobs: `{result['replayed_job_count']}/24`.
- Maximum replay residual: `{result['maximum_reproduction_relative_residual']:.3e}`.
- Source-family count: `{result['family_count']}`.
- Dominant-family covariance fraction: `{result['dominant_family']['covariance_fraction_of_total_variance']:.9g}`.
- A00 real SD ratio: `{control['A00_real_variance']['standard_deviation_ratio']:.9g}`.
- Full `z=-0.6` real SD ratio: `{control['full_zm0p6_real_variance']['standard_deviation_ratio']:.9g}`.
- Topological-local real SD ratio: `{raw['standard_deviation_ratio']:.9g}`.
- Topological-local variance reduction: `{raw['variance_reduction_factor']:.9g}`.
- Control mean in standard errors: `{control['control_mean_in_standard_errors']:.9g}`.
- Leave-one-event-out source-family selection unanimous:
  `{control['leave_one_event_out_selection_unanimous']}`.
- Retrospective candidate:
  `K_mu={projection['retrospective_controlled_candidate_K_mu']['real']:.9g}`
  `{projection['retrospective_controlled_candidate_K_mu']['imaginary']:+.9g} i`
  with real standard error
  `{projection['retrospective_controlled_real_standard_error']:.9g}`.

The candidate shift is diagnostic only. A control with exactly zero ensemble
mean can move a small retrospective sample substantially; the fresh pilot is
the required bias and efficiency test.

## Claim boundary

This checkpoint proves the control identity and demonstrates retrospective
variance reduction. It does not prove tail convergence, a numerical
two-loop coefficient, local GR, the galaxy branch, or full MTS. Numeric-UV,
local-GR and full-MTS claim flags remain false.

## Next experiment

Freeze the source signatures, rootwise ratio, coefficient `1`, real-only
application, and acceptance thresholds before drawing fresh topological
seeds. Run a small independent pilot first; scale only if it reproduces the
variance reduction without a detectable nonzero control mean.

## Machine-readable evidence

- `{AUDIT_JSON}`
- `{PAIR_ROWS_CSV}`
- `{FAMILY_ROWS_CSV}`
- `{EVENT_ROWS_CSV}`
- `{VALIDATION_CSV}`
- `{PROVENANCE}`
"""
    atomic_text(DOCUMENT, document)

    provenance_lines = [
        "# 5214 provenance",
        "",
        "## Sources",
        "",
    ]
    provenance_lines.extend(
        f"- `{row['path']}` - `{row['sha256']}`" for row in source_rows
    )
    provenance_lines.extend(
        [
            "",
            "## Replay",
            "",
            f"- Replayed pair jobs: `{result['replayed_job_count']}`.",
            f"- Replay tree SHA-256: `{result['replay_job_tree_sha256']}`.",
            f"- Locked source config digest: `{result['source_config_digest']}`.",
            "",
            "## Outputs",
            "",
            f"- `{AUDIT_JSON}`",
            f"- `{PAIR_ROWS_CSV}`",
            f"- `{FAMILY_ROWS_CSV}`",
            f"- `{EVENT_ROWS_CSV}`",
            f"- `{VALIDATION_CSV}`",
            f"- `{DOCUMENT}`",
            "",
            "All outputs are private, retrospective, and non-claim.",
        ]
    )
    atomic_text(PROVENANCE, "\n".join(provenance_lines) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("audit", "analyse"), default="audit"
    )
    arguments = parser.parse_args()

    config = read_json(RUN_SOURCE / "config.json")
    if config["config_digest"] != SOURCE_CONFIG_DIGEST:
        raise RuntimeError("locked 5212 source configuration changed")
    if read_json(GATE_5213)["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("formalization baseline changed")
    replay_config_digest = replay_digest(config)
    seeds = tuple(
        int(value)
        for value in config["two_stratum_contract"]["topological_seeds"]
    )

    M5212.source_separated_cluster_gate()
    M5212.M5077.certified_primary_catalog = M5212.certified_5212_catalog
    M5212.M5077.M5085.CertifiedRemovableGlobalExtension = (
        M5212.AdaptiveRemovableGlobalExtension
    )
    M5212.M5077.install_history_invariant_breakpoints(
        M5212.M5077.M5036.N5030
    )
    manager = M5212.M5077.CentralTopologyManager(RUN_SOURCE, config)
    replayed: list[dict[str, Any]] = []
    for seed in seeds:
        for epsilon_id in ("E020", "E040"):
            path = (
                REPLAY_JOBS
                / f"TOP__{epsilon_id}__S{seed}_N0000__A00__primary24.json"
            )
            if arguments.mode == "analyse" and not path.exists():
                raise RuntimeError(f"missing replay job: {path}")
            replayed.append(
                replay_job(
                    manager,
                    config,
                    replay_config_digest,
                    epsilon_id,
                    seed,
                )
            )
    result = write_checkpoint_outputs(
        analyse(config, replay_config_digest, replayed)
    )
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "replayed_job_count": result["replayed_job_count"],
                "maximum_reproduction_relative_residual": result[
                    "maximum_reproduction_relative_residual"
                ],
                "family_count": result["family_count"],
                "dominant_family": result["dominant_family"],
                "permutation_control": result["permutation_control"],
                "control_variate_derived": True,
                "control_variate_retrospective_gate": result[
                    "control_variate_retrospective_gate"
                ],
                "valid_for_numeric_UV_claim": False,
                "passed": result["passed"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["passed"]:
        raise RuntimeError("5214 permutation-control gate failed")


if __name__ == "__main__":
    main()
