from __future__ import annotations

import argparse
import copy
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable


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
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5286"

SCRIPT_5285 = (
    SCRIPTS / "Y5_R2FR_5285_channel_derivative_material_pole_residues.py"
)
RESULT_5285 = (
    FUNCTIONAL_RG / "5285" / "channel_derivative_residue_result.json"
)
VALIDATION_5285 = (
    FUNCTIONAL_RG / "5285" / "channel_derivative_residue_validation.csv"
)
ROOTS_5285 = (
    FUNCTIONAL_RG / "5285" / "refined_channel_poles_and_derivatives.csv"
)

DRY_RUN = SOURCE / "angular_node_pole_atlas_dry_run.json"
NODE_ROWS = SOURCE / "angular_order2_nodes.csv"
POLE_ROWS = SOURCE / "angular_node_material_pole_atlas.csv"
PANEL_ROWS = SOURCE / "angular_node_energy_panel_contract.csv"
RESULT = SOURCE / "angular_node_pole_atlas_result.json"
VALIDATION = SOURCE / "angular_node_pole_atlas_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5286_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5286-Y5-R2FR-angular-node-material-pole-atlas-preflight.md"

CHECKPOINT = 5286
PARENT_CHECKPOINT = 5285
MARKER = "MTS_5286_ANGULAR_NODE_MATERIAL_POLE_ATLAS_PREFLIGHT"
REVISION = "angular-node-material-pole-atlas-preflight-v1"
REGULATOR_IDS = ("E040", "E020")
MATERIAL_COMPONENT_IDS = ("MC04", "MC12")
ANGULAR_ORDER = 2
ENERGY_SCAN_POINTS = 801
CHANNEL_ROOT_RESIDUAL_LIMIT = 1.0e-10
NEAR_ZERO_WITHOUT_CROSSING_LIMIT = 1.0e-4
REGULATOR_ROOT_MATCH_LIMIT = 1.0e-5
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


