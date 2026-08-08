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
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5279"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5278 = (
    SCRIPTS
    / "Y5_R2FR_5278_eight_component_exact_mask_joint_cubature_smoke.py"
)
RESULT_5278 = (
    FUNCTIONAL_RG
    / "5278"
    / "eight_component_joint_cubature_result.json"
)
VALIDATION_5278 = (
    FUNCTIONAL_RG
    / "5278"
    / "eight_component_joint_cubature_validation.csv"
)
NODE_ROWS_5278 = (
    FUNCTIONAL_RG / "5278" / "joint_cubature_node_residues.csv"
)
LIMIT_ROWS_5275 = (
    FUNCTIONAL_RG
    / "5275"
    / "owner_resolved_local_coefficient_limits.csv"
)
TARGET_POINTS_5275 = (
    FUNCTIONAL_RG / "5275" / "high_precision_target_points.csv"
)

DRY_RUN = SOURCE / "algebraic_branch_selector_dry_run.json"
THEOREM_ROWS = SOURCE / "algebraic_branch_selector_theorem.csv"
REPLAY_ROWS = SOURCE / "stored_transport_selector_replay.csv"
STRESS_ROWS = SOURCE / "algebraic_selector_stress.csv"
RESULT = SOURCE / "algebraic_reciprocal_branch_selector_result.json"
VALIDATION = SOURCE / "algebraic_reciprocal_branch_selector_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5279_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5279-Y5-R2FR-algebraic-reciprocal-branch-selector.md"
)

CHECKPOINT = 5279
PARENT_CHECKPOINT = 5278
MARKER = "MTS_5279_ALGEBRAIC_RECIPROCAL_BRANCH_SELECTOR"
REVISION = "algebraic-reciprocal-branch-selector-v1"
REGULATOR_IDS = ("E040", "E020")
COMPONENT_IDS = (
    "MC02",
    "MC03",
    "MC04",
    "MC07",
    "MC08",
    "MC12",
    "MC14",
    "MC15",
)
STRESS_POINT_COUNT = 256
RECIPROCAL_RESIDUAL_LIMIT = 2.0e-8
REPLAY_CHORDAL_LIMIT = 1.0e-12
UNIT_DEGENERACY_FLOOR = 1.0e-10
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


M5278 = load_module("mts_5278_for_5279", SCRIPT_5278)
M5277 = M5278.M5277
M5275 = M5278.M5275
M5274 = M5278.M5274
np = M5278.np


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


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
        SCRIPT_5278,
        RESULT_5278,
        VALIDATION_5278,
        NODE_ROWS_5278,
        LIMIT_ROWS_5275,
        TARGET_POINTS_5275,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5278.formal_inventory_digest())


def chordal_distance(first: complex, second: complex) -> float:
    return float(
        M5274.M5237.M5030.chordal_distance(first, second)
    )


def alternate_separation(
    selected: complex,
    roots: list[complex],
) -> float:
    return min(
        (
            chordal_distance(selected, root)
            for root in roots
            if chordal_distance(selected, root) > 1.0e-14
        ),
        default=1.0,
    )


