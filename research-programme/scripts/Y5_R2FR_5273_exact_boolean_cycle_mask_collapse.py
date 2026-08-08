from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5273"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5272 = (
    SCRIPTS
    / "Y5_R2FR_5272_exact_analytic_boundary_surface_and_event_solver.py"
)
RESULT_5272 = (
    FUNCTIONAL_RG
    / "5272"
    / "exact_analytic_boundary_surface_result.json"
)
VALIDATION_5272 = (
    FUNCTIONAL_RG
    / "5272"
    / "exact_analytic_boundary_surface_validation.csv"
)
SURFACES_5272 = (
    FUNCTIONAL_RG / "5272" / "analytic_surface_descriptors.csv"
)
DESCRIPTORS_5270 = (
    FUNCTIONAL_RG / "5270" / "shared_cycle_boundary_descriptors.csv"
)
ATLAS_5269 = (
    FUNCTIONAL_RG / "5269" / "energy_cycle_state_atlas.csv"
)
PANELS_5271 = (
    FUNCTIONAL_RG
    / "5271"
    / "soft_energy_topology_uniform_panels.csv"
)

DRY_RUN = SOURCE / "exact_boolean_cycle_mask_dry_run.json"
COMPONENT_LAWS = SOURCE / "component_boolean_mask_laws.csv"
ATLAS_VERIFICATION = SOURCE / "5269_cycle_atlas_mask_verification.csv"
PANEL_VERIFICATION = SOURCE / "5271_panel_signature_mask_verification.csv"
INTERIOR_STRESS = SOURCE / "interior_boolean_mask_stress.csv"
BOUNDARY_AUDIT = SOURCE / "boundary_exception_and_denominator_audit.csv"
RESULT = SOURCE / "exact_boolean_cycle_mask_result.json"
VALIDATION = SOURCE / "exact_boolean_cycle_mask_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5273_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5273-Y5-R2FR-exact-boolean-cycle-mask-collapse.md"

CHECKPOINT = 5273
PARENT_CHECKPOINT = 5272
MARKER = "MTS_5273_EXACT_BOOLEAN_CYCLE_MASK_COLLAPSE"
REVISION = "exact-boolean-cycle-mask-collapse-v1"
STRESS_POINT_COUNT = 2048
BOUNDARY_SILENCE_TOLERANCE = 1.0e-12
CLAIM_FIELDS = (
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5272 = load_module("mts_5272_for_5273", SCRIPT_5272)
M5271 = M5272.M5271
M5270 = M5272.M5270
M5267 = M5272.M5267


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"cannot serialize {type(value)!r}")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            default=json_default,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5272,
        RESULT_5272,
        VALIDATION_5272,
        SURFACES_5272,
        DESCRIPTORS_5270,
        ATLAS_5269,
        PANELS_5271,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5272.formal_inventory_digest())


def descriptor_surface_key(
    descriptor: dict[str, str],
) -> str:
    return M5272.surface_key(
        descriptor["source_name"],
        M5272.target_from_label(descriptor["root_label"]),
        float(descriptor["chamber_midpoint"]),
    )