M5285 = load_module("mts_5285_for_5286", SCRIPT_5285)
M5280 = M5285.M5280
M5283 = M5285.M5283
M5267 = M5285.M5267
np = M5280.np


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5285,
        RESULT_5285,
        VALIDATION_5285,
        ROOTS_5285,
        M5267.MANIFEST_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def angular_nodes() -> list[dict[str, Any]]:
    nodes, weights = np.polynomial.legendre.leggauss(ANGULAR_ORDER)
    limit = float(M5280.M5274.M5270.ANGULAR_LIMIT)
    rows: list[dict[str, Any]] = []
    for soft_index, (soft_node, soft_weight) in enumerate(
        zip(nodes, weights),
        start=1,
    ):
        for decay_index, (decay_node, decay_weight) in enumerate(
            zip(nodes, weights),
            start=1,
        ):
            rows.append(
                {
                    "angular_node_id": (
                        f"A{ANGULAR_ORDER:02d}_"
                        f"S{soft_index:02d}_D{decay_index:02d}"
                    ),
                    "soft_cosine": limit * float(soft_node),
                    "decay_cosine": limit * float(decay_node),
                    "angular_weight": (
                        limit
                        * float(soft_weight)
                        * limit
                        * float(decay_weight)
                    ),
                    "angular_jacobian": M5280.M5278.ANGULAR_JACOBIAN,
                    "valid_for_angular_pole_preflight": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def source_jobs() -> dict[tuple[str, str], dict[str, Any]]:
    manifest = M5267.read_json(M5267.MANIFEST_5239)
    return {
        (epsilon_id, component_id): next(
            job
            for job in manifest["jobs"]
            if job["epsilon_id"] == epsilon_id
            and job["component_id"] == component_id
        )
        for epsilon_id in REGULATOR_IDS
        for component_id in MATERIAL_COMPONENT_IDS
    }


def material_surface_ids() -> dict[tuple[str, str], str]:
    return {
        (row["epsilon_id"], row["component_id"]): row["surface_id"]
        for row in read_csv(ROOTS_5285)
    }


def angular_problem(
    source_job: dict[str, Any],
    soft_cosine: float,
    decay_cosine: float,
) -> dict[str, Any]:
    modified = copy.deepcopy(source_job)
    modified["soft_cosine"] = soft_cosine
    modified["decay_cosine"] = decay_cosine
    problem = M5267.M5239.build_problem(M5267.energy_job(modified))
    M5267.install_paired_track(problem)
    return problem


def channel_function(
    problem: dict[str, Any],
    surface_id: str,
) -> Callable[[complex], complex]:
    return lambda coordinate: complex(
        M5267.M5239.owner_surface_values(
            problem,
            complex(coordinate),
        )[surface_id]
    )


def bisection_seed(
    channel: Callable[[complex], complex],
    left: float,
    right: float,
) -> float:
    left_value = channel(complex(left)).real
    for _ in range(60):
        midpoint = 0.5 * (left + right)
        midpoint_value = channel(complex(midpoint)).real
        if left_value * midpoint_value <= 0.0:
            right = midpoint
        else:
            left = midpoint
            left_value = midpoint_value
    return 0.5 * (left + right)


def newton_root(
    channel: Callable[[complex], complex],
    seed: complex,
) -> tuple[complex, int, float]:
    root = seed
    for iteration in range(1, 13):
        step = 1.0e-6
        derivative = (
            channel(root + step) - channel(root - step)
        ) / (2.0 * step)
        root -= channel(root) / derivative
        residual = abs(channel(root))
        if residual <= CHANNEL_ROOT_RESIDUAL_LIMIT:
            return root, iteration, residual
    return root, 12, abs(channel(root))


def locate_material_poles(
    node: dict[str, Any],
    source_job_lookup: dict[tuple[str, str], dict[str, Any]],
    surface_lookup: dict[tuple[str, str], str],
) -> list[dict[str, Any]]:
    minimum = float(M5280.M5274.M5267.ENERGY_MINIMUM)
    maximum = float(M5280.M5274.M5267.ENERGY_MAXIMUM)
    coordinates = np.linspace(minimum, maximum, ENERGY_SCAN_POINTS)
    rows: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        for component_id in MATERIAL_COMPONENT_IDS:
            key = (epsilon_id, component_id)
            problem = angular_problem(
                source_job_lookup[key],
                float(node["soft_cosine"]),
                float(node["decay_cosine"]),
            )
            surface_id = surface_lookup[key]
            channel = channel_function(problem, surface_id)
            values = [channel(complex(float(value))) for value in coordinates]
            signs = [
                index
                for index in range(len(coordinates) - 1)
                if values[index].real * values[index + 1].real < 0.0
            ]
            roots: list[complex] = []
            root_iterations: list[int] = []
            root_residuals: list[float] = []
            for index in signs:
                real_seed = bisection_seed(
                    channel,
                    float(coordinates[index]),
                    float(coordinates[index + 1]),
                )
                root, iterations, residual = newton_root(
                    channel,
                    complex(real_seed),
                )
                if (
                    minimum < root.real < maximum
                    and all(abs(root - existing) > 1.0e-7 for existing in roots)
                ):
                    roots.append(root)
                    root_iterations.append(iterations)
                    root_residuals.append(residual)
            magnitudes = np.abs(np.asarray(values, dtype=np.complex128))
            minimum_index = int(np.argmin(magnitudes))
            minimum_magnitude = float(magnitudes[minimum_index])
            ambiguous = (
                not roots
                and minimum < float(coordinates[minimum_index]) < maximum
                and minimum_magnitude <= NEAR_ZERO_WITHOUT_CROSSING_LIMIT
            )
            if not roots:
                rows.append(
                    {
                        "angular_node_id": node["angular_node_id"],
                        "soft_cosine": node["soft_cosine"],
                        "decay_cosine": node["decay_cosine"],
                        "epsilon_id": epsilon_id,
                        "component_id": component_id,
                        "surface_id": surface_id,
                        "pole_index": 0,
                        "pole_present": False,
                        "pole_real": "",
                        "pole_imaginary": "",
                        "channel_root_residual": "",
                        "channel_derivative_real": "",
                        "channel_derivative_imaginary": "",
                        "newton_iterations": 0,
                        "real_sign_change_count": len(signs),
                        "minimum_real_scan_magnitude": minimum_magnitude,
                        "minimum_real_scan_energy": float(
                            coordinates[minimum_index]
                        ),
                        "near_zero_without_crossing": ambiguous,
                        "valid_for_angular_pole_preflight": not ambiguous,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
                continue
            for pole_index, (root, iterations, residual) in enumerate(
                zip(roots, root_iterations, root_residuals),
                start=1,
            ):
                step = 1.0e-6
                derivative = (
                    channel(root + step) - channel(root - step)
                ) / (2.0 * step)
                rows.append(
                    {
                        "angular_node_id": node["angular_node_id"],
                        "soft_cosine": node["soft_cosine"],
                        "decay_cosine": node["decay_cosine"],
                        "epsilon_id": epsilon_id,
                        "component_id": component_id,
                        "surface_id": surface_id,
                        "pole_index": pole_index,
                        "pole_present": True,
                        "pole_real": root.real,
                        "pole_imaginary": root.imag,
                        "channel_root_residual": residual,
                        "channel_derivative_real": derivative.real,
                        "channel_derivative_imaginary": derivative.imag,
                        "newton_iterations": iterations,
                        "real_sign_change_count": len(signs),
                        "minimum_real_scan_magnitude": minimum_magnitude,
                        "minimum_real_scan_energy": float(
                            coordinates[minimum_index]
                        ),
                        "near_zero_without_crossing": False,
                        "valid_for_angular_pole_preflight": (
                            residual <= CHANNEL_ROOT_RESIDUAL_LIMIT
                        ),
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return rows


def panel_contract_rows(
    nodes: list[dict[str, Any]],
    poles: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    base_context = M5280.source_context()
    rows: list[dict[str, Any]] = []
    for node in nodes:
        context = dict(base_context)
        event = dict(base_context["source_event"])
        event["soft_cosine"] = float(node["soft_cosine"])
        event["decay_cosine"] = float(node["decay_cosine"])
        context["source_event"] = event
        masks = M5280.exact_energy_mask_boundaries(context)
        local_poles = [
            {
                "center": float(row["pole_real"]),
            }
            for row in poles
            if row["angular_node_id"] == node["angular_node_id"]
            and parse_bool(row["pole_present"])
        ]
        panels = M5280.composite_panel_rows(masks, local_poles)
        rows.append(
            {
                "angular_node_id": node["angular_node_id"],
                "soft_cosine": node["soft_cosine"],
                "decay_cosine": node["decay_cosine"],
                "exact_energy_mask_boundary_count": len(masks),
                "material_pole_count": len(local_poles),
                "energy_panel_count": len(panels),
                "maximum_energy_panel_width": max(
                    float(row["width"]) for row in panels
                ),
                "valid_for_inner_energy_runner": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def regulator_pattern_checks(
    poles: list[dict[str, Any]],
) -> tuple[bool, float]:
    maximum_separation = 0.0
    passed = True
    for node_id in {row["angular_node_id"] for row in poles}:
        for component_id in MATERIAL_COMPONENT_IDS:
            local = [
                row
                for row in poles
                if row["angular_node_id"] == node_id
                and row["component_id"] == component_id
            ]
            counts = {
                epsilon_id: sum(
                    parse_bool(row["pole_present"])
                    for row in local
                    if row["epsilon_id"] == epsilon_id
                )
                for epsilon_id in REGULATOR_IDS
            }
            passed = passed and counts["E040"] == counts["E020"]
            E040 = [
                float(row["pole_real"])
                for row in local
                if row["epsilon_id"] == "E040"
                and parse_bool(row["pole_present"])
            ]
            E020 = [
                float(row["pole_real"])
                for row in local
                if row["epsilon_id"] == "E020"
                and parse_bool(row["pole_present"])
            ]
            for first, second in zip(sorted(E040), sorted(E020)):
                separation = abs(first - second)
                maximum_separation = max(maximum_separation, separation)
                passed = passed and separation <= REGULATOR_ROOT_MATCH_LIMIT
    return passed, maximum_separation


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5285,
        RESULT_5285,
        VALIDATION_5285,
        ROOTS_5285,
        M5267.MANIFEST_5239,
    )
    parent = read_json(RESULT_5285)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5285_accepted": bool(parent["acceptance_passed"]),
        "parent_5285_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5285)
        ),
        "channel_residue_certificate_passed": bool(
            parent["channel_derivative_residue_certificate_passed"]
        ),
        "four_order2_angular_nodes": len(angular_nodes()) == 4,
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
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
        "decision": (
            "DRY_RUN_ACCEPTED__BUILD_ORDER2_ANGULAR_POLE_ATLAS"
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
        raise RuntimeError("5286 dry run did not pass")
    parent = read_json(RESULT_5285)
    nodes = angular_nodes()
    jobs = source_jobs()
    surfaces = material_surface_ids()
    poles: list[dict[str, Any]] = []
    for node in nodes:
        poles.extend(locate_material_poles(node, jobs, surfaces))
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "last_angular_node_id": node["angular_node_id"],
                "pole_row_count": len(poles),
            },
        )
    panel_rows = panel_contract_rows(nodes, poles)
    pattern_passed, maximum_regulator_separation = (
        regulator_pattern_checks(poles)
    )
    present = [row for row in poles if parse_bool(row["pole_present"])]
    maximum_root_residual = max(
        (
            float(row["channel_root_residual"]) for row in present
        ),
        default=0.0,
    )
    ambiguous_count = sum(
        parse_bool(row["near_zero_without_crossing"]) for row in poles
    )
    patterns = {
        node["angular_node_id"]: sorted(
            {
                row["component_id"]
                for row in poles
                if row["angular_node_id"] == node["angular_node_id"]
                and parse_bool(row["pole_present"])
            }
        )
        for node in nodes
    }
    checks = {
        "all_four_angular_nodes_completed": (
            {row["angular_node_id"] for row in poles}
            == {row["angular_node_id"] for row in nodes}
        ),
        "all_material_channels_classified": len(poles) >= 16,
        "all_present_roots_converged": (
            maximum_root_residual <= CHANNEL_ROOT_RESIDUAL_LIMIT
        ),
        "no_unresolved_near_zero_without_crossing": ambiguous_count == 0,
        "regulator_root_patterns_match": pattern_passed,
        "all_inner_panel_contracts_nonempty": all(
            int(row["energy_panel_count"]) > 0 for row in panel_rows
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "angular-node-material-pole-atlas-preflight",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_node_count": len(nodes),
        "material_channel_classification_row_count": len(poles),
        "present_material_pole_count": len(present),
        "absent_material_channel_count": len(poles) - len(present),
        "ambiguous_channel_count": ambiguous_count,
        "maximum_channel_root_residual": maximum_root_residual,
        "maximum_E040_E020_real_pole_separation": (
            maximum_regulator_separation
        ),
        "angular_node_component_patterns": patterns,
        "panel_contracts": panel_rows,
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == str(parent["formalization_workbench_end_digest"])
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
            "ACCEPT_ORDER2_ANGULAR_POLE_ATLAS__RUN_INNER_ENERGY_SMOKE"
            if accepted
            else "ANGULAR_POLE_ATLAS_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_order2_angular_pole_atlas": accepted,
            "valid_for_inner_energy_smoke": accepted,
            "valid_for_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This locates material channel poles and exact energy "
                "panels at the order-two angular nodes; no residue or "
                "inner energy integral is evaluated here."
            ),
        },
    }
    write_csv(NODE_ROWS, nodes)
    write_csv(POLE_ROWS, poles)
    write_csv(PANEL_ROWS, panel_rows)
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
    return {"gate_id": gate_id, "passed": passed, "detail": detail}


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    patterns = "\n".join(
        f"- `{node_id}`: `{components}`"
        for node_id, components in result[
            "angular_node_component_patterns"
        ].items()
    )
    text = f"""# 5286 — Angular-node material-pole atlas preflight

## Purpose

The fixed-angle source result cannot simply be copied across the angular
domain. This checkpoint rebuilds the energy-channel geometry at each
order-two angular Gauss node, scans for interior channel zeros, refines
each detected complex pole, and builds the exact-mask energy-panel
contract required by an inner integrator.

## Pole-presence patterns

{patterns}

- present material poles:
  `{result['present_material_pole_count']}`;
- absent material channels:
  `{result['absent_material_channel_count']}`;
- unresolved near-zero channels:
  `{result['ambiguous_channel_count']}`;
- maximum channel-root residual:
  `{result['maximum_channel_root_residual']:.12g}`;
- maximum E040/E020 real-pole separation:
  `{result['maximum_E040_E020_real_pole_separation']:.12g}`.

Decision:
`{result['decision']}`.

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This is a working pole atlas and panel preflight. It does not yet claim
angular convergence or a full phase-space coefficient.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    required_csvs = (NODE_ROWS, POLE_ROWS, PANEL_ROWS)
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
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
    source_files = result["source_files"]
    current_formal_digest = M5283.formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
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
            "PARENT_5285_CERTIFIED",
            bool(
                read_json(RESULT_5285)[
                    "channel_derivative_residue_certificate_passed"
                ]
            ),
            str(read_json(RESULT_5285)["decision"]),
        ),
        validation_gate(
            "POLE_ATLAS_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            len(csv_rows) == len(required_csvs) and all(csv_rows.values()),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "NO_AMBIGUOUS_CHANNELS",
            result["ambiguous_channel_count"] == 0,
            str(result["ambiguous_channel_count"]),
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
                and result["resource_contract"]["worker_math_threads"] == 1
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
            "VALIDATED_ANGULAR_NODE_MATERIAL_POLE_ATLAS"
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