def algebraic_component_selector(
    event: dict[str, Any],
    scattering_target: complex,
    component: dict[str, Any],
    rationals: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if rationals is None:
        rationals = M5274.M5231.root_rationals(
            event,
            scattering_target,
        )
    representative_labels = M5274.pair_labels(
        component["representative"]
    )
    reciprocal_labels = M5274.pair_labels(
        component["reciprocal"]
    )
    representative_roots = M5274.collision_roots(
        rationals,
        representative_labels,
    )
    reciprocal_roots = M5274.collision_roots(
        rationals,
        reciprocal_labels,
    )
    if not representative_roots or not reciprocal_roots:
        raise RuntimeError(
            f"collision branch disappeared for "
            f"{component['component_id']}"
        )
    representative = max(representative_roots, key=abs)
    reciprocal = min(reciprocal_roots, key=abs)
    reciprocal_residual = abs(
        representative * reciprocal - 1.0
    )
    if abs(representative) >= 1.0:
        selected_role = "representative"
        selected_entry = component["representative"]
        selected_root = representative
        partner_root = reciprocal
    else:
        selected_role = "reciprocal"
        selected_entry = component["reciprocal"]
        selected_root = reciprocal
        partner_root = representative
    return {
        "representative_labels": representative_labels,
        "reciprocal_labels": reciprocal_labels,
        "representative_roots": representative_roots,
        "reciprocal_roots": reciprocal_roots,
        "representative_root": representative,
        "reciprocal_root": reciprocal,
        "reciprocal_residual": float(reciprocal_residual),
        "selected_role": selected_role,
        "selected_entry": selected_entry,
        "selected_labels": M5274.pair_labels(selected_entry),
        "selected_root": selected_root,
        "partner_root": partner_root,
        "selected_unit_margin": abs(
            math.log(max(abs(selected_root), 1.0e-300))
        ),
        "representative_alternate_separation": (
            alternate_separation(
                representative,
                representative_roots,
            )
        ),
        "reciprocal_alternate_separation": (
            alternate_separation(
                reciprocal,
                reciprocal_roots,
            )
        ),
    }


def component_inventory(
    epsilon_id: str,
    source_event: dict[str, Any],
    contract: dict[str, Any],
) -> tuple[complex, dict[str, dict[str, Any]]]:
    target, components, _ = M5274.component_inventory(
        epsilon_id,
        source_event,
        contract,
    )
    return (
        target,
        {
            str(component["component_id"]): component
            for component in components
            if component["component_id"] in COMPONENT_IDS
        },
    )


def theorem_rows() -> list[dict[str, Any]]:
    contract = M5274.M5239.source_contract()
    source_event = M5274.M5239.source_event(contract)
    target, components = component_inventory(
        "E040",
        source_event,
        contract,
    )
    rationals = M5274.M5231.root_rationals(
        source_event,
        target,
    )
    rows: list[dict[str, Any]] = []
    for component_id in COMPONENT_IDS:
        component = components[component_id]
        selection = algebraic_component_selector(
            source_event,
            target,
            component,
            rationals,
        )
        rows.append(
            {
                "component_id": component_id,
                "family": component["family"],
                "owner_summand": component["owner_summand"],
                "representative_pair": "|".join(
                    selection["representative_labels"]
                ),
                "reciprocal_pair": "|".join(
                    selection["reciprocal_labels"]
                ),
                "representative_candidate_rule": (
                    "maximum_modulus_collision_root"
                ),
                "reciprocal_candidate_rule": (
                    "minimum_modulus_collision_root"
                ),
                "outer_selector_rule": (
                    "representative if |R_rep|>=1 else reciprocal"
                ),
                "source_representative_root_count": len(
                    selection["representative_roots"]
                ),
                "source_reciprocal_root_count": len(
                    selection["reciprocal_roots"]
                ),
                "source_reciprocal_residual": selection[
                    "reciprocal_residual"
                ],
                "proof_identity": (
                    "u/v spinor-root dictionary plus reciprocal "
                    "component construction gives "
                    "R_rep R_rec=1"
                ),
                "proof_scope": (
                    "ALMOST_EVERYWHERE_AWAY_FROM_UNIT_AND_"
                    "COLLISION_DEGENERACY_SETS"
                ),
                "valid_for_algebraic_branch_selector": True,
                "valid_for_global_pointwise_branch_theorem": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def replay_5278_rows() -> list[dict[str, Any]]:
    contract = M5274.M5239.source_contract()
    source_event = M5274.M5239.source_event(contract)
    grouped: defaultdict[
        tuple[str, str, str],
        list[dict[str, str]],
    ] = defaultdict(list)
    for row in read_csv(NODE_ROWS_5278):
        grouped[
            (
                row["epsilon_id"],
                row["quadrature_order"],
                row["node_id"],
            )
        ].append(row)
    inventories = {
        epsilon_id: component_inventory(
            epsilon_id,
            source_event,
            contract,
        )
        for epsilon_id in REGULATOR_IDS
    }
    rows: list[dict[str, Any]] = []
    for key in sorted(grouped):
        epsilon_id, order, node_id = key
        local = grouped[key]
        event = {
            coordinate: float(local[0][coordinate])
            for coordinate in (
                "soft_energy",
                "soft_cosine",
                "decay_cosine",
            )
        }
        target, components = inventories[epsilon_id]
        rationals = M5274.M5231.root_rationals(event, target)
        for stored in local:
            component_id = stored["component_id"]
            selection = algebraic_component_selector(
                event,
                target,
                components[component_id],
                rationals,
            )
            stored_root = complex(
                float(stored["relative_root_real"]),
                float(stored["relative_root_imaginary"]),
            )
            distance = chordal_distance(
                selection["selected_root"],
                stored_root,
            )
            rows.append(
                {
                    "source_checkpoint": 5278,
                    "epsilon_id": epsilon_id,
                    "point_id": node_id,
                    "quadrature_order": order,
                    "component_id": component_id,
                    "stored_role": stored["selected_role"],
                    "algebraic_role": selection["selected_role"],
                    "role_agrees": (
                        stored["selected_role"]
                        == selection["selected_role"]
                    ),
                    "root_chordal_distance": distance,
                    "reciprocal_residual": selection[
                        "reciprocal_residual"
                    ],
                    "selected_unit_margin": selection[
                        "selected_unit_margin"
                    ],
                    "representative_alternate_separation": selection[
                        "representative_alternate_separation"
                    ],
                    "reciprocal_alternate_separation": selection[
                        "reciprocal_alternate_separation"
                    ],
                    "selector_reproduces_stored_transport": (
                        distance <= REPLAY_CHORDAL_LIMIT
                        and stored["selected_role"]
                        == selection["selected_role"]
                    ),
                    "valid_for_algebraic_branch_selector": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def replay_5275_rows() -> list[dict[str, Any]]:
    contract = M5274.M5239.source_contract()
    source_event = M5274.M5239.source_event(contract)
    points = {
        row["point_id"]: row
        for row in read_csv(TARGET_POINTS_5275)
    }
    inventories = {
        epsilon_id: component_inventory(
            epsilon_id,
            source_event,
            contract,
        )
        for epsilon_id in REGULATOR_IDS
    }
    rows: list[dict[str, Any]] = []
    for stored in read_csv(LIMIT_ROWS_5275):
        component_id = stored["component_id"]
        if component_id not in COMPONENT_IDS:
            continue
        epsilon_id = stored["epsilon_id"]
        point = points[stored["point_id"]]
        event = {
            coordinate: float(point[coordinate])
            for coordinate in (
                "soft_energy",
                "soft_cosine",
                "decay_cosine",
            )
        }
        target, components = inventories[epsilon_id]
        selection = algebraic_component_selector(
            event,
            target,
            components[component_id],
        )
        stored_root = complex(
            float(stored["relative_root_real"]),
            float(stored["relative_root_imaginary"]),
        )
        distance = chordal_distance(
            selection["selected_root"],
            stored_root,
        )
        rows.append(
            {
                "source_checkpoint": 5275,
                "epsilon_id": epsilon_id,
                "point_id": stored["point_id"],
                "quadrature_order": "",
                "component_id": component_id,
                "stored_role": stored["selected_role"],
                "algebraic_role": selection["selected_role"],
                "role_agrees": (
                    stored["selected_role"]
                    == selection["selected_role"]
                ),
                "root_chordal_distance": distance,
                "reciprocal_residual": selection[
                    "reciprocal_residual"
                ],
                "selected_unit_margin": selection[
                    "selected_unit_margin"
                ],
                "representative_alternate_separation": selection[
                    "representative_alternate_separation"
                ],
                "reciprocal_alternate_separation": selection[
                    "reciprocal_alternate_separation"
                ],
                "selector_reproduces_stored_transport": (
                    distance <= REPLAY_CHORDAL_LIMIT
                    and stored["selected_role"]
                    == selection["selected_role"]
                ),
                "valid_for_algebraic_branch_selector": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def stress_points() -> list[dict[str, Any]]:
    generator = np.random.default_rng(CHECKPOINT)
    samples = generator.random((STRESS_POINT_COUNT, 3))
    energy_minimum = float(M5274.M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5274.M5267.ENERGY_MAXIMUM)
    angular_limit = float(M5274.M5270.ANGULAR_LIMIT)
    return [
        {
            "point_id": f"S{index:04d}",
            "soft_energy": (
                energy_minimum
                + (energy_maximum - energy_minimum)
                * float(sample[0])
            ),
            "soft_cosine": angular_limit * (
                2.0 * float(sample[1]) - 1.0
            ),
            "decay_cosine": angular_limit * (
                2.0 * float(sample[2]) - 1.0
            ),
        }
        for index, sample in enumerate(samples)
    ]


def stress_rows() -> list[dict[str, Any]]:
    contract = M5274.M5239.source_contract()
    source_event = M5274.M5239.source_event(contract)
    surfaces = M5277.exact_surface_lookup()
    laws = M5278.law_lookup()
    inventories = {
        epsilon_id: component_inventory(
            epsilon_id,
            source_event,
            contract,
        )
        for epsilon_id in REGULATOR_IDS
    }
    rows: list[dict[str, Any]] = []
    for point in stress_points():
        event = {
            coordinate: float(point[coordinate])
            for coordinate in (
                "soft_energy",
                "soft_cosine",
                "decay_cosine",
            )
        }
        for epsilon_id in REGULATOR_IDS:
            target, components = inventories[epsilon_id]
            rationals = M5274.M5231.root_rationals(event, target)
            for component_id in COMPONENT_IDS:
                component = components[component_id]
                selection = algebraic_component_selector(
                    event,
                    target,
                    component,
                    rationals,
                )
                (
                    pair_mask_active,
                    _,
                    _,
                    _,
                ) = M5277.exact_mask_orientation(
                    selection["selected_labels"],
                    event,
                    surfaces,
                )
                law_active, _, _ = M5278.law_state(
                    laws[component_id],
                    event,
                    surfaces,
                )
                rows.append(
                    {
                        "point_id": point["point_id"],
                        "epsilon_id": epsilon_id,
                        "component_id": component_id,
                        "soft_energy": event["soft_energy"],
                        "soft_cosine": event["soft_cosine"],
                        "decay_cosine": event["decay_cosine"],
                        "selected_role": selection["selected_role"],
                        "representative_root_count": len(
                            selection["representative_roots"]
                        ),
                        "reciprocal_root_count": len(
                            selection["reciprocal_roots"]
                        ),
                        "reciprocal_residual": selection[
                            "reciprocal_residual"
                        ],
                        "selected_root_magnitude": abs(
                            selection["selected_root"]
                        ),
                        "partner_root_magnitude": abs(
                            selection["partner_root"]
                        ),
                        "selected_unit_margin": selection[
                            "selected_unit_margin"
                        ],
                        "representative_alternate_separation": (
                            selection[
                                "representative_alternate_separation"
                            ]
                        ),
                        "reciprocal_alternate_separation": selection[
                            "reciprocal_alternate_separation"
                        ],
                        "law_mask_active": law_active,
                        "selected_pair_mask_active": pair_mask_active,
                        "mask_agrees": (
                            law_active == pair_mask_active
                        ),
                        "away_from_unit_degeneracy": (
                            selection["selected_unit_margin"]
                            > UNIT_DEGENERACY_FLOOR
                        ),
                        "selector_passed": (
                            selection["reciprocal_residual"]
                            <= RECIPROCAL_RESIDUAL_LIMIT
                            and abs(selection["selected_root"])
                            >= 1.0 - 1.0e-12
                            and abs(selection["partner_root"])
                            <= 1.0 + 1.0e-12
                            and law_active == pair_mask_active
                        ),
                        "valid_for_algebraic_branch_selector": True,
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
        SCRIPT_5278,
        RESULT_5278,
        VALIDATION_5278,
        NODE_ROWS_5278,
        LIMIT_ROWS_5275,
        TARGET_POINTS_5275,
    )
    parent = read_json(RESULT_5278)
    parent_validation = read_csv(VALIDATION_5278)
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5278_accepted": bool(parent["acceptance_passed"]),
        "parent_5278_validated": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "parent_eight_component_integrand_accepted": bool(
            parent["claim_boundary"][
                "valid_for_exact_eight_component_integrand"
            ]
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "stress_point_count": STRESS_POINT_COUNT,
        "expected_stress_row_count": (
            STRESS_POINT_COUNT
            * len(REGULATOR_IDS)
            * len(COMPONENT_IDS)
        ),
        "decision": (
            "DRY_RUN_ACCEPTED__PROVE_ALGEBRAIC_BRANCH_SELECTOR"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
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
        raise RuntimeError("5279 dry run did not pass")
    parent = read_json(RESULT_5278)
    theorem = theorem_rows()
    replay = replay_5278_rows() + replay_5275_rows()
    stress = stress_rows()
    maximum_replay_distance = max(
        float(row["root_chordal_distance"]) for row in replay
    )
    maximum_replay_reciprocal = max(
        float(row["reciprocal_residual"]) for row in replay
    )
    maximum_stress_reciprocal = max(
        float(row["reciprocal_residual"]) for row in stress
    )
    minimum_stress_margin = min(
        float(row["selected_unit_margin"]) for row in stress
    )
    minimum_alternate_separation = min(
        min(
            float(row["representative_alternate_separation"]),
            float(row["reciprocal_alternate_separation"]),
        )
        for row in stress
    )
    role_counts: defaultdict[str, int] = defaultdict(int)
    for row in stress:
        role_counts[str(row["selected_role"])] += 1
    checks = {
        "parent_5278_accepted": bool(parent["acceptance_passed"]),
        "theorem_covers_eight_components": (
            len(theorem) == len(COMPONENT_IDS)
            and {
                row["component_id"] for row in theorem
            }
            == set(COMPONENT_IDS)
        ),
        "all_stored_transports_reproduced": (
            bool(replay)
            and all(
                bool(row["selector_reproduces_stored_transport"])
                for row in replay
            )
            and maximum_replay_distance
            <= REPLAY_CHORDAL_LIMIT
        ),
        "all_replay_pairs_reciprocal": (
            maximum_replay_reciprocal
            <= RECIPROCAL_RESIDUAL_LIMIT
        ),
        "complete_stress_matrix": (
            len(stress) == int(dry["expected_stress_row_count"])
        ),
        "all_stress_selectors_pass": all(
            bool(row["selector_passed"]) for row in stress
        ),
        "all_stress_pairs_reciprocal": (
            maximum_stress_reciprocal
            <= RECIPROCAL_RESIDUAL_LIMIT
        ),
        "stress_sample_avoids_degeneracy_sets": (
            minimum_stress_margin > UNIT_DEGENERACY_FLOOR
        ),
        "both_selector_roles_exercised": (
            role_counts["representative"] > 0
            and role_counts["reciprocal"] > 0
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
        "mode": "algebraic-reciprocal-branch-selector",
        "checks": checks,
        "acceptance_passed": accepted,
        "theorem_row_count": len(theorem),
        "stored_replay_row_count": len(replay),
        "stress_point_count": STRESS_POINT_COUNT,
        "stress_row_count": len(stress),
        "maximum_replay_root_chordal_distance": (
            maximum_replay_distance
        ),
        "maximum_replay_reciprocal_residual": (
            maximum_replay_reciprocal
        ),
        "maximum_stress_reciprocal_residual": (
            maximum_stress_reciprocal
        ),
        "minimum_stress_selected_unit_margin": (
            minimum_stress_margin
        ),
        "minimum_stress_alternate_branch_separation": (
            minimum_alternate_separation
        ),
        "stress_selected_role_counts": dict(role_counts),
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
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ACCEPT_ALGEBRAIC_RECIPROCAL_BRANCH_SELECTOR__"
            "REMOVE_PATH_TRANSPORT_FROM_CUBATURE_EVALUATOR"
            if accepted
            else "ALGEBRAIC_BRANCH_SELECTOR_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_algebraic_branch_selection_almost_everywhere": (
                accepted
            ),
            "valid_for_path_transport_elimination_in_cubature": (
                accepted
            ),
            "valid_for_unit_or_collision_degeneracy_sets": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The reciprocal max/min selector exactly reproduces "
                "stored continuation roots and passes a broad interior "
                "stress audit. Unit-circle and multiple-root degeneracy "
                "sets remain measure-zero boundaries handled by the "
                "exact mask/chamber partition, not by this selector."
            ),
        },
    }
    write_csv(THEOREM_ROWS, theorem)
    write_csv(REPLAY_ROWS, replay)
    write_csv(STRESS_ROWS, stress)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": result["mode"],
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
    text = f"""# 5279 — Algebraic reciprocal branch selector

## Purpose

The 5278 integrand was correct, but every cubature node still inherited
an expensive source-to-node continuation. This checkpoint removes that
numerical path dependency.

## Selector

For each component:

1. solve the representative collision equation and choose its
   maximum-modulus root;
2. solve the reciprocal collision equation and choose its
   minimum-modulus root;
3. use the representative when its modulus is at least one, otherwise
   use the reciprocal.

The spinor `u/v` root dictionary and reciprocal component construction
give `R_rep R_rec=1` away from degeneracy sets. The exact Boolean mask
owns the unit-circle boundary.

## Evidence

- Stored high-precision/transport rows replayed:
  `{result['stored_replay_row_count']}`;
- maximum replay chordal distance:
  `{result['maximum_replay_root_chordal_distance']:.12g}`;
- random interior stress rows:
  `{result['stress_row_count']}`;
- maximum stress reciprocal residual:
  `{result['maximum_stress_reciprocal_residual']:.12g}`;
- minimum selected-root unit margin:
  `{result['minimum_stress_selected_unit_margin']:.12g}`;
- selected roles:
  `{result['stress_selected_role_counts']}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

The selector is an almost-everywhere algebraic replacement for branch
transport in volume cubature. It is not a theorem on the unit-circle or
multiple-root degeneracy sets and does not establish the phase-space
coefficient, UV coefficient, local GR, or full MTS framework. Its
practical consequence is important: the next energy-first calculation
can spend its cost on pole subtraction and convergence rather than
thousands of continuation steps.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5278)
    required_csvs = (THEOREM_ROWS, REPLAY_ROWS, STRESS_ROWS)
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
        sort_keys=True,
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
            "PARENT_5278_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "ALGEBRAIC_SELECTOR_ACCEPTED",
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
            "STORED_REPLAY_EXACT",
            float(
                result["maximum_replay_root_chordal_distance"]
            )
            <= REPLAY_CHORDAL_LIMIT,
            (
                f"{result['stored_replay_row_count']} rows; "
                f"max={result['maximum_replay_root_chordal_distance']}"
            ),
        ),
        validation_gate(
            "STRESS_MATRIX_COMPLETE",
            int(result["stress_row_count"])
            == (
                STRESS_POINT_COUNT
                * len(REGULATOR_IDS)
                * len(COMPONENT_IDS)
            ),
            f"{result['stress_row_count']} rows",
        ),
        validation_gate(
            "RECIPROCAL_IDENTITY_CONTROLLED",
            float(result["maximum_stress_reciprocal_residual"])
            <= RECIPROCAL_RESIDUAL_LIMIT,
            (
                "max="
                f"{result['maximum_stress_reciprocal_residual']}"
            ),
        ),
        validation_gate(
            "PATH_TRANSPORT_ELIMINATION_AUTHORIZED",
            bool(
                result["claim_boundary"][
                    "valid_for_path_transport_elimination_in_cubature"
                ]
            ),
            "algebraic selector accepted almost everywhere",
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
            "state": "COMPLETED",
            "mode": "validation",
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
            "VALIDATED_ALGEBRAIC_RECIPROCAL_BRANCH_SELECTOR"
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