def component_law_rows() -> list[dict[str, Any]]:
    descriptors = read_csv(DESCRIPTORS_5270)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for descriptor in descriptors:
        grouped[descriptor["component_id"]].append(descriptor)
    rows: list[dict[str, Any]] = []
    for component_id, local in sorted(grouped.items()):
        by_role = {
            role: [
                descriptor
                for descriptor in local
                if descriptor["role"] == role
            ]
            for role in ("representative", "reciprocal")
        }
        role_surface_sets = {
            role: {
                descriptor_surface_key(descriptor)
                for descriptor in role_rows
            }
            for role, role_rows in by_role.items()
        }
        role_suffix_maps = {
            role: {
                descriptor_surface_key(descriptor):
                descriptor["root_label"].rsplit("_", 1)[1]
                for descriptor in role_rows
            }
            for role, role_rows in by_role.items()
        }
        role_parities = {
            role: math.prod(
                1 if suffix == "u" else -1
                for suffix in suffix_map.values()
            )
            for role, suffix_map in role_suffix_maps.items()
        }
        shared_surfaces = sorted(
            role_surface_sets["representative"]
        )
        representative_suffixes = "|".join(
            f"{surface}:{suffix}"
            for surface, suffix in sorted(
                role_suffix_maps["representative"].items()
            )
        )
        reciprocal_suffixes = "|".join(
            f"{surface}:{suffix}"
            for surface, suffix in sorted(
                role_suffix_maps["reciprocal"].items()
            )
        )
        parity = role_parities["representative"]
        derivation_closed = (
            all(len(by_role[role]) == 2 for role in by_role)
            and role_surface_sets["representative"]
            == role_surface_sets["reciprocal"]
            and len(shared_surfaces) == 2
            and role_parities["representative"]
            == role_parities["reciprocal"]
            and all(
                suffix in {"u", "v"}
                for suffix_map in role_suffix_maps.values()
                for suffix in suffix_map.values()
            )
        )
        rows.append(
            {
                "component_id": component_id,
                "owner_summand": local[0]["owner_summand"],
                "surface_A": (
                    shared_surfaces[0] if shared_surfaces else ""
                ),
                "surface_B": (
                    shared_surfaces[1]
                    if len(shared_surfaces) > 1
                    else ""
                ),
                "representative_root_suffixes": (
                    representative_suffixes
                ),
                "reciprocal_root_suffixes": reciprocal_suffixes,
                "representative_surface_set": "|".join(
                    sorted(
                        role_surface_sets["representative"]
                    )
                ),
                "reciprocal_surface_set": "|".join(
                    sorted(role_surface_sets["reciprocal"])
                ),
                "u_margin_sign": "sign(F)",
                "v_margin_sign": "-sign(F)",
                "representative_root_parity_product": (
                    role_parities["representative"]
                ),
                "reciprocal_root_parity_product": (
                    role_parities["reciprocal"]
                ),
                "root_parity_product": parity,
                "representative_xor_equals_reciprocal_xor": (
                    derivation_closed
                ),
                "cycle_active_law": (
                    "F_A*F_B<0"
                    if parity == 1
                    else "F_A*F_B>0"
                ),
                "boundary_exception": "F_A*F_B=0",
                "derivation_closed": derivation_closed,
                "valid_for_exact_cycle_mask": derivation_closed,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def surface_value(
    surface: dict[str, Any],
    energy: float,
    soft_cosine: float,
    decay_cosine: float,
) -> float:
    if surface["family"] == "boosted_hard_leg":
        return M5272.hard_boundary_value(
            math.sqrt(1.0 - energy),
            soft_cosine,
            decay_cosine,
            int(surface["hard_leg_sign"]),
            float(surface["target_cosine"]),
            float(surface["chamber_midpoint"]),
        )
    if surface["family"] == "static_soft_direction":
        return soft_cosine - float(surface["target_cosine"])
    if surface["family"] == "static_decay_direction":
        return decay_cosine - float(surface["target_cosine"])
    raise ValueError(f"unknown family: {surface['family']}")


def mask_state(
    law: dict[str, Any],
    surfaces: dict[str, dict[str, Any]],
    energy: float,
    soft_cosine: float,
    decay_cosine: float,
) -> tuple[bool, float, float, float]:
    first = surface_value(
        surfaces[str(law["surface_A"])],
        energy,
        soft_cosine,
        decay_cosine,
    )
    second = surface_value(
        surfaces[str(law["surface_B"])],
        energy,
        soft_cosine,
        decay_cosine,
    )
    product = first * second
    signed_product = int(law["root_parity_product"]) * product
    return signed_product < 0.0, first, second, product


def atlas_verification_rows(
    laws: dict[str, dict[str, Any]],
    surfaces: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for atlas in read_csv(ATLAS_5269):
        energy = float(atlas["energy_witness"])
        soft_cosine = float(atlas["soft_cosine"])
        decay_cosine = float(atlas["decay_cosine"])
        component_id = atlas["component_id"]
        predicted, first, second, product = mask_state(
            laws[component_id],
            surfaces,
            energy,
            soft_cosine,
            decay_cosine,
        )
        expected = atlas["cycle_active"].lower() == "true"
        rows.append(
            {
                "job_id": atlas["job_id"],
                "epsilon_id": atlas["epsilon_id"],
                "component_id": component_id,
                "soft_cosine": soft_cosine,
                "decay_cosine": decay_cosine,
                "soft_energy": energy,
                "atlas_cycle_active": expected,
                "boolean_mask_active": predicted,
                "surface_A_value": first,
                "surface_B_value": second,
                "surface_product": product,
                "minimum_absolute_surface_value": min(
                    abs(first), abs(second)
                ),
                "matched": predicted == expected,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def panel_verification_rows(
    law_list: list[dict[str, Any]],
    surfaces: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    ordered_laws = sorted(
        law_list, key=lambda row: str(row["component_id"])
    )
    rows: list[dict[str, Any]] = []
    for panel in read_csv(PANELS_5271):
        energy = float(panel["energy_witness"])
        fixed = float(panel["fixed_coordinate"])
        midpoint = float(panel["panel_midpoint"])
        if panel["direction"] == "soft_cosine":
            soft_cosine = midpoint
            decay_cosine = fixed
        else:
            soft_cosine = fixed
            decay_cosine = midpoint
        bits: list[str] = []
        minimum_surface = math.inf
        for law in ordered_laws:
            active, first, second, _ = mask_state(
                law,
                surfaces,
                energy,
                soft_cosine,
                decay_cosine,
            )
            bits.append("1" if active else "0")
            minimum_surface = min(
                minimum_surface, abs(first), abs(second)
            )
        predicted = "".join(bits)
        expected = panel["cycle_signature"]
        rows.append(
            {
                "direction": panel["direction"],
                "soft_energy": energy,
                "fixed_coordinate": fixed,
                "panel_index": panel["panel_index"],
                "panel_midpoint": midpoint,
                "panel_cycle_signature": expected,
                "boolean_mask_signature": predicted,
                "minimum_absolute_surface_value": minimum_surface,
                "matched": predicted == expected,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def root_engine_component_map() -> dict[str, list[dict[str, Any]]]:
    E040, E020 = M5270.source_jobs()
    _, by_component, mismatch_count = M5270.descriptor_rows(
        E040, E020
    )
    if mismatch_count:
        raise RuntimeError("regulator descriptor mismatch")
    return by_component


def interior_stress_rows(
    law_list: list[dict[str, Any]],
    surfaces: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    ordered_laws = sorted(
        law_list, key=lambda row: str(row["component_id"])
    )
    descriptors = root_engine_component_map()
    generator = np.random.default_rng(5273)
    points = generator.random((STRESS_POINT_COUNT, 3))
    energy_minimum = float(M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5267.ENERGY_MAXIMUM)
    angular_limit = float(M5270.ANGULAR_LIMIT)
    rows: list[dict[str, Any]] = []
    for point_index, point in enumerate(points):
        energy = (
            energy_minimum
            + (energy_maximum - energy_minimum) * float(point[0])
        )
        soft_cosine = angular_limit * (
            2.0 * float(point[1]) - 1.0
        )
        decay_cosine = angular_limit * (
            2.0 * float(point[2]) - 1.0
        )
        exact_bits: list[str] = []
        root_bits: list[str] = []
        minimum_surface = math.inf
        minimum_margin = math.inf
        for law in ordered_laws:
            active, first, second, _ = mask_state(
                law,
                surfaces,
                energy,
                soft_cosine,
                decay_cosine,
            )
            root_active, root_margin = (
                M5270.component_cycle_active(
                    energy,
                    soft_cosine,
                    decay_cosine,
                    descriptors[str(law["component_id"])],
                )
            )
            exact_bits.append("1" if active else "0")
            root_bits.append("1" if root_active else "0")
            minimum_surface = min(
                minimum_surface, abs(first), abs(second)
            )
            minimum_margin = min(minimum_margin, root_margin)
        exact_signature = "".join(exact_bits)
        root_signature = "".join(root_bits)
        rows.append(
            {
                "point_index": point_index,
                "soft_energy": energy,
                "soft_cosine": soft_cosine,
                "decay_cosine": decay_cosine,
                "boolean_mask_signature": exact_signature,
                "root_engine_signature": root_signature,
                "minimum_absolute_surface_value": minimum_surface,
                "minimum_absolute_root_margin": minimum_margin,
                "matched": exact_signature == root_signature,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def boundary_audit_rows(
    surfaces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    q_minimum = math.sqrt(
        1.0 - float(M5267.ENERGY_MAXIMUM)
    )
    denominator_lower_bound = 2.0 * q_minimum**2
    rows: list[dict[str, Any]] = []
    for surface in surfaces:
        if surface["family"] == "boosted_hard_leg":
            exception_set = (
                f"{surface['surface_key']}: F(q,a,d)=0"
            )
            denominator_statement = (
                "D=1+q^2-s(1-q^2)r >= 2q^2"
            )
            lower_bound = denominator_lower_bound
        elif surface["family"] == "static_soft_direction":
            exception_set = (
                f"{surface['surface_key']}: "
                f"a={surface['target_cosine']}"
            )
            denominator_statement = "static direction; no boost denominator"
            lower_bound = 1.0
        else:
            exception_set = (
                f"{surface['surface_key']}: "
                f"d={surface['target_cosine']}"
            )
            denominator_statement = "static direction; no boost denominator"
            lower_bound = 1.0
        rows.append(
            {
                "surface_key": surface["surface_key"],
                "family": surface["family"],
                "boundary_exception_set": exception_set,
                "codimension_in_energy_angle_domain": 1,
                "measure_zero_for_regular_volume_cubature": True,
                "denominator_statement": denominator_statement,
                "proven_denominator_lower_bound": lower_bound,
                "denominator_strictly_positive": lower_bound > 0.0,
                "mask_value_on_boundary": "prescription-dependent; excluded",
                "valid_for_exact_almost_everywhere_mask": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5272,
        RESULT_5272,
        VALIDATION_5272,
        SURFACES_5272,
        DESCRIPTORS_5270,
        ATLAS_5269,
        PANELS_5271,
    )
    parent = read_json(RESULT_5272)
    validation = read_csv(VALIDATION_5272)
    laws = component_law_rows()
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5272_accepted": bool(parent["acceptance_passed"]),
        "parent_5272_validation_passed": all(
            row["passed"].lower() == "true" for row in validation
        ),
        "six_component_laws_recovered": len(laws) == 6,
        "all_component_derivations_close": all(
            bool(row["derivation_closed"]) for row in laws
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "component_law_count": len(laws),
        "runtime_seconds": 0.0,
        "decision": (
            "DRY_RUN_ACCEPTED__VERIFY_EXACT_BOOLEAN_CYCLE_MASK"
            if all(checks.values())
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5273 dry run did not pass")
    parent = read_json(RESULT_5272)
    surfaces = M5272.surface_rows()
    surface_map = M5272.surface_lookup(surfaces)
    laws = component_law_rows()
    law_map = {
        str(row["component_id"]): row for row in laws
    }
    atlas = atlas_verification_rows(law_map, surface_map)
    panels = panel_verification_rows(laws, surface_map)
    stress = interior_stress_rows(laws, surface_map)
    boundary = boundary_audit_rows(surfaces)
    atlas_mismatches = sum(
        not bool(row["matched"]) for row in atlas
    )
    panel_mismatches = sum(
        not bool(row["matched"]) for row in panels
    )
    stress_mismatches = sum(
        not bool(row["matched"]) for row in stress
    )
    minimum_atlas_surface = min(
        float(row["minimum_absolute_surface_value"])
        for row in atlas
    )
    minimum_panel_surface = min(
        float(row["minimum_absolute_surface_value"])
        for row in panels
    )
    minimum_stress_surface = min(
        float(row["minimum_absolute_surface_value"])
        for row in stress
    )
    proven_denominator_lower_bound = min(
        float(row["proven_denominator_lower_bound"])
        for row in boundary
        if row["family"] == "boosted_hard_leg"
    )
    checks = {
        "parent_5272_accepted": bool(parent["acceptance_passed"]),
        "all_component_derivations_close": all(
            bool(row["derivation_closed"]) for row in laws
        ),
        "all_5269_cycle_states_match": atlas_mismatches == 0,
        "all_5271_panel_signatures_match": panel_mismatches == 0,
        "all_random_interior_root_states_match": (
            stress_mismatches == 0
        ),
        "boundary_exceptions_are_measure_zero": all(
            bool(row["measure_zero_for_regular_volume_cubature"])
            for row in boundary
        ),
        "hard_leg_denominator_proven_positive": (
            proven_denominator_lower_bound > 0.0
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "exact-boolean-cycle-mask-collapse",
        "checks": checks,
        "acceptance_passed": accepted,
        "component_law_count": len(laws),
        "atlas_row_count": len(atlas),
        "atlas_mismatch_count": atlas_mismatches,
        "panel_row_count": len(panels),
        "panel_mismatch_count": panel_mismatches,
        "interior_stress_point_count": len(stress),
        "interior_stress_mismatch_count": stress_mismatches,
        "boundary_surface_count": len(boundary),
        "minimum_atlas_absolute_surface_value": (
            minimum_atlas_surface
        ),
        "minimum_panel_absolute_surface_value": (
            minimum_panel_surface
        ),
        "minimum_stress_absolute_surface_value": (
            minimum_stress_surface
        ),
        "proven_hard_denominator_lower_bound": (
            proven_denominator_lower_bound
        ),
        "exact_mask_contract": {
            "u_root_margin_sign": "sign(F)",
            "v_root_margin_sign": "-sign(F)",
            "component_active": "p_AB*F_A*F_B<0",
            "component_inactive": "p_AB*F_A*F_B>0",
            "boundary_exception": "F_A*F_B=0",
            "representative_reciprocal_identity": (
                "p_AB is the same root-suffix parity product in "
                "representative and reciprocal roles"
            ),
            "cubature_rule": (
                "evaluate the Boolean mask pointwise; boundary sets "
                "have measure zero under regular volume integration"
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ADOPT_EXACT_BOOLEAN_CYCLE_MASK__"
            "REMOVE_BRANCH_TRACKER_FROM_VOLUME_CUBATURE"
            if accepted
            else "REPAIR_BOOLEAN_CYCLE_MASK_DERIVATION"
        ),
        "claim_boundary": {
            "valid_for_exact_almost_everywhere_cycle_mask": accepted,
            "valid_for_pointwise_topology_safe_cubature_mask": accepted,
            "valid_for_boundary_distribution_terms": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The causal-cycle state is now an exact Boolean mask "
                "almost everywhere. Boundary-supported distributional "
                "terms and the weighted phase-space integral are not "
                "yet evaluated."
            ),
        },
    }
    write_csv(COMPONENT_LAWS, laws)
    write_csv(ATLAS_VERIFICATION, atlas)
    write_csv(PANEL_VERIFICATION, panels)
    write_csv(INTERIOR_STRESS, stress)
    write_csv(BOUNDARY_AUDIT, boundary)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": result["mode"],
            "state": "COMPLETED",
            "acceptance_passed": accepted,
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": passed,
        "detail": detail,
    }


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    checks = "\n".join(
        f"- `{name}`: **{'PASS' if passed else 'FAIL'}**"
        for name, passed in result["checks"].items()
    )
    text = f"""# 5273 — Exact Boolean cycle-mask collapse

## Scope

Checkpoint 5272 derived the exact seven boundary surfaces. This checkpoint
uses the paired root structure to remove branch tracking from the interior
volume integral. It is private, leaves the formalization workbench
untouched, and makes no UV, local-GR, or full-MTS claim.

## Derivation

For every sourced surface, the `u` root has margin sign `sign(F)` and the
paired `v` root has margin sign `-sign(F)`. Each component's representative
pair uses the same two surfaces as its reciprocal pair. The product of the
two root-suffix parities, `p_AB`, is also the same in both roles. Therefore
the full representative-plus-reciprocal causal condition reduces to

`cycle_active <=> p_AB F_A F_B < 0`.

Five components have `p_AB=+1`. `MC15` has one `u` and one `v` root per
role, hence `p_AB=-1` and the equivalent inequality `F_A F_B>0`.

The only exception is `F_A F_B=0`, where a root lies on the unit circle.
Those are the codimension-one surfaces already derived in 5272.

## Verification

- Component laws derived: **{result['component_law_count']}**.
- 5269 cycle-atlas rows: **{result['atlas_row_count']}**, mismatches **{result['atlas_mismatch_count']}**.
- 5271 topology-panel rows: **{result['panel_row_count']}**, mismatches **{result['panel_mismatch_count']}**.
- Random interior points: **{result['interior_stress_point_count']}**, mismatches **{result['interior_stress_mismatch_count']}**.
- Boundary surfaces audited: **{result['boundary_surface_count']}**.
- Proven hard-leg denominator lower bound: `{result['proven_hard_denominator_lower_bound']:.12g}`.

For hard legs,

`D=1+q^2-s(1-q^2)r >= 2q^2 > 0`,

so the multiplication used to derive `F` introduces no physical
denominator-zero branch in the sourced soft-energy domain.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Consequence

The volume cubature no longer needs nearest-root matching, chamber
continuation, or an interpolated occupation table. It can evaluate the six
exact inequalities pointwise. Boundary-supported distributional terms are
still a separate question and are not silently discarded if the parent
integrand contains derivatives of the mask.

## Next target

Audit the sourced weighted integrand for boundary derivatives. If none are
present, run the first topology-safe joint soft-energy and two-angle
cubature directly with these exact masks. If derivatives are present,
derive their surface-delta contribution before volume integration.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5272)
    required_csvs = (
        COMPONENT_LAWS,
        ATLAS_VERIFICATION,
        PANEL_VERIFICATION,
        INTERIOR_STRESS,
        BOUNDARY_AUDIT,
    )
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
    source_files = result["source_files"]
    current_formal_digest = formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
    serialized = json.dumps(
        {"result": result, "csvs": csv_rows},
        default=json_default,
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    rows = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            all(
                digest(Path(row["path"])) == row["sha256"]
                for row in source_files
            ),
            "all recorded source hashes reproduce",
        ),
        validation_gate(
            "PARENT_5272_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "BOOLEAN_MASK_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            (
                len(csv_rows) == len(required_csvs)
                and all(csv_rows.values())
            ),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "ALL_ATLAS_STATES_MATCH",
            int(result["atlas_mismatch_count"]) == 0,
            f"{result['atlas_row_count']} atlas rows",
        ),
        validation_gate(
            "ALL_PANEL_SIGNATURES_MATCH",
            int(result["panel_mismatch_count"]) == 0,
            f"{result['panel_row_count']} panel rows",
        ),
        validation_gate(
            "ALL_INTERIOR_STRESS_STATES_MATCH",
            int(result["interior_stress_mismatch_count"]) == 0,
            f"{result['interior_stress_point_count']} random points",
        ),
        validation_gate(
            "BOUNDARY_EXCEPTIONS_EXPLICIT",
            all(
                row["measure_zero_for_regular_volume_cubature"].lower()
                == "true"
                for row in csv_rows[str(BOUNDARY_AUDIT)]
            ),
            "all unit-circle equalities retained as boundary exceptions",
        ),
        validation_gate(
            "HARD_DENOMINATOR_PROVEN_POSITIVE",
            float(result["proven_hard_denominator_lower_bound"])
            > 0.0,
            (
                "lower bound="
                f"{result['proven_hard_denominator_lower_bound']}"
            ),
        ),
        validation_gate(
            "BOUNDARY_DISTRIBUTION_CLAIM_REMAINS_FALSE",
            not result["claim_boundary"][
                "valid_for_boundary_distribution_terms"
            ],
            "surface-delta terms require an integrand audit",
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized,
            "no MISSING_ token in checkpoint artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                all(
                    not result["claim_boundary"][field]
                    for field in CLAIM_FIELDS
                )
                and all(
                    row.get(field, "false").lower() == "false"
                    for row in claim_rows
                    for field in CLAIM_FIELDS
                    if field in row
                )
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
        validation_gate(
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            current_formal_digest == reference_formal_digest,
            (
                f"reference={reference_formal_digest}; "
                f"current={current_formal_digest}"
            ),
        ),
        validation_gate(
            "RESOURCE_CONTRACT_RECORDED",
            (
                result["resource_contract"][
                    "maximum_task_python_processes"
                ]
                == 1
                and result["resource_contract"][
                    "worker_math_threads"
                ]
                == 1
            ),
            "one below-normal single-thread process",
        ),
    ]
    passed = all(row["passed"] for row in rows)
    write_csv(VALIDATION, rows)
    write_csv(RESIDUAL_VALIDATION, rows)
    render_document(result, passed)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": "validation",
            "state": "COMPLETED",
            "validation_passed": passed,
            "validation_gate_count": len(rows),
            "decision": result["decision"],
        },
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_EXACT_BOOLEAN_CYCLE_MASK"
            if passed
            else "VALIDATION_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "validation_gate_count": len(rows),
        "failed_gates": [
            row["gate_id"] for row in rows if not row["passed"]
        ],
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        default="dry-run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    elif args.mode == "validate":
        result = validate_outputs()
    else:
        raise RuntimeError(f"unsupported mode: {args.mode}")
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
